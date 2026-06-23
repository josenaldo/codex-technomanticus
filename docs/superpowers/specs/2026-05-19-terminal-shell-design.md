---
title: "Spec — Galho 2 da trilha Terminal (Shell / Zsh + Oh-My-Zsh + Powerlevel10k)"
date: 2026-05-19
author: Josenaldo
status: draft
type: spec
publish: false
---

# Spec — Galho 2 da trilha Terminal (Shell / Zsh + Oh-My-Zsh + Powerlevel10k)

## 1. Contexto e motivação

Este é o **segundo galho** da trilha Terminal (roadmap em `docs/superpowers/specs/2026-05-18-trilha-terminal-design.md`). Pressupõe leitura desse roadmap — a tríade Iniciado/Adepto/Magus, a estrutura tronco/galho e a iteração vertical por galho não são repetidas aqui.

O usuário já roda Zsh + Oh-My-Zsh + Powerlevel10k como shell daily-driver há tempo, com `~/.zshrc` enxuto (template OMZ + 7 plugins + ~10 linhas de customização) e `~/.p10k.zsh` gerado pelo wizard P10k em estilo rainbow + powerline + 2 linhas + nerdfont-v3. Sabe operar mas não dominou o motor: completion ainda é caixa-preta, ZLE/widgets nunca abriu, globbing avançado é misterioso, e há conflitos visíveis na config (dois plugins de syntax-highlight carregados, `zsh-autocomplete` sobrepondo OMZ completion, NVM duplicado em `.zshenv`+`.zshrc`) que ele não diagnosticou.

As 10 notas cobrem do "Zsh vs Bash" até "escrevendo seu plugin OMZ". A ordem é por fase (Iniciado → Adepto → Magus), e OMZ + P10k é o caminho primário em Iniciado/Adepto (porque é o setup real do usuário); Zsh puro aparece quando o conceito é universal (history, setopt, expansion) e domina em Magus.

## 2. Objetivo

Produzir, em uma sessão de execução dedicada, **10 notas atômicas + 1 MOC do galho + expansão do Dicionário do Terminal** em `03-Dominios/Tecnologia/Terminal/Shell/` e `03-Dominios/Tecnologia/Terminal/`, todas `publish: true`, em PT-BR, distribuídas em 3 fases (4 Iniciado + 4 Adepto + 2 Magus).

A trilha precisa ser:

- **Atômica** — cada nota linkável e citável separadamente
- **Híbrida em camadas** — TL;DR + corpo técnico, no padrão do vault
- **Casada com o setup real** — OMZ + P10k 2024-07 instalado via git em `~/powerlevel10k/`, plugins canônicos do usuário usados como referência
- **Atualizada com 2026** — Zsh 5.9+, OMZ master, P10k congelado em 2024 (fato relevante e mencionado)
- **Apoiada por dicionário** — jargão técnico tem verbete no dicionário do domínio, linkado nas notas

## 3. Escopo

### Em escopo

- 11 arquivos markdown:
  - 10 notas em `03-Dominios/Tecnologia/Terminal/Shell/`
  - 1 MOC do galho em `03-Dominios/Tecnologia/Terminal/Shell/index.md`
- Expansão do `03-Dominios/Tecnologia/Terminal/Dicionário do Terminal.md` com **≥30 verbetes novos** (bloco "Shell / Zsh / OMZ"); verbetes existentes "Keymap" e "Plugin" expandidos com sub-definições Zsh
- Atualização do tronco `03-Dominios/Tecnologia/Terminal/index.md` ativando o wikilink do Shell
- Todos os arquivos com `publish: true`
- Idioma: PT-BR; termos técnicos em inglês mantidos; cada nota tem seção "Em inglês" com 5-10 termos PT→EN
- Pesquisa baseada em fontes primárias verificadas (links concretos no spec)
- Trechos de config reais do usuário (com paths generalizados pra `~/...` e aliases pessoais omitidos/anonimizados)

### Fora de escopo

- **Comparativo extenso shell-a-shell** (fish, nushell, elvish) — nota 01 toca por que Zsh, mas não desenvolve outras shells
- **Bash em profundidade** — só o necessário pra mostrar diferenças relevantes
- **Distribuições alternativas a OMZ** (Prezto, zinit como manager principal, Antibody) — nota 04 cita em "Veja também" sem desenvolver
- **Theme engines alternativos a P10k** (starship, pure, oh-my-posh) — nota 05 cita em "Veja também" + armadilha "P10k congelado", sem virar comparativo
- **Integração de ferramentas externas** (NVM, asdf, direnv, sdkman) — pertencem ao galho 5 (Dotfiles) ou Workflow (7). Aparição casual em notas 02/04 sem aprofundamento.
- **Scripting shell genérico** (loops, condicionais, traps) — pertence a um futuro galho de scripting ou ao domínio Linux
- **Workflow cross-tool** (Zellij + Shell, Lazygit + Shell) — outros galhos da trilha

### Foco

Dev individual operando shell interativo no setup OMZ + P10k. Comandos do dia-a-dia, customização real e diagnóstico de problemas comuns no stack.

## 4. Audiência e barra de qualidade

**Audiência primária:** dev senior com fluência shell (Bash) e anos de IntelliJ/VS Code. Já usa OMZ + P10k mas não customizou nada além do que o wizard gerou. Quer dominar — não regredir.

**Audiência secundária:** o mesmo dev seis meses depois, voltando pra técnica específica esquecida (regex de compsys, glob qualifier, escrever widget custom).

**Barra de qualidade:** ao terminar de ler o galho, o leitor deve conseguir:

1. Escrever função Zsh com locals e return code, e adicionar ao `~/.zshrc`
2. Configurar history pra share + extended + sem-duplicatas, e usar `fc` pra editar comandos
3. Listar e auditar plugins OMZ ativos (`omz plugin list`, `omz plugin info <name>`)
4. Rodar `p10k configure` confiante; ajustar segmentos manualmente em `~/.p10k.zsh`
5. Bindar Home/End/Ctrl-Arrows corretamente em qualquer terminal (`cat -v` + `bindkey`)
6. Escrever widget Zsh simples (e.g., `expand-or-complete-with-dots`) e ligar com `bindkey`
7. Debug de completion (`compaudit`, rebuild de `.zcompdump`, `zstyle`)
8. Usar globbing avançado pra operações reais (`rm **/*.log(.om[1,5])`, `print -l **/*.ts(N)`)
9. Escrever plugin OMZ próprio + theme próprio
10. Diagnosticar conflito entre plugins (zsh-autocomplete vs OMZ completion, syntax-highlight double-load)

