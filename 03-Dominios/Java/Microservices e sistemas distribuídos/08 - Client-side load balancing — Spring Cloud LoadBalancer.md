---
title: "Client-side load balancing — Spring Cloud LoadBalancer"
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
  - load-balancing
aliases:
  - "Spring Cloud LoadBalancer"
  - "Client-side load balancing"
---

# Client-side load balancing — Spring Cloud LoadBalancer

> [!abstract] TL;DR
> Quando um serviço tem **várias instâncias**, alguém precisa escolher pra qual delas mandar cada requisição. No modelo **client-side**, quem escolhe é o próprio chamador — ele pega a lista de instâncias do [[03-Dominios/Java/Microservices e sistemas distribuídos/06 - Service discovery — o conceito e o Eureka|service discovery]] e faz o rodízio em código. O **Ribbon** (Netflix) era a peça que fazia isso no Spring Cloud, mas **morreu**: saiu do trem **2020.0.0 (Ilford)**. O substituto oficial é o **Spring Cloud LoadBalancer** — funciona em cliente *blocking* (`RestTemplate`, `RestClient`) e *reativo* (`WebClient`), com estratégias *round-robin* (padrão) e *random*. Você marca o cliente com `@LoadBalanced` e usa URIs no esquema `lb://order-service`; o LB resolve o `service-id` numa instância real. Se você roda sobre um **service mesh** ou Kubernetes Service, o balanceamento já acontece na infra — aí client-side LB vira redundância (ver [[03-Dominios/Java/Microservices e sistemas distribuídos/22 - Service mesh — quando a resiliência sai do código|service mesh]]).

## O que é

**Load balancing** é a distribuição de requisições entre múltiplas réplicas de um mesmo serviço. Num sistema de microsserviços você quase nunca tem *uma* instância de `order-service` — tem três, dez, quarenta, escalando conforme a carga. Cada chamada precisa cair em *alguma* delas, e idealmente de forma equilibrada.

Existem dois lugares onde essa decisão pode morar:

- **Server-side load balancing**: um intermediário no caminho (um load balancer dedicado, um Kubernetes Service, um proxy de service mesh) recebe a requisição e a encaminha pra uma instância. O cliente fala com *um* endereço estável e não sabe quantas instâncias existem.
- **Client-side load balancing**: o **próprio cliente** consulta a lista de instâncias disponíveis (via service discovery) e escolhe, em código, pra qual instância mandar. Não há um intermediário no caminho dos dados.

O **Spring Cloud LoadBalancer** (SC LoadBalancer, ou simplesmente *LB*) é a implementação canônica de **client-side load balancing** no ecossistema Spring. Ele é uma abstração: pega um `service-id` lógico (`order-service`) e resolve numa instância física (`10.0.3.7:8081`) no momento da chamada.

> [!info] O nome enganador
> "Load balancer" no senso comum evoca uma caixa server-side (um NGINX, um ELB da AWS). O Spring Cloud LoadBalancer é o oposto: ele vive *dentro* do seu serviço chamador, como uma biblioteca. Não há servidor extra pra subir.

## Por que importa

O Ribbon foi o **load balancer client-side** do Spring Cloud por anos, herdado da stack Netflix OSS. Em 2018 o time da Netflix colocou Ribbon (junto de Hystrix, Zuul e Archaius) em **maintenance mode** — nenhuma feature nova, só correções críticas. No trem de release **2020.0.0 (codinome Ilford)**, o Ribbon foi **removido de vez** do Spring Cloud. Quem subia uma aplicação Spring Cloud moderna e procurava `@RibbonClient` ou `spring-cloud-starter-netflix-ribbon` simplesmente não encontrava mais nada.

Isso importa por três razões práticas:

1. **Tutoriais antigos quebram.** Muito material pré-2021 ensina Ribbon. Se você seguir, vai bater num beco sem saída — a dependência não existe no classpath atual.
2. **A migração é conceitual, não só de nome.** SC LoadBalancer não é "Ribbon renomeado". Tem outra API de configuração, outro modelo de extensão (`ServiceInstanceListSupplier`) e suporte nativo a clientes reativos, coisa que o Ribbon (blocking-only) nunca teve.
3. **Em entrevista, é pegadinha de versão.** Saber que Ribbon morreu e *quando* (Ilford) separa quem leu a documentação atual de quem decorou um curso de 2019.

