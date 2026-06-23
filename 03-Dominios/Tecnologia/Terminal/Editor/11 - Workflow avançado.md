---
title: "Workflow avançado"
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
  - quickfix
  - workflow
  - refactoring
aliases:
  - Workflow avançado
  - Quickfix
---

# Workflow avançado

> [!abstract] TL;DR
> [[Dicionário do Terminal#Quickfix list|Quickfix]] é a lista global de "lugares pra ir/editar" em Neovim. Telescope manda resultados pra ela; `:cdo` aplica edição em todos. Sessions trazem layout de volta. Workflow que substitui muita ferramenta de IDE.

## O que é / Como funciona

### Quickfix list vs location list

O Neovim mantém dois tipos de lista de posições navegáveis:

| Característica  | Quickfix list             | Location list                |
| --------------- | ------------------------- | ---------------------------- |
| Escopo          | Global (uma por sessão)   | Local (uma por window/split) |
| Prefixo cmds    | `:c…` (`:copen`, `:cnext`) | `:l…` (`:lopen`, `:lnext`)  |
| Abrir           | `:copen`                  | `:lopen`                     |
| Navegar         | `:cnext` / `:cprev`       | `:lnext` / `:lprev`          |
| LazyVim keymap  | `]q` / `[q`               | `]l` / `[l`                  |
| Editar em massa | `:cdo <cmd>`              | `:ldo <cmd>`                 |
| Editar por arq  | `:cfdo <cmd>`             | `:lfdo <cmd>`                |

A mesma API, com prefixos distintos. A escolha depende do scope desejado: use quickfix para operações de projeto, location list para diagnósticos de uma janela específica (o LSP já usa location list internamente para alguns fluxos).

### Populando a quickfix list

Há várias formas de colocar itens na quickfix:

**Via grep externo (`:grep`)**

```vim
:grep -r "pattern" src/
```

O Neovim delega ao comando definido em `grepprg`. Para usar ripgrep:

```lua
-- em lua/config/options.lua
vim.opt.grepprg = "rg --vimgrep --smart-case"
vim.opt.grepformat = "%f:%l:%c:%m"
```

Com isso, `:grep` usa `rg` e popula a quickfix com resultados no formato `arquivo:linha:coluna:mensagem`.

**Via grep interno (`:vimgrep`)**

```vim
:vimgrep /pattern/ **/*.ts
```

Busca interna do Neovim. Mais lenta em projetos grandes, mas funciona sem dependências externas. O glob `**/*.ts` busca recursivamente.

**Via Telescope `<C-q>`**

Após qualquer busca no Telescope (live grep, LSP references, find files…), pressionar `<C-q>` manda os itens atualmente visíveis para a quickfix. Isso inclui apenas o que está na lista filtrada — limpar o input antes para enviar todos os resultados.

**Via LSP references + Telescope**

```
gr             " LSP references in Telescope
<C-q>          " send visible results to quickfix
```

Ou, para múltipla seleção antes de enviar: `<Tab>` em cada item no Telescope para marcar, depois `<C-q>`.

**Via make / compilação**

```vim
:make
```

Erros de compilação caem na quickfix se `makeprg` e `errorformat` estiverem configurados para o compilador/linter. Frameworks como Go, Rust, TypeScript têm `errorformat` prontos ou plugins dedicados.

**Via todo-comments.nvim**

```vim
:TodoQuickFix
```

Envia todos os `TODO:`, `FIXME:`, `HACK:`, `WARN:` do projeto para a quickfix. Bundle LazyVim, zero configuração.

### Navegação na quickfix

```vim
:copen       " abre o split da quickfix
:cclose      " fecha o split
:cnext       " próximo item (LazyVim: ]q)
:cprev       " item anterior (LazyVim: [q)
:cc N        " pula pro item N (ex: :cc 5)
:cfirst      " primeiro item
:clast       " último item
:cdo <cmd>   " executa <cmd> em CADA item da quickfix
:cfdo <cmd>  " executa <cmd> em cada ARQUIVO único da quickfix (uma vez por arquivo)
```

A diferença entre `:cdo` e `:cfdo` é relevante quando vários itens apontam para o mesmo arquivo. `:cdo` executa o comando uma vez por item (potencialmente N vezes no mesmo arquivo); `:cfdo` executa uma vez por arquivo, independente de quantos itens ele tem.

### Edição em massa com `:cdo`

O padrão básico de refactor com quickfix:

1. Popular a quickfix com os lugares afetados.
2. Rodar `:cdo s/old/new/g | update` para aplicar substituição e salvar.

O `| update` no final salva cada buffer apenas se houve mudança (diferente de `:w`, que salva mesmo sem alteração). Isso é importante para não tocar timestamps de arquivos não modificados.

**Padrão com LSP references:**

```vim
" Cursor no símbolo alvo
gr                           " LSP references → Telescope
<C-q>                        " send to quickfix
:cdo s/\<oldName\>/newName/g | update
```

**Padrão com grep:**

```vim
:grep -F "oldString" src/
:cdo s/oldString/newString/g | update
```

A flag `-F` no ripgrep trata o pattern como string literal (sem regex), útil para nomes com caracteres especiais.

**Padrão combinado com filter:**

Quando a quickfix retorna falsos positivos, abra com `:copen`, navegue aos itens indesejados e delete a linha no buffer da quickfix (o buffer qf é editável). Depois aplique `:cdo`.

### Sessions com persistence.nvim

LazyVim inclui `persistence.nvim` (Folke) por padrão. Uma session é um snapshot do layout de trabalho:

- Windows abertas e suas dimensões
- Buffers carregados (arquivos lidos de disco, não conteúdo em memória)
- Tabs
- Marks e registers
- Opções do Neovim para a sessão

**O que sessions NÃO salvam:** terminais embutidos (`:terminal`), jobs async em andamento, conteúdo de buffers não salvos.

**Keymaps LazyVim default:**

```
<leader>qs    " restore session do cwd atual
<leader>ql    " restore a última session usada
<leader>qd    " parar de salvar session atual (útil pra configs temp)
<leader>qS    " select session (Telescope, se habilitado)
```

Sessions ficam em `~/.local/state/nvim/sessions/`. O nome do arquivo é derivado do path do cwd.

**Sessions manuais (múltiplos projetos sem persistence):**

```vim
:mksession ~/sessions/myproject.vim     " salva
:source ~/sessions/myproject.vim        " restaura
```

Útil para alternar entre contextos diferentes no mesmo cwd, o que `persistence.nvim` não suporta diretamente (ele usa o cwd como chave).

### todo-comments.nvim

Bundle LazyVim. Destaca comentários com keywords específicas usando cores distintas:

| Keyword   | Cor típica | Semântica                          |
| --------- | ---------- | ---------------------------------- |
| `TODO:`   | Azul       | Trabalho pendente intencional      |
| `FIXME:`  | Vermelho   | Bug conhecido                      |
| `HACK:`   | Laranja    | Solução temporária / workaround    |
| `WARN:`   | Amarelo    | Atenção, potencial problema        |
| `NOTE:`   | Verde      | Observação explicativa             |
| `PERF:`   | Roxo       | Oportunidade de otimização         |

**Comandos:**

```vim
:TodoTelescope       " busca fuzzy todos os TODOs do projeto
:TodoQuickFix        " envia todos pra quickfix
:TodoLocList         " envia pra location list da window atual
```

**Keymaps LazyVim:**

```
<leader>st    " TodoTelescope
]t / [t       " próximo / anterior TODO no buffer
```

Combinação poderosa: `:TodoQuickFix` + `:cdo` para processar todos os FIXMEs de um projeto sistematicamente.

## Na prática

### Exemplo 1 — Refactor de método em projeto TypeScript

Cenário: renomear `getUserData` para `fetchUserProfile` em todo o projeto, garantindo que só references reais do LSP sejam afetadas (não strings em comentários).

```vim
" Cursor em cima de getUserData (qualquer ocorrência)
gr                              " LSP references → Telescope
" Inspecionar lista, remover falsos positivos com <Tab> se necessário
<C-q>                           " send to quickfix
:cdo s/\<getUserData\>/fetchUserProfile/g | update
" \< e \> são word boundaries — evita substituir 'getUserDataCached'
```

Verificar resultado:

```vim
:grep -F "getUserData" src/     " deve retornar zero resultados
```

### Exemplo 2 — Grep + review manual + edição em massa

Cenário: substituir `throw new Error` por `throw new AppError` em todos os arquivos `src/`, mas revisar antes para não alterar arquivos de teste.

```vim
:grep -F "throw new Error" src/
:copen                          " inspeciona a lista
" Navegar, ver contexto com <CR>, deletar linhas de arquivos .spec. no buffer qf
:cdo s/throw new Error/throw new AppError/g | update
```

### Exemplo 3 — Session para alternância de projetos

```bash
# Terminal: abre projeto A
cd ~/projects/api-service
nvim
```

```vim
" Em Neovim:
<leader>qs       " restore session anterior de ~/projects/api-service
" ... trabalha ...
" Fechar Neovim: persistence.nvim salva automaticamente ao sair
```

```bash
# Terminal: muda para projeto B
cd ~/projects/frontend-app
nvim
```

```vim
<leader>qs       " restore session de ~/projects/frontend-app
```

Cada cwd tem sua própria session independente.

### Exemplo 4 — TODOs como quickfix navegável

```vim
:TodoQuickFix
:copen
" Lista todos os TODO/FIXME/HACK/WARN do projeto com arquivo e linha
]q               " navega para o próximo TODO
[q               " volta para o anterior
<CR>             " abre o arquivo na linha do item
```

Útil para fazer triagem de débito técnico. Combinado com `:cdo`:

```vim
" Processar todos os FIXME com uma transformação:
:TodoQuickFix FIXME
:cdo s/\/\/ FIXME:/\/\/ FIXED:/g | update
```

### Exemplo 5 — vimgrep recursivo com filtro de extensão

Quando ripgrep não está disponível ou o projeto está em remote sem `rg`:

```vim
:vimgrep /TODO\|FIXME/ **/*.{ts,tsx,js}
:copen
```

O pattern usa `\|` para alternação no vimgrep (diferente de `|` no regex externo).

### Exemplo 6 — Quickfix para compile errors

Projeto Go com `makeprg` configurado:

```lua
-- em ftplugin/go.lua
vim.opt_local.makeprg = "go build ./..."
vim.opt_local.errorformat = "%f:%l:%c: %m"
```

```vim
:make
:copen
" Erros de compilação listados com arquivo e linha
]q               " próximo erro
```

## Armadilhas

### 1. `:cdo` em buffers com unsaved changes conflitantes

Se algum buffer referenciado na quickfix tem alterações não salvas, `:cdo` pode falhar ou se comportar inesperadamente — o Neovim tentará modificar um buffer "dirty". Antes de rodar `:cdo` em massa:

```vim
:wa              " salva todos os buffers abertos
" ou
:cdo s/old/new/g | update   " 'update' só salva se mudou, mas não resolve conflicts pré-existentes
```

Para inspecionar buffers com alterações: `:ls` mostra `+` nos buffers modificados.

### 2. Confundir `:cnext` (quickfix) com `:lnext` (location list)

São listas distintas. O LSP usa location list em alguns contextos (diagnósticos por window), enquanto grep usa quickfix. Misturar os comandos navega na lista errada silenciosamente.

Em LazyVim: `]q` / `[q` navega quickfix; `]l` / `[l` navega location list. Verificar qual lista está ativa com `:copen` vs `:lopen`.

### 3. Telescope `<C-q>` envia apenas os itens visíveis

Se você fuzzy-filtra os resultados no Telescope antes de apertar `<C-q>`, a quickfix recebe apenas os itens filtrados — não todos os results da busca original. Isso é intencional para workflows onde você quer excluir falsos positivos, mas pode ser um problema se você queria enviar tudo.

Para enviar todos sem filtro: limpe o input do Telescope (apagar o texto digitado) e então `<C-q>`.

### 4. `:grep` sobrescreve a quickfix sem confirmação

Se há uma quickfix carregada com um refactor parcialmente feito (alguns itens editados, outros não), rodar `:grep` para outra busca sobrescreve a lista sem aviso. Trabalho da sessão anterior é perdido.

Estratégias para evitar:

```vim
" Opção 1: usar location list para a nova busca (não toca a quickfix)
:lgrep "pattern" src/
:lopen

" Opção 2: salvar a quickfix em register antes
:copen
" ggVGy        " yank todo o conteúdo do buffer qf como referência

" Opção 3: completar o cdo antes de qualquer novo grep
:cdo s/old/new/g | update
:grep "newterm" src/          " agora pode sobrescrever com segurança
```

### 5. Sessions não persistem terminais embutidos

Terminais abertos com `:terminal` (ou `<leader>ft` em LazyVim) não são restaurados pelo `persistence.nvim`. Ao restaurar uma session, o layout de windows volta, mas splits que eram terminais aparecem como buffers vazios ou com o último arquivo aberto.

Comportamento aceitável: terminais são efêmeros por natureza (estado de shell não persiste entre sessões de trabalho). Recompõe em segundos. Evitar dependência de terminais em layouts complexos que precisam persistir.

## Em inglês

| PT-BR                       | EN                                    |
| --------------------------- | ------------------------------------- |
| lista de quickfix           | quickfix list                         |
| lista de localização        | location list                         |
| correção em massa           | bulk edit / batch replace             |
| refatoração                 | refactoring                           |
| referências (LSP)           | references                            |
| sessão                      | session                               |
| restaurar                   | restore                               |
| arquivo único               | single file (contexto: `:cfdo`)       |
| janela ativa                | active window                         |
| pesquisar globalmente       | global search                         |
| escopo (global vs janela)   | scope (global vs window)              |
| padrão de limite de palavra | word boundary (ex: `\<word\>`)        |
| buffer sujo                 | dirty buffer / buffer with unsaved changes |

**Quickfix list** (EN): A global list of file positions (search results, compile errors, LSP references, TODOs) that Neovim maintains for navigation and batch editing. Commands prefixed with `c`. The location list (`:l…`) is its window-local counterpart.

**`:cdo`** (EN): Execute a command on each entry in the quickfix list, visiting each file in sequence. `:cfdo` does the same but once per unique file, regardless of how many entries that file has.

## Veja também

- [[03 - Edição e navegação]] — busca e navegação base (a fundação do que quickfix estende)
- [[09 - LSP no Neovim]] — LSP references alimenta a quickfix via Telescope `<C-q>`
- [[10 - Registers, marks, macros]] — substituto em casos simples; macros para edição iterativa sem quickfix
- [[12 - Treesitter avançado]] — outro caminho de refactor, estrutural via AST
- [[03-Dominios/Tecnologia/Terminal/Editor/index|MOC do galho]]
- [[Dicionário do Terminal#Quickfix list|quickfix list]]

## Referências

- <https://neovim.io/doc/user/quickfix.html> — documentação oficial da quickfix list
- <https://neovim.io/doc/user/quickfix.html#location-list> — location list, diferenças e API
- <https://neovim.io/doc/user/starting.html#session-file> — session files: mksession e source
- <https://github.com/folke/persistence.nvim> — persistence.nvim: session management para LazyVim
- <https://github.com/folke/todo-comments.nvim> — todo-comments.nvim: highlight e quickfix de TODOs
- <https://learnvimscriptthehardway.stevelosh.com/> — Vim script avançado: errorformat, grepprg, makeprg
