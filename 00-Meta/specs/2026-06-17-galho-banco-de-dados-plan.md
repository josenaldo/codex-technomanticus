---
title: "Galho Banco de Dados — design e plano (Fundamentos, Camada A)"
created: 2026-06-17
type: plan
status: draft
publish: false
tags:
  - meta
  - plan
  - fundamentos
  - banco-de-dados
---

# Galho Banco de Dados — design e plano

## Contexto
Quinto galho da Camada A do meta-plano de Fundamentos (`2026-06-15-fundamentos-meta-planejamento-design.md`),
depois de **Estruturas de Dados**, **Algoritmos**, **OO** e **SOLID** (todos COMPLETOS, 2026-06-17).
Refatora o monólito `03-Dominios/Fundamentos/Banco de dados.md` (616 ln, evergreen) no padrão
tronco/galhos + 3 fases. Interview-critical (★). Aprovado pelo usuário em 2026-06-17.

A semente é o monólito inteiro: SQL/NoSQL, ACID, isolamento, modelagem, SQL essencial, índices,
performance, concorrência, CAP, transações distribuídas, operação em produção, armadilhas, e 4
experiências reais do usuário (preservar, [[feedback-no-fabrication]]).

## Decisões de escopo (aprovadas)

1. **Relacional a fundo + UMA nota honesta de NoSQL.** O galho é dono do relacional. NoSQL vira uma
   nota Magus (taxonomia das famílias, BASE×ACID, polyglot persistence, "comece com Postgres"). NÃO
   uma nota por família. Vector DB linka IA/RAG.
2. **Engine TARGETED, voz-padrão PostgreSQL.** Narrativa default PG. MySQL/InnoDB e SQLite só onde
   divergem de verdade e cai em entrevista (defaults de isolamento, MVCC heap+VACUUM × undo log,
   PK clusterizada InnoDB × heap PG, phantom no REPEATABLE READ). Drivers/ORMs = callout, não corpo.
3. **Teto de prosa 2400 (permissão, não alvo); código/SQL não conta.** Idêntico a ED/Algo/OO/SOLID.
4. **Fronteiras (linka, não duplica):** ver abaixo.

## Fronteiras (rígido)
- **Estruturas de Dados / nota 09 (Árvores B e índices)** é dona de B-Tree/B+Tree *como estrutura*.
  A nota 07 (Índices) foca em **uso** (que índice criar, quando, custo, leftmost prefix, seletividade)
  e **linka** ED/09 pro interno. Não reimplementa a estrutura.
- **Arquitetura (System Design / Mensageria / Event Storming)**: replicação/sharding/CAP (nota 12)
  ficam na escala-de-banco e **linkam** `[[System Design]]` pro scale-out de sistema. Saga/Outbox
  (nota 13) — a nota é dona do lado-banco (dual-write problem, 2PC, por que Outbox resolve) e
  **forward-linka** `[[Mensageria]]`/`[[Arquitetura de Software]]`/`[[Event Storming]]`.
- **Java (JPA/Hibernate/Spring Data)**: SQL/modelagem/transações stack-agnóstico; linka
  `[[Spring Boot]]` onde for específico (`@Transactional` é proxy, `@Version`, `@EntityGraph`,
  `JOIN FETCH`). Os exemplos N+1 do monólito (Java) viram exemplo enquadrado de forma agnóstica + link.

## Preservação (rígido) — experiências REAIS, relocadas do monólito
- **`total_avaliacoes` denormalizada via domain event** (lista de médicos no MedEspecialista) → **nota 04**.
- **Migração `BIGINT` → ULID** ao quebrar o monólito em serviços (gerar ID antes de publicar evento) → **nota 04**.
- **Índice composto `(paciente_id, data DESC)` derrubando endpoint de 2s → 30ms** via `EXPLAIN ANALYZE` → **nota 08**.
- **Batch noturno em transação-gigante** (rollback de horas) → lotes de 1000 + tabela de progresso → **nota 05**.
- **Migration `NOT NULL` sem default travando tabela de 20M linhas** 15 min → **nota 15**.
- **JPA produtivo mas 5% cai pro SQL nativo/JdbcTemplate** (hot paths/relatório) → **nota 10** (ou capstone).
- O `@Transactional` é proxy (não funciona em método privado/chamada interna) — exp de debug → **nota 05** (callout Java).

## Roster de notas (16; pode crescer/encolher por split)

### Iniciado
1. **O que é um banco de dados** *(âncora)* — persistência, SGBD, modelo relacional como mapa, SQL como
   linguagem, papel central no sistema, o mapa SQL/NoSQL como território. Forward-link às vizinhas.
2. **O modelo relacional** — tabelas/tuplas/schema, PK/FK, integridade referencial, constraints,
   pitada de álgebra relacional.
3. **SQL: consultas** — SELECT/WHERE, todos os JOINs, GROUP BY/HAVING, ORDER BY, subqueries; WHERE×HAVING.
4. **Modelagem e normalização** — 1NF→BCNF, desnormalização intencional, relacionamentos 1:1/1:N/N:M,
   natural × surrogate, IDs (auto-increment/UUIDv4/v7/ULID/Snowflake). *(exp real: `total_avaliacoes`; ULID)*

