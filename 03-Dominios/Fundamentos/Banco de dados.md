---
title: "Banco de dados"
created: 2026-04-01
updated: 2026-04-09
type: concept
status: evergreen
tags:
  - fundamentos
  - entrevista
publish: false
---

# Banco de dados

Sistemas para armazenar, consultar e manipular dados de forma estruturada, durável e eficiente. Para um senior fullstack, o banco de dados raramente é só um detalhe de persistência — é **o coração do sistema** onde vivem as garantias de consistência, as maiores oportunidades de performance e os bugs mais caros de consertar.

## O que é

Um banco de dados é um sistema que armazena dados de forma **persistente** e fornece uma linguagem (tipicamente SQL) para consultar e manipulá-los, com garantias de **integridade**, **concorrência** e **durabilidade**.

Em entrevistas, o que diferencia um senior não é lembrar sintaxe SQL — é:

1. **Modelar corretamente** (normalização + quando desnormalizar)
2. **Entender ACID** e níveis de isolamento
3. **Ler `EXPLAIN`** e otimizar queries
4. **Escolher índices** com critério
5. **Saber quando SQL não é a resposta** (NoSQL, cache, search engine)
6. **Operar em produção:** migrações, backup, replicação, observabilidade

---

## SQL vs NoSQL

### Bancos Relacionais (SQL)

Organizam dados em **tabelas** com **schema** rígido e relações definidas por **chaves estrangeiras**. Operam sob o modelo **ACID**.

**Principais:** PostgreSQL, MySQL, SQL Server, Oracle, SQLite.

**Pontos fortes:**

- Transações com garantias fortes
- Integridade referencial
- Linguagem padronizada (SQL)
- Joins arbitrários sobre o modelo
- Índices sofisticados (B-Tree, GIN, BRIN, partial, expression)

**Limitações:**

- Schema rígido dificulta evolução rápida
- Joins complexos podem ser caros em alta escala
- Escalar horizontalmente é não-trivial (sharding)

### NoSQL

Categoria heterogênea. "NoSQL" é mais um guarda-chuva do que uma categoria técnica — cada tipo tem trade-offs distintos.

| Tipo | Exemplo | Modelo | Use case |
| --- | --- | --- | --- |
| Documento | MongoDB, CouchDB | JSON/BSON | schemas flexíveis, dados semi-estruturados, prototipagem |
| Chave-valor | Redis, DynamoDB, Memcached | `key → value` | cache, sessões, rate limiting, leaderboards |
| Coluna larga | Cassandra, HBase, ScyllaDB | colunas dinâmicas por linha | escrita massiva, séries temporais, logs |
| Grafo | Neo4j, Neptune, ArangoDB | nós + arestas | redes sociais, recomendações, detecção de fraude |
| Search engine | Elasticsearch, OpenSearch, Solr | documentos invertidos | full-text search, logs, analytics |
| Time series | InfluxDB, TimescaleDB, Prometheus | timestamp + métricas | monitoramento, IoT, métricas |
| Vector DB | Pinecone, Weaviate, pgvector | vetores de embeddings | RAG, busca semântica, ML |

### Quando escolher cada um

- **SQL (PostgreSQL):** **default**. Sistemas com dados relacionais, transações, integridade referencial.
- **Redis:** cache L2, sessões, filas leves, rate limiting, locks distribuídos, pub/sub.
- **MongoDB:** dados semi-estruturados, schemas que evoluem rápido, documentos auto-contidos. Cuidado em cenários com muitos joins — não é o forte dele.
- **Elasticsearch:** busca full-text, agregações sobre logs, autocomplete avançado. **Nunca como fonte primária de verdade.**
- **Cassandra:** escrita massiva distribuída, eventual consistency aceitável, séries temporais.
- **Neo4j:** relações profundas (amigos-de-amigos-de-amigos) que em SQL viram joins recursivos caros.
- **TimescaleDB:** séries temporais mas mantendo SQL e PostgreSQL. Sweet spot pra muita gente.
- **pgvector:** busca semântica em Postgres sem adicionar outro banco. Simplicidade vence.

> **Regra prática:** comece com PostgreSQL. Só adicione outro banco quando houver **dor concreta** e medida. Polyglot persistence tem custo operacional alto — cada banco novo é mais um sistema para monitorar, fazer backup, atualizar, debugar.

---

## ACID

