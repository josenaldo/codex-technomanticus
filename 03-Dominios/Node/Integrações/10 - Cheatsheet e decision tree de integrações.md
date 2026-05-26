---
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
---

# Cheatsheet e decision tree de integrações

> [!abstract] TL;DR
> Para banco de dados relacional: prefira `pg` (node-postgres) quando precisar de controle total e performance crítica, ou `postgres.js` quando quiser DX moderna com tagged templates; use um ORM apenas quando o modelo de domínio for complexo (ver [[03-Dominios/Node/ORMs e banco de dados/index|ORMs e banco de dados]]).
> Para cache e mensageria leve: `ioredis` para sessões, pub/sub e locks distribuídos; use BullMQ sobre Redis quando precisar de durabilidade, retry e dead-letter queue.
> Para comunicação entre serviços: gRPC para microserviços internos com contrato forte e performance; REST para APIs públicas; GraphQL quando o cliente precisa de flexibilidade para compor dados.
> Para resiliência: cockatiel (retry + circuit breaker + bulkhead) ou opossum (circuit breaker stand-alone) devem envolver **toda** chamada a serviço externo em produção.
> O galho 9 cobre todos esses padrões em detalhe — esta nota é o mapa de navegação. Veja [[03-Dominios/Node/Integrações/index|Integrações]].

## Como funciona

### A lógica por trás da escolha de integrações

Escolher a tecnologia de integração correta não é questão de preferência pessoal — é uma decisão de engenharia guiada por quatro variáveis:

**Acoplamento** — quão fortemente o produtor precisa conhecer o consumidor. gRPC e REST são síncronos: o produtor espera a resposta. Kafka é assíncrono: o produtor publica e esquece. BullMQ é assíncrono com garantia de entrega. O nível de acoplamento aceitável é ditado pelo domínio: pagamentos exigem resposta síncrona; envio de e-mail não exige.

**Throughput e latência** — quantas mensagens por segundo e qual o tempo de resposta tolerável. Para alto throughput com baixa latência, `undici` e conexões gRPC com HTTP/2 ganham de `axios` e REST sobre HTTP/1.1. Para processamento em background sem SLA de latência, BullMQ é suficiente; para replay e fan-out a múltiplos consumers, Kafka é o padrão.

**Custo operacional** — o que é necessário para colocar e manter em produção. Redis com ioredis tem footprint menor que Kafka. gRPC exige geração de código e protoc. Apollo Server tem overhead de runtime maior que Mercurius (Fastify-native). A pergunta correta não é "qual é mais poderoso?" mas "qual a complexidade mínima que resolve o problema?"

**Contrato e evolução** — com que frequência o contrato entre produtor e consumidor muda, e quem controla ambos os lados. Quando a equipe controla servidor e cliente, gRPC com `.proto` versionado é superior a REST sem contrato formal. Quando o cliente é um browser ou mobile de terceiros, REST ou GraphQL permitem evolução sem coordenação de versão obrigatória.

### Padrões transversais que se aplicam a toda integração

Independentemente da tecnologia escolhida, quatro padrões se aplicam a **toda** integração Node.js de produção:

**Connection pool** — nunca abra e feche conexões por request. `pg` tem `Pool`, `undici` tem `Pool`, `ioredis` gerencia conexões internamente. Dimensione o pool com base no número de workers do serviço e na capacidade do backend, não com o valor padrão da biblioteca.

**Timeout duplo** — configure sempre dois timeouts: `connectTimeout` (tempo para estabelecer a conexão) e `requestTimeout` (tempo para receber a resposta). Uma chamada sem timeout pode bloquear um worker Node indefinidamente, esgotando o pool e derrubando a API inteira.

**Graceful shutdown** — ao receber `SIGTERM`, o processo deve (1) parar de aceitar novas conexões, (2) aguardar os requests em andamento finalizarem, (3) desconectar todos os clientes (pg pool, ioredis, kafka consumer, bullmq worker). Sem graceful shutdown, deploys em Kubernetes causam erros de conexão para os clientes.

