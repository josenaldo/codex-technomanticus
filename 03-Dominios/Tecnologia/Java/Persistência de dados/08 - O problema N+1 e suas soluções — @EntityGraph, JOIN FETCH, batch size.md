---
title: "O problema N+1 e suas soluções — @EntityGraph, JOIN FETCH, batch size"
created: 2026-06-09
updated: 2026-06-09
type: concept
progress: backlog
status: seedling
publish: true
fase: adepto
tags:
  - java
  - persistencia
  - adepto
  - fetch
  - n-mais-1
aliases:
  - "problema N+1"
  - "N+1 queries"
  - "@EntityGraph"
---

# O problema N+1 e suas soluções — @EntityGraph, JOIN FETCH, batch size

> [!abstract] TL;DR
> O N+1 é o bug mais caro da JPA: carregar N pais e acessar uma relação lazy de cada um gera **1+N queries** — uma para buscar os pais e mais uma por pai para resolver a coleção. Você resolve com `@EntityGraph` (declarativo, preferido no Spring Data), `JOIN FETCH` (JPQL, traz a coleção na mesma query — mas só **uma** coleção por query, senão vira produto cartesiano), `@BatchSize` (carrega N pais por query em vez de 1) ou **DTO projection**. E cuidado redobrado ao misturar fetch de coleção com **paginação**: o Hibernate avisa `HHH000104` e pagina em **memória**.

## O que é

O **problema N+1** acontece quando você carrega uma lista de N entidades pai e, ao acessar uma associação **lazy** de cada uma delas, o provedor JPA dispara uma query adicional por entidade. O total fica em **1 query para os pais + N queries para as relações** — daí o nome.

É um problema **silencioso**: o código compila, passa nos testes locais com 3 registros e funciona em dev. Em produção, com 5 000 registros, são 5 001 idas ao banco numa única requisição. A latência explode, o pool de conexões satura, e o culpado é um `for` aparentemente inocente.

O N+1 não é exclusivo de coleções (`@OneToMany`/`@ManyToMany`). Associações `@ManyToOne` lazy também o causam: carregar N `Order` e ler `order.getCustomer().getName()` de cada uma dispara N queries para os clientes.

## Por que importa

Latência de banco domina o tempo de resposta de quase toda aplicação CRUD. Cada query tem custo fixo: round-trip de rede, parsing, planejamento, aquisição de conexão do pool. Trocar **1 query** por **501 queries** não multiplica o custo por 1,2 — multiplica por centenas, porque o gargalo é o número de round-trips, não o volume de dados.

O N+1 é o problema de performance **número um** em aplicações JPA, e o mais traiçoeiro porque:

- Não aparece em revisão de código (o `for` parece trivial).
- Não aparece em teste unitário com mock de repositório.
- Não aparece em ambiente de dev com poucos dados.
- Aparece em produção, sob carga, como timeout intermitente.

Dominar as quatro soluções — `@EntityGraph`, `JOIN FETCH`, `@BatchSize` e DTO projection — e saber **quando** aplicar cada uma é o que separa um Adepto de um Iniciado em persistência.

## Como funciona

### O que é o N+1 (1 query pai + N filhos ao iterar coleção lazy)

Considere `Customer` com uma coleção lazy de `Order`:

```java
import jakarta.persistence.Entity;
import jakarta.persistence.FetchType;
import jakarta.persistence.GeneratedValue;
import jakarta.persistence.GenerationType;
import jakarta.persistence.Id;
import jakarta.persistence.OneToMany;
import java.util.List;

@Entity
public class Customer {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    private String name;

    @OneToMany(mappedBy = "customer", fetch = FetchType.LAZY)
    private List<Order> orders;

    // getters/setters
}
```

O código que dispara o N+1:

```java
List<Customer> customers = customerRepository.findAll(); // 1 query
for (Customer customer : customers) {
    // cada chamada a getOrders() resolve um proxy lazy → 1 query POR cliente
    System.out.println(customer.getName() + ": " + customer.getOrders().size());
}
```

O SQL gerado, com 3 clientes no banco:

```sql
-- 1 query para os pais
select c.id, c.name from customer c;

-- N queries para as coleções (uma por cliente)
select o.id, o.total, o.customer_id from orders o where o.customer_id = 1;
select o.id, o.total, o.customer_id from orders o where o.customer_id = 2;
select o.id, o.total, o.customer_id from orders o where o.customer_id = 3;
```

Três clientes → 4 queries. Cinco mil clientes → 5 001 queries. O número de queries cresce **linearmente** com o número de pais, e cada uma é um round-trip completo ao banco.

### Detectar: SQL logging, `generate_statistics`, contador de query no teste

Há três níveis de detecção, do mais barato ao mais robusto.

**1. SQL logging** — ligue o logger `org.hibernate.SQL` em `DEBUG`. Você vê cada SQL no console e conta visualmente o padrão repetido:

```yaml
logging:
  level:
    org.hibernate.SQL: DEBUG
    # opcional: ver os valores dos parâmetros (NÃO usar em produção)
    org.hibernate.orm.jdbc.bind: TRACE
spring:
  jpa:
    properties:
      hibernate:
        format_sql: true
```

Se você vê a mesma query `select ... from orders where customer_id = ?` repetindo dezenas de vezes seguidas, é N+1.

**2. `hibernate.generate_statistics`** — habilita o coletor de métricas do Hibernate. Cada requisição loga um resumo com o número de queries executadas:

```yaml
spring:
  jpa:
    properties:
      hibernate:
        generate_statistics: true
```

No log aparece algo como `Session Metrics ... 502 statements`. Um número absurdo de `statements` para uma operação simples denuncia o N+1.

**3. Contador de query no teste** — a defesa mais forte é **automatizar**. Uma assertiva de teste que falha se o número de queries ultrapassar o esperado transforma o N+1 silencioso num teste vermelho. Com `org.hibernate.stat.Statistics`:

```java
import org.hibernate.SessionFactory;
import org.hibernate.stat.Statistics;
import org.junit.jupiter.api.Test;
import jakarta.persistence.EntityManagerFactory;
import static org.assertj.core.api.Assertions.assertThat;

@DataJpaTest
class CustomerQueryCountTest {

    @Autowired
    private EntityManagerFactory emf;

    @Autowired
    private CustomerRepository repository;

    @Test
    void carregarClientesComPedidosNaoDeveCausarNMaisUm() {
        Statistics stats = emf.unwrap(SessionFactory.class).getStatistics();
        stats.setStatisticsEnabled(true);
        stats.clear();

        repository.findAllWithOrders().forEach(c -> c.getOrders().size());

        // 1 query só, não 1+N
        assertThat(stats.getPrepareStatementCount()).isEqualTo(1L);
    }
}
```

Bibliotecas como **datasource-proxy** ou **QuickPerf** oferecem assertivas declarativas equivalentes (`@ExpectSelect(1)`), mas o princípio é o mesmo: **fixar o número de queries** como invariante testável.

### Soluções: `@EntityGraph`, `JOIN FETCH`, `@BatchSize`, DTO projection

Há quatro ferramentas. Elas não competem — cada uma tem um cenário ideal.

**`@EntityGraph` (declarativo, preferido no Spring Data).** Você anota o método do repositório dizendo **quais atributos** carregar junto, sem escrever JPQL. O Hibernate gera o `LEFT JOIN FETCH` por baixo dos panos:

```java
import org.springframework.data.jpa.repository.EntityGraph;
import org.springframework.data.jpa.repository.JpaRepository;
import java.util.List;

public interface CustomerRepository extends JpaRepository<Customer, Long> {

    @EntityGraph(attributePaths = "orders")
    List<Customer> findAll(); // sobrescreve o findAll trazendo orders junto
}
```

`attributePaths` aceita caminhos aninhados (`"orders.items"`). Há dois tipos via `EntityGraph.EntityGraphType`: `FETCH` (padrão — só os atributos listados são EAGER, o resto segue o default) e `LOAD` (os atributos listados são EAGER e o resto segue o que está mapeado na entidade). Para grafos reutilizáveis, declare um `@NamedEntityGraph` na entidade e referencie pelo nome:

