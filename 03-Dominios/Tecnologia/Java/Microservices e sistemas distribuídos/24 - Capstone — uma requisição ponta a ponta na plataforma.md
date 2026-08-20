---
title: "Capstone — uma requisição ponta a ponta na plataforma"
created: 2026-06-12
updated: 2026-06-12
type: concept
status: seedling
publish: true
fase: magus
tags:
  - java
  - microservices
  - magus
  - capstone
aliases:
  - "Capstone Microservices"
  - "Requisição ponta a ponta"
---

# Capstone — uma requisição ponta a ponta na plataforma

> [!abstract] TL;DR
> Uma única requisição HTTP — "criar um pedido" — atravessa **toda** a plataforma de microservices: entra pelo **gateway**, que aplica predicates e filters; é roteada para o `order-service`, que precisa cobrar o cliente. Para isso, ele **descobre** onde mora o `payment-service` (discovery), escolhe **uma instância** (client-side load balancing), e faz a chamada **embrulhada em resiliência** (time limiter + circuit breaker + retry). Se o pagamento for **assíncrono**, em vez de chamar direto ele publica um evento ([[03-Dominios/Tecnologia/Java/Mensageria/index|Galho 14]]) e aceita **consistência eventual**. Durante tudo isso, um único **traceId** propaga pelos serviços, costurando os logs numa história só. Esta nota não introduz nada novo — ela **costura os 23 conceitos** anteriores numa narrativa de ponta a ponta.

## O que é

Os 23 conceitos anteriores deste galho foram apresentados **um de cada vez**: discovery numa nota, load balancing em outra, circuit breaker noutra. Isso é ótimo para aprender, mas é **mentiroso sobre a realidade**. Numa plataforma de verdade, esses conceitos não acontecem em isolamento — eles colapsam todos no **caminho de uma única requisição**.

Esta nota faz o movimento inverso da decomposição: pega **uma requisição concreta** e mostra cada conceito se ativando, na ordem, no momento em que a requisição passa por ele. É o capstone de **síntese** do galho.

A requisição que vamos seguir:

> Um cliente clica em "Finalizar pedido". O frontend chama `POST /api/orders`. Essa chamada precisa criar o pedido (`order-service`) **e** cobrar o cartão (`payment-service`). Vamos seguir esse byte do gateway até a resposta voltar.

> [!info] Por que "ponta a ponta" e não "componente a componente"
> Pense num jogo de futebol. Você pode estudar separadamente o que é um passe, um drible, um chute. Mas só entende o jogo quando vê **uma jogada inteira**: o passe que vira drible que vira chute que vira gol. O capstone é a jogada inteira. Cada conceito anterior é um fundamento isolado; aqui eles viram **futebol**.

## Por que importa

Quem só estudou os conceitos isolados comete dois erros previsíveis:

1. **Ativa o conceito errado na camada errada.** Coloca circuit breaker no gateway quando ele devia estar na chamada client-side; ou tenta fazer discovery na borda quando o gateway já resolve via service-name. Sem a visão de ponta a ponta, você não sabe **onde** cada peça mora.
2. **Acha que cada peça é independente.** Não é. O time limiter precisa ser **menor** que o timeout do retry, que precisa ser coerente com a janela do circuit breaker — senão os padrões brigam entre si (a lição de [[03-Dominios/Tecnologia/Java/Microservices e sistemas distribuídos/16 - Resiliência IV — compondo os padrões|Resiliência IV]]). E o traceId precisa **sobreviver** a todas essas camadas, ou seu trace fica cego no meio do caminho.

Em entrevista sênior, a pergunta clássica não é "o que é circuit breaker?" (júnior). É **"me conta o que acontece quando uma requisição entra no seu sistema"** (sênior). Esta nota é o roteiro dessa resposta.

## Como funciona

### O fluxo da requisição, passo a passo

Vamos seguir `POST /api/orders` desde a borda até a resposta. Cada passo cita a nota que o detalha.

