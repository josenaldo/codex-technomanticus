---
title: "BullMQ"
created: 2026-04-01
updated: 2026-04-10
type: concept
status: evergreen
tags:
  - arquitetura
  - mensageria
  - javascript
  - entrevista
publish: false
---

# BullMQ

Biblioteca de **job queue** para Node.js baseada em Redis — background jobs, scheduling, rate limiting, retries, flows e workers distribuídos. É a escolha padrão para processamento assíncrono em aplicações Node.js que já usam (ou podem usar) Redis. Enquanto [[03-Dominios/Arquitetura/Mensageria/Kafka]] é uma plataforma de event streaming e [[RabbitMQ]] é um message broker com routing flexível, BullMQ é uma **job queue especializada** para o ecossistema Node.js.

## O que é

BullMQ é uma biblioteca Node.js/TypeScript para processamento de **jobs** (tarefas) em filas, usando Redis como backend. É a evolução do **Bull** (escrito pelo mesmo autor, Manuel Astudillo), com suporte a flows (DAGs de jobs), rate limiting mais robusto, melhor TypeScript support, e reescrita em classes modernas.

**Por que existe:**
- Node.js é single-threaded. Operações pesadas (imagens, relatórios, APIs externas lentas) bloqueiam o event loop.
- Solução: mover trabalho pesado para **workers** (processos ou containers separados), comunicando via fila.
- Redis é frequentemente já presente (cache, session store) — reutilizar reduz infraestrutura.
- BullMQ oferece tudo que job queue séria precisa: delays, retries, priorities, scheduling, flows, dashboards.

Em entrevistas, o que diferencia um senior em BullMQ:

1. **Saber quando usar e quando NÃO** — BullMQ é para jobs (task queue), não para event streaming ou pub/sub inter-serviços multi-stack
2. **Conhecer as features avançadas** — flows, rate limiters, parentless dependencies, job schedulers
3. **Idempotência** — BullMQ garante at-least-once; jobs devem ser idempotentes
4. **Observabilidade** — Bull Board ou Arena para monitorar filas em produção
5. **Saber como escalar** — múltiplos workers, concurrency por worker, sandboxed processors

---

## Conceitos fundamentais

### Queue

A fila é onde jobs são enfileirados para processamento futuro. Cada fila tem um nome e é identificada no Redis.

```typescript
import { Queue } from 'bullmq';

const emailQueue = new Queue('emails', {
  connection: { host: 'localhost', port: 6379 }
});
```

### Job

Um job é uma unidade de trabalho. Tem um nome, dados (payload), e opções (delay, priority, retries).

```typescript
await emailQueue.add('welcome-email', {
  to: 'paciente@example.com',
  template: 'welcome',
  data: { name: 'Maria' }
});
```

### Worker

O worker consome jobs da fila e executa o processamento.

```typescript
import { Worker } from 'bullmq';

const emailWorker = new Worker('emails', async (job) => {
  const { to, template, data } = job.data;
  await sendEmail(to, template, data);
  return { sent: true };  // valor de retorno salvo em job.returnvalue
}, {
  connection: { host: 'localhost', port: 6379 },
  concurrency: 5  // processa até 5 jobs em paralelo
});

emailWorker.on('completed', (job) => {
  console.log(`Job ${job.id} completed`);
});

emailWorker.on('failed', (job, err) => {
  console.error(`Job ${job?.id} failed:`, err.message);
});
```

### QueueEvents

Escutar eventos globais da fila (não apenas do seu worker local).

```typescript
import { QueueEvents } from 'bullmq';

const queueEvents = new QueueEvents('emails', { connection });

queueEvents.on('completed', ({ jobId, returnvalue }) => {
  console.log(`Job ${jobId} completed globally`);
});

queueEvents.on('failed', ({ jobId, failedReason }) => {
  console.log(`Job ${jobId} failed: ${failedReason}`);
});

queueEvents.on('progress', ({ jobId, data }) => {
  console.log(`Job ${jobId} progress: ${data}%`);
});
```

### FlowProducer

Para criar fluxos hierárquicos de jobs (parent-child). Útil quando um job depende do resultado de outros.

