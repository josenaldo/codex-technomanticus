---
title: "Capstone — uma request reativa de ponta a ponta no WebFlux"
created: 2026-06-10
updated: 2026-06-10
type: concept
progress: backlog
status: seedling
publish: true
fase: magus
tags:
  - java
  - reativa
  - magus
  - webflux
  - r2dbc
aliases:
  - "Capstone Reativa"
  - "request reativa ponta a ponta"
---

# Capstone — uma request reativa de ponta a ponta no WebFlux

> [!abstract] TL;DR
> Uma request reativa atravessa o `DispatcherHandler` → um controller reativo (`@RestController`) → `WebClient` (serviço externo) **+** R2DBC (banco) → operadores como `flatMap`/`zip` e error handling com `onErrorResume` → backpressure via `request(n)` → um `Flux<OrderDto>` que o framework serializa **no event loop do Netty**, sem bloquear nenhum thread em ponto algum. O ponto-chave do galho inteiro: **quem chama `subscribe` é o framework**, não você. Você só **descreve** o pipeline; o `DispatcherHandler` assina e o event loop carrega os dados. Se um único `.block()` ou uma chamada JDBC vazar pra dentro dessa cadeia, o event loop trava e o modelo todo desaba.

## O que é

Esta é a **nota capstone** do Galho 11: a que costura as 15 anteriores num único trace executável. Em vez de mais uma peça isolada (Mono/Flux, operadores, schedulers, WebFlux, WebClient, R2DBC), aqui a gente segue **uma request real** — `GET /orders` — do byte que chega no socket até o JSON que sai, e mostra **onde cada conceito do galho entra**.

A tese é simples de enunciar e difícil de internalizar: numa stack reativa, o seu código de controller e service **não executa I/O** — ele **monta uma receita** (`Mono`/`Flux`) de como o I/O deveria acontecer. A execução só dispara quando o framework assina a receita, e a partir daí tudo corre **nos poucos threads do event loop**, dirigido por eventos de I/O não-bloqueante. Bloquear qualquer um desses threads é o pecado capital.

## Por que importa

Numa entrevista internacional sênior, "monte um endpoint reativo" raramente é a pergunta. A pergunta é **"o que acontece quando essa request chega?"** — e é aí que candidatos desmoronam. Eles sabem escrever `Mono<Order>`, mas não sabem dizer **quem assina**, **em que thread roda**, **o que acontece se o serviço externo cair**, ou **por que um `findAll()` do JPA dentro do handler destrói tudo**.

Saber o trace ponta a ponta é o que separa "já usei WebFlux" de "entendo WebFlux". É também o que te protege na produção: a classe mais comum de incidente reativo não são bugs de lógica — são **bloqueios acidentais do event loop** (uma lib legada, um `.block()` de debug que ficou, um driver JDBC escondido num `@Transactional`). Quem tem o trace na cabeça **vê o bloqueio antes de ele chegar em produção**.

## Como funciona

### Trace: `GET /orders` da chamada à resposta

O caminho completo de uma request reativa, com cada conceito do galho marcado:

```text
HTTP GET /orders  (socket no event loop do Reactor Netty)
        │
        ▼
DispatcherHandler            ← análogo ao DispatcherServlet do MVC (nota 10)
        │  consulta HandlerMapping → acha o método do controller
        ▼
@RestController reativo       ← retorna Flux<OrderDto> IMEDIATAMENTE (não-bloqueante)
        │  o método só MONTA o pipeline; nada de I/O ainda (nota 04)
        ▼
WebClient (serviço externo)  +  R2dbcRepository (banco)
   nota 11: cliente HTTP        nota 13: persistência reativa
   reativo, não-bloqueante      sem EntityManager, sobre driver R2DBC
        │                                    │
        └──────── flatMap / zip ─────────────┘   ← compõe os dois fluxos (notas 05, 06)
        │
        ▼
onErrorResume(...)            ← error handling no FIM da cadeia (nota 07)
        │
        ▼
backpressure: request(n)      ← o cliente puxa no seu ritmo (nota 09)
        │
        ▼
Flux<OrderDto>
        │
        ▼
o FRAMEWORK chama subscribe()  ← VOCÊ nunca assina num handler (nota 04)
        │
        ▼
event loop do Netty           ← serializa pra JSON e escreve no socket (nota 10)
        │                        poucos threads, thread-per-request NÃO existe aqui
        ▼
HTTP 200 + JSON  →  cliente
```

