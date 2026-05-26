---
title: "Testes em Java"
created: 2026-04-01
updated: 2026-04-10
type: concept
status: evergreen
tags:
  - java
  - testes
  - entrevista
publish: false
---

# Testes em Java

Deep dive em estratégias, ferramentas e patterns de teste na stack Java moderna. Para fundamentos gerais de testes (pirâmide, estratégias, tipos), ver [[Testes]]. Esta nota foca em **como** testar Java idiomaticamente com **JUnit 5**, **Mockito**, **AssertJ**, **Testcontainers** e **Spring Boot Test**.

## O que é

Testar em Java hoje é fundamentalmente diferente de testar em 2010. JUnit 5 substituiu o modelo do JUnit 4, AssertJ substituiu hamcrest para asserções legíveis, Testcontainers tornou testes de integração reais viáveis, e Spring Boot oferece slices de teste para isolar camadas. Para um senior, dominar esse stack é tão importante quanto dominar a linguagem.

Em entrevistas, o que diferencia um senior em testes Java:

1. **Pirâmide correta** — muitos unit tests, alguns integration, poucos E2E. Não inverter.
2. **Testcontainers > mocks de DB** — teste com Postgres real, não H2
3. **Dominar mocks** — Mockito, quando mockar vs quando usar fake real, ArgumentCaptor
4. **Slices do Spring Boot** — `@WebMvcTest`, `@DataJpaTest`, `@SpringBootTest` — cada um para um propósito
5. **Testes que servem como documentação** — nomes expressivos, fácil de ler, AAA pattern
6. **Conhecer ferramentas avançadas** — ArchUnit, PIT mutation testing, JMH para performance, Pact para contract testing

---

## Stack de testes moderno (Java 21+ / Spring Boot 3+)

| Ferramenta | Propósito | Status |
| --- | --- | --- |
| **JUnit 5 (Jupiter)** | Framework de testes | Padrão |
| **AssertJ** | Asserções fluent | Padrão moderno (melhor que hamcrest) |
| **Mockito** | Mocks e spies | Padrão |
| **Testcontainers** | Containers Docker para integração | Essencial |
| **Spring Boot Test** | Slices e contextos de teste | Para apps Spring |
| **WireMock** | Mock de HTTP externo | Para integrações |
| **JSONassert / json-path** | Asserções em JSON | Para APIs REST |
| **Awaitility** | Async/eventual consistency | Para testes assíncronos |
| **ArchUnit** | Testes de arquitetura | Fitness functions |
| **PIT (Pitest)** | Mutation testing | Qualidade dos testes |
| **JMH** | Microbenchmarks | Performance |
| **Pact** | Contract testing | Microserviços |
| **Selenide / Playwright for Java** | E2E web | UI tests |

**Ferramentas deprecated que você ainda pode encontrar:**
- JUnit 4 (ainda comum em projetos legacy)
- Hamcrest (substituído por AssertJ)
- H2 in-memory DB (substituído por Testcontainers)
- PowerMock (hack para mockar static/final — geralmente sinal de design ruim)
- EasyMock, JMock (substituídos por Mockito)

---

## JUnit 5 (Jupiter)

Framework de testes moderno para Java. Reescrito do zero, com arquitetura modular.

### Arquitetura

JUnit 5 = **JUnit Platform** + **JUnit Jupiter** + **JUnit Vintage**

- **Platform** — base para executar testes na JVM
- **Jupiter** — API moderna (`@Test`, `@BeforeEach`, etc.)
- **Vintage** — compatibilidade com JUnit 3/4

### Setup (Maven)

```xml
<dependency>
    <groupId>org.junit.jupiter</groupId>
    <artifactId>junit-jupiter</artifactId>
    <version>5.10.2</version>
    <scope>test</scope>
</dependency>
```

Com Spring Boot, `spring-boot-starter-test` já traz JUnit 5 + AssertJ + Mockito + muito mais.

### Anatomia de um teste

```java
import org.junit.jupiter.api.*;
import static org.assertj.core.api.Assertions.*;

class PatientServiceTest {

    private PatientService service;

    @BeforeAll
    static void setUpClass() {
        // Roda uma vez antes de todos os testes (static)
    }

    @BeforeEach
    void setUp() {
        // Roda antes de cada teste
        service = new PatientService();
    }

    @Test
    @DisplayName("should create patient when all fields are valid")
    void shouldCreatePatientWhenAllFieldsAreValid() {
        // given
        var request = new CreatePatientRequest("Maria", "maria@example.com");

        // when
        Patient result = service.create(request);

        // then
        assertThat(result).isNotNull();
        assertThat(result.id()).isPositive();
        assertThat(result.name()).isEqualTo("Maria");
    }

    @AfterEach
    void tearDown() {
        // Roda após cada teste
    }

    @AfterAll
    static void tearDownClass() {
        // Roda uma vez após todos os testes (static)
    }
}
```

**AAA Pattern:** Arrange (given) → Act (when) → Assert (then). Torna testes legíveis em segundos.

**Convenções de nome:**
- `should<Expected>When<Condition>` — `shouldReturn404WhenPatientNotFound`
- `<method>_<scenario>_<expectedOutcome>` — `create_withValidData_returnsSavedPatient`
- Português: `deveCriarPacienteQuandoDadosValidos` (alguns times preferem)
- Use `@DisplayName` para mensagens em linguagem natural com espaços e acentos

### Assertions básicas (JUnit built-in)

```java
import static org.junit.jupiter.api.Assertions.*;

assertEquals(expected, actual);
assertNotEquals(unexpected, actual);
assertTrue(condition);
assertFalse(condition);
assertNull(value);
assertNotNull(value);
assertSame(expected, actual);  // mesma referência
assertArrayEquals(expected, actual);
assertThrows(IllegalArgumentException.class, () -> service.invalidCall());
assertDoesNotThrow(() -> service.validCall());
assertTimeout(Duration.ofSeconds(5), () -> service.longOperation());
```

**Na prática, prefira AssertJ** — mais fluent, melhores mensagens de erro.

### Tests parametrizados

```java
@ParameterizedTest
@ValueSource(strings = { "", " ", "\t", "\n" })
void shouldRejectBlankEmail(String blank) {
    assertThatThrownBy(() -> service.create(new PatientRequest("Maria", blank)))
        .isInstanceOf(IllegalArgumentException.class);
}

@ParameterizedTest
@CsvSource({
    "18, adult",
    "17, minor",
    "65, senior"
})
void shouldClassifyAge(int age, String expected) {
    assertThat(classifier.classify(age)).isEqualTo(expected);
}

@ParameterizedTest
@MethodSource("invalidEmails")
void shouldRejectInvalidEmails(String email) {
    assertThat(validator.isValid(email)).isFalse();
}

static Stream<String> invalidEmails() {
    return Stream.of("no-at-sign.com", "@no-local.com", "a@", "double@@domain.com");
}

@ParameterizedTest
@EnumSource(OrderStatus.class)
void shouldHandleAllStatuses(OrderStatus status) {
    // testa todos os enum values
}

@ParameterizedTest
@CsvFileSource(resources = "/test-cases.csv", numLinesToSkip = 1)
void shouldProcessCsvCases(String input, String expected) { ... }
```

