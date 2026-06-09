---
title: "Clientes HTTP — RestClient, WebClient, RestTemplate"
created: 2026-06-08
updated: 2026-06-08
type: concept
progress: backlog
status: seedling
publish: true
fase: magus
tags:
  - java
  - web
  - magus
  - http-client
aliases:
  - "RestClient"
  - "RestTemplate"
---

# Clientes HTTP — RestClient, WebClient, RestTemplate

> [!abstract] TL;DR
> Pra consumir outra API de forma bloqueante, o default moderno é o `RestClient` (Spring Framework 6.1+, API fluent). O `RestTemplate` é o legado em manutenção desde a 5.0 — ainda onipresente, mas você não começa código novo nele. O `WebClient` é o cliente reativo (parte do WebFlux; uso reativo/streaming = Galho 11, planejado). A escolha não é pelo hype: ela segue o modelo de execução do seu stack. Stack imperativo pede `RestClient`; stack reativo pede `WebClient`.

## O que é

Um cliente HTTP é o componente que o seu serviço usa quando ele mesmo precisa **chamar outra API** — buscar um catálogo de produtos, validar um endereço, disparar um webhook. É o lado oposto do `@RestController`: ali você recebe requisições, aqui você as emite.

O Spring oferece três clientes, e a confusão de qual usar vem do fato de que eles nasceram em épocas diferentes e resolvem problemas parcialmente sobrepostos:

- **`RestTemplate`** — o cliente clássico, baseado em template method (`getForObject`, `postForEntity`, `exchange`). Síncrono e bloqueante. Em **manutenção desde o Spring 5.0**: recebe correções, mas não ganha features novas.
- **`WebClient`** — introduzido no Spring 5.0 junto com o WebFlux. Reativo e não-bloqueante, construído sobre o Project Reactor (`Mono`/`Flux`). Suporta cenários síncronos, assíncronos e de streaming.
- **`RestClient`** — introduzido no **Spring Framework 6.1**. Síncrono e bloqueante como o `RestTemplate`, mas com a **API fluent** que o `WebClient` popularizou. É o sucessor natural do `RestTemplate` para código bloqueante.

A regra mental curta: `RestClient` é "o `WebClient` síncrono". Mesma ergonomia fluent, sem puxar o Reactor pro classpath.

## Por que importa

- **Microservices vivem de chamadas HTTP**: num sistema distribuído, cada serviço é cliente de vários outros. A qualidade desse cliente (timeouts, tratamento de erro, reuso) define a resiliência do sistema inteiro.
- **Escolher errado custa caro**: adotar `WebClient` num stack imperativo arrasta o Project Reactor e um modelo mental assíncrono que o time não pediu. Manter `RestTemplate` em código novo significa começar já no legado.
- **`RestTemplate` é onipresente**: bases de código com anos de idade estão cheias dele. Saber migrar pro `RestClient` — e saber por que migrar — é tema recorrente de revisão de arquitetura.
- **Os erros de cliente são silenciosos**: cliente sem timeout não falha no happy path; ele falha em produção, sob carga, quando a dependência fica lenta. Por isso o tema aparece como decisão de fase Magus, não de Iniciado.

## Como funciona

### RestClient (Framework 6.1+): o default síncrono moderno (API fluent)

O `RestClient` foi desenhado pra ser o ponto de chegada de quem precisa de chamadas bloqueantes. A API é fluent: você encadeia método HTTP, URI, headers, e termina com `retrieve().body(...)`.

```java
RestClient restClient = RestClient.create();

OrderDto order = restClient.get()
        .uri("https://catalog.example.com/orders/{id}", orderId)
        .accept(MediaType.APPLICATION_JSON)
        .retrieve()
        .body(OrderDto.class);
```

Pra produção você quase nunca usa `RestClient.create()` cru — você constrói um **bean configurado** com `baseUrl`, headers padrão, interceptors e request factory:

```java
@Configuration
public class HttpClientConfig {

    @Bean
    RestClient catalogClient(RestClient.Builder builder) {
        return builder
                .baseUrl("https://catalog.example.com")
                .defaultHeader("Accept", MediaType.APPLICATION_JSON_VALUE)
                .build();
    }
}
```

O Spring Boot já expõe um `RestClient.Builder` pré-configurado no contexto, então injetá-lo é o caminho idiomático. Internamente, o `RestClient` delega a transmissão a um `ClientHttpRequestFactory` (por padrão o `JdkClientHttpRequestFactory`, sobre o `java.net.http.HttpClient` do JDK), o mesmo ponto de extensão onde você configura timeouts.

