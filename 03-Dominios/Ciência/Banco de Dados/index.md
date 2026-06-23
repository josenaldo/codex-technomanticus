---
title: "Banco de Dados"
created: 2026-06-17
updated: 2026-06-17
type: moc
status: growing
publish: true
tags:
  - fundamentos
  - banco-de-dados
  - sql
  - entrevista
  - moc
aliases:
  - Banco de Dados
  - Banco de dados
  - Bancos de Dados
  - Banco de Dados Relacional
  - Database
  - Galho - Banco de Dados
---

# Banco de Dados

> [!abstract] TL;DR
> Galho de Ciência da Computação sobre como software guarda, consulta e protege dados. Coração do
> relacional — **modelo, SQL, transações (ACID), índices, performance e concorrência** — com
> um tratamento honesto de **distribuídos** e **NoSQL**. Para um senior, o banco raramente é
> só persistência: é onde vivem as garantias de consistência, os maiores ganhos de performance
> e os bugs mais caros. Interview-critical.

## Sobre este galho

A narrativa default é **PostgreSQL** (o ferramental mais rico de índice e o melhor valor
didático); MySQL/InnoDB e SQLite entram **só onde divergem de verdade** e cai em entrevista.
O galho é stack-agnóstico em SQL/modelagem/transações e **linka** a estante Java onde a mecânica
é específica de framework.

**Fronteiras (linka, não duplica):**
- **B-Tree/B+Tree como estrutura** → [[09 - Árvores B e índices]] (galho Estruturas de Dados). Aqui
  a nota de Índices foca em **uso**: que índice criar, quando, a que custo.
- **Scale-out de sistema** (replicação/sharding/CAP na escala de arquitetura) → [[System Design]].
- **Saga/Outbox como padrões de mensageria** → [[Mensageria]] / [[Arquitetura de Software]]. Aqui
  fica o lado-banco (o *dual-write problem*, 2PC, por que Outbox resolve).
- **JPA/Hibernate/Spring Data** → [[Spring Boot]]. O galho trata SQL/transações; o ORM linka.

**Audiência:** dev senior em preparação para entrevista internacional. Cada nota tem seção
"Em entrevista" com frases prontas em inglês e vocabulário técnico.

## Iniciado — o modelo, a linguagem, a modelagem

1. [[01 - O que é um banco de dados]] — persistência, SGBD, o modelo relacional como mapa, SQL como linguagem.
2. [[02 - O modelo relacional]] — tabelas, tuplas, schema, chaves (PK/FK), integridade referencial, constraints.
3. [[03 - SQL - consultas]] — SELECT/WHERE, os JOINs, GROUP BY/HAVING, ORDER BY, subqueries.
4. [[04 - Modelagem e normalização]] — 1NF→BCNF, desnormalização intencional, relacionamentos, chaves e IDs.

## Adepto — transações, índices, performance

5. [[05 - Transações e ACID]] — atomicidade/consistência/isolamento/durabilidade, WAL, commit/rollback.
6. [[06 - Isolamento e anomalias]] — dirty/non-repeatable/phantom/lost-update/write-skew, MVCC, snapshot isolation.
7. [[07 - Índices]] — que índice criar e quando; tipos, composto + leftmost prefix, seletividade.
8. [[08 - EXPLAIN e otimização]] — ler o plano de execução, tipos de scan, join strategies, quando *não* indexar.
9. [[09 - SQL avançado]] — window functions, CTEs (+ recursivas), LATERAL, upsert, keyset pagination.
10. [[10 - Performance e armadilhas]] — N+1, queries lentas, tabelas gigantes, SELECT *, OFFSET alto, leaks.

## Magus — concorrência, distribuídos, NoSQL, produção

11. [[11 - Concorrência e locking]] — optimistic vs pessimistic, deadlock, SKIP LOCKED, lock contention.
12. [[12 - Replicação, sharding e CAP]] — read replicas, sharding, CAP/PACELC, eventual consistency.
13. [[13 - Transações distribuídas]] — dual-write problem, 2PC, Saga, Outbox.
14. [[14 - NoSQL e polyglot persistence]] — as famílias, BASE×ACID, quando escolher, "comece com Postgres".
15. [[15 - Operação em produção]] — migrations zero-downtime, backup/PITR, replicação, observabilidade.
16. [[16 - Banco de dados em entrevista]] — system design de dados, defender escolhas, cheat-sheet, inglês.

## Rotas alternativas

### Entrevista internacional
01 → 04 → 05 → 06 → 07 → 08 → 16. O modelo, a modelagem, transações/isolamento, índices/EXPLAIN e o capstone.

### Performance de queries
03 → 07 → 08 → 09 → 10. SQL, índices, leitura de plano, SQL avançado e as armadilhas.

### Dados distribuídos
05 → 06 → 12 → 13 → 14. Transações e isolamento como base, depois replicação, distribuídas e NoSQL.

## Todas as notas

```dataview
TABLE fase, status, updated
FROM "03-Dominios/Ciência/Banco de Dados"
WHERE type = "concept"
SORT file.name ASC
```

## Veja também

- [[03-Dominios/Ciência/index|Fundamentos (MOC do domínio)]]
- [[09 - Árvores B e índices]] — como o índice é implementado por dentro (galho Estruturas de Dados)
- [[System Design]] — replicação/sharding/CAP na escala de arquitetura
- [[Arquitetura de Software]] — Saga, Outbox e consistência distribuída em sistemas
- [[Spring Boot]] — JPA, Hibernate, `@Transactional`, `@Version`
- [[Dicionário de Ciência da Computação]]
