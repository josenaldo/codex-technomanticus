---
title: "JPA — a especificação de persistência"
created: 2026-06-07
updated: 2026-06-09
type: concept
progress: backlog
status: seedling
publish: true
fase: Adepto
tags:
  - java
  - jakarta-ee
  - adepto
  - jpa
aliases:
  - "JPA"
  - "Jakarta Persistence"
  - "@Entity"
---

# JPA — a especificação de persistência

> [!abstract] TL;DR
> JPA é a **especificação** de mapeamento objeto-relacional da plataforma — **Jakarta Persistence 3.2** no Jakarta EE 11. Ela define o **contrato**: `@Entity`, `@Id`, relacionamentos, `EntityManager`, JPQL, `persistence.xml`. Hibernate e EclipseLink são **implementações** desse contrato. **JPA não é o Hibernate** — confundir os dois é o erro de vocabulário mais comum do ecossistema Java. Esta nota cobre o contrato; comportamento de provider, tuning e o ecossistema em volta são assunto do Galho 10.

---

## O que é

**Jakarta Persistence** (historicamente "JPA", de *Java Persistence API* — a sigla sobreviveu à renomeação) é a especificação que define como classes Java viram linhas de tabela e vice-versa. Como toda spec da plataforma (retomando [[01 - O modelo Jakarta EE — especificações e implementações]]), ela é um **documento + um conjunto de interfaces e annotations** no pacote `jakarta.persistence` — e **nenhuma linha de código que executa de verdade**.

Vamos cravar isso logo de cara, porque é o caso concreto mais famoso da dupla spec × provider:

> [!important] JPA não é o Hibernate
> **JPA é o contrato. Hibernate é uma implementação.** EclipseLink é outra (e é a implementação de referência da spec). Quando você escreve `@Entity`, `EntityManager`, JPQL — você está falando JPA. Quando o SQL é de fato gerado e executado, quem trabalha é o provider que você plugou. Dizer "uso Hibernate" quando se quis dizer "uso JPA" (ou vice-versa) é o equivalente a confundir a tomada com o eletrodoméstico.

A spec define, em essência:

- O **modelo de entidades**: o que é uma `@Entity`, quais requisitos a classe precisa cumprir, como declarar identidade (`@Id`) e mapeamento (colunas, tabelas, tipos);
- O **vocabulário de relacionamentos**: `@ManyToOne`, `@OneToMany`, `@ManyToMany`, `@OneToOne`, owning side, `mappedBy`;
- A **API de acesso**: `EntityManager`, `EntityManagerFactory`, o ciclo de vida da entidade (assunto da nota [[10 - EntityManager e o ciclo de vida da entidade]]);
- A **linguagem de consulta**: JPQL (orientada a entidades, não a tabelas) e a Criteria API;
- A **configuração**: a *persistence unit*, declarada em `persistence.xml` ou — novidade da 3.2 — programaticamente via `PersistenceConfiguration`.

No **Jakarta EE 11**, a versão vigente é a **Persistence 3.2**. Entre as novidades verificadas na spec: records como `@Embeddable`, suporte a `java.time.Instant` e `java.time.Year` como tipos básicos, operações de conjunto em JPQL (`UNION`/`INTERSECT`/`EXCEPT`), `getSingleResultOrNull()`, a API `SchemaManager` para DDL, `@EnumeratedValue` para mapeamento customizado de enums e a já citada `PersistenceConfiguration`.

---

## Por que importa

### A confusão mais comum do ecossistema

Pergunte a dez devs Java "o que é JPA?" e uma parte vai responder "é o Hibernate" — ou pior, "é o Spring Data". A confusão é compreensível (quase ninguém usa JPA sem um provider por trás, e muita gente só encontra JPA embrulhada pelo Spring Data — Galho 10), mas ela tem custo real:

