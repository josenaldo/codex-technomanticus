---
title: "Redis e ioredis"
created: 2026-05-12
updated: 2026-05-12
type: concept
status: growing
publish: true
tags:
  - node
  - redis
  - cache
  - integrações
aliases:
  - ioredis
  - Redis Node
  - Cache Redis
---

# Redis e ioredis

> [!abstract] TL;DR
> `ioredis` é o cliente Redis de referência em [[Node.js]]: suporta Cluster, Sentinel, pipeline, Lua scripting e reconexão automática out of the box. Redis oferece seis estruturas de dados nativas — string, hash, list, set, sorted set e stream — cada uma com semânticas e comandos próprios. Os padrões mais usados em produção são: **cache** (strings com TTL), **session store** (hashes), **pub/sub** (dois clients separados), **rate limiting** (INCR + EXPIRE) e **distributed lock** (SET NX PX + Lua para release atômico). A separação entre cliente pub/sub e cliente de operações normais não é opcional: um client em modo `subscribe` fica bloqueado e rejeita qualquer outro comando. Veja [[03-Dominios/Node/Integrações/index|Integrações]] para o contexto completo do galho.

## Como funciona

### Conexão básica

`ioredis` expõe uma classe `Redis` que encapsula a conexão TCP com o servidor. A instância gerencia reconexão automática por padrão — sem necessidade de código extra para lidar com quedas de rede temporárias.

```ts
import Redis from 'ioredis'

const client = new Redis(process.env.REDIS_URL)
// ou explícito:
const client = new Redis({ host: 'localhost', port: 6379, db: 0 })
```

Diferente do `pg.Pool`, `ioredis` não usa pool de conexões por padrão. Uma instância `Redis` = uma conexão multiplexada via pipelining interno. Para cenários de altíssima concorrência, multiplique instâncias manualmente ou use `ioredis.Cluster`.

### Pool implícito vs ioredis.Cluster

`ioredis.Cluster` conecta automaticamente a todos os nós de um Redis Cluster, descobre slots e roteia comandos para o shard correto. Ele também faz retry em caso de `MOVED` e `ASK` (respostas de roteamento do Cluster).

```ts
import { Cluster } from 'ioredis'

const cluster = new Cluster([
  { host: '127.0.0.1', port: 7000 },
  { host: '127.0.0.1', port: 7001 },
])
```

Para Redis Sentinel (alta disponibilidade sem sharding), use a opção `sentinels`:

```ts
const client = new Redis({
  sentinels: [{ host: 'sentinel-1', port: 26379 }],
  name: 'mymaster',
})
```

### Pipeline e multi-exec

- **Pipeline**: agrupa múltiplos comandos em uma única chamada de rede. Os comandos são enviados juntos, as respostas chegam juntas. Reduz latência de N round-trips para 1. **Não é transacional** — cada comando executa independentemente no servidor.
- **MULTI/EXEC (transaction)**: bloco atômico no servidor. Todos os comandos são enfileirados e executados sem interrupção. Se um comando falhar, os outros ainda executam (Redis não faz rollback). Use para garantir que nenhum outro client leia estado intermediário.

### Lua scripting com defineCommand

`client.defineCommand` permite registrar scripts Lua como se fossem comandos nativos do ioredis. O script executa atomicamente no servidor, sem round-trips extras. É a única forma de garantir atomicidade real em operações compostas (leia-compare-escreva).

```ts
client.defineCommand('releaseLock', {
  numberOfKeys: 1,
  lua: `
    if redis.call("get", KEYS[1]) == ARGV[1] then
      return redis.call("del", KEYS[1])
    else
      return 0
    end
  `,
})
```

---

## Snippet 1 — Operações básicas com TTL

```ts
import Redis from 'ioredis'

const redis = new Redis(process.env.REDIS_URL)

// SET com TTL em segundos (SETEX)
await redis.set('user:42:profile', JSON.stringify({ name: 'Ana' }), 'EX', 300)

// GET (retorna string | null)
const raw = await redis.get('user:42:profile')
const profile = raw ? JSON.parse(raw) : null

// Verificar existência sem buscar o valor
const exists = await redis.exists('user:42:profile') // 1 ou 0

// Atualizar TTL sem alterar o valor
await redis.expire('user:42:profile', 600)

// Deletar chave
await redis.del('user:42:profile')

// Verificar TTL restante (em segundos; -1 = sem TTL; -2 = não existe)
const ttl = await redis.ttl('user:42:profile')
console.log(`TTL restante: ${ttl}s`)
```

