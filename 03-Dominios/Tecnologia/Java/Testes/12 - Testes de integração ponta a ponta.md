---
title: "Testes de integração ponta a ponta"
created: 2026-06-11
updated: 2026-06-11
type: concept
progress: backlog
status: seedling
publish: true
fase: adepto
tags:
  - java
  - testes
  - adepto
  - integracao
  - testcontainers
aliases:
  - "testes de integração"
  - "@SpringBootTest integração"
---

# Testes de integração ponta a ponta

> [!abstract] TL;DR
> `@SpringBootTest` sobe o **contexto completo** da aplicação e, combinado com Testcontainers, testa o **fluxo inteiro** (controller → service → banco real) num único teste. O atributo `webEnvironment` escolhe entre ambiente mockado (`MockMvc`) e servidor real escutando numa porta (`RANDOM_PORT`). É o **topo da pirâmide de slices**: dá a maior confiança, mas é o teste mais lento e mais pesado — use com **parcimônia**.

## O que é

Um teste de integração ponta a ponta (E2E) exercita a aplicação **do jeito que ela roda em produção**, atravessando todas as camadas: a requisição entra pelo controller, passa pelo service, toca o repositório e bate num banco de dados **de verdade** — sem mocks de infraestrutura no meio do caminho.

Em Spring Boot, a porta de entrada para esse tipo de teste é a anotação `@SpringBootTest`. Diferente dos *slices* (`@WebMvcTest`, `@DataJpaTest`), que carregam só uma fatia do contexto, `@SpringBootTest` instancia o `ApplicationContext` **inteiro** — todos os beans, todas as auto-configurations. Quando você o combina com [[03-Dominios/Tecnologia/Java/Testes/11 - Testcontainers — infra real em testes|Testcontainers]], o "banco de verdade" deixa de ser uma ameaça frágil (um Postgres compartilhado no CI) e vira um container Docker efêmero, descartável e idêntico ao de produção.

A pergunta-chave que essa nota responde é: como sobir o contexto completo, ligá-lo a containers reais e escolher o cliente HTTP certo para verificar o fluxo de ponta a ponta.

## Por que importa

Slices testam **unidades de comportamento isoladas**. Mas bugs reais moram nas **costuras**: a serialização JSON que diverge entre o que o controller produz e o que o service espera; a transação que não propaga; o mapeamento JPA que só quebra com o dialeto real do Postgres; o filtro de segurança que muda o status code. Nada disso aparece num teste unitário com mock.

O teste E2E é a sua **rede de segurança final**. Ele responde à pergunta que o cliente faz: *"quando eu mando este POST, o pedido aparece no banco?"*. Nenhuma quantidade de testes unitários verdes garante isso — só o fluxo completo garante.

Há ainda um ganho sutil: o E2E valida a **configuração** da aplicação, não só o código. Um `application.yml` com uma property errada, um bean que falta na auto-configuration, um perfil que não ativa — nada disso quebra um teste unitário, mas tudo isso explode quando você sobe o contexto completo. O E2E é, na prática, o primeiro lugar onde a aplicação "liga inteira" antes do deploy.

O custo é proporcional: subir o contexto inteiro leva segundos, não milissegundos. Por isso a [[03-Dominios/Tecnologia/Java/Testes/21 - Capstone — a estratégia de testes de uma app Spring production-grade|estratégia de testes]] saudável tem **poucos** E2E no topo e **muitos** slices/unit na base. Inverter essa pirâmide é a armadilha número um (veja abaixo).

## Como funciona

### @SpringBootTest: o contexto completo + WebEnvironment (MOCK / RANDOM_PORT / DEFINED_PORT / NONE)

`@SpringBootTest` procura a classe `@SpringBootApplication` (ou `@SpringBootConfiguration`) e carrega o contexto completo a partir dela. O comportamento web é controlado pelo atributo `webEnvironment`:

| `WebEnvironment` | Servidor embarcado | Para que serve |
|---|---|---|
| **`MOCK`** (default) | **Não** sobe | Ambiente web *mockado*; combine com `@AutoConfigureMockMvc` ou `@AutoConfigureWebTestClient` |
| **`RANDOM_PORT`** | **Sobe**, porta aleatória | Servidor real; cliente HTTP de verdade (`TestRestTemplate`/`WebTestClient`) |
| **`DEFINED_PORT`** | **Sobe**, porta fixa | Servidor real na porta de `application.properties` (ou `8080`) |
| **`NONE`** | Não sobe | Sem ambiente web nenhum (testes de service/batch/scheduler) |