- **Portabilidade**: quem conhece o contrato sabe o que funciona em *qualquer* provider e o que é extensão proprietária. Trocar de Hibernate para EclipseLink (ou rodar testes num provider e produção noutro) só é viável se o seu código fala a língua da spec.
- **Diagnóstico**: quando algo se comporta "estranho", saber se o comportamento é **mandatado pela spec** ou **decisão do provider** muda completamente onde você procura a resposta — no documento da spec ou na documentação do Hibernate/EclipseLink.
- **Vocabulário**: entidade, persistence unit, owning side, JPQL — esse é o vocabulário que todo o bloco de persistência usa. O [[03-Dominios/Tecnologia/Java/Persistência de dados/01 - O que é a camada de persistência — Spring Data, JPA e Hibernate|Galho 10]] constrói em cima dele; sem o contrato, o resto é cargo cult.

### Em entrevista

*"O que é JPA?"* é um **filtro de senioridade** disfarçado de pergunta básica. A resposta júnior é "uma biblioteca de banco de dados". A resposta senior distingue spec de provider em uma frase, cita o pacote `jakarta.persistence`, e sabe contar a história da renomeação de namespace que trouxe a spec até aqui ([[02 - De Java EE a Jakarta EE]]). É uma das raras perguntas em que 30 segundos de resposta revelam anos de entendimento.

---

## Como funciona

### `@Entity` — requisitos da classe e identidade

Uma entidade é uma classe anotada com `@Entity` que cumpre os requisitos do contrato. Conforme o javadoc da Persistence 3.2, a classe anotada **deve**:

- Ser uma classe **top-level não-`final`** ou uma **inner class `static`**;
- Ter um **construtor sem parâmetros `public` ou `protected`** (o provider precisa instanciar a entidade por reflexão ao materializar resultados);
- **Não** ter métodos `final` nem variáveis de instância persistentes `final`;
- **Não** ser enum, record ou interface (records podem ser `@Embeddable` na 3.2 — mas não `@Entity`);
- Ter identidade declarada: **`@Id`** (chave simples) ou `@EmbeddedId` (chave composta).

A identidade pode ser atribuída pela aplicação ou **gerada** via `@GeneratedValue`, cujas estratégias fazem parte do contrato (`jakarta.persistence.GenerationType`):

| Estratégia | O que a spec exige do provider | Tipos de PK suportados |
|---|---|---|
| `AUTO` | Provider escolhe a estratégia adequada ao tipo da PK | numéricos ou UUID/String |
| `IDENTITY` | PK atribuída por coluna identity do banco | `Long`, `Integer`, `long`, `int` |
| `SEQUENCE` | PK atribuída por sequence do banco (configurável com `@SequenceGenerator`) | `Long`, `Integer`, `long`, `int` |
| `TABLE` | PK atribuída usando uma tabela auxiliar para garantir unicidade | `Long`, `Integer`, `long`, `int` |
| `UUID` | PK gerada como UUID RFC 4122 (entrou na **spec 3.1**, Jakarta EE 10) | `java.util.UUID`, `String` |

Note o fraseado: *o que a spec exige do provider*. A spec define o **resultado contratual** (haverá uma PK única, vinda de tal mecanismo); *como* o provider implementa, otimiza ou agrupa essas gerações é território dele — e do Galho 10.

### Mapeamento básico — colunas, tabelas e tipos

Por padrão, JPA funciona por **convenção**: a entidade mapeia para uma tabela com o nome da classe, cada atributo persistente para uma coluna com o nome do atributo. As annotations de mapeamento são o mecanismo de **exceção à convenção**:

- **`@Table(name = "...")`** — quando o nome da tabela difere do nome da classe (na 3.2, `@Table` ganhou suporte a `comment` e check constraints no contrato);
- **`@Column`** — nome, `nullable`, `length`, `unique`, `precision`/`scale` da coluna;
- **`@Transient`** — exclui um atributo da persistência (campo calculado, cache local, etc.);
- **`@Enumerated`** — controla como enums são gravados: `EnumType.ORDINAL` (posição — o default, e uma armadilha clássica) ou `EnumType.STRING` (nome da constante). A 3.2 adiciona `@EnumeratedValue` para mapear um campo customizado do enum.