> [!warning] Sempre serializar/deserializar manualmente
> Redis armazena apenas bytes. `ioredis` não serializa objetos automaticamente. Sempre `JSON.stringify` antes de `set` e `JSON.parse` após `get`. Esquecer isso é uma das armadilhas mais comuns: você armazena `[object Object]` sem erros e só percebe na leitura.

---

## Snippet 2 — Pipeline para batch de operações

Use pipeline quando precisar executar múltiplos comandos e quer evitar N round-trips de rede. O `exec()` retorna um array de `[error, result]` para cada comando.

```ts
import Redis from 'ioredis'

const redis = new Redis(process.env.REDIS_URL)

async function warmupUserCache(userIds: number[]): Promise<void> {
  const pipeline = redis.pipeline()

  for (const id of userIds) {
    pipeline.set(`user:${id}:online`, '1', 'EX', 60)
    pipeline.hincrby(`stats:users`, 'online_count', 1)
  }

  const results = await pipeline.exec()

  // results: Array<[Error | null, string | number | null]>
  for (const [err, result] of results ?? []) {
    if (err) {
      console.error('Pipeline command failed:', err)
    }
  }
}

await warmupUserCache([1, 2, 3, 4, 5])
// Enviou 10 comandos em 1 round-trip ao invés de 10
```

> [!tip] Pipeline vs MULTI/EXEC
> Use **pipeline** para otimização de rede quando os comandos são independentes. Use **MULTI/EXEC** quando precisar de atomicidade (nenhum outro cliente deve ver estado intermediário). O pipeline não garante que os comandos rodem sem interrupção no servidor.

---

## Snippet 3 — Pub/Sub com dois clientes distintos

```ts
import Redis from 'ioredis'

// REGRA CRÍTICA: pub/sub EXIGE dois clients separados.
// Um client em modo subscribe fica bloqueado para qualquer outro comando.
const publisher  = new Redis(process.env.REDIS_URL)
const subscriber = new Redis(process.env.REDIS_URL)

// --- SUBSCRIBER ---
await subscriber.subscribe('orders:created', 'orders:updated')

subscriber.on('message', (channel: string, message: string) => {
  console.log(`[${channel}]`, JSON.parse(message))
})

subscriber.on('error', (err) => {
  console.error('Subscriber error:', err)
})

// --- PUBLISHER ---
async function publishOrder(event: string, payload: object): Promise<void> {
  const channel = `orders:${event}`
  const message = JSON.stringify(payload)
  const receiverCount = await publisher.publish(channel, message)
  console.log(`Published to ${channel}, ${receiverCount} subscribers received`)
}

await publishOrder('created', { id: 'ord-99', total: 149.90 })

// Cleanup
process.on('SIGTERM', async () => {
  await subscriber.unsubscribe()
  subscriber.disconnect()
  publisher.disconnect()
})
```

> [!danger] Nunca reutilize o mesmo client para pub/sub e operações normais
> Quando você chama `subscribe()`, o client entra em modo subscriber e passa a aceitar apenas `subscribe`, `unsubscribe`, `psubscribe`, `punsubscribe` e `ping`. Qualquer outro comando — incluindo `get`, `set`, `hget` — resulta em erro. Sempre crie dois clients: um exclusivo para subscribe, outro para todas as demais operações.

---

## Snippet 4 — Distributed Lock com SET NX PX e Lua script

