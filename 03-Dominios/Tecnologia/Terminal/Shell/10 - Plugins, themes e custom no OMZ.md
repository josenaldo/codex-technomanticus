---
title: "Plugins, themes e custom no OMZ"
created: 2026-05-19
updated: 2026-05-21
type: concept
progress: backlog
status: seedling
publish: true
fase: magus
tags:
  - terminal
  - shell
  - zsh
  - magus
  - oh-my-zsh
  - plugins
  - themes
aliases:
  - Plugins custom OMZ
  - Themes custom OMZ
---
# Plugins, themes e custom no OMZ

## TL;DR

Plugin custom OMZ = pasta `~/.oh-my-zsh/custom/plugins/<nome>/<nome>.plugin.zsh`. Theme custom = `~/.oh-my-zsh/custom/themes/<nome>.zsh-theme` com `PROMPT`/`RPROMPT`. Tudo em Zsh — sem build, sem manifest. Adicionar ao array `plugins=(...)` ou setar `ZSH_THEME` e source. Publicar = mover pra repo git e instruir clone.

---

## O que é / Como funciona

### Plugin custom OMZ

**Estrutura mínima:**

```
~/.oh-my-zsh/custom/plugins/<nome>/
└── <nome>.plugin.zsh
```

Naming convention (obrigatório): nome da pasta = nome do arquivo (sem extensão) + `.plugin.zsh`.

**Conteúdo do `.plugin.zsh`** pode incluir:

- Aliases: `alias gst='git status'`
- Funções: `myfunc() { ... }`
- Plugin completion: função `_<comando>` em arquivo separado dentro da pasta + `fpath+=(${0:h})` no topo do `.plugin.zsh`
- Inicialização: source de configs, registro de widgets, bindkey

**Loading:** adicionar `<nome>` ao array `plugins=(...)` no `.zshrc`. OMZ tenta carregar de `$ZSH_CUSTOM/plugins/<nome>/` primeiro; se não encontrar, cai pro `$ZSH/plugins/<nome>/` (embarcado). É por isso que custom **vence** override de plugins embarcados com o mesmo nome.

---

### Theme custom OMZ

**Estrutura mínima:**

```
~/.oh-my-zsh/custom/themes/<nome>.zsh-theme
```

**Variáveis chave:**

- `PROMPT` (alias: `PS1`) — prompt da esquerda (multilinha permitido com `\n`)
- `RPROMPT` (alias: `RPS1`) — prompt da direita (alinha à direita do terminal)
- `PS2` — continuation prompt (`>` quando comando incompleto)

**Prompt escape sequences (Zsh):**

- `%n` — username
- `%m` — hostname (sem domain)
- `%M` — hostname completo
- `%~` — cwd (contrai `$HOME` pra `~`)
- `%/` — cwd absoluto
- `%#` — `%` (user) ou `#` (root)
- `%?` — exit code do último comando
- `%j` — número de jobs
- `%(?.<true>.<false>)` — conditional (exit code 0 ou não)
- `%D{format}` — date/time formatada

**Color codes:**

- `%F{color}...%f` — foreground colorida (`color` = nome ou 0-255)
- `%K{color}...%k` — background colorida
- `%B...%b` — bold
- `%U...%u` — underline
- `%S...%s` — standout (reverse video)

**Git info no prompt** (via plugin OMZ `git` ou `vcs_info`):

```zsh
# PROMPT que mostra branch atual
# Requer plugin 'git' em plugins=(...) — git_prompt_info é função dele
PROMPT='%F{cyan}%~%f $(git_prompt_info)%# '
```

`git_prompt_info` é uma função do plugin `git` embarcado no OMZ — retorna a branch atual com delimitadores configuráveis via `ZSH_THEME_GIT_PROMPT_PREFIX`/`ZSH_THEME_GIT_PROMPT_SUFFIX`.

**Loading:** setar `ZSH_THEME="<nome>"` no `.zshrc` (sem `.zsh-theme`). OMZ tenta carregar de `$ZSH_CUSTOM/themes/<nome>.zsh-theme` primeiro; se não encontrar, cai pro `$ZSH/themes/<nome>.zsh-theme` (embarcado). É por isso que custom **vence** override.