### Nested tests

Organize cenários relacionados:

```java
class OrderServiceTest {

    @Nested
    @DisplayName("when order is pending")
    class WhenOrderIsPending {

        @Test
        void canBeConfirmed() { ... }

        @Test
        void canBeCancelled() { ... }

        @Test
        void cannotBeShipped() { ... }
    }

    @Nested
    @DisplayName("when order is confirmed")
    class WhenOrderIsConfirmed {
        // ...
    }
}
```

### Tags e execução seletiva

```java
@Test
@Tag("slow")
@Tag("integration")
void integrationTest() { ... }

@Test
@Tag("unit")
void unitTest() { ... }
```

```bash
# Maven Surefire — executa só testes rápidos
mvn test -Dgroups="unit"
mvn test -DexcludedGroups="slow"
```

### Assumptions

```java
@Test
void onlyOnLinux() {
    Assumptions.assumeTrue(System.getProperty("os.name").contains("Linux"));
    // só roda em Linux
}
```

### Disabled

```java
@Test
@Disabled("waiting for feature X")
void pendingTest() { ... }

@Test
@DisabledOnOs(OS.WINDOWS)
@EnabledOnJre(JRE.JAVA_21)
void conditionallyEnabled() { ... }
```

### Timeouts

```java
@Test
@Timeout(value = 100, unit = TimeUnit.MILLISECONDS)
void shouldCompleteQuickly() {
    service.fastOperation();
}
```

### Lifecycle: per-method vs per-class

Por default, JUnit cria nova instância da classe por teste. Isso previne estado compartilhado acidental.

```java
@TestInstance(TestInstance.Lifecycle.PER_CLASS)
class SharedStateTest {
    private ExpensiveResource resource;  // compartilhado entre testes

    @BeforeAll  // agora pode ser não-static
    void setUp() {
        resource = new ExpensiveResource();
    }
}
```

**Use PER_CLASS** quando precisa compartilhar setup caro. Mas cuidado com estado entre testes.

### Extensions

Mecanismo poderoso para estender JUnit. Exemplos comuns:

```java
@ExtendWith(MockitoExtension.class)       // Mockito
@ExtendWith(SpringExtension.class)         // Spring (incluso em @SpringBootTest)
@Testcontainers                            // Testcontainers (incluso @ExtendWith)
```

Você pode escrever extensions customizadas para setup repetitivo (banco, mocks compartilhados, etc.).

---

## AssertJ: fluent assertions

Biblioteca de asserções com API fluent. **Muito mais legível** que JUnit built-in ou Hamcrest.

### Basic assertions

```java
import static org.assertj.core.api.Assertions.*;

// Strings
assertThat(name)
    .isNotNull()
    .isNotBlank()
    .startsWith("Mar")
    .contains("ia")
    .hasSize(5)
    .matches("[A-Z][a-z]+");

// Numbers
assertThat(total)
    .isPositive()
    .isBetween(100, 1000)
    .isCloseTo(500.0, within(0.01));

// Collections
assertThat(patients)
    .isNotEmpty()
    .hasSize(3)
    .contains(maria)
    .containsExactly(ana, bruno, carlos)           // ordem estrita
    .containsExactlyInAnyOrder(bruno, ana, carlos)  // qualquer ordem
    .extracting(Patient::name)                      // projeção
    .containsExactly("Ana", "Bruno", "Carlos");

// Maps
assertThat(scores)
    .hasSize(2)
    .containsKey("Ana")
    .containsEntry("Bruno", 95)
    .doesNotContainKey("deleted");

// Optional
assertThat(optional)
    .isPresent()
    .contains(expected)
    .hasValueSatisfying(user -> assertThat(user.name()).isEqualTo("Ana"));

// Dates
assertThat(birthDate)
    .isBefore(LocalDate.now())
    .isAfter(LocalDate.of(1900, 1, 1))
    .hasYear(1985);
```

### Exception assertions

```java
// Mais legível que @Test(expected = ...) ou assertThrows
assertThatThrownBy(() -> service.findById(999L))
    .isInstanceOf(PatientNotFoundException.class)
    .hasMessage("Patient not found: 999")
    .hasMessageContaining("999")
    .hasCauseInstanceOf(SQLException.class);

// Variação: captura e valida
Throwable ex = catchThrowable(() -> service.findById(999L));
assertThat(ex)
    .isInstanceOf(PatientNotFoundException.class)
    .hasFieldOrPropertyWithValue("patientId", 999L);

// Não deve lançar
assertThatNoException().isThrownBy(() -> service.findById(1L));

// Exception customizada
assertThatExceptionOfType(ValidationException.class)
    .isThrownBy(() -> service.validate(invalid))
    .withMessageContaining("email")
    .satisfies(ex -> assertThat(ex.getErrors()).hasSize(2));
```

### Soft assertions

Acumula falhas em vez de parar na primeira.

```java
@Test
void multipleAssertions() {
    var patient = service.findById(1L);

    SoftAssertions.assertSoftly(softly -> {
        softly.assertThat(patient.name()).isEqualTo("Maria");
        softly.assertThat(patient.age()).isEqualTo(39);
        softly.assertThat(patient.email()).endsWith("@example.com");
    });
    // Reporta TODAS as falhas no final, não só a primeira
}
```

### Comparação de objetos

```java
// Comparar todos os campos (recursivamente)
assertThat(actual)
    .usingRecursiveComparison()
    .isEqualTo(expected);

// Ignorar alguns campos (IDs gerados, timestamps)
assertThat(actual)
    .usingRecursiveComparison()
    .ignoringFields("id", "createdAt", "updatedAt")
    .isEqualTo(expected);
```

### Custom assertions

Para domínio específico, crie asserções expressivas:

```java
public class PatientAssert extends AbstractAssert<PatientAssert, Patient> {

    public PatientAssert(Patient actual) {
        super(actual, PatientAssert.class);
    }

    public static PatientAssert assertThat(Patient actual) {
        return new PatientAssert(actual);
    }

    public PatientAssert isAdult() {
        isNotNull();
        if (actual.age() < 18) {
            failWithMessage("Expected adult but age was <%d>", actual.age());
        }
        return this;
    }

    public PatientAssert hasEmail(String email) {
        isNotNull();
        if (!Objects.equals(actual.email(), email)) {
            failWithMessage("Expected email <%s> but was <%s>", email, actual.email());
        }
        return this;
    }
}

// Uso
PatientAssert.assertThat(patient)
    .isAdult()
    .hasEmail("maria@example.com");
```

