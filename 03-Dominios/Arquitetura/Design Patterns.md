---
title: "Design Patterns"
created: 2026-04-01
updated: 2026-04-09
type: concept
status: evergreen
tags:
  - arquitetura
  - entrevista
publish: false
---

# Design Patterns

Soluções catalogadas e reutilizáveis para problemas recorrentes em design de software. Em entrevistas de senior, o que se espera não é recitar os 23 padrões do GoF — é **reconhecer** quando um padrão resolve um problema real, **implementá-lo** de forma idiomática na linguagem/framework, e **saber quando não usar** (a armadilha mais comum).

## O que é

Um **design pattern** é uma descrição de uma solução genérica para um problema de design que se repete. Os 23 padrões clássicos foram catalogados em 1994 pelo *Gang of Four* (Gamma, Helm, Johnson, Vlissides) no livro *Design Patterns: Elements of Reusable Object-Oriented Software*.

Padrões não são bibliotecas nem código para copiar — são **vocabulário**. Dizer "aqui precisa de um Strategy" é mais rápido que descrever "uma interface com implementações intercambiáveis selecionadas em runtime".

### Três categorias clássicas

1. **Criacionais** — como objetos são criados (Singleton, Factory, Builder, Prototype, Abstract Factory)
2. **Estruturais** — como objetos são compostos (Adapter, Decorator, Facade, Proxy, Composite, Bridge, Flyweight)
3. **Comportamentais** — como objetos interagem (Strategy, Observer, Command, Template Method, Iterator, State, Chain of Responsibility, Mediator, Memento, Visitor, Interpreter)

### Patterns em um mundo com frameworks

A maioria dos frameworks modernos **já implementa** os padrões mais importantes. Você raramente escreve um Singleton "à mão" em Spring — você anota `@Service` e o container gerencia. Reconhecer os padrões aplicados pelo framework é mais importante que reimplementá-los.

---

## Padrões Criacionais

### Singleton

Garante que uma classe tenha **apenas uma instância** e fornece um ponto global de acesso a ela.

**Onde aparece naturalmente:**

- Beans do Spring (`@Service`, `@Component`, `@Repository`) — escopo default é singleton
- `Runtime.getRuntime()` em Java
- Connection pools, loggers, caches compartilhados

**Implementação manual em Java (raramente necessária):**

```java
public class Config {
    private static final Config INSTANCE = new Config();
    private Config() { /* privado */ }
    public static Config getInstance() { return INSTANCE; }
}

// Ou, thread-safe e lazy via enum (idiomático):
public enum Config {
    INSTANCE;
    public void load() { /* ... */ }
}
```

**Armadilhas:**

- **Singleton mutável = estado global** — dificulta testes, causa bugs de concorrência
- **Esconde dependências** — código que chama `Config.getInstance()` depende de Config sem declarar isso no construtor
- **Dificulta mock em testes** — prefira injeção de dependência com escopo singleton gerenciado pelo container

> **Regra prática moderna:** em vez de implementar Singleton, declare a classe como bean e deixe o container (Spring, Guice, Nest) cuidar do ciclo de vida. Você ganha o escopo singleton **sem** o acoplamento do padrão clássico.

### Factory Method

Define uma interface para criar objetos, mas delega a decisão de **qual classe concreta** instanciar.

```java
public interface NotificationFactory {
    Notification create(NotificationType type);
}

public class DefaultNotificationFactory implements NotificationFactory {
    public Notification create(NotificationType type) {
        return switch (type) {
            case EMAIL -> new EmailNotification();
            case SMS   -> new SmsNotification();
            case PUSH  -> new PushNotification();
        };
    }
}
```

**Quando usar:**

- A escolha da classe depende de configuração, contexto ou input do usuário
- Encapsular lógica complexa de criação em um só lugar
- Permitir que subclasses mudem o tipo criado (Template Method + Factory)

**Variação Spring-friendly:** injete `Map<String, Notification>` — o Spring popula com todos os beans, indexados por nome. Use `@Qualifier` ou um "resolver" que seleciona pela chave.

### Abstract Factory

Factory de factories: uma interface para criar **famílias** de objetos relacionados. Usado quando você precisa trocar múltiplos objetos em conjunto (ex.: tema claro vs escuro, onde cada tema cria seus próprios botões, janelas, scrollbars).

Raro em backend moderno — quando aparece, é em bibliotecas de UI ou configurações de ambiente.

