---
title: "Keybindings práticos"
created: 2026-05-19
updated: 2026-05-19
type: concept
progress: backlog
status: seedling
publish: true
fase: adepto
tags:
  - terminal
  - shell
  - zsh
  - adepto
  - keybindings
  - zle
aliases:
  - Keybindings práticos
  - Bindkey
---

# Keybindings práticos

## TL;DR

`bindkey` mapeia sequências de tecla a widgets do ZLE. Modo emacs (default) ou vi. Setup comum: fix de Home/End/Ctrl-Arrows pra funcionar no seu terminal. Combine com plugins (history-substring-search, edit-command-line) pra ganhos imediatos.

---

## O que é

`bindkey` é o builtin do Zsh que gerencia as associações entre sequências de tecla e widgets do ZLE (Zsh Line Editor). Sem configuração explícita, o Zsh usa os bindings do modo emacs — um conjunto razoável, mas que não cobre teclas que dependem do terminal (Home, End, Ctrl-Arrows). A maioria dos problemas de "Home não funciona" ou "Ctrl-Right não pula palavra" se resolve com três linhas de `bindkey` no `.zshrc`.

---

## Como funciona

### O par bindkey ↔ widget

Cada tecla (ou sequência de escape) está associada a um **widget** — uma função registrada no ZLE que executa uma ação de edição. A relação é:

```
sequência de escape → widget → ação
```

Exemplo: `^[[H` (sequência que o terminal manda ao pressionar Home) → widget `beginning-of-line` → cursor vai pro início da linha.

### Comandos essenciais

```zsh
bindkey                         # lista TODOS os bindings do keymap ativo
bindkey '<seq>'                 # mostra qual widget está bound à sequência
bindkey '<seq>' <widget>        # define um binding
bindkey -r '<seq>'              # remove um binding
bindkey -l                      # lista os keymaps disponíveis
bindkey -M <keymap> '<seq>' <widget>   # binda em keymap específico
bindkey -e                      # ativa modo emacs (default)
bindkey -v                      # ativa modo vi
```

### Modo emacs vs vi

O Zsh determina o modo inicial pelo valor de `$VISUAL` ou `$EDITOR`: se contiverem `vi` ou `vim`, ativa vi-mode; caso contrário, usa emacs-mode.

**Modo emacs** (`bindkey -e`) — default pra maioria dos setups:

| Tecla | Widget | Ação |
|-------|--------|------|
| `Ctrl-A` | `beginning-of-line` | início da linha |
| `Ctrl-E` | `end-of-line` | fim da linha |
| `Ctrl-K` | `kill-line` | apaga até o fim |
| `Ctrl-W` | `backward-kill-word` | apaga palavra anterior |
| `Ctrl-Y` | `yank` | cola o que foi apagado |
| `Ctrl-R` | `history-incremental-search-backward` | busca no history |
| `Tab` | `expand-or-complete` | completion |
| `Ctrl-U` | `kill-whole-line` | apaga linha inteira |
| `Ctrl-L` | `clear-screen` | limpa tela |

**Modo vi** (`bindkey -v`) — dois submodos:

- **viins** (insert): modo padrão ao entrar no shell. Digitação normal; `Esc` troca pra modo normal.
- **vicmd** (normal): comandos vim — `h`/`l` mover, `0`/`$` início/fim, `dd` apaga linha, etc.

### Keymaps disponíveis

`bindkey -l` lista os keymaps. Os relevantes:

| Keymap | Quando ativo |
|--------|-------------|
| `main` | alias do keymap default (`emacs` ou `viins`) |
| `emacs` | modo emacs |
| `viins` | modo insert do vi |
| `vicmd` | modo normal do vi |
| `command` | leitura de nome de comando após `:` em vi |
| `isearch` | durante busca incremental (`Ctrl-R`) |
| `.safe` | fallback imutável (não alterar) |

### Descobrir o código de uma tecla

O terminal manda sequências de escape ao pressionar teclas especiais — e elas variam por emulador de terminal. Para descobrir:

**Método 1 — `cat -v`:**
```bash
cat -v
# pressione a tecla e veja a sequência impressa
# Ctrl-C pra sair
```

