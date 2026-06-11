---
title: "Eventos in-process do Spring"
fase: adepto
tags:
  - java
  - mensageria
  - adepto
  - eventos
  - spring
type: concept
status: seedling
publish: true
created: 2026-06-11
updated: 2026-06-11
---

# Eventos in-process do Spring

> [!abstract] TL;DR
> O Spring possui um **event bus embutido no `ApplicationContext`** que permite comunicação desacoplada entre componentes **dentro do mesmo processo** — sem broker, sem rede, sem durabilidade entre serviços. É a ferramenta certa quando você quer separar responsabilidades num módulo ou numa aplicação monolítica; é a ferramenta errada quando precisa garantir entrega a outro serviço ou sobreviver a uma reinicialização. A grande alavanca arquitetural é o `@TransactionalEventListener(phase=AFTER_COMMIT)`: o listener só dispara se — e somente se — a transação que publicou o evento foi comitada com sucesso.

## O que é

O Spring oferece um mecanismo de publicação e escuta de eventos através do `ApplicationEventPublisher` e das anotações `@EventListener` / `@TransactionalEventListener`. Esse mecanismo está disponível em qualquer bean gerenciado pelo `ApplicationContext`, sem dependências externas.

> [!note] Mecanismo detalhado no Galho 8
> Esta nota foca no **ângulo arquitetural** — quando usar esse event bus e quais são suas garantias. O mecanismo em si (como publicar, como anotar listeners, eventos genéricos, `@Order`, condições SpEL) está documentado em [[03-Dominios/Java/Spring Core e Boot/11 - Eventos do ApplicationContext|Eventos do ApplicationContext]].

## Por que importa

Em entrevistas sênior, o ponto que separa respostas medianas de respostas fortes é saber **onde o event bus interno termina e o broker começa**. Os dois desacoplam componentes via eventos — mas as garantias são radicalmente diferentes.

Além disso, o `@TransactionalEventListener` resolve um problema clássico e traiçoeiro: você salva um pedido no banco e publica um evento para enviar um e-mail de confirmação. Se o commit falhar depois que o listener já disparou, o e-mail é enviado para uma ordem que não existe. O `AFTER_COMMIT` elimina essa classe de bug.

Saber escolher entre event bus in-process e broker (Kafka/RabbitMQ) — e saber articular o porquê — demonstra maturidade de design.

## Como funciona

### Síncrono por default vs `@Async`

Por padrão, `@EventListener` executa **na mesma thread** do publisher. Isso tem duas implicações diretas:

1. **Contexto de transação compartilhado**: o listener enxerga a mesma transação aberta pelo código que chamou `publishEvent(...)`. Uma exception no listener pode rolar back a transação inteira.
2. **Bloqueio**: o publisher espera todos os listeners terminarem antes de continuar.

Para tornar um listener assíncrono, combina-se `@EventListener` com `@Async` (requer `@EnableAsync` na configuração):

```java
@EventListener
@Async
public void handleOrderPlaced(OrderPlacedEvent event) {
    // executa em thread separada do executor configurado
    notificationService.sendConfirmationEmail(event.getCustomerEmail());
}
```

> [!warning] Exceções em listeners `@Async` não propagam para o caller
> Elas são tratadas pelo `AsyncUncaughtExceptionHandler`. Configure-o explicitamente ou exceções serão silenciadas. Listeners `@Async` também **não podem publicar eventos subsequentes retornando um valor** — use `ApplicationEventPublisher` injetado se precisar encadear eventos.

### `@TransactionalEventListener` — `AFTER_COMMIT`

`@TransactionalEventListener` amarra a execução do listener a uma **fase do ciclo de vida da transação**. O valor padrão do atributo `phase` é `TransactionPhase.AFTER_COMMIT`.

