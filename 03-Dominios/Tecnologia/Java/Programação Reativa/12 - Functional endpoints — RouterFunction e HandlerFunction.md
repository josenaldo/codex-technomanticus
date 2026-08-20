---
title: "Functional endpoints — RouterFunction e HandlerFunction"
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
  - webflux
aliases:
  - "functional endpoints"
  - "RouterFunction"
---

# Functional endpoints — RouterFunction e HandlerFunction

> [!abstract] TL;DR
> Functional endpoints (WebFlux.fn) são a **alternativa funcional** aos controllers anotados do WebFlux: em vez de declarar rotas com `@GetMapping` e deixar o framework descobri-las por reflexão, o **roteamento vira código explícito** — você constrói um `RouterFunction` com `RouterFunctions.route().GET(...).build()`. Cada rota aponta para uma **`HandlerFunction`**, que é só uma função `ServerRequest → Mono<ServerResponse>` — o equivalente ao corpo de um método `@RequestMapping`, mas como um lambda comum. A resposta também é reativa: `ServerResponse.ok().body(orderMono, OrderDto.class)`. O modelo anotado e o funcional rodam sobre o **mesmo** `DispatcherHandler` e o mesmo stack não-bloqueante; muda só *quem escreve o roteamento* — o framework (anotações) ou você (código).

## O que é

**Functional endpoints** — apelidados de **WebFlux.fn** na documentação — são um modelo de programação leve em que **funções** roteiam e tratam requisições. A doc o descreve como "a lightweight functional programming model in which functions are used to route and handle requests and contracts are designed for immutability".

Duas abstrações sustentam o modelo:

- **`RouterFunction`** — uma função que recebe uma `ServerRequest` e devolve um `Mono<HandlerFunction>`: dado o request, ela decide *qual* handler responde (ou nenhum). É o roteamento.
- **`HandlerFunction`** — uma função `ServerRequest → Mono<ServerResponse>`: dado o request, produz a resposta. É o tratamento.

Em vez de espalhar anotações por uma classe `@RestController`, você concentra o roteamento num `RouterFunction` construído programaticamente e registra esse objeto como um `@Bean`. O `DispatcherHandler` (o mesmo do Galho 10) descobre esse bean via `RouterFunctionMapping` e despacha por ele — exatamente como descobre os controllers anotados via outro `HandlerMapping`.

## Por que importa

O modelo anotado esconde o roteamento atrás de reflexão: o mapeamento de URL para método é montado pelo framework lendo `@GetMapping`, `@PathVariable` e companhia. É conveniente e familiar — mas é **mágica implícita**. Funciona muito bem até você querer compor rotas dinamicamente, aplicar um predicado comum a um grupo inteiro de endpoints, ou simplesmente ver o roteamento **inteiro em um lugar, como dado**.

Functional endpoints invertem isso. O roteamento passa a ser um **objeto de primeira classe** que você constrói, compõe e testa como qualquer outro código. Você pode aninhar rotas sob um prefixo, aplicar um `RequestPredicate` (ex.: `accept(APPLICATION_JSON)`) a um bloco, combinar vários `RouterFunction` com `.andOther(...)`, e montar tudo condicionalmente em tempo de inicialização. A imutabilidade dos contratos (`ServerRequest`/`ServerResponse` são interfaces imutáveis) torna o handler uma função pura mais fácil de raciocinar.

Em entrevista, saber que **os dois modelos coexistem sobre o mesmo runtime** mostra que você entende a arquitetura do WebFlux, não só decorou anotações. Não é "qual é melhor"; é "qual encaixa neste caso" — e por quê.

## Como funciona

### Roteamento como código: `RouterFunctions.route().GET(...).build()`

O ponto de entrada é `RouterFunctions.route()` (estático, normalmente importado de forma estática), que devolve um **builder fluente**. Você encadeia métodos por verbo HTTP — `GET`, `POST`, `PUT`, `DELETE` — cada um associando um padrão de path (e, opcionalmente, um `RequestPredicate`) a uma `HandlerFunction`. No fim, `.build()` materializa o `RouterFunction<ServerResponse>` composto.

```java
import static org.springframework.web.reactive.function.server.RequestPredicates.accept;
import static org.springframework.web.reactive.function.server.RouterFunctions.route;
import static org.springframework.http.MediaType.APPLICATION_JSON;

RouterFunction<ServerResponse> orderRoutes = route()
    .GET("/orders/{id}", accept(APPLICATION_JSON), handler::getOrder)
    .GET("/orders", accept(APPLICATION_JSON), handler::listOrders)
    .POST("/orders", handler::createOrder)
    .build();
```

As rotas são avaliadas **em ordem** e o **primeiro match vence** — diferente do modelo anotado, que escolhe o método "mais específico". Isso significa que a ordem em que você declara importa: rotas mais específicas vêm antes das mais genéricas.

### `HandlerFunction`: `ServerRequest → Mono<ServerResponse>`

Uma `HandlerFunction<ServerResponse>` é uma interface funcional com um único método: recebe uma `ServerRequest` e devolve um `Mono<ServerResponse>`. A doc diz que é "the equivalent of the body of a `@RequestMapping` method in the annotation-based programming model".

