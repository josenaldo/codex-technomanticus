---
title: "Spec — Galho 1 da trilha Terminal (Editor / Neovim + LazyVim)"
date: 2026-05-19
author: Josenaldo
status: draft
type: spec
publish: false
---

# Spec — Galho 1 da trilha Terminal (Editor / Neovim + LazyVim)

## 1. Contexto e motivação

Este é o **primeiro galho** da trilha Terminal (roadmap em `docs/superpowers/specs/2026-05-18-trilha-terminal-design.md`). Pressupõe leitura desse roadmap — a tríade Iniciado/Adepto/Magus, a estrutura tronco/galho e a iteração vertical por galho não são repetidas aqui.

O usuário acabou de instalar LazyVim sobre Neovim e quer dominar o editor — não como curiosidade, como ferramenta principal de trabalho. O Editor é o galho mais denso e íngreme do stack: modal editing tem curva de aprendizado própria, LazyVim adiciona uma camada de abstração com plugins pré-configurados, e config customizada exige Lua.

As 13 notas cobrem do "abrir um arquivo e salvar" até "criar text objects com Treesitter e configurar DAP". A ordem de implementação é por fase (Iniciado → Adepto → Magus), e LazyVim é o caminho primário em Iniciado/Adepto (porque é o setup real do usuário); Vim/Neovim core aparece quando o conceito é universal (modal editing, motions) e domina em Magus.

## 2. Objetivo

Produzir, em uma sessão de execução dedicada, **13 notas atômicas + 1 MOC do galho + Dicionário do Terminal** em `03-Dominios/Terminal/Editor/` e `03-Dominios/Terminal/`, todas `publish: true`, em PT-BR, distribuídas em 3 fases (4 Iniciado + 5 Adepto + 4 Magus).

A trilha precisa ser:

- **Atômica** — cada nota linkável e citável separadamente
- **Híbrida em camadas** — TL;DR + corpo técnico, no padrão do vault
- **Casada com o setup real** — LazyVim como caminho primário, não Neovim vanilla
- **Atualizada com 2026** — Neovim 0.10+, LazyVim atual, lazy.nvim atual
- **Apoiada por dicionário** — jargão técnico tem verbete no dicionário do domínio, linkado nas notas

## 3. Escopo

### Em escopo

- 14 arquivos markdown:
  - 13 notas em `03-Dominios/Terminal/Editor/`
  - 1 MOC do galho em `03-Dominios/Terminal/Editor/index.md` (segue o padrão do tronco e do roadmap)
- 1 dicionário em `03-Dominios/Terminal/Dicionário do Terminal.md` com ~30 verbetes iniciais
- Atualização do tronco `03-Dominios/Terminal/index.md` ativando o wikilink do Editor
- Todos os arquivos com `publish: true`
- Idioma: PT-BR; termos técnicos em inglês mantidos; cada nota tem seção "Em inglês" com 5-10 termos PT→EN
- Pesquisa baseada em fontes primárias verificadas (links concretos no spec)

### Fora de escopo

- **Comparação Vim vs Emacs vs IDEs** — não é o foco da trilha
- **Vimscript** — apenas Lua (Vimscript aparece só quando incontornável)
- **Distribuições alternativas** (LunarVim, AstroNvim, NvChad) — LazyVim é a escolha
- **Plugins fora do que LazyVim bundle ou que sejam mainstream consensuais** — Telescope-extensions exóticas, vsnip, snippy, null-ls ficam fora; conform.nvim e nvim-lint (defaults atuais do LazyVim) entram
- **Workflow cross-tool** — Lazygit, Zellij e Lazydocker são outros galhos da trilha
- **Criação de plugin do zero** — fora do escopo do galho (poderia virar futuro galho de Workflow ou nota independente)

### Foco

Dev individual editando código no stack típico do usuário (TS/JS, Lua, Markdown). LazyVim é o setup operado; Neovim é a fundação invisível na maior parte das notas.

## 4. Audiência e barra de qualidade

**Audiência primária:** dev senior com anos de IntelliJ/VS Code, novo em Neovim. Sabe que modal editing existe mas não tem fluência, instalou LazyVim e quer dominar — não regredir produtivamente enquanto aprende.

**Audiência secundária:** o mesmo dev seis meses depois, voltando a uma técnica avançada que esqueceu (macros, queries de Treesitter, custom snippet). Para esse público, o MOC com rotas alternativas é otimizado.

**Barra de qualidade:** ao terminar de ler o galho, o leitor deve conseguir:

