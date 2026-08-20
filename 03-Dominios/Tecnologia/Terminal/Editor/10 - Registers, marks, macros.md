---
title: "Registers, marks, macros"
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
  - registers
  - marks
  - macros
aliases:
  - Registers
  - Marks
  - Macros
---

# Registers, marks, macros

> [!abstract] TL;DR
> Vim tem dezenas de "clipboards" ([[Dicionário do Terminal#Register|registers]]), bookmarks dentro e entre arquivos ([[Dicionário do Terminal#Mark|marks]]), e gravação de keystrokes pra replay ([[Dicionário do Terminal#Macro|macros]]). Combinados, multiplicam edição. Saber os 5-10 essenciais já automatiza muito.

## O que é / Como funciona

### Registers — os múltiplos clipboards

O Vim não tem um clipboard — tem dezenas. Um **register** é um slot nomeado onde operadores de edição (`d`, `c`, `y`, `s`) escrevem e `p`/`P` lê. Selecionar explicitamente um register é feito com `"<reg>` antes do operador.

Listar todos os registers ativos: `:registers` (ou `:reg`). Em LazyVim, `<leader>sr` abre Telescope para inspecionar registers.

#### Named — `a` a `z` (e `A` a `Z`)

Os 26 registers nomeados (`a`-`z`) são explícitos e persistem até você sobrescrevê-los.

```
"ayy    → yank a linha atual pro register a
"ap     → cola o conteúdo do register a
"AY     → APPEND (uppercase) a linha atual no register a (acumula, não substitui)
"ayiw   → yank inner word pro register a
"adiw   → delete inner word e guarda no register a
```

A convenção uppercase (`A`-`Z`) é append: `"Ayy` acrescenta a linha atual ao que já está em `a`. Útil pra acumular trechos dispersos pra colar juntos depois.

#### Unnamed — `""`

O register padrão. Todo `y`, `d`, `c`, `s` que não especifica register explícito vai pra `""`. O comando `p` (ou `P`) cola desse register.

```
yy    → yank linha pro register "" (e pro "0, se for só yank)
dd    → delete linha pro register "" (e desloca "1-"9)
p     → cola o conteúdo do register ""
```

> [!note] `dd` sobrescreve `""` — armadilha clássica ao intercalar deletes e pastes. Se você yankou, depois apagou uma linha com `dd`, o `p` seguinte cola o que foi deletado, não o que foi yankado. Use `"0p` pra garantir o último yank.

#### Numbered — `"0` a `"9`

O Vim mantém um histórico automático:

- `"0` — sempre o último **yank** (`y`). Nunca é afetado por `d` ou `c`.
- `"1` — o delete/change mais recente que afetou uma linha inteira (ou mais de um caractere).
- `"2` a `"9` — histórico rotativo: cada novo delete empurra o anterior pra um número acima. `"9` é o mais antigo.

Isso cria um histórico de deletes/changes que você pode recuperar sem plugin de clipboard history.

```
"0p    → cola o último yank (independente de deletes intermediários)
"1p    → cola o último delete
"2p    → cola o penúltimo delete
```

#### Sistema — `"+` e `"*`

Esses dois registers integram com o clipboard do sistema operacional:

- `"+` — clipboard principal (Ctrl+C / Ctrl+V no OS). Disponível em todos os sistemas (Linux X11/Wayland, macOS, Windows).
- `"*` — X11 primary selection (Linux): texto selecionado com mouse, colado com botão do meio. Em macOS, `"*` é equivalente a `"+`.

```
"+yy     → copia linha pro clipboard do OS (colar no Slack, navegador, etc.)
"+p      → cola o clipboard do OS no Neovim
"+yiw    → copia word pro clipboard
"*y}     → copia parágrafo pro primary selection (Linux)
```

> [!tip] Se `"+` não funcionar, o Neovim pode não ter sido compilado com suporte a clipboard. `:checkhealth` vai indicar o problema. Solução: instalar `xclip`, `xsel` (Linux X11), `wl-clipboard` (Wayland), ou `pbcopy/pbpaste` (macOS). Em LazyVim, `vim.opt.clipboard = "unnamedplus"` faz o register padrão (`""`) virar `"+` — conveniente mas muda o comportamento de `d`/`c`.

#### Expression — `"=`

O register de expressão avalia Vimscript/Lua e insere o resultado.

```
(em insert mode) <C-r>=2+2<CR>    → insere 4
(em insert mode) <C-r>=strftime("%Y-%m-%d")<CR>    → insere data atual
"=2*21<CR>p    → (em normal mode) calcula e cola o resultado
```

Útil pra inserir valores calculados sem sair do insert mode.

#### Outros registers especiais

| Register | Conteúdo |
|---|---|
| `"/` | Última busca (`:put /` injeta no buffer) |
| `":` | Último comando Ex executado |
| `"_` | Black hole — descarta silenciosamente |
| `"%` | Nome do arquivo atual |
| `"#` | Nome do arquivo alternativo (último buffer) |

O **black hole** (`"_`) é especialmente útil:

```
"_dd    → delete linha SEM poluir o register unnamed ou numbered
"_d2j   → delete 3 linhas sem perder o yank atual
"_ciw   → change word sem afetar clipboard
```

---

### Marks — bookmarks de posição

Uma **mark** salva a posição do cursor (linha + coluna) em um buffer. Diferente de jumplist (automática), marks são criadas intencionalmente.

Criar: `m<letra>`. Saltar: `'<letra>` (início da linha) ou `` `<letra> `` (posição exata — linha + coluna).

#### Locais — `a` a `z`

Scope restrito ao buffer atual. Não persistem em outros arquivos.

```
ma       → cria mark a na posição atual
'a       → salta pra início da linha onde a mark a está
`a       → salta pra posição exata (linha e coluna) da mark a
d`a      → delete do cursor até a posição da mark a
y`a      → yank do cursor até a mark a
```

Usar marks com operadores é poderoso: `d`a` deleta do cursor até onde `a` está marcado, sem contar linhas nem estimar distâncias.

#### Globais — `A` a `Z`

Marks globais cruzam arquivos e persistem entre sessões (via `shada`). São a forma mais direta de "lembrar de voltar aqui" em projetos grandes.

```
mU       → cria mark global U em qualquer arquivo aberto
'U       → salta pro arquivo + linha onde U foi criada
`U       → salta pro arquivo + posição exata
```

Exemplo de uso: marcou `mU` em `src/api/users.ts` enquanto lia testes. Abre o arquivo de testes, edita. Quando terminar, `` `U `` volta exatamente ao ponto em `users.ts`.

#### Marks especiais automáticas

O Neovim mantém marks automáticas que você não precisa criar:

| Mark | Significado |
|---|---|
| `'.` | Última posição onde texto foi modificado |
| `''` | Posição antes do último salto grande (ex: `gg`, `G`, busca) |
| `'^` | Última posição onde o insert mode foi encerrado |
| `` `< `` / `` `> `` | Início / fim da última seleção visual |
| `'[` / `']` | Início / fim do último texto yanked ou colocado |

```
'.     → volta pra onde você editou por último
''     → volta pro ponto onde você estava antes de ir pro início/fim do arquivo
`<     → volta pro início da última seleção visual
gv     → reseleciona a última seleção visual (usa `< e `> internamente)
```

#### Gerenciamento de marks

```
:marks           → lista todas as marks ativas
:delmarks a      → remove mark a
:delmarks a-d    → remove marks a, b, c, d
:delmarks!       → remove todas as marks locais (não globais)
```

Em LazyVim com Telescope: `<leader>sm` (`search marks`) lista marks navegáveis.

---

### Macros — keystroke recording

Uma **macro** é uma sequência de keystrokes gravada e reproduzível. O Neovim grava tudo que você digita — inclusive movimentos, busca, substituição, insert mode — e reproduz exatamente.

#### Gravar e reproduzir

```
q<reg>    → começa a gravar no register <reg> (ex: qa)
(teclas)  → qualquer sequência de comandos
q         → para a gravação

@<reg>    → executa a macro do register <reg>
@@        → re-executa a última macro rodada
5@a       → executa a macro de a exatamente 5 vezes
100@a     → executa 100 vezes (para automaticamente se der erro)
```

> [!tip] A contagem `N@a` para automaticamente quando o macro encontra um erro (ex: tentou mover pra baixo na última linha). Use isso a favor: `100@a` numa lista de 20 itens aplica o macro em todas as 20 linhas e para no fim sem input adicional.

#### Macro é register

Macros são armazenadas em registers nomeados — literalmente o mesmo mecanismo. Isso tem implicações práticas:

```
:reg a      → mostra o conteúdo do macro gravado em a
"ap         → cola o macro no buffer como texto editável
(editar)    → corrige o keystroke errado
"ay$        → yank de volta pro register a
```

Editar o macro como texto evita ter que regravar do zero quando um único passo está errado.

#### Macros aninhados

Dentro de um macro você pode chamar outro:

```
qa
  (faz edições no arquivo A)
  @b          → chama o macro de b (que processa outra coisa)
q
```

Macros aninhados permitem compor comportamentos: um macro "outer" itera, um macro "inner" transforma.

#### Macros recursivos

Um macro pode se chamar — com cuidado:

```
qqq         → limpa o register q (grava macro vazio)
qq          → começa a gravar em q
  (edições)
  j         → move pra próxima linha
  @q        → chama a si mesmo (mas q estava vazio quando começou — é seguro)
q           → para a gravação
@q          → roda o macro recursivo (para quando j não puder mover)
```

Macros recursivos exigem que o register esteja vazio antes de gravar para evitar loop infinito imediato. O idioma `qqq` limpa o register antes de iniciar.

---

## Na prática

### Exemplo 1 — Preservar yank ao deletar

Fluxo clássico: yank um trecho pra substituir outro, mas precisa deletar a linha de destino antes.

```
yiw          → yank inner word (vai pro "" e pro "0)
"_dd         → deleta a linha de destino pro black hole (não polui "")
p            → cola o que foi yankado (ainda em "")
```

Sem `"_`, o `dd` sobrescreveria `""` e o `p` colaria o delete, não o yank. `"0p` resolve também, mas `"_dd` é mais limpo em fluxo.

### Exemplo 2 — Accumulate scattered snippets

Precisa juntar definições de tipos espalhadas em vários arquivos:

```
"ayiW        → yank a palavra atual pro register a
(navega pro próximo trecho)
"Ayiw        → APPEND no register a (sem sobrescrever)
(navega pro próximo)
"Ayap        → append o parágrafo no register a
(abre novo buffer)
"ap          → cola tudo acumulado de uma vez
```

A diferença entre `"a` (overwrite) e `"A` (append) é a letra maiúscula — detalhe que economiza muita navegação.

### Exemplo 3 — Marks pra refactor cross-file

Cenário: precisa adicionar um método em `src/utils.ts` e um teste correspondente em `tests/utils.test.ts`, alternando entre os dois arquivos com precisão.

```
(em src/utils.ts, no ponto de inserção do método)
mU                → mark global U

(abre tests/utils.test.ts)
mT                → mark global T pra referência futura

(faz edições no arquivo de teste)

`U                → salta de volta pro ponto exato em src/utils.ts
(edita o método)
`T                → salta de volta pro arquivo de teste
```

Marks globais eliminam a sequência `<leader>,` → buscar arquivo → scroll até linha.

### Exemplo 4 — Macro pra transformar lista

Buffer com uma lista de nomes no formato `firstName lastName` (um por linha). Precisa transformar pra `lastName, firstName`.

```
qa                    → grava em a
  ^                   → vai pro início da linha
  "ByiW               → yank primeiro nome pro register b (inner WORD)
  W                   → vai pro segundo nome
  "Byaw               → append o space+sobrenome em b... 
```

Abordagem mais direta com substituição neste caso:

```
:%s/^\(\w\+\) \(\w\+\)$/\2, \1/
```

Mas quando o padrão é irregular (linhas com formatos mistos), macro grava melhor:

```
qa
  ^
  yiW           → yank primeiro nome pro ""
  dW            → deleta primeiro nome + espaço
  A, <Esc>      → vai pro fim da linha, insere ", "
  p             → cola o primeiro nome no fim
  j             → vai pra próxima linha
q
@a              → executa uma vez pra testar
5@a             → aplica nas próximas 5 linhas
```

### Exemplo 5 — Incremento sequencial com `g<C-a>`

Criar lista numerada a partir de uma lista com valores todos `1`:

```
1. item A
1. item B
1. item C
1. item D
```

```
(seleciona as 4 linhas em visual-line com V)
g<C-a>
```

Resultado:
```
1. item A
2. item B
3. item C
4. item D
```

`g<C-a>` aplica incremento sequencial em cada linha selecionada. Sem macro, sem substituição complexa.

### Exemplo 6 — Editar macro gravado

Macro em `q` com erro num keystroke no meio da sequência:

```
:put q           → cola o conteúdo do macro no buffer atual como texto
(edita o texto — é a sequência de keys literais)
(seleciona visualmente a linha corrigida)
"qy$             → yank de volta pro register q (do início da linha até o fim)
:d               → deleta a linha do buffer (se quiser limpar)
@q               → testa a versão corrigida
```

Editar o macro como texto evita regravar do zero — valioso quando o macro tem 20+ steps.

---

## Armadilhas

> [!warning] Armadilha 1 — `dd` polui o unnamed register
> O `d` (delete) e `c` (change) escrevem em `""` e em `"1`-`"9`. Isso sobrescreve qualquer yank anterior em `""`. Se você yank pra colar várias vezes e intercala com `dd`, use `"0p` (sempre o último yank) ou `"_dd` (delete pro black hole). `"_d{motion}` é o padrão mais seguro quando precisar deletar sem alterar a área de transferência de trabalho.

> [!warning] Armadilha 2 — Macro captura estado do editor, não intenção
> Se durante a gravação você abrir Telescope (`<leader>ff`), o macro grava as teclas `<Space>ff` literalmente — e no replay, Telescope pode abrir em contexto diferente, navegar pra arquivo errado, ou falhar silenciosamente. Macros são mais confiáveis com operadores e motions puras (normal mode). Testar sempre com `@a` em uma linha antes de aplicar em escala.

> [!warning] Armadilha 3 — Marks globais apontam pra path obsoleto
> Marks globais (`A`-`Z`) persistem no `shada` associadas ao path absoluto do arquivo. Se o arquivo for movido ou renomeado fora do Neovim (ex: via terminal, git mv, refactor no IDE), a mark global aponta pra path que não existe mais — e o salto falha silenciosamente ou abre um buffer vazio. Limpar marks obsoletas: `:delmarks A` (individual) ou `:wshada!` + recriar as que importam.

> [!warning] Armadilha 4 — `<C-a>` incrementa o número errado
> `<C-a>` incrementa o **primeiro número** que encontra a partir da posição do cursor na linha. Com cursor antes de `foo123`, `<C-a>` pula até `123` e incrementa. Em visual + `g<C-a>`, incrementa sequencialmente cada linha selecionada — mas se a linha tem múltiplos números, incrementa o primeiro encontrado, que pode não ser o desejado. Conferir o padrão da linha antes de aplicar em escala.

> [!warning] Armadilha 5 — Register `""` vs `"0` é confusão frequente
> `""` contém o último yank **ou** o último delete/change — o que vier por último. `"0` contém sempre e apenas o último **yank** (`y`), nunca afetado por `d` ou `c`. Quando estiver em dúvida sobre o que `p` vai colar, `:reg` mostra o estado atual de todos os registers. Nas primeiras semanas com registers, consultar `:reg` antes de colar é boa prática.

> [!warning] Armadilha 6 — Macro recursivo sem limpeza prévia cria loop infinito
> Gravar um macro recursivo (`@q` dentro de `q`) sem limpar `q` antes (`qqq`) significa que o macro chama a versão anterior de si mesmo imediatamente, criando loop infinito ou comportamento imprevisível. Sempre limpar o register antes de gravar macro recursivo: `qqq` (grava macro vazio em `q`) → `qq` (começa a gravar a versão nova).

---

## Em inglês

| PT-BR | EN |
|---|---|
| registrador | register |
| marca | mark |
| gravar | record |
| reproduzir | replay / playback |
| aninhado | nested |
| buraco negro | black hole (termo técnico mantido) |
| acrescentar | append |
| sobrescrever | overwrite |
| numerado | numbered |
| nomeado | named |
| recursivo | recursive |
| seleção primária | primary selection (X11) |
| histórico de desfazimento | undo history |
| sessão | session |
| persistir | persist |

---

## Veja também

- [[02 - Motions, operadores e text objects]] — operadores (`d`, `c`, `y`) escrevem em registers; entender operadores é pré-requisito pra usar registers bem
- [[03 - Edição e navegação]] — yank, delete e paste base; jump list (diferente de marks)
- [[11 - Workflow avançado]] — quickfix list tem pattern register-like; macros + quickfix = refactor em escala
- [[12 - Treesitter avançado]] — text objects estruturais + macros = refactor baseado em AST
- [[03-Dominios/Tecnologia/Terminal/Editor/index|MOC do galho]]

### Verbetes relacionados

- [[Dicionário do Terminal#Register|Register]]
- [[Dicionário do Terminal#Mark|Mark]]
- [[Dicionário do Terminal#Macro|Macro]]
- [[Dicionário do Terminal#Operador|Operador]]
- [[Dicionário do Terminal#Motion|Motion]]
- [[Dicionário do Terminal#Text object|Text object]]

---

## Referências

- <https://neovim.io/doc/user/change.html#registers>
- <https://neovim.io/doc/user/motion.html#mark-motions>
- <https://neovim.io/doc/user/repeat.html#recording>
- <https://www.brianstorti.com/vim-registers/>
- <https://www.youtube.com/@ThePrimeagen>
- <https://pragprog.com/titles/dnvim2/practical-vim-second-edition/>
