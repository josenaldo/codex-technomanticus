---
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
---

# Kafka com kafkajs

> [!abstract] TL;DR
> **kafkajs** é o cliente Kafka mais adotado em [[Node.js]]: escrito em TypeScript puro, sem dependências nativas, oferece `Producer` com `acks: -1` e `idempotent: true` para entrega exactly-once, `Consumer` com consumer groups e commit manual de offset para controle preciso de at-least-once, processamento em lote via `eachBatch` com suporte a `heartbeat()`, e `Admin` client para criação de tópicos e monitoramento de lag. Kafka se diferencia de filas tradicionais por ser um **log distribuído e persistente**: mensagens ficam no tópico por tempo configurável (padrão 7 dias), múltiplos consumer groups podem ler o mesmo tópico independentemente, e cada partição garante ordenação total. Schema Registry com Avro ou JSON Schema protege contratos entre producers e consumers em times grandes. Veja [[03-Dominios/Node/Integrações/index|Integrações]] para o contexto completo do galho.

## Como funciona

### Arquitetura geral

Kafka organiza dados em **tópicos** (topics), cada tópico dividido em **partições** (partitions). Cada partição é um log append-only imutável, com cada mensagem identificada por um **offset** crescente.

```
Topic: pedidos
├── Partition 0: [offset 0] [offset 1] [offset 2] ...
├── Partition 1: [offset 0] [offset 1] ...
└── Partition 2: [offset 0] ...
```

O kafkajs expõe três entidades principais:

- **`Kafka`** — cliente raiz. Contém configuração de brokers, autenticação SSL/SASL e configurações de retry. É a factory para `Producer`, `Consumer` e `Admin`.
- **`Producer`** — publica mensagens em tópicos. Pode ser configurado com `acks` (controle de durabilidade), `idempotent` (evita duplicatas por retry) e `transactionalId` (exactly-once end-to-end).
- **`Consumer`** — subscreve tópicos dentro de um **consumer group**. O broker distribui as partições entre os consumers do mesmo grupo (cada partição é processada por exatamente um consumer por vez). Commits de offset controlam o progresso.
- **`Admin`** — gerencia o cluster: cria/deleta tópicos, inspeciona consumer groups, verifica lag.

### Partições e consumer groups

O par partição/consumer group é o mecanismo de escalabilidade horizontal do Kafka:

- **1 partição → 1 consumer ativo** por consumer group em um dado momento.
- Para aumentar paralelismo, aumente o número de partições e de instâncias do consumer.
- Partições a mais que consumers ficam em espera — se um consumer cai, o broker redistribui suas partições (**rebalancing**).
- Dois consumer groups no mesmo tópico processam mensagens de forma totalmente independente — ideal para fanout (ex.: um grupo para analytics e outro para notificações no mesmo tópico de pedidos).

### Offset management

Cada consumer group mantém um **offset** por partição — a posição da próxima mensagem a ser consumida. Há dois modos:

| Modo | Comportamento | Risco |
|---|---|---|
| `autoCommit: true` | Commit automático a cada `autoCommitInterval` ms | Mensagem processada com erro pode ser perdida se o commit já ocorreu |
| `autoCommit: false` | Commit manual via `resolveOffset` + `commitOffsetsIfNecessary` | Controle total; requer disciplina no código |

Em produção, **sempre use `autoCommit: false`** quando o processamento pode falhar e você não quer perder mensagens.

### `eachMessage` vs `eachBatch`

| Característica | `eachMessage` | `eachBatch` |
|---|---|---|
| Granularidade | Uma mensagem por vez | Lote inteiro por vez |
| Heartbeat | Automático | Manual (chame `heartbeat()` periodicamente) |
| Throughput | Menor | Maior |
| Complexidade | Baixa | Média |
| Uso ideal | Processamentos lentos ou com efeitos colaterais | Pipelines de alto throughput, batch inserts |

---

## Snippet 1 — Producer com `acks: -1` e `idempotent: true`

