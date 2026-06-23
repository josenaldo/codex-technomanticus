# Galho 13 — Testes (Java Senior) — Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Criar o Galho 13 da trilha Java Senior — 21 notas atômicas (pirâmide/stack, JUnit 5, AssertJ, parametrizados, builders, Mockito ×2, Spring Boot Test/slices, @WebMvcTest, @DataJpaTest, Testcontainers, integração e2e, testando segurança/async/reativo, WireMock, PIT, JMH, ArchUnit, Pact, capstone) em 3 fases + MOC do galho + expansão do Dicionário + ativação do MOC central + **poda INTEGRAL** do tronco `Backend/Testes em Java.md` + **quitação da dívida reversa**.

**Architecture:** Padrão galhos + 3 fases (Iniciado/Adepto/Magus). Pasta flat `03-Dominios/Tecnologia/Java/Testes/`, notas `publish: true` em PT-BR, numeração global 01-21 (5/7/9). **Galho HÍBRIDO** = refator (poda integral de tronco monolítico de 1616 linhas, padrão JavaFX/Galho 10/12 — vira hub; toda a fabricação `Patient`/MedEspecialista/"evolução da stack"/flakiness evapora) + pesquisa (version-specific via WebFetch). **Galho de CONVERGÊNCIA: testa o que os Galhos 1-12 construíram** — cada técnica linka de volta ao galho da coisa testada (@WebMvcTest→G9, @DataJpaTest→G10, StepVerifier/@WebFluxTest→G11, @WithMockUser→G12, slices→G8, Awaitility→G4, JMH→G3, assertThrows→G1). Paga 3 dívidas explícitas (G10 @DataJpaTest, G11 StepVerifier, G12 @WithMockUser). Galhos 14/16/17 = texto "(planejado)", sem wikilink. **Direto na `main`** ([[feedback_galhos_direto_main]]); push manual do usuário.

**Tech Stack:** Obsidian Flavored Markdown, frontmatter YAML, wikilinks, callouts, Dataview, Quartz v4. Verificação via WebFetch (junit.org, javadoc.io/mockito, docs.spring.io/spring-boot/testing, java.testcontainers.org, assertj.github.io, projectreactor.io, pitest.org, archunit.org, docs.pact.io, github.com/openjdk/jmh).

---

## Convenções aplicadas a TODAS as notas (ler antes de qualquer task)

**Frontmatter** (ajustar `title`/`fase`/`tags`/`aliases` por nota; `created`/`updated: 2026-06-11`):

```yaml
---
title: "<título sem prefixo numérico>"
created: 2026-06-11
updated: 2026-06-11
type: concept
progress: backlog
status: seedling
publish: true
fase: iniciado | adepto | magus
tags:
  - java
  - testes
  - <fase>
  - <1-3 tags de conceito: junit, assertj, mockito, parametrizados, spring-test, webmvctest, datajpatest, testcontainers, integracao, awaitility, stepverifier, wiremock, pit, jmh, archunit, pact>
aliases:
  - <aliases>
---
```

H1 `# Título` após o frontmatter.

**Estrutura H2 obrigatória** (nesta ordem):

1. `> [!abstract] TL;DR` — 2-4 linhas. Callout, NÃO H2.
2. `## O que é` — definição.
3. `## Por que importa` — relevância pra senior/entrevista.
4. `## Como funciona` — H3s; mínimo 3 em Adepto/Magus.
5. `## Na prática` — código compilável; framing neutro; **NUNCA** 1ª pessoa, `Patient`, `Maria`, `Josenaldo`, `MedEspecialista`, "da minha experiência", "quando comecei o projeto", "incidente de flakiness". Domínios neutros: `Order`, `Customer`, `User`, `Product`, `OrderService`, `OrderRepository`, `OrderController`. Imports corretos (`org.junit.jupiter.api.*`, `org.assertj.core.api.Assertions.*`, `org.mockito.*`, `org.springframework.boot.test.*`).
6. `## Armadilhas` — ≥2 (Iniciado) / ≥3 (Adepto/Magus). Cada uma: `### (N) Título` + descrição + exemplo curto + fix em 1 linha (H3 numerado, NÃO callout `[!warning]`).
7. `## Em entrevista` — `### Frase pronta (inglês)` com **3+ sentenças** + `### Vocabulário` **6+ termos** em tabela `| Termo PT | Termo EN |`.
8. `## Veja também` — wikilinks SEM backticks, SEM âncoras same-file. Sempre: notas do galho + `[[03-Dominios/Tecnologia/Java/Testes/index|Testes (MOC do galho)]]` + `[[03-Dominios/Tecnologia/Java/index|Trilha Java]]` + (quando testa uma camada) a nota do galho dono + verbetes do Dicionário.
9. `## Referências` — docs oficiais consultadas.

**Tamanho:** 200-500 linhas (densas até 600 — limite de [[feedback_notas_atomicas]]).

**Restrições absolutas:**
- **CONVERGÊNCIA-assinatura.** Mapeamento de link-back: **G9** (controllers/clientes HTTP testados) → `Web e APIs REST/02 - @RestController e os mapeamentos`, `06 - O pipeline do DispatcherServlet`, `09 - Tratamento de exceções com @ControllerAdvice`, `15 - Clientes HTTP — RestClient, WebClient, RestTemplate`; **G10** (repos testados) → `Persistência de dados/04 - Spring Data repositories — JpaRepository e query methods derivados`, `09 - Consultas com @Query — JPQL, native e @Modifying`; **G11** (reativo testado) → `Programação Reativa/10 - Spring WebFlux — o stack não-bloqueante sobre Netty e o DispatcherHandler`, `11 - WebClient — o cliente HTTP reativo a fundo`; **G12** (segurança testada) → `Segurança/05 - Autorização baseada em URL — authorizeHttpRequests, roles vs authorities`, `07 - Method security — @PreAuthorize, @PostAuthorize e SpEL`; **G8** (container/slices) → `Spring Core e Boot/06 - ApplicationContext — o container e seu ciclo`, `15 - Auto-configuration e starters`; **G4** (async) → `Concorrência e paralelismo/index`; **G3** (JIT/JMH) → `JVM/07 - O compilador JIT — C1, C2 e a compilação adaptativa`; **G1** (exceções) → `Linguagem e sintaxe moderna/10 - Exceções e tratamento de erros`.
- **Galhos 14/16/17 só como texto "(planejado)", SEM wikilink.** Greps de review checam `\[\[[^]]*(Galho (14|16|17)|Spring Cloud|Selenide|Playwright|Kafka)`.
- Sem fabricação ([[feedback_no_fabrication]]); usar `Order`/`Customer`/`User`/`Product`. **Zero estatística de adoção inventada** — a distribuição da pirâmide (70-80% unit / 15-25% integration / 2-5% E2E) é **heurística da indústria**, apresentada como "regra prática comum", NÃO "X% dos projetos fazem".
- **Pesquisa pras partes version-specific:** notas 07/08/09/10/11/13/15 fundam-se em WebFetch (Step 1); qualquer outra que cravar versão também confirma. Fatos a confirmar: versão atual de JUnit 5/Mockito 5/AssertJ/Testcontainers; **`@MockitoBean` (Boot 3.4+) substituiu `@MockBean`** (deprecated); **`@ServiceConnection` (Boot 3.1+)**; static mocking nativo do Mockito 5 (sem PowerMock); `reactor-test`/`StepVerifier`; `spring-security-test` (`@WithMockUser`/`SecurityMockMvcRequestPostProcessors.jwt()`/`.csrf()`); `pitest-junit5-plugin`; ArchUnit; JMH. Baseline Boot 3.x (`jakarta.*`, Java 17), citando Boot 4.x como "mais recente". Nada de memória.
- **Não re-explicar o que é de outro galho:** controllers/DispatcherServlet/clientes HTTP → G9 (linkar); repos/queries/persistence context → G10 (linkar); WebFlux/Mono/Flux → G11 (linkar); authn/authz/method security → G12 (linkar); container/auto-config/AOP → G8 (linkar); concorrência/async → G4 (linkar); JIT/warmup → G3 (linkar); exceções → G1 (linkar). Microservices/Spring Cloud Contract → G16 (texto); profiling de produção → G17 (texto); E2E web → menção.
- Comparações justas (quando X E quando Y): mock vs spy vs fake, slice vs @SpringBootTest, H2 vs Testcontainers, AssertJ vs JUnit built-in, line vs mutation coverage, Thread.sleep vs Awaitility, unit vs integration.
- Code fences: ` ```java `, ` ```xml ` (pom), ` ```yaml `/` ```properties ` (config), ` ```bash ` (Maven), ` ```json ` (payloads), ` ```text ` (pirâmide/output). Sempre fechadas.
- Commits: sem `Co-Authored-By: Claude`; sem `--no-verify`; `git add <path>` nominal (bot de backup roda em timer — NUNCA `-A`; guardar contra `.git/index.lock`); 1 commit por nota; direto na `main`; **sem push, sem deploy**. Subagents NÃO rodam git — o controlador commita.

**Modelo por nota:** sonnet por padrão; **opus** nas **01** (assinatura/pirâmide), **06** (Mockito core), **09** (@WebMvcTest), **10** (@DataJpaTest), **12** (integração e2e), **15** (reativo/StepVerifier), **20** (Pact/contract), **21** (capstone).

**Fontes oficiais (base):**
- JUnit 5 user guide: `https://junit.org/junit5/docs/current/user-guide/`
- AssertJ: `https://assertj.github.io/doc/`
- Mockito: `https://javadoc.io/doc/org.mockito/mockito-core/latest/index.html` + `https://site.mockito.org/`
- Spring Boot Testing: `https://docs.spring.io/spring-boot/reference/testing/index.html`
- Spring MockMvc / Spring TestContext: `https://docs.spring.io/spring-framework/reference/testing/`
- Testcontainers: `https://java.testcontainers.org/` + `https://docs.spring.io/spring-boot/reference/testing/testcontainers.html`
- Reactor test (StepVerifier): `https://projectreactor.io/docs/core/release/reference/#testing`
- Spring Security testing: `https://docs.spring.io/spring-security/reference/servlet/test/index.html`
- Awaitility: `https://github.com/awaitility/awaitility/wiki/Usage`
- WireMock: `https://wiremock.org/docs/`
- PIT: `https://pitest.org/`
- ArchUnit: `https://www.archunit.org/userguide/html/000_Index.html`
- Pact: `https://docs.pact.io/`
- JMH: `https://github.com/openjdk/jmh`

---

## Task 0: Pré-flight — pasta, terreno e baselines

**Files:**
- Create: `03-Dominios/Tecnologia/Java/Testes/` (pasta)

- [ ] **Step 1: Confirmar `main`**
```bash
git branch --show-current
```
Expected: `main`. NÃO criar branch.

- [ ] **Step 2: Criar a pasta do galho**
```bash
mkdir -p "03-Dominios/Tecnologia/Java/Testes"
```