**A**tomicity, **C**onsistency, **I**solation, **D**urability. As quatro garantias clássicas dos bancos relacionais.

### Atomicity

Uma transação é **tudo ou nada**. Se algum passo falha, todos os efeitos anteriores são revertidos. Não existe "metade feito".

### Consistency

O banco nunca fica em estado inválido. Invariantes (constraints, foreign keys, checks, triggers) são sempre preservadas ao final de cada transação.

> Atenção: "consistency" em ACID ≠ "consistency" em CAP. Em ACID, é sobre invariantes do schema. Em CAP, é sobre visibilidade entre réplicas.

### Isolation

Transações concorrentes não veem estados intermediários umas das outras. Controlado pelo **nível de isolamento** (ver abaixo).

### Durability

Uma vez commitada, a transação **sobrevive a falhas** (crash, queda de energia). Tipicamente garantido via WAL (Write-Ahead Log) gravado em disco antes de confirmar o commit.

---

## Níveis de isolamento

Trade-off entre consistência e performance. Quanto maior o isolamento, mais seguro e mais lento.

| Nível | Dirty Read | Non-repeatable Read | Phantom Read | Usado por |
| --- | --- | --- | --- | --- |
| READ UNCOMMITTED | sim | sim | sim | raro (MySQL permite) |
| READ COMMITTED | não | sim | sim | **default PostgreSQL**, Oracle |
| REPEATABLE READ | não | não | sim (exceto PG) | **default MySQL/InnoDB** |
| SERIALIZABLE | não | não | não | crítico financeiro |

### Anomalias explicadas

- **Dirty Read:** ler dados de uma transação que ainda não commitou (pode ser revertida).
- **Non-repeatable Read:** ler a mesma linha duas vezes na mesma transação e receber valores diferentes (alguém fez UPDATE entre os reads).
- **Phantom Read:** ler um conjunto de linhas duas vezes e receber **linhas diferentes** (alguém fez INSERT/DELETE entre os reads).
- **Lost Update:** dois `read-modify-write` concorrentes — a segunda escrita sobrescreve a primeira sem levar em conta as mudanças dela. Classic race condition.
- **Write Skew:** anomalia de SERIALIZABLE — duas transações leem dados sobrepostos, tomam decisões baseadas no que leram, e escrevem em linhas diferentes. O resultado é inconsistente com qualquer execução serial.

### MVCC (Multi-Version Concurrency Control)

Como PostgreSQL e InnoDB implementam isolamento sem travar leituras. Cada transação vê um **snapshot** consistente do banco. Writers não bloqueiam readers — o trade-off é espaço em disco (versões antigas precisam ser limpas via `VACUUM`/purge).

> **Pegadinha PostgreSQL:** "REPEATABLE READ" no PG **não** tem phantom reads — é equivalente a "snapshot isolation". Se você precisa **de verdade** de SERIALIZABLE (que inclui detecção de write skew), peça explicitamente.

---

## Modelagem relacional

### Normalização

Processo de eliminar redundância e dependências indesejadas. Formas normais:

- **1NF** — valores atômicos (sem listas em uma coluna)
- **2NF** — 1NF + nenhum atributo não-chave depende apenas de parte da chave composta
- **3NF** — 2NF + nenhum atributo não-chave depende de outro atributo não-chave (sem dependências transitivas)
- **BCNF** — 3NF mais estrito para dependências funcionais

**Na prática:** mire 3NF. Acima disso é exercício acadêmico. Abaixo disso é quase sempre erro.

### Desnormalização intencional

Adicionar redundância controlada para acelerar leituras. Ex.: armazenar `total_avaliacoes` no perfil do médico em vez de `SELECT COUNT(*) FROM avaliacoes WHERE medico_id = ?` toda vez.

**Quando:**

- Query dominante custa muito mesmo com índices
- Dado mudanças raramente comparado à frequência de leitura
- Você pode manter a consistência via triggers, eventos ou batch

**Custo:** você paga em complexidade de escrita e risco de inconsistência. Avalie se vale.

### Relacionamentos

- **1:1** — raro, geralmente pode ser achatado em uma tabela
- **1:N** — o mais comum. FK no lado N apontando para o 1
- **N:M** — precisa de **tabela de junção** (join table)
- **Auto-relacionamento** — árvores, hierarquias (adjacency list, path enumeration, nested set, closure table)