O `MOCK` é o default: ele cria um `WebApplicationContext` mas **não inicia o Tomcat**. Você fala com os endpoints através de uma camada mockada via `@AutoConfigureMockMvc` — é rápido, mas não exercita a stack de rede real (conexão TCP, serialização do servlet container).

Para um E2E "de verdade", `RANDOM_PORT` é a escolha canônica: sobe um Tomcat real numa porta aleatória (evitando colisão no CI) e você injeta a porta com `@LocalServerPort` ou usa um cliente que já a conhece.

Um detalhe que pega muita gente: subir o contexto inteiro é **caro**, mas o Spring **cacheia** contextos entre classes de teste. Se duas classes usam a *mesma* configuração (mesmas anotações, mesmos `@DynamicPropertySource`, mesmos `@MockBean`), o contexto é reaproveitado — não sobe de novo. Por isso vale padronizar as classes E2E em torno de uma **classe-base comum**: além de centralizar os containers, você maximiza o cache e a suíte inteira sobe o contexto uma vez só, não uma vez por classe.

> [!warning] Cuidado com `@Transactional` + servidor real
> Quando o teste é `@Transactional`, o Spring faz rollback ao fim de cada método. Mas com `RANDOM_PORT`/`DEFINED_PORT` o cliente HTTP e o servidor rodam em **threads separadas** — logo, em **transações separadas**. Qualquer transação iniciada no servidor **não** é revertida pelo rollback do teste. É por isso que a Armadilha 2 existe.

### Múltiplos containers (Postgres + Redis + Kafka) num teste

Aplicações reais não dependem só de um banco. Um pedido pode ser **persistido** no Postgres, ter um cache **invalidado** no Redis e disparar um evento no **Kafka**. O teste E2E precisa de todos eles de pé ao mesmo tempo.

Com [[03-Dominios/Tecnologia/Java/Testes/11 - Testcontainers — infra real em testes|Testcontainers]], você declara cada container como um campo `static` na classe de teste (ou numa classe-base compartilhada). O `static` é essencial: garante **um** container por suíte, não um por método — caro demais.

```java
@Container
@ServiceConnection
static PostgreSQLContainer<?> postgres = new PostgreSQLContainer<>("postgres:16-alpine");

@Container
@ServiceConnection
static GenericContainer<?> redis = new GenericContainer<>("redis:7-alpine").withExposedPorts(6379);

@Container
@ServiceConnection
static KafkaContainer kafka = new KafkaContainer(DockerImageName.parse("confluentinc/cp-kafka:7.6.0"));
```

Os três sobem **em paralelo** quando a suíte arranca e ficam de pé durante todos os métodos da classe (graças ao `static`). Cada um custa segundos de startup — outro motivo para concentrar os E2E numa classe-base compartilhada e deixar o cache de contexto do Spring trabalhar.

O desafio é o **wiring**: a aplicação precisa saber em qual host/porta cada container subiu — e isso só é conhecido em runtime, depois do Docker alocar as portas. Há dois mecanismos para isso: `@ServiceConnection` (automático, quando o Spring Boot reconhece o container) e `@DynamicPropertySource` (manual, para o que ele não reconhece). Ambos a seguir.

### MockMvc vs WebTestClient vs TestRestTemplate

Os três são clientes para falar com seus endpoints, mas operam em camadas diferentes:

| Cliente | Sobe servidor? | Estilo | Quando usar |
|---|---|---|---|
| **`MockMvc`** | Não (`MOCK`) | `perform(...).andExpect(...)` (Hamcrest) | Slices de controller; rápido; sem rede real |
| **`TestRestTemplate`** | Sim (`RANDOM_PORT`) | Template imperativo (`getForObject`) | E2E clássico em apps MVC; já trata a base URL |
| **`WebTestClient`** | Sim (ou mockado) | Fluente `get().uri().exchange().expectStatus()` | E2E moderno; obrigatório em apps WebFlux reativas |

Regra prática:

- **`MockMvc`** → quando o `webEnvironment` é `MOCK`. É o cliente do [[03-Dominios/Tecnologia/Java/Testes/09 - @WebMvcTest — testando controllers com MockMvc|@WebMvcTest]] e funciona também com `@SpringBootTest` + `@AutoConfigureMockMvc`. Não há porta nem Tomcat: ele invoca o `DispatcherServlet` diretamente.
- **`TestRestTemplate`** → quando você sobe servidor real (`RANDOM_PORT`) numa app MVC tradicional. É auto-configurado e já conhece a porta aleatória.
- **`WebTestClient`** → o cliente fluente moderno. Funciona contra servidor real **ou** mockado, e é o único que faz sentido numa stack reativa (WebFlux). É a escolha preferida para código novo.

### @DynamicPropertySource: apontar a config pros containers