A `ServerRequest` é uma interface **imutável** que dá acesso ao request: `request.pathVariable("id")` lê uma variável de path; `request.bodyToMono(OrderDto.class)` e `request.bodyToFlux(OrderDto.class)` desserializam o corpo de forma reativa; há também `queryParam`, `headers`, `formData`, etc.

```java
public Mono<ServerResponse> getOrder(ServerRequest request) {
    Long id = Long.valueOf(request.pathVariable("id"));
    Mono<OrderDto> order = orderService.findById(id);
    return ServerResponse.ok()
        .contentType(APPLICATION_JSON)
        .body(order, OrderDto.class);
}
```

Como é só uma função, um handler pode ser um **lambda** para casos triviais (`request -> ServerResponse.ok().bodyValue("pong")`) ou um **método de uma classe handler** (`handler::getOrder`) para a lógica de verdade. O contrato é o mesmo do controller anotado em termos reativos: você **monta e devolve** o `Mono<ServerResponse>`, sem `.block()` nem `.subscribe()`.

### Functional vs anotado: quando cada um

Os dois modelos produzem o mesmo resultado sobre o mesmo `DispatcherHandler`. A escolha é de **estilo e necessidade**, não de capacidade:

- **Anotado (Galho 9/10)** — `@RestController` + `@GetMapping`. Vence pela **familiaridade**: todo time Spring já conhece, o roteamento é declarativo e conciso, e a integração com validação/binding é direta. É o caminho padrão para CRUD e APIs convencionais.
- **Funcional (WebFlux.fn)** — `RouterFunction` + `HandlerFunction`. Vence quando você quer **roteamento como dado**: composição programática de rotas, predicados compartilhados, montagem condicional em tempo de boot, ou um controle mais explícito e testável do mapeamento request→handler. Útil também em libraries/gateways que geram rotas dinamicamente.

Não é preciso escolher para o projeto inteiro: ambos podem coexistir. Mas misturá-los **sem critério** confunde quem lê o código (ver Armadilhas). Não vou re-explicar aqui como o modelo anotado funciona — isso é o Galho 9. O foco desta nota é o **contraste**: o que você ganha movendo o roteamento de anotações para código.

## Na prática

Um `RouterFunction` registrado como `@Bean`, roteando `GET /orders/{id}` para uma `HandlerFunction` que devolve um `Mono<ServerResponse>` com corpo reativo:

```java
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.stereotype.Component;
import org.springframework.web.reactive.function.server.RouterFunction;
import org.springframework.web.reactive.function.server.ServerRequest;
import org.springframework.web.reactive.function.server.ServerResponse;
import reactor.core.publisher.Mono;

import static org.springframework.http.MediaType.APPLICATION_JSON;
import static org.springframework.web.reactive.function.server.RequestPredicates.accept;
import static org.springframework.web.reactive.function.server.RouterFunctions.route;

// O roteamento: descoberto pelo RouterFunctionMapping como qualquer @Bean
@Configuration
public class OrderRouter {

    @Bean
    public RouterFunction<ServerResponse> orderRoutes(OrderHandler handler) {
        return route()
            .GET("/orders/{id}", accept(APPLICATION_JSON), handler::getOrder)
            .build();
    }
}

// O tratamento: ServerRequest -> Mono<ServerResponse>, tudo reativo
@Component
public class OrderHandler {

    private final OrderService orderService;

    public OrderHandler(OrderService orderService) {
        this.orderService = orderService;
    }

    public Mono<ServerResponse> getOrder(ServerRequest request) {
        Long id = Long.valueOf(request.pathVariable("id"));
        Mono<OrderDto> order = orderService.findById(id); // Mono, nunca .block()
        return ServerResponse.ok()
            .contentType(APPLICATION_JSON)
            .body(order, OrderDto.class); // corpo reativo: o framework escreve quando o Mono emite
    }
}
```

Repare em dois pontos. Primeiro: o handler **não bloqueia o event loop** — ele só monta o pipeline (`pathVariable` → `findById` → `body`) e devolve o `Mono<ServerResponse>`; o framework subscreve no momento certo. Segundo: `.body(order, OrderDto.class)` recebe um **publisher** (`order` é um `Mono<OrderDto>`), então a própria escrita da resposta é não-bloqueante e respeita *back pressure*.

## Armadilhas

### (1) Misturar functional e anotado sem critério

Espalhar parte das rotas em `@RestController` e parte em `RouterFunction` sem uma fronteira clara. Ambos funcionam ao mesmo tempo (são `HandlerMapping`s diferentes sobre o mesmo `DispatcherHandler`), mas quem lê o código perde a noção de **onde uma rota está definida** — para achar quem responde `GET /orders/{id}`, precisa caçar nos dois lugares.

```text
OrderController       @GetMapping("/orders/{id}")     <- anotado
OrderRouter           route().GET("/orders", ...)      <- funcional
ReportController      @GetMapping("/orders/report")    <- anotado de novo
```
Navegar pela API vira uma caça ao tesouro entre dois estilos.