1. Editar texto fluentemente em modo normal (motions + operadores + text objects)
2. Salvar, abrir e navegar entre arquivos sem precisar consultar
3. Usar LazyVim no dia-a-dia (Telescope, neo-tree, which-key, LSP keys default, complete, comment, surround)
4. Editar `~/.config/nvim/` sem medo — adicionar plugin, override de keymap, habilitar Extra
5. Diagnosticar problema de LSP (`:LspInfo`, `:Mason`, `:ConformInfo`)
6. Usar registers e marks rotineiramente (yank em registers nomeados, marks pra arquivos abertos)
7. Gravar e editar macros pra automação repetitiva
8. Operar refactoring de projeto (Telescope → quickfix → cdo)
9. Escrever query Treesitter pra textobject customizado
10. Habilitar e usar DAP em pelo menos uma linguagem

## 5. Estrutura do galho (14 arquivos)

### MOC do galho

Arquivo: `03-Dominios/Terminal/Editor/index.md` (mesmo padrão do tronco `Terminal/index.md` e do roadmap).

Estrutura:

```markdown
> [!abstract] TL;DR
> Galho 1 da trilha Terminal. Domínio de Neovim + LazyVim como editor primário,
> em 3 fases (4 + 5 + 4 = 13 notas).

## Iniciado
- [[01 - Modal editing]]
- [[02 - Motions, operadores e text objects]]
- [[03 - Edição e navegação]]
- [[04 - LazyVim tour]]

## Adepto
- [[05 - Lua para Neovim]]
- [[06 - Estrutura de config]]
- [[07 - lazy.nvim]]
- [[08 - Customizando LazyVim]]
- [[09 - LSP no Neovim]]

## Magus
- [[10 - Registers, marks, macros]]
- [[11 - Workflow avançado]]
- [[12 - Treesitter avançado]]
- [[13 - Snippets e DAP]]

## Rotas alternativas
- **Uso diário** (Iniciado completa): 01 → 02 → 03 → 04
- **Customização**: 04 → 06 → 07 → 08
- **Produtividade avançada**: 02 → 10 → 11 → 12

## Veja também
- [[Dicionário do Terminal]]
- [[03-Dominios/Terminal/index|Trilha Terminal]]
```

### Fase Iniciado (4 notas)

