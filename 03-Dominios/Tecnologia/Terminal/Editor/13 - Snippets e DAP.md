---
title: "Snippets e DAP"
created: 2026-05-19
updated: 2026-05-19
type: concept
progress: backlog
status: seedling
publish: true
fase: Magus
tags:
  - terminal
  - editor
  - magus
  - snippets
  - luasnip
  - dap
  - debugging
aliases:
  - DAP
  - Snippets
  - LuaSnip
---

# Snippets e DAP

> [!tldr] TL;DR
> [[Dicionário do Terminal#LuaSnip|LuaSnip]] é o snippet engine do LazyVim — expande triggers em código com tabstops navegáveis. [[Dicionário do Terminal#DAP|DAP]] é Debug Adapter Protocol — debugger plugado no Neovim com breakpoints, step e REPL. Ambos opcionais mas multiplicam quando o flow é repetitivo (boilerplate) ou crítico (debug).

---

## O que é / Como funciona

### Snippets

Um [[Dicionário do Terminal#Snippet|snippet]] é um trecho de código parametrizável que se expande a partir de um **trigger** — uma palavra-chave curta digitada em insert mode. Depois da expansão, o cursor navega entre campos editáveis (**tabstops**) via `<Tab>` e `<S-Tab>`.

O engine padrão do LazyVim é o **LuaSnip**, que suporta dois formatos de definição:

- **Lua puro** — mais expressivo, suporta lógica e transformations.
- **VS Code JSON** — mais portável; pacotes como `friendly-snippets` usam esse formato e já vêm com catálogos prontos pra TS, JS, Lua, Markdown e outras linguagens.

#### Anatomia de um snippet

**Trigger**
Texto curto que dispara a expansão. Exemplo: digitar `func` e pressionar `<Tab>` expande para `function foo() {}`. O trigger é definido na spec do snippet como `prefix` (JSON) ou primeiro argumento de `s()` (Lua).

**Tabstops**
Posições de cursor numeradas: `$1`, `$2`, `$0`. Ao expandir, o cursor vai para `$1`; cada `<Tab>` avança ao próximo número; `$0` é o ponto final. Sem `$0`, o cursor para no último `$N` declarado.

**Placeholders**
Texto default dentro de um tabstop: `${1:name}` apresenta `name` já selecionado — basta digitar para substituir. Útil para sinalizar o que vai naquele campo sem obrigar a digitar do zero.

**Choice**
`${1|a,b,c|}` abre um menu de escolha com as opções listadas. Em LuaSnip: nó `choice_node` com lista de nós. Navegar entre choices: `<C-l>` (próxima) e `<C-h>` (anterior) — keymaps configuráveis.

**Transformations (LuaSnip, Lua-side)**
Tabstop derivado de outro via função Lua. Exemplo clássico: dado o nome de uma função em `$1`, gerar automaticamente o nome do teste em `$2` com `"test_" .. tabstop_value`. Suportado apenas na API Lua do LuaSnip — não tem equivalente direto em JSON.

#### Tipos de nós na API Lua do LuaSnip

LuaSnip modela snippets como árvores de nós. Os principais:

| Nó | Alias | Função |
|---|---|---|
| `snippet` | `s` | Container raiz do snippet |
| `text_node` | `t` | Texto estático (não editável) |
| `insert_node` | `i` | Tabstop editável (com placeholder opcional) |
| `function_node` | `f` | Texto derivado de função Lua |
| `choice_node` | `c` | Nó com lista de opções navegáveis |
| `dynamic_node` | `d` | Nó gerado dinamicamente por função |
| `restore_node` | `r` | Restaura conteúdo de sessão anterior |

Na prática, `s`, `t`, `i` e `f` cobrem 95% dos casos de uso.

#### Comparação: JSON vs Lua

| Critério | VS Code JSON | LuaSnip Lua |
|---|---|---|
| Portabilidade | Alta — funciona em VS Code, Zed, outros editores | Neovim-only |
| Expressividade | Básica — texto estático + tabstops | Total — lógica arbitrária, transformations |
| Transformations | Regex limitado (spec VS Code) | Lua puro, qualquer operação |
| Manutenção | Mais fácil pra não-devs Lua | Requer Lua básico |
| Fonte de catálogos | `friendly-snippets`, `rafamadriz` | Comunidade Neovim, plugins específicos |

Recomendação pragmática: use JSON pra snippets de equipe (compartilhável com VS Code) e Lua pra snippets pessoais com lógica.

---

### DAP

**Debug Adapter Protocol** (DAP) é um protocolo open source criado pela Microsoft que padroniza a comunicação entre editores e debuggers nativos. Em vez de cada editor implementar integração com cada debugger, existe uma camada de adaptação por linguagem — o **adapter** — que traduz comandos do protocolo pro debugger nativo da linguagem.

No Neovim, o DAP funciona em três camadas:

| Camada | Plugin | Função |
|---|---|---|
| Cliente DAP | `nvim-dap` | Controla a sessão de debug |
| UI | `nvim-dap-ui` | Splits de scopes, watches, stacks, breakpoints |
| Instalador | `mason-nvim-dap` | Instala adapters via Mason |

A separação em camadas é intencional: `nvim-dap` expõe API Lua para controlar sessões programaticamente (útil pra integrar com test runners, por exemplo), enquanto `nvim-dap-ui` é puramente presentacional — pode ser substituído ou desabilitado sem afetar o debugging em si.

#### Por que DAP é diferente de LSP

LSP e DAP são protocolos distintos que seguem arquitetura semelhante (cliente/servidor), mas cobrem fases diferentes do desenvolvimento:

- **LSP** — análise estática do código em repouso (definições, tipos, completions, diagnostics).
- **DAP** — comportamento do código em execução (breakpoints, variáveis em runtime, call stack, REPL).

Eles compartilham infraestrutura (Mason instala ambos) mas são processos separados — o language server e o debug adapter rodam independentemente.

#### Adapters comuns

| Linguagem | Adapter |
|---|---|
| Node.js / TypeScript | `js-debug-adapter` |
| Python | `debugpy` |
| Rust / C++ | `codelldb` |
| Go | `delve` |
| Java | `java-debug-adapter` |
| PHP | `php-debug-adapter` |
| C# / .NET | `netcoredbg` |

#### LazyVim Extras de debug

LazyVim separa debug em Extras — módulos opcionais ativados via `:LazyExtras`:

- `dap/core` — base (nvim-dap + nvim-dap-ui + mason-nvim-dap).
- `dap/<lang>` — Extra por linguagem: `lang.typescript`, `lang.python`, `lang.rust`, `lang.go`, etc. Cada Extra de linguagem já inclui LSP + formatter + linter + DAP quando disponível.

Isso significa que habilitar `lang.typescript` em `:LazyExtras` ativa o `js-debug-adapter` além do `ts_ls` — tudo integrado.

#### O que a UI do nvim-dap-ui mostra

Quando uma sessão de debug está ativa e a UI está aberta (`<leader>du`), os splits padrão são:

- **Scopes** (esquerda, cima) — variáveis locais e globais do frame selecionado na call stack. Expandível por tipo/objeto.
- **Watches** (esquerda, meio) — expressões que você adicionou manualmente pra monitorar durante toda a sessão; atualizadas a cada passo.
- **Stacks** (direita) — call stack completa; clicar em um frame diferente muda o contexto de scopes (útil pra inspecionar quem chamou quem).
- **Breakpoints** (direita, baixo) — lista de todos os breakpoints ativos, com condição se houver.
- **Console** / **REPL** — output do programa e prompt interativo.

A disposição exata é configurável em `opts` do `nvim-dap-ui`, mas o default cobre o essencial sem configuração adicional.

#### Quando usar snippets vs templates vs LSP completions

Três ferramentas cobrem "geração de código" e frequentemente se sobrepõem:

| Ferramenta | Melhor pra | Limitação |
|---|---|---|
| **Snippet** | Boilerplate com estrutura fixa e campos editáveis | Não tem contexto semântico do código |
| **LSP completion** | Completar símbolos existentes, imports automáticos | Não expande estruturas multi-linha |
| **Template de arquivo** | Criar arquivo inteiro com estrutura padrão | Não opera dentro de arquivos existentes |

Snippets brilham pra padrões repetitivos que o LSP não gera: estrutura de test, bloco try-catch com campos nomeados, componente React com props tipadas. Quando um snippet fica genérico demais, considere usar `function_node` pra gerar partes do código com base no contexto.

---

## Na prática

### Snippets

#### Listar snippets disponíveis

Com LuaSnip + friendly-snippets instalados (default LazyVim), para ver os snippets disponíveis no filetype atual:

```lua
:lua print(vim.inspect(require("luasnip").available()))
```

Retorna tabela com todos os snippets carregados para o filetype do buffer atual, com trigger e descrição.

#### Expandir um snippet

1. Em insert mode, digita o trigger (ex: `test`).
2. Pressiona `<Tab>` — LuaSnip expande.
3. Edita o tabstop `$1`; pressiona `<Tab>` pra avançar.
4. `<S-Tab>` volta ao tabstop anterior.
5. Ao chegar em `$0`, snippets mode encerra — `<Tab>` volta ao comportamento de nvim-cmp/indent.

> [!note] Interação com nvim-cmp
> Quando o popup de completion do cmp está aberto, `<Tab>` confirma a completion, não avança no snippet. Se o popup não está aberto, `<Tab>` navega no snippet. Essa ordem de prioridade é configurada em `lua/plugins/nvim-cmp.lua`.

#### Criar snippet em formato VS Code JSON (portável)

Arquivo: `~/.config/nvim/snippets/typescript.json`

```json
{
  "Test boilerplate": {
    "prefix": "test",
    "body": [
      "describe(\"$1\", () => {",
      "  it(\"$2\", () => {",
      "    $0",
      "  });",
      "});"
    ],
    "description": "Jest/Vitest test"
  }
}
```

Para carregar o diretório custom, adicione em `lua/plugins/luasnip.lua`:

```lua
return {
  "L3MON4D3/LuaSnip",
  opts = function(_, opts)
    opts.history = true
    opts.delete_check_events = "TextChanged"
  end,
  config = function(_, opts)
    require("luasnip").setup(opts)
    -- Carrega snippets VS Code do diretório custom
    require("luasnip.loaders.from_vscode").lazy_load({ paths = "./snippets" })
    -- friendly-snippets já é carregado pelo LazyVim; esta linha adiciona o dir custom
  end,
}
```

> [!tip] Caminho relativo
> `"./snippets"` é relativo ao CWD quando o Neovim abre. Para um path absoluto garantido: `vim.fn.stdpath("config") .. "/snippets"`.

#### Criar snippet em Lua puro (expressivo)

API Lua do LuaSnip — mais verbosa mas permite transformations, choice nodes e lógica arbitrária:

```lua
local ls = require("luasnip")
local s  = ls.snippet
local t  = ls.text_node
local i  = ls.insert_node

ls.add_snippets("typescript", {
  s("log", {
    t('console.log("'),
    i(1, "msg"),
    t('", '),
    i(0),
    t(");"),
  }),
})
```

Exemplo com transformation — gerar nome de teste a partir de nome de função:

```lua
local ls  = require("luasnip")
local s   = ls.snippet
local t   = ls.text_node
local i   = ls.insert_node
local f   = ls.function_node

ls.add_snippets("typescript", {
  s("testfn", {
    t("it(\"should "),
    f(function(args) return args[1][1]:lower() end, { 1 }),
    t({ '", () => {', "  " }),
    i(0),
    t({ "", "});" }),
  }),
})
```

Neste snippet, `$0` recebe o cursor final; o texto do `it(` é derivado do que foi digitado em `$1` (nome da função) em lowercase.

#### Carregar snippets Lua a partir de arquivo separado

Pra organizar snippets Lua em arquivos por linguagem (ao invés de todos em `luasnip.lua`), use o loader de Lua do LuaSnip:

```lua
-- lua/plugins/luasnip.lua
return {
  "L3MON4D3/LuaSnip",
  config = function(_, opts)
    require("luasnip").setup(opts)

    -- Carrega arquivos em lua/snippets/<ft>.lua automaticamente
    require("luasnip.loaders.from_lua").lazy_load({
      paths = vim.fn.stdpath("config") .. "/lua/snippets",
    })

    -- Também carrega VS Code JSON do dir custom
    require("luasnip.loaders.from_vscode").lazy_load({
      paths = vim.fn.stdpath("config") .. "/snippets",
    })
  end,
}
```

Estrutura de diretórios resultante:

```
~/.config/nvim/
├── lua/
│   └── snippets/
│       ├── typescript.lua   ← snippets Lua pra TS
│       └── markdown.lua     ← snippets Lua pra MD
└── snippets/
    └── typescript.json      ← snippets VS Code JSON pra TS
```

Cada arquivo Lua em `lua/snippets/<ft>.lua` deve retornar uma lista de snippets:

```lua
-- lua/snippets/typescript.lua
local ls = require("luasnip")
local s, t, i = ls.snippet, ls.text_node, ls.insert_node

return {
  s("iife", {
    t("(function () {"),
    t({ "", "  " }),
    i(0),
    t({ "", "})();" }),
  }),
}
```

---

### DAP

#### Quando usar DAP vs `console.log`

Debug com `console.log` (ou equivalente) é rápido pra casos simples, mas tem custo: você modifica o código, precisa lembrar de remover depois e não tem visibilidade do estado completo. DAP é superior quando:

- O bug aparece em condições específicas que exigem **breakpoint condicional** (parar só quando `count > 100`, por exemplo).
- Você precisa inspecionar o estado de **múltiplas variáveis ao mesmo tempo** sem logar cada uma.
- O bug está num loop de muitas iterações — breakpoint condicional poupa tempo vs logs.
- Você precisa entender o **call stack** — quem chamou quem e com quais argumentos.
- O ambiente de produção tem logs verbosos mas você precisa de contexto local preciso.

`console.log` ainda é útil pra confirmar "chegou aqui" rápido, ou quando o overhead de iniciar uma sessão DAP não compensa. O snippet de `log` (definido acima) ajuda exatamente nesse caso — digita `log<Tab>`, escreve a mensagem, salva. Se for manter longo prazo, DAP.

#### Habilitar o Extra de debug

1. Abre `:LazyExtras` (ou `<leader>L` → Extras).
2. Busca `lang.typescript` (ou a linguagem desejada).
3. Pressiona `x` pra toggle (ativar).
4. Fecha e roda `:Lazy sync` pra instalar os plugins e adapters.

O Extra instala automaticamente o adapter via Mason. Verificar instalação: `:Mason` → filter por "DAP".

#### Keymaps default LazyVim (após Extra ativo)

| Keymap | Ação |
|---|---|
| `<leader>db` | Toggle breakpoint na linha |
| `<leader>dB` | Breakpoint condicional (prompt de expressão) |
| `<leader>dc` | Continue (inicia ou continua sessão) |
| `<leader>di` | Step into |
| `<leader>do` | Step out |
| `<leader>dO` | Step over |
| `<leader>dr` | Toggle REPL |
| `<leader>du` | Toggle UI (nvim-dap-ui) |
| `<leader>dn` | Run nearest test (quando Extra define) |
| `<leader>dl` | Run last debug config |

#### Interop com `.vscode/launch.json`

Se o projeto tem `.vscode/launch.json`, nvim-dap lê automaticamente as configs via o plugin equivalente incluído no Extra (ex: `nvim-dap-vscode-js` pra Node). Configs de VS Code funcionam direto — útil em projetos de time que já usam VS Code.

Exemplo de `launch.json` pra Node/TS:

```json
{
  "version": "0.2.0",
  "configurations": [
    {
      "type": "node",
      "request": "launch",
      "name": "Debug index.ts",
      "program": "${workspaceFolder}/src/index.ts",
      "runtimeArgs": ["-r", "ts-node/register"],
      "sourceMaps": true,
      "outFiles": ["${workspaceFolder}/dist/**/*.js"]
    }
  ]
}
```

#### Fluxo de debug passo a passo

**1. Coloca breakpoint**

Vai até a linha de interesse, pressiona `<leader>db`. Um sinal aparece no gutter (coluna esquerda). Para breakpoint condicional — `<leader>dB` — o DAP pede uma expressão na linguagem do programa (ex: `count > 10` em TS).

**2. Inicia sessão**

`<leader>dc` (continue/start) abre popup pra escolher a config de debug (do `launch.json` ou definida pelo Extra). Seleciona e confirma.

**3. Execução para no breakpoint**

O DAP suspende a execução. A UI do `nvim-dap-ui` abre automaticamente com splits:

- **Scopes** — variáveis locais e de fechamento no frame atual.
- **Watches** — expressões monitoradas manualmente.
- **Stacks** — call stack; clicar num frame muda o contexto de inspeção.
- **Breakpoints** — lista de todos os breakpoints ativos.

**4. Inspecionar variáveis**

Hover com `K` sobre uma variável no buffer (quando nvim-dap-ui está ativo) mostra o valor atual em popup. `<leader>du` toggle a UI se fechou. Para adicionar uma variável ao painel Watches: posicione o cursor sobre ela e use `:lua require("dap.ui.widgets").hover()` ou configure um keymap pra `dap.ui.widgets`.

**5. Navegar na execução**

- `<leader>di` — step into (entra na função chamada).
- `<leader>dO` — step over (executa linha sem entrar em funções).
- `<leader>do` — step out (executa até sair da função atual).
- `<leader>dc` — continue até próximo breakpoint ou fim.

A granularidade de step é importante: `step into` é útil pra entrar em uma função suspeita; `step over` pra avançar na lógica sem se perder em detalhes de implementação; `step out` pra sair de uma função que já inspecionou o suficiente.

**6. Breakpoints programáticos via Lua**

Além dos keymaps interativos, é possível definir breakpoints via API Lua — útil pra scripts de setup de debug:

```lua
-- Breakpoint simples
require("dap").toggle_breakpoint()

-- Breakpoint condicional
require("dap").set_breakpoint("count > 10")

-- Breakpoint com log message (não para, só loga)
require("dap").set_breakpoint(nil, nil, "chegou aqui: count=%d {count}")
```

O terceiro argumento de `set_breakpoint` é um `log_message` — o adapter imprime no console sem parar a execução. Equivalente ao `console.log` de debug, mas sem modificar o código.

**7. REPL interativo**

`<leader>dr` abre o REPL do DAP — uma janela onde você digita expressões na linguagem do programa e vê o resultado em tempo real no contexto do frame pausado. Útil pra testar hipóteses sem reiniciar. Exemplos em TS no REPL: `user.name`, `arr.length`, `JSON.stringify(obj)`.

**8. Encerrar sessão**

Quando terminar, `<leader>dq` (ou `:DapTerminate`) encerra a sessão e a UI fecha. Breakpoints persistem entre sessões — eles são mantidos em memória pelo nvim-dap até você removê-los explicitamente com `<leader>db` (toggle off) ou `:DapClearBreakpoints`.

---

## Armadilhas

### 1. (Snippets) Conflito de `<Tab>` com nvim-cmp

Em LazyVim default, `<Tab>` tem prioridade para confirmar a seleção do popup de completion do nvim-cmp. Se o popup está aberto, `<Tab>` **não** navega para o próximo tabstop — ele aceita a completion. O comportamento esperado: feche o popup com `<Esc>` ou `<C-e>` antes de avançar no snippet, ou ajuste a config de prioridade em `lua/plugins/nvim-cmp.lua` para dar precedência ao LuaSnip quando dentro de um snippet ativo.

### 2. (Snippets) Esquecer `$0` no snippet

`$0` marca a posição final do cursor após navegar por todos os tabstops. Sem ele, o LuaSnip encerra o snippet mode no último `$N` declarado — o que pode parecer um bug quando `<Tab>` para de funcionar inesperadamente ou o cursor fica em posição estranha.

### 3. (Snippets) Custom dir não carregado

`require("luasnip.loaders.from_vscode").lazy_load({ paths = "./snippets" })` precisa ser chamado no `config` (não em `opts`) do plugin, pois depende do LuaSnip já inicializado. LazyVim faz isso automaticamente pra `friendly-snippets`; para diretórios custom, é preciso adicionar explicitamente. Caminho relativo resolve com base no CWD — prefira `vim.fn.stdpath("config") .. "/snippets"` para robustez.

### 4. (DAP) Adapter não instalado

A mensagem `"session ended early"` ou `"no adapter found for <filetype>"` quase sempre significa que o adapter não está instalado. Verificar: `:Mason` → filtrar por "DAP". Para Node/TS, o adapter é `js-debug-adapter`. Instalar manualmente via `:MasonInstall js-debug-adapter` ou garantir que `mason-nvim-dap` tem o adapter na lista `ensure_installed`.

### 5. (DAP) Breakpoint condicional com expressão Lua

O campo de expressão em `<leader>dB` espera código **na linguagem do programa**, não em Lua. Em TypeScript/JavaScript, escreva `count > 10`; em Python, `item is None`. Escrever sintaxe Lua causa falha silenciosa — o breakpoint existe mas nunca para a execução.

### 6. (DAP) `launch.json` com campos não suportados

Alguns campos do `launch.json` do VS Code (`preLaunchTask`, `postDebugTask`, integrações de build) não têm suporte no nvim-dap. O DAP do Neovim faz parse parcial e ignora campos desconhecidos sem erro explícito. Se a sessão não inicia como esperado, verifique o log DAP: `:lua require("dap").set_log_level("DEBUG")` e depois `:e ~/.cache/nvim/dap.log` pra ver o que foi passado pro adapter.

---

## Em inglês

| PT-BR | EN |
|---|---|
| trecho de código | snippet |
| gatilho | trigger |
| parada de tab | tabstop |
| placeholder | placeholder |
| expansão | expansion |
| depurador | debugger |
| ponto de parada | breakpoint |
| passo (debug) | step |
| depurar | debug |
| REPL | REPL (Read-Eval-Print Loop) |
| modo de inserção | insert mode |
| sessão de depuração | debug session |

---

## Veja também

- [[04 - LazyVim tour]] — keymaps default de cmp e snippets, overview do bundle
- [[09 - LSP no Neovim]] — LSP, Mason e conform compartilham infraestrutura com DAP
- [[12 - Treesitter avançado]] — Treesitter cobre estrutura estática (AST); DAP cobre comportamento em runtime
- [[06 - Estrutura de config]] — onde colocar plugin spec de LuaSnip e nvim-dap
- [[08 - Customizando LazyVim]] — como habilitar Extras via `:LazyExtras`
- [[03-Dominios/Tecnologia/Terminal/Editor/index|MOC do galho]]
- [[Dicionário do Terminal#Snippet|snippet]], [[Dicionário do Terminal#LuaSnip|LuaSnip]], [[Dicionário do Terminal#DAP|DAP]], [[Dicionário do Terminal#Mason|Mason]]

---

## Referências

- <https://github.com/L3MON4D3/LuaSnip>
- <https://github.com/L3MON4D3/LuaSnip/blob/master/DOC.md>
- <https://github.com/mfussenegger/nvim-dap>
- <https://github.com/rcarriga/nvim-dap-ui>
- <https://microsoft.github.io/debug-adapter-protocol/>
- <https://github.com/rafamadriz/friendly-snippets>
- <https://www.lazyvim.org/extras>
- <https://www.youtube.com/@teej_dv> (TJ DeVries — DAP overview)
