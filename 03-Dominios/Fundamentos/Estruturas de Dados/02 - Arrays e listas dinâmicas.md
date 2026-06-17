---
title: "Arrays e listas dinâmicas"
created: 2026-06-17
updated: 2026-06-17
type: concept
progress: backlog
status: seedling
publish: false
fase: iniciado
tags:
  - fundamentos
  - estruturas-de-dados
  - iniciado
  - arrays
  - entrevista
---

# Arrays e listas dinâmicas

O array é a estrutura mais antiga e mais simples que existe — e, justamente por isso, a mais subestimada.

Quase toda outra estrutura de dados é construída sobre ele por baixo. A tabela hash guarda seus buckets num array. O heap é um array. O `ArrayList`, a `list` do Python, a slice do Go — todos são, no fundo, um array que cresceu sozinho.

Esta é a primeira estrutura concreta do galho. Depois de [[01 - O que é uma estrutura de dados|entender o que é uma estrutura de dados]] de forma abstrata, aqui você desce ao nível da memória: o que é um array de verdade, por que o acesso por índice é O(1), e como quatro linguagens — Java, TypeScript, Python e Go — pegam o mesmo conceito e o implementam de quatro jeitos radicalmente diferentes.

> [!abstract] TL;DR
> Um **array** é uma região **contígua** de memória com tamanho fixo. O acesso por índice é O(1) porque o endereço se calcula direto: `base + i · tamanho`. Por estarem juntos na memória, arrays têm **localidade de cache** excelente — a razão real de eles ganharem de estruturas "teoricamente melhores". Inserir/remover no meio é O(n) (precisa deslocar). Uma **lista dinâmica** (`ArrayList`, `list`, slice) embrulha um array interno e cresce copiando para um array maior — `append` é O(1) **amortizado**. O fator de crescimento é um trade-off (tempo × memória desperdiçada): Java cresce **1,5×**, Python ~1,125× mais constante, Go dobra até 256 elementos e depois suaviza. O grande insight senior: o mesmo "array" tem **quatro modelos de memória** distintos — valores contíguos (`int[]` do Java, `[]int` do Go, typed arrays do JS) versus ponteiros espalhados (`Integer[]` do Java, `list` do Python). E a slice do Go tem o twist que define a linguagem: um header `(ptr, len, cap)`.

## O que é um array, de fato

Comece pela imagem mental certa, porque ela explica tudo o que vem depois.

Um array é um **bloco único e contíguo de memória**, dividido em células de tamanho igual.

"Contíguo" é a palavra-chave. As células não estão espalhadas — estão grudadas, uma do lado da outra, na mesma vizinhança da memória. Um `int[5]` em Java é um bloco de 20 bytes seguidos (5 inteiros de 4 bytes), não cinco inteiros perdidos em lugares aleatórios.

Esse layout tem três consequências diretas, e cada uma é uma propriedade que você vai citar em entrevista.

### Acesso por índice é O(1)

Por que ler `arr[i]` custa o mesmo, não importa se `i` é 0 ou 1 milhão?

Porque o computador não *procura* a posição `i` — ele a **calcula**:

```
endereço = endereço_base + i · tamanho_do_elemento
```

Se o array começa no endereço `1000` e cada elemento ocupa 4 bytes, então `arr[3]` está em `1000 + 3·4 = 1012`. Uma multiplicação e uma soma. Constante. Não há varredura, não há comparação — só aritmética de ponteiro.

Esse é o superpoder do array, e a razão de ele ser a fundação de tantas outras estruturas: **acesso aleatório verdadeiramente O(1)**.

A imagem abaixo mostra esse cálculo acontecendo.

```mermaid
flowchart LR
    subgraph Memoria["Memória contígua"]
        direction LR
        C0["base+0\n'A'"]
        C1["base+4\n'B'"]
        C2["base+8\n'C'"]
        C3["base+12\n'D'"]
        C4["base+16\n'E'"]
        C0 --- C1 --- C2 --- C3 --- C4
    end
    Q["arr[3]?"] -->|"base + 3 · 4 = base+12"| C3
```

Leitura do diagrama: para achar `arr[3]`, o sistema não percorre as células — ele aplica `base + 3 · tamanho` e salta direto para a célula que contém `'D'`. O índice vira aritmética, e por isso o custo independe da posição.

### Localidade de cache: a vantagem invisível

Aqui está a propriedade que os livros de Big-O escondem, mas que decide o desempenho real.

