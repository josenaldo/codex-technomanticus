---
title: "Nada acontece até o subscribe — lazy, assembly vs subscription, cold vs hot"
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
  - reactor
aliases:
  - "nada acontece até o subscribe"
  - "cold vs hot publisher"
  - "assembly time"
---

# Nada acontece até o subscribe — lazy, assembly vs subscription, cold vs hot

> [!abstract] TL;DR
> Um pipeline reativo é **lazy**: declarar operadores (`map`, `filter`, `flatMap`) não executa nada — só monta a descrição do processamento. O dado só flui quando alguém chama `subscribe()`. No WebFlux você quase nunca subscreve à mão: o framework subscreve por você. E há dois temperamentos de fonte: **cold** (cada subscriber refaz o trabalho desde o começo) vs **hot** (a fonte é compartilhada e late subscribers só pegam o que vier depois).

## O que é

Em Reactor, escrever uma cadeia de operadores sobre um `Mono` ou `Flux` **não dispara nada**. Você está montando uma *descrição* de um processo assíncrono — um plano. Como diz a documentação, ao escrever uma cadeia de `Publisher`, os dados não começam a fluir por padrão.

A execução só acontece quando um `Subscriber` se conecta ao `Publisher` via `subscribe()`. Esse é o momento em que um sinal de `request` sobe a cadeia até a fonte e o dado finalmente começa a fluir.

Há duas linhas do tempo distintas:

- **Assembly time** — quando a cadeia de operadores é construída. Cada operador embrulha o `Publisher` anterior num novo. Nenhum dado flui.
- **Subscription time** — quando `subscribe()` amarra um `Subscriber` à fonte. O `request` propaga pra cima e o dado flui.

Além disso, cada fonte tem um temperamento:

- **Cold** — começa do zero pra cada subscriber, incluindo na origem do dado. Se a fonte embrulha uma chamada HTTP, um novo request HTTP sai por subscription.
- **Hot** — não recomeça pra cada subscriber. Late subscribers recebem apenas os sinais emitidos *depois* de assinarem.

## Por que importa

Esse é o mal-entendido número um de quem vem de código imperativo. Você escreve um pipeline lindo, com `map`, `flatMap`, log no meio — e nada acontece. Nenhum erro, nenhum dado, silêncio. O motivo quase sempre é o mesmo: ninguém subscreveu.

Entender lazy vs eager muda como você raciocina:

- **Testes e código standalone** — se você não chamar `subscribe()` (ou `block()`), o pipeline nunca roda. Bugs silenciosos nascem daqui.
- **WebFlux** — o framework subscreve por você. Retornar um `Mono`/`Flux` de um controller é suficiente; subscrever à mão lá é antipadrão.
- **Cold vs hot** — assumir que dois subscribers de um cold publisher compartilham o resultado leva a HTTP duplicado, recálculo e efeitos colaterais repetidos. Saber forçar hot com `share()` evita isso.

## Como funciona

### Lazy: declarar ≠ executar (o erro nº1 do iniciante)

Quando você escreve `Flux.just(1, 2, 3).map(x -> x * 2)`, nada roda. Você só construiu um objeto `Flux` que *sabe como* dobrar os números — mas não dobrou nada ainda. É como uma receita escrita num papel: a receita não cozinha sozinha.

A cadeia só vira ação quando `subscribe()` é chamado. Nesse instante, um sinal de `request(n)` sobe a cadeia (do subscriber até a fonte), e a fonte começa a empurrar os itens pra baixo, operador por operador.

### Assembly time vs subscription time

Esses dois momentos acontecem em ordem, e confundi-los gera bugs sutis.

- **Assembly time** é o `new` da cadeia. Tudo que está *fora* de um operador lazy (ou seja, código Java comum que produz argumentos) roda agora. Por isso `Mono.just(buscarAgora())` já chamou `buscarAgora()` no assembly — antes de qualquer subscribe.
- **Subscription time** é quando o dado flui. Operadores como `map`, `filter`, `flatMap` só executam suas lambdas aqui.

A distinção importa pra coisas como `defer`: `Mono.defer(() -> Mono.just(buscarAgora()))` adia `buscarAgora()` pro subscription time, e refaz a cada subscribe.