- [ ] **Step 3: Confirmar títulos exatos das notas dos Galhos 1/3/4/8/9/10/11/12 (linkadas de volta)**
```bash
ls "03-Dominios/Tecnologia/Java/Linguagem e sintaxe moderna/" | grep -E "^10 "
ls "03-Dominios/Tecnologia/Java/JVM/" | grep -E "^07 "
ls "03-Dominios/Tecnologia/Java/Spring Core e Boot/" | grep -E "^(06|15) "
ls "03-Dominios/Tecnologia/Java/Web e APIs REST/" | grep -E "^(02|06|09|15) "
ls "03-Dominios/Tecnologia/Java/Persistência de dados/" | grep -E "^(04|09) "
ls "03-Dominios/Tecnologia/Java/Programação Reativa/" | grep -E "^(10|11) "
ls "03-Dominios/Tecnologia/Java/Segurança/" | grep -E "^(05|07) "
```
Expected: G1 `10 - Exceções e tratamento de erros`; G3 `07 - O compilador JIT — C1, C2 e a compilação adaptativa`; G8 `06 - ApplicationContext — o container e seu ciclo`, `15 - Auto-configuration e starters`; G9 `02 - @RestController e os mapeamentos`, `06 - O pipeline do DispatcherServlet`, `09 - Tratamento de exceções com @ControllerAdvice`, `15 - Clientes HTTP — RestClient, WebClient, RestTemplate`; G10 `04 - Spring Data repositories — JpaRepository e query methods derivados`, `09 - Consultas com @Query — JPQL, native e @Modifying`; G11 `10 - Spring WebFlux — o stack não-bloqueante sobre Netty e o DispatcherHandler`, `11 - WebClient — o cliente HTTP reativo a fundo`; G12 `05 - Autorização baseada em URL — authorizeHttpRequests, roles vs authorities`, `07 - Method security — @PreAuthorize, @PostAuthorize e SpEL`. Anotar divergências (se o nome real do JIT no G3 diferir, usar o real).

- [ ] **Step 4: Relocalizar a dívida reversa (1 inline + 5 parágrafos — linhas podem ter mudado)**
```bash
grep -rn "Galho 13\|galho 13" "03-Dominios/Tecnologia/Java/Segurança/18 - Capstone — projetando a segurança de uma API Spring production-grade.md" "03-Dominios/Tecnologia/Java/Segurança/index.md" "03-Dominios/Tecnologia/Java/Persistência de dados/index.md" "03-Dominios/Tecnologia/Java/Programação Reativa/index.md" "03-Dominios/Tecnologia/Java/Spring Core e Boot/index.md" "03-Dominios/Tecnologia/Java/Web e APIs REST/index.md"
grep -n "Testes\|planejado" "03-Dominios/Tecnologia/Java/index.md" | grep "13\."
```
Expected (anotar linhas reais pra Task 23): MOC central item 13 (`~43`); Segurança/18 :~98 (inline); Segurança/index :~32; Persistência/index :~32; Reativa/index :~35; Spring Core/index :~32; Web/index :~32. **NÃO tocar:** horizonte-lists de uma linha (Spring Core :97, Web :95, Persistência :92).

- [ ] **Step 5: Baseline do Dicionário**
```bash
grep -cE "^### " "03-Dominios/Tecnologia/Java/Dicionário de Java.md"
```
Expected: **366** (baseline pós-Galho 12). Anotar o número real.

- [ ] **Step 6: Ler o tronco a podar (pra Task 22) e mapear a fabricação**
```bash
grep -nE "^## " "03-Dominios/Tecnologia/Java/Backend/Testes em Java.md"
grep -ciE "Patient|Maria|MedEspecialista|minha experiência|quando comecei|incidente de flakiness|How to explain" "03-Dominios/Tecnologia/Java/Backend/Testes em Java.md"
```
Expected: tronco monolítico (1616 linhas, `publish: false`) com `## Na prática (da minha experiência)` (~1483) e `## How to explain in English` (~1516) fabricados + `Patient`/`Maria` em todo o corpo (~97 matches). **Poda INTEGRAL** (todo o corpo vira hub). Anotar a linha do frontmatter pra preservar.

- [ ] **Step 7: Fixar fatos a verificar via WebFetch** — `@MockitoBean` (Boot 3.4+) substituiu `@MockBean`; `@ServiceConnection` (Boot 3.1+); static mocking nativo Mockito 5; versões atuais JUnit 5/Mockito/Testcontainers/AssertJ; `reactor-test`/`StepVerifier`; `spring-security-test`; PIT/ArchUnit/JMH; baseline Boot 3.x. Nada de memória.

- [ ] **Step 8: Sem commit** (preparação).

---

## Fase INICIADO (notas 01-05)

### Task 1: Nota 01 — O que é testar em Java — a pirâmide e o stack moderno ⟦opus⟧

**Files:**
- Create: `03-Dominios/Tecnologia/Java/Testes/01 - O que é testar em Java — a pirâmide e o stack moderno.md`

- [ ] **Step 1: Pesquisar** — WebFetch `https://junit.org/junit5/docs/current/user-guide/` (intro) + `https://docs.spring.io/spring-boot/reference/testing/index.html`. CONFIRMAR: a pirâmide (unit/integration/E2E); o stack moderno (JUnit 5/AssertJ/Mockito/Testcontainers/Spring Boot Test); `spring-boot-starter-test` traz JUnit 5+AssertJ+Mockito; deprecated (JUnit 4/Hamcrest/H2/PowerMock).

