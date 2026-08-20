---
title: "Comparable e Comparator"
created: 2026-06-04
updated: 2026-06-04
type: concept
progress: backlog
status: seedling
publish: true
fase: Adepto
tags:
  - java
  - collections
  - adepto
  - comparator
  - ordenacao
aliases:
  - Comparable
  - Comparator
  - Ordenação
---

# Comparable e Comparator

> [!abstract] TL;DR
> **`Comparable`** define a **ordem natural** de uma classe — implementado dentro dela, via `compareTo`. **`Comparator`** é uma estratégia de ordenação **externa e plugável** — construída fora da classe, composta com combinadores como `comparing`, `thenComparing`, `reversed`, `nullsFirst` e `nullsLast`. Use `Comparable` para a ordenação canônica (ex.: preço crescente de `Product`); use `Comparator` para ordenações alternativas ou quando a classe não é sua. O contrato central: `compareTo` e `compare` retornam negativo (menor), zero (igual) ou positivo (maior). A violação do contrato de consistência com `equals` causa comportamentos silenciosamente errados em `TreeSet`, `TreeMap` e outros sorted collections.

## O que é

`Comparable<T>` é uma interface da `java.lang` que faz a própria classe declarar sua **ordem natural** — a ordenação canônica usada por padrão ao inserir em `SortedSet`, `SortedMap` ou ao chamar `Collections.sort` / `Arrays.sort` sem argumento adicional.

```java
public interface Comparable<T> {
    int compareTo(T o);
}
```

`Comparator<T>` é uma **interface funcional** de `java.util` que encapsula uma estratégia de ordenação **externa** à classe comparada. Por ser `@FunctionalInterface`, aceita lambdas e method references. Seu método abstrato é:

```java
@FunctionalInterface
public interface Comparator<T> {
    int compare(T o1, T o2);
    // + dezenas de métodos default e estáticos (combinadores)
}
```

A distinção central:

| Aspecto | `Comparable` | `Comparator` |
|---|---|---|
| Onde vive | Dentro da classe | Fora da classe |
| Quantas ordenações | Uma (natural) | Ilimitadas |
| Modifica a classe | Sim | Não |
| Uso típico | `sort(list)` sem argumento | `sort(list, comparator)` |
| Interface funcional | Não | Sim |

## Por que importa

Ordenação correta é crítica em toda coleção sorted (`TreeSet`, `TreeMap`, `PriorityQueue`) e em pipelines de `Stream`. Um `Comparator` mal construído pode produzir ordenações inconsistentes que violam silenciosamente o contrato de equals — levando `TreeSet` a "perder" elementos que, para o `equals`, são distintos, ou a "fundir" elementos que deveriam coexistir.

Saber compor `Comparator` com os combinadores da API é um requisito recorrente em entrevistas sênior, onde o código idiomático substitui loops explícitos e implementações manuais de `compare`.

## Como funciona

### `Comparable<T>.compareTo` — contrato -/0/+ e consistência com equals

`compareTo(T o)` retorna:
- **negativo** → `this` é menor que `o`
- **zero** → `this` é igual a `o` (para fins de ordenação)
- **positivo** → `this` é maior que `o`

O contrato exige três propriedades:

1. **Anti-simetria**: `signum(x.compareTo(y)) == -signum(y.compareTo(x))`
2. **Transitividade**: se `x > y` e `y > z`, então `x > z`
3. **Consistência de zero**: `x.compareTo(y) == 0` implica que `x` e `z` têm a mesma relação que `y` e `z` para todo `z`

**Consistência com `equals`** — fortemente recomendada, não obrigatória:

```
(x.compareTo(y) == 0)  ==  (x.equals(y))
```

Quando a consistência é violada, `TreeSet` e `TreeMap` usam `compareTo` para decidir unicidade — o que faz com que dois objetos que `equals` considera distintos sejam tratados como o mesmo elemento. `BigDecimal` é o exemplo canônico da API: `new BigDecimal("4.0").compareTo(new BigDecimal("4.00")) == 0`, mas `equals` retorna `false`.

**Implementação canônica** — compare campo a campo, delegando para o tipo primitivo ou para `Comparable` existente:

```java
public class Product implements Comparable<Product> {
    private final String name;
    private final BigDecimal price;

    @Override
    public int compareTo(Product other) {
        // delega para BigDecimal.compareTo — preserva consistência com equals do tipo
        return this.price.compareTo(other.price);
    }
}
```

---

### `Comparator` e combinadores — `comparing`, `comparingInt`, `thenComparing`, `reversed`

A API de fábrica e composição torna quase desnecessário escrever lambdas explícitas de comparação:

**`Comparator.comparing(keyExtractor)`** — extrai uma chave `Comparable` e ordena por ela:

```java
// ordena Order pela data de criação (LocalDate implementa Comparable)
Comparator<Order> byDate = Comparator.comparing(Order::getCreatedAt);
```

**`Comparator.comparingInt(keyExtractor)`** — versão especializada para `int`, evitando boxing:

```java
// ordena Order pela quantidade de itens (campo int)
Comparator<Order> byItemCount = Comparator.comparingInt(Order::getItemCount);
```

