---
title: "Error handling reativo — onErrorResume, onErrorReturn, retry"
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
  - operadores
aliases:
  - "error handling reativo"
  - "onErrorResume"
---

# Error handling reativo — onErrorResume, onErrorReturn, retry

> [!abstract] TL;DR
> No mundo reativo o erro é um **sinal terminal**: assim que ele acontece, o `onError` encerra a sequência e nada mais é emitido nesse fluxo. A recuperação é **declarativa**, montada na própria cadeia com `onErrorReturn` (valor fixo), `onErrorResume` (outro publisher), `onErrorMap` (traduzir a exceção) e `retry`/`retryWhen` (re-subscribe, idealmente com backoff). Um `try/catch` em volta da cadeia **não pega** o sinal reativo — ele só captura exceções lançadas na thread durante a montagem, não o `onError` que viaja pelo fluxo assíncrono.

## O que é

Error handling reativo é o conjunto de operadores que o Project Reactor oferece para interceptar, transformar ou recuperar de um **sinal de erro** (`onError`) que percorre a cadeia de `Mono`/`Flux`.

Em Reactive Streams existem três sinais terminais possíveis num fluxo: `onComplete` (terminou com sucesso), `onError` (terminou com falha) e o cancelamento pelo subscriber. O `onError` é mutuamente exclusivo com `onComplete` — um fluxo termina de exatamente uma dessas formas. Quando um operador encontra um problema (uma exceção lançada dentro de um `map`, uma falha de rede num `WebClient`, um timeout), ele converte isso num sinal `onError` que desce pela cadeia até o subscriber, **interrompendo a emissão de qualquer item adicional**.

Os operadores de recuperação não "consertam" o fluxo original que falhou: eles o **substituem** por um fluxo de fallback a partir do ponto em que foram declarados.

## Por que importa

Quem vem do mundo imperativo tende a embrulhar a cadeia reativa num `try/catch` e se frustra: o bloco nunca dispara. Isso acontece porque a cadeia é **assíncrona e lazy** — a falha não sobe pela pilha de chamadas, ela viaja como dado pelo fluxo. Entender que o erro é um sinal, e não uma exceção propagada pela stack, é o divisor de águas entre escrever código reativo robusto e código que silenciosamente engole falhas.

Numa entrevista de backend sênior, error handling reativo é onde se separa quem "usou WebFlux uma vez" de quem entende o modelo. Saber escolher entre `onErrorReturn` e `onErrorResume`, justificar por que `retry()` sem backoff é perigoso, e explicar a fronteira entre o tratamento na cadeia (WebFlux) e o `@ControllerAdvice` imperativo (Spring MVC) demonstra domínio real do paradigma.

## Como funciona

### O erro é um sinal terminal (`onError` encerra o fluxo)

Em Reactive Streams, erros são eventos terminais. Assim que um erro ocorre, ele **para a sequência** e se propaga cadeia abaixo, operador por operador, até o último passo — o `Subscriber`. Depois de um `onError`, o publisher não emite mais nada: nem `onNext`, nem `onComplete`.

Por isso os operadores de erro não retomam a sequência original — eles a **trocam** por uma sequência de fallback. No `subscribe`, o segundo argumento (após o consumidor de `onNext`) é justamente o handler de erro:

```java
Flux.just(1, 2, 0)
    .map(i -> "100 / " + i + " = " + (100 / i))
    .subscribe(
        value -> System.out.println("RECEBIDO " + value),
        error -> System.err.println("CAPTUREI " + error) // handler de onError
    );
```

A divisão por zero vira um `onError`; o `Flux` emite os dois primeiros resultados e então termina pelo ramo de erro.

### Recuperação declarativa: `onErrorReturn`, `onErrorResume`, `onErrorMap`

Três operadores cobrem a maioria dos casos de recuperação, e cada um tem um propósito distinto:

- **`onErrorReturn(valor)`** — substitui o erro por um único **valor fixo** de fallback. Aceita predicado ou tipo de exceção para recuperar só de certos erros. Use quando há um default estático e barato.
- **`onErrorResume(fn)`** — troca para uma **sequência alternativa** (outro `Publisher`). A função recebe a exceção e devolve um `Mono`/`Flux`, permitindo escolher a estratégia de recuperação dinamicamente (ex: cair num cache, devolver `Mono.empty()`, ou re-lançar outra coisa). É o mais poderoso.
- **`onErrorMap(fn)`** — **traduz** a exceção antes de propagá-la cadeia abaixo, sem recuperar. Útil para embrulhar uma `IOException` de baixo nível numa exceção de domínio.