### RestTemplate: o legado em manutenção (getForObject/exchange) e a migração pro RestClient

O `RestTemplate` usa o padrão **template method**: um método por combinação de verbo HTTP e tipo de retorno. Os mais comuns:

```java
RestTemplate restTemplate = new RestTemplate();

// Retorna o corpo desserializado direto:
OrderDto order = restTemplate.getForObject(
        "https://catalog.example.com/orders/{id}", OrderDto.class, orderId);

// Retorna o ResponseEntity completo (status, headers, corpo):
ResponseEntity<OrderDto> response = restTemplate.exchange(
        "https://catalog.example.com/orders/{id}",
        HttpMethod.GET,
        new HttpEntity<>(headers),
        OrderDto.class,
        orderId);
```

O `exchange` é o método "canivete suíço": dá controle total sobre verbo, headers de request e tipo de resposta. O `getForObject`/`postForObject` são atalhos para os casos simples.

**A migração pro `RestClient`** é direta porque o `RestClient` cobre tudo que o `RestTemplate` faz, com API mais legível. O mapeamento mental:

| RestTemplate | RestClient |
| --- | --- |
| `getForObject(url, Type.class)` | `get().uri(url).retrieve().body(Type.class)` |
| `exchange(url, GET, entity, Type.class)` | `get().uri(url).headers(...).retrieve().toEntity(Type.class)` |
| `postForEntity(url, body, Type.class)` | `post().uri(url).body(body).retrieve().toEntity(Type.class)` |

> [!tip] Reuso garantido na migração
> O `RestClient` pode ser construído a partir de um `RestTemplate` existente via `RestClient.create(restTemplate)`, herdando message converters e request factory já configurados. Isso permite migrar incrementalmente, sem reconfigurar tudo de uma vez.

Em versões recentes do Spring Framework, o `RestTemplate` deixou de ser apenas "em manutenção" e passou a ser **formalmente marcado como obsoleto** em favor do `RestClient`. O sinal é o mesmo desde a 5.0: comece código novo no `RestClient`.

### WebClient: menção — reativo, do WebFlux (uso reativo/streaming = Galho 11, planejado)

O `WebClient` é o cliente **não-bloqueante e reativo** do Spring. Ele faz parte do módulo WebFlux e trabalha sobre o Project Reactor: as respostas chegam como `Mono<T>` (zero ou um elemento) ou `Flux<T>` (stream de N elementos), com suporte a back-pressure.

```java
// Ilustrativo — o tipo de retorno é reativo (Mono), não o objeto direto:
Mono<OrderDto> orderMono = webClient.get()
        .uri("/orders/{id}", orderId)
        .retrieve()
        .bodyToMono(OrderDto.class);
```

Repare na diferença essencial: o `RestClient` te devolve `OrderDto`; o `WebClient` te devolve `Mono<OrderDto>`, um valor que ainda não chegou. Você só usa o `WebClient` quando o **resto do seu stack também é reativo** — caso contrário, você acaba bloqueando um fluxo reativo (`.block()`) e perde toda a vantagem, pagando a complexidade sem o benefício.

O uso aprofundado do `WebClient` — programação reativa, streaming de respostas, back-pressure — é tema do Galho 11 (planejado). Aqui ele entra só como o terceiro lado da escolha: existe, é reativo, e não é o que você quer num serviço imperativo.

### Timeouts e error handling no cliente (onStatus)

Dois cuidados separam um cliente de brinquedo de um cliente de produção.

**Timeouts.** Por padrão, muitos clientes esperam *indefinidamente* por uma resposta. Numa dependência lenta, isso prende a thread pra sempre e, sob carga, exaure o pool. Você configura timeouts no `ClientHttpRequestFactory`:

```java
@Bean
RestClient catalogClient(RestClient.Builder builder) {
    var settings = ClientHttpRequestFactorySettings.defaults()
            .withConnectTimeout(Duration.ofSeconds(2))
            .withReadTimeout(Duration.ofSeconds(5));

    return builder
            .baseUrl("https://catalog.example.com")
            .requestFactory(ClientHttpRequestFactories.get(settings))
            .build();
}
```