Para containers que o Spring Boot **não** reconhece automaticamente, você usa `@DynamicPropertySource`: um método `static` que recebe um `DynamicPropertyRegistry` e registra propriedades **calculadas em runtime**, depois que os containers já têm host/porta.

```java
@DynamicPropertySource
static void registerProps(DynamicPropertyRegistry registry) {
    registry.add("spring.data.redis.host", redis::getHost);
    registry.add("spring.data.redis.port", () -> redis.getMappedPort(6379));
}
```

Repare que os valores são `Supplier<>` (lambdas/method references), não strings literais — porque a porta só existe **depois** que o container subiu, e o registry é avaliado tarde o suficiente.

A alternativa mais nova e enxuta é `@ServiceConnection`: para containers conhecidos (Postgres, MongoDB, Redis, Kafka...), o Spring Boot detecta o tipo e **liga sozinho** todas as propriedades de conexão — sem você escrever uma linha de `@DynamicPropertySource`. Use `@ServiceConnection` quando der; caia para `@DynamicPropertySource` no que sobrar.

Pense nos dois como camadas de um mesmo problema — "como a aplicação descobre onde o container está?":

- `@ServiceConnection` é **declarativo e tipado**: você anota o container e o Spring Boot resolve as propriedades certas pelo tipo dele. Menos código, menos chance de errar o nome da property.
- `@DynamicPropertySource` é o **escape hatch genérico**: registra qualquer propriedade arbitrária via lambda. Indispensável para um `GenericContainer` de uma tecnologia que o Boot não conhece (um serviço HTTP customizado, um mock server, uma flag derivada da URL do container).

Na dúvida, comece com `@ServiceConnection`. Se a property que você precisa não for ligada automaticamente, complemente com um `@DynamicPropertySource` para os ajustes finos.

## Na prática

Um E2E real: servidor de verdade (`RANDOM_PORT`), Postgres + Redis via `@ServiceConnection`, e um fluxo completo — `POST` cria um `Order` pelo controller e o teste confirma a persistência consultando o `OrderRepository` direto.

```java
@SpringBootTest(webEnvironment = WebEnvironment.RANDOM_PORT)
@Testcontainers
class OrderEndToEndTest {

    @Container
    @ServiceConnection
    static PostgreSQLContainer<?> postgres =
            new PostgreSQLContainer<>("postgres:16-alpine");

    @Container
    @ServiceConnection
    static GenericContainer<?> redis =
            new GenericContainer<>("redis:7-alpine").withExposedPorts(6379);

    @Autowired
    private TestRestTemplate restTemplate;

    @Autowired
    private OrderRepository orderRepository;

    @BeforeEach
    void cleanState() {
        // @SpringBootTest NÃO faz rollback automático aqui — limpamos à mão.
        orderRepository.deleteAll();
    }

    @Test
    void postCreatesOrderAndPersistsItToTheRealDatabase() {
        var request = new CreateOrderRequest("SKU-42", 3, "alice@example.com");

        ResponseEntity<OrderResponse> response =
                restTemplate.postForEntity("/api/orders", request, OrderResponse.class);

        // 1. A resposta HTTP veio do servidor real
        assertThat(response.getStatusCode()).isEqualTo(HttpStatus.CREATED);
        assertThat(response.getBody()).isNotNull();
        Long createdId = response.getBody().id();

        // 2. O fluxo atravessou controller → service → banco real
        Optional<Order> persisted = orderRepository.findById(createdId);
        assertThat(persisted).isPresent();
        assertThat(persisted.get().getSku()).isEqualTo("SKU-42");
        assertThat(persisted.get().getQuantity()).isEqualTo(3);
    }
}
```

Note os pilares: `RANDOM_PORT` (servidor real) + dois containers com `@ServiceConnection` (zero `@DynamicPropertySource` porque ambos são reconhecidos) + `TestRestTemplate` (conhece a porta sozinho) + verificação **dupla** (resposta HTTP **e** estado no banco). O `@BeforeEach` limpando o estado não é opcional — é a defesa contra a Armadilha 2.

## Armadilhas

### (1) Integração demais — a pirâmide invertida

`@SpringBootTest` é viciante: sobe tudo, "testa de verdade", parece o teste definitivo. O resultado é uma suíte onde **quase todo** teste é E2E. A suíte então leva minutos (cada um sobe o contexto + containers), o feedback fica lento e os devs param de rodar os testes localmente.

```text
   /\        Anti-padrão: poucos unit, muitos @SpringBootTest
  /  \       → suíte de 8 minutos, ninguém roda local
 /----\
/      \  ← deveria ser a base larga, mas está vazia
```