```java
@TransactionalEventListener(phase = TransactionPhase.AFTER_COMMIT)
public void onOrderPlaced(OrderPlacedEvent event) {
    // só chega aqui se a transação que publicou o evento comitou com sucesso
    notificationService.sendConfirmationEmail(event.getCustomerEmail());
}
```

Fases disponíveis:

| Fase | Quando dispara |
|------|---------------|
| `BEFORE_COMMIT` | Antes do commit (ainda dentro da transação) |
| `AFTER_COMMIT` | Após commit bem-sucedido (padrão) |
| `AFTER_ROLLBACK` | Após rollback |
| `AFTER_COMPLETION` | Após qualquer desfecho (commit ou rollback) |

**Comportamento sem transação ativa**: por padrão, se não houver transação em andamento quando o evento é publicado, o listener **não é invocado**. Para alterar isso:

```java
@TransactionalEventListener(fallbackExecution = true)
public void onOrderPlaced(OrderPlacedEvent event) {
    // dispara mesmo sem transação ativa
}
```

### In-process vs broker — quando cada um basta

| Dimensão | Event bus in-process | Broker (Kafka/RabbitMQ) |
|----------|---------------------|------------------------|
| Escopo | Mesmo processo JVM | Entre processos/serviços |
| Durabilidade | Nenhuma — evento some com o processo | Mensagens persistidas no broker |
| Entrega após reinício | Não | Sim (consumidores retomam offset) |
| Múltiplos consumidores entre serviços | Não | Sim |
| Latência | Submilissegundo | Milissegundos a dezenas de ms |
| Infraestrutura adicional | Nenhuma | Broker rodando |
| Garantias transacionais | `AFTER_COMMIT` garante coerência local | Exige exactly-once ou idempotência |

**Use o event bus in-process quando:**
- Você quer desacoplar módulos dentro de um monólito ou monólito modular.
- O listener e o publisher vivem no mesmo processo e reiniciam juntos.
- Você não precisa de entrega garantida entre serviços.
- Você quer acionar efeitos colaterais (e-mail, log, cache) apenas se a transação principal comitar.

**Prefira um broker quando:**
- Outro serviço precisa consumir o evento.
- A mensagem precisa sobreviver a falhas e reinicializações.
- Você precisa de backpressure, replay ou processamento paralelo em múltiplas instâncias.

## Na prática

Cenário: ao finalizar um pedido, publicar um `OrderPlacedEvent` e enviar e-mail de confirmação **somente se o pedido foi persistido com sucesso**.

```java
// Evento — POJO simples; não precisa estender ApplicationEvent no Spring moderno
public record OrderPlacedEvent(Long orderId, String customerEmail) {}
```

```java
// Serviço que persiste o pedido e publica o evento
@Service
@RequiredArgsConstructor
public class OrderService {

    private final OrderRepository orderRepository;
    private final ApplicationEventPublisher eventPublisher;

    @Transactional
    public Order placeOrder(OrderRequest request) {
        Order order = orderRepository.save(Order.from(request));
        // evento publicado dentro da transação; listener só dispara após AFTER_COMMIT
        eventPublisher.publishEvent(new OrderPlacedEvent(order.getId(), request.customerEmail()));
        return order;
    }
}
```

```java
// Listener transacional — dispara SOMENTE após o commit bem-sucedido
@Component
@RequiredArgsConstructor
public class OrderNotificationListener {

    private final NotificationService notificationService;

    @TransactionalEventListener(phase = TransactionPhase.AFTER_COMMIT)
    public void onOrderPlaced(OrderPlacedEvent event) {
        notificationService.sendConfirmationEmail(event.customerEmail());
    }
}
```

> [!tip] Por que `record` em vez de herdar `ApplicationEvent`?
> Desde o Spring 4.2, qualquer objeto pode ser publicado como evento — não é obrigatório estender `ApplicationEvent`. `record` é idiomático no Java moderno e mantém o evento como dado imutável.

## Armadilhas

### (1) `@EventListener` síncrono achando que é assíncrono

