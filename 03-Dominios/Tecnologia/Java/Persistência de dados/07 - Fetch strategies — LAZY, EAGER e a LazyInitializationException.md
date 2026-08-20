---
title: "Fetch strategies — LAZY, EAGER e a LazyInitializationException"
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
aliases:
  - "fetch strategies"
  - "LazyInitializationException"
  - "Open Session In View"
---

# Fetch strategies — LAZY, EAGER e a LazyInitializationException

> [!abstract] TL;DR
> A *fetch strategy* define **quando** o JPA/Hibernate vai ao banco buscar uma associação: imediatamente junto com a entidade pai (EAGER) ou só quando o código a acessar explicitamente (LAZY). A regra prática é **sempre declarar LAZY** — inclusive em `@ManyToOne`, que é EAGER por padrão e injeta JOINs indesejados em toda query. A `LazyInitializationException` surge ao acessar uma associação LAZY *fora* da transação/persistence context ativo; o caminho certo é projetar DTOs *dentro* da transação, não estender a sessão. O Spring Boot registra o Open Session In View por padrão (`spring.jpa.open-in-view=true`), o que mascara N+1 e mantém conexões abertas desnecessariamente — desabilitar em produção é obrigatório.

---

## O que é

*Fetch strategy* (estratégia de busca) é a política que governa o momento em que o JPA carrega dados de uma associação mapeada (`@ManyToOne`, `@OneToMany`, `@ManyToMany`, `@OneToOne`). Existem dois valores possíveis para o atributo `fetch`:

| Valor | Comportamento | Analogia |
|---|---|---|
| `FetchType.LAZY` | Carrega sob demanda; associação vira proxy ou coleção não-inicializada | Pedir a conta só quando for embora |
| `FetchType.EAGER` | Carrega junto com a entidade pai, na mesma query (ou com JOIN/subquery extra) | Trazer toda a ementa junto com o cardápio |

---

## Por que importa

A escolha da estratégia afeta diretamente:

- **Número de queries**: EAGER gera JOINs ou subqueries extras em *toda* busca, mesmo que o código nunca use a associação naquela chamada.
- **Uso de memória**: carregar coleções inteiras ao buscar um único registro pode trazer milhares de linhas sem necessidade.
- **Comportamento fora da transação**: LAZY exige que o persistence context esteja aberto; acessá-la após o fechamento da sessão lança `LazyInitializationException`.
- **Rastreabilidade de queries**: com EAGER, queries extras aparecem silenciosamente sem nenhuma anotação no stack trace.

---

## Como funciona

### LAZY vs EAGER — proxy, coleção lazy e a tabela de defaults

Quando o JPA carrega uma entidade com associação LAZY, ele não executa a query da associação de imediato. Em vez disso:

- **Associações para entidade única** (`@ManyToOne`, `@OneToOne`): Hibernate injeta um *proxy* — um objeto gerado em tempo de execução que estende a classe alvo. O banco só é consultado na primeira chamada a um método que não seja o getter do `id`.
- **Coleções** (`@OneToMany`, `@ManyToMany`): o campo recebe uma implementação especial de `Collection` (ex.: `PersistentBag`, `PersistentSet`) que permanece não-inicializada até que `size()`, `iterator()` ou qualquer acesso seja realizado.

Defaults do JPA (sem anotação explícita de `fetch`):

| Anotação | Default JPA |
|---|---|
| `@ManyToOne` | **EAGER** |
| `@OneToOne` | **EAGER** |
| `@OneToMany` | LAZY |
| `@ManyToMany` | LAZY |

Isso significa que o default mais perigoso — `@ManyToOne` EAGER — já está ativo em todo relacionamento para-um sem declaração explícita.

---

### A regra prática: sempre LAZY — o `@ManyToOne` EAGER é o vilão escondido

Com `@ManyToOne` EAGER, toda query de uma entidade que possui 3 relacionamentos EAGER resultará em pelo menos 3 JOINs adicionais, mesmo que a camada de negócio nunca precise dessas associações naquele contexto. Em um `findAll()` que retorna 200 registros, esses JOINs multiplicam o volume de dados transferido pelo banco.

