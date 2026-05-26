---
title: "Spring Boot"
created: 2026-04-01
updated: 2026-04-11
type: concept
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

O coração do Spring. Entender o IoC container é entender Spring.

### BeanFactory vs ApplicationContext

**`BeanFactory`** — interface básica, lazy init, usada raramente diretamente.

**`ApplicationContext`** — estende BeanFactory com features enterprise: event publication, internationalization, environment abstraction, resource loading. **O que você usa na prática.**

Em Spring Boot, o `ApplicationContext` concreto é:

- **`AnnotationConfigApplicationContext`** — para apps standalone
- **`AnnotationConfigServletWebServerApplicationContext`** — para web apps servlet-based (Spring MVC)
- **`AnnotationConfigReactiveWebServerApplicationContext`** — para apps reactive (Spring WebFlux)

Você raramente interage com o ApplicationContext diretamente, mas pode injetá-lo:

```java
@Service
public class MeuServico {
    private final ApplicationContext context;

    public MeuServico(ApplicationContext context) {
        this.context = context;
    }

    public void exemplo() {
        String[] names = context.getBeanDefinitionNames();
        MeuBean b = context.getBean(MeuBean.class);
    }
}
```

### Inversão de Controle (IoC) e Dependency Injection (DI)

**Inversão de Controle** é o princípio: o framework controla a criação e wiring de objetos, não o seu código.

**Dependency Injection** é uma forma de implementar IoC: o framework **injeta** dependências no objeto, em vez do objeto criá-las.

**Antes (sem DI):**

```java
public class AppointmentService {
    private PatientRepository repo = new JdbcPatientRepository();  // acoplado!
}
```

**Com DI:**

```java
@Service
public class AppointmentService {
    private final PatientRepository repo;

    public AppointmentService(PatientRepository repo) {
        this.repo = repo;  // Spring injeta qualquer implementação
    }
}
```

### Tipos de injeção

**Constructor injection (recomendado):**

```java
@Service
public class AppointmentService {
    private final PatientRepository repo;
    private final NotificationSender notifier;

    public AppointmentService(PatientRepository repo, NotificationSender notifier) {
        this.repo = repo;
        this.notifier = notifier;
    }
}
```

**Vantagens:**

- Dependências explícitas e imutáveis (`final`)
- Fácil de testar (new MeuServico(mockRepo, mockNotifier))
- Falha na inicialização se dependência faltar (fail-fast)
- Previne dependências circulares silenciosas

**Setter injection:** usado raramente, útil para dependências opcionais.

```java
@Autowired
public void setCache(Optional<Cache> cache) {
    this.cache = cache.orElse(null);
}
```

**Field injection (`@Autowired` em campo):** **evite.**

```java
// RUIM
@Autowired
private PatientRepository repo;
```

Problemas:

- Difícil testar (precisa de reflection ou Spring test context)
- Esconde dependências
- Não permite `final`
- Permite dependências circulares silenciosas

**Spring Boot 2.6+:** dependências circulares são **proibidas** por default. Você precisa `spring.main.allow-circular-references=true` — o que é um sinal claro de design ruim.

### Bean lifecycle

```
1. Instantiation           (new SeuBean())
2. Populate properties     (@Autowired, setters)
3. BeanNameAware.setBeanName
4. BeanFactoryAware.setBeanFactory
5. ApplicationContextAware.setApplicationContext
6. BeanPostProcessor.postProcessBeforeInitialization
7. @PostConstruct / InitializingBean.afterPropertiesSet / init-method
8. BeanPostProcessor.postProcessAfterInitialization   ← aqui é onde proxies são criados (AOP)
9. Bean pronto para uso
   ...
10. @PreDestroy / DisposableBean.destroy / destroy-method (em shutdown)
```

**Hooks úteis:**

```java
@Service
public class MeuServico {

    @PostConstruct
    public void inicializar() {
        // executado após DI completar
    }

    @PreDestroy
    public void cleanup() {
        // executado no shutdown graceful
    }
}
```

### Bean scopes

