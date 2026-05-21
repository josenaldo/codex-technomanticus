---
title: "Lua para Neovim"
created: 2026-05-19
updated: 2026-05-19
type: concept
status: seedling
publish: true
fase: adepto
tags:
  - terminal
  - editor
  - adepto
  - lua
  - neovim
aliases:
  - Lua
  - Lua no Neovim
---

# Lua para Neovim

> [!abstract] TL;DR
> Neovim usa Lua como linguagem de config — especificamente LuaJIT, compatível com Lua 5.1. A linguagem em si é minúscula: tabelas, funções, módulos e alguns operadores. O que demanda mais atenção é a API `vim.*` que o Neovim expõe pro editor. Ler config alheia fica fácil em poucas horas; escrever plugin do zero é outra história.

## O que é / Como funciona

### Por que Lua?

Neovim adotou Lua como linguagem de scripting de primeira classe a partir da versão 0.5 (2021). Antes disso, configuração era feita em Vimscript — uma linguagem específica do Vim, com sintaxe própria e pouco reaproveitamento de conhecimento. Lua resolve isso:

- **Embutida via LuaJIT** — compilada junto com o Neovim, sem instalação extra.
- **Minimalista** — a spec completa da linguagem cabe em ~100 páginas. Um dev experiente lê config de qualquer plugin em minutos.
- **API rica** — `vim.*` expõe opções, keymaps, autocmds, buffers, janelas e IO assíncrono com libuv.
- **Ecosistema crescente** — quase todos os plugins modernos são escritos em Lua; repos como `kickstart.nvim` servem como template comentado.

