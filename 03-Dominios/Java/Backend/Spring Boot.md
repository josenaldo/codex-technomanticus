---
title: "Spring Boot"
created: 2026-04-01
updated: 2026-06-10
type: concept
progress: backlog
status: evergreen
tags:
  - java
  - backend
  - entrevista
publish: false
---

# Spring Boot

O framework Java dominante para microserviços e aplicações web. Spring Boot é construído sobre o **Spring Framework**, adicionando **autoconfiguração**, **servidor embarcado**, **starters** de dependências, e **production-ready features** (Actuator, métricas). Para deep dive em persistência, ver [[Spring Data JPA]]. Para segurança, ver [[Spring Security]]. Para deep dive em testes, ver [[Testes em Java]].

## O que é

> [!nota] Migrado para galho próprio
> Os fundamentos de Spring (Framework vs Boot, o stack, convention-over-configuration) foram expandidos no galho [[03-Dominios/Java/Spring Core e Boot/index|Spring Core e Boot]]. Veja [[03-Dominios/Java/Spring Core e Boot/01 - O que é Spring — Framework, Boot e o ecossistema|O que é Spring]].

Spring Boot (lançado em 2014 por Pivotal/VMware, hoje Broadcom) simplifica radicalmente o Spring — elimina XML de configuração, gera projetos com `start.spring.io`, e permite executar uma aplicação web completa com `java -jar app.jar`. É o framework Java de facto para backend moderno.

O stack canônico Spring:

```
┌──────────────────────────────────────────────────────────────┐
│                    Spring Boot                                │
│  (autoconfig, starters, Actuator, embedded server, CLI)       │
├──────────────────────────────────────────────────────────────┤
│                    Spring Framework                           │
│  (IoC container, AOP, Transaction management, Spring MVC,     │
│   Spring WebFlux, Spring Expression Language, JDBC template)  │
├──────────────────────────────────────────────────────────────┤
│  Spring Data  │  Spring Security  │  Spring Cloud  │ ...      │
│  (projetos modulares adicionando features específicas)        │
└──────────────────────────────────────────────────────────────┘
```

Em entrevistas, o que diferencia um senior em Spring Boot:

1. **Entender o IoC container** — como beans são criados, lifecycle, BeanPostProcessor
2. **Dominar AOP e proxies** — como `@Transactional`, `@Async`, `@Cacheable` funcionam por baixo
3. **Transações** — propagation, isolation, rollback rules, pitfalls de self-invocation
4. **Spring MVC pipeline** — DispatcherServlet, HandlerMapping, HandlerAdapter, ViewResolver
5. **Profiles e Configuration** — hierarquia, binding para classes tipadas, ConditionalOnProperty
6. **Actuator e observabilidade** — endpoints, custom health indicators, Micrometer
7. **Testing** — slices (`@WebMvcTest`, `@DataJpaTest`), Testcontainers
8. **Spring Boot internals** — auto-configuration, `@ConditionalOnClass`, Conditional evaluation

## Spring IoC Container — deep dive

> [!nota] Migrado para galho próprio
> Expandido no galho [[03-Dominios/Java/Spring Core e Boot/index|Spring Core e Boot]]. Veja [[03-Dominios/Java/Spring Core e Boot/02 - IoC e injeção de dependência no Spring|IoC e injeção de dependência]], [[03-Dominios/Java/Spring Core e Boot/03 - Beans e estereótipos — @Component, @Service, @Repository, @Controller|Beans e estereótipos]], [[03-Dominios/Java/Spring Core e Boot/04 - Tipos de injeção — constructor, setter, field|Tipos de injeção]], [[03-Dominios/Java/Spring Core e Boot/05 - @Configuration e @Bean — definição explícita de beans|@Configuration e @Bean]], [[03-Dominios/Java/Spring Core e Boot/06 - ApplicationContext — o container e seu ciclo|ApplicationContext]], [[03-Dominios/Java/Spring Core e Boot/07 - Ciclo de vida e escopos de beans|Ciclo de vida e escopos]], [[03-Dominios/Java/Spring Core e Boot/13 - BeanPostProcessor e BeanFactoryPostProcessor|BeanPostProcessor]], [[03-Dominios/Java/Spring Core e Boot/14 - Conditional beans — @Conditional e os @ConditionalOn|Conditional beans]].

