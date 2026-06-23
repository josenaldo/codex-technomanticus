---
title: "@ManyToMany, @OneToOne, cascade e orphanRemoval"
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
  - relacionamentos
aliases:
  - "@ManyToMany"
  - "cascade"
  - "orphanRemoval"
---

# @ManyToMany, @OneToOne, cascade e orphanRemoval

> [!abstract] TL;DR
> `@ManyToMany` mapeia relações N:N via tabela de junção com `@JoinTable` — mas prefira uma entidade associativa explícita sempre que a relação tiver atributos próprios (quantidade, data, status). `@OneToOne` carrega lazy de forma problemática sem `@MapsId`; com ele, a FK vira PK e o proxy funciona corretamente. `cascade` propaga operações do pai para os filhos (PERSIST, MERGE, REMOVE, REFRESH, DETACH, ALL). `orphanRemoval = true` vai além: remove automaticamente qualquer filho que seja retirado da coleção do pai, mesmo sem deletar o pai.

## O que é

`@ManyToMany` estabelece um relacionamento muitos-para-muitos entre duas entidades usando uma **tabela de junção** no banco. A anotação `@JoinTable` descreve o nome dessa tabela e as colunas de chave estrangeira de cada lado.

`@OneToOne` mapeia uma relação de um-para-um entre entidades. O desafio é o carregamento lazy: Hibernate não consegue inicializar o proxy sem consultar o banco a menos que a chave estrangeira também seja a chave primária — situação viabilizada pela anotação `@MapsId`.

`cascade` instrui o JPA a propagar uma operação de ciclo de vida (persist, merge, remove, refresh, detach) do pai para as entidades associadas. `orphanRemoval` é um mecanismo complementar: apaga filhos que forem removidos da coleção, independentemente de o pai ser deletado.

## Por que importa

Esses recursos definem o **comportamento de escrita em cascata** e o **ciclo de vida de entidades dependentes**. Sem entendê-los, erros clássicos aparecem: objetos duplicados ao persistir, filhos que ficam órfãos no banco, remoções acidentais por `CascadeType.ALL` mal aplicado, ou N+1 queries em `@OneToOne` EAGER carregando dados desnecessários em cada consulta.

Além disso, `@ManyToMany` com uma entidade simples parece conveniente até que a relação precise de atributos extras — nesse ponto, a refatoração para entidade associativa é inevitável.

## Como funciona

### `@ManyToMany` + `@JoinTable` (e por que preferir entidade associativa)

O lado dono da relação declara `@JoinTable` com:

- **`joinColumns`** — FK que aponta para a entidade dona.
- **`inverseJoinColumns`** — FK que aponta para a entidade inversa.

O lado inverso usa `mappedBy` e não controla a tabela.

```java
@Entity
public class Product {
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;
    private String name;

    @ManyToMany
    @JoinTable(
        name = "product_tag",
        joinColumns = @JoinColumn(name = "product_id"),
        inverseJoinColumns = @JoinColumn(name = "tag_id")
    )
    private Set<Tag> tags = new HashSet<>();
}

@Entity
public class Tag {
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;
    private String label;

    @ManyToMany(mappedBy = "tags")
    private Set<Product> products = new HashSet<>();
}
```

**Quando preferir entidade associativa:** se a tabela de junção precisar armazenar dados próprios (quantidade, data de associação, desconto aplicado), `@ManyToMany` deixa de ser suficiente. A solução é criar uma entidade que representa a associação e mapear cada lado com `@ManyToOne`.

### `@OneToOne` (e o lazy problemático sem `@MapsId`)

Por padrão, `@OneToOne` carrega EAGER — toda query no pai já faz JOIN com o filho. Marcar `fetch = FetchType.LAZY` deveria resolver, mas o Hibernate mantém a associação EAGER na maioria dos cenários porque precisa **verificar se o registro filho existe** antes de criar o proxy. Sem saber isso, ele teria de fazer um proxy de algo potencialmente nulo.

`@MapsId` resolve o problema ao usar a mesma coluna como FK e PK da entidade filha. Como o Hibernate já conhece o ID do pai, ele consegue criar o proxy sem consulta extra:

```java
@Entity
public class Customer {
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;
    private String name;
}

@Entity
public class CustomerProfile {
    @Id
    private Long id;          // mesmo valor do customer.id

    @OneToOne(fetch = FetchType.LAZY)
    @MapsId
    @JoinColumn(name = "customer_id")
    private Customer customer;

    private String bio;
    private String avatarUrl;
}
```

Com `@MapsId`, `customerProfile.getId()` e `customer.getId()` retornam o mesmo valor — FK e PK compartilham a coluna.