---

### Por que Powerlevel10k é prompt e não theme tradicional

P10k é mais que um `.zsh-theme` — tem instant prompt (precisa estar no TOPO do `.zshrc`), wizard (`p10k configure`), segments programáveis, e hooks de redisplay. Por isso o setup recomendado pelo projeto é **clone direto + source manual**, não `ZSH_THEME`. P10k pode ser usado como OMZ theme (`ZSH_THEME="powerlevel10k/powerlevel10k"`), mas perde o instant prompt — o bloco de instant prompt precisa ser sourced antes do OMZ, e o sistema de themes do OMZ só sourced o theme depois.

---

### Publicação

- **Custom local:** fica em `~/.oh-my-zsh/custom/`. Vincular ao seu repo de dotfiles (symlink ou stow).
- **PR upstream pro OMZ:** se for útil pra muitos, abrir PR em `ohmyzsh/ohmyzsh` seguindo `CONTRIBUTING.md`.
- **Repo próprio:** criar repo git `<usuario>/<plugin-name>` com README explicando install (`git clone ... custom/plugins/<nome>`).
- **Plugin managers que entendem repos:** zinit, zplug, antibody (arquivado em 2021 — prefira zinit ou zplug em novos setups) — permitem source de plugins direto do GitHub sem clone manual (galho 5 — Dotfiles).

---

## Na prática

### Exemplo: plugin custom `notify` (avisar quando comando longo termina)

Estrutura:

```
~/.oh-my-zsh/custom/plugins/notify/
└── notify.plugin.zsh
```

Conteúdo de `notify.plugin.zsh`:

```zsh
# Avisar via notify-send quando comando que demorou >=10s termina.
# Requer: notify-send instalado (pacote libnotify-bin no Debian/Ubuntu)
# Requer: zmodload zsh/datetime (carregado por default em Zsh interativo moderno)
# Uso: notify-long <comando> [args...]
# Ex:  notify-long npm install

notify-long() {
  local start end elapsed
  start=$EPOCHSECONDS
  "$@"
  local exit_code=$?
  end=$EPOCHSECONDS
  elapsed=$((end - start))

  if (( elapsed >= 10 )); then
    if (( exit_code == 0 )); then
      notify-send "Comando terminou" "$*\nTempo: ${elapsed}s"
    else
      notify-send "Comando falhou" "$*\nExit: $exit_code"
    fi
  fi
  return $exit_code
}
```

Nota: `$EPOCHSECONDS` é provida pelo módulo `zsh/datetime`. Em Zsh interativo moderno, esse módulo já é carregado. Em scripts não-interativos, adicione `zmodload zsh/datetime` no topo do plugin.

Ativar no `.zshrc`:

```zsh
plugins=(... notify)
```

Abrir novo shell (ou `source ~/.zshrc`) e testar:

```zsh
notify-long sleep 15
```

---

### Exemplo: theme custom minimalista `tiny`

Estrutura:

```
~/.oh-my-zsh/custom/themes/tiny.zsh-theme
```

Conteúdo de `tiny.zsh-theme`:

```zsh
# Prompt minimalista de 1 linha
# Formato: cwd colorida + git branch (se em repo) + caractere de prompt

setopt PROMPT_SUBST

function tiny_git_branch() {
  local branch
  branch=$(git symbolic-ref --short HEAD 2>/dev/null)
  [[ -n "$branch" ]] && echo " %F{yellow}(${branch})%f"
}

PROMPT='%F{cyan}%~%f$(tiny_git_branch) %# '
RPROMPT='%(?..%F{red}[%?]%f)'   # exit code no RPROMPT se != 0
```

Ativar no `.zshrc`:

```zsh
ZSH_THEME="tiny"
```

Abrir novo shell e testar em um diretório git.

> **Nota sobre `PROMPT_SUBST`:** O OMZ ativa `setopt PROMPT_SUBST` automaticamente. O `setopt` no arquivo `.zsh-theme` é idempotente — reforça o comportamento esperado para o caso de uso do theme fora do OMZ, mas não é necessário quando o OMZ já está ativo.

---

### Exemplo: completion custom dentro do plugin