### Chaves: natural vs surrogate

- **Natural key:** valor que tem significado de negócio (CPF, ISBN)
- **Surrogate key:** valor sem significado de negócio (auto-increment, UUID)

**Default:** surrogate key como PK, natural key como `UNIQUE`. Por quê? Naturais mudam (CPF pode ser corrigido), surrogate nunca. Surrogate também é mais eficiente em índices e JOINs.

### IDs: auto-increment vs UUID vs ULID

| Tipo | Ordem | Tamanho | Distribuído | Fragmenta B-Tree | Expõe volume |
| --- | --- | --- | --- | --- | --- |
| Auto-increment | sim | 4/8 bytes | não | não | sim |
| UUID v4 | não | 16 bytes | sim | **sim** (ruim!) | não |
| UUID v7 / ULID | sim (por tempo) | 16 bytes | sim | não | parcial |
| Snowflake (Twitter) | sim | 8 bytes | sim | não | parcial |

**Por que UUID v4 fragmenta B-Tree:** chaves aleatórias forçam inserts em páginas aleatórias, causando page splits e fragmentação. Em uma tabela grande, isso derruba performance de insert e bloat de índice.

**Recomendação moderna:** use **UUID v7** (ordenável por tempo) ou **ULID** se precisa de IDs distribuídos. Só mantenha auto-increment se **nunca** vai precisar gerar IDs fora do banco.

---

## SQL essencial

### Joins

| JOIN | Comportamento |
| --- | --- |
| `INNER JOIN` | só linhas com match em ambos os lados |
| `LEFT JOIN` | todas da esquerda + matches da direita (NULL se não tiver) |
| `RIGHT JOIN` | espelho do LEFT (raramente usado na prática) |
| `FULL OUTER JOIN` | todas de ambos os lados |
| `CROSS JOIN` | produto cartesiano |
| `LATERAL JOIN` | subquery correlacionada no SELECT — top-N por grupo |

### Agregações e GROUP BY

```sql
SELECT especialidade, COUNT(*) AS total, AVG(anos_experiencia) AS media
FROM medicos
WHERE ativo = true
GROUP BY especialidade
HAVING COUNT(*) > 5
ORDER BY total DESC;
```

**`WHERE` vs `HAVING`:** `WHERE` filtra linhas antes do agrupamento; `HAVING` filtra grupos depois.

### Window Functions

Super poder que muita gente nem sabe que existe. Calcula sobre uma "janela" de linhas sem colapsá-las como GROUP BY.

```sql
SELECT
  nome,
  especialidade,
  salario,
  RANK() OVER (PARTITION BY especialidade ORDER BY salario DESC) AS rank_na_especialidade,
  AVG(salario) OVER (PARTITION BY especialidade) AS media_especialidade
FROM medicos;
```

Use para: top-N por grupo, running totals, médias móveis, percentis, gap analysis.

### CTEs (Common Table Expressions)

```sql
WITH pacientes_frequentes AS (
  SELECT paciente_id, COUNT(*) AS visitas
  FROM consultas
  WHERE data >= NOW() - INTERVAL '1 year'
  GROUP BY paciente_id
  HAVING COUNT(*) >= 10
)
SELECT p.nome, pf.visitas
FROM pacientes p
JOIN pacientes_frequentes pf ON pf.paciente_id = p.id;
```

**CTEs recursivas** resolvem hierarquias (árvores de categorias, org charts, listas de navegação).

### Upsert (INSERT ... ON CONFLICT)

```sql
INSERT INTO user_counts (user_id, count)
VALUES (42, 1)
ON CONFLICT (user_id) DO UPDATE
SET count = user_counts.count + 1;
```

Essencial para idempotência e para evitar race conditions em contadores.

### Transações explícitas

```sql
BEGIN;
UPDATE contas SET saldo = saldo - 100 WHERE id = 1;
UPDATE contas SET saldo = saldo + 100 WHERE id = 2;
COMMIT;  -- ou ROLLBACK em caso de erro
```

Em aplicações, você raramente escreve isso manualmente — o framework (Spring `@Transactional`, TypeORM, Prisma) cuida.

---

## Índices

Estruturas auxiliares que aceleram consultas ao custo de espaço e escrita mais lenta. Sem índice = full table scan em tudo.

### Tipos de índice