```typescript
import { FlowProducer } from 'bullmq';

const flowProducer = new FlowProducer({ connection });

await flowProducer.add({
  name: 'generate-report',
  queueName: 'reports',
  data: { reportId: '42' },
  children: [
    { name: 'fetch-patients', queueName: 'data', data: {} },
    { name: 'fetch-appointments', queueName: 'data', data: {} },
    { name: 'fetch-payments', queueName: 'data', data: {} }
  ]
});
// O job parent só executa após todos os children completarem
```

---

## Features essenciais

### Delayed jobs

Executar um job em um momento futuro.

```typescript
// Lembrete 1 hora antes da consulta
await reminderQueue.add('appointment-reminder',
  { appointmentId: '42' },
  { delay: 3600 * 1000 }  // 1 hora em ms
);

// Delay absoluto com timestamp
const target = new Date('2026-04-15T10:00:00Z');
await queue.add('scheduled-task', data, {
  delay: target.getTime() - Date.now()
});
```

### Repeatable jobs (cron)

Jobs que executam em intervalos ou conforme cron expression.

```typescript
// A cada 10 minutos
await queue.add('sync-external-data', {}, {
  repeat: { every: 10 * 60 * 1000 }
});

// Cron: todo dia às 3am
await queue.add('daily-report', {}, {
  repeat: { pattern: '0 3 * * *' }
});

// Com limite de execuções
await queue.add('limited-task', {}, {
  repeat: { every: 60000, limit: 10 }
});
```

### Retries e backoff

```typescript
await queue.add('external-api-call', data, {
  attempts: 5,
  backoff: {
    type: 'exponential',
    delay: 1000  // 1s, 2s, 4s, 8s, 16s
  }
});

// Backoff customizado
await queue.add('task', data, {
  attempts: 3,
  backoff: {
    type: 'custom'
  }
});

// No worker, implementar a estratégia customizada
new Worker('queue', handler, {
  connection,
  settings: {
    backoffStrategy: (attemptsMade) => Math.random() * 10000  // até 10s random
  }
});
```

**Importante:** BullMQ faz retry automático em caso de erro **não capturado** no handler. Se você captura o erro e retorna normalmente, o job é considerado sucesso.

### Priorities

```typescript
await queue.add('urgent-notification', data, { priority: 1 });   // maior prioridade
await queue.add('normal-task', data, { priority: 5 });
await queue.add('low-task', data, { priority: 10 });             // menor prioridade
// Menor número = maior prioridade
```

**Cuidado:** priorities adicionam overhead. Use apenas se realmente precisa — para a maioria dos casos, filas separadas por prioridade são mais eficientes.

### Rate limiting

Limitar quantos jobs por intervalo o worker processa — útil para respeitar rate limits de APIs externas.

```typescript
new Worker('emails', handler, {
  connection,
  limiter: {
    max: 100,       // máximo 100 jobs
    duration: 60000 // por minuto
  }
});
```

**Exemplo real:** integração com API externa que limita a 10 req/s.

```typescript
new Worker('external-api-sync', async (job) => {
  await externalApi.call(job.data);
}, {
  limiter: { max: 10, duration: 1000 }  // 10 por segundo
});
```

### Concurrency

Um worker pode processar múltiplos jobs em paralelo.

```typescript
new Worker('queue', handler, {
  connection,
  concurrency: 10  // até 10 jobs simultâneos
});
```

**Gotcha:** concurrency alta + operações CPU-bound bloqueia o event loop. Para CPU-heavy, use **sandboxed processors**.

### Sandboxed processors

Roda o handler em um processo Node.js separado. Útil para CPU-bound ou para isolar falhas.

```typescript
// worker.ts — processo principal
new Worker('image-processing', __dirname + '/processors/resize.js', {
  connection,
  concurrency: 5  // cada job roda em um processo filho
});

// processors/resize.js — processo isolado
module.exports = async (job) => {
  return await resizeImage(job.data);
};
```

**Prós:** não bloqueia o event loop do worker principal, crashes isolados.

**Contras:** overhead de fork, sem acesso ao state do worker principal.