**Método 2 — `Ctrl-V` no Zsh:**
```zsh
# no prompt do Zsh, pressione Ctrl-V e depois a tecla
# a sequência literal é inserida na linha (ex: ^[[1;5C)
```

**Método 3 — `zkbd`:**
```zsh
autoload -Uz zkbd
zkbd
# wizard interativo que descobre as sequências do terminal atual
```

---

## Na prática

### Fix de Home/End

```zsh
bindkey '^[[H' beginning-of-line   # Home
bindkey '^[[F' end-of-line         # End
```

> Sequências `^[[H`/`^[[F` são as mais comuns (GNOME Terminal, Alacritty, Kitty). Se não funcionar, descubra a sequência certa com `cat -v`.

### Ctrl-Arrows — mover por palavra

```zsh
bindkey '^[[1;5C' forward-word     # Ctrl-Right
bindkey '^[[1;5D' backward-word    # Ctrl-Left
```

### Ctrl-Delete / Ctrl-Backspace

```zsh
bindkey '^[[3;5~' kill-word         # Ctrl-Delete
bindkey '^H' backward-kill-word     # Ctrl-Backspace
```

### History substring search (plugin)

Com o plugin `zsh-history-substring-search` ativo:

```zsh
bindkey '^[[A' history-substring-search-up      # Up
bindkey '^[[B' history-substring-search-down    # Down
```

> Importante: o plugin deve ser carregado **depois** de `zsh-syntax-highlighting`, e os bindings de Up/Down devem vir **depois** do plugin ser sourced — caso contrário, os widgets `history-substring-search-up`/`history-substring-search-down` não existem ainda.

### Sudo-toggle (plugin sudo do OMZ)

Após adicionar `sudo` ao array `plugins=(...)`:

```zsh
# Esc-Esc adiciona `sudo` no início do comando atual
bindkey '\e\e' sudo-command-line
```

> O plugin sudo já configura `Esc-Esc` por default no OMZ — esse binding explícito é útil se você usa configuração manual sem OMZ.

### Editar comando longo no `$EDITOR`

```zsh
autoload -U edit-command-line
zle -N edit-command-line
bindkey '^X^E' edit-command-line    # Ctrl-X Ctrl-E
```

Ao pressionar `Ctrl-X Ctrl-E`, o conteúdo da linha atual abre no editor configurado em `$EDITOR`. Ao salvar e sair, o comando editado é submetido.

### Forward search (Ctrl-S)

Por default, `Ctrl-S` é capturado pelo terminal como "stop output" (XON/XOFF). Pra liberar o atalho de busca forward no ZLE:

```zsh
stty -ixon   # desativa XON/XOFF do terminal
bindkey '^S' history-incremental-search-forward
```

### Trocar para vi-mode

```zsh
bindkey -v
```

Com vi-mode, bindings do modo emacs deixam de funcionar no `viins` — é preciso reconfigurá-los explicitamente em `viins` se quiser mantê-los:

```zsh
bindkey -v
bindkey -M viins '^A' beginning-of-line
bindkey -M viins '^E' end-of-line
bindkey -M viins '^R' history-incremental-search-backward
```

### Criando widget custom

```zsh
# Função que executa `ls` ao pressionar Alt-L
_ls-on-demand() {
  zle -I
  ls
}
zle -N _ls-on-demand
bindkey '^[l' _ls-on-demand    # Alt-L
```

Passos: (1) definir função shell, (2) registrar com `zle -N`, (3) bindar com `bindkey`.

---

## Armadilhas

### 1. Bindings feitos antes do OMZ carregar são sobrescritos

**Causa:** Oh-My-Zsh (e alguns plugins como `zsh-syntax-highlighting`) resetam ou modificam o keymap durante o load. Qualquer `bindkey` colocado antes de `source $ZSH/oh-my-zsh.sh` pode ser sobrescrito.

**Sintoma:** O binding existe mas não funciona; `bindkey '<seq>'` no prompt mostra outro widget.

**Como detectar:** Adicionar `bindkey '<seq>'` no prompt pra ver o estado atual vs o que você configurou no `.zshrc`.

**Solução:** Colocar todos os `bindkey` no **final** do `.zshrc`, após o `source` do OMZ e de todos os plugins.

---

### 2. Escape sequences variam por terminal

