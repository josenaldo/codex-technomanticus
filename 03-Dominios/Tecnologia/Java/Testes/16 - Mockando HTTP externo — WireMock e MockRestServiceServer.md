---
title: "Mockando HTTP externo — WireMock e MockRestServiceServer"
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
  - wiremock
  - spring-test
aliases:
  - "WireMock"
  - "MockRestServiceServer"
---

# Mockando HTTP externo — WireMock e MockRestServiceServer

> [!abstract] TL;DR
> Pra testar a integração com uma API externa sem depender dela, suba um **WireMock** (um servidor HTTP de mentira que faz *stub* das respostas) e aponte o seu client pra ele via `@DynamicPropertySource`. Você controla status, corpo, latência e até falhas intermitentes (cenários de retry) — e ainda pode **verificar** que a chamada saiu com a URL/headers certos. Em apps Spring que usam `RestClient`/`RestTemplate`, a alternativa leve é `@RestClientTest` + `MockRestServiceServer`: nada de socket real, o transporte é interceptado em memória.

## O que é

São duas formas de testar o código que **consome** uma API externa, isolando o teste do servidor real:

- **WireMock** — um servidor HTTP de verdade (sobe numa porta, fala TCP), programável pra responder o que você mandar. O seu client conecta nele como se fosse a API real. É *transport-real, server-fake*: passa pela serialização, pela URL, pelos headers, pela camada de rede.
- **MockRestServiceServer** — utilitário do Spring Test que **intercepta o transporte** do `RestClient`/`RestTemplate` em memória, sem abrir socket. É *transport-fake*: mais rápido e leve, mas só funciona com clients Spring e não exercita a pilha de rede.

Ambos resolvem o mesmo problema — "como testo o meu client sem bater na API de produção?" — em níveis de fidelidade diferentes.

## Por que importa

Bater na API externa real no teste é o caminho mais curto pra um suite **flaky**: a rede cai, a API tem rate limit, o ambiente de staging fica fora do ar, a resposta muda sem aviso. Pior: você não consegue forçar os casos que mais interessam — o `500`, o timeout, o JSON malformado, o retry que só funciona na segunda tentativa.

Mockar o HTTP externo te dá **controle total e determinismo**: o teste roda igual no seu laptop e no CI, offline, em milissegundos. E — ponto que muita gente esquece — testar contra um servidor *fake* (não contra um mock do próprio client) preserva o que importa: a montagem da URL, a serialização do corpo, os headers de auth, o parsing da resposta. É exatamente aí que os bugs de integração moram.

## Como funciona

### Por que mockar o HTTP externo (não depender da API real, controlar respostas)

A regra de ouro: **mocke o transporte, não a abstração**. O seu `ExternalOrderClient` provavelmente embrulha um `RestClient`. Se você der `mock(ExternalOrderClient.class)`, o teste vira tautologia — você está testando que o mock retorna o que você mandou ele retornar, e o código real (URL, headers, parsing) nunca roda.

Mockar no nível HTTP coloca o ponto de corte *depois* de todo o código que você quer testar. O client monta a requisição de verdade, serializa de verdade, e só a resposta vem de um servidor controlado. Bônus: você consegue **simular falhas** que a API real raramente entrega sob demanda — `503`, latência alta, conexão resetada — e verificar que o seu retry/circuit-breaker reage certo.

### WireMock: stubFor / verify / cenários (retry)

O verbo central é `stubFor`, que registra um *stub*: "quando chegar uma requisição que casa com X, responda Y".

```java
wireMock.stubFor(get(urlEqualTo("/orders/42"))
    .willReturn(ok()
        .withHeader("Content-Type", "application/json")
        .withBody("""
            {"id":42,"customer":"Order-Customer","total":199.90}
            """)));
```

Pra **verificar** que a chamada realmente aconteceu (e com a forma certa), use `verify` com um *request matcher*:

