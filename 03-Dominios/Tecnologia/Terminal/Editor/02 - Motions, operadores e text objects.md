---
title: "Motions, operadores e text objects"
created: 2026-05-19
updated: 2026-05-19
type: concept
progress: backlog
status: seedling
publish: true
fase: iniciado
tags:
  - terminal
  - editor
  - iniciado
  - motions
  - text-objects
  - operators
aliases:
  - Motions
  - Text objects
  - Operadores
---

# Motions, operadores e text objects

> [!abstract] TL;DR
> Edição em Vim é `<operador><motion ou text object>`. Aprender 10 operadores × 20 motions/text objects te dá centenas de combinações sem memorizar atalhos avulsos. O `.` repete a última edição — isso multiplica silenciosamente qualquer change.

## O que é / Como funciona

### A gramática verbo + substantivo

Vim trata edição como uma linguagem: **operadores** são verbos, **motions** e **text objects** são substantivos. Combinados, eles formam comandos expressivos:

| Verbo (operador) | Substantivo (motion/text object) | Comando | Significado |
|---|---|---|---|
| `d` — delete | `iw` — inner word | `diw` | apaga a palavra sob o cursor (sem espaços ao redor) |
| `c` — change | `ap` — around paragraph | `cap` | apaga o parágrafo e entra em insert |
| `y` — yank | `i"` — inside quotes | `yi"` | copia o conteúdo entre aspas duplas |
| `>` — indent | `ip` — inner paragraph | `>ip` | indenta o parágrafo atual |
| `gU` — uppercase | `iw` — inner word | `gUiw` | coloca a palavra em maiúsculas |

Essa gramática é composicional: aprender um novo operador multiplica todos os motions/text objects que você já conhece, e vice-versa.

### Operadores principais

```
d     → delete (apaga e guarda no register)
c     → change (apaga e entra em insert)
y     → yank (copia para o register)
v     → visual (seleciona para operação subsequente)
gu    → lowercase (converte para minúsculas)
gU    → uppercase (converte para maiúsculas)
>     → indent (aumenta indentação)
<     → dedent (reduz indentação)
=     → auto-indent (reformata indentação via formatador do buffer)
```

> [!note] Operadores que têm dois caracteres (`gu`, `gU`) funcionam da mesma forma: `gu` + motion/text object. Ex: `guiw` = lowercase da palavra.

Usar o mesmo operador duas vezes aplica-o à linha inteira: `dd` apaga a linha, `yy` copia a linha, `>>` indenta a linha, `cc` apaga a linha e entra em insert.

### Motions — movem o cursor

Motions movem o cursor de um ponto a outro. Quando usados após um operador, definem o intervalo de texto afetado (do ponto inicial até o ponto de destino).

**Por caractere:**

```
h / l    → esquerda / direita (1 caractere)
j / k    → abaixo / acima (1 linha)
```

**Por palavra:**

```
w    → início da próxima word (para em pontuação)
e    → fim da word atual ou próxima (para em pontuação)
b    → início da word anterior (para em pontuação)
W    → início da próxima WORD (só para em espaço)
E    → fim da WORD atual ou próxima (só para em espaço)
B    → início da WORD anterior (só para em espaço)
```

**Por linha:**

```
0    → início absoluto da linha (coluna 0)
^    → primeiro caractere não-branco da linha
$    → fim da linha
```

**Por arquivo:**

```
gg   → primeira linha do buffer
G    → última linha do buffer
```

**Busca no caractere da linha (find/till):**

```
f<x>    → avança até o próximo caractere x (cursor em cima de x)
t<x>    → avança até antes do próximo caractere x (cursor antes de x)
F<x>    → recua até o caractere x anterior
T<x>    → recua até depois do caractere x anterior
;       → repete o último f/t/F/T na mesma direção
,       → repete o último f/t/F/T na direção oposta
```

**Por parágrafo e delimitador:**

```
}    → próximo parágrafo (bloco separado por linha em branco)
{    → parágrafo anterior
%    → pula para o delimitador correspondente: ( ), [ ], { }, /* */
```

### Text objects — delimitam regiões

Text objects diferem de motions: não dependem da posição atual do cursor dentro do alvo para definir o intervalo — eles delimitam semanticamente. Usar `diw` com o cursor em qualquer caractere da palavra apaga a palavra inteira.

