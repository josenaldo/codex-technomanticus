# Galho 9 — Integrações: Plano de Execução

## Objetivo

Criar o galho 9 da trilha Node Senior: **Integrações**. O galho cobre as principais integrações de produção em Node.js — banco de dados relacional (PostgreSQL/node-postgres), cache e pub/sub (Redis/ioredis), filas de tarefas (BullMQ), streaming de eventos (Kafka/kafkajs), comunicação entre serviços (gRPC), APIs flexíveis (GraphQL com Apollo Server 4 e Mercurius), comunicação em tempo real (WebSockets), clientes HTTP modernos e padrões de resiliência (retry, circuit breaker, bulkhead).

O conteúdo de integrações não existia como seção dedicada no tronco (`Node.js.md`), portanto não há poda. A tarefa final apenas registra o galho no índice principal e no tronco.

## Arquitetura do galho

```
03-Dominios/Node/Integrações/
  index.md                                           ← MOC do galho
  01 - PostgreSQL com node-postgres.md
  02 - Redis e ioredis.md
  03 - BullMQ - filas de tarefas.md
  04 - Kafka com kafkajs.md
  05 - gRPC com grpc-js.md
  06 - GraphQL com Apollo Server e Mercurius.md
  07 - WebSockets com ws e Socket.io.md
  08 - Clientes HTTP - fetch, axios, got e undici.md
  09 - Padrões de resiliência - retry, circuit breaker e bulkhead.md
  10 - Cheatsheet e decision tree de integrações.md
```

## Stack técnica

- **PostgreSQL:** `pg` v8 (node-postgres), `pg-pool`, `postgres` (postgres.js)
- **Redis:** `ioredis` v5, padrões pub/sub, pipeline, Lua scripting
- **BullMQ:** v5, workers, queues, repeatables, FlowProducer
- **Kafka:** `kafkajs` v2, producers, consumers, consumer groups, exactly-once
- **gRPC:** `@grpc/grpc-js` v1.10+, protobuf, streaming RPC, reflection
- **GraphQL:** Apollo Server v4, Mercurius (Fastify-native), DataLoader, subscriptions
- **WebSockets:** `ws` v8, Socket.io v4, heartbeat, rooms, namespaces
- **HTTP clients:** native `fetch` (Node 18+), `axios` v1, `got` v14, `undici` v6
- **Resiliência:** `cockatiel`, `opossum`, padrões retry/bulkhead/timeout

## REGRAS CRÍTICAS

1. **Nenhuma nota abaixo do mínimo de linhas.** Conte as linhas antes do commit. Se estiver abaixo, expanda exemplos, armadilhas ou seção de entrevista.
2. **Snippets obrigatórios.** Cada nota tem número mínimo especificado. Snippets devem ser funcionais e realistas — não pseudo-código.
3. **"Em entrevista" obrigatório em todas as notas de conteúdo.** Mínimo 3 perguntas em inglês com respostas em parágrafos completos (≥ 4 frases por resposta).
4. **Frontmatter completo.** Campos obrigatórios: `title`, `created`, `updated`, `type: concept`, `status: growing`, `publish: true`, `tags` (mínimo 3), `aliases` (mínimo 1).
5. **Commit por tarefa.** Cada tarefa gera exatamente um commit com a convenção `feat(node/g9): add <NN> - <título>`. Tarefa final usa `chore(node/g9):`.

## Self-Check (executar antes de cada commit)

```
[ ] 1. Frontmatter completo: title, created, updated, type, status, publish, tags (≥3), aliases (≥1)
[ ] 2. TL;DR presente com ≥3 linhas de conteúdo (callout [!abstract])
[ ] 3. Contagem de linhas ≥ mínimo especificado na tarefa
[ ] 4. Seção "Em entrevista" com ≥3 perguntas em inglês, cada resposta ≥4 frases
[ ] 5. Seção "Vocabulário" com ≥6 termos definidos em tabela
[ ] 6. Seção de armadilhas com pelo menos 1 callout [!danger] ou [!warning] (problema + fix)
[ ] 7. Seção "Como funciona" com ≥3 subseções ou blocos distintos
[ ] 8. Snippets de código ≥ mínimo especificado, todos com linguagem declarada (typescript, bash, etc.)
[ ] 9. Wikilinks para [[Node.js]] e [[Integrações]] presentes no corpo ou em "Veja também"
[ ] 10. Seção "Veja também" com pelo menos 1 link para documentação oficial da tecnologia
```

