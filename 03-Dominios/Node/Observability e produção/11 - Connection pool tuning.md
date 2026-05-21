---
title: "Connection pool tuning"
created: 2026-05-09
updated: 2026-05-09
type: concept
status: seedling
publish: true
tags:
  - node
  - resiliencia
  - database
  - connection-pool
  - prisma
  - knex
aliases:
  - connection pool Node
  - pool tuning
  - pool exausto
---

# Connection pool tuning

> [!abstract] TL;DR
> - **Pool exausto** é uma das falhas mais silenciosas em APIs Node.js: não aparece como "banco lento", aparece como requests travadas aguardando uma conexão disponível — até virar timeout 500 pro cliente sem que nenhuma query tenha sido executada.
> - Cada instância de app tem seu próprio pool. Com 10 pods e pool de 20, são **200 conexões abertas no banco** — e o `max_connections` padrão do Postgres é 100. Esse cálculo é obrigatório antes de ir para produção.
> - **knex / pg-pool**: configure `min`, `max`, `acquireTimeoutMillis` e `idleTimeoutMillis`. **Prisma**: `connection_limit` e `pool_timeout` na DATABASE_URL. **HTTP**: `http.Agent({ keepAlive: true, maxSockets: N })` para reusar conexões TCP.
> - Monitore com uma Gauge do prom-client em `pool.numPendingAcquires()` — quando essa métrica cresce sob carga normal, é sinal de pool subdimensionado; quando cresce de forma episódica, suspeite de transaction leak.
> - Transação sem `try/finally` com rollback é o caminho mais curto para vazar conexões e esgotar o pool silenciosamente.

Abrir uma conexão TCP + TLS + handshake PostgreSQL custa entre 10 ms e 50 ms. Sem pool, cada query paga esse custo — em uma API com 500 req/s, isso significaria 500 conexões novas por segundo, cada uma durando menos de 2 ms, mas custando 50 ms só para estabelecer. O connection pool resolve esse problema mantendo um conjunto de conexões abertas e reutilizando-as entre requisições. Esta nota cobre como dimensionar, configurar e monitorar pools nas três camadas mais comuns em apps Node.js: banco de dados relacional (knex/Prisma), banco de dados in-memory (Redis) e HTTP (axios/node:http).

## O que é

Um **connection pool** é um mecanismo que mantém N conexões abertas e prontas para uso, servindo-as sob demanda para queries ou requisições. Quando uma query chega, o pool empresta uma conexão livre; quando a query termina, a conexão volta ao pool — em vez de ser fechada. Se não há conexão livre e o pool já atingiu o máximo configurado, a requisição fica na fila aguardando — esse é o estado de **pool exhaustion**.

O pool resolve dois problemas complementares:

1. **Custo de setup**: conexões TCP+TLS+auth custam dezenas de milissegundos para estabelecer. Reutilizá-las elimina esse overhead por query.
2. **Limitação do banco**: Postgres, MySQL e outros bancos relacionais têm um número máximo de conexões simultâneas (`max_connections`). O pool garante que a aplicação não ultrapasse esse limite.

## Por que importa

Pool exausto é **silencioso do ponto de vista do banco**. O banco não registra nenhuma query lenta, nenhum lock — porque nenhuma query chegou até ele. O que acontece é:

1. Todas as `N` conexões do pool estão em uso.
2. Uma nova query chega.
3. A query entra na fila de espera.
4. O `acquireTimeoutMillis` expira.
5. O pool rejeita com erro `"Knex: Timeout acquiring a connection"` (ou equivalente).
6. O handler HTTP captura o erro e retorna 500.
7. O cliente recebe 500 — sem nenhum sinal claro de qual query causou o problema.

Métricas de latência do banco ficam normais (porque queries normais que chegam a executar saem rápido). A métrica que aponta o problema é o número de **pending acquires** — quantas queries estão esperando uma conexão.