### Builder

Constrói objetos complexos **passo a passo**. Resolve o problema do "construtor com 10 parâmetros" e permite objetos imutáveis com muitos campos opcionais.

```java
// Com Lombok
@Builder
public class User {
    private final String name;
    private final String email;
    private final Role role;
    private final Address address;
    private final LocalDate birthdate;
}

var user = User.builder()
    .name("Josenaldo")
    .email("jm@example.com")
    .role(Role.ADMIN)
    .build();
```

**Quando usar:**

- Construtor com 4+ parâmetros
- Muitos parâmetros opcionais
- Objetos imutáveis complexos
- Construção com etapas de validação

**Na biblioteca padrão:** `StringBuilder`, `Stream.Builder`, `HttpRequest.newBuilder()`.

### Prototype

Cria novos objetos **clonando** um existente. Útil quando a criação é cara (ex.: objeto carregado do banco) e você quer uma cópia modificável.

Em Java: `Object.clone()` (cuidado: shallow por default) ou copy constructor. Em JS/TS: `structuredClone()` ou `{ ...obj }` para shallow.

> Raramente é a resposta em entrevistas modernas — prefira imutabilidade + método `with...()` que retorna nova instância.

---

## Padrões Estruturais

### Adapter

Converte a interface de uma classe para outra **esperada pelo cliente**. Ponte entre código novo e legado, ou entre sua aplicação e APIs de terceiros.

```java
// Cliente espera:
interface PaymentGateway {
    PaymentResult charge(Money amount, String customerId);
}

// Biblioteca de terceiros tem interface diferente:
class StripeClient {
    public StripeCharge createCharge(long cents, String currency, String customer) { /* ... */ }
}

// Adapter
class StripeAdapter implements PaymentGateway {
    private final StripeClient stripe;

    public PaymentResult charge(Money amount, String customerId) {
        StripeCharge charge = stripe.createCharge(
            amount.getCents(),
            amount.getCurrency().getCode(),
            customerId
        );
        return PaymentResult.fromStripe(charge);
    }
}
```

**Quando usar:** integrar bibliotecas externas mantendo sua aplicação livre do vocabulário delas. Essencial para Ports & Adapters (Hexagonal Architecture).

### Decorator

Adiciona comportamento a um objeto **sem alterar sua classe**, envolvendo-o em outro objeto que implementa a mesma interface.

```java
// Biblioteca padrão Java: decorators de I/O
InputStream in = new BufferedInputStream(           // buffering
    new GZIPInputStream(                            // descompressão
        new FileInputStream("data.gz")              // leitura
    )
);
```

**Diferença para herança:** decorator adiciona comportamento **em runtime**, de forma composicional. Você pode empilhar múltiplos decorators na mesma instância.

**Em frameworks:**

- Java I/O streams
- Spring AOP (aspects decoram beans)
- Express / NestJS middleware
- Decorators de TypeScript (`@Transactional`, `@Cacheable`)

### Facade

Interface **simplificada** para um subsistema complexo. Esconde múltiplas classes/dependências atrás de uma API única e limpa.

```java
@Service
public class CheckoutFacade {
    private final CartService cart;
    private final InventoryService inventory;
    private final PaymentGateway payment;
    private final OrderRepository orders;
    private final NotificationService notifications;

    public OrderResult checkout(CheckoutRequest req) {
        inventory.reserve(req.items());
        PaymentResult result = payment.charge(req.amount(), req.customerId());
        Order order = orders.save(Order.from(req, result));
        notifications.sendConfirmation(order);
        return OrderResult.success(order);
    }
}
```

**Onde aparece:** quase todo service do Spring é uma Facade sobre repositórios + clients + validators. Facade é o padrão mais usado do mundo, mesmo sem você perceber.

### Proxy

Objeto que **controla acesso** a outro objeto, implementando a mesma interface. Pode adicionar lazy loading, caching, logging, segurança, ou chamadas remotas transparentes.

**Onde aparece:**

- **JPA/Hibernate** — entidades carregadas lazy são proxies que buscam dados ao primeiro `get`
- **Spring AOP** — aspects são implementados via proxies dinâmicos (JDK dynamic proxy ou CGLIB)
- **`@Transactional`** — o método anotado é chamado através de um proxy que abre/commita/rollback da transação
- **`@Cacheable`** — proxy checa cache antes de chamar o método real
- **gRPC / REST clients** — chamadas remotas aparentam ser chamadas locais