**Retry com backoff exponencial + circuit breaker** — toda chamada a serviço externo deve ser envolvida por retry com backoff exponencial e jitter (para evitar thundering herd) e por um circuit breaker que abre quando a taxa de erro ultrapassa um limiar. Cockatiel ou opossum implementam esses padrões com poucas linhas de código.

### Como padrões de resiliência se compõem com clients de integração

Os padrões de resiliência não substituem o client — eles envolvem o client. A composição correta é:

```
request → bulkhead → circuit breaker → retry → timeout → client
```

O bulkhead limita a concorrência máxima para aquela integração específica, isolando falhas de um backend dos demais. O circuit breaker interrompe tentativas quando o backend está claramente indisponível. O retry tenta novamente erros transientes. O timeout garante que nenhuma tentativa trava o worker indefinidamente. O client executa a chamada real.

Essa composição é o que separa uma integração de produção de um `fetch()` nu sem tratamento de erro. A nota [[03-Dominios/Node/Integrações/09 - Padrões de resiliência - retry, circuit breaker e bulkhead]] detalha cada camada com código de produção.

## Decision Trees

### Banco de dados relacional

- Precisa de controle total sobre queries, performance crítica, queries complexas sem abstração?
  - Sim → **`pg` (node-postgres)**
    - Gerencia Pool manualmente, escreve SQL direto, máximo controle
    - Use quando: relatórios complexos, otimização de índices, queries com CTEs e window functions
    - Não use quando: equipe não tem conforto com SQL manual ou o modelo de domínio é rico em relações

- Quer DX moderna com tagged templates e type safety sem ORM?
  - Sim → **`postgres.js`**
    - SQL como template literals: `` sql`SELECT * FROM users WHERE id = ${id}` ``
    - Escapamento automático, connection pool integrado, suporte a arrays nativos do Postgres
    - Use quando: projeto novo, equipe prefere SQL mas quer ergonomia moderna
    - Não use quando: precisa de migrations automatizadas ou o projeto já usa `pg`

- Modelo de domínio complexo, relações ricas, necessidade de migrations versionadas?
  - Sim → **ORM** — ver [[03-Dominios/Node/ORMs e banco de dados/index|ORMs e banco de dados]] (galho 6)
    - Prisma para projetos TypeScript greenfield
    - TypeORM para times vindos de Java/Spring
    - Drizzle para serverless/edge

### Cache e mensageria leve

- Precisa de cache, sessão, pub/sub, lock distribuído ou rate limiting?
  - Sim → **`ioredis`**
    - Use `SET key value EX ttl` para cache com expiração
    - Use `SETNX` + `EXPIRE` ou Redlock para locks distribuídos
    - Use `PUBLISH` / `SUBSCRIBE` para pub/sub leve (sem persistência)
    - Use `INCR` + `EXPIRE` com janela deslizante para rate limiting

- Precisa de fila com durabilidade, retry automático, dead-letter queue ou jobs agendados?
  - **NÃO use Redis pub/sub ou listas simples** — mensagens perdidas em caso de crash
  - → Use **BullMQ** (que usa Redis por baixo, mas com garantias de entrega)

- Redis vs Memcached?
  - Redis suporta estruturas de dados ricas (sets, sorted sets, hashes), pub/sub, scripting Lua e persistência
  - Memcached só faz cache simples de chave-valor em memória
  - Em projetos Node modernos, **sempre Redis** — a flexibilidade é superior ao ganho marginal de performance do Memcached

### Fila de tarefas

- Tarefas discretas com retry, prioridade, agendamento (cron), dependências entre jobs e DLQ?
  - Sim → **BullMQ**
    - Implementado sobre Redis; operações atômicas com scripts Lua
    - Worker model: cada worker processa um job por vez (ou com concurrency configurável)
    - Use quando: envio de e-mail, processamento de imagem, geração de relatório, notificações push
    - Não use quando: volume > 10k mensagens/s ou precisar de replay histórico

