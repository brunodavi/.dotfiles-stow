#!/usr/bin/env python3
import argparse
import importlib.util
import pathlib
import shutil
import sys

from shared.utils import create_symlink

REPO_ROOT = pathlib.Path(__file__).resolve().parent
HOME = pathlib.Path.home()

LINKS = {
    "config/nvim": ".config/nvim",
    "config/starship.toml": ".config/starship.toml",
    "git/gitconfig": ".gitconfig",
}

DEFAULT_HOOKS = ["shell", "termux"]

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
    return normalized.lower()

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

def find_hook_for_source(source):
    if source.is_dir():
        candidate = source / "hook.py"
        if candidate.exists():
            return candidate
    else:
        candidate = source.parent / "hook.py"
        if candidate.exists():
            return candidate
    return None

def install():
    args = parse_arguments()
    dry_run = args.dry_run
    selected = args.modules
    if selected:
        normalized_selected = [normalize_module_name(s) for s in selected]
        filtered = {}
        matched_selected = set()
        for source_key, target_rel in LINKS.items():
            source_path = pathlib.Path(source_key)
            candidates = {
                source_key.lower(),
                source_path.name.lower(),
                source_path.stem.lower(),
                source_path.parent.name.lower(),
            }
            for sel in normalized_selected:
                if sel in candidates or sel == source_path.name.lower() or sel == source_path.stem.lower() or sel in source_key.lower():
                    filtered[source_key] = target_rel
                    matched_selected.add(sel)
                    break
        for sel in normalized_selected:
            if sel not in matched_selected and sel not in [normalize_module_name(h) for h in DEFAULT_HOOKS]:
                print(f"Warning: unknown module '{sel}' skipped")
        links_to_install = filtered
        matched_hooks = [h for h in DEFAULT_HOOKS if normalize_module_name(h) in normalized_selected]
        hooks_to_run = matched_hooks
    else:
        links_to_install = LINKS
        hooks_to_run = DEFAULT_HOOKS
    for source_key, target_rel in sorted(links_to_install.items()):
        source = REPO_ROOT / source_key
        target = HOME / target_rel
        if not source.exists():
            print(f"Warning: source {source} does not exist skipped")
            continue
        create_symlink(source, target, dry_run)
        hook_path = find_hook_for_source(source)
        if hook_path is not None:
            load_hook_and_run(hook_path, dry_run)
    for hook_name in hooks_to_run:
        hook_path = REPO_ROOT / hook_name / "hook.py"
        if hook_path.exists():
            load_hook_and_run(hook_path, dry_run)
    if dry_run:
        print("Dry run completed")
    else:
        print("Installation completed")

if __name__ == "__main__":
    install()
