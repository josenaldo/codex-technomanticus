---
title: "ApplicationContext — o container e seu ciclo"
created: 2026-06-08
updated: 2026-06-08
type: concept
progress: backlog
status: seedling
publish: true
fase: adepto
tags:
  - java
  - spring
  - adepto
  - ioc
aliases:
  - "ApplicationContext"
  - "BeanFactory"
---

# ApplicationContext — o container e seu ciclo

> [!abstract] TL;DR
> `ApplicationContext` é a face completa do container Spring: ele **estende** `BeanFactory` com eventos, internacionalização, carregamento de recursos e abstração de ambiente. Em produção, você quase nunca usa `BeanFactory` diretamente — o Spring Boot entrega um `ApplicationContext` já configurado. O ciclo de vida do container gira em torno do método `refresh()`: ao ser chamado, ele carrega definições, instancia singletons e dispara `ContextRefreshedEvent`. Entender esse ciclo é essencial para debug de inicialização, integração com frameworks web e escrita de extensões do container.

## O que é

`ApplicationContext` é a interface central do módulo `spring-context`. Ela herda de `BeanFactory` (que resolve e fornece beans) e acrescenta um conjunto de contratos orientados a aplicação:

- `MessageSource` — internacionalização (i18n) com resolução por locale
- `ResourceLoader` — acesso transparente a arquivos, URLs e resources do classpath
- `ApplicationEventPublisher` — publicação de eventos para listeners registrados
- `HierarchicalBeanFactory` — suporte a contextos pai/filho (ex.: root + web layer)
- `EnvironmentCapable` — acesso a perfis ativos e propriedades de configuração

A distinção prática é que `BeanFactory` faz o mínimo (resolve beans sob demanda) enquanto `ApplicationContext` é o **framework completo**, incluindo pós-processadores, eventos de ciclo de vida e suporte a AOP.

## Por que importa

Em entrevistas e no dia a dia, o candidato precisa saber:

1. **Qual interface usar** — você injeta `ApplicationContext` quando precisa publicar eventos ou carregar recursos dinamicamente; para resolver beans diretamente (`getBean()`), a prática é um anti-pattern (veja Armadilhas).
2. **O que acontece antes do `main` retornar** — o Spring Boot chama `refresh()` automaticamente; falhas de wiring aparecem aqui, não em runtime tardio.
3. **Como estender o container** — `BeanFactoryPostProcessor`, `BeanPostProcessor` e interfaces `*Aware` são os pontos de extensão canonicamente usados por bibliotecas (Spring Security, Spring Data, etc.).

## Como funciona

### BeanFactory vs ApplicationContext (o que o segundo adiciona)

`BeanFactory` resolve beans lazily e não carrega extensões automaticamente. `ApplicationContext`, ao chamar `refresh()`, executa uma sequência enriquecida:

| Capacidade | Interface adicionada | Detalhe |
|---|---|---|
| Internacionalização | `MessageSource` | Procura bean `messageSource`; fallback: `DelegatingMessageSource` vazio |
| Acesso a recursos | `ResourceLoader` | `classpath:`, `file:`, `http:` transparentes |
| Publicação de eventos | `ApplicationEventPublisher` | Sincrono por padrão; pode ser tornado assíncrono via `SimpleApplicationEventMulticaster` com `TaskExecutor` |
| Hierarquia de contextos | `HierarchicalBeanFactory` | Root context (serviços/repositórios) + child context (web/MVC) |
| Abstração de ambiente | `EnvironmentCapable` | Perfis (`@Profile`) e properties (`@Value`, `Environment`) |

Em aplicações simples, `BeanFactory` nunca é instanciada diretamente. Ela aparece principalmente em ambientes com severa restrição de memória (IoT, Android) ou como abstração interna de integrações legadas.

### Tipos concretos (standalone, servlet, reactive)

O Spring oferece implementações para cada estilo de deploy:

**Standalone (linha de comando ou testes):**

```java
// Configuração por anotações — o mais comum hoje
AnnotationConfigApplicationContext ctx =
    new AnnotationConfigApplicationContext(AppConfig.class);

// Configuração XML — legado, ainda válido
ClassPathXmlApplicationContext ctx =
    new ClassPathXmlApplicationContext("beans.xml");
```

**Servlet (Spring MVC / Spring Boot + Tomcat/Jetty):**

- `AnnotationConfigWebApplicationContext` — usado pelo `DispatcherServlet`
- `XmlWebApplicationContext` — suporta "hot refresh" (recarregar sem reiniciar JVM)
- `GenericWebApplicationContext` — não suporta hot refresh; padrão no Spring Boot moderno

**Reactive (Spring WebFlux / Spring Boot + Netty):**

- `AnnotationConfigReactiveWebServerApplicationContext` — entregue automaticamente pelo Boot quando a pilha WebFlux é detectada no classpath

O Spring Boot escolhe a implementação correta baseado no classpath: ausência de `spring-webmvc` e `spring-webflux` → standalone; presença de `spring-webmvc` → servlet; presença de `spring-webflux` (sem MVC) → reactive.