O objetivo desta nota **não é escrever plugin do zero**. É ler e escrever configuração pessoal — [[Dicionário do Terminal#init.lua|init.lua]], specs de plugin, overrides de LazyVim.

---

### Lua minimal — o que você precisa saber

#### Tipos

Lua tem seis tipos primitivos relevantes pra config:

| Tipo | Exemplo | Observação |
|---|---|---|
| `nil` | `nil` | Ausência de valor. Única forma de "apagar" variável |
| `boolean` | `true`, `false` | — |
| `number` | `42`, `3.14` | Sem distinção int/float |
| `string` | `"hello"`, `'world'` | Imutável. Concat com `..` |
| `table` | `{ 1, 2, 3 }` | Único container da linguagem |
| `function` | `function() end` | First-class — passa como argumento, retorna de função |

Não há: array, map, set, class, struct. Tudo é tabela.

#### Variáveis e escopo

```lua
-- Variável local (preferida — escopo léxico)
local x = 1
local msg = "hello"

-- Global (evitar em config)
y = 99  -- polui namespace global
```

Use `local` em tudo. Em config compartilhada ou multi-arquivo, global vaza entre módulos.

#### Funções

```lua
-- Definição padrão
local function soma(a, b)
  return a + b
end

-- Função anônima atribuída a local (equivalente)
local soma = function(a, b)
  return a + b
end

-- Passando função como argumento (comum em callbacks de autocmd/keymap)
local resultado = soma(2, 3)  -- 5
```

Funções são first-class: você as passa como callbacks pro `vim.keymap.set`, `vim.api.nvim_create_autocmd`, specs de plugin, etc.

#### Tabelas

A tabela é o único container de Lua. Ela assume os três papéis abaixo conforme o uso:

```lua
-- Array (1-indexed)
local lista = { "neovim", "lua", "treesitter" }
print(lista[1])   -- "neovim" (índice começa em 1, não 0)
print(#lista)     -- 3

-- Dict (chave string → valor)
local config = { theme = "tokyonight", number = true }
print(config.theme)        -- "tokyonight"  (açúcar sintático)
print(config["theme"])     -- "tokyonight"  (equivalente)

-- Misto (raro, evitar em config — leiaute imprevisível)
local misto = { "a", chave = "b", "c" }
```

**Regra prática:** se todos os valores são indexados por inteiro sequencial → array. Se todos têm chave string → dict. Não misture.

#### Truthiness

Em Lua, **somente `false` e `nil` são falsy**. Todo o resto é truthy:

```lua
if 0 then print("truthy") end      -- imprime (0 é truthy em Lua!)
if "" then print("truthy") end     -- imprime ("" é truthy em Lua!)
if {} then print("truthy") end     -- imprime ({} é truthy em Lua!)
if nil then print("truthy") end    -- não imprime
if false then print("truthy") end  -- não imprime
```

Vindo de JavaScript ou Python, `if x then` com `x = 0` vai te surpreender. Pra checar "vazio" use `x == nil` ou `x == 0` explicitamente.

#### Operadores

| Operação | Lua | Lua ≠ JS/Python |
|---|---|---|
| Igualdade | `==` | igual |
| Desigualdade | `~=` | JS usa `!=`, Python usa `!=` |
| Negação lógica | `not` | JS usa `!`, Python usa `not` |
| E lógico | `and` | JS usa `&&` |
| Ou lógico | `or` | JS usa `\|\|` |
| Concatenação | `..` | JS usa `+`, Python usa `+` |

```lua
local a = "foo"
local b = "bar"
print(a .. b)       -- "foobar"
print(a ~= b)       -- true
print(not false)    -- true
```

#### Módulos e require

```lua
-- Carrega módulo (busca em runtimepath — ~/.config/nvim/lua/)
local M = require("meu_modulo")

-- Um módulo é apenas um arquivo Lua que retorna um valor
-- lua/meu_modulo.lua:
local M = {}
M.setup = function(opts) end
return M
```

`require` usa cache — rodar duas vezes retorna o mesmo objeto. Para recarregar em dev: `package.loaded["nome"] = nil; require("nome")`.

---

### API Neovim — `vim.*`

A maior curva de aprendizado não é a linguagem Lua, mas a API que o Neovim expõe. Os namespaces que aparecem em toda config:

#### `vim.opt` — opções do editor

```lua
vim.opt.number = true           -- :set number
vim.opt.relativenumber = true   -- :set relativenumber
vim.opt.expandtab = true        -- :set expandtab
vim.opt.shiftwidth = 2          -- :set shiftwidth=2
vim.opt.wrap = false            -- :set nowrap

-- Opções de lista (append/remove)
vim.opt.listchars:append({ tab = "→ ", trail = "·" })
```

`vim.opt` aceita operações compostas (`:append`, `:remove`, `:prepend`) e tabelas Lua como valor. Diferente de `vim.o` que só aceita string/bool/number.

#### `vim.g` — variáveis globais (globals de Vim)

```lua
vim.g.mapleader = " "       -- :let g:mapleader = " "
vim.g.maplocalleader = ","  -- :let g:maplocalleader = ","
```

`vim.g.mapleader` deve ser definido **antes** de qualquer `require` de plugin manager — LazyVim espera isso no topo do `init.lua`.

#### `vim.keymap.set` — keymaps

```lua
-- vim.keymap.set(modo, lhs, rhs, opts)
vim.keymap.set("n", "<leader>w", "<cmd>w<CR>", { desc = "Salvar" })
vim.keymap.set("i", "jk", "<Esc>", { desc = "Escape rápido" })

-- rhs como função (callback inline)
vim.keymap.set("n", "<leader>rs", function()
  vim.cmd("source %")
  vim.notify("Sourced!")
end, { desc = "Re-source current file" })
```

Modos: `"n"` (normal), `"i"` (insert), `"v"` (visual), `"x"` (visual sem select), `"t"` (terminal), `"c"` (command-line), `""` (todos).

#### `vim.api.*` — API de baixo nível

```lua
-- Autocmd: formatar ao salvar
vim.api.nvim_create_autocmd("BufWritePre", {
  pattern = "*.lua",
  callback = function()
    vim.lsp.buf.format()
  end,
})

-- Grupo de autocmds (evita duplicata ao re-source)
local group = vim.api.nvim_create_augroup("MeuGrupo", { clear = true })
vim.api.nvim_create_autocmd("FileType", {
  group = group,
  pattern = "markdown",
  callback = function()
    vim.opt_local.wrap = true
  end,
})
```

`vim.api.nvim_create_augroup` com `{ clear = true }` limpa o grupo se ele existir — evita duplicação ao recarregar config.

#### `vim.fn.*` — funções Vimscript

```lua
local path = vim.fn.expand("%:p")    -- caminho absoluto do arquivo atual
local line = vim.fn.line(".")        -- número da linha atual
local exists = vim.fn.filereadable("~/.config/nvim/init.lua")
```

`vim.fn` chama funções do Vimscript diretamente. Útil quando a operação não tem equivalente em `vim.api`.

#### `vim.cmd` — comandos Ex

```lua
vim.cmd("colorscheme tokyonight")
vim.cmd("set number")

-- Bloco multi-linha (here-string)
vim.cmd([[
  highlight Normal guibg=NONE
  highlight NonText guibg=NONE
]])
```

Útil para colar snippets de Vimscript em config Lua sem reescrita completa.

#### `vim.uv` — libuv (IO assíncrono)

```lua
-- Alias pra vim.loop (deprecated) — use vim.uv
local timer = vim.uv.new_timer()
timer:start(1000, 0, function()
  vim.schedule(function()
    print("1 segundo depois")
  end)
end)
```

Raro em config pessoal. Aparece em plugins que fazem operações de filesystem ou timers sem bloquear o editor.

---

### Vimscript vs Lua — leitura de configs alheias

Você vai encontrar snippets mistos online. Tabela de equivalências rápidas:

| Vimscript | Lua equivalente |
|---|---|
| `let g:x = 1` | `vim.g.x = 1` |
| `set number` | `vim.opt.number = true` |
| `nnoremap <leader>w :w<CR>` | `vim.keymap.set("n", "<leader>w", "<cmd>w<CR>")` |
| `function! Foo()` | `local function Foo()` |
| `autocmd BufWritePre * lua vim.lsp.buf.format()` | `vim.api.nvim_create_autocmd(...)` |

Vimscript ainda funciona via `vim.cmd([[...]])`. Para snippets antigos que não vale reescrever, isso é suficiente.

---

### Lendo uma spec de plugin LazyVim

Pra ler config alheia, entender o formato de plugin spec do lazy.nvim é essencial (a nota [[07 - lazy.nvim]] aprofunda, mas o básico é aqui):

```lua
return {
  "folke/which-key.nvim",   -- URL do repositório GitHub (user/repo)
  event = "VeryLazy",       -- evento que dispara o carregamento (lazy loading)
  opts = { delay = 200 },   -- tabela passada pro setup() do plugin automaticamente
}
```

Campos mais comuns em specs:

| Campo | Tipo | Função |
|---|---|---|
| `"user/repo"` | string | Repositório GitHub do plugin |
| `event` | string/table | Evento de carregamento (ex: `"VeryLazy"`, `"BufReadPost"`) |
| `cmd` | string/table | Comando que dispara carga (ex: `"Telescope"`) |
| `keys` | table | Keymaps que disparam carga |
| `opts` | table | Passado diretamente ao `require("plugin").setup(opts)` |
| `config` | function | Função `function(_, opts)` pra configuração customizada |
| `dependencies` | table | Plugins que devem ser carregados antes |

O campo `opts` é o mais usado em overrides de LazyVim: você só declara o que quer mudar, e LazyVim mescla com os defaults do plugin.

---

## Na prática

### Opções e leader (base do `init.lua`)

```lua
-- Deve vir antes de qualquer require
vim.g.mapleader = " "
vim.g.maplocalleader = ","

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
```

### Keymap com callback inline

```lua
-- Re-source arquivo atual e notifica
vim.keymap.set("n", "<leader>rs", function()
  vim.cmd("source %")
  vim.notify("Sourced!", vim.log.levels.INFO)
end, { desc = "Re-source current file" })

-- Toggle wrap
vim.keymap.set("n", "<leader>uw", function()
  vim.opt.wrap = not vim.opt.wrap:get()
end, { desc = "Toggle wrap" })
```

### Autocmd em Lua

```lua
-- Formatar ao salvar arquivos Lua via LSP
vim.api.nvim_create_autocmd("BufWritePre", {
  pattern = "*.lua",
  callback = function()
    vim.lsp.buf.format({ async = false })
  end,
})

-- Highlight ao yankar (yank flash)
vim.api.nvim_create_autocmd("TextYankPost", {
  callback = function()
    vim.highlight.on_yank({ higroup = "IncSearch", timeout = 150 })
  end,
})
```

### Spec de plugin com override de opts

```lua
-- Modificar delay do which-key no LazyVim
return {
  "folke/which-key.nvim",
  opts = {
    delay = 500,  -- ms antes de mostrar popup (default 200)
  },
}
```

### Módulo auxiliar simples

```lua
-- lua/utils.lua
local M = {}

M.is_git_repo = function()
  local result = vim.fn.system("git rev-parse --is-inside-work-tree 2>/dev/null")
  return vim.v.shell_error == 0
end

return M

-- Em outro arquivo:
local utils = require("utils")
if utils.is_git_repo() then
  -- carrega plugins git
end
```

---

## Armadilhas comuns

> [!warning] `0` é truthy em Lua
> `if x then` aceita `x = 0`. Vindo de JavaScript (onde `0` é falsy) ou Python (idem), esta é a armadilha mais frequente. Em Lua, apenas `false` e `nil` são falsy. Pra comparar com zero: `if x == 0 then`.

> [!warning] Tabelas são 1-indexed
> `t[1]` é o primeiro elemento — não `t[0]`. `#t` retorna o comprimento *do segmento inicial sem buracos*: uma lista com `nil` no meio tem `#` imprevisível. Para tabelas densas (sem `nil`), `#t` é seguro.

> [!warning] `local` esquecido cria global silenciosa
> `x = 1` no top-level de qualquer arquivo Lua cria `_G.x` — uma global que vaza entre módulos e sobrevive ao re-source. Em config Neovim isso polui o namespace. Hábito: sempre `local`. Ferramentas como `luacheck` detectam globals não declaradas.

> [!warning] `vim.opt` vs `vim.o`
> `vim.o.listchars = "tab:→ "` aceita apenas string (interface direta ao Vimscript). `vim.opt.listchars = { tab = "→ " }` aceita tabela Lua e habilita operações compostas (`:append`, `:remove`, `:prepend`). LazyVim usa `vim.opt` por convenção — e é o que permite `vim.opt.listchars:append(...)` sem sobrescrever o valor inteiro.

> [!warning] `require` com ponto ou barra?
> `require("foo.bar")` busca `lua/foo/bar.lua` no runtimepath — usa ponto como separador de diretório. Não confunda com `require("foo/bar")` que alguns snippets antigos usam — o correto pra Neovim é ponto.

---

## Em inglês

| PT-BR | EN | Uso técnico |
|---|---|---|
| tabela | table | `local t = {}` — Lua's only container type |
| módulo | module | a file that returns a value via `return` |
| escopo léxico | lexical scope | variables visible only in their enclosing block |
| variável local | local variable | `local x = 1` — block-scoped, preferred |
| verdadeiro/falso | truthy/falsy | only `false` and `nil` are falsy in Lua |
| concatenar | concatenate | `"foo" .. "bar"` → `"foobar"` |
| requerir / carregar | require | `require("module")` loads and caches a module |
| retornar | return | `return M` at the end of a module file |
| chamar | call | `vim.keymap.set(...)` — invoking a function |
| expressão | expression | any value-producing construct (e.g., `1 + 2`) |

---

## Veja também

- [[04 - LazyVim tour]] — uso antes de configurar; referência dos keymaps padrão
- [[06 - Estrutura de config]] — onde `init.lua` vive e como os módulos se organizam
- [[07 - lazy.nvim]] — Lua DSL pra declarar e carregar plugins
- [[08 - Customizando LazyVim]] — overrides são tabelas Lua em specs de plugin
- [[03-Dominios/Terminal/Editor/index|MOC do galho]]
- [[Dicionário do Terminal#Lua|Lua]], [[Dicionário do Terminal#init.lua|init.lua]]

---

## Referências

- [Neovim Lua Guide](https://neovim.io/doc/user/lua-guide.html) — `:help lua-guide` (documentação oficial, ponto de entrada)
- [Neovim Lua Reference](https://neovim.io/doc/user/lua.html) — `:help lua` (referência completa da integração)
- [Lua 5.1 Reference Manual](https://www.lua.org/manual/5.1/) — spec da linguagem usada pelo LuaJIT
- [Learn Lua in Y Minutes](https://learnxinyminutes.com/docs/lua/) — overview compacto da sintaxe
- [TJ DeVries no YouTube](https://www.youtube.com/@teej_dv) — maintainer de Neovim, tutoriais de Lua/Neovim
- [kickstart.nvim](https://github.com/nvim-lua/kickstart.nvim) — config template comentado, referência canônica para começar do zero
