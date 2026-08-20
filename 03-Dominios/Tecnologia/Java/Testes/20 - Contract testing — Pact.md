---
title: "Contract testing — Pact"
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
  - pact
aliases:
  - "Pact"
  - "contract testing"
  - "consumer-driven contract"
---

# Contract testing — Pact

> [!abstract] TL;DR
> Testes E2E entre serviços são frágeis e lentos: pra verificar que dois serviços se entendem você precisa subir os dois (mais banco, fila, rede) e torcer pra nada estar fora do ar. O **contract testing** com Pact inverte essa lógica: o **consumer** declara o que espera da API do producer e gera um arquivo de contrato (o *pact*); o **producer** verifica que cumpre esse contrato dentro do próprio build. Uma quebra de compatibilidade falha **antes do merge**, sem precisar orquestrar os dois serviços rodando juntos.

## O que é

Contract testing é uma técnica pra testar a **integração entre dois serviços** verificando, de cada lado e isoladamente, que ambos respeitam um **contrato** compartilhado — sem nunca rodar os dois ao mesmo tempo.

[Pact](https://docs.pact.io/) é a ferramenta mais difundida pra fazer isso no estilo **consumer-driven** (dirigido pelo consumidor). A ideia central:

- O **consumer** é quem *consome* a API (o cliente HTTP).
- O **producer** (ou **provider**) é quem *expõe* a API (o servidor).
- O contrato não é escrito à mão nem negociado em reunião: ele é **gerado a partir dos testes do consumer**. Cada interação que o consumer declara vira um exemplo concreto de request esperado e response esperado.

O resultado é um arquivo JSON — o *pact* — que descreve, em linguagem de máquina, exatamente o que o consumer precisa do producer. A documentação chama isso de *"contract by example"*: o contrato captura só o que o consumer realmente usa, não tudo o que a API teoricamente oferece.

> [!info] Consumer-driven, não provider-driven
> Existem outras famílias de contract testing (ex.: schema-first, OpenAPI). O diferencial do Pact é que **o consumer dirige**: o contrato nasce das expectativas reais de quem consome, não de uma especificação que o producer publica e torce pra alguém seguir.

## Por que importa

Numa arquitetura distribuída (vários serviços conversando por HTTP), a pergunta mais cara de responder é: *"se eu mudar a resposta deste endpoint, quebro quem depende dele?"*

Sem contract testing, as respostas usuais são ruins:

- **Testes E2E**: sobem o sistema inteiro. Lentos, instáveis (*flaky*), caros de manter, e quando quebram raramente apontam a causa.
- **Confiar na documentação**: a doc envelhece, ninguém garante que o código a segue.
- **Descobrir em produção**: o pior cenário — o consumer quebra quando o producer faz deploy.

Contract testing dá a garantia que importa — *"esses dois serviços vão se entender"* — com testes **rápidos, determinísticos e que rodam no build de cada lado**. A documentação do Pact resume o ganho: você consegue *"confirmar com segurança que suas aplicações vão funcionar juntas sem precisar fazer deploy do mundo inteiro primeiro"*.

E há um benefício político subestimado: o contrato vira um **artefato de comunicação entre times**. Quando o time do `order-service` quer mudar um campo, ele vê na verificação do contrato quais consumers dependem daquele campo — a conversa acontece no build, não no incidente.

## Como funciona

### O problema: E2E entre serviços é frágil e lento

Imagine um `billing-service` (consumer) que chama o `order-service` (producer) pra buscar os detalhes de um pedido antes de faturar. Pra testar essa integração de ponta a ponta você precisaria:

1. Subir o `order-service` real (com seu banco, suas dependências).
2. Subir o `billing-service`.
3. Colocar dados consistentes nos dois.
4. Fazer a chamada e validar.

Cada passo é um ponto de falha. O teste fica lento, depende de rede, e quando falha você não sabe se foi bug, dado faltando ou um serviço fora do ar. Pior: esse teste só pode rodar num ambiente onde **os dois serviços coexistem** — o que normalmente é tarde demais no pipeline.

Contract testing remove a coexistência. Cada lado testa contra um **substituto** do outro: o consumer testa contra um mock; o producer testa contra um arquivo.

### Consumer declara expectativas e gera o pact (@Pact)

No lado do consumer, o teste descreve a interação esperada e roda contra um **mock server** que o Pact levanta. Com JUnit 5, o esqueleto é:

- `@ExtendWith(PactConsumerTestExt.class)` — ativa a extensão do Pact.
- `@Pact(consumer = "...", provider = "...")` — método que constrói a interação via `PactDslWithProvider` (DSL fluente: `given` / `uponReceiving` / `path` / `method` / `willRespondWith`).
- `@PactTestFor(...)` — amarra o teste ao provider e injeta o `MockServer`.

Quando o teste passa, o Pact **escreve o arquivo de contrato** (por padrão em `target/pacts/`). Esse JSON é o pact: a lista de interações que o `billing-service` precisa que o `order-service` cumpra.

> [!tip] O contrato é um subproduto, não um documento
> Você não "escreve o pact". Você escreve um teste de consumer honesto, e o pact cai como output. Isso garante que o contrato nunca diverge do que o consumer de fato faz.

### Producer verifica que cumpre o contrato (@Provider / @State)

No lado do producer, o teste **lê o pact gerado** e dispara cada interação contra o serviço real (ou contra o controller, dependendo do alvo configurado). Anotações principais:

- `@Provider("order-service")` — nome do producer (precisa bater com o `provider` do pact).
- `@PactFolder("pacts")` — onde estão os arquivos de contrato.
- `@State("...")` — prepara o estado que aquela interação assume (ex.: "existe um pedido com id 42"). O `given(...)` do consumer aponta pra esse estado.
- `@TestTemplate` + `@ExtendWith(PactVerificationInvocationContextProvider.class)` — gera **um teste por interação** encontrada nos pacts.

O `PactVerificationContext` executa a verificação chamando `context.verifyInteraction()`. Se a resposta real do producer divergir do que o pact espera (campo faltando, status errado, tipo trocado), o teste falha.

> [!note] Por que `@State` existe
> Muitas interações só fazem sentido sob uma precondição: "buscar o pedido 42" pressupõe que o pedido 42 exista. O consumer expressa isso com `given("existe um pedido com id 42")`; o producer recebe esse mesmo texto em `@State` e prepara o cenário (popula banco, ajusta um stub interno) antes de a interação ser disparada. Sem esse handshake, o producer responderia 404 e a verificação falharia por um motivo artificial — estado faltando, não contrato violado.

### Quebra de contrato falha no build (sem rodar os 2 serviços juntos)

Esse é o coração do mecanismo. Repare que em **nenhum momento** os dois serviços rodaram juntos:

- O consumer testou contra um **mock** (Pact mock server).
- O producer testou contra um **arquivo** (o pact em disco).

Se o time do `order-service` remove um campo que o `billing-service` usa, a verificação do producer **falha no build do `order-service`** — porque o pact ainda exige aquele campo. A incompatibilidade é detectada cedo, no lugar certo, sem ambiente E2E.

> [!warning] O elo: o pact precisa chegar do consumer ao producer
> Em projetos sérios o transporte do arquivo não é manual. Usa-se um **Pact Broker** (ou Pactflow) pra publicar pacts do consumer e o producer baixar a versão certa, com versionamento por branch/tag. O `@PactFolder` mostrado aqui é o atalho didático (arquivo em disco); a orquestração distribuída do broker entre times conversa com o galho [[03-Dominios/Tecnologia/Java/Microservices e sistemas distribuídos/index|Microservices e sistemas distribuídos]].

## Na prática

Consumer (`billing-service`) declarando o que espera do `order-service` e gerando o pact:

```java
@ExtendWith(PactConsumerTestExt.class)
@PactTestFor(providerName = "order-service")
class OrderClientPactTest {

    @Pact(consumer = "billing-service", provider = "order-service")
    RequestResponsePact pactExisteUmPedido(PactDslWithProvider builder) {
        return builder
            .given("existe um pedido com id 42")          // vira o @State no producer
            .uponReceiving("buscar detalhes do pedido 42")
            .path("/orders/42")
            .method("GET")
            .willRespondWith()
            .status(200)
            .headers(Map.of("Content-Type", "application/json"))
            // declare SÓ o que o billing-service realmente usa
            .body(new PactDslJsonBody()
                .integerType("id", 42)
                .decimalType("total", 199.90)
                .stringType("status", "CONFIRMED"))
            .toPact();
    }

    @Test
    @PactTestFor(pactMethod = "pactExisteUmPedido")
    void buscaPedidoEMapeiaTotal(MockServer mockServer) throws IOException {
        // 'order' aponta para o MockServer do Pact, não para o serviço real
        var client = new OrderClient(mockServer.getUrl());

        Order order = client.findById(42);

        assertThat(order.total()).isEqualByComparingTo("199.90");
        assertThat(order.status()).isEqualTo("CONFIRMED");
    }
}
```

Producer (`order-service`) verificando que cumpre o pact gerado:

```java
@Provider("order-service")
@PactFolder("pacts")            // ou @PactBroker(...) num setup com broker
class OrderServiceContractTest {

    @LocalServerPort
    int port;

    @BeforeEach
    void setTarget(PactVerificationContext context) {
        context.setTarget(new HttpTestTarget("localhost", port));
    }

    @State("existe um pedido com id 42")
    void prepararPedido42() {
        // popula o estado que a interação do consumer assume
        orderRepository.save(new Order(42L, new BigDecimal("199.90"), "CONFIRMED"));
    }

    @TestTemplate
    @ExtendWith(PactVerificationInvocationContextProvider.class)
    void verificarContrato(PactVerificationContext context) {
        context.verifyInteraction();   // um teste por interação no pact
    }
}
```

A simetria é o ponto: o `given(...)` do consumer e o `@State(...)` do producer são o mesmo texto, e é isso que costura os dois lados sem nunca subir os dois serviços ao mesmo tempo.

## Armadilhas

### (1) Contrato acoplado a detalhe de implementação

**Problema**: declarar no pact campos que o consumer não usa, ou casar valores exatos onde só o tipo importa. O contrato passa a quebrar a cada mudança cosmética do producer.

**Exemplo**: o `billing-service` só precisa de `id`, `total` e `status`, mas o teste declara o JSON inteiro do pedido (`createdAt`, `customerName`, `items[]`...) com `stringValue("status", "CONFIRMED")` casando o valor literal. Aí o producer muda o formato de `createdAt` — um campo que o billing nem lê — e a verificação falha.

**Fix**: declare **só o que o consumer realmente consome**, e prefira *matchers de tipo* (`integerType`, `stringType`, `decimalType`) a valores literais. O contrato deve afirmar "espero um inteiro chamado `id`", não "espero exatamente `42`". O contrato é sobre **forma**, não sobre dado.

### (2) Producer que não roda a verificação no CI

**Problema**: o consumer gera o pact, mas o teste de verificação do producer não está na suíte do build. O contrato vira **mentira documentada**: existe um arquivo, mas ninguém garante que o producer o cumpre.

**Exemplo**: o `OrderServiceContractTest` está marcado como `@Disabled` "porque estava quebrando", ou roda só num módulo que o CI não executa. O producer remove um campo, o build passa verde, e o `billing-service` quebra em produção.

**Fix**: a verificação do producer tem que ser **parte obrigatória do build do producer** (`mvn verify` / `gradle check`), falhando o pipeline quando o contrato é violado. Um contrato que não é verificado no CI não é um contrato — é um comentário.

### (3) Usar Pact onde um teste de integração simples bastava

**Problema**: aplicar Pact pra toda chamada HTTP, inclusive contra APIs de terceiros que você não controla ou contra um stub que o próprio time mantém. Vira cerimônia: dois lados, broker, estados — pra um caso que um stub HTTP resolveria.

**Exemplo**: criar contrato Pact pra consumir uma API pública de terceiros. Você não controla o producer, não há como rodar a verificação do lado deles, então o "contrato" nunca é verificado — é só um mock disfarçado.

**Fix**: Pact rende quando há **dois serviços sob controle de times diferentes** (ou do mesmo time) que precisam evoluir independentemente. Pra API externa que você só consome, prefira mockar o HTTP com WireMock; pra colaboração interna entre camadas, um teste de integração direto basta. Use a ferramenta certa: contract testing é pra **fronteiras entre serviços que se versionam**.

## Em entrevista

### Frase pronta (inglês)

> End-to-end tests across services are slow and flaky because they require deploying both services together just to confirm they agree on an API. Pact flips this with consumer-driven contract testing: the consumer declares exactly what it expects and generates a contract — the pact — while testing against a mock; the provider then verifies it satisfies that pact within its own build, against the file rather than a live consumer. A breaking change fails the provider's build before merge, so we catch incompatibilities early, in the right place, without ever orchestrating both services in the same environment.

### Vocabulário

| Termo (EN) | Tradução / sentido |
| --- | --- |
| consumer-driven contract | contrato dirigido pelo consumidor |
| consumer / provider | quem consome a API / quem a expõe |
| pact (contract file) | arquivo de contrato gerado pelo consumer |
| contract by example | contrato derivado de exemplos reais de uso |
| provider verification | verificação de que o producer cumpre o pact |
| provider state | estado que uma interação assume (`@State` / `given`) |
| Pact Broker | repositório que distribui pacts entre times |
| flaky test | teste instável, que falha de forma intermitente |

## Veja também

- [[03-Dominios/Tecnologia/Java/Testes/19 - Fitness functions — ArchUnit (testes de arquitetura)|Fitness functions — ArchUnit]]
- [[03-Dominios/Tecnologia/Java/Testes/16 - Mockando HTTP externo — WireMock e MockRestServiceServer|Mockando HTTP externo]]
- [[03-Dominios/Tecnologia/Java/Testes/21 - Capstone — a estratégia de testes de uma app Spring production-grade|Capstone de testes]]
- [[03-Dominios/Tecnologia/Java/Testes/index|Testes (MOC do galho)]]
- [[03-Dominios/Tecnologia/Java/index|Trilha Java]]
- [[03-Dominios/Tecnologia/Java/Dicionário de Java]]

## Referências

- [Pact — documentação oficial](https://docs.pact.io/)
- [Pact JVM — implementation guide](https://docs.pact.io/implementation_guides/jvm)
- [Pact JVM — consumer JUnit5](https://docs.pact.io/implementation_guides/jvm/consumer/junit5)
- [Pact JVM — provider JUnit5](https://docs.pact.io/implementation_guides/jvm/provider/junit5)
