---
title: "Spec — Galho 13 da trilha Java Senior (Testes)"
date: 2026-06-11
author: Josenaldo
status: draft
type: spec
publish: false
---

# Spec — Galho 13 da trilha Java Senior (Testes)

## 1. Contexto e motivação

Este é o **décimo terceiro galho** da trilha Java Senior (roadmap em `docs/superpowers/specs/2026-06-02-java-senior-roadmap-design.md`, §5, bloco "Fundamentos enterprise e Spring", linha 158). Pressupõe leitura do roadmap, que estabelece topologia flat, esquema de 3 fases, padrões editoriais e política de poda. Os Galhos 1 a 12 já fecharam em `main` — seus artefatos são o **template de padrão e qualidade** deste galho. As dependências diretas são os **Galhos 1 e 8** (linha 160 do roadmap): o Galho 1 é a linguagem (exceções pro `assertThrows`, records/lambdas nos testes); o Galho 8 é o **container** (os slices do Spring carregam um `ApplicationContext` parcial).

**Galho HÍBRIDO: REFATOR (poda INTEGRAL de tronco monolítico) + PESQUISA.** Como os Galhos 10 e 12, poda **um único** tronco de forma integral (padrão JavaFX/Galho 6):

- **Parte REFATOR (poda integral):** `Backend/Testes em Java.md` (1616 linhas, `publish: false`, `status: evergreen`) é o **tronco dedicado deste galho**. Cobre **todo** o escopo do roadmap (JUnit 5, AssertJ, Mockito, Spring Boot Test e slices, Testcontainers, integração, contract testing, estratégia/pirâmide) **e mais** (WireMock, Awaitility, ArchUnit, PIT mutation testing, JMH, test data builders, Clock/time), de forma densa e monolítica. **Poda INTEGRAL** (padrão JavaFX/Galho 10/12): o tronco encolhe a um hub de ~20 linhas — frontmatter (`publish: false`), H1, 1-2 frases de intro e um único callout `[!nota] Migrado para galho próprio`. **Toda a fabricação evapora** com a poda (o tronco tem `Patient`/`PatientService`/`PatientRepository`/`PatientController`/`Maria`/`maria@example.com`/`PatientBuilder`/`PatientAssert`, a seção `## Na prática (da minha experiência)` ~1483 com a "evolução da stack de testes do MedEspecialista" — JUnit4→5, H2→Testcontainers, incidente de flakiness no Kafka, mutation testing rodado uma vez —, e `## How to explain in English` em 1ª pessoa ~1516 + `### Frases úteis` — **contraexemplo, jamais copiar pras notas**).

- **Parte PESQUISA:** mesmo o tronco sendo rico, várias afirmações são **version-specific** e exigem confirmação via WebFetch (ZERO memória): versão atual do **JUnit 5** e do **Mockito 5**; **`@MockitoBean` (Spring Boot 3.4+) substituiu `@MockBean`** (deprecated); **`@ServiceConnection` (Spring Boot 3.1+)**; static mocking nativo do Mockito 5 (sem PowerMock); Testcontainers atual; AssertJ atual; ArchUnit, PIT e JMH atuais. Fonte: `junit.org/junit5/docs/current/user-guide/`, `javadoc.io/doc/org.mockito`, `docs.spring.io/spring-boot/...testing`, `java.testcontainers.org`, `assertj.github.io`, `pitest.org`, `archunit.org`, `docs.pact.io`.

**A fronteira-assinatura é MÚLTIPLA — este é o galho de CONVERGÊNCIA.** Testes é a camada que **testa o que os Galhos 1-12 construíram**. Cada técnica de teste linka de volta ao galho da coisa testada, sem re-explicá-la:

- **Galho 9 (a camada web testada):** `@WebMvcTest` + `MockMvc` exercitam controllers/`@ControllerAdvice`/serialização → [[03-Dominios/Tecnologia/Java/Web e APIs REST/02 - @RestController e os mapeamentos|@RestController]], [[03-Dominios/Tecnologia/Java/Web e APIs REST/06 - O pipeline do DispatcherServlet|DispatcherServlet]], [[03-Dominios/Tecnologia/Java/Web e APIs REST/09 - Tratamento de exceções com @ControllerAdvice|@ControllerAdvice]]. WireMock/`@RestClientTest` testam os clientes HTTP → [[03-Dominios/Tecnologia/Java/Web e APIs REST/15 - Clientes HTTP — RestClient, WebClient, RestTemplate|Clientes HTTP]].
- **Galho 10 (a persistência testada):** `@DataJpaTest` + `TestEntityManager` + Testcontainers testam repositories/queries → [[03-Dominios/Tecnologia/Java/Persistência de dados/04 - Spring Data repositories — JpaRepository e query methods derivados|Spring Data repositories]], [[03-Dominios/Tecnologia/Java/Persistência de dados/09 - Consultas com @Query — JPQL, native e @Modifying|Consultas com @Query]]. **Paga a dívida** que o Galho 10 deixou ("testes de repositório com Testcontainers/`@DataJpaTest` = Galho 13").
- **Galho 11 (o reativo testado):** `StepVerifier` + `@WebFluxTest` + `WebTestClient` testam Mono/Flux → [[03-Dominios/Tecnologia/Java/Programação Reativa/10 - Spring WebFlux — o stack não-bloqueante sobre Netty e o DispatcherHandler|Spring WebFlux]]. **Paga a dívida** que o Galho 11 deixou explícita (`index:35` "testes reativos com `StepVerifier` = Galho 13").
- **Galho 12 (a segurança testada):** `@WithMockUser`/`with(jwt())`/`with(csrf())` no MockMvc testam authn/authz → [[03-Dominios/Tecnologia/Java/Segurança/05 - Autorização baseada em URL — authorizeHttpRequests, roles vs authorities|Autorização baseada em URL]], [[03-Dominios/Tecnologia/Java/Segurança/07 - Method security — @PreAuthorize, @PostAuthorize e SpEL|Method security]]. **Paga a dívida** da nota 18 do Galho 12 ("a stack de teste = Galho 13").
- **Galho 8 (o container que os slices carregam):** o contexto de teste É um `ApplicationContext`; os slices auto-configuram um subconjunto → [[03-Dominios/Tecnologia/Java/Spring Core e Boot/06 - ApplicationContext — o container e seu ciclo|ApplicationContext]], [[03-Dominios/Tecnologia/Java/Spring Core e Boot/15 - Auto-configuration e starters|Auto-configuration e starters]].
- **Galho 4 (a concorrência testada):** Awaitility testa consistência eventual/código assíncrono → [[03-Dominios/Tecnologia/Java/Concorrência e paralelismo/index|Concorrência e paralelismo]].
- **Galho 3 (a performance medida):** JMH lida com warmup/JIT/dead-code elimination → [[03-Dominios/Tecnologia/Java/JVM/07 - O compilador JIT — C1, C2 e a compilação adaptativa|O compilador JIT]] (por que microbenchmark ingênuo mente).
- **Galho 1 (a linguagem):** `assertThrows`/`assertThatThrownBy` testam o contrato de exceção → [[03-Dominios/Tecnologia/Java/Linguagem e sintaxe moderna/10 - Exceções e tratamento de erros|Exceções e tratamento de erros]].

