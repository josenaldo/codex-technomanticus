---
title: "Zsh essencial"
created: 2026-05-20
updated: 2026-05-20
type: concept
progress: backlog
status: seedling
publish: true
fase: iniciado
tags:
  - terminal
  - shell
  - zsh
  - iniciado
  - aliases
  - functions
  - setopt
aliases:
  - Zsh essencial
  - Aliases, funções e opts
---

# Zsh essencial

> [!abstract] TL;DR
> Aliases viram comandos longos em curtos. Funções juntam várias linhas com parâmetros e return code. `setopt` muda comportamento do shell (`EXTENDED_GLOB`, `AUTO_CD`, `INTERACTIVE_COMMENTS`). Onde colocar tudo: `~/.zshrc` (interativo) vs `~/.zshenv` (sempre, inclusive scripts).

## O que é / Como funciona

### Aliases — 3 tipos

Alias é um atalho que o Zsh expande antes de executar o comando. Existem três tipos:

#### Regular

```zsh
alias gco='git checkout'
alias ll='ls -lah'
alias ..='cd ..'
```

- Expansão ocorre **apenas no início do comando** (posição de comando).
- Uma barra invertida antes do nome (`\rm`) ou `command rm` bypassa o alias e chama o binário diretamente.
- `alias` sem argumentos lista todos os aliases definidos.
- `unalias nome` remove; `alias -L` imprime em formato reutilizável em scripts.

#### Global (`-g`)

```zsh
alias -g G='| grep'
alias -g L='| less'
alias -g NUL='> /dev/null 2>&1'
```

- Expande **em qualquer posição** do comando, não apenas no início.
- Exemplos de uso:

```zsh
ps aux G nginx       # → ps aux | grep nginx
journalctl -xe L     # → journalctl -xe | less
```

- Poderosos, mas podem surpreender: qualquer ocorrência do token `G` no comando será expandida.

#### Suffix (`-s`)

```zsh
alias -s md=nvim
alias -s json=cat
alias -s py=python3
```

- Dispara quando você digita um **arquivo com aquele sufixo** como comando.
- `./README.md` → executa `nvim ./README.md`.
- Útil para "abrir com" sem lembrar o programa certo.

---

### Funções — declaração e mecânica

Funções são blocos nomeados de comandos que aceitam parâmetros, têm escopo local e retornam código de saída.

#### Sintaxe de declaração

As duas formas são **equivalentes**:

```zsh
# Forma 1 — POSIX-style
mkcd() {
  # ...
}

# Forma 2 — Zsh/ksh-style
function mkcd {
  # ...
}
```

#### Parâmetros

| Token | Significado                              |
|-------|------------------------------------------|
| `$0`  | Nome da função                           |
| `$1`  | Primeiro argumento                       |
| `$2`  | Segundo argumento                        |
| `$@`  | Todos os argumentos (array preservado)   |
| `$#`  | Contagem de argumentos                   |

```zsh
mostrar() {
  print "Nome da função: $0"
  print "Primeiro arg:   $1"
  print "Todos os args:  $@"
  print "Quantidade:     $#"
}
```

#### `local` — escopo de variáveis

```zsh
calcular() {
  local resultado   # visível apenas dentro desta função
  resultado=$(( $1 + $2 ))
  print "$resultado"
}
```

Sem `local`, a variável vaza para o shell pai. Sempre declare variáveis temporárias com `local`.

#### `return` — código de retorno

```zsh
checar_arquivo() {
  local path="$1"
  [[ -f "$path" ]] || return 1   # falha: arquivo não existe
  return 0                        # sucesso (implícito se omitido)
}
```

- `return 0` = sucesso; qualquer outro valor = falha.
- Sem `return`, o código de saída é o do último comando executado.

#### Alias vs função — quando usar cada um

