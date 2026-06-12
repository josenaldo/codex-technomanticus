---
title: "Resiliência I — a falha distribuída e o Circuit Breaker"
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
  - "Circuit Breaker"
  - "Resilience4j Circuit Breaker"
---

# Resiliência I — a falha distribuída e o Circuit Breaker

> [!abstract] TL;DR
> Num sistema distribuído, **a rede é o inimigo**: chamadas remotas falham, demoram ou somem — e uma falha num serviço lento pode se propagar e derrubar todo mundo (**cascading failure**). O **Circuit Breaker** (disjuntor) é o padrão que protege seu serviço de bater repetidamente numa porta que não abre: ele *monitora* a taxa de falhas e, quando ela passa de um limiar, **abre o circuito** e passa a rejeitar chamadas instantaneamente (devolvendo um *fallback*), em vez de esperar por timeouts. No ecossistema Java moderno, a implementação de referência é o **Resilience4j 2.4.0** (mar/2025, baseline Java 17). O disjuntor tem três estados normais — **CLOSED**, **OPEN** e **HALF_OPEN** — mais dois especiais (**DISABLED**, **FORCED_OPEN**), e decide com base numa **janela deslizante** (*count-based* ou *time-based*). Esta é a porta de entrada da resiliência: as notas seguintes cobrem Retry, Time Limiter, Bulkhead e a composição de tudo.

## O que é

O **Circuit Breaker** (disjuntor de circuito) é um padrão de resiliência que envolve uma chamada potencialmente arriscada — tipicamente uma chamada de rede a outro serviço — e monitora seus resultados. Quando a proporção de falhas (ou de chamadas lentas) ultrapassa um limiar configurado, o disjuntor **"abre"**: a partir daí, ele para de deixar as chamadas passarem e devolve um erro imediato (ou um valor de contingência) sem nem tentar contatar o serviço problemático.

A analogia é literalmente um disjuntor elétrico. Quando há um curto-circuito, o disjuntor da sua casa desarma e corta a energia — não para te incomodar, mas para evitar que o curto vire incêndio. Ele fica desarmado por um tempo; depois você pode rearmá-lo para *testar* se o problema passou. Se persistir, ele desarma de novo. O Circuit Breaker de software faz exatamente isso: corta o fluxo para um serviço doente, espera, e periodicamente testa se ele se recuperou.