> **Pegadinha clássica:** `@Transactional` em método privado ou chamada interna (`this.metodo()`) **não funciona** porque o proxy só intercepta chamadas externas.

### Composite

Compõe objetos em estruturas de árvore para representar hierarquias parte-todo. Cliente trata objetos individuais e composições **da mesma forma**.

**Uso clássico:** sistema de arquivos (arquivo e diretório implementam a mesma interface), árvores de UI, expressões matemáticas.

---

## Padrões Comportamentais

### Strategy

Encapsula algoritmos intercambiáveis por trás de uma interface. O cliente seleciona a implementação em runtime.

```java
public interface DiscountStrategy {
    Money apply(Money amount, Customer customer);
}

public class NoDiscountStrategy implements DiscountStrategy { /* ... */ }
public class LoyalCustomerStrategy implements DiscountStrategy { /* 10% off */ }
public class BlackFridayStrategy implements DiscountStrategy { /* 30% off */ }

@Service
public class CheckoutService {
    public Money finalPrice(Money base, Customer c, DiscountStrategy strategy) {
        return strategy.apply(base, c);
    }
}
```

**Spring idiomático:** injete `Map<String, DiscountStrategy>` — o container popula automaticamente com todos os beans da interface, indexados pelo nome.

```java
@Service
public class CheckoutService {
    private final Map<String, DiscountStrategy> strategies;

    public Money finalPrice(Money base, Customer c, String strategyName) {
        return strategies.get(strategyName).apply(base, c);
    }
}
```

**Pegadinha:** se você tem **uma só implementação** e **nenhuma perspectiva** de ter outras, não crie a interface. É abstração prematura.

### Observer (Publish-Subscribe)

Define uma dependência um-para-muitos: quando um objeto muda, todos os dependentes são **notificados automaticamente**. Base de sistemas event-driven.

```java
// Spring Events
public record OrderCreatedEvent(Long orderId, BigDecimal total) { }

@Service
public class OrderService {
    private final ApplicationEventPublisher events;

    public void createOrder(Order o) {
        orderRepository.save(o);
        events.publishEvent(new OrderCreatedEvent(o.getId(), o.getTotal()));
    }
}

@Component
public class InventoryListener {
    @EventListener
    public void onOrderCreated(OrderCreatedEvent event) {
        // reduzir estoque, sem acoplar InventoryListener ao OrderService
    }
}
```

**Onde aparece:**

- Spring `ApplicationEvent` e `@EventListener`
- Node.js `EventEmitter`
- DOM events no navegador
- Domain events no DDD
- Reactive streams (RxJava, Project Reactor, RxJS)
- Sistemas de mensageria como Kafka, RabbitMQ (observer distribuído)

**Armadilha:** listeners que nunca são removidos causam **memory leaks**. Em Spring isso não é problema (beans vivem durante a app), mas em UIs ou código dinâmico, sim.

### Command

Encapsula uma requisição como um **objeto**. Isso permite parametrizar clientes com operações, enfileirá-las, registrar no log, desfazer/refazer.

```java
public interface Command {
    void execute();
    void undo();
}

public class MoveCommand implements Command {
    private final Entity entity;
    private final Point from, to;

    public void execute() { entity.moveTo(to); }
    public void undo()    { entity.moveTo(from); }
}
```

**Onde aparece:**

- Undo/redo em editores
- Filas de tarefas (a tarefa é um Command serializado)
- CQRS (Command Query Responsibility Segregation) — Commands mutam, Queries leem
- GUI actions (Swing, Android)

### Template Method

Define o **esqueleto** de um algoritmo em uma classe base; subclasses preenchem os passos variáveis.

```java
public abstract class ReportGenerator {
    public final String generate() {
        String header = buildHeader();
        String body   = buildBody();
        String footer = buildFooter();
        return header + body + footer;
    }

    protected abstract String buildHeader();
    protected abstract String buildBody();
    protected String buildFooter() { return "— fim —"; } // default
}

public class SalesReport extends ReportGenerator {
    protected String buildHeader() { /* ... */ }
    protected String buildBody()   { /* ... */ }
}
```

**Quando usar:** quando múltiplas classes compartilham um algoritmo com variações pequenas em passos específicos.

**Moderno:** muitas vezes substituível por composição + lambdas, especialmente em linguagens funcionais ou Java moderno com interfaces funcionais.

### State