### `cascade` (PERSIST/MERGE/REMOVE/ALL): propagando operações pai→filho

| CascadeType | Quando se propaga               |
|-------------|--------------------------------|
| PERSIST     | `entityManager.persist(pai)`   |
| MERGE       | `entityManager.merge(pai)`     |
| REMOVE      | `entityManager.remove(pai)`    |
| REFRESH     | `entityManager.refresh(pai)`   |
| DETACH      | `entityManager.detach(pai)`    |
| ALL         | Todos os acima                 |

Exemplo típico: salvar um pedido e seus itens de uma só vez.

```java
@Entity
public class Order {
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @OneToMany(mappedBy = "order", cascade = CascadeType.PERSIST)
    private List<OrderItem> items = new ArrayList<>();
}
```

Com `CascadeType.PERSIST`, basta persistir o `Order` — os `OrderItem` são persistidos automaticamente se estiverem na coleção.

### `orphanRemoval`: a diferença para `cascade = REMOVE`

`cascade = REMOVE` dispara apenas quando o **pai é removido**: `entityManager.remove(order)` deleta também os itens.

`orphanRemoval = true` age de forma adicional: remove o filho quando ele é **retirado da coleção** do pai, mesmo que o pai continue existindo.

```java
@Entity
public class Order {
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @OneToMany(mappedBy = "order", cascade = CascadeType.ALL, orphanRemoval = true)
    private List<OrderItem> items = new ArrayList<>();
}
```

```java
// Este código emite um DELETE para o item removido da lista:
order.getItems().remove(0);
orderRepository.save(order);
```

Sem `orphanRemoval`, a linha acima apenas desmarca a FK do item (tornando-o órfão no banco, com FK nula ou mantendo o registro sem dono).

## Na prática

### Exemplo 1 — `@ManyToMany` simples: Product ↔ Tag

```java
import jakarta.persistence.*;
import java.util.HashSet;
import java.util.Set;

@Entity
@Table(name = "products")
public class Product {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    private String name;

    @ManyToMany(cascade = {CascadeType.PERSIST, CascadeType.MERGE})
    @JoinTable(
        name = "product_tag",
        joinColumns = @JoinColumn(name = "product_id"),
        inverseJoinColumns = @JoinColumn(name = "tag_id")
    )
    private Set<Tag> tags = new HashSet<>();

    public void addTag(Tag tag) {
        tags.add(tag);
        tag.getProducts().add(this);
    }

    public void removeTag(Tag tag) {
        tags.remove(tag);
        tag.getProducts().remove(this);
    }

    // getters/setters omitidos
}

@Entity
@Table(name = "tags")
public class Tag {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    private String label;

    @ManyToMany(mappedBy = "tags")
    private Set<Product> products = new HashSet<>();

    // getters/setters omitidos
}
```

### Exemplo 2 — Entidade associativa explícita: Order ↔ Product via OrderItem

Quando a relação precisa de `quantity` (atributo próprio), `@ManyToMany` não basta. A entidade `OrderItem` assume o papel de tabela de junção com estado.

```java
import jakarta.persistence.*;
import java.math.BigDecimal;

@Entity
@Table(name = "order_items")
public class OrderItem {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @ManyToOne(fetch = FetchType.LAZY, optional = false)
    @JoinColumn(name = "order_id")
    private Order order;

    @ManyToOne(fetch = FetchType.LAZY, optional = false)
    @JoinColumn(name = "product_id")
    private Product product;

    private int quantity;
    private BigDecimal unitPrice;

    // getters/setters omitidos
}

@Entity
@Table(name = "orders")
public class Order {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @ManyToOne(fetch = FetchType.LAZY, optional = false)
    @JoinColumn(name = "customer_id")
    private Customer customer;

    @OneToMany(mappedBy = "order", cascade = CascadeType.ALL, orphanRemoval = true)
    private List<OrderItem> items = new ArrayList<>();

    public void addItem(Product product, int quantity, BigDecimal unitPrice) {
        OrderItem item = new OrderItem();
        item.setOrder(this);
        item.setProduct(product);
        item.setQuantity(quantity);
        item.setUnitPrice(unitPrice);
        items.add(item);
    }

    public void removeItem(OrderItem item) {
        items.remove(item);
        item.setOrder(null);
    }
}
```

## Armadilhas

### (1) `@ManyToMany` escondendo uma entidade que deveria existir

**Problema:** o modelo começa com uma relação N:N simples, mas com o tempo surgem novos requisitos: quantidade, data de criação, desconto aplicado. A tabela de junção passa a ter colunas que não pertencem a nenhuma das entidades.