### Adepto
5. **Transações e ACID** — A/C/I/D, WAL, BEGIN/COMMIT/ROLLBACK; `@Transactional` proxy (callout Java).
   *(exp real: batch noturno; @Transactional proxy)*
6. **Isolamento e anomalias** — dirty/non-repeatable/phantom/lost-update/write-skew, tabela de níveis,
   MVCC, snapshot isolation, pegadinha do REPEATABLE READ no PG. *(divergência PG×InnoDB targeted)*
7. **Índices: que índice criar e quando** — tipos (B-Tree/Hash/GIN/GiST/BRIN/partial/expression/
   covering/unique), composto + leftmost prefix, seletividade/cardinalidade. **Linka [[09 - Árvores B e índices|ED/09]]**.
8. **Lendo o plano: EXPLAIN e otimização** — EXPLAIN ANALYZE, tipos de scan, join strategies
   (nested loop/hash/merge), estatísticas/ANALYZE, buffers, quando **não** indexar. *(exp real: índice composto)*
9. **SQL avançado** — window functions, CTEs (+ recursivas), LATERAL, upsert/ON CONFLICT, keyset pagination.
10. **Performance e armadilhas** — N+1, queries lentas, tabelas gigantes (particionamento/vacuum/
    arquivamento), `SELECT *`, OFFSET alto, connection leak, materialized views. Absorve "Armadilhas comuns".

### Magus
11. **Concorrência e locking** — optimistic (`@Version`) × pessimistic (`FOR UPDATE`), deadlock e ordem
    de lock, `SKIP LOCKED` em filas, lock contention.
12. **Replicação, sharding e CAP** — read replicas, replicação síncrona/assíncrona, sharding como
    particionamento horizontal, CAP/PACELC, eventual consistency. **Linka [[System Design]]**.
13. **Transações distribuídas** — dual-write problem, 2PC e por que dói, Saga, Outbox. Lean —
    **forward-linka [[Mensageria]]/[[Arquitetura de Software]]**.
14. **NoSQL e polyglot persistence** — famílias (chave-valor/documento/coluna/grafo/search/timeseries/
    vector), BASE×ACID, quando escolher, "comece com Postgres". Vector DB linka IA/RAG.
15. **Operação em produção** — migrations (expand/migrate/contract, zero-downtime), backup/PITR,
    replicação operacional, observabilidade (slow query log, pg_stat_statements). *(exp real: migration NOT NULL)*
16. **Capstone: banco em entrevista** — modelar dados num system-design, escolher store, defender
    índices com `EXPLAIN`, cheat-sheet, "How to explain in English" + vocabulário PT→EN, armadilhas.

## Padrão por nota (idêntico aos galhos anteriores)
- Feynman didático, profundo à medida do tema; teto 2400 (permissão, código não conta).
- **3–5 diagramas Mermaid** por nota onde ajudam, cada um com lead-in + "leitura do diagrama". **Sem
  `xychart-beta`** (não renderiza no Obsidian — usar tabela/flowchart). Símbolos/parênteses LITERAIS na
  prosa; entidades HTML SÓ dentro de rótulos Mermaid e sempre entre aspas.
- **Seção "Em entrevista"** (interview-critical) — frases em inglês + vocabulário PT→EN.
- Fontes verificadas na web; callout "Lastro" de honestidade.
- Atomicidade: linka vizinhas em vez de duplicar. `NN - Título.md` flat.
- `publish: false` nas notas; `publish: true` só no `index.md`. Frontmatter `fase:`, tags.
- **NUNCA fabricar** experiências/dados do usuário; preservar e relocar as seções "Na prática" reais.

## Tronco e MOC
- Pasta `03-Dominios/Fundamentos/Banco de Dados/` com `index.md` (MOC, `type: moc`, `publish: true`,
  agrupado por fase, rota de entrevista, dataview, "Veja também").
- Alias do `index.md`: **"Banco de Dados"** + **"Banco de dados"** + "Bancos de Dados" + "Database" para
  resolver os links de entrada (Spring Boot, System Design, ED, Arquitetura referenciam Banco de dados).
- A entrada Banco de Dados entra no MOC do domínio (`Fundamentos/index.md` e `Fundamentos.md`).

## Convenções de execução
- Subagent-driven, um subagente por nota, escrita em UMA chamada Write.
- Commits direto na main, SEM push, SEM Co-Authored-By ([[feedback-commits]]).

## Sequência de construção
1. Scaffold `Banco de Dados/index.md` + aliases.
2. Registrar a entrada no MOC do domínio (`Fundamentos/index.md` + `Fundamentos.md`).
3. Escrever as notas Iniciado (1–4), Adepto (5–10), Magus (11–16), uma por subagente. Relocar as
   experiências reais conforme o mapa de preservação.
4. Remover o monólito `Banco de dados.md`; `verificar-wikilinks` (incl. checagem de `[[` partido por
   quebra de linha); fechar MOCs; atualizar memória.