Os Galhos 10, 11 e 12 deixaram **ganchos "Galho 13 (planejado)"** em texto esperando exatamente essas notas (dívida reversa — §3.6). Este galho **quita** essa dívida.

Testes é a **disciplina que sustenta os 12 galhos anteriores**: como testar a linguagem (JUnit 5/AssertJ), os colaboradores (Mockito), cada camada Spring isoladamente (slices) e em conjunto (integração com Testcontainers), e como ir além do verde/vermelho (mutation testing, performance, fitness functions, contratos). Depende dos Galhos 1 (linguagem) e 8 (container), e linka de volta a praticamente todos.

## 2. Objetivo

Produzir, em uma sessão de execução dedicada, **21 notas atômicas + 1 MOC do galho + expansão do Dicionário de Java + ativação do MOC central + poda INTEGRAL do tronco `Testes em Java.md` + quitação da dívida reversa**, em `03-Dominios/Tecnologia/Java/Testes/` e `03-Dominios/Tecnologia/Java/`, todas `publish: true`, em PT-BR, distribuídas em 3 fases (**5 Iniciado + 7 Adepto + 9 Magus**).

Ao terminar o galho, o leitor deve conseguir:

- **Explicar em inglês** a pirâmide de testes (muitos unit, alguns integration, poucos E2E), o stack moderno (JUnit 5/AssertJ/Mockito/Testcontainers/Spring Boot Test) e quando usar cada slice (`@WebMvcTest`/`@DataJpaTest`/`@SpringBootTest`).
- **Reconhecer o que cada teste testa de qual galho**: `@WebMvcTest`↔controllers (G9), `@DataJpaTest`↔repositories (G10), `@WebFluxTest`/StepVerifier↔reativo (G11), `@WithMockUser`↔segurança (G12), slices↔container (G8).
- **Projetar uma suíte de testes production-grade**: unit tests sem Spring (`new Service(mockRepo)`), slices pra camadas isoladas, integração com Testcontainers (não H2), AssertJ pra asserções legíveis, mocks só do que importa, Awaitility no lugar de `Thread.sleep`, e fitness functions (ArchUnit) como guardrail.
- **Ir além da cobertura de linha**: mutation testing (PIT) pra validar que os testes pegam bugs, JMH pra medir performance corretamente, Pact pra contratos entre serviços.
- **Diagnosticar armadilhas clássicas**: H2 em vez de Testcontainers (falso-positivo de dialeto SQL), mockar demais, `Thread.sleep` (flakiness), testes dependentes de ordem, `@SpringBootTest` pra teste unitário, testar implementação (`verify(times(3))`) em vez de comportamento, line coverage como meta.

A barra é "projetar e justificar uma suíte de testes que protege o stack inteiro, sabendo o que testar em qual nível e com qual ferramenta" — não "escrever uma extension custom do JUnit Platform Launcher".

## 3. Saídas concretas

### 3.1. Notas (`03-Dominios/Tecnologia/Java/Testes/`)

Pasta **nova**, flat. 21 notas + 1 MOC (`index.md`, obrigatório pro folder-link do Quartz). Numeração global por galho (não reinicia por fase).

#### Iniciado (5 notas — vocabulário + JUnit/AssertJ base)

| # | Nota | Escopo nuclear |
|---|------|----------------|
| 01 | O que é testar em Java — a pirâmide e o stack moderno *(opus, assinatura)* | A pirâmide (unit/integration/E2E, não inverter); o stack (JUnit 5/AssertJ/Mockito/Testcontainers/Spring Boot Test — tabela "ferramenta/propósito"); ferramentas deprecated (JUnit 4/Hamcrest/H2/PowerMock). **A nota-assinatura da convergência:** Testes testa os Galhos 1-12 — cada técnica linka de volta ao galho da coisa testada. |
| 02 | JUnit 5 — anatomia, lifecycle e o padrão AAA | Platform/Jupiter/Vintage; `@Test`/`@BeforeEach`/`@AfterEach`/`@BeforeAll`/`@AfterAll`; AAA (given/when/then); `@DisplayName` e convenções de nome; per-method vs per-class (`@TestInstance`); `@Timeout`/`@Disabled`/`@DisabledOnOs`. |
| 03 | AssertJ — fluent assertions | `assertThat(...)` encadeado (strings/numbers/collections/maps/Optional/dates); `extracting`; `assertThatThrownBy`/`catchThrowable`/`assertThatExceptionOfType`; soft assertions; `usingRecursiveComparison().ignoringFields(...)`; por que > JUnit built-in/Hamcrest. |
| 04 | Testes parametrizados e organização | `@ParameterizedTest` + `@ValueSource`/`@CsvSource`/`@MethodSource`/`@EnumSource`/`@CsvFileSource`; `@Nested`; `@Tag` + execução seletiva (Surefire `-Dgroups`); `@ExtendWith` (extensions). |
| 05 | Test data builders e fixtures | O builder/object mother (`aPatient().withName(...).asAdult().build()` → neutro `anOrder()...`); evitar construtores de 15 args e setup duplicado; `@BeforeEach` vs builder; menção a Instancio (geração automática). |

#### Adepto (7 notas — Mockito + slices do Spring)

| # | Nota | Escopo nuclear |
|---|------|----------------|
| 06 | Mockito — mocks, stubbing e matchers *(opus)* | mock vs spy vs fake vs stub; `@Mock`/`@InjectMocks`/`MockitoExtension`; `when(...).thenReturn/thenThrow/thenAnswer`; `doX().when()` pra void; argument matchers (`any`/`eq`/`argThat`/`intThat`) e a regra "todos ou nenhum". |
| 07 | Mockito — verify, ArgumentCaptor e quando NÃO mockar | `verify(...times/never/atLeast/atMost)`, `InOrder`, `verifyNoMoreInteractions`/`verifyNoInteractions`; `ArgumentCaptor`; static mocking (`mockStatic`, Mockito 5+); anti-patterns (mockar value object, testar mocks, verify em tudo); design testável (injetar `Clock`/`Supplier`). |
| 08 | Spring Boot Test e os slices — o contexto de teste | A tabela de slices (`@SpringBootTest`/`@WebMvcTest`/`@DataJpaTest`/`@JsonTest`/`@RestClientTest`/`@WebFluxTest`); `@SpringBootTest` (contexto completo) vs slices (parcial); **caching do contexto de teste** (por que reusar acelera) — liga **G8**; **`@MockitoBean` substituiu `@MockBean`** (WebFetch); `@ActiveProfiles`. |
| 09 | @WebMvcTest — testando controllers com MockMvc *(opus)* | Carrega só a web layer (controllers/advice/filters/converters, **não** services/repos); `MockMvc.perform(...).andExpect(status()/jsonPath())`; `@MockitoBean` no service; testar 200/404/422/validação. Liga **G9** (testa o pipeline do DispatcherServlet). |
| 10 | @DataJpaTest — testando repositories *(opus)* | Carrega só JPA; `TestEntityManager` (persist/flush); transação + rollback automático por teste; `@AutoConfigureTestDatabase(Replace.NONE)` pra usar banco real; testar derived queries/`@Query`. Liga **G10** (paga a dívida de "testes de repositório"). |
| 11 | Testcontainers — infra real em testes | Por que **não H2** (dialeto SQL/JSONB diverge → falso-positivo); `@Container`/`@Testcontainers`; **`@ServiceConnection` (Boot 3.1+, WebFetch)** auto-configura datasource; singleton pattern + `withReuse(true)` (dev local); módulos (Postgres/MySQL/Kafka/Redis/LocalStack). Liga **G10**. |
| 12 | Testes de integração ponta a ponta *(opus)* | `@SpringBootTest(webEnvironment=RANDOM_PORT)` + Testcontainers (múltiplos containers) + `MockMvc`/`WebTestClient`/`TestRestTemplate`; `WebEnvironment` (MOCK/RANDOM_PORT/DEFINED_PORT/NONE); `@DynamicPropertySource`; o teste que atravessa controller→service→banco. |

