---
title: "Eventos do ApplicationContext"
created: 2026-06-08
updated: 2026-08-25
type: concept
progress: backlog
status: seedling
publish: true
fase: adepto
tags:
  - java
  - spring
  - adepto
  - eventos
aliases:
  - "@EventListener"
  - "ApplicationEvent"
---

# Eventos do ApplicationContext

> [!abstract] TL;DR
> O Spring oferece um mecanismo de pub/sub in-process via `ApplicationEventPublisher.publishEvent()`. Desde o Spring 4.2, qualquer POJO pode ser evento — sem precisar estender `ApplicationEvent`. Ouvintes são métodos anotados com `@EventListener`. A entrega é **síncrona por padrão**: o publisher bloqueia até todos os listeners terminarem. Para não bloquear, combine `@EventListener` com `@Async`. O Spring Boot adiciona eventos próprios ao ciclo de startup, sendo `ApplicationReadyEvent` o ponto mais tardio e seguro para inicializar recursos.

## O que é

O `ApplicationContext` implementa a interface `ApplicationEventPublisher`, que expõe o método `publishEvent(Object event)`. Qualquer bean pode injetar essa interface (ou o próprio contexto) e disparar eventos para os demais beans sem que remetente e receptor se conheçam diretamente — o clássico padrão Observer aplicado ao container Spring.

Existem dois tipos de evento:

| Abordagem | Quando usar |
|-----------|-------------|
| POJO simples (Spring 4.2+) | Qualquer objeto; Spring envolve automaticamente em `PayloadApplicationEvent` | 
| Classe que estende `ApplicationEvent` | Necessário para acessar `getSource()` e timestamp diretamente |

A abordagem POJO é preferida em código moderno: menos acoplamento à API do framework.

## Por que importa

- **Desacoplamento**: o publicador não precisa saber quantos ou quais beans estão ouvindo.
- **Reação a ciclo de vida**: código que precisa rodar após o contexto estar completamente pronto usa `ApplicationReadyEvent` sem poluir a lógica de negócio.
- **Alternativa ao observer manual**: evita criar `List<Listener>` + iterar manualmente; o container faz o dispatch.
- **Preparação para sistemas orientados a eventos**: o modelo mental é idêntico ao de mensageria assíncrona (Kafka, RabbitMQ), porém in-process e síncrono por default — o contraste in-process vs broker é o galho [[03-Dominios/Tecnologia/Java/Mensageria/16 - Eventos in-process do Spring|Mensageria]].

Em entrevistas, dominar esse mecanismo demonstra conhecimento do ciclo de vida do Spring além de simples `@Autowired`.

## Como funciona

### Publicar e ouvir (ApplicationEventPublisher, POJO events, @EventListener)

Para publicar, injeta-se `ApplicationEventPublisher` (ou `ApplicationContext`) e chama-se `publishEvent`:

```java
@Service
public class OrderService {

    private final ApplicationEventPublisher publisher;

    public OrderService(ApplicationEventPublisher publisher) {
        this.publisher = publisher;
    }

    public void placeOrder(Order order) {
        // lógica de negócio...
        publisher.publishEvent(new OrderPlacedEvent(order.getId()));
    }
}
```

O evento pode ser um POJO simples:

```java
public record OrderPlacedEvent(Long orderId) {}
```

Para ouvir, basta anotar um método de bean com `@EventListener`:

```java
@Component
public class NotificationListener {

    @EventListener
    public void onOrderPlaced(OrderPlacedEvent event) {
        // envia notificação, atualiza cache, etc.
    }
}
```

Não é necessário implementar nenhuma interface. O Spring descobre os métodos `@EventListener` via pós-processamento do contexto.

**Recursos adicionais do `@EventListener`:**

- Múltiplos tipos: `@EventListener({OrderPlacedEvent.class, OrderCancelledEvent.class})`
- Filtragem via SpEL: `@EventListener(condition = "#event.orderId > 0")`
- Encadeamento: retornar outro objeto do método publica esse objeto como novo evento
- Ordenação: `@Order(10)` controla a sequência entre múltiplos listeners do mesmo evento

### Síncrono por default vs @Async events

Por padrão, `publishEvent` **bloqueia a thread do publicador** até que todos os listeners terminem. Isso garante que, dentro de uma transação, os listeners enxergam os mesmos dados que o publicador vê antes do commit.

Quando o processamento do listener for pesado (envio de e-mail, chamada HTTP), usar `@Async` para não atrasar o fluxo principal:

```java
@Component
public class EmailListener {

    @EventListener
    @Async
    public void onOrderPlaced(OrderPlacedEvent event) {
        // executa em thread separada do pool de @EnableAsync
    }
}
```

**Cuidados com `@Async`:**