---

## AOP e proxies — a mágica por baixo

> [!nota] Migrado para galho próprio
> Expandido no galho [[03-Dominios/Java/Spring Core e Boot/index|Spring Core e Boot]]. Veja [[03-Dominios/Java/Spring Core e Boot/09 - AOP e proxies no Spring|AOP e proxies no Spring]] e [[03-Dominios/Java/Spring Core e Boot/10 - Self-invocation e os limites do proxy|Self-invocation e os limites do proxy]]. (O comportamento transacional do `@Transactional` — propagation/isolation/rollback — é coberto no Galho 10: ver [[03-Dominios/Java/Persistência de dados/12 - Transações operacionais — @Transactional propagação, isolamento, rollback, readOnly|Transações operacionais]].)

---

## Gerenciamento de transações — @Transactional deep dive

> [!nota] Migrado para galho próprio
> Expandido no galho [[03-Dominios/Java/Persistência de dados/index|Persistência de dados]]. Veja [[03-Dominios/Java/Persistência de dados/12 - Transações operacionais — @Transactional propagação, isolamento, rollback, readOnly|Transações operacionais (@Transactional)]] e [[03-Dominios/Java/Persistência de dados/13 - Locking — optimistic (@Version) e pessimistic|Locking]]. O mecanismo (proxy AOP, self-invocation) é do galho [[03-Dominios/Java/Spring Core e Boot/index|Spring Core e Boot]].

---

## Spring MVC pipeline

> [!nota] Migrado para galho próprio
> Expandido no galho [[03-Dominios/Java/Web e APIs REST/index|Web e APIs REST]]. Veja [[03-Dominios/Java/Web e APIs REST/01 - O que é Spring MVC — a camada web sobre o container|O que é Spring MVC]], [[03-Dominios/Java/Web e APIs REST/06 - O pipeline do DispatcherServlet|O pipeline do DispatcherServlet]], [[03-Dominios/Java/Web e APIs REST/07 - Content negotiation|Content negotiation]], [[03-Dominios/Java/Web e APIs REST/11 - Interceptors vs Filters|Interceptors vs Filters]] e [[03-Dominios/Java/Web e APIs REST/09 - Tratamento de exceções com @ControllerAdvice|Tratamento de exceções com @ControllerAdvice]] (com [[03-Dominios/Java/Web e APIs REST/10 - Problem Details — RFC 9457|Problem Details / RFC 9457]]).

---

## Configuração e Profiles — deep dive

> [!nota] Migrado para galho próprio
> Expandido no galho [[03-Dominios/Java/Spring Core e Boot/index|Spring Core e Boot]]. Veja [[03-Dominios/Java/Spring Core e Boot/12 - Configuração e profiles|Configuração e profiles]].

---

## Actuator — production-ready features

> [!nota] Migrado para galho próprio
> Expandido no galho [[03-Dominios/Java/Spring Core e Boot/index|Spring Core e Boot]]. Veja [[03-Dominios/Java/Spring Core e Boot/17 - Actuator e observabilidade|Actuator e observabilidade]]. (Observabilidade distribuída — OpenTelemetry, tracing — fica para o Galho 17, planejado.)

---

## Spring WebFlux — visão geral

> [!nota] Migrado para galho próprio
> Expandido no galho [[03-Dominios/Java/Programação Reativa/index|Programação Reativa]]. Veja [[03-Dominios/Java/Programação Reativa/10 - Spring WebFlux — o stack não-bloqueante sobre Netty e o DispatcherHandler|Spring WebFlux]], [[03-Dominios/Java/Programação Reativa/01 - O que é programação reativa — o modelo push, assíncrono e não-bloqueante|O que é programação reativa]] e o confronto honesto [[03-Dominios/Java/Programação Reativa/14 - Reativo vs Virtual Threads — o confronto honesto|Reativo vs Virtual Threads]].

---

## Spring Cloud — visão geral

Conjunto de projetos para microserviços distribuídos.

