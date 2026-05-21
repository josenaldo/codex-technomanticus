---
title: "Edição e navegação"
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
  - ex-commands
  - navigation
  - search
aliases:
  - Edição e navegação
  - Ex commands
---

# Edição e navegação

> [!abstract] TL;DR
> Depois de motions/operadores, o que falta para o uso diário é o resto da interface: Ex commands (`:w`, `:e`), busca (`/`, `:s`), undo/redo, e o modelo buffer/window/tab. Saber esses ~30 comandos cobre 90% do dia. A maioria dos usuários de IDE abre o Neovim, aprende os modos e fica travado exatamente aqui — não porque seja difícil, mas porque o modelo mental é diferente do esperado.

## O que é / Como funciona

### Ex commands — o modo command-line

O modo command-line é ativado com `:` a partir do modo normal. Ele expõe a camada de comandos de texto do Vim — herdada do editor `ex` dos anos 70 — que controla arquivos, buffers, substituições e shell.

Comandos Ex persistem em histórico: pressione `:` e use `<Up>`/`<Down>` para navegar por comandos anteriores, ou `:<C-p>`/`:<C-n>`. Em LazyVim, o histórico também é acessível via `<leader>:` (Telescope command history).

**Operações de arquivo:**

```
:w                → write (salva o buffer atual no disco)
:w <path>         → salva em outro arquivo (não altera o buffer atual)
:e <path>         → edit (abre arquivo — tab completa o path)
:e!               → recarrega o arquivo do disco, descartando mudanças locais
:q                → quit (fecha a window atual; reclama se houver mudanças não salvas)
:wq               → write + quit
:x                → equivalente a :wq, mas só escreve se houver mudanças
:q!               → quit forçado sem salvar
:qa               → quit all (fecha todas as windows)
:qa!              → quit all forçado
```

> [!tip] `:x` é preferível a `:wq` para quem usa sistemas de build sensíveis a timestamps: `:wq` sempre atualiza o mtime mesmo se nada mudou; `:x` só grava se o buffer foi modificado.

**Shell — executar comandos sem sair do editor:**

```
:!<cmd>           → executa o comando no shell e mostra a saída
:!git status      → exemplo: mostra o status do git
:!npm test        → roda os testes
:r !<cmd>         → read: insere a saída do comando no buffer, na posição do cursor
```

`:%!<cmd>` passa o conteúdo do buffer como stdin para o comando e substitui o buffer pela saída. Padrão usado para formatar JSON com `:% !jq '.'` ou ordenar linhas com `:%!sort`.

### Yank, delete e paste básico

O sistema de registers completo é coberto em [[10 - Registers, marks, macros]], mas o essencial para o dia a dia:

```
yy      → yank (copia) a linha inteira para o register padrão
dd      → delete (apaga e guarda no register) a linha inteira
p       → paste após o cursor (ou abaixo da linha, se o register contém linha inteira)
P       → paste antes do cursor (ou acima da linha)
```

> [!note] Em Vim, `dd` não é um simples "delete" — o conteúdo vai para o register `"` (unnamed) e pode ser colado com `p`. Se você quer apagar sem contaminar o register, use `"_dd` (register black hole `_`). Isso é coberto em [[10 - Registers, marks, macros]].

Duplicar uma linha rapidamente:

```
yy p    → copia a linha e cola abaixo
```

Mover uma linha:

```
dd p    → apaga a linha e cola abaixo do cursor atual
```

### Busca

**Busca básica no buffer:**

```
/<termo>          → busca forward (pressione <CR> para confirmar)
?<termo>          → busca backward
n                 → próxima ocorrência (na direção da busca)
N                 → ocorrência anterior (direção oposta)
*                 → busca a palavra sob o cursor (forward, word boundary automático)
#                 → busca a palavra sob o cursor (backward)
```

