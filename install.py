#!/usr/bin/env python3
import argparse
import importlib.util
import pathlib
import shutil
import sys

REPO_ROOT = pathlib.Path(__file__).resolve().parent
HOME = pathlib.Path.home()

EXCLUDES = [
    ".git",
    ".gitignore",
    "README.md",
    "LICENSE",
    "install.py",
    "install.sh",
    "__pycache__",
    ".venv",
    "venv",
    "shell",
]

def parse_arguments():
    parser = argparse.ArgumentParser(description="Dotfiles installer")
    parser.add_argument("modules", nargs="*", help="modules to install (default: all)")
    parser.add_argument("--dry-run", action="store_true", help="show what would be done without making changes")
    return parser.parse_args()

def normalize_module_name(name):
    normalized = name
    if normalized.startswith("dot_"):
        normalized = normalized[4:]
    if normalized.startswith("."):
        normalized = normalized[1:]
    return normalized

def get_available_modules():
    modules = {}
    for entry in REPO_ROOT.iterdir():
        if entry.name in EXCLUDES:
            continue
        if not entry.name.startswith("dot_"):
            continue
        normalized = normalize_module_name(entry.name)
        modules[normalized] = entry
    return modules

def create_symlink(source, target, dry_run):
    if dry_run:
        print(f"Would link {source} -> {target}")
        return
    target.parent.mkdir(parents=True, exist_ok=True)
    if target.is_symlink() or target.exists():
        if target.is_symlink() and target.resolve() == source.resolve():
            print(f"Symlink already correct {target} -> {source}")
            return
        if target.is_symlink():
            target.unlink()
        elif target.is_dir():
            shutil.rmtree(target)
        else:
            target.unlink()
    target.symlink_to(source)
    print(f"Linked {source} -> {target}")

def load_hook_and_run(hook_path, dry_run):
    spec = importlib.util.spec_from_file_location("hook", hook_path)
    if spec is None or spec.loader is None:
        print(f"Failed to load hook {hook_path}")
        return
    module = importlib.util.module_from_spec(spec)
    sys.modules["hook"] = module
    spec.loader.exec_module(module)
    if not hasattr(module, "main"):
        print(f"Hook {hook_path} has no main function")
        return
    print(f"Running hook {hook_path}")
    module.main(dry_run)

def install():
    args = parse_arguments()
    dry_run = args.dry_run
    selected = args.modules
    available = get_available_modules()
    if selected:
        normalized_selected = [normalize_module_name(s) for s in selected]
        filtered = {}
        shell_requested = False
        for name in normalized_selected:
            if name == "shell":
                shell_requested = True
                continue
            if name in available:
                filtered[name] = available[name]
            else:
                print(f"Warning: unknown module '{name}' skipped")
        modules_to_install = filtered
        install_shell = shell_requested
    else:
        modules_to_install = available
        install_shell = True
    for name, source in sorted(modules_to_install.items()):
        target = HOME / f".{name}"
        create_symlink(source, target, dry_run)
        hook_path = source / "hook.py" if source.is_dir() else None
        if hook_path is not None and hook_path.exists():
            load_hook_and_run(hook_path, dry_run)
    if install_shell:
        hook_path = REPO_ROOT / "shell" / "hook.py"
        if hook_path.exists():
            load_hook_and_run(hook_path, dry_run)
    if dry_run:
        print("Dry run completed")
    else:
        print("Installation completed")

if __name__ == "__main__":
    install()
