---
title: "Consultas dinâmicas e os limites da JPA — Specifications, Criteria e SQL"
created: 2026-06-09
updated: 2026-06-09
type: concept
progress: backlog
status: seedling
publish: true
fase: Magus
tags:
  - java
  - persistencia
  - magus
  - spring-data
  - jpql
aliases:
  - "Specifications"
  - "Criteria API"
  - "limites da JPA"
---

# Consultas dinâmicas e os limites da JPA — Specifications, Criteria e SQL

> [!abstract] TL;DR
> Para filtros dinâmicos componíveis, use Specifications do Spring Data — construídas sobre a Criteria API type-safe da spec Jakarta Persistence — via `JpaSpecificationExecutor` e composição fluente (`where(...).and(...).or(...)`). Quando a JPA não basta (analítico, window functions, bulk, reporting), desça ao SQL com `JdbcClient`/`JdbcTemplate` (Spring) ou jOOQ (type-safe). Sem dogma: a ferramenta certa para o problema certo.

## O que é

**Specification** é uma interface do Spring Data JPA que encapsula um único predicado de consulta em um objeto componível:

```java
public interface Specification<T> {
    Predicate toPredicate(Root<T> root, CriteriaQuery<?> query, CriteriaBuilder cb);
}
```

Especificações são combinadas com `Specification.where(...).and(...).or(...)`, produzindo queries dinâmicas sem proliferação de métodos derivados ou JPQL concatenado manualmente.

A **Criteria API** (especificação Jakarta Persistence, também presente no Galho 7) é a camada sobre a qual as Specifications operam: `CriteriaBuilder` constrói predicados, `CriteriaQuery` define a estrutura da query e `Root<T>` representa a entidade raiz — tudo verificado em tempo de compilação.

## Por que importa

Queries com filtros opcionais são ubíquas em sistemas reais — buscas com múltiplos parâmetros, dashboards com facetas, filtros de listagem. As alternativas ingênuas escalam mal:

- **Query methods derivados** (`findByStatusAndTotalGreaterThan(...)`) explodem em número quando as combinações crescem.
- **JPQL concatenado manualmente** produz código frágil, propenso a SQL injection e difícil de testar.
- **`@Query` com `nativeQuery`** resolve casos específicos mas não é componível.

Specifications endereçam o problema de composição. E reconhecer os limites da JPA — sabendo quando usar SQL direto — é sinal de maturidade na camada de persistência.

## Como funciona

### Specifications: filtros dinâmicos componíveis (`JpaSpecificationExecutor`, `where(...).and(...)`)

O repositório precisa estender `JpaSpecificationExecutor<T>`:

```java
public interface OrderRepository
        extends JpaRepository<Order, Long>,
                JpaSpecificationExecutor<Order> {
}
```

Isso habilita métodos como `findAll(Specification<T>)`, `findOne(Specification<T>)`, `count(Specification<T>)` e `exists(Specification<T>)`.

As especificações são criadas como métodos estáticos de fábrica em uma classe auxiliar:

```java
import jakarta.persistence.criteria.*;

public class OrderSpecs {

    public static Specification<Order> hasStatus(OrderStatus status) {
        return (root, query, cb) ->
                cb.equal(root.get("status"), status);
    }

    public static Specification<Order> totalGreaterThan(BigDecimal threshold) {
        return (root, query, cb) ->
                cb.greaterThan(root.get("total"), threshold);
    }

    public static Specification<Order> forCustomer(Long customerId) {
        return (root, query, cb) ->
                cb.equal(root.get("customerId"), customerId);
    }
}
```

A composição no service fica legível e declarativa:

```java
Specification<Order> spec = Specification
        .where(OrderSpecs.hasStatus(OrderStatus.PAID))
        .and(OrderSpecs.totalGreaterThan(new BigDecimal("500")))
        .and(OrderSpecs.forCustomer(customerId));

List<Order> orders = orderRepository.findAll(spec);
```

Parâmetros opcionais são tratados com verificações simples:

```java
Specification<Order> spec = Specification.where(null);
if (status != null)   spec = spec.and(OrderSpecs.hasStatus(status));
if (minTotal != null) spec = spec.and(OrderSpecs.totalGreaterThan(minTotal));
```

### Criteria API: a query programática type-safe da spec JPA (Galho 7) sob as Specifications

A Criteria API é definida na especificação Jakarta Persistence e implementada pelo Hibernate (e outros provedores). Ela permite construir queries inteiramente em Java, sem strings.

Os três atores principais:

| Objeto | Papel |
|---|---|
| `CriteriaBuilder` | Fábrica de predicados, expressões e funções (`cb.equal`, `cb.like`, `cb.and`, `cb.lessThan`...) |
| `CriteriaQuery<T>` | Estrutura da query: `select`, `from`, `where`, `orderBy` |
| `Root<T>` | Ponto de entrada para navegar nos atributos da entidade (`root.get("total")`) |