## Como funciona

### Dimensionamento do pool

A fórmula prática de dimensionamento de pool para banco relacional (recomendada por Percona e HikariCP):

```
pool_size = (num_cores × 2) + effective_spindle_count
```

Para SSDs e NVMe (spindle virtual = 1):

```
Servidor 4 cores, SSD:
pool_size = (4 × 2) + 1 = 9 → arredonda para 10

Servidor 8 cores, SSD:
pool_size = (8 × 2) + 1 = 17 → arredonda para 20
```

Mas em Kubernetes, o cálculo crítico é o **total de conexões abertas no banco**:

```
total_connections = pool_size × num_pods

Exemplo:
  pool_size = 20
  num_pods = 10
  total = 200 conexões

Postgres max_connections padrão = 100 → overflow!
```

A regra prática: `pool_size = max_connections_do_banco / num_pods`, com margem de 20% para picos e conexões administrativas. Para um Postgres com `max_connections = 100` e 10 pods:

```
pool_size = (100 × 0.8) / 10 = 8 conexões por pod
```

### knex e pg-pool — configuração completa

```typescript
import Knex from 'knex';
import { Gauge } from 'prom-client';

const knex = Knex({
  client: 'pg',
  connection: process.env.DATABASE_URL,
  pool: {
    min: 2,                       // conexões idle mantidas abertas
    max: 10,                      // máximo de conexões por instância
    acquireTimeoutMillis: 30_000, // timeout para adquirir conexão do pool
    idleTimeoutMillis: 10_000,    // liberar conexão idle após 10s
    reapIntervalMillis: 1_000,    // verificar por conexões ociosas a cada 1s
    createTimeoutMillis: 5_000,   // timeout para criar nova conexão
  },
});

// Gauge para monitorar pending acquires
const poolWaiting = new Gauge({
  name: 'db_pool_waiting_requests',
  help: 'Requests waiting for a connection from the pool',
});

setInterval(() => {
  const pool = knex.client.pool;
  if (pool) {
    poolWaiting.set(pool.numPendingAcquires());
  }
}, 5_000);
```

**Significado de cada opção:**

| Opção | Descrição | Valor seguro |
|---|---|---|
| `min` | Conexões mínimas mantidas abertas (idle) | 2–5 |
| `max` | Máximo por instância; multiplica pelo número de pods | `max_connections_pg / pods × 0.8` |
| `acquireTimeoutMillis` | Timeout de espera na fila; estoura com erro explícito | 20s–30s |
| `idleTimeoutMillis` | Fecha conexão idle após N ms (evita keepalive desnecessário) | 10s–30s |
| `createTimeoutMillis` | Timeout para estabelecer nova conexão TCP | 5s |

### Prisma — connection_limit via URL

Prisma gerencia seu próprio pool interno via `connection_limit` e `pool_timeout` na connection string:

```
# .env
DATABASE_URL="postgresql://user:pass@host:5432/mydb?connection_limit=10&pool_timeout=30"
```

| Parâmetro | Descrição | Padrão |
|---|---|---|
| `connection_limit` | Máximo de conexões por instância do PrismaClient | `num_cpus + 1` |
| `pool_timeout` | Segundos aguardando conexão antes de lançar erro | 10 |
| `connect_timeout` | Segundos para estabelecer nova conexão TCP | 5 |

Configuração mínima recomendada para produção:

```typescript
import { PrismaClient } from '@prisma/client';

const prisma = new PrismaClient({
  log: ['warn', 'error'],
  // connection_limit e pool_timeout são configurados na DATABASE_URL
});

// Conectar explicitamente no startup (detecta problemas antes de receber tráfego)
await prisma.$connect();

// Desconectar no shutdown
process.on('SIGTERM', async () => {
  await prisma.$disconnect();
  process.exit(0);
});
```

