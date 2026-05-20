---
title: "Shell"
type: moc
publish: true
created: 2026-05-19
updated: 2026-05-19
status: growing
progresso: andamento
tags:
  - terminal
  - shell
  - zsh
  - oh-my-zsh
  - powerlevel10k
  - moc
aliases:
  - Shell
  - Zsh
  - Oh-My-Zsh
  - Powerlevel10k
---
# Shell

> [!abstract] TL;DR
> Galho 2 da trilha Terminal. Domínio de Zsh + Oh-My-Zsh + Powerlevel10k como shell primário, em 3 fases (4 + 4 + 2 = 10 notas): do "Zsh vs Bash" ao escrever seu plugin OMZ e seu theme.

Esse galho cobre o shell end-to-end: fundamentos do Zsh e diferenças do Bash, history e plugins essenciais do OMZ (Iniciado), customização com Powerlevel10k, keybindings, ZLE e completion system (Adepto), e maestria com globbing avançado, parameter expansion e plugins/themes próprios (Magus). OMZ + P10k é o caminho primário porque é o setup real operado; Zsh puro aparece quando o conceito é universal.

## Conteúdo

### Iniciado

- [[01 - Zsh vs Bash]]
- [[02 - Zsh essencial]]
- [[03 - History do Zsh]]
- [[04 - Oh-My-Zsh — anatomia e plugins essenciais]]

### Adepto

- [[05 - Powerlevel10k]]
- [[06 - Keybindings práticos]]
- [[07 - ZLE]]
- [[08 - Completion system (compsys)]]

### Magus

- [[09 - Globbing avançado e parameter expansion]]
- [[10 - Plugins, themes e custom no OMZ]]

## Rotas alternativas

- **Daily-driver enxuto** (Iniciado completa): `01` → `02` → `03` → `04`
- **Customização visual**: `04` → `05` → `10`
- **Domínio do motor**: `02` → `06` → `07` → `08` → `09`

## Versões assumidas

- **Zsh:** 5.9+ (Ubuntu/Linux bundle) — versão capturada no Task 0
- **Oh-My-Zsh:** `master` em ~maio/2026 (commit declarado em pass final)
- **Powerlevel10k:** `master` 2024-07 (commit declarado em pass final) — projeto em modo manutenção
- Plugins externos: versões `master` em 2026-05-19

## Veja também

- [[Dicionário do Terminal]]
- [[03-Dominios/Terminal/index|Trilha Terminal]]