Sobre tipos temporais: a spec 3.2 lista como **tipos básicos** (mapeáveis sem conversão) `LocalDate`, `LocalTime`, `LocalDateTime`, `OffsetTime`, `OffsetDateTime` e — novidades da 3.2 — **`Instant`** e **`Year`**, todos de `java.time`. Ou seja: `java.time` é cidadão de primeira classe no contrato; os antigos `@Temporal` + `java.util.Date` são legado.

### Relacionamentos — o vocabulário da spec

Relacionamentos entre entidades são declarados com quatro annotations, e aqui o conceito central do contrato é o **owning side** (lado dono):

> [!important] Owning side: quem escreve a FK
> Todo relacionamento bidirecional tem **um** lado dono — o lado cujo estado o provider lê para escrever a foreign key (ou a join table) no banco. O outro lado é o **inverso**, marcado com `mappedBy`, e é **somente leitura** do ponto de vista da persistência. Mudar só o lado inverso **não altera nada no banco**.

- **`@ManyToOne`** — o lado "muitos" aponta para o "um". É **sempre o owning side** num bidirecional com `@OneToMany`: a FK mora na tabela do lado muitos.
- **`@OneToMany(mappedBy = "...")`** — o lado "um" enxerga a coleção. Num bidirecional, declara `mappedBy` apontando para o atributo dono do outro lado. Sem `mappedBy`, a spec trata como **unidirecional** — e o mapeamento default usa join table (veja Armadilha 3).
- **`@ManyToMany`** — junção N:N via join table (`@JoinTable` configura nome e colunas). Um lado é dono, o outro usa `mappedBy`.
- **`@OneToOne`** — 1:1; o owning side é o que carrega a FK (`@JoinColumn`).

Todas aceitam o atributo **`fetch`** (`FetchType.LAZY` ou `FetchType.EAGER`), que **existe no contrato** com defaults definidos pela spec: `@ManyToOne` e `@OneToOne` são `EAGER` por default; `@OneToMany` e `@ManyToMany` são `LAZY`. Aqui esta nota **para de propósito**: o que fazer com isso — estratégias de carregamento, consequências de performance e os padrões/anti-padrões associados — é assunto do [[03-Dominios/Tecnologia/Java/Persistência de dados/07 - Fetch strategies — LAZY, EAGER e a LazyInitializationException|Galho 10]]. No nível do contrato, basta saber que o atributo existe e quais são os defaults.

### Persistence unit — `persistence.xml`

Entidades anotadas não fazem nada sozinhas. Quem dá vida a elas é a **persistence unit**: a unidade de configuração que agrupa um conjunto de entidades + um provider + um datasource + propriedades. A forma clássica de declará-la é o **`persistence.xml`** (em `META-INF/`), cujo schema na 3.2 é o `persistence_3_2.xsd` sob o namespace `https://jakarta.ee/xml/ns/persistence`.

Os elementos centrais de uma `<persistence-unit>`:

| Elemento | Papel |
|---|---|
| `name` (atributo) | Identifica a unit — é o nome que você referencia ao obter o `EntityManagerFactory` |
| `<provider>` | Classe do provider (opcional se há só um no classpath) |
| `<jta-data-source>` / `<non-jta-data-source>` | JNDI do datasource, conforme o tipo de transação |
| `<class>` | Entidades incluídas (em ambiente EE, o container geralmente as descobre sozinho) |
| `<properties>` | Propriedades padronizadas (`jakarta.persistence.*`) e específicas do provider |
| `transaction-type` (atributo) | `JTA` (transação gerenciada pela plataforma) ou `RESOURCE_LOCAL` (você controla via `EntityTransaction`) |

A distinção **JTA × resource-local** é só um teaser aqui: o ciclo do `EntityManager` é a nota [[10 - EntityManager e o ciclo de vida da entidade]], e transações na plataforma são a nota [[11 - JTA — transações na plataforma]].

