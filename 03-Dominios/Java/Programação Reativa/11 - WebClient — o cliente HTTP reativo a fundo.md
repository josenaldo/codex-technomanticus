---
title: "WebClient — o cliente HTTP reativo a fundo"
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
  - webclient
  - webflux
aliases:
  - "WebClient"
---

# WebClient — o cliente HTTP reativo a fundo

> [!abstract] TL;DR
> `WebClient` é o cliente HTTP **não-bloqueante** do WebFlux, com a API *fluent* `get().uri().retrieve().bodyToMono(...)`. Ele é o **par reativo** do `RestClient` síncrono (Galho 9): mesma cara, modelo de execução oposto. A chamada não devolve o objeto pronto — devolve um `Mono<T>` (zero-ou-um) ou `Flux<T>` (zero-ou-muitos) que só dispara o request no `subscribe`. Use `WebClient` quando você está num stack reativo de ponta a ponta; num serviço **MVC imperativo**, `WebClient` + `.block()` é o **pior dos dois mundos** — paga a complexidade do reativo sem ganhar nada — e ali o certo é o `RestClient`. A regra prática: o `WebClient` é *thread-safe*, crie **um** e reuse.

## O que é

`WebClient` é o cliente HTTP reativo do Spring Framework, parte do módulo WebFlux. A documentação o descreve como uma interface não-bloqueante e reativa para executar requisições HTTP, construída sobre o Project Reactor (`Mono`/`Flux`).

Ele expõe uma API *fluent*: você encadeia o verbo (`get()`, `post()`, `put()`, `delete()`, `patch()`), a URI, os cabeçalhos e o corpo, e termina decidindo **como consumir a resposta** — via `retrieve()` (caminho simples) ou `exchangeToMono()`/`exchangeToFlux()` (controle total sobre a `ClientResponse`). O resultado nunca é o objeto cru: é um *publisher* que só executa o request quando alguém se inscreve.

A criação tem duas portas: o atalho estático `WebClient.create()` (ou `WebClient.create("https://...")`) e o `WebClient.builder()`, recomendado quando você precisa configurar `baseUrl`, cabeçalhos default, codecs ou filtros.

## Por que importa

Quase todo serviço moderno é, no fundo, um **orquestrador de outros serviços** por HTTP. Como você faz essas chamadas define o modelo de concorrência da aplicação inteira. Num stack reativo (Galho 10), o `WebClient` é o que mantém a promessa de ponta a ponta: a chamada de saída também é não-bloqueante, então o *event loop* dispara o request e fica livre para atender outras requisições enquanto a resposta não chega.

O erro caro é o inverso: usar `WebClient` num serviço imperativo e fechar a chamada com `.block()`. Aí você paga **toda** a ceticidade do reativo — operadores, *schedulers*, *publishers* — só pra, no fim, bloquear a thread como se fosse um cliente síncrono qualquer. É o **pior dos dois mundos**, e foi exatamente esse buraco que o `RestClient` (Spring 6.1, Galho 9) veio tapar: a mesma API *fluent*, mas síncrona de verdade, sem `Mono`/`Flux` no caminho.

Em entrevista, saber **quando não usar** `WebClient` vale mais que decorar a API. A pergunta que separa os candidatos é: "seu serviço é MVC ou WebFlux?" — porque a resposta dita qual cliente é o certo.

## Como funciona

### `WebClient`: o cliente HTTP não-bloqueante do WebFlux

O `WebClient` é a contraparte de saída do WebFlux. Onde o `DispatcherHandler` (Galho 10) recebe requisições sem bloquear o *event loop*, o `WebClient` **emite** requisições com a mesma disciplina. Ele reaproveita a mesma infraestrutura de codecs (Jackson para JSON, por exemplo) do lado servidor.

A construção típica usa o *builder*:

```java
import org.springframework.web.reactive.function.client.WebClient;

WebClient webClient = WebClient.builder()
    .baseUrl("https://orders.internal")
    .defaultHeader("Accept", "application/json")
    .build();
```

Ponto crítico: o `WebClient` é **imutável e thread-safe**. Uma vez configurado, ele pode ser compartilhado por toda a aplicação — tipicamente como um `@Bean` único. Recriá-lo a cada chamada desperdiça recursos (ver Armadilhas).

### `retrieve()` + `bodyToMono`/`bodyToFlux`: consumindo a resposta

O caminho mais comum é `retrieve()`, que dá acesso direto ao corpo da resposta sem expor a `ClientResponse` inteira. Depois dele você escolhe a cardinalidade:

- `bodyToMono(Tipo.class)` — quando a resposta é **um** recurso (ou nenhum): devolve `Mono<T>`.
- `bodyToFlux(Tipo.class)` — quando a resposta é uma **coleção** ou um *stream*: devolve `Flux<T>`.

```java
import reactor.core.publisher.Mono;
import reactor.core.publisher.Flux;

Mono<OrderDto> order = webClient.get()
    .uri("/orders/{id}", id)
    .retrieve()
    .bodyToMono(OrderDto.class);

Flux<OrderDto> orders = webClient.get()
    .uri("/orders")
    .retrieve()
    .bodyToFlux(OrderDto.class);
```