Cada seta é um conceito que já foi nota inteira no galho. O capstone é ver que eles não são tópicos soltos — são **estágios do mesmo fluxo**. A documentação do Spring confirma: o `DispatcherHandler` recebe o `Mono`/`Flux` do handler e **assina internamente**; a partir daí, operações não-bloqueantes (R2DBC, WebClient) correm no event loop, que **nunca trava** porque libera o thread enquanto espera o I/O.

### O que NÃO pode acontecer: bloquear o event loop

O event loop do Netty tem **pouquíssimos threads** (tipicamente um por core). Eles servem **todas** as requests concorrentes intercalando trabalho enquanto o I/O acontece em background. Se **um** desses threads parar esperando — `.block()`, um `Thread.sleep`, uma query JDBC síncrona, uma lib HTTP bloqueante — ele para de servir **todas** as outras requests que estavam multiplexadas nele.

```java
// ERRADO — isto trava o event loop e derruba a vazão de todo o servidor
@GetMapping("/orders")
public Flux<OrderDto> bad() {
    List<Order> orders = jpaRepository.findAll();   // JDBC bloqueante no event loop!
    return Flux.fromIterable(orders).map(this::toDto);
}
```

O sintoma é traiçoeiro: em desenvolvimento, com uma request por vez, **funciona**. Sob carga, a vazão despenca e as latências explodem, porque o punhado de threads do event loop vive bloqueado. A regra é absoluta: **nenhuma chamada bloqueante numa cadeia reativa servida pelo event loop**. Se uma lib bloqueante é inevitável, ela vai pra um `Scheduler` separado (`boundedElastic`) — nunca no event loop (nota 08).

### Galho 11 (reativo) ↔ imperativo (Galhos 9/10) + Virtual Threads (Galho 4)

O reativo não vive sozinho. Cada peça dele tem um análogo imperativo que você já conhece dos Galhos 9 (web) e 10 (persistência), e um terceiro caminho via Virtual Threads (Galho 4). Ver os três lado a lado desmistifica o reativo:

| Papel | Reativo (Galho 11) | Imperativo bloqueante (Galhos 9/10) | Imperativo + Virtual Threads (Galho 4) |
| --- | --- | --- | --- |
| Front controller | `DispatcherHandler` | `DispatcherServlet` | `DispatcherServlet` |
| Cliente HTTP | `WebClient` | `RestClient` / `RestTemplate` | `RestClient` (bloqueante, barato em VT) |
| Persistência | R2DBC (`R2dbcRepository`) | JPA / Hibernate (`JpaRepository`) | JPA / JDBC (bloqueante, barato em VT) |
| Modelo de thread | event loop (poucos threads, multiplexado) | thread-per-request (pool grande do SO) | thread-per-request **virtual** (milhares baratos) |
| Backpressure | nativo (`request(n)`) | inexistente | inexistente (você implementa na mão) |
| Stack trace / debug | montado, assíncrono, difícil | linear, trivial | linear, trivial |

A leitura honesta (aprofundada na nota 14): Virtual Threads tornaram o **imperativo bloqueante viável pra alta concorrência**, então o reativo deixou de ser a única resposta pra "escalar I/O". Reativo **ainda vence** em streaming real e backpressure ponta a ponta — mas o CRUD de alta concorrência, que era um motivo central pra WebFlux, hoje cabe num MVC sobre Virtual Threads.

## Na prática

Um controller reativo completo que faz exatamente o trace acima: recebe a request, busca os pedidos no banco via R2DBC, **enriquece cada um** com dados de um serviço externo via `WebClient`, compõe os dois fluxos, trata erro no fim e devolve `Flux<OrderDto>` — tudo não-bloqueante.

