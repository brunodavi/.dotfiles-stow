"""Hook do tmux: instala o binário e clona os plugins de persistência.

resurrect + continuum salvam a árvore de sessões em disco (sessões,
janelas, layout de painéis, diretórios e programas rodando), então o
estado sobrevive a reboot/fechar o proot. Clonamos direto, sem tpm,
porque os dois são sourceados manualmente no tmux.conf.
"""

import pathlib
import subprocess

from shared.packages import install

PLUGINS = {
    "tmux-resurrect": "https://github.com/tmux-plugins/tmux-resurrect",
    "tmux-continuum": "https://github.com/tmux-plugins/tmux-continuum",
}


def _git_clone(url: str, target: pathlib.Path, dry_run: bool):
    if target.exists() and any(target.iterdir()):
        print(f"[tmux] plugin {target.name} já clonado, pulando")
        return
    cmd = ["git", "clone", "--depth", "1", url, str(target)]
    if dry_run:
        print(f"[packages] (dry-run) {' '.join(cmd)}")
        return
    result = subprocess.run(cmd)
    if result.returncode == 0:
        print(f"[tmux] clone ok: {target.name}")


def main(dry_run: bool):
    install("tmux", check="tmux", dry_run=dry_run)
    install("git", check="git", dry_run=dry_run)

    plugins_dir = pathlib.Path.home() / ".tmux" / "plugins"
    if not dry_run:
        plugins_dir.mkdir(parents=True, exist_ok=True)
    for name, url in PLUGINS.items():
        _git_clone(url, plugins_dir / name, dry_run)