Lembre do Galho 4: nada acontece até o `subscribe`. Esses `Mono`/`Flux` são receitas frias — o request HTTP só sai quando o WebFlux (ou um `.block()`) se inscrever.

Quando você precisa do controle total — inspecionar status, cabeçalhos e corpo juntos — existe o `exchangeToMono()` / `exchangeToFlux()`, que entrega a `ClientResponse` na sua mão. É mais poderoso e mais perigoso: você fica responsável por **sempre** consumir o corpo, senão vaza conexão.

### Error handling: `onStatus` (HTTP de erro vira `WebClientResponseException`)

Por padrão, `retrieve()` trata qualquer status **4xx ou 5xx** como erro, propagando um sinal `onError` com uma `WebClientResponseException` (que carrega o status, o texto e o corpo da resposta de erro). Você captura isso com os operadores reativos do Galho 7 — `onErrorResume`, `onErrorReturn`, `retry`.

O `onStatus` permite **interceptar faixas de status antes** de virarem exceção genérica, mapeando cada caso para um erro de domínio:

```java
import org.springframework.web.reactive.function.client.WebClientResponseException;

Mono<OrderDto> order = webClient.get()
    .uri("/orders/{id}", id)
    .retrieve()
    .onStatus(
        status -> status.value() == 404,
        response -> Mono.error(new OrderNotFoundException(id)))
    .bodyToMono(OrderDto.class);
```

### Streaming de respostas (`bodyToFlux` + `text/event-stream`)

`bodyToFlux` não serve só para coleções JSON — ele brilha em **streams contínuos**. Quando o servidor responde com `text/event-stream` (Server-Sent Events), o WebFlux entrega cada evento **assim que chega**, sem esperar o corpo inteiro. O `Flux` emite item a item, com *backpressure* (Galho 9) regulando o ritmo:

```java
Flux<OrderEvent> events = webClient.get()
    .uri("/orders/{id}/events", id)
    .accept(org.springframework.http.MediaType.TEXT_EVENT_STREAM)
    .retrieve()
    .bodyToFlux(OrderEvent.class);
```

Isso é impossível num cliente síncrono: um `RestClient` precisa do corpo completo antes de devolver. O *streaming* incremental é uma capacidade exclusiva do modelo reativo.

### vs `RestClient` síncrono (Galho 9 nota 15 — mesma API fluent, modelo oposto)

O `RestClient` (Spring 6.1) foi desenhado para ter **a mesma API *fluent*** do `WebClient` — `get().uri().retrieve()` —, mas com modelo de execução **oposto**: ele **bloqueia** e devolve o objeto cru, não um *publisher*.

| Aspecto | `WebClient` | `RestClient` (Galho 9) |
|---|---|---|
| Modelo | Não-bloqueante (reativo) | Síncrono (bloqueante) |
| Retorno | `Mono<T>` / `Flux<T>` | `T` direto (`.body(Tipo.class)`) |
| Stack ideal | WebFlux (Galho 10) | MVC imperativo |
| Streaming incremental | Sim (`bodyToFlux` + SSE) | Não |

A escolha não é de gosto: ela segue o stack. Reativo de ponta a ponta → `WebClient`. Serviço MVC → `RestClient`. O detalhe sobre o `RestClient` em si está no Galho 9 nota 15 — aqui só contrastamos.

## Na prática

```java
import org.springframework.web.reactive.function.client.WebClient;
import org.springframework.web.reactive.function.client.WebClientResponseException;
import org.springframework.http.MediaType;
import reactor.core.publisher.Mono;
import reactor.core.publisher.Flux;

// Um WebClient compartilhado, criado uma vez (thread-safe).
WebClient webClient = WebClient.builder()
    .baseUrl("https://orders.internal")
    .build();

// 1. Buscar um pedido por id -> Mono<OrderDto>
Mono<OrderDto> order = webClient.get()
    .uri("/orders/{id}", id)
    .retrieve()
    .bodyToMono(OrderDto.class);

// 2. Streaming de eventos do pedido via SSE -> Flux<OrderEvent>
Flux<OrderEvent> events = webClient.get()
    .uri("/orders/{id}/events", id)
    .accept(MediaType.TEXT_EVENT_STREAM)
    .retrieve()
    .bodyToFlux(OrderEvent.class);

// 3. Tratar 404 como erro de domínio antes de desserializar o corpo
Mono<CustomerDto> customer = webClient.get()
    .uri("/customers/{id}", customerId)
    .retrieve()
    .onStatus(
        status -> status.value() == 404,
        response -> Mono.error(new CustomerNotFoundException(customerId)))
    .bodyToMono(CustomerDto.class);
```

Repare: nenhum `.block()`. Esses `Mono`/`Flux` são devolvidos a montante (a um controller WebFlux, por exemplo) e subscritos pelo framework. O dia em que você sente a tentação de chamar `.block()` aqui é o dia de perguntar se não era pra ser um `RestClient`.