| Scope | Descrição | Uso |
| --- | --- | --- |
| **`singleton`** (default) | Uma instância por ApplicationContext | 99% dos casos |
| **`prototype`** | Nova instância a cada `getBean()` ou injeção | Beans stateful raros |
| **`request`** | Uma por HTTP request | Web apps, state por request |
| **`session`** | Uma por HTTP session | Web apps, state por usuário |
| **`application`** | Uma por ServletContext | Web apps globais |
| **`websocket`** | Uma por WebSocket | Apps WebSocket |

**Cuidado:** injetar **prototype** em **singleton** não funciona ingenuamente — o singleton recebe uma única instância do prototype. Soluções:

- `@Lookup` method injection
- `ObjectProvider<T>` ou `Provider<T>`
- `@Scope(value = "prototype", proxyMode = ScopedProxyMode.TARGET_CLASS)` no prototype

```java
@Service
public class SingletonServico {

    @Autowired
    private ObjectProvider<ProtoypeBean> proto;

    public void usar() {
        ProtoypeBean novo = proto.getObject();  // nova instância a cada chamada
    }
}
```

### BeanPostProcessor — o poder oculto

`BeanPostProcessor` é o hook que permite ao Spring **modificar** ou **envolver** beans após a criação. É como AOP, `@Async`, `@Transactional`, `@EventListener` funcionam: todos têm BeanPostProcessors que envolvem seus beans em proxies.

```java
@Component
public class MeuBPP implements BeanPostProcessor {

    @Override
    public Object postProcessAfterInitialization(Object bean, String beanName) {
        if (bean instanceof MeuTipo) {
            // Pode retornar proxy, wrapper, ou o próprio bean
            return Proxy.newProxyInstance(...);
        }
        return bean;
    }
}
```

Raramente você precisa escrever um. Mas entender que existem explica muita "mágica" do Spring.

### @Component vs @Service vs @Repository vs @Controller

Tecnicamente, **os 4 fazem a mesma coisa**: registram a classe como bean. A diferença é semântica + alguns comportamentos específicos:

- **`@Component`** — genérico, qualquer bean gerenciado
- **`@Service`** — camada de lógica de negócio (sem comportamento extra)
- **`@Repository`** — camada de persistência. **Adiciona tradução de exceções** de persistência para `DataAccessException`
- **`@Controller`** / **`@RestController`** — handler de HTTP requests. Spring MVC usa para mapping

**Regra prática:** use a anotação semântica (`@Service`, `@Repository`, `@Controller`). Isso documenta intenção e permite scanning específico.

### Configuração com @Configuration e @Bean

Além de component scanning, você pode declarar beans explicitamente:

```java
@Configuration
public class MinhaConfig {

    @Bean
    public RestTemplate restTemplate() {
        return new RestTemplate();
    }

    @Bean
    public ObjectMapper objectMapper() {
        return new ObjectMapper()
            .registerModule(new JavaTimeModule())
            .disable(SerializationFeature.WRITE_DATES_AS_TIMESTAMPS);
    }

    @Bean
    @ConditionalOnMissingBean  // só cria se não existe outro
    public MeuCache cache() {
        return new InMemoryCache();
    }
}
```

**Uso típico:** beans de bibliotecas externas (que você não pode anotar), beans complexos que exigem lógica de construção, overrides condicionais.

### Conditional beans

```java
@Configuration
public class CacheConfig {

    @Bean
    @ConditionalOnProperty(name = "cache.type", havingValue = "redis")
    public CacheManager redisCache() { ... }

    @Bean
    @ConditionalOnProperty(name = "cache.type", havingValue = "caffeine", matchIfMissing = true)
    public CacheManager caffeineCache() { ... }

    @Bean
    @ConditionalOnClass(name = "com.hazelcast.core.HazelcastInstance")
    public CacheManager hazelcastCache() { ... }

    @Bean
    @ConditionalOnMissingBean(CacheManager.class)
    public CacheManager fallbackCache() { ... }
}
```

Isso é exatamente como a **autoconfiguração** do Spring Boot funciona internamente.

---

## AOP e proxies — a mágica por baixo

**Aspect-Oriented Programming (AOP)** permite modularizar cross-cutting concerns (logging, transações, segurança, cache) separados da lógica de negócio.

Anotações como `@Transactional`, `@Async`, `@Cacheable`, `@PreAuthorize` são **implementadas via AOP**. Entender isso explica várias armadilhas.