A orientação canônica do Hibernate User Guide é declarar todas as associações como LAZY e **buscar de forma explícita** (via `JOIN FETCH` em JPQL, `@EntityGraph`, ou `fetch join` em Criteria) somente quando a associação for necessária para o caso de uso em questão.

```java
// Errado — default EAGER injeta JOIN em toda query
@ManyToOne
private Customer customer;

// Correto — LAZY; o JOIN só ocorre quando explicitamente solicitado
@ManyToOne(fetch = FetchType.LAZY)
private Customer customer;
```

---

### `LazyInitializationException` — acesso lazy fora da transação e as soluções

A exceção ocorre quando o código tenta inicializar uma associação LAZY após o fechamento do persistence context (da `Session`/`EntityManager`). O proxy ainda existe na memória, mas não há sessão ativa para executar o SQL.

Cenário típico em uma aplicação Spring:

```
@Transactional  ← transação abre aqui
findById(id)    ← Order carregada, items é proxy não-inicializado
@Transactional  ← transação fecha aqui (método retorna)

// Na camada de apresentação / serializador:
order.getItems().size()  → LazyInitializationException!
```

**Soluções corretas:**

1. **Mapear para DTO dentro da transação** (preferida): o service transforma `Order` em `OrderDTO` antes de retornar — a associação é acessada enquanto o contexto ainda está ativo.
2. **`@EntityGraph`**: instrui o JPA a fazer JOIN FETCH para aquela operação específica, sem alterar o mapeamento global.
3. **JPQL com `JOIN FETCH`**: consulta explícita que carrega a associação quando necessário.

O que **não** fazer: colocar `@Transactional` no controller para "resolver" a exceção ou habilitar OSIV permanentemente — ambos apenas adiam o problema enquanto introduzem acoplamento e vazamento de recursos.

---

### Open Session In View — o Boot habilita por default; `open-in-view: false` em produção

O padrão *Open Session In View* (OSIV) consiste em manter o `EntityManager` aberto durante toda a requisição HTTP — incluindo a renderização da view ou a serialização JSON. O Spring Boot registra automaticamente o `OpenEntityManagerInViewInterceptor` com esse comportamento.

**Por que isso é problemático em produção:**

- A conexão com o banco permanece alocada desde o início até o fim da requisição HTTP, mesmo durante operações que não precisam de banco (ex.: serialização, logging).
- Lazy loading ocorre silenciosamente na camada de apresentação, tornando invisível o custo real de cada endpoint e facilitando o surgimento de N+1 queries.
- Sob carga alta, o pool de conexões se esgota enquanto threads aguardam serialização — latência aumenta de forma não óbvia.

```yaml
# application.yml
spring:
  jpa:
    open-in-view: false  # desabilitar em produção
```

Com OSIV desabilitado, qualquer acesso a associação LAZY fora da transação lança `LazyInitializationException` imediatamente, tornando o problema visível e forçando a correção adequada na camada de serviço.

---

## Na prática

Cenário: um endpoint que retorna detalhes de um pedido com os itens. Sem cuidado, a serialização JSON acessa `order.getItems()` fora da transação.

```java
// Entidade — LAZY explícito em todos os relacionamentos
@Entity
public class Order {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    private String reference;

    @ManyToOne(fetch = FetchType.LAZY)   // não confiar no default EAGER
    @JoinColumn(name = "customer_id")
    private Customer customer;

    @OneToMany(mappedBy = "order", fetch = FetchType.LAZY)
    private List<OrderItem> items = new ArrayList<>();

    // getters/setters omitidos
}
```

```java
// Problema: retornar a entidade diretamente
@GetMapping("/{id}")
public Order getOrder(@PathVariable Long id) {
    return orderRepository.findById(id).orElseThrow();
    // Jackson tenta serializar order.getItems() FORA da transação
    // → LazyInitializationException
}
```

```java
// Solução correta: projetar DTO dentro da transação
@Service
public class OrderService {

    @Transactional(readOnly = true)
    public OrderDTO findById(Long id) {
        Order order = orderRepository.findById(id).orElseThrow();
        // acesso à associação DENTRO da transação — sem exceção
        List<OrderItemDTO> items = order.getItems().stream()
            .map(item -> new OrderItemDTO(item.getProduct().getName(), item.getQuantity()))
            .toList();
        return new OrderDTO(order.getId(), order.getReference(), items);
    }
}
```