- Eventos de domínio, alto volume (>10k msg/s), múltiplos consumers independentes, replay, auditoria?
  - Sim → **Kafka (kafkajs)**
    - Consumer groups permitem que múltiplos serviços consumam o mesmo tópico independentemente
    - Retenção configurável: replay desde o início ou desde um offset específico
    - Partições permitem paralelismo e ordering por chave
    - Use quando: event sourcing, CQRS, pipelines de dados, integrações entre bounded contexts
    - Não use quando: o overhead operacional (cluster Kafka + Zookeeper/KRaft) supera o benefício

### Comunicação entre serviços

- Comunicação entre microserviços internos, contrato forte, performance crítica ou streaming?
  - Sim → **gRPC (`@grpc/grpc-js`)**
    - Contrato definido em `.proto` — ambos os lados compartilham o mesmo arquivo
    - HTTP/2 por padrão: multiplexing, header compression, streaming bidirecional
    - Code generation garante type safety em TypeScript sem esforço manual
    - Use quando: serviços internos sob controle da mesma equipe, latência < 10ms é requisito
    - Não use quando: o cliente é um browser (requer grpc-web ou transcoding)

- API pública consumida por clientes externos (browser, mobile, parceiros)?
  - → **REST (HTTP + JSON)**
    - Universalmente suportado, sem necessidade de geração de código no cliente
    - Documentação com OpenAPI/Swagger é padrão de mercado
    - Use quando: API pública, time não controla os clientes, simplicidade de adoção é prioridade

- Frontend precisa de flexibilidade para compor dados de múltiplas entidades em uma só chamada?
  - → **GraphQL (Apollo Server ou Mercurius)**
    - Apollo Server: ecossistema rico, schema federation, plugins — melhor para times grandes
    - Mercurius: integração nativa com Fastify, melhor performance, JIT de resolvers
    - Use quando: múltiplos clientes com necessidades diferentes (web, mobile, TV), BFF pattern
    - Não use quando: API simples com poucos endpoints — GraphQL adiciona complexidade desnecessária

### Tempo real (cliente ↔ servidor)

- WebSocket puro, sem fallback, sem rooms, sem state compartilhado no servidor?
  - Sim → **`ws`**
    - Implementação minimalista, baixo overhead, controle total do protocolo
    - Use quando: jogos, feeds de dados financeiros, telemetria em tempo real
    - Não use quando: precisa de rooms, namespaces ou suporte a clientes que bloqueiam WebSocket

- Precisa de rooms, namespaces, fallback para HTTP long-polling ou scaling horizontal com Redis adapter?
  - Sim → **Socket.io**
    - Abstração sobre WebSocket com fallback automático
    - `socket.join('room')` e `io.to('room').emit(event)` sem boilerplate
    - Redis adapter para broadcasting em múltiplas instâncias (horizontal scaling)
    - Use quando: chat, notificações por grupo, dashboard colaborativo, jogos com lobbies

### HTTP cliente (chamadas a APIs externas)

- Node.js 18+ e a chamada é simples (sem retry nativo, sem interceptors globais)?
  - → **`fetch` nativo**
    - Zero dependências, padrão Web, funciona em Node e browser com o mesmo código
    - Combine com cockatiel para retry e circuit breaker externos

- Performance crítica, controle fino sobre o pool de conexões, worker threads?
  - → **`undici`**
    - A base do `fetch` nativo no Node.js, mas com API de baixo nível
    - `undici.Pool` para reuso agressivo de conexões
    - Use quando: proxy reverso, gateway de API que roteia milhares de chamadas por segundo

- Precisa de retry nativo, suporte a streams, cancelamento com AbortController e DX moderna?
  - → **`got`**
    - Retry com backoff embutido, eventos de progresso, suporte a OAuth
    - Use quando: chamadas a APIs externas com retry automático sem depender de biblioteca extra

- Codebase existente usa axios, precisa de interceptors globais ou TypeScript generics no response?
  - → **`axios`**
    - Interceptors de request e response para auth, logging e tratamento de erro centralizado
    - `axios.create()` para instâncias por base URL com configuração isolada
    - Use para manter consistência em codebases que já adotaram axios; evite introduzir em projetos novos

## Snippets

