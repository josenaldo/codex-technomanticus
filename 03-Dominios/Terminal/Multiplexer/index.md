---
title: "Multiplexer"
type: moc
publish: true
created: 2026-05-21
updated: 2026-05-21
status: growing
progresso: andamento
tags:
  - terminal
  - multiplexer
  - zellij
  - moc
aliases:
  - Multiplexer
  - Zellij
---
# Multiplexer

> [!abstract] TL;DR
> Galho 3 da trilha Terminal. Domínio de Zellij como multiplexer primário, em 3 fases (3 + 2 + 2 = 7 notas): do "Zellij vs tmux" ao escrever layout KDL e estender com plugin WASM.

Esse galho cobre o multiplexer end-to-end: por que Zellij e quando tmux ainda ganha (Iniciado); modelo mental de sessions/tabs/panes; modos básicos e keybindings essenciais; sessões persistentes e layouts declarativos em KDL (Adepto); modos avançados, plugins WASM e integração com Neovim e shell (Magus).

## Conteúdo

### Iniciado

- [[01 - Zellij vs tmux vs screen]]
- [[02 - Modelo mental — sessions, tabs, panes]]
- [[03 - Modos básicos e keybindings essenciais]]

### Adepto

- [[04 - Sessões persistentes — detach, attach, gerenciamento]]
- [[05 - Layouts declarativos em KDL]]

### Magus

- [[06 - Modos avançados, plugins e copy-mode]]
- [[07 - Integração com Neovim e shell]]

## Rotas alternativas

- **Daily-driver enxuto** (Iniciado completa + sessions): `01` → `02` → `03` → `04`
- **Config-first** (saltar pra layouts cedo): `02` → `05` → `04`
- **Maestria** (motor + integração): `03` → `04` → `05` → `06` → `07`

## Versões assumidas

- **Zellij:** `<VERSAO_ZELLIJ>` (capturada no pré-flight)
- Plugins externos: versões `master` em 2026-05-21

## Veja também

- [[Dicionário do Terminal]]
- [[03-Dominios/Terminal/index|Trilha Terminal]]
