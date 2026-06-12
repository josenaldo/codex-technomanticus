---
title: "Comunicação síncrona — OpenFeign e @HttpExchange"
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
  - feign
aliases:
  - "OpenFeign"
  - "@HttpExchange"
  - "HTTP Interface clients"
---

# Comunicação síncrona — OpenFeign e @HttpExchange

> [!abstract] TL;DR
> Quando o eixo da decisão é **síncrono**, você precisa de um **cliente HTTP declarativo**: em vez de montar a requisição à mão, você escreve uma *interface* Java e o framework gera a implementação que fala HTTP por baixo.
> - **OpenFeign** (`@FeignClient`, `@EnableFeignClients`) foi o padrão de fato no mundo Spring Cloud por anos. Hoje está **feature-complete** desde Spring Cloud **2022.0.0 "Kilburn"** (16/dez/2022): só recebe *bugfix*, sem features novas.
> - A Spring agora recomenda os **HTTP Interface clients** (`@HttpExchange`), nativos do **Spring Framework 6.1+**, que rodam **sobre `RestClient`/`WebClient`** (Galho 9) e **não exigem Spring Cloud**.
> - Spring Cloud **2025.1** trouxe **load balancing + circuit breaking** transparentes para os **HTTP service groups** — fechando a última lacuna que ainda justificava o Feign.
> Regra de bolso: **projeto novo → `@HttpExchange`.** Feign só permanece em base legada que já o usa.

## O que é

No [[03-Dominios/Java/Microservices e sistemas distribuídos/05 - Comunicação inter-serviços — síncrono vs assíncrono|eixo síncrono]], um serviço chama outro pela rede e **espera a resposta**. Você *poderia* fazer isso na unha, montando uma requisição com o cliente HTTP base — mas escrever URL, método, headers e desserialização a cada chamada é repetitivo e propenso a erro.

A solução idiomática no ecossistema Spring é o **cliente declarativo**: você descreve a chamada como uma **interface Java anotada**, e o framework gera em runtime uma implementação (um *proxy*) que executa o HTTP de verdade. Você programa contra o contrato; o transporte fica escondido.

Existem dois protagonistas para isso em Java/Spring:

1. **OpenFeign** — o projeto **Spring Cloud OpenFeign**, integração do Spring com a biblioteca Feign (originalmente da Netflix). Anotações `@FeignClient` na interface, `@EnableFeignClients` para ligar o scanning. Foi a escolha-padrão por toda a era do Spring Cloud Netflix.
2. **HTTP Interface clients** — recurso **nativo do Spring Framework** (6.1+), com `@HttpExchange` e os verbos `@GetExchange`, `@PostExchange` etc. **Não depende de Spring Cloud**: roda sobre o `RestClient` ou o `WebClient` que você já conhece do [[03-Dominios/Java/Web e APIs REST/15 - Clientes HTTP — RestClient, WebClient, RestTemplate|Galho 9]].

> [!info] Feynman: o garçom que você não vê cozinhar
> Pense numa interface declarativa como o cardápio de um restaurante. Você aponta para o prato ("`getOrder(id)`") e o garçom traz. Você não sabe — nem quer saber — como a cozinha (o cliente HTTP base) montou o prato. O *proxy* gerado é esse garçom: ele traduz seu pedido declarativo em uma chamada de rede concreta. Trocar Feign por `@HttpExchange` é trocar o garçom; a cozinha (o `RestClient`) pode ser a mesma.

Esta nota **fecha o gancho do Feign** que ficou em aberto no Galho 9: lá você viu os clientes HTTP base; aqui você vê a camada declarativa por cima deles.

## Por que importa

Porque a escolha de cliente síncrono é uma **aposta de longo prazo** sobre a qual time inteiro vai construir. Escolher errado em 2026 significa apostar em uma tecnologia que **não vai mais evoluir**.

O ponto duro: **OpenFeign está feature-complete**. Citando a própria documentação do projeto:

> *"As announced in Spring Cloud 2022.0.0 release blog entry, we're now treating the Spring Cloud OpenFeign project as feature-complete. We are only going to be adding bugfixes and possibly merging some small community feature PRs."*
> — docs.spring.io/spring-cloud-openfeign/reference