1. **A borda: o gateway recebe.** A requisição bate no [[03-Dominios/Tecnologia/Java/Microservices e sistemas distribuídos/10 - API Gateway — papel, roteamento, predicates e filters|API Gateway]]. Um **predicate** (`Path=/api/orders/**`) decide que essa rota é do `order-service`; **filters** podem reescrever o path (`StripPrefix`), validar o token (cross-cutting, [[03-Dominios/Tecnologia/Java/Microservices e sistemas distribuídos/17 - Segurança entre serviços|segurança]]) e adicionar headers. O gateway é **WebFlux ou MVC** ([[03-Dominios/Tecnologia/Java/Microservices e sistemas distribuídos/11 - Gateway reativo vs MVC — as duas variantes|as duas variantes]]) — a escolha muda o starter, não o conceito.

2. **Resolver o destino: discovery.** O gateway não tem o IP do `order-service` cravado. Ele usa um **service-name** (`lb://order-service`) e pergunta ao [[03-Dominios/Tecnologia/Java/Microservices e sistemas distribuídos/06 - Service discovery — o conceito e o Eureka|service discovery]] (Eureka, [[03-Dominios/Tecnologia/Java/Microservices e sistemas distribuídos/07 - Discovery — Consul e Kubernetes-native|Consul ou k8s-native]]) quais instâncias de `order-service` estão vivas agora.

3. **Escolher a instância: load balancing.** Existem 3 instâncias de `order-service`. O [[03-Dominios/Tecnologia/Java/Microservices e sistemas distribuídos/08 - Client-side load balancing — Spring Cloud LoadBalancer|Spring Cloud LoadBalancer]] escolhe **uma** (round-robin por padrão). A requisição finalmente chega ao `order-service`.

4. **Dentro do order-service: a chamada para o payment.** O `order-service` precisa cobrar. Ele tem um cliente [[03-Dominios/Tecnologia/Java/Microservices e sistemas distribuídos/09 - Comunicação síncrona — OpenFeign e HTTP Interface|OpenFeign ou HTTP Interface]] declarativo para `payment-service`. Esse cliente **também** resolve via discovery + LB (passos 2 e 3 se repetem internamente). É [[03-Dominios/Tecnologia/Java/Microservices e sistemas distribuídos/05 - Comunicação inter-serviços — síncrono vs assíncrono|comunicação síncrona]].

5. **A chamada resiliente.** Aqui mora o coração da camada Magus. A chamada ao `payment-service` **não** é um `httpClient.post()` cru. Ela é embrulhada em [[03-Dominios/Tecnologia/Java/Microservices e sistemas distribuídos/13 - Resiliência I — a falha distribuída e o Circuit Breaker|Circuit Breaker]] + [[03-Dominios/Tecnologia/Java/Microservices e sistemas distribuídos/14 - Resiliência II — Retry e Time Limiter|Time Limiter + Retry]], possivelmente com [[03-Dominios/Tecnologia/Java/Microservices e sistemas distribuídos/15 - Resiliência III — Bulkhead e Rate Limiter|Bulkhead]] isolando o pool. A ordem de composição importa ([[03-Dominios/Tecnologia/Java/Microservices e sistemas distribuídos/16 - Resiliência IV — compondo os padrões|Resiliência IV]]).

6. **Config e segurança transversais.** Os timeouts, os nomes de instância de resiliência, as URLs base — nada disso está hard-coded. Vêm do [[03-Dominios/Tecnologia/Java/Microservices e sistemas distribuídos/12 - Config centralizado — Spring Cloud Config|Config centralizado]]. E a chamada interna carrega credencial de serviço-para-serviço ([[03-Dominios/Tecnologia/Java/Microservices e sistemas distribuídos/17 - Segurança entre serviços|segurança entre serviços]]).

7. **O fio invisível: o trace.** Desde o passo 1, um **traceId** foi gerado (ou propagado de upstream). Ele viaja em headers (`traceparent`) por **todos** os hops — gateway → order → payment — costurando os logs ([[03-Dominios/Tecnologia/Java/Microservices e sistemas distribuídos/18 - Tracing distribuído I — correlação no código|correlação no código]]) e sendo exportado para um backend ([[03-Dominios/Tecnologia/Java/Microservices e sistemas distribuídos/19 - Tracing distribuído II — exportando o trace|exportando o trace]]).

8. **A resposta volta.** Pagamento OK → pedido criado → `201 Created` sobe pela mesma cadeia, sai pelo gateway, chega ao cliente. Fim da jogada.

