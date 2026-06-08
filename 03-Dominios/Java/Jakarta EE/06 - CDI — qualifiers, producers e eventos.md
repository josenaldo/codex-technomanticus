---
title: "CDI — qualifiers, producers e eventos"
created: 2026-06-07
updated: 2026-06-08
type: concept
progress: backlog
status: seedling
publish: true
fase: adepto
tags:
  - java
  - jakarta-ee
  - adepto
  - cdi
aliases:
  - "Qualifiers CDI"
  - "@Produces"
  - "Eventos CDI"
---

# CDI — qualifiers, producers e eventos

> [!abstract] TL;DR
> **Qualifiers** desambiguam: quando você tem dois beans que implementam o mesmo tipo (`PaymentGateway`), o container precisa de uma pista extra — e é para isso que servem. **Producers** fabricam o que o container não sabe criar sozinho: objetos de bibliotecas de terceiros, valores de configuração, qualquer coisa que precise de lógica de construção personalizada. **Eventos** desacoplam quem emite de quem ouve: o emissor não sabe nada sobre os ouvintes — é o pub/sub embutido no próprio container. Juntos, os três mecanismos resolvem a maioria dos casos em que a injeção simples por tipo não é suficiente.

## O que é

Nas notas [[04 - CDI — beans e injeção]] e [[05 - CDI — escopos e contextos]] você viu o coração do CDI: o container descobre beans pelo tipo e gerencia o ciclo de vida por escopo. Esta nota cobre os **três mecanismos de flexibilidade** que o CDI oferece quando a resolução pura por tipo não basta:

**Qualifiers** são anotações que funcionam como rótulos adicionais sobre um bean. O container usa esses rótulos para desempatar quando há mais de uma implementação do mesmo tipo no classpath. Em vez de identificar beans por string (como `"pix"` ou `"creditcard"`), você usa tipos — e o compilador verifica por você.

**Producers** são métodos ou campos anotados com `@Produces` que ensinam o container a criar objetos que ele não saberia instanciar por conta própria. Qualquer objeto pode ser produzido e gerenciado pelo container: um `DataSource` configurado, um `Logger` por classe, um objeto de config lido de um arquivo externo.

**Eventos** implementam o padrão observer diretamente na spec. Um bean dispara um evento via `Event<T>.fire()` sem saber quem vai receber. Outros beans declaram `@Observes` em métodos de escuta. O container coordena a entrega — de forma síncrona ou assíncrona.

## Por que importa

Todo sistema real chega a um ponto em que há **duas ou mais implementações do mesmo contrato**: gateway de pagamento por Pix e por cartão de crédito, repositório em memória (testes) e em banco (produção), serviço de e-mail real e fake. Sem qualifiers, o container lança `AmbiguousResolutionException`. Com qualifiers tipados, a escolha é feita em tempo de compilação, sem uma linha de XML de configuração.

**Integrar bibliotecas de terceiros** é o dia-a-dia do desenvolvimento — e é exatamente onde producers brilham. O container só sabe gerenciar beans cujo ciclo de vida ele controla. Quando você precisa injetar um `ObjectMapper` do Jackson ou um `EntityManager` do JPA, você escreve um producer: um método que cria o objeto, e um disposer que faz o cleanup. A partir daí, o objeto de terceiro se comporta como qualquer bean CDI.

O **padrão de eventos** é a versão da spec de um pub/sub embutido — o mesmo papel que bibliotecas dedicadas (como o Guava EventBus) e frameworks de aplicação (veja [[03-Dominios/Java/Spring Core e Boot/11 - Eventos do ApplicationContext|eventos do Spring]]) cumprem. A vantagem é que você não precisa de nenhuma dependência extra: funciona em qualquer runtime Jakarta EE ou MicroProfile.

> [!warning] Dois `@Produces` completamente diferentes
> O `@Produces` do CDI (`jakarta.enterprise.inject.Produces`) e o `@Produces` do JAX-RS (`jakarta.ws.rs.Produces`) são **homônimos sem nenhuma relação**. O primeiro declara um bean producer para o container de injeção. O segundo declara o media type que um endpoint REST produz. Sempre confira o import. A nota [[07 - JAX-RS — REST declarativo]] cobre o `@Produces` do JAX-RS em detalhe.