#### Magus (9 notas — fronteiras, qualidade e arquitetura)

| # | Nota | Escopo nuclear |
|---|------|----------------|
| 13 | Testando a segurança | `@WithMockUser`/`@WithUserDetails`, `with(jwt())`, `with(csrf())` no MockMvc; testar 401 vs 403, roles, method security; `spring-security-test`. Liga **G12** (paga a dívida da nota 18). |
| 14 | Testando código assíncrono — Awaitility | `await().atMost(...).pollInterval(...).untilAsserted(...)`; consistência eventual (ex.: consumir evento e verificar efeito); **nunca `Thread.sleep`** (flakiness). Liga **G4** (o código concorrente/assíncrono testado). |
| 15 | Testando código reativo — StepVerifier e @WebFluxTest *(opus)* | **`StepVerifier`** (`.expectNext`/`.expectError`/`.verifyComplete`, `expectNextCount`, `withVirtualTime`); `@WebFluxTest` + `WebTestClient`; testar Mono/Flux sem bloquear. Liga **G11** (paga a dívida do `StepVerifier`). `reactor-test`. |
| 16 | Mockando HTTP externo — WireMock e MockRestServiceServer | WireMock (`stubFor`/`verify`, cenários/retry, `@DynamicPropertySource` pra apontar a base-url); `@RestClientTest` + `MockRestServiceServer` pra `RestClient`/`RestTemplate`. Liga **G9** (os clientes HTTP). |
| 17 | Mutation testing — PIT e cobertura honesta | Line coverage mente (100% sem asserção é inútil); **PIT** muta o bytecode (`>`→`>=`, remove `return`, nega condição) e mede se os testes pegam; **mutation coverage > line coverage**; custo (nightly, não cada build); `pitest-junit5-plugin`. |
| 18 | Performance — JMH e microbenchmarks | **JMH** (`@Benchmark`/`@Warmup`/`@Measurement`/`@Fork`/`@State`/`@Param`); por que `System.nanoTime()` num `@Test` mente (warmup, JIT, dead-code elimination, constant folding). Liga **G3** (o JIT que torna o microbenchmark traiçoeiro). |
| 19 | Fitness functions — ArchUnit (testes de arquitetura) *(opus)* | Regras de arquitetura como teste: `noClasses().that().resideInAPackage("..controller..").should().dependOnClassesThat()...`; `layeredArchitecture()`; sem ciclos (`slices().should().beFreeOfCycles()`); convenções de nome/anotação; guardrail contra drift. |
| 20 | Contract testing — Pact *(opus)* | Consumer declara expectativas (`@Pact`, `PactDslWithProvider`), gera o pact; producer verifica (`@Provider`, `@State`); quebra de contrato falha o build sem E2E frágil entre serviços. Liga **microservices (Galho 16, planejado — texto)**. |
| 21 | Capstone — a estratégia de testes de uma app Spring production-grade *(opus, checklist + síntese)* | A pirâmide na prática (70-80% unit / 15-25% integration / 2-5% E2E); tempo de suite alvo (unit <30s, total CI <10min); o que testar em qual nível; combate à flakiness; **tabela "o que testar → qual ferramenta/slice → qual galho"** (controller↔@WebMvcTest↔G9, repo↔@DataJpaTest↔G10, reativo↔StepVerifier↔G11, segurança↔@WithMockUser↔G12); cheatsheet nota→problema; munição de entrevista. |

**Notas opus (8):** 01 (assinatura/convergência), 06 (Mockito core), 09 (@WebMvcTest — liga G9), 10 (@DataJpaTest — liga G10), 12 (integração e2e), 15 (reativo/StepVerifier — liga G11), 20 (Pact/contract), 21 (capstone). As demais → sonnet. Notas version-specific (07, 08, 09, 10, 11, 13, 15) fazem WebFetch no Step 1 independentemente do modelo.

**Decisões de fronteira (escopo de outro dono — link-back ou texto "(planejado)"):**
- **A camada testada** (web/persistência/reativo/segurança/container/concorrência) → Galhos 9/10/11/12/8/4 (COMPLETOS). **Linkar de volta, nunca re-explicar.** Faces da convergência-assinatura.
- **Performance em produção / profiling / observabilidade** → Galho 17 (planejado). A nota 18 (JMH) cobre **microbenchmark de código**, não profiling de produção.
- **Contract testing aprofundado / Spring Cloud Contract / orquestração de microservices** → Galho 16 (planejado). A nota 20 (Pact) cobre o **conceito consumer/producer**, não a plataforma distribuída.
- **E2E web (Selenide/Playwright for Java)** → menção (fora do escopo backend; o foco é unit/slice/integration).
- **Mensageria testada (Kafka com Testcontainers/embedded)** → tocada de leve (Testcontainers Kafka como módulo na nota 11); profundidade fica no Galho 14 (planejado).
- **Teoria geral de testes (pirâmide como conceito abstrato, tipos de teste)** → o galho cobre a pirâmide **aplicada a Java/Spring**; não há nota geral `[[Testes]]` separada (o link no tronco era morto).

### 3.2. MOC do galho

`03-Dominios/Tecnologia/Java/Testes/index.md`:
- `type: moc`, `status: growing`
- Frontmatter padrão (`title: "Testes"`, tags `java`/`testes`/`moc`, aliases `["Testes", "Testes em Java", "Testing", "Galho 13 - Testes"]`)
- TL;DR callout (galho cobre a disciplina que testa os Galhos 1-12: JUnit 5/AssertJ/Mockito, os slices do Spring, Testcontainers e integração, testes de segurança/async/reativo, e o que vai além do verde — mutation testing, performance, fitness functions, contratos)
- "Sobre este galho" + audiência primária/secundária + nota de que é galho híbrido (poda integral do tronco `Testes em Java.md` + pesquisa version-specific) e de **convergência** (testa o que os Galhos 1-12 construíram; cada técnica linka de volta ao galho da coisa testada)
- Conteúdo agrupado em 3 H2 (`## Iniciado` / `## Adepto` / `## Magus`) com wikilinks pras 21 notas (uma linha descritiva cada)
- **Rotas alternativas (5):**
  - **Completa** — 01 → 21 em ordem
  - **Entrevista internacional** — 01 → 02 → 03 → 06 → 09 → 10 → 12 → 21 (pirâmide, JUnit, AssertJ, Mockito, slices web/data, integração, capstone)
  - **Os slices do Spring** — 08 → 09 → 10 → 11 → 12 → 13 (contexto, web, data, Testcontainers, integração, segurança)
  - **Indo além do verde** — 17 → 18 → 19 → 20 (mutation, performance, arquitetura, contrato)
  - **Testando o stack reativo** (ponte com o Galho 11) — 01 → 08 → 15 + notas do Galho 11 (WebFlux, WebClient)