### Flows (DAGs de jobs)

```typescript
const flow = await flowProducer.add({
  name: 'checkout',
  queueName: 'orders',
  data: { orderId: '42' },
  children: [
    {
      name: 'charge-payment',
      queueName: 'payments',
      data: { amount: 100 }
    },
    {
      name: 'reserve-inventory',
      queueName: 'inventory',
      data: { items: [...] }
    },
    {
      name: 'send-confirmation',
      queueName: 'emails',
      data: { to: '...' },
      // Depende de outro child implicitamente via flow structure
    }
  ]
});
```

**Semântica:** o parent job só executa quando **todos** os children completam com sucesso. Se qualquer child falha permanentemente, o parent falha também.

**Uso:** workflows complexos, composição de tarefas, map-reduce.

### Job scheduler (BullMQ 5+)

Nova API mais robusta para jobs recorrentes (substitui parcialmente `repeat`):

```typescript
await queue.upsertJobScheduler(
  'daily-report-scheduler',
  { pattern: '0 3 * * *' },  // todo dia 3am
  {
    name: 'generate-daily-report',
    data: { reportType: 'sales' }
  }
);
```

Vantagem: scheduler tem ID único e é idempotente (chamar upsert múltiplas vezes não duplica).

---

## Padrões de uso

### Producer + Worker separados

A arquitetura mais comum: a API publica jobs, workers dedicados consomem.

```
┌─────────────┐              ┌──────────┐              ┌──────────────┐
│   API       │  .add(job)   │  Redis   │  .process()  │   Worker     │
│ (express)   │ ───────────→ │ (BullMQ) │ ────────────→│ (process)    │
└─────────────┘              └──────────┘              └──────────────┘
```

**Vantagens:**
- API responde rápido (não bloqueia)
- Workers escalam independentemente
- Worker pode ser reiniciado sem afetar API
- Workers podem rodar em containers diferentes, máquinas diferentes

```typescript
// api.ts
import express from 'express';
import { Queue } from 'bullmq';

const app = express();
const emailQueue = new Queue('emails', { connection });

app.post('/users', async (req, res) => {
  const user = await createUser(req.body);
  await emailQueue.add('welcome', { userId: user.id });
  res.status(201).json(user);  // responde sem esperar email
});

// worker.ts — processo separado
import { Worker } from 'bullmq';
new Worker('emails', async (job) => {
  await sendWelcomeEmail(job.data.userId);
}, { connection, concurrency: 10 });
```

### Graceful shutdown

```typescript
const worker = new Worker(/* ... */);

process.on('SIGTERM', async () => {
  console.log('SIGTERM received, closing worker...');
  await worker.close();  // termina jobs em andamento, não aceita novos
  await emailQueue.close();
  process.exit(0);
});
```

**Importante:** `worker.close()` espera jobs em andamento terminarem antes de fechar. Sem isso, jobs em execução são interrompidos e marcados como stalled.

### Idempotência

BullMQ garante at-least-once (jobs podem ser reprocessados em retries ou após crash). Workers devem ser idempotentes.

```typescript
new Worker('payments', async (job) => {
  const { paymentId } = job.data;

  // Idempotência: checar se já processado
  const existing = await db.payments.findOne({ externalId: paymentId });
  if (existing && existing.status === 'processed') {
    return { alreadyProcessed: true };
  }

  await processPayment(paymentId);
  await db.payments.updateOne({ externalId: paymentId }, { status: 'processed' });
});
```

### Job progress

Reportar progresso de jobs longos para UI ou monitoramento.

```typescript
new Worker('reports', async (job) => {
  const total = 1000;
  for (let i = 0; i < total; i++) {
    await processItem(i);
    await job.updateProgress(Math.floor((i / total) * 100));
  }
});

// Client pode escutar progress
queueEvents.on('progress', ({ jobId, data }) => {
  console.log(`Job ${jobId}: ${data}%`);
});
```

### Cancelamento de jobs

```typescript
const job = await queue.add('long-task', data);

// Algum tempo depois
await job.remove();  // remove se ainda não iniciado
// Para cancelar em execução, o handler precisa cooperar
```