## Como funciona

### Qualifiers

**Definindo um qualifier custom**

Um qualifier é uma anotação Java anotada com `@jakarta.inject.Qualifier`. A spec CDI 4.1 exige `@Retention(RUNTIME)` e recomenda `@Target({METHOD, FIELD, PARAMETER, TYPE})`:

```java
import jakarta.inject.Qualifier;
import java.lang.annotation.Retention;
import java.lang.annotation.RetentionPolicy;
import java.lang.annotation.Target;
import java.lang.annotation.ElementType;

@Qualifier
@Retention(RetentionPolicy.RUNTIME)
@Target({ElementType.METHOD, ElementType.FIELD,
         ElementType.PARAMETER, ElementType.TYPE})
public @interface Pix {}
```

Você coloca o qualifier tanto na implementação quanto no ponto de injeção:

```java
@Pix
@ApplicationScoped
public class PixGateway implements PaymentGateway { ... }

@Inject @Pix
private PaymentGateway gateway; // o container entrega PixGateway
```

**Qualifiers built-in: `@Default` e `@Any`**

Dois qualifiers são implícitos em todo bean. `@Default` é aplicado automaticamente quando um bean não declara nenhum outro qualifier (além de `@Named` ou `@Any`). `@Any` está presente em **todo** bean, sem exceção — é usado para seleção programática via `Instance<T>`.

**Por que `@Named` não é para injeção típica**

`@Named` (`jakarta.inject.Named`) é um qualifier built-in que atribui um nome string ao bean. Seu uso correto é exposição para **Jakarta Unified Expression Language** (EL) — em páginas JSF, por exemplo. Para injeção entre beans Java, prefira sempre qualifiers tipados: um typo em uma string não é detectado pelo compilador, mas um import errado é.

### Producers

**`@Produces` em método**

Um producer method é qualquer método anotado com `@jakarta.enterprise.inject.Produces` numa classe gerenciada pelo CDI. O tipo de retorno torna-se um bean type disponível para injeção:

```java
@ApplicationScoped
public class AppProducers {

    @Produces
    @ApplicationScoped
    public ObjectMapper objectMapper() {
        return new ObjectMapper()
            .findAndRegisterModules()
            .disable(SerializationFeature.WRITE_DATES_AS_TIMESTAMPS);
    }
}
```

A partir desse producer, qualquer bean pode receber `@Inject ObjectMapper mapper` normalmente.

**`@Produces` em campo**

Para objetos mais simples, um campo anotado faz o mesmo trabalho sem precisar de método:

```java
@Produces
@RequestScoped
private final RequestContext requestContext = new RequestContext();
```

**Escopo do producer**

O producer **não herda o escopo da classe que o declara**. Cada producer tem seu próprio escopo — o default é `@Dependent` caso nenhum escopo seja declarado explicitamente. Isso significa que a classe pode ser `@ApplicationScoped` e o producer ser `@RequestScoped`: são dois beans distintos do ponto de vista do container.

**`@Disposes` — o par obrigatório para recursos**

Quando um producer cria um recurso que precisa de cleanup (conexão, stream, cliente HTTP), um método disposer completa o ciclo:

```java
@Produces
@RequestScoped
public EntityManager createEntityManager(EntityManagerFactory emf) {
    return emf.createEntityManager();
}

public void closeEntityManager(
        @Disposes EntityManager em) {
    if (em.isOpen()) em.close();
}
```

O container chama o disposer automaticamente quando o contexto do bean produzido termina. O parâmetro anotado com `@Disposes` deve ter o mesmo tipo (e os mesmos qualifiers) do producer correspondente.

### Eventos síncronos

**Disparando e observando**

O ponto de disparo injeta `Event<T>` e chama `fire()`:

```java
@Inject
private Event<OrderPlaced> orderEvent;

public void placeOrder(Order order) {
    processOrder(order);
    orderEvent.fire(new OrderPlaced(order.id()));
}
```

O container chama todos os observer methods registrados para o tipo `OrderPlaced` de forma **síncrona e sequencial**, na mesma thread. Se algum observer lançar exceção, o `fire()` propaga.

Um observer method declara `@Observes` no parâmetro do evento:

```java
@ApplicationScoped
public class EmailNotifier {

    public void onOrderPlaced(@Observes OrderPlaced event) {
        sendEmail(event.orderId());
    }
}
```

**Ordenação com `@Priority`**

Quando há múltiplos observers do mesmo tipo, `@Priority` (do pacote `jakarta.annotation`) controla a ordem: menor valor é executado primeiro.

```java
public void onOrderPlaced(
        @Observes @Priority(100) OrderPlaced event) { ... }
```

**Transactional observers — menção**

Observers podem declarar em qual fase de uma transação querem ser notificados (`IN_PROGRESS`, `BEFORE_COMPLETION`, `AFTER_SUCCESS`, `AFTER_FAILURE`, `AFTER_COMPLETION`). Isso garante, por exemplo, que o envio de e-mail só aconteça após o commit com sucesso — evitando enviar notificação de uma operação que vai ser revertida.

### Eventos assíncronos

**`fireAsync` e `@ObservesAsync`**

Para não bloquear o caller durante a entrega do evento, use `fireAsync()`. O método retorna um `CompletionStage<T>` imediatamente; o container notifica os observers assíncronos em uma ou mais threads separadas:

```java
orderEvent.fireAsync(new OrderPlaced(order.id()))
    .exceptionally(e -> {
        log.error("Async observer falhou", e);
        return null;
    });
```

Do lado do observer, troque `@Observes` por `@ObservesAsync`:

```java
public void auditAsync(@ObservesAsync OrderPlaced event) {
    auditLog.record(event.orderId());
}
```

> [!info] Threading e context propagation
> Observers assíncronos rodam fora do contexto da requisição original. Para processamento concorrente mais elaborado — pools, virtual threads, `CompletableFuture` — veja [[03-Dominios/Java/Concorrência e paralelismo/index|Concorrência (Galho 4)]]; esta nota não re-explica o modelo de threading.

### `@Alternative` e `Instance<T>`

**Trocando implementação por configuração**

`@Alternative` marca um bean como substituto opcional de outro. Por padrão, alternatives ficam desabilitados. Há duas formas de ativar:

- **beans.xml** (escopo de bean archive): lista a classe na seção `<alternatives>`.
- **`@Priority`** (escopo de aplicação, CDI 1.1+): coloque `@Priority(valor)` junto com `@Alternative` na classe — o container ativa o alternative para toda a aplicação, sem XML.

```java
@Alternative
@Priority(100)           // ativa para toda a aplicação
@ApplicationScoped
public class FakePaymentGateway implements PaymentGateway { ... }
```

**`Instance<T>` — resolução programática e lazy**

Quando a escolha do bean precisa acontecer em tempo de execução (estratégia dinâmica, multi-tenant), `Instance<T>` permite lookup programático:

```java
@Inject @Any
private Instance<PaymentGateway> gateways;

public PaymentGateway resolve(PaymentMethod method) {
    Annotation qualifier = method == PIX
        ? new PixLiteral()
        : new CreditCardLiteral();
    Instance<PaymentGateway> selected = gateways.select(qualifier);
    if (selected.isResolvable()) {
        return selected.get();
    }
    throw new IllegalArgumentException("Gateway não encontrado: " + method);
}
```

Use `@Any` no ponto de injeção para obter todos os beans do tipo e depois filtrar com `select(qualifier)`. Beans obtidos via `get()` devem ser destruídos com `destroy()` quando não forem mais necessários (especialmente beans `@Dependent`).

## Na prática

