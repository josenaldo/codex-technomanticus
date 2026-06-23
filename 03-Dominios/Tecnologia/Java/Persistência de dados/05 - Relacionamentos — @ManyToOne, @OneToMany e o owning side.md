---
title: "Relacionamentos — @ManyToOne, @OneToMany e o owning side"
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
  - relacionamentos
aliases:
  - "relacionamentos JPA"
  - "owning side"
---

# Relacionamentos — @ManyToOne, @OneToMany e o owning side

> [!abstract] TL;DR
> O par `@ManyToOne` / `@OneToMany` modela um relacionamento um-para-muitos entre duas entidades. O **owning side** (`@ManyToOne`) é o lado que carrega a chave estrangeira no banco e controla o que o JPA persiste; o **inverse side** (`@OneToMany(mappedBy = "...")`) é apenas um espelho navegacional — o JPA ignora ele para DML. Em relações bidirecionais, **helper methods** (`addOrder` / `removeOrder`) são obrigatórios para manter os dois lados sincronizados em memória antes do flush.

---

## O que é

Em JPA, dois objetos se relacionam quando uma entidade referencia outra como campo. Para persistir essa relação corretamente, o mapeamento precisa indicar **quem carrega a chave estrangeira (FK)** e, em relações bidirecionais, **qual lado é o espelho**.

Dois conceitos fundamentais:

- **Owning side (lado dono):** o lado que possui a coluna FK no banco. Qualquer mudança na referência só é persistida se feita aqui.
- **Inverse side (lado inverso):** declarado com `mappedBy`; existe apenas para navegação em memória — o JPA não gera DML baseado neste lado.

No modelo um-para-muitos (`Customer` ↔ `Order`):

| Lado | Annotation | Tem FK? | Controla DML? |
|---|---|---|---|
| `Order.customer` | `@ManyToOne` | Sim | Sim |
| `Customer.orders` | `@OneToMany(mappedBy)` | Não | Não |

---

## Por que importa

Confundir owning side com inverse side é a **fonte número 1 de bugs de mapeamento JPA**:

- Esquecer `mappedBy` faz o JPA criar uma *join table* ou uma segunda FK silenciosamente.
- Salvar apenas o lado `@OneToMany` (inverse) **não persiste nada** no banco — a relação é ignorada.
- O tema aparece em praticamente toda entrevista de nível pleno ou sênior que envolve JPA/Hibernate.
- Compreender owning side também é pré-requisito para entender fetch strategies (N+1) e cascade — temas das notas 06 e 07.

---

## Como funciona

### Owning side (`@ManyToOne`) — quem tem a FK

```java
import jakarta.persistence.*;

@Entity
@Table(name = "orders")
public class Order {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    // Owning side: esta coluna existe na tabela `orders`
    @ManyToOne(fetch = FetchType.LAZY)
    @JoinColumn(name = "customer_id", nullable = false)
    private Customer customer;

    // outros campos...
}
```

O JPA persiste ou atualiza a FK `customer_id` sempre que `order.setCustomer(c)` for chamado e a transação fizer flush.

### Inverse side (`mappedBy`) — o espelho navegacional

```java
import jakarta.persistence.*;
import java.util.ArrayList;
import java.util.List;

@Entity
@Table(name = "customers")
public class Customer {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    // Inverse side: mappedBy aponta pro campo `customer` em Order
    @OneToMany(mappedBy = "customer", cascade = CascadeType.ALL, orphanRemoval = true)
    private List<Order> orders = new ArrayList<>();

    // outros campos...
}
```

O valor de `mappedBy` deve ser o **nome exato do campo** no owning side. Qualquer erro de digitação lança uma exceção na inicialização do `EntityManagerFactory`.

### `@JoinColumn` e o lado dono

`@JoinColumn` é opcional: sem ele, o Hibernate gera um nome de coluna por convenção (`<nome_campo>_<pk_alvo>` → `customer_id`). Com ele, o nome é explícito e o contrato fica documentado no código.

Atributos relevantes:

| Atributo | Padrão | Descrição |
|---|---|---|
| `name` | convenção | nome da coluna FK na tabela |
| `nullable` | `true` | se a FK pode ser nula |
| `insertable` / `updatable` | `true` | controle fino em mapeamentos compostos |

### Bidirecional + helper methods (`addOrder` / `removeOrder`)

Sem helper methods, manter os dois lados sincronizados fica a cargo do código de negócio — e erros são frequentes. A prática recomendada é encapsular a sincronização dentro da entidade:

```java
import jakarta.persistence.*;
import java.util.ArrayList;
import java.util.List;

@Entity
@Table(name = "customers")
public class Customer {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    private String name;

    @OneToMany(mappedBy = "customer", cascade = CascadeType.ALL, orphanRemoval = true)
    private List<Order> orders = new ArrayList<>();

    /** Helper method — mantém os dois lados sincronizados */
    public void addOrder(Order order) {
        orders.add(order);
        order.setCustomer(this);   // atualiza o owning side
    }

    /** Helper method — remove dos dois lados */
    public void removeOrder(Order order) {
        orders.remove(order);
        order.setCustomer(null);   // limpa o owning side
    }

    // getters/setters omitidos para brevidade
}
```

> [!important] Por que o helper method é obrigatório?
> O JPA persiste com base no owning side, mas o grafo de objetos em memória precisa ser consistente **antes** de qualquer serialização, comparação ou lógica de negócio que ocorra no mesmo contexto de persistência. Sem o helper, `customer.getOrders()` retorna lista desatualizada até o reload da entidade.

### Defaults de fetch — a armadilha que a nota 07 ataca

A especificação Jakarta Persistence define os seguintes defaults:

| Annotation | Fetch default | Risco |
|---|---|---|
| `@ManyToOne` | **EAGER** | Pode gerar queries extras silenciosas |
| `@OneToOne` | **EAGER** | Mesmo risco |
| `@OneToMany` | **LAZY** | Seguro por padrão |
| `@ManyToMany` | **LAZY** | Seguro por padrão |

O default EAGER do `@ManyToOne` é o comportamento especificado, mas na prática **quase sempre é sobrescrito** com `fetch = FetchType.LAZY` para evitar carregamentos desnecessários. A nota 07 detalha o problema N+1 que surge quando esse cuidado é ignorado.

---

## Na prática

Modelo completo `Customer` ↔ `Order` com todos os elementos:

```java
import jakarta.persistence.*;
import java.util.ArrayList;
import java.util.List;

@Entity
@Table(name = "customers")
public class Customer {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @Column(nullable = false)
    private String name;

    @OneToMany(mappedBy = "customer", cascade = CascadeType.ALL, orphanRemoval = true)
    private List<Order> orders = new ArrayList<>();

    public void addOrder(Order order) {
        orders.add(order);
        order.setCustomer(this);
    }

    public void removeOrder(Order order) {
        orders.remove(order);
        order.setCustomer(null);
    }

    // getters e setters
    public Long getId() { return id; }
    public String getName() { return name; }
    public void setName(String name) { this.name = name; }
    public List<Order> getOrders() { return orders; }
}
```

```java
import jakarta.persistence.*;
import java.math.BigDecimal;

@Entity
@Table(name = "orders")
public class Order {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @Column(nullable = false)
    private BigDecimal total;

    @ManyToOne(fetch = FetchType.LAZY)
    @JoinColumn(name = "customer_id", nullable = false)
    private Customer customer;

    // getters e setters
    public Long getId() { return id; }
    public BigDecimal getTotal() { return total; }
    public void setTotal(BigDecimal total) { this.total = total; }
    public Customer getCustomer() { return customer; }
    public void setCustomer(Customer customer) { this.customer = customer; }
}
```

Uso no serviço:

```java
// Correto: usar o helper method
Customer customer = em.find(Customer.class, 1L);
Order order = new Order();
order.setTotal(new BigDecimal("99.90"));
customer.addOrder(order);   // sincroniza os dois lados
// flush persiste via owning side (order.customer)
```

---

