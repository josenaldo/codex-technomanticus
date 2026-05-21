---
title: "ZLE"
created: 2026-05-19
updated: 2026-05-21
type: concept
status: seedling
publish: true
fase: adepto
tags:
  - terminal
  - shell
  - zsh
  - adepto
  - zle
  - widgets
aliases:
  - ZLE
  - Zsh Line Editor
---

# ZLE

## TL;DR

ZLE (Zsh Line Editor) é o editor de linha do Zsh — o motor que interpreta cada tecla, mantém um buffer e dispatcha widgets (ações). Tudo que `bindkey` mapeia, ZLE executa. Escrever widget próprio é como criar um comando do editor sob medida.

---

## O que é / Como funciona

### Modelo de funcionamento

ZLE entra em ação toda vez que o Zsh aguarda input interativo. O fluxo é:

```
Input (tecla) → keymap atual lookup → widget associado → widget altera buffer → display atualiza
```

O **buffer** é o texto que você está editando antes do Enter. É uma string mutável que vive na memória do processo ZLE; ao pressionar Enter, o buffer vira o comando executado e é descartado.

### Keymaps disponíveis

| Keymap | Quando ativo |
|---|---|
| `emacs` | Default (`bindkey -e`) |
| `viins` | VI insert mode (`bindkey -v`) |
| `vicmd` | VI command/normal mode |
| `viopp` | VI operator pending |
| `visual` | VI visual (seleção ativa) |
| `isearch` | Busca incremental ativa |
| `command` | Leitura de nome de comando (`:` no vi) |
| `.safe` | Fallback imutável — nunca pode ser alterado |

`main` é sempre um alias para o keymap default ativo (emacs ou viins). Mudar de emacs para vi com `bindkey -v` faz `main` apontar para `viins`.

### Categorias de widgets builtin

**Inserção e execução:**
- `self-insert` — insere o caractere da tecla pressionada no buffer
- `accept-line` — executa o buffer (Enter)
- `accept-and-hold` — executa e re-insere o buffer para nova edição
- `quoted-insert` — insere o próximo caractere literalmente (sem interpretar como binding)

**Movimentação:**
- `beginning-of-line` / `end-of-line`
- `forward-char` / `backward-char`
- `forward-word` / `backward-word`
- `vi-beginning-of-line` / `vi-end-of-line`

**Edição:**
- `delete-char` / `backward-delete-char`
- `kill-word` / `backward-kill-word`
- `kill-line` — mata do cursor até o fim
- `yank` — cola o último texto matado
- `transpose-chars` — troca o char anterior com o atual
- `undo` / `redo`

**History:**
- `up-line-or-history` / `down-line-or-history`
- `history-incremental-search-backward` (`Ctrl-R` em emacs)
- `history-search-backward` / `history-search-forward`
- `insert-last-word` (Alt-. em emacs)

**Controle de buffer e tela:**
- `clear-screen` — limpa a tela
- `push-line` — empurra o buffer pra uma pilha interna (limpa a linha) e restaura depois do próximo Enter
- `get-line` — restaura o buffer da pilha
- `redisplay` — redesenha a linha atual sem executar
- `reset-prompt` — redesenha o prompt inteiro (incluindo o PS1)

**Completion:**
- `expand-or-complete` — expande glob ou dispara completion (Tab)
- `complete-word` — completa a palavra atual
- `menu-complete` / `reverse-menu-complete` — navega entre opções de completion
- `list-choices` — lista opções sem inserir
- `delete-char-or-list` — deleta char ou lista choices se buffer vazio

---

### Variáveis especiais (acessíveis em widget custom)

| Variável | Descrição |
|---|---|
| `BUFFER` | Todo o texto do buffer (leitura/escrita) |
| `LBUFFER` | Texto à esquerda do cursor (leitura/escrita) |
| `RBUFFER` | Texto à direita do cursor (leitura/escrita) |
| `CURSOR` | Posição do cursor (0-indexed, 0 = antes do 1º char) |
| `KEYS` | Sequência de tecla que disparou o widget (read-only) |
| `WIDGET` | Nome do widget em execução (read-only) |
| `KEYMAP` | Keymap ativo no momento da invocação |
| `NUMERIC` | Argumento numérico (ex: `5w`) — unset se não fornecido |
| `MARK` | Posição da marca de seleção de região |
| `CUTBUFFER` | Último texto morto (kill) |
| `killring` | Array com histórico de kills anteriores |

Alterar `LBUFFER` ou `RBUFFER` automaticamente atualiza `CURSOR` e `BUFFER` de forma consistente — é mais seguro do que calcular índices manualmente em `BUFFER`.

---

### Criar widget custom

O processo tem três etapas obrigatórias e sempre nessa ordem:

**1. Definir a função Zsh:**
```zsh
my-widget() {
  # lógica aqui — acessa BUFFER, CURSOR, etc.
}
```

