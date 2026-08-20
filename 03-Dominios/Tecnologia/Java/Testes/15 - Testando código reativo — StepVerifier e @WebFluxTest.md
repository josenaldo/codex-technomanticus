---
title: "Testando código reativo — StepVerifier e @WebFluxTest"
created: 2026-06-11
updated: 2026-06-11
type: concept
progress: backlog
status: seedling
publish: true
fase: Magus
tags:
  - java
  - testes
  - magus
  - stepverifier
  - spring-test
aliases:
  - "StepVerifier"
  - "@WebFluxTest"
  - "testando reativo"
---

# Testando código reativo — StepVerifier e @WebFluxTest

> [!abstract] TL;DR
> `StepVerifier` é o "JUnit do reativo": ele **assina** o `Mono`/`Flux` e verifica o fluxo **passo a passo** — `expectNext(...)` para cada item, `expectError(...)` para a falha esperada, e `verifyComplete()`/`verify()` no fim para realmente disparar a assinatura. `expectNextCount(n)` conta itens sem casar valor a valor. `StepVerifier.withVirtualTime(() -> ...)` testa delays (`Mono.delay`, `Flux.interval`) **sem esperar o tempo real** — o relógio é virtual e `thenAwait(Duration)` adianta o ponteiro. Para reactive controllers, `@WebFluxTest` sobe só a fatia WebFlux e injeta um `WebTestClient` que exercita os endpoints de forma não-bloqueante. Dependência: `io.projectreactor:reactor-test` (scope `test`).

## O que é

Código reativo não retorna valores — retorna **publishers preguiçosos** (`Mono`/`Flux`) que só executam quando alguém assina. Um teste comum (`assertEquals(esperado, metodo())`) não funciona: ele compararia o objeto `Flux` em si, não os itens que ele emite. Pior, sem assinatura **nada roda**.

`StepVerifier` (do módulo `reactor-test`) é a ferramenta canônica para esse cenário. Ele é o **assinante de teste**: descreve uma sequência de expectativas sobre o fluxo de sinais (`onNext`, `onError`, `onComplete`) e, ao chamar `verify()`/`verifyComplete()`, assina o publisher e valida cada sinal contra a expectativa correspondente — falhando o teste se algo divergir.

Do lado HTTP, `@WebFluxTest` é a fatia de teste do Spring Boot para reactive controllers: sobe apenas a infraestrutura WebFlux (`@Controller`, `@ControllerAdvice`, `WebFluxConfigurer`, filtros, conversores) e auto-configura um `WebTestClient` para bater nos endpoints sem subir servidor real nem o contexto inteiro.

> Os tipos reativos em si (`Mono`, `Flux`, backpressure, schedulers) e o stack WebFlux são do Galho 11 — aqui o foco é **testá-los**, não reexplicá-los. Veja [[03-Dominios/Tecnologia/Java/Programação Reativa/10 - Spring WebFlux — o stack não-bloqueante sobre Netty e o DispatcherHandler|Spring WebFlux]] e [[03-Dominios/Tecnologia/Java/Programação Reativa/11 - WebClient — o cliente HTTP reativo a fundo|WebClient]].

## Por que importa

Reativo testado errado é reativo **não testado**. Os dois erros mais caros são silenciosos:

- **Esquecer o `verify`**: a cadeia de `expectNext` parece um teste, mas sem `verify()`/`verifyComplete()` o `StepVerifier` **nunca assina** — o publisher nem executa, e o teste passa verde sem ter exercido uma linha de produção. É um falso positivo perfeito.
- **`block()` no teste**: bloquear o `Mono`/`Flux` para "pegar o valor" funciona em casos triviais, mas joga fora a natureza assíncrona (ordem de emissão, sinais de erro, backpressure) e pode **travar** o teste se o fluxo nunca completar.

Além disso, código reativo frequentemente tem **tempo embutido** — timeouts, retries com backoff, `Flux.interval`, polling. Testar isso com tempo real torna a suíte lenta e flaky. `withVirtualTime` resolve: um delay de uma hora passa em microssegundos de relógio virtual. Em entrevista sênior, saber distinguir `StepVerifier` de `block()`, e saber por que `verify()` é obrigatório, é o tipo de detalhe que separa quem usou reativo de quem só leu sobre.

