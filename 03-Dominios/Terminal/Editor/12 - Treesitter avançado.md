---
title: "Treesitter avançado"
created: 2026-05-19
updated: 2026-05-19
type: concept
progress: backlog
status: seedling
publish: true
fase: magus
tags:
  - terminal
  - editor
  - magus
  - treesitter
  - ast
  - textobjects
aliases:
  - Treesitter
---

# Treesitter avançado

> [!abstract] TL;DR
> Treesitter dá ao Neovim [[Dicionário do Terminal#AST|AST]] por linguagem em tempo real. Beneficia highlight (preciso vs regex), [[Dicionário do Terminal#Text object|text objects]] estruturais (`af` = around function), navegação por nó, e [[Dicionário do Terminal#Query|queries]] customizadas pro seu workflow.

## O que é / Como funciona

### O problema que resolve

O highlight tradicional do Vim usa regex sobre regiões de syntax (`:syntax on`). Funciona para linguagens simples, mas é frágil para linguagens com sintaxe rica — TypeScript, JSX, Rust. Um comment multi-linha, uma template string, um JSX expression dentro de atributo: qualquer um desses pode quebrar o regex e deixar o highlight incoerente por dezenas de linhas abaixo.

[[Dicionário do Terminal#Treesitter|Treesitter]] resolve isso com um parser por linguagem que gera uma [[Dicionário do Terminal#AST|AST]] incremental. Em vez de reler o arquivo inteiro a cada keystroke, o parser identifica qual nó da árvore mudou e re-parseia apenas aquela subárvore. O resultado é highlight contextualmente correto que nunca "quebra" por causa de uma string mal fechada temporária.

### AST — árvore sintática abstrata

A AST (Abstract Syntax Tree) é a representação hierárquica da estrutura do código. Cada nó na árvore tem:

- **`kind`** — o tipo sintático do nó: `function_declaration`, `if_statement`, `call_expression`, `string`, `identifier`, etc.
- **`range`** — posição no arquivo: `start_row`, `start_col`, `end_row`, `end_col`.
- **filhos** — nós aninhados que compõem o nó pai.

Exemplo para `function foo(a, b) { return a + b; }`:

```
function_declaration          [0,0]–[0,38]
  name: identifier "foo"      [0,9]–[0,12]
  parameters: formal_parameters
    required_parameter        [0,13]–[0,14]
      pattern: identifier "a"
    required_parameter        [0,16]–[0,17]
      pattern: identifier "b"
  body: statement_block
    return_statement
      binary_expression
        left: identifier "a"
        operator: "+"
        right: identifier "b"
```

Use `:InspectTree` (built-in do Neovim 0.10+) para ver essa árvore ao vivo no buffer atual.

### Highlight via Treesitter

`nvim-treesitter` conecta parsers ao sistema de highlight. Para cada linguagem, há um arquivo `highlights.scm` com queries que mapeiam nós da AST para grupos de highlight:

```scheme
; highlights.scm do TypeScript (simplificado)
(function_declaration name: (identifier) @function)
(call_expression function: (identifier) @function.call)
(string) @string
(comment) @comment
```

O capture `@function` é vinculado ao grupo `Function` do colorscheme. O resultado é highlight que reflete a estrutura real do código — não o que um regex infere dela.

### Textobjects estruturais

Com `nvim-treesitter-textobjects` (Extra no LazyVim), text objects passam a mapear para nós da AST em vez de caracteres delimitadores:

**Text objects disponíveis (padrão LazyVim):**

| Text object | Significado                               |
| ----------- | ----------------------------------------- |
| `af` / `if` | around / inner function                   |
| `ac` / `ic` | around / inner class                      |
| `aa` / `ia` | around / inner argument (parâmetro)       |
| `al` / `il` | around / inner loop                       |
| `aB` / `iB` | around / inner block (genericamente)      |

O comportamento exato varia por linguagem: o que é "função" em Python é diferente do que é em TypeScript (método de classe, arrow function, function declaration). O treesitter-textobjects usa queries por linguagem para definir o que cada text object seleciona.

Uso com operadores padrão:

```vim
daf          " deleta a função inteira (around: inclui assinatura + corpo)
yif          " yank o corpo interno da função
cic          " change o conteúdo interno da classe
vaa          " visual select o argumento incluindo vírgula
```

### Motions estruturais

Além de text objects, `nvim-treesitter-textobjects` fornece motions para navegar entre nós da mesma categoria:

```vim
]f   " próxima função
[f   " função anterior
]c   " próxima classe
[c   " classe anterior
]a   " próximo argumento
[a   " argumento anterior
```

Esses motions são contextuais à linguagem do buffer — funcionam em TypeScript, Python, Rust, Go, etc., desde que o parser esteja instalado.

### Swap e move de argumentos

LazyVim (com o Extra `nvim-treesitter-textobjects`) define keymaps para reordenar argumentos mantendo a estrutura correta:

```vim
<leader>a    " swap argument com o próximo
<leader>A    " swap argument com o anterior
```

Isso é estruturalmente correto — o swap age sobre nós da AST, não sobre texto delimitado por vírgula. Funciona mesmo com argumentos multi-linha ou com funções como valores.

### Inspecionando a AST com `:InspectTree` e `:Inspect`

**`:InspectTree`** — abre um split mostrando a AST do buffer atual. Movendo o cursor no código, o nó correspondente é destacado na árvore. Movendo o cursor na árvore, o range correspondente é destacado no código. Ferramenta essencial pra escrever queries.

```vim
:InspectTree     " abre split com AST do buffer
" (built-in Neovim 0.10+, não requer nvim-treesitter)
```

**`:Inspect`** — mostra os captures do Treesitter e grupos de highlight sob o cursor:

```vim
:Inspect
" Output exemplo:
" Treesitter
"   @function.call vim.treesitter.query (line 42)
"   @function.method.call (line 42)
" Syntax
"   ...
```

Útil para descobrir por que um token está com determinada cor, ou qual capture está ativo antes de escrever uma query.

### Queries — pattern matching na AST

Queries são arquivos `.scm` (S-expression) que definem padrões para casa contra a AST. São a linguagem que conecta Treesitter a funcionalidades como highlight, text objects, indentation e custom tooling.

**Sintaxe básica:**

```scheme
; Casa qualquer function_declaration
(function_declaration)

; Casa function_declaration e captura o nome
(function_declaration name: (identifier) @function.name)

; Predicate: casa apenas se o nome começa com "test_"
(function_declaration
  name: (identifier) @function.test
  (#match? @function.test "^test_"))

; any-of?: casa se o identificador é um dos valores listados
(call_expression
  function: (identifier) @function.test
  (#any-of? @function.test "describe" "it" "test" "beforeEach" "afterEach"))
```

**Onde ficam os arquivos de query:**

- Built-in do parser (instalados via `:TSInstall`): `~/.local/share/nvim/lazy/nvim-treesitter/queries/<lang>/`
- Override / extensão local: `~/.config/nvim/after/queries/<lang>/`

**A diretiva `;; extends`:**

```scheme
;; extends
; Adiciona ao highlight default, sem substituir
(call_expression
  function: (identifier) @keyword.test
  (#any-of? @keyword.test "describe" "it" "test"))
```

Sem `;; extends`, o arquivo substitui completamente o default da linguagem. Com ela, o que está no arquivo é adicionado ao que já existe. Use `extends` pra customizações locais.

**Predicates disponíveis:**

| Predicate          | Função                                                         |
| ------------------ | -------------------------------------------------------------- |
| `#match?`          | regex match no texto do nó                                     |
| `#eq?`             | igualdade exata                                                |
| `#any-of?`         | nó igual a qualquer um dos valores listados                    |
| `#is?` / `#is-not?`| metadata predicates (ex: verificar se nó está em determinado contexto) |
| `#has-ancestor?`   | verifica se o nó tem um ancestral de determinado tipo          |

## Na prática

### Exemplo 1 — Navegação e edição estrutural em TypeScript

Cenário: refatorar uma função grande, movendo argumentos e extraindo o corpo.

```ts
// Arquivo: src/api/user.ts
async function fetchUserData(userId: string, options: RequestOptions) {
  const response = await fetch(`/api/users/${userId}`, options);
  return response.json();
}
```

```vim
" Cursor dentro da função:
af           " seleciona a função inteira (assinatura + corpo)
yaf          " yank a função completa pra colar em outro arquivo

" Cursor em 'userId':
]a           " move para o próximo argumento (options)
<leader>A    " swap: 'options' vai pra frente, 'userId' fica depois
" Resultado: fetchUserData(options: RequestOptions, userId: string)

" Extrair corpo pra nova função:
dif          " deleta o corpo interno (mantém assinatura)
```

### Exemplo 2 — Swap de argumentos em função com tipos complexos

```ts
function mergeConfigs(
  base: DeepPartial<Config>,
  override: Partial<Config>,
  metadata?: Record<string, unknown>
) {
  // ...
}
```

```vim
" Cursor em 'base' (primeiro argumento):
<leader>a    " swap com next → 'override' fica primeiro, 'base' segundo
" Resultado correto mesmo com tipos multi-linha e opcional no final
```

Comportamento diferente de uma substituição regex: o swap age sobre os nós `required_parameter` e `optional_parameter` da AST, preservando os tipos e a vírgula de separação corretamente.

### Exemplo 3 — Query customizada para destacar funções de teste

Criar o arquivo `~/.config/nvim/after/queries/typescript/highlights.scm`:

```scheme
;; extends
(call_expression
  function: (identifier) @keyword.test
  (#any-of? @keyword.test "describe" "it" "test" "beforeEach" "afterEach" "beforeAll" "afterAll"))
```

Após salvar, recarregar o buffer TypeScript com `:e`. Os nomes de funções de teste ganharão highlight distinto (mapeado para o grupo `@keyword.test` do colorscheme).

Para o mesmo em JavaScript:

```
~/.config/nvim/after/queries/javascript/highlights.scm
```

Conteúdo idêntico — as queries não são compartilhadas entre linguagens, mesmo quando a estrutura da AST é parecida (TypeScript e JavaScript têm parsers distintos no Treesitter).

### Exemplo 4 — Usando `:InspectTree` para entender a AST antes de escrever uma query

Cenário: quero escrever uma query que capture apenas arrow functions atribuídas a `const`, não function declarations.

```ts
const handler = (req, res) => { res.send(200); };
function middleware(req, res, next) { next(); }
```

Passos:

```vim
:InspectTree
" O split mostra a AST do buffer
" Mover cursor sobre 'handler =':
```

```
lexical_declaration           " a const declaration
  variable_declarator
    name: identifier "handler"
    value: arrow_function
      parameters: formal_parameters
      body: statement_block
```

```vim
" Mover cursor sobre 'function middleware':
```

```
function_declaration
  name: identifier "middleware"
  parameters: formal_parameters
  body: statement_block
```

Com essa informação, escrever a query que casa apenas arrow functions em declarações:

```scheme
;; extends
(lexical_declaration
  (variable_declarator
    value: (arrow_function) @function.arrow))
```

Sem `:InspectTree`, seria necessário consultar a documentação do parser específico (tree-sitter-typescript) ou adivinhar os nomes dos nós.

### Exemplo 5 — Verificar captura ativa antes de customizar

```vim
" Cursor em cima de 'describe' num arquivo de teste TypeScript
:Inspect

" Output:
" Treesitter highlights:
"   @function.call › @function — 'function.call'
" Active highlight groups:
"   @function.call  (links to Function)
```

Com isso, sabemos que `describe` está sendo capturado como `@function.call`. A query customizada pode sobrescrever isso capturando o mesmo nó com `@keyword.test`, que tem prioridade se definida depois (ou via `;; extends`).

### Exemplo 6 — Desabilitar Treesitter em arquivo grande

Em arquivos com 20k+ linhas, o parsing incremental pode causar lag perceptível (especialmente ao colar grandes blocos):

```vim
" Desabilitar Treesitter apenas para o buffer atual:
:lua vim.treesitter.stop()

" Reativar:
:lua vim.treesitter.start()
```

Ou para disable permanente por filetype, adicionar em `~/.config/nvim/lua/config/options.lua`:

```lua
vim.treesitter.language.register("nohl", "bigfile")
```

Alternativa: LazyVim tem um Extra `bigfile` que automaticamente desativa Treesitter (e LSP, format on save) para arquivos acima de um threshold configurável.

## Armadilhas

### 1. Parser não instalado silenciosamente

Sem o parser da linguagem, Treesitter não funciona — e falha silenciosamente. O highlight cai de volta para o regex-based syntax sem aviso. Checar:

```vim
:checkhealth nvim-treesitter
" Mostra parsers instalados, ausentes e desatualizados

:TSInstall typescript      " instala o parser de TypeScript
:TSInstall tsx             " TS e TSX são parsers DISTINTOS
:TSUpdate                  " atualiza todos os instalados
```

LazyVim auto-instala os parsers mais comuns (TS, JS, Lua, Python, etc.) via `ensure_installed` no setup. Parsers menos comuns precisam de `:TSInstall` manual.

### 2. `af` e `]f` não funcionam em filetype sem textobjects configurado

Os text objects e motions estruturais requerem `nvim-treesitter-textobjects` e queries específicas por linguagem. Se o filetype não tem queries de textobjects definidas, `af` silenciosamente não faz nada (ou recai sobre o text object padrão de outro plugin).

Checar se há queries de textobjects pra linguagem:

```vim
:TSEditQuery textobjects
" Abre o arquivo .scm de textobjects da linguagem atual (se existir)
```

Se o arquivo não existir, o text object estrutural não está disponível para esse filetype.

### 3. Query syntax frágil e falha silenciosa

Um parêntese errado ou vírgula extra na query `.scm` faz a query inteira falhar sem mensagem de erro visível — o highlight simplesmente não aplica. Debugar:

```vim
:checkhealth nvim-treesitter
" Pode apontar erros em queries customizadas

:lua vim.treesitter.query.parse("typescript", "(call_expression function: (identifier) @fn)")
" Se a query for inválida, mostra erro no output
```

Escrever queries incrementalmente: começar com o pattern mais simples possível, testar, adicionar predicates um a um.

### 4. Highlight piora ao desabilitar Treesitter em linguagens sem boa syntax

Em linguagens como TypeScript e JSX, o highlight baseado em regex (`:syntax on`) é notavelmente mais fraco. Desabilitar Treesitter nesses casos resulta em perda real de informação visual — JSX attributes, template literals e type annotations ficam sem cor ou com coloração incorreta.

O regex-based syntax foi o estado da arte pré-2018. Treesitter é o padrão atual, e desabilitá-lo é um downgrade funcional, não apenas visual.

### 5. `;; extends` ausente substitui todo o highlight da linguagem

Criar `after/queries/typescript/highlights.scm` sem a diretiva `;; extends` na primeira linha faz o arquivo substituir completamente o highlight padrão do TypeScript — resultado: apenas os captures definidos no seu arquivo ganham highlight; todo o resto perde cor.

Sempre iniciar arquivos de override com:

```scheme
;; extends
```

A não ser que a intenção seja realmente substituir completamente.

### 6. TSX e TypeScript são parsers distintos

Um arquivo `.tsx` usa o parser `tsx`, não `typescript`. Queries criadas em `after/queries/typescript/` não se aplicam automaticamente a arquivos `.tsx`. É preciso criar o arquivo equivalente em `after/queries/tsx/` com o mesmo conteúdo (ou com diferenças JSX-específicas).

```
after/queries/typescript/highlights.scm   → arquivos .ts
after/queries/tsx/highlights.scm          → arquivos .tsx
```

## Em inglês

| PT-BR                        | EN                                         |
| ---------------------------- | ------------------------------------------ |
| árvore sintática abstrata    | abstract syntax tree (AST)                 |
| parser                       | parser                                     |
| captura                      | capture                                    |
| consulta                     | query                                      |
| nó                           | node                                       |
| nó filho                     | child node                                 |
| nó ancestral                 | ancestor node                              |
| declaração de função         | function declaration                       |
| declaração de arrow function | arrow function declaration                 |
| bloco                        | block                                      |
| incremental                  | incremental                                |
| predicado                    | predicate                                  |
| tipo de nó                   | node kind / node type                      |
| alcance / intervalo          | range (start/end row + col)                |
| text object estrutural       | structural text object                     |
| extensão de query            | query extension (`;; extends`)             |
| destaque / coloração         | highlight / syntax highlighting            |
| análise léxica               | parsing / lexical analysis                 |
| sobreposição                 | override (no contexto de queries)          |
| desativar por buffer         | buffer-local disable                       |

**Abstract Syntax Tree (AST)** (EN): A hierarchical, language-agnostic representation of source code structure. Each node has a `kind` (e.g. `function_declaration`), a `range` (start/end row+col), and child nodes. Treesitter generates and incrementally updates this tree as the user types.

**Capture** (EN): A named binding in a Tree-sitter query that matches a specific node or token, annotated with `@name` syntax. Captures are used by highlight, textobject, and custom query consumers to identify relevant AST nodes.

**Query** (EN): A pattern written in Tree-sitter's S-expression DSL (stored in `.scm` files) that matches against the AST. Composed of node patterns, field names, captures, and predicates (`#match?`, `#any-of?`, `#eq?`). Used to define highlights, textobjects, indentation, and custom analyses.

## Veja também

- [[02 - Motions, operadores e text objects]] — text objects base (fundação que textobjects estruturais estendem)
- [[09 - LSP no Neovim]] — complementar: Treesitter fornece estrutura local, LSP fornece semântica cross-file
- [[11 - Workflow avançado]] — quickfix + cdo é outro caminho de refactor em massa
- [[10 - Registers, marks, macros]] — macros combinados com text objects estruturais para automação
- [[03-Dominios/Terminal/Editor/index|MOC do galho]]
- [[Dicionário do Terminal#Treesitter|Treesitter]], [[Dicionário do Terminal#AST|AST]], [[Dicionário do Terminal#Query|query]], [[Dicionário do Terminal#Text object|text object]]

## Referências

- <https://github.com/nvim-treesitter/nvim-treesitter> — plugin de bootstrap: instalação de parsers, highlight, indentation
- <https://github.com/nvim-treesitter/nvim-treesitter-textobjects> — text objects e motions estruturais
- <https://neovim.io/doc/user/treesitter.html> — documentação oficial: API Lua, `:InspectTree`, `:Inspect`, vim.treesitter
- <https://tree-sitter.github.io/tree-sitter/using-parsers#pattern-matching-with-queries> — referência oficial de queries: S-expressions, captures, predicates
- <https://www.youtube.com/@teej_dv> — TJ DeVries (core contributor do Neovim): talks sobre Treesitter e queries