Novidade da 3.2: a **`PersistenceConfiguration`** — uma API fluente para construir a persistence unit **programaticamente**, sem XML:

```java
EntityManagerFactory emf = new PersistenceConfiguration("orders")
        .nonJtaDataSource("java:global/jdbc/OrdersDB")
        .managedClass(Order.class)
        .managedClass(OrderItem.class)
        .createEntityManagerFactory();
```

Pelo javadoc, ela é voltada a persistence units no estilo Java SE (mesmo quando usadas dentro de um ambiente EE) — o `persistence.xml` continua sendo o caminho canônico no container.

### Spec vs provider na prática

A linha que separa o portável do proprietário:

| Portável (contrato) | Extensão (provider) |
|---|---|
| `jakarta.persistence.*` — annotations, `EntityManager`, JPQL, Criteria | Qualquer import `org.hibernate.*` ou `org.eclipse.persistence.*` |
| Estratégias de `@GeneratedValue` e seus tipos de PK | Geradores customizados do provider |
| Propriedades `jakarta.persistence.*` no `persistence.xml` | Propriedades `hibernate.*` / `eclipselink.*` |
| Defaults de `fetch` definidos pela spec | Tudo que vai além do default — Galho 10 |
| JPQL conforme o capítulo de query language da spec | Dialetos, funções nativas, hints proprietários |

Regra prática de Adepto: **escreva contra `jakarta.persistence.*` e trate cada import do provider como dívida consciente** — às vezes vale a pena, mas precisa ser uma decisão, não um acidente. Hibernate e EclipseLink ficam aqui como nomes citados; o que cada um faz além do contrato é assunto do Galho 10.

---

## Na prática

O trio `Customer` / `Order` / `OrderItem`, mapeado conforme o contrato:

```java
import jakarta.persistence.Column;
import jakarta.persistence.Entity;
import jakarta.persistence.EnumType;
import jakarta.persistence.Enumerated;
import jakarta.persistence.GeneratedValue;
import jakarta.persistence.GenerationType;
import jakarta.persistence.Id;
import jakarta.persistence.JoinColumn;
import jakarta.persistence.ManyToOne;
import jakarta.persistence.OneToMany;
import jakarta.persistence.Table;
import jakarta.persistence.Transient;

import java.math.BigDecimal;
import java.time.OffsetDateTime;
import java.util.ArrayList;
import java.util.List;
import java.util.UUID;

@Entity
@Table(name = "customers")
public class Customer {

    @Id
    @GeneratedValue(strategy = GenerationType.UUID) // contrato: UUID RFC 4122, spec 3.1+
    private UUID id;

    @Column(nullable = false, length = 120)
    private String name;

    @Column(nullable = false, unique = true, length = 254)
    private String email;

    protected Customer() { } // exigência da spec: no-args public/protected

    public Customer(String name, String email) {
        this.name = name;
        this.email = email;
    }

    public UUID getId() { return id; }
    public String getName() { return name; }
    public String getEmail() { return email; }
}
```