A CPU não lê a memória byte a byte. Ela lê em blocos chamados **cache lines** (tipicamente 64 bytes) e os guarda numa memória ultrarrápida (o cache L1/L2).

Quando você lê `arr[0]`, a CPU traz para o cache não só `arr[0]`, mas toda a vizinhança — `arr[1]`, `arr[2]`, ... — de graça, no mesmo movimento.

Resultado: iterar um array sequencialmente é absurdamente rápido. Os próximos elementos já estão no cache quando você chega neles.

> [!tip] Por que isso vence o Big-O
> Uma lista encadeada e um array têm a mesma complexidade de iteração: O(n). Mas percorrer 10.000 inteiros num array pode ser **ordens de magnitude** mais rápido, porque os elementos estão grudados (cache hits) enquanto os nós da lista estão espalhados pela memória (cache misses, cada um custando uma ida cara à RAM). Big-O conta operações; localidade de cache decide quanto cada operação realmente custa. Voltamos a isso em [[03 - Listas encadeadas]].

### Tamanho fixo e o custo do meio

A terceira consequência do bloco contíguo é uma limitação.

Como o array é um bloco alocado de uma vez, ele tem **tamanho fixo**. Um `int[10]` não cresce — não há garantia de que a memória logo depois dele esteja livre. Para "crescer", a única saída é alocar um bloco maior e copiar tudo.

E inserir ou remover **no meio** é O(n).

Por quê? Porque o array não pode ter buracos — ele é contíguo por definição. Se você insere na posição 2 de um array de 10 elementos, os 8 elementos à direita precisam **deslocar** uma casa para abrir espaço. Remover é o mesmo ao contrário: todos à direita deslocam para tampar o buraco.

> [!summary] As três propriedades, em uma frase
> Array = bloco contíguo → acesso por índice O(1) (aritmética) + localidade de cache excelente (vizinhos juntos) − tamanho fixo e inserção/remoção no meio O(n) (deslocamento).

## Array dinâmico: o array que cresce sozinho

O tamanho fixo do array é um incômodo. Na prática, raramente sabemos de antemão quantos elementos virão.

A solução é o **array dinâmico** (ou lista dinâmica): uma estrutura que **embrulha** um array interno e o gerencia para você.

A ideia é simples. A lista guarda dois números:

- **tamanho** (`size`/`len`) — quantos elementos você realmente colocou;
- **capacidade** (`capacity`/`cap`) — quantos cabem no array interno antes de precisar crescer.

Enquanto `size < capacity`, adicionar no fim é só escrever na próxima célula livre: O(1). Quando o array enche (`size == capacity`), a lista faz o **resize**: aloca um array maior, copia tudo, e descarta o antigo.

```mermaid
flowchart LR
    A["cap=4, size=4\n[a][b][c][d]\nCHEIO"] -->|"append(e)"| B["aloca cap=6\n(1,5× de 4)"]
    B -->|"copia a,b,c,d"| C["[a][b][c][d][_][_]"]
    C -->|"escreve e"| D["cap=6, size=5\n[a][b][c][d][e][_]"]
    D -->|"próximos appends"| E["O(1) direto\naté encher de novo"]
```

Leitura do diagrama: quando o array interno enche, o `append` paga uma vez o custo O(n) de alocar um array maior e copiar tudo; depois disso, os próximos `append` voltam a ser O(1) baratos até a capacidade esgotar de novo. O custo da cópia se dilui sobre muitos appends.

### Por que `append` é O(1) *amortizado*

Essa palavra — **amortizado** — é um sinal de senioridade em entrevista. Vale entender de verdade.

Cada `append` individual é O(1)... exceto os raros que disparam um resize, que são O(n).

A mágica está na frequência. Como a capacidade **dobra** (ou cresce por um fator), os resizes ficam cada vez mais espaçados: você copia 4, depois 8, depois 16, depois 32...

Some o custo total de inserir n elementos: as cópias somam `4 + 8 + 16 + ... + n`, uma série geométrica que converge para **~2n**. Distribuído pelos n appends, dá custo constante por operação.

> [!note] Amortizado ≠ caso médio
> "Amortizado O(1)" não é uma probabilidade — é uma **garantia sobre uma sequência**. Qualquer sequência de n appends custa O(n) no total, logo O(1) por operação na média da sequência. Um único append pode ser O(n) (azarado, caiu no resize), mas a soma é sempre limitada. Frase de entrevista: *"append is amortized O(1) — individual inserts can be O(n) during a resize, but any sequence of n appends totals O(n)."*