Traduzindo o que "feature-complete" significa na prática:
- **Bugfix?** Sim, continua recebendo.
- **Feature nova?** Não — no máximo um PR pequeno de comunidade. Nada de roadmap.
- **Recomendação oficial?** Migrar para os **HTTP Service Clients** do Spring Framework.

Ou seja: o Feign não está *quebrado*, nem foi removido. Mas a água parou de correr. Qualquer recurso novo do mundo HTTP — e a própria menção do Spring é explícita ao apontar para o `@HttpExchange` — vai chegar **do outro lado**. Saber disso é o que separa quem segue a corrente do framework de quem fica preso numa tecnologia em manutenção.

E há a fronteira da resiliência: **chamada síncrona é uma cascata esperando para acontecer** se você confiar nela sem timeout e circuit breaker. Isso vale para Feign e para `@HttpExchange` igualmente, e é assunto das notas de resiliência deste galho.

## Como funciona

### OpenFeign e o feature-complete

**OpenFeign** liga a chamada a uma interface anotada com `@FeignClient`. Você nomeia o serviço-alvo, declara os métodos com as mesmas anotações MVC que já conhece (`@GetMapping`, `@PostMapping`), e o Spring Cloud gera o cliente.

```java
@FeignClient(name = "payment-service")
public interface PaymentClient {
    @PostMapping("/payments")
    PaymentResult charge(@RequestBody PaymentRequest request);
}
```

Para ativar, você anota uma classe de configuração com `@EnableFeignClients`. Por baixo, o Feign integra com **service discovery** e **load balancing** do Spring Cloud quase de graça — historicamente foi *esse* o seu grande atrativo: você escrevia `name = "payment-service"` (um nome lógico, não uma URL) e o Spring Cloud LoadBalancer resolvia para uma instância real.

O detalhe decisivo: desde **Spring Cloud 2022.0.0 "Kilburn"** (16 de dezembro de 2022), o projeto é **feature-complete**. Ele funciona, é estável, recebe bugfix — mas **não terá features novas**, e a recomendação da própria Spring é migrar. Feign não é mais o futuro; é o presente que para de crescer.

### HTTP Interface `@HttpExchange`

Os **HTTP Interface clients** são a aposta atual da Spring. A ideia é a mesma — interface declarativa — mas o recurso é **do Spring Framework (6.1+)**, não do Spring Cloud, e roda **sobre os clientes HTTP base do Galho 9**.

```java
@HttpExchange("/payments")
public interface PaymentClient {
    @PostExchange
    PaymentResult charge(@RequestBody PaymentRequest request);
}
```

Anotações: `@HttpExchange` no tipo (atributos comuns: URL base, `accept`, `contentType`) e os verbos por método — `@GetExchange`, `@PostExchange`, `@PutExchange`, `@PatchExchange`, `@DeleteExchange`. Parâmetros usam `@PathVariable`, `@RequestParam`, `@RequestHeader`, `@RequestBody`, idênticos ao mundo MVC.

A mecânica por baixo é o **`HttpServiceProxyFactory`**, que cria o proxy a partir da interface, ligado a um **adapter** sobre o cliente HTTP base:

| Adapter | Cliente base | Modelo |
| --- | --- | --- |
| `RestClientAdapter` | `RestClient` | síncrono |
| `WebClientAdapter` | `WebClient` | reativo |
| `RestTemplateAdapter` | `RestTemplate` | síncrono legado |

> [!important] Fronteira de galho — Galho 9 (Web/REST)
> O **`RestClient`/`WebClient`/`RestTemplate`** são o cliente HTTP *base* e foram explicados no [[03-Dominios/Java/Web e APIs REST/15 - Clientes HTTP — RestClient, WebClient, RestTemplate|Galho 9]]. **Esta nota não os re-explica** — só mostra que o `@HttpExchange` é a camada *declarativa* por cima deles. Se a dúvida for "como configuro o `RestClient`?", a resposta está lá, não aqui.

E o que faltava? Por anos, a vantagem do Feign foi o **load balancing transparente** via nome lógico. O `@HttpExchange` puro do Framework não trazia isso de fábrica. Mudou: **Spring Cloud 2025.1** adicionou suporte transparente a **load balancing e circuit breaking** para os **HTTP service groups** — um *grupo* sendo, nas palavras do blog da Spring, *"a set of HTTP services that share the same HTTP client configuration, and the resulting client instance"*. Com isso, a última grande justificativa para continuar no Feign cai.