```java
import jakarta.persistence.NamedAttributeNode;
import jakarta.persistence.NamedEntityGraph;

@Entity
@NamedEntityGraph(
    name = "Customer.withOrders",
    attributeNodes = @NamedAttributeNode("orders")
)
public class Customer { /* ... */ }
```

```java
@EntityGraph(value = "Customer.withOrders")
List<Customer> findByNameContaining(String fragment);
```

**`JOIN FETCH` (JPQL, traz a coleção na mesma query).** O controle explícito. Você escreve a query e diz `JOIN FETCH` para materializar a associação no mesmo SELECT:

```java
import org.springframework.data.jpa.repository.Query;

@Query("SELECT DISTINCT c FROM Customer c JOIN FETCH c.orders")
List<Customer> findAllWithOrders();
```

O `DISTINCT` é necessário porque o JOIN duplica a linha do pai uma vez por filho — sem ele você recebe o mesmo `Customer` repetido N vezes na lista. Regra de ouro: **só UMA coleção por `JOIN FETCH`**. Fazer fetch de duas coleções na mesma query gera **produto cartesiano** (toda combinação de orders × items) ou, com `List`, a `MultipleBagFetchException`.

**`@BatchSize` (carrega N pais por query em vez de 1).** Não elimina as queries extras — **reduz** o número delas agrupando. Em vez de 1 query por pai, o Hibernate carrega as coleções de até N pais de uma vez com um `IN (?, ?, ..., ?)`:

```java
import org.hibernate.annotations.BatchSize;

@OneToMany(mappedBy = "customer", fetch = FetchType.LAZY)
@BatchSize(size = 20)
private List<Order> orders;
```

Com `size = 20` e 100 clientes, o N+1 vira **1 + 5 queries** (100 ÷ 20). O SQL das coleções vira `... where customer_id in (?, ?, ... 20 valores)`. Vantagem sobre `JOIN FETCH`: não há produto cartesiano e funciona com **várias** coleções ao mesmo tempo. Pode ser configurado globalmente via `hibernate.default_batch_fetch_size`.

**DTO projection.** A solução mais enxuta quando você só precisa **ler** dados (não atualizar). Em vez de carregar entidades gerenciadas e suas coleções, você projeta exatamente os campos que precisa direto numa classe DTO via `SELECT new`:

```java
public record CustomerSummary(Long id, String name, long orderCount) {}
```

```java
@Query("""
    SELECT new com.example.CustomerSummary(c.id, c.name, COUNT(o))
    FROM Customer c LEFT JOIN c.orders o
    GROUP BY c.id, c.name
    """)
List<CustomerSummary> findCustomerSummaries();
```

Uma query, zero entidades gerenciadas, zero risco de lazy loading. É a escolha natural para telas de listagem e relatórios.

### O cuidado `JOIN FETCH` + paginação (`HHH000104` — pagina em memória; use DTO/subquery)

Misturar **fetch de coleção** com **paginação** (`setFirstResult`/`setMaxResults`, ou `Pageable` no Spring Data) é uma armadilha clássica. O problema: o `JOIN FETCH` de coleção multiplica as linhas (uma linha de SQL por filho), mas a paginação raciocina em termos de **entidades pai**. O Hibernate não consegue traduzir "página de 10 clientes" para um `LIMIT` no SQL multiplicado, então **desiste do `LIMIT`**: carrega **todas** as linhas para a memória e pagina lá. O aviso é o famoso:

```text
WARN HHH000104: firstResult/maxResults specified with collection fetch;
applying in memory
```

Em um banco grande, isso significa puxar milhões de linhas para a JVM para devolver 10 — risco real de `OutOfMemoryError`.

A solução correta é **separar a paginação do fetch da coleção**:

- **DTO projection** com paginação — projete os campos sem fetch de coleção; o `LIMIT` volta a funcionar no banco.
- **Estratégia em duas queries** — primeiro pagine só os **IDs** dos pais (`LIMIT` real no banco), depois carregue as coleções desses IDs com `JOIN FETCH ... WHERE c.id IN (:ids)` (sem paginação, agora segura).
- **`@BatchSize`** — pagina os pais normalmente (sem fetch) e deixa o batch fetching resolver as coleções em poucas queries adicionais.

