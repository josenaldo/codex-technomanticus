---
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
---

# BullMQ - filas de tarefas

> [!abstract] TL;DR
> BullMQ é o sistema de filas distribuídas de referência em [[Node.js]]: construído sobre Redis, oferece producers (`Queue`), consumers (`Worker`), observação de eventos (`QueueEvents`), jobs recorrentes com cron (`repeatables`), pipelines de dependências com `FlowProducer` e UI de monitoramento com Bull Board. O ciclo de vida de um job — `waiting → active → completed | failed` — é gerenciado atomicamente via scripts Lua no Redis, garantindo durabilidade e at-least-once delivery mesmo com falha do worker. Os padrões essenciais em produção são: **retry com backoff exponencial** (evitar thundering herd), **limitar concurrency** (não afogar o banco), **removeOnComplete/removeOnFail** (evitar estouro de memória no Redis) e **graceful shutdown** (workers drenam jobs ativos antes de encerrar). Veja [[03-Dominios/Node/Integrações/index|Integrações]] para o contexto completo do galho.

## Como funciona

### Arquitetura geral

BullMQ separa responsabilidades em três entidades principais:

- **`Queue`** — o produtor. Recebe jobs, serializa como JSON e os empilha no Redis via lista ou sorted set (dependendo do delay/priority). Não processa nada sozinho.
- **`Worker`** — o consumidor. Faz polling bloqueante no Redis (`BRPOPLPUSH` internamente), pega um job, executa o processador e registra o resultado. Pode rodar em processos ou máquinas separadas.
- **`QueueEvents`** — o observador. Subscreve em streams Redis para emitir eventos de ciclo de vida (`completed`, `failed`, `progress`, `stalled`). Útil para logging centralizado e métricas sem poluir o código do worker.

A camada de persistência é 100% Redis. Não há banco de dados SQL envolvido. Todos os estados de job são armazenados em chaves Redis com prefixo `bull:<queue-name>:`.

### Ciclo de vida do job

```
[add()]  →  waiting  →  active  →  completed
                                ↘  failed  →  (retry ou dead-letter)
```

1. **waiting** — job foi adicionado via `queue.add()`. Fica em uma lista Redis aguardando worker disponível.
2. **active** — worker pegou o job e começou a processar. O job é movido atomicamente para um sorted set de jobs ativos.
3. **completed** — processador retornou sem erro. Job é movido para sorted set de completados (ou removido se `removeOnComplete: true`).
4. **failed** — processador lançou exceção. BullMQ verifica as tentativas restantes (`attempts`). Se ainda há tentativas, reagenda com backoff. Se esgotou, move para o sorted set de falhas.

A movimentação entre estados é feita via scripts Lua atômicos diretamente no Redis — não há race condition entre múltiplos workers.

### Stalled jobs

Se um worker morre enquanto processa um job (crash, OOM, SIGKILL), o job fica "travado" em `active`. BullMQ tem um mecanismo de stall check: periodicamente verifica jobs em `active` que não atualizaram seu heartbeat e os move de volta para `waiting`. O intervalo é configurável via `stalledInterval`.

### Retry com backoff

BullMQ suporta dois tipos de backoff:

- **`fixed`** — espera sempre o mesmo intervalo (ex: 5s entre cada tentativa).
- **`exponential`** — dobra o intervalo a cada tentativa (ex: 1s, 2s, 4s, 8s...). Essencial para evitar thundering herd quando um serviço dependente cai.

## Snippet 1 — Criando fila e adicionando jobs