O Spring Data JPA injeta esses três objetos no lambda da `Specification`, abstraindo o boilerplate de criar `EntityManager` e executar a query manualmente.

Para type-safety ainda maior, a JPA Metamodel (classes geradas como `Order_`) permite referenciar atributos sem strings: `root.get(Order_.total)`. Isso evita erros de digitação detectáveis somente em runtime.

### Quando a JPA não basta (analítico, window functions, bulk, reporting)

A JPA (JPQL e Criteria) modela operações orientadas a entidades. Há cenários onde esse modelo sofre ou simplesmente não suporta:

- **Window functions** (`ROW_NUMBER()`, `RANK()`, `LAG()`, `SUM() OVER (PARTITION BY ...)`) — sem suporte em JPQL padrão.
- **Queries analíticas complexas** com múltiplos `GROUP BY`, `ROLLUP`, `CUBE` ou CTEs recursivas.
- **Bulk updates/deletes com lógica condicional** que precisa de subconsultas correlacionadas elaboradas.
- **Relatórios e ETL** que cruzam múltiplas tabelas de forma desnormalizada — mapear tudo para entidades é custo sem benefício.

Nesses casos, tentar forçar JPQL ou Criteria API produz código ilegível, com workarounds frágeis. O escape hatch é legítimo e profissional.

### O escape hatch: `JdbcClient`/`JdbcTemplate`, jOOQ (type-safe)

**`JdbcClient`** (Spring 6.1+) é a API fluente moderna para SQL direto:

```java
// Exemplo na seção "Na prática"
jdbcClient.sql("SELECT ...")
          .param("customerId", customerId)
          .query(RowMapper)
          .list();
```

**`JdbcTemplate`** é a alternativa clássica (Spring Framework desde a versão 1): mais verboso, mas amplamente conhecido e suportado.

**jOOQ** (Java Object Oriented Querying) gera código Java a partir do schema do banco e oferece uma DSL type-safe para SQL completo — incluindo window functions, CTEs e dialect-specific features. É a escolha quando se quer a expressividade do SQL com a segurança do compilador Java, sem o modelo ORM.

A escolha entre os três depende do contexto: `JdbcClient` para queries pontuais e simples; jOOQ quando o projeto já adotou a ferramenta ou a complexidade das queries analíticas justifica o investimento.

## Na prática

```java
// Repositório com suporte a Specifications
public interface OrderRepository
        extends JpaRepository<Order, Long>,
                JpaSpecificationExecutor<Order> {
}

// Especificações reutilizáveis
import jakarta.persistence.criteria.*;
import org.springframework.data.jpa.domain.Specification;
import java.math.BigDecimal;

public class OrderSpecs {

    public static Specification<Order> hasStatus(OrderStatus status) {
        return (root, query, cb) ->
                status == null ? cb.conjunction()
                               : cb.equal(root.get("status"), status);
    }

    public static Specification<Order> totalGreaterThan(BigDecimal threshold) {
        return (root, query, cb) ->
                threshold == null ? cb.conjunction()
                                  : cb.greaterThan(root.get("total"), threshold);
    }

    public static Specification<Order> forCustomer(Long customerId) {
        return (root, query, cb) ->
                customerId == null ? cb.conjunction()
                                   : cb.equal(root.get("customerId"), customerId);
    }
}

// Service: composição fluente com parâmetros opcionais
@Service
@RequiredArgsConstructor
public class OrderQueryService {

    private final OrderRepository orderRepository;
    private final JdbcClient jdbcClient;

    public List<Order> search(OrderStatus status, BigDecimal minTotal, Long customerId) {
        Specification<Order> spec = Specification
                .where(OrderSpecs.hasStatus(status))
                .and(OrderSpecs.totalGreaterThan(minTotal))
                .and(OrderSpecs.forCustomer(customerId));

        return orderRepository.findAll(spec);
    }

    // Escape hatch: relatório analítico com window function
    public List<CustomerRankingDTO> topCustomersByRevenue(int year) {
        String sql = """
                SELECT
                    c.id,
                    c.name,
                    SUM(o.total)                                         AS total_revenue,
                    RANK() OVER (ORDER BY SUM(o.total) DESC)             AS revenue_rank
                FROM orders o
                JOIN customers c ON c.id = o.customer_id
                WHERE EXTRACT(YEAR FROM o.created_at) = :year
                GROUP BY c.id, c.name
                ORDER BY revenue_rank
                """;

        return jdbcClient.sql(sql)
                .param("year", year)
                .query((rs, rowNum) -> new CustomerRankingDTO(
                        rs.getLong("id"),
                        rs.getString("name"),
                        rs.getBigDecimal("total_revenue"),
                        rs.getInt("revenue_rank")
                ))
                .list();
    }
}
```

