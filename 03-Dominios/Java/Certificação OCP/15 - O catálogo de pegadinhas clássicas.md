---
title: "O catálogo de pegadinhas clássicas"
created: 2026-06-13
updated: 2026-06-13
type: concept
status: seedling
publish: true
fase: estrategia
tags:
  - java
  - certificacao-ocp
  - estrategia
aliases:
  - "Pegadinhas OCP"
  - "Gotchas Java"
  - "Armadilhas da prova OCP"
---

# O catálogo de pegadinhas clássicas

> [!abstract] TL;DR
> Esta nota vale ouro. É o catálogo das armadilhas recorrentes que a prova OCP adora — aquelas em que quem programa Java há anos cai justamente por excesso de confiança. Você "sabe" o resultado de cabeça, marca a alternativa óbvia, e a banca contava exatamente com isso. Cada pegadinha aqui tem um snippet curto, o resultado real (com o porquê) e o domínio onde a mecânica de verdade mora, pra você revisar fundo se precisar.

## Como usar este catálogo

Revise esta nota inteira na véspera da prova, depois de já ter rodado a [[03-Dominios/Java/Certificação OCP/04 - O mapa objetivo → galho — revisar a trilha pra prova|mapa objetivo → galho]]. A diferença entre uma pegadinha e um conceito é o ângulo: o conceito você estuda uma vez e segue; a pegadinha você precisa *re-treinar o reflexo*, porque seu instinto de programador experiente aponta pra resposta errada. Cada subseção é proposital e curta — leia o snippet, cubra a explicação com a mão, responda mentalmente, e só então confira. Se errar (ou acertar pelo motivo errado), siga o ponteiro do domínio indicado e revise a mecânica de raiz antes de voltar.

A regra de ouro que atravessa metade deste catálogo: **`==` compara identidade de referência, `equals` compara conteúdo.** Boa parte das pegadinhas de tipos e de coleções é só a banca explorando a tentação de usar `==` onde você deveria usar `equals`.

## Tipos e valores

### Integer cache (-128..127)

```java
Integer a = 127;
Integer b = 127;
System.out.println(a == b);   // true  — vêm do cache compartilhado

Integer c = 128;
Integer d = 128;
System.out.println(c == d);   // false — fora do cache, objetos distintos

System.out.println(c.equals(d)); // true — equals SEMPRE compara valor
```

A JVM mantém um cache de objetos `Integer` para a faixa `-128..127` (autoboxing reaproveita instâncias). Dentro da faixa, `==` parece funcionar; um número acima e a ilusão quebra. A lição não é decorar a faixa — é **nunca comparar wrappers com `==`**. Use `equals`. A mesma armadilha vale para `Long`, `Short`, `Byte` e `Character`.

### String pool vs `new String` / `intern`

```java
String s1 = "hello";
String s2 = "hello";
String s3 = new String("hello");

System.out.println(s1 == s2);          // true  — ambos vêm do pool
System.out.println(s1 == s3);          // false — new String() força objeto novo no heap
System.out.println(s1.equals(s3));     // true  — conteúdo igual
System.out.println(s1 == s3.intern()); // true  — intern() devolve a instância do pool
```

Literais de String vivem no *pool* e são deduplicados — por isso `s1 == s2`. Mas `new String("hello")` deliberadamente cria um objeto novo, fora do pool, então `s1 == s3` é `false`. `intern()` consulta o pool e devolve a referência canônica. Mesma moral do Integer cache: para conteúdo, sempre `equals`.

### `var` com tipos ambíguos (e o que `var` NÃO pode)

```java
var list = new ArrayList<>(); // inferido como ArrayList<Object>, não <String>!
list.add("hello");
list.add(42);                  // compila — porque é List<Object>
```

O diamante vazio `<>` num `var` infere `Object`, não o tipo que você "queria". O `var` só conhece o que está do lado direito do `=`.

E `var` **não pode** aparecer em vários lugares que a prova adora testar:

```java
// var x;                   // ERRO — sem inicializador, nada a inferir
// var y = null;            // ERRO — null não tem tipo
// var z = () -> 1;         // ERRO — lambda precisa de target type explícito
// var a = new int[]{1,2};  // OK, mas: var arr[] = ...  // ERRO — notação de array
// var method() { }         // ERRO — não serve como tipo de retorno
// public var field;        // ERRO — não serve em campo de classe
```

`var` é só inferência local de variável (dentro de método, `for`, `try-with-resources`). Onde o compilador não tem uma expressão concreta pra inferir, ele recusa.

### Autoboxing com `null` → NPE

```java
Integer i = null;
int j = i;   // NullPointerException em runtime!
```

Atribuir um `Integer` a um `int` dispara *unboxing* implícito — o compilador insere um `i.intValue()`. Se a referência for `null`, isso é um NPE silencioso, sem cast à vista. A prova esconde isso dentro de expressões maiores (ternários, somas com wrappers, `Map.get` que retorna `null`).

### `final` com objeto mutável (referência final ≠ conteúdo imutável)

```java
final List<String> list = new ArrayList<>();
list.add("hello");          // OK — só a REFERÊNCIA é final
// list = new ArrayList<>(); // ERRO — não pode reapontar a referência
```

`final` congela a *variável*, não o *objeto*. Você não pode reatribuir `list`, mas pode mutar à vontade o conteúdo apontado. A banca usa isso pra confundir `final` com imutabilidade.

### Inicialização de arrays (0 / null / false)

```java
int[]     a = new int[5];     // [0, 0, 0, 0, 0]
Integer[] b = new Integer[5]; // [null, null, null, null, null]
boolean[] c = new boolean[5]; // [false, false, false, false, false]
String[]  d = new String[5];  // [null, null, null, null, null]
double[]  e = new double[5];  // [0.0, 0.0, 0.0, 0.0, 0.0]
```

`new T[n]` zera tudo com o valor default de `T`: numéricos viram `0`/`0.0`, `boolean` vira `false`, **referências** (incluindo wrappers como `Integer`) viram `null`. A pegadinha clássica: assumir que `Integer[]` começa com zeros — não, começa com `null`, e iterar somando dá NPE por unboxing.

## Orientação a objetos

### Override vs overload com autoboxing

```java
class Handler {
    void handle(int x)     { System.out.println("int"); }
    void handle(Integer x) { System.out.println("Integer"); }
    void handle(Object x)  { System.out.println("Object"); }
}

new Handler().handle(1);           // "int"     — match exato vence
new Handler().handle((Integer) 1); // "Integer"
new Handler().handle("str");       // "Object"
```

Quando há sobrecargas, o compilador escolhe **em compile-time** seguindo uma ordem rígida de preferência:

> [!info] Ordem de resolução de sobrecarga
> 1. **Match exato** (tipo idêntico)
> 2. **Widening** (alargamento primitivo: `int` → `long` → `double`)
> 3. **Autoboxing** (`int` → `Integer`)
> 4. **Varargs** (`int...`) — sempre o último recurso

O compilador *desce* essa escada e para no primeiro nível que tem candidato. Por isso `handle(1)` chama `int` (match exato), e não `Integer` nem `Object`, mesmo que ambos sirvam. Veja o domínio em [[03-Dominios/Java/Certificação OCP/07 - Domínio 3 — Orientação a objetos|Domínio 3 — Orientação a objetos]].

### Static method hiding (resolvido em compile-time pelo tipo declarado)

```java
class Parent {
    static void foo() { System.out.println("Parent"); }
}
class Child extends Parent {
    static void foo() { System.out.println("Child"); }
}

Parent p = new Child();
p.foo();  // "Parent" — NÃO é override; é hiding, resolvido pelo TIPO declarado
```

Métodos `static` **não sofrem override** — eles sofrem *hiding* (ocultação). Não há despacho dinâmico: o método chamado é decidido em compile-time pelo **tipo declarado** da variável (`Parent`), não pelo objeto real (`Child`). Compare com método de instância, que faria o oposto (chamaria `Child`). Essa inversão é uma das pegadinhas favoritas da prova.