Permite que um objeto altere seu comportamento quando seu **estado interno** muda. Parece que a classe mudou de tipo.

```java
public class Order {
    private OrderState state = new PendingState();

    public void approve() { state.approve(this); }
    public void cancel()  { state.cancel(this); }

    void setState(OrderState state) { this.state = state; }
}

interface OrderState {
    void approve(Order order);
    void cancel(Order order);
}

class PendingState implements OrderState {
    public void approve(Order o) { o.setState(new ApprovedState()); }
    public void cancel(Order o)  { o.setState(new CancelledState()); }
}
```

Alternativa simples: máquina de estados com enum. State pattern é útil quando cada estado tem comportamento complexo.

### Chain of Responsibility

Passa uma requisição por uma **cadeia** de handlers até que um deles a processe.

**Onde aparece:**

- Servlet filters
- Spring Security filter chain
- Middleware no Express / NestJS
- Log handlers em hierarquia (Java Logging, SLF4J)
- Pipelines de validação

### Iterator

Fornece uma maneira de acessar elementos de uma coleção **sem expor** sua representação interna.

Já é nativo de praticamente todas as linguagens modernas (`Iterator` em Java, `for...of` em JS/TS, `__iter__` em Python). Você raramente implementa, mas consome o tempo todo.

### Mediator

Define um objeto que **encapsula interações** entre um conjunto de objetos, reduzindo acoplamento direto entre eles.

**Onde aparece:** command buses (CQRS), MediatR em .NET, Spring `ApplicationEventMulticaster` internamente.

### Visitor

Permite adicionar operações a uma estrutura de objetos **sem modificá-los**. Útil quando você tem muitos tipos e quer adicionar novas operações frequentemente.

Pouco comum em Java/TS do dia a dia — mais usado em compiladores, AST traversal, análise estática. Em linguagens com pattern matching (Scala, Kotlin, Java 21+ com sealed types), é substituído por `switch` sobre tipos selados.

---

## Padrões de arquitetura (não-GoF)

Padrões que transcendem classes e estruturam módulos ou sistemas inteiros. Frequentemente confundidos com GoF em entrevistas.

### Repository

Abstração sobre persistência. Esconde o mecanismo de acesso a dados (banco, API, arquivo) atrás de uma interface que parece uma coleção em memória.

```java
public interface UserRepository {
    Optional<User> findById(Long id);
    User save(User user);
    void deleteById(Long id);
}
```

**Spring Data JPA** implementa Repository pattern de forma canônica: você declara uma interface estendendo `JpaRepository`, e o Spring gera a implementação em runtime.

### Unit of Work

Mantém uma lista de mudanças feitas durante uma operação de negócio e as persiste de uma só vez, em uma transação. Hibernate `Session` e JPA `EntityManager` implementam Unit of Work.

### DTO (Data Transfer Object)

Objeto simples usado para **transferir dados** entre camadas (controller ↔ service) ou entre sistemas (API ↔ cliente). Sem comportamento de negócio. Em Java moderno, `record` é ideal.

```java
public record UserResponse(Long id, String name, String email) { }
```

### MVC / MVP / MVVM

Separação de responsabilidades em UIs. Spring MVC implementa Model-View-Controller classicamente.

### Dependency Injection / IoC

Inversão de controle: o objeto não cria suas dependências — elas são **fornecidas**. Base de Spring, Nest, Angular, Guice.

### Event Sourcing

Em vez de armazenar o **estado atual**, armazena a **sequência de eventos** que levou a ele. Estado é reconstruído aplicando eventos.

### CQRS

Separa comandos (escritas) de queries (leituras), frequentemente com modelos e até bancos diferentes para cada um.

### Saga

Coordena transações distribuídas em múltiplos serviços através de uma série de passos, com compensação em caso de falha.

---

## Padrões em frameworks do dia a dia