| Projeto | O que faz |
| --- | --- |
| **Spring Cloud Config** | Configuração centralizada (Git, Vault) |
| **Spring Cloud Netflix Eureka** | Service Discovery (deprecado, hoje usa-se Kubernetes) |
| **Spring Cloud LoadBalancer** | Client-side load balancing |
| **Spring Cloud OpenFeign** | HTTP client declarativo |
| **Spring Cloud Gateway** | API Gateway (substitui Zuul) |
| **Spring Cloud Sleuth** (deprecated) / **Micrometer Tracing** | Distributed tracing |
| **Spring Cloud Stream** | Abstração de messaging (Kafka, RabbitMQ) |
| **Spring Cloud Bus** | Eventos via broker para sincronizar configs |
| **Spring Cloud Circuit Breaker** | Abstração sobre Resilience4j / Sentinel |

### OpenFeign — HTTP client declarativo

Popular para chamadas entre microserviços:

```java
@FeignClient(name = "notification-service", url = "${notification.url}")
public interface NotificationClient {

    @PostMapping("/notifications")
    void send(@RequestBody NotificationRequest req);

    @GetMapping("/notifications/{id}")
    NotificationStatus getStatus(@PathVariable String id);
}

// Habilitar
@SpringBootApplication
@EnableFeignClients
public class App { }

// Usar
@Service
@RequiredArgsConstructor
public class OrderService {
    private final NotificationClient notifications;

    public void createOrder(Order o) {
        // ...
        notifications.send(new NotificationRequest(o.getUserId(), "Pedido criado"));
    }
}
```

**Configuração:**

```yaml
spring:
  cloud:
    openfeign:
      client:
        config:
          default:
            connect-timeout: 5000
            read-timeout: 10000
          notification-service:
            read-timeout: 30000
```

### Alternativa moderna

Em 2026, muitas equipes preferem:

- **Kubernetes Service Discovery** em vez de Eureka
- **Envoy / Istio** em vez de Spring Cloud Gateway
- **HashiCorp Vault** direto em vez de Spring Cloud Config
- **OpenTelemetry** em vez de Sleuth

Spring Cloud ainda é relevante, mas o mundo se moveu para infraestrutura declarativa.

---

## Camadas típicas de uma aplicação Spring Boot

A arquitetura em camadas canônica:

```text
┌─────────────────────────────────────────┐
│  Controller (@RestController)           │  ← HTTP, validação, @Valid
│    ↕ DTO                                │
├─────────────────────────────────────────┤
│  Service (@Service)                     │  ← Lógica de negócio, @Transactional
│    ↕ Entity / Domain object             │
├─────────────────────────────────────────┤
│  Repository (@Repository / JpaRepository)│ ← Persistência
│    ↕ SQL / JPQL                         │
├─────────────────────────────────────────┤
│  Database (PostgreSQL, MySQL, ...)      │
└─────────────────────────────────────────┘
```

**Responsabilidades:**

- **Controller** — mapeia HTTP, valida input, delega ao service, serializa response. **Sem lógica de negócio.**
- **Service** — lógica de negócio, coordenação de repositories, transações. **Sem HTTP nem JPA direto.**
- **Repository** — persistência pura. Spring Data JPA cuida do básico, queries customizadas via `@Query` ou Specifications.
- **Domain** — entidades ou records representando conceitos de negócio.

Para projetos maiores, considere Hexagonal/Clean Architecture com DDD — ver [[Arquitetura de Software]].

### Persistência (Spring Data JPA + Hibernate)

Deep dive em [[Spring Data JPA]] — JPA/Hibernate, JPQL, Criteria, projections, fetch strategies, transações, N+1, caching (L1/L2), batch operations.

**Resumo rápido:**

```java
public interface PatientRepository extends JpaRepository<Patient, Long> {
    List<Patient> findBySpecialtyAndActive(String specialty, boolean active);

    @Query("SELECT p FROM Patient p WHERE p.rating > :min ORDER BY p.rating DESC")
    List<Patient> findTopRated(@Param("min") double min);

    @EntityGraph(attributePaths = {"appointments"})
    Optional<Patient> findWithAppointmentsById(Long id);
}
```

### Spring Security

Deep dive em [[Spring Security]] — filter chain, authentication, JWT, OAuth2/OIDC, method security, CSRF, CORS.

**Resumo rápido:**