---

## Mockito

Framework de mocks para Java. De facto standard.

### Setup

Spring Boot Test já inclui. Ou manualmente:

```xml
<dependency>
    <groupId>org.mockito</groupId>
    <artifactId>mockito-junit-jupiter</artifactId>
    <version>5.11.0</version>
    <scope>test</scope>
</dependency>
```

### Mock vs Spy vs Fake vs Stub

- **Mock** — objeto falso controlado, verificamos como foi chamado
- **Spy** — wrapper sobre objeto real, podemos stubar alguns métodos
- **Fake** — implementação simples alternativa (ex.: `HashMap` como fake repository)
- **Stub** — retorna respostas predefinidas, sem lógica

**Default:** use mocks. Spies só quando precisa de comportamento real misturado.

### Criando mocks

```java
@ExtendWith(MockitoExtension.class)
class PatientServiceTest {

    @Mock
    private PatientRepository repository;

    @Mock
    private NotificationSender notifier;

    @InjectMocks  // injeta os mocks no service
    private PatientService service;

    @Test
    void shouldSendNotificationOnCreate() {
        // given
        var request = new CreatePatientRequest("Maria", "maria@example.com");
        var saved = new Patient(1L, "Maria", "maria@example.com");
        when(repository.save(any(Patient.class))).thenReturn(saved);

        // when
        Patient result = service.create(request);

        // then
        assertThat(result).isEqualTo(saved);
        verify(notifier).sendWelcome("maria@example.com");
    }
}
```

### Stubbing

```java
// Retornar valor fixo
when(repository.findById(1L)).thenReturn(Optional.of(patient));

// Lançar exceção
when(repository.findById(999L)).thenThrow(new NotFoundException());

// Múltiplas chamadas — retornos diferentes
when(repository.count())
    .thenReturn(10L)   // primeira chamada
    .thenReturn(11L);  // segunda e subsequentes

// Resposta dinâmica via lambda
when(repository.save(any(Patient.class)))
    .thenAnswer(invocation -> {
        Patient p = invocation.getArgument(0);
        return new Patient(1L, p.name(), p.email());  // adiciona ID
    });

// Para void methods
doNothing().when(notifier).send(anyString());
doThrow(new RuntimeException("fail")).when(notifier).send("bad@email.com");
doAnswer(invocation -> {
    System.out.println("Side effect");
    return null;
}).when(notifier).send(anyString());
```

### Argument matchers

```java
// Matchers comuns
when(repository.save(any())).thenReturn(saved);            // qualquer argumento
when(repository.save(any(Patient.class))).thenReturn(saved); // qualquer Patient
when(repository.findByEmail(anyString())).thenReturn(Optional.empty());
when(repository.findByEmail(eq("maria@example.com"))).thenReturn(Optional.of(maria));

// Matcher customizado
when(repository.findByAge(intThat(age -> age > 60))).thenReturn(seniors);

// Matcher com argThat
when(repository.save(argThat(p -> p.name().startsWith("Dr."))))
    .thenReturn(doctor);
```

**Regra:** se usa matcher em um argumento, **todos** os outros também devem ser matchers. `when(x.foo(eq(1), matcher))` funciona, `when(x.foo(1, matcher))` falha.

### Verify

```java
// Foi chamado (pelo menos uma vez)
verify(repository).save(any(Patient.class));

// Número específico de vezes
verify(notifier, times(3)).send(anyString());
verify(notifier, never()).send("admin@example.com");
verify(notifier, atLeast(1)).send(anyString());
verify(notifier, atMost(5)).send(anyString());

// Não houve interação
verifyNoInteractions(unusedMock);

// Nenhuma outra interação além das verificadas
verify(notifier).send("user1@example.com");
verify(notifier).send("user2@example.com");
verifyNoMoreInteractions(notifier);

// Ordem importa (InOrder)
InOrder inOrder = inOrder(repository, notifier);
inOrder.verify(repository).save(any());
inOrder.verify(notifier).send(anyString());
```

### ArgumentCaptor

Captura argumentos passados para um mock, permitindo asserções detalhadas.

```java
@Test
void shouldCreatePatientWithNormalizedEmail() {
    // given
    var request = new CreatePatientRequest("Maria", "MARIA@EXAMPLE.COM  ");
    ArgumentCaptor<Patient> captor = ArgumentCaptor.forClass(Patient.class);

    // when
    service.create(request);

    // then
    verify(repository).save(captor.capture());
    Patient captured = captor.getValue();

    assertThat(captured.name()).isEqualTo("Maria");
    assertThat(captured.email()).isEqualTo("maria@example.com");  // normalizado
}
```

### Spy

```java
@Test
void shouldUseRealImplementationExceptForOneMethod() {
    List<String> spy = spy(new ArrayList<>());
    spy.add("one");  // comportamento real
    spy.add("two");

    when(spy.size()).thenReturn(100);  // stub override

    assertThat(spy.size()).isEqualTo(100);  // mockado
    assertThat(spy.get(0)).isEqualTo("one");  // real
}
```

**Cuidado com spies:** use `doReturn().when(spy)` em vez de `when(spy).thenReturn()` para métodos que têm side effects.

### Mockando static methods (Mockito 5+)

Mockito moderno suporta mock de static sem PowerMock.

```java
@Test
void shouldMockStaticMethod() {
    try (MockedStatic<Instant> mocked = mockStatic(Instant.class)) {
        Instant fixed = Instant.parse("2026-04-10T12:00:00Z");
        mocked.when(Instant::now).thenReturn(fixed);

        assertThat(Instant.now()).isEqualTo(fixed);
    }
    // Fora do try, comportamento volta ao normal
}
```

**Use com parcimônia** — mockar static é frequentemente sinal de design testável ruim. Prefira injetar `Clock` ou `Supplier<Instant>`.

### Anti-patterns Mockito

```java
// RUIM — mockar value object
Patient mock = mock(Patient.class);  // Patient é simples, não precisa mock

// RUIM — mockar para testar getters/setters
when(patient.getName()).thenReturn("Maria");
// → Use um Patient real

// RUIM — mocks demais
// Se você tem 5+ mocks em um teste, provavelmente o código sob teste faz coisas demais

// RUIM — verify em tudo
verify(repo).save(any());  // OK
verify(repo).findById(1L); // OK
verify(repo).count();      // frágil — acoplado à implementação

// BOM — verify só o que importa para o contrato
```

---

## Spring Boot Testing

Spring Boot oferece **test slices** — configurações minimalistas que carregam só o que você precisa testar.

### Slices disponíveis