- "Veja também": MOC central `[[03-Dominios/Tecnologia/Java/index|Trilha Java]]`, **Galho 8** (o container que os slices carregam), **Galho 9** (a web testada), **Galho 10** (a persistência testada), **Galho 11** (o reativo testado), **Galho 12** (a segurança testada), Dicionário de Java; Galhos 14/16/17 como texto "(planejado)" sem wikilink
- Dataview "Todas as notas do galho"

### 3.3. Dicionário de Java (EXPANSÃO — não recriar)

`03-Dominios/Tecnologia/Java/Dicionário de Java.md` já existe (**366 verbetes** após o Galho 12, `type: glossary`, `updated: 2026-06-10`, seções alfabéticas únicas `## A`…`## Z` com verbetes `### `). Este galho **expande** o arquivo existente inserindo os verbetes **em ordem alfabética case-insensitive (sem acento)** nas seções de letra apropriadas. **Nunca recriar o arquivo nem reordenar verbetes existentes.** Atualizar `updated` para `2026-06-11`.

Verbetes a inserir (~38, conferir dups antes):

`@DataJpaTest`, `@MockitoBean`, `@Nested`, `@ParameterizedTest`, `@ServiceConnection`, `@SpringBootTest`, `@WebFluxTest`, `@WebMvcTest`, `@WithMockUser`, `AAA (Arrange-Act-Assert)`, `ArchUnit`, `ArgumentCaptor`, `AssertJ`, `Awaitility`, `contract testing`, `fitness function`, `H2 (vs Testcontainers)`, `InjectMocks`, `JMH (microbenchmark)`, `JUnit 5 (Jupiter)`, `MockMvc`, `Mockito`, `mock vs spy vs fake vs stub`, `MockRestServiceServer`, `mutation testing`, `Pact`, `PIT (Pitest)`, `soft assertions`, `StepVerifier`, `test data builder`, `test pyramid (pirâmide de testes)`, `test slice (Spring Boot)`, `Testcontainers`, `TestEntityManager`, `usingRecursiveComparison`, `verify (Mockito)`, `WebTestClient`, `WireMock`.

Cada verbete: definição curta (1-3 linhas) em PT-BR + `Veja também:` apontando pra(s) nota(s) canônica(s) do galho. **Conferir com grep os verbetes já existentes** (possíveis dups dos Galhos 9-11: `WebTestClient`/`WebClient`, `MockMvc` se já houver; `JUnit` em alguma menção) para **não duplicar** — quando um termo tocar um já existente, **linkar entre si** em vez de criar segundo verbete. **Conferir 1:1** que os headings batem com âncoras `[[Dicionário de Java#...]]` usadas nas notas (extrair via grep e conferir, como nos galhos anteriores; se as notas linkarem o Dicionário sem âncora, basta inserção alfabética).

### 3.4. MOC central (ativação do Galho 13)

`03-Dominios/Tecnologia/Java/index.md` já existe. Task **mínima**: trocar a linha 43 (atualmente `13. Testes *(planejado)* — JUnit 5, Mockito, AssertJ, Spring Boot Test, Testcontainers`) por wikilink ativo no padrão dos galhos fechados:

```markdown
13. [[03-Dominios/Tecnologia/Java/Testes/index|Testes]] — a pirâmide e o stack moderno, JUnit 5/AssertJ/Mockito, os slices do Spring Boot, Testcontainers e integração, testes de segurança/async/reativo, mutation testing, performance, fitness functions e contract testing
```

Atualizar `updated` para `2026-06-11`. Não mexer no resto do MOC central.

### 3.5. Poda INTEGRAL do tronco `Backend/Testes em Java.md`

O tronco dedicado deste galho (1616 linhas, `publish: false`). **Poda integral** (padrão JavaFX/Galho 10/12): substituir **todo o corpo** (da linha após o frontmatter até o fim) por:
- frontmatter preservado, com `publish: false` (mantém — é tronco de trabalho) e `updated: 2026-06-11`;
- H1 `# Testes em Java`;
- 1-2 frases de intro neutras (sem fabricação);
- um único callout `[!nota] Migrado para galho próprio` com wikilink pro MOC do galho + ~5-6 notas representativas (01, 06, 09, 10, 12, 21), formato herdado do JavaFX/Galho 10/12:

```markdown
> [!nota] Migrado para galho próprio
> Expandido no galho [[03-Dominios/Tecnologia/Java/Testes/index|Testes]]. Veja [[03-Dominios/Tecnologia/Java/Testes/01 - O que é testar em Java — a pirâmide e o stack moderno|O que é testar em Java]], [[03-Dominios/Tecnologia/Java/Testes/06 - Mockito — mocks, stubbing e matchers|Mockito]], [[03-Dominios/Tecnologia/Java/Testes/09 - @WebMvcTest — testando controllers com MockMvc|@WebMvcTest]], [[03-Dominios/Tecnologia/Java/Testes/10 - @DataJpaTest — testando repositories|@DataJpaTest]], [[03-Dominios/Tecnologia/Java/Testes/12 - Testes de integração ponta a ponta|Testes de integração]] e o [[03-Dominios/Tecnologia/Java/Testes/21 - Capstone — a estratégia de testes de uma app Spring production-grade|Capstone]].
```

**Toda a fabricação some** (`Patient`/`PatientService`/`PatientController`/`Maria`/`PatientBuilder`/`PatientAssert`, `## Na prática (da minha experiência)` com a "evolução da stack do MedEspecialista" e o "incidente de flakiness no Kafka", `## How to explain in English` 1ª pessoa, `### Frases úteis em entrevista`). O nome de arquivo `Testes em Java.md` permanece. Confirmar números de linha na execução (lendo o tronco primeiro — política §9 do roadmap).

**NÃO TOCAR em outros troncos:** `Backend/Spring Boot.md`, `Backend/Spring Data JPA.md` (hub Galho 10), `Backend/Spring Security.md` (hub Galho 12), `Backend/Kafka/` + `Backend/gRPC e Go.md` (Galho 14). O `## Veja também` do tronco podado recebe wikilink pro MOC do Galho 13.

### 3.6. Dívida reversa (ganchos "Galho 13 / planejado")

Pré-flight localizou **1 ponteiro inline + 5 parágrafos de fronteira** a quitar após as notas existirem. Viram wikilinks pras notas do Galho 13; os testes deixam de ser texto "(planejado)" **nesses pontos específicos**:

| # | Arquivo:linha | Texto atual (resumo) | Vira wikilink pra |
|---|---|---|---|
| 1 | `index.md:43` (MOC central) | `13. Testes *(planejado)*` | ativação (§3.4) |
| 2 | `Segurança/18 - Capstone:98` | "a stack de teste ... é assunto do galho de Testes (Galho 13, planejado)" | **nota 13** (testando a segurança) |
| 3 | `Segurança/index.md:32` (parágrafo fronteira) | "Testes de segurança (Galho 13 planejado)" | **nota 13** ou MOC |
| 4 | `Persistência de dados/index.md:32` (parágrafo fronteira) | "testes de repositório (Galho 13)" | **nota 10** (@DataJpaTest) ou MOC |
| 5 | `Programação Reativa/index.md:35` (parágrafo fronteira) | "testes reativos com `StepVerifier` (Galho 13)" | **nota 15** (testando reativo) |
| 6 | `Spring Core e Boot/index.md:32` (parágrafo fronteira) | "Testes no ecossistema Spring (Galho 13)" | **MOC do galho** |
| 7 | `Web e APIs REST/index.md:32` (parágrafo fronteira) | "Testes no ecossistema Spring (Galho 13)" | **MOC do galho** |