Prefixos obrigatórios:
- `i` = **inner** (só o conteúdo, sem delimitadores ou espaço ao redor)
- `a` = **around** (inclui delimitadores ou espaço adjacente)

**Palavra e parágrafo:**

```
iw / aw    → inner/around word
iW / aW    → inner/around WORD
ip / ap    → inner/around paragraph (bloco separado por linha em branco)
is / as    → inner/around sentence (frase terminada em . ? !)
```

**Pares de delimitadores:**

```
i" / a"    → dentro/em volta de aspas duplas
i' / a'    → dentro/em volta de aspas simples
i` / a`    → dentro/em volta de backtick
i( / a(    → dentro/em volta de parênteses  (também: ib / ab)
i[ / a[    → dentro/em volta de colchetes
i{ / a{    → dentro/em volta de chaves      (também: iB / aB)
i< / a<    → dentro/em volta de angle brackets
it / at    → dentro/em volta de tag HTML/XML (ex: <div>...</div>)
```

> [!tip] `ci"` é provavelmente o text object mais usado no dia a dia: **change inside quotes**. Cursor pode estar em qualquer ponto dentro das aspas ou no próprio delimitador — o text object encontra o par.

### Contagem (count)

Prefixar um número a um motion ou comando define a quantidade de repetições:

```
3w      → avança 3 words
5j      → desce 5 linhas
d3w     → deleta 3 words a partir do cursor
3dd     → deleta 3 linhas
2ci"    → (atípico) change inside quotes 2 vezes — não muito útil; prefira outras composições
```

A semântica exata: o número multiplica a motion/text object, não o operador. `d3w` = delete aplicado à motion `3w` (3 words). `3dw` e `d3w` têm o mesmo resultado prático para `dw`, mas a distinção importa em operadores que acumulam efeito por repetição.

### O dot command: `.`

`.` repete a última **change** (não uma motion). "Change" = qualquer operação que modificou o buffer: insert, delete, substitute, operator + motion.

```
ciw novo_nome <Esc>    → renomeia a palavra sob o cursor
.                      → repete: apaga a próxima palavra e insere "novo_nome"
```

Fluxo de produtividade clássico com `/` e `n`:

```
/pattern <CR>    → busca o padrão
cgn              → change next match (altera a próxima ocorrência e entra em insert)
novo <Esc>       → digita o substituto
n                → pula para a próxima ocorrência
.                → repete o change (apply "novo" ali também)
```

`cgn` é especialmente poderoso porque o `gn` como motion seleciona sempre o próximo match da busca ativa — tornando `.` exato para refactor manual controlado ocorrência por ocorrência.

## Na prática

### Tabela de exemplos copiáveis

| Comando | O que faz |
|---|---|
| `daw` | deleta a word sob o cursor **e** o espaço adjacente |
| `diw` | deleta a word sob o cursor (sem espaços ao redor) |
| `ci"` | apaga o conteúdo entre aspas duplas e entra em insert |
| `ca"` | apaga as aspas duplas e o conteúdo, entra em insert |
| `yi(` | copia o conteúdo entre parênteses para o register |
| `ya(` | copia parênteses + conteúdo para o register |
| `>ip` | indenta o parágrafo atual um nível |
| `=ip` | auto-indenta o parágrafo (usa o formatador do buffer) |
| `gUiw` | converte a palavra atual para MAIÚSCULAS |
| `guiw` | converte a palavra atual para minúsculas |
| `gU$` | converte do cursor até o fim da linha para maiúsculas |
| `dt,` | deleta do cursor até a próxima vírgula (não inclui `,`) |
| `df,` | deleta do cursor até a próxima vírgula (inclui `,`) |
| `ct)` | apaga do cursor até o `)` e entra em insert |
| `cit` | apaga o conteúdo de uma tag HTML e entra em insert |
| `vip` | seleciona o parágrafo em visual mode |
| `dap` | deleta o parágrafo inteiro (incluindo linha em branco adjacente) |
| `yG` | copia do cursor até o fim do arquivo |
| `d^` | deleta do cursor até o primeiro caractere não-branco da linha |

### Workflow real: renomear variável dentro de uma função

Cenário: você quer renomear `oldName` para `newName` em 3-5 ocorrências visíveis na tela (não global).