### O trade-off do fator de crescimento

Por que dobrar? Por que não crescer de 1 em 1, ou de 1000 em 1000?

É um trade-off entre **tempo** e **memória desperdiçada**.

- **Fator pequeno** (ex: +1 a cada vez) → quase nenhum desperdício de memória, mas resize a cada append → custo total O(n²). Péssimo.
- **Fator grande** (ex: 2×) → resizes raros, ótimo tempo amortizado, mas pode desperdiçar até ~50% da memória logo após um resize (você dobrou, mas só usou uma célula a mais).

Cada linguagem escolhe um ponto diferente nessa curva — e é exatamente aí que as implementações divergem. Java escolhe 1,5×. Go dobra (e depois suaviza). Python cresce devagar, ~1,125×. Veremos cada uma a seguir.

> [!info] Por que o meio continua O(n)
> O array dinâmico só otimiza o crescimento **pelo fim**. Inserir ou remover no **meio** continua O(n), porque o array interno ainda é contíguo — os elementos à direita continuam tendo que deslocar. Lista dinâmica resolve o "tamanho fixo", não o "custo do meio". Para inserção/remoção barata no meio (com referência), é território de [[03 - Listas encadeadas]].

## Implementações comparadas: Java · TypeScript · Python · Go

Agora a parte que separa quem sabe "array" de quem sabe *como o array vive* em cada linguagem.

O conceito é o mesmo nas quatro. Mas a representação na memória é tão diferente que muda performance, pegadinhas e idiomas. A pergunta central que vamos perseguir é uma só:

*Os elementos estão guardados como valores contíguos, ou como ponteiros para objetos espalhados?*

### Java: `int[]` contíguo vs `Integer[]` de referências

Java tem uma divisão brutal que outras linguagens escondem: **primitivos vs objetos**.

Um `int[]` é um array de **valores**: cada célula contém os 4 bytes do inteiro, em sequência, contíguos. É o array "puro" do conceito — máxima localidade de cache, zero indireção.

```java
int[] numeros = new int[5];   // 20 bytes contíguos de valores
numeros[3] = 42;              // escreve direto na célula
int x = numeros[3];           // lê o valor, sem indireção
```

Já um `Integer[]` (ou qualquer `Object[]`) é um array de **referências**: cada célula contém um **ponteiro** para um objeto `Integer` que vive em outro lugar do heap. Os valores estão espalhados; o array só guarda os endereços.

```java
Integer[] caixa = new Integer[5];  // 5 ponteiros contíguos...
caixa[3] = 42;                     // autoboxing: cria new Integer(42) no heap
                                   // ...mas o objeto 42 está longe, espalhado
```

Isso é o **boxing**, e o custo é duplo: memória (cada `Integer` tem overhead de objeto, ~16 bytes contra 4 de um `int`) e cache (seguir o ponteiro para um objeto distante = cache miss).

> [!warning] Arrays em Java são covariantes
> `Integer[]` é um subtipo de `Object[]` — isso se chama **covariância de arrays**, e é uma decisão de design controversa. Ela permite código que compila mas explode em runtime:
> ```java
> Object[] arr = new Integer[3];   // compila: covariância
> arr[0] = "uma string";           // ArrayStoreException em runtime!
> ```
> O array carrega seu tipo real e checa cada escrita, lançando `ArrayStoreException` se você tentar guardar o tipo errado. Generics (`List<Integer>`) são **invariantes** justamente para fechar esse buraco em tempo de compilação.

O array dinâmico de Java é o **`ArrayList`**, que embrulha um `Object[] elementData` interno.

Seu crescimento é **1,5×**, não 2×. No método `grow()`, a nova capacidade é `oldCapacity + (oldCapacity >> 1)` — o `>> 1` é divisão por 2 via bit shift, então 1,5×. A cópia usa `Arrays.copyOf`, que por baixo chama `System.arraycopy` (memória em bloco, nativo).

```java
List<String> lista = new ArrayList<>();   // cap inicial 10 no 1º add
lista.add("Ana");                          // O(1) amortizado
lista.get(0);                              // O(1)
lista.add(1, "x");                         // O(n): desloca à direita
lista.remove(0);                           // O(n): desloca à esquerda
((ArrayList<String>) lista).ensureCapacity(1000); // pré-aloca, evita resizes
```