**Exemplo sintomático:**

```java
// Tabela product_tag ganha colunas extras... mas não há entidade pra mapeá-las
@ManyToMany
@JoinTable(name = "product_tag", ...)
private Set<Tag> tags;  // como adicionar "addedAt"?
```

**Fix:** criar `ProductTag` (ou o equivalente de domínio) como entidade associativa com `@ManyToOne` para cada lado e os atributos extras como campos comuns. Considere desde o início se a relação pode ter dados próprios.

### (2) `cascade = CascadeType.ALL` deletando filhos inesperadamente

**Problema:** `CascadeType.ALL` inclui `REMOVE`. Se o repositório de uma entidade pai executar um `delete`, todos os filhos em cascata são removidos — mesmo que o desenvolvedor não tivesse essa intenção.

**Exemplo sintomático:**

```java
@OneToMany(cascade = CascadeType.ALL)
private List<Tag> tags;  // deletar Product apaga Tags globais compartilhadas!
```

**Fix:** seja explícito. Use apenas os cascade types necessários (`PERSIST` e `MERGE` costumam ser suficientes). Evite `ALL` em entidades com filhos compartilhados entre diferentes pais.

### (3) `@OneToOne` EAGER dobrando JOINs em toda query

**Problema:** `@OneToOne` é EAGER por padrão. Em uma lista de `Customer`, o Hibernate emitirá um JOIN com `CustomerProfile` para cada registro, mesmo quando o perfil não for necessário.

**Exemplo sintomático:**

```java
// Sem fetch = LAZY: toda consulta de Customer arrasta CustomerProfile
@OneToOne
@JoinColumn(name = "profile_id")
private CustomerProfile profile;
```

**Fix:** use `fetch = FetchType.LAZY` e aplique `@MapsId` para que o lazy realmente funcione. Sem `@MapsId`, o Hibernate pode ignorar o `LAZY` e continuar carregando EAGER.

## Em entrevista

### Frase pronta (inglês)

"In JPA, `@ManyToMany` maps a many-to-many relationship using a join table, but I prefer an explicit association entity whenever the relationship carries its own attributes — like quantity or timestamp — since `@ManyToMany` can't hold extra columns. `@OneToOne` is eager by default, and even marking it `LAZY` won't work reliably without `@MapsId`, which makes the foreign key double as the primary key so Hibernate can build the proxy without an extra query. For lifecycle propagation, `cascade` pushes operations like persist and merge from parent to child, while `orphanRemoval` goes further by deleting any child that gets removed from the parent's collection, even if the parent itself is still alive."

### Vocabulário

| Termo PT | Termo EN |
|---|---|
| Tabela de junção | Join table |
| Entidade associativa | Association entity |
| Cascata / cascade | Cascade |
| Remoção de órfãos | Orphan removal |
| Relação muitos-para-muitos | Many-to-many relationship |
| Relação um-para-um | One-to-one relationship |
| Lado dono | Owning side |
| Chave primária compartilhada | Shared primary key |

## Veja também

- [[03-Dominios/Tecnologia/Java/Persistência de dados/05 - Relacionamentos — @ManyToOne, @OneToMany e o owning side|Relacionamentos]]
- [[03-Dominios/Tecnologia/Java/Persistência de dados/07 - Fetch strategies — LAZY, EAGER e a LazyInitializationException|Fetch strategies]]
- [[03-Dominios/Tecnologia/Java/Persistência de dados/index|Persistência de dados (MOC do galho)]]
- [[03-Dominios/Tecnologia/Java/index|Trilha Java]]
- [[03-Dominios/Tecnologia/Java/Dicionário de Java#@ManyToMany|@ManyToMany]]
- [[03-Dominios/Tecnologia/Java/Dicionário de Java#cascade / orphanRemoval|cascade / orphanRemoval]]

## Referências

- Hibernate ORM User Guide — Associations: https://docs.hibernate.org/orm/current/userguide/html_single/Hibernate_User_Guide.html
- Jakarta Persistence 3.2 Specification — Section 2.9 (Entity Relationships): https://jakarta.ee/specifications/persistence/3.2/
- Vlad Mihalcea — The best way to map a @ManyToMany association with extra columns: https://vladmihalcea.com/the-best-way-to-map-a-many-to-many-association-with-extra-columns-when-using-jpa-and-hibernate/
- Vlad Mihalcea — The best way to map a @OneToOne relationship with JPA and Hibernate: https://vladmihalcea.com/the-best-way-to-map-a-onetoone-relationship-with-jpa-and-hibernate/