### Quando migrar / qual escolher

A decisão, em 2026, é direta:

| Situação | Escolha |
| --- | --- |
| Projeto **novo** | **`@HttpExchange`** (HTTP Interface clients) |
| Base **legada** que já usa Feign, estável | Manter Feign por ora; migrar quando houver oportunidade |
| Precisa só de Spring Framework, sem Spring Cloud | `@HttpExchange` (Feign exige Spring Cloud) |
| Precisa de LB + circuit breaker no cliente declarativo | `@HttpExchange` + Spring Cloud **2025.1+** (HTTP service groups) |

Não há urgência em *arrancar* Feign de uma base que funciona — feature-complete não é deprecated. Mas **não se começa projeto novo com Feign**: você estaria adotando uma tecnologia que a própria Spring já apontou como caminho de saída.

## Na prática

O mesmo cliente — `order-service` chamando `payment-service` — escrito nos dois estilos, lado a lado:

```java
// ===== OpenFeign (feature-complete — base legada) =====
// Requer Spring Cloud OpenFeign + @EnableFeignClients na config.

@FeignClient(name = "payment-service")
public interface PaymentFeignClient {

    @PostMapping("/payments")
    PaymentResult charge(@RequestBody PaymentRequest request);

    @GetMapping("/payments/{id}")
    PaymentResult find(@PathVariable("id") String id);
}


// ===== HTTP Interface — @HttpExchange (recomendado — Spring Framework 6.1+) =====
// Nativo do Framework; roda sobre RestClient/WebClient (Galho 9).

@HttpExchange("/payments")
public interface PaymentHttpClient {

    @PostExchange
    PaymentResult charge(@RequestBody PaymentRequest request);

    @GetExchange("/{id}")
    PaymentResult find(@PathVariable String id);
}
```

A fábrica do proxy para o `@HttpExchange`, usando o `RestClient` base (definido no Galho 9):

```java
@Configuration
class PaymentClientConfig {

    @Bean
    PaymentHttpClient paymentHttpClient(RestClient.Builder builder) {
        // o RestClient base e seu tuning (timeout, baseUrl) vêm do Galho 9
        RestClient restClient = builder
                .baseUrl("http://payment-service")
                .build();

        var adapter = RestClientAdapter.create(restClient);
        var factory = HttpServiceProxyFactory.builderFor(adapter).build();

        return factory.createClient(PaymentHttpClient.class);
    }
}
```

Configuração via `application.yml` — o Spring Boot expõe propriedades para os HTTP service clients, e o Spring Cloud 2025.1+ liga LB e circuit breaker por grupo:

```yaml
spring:
  http:
    client:
      # baseUrl, timeouts e demais ajustes do cliente base (Galho 9)
      connect-timeout: 2s
      read-timeout: 5s

# OpenFeign (quando ainda em uso na base legada)
feign:
  client:
    config:
      payment-service:
        connect-timeout: 2000
        read-timeout: 5000
```

Repare: a interface declarativa muda pouco entre os dois mundos. A migração de Feign para `@HttpExchange` é, na maioria dos casos, troca de anotações (`@PostMapping` → `@PostExchange`) e a forma de instanciar o cliente.

## Armadilhas

### (1) Começar um projeto novo só com Feign

Feign é confortável: muita gente já sabe, há tutoriais por toda parte, e ele "simplesmente funciona". A tentação de começar um serviço novo com `@FeignClient` é real — e é a armadilha. Você estaria adotando, em projeto greenfield, uma tecnologia **feature-complete** que a própria Spring recomenda *deixar*. Cada interface Feign nova é uma futura migração que você está marcando para si mesmo. **Projeto novo começa com `@HttpExchange`.**

### (2) Confiar no Feign para evoluir

"Tudo bem, eu uso Feign e quando precisar de uma feature nova eu peço/espero." Não vai chegar. Feature-complete significa, textualmente, *"only going to be adding bugfixes and possibly merging some small community feature PRs"*. Não há roadmap de features. Construir a *estratégia de evolução* do seu cliente HTTP em cima do Feign é apostar num projeto que, por decisão oficial, parou de crescer em 2022. Bugfix você tem; futuro, não.

### (3) Chamada síncrona sem timeout / circuit breaker

