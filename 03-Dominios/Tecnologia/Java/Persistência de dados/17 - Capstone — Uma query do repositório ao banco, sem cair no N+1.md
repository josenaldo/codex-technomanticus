---
title: "Capstone — Uma query do repositório ao banco, sem cair no N+1"
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
  - jpa
aliases:
  - "Capstone Persistência"
  - "Query do repositório ao banco"
---

# Capstone — Uma query do repositório ao banco, sem cair no N+1

> [!abstract] TL;DR
> Uma única query atravessa uma pilha inteira: o **proxy do Spring Data** intercepta a chamada do repositório → traduz para **JPQL/Criteria** → o **Hibernate** monta o **SQL** → o **persistence context** registra o que será gerenciado → o **JDBC** dispara a query → o **`ResultSet`** volta → vira **entidades managed** → projeta-se um **DTO** na borda. Projetar a camada de dados é dominar esse caminho inteiro sem cair no **N+1**. O capstone amarra todo o Galho 10 num único trace e num checklist de design production-grade.

## O que é

Este é o capstone do Galho 10. Em vez de introduzir um conceito novo, ele faz duas coisas que nenhuma nota isolada faz: (1) segue **uma chamada de método de repositório do início ao fim**, mostrando cada engrenagem que ela aciona, e (2) condensa as decisões de projeto recorrentes num **checklist de design** que separa código de demonstração de código de produção.

O fio condutor é uma chamada banal:

```java
Page<OrderDto> page = orderRepository.findAll(spec, pageable);
```

Parece uma linha. Por baixo dela há um proxy gerado em runtime, uma árvore de `Specification` virando predicados Criteria, um tradutor JPQL/Criteria → SQL, um persistence context que decide o que rastrear, uma chamada JDBC, um `ResultSet` materializado em entidades managed e — se você não cuidar — N consultas extras escondidas atrás de cada relacionamento LAZY.

## Por que importa

A maioria dos bugs de performance em aplicações Java não nasce de um algoritmo ruim no domínio: nasce na **fronteira com o banco**. O N+1 é o exemplo arquetípico — uma query vira centenas porque cada entidade da lista dispara um `SELECT` adicional ao tocar num relacionamento. Quem enxerga o repositório como uma "caixa que devolve objetos" não tem onde intervir. Quem enxerga a **pilha inteira** sabe exatamente em que camada cada decisão pesa: o fetch plan se resolve no JPQL/Criteria, a tradução acontece no Hibernate, o ciclo de vida da entidade vive no persistence context, e o limite transacional é demarcado por um proxy AOP.

Em entrevista sênior, a pergunta raramente é "o que é JPA". É "explique o que acontece quando você chama esse método" e "onde o N+1 entra nessa história". Saber o trace é o que separa quem usa o framework de quem o entende.

## Como funciona

### Trace: `repo.findAll(spec, pageable)` da chamada ao banco e de volta

O caminho de ida e volta, em uma linha cada:

```text
1. chamada de método      orderRepository.findAll(spec, pageable)
   ↓
2. proxy Spring Data      proxy gerado em runtime intercepta; delega a SimpleJpaRepository
   ↓
3. JPQL/Criteria          a Specification vira Predicates de uma CriteriaQuery; Pageable vira LIMIT/OFFSET + count
   ↓
4. tradução p/ SQL        o Hibernate traduz a Criteria em SQL dialetal (paginação + join do fetch plan)
   ↓
5. persistence context    o EntityManager (1st-level cache) prepara o registro das entidades a materializar
   ↓
6. JDBC                   PreparedStatement parametrizado é executado contra a conexão do pool
   ↓
7. ResultSet              o banco devolve linhas; o Hibernate lê o ResultSet coluna a coluna
   ↓
8. entidades managed      cada linha vira uma entidade hidratada e registrada como MANAGED no contexto
   ↓
9. projeção / DTO         um mapeamento converte a entidade managed em OrderDto (borda da aplicação)
```

Pontos que merecem destaque no trace:

- **Passo 2 — o proxy não é decoração.** O `SimpleJpaRepository` por trás do proxy é quem realmente fala com o `EntityManager`. O método derivado ou a `Specification` são montados aqui. Veja [[03-Dominios/Tecnologia/Java/Persistência de dados/04 - Spring Data repositories — JpaRepository e query methods derivados|Spring Data repositories]].
- **Passo 3 — `Pageable` gera duas queries.** Uma de dados (com `LIMIT`/`OFFSET`) e uma de `count` para o total. Isso é esperado e não é N+1 — é o preço da paginação. Veja [[03-Dominios/Tecnologia/Java/Persistência de dados/11 - Paginação e ordenação — Pageable, Page e Slice|Paginação e ordenação]].
- **Passo 4 — o fetch plan decide os JOINs.** Se o `@EntityGraph` ou um `JOIN FETCH` estiver presente, os relacionamentos vêm na **mesma** query. Se não estiver, eles ficam LAZY — e é aqui que o N+1 se esconde para detonar no passo 9.
- **Passo 8 — managed significa rastreado.** Toda entidade hidratada entra no persistence context e passa a ser observada por dirty checking. Se você só vai ler, isso é overhead puro (daí `readOnly=true`).
- **Passo 9 — a projeção é a defesa.** Converter para DTO **antes** de a entidade escapar do contexto evita tanto vazamento de domínio no JSON quanto `LazyInitializationException` na serialização. Veja [[03-Dominios/Tecnologia/Java/Persistência de dados/10 - Projections e DTOs — não vazar a entidade|Projections e DTOs]].

### O caminho transacional (o proxy AOP abre a tx → dirty checking → commit)

Paralelo ao trace de dados corre o trace **transacional**, que é o que dá segurança ao trace de dados:

```text
@Transactional no método de serviço
   ↓
proxy AOP do Spring intercepta a chamada (advice around)
   ↓
abre / participa de uma transação  → vincula um EntityManager ao thread
   ↓
[ executa o corpo do método: o trace de dados acima roda aqui dentro ]
   ↓
no retorno: flush → dirty checking compara o snapshot das entidades managed
   ↓
gera UPDATE/INSERT/DELETE para o que mudou
   ↓
commit (ou rollback se exceção de runtime escapou)
```

Três fatos que costumam confundir:

- **O `@Transactional` é um proxy, não mágica.** É exatamente o mesmo mecanismo de [[03-Dominios/Tecnologia/Java/Spring Core e Boot/09 - AOP e proxies no Spring|AOP e proxies]]: um advice envolve o método. Por isso a auto-invocação (chamar um método `@Transactional` de dentro da mesma classe) **não** abre transação — o proxy é contornado.
- **O `flush` é implícito.** Você raramente chama `flush()` à mão; ele acontece no commit (e antes de queries que possam ser afetadas por mudanças pendentes). O dirty checking compara o estado atual com o snapshot capturado na hidratação.
- **Rollback é por exceção de runtime.** Por padrão, só `RuntimeException`/`Error` disparam rollback. Checked exceptions **não** revertem a menos que declaradas em `rollbackFor`. Veja [[03-Dominios/Tecnologia/Java/Persistência de dados/12 - Transações operacionais — @Transactional propagação, isolamento, rollback, readOnly|Transações operacionais]].

### Galho 10 → spec Jakarta (Galho 7)

O Galho 10 ensina a usar persistência **na prática** (Spring Data + Hibernate). Mas quase tudo o que parece "feature do Spring" é, na verdade, uma **especificação Jakarta** com um mecanismo do Spring por cima. Esta tabela é o mapa de quitação da dívida conceitual:

| Conceito do Galho 10 (prática) | É, na verdade… | Onde mora |
| --- | --- | --- |
| `@Entity`, `@Id`, `@ManyToOne` | **JPA** (a spec) — anotações e modelo | `jakarta.persistence.*` |
| persistence context / estados (transient, managed, detached, removed) | o **`EntityManager`** da JPA | spec JPA (Galho 7) |
| `@Query`, JPQL | **JPQL**, a query language da JPA | spec JPA (Galho 7) |
| `JpaRepository`, query methods | **proxy AOP do Spring** sobre `SimpleJpaRepository` | Spring Data (mecanismo) |
| `@Transactional` | demarcação de transação ≈ **JTA** | spec JTA (Galho 7) + proxy AOP do Spring (Galho 8) |
| Hibernate gerando o SQL | **implementação** da spec JPA | provider (Galho 7: spec ↔ impl) |

Para o lado Jakarta dessa tabela, veja [[03-Dominios/Tecnologia/Java/Jakarta EE/09 - JPA — a especificação de persistência|JPA (a spec)]] e [[03-Dominios/Tecnologia/Java/Jakarta EE/11 - JTA — transações na plataforma|JTA]].

## Na prática

### Checklist de design production-grade

Um repositório que passa no code review sênior costuma respeitar todos estes pontos:

- **Sempre LAZY por padrão.** Nunca `FetchType.EAGER` em coleções. EAGER é a porta de entrada do N+1 e tira de você o controle do fetch plan. Veja [[03-Dominios/Tecnologia/Java/Persistência de dados/07 - Fetch strategies — LAZY, EAGER e a LazyInitializationException|Fetch strategies]].
- **Fetch explícito, query a query.** Quando precisar do relacionamento, traga-o com `@EntityGraph`, `JOIN FETCH` ou batch size — **na própria query**, não por acidente de acesso. Sem N+1.
- **DTO não-entidade na borda.** A camada web nunca recebe a entidade managed. Projete para um `record`/DTO antes de sair do serviço.
- **`@Transactional(readOnly = true)` como default no Service.** Leitura é o caso comum; `readOnly` dispensa dirty checking e sinaliza intenção. Escritas sobrescrevem explicitamente.
- **`@Version` onde há concorrência.** Optimistic locking detecta lost update sem segurar lock pessimista. Sem ele, dois commits concorrentes se sobrescrevem em silêncio.
- **Migrations com expand-and-contract.** Schema evolui em duas fases (adiciona o novo compatível → migra → remove o velho), nunca num big-bang que quebra deploys em andamento.
- **OSIV (Open Session In View) desabilitado.** Mantê-lo ligado mascara `LazyInitializationException` ao custo de segurar a conexão durante toda a renderização e esconder N+1. Desligar força o fetch a ser explícito.

Um exemplo curto que junta vários pontos do checklist:

```java
import jakarta.persistence.EntityGraph;
import org.springframework.data.jpa.repository.EntityGraph.EntityGraphType;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Query;
import org.springframework.transaction.annotation.Transactional;
import java.util.List;

public interface OrderRepository extends JpaRepository<Order, Long> {

    // fetch explícito: traz os itens junto, na MESMA query — sem N+1
    @org.springframework.data.jpa.repository.EntityGraph(
            attributePaths = {"customer", "items"},
            type = EntityGraphType.LOAD)
    @Query("select o from Order o where o.customer.id = :customerId")
    List<Order> findByCustomer(Long customerId);
}
```

```java
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;
import java.util.List;

@Service
public class OrderQueryService {

    private final OrderRepository orders;

    public OrderQueryService(OrderRepository orders) {
        this.orders = orders;
    }

    // readOnly por padrão: sem dirty checking, intenção explícita
    @Transactional(readOnly = true)
    public List<OrderSummary> summariesFor(Long customerId) {
        return orders.findByCustomer(customerId).stream()
                // DTO na borda: a entidade managed NÃO escapa do serviço
                .map(OrderSummary::from)
                .toList();
    }
}
```

```java
// DTO não-entidade: imutável, sem proxy LAZY, seguro para serializar
public record OrderSummary(Long id, String customerName, int itemCount) {

    static OrderSummary from(Order order) {
        return new OrderSummary(
                order.getId(),
                order.getCustomer().getName(),   // já carregado pelo @EntityGraph
                order.getItems().size());         // idem — sem query extra
    }
}
```

## Armadilhas

### (1) "O repositório vai direto no banco"

A intuição de que `orderRepository.findAll(...)` é um atalho fino sobre o JDBC é a raiz de quase todo desentendimento de performance. Há uma **engrenagem inteira** entre a interface e o banco: um proxy AOP, um `SimpleJpaRepository`, um tradutor de Criteria/JPQL para SQL, um persistence context que decide o que rastrear e um `ResultSet` sendo hidratado linha a linha. Quem não enxerga essas camadas não sabe **onde** intervir quando a query degrada — e tenta otimizar no lugar errado (índice, JVM, cache de aplicação) enquanto o problema real é um fetch plan ausente.

### (2) "JPA resolve tudo"

JPA é excelente para o caminho OLTP (carregar, modificar, persistir agregados pequenos). Mas há um teto: relatórios analíticos, agregações pesadas, `GROUP BY` largos e projeções complexas pagam um preço alto se forçados pelo modelo de objetos. O erro de raciocínio é tratar a JPA como ferramenta universal e ignorar o **escape hatch**: query nativa, projeções planas, ou uma rota dedicada de leitura. Quem domina a camada sabe **quando sair dela**. Veja [[03-Dominios/Tecnologia/Java/Persistência de dados/15 - Consultas dinâmicas e os limites da JPA — Specifications, Criteria e SQL|SQL nativo e o escape hatch]].

### (3) "EAGER é mais simples"

`FetchType.EAGER` parece eliminar o problema do LAZY ("assim nunca dá `LazyInitializationException`"). É exatamente o contrário: EAGER em coleções faz cada carga de entidade arrastar todos os relacionamentos, e numa lista de N entidades isso vira o N+1 clássico — ou pior, um produto cartesiano de JOINs. O atalho aparente é a fonte do problema. O caminho correto é **LAZY por padrão + fetch explícito por query**: você decide, caso a caso, o que trazer junto. Veja [[03-Dominios/Tecnologia/Java/Persistência de dados/08 - O problema N+1 e suas soluções — @EntityGraph, JOIN FETCH, batch size|O problema N+1]].