```typescript
import { Kafka, CompressionTypes, logLevel } from 'kafkajs';

const kafka = new Kafka({
  clientId: 'meu-servico',
  brokers: ['kafka-broker-1:9092', 'kafka-broker-2:9092'],
  logLevel: logLevel.WARN,
});

const producer = kafka.producer({
  // acks: -1 (all) — broker só confirma após todas as réplicas in-sync receberem
  // Mais lento, mas garante zero perda de mensagem em crash de broker
  acks: -1,
  // idempotent: true — atribui sequence number a cada mensagem
  // Kafka descarta duplicatas causadas por retry automático
  idempotent: true,
  // retry aggressivo para produtores idempotentes
  retry: {
    initialRetryTime: 300,
    retries: 5,
  },
});

async function publicarPedido(pedido: { id: string; valor: number }) {
  await producer.connect();

  await producer.send({
    topic: 'pedidos',
    compression: CompressionTypes.GZIP,
    messages: [
      {
        // key define a partição — mesma key sempre vai para mesma partição
        // garante ordenação por entidade (todos os eventos do pedido X na mesma partição)
        key: pedido.id,
        value: JSON.stringify(pedido),
        headers: {
          'content-type': 'application/json',
          'source-service': 'api-pedidos',
        },
      },
    ],
  });

  console.log(`Pedido ${pedido.id} publicado`);
}

// Sempre desconecte o producer ao finalizar
// (ver Snippet 5 para graceful shutdown)
```

---

## Snippet 2 — Consumer com `groupId`, `eachMessage` e commit manual de offset

```typescript
import { Kafka, EachMessagePayload } from 'kafkajs';

const kafka = new Kafka({
  clientId: 'processador-pedidos',
  brokers: ['kafka-broker-1:9092'],
});

const consumer = kafka.consumer({
  groupId: 'grupo-processador-pedidos',
  // Sem autoCommit — controle total sobre o offset
  // Evita perda silenciosa de mensagens em caso de erro no processamento
  sessionTimeout: 30000,   // ms — quanto tempo sem heartbeat antes de rebalance
  heartbeatInterval: 3000, // ms — frequência do heartbeat enviado ao broker
});

async function iniciarConsumer() {
  await consumer.connect();
  await consumer.subscribe({
    topic: 'pedidos',
    // fromBeginning: true relê todo o tópico desde o início
    // Use apenas em desenvolvimento ou reset intencional
    fromBeginning: false,
  });

  await consumer.run({
    autoCommit: false, // commit manual — nunca perca uma mensagem em erro

    eachMessage: async ({ topic, partition, message, heartbeat }: EachMessagePayload) => {
      const offset = message.offset;
      const valor = message.value?.toString();

      if (!valor) {
        // Mensagem vazia — commit e pule (não reprocesse lixo indefinidamente)
        await consumer.commitOffsets([{ topic, partition, offset: String(Number(offset) + 1) }]);
        return;
      }

      try {
        const pedido = JSON.parse(valor);
        await processarPedido(pedido);

        // Commit APÓS processamento bem-sucedido
        // offset + 1 indica "próxima mensagem a consumir"
        await consumer.commitOffsets([
          { topic, partition, offset: String(Number(offset) + 1) },
        ]);
      } catch (err) {
        // Em caso de erro: NÃO faça commit
        // A mensagem será reprocessada após rebalance ou restart do consumer
        console.error(`Erro ao processar offset ${offset} na partição ${partition}:`, err);
        // Considere enviar para dead-letter topic após N falhas
        throw err; // interrompe o processamento do batch atual
      }
    },
  });
}

async function processarPedido(pedido: { id: string; valor: number }) {
  // lógica de negócio aqui
  console.log(`Processando pedido ${pedido.id} — valor: ${pedido.valor}`);
}
```

---

## Snippet 3 — `eachBatch` para processamento em lote com `heartbeat()`