## Como funciona

### StepVerifier: o JUnit do reativo (expectNext / expectError / verifyComplete)

O fluxo básico é sempre o mesmo: **`create` → expectativas → `verify`**.

- `StepVerifier.create(publisher)` envolve o `Mono`/`Flux` sob teste e abre a cadeia de expectativas.
- `expectNext(a, b, c)` afirma que os próximos sinais `onNext` carregam exatamente esses valores, nessa ordem.
- `expectError(IllegalArgumentException.class)` / `expectErrorMessage("...")` afirmam que a sequência **termina** com aquele erro.
- `verifyComplete()` afirma término por `onComplete` **e** dispara a verificação (assina o publisher e bloqueia até terminar ou falhar). `verify()` é a forma genérica, usada quando o término esperado é um erro.

A regra de ouro: **a cadeia só executa no `verify`**. Tudo antes é descrição declarativa; o `verify`/`verifyComplete` é o gatilho que assina e roda.

### expectNextCount e asserções sobre o fluxo

Quando os valores exatos não importam — só a **quantidade** — `expectNextCount(long)` conta `n` sinais `onNext` sem casar valor a valor. Útil para fluxos grandes ou não-determinísticos onde casar item a item seria frágil.

Há um arsenal de variantes para asserções mais ricas:

- `expectNextMatches(predicate)` — casa o próximo item contra um predicado (`o -> o.total() > 0`).
- `assertNext(consumer)` — entrega o próximo item a um consumidor onde você roda asserções AssertJ/JUnit livremente.
- `expectNextSequence(iterable)` — casa contra uma coleção esperada inteira.
- `thenConsumeWhile(predicate)` — drena itens enquanto o predicado for verdadeiro (útil antes de checar o término).

Combine: `expectNext(primeiro).expectNextCount(2).expectNextMatches(...).verifyComplete()`.

### withVirtualTime: testar delays sem esperar de verdade

Fluxos com tempo (`Mono.delay`, `Flux.interval`, `timeout`, retry com backoff) não podem ser testados com `Thread.sleep` — seria lento e flaky. `StepVerifier.withVirtualTime(Supplier<Publisher>)` instala um `VirtualTimeScheduler` e, crucialmente, **recebe o publisher dentro de um `Supplier`** (lambda) — porque ele precisa ser construído *depois* que o scheduler virtual está ativo, senão o agendamento usa o relógio real.

Com o relógio virtual ligado:

- `thenAwait(Duration.ofHours(1))` **adianta o ponteiro** uma hora instantaneamente, em vez de bloquear.
- `expectNoEvent(Duration)` afirma que, durante aquela janela virtual, **nada** foi emitido (bom para validar que o delay realmente segura o item).

Um delay de horas vira um teste de milissegundos, e é **determinístico**.

### @WebFluxTest + WebTestClient: testar reactive controllers

`@WebFluxTest` é a fatia de teste para controllers WebFlux. Diferente de `@SpringBootTest`, ela **não sobe o contexto inteiro**: limita os beans escaneados a `@Controller`, `@ControllerAdvice`, `WebFluxConfigurer`, `Filter`, conversores e afins — `@Component`/`@Service` comuns **não** são carregados. As dependências do controller (o `OrderService`, por exemplo) você fornece como mock via `@MockitoBean`.

Em troca, ela auto-configura um **`WebTestClient`** (injetado por `@Autowired`), um cliente reativo de teste com API fluente: `.get().uri(...).exchange().expectStatus().isOk().expectBodyList(Order.class)`. Ele exercita o controller de ponta a ponta (roteamento, serialização, content negotiation) **sem servidor HTTP real** e sem bloquear threads. Restrinja o escopo com `@WebFluxTest(OrderController.class)` para subir só o controller sob teste.

## Na prática