Fetch de associação `@ManyToOne` (lado "um", não coleção) **não** dispara o `HHH000104` — só coleções multiplicam linhas. Paginar com `JOIN FETCH c.customer` é seguro.

## Na prática

O ponto de partida: o loop que causa o N+1.

```java
// Repositório ingênuo
public interface CustomerRepository extends JpaRepository<Customer, Long> {
    // herda findAll() — orders é LAZY
}

// Serviço que dispara o N+1
List<Customer> customers = customerRepository.findAll();
for (Customer customer : customers) {
    log.info("{} tem {} pedidos", customer.getName(), customer.getOrders().size());
}
```

O log com `org.hibernate.SQL=DEBUG` revela o padrão (1 + N):

```sql
select c.id, c.name from customer c;
select o.id, o.total from orders o where o.customer_id = 1;
select o.id, o.total from orders o where o.customer_id = 2;
select o.id, o.total from orders o where o.customer_id = 3;
-- ... uma por cliente
```

As quatro soluções, lado a lado:

```java
import org.hibernate.annotations.BatchSize;
import org.springframework.data.jpa.repository.EntityGraph;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Query;
import jakarta.persistence.Entity;
import jakarta.persistence.FetchType;
import jakarta.persistence.OneToMany;
import java.util.List;

// ── Solução 1: @EntityGraph (declarativo, preferido) ───────────────
public interface CustomerRepository extends JpaRepository<Customer, Long> {

    @EntityGraph(attributePaths = "orders")
    List<Customer> findAll();
}

// ── Solução 2: JOIN FETCH (JPQL, uma coleção por query) ────────────
public interface CustomerRepositoryFetch extends JpaRepository<Customer, Long> {

    @Query("SELECT DISTINCT c FROM Customer c JOIN FETCH c.orders")
    List<Customer> findAllWithOrders();
}

// ── Solução 3: @BatchSize (N pais por query) ───────────────────────
@Entity
class CustomerBatched {

    @OneToMany(mappedBy = "customer", fetch = FetchType.LAZY)
    @BatchSize(size = 20)
    private List<Order> orders;
}

// ── Solução 4: DTO projection via SELECT new (read-only, enxuto) ───
record CustomerSummary(Long id, String name, long orderCount) {}

interface CustomerSummaryRepository extends JpaRepository<Customer, Long> {

    @Query("""
        SELECT new com.example.CustomerSummary(c.id, c.name, COUNT(o))
        FROM Customer c LEFT JOIN c.orders o
        GROUP BY c.id, c.name
        """)
    List<CustomerSummary> findSummaries();
}
```

A configuração de SQL logging para flagrar tudo isso em dev e em teste:

```yaml
spring:
  jpa:
    properties:
      hibernate:
        format_sql: true
        generate_statistics: true   # loga "Session Metrics ... N statements"
logging:
  level:
    org.hibernate.SQL: DEBUG        # mostra cada SQL gerado
    org.hibernate.orm.jdbc.bind: TRACE  # valores dos parâmetros (só em dev)
```

Critério de escolha rápido: precisa **só ler** → DTO projection. Precisa das **entidades gerenciadas** com **uma** coleção → `@EntityGraph` ou `JOIN FETCH`. Precisa de **várias** coleções ou de **paginação** → `@BatchSize`.

## Armadilhas

### (1) N+1 silencioso escondido por OSIV

O **Open Session In View** (`spring.jpa.open-in-view=true`, ligado por padrão no Spring Boot) mantém a sessão aberta até o fim da requisição HTTP. Isso impede a `LazyInitializationException` — mas **mascara o N+1**: a serialização JSON da resposta itera as coleções lazy e dispara as queries extras na camada web, longe do repositório. O código "funciona", passa em dev com poucos dados, e só explode em produção sob carga. Desligar o OSIV transforma o N+1 mascarado num erro explícito na hora certa (no service), forçando você a resolver o fetch corretamente. Veja [[03-Dominios/Tecnologia/Java/Persistência de dados/07 - Fetch strategies — LAZY, EAGER e a LazyInitializationException|Fetch strategies]].

### (2) JOIN FETCH de DUAS coleções

