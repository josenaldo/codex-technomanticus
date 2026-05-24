---
title: "Workflow"
type: moc
publish: true
created: 2026-05-24
updated: 2026-05-24
status: growing
tags:
  - terminal
  - workflow
  - moc
aliases:
  - MOC Workflow
  - Galho 7
---
# Workflow

> [!abstract] TL;DR
> Galho 7 e último da trilha Terminal. 5 playbooks que recombinam ferramentas dos galhos 1-6 + 4 meta-práticas (filosofia keyboard-first, anatomia da sessão, ergonomia, transições de contexto) + 1 capstone sintetizando a trilha inteira em forma de "anatomia de um dia keyboard-first". 10 notas (3 Iniciado + 4 Adepto + 3 Magus).

Este galho NÃO é mais uma ferramenta — é a tese sobre como compor as ferramentas dos galhos 1-6 em fluxos reais de trabalho. As 4 meta-práticas dão o porquê (filosofia, anatomia da sessão, ergonomia, transições de contexto). Os 5 playbooks dão o quê (onboarding, setup matinal, code review, worktrees, refactoring). O capstone dá o como integrado, em forma de cenário cronológico — anatomia de um dia keyboard-first de ponta a ponta.

## Conteúdo

### Iniciado

- [[01 - Filosofia keyboard-first — quando vale e quando não]]
- [[02 - Anatomia da sessão de trabalho]]
- [[03 - Onboarding em projeto novo]]

### Adepto

- [[04 - Setup matinal e tear-down]]
- [[05 - Code review no terminal]]
- [[06 - Ergonomia das mãos]]
- [[07 - Worktrees + Zellij paralelos]]

### Magus

- [[08 - Refactoring multi-arquivo]]
- [[09 - Transições de contexto]]
- [[10 - Sessão ideal — anatomia de um dia keyboard-first]]

## Tools usadas por cada nota

| Nota | Editor (G1) | Shell (G2) | Multiplexer (G3) | TUIs (G4) | Dotfiles (G5) | CLI Utils (G6) |
|------|---|---|---|---|---|---|
| 01 — Filosofia | — | — | — | — | — | — |
| 02 — Anatomia sessão | — | — | Zellij conceitos | — | — | — |
| 03 — Onboarding | nvim+telescope | — | — | lazygit | — | zoxide, eza, rg, bat |
| 04 — Setup matinal | nvim | — | Zellij sessions+layouts | lazygit | configs versionadas | atuin |
| 05 — Code review | nvim | — | Zellij panes | lazygit | — | delta, bat, gh CLI |
| 06 — Ergonomia | nvim keymaps | Zsh keybindings | Zellij keybindings | — | — | — |
| 07 — Worktrees | nvim | — | Zellij named sessions | lazygit | — | — |
| 08 — Refactoring | nvim+quickfix+LSP | — | — | — | — | rg |
| 09 — Transições | — | — | Zellij sessions+focus | — | — | atuin |
| 10 — Capstone | tudo | tudo | tudo | tudo | tudo | tudo |

## Rotas alternativas

- **Mínimo viável (Iniciado primeiro):** `01` → `02` → `03` — entende filosofia, vocabulário, primeiro fluxo concreto.
- **Quer ser produtivo já:** `03` → `04` → `05` — onboarding, setup matinal, code review. Pula meta-prática.
- **Quer entender modelo mental:** `01` → `02` → `06` → `09` — pula playbooks, foca nas 4 meta-práticas.
- **Refactor pesado:** `08` direto (assume Editor + CLI Utils dominados).
- **Capstone:** `10` — só depois de ter lido as 9 anteriores.

## Pré-requisitos

Este galho assume galhos 1-6 dominados. Notas referenciam mas NÃO re-explicam ferramentas:

- Editor (galho 1): nvim, LazyVim, telescope, quickfix, LSP
- Shell (galho 2): zsh, p10k, keybindings, completion
- Multiplexer (galho 3): Zellij sessions, layouts, panes
- TUIs (galho 4): lazygit (operações intermediárias)
- Dotfiles (galho 5): chezmoi/stow (configs versionadas)
- CLI Utils (galho 6): fzf, rg, bat, eza, zoxide, atuin, delta

## Veja também

- [[Dicionário do Terminal]]
- [[03-Dominios/Terminal/index|Trilha Terminal]]
- [[03-Dominios/Terminal/Editor/index|Editor (galho 1)]]
- [[03-Dominios/Terminal/Shell/index|Shell (galho 2)]]
- [[03-Dominios/Terminal/Multiplexer/index|Multiplexer (galho 3)]]
- [[03-Dominios/Terminal/TUIs/index|TUIs de Dev (galho 4)]]
- [[03-Dominios/Terminal/Dotfiles/index|Dotfiles (galho 5)]]
- [[03-Dominios/Terminal/CLI Utils/index|CLI Utils (galho 6)]]