**NÃO quitar (permanece "(planejado)"):**
- **Horizonte-lists de uma linha** (`Spring Core e Boot/index.md:97`, `Web e APIs REST/index.md:95`, `Persistência de dados/index.md:92`) — listas-resumo de galhos futuros que os galhos anteriores deixaram intactas (padrão estabelecido); 14/16/17 permanecem "(planejado)" lá, e o 13 também se aparecer nessas listas-resumo de uma linha.

Em todos os pontos, manter como texto "(planejado)" qualquer referência a galhos **ainda** inexistentes (14/16/17). Confirmar os números de linha na execução (podem ter deslocado) via grep `"Galho 13"`/`"planejado"`.

## 4. Convenções por nota

Herda §7 do roadmap e §4 dos specs dos Galhos 10/11/12. Reforços específicos:

### 4.1. Frontmatter

```yaml
---
title: "<título>"
created: 2026-06-11
updated: 2026-06-11
type: concept
status: seedling
publish: true
fase: iniciado | adepto | magus
tags:
  - java
  - testes
  - <fase>
  - <tags específicas: junit, assertj, mockito, parametrizados, spring-test, webmvctest, datajpatest, testcontainers, integracao, awaitility, stepverifier, wiremock, pit, jmh, archunit, pact, ...>
aliases:
  - <aliases opcionais>
---
```

H1 `# Título` após o frontmatter (padrão dos galhos publicados).

### 4.2. Estrutura H2 obrigatória

- `> [!abstract] TL;DR` (callout, NÃO H2) — 2-4 linhas: conceito + regra prática + por que importa
- `## O que é` / `## Por que importa` / `## Como funciona` (≥3 subseções H3 em notas Adepto/Magus)
- `## Na prática` — exemplos compiláveis; framing **neutro** (`Order`/`Customer`/`User`/`Product`/`OrderService`/`OrderRepository`/`OrderController`); "padrão observado em suítes de teste"; NUNCA `Patient`/`MedEspecialista`/"da minha experiência"/"quando comecei o projeto" (o tronco está cheio disso — **contraexemplo**)
- `## Armadilhas` — **≥2** (Iniciado) / **≥3** (Adepto/Magus), cada uma com `### (N) Título` (H3 numerado, NÃO callout `[!warning]`) + descrição + exemplo curto + fix em 1 linha
- `## Em entrevista` — subheading `### Frase pronta (inglês)` com **3+ sentenças** (trade-off + decisão + caveat) + subheading `### Vocabulário` com tabela `| Termo PT | Termo EN |` de **6+ termos**
- `## Veja também` — wikilinks **SEM backticks**, **SEM âncoras same-file**; sempre inclui notas relacionadas do galho + `[[03-Dominios/Tecnologia/Java/Testes/index|MOC do galho]]` + `[[03-Dominios/Tecnologia/Java/index|Trilha Java]]` + (quando testa uma camada) a nota do galho correspondente (G9 controllers, G10 repos, G11 reativo, G12 segurança, G8 container, G4 async, G3 JIT, G1 exceções) + verbetes do Dicionário
- `## Referências` — docs oficiais (junit.org, javadoc Mockito, docs.spring.io testing, testcontainers.org, assertj, pitest.org, archunit.org, docs.pact.io, openjdk JMH)

### 4.3. Restrições absolutas

1. **Convergência-assinatura (linkar de volta ao galho da coisa testada)** — toda técnica que testa uma camada aponta pra nota do galho dono (G9/G10/G11/G12/G8/G4/G3/G1), sem re-explicar a camada. Galhos 14/16/17 = texto "(planejado)", sem wikilink.
2. **Sem fabricação** de experiência pessoal. Exemplos neutros (`Order`, `Customer`, `User`, `Product`) — NUNCA `Patient`/`Maria`/`josenaldo`/`MedEspecialista`/1ª pessoa/"quando comecei o projeto"/"incidente de flakiness". **O tronco é matéria-prima a higienizar, jamais a copiar** (tem `## Na prática (da minha experiência)` com a evolução da stack do MedEspecialista e `## How to explain` 1ª pessoa — contraexemplo). **Zero estatística de adoção inventada** — os números de distribuição da pirâmide (70-80% unit etc.) vêm do tronco como **regra prática/heurística da indústria**, apresentados como tal (não "X% dos projetos fazem"), e idealmente confirmados/atenuados ("regra prática comum", sem cravar fonte estatística inventada).
3. **Sem invenção** de APIs/comportamentos. WebFetch obrigatório no Step 1 das notas version-specific (07/08/09/10/11/13/15) e pra **toda afirmação version-specific**. Pontos minados verificados via WebFetch: **`@MockitoBean` (Boot 3.4+) substituiu `@MockBean`**; **`@ServiceConnection` (Boot 3.1+)**; static mocking nativo do **Mockito 5** (sem PowerMock); versão atual de JUnit 5/Mockito/Testcontainers/AssertJ; `StepVerifier`/`reactor-test`; `spring-security-test` (`@WithMockUser`/`SecurityMockMvcRequestPostProcessors`). Spring Boot 3.x baseline (`jakarta.*`, Java 17), citando Boot 4.x como "mais recente" quando relevante. Fonte: docs oficiais. Nada "de memória".
4. **Code samples compiláveis** — Java moderno (records pra DTO/fixtures, `var`, text blocks pra JSON); imports corretos (`org.junit.jupiter.api.*`, `org.assertj.core.api.Assertions.*`, `org.mockito.*`, `org.springframework.boot.test.*`); fences corretas (`java`/`xml`/`yaml`/`bash`/`json`/`text`).
5. **Comparações justas** — mock vs spy vs fake, slice vs `@SpringBootTest`, H2 vs Testcontainers, AssertJ vs JUnit built-in, line vs mutation coverage, `Thread.sleep` vs Awaitility, unit vs integration: sempre "quando X" E "quando Y". O capstone (21) é o ápice (a pirâmide aplicada, sem dogma).
6. **Wikilinks sem backticks** em "Veja também"; MOC do galho + MOC central obrigatórios. **Não linkar galhos inexistentes** (14/16/17) — texto "(planejado)".
7. **Code fences corretos:** ` ```java ` pra código, ` ```xml `/` ```yaml ` pra config/pom, ` ```bash ` pra Maven/CLI, ` ```json ` pra payloads, ` ```text ` pra diagrama/pirâmide/output. Sempre fechadas.
8. **`fase:` no frontmatter + na tag** — obrigatório.
9. **Higiene de commits** — sem `Co-Authored-By: Claude`, sem `--no-verify`, `git add <path>` nominal (nunca `-A` — bot de backup Obsidian Git roda em timer), 1 commit por nota, controlador commita (subagents write-only). Guardar contra `.git/index.lock`.
10. **Tom pedagógico graduado** — Iniciado assume Galhos 1-2 (linguagem); Adepto assume Galho 8 (container) + 9/10 (web/persistência); Magus assume o stack inteiro (8-12).