| Slice | Carrega | Use case |
| --- | --- | --- |
| `@SpringBootTest` | Contexto completo | Integration tests |
| `@WebMvcTest` | Só web layer (controllers) | Testar controllers isoladamente |
| `@DataJpaTest` | JPA + H2 in-memory | Testar repositories |
| `@JdbcTest` | JDBC + H2 | Testar DAOs JDBC |
| `@JsonTest` | Jackson / ObjectMapper | Testar serialização |
| `@RestClientTest` | RestTemplate / WebClient | Testar clients HTTP |
| `@DataRedisTest` | Redis template | Testar Redis |
| `@WebFluxTest` | Spring WebFlux routes | Testar reactive controllers |

### @WebMvcTest — testando controllers

```java
@WebMvcTest(PatientController.class)
class PatientControllerTest {

    @Autowired
    private MockMvc mockMvc;

    @MockitoBean  // Spring Boot 3.4+; antes: @MockBean (deprecated)
    private PatientService service;

    @Test
    void shouldReturnPatientById() throws Exception {
        // given
        when(service.findById(1L)).thenReturn(new Patient(1L, "Maria"));

        // when + then
        mockMvc.perform(get("/patients/1"))
            .andExpect(status().isOk())
            .andExpect(jsonPath("$.id").value(1))
            .andExpect(jsonPath("$.name").value("Maria"));
    }

    @Test
    void shouldReturn404WhenNotFound() throws Exception {
        when(service.findById(999L))
            .thenThrow(new PatientNotFoundException(999L));

        mockMvc.perform(get("/patients/999"))
            .andExpect(status().isNotFound())
            .andExpect(jsonPath("$.title").value("Resource Not Found"));
    }

    @Test
    void shouldReturn422OnInvalidRequest() throws Exception {
        String badJson = """
            {"name": "", "email": "not-an-email"}
            """;

        mockMvc.perform(post("/patients")
                .contentType(MediaType.APPLICATION_JSON)
                .content(badJson))
            .andExpect(status().isUnprocessableEntity())
            .andExpect(jsonPath("$.errors[*].field")
                .value(containsInAnyOrder("name", "email")));
    }
}
```

**`@WebMvcTest` carrega apenas:** controllers, ControllerAdvice, filters, converters. **Não** carrega services, repositories, configurações não-web.

### @DataJpaTest — testando repositories

```java
@DataJpaTest
@Testcontainers
@AutoConfigureTestDatabase(replace = AutoConfigureTestDatabase.Replace.NONE)
class PatientRepositoryTest {

    @Container
    @ServiceConnection  // Spring Boot 3.1+ — auto-configura datasource
    static PostgreSQLContainer<?> postgres = new PostgreSQLContainer<>("postgres:16");

    @Autowired
    private PatientRepository repository;

    @Autowired
    private TestEntityManager em;

    @Test
    void shouldFindByEmail() {
        // given
        em.persist(new Patient("Maria", "maria@example.com"));
        em.flush();

        // when
        var result = repository.findByEmail("maria@example.com");

        // then
        assertThat(result).isPresent();
        assertThat(result.get().getName()).isEqualTo("Maria");
    }

    @Test
    void shouldReturnEmptyWhenEmailNotFound() {
        var result = repository.findByEmail("ghost@example.com");
        assertThat(result).isEmpty();
    }
}
```

**`@DataJpaTest`:**
- Por default, substitui datasource por H2 in-memory (use `Replace.NONE` para Testcontainers)
- Cada teste roda em transação, rollback automático ao final
- Carrega só configurações JPA

### @SpringBootTest — integration test completo

```java
@SpringBootTest(webEnvironment = SpringBootTest.WebEnvironment.RANDOM_PORT)
@Testcontainers
@AutoConfigureMockMvc
class PatientIntegrationTest {

    @Container
    @ServiceConnection
    static PostgreSQLContainer<?> postgres = new PostgreSQLContainer<>("postgres:16");

    @Container
    @ServiceConnection
    static RedisContainer redis = new RedisContainer("redis:7");

    @Autowired
    private MockMvc mockMvc;

    @Autowired
    private PatientRepository repository;

    @Test
    void shouldCreatePatientEndToEnd() throws Exception {
        String json = """
            {"name": "Maria", "email": "maria@example.com", "birthDate": "1985-03-15"}
            """;

        // Criar via controller
        String response = mockMvc.perform(post("/patients")
                .contentType(MediaType.APPLICATION_JSON)
                .content(json))
            .andExpect(status().isCreated())
            .andReturn().getResponse().getContentAsString();

        Patient created = objectMapper.readValue(response, Patient.class);

        // Verificar no banco
        var saved = repository.findById(created.getId());
        assertThat(saved).isPresent();
        assertThat(saved.get().getEmail()).isEqualTo("maria@example.com");
    }
}
```

### WebEnvironment options

- `MOCK` (default) — MockMvc, sem servidor real
- `RANDOM_PORT` — servidor real em porta aleatória
- `DEFINED_PORT` — servidor real em porta de `application.properties`
- `NONE` — sem web

### Profiles de teste

```java
@SpringBootTest
@ActiveProfiles("test")
class MyIntegrationTest { ... }
```

```yaml
# application-test.yml
spring:
  jpa:
    show-sql: true
logging:
  level:
    com.example: DEBUG
```

### TestRestTemplate vs WebTestClient vs MockMvc

- **MockMvc** — para `@WebMvcTest`, sem servidor (fast)
- **TestRestTemplate** — servidor real, HTTP sobre sockets, Spring MVC
- **WebTestClient** — reactive, funciona com MVC também

---

## Testcontainers

Infraestrutura real em containers Docker durante testes. **Substituiu completamente H2 e outros in-memory databases**.

### Por que Testcontainers

**H2 (antigo padrão):**
- ❌ Schema SQL subtly diferente de PostgreSQL
- ❌ Features de PostgreSQL (JSONB, arrays, window functions) não funcionam
- ❌ Testes passam, produção quebra
- ✅ Rápido

**Testcontainers:**
- ✅ Mesma versão exata de Postgres da produção
- ✅ Features específicas funcionam
- ✅ Confiança altíssima
- ⚠️ Startup lento (~1-2s por container, mitigável com reuse)

**Regra moderna:** use Testcontainers para testes que tocam banco. Sem exceção.

### Setup

```xml
<dependency>
    <groupId>org.testcontainers</groupId>
    <artifactId>testcontainers</artifactId>
    <version>1.19.7</version>
    <scope>test</scope>
</dependency>
<dependency>
    <groupId>org.testcontainers</groupId>
    <artifactId>postgresql</artifactId>
    <scope>test</scope>
</dependency>
<dependency>
    <groupId>org.testcontainers</groupId>
    <artifactId>junit-jupiter</artifactId>
    <scope>test</scope>
</dependency>
```

