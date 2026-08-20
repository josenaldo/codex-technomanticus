---
title: "Estrutura de config"
created: 2026-05-19
updated: 2026-05-19
type: concept
progress: backlog
status: seedling
publish: true
fase: Adepto
tags:
  - terminal
  - editor
  - adepto
  - config
  - lazyvim
aliases:
  - Estrutura de config
  - Layout LazyVim
---

# Estrutura de config

> [!abstract] TL;DR
> LazyVim organiza config em pastas: `lua/config/` pra options/keymaps/autocmds/bootstrap, e `lua/plugins/` pra plugins. Saber a ordem de carregamento é o que destrava a confusão "onde colocar isto?". Leader deve ser definido antes dos plugins; keymaps globais depois; autocmds e options no meio.

## O que é / Como funciona

### Layout do `~/.config/nvim/`

A raiz da config Neovim com LazyVim segue uma estrutura canônica. Entender cada arquivo e seu papel elimina boa parte das dúvidas de "onde vai isso?":

```
~/.config/nvim/
├── init.lua                    # entry point — require("config.lazy")
├── lua/
│   ├── config/
│   │   ├── lazy.lua            # bootstrap do lazy.nvim, leader, imports
│   │   ├── options.lua         # vim.opt.* (carregado antes dos plugins)
│   │   ├── autocmds.lua        # vim.api.nvim_create_autocmd
│   │   └── keymaps.lua         # vim.keymap.set (carregado após plugins)
│   └── plugins/                # 1 arquivo por plugin ou grupo
│       ├── editor.lua
│       ├── lsp.lua
│       └── ...
└── lazy-lock.json              # versões fixadas (commit no git)
```

