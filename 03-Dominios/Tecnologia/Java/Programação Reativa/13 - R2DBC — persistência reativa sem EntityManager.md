---
title: "R2DBC — persistência reativa sem EntityManager"
created: 2026-06-10
updated: 2026-06-10
type: concept
progress: backlog
status: seedling
publish: true
fase: Magus
tags:
  - java
  - reativa
  - magus
  - r2dbc
aliases:
  - "R2DBC"
  - "persistência reativa"
---

# R2DBC — persistência reativa sem EntityManager

> [!abstract] TL;DR
> **R2DBC** (Reactive Relational Database Connectivity) é o acesso **reativo, não-bloqueante** a bancos relacionais: o driver fala com o banco sem segurar a thread esperando o I/O. Em cima dele, o Spring Data R2DBC oferece `R2dbcRepository` e `DatabaseClient`, cujos métodos devolvem `Mono`/`Flux` em vez de objetos prontos. O preço: **não há `EntityManager`, persistence context (cache de 1º nível), dirty checking nem lazy loading**. Relacionamentos não vêm de `@OneToMany`/`@ManyToOne` — você os resolve **à mão**, encadeando consultas com `flatMap`. É o contraponto da JPA do Galho 10: ganhar não-bloqueio custa o ORM inteiro.

## O que é

R2DBC é uma **especificação (SPI) de driver** para falar com bancos relacionais de forma reativa. O análogo bloqueante é o JDBC: onde o JDBC expõe `Connection`/`Statement`/`ResultSet` com chamadas síncronas que **bloqueiam a thread** até o banco responder, o R2DBC expõe `Connection`/`Statement`/`Result`/`Row` cujas operações devolvem **`Publisher`** (Reactive Streams) — nada bloqueia, tudo é assinado e entregue de forma assíncrona.

Em cima da SPI vive o **Spring Data R2DBC**, que dá o sabor familiar de Spring Data: repositórios (`R2dbcRepository`), query methods derivados, mapeamento objeto-linha e um `DatabaseClient`/`R2dbcEntityTemplate` para SQL fluente. Mas — e este é o ponto da nota — **Spring Data R2DBC não é um ORM**. Ele mapeia uma linha para um objeto e pronto; não rastreia entidades, não mantém um contexto de persistência, não materializa grafos de objetos.

## Por que importa

Numa pilha reativa (WebFlux sobre Netty, ver [[03-Dominios/Tecnologia/Java/Programação Reativa/10 - Spring WebFlux — o stack não-bloqueante sobre Netty e o DispatcherHandler|Spring WebFlux]]), **o caminho inteiro precisa ser não-bloqueante**. Um único acesso JDBC bloqueante no meio de um handler reativo segura uma thread do event loop e mata a vazão — exatamente o problema que o WebFlux existe para evitar. R2DBC é a peça que faltava: a camada de dados reativa que fecha o circuito.

O custo é conceitual, não só de API. Quem vem da JPA chega esperando o conforto do persistence context — dirty checking automático, lazy loading de relações, cache de 1º nível — e **nada disso existe**. Em entrevista, o sinal de senioridade é saber **qual conforto você está abrindo mão** e por quê, em vez de tratar R2DBC como "JPA que devolve `Flux`".

## Como funciona

### R2DBC: o driver reativo (não-bloqueante) vs JDBC (bloqueante)

O JDBC é uma API **bloqueante por design**: `statement.executeQuery()` só retorna quando o banco terminou, e a thread chamadora fica parada nesse meio-tempo. Isso casa com o modelo thread-por-requisição do servlet, mas é veneno num event loop.

O R2DBC redesenha a SPI em torno de `Publisher`: `connection.createStatement(sql)`, `statement.execute()` e `result.map(...)` devolvem fluxos reativos. A thread dispara o I/O e **é liberada**; quando o banco responde, o resultado é empurrado pelo `Publisher`. Os drivers existem por banco — PostgreSQL, MySQL, MariaDB, SQL Server, Oracle, H2, entre outros (a especificação está em `1.0.0.RELEASE`). Não há driver R2DBC genérico: cada banco precisa do seu.

### `R2dbcRepository` e `DatabaseClient`: o acesso reativo

O Spring Data R2DBC oferece duas portas de entrada:

- **`R2dbcRepository<T, ID>`** (`org.springframework.data.r2dbc.repository.R2dbcRepository`) — a interface de repositório. `findById` devolve `Mono<T>`, `findAll` devolve `Flux<T>`, `save` devolve `Mono<T>`. Query methods derivados (`findByStatus`) funcionam, devolvendo `Mono`/`Flux`.
- **`DatabaseClient`** (`org.springframework.r2dbc.core.DatabaseClient`) — API fluente de SQL para quando você quer controle total: `sql("...").bind(...).map(...).all()`/`.one()`. Há ainda o `R2dbcEntityTemplate`, que combina mapeamento de entidade com a fluência do client.

Os tipos de retorno são sempre reativos — você compõe com `map`/`flatMap` (ver [[03-Dominios/Tecnologia/Java/Programação Reativa/05 - map e flatMap — transformando o fluxo|map e flatMap]]) e **nada toca o banco até o `subscribe`**.

### O que NÃO existe: sem `EntityManager`, sem persistence context, sem dirty checking, sem lazy loading

Aqui mora o contraste. Na JPA (Galho 10), o [[03-Dominios/Tecnologia/Java/Persistência de dados/03 - O persistence context e os estados da entidade|persistence context]] é o coração: ele rastreia cada entidade gerenciada, faz **dirty checking** (detecta mudanças e sincroniza no flush), serve de **cache de 1º nível** (mesma `@Id` → mesma instância na transação) e habilita o **lazy loading**.

No R2DBC, **não há `EntityManager`**. Logo:

- **Sem persistence context / cache de 1º nível** — buscar a mesma linha duas vezes faz duas idas ao banco; não há garantia de identidade de instância.
- **Sem dirty checking** — mudar um campo de um objeto carregado **não persiste nada**. Você precisa chamar `save` explicitamente.
- **Sem lazy loading** — não existe proxy que dispara uma query ao acessar uma relação. A relação simplesmente não está lá (ver o contraste em [[03-Dominios/Tecnologia/Java/Persistência de dados/07 - Fetch strategies — LAZY, EAGER e a LazyInitializationException|Fetch strategies]]).

### Relacionamentos resolvidos manualmente (`flatMap`), não com `@OneToMany`

A JPA materializa grafos: um `@ManyToOne` LAZY te dá `order.getCustomer()` que dispara a query sob demanda. No R2DBC **não há mapeamento de relação**. Uma entidade `Order` guarda no máximo a **chave estrangeira** (`customerId`), não um objeto `Customer`.

Para "navegar" a relação, você compõe consultas explicitamente: carrega o `Order`, e com `flatMap` carrega o `Customer` correspondente pela FK. O grafo vira **composição reativa**, não mágica do ORM. É mais código, mas é explícito — você vê exatamente quantas queries acontecem (sem surpresa de N+1 escondido por um proxy).

### Transações reativas (`TransactionalOperator` / `@Transactional` reativo)

Transação numa pilha reativa não pode pendurar o estado em um `ThreadLocal` — a execução salta de thread em thread. O contexto transacional viaja no **Reactor Context**, e há dois jeitos de demarcar:

- **`@Transactional`** sobre um método que devolve `Mono`/`Flux` — o Spring detecta o tipo reativo e gerencia a transação ao longo da cadeia, com commit no sucesso e rollback no `onError`.
- **`TransactionalOperator`** (`org.springframework.transaction.reactive.TransactionalOperator`) — demarcação programática: `operator.transactional(meuFluxo)` envolve a cadeia reativa numa transação.

A propagação e os trade-offs conceituais se parecem com os da JPA (ver [[03-Dominios/Tecnologia/Java/Persistência de dados/12 - Transações operacionais — @Transactional propagação, isolamento, rollback, readOnly|Transações operacionais]]), mas a fronteira é o **fluxo reativo**, não a thread.

## Na prática

Schema e entidade. Note que `Order` guarda `customerId` (a FK), **não** um objeto `Customer`.

```sql
CREATE TABLE customer (
    id      BIGINT GENERATED BY DEFAULT AS IDENTITY PRIMARY KEY,
    name    VARCHAR(120) NOT NULL
);

CREATE TABLE orders (
    id          BIGINT GENERATED BY DEFAULT AS IDENTITY PRIMARY KEY,
    customer_id BIGINT NOT NULL REFERENCES customer(id),
    status      VARCHAR(20) NOT NULL,
    total       NUMERIC(12,2) NOT NULL
);
```