### Síncrono vs. evento assíncrono

O passo 5 assumiu uma chamada **síncrona**: o `order-service` espera o `payment-service` responder. Mas há uma bifurcação fundamental aqui ([[03-Dominios/Tecnologia/Java/Microservices e sistemas distribuídos/05 - Comunicação inter-serviços — síncrono vs assíncrono|síncrono vs assíncrono]]).

**Caminho síncrono (request/response):**
- `order-service` chama `payment-service` e **bloqueia** esperando.
- Simples de raciocinar, resposta imediata, mas **acopla disponibilidade**: se o payment cai, o order sente na hora (daí toda a resiliência do passo 5).

**Caminho assíncrono (evento):**
- `order-service` publica um evento `OrderPlaced` num broker e **responde já** (`202 Accepted`).
- O `payment-service` consome o evento quando puder. Desacopla disponibilidade, absorve picos — mas troca **resposta imediata** por **[[03-Dominios/Tecnologia/Java/Microservices e sistemas distribuídos/20 - Consistência em sistemas distribuídos|consistência eventual]]**.
- Toda a mecânica de broker, ordering, idempotência e o padrão **saga** vivem no [[03-Dominios/Tecnologia/Java/Mensageria/index|Galho 14 — Mensageria e eventos]]. Aqui a nota só **aponta a bifurcação**; a profundidade async está lá.

> [!tip] A pergunta que decide o caminho
> "O cliente precisa saber **agora** se o pagamento passou?" Se sim, síncrono (com resiliência). Se "o pagamento pode confirmar em segundos e eu aviso depois", async + saga. Pagamento de e-commerce frequentemente é **híbrido**: autoriza síncrono, captura assíncrono.

### Consistência eventual no fim da linha

No caminho assíncrono, no instante em que o `order-service` respondeu `202`, o pedido existe mas **ainda não foi pago**. O sistema está temporariamente **inconsistente** — e isso é por design.

[[03-Dominios/Tecnologia/Java/Microservices e sistemas distribuídos/20 - Consistência em sistemas distribuídos|Consistência em sistemas distribuídos]] explica por que num sistema particionado você **não pode** ter consistência forte e disponibilidade ao mesmo tempo (a intuição do CAP). A saída prática é a **saga**: uma sequência de passos locais, cada um com sua **compensação** se algo falhar adiante (pagamento recusado → cancela o pedido). E os modos de falha que a saga precisa tolerar — mensagem duplicada, fora de ordem, perdida — são exatamente [[03-Dominios/Tecnologia/Java/Microservices e sistemas distribuídos/21 - Os padrões de falha distribuída|os padrões de falha distribuída]].

A síntese é esta: **consistência eventual não é um bug do async, é o preço do desacoplamento.** Você paga esse preço conscientemente, com saga + idempotência, ou não usa async.

## Na prática

### O diagrama de ponta a ponta

```text
                 POST /api/orders
                        │
                        ▼
              ┌───────────────────┐
              │   API GATEWAY     │  ← predicates (Path) + filters (StripPrefix, auth)
              │  (WebFlux | MVC)  │     traceId GERADO aqui (notas 10, 11, 18)
              └─────────┬─────────┘
                        │  lb://order-service
                        ▼
              ┌───────────────────┐
              │ SERVICE DISCOVERY │  ← "quais instâncias de order-service vivem?" (06, 07)
              └─────────┬─────────┘
                        │  [inst-A, inst-B, inst-C]
                        ▼
              ┌───────────────────┐
              │  LOAD BALANCER    │  ← escolhe UMA instância (round-robin) (08)
              └─────────┬─────────┘
                        ▼
              ┌─────────────────────────────────────────┐
              │            order-service                 │
              │                                          │
              │   precisa cobrar → cliente Feign (09)    │
              │   resolve payment via discovery+LB (06-08)│
              │                                          │
              │   ┌──────────────────────────────────┐   │
              │   │  CHAMADA RESILIENTE (13,14,15,16) │   │
              │   │  @CircuitBreaker @Retry           │   │
              │   │  @TimeLimiter [@Bulkhead]         │   │
              │   └────────────────┬─────────────────┘   │
              └────────────────────┼─────────────────────┘
                                   │
              ┌────────────────────┴────────────────────┐
              │                                          │
       SÍNCRONO (05,09)                          ASSÍNCRONO (05 → G14)
              │                                          │
              ▼                                          ▼
     ┌─────────────────┐                       publica OrderPlaced
     │ payment-service │                       responde 202 Accepted
     │  (HTTP direto)  │                       payment consome depois
     └────────┬────────┘                       saga + compensação (20,21)
              │                                 consistência EVENTUAL (20)
              ▼
        201 Created
              │
   (traceId propagado em TODOS os hops → exportado, notas 18, 19)
              ▼
        resposta → cliente
```

