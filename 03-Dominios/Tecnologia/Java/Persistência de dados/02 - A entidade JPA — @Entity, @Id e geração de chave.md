---
title: "A entidade JPA — @Entity, @Id e geração de chave"
created: 2026-06-09
updated: 2026-06-09
type: concept
progress: backlog
status: seedling
publish: true
fase: Iniciado
tags:
  - java
  - persistencia
  - iniciado
  - entidade
  - jpa
aliases:
  - "entidade JPA"
  - "@Entity"
---

# A entidade JPA — @Entity, @Id e geração de chave

> [!abstract] TL;DR
> Uma classe vira tabela colocando `@Entity` + `@Id` nela — dois metadados obrigatórios que dizem ao Hibernate "este objeto tem representação no banco". `@GeneratedValue` define *como* a PK é gerada: **SEQUENCE** é o default recomendado (permite batch); **IDENTITY** bloqueia batch inserts e deve ser evitado em workloads de escrita. A estratégia **UUID** chegou na **JPA 3.1** (Jakarta EE 10). A entidade precisa de construtor sem-arg (pode ser `protected`) e `equals`/`hashCode` baseados em business key — nunca em `@Data` do Lombok nem no id gerado (que é `null` antes do `save`).

## O que é

Uma entidade JPA é uma classe Java mapeada a uma tabela de banco de dados. Cada instância persistida corresponde a uma linha; cada campo anotado (ou mapeado por convenção) corresponde a uma coluna. O Hibernate usa os metadados de anotação para construir o schema, formular SQL e gerenciar o ciclo de vida do objeto dentro do persistence context.

A anotação mínima é `@Entity` na classe e `@Id` num campo — tudo o mais (`@Table`, `@Column`, `@GeneratedValue`) é configuração opcional sobre esse núcleo.

## Por que importa

A entidade é o bloco fundamental de toda a camada de persistência. Sem entendê-la bem, nenhum repositório, nenhuma query JPQL e nenhuma transação faz sentido. Em entrevistas técnicas para vagas sênior três pontos costumam aparecer juntos:

- qual estratégia de geração de ID escolher e por quê;
- como implementar `equals`/`hashCode` sem quebrar coleções ou lazy loading;
- por que `record` do Java não pode ser entidade.

## Como funciona

### `@Entity`, `@Table` e `@Column`: o mapeamento básico

`@Entity` sinaliza ao provider JPA que a classe é gerenciável. Por padrão, o nome da tabela é o nome simples da classe (case-insensitive no DDL). `@Table(name = "...")` sobrescreve esse default.

`@Column` personaliza nome, nullability e tamanho da coluna. Sem ela, o Hibernate deriva o nome da coluna a partir do nome do campo (snake_case no Hibernate 6 com `PhysicalNamingStrategyStandardImpl`).

```java
import jakarta.persistence.*;

@Entity
@Table(name = "orders")
public class Order {

    @Id
    @GeneratedValue(strategy = GenerationType.SEQUENCE, generator = "order_seq")
    @SequenceGenerator(name = "order_seq", sequenceName = "order_seq", allocationSize = 50)
    private Long id;

    @Column(name = "external_id", nullable = false, unique = true)
    private UUID externalId;

    @Column(nullable = false)
    private String status;

    // construtor sem-arg obrigatório (pode ser protected)
    protected Order() {}

    public Order(String status) {
        this.externalId = UUID.randomUUID();
        this.status = status;
    }
}
```

### `@Id` e `@GeneratedValue`: quando usar cada estratégia

`@Id` marca o campo que mapeia a chave primária. `@GeneratedValue` instrui o provider a gerar o valor automaticamente. As cinco estratégias disponíveis são:

| Estratégia | Mecanismo | Quando usar |
|---|---|---|
| `SEQUENCE` | Sequence de banco | **Default recomendado**; compatível com batch; exige suporte a sequences (PostgreSQL, Oracle, H2) |
| `IDENTITY` | Auto-increment / serial | MySQL/MariaDB legado; **bloqueia batch inserts** — evitar em workload write-heavy |
| `TABLE` | Tabela de contador gerenciada pelo provider | Portável, mas lento; raramente justificado |
| `AUTO` | Provider escolhe SEQUENCE ou TABLE | Conveniente no dev; pode variar entre ambientes |
| `UUID` | UUID gerado pelo provider | **Adicionado na JPA 3.1** (Jakarta EE 10); dispensa sequence de banco; bom para IDs distribuídos |

