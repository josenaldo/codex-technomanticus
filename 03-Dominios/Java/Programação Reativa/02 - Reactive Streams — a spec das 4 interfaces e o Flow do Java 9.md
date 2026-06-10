---
title: "Reactive Streams — a spec das 4 interfaces e o Flow do Java 9"
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
  - reactive-streams
aliases:
  - "Reactive Streams"
  - "java.util.concurrent.Flow"
---

# Reactive Streams — a spec das 4 interfaces e o Flow do Java 9

> [!abstract] TL;DR
> **Reactive Streams** é uma especificação de apenas **4 interfaces** — `Publisher`, `Subscriber`, `Subscription` e `Processor` — que padroniza o fluxo de dados assíncrono com **backpressure** (o consumidor pede; o produtor não empurra à força).
> A spec foi **absorvida no JDK como `java.util.concurrent.Flow` no Java 9**, com as interfaces aninhadas 1:1 semanticamente equivalentes às originais.
> Project Reactor, RxJava e Akka Streams são **implementações**; a spec é só o contrato. Você quase nunca a implementa na mão — usa o Reactor.

## O que é

Reactive Streams é uma **especificação** (não uma biblioteca) que define como dois lados de uma fronteira assíncrona trocam um fluxo de elementos sem que o lado receptor seja forçado a bufferizar uma quantidade arbitrária de dados. O objetivo declarado na própria spec é "governar a troca de dados de stream através de uma fronteira assíncrona... garantindo que o lado receptor não seja forçado a bufferizar quantidades arbitrárias".

O coração da spec são **4 interfaces** e **4 sinais**. Tudo o mais — operadores, schedulers, `Mono`/`Flux` — é construído por cima disso pelas implementações. A spec em si é minúscula e propositalmente neutra: ela só descreve o **protocolo** de conversa entre produtor e consumidor.

Desde o **Java 9**, essas mesmas interfaces vivem dentro do JDK na classe `java.util.concurrent.Flow`, como interfaces aninhadas (`Flow.Publisher`, `Flow.Subscriber`, etc.), 1:1 semanticamente equivalentes às do `org.reactivestreams`.

## Por que importa

Sem um contrato comum, cada biblioteca reativa falaria um dialeto próprio e elas não interoperariam. Reactive Streams é o **denominador comum**: um `Publisher` do Reactor pode conversar com um `Subscriber` do RxJava porque ambos honram o mesmo protocolo.

Para quem está em entrevista, três pontos importam:

- **Backpressure é parte integral do modelo.** Não é um extra opcional — a spec foi desenhada para que filas entre threads sejam *limitadas* (bounded), evitando `OutOfMemoryError` quando o produtor é mais rápido que o consumidor.
- **A spec virou JDK no Java 9.** Saber que `java.util.concurrent.Flow` existe (e que é a mesma coisa) mostra que você entende a linha do tempo, não só a marca "Reactor".
- **Spec ≠ implementação.** Confundir `Flux` (Reactor) com `Flow.Publisher` (JDK) é um erro clássico. `Flux` *adapta* para `Flow.Publisher`, mas não *é* essa interface.

## Como funciona

### As 4 interfaces e os 4 sinais (`onSubscribe`/`onNext`/`onError`/`onComplete`)

As quatro interfaces (na forma do `Flow` do JDK) são:

- **`Publisher<T>`** — produz itens. Um único método: `void subscribe(Subscriber<? super T> s)`.
- **`Subscriber<T>`** — consome itens, recebendo os **4 sinais**:
  - `onSubscribe(Subscription s)` — chamado uma vez, no início, entregando a `Subscription`.
  - `onNext(T item)` — chamado zero ou mais vezes, um por item.
  - `onError(Throwable t)` — sinal terminal de falha.
  - `onComplete()` — sinal terminal de sucesso.
- **`Subscription`** — o canal de controle entre os dois (ver abaixo).
- **`Processor<T,R>`** — é ao mesmo tempo `Subscriber<T>` e `Publisher<R>`: um estágio que recebe `T` e emite `R`.

O protocolo é estritamente ordenado: para uma dada `Subscription`, as chamadas ao `Subscriber` são sequenciais. Há exatamente **um** sinal terminal — ou `onError`, ou `onComplete`, nunca os dois, nunca depois de já ter terminado.