```typescript
import { Kafka, EachBatchPayload } from 'kafkajs';

const kafka = new Kafka({
  clientId: 'batch-analytics',
  brokers: ['kafka-broker-1:9092'],
});

const consumer = kafka.consumer({
  groupId: 'grupo-analytics',
  // maxBytesPerPartition: limita o tamanho de cada batch por partição
  maxBytesPerPartition: 1_048_576, // 1 MB
});

await consumer.connect();
await consumer.subscribe({ topic: 'pedidos', fromBeginning: false });

await consumer.run({
  autoCommit: false,
  // eachBatch expõe o lote inteiro — ideal para bulk inserts em banco
  eachBatch: async ({
    batch,
    resolveOffset,
    heartbeat,
    commitOffsetsIfNecessary,
    isRunning,
    isStale,
  }: EachBatchPayload) => {
    const registros: object[] = [];

    for (const message of batch.messages) {
      // Interrompa se o consumer foi parado ou o batch ficou obsoleto (rebalance)
      if (!isRunning() || isStale()) break;

      const valor = message.value?.toString();
      if (valor) {
        registros.push(JSON.parse(valor));
      }

      // Marque o offset como processado (mas ainda não comitado)
      resolveOffset(message.offset);

      // Chame heartbeat() a cada ~100 mensagens para evitar timeout de sessão
      // Processamentos longos sem heartbeat causam rebalance indesejado
      if (registros.length % 100 === 0) {
        await heartbeat();
      }
    }

    // Bulk insert — muito mais eficiente que inserir um a um
    if (registros.length > 0) {
      await salvarRegistrosEmLote(registros);
    }

    // Commita todos os offsets resolvidos acima de uma vez
    await commitOffsetsIfNecessary();
  },
});

async function salvarRegistrosEmLote(registros: object[]) {
  // ex.: INSERT ... VALUES (...), (...), (...) com pg
  console.log(`Salvando ${registros.length} registros em lote`);
}
```

---

## Snippet 4 — Admin client para criar tópico e verificar lag de consumer group

```typescript
import { Kafka } from 'kafkajs';

const kafka = new Kafka({
  clientId: 'admin-cli',
  brokers: ['kafka-broker-1:9092'],
});

const admin = kafka.admin();

async function configurarTopico() {
  await admin.connect();

  // Criar tópico se não existir
  await admin.createTopics({
    waitForLeaders: true,
    topics: [
      {
        topic: 'pedidos',
        numPartitions: 6,      // 6 partições = 6 consumers em paralelo no máximo
        replicationFactor: 3,  // 3 réplicas — tolera falha de 2 brokers
        configEntries: [
          { name: 'retention.ms', value: String(7 * 24 * 60 * 60 * 1000) }, // 7 dias
          { name: 'compression.type', value: 'gzip' },
        ],
      },
    ],
  });
  console.log('Tópico "pedidos" criado (ou já existia)');

  // Verificar lag do consumer group
  const offsets = await admin.fetchTopicOffsets('pedidos');
  const groupOffsets = await admin.fetchOffsets({
    groupId: 'grupo-processador-pedidos',
    topics: ['pedidos'],
  });

  console.log('\n--- Lag por partição ---');
  for (const partitionOffset of offsets) {
    const partition = partitionOffset.partition;
    const highWatermark = Number(partitionOffset.high);

    const groupPartition = groupOffsets[0]?.partitions.find(
      (p) => p.partition === partition
    );
    const committedOffset = Number(groupPartition?.offset ?? 0);
    const lag = highWatermark - committedOffset;

    console.log(`  Partição ${partition}: lag = ${lag} mensagens`);
  }

  await admin.disconnect();
}

configurarTopico().catch(console.error);
```

---

## Snippet 5 — Graceful shutdown com `producer.disconnect()` e `consumer.disconnect()`

```typescript
import { Kafka, Producer, Consumer } from 'kafkajs';

const kafka = new Kafka({
  clientId: 'api-pedidos',
  brokers: ['kafka-broker-1:9092'],
});

const producer: Producer = kafka.producer({ idempotent: true, acks: -1 });
const consumer: Consumer = kafka.consumer({ groupId: 'grupo-pedidos' });

async function iniciar() {
  await producer.connect();
  await consumer.connect();
  await consumer.subscribe({ topic: 'pedidos' });
  await consumer.run({
    autoCommit: false,
    eachMessage: async ({ message }) => {
      console.log('Mensagem recebida:', message.value?.toString());
    },
  });
  console.log('Kafka producer e consumer conectados');
}

// Graceful shutdown — chamado em SIGTERM (ex.: kubectl stop, PM2 restart)
async function encerrar(sinal: string) {
  console.log(`Sinal ${sinal} recebido — iniciando shutdown...`);

  // 1. Pause o consumer — para de receber novas mensagens
  consumer.pause([{ topic: 'pedidos' }]);

  // 2. Aguarde um ciclo de event loop — deixe mensagens em andamento terminarem
  await new Promise((resolve) => setTimeout(resolve, 1000));

  // 3. Desconecte consumer e producer — libera conexões no broker
  // A ORDEM IMPORTA: desconecte consumer antes de producer
  await consumer.disconnect();
  await producer.disconnect();

  console.log('Shutdown concluído — conexões Kafka encerradas');
  process.exit(0);
}

// Registre handlers para os sinais de encerramento
process.on('SIGTERM', () => encerrar('SIGTERM'));
process.on('SIGINT', () => encerrar('SIGINT'));

iniciar().catch((err) => {
  console.error('Erro ao iniciar Kafka:', err);
  process.exit(1);
});
```

