---
title: "Spring WebFlux — o stack não-bloqueante sobre Netty e o DispatcherHandler"
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
  - webflux
aliases:
  - "Spring WebFlux"
  - "DispatcherHandler"
---

# Spring WebFlux — o stack não-bloqueante sobre Netty e o DispatcherHandler

> [!abstract] TL;DR
> WebFlux é o stack web **não-bloqueante** do Spring, rodando por padrão sobre **Netty** e um **event loop de poucos threads** — em vez do modelo *thread-per-request* do servlet (Galho 9). O coração é o `DispatcherHandler`, que faz o mesmo papel de *front controller* do `DispatcherServlet`, mas operando sobre `Mono`/`Flux` em vez de objetos prontos. Controllers `@RestController` mudam só o tipo de retorno: um endpoint devolve `Mono<OrderDto>` (zero-ou-um) ou `Flux<OrderDto>` (zero-ou-muitos), e o framework subscreve por você. A regra de ouro: **nunca bloquear o event loop** — um `.block()` ou um JDBC síncrono dentro do handler trava todas as requisições que compartilham aquele thread.

## O que é

Spring WebFlux é o módulo web reativo do Spring Framework, introduzido na versão 5.0 como alternativa ao Spring MVC. A documentação o descreve como **"fully non-blocking, supports Reactive Streams back pressure, and runs on such servers as Netty, and Servlet containers"** — totalmente não-bloqueante, com suporte a *back pressure* dos Reactive Streams, rodando sobre Netty ou containers servlet.

Ele expõe o mesmo modelo de programação anotado que você já conhece — `@RestController`, `@GetMapping`, `@PathVariable` — só que os métodos retornam **publishers** (`Mono<T>` ou `Flux<T>`, do Project Reactor) em vez de objetos de domínio crus. O starter é o `spring-boot-starter-webflux`, e a baseline atual é Spring Boot 3.x.

A peça central do despacho é o `DispatcherHandler`: o equivalente reativo do `DispatcherServlet` do Galho 9. Mesma responsabilidade (orquestrar a request), modelo de execução completamente diferente (assíncrono, não-bloqueante).

## Por que importa

O modelo servlet clássico amarra **uma thread por requisição** durante todo o ciclo de vida dela. Enquanto a request espera por I/O — uma query no banco, uma chamada HTTP a outro serviço — a thread fica **parada, ocupando memória**, sem fazer nada útil. Sob carga alta com muito I/O, o pool de threads esgota e novas requisições enfileiram, mesmo com a CPU ociosa.

WebFlux ataca exatamente esse desperdício. Com um **event loop de poucos threads**, uma única thread inicia centenas de operações de I/O e segue tratando outras requisições enquanto o sistema operacional cuida da espera. Quando o I/O completa, o resultado volta como um sinal reativo e a thread retoma o processamento. O ganho não é "responder uma request mais rápido" — é **sustentar muito mais requisições concorrentes** com bem menos threads. É uma escolha de **throughput sob I/O-bound**, não de latência por chamada.

Em entrevista, essa distinção separa quem decorou o nome do framework de quem entende o trade-off. WebFlux não é "Spring mais rápido"; é Spring com um modelo de concorrência diferente, que só compensa quando o gargalo é I/O e a concorrência é alta — e que cobra um preço alto de complexidade e de disciplina (não bloquear nunca).

## Como funciona

### Event loop (Netty, poucos threads) vs thread-per-request (servlet — Galho 9)

No stack imperativo do Galho 9, o container servlet (Tomcat por padrão) dedica **uma thread a cada request** do início ao fim. Se o handler chama o banco e espera 50 ms, a thread fica bloqueada 50 ms. Com 200 threads no pool, 200 requests simultâneas em espera já saturam o servidor.

