#!/usr/bin/env bash
set -e

FORCE=0

for arg in "$@"; do
  case "$arg" in
  -f | --force)
    FORCE=1
    ;;
  esac
done

CONFIGS=(
  LazyVim
)

for cfg in "${CONFIGS[@]}"; do
  echo "Aplicando stow para: $cfg"

  if [ "$FORCE" -eq 1 ]; then
    # Se forçado, removemos os links antigos do pacote 'nvim' para liberar o caminho
    echo "Removendo links antigos do pacote 'nvim' (se existirem)..."
    stow -D nvim 2>/dev/null || true

    # Aplica o stow adotando eventuais arquivos órfãos
    stow -R --adopt "$cfg"
    echo "Configuração do Neovim via $cfg aplicada com sucesso!"
  else
    if ! stow -R "$cfg" 2>/dev/null; then
      echo ""
      echo "Erro: Conflito detectado. Os arquivos já estão linkados por outro pacote (provavelmente 'nvim')."
      echo "Para forçar a substituição e migrar para o lazy.nvim, execute:"
      echo "  ./lazy.nvim/install.sh --force"
      exit 1
    fi
  fi
done
