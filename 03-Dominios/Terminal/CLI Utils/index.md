---
title: "CLI Utils"
type: moc
publish: true
created: 2026-05-22
updated: 2026-05-22
status: growing
tags:
  - terminal
  - cli-utils
  - moc
aliases:
  - MOC CLI Utils
  - Galho 6
---
# CLI Utils

> [!abstract] TL;DR
> Galho 6 da trilha Terminal. Ferramentas pequenas e modernas que substituem ou complementam utilitários UNIX clássicos (`cat`, `ls`, `grep`, `find`, `du`, `top`) e elevam o fluxo interativo (`fzf`, `zoxide`, `atuin`) e o processamento de dados (`jq`, `yq`). 13 notas (4 Iniciado + 4 Adepto + 5 Magus), incluindo 2 capstones de composição (stack interativo + pipeline JSON/YAML).

Galho parte do zero (sem assumir uso prévio) até workflows compostos. Iniciado cobre as 4 ferramentas que mais mudam o dia-a-dia. Adepto adiciona produtividade interativa e processamento estruturado. Magus traz capstones de composição e ferramentas operacionais (docs em fluxo, git diff moderno, monitores).

## Conteúdo

### Iniciado

- [[01 - fzf — fuzzy finder universal]]
- [[02 - ripgrep e fd — buscar conteúdo e nomes]]
- [[03 - bat — cat moderno com syntax highlight]]
- [[04 - eza — ls moderno]]

### Adepto

- [[05 - zoxide — cd inteligente com frecency]]
- [[06 - atuin — history shell com SQLite e sync]]
- [[07 - jq — processor JSON com DSL]]
- [[08 - yq — processor YAML e as duas implementações]]

### Magus

- [[09 - tldr e cheat — docs práticas em fluxo]]
- [[10 - delta — pager moderno pra git diff]]
- [[11 - Monitores e disco — btop htop dust]]
- [[12 - Stack interativo — fzf zoxide atuin]]
- [[13 - Pipeline JSON e YAML — jq yq fzf]]

## Mapa de substituições clássicas → modernas

| Clássico | Moderno | Nota |
|---|---|---|
| `cat` | `bat` | [[03 - bat — cat moderno com syntax highlight\|03]] |
| `ls` | `eza` | [[04 - eza — ls moderno\|04]] |
| `grep` | `rg` | [[02 - ripgrep e fd — buscar conteúdo e nomes\|02]] |
| `find` | `fd` | [[02 - ripgrep e fd — buscar conteúdo e nomes\|02]] |
| `cd` (com frecency) | `zoxide` | [[05 - zoxide — cd inteligente com frecency\|05]] |
| `history` / Ctrl-R | `atuin` | [[06 - atuin — history shell com SQLite e sync\|06]] |
| `du` | `dust` | [[11 - Monitores e disco — btop htop dust\|11]] |
| `top` | `btop` / `htop` | [[11 - Monitores e disco — btop htop dust\|11]] |
| `man` (rápido) | `tldr`, `cheat` | [[09 - tldr e cheat — docs práticas em fluxo\|09]] |
| `git diff` / pager | `delta` | [[10 - delta — pager moderno pra git diff\|10]] |

## Rotas alternativas

- **Substituições UNIX mais comuns:** `01` → `02` → `03` → `04`
- **Fluxo interativo moderno:** `01` → `05` → `06` → `12`
- **Processamento estruturado:** `07` → `08` → `13`
- **Git e revisão:** `02` → `10`
- **Observabilidade local:** `11` + tldr (`09`) pra explorar flags rapidamente

## Versões assumidas

Capturadas no pré-flight da execução:

- **fzf:** `<VERSAO_FZF>`
- **ripgrep:** `14.1.0` (sistema de referência: Ubuntu 24.04)
- **fd:** `9.0.0` (binário `fdfind` em Debian/Ubuntu)
- **bat:** `<VERSAO_BAT>` (binário `batcat` em Debian/Ubuntu)
- **eza:** `<VERSAO_EZA>`
- **zoxide:** `<VERSAO_ZOXIDE>`
- **atuin:** `<VERSAO_ATUIN>`
- **jq:** `1.7` (sistema de referência: Ubuntu 24.04)
- **yq:** `<VERSAO_YQ>` (especificar Go ou Python)
- **delta:** `<VERSAO_DELTA>`
- **btop:** `<VERSAO_BTOP>`
- **htop:** `3.3.0` (sistema de referência: Ubuntu 24.04)
- **dust:** `<VERSAO_DUST>`
- **OS de referência:** Ubuntu 24.04.4 LTS

Versões nas notas são hedged ("0.4x+; verifique localmente") pra envelhecer bem.

## Veja também

- [[Dicionário do Terminal]]
- [[03-Dominios/Terminal/index|Trilha Terminal]]
- [[03-Dominios/Terminal/Shell/index|Shell (galho 2)]] — Zsh + integrações pra muitas dessas ferramentas
- [[03-Dominios/Terminal/Dotfiles/index|Dotfiles (galho 5)]] — versionar configs dessas ferramentas
