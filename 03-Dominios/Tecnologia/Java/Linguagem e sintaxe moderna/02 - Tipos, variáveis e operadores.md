---
title: "Tipos, variáveis e operadores"
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
  - tipos
  - operadores
aliases:
  - Tipos primitivos
  - var
---

# Tipos, variáveis e operadores

> [!abstract] TL;DR
> Java tem **8 tipos primitivos** (armazenados direto na stack) e **tipos de referência** (objetos no heap). **Autoboxing** converte entre os dois automaticamente, mas tem custo de alocação em hot paths. A palavra-chave **`var`** (Java 10+) permite inferência de tipo local sem abrir mão da tipagem estática. A armadilha mais clássica do dia-a-dia: usar **`==`** quando se quer comparar valor — `==` compara referência; **`.equals()`** compara conteúdo.

## O que é

Em Java, todo valor pertence a uma de duas categorias:

**Tipos primitivos** — os 8 tipos nativos da linguagem. Armazenam o valor diretamente na memória (stack, para variáveis locais; campo do objeto, para fields). Não são objetos: não têm métodos, não podem ser `null`, não podem ser usados como parâmetro genérico (`List<int>` é inválido).

**Tipos de referência** — tudo que é objeto, incluindo arrays, Strings, e as classes wrapper (`Integer`, `Double` etc.). Uma variável de tipo de referência armazena um **ponteiro** (endereço de memória) para o objeto no heap, não o objeto em si. Isso tem consequências diretas para igualdade (`==` compara ponteiros, não valores) e para o custo de alocação.

A distinção primitivo/referência é o pano de fundo de várias armadilhas clássicas de Java.

## Como funciona

### Primitivos e wrappers

Os 8 tipos primitivos e seus correspondentes wrappers:

| Primitivo | Tamanho | Range (aproximado)   | Wrapper     |
|-----------|---------|----------------------|-------------|
| `byte`    | 8 bits  | -128 a 127           | `Byte`      |
| `short`   | 16 bits | -32.768 a 32.767     | `Short`     |
| `int`     | 32 bits | -2.147.483.648 a 2.147.483.647 | `Integer` |
| `long`    | 64 bits | ±9,2 × 10¹⁸          | `Long`      |
| `float`   | 32 bits | ±3,4 × 10³⁸ (IEEE 754) | `Float`  |
| `double`  | 64 bits | ±1,7 × 10³⁰⁸ (IEEE 754) | `Double` |
| `char`    | 16 bits | '\u0000' a '\uffff' (Unicode BMP) | `Character` |
| `boolean` | 1 bit¹  | `true` / `false`     | `Boolean`   |

> ¹ O tamanho de `boolean` em memória é definido pela JVM — a JLS não especifica um tamanho exato; na prática HotSpot usa 1 byte.

**Autoboxing e unboxing** são conversões automáticas que o compilador Java insere. Quando um `int` é atribuído a um `Integer` (ou passado para um método que espera `Integer`), o compilador gera `Integer.valueOf(i)`. No sentido inverso, quando um `Integer` é usado onde se espera `int`, o compilador gera `.intValue()`.

```java
Integer a = 42;        // autoboxing: compilador gera Integer.valueOf(42)
int b = a;             // unboxing:   compilador gera a.intValue()

List<Integer> lista = new ArrayList<>();
lista.add(7);          // autoboxing automático: Integer.valueOf(7)
```

**Cache do Integer:** a JLS garante que `Integer.valueOf(n)` retorna o **mesmo objeto** para valores entre **-128 e 127** (inclusive). Fora dessa faixa, cada chamada pode criar um objeto novo. Isso é especificado na seção §5.1.7 da Java Language Specification para `int`, `long`, `boolean`, `byte`, e `char` (até `'\u007f'`).

```java
Integer x = 100;
Integer y = 100;
System.out.println(x == y);  // true  — mesmo objeto (cache)

Integer p = 200;
Integer q = 200;
System.out.println(p == q);  // false — objetos distintos (fora do cache)
System.out.println(p.equals(q)); // true — mesmo valor
```

