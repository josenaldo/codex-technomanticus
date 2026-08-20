---
title: "Backpressure — request(n) e as estratégias BUFFER, DROP, LATEST"
created: 2026-06-10
updated: 2026-06-10
type: concept
progress: backlog
status: seedling
publish: true
fase: adepto
tags:
  - java
  - reativa
  - adepto
  - backpressure
  - reactive-streams
aliases:
  - "backpressure"
  - "request(n)"
---

# Backpressure — request(n) e as estratégias BUFFER, DROP, LATEST

> [!abstract] TL;DR
> **Backpressure** é o mecanismo do Reactive Streams onde o **consumidor controla a demanda** via `request(n)` — o produtor não empurra mais do que o consumidor aguenta. Em vez de o produtor jogar dados na cara do consumidor (push puro), o consumidor diz "me manda `n` itens", e o produtor só emite até esse limite. Quando o produtor é intrinsecamente mais rápido (um clique de mouse, um sensor, um socket), e não dá pra desacelerar a fonte, entram as **estratégias de overflow**: `onBackpressureBuffer` (guarda numa fila), `onBackpressureDrop` (descarta o que sobra), `onBackpressureLatest` (mantém só o mais recente) ou `onBackpressureError` (estoura na cara). Em `Flux.create`, a `OverflowStrategy` faz esse papel no momento da emissão. Escolher errado custa memória (`OutOfMemoryError`) ou dados perdidos silenciosamente.

## O que é

Backpressure é o protocolo de controle de fluxo embutido no [[03-Dominios/Tecnologia/Java/Programação Reativa/02 - Reactive Streams — a spec das 4 interfaces e o Flow do Java 9|Reactive Streams]]. A spec o descreve como "asynchronous stream processing with non-blocking back pressure": o objetivo é "govern the exchange of stream data across an asynchronous boundary" de modo que "the receiving side is not forced to buffer arbitrary amounts of data".

Traduzindo: numa fronteira assíncrona (threads diferentes, rede, fila), o lado que **recebe** não pode ser obrigado a engolir tudo que o lado que **produz** despeja. O receptor precisa de uma alavanca pra dizer "espera, eu só consigo processar `n` por enquanto". Essa alavanca é o método `Subscription.request(n)`.

A sacada é que backpressure aqui é **non-blocking**: o consumidor não trava a thread do produtor enquanto processa. Ele sinaliza demanda de forma assíncrona — pede `n`, processa, pede mais. A spec é explícita: "the communication of back pressure" deve ser "fully non-blocking and asynchronous", porque backpressure síncrono (tipo um `Thread.sleep` no produtor) jogaria fora os ganhos do modelo assíncrono.

## Por que importa

Sem backpressure, um produtor rápido + consumidor lento tem só dois finais ruins:

1. **Buffer ilimitado** — você guarda tudo que chega numa fila esperando processar, e a fila cresce até `OutOfMemoryError`. É a falha clássica de pipelines que "funcionam em dev" e caem em produção sob carga.
2. **Perda descontrolada** — você descarta o excesso, mas sem um contrato explícito de _o quê_ e _quando_ descartar, perde dados de forma imprevisível.

Backpressure transforma essa escolha implícita e perigosa numa **decisão de design explícita**. Você declara no pipeline: "se o consumidor não acompanhar, eu faço X". X é uma das estratégias de overflow. O sistema fica previsível: ou ele segura a barra (buffer limitado), ou descarta com regra clara, ou falha rápido — mas nunca te surpreende com um OOM às 3 da manhã.

É também o que separa Reactive Streams de um `Stream` comum ou de um pub/sub ingênuo: o contrato de demanda é a feature central, não um detalhe.

## Como funciona

### `request(n)`: o consumidor controla a demanda (o produtor não empurra mais do que aguenta)

O `Subscriber` recebe um `Subscription` no `onSubscribe`. A partir daí, **nada é emitido** até o consumidor chamar `subscription.request(n)`. Esse `n` é um crédito: "estou autorizado a receber até `n` itens agora". O produtor emite no máximo `n` `onNext`, e então espera o próximo `request`.