## Como funciona

### Ribbon morreu — e por quê

O Ribbon nasceu na Netflix como parte de uma stack que resolvia problemas reais de 2012: discovery (Eureka), circuit breaker (Hystrix), gateway (Zuul) e load balancing client-side (Ribbon). Com o tempo, a Netflix parou de investir nessas bibliotecas internamente — tinha migrado pra soluções próprias e pra service mesh. Sem um mantenedor ativo upstream, o Spring Cloud não podia mais evoluí-las.

A consequência:

- **2018** — Ribbon, Hystrix, Zuul e Archaius entram em *maintenance mode* (só fixes, sem features).
- **2020.0.0 (Ilford)** — Ribbon é **removido** do Spring Cloud. Hystrix sai em favor do Resilience4j (ver [[03-Dominios/Java/Microservices e sistemas distribuídos/index|MOC do galho]], nota de resiliência); Zuul sai em favor do Spring Cloud Gateway.

O ponto de fundo: o Ribbon era *blocking* por design e tinha uma API de configuração datada (baseada em Archaius e em `IRule`/`IPing`). Reescrever em cima dele era pior do que partir pra uma abstração nova, reativa-first.

> [!warning] Não confunda os papéis
> Ribbon (load balancing) ≠ Hystrix (circuit breaker) ≠ Zuul (gateway). Os quatro módulos Netflix saíram *juntos* de manutenção, mas cada um foi substituído por uma peça diferente. Esta nota é só sobre o sucessor do **Ribbon**.

### Spring Cloud LoadBalancer (client-side)

O SC LoadBalancer é a peça que substitui o Ribbon. Características centrais:

- **Blocking e reativo.** Para clientes *blocking* (`RestTemplate`, `RestClient`), o trabalho é feito pelo `BlockingLoadBalancerClient`. Para clientes reativos (`WebClient`), pelo `ReactorLoadBalancerExchangeFilterFunction`. O Ribbon nunca teve a parte reativa.
- **Estratégias de seleção.** Por padrão, **round-robin** (`RoundRobinLoadBalancer`) — rodízio circular entre as instâncias. Há também **random** (`RandomLoadBalancer`), e configurações prontas como `weighted`, `zone-preference` e `health-check`.
- **Integração com discovery.** O LB não inventa a lista de instâncias — ele a obtém via `ServiceInstanceListSupplier`, que por baixo consulta o `DiscoveryClient` (Eureka, Consul, k8s, etc.). É a ponte direta com a nota de [[03-Dominios/Java/Microservices e sistemas distribuídos/06 - Service discovery — o conceito e o Eureka|service discovery]].
- **Esquema de URI `lb://`.** Você não escreve `http://10.0.3.7:8081`; escreve `http://order-service` (com `@LoadBalanced`) ou explicitamente `lb://order-service`. O `service-id` é resolvido na hora da chamada.
- **Cache.** O `spring-cloud-starter-loadbalancer` traz cache da lista de instâncias (`spring.cloud.loadbalancer.cache.ttl`, padrão na casa de dezenas de segundos), pra não martelar o discovery a cada requisição.

O fluxo de uma chamada, em câmera lenta:

1. Seu código chama `restTemplate.getForObject("http://order-service/orders/42", ...)`.
2. O interceptor de `@LoadBalanced` vê o host `order-service` e percebe que é um `service-id`, não um hostname real.
3. O LB pede ao `ServiceInstanceListSupplier` a lista de instâncias vivas de `order-service`.
4. A estratégia (round-robin) escolhe **uma** instância — digamos `10.0.3.7:8081`.
5. A URI é reescrita pra `http://10.0.3.7:8081/orders/42` e a chamada segue.

### Client-side vs server-side LB

A pergunta que separa os dois mundos: **quem decide a instância de destino?**