```java
import jakarta.persistence.Column;
import jakarta.persistence.Entity;
import jakarta.persistence.EnumType;
import jakarta.persistence.Enumerated;
import jakarta.persistence.GeneratedValue;
import jakarta.persistence.GenerationType;
import jakarta.persistence.Id;
import jakarta.persistence.JoinColumn;
import jakarta.persistence.ManyToOne;
import jakarta.persistence.OneToMany;
import jakarta.persistence.Table;
import jakarta.persistence.Transient;

import java.math.BigDecimal;
import java.time.OffsetDateTime;
import java.util.ArrayList;
import java.util.List;

@Entity
@Table(name = "orders")
public class Order {

    public enum Status { OPEN, PAID, SHIPPED, CANCELED }

    @Id
    @GeneratedValue(strategy = GenerationType.SEQUENCE)
    private Long id;

    // Owning side do Order→Customer: a FK customer_id mora na tabela orders.
    @ManyToOne
    @JoinColumn(name = "customer_id", nullable = false)
    private Customer customer;

    // Lado INVERSO do Order↔OrderItem: mappedBy aponta pro atributo dono
    // ("order" em OrderItem). Este lado NÃO escreve nada no banco.
    @OneToMany(mappedBy = "order")
    private List<OrderItem> items = new ArrayList<>();

    @Enumerated(EnumType.STRING) // STRING, não o default ORDINAL — ver Armadilhas
    @Column(nullable = false, length = 20)
    private Status status = Status.OPEN;

    @Column(nullable = false)
    private OffsetDateTime createdAt = OffsetDateTime.now(); // java.time é tipo básico na spec

    @Transient // calculado, não persiste
    private BigDecimal cachedTotal;

    protected Order() { }

    public Order(Customer customer) {
        this.customer = customer;
    }

    public Long getId() { return id; }
    public Customer getCustomer() { return customer; }
    public List<OrderItem> getItems() { return items; }
    public Status getStatus() { return status; }
}
```

```java
import jakarta.persistence.Column;
import jakarta.persistence.Entity;
import jakarta.persistence.GeneratedValue;
import jakarta.persistence.GenerationType;
import jakarta.persistence.Id;
import jakarta.persistence.JoinColumn;
import jakarta.persistence.ManyToOne;
import jakarta.persistence.Table;

import java.math.BigDecimal;

@Entity
@Table(name = "order_items")
public class OrderItem {

    @Id
    @GeneratedValue(strategy = GenerationType.SEQUENCE)
    private Long id;

    // OWNING SIDE do relacionamento Order↔OrderItem:
    // é o estado DESTE atributo que o provider lê pra gravar a FK order_id.
    @ManyToOne
    @JoinColumn(name = "order_id", nullable = false)
    private Order order;

    @Column(nullable = false, length = 80)
    private String productName;

    @Column(nullable = false)
    private int quantity;

    @Column(nullable = false, precision = 10, scale = 2)
    private BigDecimal unitPrice;

    protected OrderItem() { }

    public OrderItem(Order order, String productName, int quantity, BigDecimal unitPrice) {
        this.order = order;
        this.productName = productName;
        this.quantity = quantity;
        this.unitPrice = unitPrice;
    }

    public Long getId() { return id; }
    public Order getOrder() { return order; }
}
```

E o `persistence.xml` mínimo (em `META-INF/persistence.xml`), no schema 3.2:

```xml
<?xml version="1.0" encoding="UTF-8"?>
<persistence xmlns="https://jakarta.ee/xml/ns/persistence"
             xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
             xsi:schemaLocation="https://jakarta.ee/xml/ns/persistence
                                 https://jakarta.ee/xml/ns/persistence/persistence_3_2.xsd"
             version="3.2">

    <persistence-unit name="orders" transaction-type="JTA">
        <!-- O provider (Hibernate/EclipseLink) entra aqui — comportamento
             além do contrato é assunto do Galho 10. -->
        <jta-data-source>java:app/jdbc/OrdersDB</jta-data-source>
        <class>com.example.orders.Customer</class>
        <class>com.example.orders.Order</class>
        <class>com.example.orders.OrderItem</class>
        <properties>
            <!-- só propriedades jakarta.persistence.* são portáveis -->
        </properties>
    </persistence-unit>

</persistence>
```

Tudo acima é contrato puro: roda igual em qualquer provider compatível com Persistence 3.2.

---

## Armadilhas

### (1) Entidade sem construtor no-args — o provider não consegue instanciar

A spec **exige** construtor sem parâmetros `public` ou `protected`. Se você cria só o construtor "de negócio", o compilador não gera o default — e o provider falha ao materializar a entidade vinda do banco (tipicamente com uma exceção de instanciação na primeira query).