```text
Consumidor                         Produtor
   |  onSubscribe(subscription)       |
   |--------------------------------->|
   |  request(2)                      |
   |--------------------------------->|
   |              onNext(A)           |
   |<---------------------------------|
   |              onNext(B)           |
   |<---------------------------------|   (parou: crédito esgotado)
   |  request(2)                      |
   |--------------------------------->|
   |              onNext(C)           |
   |<---------------------------------|
```

O fluxo é **pull-based na sinalização, push-based na entrega**: o consumidor _puxa_ permissão, o produtor _empurra_ até o limite dado. `request(Long.MAX_VALUE)` é o caso "demanda ilimitada" — equivale a desligar backpressure (você confia que ninguém vai te afogar).

Operadores como `limitRate(n)` no Reactor exploram isso: em vez de pedir `Long.MAX_VALUE`, o operador pede em lotes de `n`, criando backpressure mesmo quando o consumidor final pediria tudo.

### Overflow: produtor mais rápido que o consumidor

`request(n)` resolve o caso onde o produtor **consegue** desacelerar — um banco de dados paginando resultados, um arquivo sendo lido linha a linha. O produtor simplesmente para de ler até receber mais crédito.

O problema difícil é a fonte que **não dá pra frear**: cliques de mouse, ticks de um sensor, mensagens chegando num socket TCP, eventos de um WebSocket. Esses eventos acontecem no tempo do mundo real, não no tempo do consumidor. Se o consumidor pediu 2 e chegaram 50, sobram 48 sem crédito. Isso é **overflow**: sinais emitidos além da demanda corrente.

Aqui o `request(n)` sozinho não basta — você precisa decidir o destino do excedente. Essa decisão é a estratégia de overflow.

### Estratégias: `onBackpressureBuffer`/`Drop`/`Latest`/`Error`

No Project Reactor, operadores `onBackpressure*` interceptam o que excede a demanda downstream:

- **`onBackpressureBuffer`** — guarda o excedente numa fila e entrega quando o consumidor pedir mais. Sem argumento, a fila é **ilimitada** (risco de OOM). Com `onBackpressureBuffer(maxSize)`, a fila é limitada e você define o que fazer ao estourar (erro ou descarte, dependendo da sobrecarga do método).
- **`onBackpressureDrop`** — descarta silenciosamente o que excede a demanda. Há a sobrecarga `onBackpressureDrop(consumer)` que te dá um callback pra _logar_ ou contabilizar cada item dropado (use sempre).
- **`onBackpressureLatest`** — mantém só o **item mais recente** e descarta os anteriores não consumidos. Ideal pra "estado atual" (último preço, última posição do cursor) onde valores velhos não importam.
- **`onBackpressureError`** — sinaliza um erro (`IllegalStateException`, com mensagem de overflow) assim que houver overflow. Fail-fast: prefira isso a um OOM silencioso quando perder dado é inaceitável.

A escolha é semântica, não técnica: depende se o dado é **acumulável** (buffer), **descartável** (drop/latest) ou **crítico** (error).

### `Flux.create` com `FluxSink` e `OverflowStrategy`

Quando você faz a **ponte** de uma API assíncrona legada (um listener, um callback) pro mundo reativo, usa `Flux.create`. Ele te entrega um `FluxSink`, no qual você chama `sink.next(...)`, `sink.error(...)`, `sink.complete()` — de uma ou várias threads produtoras.

Como o `FluxSink` aceita emissões a qualquer momento (o mundo externo não respeita `request(n)`), você passa uma `OverflowStrategy` no segundo parâmetro:

```java
Flux.create(Consumer<FluxSink<T>>, OverflowStrategy)
```

Os valores do enum `FluxSink.OverflowStrategy` (conforme o Javadoc do Reactor):

| Strategy | Comportamento |
| --- | --- |
| `IGNORE` | Ignora completamente a demanda downstream. Pode resultar em `IllegalStateException` quando as filas internas enchem. |
| `ERROR` | Sinaliza `IllegalStateException` quando o downstream não acompanha. |
| `DROP` | Descarta o sinal recebido se o downstream não está pronto pra recebê-lo. |
| `LATEST` | O downstream recebe só os sinais mais recentes do upstream. |
| `BUFFER` (default) | Bufferiza todos os sinais se o downstream não acompanha — buffer **ilimitado**, risco de `OutOfMemoryError`. |