### Rota no gateway (YAML)

A borda. Confirmado contra a [referência do Spring Cloud Gateway](https://docs.spring.io/spring-cloud-gateway/reference/): `spring.cloud.gateway.routes` com `predicates` e `filters`. O `lb://` aciona o LoadBalancer + discovery.

```yaml
spring:
  cloud:
    gateway:
      routes:
        - id: order-route
          uri: lb://order-service        # lb:// → discovery + load balancing
          predicates:
            - Path=/api/orders/**         # predicate: só essa rota casa
          filters:
            - StripPrefix=1               # filter: /api/orders/x → /orders/x
            - AddRequestHeader=X-Edge, gateway
```

> [!note] WebFlux vs. MVC — só o starter muda
> Reativo: starter `spring-cloud-starter-gateway-server-webflux`. Servlet/bloqueante: `spring-cloud-starter-gateway-server-webmvc`. O YAML acima é praticamente o mesmo nas duas variantes; a diferença está no modelo de I/O por baixo ([[03-Dominios/Tecnologia/Java/Microservices e sistemas distribuídos/11 - Gateway reativo vs MVC — as duas variantes|nota 11]]).

### Cliente declarativo do order para o payment (Java)

Dentro do `order-service`. OpenFeign declarativo: o `name` é o **service-name**, não um host — o discovery + LB resolvem ([[03-Dominios/Tecnologia/Java/Microservices e sistemas distribuídos/09 - Comunicação síncrona — OpenFeign e HTTP Interface|nota 09]]).

```java
@FeignClient(name = "payment-service")   // name = service-name → discovery + LB
public interface PaymentClient {

    @PostMapping("/payments")
    PaymentResult charge(@RequestBody ChargeRequest request);
}
```

### A chamada resiliente (Java + YAML)

O coração Magus. Resilience4j **2.4.0** com `resilience4j-spring-boot3`. As anotações empilham; o `fallbackMethod` é o plano B quando o circuito abre ou o tempo estoura. Sintaxe confirmada contra a [doc do Resilience4j](https://resilience4j.readme.io/docs).

```java
@Service
public class PaymentGateway {

    private final PaymentClient client;

    public PaymentGateway(PaymentClient client) {
        this.client = client;
    }

    // ordem de composição importa (nota 16): TimeLimiter recorta a chamada,
    // Retry repete, CircuitBreaker conta as falhas da janela.
    @CircuitBreaker(name = "payment", fallbackMethod = "chargeFallback")
    @Retry(name = "payment")
    @TimeLimiter(name = "payment")
    public CompletableFuture<PaymentResult> charge(ChargeRequest req) {
        return CompletableFuture.supplyAsync(() -> client.charge(req));
    }

    // fallback: assinatura = método original + o Throwable no fim
    private CompletableFuture<PaymentResult> chargeFallback(ChargeRequest req, Throwable t) {
        return CompletableFuture.completedFuture(PaymentResult.pending(req.orderId()));
    }
}
```

```yaml
resilience4j:
  timelimiter:
    instances:
      payment:
        timeout-duration: 2s          # corta a chamada antes do retry/CB
  retry:
    instances:
      payment:
        max-attempts: 3
        wait-duration: 200ms
  circuitbreaker:
    instances:
      payment:
        sliding-window-size: 20
        failure-rate-threshold: 50    # 50% de falha na janela → abre
        wait-duration-in-open-state: 10s
```

> [!warning] Coerência entre os timeouts
> Regra de ouro: `timeout-duration` (TimeLimiter) ≤ orçamento total da chamada; e `max-attempts × (wait-duration + timeout)` precisa caber no SLA do gateway upstream. Se o gateway desiste em 5s mas seu retry leva 6s, você gastou recursos numa resposta que **ninguém vai esperar**. (Lição da [[03-Dominios/Tecnologia/Java/Microservices e sistemas distribuídos/16 - Resiliência IV — compondo os padrões|nota 16]].)

## Tabela de decisão

| Decisão | Escolha A | Escolha B | Critério de desempate |
|---|---|---|---|
| **Síncrono vs. assíncrono** | Síncrono (Feign/HTTP) | Async (evento + broker) | "O cliente precisa da resposta **agora**?" Sim → síncrono. "Pode confirmar depois / preciso desacoplar disponibilidade / absorver pico?" → async + saga (G14) |
| **Quando colocar gateway** | Sim, gateway na borda | Não, exposição direta | Há **cross-cutting** na borda (auth, rate limit, roteamento, TLS termination)? Sim → gateway. Um único serviço trivial sem borda compartilhada → talvez dispensável |
| **Quando service mesh** | Mesh (sidecar) | Resiliência in-app | Poliglota (vários runtimes), quer resiliência/mTLS **uniforme sem mexer no código**, já tem k8s → mesh (nota 22). Stack Java homogênea, time pequeno, controle fino no código → in-app |
| **Eureka vs. k8s-native** | Eureka (Spring) | k8s Services/DNS | Roda **fora** do k8s ou quer registry Spring-idiomático → Eureka (06). Já está em k8s → use Services nativos, evite duplicar o discovery (07) |
| **Resiliência: in-app vs. mesh** | Resilience4j no código | Sidecar (Istio/Linkerd) | Precisa de **fallback com lógica de negócio** (ex.: `PaymentResult.pending`)? → in-app, mesh não conhece seu domínio. Só timeout/retry/CB **genéricos** uniformes? → mesh resolve sem código (22) |

## Armadilhas

### (1) "Microservices é mais escalável por definição"

O raciocínio falho: "quebrei em serviços, logo escala melhor". Não. Você **trocou** chamadas de função (nanossegundos, confiáveis) por chamadas de rede (milissegundos, falíveis). A escalabilidade vem de poder **escalar partes independentemente** — mas só se as partes forem de fato independentes. Se `order` e `payment` sempre escalam juntos e falam o tempo todo, você criou um **monólito distribuído**: a latência do monólito **mais** a falibilidade da rede. [[03-Dominios/Tecnologia/Java/Microservices e sistemas distribuídos/23 - Quando NÃO fazer microservices|Quando NÃO fazer microservices]] é o antídoto. Escalabilidade é uma **propriedade de design**, não um efeito colateral de separar processos.

### (2) "Circuit breaker resolve tudo"

O raciocínio falho: "botei `@CircuitBreaker`, agora estou resiliente". Circuit breaker resolve **um** problema: parar de bater num serviço que já está morto, para não desperdiçar recursos e não cascatear a falha ([[03-Dominios/Tecnologia/Java/Microservices e sistemas distribuídos/13 - Resiliência I — a falha distribuída e o Circuit Breaker|nota 13]]). Ele **não** resolve: lentidão pontual (isso é Time Limiter + Retry, [[03-Dominios/Tecnologia/Java/Microservices e sistemas distribuídos/14 - Resiliência II — Retry e Time Limiter|nota 14]]); exaustão de pool por um endpoint lento contaminar os outros (isso é Bulkhead, [[03-Dominios/Tecnologia/Java/Microservices e sistemas distribuídos/15 - Resiliência III — Bulkhead e Rate Limiter|nota 15]]); nem decide **o que fazer quando o circuito abre** (isso é o fallback, lógica sua). Resiliência é uma **composição** de padrões, cada um cobrindo um modo de falha. Um padrão sozinho deixa buracos.

### (3) "Mesh dispensa pensar resiliência"

O raciocínio falho: "instalei Istio, o sidecar cuida da resiliência, não preciso mais pensar nisso". O mesh ([[03-Dominios/Tecnologia/Java/Microservices e sistemas distribuídos/22 - Service mesh — quando a resiliência sai do código|nota 22]]) move a resiliência **genérica** para fora do código — timeout, retry, circuit breaking **agnósticos de domínio**. Mas o mesh **não conhece o seu negócio**: ele não sabe que, quando o pagamento falha, o fallback correto é marcar o pedido como `pending` e disparar uma compensação. Resiliência com **semântica de domínio** continua sendo sua responsabilidade, no código. O mesh tira o boilerplate, não o pensamento. Decidir **o que significa** falhar continua sendo design de aplicação.

## Em entrevista

### Frase pronta (inglês)

> "Let me walk you through what happens when a request hits our platform. It enters through the **API gateway**, which matches a route predicate and applies edge filters like auth and path rewriting. The gateway resolves the target via **service discovery** and the **client-side load balancer** picks a healthy instance. Inside the order service, the call to the payment service is **wrapped in resilience patterns** — a time limiter and circuit breaker with a retry — so a slow or dead dependency degrades gracefully via a fallback instead of cascading. If the operation can be deferred, we publish an **event** and accept **eventual consistency** through a saga rather than blocking. Throughout, a single **trace ID** propagates across every hop, so we can reconstruct the whole journey in our observability backend. The key insight is that no pattern works alone — they **compose** along the request path, and you have to reason about where each one lives."

### Vocabulário

| Termo (inglês) | Tradução / sentido |
|---|---|
| request path | caminho que a requisição percorre pelos serviços |
| graceful degradation | degradar com elegância (fallback) em vez de quebrar |
| cascading failure | falha que se propaga em cascata para o chamador |
| eventual consistency | consistência atingida com o tempo, não imediata |
| trace propagation | propagação do traceId por todos os hops |
| compose (patterns) | empilhar padrões de resiliência de forma coerente |
| service-to-service | comunicação interna entre serviços (não da borda) |

## Cheatsheet nota→problema

Mapa de "qual dor sintoma → qual nota":

- **"Vale a pena quebrar meu monólito? Quando NÃO?"** → [[03-Dominios/Tecnologia/Java/Microservices e sistemas distribuídos/01 - O que são microservices e a tese honesta|01]] e [[03-Dominios/Tecnologia/Java/Microservices e sistemas distribuídos/23 - Quando NÃO fazer microservices|23]]
- **"Um repo só ou um por serviço?"** → [[03-Dominios/Tecnologia/Java/Microservices e sistemas distribuídos/02 - Monorepo vs multi-repo|02]]
- **"Como deixar o serviço portável / cloud-native?"** → [[03-Dominios/Tecnologia/Java/Microservices e sistemas distribuídos/03 - Os 12 fatores e o serviço cloud-native|03]]
- **"O que existe no Spring Cloud hoje e o que foi descontinuado?"** → [[03-Dominios/Tecnologia/Java/Microservices e sistemas distribuídos/04 - Panorama do Spring Cloud — e o que morreu|04]]
- **"Chamo direto ou mando evento?"** → [[03-Dominios/Tecnologia/Java/Microservices e sistemas distribuídos/05 - Comunicação inter-serviços — síncrono vs assíncrono|05]] (async profundo → [[03-Dominios/Tecnologia/Java/Mensageria/index|G14]])
- **"Como um serviço acha o outro sem IP cravado?"** → [[03-Dominios/Tecnologia/Java/Microservices e sistemas distribuídos/06 - Service discovery — o conceito e o Eureka|06]] e [[03-Dominios/Tecnologia/Java/Microservices e sistemas distribuídos/07 - Discovery — Consul e Kubernetes-native|07]]
- **"Tenho 3 instâncias, qual chamo?"** → [[03-Dominios/Tecnologia/Java/Microservices e sistemas distribuídos/08 - Client-side load balancing — Spring Cloud LoadBalancer|08]]
- **"Como escrevo o cliente HTTP sem boilerplate?"** → [[03-Dominios/Tecnologia/Java/Microservices e sistemas distribuídos/09 - Comunicação síncrona — OpenFeign e HTTP Interface|09]]
- **"Preciso de uma porta de entrada única com auth/roteamento?"** → [[03-Dominios/Tecnologia/Java/Microservices e sistemas distribuídos/10 - API Gateway — papel, roteamento, predicates e filters|10]] e [[03-Dominios/Tecnologia/Java/Microservices e sistemas distribuídos/11 - Gateway reativo vs MVC — as duas variantes|11]]
- **"Não quero config hard-coded espalhado"** → [[03-Dominios/Tecnologia/Java/Microservices e sistemas distribuídos/12 - Config centralizado — Spring Cloud Config|12]]
- **"Serviço lento ou morto derrubando o chamador?"** → [[03-Dominios/Tecnologia/Java/Microservices e sistemas distribuídos/13 - Resiliência I — a falha distribuída e o Circuit Breaker|13]] (CB) + [[03-Dominios/Tecnologia/Java/Microservices e sistemas distribuídos/15 - Resiliência III — Bulkhead e Rate Limiter|15]] (Bulkhead)
- **"Falha transitória / chamada que demora demais?"** → [[03-Dominios/Tecnologia/Java/Microservices e sistemas distribuídos/14 - Resiliência II — Retry e Time Limiter|14]]
- **"Como empilho os padrões sem eles brigarem?"** → [[03-Dominios/Tecnologia/Java/Microservices e sistemas distribuídos/16 - Resiliência IV — compondo os padrões|16]]
- **"Como autentico serviço-para-serviço?"** → [[03-Dominios/Tecnologia/Java/Microservices e sistemas distribuídos/17 - Segurança entre serviços|17]]
- **"Perdi o rastro da requisição entre serviços"** → [[03-Dominios/Tecnologia/Java/Microservices e sistemas distribuídos/18 - Tracing distribuído I — correlação no código|18]] e [[03-Dominios/Tecnologia/Java/Microservices e sistemas distribuídos/19 - Tracing distribuído II — exportando o trace|19]]
- **"Dados temporariamente divergentes entre serviços?"** → [[03-Dominios/Tecnologia/Java/Microservices e sistemas distribuídos/20 - Consistência em sistemas distribuídos|20]] + [[03-Dominios/Tecnologia/Java/Microservices e sistemas distribuídos/21 - Os padrões de falha distribuída|21]]
- **"Quero resiliência/mTLS uniforme sem mexer no código?"** → [[03-Dominios/Tecnologia/Java/Microservices e sistemas distribuídos/22 - Service mesh — quando a resiliência sai do código|22]]

## Veja também

- [[03-Dominios/Tecnologia/Java/Microservices e sistemas distribuídos/index|Microservices e sistemas distribuídos (MOC do galho)]]
- [[03-Dominios/Tecnologia/Java/index|Trilha Java]]
- [[03-Dominios/Tecnologia/Java/Microservices e sistemas distribuídos/05 - Comunicação inter-serviços — síncrono vs assíncrono|05 - Comunicação inter-serviços — síncrono vs assíncrono]]
- [[03-Dominios/Tecnologia/Java/Microservices e sistemas distribuídos/10 - API Gateway — papel, roteamento, predicates e filters|10 - API Gateway — papel, roteamento, predicates e filters]]
- [[03-Dominios/Tecnologia/Java/Microservices e sistemas distribuídos/16 - Resiliência IV — compondo os padrões|16 - Resiliência IV — compondo os padrões]]
- [[03-Dominios/Tecnologia/Java/Microservices e sistemas distribuídos/18 - Tracing distribuído I — correlação no código|18 - Tracing distribuído I — correlação no código]]
- [[03-Dominios/Tecnologia/Java/Microservices e sistemas distribuídos/20 - Consistência em sistemas distribuídos|20 - Consistência em sistemas distribuídos]]
- [[03-Dominios/Tecnologia/Java/Microservices e sistemas distribuídos/22 - Service mesh — quando a resiliência sai do código|22 - Service mesh — quando a resiliência sai do código]]

## Referências

- Spring Cloud Gateway — Reference (routes, predicates, filters, WebFlux vs. WebMVC): https://docs.spring.io/spring-cloud-gateway/reference/
- Resilience4j — Documentation (anotações `@CircuitBreaker`/`@Retry`/`@TimeLimiter`, `fallbackMethod`, config `resilience4j.*.instances`; linha 2.x): https://resilience4j.readme.io/docs