---

## Armadilhas

> [!danger] Não chamar `heartbeat()` em processamentos longos
> Sem chamadas periódicas a `heartbeat()` durante o processamento de um batch (`eachBatch`), o broker interpreta o consumer como morto após `sessionTimeout` (padrão: 30 s) e dispara um **rebalance**. Resultado: o batch em andamento é abandonado, as mensagens são redistribuídas para outro consumer, e você processa as mesmas mensagens duas vezes. Regra: chame `heartbeat()` a cada 50–100 mensagens ou sempre que o processamento individual puder levar mais de `heartbeatInterval` (padrão: 3 s).

> [!danger] Commit automático em caso de erro
> Com `autoCommit: true`, o offset é comitado periodicamente, independente do resultado do processamento. Se o seu handler lançou exceção depois do commit automático, a mensagem foi considerada consumida — **você a perdeu**. Em sistemas financeiros, de pedidos ou qualquer contexto onde perda é inaceitável, use sempre `autoCommit: false` e só comite após garantir que o efeito colateral (escrita no banco, chamada de API) foi bem-sucedido.

> [!danger] Não tratar o erro `REBALANCING`
> Durante um rebalance, o broker pode retornar um erro `REBALANCING` ao tentar fazer commit de offset. Se o seu código não captura esse erro especificamente, ele pode crashar ou — pior — tentar comitar em uma partição que não pertence mais a esse consumer. Use `isStale()` em `eachBatch` e capture `KafkaJSNonRetriableError` para tratar rebalances graciosamente.

> [!warning] `autoCommit: true` em contextos que exigem exactly-once
> Exactly-once semântica exige commit de offset **atômico** com o efeito colateral (ex.: gravação no banco). Com `autoCommit: true`, os commits são desacoplados do processamento. Para exactly-once real, use transações Kafka com `transactionalId` + `readUncommitted: false`, ou o padrão **transactional outbox** com um banco SQL.

> [!warning] Usar `autoCommit: true` com `eachBatch`
> Ao usar `eachBatch`, o kafkajs desabilita automaticamente o autoCommit interno e exige chamadas manuais a `resolveOffset` + `commitOffsetsIfNecessary`. Forçar `autoCommit: true` nesse contexto causa comportamento indefinido — alguns offsets podem ser comitados antes de `resolveOffset` ser chamado, perdendo mensagens.

> [!warning] Esquecer `disconnect()` no shutdown
> Sair do processo sem desconectar o producer/consumer deixa sessões abertas no broker. O broker só percebe o abandono após `sessionTimeout`, disparando um rebalance desnecessário que impacta todos os consumers do grupo. Em ambientes Kubernetes com rolling updates frequentes, isso causa ondas de rebalance que degradam o throughput. Sempre registre handlers para `SIGTERM` e `SIGINT`.

---

## Comparativo: Kafka vs Redis Streams vs BullMQ