### Como funciona: proxies

Spring cria um **proxy** ao redor do bean. Quando você chama um método anotado, a chamada passa pelo proxy, que executa o "advice" (código do aspecto) antes/depois do método real.

```
Client code
    ↓
  Proxy (Spring-generated)       ← intercepta a chamada
    ↓ (advice antes, ex.: begin transaction)
    ↓
  Real Bean                      ← método real
    ↓
  Proxy                          ← advice depois, ex.: commit / rollback
    ↓
Client code
```

### JDK Dynamic Proxy vs CGLIB

Spring usa dois tipos de proxy:

**JDK Dynamic Proxy** — proxy baseado em interface. Só funciona se o bean implementa interface.

```java
public interface PatientService { void save(Patient p); }

@Service
public class PatientServiceImpl implements PatientService {
    @Transactional
    public void save(Patient p) { ... }
}
// Spring cria JDK proxy que implementa PatientService
```

**CGLIB Proxy** — cria subclasse em runtime via bytecode manipulation. Funciona mesmo sem interface.

```java
@Service
public class PatientService {  // sem interface
    @Transactional
    public void save(Patient p) { ... }
}
// Spring cria CGLIB proxy que estende PatientService
```

**Default em Spring Boot 2.x+:** CGLIB (`spring.aop.proxy-target-class=true`). Antes era JDK.

**Limitações CGLIB:**

- Classes `final` não podem ser proxadas (CGLIB precisa estender)
- Métodos `final` não são interceptados (não pode sobrescrever)
- Métodos `private` não são interceptados (não são visíveis para subclass)
- Construtor é chamado 2x (uma para superclass, uma para subclass proxy)

### Self-invocation: a armadilha clássica

A chamada interna **não passa pelo proxy** — bypassa o AOP.

```java
@Service
public class OrderService {

    public void createOrder(OrderRequest req) {
        validateOrder(req);
        sendConfirmation(req);  // ← chamada interna, NÃO passa pelo proxy
    }

    @Transactional
    public void sendConfirmation(OrderRequest req) {
        // @Transactional IGNORADO quando chamado internamente!
    }
}
```

**Por quê:** `this.sendConfirmation(req)` é uma chamada direta ao objeto, não ao proxy. O proxy só intercepta chamadas externas.

**Soluções:**

1. **Extrair para outro bean** (mais limpa):

```java
@Service
@RequiredArgsConstructor
public class OrderService {
    private final ConfirmationService confirmationService;

    public void createOrder(OrderRequest req) {
        validateOrder(req);
        confirmationService.sendConfirmation(req);  // passa pelo proxy
    }
}
```

2. **Self-injection** (funciona, mas feio):

```java
@Service
public class OrderService {

    @Autowired
    private OrderService self;  // auto-injeta via proxy

    public void createOrder(OrderRequest req) {
        self.sendConfirmation(req);  // passa pelo proxy
    }
}
```

3. **`@Transactional` no método público** — se o método público é o único ponto de entrada, anote ele:

```java
@Transactional
public void createOrder(OrderRequest req) {
    validateOrder(req);
    sendConfirmation(req);
}
```

### @Transactional em métodos private ou final

- **`private`** — proxy CGLIB não intercepta. `@Transactional` é **ignorado sem warning**.
- **`final`** — CGLIB não pode sobrescrever. `@Transactional` é ignorado.

**Regra:** para anotações AOP funcionarem, o método deve ser `public` e não-`final`.

### Advice types

Tipos de advice que você pode declarar (raro escrever à mão, mas útil conhecer):

- **`@Before`** — antes do método
- **`@After`** — depois (sempre)
- **`@AfterReturning`** — após sucesso
- **`@AfterThrowing`** — após exceção
- **`@Around`** — envolve a chamada (mais poderoso, pode decidir se executa)

**Exemplo de aspect customizado — logging:**

