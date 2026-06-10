---
title: "Mono e Flux — os publishers do Project Reactor"
created: 2026-06-10
updated: 2026-06-10
type: concept
progress: backlog
status: seedling
publish: true
fase: iniciado
tags:
  - java
  - reativa
  - iniciado
  - mono-flux
  - reactor
aliases:
  - "Mono"
  - "Flux"
  - "Project Reactor"
---

# Mono e Flux — os publishers do Project Reactor

> [!abstract] TL;DR
> `Mono<T>` representa **0-1 elemento** e `Flux<T>` representa **0-N elementos** — a cardinalidade fica codificada no próprio **sistema de tipos**, não escondida em documentação.
> Ambos são `Publisher`s **lazy**: descrever o pipeline (assembly) não dispara nada; o trabalho só roda no `subscribe`.
> São as duas peças centrais do **Project Reactor** (família 3.x, hoje 3.8.x), a implementação de Reactive Streams adotada pelo Spring WebFlux.

## O que é

`Mono` e `Flux` são os dois tipos reativos centrais do **Project Reactor**. Ambos implementam o `Publisher` da spec Reactive Streams, mas se distinguem por uma coisa: **quantos elementos podem emitir**.

- **`Mono<T>`** — uma sequência assíncrona de **0 ou 1** elemento (zero-or-one). Termina com no máximo um `onNext` seguido de `onComplete`, ou direto com `onComplete` (vazio), ou com `onError`.
- **`Flux<T>`** — uma sequência assíncrona de **0 a N** elementos (zero-to-many). Pode emitir nenhum, um, muitos ou infinitos `onNext` antes do sinal terminal.

A documentação oficial coloca exatamente assim: `Flux` é "uma sequência reativa de 0..N itens", enquanto um `Mono` é "um resultado de valor-único-ou-vazio (0..1)". A diferença não é estilística — é **semântica codificada no tipo**.

## Por que importa

A cardinalidade no tipo é uma forma de **documentação executável**. A assinatura `Mono<Order> findById(String id)` diz, sem comentário nenhum, que aquela busca retorna no máximo um pedido. Já `Flux<Order> findByCustomer(String customerId)` anuncia que podem vir vários. O compilador passa a carregar parte da intenção do código.

Para entrevista, três pontos importam:

- **Escolher o tipo certo é design de API.** Trocar `Mono` por `Flux` (ou vice-versa) quando a cardinalidade real é outra confunde quem consome e força conversões desnecessárias (`.next()`, `.single()`, `.collectList()`).
- **Lazy é o comportamento padrão.** Diferente de um `CompletableFuture`, que já está rodando quando você o tem em mãos, um `Mono`/`Flux` é só uma **receita**. Nada acontece até alguém assinar.
- **São interoperáveis.** Por implementarem `Publisher`, conversam com qualquer biblioteca Reactive Streams e com o `java.util.concurrent.Flow` do JDK (via adaptador).

## Como funciona

### `Mono` (0-1): zero ou um elemento

`Mono<T>` modela uma resposta **pontual**: o resultado de uma chamada HTTP, uma leitura por chave primária, a confirmação de um comando. Ele emite **no máximo um** valor.

Os três finais possíveis de um `Mono`:

- **um valor** → `onNext(t)` seguido de `onComplete()`;
- **vazio** → só `onComplete()` (ex.: `Mono.empty()`, ou um `findById` que não achou nada);
- **erro** → `onError(throwable)`.

Por emitir no máximo um item, `Mono` oferece operadores que não fazem sentido em fluxos longos, e é o tipo natural para representar "tenho ou não tenho um resultado".

### `Flux` (0-N): um stream de zero a muitos

`Flux<T>` modela um **stream**: linhas de um arquivo, eventos de uma fila, páginas de um cursor, ticks de um relógio. Pode emitir de zero a infinitos elementos antes (se algum dia) de terminar.

```text
Flux<Order>:  --o1--o2--o3--|
                              ^ onComplete (opcional; um Flux infinito nunca chega aqui)

Mono<Order>:  ------o1--|
                        ^ no máximo um onNext, depois onComplete
```