## 5. Conteúdo por nota (síntese)

Esboço do recorte. Todas as notas partem do tronco `Testes em Java.md` refinado e higienizado; afirmações version-specific re-fundadas em doc oficial via WebFetch. Fontes-base: `junit.org/junit5/docs/current/user-guide/`, `javadoc.io/doc/org.mockito/mockito-core/latest`, `docs.spring.io/spring-boot/reference/testing/`, `java.testcontainers.org`, `assertj.github.io/doc/`, `pitest.org`, `archunit.org`, `docs.pact.io`, `github.com/openjdk/jmh`.

- **01 — O que é testar em Java (refator, opus).** Pirâmide; stack moderno (tabela); deprecated (JUnit4/Hamcrest/H2/PowerMock); **a convergência numa frase** (Testes testa os Galhos 1-12). Armadilhas: inverter a pirâmide; "coverage = qualidade". Fontes: junit.org, docs.spring.io.
- **02 — JUnit 5 (refator).** Platform/Jupiter/Vintage; lifecycle; AAA; `@DisplayName`/naming; per-method vs per-class; `@Timeout`/`@Disabled`. Armadilhas: estado compartilhado em PER_CLASS sem reset; `@BeforeAll` não-static sem PER_CLASS. Fontes: junit.org.
- **03 — AssertJ (refator).** `assertThat` encadeado; `extracting`; exception assertions; soft; recursive comparison. Armadilhas: `assertTrue(x.equals(y))` em vez de `isEqualTo` (mensagem ruim); esquecer `assertAll`/soft e parar na 1ª falha. Fontes: assertj.github.io.
- **04 — Parametrizados e organização (refator).** `@ParameterizedTest` + sources; `@Nested`; `@Tag`. Armadilhas: `@MethodSource` apontando método não-static sem PER_CLASS; teste parametrizado que esconde casos distintos. Fontes: junit.org.
- **05 — Test data builders e fixtures (refator).** Builder/object mother neutro; evitar setup duplicado; Instancio (menção). Armadilhas: builder mutável compartilhado entre testes; fixture gigante "pra tudo". Fontes: tronco higienizado + instancio.org (menção).
- **06 — Mockito mocks/stubbing/matchers (refator, opus).** mock/spy/fake/stub; `@Mock`/`@InjectMocks`; stubbing; matchers + regra "todos ou nenhum". Armadilhas: `when(spy).thenReturn` com side effect (use `doReturn`); misturar matcher e literal; stub não usado (`UnnecessaryStubbingException`). Fontes: javadoc.io/mockito, site.mockito.org.
- **07 — Mockito verify/captor/quando-não-mockar (refator).** verify/InOrder/noMoreInteractions; ArgumentCaptor; static mocking (5+); anti-patterns; injetar `Clock`. Armadilhas: `verify(times(n))` acoplado à implementação; mockar value object; `mockStatic` sem try-with-resources. Fontes: javadoc.io/mockito.
- **08 — Spring Boot Test e slices (refator + research).** Tabela de slices; `@SpringBootTest` vs slice; **caching do contexto** (liga G8); **`@MockitoBean` substituiu `@MockBean`** (WebFetch); `@ActiveProfiles`. Armadilhas: `@SpringBootTest` pra unit; contexto novo por config diferente (quebra cache, suíte lenta); `@MockBean` deprecated. Fontes: docs.spring.io/spring-boot (testing).
- **09 — @WebMvcTest (refator + research, opus).** Carrega só web; `MockMvc`+`jsonPath`; `@MockitoBean` no service; 200/404/422. Liga **G9**. Armadilhas: esperar que service/repo carreguem (não carregam); testar serialização sem `@JsonTest`; `MockMvc` vs servidor real. Fontes: docs.spring.io (MockMvc).
- **10 — @DataJpaTest (refator + research, opus).** Só JPA; `TestEntityManager`; rollback por teste; `Replace.NONE` + Testcontainers. Liga **G10**. Armadilhas: H2 default escondendo bug de dialeto; assumir commit (é rollback); testar derived query sem `flush`. Fontes: docs.spring.io (@DataJpaTest).
- **11 — Testcontainers (refator + research).** Por que não H2; `@Container`/`@ServiceConnection` (WebFetch); singleton + reuse; módulos. Liga **G10**. Armadilhas: container por teste (lento — use singleton/static); esquecer Docker no CI; reuse em CI (só dev). Fontes: java.testcontainers.org, docs.spring.io (@ServiceConnection).
- **12 — Integração ponta a ponta (refator, opus).** `@SpringBootTest(RANDOM_PORT)` + Testcontainers + `MockMvc`/`WebTestClient`/`TestRestTemplate`; `@DynamicPropertySource`; controller→service→banco. Armadilhas: integração demais (pirâmide invertida); estado vazando entre testes (sem rollback/reset); porta fixa. Fontes: docs.spring.io (testing).
- **13 — Testando a segurança (refator + research).** `@WithMockUser`/`@WithUserDetails`/`with(jwt())`/`with(csrf())`; 401 vs 403; `spring-security-test`. Liga **G12** (paga dívida nota 18). Armadilhas: testar endpoint protegido sem auth e estranhar 401; esquecer `with(csrf())` em POST stateful; `@WithMockUser` num teste sem method security ligado. Fontes: docs.spring.io/spring-security (testing).
- **14 — Async com Awaitility (refator).** `await().atMost().untilAsserted`; consistência eventual; nunca `Thread.sleep`. Liga **G4**. Armadilhas: `Thread.sleep` (flaky); timeout curto demais (flaky no CI lento); poll sem assert (passa cedo). Fontes: github.com/awaitility.
- **15 — Reativo: StepVerifier e @WebFluxTest (refator + research, opus).** `StepVerifier` (expectNext/expectError/verifyComplete, withVirtualTime); `@WebFluxTest`+`WebTestClient`. Liga **G11** (paga dívida do StepVerifier). Armadilhas: `block()` no teste em vez de `StepVerifier`; esquecer `verifyComplete`/`verify` (não assina); testar tempo real sem `withVirtualTime`. Fontes: projectreactor.io (testing), docs.spring.io (@WebFluxTest).
- **16 — HTTP externo: WireMock e MockRestServiceServer (refator).** WireMock (stub/verify/cenários, `@DynamicPropertySource`); `@RestClientTest`+`MockRestServiceServer`. Liga **G9** (clientes HTTP). Armadilhas: porta fixa do WireMock (colisão — use dynamic); não verificar a chamada; mockar o client em vez do transporte. Fontes: wiremock.org, docs.spring.io (@RestClientTest).
- **17 — Mutation testing: PIT (refator + research).** Line coverage mente; PIT muta o bytecode; mutation > line; custo (nightly). Armadilhas: line coverage como meta; PIT em cada build (lento); ignorar mutações sobreviventes. Fontes: pitest.org.
- **18 — Performance: JMH (refator + research).** `@Benchmark`/warmup/fork/state/param; por que `nanoTime` num `@Test` mente (JIT/warmup/dead-code/constant-fold). Liga **G3** (o JIT). Armadilhas: medir com `System.nanoTime()` num `@Test`; sem warmup; resultado não consumido (dead-code elimination — use `Blackhole`). Fontes: github.com/openjdk/jmh, docs.spring.io (n/a).
- **19 — Fitness functions: ArchUnit (refator, opus).** Regras de arquitetura como teste; `layeredArchitecture`; sem ciclos; convenções. Armadilhas: regra frágil por nome de pacote literal; ArchUnit sem rodar no CI (vira decoração); regra que ninguém entende. Fontes: archunit.org.
- **20 — Contract testing: Pact (refator + research, opus).** Consumer declara, gera pact; producer verifica (`@State`); quebra falha no build. Liga **microservices (G16, texto)**. Armadilhas: contrato acoplado a detalhe de implementação; producer não rodando a verificação no CI; usar Pact onde um teste de integração bastava. Fontes: docs.pact.io.
- **21 — Capstone: estratégia production-grade (refator, opus, checklist).** Pirâmide aplicada (70-80/15-25/2-5 como heurística); tempo de suite; o que testar onde; flakiness; **tabela "o que testar → ferramenta/slice → galho"**; cheatsheet nota→problema; munição de entrevista. Armadilhas de raciocínio: "coverage alto = bom" (mutation); "tudo integration" (pirâmide invertida); "H2 serve" (dialeto). Fontes: docs.spring.io, junit.org.