## Estrutura de arquivos

```
03-Dominios/Node/Integrações/
  index.md
  01 - PostgreSQL com node-postgres.md
  02 - Redis e ioredis.md
  03 - BullMQ - filas de tarefas.md
  04 - Kafka com kafkajs.md
  05 - gRPC com grpc-js.md
  06 - GraphQL com Apollo Server e Mercurius.md
  07 - WebSockets com ws e Socket.io.md
  08 - Clientes HTTP - fetch, axios, got e undici.md
  09 - Padrões de resiliência - retry, circuit breaker e bulkhead.md
  10 - Cheatsheet e decision tree de integrações.md
```

---

## Tarefas

### Tarefa 1 — MOC do galho

**Arquivos:**
- Criar: `03-Dominios/Node/Integrações/index.md`

**Commit:** `feat(node/g9): add index - moc integracoes`

**Frontmatter:**

```yaml
title: "Integrações"
type: moc
publish: true
created: 2026-05-12
updated: 2026-05-12
status: growing
progresso: andamento
tags:
  - node
  - integrações
  - moc
  - backend
aliases:
  - Node Integrações
  - Integrações Node
```

**Conteúdo mínimo:**
- Callout `[!abstract] TL;DR` com visão geral do galho (tecnologias cobertas)
- Parágrafo de introdução sobre o galho
- Seção `## Conteúdo` com lista de todas as 10 notas linkadas com descrição de uma linha cada
- Seção `## Veja também` com links para os outros galhos da trilha e para `[[Node.js]]`

**Mínimo de linhas:** 80

---

### Tarefa 2 — PostgreSQL com node-postgres

**Arquivos:**
- Criar: `03-Dominios/Node/Integrações/01 - PostgreSQL com node-postgres.md`

**Commit:** `feat(node/g9): add 01 - postgresql com node-postgres`

**Frontmatter:**

```yaml
title: "PostgreSQL com node-postgres"
created: 2026-05-12
updated: 2026-05-12
type: concept
status: growing
publish: true
tags:
  - node
  - postgresql
  - banco-de-dados
  - integrações
aliases:
  - node-postgres
  - pg Node
  - PostgreSQL Node
```

**Conteúdo mínimo:**
- TL;DR: `pg` como cliente de referência, pool de conexões, transações manuais vs gerenciadas, `postgres.js` como alternativa moderna com template literals
- Como funciona: `pg.Pool` vs `pg.Client`, configuração de pool (`max`, `idleTimeoutMillis`, `connectionTimeoutMillis`), ciclo de vida da conexão
- Snippet: configuração de `Pool` com variáveis de ambiente e pool sizing baseado em CPU
- Snippet: query parametrizada com `$1/$2` (prevenção de SQL injection)
- Snippet: transação com `BEGIN/COMMIT/ROLLBACK` usando `pg.Client` explícito e `try/finally` com `client.release()`
- Snippet: `postgres.js` (postgres.js) com template literals e tagged templates
- Snippet: migração de schema com `node-pg-migrate` ou SQL puro com controle de versão
- Armadilhas: connection pool exausto (verificar `max` vs `DB_POOL_SIZE`), `client.release()` esquecido em `catch`, interpolação de string direta em query (SQL injection), não fechar pool em graceful shutdown
- Comparação `pg` vs `postgres.js` vs `pg-promise` em tabela
- Em entrevista: como configurar pool em produção, diferença entre `Pool` e `Client`, como prevenir SQL injection com `pg`, trade-offs entre `pg` e `postgres.js`
- Vocabulário: connection pool, prepared statement, parameterized query, idle timeout, connection timeout, `pg.Pool`, `pg.Client`, `client.release()`

**Mínimo de linhas:** 300
**Mínimo de snippets:** 5

---

### Tarefa 3 — Redis e ioredis

**Arquivos:**
- Criar: `03-Dominios/Node/Integrações/02 - Redis e ioredis.md`

**Commit:** `feat(node/g9): add 02 - redis e ioredis`

**Frontmatter:**

```yaml
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
```

