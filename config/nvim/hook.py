"""Hook do nvim: dependências de sistema dos plugins.

Ripgrep é exigido pelo grug-far (search & replace) e acelera o
mini.pick (files/grep_live). Instala pelo gerenciador do sistema.
"""

from shared.packages import install

# nomes divergentes entre distros vão no dict; ausentes usam "ripgrep"
RIPGREP_PKGS = {
    "apt": "ripgrep",
    "apt-get": "ripgrep",
    "dnf": "ripgrep",
    "yum": "ripgrep",
    "pacman": "ripgrep",
    "apk": "ripgrep",
    "zypper": "ripgrep",
    "brew": "ripgrep",
    "pkg": "ripgrep",
}


def main(dry_run: bool):
    install(RIPGREP_PKGS, managers=RIPGREP_PKGS, check="rg", dry_run=dry_run)