```typescript
import { Queue } from 'bullmq'
import IORedis from 'ioredis'

const connection = new IORedis(process.env.REDIS_URL, {
  maxRetriesPerRequest: null, // obrigatório para BullMQ
})

const emailQueue = new Queue('email-notifications', { connection })

// Adicionar um job com opções
await emailQueue.add(
  'send-welcome',
  {
    to: 'user@example.com',
    template: 'welcome',
    userId: 'u_123',
  },
  {
    attempts: 3,                         // máximo de tentativas
    backoff: {
      type: 'exponential',
      delay: 1000,                       // 1s, 2s, 4s...
    },
    delay: 5000,                         // aguardar 5s antes de processar
    priority: 1,                         // menor número = maior prioridade
    removeOnComplete: { count: 100 },    // manter apenas os últimos 100 completados
    removeOnFail: { count: 500 },        // manter últimos 500 falhos para diagnóstico
  }
)

// Adicionar múltiplos jobs de uma vez (bulk — muito mais eficiente que loop)
await emailQueue.addBulk([
  {
    name: 'send-promo',
    data: { to: 'a@example.com', template: 'promo' },
    opts: { attempts: 2, removeOnComplete: true },
  },
  {
    name: 'send-promo',
    data: { to: 'b@example.com', template: 'promo' },
    opts: { attempts: 2, removeOnComplete: true },
  },
])

// Fechar quando não precisar mais da fila no processo produtor
await emailQueue.close()
```

> [!warning] `maxRetriesPerRequest: null` é obrigatório
> BullMQ usa comandos bloqueantes do Redis (como `BLMOVE`). O ioredis rejeita comandos bloqueantes por padrão após N retries. Definir `maxRetriesPerRequest: null` desativa esse limite — sem isso, o worker falha silenciosamente.

## Snippet 2 — Worker com concurrency e progresso

```typescript
import { Worker, Job } from 'bullmq'
import IORedis from 'ioredis'

const connection = new IORedis(process.env.REDIS_URL, {
  maxRetriesPerRequest: null,
})

const worker = new Worker(
  'email-notifications',
  async (job: Job) => {
    // job.name: nome do job ('send-welcome', 'send-promo'...)
    // job.data: payload serializado
    // job.id: ID único gerado pelo BullMQ
    // job.attemptsMade: número de tentativas já realizadas

    await job.updateProgress(10)  // 10% concluído

    try {
      await sendEmail(job.data.to, job.data.template)
      await job.updateProgress(100)

      // Valor retornado fica em job.returnvalue após completed
      return { sent: true, timestamp: Date.now() }
    } catch (err) {
      // Lançar aqui marca o job como failed e dispara retry se configurado
      throw err
    }
  },
  {
    connection,
    concurrency: 5,          // processar até 5 jobs em paralelo por worker
    limiter: {
      max: 100,              // throttle global: máx 100 jobs por duration
      duration: 60_000,      // janela de 1 minuto
    },
  }
)

// Eventos locais do worker (apenas jobs processados por ESTE worker)
worker.on('completed', (job) => {
  console.log(`Job ${job.id} concluído:`, job.returnvalue)
})

worker.on('failed', (job, err) => {
  console.error(`Job ${job?.id} falhou (tentativa ${job?.attemptsMade}):`, err.message)
})

// Graceful shutdown: aguarda jobs ativos terminarem antes de fechar
async function shutdown() {
  await worker.close()  // para de pegar novos jobs e drena os ativos
  await connection.quit()
  process.exit(0)
}

process.on('SIGTERM', shutdown)
process.on('SIGINT', shutdown)
```

## Snippet 3 — Job repeatable com cron

```typescript
import { Queue } from 'bullmq'
import IORedis from 'ioredis'

const connection = new IORedis(process.env.REDIS_URL, {
  maxRetriesPerRequest: null,
})

const reportQueue = new Queue('reports', { connection })

// Job que roda todo dia às 6h UTC
await reportQueue.add(
  'daily-summary',
  { type: 'daily', recipients: ['team@example.com'] },
  {
    repeat: {
      pattern: '0 6 * * *',   // cron expression padrão
      tz: 'America/Sao_Paulo', // timezone explícito (recomendado)
    },
    removeOnComplete: { age: 86400 },  // remover completados após 24h
    removeOnFail: { count: 10 },
  }
)

// Listar todos os repeatables configurados na fila
const repeatables = await reportQueue.getRepeatableJobs()
console.log(repeatables)

// Remover um repeatable (usar o key retornado por getRepeatableJobs)
// await reportQueue.removeRepeatableByKey(repeatables[0].key)

await reportQueue.close()
```

> [!warning] Repeatables sobrevivem ao processo
> O job repeatable fica registrado no Redis, não no código. Se você alterar a cron expression no código mas não remover o repeatable antigo, ambos vão coexistir e rodar em paralelo. Sempre faça `removeRepeatableByKey` antes de adicionar uma nova versão do repeatable.