Sequência de capacidades partindo de 10: 10 → 15 → 22 → 33 → 49... (cada uma é 1,5× a anterior, arredondado). Note que `ArrayList` sempre guarda `Object`, então `ArrayList<Integer>` **sempre faz boxing** — não existe `ArrayList` de primitivos (é onde bibliotecas como Eclipse Collections ou `IntStream` entram).

### TypeScript / JavaScript: o array que finge ser array

Em JS, `Array` é, tecnicamente, um **objeto** — um caso especial de objeto com chaves numéricas e uma propriedade `length`. Isso soa como um desastre de performance. E seria, se a engine fosse ingênua.

A V8 (Chrome, Node, Deno) não é ingênua. Ela classifica cada array por **elements kind** e escolhe a representação interna conforme o conteúdo.

Os tipos formam uma **treliça (lattice)**, do mais rápido ao mais lento:

- `PACKED_SMI_ELEMENTS` — só inteiros pequenos (Smi, *small integer*), densos. O backing store é contíguo, valores crus. O mais rápido.
- `PACKED_DOUBLE_ELEMENTS` — só números (com floats), densos. Ainda contíguo.
- `PACKED_ELEMENTS` — valores arbitrários (strings, objetos), densos. Array de ponteiros.
- As variantes `HOLEY_*` — versões "furadas" dos acima.
- `DICTIONARY_ELEMENTS` — o modo lento: vira um hash map de índice → valor.

Duas regras governam isso, e ambas são pegadinhas de performance.

**Regra 1 — packed vs holey.** Um array é *packed* (denso) se todas as posições de 0 a `length-1` estão preenchidas. Basta criar um "buraco" — `arr[100] = 1` num array de 3 elementos, ou `delete arr[1]` — para ele virar *holey*. E aqui está o veneno: **uma vez holey, sempre holey**. A V8 não promove de volta, mesmo que você preencha os buracos depois. Arrays holey são mais lentos porque toda iteração precisa checar se cada posição existe.

**Regra 2 — transições só descem.** A treliça é uma via de mão única. Adicione um float a um array de Smis e ele vira DOUBLE para sempre — mesmo que você sobrescreva o float com um inteiro depois. Misture tipos e ele cai para PACKED_ELEMENTS (ponteiros). Nunca sobe.

```typescript
const a = [1, 2, 3];      // PACKED_SMI: backing store contíguo, rápido
a.push(4.5);              // vira PACKED_DOUBLE (irreversível)
a.push("x");              // vira PACKED_ELEMENTS: array de ponteiros
const b = [1, 2, 3];
b[100] = 1;               // vira HOLEY: 97 buracos, iteração mais lenta p/ sempre
```

Em termos de complexidade, as operações de fim são amortizadas O(1) e as de início são O(n):

```typescript
const arr = [1, 2, 3];
arr.push(4);     // O(1) amortizado — escreve no fim
arr.pop();       // O(1)
arr.unshift(0);  // O(n) — desloca TODOS à direita para abrir o índice 0
arr.shift();     // O(n) — desloca todos à esquerda
```

> [!tip] Typed arrays = array contíguo de verdade
> Quando você precisa de números contíguos garantidos (processamento numérico, binário, performance), use **typed arrays**: `Int32Array`, `Float64Array`, `Uint8Array`. Eles são contíguos por especificação — não há elements kinds, não há holey, não há ponteiros. São o `int[]` do mundo JS.
> ```typescript
> const buf = new Int32Array(1000); // 4000 bytes contíguos, valores crus
> buf[3] = 42;                       // sem boxing, sem indireção
> ```

A lição: para a V8 te dar o array rápido (contíguo), mantenha-o **denso e homogêneo**. Arrays buracados ou de tipos misturados caem para representações mais lentas.

### Python: `list` é um array de ponteiros, sempre

Python tem o modelo mais uniforme — e mais caro — dos quatro.

Uma `list` do Python é um array dinâmico, sim. Mas é um array de **`PyObject*`**: ponteiros. Nunca valores crus. Em Python, *tudo é objeto*, inclusive os inteiros.

Isso significa que `[1, 2, 3]` **não** guarda os bytes 1, 2 e 3. Guarda três ponteiros, cada um apontando para um objeto inteiro (`PyLongObject`) que vive em outro lugar do heap.

```python
nums = [1, 2, 3]   # array contíguo de 3 ponteiros...
                   # ...para 3 objetos int espalhados pelo heap
```