**Conteúdo mínimo:**
- TL;DR: `ioredis` como cliente de referência, estruturas de dados Redis (string, hash, list, set, sorted set, stream), padrões principais (cache, session, pub/sub, rate limiting, distributed lock)
- Como funciona: conexão com `new Redis(url)`, pool implícito vs `ioredis.Cluster`, pipeline e multi-exec, Lua scripting com `client.defineCommand`
- Snippet: operações básicas com TTL (`set`, `get`, `setex`, `del`)
- Snippet: pipeline para batch de operações (reduzir round-trips)
- Snippet: pub/sub com dois clientes distintos (publisher + subscriber)
- Snippet: distributed lock com `SET NX PX` e release condicional com Lua script
- Snippet: rate limiting simples com `INCR` + `EXPIRE`
- Armadilhas: usar o mesmo client para pub/sub e operações normais (bloqueio), esquecer TTL em cache (memory overflow), não tratar reconexão automática em produção, serializar/deserializar JSON manualmente (usar `JSON.stringify/parse`)
- Comparação `ioredis` vs `node-redis` (redis v4) em tabela
- Em entrevista: diferença entre pipeline e multi-exec/MULTI, como implementar distributed lock, quando usar Redis vs Memcached, trade-offs de pub/sub Redis vs Kafka
- Vocabulário: pipeline, MULTI/EXEC, Lua script, pub/sub, keyspace notification, TTL, eviction policy, distributed lock, `SETNX`

**Mínimo de linhas:** 300
**Mínimo de snippets:** 5

---

### Tarefa 4 — BullMQ: filas de tarefas

**Arquivos:**
- Criar: `03-Dominios/Node/Integrações/03 - BullMQ - filas de tarefas.md`

**Commit:** `feat(node/g9): add 03 - bullmq filas de tarefas`

**Frontmatter:**

```yaml
title: "BullMQ - filas de tarefas"
created: 2026-05-12
updated: 2026-05-12
type: concept
status: growing
publish: true
tags:
  - node
  - bullmq
  - filas
  - integrações
aliases:
  - BullMQ
  - Job Queue Node
  - Fila de tarefas Node
```

**Conteúdo mínimo:**
- TL;DR: BullMQ como sistema de filas distribuídas sobre Redis, workers, repeatables, FlowProducer para workflows, Bull Board para UI
- Como funciona: `Queue` (produtor), `Worker` (consumidor), `QueueEvents` (observação), ciclo de vida do job (waiting → active → completed/failed), retry com backoff
- Snippet: criar fila e adicionar job com `addBulk` e opções (`attempts`, `backoff`, `delay`)
- Snippet: worker com processador assíncrono, tratamento de erro e concurrency
- Snippet: job repeatable com cron expression e `removeOnComplete`
- Snippet: `FlowProducer` para pipeline de jobs com dependências
- Snippet: `QueueEvents` para observar eventos de jobs em produção
- Armadilhas: esquecer `removeOnComplete`/`removeOnFail` (Redis memory cresce indefinidamente), workers que não fazem graceful shutdown (jobs ficam em "active" travados), não limitar concurrency (starva outros serviços), uso de `Queue.add` em loop sem `addBulk` (N round-trips ao Redis)
- Comparação BullMQ vs Agenda vs BeeQueue vs Kafka em tabela (use case primário)
- Em entrevista: como garantir exactly-once em BullMQ, estratégia de retry e dead-letter, diferença entre BullMQ e Kafka para processamento assíncrono
- Vocabulário: job, queue, worker, repeatable, FlowProducer, dead-letter queue, backoff, concurrency, `BRPOPLPUSH` (mecanismo Redis subjacente), `removeOnComplete`

**Mínimo de linhas:** 300
**Mínimo de snippets:** 5

---

### Tarefa 5 — Kafka com kafkajs

**Arquivos:**
- Criar: `03-Dominios/Node/Integrações/04 - Kafka com kafkajs.md`

**Commit:** `feat(node/g9): add 04 - kafka com kafkajs`

**Frontmatter:**

```yaml
title: "Kafka com kafkajs"
created: 2026-05-12
updated: 2026-05-12
type: concept
status: growing
publish: true
tags:
  - node
  - kafka
  - streaming
  - integrações
aliases:
  - kafkajs
  - Kafka Node
  - Event Streaming Node
```