### O `Subscription` e o contrato de backpressure (`request(n)`/`cancel`)

A `Subscription` é o que transforma um "push cego" em um **pull-push controlado**. Ela tem só dois métodos:

- `request(long n)` — o `Subscriber` declara que está pronto para receber até `n` itens a mais. O `Publisher` só pode emitir `onNext` até o total demandado.
- `cancel()` — o `Subscriber` pede para parar; o `Publisher` deve eventualmente cessar as emissões.

Esse é o **backpressure**: o consumidor dita o ritmo. O produtor nunca empurra mais do que foi pedido. Se o consumidor está lento, ele simplesmente demora a chamar `request` de novo, e a fila entre as threads permanece limitada.

### `java.util.concurrent.Flow`: a spec no JDK desde o Java 9

No **Java 9** (JEP 266), a especificação entrou no JDK como `java.util.concurrent.Flow`, uma classe que serve apenas de namespace para as 4 interfaces aninhadas: `Flow.Publisher`, `Flow.Subscriber`, `Flow.Subscription` e `Flow.Processor`. As assinaturas são idênticas às do `org.reactivestreams` e a documentação afirma que elas "correspondem à especificação reactive-streams desde o Java 9".

O JDK também traz `Flow.defaultBufferSize()` (256 no Java 21) e uma implementação utilitária, `SubmissionPublisher`, mas **não** traz operadores como `map`/`filter`/`flatMap`. Para isso, você ainda precisa de uma biblioteca.

### Implementações: Reactor, RxJava, Akka Streams (a spec é o denominador comum)

A spec é só o contrato; as bibliotecas é que entregam a usabilidade:

- **Project Reactor** — `Mono` e `Flux`; é a implementação adotada pelo Spring WebFlux.
- **RxJava** — `Flowable` (com backpressure), além de `Observable`/`Single`/etc.
- **Akka Streams** — `Source`/`Flow`/`Sink`, com materialização explícita.

Como todas honram Reactive Streams, um `Publisher` de uma pode ser consumido por um `Subscriber` de outra. A spec é o que garante essa interoperabilidade.

## Na prática

As 4 interfaces, na forma do JDK, têm assinaturas mínimas:

```java
import java.util.concurrent.Flow;

interface Publisher<T> {
    void subscribe(Flow.Subscriber<? super T> subscriber);
}

interface Subscriber<T> {
    void onSubscribe(Flow.Subscription subscription); // 1x, entrega o controle
    void onNext(T item);                              // 0..n itens
    void onError(Throwable throwable);                // terminal: falha
    void onComplete();                                // terminal: sucesso
}

interface Subscription {
    void request(long n); // backpressure: "estou pronto p/ mais n"
    void cancel();        // pare de emitir
}

// Processor é Subscriber<T> + Publisher<R> ao mesmo tempo
interface Processor<T, R> extends Flow.Subscriber<T>, Flow.Publisher<R> {}
```

Um `Subscriber` mínimo, implementando os 4 callbacks à mão, deixa o protocolo explícito:

```java
import java.util.concurrent.Flow;

class OrderSubscriber implements Flow.Subscriber<Order> {

    private Flow.Subscription subscription;

    @Override
    public void onSubscribe(Flow.Subscription subscription) {
        this.subscription = subscription;
        subscription.request(1); // pede o primeiro item (backpressure)
    }

    @Override
    public void onNext(Order order) {
        System.out.println("Recebido: " + order.id());
        subscription.request(1); // já consumi, peço o próximo
    }

    @Override
    public void onError(Throwable throwable) {
        System.err.println("Falhou: " + throwable.getMessage());
    }

    @Override
    public void onComplete() {
        System.out.println("Stream de pedidos encerrado.");
    }
}
```

Na vida real você **não** escreve isso. Você usa o Reactor e deixa o operador cuidar do `request`:

```java
import reactor.core.publisher.Flux;

Flux.just(new Order("A-1"), new Order("A-2"), new Order("A-3"))
    .map(Order::id)
    .subscribe(
        id -> System.out.println("Recebido: " + id), // onNext
        err -> System.err.println("Falhou: " + err),  // onError
        () -> System.out.println("Encerrado.")        // onComplete
    );
```