## 5. Estrutura do galho (11 arquivos)

### MOC do galho

Arquivo: `03-Dominios/Tecnologia/Terminal/Shell/index.md` (mesmo padrão do MOC do Editor).

Estrutura:

```markdown
> [!abstract] TL;DR
> Galho 2 da trilha Terminal. Domínio de Zsh + Oh-My-Zsh + Powerlevel10k como
> shell primário, em 3 fases (4 + 4 + 2 = 10 notas).

## Iniciado
- [[01 - Zsh vs Bash]]
- [[02 - Zsh essencial]]
- [[03 - History do Zsh]]
- [[04 - Oh-My-Zsh — anatomia e plugins essenciais]]

## Adepto
- [[05 - Powerlevel10k]]
- [[06 - Keybindings práticos]]
- [[07 - ZLE]]
- [[08 - Completion system (compsys)]]

## Magus
- [[09 - Globbing avançado e parameter expansion]]
- [[10 - Plugins, themes e custom no OMZ]]

## Rotas alternativas
- **Daily-driver enxuto** (Iniciado completa): 01 → 02 → 03 → 04
- **Customização visual**: 04 → 05 → 10
- **Domínio do motor**: 02 → 06 → 07 → 08 → 09

## Versões assumidas
- Zsh 5.9+ (Ubuntu/Linux bundle)
- Oh-My-Zsh master (commit ~maio/2026)
- Powerlevel10k master (último release: 2024-07, projeto congelado)

## Veja também
- [[Dicionário do Terminal]]
- [[03-Dominios/Tecnologia/Terminal/index|Trilha Terminal]]
```

### Fase Iniciado (4 notas)

