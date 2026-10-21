"""Helper universal de instalação de pacotes para os hooks dos dotfiles.

Detecta o gerenciador de pacotes do sistema, escolhe o nome certo do
pacote para ele e roda o comando de install — com dry_run pra simulação.
Se o install falha (ex.: "pacote não encontrado"), pesquisa o termo no
gerenciador e pergunta ao usuário qual candidato instalar.

Uso:
    install("ripgrep", dry_run=False)                  # mesmo nome em todos
    install("ripgrep", {"dnf": "ripgrep"}, dry_run=dry)  # nome custom por PM
"""

import os
import shutil
import subprocess
import sys

# ordem de detecção = preferência
PKG_MANAGERS = [
    "pkg",       # Termux (envelope do apt, sem sudo)
    "apt",       # Debian/Ubuntu
    "apt-get",
    "dnf",       # Fedora
    "yum",
    "pacman",    # Arch
    "apk",       # Alpine
    "zypper",    # openSUSE
    "brew",      # macOS / Linuxbrew
]

# comando base de install por gerenciador
INSTALL_CMD = {
    "pkg": ["pkg", "install", "-y"],
    "apt": ["apt", "install", "-y"],
    "apt-get": ["apt-get", "install", "-y"],
    "dnf": ["dnf", "install", "-y"],
    "yum": ["yum", "install", "-y"],
    "pacman": ["pacman", "-S", "--noconfirm"],
    "zypper": ["zypper", "--non-interactive", "install"],
    "apk": ["apk", "add"],
    "brew": ["brew", "install"],
}

# comando de pesquisa por gerenciador
SEARCH_CMD = {
    "pkg": ["pkg", "search"],
    "apt": ["apt-cache", "search"],
    "apt-get": ["apt-cache", "search"],
    "dnf": ["dnf", "search"],
    "yum": ["yum", "search"],
    "pacman": ["pacman", "-Ss"],
    "apk": ["apk", "search", "-v"],
    "zypper": ["zypper", "search"],
    "brew": ["brew", "search"],
}

# gerenciadores que exigem root (e aceitam sudo)
NEED_ROOT = {"apt", "apt-get", "dnf", "yum", "pacman", "zypper", "apk"}


def _pick_manager(managers):
    """Primeiro gerenciador disponível na máquina."""
    for name in PKG_MANAGERS:
        if shutil.which(name):
            return name
    if managers:  # segue a ordem do dict caso tenha gerenciador fora da lista
        for name in managers:
            if shutil.which(name):
                return name
    return None


def _sudo_prefix(manager):
    if manager not in NEED_ROOT:
        return []
    if os.geteuid() == 0:
        return []
    if shutil.which("sudo"):
        return ["sudo"]
    return []


def _system_context():
    """Descrição curta do sistema (distros + termux) p/ mensagens de erro."""
    ids = []
    try:
        with open("/etc/os-release") as release:
            for line in release:
                key, _, value = line.partition("=")
                if key in ("ID", "ID_LIKE"):
                    ids.append(value.strip().strip('"'))
    except OSError:
        pass
    if "com.termux" in os.environ.get("PREFIX", ""):
        ids.append("termux")
    ids = list(dict.fromkeys(ids))  # dedup mantendo ordem
    return " + ".join(ids) if ids else os.uname().sysname


