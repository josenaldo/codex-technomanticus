---
title: "Resiliência IV — compondo os padrões"
created: 2026-06-12
updated: 2026-06-12
type: concept
status: seedling
publish: true
fase: adepto
tags:
  - java
  - microservices
  - adepto
  - resiliencia
  - resilience4j
aliases:
  - "Compondo padrões de resiliência"
  - "Ordem dos aspectos Resilience4j"
  - "Spring Cloud Circuit Breaker"
---

# Resiliência IV — compondo os padrões

> [!abstract] TL;DR
> Os padrões de resiliência (Retry, Circuit Breaker, Rate Limiter, Time Limiter, Bulkhead) raramente vivem sozinhos — você os **compõe** numa mesma chamada. No Resilience4j (2.4.0, Java 17), quando você empilha as anotações, elas se aninham numa **ordem de aspectos** fixa, do mais externo ao mais interno: `Retry( CircuitBreaker( RateLimiter( TimeLimiter( Bulkhead( fn ) ) ) ) )`. O **Retry é o mais externo** — ele reexecuta tudo que está dentro. Essa ordem importa: como o Circuit Breaker está *dentro* do Retry, cada tentativa do Retry conta uma falha no contador do CB, podendo "inflar" o disjuntor. Você customiza a ordem com as propriedades `...AspectOrder` (maior valor = mais externo). O **fallback** (`fallbackMethod`) é a contingência quando tudo falha. E o **Spring Cloud Circuit Breaker** é uma *abstração* (`CircuitBreakerFactory`) por cima do Resilience4j — útil pra portabilidade, mas esconde parte do tuning fino.

## O que é

As notas anteriores deste galho cada uma trata de um padrão isolado: o [[03-Dominios/Java/Microservices e sistemas distribuídos/13 - Resiliência I — a falha distribuída e o Circuit Breaker|Circuit Breaker]] que abre quando o serviço-alvo está doente; o [[03-Dominios/Java/Microservices e sistemas distribuídos/14 - Resiliência II — Retry e Time Limiter|Retry e o Time Limiter]] que reexecutam e cortam chamadas lentas; o [[03-Dominios/Java/Microservices e sistemas distribuídos/15 - Resiliência III — Bulkhead e Rate Limiter|Bulkhead e o Rate Limiter]] que isolam e limitam.

Na vida real, uma única chamada a um serviço remoto costuma querer **todos eles ao mesmo tempo**: limitar quantas chamadas concorrentes (Bulkhead), abortar se demorar demais (Time Limiter), não estourar a cota do alvo (Rate Limiter), abrir o disjuntor se o alvo está caído (Circuit Breaker) e, só então, talvez tentar de novo (Retry).

Esta nota é a **síntese**: como esses decoradores se **compõem** numa mesma invocação, em que **ordem** eles se aninham, e o que fazer quando, mesmo com tudo isso, a chamada falha (o **fallback**). Também cobre a escolha entre usar o **Resilience4j direto** ou a **abstração do Spring Cloud Circuit Breaker**.

> [!info] Versões cravadas
> Resilience4j **2.4.0**, baseline **Java 17**. Starter direto: `resilience4j-spring-boot3`. Abstração: `spring-cloud-starter-circuitbreaker-resilience4j`.

## Por que importa

Compor padrões não é "ligar todas as anotações e torcer". A **ordem de aninhamento** muda o comportamento observável do sistema — e ela é, por padrão, **fixa e invisível**. Se você não sabe que o Retry está *por fora* do Circuit Breaker, vai se surpreender quando o disjuntor abrir "cedo demais": cada retry conta como uma falha separada no CB.

Pense numa boneca russa (matrioska). A chamada de verdade está lá no centro. Cada padrão é uma boneca que envolve a anterior. Quem está mais por fora "vê" a chamada inteira (incluindo o que as bonecas internas fizeram); quem está mais por dentro só vê a função crua. Trocar a ordem das bonecas muda quem reage a quê — e é exatamente isso que a propriedade `aspectOrder` permite.

Do ponto de vista de entrevista, este é o tópico onde o entrevistador separa quem "usou Resilience4j num tutorial" de quem **operou** resiliência em produção: a pergunta clássica é *"em que ordem o Retry e o Circuit Breaker se compõem, e por quê?"*.

## Como funciona

### A ordem dos aspectos (e por que importa)