**Fix:** decida uma fronteira explícita e documente-a. Por exemplo: use **um** modelo por módulo/contexto (todas as rotas de pedidos no estilo funcional, todas as de relatórios no anotado), nunca os dois para o mesmo recurso. Quando coexistirem, que seja por uma razão deliberada e visível, não por acúmulo acidental.

### (2) Lógica de negócio dentro do router/handler

Colocar regra de negócio — cálculos, validações de domínio, orquestração de várias chamadas — direto no `HandlerFunction` (ou pior, no builder do router). O handler incha, fica difícil de testar isoladamente e mistura a camada web com o domínio.

```java
// ERRADO: regra de negócio no handler
public Mono<ServerResponse> createOrder(ServerRequest request) {
    return request.bodyToMono(OrderDto.class)
        .flatMap(dto -> {
            if (dto.total() > 10_000) { /* aprovação manual... */ }
            // cálculo de imposto, desconto, persistência... tudo aqui
            return repository.save(toEntity(dto));
        })
        .flatMap(saved -> ServerResponse.ok().bodyValue(saved));
}
```

**Fix:** mantenha o handler **fino** — ele só extrai dados do `ServerRequest`, delega ao `service` e adapta o resultado para `ServerResponse`. A regra vive no service, que devolve `Mono`/`Flux`:

```java
// CERTO: handler fino, regra no service
public Mono<ServerResponse> createOrder(ServerRequest request) {
    return request.bodyToMono(OrderDto.class)
        .flatMap(orderService::place)            // toda a regra está no service
        .flatMap(saved -> ServerResponse.status(201).bodyValue(saved));
}
```

### (3) Esquecer que o `ServerResponse` também é reativo

Tratar o `ServerResponse` como se você precisasse ter o valor **pronto** para construí-lo — chamando `.block()` no `Mono` do service só para passar o objeto cru a `bodyValue(...)`. Isso bloqueia o event loop (catastrófico no WebFlux, ver Galho 10) e ignora que o `body(...)` aceita um publisher.

```java
// ERRADO: bloqueia o loop para "ter o valor" antes de montar a resposta
public Mono<ServerResponse> getOrder(ServerRequest request) {
    OrderDto order = orderService.findById(id).block(); // mata o event loop
    return ServerResponse.ok().bodyValue(order);
}
```

**Fix:** passe o **publisher** direto para `body(publisher, Class)` — o `ServerResponse` é montado de forma diferida e o framework escreve o corpo quando o `Mono`/`Flux` emite, sem bloquear:

```java
// CERTO: corpo reativo, escrito quando o Mono emite
public Mono<ServerResponse> getOrder(ServerRequest request) {
    Long id = Long.valueOf(request.pathVariable("id"));
    Mono<OrderDto> order = orderService.findById(id);
    return ServerResponse.ok().body(order, OrderDto.class);
}
```

(Use `bodyValue(obj)` só quando o valor **já está em mãos** de forma síncrona, sem `.block()` — por exemplo um literal ou um objeto já materializado a montante na cadeia.)

## Em entrevista

### Frase pronta (inglês)

> Functional endpoints, or WebFlux.fn, are the functional alternative to annotated controllers in Spring WebFlux. Instead of declaring routes with annotations like `@GetMapping` and letting the framework discover them by reflection, you build the routing as explicit code with `RouterFunctions.route().GET(...).build()`, which produces a `RouterFunction` you register as a bean. Each route points to a `HandlerFunction`, which is just a function from `ServerRequest` to `Mono<ServerResponse>` — the equivalent of an annotated handler method body, but as a plain lambda or method reference. Both models run on the very same `DispatcherHandler` and the same non-blocking stack, so the response stays reactive too: I return `ServerResponse.ok().body(orderMono, OrderDto.class)` and the framework writes the body when the publisher emits, never blocking the event loop. I reach for the functional model when I want routing as first-class data — composable, conditionally assembled, with shared predicates — and I stick with the annotated model when familiarity and conciseness matter more.

### Vocabulário

| Termo PT | Termo EN |
| --- | --- |
| endpoints funcionais | functional endpoints |
| função de roteamento | router function |
| função de tratamento | handler function |
| roteamento como código | routing as code |
| referência de método | method reference |
| variável de path | path variable |
| corpo reativo da resposta | reactive response body |
| primeiro match vence | first match wins |

## Veja também

- [[03-Dominios/Tecnologia/Java/Programação Reativa/10 - Spring WebFlux — o stack não-bloqueante sobre Netty e o DispatcherHandler|Spring WebFlux]]
- [[03-Dominios/Tecnologia/Java/Web e APIs REST/01 - O que é Spring MVC — a camada web sobre o container|O que é Spring MVC]]
- [[03-Dominios/Tecnologia/Java/Programação Reativa/index|Programação Reativa (MOC do galho)]]
- [[03-Dominios/Tecnologia/Java/index|Trilha Java]]
- [[03-Dominios/Tecnologia/Java/Dicionário de Java|Dicionário de Java]]

## Referências

- Spring Framework Reference — Functional Endpoints (WebFlux.fn): https://docs.spring.io/spring-framework/reference/web/webflux-functional.html