```java
import org.springframework.data.annotation.Id;
import org.springframework.data.relational.core.mapping.Table;

@Table("orders")
public class Order {
    @Id
    private Long id;
    private Long customerId;   // a FK, não um Customer — sem @ManyToOne
    private String status;
    private BigDecimal total;
    // getters/setters
}

@Table("customer")
public class Customer {
    @Id
    private Long id;
    private String name;
    // getters/setters
}
```

Repositórios reativos. Os retornos são `Mono`/`Flux`, nunca o objeto cru:

```java
import org.springframework.data.r2dbc.repository.R2dbcRepository;
import reactor.core.publisher.Flux;
import reactor.core.publisher.Mono;

public interface OrderRepository extends R2dbcRepository<Order, Long> {
    Flux<Order> findByStatus(String status);   // query method derivado, reativo
}

public interface CustomerRepository extends R2dbcRepository<Customer, Long> {
}
```

Resolvendo a relação **à mão** com `flatMap` (o que na JPA seria `order.getCustomer()` por trás de um `@ManyToOne` LAZY):

```java
import reactor.core.publisher.Flux;
import reactor.core.publisher.Mono;

public class OrderService {

    private final OrderRepository orders;
    private final CustomerRepository customers;

    public OrderService(OrderRepository orders, CustomerRepository customers) {
        this.orders = orders;
        this.customers = customers;
    }

    // Carrega o Order e, em seguida, o Customer pela FK — composição explícita.
    public Mono<OrderView> findOrderWithCustomer(Long orderId) {
        return orders.findById(orderId)
            .flatMap(order ->
                customers.findById(order.getCustomerId())
                    .map(customer -> new OrderView(order, customer)));
    }

    public Flux<Order> pendingOrders() {
        return orders.findByStatus("PENDING");
    }
}
```

SQL fluente direto, via `DatabaseClient`, quando o query method não basta:

```java
import org.springframework.r2dbc.core.DatabaseClient;
import reactor.core.publisher.Flux;

public class ProductDao {

    private final DatabaseClient client;

    public ProductDao(DatabaseClient client) {
        this.client = client;
    }

    public Flux<String> productNamesAbove(BigDecimal price) {
        return client.sql("SELECT name FROM product WHERE price > :price")
            .bind("price", price)
            .map((row, meta) -> row.get("name", String.class))
            .all();
    }
}
```

> [!warning] Nunca bloqueie o event loop
> Em todo o caminho acima, **não** chame `.block()` nem misture I/O bloqueante. Numa pilha WebFlux, bloquear uma thread do event loop trava todas as requisições que a compartilham. O ponto de usar R2DBC é justamente manter o caminho reativo de ponta a ponta.

## Armadilhas

### (1) Esperar lazy loading da JPA — ele não existe no R2DBC

Quem vem da JPA carrega um `Order` e chama `order.getCustomer()` esperando o proxy disparar a query. No R2DBC **não há proxy nem relação mapeada** — `Order` nem tem um campo `Customer`, só `customerId`. O acesso simplesmente não existe (ou devolve `null`).

```java
// ❌ Mentalidade JPA: não há getCustomer() — Order só tem a FK
Order order = orders.findById(1L).block();
Customer c = order.getCustomer();   // não compila / não existe
```

**Fix:** resolva a relação compondo consultas com `flatMap`, carregando o `Customer` pela FK — como no `findOrderWithCustomer` acima. O grafo é construído por você, explicitamente, não materializado pelo ORM.

### (2) Misturar JDBC bloqueante "junto" do R2DBC

Tentar reaproveitar um `JdbcTemplate`/repositório JPA "só nessa parte" dentro de um fluxo reativo mata o ganho inteiro: a chamada bloqueante segura uma thread do event loop, e a vazão despenca para a de uma pilha bloqueante (ou pior).

```java
// ❌ chamada JDBC bloqueante no meio de um fluxo reativo
return orders.findById(id)
    .map(order -> jdbcTemplate.queryForObject(   // BLOQUEIA o event loop
        "SELECT name FROM customer WHERE id = ?",
        String.class, order.getCustomerId()));
```

