---
title: "delta — pager moderno pra git diff"
created: 2026-05-22
updated: 2026-05-22
type: concept
progress: backlog
status: seedling
publish: true
fase: Magus
tags:
  - terminal
  - cli-utils
  - magus
  - delta
  - git
aliases:
  - delta
  - git-delta
---

> [!abstract] TL;DR
> delta é pager especializado em git diff/show/log/blame, com syntax highlight (syntect, igual bat), side-by-side opcional, navegação por keys (n/N entre hunks), hyperlinks OSC 8 (terminais modernos), preservação de cores. Configurado no `~/.gitconfig`. Standalone funciona em diff puro também (`diff -u a b | delta`). Ao adotar, o ganho é transformar `git diff` de cinza/preto em revisão visual com syntax highlight e navegação.

## O que é / Como funciona

### Filosofia: pager especializado pra git

delta não é pager genérico — é uma reformatação visual do output de `git diff` (e affins). Engine syntect (mesma do bat) aplica syntax highlight em ~150 linguagens. Recebe diff unified como input, devolve diff reformatado pro terminal.

Compatível com qualquer comando git que produza diff:

- `git diff`
- `git show <hash>`
- `git log -p`
- `git blame`
- `git stash show -p`

Também funciona em diff fora do git: `diff -u a.txt b.txt | delta`.

### Features (todas opcionais, ativadas no config)

- `navigate` — `n` e `N` pulam entre hunks; útil em diff grande
- `side-by-side` — antes/depois lado a lado (precisa terminal largo)
- `line-numbers` — numeração nas duas colunas
- `hyperlinks` — OSC 8 escape sequences viram commits/paths clicáveis em terminais que suportam
- `syntax-theme` — tema syntax (compartilha temas bat, via `bat --list-themes`)
- `features` — preset combinado (decorations agrupa file/hunk headers visuais)
- `dark` / `light` — escolha de tema; sem isso, delta tenta auto-detectar

### Config em gitconfig

```toml
[core]
    pager = delta

[interactive]
    diffFilter = delta --color-only

[delta]
    navigate = true
    light = false
    side-by-side = true
    line-numbers = true
    syntax-theme = Dracula
    hyperlinks = true
    features = decorations

[merge]
    conflictStyle = diff3

[diff]
    colorMoved = default
```

### `[interactive] diffFilter` — afeta `git add -p`

Sem essa key: `git add -p` (patch interativo) usa pager default (cru).
Com essa key: os chunks que aparecem em `git add -p` ficam coloridos pelo delta.

### Modo standalone

```bash
diff -u a.txt b.txt | delta
# Funciona pra qualquer diff unified, fora do git
```

### Hyperlinks OSC 8

Terminais com suporte: kitty, wezterm, recent gnome-terminal (3.40+), recent iTerm. Em terminais sem suporte, hyperlinks viram texto literal `]8;;file://...` — pode ficar feio.

Em delta:

- Commit hashes viram links pra hosting provider (GitHub/GitLab)
- File paths viram links que abrem no editor configurado

## Na prática

### Setup inicial

```bash
# Configurar gitconfig global
git config --global core.pager delta
git config --global interactive.diffFilter "delta --color-only"
git config --global delta.navigate true
git config --global delta.side-by-side true
git config --global delta.line-numbers true
git config --global delta.syntax-theme "Dracula"

# Verificar
git diff HEAD~1
```

### Receitas

```bash
# Diff comum
git diff
git diff HEAD~5

# Show de commit
git show <hash>

# Log com diffs (cuidado com volume)
git log -p --max-count=3

# Standalone (sem git)
diff -u file_a file_b | delta

# Comparar dois branches lado a lado
git diff main..feature -- src/

# Diff em formato específico, encanado pra delta
diff -u /etc/hosts.bak /etc/hosts | delta
```

### Integrar com bat themes

```bash
# Listar themes (engine compartilhada com bat)
bat --list-themes

# Configurar tema escolhido no gitconfig
git config --global delta.syntax-theme "Monokai Extended"
```

Mesmos themes funcionam em bat e delta (port syntect do Sublime grammars).

### Comparação: delta vs alternativas

| Pager | Syntax highlight | Side-by-side | Navegação | Hyperlinks |
|---|---|---|---|---|
| less (default git) | não | não | limitada | não |
| diff-so-fancy | não | não | limitada | não |
| delta | sim | sim | n/N | OSC 8 |

### Versão hedged

delta 0.19+; verifique `delta --version` localmente.

## Armadilhas

### (1) Config errada no gitconfig é silenciosa

**Causa:** typo em `[delta]` section ou key — delta não roda e git cai pra less default, sem mensagem de erro.

**Sintoma:** `git diff` aparece sem syntax (listras vermelhas/verdes só).