**Custo do autoboxing:** cada `Integer.valueOf(n)` fora do cache aloca um novo objeto no heap e pressiona o garbage collector. Em código de caminho quente (hot path), esse custo pode se acumular significativamente — ver a armadilha **(2) Autoboxing em loop quente** abaixo.

---

### Casting e promoção numérica

**Widening (promoção implícita):** Java promove automaticamente um tipo para um tipo maior, sem risco de perda de dados. A cadeia é: `byte` → `short` → `int` → `long` → `float` → `double`.

```java
int n = 1_000;
long grande = n;      // widening implícito: int → long
double d = grande;    // widening implícito: long → double
```

**Narrowing (estreitamento explícito):** o inverso exige cast manual. O programador assume a responsabilidade por possível perda de dados.

```java
double pi = 3.14159;
int truncado = (int) pi;   // 3 — trunca (não arredonda)

int grande = 300;
byte pequeno = (byte) grande; // overflow silencioso! resultado: 44
                               // 300 em binário: 0001_0010_1100 → byte pega só os 8 bits baixos
```

**Overflow:** tipos inteiros em Java têm overflow silencioso — sem exceção, sem aviso. `Integer.MAX_VALUE + 1` vira `Integer.MIN_VALUE`.

```java
int max = Integer.MAX_VALUE;  // 2_147_483_647
int overflow = max + 1;       // -2_147_483_648 — silencioso!
```

**Promoção em expressões:** operandos `byte` e `short` são promovidos para `int` antes de qualquer operação aritmética. Isso pode surpreender:

```java
byte a = 10;
byte b = 20;
byte soma = a + b;       // erro de compilação: resultado da expressão é int
byte soma = (byte)(a + b); // necessário cast explícito
```

---

### `var` e inferência de tipo local

Introduzida no **Java 10** (JEP 286), `var` permite que o compilador infira o tipo de uma variável local a partir do inicializador. A tipagem continua **estática e forte** — o tipo é resolvido em compile-time, não em runtime.

```java
var lista = new ArrayList<String>();     // tipo inferido: ArrayList<String>
var entrada = new BufferedReader(new FileReader("dados.csv")); // tipo verboso → var clarifica
var i = 0;                               // tipo inferido: int
```

**Quando `var` melhora legibilidade:**
- Tipos longos e óbvios pelo contexto: `var reader = new BufferedReader(...)` — o tipo está evidente
- Variáveis de iteração em for-each: `for (var entry : mapa.entrySet())`

**Quando `var` prejudica legibilidade:**
- Retorno de método não-óbvio: `var resultado = processarDados(input)` — qual é o tipo de `resultado`?
- Literais numéricos: `var n = 10` — é `int`, mas um leitor pode não saber sem verificar

**Restrições de `var`:**
- Não funciona em **campos de classe** (`var` é apenas para variáveis locais)
- Não funciona em **parâmetros de método** nem em **tipos de retorno**
- Não pode ser `null` sem cast explícito: `var x = null` não compila (sem contexto para inferir o tipo)

```java
class Exemplo {
    var campo = "isso não compila";   // erro: var não permitido em campos

    public var metodo() { ... }       // erro: var não permitido em retorno
}
```

---

### Igualdade: `==` vs `equals`

**`==`** compara **referências** (endereços de memória) para tipos de referência. Para primitivos, compara valores diretos.

**`.equals()`** compara **conteúdo**, conforme o contrato implementado pela classe. Para `String`, `Integer`, `List` etc., compara o valor semântico.

```java
String a = new String("hello");
String b = new String("hello");

System.out.println(a == b);       // false — objetos distintos na memória
System.out.println(a.equals(b));  // true  — mesmo conteúdo

// String pool (literais internados automaticamente):
String c = "hello";
String d = "hello";
System.out.println(c == d);       // true — JVM reutiliza o mesmo objeto do pool
                                   // MAS: não confie nisso em código geral
```

A regra prática: **para objetos, sempre use `.equals()` para comparar valor**. Reserve `==` para checar se duas variáveis apontam para o mesmo objeto (identidade), o que raramente é o que se quer.