def _search_packages(manager, term):
    """Pesquisa `term` no gerenciador. Retorna [(nome, descrição), ...]."""
    search_cmd = _sudo_prefix(manager) + SEARCH_CMD[manager] + [term]
    result = subprocess.run(
        search_cmd, capture_output=True, text=True, timeout=90
    )
    pairs = []
    prev_repo_name = None
    lines = (result.stdout or "").splitlines()
    for line in lines:
        line = line.rstrip()
        if not line or line.startswith(("==>", "#", "\x1b") ):
            continue

        # pacman -Ss: "repo/nome" + descrição na linha seguinte indentada
        if "/" in line and line.split("/")[0] and " " not in line.split("/")[0]:
            prev_repo_name = line.split("/")[1].strip()
            continue
        if prev_repo_name and line.startswith("    "):
            pairs.append((prev_repo_name, line.strip()))
            prev_repo_name = None
            continue

        # apt-cache/pkg: "nome - descrição"
        if " - " in line:
            name, _, desc = line.partition(" - ")
            pairs.append((name.strip(), desc.strip()))
            continue

        # zypper: "nome | versão | arch | repo | resumo"
        if "|" in line:
            cells = [c.strip() for c in line.split("|")]
            if len(cells) >= 5 and cells[0] not in ("S", "Name"):
                pairs.append((cells[0], cells[4]))
            continue

        # dnf: "nome : descrição"
        name, sep, desc = line.partition(" : ")
        if sep:
            pairs.append((name.strip(), desc.strip()))
            continue

        # fallback: apk/brew e formatos soltos — primeira palavra é o nome
        tokens = line.split()
        if tokens:
            name = tokens[0].split("-")[0] if manager == "apk" else tokens[0]
            pairs.append((name, line.strip()))
    # dedup por nome mantendo a ordem
    seen, out = set(), []
    for name, desc in pairs:
        if name and name not in seen:
            seen.add(name)
            out.append((name, desc))
    return out


def _ask_candidate(manager, term, candidates):
    """Pergunta ao usuário qual candidato instalar. None = cancelar."""
    print(f"\n[packages] sistema: {_system_context()} | gerenciador: {manager}")
    print(f"[packages] pacote '{term}' não encontrado; candidatos para esse termo:\n")
    for index, (name, desc) in enumerate(candidates[:15], start=1):
        print(f"  {index:2}. {name:30} {desc[:60]}")
    print()
    if not sys.stdin.isatty():
        print("[packages] modo não-interativo: nada instalado")
        return None
    answer = input(
        "[packages] número do pacote para instalar (vazio = cancelar): "
    ).strip()
    if not answer.isdigit() or not (1 <= int(answer) <= min(len(candidates), 15)):
        print("[packages] cancelado")
        return None
    return candidates[int(answer) - 1][0]


def install(pkg, managers=None, check=None, dry_run=False):
    """Instala `pkg` no gerenciador disponível.

    Args:
        pkg: nome do pacote (str) ou lista de nomes.
        managers: dict opcional {nome_do_PM: nome_do_pacote} — pacotes com
            nome diferente por gerenciador usam o valor do dict; PMs ausentes
            no dict caem no nome padrão de `pkg`.
        check: binário a testar antes de instalar (idempotência). Se já
            existir no PATH, não instala. Ex: check="rg" para o pkg ripgrep.
        dry_run: só imprime os comandos que ser rodados.

    Returns:
        True se instalou (ou rodou), False se pulou/falhou/cancelou.
    """
    names = [pkg] if isinstance(pkg, str) else list(pkg)
    manager = _pick_manager(managers or {})
    if manager is None:
        print(f"[packages] nenhum gerenciador conhecido; pulando {names}")
        return False

    if check and shutil.which(check):
        print(f"[packages] {check} já instalado, pulando")
        return False

    # nome deste pacote para este gerenciador (fallback: mesmo nome)
    pkg_name = names[0]
    if managers:
        pkg_name = managers.get(manager, pkg_name)

    def _run(name):
        cmd = _sudo_prefix(manager) + INSTALL_CMD[manager] + [name]
        if dry_run:
            print(f"[packages] (dry-run) {' '.join(cmd)}")
            return True
        print(f"[packages] $ {' '.join(cmd)}")
        result = subprocess.run(cmd)
        return result.returncode == 0

    # apt/apt-get com cache velho falha com "unable to locate package":
    # atualizar o índice antes evita falso negativo de pacote existente
    if manager in ("apt", "apt-get") and not dry_run:
        update = _sudo_prefix(manager) + [manager, "update"]
        print(f"[packages] $ {' '.join(update)}")
        subprocess.run(update)

    ok = _run(pkg_name)
    if ok or dry_run:
        print(f"[packages] install {'ok' if ok else 'dry-run'}: {pkg_name} via {manager}")
        return ok

    # fallback: pesquisa o termo e pergunta ao usuário
    candidates = _search_packages(manager, names[0])
    if not candidates:
        print(f"[packages] nada encontrado para '{names[0]}' ({_system_context()})")
        return False
    chosen = _ask_candidate(manager, names[0], candidates)
    if chosen is None:
        return False
    return _run(chosen)