Você navega entre os dois quando a cardinalidade muda: `flux.next()` pega o primeiro elemento como `Mono`; `mono.flux()` promove para `Flux`; `flux.collectList()` agrega tudo num `Mono<List<T>>`.

### Criação: `just`, `fromIterable`, `defer`, `empty`, `error`, `fromCallable`

Os métodos de fábrica mais comuns:

- **`Mono.just(value)` / `Flux.just(a, b, c)`** — envolve valores **já existentes em memória**. Os valores são capturados no momento do *assembly* (quando você escreve a linha), não no `subscribe`.
- **`Flux.fromIterable(collection)`** — emite cada elemento de um `Iterable` (uma `List`, por exemplo), um `onNext` por item.
- **`Mono.fromCallable(() -> ...)`** — adia uma chamada **bloqueante/custosa** para o momento do `subscribe`; a lambda (`Callable`) só roda quando alguém assina. Ideal para envolver código síncrono num `Mono` lazy.
- **`Mono.defer(supplier)` / `Flux.defer(supplier)`** — adia a **construção do próprio publisher** para cada assinatura. O `Supplier` é chamado a cada `subscribe`, gerando um publisher fresco por assinante.
- **`Mono.empty()` / `Flux.empty()`** — completa imediatamente sem emitir nenhum valor.
- **`Mono.error(throwable)` / `Flux.error(throwable)`** — termina imediatamente com `onError`.

A distinção `just` vs `fromCallable`/`defer` é a fronteira entre **eager no assembly** e **lazy no subscribe** — o tema central da [[03-Dominios/Java/Programação Reativa/04 - Nada acontece até o subscribe — lazy, assembly vs subscription, cold vs hot|próxima nota]].

### Marble diagrams: a linguagem visual dos operadores

A documentação do Reactor descreve cada operador com **marble diagrams** (diagramas de bolinhas). A convenção:

```text
Tempo flui da esquerda para a direita ──────────────►

  --1--2--3--|        cada bolinha = um onNext; "|" = onComplete
  --1--2--X           "X" = onError (sinal terminal de falha)

        │  operador  │
        ▼            ▼

  --A--B--C--|        a linha de baixo é a saída transformada
```

Ler marble diagrams é o atalho para entender qualquer operador (`map`, `filter`, `flatMap`, `merge`…) sem decorar prosa: você vê o que entra, o que sai e quando termina.

## Na prática

```java
import reactor.core.publisher.Mono;
import reactor.core.publisher.Flux;

import java.util.List;

// 1. Mono.just — um valor já em memória (0-1)
Order order = new Order("A-1");
Mono<Order> single = Mono.just(order);

// 2. Flux.fromIterable — emite cada elemento de uma coleção (0-N)
List<Order> orders = List.of(new Order("A-1"), new Order("A-2"), new Order("A-3"));
Flux<Order> stream = Flux.fromIterable(orders);

// 3. Mono.fromCallable — adia uma chamada custosa para o subscribe
Mono<Customer> lookup = Mono.fromCallable(() -> repository.find(customerId));
//   repository.find(...) só roda quando alguém assina, não aqui.

// 4. Mono.defer — constrói um publisher novo por assinatura
Mono<Product> deferred = Mono.defer(() -> Mono.just(loadProduct()));
//   loadProduct() roda a cada subscribe, gerando um Mono fresco.

// Nada acima executou trabalho de I/O ainda; só no subscribe:
stream
    .map(Order::id)
    .subscribe(id -> System.out.println("Pedido: " + id));
```

Marble diagram do `Flux.fromIterable` sobre três pedidos seguido de `map(Order::id)`:

```text
fromIterable([A-1, A-2, A-3]):  --[A-1]--[A-2]--[A-3]--|

                                  │  map(Order::id)  │
                                  ▼                  ▼

                                --"A-1"--"A-2"--"A-3"--|
```

## Armadilhas

### (1) `Mono.just(expensiveCall())` avalia eager no assembly