```java
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;
import org.springframework.web.reactive.function.client.WebClient;
import reactor.core.publisher.Flux;
import reactor.core.publisher.Mono;

@RestController
@RequestMapping("/orders")
public class OrderController {

    private final OrderRepository orders;       // R2dbcRepository<Order, Long>
    private final CustomerRepository customers; // R2dbcRepository<Customer, Long>
    private final WebClient productClient;      // serviço externo de catálogo

    public OrderController(OrderRepository orders,
                           CustomerRepository customers,
                           WebClient productClient) {
        this.orders = orders;
        this.customers = customers;
        this.productClient = productClient;
    }

    // GET /orders — lista todos os pedidos, cada um enriquecido com cliente + produto
    @GetMapping
    public Flux<OrderDto> listOrders() {
        return orders.findAll()                 // Flux<Order> do banco (R2DBC), não-bloqueante
            .flatMap(this::enrich)              // pra cada Order, compõe cliente + produto
            .onErrorResume(this::fallback);     // error handling NO FIM da cadeia
    }

    // GET /orders/{id} — um único pedido enriquecido
    @GetMapping("/{id}")
    public Mono<OrderDto> getOrder(@PathVariable Long id) {
        return orders.findById(id)
            .flatMap(this::enrich)
            .switchIfEmpty(Mono.error(new OrderNotFoundException(id)))
            .onErrorResume(this::fallbackMono);
    }

    // compõe DUAS fontes em paralelo: cliente (banco) + produto (serviço externo)
    private Mono<OrderDto> enrich(Order order) {
        Mono<Customer> customer = customers.findById(order.customerId());
        Mono<Product> product = productClient.get()
            .uri("/products/{id}", order.productId())
            .retrieve()
            .bodyToMono(Product.class)
            .timeout(java.time.Duration.ofSeconds(2));   // não fica pendurado pra sempre

        // zip espera os dois resolverem e combina — sem bloquear thread nenhum
        return Mono.zip(customer, product,
                (c, p) -> new OrderDto(order.id(), c.name(), p.name(), order.total()));
    }

    private Flux<OrderDto> fallback(Throwable error) {
        // degrada elegante: loga e devolve fluxo vazio em vez de propagar 500
        return Flux.empty();
    }

    private Mono<OrderDto> fallbackMono(Throwable error) {
        return Mono.empty();
    }
}
```

Note o que **não** está aqui: nenhum `.block()`, nenhum `subscribe()`, nenhum `for`/`while` sobre resultados de I/O, nenhuma chamada JDBC. O método **descreve** o pipeline e devolve o publisher; o `DispatcherHandler` assina, o event loop executa, o `request(n)` do cliente regula o ritmo.

### Checklist de design production-grade

- [ ] **Nunca `.block()` num handler.** Bloquear o event loop derruba a vazão do servidor inteiro. Se você "precisa" de `.block()`, o desenho está errado.
- [ ] **Lib bloqueante inevitável vai pro `boundedElastic()`.** Use `.subscribeOn(Schedulers.boundedElastic())` pra isolar a chamada bloqueante num pool dedicado, fora do event loop (nota 08).
- [ ] **Error handling no fim da cadeia.** `onErrorResume`/`onErrorReturn` no final cobre toda a cadeia acima. Espalhar `try/catch` no meio do pipeline reativo não funciona — o erro é um sinal, não uma exceção lançada na hora (nota 07).
- [ ] **Backpressure consciente.** Em streaming real (SSE, fluxo infinito), pense na estratégia: o produtor é mais rápido que o consumidor? `BUFFER` pode estourar memória; escolha `DROP`/`LATEST` quando perder dados é aceitável (nota 09).
- [ ] **O `subscribe` é do framework.** Você nunca assina dentro de um handler WebFlux. Se você escreveu `.subscribe()` num controller, quase certamente introduziu um bug (fire-and-forget que perde o resultado e o backpressure).
- [ ] **Timeouts em toda chamada externa.** Sem `.timeout(...)`, uma dependência lenta segura o pipeline indefinidamente — em reativo isso não consome um thread, mas consome conexões e memória.
- [ ] **Não esconda JDBC atrás de abstração.** Um `@Transactional` com `JpaRepository` no meio de uma stack WebFlux é JDBC bloqueante disfarçado. Persistência reativa = R2DBC, ponto.