```java
@Aspect
@Component
@Slf4j
public class LoggingAspect {

    @Around("@annotation(loggable)")
    public Object logExecution(ProceedingJoinPoint pjp, Loggable loggable) throws Throwable {
        long start = System.currentTimeMillis();
        String method = pjp.getSignature().toShortString();

        log.info("Entering {}", method);
        try {
            Object result = pjp.proceed();
            log.info("{} completed in {}ms", method, System.currentTimeMillis() - start);
            return result;
        } catch (Exception e) {
            log.error("{} failed: {}", method, e.getMessage());
            throw e;
        }
    }
}

@Target(ElementType.METHOD)
@Retention(RetentionPolicy.RUNTIME)
public @interface Loggable {}

// Uso
@Service
public class MeuServico {
    @Loggable
    public void processar() { ... }
}
```

### Pointcut expressions

Linguagem para selecionar onde o advice se aplica.

```java
// Todos os métodos de uma classe
@Pointcut("execution(* com.app.service.PatientService.*(..))")

// Todos os métodos de um package
@Pointcut("execution(* com.app.service..*.*(..))")

// Métodos anotados com @Transactional
@Pointcut("@annotation(org.springframework.transaction.annotation.Transactional)")

// Classes anotadas com @Service
@Pointcut("within(@org.springframework.stereotype.Service *)")

// Combinando com AND/OR/NOT
@Pointcut("execution(* com.app..*.*(..)) && @annotation(Loggable)")
```

---

## Gerenciamento de transações — @Transactional deep dive

Uma das features mais usadas e mal compreendidas do Spring.

### O básico

```java
@Service
public class TransferenciaService {

    @Transactional
    public void transferir(Account origem, Account destino, Money valor) {
        origem.debitar(valor);
        contaRepo.save(origem);
        destino.creditar(valor);
        contaRepo.save(destino);
        // Se qualquer operação lançar RuntimeException, tudo faz rollback
    }
}
```

Por baixo: Spring cria proxy → ao entrar no método, chama `PlatformTransactionManager.getTransaction()` → commit ou rollback ao sair.

### Propagation

Como transações se comportam quando uma chama outra.

| Propagation | Comportamento |
| --- | --- |
| **`REQUIRED`** (default) | Usa tx existente ou cria nova |
| **`REQUIRES_NEW`** | Suspende tx atual e cria nova (independente) |
| **`SUPPORTS`** | Usa tx se existir, caso contrário sem tx |
| **`NOT_SUPPORTED`** | Suspende tx atual, executa sem tx |
| **`MANDATORY`** | Exige tx existente, lança se não houver |
| **`NEVER`** | Lança se houver tx em andamento |
| **`NESTED`** | Savepoint dentro da tx atual (se suportado) |

**Uso prático de `REQUIRES_NEW`:** auditoria que deve commitar mesmo se a tx principal falhar.

```java
@Service
public class AuditoriaService {

    @Transactional(propagation = Propagation.REQUIRES_NEW)
    public void registrar(Evento e) {
        auditoriaRepo.save(e);
        // Mesmo se a tx externa rollback, esta aqui commita
    }
}
```

### Isolation levels

Controla visibilidade entre transações concorrentes. Ver [[Banco de dados]] para teoria completa.

| Isolation | Dirty read | Non-repeatable read | Phantom read |
| --- | --- | --- | --- |
| `READ_UNCOMMITTED` | ✓ possível | ✓ possível | ✓ possível |
| `READ_COMMITTED` (default PostgreSQL) | ✗ | ✓ possível | ✓ possível |
| `REPEATABLE_READ` (default MySQL) | ✗ | ✗ | ✓ possível |
| `SERIALIZABLE` | ✗ | ✗ | ✗ |

```java
@Transactional(isolation = Isolation.SERIALIZABLE)
public void operacaoCritica() { ... }
```

**Na prática:** `READ_COMMITTED` resolve a maioria dos casos. `SERIALIZABLE` tem custo de performance.

### Rollback rules

**Regra default:** rollback **apenas** em `RuntimeException` (unchecked) e `Error`. Checked exceptions **não fazem rollback**.

```java
@Transactional
public void transferir(...) throws InsufficientFundsException {
    // Se InsufficientFundsException (checked) for lançada, a tx COMMITA!
}

// Correção
@Transactional(rollbackFor = InsufficientFundsException.class)
public void transferir(...) throws InsufficientFundsException { ... }

// Ou rollback para qualquer exceção
@Transactional(rollbackFor = Exception.class)
public void transferir(...) throws Exception { ... }
```