> [!note] Fronteira com o Galho 4 — Virtual Threads NÃO dão backpressure
> Os [[03-Dominios/Tecnologia/Java/Concorrência e paralelismo/12 - Virtual Threads e Project Loom|Virtual Threads e Project Loom]] (Java 21) resolvem o problema de _custo_ de blocking I/O — você pode ter milhões de threads baratas bloqueando sem pagar o preço das plataformas. Mas eles **não dão backpressure nativo**: se uma fonte rápida alimenta um consumidor lento, Virtual Threads não criam nenhum sinal de demanda pra frear a fonte — você ainda acumula trabalho (filas, tasks pendentes) até estourar. Esse é justamente um ponto onde o modelo reativo ainda vence: o `request(n)` é parte do contrato. O confronto detalhado está em [[03-Dominios/Tecnologia/Java/Programação Reativa/14 - Reativo vs Virtual Threads — o confronto honesto|Reativo vs Virtual Threads]].

## Na prática

Cenário: um feed externo de eventos de pedidos (`Order`) chega por um listener que não respeita demanda. Fazemos a ponte com `Flux.create` e estratégia `DROP` — se o consumidor não acompanhar, perdemos o evento (aceitável para telemetria, não para cobrança).

```java
import reactor.core.publisher.Flux;
import reactor.core.publisher.FluxSink;

Flux<Order> orders = Flux.create(sink -> {
    OrderFeed feed = new OrderFeed();
    feed.onEvent(order -> sink.next(order));   // produtor externo, sem request(n)
    feed.onClose(() -> sink.complete());
    feed.onFailure(sink::error);
    sink.onCancel(feed::close);                // libera o recurso ao cancelar
}, FluxSink.OverflowStrategy.DROP);             // excedente é descartado
```

Cenário alternativo: um stream rápido onde queremos **segurar** o excedente numa fila limitada de 1000, em vez de descartar — e processar item a item devagar.

```java
import reactor.core.publisher.Flux;
import java.time.Duration;

Flux<Customer> fast = customerSource()                 // emite muito rápido
    .onBackpressureBuffer(1000)                         // fila limitada: 1000
    .delayElements(Duration.ofMillis(50));              // consumidor lento

fast.subscribe(customer -> process(customer));
// Ao passar de 1000 itens em espera, o pipeline sinaliza overflow
// (em vez de crescer até OutOfMemoryError, como faria o buffer default).
```

E o que `request(n)` faz no caso de uma fonte que _respeita_ demanda — um repositório paginado de `Product`:

```text
request(10)  -->  emite Product[1..10]   -->  consumidor processa
request(10)  -->  emite Product[11..20]  -->  consumidor processa
                  (produtor só busca a próxima página quando há crédito)
```

A fonte nunca carrega o catálogo inteiro na memória: ela busca exatamente o que foi pedido.

## Armadilhas

### (1) Produtor rápido + consumidor lento sem estratégia nenhuma

Sem declarar overflow, o default de muitos caminhos (incluindo `Flux.create` sem strategy explícita e `onBackpressureBuffer()` sem limite) é **bufferizar de forma ilimitada**. Sob carga sustentada, a fila cresce até `OutOfMemoryError` — e some em testes de dev, onde a carga é baixa.

```java
// Armadilha: buffer ilimitado escondido
Flux<Order> bomb = Flux.create(sink ->
    feed.onEvent(sink::next)
);  // sem OverflowStrategy -> BUFFER ilimitado por padrão
```

**Fix:** seja explícito sobre o limite e a política. Use `onBackpressureBuffer(maxSize)` ou passe uma `OverflowStrategy` adequada (ou um buffer limitado com `onBackpressureBuffer(maxSize, dropHandler)`).

```java
Flux<Order> safe = Flux.create(sink ->
    feed.onEvent(sink::next),
    FluxSink.OverflowStrategy.LATEST   // ou DROP/ERROR, conforme a semântica
);
```

### (2) `onBackpressureDrop` perdendo dados sem ninguém perceber

`onBackpressureDrop` sem argumento descarta em silêncio. Você ganha estabilidade de memória, mas perde observabilidade: ninguém sabe quantos eventos sumiram, nem quais. Em telemetria pode passar; em pedidos ou pagamentos, é incidente.