```java
wireMock.verify(getRequestedFor(urlEqualTo("/orders/42"))
    .withHeader("Authorization", matching("Bearer .+")));
```

Pra **falhas intermitentes** (testar retry), WireMock tem **cenários**: um stub muda o estado do cenário, e outro stub só casa naquele estado. Assim a mesma URL responde diferente a cada chamada:

```java
wireMock.stubFor(get(urlEqualTo("/orders/42"))
    .inScenario("retry")
    .whenScenarioStateIs(Scenario.STARTED)
    .willReturn(aResponse().withStatus(503))
    .willSetStateTo("recovered"));

wireMock.stubFor(get(urlEqualTo("/orders/42"))
    .inScenario("retry")
    .whenScenarioStateIs("recovered")
    .willReturn(ok().withBody("{\"id\":42}")));
```

Primeira chamada leva `503` e avança o estado; a segunda já encontra o estado `recovered` e leva `200`. Perfeito pra provar que o seu client tenta de novo.

### @DynamicPropertySource: apontar o client pro WireMock

WireMock sobe numa **porta dinâmica** (`dynamicPort()`) pra evitar colisão no CI e em testes paralelos. Mas aí você não sabe a URL de antemão — ela só existe depois que o servidor sobe. A ponte é `@DynamicPropertySource`: um método estático que **injeta a base-url do WireMock na configuração** antes do contexto Spring subir, sobrescrevendo a URL de produção.

```java
@DynamicPropertySource
static void overrideBaseUrl(DynamicPropertyRegistry registry) {
    registry.add("external.api.base-url", wireMock::baseUrl);
}
```

Repare que você passa `wireMock::baseUrl` (um `Supplier`), não o valor — porque a porta só é conhecida no momento da resolução. O seu `ExternalOrderClient`, configurado via `@Value("${external.api.base-url}")` ou `@ConfigurationProperties`, passa a apontar pro WireMock de forma transparente.

### @RestClientTest + MockRestServiceServer (alternativa Spring)

Quando o client é um `RestClient`/`RestTemplate` Spring e você não precisa de socket real, `@RestClientTest` carrega só a fatia necessária e expõe um `MockRestServiceServer`. Ele **intercepta o transporte** em memória: nenhuma porta é aberta.

```java
mockServer.expect(requestTo("/orders/42"))
    .andExpect(method(HttpMethod.GET))
    .andRespond(withSuccess("{\"id\":42}", MediaType.APPLICATION_JSON));
```

E `mockServer.verify()` confere que **todas** as expectativas foram satisfeitas (na ordem, por padrão). É mais rápido que WireMock e ótimo pra teste de unidade do client, mas não exercita serialização real de rede nem casos como reset de conexão — pra esses, WireMock ganha.

## Na prática

Os exemplos usam domínios neutros — um `ExternalOrderClient` que busca pedidos numa API externa. Não re-explicamos o `RestClient` em si; isso é assunto do [[03-Dominios/Tecnologia/Java/Web e APIs REST/15 - Clientes HTTP — RestClient, WebClient, RestTemplate|Galho 9]].

**WireMock com porta dinâmica + `@DynamicPropertySource`:**

```java
@SpringBootTest
class ExternalOrderClientWireMockTest {

    static WireMockServer wireMock =
        new WireMockServer(options().dynamicPort());

    @Autowired
    ExternalOrderClient client;

    @BeforeAll
    static void startServer() {
        wireMock.start();
    }

    @AfterAll
    static void stopServer() {
        wireMock.stop();
    }

    @AfterEach
    void resetStubs() {
        wireMock.resetAll();
    }

    @DynamicPropertySource
    static void overrideBaseUrl(DynamicPropertyRegistry registry) {
        registry.add("external.api.base-url", wireMock::baseUrl);
    }

    @Test
    void buscaPedidoEParseiaResposta() {
        wireMock.stubFor(get(urlEqualTo("/orders/42"))
            .willReturn(ok()
                .withHeader("Content-Type", "application/json")
                .withBody("""
                    {"id":42,"customer":"Order-Customer","total":199.90}
                    """)));

        Order order = client.findById(42L);

        assertThat(order.id()).isEqualTo(42L);
        assertThat(order.customer()).isEqualTo("Order-Customer");

        // não basta o assert da resposta: prove que a chamada saiu certa
        wireMock.verify(getRequestedFor(urlEqualTo("/orders/42"))
            .withHeader("Authorization", matching("Bearer .+")));
    }
}
```