**Rollback manual:**

```java
@Transactional
public void minhaOperacao() {
    try {
        repo.save(entidade);
    } catch (Exception e) {
        TransactionAspectSupport.currentTransactionStatus().setRollbackOnly();
        throw e;
    }
}
```

### Read-only

Otimização — o Spring e o banco podem pular overhead se souber que é só leitura.

```java
@Transactional(readOnly = true)
public Page<Patient> listarPacientes(Pageable pageable) {
    return repo.findAll(pageable);
}
```

**Hibernate benefit:** desabilita dirty checking automático (não verifica mudanças no final).

### Timeout

```java
@Transactional(timeout = 30)  // segundos
public void operacaoLenta() { ... }
```

Lança `TransactionTimedOutException` se passar.

### Padrão arquitetural: transações na camada Service

**Regra:** `@Transactional` na **camada Service**, não no Controller nem no Repository.

**Razões:**

- Service define as **fronteiras do caso de uso**
- Controller não deve saber de persistência
- Repository é muito granular (cada call vira uma tx, ineficiente)

```java
// BOM
@Service
public class OrderService {
    @Transactional
    public Order createOrder(OrderRequest req) {
        // valida, salva, dispara eventos — tudo em uma tx
    }
}

// RUIM — @Transactional no Repository
public interface OrderRepository extends JpaRepository<Order, Long> {
    // cada save é uma tx separada
}
```

→ Para deep dive em JPA, transações, N+1: ver [[Spring Data JPA]]

---

## Spring MVC pipeline

Entender como um HTTP request vira uma resposta é essencial.

### O pipeline

```
HTTP Request
    ↓
Tomcat (servlet container)
    ↓
Filter chain (FilterRegistrationBean)
    ↓  CharacterEncodingFilter, security filters, etc.
    ↓
DispatcherServlet (o "front controller" do Spring MVC)
    ↓
HandlerMapping (resolve request → controller method)
    ↓
HandlerInterceptor.preHandle
    ↓
HandlerAdapter
    ↓  invoca o método do Controller
    ↓
@Controller method (ou @RestController)
    ↓  executa lógica, retorna ModelAndView ou @ResponseBody
    ↓
HandlerInterceptor.postHandle
    ↓
HttpMessageConverter (serializa @ResponseBody → JSON via Jackson)
    ↓
HandlerInterceptor.afterCompletion
    ↓
Filter chain (saída)
    ↓
HTTP Response
```

### DispatcherServlet

O "Front Controller" — recebe todos os requests e delega. Registrado automaticamente pelo Spring Boot em `/` (ou `server.servlet.context-path`).

### HandlerMapping

Resolve "qual controller trata este request". O principal é `RequestMappingHandlerMapping` que lê anotações `@RequestMapping`, `@GetMapping`, `@PostMapping`, etc.

### HandlerAdapter

Executa o handler. Traduz argumentos do método (via `HandlerMethodArgumentResolver`): `@RequestBody`, `@PathVariable`, `@RequestParam`, `@RequestHeader`, `HttpServletRequest`, etc.

### HttpMessageConverter

Converte body do request ↔ objetos Java. `MappingJackson2HttpMessageConverter` é o principal (JSON via Jackson). Você pode customizar:

```java
@Configuration
public class WebMvcConfig implements WebMvcConfigurer {

    @Override
    public void configureMessageConverters(List<HttpMessageConverter<?>> converters) {
        converters.add(customConverter());
    }

    @Bean
    public Jackson2ObjectMapperBuilderCustomizer jacksonCustomizer() {
        return builder -> builder
            .modulesToInstall(new JavaTimeModule())
            .failOnUnknownProperties(false);
    }
}
```

### Interceptors vs Filters

- **Filter** (javax/jakarta.servlet) — nível servlet. Executa **antes** do DispatcherServlet. Usado para auth cross-cutting, encoding, CORS.
- **Interceptor** (Spring MVC) — executa dentro do pipeline Spring MVC. Tem acesso ao handler method. Usado para logging de business-specific, validação.