Versões análogas existem para `long` (`comparingLong`) e `double` (`comparingDouble`).

**`.thenComparing(keyExtractor)`** — desempate lexicográfico: aplica o segundo critério quando o primeiro empata:

```java
// ordena por cliente, e em caso de empate, por valor decrescente
Comparator<Order> byCustomerThenValue =
    Comparator.comparing(Order::getCustomerName)
              .thenComparing(Comparator.comparingInt(Order::getTotalValue).reversed());
```

**`.reversed()`** — inverte a ordem do comparador:

```java
// ordena por valor decrescente
Comparator<Order> byValueDesc = Comparator.comparingInt(Order::getTotalValue).reversed();
```

**`Comparator.naturalOrder()` / `Comparator.reverseOrder()`** — atalhos para a ordem natural e sua inversa em coleções de `Comparable`:

```java
List<String> names = List.of("Carlos", "Ana", "Bruno");
names.stream().sorted(Comparator.reverseOrder()).toList();
// → ["Carlos", "Bruno", "Ana"]
```

---

### Nulos — `nullsFirst` e `nullsLast`

Por padrão, qualquer comparador que tente comparar um valor nulo lançará `NullPointerException`. `nullsFirst` e `nullsLast` envolvem um comparador existente com tratamento de nulo:

```java
// nulls vão para o início; não-nulos são comparados pela ordem natural
Comparator<String> comNulos =
    Comparator.nullsFirst(Comparator.naturalOrder());

// nulls vão para o fim; não-nulos ordenados pelo nome do cliente
Comparator<Order> clienteNuloNoFim =
    Comparator.nullsLast(Comparator.comparing(Order::getCustomerName));
```

Quando ambos os valores são nulos, são considerados iguais entre si. O comparador passado como argumento só é chamado quando ambos são não-nulos.

---

### Ordenar `List` (`sort`) e streams (`sorted`)

**`List.sort(comparator)`** — ordena in-place (algoritmo TimSort, O(n log n), estável):

```java
List<Order> orders = new ArrayList<>(fetchOrders());
orders.sort(Comparator.comparingInt(Order::getTotalValue));
```

**`Stream.sorted(comparator)`** — retorna um stream com elementos em ordem; a lista original não é modificada:

```java
List<Order> ordenados = orders.stream()
    .sorted(Comparator.comparing(Order::getCreatedAt).reversed())
    .toList();
```

**`Collections.sort(list)`** (sem argumento) exige que os elementos implementem `Comparable`. `stream().sorted()` sem argumento também usa a ordem natural.

## Na prática

O cenário mais comum em APIs de domínio: ordenar uma lista de `Order` por valor total decrescente e, em empate, por data de criação crescente.

```java
// hipotético: Order com campos totalValue (int) e createdAt (LocalDate)
List<Order> orders = new ArrayList<>(repository.findAll());

Comparator<Order> byValueDescThenDate =
    Comparator.comparingInt(Order::getTotalValue)
              .reversed()
              .thenComparing(Order::getCreatedAt);

orders.sort(byValueDescThenDate);
```

Versão em stream, sem modificar a lista original:

```java
List<Order> ordenados = orders.stream()
    .sorted(Comparator.comparingInt(Order::getTotalValue)
                      .reversed()
                      .thenComparing(Order::getCreatedAt))
    .toList();
```

Ordena por nome de cliente em ordem reversa (útil para exibição decrescente):

```java
// inversão de Comparator.comparing — não de naturalOrder
Comparator<Order> byCustomerReversed =
    Comparator.comparing(Order::getCustomerName).reversed();

orders.sort(byCustomerReversed);
```

> [!tip] `.reversed()` em comparator composto
> Quando encadeado após `.thenComparing`, `.reversed()` inverte **todo o comparador acumulado**, não apenas o último critério. Para inverter somente um critério específico, envolva-o antes de encadear: `Comparator.comparingInt(Order::getValue).reversed().thenComparing(Order::getDate)` inverte só o valor; `thenComparing` permanece crescente.

## Armadilhas

### (1) Comparator inconsistente com equals — `TreeSet` e `TreeMap` "perdem" elementos

**O problema:** `TreeSet` e `TreeMap` usam `compareTo` (ou o `Comparator` fornecido) para determinar unicidade — não `equals`. Se o comparador considera dois objetos iguais (`compare` retorna 0) mas `equals` os diferencia, o segundo elemento é silenciosamente descartado.

```java
// RUIM — compara só pelo nome; dois produtos com mesmo nome mas preços diferentes
// são tratados como duplicatas no TreeSet
Comparator<Product> byName = Comparator.comparing(Product::getName);

TreeSet<Product> catalog = new TreeSet<>(byName);
catalog.add(new Product("Widget", new BigDecimal("10.00")));
catalog.add(new Product("Widget", new BigDecimal("20.00")));  // silenciosamente ignorado!

System.out.println(catalog.size());  // 1, não 2
```