**Cancelamento em execução:** BullMQ não tem kill forçado. O handler precisa verificar periodicamente um flag ou usar AbortController.

```typescript
new Worker('tasks', async (job) => {
  const ac = new AbortController();

  // Escuta eventos para cancelar
  queueEvents.on('removed', ({ jobId }) => {
    if (jobId === job.id) ac.abort();
  });

  await longRunningOperation({ signal: ac.signal });
});
```

---

## Observabilidade

### Bull Board

Dashboard web para monitorar filas em desenvolvimento e produção.

```typescript
import { createBullBoard } from '@bull-board/api';
import { BullMQAdapter } from '@bull-board/api/bullMQAdapter';
import { ExpressAdapter } from '@bull-board/express';

const serverAdapter = new ExpressAdapter();
serverAdapter.setBasePath('/admin/queues');

createBullBoard({
  queues: [
    new BullMQAdapter(emailQueue),
    new BullMQAdapter(reportQueue),
    new BullMQAdapter(paymentQueue)
  ],
  serverAdapter,
});

app.use('/admin/queues', serverAdapter.getRouter());
```

Acesse `http://localhost:3000/admin/queues` para ver:
- Jobs waiting, active, completed, failed, delayed
- Detalhes de cada job (data, logs, stacktrace)
- Retry manual de jobs falhados
- Limpeza de jobs antigos
- Taxa de processamento

**Proteja com auth em produção:**

```typescript
app.use('/admin/queues', basicAuth({ users: { admin: 'secret' } }), serverAdapter.getRouter());
```

### Arena (alternativa)

Dashboard similar, mais antigo mas ainda popular:

```bash
npm install bull-arena
```

### Métricas Prometheus

Para integrar com Grafana, exporte métricas manualmente via `queueEvents`:

```typescript
import { register, Counter, Gauge } from 'prom-client';

const jobsCompletedTotal = new Counter({
  name: 'bullmq_jobs_completed_total',
  help: 'Total completed jobs',
  labelNames: ['queue']
});

const jobsFailedTotal = new Counter({
  name: 'bullmq_jobs_failed_total',
  help: 'Total failed jobs',
  labelNames: ['queue']
});

const queueWaiting = new Gauge({
  name: 'bullmq_queue_waiting',
  help: 'Waiting jobs count',
  labelNames: ['queue']
});

queueEvents.on('completed', () => jobsCompletedTotal.inc({ queue: 'emails' }));
queueEvents.on('failed', () => jobsFailedTotal.inc({ queue: 'emails' }));

// Poll periódico da quantidade waiting
setInterval(async () => {
  const count = await emailQueue.getWaitingCount();
  queueWaiting.set({ queue: 'emails' }, count);
}, 5000);
```

### Métricas importantes

- **Waiting jobs** — crescimento contínuo indica workers lentos ou parados
- **Active jobs** — quantos em processamento
- **Failed jobs** — deveria ser baixo; picos indicam problema
- **Completed per second** — throughput efetivo
- **Average processing time** — evolução indica degradação
- **Stalled jobs** — jobs travados (worker morreu sem liberar lock)

---

## Connection e Redis

### Configuração

```typescript
import { Queue } from 'bullmq';
import IORedis from 'ioredis';

// Connection única reutilizada
const connection = new IORedis({
  host: process.env.REDIS_HOST,
  port: parseInt(process.env.REDIS_PORT!),
  password: process.env.REDIS_PASSWORD,
  maxRetriesPerRequest: null,  // OBRIGATÓRIO para BullMQ
  enableReadyCheck: false,
});

const queue = new Queue('emails', { connection });
```

**⚠️ `maxRetriesPerRequest: null` é obrigatório** — sem isso, BullMQ pode falhar silenciosamente em reconexões.

### Redis Cluster

BullMQ suporta Redis Cluster desde a versão 4+:

```typescript
import { Cluster } from 'ioredis';

const connection = new Cluster([
  { host: 'redis-node-1', port: 6379 },
  { host: 'redis-node-2', port: 6379 },
  { host: 'redis-node-3', port: 6379 },
], {
  redisOptions: { password: 'secret' }
});
```

