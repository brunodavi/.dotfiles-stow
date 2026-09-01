#!/usr/bin/env bash
set -e

APPS=(
  stow
  neovim
  python3
  eza
)

CONFIGS=(
  git
  nvim
  bash
)

has_cmd() {
  command -v "$1" &>/dev/null
}

if has_cmd apk; then
  apk add --no-cache "${APPS[@]}"
elif has_cmd pkg; then
  pkg install -y "${APPS[@]}"
elif has_cmd apt-get; then
  sudo apt-get install -y "${APPS[@]}"
fi

mkdir -p ~/.config

for cfg in "${CONFIGS[@]}"; do
  echo "Link: $cfg"
  stow -R "$cfg"
done