- [ ] **Step 2: Escrever** — `fase: iniciado`, tags `[java, testes, iniciado, junit]`, aliases `["testes em Java", "pirâmide de testes", "stack de testes Java"]`. **Nota-assinatura da CONVERGÊNCIA.** Conteúdo:
  - TL;DR: testar em Java hoje é um stack (JUnit 5/AssertJ/Mockito/Testcontainers/Spring Boot Test) sobre uma pirâmide (muitos unit, alguns integration, poucos E2E); este galho testa o que os Galhos 1-12 construíram — cada técnica linka de volta ao galho da coisa testada.
  - `## O que é` — testar Java moderno vs 2010.
  - `## Por que importa` — pra senior, dominar o stack é tão importante quanto a linguagem; entrevista cobra "qual sua estratégia de testes".
  - `## Como funciona` — H3s: "A pirâmide: muitos unit, alguns integration, poucos E2E (não inverter)", "O stack moderno: JUnit 5, AssertJ, Mockito, Testcontainers, Spring Boot Test" (com tabela ferramenta/propósito), "Ferramentas deprecated que você ainda encontra (JUnit 4, Hamcrest, H2, PowerMock)", "A convergência: Testes testa os Galhos 1-12 (cada slice/técnica linka o galho da camada testada)".
  - `## Na prática` — um teste mínimo JUnit 5 + AssertJ de um `OrderService` neutro (```java) mostrando AAA.
  - `## Armadilhas` — ≥2: (1) inverter a pirâmide (muitos @SpringBootTest, poucos unit — suíte lenta); (2) "coverage alto = qualidade" (100% sem asserção é inútil — prenúncio do mutation testing).
  - `## Em entrevista` + `## Veja também` ([[02 - JUnit 5 — anatomia, lifecycle e o padrão AAA]], [[21 - Capstone — a estratégia de testes de uma app Spring production-grade]], MOC galho, MOC central, verbetes `test pyramid (pirâmide de testes)`/`JUnit 5 (Jupiter)`/`AssertJ`/`Mockito`/`Testcontainers`) + `## Referências`.

- [ ] **Step 3: Verificar**
```bash
grep -cE "^## (O que é|Por que importa|Como funciona|Na prática|Armadilhas|Em entrevista|Veja também|Referências)" "03-Dominios/Tecnologia/Java/Testes/01 - O que é testar em Java — a pirâmide e o stack moderno.md"
grep -riE "Patient|Maria|MedEspecialista|minha experiência|quando comecei" "03-Dominios/Tecnologia/Java/Testes/01 - O que é testar em Java — a pirâmide e o stack moderno.md"
```
Expected: ≥7 seções; segundo grep **VAZIO**.

- [ ] **Step 4: Commit** — `git add "<path>"` && `git commit -m "feat(java): galho 13 nota 01 — o que é testar em Java (a pirâmide e o stack moderno)"`

### Task 2: Nota 02 — JUnit 5 — anatomia, lifecycle e o padrão AAA

**Files:**
- Create: `03-Dominios/Tecnologia/Java/Testes/02 - JUnit 5 — anatomia, lifecycle e o padrão AAA.md`

- [ ] **Step 1: Pesquisar (version-specific)** — WebFetch `https://junit.org/junit5/docs/current/user-guide/#writing-tests`. CONFIRMAR: Platform/Jupiter/Vintage; `@Test`/`@BeforeEach`/`@AfterEach`/`@BeforeAll`/`@AfterAll`; `@DisplayName`; `@TestInstance(PER_CLASS)` (permite `@BeforeAll` não-static); `@Timeout`/`@Disabled`/`@DisabledOnOs`; nova instância por teste (default PER_METHOD). **WebFetch obrigatório.**

- [ ] **Step 2: Escrever** — `fase: iniciado`, tags `[java, testes, iniciado, junit]`. Conteúdo:
  - TL;DR: JUnit 5 (Jupiter) é o framework de testes moderno; cada teste é um método `@Test` numa classe, com hooks de lifecycle (`@BeforeEach`/etc.) e o padrão AAA (given/when/then); `@DisplayName` dá nomes legíveis.
  - H3s: "Platform / Jupiter / Vintage: as 3 partes", "O lifecycle: @BeforeAll/@BeforeEach/@AfterEach/@AfterAll", "AAA (Arrange-Act-Assert) e convenções de nome", "Per-method vs per-class (@TestInstance) e por que o default isola estado".
  - `## Na prática` — uma classe `OrderServiceTest` (neutra!) com os hooks + um teste AAA + `@DisplayName` (```java).
  - `## Armadilhas` — ≥2: (1) estado compartilhado entre testes com PER_CLASS sem reset (contamina); (2) `@BeforeAll` não-static sem PER_CLASS (não compila/não roda).
  - `## Veja também` — [[01 - O que é testar em Java — a pirâmide e o stack moderno]], [[03 - AssertJ — fluent assertions]], [[04 - Testes parametrizados e organização]], verbetes `JUnit 5 (Jupiter)`/`AAA (Arrange-Act-Assert)`.

- [ ] **Step 3: Verificar** — ≥7 seções; anti-fabricação VAZIO; `grep -i "BeforeEach\|@DisplayName"` ≥2.

- [ ] **Step 4: Commit** — `git commit -m "feat(java): galho 13 nota 02 — JUnit 5 (anatomia, lifecycle e o padrão AAA)"`

### Task 3: Nota 03 — AssertJ — fluent assertions

**Files:**
- Create: `03-Dominios/Tecnologia/Java/Testes/03 - AssertJ — fluent assertions.md`

- [ ] **Step 1: Pesquisar** — WebFetch `https://assertj.github.io/doc/#assertj-core`. CONFIRMAR: `assertThat(...)` encadeado pra String/Number/Collection/Map/Optional; `extracting`; `assertThatThrownBy`/`catchThrowable`/`assertThatExceptionOfType`/`assertThatNoException`; `SoftAssertions.assertSoftly`; `usingRecursiveComparison().ignoringFields(...)`.

- [ ] **Step 2: Escrever** — `fase: iniciado`, tags `[java, testes, iniciado, assertj]`. Conteúdo:
  - TL;DR: AssertJ dá asserções fluent (`assertThat(x).isNotNull().hasSize(3).contains(...)`) muito mais legíveis que JUnit built-in/Hamcrest, com mensagens de erro claras; é o padrão moderno (vem no starter).
  - H3s: "assertThat encadeado: String/Number/Collection/Map/Optional", "extracting: projetar campos antes de asserir", "Exception assertions: assertThatThrownBy / catchThrowable", "Soft assertions: acumular falhas em vez de parar na primeira", "usingRecursiveComparison: comparar objetos campo a campo (ignorando id/timestamps)".
  - `## Na prática` — asserções sobre `List<Order>` (`extracting(Order::total)`), exception assertion, soft, recursive comparison `ignoringFields("id", "createdAt")` (```java). Domínios neutros.
  - `## Armadilhas` — ≥2: (1) `assertTrue(x.equals(y))` em vez de `assertThat(x).isEqualTo(y)` (mensagem de falha inútil); (2) parar na 1ª falha quando 3 asserções independentes deviam ser soft.
  - `## Veja também` — [[02 - JUnit 5 — anatomia, lifecycle e o padrão AAA]], [[06 - Mockito — mocks, stubbing e matchers]], verbetes `AssertJ`/`soft assertions`/`usingRecursiveComparison`.

- [ ] **Step 3: Verificar** — ≥7 seções; anti-fabricação VAZIO; `grep -i "assertThat\|assertThatThrownBy"` ≥3.

- [ ] **Step 4: Commit** — `git commit -m "feat(java): galho 13 nota 03 — AssertJ (fluent assertions)"`

### Task 4: Nota 04 — Testes parametrizados e organização

**Files:**
- Create: `03-Dominios/Tecnologia/Java/Testes/04 - Testes parametrizados e organização.md`

- [ ] **Step 1: Pesquisar** — WebFetch `https://junit.org/junit5/docs/current/user-guide/#writing-tests-parameterized-tests`. CONFIRMAR: `@ParameterizedTest` + `@ValueSource`/`@CsvSource`/`@MethodSource`/`@EnumSource`/`@CsvFileSource`; `@Nested`; `@Tag` + Surefire `-Dgroups`/`-DexcludedGroups`; `@ExtendWith`.

- [ ] **Step 2: Escrever** — `fase: iniciado`, tags `[java, testes, iniciado, junit, parametrizados]`. Conteúdo:
  - TL;DR: `@ParameterizedTest` roda o mesmo teste com vários inputs (de `@ValueSource`/`@CsvSource`/`@MethodSource`); `@Nested` agrupa cenários; `@Tag` permite execução seletiva no CI.
  - H3s: "@ParameterizedTest + sources (ValueSource/CsvSource/MethodSource/EnumSource)", "@Nested: agrupar cenários relacionados", "@Tag e execução seletiva (unit vs slow vs integration)", "@ExtendWith: o ponto de extensão do JUnit 5".
  - `## Na prática` — um `@ParameterizedTest @CsvSource` classificando `OrderStatus`, um `@MethodSource` com `Stream<String>`, um `@Nested` "when order is pending" (```java + ```bash do Surefire). Neutros.
  - `## Armadilhas` — ≥2: (1) `@MethodSource` apontando método de instância sem PER_CLASS (precisa static ou PER_CLASS); (2) teste parametrizado escondendo casos que mereciam testes nomeados distintos.
  - `## Veja também` — [[02 - JUnit 5 — anatomia, lifecycle e o padrão AAA]], [[05 - Test data builders e fixtures]], verbetes `@ParameterizedTest`/`@Nested`.

- [ ] **Step 3: Verificar** — ≥7 seções; anti-fabricação VAZIO; `grep -i "ParameterizedTest\|@Nested"` ≥2.

- [ ] **Step 4: Commit** — `git commit -m "feat(java): galho 13 nota 04 — testes parametrizados e organização"`

### Task 5: Nota 05 — Test data builders e fixtures

**Files:**
- Create: `03-Dominios/Tecnologia/Java/Testes/05 - Test data builders e fixtures.md`

- [ ] **Step 1: Pesquisar** — WebFetch `https://www.instancio.org/` (menção). Resto vem do tronco higienizado (o padrão builder é estável, não version-specific).

- [ ] **Step 2: Escrever** — `fase: iniciado`, tags `[java, testes, iniciado]`. Conteúdo:
  - TL;DR: builders de dados de teste (`anOrder().withTotal(...).build()`) evitam construtores de 15 argumentos e setup duplicado, deixando o teste legível e focado no que importa; bibliotecas como Instancio geram objetos com defaults automáticos.
  - H3s: "O builder / object mother: defaults sensatos + overrides", "Métodos semânticos (asPaid(), asCancelled()) que expressam intenção", "@BeforeEach vs builder: quando cada um", "Geração automática: Instancio (menção)".
  - `## Na prática` — um `OrderBuilder` neutro (`anOrder()`, `withCustomer`, `asPaid`, `build`) + uso num teste (```java).
  - `## Armadilhas` — ≥2: (1) builder mutável compartilhado (estático) entre testes (vaza estado); (2) fixture gigante "pra tudo" (cada teste carrega dado irrelevante — prefira builders específicos).
  - `## Veja também` — [[04 - Testes parametrizados e organização]], [[06 - Mockito — mocks, stubbing e matchers]], [[21 - Capstone — a estratégia de testes de uma app Spring production-grade]], verbete `test data builder`.

- [ ] **Step 3: Verificar** — ≥7 seções; anti-fabricação VAZIO (o tronco tem `PatientBuilder` — usar `OrderBuilder`); ≥2 armadilhas.

- [ ] **Step 4: Commit** — `git commit -m "feat(java): galho 13 nota 05 — test data builders e fixtures"`

---

## Fase ADEPTO (notas 06-12)

### Task 6: Nota 06 — Mockito — mocks, stubbing e matchers ⟦opus⟧

**Files:**
- Create: `03-Dominios/Tecnologia/Java/Testes/06 - Mockito — mocks, stubbing e matchers.md`

- [ ] **Step 1: Pesquisar (version-specific)** — WebFetch `https://javadoc.io/doc/org.mockito/mockito-core/latest/index.html` + `https://site.mockito.org/`. CONFIRMAR: `@ExtendWith(MockitoExtension.class)`, `@Mock`/`@InjectMocks`; `when(...).thenReturn/thenThrow/thenAnswer`; `doNothing/doThrow/doAnswer().when()` pra void; matchers (`any`/`any(Type.class)`/`eq`/`anyString`/`argThat`/`intThat`); a regra "se usa matcher num arg, todos são matchers"; mock vs spy vs fake vs stub; versão atual Mockito 5.x. **WebFetch obrigatório.**

- [ ] **Step 2: Escrever** — `fase: adepto`, tags `[java, testes, adepto, mockito]`. **A nota densa de mocks.** ≥3 H3s: "Mock vs spy vs fake vs stub (e qual usar)", "@Mock / @InjectMocks / MockitoExtension", "Stubbing: when().thenReturn/thenThrow/thenAnswer e doX().when() pra void", "Argument matchers e a regra 'todos ou nenhum'". `## Na prática` — um `OrderServiceTest` com `@Mock OrderRepository`/`@Mock NotificationSender`/`@InjectMocks OrderService`, stubbing e matchers (```java). Neutros. `## Armadilhas` ≥3: (1) `when(spy).thenReturn` com side effect (use `doReturn().when(spy)`); (2) misturar matcher e literal (`foo(eq(1), matcher)` ok, `foo(1, matcher)` falha); (3) stub não usado (`UnnecessaryStubbingException` no strict). `## Veja também` — [[07 - Mockito — verify, ArgumentCaptor e quando NÃO mockar]], [[03 - AssertJ — fluent assertions]], verbetes `Mockito`/`mock vs spy vs fake vs stub`/`InjectMocks`.

- [ ] **Step 3: Verificar** — ≥7 seções; ≥3 armadilhas; anti-fabricação VAZIO; `grep -i "@Mock\|when("` ≥3.

- [ ] **Step 4: Commit** — `git commit -m "feat(java): galho 13 nota 06 — Mockito (mocks, stubbing e matchers)"`

### Task 7: Nota 07 — Mockito — verify, ArgumentCaptor e quando NÃO mockar

**Files:**
- Create: `03-Dominios/Tecnologia/Java/Testes/07 - Mockito — verify, ArgumentCaptor e quando NÃO mockar.md`

- [ ] **Step 1: Pesquisar (version-specific)** — WebFetch `https://javadoc.io/doc/org.mockito/mockito-core/latest/index.html` (Mockito javadoc — verify/ArgumentCaptor/mockStatic). CONFIRMAR: `verify(mock, times/never/atLeast/atMost)`, `InOrder`, `verifyNoMoreInteractions`/`verifyNoInteractions`; `ArgumentCaptor.forClass`/`.capture()`/`.getValue()`; static mocking `mockStatic(...)` em try-with-resources (Mockito 5+, sem PowerMock); anti-patterns. **WebFetch obrigatório.**

- [ ] **Step 2: Escrever** — `fase: adepto`, tags `[java, testes, adepto, mockito]`. ≥3 H3s: "verify: times/never/atLeast + InOrder + verifyNoMoreInteractions", "ArgumentCaptor: capturar e asserir o argumento", "Static mocking sem PowerMock (mockStatic, Mockito 5+)", "Quando NÃO mockar: value objects, código testável (injetar Clock/Supplier)". `## Na prática` — `verify(repository).save(captor.capture())` + assert no capturado; `mockStatic(Instant.class)` em try-with-resources; injeção de `Clock` pra testar tempo (```java). Neutros (`OrderService` com `Clock`). `## Armadilhas` ≥3: (1) `verify(repo, times(3)).save(any())` acoplado à implementação (verifique efeito observável); (2) mockar value object (`mock(Order.class)` — use real); (3) `mockStatic` sem try-with-resources (vaza o mock pra outros testes). `## Veja também` — [[06 - Mockito — mocks, stubbing e matchers]], [[14 - Testando código assíncrono — Awaitility]], verbetes `verify (Mockito)`/`ArgumentCaptor`.

- [ ] **Step 3: Verificar** — ≥7 seções; ≥3 armadilhas; anti-fabricação VAZIO; `grep -i "verify\|ArgumentCaptor"` ≥2.

- [ ] **Step 4: Commit** — `git commit -m "feat(java): galho 13 nota 07 — Mockito (verify, ArgumentCaptor e quando não mockar)"`

### Task 8: Nota 08 — Spring Boot Test e os slices — o contexto de teste

**Files:**
- Create: `03-Dominios/Tecnologia/Java/Testes/08 - Spring Boot Test e os slices — o contexto de teste.md`

- [ ] **Step 1: Pesquisar (version-specific)** — WebFetch `https://docs.spring.io/spring-boot/reference/testing/spring-boot-applications.html`. CONFIRMAR: a tabela de slices (`@SpringBootTest`/`@WebMvcTest`/`@DataJpaTest`/`@JsonTest`/`@RestClientTest`/`@WebFluxTest`/`@JdbcTest`/`@DataRedisTest`); `@SpringBootTest` (contexto completo) vs slices (parcial); **caching do contexto de teste** (mesma config → reusa); **`@MockitoBean` (Boot 3.4+) substituiu `@MockBean`** (deprecated); `@ActiveProfiles`. **WebFetch obrigatório.**

- [ ] **Step 2: Escrever** — `fase: adepto`, tags `[java, testes, adepto, spring-test]`. **Liga o container do G8.** ≥3 H3s: "Os slices: tabela do que cada um carrega", "@SpringBootTest (contexto completo) vs slice (parcial)", "O contexto de teste é um ApplicationContext — e o cache que acelera a suíte (Galho 8)", "@MockitoBean (substituiu @MockBean) e @ActiveProfiles". `## Na prática` — a tabela de slices; um `@SpringBootTest @ActiveProfiles("test")` + um `@WebMvcTest` com `@MockitoBean` lado a lado (```java). Linka **G8** (ApplicationContext/auto-config). `## Armadilhas` ≥3: (1) `@SpringBootTest` pra testar um método (carrega o mundo — use slice ou sem Spring); (2) config diferente por teste quebra o cache do contexto (suíte lenta); (3) `@MockBean` (deprecated — use `@MockitoBean`). `## Veja também` — [[09 - @WebMvcTest — testando controllers com MockMvc]], [[10 - @DataJpaTest — testando repositories]], **[[03-Dominios/Tecnologia/Java/Spring Core e Boot/06 - ApplicationContext — o container e seu ciclo|ApplicationContext]]**, **[[03-Dominios/Tecnologia/Java/Spring Core e Boot/15 - Auto-configuration e starters|Auto-configuration e starters]]**, verbetes `test slice (Spring Boot)`/`@SpringBootTest`/`@MockitoBean`.

- [ ] **Step 3: Verificar** — ≥7 seções; ≥3 armadilhas; anti-fabricação VAZIO; `grep -c "Spring Core e Boot/06"` ≥1; `grep -i "@MockitoBean"` ≥1.

- [ ] **Step 4: Commit** — `git commit -m "feat(java): galho 13 nota 08 — Spring Boot Test e os slices (o contexto de teste)"`

### Task 9: Nota 09 — @WebMvcTest — testando controllers com MockMvc ⟦opus⟧

**Files:**
- Create: `03-Dominios/Tecnologia/Java/Testes/09 - @WebMvcTest — testando controllers com MockMvc.md`

- [ ] **Step 1: Pesquisar (version-specific)** — WebFetch `https://docs.spring.io/spring-boot/reference/testing/spring-boot-applications.html#testing.spring-boot-applications.spring-mvc-tests` + `https://docs.spring.io/spring-framework/reference/testing/mockmvc/`. CONFIRMAR: `@WebMvcTest(OrderController.class)` carrega só web (controllers/advice/filters/converters, NÃO services/repos); `MockMvc.perform(get(...)).andExpect(status().isOk()).andExpect(jsonPath(...))`; `@MockitoBean` no service; testar 404/422/validação. **WebFetch obrigatório.**

- [ ] **Step 2: Escrever** — `fase: adepto`, tags `[java, testes, adepto, spring-test, webmvctest]`. **A face G9 da convergência.** ≥3 H3s: "@WebMvcTest carrega só a web layer (e o que NÃO carrega)", "MockMvc: perform + andExpect (status / jsonPath)", "Mockar o service com @MockitoBean", "Testar 200 / 404 / 422 / validação". `## Na prática` — `@WebMvcTest(OrderController.class)` com `@Autowired MockMvc`, `@MockitoBean OrderService`, testes de `get`/`post` com `jsonPath` (```java). Neutros. Linka **G9** (testa o pipeline do DispatcherServlet/controllers). `## Armadilhas` ≥3: (1) esperar que service/repo reais carreguem (não carregam — mocke); (2) testar serialização complexa aqui em vez de `@JsonTest`; (3) confundir `MockMvc` (sem servidor) com servidor real. `## Veja também` — [[08 - Spring Boot Test e os slices — o contexto de teste]], [[12 - Testes de integração ponta a ponta]], [[13 - Testando a segurança]], **[[03-Dominios/Tecnologia/Java/Web e APIs REST/02 - @RestController e os mapeamentos|@RestController e os mapeamentos]]**, **[[03-Dominios/Tecnologia/Java/Web e APIs REST/06 - O pipeline do DispatcherServlet|O pipeline do DispatcherServlet]]**, **[[03-Dominios/Tecnologia/Java/Web e APIs REST/09 - Tratamento de exceções com @ControllerAdvice|Tratamento de exceções com @ControllerAdvice]]**, verbetes `@WebMvcTest`/`MockMvc`.

- [ ] **Step 3: Verificar** — ≥7 seções; ≥3 armadilhas; anti-fabricação VAZIO; `grep -c "Web e APIs REST/0(2|6|9)"` ≥1; `grep -i "MockMvc\|jsonPath"` ≥2.

- [ ] **Step 4: Commit** — `git commit -m "feat(java): galho 13 nota 09 — @WebMvcTest (testando controllers com MockMvc)"`

### Task 10: Nota 10 — @DataJpaTest — testando repositories ⟦opus⟧

**Files:**
- Create: `03-Dominios/Tecnologia/Java/Testes/10 - @DataJpaTest — testando repositories.md`

- [ ] **Step 1: Pesquisar (version-specific)** — WebFetch `https://docs.spring.io/spring-boot/reference/testing/spring-boot-applications.html#testing.spring-boot-applications.autoconfigured-spring-data-jpa`. CONFIRMAR: `@DataJpaTest` carrega só JPA; `TestEntityManager` (`persist`/`flush`); transação + **rollback automático** por teste; default substitui datasource por H2 — `@AutoConfigureTestDatabase(replace = Replace.NONE)` pra usar banco real (Testcontainers). **WebFetch obrigatório.**

- [ ] **Step 2: Escrever** — `fase: adepto`, tags `[java, testes, adepto, spring-test, datajpatest]`. **A face G10 da convergência (paga a dívida).** ≥3 H3s: "@DataJpaTest carrega só a camada JPA", "TestEntityManager: persist/flush sem passar pelo repositório", "Transação + rollback automático por teste", "H2 default vs banco real (Replace.NONE + Testcontainers)". `## Na prática` — `@DataJpaTest @AutoConfigureTestDatabase(replace=Replace.NONE)` + `@Container PostgreSQLContainer` + `@ServiceConnection` + `TestEntityManager` testando uma derived query do `OrderRepository` (```java). Neutros. Linka **G10**. `## Armadilhas` ≥3: (1) H2 default escondendo bug de dialeto (JSONB/funções Postgres — use Testcontainers); (2) assumir commit (é rollback — o dado some); (3) testar derived query sem `em.flush()` antes (a query não vê o persist). `## Veja também` — [[11 - Testcontainers — infra real em testes]], [[08 - Spring Boot Test e os slices — o contexto de teste]], **[[03-Dominios/Tecnologia/Java/Persistência de dados/04 - Spring Data repositories — JpaRepository e query methods derivados|Spring Data repositories]]**, **[[03-Dominios/Tecnologia/Java/Persistência de dados/09 - Consultas com @Query — JPQL, native e @Modifying|Consultas com @Query]]**, verbetes `@DataJpaTest`/`TestEntityManager`.

- [ ] **Step 3: Verificar** — ≥7 seções; ≥3 armadilhas; anti-fabricação VAZIO; `grep -c "Persistência de dados/0(4|9)"` ≥1; `grep -i "TestEntityManager\|Replace.NONE"` ≥1.

- [ ] **Step 4: Commit** — `git commit -m "feat(java): galho 13 nota 10 — @DataJpaTest (testando repositories)"`

### Task 11: Nota 11 — Testcontainers — infra real em testes

**Files:**
- Create: `03-Dominios/Tecnologia/Java/Testes/11 - Testcontainers — infra real em testes.md`

- [ ] **Step 1: Pesquisar (version-specific)** — WebFetch `https://java.testcontainers.org/` + `https://docs.spring.io/spring-boot/reference/testing/testcontainers.html`. CONFIRMAR: por que não H2; `@Testcontainers` + `@Container`; **`@ServiceConnection` (Boot 3.1+)** auto-configura datasource/conexões; singleton pattern (static container, sem stop) + `withReuse(true)` (`~/.testcontainers.properties` `testcontainers.reuse.enable=true`, só dev); módulos (Postgres/MySQL/Kafka/Redis/LocalStack). **WebFetch obrigatório.**

- [ ] **Step 2: Escrever** — `fase: adepto`, tags `[java, testes, adepto, testcontainers]`. ≥3 H3s: "Por que Testcontainers > H2 (dialeto SQL/JSONB diverge → falso-positivo)", "@Testcontainers + @Container + @ServiceConnection (Boot 3.1+)", "Singleton pattern e reuse (acelerar o ciclo local)", "Módulos prontos (Postgres, Kafka, Redis, LocalStack)". `## Na prática` — um container Postgres static + `@ServiceConnection`; e o singleton pattern (```java + ```properties do reuse). Linka **G10**. `## Armadilhas` ≥3: (1) container por método de teste (lento — use static/singleton); (2) esquecer Docker disponível no CI; (3) `withReuse(true)` no CI (é só pra dev local — no CI gera lixo). `## Veja também` — [[10 - @DataJpaTest — testando repositories]], [[12 - Testes de integração ponta a ponta]], **[[03-Dominios/Tecnologia/Java/Persistência de dados/04 - Spring Data repositories — JpaRepository e query methods derivados|Spring Data repositories]]**, verbetes `Testcontainers`/`@ServiceConnection`/`H2 (vs Testcontainers)`.

- [ ] **Step 3: Verificar** — ≥7 seções; ≥3 armadilhas; anti-fabricação VAZIO; `grep -i "@ServiceConnection\|Testcontainers"` ≥2.

- [ ] **Step 4: Commit** — `git commit -m "feat(java): galho 13 nota 11 — Testcontainers (infra real em testes)"`

### Task 12: Nota 12 — Testes de integração ponta a ponta ⟦opus⟧

**Files:**
- Create: `03-Dominios/Tecnologia/Java/Testes/12 - Testes de integração ponta a ponta.md`

- [ ] **Step 1: Pesquisar (version-specific)** — WebFetch `https://docs.spring.io/spring-boot/reference/testing/spring-boot-applications.html`. CONFIRMAR: `@SpringBootTest(webEnvironment=RANDOM_PORT)` + `@AutoConfigureMockMvc`; `WebEnvironment` (MOCK/RANDOM_PORT/DEFINED_PORT/NONE); `TestRestTemplate` vs `WebTestClient` vs `MockMvc`; `@DynamicPropertySource`; múltiplos containers. **WebFetch obrigatório.**

- [ ] **Step 2: Escrever** — `fase: adepto`, tags `[java, testes, adepto, integracao, testcontainers]`. ≥3 H3s: "@SpringBootTest: o contexto completo + WebEnvironment (MOCK/RANDOM_PORT/...)", "Múltiplos containers (Postgres + Redis + Kafka) num teste", "MockMvc vs WebTestClient vs TestRestTemplate", "@DynamicPropertySource: apontar config pros containers". `## Na prática` — um `@SpringBootTest(RANDOM_PORT)` + 2 containers + `@ServiceConnection` + um fluxo `post` → verificar no banco via repositório (```java). Neutros. `## Armadilhas` ≥3: (1) integração demais (pirâmide invertida — suíte lenta); (2) estado vazando entre testes (sem rollback/reset — `@SpringBootTest` não dá rollback automático como `@DataJpaTest`); (3) porta fixa (`DEFINED_PORT` colide no CI — use RANDOM_PORT). `## Veja também` — [[11 - Testcontainers — infra real em testes]], [[09 - @WebMvcTest — testando controllers com MockMvc]], [[21 - Capstone — a estratégia de testes de uma app Spring production-grade]], verbetes `@SpringBootTest`/`WebTestClient`.

- [ ] **Step 3: Verificar** — ≥7 seções; ≥3 armadilhas; anti-fabricação VAZIO; `grep -i "RANDOM_PORT\|@DynamicPropertySource"` ≥1.

- [ ] **Step 4: Commit** — `git commit -m "feat(java): galho 13 nota 12 — testes de integração ponta a ponta"`

---

## Fase MAGUS (notas 13-21)

### Task 13: Nota 13 — Testando a segurança

**Files:**
- Create: `03-Dominios/Tecnologia/Java/Testes/13 - Testando a segurança.md`

- [ ] **Step 1: Pesquisar (version-specific)** — WebFetch `https://docs.spring.io/spring-security/reference/servlet/test/index.html` + `.../test/mockmvc/index.html`. CONFIRMAR: `spring-security-test`; `@WithMockUser`/`@WithUserDetails`; `SecurityMockMvcRequestPostProcessors.jwt()`/`.csrf()`/`.user()`; testar 401 (não-autenticado) vs 403 (não-autorizado); method security em teste. **WebFetch obrigatório.**

- [ ] **Step 2: Escrever** — `fase: magus`, tags `[java, testes, magus, spring-test]`. **A face G12 (paga a dívida da nota 18 do Segurança).** ≥3 H3s: "@WithMockUser / @WithUserDetails: identidade simulada", "with(jwt()) / with(csrf()): post-processors do MockMvc", "Testar 401 vs 403 (não-autenticado vs não-autorizado)", "Testar method security (@PreAuthorize)". `## Na prática` — `@WebMvcTest` + `@WithMockUser(roles="ADMIN")` testando endpoint protegido; `mockMvc.perform(post(...).with(csrf()))`; `.with(jwt().authorities(...))` (```java). Neutros (`User`/`Role`). Linka **G12**. `## Armadilhas` ≥3: (1) testar endpoint protegido sem auth e estranhar 401 (configure `@WithMockUser`); (2) esquecer `with(csrf())` num POST com CSRF ligado (403); (3) `@WithMockUser` sem method security habilitado no slice (a anotação não dispara). `## Veja também` — [[09 - @WebMvcTest — testando controllers com MockMvc]], [[12 - Testes de integração ponta a ponta]], **[[03-Dominios/Tecnologia/Java/Segurança/05 - Autorização baseada em URL — authorizeHttpRequests, roles vs authorities|Autorização baseada em URL]]**, **[[03-Dominios/Tecnologia/Java/Segurança/07 - Method security — @PreAuthorize, @PostAuthorize e SpEL|Method security]]**, verbete `@WithMockUser`.

- [ ] **Step 3: Verificar** — ≥7 seções; ≥3 armadilhas; anti-fabricação VAZIO; `grep -c "Segurança/0(5|7)"` ≥1; `grep -i "@WithMockUser"` ≥1.

- [ ] **Step 4: Commit** — `git commit -m "feat(java): galho 13 nota 13 — testando a segurança"`

### Task 14: Nota 14 — Testando código assíncrono — Awaitility

**Files:**
- Create: `03-Dominios/Tecnologia/Java/Testes/14 - Testando código assíncrono — Awaitility.md`

- [ ] **Step 1: Pesquisar** — WebFetch `https://github.com/awaitility/awaitility/wiki/Usage`. CONFIRMAR: `Awaitility.await().atMost(...).pollInterval(...).untilAsserted(() -> ...)`; `until(...)` com Callable; por que substitui `Thread.sleep`.

- [ ] **Step 2: Escrever** — `fase: magus`, tags `[java, testes, magus, awaitility]`. **Liga G4 (concorrência/async).** ≥3 H3s: "Consistência eventual: o efeito acontece 'depois' (async)", "await().atMost().untilAsserted: polling declarativo", "Nunca Thread.sleep (flakiness garantida)", "Configurar pollInterval e timeout para o CI". `## Na prática` — um teste que dispara um processamento assíncrono e usa `await().atMost(5, SECONDS).untilAsserted(() -> assertThat(repo.findById(id)).isPresent())` (```java). Neutros (`Order` processado async). Linka **G4** (o código concorrente). `## Armadilhas` ≥3: (1) `Thread.sleep(2000)` (flaky — lento quando passa, falha quando o CI está lento); (2) timeout curto demais (flaky no CI carregado); (3) `until()` sem assert que valida o estado (passa cedo demais). `## Veja também` — [[15 - Testando código reativo — StepVerifier e @WebFluxTest]], [[07 - Mockito — verify, ArgumentCaptor e quando NÃO mockar]], **[[03-Dominios/Tecnologia/Java/Concorrência e paralelismo/index|Concorrência e paralelismo]]**, verbete `Awaitility`.

- [ ] **Step 3: Verificar** — ≥7 seções; ≥3 armadilhas; anti-fabricação VAZIO; `grep -c "Concorrência e paralelismo/index"` ≥1; `grep -i "await\|Awaitility"` ≥2.

- [ ] **Step 4: Commit** — `git commit -m "feat(java): galho 13 nota 14 — testando código assíncrono (Awaitility)"`

### Task 15: Nota 15 — Testando código reativo — StepVerifier e @WebFluxTest ⟦opus⟧

**Files:**
- Create: `03-Dominios/Tecnologia/Java/Testes/15 - Testando código reativo — StepVerifier e @WebFluxTest.md`

- [ ] **Step 1: Pesquisar (version-specific)** — WebFetch `https://projectreactor.io/docs/core/release/reference/#testing` + `https://docs.spring.io/spring-boot/reference/testing/spring-boot-applications.html` (@WebFluxTest). CONFIRMAR: `reactor-test`; `StepVerifier.create(flux).expectNext(...).expectError(...).verifyComplete()`; `expectNextCount`; `StepVerifier.withVirtualTime(...)` pra tempo; `@WebFluxTest` + `WebTestClient`. **WebFetch obrigatório.**

- [ ] **Step 2: Escrever** — `fase: magus`, tags `[java, testes, magus, stepverifier, spring-test]`. **A face G11 (paga a dívida do StepVerifier).** ≥3 H3s: "StepVerifier: o JUnit do reativo (expectNext/expectError/verifyComplete)", "expectNextCount e asserções sobre o fluxo", "withVirtualTime: testar delays sem esperar de verdade", "@WebFluxTest + WebTestClient: testar reactive controllers". `## Na prática` — `StepVerifier.create(orderService.findAll()).expectNextCount(3).verifyComplete()`; um `@WebFluxTest` com `WebTestClient` (```java). Neutros (`Flux<Order>`). Linka **G11**. `## Armadilhas` ≥3: (1) `block()` no teste em vez de `StepVerifier` (perde a natureza reativa); (2) esquecer `verifyComplete()`/`.verify()` (não assina — o teste passa sem rodar nada); (3) testar um delay com tempo real (lento — use `withVirtualTime`). `## Veja também` — [[14 - Testando código assíncrono — Awaitility]], [[12 - Testes de integração ponta a ponta]], **[[03-Dominios/Tecnologia/Java/Programação Reativa/10 - Spring WebFlux — o stack não-bloqueante sobre Netty e o DispatcherHandler|Spring WebFlux]]**, **[[03-Dominios/Tecnologia/Java/Programação Reativa/11 - WebClient — o cliente HTTP reativo a fundo|WebClient]]**, verbetes `StepVerifier`/`@WebFluxTest`/`WebTestClient`.

- [ ] **Step 3: Verificar** — ≥7 seções; ≥3 armadilhas; anti-fabricação VAZIO; `grep -c "Programação Reativa/1(0|1)"` ≥1; `grep -i "StepVerifier"` ≥2.

- [ ] **Step 4: Commit** — `git commit -m "feat(java): galho 13 nota 15 — testando código reativo (StepVerifier e @WebFluxTest)"`

### Task 16: Nota 16 — Mockando HTTP externo — WireMock e MockRestServiceServer

**Files:**
- Create: `03-Dominios/Tecnologia/Java/Testes/16 - Mockando HTTP externo — WireMock e MockRestServiceServer.md`

- [ ] **Step 1: Pesquisar** — WebFetch `https://wiremock.org/docs/` + `https://docs.spring.io/spring-boot/reference/testing/spring-boot-applications.html` (@RestClientTest). CONFIRMAR: WireMock (`stubFor(get(...).willReturn(...))`, `verify(getRequestedFor(...))`, cenários/`inScenario`, `dynamicPort`, `@DynamicPropertySource` pra apontar base-url); `@RestClientTest` + `MockRestServiceServer`.

- [ ] **Step 2: Escrever** — `fase: magus`, tags `[java, testes, magus, wiremock, spring-test]`. ≥3 H3s: "Por que mockar o HTTP externo (não depender da API real)", "WireMock: stubFor / verify / cenários (retry)", "@DynamicPropertySource: apontar o client pro WireMock", "@RestClientTest + MockRestServiceServer (alternativa Spring pra RestClient/RestTemplate)". `## Na prática` — um `WireMockServer` com `stubFor` + `@DynamicPropertySource` apontando `external.api.base-url`; e um `@RestClientTest` com `MockRestServiceServer` (```java). Neutros (`ExternalOrderClient`). Linka **G9** (clientes HTTP). `## Armadilhas` ≥3: (1) porta fixa do WireMock (colisão no CI — use `dynamicPort()`); (2) não verificar que a chamada aconteceu (`wireMock.verify(...)`); (3) mockar o client em vez do transporte HTTP (perde o teste da serialização/URL). `## Veja também` — [[09 - @WebMvcTest — testando controllers com MockMvc]], [[12 - Testes de integração ponta a ponta]], **[[03-Dominios/Tecnologia/Java/Web e APIs REST/15 - Clientes HTTP — RestClient, WebClient, RestTemplate|Clientes HTTP]]**, verbetes `WireMock`/`MockRestServiceServer`.

- [ ] **Step 3: Verificar** — ≥7 seções; ≥3 armadilhas; anti-fabricação VAZIO; `grep -c "Web e APIs REST/15"` ≥1; `grep -i "WireMock\|stubFor"` ≥2.

- [ ] **Step 4: Commit** — `git commit -m "feat(java): galho 13 nota 16 — mockando HTTP externo (WireMock e MockRestServiceServer)"`

### Task 17: Nota 17 — Mutation testing — PIT e cobertura honesta

**Files:**
- Create: `03-Dominios/Tecnologia/Java/Testes/17 - Mutation testing — PIT e cobertura honesta.md`

- [ ] **Step 1: Pesquisar (version-specific)** — WebFetch `https://pitest.org/` + `https://pitest.org/quickstart/maven/`. CONFIRMAR: PIT muta o bytecode (mutadores: condicional, return, incremento); roda os testes contra o mutante; mutante sobrevive = teste fraco; `pitest-maven` + `pitest-junit5-plugin`; mutation coverage > line coverage; lento (nightly).

- [ ] **Step 2: Escrever** — `fase: magus`, tags `[java, testes, magus, pit]`. ≥3 H3s: "Line coverage mente (100% sem asserção é inútil)", "Mutation testing: PIT muta o bytecode e mede se os testes pegam", "Mutante sobrevivente = teste fraco; mutante morto = teste bom", "Custo: rodar no nightly, não em cada build". `## Na prática` — o plugin `pitest-maven` + `pitest-junit5-plugin` (```xml); `mvn org.pitest:pitest-maven:mutationCoverage` (```bash); explicação de uma mutação (`>` → `>=`). `## Armadilhas` ≥3: (1) line coverage como meta de PR (passa sem asserção); (2) rodar PIT em cada build (lento — nightly); (3) ignorar mutantes sobreviventes (são exatamente os bugs que escapam). `## Veja também` — [[18 - Performance — JMH e microbenchmarks]], [[01 - O que é testar em Java — a pirâmide e o stack moderno]], [[21 - Capstone — a estratégia de testes de uma app Spring production-grade]], verbetes `mutation testing`/`PIT (Pitest)`.

- [ ] **Step 3: Verificar** — ≥7 seções; ≥3 armadilhas; anti-fabricação VAZIO; `grep -i "mutation\|PIT\|pitest"` ≥2.

- [ ] **Step 4: Commit** — `git commit -m "feat(java): galho 13 nota 17 — mutation testing (PIT e cobertura honesta)"`

### Task 18: Nota 18 — Performance — JMH e microbenchmarks

**Files:**
- Create: `03-Dominios/Tecnologia/Java/Testes/18 - Performance — JMH e microbenchmarks.md`

- [ ] **Step 1: Pesquisar** — WebFetch `https://github.com/openjdk/jmh`. CONFIRMAR: `@Benchmark`/`@BenchmarkMode`/`@Warmup`/`@Measurement`/`@Fork`/`@State`/`@Param`; `Blackhole` pra consumir resultado (anti dead-code elimination); por que `System.nanoTime()` num `@Test` mente (warmup, JIT, dead-code, constant folding).

- [ ] **Step 2: Escrever** — `fase: magus`, tags `[java, testes, magus, jmh]`. **Liga G3 (o JIT).** ≥3 H3s: "Por que medir performance num @Test mente (warmup, JIT, dead-code elimination, constant folding)", "JMH: @Benchmark / @Warmup / @Measurement / @Fork / @State", "@Param: variar o tamanho do input", "Blackhole: consumir o resultado pra o JIT não eliminar". `## Na prática` — um `StringConcatBenchmark` (`+` vs `StringBuilder`) com as anotações JMH (```java). Linka **G3** (o JIT que torna o microbenchmark traiçoeiro). `## Armadilhas` ≥3: (1) `System.nanoTime()` num `@Test` (o JIT engana); (2) sem warmup (mede a JVM fria/interpretada); (3) resultado não consumido (dead-code elimination apaga o cálculo — use `Blackhole`/return). `## Veja também` — [[17 - Mutation testing — PIT e cobertura honesta]], **[[03-Dominios/Tecnologia/Java/JVM/07 - O compilador JIT — C1, C2 e a compilação adaptativa|O compilador JIT]]**, verbete `JMH (microbenchmark)`. **Profiling de produção = Galho 17 (texto "(planejado)", sem wikilink).**

- [ ] **Step 3: Verificar** — ≥7 seções; ≥3 armadilhas; anti-fabricação VAZIO; `grep -c "JVM/07"` ≥1; `grep -i "JMH\|@Benchmark"` ≥2.

- [ ] **Step 4: Commit** — `git commit -m "feat(java): galho 13 nota 18 — performance (JMH e microbenchmarks)"`

### Task 19: Nota 19 — Fitness functions — ArchUnit (testes de arquitetura) ⟦opus⟧

**Files:**
- Create: `03-Dominios/Tecnologia/Java/Testes/19 - Fitness functions — ArchUnit (testes de arquitetura).md`

- [ ] **Step 1: Pesquisar (version-specific)** — WebFetch `https://www.archunit.org/userguide/html/000_Index.html`. CONFIRMAR: `@AnalyzeClasses(packages=...)` + `@ArchTest static final ArchRule`; `noClasses().that().resideInAPackage("..controller..").should().dependOnClassesThat()...`; `layeredArchitecture()`; `slices().should().beFreeOfCycles()`; convenções (nome/anotação). **WebFetch obrigatório.**

- [ ] **Step 2: Escrever** — `fase: magus`, tags `[java, testes, magus, archunit]`. ≥3 H3s: "Fitness function: regra de arquitetura como teste que falha o build", "Dependências entre camadas (noClasses / layeredArchitecture)", "Sem ciclos entre pacotes (slices().beFreeOfCycles())", "Convenções: nome de classe, anotação obrigatória". `## Na prática` — um `ArchitectureTest` com `@AnalyzeClasses` + regras "controllers não dependem de repositories", `layeredArchitecture()`, `no_cycles` (```java). Neutros (`..controller..`/`..service..`/`..repository..`). `## Armadilhas` ≥3: (1) regra acoplada a nome de pacote literal frágil (refator quebra); (2) ArchUnit que não roda no CI (vira decoração); (3) regra críptica sem mensagem (ninguém entende a falha). `## Veja também` — [[20 - Contract testing — Pact]], [[21 - Capstone — a estratégia de testes de uma app Spring production-grade]], **[[03-Dominios/Tecnologia/Java/Spring Core e Boot/06 - ApplicationContext — o container e seu ciclo|ApplicationContext]]**, verbetes `ArchUnit`/`fitness function`.

- [ ] **Step 3: Verificar** — ≥7 seções; ≥3 armadilhas; anti-fabricação VAZIO; `grep -i "ArchUnit\|ArchRule\|layeredArchitecture"` ≥2.

- [ ] **Step 4: Commit** — `git commit -m "feat(java): galho 13 nota 19 — fitness functions (ArchUnit)"`

### Task 20: Nota 20 — Contract testing — Pact ⟦opus⟧

**Files:**
- Create: `03-Dominios/Tecnologia/Java/Testes/20 - Contract testing — Pact.md`

- [ ] **Step 1: Pesquisar (version-specific)** — WebFetch `https://docs.pact.io/` + `https://docs.pact.io/implementation_guides/jvm`. CONFIRMAR: consumer-driven contract; consumer (`@ExtendWith(PactConsumerTestExt.class)`, `@Pact`, `PactDslWithProvider`, gera o pact); producer (`@Provider`, `@PactFolder`, `@State`, `PactVerificationInvocationContextProvider`); quebra de contrato falha o build sem E2E. **WebFetch obrigatório.**

- [ ] **Step 2: Escrever** — `fase: magus`, tags `[java, testes, magus, pact]`. ≥3 H3s: "O problema: E2E entre serviços é frágil e lento", "Consumer declara expectativas e gera o pact (@Pact)", "Producer verifica que cumpre o contrato (@Provider / @State)", "Quebra de contrato falha no build (sem rodar os 2 serviços juntos)". `## Na prática` — um consumer test (`@Pact` + `PactDslWithProvider` + `@PactTestFor`) e um producer test (`@Provider` + `@State`) neutros (`order-service`/`billing-service`) (```java). **Microservices/orquestração distribuída = Galho 16 (texto "(planejado)", sem wikilink).** `## Armadilhas` ≥3: (1) contrato acoplado a detalhe de implementação (muda toda hora); (2) producer não rodando a verificação no CI (o contrato vira mentira); (3) Pact onde um teste de integração simples bastava (over-engineering). `## Veja também` — [[19 - Fitness functions — ArchUnit (testes de arquitetura)]], [[16 - Mockando HTTP externo — WireMock e MockRestServiceServer]], [[21 - Capstone — a estratégia de testes de uma app Spring production-grade]], verbetes `contract testing`/`Pact`.

- [ ] **Step 3: Verificar** — ≥7 seções; ≥3 armadilhas; anti-fabricação VAZIO; `grep -E "\[\[[^]]*Galho 16" "<path>"` VAZIO (Galho 16 só texto); `grep -i "Pact\|contract"` ≥2.

- [ ] **Step 4: Commit** — `git commit -m "feat(java): galho 13 nota 20 — contract testing (Pact)"`

### Task 21: Nota 21 — Capstone — a estratégia de testes de uma app Spring production-grade ⟦opus⟧

**Files:**
- Create: `03-Dominios/Tecnologia/Java/Testes/21 - Capstone — a estratégia de testes de uma app Spring production-grade.md`

- [ ] **Step 1: Pesquisar** — WebFetch `https://docs.spring.io/spring-boot/reference/testing/index.html` (índice, pra reforçar o checklist). Reforçar a pirâmide.

- [ ] **Step 2: Escrever** — `fase: magus`, tags `[java, testes, magus]`. **Capstone-síntese.** Conteúdo:
  - TL;DR: uma suíte production-grade segue a pirâmide (muitos unit rápidos, slices pra camadas, integração com Testcontainers, poucos E2E), usa AssertJ pra legibilidade, mocka só o que importa, troca `Thread.sleep` por Awaitility, e vai além do verde com mutation testing e fitness functions.
  - `## A pirâmide na prática` — distribuição como **heurística** (70-80% unit / 15-25% integration / 2-5% E2E — "regra prática comum", SEM "X% dos projetos"); tempo de suite alvo (unit <30s, total CI <10min).
  - `## O que testar em qual nível` — unit (sem Spring, `new Service(mock)`), slice (`@WebMvcTest`/`@DataJpaTest`), integração (`@SpringBootTest`+Testcontainers), E2E (fluxos críticos).
  - `## A convergência numa tabela` — tabela "o que testar | ferramenta/slice | galho dono": controller↔@WebMvcTest↔G9, repository↔@DataJpaTest↔G10, reativo↔StepVerifier/@WebFluxTest↔G11, segurança↔@WithMockUser↔G12, container/slice↔G8, async↔Awaitility↔G4.
  - `## Combate à flakiness` — nunca Thread.sleep (Awaitility), testes independentes de ordem, Testcontainers (não "na minha máquina"), investigar flaky em vez de "roda de novo".
  - `## Cheatsheet nota → problema` — tabela "problema → nota do galho" (usar os **títulos EXATOS** das notas 01-20 — conferir 1:1, lição do Galho 12).
  - `## Armadilhas` (de raciocínio) ≥3: (1) "coverage alto = bom" (mutation testing); (2) "tudo @SpringBootTest" (pirâmide invertida, suíte lenta); (3) "H2 serve" (dialeto SQL diverge).
  - `## Em entrevista` (munição: "qual sua estratégia de testes?") + `## Veja também` — [[01 - O que é testar em Java — a pirâmide e o stack moderno]], [[12 - Testes de integração ponta a ponta]], [[17 - Mutation testing — PIT e cobertura honesta]], MOC galho, MOC central + `## Referências`.

- [ ] **Step 3: Verificar** — ≥8 seções; ≥3 armadilhas; anti-fabricação VAZIO; **conferir os títulos do cheatsheet 1:1 com os arquivos reais** (`for n in 01..20; do ls "03-Dominios/Tecnologia/Java/Testes/$n "*; done` e cruzar com os wikilinks da nota); `grep -E "\[\[[^]]*Galho (14|16|17)" "<path>"` VAZIO.

- [ ] **Step 4: Commit** — `git commit -m "feat(java): galho 13 nota 21 — capstone (a estratégia de testes de uma app Spring production-grade)"`

---

## Task 22: MOC do galho

**Files:**
- Create: `03-Dominios/Tecnologia/Java/Testes/index.md`

- [ ] **Step 1: Escrever** — modelar pelo `03-Dominios/Tecnologia/Java/Segurança/index.md`. Frontmatter: `type: moc`, `status: growing`, `publish: true`, `title: "Testes"`, tags `[java, testes, moc]`, aliases `["Testes", "Testes em Java", "Testing", "Galho 13 - Testes"]`, `created`/`updated: 2026-06-11`. Conteúdo:
  - TL;DR — Galho 13; a disciplina que testa os Galhos 1-12: JUnit 5/AssertJ/Mockito, os slices do Spring, Testcontainers e integração, testes de segurança/async/reativo, e o que vai além do verde (mutation, performance, fitness functions, contratos); 21 notas em 3 fases.
  - `## Sobre este galho` — escopo + audiência + **galho híbrido** (poda integral do tronco `Testes em Java.md` + pesquisa version-specific) + **convergência** (testa o que os Galhos 1-12 construíram; cada técnica linka de volta ao galho dono; paga 3 dívidas — G10/G11/G12). Galhos 14/16/17 planejados (texto).
  - `## Iniciado` (01-05) / `## Adepto` (06-12) / `## Magus` (13-21) — wikilinks + 1 linha cada.
  - `## Rotas alternativas` — 5: **Completa** (01→21); **Entrevista internacional** (01→02→03→06→09→10→12→21); **Os slices do Spring** (08→09→10→11→12→13); **Indo além do verde** (17→18→19→20); **Testando o stack reativo** (01→08→15 + Galho 11 WebFlux/WebClient).
  - `## Todas as notas` — Dataview (`FROM "03-Dominios/Tecnologia/Java/Testes"`, `WHERE type = "concept"`).
  - `## Veja também` — MOC central, **[[03-Dominios/Tecnologia/Java/Spring Core e Boot/index|Spring Core e Boot]]** (o container que os slices carregam), **[[03-Dominios/Tecnologia/Java/Web e APIs REST/index|Web e APIs REST]]** (a web testada), **[[03-Dominios/Tecnologia/Java/Persistência de dados/index|Persistência de dados]]** (a persistência testada), **[[03-Dominios/Tecnologia/Java/Programação Reativa/index|Programação Reativa]]** (o reativo testado), **[[03-Dominios/Tecnologia/Java/Segurança/index|Segurança]]** (a segurança testada), Dicionário; Galhos 14/16/17 como texto "(planejado)" SEM wikilink.

- [ ] **Step 2: Verificar**
```bash
grep -cE "^## (Iniciado|Adepto|Magus|Rotas alternativas)" "03-Dominios/Tecnologia/Java/Testes/index.md"
grep -c "\[\[" "03-Dominios/Tecnologia/Java/Testes/index.md"
grep -E "\[\[[^]]*(Galho (14|16|17))" "03-Dominios/Tecnologia/Java/Testes/index.md"
```
Expected: 4 headings; ≥21 wikilinks; **último grep VAZIO**.

- [ ] **Step 3: Commit** — `git add "<path>"` && `git commit -m "feat(java): galho 13 MOC — Testes"`

---

## Task 23: Expandir o Dicionário de Java (NÃO recriar)

**Files:**
- Modify: `03-Dominios/Tecnologia/Java/Dicionário de Java.md`

- [ ] **Step 1: Extrair as âncoras realmente usadas pelas notas**
```bash
grep -rhoE "Dicionário de Java#[^]|]+" "03-Dominios/Tecnologia/Java/Testes/" | sort -u
```
Se as notas linkarem o Dicionário SEM âncora (como no Galho 12), não há âncora a conferir — basta inserção alfabética. Lista esperada (~38): `@DataJpaTest`, `@MockitoBean`, `@Nested`, `@ParameterizedTest`, `@ServiceConnection`, `@SpringBootTest`, `@WebFluxTest`, `@WebMvcTest`, `@WithMockUser`, `AAA (Arrange-Act-Assert)`, `ArchUnit`, `ArgumentCaptor`, `AssertJ`, `Awaitility`, `contract testing`, `fitness function`, `H2 (vs Testcontainers)`, `InjectMocks`, `JMH (microbenchmark)`, `JUnit 5 (Jupiter)`, `MockMvc`, `Mockito`, `mock vs spy vs fake vs stub`, `MockRestServiceServer`, `mutation testing`, `Pact`, `PIT (Pitest)`, `soft assertions`, `StepVerifier`, `test data builder`, `test pyramid (pirâmide de testes)`, `test slice (Spring Boot)`, `Testcontainers`, `TestEntityManager`, `usingRecursiveComparison`, `verify (Mockito)`, `WebTestClient`, `WireMock`.

- [ ] **Step 2: Ler o Dicionário e conferir duplicatas** — formato `### Termo` + 1-3 linhas + `Veja também:`. **NÃO recriar/reordenar.** Conferir dups (Galhos 9-11): `WebTestClient`/`WebClient` (G9/G11 — se existir, complementar/linkar, não duplicar), `MockMvc` (G9 — pode existir). Conferir com:
```bash
grep -nE "^### (WebClient|WebTestClient|MockMvc|RestClient|Mockito|JUnit)" "03-Dominios/Tecnologia/Java/Dicionário de Java.md"
```

- [ ] **Step 3: Inserir em ordem alfabética** (case-insensitive, sem acento; `@`-prefixados alfabetizam pela palavra após o `@`; conferir vizinhos). Cada verbete: heading EXATO + definição fiel às notas + `Veja também:` pra nota canônica (test pyramid/JUnit/AssertJ/Mockito/Testcontainers→01; AAA→02; AssertJ/soft/usingRecursiveComparison→03; @ParameterizedTest/@Nested→04; test data builder→05; Mockito/mock-vs-spy/InjectMocks→06; verify/ArgumentCaptor→07; test slice/@SpringBootTest/@MockitoBean→08; @WebMvcTest/MockMvc→09; @DataJpaTest/TestEntityManager→10; Testcontainers/@ServiceConnection/H2→11; WebTestClient→12; @WithMockUser→13; Awaitility→14; StepVerifier/@WebFluxTest→15; WireMock/MockRestServiceServer→16; mutation testing/PIT→17; JMH→18; ArchUnit/fitness function→19; Pact/contract testing→20). Atualizar `updated: 2026-06-11`.

- [ ] **Step 4: Verificar**
```bash
grep -E "^### (JUnit 5|Mockito|@WebMvcTest|Testcontainers|StepVerifier|Pact)" "03-Dominios/Tecnologia/Java/Dicionário de Java.md"
grep -cE "^### " "03-Dominios/Tecnologia/Java/Dicionário de Java.md"
```
Expected: novos presentes; contagem subiu ~38 vs baseline (366 → ~404, descontando os que já existiam e foram linkados).

- [ ] **Step 5: Commit** — `git add "<path>"` && `git commit -m "feat(java): expande Dicionário de Java com verbetes do galho 13 (Testes)"`

---

## Task 24: Ativar o Galho 13 no MOC central

**Files:**
- Modify: `03-Dominios/Tecnologia/Java/index.md`

- [ ] **Step 1: Trocar a linha do item 13** (localizar por conteúdo: `13. Testes *(planejado)* — JUnit 5, Mockito, AssertJ, Spring Boot Test, Testcontainers`) por:
```markdown
13. [[03-Dominios/Tecnologia/Java/Testes/index|Testes]] — a pirâmide e o stack moderno, JUnit 5/AssertJ/Mockito, os slices do Spring Boot, Testcontainers e integração, testes de segurança/async/reativo, mutation testing, performance, fitness functions e contract testing
```
Atualizar `updated: 2026-06-11`. Não mexer no resto (14/16/17 permanecem "(planejado)").

- [ ] **Step 2: Verificar**
```bash
grep -E "Testes/index" "03-Dominios/Tecnologia/Java/index.md"
grep -c "planejado" "03-Dominios/Tecnologia/Java/index.md"
```
Expected: wikilink ativo; "planejado" caiu exatamente 1 vs baseline.

- [ ] **Step 3: Commit** — `git add "<path>"` && `git commit -m "feat(java): ativa Galho 13 (Testes) no MOC central"`

---

## Task 25: Poda INTEGRAL do tronco (`Backend/Testes em Java.md`) — vira hub

**Files:**
- Modify: `03-Dominios/Tecnologia/Java/Backend/Testes em Java.md`

- [ ] **Step 1: Ler o tronco e confirmar o frontmatter** (política §9 — ler antes de podar)
```bash
sed -n '1,16p' "03-Dominios/Tecnologia/Java/Backend/Testes em Java.md"
```
Confirmar o bloco de frontmatter (linhas 1-13, `publish: false`, tags incluindo `testes`) a **preservar**; o corpo (do H1 `# Testes em Java` até o fim) será **substituído**.

- [ ] **Step 2: Poda INTEGRAL** — reescrever o arquivo inteiro (preservando o frontmatter com `updated: 2026-06-11`, `publish: false`) com H1 + 1-2 frases de intro neutras + um único callout `[!nota] Migrado para galho próprio`:
```markdown
# Testes em Java

Estratégias, ferramentas e patterns de teste na stack Java moderna — JUnit 5, AssertJ, Mockito, Spring Boot Test e slices, Testcontainers e qualidade de testes. Conteúdo migrado para galho próprio na trilha Java Senior.

> [!nota] Migrado para galho próprio
> Expandido no galho [[03-Dominios/Tecnologia/Java/Testes/index|Testes]]. Veja [[03-Dominios/Tecnologia/Java/Testes/01 - O que é testar em Java — a pirâmide e o stack moderno|O que é testar em Java]], [[03-Dominios/Tecnologia/Java/Testes/06 - Mockito — mocks, stubbing e matchers|Mockito]], [[03-Dominios/Tecnologia/Java/Testes/09 - @WebMvcTest — testando controllers com MockMvc|@WebMvcTest]], [[03-Dominios/Tecnologia/Java/Testes/10 - @DataJpaTest — testando repositories|@DataJpaTest]], [[03-Dominios/Tecnologia/Java/Testes/12 - Testes de integração ponta a ponta|Testes de integração]] e o [[03-Dominios/Tecnologia/Java/Testes/21 - Capstone — a estratégia de testes de uma app Spring production-grade|Capstone]].
```
**Toda a fabricação some** (`Patient`/`PatientService`/`Maria`/`PatientBuilder`/`PatientAssert`, `## Na prática (da minha experiência)` com a "evolução da stack do MedEspecialista"/"incidente de flakiness", `## How to explain in English` 1ª pessoa, `### Frases úteis`).

- [ ] **Step 3: Verificar (poda integral — só o hub sobra)**
```bash
wc -l "03-Dominios/Tecnologia/Java/Backend/Testes em Java.md"
grep -c "Migrado para galho próprio" "03-Dominios/Tecnologia/Java/Backend/Testes em Java.md"
grep -riE "Patient|Maria|MedEspecialista|minha experiência|quando comecei|incidente de flakiness|How to explain|## Na prática" "03-Dominios/Tecnologia/Java/Backend/Testes em Java.md"
grep -E "^publish: false" "03-Dominios/Tecnologia/Java/Backend/Testes em Java.md"
```
Expected: ~10-12 linhas; ≥1 callout; **terceiro grep VAZIO**; `publish: false` presente.

- [ ] **Step 4: Confirmar troncos vizinhos intocados**
```bash
git status --short "03-Dominios/Tecnologia/Java/Backend/Spring Boot.md" "03-Dominios/Tecnologia/Java/Backend/Spring Data JPA.md" "03-Dominios/Tecnologia/Java/Backend/Spring Security.md" "03-Dominios/Tecnologia/Java/Backend/Kafka/"
```
Expected: **VAZIO**.

- [ ] **Step 5: Commit** — `git add "03-Dominios/Tecnologia/Java/Backend/Testes em Java.md"` && `git commit -m "refactor(java): poda integral do tronco Testes em Java — vira hub do galho 13"`

---

## Task 26: Quitar a dívida reversa (1 inline + 5 parágrafos → wikilinks)

**Files:**
- Modify: `03-Dominios/Tecnologia/Java/Segurança/18 - Capstone — projetando a segurança de uma API Spring production-grade.md`
- Modify: `03-Dominios/Tecnologia/Java/Segurança/index.md`
- Modify: `03-Dominios/Tecnologia/Java/Persistência de dados/index.md`
- Modify: `03-Dominios/Tecnologia/Java/Programação Reativa/index.md`
- Modify: `03-Dominios/Tecnologia/Java/Spring Core e Boot/index.md`
- Modify: `03-Dominios/Tecnologia/Java/Web e APIs REST/index.md`

- [ ] **Step 1: Relocalizar (por conteúdo — linhas podem ter mudado)**
```bash
grep -rn "Galho 13\|galho 13" "03-Dominios/Tecnologia/Java/Segurança/18 - Capstone — projetando a segurança de uma API Spring production-grade.md" "03-Dominios/Tecnologia/Java/Segurança/index.md" "03-Dominios/Tecnologia/Java/Persistência de dados/index.md" "03-Dominios/Tecnologia/Java/Programação Reativa/index.md" "03-Dominios/Tecnologia/Java/Spring Core e Boot/index.md" "03-Dominios/Tecnologia/Java/Web e APIs REST/index.md"
```

- [ ] **Step 2: Aplicar os wikilinks** — trocar "Galho 13 (planejado)" pelo wikilink, mantendo natural a frase e atualizando `updated: 2026-06-11` no frontmatter de cada arquivo tocado:
  - **Segurança/18 - Capstone (~:98):** "...a stack de teste ... é assunto do galho de Testes (Galho 13, planejado)." → "...é assunto do galho [[03-Dominios/Tecnologia/Java/Testes/13 - Testando a segurança|Testes]]." (mantém a frase; o resto da frase sobre `@WithMockUser`/`with(jwt())` continua).
  - **Segurança/index (~:32):** "Testes de segurança (Galho 13 planejado)..." → "Testes de segurança são o galho [[03-Dominios/Tecnologia/Java/Testes/13 - Testando a segurança|Testes]]..." (ajustar a frase; manter 16/17 planejados como texto).
  - **Persistência de dados/index (~:32):** "...testes de repositório (Galho 13) e dados distribuídos/saga (Galho 16) são planejados..." → "...testes de repositório são o galho [[03-Dominios/Tecnologia/Java/Testes/10 - @DataJpaTest — testando repositories|Testes]]; dados distribuídos/saga (Galho 16) são planejados..."
  - **Programação Reativa/index (~:35):** "...segurança reativa (Galho 12) e testes reativos com `StepVerifier` (Galho 13) são planejados..." → "...segurança reativa (Galho 12, planejado) e testes reativos com `StepVerifier` são o galho [[03-Dominios/Tecnologia/Java/Testes/15 - Testando código reativo — StepVerifier e @WebFluxTest|Testes]]..." (manter 12/14/16 como texto planejado conforme a frase original).
  - **Spring Core e Boot/index (~:32):** "...Testes no ecossistema Spring (Galho 13) e Microservices/Cloud com Spring Cloud (Galhos 16 e 17) são planejados..." → "...Testes no ecossistema Spring é o galho [[03-Dominios/Tecnologia/Java/Testes/index|Testes]]; Microservices/Cloud com Spring Cloud (Galhos 16 e 17) são planejados..." **NÃO tocar o horizonte-list :97.**
  - **Web e APIs REST/index (~:32):** "...Testes no ecossistema Spring (Galho 13), Microservices (Galho 16) e Spring Cloud (Galho 17) são planejados..." → "...Testes no ecossistema Spring é o galho [[03-Dominios/Tecnologia/Java/Testes/index|Testes]]; Microservices (Galho 16) e Spring Cloud (Galho 17) são planejados..." **NÃO tocar o horizonte-list :95.**

- [ ] **Step 3: Verificar**
```bash
grep -rn "Galho 13\|galho 13" "03-Dominios/Tecnologia/Java/Segurança/18 - Capstone — projetando a segurança de uma API Spring production-grade.md" "03-Dominios/Tecnologia/Java/Segurança/index.md" "03-Dominios/Tecnologia/Java/Persistência de dados/index.md" "03-Dominios/Tecnologia/Java/Programação Reativa/index.md" "03-Dominios/Tecnologia/Java/Spring Core e Boot/index.md" "03-Dominios/Tecnologia/Java/Web e APIs REST/index.md" | grep -iE "planejado" | grep -vE ":(95|97|92):"
grep -rn "Testes/index\|Testes/10\|Testes/13\|Testes/15" "03-Dominios/Tecnologia/Java/Segurança/index.md" "03-Dominios/Tecnologia/Java/Persistência de dados/index.md" "03-Dominios/Tecnologia/Java/Programação Reativa/index.md" "03-Dominios/Tecnologia/Java/Spring Core e Boot/index.md" "03-Dominios/Tecnologia/Java/Web e APIs REST/index.md" "03-Dominios/Tecnologia/Java/Segurança/18 - Capstone — projetando a segurança de uma API Spring production-grade.md"
```
Expected: primeiro grep **VAZIO** ou só horizonte-lists; segundo grep ≥6 (wikilinks aplicados). Conferir manualmente que cada "Galho 13" remanescente vem com o wikilink "Testes", e que os horizonte-lists (:95/:97/:92) e galhos 14/16/17 permanecem "(planejado)".

- [ ] **Step 4: Commit** — `git add` nominal dos 6 arquivos && `git commit -m "refactor(java): quita dívida reversa do galho 13 — ponteiros de testes viram wikilinks"`

---

## Task 27: Verificação final do galho

**Files:** (somente leitura/verificação)

- [ ] **Step 1: 21 notas + MOC**
```bash
ls "03-Dominios/Tecnologia/Java/Testes/" | sort
```
Expected: 01..21 + index.md (22 arquivos).

- [ ] **Step 2: Fases (5/7/9)**
```bash
for f in "03-Dominios/Tecnologia/Java/Testes/"[0-9]*.md; do grep -H "^fase:" "$f"; done
```
Expected: 01-05 `iniciado`, 06-12 `adepto`, 13-21 `magus`.

- [ ] **Step 3: Seções obrigatórias (3 por nota)**
```bash
for f in "03-Dominios/Tecnologia/Java/Testes/"[0-9]*.md; do echo "$f: $(grep -cE '^## (Em entrevista|Armadilhas|Veja também)' "$f")"; done
```
Expected: 3 em todas.

- [ ] **Step 4: Anti-fabricação + estatística + fronteiras (greps decisivos)**
```bash
grep -riE "minha experiência|no meu projeto|josenaldo|Patient|Maria|MedEspecialista|quando comecei|incidente de flakiness|[0-9]+% d[ao]s (projetos|times|empresas)" "03-Dominios/Tecnologia/Java/Testes/"
grep -rE "\[\[[^]]*(Galho (14|16|17)|Spring Cloud|Selenide|Playwright)" "03-Dominios/Tecnologia/Java/Testes/"
grep -rn '\[\[#' "03-Dominios/Tecnologia/Java/Testes/"
```
Expected: **todos VAZIOS**.

- [ ] **Step 5: Convergência-assinatura (links de volta presentes)**
```bash
grep -rl "Web e APIs REST/0(2|6|9)" "03-Dominios/Tecnologia/Java/Testes/" | sort       # G9 (09)
grep -rl "Persistência de dados/0(4|9)" "03-Dominios/Tecnologia/Java/Testes/" | sort    # G10 (10, 11)
grep -rl "Programação Reativa/1(0|1)" "03-Dominios/Tecnologia/Java/Testes/" | sort       # G11 (15)
grep -rl "Segurança/0(5|7)" "03-Dominios/Tecnologia/Java/Testes/" | sort                 # G12 (13)
grep -rl "Spring Core e Boot/(06|15)" "03-Dominios/Tecnologia/Java/Testes/" | sort       # G8 (08)
grep -rl "Concorrência e paralelismo/index" "03-Dominios/Tecnologia/Java/Testes/" | sort # G4 (14)
grep -rl "JVM/07" "03-Dominios/Tecnologia/Java/Testes/" | sort                           # G3 (18)
```
Expected: nota 09→G9, 10/11→G10, 15→G11, 13→G12, 08→G8, 14→G4, 18→G3 (no mínimo).

- [ ] **Step 6: Frase pronta (1 por nota)**
```bash
for f in "03-Dominios/Tecnologia/Java/Testes/"[0-9]*.md; do echo "$f: $(grep -c '### Frase pronta (inglês)' "$f")"; done
```
Expected: 1 em todas.

- [ ] **Step 7: Tronco — poda integral confirmada; vizinhos intocados**
```bash
wc -l "03-Dominios/Tecnologia/Java/Backend/Testes em Java.md"
grep -c "Migrado para galho próprio" "03-Dominios/Tecnologia/Java/Backend/Testes em Java.md"
grep -riE "Patient|MedEspecialista|## Na prática|How to explain" "03-Dominios/Tecnologia/Java/Backend/Testes em Java.md"
git status --short "03-Dominios/Tecnologia/Java/Backend/Spring Boot.md" "03-Dominios/Tecnologia/Java/Backend/Spring Data JPA.md" "03-Dominios/Tecnologia/Java/Backend/Spring Security.md" "03-Dominios/Tecnologia/Java/Backend/Kafka/"
```
Expected: `Testes em Java.md` ~10-12 linhas só com o hub (≥1 callout; terceiro grep **VAZIO**); troncos vizinhos **sem modificação**.

- [ ] **Step 8: Skill `verificar-wikilinks`** — rodar na pasta `03-Dominios/Tecnologia/Java/Testes/` + conferir os arquivos tocados fora (MOC central, Dicionário, o tronco Testes em Java, os 6 arquivos da dívida reversa). **Conferir EXPLICITAMENTE os títulos do cheatsheet do capstone (nota 21) e do checklist — lição do Galho 12** (a nota 18 do Segurança inventou títulos de notas; o checker pegou 20 quebras). As quebras legadas da árvore Java NÃO são deste galho — só corrigir o que este galho introduziu. Corrigir e commitar à parte se houver.

- [ ] **Step 9: Resumo de fechamento (sem commit)** — reportar: 21 notas (5/7/9), ~38 verbetes (366→~404), MOC galho + MOC central, **poda integral** (tronco `Testes em Java.md` vira hub; toda a fabricação MedEspecialista/flakiness/`How to explain` sumiu), **dívida reversa quitada** (1 inline + 5 parágrafos; horizonte-lists e galhos 14/16/17 preservados como "(planejado)"; as 3 dívidas G10/G11/G12 pagas), troncos vizinhos intocados, wikilinks limpos, **convergência-assinatura** (cada técnica linka o galho da camada testada), **zero estatística inventada** (pirâmide como heurística). Commits locais na `main`; **push manual do usuário; sem deploy**. Atualizar memória [[project_trilha_java]] com Galho 13 completo + fatos cravados via WebFetch (`@MockitoBean` Boot 3.4+, `@ServiceConnection` Boot 3.1+, static mocking Mockito 5, versões JUnit/Mockito/Testcontainers).

---

## Self-Review (preenchido na escrita do plano)

**Spec coverage:** Tasks 1-21 ↔ spec §3.1 (21 notas, escopos idênticos, opus 01/06/09/10/12/15/20/21, distribuição 5/7/9); Task 22 ↔ §3.2 (MOC, 5 rotas iguais); Task 23 ↔ §3.3 (~38 verbetes, dups WebTestClient/MockMvc conferidos); Task 24 ↔ §3.4 (item 13); Task 25 ↔ §3.5 (poda integral — tronco vira hub; fabricação some; `publish: false` mantido; vizinhos intocados); Task 26 ↔ §3.6 (1 inline + 5 parágrafos; Segurança/18→nota13, Persistência:32→nota10, Reativa:35→nota15, Segurança:32→nota13, Spring Core/Web:32→MOC; horizonte-lists e 14/16/17 preservados); Task 0 ↔ §6 (pré-flight, baseline 366, leitura do tronco); Task 27 ↔ §7. Convergência-assinatura (§4.3.1) garantida por links obrigatórios nas Tasks 8/9/10/11/13/14/15/16/18 e pelo grep da Task 27 Step 5; fronteira galhos 14/16/17 pelo grep da Task 27 Step 4.

**Placeholder scan:** sem TBD/TODO; cada nota tem fonte WebFetch nomeada com URL, frontmatter concreto, H3s, armadilhas mínimas com conteúdo real, tamanho-alvo herdado das convenções. Pontos version-sensitive marcados com "confirmar" são instruções de verificação WebFetch (a parte pesquisa), não placeholders: `@MockitoBean`/`@MockBean`, `@ServiceConnection`, static mocking Mockito 5, versões, `StepVerifier`/`reactor-test`, `spring-security-test`. A confirmação dos ranges/linhas do tronco e da dívida reversa (Tasks 0/25/26) é resolução-na-execução por política §9 do roadmap.

**Type/naming consistency:** numeração 01-21 idêntica entre tasks, MOC, Dicionário, dívida reversa, poda e cheatsheet do capstone; distribuição 5/7/9 consistente; opus 01/06/09/10/12/15/20/21 marcadas ⟦opus⟧ (8 notas, batendo com spec §3.1); filenames com em dash (sem `:`/`/`); mapeamento de link-back G9→notas (02/06/09/15), G10→(04/09), G11→(10/11), G12→(05/07), G8→(06/15), G4→index, G3→JVM/07, G1→Linguagem/10 consistente entre spec §4.3.1, convenções e Tasks; âncoras do Dicionário extraídas por grep antes de inserir (Task 23); cheatsheet do capstone (nota 21) com conferência 1:1 dos títulos reais (lição do Galho 12 reforçada na Task 21 Step 3 e Task 27 Step 8).