Quando você empilha as anotações do Resilience4j no mesmo método, o framework as aplica como **aspectos AOP aninhados**. A ordem default, do **mais externo ao mais interno**, é:

```
Retry( CircuitBreaker( RateLimiter( TimeLimiter( Bulkhead( fn ) ) ) ) )
```

Lendo de fora pra dentro:

1. **Retry** é o mais externo — reexecuta *tudo* o que está dentro dele.
2. **CircuitBreaker** — decide se a chamada interna sequer acontece (aberto = curto-circuito).
3. **RateLimiter** — segura a chamada se a cota de permissões estourou.
4. **TimeLimiter** — aborta se a chamada interna demora demais.
5. **Bulkhead** — limita a concorrência, o mais interno.
6. **`fn`** — a chamada de verdade.

**Por que essa ordem importa.** Como o **Circuit Breaker está dentro do Retry**, cada tentativa que o Retry faz passa *de novo* pelo CB. Se o Retry tenta 3 vezes e todas falham, o CB registra **3 falhas**, não 1. Em alto volume, isso pode **inflar o contador de falha do CB** e abrir o disjuntor mais rápido do que a sua intenção. Essa é uma armadilha conhecida da ordem default (há *issues* registradas sobre exatamente esse comportamento Retry-por-fora-do-CB).

**Como customizar.** Cada padrão expõe uma propriedade `...AspectOrder`, e a regra é simples: **maior valor = mais externo**. Por exemplo, pra colocar o Circuit Breaker *por fora* do Retry (de modo que o CB conte uma falha por chamada lógica, não por tentativa), você dá ao `retryAspectOrder` um valor **menor** que o `circuitBreakerAspectOrder`:

- `resilience4j.retry.retryAspectOrder`
- `resilience4j.circuitbreaker.circuitBreakerAspectOrder`
- `resilience4j.ratelimiter.rateLimiterAspectOrder`
- `resilience4j.timelimiter.timeLimiterAspectOrder`
- `resilience4j.bulkhead.bulkheadAspectOrder`

> [!tip] Regra mnemônica
> "Maior número, mais por fora." O aspecto com o maior `aspectOrder` é a boneca russa externa; o menor é a que abraça a função crua.

### Fallback — a contingência quando tudo falha

Compor padrões reduz a chance de falha, mas não a zera. Quando *todas* as camadas falham (Retry esgotado, CB aberto, time-out estourado), você ainda precisa **devolver alguma coisa** ao chamador. É o **fallback**.

No Resilience4j com Spring, isso é o atributo `fallbackMethod` da anotação. O método de fallback:

- **vive na mesma classe** do método decorado;
- tem a **mesma assinatura** do método original, **mais um parâmetro de exceção** no fim;
- esse parâmetro pode ser `Throwable` (pega tudo) ou um tipo mais específico — o Resilience4j escolhe o handler **mais específico** que casa com a exceção lançada.

Aceitar `Throwable` é o "pega-tudo" pragmático: garante que nenhuma falha escape sem fallback. Mas (ver Armadilhas) cuidado com o que esse fallback devolve — um fallback que mascara a falha com dado errado é pior que a falha.

### Spring Cloud Circuit Breaker: abstração vs Resilience4j direto

Existem dois jeitos de chegar ao Resilience4j num app Spring Boot:

**1. Resilience4j direto** — starter `resilience4j-spring-boot3`. Você usa as anotações (`@CircuitBreaker`, `@Retry`, `@Bulkhead`, `@TimeLimiter`, `@RateLimiter`) e configura tudo no `application.yml` sob `resilience4j.*`. Acesso total a cada parâmetro, incluindo a ordem dos aspectos.

**2. Spring Cloud Circuit Breaker** — starter `spring-cloud-starter-circuitbreaker-resilience4j`. É uma **abstração** que vive no Spring Cloud Commons e expõe uma API neutra de fornecedor: a `CircuitBreakerFactory`. Você cria um `CircuitBreaker` a partir da fábrica e envolve a chamada programaticamente:

```java
circuitBreakerFactory.create("payment-call")
    .run(() -> paymentClient.charge(order), throwable -> fallbackResponse());
```

O ponto da abstração é a **portabilidade**: a mesma `CircuitBreakerFactory` pode ser respaldada por Resilience4j, Spring Retry ou o retry nativo do Spring Framework. Você troca a implementação trocando o starter, sem reescrever a lógica de negócio.