```ts
import Redis from 'ioredis'
import { randomUUID } from 'crypto'

const redis = new Redis(process.env.REDIS_URL)

// Registra o script Lua de release atômico uma vez na inicialização
// O script garante: só deleta se o valor ainda for o nosso token
// Sem Lua, haveria race condition entre GET + DEL
;(redis as any).defineCommand('releaseLock', {
  numberOfKeys: 1,
  lua: `
    if redis.call("get", KEYS[1]) == ARGV[1] then
      return redis.call("del", KEYS[1])
    else
      return 0
    end
  `,
})

const LOCK_TTL_MS = 5000 // 5 segundos

async function acquireLock(resource: string): Promise<string | null> {
  const token = randomUUID()
  // SET key value NX PX ttl
  // NX = só seta se a chave NÃO existe
  // PX = TTL em milissegundos (garante liberação mesmo em crash)
  const result = await redis.set(`lock:${resource}`, token, 'NX', 'PX', LOCK_TTL_MS)
  return result === 'OK' ? token : null
}

async function releaseLock(resource: string, token: string): Promise<boolean> {
  // Cast necessário porque defineCommand adiciona o método dinamicamente
  const released = await (redis as any).releaseLock(`lock:${resource}`, token)
  return released === 1
}

// --- USO ---
async function processPayment(orderId: string): Promise<void> {
  const token = await acquireLock(`payment:${orderId}`)

  if (!token) {
    throw new Error(`Order ${orderId} is already being processed`)
  }

  try {
    // seção crítica — apenas um worker executa isso por vez
    console.log(`Processing payment for order ${orderId}`)
    await new Promise(resolve => setTimeout(resolve, 1000)) // simula I/O
  } finally {
    // Sempre libera no finally para evitar lock órfão
    await releaseLock(`payment:${orderId}`, token)
  }
}
```

> [!warning] Edge cases do distributed lock
> Este padrão protege contra race conditions normais, mas **não é Redlock**. Em cenários de falha de rede entre acquire e release, o TTL garante liberação eventual. O token único evita que um worker lento libere o lock de outro worker. Para garantias mais fortes em multi-node Redis, use o algoritmo Redlock com múltiplas instâncias independentes.

---

## Snippet 5 — Rate Limiting com INCR + EXPIRE

```ts
import Redis from 'ioredis'

const redis = new Redis(process.env.REDIS_URL)

interface RateLimitResult {
  allowed: boolean
  current: number
  limit: number
  ttl: number
}

// Fixed window rate limiter
// Janela de `windowSeconds` segundos, máximo `limit` requisições
async function checkRateLimit(
  identifier: string,
  limit: number = 100,
  windowSeconds: number = 60
): Promise<RateLimitResult> {
  const key = `ratelimit:${identifier}:${Math.floor(Date.now() / (windowSeconds * 1000))}`

  // Pipeline garante que INCR e EXPIRE sejam enviados juntos
  const pipeline = redis.pipeline()
  pipeline.incr(key)
  pipeline.ttl(key)
  const [[, current], [, ttl]] = (await pipeline.exec()) as [[null, number], [null, number]]

  // Seta TTL apenas na primeira requisição da janela
  if (current === 1) {
    await redis.expire(key, windowSeconds)
  }

  return {
    allowed: current <= limit,
    current,
    limit,
    ttl: ttl === -1 ? windowSeconds : ttl,
  }
}

// --- MIDDLEWARE EXEMPLO (Express/Fastify) ---
async function rateLimitMiddleware(req: any, res: any, next: any): Promise<void> {
  const ip = req.ip ?? 'unknown'
  const result = await checkRateLimit(`ip:${ip}`)

  res.setHeader('X-RateLimit-Limit', result.limit)
  res.setHeader('X-RateLimit-Remaining', Math.max(0, result.limit - result.current))
  res.setHeader('X-RateLimit-Reset', result.ttl)

  if (!result.allowed) {
    res.status(429).json({ error: 'Too Many Requests' })
    return
  }

  next()
}
```

> [!tip] Fixed window vs Sliding window
> **Fixed window** (acima) é simples e barato: uma chave por janela, `INCR` atômico, `EXPIRE` na primeira chamada. O problema é o "boundary burst": um cliente pode fazer `2×limit` requests em torno da virada da janela. **Sliding window** é mais justa mas exige sorted sets (`ZADD` + `ZREMRANGEBYSCORE` + `ZCOUNT`), com custo O(log N) por request. Para APIs internas ou low-traffic, fixed window é suficiente.

---

## Armadilhas

> [!danger] Usar o mesmo client para pub/sub e operações normais
> O client em modo `subscribe` fica bloqueado e rejeita qualquer outro comando com `ERR only (P)SUBSCRIBE / (P)UNSUBSCRIBE / PING / QUIT allowed in this context`. Sempre crie dois clients: um exclusivo para subscribe, outro para todas as demais operações. Esse erro silencioso quebra a aplicação inteira se o código for compartilhado entre módulos.