A estratégia **UUID foi introduzida na JPA 3.1** (especificação publicada junto ao Jakarta EE 10) e permite declarar `@GeneratedValue(strategy = GenerationType.UUID)` com campo do tipo `java.util.UUID` sem dependência de extensão proprietária.

```java
// Exemplo com UUID (JPA 3.1+, Spring Boot 3+)
@Id
@GeneratedValue(strategy = GenerationType.UUID)
private UUID id;
```

Para SEQUENCE, o parâmetro `allocationSize` controla quantos valores são pré-alocados em memória por consulta ao banco. O default do Hibernate é 50, o que reduz drasticamente o número de round-trips em bulk inserts. Um `allocationSize = 1` força um hit ao banco para cada novo ID — nunca faça isso em produção sem justificativa.

### `equals`/`hashCode` por business key (nunca `@Data` do Lombok)

O `id` gerado pelo banco é `null` até o `EntityManager.persist()` confirmar o insert. Implementar `equals`/`hashCode` sobre ele significa que dois objetos `new Order()` antes do save são considerados iguais — o que quebra `Set<Order>` e qualquer estrutura hash.

A solução canônica é usar uma **business key** imutável (geralmente um UUID atribuído no construtor do objeto, antes de qualquer persistência):

```java
@Override
public boolean equals(Object o) {
    if (this == o) return true;
    if (!(o instanceof Order other)) return false;
    return externalId != null && externalId.equals(other.externalId);
}

@Override
public int hashCode() {
    // constante garante comportamento estável antes e depois do persist
    return getClass().hashCode();
}
```

Essa abordagem é consistente ao longo de todo o ciclo de vida da entidade: antes do save, depois do save, detached e reattached.

### Por que `record` não serve como entidade

Java records são imutáveis por design: todos os campos são `final`, não há setters e não há construtor sem-arg padrão. O provider JPA precisa de:

1. **Construtor sem-arg** para instanciar a entidade ao carregar do banco via reflection.
2. **Campos mutáveis** (ou pelo menos acessíveis por reflection sem `final`) para que o persistence context injete os valores após a consulta.
3. **Capacidade de proxy** (subclassing pelo Hibernate) para lazy loading — `final class` impede isso.

Records violam os três requisitos, portanto não podem ser anotados com `@Entity`.

## Na prática

Entidade `Order` com SEQUENCE, business key como `externalId` e `equals`/`hashCode` corretos:

```java
import jakarta.persistence.*;
import java.util.Objects;
import java.util.UUID;

@Entity
@Table(name = "orders")
public class Order {

    @Id
    @GeneratedValue(strategy = GenerationType.SEQUENCE, generator = "order_seq")
    @SequenceGenerator(
        name        = "order_seq",
        sequenceName = "order_seq",
        allocationSize = 50
    )
    private Long id;

    @Column(name = "external_id", nullable = false, unique = true, updatable = false)
    private UUID externalId;

    @Column(nullable = false)
    private String status;

    @Column(name = "customer_id", nullable = false)
    private Long customerId;

    protected Order() {}

    public Order(String status, Long customerId) {
        this.externalId  = UUID.randomUUID();   // business key gerada na construção
        this.status      = status;
        this.customerId  = customerId;
    }

    // getters omitidos por brevidade

    @Override
    public boolean equals(Object o) {
        if (this == o) return true;
        if (!(o instanceof Order other)) return false;
        return externalId != null && externalId.equals(other.externalId);
    }

    @Override
    public int hashCode() {
        return getClass().hashCode();
    }

    @Override
    public String toString() {
        return "Order{externalId=" + externalId + ", status='" + status + "'}";
    }
}
```

> [!tip] Por que `Long id` + `UUID externalId`?
> O `Long` como PK interna maximiza performance de JOIN e índice no banco. O `UUID externalId` serve de chave de negócio (exposta na API) — desacopla o id interno do id público e evita enumeração.

## Armadilhas

### 1. `@Data` do Lombok em entidades JPA

`@Data` gera `equals`/`hashCode` baseados em todos os campos, incluindo relacionamentos lazy (`@OneToMany`, `@ManyToOne`). Isso provoca:

- **`LazyInitializationException`** ao chamar `hashCode()` fora de uma sessão aberta (o Hibernate tenta inicializar a coleção lazy).
- `toString()` recursivo com relacionamentos bidirecionais → `StackOverflowError`.

**Fix**: usar apenas `@Getter`/`@Setter`/`@NoArgsConstructor` separadamente e implementar `equals`/`hashCode` manualmente ou com `@EqualsAndHashCode(onlyExplicitlyIncluded = true)` marcando só a business key.

### 2. `equals`/`hashCode` baseados no id gerado

```java
// ERRADO — id é null antes do persist
@Override
public boolean equals(Object o) {
    if (!(o instanceof Order other)) return false;
    return Objects.equals(id, other.id); // null == null → true para qualquer par de objetos novos
}
```

Consequência: dois `new Order()` distintos são considerados iguais, quebrando `Set<Order>` e detecção de duplicatas no persistence context.

**Fix**: usar business key imutável (ver seção acima) ou o padrão de `hashCode` constante com `equals` por business key.

### 3. Estratégia IDENTITY em workloads write-heavy

Com `IDENTITY`, o banco só gera e retorna o ID após o `INSERT` concluir. O Hibernate **não consegue** acumular inserts em batch porque precisa do ID de volta antes de continuar. Em workloads que inserem centenas de registros por transação, isso eleva linearmente o número de round-trips.

```text
Hibernate com IDENTITY (batch de 100 registros):
  → 100 INSERTs individuais + 100 SELECT LAST_INSERT_ID()

Hibernate com SEQUENCE (allocationSize=50, batch de 100):
  → 2 chamadas à sequence + 1 batch INSERT com 100 linhas
```

**Fix**: migrar para `SEQUENCE` (PostgreSQL, H2, Oracle) ou, em MySQL, usar `TABLE` como alternativa menos pior — e configurar `spring.jpa.properties.hibernate.jdbc.batch_size`.

## Em entrevista

### Frase pronta (inglês)

"For primary key generation, I default to `SEQUENCE` with a tuned `allocationSize` because it's the only strategy that allows Hibernate to batch inserts — `IDENTITY` forces a round-trip per row, which kills throughput at scale. Since JPA 3.1, there's also a `UUID` strategy for distributed systems where you don't want a database sequence at all. For `equals` and `hashCode`, I never use the generated database ID because it's `null` before the entity is persisted; instead, I assign a UUID business key in the constructor and base equality on that — it stays stable across the entire object lifecycle, including detached state."

### Vocabulário

| Termo PT | Termo EN |
|---|---|
| Entidade | Entity |
| Chave primária | Primary key |
| Geração de chave | Key generation / ID generation |
| Sequência | Sequence |
| Chave de negócio | Business key |
| Mapeamento | Mapping |
| Construtor sem-arg | No-arg constructor |
| Tamanho de alocação | Allocation size |
| Inserção em lote | Batch insert |
| Chave única universal | UUID (Universally Unique Identifier) |

## Veja também

- [[03-Dominios/Tecnologia/Java/Persistência de dados/01 - O que é a camada de persistência — Spring Data, JPA e Hibernate|O que é a camada de persistência]]
- [[03-Dominios/Tecnologia/Java/Persistência de dados/03 - O persistence context e os estados da entidade|O persistence context e os estados da entidade]]
- [[03-Dominios/Tecnologia/Java/Jakarta EE/09 - JPA — a especificação de persistência|JPA (a spec define as anotações)]]
- [[03-Dominios/Tecnologia/Java/Linguagem e sintaxe moderna/11 - Annotations|Annotations]]
- [[03-Dominios/Tecnologia/Java/Persistência de dados/index|Persistência de dados (MOC do galho)]]
- [[03-Dominios/Tecnologia/Java/index|Trilha Java]]
- [[03-Dominios/Tecnologia/Java/Dicionário de Java#@GeneratedValue|@GeneratedValue]]

## Referências

- Jakarta Persistence 3.1 Specification — <https://jakarta.ee/specifications/persistence/3.1/>
- Hibernate ORM User Guide — Identifiers: <https://docs.hibernate.org/orm/current/userguide/html_single/Hibernate_User_Guide.html>