| Tipo | Para o quê | Exemplo |
| --- | --- | --- |
| **B-Tree** | equality, range, ordenação | default, 90% dos casos |
| **Hash** | só equality | raramente manual (PG usa em JOINs) |
| **GIN** | arrays, JSONB, full-text | `WHERE tags @> ARRAY['java']` |
| **GiST** | dados geoespaciais, ranges | PostGIS, intervalos |
| **BRIN** | tabelas grandes, ordenadas fisicamente | logs, séries temporais |
| **Partial** | subconjunto de linhas | `WHERE ativo = true` |
| **Expression** | expressões calculadas | `LOWER(email)` |
| **Covering** | inclui colunas extras para evitar acesso à tabela | `INCLUDE (nome, email)` |
| **Unique** | impõe unicidade + acelera equality | PK, email único |

### Índice composto e leftmost prefix

Um índice em `(a, b, c)` serve para queries filtrando por:

- `a` sozinho ✅
- `a, b` ✅
- `a, b, c` ✅
- `b` sozinho ❌
- `a, c` (parcialmente) ⚠️

**Regra:** ponha as colunas mais seletivas (maior cardinalidade) primeiro, e as usadas em range no final.

### EXPLAIN e EXPLAIN ANALYZE

A ferramenta mais importante para otimizar queries. **Sempre** rode antes de criar um índice.

```sql
EXPLAIN ANALYZE
SELECT * FROM consultas
WHERE paciente_id = 42 AND data >= '2026-01-01'
ORDER BY data DESC;
```

**O que procurar:**

- `Seq Scan` em tabela grande — falta índice
- `Index Scan` / `Index Only Scan` — índice sendo usado
- `Nested Loop` com muitas linhas externas — pode virar O(n × m)
- `Hash Join` — geralmente bom para JOINs grandes
- `rows` muito diferente do `actual rows` — estatísticas desatualizadas, rode `ANALYZE`
- `Buffers` (com `BUFFERS`) — quantas páginas foram lidas; quanto menor, melhor

### Quando **não** indexar

- Tabelas pequenas (seq scan é mais rápido)
- Colunas com baixa cardinalidade (ex.: boolean) — exceção: partial index
- Colunas quase nunca usadas em WHERE/JOIN/ORDER BY
- Quando o custo de escrita supera o ganho de leitura

**Cada índice custa espaço, escrita mais lenta, e VACUUM mais caro. Não indexe tudo.**

---

## Problemas clássicos de performance

### N+1 queries

**O bug mais comum em ORMs.** Você carrega uma lista e depois acessa um relacionamento lazy dentro de um loop — gerando uma query por elemento.

```java
// N+1: 1 query para listar médicos + N queries para endereços
List<Medico> medicos = medicoRepository.findAll();
for (Medico m : medicos) {
    System.out.println(m.getEndereco().getCidade()); // cada get dispara query
}
```

**Soluções:**

- **JPA `@EntityGraph`** — carrega relacionamentos em uma só query
- **JPQL com `JOIN FETCH`** — `SELECT m FROM Medico m JOIN FETCH m.endereco`
- **Projeções** — carregar só os campos necessários via DTO
- **Batch size** — Hibernate pode agrupar N queries em uma com `IN (...)`
- **Detectar com ferramentas** — Hibernate Statistics, p6spy, datasource-proxy

### Queries lentas

- Sempre rode `EXPLAIN ANALYZE` antes de culpar o índice
- Verifique se estatísticas estão atualizadas (`ANALYZE`)
- Considere denormalização se o plano é inevitável
- Use views materializadas para relatórios caros
- Cache em Redis para o que muda pouco
- Particionamento para tabelas gigantes

### Tabelas gigantes

- **Particionamento (partitioning):** divide uma tabela em partições físicas por critério (range de data, hash). Queries que filtram por esse critério só varrem uma partição.
- **Vacuum / autovacuum:** limpe tuplas mortas do MVCC regularmente.
- **Arquivamento:** mova dados antigos para tabela histórica ou cold storage.

### Lock contention

Transações longas seguram locks e causam bloqueios em cascata. Mitigações:

- Transações curtas
- Ordem consistente ao adquirir locks (evitar deadlock)
- `SELECT ... FOR UPDATE SKIP LOCKED` em filas
- Otimistic locking com versioning (`@Version` em JPA) em vez de locks pessimistas

---

## Concorrência e locking

### Optimistic locking