```java
// ── 1. Qualifiers custom ────────────────────────────────────────────────────

import jakarta.inject.Qualifier;
import java.lang.annotation.*;

@Qualifier
@Retention(RetentionPolicy.RUNTIME)
@Target({ElementType.METHOD, ElementType.FIELD,
         ElementType.PARAMETER, ElementType.TYPE})
public @interface Pix {}

@Qualifier
@Retention(RetentionPolicy.RUNTIME)
@Target({ElementType.METHOD, ElementType.FIELD,
         ElementType.PARAMETER, ElementType.TYPE})
public @interface CreditCard {}

// ── 2. Contrato e implementações ────────────────────────────────────────────

public interface PaymentGateway {
    void charge(Order order);
}

@Pix
@ApplicationScoped
public class PixGateway implements PaymentGateway {
    @Override
    public void charge(Order order) {
        // lógica Pix
    }
}

@CreditCard
@ApplicationScoped
public class CreditCardGateway implements PaymentGateway {
    @Override
    public void charge(Order order) {
        // lógica cartão
    }
}

// ── 3. Injeção com qualifier ─────────────────────────────────────────────────

@ApplicationScoped
public class CheckoutService {

    @Inject @Pix
    private PaymentGateway pixGateway;

    @Inject @CreditCard
    private PaymentGateway creditCardGateway;

    public void checkout(Order order, PaymentMethod method) {
        PaymentGateway gateway = method == PIX ? pixGateway : creditCardGateway;
        gateway.charge(order);
        orderEvent.fire(new OrderPlaced(order.id()));
    }

    @Inject
    private Event<OrderPlaced> orderEvent;
}

// ── 4. Producer de objeto de terceiro com disposer ───────────────────────────

import jakarta.enterprise.context.ApplicationScoped;
import jakarta.enterprise.inject.Produces;
import jakarta.enterprise.inject.Disposes;
import com.fasterxml.jackson.databind.ObjectMapper;
import com.fasterxml.jackson.databind.SerializationFeature;

@ApplicationScoped
public class InfraProducers {

    @Produces
    @ApplicationScoped
    public ObjectMapper objectMapper() {
        return new ObjectMapper()
            .findAndRegisterModules()
            .disable(SerializationFeature.WRITE_DATES_AS_TIMESTAMPS);
    }

    // ObjectMapper não precisa de close, mas o padrão é idêntico para recursos
    public void disposeObjectMapper(@Disposes ObjectMapper mapper) {
        // cleanup se necessário
    }
}

// ── 5. Evento com observers síncrono e assíncrono ───────────────────────────

// Evento (POJO simples — record é ideal)
public record OrderPlaced(String orderId) {}

// Observer síncrono — roda na mesma thread do fire()
import jakarta.enterprise.context.ApplicationScoped;
import jakarta.enterprise.event.Observes;
import jakarta.annotation.Priority;

@ApplicationScoped
public class EmailNotifier {

    public void onOrderPlaced(
            @Observes @Priority(10) OrderPlaced event) {
        sendEmail(event.orderId());
    }

    private void sendEmail(String orderId) { /* ... */ }
}

// Observer assíncrono — roda em thread separada
import jakarta.enterprise.event.ObservesAsync;

@ApplicationScoped
public class AuditLogger {

    public void onOrderPlaced(@ObservesAsync OrderPlaced event) {
        writeAuditLog(event.orderId());
    }

    private void writeAuditLog(String orderId) { /* ... */ }
}
```

## Armadilhas

### (1) Usar `@Named("x")` como qualifier de injeção

`@Named` recebe uma string — e strings não são verificadas pelo compilador. Um typo no nome passa pela build, falha em runtime, e a mensagem de erro do container pode ser confusa.

```java
// ❌ frágil: "pix" pode virar "Pix" ou "PIX" sem aviso do compilador
@Inject @Named("pix")
private PaymentGateway gateway;

// ✅ tipado: o compilador detecta o import errado imediatamente
@Inject @Pix
private PaymentGateway gateway;
```

`@Named` deve ser reservado para exposição de beans na Expression Language (EL) de páginas JSF — não para injeção entre beans Java.

### (2) Producer de recurso caro sem `@Disposes`

Um producer que abre conexão, arquivo ou cliente HTTP sem um disposer correspondente causa **vazamento de recurso** garantido. O container não tem como fazer cleanup se você não ensinar a ele como.

```java
// ❌ leak: EntityManager nunca é fechado
@Produces
@RequestScoped
public EntityManager leakyEntityManager(EntityManagerFactory emf) {
    return emf.createEntityManager();
}

// ✅ par produce/dispose: o container chama closeEntityManager ao fim do contexto
@Produces
@RequestScoped
public EntityManager createEntityManager(EntityManagerFactory emf) {
    return emf.createEntityManager();
}

public void closeEntityManager(@Disposes EntityManager em) {
    if (em.isOpen()) em.close();
}
```

O parâmetro anotado com `@Disposes` deve ter o mesmo tipo e qualifiers do producer.

### (3) Observer síncrono lento bloqueando o `fire()`