**Quando usar qual:**

| Situação | Escolha |
|---|---|
| Quer tuning fino (aspectOrder, sliding window, half-open detalhado) | **Resilience4j direto** |
| Quer poder trocar a engine de resiliência sem mexer no código | **Spring Cloud (abstração)** |
| Equipe já domina as anotações Resilience4j | **Resilience4j direto** |
| Código de biblioteca que não quer acoplar a um fornecedor | **Spring Cloud (abstração)** |
| Precisa de Rate Limiter / Bulkhead / Time Limiter compostos | **Resilience4j direto** (a abstração foca no circuit breaker) |

> [!warning] A abstração não expõe tudo
> A `CircuitBreakerFactory` cobre bem o *circuit breaker* (e parcialmente retry/time-limit, conforme o adapter), mas **não dá acesso ergonômico à composição completa** (Bulkhead + Rate Limiter + ordem de aspectos). Se você precisa orquestrar os cinco padrões com ordem customizada, vá de Resilience4j direto.

## Na prática

Composição completa num cliente de pagamentos, do ponto de vista de um `order-service` que chama um `payment-service`. As cinco anotações no mesmo método, com `fallbackMethod`:

```java
@Service
public class PaymentClient {

    private final PaymentApi api;

    public PaymentClient(PaymentApi api) {
        this.api = api;
    }

    // Aninhamento default: Retry( CircuitBreaker( RateLimiter( TimeLimiter( Bulkhead( charge ) ) ) ) )
    @Retry(name = "payment-service", fallbackMethod = "chargeFallback")
    @CircuitBreaker(name = "payment-service")
    @RateLimiter(name = "payment-service")
    @TimeLimiter(name = "payment-service")
    @Bulkhead(name = "payment-service", type = Bulkhead.Type.SEMAPHORE)
    public CompletableFuture<PaymentResult> charge(Order order) {
        return CompletableFuture.supplyAsync(() -> api.charge(order));
    }

    // Fallback na MESMA classe; mesma assinatura + Throwable no fim.
    // Devolve um resultado HONESTO de "não confirmado", nunca um falso "pago".
    private CompletableFuture<PaymentResult> chargeFallback(Order order, Throwable t) {
        log.warn("Pagamento indisponível para order {}: {}", order.id(), t.toString());
        return CompletableFuture.completedFuture(
            PaymentResult.unconfirmed(order.id(), "payment-service indisponível"));
    }
}
```

Configuração e **customização da ordem dos aspectos** — aqui colocamos o Circuit Breaker *por fora* do Retry, pra que o CB conte uma falha por chamada lógica (não por tentativa de retry):

```yaml
resilience4j:
  circuitbreaker:
    # maior valor = mais externo -> CB envolve o Retry
    circuitBreakerAspectOrder: 3
    instances:
      payment-service:
        sliding-window-type: COUNT_BASED
        sliding-window-size: 20
        failure-rate-threshold: 50
        wait-duration-in-open-state: 10s
  retry:
    # menor que o do CB -> Retry fica por DENTRO do CB
    retryAspectOrder: 2
    instances:
      payment-service:
        max-attempts: 3
        wait-duration: 200ms
  ratelimiter:
    rateLimiterAspectOrder: 1
    instances:
      payment-service:
        limit-for-period: 50
        limit-refresh-period: 1s
  timelimiter:
    instances:
      payment-service:
        timeout-duration: 2s
  bulkhead:
    instances:
      payment-service:
        max-concurrent-calls: 25
```

> [!note] Time Limiter exige `CompletableFuture`
> Como na nota 14, o `@TimeLimiter` só atua sobre métodos que retornam `CompletableFuture` (ou tipos reativos). Por isso o `charge` devolve `CompletableFuture<PaymentResult>` e o fallback acompanha a mesma assinatura.

## Armadilhas

### (1) Ordem errada inflando o Circuit Breaker

Na ordem default, **o Retry está por fora do CB**, então o CB vê cada tentativa como uma falha independente. Um Retry de 3 tentativas que falha registra **3 falhas** no contador do disjuntor — em volume, isso abre o CB "cedo demais", às vezes derrubando um alvo que estava só com soluços. Se a sua intenção é que o CB conte **uma falha por chamada lógica**, inverta a ordem via `aspectOrder` (CB com valor maior que o Retry), colocando o **Circuit Breaker por fora do Retry**. Decida conscientemente — não aceite a ordem default sem entender o que ela faz com as suas métricas.

