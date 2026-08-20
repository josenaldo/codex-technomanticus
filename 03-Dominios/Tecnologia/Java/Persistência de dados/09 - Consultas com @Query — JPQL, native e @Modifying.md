---
title: "Consultas com @Query — JPQL, native e @Modifying"
created: 2026-06-09
updated: 2026-06-09
type: concept
progress: backlog
status: seedling
publish: true
fase: Adepto
tags:
  - java
  - persistencia
  - adepto
  - spring-data
  - jpql
aliases:
  - "@Query"
  - "JPQL"
  - "@Modifying"
---

# Consultas com @Query — JPQL, native e @Modifying

> [!abstract] TL;DR
> Quando os query methods derivados não bastam, `@Query` permite escrever JPQL — que consulta **entidades e atributos Java**, não tabelas e colunas do banco — ou SQL nativo com `nativeQuery = true`. Para UPDATE e DELETE em massa, `@Modifying` executa o DML direto no banco, mas é preciso acionar `clearAutomatically = true` para que o persistence context (L1 cache) não fique com objetos obsoletos na memória.

---

## O que é

`@Query` é uma anotação do Spring Data JPA que permite declarar consultas explícitas diretamente na interface do repositório, substituindo ou complementando os query methods derivados gerados pelo framework.

Ela suporta dois dialetos:

- **JPQL** (Java Persistence Query Language) — linguagem orientada a objetos que opera sobre entidades e seus atributos; é portável entre bancos.
- **SQL nativo** — SQL puro do banco de dados, acessado via `nativeQuery = true`; útil para recursos específicos do dialeto ou otimizações finas.

Para operações de escrita (`UPDATE`, `DELETE`) em massa, o `@Modifying` complementa o `@Query`, autorizando Spring Data a executar DML via JPQL ou SQL nativo.

---

## Por que importa

Os query methods derivados (`findByStatusAndTotalGreaterThan`) cobrem a maior parte dos casos simples, mas têm limites:

- Expressões complexas (subconsultas, funções de agregação, `CASE`, `JOIN` multivariado) não têm representação nos métodos derivados.
- SQL nativo é necessário quando se usa índices de texto completo, tipos proprietários ou CTEs recursivas.
- UPDATE e DELETE em massa via `deleteAll(list)` ou `saveAll` carregam todas as entidades na memória antes de agir; `@Modifying @Query` executa um único statement SQL, reduzindo drasticamente o volume de roundtrips ao banco.

Entender `@Query` separa quem sabe "usar Spring Data" de quem sabe "controlar o que acontece no banco".

---

## Como funciona

### JPQL: consulta entidades/atributos, não tabelas/colunas

JPQL é inspirado em SQL, mas referencia o **modelo de objetos**, não o esquema relacional:

- `FROM Order o` — entidade `Order`, não a tabela `orders`
- `o.status` — atributo Java, não a coluna `status_id`
- `o.customer.name` — navega pela associação; gera JOIN automaticamente

O Hibernate traduz JPQL para SQL em tempo de execução, adaptando ao dialeto configurado. Isso significa que a mesma query JPQL funciona em PostgreSQL, MySQL e H2 sem alteração.

Parâmetros podem ser posicionais (`?1`, `?2`) ou nomeados (`:status`, `:min`). Prefira os nomeados com `@Param` — são mais legíveis e resilientes a reordenações de parâmetros.

```java
public interface OrderRepository extends JpaRepository<Order, Long> {

    @Query("SELECT o FROM Order o WHERE o.status = :status AND o.total > :min")
    List<Order> findByStatusAndMinTotal(
            @Param("status") String status,
            @Param("min") BigDecimal min);
}
```

### SQL nativo (`nativeQuery = true`): quando o JPQL não basta

Com `nativeQuery = true`, o Spring Data passa o SQL diretamente ao driver JDBC sem tradução. O mapeamento de resultado segue as mesmas regras de projeção (entidade, `Projection`, `Tuple`), mas a query usa **nomes de tabelas e colunas reais**.

Casos de uso típicos:

- `FULL TEXT SEARCH` (PostgreSQL `@@` / MySQL `MATCH AGAINST`)
- `RETURNING` clause (PostgreSQL)
- Funções de janela (`ROW_NUMBER`, `LAG`, `LEAD`)
- Subqueries correlacionadas complexas que o Hibernate não optimiza bem em JPQL

```java
@Query(
    value = "SELECT * FROM orders WHERE status = :status AND total > :min ORDER BY created_at DESC",
    nativeQuery = true)
List<Order> findByStatusNative(
        @Param("status") String status,
        @Param("min") BigDecimal min);
```

