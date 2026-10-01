from pathlib import Path
from shared.utils import create_symlink


def main(dry_run: bool):
    home = Path.home()

    if 'com.termux' not in str(home):
        return

    repo_root = Path(__file__).resolve().parent.parent

    target = repo_root / 'termux'
    dest = home / '.termux'

    create_symlink(target, dest, dry_run)
