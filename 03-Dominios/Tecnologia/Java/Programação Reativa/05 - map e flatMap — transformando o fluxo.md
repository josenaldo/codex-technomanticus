---
title: "map e flatMap — transformando o fluxo"
created: 2026-06-10
updated: 2026-06-10
type: concept
progress: backlog
status: seedling
publish: true
fase: Adepto
tags:
  - java
  - reativa
  - adepto
  - operadores
  - reactor
aliases:
  - "map e flatMap"
  - "flatMap reativo"
---

# map e flatMap — transformando o fluxo

> [!abstract] TL;DR
> `map` é uma transformação **síncrona 1:1** (`T → R`): pega cada elemento e devolve outro valor, na mesma thread, sem assinar nada.
> `flatMap` é uma transformação **assíncrona** (`T → Publisher<R>`): para cada elemento você devolve **outro publisher**, e o `flatMap` o **assina e achata** o resultado de volta no fluxo de fora.
> A confusão central do reativo: usar `map` onde você precisava de `flatMap` produz um `Mono<Mono<T>>` (ou `Flux<Mono<T>>`) aninhado, porque o `map` nunca assina o publisher interno.

## O que é

`map` e `flatMap` são os dois operadores de transformação mais usados do **Project Reactor**, e a diferença entre eles é a fronteira que separa "transformar um valor" de "encadear outra operação assíncrona".

- **`map(Function<T, R>)`** — aplica uma função **pura e síncrona** a cada elemento, na base **1-para-1**. Entra um `T`, sai um `R`. Nada é assinado, nada é achatado. É o `Stream.map` da API reativa.
- **`flatMap(Function<T, Publisher<R>>)`** — para cada elemento, a função devolve um **novo publisher** (`Mono` ou `Flux`). O `flatMap` **assina** cada publisher interno e **mescla** (achata) suas emissões no fluxo de saída. É o operador para encadear chamadas reativas: I/O, repositório, HTTP.

A regra mnemônica: **se a sua lambda devolve um valor comum, use `map`; se devolve um `Mono`/`Flux`, use `flatMap`.**

## Por que importa

Esta é a dúvida que mais derruba gente em código reativo. Numa cadeia síncrona o tipo de retorno da lambda some dentro do `map`; em código reativo, **o tipo importa**, porque o publisher interno precisa ser assinado para entregar seu valor.

- **`map` com lambda que retorna publisher gera aninhamento.** `mono.map(id -> repository.findById(id))` — onde `findById` retorna `Mono<Order>` — produz um `Mono<Mono<Order>>`. O `map` viu um valor de tipo `Mono<Order>` e o tratou como um `R` qualquer. O `Order` lá dentro **nunca é extraído**, porque ninguém assinou o publisher interno.
- **`flatMap` é o ponto de costura entre operações assíncronas.** Toda vez que um passo da cadeia faz I/O (busca no banco, chamada HTTP), o retorno é um publisher, e você precisa de `flatMap` para emendá-lo na cadeia.
- **Ordem e concorrência são decisões de design.** `flatMap` **intercala** resultados (prioriza concorrência sobre ordem); quando a ordem importa, troca-se por `concatMap` ou `flatMapSequential`. Saber qual escolher é o que separa "funciona" de "funciona certo".

## Como funciona

### `map`: transformação síncrona 1:1 (`T → R`)

`map` recebe uma `Function<T, R>` e a aplica a cada `onNext`, **na mesma thread** em que o elemento chegou. Não há assinatura de sub-publishers, não há mudança de cardinalidade: um elemento de entrada vira **exatamente um** de saída.

```text
Flux<Order>:  --o1--o2--o3--|

              │  map(o -> o.total())  │
              ▼                       ▼

Flux<Money>:  --m1--m2--m3--|
```

Use `map` para transformações puras: extrair um campo, calcular um valor derivado, converter um DTO. Se a função pode lançar exceção verificada ou bloqueia, ela ainda roda na thread do `onNext` — o que pode ser um problema (ver [[03-Dominios/Tecnologia/Java/Programação Reativa/08 - Schedulers — subscribeOn, publishOn e em qual thread o código roda|Schedulers]]).

### `flatMap`: transformação assíncrona que retorna outro publisher (`T → Publisher<R>`, achatado)

`flatMap` recebe uma `Function<T, Publisher<R>>`. Para cada elemento de entrada, a função produz um **publisher interno**; o `flatMap` **assina** esse publisher e **mescla** as emissões dele no fluxo de saída. É uma operação **assíncrona**: vários publishers internos podem estar ativos ao mesmo tempo, e por isso `flatMap` **não garante ordem** — os resultados saem na ordem em que **chegam**, não na ordem dos elementos de origem.

```text
Flux<String>:  --A----B--------|       (ids de pedido)

               │  flatMap(id -> findById(id))  │     cada inner é um Mono assíncrono
               ▼                                ▼

Flux<Order>:   ----oB----oA-----|       B respondeu antes de A: ordem INTERCALADA
```