```java
@Entity
public class Customer {
    @Id @GeneratedValue(strategy = GenerationType.UUID)
    private UUID id;
    private String name;

    public Customer(String name) { this.name = name; } // único construtor: viola a spec
}
```

**Fix:** declare o no-args explicitamente — `protected` é o sweet spot (satisfaz a spec sem expor um construtor vazio na API pública da classe):

```java
protected Customer() { } // pro provider; o construtor de negócio continua existindo
```

### (2) `equals`/`hashCode` com id gerado ou campos mutáveis — quebra em `Set` antes do persist

O dilema é real e não tem resposta única — apresentando honestamente:

- **Baseado no `@Id` gerado:** antes do persist, o id é `null`. Duas entidades novas são "iguais" (ou o `hashCode` muda quando o id é atribuído) — e um `HashSet` que recebeu a entidade antes do persist pode "perdê-la" depois, porque ela foi guardada no bucket do hash antigo.
- **Baseado em campos de negócio mutáveis:** mesmo problema, deslocado — editar o campo depois de inserir num `Set` corrompe o bucket.

```java
Set<Order> orders = new HashSet<>();
Order order = new Order(customer);
orders.add(order);              // hashCode com id == null
em.persist(order);              // provider atribui o id...
orders.contains(order);         // ...e isto pode retornar false (bucket errado)
```

**Fix:** estratégia **consciente**, não dogma. Opções defensáveis: (a) **natural key imutável** (ex.: `email` de `Customer`, se o domínio garante imutabilidade) — a mais limpa quando existe; (b) id atribuído pela aplicação (ex.: `UUID` gerado no construtor, sem `@GeneratedValue`) — `equals`/`hashCode` estáveis desde o `new`; (c) não sobrescrever e não usar entidades novas em `Set`/`Map` antes do persist. O importante em entrevista e em code review é **saber explicar o trade-off escolhido**.

### (3) Esquecer `mappedBy` — join table (ou FK duplicada) inesperada

Você declara os dois lados do Order↔OrderItem, mas esquece o `mappedBy`:

```java
@Entity
public class Order {
    @OneToMany                       // sem mappedBy: a spec trata como
    private List<OrderItem> items;   // relacionamento SEPARADO, unidirecional
}

@Entity
public class OrderItem {
    @ManyToOne
    private Order order;             // outro relacionamento, na visão do provider
}
```

Resultado: em vez de um bidirecional com uma FK, o provider enxerga **dois relacionamentos independentes** — e o `@OneToMany` unidirecional mapeia por default via **join table** (`orders_order_items`), que aparece "do nada" no schema, além da FK do `@ManyToOne`. Estado duplicado, escrita inconsistente.

**Fix:** owning side **explícito** — o inverso declara `mappedBy` apontando para o atributo dono:

```java
@OneToMany(mappedBy = "order")   // "order" = nome do atributo em OrderItem
private List<OrderItem> items;
```

E lembre: ao montar o grafo em memória, **sete o lado dono** (`item.setOrder(order)`) — é ele que o provider lê.

### (4) Anotar `@Entity` e esperar que "funcione" — sem persistence unit não há persistência

`@Entity` sozinha é só metadado. Se a classe não pertence a nenhuma persistence unit (não está no `persistence.xml`, não foi descoberta pelo container, não foi registrada via `PersistenceConfiguration`), o provider **não a conhece**: a falha típica é uma exceção de "unknown entity" / entidade não mapeada na primeira operação, ou a unit nem sobe.

```text
# Sintoma típico (mensagem varia por provider):
Order is not a known entity type / Not an entity: com.example.orders.Order
```

**Fix:** garanta a entidade dentro de uma unit — `<class>com.example.orders.Order</class>` no `persistence.xml` (ou descoberta automática no container EE, ou `managedClass(Order.class)` na `PersistenceConfiguration`). Annotation declara; **a persistence unit é quem ativa**.

### (5) `@Enumerated` no default `ORDINAL` — reordenou o enum, corrompeu o banco