A consequência é localidade de cache pobre: o array de ponteiros é contíguo, mas seguir cada ponteiro é um salto para um objeto distante. É o mesmo problema do `Integer[]` do Java, só que aqui é o **default e o único jeito** — não há `list` de primitivos.

O crescimento da `list` é mais conservador que o de Java ou Go. Em `list_resize` (`listobject.c`), a fórmula de over-allocation é:

```c
new_allocated = ((size_t)newsize + (newsize >> 3) + (newsize < 9 ? 3 : 6)) & ~(size_t)3;
```

Ou seja: `newsize + newsize/8 + constante`, arredondado para múltiplo de 4. Isso dá um fator de crescimento de aproximadamente **1,125×** mais um termo constante — bem menos agressivo que o 1,5× de Java ou o 2× de Go. A sequência de capacidades resultante é: 0, 4, 8, 16, 24, 32, 40, 52, 64, 76...

```python
nums = []
for i in range(100):
    nums.append(i)   # O(1) amortizado; resizes seguindo a sequência acima
nums[3]              # O(1)
nums.insert(0, -1)   # O(n): desloca todos os ponteiros à direita
nums.pop()           # O(1): remove do fim
nums.pop(0)          # O(n): remove do início, desloca todos
```

> [!info] Quando você precisa de números contíguos em Python
> A `list` nunca te dá valores contíguos. Para isso, há duas saídas: o módulo `array` da stdlib (`array('i', [1,2,3])` — um array de inteiros C de verdade) ou, para qualquer coisa séria, **NumPy** (`np.array([1,2,3])` — `ndarray` contíguo, vetorizado, com localidade de cache real). O custo "tudo-é-objeto" é o motivo de loops numéricos em Python puro serem lentos e de NumPy existir.

### Go: array é valor, slice é um header de 3 palavras

Go faz uma distinção que nenhuma das outras faz tão explicitamente: **array vs slice**.

Um **array** em Go é um **tipo valor**, e seu tamanho faz parte do tipo. `[3]int` e `[4]int` são tipos *diferentes*. E porque é valor, ele é **copiado** ao ser atribuído ou passado para uma função:

```go
a := [3]int{1, 2, 3}
b := a          // CÓPIA completa dos 3 inteiros
b[0] = 99       // não afeta a — são blocos independentes
func f(arr [3]int) { ... }  // recebe uma CÓPIA do array inteiro
```

Justamente por isso arrays de tamanho fixo são raros em Go idiomático. O que você usa o tempo todo é a **slice**.

Uma slice **não** é um array. É um **header de 3 palavras** que aponta para um array de fundo (*backing array*):

- **ptr** — ponteiro para o início dos dados no backing array;
- **len** — quantos elementos a slice expõe;
- **cap** — quantos cabem do ptr até o fim do backing array.

```mermaid
flowchart LR
    subgraph S1["slice s1"]
        P1["ptr"]
        L1["len=3"]
        C1["cap=5"]
    end
    subgraph Backing["backing array (cap=5)"]
        direction LR
        B0["10"]
        B1["20"]
        B2["30"]
        B3["?"]
        B4["?"]
        B0 --- B1 --- B2 --- B3 --- B4
    end
    subgraph S2["slice s2 = s1[1:3]"]
        P2["ptr"]
        L2["len=2"]
        C2["cap=4"]
    end
    P1 --> B0
    P2 --> B1
```

Leitura do diagrama: `s1` e `s2` são dois headers diferentes, mas seus ponteiros entram no **mesmo** backing array — `s2` começa uma casa adiante. Escrever em `s2[0]` muda o que `s1[1]` enxerga: elas compartilham os dados. Esse compartilhamento é a fonte de poder e de bugs das slices.

O `append` faz a slice crescer. Desde **Go 1.18**, a fórmula mudou: em vez do antigo "dobra até 1024, depois 1,25×", a função `nextslicecap` (em `runtime/slice.go`) suaviza a curva — **dobra a capacidade até 256 elementos**, e a partir daí aplica `newcap += (newcap + 3·256) >> 2` iterativamente, dando um fator que desce gradualmente de 2× rumo a ~1,25× conforme a slice cresce.

```go
s := make([]int, 0, 4)  // len=0, cap=4
s = append(s, 1, 2, 3)  // len=3, cap=4: cabe, sem realocar
s = append(s, 4, 5)     // estourou cap 4 → dobra para 8, copia, REALOCA
```