Por padrão, `flatMap` mantém até **256 publishers internos** assinados simultaneamente (o parâmetro `concurrency`, ver adiante). É o operador certo sempre que o próximo passo da cadeia é, ele mesmo, reativo.

### Por que uma chamada reativa dentro de outra exige `flatMap` (senão vira `Mono<Mono<T>>`)

Quando a lambda devolve um publisher, o que importa é **quem assina esse publisher interno**:

- **`map` não assina nada.** Ele trata o `Mono<Order>` devolvido como um valor `R` qualquer e o repassa intacto. Resultado: `Mono<Mono<Order>>` — um publisher que, ao ser assinado, emite **outro publisher** em vez do `Order`. O dado de dentro fica preso.
- **`flatMap` assina o publisher interno** e propaga o que ele emite. Resultado: `Mono<Order>` — achatado, com o `Order` realmente extraído.

```text
mono.map(id -> findById(id))      ->  Mono<Mono<Order>>   (aninhado: ninguém assinou o inner)
mono.flatMap(id -> findById(id))  ->  Mono<Order>         (achatado: flatMap assinou e mesclou)
```

"Achatar" (*flatten*) é literalmente remover um nível de aninhamento de publishers. É a razão de o operador se chamar `flatMap` e não só `map`.

### `concatMap`/`flatMapSequential`: quando a ordem importa

`flatMap` troca ordem por concorrência. Quando você precisa da ordem da origem preservada, há duas alternativas:

- **`concatMap`** — assina **um publisher interno de cada vez**: só começa o próximo depois que o anterior completa. Garante ordem **e** serializa a execução (concorrência efetiva = 1). Mais previsível, porém mais lento, pois não sobrepõe as chamadas.
- **`flatMapSequential`** — assina os publishers internos **eagerly** (em paralelo, como o `flatMap`), mas **bufferiza e reordena** as saídas para respeitar a ordem da origem. Mantém a concorrência do `flatMap` com a ordem do `concatMap`, ao custo de memória para o buffer.

```text
Origem:            --A--B--C--|

flatMap:           --B--A--C--|    (rápido, ordem NÃO preservada)
concatMap:         --A--B--C--|    (ordem preservada, um de cada vez — serial)
flatMapSequential: --A--B--C--|    (ordem preservada, internos em paralelo + reordena)
```

Operadores irmãos de finalização: **`then()`** ignora os valores e devolve um `Mono<Void>` que sinaliza só a conclusão; **`thenMany(publisher)`** descarta os valores da cadeia atual e, ao completar, troca para outro publisher. Úteis para "faça isto, descarte o resultado, depois faça aquilo".

## Na prática

`map` para transformação pura vs. `flatMap` para encadear uma chamada reativa, lado a lado:

```java
import reactor.core.publisher.Mono;
import reactor.core.publisher.Flux;

import java.math.BigDecimal;

// --- map: transformação SÍNCRONA 1:1 (T -> R) ---
// Somar imposto é cálculo puro: a lambda devolve um VALOR, não um publisher.
Mono<Order> order = Mono.just(new Order("A-1", new BigDecimal("100.00")));

Mono<Order> withTax = order
    .map(o -> o.withTotal(o.total().multiply(new BigDecimal("1.10"))));
//        ^ Order -> Order, na mesma thread, nada assinado.

// --- flatMap: transformação ASSÍNCRONA (T -> Publisher<R>), achatada ---
// findById devolve Mono<Order>: a lambda devolve um PUBLISHER -> precisa de flatMap.
Mono<String> orderId = Mono.just("A-1");

Mono<Order> loaded = orderId
    .flatMap(id -> orderRepository.findById(id));
//        ^ String -> Mono<Order>; flatMap assina o inner e achata -> Mono<Order>.

// --- O ERRO: map onde precisava de flatMap ---
// map vê o Mono<Order> como um R qualquer e o repassa SEM assinar:
Mono<Mono<Order>> nested = orderId
    .map(id -> orderRepository.findById(id));
//        ^ String -> Mono<Order>; map NÃO achata -> Mono<Mono<Order>> aninhado.
//          O Order lá dentro nunca é extraído.

// --- flatMap sobre um Flux: encadear I/O para cada elemento ---
Flux<String> ids = Flux.just("A-1", "A-2", "A-3");

Flux<Order> orders = ids
    .flatMap(id -> orderRepository.findById(id)); // ordem dos resultados NÃO garantida

// Se a ordem dos pedidos importa, troque por concatMap:
Flux<Order> ordered = ids
    .concatMap(id -> orderRepository.findById(id)); // ordem A-1, A-2, A-3 preservada
```

Suponha as assinaturas reativas:

```java
import reactor.core.publisher.Mono;

interface OrderRepository {
    Mono<Order> findById(String id);          // 0-1 pedido
}

record Order(String id, BigDecimal total) {
    Order withTotal(BigDecimal newTotal) { return new Order(id, newTotal); }
}
```

## Armadilhas