| Aspecto | Client-side (SC LoadBalancer) | Server-side (k8s Service, mesh, ELB) |
| --- | --- | --- |
| Quem escolhe a instância | O cliente chamador, em código | Um intermediário na infra |
| Precisa de service discovery no app? | Sim — o cliente lê a lista | Não — o intermediário cuida disso |
| Hop de rede extra | Não (vai direto à instância) | Sim (passa pelo proxy/LB) |
| Onde mora a lógica | Na sua aplicação (biblioteca) | Fora do código (plataforma) |
| Linguagem-dependente | Sim (é código Java/Spring) | Não (independe da stack) |

Nenhum dos dois é "melhor" em abstrato — depende de **onde** você quer a responsabilidade. Se você roda em VMs com Eureka e quer evitar um hop extra, client-side faz sentido. Se você roda em **Kubernetes** (onde o `Service` já balanceia) ou sob um **service mesh** (onde o sidecar balanceia), o LB client-side vira redundância — e aí a fronteira é a nota de [[03-Dominios/Java/Microservices e sistemas distribuídos/22 - Service mesh — quando a resiliência sai do código|service mesh]], onde load balancing, retry e circuit breaking saem do código e descem pra infraestrutura.

> [!tip] A analogia do táxi
> Server-side é como uma fila de táxi no aeroporto: você entra na fila, e um *despachante* (o LB da infra) te aponta o próximo carro. Client-side é como você ter a lista de todos os motoristas no celular e escolher um você mesmo a cada corrida. No primeiro caso, o despachante é um ponto a mais no caminho; no segundo, você fala direto com o motorista — mas precisa manter a lista atualizada.

## Na prática

Cliente *blocking* com `RestTemplate`. O bean precisa de `@LoadBalanced`:

```java
@Configuration
public class HttpClientConfig {

    @Bean
    @LoadBalanced
    public RestTemplate restTemplate() {
        return new RestTemplate();
    }
}
```

Uso — repare que o host é o `service-id`, não um IP:

```java
@Service
public class OrderClient {

    private final RestTemplate restTemplate;

    public OrderClient(RestTemplate restTemplate) {
        this.restTemplate = restTemplate;
    }

    public Order fetchOrder(long id) {
        // "order-service" é resolvido em uma instância real pelo LoadBalancer
        return restTemplate.getForObject(
                "http://order-service/orders/{id}", Order.class, id);
    }
}
```

Versão reativa com `WebClient.Builder` (também marcado com `@LoadBalanced`):

```java
@Configuration
public class WebClientConfig {

    @Bean
    @LoadBalanced
    public WebClient.Builder loadBalancedWebClientBuilder() {
        return WebClient.builder();
    }
}
```

```java
@Service
public class InventoryClient {

    private final WebClient webClient;

    public InventoryClient(WebClient.Builder builder) {
        this.webClient = builder.build();
    }

    public Mono<Stock> stockFor(String sku) {
        return webClient.get()
                .uri("http://inventory-service/stock/{sku}", sku)
                .retrieve()
                .bodyToMono(Stock.class);
    }
}
```

Dependência e configuração (`application.yml`):

```xml
<dependency>
    <groupId>org.springframework.cloud</groupId>
    <artifactId>spring-cloud-starter-loadbalancer</artifactId>
</dependency>
```

```yaml
spring:
  cloud:
    loadbalancer:
      # cache da lista de instâncias (evita martelar o discovery)
      cache:
        enabled: true
        ttl: 35s
        capacity: 256
      # health-check filtra instâncias fora do ar antes do rodízio
      health-check:
        path:
          default: /actuator/health
```

Quando você quer trocar a estratégia (de round-robin pra random, por exemplo) ou customizar o `ServiceInstanceListSupplier`, declara uma configuração e a associa ao serviço com `@LoadBalancerClient(value = "order-service", configuration = CustomLbConfig.class)`.

## Armadilhas

### (1) Procurar Ribbon — ele não existe mais

A armadilha número um é seguir um tutorial antigo e tentar `@RibbonClient`, `IRule`, `IPing` ou a dependência `spring-cloud-starter-netflix-ribbon`. Nada disso resolve num Spring Cloud atual — **Ribbon foi removido no trem 2020.0.0 (Ilford)**. Se você herda um projeto legado que ainda referencia Ribbon, a migração é pra `spring-cloud-starter-loadbalancer`, e a API de extensão muda (não é só renomear classes). Sintoma típico: `@LoadBalanced` parece "não fazer nada" porque você esqueceu de remover uma config de Ribbon residual que conflita.