### Snippet 1 — Bootstrap de clientes: pg Pool + ioredis + BullMQ Queue

```typescript
// src/infra/clients.ts
import { Pool } from 'pg';
import Redis from 'ioredis';
import { Queue } from 'bullmq';

// PostgreSQL — pool com limites explícitos e timeout configurado
export const pgPool = new Pool({
  host: process.env.POSTGRES_HOST ?? 'localhost',
  port: Number(process.env.POSTGRES_PORT ?? 5432),
  database: process.env.POSTGRES_DB ?? 'app',
  user: process.env.POSTGRES_USER ?? 'app',
  password: process.env.POSTGRES_PASSWORD,
  max: 20,                  // máximo de conexões simultâneas
  min: 2,                   // mínimo mantido aquecido
  idleTimeoutMillis: 30_000, // fecha conexão ociosa após 30s
  connectionTimeoutMillis: 5_000, // erro se não conectar em 5s
});

pgPool.on('error', (err) => {
  console.error('[pg] unexpected error on idle client', err);
});

// Redis — conexão única reutilizada via ioredis (auto-reconnect embutido)
export const redis = new Redis({
  host: process.env.REDIS_HOST ?? 'localhost',
  port: Number(process.env.REDIS_PORT ?? 6379),
  password: process.env.REDIS_PASSWORD,
  maxRetriesPerRequest: 3,
  enableReadyCheck: true,
  lazyConnect: false,
});

redis.on('error', (err) => {
  console.error('[redis] connection error', err);
});

// BullMQ Queue — usa a mesma conexão Redis
// Nota: BullMQ requer uma conexão dedicada (não compartilhar com pub/sub)
export const emailQueue = new Queue('email', {
  connection: {
    host: process.env.REDIS_HOST ?? 'localhost',
    port: Number(process.env.REDIS_PORT ?? 6379),
    password: process.env.REDIS_PASSWORD,
  },
  defaultJobOptions: {
    attempts: 3,
    backoff: { type: 'exponential', delay: 1_000 },
    removeOnComplete: { count: 100 },
    removeOnFail: { count: 500 },
  },
});
```

### Snippet 2 — Kafka producer + consumer com kafkajs

```typescript
// src/infra/kafka.ts
import { Kafka, logLevel, CompressionTypes } from 'kafkajs';

const kafka = new Kafka({
  clientId: process.env.SERVICE_NAME ?? 'my-service',
  brokers: (process.env.KAFKA_BROKERS ?? 'localhost:9092').split(','),
  logLevel: logLevel.WARN,
  retry: {
    initialRetryTime: 300,
    retries: 10,
  },
});

// Producer — singleton por processo
export const producer = kafka.producer({
  allowAutoTopicCreation: false,
  transactionTimeout: 30_000,
});

export async function connectProducer(): Promise<void> {
  await producer.connect();
  console.log('[kafka] producer connected');
}

export async function publishEvent(
  topic: string,
  key: string,
  payload: Record<string, unknown>,
): Promise<void> {
  await producer.send({
    topic,
    compression: CompressionTypes.GZIP,
    messages: [
      {
        key,
        value: JSON.stringify(payload),
        headers: {
          'content-type': 'application/json',
          'produced-at': new Date().toISOString(),
        },
      },
    ],
  });
}

// Consumer — cada instância do serviço é um membro do consumer group
export const consumer = kafka.consumer({
  groupId: process.env.KAFKA_GROUP_ID ?? 'my-service-group',
  heartbeatInterval: 3_000,
  sessionTimeout: 30_000,
});

export async function startConsumer(
  topic: string,
  handler: (key: string | null, payload: unknown) => Promise<void>,
): Promise<void> {
  await consumer.connect();
  await consumer.subscribe({ topic, fromBeginning: false });

  await consumer.run({
    eachMessage: async ({ topic: t, partition, message }) => {
      const key = message.key?.toString() ?? null;
      const value = message.value ? JSON.parse(message.value.toString()) : null;

      try {
        await handler(key, value);
      } catch (err) {
        // Em produção: enviar para DLQ ou logar com contexto completo
        console.error(`[kafka] failed to process message from ${t}[${partition}]`, err);
        throw err; // Re-throw para que o kafkajs pause e retry
      }
    },
  });
}
```