### (1) Usar `map` com função que retorna `Mono`/`Flux`

Se a lambda do `map` devolve um publisher, o `map` o trata como um valor comum e **não o assina**. Sobre um `Flux` você acaba com `Flux<Mono<Order>>`; sobre um `Mono`, com `Mono<Mono<Order>>`. O dado interno nunca é emitido, e o pior: às vezes compila e roda, mas o publisher interno fica órfão (nunca assinado), então o I/O **nem acontece**.

```java
// ERRADO: findById devolve Mono<Order>; map não achata.
Flux<Mono<Order>> oops = ids.map(id -> orderRepository.findById(id));
```

**Fix:** quando a lambda retorna um publisher, use `flatMap` (ou `concatMap`) para assinar e achatar.

### (2) `flatMap` quando a ordem importa (intercala os resultados)

`flatMap` prioriza concorrência sobre ordem: os publishers internos rodam em paralelo e as emissões saem na ordem em que **completam**, não na ordem da origem. Se você está montando uma lista paginada, exportando um relatório ordenado ou aplicando passos sequenciais, o resultado vem embaralhado.

```java
// ERRADO: páginas processadas em paralelo saem fora de ordem.
Flux<Row> rows = pageIds.flatMap(id -> renderPage(id)); // ordem indeterminada
```

**Fix:** use `concatMap` (serial, ordem garantida) ou `flatMapSequential` (paralelo + reordena) quando a ordem da origem precisa ser preservada.

### (3) Explosão de concorrência sem `flatMap(fn, concurrency)`

O `flatMap` padrão mantém até **256** publishers internos assinados ao mesmo tempo. Sobre um `Flux` grande, onde cada elemento dispara uma chamada HTTP ou query, isso pode abrir centenas de conexões simultâneas e derrubar o serviço de destino ou esgotar o pool.

```java
// ERRADO: até 256 chamadas concorrentes — pode estourar o pool de conexões.
Flux<Response> responses = thousandsOfIds.flatMap(id -> httpClient.call(id));
```

**Fix:** limite com a sobrecarga `flatMap(fn, concurrency)`, ex. `flatMap(id -> httpClient.call(id), 8)`, fixando um teto de chamadas em voo.

## Em entrevista

### Frase pronta (inglês)

> The key distinction is that `map` is a synchronous one-to-one transformation — you take a `T` and return an `R`, on the same thread, and nothing is subscribed. `flatMap` is asynchronous: the function returns a `Publisher`, and `flatMap` subscribes to each inner publisher and flattens its emissions back into the outer sequence, which is exactly what you need to chain reactive calls like a repository or an HTTP request. The classic mistake is using `map` where you needed `flatMap`: since `map` doesn't subscribe to the inner publisher, you end up with a nested `Mono<Mono<T>>` and the inner value is never extracted. One more nuance: `flatMap` interleaves results and favors concurrency over order, so when ordering matters I reach for `concatMap`, which processes one inner publisher at a time, or `flatMapSequential`, which runs them eagerly but reorders the output. I also cap fan-out with the `flatMap(fn, concurrency)` overload to avoid overwhelming downstream services.

### Vocabulário

| Termo PT | Termo EN |
|---|---|
| achatar | flatten |
| publisher interno | inner publisher |
| aninhado | nested |
| transformação 1-para-1 | one-to-one transformation |
| preservar a ordem | preserve ordering |
| intercalar | interleave |
| teto de concorrência | concurrency cap / limit |
| chamadas em voo | in-flight calls |

## Veja também

- [[03-Dominios/Tecnologia/Java/Programação Reativa/03 - Mono e Flux — os publishers do Project Reactor|Mono e Flux]]
- [[03-Dominios/Tecnologia/Java/Programação Reativa/06 - Combinando publishers — zip, merge, concat, filter|Combinando publishers]]
- [[03-Dominios/Tecnologia/Java/Programação Reativa/08 - Schedulers — subscribeOn, publishOn e em qual thread o código roda|Schedulers]]
- [[03-Dominios/Tecnologia/Java/Programação Reativa/index|Programação Reativa (MOC do galho)]]
- [[03-Dominios/Tecnologia/Java/index|Trilha Java]]
- [[03-Dominios/Tecnologia/Java/Dicionário de Java|Dicionário de Java]]

## Referências

- Project Reactor — Reference Guide, "Which operator do I need? / Transforming an Existing Sequence" (map, flatMap, concatMap, flatMapSequential): https://projectreactor.io/docs/core/release/reference/apdx-operatorChoice.html
- Project Reactor — Javadoc, `Flux` (`map`, `flatMap`, `flatMap(fn, concurrency)`, `concatMap`, `flatMapSequential`, `then`, `thenMany`): https://projectreactor.io/docs/core/release/api/reactor/core/publisher/Flux.html
- Project Reactor — Javadoc, `Mono` (`map`, `flatMap`, `then`, `thenMany`): https://projectreactor.io/docs/core/release/api/reactor/core/publisher/Mono.html