```java
@Configuration
@EnableMethodSecurity
public class SecurityConfig {

    @Bean
    public SecurityFilterChain securityFilterChain(HttpSecurity http) throws Exception {
        return http
            .authorizeHttpRequests(auth -> auth
                .requestMatchers("/api/public/**").permitAll()
                .requestMatchers("/api/admin/**").hasRole("ADMIN")
                .anyRequest().authenticated()
            )
            .oauth2ResourceServer(oauth2 -> oauth2.jwt(Customizer.withDefaults()))
            .sessionManagement(sm -> sm.sessionCreationPolicy(SessionCreationPolicy.STATELESS))
            .csrf(csrf -> csrf.disable())  // APIs stateless
            .build();
    }
}
```

### Bean Validation

Validação declarativa com anotações Jakarta Validation:

```java
public record CreatePatientRequest(
    @NotBlank String name,
    @Email @NotBlank String email,
    @Past LocalDate birthDate,
    @Size(min = 11, max = 11) String cpf
) {}

@RestController
public class PatientController {
    @PostMapping("/patients")
    public ResponseEntity<?> create(@Valid @RequestBody CreatePatientRequest req) {
        // Se validação falhar, Spring retorna 400 automaticamente
        return ResponseEntity.created(uri).body(service.create(req));
    }
}
```

**Anotações principais:** `@NotNull`, `@NotBlank`, `@NotEmpty`, `@Size`, `@Email`, `@Min`, `@Max`, `@Past`, `@Future`, `@Pattern`

**`@Valid` vs `@Validated`:** `@Valid` (Jakarta, cascata em objetos aninhados) vs `@Validated` (Spring, suporta validation groups)

**Validador customizado:**

```java
@Target(ElementType.FIELD)
@Constraint(validatedBy = CpfValidator.class)
public @interface ValidCpf {
    String message() default "CPF inválido";
}
```