### Enum constructor é sempre `private`

```java
enum Status {
    ACTIVE("active"),
    INACTIVE("inactive");

    private final String label;

    Status(String label) {   // implicitamente private
        this.label = label;
    }
}
```

O construtor de um `enum` é **implicitamente `private`** e **não pode** ser declarado `public` nem `protected` — tentar isso é erro de compilação. Faz sentido: as instâncias de um enum são fixas e criadas só pela própria declaração; ninguém de fora pode instanciar. A prova mostra um construtor de enum marcado `public` e pergunta o resultado (resposta: não compila).

### Generics e type erasure (`getClass()` é igual)

```java
List<String>  stringList = new ArrayList<>();
List<Integer> intList    = new ArrayList<>();

System.out.println(stringList.getClass() == intList.getClass()); // true!
```

Generics existem só em compile-time. Em runtime, `List<String>` e `List<Integer>` são ambos apenas `ArrayList` — o tipo paramétrico foi *apagado* (type erasure). Por isso `getClass()` devolve a mesma `Class` para os dois, você não pode fazer `new T[]`, e não dá pra testar `instanceof List<String>`. Isso vive em [[03-Dominios/Java/Certificação OCP/07 - Domínio 3 — Orientação a objetos|Domínio 3 — Orientação a objetos]].

## Fluxo e exceções

### `try`/`finally` com `return` (o `finally` vence)

```java
int method() {
    try {
        return 1;
    } finally {
        return 2;   // sobrescreve o return do try
    }
}
// retorna 2
```

Um `return` (ou `throw`) dentro de `finally` **sobrepõe** qualquer `return` ou exceção pendente do `try`/`catch`. O `try` "ia retornar 1", mas o `finally` executa antes de a pilha desenrolar e impõe o `2` — inclusive engolindo exceções que estavam a caminho. É código ruim na prática (vários linters acusam), mas a prova pergunta exatamente o valor de retorno.

### `try-with-resources`: ordem reversa de `close()`

```java
try (var a = new ResourceA();
     var b = new ResourceB();
     var c = new ResourceC()) {
    // uso
}
// Ordem de fechamento: c → b → a (reversa da declaração)
```

Os recursos de um `try-with-resources` são fechados na **ordem inversa** em que foram abertos — como uma pilha. O último aberto (`c`) é o primeiro a fechar. Isso garante que um recurso que depende de outro (ex.: um `Writer` sobre um `Stream`) feche antes da sua dependência. A prova testa numerando os recursos e perguntando a sequência impressa pelos `close()`.

### Switch `case:` (fall-through) vs `case ->` (sem fall-through)

O switch **statement** com dois-pontos sofre *fall-through*: sem `break`, a execução escorre pros próximos cases.

```java
int x = 2;
switch (x) {
    case 1: System.out.println("1");
    case 2: System.out.println("2");
    case 3: System.out.println("3");
    default: System.out.println("default");
}
// Imprime: 2, 3, default  — escorreu do case 2 até o fim
```

O switch **expression** com seta (`->`) **não** tem fall-through: executa só o ramo casado.

```java
switch (x) {
    case 1 -> System.out.println("1");
    case 2 -> System.out.println("2");
    case 3 -> System.out.println("3");
    default -> System.out.println("default");
}
// Imprime apenas: 2
```

A pegadinha é misturar as sintaxes mentalmente e esquecer que os dois-pontos *escorrem*. Sempre que ver `case X:` sem `break`, conte os prints até o próximo `break` (ou o fim do switch).

## Coleções e streams

### `Arrays.asList` tem tamanho fixo

```java
List<String> list = Arrays.asList("a", "b", "c");
list.set(0, "z");   // OK — pode trocar elementos existentes
list.add("d");      // UnsupportedOperationException — tamanho é fixo!
list.remove("a");   // UnsupportedOperationException
```