| Situação                        | Usar          |
|---------------------------------|---------------|
| Renomear / encurtar comando     | alias         |
| Lógica, condicionais, loops     | função        |
| Aceitar parâmetros variáveis    | função        |
| Piping inline (posição qualquer)| alias global  |
| "Abrir com" por extensão        | alias suffix  |

---

### `setopt` — interface de opts

O builtin `setopt` ativa e desativa opções do comportamento do Zsh.

```zsh
setopt EXTENDED_GLOB     # liga a opção
unsetopt EXTENDED_GLOB   # desliga a opção
setopt                   # lista todas as opções atualmente ligadas
setopt | grep history    # busca entre as opções ativas
```

Opções são **case-insensitive** e underscores são ignorados: `EXTENDED_GLOB`, `extendedglob` e `extended_glob` são equivalentes.

Prefixo `NO_` (ou `no`) desativa: `setopt NO_BEEP` é o mesmo que `unsetopt BEEP`.

#### Opts essenciais — o que cada uma faz

| Opção                  | Efeito                                                                 |
|------------------------|------------------------------------------------------------------------|
| `AUTO_CD`              | Digite só o nome do diretório para entrar nele (sem `cd`)              |
| `EXTENDED_GLOB`        | Habilita `#`, `~`, `^` como metacaracteres em padrões de globbing      |
| `INTERACTIVE_COMMENTS` | Permite comentários com `#` na linha de comando interativa             |
| `NO_BEEP`              | Silencia o bipe em erros do ZLE                                        |
| `CORRECT`              | Sugere correção ortográfica quando o comando não existe                |
| `PROMPT_SUBST`         | Permite expansão de parâmetros e subcomandos no prompt (`$PS1`)        |
| `SHARE_HISTORY`        | Sincroniza histórico entre sessões abertas simultaneamente              |

---

### Variáveis vs env

#### Escopo de variáveis

```zsh
var=valor          # variável local ao processo shell atual
export var=valor   # variável de ambiente: visível a subprocessos
```

Subprocessos (scripts, programas externos) **não enxergam** variáveis não exportadas.

```zsh
EDITOR=nvim           # sem export: só este shell enxerga
export EDITOR=nvim    # com export: subprocessos (git, etc.) enxergam
```

#### Modificadores úteis com `typeset`

```zsh
typeset -r CONST=42        # readonly — qualquer tentativa de mudar gera erro
typeset -U PATH            # unique — remove duplicatas ao fazer PATH=$PATH:...
local var                  # scope de função (equivalente a typeset sem flags)
```

`typeset -U PATH` é especialmente útil em `.zshrc` para evitar que o `$PATH` cresça com duplicatas a cada reload.

---

### Loading order (CRÍTICO)

O Zsh carrega arquivos de config em ordem fixa dependendo do tipo de shell:

```
~/.zshenv          → SEMPRE (login, interativo, script, qualquer)
~/.zprofile        → login shell (antes de .zshrc)
~/.zshrc           → shell interativo (terminal aberto pelo usuário)
~/.zlogin          → login shell (depois de .zshrc — raramente usado)
~/.zlogout         → ao sair de um login shell
```

#### O que colocar em cada arquivo

| Arquivo         | Colocar                                                            | Não colocar                          |
|-----------------|--------------------------------------------------------------------|--------------------------------------|
| `~/.zshenv`     | `EDITOR`, `PATH`, variáveis que processos não-interativos precisam | Aliases, funções interativas, prompts |
| `~/.zprofile`   | Comandos que rodam uma vez ao fazer login (homebrew path, etc.)    | Aliases, setopt                      |
| `~/.zshrc`      | Aliases, funções, `setopt`, plugins OMZ, prompt, completions       | Nada lento ou desnecessário em scripts|
| `~/.zlogin`     | Comandos pós-inicialização de login (raros)                        | Configuração de shell                 |

**Regra prática:** quase tudo vai em `~/.zshrc`. Só vai em `~/.zshenv` o que scripts não-interativos precisam enxergar (como `$EDITOR` e `$PATH`).

