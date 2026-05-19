---
title: "LazyVim tour"
created: 2026-05-19
updated: 2026-05-19
type: concept
status: seedling
publish: true
fase: iniciado
tags:
  - terminal
  - editor
  - iniciado
  - lazyvim
  - tour
aliases:
  - LazyVim tour
  - LazyVim defaults
---

# LazyVim tour

> [!abstract] TL;DR
> LazyVim é uma [[Dicionário do Terminal#Distribuição|distribuição]] Neovim que vem com ~50 plugins pré-configurados e keymaps coerentes. Esta nota é um tour: o que vem ligado, qual key usa, e quando consultar [[Dicionário do Terminal#which-key|which-key]] pra descobrir o resto. Não configura nada — só usa.

## O que é / Como funciona

### Distribuição: Neovim com baterias incluídas

Neovim "vanilla" é um editor poderoso mas nu. Para ter fuzzy finder, LSP, file explorer, auto-complete e git integration funcionando, você precisa escolher ~20 plugins, entender como cada um se configura em Lua, e fazer tudo conversar. Semanas de yak shaving.

Uma [[Dicionário do Terminal#Distribuição|distribuição]] resolve isso: é um preset opinado de plugins + configuração + keymaps que funciona de saída. Você clona, abre o Neovim, e em 2-3 minutos o editor está completo. Outros exemplos de distribuições: LunarVim, AstroNvim, NvChad, kickstart.nvim.

[[Dicionário do Terminal#LazyVim|LazyVim]] é a distribuição mantida por Folke Lemaitre (o mesmo autor do lazy.nvim, tokyonight, flash.nvim). É a mais adotada na comunidade em 2026, e o setup que estas notas assumem.

### O que vem incluído

O bundle principal do LazyVim inclui (não exaustivo):

| Categoria | Plugin | Papel |
|---|---|---|
| Plugin manager | lazy.nvim | Instala, carrega e atualiza plugins |
| Fuzzy finder | Telescope | Busca arquivos, grep, buffers, help |
| File explorer | neo-tree | Árvore lateral de arquivos |
| Descoberta de keys | which-key | Popup de keymaps ao pressionar prefix |
| LSP client | nvim-lspconfig | Conecta aos language servers |
| LSP installer | Mason | Instala/gerencia language servers |
| Auto-complete | nvim-cmp | Popup de completions (LSP + snippets) |
| Formatter | conform.nvim | Format on save |
| Linter | nvim-lint | Diagnósticos extras |
| Statusline | lualine.nvim | Barra de status na base |
| Bufferline | bufferline.nvim | Buffers como tabs visuais no topo |
| Tema | tokyonight | Colorscheme default |
| Git | gitsigns.nvim | Hunks, blame, diff no gutter |
| Surround | nvim-surround | Add/change/delete delimitadores |
| Comment | Comment.nvim | Toggle comentários |
| Autopairs | nvim-autopairs | Fecha `(`, `[`, `{`, `"` automaticamente |
| Snippets | LuaSnip | Engine de snippets |
| Terminal | toggleterm.nvim | Terminal flutuante integrado |

### Instalação em uma linha

```bash
git clone https://github.com/LazyVim/starter ~/.config/nvim && nvim
```

Na primeira abertura o lazy.nvim baixa todos os plugins declarados. Não há mais nada a fazer. Quem está lendo esta nota já passou por isso — o foco aqui é usar o que veio instalado.

### Filosofia: use defaults, customize on top

A maneira certa de usar o LazyVim: **não lute contra os defaults**. Se um keymap parece errado, descubra primeiro o que o LazyVim espera que você faça antes de sobrescrever. Customização e override são tema das notas [[06 - Estrutura de config]] e [[08 - Customizando LazyVim]] — não desta.

Essa filosofia existe porque a maior parte do custo de manter um config Neovim customizado é reconciliar mudanças upstream com as suas. Quanto menos você divergir dos defaults, menos trabalho de manutenção. Usuários experientes de LazyVim tendem a ter configs surpreendentemente pequenas — a distribuição já fez a maior parte do trabalho.

### `<leader>` é `<Space>`

Antes de qualquer keymap: no LazyVim o `<leader>` é a tecla `<Space>`. Ao longo de toda esta nota, `<leader>X` significa `<Space>X`. Se você vem de configs com `,` como leader, adapte os dedos — não tente mudar o leader no início.

A escolha de `<Space>` como leader é intencional: é a tecla mais acessível do teclado, pressionada pelo polegar, e não tem nenhuma função em modo normal no Vim default. Isso a torna ideal para um namespace de keymaps sem conflitos.

### Versão assumida nesta nota

Esta nota assume **LazyVim versão de 2026-05-19** (conforme o MOC do galho). Keymaps do LazyVim mudam entre versões — sempre verifique com `:Lazy` (versão atual do bundle) e consulte [lazyvim.org/keymaps](https://www.lazyvim.org/keymaps) para a referência canônica atualizada. Keymaps marcados "(verificar versão)" são pontos onde houve mudança recente de comportamento entre versões.

## Na prática

### Telescope (fuzzy finder)

[[Dicionário do Terminal#Telescope|Telescope]] é o motor de busca do LazyVim. Quase toda operação de "encontrar algo" passa por ele.

**Keymaps principais:**

| Key | Ação |
|---|---|
| `<leader>ff` | Find files no projeto (git-aware, respeita `.gitignore`) |
| `<leader>fF` | Find files sem filtro — inclui hidden e gitignored |
| `<leader>fg` | Live grep (busca por texto em todo o projeto) |
| `<leader>,` | Switch buffer (lista buffers abertos) |
| `<leader>fr` | Recent files |
| `<leader>fh` | Help tags (fuzzy sobre `:help`) |
| `<leader>sk` | Search keymaps (lista todos os keymaps definidos) |
| `<leader>sn` | Search notes (snippets) |
| `<leader>sd` | Search diagnostics |
| `<leader>sw` | Search word under cursor (grep do termo atual) |

**Dentro do prompt Telescope:**

| Key | Ação |
|---|---|
| `<C-n>` / `<C-p>` | Navegar nos resultados (ou setas) |
| `<C-q>` | Enviar resultados para a quickfix list |
| `<Tab>` | Multi-select (marcar múltiplos itens) |
| `<C-x>` | Abrir em split horizontal |
| `<C-v>` | Abrir em split vertical |
| `<C-t>` | Abrir em nova tab |
| `<Esc>` ou `<C-c>` | Fechar o prompt |

> [!tip] `<leader>sk` (search keymaps) é o atalho para descoberta. Se você esqueceu um keymap, Telescope busca por ele. É mais rápido que consultar documentação.

### neo-tree (file explorer)

[[Dicionário do Terminal#neo-tree|neo-tree]] é o explorador de arquivos lateral do LazyVim.

**Abrir e fechar:**

| Key | Ação |
|---|---|
| `<leader>e` | Toggle neo-tree no escopo do git root (diretório raiz do repo) |
| `<leader>fe` | Toggle neo-tree no escopo do cwd atual |
| `<leader>E` | Toggle neo-tree com foco no arquivo atual |

**Dentro do neo-tree:**

| Key | Ação |
|---|---|
| `a` | Add — criar arquivo ou diretório (termina com `/` para dir) |
| `d` | Delete — apagar o item selecionado |
| `r` | Rename |
| `c` | Copy (marcar para copiar) |
| `x` | Cut (marcar para mover) |
| `p` | Paste (no diretório selecionado) |
| `Y` | Copy path absoluto para o clipboard |
| `<CR>` | Abrir arquivo / expandir diretório |
| `P` | Preview (abre mas mantém foco no neo-tree) |
| `q` | Fechar neo-tree |
| `?` | Help do neo-tree (lista todos os keymaps) |
| `H` | Toggle hidden files |
| `R` | Refresh |

> [!note] neo-tree não é o único jeito de navegar. Para maioria dos casos, `<leader>ff` no Telescope é mais rápido. neo-tree brilha quando você precisa visualizar a estrutura ou fazer operações em arquivos (rename, criar pastas).

### which-key (descoberta de keymaps)

[[Dicionário do Terminal#which-key|which-key]] resolve o problema clássico do Vim: memorização excessiva.

**Como usar:** pressione `<leader>` (ou qualquer key prefix como `g`, `z`, `]`) e **espere ~1 segundo**. Um popup aparece mostrando todos os keymaps disponíveis para aquele prefix, agrupados por categoria:

```
<leader>
  f  → find/files
  g  → git
  c  → code
  s  → search
  b  → buffer
  w  → windows
  u  → ui
  x  → diagnostics/quickfix
  ...
```

Cada grupo tem um label descritivo. Você não precisa memorizar todos os keymaps de saída — which-key os descobre pra você.

**Dica de ouro:** o mesmo popup funciona para prefixos de operadores. Pressione `d` no modo normal e espere — which-key mostra o que pode vir depois (motions). Pressione `y` e veja as opções.

**`<leader>sk`** (search keymaps via Telescope) é o complemento: busca por texto nos keymaps. Ex: `<leader>sk` → digitar "buffer" → encontra todos os keymaps relacionados a buffer.

### Statusline (lualine) e bufferline

**Statusline (barra de status na base):**

A lualine.nvim mostra, da esquerda para a direita:
- Modo atual (NORMAL, INSERT, VISUAL…) com cor correspondente
- Branch do git atual
- Diagnósticos LSP: contagem de erros (E), warnings (W), hints (H)
- Caminho do arquivo + flag de modificado (`[+]`)
- Posição do cursor (linha:coluna)
- Porcentagem no arquivo

**Bufferline (lista de buffers no topo):**

Buffers abertos aparecem como "tabs" na parte superior. Útil para visualizar o que está aberto sem usar `:ls`.

| Key | Ação |
|---|---|
| `<S-h>` | Mover para o buffer anterior (shift+h) |
| `<S-l>` | Mover para o buffer seguinte (shift+l) |
| `<leader>bd` | Fechar o buffer atual (sem fechar a window) |
| `<leader>bD` | Fechar buffer + window |
| `<leader>bo` | Fechar todos os outros buffers |
| `<leader>bp` | Pin/unpin buffer |

> [!tip] `<leader>bd` (buffer delete) é diferente de `:q`. `:q` fecha a window; `<leader>bd` fecha o buffer sem fechar a layout. Use `<leader>bd` para fechar arquivos sem desmanchar sua divisão de telas.

### LSP keys default (usar, não configurar)

O [[Dicionário do Terminal#LSP|LSP]] no LazyVim funciona de saída para as linguagens instaladas via Mason. Os keymaps abaixo estão disponíveis em qualquer arquivo com LSP ativo:

| Key | Ação |
|---|---|
| `gd` | Go to definition |
| `gD` | Go to declaration |
| `gr` | References (lista em Telescope) |
| `gI` | Go to implementations |
| `gy` | Go to type definition |
| `K` | Hover — doc inline do símbolo sob o cursor |
| `<leader>ca` | [[Dicionário do Terminal#Code action|Code action]] — ações contextuais do LSP |
| `<leader>cr` | Rename symbol (renomeia em todo o projeto) |
| `<leader>cf` | Format o arquivo atual |
| `<leader>cA` | Source actions |
| `]d` | Próximo diagnostic |
| `[d` | Diagnostic anterior |
| `]e` | Próximo error |
| `[e` | Error anterior |
| `<leader>cd` | Line diagnostics (popup com diagnóstico da linha atual) |
| `<leader>cl` | LSP info (mostra servers ativos para o buffer) |

> [!warning] LSP keys são ativas **apenas quando há um language server rodando** para o arquivo. Em arquivos de log, texto puro ou linguagens sem server instalado, `gd` cai de volta para o comportamento nativo do Vim (jump para declaração local). Cheque `<leader>cl` para saber se o LSP está ativo.

Para instalar servers adicionais: `:Mason` abre a interface, `i` instala o server selecionado. Para saber o que está disponível para sua linguagem, [[09 - LSP no Neovim]] cobre isso em detalhe.

### nvim-cmp (auto-complete)

O popup de completion aparece **automaticamente** em insert mode quando há suggestions disponíveis — LSP, buffer, path, snippets. Não há tecla para abrir manualmente (mas `<C-Space>` força o popup se não aparecer).

| Key | Ação |
|---|---|
| `<C-n>` | Próxima suggestion |
| `<C-p>` | Suggestion anterior |
| `<CR>` | Aceitar suggestion selecionada |
| `<Tab>` | Aceitar / avançar no snippet |
| `<S-Tab>` | Voltar no snippet |
| `<C-e>` | Cancelar e fechar popup |
| `<C-Space>` | Forçar abertura do popup |
| `<C-b>` / `<C-f>` | Scroll na doc preview (quando visível) |

O popup inclui um preview lateral com a documentação do item. Útil para ver a assinatura de funções antes de aceitar.

### Comment.nvim

Toggle de comentários baseado na linguagem do arquivo (usa `commentstring` ou Treesitter para detectar o tipo de comentário correto).

| Key | Ação |
|---|---|
| `gcc` | Comenta/descomenta a linha atual (modo normal) |
| `gbc` | Comenta/descomenta com block comment |
| `gc<motion>` | Comenta a região coberta pelo motion |
| `gcap` | Comenta o parágrafo inteiro |
| `gc` | (modo visual) Comenta a seleção |
| `gb` | (modo visual) Block comment na seleção |

```
# Exemplo: comentar 3 linhas
3gcc

# Equivalente com motion:
gc2j     (gc + mover 2 linhas pra baixo = comenta 3 linhas)
```

### nvim-surround

Add, change e delete de delimitadores (aspas, parênteses, tags, etc.) ao redor de text objects.

| Key | Ação |
|---|---|
| `ys<motion><char>` | Add surround — envolve o alvo no delimitador |
| `yss<char>` | Add surround na linha inteira |
| `cs<old><new>` | Change surround — troca o delimitador |
| `ds<char>` | Delete surround — remove o delimitador |
| `S<char>` | (visual) Add surround na seleção |

**Exemplos concretos:**

```
# Palavra: hello
ysiw"   →   "hello"      (yank-surround inner-word com aspas)
cs"'    →   'hello'      (change surround de " para ')
ds'     →   hello        (delete surround ')

# Função: foo(bar)
csb[    →   foo[bar]     (b = parêntese; [ = colchete)
dst     →   (remove tags HTML ao redor)

# Visual: selecionar texto → S"
→ envolve a seleção em aspas duplas
```

Pares especiais: `(` e `)` são equivalentes (`b`); `{` e `}` são equivalentes (`B`); `[` e `]` são equivalentes; `t` = tag HTML.

### Format on save

LazyVim habilita [[Dicionário do Terminal#Format on save|format on save]] por default via conform.nvim. Ao pressionar `:w`, o formatter roda automaticamente antes de salvar.

O formatter usado depende da linguagem (configurado no LazyVim por convenção de comunidade — Prettier para JS/TS/JSON/CSS, stylua para Lua, black para Python, etc.).

**Toggle por buffer:**

| Key | Ação |
|---|---|
| `<leader>uf` | Toggle format on save (buffer local) |
| `<leader>uF` | Toggle format on save (global) |

Se format on save estiver causando problemas em um arquivo específico, `<leader>uf` desabilita só para aquele buffer na sessão atual.

Para salvar sem formatar em um caso pontual:
```vim
:noautocmd w
```

### `:Lazy` (interface do plugin manager)

`:Lazy` abre a interface visual do lazy.nvim para gerenciar plugins.

| Key (dentro do :Lazy) | Ação |
|---|---|
| `S` | Sync — install + update + clean em um comando |
| `U` | Update — atualiza plugins desatualizados |
| `I` | Install — instala plugins novos declarados |
| `C` | Clean — remove plugins não mais declarados |
| `R` | Restore — reverte ao lockfile (`lazy-lock.json`) |
| `P` | Profile — mostra tempo de load por plugin |
| `D` | Debug |
| `L` | Log — histórico de operações |
| `?` | Help (lista todos os keymaps do :Lazy) |
| `q` | Fechar |

> [!tip] Após instalar ou atualizar, sempre feche e reabra o Neovim (ou `:Lazy reload`) para garantir que as mudanças estejam ativas. O `lazy-lock.json` no seu config é o snapshot de versões — commite-o para manter reprodutibilidade.

### Extras do LazyVim

LazyVim tem um sistema de **extras** — coleções de plugins opcionais que você pode habilitar por linguagem ou ferramenta. Para ver e ativar: `:LazyExtras`.

Exemplos de extras populares: `lang.typescript`, `lang.python`, `lang.go`, `editor.telescope`, `ui.mini-animate`. Ativar extras é o caminho certo antes de tentar configurar plugins do zero — provavelmente já existe um extra para o que você quer.

Isso é território do Adepto — [[08 - Customizando LazyVim]] explica o mecanismo.

### git (gitsigns.nvim)

Gitsigns adiciona indicadores de diff no gutter (a coluna à esquerda dos números de linha) e keymaps para navegar em hunks.

| Key | Ação |
|---|---|
| `]h` | Próximo hunk |
| `[h` | Hunk anterior |
| `<leader>ghs` | Stage hunk |
| `<leader>ghr` | Reset hunk |
| `<leader>ghS` | Stage buffer inteiro |
| `<leader>ghR` | Reset buffer inteiro |
| `<leader>ghp` | Preview hunk (diff inline) |
| `<leader>ghb` | Blame line (quem editou essa linha) |
| `<leader>ghd` | Diff against HEAD |
| `<leader>ghD` | Diff against último commit |

### Terminal integrado (toggleterm)

| Key | Ação |
|---|---|
| `<leader>ft` | Float terminal |
| `<leader>fT` | Float terminal (root dir) |
| `<C-/>` | Toggle terminal flutuante |
| `<C-\><C-n>` | Sair do terminal mode para normal mode |

### UI toggles

LazyVim agrupa vários toggles de UI sob `<leader>u`. Útil quando você precisa ajustar o ambiente sem mexer em config:

| Key | Ação |
|---|---|
| `<leader>uf` | Toggle format on save (buffer) |
| `<leader>uF` | Toggle format on save (global) |
| `<leader>us` | Toggle spell check |
| `<leader>uw` | Toggle word wrap |
| `<leader>ul` | Toggle line numbers |
| `<leader>ud` | Toggle diagnostics |
| `<leader>uc` | Toggle conceal |
| `<leader>uT` | Toggle Treesitter highlight |
| `<leader>ub` | Toggle background (dark/light) |
| `<leader>uh` | Toggle inlay hints |

### Workflow típico: primeiro dia com LazyVim

Um roteiro prático para dev vindo de VS Code/IntelliJ:

```
1. Abrir projeto:
   nvim .          → abre o Neovim no diretório atual

2. Encontrar arquivo:
   <leader>ff      → Telescope find files; digitar nome parcial; <CR> abre

3. Navegar no código:
   gd              → go to definition (LSP)
   <C-o>           → voltar (jump list)
   gr              → references em Telescope

4. Editar:
   ci"  /  cw  /  A    → text objects e motions das notas anteriores
   gcc                  → toggle comentário
   <leader>ca           → code action (import, fix, refactor)

5. Salvar e fechar:
   :w              → salva (formata automaticamente)
   <leader>bd      → fecha o buffer

6. Quando estiver perdido:
   <leader>         → espera 1s → which-key popup
   <leader>sk       → search keymaps no Telescope
   <leader>cl       → verifica LSP ativo
```

Este fluxo usa apenas o que existe por default. Nenhuma configuração extra necessária.

## Armadilhas

### 1. Format on save reescreve edits inesperadamente

**Cenário:** você salva um arquivo JSON com comentários `//`. O formatter remove os comentários porque JSON estrito não aceita. Você perde as anotações.

**Ou:** você edita código propositalmente "quebrado" para testar algo; ao salvar, o formatter reorganiza a indentação e você perde a referência visual.

**Solução imediata:** `<leader>uf` toggle desabilita format on save para o buffer atual. Para salvar sem formatar uma vez: `:noautocmd w`.

**Solução permanente por filetype:** isso é configuração — [[08 - Customizando LazyVim]].

### 2. `<leader>` é `<Space>` — e isso quebra o músculo velho

**Cenário:** você vem de anos de Vim com `<leader>` mapeado para `,` ou `\`. Toda vez que tenta acionar um keymap do LazyVim, pressiona `,` e nada acontece (ou acontece algo errado).

**Diagnóstico:** `:echo mapleader` confirma que é `" "` (espaço).

**Solução:** treino muscular. Não mude o leader no início — é o padrão de toda a comunidade LazyVim e muitos plugins assumem `<Space>`. Se quiser mudar, [[08 - Customizando LazyVim]].

### 3. Telescope `<leader>ff` em projeto sem `.git`

**Cenário:** você abre o Neovim em um diretório que não é um repo git. `<leader>ff` busca a partir do `cwd`, mas mostra resultados estranhos ou lentos porque não há filtro de `.gitignore` ativo.

**Causa:** LazyVim usa `git_files` (que respeita gitignore) quando detecta repo, e `find_files` (menos eficiente) fora de repo.

**Solução:** `cd` para o root correto antes de abrir o Neovim, ou use `<leader>fF` (find all files sem filtro de ignore — explícito). Em projetos grandes sem git, considere adicionar um `.gitignore` ou configurar Telescope — [[08 - Customizando LazyVim]].

### 4. `gd` LSP vs `gd` nativo do Vim

**Cenário:** você pressiona `gd` esperando LSP go-to-definition, mas o comportamento parece diferente do que você esperava. Em um arquivo Python sem servidor Mason instalado, `gd` age como o comando nativo do Vim (vai para a declaração local no arquivo, sem entender o projeto).

**Causa:** LazyVim sobrescreve `gd` com LSP go-to-definition **apenas quando há server ativo**. Sem server, o keymap cai de volta para o `gd` nativo.

**Diagnóstico:** `<leader>cl` mostra os servers LSP ativos para o buffer atual. Se a lista estiver vazia, instale o server via `:Mason`.

### 5. nvim-cmp aceita suggestion com `<CR>` ao confirmar código

**Cenário:** você está escrevendo, o popup de completion aparece, e ao pressionar `<Enter>` para ir pra próxima linha, acaba aceitando a suggestion em vez de apenas pular de linha.

**Causa:** por padrão no LazyVim, `<CR>` aceita a suggestion selecionada (com highlight) no popup do nvim-cmp.

**Solução imediata:** pressione `<C-e>` para fechar o popup primeiro, depois `<Enter>`. Ou use `<C-n>/<C-p>` para navegar sem selecionar, deixando o popup sem item selecionado — aí `<CR>` só pula linha. Configurar esse comportamento: [[08 - Customizando LazyVim]].

### 6. gitsigns não aparece em arquivo novo não commitado

**Cenário:** você cria um arquivo novo (`a` no neo-tree ou `:e novo-arquivo.lua`), começa a escrever, e o gutter não mostra nenhum indicador de diff.

**Causa:** gitsigns mostra diff contra o HEAD. Arquivos não rastreados pelo git (`git status` mostra como "untracked") não têm diff contra HEAD — ainda não foram adicionados.

**Solução:** `git add <arquivo>` no terminal, ou use `<leader>ghs` para stage hunk após o arquivo ter sido adicionado. O indicador `+` (novo conteúdo) aparece após o `git add`.

## Em inglês

- **distribuição** → *distribution*. "LazyVim is a Neovim **distribution** — an opinionated preset of plugins, options, and keymaps that works out of the box."
- **atalho de teclado** → *keymap* / *keybinding*. "LazyVim ships with sensible default **keymaps** for every major operation; learn them before overriding."
- **descobertabilidade** → *discoverability*. "which-key improves **discoverability** by showing available keymaps after you press a prefix key."
- **formatação ao salvar** → *format on save*. "**Format on save** runs the configured formatter automatically every time you write the buffer with `:w`."
- **ação de código** → *code action*. "Press `<leader>ca` to open the **code action** menu — import missing symbol, extract function, fix lint warning."
- **saltar para definição** → *go to definition*. "Use `gd` to **go to the definition** of the symbol under the cursor; `<C-o>` jumps back."
- **referências** → *references*. "**References** (`gr`) opens a Telescope picker listing every location in the codebase that uses the symbol."
- **popup de completion** → *completion popup*. "The **completion popup** appears automatically in insert mode when the LSP or buffer source has suggestions."
- **explorador de arquivos** → *file explorer*. "neo-tree is LazyVim's default **file explorer** — toggle it with `<leader>e` to browse the project tree."
- **buscador difuso** → *fuzzy finder*. "Telescope is the **fuzzy finder** — it lets you search files, grep text, browse help, and list keymaps with instant filtering."

## Veja também

- [[01 - Modal editing]]
- [[02 - Motions, operadores e text objects]]
- [[03 - Edição e navegação]]
- [[06 - Estrutura de config]] — onde fica cada arquivo de configuração do LazyVim
- [[08 - Customizando LazyVim]] — como sobrescrever defaults e adicionar plugins
- [[09 - LSP no Neovim]] — LSP em detalhe: servers, mason, diagnósticos
- [[03-Dominios/Terminal/Editor/index|MOC do galho]]
- Verbetes: [[Dicionário do Terminal#Distribuição|distribuição]], [[Dicionário do Terminal#LazyVim|LazyVim]], [[Dicionário do Terminal#Telescope|Telescope]], [[Dicionário do Terminal#neo-tree|neo-tree]], [[Dicionário do Terminal#which-key|which-key]], [[Dicionário do Terminal#LSP|LSP]], [[Dicionário do Terminal#Code action|code action]], [[Dicionário do Terminal#Format on save|format on save]]

## Referências

- [LazyVim — site oficial](https://www.lazyvim.org/)
- [LazyVim keymaps](https://www.lazyvim.org/keymaps)
- [LazyVim starter (template de config)](https://github.com/LazyVim/starter)
- [LazyVim repositório principal](https://github.com/LazyVim/LazyVim)
- [LazyVim discussions (comunidade)](https://github.com/LazyVim/LazyVim/discussions)
- [TJ DeVries — @teej_dv (Neovim from scratch)](https://www.youtube.com/@teej_dv)