```java
// valor fixo
fluxArriscado.onErrorReturn("RECUPERADO");

// sequência alternativa (cache) por tipo de exceção
chamarServico(key).onErrorResume(e -> buscarNoCache(key));

// traduzir a exceção
chamarServico(key).onErrorMap(e -> new BusinessException("SLA estourado", e));
```

### `retry`/`retryWhen` com backoff: re-subscribe

`retry(n)` reage ao `onError` **re-inscrevendo-se** na fonte upstream, até `n` vezes. Importante: cada tentativa cria uma **nova subscription** — uma sequência fresca, não a continuação da anterior. Em fontes cold isso refaz o trabalho do zero.

`retryWhen(retrySpec)` é a versão avançada: recebe uma `Retry` strategy que decide quando (e se) re-inscrever, com base num companion `Flux<RetrySignal>` carregando metadados de cada falha. É aqui que entra o **backoff exponencial** via `Retry.backoff(maxTentativas, duracaoMinima)`, que espalha as re-tentativas no tempo em vez de martelar o serviço imediatamente:

```java
import reactor.util.retry.Retry;
import java.time.Duration;

fluxComErro.retryWhen(Retry.backoff(3, Duration.ofMillis(100)));
```

A `Retry` strategy também suporta filtrar por tipo de exceção, executar efeitos colaterais antes/depois de cada retry, e o modo `transientErrors(true)`, que reseta a contagem após uma recuperação bem-sucedida — ideal para rajadas de erros independentes.

### `try/catch` não pega o sinal reativo (e por quê)

Um `try/catch` tradicional **não intercepta** o sinal de erro reativo porque os dois operam em modelos de execução diferentes. A cadeia reativa é assíncrona e **lazy**: o `try/catch` envolve apenas a fase de **montagem** (assembly) da cadeia, que roda na thread atual. Mas a falha real acontece depois, durante a **subscription**, possivelmente em outra thread, e se propaga pelo callback `onError` — não pela pilha de chamadas.

```java
// NÃO funciona: o catch nunca dispara
try {
    Flux.just(1, 2, 0)
        .map(i -> 100 / i)
        .subscribe(System.out::println);
} catch (ArithmeticException e) {
    // morto: o erro virou sinal onError, não exceção na stack
}
```

O lugar de tratar é na própria cadeia (`onError*`) ou no handler de erro do `subscribe`.

> [!info] Fronteira com o Galho 9 (Spring MVC)
> No **Spring MVC** (imperativo), o tratamento de exceções da camada web é centralizado num `@ControllerAdvice` com métodos `@ExceptionHandler` — veja [[03-Dominios/Java/Web e APIs REST/01 - O que é Spring MVC — a camada web sobre o container|O que é Spring MVC]] e o galho de tratamento de exceções imperativo. No **WebFlux** (reativo), o erro vive na própria cadeia (`onError*`) ou é tratado por um `WebExceptionHandler` global. São modelos distintos: aqui tratamos o lado reativo; não re-explicamos o handling imperativo.

## Na prática

Cenário neutro: buscar um `Order` num serviço HTTP via `WebClient`, tolerando "não encontrado" como vazio e re-tentando falhas transientes com backoff.

```java
import reactor.core.publisher.Mono;
import reactor.util.retry.Retry;
import java.time.Duration;

public Mono<Order> buscarPedido(String orderId) {
    return webClient.get()
        .uri("/orders/{id}", orderId)
        .retrieve()
        .bodyToMono(Order.class)
        // 404 do serviço vira "pedido inexistente" => Mono vazio
        .onErrorResume(NotFoundException.class, e -> Mono.empty())
        // re-tenta falhas transientes com backoff exponencial (3x, base 200ms)
        .retryWhen(Retry.backoff(3, Duration.ofMillis(200)))
        // observa qualquer erro que sobreviva sem alterar o fluxo
        .doOnError(e -> log.error("Falha ao buscar pedido {}", orderId, e));
}
```

E uma variante para `Flux`, montando uma lista de produtos com fallback estático:

```java
import reactor.core.publisher.Flux;

public Flux<Product> catalogo(Customer customer) {
    return produtoService.recomendados(customer)
        .onErrorReturn(Product.indisponivel()) // default barato se a recomendação falhar
        .doOnError(e -> log.warn("Recomendações indisponíveis para {}", customer.id()));
}
```