> [!tip] Múltiplas instâncias de PrismaClient
> Cada instância de `PrismaClient` abre seu próprio pool. Em ambientes que importam `prisma` em múltiplos módulos sem singleton, você pode acabar com dezenas de pools paralelos sem perceber. Sempre exporte um singleton: `export const prisma = new PrismaClient()`.

### Transações sem finally — connection leak

A causa mais comum de pool exhaustion progressivo (que piora com o tempo em produção) é transaction leak: uma transação que começa mas nunca é committed nem rolled back, mantendo a conexão presa até o processo morrer.

```typescript
// RUIM — se fetchUser() lançar, trx nunca é committed/rolled back
// → conexão presa no pool para sempre até o processo reiniciar
async function createOrderBad(data: OrderData) {
  const trx = await knex.transaction();
  const user = await fetchUser(data.userId);  // pode lançar!
  await trx('orders').insert({ ...data, userId: user.id });
  await trx.commit();
}

// BOM — try/catch garante rollback em qualquer caminho de erro
async function createOrderGood(data: OrderData) {
  const trx = await knex.transaction();
  try {
    const user = await fetchUser(data.userId);
    await trx('orders').insert({ ...data, userId: user.id });
    await trx.commit();
  } catch (err) {
    await trx.rollback();
    throw err;
  }
}
```

Knex também oferece a forma callback, que faz o rollback automaticamente:

```typescript
// Forma callback — rollback automático em caso de erro
const result = await knex.transaction(async (trx) => {
  const user = await fetchUser(data.userId);
  return trx('orders').insert({ ...data, userId: user.id }).returning('*');
});
```

### HTTP keepalive com axios

O `http.Agent` padrão do Node.js não usa keepalive — cada requisição HTTP abre uma nova conexão TCP e fecha ao terminar. Para APIs que fazem muitas chamadas a serviços externos, isso é exatamente o problema do pool de banco replicado para HTTP.

```typescript
import http from 'node:http';
import https from 'node:https';
import axios from 'axios';

const httpAgent = new http.Agent({
  keepAlive: true,
  maxSockets: 50,         // conexões HTTP simultâneas por host
  maxFreeSockets: 10,     // manter 10 conexões idle abertas
  timeout: 60_000,
  keepAliveMsecs: 30_000, // intervalo de keepalive probe
});

const httpsAgent = new https.Agent({
  keepAlive: true,
  maxSockets: 50,
  maxFreeSockets: 10,
});

export const httpClient = axios.create({
  httpAgent,
  httpsAgent,
  timeout: 5_000,
});
```

> [!tip] undici como alternativa
> O pacote `undici` (usado internamente pelo `fetch` global do Node 18+) tem keepalive por padrão e um pool de conexões embutido com configuração via `undici.setGlobalDispatcher(new Pool(baseUrl, { connections: N }))`. Para cenários de alta concorrência, `undici` tende a ter menor overhead que axios com http.Agent.

### Diagnóstico de pool exausto em produção

Quando suspeitar de pool exhaustion, os comandos SQL abaixo mostram o estado atual das conexões no Postgres:

```sql
-- Estado geral das conexões por estado e evento de espera
SELECT count(*), state, wait_event_type, wait_event
FROM pg_stat_activity
WHERE datname = 'mydb'
GROUP BY state, wait_event_type, wait_event
ORDER BY count DESC;

-- Conexões por aplicação (detecta quem está consumindo mais)
SELECT application_name, state, count(*)
FROM pg_stat_activity
WHERE datname = 'mydb'
GROUP BY application_name, state
ORDER BY count DESC;

-- Transações longas abertas (suspeita de transaction leak)
SELECT pid, now() - pg_stat_activity.query_start AS duration, query, state
FROM pg_stat_activity
WHERE state = 'idle in transaction'
  AND query_start < now() - interval '5 minutes'
ORDER BY duration DESC;
```

## Na prática

Configuração completa recomendada para uma API Node.js com Prisma, Redis e HTTP externo:

```typescript
import { PrismaClient } from '@prisma/client';
import { createClient } from 'redis';
import http from 'node:http';
import https from 'node:https';
import axios from 'axios';
import { Gauge } from 'prom-client';

// Prisma — singleton com connection_limit na URL
// DATABASE_URL="postgresql://...?connection_limit=10&pool_timeout=30"
export const prisma = new PrismaClient({
  log: process.env.NODE_ENV === 'production' ? ['warn', 'error'] : ['query', 'warn', 'error'],
});

// Redis — pool implícito via socket keepalive
export const redis = createClient({
  url: process.env.REDIS_URL,
  socket: {
    keepAlive: 5000,
    reconnectStrategy: (retries) => Math.min(retries * 50, 2000),
  },
});

// HTTP client com keepalive
const httpAgent = new http.Agent({ keepAlive: true, maxSockets: 50 });
const httpsAgent = new https.Agent({ keepAlive: true, maxSockets: 50 });
export const httpClient = axios.create({ httpAgent, httpsAgent, timeout: 5_000 });

// Métricas de pool
const dbPoolWaiting = new Gauge({
  name: 'db_pool_waiting_requests',
  help: 'Requests waiting for a Prisma/PG connection',
});

// Prisma expõe métricas via $metrics (Prisma 4.9+ com previewFeatures = ["metrics"] no schema)
async function collectPrismaMetrics() {
  const metrics = await prisma.$metrics.json();
  // prisma_pool_connections_busy sobe sob pressão; idle desce — sinal inverso
  const busy = metrics.gauges.find((g) => g.key === 'prisma_pool_connections_busy');
  if (busy) {
    dbPoolWaiting.set(busy.value);
  }
}
setInterval(collectPrismaMetrics, 10_000);

// Graceful shutdown
process.on('SIGTERM', async () => {
  await prisma.$disconnect();
  await redis.quit();
  process.exit(0);
});
```

## Em entrevista

**What is connection pool exhaustion and how do you diagnose it?**

Connection pool exhaustion is one of the most common silent failures in Node.js APIs — it looks like slow requests or timeouts to the client, but the database shows no unusual activity because no queries are actually reaching it. The root cause is usually pool misconfiguration: either the pool is too small for the load, transactions that aren't rolled back on error cause connections to leak, or multiple pods each holding a large pool collectively exceed the database's `max_connections`. I diagnose it by monitoring a Prometheus gauge on pending pool acquires — if that gauge grows under normal load, it's a pool sizing problem; if it grows episodically and resets, it's likely a transaction leak. I then confirm with `SELECT state, wait_event FROM pg_stat_activity WHERE datname = 'mydb'` — a large number of `idle in transaction` connections is the smoking gun for transaction leaks. For Prisma, I set `connection_limit` in the database URL; for knex, I configure `acquireTimeoutMillis` so pool exhaustion produces an explicit error rather than a hanging request.

## Vocabulário

| PT | EN |
|---|---|
| pool de conexões | connection pool |
| pool exausto | pool exhaustion |
| aquisição de conexão | connection acquire |
| timeout de aquisição | acquire timeout |
| conexão idle | idle connection |
| keep-alive HTTP | HTTP keepalive |
| vazamento de conexão | connection leak |
| transação aberta sem rollback | unclosed transaction / transaction leak |

## Armadilhas

> [!warning] Múltiplos pods com pool grande excedem `max_connections`
> O erro mais comum ao ir para produção com Kubernetes é não calcular o total de conexões: `pool_size × num_pods`. Com 20 pods e pool de 20, você tem 400 conexões tentando se abrir num Postgres com `max_connections = 100`. O Postgres começa a recusar conexões com `FATAL: sorry, too many clients already`. Sempre calcule: `pool_por_pod = (max_connections × 0.8) / num_pods`. Reserve os 20% restantes para conexões de ferramentas de DBA, migrações e monitoramento.

