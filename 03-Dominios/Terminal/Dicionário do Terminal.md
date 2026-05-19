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

### Macro
Sequência de teclas gravada e replicável em Neovim. Gravar: `q<reg>` + teclas + `q`. Replay: `@<reg>` (uma vez), `@@` (último), `N@<reg>` (N vezes). O macro é um register editável — `:put a` mostra/edita.

Veja também: [[10 - Registers, marks, macros]].

### Mark
Posição salva (linha + coluna) em um buffer. Locais (`a`-`z`, scope buffer) ou globais (`A`-`Z`, persistem entre arquivos e sessões). Criar: `m<letra>`. Saltar: `'<letra>` (linha) ou `` `<letra> `` (linha+coluna). Listar: `:marks`.

Veja também: [[10 - Registers, marks, macros]].

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

### Quickfix list
Lista global de "lugares pra ir" no Neovim (resultados de grep, compile errors, LSP references, TODOs…). Editável em massa via `:cdo <cmd>`. Comandos: `:copen` (abre), `:cnext`/`:cprev` (navega), `:cc N` (item N). Em LazyVim: `]q`/`[q` é keymap default.

Veja também: [[11 - Workflow avançado]].

### Register
"Clipboard" nomeado do Vim. Yank/delete/change escrevem em registers; paste lê. Classes: named (`a`-`z`), numbered (`0`-`9`, histórico), system (`+`/`*`), expression (`=`), search (`/`), command (`:`), black hole (`_`). Listar: `:reg`.

Veja também: [[10 - Registers, marks, macros]].

### Text object
Região textual delimitada semanticamente (palavra, parágrafo, par de delimitadores, tag HTML…). Acessada por prefixos `i` (inner — só o conteúdo) ou `a` (around — inclui delimitadores). Ex: `ci"` muda o conteúdo entre aspas; `da{` deleta o bloco `{ }` inteiro.

Veja também: [[02 - Motions, operadores e text objects]], [[12 - Treesitter avançado]].

### Undotree
Estrutura em árvore (não linear) que o Neovim mantém para desfazer/refazer. Cada `u` volta no tempo; mas se você edita após um undo, cria um novo ramo. Plugin `undotree.nvim` (LazyVim Extra) navega visualmente; comandos `:earlier`/`:later` movem por tempo (`:earlier 5m`).

Veja também: [[03 - Edição e navegação]].

## Ecossistema LazyVim

### AST
Abstract Syntax Tree — árvore sintática abstrata. Representação hierárquica da estrutura de um código por um parser. Em Neovim, fornecida por Treesitter por linguagem; viabiliza highlight preciso, text objects estruturais e navegação por nó.

Veja também: [[12 - Treesitter avançado]].

### Distribuição
Preset de configuração de Neovim que combina um conjunto de plugins, opções e keymaps. Exemplos: LazyVim, LunarVim, AstroNvim, NvChad, kickstart.nvim. Diferente de Neovim "vanilla", onde tudo é configurado do zero.

Veja também: [[04 - LazyVim tour]], [[08 - Customizando LazyVim]].

### Lazy-loading
Carregar um plugin apenas quando necessário (em evento, comando, filetype ou tecla específica), ao invés de no startup. Reduz tempo de boot. Em lazy.nvim: campos `event`, `cmd`, `ft`, `keys` na plugin spec.

Veja também: [[07 - lazy.nvim]].

### lazy.nvim
Plugin manager moderno do Neovim mantido por Folke Lemaitre. Usa Lua DSL pra spec de plugins. Recursos: lazy-loading nativo, lockfile (`lazy-lock.json`), profiling, UI interativa (`:Lazy`).

Veja também: [[07 - lazy.nvim]].

### LazyVim
Distribuição Neovim opinada mantida por Folke Lemaitre. Bundle inclui Telescope (fuzzy), neo-tree (explorer), which-key, lazy.nvim (plugin manager), LSP stack (mason + nvim-lspconfig + nvim-cmp + conform). Filosofia: "use defaults; customize on top".

Veja também: [[04 - LazyVim tour]], [[08 - Customizando LazyVim]].

### neo-tree
Plugin de file explorer (árvore de arquivos lateral) que LazyVim usa como default. Atalho `<leader>e`. Suporta operações sobre arquivos (add, delete, rename, copy/paste) por keymaps dentro da árvore.

Veja também: [[04 - LazyVim tour]].

### Plugin manager
Ferramenta que instala, atualiza e carrega plugins do Neovim. Os principais: lazy.nvim (atual, em LazyVim), packer.nvim (legado), vim-plug (legado, Vimscript). LazyVim usa lazy.nvim por default.

Veja também: [[07 - lazy.nvim]], [[04 - LazyVim tour]].

### Plugin spec
Descrição de um plugin em formato tabela Lua, usada pelo lazy.nvim. Campos comuns: URL/source, `opts` (config passada ao setup), `config` (callback de init custom), `event`/`cmd`/`ft`/`keys` (triggers de lazy-load), `dependencies`.

Veja também: [[07 - lazy.nvim]], [[08 - Customizando LazyVim]].

### Query
Pattern em Tree-sitter (sintaxe S-expression em arquivos `.scm`) que casa contra a AST. Usada pra definir highlights, text objects, captures custom. Composta de patterns, captures (`@nome`) e predicates (`#match?`, `#any-of?`).

Veja também: [[12 - Treesitter avançado]].

### Telescope
Plugin de fuzzy finder pra Neovim. Em LazyVim, atalhos principais: `<leader>ff` (find files), `<leader>fg` (live grep), `<leader>,` (buffers), `<leader>fh` (help). Pode mandar resultados pra quickfix com `<C-q>`.

Veja também: [[04 - LazyVim tour]], [[11 - Workflow avançado]].

### Treesitter
Biblioteca de parsing incremental (do GitHub). No Neovim, integrada via `nvim-treesitter` — gera AST por linguagem em tempo real, usada pra highlight preciso, text objects estruturais (`af`, `ic`), navegação por nó. Parsers instaláveis via `:TSInstall <lang>`.

Veja também: [[12 - Treesitter avançado]].

### which-key
Plugin de descoberta de keymaps. Após pressionar uma key prefix (ex: `<leader>`), espera ~1s e mostra popup com os keymaps disponíveis e o que fazem. Atalho `<leader>sk` no LazyVim faz search-keymap.

Veja também: [[04 - LazyVim tour]].

## LSP & dev

### Code action
Operação contextual sugerida pelo LSP — refactoring, fix automático, import, etc. Em LazyVim: `<leader>ca` lista as code actions disponíveis na linha/cursor atual.

Veja também: [[04 - LazyVim tour]], [[09 - LSP no Neovim]].

### Diagnostic
Mensagem de problema (erro, warning, info, hint) emitida por um language server ou linter sobre um arquivo. Em Neovim: rendered como sign no gutter, virtual text inline, underline. Listada via `:lopen` ou Telescope `<leader>xd`.

Veja também: [[09 - LSP no Neovim]].

### Format on save
Comportamento (default no LazyVim) de rodar o formatter (conform.nvim no LazyVim) automaticamente ao salvar (`:w`). Toggle: `<leader>uf`.

Veja também: [[04 - LazyVim tour]], [[09 - LSP no Neovim]].

### Formatter
Ferramenta que reformata código segundo regras (prettier, ruff, gofmt, stylua…). Em LazyVim moderno, dispatcher é conform.nvim. Acionado em `:w` (format on save) ou explicitamente via `<leader>cf`.

Veja também: [[09 - LSP no Neovim]].

### Language server
Processo separado que implementa a Language Server Protocol pra uma linguagem específica (ex: `ts_ls` pra TypeScript, `lua_ls` pra Lua, `rust_analyzer` pra Rust). Editor é cliente; server responde requests sobre o código (hover, definition, refactor).

Veja também: [[09 - LSP no Neovim]].

### Linter
Ferramenta que analisa código por padrões problemáticos sem necessariamente quebrar build (eslint, ruff, shellcheck…). Em LazyVim, dispatcher é nvim-lint. Diagnostics aparecem no mesmo flow do LSP.

Veja também: [[09 - LSP no Neovim]].

### LSP
Language Server Protocol — protocolo cliente/servidor que dá a editores recursos como go-to-definition, hover, completions, diagnostics, formatting. Implementado em Neovim via cliente built-in (`vim.lsp`) e `nvim-lspconfig`. Servers são instalados via Mason.

Veja também: [[04 - LazyVim tour]], [[09 - LSP no Neovim]].

### Mason
Plugin de Neovim que gerencia instalação/atualização de language servers, formatters, linters e DAP adapters. `:Mason` abre TUI. Bundle do LazyVim.

Veja também: [[09 - LSP no Neovim]], [[13 - Snippets e DAP]].

### nvim-cmp
Engine de completion pra Neovim. Aceita múltiplas sources (LSP, buffer, path, snippet). Renderiza popup em insert mode. Bundle do LazyVim.

Veja também: [[09 - LSP no Neovim]].

### nvim-lspconfig
Plugin que provê configs padronizadas pra ~200 language servers em Neovim. Em LazyVim, customização via `opts.servers.<nome> = { settings = {...} }`.

Veja também: [[09 - LSP no Neovim]].

## Avançado

### DAP
Debug Adapter Protocol — protocolo open source (Microsoft) que padroniza comunicação entre editores e debuggers. Em Neovim: `nvim-dap` (cliente) + adapter por linguagem (instalável via Mason). UI: `nvim-dap-ui`.

Veja também: [[13 - Snippets e DAP]].

### init.lua
Arquivo principal de configuração do Neovim moderno (sucessor do `init.vim` em Vimscript). Localização: `~/.config/nvim/init.lua`. No LazyVim, é minimal — apenas faz `require("config.lazy")` que carrega o bootstrap.

Veja também: [[05 - Lua para Neovim]], [[06 - Estrutura de config]].

### Lua
Linguagem de scripting embutida em Neovim (via LuaJIT — Lua 5.1-compatible). Substitui Vimscript pra config moderna. Tipos minimal (nil, boolean, number, string, table, function), 1-indexed em tabelas, truthiness peculiar (`0` é truthy).

Veja também: [[05 - Lua para Neovim]].

### LuaSnip
Snippet engine pra Neovim, escrita em Lua. Suporta snippets em Lua puro (mais expressivo) e em formato VS Code JSON (mais portável, pacotes como `friendly-snippets`). Integra com `nvim-cmp`.

Veja também: [[13 - Snippets e DAP]].

### Snippet
Trecho de código parametrizável que expande a partir de um trigger. Tabstops (`$1`, `$2`, `$0`) permitem navegação ordenada entre campos editáveis. Em Neovim moderno: LuaSnip (engine) + friendly-snippets (catálogo VS Code-style).

Veja também: [[13 - Snippets e DAP]].