## Armadilhas

### (1) `try/catch` em volta de uma cadeia reativa

Embrulhar a montagem da cadeia num `try/catch` esperando capturar a falha do fluxo. O bloco roda na thread de montagem e termina antes da subscription real; o erro vira sinal `onError` e escapa pelo callback, nunca pela stack.

```java
// errado
try {
    return webClient.get().uri("/orders/{id}", id)
        .retrieve().bodyToMono(Order.class);
} catch (Exception e) {
    return Mono.empty(); // nunca executa
}
```

**Fix:** trate dentro da cadeia.

```java
// certo
return webClient.get().uri("/orders/{id}", id)
    .retrieve().bodyToMono(Order.class)
    .onErrorResume(e -> Mono.empty());
```

### (2) `retry()` infinito (ou sem backoff) que martela o serviço

Chamar `retry()` sem argumento (re-tentativa infinita) ou `retry(n)` sem espaçamento re-inscreve imediatamente após cada falha. Contra um serviço já sobrecarregado, isso vira uma tempestade de re-tentativas que piora o incidente (retry storm).

```java
// errado: re-tenta sem parar e sem pausa
chamarServico(id).retry();
```

**Fix:** use `retryWhen` com `Retry.backoff`, que limita as tentativas e espalha no tempo.

```java
// certo
import reactor.util.retry.Retry;
import java.time.Duration;

chamarServico(id)
    .retryWhen(Retry.backoff(3, Duration.ofMillis(200)));
```

### (3) Engolir o erro com `onErrorReturn` sem observabilidade

Recuperar com `onErrorReturn(default)` e seguir em frente sem registrar nada. O fluxo fica verde, mas falhas reais (serviço caído, bug de serialização) desaparecem silenciosamente da telemetria, e o bug só aparece quando o default já contaminou os dados.

```java
// errado: falha some sem rastro
recomendados(customer).onErrorReturn(Product.indisponivel());
```

**Fix:** adicione `doOnError` (efeito colateral que observa sem interromper a propagação) antes de recuperar.

```java
// certo
recomendados(customer)
    .doOnError(e -> log.error("Recomendação falhou para {}", customer.id(), e))
    .onErrorReturn(Product.indisponivel());
```

## Em entrevista

### Frase pronta (inglês)

> In Reactor, an error is a **terminal signal**: the moment `onError` fires, the sequence stops and no further items are emitted on that flux. That's why a plain `try/catch` around a reactive chain never triggers — the failure travels through the `onError` callback, not up the call stack, so I recover declaratively with operators instead. I reach for `onErrorReturn` when a static fallback value is enough, `onErrorResume` when I need to switch to another publisher like a cache, and `onErrorMap` when I just want to wrap a low-level exception into a domain one. For transient failures I use `retryWhen(Retry.backoff(...))` rather than a bare `retry()`, because re-subscribing without backoff just hammers an already struggling service, and I always pair recovery with `doOnError` so I never swallow a failure silently.

### Vocabulário

| Termo PT | Termo EN |
| --- | --- |
| sinal terminal | terminal signal |
| sinal de erro | error signal |
| re-inscrever (re-subscribe) | re-subscribe |
| recuperação declarativa | declarative recovery |
| sequência de fallback | fallback sequence |
| recuo exponencial | exponential backoff |
| falha transiente | transient failure |
| tempestade de re-tentativas | retry storm |
| efeito colateral | side-effect |

## Veja também

- [[03-Dominios/Java/Programação Reativa/06 - Combinando publishers — zip, merge, concat, filter|Combinando publishers]]
- [[03-Dominios/Java/Programação Reativa/11 - WebClient — o cliente HTTP reativo a fundo|WebClient]]
- [[03-Dominios/Java/Web e APIs REST/01 - O que é Spring MVC — a camada web sobre o container|O que é Spring MVC]]
- [[03-Dominios/Java/Programação Reativa/index|Programação Reativa (MOC do galho)]]
- [[03-Dominios/Java/index|Trilha Java]]
- [[03-Dominios/Java/Dicionário de Java|Dicionário de Java]]

## Referências

- Project Reactor Reference Guide — Handling Errors: https://projectreactor.io/docs/core/release/reference/coreFeatures/error-handling.html
- Project Reactor — `reactor.util.retry.Retry` (backoff e retry specs): https://projectreactor.io/docs/core/release/api/reactor/util/retry/Retry.html