## Armadilhas

### (1) Esquecer `mappedBy` — join table inesperada

**Problema:** Sem `mappedBy`, o JPA interpreta a relação como dois mapeamentos unidirecionais independentes e cria uma *join table* (ex.: `customer_orders`) ou uma segunda coluna FK.

```java
// ERRADO — falta mappedBy
@OneToMany
private List<Order> orders;
```

**Fix:** Sempre usar `mappedBy` no lado `@OneToMany` quando a relação for bidirecional.

```java
// CORRETO
@OneToMany(mappedBy = "customer")
private List<Order> orders;
```

### (2) Salvar apenas o inverse side — relação não persiste

**Problema:** Modificar apenas a coleção `customer.getOrders().add(order)` sem setar `order.setCustomer(customer)` não gera nenhum UPDATE ou INSERT na FK — o JPA ignora o inverse side para DML.

```java
// ERRADO — owning side não foi atualizado
customer.getOrders().add(order);
em.persist(order);
// customer_id em `orders` permanece NULL
```

**Fix:** Usar o helper method que atualiza o owning side.

```java
// CORRETO
customer.addOrder(order);   // helper method seta order.customer também
em.persist(order);
```

### (3) Confiar no default EAGER do `@ManyToOne`

**Problema:** O default EAGER faz o Hibernate carregar o `Customer` junto com cada `Order` em toda query — mesmo quando o `Customer` não é necessário. Com listas grandes, isso multiplica as queries (problema N+1 tratado na nota 07).

```java
// PERIGOSO — default EAGER carrega Customer em toda query de Order
@ManyToOne
@JoinColumn(name = "customer_id")
private Customer customer;
```

**Fix:** Declarar `LAZY` explicitamente e carregar via JOIN FETCH somente quando necessário.

```java
// SEGURO
@ManyToOne(fetch = FetchType.LAZY)
@JoinColumn(name = "customer_id")
private Customer customer;
```

---

## Em entrevista

### Frase pronta (inglês)

> "In a bidirectional one-to-many mapping, the `@ManyToOne` side is the owning side because it holds the foreign key column — any changes must be made there for the JPA provider to generate the correct DML. The `@OneToMany(mappedBy)` side is purely navigational and is ignored for writes. To keep both sides consistent in memory before flush, I always add helper methods like `addOrder` and `removeOrder` on the parent entity. On top of that, I override the spec default and always declare `fetch = FetchType.LAZY` on `@ManyToOne` to avoid silent N+1 queries."

### Vocabulário

| Termo PT | Termo EN |
|---|---|
| Relacionamento | Relationship |
| Lado dono | Owning side |
| Lado inverso | Inverse side |
| Chave estrangeira | Foreign key |
| Bidirecional | Bidirectional |
| Carregamento | Fetching |
| Mapeamento | Mapping |
| Método auxiliar | Helper method |

---

## Veja também

- [[03-Dominios/Tecnologia/Java/Persistência de dados/06 - @ManyToMany, @OneToOne, cascade e orphanRemoval|@ManyToMany, @OneToOne, cascade e orphanRemoval]]
- [[03-Dominios/Tecnologia/Java/Persistência de dados/07 - Fetch strategies — LAZY, EAGER e a LazyInitializationException|Fetch strategies]]
- [[03-Dominios/Tecnologia/Java/Jakarta EE/09 - JPA — a especificação de persistência|JPA (os defaults de fetch são da spec)]]
- [[03-Dominios/Tecnologia/Java/Persistência de dados/index|Persistência de dados (MOC do galho)]]
- [[03-Dominios/Tecnologia/Java/index|Trilha Java]]
- [[03-Dominios/Tecnologia/Java/Dicionário de Java#@ManyToOne / @OneToMany|@ManyToOne / @OneToMany]]

---

## Referências

- Hibernate ORM User Guide — Associations: <https://docs.hibernate.org/orm/current/userguide/html_single/Hibernate_User_Guide.html>
- Jakarta Persistence 3.2 Specification: <https://jakarta.ee/specifications/persistence/3.2/>
