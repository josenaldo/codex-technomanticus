---
title: "LSP no Neovim"
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
  - lsp
  - mason
  - completion
aliases:
  - LSP
  - Language Server Protocol
---

# LSP no Neovim

> [!abstract] TL;DR
> Language Server Protocol (LSP) é cliente-servidor: editor (cliente) fala JSON-RPC com servidor da linguagem (TypeScript, Rust, etc.) pra hover, completions, refactor. Em LazyVim: [[Dicionário do Terminal#Mason|Mason]] instala servers, [[Dicionário do Terminal#nvim-lspconfig|nvim-lspconfig]] configura, [[Dicionário do Terminal#nvim-cmp|nvim-cmp]] completa, conform formata.

## O que é / Como funciona

### O protocolo

O Language Server Protocol é uma especificação da Microsoft que desacopla o editor (cliente LSP) do conhecimento de linguagem (servidor LSP). Antes do LSP, cada editor precisava implementar suporte nativo a cada linguagem — uma integração N×M. Com o protocolo, a lógica de linguagem vive num [[Dicionário do Terminal#Language server|language server]] separado e qualquer editor que fale LSP acessa hover, go-to-definition, completions, refactor e [[Dicionário do Terminal#Diagnostic|diagnostics]] sem retrabalho.

O transporte é **JSON-RPC over stdio**: editor e server trocam mensagens JSON numeradas. O editor envia requests:

- `textDocument/hover` — exibe documentação ao pressionar `K`
- `textDocument/definition` — navega com `gd`
- `textDocument/references` — lista referências com `gr`
- `textDocument/rename` — renomeia symbol com `<leader>cr`
- `textDocument/codeAction` — lista code actions com `<leader>ca`
- `textDocument/publishDiagnostics` — server publica erros/warnings no editor (push, não poll)

### Capabilities

Na inicialização da sessão (`initialize` / `initialized`), cliente e server trocam um objeto `capabilities`. O cliente declara o que sabe renderizar (ex: `hoverContentFormat: ["markdown"]`); o server declara o que implementa (ex: `referencesProvider: true`). Só features que ambos suportam ficam ativas. Isso permite que um server simples coexista com um editor avançado sem erros.

### Stack LSP do LazyVim

O LazyVim monta uma stack completa de LSP — você não precisa configurar do zero, mas precisa entender as peças pra customizar:

| Camada | Plugin | Função |
|---|---|---|
| Instalação | [[Dicionário do Terminal#Mason|Mason]] | Instala/atualiza server binaries |
| Configuração | [[Dicionário do Terminal#nvim-lspconfig|nvim-lspconfig]] | Configs padronizadas pra ~200 servers |
| Completion | [[Dicionário do Terminal#nvim-cmp|nvim-cmp]] | Engine de autocomplete |
| Formatting | conform.nvim | Dispatcher de formatters |
| Linting | nvim-lint | Dispatcher de linters |

---

#### Mason

O [[Dicionário do Terminal#Mason|Mason]] é o gerenciador de ferramentas de desenvolvimento do Neovim. Ele instala e atualiza binaries de [[Dicionário do Terminal#Language server|language servers]], [[Dicionário do Terminal#Formatter|formatters]], [[Dicionário do Terminal#Linter|linters]] e DAP adapters num diretório local (`~/.local/share/nvim/mason/`), sem poluir o sistema.

- `:Mason` abre a TUI. Navegar com `j`/`k`, instalar com `i`, desinstalar com `X`, atualizar com `u`.
- `:MasonInstall <server>` instala via linha de comando.
- O LazyVim usa `mason-lspconfig.nvim` como ponte: servers declarados em `opts.servers` do nvim-lspconfig são auto-instalados pelo Mason se `mason = true` (default).

---

#### nvim-lspconfig

O `nvim-lspconfig` não é o cliente LSP — o Neovim tem cliente LSP built-in (`vim.lsp`). O que `nvim-lspconfig` fornece são **configs padronizadas** para ~200 servers: saber qual binary executar, quais filetypes ativar, qual `root_dir` usar.

Em LazyVim, a customização de servers é feita via plugin spec:

```lua
-- lua/plugins/lsp.lua
return {
  "neovim/nvim-lspconfig",
  opts = {
    servers = {
      ts_ls = {           -- TypeScript (nome atual desde 2024)
        settings = {
          typescript = {
            inlayHints = {
              parameterNames = { enabled = "all" },
              parameterTypes = { enabled = true },
            },
          },
        },
      },
    },
  },
}
```

O LazyVim faz deep merge: sua spec se combina com a spec interna sem precisar copiar tudo.

---

#### nvim-cmp

O [[Dicionário do Terminal#nvim-cmp|nvim-cmp]] é o engine de completion do Neovim. Ele não gera completions — ele agrega **sources** e renderiza o popup:

- `nvim_lsp` — completions do language server (a fonte principal)
- `buffer` — palavras do buffer atual
- `path` — caminhos de arquivo
- `luasnip` / `vsnip` — snippets

Em LazyVim, o nvim-cmp está pré-configurado. Keymaps default em insert mode:
- `<Tab>` / `<S-Tab>` — navegar no popup
- `<CR>` — confirmar
- `<C-e>` — fechar popup

---

#### conform.nvim

O `conform.nvim` é o dispatcher de [[Dicionário do Terminal#Formatter|formatters]] no LazyVim moderno (substituto do `null-ls` arquivado). Ele invoca a ferramenta correta por filetype (`prettier`, `ruff`, `gofmt`, `stylua`…) e passa o resultado de volta ao buffer.

Em LazyVim, `format on save` chama o conform por default. Para adicionar ou customizar formatters:

```lua
-- lua/plugins/conform.lua
return {
  "stevearc/conform.nvim",
  opts = {
    formatters_by_ft = {
      markdown = { "prettier", "markdownlint" },
    },
    formatters = {
      markdownlint = {
        prepend_args = { "--fix" },
      },
    },
  },
}
```

`:ConformInfo` no buffer mostra qual formatter está ativo e por quê.

---

#### nvim-lint

O `nvim-lint` é o dispatcher de [[Dicionário do Terminal#Linter|linters]] (análise sem formatação: `eslint_d`, `ruff`, `shellcheck`…). Os diagnostics do nvim-lint entram no mesmo pipeline do LSP e aparecem no gutter, virtual text e lista de diagnósticos — o usuário não percebe a diferença de origem.

---

### Keymaps default do LazyVim

As keymaps LSP são ativadas automaticamente em qualquer buffer onde um [[Dicionário do Terminal#Language server|language server]] está ativo (via `LspAttach`):

| Keymap | Ação |
|---|---|
| `gd` | Go to definition |
| `gr` | References (Telescope) |
| `gI` | Implementations |
| `gy` | Type definition |
| `K` | Hover (docs inline) |
| `<leader>ca` | [[Dicionário do Terminal#Code action\|Code action]] |
| `<leader>cr` | Rename symbol |
| `<leader>cf` | [[Dicionário do Terminal#Format on save\|Format]] (manual) |
| `]d` / `[d` | Diagnostic próximo/anterior |
| `]e` / `[e` | Error próximo/anterior |
| `]w` / `[w` | Warning próximo/anterior |
| `<leader>cd` | Line diagnostic (popup) |

Essas keymaps foram introduzidas em [[04 - LazyVim tour]]; aqui entendemos de onde vêm e como customizá-las por server.

---

### Diagnostic flow

O [[Dicionário do Terminal#Diagnostic|diagnostic]] é o canal pelo qual erros, warnings, infos e hints chegam ao editor. O server emite `textDocument/publishDiagnostics` com uma lista de mensagens posicionadas. O Neovim as renderiza via `vim.diagnostic.*`:

- **Sign no gutter** — ícone na coluna esquerda (E, W, I, H)
- **Virtual text inline** — mensagem no final da linha
- **Underline** — sublinhado no trecho problemático
- **Float popup** — `<leader>cd` ou `vim.diagnostic.open_float()` mostra detalhes

Para listar todos os diagnostics:
- `:lopen` — quickfix list local
- `<leader>xd` — Telescope (todos os diagnostics do projeto)

Severidades: `ERROR`, `WARN`, `INFO`, `HINT`. Configurar visibilidade por severidade:

```lua
-- em opts.diagnostics da spec do nvim-lspconfig
diagnostics = {
  virtual_text = { severity = { min = vim.diagnostic.severity.WARN } },
  signs = true,
  underline = true,
},
```

---

### on_attach — keymap por server

Para adicionar keymaps específicos de um server (ex: TypeScript tem `OrganizeImports`, Rust tem `expand_macro`):

```lua
-- lua/plugins/lsp.lua
return {
  "neovim/nvim-lspconfig",
  opts = {
    servers = {
      ts_ls = {
        on_attach = function(client, bufnr)
          vim.keymap.set("n", "<leader>co", "<cmd>TypescriptOrganizeImports<cr>",
            { buffer = bufnr, desc = "Organize imports" })
        end,
      },
    },
  },
}
```

O `on_attach` é chamado quando o server se conecta ao buffer. `bufnr` limita o keymap ao buffer atual — sem vazamento para outros filetypes.

---

### Instalar server via Mason

Para instalar um server manualmente:

1. `:Mason` — abre TUI
2. `/` — buscar (ex: `lua-language-server`)
3. `i` — instalar
4. Aguardar download e compilação

Para instalar via linha de comando: `:MasonInstall lua-language-server`.

Para servers não-bundled pelo LazyVim, declarar na spec de lspconfig:

```lua
opts = {
  servers = {
    lua_ls = {},     -- bundled, Mason auto-instala
    someserver = {}, -- não-bundled: Mason instala se binary existir no registry
  },
},
```

---

### Troubleshooting

Quando o LSP não funciona como esperado, sequência de diagnose:

| Comando | O que mostra |
|---|---|
| `:LspInfo` | Clients ativos no buffer atual e status |
| `:Mason` | Servers instalados e versões |
| `:checkhealth lsp` | Diagnose geral do cliente LSP built-in |
| `:ConformInfo` | Qual formatter ativo no buffer |
| `:LspLog` | Log de comunicação JSON-RPC do client |
| `:LspRestart` | Reinicia os clients do buffer atual |

Fluxo típico:
1. `:LspInfo` — server está ativo? Se não: ver item 2.
2. `:Mason` — binary instalado? Se não: instalar.
3. `:LspLog` — server crashando? Ver stack trace.
4. `:ConformInfo` — formatter não dispara? Verificar se filetype está mapeado.

---

## Na prática

### Exemplo 1 — habilitar inlay hints no TypeScript

```lua
-- lua/plugins/lsp.lua
return {
  "neovim/nvim-lspconfig",
  opts = {
    servers = {
      ts_ls = {
        settings = {
          typescript = {
            inlayHints = {
              parameterNames = { enabled = "all" },
              parameterTypes = { enabled = true },
            },
          },
          javascript = {
            inlayHints = {
              parameterNames = { enabled = "all" },
              parameterTypes = { enabled = true },
            },
          },
        },
      },
    },
  },
}
```

Inlay hints aparecem em cinza após os parâmetros e expressões. Toggle em LazyVim: `<leader>uh`.

---

### Exemplo 2 — adicionar formatter para Markdown

```lua
-- lua/plugins/conform.lua
return {
  "stevearc/conform.nvim",
  opts = {
    formatters_by_ft = {
      markdown = { "prettier", "markdownlint" },
    },
    formatters = {
      markdownlint = {
        prepend_args = { "--fix" },
      },
    },
  },
}
```

O conform tenta os formatters em ordem. Se `prettier` não estiver instalado, cai para `markdownlint`. `:MasonInstall markdownlint-cli` instala o binary.

---

### Exemplo 3 — keymap específico por server

```lua
-- lua/plugins/lsp.lua
return {
  "neovim/nvim-lspconfig",
  opts = {
    servers = {
      ts_ls = {
        on_attach = function(client, bufnr)
          vim.keymap.set("n", "<leader>co", "<cmd>TypescriptOrganizeImports<cr>",
            { buffer = bufnr, desc = "Organize imports" })
        end,
      },
    },
  },
}
```

O `buffer = bufnr` é essencial — sem ele o keymap vaza para todos os buffers, incluindo Lua, Python, etc.

---

### Exemplo 4 — desabilitar virtual text de diagnostics

Algumas pessoas preferem ver diagnostics apenas via `:lopen` ou float, sem virtual text inline:

```lua
-- lua/plugins/lsp.lua
return {
  "neovim/nvim-lspconfig",
  opts = {
    diagnostics = {
      virtual_text = false,
      signs = true,
      underline = true,
      update_in_insert = false,
    },
  },
}
```

Toggle rápido em LazyVim: `<leader>ud` (virtual text) / `<leader>uD` (diagnostics do buffer).

---

## Armadilhas

> [!warning] Armadilha 1 — Mason install ≠ server ativo
> Mason instala o binary no path local. Para o server ser ativado no Neovim, é preciso que ele esteja declarado no nvim-lspconfig (direta ou indiretamente via LazyVim bundle). Se instalar um server exótico via Mason e ele não ativar, criar a spec em `lua/plugins/lsp.lua` com `opts.servers.<nome> = {}`.

> [!warning] Armadilha 2 — `ts_ls` vs `tsserver`
> O language server do TypeScript foi renomeado de `tsserver` para `ts_ls` em 2024. Tutoriais anteriores a isso usam `tsserver` nas configs — e **quebram silenciosamente**: o server não ativa, sem erro óbvio. No Mason, o nome do package também mudou. Sempre verificar o nome atual em `:Mason` antes de replicar config de tutorial antigo.

> [!warning] Armadilha 3 — Format on save vs LSP format vs conform
> Em LazyVim, `:w` aciona o **conform.nvim**, não o LSP. O comando `:lua vim.lsp.buf.format()` chama o formatter do LSP diretamente — resultado pode ser diferente. A prioridade do LazyVim: conform.nvim tem preferência; LSP format só roda se o filetype não tem formatter conform configurado. Confusão clássica: "formatei com `<leader>cf` e salvei, veio resultado diferente" — sinal de que o formatter do LSP e o conform estão divergindo.

> [!warning] Armadilha 4 — Diagnostic flood em mono-repo
> Servers como `ts_ls` podem reportar erros em arquivos **fora** dos abertos — em projetos grandes isso gera centenas de diagnostics falsos. A causa é `root_dir` mal configurado. Solução: garantir que `tsconfig.json` existe na raiz correta e que o `root_dir` da spec aponta para ele. Em workspaces multi-projeto, configurar `ts_ls` com `single_file_support = false` e `root_dir` customizado.

> [!warning] Armadilha 5 — `null-ls` em tutoriais 2022-2023
> O `null-ls` foi **arquivado** pelo maintainer. Tutoriais de 2022-2023 usam null-ls como bridge para formatters e linters. No LazyVim moderno, isso está partido em dois plugins dedicados: **conform.nvim** (formatting) e **nvim-lint** (linting). Se copiar config de tutorial antigo com `null-ls`, o plugin não vai estar disponível e a config vai falhar na inicialização.

> [!tip] Armadilha 6 (bônus) — `on_attach` vs `opts`
> Dois jeitos de configurar um server: via `settings` (JSON enviado ao server) e via `on_attach` (callback Lua quando o server conecta). São camadas diferentes. `settings` controla o **comportamento do server**; `on_attach` controla **integrações do editor** (keymaps, autocommands locais). Misturar os dois sem entender a distinção gera configs confusas.

---

## Vocabulário

| PT-BR | EN |
|---|---|
| servidor de linguagem | language server |
| capabilities | capabilities |
| diagnóstico | diagnostic |
| refatorar renomeando | rename symbol |
| formatador | formatter |
| linter | linter |
| gutter | gutter |
| saltar para definição | go to definition |
| referências | references |
| protocolo | protocol |
| dicas inline | inlay hints |
| action de código | code action |

---

## Veja também

- [[04 - LazyVim tour]] — LSP keys default (onde essas keymaps aparecem primeiro)
- [[06 - Estrutura de config]] — onde a config do LSP vive na árvore de arquivos
- [[07 - lazy.nvim]] — plugin spec e como o deep merge funciona
- [[08 - Customizando LazyVim]] — override de opts, padrão geral de customização
- [[12 - Treesitter avançado]] — complementar: Treesitter dá estrutura sintática local, LSP dá semântica cross-arquivo
- [[13 - Snippets e DAP]] — DAP é "irmão" do LSP; Mason compartilhado para DAP adapters
- [[03-Dominios/Terminal/Editor/index|MOC do galho]]

### Verbetes relacionados

- [[Dicionário do Terminal#LSP|LSP]]
- [[Dicionário do Terminal#Language server|Language server]]
- [[Dicionário do Terminal#Mason|Mason]]
- [[Dicionário do Terminal#nvim-cmp|nvim-cmp]]
- [[Dicionário do Terminal#nvim-lspconfig|nvim-lspconfig]]
- [[Dicionário do Terminal#Diagnostic|Diagnostic]]
- [[Dicionário do Terminal#Formatter|Formatter]]
- [[Dicionário do Terminal#Linter|Linter]]
- [[Dicionário do Terminal#Code action|Code action]]
- [[Dicionário do Terminal#Format on save|Format on save]]

---

## Referências

- <https://www.lazyvim.org/configuration/lsp>
- <https://github.com/neovim/nvim-lspconfig>
- <https://github.com/williamboman/mason.nvim>
- <https://github.com/hrsh7th/nvim-cmp>
- <https://github.com/stevearc/conform.nvim>
- <https://microsoft.github.io/language-server-protocol/>
- <https://www.youtube.com/@teej_dv> (TJ DeVries — LSP explained)