A implementação canônica em Java é a biblioteca **[Resilience4j](https://resilience4j.readme.io/docs/circuitbreaker)**, cuja versão estável é a **2.4.0** (lançada em março de 2025, com baseline **Java 17**). Ela é leve, funcional (decora `Supplier`/`Function`/`CompletableFuture`) e integra-se ao Spring Boot 3 via um *starter* dedicado.

> [!warning] Não existe Resilience4j 3.x estável
> A linha estável é a **2.x** (atualmente **2.4.0**, Java 17). Uma eventual v3 com baseline Java 21 é **roadmap não lançado** — descarte qualquer referência a "Resilience4j 3.0 estável". Ver a armadilha (3) abaixo.

## Por que importa

### A rede é o inimigo

Numa aplicação monolítica, chamar outro componente é uma invocação de método: rápida, confiável, dentro do mesmo processo. Num sistema distribuído, "chamar outro serviço" significa atravessar a **rede** — e a rede mente. As **falácias da computação distribuída** começam justamente com "a rede é confiável", "a latência é zero" e "a largura de banda é infinita". Nenhuma dessas é verdade.

Isso introduz um modo de falha que o monólito não tinha: a **falha parcial**. Seu serviço está perfeitamente saudável, mas o `payment-service` que ele chama está fora do ar, ou — pior — está *lento*. A falha parcial é traiçoeira porque ela não é binária: o serviço não está "morto", ele está "respondendo em 30 segundos em vez de 50 milissegundos".

### Cascading failure (falha em cascata)

E aqui mora o perigo real. Imagine que o `order-service` chama o `payment-service` de forma síncrona. O `payment-service` fica lento. O que acontece com o `order-service`?

Cada thread do `order-service` que faz uma chamada de pagamento fica **bloqueada esperando**. Como as requisições continuam chegando, o pool de threads (ou de conexões) do `order-service` se esgota rapidamente — todas as threads estão paradas esperando um serviço que não responde. Agora o `order-service` também parou de responder. E se algum `checkout-service` chama o `order-service`, ele trava também. A doença de um serviço se **propaga em cascata** por toda a malha.

> [!info] A intuição contra-intuitiva
> Um serviço **lento** é frequentemente mais perigoso que um serviço **morto**. Um serviço morto te dá um erro de conexão na hora; você falha rápido e libera a thread. Um serviço lento *segura* suas threads, e é assim que ele te arrasta para o fundo junto com ele. Por isso o Circuit Breaker se importa não só com *falhas*, mas com *chamadas lentas* (`slowCallRateThreshold`).

O Circuit Breaker quebra essa cadeia: ao detectar que o `payment-service` está doente, ele **abre** e passa a rejeitar as chamadas em microssegundos, sem bloquear thread alguma. O `order-service` permanece responsivo, devolve um fallback ("pagamento indisponível, tente em instantes") e — de quebra — dá ao `payment-service` uma trégua para se recuperar, em vez de bombardeá-lo com retentativas enquanto ele agoniza.

## Como funciona

### Os estados do disjuntor (3 normais + 2 especiais)

O Resilience4j modela o Circuit Breaker como uma **máquina de estados finita**. Os três estados normais são:

- **CLOSED** (fechado) — o estado saudável. O circuito está fechado *como um circuito elétrico fechado*: a corrente (as chamadas) passa normalmente. O disjuntor registra cada resultado na janela deslizante. Enquanto a taxa de falha estiver abaixo do limiar, fica aqui.
- **OPEN** (aberto) — o estado de proteção. A taxa de falha estourou o limiar, o circuito **abriu** e as chamadas **não passam mais**: o Resilience4j as rejeita imediatamente lançando `CallNotPermittedException`. Ele fica neste estado por `waitDurationInOpenState`.
- **HALF_OPEN** (meio-aberto) — o estado de teste. Depois do tempo de espera, o disjuntor entreabre a porta: permite um número configurável de chamadas de prova (`permittedNumberOfCallsInHalfOpenState`) passarem. Se elas tiverem sucesso (taxa de falha abaixo do limiar), o circuito volta para **CLOSED**. Se falharem, volta para **OPEN** e o relógio recomeça.

> [!example] O ciclo de vida em uma frase
> CLOSED (passa tudo) → falhas demais → OPEN (rejeita tudo) → espera → HALF_OPEN (deixa algumas provas passarem) → provas OK → CLOSED, ou → provas falham → OPEN.

Além desses, há dois estados **especiais**, acionados manualmente (via API ou métricas), que *não* fazem transições automáticas:

- **DISABLED** — desligado. Sempre permite o acesso e **não registra métricas** nem dispara transições. Útil para suspender o disjuntor sem removê-lo do código.
- **FORCED_OPEN** — forçadamente aberto. Sempre nega o acesso e também não registra métricas. Útil para tirar manualmente um serviço de circulação (ex.: durante uma manutenção conhecida).

> [!note] Curiosidade: METRICS_ONLY
> A documentação do Resilience4j cita ainda um estado `METRICS_ONLY`, que permite todas as chamadas e *registra métricas*, mas nunca abre. Para entrevista, foque nos 3 normais + 2 especiais (DISABLED/FORCED_OPEN); o METRICS_ONLY é um detalhe de observabilidade.

### Janela deslizante: count-based vs time-based

Como o disjuntor *sabe* que "as falhas passaram do limiar"? Ele guarda os resultados das chamadas recentes numa **janela deslizante** (*sliding window*) e calcula a taxa sobre ela. Há dois tipos, escolhidos por `slidingWindowType`:

- **COUNT_BASED** (baseada em contagem) — guarda o resultado das últimas **N chamadas** (`slidingWindowSize`, default 100). Implementada como um array circular. A taxa de falha é "X das últimas 100 chamadas falharam". É o **default**.
- **TIME_BASED** (baseada em tempo) — guarda os resultados dos últimos **N segundos** (`slidingWindowSize` passa a significar segundos), usando agregações parciais por segundo. A taxa é "X% das chamadas nos últimos 10 segundos falharam".

A escolha importa: **count-based** é mais previsível sob carga uniforme; **time-based** lida melhor com tráfego irregular, porque uma rajada antiga não fica "presa" na janela esperando ser empurrada para fora por chamadas novas que talvez nunca venham.

### Thresholds e minimumNumberOfCalls

A decisão de abrir é governada por alguns limiares. Os defaults do Resilience4j 2.4.0:

| Propriedade | Default | O que faz |
| --- | --- | --- |
| `failureRateThreshold` | **50%** | Taxa de falha que dispara a transição para OPEN. |
| `slowCallRateThreshold` | **100%** | Percentual de chamadas *lentas* que também dispara OPEN. |
| `slowCallDurationThreshold` | **60s** (60000 ms) | Acima disso, a chamada conta como "lenta". |
| `minimumNumberOfCalls` | **100** | Chamadas mínimas registradas na janela antes de o disjuntor *calcular* qualquer taxa. |
| `slidingWindowSize` | **100** | Tamanho da janela (chamadas se COUNT, segundos se TIME). |
| `slidingWindowType` | **COUNT_BASED** | Tipo da janela. |
| `waitDurationInOpenState` | **60s** | Tempo em OPEN antes de ir para HALF_OPEN. |
| `permittedNumberOfCallsInHalfOpenState` | **10** | Chamadas de prova permitidas em HALF_OPEN. |

> [!tip] O papel do `minimumNumberOfCalls`
> Esse parâmetro é o que impede falsos positivos no *cold start*. Se uma das suas duas primeiras chamadas falhar, a taxa "é 50%" — mas isso é ruído estatístico, não um padrão. O `minimumNumberOfCalls` diz "não confie na taxa enquanto eu não tiver pelo menos N amostras". Com o default de 100, o disjuntor só *começa* a poder abrir depois de 100 chamadas registradas — o que é alto demais para muitos cenários (ver armadilha 1).

## Na prática

Em uma aplicação Spring Boot 3, a configuração mora no `application.yml` e a decoração é declarativa via anotação `@CircuitBreaker`.

### Dependência (starter Boot 3)

```xml
<!-- pom.xml -->
<dependency>
    <groupId>io.github.resilience4j</groupId>
    <artifactId>resilience4j-spring-boot3</artifactId>
    <version>2.4.0</version>
</dependency>

<!-- Companheiros obrigatórios: o starter precisa de actuator + aop -->
<dependency>
    <groupId>org.springframework.boot</groupId>
    <artifactId>spring-boot-starter-actuator</artifactId>
</dependency>
<dependency>
    <groupId>org.springframework.boot</groupId>
    <artifactId>spring-boot-starter-aop</artifactId>
</dependency>
```

> [!note] Por que actuator e aop?
> O `spring-boot-starter-aop` habilita a interceptação por *aspectos* que faz a anotação `@CircuitBreaker` funcionar (o método é envolvido por um proxy). O `spring-boot-starter-actuator` expõe os endpoints de saúde e métricas do disjuntor (`/actuator/circuitbreakers`, `/actuator/circuitbreakerevents`), que você vai querer para observar os estados em produção.

### Configuração do CircuitBreaker

```yaml
# application.yml — o order-service protegendo as chamadas ao payment-service
resilience4j:
  circuitbreaker:
    instances:
      paymentService:
        sliding-window-type: COUNT_BASED          # ou TIME_BASED
        sliding-window-size: 20                    # últimas 20 chamadas
        minimum-number-of-calls: 10                # só calcula taxa após 10 chamadas
        failure-rate-threshold: 50                 # abre se >= 50% falharem
        slow-call-rate-threshold: 100              # abre se 100% forem lentas
        slow-call-duration-threshold: 2s           # "lenta" = acima de 2s
        wait-duration-in-open-state: 10s           # tempo em OPEN antes de HALF_OPEN
        permitted-number-of-calls-in-half-open-state: 5
        automatic-transition-from-open-to-half-open-enabled: true
        register-health-indicator: true
```

> [!info] Defaults vs. produção
> Note que aqui os valores foram *reduzidos* em relação aos defaults da biblioteca (que são pensados para alto volume): janela de 20, `minimum-number-of-calls` de 10 e `wait-duration` de 10s. Em um serviço de baixo/médio tráfego, os defaults (`minimumNumberOfCalls: 100`, `waitDurationInOpenState: 60s`) fariam o disjuntor praticamente nunca disparar a tempo. **Dimensione a janela ao seu volume real.**

### Decoração com `@CircuitBreaker` e fallback

```java
// order-service: o cliente que chama o payment-service
@Service
public class PaymentClient {

    private final RestClient restClient;

    public PaymentClient(RestClient restClient) {
        this.restClient = restClient;
    }

    // 'name' aponta para a instância configurada no YAML;
    // 'fallbackMethod' é chamado quando o circuito abre ou a chamada falha.
    @CircuitBreaker(name = "paymentService", fallbackMethod = "pagamentoIndisponivel")
    public PaymentResult cobrar(OrderId orderId, Money valor) {
        return restClient.post()
                .uri("http://payment-service/charges")
                .body(new ChargeRequest(orderId, valor))
                .retrieve()
                .body(PaymentResult.class);
    }

    // O fallback DEVE ter a mesma assinatura + um parâmetro de exceção no fim.
    // É invocado tanto para falhas normais quanto para CallNotPermittedException
    // (circuito aberto).
    private PaymentResult pagamentoIndisponivel(OrderId orderId, Money valor, Throwable t) {
        // Degrade graciosamente: enfileire para processamento assíncrono,
        // retorne um status PENDENTE, etc. — nunca propague o erro cru.
        return PaymentResult.pendente(orderId, "Pagamento temporariamente indisponível");
    }
}
```

A mecânica: enquanto `paymentService` estiver **CLOSED**, `cobrar(...)` executa normalmente. Quando as falhas/lentidões passam do limiar, o disjuntor vai para **OPEN** e, a partir daí, *nem entra* no corpo do método — vai direto para `pagamentoIndisponivel(...)`, devolvendo a contingência em microssegundos. Depois de `wait-duration-in-open-state`, ele entra em **HALF_OPEN** e deixa 5 chamadas de prova tentarem o `payment-service` de verdade.

## Armadilhas

### (1) Janela deslizante mal dimensionada — abre cedo demais ou tarde demais

Os defaults do Resilience4j (`slidingWindowSize: 100`, `minimumNumberOfCalls: 100`) são calibrados para serviços de **alto volume**. Num serviço que recebe poucas chamadas por minuto, o disjuntor pode levar *minutos* para acumular 100 amostras — ou seja, ele **abre tarde demais**, depois do estrago já feito. O oposto também acontece: uma janela pequena demais (ex.: `size: 5`, `minimum: 3`) reage a ruído estatístico e **abre cedo demais**, derrubando o circuito por causa de duas falhas transitórias. Dimensione a janela e o `minimumNumberOfCalls` ao volume real do endpoint — não copie os defaults cegamente.

### (2) Circuit Breaker sem fallback — a exceção só muda de roupa

Sem `fallbackMethod`, quando o circuito abre, o Resilience4j lança `CallNotPermittedException`. Se você não tratar isso, o erro **propaga** para cima exatamente como o erro original propagaria — você trocou um timeout por uma exceção, mas o cliente final continua recebendo um 500. O Circuit Breaker protege seu *serviço* de gastar recursos, mas só entrega uma boa **experiência** se houver um fallback que degrade graciosamente (valor em cache, resposta parcial, status "pendente", fila assíncrona). CB sem fallback é meia resiliência.

### (3) Achar que existe Resilience4j 3.x estável (ou usar a versão errada)

A linha estável é a **2.x — atualmente 2.4.0 (mar/2025), baseline Java 17**. Não existe Resilience4j 3.0 estável lançado; uma v3 com baseline Java 21 é roadmap. Erros comuns daí: (a) tentar declarar `<version>3.0.0</version>` e quebrar o build; (b) usar o *starter* errado — em **Spring Boot 3** o artefato é `resilience4j-spring-boot3` (o antigo `resilience4j-spring-boot2` é para a linha Boot 2, com `javax.*` em vez de `jakarta.*`); (c) esquecer o `spring-boot-starter-aop`, fazendo a anotação `@CircuitBreaker` ser silenciosamente ignorada porque não há proxy para interceptá-la.

## Em entrevista

### Frase pronta (inglês)

> In a distributed system, the network is the enemy: remote calls fail, hang, or slow down, and a single slow downstream can exhaust your thread pool and trigger a cascading failure across the whole mesh. The Circuit Breaker pattern prevents that by monitoring the failure rate over a sliding window and, once it crosses a threshold, *opening* the circuit so calls are rejected instantly and routed to a fallback instead of piling up against an unhealthy service. In the Java ecosystem I'd reach for Resilience4j — its breaker moves between CLOSED, OPEN, and HALF_OPEN, and I tune the sliding window, failure-rate threshold, and minimum number of calls to the actual traffic volume rather than trusting the high-volume defaults.

### Vocabulário

| Português | Inglês |
| --- | --- |
| disjuntor | circuit breaker |
| janela deslizante | sliding window |
| taxa de falha | failure rate |
| falha em cascata | cascading failure |
| alternativa de contingência | fallback |
| meio-aberto | half-open |
| esgotamento do pool de threads | thread pool exhaustion |
| falha parcial | partial failure |

## Veja também

- [[03-Dominios/Java/Microservices e sistemas distribuídos/14 - Resiliência II — Retry e Time Limiter|Retry e Time Limiter]]
- [[03-Dominios/Java/Microservices e sistemas distribuídos/16 - Resiliência IV — compondo os padrões|Compondo os padrões de resiliência]]
- [[03-Dominios/Java/Microservices e sistemas distribuídos/21 - Os padrões de falha distribuída|Os padrões de falha distribuída]]
- [[03-Dominios/Java/Microservices e sistemas distribuídos/index|Microservices e sistemas distribuídos (MOC do galho)]]
- [[03-Dominios/Java/index|Trilha Java]]

> [!note] Onde isto se encaixa
> Esta é a **porta de entrada da resiliência** no galho de Microservices. As próximas notas dão sequência: **Resiliência II** cobre Retry e Time Limiter, **III** cobre Bulkhead e Rate Limiter (planejado), e **IV** compõe todos os decoradores na ordem correta. As notas sobre malha de serviço e observabilidade do galho 17/18 (planejado) tratam de onde *aplicar* esses padrões em escala.

## Referências

- Resilience4j — [CircuitBreaker](https://resilience4j.readme.io/docs/circuitbreaker) (estados, janela deslizante e defaults de configuração). Acesso em 2026-06-12.
- Resilience4j — [Getting Started with Spring Boot 3](https://resilience4j.readme.io/docs/getting-started-3) (*starter* `resilience4j-spring-boot3`, dependências actuator + aop, anotação `@CircuitBreaker`). Acesso em 2026-06-12.
- Resilience4j — versão estável **2.4.0** (março de 2025), baseline **Java 17**. Não há linha 3.x estável lançada (verificado em 2026-06-12).