- Exceções não propagam ao publicador; configure `AsyncUncaughtExceptionHandler`.
- Retornar valor de um método `@Async` não publica um segundo evento (o retorno é ignorado).
- `ThreadLocal` e contexto de logging (MDC) não são propagados automaticamente; copiar manualmente se necessário.
- Requer `@EnableAsync` na classe de configuração.

Para despacho assíncrono global (todos os listeners), configure `ApplicationEventMulticaster`:

```java
@Bean
ApplicationEventMulticaster applicationEventMulticaster(TaskExecutor taskExecutor) {
    SimpleApplicationEventMulticaster multicaster = new SimpleApplicationEventMulticaster();
    multicaster.setTaskExecutor(taskExecutor);
    return multicaster;
}
```

### Eventos built-in do contexto (ContextRefreshedEvent, ApplicationReadyEvent)

O Spring Framework publica eventos automáticos ao longo do ciclo de vida do contexto:

| Evento | Momento |
|--------|---------|
| `ContextRefreshedEvent` | Contexto inicializado ou recarregado; todos os singletons prontos |
| `ContextStartedEvent` | Após `context.start()` explícito; beans `Lifecycle` recebem sinal de início |
| `ContextStoppedEvent` | Após `context.stop()` explícito; contexto pode ser reiniciado |
| `ContextClosedEvent` | Contexto fechado; todos os singletons serão destruídos |

O **Spring Boot** acrescenta eventos de startup ordenados:

| Evento | Momento |
|--------|---------|
| `ApplicationStartingEvent` | Antes de qualquer processamento (nem environment criado) |
| `ApplicationEnvironmentPreparedEvent` | Environment conhecido, contexto ainda não criado |
| `ApplicationPreparedEvent` | Bean definitions carregadas, antes do refresh |
| `ApplicationStartedEvent` | Contexto refreshado, antes dos runners |
| `ApplicationReadyEvent` | Após `CommandLineRunner` / `ApplicationRunner`; **aplicação pronta para tráfego** |
| `ApplicationFailedEvent` | Exceção durante o startup |

`ApplicationReadyEvent` é o momento mais seguro para executar código de inicialização que depende de todo o contexto estar operacional (ex.: popular cache, checar integridade de dados).

> [!warning] Eventos precoces do Boot
> `ApplicationStartingEvent`, `ApplicationEnvironmentPreparedEvent` e `ApplicationContextInitializedEvent` disparam **antes** do `ApplicationContext` ser criado, então não podem ser registrados como `@Bean`. Use `SpringApplication.addListeners(...)` ou `META-INF/spring.factories` para esses casos.

## Na prática

Cenário: ao finalizar um pedido, o sistema deve enviar notificação sem atrasar a resposta HTTP.

**Evento:**

```java
public record OrderPlacedEvent(Long orderId, String customerEmail) {}
```

**Publicador (serviço de domínio):**

```java
@Service
@RequiredArgsConstructor
public class OrderService {

    private final OrderRepository repository;
    private final ApplicationEventPublisher publisher;

    @Transactional
    public Order placeOrder(CreateOrderRequest req) {
        Order order = repository.save(Order.from(req));
        publisher.publishEvent(new OrderPlacedEvent(order.getId(), req.email()));
        return order;
    }
}
```

**Ouvinte assíncrono:**

```java
@Component
@Slf4j
public class OrderNotificationListener {

    private final NotificationService notificationService;

    public OrderNotificationListener(NotificationService notificationService) {
        this.notificationService = notificationService;
    }

    @EventListener
    @Async
    public void onOrderPlaced(OrderPlacedEvent event) {
        log.info("Enviando notificação para orderId={}", event.orderId());
        notificationService.sendConfirmation(event.customerEmail());
    }
}
```

**Ouvinte de startup (ApplicationReadyEvent):**

```java
@Component
@Slf4j
public class CacheWarmupListener {

    @EventListener(ApplicationReadyEvent.class)
    public void warmUpCache() {
        log.info("Aquecendo cache de produtos...");
        // lógica de pré-carregamento
    }
}
```