### Snippet 3 — Composição de resiliência com cockatiel

```typescript
// src/infra/resilience.ts
import {
  Policy,
  retry,
  ExponentialBackoff,
  circuitBreaker,
  ConsecutiveBreaker,
  bulkhead,
  timeout,
  TimeoutStrategy,
} from 'cockatiel';

/**
 * Cria uma política de resiliência composta para chamadas a serviços externos.
 * Composição: bulkhead → circuit breaker → retry → timeout → chamada real
 */
export function createResilientPolicy(options: {
  name: string;
  concurrency?: number;      // bulkhead: máx. chamadas simultâneas
  breakerThreshold?: number; // circuit breaker: falhas consecutivas para abrir
  maxAttempts?: number;      // retry: máximo de tentativas
  timeoutMs?: number;        // timeout por tentativa
}) {
  const {
    name,
    concurrency = 10,
    breakerThreshold = 5,
    maxAttempts = 3,
    timeoutMs = 5_000,
  } = options;

  const timeoutPolicy = timeout(timeoutMs, TimeoutStrategy.Aggressive);

  const retryPolicy = retry(Policy.handleAll(), {
    maxAttempts,
    backoff: new ExponentialBackoff({
      initialDelay: 100,
      maxDelay: 5_000,
      exponent: 2,
    }),
  });

  const cbPolicy = circuitBreaker(Policy.handleAll(), {
    halfOpenAfter: 10_000, // tenta fechar o circuito após 10s
    breaker: new ConsecutiveBreaker(breakerThreshold),
  });

  cbPolicy.onHalfOpen(() => console.warn(`[resilience:${name}] circuit half-open`));
  cbPolicy.onBreak(() => console.error(`[resilience:${name}] circuit OPEN — calls blocked`));
  cbPolicy.onReset(() => console.info(`[resilience:${name}] circuit closed`));

  const bulkheadPolicy = bulkhead(concurrency, concurrency * 2); // queue até 2x concurrency

  // Composição: bulkhead > circuit breaker > retry > timeout
  return Policy.wrap(bulkheadPolicy, cbPolicy, retryPolicy, timeoutPolicy);
}

// Exemplo de uso: chamada HTTP protegida por resiliência
import { fetch } from 'undici';

const inventoryPolicy = createResilientPolicy({
  name: 'inventory-service',
  concurrency: 8,
  breakerThreshold: 5,
  maxAttempts: 3,
  timeoutMs: 3_000,
});

export async function getInventory(productId: string): Promise<{ quantity: number }> {
  return inventoryPolicy.execute(async () => {
    const res = await fetch(
      `${process.env.INVENTORY_SERVICE_URL}/products/${productId}/inventory`,
    );

    if (!res.ok) {
      throw new Error(`inventory-service responded ${res.status}`);
    }

    return res.json() as Promise<{ quantity: number }>;
  });
}
```

### Snippet 4 — Graceful shutdown que desconecta todos os clientes

```typescript
// src/infra/shutdown.ts
import { pgPool } from './clients';
import { redis, emailQueue } from './clients';
import { consumer, producer } from './kafka';

type ShutdownHook = () => Promise<void>;

const shutdownHooks: ShutdownHook[] = [];

/** Registra um hook de shutdown. Executado em ordem LIFO. */
export function onShutdown(hook: ShutdownHook): void {
  shutdownHooks.unshift(hook);
}

/** Executa todos os hooks e encerra o processo. */
async function shutdown(signal: string): Promise<void> {
  console.log(`[shutdown] received ${signal} — starting graceful shutdown`);

  const results = await Promise.allSettled(
    shutdownHooks.map((hook) => hook()),
  );

  results.forEach((result, i) => {
    if (result.status === 'rejected') {
      console.error(`[shutdown] hook #${i} failed:`, result.reason);
    }
  });

  console.log('[shutdown] all hooks executed — exiting');
  process.exit(0);
}