Os dois timeouts são distintos: **connect timeout** é o tempo máximo pra estabelecer a conexão TCP; **read timeout** é o tempo máximo esperando os dados depois de conectado.

**Error handling.** Por padrão, o `RestClient` lança uma exceção (`RestClientException` e subtipos) para respostas 4xx/5xx ao chamar `retrieve()`. Quando você quer um tratamento específico — converter num erro de domínio, logar, decidir por status — usa `onStatus`:

```java
OrderDto order = restClient.get()
        .uri("/orders/{id}", orderId)
        .retrieve()
        .onStatus(HttpStatusCode::is4xxClientError, (req, res) -> {
            throw new OrderNotFoundException(orderId);
        })
        .onStatus(HttpStatusCode::is5xxServerError, (req, res) -> {
            throw new CatalogUnavailableException();
        })
        .body(OrderDto.class);
```

Pra aplicar a política a *todas* as chamadas de um cliente, configure um `defaultStatusHandler` no builder. O equivalente no `RestTemplate` é o `ResponseErrorHandler` — mais verboso, e mais um motivo pra preferir o `RestClient`.

## Na prática

Cenário típico: um serviço de pedidos consulta um serviço de catálogo. Um único bean `RestClient`, com `baseUrl`, timeouts e tratamento de erro, reusado em todas as chamadas.

```java
@Configuration
public class CatalogClientConfig {

    @Bean
    RestClient catalogClient(RestClient.Builder builder) {
        var settings = ClientHttpRequestFactorySettings.defaults()
                .withConnectTimeout(Duration.ofSeconds(2))
                .withReadTimeout(Duration.ofSeconds(5));

        return builder
                .baseUrl("https://catalog.example.com")
                .defaultHeader("Accept", MediaType.APPLICATION_JSON_VALUE)
                .requestFactory(ClientHttpRequestFactories.get(settings))
                .build();
    }
}

@Service
public class CatalogGateway {

    private final RestClient catalogClient;

    public CatalogGateway(RestClient catalogClient) {
        this.catalogClient = catalogClient;
    }

    public OrderDto fetchOrder(Long orderId) {
        return catalogClient.get()
                .uri("/orders/{id}", orderId)
                .retrieve()
                .onStatus(HttpStatusCode::is4xxClientError, (req, res) -> {
                    throw new OrderNotFoundException(orderId);
                })
                .body(OrderDto.class);
    }

    public ProductDto createProduct(ProductDto product) {
        return catalogClient.post()
                .uri("/products")
                .contentType(MediaType.APPLICATION_JSON)
                .body(product)
                .retrieve()
                .body(ProductDto.class);
    }
}
```

Os três pilares estão todos aqui: **bean único reusado** (injetado, não instanciado por chamada), **timeouts configurados** (connect + read) e **erro tratado** (`onStatus` convertendo 4xx num erro de domínio).

## Armadilhas

### (1) Instanciar `new RestTemplate()` (ou `RestClient.create()`) a cada chamada

Criar um cliente novo dentro de cada método joga fora todo o estado caro: pool de conexões, message converters configurados, request factory. Sob carga, isso multiplica o custo de setup e impede reuso de conexões keep-alive.

```java
// RUIM — um cliente novo, sem config, a cada chamada:
public OrderDto fetchOrder(Long id) {
    RestTemplate rt = new RestTemplate(); // timeouts default (infinitos!), zero reuso
    return rt.getForObject("https://catalog.example.com/orders/" + id, OrderDto.class);
}
```

**Fix:** crie **um bean** (`@Bean RestClient ...`) configurado uma vez e injete-o onde precisar. O cliente é thread-safe; um por dependência é o padrão.

### (2) Cliente sem timeout (thread presa pra sempre)

Sem `connectTimeout`/`readTimeout`, uma dependência que trava deixa a thread chamadora esperando indefinidamente. Sob tráfego, as threads se acumulam até o pool do servidor esgotar — e aí o *seu* serviço cai por causa de uma dependência lenta.

```java
// RUIM — sem timeout: uma dependência lenta vira indisponibilidade sua.
RestClient client = RestClient.create();
```

**Fix:** sempre configure timeouts no `ClientHttpRequestFactory`. Um read timeout na casa de poucos segundos é o mínimo; ajuste pelo SLA da dependência.

### (3) Ignorar o status de erro do cliente (não tratar 4xx/5xx)