```java
// Armadilha: descarte invisível
Flux<Order> lossy = orders.onBackpressureDrop();
```

**Fix:** use a sobrecarga com callback pra logar/metrificar cada item dropado — e questione se `DROP` é mesmo a política certa pra esse dado.

```java
Flux<Order> observed = orders.onBackpressureDrop(dropped ->
    log.warn("Order descartado por backpressure: {}", dropped.id())
);
```

### (3) Ignorar backpressure num `Flux.create` (push sem demanda)

Usar `OverflowStrategy.IGNORE` (ou tratar o `sink` como se demanda não existisse) faz o produtor empurrar tudo independente do consumidor. O Javadoc é claro: `IGNORE` "completely ignore downstream backpressure requests" e pode resultar em `IllegalStateException` quando as filas internas enchem. Você troca um OOM por uma exceção tardia e confusa, sem nenhum controle de fluxo real.

```java
// Armadilha: empurrar sem respeitar demanda
Flux<Product> push = Flux.create(sink -> {
    for (Product p : hugeCatalog()) sink.next(p);   // despeja tudo de uma vez
}, FluxSink.OverflowStrategy.IGNORE);
```

**Fix:** respeite a demanda com `sink.onRequest(n -> ...)` (modelo híbrido push/pull, em que você só emite `n` por vez) ou escolha uma estratégia de overflow real (`BUFFER` limitado, `DROP`, `LATEST`, `ERROR`).

```java
Flux<Product> demandAware = Flux.create(sink ->
    sink.onRequest(n -> emitUpTo(sink, n)),          // só emite o que foi pedido
    FluxSink.OverflowStrategy.ERROR
);
```

## Em entrevista

### Frase pronta (inglês)

> Backpressure is the flow-control contract at the heart of Reactive Streams: instead of a producer pushing data at whatever rate it wants, the consumer signals demand through `Subscription.request(n)`, so the producer never emits more than the consumer asked for. When the source is inherently faster and can't be slowed down — like socket events or sensor ticks — you can't rely on demand alone, so you pick an overflow strategy: buffer the excess, drop it, keep only the latest value, or fail fast with an error. The dangerous default is an unbounded buffer, which trades a clear design decision for an `OutOfMemoryError` under load, so I always make the strategy explicit and log anything I drop.

### Vocabulário

| Termo PT | Termo EN |
| --- | --- |
| contrapressão / backpressure | backpressure |
| demanda | demand |
| sinalizar demanda | signal demand |
| controle de fluxo | flow control |
| transbordamento / excedente | overflow |
| buffer ilimitado | unbounded buffer |
| descartar (dados) | drop / discard |
| falhar rápido | fail fast |
| fonte rápida / produtor rápido | fast producer / fast source |

## Veja também

- [[03-Dominios/Tecnologia/Java/Programação Reativa/02 - Reactive Streams — a spec das 4 interfaces e o Flow do Java 9|Reactive Streams]]
- [[03-Dominios/Tecnologia/Java/Programação Reativa/08 - Schedulers — subscribeOn, publishOn e em qual thread o código roda|Schedulers]]
- [[03-Dominios/Tecnologia/Java/Programação Reativa/14 - Reativo vs Virtual Threads — o confronto honesto|Reativo vs Virtual Threads]]
- [[03-Dominios/Tecnologia/Java/Concorrência e paralelismo/12 - Virtual Threads e Project Loom|Virtual Threads e Project Loom]]
- [[03-Dominios/Tecnologia/Java/Programação Reativa/index|Programação Reativa (MOC do galho)]]
- [[03-Dominios/Tecnologia/Java/index|Trilha Java]]
- [[03-Dominios/Tecnologia/Java/Dicionário de Java|Dicionário de Java]]

## Referências

- Reactive Streams — especificação oficial: https://www.reactive-streams.org/
- Project Reactor — Reference Guide, "Programmatically creating a sequence" (Flux.create, FluxSink, OverflowStrategy): https://projectreactor.io/docs/core/release/reference/
- Project Reactor — Javadoc `FluxSink.OverflowStrategy`: https://projectreactor.io/docs/core/release/api/reactor/core/publisher/FluxSink.OverflowStrategy.html
