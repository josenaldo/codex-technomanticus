---
title: "Terminal"
type: moc
publish: true
created: 2026-05-18
updated: 2026-05-21
status: growing
progresso: andamento
tags:
  - terminal
  - moc
  - dev-environment
aliases:
  - Terminal
---
# Terminal

> [!abstract] TL;DR
> Trilha do ambiente de trabalho no terminal: editor (Neovim/LazyVim), shell (Zsh/p10k), multiplexer (Zellij), TUIs (Lazygit/Lazydocker), dotfiles, CLI utils e playbooks de workflow. 7 galhos, ~57 notas distribuídas em 3 fases (Iniciado → Adepto → Magus) por galho. Cada galho é implementado em sessão própria — esta nota é o roadmap interativo da trilha.

Esta trilha cobre o ecossistema TUI/keyboard-first pra trabalho de desenvolvimento no terminal. Cada galho é fechado em si mesmo (Iniciado + Adepto + Magus na mesma execução) e nasce em uma sessão dedicada com spec e plano próprios.

## Conteúdo

### Galhos

- [[03-Dominios/Terminal/Editor/index|Editor]] — galho 1: Neovim + LazyVim (modal editing, plugins, LSP, Treesitter, DAP)
- [[03-Dominios/Terminal/Shell/index|Shell]] — galho 2: Zsh + Oh-My-Zsh + Powerlevel10k (config, plugins, completion, ZLE)
- [[03-Dominios/Terminal/Multiplexer/index|Multiplexer]] — galho 3: Zellij (sessions, layouts KDL, plugins WASM)
- [[03-Dominios/Terminal/TUIs/index|TUIs de Dev]] — galho 4: Lazygit + Lazydocker (operações, config, debugging)
- Dotfiles — galho 5 (planejado): gerenciamento de configs e sync
- CLI Utils — galho 6 (planejado): fzf, ripgrep, bat, eza, zoxide…
- Workflow — galho 7 (planejado): playbooks cross-tool

### Fases de aprendizado

Cada galho organiza suas notas em 3 fases progressivas:

- **Iniciado** — visão geral, nível júnior. Vocabulário básico, modelo mental, comandos suficientes pra começar a usar a ferramenta.
- **Adepto** — domínio operacional, nível pleno. Configurar, customizar, usar com confiança em projetos reais.
- **Magus** — maestria, nível senior. Técnicas avançadas, otimização, casos de uso obscuros.

## Veja também

- [[03-Dominios/Ferramentas/Ferramentas|Ferramentas]]