**Cuidado:** flows (FlowProducer) têm limitações em cluster porque dependem de multi-key operations.

### Redis requirements

- Redis 6.2+ (recomendado 7+ para melhor performance)
- Memory: jobs ficam em memória até processados + dados históricos. Dimensione com folga.
- Persistence: use AOF (Append-Only File) se perder jobs é inaceitável

---

## Limpeza e retenção

Jobs completados e falhados ficam no Redis por default. Em produção, limpe periodicamente.

### Auto-cleanup

```typescript
const emailQueue = new Queue('emails', {
  connection,
  defaultJobOptions: {
    removeOnComplete: {
      age: 3600,        // remover após 1h
      count: 1000       // manter no máximo 1000
    },
    removeOnFail: {
      age: 24 * 3600    // falhados ficam 24h para debug
    }
  }
});
```

### Limpeza manual

```typescript
// Limpar jobs completados mais antigos que 1 dia
await queue.clean(24 * 3600 * 1000, 0, 'completed');

// Limpar jobs falhados
await queue.clean(7 * 24 * 3600 * 1000, 0, 'failed');

// Drain: remover todos os jobs waiting
await queue.drain();

// Obliterate: apagar TUDO da fila (incluindo active)
await queue.obliterate({ force: true });
```

---

## Quando usar (e quando NÃO)

### Use BullMQ quando:

- **Background jobs em aplicação Node.js** — emails, relatórios, processamento de imagens, syncs com APIs externas
- **Job scheduling** — cron jobs, lembretes, tarefas recorrentes
- **Rate limiting de calls externas** — respeitar quotas de API de terceiros
- **Filas com retries robustos** — exponential backoff, priority
- **Workflows hierárquicos** (flows) — composição de tarefas dependentes
- **Já usa Redis** e quer minimizar infraestrutura adicional
- **Equipe Node.js-only** — domina o ecossistema

### NÃO use BullMQ quando:

- **Precisa de event streaming / replay** → use Kafka
- **Comunicação entre serviços de linguagens diferentes** → use RabbitMQ, Kafka, NATS
- **Ordenação estrita de milhões de eventos** → Kafka
- **Pub/sub multi-consumer com consumer groups independentes** → Kafka
- **Sem Redis disponível e não quer adicionar** → considere BullMQ+Postgres (Graphile Worker) ou SQS
- **Escala enorme** (milhões de jobs/dia) → Redis como broker tem limites; Kafka escala melhor

### Alternativas no ecossistema Node

- **Graphile Worker** — job queue com PostgreSQL, sem Redis
- **Agenda** — scheduling em MongoDB
- **Bee-Queue** — mais simples que BullMQ, menos features
- **Kue** — legado, sem manutenção ativa
- **node-cron** — só scheduling in-process, sem persistência
- **RabbitMQ + amqplib** — quando precisa do poder do RabbitMQ em Node.js

---

## Armadilhas comuns

- **Esquecer `maxRetriesPerRequest: null`** — erros silenciosos em reconexão
- **Worker sem idempotência** — jobs reprocessados em retries causam duplicação (emails duplicados, cobranças dobradas)
- **Concurrency alto em CPU-bound** — bloqueia event loop, tudo vira lento. Use sandboxed processors.
- **Não limpar jobs completados** — Redis enche com milhões de jobs antigos, performance degrada
- **Não proteger Bull Board em produção** — dashboard com dados sensíveis exposto publicamente
- **Processar jobs dentro da API (mesmo processo)** — API lenta, não escala, derruba tudo se worker crashar
- **Job data gigante** — payloads enormes estouram memória. Passe IDs, não dados.
- **Sem graceful shutdown** — deploy interrompe jobs, eles ficam stalled
- **Sem monitoring de waiting count** — lag cresce silenciosamente até alguém reclamar
- **Retry sem limite** — jobs venenosos giram em loop para sempre
- **Sem DLQ conceitual** — em BullMQ, use `removeOnFail: false` + monitoring de failed + replay manual
- **Flows em Redis Cluster sem testar** — limitações de multi-key operations podem quebrar
- **Scheduler repeat duplicado** — `repeat: { every: 1000 }` com jobId diferente cria múltiplos schedulers. Use `jobId` consistente ou `upsertJobScheduler`.
- **Connection pooling errado** — criar Queue/Worker em cada request vaza conexões. Singleton.
- **Ignorar rate limiter da fonte externa** — API retorna 429 em massa, jobs ficam em retry, fila explode
- **Confundir BullMQ com pub/sub** — BullMQ é job queue (cada job processado uma vez). Não é broadcast.

