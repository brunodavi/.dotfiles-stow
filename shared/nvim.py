"""Instalador do Neovim (shared/nvim) pra hooks dos dotfiles.

- termux/alpine: usa o gerenciador de pacotes (os repositórios desses
  ambientes acompanham a versão recente).
- outros linux (ubuntu/debian/fedora...): o pacote costuma ser velho,
  então baixa a última release do GitHub e extrai em /opt/nvim-linux-*,
  lugar que shell/env.sh já coloca no PATH na frente, pra vencer o
  nvim velho do sistema.

Uso no hook:
    from shared.nvim import install
    install(dry_run=dry_run)
"""

import os
import pathlib
import platform
import shutil
import subprocess
import tempfile
import urllib.error

from shared import github
from shared.packages import install as install_pkg

REPO = "neovim/neovim"

# (dir dentro do tarball, nome do asset) por arquitetura
ARCH_TAR = {
    "x86_64": ("nvim-linux-x86_64", "nvim-linux-x86_64.tar.gz"),
    "aarch64": ("nvim-linux-arm64", "nvim-linux-arm64.tar.gz"),
}

# gerenciadores cujo nvim no repo costuma estar atualizado
PM_FRESH = ("pkg", "apk")


def _root_prefix():
    """[] quando somos root, ["sudo"] quando disponível, None se impossível."""
    if os.geteuid() == 0:
        return []
    if shutil.which("sudo"):
        return ["sudo"]
    return None


def _version(binary):
    """Versão instalada ("v0.11.5") lida do --version — None se falhar."""
    if not binary:
        return None
    result = subprocess.run(
        [str(binary), "--version"], capture_output=True, text=True
    )
    for line in (result.stdout or "").splitlines():
        if line.startswith("NVIM"):
            return line.split()[-1]
    return None


def _current(arch_dir):
    """Versão em uso no PATH — /opt vence (o env.sh o coloca na frente)."""
    do_opt = pathlib.Path("/opt") / arch_dir / "bin" / "nvim"
    if do_opt.exists():
        return _version(do_opt)
    return _version(shutil.which("nvim"))


def install(dry_run=False):
    """Instala/atualiza o nvim do jeito certo pro sistema. True se rodou."""
    arch = platform.machine()
    if shutil.which("pkg") or shutil.which("apk"):
        return install_pkg("neovim", check="nvim", dry_run=dry_run)

    if arch not in ARCH_TAR:
        print(f"[nvim] arquitetura '{arch}' sem tarball mapeado; pulando")
        return False
    arch_dir, tar_name = ARCH_TAR[arch]

    prefix = _root_prefix()
    if prefix is None:
        print("[nvim] /opt requer root ou sudo; pulando")
        return False

    try:
        release = github.api(REPO)
    except (urllib.error.URLError, OSError) as erro:
        print(f"[nvim] sem acesso ao GitHub ({erro}); pulando")
        return False
    tag = release["tag_name"]

    if _current(arch_dir) == tag:
        print(f"[nvim] nvim {tag} já instalado, pulando")
        return False

    if dry_run:
        print(f"[packages] (dry-run) {tar_name} ({tag}) -> /opt/{arch_dir}")
        return True

    url = github.asset_url(release, tar_name)
    if url is None:
        print(f"[nvim] release {tag} sem o asset {tar_name}; pulando")
        return False

    staging = pathlib.Path(tempfile.mkdtemp(prefix="dotfiles-nvim-"))
    tarball = staging / tar_name
    github.download(url, tarball)
    if not github.checksum(release, tarball):
        print(f"[nvim] checksum falhou; artefato descartado ({staging})")
        return False
    if not github.extract(tarball, staging):
        return False

    origem = staging / arch_dir
    if not origem.exists():
        print(f"[nvim] tarball inesperado (sem {arch_dir}/); ({staging})")
        return False

    destino = pathlib.Path("/opt") / arch_dir
    if destino.exists():
        subprocess.run(prefix + ["rm", "-rf", str(destino)], check=True)
    subprocess.run(prefix + ["mv", str(origem), str(destino)], check=True)
    shutil.rmtree(staging)
    print(f"[nvim] nvim {tag} instalado em {destino}")
    return True
