#!/usr/bin/env python3
import os
import shutil
import argparse
from pathlib import Path

HOME = Path.home()
BIN_DIRS = [HOME / ".local" / "bin", HOME / "bin"]
CONFIG_DIRS = [
    HOME / ".config",
    HOME / ".local" / "share",
    HOME / ".cache",
    HOME / ".local" / "state"
]
EXCLUDES = [
    # User
    'android',
    'dotfiles',
    'termux',

    # System
    'man',
    'gtk-3.0',
    'dconf',
    'pulse',
    'systemd',
    'user-dirs.dirs',
    'mozila',
    'firefox',
    'chrome',
    'brave',
]

class Colors:
    BLUE = '\033[94m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    RESET = '\033[0m'

def find_local_binaries():
    binaries = set()
    for directory in BIN_DIRS:
        if directory.exists() and directory.is_dir():
            for file_path in directory.iterdir():
                if file_path.is_file() and os.access(file_path, os.X_OK):
                    binaries.add(file_path.name)
    return binaries

def find_configuration_paths():
    configs = {}
    for directory in CONFIG_DIRS:
        if directory.exists() and directory.is_dir():
            for folder_path in directory.iterdir():
                if folder_path.is_dir():
                    configs.setdefault(folder_path.name, []).append(folder_path)

    for path in HOME.glob(".*"):
        if path.is_dir() and path.name not in [".", "..", ".config", ".local", ".cache"]:
            clean_name = path.name.lstrip(".")
            configs.setdefault(clean_name, []).append(path)

    return configs

def inspect_system_apps():
    binaries = find_local_binaries()
    configs = find_configuration_paths()

    installed_apps = {}
    residual_configs = {}

    all_app_names = set(binaries) | set(configs.keys())
    ignored_system_names = EXCLUDES

    for app_name in all_app_names:
        matched_paths = configs.get(app_name, [])
        for bin_dir in BIN_DIRS:
            binary_file = bin_dir / app_name
            if binary_file.exists():
                matched_paths.append(binary_file)

        if app_name in binaries:
            installed_apps[app_name] = matched_paths
        elif app_name not in ignored_system_names and not shutil.which(app_name):
            residual_configs[app_name] = matched_paths

    return installed_apps, residual_configs

def list_apps_command():
    installed_apps, residual_configs = inspect_system_apps()

    print(f"\n{Colors.BLUE}=== Installed Home Binaries ==={Colors.RESET}")
    if installed_apps:
        for app_name, paths in sorted(installed_apps.items()):
            print(f"{Colors.GREEN}● {app_name}{Colors.RESET} ({len(paths)} items mapped)")
    else:
        print("No local binaries found in ~/.local/bin or ~/bin")

    print(f"\n{Colors.YELLOW}=== Residual Configurations (Orphaned) ==={Colors.RESET}")
    if residual_configs:
        for app_name, paths in sorted(residual_configs.items()):
            print(f"○ {app_name} -> {Colors.RED}{len(paths)} orphaned paths{Colors.RESET}")
    else:
        print("Your home directory is clean!")
    print()

def remove_app_command(target_app):
    installed_apps, residual_configs = inspect_system_apps()
    paths_to_remove = installed_apps.get(target_app, []) or residual_configs.get(target_app, [])

    if not paths_to_remove:
        print(f"{Colors.RED}No binaries or configuration files found for '{target_app}'.{Colors.RESET}")
        return

    print(f"\n{Colors.YELLOW}The following paths were found for '{target_app}':{Colors.RESET}")
    for path in paths_to_remove:
        item_type = "Dir " if path.is_dir() else "File"
        print(f"  [{item_type}] {path}")

    print(f"\n{Colors.RED}WARNING: This action cannot be undone!{Colors.RESET}")
    confirmation = input("Are you sure you want to delete everything listed above? [y/N]: ")

    if confirmation.strip().lower() in ['y', 'yes']:
        for path in paths_to_remove:
            try:
                if path.is_dir():
                    shutil.rmtree(path)
                else:
                    path.unlink()
                print(f"{Colors.GREEN}Removed:{Colors.RESET} {path}")
            except Exception as error:
                print(f"{Colors.RED}Error removing {path}:{Colors.RESET} {error}")
        print(f"\n{Colors.GREEN}Cleanup completed!{Colors.RESET}")
    else:
        print("Operation cancelled.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Standalone Home App & Configuration Manager")
    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    subparsers.add_parser("list", help="List installed local apps and residual configurations")

    remove_parser = subparsers.add_parser("remove", help="Remove an app and all its configurations")
    remove_parser.add_argument("app", help="Target app name to remove")

    args = parser.parse_args()

    if args.command == "list":
        list_apps_command()
    elif args.command == "remove":
        remove_app_command(args.app)
    else:
        parser.print_help()