---

## Na prática (da minha experiência)

> **MedEspecialista — BullMQ para processamento assíncrono:**
> No MedEspecialista, uso BullMQ no backend Node.js para várias tarefas assíncronas:
>
> **1. Envio de emails e SMS:** quando uma consulta é confirmada, a API publica um job na fila `notifications` e responde ao cliente imediatamente. Um worker separado processa a fila, com rate limit de 50 msgs/s para respeitar o provedor (SendGrid). Retries com exponential backoff (5 tentativas), e jobs falhados ficam 7 dias para investigação.
>
> **2. Geração de relatórios:** relatórios PDF grandes demoram 30-60s. Impossível fazer síncrono — o usuário receberia timeout. Worker dedicado processa (sandboxed processor, porque puppeteer é CPU-heavy). O usuário acompanha via Server-Sent Events que escutam `queueEvents.on('progress')`. Quando completa, notificação in-app + email com link pro download.
>
> **3. Syncs com APIs externas:** integração com clínicas parceiras via API REST. Cron via `repeat`: a cada 10 minutos, um job `sync-partners` busca dados de todos os parceiros. Rate limiter garante que não excedemos as quotas. Falhas geram alerta no Slack.
>
> **4. Cleanup schedulers:** cron jobs diários à 3am para limpeza de dados temporários, geração de métricas agregadas, e backups de arquivos de exame.
>
> **Lições aprendidas:**
>
> **1. Idempotência é mandatória.** Tive um bug onde um worker processou o mesmo job duas vezes após um crash — email duplicado foi enviado. Desde então, todo worker tem checagem de "já processado" antes de agir.
>
> **2. Bull Board salva vidas em debugging.** Quando usuário reporta "não recebi o email", eu abro o dashboard, busco pelo user_id, vejo se o job foi criado, se foi processado, se falhou, e por quê. Sem dashboard, seria escavar logs por horas.
>
> **3. Sandboxed processor para puppeteer.** Inicialmente colocamos puppeteer direto no worker principal. Resultado: um crash de chrome derrubava o worker inteiro e travava jobs em paralelo. Mudamos para sandboxed processor — cada PDF roda em processo isolado, crashes não afetam outros jobs.
>
> **4. Rate limiter por worker ≠ rate limiter global.** Tínhamos 3 instâncias do worker e rate limiter configurado em `max: 10/s`. Na prática, isso era 30/s total (cada worker com seu próprio limiter). Precisamos implementar rate limiting centralizado com Redis para respeitar a quota global.
>
> **5. Graceful shutdown é crítico em deploy.** Antes de implementar, cada deploy interrompia jobs no meio, deixando-os stalled. Workers começavam ao reiniciar e reprocessavam (idempotência salvou) — mas o usuário via delays. `worker.close()` no SIGTERM resolveu.
>
> **A lição principal:** BullMQ é extremamente produtivo para Node.js. É simples de começar, tem todas as features que você vai precisar (delayed, recurring, retries, rate limiting, flows), e se integra bem com Redis que a maioria dos projetos já tem. Mas é uma **job queue**, não um **event broker**. Se seu caso é "múltiplos serviços reagindo ao mesmo evento", use Kafka. Se é "processar este trabalho depois", BullMQ é a escolha certa.

---

## How to explain in English