**Atenção com `null`:** chamar `.equals()` em uma referência `null` lança `NullPointerException`. Padrão seguro: `Objects.equals(a, b)` (retorna `false` se um dos dois for `null`).

---

### Contrato equals/hashCode (introdução)

Em Java, os métodos `equals()` e `hashCode()` formam um **contrato**: se `a.equals(b)` é `true`, então `a.hashCode()` deve ser igual a `b.hashCode()`. Quebrar essa regra causa comportamentos silenciosamente errados em `HashMap`, `HashSet` e qualquer coleção baseada em hash.

Um exemplo clássico: implementar `equals()` sem sobrescrever `hashCode()` faz com que `HashMap.get()` não encontre a chave mesmo quando `equals()` retorna `true` — porque o bucket de hash é calculado com o `hashCode()` padrão da `Object` (baseado em identidade).

O deep dive completo — implementação correta, `Objects.hash()`, e as implicações de herança — está em [[07 - Herança e polimorfismo]].

## Na prática

**Autoboxing em loop quente — custo real:**

```java
// Padrão problemático: autoboxing em cada iteração
List<Integer> acumulador = new ArrayList<>();
for (int i = 0; i < 1_000_000; i++) {
    acumulador.add(i);            // Integer.valueOf(i) para todo i > 127
}                                  // → ~870.000 alocações de objeto Integer

// Alternativa quando o tipo primitivo é suficiente:
int[] acumuladorPrimitivo = new int[1_000_000];
for (int i = 0; i < 1_000_000; i++) {
    acumuladorPrimitivo[i] = i;   // zero alocação
}

// Ou, para acumulação numérica pura, IntStream:
int soma = IntStream.range(0, 1_000_000).sum(); // sem boxing
```

O padrão com `List<Integer>` não é errado para a maioria dos usos. O problema aparece quando o loop está em um hot path e o profiler mostra pressão de GC por alocação excessiva de wrappers.

**`var` legível vs. `var` que ofusca:**

```java
// Legível: tipo óbvio pelo inicializador
var conexao = dataSource.getConnection();           // tipo evidente: Connection
var entries = configuracoes.entrySet();             // Set<Map.Entry<String,String>>

// Ofuscante: tipo não é óbvio sem inspecionar a assinatura do método
var resultado = servico.calcular(parametros);       // qual tipo é resultado?
var dados = repositorio.buscar(filtro);             // Collection? Optional? Object?
```

A heurística prática: se você precisar ir até a declaração do método para saber o tipo inferido, `var` provavelmente está prejudicando a legibilidade nesse ponto.

## Armadilhas

### (1) `==` em wrappers e Strings — o cache do Integer ilude

**O problema:** o cache do `Integer` para valores entre -128 e 127 faz `==` funcionar corretamente para esses valores, criando uma falsa sensação de segurança. Fora da faixa, o comportamento muda silenciosamente.

```java
Integer a = 127;
Integer b = 127;
System.out.println(a == b);  // true  — cache garante mesmo objeto

Integer x = 128;
Integer y = 128;
System.out.println(x == y);  // false — novos objetos, fora do cache
```

O mesmo vale para Strings: literais são internados no String pool e `==` pode retornar `true`, mas `new String("texto")` cria um objeto fora do pool.

**Fix:** sempre use `.equals()` para comparar valor de wrappers e Strings.

```java
Objects.equals(x, y); // null-safe e correto em todos os casos
```

---

### (2) Autoboxing em loop quente

**O problema:** adicionar primitivos a uma `Collection` ou usar wrappers em operações aritméticas dentro de um loop quente aloca um objeto por iteração. Em escala, isso pressiona o GC.

```java
// Problemático em hot path de alta frequência:
Long soma = 0L;
for (long i = 0; i < 10_000_000L; i++) {
    soma += i;  // unboxing de soma + adição + autoboxing do resultado
                // → uma alocação Long por iteração = 10 milhões de objetos
}
```

**Fix:** use o tipo primitivo diretamente. Se precisar de coleção, use arrays primitivos ou `IntStream`/`LongStream`.