Mesmo que o `RestClient` lance exceção por padrão, deixar a exceção genérica subir sem tratamento esconde a causa real (404 de recurso inexistente vs. 503 da dependência fora do ar) e vaza detalhes de transporte pra camadas que não deveriam conhecê-los.

```java
// RUIM — qualquer erro vira a mesma exceção genérica e opaca:
OrderDto order = restClient.get().uri("/orders/{id}", id)
        .retrieve()
        .body(OrderDto.class); // 404? 503? quem chamou não sabe.
```

**Fix:** use `onStatus` (ou um `defaultStatusHandler` no builder) pra converter cada faixa de status num erro de domínio significativo, que a sua camada de exceções saiba traduzir.

### (4) Escolher `WebClient` "porque é novo" num stack imperativo

Adotar o `WebClient` num serviço Spring MVC tradicional arrasta o Project Reactor e um modelo assíncrono que o time não vai usar — quase sempre terminando com um `.block()` que bloqueia o fluxo reativo e anula o ganho. Você paga a complexidade do reativo sem colher nenhum benefício.

```java
// RUIM — num stack imperativo, isto é WebClient com freio de mão puxado:
OrderDto order = webClient.get().uri("/orders/{id}", id)
        .retrieve()
        .bodyToMono(OrderDto.class)
        .block(); // bloqueia o reativo: o pior dos dois mundos
```

**Fix:** num stack imperativo, use `RestClient`. Reserve o `WebClient` para quando o serviço inteiro for reativo (tema do Galho 11, planejado).

## Em entrevista

### Frase pronta (inglês)

> For blocking HTTP calls in modern Spring, the default is `RestClient`, introduced in Spring Framework 6.1 — it offers the same fluent API as `WebClient` but stays synchronous, so it doesn't pull in the reactive stack. `RestTemplate` has been in maintenance mode since 5.0 and is being phased out in favor of `RestClient`, so I migrate from it whenever I touch legacy code, mapping `getForObject`/`exchange` calls to the fluent `retrieve().body(...)` form. I only reach for `WebClient` when the whole service is reactive; otherwise I'd just be blocking a `Mono` and paying for Reactor with no benefit. In every case I configure connect and read timeouts on the `ClientHttpRequestFactory` and handle 4xx/5xx explicitly with `onStatus`, instead of letting a slow dependency take my threads down.

### Vocabulário

| Português | English |
| --- | --- |
| cliente HTTP | HTTP client |
| bloqueante / não-bloqueante | blocking / non-blocking |
| em manutenção (legado) | in maintenance mode (legacy) |
| API fluente | fluent API |
| timeout de leitura / conexão | read / connect timeout |
| tratamento de erro | error handling |
| pool de conexões | connection pool |
| stack reativo / imperativo | reactive / imperative stack |

## Veja também

- [[03-Dominios/Java/Web e APIs REST/02 - @RestController e os mapeamentos|@RestController e os mapeamentos]]
- [[03-Dominios/Java/Web e APIs REST/05 - Serialização JSON com Jackson|Serialização JSON com Jackson]]
- [[03-Dominios/Java/Web e APIs REST/index|Web e APIs REST]]
- [[03-Dominios/Java/index|Trilha Java]]
- Verbetes: [[03-Dominios/Java/Dicionário de Java#RestClient|RestClient]], [[03-Dominios/Java/Dicionário de Java#RestTemplate|RestTemplate]], [[03-Dominios/Java/Dicionário de Java#WebClient|WebClient]]

O uso reativo/streaming do `WebClient` (WebFlux/Reactor) é tema do Galho 11 (planejado). O cliente declarativo `@FeignClient` (Spring Cloud OpenFeign) — orientado a microservices, com service discovery e load balancing — é tema do Galho 16 (planejado); ele fecha o leque "e o Feign?", mas pertence ao mundo do Spring Cloud, não ao core do Spring Framework. Ambos aparecem aqui só como menção de fronteira, sem wikilink.

## Referências

- Spring Framework Reference — REST Clients: https://docs.spring.io/spring-framework/reference/integration/rest-clients.html
- Spring Framework Reference — RestClient: https://docs.spring.io/spring-framework/reference/integration/rest-clients.html#rest-restclient
- Spring Framework Reference — RestTemplate (maintenance/migration): https://docs.spring.io/spring-framework/reference/integration/rest-clients.html#rest-resttemplate
- Spring Framework Reference — WebClient: https://docs.spring.io/spring-framework/reference/web/webflux-webclient.html