> "BullMQ is my default choice for background job processing in Node.js applications. It's a job queue library built on top of Redis, which means if you're already using Redis for caching or sessions, adding BullMQ doesn't require new infrastructure.
>
> The mental model is straightforward: the API publishes a job — 'send this welcome email', 'generate this report', 'sync with this external API' — and a separate worker process picks it up and executes it. The API responds to the user immediately without waiting, and the heavy work happens in the background. This is essential for Node.js because the main thread can't block without affecting all concurrent requests.
>
> BullMQ supports everything a production job queue needs: delayed jobs for scheduled tasks, repeatable jobs with cron patterns, retries with exponential backoff, priorities, rate limiting, and flows for hierarchical job dependencies. For UI feedback on long-running jobs, I use the progress API combined with Server-Sent Events.
>
> A few production practices are critical. First, workers must be idempotent, because BullMQ provides at-least-once delivery — jobs can be reprocessed after retries or crashes. Second, for CPU-intensive work like PDF generation, I use sandboxed processors to isolate the work in a child process and prevent blocking the event loop. Third, I always implement graceful shutdown in workers so deploys don't interrupt running jobs. Fourth, Bull Board is essential for observability in production — it lets me inspect queues, retry failed jobs, and debug issues without digging through logs.
>
> I choose BullMQ over Kafka or RabbitMQ when the system is Node.js only and I'm doing task processing. For event streaming across multiple services or languages, or when I need replay capability, I use Kafka. For complex routing, RabbitMQ. BullMQ shines in the Node.js + Redis sweet spot."

### Frases úteis em entrevista

- "BullMQ is my default for background jobs in Node.js because it uses Redis which is often already available."
- "The API publishes jobs and responds immediately; workers process asynchronously."
- "Workers must be idempotent — BullMQ guarantees at-least-once delivery."
- "For CPU-heavy work like PDF generation, I use sandboxed processors to avoid blocking the event loop."
- "Bull Board is essential for observability — it lets me inspect and retry jobs in production."
- "Graceful shutdown with `worker.close()` on SIGTERM prevents job interruption during deploys."
- "I use BullMQ for task processing, not for event streaming — that's Kafka's job."
- "For rate limiting external API calls, BullMQ's built-in limiter respects per-worker quotas."

### Key vocabulary

- fila de jobs → job queue
- trabalho em segundo plano → background job
- processador → processor / worker
- job atrasado → delayed job
- job recorrente → repeatable job / scheduled job
- tentativas → attempts / retries
- retrocesso exponencial → exponential backoff
- prioridade → priority
- limitador de taxa → rate limiter
- fluxo hierárquico → flow (hierarchical jobs)
- processador isolado → sandboxed processor
- desligamento gracioso → graceful shutdown
- progresso do job → job progress
- painel → dashboard
- parado (stalled) → stalled job

---

## Recursos

### Documentação

- [BullMQ Documentation](https://docs.bullmq.io/) — documentação oficial
- [BullMQ GitHub](https://github.com/taskforcesh/bullmq) — repositório
- [BullMQ API Reference](https://api.docs.bullmq.io/)

### Dashboards e ferramentas

- [Bull Board](https://github.com/felixmosh/bull-board) — dashboard mais popular
- [Taskforce.sh](https://taskforce.sh/) — dashboard comercial do criador do BullMQ
- [Arena](https://github.com/bee-queue/arena) — dashboard alternativo

### Artigos e tutorials

- [BullMQ vs Bull — guia de migração](https://docs.bullmq.io/bull/bull-3.x-migration)
- [Getting started with BullMQ and Redis](https://blog.taskforce.sh/getting-started-with-bullmq/)
- [BullMQ patterns guide](https://docs.bullmq.io/patterns/adding-bulks)

### Exemplos

- [BullMQ Examples](https://github.com/taskforcesh/bullmq-pro-examples)

---

## Veja também

- [[Mensageria]] — contexto geral, quando usar cada broker
- [[03-Dominios/Arquitetura/Mensageria/Kafka]] — alternativa para event streaming e comunicação entre serviços
- [[RabbitMQ]] — alternativa para routing complexo multi-linguagem
- [[Node.js]] — troubleshooting, patterns, ecossistema
- [[System Design]] — onde encaixar job queues em system design
- [[API Design]] — operações assíncronas via 202 Accepted + job