> [!tip] `cb.conjunction()`
> Retorna um predicado sempre verdadeiro (`1=1`). É o idioma canônico para lidar com parâmetros opcionais dentro de uma `Specification` — garante que a composição com `.and()` funcione corretamente mesmo quando o filtro não se aplica.

## Armadilhas

### (1) Forçar JPQL/Criteria onde SQL era a ferramenta certa

Tentar implementar um relatório com `RANK() OVER (PARTITION BY ...)` via Criteria API resulta em código monstruoso cheio de workarounds — ou simplesmente não é possível em JPQL padrão. O sinal de alerta é quando o predicado começa a precisar de `query.subquery(...)` em cascata para algo que seria trivial em SQL. Reconhecer esse ponto e usar `JdbcClient` ou jOOQ não é derrota — é decisão técnica correta.

### (2) Specification com lógica de negócio excessiva

`Specification` deve encapsular **um predicado** bem definido, não um fluxo de decisão. Quando uma especificação começa a consultar outros repositórios, fazer cálculos complexos ou ter múltiplos `if`/`else` internos, a abstração foi ultrapassada. O predicate deve ser dumb; a orquestração fica no service.

### (3) Achar que JPA serve para tudo e ignorar o escape hatch

O mapeamento objeto-relacional resolve persistência orientada a entidades com elegância. Quando o problema é analítico, o custo de mapear resultados para entidades (ou projections complexas) pode superar qualquer ganho. Ignorar `JdbcClient`, `JdbcTemplate` e jOOQ por purismo ORM é uma armadilha comum em equipes que aprenderam JPA primeiro e nunca questionaram seus limites.

## Em entrevista

### Frase pronta (inglês)

"Spring Data Specifications wrap the JPA Criteria API into composable predicates — you implement the `Specification<T>` interface, returning a `Predicate` from `CriteriaBuilder`, and compose filters with `where().and().or()` without proliferating repository methods. When JPA hits its ceiling — window functions, complex analytics, bulk reporting — I reach for `JdbcClient` for straightforward SQL or jOOQ when I need full type-safety across the whole query. The key insight is knowing when to step outside the ORM layer rather than forcing it to do something it was never designed for."

### Vocabulário

| Termo PT | Termo EN | Definição rápida |
|---|---|---|
| Consulta dinâmica | Dynamic query | Query cujos filtros variam em runtime conforme parâmetros opcionais |
| Especificação | Specification | Objeto que encapsula um predicado componível (`Specification<T>`) |
| API de critérios | Criteria API | API Jakarta Persistence para construir queries programáticas e type-safe |
| Type-safe | Type-safe | Verificado pelo compilador; erros de tipo são detectados em compile-time, não em runtime |
| Função de janela | Window function | Função SQL (`RANK`, `LAG`, `SUM OVER`) que opera sobre partições de linhas sem colapsar o resultado |
| Escotilha de fuga | Escape hatch | Mecanismo deliberado para contornar uma abstração (JPA) e acessar a camada inferior (SQL direto) |

## Veja também

- [[03-Dominios/Tecnologia/Java/Persistência de dados/09 - Consultas com @Query — JPQL, native e @Modifying|Consultas com @Query]]
- [[03-Dominios/Tecnologia/Java/Persistência de dados/11 - Paginação e ordenação — Pageable, Page e Slice|Paginação e ordenação]]
- [[03-Dominios/Tecnologia/Java/Jakarta EE/09 - JPA — a especificação de persistência|JPA (a Criteria API é da spec)]]
- [[03-Dominios/Ciência/Banco de Dados/index|Banco de dados]]
- [[03-Dominios/Tecnologia/Java/Persistência de dados/index|Persistência de dados (MOC do galho)]]
- [[03-Dominios/Tecnologia/Java/index|Trilha Java]]
- [[03-Dominios/Tecnologia/Java/Dicionário de Java#Specification (Spring Data)|Specification (Spring Data)]]
- [[03-Dominios/Tecnologia/Java/Dicionário de Java#Criteria API|Criteria API]]

## Referências

- Spring Data JPA — Specifications: <https://docs.spring.io/spring-data/jpa/reference/jpa/specifications.html>
- jOOQ — Type-safe SQL for Java: <https://www.jooq.org/>
- Jakarta Persistence 3.2 Specification (Criteria API): <https://jakarta.ee/specifications/persistence/>
- Spring Framework — `JdbcClient`: <https://docs.spring.io/spring-framework/reference/data-access/jdbc/jdbcclient.html>