Assume que conflitos são raros. Cada linha tem um campo `version`. Ao atualizar, você verifica se a versão é a mesma que leu. Se não, alguém editou — sua operação falha e você retry.

```java
@Entity
public class Pedido {
    @Version
    private Long version;
}
```

**Quando usar:** leituras dominam escritas, baixa contenção.

### Pessimistic locking

Trava a linha explicitamente ao ler, bloqueando outros leitores/escritores.

```sql
SELECT * FROM contas WHERE id = 42 FOR UPDATE;
```

**Quando usar:** alta contenção, crítico financeiro, lógica sensível a race condition.

### Deadlock

Duas transações esperam recursos que a outra segura, mutualmente. O banco detecta e aborta uma delas. **Prevenção:** adquira locks sempre na mesma ordem.

---

## CAP Theorem e consistência distribuída

Em um sistema distribuído, você só pode garantir **dois dos três**:

- **C**onsistency — todos os nós vêem os mesmos dados ao mesmo tempo
- **A**vailability — cada requisição recebe resposta (sucesso ou falha)
- **P**artition tolerance — sistema continua operando apesar de falhas de rede

Como partições **sempre** podem acontecer, na prática a escolha real é **CP** (PostgreSQL com failover, MongoDB) ou **AP** (Cassandra, DynamoDB).

### PACELC

Extensão do CAP: **se há Partição, escolha A ou C; senão (**E**lse), escolha Latência ou Consistência**. Mais realista — até sistemas saudáveis precisam escolher entre latência e consistência forte.

### Eventual consistency

Estado onde, se nenhuma escrita nova for feita, eventualmente todas as réplicas convergem. Aceitável para contadores de likes, feeds. **Inaceitável** para saldo bancário.

---

## Transações distribuídas

Quando uma operação atravessa múltiplos serviços ou bancos:

- **Two-phase commit (2PC):** protocolo clássico. Funciona, mas bloqueia participantes e é frágil em falhas.
- **Saga pattern:** sequência de transações locais, cada uma com uma **compensação** em caso de falha. Não é ACID, mas funciona bem em microserviços.
- **Outbox pattern:** publique eventos na mesma transação que escreve no banco, via uma tabela de eventos pendentes. Garante que "atualizei X e publiquei evento Y" é atômico.

---

## Operação em produção

### Migrations

Mudanças de schema versionadas e aplicadas automaticamente. **Ferramentas:** Flyway, Liquibase (Java); Prisma Migrate, TypeORM migrations (Node); Alembic (Python).

**Regras:**

- Migrations são **imutáveis** depois de aplicadas em produção
- **Versionadas no git** junto com o código
- Evite operações que travam tabela grande (adicionar coluna NOT NULL sem default)
- Separe mudanças breaking em passos: adicionar → migrar dados → remover antigo

### Blue-green / zero-downtime migrations

Três passos para mudanças incompatíveis:

1. **Expand:** adicione a nova estrutura mantendo a antiga
2. **Migrate:** atualize código para usar a nova; copie dados
3. **Contract:** remova a antiga depois que o deploy estabilizar

Exemplo: renomear coluna = adicionar nova → backfill → ler/escrever em ambas → remover antiga.

### Backup e restore

- **Backup físico** — snapshot do disco (rápido, grande)
- **Backup lógico** — `pg_dump`, `mysqldump` (portável, lento)
- **PITR (Point-in-Time Recovery)** — backup base + WAL, permite restaurar em qualquer instante
- **Teste o restore regularmente.** Backup que nunca foi testado é incerteza.

### Replicação

- **Streaming replication (PG):** primary → standby(s), assíncrono ou síncrono
- **Read replicas** para escalar leituras
- **Failover** automático via ferramentas como Patroni
- **Lag de replicação** é métrica crítica

### Observabilidade

- **Slow query log** — configure `log_min_duration_statement` no PG
- **pg_stat_statements** — top queries por tempo total
- **Métricas:** conexões ativas, cache hit ratio, locks, bloat, lag de replicação
- **Ferramentas:** pgBadger, Datadog, New Relic, Grafana + Prometheus

---

## Armadilhas comuns