> [!danger] Esquecer TTL em cache — memory overflow
> Redis por padrão não expira chaves sem TTL. Em produção, chaves sem expiração acumulam memória indefinidamente. Quando o Redis atinge `maxmemory`, a política de eviction entra em ação (ou o Redis para de aceitar writes se a política for `noeviction`). Sempre passe `EX` ou `PX` em `SET`, ou use `EXPIRE` explicitamente. Audite chaves com `redis-cli --scan --pattern 'cache:*' | xargs redis-cli object encoding` para identificar chaves sem TTL.

> [!warning] Não tratar reconexão automática em produção
> `ioredis` reconecta automaticamente por padrão, mas comandos emitidos durante a desconexão podem ser silenciosamente descartados ou enfileirados indefinidamente dependendo de `enableOfflineQueue` (padrão: `true`). Em produção, configure `maxRetriesPerRequest`, `connectTimeout` e `retryStrategy` explicitamente. Monitore eventos `error` e `reconnecting` para alertas.

```ts
const redis = new Redis({
  host: 'redis-prod',
  maxRetriesPerRequest: 3,
  connectTimeout: 5000,
  retryStrategy(times) {
    if (times > 5) return null // desiste após 5 tentativas
    return Math.min(times * 200, 2000) // backoff exponencial até 2s
  },
})

redis.on('error', (err) => logger.error({ err }, 'Redis connection error'))
redis.on('reconnecting', () => logger.warn('Redis reconnecting...'))
```

> [!warning] Não serializar/deserializar JSON
> Redis armazena strings. Se você fizer `redis.set('key', { foo: 'bar' })`, o valor armazenado será a string `[object Object]`. `ioredis` não converte automaticamente. Sempre `JSON.stringify()` antes de gravar e `JSON.parse()` após ler — ou use uma camada de abstração que faça isso de forma consistente.

> [!warning] Usar KEYS em produção
> O comando `KEYS pattern` bloqueia o event loop do Redis para varrer todo o keyspace. Em produção com milhões de chaves, isso paralisa o servidor por segundos. Use `SCAN` iterativo no lugar de `KEYS`. O `ioredis` expõe `redis.scanStream()` para iterar de forma não-bloqueante.

---

## ioredis vs node-redis (redis v4)

| Critério | `ioredis` | `node-redis` (redis v4) |
|---|---|---|
| **DX / API** | Promessas nativas, API fluente, `defineCommand` simples | API moderna com promessas, mas menos conveniente para Lua e cluster |
| **Cluster** | Suporte nativo, detecção automática de slots, retry em MOVED | Suporte via `createCluster()`, menos maduro em edge cases |
| **Sentinel** | Suporte nativo via opção `sentinels` | Suporte via `createClient({ socket: { sentinels } })` |
| **Reconexão** | Automática, configurável via `retryStrategy` | Requer `socket.reconnectStrategy` explícito |
| **Pipeline** | `.pipeline()` simples, fluente | `.multi()` para MULTI/EXEC; pipeline via batch menos óbvio |
| **Performance** | Levemente superior em benchmarks de alta concorrência | Comparável para uso geral |
| **TypeScript** | Tipos bundled, bem mantidos | Tipos bundled desde v4, qualidade similar |
| **Popularidade** | Downloads mais altos, mais questões no StackOverflow | Biblioteca oficial Redis, suporte da Redis Ltd |
| **Lua scripting** | `defineCommand` registra scripts como métodos tipados | `client.sendCommand(['EVAL', ...])` — mais verboso |
| **Streaming** | `scanStream`, `hscanStream` built-in | Sem streaming nativo equivalente |
| **Recomendação** | Preferir em novos projetos e equipes com prod Redis | Considerar se já usa ou se precisar de suporte oficial |

---

## Em entrevista

### "What's the difference between pipeline and MULTI/EXEC in Redis?"

A **pipeline** is a client-side optimization that batches multiple commands into a single network round-trip. The commands are sent together, but they are executed independently on the server — there is no atomicity guarantee. Other clients can interleave commands between them. The primary benefit is reducing network latency when you need to fire many independent commands at once, turning N round-trips into one.