```java
// FIX — inclui o preço como desempate, tornando o comparador consistente com equals
Comparator<Product> byNameThenPrice =
    Comparator.comparing(Product::getName)
              .thenComparing(Product::getPrice);

TreeSet<Product> catalog = new TreeSet<>(byNameThenPrice);
catalog.add(new Product("Widget", new BigDecimal("10.00")));
catalog.add(new Product("Widget", new BigDecimal("20.00")));

System.out.println(catalog.size());  // 2 — correto
```

> [!warning] Sempre que usar `TreeSet` ou `TreeMap` com `Comparator` customizado, verifique se dois objetos que `equals` distingue também são distinguidos pelo comparador.

---

### (2) `a - b` para comparar inteiros — overflow silencioso

**O problema:** o "atalho" `return a - b` para comparar dois `int` parece funcionar, mas produz resultados errados quando a diferença estoura o intervalo de `int` (overflow de complemento a dois).

```java
// RUIM — overflow: se a = Integer.MIN_VALUE e b = 1, a - b é positivo (errado!)
Comparator<Order> byValue = (o1, o2) -> o1.getTotalValue() - o2.getTotalValue();

// com valores extremos:
int a = Integer.MIN_VALUE;  // -2147483648
int b = 1;
System.out.println(a - b);  // 2147483647 (positivo!) — deveria ser negativo
```

```java
// FIX — use Integer.compare ou comparingInt
Comparator<Order> byValue = Comparator.comparingInt(Order::getTotalValue);

// ou, se precisar de lambda explícita:
Comparator<Order> byValue2 = (o1, o2) -> Integer.compare(o1.getTotalValue(), o2.getTotalValue());
```

O mesmo vale para `long`: use `Long.compare`, não `a - b`.

---

### (3) Campo nulável sem `nullsFirst` / `nullsLast` — NPE em runtime

**O problema:** ao ordenar por um campo que pode ser `null`, qualquer comparador padrão lança `NullPointerException` ao tentar acessar o valor.

```java
// RUIM — Order.getCustomerName() pode retornar null; lança NPE na ordenação
orders.sort(Comparator.comparing(Order::getCustomerName));
// java.lang.NullPointerException em runtime, possivelmente intermitente
```

```java
// FIX — envolva com nullsLast (ou nullsFirst) antes de comparar
orders.sort(
    Comparator.nullsLast(Comparator.comparing(Order::getCustomerName))
);

// ou, para campo aninhado (Customer pode ser null):
orders.sort(
    Comparator.nullsLast(
        Comparator.comparing(
            Order::getCustomerName,
            Comparator.nullsLast(String::compareTo)
        )
    )
);
```

> [!danger] NPEs em comparadores são especialmente traiçoeiros: o stack trace aponta para o `sort` ou `sorted`, não para o campo nulo, dificultando o diagnóstico.

## Em entrevista

### Frase pronta (inglês)

> "`Comparable` is for defining a class's natural ordering from within — it's part of the class contract and implies there is one canonical way to compare instances. `Comparator`, on the other hand, is an external, pluggable strategy that lets you define as many orderings as you need without touching the original class." "The key contract is consistency with `equals`: if `compareTo` returns zero for two objects, they should ideally be `equals` as well. Violating this is legal, but it causes `TreeSet` and `TreeMap` to silently deduplicate elements that `equals` would keep separate." "In modern Java I reach for the `Comparator` factory methods — `comparing`, `comparingInt`, `thenComparing`, `reversed`, `nullsFirst` — because they compose cleanly and avoid common pitfalls like integer overflow from the subtraction trick."

### Vocabulário

| Termo PT | Termo EN |
|---|---|
| ordem natural | natural ordering |
| ordenação customizada | custom / external ordering |
| comparador | comparator |
| consistência com equals | consistency with equals |
| combinador de comparadores | comparator combinator / chaining |
| desempate lexicográfico | lexicographic tiebreak |
| nulos no início / fim | nulls first / nulls last |
| overflow de inteiro | integer overflow |
| coleção ordenada | sorted collection |
| extrator de chave | key extractor |
| inversão de ordem | reversed / descending order |
| ordenação estável | stable sort |

## Veja também

- [[01 - O Collections Framework]]
- [[02 - Listas, conjuntos e filas]]
- [[07 - Operações de Stream — intermediárias e terminais]]
- [[03-Dominios/Tecnologia/Java/Collections e Streams/index|Collections e Streams (MOC do galho)]]
- [[03-Dominios/Tecnologia/Java/index|Trilha Java]]
- [[03-Dominios/Tecnologia/Java/Linguagem e sintaxe moderna/13 - Records e record patterns|Records]]
- [[03-Dominios/Tecnologia/Java/Dicionário de Java#Comparable|Comparable]]
- [[03-Dominios/Tecnologia/Java/Dicionário de Java#Comparator|Comparator]]

## Referências

- [Comparable — Java 21 API (Oracle)](https://docs.oracle.com/en/java/javase/21/docs/api/java.base/java/lang/Comparable.html)
- [Comparator — Java 21 API (Oracle)](https://docs.oracle.com/en/java/javase/21/docs/api/java.base/java/util/Comparator.html)
- [Sorting Objects — dev.java](https://dev.java/learn/api/collections-framework/sorting/)