- **N+1 queries** em ORMs — use `JOIN FETCH` ou `@EntityGraph`
- **Indexar tudo** — cada índice custa escrita, espaço e VACUUM
- **Ignorar `EXPLAIN`** — otimizar no achismo
- **UUID v4 como PK** — fragmenta B-Tree; use UUID v7 ou ULID
- **Migrations não-versionadas** — aplicar SQL direto no banco. Caminho para dívida técnica
- **Transações longas** — seguram locks, derrubam concorrência, inflam WAL
- **`SELECT *`** — traz colunas desnecessárias, atrapalha covering indexes
- **Joins sem índice na FK** — ORMs não criam índice na FK automaticamente em todos os bancos
- **`OFFSET` alto para paginação** — `OFFSET 100000` faz o banco ler 100k linhas. Use cursor/keyset pagination.
- **Falta de `UNIQUE` constraints** — confiar na aplicação para impedir duplicatas
- **`NULL` com semântica confusa** — `NULL = NULL` é `NULL`, não `TRUE`
- **Esquecer `ORDER BY`** — SQL não garante ordem sem ele, nem mesmo "a ordem que está no banco"
- **Cachear tudo** — cache sem estratégia de invalidação = dados inconsistentes
- **Colocar lógica de negócio em triggers** — difícil de testar, debugar, versionar
- **Stored procedures como arquitetura** — dificulta evolução, versionamento, deploy
- **Connection leak** — não fechar conexão vaza do pool. Use try-with-resources / `@Transactional`

---

## Na prática (da minha experiência)

> No MedEspecialista, meu stack padrão é **PostgreSQL + Spring Data JPA + Flyway**. Começo sempre com schema normalizado em 3NF e desnormalizo só quando um relatório específico pede. A tabela de avaliações mantinha `SELECT COUNT(*)` sendo chamado em todo list de médicos — virou `total_avaliacoes` denormalizada atualizada por domain event após cada avaliação. Ganho de ordem de magnitude no endpoint de listagem.
>
> **Um caso concreto de EXPLAIN salvando o dia:** um endpoint de busca de consultas estava lento (~2s). O `EXPLAIN ANALYZE` mostrou `Seq Scan` em uma tabela de 5M linhas. Tinha índice em `paciente_id`, mas a query filtrava por `paciente_id AND data BETWEEN`. Adicionei índice composto `(paciente_id, data DESC)` e caiu pra 30ms. Zero alteração de código.
>
> **Sobre IDs:** migrei do `BIGINT` auto-increment para **ULID** quando quebramos o monolito em serviços. Motivo: precisamos gerar IDs no serviço antes de publicar eventos, e não dá pra depender do banco nesse ponto. ULID por ser ordenável evita o problema de fragmentação do UUID v4.
>
> **Uma lição dolorosa com transações longas:** um batch noturno rodava dentro de uma `@Transactional` gigante que abria sessão, processava milhares de registros e commitava no final. Qualquer exceção no meio → rollback de tudo, horas perdidas. Refatorei pra lotes de 1000 registros em transações curtas, com controle de ponto de retomada em uma tabela de progresso. Robustez disparou.
>
> **Sobre migrations:** uma vez uma migration adicionou uma coluna `NOT NULL` sem default em uma tabela de 20M linhas. O Flyway travou por 15 minutos fazendo rewrite completo. Lição: em tabelas grandes, sempre `ADD COLUMN nullable → backfill em background → ALTER COLUMN SET NOT NULL` depois.
>
> **Sobre ORMs:** JPA é produtivo, mas em 5% dos casos (hot paths, queries de relatório) eu caio pro SQL nativo ou JdbcTemplate. Tentar forçar tudo em JPQL é fonte de N+1, queries ilegíveis e performance ruim. Escolha a ferramenta certa para cada caso.

---

## How to explain in English

> "Database design is one of the areas where senior experience matters most. I default to PostgreSQL for any new project — it's battle-tested, has excellent indexing, handles transactions with MVCC, and scales well for 99% of what I build. I add other stores only when there's measurable pain: Redis for cache and rate limiting, Elasticsearch if I need real full-text search, and I consider TimescaleDB before adding Cassandra for time series.
>
> When I model a domain, I start in third normal form. I denormalize only when I have a specific hot query that justifies the complexity, and I always have a plan for keeping the redundant data consistent — usually through domain events or triggers. The trade-off is never 'normalized or denormalized' globally; it's query by query.
>
> Indexing is evidence-driven. I don't add indexes preventively — I run `EXPLAIN ANALYZE` on the slow queries and add composite indexes based on actual access patterns, respecting the leftmost prefix rule. I've seen teams add dozens of indexes 'just in case' and then wonder why writes are slow.
>
> For transactions, I lean on the framework — Spring's `@Transactional` — but I know it's implemented as a proxy, which means it doesn't work on private methods or internal calls. I've debugged that exact issue more than once. For concurrency, I use optimistic locking with JPA's `@Version` by default, switching to pessimistic locking only when contention is real.
>
> One hard lesson I learned: long transactions are a trap. A batch job that opens one transaction and processes millions of rows locks resources, inflates the WAL, and loses everything on any exception. I now write batch jobs as small transactions with a progress table — much more robust, and recoverable after failure."

