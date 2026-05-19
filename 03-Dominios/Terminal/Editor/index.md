---
title: "Editor"
type: moc
publish: true
created: 2026-05-19
updated: 2026-05-19
status: growing
progresso: andamento
tags:
  - terminal
  - editor
  - moc
  - neovim
  - lazyvim
aliases:
  - Editor
  - Neovim
  - LazyVim
---
# Editor

> [!abstract] TL;DR
> Galho 1 da trilha Terminal. Domínio de Neovim + LazyVim como editor primário, em 3 fases (4 + 5 + 4 = 13 notas): do modal editing à customização avançada com Treesitter, DAP e snippets.

Esse galho cobre o editor end-to-end: filosofia modal, motions e text objects (Iniciado), config em Lua, lazy.nvim, LSP e customização (Adepto), técnicas de produtividade e refactoring assistido por AST (Magus). LazyVim é o caminho primário porque é o setup real operado; Vim/Neovim core aparece quando o conceito é universal.

## Conteúdo

### Iniciado

- [[01 - Modal editing]]
- [[02 - Motions, operadores e text objects]]
- [[03 - Edição e navegação]]
- [[04 - LazyVim tour]]

### Adepto

- [[05 - Lua para Neovim]]
- [[06 - Estrutura de config]]
- [[07 - lazy.nvim]]
- [[08 - Customizando LazyVim]]
- [[09 - LSP no Neovim]]

### Magus

- [[10 - Registers, marks, macros]]
- [[11 - Workflow avançado]]
- [[12 - Treesitter avançado]]
- [[13 - Snippets e DAP]]

## Rotas alternativas

- **Uso diário** (Iniciado completa): `01` → `02` → `03` → `04`
- **Customização**: `04` → `06` → `07` → `08`
- **Produtividade avançada**: `02` → `10` → `11` → `12`

## Versões assumidas

- **Neovim:** 0.10+ stable (features 0.11+ marcadas explicitamente nas notas)
- **LazyVim:** versão de 2026-05-19 (verificar `:Lazy` na sessão de execução; declarar exata em pass final)
- **lazy.nvim:** latest
- **LuaJIT:** bundled com Neovim (Lua 5.1-compatible)

## Veja também

- [[Dicionário do Terminal]]
- [[03-Dominios/Terminal/index|Trilha Terminal]]