## Snippet 4 — FlowProducer para pipeline de jobs

```typescript
import { FlowProducer } from 'bullmq'
import IORedis from 'ioredis'

const connection = new IORedis(process.env.REDIS_URL, {
  maxRetriesPerRequest: null,
})

const flow = new FlowProducer({ connection })

// Pipeline: processar pedido → enviar email + gerar nota fiscal (em paralelo)
// O job pai só executa após TODOS os filhos completarem
const tree = await flow.add({
  name: 'process-order',        // job PAI (executa por último)
  queueName: 'orders',
  data: { orderId: 'ord_456' },
  children: [
    {
      name: 'send-confirmation-email',  // filho 1
      queueName: 'email-notifications',
      data: { orderId: 'ord_456', template: 'order-confirm' },
    },
    {
      name: 'generate-invoice',          // filho 2
      queueName: 'invoices',
      data: { orderId: 'ord_456', format: 'pdf' },
    },
  ],
})

console.log('Flow criado. Job pai ID:', tree.job.id)

// Cada filho pode ter seus próprios filhos (árvore arbitrariamente profunda)
// O pai recebe os returnvalues dos filhos via job.getChildrenValues()

await flow.close()
```

> [!warning] FlowProducer requer workers para TODAS as filas
> Se um filho rodar em uma fila sem worker, o job pai nunca sai do estado `waiting-children` — sem timeout, sem aviso. Garanta que todos os `queueName` referenciados nos filhos tenham workers ativos.

## Snippet 5 — QueueEvents para observação em produção

```typescript
import { QueueEvents } from 'bullmq'
import IORedis from 'ioredis'

const connection = new IORedis(process.env.REDIS_URL, {
  maxRetriesPerRequest: null,
})

// QueueEvents usa um client Redis separado (modo subscribe)
const queueEvents = new QueueEvents('email-notifications', { connection })

// Observar completados (de QUALQUER worker, não só o local)
queueEvents.on('completed', ({ jobId, returnvalue }) => {
  console.log(`[QueueEvents] Job ${jobId} completado:`, JSON.parse(returnvalue))
})

// Observar falhas
queueEvents.on('failed', ({ jobId, failedReason }) => {
  console.error(`[QueueEvents] Job ${jobId} falhou: ${failedReason}`)
  // Aqui: enviar alerta, incrementar métrica Prometheus, etc.
})

// Observar progresso (útil para websockets de acompanhamento)
queueEvents.on('progress', ({ jobId, data }) => {
  console.log(`[QueueEvents] Job ${jobId} progresso: ${JSON.stringify(data)}`)
  // ex: emitir via Socket.io para o cliente que aguarda
})

// Observar jobs que ficaram stalled
queueEvents.on('stalled', ({ jobId }) => {
  console.warn(`[QueueEvents] Job ${jobId} travou (worker morreu?)`)
})

// Aguardar um job específico com timeout (útil em testes ou APIs síncronas)
// const result = await queueEvents.waitUntilFinished(job, 30_000)

// Fechar quando o processo terminar
process.on('SIGTERM', async () => {
  await queueEvents.close()
  await connection.quit()
})
```

## Armadilhas

> [!danger] Esquecer `removeOnComplete` e `removeOnFail`
> Por padrão, BullMQ mantém **todos** os jobs completados e falhos no Redis indefinidamente. Em filas de alto volume, isso consome memória Redis progressivamente até causar OOM ou degradação severa de performance. Sempre defina `removeOnComplete` e `removeOnFail` na criação do job ou como default na Queue.
>
> ```typescript
> // Configurar defaults na Queue (vale para todos os jobs)
> const queue = new Queue('minha-fila', {
>   connection,
>   defaultJobOptions: {
>     removeOnComplete: { count: 1000, age: 3600 },
>     removeOnFail: { count: 5000 },
>   },
> })
> ```

> [!danger] Workers sem graceful shutdown causam jobs travados em "active"
> Se o processo for morto com `SIGKILL` (ou encerrado sem chamar `worker.close()`), o job fica em estado `active` até o stall check detectar que o heartbeat parou. Durante esse tempo, nenhum outro worker pega o job. O stall check padrão roda a cada 30s. Em filas críticas, isso causa atraso perceptível. Sempre registre handlers para `SIGTERM` e `SIGINT` e chame `worker.close()`.