Esta vale para **os dois** clientes igualmente, e é a mais perigosa. Uma chamada síncrona sem **timeout** fica pendurada para sempre quando o outro lado trava, segurando threads e conexões até esgotar o pool — e aí o *seu* serviço cai por causa do alheio. Sem **circuit breaker**, uma falha do `payment-service` vira falha do `order-service` em cascata. O cliente declarativo torna a chamada *fácil de escrever*, o que paradoxalmente torna fácil esquecer que ainda é **rede hostil**. Timeout sempre; circuit breaker e fallback nas chamadas críticas. Esse é o assunto das notas de resiliência deste galho — ver [[03-Dominios/Java/Microservices e sistemas distribuídos/13 - Resiliência I — a falha distribuída e o Circuit Breaker|Circuit Breaker]] e [[03-Dominios/Java/Microservices e sistemas distribuídos/14 - Resiliência II — Retry e Time Limiter|Retry e Time Limiter]].

## Em entrevista

### Frase pronta (inglês)

> "For synchronous inter-service calls in Spring, I reach for a declarative HTTP client — you describe the call as a Java interface and the framework generates the proxy. OpenFeign was the de-facto standard for years, but it's been feature-complete since Spring Cloud 2022.0.0 'Kilburn', meaning it only gets bugfixes, no new features, and Spring itself recommends migrating away from it. The current recommendation is HTTP Interface clients with `@HttpExchange`, which are native to Spring Framework 6.1 and up — they run on top of `RestClient` or `WebClient`, so they don't even require Spring Cloud. The last gap was load balancing, and Spring Cloud 2025.1 closed it by adding transparent load balancing and circuit breaking to HTTP service groups. So for any new project I start with `@HttpExchange`; I'd only keep Feign in legacy code that already uses it. Either way, a synchronous call without a timeout and a circuit breaker is a cascading failure waiting to happen — that part is non-negotiable."

### Vocabulário

| Português | Inglês |
| --- | --- |
| cliente declarativo | declarative client |
| completo em features | feature-complete |
| interface HTTP | HTTP interface |
| grupo de serviço HTTP | HTTP service group |
| adaptador | adapter |
| proxy gerado | generated proxy |
| balanceamento de carga | load balancing |
| disjuntor / circuit breaker | circuit breaker |

## Veja também

- [[03-Dominios/Java/Microservices e sistemas distribuídos/05 - Comunicação inter-serviços — síncrono vs assíncrono|Comunicação inter-serviços]] — o eixo síncrono vs assíncrono que esta nota aprofunda do lado síncrono
- [[03-Dominios/Java/Microservices e sistemas distribuídos/16 - Resiliência IV — compondo os padrões|Resiliência (compondo os padrões)]] — por que toda chamada síncrona precisa de rede de proteção
- [[03-Dominios/Java/Web e APIs REST/15 - Clientes HTTP — RestClient, WebClient, RestTemplate|Clientes HTTP (Galho 9)]] — fronteira: o cliente HTTP base sobre o qual o `@HttpExchange` roda (não re-explicado aqui)
- [[03-Dominios/Java/Microservices e sistemas distribuídos/index|Microservices e sistemas distribuídos (MOC do galho)]]
- [[03-Dominios/Java/index|Trilha Java]]

## Referências

- *Spring Cloud OpenFeign — Reference*. docs.spring.io/spring-cloud-openfeign/reference — aviso de *feature-complete* desde Spring Cloud 2022.0.0 "Kilburn"; recomendação de migrar para os HTTP Service Clients do Spring Framework. (acesso 2026-06-12)
- *Spring Cloud 2022.0.0 (codename Kilburn) has been released* — spring.io/blog, 16/dez/2022 — anúncio original do *feature-complete* do OpenFeign.
- *REST Clients — HTTP Interface*. docs.spring.io/spring-framework/reference/integration/rest-clients.html — `@HttpExchange`, `HttpServiceProxyFactory`, adapters (`RestClientAdapter`/`WebClientAdapter`/`RestTemplateAdapter`); Spring Framework 6.1+; independente de Spring Cloud. (acesso 2026-06-12)
- *HTTP Service Client Enhancements* — spring.io/blog, 23/set/2025 — load balancing e circuit breaking transparentes para HTTP service groups no Spring Cloud 2025.1; definição de *group* como conjunto de serviços que compartilham configuração de cliente.
