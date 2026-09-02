---
title: "Go — Persistência"
type: moc
publish: true
created: 2026-07-18
updated: 2026-07-18
status: growing
tags:
  - moc
  - go
  - database
  - sql
  - persistencia
aliases:
  - Galho 11 Go
---
# Go — Persistência

> [!abstract] TL;DR
> Galho 11 da trilha [[03-Dominios/Tecnologia/Go/index|Go]] — como programas Go conversam com bancos de dados. 8 notas em 3 fases: o contrato `database/sql` (Iniciado); pool de conexões, o padrão manual de Query/Scan, e os três caminhos mais usados em produção — pgx, sqlc e GORM (Adepto); migrations e o padrão repository sobre transações (Magus). Ao fim, você escolhe entre driver puro, codegen ou ORM com critério, e sabe orquestrar transações sem vazar `*sql.DB` pelo código.

Go não tem ORM embutido na stdlib — tem um contrato mínimo, `database/sql`, sobre o qual o ecossistema construiu camadas de conveniência com trade-offs bem diferentes entre si.

## Notas por fase

### Iniciado — o contrato

1. [[01 - database-sql — o contrato]] — `sql.DB` não é uma conexão, é um pool; `sql.Open` é preguiçoso; a interface `driver.Driver`

### Adepto — os caminhos de acesso

2. [[02 - Connection pool]] — `MaxOpenConns`, `MaxIdleConns`, `ConnMaxLifetime`, exaustão de pool em produção
3. [[03 - Query, Scan e o mapeamento manual]] — `Query` vs `QueryRow` vs `Exec`, `Scan` linha a linha, `rows.Close()`, SQL injection e placeholders
4. [[04 - pgx — o driver Postgres avançado]] — por que pgx além de `lib/pq`, pool nativo, tipos Postgres nativos, `pgxpool`
5. [[05 - sqlc — SQL type-safe por codegen]] — SQL como fonte da verdade, geração de código Go tipado, trade-off vs ORM
6. [[06 - GORM — o ORM]] — modelos, migrations automáticas, associations, o preço da mágica (N+1, lazy loading)

### Magus — orquestração e evolução do schema

7. [[07 - Migrations]] — golang-migrate, versionamento de schema, up/down, migrations em CI/CD
8. [[08 - Transações e o padrão repository]] — `Begin`/`Commit`/`Rollback`, propagação de transação, interface repository desacoplada do driver

## Veja também

- [[03-Dominios/Tecnologia/Go/index|Trilha Go]] — índice geral (21 galhos + capstone)
- Galho anterior: [[03-Dominios/Tecnologia/Go/index|Trilha Go]] (galho 10 — HTTP e frameworks web)
- Próximo galho: **gRPC e protobuf** (galho 12) — onde a comunicação entre serviços troca REST por contratos binários fortemente tipados