**Causa:** Cada emulador de terminal (GNOME Terminal, iTerm2, Alacritty, Kitty, WezTerm) pode enviar sequências diferentes pra mesma tecla. Dentro de tmux ou Zellij, as sequências mudam novamente. Via SSH, o terminal local negocia o protocolo — o servidor recebe o que o cliente enviar.

**Sintoma:** Home/End/Ctrl-Arrows funcionam localmente mas não via SSH, ou funcionam no GNOME Terminal mas não no tmux.

**Como detectar:** `cat -v` no ambiente com problema — comparar a sequência com o que está no `.zshrc`.

**Solução:** Redescobrir as sequências com `cat -v` em cada ambiente. Usar `zkbd` pra automação. Considerar condicionais por `$TERM` ou `$TERMINAL` se precisar de config portável.

---

### 3. `Ctrl-S` capturado pelo terminal (XON/XOFF)

**Causa:** O protocolo XON/XOFF do terminal reserva `Ctrl-S` (stop output) e `Ctrl-Q` (resume output) antes que o ZLE veja a tecla.

**Sintoma:** Pressionar `Ctrl-S` "trava" o terminal (parece que travou mas é só o output suspenso). `Ctrl-Q` desbloqueia. O binding `bindkey '^S' history-incremental-search-forward` não funciona.

**Como detectar:** Pressionar `Ctrl-S` e verificar se o terminal para de responder. Confirmar com `stty -a | grep ixon`.

**Solução:**
```zsh
stty -ixon   # adicionar no .zshrc antes de qualquer bindkey ^S
```

---

### 4. Vi-mode sem indicador visual de modo

**Causa:** `bindkey -v` não fornece nenhum feedback visual de qual modo (insert vs normal) está ativo. É fácil digitar um comando em modo normal sem perceber — e tudo vira navegação vim.

**Sintoma:** Comandos aparentemente ignorados; cursor sumindo; `j`/`k` não navegando o history.

**Como detectar:** Pressionar `Esc` e verificar se comandos de edição Vim passam a funcionar — se sim, estava em insert.

**Solução — plugin `zsh-vim-mode`:**
```zsh
# custom plugin: jeffreytse/zsh-vi-mode (ou softmoth/zsh-vim-mode)
# muda a cor/forma do cursor por modo
```

**Solução — hook manual:**
```zsh
function zle-keymap-select {
  case $KEYMAP in
    vicmd)      print -n '\e[2 q' ;;  # cursor bloco (modo normal)
    viins|main) print -n '\e[6 q' ;;  # cursor barra (modo insert)
  esac
}
zle -N zle-keymap-select
```

---

## Em inglês

- **atalho de teclado** — *keybinding*. "Configure your keybindings in `.zshrc`."
- **tecla** — *key*. "Press the key to trigger the widget."
- **sequência de escape** — *escape sequence*. "Each terminal sends a different escape sequence for Home."
- **keymap** — *keymap*. "ZLE has several built-in keymaps: emacs, viins, vicmd."
- **modo emacs** — *emacs mode*. "Emacs mode is the ZLE default."
- **modo vi** — *vi mode*. "Enable vi mode with `bindkey -v`."
- **tecla modificadora** — *modifier key*. "Ctrl and Alt are common modifier keys."
- **descobrir sequência** — *find key sequence*. "Use `cat -v` to find the escape sequence for any key."
- **bindar tecla** — *bind a key*. "Bind the key to a widget with `bindkey`."
- **widget** — *widget*. "Register a custom widget with `zle -N`."

---

## Veja também

- [[07 - ZLE]] — sistema por trás dos widgets
- [[08 - Completion system (compsys)]] — Tab e completion-related bindings
- [[04 - Oh-My-Zsh — anatomia e plugins essenciais]] — plugins com bindings
- [[03-Dominios/Terminal/Shell/index|MOC do galho]]
- [[03-Dominios/Terminal/index|Trilha Terminal]]
- [[Dicionário do Terminal#Bindkey|bindkey]], [[Dicionário do Terminal#Widget|widget]], [[Dicionário do Terminal#Keymap|keymap]]

---

## Referências

- Zsh manual — Zsh Line Editor — https://zsh.sourceforge.io/Doc/Release/Zsh-Line-Editor.html
- zsh-history-substring-search — https://github.com/zsh-users/zsh-history-substring-search
