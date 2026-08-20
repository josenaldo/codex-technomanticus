---
title: "Spring Data repositories — JpaRepository e query methods derivados"
created: 2026-06-09
updated: 2026-06-09
type: concept
progress: backlog
status: seedling
publish: true
fase: iniciado
tags:
  - java
  - persistencia
  - iniciado
  - spring-data
aliases:
  - "JpaRepository"
  - "query methods derivados"
---

# Spring Data repositories — JpaRepository e query methods derivados

> [!abstract] TL;DR
> Basta declarar uma interface `extends JpaRepository<T, ID>` e o Spring Data gera a implementação em runtime via proxy. CRUD completo vem herdado (`save`, `findById`, `findAll`, `delete`, `count`, `existsById`). Para consultas extras, basta nomear o método seguindo as keywords da framework — o Spring lê o nome e gera o SQL correspondente, sem uma linha de implementação.

---

## O que é

Um **repositório Spring Data** é uma interface Java que o desenvolvedor declara, mas nunca implementa. O Spring Data JPA escaneia as interfaces que estendem `Repository` (ou suas subinterfaces) e gera um **proxy** em runtime com toda a lógica de acesso ao banco.

O resultado prático: em vez de escrever um DAO com `EntityManager`, `createQuery`, abertura e fechamento de transação, basta declarar:

```java
public interface OrderRepository extends JpaRepository<Order, Long> {
}
```

Esse repositório já tem dezenas de métodos funcionais — nenhuma implementação escrita à mão.

---

## Por que importa

- **Elimina boilerplate de DAO**: sem `EntityManager` explícito para operações básicas.
- **Consistência**: todas as equipes usam o mesmo padrão de acesso a dados.
- **Entrevistas cobram dois pontos críticos**:
  1. *Como o Spring Data gera a query a partir do nome do método?* (parsing do nome + geração de JPQL)
  2. *Qual o limite das derived queries e quando usar `@Query`?* (legibilidade e complexidade)

---

## Como funciona

### A hierarquia (`Repository` → `CrudRepository` → `PagingAndSortingRepository` → `JpaRepository`)

```text
Repository<T, ID>                  ← interface marcadora (sem métodos)
    └── CrudRepository<T, ID>      ← CRUD básico
            └── ListCrudRepository<T, ID>          ← igual ao Crud, mas retorna List
            └── PagingAndSortingRepository<T, ID>  ← findAll(Sort) e findAll(Pageable)
                    └── JpaRepository<T, ID>       ← JPA-específico: flush, saveAll, getReferenceById
```

`JpaRepository` herda tudo das interfaces acima e adiciona capacidades JPA: `flush()`, `saveAllAndFlush()`, `deleteAllInBatch()`, `getReferenceById()` (retorna proxy lazy sem hit no banco).

### CRUD herdado (`save` / `findById` / `findAll` / `delete` / `count` / `existsById`)

| Método | Comportamento |
|---|---|
| `save(entity)` | `persist` se entidade nova, `merge` se existente (detectado pelo `@Id`) |
| `findById(id)` | Retorna `Optional<T>`; SELECT por PK |
| `findAll()` | SELECT * (cuidado com tabelas grandes) |
| `delete(entity)` | Remove por referência |
| `deleteById(id)` | Remove por PK |
| `count()` | `SELECT COUNT(*)` |
| `existsById(id)` | `SELECT COUNT(*) > 0` — mais leve que `findById` quando só precisamos saber se existe |

### Derived queries: o SQL gerado do nome do método (keywords)

O Spring Data analisa o nome do método em duas partes:

- **Subject**: o que fazer — `find`, `count`, `exists`, `delete`, `remove`
- **Predicate**: os critérios — tudo depois de `By`

A partir dessas partes, o framework gera JPQL em runtime. Exemplos de keywords suportadas:

| Keyword | Método de exemplo | Trecho JPQL gerado |
|---|---|---|
| `And` | `findByStatusAndTotal(...)` | `WHERE status = ? AND total = ?` |
| `Or` | `findByStatusOrCustomer(...)` | `WHERE status = ? OR customer = ?` |
| `Between` | `findByTotalBetween(min, max)` | `WHERE total BETWEEN ? AND ?` |
| `LessThan` | `findByTotalLessThan(val)` | `WHERE total < ?` |
| `GreaterThan` | `findByTotalGreaterThan(val)` | `WHERE total > ?` |
| `Like` | `findByDescriptionLike(pat)` | `WHERE description LIKE ?` |
| `Containing` | `findByDescriptionContaining(s)` | `WHERE description LIKE %?%` |
| `In` | `findByStatusIn(collection)` | `WHERE status IN (?, ?, ...)` |
| `True` / `False` | `findByActiveTrue()` | `WHERE active = true` |
| `IgnoreCase` | `findByEmailIgnoreCase(e)` | `LOWER(email) = LOWER(?)` |
| `OrderBy` | `findByStatusOrderByCreatedAtDesc(s)` | `ORDER BY created_at DESC` |
| `Top` / `First` | `findTop5ByStatus(s)` | `LIMIT 5` |

O método pode combinar múltiplas keywords: `findByStatusAndTotalGreaterThanOrderByCreatedAtDesc`.

### Quando a derived query fica ilegível → `@Query` (nota 09)

Derived queries são ótimas para condições simples. Quando o nome do método começa a parecer uma frase em inglês de três linhas, é hora de usar `@Query` com JPQL ou SQL nativo. Ver [[03-Dominios/Tecnologia/Java/Persistência de dados/09 - Consultas com @Query — JPQL, native e @Modifying|Consultas com @Query]].

---

## Na prática

```java
import jakarta.persistence.Entity;
import jakarta.persistence.GeneratedValue;
import jakarta.persistence.GenerationType;
import jakarta.persistence.Id;
import jakarta.persistence.ManyToOne;
import java.math.BigDecimal;
import java.util.List;
import java.util.Optional;
import org.springframework.data.jpa.repository.JpaRepository;

// --- Entidade ---
@Entity
public class Order {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    private String externalId;
    private String status;
    private BigDecimal total;

    @ManyToOne
    private Customer customer;

    // getters e setters omitidos
}

// --- Repositório ---
public interface OrderRepository extends JpaRepository<Order, Long> {

    // Busca por campo simples
    List<Order> findByStatus(String status);

    // AND com comparação numérica
    List<Order> findByStatusAndTotalGreaterThan(String status, BigDecimal minTotal);

    // Busca por propriedade de associação (traversal)
    List<Order> findByCustomerEmail(String email);

    // COUNT derivado
    long countByStatus(String status);

    // EXISTS derivado — não carrega a entidade
    boolean existsByExternalId(String externalId);

    // Retorno Optional para consulta única
    Optional<Order> findByExternalId(String externalId);

    // Paginação
    org.springframework.data.domain.Page<Order> findByStatus(
            String status,
            org.springframework.data.domain.Pageable pageable);
}
```

O Spring Data registra `OrderRepository` como um bean gerenciado pelo container. Basta injetar normalmente:

```java
@Service
public class OrderService {

    private final OrderRepository orderRepository;

    public OrderService(OrderRepository orderRepository) {
        this.orderRepository = orderRepository;
    }

    public List<Order> pendingHighValue(BigDecimal threshold) {
        return orderRepository.findByStatusAndTotalGreaterThan("PENDING", threshold);
    }
}
```

---

## Armadilhas

### (1) Derived query longa e ilegível

Métodos como `findByCustomerCountryAndStatusInAndTotalGreaterThanOrderByCreatedAtDesc` compila e funciona, mas é praticamente impossível de revisar em code review.