> [!warning] Portabilidade
> SQL nativo amarra o código ao dialeto do banco. Isole essas queries; documente o motivo pelo qual JPQL não foi suficiente.

### `@Modifying`: UPDATE/DELETE em massa (e o `clearAutomatically`/`flushAutomatically` que limpa o L1)

UPDATE e DELETE em JPQL ou SQL nativo exigem `@Modifying` para que o Spring Data libere a execução do DML. Sem ele, o framework interpreta a query como SELECT e lança exceção.

```java
@Modifying(clearAutomatically = true, flushAutomatically = true)
@Query("UPDATE Order o SET o.status = :newStatus WHERE o.status = :oldStatus AND o.updatedAt < :cutoff")
int bulkUpdateStatus(
        @Param("newStatus") String newStatus,
        @Param("oldStatus") String oldStatus,
        @Param("cutoff") LocalDateTime cutoff);
```

**Por que `clearAutomatically = true`?**

O Hibernate mantém um **persistence context** (L1 cache) com snapshots de todas as entidades carregadas na sessão atual. Quando um `UPDATE` ou `DELETE` em massa é executado diretamente no banco via JPQL/SQL, o persistence context **não é notificado** — os objetos Java em memória continuam refletindo o estado anterior. Qualquer leitura posterior retornará dados obsoletos (stale).

`clearAutomatically = true` instrui o Spring Data a chamar `EntityManager.clear()` logo após o DML, descartando todos os snapshots do contexto. O próximo `find` buscará os dados frescos do banco.

**Por que `flushAutomatically = true`?**

Antes de executar o DML em massa, pode haver alterações pendentes no contexto (entidades `dirty` ainda não sincronizadas). `flushAutomatically = true` garante que essas mudanças sejam persistidas (flush) antes do bulk operation, evitando inconsistências.

> [!info] Trade-off do `clearAutomatically`
> Limpar o persistence context descarta também entidades que ainda não foram salvas e que serão perdidas se não houver flush prévio. Por isso, `clearAutomatically` é mais seguro quando combinado com `flushAutomatically = true` ou dentro de transações bem delimitadas.

---

## Na prática

```java
import jakarta.persistence.Entity;
import jakarta.persistence.Id;
import jakarta.persistence.GeneratedValue;
import jakarta.persistence.GenerationType;
import java.math.BigDecimal;
import java.time.LocalDateTime;

@Entity
public class Order {
    @Id @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;
    private String status;
    private BigDecimal total;
    private LocalDateTime updatedAt;
    // getters/setters omitidos
}
```

```java
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Modifying;
import org.springframework.data.jpa.repository.Query;
import org.springframework.data.repository.query.Param;
import java.math.BigDecimal;
import java.time.LocalDateTime;
import java.util.List;

public interface OrderRepository extends JpaRepository<Order, Long> {

    // 1. JPQL — consulta entidades e atributos Java
    @Query("SELECT o FROM Order o WHERE o.status = :status AND o.total > :min")
    List<Order> findByStatusAndMinTotal(
            @Param("status") String status,
            @Param("min") BigDecimal min);

    // 2. SQL nativo — usa tabela e colunas reais
    @Query(
        value = "SELECT * FROM orders WHERE customer_id = :customerId ORDER BY created_at DESC LIMIT :limit",
        nativeQuery = true)
    List<Order> findRecentByCustomer(
            @Param("customerId") Long customerId,
            @Param("limit") int limit);

    // 3. @Modifying — UPDATE em massa + limpeza do L1
    @Modifying(clearAutomatically = true, flushAutomatically = true)
    @Query("UPDATE Order o SET o.status = :newStatus WHERE o.status = :oldStatus AND o.updatedAt < :cutoff")
    int bulkUpdateStatus(
            @Param("newStatus") String newStatus,
            @Param("oldStatus") String oldStatus,
            @Param("cutoff") LocalDateTime cutoff);

    // 4. @Modifying — DELETE em massa
    @Modifying(clearAutomatically = true)
    @Query("DELETE FROM Order o WHERE o.status = 'CANCELLED' AND o.updatedAt < :cutoff")
    int deleteCancelledBefore(@Param("cutoff") LocalDateTime cutoff);
}
```

No serviço, o método de bulk update deve rodar dentro de `@Transactional`:

```java
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;
import java.time.LocalDateTime;

@Service
public class OrderService {

    private final OrderRepository orderRepository;

    public OrderService(OrderRepository orderRepository) {
        this.orderRepository = orderRepository;
    }

    @Transactional
    public int expireOldPendingOrders(LocalDateTime cutoff) {
        return orderRepository.bulkUpdateStatus("EXPIRED", "PENDING", cutoff);
    }
}
```

---

## Armadilhas

### (1) `@Modifying` sem `clearAutomatically` — entidade stale no persistence context