```
*              → busca a palavra sob o cursor (todas as ocorrências no buffer)
cgn            → change the next match (altera a primeira ocorrência, entra em insert)
newName <Esc>  → digita o novo nome, volta ao normal
.              → repete o change na próxima ocorrência
.              → repete novamente
```

Vantagem sobre `:%s`: você confirma cada ocorrência visualmente antes de aplicar. Use `n` para pular uma ocorrência sem aplicar e `.` para aplicar nas que quiser.

> [!note] `gd` (go to definition local) é abordado em [[04 - LazyVim tour]]. Para renomear via LSP (buffer inteiro + arquivos relacionados), use `<leader>cr` no LazyVim (rename do LSP) — mais poderoso, mas menos granular.

### Visual mode como operador implícito

Quando o alvo é incomum ou difícil de expressar como text object/motion, use visual mode para selecionar manualmente e depois aplique o operador:

```
v                  → entra em visual (char)
3w                 → seleciona 3 words
d                  → apaga a seleção
```

```
V                  → visual line
3j                 → seleciona 3 linhas abaixo
>                  → indenta as linhas selecionadas
```

```
<C-v>              → visual block
3j                 → 4 linhas em bloco
I// <Esc>          → insere "//" no início de cada linha (comentar bloco)
```

Visual mode não cancela as combinações com text objects — você pode fazer `v` seguido de `iw` para selecionar a word sem mover o cursor manualmente até ela.

### Diferença `w` vs `W` em código TypeScript

Dado: `foo.bar.baz` com o cursor em `f`:

```
w    → para em 'f' de 'foo', depois em '.' antes de 'bar', depois em 'b' de 'bar'…
W    → pula de 'foo.bar.baz' inteiro para o próximo token separado por espaço
```

Na prática: `dW` em `foo.bar.baz ` (com espaço depois) apaga `foo.bar.baz` de uma vez. `dw` apaga apenas `foo`.

Regra prática:
- Use `w`/`b`/`e` para navegar dentro de expressões (segmentado por pontuação).
- Use `W`/`B`/`E` para pular entre tokens inteiros separados por espaço (identifiers compostos, paths, URLs).

### Contagem para navegação rápida

```
5j        → desce 5 linhas (útil com número relativo de linha no LazyVim)
3w        → avança 3 words
d5j       → apaga da linha atual até 5 linhas abaixo (6 linhas total)
```

> [!tip] LazyVim habilita `relativenumber` por padrão. Com números relativos na gutter, você lê diretamente `3j` ou `3k` sem contar linhas manualmente.

## Armadilhas

### 1. Confundir `w` com `W`

Em código com pontuação (TypeScript, Rust, Python), `w` para em cada caractere de pontuação (`.`, `_`, `(`, `)`…). Se você usa `dw` esperando apagar `foo.bar`, vai apagar só `foo`.

**Diagnóstico:** cursor para mais cedo que o esperado; a operação afeta menos texto que você queria.

**Solução:** use `dW` quando o alvo termina no próximo espaço, ou use text objects (`diw`, `da(`) quando o alvo é delimitado semanticamente.

Exemplo:
```
cursor em 'f' de: const foo.bar.baz = 1
dw  → apaga 'foo', cursor vai para '.'
dW  → apaga 'foo.bar.baz', cursor vai para '='
```

### 2. Text object não-funcional fora da linha do delimitador

Text objects de par de caracteres como `i"`, `i'`, `i(` operam na **linha atual do cursor**. Se o cursor está em uma linha e as aspas estão em outra, o text object falha silenciosamente (tenta encontrar o par na linha errada) ou não faz nada.

**Cenário problemático:**

```text
const x = "hello   ← cursor aqui, quer apagar o conteúdo
world"              ← aspas fecham aqui
```

`ci"` com o cursor na linha de `const x` funciona se o par de aspas abre nessa linha. Se o cursor estiver em "world" e as aspas não fecharem nessa linha, pode não funcionar como esperado.

**Solução:** mova o cursor para dentro do par antes de aplicar o text object. Para strings multi-linha, use `vi"` em visual para verificar o que foi selecionado antes de aplicar o operador.

> [!note] Text objects de parágrafo (`ip`/`ap`) e frase (`is`/`as`) são exceções: operam além de uma linha por definição. Text objects baseados em Treesitter (ver [[12 - Treesitter avançado]]) também são context-aware e frequentemente resolvem esse problema.