O `subscribe(...)` do Reactor recebe lambdas que mapeiam exatamente para os mesmos 3 sinais não-`onSubscribe` — o `onSubscribe` e a chamada inicial de `request` são tratados pelo framework.

## Armadilhas

### (1) Implementar `Publisher`/`Subscriber` na mão

O protocolo parece simples, mas tem **regras sutis**: exatamente um sinal terminal, nada de emitir `onNext` além do que foi demandado, chamadas sequenciais, tratar `cancel()` de forma thread-safe, não chamar nada depois de `onComplete`/`onError`. É fácil violar a spec sem perceber e produzir bugs de concorrência intermitentes.

```java
// ERRADO: emite sem respeitar o request(n) e chama onNext depois de onComplete
public void onSubscribe(Flow.Subscription s) {
    s.request(Long.MAX_VALUE);     // "me dê tudo" — joga backpressure fora
}
// ...e em algum lugar: subscriber.onComplete(); subscriber.onNext(x); // viola a spec
```

**Fix:** use o Reactor (`Flux.create`, `Flux.generate`, operadores) em vez de implementar as interfaces manualmente.

### (2) Confundir a spec (`Flow`) com a implementação (Reactor)

`Flux` **não é** um `java.util.concurrent.Flow.Publisher`. São tipos diferentes: a spec é o contrato, `Flux` é a implementação concreta do Reactor. Tratar um como o outro causa erro de compilação (ou confusão conceitual em entrevista).

```java
// NÃO compila: Flux não estende Flow.Publisher
Flow.Publisher<Order> p = Flux.just(new Order("A-1"));
```

**Fix:** adapte explicitamente — `JdkFlowAdapter.publisherToFlowPublisher(flux)` converte um `Flux` num `Flow.Publisher`, e há o caminho de volta.

## Em entrevista

### Frase pronta (inglês)

> Reactive Streams is a minimal specification — just four interfaces: `Publisher`, `Subscriber`, `Subscription`, and `Processor`, plus four signals: `onSubscribe`, `onNext`, `onError`, and `onComplete`. Its whole point is backpressure: the subscriber controls the pace through `Subscription.request(n)`, so the producer never overwhelms a slower consumer and the queues between threads stay bounded. The specification was absorbed into the JDK as `java.util.concurrent.Flow` back in Java 9, with the nested interfaces being one-to-one equivalent. Project Reactor, RxJava, and Akka Streams are implementations of that common contract — in practice I use Reactor rather than implementing `Publisher` or `Subscriber` by hand, because the protocol is subtle and easy to get wrong.

### Vocabulário

| Termo PT | Termo EN |
|---|---|
| especificação | specification |
| contra-pressão | backpressure |
| produtor / consumidor | publisher / subscriber |
| inscrição (canal de controle) | subscription |
| sinal terminal | terminal signal |
| demanda (de itens) | demand (request) |
| fronteira assíncrona | asynchronous boundary |
| fila limitada | bounded queue |

## Veja também

- [[03-Dominios/Java/Programação Reativa/01 - O que é programação reativa — o modelo push, assíncrono e não-bloqueante|O que é programação reativa]]
- [[03-Dominios/Java/Programação Reativa/03 - Mono e Flux — os publishers do Project Reactor|Mono e Flux]]
- [[03-Dominios/Java/Programação Reativa/09 - Backpressure — request(n) e as estratégias BUFFER, DROP, LATEST|Backpressure]]
- [[03-Dominios/Java/Linguagem e sintaxe moderna/15 - A evolução do Java (8 a 25)|A evolução do Java]]
- [[03-Dominios/Java/Programação Reativa/index|Programação Reativa (MOC do galho)]]
- [[03-Dominios/Java/index|Trilha Java]]
- [[03-Dominios/Java/Dicionário de Java|Dicionário de Java]]

## Referências

- Reactive Streams — site oficial e especificação: https://www.reactive-streams.org/
- Reactive Streams JVM (README da spec, v1.0.4): https://github.com/reactive-streams/reactive-streams-jvm
- JDK 21 — `java.util.concurrent.Flow` (javadoc): https://docs.oracle.com/en/java/javase/21/docs/api/java.base/java/util/concurrent/Flow.html