**Conteúdo mínimo:**
- TL;DR: kafkajs como cliente Kafka para Node.js, producers com acks, consumers com consumer groups, exactly-once semantics, schema registry com Avro/JSON Schema, admin client
- Como funciona: `Kafka` (client), `Producer`, `Consumer`, partições e consumer groups, offset management, `eachMessage` vs `eachBatch`
- Snippet: producer com `acks: -1` (all) e `idempotent: true`
- Snippet: consumer com `groupId`, `eachMessage` e commit manual de offset
- Snippet: `eachBatch` para processamento em lote com `heartbeat()` a cada N mensagens
- Snippet: admin client para criar tópico e verificar lag de consumer group
- Snippet: graceful shutdown com `producer.disconnect()` e `consumer.disconnect()` em `SIGTERM`
- Armadilhas: não chamar `heartbeat()` em processamentos longos (rebalance indesejado), commit automático em erro (mensagem perdida), não tratar `REBALANCING` error, usar `autoCommit: true` em contextos que exigem exactly-once, esquecer `disconnect()` no shutdown
- Comparação Kafka vs Redis Streams vs BullMQ em tabela (throughput, ordering, replay)
- Em entrevista: diferença entre at-least-once e exactly-once no Kafka, como funciona rebalancing de consumer group, quando usar Kafka vs BullMQ vs Redis Streams
- Vocabulário: producer, consumer, consumer group, partition, offset, lag, rebalancing, exactly-once, idempotent producer, `acks`, heartbeat, schema registry

**Mínimo de linhas:** 320
**Mínimo de snippets:** 5

---

### Tarefa 6 — gRPC com grpc-js

**Arquivos:**
- Criar: `03-Dominios/Node/Integrações/05 - gRPC com grpc-js.md`

**Commit:** `feat(node/g9): add 05 - grpc com grpc-js`

**Frontmatter:**

```yaml
title: "gRPC com grpc-js"
created: 2026-05-12
updated: 2026-05-12
type: concept
status: growing
publish: true
tags:
  - node
  - grpc
  - rpc
  - integrações
aliases:
  - grpc-js
  - gRPC Node
  - Protobuf Node
```

**Conteúdo mínimo:**
- TL;DR: `@grpc/grpc-js` como implementação pura JS (sem binários nativos), protobuf para contratos, 4 tipos de RPC (unary, server streaming, client streaming, bidi streaming), `@grpc/proto-loader` para carregar `.proto` dinamicamente
- Como funciona: definição de serviço em `.proto`, geração de código com `protoc` + `ts-protoc-gen` ou carregamento dinâmico, `grpc.Server`, `grpc.credentials`
- Snippet: definição de `.proto` com mensagem e serviço unary
- Snippet: implementação de servidor gRPC com `addService` e `bindAsync`
- Snippet: cliente gRPC unary com `@grpc/proto-loader` dinâmico e tratamento de erro
- Snippet: server streaming RPC — servidor faz `call.write()` múltiplas vezes e `call.end()`
- Snippet: interceptor de cliente para metadata de autenticação (bearer token)
- Armadilhas: não usar TLS em produção (gRPC trafega dados sem criptografia por padrão), gerar código desatualizado após mudança no `.proto`, não tratar `DEADLINE_EXCEEDED` (requisições longas sem deadline), esquecer de fechar canal do cliente (`channel.close()`) em shutdown
- Comparação gRPC vs REST vs GraphQL em tabela (acoplamento, performance, streaming, browser support)
- Em entrevista: diferença entre gRPC e REST, quando usar streaming RPC, como versionar protobuf sem breaking change, como autenticar chamadas gRPC
- Vocabulário: protobuf, IDL, unary RPC, server streaming, client streaming, bidi streaming, channel, stub, deadline, metadata, interceptor, `proto-loader`

**Mínimo de linhas:** 300
**Mínimo de snippets:** 5

---

### Tarefa 7 — GraphQL com Apollo Server e Mercurius

**Arquivos:**
- Criar: `03-Dominios/Node/Integrações/06 - GraphQL com Apollo Server e Mercurius.md`

**Commit:** `feat(node/g9): add 06 - graphql com apollo server e mercurius`

**Frontmatter:**

```yaml
title: "GraphQL com Apollo Server e Mercurius"
created: 2026-05-12
updated: 2026-05-12
type: concept
status: growing
publish: true
tags:
  - node
  - graphql
  - apollo
  - integrações
aliases:
  - Apollo Server
  - Mercurius GraphQL
  - GraphQL Node
```

