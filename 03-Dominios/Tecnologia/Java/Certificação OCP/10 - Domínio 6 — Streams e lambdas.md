---
title: "Domínio 6 — Streams e lambdas"
created: 2026-06-13
updated: 2026-06-13
type: concept
status: seedling
publish: true
fase: dominios
tags:
  - java
  - certificacao-ocp
  - dominios
aliases:
  - "Domínio 6 OCP"
  - "Streams e lambdas na OCP"
---

# Domínio 6 — Streams e lambdas

> [!abstract] TL;DR
> O domínio que cobra programação funcional: lambdas, method references, interfaces funcionais, e o pipeline completo de Stream (criação → operações intermediárias preguiçosas → terminal). Mais `Collectors`, `Optional` e parallel streams. É o domínio mais "sintático" da prova — a Oracle adora pegadinhas de avaliação preguiçosa, reuso de stream e `orElse` vs `orElseGet`. Quem fechou o Galho 2 (Collections e Streams) já tem o terreno; aqui é revisão com lupa de certificação.

> [!info] Títulos oficiais
> - **1Z0-830 (Java 21):** *Working with Streams and Lambda expressions*
> - **1Z0-831 (Java 25):** *Processing Data Using Streams and Lambda Expressions*

## O que a Oracle cobra

- **Lambda syntax** — formas dos parâmetros (com/sem tipo, parênteses), corpo de expressão vs corpo de bloco, e a regra de ouro: variáveis capturadas precisam ser **effectively final**.
- **Method references** — as quatro formas: `Class::staticMethod`, `instance::method` (instância vinculada), `Class::instanceMethod` (instância não vinculada, o primeiro parâmetro vira o receptor) e `Class::new` (construtor).
- **Interfaces funcionais** — `Function<T,R>`, `Predicate<T>`, `Consumer<T>`, `Supplier<T>`, `BiFunction<T,U,R>`, `UnaryOperator<T>` e suas versões **primitivas** (`IntFunction`, `IntPredicate`, `ToIntFunction`, `IntUnaryOperator`, etc.) — saber qual usar para não fazer boxing à toa.
- **Criação de stream** — `coll.stream()`, `Stream.of(...)`, `Stream.generate(supplier)`, `Stream.iterate(seed, next)` (e a versão de 3 args com predicado), `IntStream.range`/`rangeClosed`.
- **Operações intermediárias** (preguiçosas, devolvem `Stream`) — `filter`, `map`, `flatMap`, `distinct`, `sorted`, `peek`, `limit`, `skip`, `takeWhile`, `dropWhile`.
- **Operações terminais** (disparam o pipeline) — `forEach`, `toList`, `collect`, `reduce`, `count`, `min`, `max`, `findFirst`, `findAny`, `anyMatch`, `allMatch`, `noneMatch`.
- **Collectors** — `toList`, `toSet`, `toMap`, `joining`, `groupingBy`, `partitioningBy`, `counting`, `summingInt`, `averagingDouble`, `mapping`, `reducing`.
- **Optional** — `of`, `empty`, `ofNullable`, `isPresent`, `ifPresent`, `orElse`, `orElseGet`, `orElseThrow`, `map`, `flatMap`, `filter`.
- **Parallel streams** — `parallelStream()` / `.parallel()`; quando ajuda (dados grandes, operações sem estado), quando atrapalha (ordering, operações stateful, overhead).
- **Gatherers** (`Stream.gather`, fábrica `Gatherers`) — finalizados no **Java 24**; podem aparecer numa questão da trilha 1Z0-831, ainda que de raspão.

## Mapa de revisão

