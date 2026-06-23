---
title: "Arrays e varargs"
created: 2026-06-02
updated: 2026-06-02
type: concept
progress: backlog
status: seedling
publish: true
fase: iniciado
tags:
  - java
  - linguagem
  - iniciado
  - arrays
  - varargs
aliases:
  - Array
  - varargs
---

# Arrays e varargs

> [!abstract] TL;DR
> **Array** é um container de tamanho fixo e tipo homogêneo, alocado no heap. Suporta múltiplas dimensões via "jagged arrays" (array de arrays). A classe `Arrays` fornece utilitários essenciais (`sort`, `fill`, `copyOf`, `equals`, `toString`) e `System.arraycopy` oferece cópia nativa de alta performance. **Varargs** é açúcar sintático sobre array que simplifica APIs de aridade variável — mas esconde armadilhas sérias ao combinar com generics (heap pollution, `@SafeVarargs`) e com `Arrays.asList()` (lista de tamanho fixo que lança `UnsupportedOperationException` no `add`).

## O que é

Um **array** em Java é um container de tamanho fixo que armazena elementos de um único tipo (primitivo ou referência). Uma vez criado, o tamanho não pode ser alterado. O array em si é um objeto alocado no heap — inclusive arrays de primitivos.

**Varargs** (variable-length arguments, Java 5+) permite declarar métodos que aceitam zero ou mais argumentos de um mesmo tipo, sem forçar o chamador a montar um array explicitamente. Internamente, o compilador converte a lista de argumentos em um array antes de passar ao método.

Juntos, arrays e varargs formam a base de muitas APIs Java — de `System.out.printf` a `List.of` — e aparecem com frequência em perguntas de entrevista precisamente porque suas armadilhas são sutis.

## Como funciona

### Declaração e inicialização

```java
// Declaração com tamanho (valores default: 0, false, null)
int[] notas = new int[5];           // [0, 0, 0, 0, 0]
String[] nomes = new String[3];     // [null, null, null]

// Inicialização com array literal (array initializer)
int[] primos = {2, 3, 5, 7, 11};   // tamanho inferido: 5
int[] pares = new int[]{0, 2, 4};   // forma explícita — necessária em expressões

// Acesso e tamanho
int primeiro = primos[0];           // 2
int ultimo = primos[primos.length - 1]; // 11 — length é campo, não método
// primos[5] → ArrayIndexOutOfBoundsException (índice fora de [0, length-1])
```

**Valores default:** ao criar um array com `new T[n]`, todos os elementos são inicializados com o default do tipo — `0` para numéricos, `false` para `boolean`, `null` para referências.

**`length`** é um campo público final do objeto array, não um método. Confundir com `String.length()` (método) ou `Collection.size()` (método) é um erro clássico de iniciante.

---

### Arrays multidimensionais

Java não tem matrizes verdadeiras — tem **jagged arrays** (arrays de arrays). Um `int[][]` é um array cujos elementos são referências para outros arrays `int[]`, que podem ter tamanhos diferentes.

```java
// Declaração retangular (todos os sub-arrays com mesmo tamanho)
int[][] matriz = new int[3][4];     // 3 linhas, 4 colunas — 12 ints no total

// Inicialização literal
int[][] grade = {
    {1, 2, 3},
    {4, 5, 6},
    {7, 8, 9}
};
int valor = grade[1][2];            // 6 — linha 1, coluna 2

// Jagged array (sub-arrays com tamanhos distintos)
int[][] triangulo = new int[3][];
triangulo[0] = new int[]{1};
triangulo[1] = new int[]{1, 2};
triangulo[2] = new int[]{1, 2, 3};
// triangulo[2].length == 3, triangulo[0].length == 1
```

A implicação prática: ao iterar um multidimensional, o comprimento de cada linha pode variar — usar `linha.length` em vez de um valor fixo é o padrão correto.

---

### Utilitários (`Arrays.sort/fill/copyOf/equals/toString`, `System.arraycopy`)

A classe `java.util.Arrays` (Java SE 21) concentra os utilitários mais usados:

```java
import java.util.Arrays;

int[] nums = {5, 2, 8, 1, 9, 3};

// Ordenação — Dual-Pivot Quicksort para primitivos, TimSort para objetos
Arrays.sort(nums);                          // [1, 2, 3, 5, 8, 9] — in-place
Arrays.sort(nums, 1, 4);                    // ordena somente [fromIndex, toIndex)

// Preenchimento
Arrays.fill(nums, 0);                       // [0, 0, 0, 0, 0, 0]
Arrays.fill(nums, 2, 5, 7);                // preenche índices 2–4 com 7

// Cópia
int[] copia = Arrays.copyOf(nums, 3);       // primeiros 3 elementos
int[] ampliado = Arrays.copyOf(nums, 10);   // expande, pads com 0
int[] trecho = Arrays.copyOfRange(nums, 1, 4); // [fromIndex, toIndex)

// Comparação (elemento a elemento)
boolean iguais = Arrays.equals(nums, copia); // false — tamanhos diferentes
int[][] a = {{1,2},{3,4}};
int[][] b = {{1,2},{3,4}};
Arrays.deepEquals(a, b);                    // true — compara recursivamente

// Representação em String
System.out.println(Arrays.toString(nums));   // [0, 0, 0, 0, 0, 0]
System.out.println(Arrays.deepToString(a));  // [[1, 2], [3, 4]]

// Busca binária (array deve estar ordenado!)
int idx = Arrays.binarySearch(new int[]{1,3,5,7}, 5); // 2
```

**`System.arraycopy`** — cópia nativa (JVM intrínseca), mais rápida para grandes volumes:

```java
int[] src = {1, 2, 3, 4, 5};
int[] dst = new int[5];
System.arraycopy(src, 1, dst, 0, 3);  // src[1..3] → dst[0..2]: [2, 3, 4, 0, 0]
// System.arraycopy(src, srcPos, dst, dstPos, length)
```

---

### Varargs

**Desugaring:** o compilador converte um parâmetro varargs `T... args` em `T[] args`. O chamador pode passar zero ou mais argumentos separados por vírgula — ou passar explicitamente um array.

```java
// Declaração
public static int somar(int... numeros) {
    int total = 0;
    for (int n : numeros) total += n;
    return total;
}

// Chamadas equivalentes
somar(1, 2, 3);                  // compilador cria new int[]{1, 2, 3}
somar(new int[]{1, 2, 3});       // array explícito — mesmo resultado
somar();                          // new int[]{} — array vazio, não null
```

**Exemplos na API padrão:**
- `System.out.printf(String format, Object... args)` — aceita qualquer número de argumentos para formatar
- `List.of(E... elements)` (Java 9+) — cria lista imutável de qualquer tamanho
- `String.format(String format, Object... args)`

**Ambiguidade de overload:** quando dois métodos sobrecarregam varargs, o compilador pode não conseguir resolver qual chamar:

```java
void log(String... msgs) { ... }
void log(Object... objs) { ... }

log("hello");   // erro de compilação: ambiguous method call
                // String é subtype de Object — ambos se aplicam
```

A regra: varargs é a opção de "último recurso" na resolução de overload. Prefira evitar sobrecargas com varargs de tipos relacionados por herança.

**Autoboxing + varargs:** a combinação pode surpreender:

```java
// Qual overload chama?
List.of(1, 2, 3);           // List.of(E... elements) — autoboxing: Integer[]
// Mas:
int[] arr = {1, 2, 3};
List.of(arr);               // NÃO desempacota — passa List<int[]> com 1 elemento!
                             // ver Armadilhas abaixo
```

---

### Arrays vs `List`

| Aspecto | Array (`T[]`) | `List<T>` |
|---|---|---|
| Tamanho | Fixo em criação | Dinâmico (`ArrayList`, `LinkedList`) |
| Primitivos | Suportados (`int[]`) | Não — precisa wrapper (`List<Integer>`) |
| Tipo genérico | Não — `List<String>[]` é problemático | Sim — `List<List<String>>` funciona |
| Performance | Melhor para acesso por índice e primitivos | Overhead de objeto + boxing para primitivos |
| Covariância | Covariante: `String[]` é `Object[]` | Invariante: `List<String>` não é `List<Object>` |
| API | Mínima (`length`, for-each) | Rica (`add`, `remove`, `stream`, `sort`) |

**Covariância de array vs invariância de generics:** arrays são covariantes por design histórico — `String[]` pode ser atribuído a `Object[]`. Isso permite código polimórfico com arrays, mas abre espaço para `ArrayStoreException` em runtime. Generics, por outro lado, são invariantes por segurança de tipo.