### Usando (Spring Boot 3.1+)

```java
@SpringBootTest
@Testcontainers
class AppTest {

    @Container
    @ServiceConnection  // auto-configura datasource Spring
    static PostgreSQLContainer<?> postgres = new PostgreSQLContainer<>("postgres:16");

    @Container
    @ServiceConnection
    static GenericContainer<?> redis = new GenericContainer<>("redis:7")
        .withExposedPorts(6379);

    @Container
    @ServiceConnection
    static KafkaContainer kafka = new KafkaContainer("confluentinc/cp-kafka:7.6.0");

    @Test
    void test() { ... }
}
```

**`@ServiceConnection`** (Spring Boot 3.1+) é mágico — auto-detecta o tipo do container e configura o `application.properties` correspondente.

### Singleton pattern (reuse entre testes)

Startup de container é lento. Para evitar recriá-lo por classe de teste:

```java
public abstract class AbstractIntegrationTest {

    static final PostgreSQLContainer<?> postgres = new PostgreSQLContainer<>("postgres:16");

    static {
        postgres.start();  // inicia uma vez, compartilha
    }

    @DynamicPropertySource
    static void configureProperties(DynamicPropertyRegistry registry) {
        registry.add("spring.datasource.url", postgres::getJdbcUrl);
        registry.add("spring.datasource.username", postgres::getUsername);
        registry.add("spring.datasource.password", postgres::getPassword);
    }
}

@SpringBootTest
class PatientTest extends AbstractIntegrationTest { ... }

@SpringBootTest
class OrderTest extends AbstractIntegrationTest { ... }
// Ambos reutilizam o mesmo container postgres
```

### Testcontainers reuse (local dev)

Para reusar containers entre `mvn test` runs (acelera dev local):

```properties
# ~/.testcontainers.properties
testcontainers.reuse.enable=true
```

```java
static PostgreSQLContainer<?> postgres = new PostgreSQLContainer<>("postgres:16")
    .withReuse(true);  // marca para reuso
```

### Containers disponíveis

Testcontainers tem modules prontos para: PostgreSQL, MySQL, MongoDB, Redis, Kafka, RabbitMQ, Elasticsearch, Cassandra, Neo4j, MinIO, Selenium, LocalStack (AWS), ...

```java
// Kafka
@Container
static KafkaContainer kafka = new KafkaContainer("confluentinc/cp-kafka:7.6.0");

// LocalStack (S3, SQS, SNS, etc.)
@Container
static LocalStackContainer localStack = new LocalStackContainer("3.0")
    .withServices(S3, SQS);

// Custom image
@Container
static GenericContainer<?> custom = new GenericContainer<>("myapp:latest")
    .withExposedPorts(8080)
    .withEnv("KEY", "value")
    .waitingFor(Wait.forHttp("/health"));
```

---

## Mocking HTTP externo: WireMock

Para testar integrações com APIs externas sem depender delas.

```java
@SpringBootTest
class ExternalApiClientTest {

    static WireMockServer wireMock;

    @BeforeAll
    static void setupWireMock() {
        wireMock = new WireMockServer(options().dynamicPort());
        wireMock.start();
    }

    @AfterAll
    static void tearDownWireMock() {
        wireMock.stop();
    }

    @DynamicPropertySource
    static void configure(DynamicPropertyRegistry registry) {
        registry.add("external.api.base-url", () -> "http://localhost:" + wireMock.port());
    }

    @Test
    void shouldHandleExternalApiResponse() {
        // Stub
        wireMock.stubFor(get("/users/42")
            .willReturn(ok()
                .withHeader("Content-Type", "application/json")
                .withBody("""
                    {"id": 42, "name": "External Maria"}
                    """)));

        // Act
        var result = client.fetchUser(42);

        // Assert
        assertThat(result.name()).isEqualTo("External Maria");

        // Verify call was made
        wireMock.verify(getRequestedFor(urlEqualTo("/users/42")));
    }

    @Test
    void shouldRetryOnServerError() {
        wireMock.stubFor(get("/users/42")
            .inScenario("retry")
            .whenScenarioStateIs(STARTED)
            .willReturn(serverError())
            .willSetStateTo("second-attempt"));

        wireMock.stubFor(get("/users/42")
            .inScenario("retry")
            .whenScenarioStateIs("second-attempt")
            .willReturn(ok().withBody("{\"id\":42}")));

        var result = client.fetchUserWithRetry(42);
        assertThat(result.id()).isEqualTo(42);

        wireMock.verify(2, getRequestedFor(urlEqualTo("/users/42")));
    }
}
```

**Alternativa moderna:** `MockServer`, `Hoverfly`, ou — para projetos Spring — `@RestClientTest` com `MockRestServiceServer`.

---

## Testando código assíncrono: Awaitility

Polling declarativo para testar condições eventuais.

```java
@Test
void shouldEventuallyProcessMessage() {
    // given
    kafkaTemplate.send("orders", orderEvent);

    // when + then — espera condição ficar verdadeira
    Awaitility.await()
        .atMost(10, SECONDS)
        .pollInterval(Duration.ofMillis(100))
        .untilAsserted(() -> {
            var order = orderRepository.findById(orderEvent.orderId());
            assertThat(order).isPresent();
            assertThat(order.get().getStatus()).isEqualTo(OrderStatus.PROCESSED);
        });
}
```

**Evite `Thread.sleep()` em testes** — é fonte constante de flakiness. Awaitility resolve corretamente.

---

## ArchUnit: testes de arquitetura

Regras arquiteturais expressas como testes. **Fitness functions** — falham o build se alguém quebrar boundaries.

```java
import com.tngtech.archunit.junit.AnalyzeClasses;
import com.tngtech.archunit.junit.ArchTest;
import com.tngtech.archunit.lang.ArchRule;
import static com.tngtech.archunit.lang.syntax.ArchRuleDefinition.*;

@AnalyzeClasses(packages = "com.example.app")
class ArchitectureTest {

    @ArchTest
    static final ArchRule controllers_should_not_depend_on_repositories =
        noClasses()
            .that().resideInAPackage("..controller..")
            .should().dependOnClassesThat().resideInAPackage("..repository..");

    @ArchTest
    static final ArchRule services_should_be_annotated =
        classes()
            .that().resideInAPackage("..service..")
            .and().haveSimpleNameEndingWith("Service")
            .should().beAnnotatedWith(Service.class);

    @ArchTest
    static final ArchRule layer_dependencies_are_respected =
        layeredArchitecture()
            .consideringAllDependencies()
            .layer("Controller").definedBy("..controller..")
            .layer("Service").definedBy("..service..")
            .layer("Repository").definedBy("..repository..")
            .whereLayer("Controller").mayNotBeAccessedByAnyLayer()
            .whereLayer("Service").mayOnlyBeAccessedByLayers("Controller")
            .whereLayer("Repository").mayOnlyBeAccessedByLayers("Service");

    @ArchTest
    static final ArchRule no_cycles =
        slices().matching("..(*)..")
            .should().beFreeOfCycles();

    @ArchTest
    static final ArchRule repositories_extend_jpa_repository =
        classes()
            .that().resideInAPackage("..repository..")
            .and().areInterfaces()
            .should().beAssignableTo(JpaRepository.class);
}
```