**MULTI/EXEC** is a server-side transaction mechanism. When you issue `MULTI`, Redis starts queuing all subsequent commands from that client. When you issue `EXEC`, all queued commands run atomically — no other client can interleave operations in between. This is critical when you need to read and write related keys without risking another client modifying them mid-operation. However, it is important to note that Redis does not support rollback: if one command fails during EXEC, the others still execute.

You can actually **combine** both: you can send a MULTI/EXEC block through a pipeline, getting both atomicity and reduced round-trips. In ioredis, `redis.multi()` creates a pipeline that wraps commands in MULTI/EXEC. A common mistake is using pipeline thinking it provides atomicity — it does not. If you need to implement something like "increment only if value is below threshold," Lua scripting is the right tool, not MULTI/EXEC, because WATCH/MULTI/EXEC optimistic locking adds complexity and retry overhead.

### "How would you implement a distributed lock in Redis, and what are the edge cases?"

The basic pattern is `SET key token NX PX ttl` — set the key only if it does not exist (`NX`), with a millisecond TTL (`PX`) and a unique token as the value. The unique token is critical: it lets the lock owner verify ownership before releasing, preventing a slow worker from accidentally releasing a lock acquired by another worker after its TTL expired. The release must be done atomically using a Lua script that checks the token and deletes the key in one operation — a naive GET + DEL has a race condition window.

The **edge cases** are numerous and important to articulate in a senior interview. First, the TTL must be long enough for the critical section to complete, but short enough to auto-release if the holder crashes. Setting it too short causes lock expiry during execution, meaning two workers hold the lock simultaneously. Second, if the holder pauses (GC pause, VM migration) after acquiring but before completing, the lock may expire and be acquired by someone else while the original holder is still in the critical section. Third, network partitions can cause the holder to lose connectivity to Redis but still be executing the critical section.

For stronger guarantees in distributed systems with multiple Redis nodes, the **Redlock algorithm** was proposed by Redis's creator. It requires acquiring the lock on a majority of N independent Redis instances (typically 3 or 5). If the client cannot acquire a majority within a timeout smaller than the lock TTL, it releases all acquired locks and retries. Redlock is controversial — Martin Kleppmann published a critique arguing it is not safe under certain failure modes involving process pauses and clock drift. For most production workloads, a single Redis instance with the SET NX PX + Lua pattern is sufficient, and you should be prepared to discuss its limitations.

### "When would you use Redis pub/sub vs Kafka for messaging?"

**Redis pub/sub** is fire-and-forget: messages are delivered to currently-connected subscribers and immediately discarded. There is no persistence, no consumer groups, and no replay. If a subscriber is offline when a message is published, that message is lost. It is best suited for real-time notifications where message loss is acceptable — think live dashboards, presence updates, or invalidating cache across multiple API instances. The latency is sub-millisecond and operational complexity is near zero if you already have Redis in your stack.

**Kafka** is a durable, partitioned, replicated commit log. Messages are retained for a configurable period (days, weeks, indefinitely). Multiple independent consumer groups can read the same stream at their own pace, and any consumer can replay from any offset. Kafka is the right choice when you need guaranteed delivery, event sourcing, audit trails, or fan-out to multiple downstream systems that may be temporarily unavailable. A payment event that needs to trigger fulfillment, notifications, analytics, and fraud detection simultaneously is a Kafka use case, not Redis pub/sub.

The **decision framework** I use is: if you can afford to lose messages and need low latency with minimal ops overhead, use Redis pub/sub or Redis Streams (which adds persistence and consumer groups to Redis). If you need guaranteed delivery, replay, or multiple independent consumer groups with different processing speeds, use Kafka. Redis Streams is an interesting middle ground — it adds persistence and consumer group semantics to Redis, making it viable for moderate-throughput event streaming without the operational weight of a full Kafka cluster.

### "What Redis eviction policies would you configure for a cache workload?"

For a **pure cache workload** — where Redis holds derived data that can be recomputed from the source of truth — `allkeys-lru` is the correct eviction policy. It evicts the least recently used key across all keys when memory is full. This is appropriate because all keys are cache entries with equal standing, and LRU is a good approximation of "least likely to be needed again." You should also set `maxmemory` explicitly to prevent Redis from consuming all available RAM, which would trigger OOM kills at the OS level.