WebFlux inverte isso. O servidor padrão é o **Netty**, construído sobre um **event loop** com um número pequeno e fixo de threads (tipicamente próximo ao número de núcleos). Cada thread do *loop* não fica presa a uma request: ela dispara a operação de I/O de forma não-bloqueante e **fica livre** para atender outra request enquanto a primeira aguarda. Quando o I/O completa, o evento é enfileirado de volta no *loop* e o processamento continua.

O efeito prático: poucos threads sustentam um volume de concorrência que exigiria centenas de threads no modelo servlet. O custo é que **qualquer bloqueio numa thread do event loop é catastrófico** — ela para de servir *todas* as requests que dependiam dela, não só a atual.

### `DispatcherHandler` vs `DispatcherServlet`: o mesmo papel, modelo diferente

O `DispatcherHandler` é o *front controller* do WebFlux. A documentação é explícita sobre o paralelo:

> Spring WebFlux, similarly to Spring MVC, is designed around the front controller pattern, where a central `WebHandler`, the `DispatcherHandler`, provides a shared algorithm for request processing, while actual work is performed by configurable, delegate components.

Mesmo desenho do `DispatcherServlet` (ver Galho 9): um ponto central que não faz o trabalho, e sim **delega a beans configuráveis**. O `DispatcherHandler` é declarado como um bean `WebHandler` de nome `webHandler`, descoberto pelo `WebHttpHandlerBuilder`. Ele orquestra três tipos de bean especiais:

- **`HandlerMapping`** — mapeia a request para um handler (controllers anotados, padrões de URL, etc.). O primeiro match vence.
- **`HandlerAdapter`** — invoca o handler escolhido sem que o `DispatcherHandler` precise saber *como* ele é chamado (resolver anotações, por exemplo). Expõe o retorno como um `HandlerResult`.
- **`HandlerResultHandler`** — processa o `HandlerResult` e finaliza a resposta, escrevendo direto ou renderizando uma view.

O fluxo, segundo a doc: cada `HandlerMapping` é consultado até achar um match; o handler é executado via `HandlerAdapter`, que expõe o retorno como `HandlerResult`; o `HandlerResult` vai a um `HandlerResultHandler` que completa a resposta.

Note o **contraste com o Galho 9**: a estrutura (mapping → adapter → result) é a mesma do `DispatcherServlet`, mas aqui tudo opera sobre tipos reativos e a escrita na resposta é não-bloqueante. Não vou re-explicar o pipeline imperativo — o ponto é que você reconhece o padrão e troca o modelo de execução por baixo.

### Controllers reativos: `@RestController` retornando `Mono<T>`/`Flux<T>`

O modelo anotado é quase idêntico ao do MVC. A diferença está no **tipo de retorno**:

- `Mono<T>` — um fluxo de **zero ou um** item. É o retorno típico de um `GET /orders/{id}`: ou tem o pedido, ou está vazio (404).
- `Flux<T>` — um fluxo de **zero ou muitos** itens. É o retorno de uma listagem ou de um stream contínuo.

Você **não chama `.block()` nem `.subscribe()`** no controller. Devolve o publisher e o framework subscreve por você no momento certo, encadeando a escrita na resposta como mais um passo da cadeia reativa. O handler é montagem declarativa de um pipeline, não execução imediata — o "nada acontece até o subscribe" do Reactor vale aqui também.

### Streaming/SSE (`text/event-stream`)

Como o retorno já é um `Flux`, **streaming sai de graça**. Declarando `produces = MediaType.TEXT_EVENT_STREAM_VALUE`, cada item emitido pelo `Flux` vira um **Server-Sent Event** enviado ao cliente conforme é produzido — sem esperar a coleção inteira. A doc observa que para SSE o encoder é invocado por evento e o output é *flushed* para garantir entrega sem atraso, e recomenda emitir dados periodicamente para detectar clientes desconectados cedo.

É a vantagem natural do modelo: um `Flux<OrderDto>` infinito (eventos de pedidos em tempo real) é servido incrementalmente, sem materializar tudo em memória.

## Na prática

Um controller WebFlux com um endpoint `Mono` (busca por id) e um endpoint `Flux` em modo SSE (stream de pedidos):