### Frases úteis em entrevista

- "Let me start by understanding the access patterns — reads vs writes, hot queries, consistency requirements."
- "I'd model this in third normal form first, then denormalize only if a specific query demands it."
- "Before adding an index, I'd run `EXPLAIN ANALYZE` to confirm the query plan and the actual row counts."
- "For this kind of contention, I'd use optimistic locking with a version column — pessimistic locks are a last resort."
- "I'd avoid UUID v4 as a primary key because it fragments B-Tree indexes — ULID or UUID v7 solve that."
- "This looks like an N+1 problem — we should use a join fetch or projection instead of lazy loading."
- "That's a long-running transaction — I'd break it into smaller chunks with a progress checkpoint."

### Key vocabulary

- chave primária / estrangeira → primary key / foreign key
- índice → index
- índice composto → composite / compound index
- plano de execução → query execution plan
- tabela de junção → join table
- normalização → normalization
- desnormalização → denormalization
- transação → transaction
- nível de isolamento → isolation level
- leitura suja → dirty read
- leitura não repetível → non-repeatable read
- leitura fantasma → phantom read
- bloqueio → lock
- bloqueio otimista / pessimista → optimistic / pessimistic locking
- impasse → deadlock
- replicação → replication
- failover → failover
- consistência eventual → eventual consistency
- particionamento → partitioning
- fragmentação → fragmentation
- migração (de schema) → (schema) migration
- varredura sequencial → sequential scan
- varredura de índice → index scan
- visão materializada → materialized view
- consulta lenta → slow query

---

## Recursos

### Livros

- *Designing Data-Intensive Applications* — Martin Kleppmann (o **único** livro que você precisa sobre storage em 2026)
- *Database Internals* — Alex Petrov (como bancos funcionam por dentro)
- *SQL Performance Explained* — Markus Winand (especialista em índices)
- *The Art of PostgreSQL* — Dimitri Fontaine

### Online

- [Use The Index, Luke](https://use-the-index-luke.com/) — guia excelente sobre índices SQL
- [Postgres EXPLAIN Visualizer (PEV2)](https://explain.dalibo.com/) — visualiza planos do PostgreSQL
- [Refactoring SQL](https://www.dbvis.com/thetable/) — artigos práticos
- [Joins visualizer](https://joins.spathon.com/) — visualização de JOINs

### Cursos (pt-BR)

> [!info] Curso de Modelagem de Dados
> [https://www.youtube.com/playlist?list=PLucm8g_ezqNoNHU8tjVeHmRGBFnjDIlxD](https://www.youtube.com/playlist?list=PLucm8g_ezqNoNHU8tjVeHmRGBFnjDIlxD)

> [!info] Álgebra Relacional
> [https://www.youtube.com/playlist?list=PLdoTFRH60cIDTo_-mZvnuwg_uJeMbu6ZP](https://www.youtube.com/playlist?list=PLdoTFRH60cIDTo_-mZvnuwg_uJeMbu6ZP)

### Artigos

> [!info] Não use UUID como PK nas tabelas do seu banco de dados
> [https://gist.github.com/rponte/bf362945a1af948aa04b587f8ff332f8](https://gist.github.com/rponte/bf362945a1af948aa04b587f8ff332f8)

> [!info] UUIDs são ruins? Entenda o que é ULID
> [https://blog.lsantos.dev/o-que-e-ulid/](https://blog.lsantos.dev/o-que-e-ulid/)

## Veja também

- [[System Design]]
- [[API Design]]
- [[Spring Boot]] — JPA, Hibernate, `@Transactional`
- [[Estruturas de Dados]] — B-Trees e índices
- [[Arquitetura de Software]]