## Armadilhas

### (1) Achar que "reativo é sempre melhor pra escala"

**Descrição.** O dogma de que WebFlux escala mais que MVC "porque é não-bloqueante". Isso era um argumento forte antes do Java 21. Hoje, Virtual Threads (JEP 444, GA no Java 21) deixam o MVC bloqueante escalar com **milhares de threads virtuais baratos**, atingindo concorrência altíssima **sem** reescrever nada em `Mono`/`Flux`.

**Explicação.** A própria documentação do Spring é honesta: se sua dependência de persistência é bloqueante (JPA/JDBC), Spring MVC é a melhor escolha pra arquiteturas comuns — e Virtual Threads reforçam isso, porque tornam o MVC escalável. Escolher WebFlux só "pra escalar" hoje paga o custo cognitivo do reativo sem necessidade.

**Fix.** Escolha por problema, não por hype. WebFlux pra **streaming real e backpressure ponta a ponta** (onde `request(n)` é insubstituível); MVC + Virtual Threads pra **CRUD de alta concorrência**. O confronto detalhado está na nota 14 — [[03-Dominios/Tecnologia/Java/Programação Reativa/14 - Reativo vs Virtual Threads — o confronto honesto|Reativo vs Virtual Threads]].

### (2) Achar que "é só trocar o tipo de retorno pra `Mono`/`Flux`"

**Descrição.** A ilusão de que "reativar" um endpoint é mudar `Order` pra `Mono<Order>` na assinatura. Não é. Se a cadeia por baixo continua bloqueante, você **mentiu pro framework**: o tipo diz "não-bloqueante" mas o código bloqueia o event loop.

**Exemplo.** Trocar `public Order get()` por `public Mono<Order> get()` mas o corpo ainda faz `jpaRepository.findById(id)` (JDBC). O retorno é `Mono.just(jpaRepository.findById(id))` — o I/O bloqueante já rodou no event loop **antes** do `Mono` existir. Em produção sob carga, o servidor trava. O tipo virou reativo; a execução não.

**Fix.** Reativar é trocar **a stack inteira**: driver (R2DBC, não JDBC), cliente HTTP (`WebClient`, não `RestTemplate` bloqueante), e compor com operadores em vez de chamar e esperar. Se você não pode trocar o driver bloqueante, **não reative** — fique no MVC. Meio-termo é o pior dos mundos.

### (3) Achar que "`WebClient` é mais rápido que `RestTemplate`"

**Descrição.** Confundir **throughput** com **latência por request**. `WebClient` não entrega a resposta de uma chamada individual mais rápido — o gargalo é a rede e o serviço remoto, idêntico pros dois.

**Explicação.** O ganho do `WebClient` é que ele **não amarra um thread** enquanto espera a resposta: o mesmo punhado de threads do event loop dispara e acompanha milhares de chamadas concorrentes. Isso é **vazão sob carga**, não velocidade de um request. Medir a latência de **uma** chamada e concluir "`WebClient` é mais rápido" (ou "mais lento") é medir a métrica errada.

**Fix.** Compare sob carga concorrente alta, medindo throughput, threads do SO usados e memória — não cronômetro num request só. E lembre: o `WebClient` só rende esse ganho se a stack ao redor **não bloquear**; um `.block()` no `WebClient` joga fora exatamente a vantagem que o tornava interessante.

## Em entrevista

### Frase pronta (inglês)