> [!warning] Concurrency ilimitada afoga recursos compartilhados
> `concurrency` padrão do Worker é 1. Aumentar sem critério (ex: `concurrency: 100`) pode saturar o pool do banco de dados, o Redis ou APIs externas chamadas dentro do processador. Calcule a concurrency em função dos recursos disponíveis: `concurrency ≤ pool_size / workers_count`.

> [!warning] `Queue.add()` em loop sem `addBulk` é ineficiente
> Cada `queue.add()` é uma round-trip ao Redis. Um loop com 1.000 `add()` faz 1.000 round-trips. Use `queue.addBulk()` para adicionar múltiplos jobs em uma única operação — reduz latência e sobrecarga de rede significativamente.

> [!warning] Repeatables duplicados ao alterar cron expression
> Mudar a cron expression no código sem remover o repeatable antigo cria **dois** repeatables coexistentes na fila. O Redis não detecta duplicação por nome — a chave inclui o cron pattern. Remova o antigo com `removeRepeatableByKey` antes de adicionar o novo.

## Comparativo: BullMQ vs alternativas

| Critério | BullMQ | Agenda | BeeQueue | Kafka |
|---|---|---|---|---|
| **Caso de uso primário** | Filas de jobs com retry, workflows | Jobs agendados (cron-like) | Filas simples de alto throughput | Streaming de eventos distribuído |
| **Throughput** | Alto (Redis Lua scripts) | Médio (MongoDB polling) | Muito alto (minimalista) | Extremamente alto (partições) |
| **Dependências** | Redis | MongoDB | Redis | Kafka + ZooKeeper/KRaft |
| **DX / Funcionalidades** | Excelente: retry, FlowProducer, UI, cron | Boa: foco em scheduling | Simples: sem retry avançado | Complexa: offsets, consumer groups |
| **Persistência após restart** | Sim (Redis) | Sim (MongoDB) | Sim (Redis) | Sim (log distribuído) |
| **Ordenação global** | Não (por queue) | Não | Não | Sim (por partição) |
| **Replay de eventos** | Não | Não | Não | Sim (retention configurável) |
| **Quando escolher** | Jobs de background com retry/cron | Apps já com MongoDB | Throughput máximo simples | Event sourcing, log de auditoria |

**Resumo decisório:**
- Use **BullMQ** quando precisar de retry inteligente, jobs recorrentes, pipelines de dependências ou monitoramento via UI.
- Use **Kafka** quando precisar de replay de eventos, múltiplos consumers independentes (consumer groups) ou throughput acima de 100k msgs/s.
- Use **BeeQueue** apenas se a simplicidade e throughput forem mais importantes que funcionalidades avançadas.
- Evite **Agenda** em projetos novos sem MongoDB já no stack — o polling em MongoDB é menos eficiente que Redis para filas.

## Em entrevista

### "How do you guarantee at-least-once delivery in BullMQ?"

BullMQ guarantees at-least-once delivery through a combination of Redis atomic operations and a stall detection mechanism. When a worker picks up a job, BullMQ moves it from the `waiting` state to `active` using a Lua script that runs atomically on the Redis server — no other worker can pick the same job simultaneously. The worker must then continuously renew a heartbeat (a Redis key with a short TTL) while processing the job; if the worker crashes or becomes unresponsive, the heartbeat expires and the stall checker moves the job back to `waiting` on the next interval. This means the job will be retried even if the original worker died mid-execution, ensuring at-least-once semantics at the cost of possible duplicate processing, which your job processor must be designed to handle idempotently.

### "What's your strategy for handling retries and dead-letter queues in BullMQ?"

My retry strategy always starts with exponential backoff — I configure `backoff: { type: 'exponential', delay: 1000 }` combined with a reasonable `attempts` count (typically 3 to 5) to avoid hammering a failing downstream service. For the dead-letter queue pattern, BullMQ doesn't have a built-in DLQ concept, so I implement it explicitly: I listen to the `failed` event on `QueueEvents`, and when `job.attemptsMade >= job.opts.attempts`, I move the job data to a dedicated `<queue-name>-failed` queue using `queue.add()` with the original payload and a flag indicating it's a dead-letter job. This separate queue can then be monitored via Bull Board or consumed by a separate worker that sends alerts or stores the failure in a database for manual review. I also ensure `removeOnFail` is set to retain a reasonable count of failed jobs so they remain inspectable without causing Redis memory issues.