**Conteúdo mínimo:**
- TL;DR: Apollo Server v4 como servidor GraphQL framework-agnostic, Mercurius como alternativa Fastify-native com JIT compilation, DataLoader para batching, subscriptions com WebSockets, persisted queries
- Como funciona: schema-first (SDL) vs code-first, resolvers, context, plugins (Apollo), hooks (Mercurius), DataLoader pattern para evitar N+1 em resolvers
- Snippet: Apollo Server v4 com Express middleware (`expressMiddleware`)
- Snippet: Mercurius com Fastify — `fastify.register(mercurius, { schema, resolvers })`
- Snippet: DataLoader para batching de queries em resolvers de campo
- Snippet: subscription com `PubSub` do `graphql-subscriptions` (Apollo) ou `mercurius-subscriptions`
- Snippet: plugin Apollo para logging de operações e métricas de resolver
- Armadilhas: N+1 em resolvers de campo sem DataLoader (cada item pai dispara query separada), introspection habilitada em produção (expõe schema inteiro), profundidade de query sem limite (DoS via queries profundas), não usar persisted queries em produção (parse/validate overhead)
- Comparação Apollo Server v4 vs Mercurius vs Yoga v3 em tabela (performance, ecossistema, DX)
- Em entrevista: como o DataLoader resolve N+1 em GraphQL, diferença entre Apollo Server e Mercurius, como proteger endpoint GraphQL em produção, trade-offs GraphQL vs REST
- Vocabulário: resolver, schema, SDL, code-first, schema-first, DataLoader, batching, deduplication, subscription, PubSub, persisted query, introspection, query depth, complexity limit

**Mínimo de linhas:** 320
**Mínimo de snippets:** 6

---

### Tarefa 8 — WebSockets com ws e Socket.io

**Arquivos:**
- Criar: `03-Dominios/Node/Integrações/07 - WebSockets com ws e Socket.io.md`

**Commit:** `feat(node/g9): add 07 - websockets com ws e socket-io`

**Frontmatter:**

```yaml
title: "WebSockets com ws e Socket.io"
created: 2026-05-12
updated: 2026-05-12
type: concept
status: growing
publish: true
tags:
  - node
  - websockets
  - realtime
  - integrações
aliases:
  - ws Node
  - Socket.io Node
  - WebSocket Node
```

**Conteúdo mínimo:**
- TL;DR: `ws` como biblioteca WebSocket minimalista (protocolo puro), Socket.io com fallback HTTP Long Polling + rooms + namespaces + acknowledgements, heartbeat/ping-pong, escalamento horizontal com Redis adapter
- Como funciona: handshake HTTP → upgrade para WebSocket, `ws.Server` e `ws.WebSocket`, Socket.io `Server` e `Socket`, ciclo de conexão/desconexão/reconexão
- Snippet: servidor WebSocket com `ws` — broadcast para todos os clientes conectados
- Snippet: heartbeat com `ping`/`pong` e detecção de clientes zumbis em `ws`
- Snippet: Socket.io — server com rooms e `socket.to(room).emit()`
- Snippet: Socket.io — acknowledgement com callback (cliente confirma recebimento)
- Snippet: Socket.io com Redis adapter para escalamento horizontal (`@socket.io/redis-adapter`)
- Armadilhas: não implementar heartbeat (clientes zumbis acumulam e vazam memória), escalar horizontalmente sem adapter (mensagens não chegam em outros pods), não autenticar na fase de handshake (autenticar em cada mensagem é ineficiente), enviar payloads grandes via WebSocket sem chunking
- Comparação `ws` vs Socket.io vs SSE (Server-Sent Events) em tabela (fallback, bidirecional, complexidade)
- Em entrevista: diferença entre WebSocket e SSE, como escalar Socket.io horizontalmente, como autenticar conexões WebSocket, quando preferir `ws` sobre Socket.io
- Vocabulário: WebSocket, handshake, upgrade, heartbeat, ping/pong, room, namespace, acknowledgement, Redis adapter, fallback, long polling, SSE

**Mínimo de linhas:** 300
**Mínimo de snippets:** 5

---

### Tarefa 9 — Clientes HTTP: fetch, axios, got e undici

**Arquivos:**
- Criar: `03-Dominios/Node/Integrações/08 - Clientes HTTP - fetch, axios, got e undici.md`

**Commit:** `feat(node/g9): add 08 - clientes http fetch axios got undici`

**Frontmatter:**

```yaml
title: "Clientes HTTP - fetch, axios, got e undici"
created: 2026-05-12
updated: 2026-05-12
type: concept
status: growing
publish: true
tags:
  - node
  - http
  - clientes
  - integrações
aliases:
  - HTTP clients Node
  - fetch Node
  - axios Node
  - undici
```