```java
import org.springframework.http.MediaType;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;
import reactor.core.publisher.Flux;
import reactor.core.publisher.Mono;

@RestController
@RequestMapping("/orders")
public class OrderController {

    private final OrderService orderService;

    public OrderController(OrderService orderService) {
        this.orderService = orderService;
    }

    // zero-ou-um: o framework subscreve; vazio vira 404
    @GetMapping("/{id}")
    public Mono<OrderDto> getOrder(@PathVariable Long id) {
        return orderService.findById(id); // Mono<OrderDto>, nunca .block()
    }

    // stream contínuo: cada item vira um Server-Sent Event
    @GetMapping(value = "/stream", produces = MediaType.TEXT_EVENT_STREAM_VALUE)
    public Flux<OrderDto> streamOrders() {
        return orderService.streamAll(); // Flux<OrderDto> servido item a item
    }
}
```

Repare que **nada bloqueia o event loop**: ambos os métodos só montam e devolvem o publisher. O `OrderService` devolve `Mono`/`Flux` que encadeiam acesso reativo a dados (por exemplo, R2DBC), não JDBC síncrono.

A dependência no `pom.xml` é o starter WebFlux — que já traz o Netty e configura o `DispatcherHandler` por auto-configuration (ver Galho 8):

```xml
<dependency>
    <groupId>org.springframework.boot</groupId>
    <artifactId>spring-boot-starter-webflux</artifactId>
</dependency>
```

## Armadilhas

### (1) Misturar `spring-boot-starter-web` e `spring-boot-starter-webflux`

Ter os dois starters no classpath ao mesmo tempo. O Spring Boot detecta o stack servlet e **o MVC vence**: a aplicação sobe como uma app servlet bloqueante (Tomcat), e seus controllers "reativos" rodam no modelo *thread-per-request* — você perde todo o benefício sem nenhum erro óbvio.

```xml
<!-- ERRADO: os dois juntos. O MVC (servlet/Tomcat) prevalece. -->
<dependency>
    <groupId>org.springframework.boot</groupId>
    <artifactId>spring-boot-starter-web</artifactId>
</dependency>
<dependency>
    <groupId>org.springframework.boot</groupId>
    <artifactId>spring-boot-starter-webflux</artifactId>
</dependency>
```

**Fix:** escolha um stack. Para uma app reativa, mantenha **apenas** o `spring-boot-starter-webflux` e remova o `-web`. Se precisar mesmo dos dois mundos no mesmo processo (raro), isso exige configuração explícita e consciente — não deixe a coexistência acidental decidir por você.

### (2) Bloquear dentro do handler (`.block()` ou JDBC síncrono)

Chamar `.block()` para "extrair o valor", ou usar uma chamada bloqueante (JDBC, `RestTemplate`, `Thread.sleep`) dentro de um handler que roda no event loop. Como o *loop* tem **poucos threads**, bloquear um deles congela **todas** as requisições que compartilham aquela thread — não só a atual. Sob carga, a aplicação inteira trava.

```java
// ERRADO: .block() na thread do event loop — congela o loop inteiro
@GetMapping("/{id}")
public OrderDto getOrder(@PathVariable Long id) {
    return orderService.findById(id).block(); // mata o event loop
}
```

**Fix:** devolva o publisher e deixe o framework subscrever. Encadeie tudo com operadores reativos (`map`, `flatMap`) e use clientes não-bloqueantes (WebClient, R2DBC). Se for **inevitável** chamar código bloqueante, isole-o num scheduler dedicado (`Mono.fromCallable(...).subscribeOn(Schedulers.boundedElastic())`), nunca no *loop*.

```java
// CERTO: devolve o Mono; o framework subscreve sem bloquear
@GetMapping("/{id}")
public Mono<OrderDto> getOrder(@PathVariable Long id) {
    return orderService.findById(id);
}
```

### (3) Achar que WebFlux "é mais rápido" para uma request única