Alternativa com `@EntityGraph` para buscar a coleção em uma única query:

```java
@EntityGraph(attributePaths = {"items", "items.product"})
Optional<Order> findWithItemsById(Long id);
```

Configuração para desabilitar OSIV:

```yaml
spring:
  jpa:
    open-in-view: false
```

---

## Armadilhas

### (1) `@ManyToOne` é EAGER por padrão

Todo `@ManyToOne` sem `fetch = FetchType.LAZY` explícito injeta um JOIN em absolutamente toda query que carrega a entidade pai. Em entidades com 4 ou 5 relacionamentos para-um, isso resulta em queries com múltiplos JOINs mesmo quando nenhum dado das associações será utilizado. Auditar os mapeamentos existentes com `@ManyToOne` é o primeiro passo ao diagnosticar queries lentas.

### (2) OSIV habilitado esconde N+1 e prende conexões

Com `spring.jpa.open-in-view=true` (default do Boot), o lazy loading funciona na camada de apresentação sem erro visível. Isso mascara queries N+1 — cada item iterado na serialização pode disparar um SELECT separado. Além disso, a conexão com o banco permanece ocupada enquanto o Jackson serializa a resposta, aumentando a pressão sobre o pool de conexões sob carga. O resultado típico é lentidão que aparece apenas em produção, nunca nos testes locais.

### (3) `@Transactional` no controller não é solução

Adicionar `@Transactional` ao método do controller apenas para evitar a `LazyInitializationException` acopla a camada de apresentação ao persistence context, além de manter a transação aberta durante toda a execução do método do controller — incluindo serialização. A correção correta é construir o DTO no service, dentro de uma transação de leitura.

---

## Em entrevista

### Frase pronta (inglês)

"The safest rule is to declare all associations as LAZY and fetch eagerly only when you explicitly need the data, using JOIN FETCH in JPQL or @EntityGraph — this keeps queries predictable and avoids loading data you'll never use. A LazyInitializationException means you tried to access a lazy association after the persistence context was closed; the fix is to project a DTO inside the transactional service method, not to extend the session. Spring Boot's Open Session In View keeps the EntityManager open for the whole HTTP request by default, which hides N+1 problems and holds database connections longer than necessary — disabling it with `spring.jpa.open-in-view=false` makes lazy loading issues surface early, where they're easy to fix."

### Vocabulário

| Português | Inglês |
|---|---|
| Carregamento preguiçoso | Lazy loading |
| Carregamento antecipado | Eager loading |
| Proxy | Proxy (objeto gerado que intercepta acesso à associação) |
| Exceção de inicialização tardia | Lazy initialization exception |
| Sessão aberta na view | Open Session in View (OSIV) |
| Estratégia de busca | Fetch strategy |
| Contexto de persistência | Persistence context |
| Grafo de entidade | Entity graph |

---

## Veja também

- [[03-Dominios/Tecnologia/Java/Persistência de dados/05 - Relacionamentos — @ManyToOne, @OneToMany e o owning side|Relacionamentos]]
- [[03-Dominios/Tecnologia/Java/Persistência de dados/08 - O problema N+1 e suas soluções — @EntityGraph, JOIN FETCH, batch size|O problema N+1]]
- [[03-Dominios/Tecnologia/Java/Web e APIs REST/05 - Serialização JSON com Jackson|Serialização JSON (DTO na borda)]]
- [[03-Dominios/Tecnologia/Java/Persistência de dados/index|Persistência de dados (MOC do galho)]]
- [[03-Dominios/Tecnologia/Java/index|Trilha Java]]
- [[03-Dominios/Tecnologia/Java/Dicionário de Java#fetch strategy (LAZY/EAGER)|fetch strategy]]

---

## Referências

- Hibernate ORM User Guide — Fetching: <https://docs.hibernate.org/orm/current/userguide/html_single/Hibernate_User_Guide.html>
- Spring Boot Reference — Data: SQL Databases (Open Session In View): <https://docs.spring.io/spring-boot/reference/data/sql.html>
