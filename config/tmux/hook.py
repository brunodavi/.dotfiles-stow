"""Hook do tmux: garante o binário instalado no sistema (termux/linux)."""

from shared.packages import install


def main(dry_run: bool):
    install("tmux", check="tmux", dry_run=dry_run)