```java
String[] strings = new String[3];
Object[] objects = strings;         // OK em compile-time — covariância
objects[0] = 42;                    // ArrayStoreException em runtime!
                                     // o array real é String[], não aceita Integer

// Com List, o compilador bloqueia no compile-time:
List<String> listaStrings = new ArrayList<>();
List<Object> listaObjetos = listaStrings; // ERRO de compilação — invariância
```

**Quando usar array:** processamento numérico intensivo com primitivos (sem boxing), interoperabilidade com APIs que exigem array, tamanho conhecido e fixo.

**Quando usar `List`:** tamanho dinâmico, necessidade de API rica, uso como parâmetro genérico.

## Na prática

**Varargs em API própria:**

```java
// API de log com varargs — prática comum
public void registrar(String nivel, String mensagem, Object... parametros) {
    String msg = String.format(mensagem, parametros);
    System.out.printf("[%s] %s%n", nivel, msg);
}

registrar("INFO", "Usuário %s fez login às %s", "joao", "14:30");
registrar("ERROR", "Falha no módulo %s", "pagamento");
registrar("DEBUG", "Aplicação iniciada");   // sem parâmetros extras — OK
```

**Conversão array ↔ List:**

```java
// Array → List (atenção: tamanho fixo!)
String[] arr = {"a", "b", "c"};
List<String> listaFixa = Arrays.asList(arr);  // List de tamanho fixo
List<String> listaMutavel = new ArrayList<>(Arrays.asList(arr)); // mutável

// Java 9+: List imutável diretamente
List<String> imutavel = List.of("a", "b", "c");

// List → Array
String[] de_volta = listaFixa.toArray(new String[0]);
// new String[0] é o padrão idiomático — JVM otimiza o tamanho automaticamente

// Stream → Array
int[] quadrados = IntStream.range(1, 6)
    .map(n -> n * n)
    .toArray();   // [1, 4, 9, 16, 25]
```

## Armadilhas

### (1) Varargs + generics = heap pollution

**O problema:** quando um método varargs tem parâmetro de tipo parametrizado (ex.: `List<String>...`), o compilador converte para `List[]` — apagando o parâmetro de tipo por erasure. Isso permite atribuir um tipo incompatível ao array em runtime, causando `ClassCastException` inesperada em ponto distante do código.

```java
// Método "armadilhado"
static void metodoFalho(List<String>... listas) {
    Object[] array = listas;              // válido em compile-time (covariância)
    array[0] = Arrays.asList(42);         // List<Integer> entra onde se esperava List<String>
    String s = listas[0].get(0);          // ClassCastException aqui — distante do problema
}
```

O compilador emite: `warning: [unchecked] Possible heap pollution from parameterized vararg type List<String>`.

**Fix — `@SafeVarargs`:** se o corpo do método é seguro (não armazena nada no array varargs, não expõe a referência), anote com `@SafeVarargs` para suprimir o warning no *call site* também. Disponível desde Java 7.

```java
@SafeVarargs
static <T> List<T> combinar(List<T>... listas) {
    List<T> resultado = new ArrayList<>();
    for (List<T> lista : listas) {
        resultado.addAll(lista);   // só lê — não modifica o array varargs
    }
    return resultado;
}
// Chamada sem warning:
List<String> tudo = combinar(List.of("a"), List.of("b", "c"));
```

`@SafeVarargs` pode ser aplicada apenas a métodos `static`, `final` ou construtores (Java 7–8) — e a métodos de instância não-overridable (Java 9+, com `private` também permitido).

`@SuppressWarnings({"unchecked","varargs"})` silencia o warning apenas na declaração, não nos call sites — é a alternativa menos desejável.

---

### (2) `Arrays.asList()` retorna lista de tamanho fixo

**O problema:** `Arrays.asList(T... a)` retorna uma implementação interna de `List` que é **backed by the array** — qualquer `set()` reflete no array original, mas `add()` e `remove()` lançam `UnsupportedOperationException` porque o tamanho não pode mudar.

```java
String[] arr = {"a", "b", "c"};
List<String> lista = Arrays.asList(arr);

lista.set(0, "X");      // OK — modifica arr[0] também
lista.add("d");          // UnsupportedOperationException em runtime!
lista.remove(0);         // UnsupportedOperationException em runtime!

// O erro é silencioso em compile-time — List<String> tem add() na interface
```