**Cenário de retry (mesma URL, respostas diferentes):**

```java
@Test
void tentaDeNovoApos503() {
    wireMock.stubFor(get(urlEqualTo("/orders/42"))
        .inScenario("retry")
        .whenScenarioStateIs(Scenario.STARTED)
        .willReturn(aResponse().withStatus(503))
        .willSetStateTo("recovered"));

    wireMock.stubFor(get(urlEqualTo("/orders/42"))
        .inScenario("retry")
        .whenScenarioStateIs("recovered")
        .willReturn(ok().withBody("{\"id\":42}")));

    Order order = client.findById(42L); // 1ª = 503, 2ª = 200

    assertThat(order.id()).isEqualTo(42L);
    wireMock.verify(2, getRequestedFor(urlEqualTo("/orders/42")));
}
```

**Alternativa Spring com `@RestClientTest` + `MockRestServiceServer`:**

```java
import static org.springframework.test.web.client.match.MockRestRequestMatchers.*;
import static org.springframework.test.web.client.response.MockRestResponseCreators.*;

@RestClientTest(ExternalOrderClient.class)
class ExternalOrderClientSliceTest {

    @Autowired
    ExternalOrderClient client;

    @Autowired
    MockRestServiceServer mockServer;

    @Test
    void buscaPedido() {
        mockServer.expect(requestTo("/orders/42"))
            .andExpect(method(HttpMethod.GET))
            .andRespond(withSuccess(
                "{\"id\":42,\"customer\":\"Order-Customer\"}",
                MediaType.APPLICATION_JSON));

        Order order = client.findById(42L);

        assertThat(order.customer()).isEqualTo("Order-Customer");
        mockServer.verify(); // todas as expectativas foram satisfeitas?
    }
}
```

## Armadilhas

### (1) Porta fixa do WireMock colide no CI e em testes paralelos

Subir o WireMock com `options().port(8080)` parece inofensivo até dois testes rodarem ao mesmo tempo (CI paralelo, build multi-módulo) e brigarem pela mesma porta — `BindException: Address already in use`. O teste falha de forma intermitente e ninguém entende por quê.

```java
// ❌ porta fixa: bomba-relógio no CI
new WireMockServer(options().port(8080));
```

Fix: use `dynamicPort()` e descubra a porta em runtime via `wireMock.baseUrl()` / `wireMock.port()`, injetando no client com `@DynamicPropertySource`.

```java
// ✅ porta dinâmica, sem colisão
new WireMockServer(options().dynamicPort());
```

### (2) Não verificar que a chamada realmente aconteceu

Um teste que só faz `assertThat(order.id()).isEqualTo(42)` prova que *algo* retornou — mas não que o seu client chamou a URL certa, com o método certo, com o header de auth. Se o código tivesse um bug que monta `/order/42` (singular) e por acaso o stub fosse permissivo, o teste poderia passar enganado, ou o stub silenciosamente não casaria.

```java
// ❌ confia só na resposta; a URL/headers ficam sem cobertura
Order order = client.findById(42L);
assertThat(order.id()).isEqualTo(42L);
```

Fix: feche o teste com `verify` (WireMock) ou `mockServer.verify()` (Spring), afirmando a forma exata da requisição que saiu.

```java
// ✅ prova a requisição, não só a resposta
wireMock.verify(getRequestedFor(urlEqualTo("/orders/42"))
    .withHeader("Authorization", matching("Bearer .+")));
```