**2. Registrar como widget no ZLE:**
```zsh
zle -N my-widget
# Se o nome da função diferir do widget:
# zle -N widget-name function-name
```

**3. Bindar a uma sequência de tecla:**
```zsh
bindkey '<seq>' my-widget
```

Sem o passo 2, `bindkey` aceita o comando sem erro mas a tecla não faz nada — a função não é reconhecida como widget.

---

### Hooks ZLE (widgets especiais disparados em eventos)

Hooks são widgets comuns registrados com nomes reservados que ZLE invoca automaticamente em eventos internos.

| Hook | Quando dispara |
|---|---|
| `zle-line-init` | Início de nova linha (antes do primeiro input) |
| `zle-line-finish` | Após Enter, antes da execução do comando |
| `zle-keymap-select` | Ao trocar de keymap (ex: viins → vicmd) |
| `zle-line-pre-redraw` | Antes de cada refresh de tela |
| `zle-isearch-update` | A cada atualização durante busca incremental |
| `zle-isearch-exit` | Ao sair da busca incremental |
| `zle-history-line-set` | Ao mudar para outra linha do history |

Para usar um hook, defina a função e registre com o nome exato:

```zsh
function my-line-init {
  # código
}
zle -N zle-line-init my-line-init
```

---

## Na prática

### Widget 1: expand-or-complete-with-dots

Mostra `...` vermelho no terminal enquanto o Zsh processa a completion — útil quando completions são lentas (rede, NFS, etc.).

```zsh
expand-or-complete-with-dots() {
  echo -n "\e[31m...\e[0m"      # imprime "..." em vermelho
  zle expand-or-complete         # dispara completion normal
  zle redisplay                  # redesenha (remove os "...")
}
zle -N expand-or-complete-with-dots
bindkey '^I' expand-or-complete-with-dots   # Tab
```

---

### Widget 2: insert-sudo

Toggle de `sudo` no início do buffer. Pressionar a sequência com `sudo` presente remove; sem `sudo`, adiciona e avança o cursor.

```zsh
insert-sudo() {
  if [[ $BUFFER == sudo\ * ]]; then
    BUFFER="${BUFFER#sudo }"
  else
    BUFFER="sudo $BUFFER"
    CURSOR=$((CURSOR + 5))
  fi
}
zle -N insert-sudo
bindkey '\e\e' insert-sudo   # Esc Esc
```

Note que `CURSOR + 5` compensa os 5 caracteres de `"sudo "` adicionados no início.

---

### Widget 3: clear-and-history

Limpa a tela e imprime os últimos 10 comandos do history antes de restaurar o prompt.

```zsh
clear-and-history() {
  clear
  print -l ${(@)history[1,10]}
  zle reset-prompt
}
zle -N clear-and-history
bindkey '^X^H' clear-and-history   # Ctrl-X Ctrl-H
```

`zle reset-prompt` redesenha o prompt após a saída do `print`, evitando que o prompt suma.

---

### Hook: indicador de modo vi no prompt

Atualiza um segmento do `PROMPT` em tempo real ao mudar entre insert e normal mode no vi.

```zsh
function zle-keymap-select {
  case $KEYMAP in
    vicmd)      VI_MODE="[N]" ;;
    main|viins) VI_MODE="[I]" ;;
  esac
  zle reset-prompt
}
zle -N zle-keymap-select

# No PROMPT, referenciar $VI_MODE com PROMPT_SUBST ativo:
setopt PROMPT_SUBST
PROMPT='${VI_MODE} %~ %# '
```

`PROMPT_SUBST` é necessário para que `${VI_MODE}` seja expandido dinamicamente a cada redesenho, em vez de ser gravado como string literal no momento da atribuição.

---

### Invocar widget a partir de outro widget

Um widget pode chamar outro com `zle <widget-name>`:

```zsh
my-composite-widget() {
  zle beginning-of-line      # move cursor para o início
  BUFFER="echo $BUFFER"      # wraps com echo
  zle end-of-line            # move cursor para o fim
}
zle -N my-composite-widget
bindkey '^X^E' my-composite-widget
```

---

### Listagem e debug

```zsh
# Listar todos os widgets registrados (builtin + custom)
zle -la

# Listar apenas widgets custom (user-defined)
zle -la | grep -v '^[.]'

# Ver o que está bindado a uma tecla específica
bindkey '^I'         # o que está no Tab

# Listar todos os bindings do keymap atual
bindkey

# Listar bindings de keymap específico
bindkey -M vicmd
```

---

## Armadilhas

### 1. Esqueceu `zle -N` antes de `bindkey`

**Causa:** `bindkey` registra a string como widget sem verificar se existe uma função associada. O ZLE só descobre o problema na hora de executar.

**Sintoma:** A tecla não faz nada. Sem mensagem de erro no terminal.

**Como detectar:** Execute `bindkey '<seq>'` para confirmar que o binding existe; depois `zle -la | grep my-widget` para ver se o widget foi registrado. Se o binding existe mas o widget não aparece na lista, faltou o `zle -N`.