// Registrar hooks dos clientes de infraestrutura
onShutdown(async () => {
  console.log('[shutdown] closing BullMQ queues');
  await emailQueue.close();
});

onShutdown(async () => {
  console.log('[shutdown] disconnecting Kafka consumer');
  await consumer.disconnect();
});

onShutdown(async () => {
  console.log('[shutdown] disconnecting Kafka producer');
  await producer.disconnect();
});

onShutdown(async () => {
  console.log('[shutdown] closing ioredis connection');
  await redis.quit();
});

onShutdown(async () => {
  console.log('[shutdown] draining pg pool');
  await pgPool.end();
});

// Registrar sinais do sistema operacional
process.once('SIGTERM', () => shutdown('SIGTERM'));
process.once('SIGINT', () => shutdown('SIGINT'));
process.once('SIGUSR2', () => shutdown('SIGUSR2')); // nodemon restart
```

## Tabela de comparação

| Tecnologia | Caso de uso primário | Quando NÃO usar | Notas |
|---|---|---|---|
| `pg` (node-postgres) | Queries SQL manuais, performance crítica | Modelo de domínio rico que se beneficia de ORM | Pool de conexões embutido; use `pg-native` para ganho adicional de performance |
| `postgres.js` | DX moderna com tagged templates, projetos novos | Equipe já padronizou em `pg` ou ORM | Tagged template literals previnem SQL injection por padrão; pool embutido |
| `ioredis` | Cache, pub/sub, locks distribuídos, rate limiting | Filas com garantia de entrega (use BullMQ) | Auto-reconnect, suporte a Redis Cluster e Sentinel, pipelining automático |
| `bullmq` | Filas de tarefas com retry, DLQ, cron, dependências | Alto volume de eventos (>10k/s) ou replay histórico | Implementado sobre Redis com scripts Lua atômicos; board UI com BullMQ Pro |
| `kafkajs` | Streaming de eventos, fan-out, replay, audit log | Overhead operacional inaceitável para o problema | Consumer groups para múltiplos consumers independentes; Schema Registry para evolução de schema |
| `@grpc/grpc-js` | Comunicação interna entre microserviços | Browser como cliente direto (requer grpc-web) | HTTP/2 multiplexing, streaming bidirecional, contrato `.proto` versionado |
| `@apollo/server` | GraphQL em projetos com múltiplos clientes e federation | APIs simples; alta latência do runtime é inaceitável | Schema federation para monorepo de serviços GraphQL; plugins para APM e auth |
| `mercurius` | GraphQL em APIs Fastify com performance máxima | Projeto que não usa Fastify como base | JIT de resolvers; integração nativa com o ecossistema Fastify |
| `ws` | WebSocket puro sem abstração | Precisa de rooms, namespaces ou fallback HTTP | Zero overhead; use diretamente quando protocolo customizado é necessário |
| `socket.io` | Tempo real com rooms, namespaces, scaling horizontal | Baixíssimo overhead de memória é crítico | Redis adapter para broadcast em múltiplas instâncias; fallback automático para long-polling |
| `fetch` (nativo) | Chamadas HTTP simples em Node 18+ | Retry nativo ou interceptors globais são necessários | Zero dependências; base do `undici`; combine com cockatiel para resiliência |
| `axios` | Codebases existentes, interceptors globais, TypeScript generics | Projetos novos onde `fetch` ou `got` são suficientes | `axios.create()` para instâncias por base URL; interceptors para auth e logging centralizado |
| `got` | Chamadas externas com retry nativo, streams, progresso | Compatibilidade com browser necessária | ESM only desde v12; retry com backoff embutido; suporte a OAuth |
| `undici` | Performance máxima, proxy/gateway, controle de pool | Chamadas simples onde `fetch` é suficiente | Menor overhead de CPU por requisição; `undici.Pool` para reuso agressivo de conexões |
| `cockatiel` | Composição de retry + CB + bulkhead + timeout | Projeto usa `opossum` já estabelecido | API funcional e composável; suporte a TypeScript de primeira classe |
| `opossum` | Circuit breaker stand-alone | Precisa de composição com retry e bulkhead em uma policy única | API mais simples que cockatiel; eventos para monitoramento (`open`, `close`, `halfOpen`) |

## Padrões transversais

Estes padrões se aplicam a **toda** integração Node.js de produção, independentemente da tecnologia:

**Connection pooling obrigatório** — nunca crie uma conexão por request. Use `pg.Pool`, `undici.Pool` e confie no pool embutido do `ioredis`. Dimensione o pool com base no número de CPUs disponíveis no backend e no número de instâncias do serviço. Uma regra prática: `pool_size = (número de CPUs do DB * 2) / número de instâncias da API`.

**Timeouts em duas camadas** — configure `connectTimeout` (tempo para estabelecer a conexão TCP/TLS) e `requestTimeout` (tempo para receber a resposta completa). Uma chamada sem timeout pode bloquear um worker Node.js indefinidamente. No PostgreSQL, use também `statement_timeout` para queries que podem explodir em complexidade.

**Graceful shutdown** — ao receber `SIGTERM` (sinal padrão do Kubernetes para encerrar pods), o processo deve: parar de aceitar novas conexões, aguardar requests em andamento finalizarem (com timeout máximo de 30s), e desconectar todos os clientes explicitamente. Veja o Snippet 4 para a implementação de referência.

**Retry + circuit breaker em toda chamada externa** — use retry com backoff exponencial e jitter para erros transientes. Use circuit breaker para parar de tentar quando o backend está claramente fora. A ausência de circuit breaker transforma a falha de um serviço downstream em falha de cascata para todos os serviços que dependem dele.

**Health check que sonda as integrações** — o endpoint `/health` (ou `/readiness` em Kubernetes) deve verificar ativamente se as integrações estão funcionais: executar um `SELECT 1` no PostgreSQL, um `PING` no Redis, verificar se o consumer Kafka está conectado. Um pod que reporta `healthy` mas não consegue falar com o banco é um pod quebrado em operação silenciosa.

**Observabilidade embutida** — instrumente todas as integrações com métricas (latência p50/p99, taxa de erro, tamanho do pool) e traces distribuídos (OpenTelemetry). Sem métricas, é impossível distinguir "conexão lenta com o banco" de "lógica de negócio lenta" durante um incidente.

## Em entrevista

**Q: "How do you choose between REST, GraphQL, and gRPC for a new service?"**

The decision starts with understanding who controls both sides of the communication and who the clients are. For internal service-to-service communication where my team owns both the server and client, I prefer gRPC because the `.proto` contract is enforced at compile time, HTTP/2 gives us multiplexing and streaming out of the box, and the performance overhead is significantly lower than JSON over HTTP/1.1. For public APIs consumed by external clients — browsers, mobile apps, third-party partners — I default to REST because it requires no code generation on the client side, has universal tooling support, and OpenAPI documentation is well understood across the industry. GraphQL enters the picture when I have multiple client types — web, mobile, TV — with genuinely different data needs, or when I'm building a BFF (Backend for Frontend) that needs to aggregate data from multiple services in a single request without over-fetching. The anti-pattern I avoid is choosing GraphQL for a simple CRUD API with three entities — the schema, resolver, and N+1 complexity outweigh the benefits in those cases.

**Q: "What transversal patterns do you always apply to Node.js integrations in production?"**

There are five patterns I treat as non-negotiable for any integration. First, connection pooling — I never open a new database or Redis connection per request; I configure pools with explicit min/max limits and tune them based on the backend's capacity and the number of service instances. Second, dual timeouts — a connect timeout to fail fast if the infrastructure is unreachable, and a request timeout to prevent a slow downstream from blocking a Node.js worker thread indefinitely. Third, graceful shutdown — on SIGTERM I stop accepting new requests, wait for in-flight work to complete, and then explicitly disconnect all clients (pg pool, ioredis, Kafka consumer, BullMQ worker) before the process exits; this is essential for zero-downtime deployments on Kubernetes. Fourth, retry with exponential backoff plus circuit breaker — I use cockatiel or opossum to wrap every external call; retry handles transient errors, and the circuit breaker prevents cascade failures when a downstream service is truly down. Fifth, active health checks — my readiness probe actually probes the integrations (SELECT 1 to Postgres, PING to Redis) so Kubernetes routes traffic away from pods that can't reach their dependencies.

**Q: "How do you handle cascading failures when one of your downstream dependencies goes down?"**

Cascading failure is the scenario where one slow or unavailable downstream brings down the entire system — a classic fallacy of distributed systems. My primary defense is the circuit breaker pattern: I wrap every downstream call with a circuit breaker that counts consecutive failures and opens the circuit after a configurable threshold, blocking further attempts and returning a fast failure instead of accumulating blocked threads. A half-open probe after a cooldown period allows the circuit to recover automatically when the downstream comes back. The circuit breaker alone is not enough because it doesn't prevent one slow downstream from consuming all available concurrency — for that I add a bulkhead, which caps the number of concurrent calls to a specific integration, so a slow inventory service can't exhaust the thread pool and starve calls to the payments service. I complement this with retry with exponential backoff and jitter to handle transient errors without creating a thundering herd on recovery. At the architectural level, I design for degraded operation: if the recommendations service is down, the product page should still load without recommendations rather than returning a 500. This means explicitly deciding which integrations are on the critical path and which can be gracefully degraded.

## Vocabulário

| Termo | Definição |
|---|---|
| Connection pool | Conjunto de conexões pré-estabelecidas e reutilizadas entre requests, evitando o overhead de criar e destruir conexões TCP/TLS a cada chamada |
| Circuit breaker | Padrão que monitora falhas em uma integração e "abre o circuito" quando um limiar é atingido, bloqueando novas tentativas por um período de cooldown para evitar cascata |
| Bulkhead | Padrão que limita a concorrência máxima para uma integração específica, isolando falhas de um backend para que não consumam todos os recursos disponíveis |
| Graceful shutdown | Processo de encerramento ordenado: parar de aceitar novas conexões, aguardar operações em andamento e desconectar clientes explicitamente antes de sair |
| Idempotency key | Chave única enviada pelo cliente que permite ao servidor identificar e deduplicar requests repetidos, garantindo que operações com efeito colateral não sejam executadas mais de uma vez |
| Thundering herd | Fenômeno em que múltiplos clientes tentam reconectar ou retentar simultaneamente após uma falha, sobrecarregando o backend no momento em que ele se recupera; mitigado com jitter no backoff |
| Backoff | Estratégia de espera crescente entre tentativas de retry; backoff exponencial com jitter distribui as tentativas no tempo e evita thundering herd |
| Fan-out | Padrão em que uma mensagem publicada em um tópico ou canal é entregue a múltiplos consumers independentes simultaneamente; típico em Kafka com múltiplos consumer groups |
| Consumer group | Abstração do Kafka que permite a um conjunto de consumers dividir as partições de um tópico entre si; múltiplos grupos independentes podem consumir o mesmo tópico sem interferência |
| Schema registry | Serviço centralizado (ex.: Confluent Schema Registry) que armazena e versiona schemas Avro/Protobuf/JSON para tópicos Kafka, garantindo compatibilidade na evolução do contrato |
| Dead-letter queue | Fila ou tópico especial onde mensagens que falharam após todos os retries são enviadas para análise manual, evitando que mensagens com problema bloqueiem o processamento normal |

## Veja também

- [[03-Dominios/Node/Integrações/index|Integrações]] — índice do galho 9 com todos os tópicos
- [[03-Dominios/Node/ORMs e banco de dados/index|ORMs e banco de dados]] — galho 6: Prisma, TypeORM, Sequelize, Drizzle
- [[03-Dominios/Node/Observability e produção/index|Observability e produção]] — galho 5: métricas, traces, health checks em produção
- [[03-Dominios/Node/Frameworks e arquitetura/index]] — galho 4: Fastify, Express, arquitetura de APIs
- [[03-Dominios/Node/Runtime e Event Loop/index]] — galho 1: event loop, async/await, I/O não-bloqueante