### "When would you choose BullMQ over Kafka for async processing?"

The decision comes down to job semantics versus event semantics. I choose BullMQ when I need task-oriented processing — sending an email, resizing an image, generating a report — where each unit of work has a clear lifecycle (retry, completion, result) and I need features like priority queues, scheduled jobs, FlowProducer pipelines, and a monitoring UI out of the box. BullMQ is also significantly simpler to operate since it only requires Redis, which most Node.js stacks already have. I choose Kafka when I need event streaming semantics: replay of past events, multiple independent consumer groups reading the same topic at their own pace, strict ordering within a partition, or retention of the event log for audit purposes. A practical rule I follow is that if a product manager would say "process this task," BullMQ fits; if they say "record this event and let multiple systems react to it," Kafka fits. Mixing both is also valid — BullMQ for task execution triggered by Kafka events, for example.

## Vocabulário

| Termo | Definição |
|---|---|
| **job** | Unidade atômica de trabalho na fila. Contém `name`, `data` (payload), `opts` (opções de retry, delay, priority) e `id` gerado pelo BullMQ. É serializado como JSON e persistido no Redis. |
| **queue** | Canal nomeado de comunicação entre producers e workers. Não processa jobs — apenas armazena e organiza. Representado pela classe `Queue` do BullMQ. |
| **worker** | Processo consumidor que pega jobs da fila, executa o processador e registra o resultado. Pode ter múltiplas instâncias em paralelo (scaling horizontal). Representado pela classe `Worker`. |
| **repeatable** | Job configurado para rodar periodicamente via cron expression ou intervalo fixo. Registrado no Redis como um template — a cada disparo, um novo job concreto é criado na fila. |
| **FlowProducer** | Classe que permite criar árvores de jobs com dependências: jobs filhos são processados primeiro e o job pai só executa quando todos os filhos completam. Ideal para pipelines de ETL ou orquestração de tarefas. |
| **dead-letter queue (DLQ)** | Fila separada onde jobs que esgotaram todas as tentativas de retry são movidos para inspeção manual ou reprocessamento futuro. BullMQ não implementa DLQ nativamente — requer implementação via `QueueEvents` + `queue.add()`. |
| **backoff** | Estratégia de espera entre tentativas de retry. `fixed` mantém intervalo constante; `exponential` dobra o intervalo a cada tentativa, reduzindo a pressão em serviços downstream que estão falhando. |
| **concurrency** | Número máximo de jobs que um Worker pode processar simultaneamente. Padrão é 1 (serial). Aumentar melhora throughput mas aumenta consumo de recursos (conexões de banco, memória, CPU). |
| **BRPOPLPUSH** | Comando Redis bloqueante que remove um elemento do final de uma lista e insere no início de outra, atomicamente. Base do mecanismo de dequeue do BullMQ (versões anteriores; BullMQ v3+ usa `LMOVE`). |
| **removeOnComplete** | Opção de job que controla quantos jobs completados são mantidos no Redis. Aceita `boolean`, `number` (count) ou `{ count, age }`. Essencial para controlar uso de memória em filas de alto volume. |

## Veja também

- [[03-Dominios/Node/Integrações/02 - Redis e ioredis]] — BullMQ usa Redis como backend; entender ioredis e estruturas de dados Redis facilita o diagnóstico de problemas de memória e performance em filas
- [[03-Dominios/Node/Integrações/04 - Kafka com kafkajs]] — alternativa para cenários de event streaming; comparativo direto na tabela acima
- [[03-Dominios/Node/Integrações/09 - Padrões de resiliência - retry, circuit breaker e bulkhead]] — backoff exponencial e circuit breaker complementam a estratégia de retry do BullMQ em chamadas a serviços externos dentro do worker
- [[03-Dominios/Node/Integrações/index|Integrações]] — índice do galho 9
- [[Node.js]] — tronco da trilha Node Senior