```java
@Component
public class LoggingInterceptor implements HandlerInterceptor {

    @Override
    public boolean preHandle(HttpServletRequest req, HttpServletResponse resp, Object handler) {
        MDC.put("traceId", UUID.randomUUID().toString());
        return true;
    }

    @Override
    public void afterCompletion(HttpServletRequest req, HttpServletResponse resp, Object handler, Exception ex) {
        MDC.clear();
    }
}

@Configuration
public class WebConfig implements WebMvcConfigurer {

    @Autowired
    private LoggingInterceptor loggingInterceptor;

    @Override
    public void addInterceptors(InterceptorRegistry registry) {
        registry.addInterceptor(loggingInterceptor);
    }
}
```

### Exception Handling

**`@ExceptionHandler`** dentro do controller:

```java
@RestController
public class PatientController {

    @ExceptionHandler(PatientNotFoundException.class)
    public ResponseEntity<ProblemDetail> handle(PatientNotFoundException e) {
        var problem = ProblemDetail.forStatusAndDetail(HttpStatus.NOT_FOUND, e.getMessage());
        return ResponseEntity.of(problem).build();
    }
}
```

**`@RestControllerAdvice`** para handlers globais (padrão recomendado):

```java
@RestControllerAdvice
public class GlobalExceptionHandler {

    @ExceptionHandler(PatientNotFoundException.class)
    public ResponseEntity<ProblemDetail> handleNotFound(PatientNotFoundException e) {
        var problem = ProblemDetail.forStatusAndDetail(HttpStatus.NOT_FOUND, e.getMessage());
        problem.setType(URI.create("https://api.example.com/errors/not-found"));
        problem.setProperty("trace_id", MDC.get("traceId"));
        return ResponseEntity.status(HttpStatus.NOT_FOUND).body(problem);
    }

    @ExceptionHandler(MethodArgumentNotValidException.class)
    public ResponseEntity<ProblemDetail> handleValidation(MethodArgumentNotValidException e) {
        List<Map<String, String>> errors = e.getBindingResult().getFieldErrors().stream()
            .map(f -> Map.of("field", f.getField(), "code", f.getCode(), "message", f.getDefaultMessage()))
            .toList();

        var problem = ProblemDetail.forStatusAndDetail(HttpStatus.UNPROCESSABLE_ENTITY, "Validation failed");
        problem.setProperty("errors", errors);
        return ResponseEntity.unprocessableEntity().body(problem);
    }
}
```

→ Para RFC 9457 Problem Details completo, ver [[API Design]]

---

## Configuração e Profiles — deep dive

### Hierarquia de configuração

Spring Boot lê propriedades de múltiplas fontes, na ordem (maior precedência vence):

1. **Devtools global config**
2. **`@TestPropertySource`** em tests
3. **Command line arguments** (`--server.port=8080`)
4. **`SPRING_APPLICATION_JSON`** environment variable
5. **ServletConfig init parameters**
6. **ServletContext init parameters**
7. **JNDI attributes**
8. **Java System properties** (`-D`)
9. **OS environment variables**
10. **RandomValuePropertySource** (`random.*`)
11. **Profile-specific `application-{profile}.yml`**
12. **`application.yml`** (main)
13. **`@PropertySource`** in `@Configuration`
14. **Default properties**

**Regra prática:** defina defaults em `application.yml`, sobrescreva com `application-prod.yml`, e use **env variables** para secrets em produção.

### Profiles

Agrupa configurações por ambiente (dev, staging, prod).

```yaml
# application.yml — default
spring:
  application:
    name: medespecialista
  profiles:
    active: ${SPRING_PROFILES_ACTIVE:dev}

# application-dev.yml
spring:
  datasource:
    url: jdbc:postgresql://localhost:5432/meddev
logging:
  level:
    com.medespecialista: DEBUG

# application-prod.yml
spring:
  datasource:
    url: ${DATABASE_URL}
    hikari:
      maximum-pool-size: 20
logging:
  level:
    root: INFO
```

**Ativar profile:**

```bash
# Via env variable (preferido em produção)
SPRING_PROFILES_ACTIVE=prod java -jar app.jar

# Via argument
java -jar app.jar --spring.profiles.active=prod

# Via código
@SpringBootApplication
public class App {
    public static void main(String[] args) {
        SpringApplication app = new SpringApplication(App.class);
        app.setAdditionalProfiles("prod");
        app.run(args);
    }
}
```

