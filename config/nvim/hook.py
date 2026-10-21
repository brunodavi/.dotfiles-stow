"""Hook do nvim: o próprio Neovim + dependências de sistema dos plugins.

- nvim: termux/alpine via gerenciador de pacotes; nas demais distros o
  pacote costuma ser velho, então a release oficial vai pra /opt via
  shared.nvim (shell/env.sh já coloca /opt no PATH na frente).
- ripgrep: exigido pelo grug-far (search & replace) e acelera o
  mini.pick (files/grep_live). Instala pelo gerenciador do sistema.
"""

from shared.nvim import install as install_nvim

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
    install_nvim(dry_run=dry_run)

    from shared.packages import install
    install(RIPGREP_PKGS, managers=RIPGREP_PKGS, check="rg", dry_run=dry_run)