**Uso típico:** adicionar uma regra por cada violação arquitetural que você detecta. Com o tempo, constrói um guardrail contra drift.

---

## PIT (Pitest): Mutation testing

Valida a **qualidade dos seus testes** introduzindo mutações no código e verificando se os testes pegam.

```xml
<plugin>
    <groupId>org.pitest</groupId>
    <artifactId>pitest-maven</artifactId>
    <version>1.16.0</version>
    <dependencies>
        <dependency>
            <groupId>org.pitest</groupId>
            <artifactId>pitest-junit5-plugin</artifactId>
            <version>1.2.1</version>
        </dependency>
    </dependencies>
</plugin>
```

```bash
mvn org.pitest:pitest-maven:mutationCoverage
```

**O que PIT faz:**
1. Modifica bytecode (ex.: `>` → `>=`, remove `return`, nega condição)
2. Roda seus testes contra o código mutado
3. Se testes passam → mutação sobreviveu → seus testes não são bons
4. Se testes falham → mutação morta → bom teste

**Output:** relatório HTML com % de mutações mortas. **Mutation coverage é métrica muito melhor que line coverage.**

**Caveat:** lento. Execute no CI em testes nightly, não em cada build.

---

## Contract Testing: Pact

Valida contratos entre consumer e producer sem testes end-to-end frágeis.

**Consumer** define expectativas:

```java
@ExtendWith(PactConsumerTestExt.class)
@PactTestFor(providerName = "patient-service")
class PatientClientConsumerTest {

    @Pact(consumer = "billing-service")
    public RequestResponsePact patientExists(PactDslWithProvider builder) {
        return builder
            .given("patient with id 42 exists")
            .uponReceiving("get patient by id")
                .path("/patients/42")
                .method("GET")
            .willRespondWith()
                .status(200)
                .body(new PactDslJsonBody()
                    .numberValue("id", 42)
                    .stringValue("name", "Maria"))
            .toPact();
    }

    @Test
    @PactTestFor(pactMethod = "patientExists")
    void shouldFetchPatient(MockServer mockServer) {
        PatientClient client = new PatientClient(mockServer.getUrl());
        Patient patient = client.findById(42L);

        assertThat(patient.name()).isEqualTo("Maria");
    }
}
```

**Producer** verifica que cumpre o contrato:

```java
@Provider("patient-service")
@PactFolder("pacts")
class PatientServiceProviderTest {

    @BeforeEach
    void setup(PactVerificationContext context) {
        context.setTarget(new HttpTestTarget("localhost", 8080));
    }

    @TestTemplate
    @ExtendWith(PactVerificationInvocationContextProvider.class)
    void verifyPact(PactVerificationContext context) {
        context.verifyInteraction();
    }

    @State("patient with id 42 exists")
    void patientExists() {
        // setup no banco
    }
}
```

**Benefício:** se o producer quebra o contrato, o build falha, sem precisar rodar os dois serviços juntos em ambiente integrado.

---

## Test data builders

Evite construtores com 15 argumentos em testes. Use builders para legibilidade:

```java
public class PatientBuilder {
    private Long id = 1L;
    private String name = "Default Name";
    private String email = "default@example.com";
    private LocalDate birthDate = LocalDate.of(1990, 1, 1);

    public static PatientBuilder aPatient() {
        return new PatientBuilder();
    }

    public PatientBuilder withId(Long id) { this.id = id; return this; }
    public PatientBuilder withName(String name) { this.name = name; return this; }
    public PatientBuilder withEmail(String email) { this.email = email; return this; }
    public PatientBuilder withBirthDate(LocalDate d) { this.birthDate = d; return this; }

    public PatientBuilder asAdult() { this.birthDate = LocalDate.now().minusYears(30); return this; }
    public PatientBuilder asMinor() { this.birthDate = LocalDate.now().minusYears(10); return this; }

    public Patient build() {
        return new Patient(id, name, email, birthDate);
    }
}

// Uso
@Test
void shouldDetectMinorAsNonAdult() {
    Patient minor = aPatient().withName("Kid").asMinor().build();
    assertThat(service.isAdult(minor)).isFalse();
}
```