| Critério | **Kafka** (kafkajs) | **Redis Streams** (ioredis) | **BullMQ** (bullmq) |
|---|---|---|---|
| **Throughput** | Muito alto (milhões msgs/s por partição) | Alto (centenas de mil/s) | Médio (dezenas de mil/s) |
| **Ordenação** | Por partição (total dentro da partição) | Por stream (global) | Por fila (FIFO ou priority) |
| **Replay de mensagens** | Sim — rewind por offset, até retenção expirar | Sim — por ID de mensagem | Não — job é removido após completado |
| **Consumer groups** | Nativo — partições distribuídas automaticamente | Nativo via `XREADGROUP` | Nativo via `Worker` com `concurrency` |
| **Persistência** | Log persistente em disco (retenção configurável) | Limitada pela memória Redis (+ AOF/RDB) | Ephemeral em Redis — pode perder em crash |
| **Exatly-once** | Sim (com transações Kafka) | Não nativo | Não nativo |
| **Schema / contrato** | Schema Registry (Avro, JSON Schema, Protobuf) | Não nativo | Não nativo |
| **DX (Developer XP)** | Média — mais configuração, conceitos específicos | Baixa — API verbosa, menos abstrações | Alta — API limpa, UI (Bull Board), TypeScript |
| **Quando usar** | Event streaming, auditoria, fanout multi-sistema, alto volume | Pub/sub simples, filas leves dentro do mesmo stack Redis | Jobs de background, retries com backoff, agendamento |

---

## Em entrevista

### What's the difference between at-least-once and exactly-once semantics in Kafka?

At-least-once delivery means a message will be processed **one or more times** — the system guarantees no message is lost, but duplicates are possible. This happens when a consumer processes a message successfully but crashes before committing the offset, causing the broker to redeliver the message after a rebalance. At-least-once is the default behavior with `autoCommit: false` and no transactional producer. To handle duplicates, consumers must be idempotent — meaning processing the same message twice produces the same result as processing it once.

Exactly-once semantics (EOS) guarantee each message is processed **precisely one time**, even in the presence of failures. In Kafka, EOS requires two components working together: an **idempotent producer** (with `idempotent: true`, which uses sequence numbers to deduplicate retries) and **transactional producers/consumers** (with `transactionalId` on the producer and `isolation.level: read_committed` on the consumer). This combination ensures that the offset commit and the downstream write happen atomically, so a crash at any point results in either both succeeding or both rolling back. EOS has a performance cost — around 10–20% lower throughput — so it's reserved for financial transactions, billing events, or any domain where duplicates cause business harm.

In practice, most Node.js microservices use at-least-once with idempotent consumers, as EOS adds significant operational complexity. The kafkajs `transactionalId` approach requires a stable producer identity across restarts, careful epoch management, and a Kafka cluster with `enable.idempotence=true` on the broker side.

---

### How does consumer group rebalancing work, and what are its implications?

A consumer group rebalance is the process by which Kafka redistributes partition ownership among the active consumers in a group. It is triggered when a consumer joins the group, a consumer leaves (graceful or crash), a new partition is added to a subscribed topic, or the group coordinator detects a consumer has missed its heartbeat deadline (`sessionTimeout`). During a rebalance, **all consumers in the group stop processing** — this is called a Stop-the-World rebalance — until the group coordinator assigns new partition ownership via the group leader.

The implications for a Node.js service are significant. Any in-flight `eachBatch` processing is interrupted — if you haven't called `resolveOffset` for the messages you processed, they will be redelivered. This is why checking `isStale()` inside `eachBatch` is essential: if the batch became stale due to a rebalance, you should abort processing immediately rather than commit offsets for a partition you no longer own. The `isRunning()` check serves a similar purpose for planned shutdowns.

Kafka introduced **incremental cooperative rebalancing** (available since kafkajs v2 via `partitionAssigners: [PartitionAssigners.roundRobin]` or cooperative sticky) to reduce the stop-the-world impact. Instead of revoking all partitions at once, only the partitions that need to move are revoked, allowing the rest to keep processing. This is the recommended approach for high-throughput consumers. To minimize rebalance frequency in production: increase `sessionTimeout` for consumers with long processing times, always call `heartbeat()` in batch loops, and use graceful shutdown (`consumer.pause` + `consumer.disconnect`) to trigger a clean rebalance rather than a crash-detected one.

---

### When would you choose Kafka over BullMQ or Redis Streams?