- [[03-Dominios/Tecnologia/Java/Collections e Streams/04 - Lambdas e interfaces funcionais|Lambdas e interfaces funcionais (G2)]]
- [[03-Dominios/Tecnologia/Java/Collections e Streams/05 - Introdução à Stream API|Introdução à Stream API (G2)]]
- [[03-Dominios/Tecnologia/Java/Collections e Streams/07 - Operações de Stream — intermediárias e terminais|Operações de Stream (G2)]]
- [[03-Dominios/Tecnologia/Java/Collections e Streams/08 - Collectors e agrupamento|Collectors e agrupamento (G2)]]
- [[03-Dominios/Tecnologia/Java/Collections e Streams/09 - Streams primitivos|Streams primitivos (G2)]]
- [[03-Dominios/Tecnologia/Java/Collections e Streams/10 - Optional|Optional (G2)]]
- [[03-Dominios/Tecnologia/Java/Collections e Streams/13 - Composição funcional e funções de alta ordem|Composição funcional (G2)]]
- [[03-Dominios/Tecnologia/Java/Collections e Streams/15 - Collectors customizados e Gatherers|Collectors customizados e Gatherers (G2)]]

## Pegadinhas deste domínio

A prova quase nunca pergunta "o que `filter` faz". Ela monta um pipeline e pergunta o que imprime — e a resposta depende de você lembrar que streams são preguiçosos e descartáveis.

**1. Stream é one-shot.** Uma vez consumido por uma operação terminal, o stream está fechado. Chamar outra terminal (ou qualquer operação) no mesmo objeto explode:

```java
Stream<String> s = Stream.of("a", "b");
s.forEach(System.out::println);
long n = s.count(); // IllegalStateException: stream has already been operated upon or closed
```

**2. `peek` é preguiçoso.** Sem terminal — ou com um terminal que não demanda todos os elementos — o `peek` pode simplesmente não rodar para alguns (ou todos) os elementos:

```java
Stream.of("a", "b", "c")
      .peek(System.out::println)   // não imprime nada: não há terminal
      .map(String::toUpperCase);
```

**3. `orElse` sempre avalia o argumento.** Mesmo quando o `Optional` tem valor, a expressão passada para `orElse(...)` é avaliada — porque é um argumento de método comum. Para adiar o custo, use `orElseGet(Supplier)`:

```java
opt.orElse(expensive());          // expensive() roda SEMPRE
opt.orElseGet(() -> expensive()); // expensive() só roda se vazio
```

**4. `Collectors.toMap` lança em chave duplicada.** A sobrecarga de 2 args estoura `IllegalStateException` se duas entradas colidirem na chave. Passe uma `mergeFunction` (3 args) ou troque para `groupingBy`:

```java
.collect(Collectors.toMap(k, v, (a, b) -> a)); // resolve a colisão
```

**5. Lambda só captura variável effectively final.** Se a variável local é reatribuída depois (ou antes, fora do ponto de captura), a lambda nem compila:

```java
int x = 10;
Runnable r = () -> System.out.println(x);
x = 20; // ERRO de compilação: x deixa de ser effectively final
```

Para o arsenal completo destas armadilhas, veja [[03-Dominios/Tecnologia/Java/Certificação OCP/15 - O catálogo de pegadinhas clássicas|catálogo de pegadinhas]].

## Em entrevista

Numa conversa técnica, o detalhe que separa quem decorou de quem entendeu é a avaliação preguiçosa:

> "I prefer `orElseGet` over `orElse` when the fallback is expensive — `orElse` always evaluates its argument, even when the `Optional` is present. And I keep in mind that a stream is single-use: once a terminal operation runs, it's closed."

Dito sem reivindicar credencial nenhuma — é fluência de linguagem, não certificado.

| PT | EN |
|----|----|
| preguiçoso | lazy |
| terminal | terminal operation |
| efetivamente final | effectively final |
| interface funcional | functional interface |
| referência de método | method reference |

## Veja também

- [[03-Dominios/Tecnologia/Java/Certificação OCP/04 - O mapa objetivo → galho — revisar a trilha pra prova|O mapa objetivo → galho]]
- [[03-Dominios/Tecnologia/Java/Certificação OCP/12 - Domínio 8 — Concorrência|Domínio 8 — Concorrência]]
- [[03-Dominios/Tecnologia/Java/Certificação OCP/index|Certificação OCP (MOC do galho)]]

## Referências

- [Enthuware — OCP Java certification resources / syllabus](https://enthuware.com/oca-ocp-java-certification-resources/290-ocp-java-21-exam-syllabus)