### (3) Mockar o próprio client em vez do transporte HTTP

A tentação preguiçosa é `mock(ExternalOrderClient.class)` e mandar ele devolver um `Order` pronto. O teste fica verde e inútil: a montagem da URL, a serialização do corpo, os headers e o parsing da resposta — todo o código que de fato pode quebrar na integração — nunca executa. Você testou o Mockito, não o seu client.

```java
// ❌ tautologia: o código real do client nunca roda
ExternalOrderClient client = mock(ExternalOrderClient.class);
when(client.findById(42L)).thenReturn(new Order(42L, "Order-Customer"));
```

Fix: deixe o client **real** e mocke o nível HTTP — WireMock (transporte real) ou `MockRestServiceServer` (transporte interceptado). O ponto de corte tem que ficar *abaixo* do código sob teste.

```java
// ✅ client real; só a resposta HTTP é controlada
mockServer.expect(requestTo("/orders/42"))
    .andRespond(withSuccess("{\"id\":42}", MediaType.APPLICATION_JSON));
Order order = client.findById(42L);
```

## Em entrevista

### Frase pronta (inglês)

> When I test code that calls an external API, I mock at the HTTP transport level, not at the client abstraction — otherwise the test becomes a tautology and never exercises URL building, serialization, or response parsing. I usually reach for WireMock: it boots a real HTTP server on a dynamic port, I stub the responses with `stubFor`, point my client at it via `@DynamicPropertySource`, and assert the outgoing request with `verify`. For pure Spring `RestClient`/`RestTemplate` slices where I don't need a real socket, I use `@RestClientTest` with `MockRestServiceServer`, which intercepts the transport in memory and is faster. WireMock's scenarios are great for simulating intermittent failures, so I can prove my retry logic actually recovers after a `503`.

### Vocabulário

| Termo (EN) | Significado |
| --- | --- |
| stub | resposta pré-programada que o servidor de mentira devolve pra uma requisição que casa |
| to verify a request | afirmar que a chamada saiu com a URL/método/headers esperados |
| dynamic port | porta atribuída em runtime, evita colisão no CI e em paralelo |
| scenario / state transition | mecanismo do WireMock pra mesma URL responder diferente a cada chamada (retry) |
| transport-level mock | ponto de corte no HTTP, abaixo do código do client (não no client em si) |
| test slice | fatia mínima do contexto Spring carregada pelo teste (ex.: `@RestClientTest`) |
| flaky test | teste que passa/falha de forma não-determinística (ex.: depender da API real) |

## Veja também

- [[03-Dominios/Tecnologia/Java/Testes/09 - @WebMvcTest — testando controllers com MockMvc|@WebMvcTest]]
- [[03-Dominios/Tecnologia/Java/Testes/12 - Testes de integração ponta a ponta|Testes de integração ponta a ponta]]
- [[03-Dominios/Tecnologia/Java/Web e APIs REST/15 - Clientes HTTP — RestClient, WebClient, RestTemplate|Clientes HTTP — RestClient, WebClient, RestTemplate]]
- [[03-Dominios/Tecnologia/Java/Testes/index|Testes (MOC do galho)]]
- [[03-Dominios/Tecnologia/Java/index|Trilha Java]]
- [[03-Dominios/Tecnologia/Java/Dicionário de Java]] (verbetes WireMock / MockRestServiceServer)

## Referências

- WireMock — Documentation: https://wiremock.org/docs/
- WireMock — Stateful Behaviour (scenarios): https://wiremock.org/docs/stateful-behaviour/
- Spring Boot — Testing Spring Boot Applications: https://docs.spring.io/spring-boot/reference/testing/spring-boot-applications.html
- Spring Framework — Integration Testing (MockRestServiceServer / Client-side REST tests): https://docs.spring.io/spring-framework/reference/testing/integration.html
