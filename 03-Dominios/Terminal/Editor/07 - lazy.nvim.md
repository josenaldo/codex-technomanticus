---
title: "lazy.nvim"
created: 2026-05-19
updated: 2026-05-19
type: concept
progress: backlog
status: seedling
publish: true
fase: adepto
tags:
  - terminal
  - editor
  - adepto
  - lazy-nvim
  - plugin-manager
aliases:
  - lazy.nvim
  - Plugin manager
---

# lazy.nvim

> [!abstract] TL;DR
> lazy.nvim é o plugin manager que LazyVim usa. Plugin = tabela Lua (spec) que diz onde buscar, quando carregar, e como configurar. Lazy-loading por evento, comando, filetype ou key é o que mantém o startup rápido — o Neovim não paga o custo de um plugin até ele ser necessário.

## O que é / Como funciona

### O que é lazy.nvim

lazy.nvim é o [[Dicionário do Terminal#Plugin manager|plugin manager]] do Neovim moderno, desenvolvido por Folke Lemaitre (o mesmo autor do LazyVim, Telescope e outros). Substitui gerações anteriores — packer.nvim (legado Lua) e vim-plug (Vimscript) — com uma abordagem declarativa, lazy-loading nativo e interface interativa.

LazyVim usa lazy.nvim como base obrigatória. O bootstrap já está em `lua/config/lazy.lua` (ver [[06 - Estrutura de config]]). O que esta nota ensina é como **descrever plugins** (plugin spec) e como o lazy.nvim decide quando carregar cada um.

---

### Plugin spec — a tabela Lua

Cada plugin é descrito por uma tabela Lua chamada **[[Dicionário do Terminal#Plugin spec|plugin spec]]**. O primeiro campo posicional (`[1]`) é o identificador do repositório no formato `"author/repo"`. Todos os outros campos são opcionais e controlam como o plugin é instalado, configurado e carregado.

#### Campos principais

| Campo | Tipo | Descrição |
|---|---|---|
| `[1]` | `string` | `"author/repo"` (GitHub) ou URL completa |
| `opts` | `table` | Passada automaticamente pra `require("plugin").setup(opts)` |
| `config` | `function` | Controle total do setup — você chama `setup` manualmente |
| `init` | `function` | Roda no startup, antes do plugin carregar (raro precisar) |
| `dependencies` | `table` | Lista de plugins que devem ser carregados antes |
| `event` | `string\|table` | Carrega em evento Neovim (`"BufReadPost"`, `"VeryLazy"`, …) |
| `cmd` | `string\|table` | Carrega quando comando Ex é chamado (`"ZenMode"`, …) |
| `ft` | `string\|table` | Carrega ao abrir arquivo do filetype (`"lua"`, `"markdown"`) |
| `keys` | `table` | Carrega quando a key é pressionada (define keymap também) |
| `enabled` | `boolean` | `false` desabilita — lazy.nvim ignora o plugin completamente |
| `priority` | `number` | Força ordem de carregamento (colorscheme: `1000`) |
| `lazy` | `boolean` | `true` força lazy-load; `false` força load no startup |

**`opts` vs `config`:**

- `opts = { x = 1 }` → lazy.nvim chama `require("plugin").setup({ x = 1 })` automaticamente. É a forma preferida para 90% dos casos — concisa, mergeável.
- `config = function(_, opts) ... end` → você controla. O segundo argumento `opts` já contém o merge final (útil quando precisa de lógica condicional antes do setup).

Se usar `config`, o `opts` **não é aplicado automaticamente** — você precisa chamar `setup(opts)` explicitamente dentro da função.

**Merge de `opts`:**

Uma propriedade poderosa do lazy.nvim é o merge automático de `opts`. Se LazyVim já define `opts = { a = 1 }` para um plugin e você adiciona uma spec com `opts = { b = 2 }`, o resultado final é `{ a = 1, b = 2 }`. Isso permite estender a config sem copiar os defaults — é a base do sistema de override do LazyVim (detalhado em [[08 - Customizando LazyVim]]).

```lua
-- LazyVim define internamente:
-- opts = { signs = true, update_in_insert = false }

-- Você adiciona em lua/plugins/diagnostics.lua:
return {
  "folke/trouble.nvim",
  opts = { use_diagnostic_signs = true },  -- mergeado, não substituído
}
-- Resultado: { signs = true, update_in_insert = false, use_diagnostic_signs = true }
```

---

### Lazy-loading — os triggers

[[Dicionário do Terminal#Lazy-loading|Lazy-loading]] significa que o plugin não é carregado no startup — ele espera até ser necessário. lazy.nvim suporta quatro tipos de trigger:

**Por evento (`event`):**

```lua
event = "BufReadPost"   -- ao abrir/ler qualquer buffer
event = "VeryLazy"      -- após a UI do Neovim estar pronta (evento lazy.nvim)
event = { "BufReadPost", "BufNewFile" }
```

`VeryLazy` é evento próprio do lazy.nvim (dispara após `UIEnter` + defer), útil para plugins que não precisam estar prontos antes da primeira tecla. Não confundir com `BufReadPost` (que dispara ao abrir arquivo).

**Por comando (`cmd`):**

```lua
cmd = "ZenMode"           -- único comando
cmd = { "Git", "GV" }    -- múltiplos comandos
```

O plugin carrega na primeira vez que o usuário roda o comando. Enquanto não rodar, zero custo.

**Por filetype (`ft`):**

```lua
ft = "markdown"
ft = { "lua", "python", "typescript" }
```

Carrega quando um buffer do tipo especificado é aberto. Ideal para plugins de sintaxe, formatação ou linguagem específica.

**Por keymap (`keys`):**

```lua
keys = {
  { "<leader>uz", "<cmd>ZenMode<cr>", desc = "Zen mode" },
}
```

`keys` faz duas coisas ao mesmo tempo: registra o keymap **e** define o trigger de load. Antes de o plugin carregar, a key já funciona — lazy.nvim intercepta, carrega o plugin, depois repassa o comando.

---

### Lifecycle de carregamento

A sequência que o lazy.nvim executa para cada plugin:

1. **Coleta de specs** — todos os arquivos em `lua/plugins/*.lua` são importados e as tabelas, coletadas.
2. **Resolução** — dependências (`dependencies`) são ordenadas; plugins com mesmo repositório são mergeados.
3. **Instalação** — ao iniciar, plugins ainda não instalados são clonados do GitHub.
4. **Lazy ou eager** — plugins sem trigger (`event`/`cmd`/`ft`/`keys`) são carregados no startup (eager). Os demais esperam o trigger.
5. **`init`** — se declarado, roda no startup independente do lazy-load (raramente necessário).
6. **`config`** — roda após o plugin ser carregado. Recebe `(plugin, opts)`.
7. **Plugin ativo** — funções e comandos do plugin estão disponíveis.

O campo `init` existe para o caso específico em que você precisa configurar algo no startup **antes** de o plugin carregar — por exemplo, setar uma variável global que o plugin lê quando inicializa. Na prática, é raro. A regra geral: use `opts` ou `config`; recorra a `init` só quando o comportamento esperado não for possível com `config`.

---

### `:Lazy` — a TUI

Ao rodar `:Lazy`, o lazy.nvim abre uma interface interativa com lista de plugins e ações. Principais keys dentro da TUI:

| Key | Ação |
|---|---|
| `S` | Sync — instala, atualiza e remove plugins (equivale a I + U + X) |
| `U` | Update — atualiza todos os plugins para o commit mais recente |
| `R` | Restore — reverte para os commits do `lazy-lock.json` |
| `X` | Clean — remove plugins que não estão mais em nenhuma spec |
| `P` | Profile — mostra tempo de carregamento de cada plugin |
| `L` | Log — changelog dos plugins |
| `?` | Help — lista todas as keys disponíveis |

`P` (profile) é o ponto de partida para diagnosticar startup lento. Plugins com > 50ms são candidatos a receber um trigger de lazy-load.

---

### `lazy-lock.json` — reprodutibilidade

O arquivo `lazy-lock.json` na raiz da config registra o commit exato de cada plugin instalado. É o equivalente do `package-lock.json` do npm — garante que "rodou na minha máquina" também rode na próxima, e na outra.

```json
{
  "lazy.nvim": { "branch": "stable", "commit": "b52b4e4" },
  "tokyonight.nvim": { "branch": "main", "commit": "f7e3882" },
  "telescope.nvim": { "branch": "master", "commit": "a0bbec2" }
}
```

**Regra:** commitar o `lazy-lock.json` no repositório de dotfiles. Sem ele, uma atualização de plugin pode quebrar a config silenciosamente. Com ele, `:Lazy restore` volta para o estado exato do snapshot.

**Fluxo de atualização deliberada:**

1. `:Lazy update` — atualiza todos os plugins para o commit mais recente.
2. Testar a config por um tempo (minutos ou dias, dependendo do risco).
3. Se tudo OK: `git add lazy-lock.json && git commit -m "chore: bump plugins"`.
4. Se quebrou: `:Lazy restore` — reverte para o `lazy-lock.json` commitado.

Esse ciclo é análogo ao `npm update` + review + commit do `package-lock.json`.

---

## Na prática

### Exemplo 1 — plugin novo com cmd e keys

Plugin de edição zen (zen-mode.nvim) carregado apenas quando o comando ou o keymap é acionado:

```lua
-- lua/plugins/zen.lua
return {
  "folke/zen-mode.nvim",
  cmd = "ZenMode",
  keys = {
    { "<leader>uz", "<cmd>ZenMode<cr>", desc = "Zen mode" },
  },
  opts = {
    window = { width = 0.8 },
  },
}
```

O plugin não ocupa startup. Ao pressionar `<leader>uz` (ou rodar `:ZenMode`), lazy.nvim carrega o plugin e executa a ação.

---

### Exemplo 2 — dependência + lazy-load por filetype

Plugin de renderização de Markdown que só carrega quando um `.md` é aberto:

```lua
-- lua/plugins/markdown.lua
return {
  "MeanderingProgrammer/render-markdown.nvim",
  ft = { "markdown" },
  dependencies = { "nvim-treesitter/nvim-treesitter" },
  opts = {},
}
```

`dependencies` garante que nvim-treesitter seja carregado antes. `opts = {}` sem `config` significa que lazy.nvim chama `require("render-markdown").setup({})` automaticamente.

---

### Exemplo 3 — config function para lógica condicional

Quando a inicialização precisa de iteração ou condicional, use `config` em vez de `opts`:

```lua
-- lua/plugins/lsp.lua
return {
  "neovim/nvim-lspconfig",
  config = function()
    local lspconfig = require("lspconfig")
    local servers = { "ts_ls", "lua_ls", "pyright" }
    for _, s in ipairs(servers) do
      lspconfig[s].setup({})
    end
  end,
}
```

Note que `opts` não é usado — o `setup` é chamado manualmente dentro de `config`.

---

### Exemplo 4 — desabilitar plugin do LazyVim

Para desabilitar um plugin que LazyVim inclui por default, repita a spec com `enabled = false`:

```lua
-- lua/plugins/disable.lua
return {
  { "folke/noice.nvim", enabled = false },
}
```

O lazy.nvim mergeia specs do mesmo repositório — o `enabled = false` sobrescreve o default do LazyVim.

---

### Exemplo 5 — diagnosticar startup lento

1. Rodar `:Lazy profile` (ou pressionar `P` dentro da TUI).
2. A lista é ordenada por tempo de carregamento.
3. Plugins com > 50ms sem um trigger de lazy-load são candidatos a receber `event = "VeryLazy"` ou `cmd`/`ft`.
4. Rodar `:Lazy profile` novamente após adicionar o trigger para comparar.

---

### Exemplo 6 — colorscheme com priority

Colorschemes precisam ser carregados antes de outros plugins para evitar flash de tema errado. Usar `priority = 1000` e `lazy = false`:

```lua
-- lua/plugins/colorscheme.lua
return {
  "folke/tokyonight.nvim",
  lazy = false,        -- carregar no startup (não lazy)
  priority = 1000,     -- antes dos outros plugins eager
  opts = {
    style = "moon",
    transparent = false,
  },
  config = function(_, opts)
    require("tokyonight").setup(opts)
    vim.cmd.colorscheme("tokyonight-moon")
  end,
}
```

`lazy = false` com `priority = 1000` é o padrão canônico para colorschemes — sem isso, o tema pode carregar depois de outros plugins que tentam usar as cores, causando highlight incorreto na abertura.

---

## Armadilhas comuns

> [!warning] Arquivo sem `return`
> `lua/plugins/foo.lua` sem `return { ... }` no final: o plugin não carrega, lazy.nvim não emite erro e `:Lazy` não lista o plugin. O sintoma é simplesmente o plugin não funcionar. Sempre termine arquivos de plugin com `return { ... }`.

> [!warning] `config` sem chamar `setup`
> Se você declara `config = function(_, opts) ... end` e se esquece de chamar `require("plugin").setup(opts)` dentro, o plugin é carregado mas não inicializado. O lazy.nvim não chama `setup` automaticamente quando `config` está presente — é responsabilidade sua.

> [!warning] `lazy-lock.json` não commitado
> Sem o lockfile no repositório de dotfiles, instalar a config em outra máquina (ou restaurar depois de semanas) pode pegar versões diferentes dos plugins. Inclua `lazy-lock.json` no git. Se quiser atualizar intencionalmente: `:Lazy update`, depois commit do novo lockfile.

> [!warning] `VeryLazy` não é evento do Neovim
> `event = "VeryLazy"` é evento interno do lazy.nvim, não do Neovim. Ele dispara após a UI estar pronta e um defer curto. Usar `event = "VeryLazy"` em plugins que precisam estar prontos *antes* do primeiro buffer abre uma janela de tempo em que eles não estão disponíveis. Para plugins que precisam carregar antes do primeiro arquivo, use `event = "BufReadPost"` ou simplesmente omita o `event` (eager).

> [!warning] `priority` só importa para plugins eager
> O campo `priority` (`priority = 1000` para colorschemes) só tem efeito em plugins carregados no startup (sem trigger de lazy-load). Para plugins com `event`/`cmd`/`ft`/`keys`, a ordem é determinada pelas `dependencies` e pela sequência de resolução — não pelo `priority`.

---

## Em inglês

| PT-BR | EN | Uso técnico |
|---|---|---|
| plugin manager | plugin manager | categoria de ferramenta (lazy.nvim, packer) |
| carregamento preguiçoso | lazy loading | carregar apenas quando necessário |
| gatilho | trigger | `event`, `cmd`, `ft`, `keys` — o que dispara o load |
| evento | event | `BufReadPost`, `VeryLazy`, `FileType`, etc. |
| dependência | dependency | plugin que deve ser carregado antes |
| arquivo de lock | lockfile | `lazy-lock.json` — snapshot de versões |
| perfil de tempo | profile / timing | `:Lazy profile` — tempo de load por plugin |
| especificação | specification (`spec`) | tabela Lua que descreve um plugin |
| fonte | source | URL ou `"author/repo"` — de onde clonar o plugin |
| desabilitar | disable | `enabled = false` na spec |

---

## Veja também

- [[05 - Lua para Neovim]] — sintaxe Lua necessária para ler e escrever specs
- [[06 - Estrutura de config]] — onde os arquivos de spec vivem e como são importados
- [[08 - Customizando LazyVim]] — override de plugin LazyVim, extras e disabled plugins
- [[09 - LSP no Neovim]] — LSP plugins configurados via spec
- [[04 - LazyVim tour]] — interface `:Lazy` e plugins default do LazyVim
- [[03-Dominios/Terminal/Editor/index|MOC do galho]]
- [[Dicionário do Terminal#lazy.nvim|lazy.nvim]], [[Dicionário do Terminal#Lazy-loading|lazy-loading]], [[Dicionário do Terminal#Plugin manager|plugin manager]], [[Dicionário do Terminal#Plugin spec|plugin spec]]

---

## Referências

- [lazy.nvim — GitHub](https://github.com/folke/lazy.nvim)
- [lazy.nvim — Documentação oficial](https://lazy.folke.io/)
- [lazy.nvim — Plugin spec](https://lazy.folke.io/spec)
- [LazyVim — Configurando plugins](https://www.lazyvim.org/configuration/plugins)
- [awesome-neovim](https://github.com/rockerBOO/awesome-neovim) — catálogo de plugins para descobrir candidatos