## 6. Pré-flight: verificações feitas

Executado nesta fase de brainstorming (2026-06-11); itens version-specific re-confirmados na execução de cada nota via WebFetch:

1. **Tronco mapeado** — `Backend/Testes em Java.md` (1616 linhas, `publish: false`, `status: evergreen`) lido **inteiro**. Cobre todo o escopo do roadmap + extras (WireMock/Awaitility/ArchUnit/PIT/JMH/Pact/builders) de forma monolítica. **Poda INTEGRAL** (padrão JavaFX/Galho 10/12). Seções: O que é, Stack moderno, JUnit 5 (arquitetura/setup/anatomia/assertions/parametrizados/nested/tags/assumptions/disabled/timeouts/lifecycle/extensions), AssertJ, Mockito (mock-spy-fake-stub/stubbing/matchers/verify/captor/spy/static/anti-patterns), Spring Boot Testing (slices/@WebMvcTest/@DataJpaTest/@SpringBootTest/WebEnvironment/profiles), Testcontainers, WireMock, Awaitility, ArchUnit, PIT, Pact, test data builders, logs/System.out/time, JMH, Estratégia/pirâmide, Armadilhas, Na prática (fabricação), How to explain (fabricação), Recursos, Veja também.
2. **Fabricação confirmada** — `Testes em Java.md`: `Patient`/`PatientService`/`PatientRepository`/`PatientController`/`PatientControllerTest`/`PatientNotFoundException`/`PatientBuilder`/`PatientAssert`/`Maria`/`maria@example.com` no corpo todo (97 matches); `## Na prática (da minha experiência)` (~1483, "evolução da stack de testes do MedEspecialista" — JUnit4→5, H2→Testcontainers, Hamcrest→AssertJ, ArchUnit, pyramid balance, Pact, PIT, "incidente de flakiness no Kafka"); `## How to explain in English` 1ª pessoa (~1516) + `### Frases úteis`. **Some toda com a poda integral.** Notas usam `Order`/`Customer`/`User`/`Product` neutros.
3. **Convergência-assinatura confirmada** — Galhos 9 (controllers/clientes HTTP), 10 (repos/queries), 11 (WebFlux), 12 (authz/method security), 8 (container/auto-config), 4 (concorrência), 3 (JIT), 1 (exceções) existem em `main`. Os Galhos 10/11/12 **esperam** o link-back deste galho.
4. **Dívida reversa localizada** — 1 ponteiro inline (Segurança/18:98) + 5 parágrafos de fronteira (Segurança/index:32, Persistência/index:32, Reativa/index:35, Spring Core/index:32, Web/index:32) + MOC central :43. **NÃO quitar**: horizonte-lists de uma linha (Spring Core:97, Web:95, Persistência:92). Confirmar linhas na execução.
5. **Dicionário** — **366 verbetes** após o Galho 12; seções alfabéticas únicas `## A`…`## Z`; verbetes `### `; `updated: 2026-06-10`. Possíveis dups (Galhos 9-11): `WebTestClient`/`WebClient`, `MockMvc` — conferir e linkar, nunca duplicar. Expansão alfabética (~38), nunca recriar/reordenar.
6. **MOC central** — `03-Dominios/Tecnologia/Java/index.md:43` é a linha do Galho 13 (`*(planejado)*`); galhos ativos usam `N. [[path/index|Title]] — summary`; `updated: 2026-06-10`.
7. **Troncos intocáveis** — `Backend/Spring Boot.md`, `Backend/Spring Data JPA.md` (hub Galho 10), `Backend/Spring Security.md` (hub Galho 12), `Backend/Kafka/` + `Backend/gRPC e Go.md` (Galho 14). Pasta `Testes/` ainda **não existe**; não há colisão com nota geral `[[Testes]]` (link morto no tronco).
8. **Versões a cravar via WebFetch na execução** — JUnit 5.x, Mockito 5.x, AssertJ, Testcontainers (todas as versões atuais); **`@MockitoBean` Boot 3.4+ substituiu `@MockBean`**; **`@ServiceConnection` Boot 3.1+**; static mocking nativo Mockito 5; `reactor-test`/`StepVerifier`; `spring-security-test`; PIT/`pitest-junit5-plugin`; ArchUnit; JMH. Baseline Boot 3.x (`jakarta.*`, Java 17), citando Boot 4.x como "mais recente". Fonte: docs oficiais.

Nenhum número de adoção é inventado. Quando faltar fato verificável, **PERGUNTAR** antes de escrever.

## 7. Critérios de aceitação do galho

Além dos critérios gerais (§10 do roadmap):