> [!warning] Transação sem rollback no catch drena o pool lentamente
> Uma transação que lança exceção e não é rolled back mantém a conexão em estado `idle in transaction` indefinidamente (até o processo reiniciar). Dois ou três desses por hora são suficientes para drenar um pool de 10 conexões em algumas horas. Use sempre `try/finally` com `trx.rollback()` ou a forma callback do knex que faz rollback automático. Detecte com a query `pg_stat_activity` filtrando por `state = 'idle in transaction'` e duração > 5 minutos.

> [!warning] HTTP sem keepalive: uma nova conexão TCP por request
> O `http.globalAgent` padrão do Node.js não usa keepalive — cada chamada HTTP abre uma conexão TCP do zero e a fecha ao terminar. Em uma API que faz 200 chamadas por segundo a um serviço externo, isso significa 200 handshakes TCP por segundo, cada um custando 1–5 ms de RTT desnecessário. Configure `http.Agent({ keepAlive: true, maxSockets: N })` e passe para o seu cliente HTTP (axios, got, node-fetch).

> [!warning] Pool muito pequeno em app I/O-bound satura antes do banco
> Um pool de 2 conexões para uma API com 500 req/s simultâneas vai saturar o pool antes de chegar ao banco — a maioria das queries vai esperar na fila. A regra `(cores × 2) + 1` é um ponto de partida, não um teto. Para workloads I/O-bound com queries rápidas, o pool pode precisar ser maior porque as conexões ficam presas por mais tempo esperando a rede, não a CPU. Meça o `acquireWaitTime` nos logs e ajuste.

> [!warning] Não monitorar `pool.numPendingAcquires()` — pool exausto invisível
> Sem monitoramento do número de requests aguardando conexão, pool exhaustion só aparece como aumento de latência P99 ou spike de 500s — ambos difíceis de diferenciar de outros problemas. Configure uma Gauge do prom-client que leia `pool.numPendingAcquires()` (knex) ou a métrica equivalente do Prisma a cada 5–10 segundos. Um alerta em `db_pool_waiting_requests > 5` por mais de 2 minutos é mais preciso do que qualquer threshold de latência para esse tipo de problema.

> [!warning] Múltiplas instâncias de PrismaClient multiplicam o pool
> Cada `new PrismaClient()` abre seu próprio pool. Se você importa Prisma em módulos diferentes sem usar um singleton compartilhado (ou se o framework de DI instancia múltiplas vezes), você pode ter 5–10 pools independentes, cada um com `connection_limit = 10`, totalizando 50–100 conexões por pod sem perceber. Sempre exporte um singleton em `src/lib/prisma.ts` e importe-o em toda a aplicação.

## Veja também

- [[03-Dominios/Node/Observability e produção/index]] — MOC do galho 5
- [[09 - Graceful shutdown profundo]] — desconectar o pool no SIGTERM
- [[10 - Circuit breaker e fallback com opossum]] — proteger chamadas quando o downstream está lento
- [[12 - SLOs, dashboards, alertas e cheatsheet]] — PromQL para monitorar pool waiting
- [[Node.js]] — tronco

## Fontes

- [knex — connection pool](https://knexjs.org/guide/#pool) — documentação oficial das opções de pool do knex
- [Prisma — connection pool](https://www.prisma.io/docs/orm/prisma-client/setup-and-configuration/databases-connections/connection-pool) — configuração de connection_limit e pool_timeout
- [pg-pool — npm](https://www.npmjs.com/package/pg-pool) — pool nativo do driver pg, base do knex
- [HikariCP — pool sizing](https://github.com/brettwooldridge/HikariCP/wiki/About-Pool-Sizing) — artigo original da fórmula de dimensionamento (cores × 2 + spindles)
- [Node.js http.Agent](https://nodejs.org/api/http.html#class-httpagent) — documentação oficial do http.Agent e suas opções de keepalive
