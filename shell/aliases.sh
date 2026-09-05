# cmd_exists_then_alias()
cxta() {
  command -v "$1" > /dev/null && alias "$2"="$3"
}

alias restart="exec bash"

alias bashrc="${EDITOR} ~/.bashrc"
alias envrc="${EDITOR} ~/.envrc"

alias dotinit="${EDITOR} ${DOTSHELL}/init.sh"
alias funcs="${EDITOR} ${DOTSHELL}/funcs.sh"
alias aliases="${EDITOR} ${DOTSHELL}/aliases.sh"


alias nv="nvim"
alias rf='rm -rf'


alias la='ls -a'
alias l1='ls -1'

alias ll='la -l --no-user'
alias l='ll --no-time --no-filesize'


cxta eza ls 'eza \
	-F always \
	--icons \
	--group-directories-first \
	--sort Extension'

cxta alias cdb 'cd-bookmark'
