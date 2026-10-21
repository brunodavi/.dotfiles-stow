TMUX NA PRÁTICA — tutorial (dotfiles)
prefixo = Ctrl+a em tudo abaixo

════════════════════════════════════════════════
 1. A IDEIA EM 3 CONCEITOS
════════════════════════════════════════════════

Pense num computador dentro do seu terminal:

  SESSÃO  = uma "mesa de trabalho" com nome
  JANELA  = uma "aba" dentro da sessão (ocupa a tela)
  PAINEL  = um pedaço da janela (tela dividida em 2, 3...)

Um desenho do seu tmux:

  sessão main ──┬─ janela 1: bash
                └─ janela 2: nvim ─┬─ painel: editor
                                   └─ painel: terminal de testes

  sessão teste ── janela 1: bash

Vantagem pra você: NUNCA precisa sair do proot alpine
pra testar outra coisa. Cria outra sessão e pronto.

════════════════════════════════════════════════
 2. O CICLO DIÁRIO
════════════════════════════════════════════════

PASSO 1 — entrar (do proot alpine, no shell):

    ta teste           cria a sessão "teste" e entra nela
    ta main            cria/entra numa outra

  (o ta é inteligente: usa ele dentro ou fora do tmux)

PASSO 2 — trocar entre sessões (sem sair do tmux):

    Ctrl+a depois s    abre a lista de sessões
                       setas ou hjkl pra mover... Enter pra ir

    Ctrl+a depois C-f  digita o nome da sessão, Enter
    Ctrl+a depois BTab volta pra última sessão usada

PASSO 3 — sair de vista (deixa TUDO rodando):

    Ctrl+a depois d    sai (detach)

  a sessão continua viva em background, o neovim
  que você deixou aberto continua lá, etc.

PASSO 4 — voltar:

    ta                 volta (e cria "main" se não tiver nada)

════════════════════════════════════════════════
 3. FECHAR UMA SESSÃO SEM SAIR DO TMUX
════════════════════════════════════════════════

    Ctrl+a depois K    encerra a sessão atual

  aparece: "encerrar a sessão 'teste'? (y/n)"
  y = a sessão (e as janelas dela) morrem
  E VOCÊ FICA DENTRO DO TMUX: ele pula pra outra sessão.

  Só que: se essa era a ÚLTIMA sessão, o tmux inteiro
  fecha com ela (não tem mais o quê mostrar).
  Nessa caso, prefere Ctrl+a d e deixar ela viva por trás?

════════════════════════════════════════════════
 4. JANELAS E PAINÉIS NA PRÁTICA
════════════════════════════════════════════════

JANELAS (as "abas" da sessão atual):

    Ctrl+a depois c     nova janela
    Ctrl+a depois C-h   janela anterior
    Ctrl+a depois C-l   janela próxima
    Ctrl+a depois 2     pula pra janela 2

PAINÉIS (divide a janela atual ao meio):

    Ctrl+a depois |     dividir lado a lado
    Ctrl+a depois -     dividir cima/baixo
    Alt+h j k l         pular de painel em painel
    Ctrl+a depois z     zoom no painel (z de novo volta)
    Ctrl+a depois x     fechar o painel

Regra de bolso:
  · coisas que você olha JUNTAS      → painéis
    (nvim de um lado, teste do outro)
  · coisas separadas                 → janelas
  · coisas separadas mesmo           → sessões

════════════════════════════════════════════════
 5. COPIAR ALGO DO TERMINAL
════════════════════════════════════════════════

    1. Ctrl+a depois [    entra no modo de cópia
    2. hjkl/setas         navegar até o texto
    3. v                  start da seleção
    4. y                  copia (vai pro android!)
    5. Ctrl+a depois p    cola dentro do tmux

    ESC ou q               sair do modo de cópia

════════════════════════════════════════════════
 6. LER A STATUS BAR (barrinha no fim da tela)
════════════════════════════════════════════════

    ┌ teste │ 1:bash  2:nvim ────── 2 janelas · 1 anexada ┐
      └──────────────────────┘   └──────────────────────┘
       o que você está agora      sessões/janelas existentes

  · nome da sessão: na esquerda, com fundo verde
  · janelas: no meio (a ATUAL fica com fundo verde)
  · direita: contagem de janelas e sessões anexadas

════════════════════════════════════════════════
 7. DICAS DE ROTINA
════════════════════════════════════════════════

· Termux se fechou por engano? As sessões sobreviveram:
  abra o proot, dá um `ta` que você volta.
· Morte total (Termux exterminado pelo Android)? O
  tmux-resurrect consegue recriar o que estava aberto:
  `ta` (volta ao tmux) e Ctrl+a C-r restaura a última
  salva — o continuum salva sozinho a cada 15 min.
  Ctrl+a C-s salva na hora se quiser garantir.
· Esqueceu o atalho? Ctrl+a ? mostra o cheat sheet
  (e Ctrl+a / lista TODOS os atalhos do tmux).
· Truque bom: no meio do trabalho, Ctrl+a N cria uma
  sessão limpa pra "brincar" e BTab te devolve.
· Config mudou? Ctrl+a r recarrega.

════════════════════════════════════════════════
 8. GLOSSÁRIO
════════════════════════════════════════════════

attach      entrar/ver uma sessão (o ta faz isso)
detach      sair de vista; a sessão segue rodando (Ctrl+a d)
buffer      área de transferência interna do tmux
osc52       truque que manda cópia pro clipboard do android
server      o "dono" das sessões; vive no fundo, invisível
prefixo     o Ctrl+a que vem antes de cada atalho
