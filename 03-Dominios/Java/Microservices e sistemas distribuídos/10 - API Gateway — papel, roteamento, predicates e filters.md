---
title: "API Gateway — papel, roteamento, predicates e filters"
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
  - gateway
aliases:
  - "API Gateway"
  - "Spring Cloud Gateway"
---

# API Gateway — papel, roteamento, predicates e filters

> [!abstract] TL;DR
> Um **API Gateway** é a **porta única** de entrada para um conjunto de microsserviços: o cliente fala só com ele, e ele decide para qual serviço encaminhar cada requisição. Além de **rotear**, o gateway concentra **preocupações transversais** (autenticação, rate limit, CORS, reescrita de caminho, retry) num lugar só, em vez de espalhá-las por todos os serviços. No **Spring Cloud Gateway**, cada **route** é `id + uri + predicates + filters`: os **predicates** (Path, Method, Header, Query...) decidem *se* a rota casa; os **filters** transformam requisição/resposta nas fases **pre** e **post**, e dividem-se em **GatewayFilter** (por rota) e **GlobalFilter** (todas as rotas). A integração com discovery vem pelo esquema `lb://serviço`, que resolve o nome lógico para uma instância via load balancer.

## O que é

Um **API Gateway** é um serviço que fica na borda do sistema, entre os clientes externos (browser, app mobile, outro sistema) e a malha interna de microsserviços. Toda chamada de fora entra por ele.

A analogia mais direta é a **portaria de um prédio**. Você não bate na porta de cada apartamento: você fala com o porteiro. O porteiro sabe quem mora onde (roteamento), confere sua identidade (autenticação), barra quem não pode entrar (autorização), controla o fluxo de visitantes (rate limit) e às vezes reescreve o destino ("o escritório 302 mudou pro 410"). O morador — cada microsserviço — não precisa saber lidar com a rua; ele confia que a portaria já filtrou o que chegou.

Sem gateway, cada cliente precisaria conhecer o endereço de cada serviço, e cada serviço precisaria reimplementar autenticação, CORS e limite de requisições. O gateway colapsa tudo isso num ponto único de entrada.

> [!note] Gateway ≠ Load Balancer ≠ Service Mesh
> Um **load balancer** distribui carga entre instâncias iguais (camada 4/7, sem entender suas regras de negócio). Um **API gateway** trabalha em camada 7 e entende rotas, headers e filtros específicos da sua aplicação. Um **service mesh** (ex.: Istio) cuida da comunicação *serviço-a-serviço interna* (leste-oeste), enquanto o gateway cuida do tráfego *cliente-para-sistema* (norte-sul). Eles coexistem.

## Por que importa

O gateway resolve um problema concreto de microsserviços: **onde colocar o que é comum a todos os serviços?**

- **Ponto único de entrada.** O cliente tem um endereço só. A topologia interna (quais serviços existem, em quais portas) fica escondida e pode mudar sem quebrar o cliente.
- **Preocupações transversais centralizadas.** Autenticação, autorização de borda, rate limiting, CORS, logging, tracing e retry vivem no gateway. Sem isso, você duplica essa lógica (e seus bugs) em cada serviço.
- **Roteamento flexível.** Você pode rotear por caminho, método, header ou query, e fazer rollout gradual (peso de rotas), canary releases ou A/B testing sem tocar nos serviços.
- **Desacoplamento de contrato.** O gateway pode **reescrever caminhos** (`/api/v2/orders` → `/orders` no serviço interno), agregar uma fachada estável sobre serviços que evoluem por baixo.