**Profile-specific beans:**

```java
@Service
@Profile("dev")
public class MockEmailSender implements EmailSender { ... }

@Service
@Profile("!dev")  // qualquer profile exceto dev
public class RealEmailSender implements EmailSender { ... }

@Service
@Profile({"prod", "staging"})
public class CloudEmailSender implements EmailSender { ... }
```

### @ConfigurationProperties — binding tipado

Em vez de usar `@Value` espalhado, agrupe configuração em classes tipadas:

```java
@ConfigurationProperties(prefix = "app.notifications")
@Validated
public record NotificationProperties(
    @NotBlank String emailFrom,
    @NotNull Duration timeout,
    @NotNull @Valid SmsProperties sms,
    List<String> channels
) {
    public record SmsProperties(
        @NotBlank String provider,
        @NotBlank String apiKey,
        int maxRetries
    ) {}
}
```

```yaml
app:
  notifications:
    email-from: noreply@example.com
    timeout: PT30S
    sms:
      provider: twilio
      api-key: ${TWILIO_API_KEY}
      max-retries: 3
    channels:
      - email
      - push
      - sms
```

```java
@SpringBootApplication
@ConfigurationPropertiesScan
public class App { }

// Injetar
@Service
public class NotificationService {
    private final NotificationProperties props;

    public NotificationService(NotificationProperties props) {
        this.props = props;
    }
}
```

**Vantagens sobre `@Value`:**

- Validação Jakarta Bean Validation
- IDE support (autocomplete em YAML)
- Documentação automática via `spring-boot-configuration-processor`
- Refactoring seguro
- Agrupamento lógico

### @Value para casos pontuais

```java
@Value("${app.max-retries:3}")  // default 3
private int maxRetries;

@Value("#{systemProperties['user.timezone']}")  // SpEL
private String timezone;
```

---

## Actuator — production-ready features

`spring-boot-starter-actuator` expõe endpoints de monitoramento e gerenciamento.

### Endpoints principais

| Endpoint | O que expõe |
| --- | --- |
| `/actuator/health` | Status da aplicação (UP/DOWN/OUT_OF_SERVICE) |
| `/actuator/info` | Informações gerais (build, git) |
| `/actuator/metrics` | Métricas (Micrometer) |
| `/actuator/prometheus` | Métricas em formato Prometheus |
| `/actuator/env` | Propriedades de ambiente |
| `/actuator/configprops` | `@ConfigurationProperties` beans |
| `/actuator/beans` | Lista todos os beans do contexto |
| `/actuator/mappings` | Mapeamentos de endpoints |
| `/actuator/loggers` | Visualizar e **alterar** níveis de log em runtime |
| `/actuator/threaddump` | Thread dump |
| `/actuator/heapdump` | Heap dump |
| `/actuator/httpexchanges` | Últimos HTTP requests |
| `/actuator/scheduledtasks` | Tasks do `@Scheduled` |

### Configuração

```yaml
management:
  endpoints:
    web:
      exposure:
        include: health,info,metrics,prometheus,loggers
      base-path: /actuator
  endpoint:
    health:
      show-details: when-authorized
      probes:
        enabled: true
  metrics:
    export:
      prometheus:
        enabled: true
    distribution:
      percentiles-histogram:
        http.server.requests: true
      percentiles:
        http.server.requests: 0.5, 0.9, 0.95, 0.99
```

**Segurança:** por default, só `/health` é exposto. Em produção, **sempre** proteja Actuator com auth:

```java
http.securityMatcher(EndpointRequest.toAnyEndpoint())
    .authorizeHttpRequests(auth -> auth
        .requestMatchers(EndpointRequest.to("health", "info")).permitAll()
        .anyRequest().hasRole("ADMIN"));
```

### Custom Health Indicator

```java
@Component
public class ExternalApiHealthIndicator implements HealthIndicator {

    private final ExternalApiClient client;

    @Override
    public Health health() {
        try {
            var response = client.ping();
            return Health.up()
                .withDetail("latency", response.latencyMs())
                .withDetail("version", response.version())
                .build();
        } catch (Exception e) {
            return Health.down()
                .withDetail("error", e.getMessage())
                .build();
        }
    }
}
```