## Armadilhas

### (1) `WebClient` + `.block()` num serviço MVC

Usar `WebClient` num controller Spring MVC e fechar com `.block()` para extrair o valor é o **pior dos dois mundos**: você importa toda a maquinaria reativa (operadores, *schedulers*, alocação de *publishers*) e ainda assim **bloqueia a thread** no fim, exatamente como um cliente síncrono — sem nenhum ganho de concorrência.

```java
// Anti-padrão num @RestController MVC:
OrderDto order = webClient.get()
    .uri("/orders/{id}", id)
    .retrieve()
    .bodyToMono(OrderDto.class)
    .block();   // bloqueia a thread; toda a complexidade reativa virou pura perda
```

**Fix:** num stack imperativo, use o `RestClient` (Galho 9 nota 15) — mesma API *fluent*, mas síncrono de verdade, sem `Mono`/`Flux` no caminho. Reserve o `WebClient` para quem está em WebFlux de ponta a ponta.

### (2) Não tratar `onStatus`: erro HTTP vira exceção tarde e genérica

Sem um `onStatus`, um `404` ou `500` do serviço de destino vira uma `WebClientResponseException` genérica que só estoura **lá na frente**, quando o `Mono` é subscrito — longe do ponto onde você sabia o que aquele status significava no domínio.

```java
// Sem tratamento: o 404 vira WebClientResponseException crua,
// e o chamador não distingue "pedido não existe" de "serviço caiu".
Mono<OrderDto> order = webClient.get()
    .uri("/orders/{id}", id)
    .retrieve()
    .bodyToMono(OrderDto.class);
```

**Fix:** mapeie os status relevantes com `onStatus` para erros de domínio, e combine com os operadores do Galho 7 (`onErrorResume`, `retry`) para a política de recuperação:

```java
Mono<OrderDto> order = webClient.get()
    .uri("/orders/{id}", id)
    .retrieve()
    .onStatus(s -> s.value() == 404,
        resp -> Mono.error(new OrderNotFoundException(id)))
    .bodyToMono(OrderDto.class);
```

### (3) Recriar o `WebClient` a cada chamada

O `WebClient` é **imutável e thread-safe**: ele foi feito para ser configurado uma vez e reusado por toda a aplicação. Recriá-lo dentro de cada método de serviço desperdiça a configuração de codecs, conexões e filtros a cada request.

```java
// Anti-padrão: um WebClient novo por chamada.
public Mono<OrderDto> findOrder(String id) {
    return WebClient.create("https://orders.internal")   // recriado toda vez
        .get().uri("/orders/{id}", id)
        .retrieve()
        .bodyToMono(OrderDto.class);
}
```

**Fix:** declare **um** `WebClient` como `@Bean` (ou campo `final` construído uma vez) e injete onde precisar:

```java
@Bean
WebClient ordersWebClient(WebClient.Builder builder) {
    return builder.baseUrl("https://orders.internal").build();
}
```

## Em entrevista

### Frase pronta (inglês)

> `WebClient` is the non-blocking HTTP client from WebFlux, and it mirrors the fluent API of the synchronous `RestClient` introduced in Spring 6.1, but with the opposite execution model — every call returns a `Mono` or a `Flux` instead of the raw object. I reach for `WebClient` only when the service is reactive end to end; in a plain Spring MVC service, wrapping a `WebClient` call in `.block()` is the worst of both worlds, so there I use `RestClient`. A couple of details I always get right: I create a single, thread-safe `WebClient` and reuse it, I handle error statuses with `onStatus` so a `404` maps to a domain error instead of leaking a generic `WebClientResponseException`, and for `text/event-stream` I use `bodyToFlux` to consume events as they arrive.

### Vocabulário

| Termo PT | Termo EN |
|---|---|
| cliente HTTP não-bloqueante | non-blocking HTTP client |
| API fluente | fluent API |
| corpo da resposta | response body |
| tratamento de erro | error handling |
| status de erro HTTP | HTTP error status |
| seguro para múltiplas threads | thread-safe |
| streaming de eventos | event streaming |
| pior dos dois mundos | worst of both worlds |

## Veja também

- [[03-Dominios/Java/Programação Reativa/10 - Spring WebFlux — o stack não-bloqueante sobre Netty e o DispatcherHandler|Spring WebFlux]]
- [[03-Dominios/Java/Programação Reativa/07 - Error handling reativo — onErrorResume, onErrorReturn, retry|Error handling reativo]]
- [[03-Dominios/Java/Web e APIs REST/15 - Clientes HTTP — RestClient, WebClient, RestTemplate|Clientes HTTP (RestClient vs WebClient)]]
- [[03-Dominios/Java/Programação Reativa/index|Programação Reativa (MOC do galho)]]
- [[03-Dominios/Java/index|Trilha Java]]
- [[03-Dominios/Java/Dicionário de Java|Dicionário de Java]]

## Referências

- Spring Framework Reference — Web on Reactive Stack, WebClient: https://docs.spring.io/spring-framework/reference/web/webflux-webclient.html