Cada arquivo tem responsabilidade única. Isso não é burocracia — é o que garante que a [[Dicionário do Terminal#Leader key|leader key]] já exista quando o plugin que usa `<leader>X` for registrado.

---

### Ordem de carregamento

O LazyVim define uma ordem precisa. Entender essa sequência é o que separa quem sabe o que está fazendo de quem tenta ao acaso:

1. **`init.lua`** — chama `require("config.lazy")`. Não faz mais nada.
2. **`config/lazy.lua`** — define `vim.g.mapleader` (obrigatório ANTES do `require("lazy")`), depois chama o bootstrap do lazy.nvim.
3. **`config/options.lua`** — carrega opções de editor (`vim.opt.*`). Roda antes dos plugins.
4. **`config/autocmds.lua`** — registra [[Dicionário do Terminal#Autocmd|autocmds]]. Roda antes dos plugins.
5. **lazy.nvim** — importa todos os arquivos em `lua/plugins/*.lua`, resolve dependências, carrega os plugins.
6. **`config/keymaps.lua`** — registra [[Dicionário do Terminal#Keymap|keymaps]] globais. Roda por último porque alguns atalhos dependem de plugins já carregados.

Essa ordem é configurada dentro de `lazy.lua` via `import` e é a mesma para qualquer instalação LazyVim padrão.

---

### `init.lua` — o entry point

O arquivo `~/.config/nvim/init.lua` no LazyVim é intencionalmente minúsculo:

```lua
-- ~/.config/nvim/init.lua
require("config.lazy")
```

É só isso. O trabalho real está em `lua/config/lazy.lua`. A separação existe por clareza: `init.lua` é o ponto de entrada; `lazy.lua` é onde o bootstrap vive.

---

### `lua/config/lazy.lua` — bootstrap e leader

Este é o arquivo mais crítico da sequência. Ele faz três coisas na ordem certa:

```lua
-- lua/config/lazy.lua

-- 1. Leader ANTES de qualquer plugin
vim.g.mapleader = " "
vim.g.maplocalleader = ","

-- 2. Bootstrap do lazy.nvim (instala se ausente)
local lazypath = vim.fn.stdpath("data") .. "/lazy/lazy.nvim"
if not vim.loop.fs_stat(lazypath) then
  vim.fn.system({
    "git", "clone", "--filter=blob:none",
    "https://github.com/folke/lazy.nvim.git",
    "--branch=stable", lazypath,
  })
end
vim.opt.rtp:prepend(lazypath)

-- 3. Inicializa lazy.nvim e importa plugins + config
require("lazy").setup({
  spec = {
    { "LazyVim/LazyVim", import = "lazyvim.plugins" },
    { import = "plugins" },
  },
  defaults = { lazy = false },
  install = { colorscheme = { "tokyonight", "habamax" } },
  -- LazyVim importa automaticamente lua/config/options, autocmds, keymaps
  -- via events internos — não precisa de require explícito aqui
})
```

A definição do `mapleader` no topo não é opcional. Se você mover pra depois do `require("lazy").setup`, plugins que declaram `keys = { "<leader>X" }` no spec vão capturar `\` (o default do Vim) em vez de `<Space>`.

---

### `lua/config/options.lua` — `vim.opt.*`

Aqui vivem todas as opções de comportamento e aparência do editor. Carrega antes dos plugins, então não depende de nada externo:

```lua
-- lua/config/options.lua

-- Aparência
vim.opt.number = true
vim.opt.relativenumber = true
vim.opt.cursorline = true
vim.opt.signcolumn = "yes"

-- Indentação
vim.opt.expandtab = true
vim.opt.shiftwidth = 2
vim.opt.tabstop = 2
vim.opt.smartindent = true

-- UX
vim.opt.wrap = false
vim.opt.scrolloff = 8
vim.opt.splitright = true
vim.opt.splitbelow = true
vim.opt.colorcolumn = "100"  -- string, não number (ver Armadilhas)
```

**`vim.opt` vs `vim.opt_local`:** `vim.opt.X = valor` é global (vale pra todos os buffers). `vim.opt_local.X = valor` é buffer-local — útil dentro de autocmds com `FileType` pra aplicar opções só em certos tipos de arquivo.

**Valores compostos:** opções como `listchars` e `wildmode` aceitam tabela com `:append`/`:remove`:

```lua
vim.opt.listchars:append({ tab = "→ ", trail = "·", eol = "¬" })
```

---

### `lua/config/autocmds.lua` — eventos e callbacks

Autocmds executam código em resposta a eventos do Neovim. O padrão correto usa `augroup` com `clear = true` para evitar duplicação ao recarregar a config:

```lua
-- lua/config/autocmds.lua

-- Grupo com clear = true evita duplicação ao :source
local augroup = vim.api.nvim_create_augroup

-- Highlight ao yankar
vim.api.nvim_create_autocmd("TextYankPost", {
  group = augroup("YankHighlight", { clear = true }),
  callback = function()
    vim.highlight.on_yank({ timeout = 200 })
  end,
})

-- Remover trailing whitespace ao salvar
vim.api.nvim_create_autocmd("BufWritePre", {
  group = augroup("TrimWhitespace", { clear = true }),
  callback = function()
    local cursor = vim.api.nvim_win_get_cursor(0)
    vim.cmd([[%s/\s\+$//e]])
    vim.api.nvim_win_set_cursor(0, cursor)
  end,
})
```

**Eventos comuns:**

| Evento | Quando dispara |
|---|---|
| `BufWritePre` | Antes de salvar (pré-save) |
| `BufWritePost` | Depois de salvar |
| `FileType` | Quando o tipo de arquivo é detectado |
| `VimEnter` | Após Neovim inicializar completamente |
| `TextYankPost` | Após um yank (`y`, `d`, `c`) |
| `InsertLeave` | Ao sair do modo insert |
| `BufReadPost` | Após ler um arquivo no buffer |

O campo `pattern` filtra por arquivo — `pattern = "*.lua"` ou `pattern = "markdown"` (com FileType, o pattern é o filetype, não glob). O campo `callback` recebe uma função Lua; ou `command` recebe string de comando Ex.

---

### `lua/config/keymaps.lua` — mapeamentos globais

Keymaps globais (que não pertencem a nenhum plugin específico) ficam aqui. Carregam depois dos plugins:

```lua
-- lua/config/keymaps.lua
local map = vim.keymap.set

-- Navegação entre windows
map("n", "<C-h>", "<C-w>h", { desc = "Go to left window" })
map("n", "<C-j>", "<C-w>j", { desc = "Go to lower window" })
map("n", "<C-k>", "<C-w>k", { desc = "Go to upper window" })
map("n", "<C-l>", "<C-w>l", { desc = "Go to right window" })

-- Utilitários
map("n", "<leader>so", "<cmd>source %<CR>", { desc = "Source current file" })
map("n", "<Esc>", "<cmd>nohlsearch<CR>", { desc = "Clear search highlight" })
```

**Assinatura de `vim.keymap.set`:**

```
vim.keymap.set(mode, lhs, rhs, opts)
```

- `mode`: string ou tabela — `"n"`, `"i"`, `"v"`, `"x"`, `"t"`, `"c"`, `""` (todos), ou `{"n", "v"}`.
- `lhs`: a sequência de teclas que você pressiona (ex: `"<leader>w"`, `"jk"`).
- `rhs`: a ação — string de teclas/comando (`"<cmd>w<CR>"`) ou função Lua.
- `opts`: tabela com `desc` (visível no which-key), `silent` (sem echo), `noremap` (default `true` em `vim.keymap.set` — diferente de `nvim_set_keymap`).

---

### `lua/plugins/` — specs de plugin

Cada arquivo em `lua/plugins/` deve retornar uma tabela (ou lista de tabelas). LazyVim importa todos automaticamente:

```lua
-- lua/plugins/editor.lua
return {
  -- Override de opção do which-key
  {
    "folke/which-key.nvim",
    opts = { delay = 500 },
  },
  -- Novo plugin adicionado
  {
    "echasnovski/mini.surround",
    opts = {},
  },
}
```

Arquivos em `lua/plugins/` são o local certo pra:
- Adicionar novos plugins.
- Fazer override de plugins que LazyVim já inclui (basta repetir o mesmo `"user/repo"` com as opções que quer mudar).
- Desabilitar um plugin default do LazyVim (campo `enabled = false`).

Tudo que é específico de um plugin vai aqui — não em `keymaps.lua` nem em `autocmds.lua`.

---

## Na prática

### Keymap simples em `keymaps.lua`

```lua
-- lua/config/keymaps.lua
vim.keymap.set("n", "<leader>so", "<cmd>source %<CR>",
  { desc = "Source current file" })
```

### Options customizadas em `options.lua`

```lua
-- lua/config/options.lua
vim.opt.wrap = true
vim.opt.linebreak = true
vim.opt.colorcolumn = "100"   -- string, não number
```

### Autocmd: highlight yank

```lua
-- lua/config/autocmds.lua
vim.api.nvim_create_autocmd("TextYankPost", {
  group = vim.api.nvim_create_augroup("YankHighlight", { clear = true }),
  callback = function()
    vim.highlight.on_yank({ timeout = 200 })
  end,
})
```

### Option buffer-local via autocmd (wrap só em Markdown)

```lua
-- lua/config/autocmds.lua
vim.api.nvim_create_autocmd("FileType", {
  pattern = "markdown",
  callback = function()
    vim.opt_local.wrap = true
    vim.opt_local.linebreak = true
  end,
})
```

### Verificar o que está carregado

```vim
:Lazy          " abre UI do lazy.nvim — mostra plugins, versões, logs
:messages      " mostra histórico de mensagens/erros do Neovim
:checkhealth   " diagnóstico completo de plugins e dependências
```

---

## Armadilhas comuns

> [!warning] Leader definido tarde demais
> Se `vim.g.mapleader` for setado em `keymaps.lua` (que carrega depois dos plugins), plugins que declaram `keys = { "<leader>X" }` no spec capturam `\` (o default do Vim) em vez de `<Space>`. **Setar em `lazy.lua` antes de `require("lazy")`** — essa é a única posição segura.

> [!warning] `lua/plugins/<arquivo>.lua` deve retornar uma tabela
> Sem `return { ... }` no final, o plugin não carrega e o lazy.nvim não emite erro óbvio — simplesmente ignora o arquivo. O symptom é o plugin não aparecer em `:Lazy`. Sempre termine com `return { ... }`.

> [!warning] Autocmd duplicado sem augroup
> Sem `augroup` com `clear = true`, toda vez que você recarrega a config (`:source %` em `autocmds.lua` ou reinicia Neovim), o autocmd é registrado novamente. Resultado: o callback dispara N vezes (format-on-save roda duas vezes, notify aparece em duplicata, etc.). `{ clear = true }` limpa o grupo antes de repopular.

> [!warning] `vim.opt.colorcolumn = 100` (number)
> Vai dar erro silencioso. A opção `colorcolumn` espera string: `"100"` ou `"80,100,120"`. Erros silenciosos como esse aparecem em `:messages` — consulte quando algo não funcionar sem mensagem de erro visível.

> [!warning] Keymap que depende de plugin em `options.lua`
> `options.lua` carrega antes dos plugins. Se você colocar um keymap que chama uma função de plugin nesse arquivo, ela não vai existir ainda e o keymap falha silenciosamente (ou pior, com erro na inicialização). Keymaps que dependem de plugins vão em `lua/plugins/<plugin>.lua` no campo `keys`, ou em `config/keymaps.lua` com guard `pcall`.

---

## Em inglês

| PT-BR | EN | Uso técnico |
|---|---|---|
| caminho de carregamento | load path / runtimepath | `vim.opt.rtp` — list of dirs Neovim searches |
| inicialização | startup | the sequence from `init.lua` to first buffer |
| opção global | global option | `vim.opt.X` — applies to all buffers |
| buffer-local | buffer-local | `vim.opt_local.X` — applies only to current buffer |
| atalho | mapping / keymap | `vim.keymap.set(mode, lhs, rhs, opts)` |
| descrição | description | `desc` field in opts — shown in which-key |
| tecla líder | leader key | `vim.g.mapleader` — prefix for custom mappings |
| grupo de autocmd | augroup | `vim.api.nvim_create_augroup(name, { clear = true })` |
| comando ex | Ex command | `:w`, `:source`, `:Lazy` — colon-prefixed commands |
| evento | event | `BufWritePre`, `FileType`, `TextYankPost`, etc. |
| versões fixadas | pinned versions / lock file | `lazy-lock.json` — reproducible installs |

---

## Veja também

- [[05 - Lua para Neovim]] — sintaxe Lua e API `vim.*` que aparece nesta nota
- [[07 - lazy.nvim]] — spec de plugin em profundidade: `event`, `keys`, `dependencies`
- [[08 - Customizando LazyVim]] — override de plugins e extras vem desta estrutura
- [[04 - LazyVim tour]] — onde os keymaps default do LazyVim vivem
- [[03-Dominios/Tecnologia/Terminal/Editor/index|MOC do galho]]
- [[Dicionário do Terminal#Autocmd|autocmd]], [[Dicionário do Terminal#Keymap|keymap]], [[Dicionário do Terminal#Leader key|leader key]], [[Dicionário do Terminal#init.lua|init.lua]]

---

## Referências

- [LazyVim — General Configuration](https://www.lazyvim.org/configuration/general)
- [LazyVim — File Structure](https://www.lazyvim.org/configuration/general#file-structure)
- [Neovim — runtimepath](https://neovim.io/doc/user/options.html#'runtimepath')
- [LazyVim starter template](https://github.com/LazyVim/starter)
- [kickstart.nvim](https://github.com/nvim-lua/kickstart.nvim) — config template comentado, alternativa ao LazyVim para quem quer controle total