`Mono.just(x)` recebe um **valor**, não uma função. Logo, `expensiveCall()` é executado **imediatamente**, na linha em que você escreve o `just` — antes de qualquer `subscribe`, e mesmo que ninguém assine. Você perde a laziness e ainda executa I/O fora da cadeia reativa.

```java
// ERRADO: repository.find(id) roda agora, no assembly, eager
Mono<Customer> bad = Mono.just(repository.find(id));
```

**Fix:** envolva a chamada num `Mono.fromCallable(() -> repository.find(id))` (ou `Mono.defer`) para adiar ao `subscribe`.

### (2) Usar `Flux` onde um `Mono` bastava

Modelar um resultado **único** como `Flux<Order>` mente sobre a cardinalidade: quem consome não sabe se vêm zero, um ou mil pedidos, e é forçado a `.next()`/`.single()` para extrair o valor. O tipo deixa de documentar a intenção.

```java
// ERRADO: findById retorna no máximo um; Flux confunde o chamador
Flux<Order> findById(String id) { ... }
```

**Fix:** use `Mono<Order> findById(String id)` quando a cardinalidade real é 0-1.

### (3) `Flux.just(list)` esperando achatar a coleção

`Flux.just(someList)` trata a `List` inteira como **um único elemento**, produzindo um `Flux<List<Order>>` que emite um `onNext` só. Você não itera sobre os pedidos — itera sobre uma lista de tamanho um.

```java
// ERRADO: emite a List como um único item -> Flux<List<Order>>
Flux<List<Order>> oops = Flux.just(orders);
```

**Fix:** use `Flux.fromIterable(orders)` para emitir cada elemento individualmente.

## Em entrevista

### Frase pronta (inglês)

> In Project Reactor the two core reactive types are `Mono` and `Flux`. A `Mono<T>` represents an asynchronous sequence of zero or one element, while a `Flux<T>` represents zero to many — the cardinality is encoded directly in the type, so the signature itself documents whether a call returns at most one result or a stream. Both are `Publisher`s and both are lazy: building the pipeline at assembly time does no work, and nothing actually runs until you subscribe. A common pitfall is wrapping an expensive or blocking call in `Mono.just(...)`, which evaluates it eagerly at assembly time; you defer it with `Mono.fromCallable` or `Mono.defer` instead. I also pick the type carefully — using `Mono` when there's at most one value keeps the API honest about cardinality.

### Vocabulário

| Termo PT | Termo EN |
|---|---|
| cardinalidade | cardinality |
| sistema de tipos | type system |
| montagem (do pipeline) | assembly (time) |
| avaliação preguiçosa | lazy evaluation |
| avaliação ansiosa | eager evaluation |
| método de fábrica | factory method |
| diagrama de bolinhas | marble diagram |
| achatar (a coleção) | flatten |

## Veja também

- [[03-Dominios/Java/Programação Reativa/01 - O que é programação reativa — o modelo push, assíncrono e não-bloqueante|O que é programação reativa]]
- [[03-Dominios/Java/Programação Reativa/04 - Nada acontece até o subscribe — lazy, assembly vs subscription, cold vs hot|Nada acontece até o subscribe]]
- [[03-Dominios/Java/Programação Reativa/05 - map e flatMap — transformando o fluxo|map e flatMap]]
- [[03-Dominios/Java/Programação Reativa/index|Programação Reativa (MOC do galho)]]
- [[03-Dominios/Java/index|Trilha Java]]
- [[03-Dominios/Java/Dicionário de Java|Dicionário de Java]]

## Referências

- Project Reactor — Reference Guide, "Introduction to Reactive Programming" (Mono/Flux, cardinalidade): https://projectreactor.io/docs/core/release/reference/reactiveProgramming.html
- Project Reactor — Reference Guide, "Reactor Core Features" (criação e marble diagrams): https://projectreactor.io/docs/core/release/reference/coreFeatures.html
- Project Reactor — "How to read marble diagrams?" (apêndice): https://projectreactor.io/docs/core/release/reference/apdx-howtoReadMarbles.html