Adotar WebFlux esperando que cada chamada individual responda mais rápido. Ela **não responde** — uma request única tem latência semelhante (às vezes pior, pela sobrecarga de orquestrar a cadeia reativa). O ganho do WebFlux é **throughput sob concorrência alta e I/O-bound**, não latência por chamada.

```text
Cenário CPU-bound, baixa concorrência, time sem experiência reativa
  -> WebFlux não acelera nada e adiciona complexidade (debug, stacktraces,
     proibição de bloquear). MVC imperativo é a escolha certa.

Cenário muitos clientes concorrentes, handlers I/O-bound (chamadas a
serviços externos, streaming)
  -> WebFlux sustenta a carga com poucos threads. Aqui o modelo paga.
```

**Fix:** escolha WebFlux pela **forma da carga** (concorrência alta, I/O-bound, streaming/SSE), não como upgrade automático. Para CRUD imperativo com pool de threads folgado, o Spring MVC (Galho 9) costuma ser mais simples e igualmente adequado.

## Em entrevista

### Frase pronta (inglês)

> Spring WebFlux is the non-blocking, reactive web stack in Spring. It runs on Netty by default, using an event loop with a small number of threads instead of the servlet's thread-per-request model, so it can sustain far more concurrent, I/O-bound requests with fewer threads. Its `DispatcherHandler` plays the same front-controller role as the `DispatcherServlet` from the servlet stack, delegating to `HandlerMapping`, `HandlerAdapter`, and `HandlerResultHandler` beans — but it operates over reactive types end to end. Controllers stay annotation-driven with `@RestController`, except handler methods return a `Mono` or a `Flux` instead of a plain object, and a `Flux` with `text/event-stream` gives you Server-Sent Events for free. The non-negotiable rule is that you must never block the event loop: a single blocking call stalls every request sharing that thread, so I treat WebFlux as a throughput choice for high-concurrency I/O workloads, not as a way to make any single request faster.

### Vocabulário

| Termo PT | Termo EN |
| --- | --- |
| stack não-bloqueante | non-blocking stack |
| event loop de poucos threads | small-thread event loop |
| modelo thread-por-requisição | thread-per-request model |
| contrapressão | back pressure |
| despacho da requisição | request dispatching |
| eventos enviados pelo servidor (SSE) | Server-Sent Events (SSE) |
| limitado por entrada/saída | I/O-bound |
| vazão / throughput | throughput |

## Veja também

- [[03-Dominios/Java/Programação Reativa/01 - O que é programação reativa — o modelo push, assíncrono e não-bloqueante|O que é programação reativa]]
- [[03-Dominios/Java/Programação Reativa/11 - WebClient — o cliente HTTP reativo a fundo|WebClient]]
- [[03-Dominios/Java/Programação Reativa/12 - Functional endpoints — RouterFunction e HandlerFunction|Functional endpoints]]
- [[03-Dominios/Java/Web e APIs REST/01 - O que é Spring MVC — a camada web sobre o container|O que é Spring MVC]]
- [[03-Dominios/Java/Web e APIs REST/06 - O pipeline do DispatcherServlet|O pipeline do DispatcherServlet]]
- [[03-Dominios/Java/Spring Core e Boot/15 - Auto-configuration e starters|Auto-configuration e starters]]
- [[03-Dominios/Java/Programação Reativa/index|Programação Reativa (MOC do galho)]]
- [[03-Dominios/Java/index|Trilha Java]]
- [[03-Dominios/Java/Dicionário de Java|Dicionário de Java]]

## Referências

- Spring Framework Reference — Web on Reactive Stack (Spring WebFlux): https://docs.spring.io/spring-framework/reference/web/webflux.html
- Spring Framework Reference — Reactive Core (`DispatcherHandler`, `WebHandler` API): https://docs.spring.io/spring-framework/reference/web/webflux/reactive-spring.html
- Spring Framework Reference — `DispatcherHandler`: https://docs.spring.io/spring-framework/reference/web/webflux/dispatcher-handler.html