Se um `Order` já foi carregado na sessão e em seguida um `@Modifying @Query` altera seu `status` no banco, a instância em memória ainda mostra o status antigo. Qualquer leitura subsequente dentro da mesma transação retornará o objeto obsoleto do cache L1, não o valor atual do banco. Adicione `clearAutomatically = true` para forçar o descarte dos snapshots.

### (2) Confundir JPQL com SQL — nome de entidade vs nome de tabela

JPQL usa o nome da classe Java (`Order`) e o atributo (`o.total`). SQL usa o nome da tabela (`orders`) e da coluna (`total`). Escrever `FROM orders` em uma query JPQL sem `nativeQuery = true` resulta em erro de parsing do Hibernate em tempo de execução, pois `orders` não é uma entidade conhecida. Sempre verifique: se `nativeQuery = true` está ausente, a query deve usar entidades e atributos Java.

### (3) `LIKE '%valor%'` em tabela grande sem índice — full scan silencioso

A query `WHERE o.status LIKE '%pend%'` impede uso de índice B-tree em qualquer banco relacional, resultando em varredura sequencial completa. O problema não aparece em desenvolvimento (poucas linhas), mas explode em produção. Para buscas por substring, use índices de texto completo do banco (`GIN`/`GiST` no PostgreSQL, `FULLTEXT` no MySQL) e SQL nativo.

### (4) `@Modifying` em método `@Transactional(readOnly = true)`

Transações read-only otimizam o flush automático do Hibernate, que é desabilitado. Executar um `@Modifying` dentro de uma transação read-only pode ser ignorado silenciosamente ou lançar exceção dependendo do provider. Garanta que métodos com `@Modifying` rodem em transações de escrita.

### (5) Ausência de `@Transactional` no método de serviço

`@Modifying` requer uma transação ativa. Sem `@Transactional` no método chamador (ou na interface do repositório), o Spring lança `TransactionRequiredException`. O Spring Data não abre transação automaticamente para métodos `@Modifying` customizados.

---

## Em entrevista

### Frase pronta (inglês)

"`@Query` lets you write explicit JPQL or native SQL when derived query methods aren't expressive enough. JPQL operates on entity names and Java attributes — not table or column names — so it stays database-agnostic. For bulk UPDATE and DELETE operations, `@Modifying` tells Spring Data to execute the DML directly, but you must set `clearAutomatically = true` to evict stale snapshots from the first-level cache; otherwise the persistence context keeps serving outdated in-memory objects even after the database has changed. When there are dirty changes pending in the session, combining it with `flushAutomatically = true` ensures those writes reach the database before the bulk operation runs."

### Vocabulário

| Português | Inglês |
|---|---|
| consulta | query |
| consulta nativa | native query |
| linguagem de consulta JPA | JPQL — Java Persistence Query Language |
| consulta de modificação | modifying query |
| parâmetro nomeado | named parameter |
| operação em massa | bulk operation |
| contexto de persistência | persistence context |
| cache de primeiro nível | first-level cache (L1 cache) |
| entidade obsoleta | stale entity |
| limpeza do contexto | context clear / `clearAutomatically` |
| descarga de pendências | flush / `flushAutomatically` |
| varredura sequencial | full table scan / sequential scan |

---

## Veja também

- [[03-Dominios/Tecnologia/Java/Persistência de dados/04 - Spring Data repositories — JpaRepository e query methods derivados|Spring Data repositories]]
- [[03-Dominios/Tecnologia/Java/Persistência de dados/10 - Projections e DTOs — não vazar a entidade|Projections e DTOs]]
- [[03-Dominios/Tecnologia/Java/Persistência de dados/15 - Consultas dinâmicas e os limites da JPA — Specifications, Criteria e SQL|Consultas dinâmicas e os limites da JPA]]
- [[03-Dominios/Tecnologia/Java/Persistência de dados/index|Persistência de dados (MOC do galho)]]
- [[03-Dominios/Tecnologia/Java/index|Trilha Java]]
- [[03-Dominios/Tecnologia/Java/Dicionário de Java#@Query (JPQL/native)|@Query (JPQL/native)]]
- [[03-Dominios/Tecnologia/Java/Dicionário de Java#@Modifying|@Modifying]]

---

## Referências

- [Spring Data JPA — Query Methods](https://docs.spring.io/spring-data/jpa/reference/jpa/query-methods.html)
- [Jakarta Persistence 3.2 Specification — Chapter 4: Query Language](https://jakarta.ee/specifications/persistence/3.2/)
- [Hibernate ORM Documentation — HQL and JPQL](https://docs.jboss.org/hibernate/orm/6.6/querylanguage/html_single/Hibernate_Query_Language.html)
