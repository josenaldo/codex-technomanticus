---
title: "Dotfiles"
type: moc
publish: true
created: 2026-05-22
updated: 2026-05-22
status: growing
progresso: andamento
tags:
  - terminal
  - dotfiles
  - moc
aliases:
  - Dotfiles
---
# Dotfiles

> [!abstract] TL;DR
> Galho 5 da trilha Terminal. Domínio de dotfiles — arquivos de config (`.zshrc`, `.gitconfig`, `~/.config/*`) versionados e syncados entre máquinas. 9 notas (3 Iniciado + 3 Adepto + 3 Magus). Formato catálogo comparativo das 3 ferramentas principais: GNU stow, chezmoi, bare git repo.

Esse galho parte do zero (o que são dotfiles, por que versionar) até workflows operacionais avançados (secrets encryption, bootstrap automático, sync entre máquinas heterogêneas). As 3 ferramentas principais recebem profundidade equivalente — Adepto cobre stow, chezmoi e bare repo em notas separadas com mesmos critérios, deixando o leitor escolher informadamente.

## Conteúdo

### Iniciado

- [[01 - Princípios — o que são dotfiles e por que versionar]]
- [[02 - Anatomia — estrutura típica e XDG Base Directory]]
- [[03 - Cross-OS — Linux vs macOS vs WSL]]

### Adepto

- [[04 - GNU stow — symlinks declarativos]]
- [[05 - chezmoi — manager completo com templates]]
- [[06 - Bare git repo — abordagem minimalista]]

### Magus

- [[07 - Secrets em dotfiles — git-crypt, age, sops]]
- [[08 - Bootstrap — máquina nova zero-to-ready]]
- [[09 - Sync entre máquinas heterogêneas]]

## Rotas alternativas

- **Mínimo viável** (entender + 1 ferramenta): `01` → `02` → `04`
- **Comparativo das ferramentas**: `01` → `02` → `04` → `05` → `06`
- **Maestria operacional**: `04` (ou `05`) → `07` → `08` → `09`
- **Cross-OS first**: `01` → `02` → `03` → `05`

## Versões assumidas

- **GNU stow:** `<VERSAO_STOW>` (capturada no pré-flight)
- **chezmoi:** `<VERSAO_CHEZMOI>` (capturada no pré-flight)
- **git:** `<VERSAO_GIT>` (capturada no pré-flight)
- **OS de referência:** `<OS_REF>`

## Veja também

- [[Dicionário do Terminal]]
- [[03-Dominios/Terminal/index|Trilha Terminal]]