### refresh() e o ciclo do container

`refresh()` é o coração do `AbstractApplicationContext`. Ao ser invocado, ele executa uma sequência determinista de fases:

1. **Preparação do environment** — valida propriedades obrigatórias
2. **Carregamento de `BeanDefinition`s** — lê anotações, XML ou código Java; registra metadados (não instâncias)
3. **Execução de `BeanFactoryPostProcessor`s** — podem modificar definições antes da instanciação (ex.: `PropertySourcesPlaceholderConfigurer` resolve `${...}`)
4. **Registro de `BeanPostProcessor`s** — hooks para envolver beans após criação (AOP proxies, `@Autowired`)
5. **Inicialização de infraestrutura** — `MessageSource`, `ApplicationEventMulticaster`
6. **Instanciação de singletons non-lazy** — todos os beans eager são criados aqui
7. **Publicação de `ContextRefreshedEvent`** — sinal de que o container está pronto

Eventos do ciclo de vida do contexto:

| Evento | Disparado por | Significado |
|---|---|---|
| `ContextRefreshedEvent` | `refresh()` | Container pronto; todos os singletons instanciados |
| `ContextStartedEvent` | `start()` | Beans `Lifecycle` recebem sinal de start explícito |
| `ContextStoppedEvent` | `stop()` | Beans `Lifecycle` recebem sinal de stop explícito |
| `ContextClosedEvent` | `close()` | Singletons destruídos; contexto encerrado |

> [!warning] Hot refresh
> `XmlWebApplicationContext` suporta chamar `refresh()` múltiplas vezes (hot refresh). `GenericApplicationContext` — e portanto `AnnotationConfigApplicationContext` — **não** suporta: uma segunda chamada a `refresh()` lança exceção. O Spring Boot usa a variante que não suporta hot refresh por padrão.

### Interfaces *Aware

O container detecta beans que implementam interfaces `*Aware` durante a fase de pós-processamento e injeta a dependência correspondente via setter, antes de qualquer `@PostConstruct`:

| Interface | Método injetado | O que é fornecido |
|---|---|---|
| `ApplicationContextAware` | `setApplicationContext()` | O próprio `ApplicationContext` |
| `BeanNameAware` | `setBeanName()` | O ID do bean no container |
| `BeanFactoryAware` | `setBeanFactory()` | A `BeanFactory` subjacente |
| `ApplicationEventPublisherAware` | `setApplicationEventPublisher()` | Publisher para emitir eventos |
| `MessageSourceAware` | `setMessageSource()` | `MessageSource` para i18n |
| `ResourceLoaderAware` | `setResourceLoader()` | `ResourceLoader` para carregar arquivos |
| `EnvironmentAware` | `setEnvironment()` | `Environment` com perfis e properties |
| `EmbeddedValueResolverAware` | `setEmbeddedValueResolver(StringValueResolver)` | Resolvedor de placeholders `${...}` para uso em código de infraestrutura |

Interfaces `*Aware` são usadas principalmente por código de infraestrutura e integrações. Em código de aplicação, prefira injeção via `@Autowired` ou construtor.

## Na prática

Em 99% dos casos, você **não injeta `ApplicationContext` diretamente** — o Spring resolve dependências via `@Autowired` ou construtor sem que o bean precise saber que há um container.

Os casos legítimos de injeção são:

- **Publicação de eventos** — prefira `ApplicationEventPublisher` (interface mais estreita)
- **Carregamento dinâmico de recursos** — `ResourceLoader` ou `ResourcePatternResolver`
- **Lookup de bean por tipo em runtime** — raro, mas existem cenários (fábricas dinâmicas)

```java
// Caso legítimo: publicar evento de domínio
@Service
public class OrderService implements ApplicationEventPublisherAware {

    private ApplicationEventPublisher publisher;

    @Override
    public void setApplicationEventPublisher(ApplicationEventPublisher publisher) {
        this.publisher = publisher;
    }

    public void placeOrder(Order order) {
        // lógica de negócio...
        publisher.publishEvent(new OrderPlacedEvent(this, order.getId()));
    }
}

// Alternativa idiomática no Spring 4.2+: injeção via @Autowired
@Service
public class OrderService {

    private final ApplicationEventPublisher publisher;

    public OrderService(ApplicationEventPublisher publisher) {
        this.publisher = publisher;
    }

    public void placeOrder(Order order) {
        publisher.publishEvent(new OrderPlacedEvent(this, order.getId()));
    }
}
```

> [!tip] Prefira interfaces estreitas
> Se precisar apenas publicar eventos, injete `ApplicationEventPublisher`. Se precisar apenas de resources, injete `ResourceLoader`. Injetar o `ApplicationContext` completo expõe mais superfície do que necessário e é sinal de que o design pode ser melhorado.

## Armadilhas

### (1) Service-locator anti-pattern com getBean()