A contrapartida — e isso cai em entrevista — é que o gateway vira um **ponto de acoplamento e de falha**. Se ele cair, tudo cai. E se você encher ele de lógica de negócio, ele vira um monólito disfarçado. As [[#Armadilhas|armadilhas]] no fim tratam exatamente disso.

## Como funciona

### O papel do gateway no fluxo de uma requisição

Pense no caminho de uma chamada `GET /orders/42` vinda do app:

1. O cliente chama o **gateway** (um endereço só, ex.: `api.loja.com`).
2. O gateway avalia suas **rotas** em ordem e encontra a primeira cujos **predicates** casam com a requisição.
3. Aplica os **filters pre** dessa rota (e os globais): valida o token, checa rate limit, reescreve o caminho, adiciona headers.
4. Encaminha (proxy) para o serviço de destino — resolvendo o endereço real via discovery se for `lb://`.
5. Recebe a resposta do serviço e aplica os **filters post**: adiciona headers de resposta, registra métricas, ajusta status.
6. Devolve a resposta ao cliente.

O gateway é, no fundo, um **proxy reverso inteligente**: ele não processa regra de negócio, ele decide *para onde* mandar e *o que fazer antes e depois*.

### Routes + predicates

No **Spring Cloud Gateway**, a unidade de configuração é a **route**. Cada route tem quatro partes:

| Parte | O que é |
| --- | --- |
| `id` | Identificador único da rota |
| `uri` | Destino para onde encaminhar (ex.: `lb://order-service`) |
| `predicates` | Condições que decidem *se* a rota casa com a requisição |
| `filters` | Transformações aplicadas à requisição/resposta |

Os **predicates** (predicados) são as condições de match. As rotas são avaliadas **em ordem**, e a **primeira** cujos predicates *todos* casam é a escolhida. Os tipos principais de predicate factory:

| Predicate | Casa quando... |
| --- | --- |
| **Path** | o caminho bate com um padrão (ex.: `/orders/**`) |
| **Method** | o método HTTP é um dos listados (ex.: `GET`, `POST`) |
| **Header** | um header existe / casa com regex |
| **Query** | existe um parâmetro de query (com valor opcional via regex) |
| **Cookie** | um cookie existe / casa com regex |
| **Host** | o header `Host` bate com um padrão (ex.: `**.loja.com`) |
| **RemoteAddr** | o IP de origem está numa faixa CIDR |
| **After / Before / Between** | a requisição chega dentro de uma janela de tempo |
| **Weight** | seleção ponderada entre rotas de um mesmo grupo (canary) |

> [!tip] Predicates são compostos por AND
> Numa mesma rota, *todos* os predicates precisam casar. `Path=/orders/**` **e** `Method=GET` significa "GET sob `/orders`". Para um OR, você cria rotas separadas.

### Filters pre/post e Global vs Gateway

Enquanto predicates decidem *se* a rota casa, os **filters** decidem *o que fazer* com a requisição e a resposta. Eles têm duas fases:

- **Pre** — antes de encaminhar ao serviço de destino. Ex.: validar token, adicionar header, reescrever caminho, checar rate limit.
- **Post** — depois que a resposta volta do serviço. Ex.: adicionar header de resposta, registrar métricas, mascarar dados.

Internamente, o gateway usa uma **cadeia de filtros** (`GatewayFilterChain`). Cada filtro roda sua lógica *pre*, chama o próximo da cadeia, e a lógica *post* é o que vem **depois** de chamar a cadeia (no runtime reativo, o `chain.filter(exchange).then(...)`; o `.then(...)` é a fase post).

Há dois sabores de filtro:

| Tipo | Escopo | Como se declara |
| --- | --- | --- |
| **GatewayFilter** | **Uma rota específica** | listado nos `filters` da route (ou como *default filters*, aplicados a todas) |
| **GlobalFilter** | **Todas as rotas** | bean que implementa `GlobalFilter`; aplicado condicionalmente a tudo |

Filtros built-in importantes são, na verdade, **GlobalFilters**: o `ReactiveLoadBalancerClientFilter` é quem resolve o esquema `lb://` consultando o load balancer; o `NettyRoutingFilter` é quem faz o proxy HTTP de fato. Você raramente os configura à mão — eles entram no jogo automaticamente.

**Ordem dos filtros** segue a interface `Ordered` (`getOrder()`): **menor valor = maior precedência**. E aqui mora uma sutileza que confunde quase todo mundo — a [[#### (3) Ordem de filters mal entendida|armadilha 3]] detalha. O filtro de maior precedência roda **primeiro na fase pre** e **por último na fase post**. É um modelo de pilha: quem entra primeiro, sai por último.

### Integração com discovery (`lb://`)

Num sistema com microsserviços, o gateway não deve apontar para `http://10.0.3.14:8080` — esse IP muda quando a instância reinicia ou escala. Em vez disso, aponta para um **nome lógico**:

```
uri: lb://order-service
```

O prefixo `lb` (load balanced) sinaliza ao gateway que `order-service` é um nome a ser resolvido pelo **discovery** (Eureka, Consul, ou o discovery do Kubernetes) e balanceado entre as instâncias disponíveis. Por baixo, é o [[03-Dominios/Java/Microservices e sistemas distribuídos/08 - Client-side load balancing — Spring Cloud LoadBalancer|Spring Cloud LoadBalancer]] que escolhe a instância. Se nenhuma instância está disponível, o filtro responde `503` por padrão.

> [!info] O runtime tem duas variantes
> O Spring Cloud Gateway existe em duas implementações de runtime: uma **reativa** (sobre WebFlux/Netty) e uma sobre **Spring MVC** (servlet). Os conceitos desta nota — routes, predicates, filters — valem para ambas; o que muda é o modelo de execução por baixo. **Qual escolher e por quê é assunto da [[03-Dominios/Java/Microservices e sistemas distribuídos/11 - Gateway reativo vs MVC — as duas variantes|nota 11]]** — não vamos aprofundar aqui.

## Na prática

Configuração declarativa em YAML, com duas rotas para domínios neutros. A primeira roteia pedidos com reescrita de caminho; a segunda, pagamentos só para `POST`, com rate limit.

```yaml
spring:
  cloud:
    gateway:
      routes:
        - id: order-route
          uri: lb://order-service          # resolvido via discovery
          predicates:
            - Path=/api/orders/**           # casa o caminho
            - Method=GET,POST               # só GET e POST
          filters:
            - RewritePath=/api/orders/(?<seg>.*), /orders/${seg}
            - AddRequestHeader=X-Source, gateway

        - id: payment-route
          uri: lb://payment-service
          predicates:
            - Path=/api/payments/**
            - Method=POST
          filters:
            - name: RequestRateLimiter       # filtro pre: barra excesso
              args:
                redis-rate-limiter.replenishRate: 10
                redis-rate-limiter.burstCapacity: 20
            - AddResponseHeader=X-Gateway, loja   # filtro post
      default-filters:
        - AddResponseHeader=X-Powered-By, edge    # aplicado a TODAS as rotas
```

O mesmo roteamento expresso **programaticamente** via `RouteLocator` — útil quando a rota depende de lógica que o YAML não expressa:

```java
@Configuration
public class GatewayRoutes {

    @Bean
    public RouteLocator routes(RouteLocatorBuilder builder) {
        return builder.routes()
            // rota de pedidos: predicate de path + reescrita
            .route("order-route", r -> r
                .path("/api/orders/**")
                .and().method(HttpMethod.GET, HttpMethod.POST)
                .filters(f -> f
                    .rewritePath("/api/orders/(?<seg>.*)", "/orders/${seg}")
                    .addRequestHeader("X-Source", "gateway"))
                .uri("lb://order-service"))
            // rota de pagamentos: só POST
            .route("payment-route", r -> r
                .path("/api/payments/**")
                .and().method(HttpMethod.POST)
                .filters(f -> f.addResponseHeader("X-Gateway", "loja"))
                .uri("lb://payment-service"))
            .build();
    }
}
```

Um **GlobalFilter** simples, que roda para todas as rotas e mostra o par pre/post:

```java
@Component
public class LoggingGlobalFilter implements GlobalFilter, Ordered {

    private static final Logger log = LoggerFactory.getLogger(LoggingGlobalFilter.class);

    @Override
    public Mono<Void> filter(ServerWebExchange exchange, GatewayFilterChain chain) {
        // ---- fase PRE: antes de encaminhar ao serviço ----
        log.info("entrada: {} {}", exchange.getRequest().getMethod(),
                                    exchange.getRequest().getPath());

        return chain.filter(exchange).then(Mono.fromRunnable(() ->
            // ---- fase POST: depois da resposta do serviço ----
            log.info("saída: status {}", exchange.getResponse().getStatusCode())
        ));
    }

    @Override
    public int getOrder() {
        return -1; // maior precedência: primeiro no pre, último no post
    }
}
```

## Armadilhas

### (1) Lógica de negócio no gateway = monólito disfarçado

A tentação é grande: "já que toda requisição passa pelo gateway, vou validar o estoque aqui antes de chamar o `order-service`". Não faça isso. O gateway deve cuidar de **roteamento e preocupações transversais** — não de regra de negócio. No momento em que ele conhece o domínio (estoque, preço, status de pedido), você acabou de criar um **monólito disfarçado de gateway**: um único ponto que precisa de deploy a cada mudança de regra, que acopla todos os serviços e que vira o gargalo de toda evolução. Regra de bolso: se a lógica precisaria mudar porque uma *regra de negócio* mudou, ela não pertence ao gateway.

### (2) Gateway como SPOF sem alta disponibilidade

O gateway é, por construção, um **ponto único de entrada** — e portanto um **ponto único de falha** (SPOF) se você rodar uma instância só. Se ele cai, *todo* o sistema fica inacessível, mesmo com todos os serviços de trás saudáveis. A mitigação é tratar o gateway como qualquer serviço crítico: **múltiplas instâncias** atrás de um load balancer de borda (ou do ingress do orquestrador), health checks, e escala horizontal. "Porta única" é uma decisão lógica de arquitetura, não uma desculpa para um único processo físico.

### (3) Ordem de filters mal entendida

A ordem dos filtros segue `Ordered`, e o ponto contra-intuitivo é: **menor valor de `getOrder()` = maior precedência**, mas isso se manifesta de forma *invertida* entre as fases. O filtro de maior precedência roda **primeiro na fase pre** e **por último na fase post** — é um modelo de pilha (LIFO). Quem ignora isso coloca, por exemplo, um filtro de autenticação com ordem baixa esperando que ele rode "primeiro em tudo", e descobre que na fase post ele roda por último. Quando a ordem importa (autenticar *antes* de reescrever o caminho; logar a resposta *depois* de tudo), pense explicitamente em qual filtro precisa estar na borda externa da pilha e qual na interna.

## Em entrevista

### Frase pronta (inglês)

> An API gateway is the single entry point in front of a set of microservices: clients talk only to the gateway, which routes each request to the right service and centralizes cross-cutting concerns like authentication, rate limiting, CORS, and path rewriting. In Spring Cloud Gateway, every route is built from an id, a target uri, a set of predicates that decide whether the route matches, and a chain of filters that transform the request and response in pre and post phases. Predicates match on things like path, method, header, or query, while filters come in two flavors — per-route GatewayFilters and GlobalFilters that apply to every route — and the `lb://` scheme lets the gateway resolve a logical service name through service discovery and load balancing. The two things I always keep in mind are that the gateway must never hold business logic, or it becomes a disguised monolith, and that it's a single point of failure, so it has to run with high availability.

### Vocabulário

| Português | Inglês |
| --- | --- |
| porta de entrada | API gateway / single entry point |
| rota | route |
| predicado | predicate |
| filtro | filter |
| preocupação transversal | cross-cutting concern |
| reescrita de caminho | path rewrite |
| ponto único de falha | single point of failure (SPOF) |
| descoberta de serviços | service discovery |

## Veja também

- [[03-Dominios/Java/Microservices e sistemas distribuídos/11 - Gateway reativo vs MVC — as duas variantes|Gateway reativo vs MVC]]
- [[03-Dominios/Java/Microservices e sistemas distribuídos/17 - Segurança entre serviços|Segurança entre serviços]] (planejado)
- [[03-Dominios/Java/Microservices e sistemas distribuídos/08 - Client-side load balancing — Spring Cloud LoadBalancer|Spring Cloud LoadBalancer]]
- [[03-Dominios/Java/Microservices e sistemas distribuídos/index|Microservices e sistemas distribuídos (MOC do galho)]]
- [[03-Dominios/Java/index|Trilha Java]]

## Referências

- Spring Cloud Gateway — Reference Documentation: https://docs.spring.io/spring-cloud-gateway/reference/
- Spring Cloud Gateway — Global Filters: https://docs.spring.io/spring-cloud-gateway/reference/spring-cloud-gateway-server-webflux/global-filters.html