---

## Na prática

### Bloco de `setopt` para `~/.zshrc`

```zsh
# AUTO_CD: digite só o diretório (sem `cd`) e ele entra
setopt AUTO_CD

# Comentários inline no shell interativo
setopt INTERACTIVE_COMMENTS

# Globbing extended (necessário pra muito do que Zsh oferece de melhor)
setopt EXTENDED_GLOB

# Sem bipe ao errar
setopt NO_BEEP

# Sugere correção quando comando não existe
setopt CORRECT

# Substituição em prompt — já ativo por default em shells interativos modernos; incluído por explicitidade
setopt PROMPT_SUBST

# Sincroniza histórico entre sessões simultâneas
setopt SHARE_HISTORY
```

---

### Função de exemplo — `mkcd`

Cria um diretório e entra nele:

```zsh
mkcd() {
  local dir="$1"
  [[ -z "$dir" ]] && { print -u2 "uso: mkcd <dir>"; return 1; }
  mkdir -p "$dir" && cd "$dir"
}
```

- `local dir` — escopo isolado, não vaza.
- `print -u2` — escreve em stderr (file descriptor 2).
- `return 1` — sinaliza falha se chamado sem argumento.
- `mkdir -p` cria hierarquia completa; `&& cd` só entra se a criação teve sucesso.

---

### Aliases no `~/.zshrc` — exemplos organizados

```zsh
# --- Aliases regulares ---
alias ll='ls -lah'
alias la='ls -A'
alias gco='git checkout'
alias gcb='git checkout -b'
alias gst='git status'
alias vim='nvim'
alias zrc='${EDITOR:-nvim} ~/.zshrc'

# --- Aliases globais ---
alias -g G='| grep'           # `ps aux G nginx` → `ps aux | grep nginx`
alias -g L='| less'           # `journalctl -xe L` → `| less`
alias -g NUL='> /dev/null 2>&1'

# --- Aliases suffix ---
alias -s md=nvim              # `./README.md` abre nvim
alias -s json=cat             # `./config.json` imprime no terminal
alias -s py=python3           # `./script.py` executa
```

---

### Variáveis no `~/.zshenv` — o que vai aqui

```zsh
# ~/.zshenv — carregado em QUALQUER tipo de shell
export EDITOR='nvim'
export VISUAL='nvim'
export PAGER='less'
export LANG='en_US.UTF-8'

# PATH sem duplicatas
typeset -U PATH
path=("$HOME/.local/bin" "$HOME/bin" $path)
```

Nota: `path` (minúsculo) é um array Zsh amarrado (tied) ao `$PATH` (maiúsculo). Modificar `path` como array e manter `typeset -U PATH` previne duplicatas automaticamente.

---

## Armadilhas

### 1. Alias que sobrescreve e muda semântica

**Causa:** `alias rm='rm -i'` altera o comportamento padrão do `rm`.

**Sintoma:** Um script que chama `rm arquivo` fica pendurado aguardando confirmação interativa — ou pior, falha silenciosamente em modo não-interativo.

**Como detectar:**

```zsh
type rm          # mostra: "rm is an alias for rm -i"
alias | grep rm  # lista o alias definido
```

**Solução:** Use `\rm arquivo` ou `command rm arquivo` para bypassar o alias. Em scripts, prefira sempre `command <nome>` para garantir que o binário é chamado.

---

### 2. `export` dentro de função polui o ambiente global

**Causa:** Uma variável declarada com `export` dentro de uma função permanece exportada no ambiente da shell depois que a função retorna.

**Sintoma:** Subprocessos subsequentes enxergam uma variável que deveria ser temporária.

```zsh
configurar_tmp() {
  export DEBUG=1    # ERRADO: vaza pra fora da função
  fazer_algo
}
configurar_tmp
echo $DEBUG         # ainda é "1" — vazou
```