**Conteúdo mínimo:**
- TL;DR: `fetch` nativo (Node 18+) como padrão moderno, `axios` como opção com interceptors e cancelamento, `got` com retry/stream nativos, `undici` (motor do fetch nativo) com máxima performance e controle de pool
- Como funciona: fetch API (Request/Response/Headers), interceptors em axios, hooks em got, `Pool` e `Agent` em undici para controle de conexão
- Snippet: `fetch` nativo com timeout via `AbortController` e `AbortSignal.timeout()`
- Snippet: axios com interceptors de request/response (adicionar token, logar erros)
- Snippet: `got` com retry automático, timeout por fase e stream de resposta
- Snippet: `undici.Pool` com configuração de conexões para alto throughput
- Snippet: mock de `fetch` em testes com `vi.stubGlobal` (Vitest) ou `MSW`
- Armadilhas: não configurar timeout (request pendente indefinidamente), não reusar `undici.Pool`/agente para o mesmo host (perde connection pooling), ignorar erros 4xx/5xx em `fetch` (não lança exceção automaticamente — verificar `response.ok`), usar `axios` com bundle edge sem verificar tamanho
- Comparação `fetch` vs `axios` vs `got` vs `undici` em tabela (bundle size, retry, streaming, interceptors, edge)
- Em entrevista: por que `fetch` não lança exceção em 404, como implementar retry com backoff em `fetch` nativo, diferença entre `undici` e `fetch` no Node 18+, quando preferir `got` ou `axios`
- Vocabulário: `AbortController`, `AbortSignal`, interceptor, hook, connection pool, `undici.Pool`, `response.ok`, keep-alive, `agent`, timeout por fase (connect/send/response)

**Mínimo de linhas:** 300
**Mínimo de snippets:** 5

---

### Tarefa 10 — Padrões de resiliência: retry, circuit breaker e bulkhead

**Arquivos:**
- Criar: `03-Dominios/Node/Integrações/09 - Padrões de resiliência - retry, circuit breaker e bulkhead.md`

**Commit:** `feat(node/g9): add 09 - padroes de resiliencia`

**Frontmatter:**

```yaml
title: "Padrões de resiliência - retry, circuit breaker e bulkhead"
created: 2026-05-12
updated: 2026-05-12
type: concept
status: growing
publish: true
tags:
  - node
  - resiliência
  - circuit-breaker
  - integrações
aliases:
  - Retry Node
  - Circuit Breaker Node
  - Resiliência Node
```

**Conteúdo mínimo:**
- TL;DR: três padrões fundamentais de resiliência — retry com backoff exponencial + jitter (reduz thundering herd), circuit breaker com estados closed/open/half-open (falha rápida), bulkhead com semáforo/pool (isola domínios de falha); biblioteca `cockatiel` cobre os três; `opossum` especializado em circuit breaker
- Como funciona: máquina de estados do circuit breaker (closed → open após N falhas → half-open após timeout → closed se próxima chamada ok), retry com `handleWhenResult`/`handleAll`, bulkhead com limite de concorrência
- Snippet: retry com `cockatiel` — `retry` com `exponentialBackoff` + `jitter` e condição de retry
- Snippet: circuit breaker com `opossum` — configuração de `timeout`, `errorThresholdPercentage`, `resetTimeout` e fallback
- Snippet: bulkhead com `cockatiel` — `bulkhead(maxConcurrent, maxQueue)` e rejeição de requisições em excesso
- Snippet: composição de políticas com `cockatiel` — `wrap(bulkhead, circuitBreaker, retry)` em ordem correta
- Snippet: timeout com `AbortController` como política independente
- Armadilhas: retry sem jitter (thundering herd — todos os clientes reentram ao mesmo tempo), retry em falhas não idempotentes (POST sem retry-token causa duplicação), circuit breaker sem half-open (nunca se recupera), bulkhead sem `maxQueue` (fila cresce sem limite), não monitorar estado do circuit breaker (falha silenciosa)
- Comparação cockatiel vs opossum vs implementação manual em tabela
- Em entrevista: diferença entre retry e circuit breaker, como o padrão bulkhead isola falhas, por que jitter é essencial no backoff exponencial, ordem correta para compor retry + circuit breaker + bulkhead
- Vocabulário: retry, exponential backoff, jitter, thundering herd, circuit breaker, closed state, open state, half-open state, fallback, bulkhead, semaphore, concurrency limit, idempotent, `resetTimeout`, `errorThresholdPercentage`