```java
import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.autoconfigure.web.reactive.WebFluxTest;
import org.springframework.test.context.bean.override.mockito.MockitoBean;
import org.springframework.test.web.reactive.server.WebTestClient;
import reactor.core.publisher.Flux;
import reactor.core.publisher.Mono;
import reactor.test.StepVerifier;

import java.time.Duration;

import static org.mockito.BDDMockito.given;

class OrderReactiveTests {

    // (1) Flux que emite 3 pedidos e completa — contagem, sem casar valor a valor
    @Test
    void findAll_emiteTresPedidosECompleta() {
        OrderService orderService = // ... colaborador sob teste
        StepVerifier.create(orderService.findAll())
            .expectNextCount(3)
            .verifyComplete();
    }

    // (2) Caminho de erro: a sequência deve terminar com a exceção esperada
    @Test
    void findById_inexistente_emiteErro() {
        OrderService orderService = // ...
        StepVerifier.create(orderService.findById("nope"))
            .expectErrorMatches(e -> e instanceof OrderNotFoundException
                && e.getMessage().contains("nope"))
            .verify();
    }

    // (3) Delay de 1 hora testado em microssegundos com relógio virtual
    @Test
    void delayedOrder_naoEsperaTempoReal() {
        StepVerifier.withVirtualTime(() ->
                Mono.delay(Duration.ofHours(1)).thenReturn(new Order("o-1")))
            .expectSubscription()
            .expectNoEvent(Duration.ofHours(1)) // nada durante a janela virtual
            .thenAwait(Duration.ofHours(1))     // adianta o relógio 1h, instantâneo
            .expectNextMatches(o -> o.id().equals("o-1"))
            .verifyComplete();
    }
}

// (4) Reactive controller via fatia WebFlux + WebTestClient
@WebFluxTest(OrderController.class)
class OrderControllerWebFluxTests {

    @Autowired
    private WebTestClient webClient;

    @MockitoBean
    private OrderService orderService; // colaborador mockado, não sobe o real

    @Test
    void getOrders_retorna200ELista() {
        given(orderService.findAll())
            .willReturn(Flux.just(new Order("o-1"), new Order("o-2")));

        webClient.get().uri("/orders")
            .exchange()
            .expectStatus().isOk()
            .expectBodyList(Order.class).hasSize(2);
    }
}
```

> `Order`, `OrderService` e `Customer` são domínios neutros de exemplo. `Mono`/`Flux`/WebFlux vêm do Galho 11 — aqui só se **testa** o que eles produzem.

## Armadilhas

### (1) Usar block() no teste em vez de StepVerifier

Bloquear o publisher para "pegar o valor" parece prático, mas descarta tudo que é reativo: ordem dos sinais, propagação de erro, backpressure, e a própria assincronia. Se o fluxo nunca completar (um `Flux` infinito, um `Mono` que depende de um sinal que não chega), o teste **trava** até o timeout.

```java
// ERRADO — bloqueia, perde a natureza reativa, pode travar
Order o = orderService.findById("o-1").block();
assertEquals("o-1", o.id());

// CERTO — assina como assinante de teste e verifica o fluxo
StepVerifier.create(orderService.findById("o-1"))
    .expectNextMatches(found -> found.id().equals("o-1"))
    .verifyComplete();
```

**Fix**: trate `Mono`/`Flux` com `StepVerifier`. Reserve `block()` para `main()`/scripts, nunca para testes de fluxo.

### (2) Esquecer verifyComplete()/verify() no fim

Sem o `verify`, o `StepVerifier` **não assina** o publisher — a cadeia de `expectNext` é só uma descrição que nunca é exercida. O código de produção não roda, e o teste passa **verde** sem ter testado nada. É o falso positivo mais perigoso do reativo.

```java
// ERRADO — nenhum verify: o publisher NUNCA é assinado, nada executa, teste passa vazio
StepVerifier.create(orderService.findAll())
    .expectNextCount(3); // <- cadeia montada e... abandonada

// CERTO — verifyComplete() dispara a assinatura e valida o término
StepVerifier.create(orderService.findAll())
    .expectNextCount(3)
    .verifyComplete();
```

**Fix**: toda cadeia `StepVerifier` termina em `verifyComplete()` (término por `onComplete`) ou `verify()` (quando o esperado é erro). Sem isso, não há teste.

### (3) Testar um delay com tempo real