I'd choose Kafka when the use case requires **durable, replayable, high-throughput event streaming** with multiple independent consumers. The defining scenarios are: (1) multiple teams or services need to read the same event stream independently — Kafka's consumer group model lets you add new consumers without affecting existing ones; (2) you need to replay historical events — Kafka retains messages on disk for days or weeks, so you can rebuild a read model or debug production issues by replaying; (3) you expect sustained throughput in the hundreds of thousands to millions of messages per second — Kafka's sequential disk I/O and batch compression scale horizontally in ways Redis simply cannot.

BullMQ is the better choice for **job queues with per-job lifecycle management**: retries with exponential backoff, scheduled/delayed jobs, priority queues, and dead-letter queues. It's much simpler to operate (it's just Redis, which you probably already have), has excellent DX with Bull Board, and handles typical background job scenarios — sending emails, resizing images, running reports — without the operational overhead of a Kafka cluster. The key limitation is that BullMQ jobs are consumed once and gone; there's no replay, and no fanout to multiple independent consumers.

Redis Streams fills the middle ground: it has consumer groups and persistence (bounded by Redis memory), but lacks Kafka's horizontal scale, schema enforcement, and long-term retention. I'd use Redis Streams for lightweight pub/sub within a single team's stack, where the simplicity of staying in Redis outweighs Kafka's capabilities. The decision ultimately comes down to three questions: do you need replay? do you need multiple independent consumer groups at scale? and can you afford to operate a Kafka cluster? If all three are yes, Kafka is the right tool.

---

## Vocabulário

| Termo | Definição |
|---|---|
| **producer** | Cliente que publica mensagens em um tópico Kafka. Serializa dados (JSON, Avro, etc.) e os envia para o broker, que os persiste na partição correta com base na key da mensagem. |
| **consumer** | Cliente que lê mensagens de um ou mais tópicos. Pertence a um consumer group; cada partição é processada por exatamente um consumer do grupo em um dado momento. |
| **consumer group** | Agrupamento lógico de consumers que cooperam para processar um tópico. Cada partição é atribuída a exatamente um consumer do grupo, permitindo processamento paralelo com garantia de ordenação por partição. |
| **partition** | Unidade de paralelismo e ordenação dentro de um tópico. É um log append-only imutável; dentro de uma partição, a ordem das mensagens é estritamente garantida. Mensagens com a mesma key sempre vão para a mesma partição. |
| **offset** | Identificador numérico sequencial de uma mensagem dentro de uma partição. O consumer group mantém o offset da última mensagem processada por partição — commit de offset é o mecanismo de "checkpoint" do Kafka. |
| **lag** | Diferença entre o offset mais recente publicado em uma partição (high watermark) e o offset comitado pelo consumer group. Lag alto indica que o consumer está atrasado em relação ao producer. |
| **rebalancing** | Redistribuição de partições entre os consumers de um grupo, disparada por entrada/saída de consumers ou timeout de heartbeat. Durante o rebalance clássico (stop-the-world), todos os consumers param de processar até a nova atribuição ser estabelecida. |
| **exactly-once** | Semântica de entrega que garante que cada mensagem seja processada exatamente uma vez, mesmo em falhas. Requer produtor idempotente (`idempotent: true`) e transações Kafka (`transactionalId`), com o consumer em modo `read_committed`. |
| **idempotent producer** | Producer configurado com `idempotent: true` que usa números de sequência para permitir que o broker descarte duplicatas causadas por retries automáticos. É pré-requisito para exactly-once semantics. |
| **acks** | Configuração do producer que define quantas réplicas devem confirmar o recebimento antes do broker responder com sucesso. `acks: 0` (fire-and-forget), `acks: 1` (líder apenas), `acks: -1`/`all` (todas as réplicas in-sync — máxima durabilidade). |
| **heartbeat** | Sinal periódico enviado pelo consumer ao broker para indicar que ainda está vivo. Se o broker não recebe heartbeat dentro de `sessionTimeout`, considera o consumer morto e dispara rebalance. Em `eachBatch`, deve ser chamado manualmente para processamentos longos. |
| **schema registry** | Serviço centralizado (ex.: Confluent Schema Registry) que armazena e versiona schemas (Avro, JSON Schema, Protobuf) para tópicos Kafka. Garante compatibilidade de contratos entre producers e consumers e permite evolução segura de schemas em times distribuídos. |