`Arrays.asList` devolve uma `List` de **tamanho fixo**, apoiada no array original. Você pode reordenar e substituir (`set`), mas **não** adicionar nem remover — isso lança `UnsupportedOperationException`. Pra ter uma lista mutável de verdade, embrulhe: `new ArrayList<>(Arrays.asList(...))`.

### Coleções imutáveis: *view* vs cópia

```java
List<String> list  = new ArrayList<>(List.of("a", "b"));
List<String> view  = Collections.unmodifiableList(list); // VIEW da original
List<String> copy  = List.copyOf(list);                  // CÓPIA independente

list.add("c");

System.out.println(view.size()); // 3 — a view enxerga a mudança na original!
System.out.println(copy.size()); // 2 — a cópia ficou congelada
```

`Collections.unmodifiableList` cria uma **view** somente-leitura: você não consegue modificá-la *pela view*, mas ela continua refletindo mudanças feitas na lista subjacente. Já `List.copyOf` faz uma **cópia** genuína e independente. A prova explora a diferença mudando a lista original depois de criar as duas e perguntando os tamanhos.

### Contrato `equals` / `hashCode` (sem `hashCode`, `HashSet`/`HashMap` quebram)

```java
class Person {
    String name;
    public boolean equals(Object o) { /* compara name */ }
    // FALTA hashCode() — BUG silencioso!
}

Set<Person> set = new HashSet<>();
set.add(new Person("Maria"));
set.contains(new Person("Maria")); // false! — hashCode default é por identidade
```

> [!warning] A regra: se você sobrescreve `equals`, **tem** que sobrescrever `hashCode`.
> O contrato exige que objetos iguais por `equals` tenham o mesmo `hashCode`. Estruturas baseadas em hash (`HashSet`, `HashMap`, `HashTable`) primeiro localizam o *bucket* pelo `hashCode` e só depois comparam com `equals`. Se o `hashCode` continua o default (baseado em identidade do objeto), os dois `Person("Maria")` caem em buckets diferentes e nunca se encontram — `contains` devolve `false` mesmo com `equals` "correto".

### Stream consumido 2x (`IllegalStateException`)

```java
Stream<String> stream = Stream.of("a", "b", "c");
stream.forEach(System.out::println); // ok
stream.forEach(System.out::println); // IllegalStateException — stream has already been operated upon or closed
```

Um `Stream` é de **uso único**. Depois de uma operação terminal (`forEach`, `collect`, `count`, `reduce`...), ele está consumido e qualquer nova operação lança `IllegalStateException`. Diferente de uma `Collection`, que você itera quantas vezes quiser. Se precisa reprocessar, recrie o stream (ou guarde o resultado numa coleção). A prova esconde a segunda operação terminal algumas linhas abaixo.

### Effectively final em lambdas

```java
int x = 10;
Runnable r = () -> System.out.println(x); // OK — x é effectively final
// x = 20;   // se descomentar, ERRO de compilação no lambda acima
```

Um lambda (ou classe anônima) só pode capturar variáveis locais que sejam `final` ou **effectively final** — isto é, atribuídas uma única vez e nunca reatribuídas, mesmo sem a palavra `final`. Basta uma reatribuição em qualquer ponto do método pra que a variável deixe de ser effectively final e o lambda pare de compilar. Note que a *captura* é por valor; mutar o conteúdo de um objeto capturado é permitido (mesma lógica do `final` com objeto mutável, lá em cima).

## Veja também

- [[03-Dominios/Java/Certificação OCP/04 - O mapa objetivo → galho — revisar a trilha pra prova|O mapa objetivo → galho]]
- [[03-Dominios/Java/Certificação OCP/07 - Domínio 3 — Orientação a objetos|Domínio 3 — Orientação a objetos]]
- [[03-Dominios/Java/Certificação OCP/16 - Estratégia de estudo e recursos|Estratégia de estudo e recursos]]
- [[03-Dominios/Java/Certificação OCP/index|Certificação OCP (MOC do galho)]]

## Referências

- [Enthuware — OCP Java 21 Exam Syllabus & Resources](https://enthuware.com/oca-ocp-java-certification-resources/290-ocp-java-21-exam-syllabus)
