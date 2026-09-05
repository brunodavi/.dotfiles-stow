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
)

has_cmd() {
  command -v "$1" &>/dev/null
}

check_all() {
    local all_ok=0
    for app in "${APPS[@]}"; do
        has_cmd "${app}" || all_ok=1
    done

    return all_ok
}

if [ ! check_all ]; then 
    if has_cmd apk; then
      apk add --no-cache "${APPS[@]}"
    elif has_cmd pkg; then
      pkg install -y "${APPS[@]}"
    elif has_cmd apt-get; then
      sudo apt-get install -y "${APPS[@]}"
    fi
else
    echo 'All installed'
fi


mkdir -p ~/.config

for cfg in "${CONFIGS[@]}"; do
  echo "Link: $cfg"
  stow -R "$cfg"
done

DOTFILES_INIT='~/.dotfiles/shell/init.sh'

CONTAIN_INIT=0
grep -qw "${DOTFILES_INIT}" ~/.bashrc || CONTAIN_INIT=1

if [ ${CONTAIN_INIT} = 1 ]; then
    echo "Add init.sh on .bashrc"
    echo -e "\nsource ${DOTFILES_INIT}" >> ~/.bashrc
else
    echo "Always init.sh on .bashrc"
fi