```java
// Ruim — nome de 90 caracteres, difícil de auditar
List<Order> findByCustomerCountryAndStatusInAndTotalGreaterThanOrderByCreatedAtDesc(
    String country, List<String> statuses, BigDecimal min);

// Melhor — usar @Query com JPQL nomeado e legível
@Query("SELECT o FROM Order o WHERE o.customer.country = :country " +
       "AND o.status IN :statuses AND o.total > :min ORDER BY o.createdAt DESC")
List<Order> findHighValueByCountryAndStatuses(
    @Param("country") String country,
    @Param("statuses") List<String> statuses,
    @Param("min") BigDecimal min);
```

**Fix**: qualquer condição com mais de dois critérios ou com ordenação explícita é candidata a `@Query`.

### (2) Usar `findById` quando bastava `existsById`

`findById` executa `SELECT *` e hidrata a entidade inteira na memória só para verificar existência.

```java
// Ruim — busca toda a entidade para checar existência
boolean exists = orderRepository.findById(id).isPresent();

// Correto — SELECT COUNT(*) ou SELECT 1, sem hidratar objeto
boolean exists = orderRepository.existsById(id);
```

**Fix**: sempre preferir `existsById` (ou derived `existsBy...`) quando a entidade em si não é necessária.

### (3) Assumir que toda derived query é eficiente

O Spring gera JPQL, mas o JPQL precisa ser traduzido para SQL pelo Hibernate e executado no banco. Traversals como `findByCustomerAddressCityAndCustomerAddressCountry(...)` podem gerar JOINs implícitos ou subqueries ineficientes dependendo do mapeamento.

```java
// Parece simples, mas pode gerar JOIN não esperado
List<Order> findByCustomerAddressCity(String city);
```

**Fix**: ativar `spring.jpa.show-sql=true` (ou usar o log SQL do Hibernate) durante o desenvolvimento para inspecionar o SQL gerado. Para queries com JOINs complexos, usar `@Query` com `JOIN FETCH` explícito ou uma `@EntityGraph`.

---

## Em entrevista

### Frase pronta (inglês)

> "Spring Data JPA generates the repository implementation at runtime as a proxy bean — you only declare the interface. CRUD methods are inherited from `JpaRepository`, which sits at the top of the hierarchy above `CrudRepository` and `PagingAndSortingRepository`. For custom queries, Spring Data parses the method name and derives JPQL from it using a fixed set of keywords like `And`, `Or`, `Between`, `Containing`, and `OrderBy`. When the method name would become unreadable — more than two predicates, complex joins, or native SQL — we switch to `@Query` with explicit JPQL or SQL to keep the intent clear and the query auditable."

### Vocabulário

| Termo PT | Termo EN |
|---|---|
| Repositório | Repository |
| Consulta derivada | Derived query |
| Método de consulta | Query method |
| Paginação | Pagination |
| Palavra-chave | Keyword |
| Proxy | Proxy |
| Interface marcadora | Marker interface |
| Ordenação | Sorting |

---

## Veja também

- [[03-Dominios/Tecnologia/Java/Persistência de dados/01 - O que é a camada de persistência — Spring Data, JPA e Hibernate|O que é a camada de persistência]]
- [[03-Dominios/Tecnologia/Java/Persistência de dados/09 - Consultas com @Query — JPQL, native e @Modifying|Consultas com @Query]]
- [[03-Dominios/Tecnologia/Java/Spring Core e Boot/09 - AOP e proxies no Spring|AOP e proxies]]
- [[03-Dominios/Tecnologia/Java/Persistência de dados/index|Persistência de dados (MOC do galho)]]
- [[03-Dominios/Tecnologia/Java/index|Trilha Java]]
- [[03-Dominios/Tecnologia/Java/Dicionário de Java#JpaRepository|JpaRepository]]

---

## Referências

- Spring Data JPA Reference — Core Concepts: <https://docs.spring.io/spring-data/jpa/reference/repositories/core-concepts.html>
- Spring Data JPA Reference — Query Methods Details: <https://docs.spring.io/spring-data/jpa/reference/repositories/query-methods-details.html>