A busca usa expressões regulares por padrão. Caracteres especiais (`.`, `*`, `[`, `\`) têm significado especial. Para buscar literalmente, escape com `\` ou use `\V` (very nomagic mode):

```
/foo\.bar         → busca "foo.bar" literalmente (escapa o ponto)
/\Vfoo.bar        → modo very nomagic: tudo é literal exceto `\`
```

Após uma busca, o padrão fica ativo (highlighted). Para limpar o highlight:

```
:nohlsearch       → desativa o highlight até a próxima busca
<leader>ur        → atalho LazyVim para nohlsearch (mnemônico: undo highlight)
```

**Busca e substituição (substitute):**

```
:s/x/y/           → substitui a primeira ocorrência de x por y na linha atual
:s/x/y/g          → substitui todas as ocorrências na linha atual
:%s/x/y/g         → substitui todas as ocorrências no arquivo inteiro
:%s/x/y/gc        → substitui com confirmação interativa por ocorrência (y/n/a/q)
```

Flags úteis:

```
/g    → global (todas as ocorrências, não só a primeira)
/c    → confirm (pede confirmação ocorrência por ocorrência)
/i    → case insensitive
/I    → case sensitive (anula o smartcase global)
/e    → ignora erro se não encontrar o padrão (não interrompe scripts)
```

**Word boundary — evitar substituições parciais:**

```
:%s/\<log\>/error/g     → substitui apenas "log" como palavra completa
```

`\<` e `\>` são os delimitadores de início e fim de palavra em Vim regex. Sem eles, `:%s/log/error/g` afeta `login`, `analog`, `catalog`, etc.

**Reuso do padrão de busca:**

```
/foo <CR>         → busca "foo"
:%s//bar/g        → pattern vazio reutiliza a última busca ("/foo")
```

Esse padrão (buscar primeiro com `/`, inspecionar as ocorrências, depois substituir com pattern vazio) é mais seguro que `:s` direto: você vê o que vai ser afetado antes de confirmar.

### Undo e redo

```
u         → undo (desfaz a última mudança)
<C-r>     → redo (refaz a última mudança desfeita)
```

O sistema de undo do Vim não é linear — é uma **árvore**. Se você desfaz 3 mudanças e depois faz uma edição nova, cria um ramo alternativo. O ramo anterior não é perdido — apenas fica inacessível via `u`/`<C-r>` direto.

**Undo persistente entre sessões:**

O LazyVim habilita `undofile` por padrão. O histórico de undo é salvo em `~/.local/state/nvim/undo/` e persiste entre sessões. Fechar e reabrir o arquivo não limpa o histórico.

**Time-based undo:**

```
:earlier 5m      → volta o estado do buffer para como estava 5 minutos atrás
:later 5m        → avança 5 minutos no tempo de edição
:earlier 10s     → volta 10 segundos
:earlier 3f      → volta 3 file writes (saves)
```

Time-based undo é útil quando você editou demais em uma direção errada e quer voltar a um ponto no tempo, não a uma operação específica.

**Plugin undotree:**

O LazyVim disponibiliza `undotree.nvim` como Extra opcional (não habilitado por padrão). Quando instalado, exibe a árvore de undo visualmente em um painel lateral, permitindo navegar para qualquer ramo com clareza. Veja [[Dicionário do Terminal#Undotree|undotree]].

### O modelo buffer/window/tab

Quem vem de VS Code ou IntelliJ assume que o modelo é: arquivo aberto = aba visível. No Neovim, os três conceitos são separados:

**[[Dicionário do Terminal#Buffer|Buffer]]:**
- Representação em memória de um arquivo (ou conteúdo sem arquivo — scratch buffer).
- Pode existir sem estar visível em nenhuma window.
- N buffers podem estar abertos simultaneamente; `:ls` lista todos.
- Um buffer pode aparecer em múltiplas windows ao mesmo tempo (dois splits mostrando o mesmo arquivo).

**Window:**
- Um viewport (split) que exibe um buffer.
- Múltiplas windows podem mostrar buffers diferentes — ou o mesmo buffer em posições diferentes.
- Fechar uma window não fecha o buffer. O buffer continua em memória.

**Tab:**
- Um layout de windows (conjunto de splits), não uma "aba de arquivo".
- Usar tabs do Neovim como se fossem tabs de browser é um erro comum de quem migra de IDE.
- O caso de uso correto: tab 1 = código, tab 2 = terminal, tab 3 = config.

```
:ls           → lista todos os buffers abertos
:ls!          → inclui buffers "unlisted" (help, terminal, etc.)
```

Indicadores do `:ls`:
- `%` = buffer atual
- `#` = buffer alternativo (`:e #` troca para ele, ou `<C-^>`)
- `a` = ativo (carregado e listado)
- `+` = modificado (não salvo)
- `-` = não listado

### Navegação entre splits (windows)

**Criar splits:**

```
:split              → divide horizontalmente (mesmo buffer)
:vsplit             → divide verticalmente (mesmo buffer)
:split <path>       → divide e abre outro arquivo
:vsplit <path>      → divide verticalmente e abre outro arquivo
```

Em LazyVim, os atalhos `<leader>-` (split horizontal) e `<leader>|` (split vertical) são equivalentes.

**Navegar entre splits:**

```
<C-w>h    → move o foco para o split à esquerda
<C-w>j    → move o foco para o split abaixo
<C-w>k    → move o foco para o split acima
<C-w>l    → move o foco para o split à direita
<C-w>w    → alterna para a próxima window (rotação)
<C-w>p    → volta para a window anterior (previous)
```

LazyVim adiciona `<C-h>`, `<C-j>`, `<C-k>`, `<C-l>` como atalhos diretos para navegar entre windows — sem o `<C-w>` intermediário. Isso também funciona entre splits do Neovim e painéis do tmux/zellij (via o plugin `vim-tmux-navigator` incluído no LazyVim).

**Gerenciar tamanho e layout:**

```
<C-w>=    → iguala o tamanho de todas as windows
<C-w>q    → fecha a window atual (buffer permanece em memória)
<C-w>o    → only — fecha todas as windows exceto a atual
<C-w>r    → rotate — rotaciona as windows no layout atual
```

Redimensionar com contagem:

```
<C-w>5>   → aumenta 5 colunas (split vertical)
<C-w>5<   → reduz 5 colunas
<C-w>5+   → aumenta 5 linhas (split horizontal)
<C-w>5-   → reduz 5 linhas
```

### Navegação entre buffers

```
:bnext      → vai para o próximo buffer
:bprev      → vai para o buffer anterior
:b <nome>   → vai para o buffer pelo nome (aceita partial match + Tab completion)
:b#         → vai para o buffer alternativo (equivalente a <C-^>)
:bd         → buffer delete (fecha o buffer, remove da lista)
<C-^>       → alterna entre o buffer atual e o alternativo (#)
```

Em LazyVim, os atalhos de buffer padrão são:

```
<S-h>       → buffer anterior (shift+h)
<S-l>       → próximo buffer (shift+l)
<leader>bd  → fecha o buffer atual
<leader>bD  → fecha o buffer e o split
```

A barra de buffers (bufferline) no topo mostra os buffers abertos com indicadores de modificação. Clicar funciona no modo GUI; no terminal, use os atalhos de teclado.

### Jump list

O Neovim mantém uma [[Dicionário do Terminal#Jump list|jump list]] para cada window — uma pilha de posições para navegação não-linear.

Comandos que **empurram** a posição atual na jump list antes de mover:
- Buscas: `/`, `?`, `*`, `#`
- Saltos estruturais: `%`, `{`, `}`, `G`, `gg`
- Comandos de go-to: `gd`, `gD`, `gf`, `gi`
- `:` seguido de número de linha (`:42<CR>`)

Navegar na jump list:

```
<C-o>       → jump back (volta para a posição anterior na lista)
<C-i>       → jump forward (avança na lista)
:jumps      → exibe toda a jump list
```

A jump list é persistente entre sessões quando `shada` está habilitado (padrão no LazyVim).

### Help integrado

```
:help <tópico>        → abre o manual em um split
:help motion.txt      → manual de motions
:help :s              → documentação do comando :s (substitute)
:help cmdline         → documentação do modo command-line
:help <C-w>           → documentação dos atalhos de window
:help pattern.txt     → documentação de expressões regulares
```

O help do Neovim usa wikilinks internos: posicione o cursor em um termo entre `|barras|` e pressione `<C-]>` para saltar para ele. `<C-o>` volta.

Em LazyVim, `<leader>fh` abre o Telescope sobre todos os tópicos de help — busca fuzzy com preview em tempo real. Muito mais ergonômico que digitar `:help` e tentar lembrar o nome exato do tópico.

## Na prática

### Sessão típica abrindo um projeto

```
nvim .                    → abre o file explorer (neo-tree) no diretório atual
j/k                       → navega no tree
<CR> ou o                 → abre o arquivo selecionado
<C-l>                     → foco para o buffer de edição (sai do neo-tree)
:vsplit outro.ts          → abre um segundo arquivo lado a lado
<C-h> / <C-l>            → alterna entre os dois splits
:w                        → salva
<leader>bd                → fecha o buffer atual quando terminar
```

### Refactor manual com busca + substitute

Cenário: renomear a função `fetchUser` para `getUser` em um arquivo, com confirmação ocorrência por ocorrência.

```
/fetchUser <CR>       → busca a primeira ocorrência (e destaca todas)
n                     → navega até a primeira ocorrência relevante
:%s//getUser/gc       → substitui (pattern vazio = reutiliza /fetchUser), com confirmação
```

Na confirmação interativa (`c`), as opções são:
- `y` = sim (substitui esta ocorrência)
- `n` = não (pula esta ocorrência)
- `a` = all (substitui todas sem mais confirmação)
- `q` = quit (para sem substituir mais)
- `l` = last (substitui esta e para)

Alternativa com `cgn` + `.` (mais visual, coberto em [[02 - Motions, operadores e text objects]]):

```
*                     → busca fetchUser sob o cursor
cgn                   → change next match
getUser <Esc>         → digita o novo nome
n.                    → vai para a próxima ocorrência e repete
```

### Recovery temporal com :earlier

Cenário: você editou por 15 minutos na direção errada e quer voltar ao ponto de partida sem precisar desfazer manualmente centenas de operações.

```
:earlier 15m          → volta o buffer para o estado de 15 minutos atrás
```

Se foi longe demais:

```
:later 5m             → avança 5 minutos no tempo
```

Após `:earlier`/`:later`, o undo normal (`u`/`<C-r>`) continua funcionando — mas a partir do novo ponto no tempo.

### Explorar comandos desconhecidos via help

Cenário: você viu alguém usar `<Up>` no prompt `:` e quer entender o histórico completo.

```
:help cmdline-history     → abre o manual específico
```

Ou via Telescope:

```
<leader>fh                → abre fuzzy search no help
cmdline history <CR>      → encontra o tópico sem saber o nome exato
```

### Splits para comparar arquivos

```
:vsplit                   → divide verticalmente (mesmo arquivo nos dois lados)
:e outro.ts               → abre o segundo arquivo no split atual
<C-w>=                    → iguala o tamanho dos splits
:diffthis                 → ativa diff no split atual
```

Em seguida, no outro split:

```
<C-l>                     → vai para o outro split
:diffthis                 → ativa diff nesse também
```

`]c` e `[c` navegam entre hunks de diff. `:diffoff` desativa.

## Armadilhas

### 1. Confundir window com tab

Quem vem de VS Code ou IntelliJ espera que "tab = arquivo aberto". No Neovim:

- **Buffer** = arquivo aberto (equivalente à aba da IDE)
- **Window** = split/viewport
- **Tab** = layout de splits

Abrir um novo arquivo com `:tabedit` cria um layout de window separado — não uma "aba de arquivo" independente. O resultado é desorientação: você tem dois "contextos" com seus próprios splits, o que raramente é o que quem vem de IDE quer.

**Solução:** use buffers + uma janela de buffer list (`:ls`, `<S-h>`/`<S-l>`, ou `<leader>fb` no LazyVim) como substituto das abas de IDE. Tabs do Neovim são para organizar workflows distintos (ex: edição vs terminal vs config), não para alternar entre arquivos.

### 2. `:q` reclama "no write since last change"

Comportamento esperado: o Vim **não** descarta mudanças silenciosamente. Se você modifica um buffer e tenta fechar sem salvar, ele para e avisa.

```
E37: No write since last change (add ! to override)
```

Opções:
- `:w` — salvar e depois `:q`
- `:wq` — salvar e fechar em um comando
- `:q!` — fechar sem salvar (as mudanças são perdidas)

Forçar `:q!` por hábito para fechar janelas rapidamente é perigoso. O padrão mais seguro é `:bd` (buffer delete), que também reclama se houver mudanças.

### 3. Substitute sem word boundary altera ocorrências parciais

`:%s/log/error/g` substitui:
- `console.log` → `console.error` ✓ (intencional)
- `logger` → `errorer` ✗ (não intencional)
- `catalog` → `caterror` ✗ (não intencional)

**Solução:** use `\<` e `\>` para delimitar a palavra:

```
:%s/\<log\>/error/g     → afeta apenas a palavra inteira "log"
```

Ou use a flag `c` para confirmar cada ocorrência e inspecionar antes de aceitar:

```
:%s/log/error/gc        → você decide caso a caso
```

### 4. `<C-i>` colide com `<Tab>` em alguns terminais

No protocolo ANSI clássico, `<C-i>` e `<Tab>` são indistinguíveis — ambos enviam o mesmo byte (0x09). Dependendo do terminal e da versão do protocolo de teclado:

- **Kitty / WezTerm (Kitty keyboard protocol):** `<C-i>` e `<Tab>` são distinguíveis.
- **xterm / a maioria dos terminais ANSI clássicos:** não distinguíveis.
- **tmux / zellij sem configuração extra:** podem interceptar `<Tab>` antes do Neovim receber.

**Sintoma:** `<C-i>` (jump forward na jump list) não funciona, ou funciona como Tab (indentação).

**Diagnóstico:**

```
:verbose map <C-i>       → mostra o que está mapeado para <C-i>
:verbose map <Tab>       → compara
```

**Solução a curto prazo:** use `:jumps` para inspecionar a lista e navegue manualmente; ou mude para um terminal com suporte ao Kitty keyboard protocol. A integração com multiplexer é abordada no galho Multiplexer da trilha Terminal.

## Em inglês

Esta seção cobre o vocabulário técnico para uso em documentação, pair programming e entrevistas em inglês.

- **salvar** — *write / save*. "Remember to **write** the buffer with `:w` before switching; Vim will warn if you try to quit with unsaved changes."
- **buscar** — *search*. "**Search** forward with `/pattern` or backward with `?pattern`; use `n` and `N` to cycle through matches."
- **substituir** — *substitute / replace*. "Use `:%s/old/new/g` to **replace** all occurrences globally, or add the `c` flag to confirm each one interactively."
- **janela** — *window*. "Open a vertical **window** split with `:vsplit` and navigate between splits with `<C-w>h` / `<C-w>l`."
- **aba** — *tab*. "In Neovim, a **tab** is a layout of windows — not a file tab like in VS Code. Use buffers for file switching."
- **buffer** — *buffer* (maintained). "Every open file lives in a **buffer**; list them with `:ls` and switch with `:b <name>` or `<S-h>`/`<S-l>`."
- **lista de saltos** — *jump list*. "The **jump list** tracks non-trivial cursor movements; navigate it with `<C-o>` (back) and `<C-i>` (forward)."
- **desfazer** — *undo*. "Press `u` to **undo** the last change; Vim maintains a full branching undo tree, not a linear stack."
- **refazer** — *redo*. "Press `<C-r>` to **redo** after an undo; if you made a new edit after undoing, the previous branch is still accessible via the undo tree."
- **dividir (a janela)** — *split*. "**Split** the window horizontally with `:split` or vertically with `:vsplit` to view two files side by side."

## Veja também

- [[01 - Modal editing]]
- [[02 - Motions, operadores e text objects]]
- [[04 - LazyVim tour]] (Telescope expande tudo daqui: fuzzy search em buffers, help, comandos)
- [[10 - Registers, marks, macros]] (detalha o sistema de paste/yank com registers nomeados)
- [[11 - Workflow avançado]] (quickfix é o "super-search" — busca em múltiplos arquivos)
- [[03-Dominios/Terminal/Editor/index|MOC do galho]]
- [[Dicionário do Terminal#Buffer|buffer]]
- [[Dicionário do Terminal#Jump list|jump list]]
- [[Dicionário do Terminal#Undotree|undotree]]

## Referências

- [Neovim — change.txt](https://neovim.io/doc/user/change.html) (`:help change.txt`)
- [Neovim — pattern.txt](https://neovim.io/doc/user/pattern.html) (`:help pattern.txt`)
- [Neovim — windows.txt](https://neovim.io/doc/user/windows.html) (`:help windows.txt`)
- [Neovim — cmdline](https://neovim.io/doc/user/cmdline.html) (`:help cmdline`)
- [Vim Registers — brianstorti.com](https://www.brianstorti.com/vim-registers/)
- [Learn Vim — Buffers, Windows, Tabs](https://learnvim.irian.to/basics/buffers_windows_tabs)
