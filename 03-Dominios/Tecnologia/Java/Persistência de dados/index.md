---
title: "Persistência de dados"
created: 2026-06-09
updated: 2026-06-11
type: moc
status: growing
publish: true
tags:
  - java
  - persistencia
  - moc
aliases:
  - "Persistência de dados"
  - "JPA"
  - "Hibernate"
  - "Spring Data JPA"
  - "Galho 10 - Persistência"
---
# Persistência de dados

> [!abstract] TL;DR
> O **Galho 10** da trilha Java Senior cobre a **camada de dados sobre a spec JPA do Galho 7**: entidades e o persistence context, mapeamento de relacionamentos, fetch strategies e o problema N+1, Spring Data repositories e consultas, paginação, transações operacionais, locking, caching e migrations de schema. São **17 notas atômicas** em 3 fases (Iniciado/Adepto/Magus), cada uma com seção "Em entrevista" em inglês.

## Sobre este galho

Persistência de dados é como o seu domínio vira linhas no banco e volta — sem cair nas armadilhas clássicas (N+1, `LazyInitializationException`, transação que não faz rollback, entidade vazando no JSON). O galho parte do básico operacional (a entidade, o persistence context, o repositório) e sobe até decisões de arquitetura (transações, locking, caching, migrations sem downtime).

**Audiência primária:** dev pleno/senior que usa Spring Data JPA no dia a dia e quer dominar o que acontece por baixo. **Secundária:** quem se prepara pra entrevista internacional e precisa explicar fetch strategies, o N+1 e transações com fluência.

Este galho tem **tripla fronteira**: este galho **operacionaliza as specs do Galho 7** ([[03-Dominios/Tecnologia/Java/Jakarta EE/index|Jakarta EE]] — JPA, EntityManager, JTA), **usa o mecanismo AOP do Galho 8** ([[03-Dominios/Tecnologia/Java/Spring Core e Boot/index|Spring Core e Boot]] — o proxy que faz o `@Transactional` funcionar) e **alimenta a borda do Galho 9** ([[03-Dominios/Tecnologia/Java/Web e APIs REST/index|Web e APIs REST]] — a entidade vira DTO antes de virar JSON). As notas linkam de volta a essas fronteiras sem re-explicá-las. Persistência reativa/R2DBC é o galho [[03-Dominios/Tecnologia/Java/Programação Reativa/13 - R2DBC — persistência reativa sem EntityManager|Programação Reativa]]; segurança (incluindo a ponte com `AuditorAware`/`SecurityContext`) é o galho [[03-Dominios/Tecnologia/Java/Segurança/index|Segurança]]; testes de repositório são o galho [[03-Dominios/Tecnologia/Java/Testes/10 - @DataJpaTest — testando repositories|Testes]]; dados distribuídos/consistência é o galho [[03-Dominios/Tecnologia/Java/Microservices e sistemas distribuídos/20 - Consistência em sistemas distribuídos|Microservices e sistemas distribuídos]].

## Iniciado

Vocabulário e modelo mental — o suficiente pra começar com confiança.

1. [[03-Dominios/Tecnologia/Java/Persistência de dados/01 - O que é a camada de persistência — Spring Data, JPA e Hibernate|O que é a camada de persistência — Spring Data, JPA e Hibernate]] — a pilha (Spring Data → spec JPA → Hibernate → JDBC) e a tripla fronteira numa frase.
2. [[03-Dominios/Tecnologia/Java/Persistência de dados/02 - A entidade JPA — @Entity, @Id e geração de chave|A entidade JPA — @Entity, @Id e geração de chave]] — `@Entity`/`@Id`/`@GeneratedValue` (UUID na JPA 3.1), `equals`/`hashCode` por business key.
3. [[03-Dominios/Tecnologia/Java/Persistência de dados/03 - O persistence context e os estados da entidade|O persistence context e os estados da entidade]] — transient/managed/detached/removed, cache de 1º nível, dirty checking.
4. [[03-Dominios/Tecnologia/Java/Persistência de dados/04 - Spring Data repositories — JpaRepository e query methods derivados|Spring Data repositories — JpaRepository e query methods derivados]] — a hierarquia de repositórios e as queries derivadas do nome do método.
5. [[03-Dominios/Tecnologia/Java/Persistência de dados/05 - Relacionamentos — @ManyToOne, @OneToMany e o owning side|Relacionamentos — @ManyToOne, @OneToMany e o owning side]] — owning vs inverse, `mappedBy`, helper methods, defaults de fetch.

## Adepto

Domínio operacional — usar com critério.