**Solução:** Use `local` para variáveis temporárias:

```zsh
configurar_tmp() {
  local DEBUG=1     # fica dentro da função
  fazer_algo
}
```

---

### 3. Código lento em `~/.zshenv` derruba performance de scripts

**Causa:** `~/.zshenv` é carregado em **todo** invocação de subshell — incluindo scripts, completions e processos internos do Zsh.

**Sintoma:** Scripts simples ficam lentos; ferramentas como `git` que chamam scripts Zsh internamente ficam lentas.

**Como detectar:**

```zsh
# Medir tempo de inicialização de um script simples
time zsh -c 'exit'
```

Se o resultado for > ~100ms, algo em `~/.zshenv` está pesado.

**Solução:** Mova tudo que é só interativo (aliases, completions, prompts, plugins) para `~/.zshrc`. Em `~/.zshenv`, mantenha apenas exports simples.

---

### 4. `setopt CORRECT` interfere em loops e scripts

**Causa:** `CORRECT` sugere correções ortográficas de comandos. Em shells interativos, isso é útil. Em scripts ou contextos automatizados, pode bloquear a execução.

**Sintoma:** Script para e pede confirmação (`zsh: correct 'x' to 'y' [nyae]?`) ou falha de modo inesperado.

**Solução:** Desligar pontualmente antes de blocos sensíveis:

```zsh
unsetopt CORRECT
fazer_coisa_automatizada
setopt CORRECT
```

Ou simplesmente não ative `CORRECT` em scripts — reserve para o `~/.zshrc` interativo.

---

## Em inglês

- **alias** — *alias*. "A regular alias expands only at command position; a global alias expands anywhere in the command line."
- **função (shell)** — *function*. "A shell function groups commands under a name, accepts parameters, and returns an exit code."
- **opt (opção)** — *option*. "Shell options are toggled with `setopt` and `unsetopt`; they control interpreter behavior."
- **shell interativo** — *interactive shell*. "An interactive shell reads from a terminal and loads `~/.zshrc`."
- **exportar variável** — *export variable*. "Exporting a variable makes it visible to child processes as an environment variable."
- **escopo local** — *local scope*. "A variable declared with `local` inside a function is destroyed when the function returns."
- **código de retorno** — *return code* / *exit code*. "By convention, return code 0 means success; any non-zero value signals failure."
- **variável de ambiente** — *environment variable*. "Environment variables are inherited by child processes and visible via `env`."
- **shell de login** — *login shell*. "A login shell reads `~/.zprofile` and `~/.zlogin` in addition to `~/.zshrc`."
- **ordem de carregamento** — *loading order*. "The loading order of Zsh startup files is: `.zshenv` → `.zprofile` → `.zshrc` → `.zlogin`."

---

## Veja também

- [[01 - Zsh vs Bash]] — diferenças entre Zsh e Bash, contexto de por que cada opt existe
- [[03 - History do Zsh]] — `SHARE_HISTORY`, `HIST_IGNORE_DUPS` e outras opts de histórico
- [[04 - Oh-My-Zsh — anatomia e plugins essenciais]] — onde aliases e funções convivem com plugins OMZ
- [[09 - Globbing avançado e parameter expansion]] — `EXTENDED_GLOB` é pré-requisito para os padrões avançados
- [[03-Dominios/Terminal/Shell/index|MOC do galho Shell]]
- [[Dicionário do Terminal#Alias|alias]], [[Dicionário do Terminal#Function (shell)|função]], [[Dicionário do Terminal#Setopt|setopt]]

---

## Referências

- Zsh manual — Options: <https://zsh.sourceforge.io/Doc/Release/Options.html>
- Zsh manual — Shell Builtin Commands: <https://zsh.sourceforge.io/Doc/Release/Shell-Builtin-Commands.html>
- A User's Guide to the Z-Shell: <https://zsh.sourceforge.io/Guide/zshguide.html>