**Solução:** Sempre na ordem: função → `zle -N` → `bindkey`. Coloque os três no `.zshrc` em sequência para não perder nenhum.

---

### 2. `zle reset-prompt` fora de contexto adequado causa redraws infinitos ou noop

**Causa:** `reset-prompt` só tem efeito dentro de um contexto ZLE ativo. Chamado em `zle-line-pre-redraw`, pode disparar um loop de redesenho se o hook alterar estado visual a cada chamada.

**Sintoma:** Terminal trava em loop de flicker ou o prompt some e aparece duplicado.

**Como detectar:** Adicione `echo "redraw triggered" >> /tmp/zle-debug.log` no início do hook e observe quantas vezes dispara por keypress. Mais de 1 por Enter indica loop.

**Solução:** Use `reset-prompt` apenas em hooks de evento discreto (`zle-keymap-select`, `zle-line-init`) ou em widgets explicitamente invocados pelo usuário. Evite em `zle-line-pre-redraw` a menos que a lógica tenha guarda de idempotência.

---

### 3. Alterar `BUFFER` diretamente em widget de inserção quebra completion

**Causa:** O sistema de completion (`compsys`) assume que `BUFFER` está estável durante o ciclo de completion. Modificar `BUFFER` de dentro de `self-insert` ou de um wrapper de Tab interrompe o estado interno do completion.

**Sintoma:** Completion produz resultados errados, duplica texto, ou trava o cursor em posição inesperada.

**Como detectar:** Teste o widget em isolamento (bind temporário a outra tecla que não Tab) e observe se o completion subsequente ainda funciona normalmente.

**Solução:** Modificações de `BUFFER` devem ocorrer em widgets explícitos e independentes, nunca dentro de wrappers que envolvem `expand-or-complete` ou `_complete` — a menos que a modificação ocorra *antes* de delegar ao widget de completion, como no widget `expand-or-complete-with-dots` da seção anterior.

---

### 4. Confundir sintaxe de `bindkey` (Zsh) com `vim.keymap.set` (Neovim)

**Causa:** Quem trabalha com Neovim e Zsh simultaneamente tende a misturar as sintaxes mentalmente.

**Sintoma:** Erros `bindkey: too many arguments` (passou table/array), ou binding silenciosamente ignorado (usou sintaxe Lua no `.zshrc`).

**Como detectar:** Revisar se a chamada usa a sintaxe correta de cada contexto antes de debugar mais fundo.

**Solução:**

| Contexto | Sintaxe correta |
|---|---|
| Zsh (ZLE) | `bindkey '<seq>' widget-name` |
| Zsh (keymap específico) | `bindkey -M vicmd '<seq>' widget-name` |
| Neovim (Lua) | `vim.keymap.set('n', '<seq>', rhs, opts)` |
| Neovim (modo múltiplo) | `vim.keymap.set({'n','v'}, '<seq>', rhs, opts)` |

Em Zsh, modos são keymaps nomeados selecionados com `-M`. Em Neovim, modos são strings ou arrays no primeiro argumento de `vim.keymap.set`.

---

## Em inglês

- **widget** — *widget*. "A named action registered in ZLE that can be bound to a key."
- **buffer** — *buffer*. "The in-memory string holding the command line being edited."
- **posição do cursor** — *cursor position*. "Zero-indexed offset into BUFFER indicating where the next character will be inserted."
- **editor de linha** — *line editor*. "The component responsible for reading and editing a command before execution."
- **dispatchar** — *dispatch*. "To look up and invoke the widget associated with a key sequence."
- **gancho** — *hook*. "A special widget automatically invoked by ZLE on internal events."
- **evento** — *event*. "A state change within ZLE that triggers a hook, such as keymap switching."
- **re-renderizar** — *redisplay*. "To refresh the terminal's display of the current buffer without executing it."
- **redefinir prompt** — *reset prompt*. "To force ZLE to re-evaluate and redraw the prompt string."
- **sequência de escape** — *escape sequence*. "A byte sequence (e.g. `\e[31m`) interpreted by the terminal to set color, move cursor, etc."

---

## Veja também

- [[06 - Keybindings práticos]] — onde widgets viram bindings e o setup completo de keymaps
- [[08 - Completion system (compsys)]] — completion é uma categoria de widget ZLE
- [[03-Dominios/Terminal/Shell/index|MOC do galho]]
- [[03-Dominios/Terminal/index|Trilha Terminal]]
- [[Dicionário do Terminal#ZLE|ZLE]], [[Dicionário do Terminal#Widget|widget]]

---

## Referências

- Zsh manual — Zsh Line Editor — https://zsh.sourceforge.io/Doc/Release/Zsh-Line-Editor.html
- Zsh manual — Widgets — https://zsh.sourceforge.io/Doc/Release/Zsh-Line-Editor.html#Widgets