### Kubernetes probes

Spring Boot 2.3+ suporta liveness e readiness built-in:

```yaml
management:
  endpoint:
    health:
      probes:
        enabled: true
```

Expõe:

- `/actuator/health/liveness` — app está viva? (Kubernetes reinicia se DOWN)
- `/actuator/health/readiness` — app pronta para receber tráfego? (Kubernetes tira do load balancer)

```yaml
# Kubernetes manifest
livenessProbe:
  httpGet:
    path: /actuator/health/liveness
    port: 8080
  initialDelaySeconds: 30
  periodSeconds: 10

readinessProbe:
  httpGet:
    path: /actuator/health/readiness
    port: 8080
  initialDelaySeconds: 5
  periodSeconds: 5
```

### Micrometer — métricas

Micrometer é a abstração de métricas de Spring Boot. Suporta Prometheus, Datadog, New Relic, CloudWatch, e outros.

**Métricas built-in:**

- JVM (GC, memory, threads, classloader)
- HTTP (latency, count, errors) — `http.server.requests`
- DataSource (HikariCP pool)
- Tomcat / Jetty / Netty
- Logback (log rate)
- Cache (Caffeine, Ehcache)

**Métricas customizadas:**

```java
@Service
public class OrderService {

    private final Counter ordersCreated;
    private final Timer processingTime;

    public OrderService(MeterRegistry registry) {
        this.ordersCreated = registry.counter("orders.created");
        this.processingTime = registry.timer("orders.processing.time");
    }

    public Order create(OrderRequest req) {
        return processingTime.record(() -> {
            Order order = doCreate(req);
            ordersCreated.increment();
            return order;
        });
    }
}
```

**Com tags (labels Prometheus):**

```java
Counter errors = Counter.builder("api.errors")
    .tag("endpoint", "/patients")
    .tag("method", "POST")
    .register(registry);
```

---

## Spring WebFlux — visão geral

Alternativa reativa ao Spring MVC. Usa Project Reactor (Mono, Flux) em vez de servlet API.

**Quando usar:**

- Alta concorrência I/O-bound (antes de Virtual Threads)
- Streaming (SSE, WebSocket)
- Stack já reactive (Reactor Kafka, R2DBC)

**Quando NÃO usar:**

- CRUD tradicional — Spring MVC é mais simples
- Equipe sem experiência com reactive programming
- Java 21+ disponível — Virtual Threads tornam WebFlux menos necessário

```java
@RestController
public class ReactiveController {

    @GetMapping("/users/{id}")
    public Mono<User> getUser(@PathVariable String id) {
        return userRepository.findById(id);
    }

    @GetMapping("/users")
    public Flux<User> listUsers() {
        return userRepository.findAll();
    }
}
```

**Não cobrimos em profundidade aqui** — WebFlux merece sua própria nota se virar relevante.

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

## Na prática (da minha experiência)

> No MedEspecialista, o backend é Spring Boot 3 com Java 21. Uso Spring Data JPA com PostgreSQL, Spring Security com JWT para autenticação, e Actuator + Micrometer para métricas exportadas ao Grafana. O CI/CD com GitHub Actions roda testes com Testcontainers (PostgreSQL e Redis em Docker), garantindo que cada PR é validada contra bancos reais. O tempo de deploy caiu de 1 hora para 2 minutos após automatizar o pipeline.

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

- [[Java Fundamentals]] — a linguagem
- [[Java Concurrency]] — concorrência, Virtual Threads, ThreadPools
- [[Spring Data JPA]] — deep dive em persistência
- [[Spring Security]] — deep dive em autenticação e autorização
- [[Testes em Java]] — JUnit 5, Mockito, Testcontainers, slices
- [[Testes]] — fundamentos gerais
- [[API Design]] — REST, RFC 9457 Problem Details
- [[03-Dominios/Java/Backend/Kafka/Kafka]] — event streaming com Spring Kafka
- [[System Design]] — troubleshooting cross-stack, building blocks
- [[Arquitetura de Software]] — Hexagonal, DDD, Clean Architecture