> In WebFlux, a request like `GET /orders` enters through the `DispatcherHandler` — the reactive analogue of MVC's `DispatcherServlet` — which routes it to a reactive `@RestController` that returns a `Flux<OrderDto>` immediately, without doing any I/O yet. The controller only assembles a pipeline: it pulls orders from the database over R2DBC, enriches each one by calling an external service with `WebClient`, composes the two sources with `flatMap` and `zip`, and handles failures with `onErrorResume` at the end of the chain. Nothing runs until the framework subscribes — you never call `subscribe` in a handler — and from that point everything executes on the Netty event loop's handful of threads, driven by non-blocking I/O and regulated by `request(n)` backpressure. The one rule that makes or breaks the whole model is that you must never block an event-loop thread: a single `.block()` or a JDBC call leaks blocking I/O into the loop and collapses the throughput of the entire server.

### Cheatsheet

| Sei explicar... | ...então resolvo o problema de |
| --- | --- |
| `map` vs `flatMap` (notas 05) | transformar valor síncrono vs encadear outra operação assíncrona/I/O |
| `zip`/`merge`/`concat` (nota 06) | combinar múltiplas fontes (banco + serviço externo) sem bloquear |
| Schedulers `boundedElastic` (nota 08) | isolar uma lib bloqueante inevitável fora do event loop |
| backpressure `request(n)` (nota 09) | produtor mais rápido que consumidor sem estourar memória |
| `DispatcherHandler` + event loop (nota 10) | quem roteia, quem assina, em que thread roda a request |
| R2DBC vs JPA (nota 13) | por que um `JpaRepository` num handler reativo trava tudo |
| reativo vs Virtual Threads (nota 14) | quando NÃO usar reativo — CRUD de alta concorrência cabe em MVC+VT |

### Vocabulário

| Termo PT | Termo EN |
| --- | --- |
| laço de eventos | event loop |
| não-bloqueante | non-blocking |
| ponta a ponta | end-to-end |
| contrapressão | backpressure |
| quem assina / assinante | subscriber |
| cadeia de operadores | operator chain |
| degradação elegante | graceful degradation |
| controlador frontal | front controller |

## Veja também

- [[03-Dominios/Tecnologia/Java/Programação Reativa/10 - Spring WebFlux — o stack não-bloqueante sobre Netty e o DispatcherHandler|Spring WebFlux]]
- [[03-Dominios/Tecnologia/Java/Programação Reativa/11 - WebClient — o cliente HTTP reativo a fundo|WebClient]]
- [[03-Dominios/Tecnologia/Java/Programação Reativa/13 - R2DBC — persistência reativa sem EntityManager|R2DBC]]
- [[03-Dominios/Tecnologia/Java/Programação Reativa/14 - Reativo vs Virtual Threads — o confronto honesto|Reativo vs Virtual Threads]]
- [[03-Dominios/Tecnologia/Java/Concorrência e paralelismo/12 - Virtual Threads e Project Loom|Virtual Threads e Project Loom]]
- [[03-Dominios/Tecnologia/Java/Web e APIs REST/01 - O que é Spring MVC — a camada web sobre o container|O que é Spring MVC]]
- [[03-Dominios/Tecnologia/Java/Persistência de dados/01 - O que é a camada de persistência — Spring Data, JPA e Hibernate|O que é a camada de persistência]]
- [[03-Dominios/Tecnologia/Java/Programação Reativa/index|Programação Reativa (MOC do galho)]]
- [[03-Dominios/Tecnologia/Java/index|Trilha Java]]
- [[03-Dominios/Tecnologia/Java/Dicionário de Java|Dicionário de Java]]

> [!info] Galhos futuros
> Este capstone fecha o Galho 11 (Programação Reativa). Os Galhos 12-16 da trilha Java ainda estão planejados.

## Referências

- Spring Framework — Web on Reactive Stack / WebFlux (`DispatcherHandler`, modelo de concorrência sobre Reactor Netty, assinatura automática pelo framework, backpressure): https://docs.spring.io/spring-framework/reference/web/webflux.html
- Project Reactor — Reference Guide (`Mono`/`Flux`, nada acontece até o `subscribe`, operadores `flatMap`/`zip`/`map`, `onErrorResume`, `request(n)`, Schedulers `boundedElastic`): https://projectreactor.io/docs/core/release/reference/