**Como detectar:** `git config --get core.pager` mostra `delta`? `delta --version` está instalado?

**Solução:** copiar config do README oficial; testar com `git diff HEAD~1` em repo conhecido. Se falhar, isolar com `git -c core.pager=delta diff` (força delta inline). Validar config YAML/TOML com tool ou eyeballing.

### (2) Side-by-side em terminal estreito

**Causa:** `side-by-side = true` precisa ~180 colunas efetivas; em terminal de 100 colunas, fica cortado.

**Sintoma:** linhas truncadas; pior que single-column em UX.

**Como detectar:** `tput cols` mostra largura atual.

**Solução:** condicional por contexto — só side-by-side em monitor wide. Ou deixar `false` global e ativar caso a caso: `git -c delta.side-by-side=true diff`.

### (3) Hyperlinks OSC 8 viram literal em terminal sem suporte

**Causa:** terminal antigo (gnome-terminal pré-3.40, alacritty antigo, GNU screen) não interpreta sequência OSC 8.

**Sintoma:** vê `]8;;file://...^G` literal no diff.

**Como detectar:** ler diff e ver texto estranho onde deveria ter link clicável.

**Solução:** desativar em terminais sem suporte: `[delta] hyperlinks = false`. Detectar terminal via `$TERM`, `$TERM_PROGRAM`.

### (4) Performance em diff gigante

**Causa:** delta aplica highlight + reformatação por linha; em diff de milhares de linhas, o custo soma.

**Sintoma:** `git log -p` em repo grande lento; `git show` de commit gigante demorado.

**Como detectar:** comparar `git --no-pager log -p` (rápido) vs `git log -p` (lento).

**Solução:** `[delta] max-line-length = 512` (linhas mais longas viram cru); ou usar pager raw temporário: `git --no-pager diff`.

### (5) Conflito com outras configs de pager

**Causa:** `[pager]` section no gitconfig tem entries customizadas (`pager.diff = something`); sobrescrevem `core.pager`.

**Sintoma:** `git diff` usa pager X; `git show` usa pager Y; comportamento inconsistente.

**Como detectar:** `git config --get-all pager.*` lista overrides.

**Solução:** garantir `core.pager = delta` E `[pager] diff = delta, log = delta, show = delta` consistentes. Ou remover overrides específicos.

### (6) `colorMoved` em diff conflita com tema delta

**Causa:** `[diff] colorMoved = zebra` ou `dimmed-zebra` colore linhas movidas com cores próprias que conflitam com tema delta.

**Sintoma:** linhas movidas em cor estranha (ex: magenta sobre azul) — ilegível.

**Como detectar:** diff com refactor (linhas movidas) usando tema escuro mostra cores feias.

**Solução:** ajustar `[delta] map-styles` pra remapear cores conflitantes; ou usar `colorMoved = default` (delta lida bem com o default).

## Em inglês

- **Pager** — *pager*. "delta é o pager especializado pra git diff."
- **Syntax highlight** — *syntax highlighting*. "syntect aplica syntax highlight em ~150 linguagens."
- **Lado a lado** — *side-by-side*. "Side-by-side compara antes/depois em duas colunas."
- **Hyperlink** — *hyperlink*. "Hyperlinks OSC 8 viram links clicáveis em terminais compatíveis."
- **Sequência de escape** — *escape sequence*. "OSC 8 é uma sequência de escape ANSI."
- **Navegação** — *navigation*. "Navegação por n/N entre hunks dispensa scroll manual."
- **Hunk** — *hunk*. "Cada hunk é um bloco contíguo de mudanças no diff."
- **Decoração** — *decoration*. "Features de decoração agrupam headers visuais."
- **Tema** — *theme*. "O tema syntax compartilha grammars com o bat."
- **Detecção de refactor** — *refactor detection*. "`colorMoved` ajuda na detecção de refactor (linhas movidas)."

## Veja também

- [[03 - bat — cat moderno com syntax highlight]] — engine compartilhada (syntect); temas comuns
- [[03-Dominios/Tecnologia/Terminal/TUIs/index|TUIs (galho 4)]] — Lazygit usa delta como pager opcionalmente
- [[03-Dominios/Tecnologia/Terminal/CLI Utils/index|MOC do galho]]
- [[03-Dominios/Tecnologia/Terminal/index|Trilha Terminal]]
- [[Dicionário do Terminal#delta|delta]]
- [[Dicionário do Terminal#OSC 8|OSC 8]]
- [[Dicionário do Terminal#syntax pager|syntax pager]]
- [[Dicionário do Terminal#BAT_THEME|BAT_THEME]]

## Referências

- delta repo: https://github.com/dandavison/delta
- delta doc: https://dandavison.github.io/delta/
