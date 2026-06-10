---
title: "Projections e DTOs — não vazar a entidade"
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
  - projection
  - spring-data
aliases:
  - "projections JPA"
  - "DTO projection"
---

# Projections e DTOs — não vazar a entidade

> [!abstract] TL;DR
> Para listagens read-only, traga só os campos que precisa: use projections (interface, DTO via `SELECT new`, ou dynamic). A entidade JPA fica no domínio — quem atravessa a borda é o DTO. Carregar a entidade inteira só para ler dois campos é desperdício de memória e um convite para N+1 acidental.

---

## O que é

**Projection** é qualquer mecanismo que restringe quais colunas o Spring Data retorna em vez de materializar a entidade completa.

O Spring Data JPA oferece três sabores:

| Sabor | Mecanismo | Proxy? |
|---|---|---|
| Interface projection | Spring cria um proxy no runtime | Sim |
| Class-based / DTO projection | JPQL `SELECT new …` ou mapeamento direto | Não |
| Dynamic projection | Tipo escolhido em tempo de chamada via `Class<T>` | Depende do tipo passado |

---

## Por que importa

Uma entidade JPA carregada no persistence context tem custo: o Hibernate precisa gerenciar o estado dela para dirty-checking, precisa rastrear relações lazy e pode disparar queries extras ao navegar por associações. Para uma resposta de listagem — que nunca vai ser modificada e deve virar JSON logo em seguida — isso é trabalho desnecessário.

Além disso, expor diretamente a entidade no JSON (via `@RestController`) acopla o contrato da API ao modelo de banco. Se a coluna `total` mudar de tipo ou for renomeada, a API quebra. O DTO é o firewall entre as duas camadas.

---

## Como funciona

### Interface projection — o proxy do Spring (closed vs open)

Declara-se uma interface com getters cujos nomes correspondem às propriedades da entidade. O Spring gera um proxy em tempo de execução que intercepta as chamadas e as redireciona ao resultado da query.

**Closed projection** — todos os getters batem em propriedades reais. O Spring consegue reescrever o SQL para selecionar só essas colunas.

```java
public interface OrderSummary {
    Long getId();
    BigDecimal getTotal();
    String getCustomerName();   // campo calculado de Customer.name
}

public interface OrderRepository extends JpaRepository<Order, Long> {
    List<OrderSummary> findByStatus(OrderStatus status);
}
```

**Open projection** — um getter usa `@Value` com SpEL, computando um valor a partir de `target`. O Spring não consegue otimizar: carrega a entidade inteira para então calcular a expressão.

```java
public interface OrderSummary {
    @Value("#{target.id + '-' + target.status}")
    String getLabel();   // open: Spring precisa do target inteiro
}
```

> [!tip] Prefira closed projections ou default methods
> Em vez de `@Value` com SpEL, use um `default` method que combine os getters já declarados. Assim o Spring ainda otimiza a query e você tem a lógica de composição na interface.

```java
public interface OrderSummary {
    Long getId();
    String getStatus();

    default String getLabel() {
        return getId() + "-" + getStatus();
    }
}
```

---

### Class-based / DTO projection — `record` via `SELECT new`

Sem proxy. O resultado da query é passado diretamente para o construtor do DTO. Java Records são a forma mais enxuta.

```java
public record OrderDto(Long id, BigDecimal total) {}
```

Com query derivada, o Spring Data tenta inferir o construtor:

```java
List<OrderDto> findByStatus(OrderStatus status);
```

Com `@Query` explícito, usa-se a sintaxe JPQL de constructor expression:

```java
@Query("SELECT new com.app.order.OrderDto(o.id, o.total) FROM Order o WHERE o.status = :status")
List<OrderDto> findSummaryByStatus(@Param("status") OrderStatus status);
```

> [!note] Pacote qualificado obrigatório
> O `SELECT new` precisa do nome totalmente qualificado da classe (`com.app.order.OrderDto`), não apenas `OrderDto`.

O Spring Data JPA também é capaz de reescrever automaticamente queries que selecionam a entidade raiz para a forma de constructor expression quando o tipo de retorno é um DTO compatível:

```java
// Spring reescreve isso para SELECT new OrderDto(o.id, o.total) FROM Order o …
@Query("SELECT o FROM Order o WHERE o.status = :status")
List<OrderDto> findByStatusRewritten(@Param("status") OrderStatus status);
```

---

### Dynamic projection — `<T> List<T> findBy...(Class<T>)`

Quando o mesmo método de repositório precisa devolver tipos diferentes dependendo do contexto, passa-se o tipo como parâmetro.

```java
public interface OrderRepository extends JpaRepository<Order, Long> {
    <T> List<T> findByStatus(OrderStatus status, Class<T> type);
}
```

Uso:

```java
// Entidade completa (para modificação)
List<Order> orders = repository.findByStatus(OPEN, Order.class);

// Projeção leve (para listagem)
List<OrderSummary> summaries = repository.findByStatus(OPEN, OrderSummary.class);
```

---

### Quando usar projection (listagem read-only) vs entidade (modificar)