> [!danger] A pegadinha do aliasing
> Porque slices compartilham backing arrays, `append` esconde uma armadilha. Se há espaço (`len < cap`), `append` escreve **no mesmo backing array** — e silenciosamente sobrescreve o vizinho:
> ```go
> base := []int{1, 2, 3, 4, 5}
> a := base[0:2]          // len=2, cap=5 (vê até o fim do backing)
> a = append(a, 99)       // cap sobrava → escreve em base[2]!
> // base agora é [1, 2, 99, 4, 5] — mutou "de longe"
> ```
> Se **não** há espaço (`len == cap`), `append` realoca para um novo backing array — e aí as slices **silenciosamente se desconectam**: a partir desse append elas não compartilham mais nada. O mesmo `append` ora muta o vizinho, ora não — dependendo da capacidade. Esse é o bug de slice clássico de Go.

A defesa contra aliasing acidental é a **expressão de slice completa** `s[a:b:c]`, que limita o `cap` (terceiro índice = até onde vai a capacidade), forçando o próximo `append` a realocar em vez de pisar no vizinho. E `copy(dst, src)` faz uma cópia explícita e segura quando você quer independência real:

```go
a := base[0:2:2]        // cap forçado a 2 → append SEMPRE realoca, não toca base
b := make([]int, len(src))
copy(b, src)            // b é independente de src
```

### A síntese senior: quatro modelos de memória

Recapitule o que viu, porque é exatamente o tipo de comparação que impressiona em entrevista internacional.

O mesmo conceito — "array" — se materializa em **dois modelos fundamentais de memória**:

- **Valores contíguos** (rápido, cache-friendly): `int[]` do Java, `[]int` do Go, typed arrays (`Int32Array`) e arrays PACKED_SMI do JS. Os dados estão na linha, grudados.
- **Ponteiros espalhados** (flexível, cache-hostil): `Integer[]`/`Object[]` do Java, `list` do Python (sempre), arrays PACKED_ELEMENTS do JS. O array guarda endereços; os objetos vivem longe.

A imagem abaixo contrasta os dois.

```mermaid
flowchart TB
    subgraph Valores["Valores contíguos — int[], []int, Int32Array"]
        direction LR
        V0["42"]
        V1["17"]
        V2["99"]
        V3["08"]
        V0 --- V1 --- V2 --- V3
    end
    subgraph Ponteiros["Ponteiros — Integer[], Python list"]
        direction LR
        Q0["ptr"]
        Q1["ptr"]
        Q2["ptr"]
        Q3["ptr"]
        Q0 --- Q1 --- Q2 --- Q3
    end
    O0["obj 42"]
    O1["obj 17"]
    O2["obj 99"]
    O3["obj 08"]
    Q0 --> O2
    Q1 --> O0
    Q2 --> O3
    Q3 --> O1
    Valores -.->|"1 cache line traz vizinhos\nde graça → rápido"| Cache["cache hits"]
    Ponteiros -.->|"cada ptr salta p/ objeto distante\n→ cache miss"| Miss["cache misses"]
```

Leitura do diagrama: no modelo de valores, ler uma célula traz as vizinhas no mesmo cache line — iteração voa. No modelo de ponteiros, o array de endereços é contíguo, mas cada acesso segue um ponteiro para um objeto espalhado, e cada salto é um cache miss. É a mesma estrutura lógica com desempenho de RAM completamente diferente.

E sobre tudo isso paira o twist do Go: a **slice é um header `(ptr, len, cap)`**, um valor pequeno que aponta para os dados. É o que permite passar slices baratas por valor (copia 3 palavras, não os dados) e o que cria toda a semântica de aliasing. Nenhuma das outras três linguagens expõe a estrutura interna do array dinâmico tão diretamente quanto Go.

> [!quote] A resposta de uma frase
> *"It's the same array concept with four memory models. Java splits primitives from objects — `int[]` is contiguous values, `Integer[]` is boxed pointers. Python's `list` is always an array of pointers, never raw values. JavaScript's V8 picks a representation by elements kind — packed-Smi arrays are contiguous, holey or mixed arrays fall back to slower stores. And Go's slice is a three-word header over a backing array, which is fast to pass but creates aliasing gotchas with append."*

## Padrões em entrevista: arrays são o palco

Reconhecer que um problema "é de array" é metade da solução. Três técnicas aparecem o tempo todo sobre arrays, e o enunciado costuma sinalizar qual usar.