6. [[03-Dominios/Tecnologia/Java/Persistência de dados/06 - @ManyToMany, @OneToOne, cascade e orphanRemoval|@ManyToMany, @OneToOne, cascade e orphanRemoval]] — o resto do mapeamento e a semântica de cascade.
7. [[03-Dominios/Tecnologia/Java/Persistência de dados/07 - Fetch strategies — LAZY, EAGER e a LazyInitializationException|Fetch strategies — LAZY, EAGER e a LazyInitializationException]] — a decisão central da JPA; OSIV (desabilite em produção).
8. [[03-Dominios/Tecnologia/Java/Persistência de dados/08 - O problema N+1 e suas soluções — @EntityGraph, JOIN FETCH, batch size|O problema N+1 e suas soluções — @EntityGraph, JOIN FETCH, batch size]] — o bug mais caro da JPA, detecção e as soluções.
9. [[03-Dominios/Tecnologia/Java/Persistência de dados/09 - Consultas com @Query — JPQL, native e @Modifying|Consultas com @Query — JPQL, native e @Modifying]] — JPQL vs SQL nativo e o UPDATE/DELETE em massa.
10. [[03-Dominios/Tecnologia/Java/Persistência de dados/10 - Projections e DTOs — não vazar a entidade|Projections e DTOs — não vazar a entidade]] — interface/class/dynamic projections; a borda recebe DTO.
11. [[03-Dominios/Tecnologia/Java/Persistência de dados/11 - Paginação e ordenação — Pageable, Page e Slice|Paginação e ordenação — Pageable, Page e Slice]] — `Page` (com count) vs `Slice` (sem count) e o custo da paginação.

## Magus

Maestria e decisões de arquitetura.

12. [[03-Dominios/Tecnologia/Java/Persistência de dados/12 - Transações operacionais — @Transactional propagação, isolamento, rollback, readOnly|Transações operacionais — @Transactional propagação, isolamento, rollback, readOnly]] — o comportamento transacional; o mecanismo (proxy AOP) é do Galho 8.
13. [[03-Dominios/Tecnologia/Java/Persistência de dados/13 - Locking — optimistic (@Version) e pessimistic|Locking — optimistic (@Version) e pessimistic]] — lost update, `@Version` e `SELECT ... FOR UPDATE`.
14. [[03-Dominios/Tecnologia/Java/Persistência de dados/14 - Caching — 1º nível, 2º nível e Spring Cache|Caching — 1º nível, 2º nível e Spring Cache]] — os três níveis e quando usar o L2.
15. [[03-Dominios/Tecnologia/Java/Persistência de dados/15 - Consultas dinâmicas e os limites da JPA — Specifications, Criteria e SQL|Consultas dinâmicas e os limites da JPA — Specifications, Criteria e SQL]] — filtros dinâmicos e quando descer pro SQL.
16. [[03-Dominios/Tecnologia/Java/Persistência de dados/16 - Migrations de schema — Flyway, Liquibase e expand-and-contract|Migrations de schema — Flyway, Liquibase e expand-and-contract]] — versionar o schema e mudar sem downtime.
17. [[03-Dominios/Tecnologia/Java/Persistência de dados/17 - Capstone — Uma query do repositório ao banco, sem cair no N+1|Capstone — Uma query do repositório ao banco, sem cair no N+1]] — o trace ponta-a-ponta e o checklist de design.

## Rotas alternativas

- **Completa** — 01 → 17, na ordem.
- **Entrevista internacional** — 01 → 03 → 05 → 07 → 08 → 12 → 17 (pilha, persistence context, relacionamentos, fetch, N+1, transações, capstone — o que mais cai).
- **Caçando o N+1** — 05 → 07 → 08 → 10 → 17 (relacionamentos, fetch, N+1, projections, capstone).
- **Projetando a camada de persistência** — 02 → 05 → 07 → 10 → 11 → 12 → 16 (entidade, relação, fetch, DTO, paginação, transação, migration).
- **Persistência sobre Jakarta EE** (a ponte com o Galho 7) — 01 → 03 → 12 + as notas do Galho 7 ([[03-Dominios/Tecnologia/Java/Jakarta EE/09 - JPA — a especificação de persistência|JPA]], [[03-Dominios/Tecnologia/Java/Jakarta EE/10 - EntityManager e o ciclo de vida da entidade|EntityManager]], [[03-Dominios/Tecnologia/Java/Jakarta EE/11 - JTA — transações na plataforma|JTA]]).

## Veja também

- [[03-Dominios/Tecnologia/Java/index|Trilha Java]] — a estante completa (18 galhos)
- [[03-Dominios/Tecnologia/Java/Jakarta EE/index|Jakarta EE]] — as specs que este galho operacionaliza (JPA, EntityManager, JTA)
- [[03-Dominios/Tecnologia/Java/Spring Core e Boot/index|Spring Core e Boot]] — o mecanismo AOP do `@Transactional`
- [[03-Dominios/Tecnologia/Java/Web e APIs REST/index|Web e APIs REST]] — a borda que consome a persistência (DTO vs entidade)
- [[03-Dominios/Ciência/Banco de Dados/index|Banco de dados]] — SQL, ACID, índices, isolamento (a teoria)
- [[03-Dominios/Tecnologia/Java/Dicionário de Java|Dicionário de Java]] — glossário de termos da trilha

> Galhos 11 (Programação Reativa/R2DBC), 12 (Segurança), 13 (Testes), 14 (Mensageria), 16 (Microservices) e 17 (Cloud-native) — planejados.