**Fix:** se precisar de lista mutável, envolva em `new ArrayList<>()`:

```java
List<String> mutavel = new ArrayList<>(Arrays.asList(arr));
mutavel.add("d");    // OK

// Ou, para lista imutável explícita (Java 9+):
List<String> imutavel = List.of("a", "b", "c");
// List.of lança UnsupportedOperationException em set/add/remove — mas é intencional e documentado
```

---

### (3) `Arrays.asList(intArray)` retorna `List<int[]>` — não `List<Integer>`

**O problema:** varargs de `Arrays.asList` é `T... a`. Como `int` não é um tipo de referência, o compilador não pode usar `int` como `T`. Em vez de fazer boxing elemento-a-elemento, ele trata o `int[]` inteiro como um único elemento do tipo `T = int[]`.

```java
int[] primitivos = {1, 2, 3};
List<int[]> lista = Arrays.asList(primitivos);  // List com 1 elemento: o próprio array!
System.out.println(lista.size());               // 1 — não 3!

// Fix 1: usar Integer[]
Integer[] boxed = {1, 2, 3};
List<Integer> listaCorreta = Arrays.asList(boxed);   // 3 elementos

// Fix 2: stream
List<Integer> viaStream = Arrays.stream(primitivos).boxed().collect(Collectors.toList());

// Fix 3: List.of não tem esse problema (também não aceita int[] como varargs)
```

## Em entrevista

### Frase pronta (inglês)

> "Arrays in Java are fixed-size, type-homogeneous containers that live on the heap; the key trade-off against `List` is that arrays support primitives natively — avoiding boxing overhead — but lose the rich `Collection` API and cannot be used as generic type parameters safely, because array covariance (`String[]` assignable to `Object[]`) breaks type safety at runtime with `ArrayStoreException`, whereas generics are invariant and catch the same mistake at compile time. Varargs is syntactic sugar that the compiler desugars into an array, which makes APIs like `printf` and `List.of` ergonomic, but combining varargs with generic parameterized types causes heap pollution — the compiler erases the type parameter to `Object[]`, allowing a `List<Integer>` to be stored where `List<String>` is expected, and the `ClassCastException` surfaces far from the offending line; the fix is to annotate safe implementations with `@SafeVarargs`. A third common caveat is that `Arrays.asList()` returns a fixed-size list backed by the original array, so calling `add()` or `remove()` throws `UnsupportedOperationException` at runtime — wrapping in `new ArrayList<>()` or switching to `List.of()` are the idiomatic solutions depending on whether mutability is needed."

### Vocabulário

| Termo PT | Termo EN |
|---|---|
| array de tamanho fixo | fixed-size array |
| array denteado / irregular | jagged array |
| argumentos de comprimento variável | varargs / variable-length arguments |
| desaçucaramento / expansão pelo compilador | desugaring |
| poluição do heap | heap pollution |
| covariância de array | array covariance |
| invariância de generics | generic invariance |
| exceção de armazenamento em array | `ArrayStoreException` |
| lista de tamanho fixo | fixed-size list |
| boxing de primitivos | primitive boxing / autoboxing |
| cópia rasa | shallow copy |
| busca binária | binary search |

## Veja também

- [[02 - Tipos, variáveis e operadores]]
- [[12 - Generics em profundidade]]
- [[03-Dominios/Tecnologia/Java/Linguagem e sintaxe moderna/index|MOC do galho]]
- [[03-Dominios/Tecnologia/Java/index|Trilha Java]]
- [[Java Fundamentals]]

## Referências

- [Arrays (java.util) — Java SE 21 API Docs (Oracle)](https://docs.oracle.com/en/java/javase/21/docs/api/java.base/java/util/Arrays.html)
- [Non-Reifiable Types and Heap Pollution — The Java Tutorials (Oracle)](https://docs.oracle.com/javase/tutorial/java/generics/nonReifiableVarargsType.html)
- [Arrays — The Java Tutorials (Oracle)](https://docs.oracle.com/javase/tutorial/java/nutsandbolts/arrays.html)
- [Varargs — The Java Tutorials (Oracle)](https://docs.oracle.com/javase/tutorial/java/javaOO/arguments.html#varargs)
- [JDK 21 Documentation — Oracle](https://docs.oracle.com/en/java/javase/21/)
