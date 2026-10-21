alias c='command -v'

export EDITOR=$(c nvim || c vi || c nano)

unalias c

export PATH="$PATH:${HOME}/.dotfiles/scripts"

export PATH="${PATH}:${HOME}/.local/bin"
export PATH="/opt/nvim-linux-x86_64/bin:/opt/nvim-linux-arm64/bin:$PATH"

source ~/.envrc