### (2) A abstração escondendo o tuning

O `spring-cloud-starter-circuitbreaker-resilience4j` é ótimo pra portabilidade, mas a `CircuitBreakerFactory` **abstrai justamente os botões que você mais precisa em produção**: a ordem dos aspectos, a composição de Bulkhead + Rate Limiter, parâmetros finos do sliding window. Times que adotam a abstração "porque é Spring Cloud" e depois precisam de tuning acabam vazando configuração Resilience4j por baixo do pano — perdendo a portabilidade que justificava a abstração em primeiro lugar. Escolha a abstração só se a portabilidade for um requisito **real**; caso contrário, Resilience4j direto é mais honesto.

### (3) Fallback que mascara a falha devolvendo dado errado silenciosamente

O fallback mais perigoso é o que "funciona": devolve um valor plausível e o sistema segue como se nada tivesse acontecido. Um `chargeFallback` que retorna `PaymentResult.paid()` quando o `payment-service` está caído cria um **pedido pago que nunca foi cobrado** — uma inconsistência silenciosa que só aparece na conciliação financeira, dias depois. O fallback deve devolver um estado **honesto e seguro**: "não confirmado", "indisponível", cache antigo *marcado como stale*, ou propagar um erro tratável. Fallback não é "fingir sucesso"; é "degradar com integridade". E sempre **logue/monitore** o fallback — um fallback silencioso esconde o sintoma do problema real.

## Em entrevista

### Frase pronta (inglês)

> In production, resilience patterns are composed, not used in isolation. With Resilience4j, the decorators nest in a fixed aspect order — from outermost to innermost: Retry, Circuit Breaker, Rate Limiter, Time Limiter, Bulkhead — so Retry wraps the Circuit Breaker by default. That default has a well-known side effect: because the Circuit Breaker sits inside the Retry, every retry attempt increments the breaker's failure counter, which can trip it earlier than intended; I customize this with the `aspectOrder` properties, where a higher value means a more outer aspect. For the last line of defense I use a `fallbackMethod` in the same class, with the original signature plus a `Throwable`, and I'm careful that the fallback degrades honestly instead of silently returning wrong data. When portability across resilience engines matters I reach for the Spring Cloud Circuit Breaker abstraction and its `CircuitBreakerFactory`, but when I need fine-grained tuning I go straight to Resilience4j.

### Vocabulário

| Português | Inglês |
|---|---|
| ordem dos aspectos | aspect order |
| composição | composition |
| alternativa de contingência | fallback |
| fábrica de disjuntor | circuit breaker factory |
| abstração | abstraction |
| decorador | decorator |
| aninhamento | nesting |
| degradação graciosa | graceful degradation |

## Veja também

- [[03-Dominios/Java/Microservices e sistemas distribuídos/13 - Resiliência I — a falha distribuída e o Circuit Breaker|Circuit Breaker]]
- [[03-Dominios/Java/Microservices e sistemas distribuídos/14 - Resiliência II — Retry e Time Limiter|Retry e Time Limiter]]
- [[03-Dominios/Java/Microservices e sistemas distribuídos/15 - Resiliência III — Bulkhead e Rate Limiter|Bulkhead e Rate Limiter]]
- [[03-Dominios/Java/Microservices e sistemas distribuídos/21 - Os padrões de falha distribuída|Os padrões de falha distribuída]]
- [[03-Dominios/Java/Microservices e sistemas distribuídos/index|Microservices e sistemas distribuídos (MOC do galho)]]
- [[03-Dominios/Java/index|Trilha Java]]

> [!note] Galhos seguintes
> Observabilidade e tracing distribuído (galho 17) e segurança em sistemas distribuídos (galho 18) ainda estão **(planejado)**.

## Referências

- Resilience4j — Getting Started (Spring Boot 3), aspect order e `fallbackMethod`: https://resilience4j.readme.io/docs/getting-started-3
- Spring Cloud Circuit Breaker — referência (`CircuitBreakerFactory`, starter `spring-cloud-starter-circuitbreaker-resilience4j`): https://docs.spring.io/spring-cloud-circuitbreaker/reference/