**Ou:** use bibliotecas como [Instancio](https://www.instancio.org/) para gerar objetos com valores default automáticos.

---

## Testing exceptions, logs, and side effects

### Capturar logs (para asserção)

Com SLF4J + Logback:

```java
@Test
void shouldLogError() {
    var logger = (Logger) LoggerFactory.getLogger(MyService.class);
    var listAppender = new ListAppender<ILoggingEvent>();
    listAppender.start();
    logger.addAppender(listAppender);

    service.doSomethingThatLogs();

    assertThat(listAppender.list)
        .extracting(ILoggingEvent::getMessage)
        .contains("Expected log message");
}
```

**Alternativa:** `LogCaptor` library, mais simples.

### Testando System.out

```java
@Test
void shouldPrintMessage(CapturedOutput output) {  // JUnit 5 extension
    service.printReport();
    assertThat(output).contains("Report generated");
}
```

Requer Spring Boot Test — `@ExtendWith(OutputCaptureExtension.class)`.

### Fixing time em testes

```java
// RUIM
@Service
public class OrderService {
    public boolean isExpired(Order o) {
        return o.createdAt().plusDays(30).isBefore(LocalDate.now());  // hardcoded
    }
}

// BOM — injetar Clock
@Service
public class OrderService {
    private final Clock clock;

    public OrderService(Clock clock) { this.clock = clock; }

    public boolean isExpired(Order o) {
        return o.createdAt().plusDays(30).isBefore(LocalDate.now(clock));
    }
}

// Teste
@Test
void shouldDetectExpiredOrder() {
    Clock fixed = Clock.fixed(Instant.parse("2026-05-01T00:00:00Z"), ZoneOffset.UTC);
    var service = new OrderService(fixed);

    Order order = new Order(LocalDate.of(2026, 3, 1));  // 2 meses atrás
    assertThat(service.isExpired(order)).isTrue();
}
```

---

## Performance: JMH

Para medir performance corretamente, use **JMH (Java Microbenchmark Harness)**. Ele lida com warmup, JIT, dead code elimination e outros artefatos.

```java
@BenchmarkMode(Mode.AverageTime)
@OutputTimeUnit(TimeUnit.NANOSECONDS)
@Warmup(iterations = 5)
@Measurement(iterations = 10)
@Fork(2)
@State(Scope.Thread)
public class StringConcatBenchmark {

    @Param({"10", "100", "1000"})
    private int size;

    @Benchmark
    public String plusConcatenation() {
        String result = "";
        for (int i = 0; i < size; i++) {
            result += i;
        }
        return result;
    }

    @Benchmark
    public String stringBuilder() {
        StringBuilder sb = new StringBuilder();
        for (int i = 0; i < size; i++) {
            sb.append(i);
        }
        return sb.toString();
    }

    public static void main(String[] args) throws Exception {
        org.openjdk.jmh.Main.main(args);
    }
}
```

**Nunca use `System.nanoTime()` em `@Test` para medir performance** — o JIT vai te enganar.

---

## Estratégia de testes em projeto Spring Boot

**Pirâmide prática:**

```
     ┌─────────────┐
     │  E2E (raros)│   ← Selenide/Playwright em fluxos críticos
     └─────────────┘
   ┌─────────────────┐
   │ Integration (muitos) │   ← @SpringBootTest + Testcontainers
   └───────────────────┘
 ┌─────────────────────────┐
 │ Slice tests             │   ← @WebMvcTest, @DataJpaTest
 └─────────────────────────┘
┌───────────────────────────┐
│ Unit tests (muitos)       │   ← POJOs, services, utilities
└───────────────────────────┘
```

**Distribuição típica de um projeto saudável:**
- **70-80% unit tests** — rápidos, sem Spring context
- **15-25% integration tests** — Testcontainers, slices Spring
- **2-5% E2E** — fluxos críticos de negócio

**Tempo de suite:**
- Unit: milissegundos por teste, suite total < 30s
- Slice: centenas de ms por teste, suite < 2min
- Integration: segundos por teste, suite < 5min
- Total no CI: < 10min

**Regras práticas:**
- **Unit tests:** não usem Spring — `new Service(mockRepo)` direto
- **Service tests com mocks:** quando lógica é rica mas dependências são simples
- **Integration tests:** quando lógica atravessa camadas (controller → service → DB)
- **E2E:** só fluxos que pagam pelo custo (checkout, login, onboarding)

---

## Armadilhas comuns

- **H2 em vez de Testcontainers** — testes passam, produção quebra com SQL incompatível
- **Mocks para tudo** — se você mocka a metade do mundo para testar uma classe, seu código tem acoplamento excessivo
- **Test coverage como meta** — 100% sem asserções é inútil. Prefira mutation testing.
- **Testes que dependem de ordem** — sempre independentes. `@TestMethodOrder` é code smell (exceto em integration tests específicos)
- **`Thread.sleep()` em testes** — flakiness garantida. Use Awaitility.
- **Testes lentos no CI** — times desligam, testes morrem. Mantenha suite rápida.
- **Mockar tipos de terceiros** (banco, S3) sem integração real — teste passa, produção quebra
- **Mutação de estado estático em testes** — contamina outros testes. Use `@DirtiesContext` ou reset explícito.
- **Ignorar testes com `@Disabled` sem prazo** — vira cemitério. PR review deve questionar.
- **Testes que testam mocks** — `verify(mock).foo()` seguido de `when(mock.foo()).thenReturn(...)` — tautológico
- **Assertions sem mensagem em falhas** — AssertJ resolve isso, mas `assertTrue(flag)` sem mensagem é inútil
- **Setup duplicado entre testes** — extraia para `@BeforeEach` ou builders
- **Teste que testa demais** — um teste = um comportamento. Se você precisa de 3 asserts não relacionados, faça 3 testes.
- **Mockar classes finais sem configurar** — Mockito moderno suporta, mas verifique `mockito-inline` no classpath
- **`@SpringBootTest` para teste unitário** — carrega contexto inteiro para testar um método. Use `@WebMvcTest` ou sem Spring.
- **Esquecer rollback em integration tests** — estado vaza para outros testes. `@Transactional` em teste causa rollback automático.
- **Testar implementação em vez de comportamento** — `verify(repo, times(3)).save(any())` é frágil. Verifique o efeito observável.
- **Tests que só rodam "na minha máquina"** — dependem de DB local, porta específica, variáveis de ambiente. Testcontainers resolve.
- **Ignorar testes flaky** — "roda de novo que passa" é dívida técnica. Investigue a causa.

---

## Na prática (da minha experiência)

> **MedEspecialista — evolução da stack de testes:**
>
> Quando comecei o projeto, a stack de testes era JUnit 4 + Hamcrest + H2 in-memory. Funcionava, mas tinha problemas:
>
> **1. Migração JUnit 4 → JUnit 5:** a arquitetura do JUnit 5 é superior — extensions, parameterized tests muito mais expressivos, `@Nested`, `@DisplayName`. Migração gradual, rodando ambos lado a lado via `junit-vintage-engine`.
>
> **2. H2 → Testcontainers:** a dor veio quando uma query com JSONB funcionava em H2 mas quebrava no Postgres. Testcontainers resolveu. Startup lento? Sim. Mas vale cada segundo pela confiança. Com `@ServiceConnection` (Spring Boot 3.1+), o setup é trivial.
>
> **3. Hamcrest → AssertJ:** `assertThat(list, hasSize(3))` vs `assertThat(list).hasSize(3).contains(expected)`. AssertJ é muito mais fluente, IDE completa melhor, mensagens de erro são mais claras. Migração em minutos.
>
> **4. ArchUnit para fitness functions:** adicionei regras de arquitetura:
> - Controllers não podem depender de Repositories
> - Cada bounded context só acessa o outro via interface pública
> - Sem ciclos entre packages
>
> Isso previne drift arquitetural. Toda vez que alguém tenta pular uma camada, o build falha com mensagem clara.
>
> **5. Pyramid balance:** comecei com muitos `@SpringBootTest` (fácil, preguiçoso). Suite demorava 5 minutos. Refatorei para mais unit tests puros e `@WebMvcTest` / `@DataJpaTest` slices. Suite caiu para 1:30, CI ficou responsivo, devs param de desligar testes.
>
> **6. Contract testing com Pact:** integração entre 3 microserviços era dor de cabeça. Testes E2E passavam hoje, quebravam amanhã. Implementei Pact — consumer gera pact, producer valida. Quebras de contrato agora falham no build do producer antes do merge.
>
> **7. Mutation testing com PIT:** rodei uma vez para ver onde os testes eram fracos. Descobri que 30% das mutações sobreviviam, mesmo com 85% de line coverage. Os testes validavam "o código executa" mas não "o resultado está correto". Melhorei asserções baseado no relatório. PIT não roda em cada build (lento), mas uma vez por semana no nightly.
>
> **Incidente de flakiness:** um teste de Kafka falhava aleatoriamente. Consumer async nem sempre processava antes do assert. Corrigi com Awaitility — `await().atMost(5, SECONDS).untilAsserted(...)`. Nunca mais flaky. Moral: `Thread.sleep()` é sempre bug escondido.
>
> **Testcontainers reuse:** com `testcontainers.reuse.enable=true` e `.withReuse(true)` no container, o Postgres fica rodando entre test runs em dev local. Acelerou o ciclo de feedback de minutos para segundos.
>
> **A lição principal:** testes são código de produção. Eles protegem você, devem ser legíveis, rápidos, e dar feedback claro. Investir em boa stack de testes e fitness functions paga por si mesmo em meses — em menos bugs em produção, menos medo de refactoring, e mais velocidade sustentável.

---

## How to explain in English

> "My testing strategy in Java follows the classic pyramid: lots of unit tests, a meaningful layer of integration tests, and a few E2E tests for critical flows. The stack I use is JUnit 5 with AssertJ for assertions, Mockito for mocks, Testcontainers for real infrastructure, and Spring Boot test slices when testing Spring-specific layers.
>
> For unit tests, I don't involve Spring at all. I instantiate the class directly with its dependencies and use Mockito for collaborators. This keeps unit tests fast — milliseconds each — and forces good design because classes with too many dependencies become hard to test.
>
> For the repository layer, I use `@DataJpaTest` with Testcontainers running a real PostgreSQL instance. H2 in-memory used to be the standard, but it has enough SQL dialect differences from Postgres that you get false positives — tests pass locally, production breaks. Testcontainers eliminates that risk.
>
> For controllers, I use `@WebMvcTest` with MockMvc. This loads only the web layer — controllers, exception handlers, serialization — and I mock the service layer. It's fast and focused. For full-stack integration tests, I use `@SpringBootTest` with Testcontainers for database, Redis, Kafka — whatever the app depends on.
>
> I use AssertJ for all assertions because its fluent API is vastly more readable than JUnit's built-in. `assertThat(result).isNotNull().hasSize(3).extracting(User::name).contains("Maria")` is self-documenting. And AssertJ's error messages are detailed enough to debug without running the test again.
>
> I enforce architecture with ArchUnit — fitness functions that fail the build when someone violates layer boundaries or introduces cycles. It's guardrails against architectural drift. And I run PIT mutation testing occasionally to validate that my tests actually catch bugs, not just execute lines.
>
> For async code, I use Awaitility instead of `Thread.sleep`. Sleep in tests is always a latent flaky test. Awaitility polls a condition until it's true or a timeout expires, which handles the uncertainty correctly.
>
> Finally, for contract testing between services, I use Pact. It lets consumers declare their expectations as tests, producers verify they meet those expectations in their own build — breaking contracts fail before they reach production."

### Frases úteis em entrevista

- "I follow the test pyramid: lots of unit tests, meaningful integration layer, few E2E."
- "I use Testcontainers for database tests, never H2 — SQL dialect differences cause false positives."
- "AssertJ's fluent API is much more readable than JUnit's built-in assertions."
- "I use `@WebMvcTest` for controller tests, `@DataJpaTest` for repositories, `@SpringBootTest` for full integration."
- "For unit tests, I don't load Spring at all — instantiate directly with mocks."
- "ArchUnit is my guardrail against architectural drift — layer boundaries enforced by tests."
- "I use PIT mutation testing occasionally to validate my tests are actually catching bugs."
- "For async code, Awaitility replaces Thread.sleep — no more flaky tests."
- "Pact contract tests catch breaking changes at the producer build, before they reach production."
- "I inject Clock instead of calling LocalDateTime.now() — tests can then control time."
- "Mutation coverage is a much better metric than line coverage."

### Key vocabulary

- teste unitário → unit test
- teste de integração → integration test
- teste de ponta a ponta → end-to-end test (E2E)
- fatia de teste → test slice
- pirâmide de testes → test pyramid
- asserção → assertion
- simulação → mock
- espião → spy
- substituto → fake / stub
- captor de argumentos → argument captor
- cobertura de testes → test coverage
- cobertura de mutação → mutation coverage
- teste de contrato → contract testing
- teste de arquitetura → architecture test
- função de fitness → fitness function
- teste flácido → flaky test
- teste parametrizado → parameterized test
- duplo de teste → test double
- configuração de teste → test fixture / setup
- dado-quando-então → given-when-then (AAA — arrange, act, assert)

---

## Recursos

### Livros

- **Effective Unit Testing** — Lasse Koskela (princípios)
- **Growing Object-Oriented Software, Guided by Tests** — Freeman & Pryce (TDD avançado)
- **Unit Testing Principles, Practices, and Patterns** — Vladimir Khorikov (excelente)
- **xUnit Test Patterns** — Gerard Meszaros (o catálogo de patterns)

### Documentação

- [JUnit 5 User Guide](https://junit.org/junit5/docs/current/user-guide/)
- [AssertJ Documentation](https://assertj.github.io/doc/)
- [Mockito Documentation](https://site.mockito.org/)
- [Testcontainers Documentation](https://testcontainers.com/)
- [Spring Boot Testing](https://docs.spring.io/spring-boot/reference/testing/index.html)
- [ArchUnit User Guide](https://www.archunit.org/userguide/html/000_Index.html)
- [Awaitility](https://github.com/awaitility/awaitility)
- [WireMock Documentation](https://wiremock.org/)
- [Pact Documentation](https://docs.pact.io/)
- [PIT Mutation Testing](https://pitest.org/)
- [JMH](https://openjdk.org/projects/code-tools/jmh/)

### Artigos

- [Baeldung — JUnit 5 vs JUnit 4](https://www.baeldung.com/junit-5-migration)
- [Baeldung — Mockito tutorials](https://www.baeldung.com/tag/mockito)
- [Testcontainers — Spring Boot integration](https://testcontainers.com/guides/testing-spring-boot-rest-api-using-testcontainers/)
- [Martin Fowler — TestPyramid](https://martinfowler.com/bliki/TestPyramid.html)
- [Martin Fowler — UnitTest](https://martinfowler.com/bliki/UnitTest.html)
- [Martin Fowler — Mocks Aren't Stubs](https://martinfowler.com/articles/mocksArentStubs.html)

---

## Veja também

- [[Testes]] — fundamentos gerais (pirâmide, tipos, estratégia)
- [[Java Fundamentals]] — a linguagem
- [[Java Concurrency]] — testando código concorrente
- [[Spring Boot]] — setup e slices de teste
- [[API Design]] — contract testing, RFC 9457
- [[Arquitetura de Software]] — fitness functions, ArchUnit
- [[Banco de dados]] — Testcontainers, rollback, migrations
- [[03-Dominios/Java/Backend/Kafka/Kafka]] — testando consumers e producers