**Fix:** **todo** o caminho precisa ser não-bloqueante. Use o repositório/`DatabaseClient` reativo. Se for absolutamente inevitável encostar em algo bloqueante (uma lib legada), isole-o em um `Scheduler` dedicado com `subscribeOn(Schedulers.boundedElastic())` (ver [[03-Dominios/Tecnologia/Java/Programação Reativa/08 - Schedulers — subscribeOn, publishOn e em qual thread o código roda|Schedulers]]) — nunca direto no event loop.

### (3) Achar que R2DBC é "JPA reativo"

R2DBC **não é um ORM**. Não há persistence context, dirty checking, cache de 1º nível, lazy loading nem mapeamento de relações. Mudar um campo de um objeto carregado **não persiste** — sem dirty checking, nada acontece até você chamar `save`.

```java
// ❌ esperando dirty checking da JPA
Order order = orders.findById(1L).block();
order.setStatus("SHIPPED");
// fim do "método transacional" — na JPA, flush persistiria. No R2DBC: nada.
```

**Fix:** persista explicitamente. R2DBC é mapeamento linha→objeto + composição reativa, não gerência de ciclo de vida de entidade:

```java
// ✓ save explícito devolve Mono<Order>
return orders.findById(1L)
    .flatMap(order -> {
        order.setStatus("SHIPPED");
        return orders.save(order);
    });
```

## Em entrevista

### Frase pronta (inglês)

> R2DBC is the reactive, non-blocking driver SPI for relational databases — the counterpart to blocking JDBC — and on top of it Spring Data R2DBC gives you `R2dbcRepository` and `DatabaseClient`, whose methods return `Mono` and `Flux` instead of plain objects. The crucial point is that R2DBC is not an ORM: there is no `EntityManager`, no persistence context, no first-level cache, no dirty checking, and no lazy loading. An entity holds the foreign key, not a related object, so I resolve relationships by hand, chaining queries with `flatMap` rather than relying on `@OneToMany` or a lazy `@ManyToOne`. I reach for it when I'm already on a reactive stack like WebFlux, because the whole path has to be non-blocking — a single blocking JDBC call in the middle would stall the event loop and erase the throughput gain. So I treat R2DBC as the price you pay for going non-blocking: you give up the entire JPA comfort layer in exchange for never blocking a thread on database I/O.

### Vocabulário

| Termo PT | Termo EN |
| --- | --- |
| acesso reativo a banco | reactive database access |
| driver não-bloqueante | non-blocking driver |
| sem contexto de persistência | no persistence context |
| sem dirty checking | no dirty checking |
| carregamento tardio (lazy) | lazy loading |
| relação resolvida à mão | manually resolved relationship |
| cache de 1º nível | first-level cache |
| transação reativa | reactive transaction |

## Veja também

- [[03-Dominios/Tecnologia/Java/Programação Reativa/10 - Spring WebFlux — o stack não-bloqueante sobre Netty e o DispatcherHandler|Spring WebFlux]]
- [[03-Dominios/Tecnologia/Java/Programação Reativa/16 - Capstone — uma request reativa de ponta a ponta no WebFlux|Capstone]]
- [[03-Dominios/Tecnologia/Java/Persistência de dados/01 - O que é a camada de persistência — Spring Data, JPA e Hibernate|O que é a camada de persistência]]
- [[03-Dominios/Tecnologia/Java/Persistência de dados/03 - O persistence context e os estados da entidade|O persistence context]]
- [[03-Dominios/Tecnologia/Java/Persistência de dados/07 - Fetch strategies — LAZY, EAGER e a LazyInitializationException|Fetch strategies]]
- [[03-Dominios/Tecnologia/Java/Programação Reativa/index|Programação Reativa (MOC do galho)]]
- [[03-Dominios/Tecnologia/Java/index|Trilha Java]]
- [[03-Dominios/Tecnologia/Java/Dicionário de Java|Dicionário de Java]]

## Referências

- R2DBC — Reactive Relational Database Connectivity: https://r2dbc.io/
- Spring Data R2DBC — Reference Documentation: https://docs.spring.io/spring-data/r2dbc/docs/current/reference/html/