| Padrão | Onde você já usa | Framework |
| --- | --- | --- |
| Singleton | Beans Spring (`@Service`, `@Component`) | Spring IoC |
| Factory | `BeanFactory`, `@Bean` methods | Spring |
| Builder | `@Builder` (Lombok), `HttpRequest.newBuilder()` | Lombok, Java HTTP client |
| Prototype | `@Scope("prototype")` | Spring |
| Observer | `@EventListener`, `EventEmitter` | Spring Events, Node |
| Strategy | Injeção de `Map<String, Impl>` | Spring, Comparator em Java |
| Decorator | AOP, middleware, I/O streams | Spring AOP, Express, Java NIO |
| Proxy | `@Transactional`, `@Cacheable`, lazy loading | Spring, JPA |
| Facade | Qualquer `@Service` que orquestra outros | Spring |
| Adapter | Wrappers de SDK de terceiros | Qualquer integração |
| Chain of Responsibility | Filter chain, middleware pipeline | Spring Security, Express |
| Template Method | `JdbcTemplate`, `RestTemplate` | Spring |
| Iterator | `for...of`, `Iterator`, streams | Linguagem padrão |
| Command | Filas, CQRS, undo/redo | RabbitMQ, MediatR |
| Repository | `JpaRepository` | Spring Data |
| DI / IoC | Injeção de construtor | Spring, Nest, Angular |

---

## Quando usar (e quando não)

### Sinais de que você precisa de um pattern

- **Strategy:** "preciso escolher entre múltiplos algoritmos para a mesma operação, e a escolha depende de contexto"
- **Observer:** "uma ação dispara múltiplas reações que não deveriam conhecer o disparador"
- **Builder:** "meu construtor tem 4+ parâmetros ou muitos opcionais"
- **Factory:** "a criação do objeto envolve lógica condicional complexa"
- **Adapter:** "preciso integrar uma API que não segue minha interface"
- **Decorator:** "quero adicionar comportamento sem mudar a classe base, possivelmente empilhando"
- **Facade:** "este fluxo atravessa 5 serviços e o controller está sujo"
- **Template Method:** "quatro classes fazem quase a mesma coisa com 2 passos diferentes"

### Sinais de que **não** precisa

- **Uma só implementação da interface, sem previsão de outras.** É abstração prematura.
- **O padrão torna o código mais difícil de ler** sem benefício concreto.
- **Você está aplicando porque "é um pattern do livro"**, não porque resolve um problema real.
- **O framework já resolve.** Spring Singleton é melhor que o seu Singleton artesanal.
- **Um `if/else` claro e legível** resolve sem cerimônia.

---

## Anti-patterns comuns

- **Pattern mania / Pattern overuse:** aplicar padrões onde código direto resolveria. Adiciona cerimônia sem benefício.
- **Singleton mutável:** estado global compartilhado. Dificulta testes, causa bugs de concorrência.
- **Singleton para tudo:** classes utilitárias viram Singletons "para não instanciar". Use `static` methods ou beans.
- **Abstract Factory prematura:** fábricas de fábricas sem necessidade. YAGNI.
- **Strategy com uma implementação:** criar interface + classe sem plano para segunda implementação.
- **Observer sem unsubscribe:** memory leaks em UIs e código dinâmico.
- **Golden Hammer:** "quando você só tem um martelo, tudo parece prego". Aplicar o mesmo padrão preferido em todo problema.
- **God Facade:** Facade que cresce indefinidamente e vira um God Object.
- **Reimplementar o que o framework faz:** escrever seu próprio container de DI, seu próprio event bus, seu próprio proxy. Use o framework.
- **Confundir padrão com arquitetura:** "minha arquitetura é baseada em Strategy" não é uma arquitetura.

---

## Na prática (da minha experiência)

> Em Spring Boot, os padrões mais úteis no dia a dia são **Strategy**, **Observer** (Spring Events), **Facade** (services orquestradores) e **Proxy** (via `@Transactional` e `@Cacheable`). Raramente implemento à mão — o framework faz — mas **reconhecer** o padrão aplicado é o que me permite debugar quando algo quebra.
>
> Um caso concreto de Strategy: no MedEspecialista, o cálculo de comissão médica tinha cinco regras dependendo do tipo de convênio. A primeira versão era um `if-else-if` de 80 linhas em um service. Refatorei para `ComissaoStrategy` + cinco implementações, injetadas via `Map<TipoConvenio, ComissaoStrategy>`. Adicionar um novo tipo de convênio virou criar uma classe — zero alteração no service.
>
> O oposto: já vi (e cometi) Strategy prematuro. Uma interface `EmailTemplateStrategy` com **uma única implementação** que ficou assim por três anos. Em retrospecto, deveria ter sido apenas uma classe concreta. Não crie abstrações para o futuro hipotético — crie quando a segunda implementação aparecer.
>
> **Pegadinha que já me pegou:** `@Transactional` em método privado ou chamada interna (`this.outroMetodo()`). O proxy do Spring não intercepta, e a transação não abre. Entender que `@Transactional` é Proxy — não mágica — resolveu esse debugging.
>
> **Sobre Observer (Spring Events):** extremamente útil para desacoplar ações pós-operação (enviar email depois de cadastro, indexar no Elasticsearch depois de salvar). Mas cuidado: eventos síncronos rodam na mesma thread da transação. Se o listener falhar, pode afetar o fluxo principal. Para fire-and-forget real, use `@Async` + `@EventListener` com cuidado.