Plugin `mytool` com completion própria:

```
~/.oh-my-zsh/custom/plugins/mytool/
├── mytool.plugin.zsh
└── _mytool
```

`mytool.plugin.zsh`:

```zsh
# Adiciona a pasta do plugin ao fpath pra que `_mytool` seja encontrado pelo compinit
# ${0:h} = dirname do arquivo atual (modifier Zsh "head")
fpath+=(${0:h})
```

`_mytool` (função de completion):

```zsh
#compdef mytool

_mytool() {
  local -a subcommands
  subcommands=('init:Initialize project' 'build:Build project' 'serve:Serve dev')
  _describe 'subcommand' subcommands
}
```

Ativar adicionando `mytool` ao array `plugins=(...)` e rebuild do dump:

```zsh
rm ~/.zcompdump*; compinit
```

---

## Armadilhas

### 1. Naming convention quebrada

**Causa:** OMZ procura especificamente `<pasta>.plugin.zsh` dentro da pasta do plugin. Um arquivo com nome diferente (ex: `my_tool.plugin.zsh` numa pasta `mytool/`) não é encontrado.

**Sintoma:** Plugin não carrega; aliases e funções definidos nele ficam indisponíveis mesmo após source do `.zshrc`.

**Como detectar:** `ls ~/.oh-my-zsh/custom/plugins/<nome>/` — verificar se o arquivo `.plugin.zsh` tem exatamente o mesmo nome da pasta (ex: pasta `notify/` → arquivo `notify.plugin.zsh`).

**Solução:** Renomear o arquivo para `<nome>.plugin.zsh`, onde `<nome>` é idêntico ao nome da pasta.

---

### 2. Custom override silencioso

**Causa:** OMZ prioriza `custom/` sobre os plugins embarcados. Criar `~/.oh-my-zsh/custom/plugins/git/git.plugin.zsh` faz o OMZ usar o seu arquivo em vez do plugin `git` upstream — sem aviso.

**Sintoma:** Aliases do plugin `git` embarcado somem ou têm comportamento inesperado; difícil de rastrear porque a mudança é silenciosa.

**Como detectar:** `omz reload` + `which gst` (ou `type gst`) — se o alias do plugin git não existir ou for diferente, confirma o override. Também: `ls ~/.oh-my-zsh/custom/plugins/` para verificar colisões de nome.

**Solução:** Renomear o plugin custom para não colidir com plugins embarcados (ex: `mygit` em vez de `git`). Se o objetivo for sobrescrever deliberadamente, documentar no plugin que é um override intencional.

---

### 3. Theme sem `setopt PROMPT_SUBST` em contexto não-OMZ

**Causa:** `PROMPT_SUBST` não é ativo no Zsh vanilla por default. O OMZ o ativa automaticamente, mas se o theme for sourced fora do OMZ (ou antes dele), a opção pode não estar ativa.

**Sintoma:** Funções chamadas dentro de `PROMPT` (como `$(tiny_git_branch)`) aparecem literalmente no prompt em vez de serem executadas.

**Como detectar:** Olhar o prompt — se mostrar `$(nome_da_funcao)` literal em vez do valor retornado, `PROMPT_SUBST` está inativo. Confirmar: `setopt | grep -i promptsubst`.

**Solução:** Adicionar `setopt PROMPT_SUBST` no topo do theme ou no `.zshrc` antes do source do OMZ. Com OMZ, o `setopt` no theme é idempotente e inofensivo.

---

### 4. Custom completion sem rebuild de `.zcompdump`

**Causa:** `compinit` cacheia as funções de completion conhecidas em `~/.zcompdump`. Ao adicionar um novo plugin com completion, o cache ainda não inclui a nova função `_<comando>`.

**Sintoma:** Tab não completa o novo comando mesmo com o plugin carregado e o `fpath` atualizado.

**Como detectar:** `which _mytool` (ou `type _mytool`) — se a função existir mas o Tab não funcionar, o problema é o cache. Confirmar: `print -l $fpath` para ver se o diretório do plugin está no fpath.

**Solução:** Deletar o cache e reinicializar: `rm ~/.zcompdump*; compinit`. Ou abrir um terminal novo (OMZ chama `compinit` no startup e recria o dump se necessário).

