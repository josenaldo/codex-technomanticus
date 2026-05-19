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

### Autocmd
Comando que dispara automaticamente em eventos do Neovim (salvar arquivo, abrir buffer, mudar tipo, etc.). Em Lua: `vim.api.nvim_create_autocmd`. Agrupados em `augroup` pra evitar duplicação ao recarregar config.

Veja também: [[06 - Estrutura de config]].

### Buffer
Representação em memória de um arquivo aberto no Neovim. Independente de windows e tabs — N buffers podem estar abertos sem nenhum visível, e o mesmo buffer pode aparecer em várias windows.

Veja também: [[03 - Edição e navegação]].

### Jump list
Pilha de saltos que o Neovim mantém para cada window. Comandos como `gd`, `*`, `}`, `/` empurram a posição. Navegar: `<C-o>` (back), `<C-i>` (forward). Listar: `:jumps`.

Veja também: [[03 - Edição e navegação]].

### Keymap
Mapeamento de uma sequência de teclas pra uma ação. Em Neovim moderno: `vim.keymap.set(mode, lhs, rhs, opts)`. Opções comuns: `desc` (descrição visível em which-key), `silent`, `noremap` (default true em vim.keymap.set).

Veja também: [[06 - Estrutura de config]], [[08 - Customizando LazyVim]].

### Leader key
Tecla "prefixo" pra atalhos custom. Default Neovim: `\`. Em LazyVim: `<Space>`. Configurada com `vim.g.mapleader = " "` ANTES de plugins carregarem.

Veja também: [[06 - Estrutura de config]], [[08 - Customizando LazyVim]].

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

### Distribuição
Preset de configuração de Neovim que combina um conjunto de plugins, opções e keymaps. Exemplos: LazyVim, LunarVim, AstroNvim, NvChad, kickstart.nvim. Diferente de Neovim "vanilla", onde tudo é configurado do zero.

Veja também: [[04 - LazyVim tour]], [[08 - Customizando LazyVim]].

### LazyVim
Distribuição Neovim opinada mantida por Folke Lemaitre. Bundle inclui Telescope (fuzzy), neo-tree (explorer), which-key, lazy.nvim (plugin manager), LSP stack (mason + nvim-lspconfig + nvim-cmp + conform). Filosofia: "use defaults; customize on top".

Veja também: [[04 - LazyVim tour]], [[08 - Customizando LazyVim]].

### Lazy-loading
Carregar um plugin apenas quando necessário (em evento, comando, filetype ou tecla específica), ao invés de no startup. Reduz tempo de boot. Em lazy.nvim: campos `event`, `cmd`, `ft`, `keys` na plugin spec.

Veja também: [[07 - lazy.nvim]].

### lazy.nvim
Plugin manager moderno do Neovim mantido por Folke Lemaitre. Usa Lua DSL pra spec de plugins. Recursos: lazy-loading nativo, lockfile (`lazy-lock.json`), profiling, UI interativa (`:Lazy`).

Veja também: [[07 - lazy.nvim]].

### neo-tree
Plugin de file explorer (árvore de arquivos lateral) que LazyVim usa como default. Atalho `<leader>e`. Suporta operações sobre arquivos (add, delete, rename, copy/paste) por keymaps dentro da árvore.

Veja também: [[04 - LazyVim tour]].

### Plugin manager
Ferramenta que instala, atualiza e carrega plugins do Neovim. Os principais: lazy.nvim (atual, em LazyVim), packer.nvim (legado), vim-plug (legado, Vimscript). LazyVim usa lazy.nvim por default.

Veja também: [[07 - lazy.nvim]], [[04 - LazyVim tour]].

### Plugin spec
Descrição de um plugin em formato tabela Lua, usada pelo lazy.nvim. Campos comuns: URL/source, `opts` (config passada ao setup), `config` (callback de init custom), `event`/`cmd`/`ft`/`keys` (triggers de lazy-load), `dependencies`.

Veja também: [[07 - lazy.nvim]], [[08 - Customizando LazyVim]].

### Telescope
Plugin de fuzzy finder pra Neovim. Em LazyVim, atalhos principais: `<leader>ff` (find files), `<leader>fg` (live grep), `<leader>,` (buffers), `<leader>fh` (help). Pode mandar resultados pra quickfix com `<C-q>`.

Veja também: [[04 - LazyVim tour]], [[11 - Workflow avançado]].

### which-key
Plugin de descoberta de keymaps. Após pressionar uma key prefix (ex: `<leader>`), espera ~1s e mostra popup com os keymaps disponíveis e o que fazem. Atalho `<leader>sk` no LazyVim faz search-keymap.

Veja também: [[04 - LazyVim tour]].

## LSP & dev

### Code action
Operação contextual sugerida pelo LSP — refactoring, fix automático, import, etc. Em LazyVim: `<leader>ca` lista as code actions disponíveis na linha/cursor atual.

Veja também: [[04 - LazyVim tour]], [[09 - LSP no Neovim]].

### Format on save
Comportamento (default no LazyVim) de rodar o formatter (conform.nvim no LazyVim) automaticamente ao salvar (`:w`). Toggle: `<leader>uf`.

Veja também: [[04 - LazyVim tour]], [[09 - LSP no Neovim]].

### LSP
Language Server Protocol — protocolo cliente/servidor que dá a editores recursos como go-to-definition, hover, completions, diagnostics, formatting. Implementado em Neovim via cliente built-in (`vim.lsp`) e `nvim-lspconfig`. Servers são instalados via Mason.

Veja também: [[04 - LazyVim tour]], [[09 - LSP no Neovim]].

## Avançado

### init.lua
Arquivo principal de configuração do Neovim moderno (sucessor do `init.vim` em Vimscript). Localização: `~/.config/nvim/init.lua`. No LazyVim, é minimal — apenas faz `require("config.lazy")` que carrega o bootstrap.

Veja também: [[05 - Lua para Neovim]], [[06 - Estrutura de config]].

### Lua
Linguagem de scripting embutida em Neovim (via LuaJIT — Lua 5.1-compatible). Substitui Vimscript pra config moderna. Tipos minimal (nil, boolean, number, string, table, function), 1-indexed em tabelas, truthiness peculiar (`0` é truthy).

Veja também: [[05 - Lua para Neovim]].