**Fix:** mantenha a pirâmide na orientação certa. A **base** são testes de unidade (service com mocks) e [[03-Dominios/Tecnologia/Java/Testes/09 - @WebMvcTest — testando controllers com MockMvc|slices]] (`@WebMvcTest`, `@DataJpaTest`) — rápidos, focados. O **topo** são uns poucos E2E cobrindo os caminhos felizes críticos de ponta a ponta. Pergunte-se: *"isto pode ser um slice?"* Quase sempre pode.

### (2) Estado vazando entre testes

Aqui mora o bug mais traiçoeiro. Diferente de `@DataJpaTest`, que é `@Transactional` e faz **rollback automático** ao fim de cada método, `@SpringBootTest` com servidor real **não** reverte nada — o cliente HTTP e o servidor rodam em threads/transações separadas, então o rollback do teste não alcança o que o servidor gravou.

```java
@Test
void firstTest() {
    restTemplate.postForEntity("/api/orders", req, OrderResponse.class);
    // Order fica no banco DEPOIS do teste...
}

@Test
void secondTest() {
    // ...e o segundo teste enxerga o lixo do primeiro. Falha intermitente.
    assertThat(orderRepository.count()).isZero(); // FALHA
}
```

**Fix:** limpe o estado **explicitamente** entre testes. Um `@BeforeEach` com `repository.deleteAll()` (como no exemplo) ou `@Sql(scripts = "/cleanup.sql")` resolvem. Não confie em rollback que não vai acontecer.

### (3) `DEFINED_PORT` colidindo no CI

Usar `webEnvironment = DEFINED_PORT` fixa a porta (a de `application.properties` ou `8080`). Em CI, várias suítes podem rodar em paralelo, ou a porta já está ocupada por outro processo — e o teste morre com `Port already in use` de forma intermitente, sem relação com o código.

```java
@SpringBootTest(webEnvironment = WebEnvironment.DEFINED_PORT) // 8080 fixo → colide
```

**Fix:** use `RANDOM_PORT`. Cada execução escolhe uma porta livre; os clientes auto-configurados (`TestRestTemplate`, `WebTestClient`) e `@LocalServerPort` descobrem a porta sozinhos. Reserve `DEFINED_PORT` para o raríssimo caso em que algo externo *precisa* de uma porta fixa conhecida.

Vale lembrar: com `RANDOM_PORT` o servidor de **management** (Actuator) também sobe numa porta aleatória separada, se a sua app o configura numa porta própria. Não chute a URL do Actuator no teste — leia-a da mesma fonte que o Spring expõe, ou o teste vira frágil de novo.

## Em entrevista

### Frase pronta (inglês)

> "For end-to-end integration tests I reach for `@SpringBootTest` with `webEnvironment = RANDOM_PORT`, which boots the full application context and a real embedded server on a random port to avoid CI collisions. I back it with Testcontainers so the test hits a real Postgres and Redis instead of an in-memory substitute — wiring them through `@ServiceConnection`, or `@DynamicPropertySource` for anything Spring Boot doesn't auto-detect. The key discipline is keeping these at the top of the pyramid: they're slow and they don't roll back automatically like `@DataJpaTest`, so I clean state explicitly between tests and lean on slices for everything else."

### Vocabulário

| Termo (EN) | Tradução / nota |
|---|---|
| full application context | contexto completo da aplicação |
| embedded server | servidor embarcado (Tomcat) |
| random port | porta aleatória (`RANDOM_PORT`, evita colisão no CI) |
| service connection | ligação automática de container a propriedades de conexão |
| dynamic property source | registro de propriedades em runtime |
| test pyramid | pirâmide de testes (base larga de unit, topo fino de E2E) |
| state leakage | vazamento de estado entre testes |
| rollback | reversão de transação ao fim do teste |

## Veja também

- [[03-Dominios/Tecnologia/Java/Testes/11 - Testcontainers — infra real em testes|Testcontainers]]
- [[03-Dominios/Tecnologia/Java/Testes/09 - @WebMvcTest — testando controllers com MockMvc|@WebMvcTest]]
- [[03-Dominios/Tecnologia/Java/Testes/21 - Capstone — a estratégia de testes de uma app Spring production-grade|Capstone de testes]]
- [[03-Dominios/Tecnologia/Java/Testes/index|Testes (MOC do galho)]]
- [[03-Dominios/Tecnologia/Java/index|Trilha Java]]
- [[03-Dominios/Tecnologia/Java/Dicionário de Java]]

## Referências

- Spring Boot Reference — Testing Spring Boot Applications: https://docs.spring.io/spring-boot/reference/testing/spring-boot-applications.html
