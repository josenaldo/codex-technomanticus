---
title: "Acesso a Dados"
created: 2026-07-28
updated: 2026-07-28
type: moc
status: evergreen
publish: true
tags:
  - moc
  - design-de-software
  - acesso-a-dados
  - persistencia
aliases:
  - Acesso a Dados
  - Padrões de Acesso a Dados
  - Data Source Patterns
  - Galho - Acesso a Dados
---

# Acesso a Dados

> [!abstract] TL;DR
> Os padrões que resolvem **como um objeto conversa com o armazenamento** — todos nascidos do
> **descasamento objeto-relacional**. Segunda família do galho-pai
> [[03-Dominios/Engenharia/Design de Software/Padrões de Projeto/index|Padrões de Projeto]], tratada
> como catálogo de consulta. A lente aqui não é a linguagem, é o **ORM**: qual framework encarna qual
> padrão (Active Record = Rails/Django; Data Mapper = Hibernate/SQLAlchemy). Eixo dorsal: **Active
> Record × Data Mapper**.

## Sobre esta família

Repertório de consulta para o sênior — inclusive em legado, onde DAOs de 2008, Active Records
inchados e Table Modules .NET ainda vivem. Cada nota é autocontida; a seção **Armadilhas** pesa no
*quando não usar*. Sobreposição com [[03-Dominios/Tecnologia/Java/index|Java (persistência)]] e
[[03-Dominios/Engenharia/Dados/index|Engenharia de Dados]] é intencional (cross-link como "aprofunde").

**Fora de escopo:** Cache-Aside, sharding, read-replicas → infra/resiliência (família Nuvem e
Resiliência) e [[03-Dominios/Tecnologia/Cloud/index|Cloud]].

## Iniciado — onde mora a lógica + entrada

1. [[01 - Panorama do acesso a dados]] — o descasamento objeto-relacional, o mapa da família, a lente cross-ORM.
2. [[02 - Transaction Script]] — lógica procedural por caso de uso; simples, e onde apodrece.
3. [[03 - Domain Model]] — lógica rica nos objetos; rico × anêmico; o coração do DDD.
4. [[04 - Table Module]] — um objeto por tabela sobre um Record Set (habitat .NET).
5. [[05 - DAO (Data Access Object)]] — a interface de acesso do J2EE; DAO × Repository.
6. [[06 - Active Record]] — o objeto que é a linha e sabe se salvar; metade do eixo dorsal.

## Adepto — mapper, repository e maquinaria de ORM

7. [[07 - Gateways]] — wrappers finos de linha e de tabela (Record Set); o encanamento que os ORMs absorveram.
8. [[08 - Data Mapper]] — a camada que isola domínio e banco; a outra metade do eixo dorsal.
9. [[09 - Repository]] — coleção-em-memória sobre o mapper; Repository × DAO revisitado.
10. [[10 - Unit of Work]] — rastreia mudanças e persiste numa transação (Session/EntityManager/DbContext).
11. [[11 - Identity Map]] — uma instância por linha na sessão; o cache L1; L1 × L2.
12. [[12 - Lazy Load]] — carregar sob demanda via proxy; a origem do N+1 e da `LazyInitializationException`.
13. [[13 - Query Object]] — a consulta como objeto componível e type-safe; a saída para a explosão de `findByXAndY`.

## Magus — NoSQL e nuvem remodelam

14. [[14 - Modelagem por agregado e single-table design]] — o NoSQL inverte o design: *query-first*, agregado, single-table no DynamoDB.
15. [[15 - Polyglot persistence e materialized views]] — o banco certo para cada carga; read models, CQRS e o mapa de escolha da família.

## Rotas alternativas

### O eixo dorsal (o debate central)
01 → 06 (Active Record) → 08 (Data Mapper) → 09 (Repository). As duas filosofias rivais e a abstração de coleção sobre elas.

### Legado enterprise
01 → 05 (DAO) → 06 (Active Record) → 07 (Gateways) → 10 (Unit of Work). Os padrões que você encontra em sistemas antigos.

## Todas as notas

```dataview
TABLE fase, status, updated
FROM "03-Dominios/Engenharia/Design de Software/Padrões de Projeto/Acesso a Dados"
WHERE type = "concept"
SORT file.name ASC
```

## Veja também

- [[03-Dominios/Engenharia/Design de Software/Padrões de Projeto/index|Padrões de Projeto]] — o galho-pai e as outras famílias.
- [[03-Dominios/Engenharia/Design de Software/Padrões de Projeto/Clássicos (GoF)/index|Clássicos (GoF)]] — a primeira família (os 23 padrões clássicos).
- [[03-Dominios/Tecnologia/Java/index|Java]] · [[03-Dominios/Engenharia/Dados/index|Engenharia de Dados]]
