---
title: "Paginação e ordenação — Pageable, Page e Slice"
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
  - paginacao
  - spring-data
aliases:
  - "paginação Spring Data"
  - "Page vs Slice"
---

# Paginação e ordenação — Pageable, Page e Slice

> [!abstract] TL;DR
> Passe um `Pageable` para o repositório e receba os resultados em fatias.
> `Page<T>` dispara uma query `COUNT` adicional para informar o total de elementos e páginas — útil para UIs de paginação completa, mas com custo.
> `Slice<T>` apenas informa se há uma próxima fatia, sem contar o total — mais barato para feeds e rolagem infinita.
> A ordenação é controlada por `Sort`, composto dentro do `PageRequest` ou passado diretamente.

---

## O que é

Paginação é a técnica de dividir um resultado grande em blocos menores (páginas ou fatias) para não trazer toda a tabela de uma vez para a memória da aplicação.

O Spring Data encapsula esse mecanismo em três abstrações centrais:

| Abstração | Papel |
|---|---|
| `Pageable` | Descreve **o que buscar**: número de página, tamanho e critério de ordenação. |
| `Page<T>` | Retorna a fatia de dados **mais** metadados completos (total de elementos e páginas). |
| `Slice<T>` | Retorna a fatia de dados com metadados mínimos (só informa se existe próxima fatia). |

`PageRequest` é a implementação concreta de `Pageable` usada na prática. `Page<T>` estende `Slice<T>`, então tudo que vale para `Slice` também vale para `Page`.

---

## Por que importa

Buscar todos os registros de uma tabela com milhões de linhas em uma única query é um caminho certo para esgotar memória heap e sobrecarregar o banco.

Mas nem todo caso de paginação exige saber quantas páginas existem. Uma tela de histórico de pedidos pode mostrar "carregar mais" sem precisar do total; já uma tela administrativa com números de páginas clicáveis precisa do total exato. Usar a abstração errada — `Page` onde `Slice` bastaria — gera uma query `COUNT` desnecessária em toda requisição.

Entender a diferença entre `Page` e `Slice` é, na prática, uma decisão de performance.

---

## Como funciona

### `Pageable`, `PageRequest` e `Sort`

`Pageable` é uma interface. O jeito mais direto de criá-la é via `PageRequest.of(...)`:

```java
// Página 0 (primeira), 20 itens por página, sem ordenação
Pageable pageable = PageRequest.of(0, 20);

// Página 0, 20 itens, ordenado por createdAt descendente
Pageable pageable = PageRequest.of(0, 20, Sort.by("createdAt").descending());

// Ordenação composta: status ascendente e depois createdAt descendente
Sort sort = Sort.by("status").ascending()
               .and(Sort.by("createdAt").descending());

Pageable pageable = PageRequest.of(0, 20, sort);
```

O índice de página é **zero-based**: página `0` é a primeira, página `1` é a segunda e assim por diante.

`Sort` pode ser construído de forma fluente. Quando não há ordenação definida, use `Sort.unsorted()` e, quando não há paginação, `Pageable.unpaged()`.

> [!warning] `Pageable` já contém o `Sort`
> Passar `Pageable` **e** `Sort` como parâmetros separados no mesmo método é inválido — o `Pageable` já carrega a ordenação. Use um ou outro.

---

### `Page<T>`: traz o total (uma query `COUNT` a mais)

`Page<T>` é o resultado quando a aplicação precisa de metadados completos de paginação: total de elementos na tabela e total de páginas.

O Spring Data executa **duas queries** para cada chamada:
1. A query principal com `LIMIT` e `OFFSET` para buscar os dados da página.
2. Uma query `COUNT(...)` separada para calcular `getTotalElements()`.

```java
interface OrderRepository extends JpaRepository<Order, Long> {
    Page<Order> findByStatus(OrderStatus status, Pageable pageable);
}
```

Métodos úteis de `Page<T>`:

| Método | Descrição |
|---|---|
| `getContent()` | Lista de elementos da página atual. |
| `getTotalElements()` | Total de registros que satisfazem o filtro. |
| `getTotalPages()` | Total de páginas para o tamanho configurado. |
| `getNumber()` | Número da página atual (zero-based). |
| `hasNext()` | Se existe próxima página. |
| `isLast()` | Se esta é a última página. |

---

### `Slice<T>`: só sabe se há próxima página (sem count — mais barato)

`Slice<T>` executa apenas **uma query**: busca `pageSize + 1` elementos. Se o banco retornou mais do que `pageSize`, `hasNext()` devolve `true`; caso contrário, `false`. O elemento extra nunca é exposto no conteúdo.

```java
interface OrderRepository extends JpaRepository<Order, Long> {
    Slice<Order> findByStatus(OrderStatus status, Pageable pageable);
}
```

Métodos úteis de `Slice<T>`:

| Método | Descrição |
|---|---|
| `getContent()` | Lista de elementos da fatia atual. |
| `hasNext()` | Se existe próxima fatia. |
| `hasPrevious()` | Se existe fatia anterior. |
| `nextPageable()` | `Pageable` pronto para buscar a próxima fatia. |
| `getNumberOfElements()` | Quantidade real de elementos retornados. |

Não há `getTotalElements()` nem `getTotalPages()` em `Slice` — essas informações simplesmente não existem nesse modelo.

---

### O custo do COUNT em tabela grande

A query `COUNT(*)` precisa varrer todos os registros que satisfazem o filtro para retornar o total. Em tabelas com milhões de linhas e filtros que não usam índices eficientes, essa contagem pode ser mais lenta do que a própria query de dados.

Comparação de custo por caso de uso:

| Cenário | Abstração recomendada | Motivo |
|---|---|---|
| UI com paginação numérica ("Página 3 de 47") | `Page<T>` | O total é exibido na tela. |
| Feed, lista infinita, "carregar mais" | `Slice<T>` | Total irrelevante; basta saber se há mais. |
| Tabela muito grande, offset alto | Keyset / cursor-based | Offset alto varre linhas desnecessárias no banco. |

---

## Na prática

```java
// Repositório com as duas variantes
public interface OrderRepository extends JpaRepository<Order, Long> {

    // Retorna total de pedidos e total de páginas — usa COUNT extra
    Page<Order> findByStatus(OrderStatus status, Pageable pageable);

    // Retorna apenas se há próxima fatia — sem COUNT
    Slice<Order> findByCustomer(Customer customer, Pageable pageable);
}
```

```java
// Serviço usando Page para tela administrativa
public Page<Order> listOrdersByStatus(OrderStatus status, int page, int size) {
    Pageable pageable = PageRequest.of(page, size,
            Sort.by("createdAt").descending());

    Page<Order> result = orderRepository.findByStatus(status, pageable);

    long total   = result.getTotalElements(); // total de pedidos com esse status
    int  pages   = result.getTotalPages();    // total de páginas
    List<Order> orders = result.getContent(); // pedidos da página atual

    return result;
}
```

```java
// Serviço usando Slice para feed de pedidos do cliente
public Slice<Order> feedOrdersByCustomer(Customer customer, int page, int size) {
    Pageable pageable = PageRequest.of(page, size,
            Sort.by("createdAt").descending());

    Slice<Order> slice = orderRepository.findByCustomer(customer, pageable);

    boolean hasMore = slice.hasNext(); // true se existir próxima fatia
    List<Order> orders = slice.getContent();

    return slice;
}
```

```java
// Navegação encadeada com Slice
Pageable current = PageRequest.of(0, 20, Sort.by("createdAt").descending());
Slice<Order> slice = orderRepository.findByCustomer(customer, current);

while (slice.hasNext()) {
    Pageable next = slice.nextPageable();
    slice = orderRepository.findByCustomer(customer, next);
}
```

---

## Armadilhas

### (1) Usar `Page` quando só se precisa de "há mais?"

Toda chamada a um método que retorna `Page<T>` dispara uma query `COUNT` extra no banco. Se a interface apenas exibe "carregar mais" ou navega por um feed, troque para `Slice<T>` — elimina o count sem mudar a lógica de negócio.

### (2) `Sort` por campo sem índice

Ordenar por uma coluna sem índice força o banco a materializar todos os registros filtrados em memória para depois ordená-los (filesort/sort on disk). Antes de expor um campo como critério de ordenação em produção, verifique se existe índice adequado — especialmente em tabelas grandes.

### (3) Deep pagination — offset alto em tabela grande

`PageRequest.of(500, 20)` instrui o banco a **varrer e descartar** os primeiros 10.000 registros antes de retornar os 20 desejados. O custo cresce linearmente com o número da página. Para feeds ou históricos com muitas páginas, considere paginação baseada em cursor (keyset pagination), que substitui o `OFFSET` por uma cláusula `WHERE id > lastSeenId`.

> [!tip] Unpaged é uma armadilha silenciosa
> `Pageable.unpaged()` retorna **todos** os registros de uma vez. É útil em testes, mas nunca deve chegar à produção em rotas de volume alto.

---

## Em entrevista

### Frase pronta (inglês)

"Spring Data supports pagination through the `Pageable` abstraction. When a repository method returns `Page<T>`, Spring Data fires an additional `COUNT` query to compute the total number of elements and pages — which is necessary for a numbered pagination UI but adds overhead on every request. When you only need to know whether there is a next page, returning `Slice<T>` is more efficient because it skips that count query entirely. For very large tables with high page offsets, even `Slice` can be slow due to offset scanning, so cursor-based pagination — rewriting the offset as a `WHERE id > lastSeenId` clause — is the right tool."

### Vocabulário

| Português | Inglês |
|---|---|
| Paginação | Pagination |
| Ordenação | Sorting |
| Página | Page |
| Fatia | Slice |
| Contagem total | Total count |
| Paginação baseada em cursor | Cursor-based pagination |
| Deslocamento | Offset |
| Critério de ordenação | Sort criterion |

---

## Veja também

- [[03-Dominios/Java/Persistência de dados/08 - O problema N+1 e suas soluções — @EntityGraph, JOIN FETCH, batch size|O problema N+1]]
- [[03-Dominios/Java/Persistência de dados/04 - Spring Data repositories — JpaRepository e query methods derivados|Spring Data repositories]]
- [[API Design]] ← paginação cursor-based
- [[03-Dominios/Java/Persistência de dados/index|Persistência de dados (MOC do galho)]]
- [[03-Dominios/Java/index|Trilha Java]]
- [[03-Dominios/Java/Dicionário de Java#Pageable / Page / Slice|Pageable / Page / Slice]]

---

## Referências

- Spring Data Commons — `Slice` interface: <https://docs.spring.io/spring-data/commons/docs/current/api/org/springframework/data/domain/Slice.html>
- Spring Data Commons — `Page` interface: <https://docs.spring.io/spring-data/commons/docs/current/api/org/springframework/data/domain/Page.html>
- Spring Data JPA Reference — Query Methods Details (paging e sorting): <https://docs.spring.io/spring-data/jpa/reference/repositories/query-methods-details.html>
- Spring Data JPA Reference — Core Concepts: <https://docs.spring.io/spring-data/jpa/reference/repositories/core-concepts.html>