### (2) Client-side LB sobre um mesh que já balanceia = duplo balanceamento

Se sua aplicação roda sob um **service mesh** (Istio, Linkerd) ou usa um **Kubernetes Service** como destino, a infraestrutura *já* faz o load balancing. Empilhar o SC LoadBalancer por cima significa **balancear duas vezes**: o cliente escolhe uma instância, e o sidecar/Service escolhe de novo. O resultado é distribuição imprevisível, métricas confusas e, às vezes, *sticky* indesejado. Em ambientes com mesh, o padrão é **não** usar client-side LB — você fala com o nome de serviço estável do mesh e deixa a infra balancear (ver [[03-Dominios/Java/Microservices e sistemas distribuídos/22 - Service mesh — quando a resiliência sai do código|service mesh]]).

### (3) Esquecer o `@LoadBalanced` → `lb://` vira host literal

O `@LoadBalanced` é o que *liga* o interceptor que reescreve URIs. Sem ele, o `RestTemplate`/`WebClient` é um cliente HTTP comum: ele trata `order-service` como um **hostname literal** e tenta resolvê-lo via DNS. Se não houver DNS pra `order-service`, você toma `UnknownHostException`; se houver `lb://order-service`, o cliente tenta abrir um socket pro "protocolo" `lb`, e falha. O sintoma é desconcertante porque o código *parece* certo — só falta a anotação no bean. Regra mental: **`@LoadBalanced` e `lb://`/`service-id` andam sempre juntos**; um sem o outro quebra.

> [!danger] O bean errado anotado
> `@LoadBalanced` vai no `RestTemplate` / `RestClient.Builder` / `WebClient.Builder` que você de fato injeta no client. Anotar um bean e injetar outro (sem a anotação) reproduz o sintoma do item (3) mesmo com a anotação presente "em algum lugar" do contexto.

## Em entrevista

### Frase pronta (inglês)

> Ribbon, the old Netflix client-side load balancer, was removed in the Spring Cloud 2020.0.0 release train, so the modern replacement is Spring Cloud LoadBalancer. It does client-side load balancing for both blocking clients like RestTemplate and RestClient and reactive ones like WebClient: you annotate the client bean with `@LoadBalanced` and call services by their logical id using the `lb://` scheme, and the load balancer resolves that service id to a concrete instance pulled from the discovery client, typically with a round-robin strategy. I always check the runtime first, though — if the service runs on Kubernetes or under a service mesh, the platform already load-balances, so adding client-side load balancing on top would balance twice, and I'd rely on the mesh instead.

### Vocabulário

| Português | Inglês |
| --- | --- |
| balanceamento no cliente | client-side load balancing |
| rodízio | round-robin |
| instância de serviço | service instance |
| no lado servidor | server-side |
| malha de serviço | service mesh |
| identificador de serviço | service id |
| salto de rede (extra) | (extra) network hop |
| descoberta de serviços | service discovery |

## Veja também

- [[03-Dominios/Java/Microservices e sistemas distribuídos/06 - Service discovery — o conceito e o Eureka|Service discovery]]
- [[03-Dominios/Java/Microservices e sistemas distribuídos/09 - Comunicação síncrona — OpenFeign e HTTP Interface|Comunicação síncrona]]
- [[03-Dominios/Java/Microservices e sistemas distribuídos/22 - Service mesh — quando a resiliência sai do código|Service mesh]]
- [[03-Dominios/Java/Microservices e sistemas distribuídos/index|Microservices e sistemas distribuídos (MOC do galho)]]
- [[03-Dominios/Java/index|Trilha Java]]

## Referências

- Spring Cloud Commons — Spring Cloud LoadBalancer: https://docs.spring.io/spring-cloud-commons/reference/spring-cloud-commons/loadbalancer.html
- Spring Cloud Netflix — Modules in Maintenance Mode: https://cloud.spring.io/spring-cloud-netflix/multi/multi__modules_in_maintenance_mode.html