1. 21 notas em `03-Dominios/Tecnologia/Java/Testes/`, frontmatter completo com `fase:`, `publish: true`, distribuídas 5/7/9.
2. MOC do galho com 3 subseções de fase + 5 rotas alternativas + dataview + folder-link resolve (`index.md` presente).
3. Dicionário de Java **expandido** (não recriado) com ~38 verbetes; verbetes dos Galhos 1-12 intactos; `updated: 2026-06-11`; dups conferidos e linkados (não duplicar `WebTestClient`/`MockMvc`/`WebClient` se vierem dos Galhos 9-11).
4. MOC central `Java/index.md` com Galho 13 ativado (linha 43 vira wikilink); resto intacto.
5. **Poda integral do tronco executada**: `Testes em Java.md` reduzido a hub (poda integral, fabricação do MedEspecialista/flakiness/`How to explain` some, `publish: false` mantido). **Outros troncos intactos**.
6. **Dívida reversa quitada**: o ponteiro inline (Segurança/18) + 5 parágrafos de fronteira com wikilinks corretos (Persistência:32→nota10, Reativa:35→nota15, Segurança:32→nota13, Spring Core/Web:32→MOC); galhos ainda inexistentes (14/16/17) permanecem texto "(planejado)"; horizonte-lists intactos.
7. Cada nota: TL;DR; code samples compiláveis (Java moderno, imports corretos, fences `java`/`xml`/`yaml`/`bash`/`json`/`text`); "Em entrevista" com `### Frase pronta (inglês)` 3+ sentenças + `### Vocabulário` tabela 6+ termos PT→EN; "Armadilhas" com `### (N) Título` numerado + exemplo + fix (≥2 Iniciado, ≥3 Adepto/Magus); wikilinks (galho + MOC central + galho da camada testada quando aplicável + Dicionário); "Referências" com docs oficiais verificadas.
8. **Convergência-assinatura respeitada**: cada técnica que testa uma camada linka de volta ao galho dono (G9/G10/G11/G12/G8/G4/G3/G1) sem re-explicar; galhos 14/16/17 só como texto "(planejado)"; nenhum wikilink pra galho inexistente.
9. **Fronteiras de escopo respeitadas**: profiling de produção = Galho 17; microservices/Spring Cloud Contract = Galho 16; E2E web (Selenide/Playwright) = menção; mensageria testada de leve (Kafka Testcontainers); zero conteúdo profundo de produção/distribuído.
10. Zero fabricação de experiência pessoal; zero estatística de adoção inventada (a distribuição da pirâmide é heurística, apresentada como tal); afirmações version-specific citam a versão verificada via WebFetch.
11. 1 commit por nota; sem `Co-Authored-By: Claude`; sem `--no-verify`; stage nominal (nunca `-A`); subagents write-only, controlador commita.
12. `verificar-wikilinks` roda limpo na pasta do galho (evitar âncoras same-file; conferir os títulos EXATOS das notas nos cheatsheets/checklist — lição do Galho 12, onde a nota 18 inventou títulos).

## 8. Riscos e mitigações

| Risco | Mitigação |
|---|---|
| **Re-explicar a camada testada** (web/persistência/reativo/segurança) em vez de linkar de volta | Restrição 4.3.1; cada nota de slice linka o galho dono (G9/G10/G11/G12); review por fase; capstone mapeia em tabela. |
| **Copiar fabricação do tronco** (`Patient`/MedEspecialista/"evolução da stack"/"incidente de flakiness") pras notas | O tronco é contraexemplo (restrição 4.3.2); poda integral faz a fabricação sumir; exemplos neutros `Order`/`Customer`; review por fase grep `Patient\|MedEspecialista\|minha experiência\|quando comecei\|incidente de flakiness`. |
| **Inventar estatística** (distribuição da pirâmide como dado de adoção) | A distribuição 70-80/15-25/2-5 é **heurística da indústria** apresentada como regra prática, não "X% dos projetos"; sem fonte estatística inventada. |
| **Inventar API/versão "de memória"** (`@MockitoBean`/`@MockBean`, `@ServiceConnection`, static mocking, versões) | WebFetch no Step 1 das notas version-specific (07/08/09/10/11/13/15); Referências com fonte oficial; nada "de memória". |
| **Cheatsheet/checklist do capstone inventar títulos de notas** (lição do Galho 12, nota 18) | Passar aos subagentes os **títulos EXATOS** das notas linkadas; `verificar-wikilinks` ao fim; review do capstone confere 1:1. |
| **Invadir Galho 16 (microservices)** ao falar de Pact/contract | Pact = conceito consumer/producer; Spring Cloud Contract/orquestração distribuída = texto "(planejado)"; review por fase. |
| **Invadir Galho 17 (produção)** ao falar de JMH | JMH = microbenchmark de código; profiling/observabilidade de produção = texto "(planejado)"; nota 18 linka G3 (JIT), não G17. |
| **Slices virarem notas redundantes** (@WebMvcTest/@DataJpaTest/@SpringBootTest/integração muito parecidas) | Cada nota tem foco distinto (08 panorama+contexto, 09 web, 10 data, 11 Testcontainers, 12 integração full); review por fase checa sobreposição. |
| Galho denso (21 notas) inflar notas individuais | Distribuição 5/7/9 fixada; se uma nota passar de ~600 linhas, dividir nota (não galho); capstone com cheatsheet enxuto. |
| Dicionário: duplicar verbete já existente (`WebTestClient`, `MockMvc`, `WebClient`) | Grep dos existentes antes de inserir; quando tocar um existente, **linkar** em vez de duplicar; inserção alfabética, nunca recriar. |
| Bot de backup (Obsidian Git) commitando no meio | Padrão dos Galhos 2-12: subagents write-only; controlador commita imediatamente após cada nota com `git add` nominal (nunca `-A`); guardar contra `.git/index.lock`. |

## 9. Próximos passos

1. **Aprovação deste spec**
2. **Plano de execução** via skill `superpowers:writing-plans` → `docs/superpowers/plans/2026-06-11-java-galho-13-testes-execution.md`
3. **Execução** via `superpowers:subagent-driven-development` **direto na `main`** (subagents write-only; sonnet por padrão, opus nas notas 01/06/09/10/12/15/20/21; review **por fase** + fix loop; push manual do usuário)
4. **Verificação** de wikilinks + conferência de âncoras do Dicionário
5. **Atualização da memória** `project_trilha_java` (Galho 13 completo) antes do próximo galho

## 10. Documentos relacionados

- `2026-06-02-java-senior-roadmap-design.md` — roadmap macro (18 galhos)
- `2026-06-10-java-galho-12-seguranca-design.md` / `...-execution.md` — Galho 12 (molde direto de **poda integral** + dupla fronteira + dívida reversa; lição do capstone-que-inventou-títulos)
- `2026-06-09-java-galho-10-persistencia-design.md` — Galho 10 (poda integral; dono dos repos que `@DataJpaTest` testa)
- `2026-06-10-java-galho-11-reativa-design.md` — Galho 11 (dono do reativo que `StepVerifier` testa; deixou a dívida do StepVerifier)
- `2026-06-08-java-galho-09-web-rest-design.md` — Galho 9 (dono dos controllers que `@WebMvcTest` testa)
- `2026-06-08-java-galho-08-spring-core-design.md` — Galho 8 (dependência: o container que os slices carregam)
- Galho 6 (JavaFX) — template de **poda integral** de tronco monolítico
- Artefatos a atualizar: `03-Dominios/Tecnologia/Java/Dicionário de Java.md`, `03-Dominios/Tecnologia/Java/index.md`, `03-Dominios/Tecnologia/Java/Backend/Testes em Java.md` (poda integral), `Segurança/18 - Capstone`, `Segurança/index.md`, `Persistência de dados/index.md`, `Programação Reativa/index.md`, `Spring Core e Boot/index.md`, `Web e APIs REST/index.md` (dívida reversa)
- Fontes-base do galho: `junit.org/junit5/docs/current/user-guide/`, `javadoc.io/doc/org.mockito`, `docs.spring.io/spring-boot/reference/testing/`, `java.testcontainers.org`, `assertj.github.io`, `pitest.org`, `archunit.org`, `docs.pact.io`, `github.com/openjdk/jmh`
- Memórias: [[project_trilha_java]], [[project_trilhas_fases_aprendizado]], [[project_tronco_galhos_pattern]], [[feedback_galhos_direto_main]], [[feedback_no_fabrication]], [[feedback_quartz_index]], [[feedback_commits]], [[feedback_dataview_inline_code]], [[feedback_notas_atomicas]], [[feedback_enriquecimento_feynman]]
