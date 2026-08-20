---
title: "Customizando LazyVim"
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
  - customization
  - lazyvim
aliases:
  - Customizando LazyVim
  - LazyVim override
---

# Customizando LazyVim

> [!abstract] TL;DR
> LazyVim é override-friendly: você cria arquivos em `lua/plugins/` que estendem ou sobrescrevem os defaults. Para plugin novo: spec completa. Para customizar existente: spec parcial com `opts` que faz merge profundo. Para desabilitar: `enabled = false`. Para Extras opcionais: `:LazyExtras` ou `{ import = "lazyvim.plugins.extras.X" }` em `lazy.lua`.

## O que é / Como funciona

O ponto central de customização do LazyVim é o diretório `lua/plugins/`. O lazy.nvim importa todos os arquivos `.lua` dentro dele automaticamente — o LazyVim chama isso de "user plugin directory". Cada arquivo retorna uma spec (ou lista de specs) que o lazy.nvim mergeia com os defaults da [[Dicionário do Terminal#Distribuição|distribuição]].

O mecanismo de merge é o que torna o LazyVim tão ergonômico. Quando dois arquivos declaram specs para o mesmo repositório (`"user/repo"`), o lazy.nvim combina os campos em vez de sobrescrever. Isso significa que você nunca precisa copiar a spec inteira do LazyVim — só declara o que quer mudar.

---

### Adicionar plugin novo

Criar `lua/plugins/<nome>.lua` retornando a [[Dicionário do Terminal#Plugin spec|plugin spec]] completa. LazyVim importa automaticamente (via `{ import = "plugins" }` em `lazy.lua`):

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

Após salvar o arquivo, `:Lazy sync` (ou `S` dentro da TUI) instala o plugin e o torna disponível.

---

### Override de plugin LazyVim — deep merge de `opts`

Para customizar um plugin que o LazyVim já inclui, crie um arquivo em `lua/plugins/` com a spec apontando para o mesmo repositório. O lazy.nvim faz **deep merge** dos campos `opts`:

```lua
-- lua/plugins/telescope-override.lua
return {
  "nvim-telescope/telescope.nvim",
  opts = {
    defaults = {
      layout_strategy = "vertical",
    },
  },
}
```

O lazy.nvim combina essa spec com a spec interna do LazyVim. Campos `opts` são mergeados em profundidade: tabelas aninhadas são combinadas; valores primitivos são sobrescritos. O resultado: a config default do LazyVim é mantida intacta, e só `layout_strategy` muda.

**O que acontece internamente:**

```lua
-- LazyVim define (simplificado):
opts = {
  defaults = {
    prompt_prefix = " ",
    selection_caret = " ",
    layout_strategy = "horizontal",
    -- ... dezenas de outros campos
  },
}

-- Você adiciona:
opts = {
  defaults = { layout_strategy = "vertical" },
}

-- Resultado final (deep merge):
opts = {
  defaults = {
    prompt_prefix = " ",
    selection_caret = " ",
    layout_strategy = "vertical",  -- sobrescrito
    -- ... outros campos preservados
  },
}
```

---

### Desabilitar plugin LazyVim

Para remover completamente um plugin do LazyVim, repita a spec com `enabled = false`. O lazy.nvim ignora o plugin na inicialização:

```lua
-- lua/plugins/disable-notify.lua
return { "rcarriga/nvim-notify", enabled = false }
```

Múltiplos disables podem ir no mesmo arquivo:

```lua
-- lua/plugins/disabled.lua
return {
  { "rcarriga/nvim-notify", enabled = false },
  { "akinsho/bufferline.nvim", enabled = false },
}
```

Depois de desabilitar, plugins instalados ficam no disco mas não carregam. Para remover do disco também: `:Lazy clean` (ou `X` na TUI) após salvar o arquivo de override.

---

### Override de keymap de plugin

O LazyVim define dezenas de [[Dicionário do Terminal#Keymap|keymaps]] via o campo `keys` nas specs internas. Para remover ou redefinir um keymap de plugin, use `false` no campo `rhs` antes de redeclará-lo:

```lua
-- lua/plugins/telescope-keys.lua
return {
  "nvim-telescope/telescope.nvim",
  keys = {
    { "<leader>ff", false },  -- remove o default do LazyVim
    {
      "<leader>ff",
      "<cmd>Telescope find_files hidden=true<cr>",
      desc = "Find files (hidden)",
    },
  },
}
```

`{ "<leader>ff", false }` instrui o lazy.nvim a remover esse keymap da spec mergeada antes de registrar os novos. Sem o `false` primeiro, o lazy.nvim pode manter ambas as definições (o comportamento depende de ordem de resolução).

**Por que `false` e não só redefinir:** o lazy.nvim acumula keymaps de múltiplas specs. Se o LazyVim define `{ "<leader>ff", "<cmd>Telescope find_files<cr>" }` e você define `{ "<leader>ff", "<cmd>Telescope find_files hidden=true<cr>" }`, ambos ficam registrados — e which-key pode mostrar duplicata. `false` garante remoção antes de adição.

---

### Keymap global (sem plugin) em `keymaps.lua`

Para keymaps que não estão associados a nenhum plugin específico, use `lua/config/keymaps.lua` (carrega depois dos plugins, ver [[06 - Estrutura de config]]):

```lua
-- lua/config/keymaps.lua
vim.keymap.set("n", "<leader>w", "<cmd>w<CR>", { desc = "Save" })
vim.keymap.set("n", "<leader>q", "<cmd>q<CR>", { desc = "Quit" })
```

Essa abordagem é correta para atalhos de uso geral que não dependem de nenhum plugin. Se o keymap depende de uma função de plugin, o lugar certo é a spec do plugin no campo `keys`.

---

### Extras — módulos opcionais do LazyVim

**Extras** são grupos de plugins e configs pré-montados pelo LazyVim para casos de uso específicos. São opcionais por design — a instalação base não os inclui, você ativa o que precisa.

**Habilitar via `:LazyExtras` (TUI interativa):**

Roda `:LazyExtras` no Neovim. Abre interface com lista de Extras disponíveis. Pressione `x` para habilitar ou desabilitar. O LazyVim salva a seleção em `lazyvim.json` na pasta de dados. Essa é a forma recomendada para experimentos.

**Habilitar em `lua/config/lazy.lua` (permanente no dotfiles):**

```lua
-- lua/config/lazy.lua
require("lazy").setup({
  spec = {
    { "LazyVim/LazyVim", import = "lazyvim.plugins" },
    { import = "lazyvim.plugins.extras.lang.typescript" },
    { import = "lazyvim.plugins.extras.lang.python" },
    { import = "lazyvim.plugins.extras.editor.harpoon2" },
    { import = "plugins" },
  },
  -- ...
})
```

Cada `{ import = "lazyvim.plugins.extras.X" }` adiciona um grupo de plugins à spec. O lazy.nvim resolve tudo junto.

**Categorias de Extras:**

| Categoria | Exemplos | O que adicionam |
|---|---|---|
| `lang/*` | `lang.typescript`, `lang.python`, `lang.rust`, `lang.go`, `lang.markdown` | LSP servers, formatters, treesitter grammars, snippets por linguagem |
| `editor/*` | `editor.harpoon2`, `editor.mini-surround`, `editor.inc-rename` | Ferramentas de edição e navegação |
| `ui/*` | `ui.mini-animate`, `ui.edgy` | Animações, layout de janelas |
| `dap/*` | `dap.core`, `dap.python` | Debugger (DAP) com adapters |
| `coding/*` | `coding.mini-comment`, `coding.yanky` | Helpers de código e yank |
| `util/*` | `util.project`, `util.rest` | Utilitários gerais |

Consulte `:LazyExtras` ou `https://www.lazyvim.org/extras` para a lista completa atualizada.

---

### Debugging de conflitos e diagnóstico

Quando um override não funciona ou o comportamento é inesperado:

**`:Lazy profile` (ou `P` na TUI):**
Lista plugins ordenados por tempo de carregamento. Útil para ver se um plugin está sendo carregado quando não deveria.

**`:Lazy log <plugin>` (ou `L` na TUI):**
Mostra o changelog/log de um plugin específico.

**`:checkhealth`:**
Diagnóstico completo. Muitos plugins implementam healthchecks que reportam dependências ausentes ou configs inválidas.

**`:LazyExtras`:**
Mostra quais Extras estão habilitados. Útil para confirmar que um Extra foi ativado corretamente.

**`:Lazy` → plugin → `Enter`:**
Mostra o spec completo e mergeado de um plugin — todas as fontes (LazyVim + seus overrides). Indispensável para entender o que está sendo aplicado.

---

## Na prática

### Exemplo 1 — customizar tema

Trocar o estilo do tokyonight e confirmar que é o colorscheme ativo:

```lua
-- lua/plugins/colorscheme.lua
return {
  { "folke/tokyonight.nvim", opts = { style = "moon" } },
  { "LazyVim/LazyVim", opts = { colorscheme = "tokyonight" } },
}
```

O segundo item (`LazyVim/LazyVim`) define qual colorscheme o LazyVim aplica no startup. Sem ele, o tema muda mas pode não ser ativado automaticamente.

---

### Exemplo 2 — adicionar formatter por linguagem

Estender o conform.nvim (formatter default do LazyVim) com formatters para Python:

```lua
-- lua/plugins/conform.lua
return {
  "stevearc/conform.nvim",
  opts = {
    formatters_by_ft = {
      python = { "ruff_format", "ruff_fix" },
    },
  },
}
```

O deep merge preserva os formatters que o LazyVim já define (para Lua, TypeScript, etc.) e adiciona `python`. Não é necessário copiar os defaults.

---

### Exemplo 3 — desabilitar bufferline

Para quem prefere trabalhar com harpoon ou gerenciar buffers sem barra visual:

```lua
-- lua/plugins/disable-bufferline.lua
return { "akinsho/bufferline.nvim", enabled = false }
```

---

### Exemplo 4 — habilitar Extra de TypeScript

Em `lua/config/lazy.lua`, dentro do `spec`:

```lua
spec = {
  { "LazyVim/LazyVim", import = "lazyvim.plugins" },
  { import = "lazyvim.plugins.extras.lang.typescript" },
  { import = "plugins" },
},
```

Após salvar e rodar `:Lazy sync`, o LazyVim instala o ts_ls server, formatters (prettierd, eslint_d), snippets TypeScript e config de treesitter para TypeScript/TSX.

---

### Exemplo 5 — override seletivo de Telescope

Mudar layout para vertical e ajustar altura do preview, preservando todos os outros defaults:

```lua
-- lua/plugins/telescope.lua
return {
  "nvim-telescope/telescope.nvim",
  opts = {
    defaults = {
      layout_strategy = "vertical",
      layout_config = {
        vertical = { preview_height = 0.6 },
      },
    },
  },
}
```

---

### Exemplo 6 — habilitar harpoon2 via Extra e adicionar keymaps

```lua
-- lua/config/lazy.lua (adicionar ao spec)
{ import = "lazyvim.plugins.extras.editor.harpoon2" },

-- lua/plugins/harpoon.lua (keymaps adicionais)
return {
  "ThePrimeagen/harpoon",
  branch = "harpoon2",
  keys = {
    { "<leader>ha", function() require("harpoon"):list():add() end, desc = "Harpoon add" },
    { "<leader>hh", function() require("harpoon").ui:toggle_quick_menu(require("harpoon"):list()) end, desc = "Harpoon menu" },
    { "<leader>h1", function() require("harpoon"):list():select(1) end, desc = "Harpoon 1" },
    { "<leader>h2", function() require("harpoon"):list():select(2) end, desc = "Harpoon 2" },
  },
}
```

---

## Armadilhas comuns

> [!warning] `opts = nil` sobrescreve o default
> `return { "nvim-telescope/telescope.nvim", opts = nil }` faz o lazy.nvim entender que você quer opts vazio, apagando os defaults do LazyVim. Se o objetivo é não mudar nada, omita o campo `opts` inteiramente. Se quiser garantir opts vazio explicitamente, use `opts = {}`.

> [!warning] Função em `opts` quebra o merge
> `opts` precisa ser tabela para o deep merge funcionar. Se você usa `opts = function(_, opts) return vim.tbl_deep_extend("force", opts, { ... }) end`, o lazy.nvim chama a função com o `opts` mergeado como argumento — o comportamento é previsível, mas perde a ergonomia do merge automático. Se precisar de lógica condicional, use `config` em vez de `opts`. Para casos ambíguos, consulte `https://www.lazyvim.org/configuration/recipes`.

> [!warning] Adicionou Extra mas plugins não aparecem
> Extras adicionam *novos* plugins à spec — eles precisam ser instalados. Após editar `lazy.lua`, rode `:Lazy sync` (`S` na TUI) para baixar os novos plugins. `:checkhealth` confirma se as dependências do Extra estão satisfeitas.

> [!warning] `{ "<leader>ff", false }` esquecido antes da redefinição
> Sem remover o default com `false`, o lazy.nvim pode manter ambas as definições ativas. A ordem de resolução determina qual prevalece — comportamento frágil. Sempre use `{ "<leader>lhs", false }` antes de redefinir um keymap existente.

> [!warning] Override não se aplica porque o plugin não tem spec no LazyVim
> Se você cria `lua/plugins/foo.lua` com `"user/plugin"` esperando fazer override, mas o LazyVim não incluía esse plugin, o resultado é que você *adicionou* um plugin novo (não fez override). Isso é correto e esperado — mas confirme primeiro em `:Lazy` se o plugin já estava na spec original.

> [!warning] `:LazyExtras` e `{ import = "..." }` podem coexistir com conflito
> Se você habilitou um Extra via `:LazyExtras` (salvo em `lazyvim.json`) **e** também adicionou o mesmo `{ import = "..." }` em `lazy.lua`, o Extra é importado duas vezes. Na maioria dos casos o lazy.nvim resolve sem problema (specs duplicadas para o mesmo repo são mergeadas), mas é confuso. Escolha uma abordagem só: ou `:LazyExtras` (interativo, não no git), ou `{ import = "..." }` em `lazy.lua` (no dotfiles).

---

## Em inglês

| PT-BR | EN | Uso técnico |
|---|---|---|
| customização | customization | adaptar o LazyVim ao próprio workflow |
| override | override | redefinir comportamento default via spec |
| mesclagem profunda | deep merge | `vim.tbl_deep_extend("force", ...)` — combina tabelas aninhadas |
| desabilitar | disable | `enabled = false` na plugin spec |
| estender | extend | adicionar campos a uma spec existente |
| prioridade | priority | campo `priority` na spec (só afeta plugins eager) |
| atalho de plugin | plugin keymap | keymap declarado no campo `keys` da spec |
| módulo extra | extra / extension | `lazyvim.plugins.extras.*` — conjuntos opcionais |
| conflito | conflict | specs que se contradizem ou comportamento inesperado após merge |
| diagnóstico de saúde | healthcheck | `:checkhealth` — verificação de dependências e config |

---

## Veja também

- [[06 - Estrutura de config]] — onde os arquivos de override vivem e a ordem de carregamento
- [[07 - lazy.nvim]] — referência completa de plugin spec, campos e lazy-loading
- [[09 - LSP no Neovim]] — customização de LSP é caso especial (mason, lspconfig, cmp)
- [[04 - LazyVim tour]] — entender os defaults antes de fazer override
- [[03-Dominios/Tecnologia/Terminal/Editor/index|MOC do galho]]
- [[Dicionário do Terminal#Distribuição|distribuição]], [[Dicionário do Terminal#Plugin spec|plugin spec]], [[Dicionário do Terminal#Keymap|keymap]], [[Dicionário do Terminal#Leader key|leader key]]

---

## Referências

- [LazyVim — Configurando plugins](https://www.lazyvim.org/configuration/plugins)
- [LazyVim — Extras](https://www.lazyvim.org/extras)
- [LazyVim — Recipes](https://www.lazyvim.org/configuration/recipes)
- [Folke dotfiles](https://github.com/folke/dot) — config real do autor do LazyVim
- [LazyVim Discussions](https://github.com/LazyVim/LazyVim/discussions) — casos de uso reais e soluções da comunidade