Sem `@Enumerated`, a spec grava enums por **posição** (`ORDINAL`). Inserir uma constante no meio do enum reinterpreta silenciosamente todos os dados já gravados:

```java
public enum Status { OPEN, PAID, SHIPPED }          // PAID grava 1
public enum Status { OPEN, REVIEW, PAID, SHIPPED }  // agora 1 significa REVIEW…
```

**Fix:** `@Enumerated(EnumType.STRING)` por padrão em código novo; na 3.2, `@EnumeratedValue` permite mapear um campo estável do próprio enum (ex.: um código `int` imutável) — o melhor dos dois mundos quando o tamanho da coluna importa.

---

## Em entrevista

### Frase pronta (inglês)

> "JPA — Jakarta Persistence, version 3.2 in Jakarta EE 11 — is the persistence *specification*, not a framework: it defines the contract — `@Entity`, the `EntityManager` API, JPQL, relationship mappings — while providers like Hibernate and EclipseLink supply the actual implementation. I write my code against `jakarta.persistence.*` so it stays portable, and I treat any provider-specific import as a conscious, documented trade-off. At the mapping level, the key concept is the owning side: in a bidirectional association, only the side without `mappedBy` writes the foreign key, so I always set the owning side when wiring the object graph. I also make sure every entity honors the spec's class requirements — a public or protected no-args constructor, non-final class — because that's what allows any compliant provider to instantiate it."

### Vocabulário

| Termo PT | Termo EN |
|---|---|
| especificação de persistência | persistence specification |
| entidade | entity |
| chave primária gerada | generated primary key |
| lado dono (do relacionamento) | owning side |
| lado inverso | inverse side |
| unidade de persistência | persistence unit |
| mapeamento objeto-relacional | object-relational mapping (ORM) |
| provedor de persistência | persistence provider |

---

## Veja também

- [[01 - O modelo Jakarta EE — especificações e implementações]] — o padrão spec × provider de que JPA é o caso mais famoso
- [[10 - EntityManager e o ciclo de vida da entidade]] — a API de acesso e os estados da entidade
- [[11 - JTA — transações na plataforma]] — o lado transacional do `transaction-type="JTA"`
- [[03-Dominios/Tecnologia/Java/Linguagem e sintaxe moderna/11 - Annotations|Annotations (Galho 1)]] — a mecânica por trás de `@Entity` e companhia
- [[03-Dominios/Tecnologia/Java/Jakarta EE/index|Jakarta EE (MOC do galho)]]
- [[03-Dominios/Tecnologia/Java/index|Trilha Java]]
- [[03-Dominios/Tecnologia/Java/Dicionário de Java#JPA (Jakarta Persistence)|JPA (Dicionário)]]
- [[03-Dominios/Tecnologia/Java/Dicionário de Java#entity (JPA)|entity (Dicionário)]]
- [[03-Dominios/Tecnologia/Java/Dicionário de Java#persistence unit / persistence.xml|persistence unit (Dicionário)]]

---

## Referências

- [Jakarta Persistence 3.2 — página da especificação](https://jakarta.ee/specifications/persistence/3.2/) — acesso em 2026-06-07
- [Jakarta Persistence 3.2 — documento da spec (HTML)](https://jakarta.ee/specifications/persistence/3.2/jakarta-persistence-spec-3.2) — acesso em 2026-06-07
- [Jakarta Persistence 3.2 — apidocs `jakarta.persistence`](https://jakarta.ee/specifications/persistence/3.2/apidocs/) — acesso em 2026-06-07 (`@Entity`, `GenerationType`, `PersistenceConfiguration` verificados)
- [Jakarta Persistence 3.1 — página da especificação](https://jakarta.ee/specifications/persistence/3.1/) — acesso em 2026-06-07 (confirmação: `GenerationType.UUID` entrou na 3.1)
- [Jakarta XML schemas — namespace persistence](https://jakarta.ee/xml/ns/persistence/) — acesso em 2026-06-07 (`persistence_3_2.xsd`)