#### 01 — Zsh vs Bash
- **Slug:** `01 - Zsh vs Bash.md`
- **Primárias:**
  - [Zsh manual — overview](https://zsh.sourceforge.io/Doc/Release/Introduction.html)
  - [Zsh FAQ — Differences from Bash](https://zsh.sourceforge.io/FAQ/zshfaq02.html)
- **Secundárias:**
  - [Bash to Z Shell migration guide (autor canônico)](https://zsh.sourceforge.io/Guide/zshguide.html)
  - [Apple docs — switching to Zsh as default](https://support.apple.com/en-us/HT208050) (contexto histórico do macOS)
- **Cobre:**
  - O que é shell, shell interativo vs script
  - POSIX compliance (Bash mais próximo, Zsh com extensões pesadas)
  - Diferenças sintáticas relevantes (arrays 1-indexed, `setopt` vs `shopt`, `${(L)var}` vs `${var,,}`, globbing)
  - Por que Zsh: interatividade rica, completion superior, extensibilidade
  - Custo da migração: scripts Bash precisam de `#!/usr/bin/env bash` ou compatibilidade explícita (`emulate bash`)
  - Mito "Zsh é superset de Bash" — falso, é parente próximo com escolhas diferentes
- **Não cobre:** outras shells (fish, nushell), Zsh scripting profundo (não é o foco do galho)
- **Verbetes referenciados:** shell, POSIX, builtin

#### 02 — Zsh essencial
- **Slug:** `02 - Zsh essencial.md`
- **Primárias:**
  - [Zsh manual — Options](https://zsh.sourceforge.io/Doc/Release/Options.html)
  - [Zsh manual — Shell Builtin Commands (alias/function/setopt)](https://zsh.sourceforge.io/Doc/Release/Shell-Builtin-Commands.html)
- **Secundárias:**
  - [The Z shell — quick reference (Stephenson)](https://zsh.sourceforge.io/Guide/zshguide03.html)
  - [Awesome Zsh — opts populares](https://github.com/unixorn/awesome-zsh-plugins)
- **Cobre:**
  - `alias` (regular, `-g` global, `-s` suffix), quando usar cada um
  - Funções: declaração (`function f() { }` vs `f() { }`), `local`, `return`, parâmetros (`$1`, `$@`, `$#`)
  - `setopt` / `unsetopt` / `setopt | grep <name>`
  - Opts essenciais: `AUTO_CD`, `EXTENDED_GLOB`, `INTERACTIVE_COMMENTS`, `NO_BEEP`, `CORRECT`, `PROMPT_SUBST`
  - Variáveis vs env (`export`, `typeset`, `local`, `readonly`)
  - Onde colocar tudo isso: `~/.zshrc` (interativo) vs `~/.zshenv` (sempre carregado) vs `~/.zprofile` (login)
  - Loading order: `.zshenv` → `.zprofile` (login) → `.zshrc` (interactive) → `.zlogin` (login final)
- **Não cobre:** scripting profundo, control flow (loops/if), traps
- **Verbetes referenciados:** alias, function, setopt, builtin

#### 03 — History do Zsh
- **Slug:** `03 - History do Zsh.md`
- **Primárias:**
  - [Zsh manual — Options (HIST_*)](https://zsh.sourceforge.io/Doc/Release/Options.html#History)
  - [Zsh manual — History command (fc)](https://zsh.sourceforge.io/Doc/Release/Shell-Builtin-Commands.html#index-fc)
  - [Zsh manual — Expansion (! history references)](https://zsh.sourceforge.io/Doc/Release/Expansion.html#History-Expansion)
- **Secundárias:**
  - [Marcelo Canina — Zsh history setup](https://marcelocanina.com/zsh-history-setup/) (exemplo canônico, validar antes de citar)
  - [Atuin docs](https://docs.atuin.sh/) (alternativa de sync, mencionar em "Veja também")
- **Cobre:**
  - `HISTFILE` (default + override), `HISTSIZE` (memória) vs `SAVEHIST` (disco)
  - Opts essenciais: `SHARE_HISTORY`, `EXTENDED_HISTORY` (com timestamp), `HIST_IGNORE_ALL_DUPS`, `HIST_VERIFY`, `HIST_REDUCE_BLANKS`, `HIST_IGNORE_SPACE`, `INC_APPEND_HISTORY`
  - Setup recomendado (block padrão pra `~/.zshrc`)
  - `history` builtin vs `fc` (fix command) — `fc -l`, `fc -e`, `fc -ln`
  - Search incremental (`Ctrl-R`, `Ctrl-S` se liberado), substring search via plugin
  - History expansion: `!!`, `!$`, `!^`, `!*`, `!:n`, `^x^y^`
- **Não cobre:** atuin/mcfly em profundidade (galho 6 — CLI Utils)
- **Verbetes referenciados:** history, fc

#### 04 — Oh-My-Zsh — anatomia e plugins essenciais
- **Slug:** `04 - Oh-My-Zsh — anatomia e plugins essenciais.md`
- **Primárias:**
  - [Oh-My-Zsh wiki](https://github.com/ohmyzsh/ohmyzsh/wiki)
  - [OMZ plugin list](https://github.com/ohmyzsh/ohmyzsh/wiki/Plugins)
  - [OMZ FAQ](https://github.com/ohmyzsh/ohmyzsh/wiki/FAQ)
- **Secundárias:**
  - [awesome-zsh-plugins](https://github.com/unixorn/awesome-zsh-plugins)
  - [zsh-users (autosuggestions, syntax-highlighting, completions)](https://github.com/zsh-users)
  - [zdharma-continuum (fast-syntax-highlighting)](https://github.com/zdharma-continuum/fast-syntax-highlighting)
  - [marlonrichert/zsh-autocomplete](https://github.com/marlonrichert/zsh-autocomplete)
- **Cobre:**
  - Layout de `~/.oh-my-zsh/`: `oh-my-zsh.sh`, `lib/`, `plugins/`, `themes/`, `custom/`, `cache/`
  - `oh-my-zsh.sh` — o loader (ordem de carregamento, autoload de funções, compinit)
  - `plugins=(...)` array — como funciona (auto-source de `plugins/<name>/<name>.plugin.zsh`)
  - Plugins essenciais demonstrados: `git` (aliases + branch info), `zsh-autosuggestions` (sugestões inline cinza), `zsh-syntax-highlighting` (cores em tempo real), `direnv` (env por pasta)
  - Plugins debatíveis: `fzf-tab` (alternativa moderna ao completion-tradicional), `zsh-autocomplete` (sobreposição agressiva)
  - Update mode: `zstyle ':omz:update' mode reminder|auto|disabled`
  - Pitfalls: double-load de plugins ("syntax-highlighting" + "fast-syntax-highlighting" carregados simultaneamente), ordem importa (syntax-highlight DEVE ser o último), `DISABLE_MAGIC_FUNCTIONS=true` quando paste de URLs quebra
- **Não cobre:** customizar/escrever plugin próprio (10), themes (10), P10k em detalhe (05)
- **Verbetes referenciados:** Oh-My-Zsh, Plugin (OMZ), zsh-autosuggestions, zsh-syntax-highlighting

### Fase Adepto (4 notas — ordem A: Consumer → infra)

#### 05 — Powerlevel10k
- **Slug:** `05 - Powerlevel10k.md`
- **Primárias:**
  - [Powerlevel10k repo + README](https://github.com/romkatv/powerlevel10k)
  - [P10k configure wizard docs](https://github.com/romkatv/powerlevel10k#configuration)
  - [P10k presets](https://github.com/romkatv/powerlevel10k#extra-icons)
- **Secundárias:**
  - [gh issue thread sobre P10k congelado / status do projeto](https://github.com/romkatv/powerlevel10k/discussions) — confirmar fonte específica antes de citar
  - [Starship](https://starship.rs/) (alternativa cross-shell)
  - [Pure prompt](https://github.com/sindresorhus/pure)
- **Cobre:**
  - Instalação canônica: clone em `~/powerlevel10k`, source no `.zshrc` (caminho usado pelo usuário)
  - Instant prompt — o que é, valores (`off`/`quiet`/`verbose`), trade-off (perf × visibilidade)
  - `p10k configure` wizard — fluxo (charset, style, time, separators, heads, tails, etc.)
  - Estrutura de `~/.p10k.zsh` — wizard output, comentários por seção, header indica preset base
  - Modos visuais: rainbow (background colorido), lean (minimalista), classic, pure-style
  - Segmentos left/right — `POWERLEVEL9K_LEFT_PROMPT_ELEMENTS`, `POWERLEVEL9K_RIGHT_PROMPT_ELEMENTS`
  - Customizando segmentos: cores (`POWERLEVEL9K_<SEG>_BACKGROUND/FOREGROUND`), visibilidade condicional
  - Transient prompt: `POWERLEVEL9K_TRANSIENT_PROMPT` (off/always/same-dir/quiet)
  - Nerdfont — instalar Meslo NF (recomendado P10k), configurar terminal
  - Troubleshooting: prompt lento → `p10k diagnose`, `POWERLEVEL9K_INSTANT_PROMPT=verbose`
- **Não cobre:** escrever theme do zero (10), prompt protocols (PS1/PROMPT no Zsh) em profundidade
- **Armadilhas inclui:**
  - **P10k congelado em 2024-07** (Roman Perepelitsa saiu da Google, mantém via voluntários apenas para fixes críticos). Plugin segue funcional e maduro; risco é não evoluir. Considerar starship/pure se você quer projeto em evolução ativa.
  - Setup do usuário desabilita instant prompt (`typeset -g POWERLEVEL9K_INSTANT_PROMPT=off` no início) — pattern comum quando há output durante init, mas tira ganho de UX
- **Verbetes referenciados:** Powerlevel10k, prompt, instant prompt, transient prompt, nerdfont

#### 06 — Keybindings práticos
- **Slug:** `06 - Keybindings práticos.md`
- **Primárias:**
  - [Zsh manual — Zle (key bindings)](https://zsh.sourceforge.io/Doc/Release/Zsh-Line-Editor.html)
  - [Zsh manual — bindkey builtin](https://zsh.sourceforge.io/Doc/Release/Zsh-Line-Editor.html#index-bindkey)
- **Secundárias:**
  - [zsh-users/zsh-history-substring-search](https://github.com/zsh-users/zsh-history-substring-search)
  - [Stack overflow — fix Home/End in Zsh](https://stackoverflow.com/questions/8638012) (canonical Q&A; validar e citar fonte)
- **Cobre:**
  - `bindkey` — listar, definir, remover (`bindkey`, `bindkey '<seq>' <widget>`, `bindkey -r '<seq>'`)
  - Modo emacs (`bindkey -e`, default na maioria das distros) vs modo vi (`bindkey -v`)
  - Keymaps por modo: `main`, `viins`, `vicmd`, `emacs`, `command`
  - Descobrir código de tecla: `cat -v` (digite, veja escape sequence), `Ctrl-V` no Zsh, ou `bindkey` lista atual
  - Setup comum: fix de Home/End (`bindkey '^[[H' beginning-of-line`, `bindkey '^[[F' end-of-line`) — bindings que o usuário já tem
  - Ctrl-Arrows, Alt-Arrows, Ctrl-Backspace, Ctrl-Delete (varia por terminal — passos pra descobrir)
  - Bindings úteis: history-substring-search-up/down, sudo-toggle (plugin sudo), edit-command-line
- **Não cobre:** criar widget custom (07), ZLE como sistema (07), vi-mode profundo (07)
- **Verbetes referenciados:** bindkey, keymap (sub-definição Zsh ZLE no verbete expandido), widget

#### 07 — ZLE
- **Slug:** `07 - ZLE.md`
- **Primárias:**
  - [Zsh manual — Zsh Line Editor (completo)](https://zsh.sourceforge.io/Doc/Release/Zsh-Line-Editor.html)
  - [Zsh manual — Widgets](https://zsh.sourceforge.io/Doc/Release/Zsh-Line-Editor.html#Widgets)
- **Secundárias:**
  - [softmoth/zsh-vim-mode](https://github.com/softmoth/zsh-vim-mode)
  - [Functional Zsh — escrevendo widgets (Wiki não-oficial)](https://wiki.archlinux.org/title/zsh#Key_bindings) — validar antes
- **Cobre:**
  - O que é ZLE: editor de linha do Zsh — interpreta input → muda buffer → dispatch
  - Modelo: input → key → widget → action no buffer
  - Widgets builtin (categorias): inserção (`self-insert`), movimentação (`beginning-of-line`), edição (`backward-delete-char`), history (`up-history`, `history-incremental-search-backward`), aceitação (`accept-line`)
  - `BUFFER`, `CURSOR`, `LBUFFER`, `RBUFFER` — variáveis dentro de widget
  - Criar widget custom: função em Zsh + `zle -N <widget-name>` + `bindkey '<seq>' <widget-name>`
  - Exemplo concreto: `expand-or-complete-with-dots` (mostra "..." enquanto completion processa)
  - Exemplo concreto: widget que escapa output ao Esc (vi-mode advanced)
  - Hooks ZLE: `zle-line-init`, `zle-keymap-select`, `zle-line-finish`
  - Integração com bindkey + relação com nota 06
- **Não cobre:** completion system (08), prompt rendering (05)
- **Verbetes referenciados:** ZLE, widget

#### 08 — Completion system (compsys)
- **Slug:** `08 - Completion system (compsys).md`
- **Primárias:**
  - [Zsh manual — Completion System](https://zsh.sourceforge.io/Doc/Release/Completion-System.html)
  - [Zsh manual — Completion Widgets](https://zsh.sourceforge.io/Doc/Release/Completion-Widgets.html)
  - [Zsh manual — compinit](https://zsh.sourceforge.io/Doc/Release/Completion-System.html#Initialization)
- **Secundárias:**
  - [Zsh completion how-to (autor canônico)](https://zsh.sourceforge.io/Guide/zshguide06.html)
  - [Aloxaf/fzf-tab](https://github.com/Aloxaf/fzf-tab)
  - [marlonrichert/zsh-autocomplete](https://github.com/marlonrichert/zsh-autocomplete) (referência sobre conflitos)
- **Cobre:**
  - Modelo: compsys = sistema de completion programável do Zsh, baseado em widgets de completion
  - `compinit` — inicializa o sistema, lê `fpath`, processa funções `_<comando>`, gera `~/.zcompdump`
  - `compdef <function> <command>` — registra função de completion pra um comando
  - `fpath` — onde Zsh procura funções de completion (`$ZSH/plugins/*/`, `$ZSH/completions/`, custom)
  - Como Zsh decide o que completar: parse do command-line, lookup em `fpath`, fallback pra `_default`
  - `zstyle` essenciais:
    - `zstyle ':completion:*' matcher-list 'm:{a-z}={A-Za-z}'` (case-insensitive)
    - `zstyle ':completion:*' menu select` (navegação interativa)
    - `zstyle ':completion:*' format 'Completing %d'`
    - `zstyle ':completion:*' group-name ''`
  - Troubleshooting: `compaudit` (audit de permissões dos `fpath` dirs), rebuild de `.zcompdump` (`rm ~/.zcompdump*; compinit`), `zsh -i -c exit` benchmark
  - Conflitos comuns: `zsh-autocomplete` (sobrepõe completion-on-tab com completion-as-you-type — incompatível com workflow OMZ tradicional), `fzf-tab` (substitui menu de completion por fzf — compatível mas precisa source antes de syntax-highlight)
- **Não cobre:** escrever função `_<comando>` complexa do zero (mostrar exemplo simples; profundidade fica como link pra Zsh completion how-to)
- **Armadilhas inclui:**
  - **`.zcompdump` corrompido** após mudança de plugins → rebuild manual
  - **fpath ordem importa** — plugin com `_<comando>` vence o que carregou depois
  - **`compaudit` reclamando de permissões** → fix com `chmod g-w` nas pastas suspeitas
  - **`compinit` lento na inicialização** → `compinit -C` (skip security check) em troca de velocidade
- **Verbetes referenciados:** compsys, compinit, compdef, fpath, zstyle

### Fase Magus (2 notas)

#### 09 — Globbing avançado e parameter expansion
- **Slug:** `09 - Globbing avançado e parameter expansion.md`
- **Primárias:**
  - [Zsh manual — Expansion (completo)](https://zsh.sourceforge.io/Doc/Release/Expansion.html)
  - [Zsh manual — Filename Generation (globbing)](https://zsh.sourceforge.io/Doc/Release/Expansion.html#Filename-Generation)
  - [Zsh manual — Parameter Expansion](https://zsh.sourceforge.io/Doc/Release/Expansion.html#Parameter-Expansion)
- **Secundárias:**
  - [Bash to Z Shell, cap. Expansion (livro)](https://www.amazon.com/Bash-Shell-Cross-Reference-Guide/dp/1590593766)
  - [Awesome Zsh — exemplos de glob](https://github.com/unixorn/awesome-zsh-plugins)
- **Cobre (globbing):**
  - Setup: `setopt EXTENDED_GLOB` (necessário pra muito do conteúdo)
  - Patterns essenciais: `*`, `?`, `[abc]`, `[a-z]`, `[^abc]`, `**` (recursive), `**/`
  - Extended glob:
    - `^pattern` — negação (`*^.bak` = tudo que não termina em .bak)
    - `~pattern` — exclusão (`*~*.bak`)
    - `(p1|p2)` — alternation
    - `pattern#` — zero ou mais
    - `pattern##` — um ou mais
  - Glob qualifiers `(...)`:
    - `(.)` — arquivos regulares
    - `(/)` — diretórios
    - `(@)` — symlinks
    - `(*)` — executáveis
    - `(N)` — null glob (sem match retorna vazio, não erro)
    - `(L+N)` — size > N (em bytes; `Lk`/`Lm`/`Lg`)
    - `(mh-N)` — modificado nas últimas N horas
    - `(om[N,M])` — ordenar por mtime, pegar índices N a M
    - `(.U)` — owned by you
  - Exemplos reais: `rm **/*.log(.om[1,5])` (5 logs mais antigos), `print -l **/*.ts(N)` (TS files, no error)
- **Cobre (parameter expansion):**
  - Básicas (compatíveis Bash): `${var:-default}`, `${var:+alt}`, `${var:=default}`, `${var:?error}`
  - Substring: `${var:offset:length}` (Zsh tem `${var[start,end]}` 1-indexed também)
  - Match/replace: `${var#prefix}`, `${var%suffix}`, `${var//pat/repl}`, `${var/#pat/repl}` (only at start)
  - Length: `${#var}`, `${#array}`
  - Zsh-specific flags `${(<flags>)var}`:
    - `(L)` — lowercase, `(U)` — uppercase, `(C)` — capitalize
    - `(s:sep:)` — split por separador (em array)
    - `(j:sep:)` — join array com separador
    - `(@)` — preservar como array
    - `(P)` — indireção (nome de variável → conteúdo)
    - `(k)` — keys de hash, `(v)` — values
  - Subscript em arrays: `${array[1,3]}` (slice), `${array[(I)pattern]}` (match)
  - Combinações úteis: `${${(s/./)hostname}[1]}` (split por ponto, pega primeiro)
- **Não cobre:** brace expansion (`{a,b,c}`, casual), command substitution (`$(cmd)`), arithmetic expansion (`$((expr))`)
- **Verbetes referenciados:** globbing, extended glob, glob qualifier, parameter expansion

#### 10 — Plugins, themes e custom no OMZ
- **Slug:** `10 - Plugins, themes e custom no OMZ.md`
- **Primárias:**
  - [Oh-My-Zsh — custom plugins](https://github.com/ohmyzsh/ohmyzsh/wiki/Customization#overriding-and-adding-plugins)
  - [Oh-My-Zsh — custom themes](https://github.com/ohmyzsh/ohmyzsh/wiki/Customization#overriding-and-adding-themes)
  - [OMZ plugin structure guide](https://github.com/ohmyzsh/ohmyzsh/wiki/Plugins#what-makes-a-plugin)
- **Secundárias:**
  - [Marcelo Canina — exemplo de plugin OMZ](https://marcelocanina.com/your-own-zsh-plugin/) (validar; canônico no estilo)
  - [Zsh manual — Prompt Expansion (PS1/PROMPT)](https://zsh.sourceforge.io/Doc/Release/Prompt-Expansion.html)
- **Cobre (plugin custom):**
  - Estrutura: `~/.oh-my-zsh/custom/plugins/<nome>/<nome>.plugin.zsh`
  - Naming convention: nome do diretório = nome do plugin = nome do arquivo `.plugin.zsh`
  - O que vai dentro: aliases, functions, completion (`_<command>` em `_<nome>` ou pasta `completions/`)
  - Auto-source: basta adicionar `<nome>` ao array `plugins=(...)` no `.zshrc`
  - Convenção pra completion: arquivo `_<nome>` (underscore prefix) na pasta do plugin
  - Exemplo completo: plugin `notify` com 2 functions (`notify-waiting`, `notify-completed`) baseado no padrão Zellij integrations
- **Cobre (theme custom):**
  - Estrutura: `~/.oh-my-zsh/custom/themes/<nome>.zsh-theme`
  - Variáveis chave: `PROMPT` (left), `RPROMPT` (right), `PS2` (continuation)
  - Color codes: `%F{color}...%f`, `%K{color}...%k`, `%B...%b` (bold), `%U...%u` (underline)
  - Prompt expansion: `%n` (user), `%m` (host), `%~` (cwd contraído), `%#` (root/user marker)
  - Git info via VCS_INFO ou plugin `git`
  - Exemplo: theme minimalista de 5 linhas (uma linha PROMPT colorida)
  - Por que P10k é prompt e não theme tradicional: P10k é theme externo (não fica em `themes/`) com lifecycle próprio (instant prompt, segments, etc.)
- **Cobre (publicação):**
  - Custom local (`custom/`) vs plugin no repo OMZ (PR upstream) vs repo próprio com instruções
  - Plugin managers que entendem repos externos: zinit, antibody, zplug (sem entrar em detalhe)
- **Não cobre:** transformar custom em PR no OMZ, plugin managers em profundidade (Dotfiles galho)
- **Verbetes referenciados:** Plugin (OMZ), Theme (custom OMZ)

## 6. Padrão estrutural por nota

Frontmatter:

```yaml
---
title: "<título sem prefixo numérico>"
type: concept
publish: true
fase: iniciado    # iniciado | adepto | magus
tags: [terminal, shell, zsh, <fase>, <conceito>]
created: 2026-05-19
updated: 2026-05-19
status: seedling
---
```

Estrutura do corpo:

```markdown
# <Título>

> [!abstract] TL;DR
> 2-4 linhas. Conceito + regra prática + por que importa.

## O que é / Como funciona

## Na prática
<exemplos concretos: configs do .zshrc, comandos, output esperado>

## Armadilhas
<2+ armadilhas reais>

## Em inglês
<5-10 termos PT → EN com curto exemplo de uso em frase técnica>

## Veja também
<wikilinks pra outras notas do galho + tronco + dicionário>

## Referências
<URLs das fontes primárias e secundárias da nota>
```

**Variações permitidas:**
- Nota 05 (P10k) pode usar sub-headers em "O que é / Como funciona" (Instant prompt, Wizard, Segmentos, Estilos)
- Notas 08 (compsys) e 09 (globbing+expansion) podem usar sub-headers em "Na prática" pra blocos densos
- MOC do galho tem estrutura própria (seção 5)

**Tamanho típico:** 200-400 linhas por nota Iniciado/Magus, 300-500 por nota Adepto. Notas 08 e 09 podem chegar a 600 — aceitar; partir só se uma sub-seção ficar autônoma o suficiente pra virar nota independente.

## 7. Dicionário e verbetes

### Localização e estrutura

**Caminho:** `03-Dominios/Tecnologia/Terminal/Dicionário do Terminal.md` (já existe; criado no galho 1).

**Estrutura:** verbetes organizados por bloco temático. Cada verbete é `### <Termo>` dentro de um `## <Bloco>`. Verbetes em ordem alfabética dentro de cada bloco. Inserção do bloco novo "Shell / Zsh / OMZ" **após** o último bloco atual ("Avançado"), preservando estabilidade dos verbetes já linkados.

### Verbetes novos (≥30)

| Bloco temático | Verbete |
|---|---|
| **Shell / Zsh / OMZ** | Alias |
| | Bindkey |
| | Builtin |
| | Compdef |
| | Compinit |
| | Compsys |
| | Extended glob |
| | fc |
| | Fpath |
| | Function (shell) |
| | Glob qualifier |
| | Globbing |
| | History |
| | Instant prompt |
| | Nerdfont |
| | Oh-My-Zsh |
| | Parameter expansion |
| | Plugin (OMZ) |
| | Powerlevel10k |
| | POSIX |
| | Prompt |
| | Setopt |
| | Shell |
| | Theme (custom OMZ) |
| | Transient prompt |
| | Widget |
| | ZLE |
| | Zsh-autosuggestions |
| | Zsh-syntax-highlighting |
| | Zstyle |

### Verbetes expandidos

| Verbete existente | Como expandir |
|---|---|
| **Keymap** | Estrutura em 2 sub-sessões dentro do verbete: "Em Neovim" (definição atual sobre `vim.keymap.set`) e "Em Zsh (ZLE)" (definição nova sobre `bindkey` + keymap names: `main`, `viins`, `vicmd`, `emacs`). Wikilink continua funcionando — `[[Dicionário do Terminal#Keymap]]` resolve. |

### Verbetes Plugin no dicionário

O dicionário atual tem dois verbetes LazyVim-flavored: **Plugin manager** (lazy.nvim) e **Plugin spec** (estrutura de declaração no `lazy.nvim`). Não há verbete genérico "Plugin".

Decisão: **criar verbete novo "Plugin (OMZ)"** standalone na lista do bloco "Shell / Zsh / OMZ", sem mexer nos verbetes LazyVim. Cobre:
- Estrutura: pasta `~/.oh-my-zsh/plugins/<nome>/<nome>.plugin.zsh` (embarcado) ou `~/.oh-my-zsh/custom/plugins/<nome>/...` (custom local)
- Loading: array `plugins=(...)` no `.zshrc`
- Distinção: embarcado vs custom vs externo (gerenciado por outro tool como zinit)

### Workflow durante a escrita

1. Cada vez que uma nota usa um termo jargão Shell/Zsh/OMZ, linka como `[[Dicionário do Terminal#<Termo>|<texto>]]`.
2. Termo sem verbete → criar na hora (usar skill `/verbete` ou edição manual no bloco novo).
3. Verbete sempre referencia, em "Veja também" do próprio verbete, a(s) nota(s) que aprofundam.
4. Manter ordem alfabética dentro do bloco "Shell / Zsh / OMZ".
5. Spec lista, por nota (seção 5), **quais verbetes referencia** — ajuda a manter cobertura.

## 8. Versões assumidas

| Componente | Versão | Política |
|---|---|---|
| **Zsh** | 5.9+ | Notas mencionam features 5.9+ quando relevante; comportamentos de 5.7/5.8 mencionados se diferentes. |
| **Oh-My-Zsh** | `master` em ~maio/2026 (commit aproximado gravado no MOC do galho na execução) | OMZ evolui, estrutura macro estável. Revisão pontual quando plugin core mudar; não rewrite. |
| **Powerlevel10k** | `master` 2024-07 (último release; projeto congelado) | Plugin segue funcional e maduro. Nota 05 menciona o status explicitamente. |
| **Plugins externos** (zsh-autosuggestions, zsh-syntax-highlighting, zsh-autocomplete, fast-syntax-highlighting, fzf-tab, direnv) | `master` em 2026-05-19 (versão declarada só se ponto fundamental depender) | |

Setup do usuário usado como referência:
- P10k instalado via `git clone` em `~/powerlevel10k/` (não dentro de OMZ themes)
- Estilo P10k: rainbow + powerline, 2 linhas, nerdfont-v3, angled separators, sharp heads, instant_prompt configurado como `off` no `.zshrc` do usuário (pattern documentado quando há init output)

## 9. Fontes globais

Referências usadas em múltiplas notas (não repetir nas notas individuais; linkar pelo dicionário ou pela bibliografia desta seção):

- **Zsh manual (completo):** https://zsh.sourceforge.io/Doc/Release/
- **Zsh FAQ:** https://zsh.sourceforge.io/FAQ/
- **A User's Guide to the Z-Shell (Peter Stephenson):** https://zsh.sourceforge.io/Guide/zshguide.html
- **Oh-My-Zsh wiki:** https://github.com/ohmyzsh/ohmyzsh/wiki
- **Powerlevel10k repo + README:** https://github.com/romkatv/powerlevel10k
- **awesome-zsh-plugins:** https://github.com/unixorn/awesome-zsh-plugins
- **zsh-users (org canônica de plugins):** https://github.com/zsh-users
- **From Bash to Z Shell** (livro Kiddle/Peek/Stephenson, 2004 — datado mas referência clássica)
- **/r/zsh:** https://www.reddit.com/r/zsh/

## 10. Decisões editoriais

- **Idioma:** PT-BR. Termos técnicos em inglês mantidos (shell, prompt, widget, completion, glob, plugin, theme).
- **Enquadramento:** domínio pessoal — sem seção "Em entrevista", sem rota de entrevista no MOC. Cada nota tem seção "Em inglês" (mini-glossário PT→EN dos termos-chave) pra fluência em discussões técnicas.
- **Tom:** pessoal natural — "no seu `.zshrc`", "você tem `git, zsh-autosuggestions, …` carregados" — mas sem fabricação. Cita apenas o que está no config real do usuário.
- **Paths em samples públicos:** generalizar `/home/josenaldo/...` → `~/...`. Aliases/funcs específicos do workflow do usuário (codemed, notify-waiting/completed) ficam como exemplo opcional ou anônimo, nunca repo-específico.
- **Caminho primário:** OMZ master + P10k 2024-07 instalado via git em `~/powerlevel10k/`. Zsh 5.9 (Ubuntu/Linux). Notas declaram isso no MOC do galho.
- **Conflitos reais:** "Armadilhas" das notas 04, 06, 08 mencionam casos reais (double-load `fast-syntax-highlighting` + `zsh-syntax-highlighting`, `zsh-autocomplete` vs OMZ completion, NVM duplicado em `.zshenv`+`.zshrc`). Apresentado como pattern comum, não auditoria pessoal explícita.
- **Plugins demonstrados em 04:** git, zsh-autosuggestions, zsh-syntax-highlighting (canônica), direnv. Plugins debatíveis (fzf-tab, zsh-autocomplete) citados com tradeoffs.
- **Em inglês:** mantém. 5-10 termos PT→EN com frase técnica curta — útil pra PR review e docs em inglês.
- **Code samples:** comandos Zsh executáveis (não pseudocódigo). Snippets de config = trechos diretos de `~/.zshrc`/`~/.p10k.zsh` (real ou plausível), comentados em PT. Cada sample testado localmente antes do close.
- **Wikilinks:** densos: nota → outras notas do galho + verbetes do dicionário + tronco.
- **Sem fabricação:** zero "no meu projeto X eu uso", zero "uma vez tive um bug Y". Hipotéticos explícitos ("um exemplo comum", "considere o caso onde…").
- **Ordem de implementação:** por fase (Iniciado → Adepto → Magus), sequencial 01→10.
- **OMZ + P10k primários:** o caminho real do usuário. Iniciado/Adepto demonstram coisas com esse stack ligado. Zsh puro aparece quando o conceito é universal (history, setopt, expansion) e domina em Magus.

## 11. Rotas alternativas no MOC

Além da sequência 01→10, o MOC oferece 3 rotas curtas pra entradas focadas:

| Rota | Sequência | Para quem |
|---|---|---|
| **Daily-driver enxuto** *(toda Iniciado)* | 01 → 02 → 03 → 04 | "Quero usar Zsh + OMZ como shell primário esta semana sem customizar nada." |
| **Customização visual** | 04 → 05 → 10 | "OMZ funciona. Agora quero meu prompt + plugins próprios." Pula ZLE/compsys — leitor não precisa entender o motor pra customizar visual. |
| **Domínio do motor** | 02 → 06 → 07 → 08 → 09 | "Já uso bem; quero entender Zsh por dentro." Foco em opts, keys, ZLE, compsys, expansion. |

## 12. Critérios de aprovação

O galho está pronto quando:

1. **11 arquivos** existem em `03-Dominios/Tecnologia/Terminal/Shell/`: 10 notas atômicas + 1 MOC do galho.
2. **Dicionário do Terminal** ganha **≥30 verbetes novos** no bloco "Shell / Zsh / OMZ"; verbete "Keymap" expandido com sub-sessões Neovim/Zsh sem quebrar wikilinks existentes; verbete novo "Plugin (OMZ)" criado standalone.
3. **Todos os arquivos** com `publish: true`, `fase` declarada (notas) ou `type: moc` (MOC), tags consistentes (`terminal`, `shell`, `zsh`, `<fase>`).
4. **MOC do galho** tem:
   - TL;DR em `[!abstract]`
   - Seções `## Iniciado` / `## Adepto` / `## Magus` agrupando as 10 notas em ordem
   - Seção `## Rotas alternativas` com as 3 rotas
   - Seção `## Versões assumidas` declarando Zsh/OMZ/P10k
   - "Veja também" com wikilinks pro tronco Terminal e pro Dicionário
5. **Cada nota satisfaz a rubrica:**
   - TL;DR em `[!abstract]`
   - 2+ wikilinks pra outras notas do galho + 1+ pro tronco ou MOC do galho
   - 2+ exemplos práticos concretos (config, comando, output esperado)
   - Seção "Em inglês" com 5-10 termos PT→EN + 1 frase de uso por termo
   - Seção "Armadilhas" com 2+ casos concretos (não genéricos)
   - Wikilinks pros verbetes apropriados do dicionário (lista no spec, seção 5)
   - Frontmatter completo (`publish: true`, `status: seedling`, `fase`, tags)
   - PT-BR natural; termos técnicos em inglês mantidos
   - Paths generalizados (`~/...`, sem `/home/josenaldo/...`)
   - **Zero atribuição de experiência pessoal fabricada** ao autor
6. **Tronco** `03-Dominios/Tecnologia/Terminal/index.md` atualizado: bullet do Shell vira wikilink ativo `[[03-Dominios/Tecnologia/Terminal/Shell/index|Shell]]`.
7. **Quartz publica** corretamente em josenaldo.github.io (rodar build local antes do close).
8. **Pelo menos 4 notas** com config/comando testado localmente (rodar snippet no shell e validar output esperado).
9. **`verificar-wikilinks`** passa em `03-Dominios/Tecnologia/Terminal/Shell/` sem broken links.
10. **Commits sem `Co-Authored-By: Claude`**, sem `--no-verify`.

## 13. Riscos e mitigações

| Risco | Mitigação |
|---|---|
| **OMZ evolui** — plugin core renomeia, default muda | Declarar commit aproximado no MOC. Revisão pontual quando ponto fundamental mudar (não rewrite). |
| **P10k congelado em 2024** — Roman saiu da Google, projeto sem updates ativos | Nota 05 menciona explicitamente em "Armadilhas" + "Veja também" lista alternativas (starship, pure, oh-my-posh) sem virar comparativo. Plugin segue funcional. |
| **`zsh-autocomplete` vs OMZ completion** — conflito notório | Nota 04 (OMZ) avisa do plugin; nota 08 (compsys) tem armadilha dedicada explicando o conflito e quando escolher cada um. |
| **`fast-syntax-highlighting` vs `zsh-syntax-highlighting`** — não devem coexistir | Armadilha explícita em nota 04 — apresentar como pattern comum, recomendar escolher um. |
| **Compsys denso demais pra 1 nota** | Sub-seções claras ("Como Zsh decide o que completar", "compinit + zcompdump", "zstyle essenciais", "Troubleshooting"). Aceitar 500-600 linhas. Não dividir — completion é uma coisa só. |
| **ZLE × bindkey overlap** com nota 06 (Keys) | Regra dura: nota 06 é operacional (bindar teclas, fixar Home/End, modo emacs/vi). Nota 07 é o motor (widgets, criar widget custom, integrar com bindkey). Cross-link forte mas zero duplicação de conteúdo. |
| **Globbing + parameter expansion como nota única** (09) | Densa por design (Magus). Sub-seções claras: "Globbing essencial", "Extended glob", "Qualifiers", "Parameter expansion", "Flags `(L)/(U)/(s:x:)`". Aceitar 500-600 linhas; partir só se uma sub-seção virar autônoma. |
| **Sample copiando `.zshrc` real expõe info pessoal no público** | Generalizar paths (`~/...`), generalizar aliases específicos do workflow, manter só plugin list pública (já é mainstream). |
| **Verbete "Keymap" ambíguo** entre Neovim e Zsh | Verbete expandido com sub-sessões claras "Em Neovim" e "Em Zsh (ZLE)". Verbete "Plugin (OMZ)" criado standalone — verbetes LazyVim ("Plugin manager", "Plugin spec") não tocados. |
| **Quartz publish quebra** — frontmatter inválido, wikilink quebrado | Build local do Quartz como passo do critério #7. `verificar-wikilinks` como critério #9. |
| **Dicionário inchando além do Editor** | OK — é trilha-wide. Bloco "Shell / Zsh / OMZ" novo é inserido depois dos blocos existentes; ordem alfabética dentro do bloco; verbetes existentes não tocados (exceto expansão de Keymap/Plugin). |
| **Conteúdo "tutorial qualquer de Zsh"** | "Armadilhas" tem 2+ casos concretos por nota. "Na prática" tem config/comando real (não pseudocódigo). Trechos do setup do usuário (anonimizados) usados quando relevante. |

## 14. Plano de execução

O plano detalhado de execução vai em `docs/superpowers/plans/2026-05-19-terminal-shell-execution.md` (gerado pela skill `superpowers:writing-plans` após aprovação deste spec).

Ordem de execução recomendada (sumária — detalhe no plano):

1. **Task 0 — Pré-flight:** confirmar branch, status git limpo, deletar `docs/superpowers/specs/PROXIMA-SESSAO-galho-2-shell.md`
2. **Esqueletos:** criar `Shell/index.md` (MOC com placeholder) + adicionar bloco "Shell / Zsh / OMZ" no Dicionário (sem verbetes ainda)
3. **Fase Iniciado:** notas 01 → 02 → 03 → 04 (verbetes criados conforme aparecem; verbete novo "Plugin (OMZ)" criado quando 04 chegar)
4. **Fase Adepto:** notas 05 → 06 → 07 → 08 (verbete "Keymap" expandido quando 06 chegar)
5. **Fase Magus:** notas 09 → 10
6. **Pass final no MOC:** todos os wikilinks ativos, "Versões assumidas" preenchida com commits/datas concretas
7. **Pass final no Dicionário:** ordenação alfabética dentro do bloco "Shell / Zsh / OMZ" + "Veja também" por verbete
8. **Atualizar tronco** `Terminal/index.md` ativando wikilink do Shell com descrição
9. **Validação:** `verificar-wikilinks` em `Shell/` + build local Quartz
10. **Commit final** do galho (ou commits por nota — decisão no plano)

Execução com `superpowers:subagent-driven-development`. **Sequential** (dicionário é estado compartilhado entre notas). Cada nota: implementer Sonnet → spot-check pelo controller → commit individual.

## 15. Documentos relacionados

- `2026-05-18-trilha-terminal-design.md` — roadmap macro da trilha (este spec é galho #2)
- `2026-05-19-terminal-editor-design.md` — spec do galho 1, formato e rubrica de referência
- `2026-05-19-terminal-editor-execution.md` — plano de execução do galho 1 (~21 tasks, proven)
- Plano de execução (criado a seguir): `2026-05-19-terminal-shell-execution.md`
- Tronco: `03-Dominios/Tecnologia/Terminal/index.md`
- Dicionário a expandir: `03-Dominios/Tecnologia/Terminal/Dicionário do Terminal.md`
- Pasta a criar: `03-Dominios/Tecnologia/Terminal/Shell/`