> **Fontes:**
> - [Validation in Spring Boot — Baeldung](https://www.baeldung.com/spring-boot-bean-validation)
> - [Bean Validation Basics — Baeldung](https://www.baeldung.com/java-validation)
> - [@Valid vs @Validated — Baeldung](https://www.baeldung.com/spring-valid-vs-validated)
> - [Custom Validator — Baeldung](https://www.baeldung.com/spring-mvc-custom-validator)
> - [Service Layer Validation — Baeldung](https://www.baeldung.com/spring-service-layer-validation)

### Ferramentas do ecossistema

**MapStruct** — mapeamento entre objetos (Entity ↔ DTO) em compile-time. Sem reflection, mais rápido que ModelMapper.

```java
@Mapper(componentModel = "spring")
public interface PatientMapper {
    PatientDTO toDto(Patient entity);
    Patient toEntity(CreatePatientRequest request);
}
```

**Lombok** — elimina boilerplate (getters, setters, constructors). **Cuidado com JPA:** `@Data` gera equals/hashCode com todos os campos, causando `LazyInitializationException` e loops infinitos com relações. Use `@Getter @Setter @NoArgsConstructor` separados e implemente equals/hashCode manualmente (ou use Records).

**SpringDoc OpenAPI** — gera OpenAPI 3 + Swagger UI automaticamente a partir dos controllers.

```java
// build.gradle
implementation 'org.springdoc:springdoc-openapi-starter-webmvc-ui:2.3.0'
// Acesse /swagger-ui.html
```

**Flyway** / **Liquibase** — versionamento de schema de banco. Flyway é mais simples (SQL puro), Liquibase mais poderoso (XML/YAML/JSON/SQL, rollback).

```text
resources/db/migration/
  V1__create_patients.sql
  V2__add_email_column.sql
  V3__create_appointments.sql
```

→ Deep dive em migrations seguras: seção Troubleshooting mais abaixo.

### Testing em Spring Boot

```java
@SpringBootTest
@Testcontainers
class AppointmentServiceIntegrationTest {

    @Container
    static PostgreSQLContainer<?> postgres = new PostgreSQLContainer<>("postgres:16");

    @Autowired
    private AppointmentService service;

    @Test
    void shouldCreateAppointment() {
        var result = service.create(new AppointmentRequest(...));
        assertThat(result.getId()).isNotNull();
    }
}
```

- **`@SpringBootTest`:** carrega o contexto completo
- **`@WebMvcTest`:** só controller layer (com MockMvc)
- **`@DataJpaTest`:** só repository layer
- **Testcontainers:** bancos reais em Docker

## Troubleshooting em produção

Problemas recorrentes em aplicações Spring Boot — o tipo de pergunta que aparece em entrevistas como "you've seen this in production, how did you debug it?"

### Connection pool exausto (HikariCP)

**Sintoma:** requests travam, logs mostram `HikariPool - Connection is not available, request timed out after 30000ms`.

**Causas comuns:**
- Pool pequeno demais para a carga
- Queries lentas segurando conexões
- Transação não fechada (leak)
- `@Transactional` em método que faz chamada HTTP externa (segura conexão enquanto espera response)

**Diagnóstico:**

```java
// application.yml — habilitar métricas do HikariCP
spring:
  datasource:
    hikari:
      maximum-pool-size: 10        # default é 10
      minimum-idle: 5
      connection-timeout: 30000     # ms para esperar conexão do pool
      leak-detection-threshold: 60000  # alerta se conexão não devolvida em 60s
      metrics-tracker-factory: io.micrometer.core.instrument.binder.db.HikariCPMetricsTrackerFactory
```

**Métricas para monitorar (Micrometer/Prometheus):**
- `hikaricp_connections_active` — quantas em uso
- `hikaricp_connections_pending` — quantas esperando (se > 0 por muito tempo, pool exausto)
- `hikaricp_connections_timeout_total` — timeouts acumulados

**Soluções:**
1. Habilitar `leak-detection-threshold` para encontrar onde a conexão está vazando
2. Não fazer I/O externo dentro de `@Transactional` — separar a chamada HTTP da transação
3. Ajustar pool size: `connections = (cores * 2) + 1` como baseline (HikariCP wiki)
4. Revisar queries lentas com `EXPLAIN ANALYZE`

### N+1 queries (JPA/Hibernate)

**Sintoma:** endpoint que deveria fazer 1-2 queries faz 50+. Latência degrada proporcionalmente ao número de registros.

**Como detectar:**

```java
// application.yml — ver queries no log
spring:
  jpa:
    show-sql: true
    properties:
      hibernate:
        format_sql: true
        generate_statistics: true  # mostra count de queries por sessão

// Ou usar Hibernate Statistics programaticamente
logging:
  level:
    org.hibernate.stat: DEBUG
```

**Cenário típico:**

```java
// RUIM — gera N+1 queries
List<Doctor> doctors = doctorRepo.findAll();  // 1 query
doctors.forEach(d -> d.getAppointments().size());  // N queries (1 por doctor)
```

**Soluções:**

```java
// 1. JOIN FETCH (JPQL)
@Query("SELECT d FROM Doctor d JOIN FETCH d.appointments WHERE d.active = true")
List<Doctor> findActiveWithAppointments();

// 2. @EntityGraph (declarativo)
@EntityGraph(attributePaths = {"appointments", "specialty"})
List<Doctor> findByActiveTrue();

// 3. @BatchSize (lazy loading em lotes, menos queries)
@Entity
public class Doctor {
    @OneToMany(mappedBy = "doctor")
    @BatchSize(size = 20)  // carrega 20 relações por vez, não 1
    private List<Appointment> appointments;
}

// 4. DTO Projection (melhor performance — sem entidade managed)
@Query("SELECT new com.app.dto.DoctorSummary(d.name, COUNT(a)) " +
       "FROM Doctor d LEFT JOIN d.appointments a GROUP BY d.name")
List<DoctorSummary> findDoctorSummaries();
```

**Regra:** sempre verificar o Hibernate statistics ou query log antes de ir para produção. N+1 em 10 registros no dev pode significar 10.000 queries em produção.

### LazyInitializationException

**Sintoma:** `org.hibernate.LazyInitializationException: could not initialize proxy - no Session`

**Causa:** acessar uma relação `@*ToMany` (lazy por default) fora do escopo de uma transação/sessão Hibernate.

```java
// RUIM — sessão já fechou quando o controller tenta serializar
@GetMapping("/doctors/{id}")
public Doctor getDoctor(@PathVariable Long id) {
    Doctor doctor = doctorRepo.findById(id).orElseThrow();
    // se Doctor tem List<Appointment> lazy, Jackson tenta serializar → BOOM
    return doctor;
}
```

**Soluções (em ordem de preferência):**

1. **DTO Projection** — retorna exatamente o que precisa, sem entidade lazy

```java
@GetMapping("/doctors/{id}")
public DoctorResponse getDoctor(@PathVariable Long id) {
    return doctorService.findById(id);  // retorna DTO, não entidade
}
```

2. **`@EntityGraph`** — carrega eager para essa query específica

```java
@EntityGraph(attributePaths = "appointments")
Optional<Doctor> findById(Long id);
```

3. **`JOIN FETCH`** — na JPQL

**Anti-pattern a evitar:** `spring.jpa.open-in-view=true` (OSIV) — mantém sessão aberta no controller. "Resolve" o erro mas causa problemas piores: connection pool exausto, queries inesperadas no view layer. **Desabilite em produção.**

```yaml
spring:
  jpa:
    open-in-view: false  # SEMPRE false em produção
```

### @Transactional: problemas sutis

**Problema 1 — `@Transactional` em método privado:**

```java
@Service
public class PaymentService {
    @Transactional  // NÃO FUNCIONA — Spring usa proxy, só intercepta public
    private void processPayment(Payment p) { ... }
}
```

Spring Boot usa proxies (CGLIB por default). O proxy só intercepta chamadas externas ao bean. Método privado ou chamada interna (self-invocation) bypassa o proxy.

**Problema 2 — self-invocation:**

```java
@Service
public class OrderService {
    public void createOrder(OrderRequest req) {
        // ... lógica
        sendConfirmation(req);  // chamada interna → @Transactional IGNORADO
    }

    @Transactional
    public void sendConfirmation(OrderRequest req) { ... }
}
```

**Solução:** extrair para outro bean, ou usar `ApplicationEventPublisher`:

```java
@Service
public class OrderService {
    private final ApplicationEventPublisher events;

    public void createOrder(OrderRequest req) {
        // ... lógica
        events.publishEvent(new OrderCreatedEvent(req));
    }
}

@Component
@TransactionalEventListener
public class OrderEventHandler {
    @Transactional
    public void onOrderCreated(OrderCreatedEvent event) { ... }
}
```

**Problema 3 — exceção checked não faz rollback:**

```java
@Transactional  // por default, só faz rollback em unchecked (RuntimeException)
public void transfer(Account from, Account to, BigDecimal amount) throws InsufficientFundsException {
    // InsufficientFundsException é checked → NÃO faz rollback!
}

// Solução: declarar explicitamente
@Transactional(rollbackFor = InsufficientFundsException.class)
```

### Memory leak e GC tuning

**Diagnóstico:**

```bash
# Heap dump quando OOM
java -XX:+HeapDumpOnOutOfMemoryError -XX:HeapDumpPath=/tmp/heapdump.hprof -jar app.jar

# Analisar com Eclipse MAT ou VisualVM
# Buscar: objetos que crescem sem parar, collections gigantes, caches sem limite
```

**Causas comuns em Spring Boot:**
- Cache sem eviction (ex.: `@Cacheable` sem TTL → memória cresce infinitamente)
- `static` collections que acumulam dados
- Event listeners que acumulam referências
- ThreadLocal não limpo (especialmente em servidores com thread pool)

**GC tuning básico:**

```bash
# G1GC (default Java 17+) — geralmente não precisa tuning
java -Xms512m -Xmx2g -XX:+UseG1GC -jar app.jar

# ZGC (Java 21+) — low-latency, pausas < 1ms
java -Xms512m -Xmx2g -XX:+UseZGC -jar app.jar

# Métricas: monitorar via Actuator/Micrometer
management.metrics.enable.jvm=true
```

### API timeout e cascading failures

**Problema:** serviço A chama serviço B que está lento → threads de A ficam presas → A também fica lento → cascata.

**Solução com Resilience4j:**

```java
// build.gradle
implementation 'io.github.resilience4j:resilience4j-spring-boot3'

// application.yml
resilience4j:
  circuitbreaker:
    instances:
      notificationService:
        sliding-window-size: 10
        failure-rate-threshold: 50    # abre após 50% de falhas
        wait-duration-in-open-state: 30s
        permitted-number-of-calls-in-half-open-state: 3
  timelimiter:
    instances:
      notificationService:
        timeout-duration: 2s          # timeout de 2s
  retry:
    instances:
      notificationService:
        max-attempts: 3
        wait-duration: 500ms

// No service
@CircuitBreaker(name = "notificationService", fallbackMethod = "fallbackNotify")
@TimeLimiter(name = "notificationService")
@Retry(name = "notificationService")
public CompletableFuture<String> notify(NotificationRequest req) {
    return CompletableFuture.supplyAsync(() -> notificationClient.send(req));
}

public CompletableFuture<String> fallbackNotify(NotificationRequest req, Throwable t) {
    log.warn("Notification failed, queuing for retry: {}", t.getMessage());
    retryQueue.add(req);  // enfileirar para retry assíncrono
    return CompletableFuture.completedFuture("queued");
}
```

### Graceful shutdown

**Problema:** deploy mata o processo enquanto requests estão em andamento → erros 502 para o usuário.

```yaml
# application.yml
server:
  shutdown: graceful  # espera requests em andamento terminarem

spring:
  lifecycle:
    timeout-per-shutdown-phase: 30s  # tempo máximo de espera
```

```java
// Para limpeza customizada
@Component
public class CleanupHandler {
    @PreDestroy
    public void cleanup() {
        // fechar conexões, flush de buffers, etc.
        log.info("Shutting down gracefully...");
    }
}
```

### Database migrations seguras (Flyway)

**Problema:** `ALTER TABLE ADD COLUMN NOT NULL` em tabela grande trava o banco (lock de escrita).

**Migração segura em produção (expand-and-contract):**

```sql
-- V10__add_email_safe.sql
-- Step 1: adiciona coluna nullable (sem lock)
ALTER TABLE patients ADD COLUMN email VARCHAR(255);

-- V11__backfill_email.sql
-- Step 2: popula em batches (sem lock longo)
UPDATE patients SET email = 'unknown@legacy.com' WHERE email IS NULL;

-- V12__make_email_not_null.sql
-- Step 3: após deploy que já escreve email, adiciona constraint
ALTER TABLE patients ALTER COLUMN email SET NOT NULL;
```

**Regras:**
- Nunca `DROP COLUMN` na mesma release que remove o código que usa. Primeiro deploy sem o código, depois migra.
- Nunca rename de coluna em uma step — cria nova, copia, valida, depois remove antiga.
- Sempre testar migração no staging com volume real de dados.

### Distributed tracing

**Problema:** request passa por 5 microserviços, está lenta. Qual serviço é o gargalo?

```java
// build.gradle — Spring Boot 3 com Micrometer Tracing
implementation 'io.micrometer:micrometer-tracing-bridge-otel'
implementation 'io.opentelemetry:opentelemetry-exporter-otlp'

// application.yml
management:
  tracing:
    sampling:
      probability: 1.0  # 100% em dev, 10% em prod
  otlp:
    tracing:
      endpoint: http://jaeger:4318/v1/traces
```

Cada request recebe um `traceId` propagado automaticamente entre serviços via headers HTTP. Visualiza no Jaeger/Zipkin o waterfall de cada serviço e identifica o bottleneck.

## Quando usar

- **Spring Boot:** default para aplicações Java. Microserviços, APIs REST, batch processing.
- **Spring WebFlux:** quando precisa de non-blocking I/O (reactive). Útil para gateways, streaming.
- **Spring Cloud:** microserviços distribuídos (service discovery, circuit breaker, config server).
- **Spring Batch:** processamento em lote de grandes volumes.

## Armadilhas comuns

- **LazyInitializationException:** acessar relação lazy fora de transação. Resolver com `@EntityGraph`, `JOIN FETCH`, ou DTO projection.
- **N+1 queries:** ocorre quando 1 query busca N entidades e depois N queries buscam relações de cada uma (total: N+1). Detectar via query logs repetidos ou Hibernate statistics. Soluções: `JOIN FETCH` na JPQL, `@EntityGraph` na interface do repository, `@BatchSize` para lazy loading em lotes, ou DTO projection que já traz os dados necessários em 1 query.
- **`@Transactional` em private methods:** não funciona! O Spring usa proxies, que só interceptam métodos públicos.
- **Circular dependencies:** A depende de B que depende de A. Reestruturar com eventos ou extrair interface.
- **Beans mutáveis singleton:** estado compartilhado em beans singleton causa race conditions.

## Na prática

> [!exemplo] Stack típico de um serviço Spring Boot
> Um backend Spring Boot 3 sobre Java 17+ costuma combinar Spring Data JPA (persistência), Spring Security (autenticação/JWT) e Actuator + Micrometer (métricas), com testes de integração via Testcontainers. Cada uma dessas peças tem (ou terá) galho próprio na trilha — veja [[03-Dominios/Java/Spring Core e Boot/index|Spring Core e Boot]] para o núcleo.

## How to explain in English

"Spring Boot is my go-to framework for Java backend development. I use it because of the mature ecosystem — Spring Data for database access, Spring Security for authentication, and Actuator for production-ready monitoring, all with minimal configuration.

My typical project structure follows a layered architecture: controllers handle HTTP mapping and validation, services contain business logic, and repositories manage data access through Spring Data JPA. I prefer constructor injection over field injection because it makes dependencies explicit and simplifies testing.

For testing, I use a combination of `@WebMvcTest` for controller unit tests, `@DataJpaTest` for repository tests, and `@SpringBootTest` with Testcontainers for full integration tests. Testcontainers is a game-changer — it spins up real PostgreSQL and Redis instances in Docker during tests, so I have high confidence that the code works correctly in production.

One area where I've seen teams struggle is with JPA's lazy loading. The LazyInitializationException is a common pitfall when accessing relationships outside of a transaction boundary. I address this by using DTO projections or `@EntityGraph` annotations, which keeps queries predictable and avoids the N+1 problem."

### Key vocabulary

- injeção de dependência → dependency injection (DI)
- contêiner IoC → IoC container: gerencia beans e suas dependências
- autoconfiguração → autoconfiguration
- perfil → profile: configuração por ambiente
- anotação → annotation: metadata no código (`@Service`, `@Repository`)
- transação → transaction: unidade atômica de trabalho no banco
- filtro de segurança → security filter chain
- inicialização tardia → lazy initialization / lazy loading

## Recursos

- [Spring Boot Reference](https://docs.spring.io/spring-boot/reference/) — documentação oficial
- [Spring Framework](https://spring.io/projects/spring-framework)
- [Spring Initializr](https://start.spring.io/) — gerador de projetos
- [Spring MVC — Web on Servlet Stack](https://docs.spring.io/spring-framework/reference/web.html)
- [Spring Security](https://spring.io/projects/spring-security)
- [Spring Testing](https://docs.spring.io/spring-framework/reference/testing.html)
- [Baeldung — Start Here](https://www.baeldung.com/start-here) — tutorials Spring Boot
- [Stop using @Autowired](https://www.linkedin.com/pulse/you-should-stop-using-spring-autowired-felix-coutinho/) — constructor injection
- [ProblemDetails para tratamento de erros](https://medium.com/@claudionetto/usando-problemdetails-para-facilitar-e-melhorar-o-retorno-de-exce%C3%A7%C3%B5es-5c060a42f637)
- [Spring @Value — Baeldung](https://www.baeldung.com/spring-value-annotation)

## Veja também

- [[03-Dominios/Java/Spring Core e Boot/index|Spring Core e Boot (Galho 8)]]
- [[03-Dominios/Java/Web e APIs REST/index|Web e APIs REST (Galho 9)]] — Spring MVC, REST controllers, Problem Details, OpenAPI, clientes HTTP
- [[Java Fundamentals]] — a linguagem
- [[Java Concurrency]] — concorrência, Virtual Threads, ThreadPools
- [[03-Dominios/Java/Persistência de dados/index|Persistência de dados (Galho 10)]] — JPA/Hibernate, fetch/N+1, transações, locking, caching, migrations
- [[03-Dominios/Java/Programação Reativa/index|Programação Reativa (Galho 11)]] — Reactor, WebFlux, backpressure, R2DBC, reativo vs Virtual Threads
- [[Spring Security]] — deep dive em autenticação e autorização
- [[Testes em Java]] — JUnit 5, Mockito, Testcontainers, slices
- [[Testes]] — fundamentos gerais
- [[API Design]] — REST, RFC 9457 Problem Details
- [[03-Dominios/Java/Backend/Kafka/Kafka]] — event streaming com Spring Kafka
- [[System Design]] — troubleshooting cross-stack, building blocks
- [[Arquitetura de Software]] — Hexagonal, DDD, Clean Architecture