**Mínimo de linhas:** 320
**Mínimo de snippets:** 5

---

### Tarefa 11 — Cheatsheet e decision tree de integrações

**Arquivos:**
- Criar: `03-Dominios/Node/Integrações/10 - Cheatsheet e decision tree de integrações.md`

**Commit:** `feat(node/g9): add 10 - cheatsheet e decision tree de integracoes`

**Frontmatter:**

```yaml
title: "Cheatsheet e decision tree de integrações"
created: 2026-05-12
updated: 2026-05-12
type: concept
status: growing
publish: true
tags:
  - node
  - integrações
  - cheatsheet
  - decision-tree
aliases:
  - Cheatsheet Integrações Node
  - Decision Tree Integrações
```

**Conteúdo mínimo:**
- TL;DR com decisões-chave: qual cliente de banco, qual fila, quando gRPC vs REST vs GraphQL, qual cliente HTTP
- Decision tree principal para escolha de tecnologia por domínio:
  - Banco relacional: `pg` (controle total) vs `postgres.js` (DX moderno) vs ORM (ver galho 6)
  - Cache/mensageria leve: Redis (`ioredis`) — pub/sub, session, distributed lock
  - Fila de tarefas: BullMQ (sobre Redis) vs Kafka (streaming de eventos de alto volume)
  - Comunicação interna: gRPC (microserviços, streaming) vs REST (APIs públicas) vs GraphQL (frontend flexível)
  - Tempo real: WebSocket (`ws` se simples, Socket.io se rooms/fallback/scale)
  - HTTP cliente: `fetch` (padrão moderno) vs `undici` (performance crítica) vs `got` (retry/stream) vs `axios` (interceptors + legado)
- Tabela de comparação: tecnologia vs caso de uso primário vs quando NÃO usar
- Seção de padrões transversais: sempre usar connection pool, configurar timeouts em todas as integrações, graceful shutdown desconectando clientes, retry + circuit breaker para dependências externas
- Snippets de configuração minimal de cada tecnologia principal (pg Pool, ioredis, BullMQ Queue, kafkajs Kafka, grpc Server, Apollo Server)
- Seção "Em entrevista" com as perguntas de integração mais frequentes em entrevistas senior
- Vocabulário consolidado com termos de todas as 9 notas anteriores

**Mínimo de linhas:** 300
**Mínimo de snippets:** 4

---

### Tarefa 12 — Registrar galho no índice e no tronco

**Arquivos a editar:**
- `03-Dominios/Node/index.md` — adicionar linha do galho 9 na seção `### Galhos da trilha Node Senior`
- `03-Dominios/JavaScript/Backend/Node.js.md` — adicionar linha do galho 9 na seção `## Veja também`

**Commit:** `chore(node/g9): register galho 9 in node index and trunk`

**Edições:**

Em `03-Dominios/Node/index.md`, adicionar após a linha do galho 6:

```
- [[03-Dominios/Node/Tooling e ecossistema/index]] — galho 7: npm, pnpm, yarn e bun, semver, ESM vs CJS, TypeScript nativo, built-in test runner, DX flags modernos, SEA e APIs Promise-based
- [[03-Dominios/Node/Segurança/index]] — galho 8: supply chain, segredos, validação de entrada (Zod/Joi), JWT, OAuth 2.0 e OIDC, RBAC, rate limiting, Helmet.js e OWASP Top 10
- [[03-Dominios/Node/Integrações/index]] — galho 9: PostgreSQL (node-postgres), Redis (ioredis), BullMQ, Kafka (kafkajs), gRPC, GraphQL, WebSockets, HTTP clients e padrões de resiliência
```

> **Nota:** Se os galhos 7 e 8 já tiverem sido registrados em execuções anteriores, adicionar apenas a linha do galho 9.

Em `03-Dominios/JavaScript/Backend/Node.js.md`, adicionar na seção `## Veja também`:

```
- [[03-Dominios/Node/Integrações/index|Integrações]] — galho 9 da trilha Node Senior; PostgreSQL, Redis, BullMQ, Kafka, gRPC, GraphQL, WebSockets, HTTP clients e padrões de resiliência
```

**Verificação:** Confirmar que o TL;DR do `index.md` menciona os 9 galhos e que `Node.js.md` lista todos os galhos na seção Veja também.