O equívoco mais comum: assumir que o listener roda "em background" ou depois da requisição. Sem `@Async`, ele roda **na mesma thread e dentro da mesma transação** do publisher. Isso significa:

- Uma exception no listener pode reverter a transação do caller.
- O tempo de execução do listener impacta diretamente a latência da operação principal.
- Não há isolamento: o listener enxerga dados não comitados da transação corrente.

### (2) Publicar evento e o commit falhar

Sem `@TransactionalEventListener`, o listener pode disparar antes do commit — ou pior, antes de um potencial rollback. O cenário clássico:

```
1. Salva pedido no banco       ← dentro de @Transactional
2. publishEvent(OrderPlacedEvent)
3. @EventListener dispara → envia e-mail ← JÁ ACONTECEU
4. Banco lança constraint violation
5. Transação faz rollback
6. Pedido não existe, mas e-mail foi enviado ← inconsistência
```

A correção é substituir `@EventListener` por `@TransactionalEventListener(phase=AFTER_COMMIT)`. O listener só executa se o step 4 não ocorrer.

### (3) Usar event bus interno esperando durabilidade ou entrega entre serviços

O `ApplicationEventPublisher` não tem fila, não tem persistência, não tem retry. Se a JVM morrer com um evento "a caminho", ele some. Se outro serviço precisa receber a notificação, o event bus in-process **não chega lá** — ele existe apenas dentro do processo que o publicou.

Sintomas de que você está usando a ferramenta errada:

- Você injeta `ApplicationEventPublisher` num `@Service` e quer que outro microsserviço reaja.
- Você espera que eventos sejam reprocessados após uma reinicialização.
- Você precisa de múltiplos consumidores independentes com offsets separados.

Nesses casos, use Kafka ou RabbitMQ com as garantias de entrega adequadas.

## Em entrevista

> "The Spring `ApplicationContext` ships with a built-in, **in-process event bus** powered by `ApplicationEventPublisher` and `@EventListener`. It's great for decoupling modules inside a monolith — for example, triggering a notification after an order is saved — but it has **no durability**: events live only in the current JVM process. The key architectural tool is `@TransactionalEventListener(phase=AFTER_COMMIT)`, which guarantees the listener fires **only after the publishing transaction commits successfully**, eliminating the classic dual-write bug where a side effect runs before a potential rollback. When I need cross-service delivery, replay after restart, or backpressure across multiple consumers, I switch to a **message broker** like Kafka or RabbitMQ, because those guarantees simply don't exist in the in-process bus."

Vocabulário para soltar com naturalidade: **in-process event bus**, **ApplicationEventPublisher**, **transactional event listener**, **AFTER_COMMIT phase**, **same-thread execution**, **fallbackExecution**, **dual-write bug**, **durability**, **broker vs in-process**.

## Veja também

- [[03-Dominios/Java/Mensageria/Mensageria|MOC — Mensageria (Galho 14)]]
- [[03-Dominios/Java/Java|Trilha Java Senior]]
- [[03-Dominios/Java/Spring Core e Boot/11 - Eventos do ApplicationContext|Eventos do ApplicationContext]] (Galho 8 — o mecanismo: `@EventListener`, `ApplicationEvent`, ordenação, eventos genéricos)
- [[03-Dominios/Java/Mensageria/01 - O que é mensageria e arquitetura orientada a eventos|O que é mensageria]]
- [[03-Dominios/Java/Dicionário de Java|Dicionário de Java]]

## Referências

- Spring Framework Reference — Standard and Custom Events (`@EventListener`, `@Async`, `ApplicationEventPublisher`): https://docs.spring.io/spring-framework/reference/core/beans/context-introduction.html
- Spring Framework Reference — Transaction-bound Events (`@TransactionalEventListener`, fases, `fallbackExecution`): https://docs.spring.io/spring-framework/reference/data-access/transaction/event.html