`JOIN FETCH` de duas coleções na mesma query é proibido na prática. Com mapeamento `List` (bag), o Hibernate lança **`MultipleBagFetchException`** logo na inicialização. Se você "contornar" trocando para `Set`, evita a exceção mas cai num **produto cartesiano**: cada `Order` é multiplicado por cada `Item`, e o número de linhas vira `orders × items` — pode estourar a memória. A solução é fazer fetch de **uma** coleção por query (e usar `@BatchSize` ou queries separadas para as demais), nunca duas.

### (3) Paginar com JOIN FETCH de coleção (HHH000104)

Combinar `Pageable`/`setMaxResults` com `JOIN FETCH` de **coleção** faz o Hibernate logar `HHH000104: firstResult/maxResults specified with collection fetch; applying in memory` e **paginar em memória**: ele puxa o resultado inteiro para a JVM e fatia a página lá, ignorando o `LIMIT` do banco. Em tabelas grandes é receita para `OutOfMemoryError`. Pagine os pais sem fetch de coleção (DTO, `@BatchSize`, ou duas queries: IDs paginados + fetch desses IDs). Veja [[03-Dominios/Tecnologia/Java/Persistência de dados/11 - Paginação e ordenação — Pageable, Page e Slice|Paginação e ordenação]].

### (4) @BatchSize não é bala de prata

`@BatchSize` **reduz** o número de queries, não elimina. Com 1 000 pais e `size = 20`, ainda são 1 + 50 queries. Para leitura pura de grandes volumes, DTO projection (1 query) costuma ganhar. `@BatchSize` brilha quando você precisa das entidades gerenciadas **e** de várias coleções, onde `JOIN FETCH` não cabe.

## Em entrevista

### Frase pronta (inglês)

> The N+1 problem happens when I load N parent entities and then access a lazy association on each one, producing one query for the parents plus N extra queries for the children. I detect it by enabling `org.hibernate.SQL` logging and `hibernate.generate_statistics`, or — more reliably — by asserting the query count in an integration test so it can never regress silently. To fix it I reach for `@EntityGraph` in Spring Data as my default declarative tool, `JOIN FETCH` when I need explicit JPQL control over a single collection, `@BatchSize` when several collections or pagination are involved, and a DTO projection when the call is read-only. The one trap I always watch for is fetching a collection together with pagination — Hibernate logs `HHH000104` and paginates in memory, so I keep the collection fetch out of the paginated query.

### Vocabulário

| Português | Inglês |
| --- | --- |
| problema N+1 | N+1 problem |
| grafo de entidade | entity graph |
| busca em lote | batch fetching |
| junção com fetch | join fetch |
| projeção | projection |
| produto cartesiano | cartesian product |
| busca preguiçosa | lazy fetching |
| contagem de queries | query count |

## Veja também

- [[03-Dominios/Tecnologia/Java/Persistência de dados/07 - Fetch strategies — LAZY, EAGER e a LazyInitializationException|Fetch strategies]]
- [[03-Dominios/Tecnologia/Java/Persistência de dados/10 - Projections e DTOs — não vazar a entidade|Projections e DTOs]]
- [[03-Dominios/Tecnologia/Java/Persistência de dados/11 - Paginação e ordenação — Pageable, Page e Slice|Paginação e ordenação]]
- [[03-Dominios/Tecnologia/Java/Persistência de dados/index|Persistência de dados (MOC do galho)]]
- [[03-Dominios/Tecnologia/Java/index|Trilha Java]]
- [[03-Dominios/Tecnologia/Java/Dicionário de Java#N+1 (problema)|N+1 (problema)]]
- [[03-Dominios/Tecnologia/Java/Dicionário de Java#@EntityGraph|@EntityGraph]]

## Referências

- Hibernate ORM User Guide — Fetching, batch fetching, `@BatchSize`, join fetch, `HHH000104`, `MultipleBagFetchException`: <https://docs.hibernate.org/orm/current/userguide/html_single/Hibernate_User_Guide.html>
- Spring Data JPA Reference — Entity Graphs (`@EntityGraph`, `@NamedEntityGraph`, `EntityGraphType`): <https://docs.spring.io/spring-data/jpa/reference/jpa/entity-graph.html>
