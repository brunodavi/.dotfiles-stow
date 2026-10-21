"""Helper universal de GitHub releases pra hooks dos dotfiles.

Baixa e instala artefatos de releases: info da release, download de
assets, conferência contra o SHA256SUMS oficial e extração de arquivos.
Tudo com a stdlib (urllib/tarfile/zipfile), sem depender de curl/jq.

Uso:
    from shared.github import api, asset_url, download, checksum, extract

    release = api("neovim/neovim")                      # última release
    url = asset_url(release, "nvim-linux-x86_64.tar.gz")
    download(url, "/tmp/f.tar.gz")
    checksum(release, "/tmp/f.tar.gz")                  # True/False
    extract("/tmp/f.tar.gz", "/tmp/staging")            # True/False
"""

import hashlib
import json
import pathlib
import shutil
import tarfile
import urllib.request
import zipfile

API = "https://api.github.com/repos/{repo}/releases/latest"
HEADERS = {"User-Agent": "dotfiles-installer (github.com/brunodavi/.dotfiles-stow)"}

TAR_NAMES = ("tar.gz", "tgz", "tar.bz2", "tar.xz")


def api(repo, tag=None):
    """Info (dict) da release mais recente do repo — ou de uma tag fixa."""
    if tag is None:
        url = API.format(repo=repo)
    else:
        url = f"https://api.github.com/repos/{repo}/releases/tags/{tag}"
    request = urllib.request.Request(url, headers=HEADERS)
    with urllib.request.urlopen(request) as response:
        return json.load(response)


def asset_url(release, name):
    """URL de download do asset `name` (nome exato) — None se não houver."""
    for asset in release.get("assets", []):
        if asset["name"] == name:
            return asset["browser_download_url"]
    return None


def download(url, dest):
    """Baixa `url` para `dest` (path aceita str/Path)."""

    dest = pathlib.Path(dest)
    request = urllib.request.Request(url, headers=HEADERS)
    with urllib.request.urlopen(request) as response:
        with open(dest, "wb") as arquivo:
            shutil.copyfileobj(response, arquivo)
    print(f"[github] download ok: {dest.name}")


def checksum(release, file):
    """Confere `file` contra o SHA256SUMS da release (se existir).

    Sem SHA256SUMS na release, assume válido (avisa). Retorna False
    quando o hash NÃO bate — quem chama decide abortar.
    """
    file = pathlib.Path(file)
    sums_url = asset_url(release, "SHA256SUMS")
    if sums_url is None:
        print(f"[github] sem SHA256SUMS na release; pulando conferência")
        return True

    request = urllib.request.Request(sums_url, headers=HEADERS)
    with urllib.request.urlopen(request) as response:
        somas = response.read().decode()

    esperado = None
    for linha in somas.splitlines():
        partes = linha.split()
        if len(partes) >= 2 and partes[-1] == file.name:
            esperado = partes[0]
            break
    if esperado is None:
        print(f"[github] {file.name} não listado no SHA256SUMS; pulando")
        return True

    atual = hashlib.sha256(file.read_bytes()).hexdigest()
    if atual != esperado:
        print(f"[github] sha256 DIFERENTE: {file.name}")
        print(f"[github] esperado: {esperado}")
        print(f"[github] obtido:   {atual}")
        return False
    print(f"[github] sha256 ok: {file.name}")
    return True


def extract(file, dest):
    """Extrai `file` (tar.gz/tgz/tar.bz2/tar.xz/zip) dentro de `dest`."""
    file = pathlib.Path(file)
    dest = pathlib.Path(dest)
    if file.name.endswith(TAR_NAMES):
        with tarfile.open(file) as arquivo:
            try:
                arquivo.extractall(dest, filter="data")  # caminhos seguros
            except TypeError:  # python < 3.12
                arquivo.extractall(dest)
    elif file.name.endswith(".zip"):
        with zipfile.ZipFile(file) as arquivo:
            arquivo.extractall(dest)
    else:
        print(f"[github] formato desconhecido p/ extrair: {file.name}")
        return False
    print(f"[github] extraído em {dest}")
    return True