---

### 5. Source manual do `.plugin.zsh` antes do OMZ load

**Causa:** Variáveis como `$ZSH`, `$ZSH_CUSTOM`, `$ZSH_THEME` são definidas pelo OMZ. Source de um plugin antes de `source "$ZSH/oh-my-zsh.sh"` não tem esse contexto disponível.

**Sintoma:** Erros "no such file or directory", variáveis `$ZSH` vazias, ou comportamento inconsistente se o plugin depende de funções ou variáveis do OMZ.

**Como detectar:** Trace com `set -x` no `.zshrc` — verificar a ordem em que o plugin é sourced relativo ao `source "$ZSH/oh-my-zsh.sh"`.

**Solução:** Usar o array `plugins=(...)` em vez de source manual. O OMZ garante que o plugin é carregado depois do contexto estar pronto.

---

### 6. Theme define `RPROMPT` direto e apaga output de outros plugins

**Causa:** Alguns plugins (ex: indicador de vi-mode, command-time) escrevem em `RPROMPT` via hook `precmd`. Se o theme define `RPROMPT="..."` diretamente (atribuição simples), sobrescreve o que o plugin tentou escrever.

**Sintoma:** Features de outros plugins não aparecem no lado direito do prompt; ex: indicator de modo vi some ao usar um theme custom.

**Como detectar:** Comentar a linha `RPROMPT=...` do theme e recarregar — se a feature do plugin aparecer, confirma a colisão.

**Solução:** Compor via hook: usar `precmd_functions+=(meu_rprompt_hook)` + função que concatena. Ou usar `RPROMPT+="..."` com cautela (ordem de concatenação importa). A abordagem mais robusta é definir a parte fixa do RPROMPT num hook `precmd` em vez de no corpo do theme.

---

## Em inglês

- **plugin** — *plugin*. "An OMZ plugin is a folder containing a `.plugin.zsh` file loaded via the `plugins=(...)` array."
- **tema** — *theme*. "A custom theme overrides `PROMPT` and `RPROMPT` via a `.zsh-theme` file in the `custom/themes/` folder."
- **customizar** — *customize*. "Everything inside `custom/` survives `omz update` and is the right place to customize your setup."
- **sobrescrever** — *override*. "Custom plugins override built-in plugins of the same name — OMZ loads `custom/` first."
- **publicar** — *publish*. "To publish a plugin, create a git repository and document the manual clone install."
- **repositório** — *repository*. "Clone external plugins into `$ZSH_CUSTOM/plugins/<name>` from their repository."
- **contribuir upstream** — *contribute upstream*. "If your plugin is broadly useful, consider contributing upstream by opening a PR to `ohmyzsh/ohmyzsh`."
- **naming convention** — *naming convention*. "OMZ enforces a naming convention: the plugin file must match the folder name exactly."
- **expansão de prompt** — *prompt expansion*. "Zsh prompt expansion converts escape sequences like `%n` and `%~` into dynamic values when `PROMPT_SUBST` is active."
- **substituição** — *substitution*. "Command substitution inside `PROMPT` (e.g., `$(git_branch)`) requires `PROMPT_SUBST` to be set."

---

## Veja também

- [[04 - Oh-My-Zsh — anatomia e plugins essenciais]] — pré-req: anatomia e plugins essenciais
- [[05 - Powerlevel10k]] — caso de theme externo avançado
- [[08 - Completion system (compsys)]] — completion custom pré-req
- [[09 - Globbing avançado e parameter expansion]] — globbing em scripts de plugin
- [[03-Dominios/Tecnologia/Terminal/Shell/index|MOC do galho]]
- [[03-Dominios/Tecnologia/Terminal/index|Trilha Terminal]]
- [[Dicionário do Terminal#Plugin (OMZ)|plugin]], [[Dicionário do Terminal#Theme (custom OMZ)|theme]]

---

## Referências

- OMZ Customization wiki: https://github.com/ohmyzsh/ohmyzsh/wiki/Customization
- Zsh manual — Prompt Expansion: https://zsh.sourceforge.io/Doc/Release/Prompt-Expansion.html