### Two pointers (dois ponteiros)

Dois índices percorrem o array — das pontas para o meio, ou um rápido e um lento. Transforma muitos problemas O(n²) em O(n).

*Sinais no enunciado:* array **ordenado**, "par com soma X", "remover duplicatas in-place", "inverter", "é palíndromo".

```java
// Par com soma alvo em array ordenado — O(n), O(1) espaço
int i = 0, j = arr.length - 1;
while (i < j) {
    int soma = arr[i] + arr[j];
    if (soma == alvo) return new int[]{i, j};
    if (soma < alvo) i++;   // precisa de mais → avança o esquerdo
    else j--;               // precisa de menos → recua o direito
}
```

### Sliding window (janela deslizante)

Uma janela contígua de tamanho fixo ou variável desliza pelo array, mantendo um agregado (soma, contagem, máximo) sem recomputar do zero.

*Sinais no enunciado:* "subarray/substring contíguo", "janela de tamanho k", "maior/menor subarray que satisfaz...".

```java
// Maior soma de subarray de tamanho k — O(n)
int soma = 0, melhor = Integer.MIN_VALUE;
for (int fim = 0; fim < arr.length; fim++) {
    soma += arr[fim];                 // entra à direita
    if (fim >= k) soma -= arr[fim - k]; // sai à esquerda
    if (fim >= k - 1) melhor = Math.max(melhor, soma);
}
```

### Prefix sum (soma de prefixos)

Pré-computa um array de somas acumuladas para responder "soma do intervalo [i, j]" em O(1) cada, após O(n) de preparo.

*Sinais no enunciado:* "soma de um intervalo", "subarray com soma igual a X" (prefix sum + HashMap), "muitas range queries".

```java
// pre[i] = soma de arr[0..i-1]; soma de [i,j] = pre[j+1] - pre[i]
int[] pre = new int[arr.length + 1];
for (int i = 0; i < arr.length; i++) pre[i + 1] = pre[i] + arr[i];
int somaIntervalo = pre[j + 1] - pre[i];  // O(1) por consulta
```

> [!tip] O reflexo de entrevista
> Viu "array ordenado" + "par/triplo"? Pense **two pointers**. Viu "subarray/substring contíguo"? Pense **sliding window**. Viu "soma de intervalo" ou "subarray com soma X"? Pense **prefix sum** (com HashMap se a soma for arbitrária). Esses três cobrem uma fatia enorme dos problemas de array do NeetCode.

## Quando usar (e quando não)

Use array ou lista dinâmica quando:

- **O acesso por índice domina** — você lê por posição com frequência.
- **A iteração sequencial é frequente** — a localidade de cache te dá performance que o Big-O não mostra.
- **O crescimento é pelo fim** — `append`/`push` é o padrão de escrita.
- **O tamanho é previsível** — e aí você pode pré-alocar (`ensureCapacity`, `make([]T, 0, n)`) e evitar resizes.

Evite (ou pense duas vezes) quando:

- **Inserção/remoção no meio é frequente** — é O(n); considere [[03 - Listas encadeadas]] se você tiver referência ao ponto, ou uma estrutura diferente.
- **Você busca por chave, não por posição** — lookup por valor é O(n) num array; isso é trabalho de [[05 - Tabelas hash]].
- **Inserções no início são frequentes** — `unshift`/`insert(0)` é O(n); um deque resolve.

> [!summary] A regra prática
> No dia a dia de backend, array dinâmico (`ArrayList`, `list`, slice) é a estrutura **default** para sequências. Ela ganha por localidade de cache mesmo em cenários onde a teoria favoreceria outra coisa. Só abandone o array dinâmico quando o perfil de acesso for claramente outro: lookup por chave (→ hash), inserção no meio com referência (→ lista encadeada), prioridade (→ heap).

## Em entrevista

Falar de arrays com fluência em inglês é mostrar que você entende o nível da memória, não só a API.