### Quem chama `subscribe`: você nos testes, o framework no WebFlux

`subscribe()` retorna um `Disposable` — uma alça pra cancelar a subscription (via `dispose()`).

- **Em testes / código standalone**, *você* é responsável por disparar. Sem `subscribe()` (ou `block()`, que subscreve e espera), o pipeline fica inerte. Ferramentas como `StepVerifier` subscrevem por você no contexto de teste.
- **No Spring WebFlux**, *o framework* subscreve. A camada reativa do WebFlux recebe o `Publisher` que seu controller retorna e subscreve internamente, na escrita ao response HTTP — você nunca chama `subscribe()`. Fazer `subscribe()` ou `block()` dentro de um controller WebFlux é antipadrão — quebra o modelo não-bloqueante.

### Cold vs hot: refaz por subscriber (`defer`) vs compartilha (`share`/`publish`)

Por padrão, fontes em Reactor são **cold**: cada `subscribe()` reinicia a sequência desde a origem. Dois subscribers num cold publisher que faz HTTP disparam dois requests independentes.

Para transformar uma sequência cold em **hot** (compartilhada):

- `share()` — multicast pros subscribers, mantendo a fonte ativa enquanto houver ao menos um subscriber. Internamente é `publish().refCount()`.
- `publish()` — devolve um `ConnectableFlux`; nada emite até você chamar `connect()`, dando controle manual de quando a fonte liga.
- `refCount()` — automatiza: conecta quando o primeiro subscriber chega, desconecta quando o último sai.

Hot publishers têm consequência importante: late subscribers só pegam o que for emitido *depois* de assinarem; o que passou, passou.

## Na prática

Pipeline declarado sem subscribe — não roda:

```java
import reactor.core.publisher.Flux;

Flux<Integer> pedidos = Flux.just(1, 2, 3)
        .map(id -> {
            System.out.println("processando order " + id);
            return id * 10;
        });

// Nada foi impresso. O pipeline está montado, mas inerte.
```

O mesmo pipeline, agora com subscribe — roda:

```java
import reactor.core.publisher.Flux;

Flux<Integer> pedidos = Flux.just(1, 2, 3)
        .map(id -> {
            System.out.println("processando order " + id);
            return id * 10;
        });

pedidos.subscribe(total -> System.out.println("total: " + total));
// Agora imprime processando order 1/2/3 e os totais.
```

Cold (default): cada subscriber refaz a fonte:

```java
import reactor.core.publisher.Flux;

Flux<Integer> precos = Flux.range(1, 3)
        .map(n -> {
            System.out.println("consultando product " + n);
            return n * 100;
        });

precos.subscribe(p -> System.out.println("subscriber A: " + p));
precos.subscribe(p -> System.out.println("subscriber B: " + p));
// "consultando product N" aparece DUAS vezes — a fonte rodou por subscriber.
```

Hot com `share()`: a fonte é compartilhada:

```java
import reactor.core.publisher.Flux;

Flux<Integer> precosCompartilhados = Flux.range(1, 3)
        .map(n -> {
            System.out.println("consultando product " + n);
            return n * 100;
        })
        .share();

precosCompartilhados.subscribe(p -> System.out.println("subscriber A: " + p));
precosCompartilhados.subscribe(p -> System.out.println("subscriber B: " + p));
// A fonte roda uma vez e os subscribers compartilham a emissão.
```

## Armadilhas

### (1) Esquecer o `subscribe` — o pipeline nunca roda (bug nº1)

Você monta uma cadeia de `Customer`, faz `map`, `flatMap`, retorna do método — e nada acontece. Nenhuma exceção, nenhum dado. Como Reactor é lazy, sem subscriber o `request` nunca sobe até a fonte.

```java
import reactor.core.publisher.Mono;

// BUG: salvarCliente é chamado? Não. Ninguém subscreveu.
Mono<Customer> salvo = repository.save(novoCustomer);
// fim do método — o save nunca foi disparado.
```

Fix: garanta uma subscription — retorne o `Mono`/`Flux` (no WebFlux o framework subscreve) ou, em testes, use `StepVerifier`/`block()`.