| Situação | O que usar | Motivo |
|---|---|---|
| Listagem paginada, somente leitura | Interface ou DTO projection | Menos dados, sem dirty-checking |
| Endpoint de detalhes que vai modificar | Entidade completa | Precisa do ciclo de vida JPA |
| Resposta de API REST | DTO (class-based) | Contrato explícito, não vaza schema |
| Consulta em lote, relatório | DTO via `SELECT new` | Sem overhead de proxy |
| Método de repositório reutilizável | Dynamic projection | Flexibilidade em tempo de chamada |

---

## Na prática

Cenário: expor um resumo de pedidos para uma listagem paginada.

**Entidade**

```java
import jakarta.persistence.*;
import java.math.BigDecimal;

@Entity
@Table(name = "orders")
public class Order {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    private BigDecimal total;

    private String status;

    @ManyToOne(fetch = FetchType.LAZY)
    @JoinColumn(name = "customer_id")
    private Customer customer;

    // getters e setters omitidos
}
```

**Interface projection (closed)**

```java
public interface OrderSummary {
    Long getId();
    BigDecimal getTotal();
    String getStatus();
}
```

**DTO record via `SELECT new`**

```java
public record OrderDto(Long id, BigDecimal total, String status) {}
```

```java
public interface OrderRepository extends JpaRepository<Order, Long> {

    // Interface projection derivada
    List<OrderSummary> findByStatus(String status);

    // DTO via JPQL explícito
    @Query("""
        SELECT new com.app.order.OrderDto(o.id, o.total, o.status)
        FROM Order o
        WHERE o.status = :status
        """)
    List<OrderDto> findDtoByStatus(@Param("status") String status);

    // Dynamic projection
    <T> List<T> findAllByStatus(String status, Class<T> type);
}
```

**Uso do dynamic projection no serviço**

```java
// Contexto de leitura: projeção leve
List<OrderSummary> summaries =
    orderRepository.findAllByStatus("OPEN", OrderSummary.class);

// Contexto de modificação: entidade completa
List<Order> orders =
    orderRepository.findAllByStatus("OPEN", Order.class);
```

---

## Armadilhas

### (1) Carregar a entidade inteira para ler 3 campos

`findAll()` retorna `List<Order>` com todos os campos e todas as relações inicializadas (ou agendadas para lazy load). Para uma listagem com 1.000 pedidos, isso pode significar gigabytes de dado desnecessário. Use uma closed projection ou DTO projection.

### (2) Projection que toca relação lazy — N+1 sutil

Se a interface projection declara `getCustomer()` retornando outra interface de projeção, o Spring vai disparar uma query extra por pedido para carregar o `Customer`. É a mesma armadilha do N+1, só que mais difícil de enxergar porque não há `customer.getName()` explícito no código — o proxy faz isso silenciosamente. Combine com `@EntityGraph` se precisar de dados do relacionamento.

### (3) Expor a entidade diretamente no JSON

Retornar `Order` em um `@RestController` acopla o contrato da API ao modelo de persistência. Renomear uma coluna, adicionar um campo `@Transient` ou alterar um relacionamento quebra a API sem aviso em tempo de compilação. O contrato da API é o DTO — veja [[03-Dominios/Java/Web e APIs REST/05 - Serialização JSON com Jackson|Serialização JSON (Galho 9)]].

---

## Em entrevista

### Frase pronta (inglês)

"In Spring Data JPA, projections let you retrieve only the columns you actually need instead of loading the full entity. For read-only use cases like paginated lists, I prefer closed interface projections or class-based DTO projections using records and `SELECT new` in JPQL — both avoid loading the full entity graph and prevent dirty-checking overhead. I keep the JPA entity strictly in the domain layer and always expose a DTO at the API boundary to decouple the persistence model from the API contract."

### Vocabulário

| Português | Inglês |
|---|---|
| projeção | projection |
| projeção de interface | interface projection |
| projeção fechada | closed projection |
| projeção aberta | open projection |
| projeção baseada em classe | class-based projection |
| objeto de transferência de dados | data transfer object (DTO) |
| somente leitura | read-only |
| proxy | proxy |
| expressão de construtor (JPQL) | constructor expression |
| projeção dinâmica | dynamic projection |

---

## Veja também

- [[03-Dominios/Java/Persistência de dados/08 - O problema N+1 e suas soluções — @EntityGraph, JOIN FETCH, batch size|O problema N+1]]
- [[03-Dominios/Java/Persistência de dados/09 - Consultas com @Query — JPQL, native e @Modifying|Consultas com @Query]]
- [[03-Dominios/Java/Web e APIs REST/05 - Serialização JSON com Jackson|Serialização JSON (DTO na borda)]]
- [[03-Dominios/Java/Persistência de dados/index|Persistência de dados (MOC do galho)]]
- [[03-Dominios/Java/index|Trilha Java]]
- [[03-Dominios/Java/Dicionário de Java#projection (JPA)|projection (JPA)]]

---

## Referências

- Spring Data JPA — Projections: https://docs.spring.io/spring-data/jpa/reference/repositories/projections.html