> [!tip] Assista: Trabalhando com eventos de domínio em Spring Boot
> **Canal:** Felix Gilioli | **Duração:** ~20min | **Idioma:** PT-BR
>
> A seção acima afirma que eventos são síncronos por default. O vídeo **prova isso com um breakpoint**: ele para a execução dentro do listener e mostra o `save` do serviço parado, esperando. É a diferença entre saber a regra e ver a requisição travar por causa dela. Ele também mostra as duas formas de assinar — implementar `ApplicationListener<T>` ou anotar um método qualquer com `@EventListener` — e oferece uma rota que esta nota não cobre: em vez de anotar listener por listener com `@Async`, você sobrescreve o bean `applicationEventMulticaster` com um executor e torna **todos** os eventos assíncronos de uma vez.
> Trecho de destaque [14:34]: *"esse processo ele é síncrono, quando eu publico o evento aqui ele vai ficar esperando todos os outros processos terminarem"*
>
> 🎬 [Assistir no YouTube](https://www.youtube.com/watch?v=wnR_59CiOcc)

## Armadilhas

**1. Listener síncrono lento bloqueando o publisher**

O listener síncrono roda na mesma thread do publicador. Um listener que faz chamada HTTP, envia e-mail ou grava em disco pode atrasar toda a stack de chamada — incluindo a resposta HTTP ao usuário. Use `@Async` para operações potencialmente lentas.

**2. Assumir contexto transacional em listener `@Async`**

Quando o método do publicador roda dentro de uma `@Transactional`, o listener síncrono compartilha essa transação. Com `@Async`, a transação do publicador já pode ter feito commit (ou rollback) antes de o listener executar — ou o listener nem participa de nenhuma transação. Assumir que dados salvos estarão visíveis sem a devida configuração causa bugs sutis. Para vincular o disparo do evento ao resultado de uma transação, use `@TransactionalEventListener` (comportamento transacional detalhado no Galho 10 — Spring Data e Transações, planejado).

**3. Acoplamento excessivo via eventos**

Eventos facilitam desacoplamento, mas usados em excesso criam fluxos invisíveis difíceis de rastrear. Se o listener A dispara B que dispara C, o debugger raramente mostra a cadeia completa. Prefira eventos para **reações opcionais** a um fato de domínio (ex.: enviar e-mail após pedido); para fluxos obrigatórios e sequenciais, chamadas diretas (ou orquestração explícita) são mais rastreáveis.

**4. Registrar listener de evento precoce do Boot como `@Bean`**

Eventos como `ApplicationStartingEvent` disparam antes do contexto existir. Um listener registrado como `@Bean` simplesmente não estará pronto a tempo. O sintoma é silencioso: nenhum erro, o evento apenas não é recebido. Registre via `SpringApplication.addListeners()` ou `spring.factories`.

## Em entrevista

### Frase pronta (inglês)

> "Spring's event mechanism uses `ApplicationEventPublisher` to dispatch events in-process. Listeners are plain beans annotated with `@EventListener` — no interface needed. Delivery is synchronous by default, so the publisher blocks until all listeners complete; adding `@Async` moves the listener to a background thread but loses the publisher's transaction context."

> "Since Spring 4.2 you can publish any POJO as an event; you don't have to extend `ApplicationEvent`. Spring wraps it in a `PayloadApplicationEvent` internally."

> "In Spring Boot, `ApplicationReadyEvent` is the safest hook for post-startup initialization because it fires after all `CommandLineRunner`s have executed, guaranteeing the full context is operational."

### Vocabulário

| Termo PT | Termo EN |
|----------|----------|
| Publicador de eventos | Event publisher |
| Ouvinte / Escutador | Event listener |
| Entrega síncrona | Synchronous delivery |
| Entrega assíncrona | Asynchronous delivery |
| Evento de ciclo de vida | Lifecycle event |
| Acoplamento fraco | Loose coupling |
| Padrão observador | Observer pattern |
| Contexto pronto | Application ready |
| Encadeamento de eventos | Event chaining |
| Fila de despacho | Event multicaster / dispatch queue |

## Veja também

- [[03-Dominios/Tecnologia/Java/Jakarta EE/06 - CDI — qualifiers, producers e eventos|CDI — qualifiers, producers e eventos]] — os eventos do CDI (`@Observes` / `Event<T>`) são a versão da spec Jakarta do mesmo pub/sub in-process; o modelo conceitual é idêntico, a API é diferente.
- [[03-Dominios/Tecnologia/Java/Concorrência e paralelismo/index|Concorrência e paralelismo]] — `@Async` delega a execução a um `TaskExecutor`; compreender pools de threads e `CompletableFuture` ajuda a dimensionar e depurar listeners assíncronos (Galho 4).
- [[03-Dominios/Tecnologia/Java/Spring Core e Boot/index|Spring Core e Boot (MOC do galho)]]
- [[03-Dominios/Tecnologia/Java/index|Trilha Java]]
- [[03-Dominios/Tecnologia/Java/Dicionário de Java#@EventListener|@EventListener]] — verbete no dicionário da trilha.

## Referências

- [Spring Framework Docs — Standard and Custom Events](https://docs.spring.io/spring-framework/reference/core/beans/context-introduction.html#context-functionality-events)
- [Spring Boot Docs — Application Events and Listeners](https://docs.spring.io/spring-boot/reference/features/spring-application.html#features.spring-application.application-events-and-listeners)