Chamar `applicationContext.getBean(ProductRepository.class)` dentro de um `@Service` transforma o container num localizador de serviços: o código passa a depender do container explicitamente, o que dificulta testes (você precisa de um contexto real ou mockar o `ApplicationContext`) e esconde dependências da assinatura do construtor.

```java
// ERRADO — service locator oculta dependências
@Service
public class ProductService {

    @Autowired
    private ApplicationContext ctx;

    public Product findProduct(Long id) {
        ProductRepository repo = ctx.getBean(ProductRepository.class); // anti-pattern
        return repo.findById(id).orElseThrow();
    }
}

// CORRETO — dependência declarada no construtor
@Service
public class ProductService {

    private final ProductRepository repo;

    public ProductService(ProductRepository repo) {
        this.repo = repo;
    }

    public Product findProduct(Long id) {
        return repo.findById(id).orElseThrow();
    }
}
```

**Fix:** declare todas as dependências no construtor ou via `@Autowired` em campo/setter.

### (2) Assumir lazy onde o padrão é eager

Singletons são instanciados durante `refresh()`, **não** na primeira chamada. Desenvolvedores que esperam inicialização tardia podem se surpreender com exceções de wiring no startup — antes de qualquer request chegar.

```java
// O bean abaixo falha no startup se DataSource não estiver configurado,
// NÃO na primeira chamada a findAll()
@Repository
public class CustomerRepository {

    private final JdbcTemplate jdbc;

    public CustomerRepository(DataSource ds) {
        this.jdbc = new JdbcTemplate(ds); // lançado durante refresh()
    }
}
```

**Fix:** se inicialização tardia for necessária (ex.: integração opcional), use `@Lazy` ou `@ConditionalOn*` do Boot para não registrar o bean quando o recurso estiver ausente. Em testes, prefira `@SpringBootTest` com contexto completo para detectar falhas de wiring cedo.

### (3) Segurar referência ao contexto além do escopo necessário

Guardar o `ApplicationContext` em variável estática (padrão comum em código legado para integração com frameworks sem DI) impede que o GC libere o contexto após o shutdown e causa vazamentos em ambientes de hot-deploy (servidores de aplicação que fazem reload de webapps).

```java
// PROBLEMÁTICO — vazamento em hot-deploy
public class LegacyBridge {
    private static ApplicationContext ctx; // mantém classloader vivo

    public static void init(ApplicationContext context) {
        ctx = context;
    }
}
```

**Fix:** injete as dependências específicas de que `LegacyBridge` precisa (ex.: o serviço ou repositório) em vez do contexto inteiro. Se a integração for inevitável, registre um `ApplicationListener<ContextClosedEvent>` para limpar a referência estática no shutdown.

## Em entrevista

### Frase pronta (inglês)

"`ApplicationContext` extends `BeanFactory` with enterprise features: event publishing, internationalization, resource loading, and environment abstraction. The container lifecycle revolves around the `refresh()` method, which loads bean definitions, runs post-processors, and pre-instantiates all non-lazy singletons — raising `ContextRefreshedEvent` when ready. In practice, you should avoid injecting `ApplicationContext` directly and rely on constructor injection instead; using `getBean()` as a service locator is a well-known anti-pattern that hides dependencies and makes testing harder."

### Vocabulário

| Termo PT | Termo EN |
|---|---|
| Container de inversão de controle | IoC container |
| Contexto de aplicação | Application context |
| Definição de bean | Bean definition |
| Pós-processador de bean | Bean post-processor |
| Carregamento antecipado (padrão) | Eager instantiation (default) |
| Carregamento tardio | Lazy initialization |
| Publicação de evento | Event publishing |
| Escuta de evento | Event listening |
| Abstração de ambiente | Environment abstraction |
| Localizador de serviços (anti-pattern) | Service locator (anti-pattern) |

## Veja também

- [[03-Dominios/Java/Spring Core e Boot/02 - IoC e injeção de dependência no Spring|IoC e injeção de dependência no Spring]]
- [[03-Dominios/Java/Spring Core e Boot/07 - Ciclo de vida e escopos de beans|Ciclo de vida e escopos de beans]]
- [[03-Dominios/Java/Jakarta EE/04 - CDI — beans e injeção|CDI — beans e injeção]] (o container da spec)
- [[03-Dominios/Java/Spring Core e Boot/index|Spring Core e Boot (MOC do galho)]]
- [[03-Dominios/Java/index|Trilha Java]]
- [[03-Dominios/Java/Dicionário de Java#ApplicationContext|ApplicationContext]]
- [[03-Dominios/Java/Dicionário de Java#BeanFactory|BeanFactory]]

## Referências

- Spring Framework Reference — [The ApplicationContext](https://docs.spring.io/spring-framework/reference/core/beans/context-introduction.html) (Framework 6.x / Boot 3.x)
- Spring Framework Reference — [BeanFactory or ApplicationContext?](https://docs.spring.io/spring-framework/reference/core/beans/beanfactory.html)
- Spring Framework Reference — [Container Extension Points](https://docs.spring.io/spring-framework/reference/core/beans/factory-extension.html)