### 3. Usar `:%s` quando `.` resolveria

Para 2-4 ocorrências sequenciais que você quer alterar individualmente, o fluxo `cgn` + `.` é mais rápido e mais seguro que `:%s`:

```
:%s/oldName/newName/gc    → substitui globalmente com confirmação (interativo, mais lento)

*cgnnewName<Esc>...       → busca, altera a primeira, repete com . nas que quiser
```

`:%s` é ideal para substituições globais cegas ou quando há dezenas de ocorrências. Para 2-5 casos contextuais, `.` + controle manual é mais preciso e não requer escapar padrões de regex.

**Regra prática:** se você vai confirmar cada ocorrência de qualquer jeito, use `cgn` + `.`. Se é global e não-ambíguo, use `:%s`.

### 4. Contagem antes vs depois do operador

```
3dw    → equivale a d3w para a maioria dos casos (delete 3 words)
d3w    → semanticamente "delete aplicado à motion 3w"
```

Para operadores simples como `d` + `w`, o resultado é idêntico. A distinção aparece em operadores de linha como `>`:

```
3>>    → indenta 3 linhas a partir do cursor (count aplicado ao operador de linha)
>>     → indenta 1 linha
```

`>>` não aceita motion/text object — é sempre "linha atual". O count vai antes do operador nesse caso. Saber disso evita erros ao tentar `>>3j` (não funciona como esperado).

## Em inglês

Esta seção cobre o vocabulário técnico de motions/operadores em contextos de entrevistas, documentação e pair programming em inglês.

- **motion** — *motion* (sem tradução direta). "Use a **motion** like `w` or `e` to define the range for your operator."
- **operador** — *operator*. "The **operator** `d` deletes, `c` changes, and `y` yanks — always composed with a motion or text object."
- **text object** — *text object* (sem tradução direta). "**Text objects** like `iw` or `i"` select semantic regions regardless of cursor position within the target."
- **palavra** — *word*. "In Vim, a **word** (`w`) is delimited by punctuation; a WORD (`W`) is delimited only by whitespace."
- **palavra-WORD** — *WORD* (mantido). "Use **WORD** motions (`W`, `B`, `E`) to jump over compound identifiers like `foo.bar.baz` as a single unit."
- **interno (prefixo i-)** — *inside / inner*. "The **inner** text object (`i"`) selects only the content between delimiters, excluding them."
- **envolvente (prefixo a-)** — *around / a-prefix*. "The **around** text object (`a"`) includes the delimiters themselves, useful when you want to remove the whole construct."
- **repetir (dot)** — *repeat (dot command)*. "The **dot command** (`.`) repeats the last change — combine it with `cgn` for surgical multi-occurrence edits."
- **gramática** — *grammar*. "Vim's operator + motion **grammar** makes it composable: learn any new operator and it immediately works with all motions you know."
- **contagem** — *count*. "Prefix a **count** before a motion or command (`3w`, `d5j`) to repeat it without pressing the key multiple times."

## Veja também

- [[01 - Modal editing]]
- [[03 - Edição e navegação]]
- [[04 - LazyVim tour]]
- [[10 - Registers, marks, macros]] (registers recebem o yank de `y` e o delete de `d`)
- [[12 - Treesitter avançado]] (text objects ts-aware ampliam o conjunto padrão)
- [[03-Dominios/Tecnologia/Terminal/Editor/index|MOC do galho]]
- [[Dicionário do Terminal#Motion|motion]]
- [[Dicionário do Terminal#Operador|operador]]
- [[Dicionário do Terminal#Text object|text object]]

## Referências

- [Neovim — motion.txt](https://neovim.io/doc/user/motion.html) (`:help motion.txt`)
- [Neovim — text-objects](https://neovim.io/doc/user/motion.html#text-objects) (`:help text-objects`)
- [Vim Text Objects: The Definitive Guide — thevaluable.dev](https://thevaluable.dev/vim-text-objects/)
- [ThePrimeagen — Vim As Your Editor (YouTube)](https://www.youtube.com/watch?v=X6AR2RMB5tE)
- [Practical Vim, 2nd ed. — Drew Neil](https://pragprog.com/titles/dnvim2/practical-vim-second-edition/)