> "An array is a contiguous block of memory with fixed size. Random access is O(1) because the address is computed directly — base plus index times element size — not searched. That contiguity also gives excellent cache locality, which is often the real reason arrays outperform structures with better Big-O on paper.
>
> Insertion or removal in the middle is O(n), because you have to shift elements to keep it contiguous. To get around the fixed size, we use a dynamic array — `ArrayList` in Java, `list` in Python, a slice in Go. It wraps an internal array and grows by reallocating and copying, which makes append amortized O(1): any sequence of n appends totals O(n), even though an individual append can be O(n) during a resize.
>
> The growth factor is a time-versus-memory trade-off. Java grows the backing array by 1.5×, Go doubles up to 256 elements and then tapers, Python grows more conservatively, around 1.125× plus a constant.
>
> What's interesting is how differently languages lay this out in memory. Java's `int[]` stores contiguous values, but `Integer[]` stores boxed pointers — same with Python's list, which is always an array of pointers. Go's slice is a three-word header over a backing array, which is why two slices can alias the same storage and an append can silently mutate — or un-share — a neighbor."

### Frases úteis

- "Append is amortized O(1) — resizes happen, but they're rare and the total cost is linear."
- "I'd pre-size the list if I know the count, to avoid intermediate reallocations."
- "Random access is O(1), but inserting in the middle is O(n) — I'd reach for a different structure if that's the hot path."
- "In Go I have to watch for slice aliasing — append can mutate the backing array shared with another slice."
- "For tight numeric loops in Python I'd use NumPy, because a plain list is an array of pointers, not contiguous values."

### Vocabulário-chave

- array contíguo → contiguous array
- lista dinâmica / array dinâmico → dynamic array / growable array
- acesso aleatório → random access
- localidade de cache → cache locality
- linha de cache → cache line
- redimensionar / realocar → resize / reallocate
- amortizado → amortized
- fator de crescimento → growth factor
- deslocar (elementos) → shift (elements)
- boxing / autoboxing → boxing / autoboxing
- ponteiro / referência → pointer / reference
- backing array (array de fundo) → backing array
- cabeçalho da slice → slice header
- aliasing (compartilhamento) → aliasing
- pré-alocar / pré-dimensionar → pre-allocate / pre-size

## Referências

- [Elements kinds in V8 · v8.dev](https://v8.dev/blog/elements-kinds) — packed/holey, a treliça de elements kinds, transições só descendentes, dictionary mode.
- [cpython/Objects/listobject.c · GitHub](https://github.com/python/cpython/blob/main/Objects/listobject.c) — `list_resize` e a fórmula de over-allocation `(newsize + (newsize >> 3) + ...) & ~3` (~1,125× + constante).
- [runtime: make slice growth formula a bit smoother · golang/go@2dda92f](https://github.com/golang/go/commit/2dda92ff6f9f07eeb110ecbf0fc2d7a0ddd27f9d) — mudança de Go 1.18: threshold 256, fórmula `nextslicecap`.
- [go/src/runtime/slice.go · GitHub](https://github.com/golang/go/blob/master/src/runtime/slice.go) — `growslice`/`nextslicecap`, header da slice.
- [Go: How slices grow · Graham King](https://darkcoding.net/software/go-how-slices-grow/) — crescimento de slice e aliasing explicados.
- [ArrayList.grow — formula `oldCapacity + (oldCapacity >> 1)`](https://medium.com/@ashutosh-ceg/day-12-arraylist-initial-capacity-growth-rate-trick-question-2e2ff73e7f11) — crescimento 1,5× do `ArrayList` (verificável também no fonte do OpenJDK `ArrayList.java`).
- [Big-O Cheat Sheet](https://bigocheatsheet.com/) — complexidades de array e lista dinâmica.
- [Visualgo — Arrays](https://visualgo.net/) — visualização interativa.

> [!info] Lastro
> Os quatro comportamentos centrais foram verificados em fonte primária: V8 elements kinds (blog oficial do V8), crescimento da `list` (CPython `listobject.c`), crescimento e aliasing de slice (commit e `slice.go` do Go), crescimento 1,5× do `ArrayList` (fórmula `oldCapacity + (oldCapacity >> 1)` do OpenJDK). A fórmula exata de over-allocation do CPython e o threshold 256 do Go 1.18 vêm do código-fonte citado; valores como cache line de 64 bytes e overhead de ~16 bytes por `Integer` são típicos de JVMs HotSpot de 64 bits e podem variar por plataforma/configuração.

## Veja também

- [[01 - O que é uma estrutura de dados]] — a nota de abertura: contrato, três dimensões, Big-O mínimo.
- [[03 - Listas encadeadas]] — o contraponto do array: nós espalhados por ponteiros, inserção O(1) com referência, mas cache-hostil.
- [[05 - Tabelas hash]] — quando a busca é por chave e não por posição.
- [[Dicionário de Fundamentos]] — verbetes de amortizado, localidade de cache, boxing, slice.