### (2) Efeito colateral no `map` esperando que rode no assembly

Você coloca um efeito colateral (log, escrita, contador) numa lambda de `map` achando que ele dispara assim que a linha é escrita. Não: a lambda do `map` só roda no subscription time, e roda de novo a cada subscribe.

```java
import reactor.core.publisher.Flux;

Flux<Order> orders = origem
        .map(o -> { auditoria.registrar(o); return o; }); // só roda no subscribe
// Aqui, antes do subscribe, NENHUM registro de auditoria foi feito.
```

Fix: entenda que lambdas de operadores executam no subscription time; pra efeito por-item visível use `doOnNext`, e não conte com execução no assembly.

### (3) Assumir que dois subscribers de um cold publisher compartilham

Você subscreve duas vezes ao mesmo cold `Flux` que faz uma chamada HTTP cara, esperando uma única chamada. Cada subscription refaz a fonte do zero — duas chamadas HTTP, dois efeitos colaterais.

```java
import reactor.core.publisher.Flux;

Flux<Product> catalogo = clienteHttp.buscarProducts(); // cold: HTTP por subscriber
catalogo.subscribe(...); // request HTTP #1
catalogo.subscribe(...); // request HTTP #2 — não compartilha!
```

Fix: se quer compartilhar a mesma emissão entre subscribers, torne a fonte hot com `share()` (ou `publish().refCount()`).

## Em entrevista

### Frase pronta (inglês)

> In Project Reactor, a publisher chain is lazy and declarative: assembling operators like `map` or `flatMap` builds a plan but executes nothing — nothing happens until you subscribe. Calling `subscribe()` connects a subscriber to the source, propagates a request signal upstream, and only then does data flow; in WebFlux you rarely subscribe yourself, because the framework subscribes to the publisher your controller returns. A key distinction is cold versus hot: a cold publisher restarts the entire source for each subscriber — so two subscribers to an HTTP-backed flux fire two requests — whereas a hot publisher, obtained via `share()` or `publish()`, multicasts a single source and only delivers later signals to late subscribers.

### Vocabulário

| Termo PT | Termo EN |
| --- | --- |
| nada acontece até o subscribe | nothing happens until you subscribe |
| preguiçoso / declarativo | lazy / declarative |
| tempo de montagem | assembly time |
| tempo de subscription | subscription time |
| publisher frio / quente | cold / hot publisher |
| compartilhar / multicast | share / multicast |
| sinal de requisição | request signal |
| late subscriber | late subscriber |

## Veja também

- [[03-Dominios/Tecnologia/Java/Programação Reativa/03 - Mono e Flux — os publishers do Project Reactor|Mono e Flux]]
- [[03-Dominios/Tecnologia/Java/Programação Reativa/08 - Schedulers — subscribeOn, publishOn e em qual thread o código roda|Schedulers]]
- [[03-Dominios/Tecnologia/Java/Programação Reativa/10 - Spring WebFlux — o stack não-bloqueante sobre Netty e o DispatcherHandler|Spring WebFlux]]
- [[03-Dominios/Tecnologia/Java/Programação Reativa/09 - Backpressure — request(n) e as estratégias BUFFER, DROP, LATEST|Backpressure e o protocolo request(n)]]
- [[03-Dominios/Tecnologia/Java/Programação Reativa/index|Programação Reativa (MOC do galho)]]
- [[03-Dominios/Tecnologia/Java/index|Trilha Java]]
- [[03-Dominios/Tecnologia/Java/Dicionário de Java|Dicionário de Java]]

## Referências

- Project Reactor Reference — Reactive Programming: https://projectreactor.io/docs/core/release/reference/reactiveProgramming.html
- Project Reactor Reference — Core Features (subscribe, assembly vs subscription, cold vs hot): https://projectreactor.io/docs/core/release/reference/coreFeatures.html
- Project Reactor Reference — `subscribe()`: https://projectreactor.io/docs/core/release/reference/#reactive.subscribe
- Project Reactor Reference — Hot vs Cold: https://projectreactor.io/docs/core/release/reference/#reactor.hotCold