Validar um `Mono.delay(Duration.ofHours(1))` (ou retry com backoff, `Flux.interval`, timeout) com o relógio real é inviável — a suíte trava por uma hora, ou alguém mete um `Thread.sleep` que deixa o teste lento e flaky.

```java
// ERRADO — relógio real: o teste literalmente espera 1 hora (ou trava no timeout)
StepVerifier.create(Mono.delay(Duration.ofHours(1)).thenReturn(new Order("o-1")))
    .expectNextMatches(o -> o.id().equals("o-1"))
    .verifyComplete();

// CERTO — relógio virtual: thenAwait adianta o tempo, teste roda em microssegundos
StepVerifier.withVirtualTime(() ->
        Mono.delay(Duration.ofHours(1)).thenReturn(new Order("o-1")))
    .expectSubscription()
    .thenAwait(Duration.ofHours(1))
    .expectNextMatches(o -> o.id().equals("o-1"))
    .verifyComplete();
```

**Fix**: use `StepVerifier.withVirtualTime(() -> ...)` — passe o publisher dentro do `Supplier` (lambda) para que seja construído já sob o `VirtualTimeScheduler` — e adiante o relógio com `thenAwait(Duration)`.

## Em entrevista

### Frase pronta (inglês)

> To test reactive code I use `StepVerifier` from `reactor-test` — it acts as a test subscriber that asserts the stream signal by signal: `expectNext` for emitted items, `expectError` for the terminal error, and `verifyComplete` (or `verify`) at the end, which is what actually subscribes and runs the publisher. A common pitfall is omitting the `verify` call: without it the chain never subscribes, so the production code never executes and the test passes green having tested nothing. For time-based operators like delays, retries or intervals I switch to `StepVerifier.withVirtualTime`, which installs a virtual clock so `thenAwait(Duration.ofHours(1))` advances time instantly instead of blocking. For reactive controllers I rely on the `@WebFluxTest` slice, which boots only the WebFlux layer and auto-configures a `WebTestClient` to exercise endpoints non-blockingly, mocking collaborators with `@MockitoBean`.

### Vocabulário

| Termo (EN) | Como usar |
| --- | --- |
| test subscriber | "`StepVerifier` acts as a **test subscriber** that drives the publisher." |
| signal by signal | "It asserts the stream **signal by signal** — onNext, onError, onComplete." |
| terminal signal | "`verifyComplete` asserts the completion **terminal signal**." |
| virtual time | "`withVirtualTime` installs a **virtual time** scheduler to skip real delays." |
| to advance the clock | "`thenAwait` **advances the clock** instead of blocking the thread." |
| sliced test | "`@WebFluxTest` is a **sliced test** — only the WebFlux layer, not the full context." |
| to mock collaborators | "I **mock collaborators** like the service with `@MockitoBean`." |
| false positive | "Forgetting `verify` is a **false positive** — green but never subscribed." |

## Veja também

- [[03-Dominios/Tecnologia/Java/Testes/14 - Testando código assíncrono — Awaitility|Testando código assíncrono]]
- [[03-Dominios/Tecnologia/Java/Testes/12 - Testes de integração ponta a ponta|Testes de integração ponta a ponta]]
- [[03-Dominios/Tecnologia/Java/Programação Reativa/10 - Spring WebFlux — o stack não-bloqueante sobre Netty e o DispatcherHandler|Spring WebFlux]]
- [[03-Dominios/Tecnologia/Java/Programação Reativa/11 - WebClient — o cliente HTTP reativo a fundo|WebClient]]
- [[03-Dominios/Tecnologia/Java/Testes/index|Testes (MOC do galho)]]
- [[03-Dominios/Tecnologia/Java/index|Trilha Java]]
- [[03-Dominios/Tecnologia/Java/Dicionário de Java]]

## Referências

- Reactor Reference — Testing (`StepVerifier`, `withVirtualTime`, `reactor-test`): https://projectreactor.io/docs/core/release/reference/testing.html
- Spring Boot — Testing applications (`@WebFluxTest`, `WebTestClient`): https://docs.spring.io/spring-boot/reference/testing/spring-boot-applications.html