```java
long soma = 0L;                         // primitivo: zero alocação
for (long i = 0; i < 10_000_000L; i++) {
    soma += i;
}
```

---

### (3) `var` escondendo o tipo / não funciona em campos

**O problema — ofuscação:** `var` pode ocultar completamente o tipo em contextos onde o leitor não tem como inferir sem consultar a assinatura do método. Isso aumenta a carga cognitiva de manutenção.

```java
// O leitor precisa saber o que calcularTaxa() retorna:
var taxa = servico.calcularTaxa(pedido);
taxa.aplicar(valor);   // o que é taxa? BigDecimal? TaxaDTO? uma lambda?
```

**O problema — compilação:** `var` não é permitido em campos de classe, parâmetros de método ou tipo de retorno. Isso pega quem vem de outras linguagens com inferência mais ampla (Kotlin, Scala).

```java
class Calculadora {
    var fator = 1.5;        // ERRO: variable fator has initializer but used as field
    
    public var calcular(var x) { // ERRO em ambos: parâmetro e retorno
        return x * fator;
    }
}
```

**Fix:** use `var` apenas quando o tipo é óbvio pelo contexto no ponto de leitura. Prefira declaração explícita em campos e em retornos de método não triviais.

## Em entrevista

### Frase pronta (inglês)

> "Autoboxing is Java's automatic conversion between primitive types and their wrapper classes — for instance, `int` to `Integer` — which the compiler inserts as calls to `Integer.valueOf()` and `intValue()`. The trade-off is that each boxing operation outside the cached range (-128 to 127 for `int`) allocates a new object on the heap, which adds GC pressure in tight loops; the fix is to work with primitives directly or use primitive streams like `IntStream`. On the identity-vs-equality front, the Integer cache is particularly tricky: `==` works correctly for cached values but silently fails for values above 127, which is why the rule is to always use `.equals()` — or `Objects.equals()` for null safety — when comparing wrapper types or Strings."

Use essa resposta para perguntas como *"What is autoboxing?"*, *"When would `==` fail on integers?"* ou *"What are the performance implications of using wrapper types?"*.

### Vocabulário

| Termo PT                     | Termo EN                                       |
|------------------------------|------------------------------------------------|
| tipo primitivo               | primitive type                                 |
| tipo de referência / objeto  | reference type / object type                  |
| encapsulamento automático    | autoboxing                                     |
| desencapsulamento automático | unboxing                                       |
| classe wrapper               | wrapper class                                  |
| promoção de tipo (implícita) | widening conversion / numeric promotion        |
| estreitamento de tipo        | narrowing conversion                           |
| transbordamento / estouro    | overflow (integer overflow)                    |
| inferência de tipo local     | local variable type inference (`var`)          |
| igualdade por referência     | reference equality (`==`)                      |
| igualdade por valor          | value equality (`.equals()`)                   |
| cache de inteiros            | Integer cache / Integer pool                   |
| pool de strings              | String pool / String intern pool               |
| contrato equals/hashCode     | equals/hashCode contract                       |

## Veja também

- [[01 - O modelo da linguagem Java]]
- [[07 - Herança e polimorfismo]]
- [[05 - Arrays e varargs]]
- [[03-Dominios/Tecnologia/Java/Linguagem e sintaxe moderna/index|MOC do galho]]
- [[03-Dominios/Tecnologia/Java/index|Trilha Java]]
- [[Java Fundamentals]]

## Referências

- [Primitive Data Types — The Java Tutorials (Oracle)](https://docs.oracle.com/javase/tutorial/java/nutsandbolts/datatypes.html)
- [Autoboxing and Unboxing — The Java Tutorials (Oracle)](https://docs.oracle.com/javase/tutorial/java/data/autoboxing.html)
- [JLS §5.1.7 Boxing Conversion — Java Language Specification SE 21](https://docs.oracle.com/javase/specs/jls/se21/html/jls-5.html#jls-5.1.7)
- [JEP 286: Local-Variable Type Inference — openjdk.org](https://openjdk.org/jeps/286)
- [JDK 21 Documentation — Oracle](https://docs.oracle.com/en/java/javase/21/)