## Em entrevista

### Frase pronta (inglês)

> When I call a Spring Data repository method, it isn't a thin wrapper over JDBC — a runtime proxy delegates to `SimpleJpaRepository`, which builds a JPQL or Criteria query that Hibernate translates into SQL, runs it through JDBC, and hydrates the `ResultSet` into managed entities inside the persistence context. The classic trap is the N+1 problem: if a relationship is LAZY and I touch it per row, one query silently becomes hundreds, so I fetch explicitly with an entity graph or a join fetch and project to a DTO at the boundary. All of this runs inside a transaction demarcated by an AOP proxy on `@Transactional`, where dirty checking on managed entities drives the UPDATEs at commit — which is why I default read paths to `readOnly` and reserve writes for explicit transactions.

### Vocabulário

| Termo (EN) | Tradução / sentido |
| --- | --- |
| persistence context | contexto de persistência; cache de 1º nível que rastreia entidades managed |
| dirty checking | detecção automática de mudanças nas entidades managed antes do flush |
| fetch plan | plano de carregamento — o que vem junto na query (graph/join fetch) |
| N+1 problem | uma query vira N+1 por acesso LAZY repetido em loop |
| optimistic locking | controle de concorrência por `@Version`, sem lock pessimista |
| entity graph | declaração de quais atributos trazer eagerly numa query específica |
| managed entity | entidade rastreada pelo persistence context (vs. detached/transient) |

### Cheatsheet

| Sintoma / Problema | Nota |
| --- | --- |
| N+1 — uma query virou centenas | [[03-Dominios/Tecnologia/Java/Persistência de dados/08 - O problema N+1 e suas soluções — @EntityGraph, JOIN FETCH, batch size|nota 08]] |
| `LazyInitializationException` na serialização | [[03-Dominios/Tecnologia/Java/Persistência de dados/07 - Fetch strategies — LAZY, EAGER e a LazyInitializationException|nota 07]] |
| vazou entidade no JSON / acoplou domínio à API | [[03-Dominios/Tecnologia/Java/Persistência de dados/10 - Projections e DTOs — não vazar a entidade|nota 10]] |
| checked exception não fez rollback | [[03-Dominios/Tecnologia/Java/Persistência de dados/12 - Transações operacionais — @Transactional propagação, isolamento, rollback, readOnly|nota 12]] |
| lost update sob concorrência | [[03-Dominios/Tecnologia/Java/Persistência de dados/13 - Locking — optimistic (@Version) e pessimistic|nota 13]] |
| JPA não dá conta do relatório analítico | [[03-Dominios/Tecnologia/Java/Persistência de dados/15 - Consultas dinâmicas e os limites da JPA — Specifications, Criteria e SQL|nota 15]] |

## Veja também

- [[03-Dominios/Tecnologia/Java/Persistência de dados/01 - O que é a camada de persistência — Spring Data, JPA e Hibernate|O que é a camada de persistência]]
- [[03-Dominios/Tecnologia/Java/Persistência de dados/08 - O problema N+1 e suas soluções — @EntityGraph, JOIN FETCH, batch size|O problema N+1]]
- [[03-Dominios/Tecnologia/Java/Persistência de dados/12 - Transações operacionais — @Transactional propagação, isolamento, rollback, readOnly|Transações operacionais]]
- [[03-Dominios/Tecnologia/Java/Jakarta EE/09 - JPA — a especificação de persistência|JPA (a spec)]]
- [[03-Dominios/Tecnologia/Java/Jakarta EE/11 - JTA — transações na plataforma|JTA]]
- [[03-Dominios/Tecnologia/Java/Spring Core e Boot/09 - AOP e proxies no Spring|AOP e proxies]]
- [[03-Dominios/Tecnologia/Java/Persistência de dados/index|Persistência de dados (MOC do galho)]]
- [[03-Dominios/Tecnologia/Java/index|Trilha Java]]

## Referências

- Spring Data JPA Reference — https://docs.spring.io/spring-data/jpa/reference/
- Hibernate ORM User Guide — https://docs.hibernate.org/orm/current/userguide/html_single/Hibernate_User_Guide.html
- Jakarta Persistence Specification — https://jakarta.ee/specifications/persistence/
- Jakarta Transactions Specification — https://jakarta.ee/specifications/transactions/