#### 01 — Modal editing
- **Slug:** `01 - Modal editing.md`
- **Primárias:**
  - [Neovim user intro](https://neovim.io/doc/user/intro.html)
  - `:Tutor` (vimtutor embutido — comando dentro do Neovim)
- **Secundárias:**
  - [Learn Vim — irian.to (livro online aberto)](https://learnvim.irian.to/)
  - [Practical Vim — Drew Neil (livro)](https://pragprog.com/titles/dnvim2/practical-vim-second-edition/)
  - [Boost your fu (guide universal Vim)](https://www.barbarianmeetscoding.com/boost-your-coding-fu-with-vscode-and-vim)
- **Cobre:**
  - Modos (normal, insert, visual, visual-line, visual-block, command, terminal)
  - Filosofia "edição como linguagem" e por que isso multiplica velocidade
  - Troca entre modos (i/a/o, Esc/<C-[>, v/V/<C-v>, :)
  - Indicadores visuais de modo no statusline do LazyVim
- **Não cobre:** motions/operadores (02), `:substitute` (03), terminal mode em profundidade (11)
- **Verbetes referenciados:** modal editing, modo

#### 02 — Motions, operadores e text objects
- **Slug:** `02 - Motions, operadores e text objects.md`
- **Primárias:**
  - [:help motion.txt](https://neovim.io/doc/user/motion.html)
  - [:help text-objects](https://neovim.io/doc/user/motion.html#text-objects)
- **Secundárias:**
  - [The Valuable Dev — Vim text objects](https://thevaluable.dev/vim-text-objects/)
  - [ThePrimeagen — Vim As Your Editor (YouTube)](https://www.youtube.com/watch?v=X6AR2RMB5tE)
  - [Drew Neil — Practical Vim (caps. operadores e text objects)](https://pragprog.com/titles/dnvim2/practical-vim-second-edition/)
- **Cobre:**
  - Gramática verbo+substantivo (`d` + `iw`, `c` + `ap`, `y` + `i"`)
  - Motions essenciais (h/j/k/l, w/e/b/B/W, f/t/F/T, `%`, gg/G, 0/$, ^)
  - Operadores principais (d, c, y, v, gu/gU, >, <)
  - Text objects (iw/aw, i"/a", ip/ap, it/at, i)/a))
  - Contagem antes de motion (3w, d3w)
  - Dot command (`.`) — repetir última edição
- **Não cobre:** registers (10), macros (10), surround.nvim como plugin (mencionar em 04)
- **Verbetes referenciados:** motion, operador, text object

#### 03 — Edição e navegação
- **Slug:** `03 - Edição e navegação.md`
- **Primárias:**
  - [:help change.txt](https://neovim.io/doc/user/change.html)
  - [:help pattern.txt](https://neovim.io/doc/user/pattern.html)
  - [:help windows.txt](https://neovim.io/doc/user/windows.html)
  - [:help cmdline](https://neovim.io/doc/user/cmdline.html)
- **Secundárias:**
  - [Brian Storti — Vim registers (intro)](https://www.brianstorti.com/vim-registers/)
  - [Learn Vim — buffers, windows, tabs](https://learnvim.irian.to/basics/buffers_windows_tabs)
- **Cobre:**
  - Ex commands básicas: `:w`, `:q`, `:wq`, `:x`, `:e <arquivo>`, `:!cmd`, `:q!`, `:qa`
  - Yank/paste/delete básico (sem entrar em registers nomeados)
  - Search (`/`, `?`, `n/N`, `*`, `#`)
  - Substitute (`:s/x/y/g`, flags, `:%s/.../.../gc`)
  - Undo/redo (u/<C-r>) + undotree
  - Buffers vs windows vs tabs (modelo mental + quando usar cada)
  - `:split`/`:vsplit`, `<C-w>` keymaps, `:bnext`/`:bprev`
  - Jump list (`<C-o>`/`<C-i>`)
  - `:help <tópico>` e descoberta (introdução; Telescope `<leader>fh` aparece em 04)
- **Não cobre:** Telescope buffer switcher (04), substitute global com quickfix (11), regex Vim avançada (Magus toca casualmente; fora do foco)
- **Verbetes referenciados:** buffer (se virar verbete), jump list, undotree

#### 04 — LazyVim tour
- **Slug:** `04 - LazyVim tour.md`
- **Primárias:**
  - [LazyVim docs](https://www.lazyvim.org/)
  - [LazyVim keymaps](https://www.lazyvim.org/keymaps)
  - [LazyVim starter](https://github.com/LazyVim/starter)
- **Secundárias:**
  - [LazyVim repo (Folke)](https://github.com/LazyVim/LazyVim)
  - [TJ DeVries — YouTube (Neovim from scratch series)](https://www.youtube.com/@teej_dv)
  - [LazyVim Discussions (padrões comuns da comunidade)](https://github.com/LazyVim/LazyVim/discussions)
- **Cobre:**
  - O que LazyVim é (distribuição), instalação do starter
  - Telescope: find files, live grep, buffers, help_tags, recent (`<leader>ff`, `<leader>fg`, `<leader>,`, `<leader>fh`, `<leader>fr`)
  - neo-tree (file explorer, `<leader>e`)
  - which-key (descoberta de keys com leader)
  - bufferline + statusline (o que mostra na tela)
  - LSP keys default (gd, gr, K, `<leader>ca`, `<leader>cr`, `<leader>cf`) — usar sem configurar
  - nvim-cmp (popup de auto-complete, Tab/`<CR>`/`<C-n>`/`<C-p>`)
  - Comment.nvim (`gcc`, `gc<motion>`)
  - nvim-surround (`ys{motion}<char>`, `cs<old><new>`, `ds<char>`)
  - Format on save (comportamento padrão — pode surpreender quem não sabe)
  - `:Lazy` interface básica (Sync/Update/Health)
- **Não cobre:** customização (08), adicionar plugin (08), Mason/LSP em detalhe (09), lazy.nvim como conceito (07)
- **Verbetes referenciados:** distribuição, LazyVim, Telescope, neo-tree, which-key, LSP, code action, format on save

### Fase Adepto (5 notas)

#### 05 — Lua para Neovim
- **Slug:** `05 - Lua para Neovim.md`
- **Primárias:**
  - [:help lua-guide](https://neovim.io/doc/user/lua-guide.html)
  - [:help lua](https://neovim.io/doc/user/lua.html)
  - [Lua 5.1 reference manual (LuaJIT é compatível com 5.1)](https://www.lua.org/manual/5.1/)
- **Secundárias:**
  - [Learn X in Y minutes — Lua](https://learnxinyminutes.com/docs/lua/)
  - [TJ DeVries — Neovim Lua intro (YouTube)](https://www.youtube.com/@teej_dv)
  - [kickstart.nvim (referência didática de config comentada)](https://github.com/nvim-lua/kickstart.nvim)
- **Cobre:**
  - Sintaxe Lua mínima (tabelas, funções, módulos, `require`, escopo, `local`)
  - O que Neovim adiciona: `vim.api`, `vim.fn`, `vim.opt`, `vim.keymap.set`, `vim.cmd`, `vim.uv`
  - Diferenças relevantes vs Vimscript (apenas o necessário pra ler configs alheias)
  - Strings, booleans, nil, truthiness em Lua (gotchas)
- **Não cobre:** Lua avançado (metatables, coroutines), referência completa de `vim.api`, escrever plugin do zero
- **Verbetes referenciados:** Lua, init.lua

#### 06 — Estrutura de config
- **Slug:** `06 - Estrutura de config.md`
- **Primárias:**
  - [LazyVim — Configuration general](https://www.lazyvim.org/configuration/general)
  - [LazyVim — File structure](https://www.lazyvim.org/configuration/general#file-structure)
  - [:help runtimepath](https://neovim.io/doc/user/options.html#'runtimepath')
- **Secundárias:**
  - [LazyVim starter README](https://github.com/LazyVim/starter)
  - [kickstart.nvim (referência didática)](https://github.com/nvim-lua/kickstart.nvim)
- **Cobre:**
  - Layout de `~/.config/nvim/` no LazyVim (`lua/config/{lazy,options,keymaps,autocmds}.lua`, `lua/plugins/`)
  - Ordem de carregamento (bootstrap → options → autocmds → plugins → keymaps)
  - Criar keymaps via `vim.keymap.set` (modos, opts, desc)
  - Opções via `vim.opt` (set vs setlocal, valores compostos)
  - Autocmds (when/why, augroup, exemplo de format on save customizado)
- **Não cobre:** lazy.nvim como manager (07), customização de plugins LazyVim (08), Lua básico (05)
- **Verbetes referenciados:** init.lua, autocmd, keymap, leader key

#### 07 — lazy.nvim
- **Slug:** `07 - lazy.nvim.md`
- **Primárias:**
  - [lazy.nvim repo](https://github.com/folke/lazy.nvim)
  - [lazy.folke.io — docs oficiais](https://lazy.folke.io/)
  - [Plugin spec reference](https://lazy.folke.io/spec)
- **Secundárias:**
  - [LazyVim — How plugins work](https://www.lazyvim.org/configuration/plugins)
  - [Awesome Neovim — plugins curados](https://github.com/rockerBOO/awesome-neovim)
- **Cobre:**
  - Plugin spec (URL, opts, config, init, keys, event, cmd, ft, dependencies)
  - Lifecycle e gatilhos de lazy-loading (event, cmd, ft, keys)
  - Interface `:Lazy` (Sync/Update/Health/Profile)
  - Lockfile (`lazy-lock.json`) e reprodutibilidade entre máquinas
  - Diferença entre `opts = {}` (passa pra `setup()`) vs `config = function() ... end` (controle total)
- **Não cobre:** customizar plugins do LazyVim (08), criar plugin próprio
- **Verbetes referenciados:** plugin manager, lazy.nvim, lazy-loading, plugin spec

#### 08 — Customizando LazyVim
- **Slug:** `08 - Customizando LazyVim.md`
- **Primárias:**
  - [LazyVim — Customize plugins](https://www.lazyvim.org/configuration/plugins)
  - [LazyVim — Extras](https://www.lazyvim.org/extras)
  - [LazyVim — Recipes](https://www.lazyvim.org/configuration/recipes)
- **Secundárias:**
  - [Folke dotfiles (exemplo real do autor)](https://github.com/folke/dot)
  - [LazyVim Discussions — padrões comuns](https://github.com/LazyVim/LazyVim/discussions)
- **Cobre:**
  - Adicionar plugin novo em `lua/plugins/<nome>.lua`
  - Override de `opts` de plugin existente (merge profundo via tabela)
  - Desabilitar plugin (`enabled = false`)
  - Override e criação de keymaps com `<leader>`
  - Habilitar Extras (linguagens, ferramentas, formatters)
  - Debugging de conflitos (`:Lazy profile`, `:checkhealth`)
- **Não cobre:** sair do LazyVim e usar starter próprio, criação de plugin do zero
- **Verbetes referenciados:** keymap, leader key, plugin spec, distribuição

#### 09 — LSP no Neovim
- **Slug:** `09 - LSP no Neovim.md`
- **Primárias:**
  - [LazyVim — LSP](https://www.lazyvim.org/configuration/lsp)
  - [nvim-lspconfig](https://github.com/neovim/nvim-lspconfig)
  - [mason.nvim](https://github.com/williamboman/mason.nvim)
  - [nvim-cmp](https://github.com/hrsh7th/nvim-cmp)
  - [conform.nvim (formatador padrão do LazyVim)](https://github.com/stevearc/conform.nvim)
- **Secundárias:**
  - [LSP spec oficial](https://microsoft.github.io/language-server-protocol/)
  - [TJ DeVries — LSP explained (YouTube)](https://www.youtube.com/@teej_dv)
- **Cobre:**
  - O que é LSP (cliente-servidor, capabilities, transporte JSON-RPC)
  - Mason (instalar/atualizar language servers e tools)
  - Config de server via `lspconfig` (override de settings, on_attach)
  - Completion via nvim-cmp (sources, mapping)
  - Format on save via conform.nvim (formatters por linguagem)
  - Keymaps default do LazyVim pra LSP (gd, gr, K, `<leader>ca`, `<leader>cr`, `<leader>cf`)
  - Diagnostic flow + virtual text + sign column
  - Troubleshooting (`:LspInfo`, `:Mason`, `:ConformInfo`, `:checkhealth lsp`)
- **Não cobre:** escrever language server (fora); null-ls/none-ls (depreciado — LazyVim usa conform+nvim-lint); nvim-dap (vai em 13)
- **Verbetes referenciados:** LSP, language server, Mason, nvim-lspconfig, nvim-cmp, code action, diagnostic, formatter, linter, format on save

### Fase Magus (4 notas)

#### 10 — Registers, marks, macros
- **Slug:** `10 - Registers, marks, macros.md`
- **Primárias:**
  - [:help registers](https://neovim.io/doc/user/change.html#registers)
  - [:help mark-motions](https://neovim.io/doc/user/motion.html#mark-motions)
  - [:help recording](https://neovim.io/doc/user/repeat.html#recording)
- **Secundárias:**
  - [Brian Storti — Vim registers](https://www.brianstorti.com/vim-registers/)
  - [ThePrimeagen — macros (YouTube)](https://www.youtube.com/@ThePrimeagen)
  - [Practical Vim — Drew Neil (caps. macros)](https://pragprog.com/titles/dnvim2/practical-vim-second-edition/)
- **Cobre:**
  - Classes de registers: named `a-z`, numbered `0-9`, sistema `+`/`*`, expression `=`, último search `/`, último comando `:`, black hole `_`
  - Uso prático: `"ay` (yank em a), `"ap` (paste de a), `"+y` (sistema)
  - Marks locais (`a-z`, scope buffer) vs globais (`A-Z`, scope cross-file)
  - `:marks`, `:Telescope marks`, jump a mark (`'a`, `` `a ``)
  - Gravando macro (`q<reg>...q`), executando (`@<reg>`, `@@`)
  - Editando macro como texto (yank do register, edita, paste de volta)
  - Macros aninhados/recursivos
- **Não cobre:** automation via plugin (Lua-equivalent), abuso de macros em vez de :substitute (mencionar como anti-pattern)
- **Verbetes referenciados:** register, mark, macro

#### 11 — Workflow avançado
- **Slug:** `11 - Workflow avançado.md`
- **Primárias:**
  - [:help quickfix](https://neovim.io/doc/user/quickfix.html)
  - [:help location-list](https://neovim.io/doc/user/quickfix.html#location-list)
  - [:help session-file](https://neovim.io/doc/user/starting.html#session-file)
- **Secundárias:**
  - [persistence.nvim (sessions no LazyVim)](https://github.com/folke/persistence.nvim)
  - [todo-comments.nvim](https://github.com/folke/todo-comments.nvim)
  - [Steve Losh — Learn Vimscript the Hard Way (clássico)](https://learnvimscriptthehardway.stevelosh.com/)
- **Cobre:**
  - Quickfix list vs location list (escopo global vs por window)
  - Populando via `:grep`/`:vimgrep`/Telescope `<C-q>` (send to qf)
  - Navegação: `:cnext`/`:cprev`/`:copen`/`:cclose`
  - Edição em massa: `:cdo s/x/y/g | update`, `:cfdo`
  - Refactoring pesado (LSP refs → quickfix → cdo)
  - Sessions com persistence.nvim (restore on enter, múltiplas sessions por projeto)
  - todo-comments integrado a quickfix (`:TodoQuickFix`)
- **Não cobre:** refactoring via Treesitter (12), debugging (13), macros (10)
- **Verbetes referenciados:** quickfix list

#### 12 — Treesitter avançado
- **Slug:** `12 - Treesitter avançado.md`
- **Primárias:**
  - [nvim-treesitter](https://github.com/nvim-treesitter/nvim-treesitter)
  - [nvim-treesitter-textobjects](https://github.com/nvim-treesitter/nvim-treesitter-textobjects)
  - [:help treesitter](https://neovim.io/doc/user/treesitter.html)
  - [Tree-sitter query language](https://tree-sitter.github.io/tree-sitter/using-parsers#pattern-matching-with-queries)
- **Secundárias:**
  - [TJ DeVries — Tree-sitter talks (YouTube)](https://www.youtube.com/@teej_dv)
  - [Treesitter playground / `:InspectTree`](https://github.com/nvim-treesitter/playground)
- **Cobre:**
  - O que Treesitter resolve (parser incremental, AST por linguagem, vs regex)
  - Textobjects ts-aware: `af`/`if` (função), `ac`/`ic` (classe), `aa`/`ia` (argumento)
  - Motion via textobjects: `]f`/`[f` (próxima/anterior função), `]c`/`[c` (classe)
  - Swap/move: `<leader>a`/`<leader>A`, `<leader>p`/`<leader>P`
  - Queries customizadas: escrever `.scm` em `~/.config/nvim/after/queries/<lang>/`
  - `:InspectTree` (visualizar AST), `:Inspect` (token highlight no cursor)
  - Override de highlight via query
- **Não cobre:** criar parser de linguagem nova (extremamente raro), refactoring via LSP (em 09)
- **Verbetes referenciados:** Treesitter, AST, query, text object

#### 13 — Snippets e DAP
- **Slug:** `13 - Snippets e DAP.md`
- **Primárias:**
  - [LuaSnip repo](https://github.com/L3MON4D3/LuaSnip)
  - [LuaSnip DOC.md](https://github.com/L3MON4D3/LuaSnip/blob/master/DOC.md)
  - [nvim-dap](https://github.com/mfussenegger/nvim-dap)
  - [nvim-dap-ui](https://github.com/rcarriga/nvim-dap-ui)
  - [DAP spec oficial](https://microsoft.github.io/debug-adapter-protocol/)
- **Secundárias:**
  - [friendly-snippets (catálogo)](https://github.com/rafamadriz/friendly-snippets)
  - [LazyVim Extras — Lang/Debug](https://www.lazyvim.org/extras)
  - [TJ DeVries — DAP overview (YouTube)](https://www.youtube.com/@teej_dv)
- **Cobre (snippets):**
  - Estrutura de snippet (trigger, tabstops `$1`, placeholders, choice, transformations)
  - LuaSnip básico: snippet em Lua puro vs vscode-style com friendly-snippets
  - Expansão integrada com nvim-cmp (Tab)
  - Criar snippet próprio (Lua e vscode JSON)
- **Cobre (DAP):**
  - Modelo cliente-servidor; adapter por linguagem
  - Habilitar Extras de Debug por linguagem no LazyVim
  - Breakpoints (`<leader>db`), conditional breakpoints
  - Step in/over/out, continue, restart
  - REPL e watch expressions
  - Reuso de `launch.json` (.vscode/) — interop com VS Code
  - dap-ui (layout de debug: scopes, breakpoints, stacks)
- **Não cobre:** escrever DAP adapter próprio, snippet engines alternativos (vsnip, snippy), debugging remoto avançado
- **Verbetes referenciados:** snippet, LuaSnip, DAP

## 6. Padrão estrutural por nota

Frontmatter:

```yaml
---
title: "<título sem prefixo numérico>"
type: concept
publish: true
fase: iniciado    # iniciado | adepto | magus
tags: [terminal, editor, <fase>, <conceito>]
created: 2026-05-19
updated: 2026-05-19
status: seedling
---
```

Estrutura do corpo:

```markdown
# <Título>

> [!abstract] TL;DR
> 2-4 linhas. Conceito + regra prática + por que importa.

## O que é / Como funciona

## Na prática
<exemplos concretos, configs, keymaps>

## Armadilhas
<2+ armadilhas reais>

## Em inglês
<5-10 termos PT → EN com curto exemplo de uso em frase técnica>

## Veja também
<wikilinks pra outras notas do galho + tronco + dicionário>

## Referências
<URLs das fontes primárias e secundárias da nota>
```

**Variações permitidas:**
- Nota 04 (LazyVim tour) usa sub-headings por área (Telescope, neo-tree, etc.) em "Na prática".
- Notas 12-13 (Magus densas) podem ter "Como funciona" dividido em sub-seções.
- MOC do galho tem estrutura própria (seção 5).

**Tamanho típico:** 200-400 linhas por nota Iniciado/Magus, 300-500 por nota Adepto (config tende a ser densa). Notas 04 e 13 podem chegar a 600 — aceitar, partir só se uma sub-seção ficar autônoma o suficiente pra virar nota independente (decisão na execução).

## 7. Dicionário e verbetes

### Localização e estrutura

**Caminho:** `03-Dominios/Terminal/Dicionário do Terminal.md` (no topo do domínio, segue o pattern de `Dicionário do Indie Hacker` e `Dicionário de React`).

**Frontmatter:**

```yaml
---
title: "Dicionário do Terminal"
type: glossary
publish: true
created: 2026-05-19
updated: <atualizado a cada inclusão>
tags: [terminal, glossary]
---
```

**Estrutura:** verbetes organizados por ordem alfabética dentro de blocos temáticos. Cada verbete é um header `## <Termo>` com 1-3 frases de definição + wikilink pra(s) nota(s) que aprofundam.

### Verbetes iniciais (Editor — ~30)

| Bloco temático | Verbetes |
|---|---|
| **Vim/Neovim core** | modal editing, modo (normal/insert/visual/visual-line/visual-block/command/terminal), motion, operador, text object, register, mark, macro, jump list, quickfix list, undotree, leader key, keymap, autocmd |
| **Ecossistema LazyVim** | distribuição, LazyVim, plugin manager, lazy.nvim, lazy-loading, plugin spec, Telescope, neo-tree, which-key, Treesitter, AST, query |
| **LSP & dev** | LSP, language server, Mason, nvim-lspconfig, nvim-cmp, code action, diagnostic, formatter, linter, format on save |
| **Avançado** | snippet, LuaSnip, DAP, Lua, init.lua |

### Workflow durante a escrita

1. Cada vez que uma nota usa um termo jargão, linka como `[[Dicionário do Terminal#LSP|LSP]]`.
2. Termo sem verbete → criar na hora (usar skill `/verbete`).
3. Verbete sempre referencia, em "Veja também" do próprio verbete, a(s) nota(s) que aprofundam.
4. O spec lista, por nota, **quais verbetes ela referencia** (seção 5) — ajuda a manter cobertura.

## 8. Versões assumidas

| Componente | Versão | Política |
|---|---|---|
| **Neovim** | 0.10+ stable | Notas mencionam features 0.11 quando relevante, marcadas como "Neovim 0.11+". |
| **LazyVim** | `main` em 2026-05-19 (versão exata gravada no MOC do galho na execução) | LazyVim evolui rápido — declarar versão no MOC do galho; revisar `updated` das notas quando shift major acontecer. |
| **lazy.nvim** | latest | Reprodutibilidade via `lazy-lock.json` (mencionar em 07). |
| **LuaJIT** | bundled com Neovim | Lua 5.1-compatible (mencionar em 05). |

Mudanças do LazyVim que afetam notas específicas (ex: `null-ls` → `none-ls` → `conform.nvim + nvim-lint`) são tratadas como *revisões pontuais* da nota afetada, não rewrite do galho.

## 9. Fontes globais

Referências usadas em múltiplas notas (não repetir nas notas individuais; linkar pelo dicionário ou pela bibliografia desta seção):

- **Neovim docs:** https://neovim.io/doc/
- **LazyVim docs:** https://www.lazyvim.org/
- **lazy.nvim docs:** https://lazy.folke.io/
- **Awesome Neovim:** https://github.com/rockerBOO/awesome-neovim
- **TJ DeVries (YouTube):** https://www.youtube.com/@teej_dv (core contributor; melhor canal pra Neovim em profundidade)
- **ThePrimeagen (YouTube):** https://www.youtube.com/@ThePrimeagen (foco workflow + entretenimento)
- **/r/neovim:** https://www.reddit.com/r/neovim/ (comunidade ativa)
- **Folke (autor LazyVim, lazy.nvim, persistence, todo-comments, which-key):** https://github.com/folke
- **kickstart.nvim:** https://github.com/nvim-lua/kickstart.nvim (referência didática)

## 10. Decisões editoriais

- **Idioma:** PT-BR. Termos técnicos em inglês mantidos (motion, plugin, buffer, register).
- **Enquadramento:** domínio pessoal — sem seção "Em entrevista", sem rota de entrevista no MOC. Cada nota tem seção "Em inglês" (mini-glossário PT→EN dos termos-chave) pra fluência em discussões técnicas (PR review, pair programming, docs).
- **Ordem de implementação:** por fase (Iniciado → Adepto → Magus), sequencial 01→13.
- **LazyVim primário:** o caminho real do usuário. Iniciado/Adepto demonstram coisas com LazyVim ligado. Vim/Neovim core aparece quando o conceito é universal (modal editing, motions) e em Magus.
- **Tom:** técnico mas acessível; TL;DR sempre presente; "Na prática" tem config/keymap copiável.
- **Wikilinks:** densidade alta entre as 13 notas + verbetes do dicionário + tronco Terminal.
- **Code samples:** Lua quando configura, comandos Neovim/Ex quando opera. Sample sempre testado localmente antes do close.

## 11. Rotas alternativas no MOC

Além da sequência 01→13, o MOC oferece 3 rotas curtas pra entradas focadas:

| Rota | Sequência | Para quem |
|---|---|---|
| **Uso diário** *(toda Iniciado)* | 01 → 02 → 03 → 04 | "Quero usar LazyVim como editor primário esta semana sem configurar nada." |
| **Customização** | 04 → 06 → 07 → 08 | "LazyVim funciona, mas quero parar de copiar config alheia e entender o que mexo." Pula Lua puro (05) — leitor aprende por imersão. |
| **Produtividade avançada** | 02 → 10 → 11 → 12 | "Já uso bem, agora quero multiplicar velocidade." Foco em técnicas Magus que não dependem de config. |

## 12. Critérios de aprovação

O galho está pronto quando:

1. **14 arquivos** existem em `03-Dominios/Terminal/Editor/`: 13 notas atômicas + 1 MOC do galho.
2. **Dicionário do Terminal** criado em `03-Dominios/Terminal/Dicionário do Terminal.md` com pelo menos **30 verbetes** cobrindo o jargão usado nas notas.
3. **Todos os arquivos** com `publish: true`, `fase` declarada (notas) ou `type: glossary` (dicionário) ou `type: moc` (MOC), tags consistentes.
4. **MOC do galho** tem:
   - TL;DR em `[!abstract]`
   - Seções `## Iniciado` / `## Adepto` / `## Magus` agrupando as 13 notas em ordem
   - Seção `## Rotas alternativas` com as 3 rotas curtas
   - "Veja também" com wikilinks pro tronco Terminal e pro Dicionário
5. **Cada nota satisfaz a rubrica:**
   - TL;DR em `[!abstract]`
   - 2+ wikilinks pra outras notas do galho + 1+ pro tronco ou MOC do galho
   - 2+ exemplos práticos concretos (config, keymap, comando)
   - Seção "Em inglês" com 5-10 termos PT→EN + 1 frase de uso por termo
   - Seção "Armadilhas" com 2+ casos concretos (não genéricos)
   - Wikilinks pros verbetes apropriados do dicionário (lista no spec, seção 5)
   - Frontmatter completo (`publish: true`, `status: seedling`, `fase`, tags)
   - PT-BR natural; termos técnicos em inglês mantidos
   - **Zero atribuição de experiência pessoal fabricada** ao autor
6. **Tronco** `03-Dominios/Terminal/index.md` atualizado: bullet do Editor vira wikilink ativo `[[03-Dominios/Terminal/Editor/index|Editor]]`.
7. **Quartz publica** corretamente em josenaldo.github.io (rodar build local antes do close).
8. **Pelo menos 4 notas** com config/keymap testado localmente (rodar a config no `~/.config/nvim/` e validar que carrega sem erro).

## 13. Riscos e mitigações

| Risco | Mitigação |
|---|---|
| **LazyVim evolui rápido** — plugin default muda, keymap default mexe | Declarar versão exata do LazyVim no MOC do galho na sessão de execução. Quando shift major acontecer, revisão em batch das notas afetadas; não rewrite. |
| **Sobreposição 04 (tour) com 08 (custom) e 09 (LSP)** | Regra dura: 04 mostra o que vem ligado e como usar — não configura nada. Configuração é exclusivamente Adepto. Quando algo precisa de explicação de "por que existe", 04 linka pra 08/09. |
| **Notas muito grandes (04 e 13)** | Aceitar 500-600 linhas; partir só se uma sub-seção ficar autônoma o suficiente pra virar nota independente. Decidir na execução. |
| **Confusão Vim core vs Neovim vs LazyVim** | Convenção visual nos exemplos: `[LazyVim default]`, `[Neovim core]`, `[Vim heritage]` quando ambíguo. Verbete "distribuição" cobre o modelo. |
| **"Em inglês" com PT-anglicismos** | Termos técnicos consagrados ficam em inglês (motion, plugin, buffer). Tradução PT só pra conceitos com tradução estável (modo, registrador). Dicionário valida. |
| **Verbetes criados mas não linkados nas notas** | Spec lista, por nota, quais verbetes referencia. Checklist de execução verifica wikilink-coverage por nota antes do close. |
| **Code samples / configs envelhecendo** | Testar localmente antes de publicar (critério #8). `:checkhealth` no fim. Issue de revisão quando uma config quebrar. |
| **Notas genéricas ("tutorial qualquer de Vim")** | "Armadilhas" tem 2+ casos concretos por nota. "Na prática" tem config real (não pseudocódigo). Spec proíbe sample inventado — só config testada ou copiada da fonte primária. |
| **Quartz publish quebra** — frontmatter inválido, wikilink quebrado | Build local do Quartz como passo do critério #7. Skill `/verificar-wikilinks` ou equivalente antes do close. |
| **Dicionário inchando além do Editor** | OK — é trilha-wide. Outros galhos vão adicionar. Manter ordenação alfabética dentro de blocos temáticos. |

## 14. Plano de execução

O plano detalhado de execução vai em `docs/superpowers/plans/2026-05-19-terminal-editor-execution.md` (gerado pela skill `superpowers:writing-plans` após aprovação deste spec).

Ordem de execução recomendada (sumária — detalhe no plano):

1. MOC esqueleto + Dicionário esqueleto (frontmatter + estrutura, sem conteúdo)
2. Fase Iniciado: 01 → 02 → 03 → 04 (com verbetes criados conforme aparecem)
3. Fase Adepto: 05 → 06 → 07 → 08 → 09
4. Fase Magus: 10 → 11 → 12 → 13
5. Pass final no MOC (wikilinks ativos)
6. Pass final no Dicionário (alfabetização + Veja também por verbete)
7. Atualizar tronco `Terminal/index.md` ativando wikilink do Editor
8. Build local do Quartz + validação de wikilinks
9. Commit final do galho

## 15. Documentos relacionados

- `2026-05-18-trilha-terminal-design.md` — roadmap macro da trilha (este spec é galho #1)
- `2026-05-07-node-runtime-event-loop-design.md` — spec de referência (galho de outra trilha, formato análogo)
- Plano de execução (criado a seguir): `2026-05-19-terminal-editor-execution.md`
- Tronco: `03-Dominios/Terminal/index.md`
- Dicionário a criar: `03-Dominios/Terminal/Dicionário do Terminal.md`