---

## How to explain in English

> "Design patterns are part of my everyday vocabulary, but I use them through frameworks much more often than I implement them by hand. In a Spring Boot application, the IoC container itself is a massive application of Dependency Injection and Singleton — every `@Service` bean is a singleton managed by the framework. When I write `@Transactional` or `@Cacheable`, I'm relying on the Proxy pattern that Spring creates dynamically around my beans.
>
> The patterns I reach for most deliberately are Strategy, Observer, Builder, and Facade. Strategy when I have multiple algorithms for the same operation — for example, different commission calculation rules based on insurance type — I'll define an interface, inject a map of implementations, and let a resolver pick the right one at runtime. Observer through Spring Events to decouple side effects like sending emails after registration. Builder whenever a constructor has more than a few parameters. Facade in almost every service — that's what a well-designed `@Service` class really is.
>
> What I've learned to avoid is pattern overuse. Early in my career, I'd create a Strategy interface with one implementation, 'just in case we need another one later'. Three years later, the second implementation never arrived, and the code was harder to follow for no reason. Now I follow YAGNI — I add the abstraction when I actually have two implementations, not before. A clear `if-else` beats a premature abstraction every time.
>
> The other thing I emphasize is recognizing patterns in the framework. `@Transactional` is Proxy. `@EventListener` is Observer. Spring Data `JpaRepository` is Repository. Knowing these helps me debug — for example, understanding why `@Transactional` doesn't work on a private method or an internal call is much easier when you know it's a proxy, not magic."

### Frases úteis em entrevista

- "I'd reach for a Strategy pattern here because the selection between algorithms depends on runtime context."
- "This is essentially a Proxy — the framework wraps the bean to add cross-cutting behavior."
- "I'd avoid introducing a Factory here; there's only one implementation, so a direct constructor call is simpler."
- "That's the Observer pattern implemented via Spring Events — the publisher doesn't know about the subscribers."
- "I'd model this as a Facade — the controller is doing too much orchestration; let's push it into a service."
- "We can use the Command pattern if we need to queue, log, or undo these operations later."
- "Premature abstraction is as bad as no abstraction. I'd wait for a second use case before introducing the pattern."

### Key vocabulary

- padrão de projeto → design pattern
- padrão criacional → creational pattern
- padrão estrutural → structural pattern
- padrão comportamental → behavioral pattern
- inversão de controle → inversion of control (IoC)
- injeção de dependência → dependency injection (DI)
- desacoplamento → decoupling / loose coupling
- fábrica → factory
- construtor → builder
- procuração → proxy
- adaptador → adapter
- decorador → decorator
- fachada → facade
- estratégia → strategy
- observador → observer
- método modelo → template method
- cadeia de responsabilidade → chain of responsibility
- abstração prematura → premature abstraction
- anti-padrão → anti-pattern

---

## Recursos

### Livros

- *Design Patterns: Elements of Reusable Object-Oriented Software* — Gamma, Helm, Johnson, Vlissides (GoF, o clássico)
- *Head First Design Patterns* — Freeman & Robson (acessível, didático)
- *Patterns of Enterprise Application Architecture* — Martin Fowler (patterns de arquitetura, não GoF)
- *Refactoring* — Martin Fowler (mostra quando aplicar padrões via refactoring)
- *Effective Java* — Joshua Bloch (Item 1: static factory methods; Item 2: Builder; etc.)

### Online

- [Refactoring Guru — Design Patterns](https://refactoring.guru/design-patterns) — catálogo visual com exemplos em várias linguagens
- [Source Making — Design Patterns](https://sourcemaking.com/design_patterns) — descrições práticas
- [Java Design Patterns](https://java-design-patterns.com/) — repositório com exemplos em Java idiomático

## Veja também

- [[Orientação a Objetos]] — os princípios SOLID que motivam os padrões
- [[Arquitetura de Software]]
- [[Spring Boot]] — onde muitos padrões aparecem na prática
- [[API Design]]
