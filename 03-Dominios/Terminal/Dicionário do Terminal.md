---
title: "Dicionário do Terminal"
created: 2026-05-19
updated: 2026-05-19
type: glossary
status: seedling
aliases: []
tags:
  - glossary
  - terminal
lang: pt
publish: true
---

# Dicionário do Terminal

> Glossário do domínio Terminal: jargão de editor (Neovim, LazyVim, modal editing), shell, multiplexer, TUIs e workflow. Cada verbete é referenciado por uma ou mais notas das trilhas do domínio.

<!--
Como usar este glossário:

- Cada verbete é um `###` dentro de uma `##` temática.
- Verbetes em ordem alfabética dentro de cada bloco.
- Linkar de outra nota: [[Dicionário do Terminal#Nome do termo]]
- Customizar texto exibido: [[Dicionário do Terminal#Nome do termo|texto]]
- A skill /verbete adiciona termos automaticamente em ordem alfabética.
- Ajuste `lang:` no frontmatter (`pt` ou `en`) — define o idioma das definições.
- Cada verbete tem (i) 1-3 frases de definição em PT-BR e (ii) "Veja também:" com wikilinks para a(s) nota(s) que aprofundam.
-->

## Vim / Neovim core

### Buffer
Representação em memória de um arquivo aberto no Neovim. Independente de windows e tabs — N buffers podem estar abertos sem nenhum visível, e o mesmo buffer pode aparecer em várias windows.

Veja também: [[03 - Edição e navegação]].

### Jump list
Pilha de saltos que o Neovim mantém para cada window. Comandos como `gd`, `*`, `}`, `/` empurram a posição. Navegar: `<C-o>` (back), `<C-i>` (forward). Listar: `:jumps`.

Veja também: [[03 - Edição e navegação]].

### Modal editing
Modelo de edição em que o editor opera em modos distintos (normal, insert, visual, command…); cada modo redefine o significado das teclas. É a base de Vim/Neovim e o que permite tratar edição como uma linguagem de comandos.

Veja também: [[01 - Modal editing]], [[02 - Motions, operadores e text objects]].

### Modo
Um dos estados internos do Neovim que define como as teclas são interpretadas. Os modos principais são: normal (comandos), insert (digitar), visual (selecionar), command-line (`:`), terminal (REPL embutido).

Veja também: [[01 - Modal editing]].

### Motion
Comando que move o cursor em modo normal (ex: `w`, `e`, `gg`, `f<x>`). Em Vim, motions são "substantivos" que combinam com operadores ("verbos") para formar comandos. Ex: `dw` = delete + word.

Veja também: [[02 - Motions, operadores e text objects]].

### Operador
Comando que age sobre um alvo definido por motion ou text object. Operadores principais: `d` (delete), `c` (change), `y` (yank), `v` (visual), `>`/`<` (indent), `gu`/`gU` (case).

Veja também: [[02 - Motions, operadores e text objects]].

### Text object
Região textual delimitada semanticamente (palavra, parágrafo, par de delimitadores, tag HTML…). Acessada por prefixos `i` (inner — só o conteúdo) ou `a` (around — inclui delimitadores). Ex: `ci"` muda o conteúdo entre aspas; `da{` deleta o bloco `{ }` inteiro.

Veja também: [[02 - Motions, operadores e text objects]], [[12 - Treesitter avançado]].

### Undotree
Estrutura em árvore (não linear) que o Neovim mantém para desfazer/refazer. Cada `u` volta no tempo; mas se você edita após um undo, cria um novo ramo. Plugin `undotree.nvim` (LazyVim Extra) navega visualmente; comandos `:earlier`/`:later` movem por tempo (`:earlier 5m`).

Veja também: [[03 - Edição e navegação]].

## Ecossistema LazyVim

## LSP & dev

## Avançado