`Event.fire()` é síncrono e bloqueia até todos os observers terminarem. Um observer que envia e-mail, chama API externa ou grava log pesado segura a thread da requisição inteira — degradando latência para o usuário.

```java
// ❌ bloqueia a requisição: envio de e-mail pode levar segundos
public void onOrderPlaced(@Observes OrderPlaced event) {
    emailClient.sendConfirmation(event.orderId()); // chamada HTTP síncrona
}

// ✅ use @ObservesAsync para trabalho I/O-bound fora da thread da requisição
public void onOrderPlaced(@ObservesAsync OrderPlaced event) {
    emailClient.sendConfirmation(event.orderId());
}
```

Se o observer precisa ser síncrono por razões de negócio (ex.: validação), mantenha-o rápido e delegue o I/O para um executor assíncrono interno.

### (4) Confundir os dois `@Produces`

Existem dois `@Produces` completamente distintos no universo Jakarta EE. Importar o errado não gera erro de compilação imediato, mas o runtime vai se comportar de forma inesperada:

```java
// ❌ import errado: este é o @Produces do JAX-RS (media type)
import jakarta.ws.rs.Produces;

@Produces("application/json")  // anota o endpoint REST, não cria bean
public ObjectMapper objectMapper() { ... }

// ✅ import correto: este é o @Produces do CDI (producer method)
import jakarta.enterprise.inject.Produces;

@Produces
@ApplicationScoped
public ObjectMapper objectMapper() { ... }
```

Sempre confira o import ao usar `@Produces`. A nota [[07 - JAX-RS — REST declarativo]] explica o `@Produces` do JAX-RS.

## Em entrevista

### Frase pronta (inglês)

"CDI qualifiers solve the ambiguous dependency problem by letting you attach type-safe annotations to both the bean and the injection point — so the container can pick the right implementation at build time rather than relying on brittle string names. Producer methods bridge the gap between CDI-managed beans and third-party objects: you teach the container how to create and destroy the resource, and from that point it behaves like any other bean. The CDI event bus decouples producers from consumers entirely — the firing bean has zero knowledge of its observers, which makes it straightforward to add cross-cutting concerns like auditing or notifications without touching existing code."

### Vocabulário

| Termo PT | Termo EN |
|---|---|
| qualifier (CDI) | qualifier |
| qualifier custom | custom qualifier |
| método producer | producer method |
| campo producer | producer field |
| método disposer | disposer method |
| evento (CDI) | CDI event |
| observer síncrono | synchronous observer |
| observer assíncrono | asynchronous observer |
| resolução programática | programmatic lookup |
| desambiguação de beans | bean disambiguation |

## Veja também

- [[04 - CDI — beans e injeção]]
- [[05 - CDI — escopos e contextos]]
- [[07 - JAX-RS — REST declarativo]]
- [[13 - CDI avançado — interceptors, decorators e extensões]]
- [[03-Dominios/Java/Jakarta EE/index|Jakarta EE (MOC do galho)]]
- [[03-Dominios/Java/index|Trilha Java]]
- [[03-Dominios/Java/Dicionário de Java#qualifier (CDI)|qualifier (Dicionário)]]
- [[03-Dominios/Java/Dicionário de Java#@Produces (producer CDI)|@Produces (Dicionário)]]
- [[03-Dominios/Java/Dicionário de Java#@Observes / eventos CDI|@Observes (Dicionário)]]

## Referências

- Jakarta CDI 4.1 Specification. Disponível em: <https://jakarta.ee/specifications/cdi/4.1/jakarta-cdi-spec-4.1>. Acesso em: 2026-06-07.
- Jakarta CDI 4.1 — Release page. Disponível em: <https://jakarta.ee/specifications/cdi/4.1/>. Acesso em: 2026-06-07.
- Weld Reference Guide — Events. Disponível em: <https://docs.jboss.org/weld/reference/latest/en-US/html/events.html>. Acesso em: 2026-06-07.
- Weld Reference Guide — Producer Methods. Disponível em: <https://docs.jboss.org/weld/reference/latest/en-US/html/producermethods.html>. Acesso em: 2026-06-07.
- Weld Reference Guide — Injection. Disponível em: <https://docs.jboss.org/weld/reference/latest/en-US/html/injection.html>. Acesso em: 2026-06-07.