If your Redis instance mixes **persistent data** (session tokens, distributed locks) with **cached data**, use `volatile-lru` instead. This evicts only keys that have a TTL set, leaving keys without TTL untouched. This way, session data stored without TTL is protected from eviction even under memory pressure. The tradeoff is that if all cache keys have TTLs and all session keys do not, the behavior is predictable. Problems arise when developers inconsistently set TTLs.

The policies `allkeys-lfu` and `volatile-lfu` use Least Frequently Used instead of LRU, which is better when you have a hotspot of a few very-frequently-accessed keys alongside many cold keys. For most web application caches with relatively uniform access patterns, LRU is sufficient and more predictable to reason about. In practice, the policy matters less than ensuring you have `maxmemory` set and are monitoring `evicted_keys` in your Redis metrics — a nonzero and climbing eviction rate is a signal to either increase memory or reduce cache entry size and TTL.

---

## Vocabulário

| Termo | Definição |
|---|---|
| **Pipeline** | Otimização client-side que agrupa múltiplos comandos Redis em um único round-trip de rede. Os comandos são enviados juntos e executados independentemente no servidor — não há garantia de atomicidade. Reduz latência de N round-trips para 1 em operações batch. |
| **MULTI/EXEC** | Mecanismo de transação server-side do Redis. `MULTI` inicia o enfileiramento de comandos; `EXEC` executa todos atomicamente, sem interrupção de outros clients. Redis não suporta rollback: comandos com erro não cancelam os demais. Combine com pipeline para otimização de rede. |
| **Lua script** | Programa Lua executado diretamente no servidor Redis de forma atômica. Usado quando uma operação composta (leia-compare-escreva) precisa ser garantidamente atômica sem MULTI/EXEC. Em ioredis, `defineCommand` registra scripts Lua como métodos nativos do client. |
| **Pub/Sub** | Padrão de mensageria assíncrona em que publishers enviam mensagens para canais sem conhecer os subscribers. Redis implementa pub/sub com fire-and-forget: mensagens são descartadas imediatamente após entrega. Subscribers offline perdem mensagens. Exige clients separados para publish e subscribe. |
| **Keyspace notification** | Recurso do Redis que emite eventos pub/sub automaticamente quando operações ocorrem em chaves específicas. Configurado via `notify-keyspace-events` no `redis.conf`. Permite reagir a eventos como expiração de TTL (`expired`) ou delete sem polling. Útil para invalidação de cache reativa. |
| **TTL (Time to Live)** | Tempo de expiração de uma chave Redis, em segundos (`EX`) ou milissegundos (`PX`). Após o TTL, o Redis deleta a chave automaticamente. Chaves sem TTL (-1) nunca expiram e acumulam memória indefinidamente. Verificado com `TTL key`; atualizado com `EXPIRE key seconds`. |
| **Eviction policy** | Política que determina quais chaves Redis apaga quando atinge `maxmemory`. Principais opções: `noeviction` (rejeita writes), `allkeys-lru` (evict LRU de qualquer chave), `volatile-lru` (evict LRU apenas de chaves com TTL), `allkeys-lfu` (evict LFU de qualquer chave). Para cache puro, `allkeys-lru` é o padrão recomendado. |
| **Distributed lock** | Mecanismo para garantir que apenas um processo em um sistema distribuído execute uma seção crítica por vez. Em Redis, implementado com `SET key token NX PX ttl`. O token único previne que um worker lento libere o lock de outro. O release deve ser atômico via Lua script para evitar race condition entre verificação e deleção. |
| **SETNX** | Comando Redis (`SET key value NX`) que seta uma chave apenas se ela não existir (`NX = Not eXists`). Retorna `OK` em sucesso e `nil` em falha (chave já existe). É a base dos distributed locks — a atomicidade do SETNX garante que apenas um caller "ganhe" a competição. A forma moderna é usar `SET key value NX PX ttl` em um único comando. |
| **Redis Streams** | Estrutura de dados do Redis (introduzida na v5.0) que implementa um log append-only persistente com consumer groups e ACK. É o meio-termo entre pub/sub (sem persistência) e Kafka (heavy ops). Suportado em ioredis via `xadd`, `xread`, `xgroup` e `xack`. Ideal para event streaming de volume moderado sem overhead de Kafka. |
