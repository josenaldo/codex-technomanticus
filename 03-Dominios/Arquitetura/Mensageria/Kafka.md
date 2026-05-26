---
title: "Kafka"
created: 2026-04-01
updated: 2026-04-10
type: concept
status: evergreen
tags:
  - arquitetura
  - mensageria
  - entrevista
publish: false
---

# Kafka

Plataforma distribuída de **event streaming** — alto throughput, persistência durável, replay, ordenação por partição, e o ecossistema mais maduro para arquiteturas event-driven. Enquanto [[Mensageria]] cobre o domínio geral (queue vs streaming, delivery semantics, comparação de brokers), esta nota é um deep dive em **Apache Kafka** especificamente.

## O que é

Apache Kafka é uma plataforma de event streaming distribuída criada pelo LinkedIn (2011) e doada para a Apache Software Foundation. É a base de facto para event-driven architecture moderna. A terminologia oficial é **"distributed event streaming platform"** — não é "só" um message broker.

**O que Kafka faz bem:**
- **Alto throughput** — milhões de mensagens/segundo em cluster moderado
- **Durabilidade** — eventos persistidos em disco com replicação
- **Retenção configurável** — de horas a infinito (compactação por key permite "infinito" semântico)
- **Replay** — consumer novo pode processar histórico inteiro
- **Ordenação por partição** — garantia forte dentro de uma partição
- **Múltiplos consumers independentes** — consumer groups lêem o mesmo tópico sem interferir

**O que Kafka NÃO faz bem (ou exige esforço):**
- Routing complexo — RabbitMQ é mais flexível
- Filas com prioridade — não tem nativamente
- Request-reply / RPC — existe, mas é forçado
- Delay de mensagens — precisa retry topics pattern
- Setup simples — requer cluster, tuning, e operação

Em entrevistas, o que diferencia um senior em Kafka:

1. **Saber explicar partições e consumer groups** — o modelo mental correto é o log imutável particionado
2. **Entender delivery semantics** — at-least-once default, exactly-once via transações
3. **Conhecer os trade-offs** — partitioning, retention, replication factor
4. **Pensar em produção** — lag, rebalance, tuning, monitoring
5. **Projetar schemas** — Schema Registry, Avro/Protobuf, evolução de schema

---

## Arquitetura

### Componentes

```
                  ┌───────────────────────────────────┐
                  │        Kafka Cluster              │
                  │                                   │
  [Producer] ───→ │  Broker 1   Broker 2   Broker 3   │ ──→ [Consumer Group A]
  [Producer] ───→ │                                   │ ──→ [Consumer Group B]
                  │  Topic "orders"                   │
                  │   Partition 0 → [Leader B1]       │
                  │                   [Replica B2]    │
                  │                   [Replica B3]    │
                  │   Partition 1 → [Leader B2]       │
                  │                   [Replica B1]    │
                  │                   [Replica B3]    │
                  │   Partition 2 → [Leader B3]       │
                  │                   [Replica B1]    │
                  │                   [Replica B2]    │
                  └───────────────────────────────────┘
                              ↑
                    [Controller / KRaft]
                    (metadata, leader election)
```

**Broker** — servidor Kafka. Um cluster tem N brokers. Cada broker armazena algumas partições (e réplicas de outras).

**Topic** — canal de mensagens. Logicamente, é uma categoria (`orders`, `payments`, `user-events`). Fisicamente, é dividido em partições.

**Partition** — unidade de paralelismo e ordenação. Cada partição é um **log imutável append-only**. Mensagens dentro de uma partição são ordenadas; entre partições não há ordem global.

**Offset** — posição de uma mensagem dentro de uma partição. Monotônico crescente. O consumer mantém seu próprio offset por partição.

**Replication** — cada partição tem `replication.factor` cópias, distribuídas em brokers diferentes. Uma é líder (handles reads/writes), as outras são followers (replicam).

**ISR (In-Sync Replicas)** — réplicas que estão atualizadas com o líder. Se o líder cai, uma ISR é promovida.

**Consumer Group** — conjunto de consumers que dividem as partições entre si. Cada partição é atribuída a **exatamente um** consumer do grupo.

**Controller** — broker especial que gerencia metadata do cluster (leader election, partition assignment). Historicamente via Zookeeper; desde Kafka 2.8+ via **KRaft** (Raft nativo, sem Zookeeper).

### O log: modelo mental fundamental

A abstração central do Kafka é o **log imutável append-only**. Entenda isso e tudo faz sentido.

```
Partition 0 (append-only log):

  offset:   0   1   2   3   4   5   6   7   8   9   10 ...
           [A] [B] [C] [D] [E] [F] [G] [H] [I] [J]  ...
            ↑                           ↑           ↑
            │                           │           │
       Consumer                    Consumer        Producer
       Group B                     Group A         (escreve aqui)
       (offset=0)                  (offset=5)
```

**Consequências deste modelo:**

1. **Writes são sequenciais** — escrita em disco é append, muito mais rápido que random write. É por isso que Kafka tem alto throughput mesmo persistindo em disco.
2. **Múltiplos consumers independentes** — cada um tem seu offset. Um não afeta o outro.
3. **Replay é trivial** — só voltar o offset.
4. **Mensagens não são "removidas"** — são descartadas por retention policy (tempo, tamanho, ou compaction).
5. **Ordem garantida dentro da partição** — por definição, já que é um log sequencial.

### Retention

Quanto tempo Kafka mantém as mensagens:

- **Time-based:** `retention.ms = 604800000` (7 dias default)
- **Size-based:** `retention.bytes = -1` (unlimited default, mas pode limitar por partição)
- **Log Compaction:** mantém apenas a **última** mensagem por key, sem limite de tempo

Quando ambos time e size são configurados, o primeiro a ser atingido dispara a limpeza.

### Log Compaction

Pattern poderoso: em vez de expirar por tempo, mantenha **sempre a última versão** de cada key.

```
Antes da compactação:
  key=user-42, value={"name": "Alice"}            offset 10
  key=user-43, value={"name": "Bob"}              offset 11
  key=user-42, value={"name": "Alice Smith"}      offset 42
  key=user-42, value={"name": "Alice Jones"}      offset 100

Depois da compactação:
  key=user-43, value={"name": "Bob"}              offset 11
  key=user-42, value={"name": "Alice Jones"}      offset 100
```

**Uso:** manter estado atual de cada entidade como um stream. Consumer novo pode reconstruir todo o estado lendo o tópico do início. É a base de **event sourcing** e **Kafka Streams** (state stores).

**Tombstone:** para "deletar" uma key, publique `(key, null)`. A compactação remove a entrada.

---

## Partições e paralelismo

Partições são **a** decisão fundamental em Kafka. Elas controlam paralelismo, ordenação e escalabilidade.

### Por que particionar

- **Paralelismo** — múltiplos consumers podem processar em paralelo (um por partição)
- **Escala horizontal** — partições distribuídas em brokers diferentes
- **Ordenação local** — mensagens com a mesma key vão para a mesma partição (ordem garantida)

### Como o producer escolhe a partição

1. **Se key é fornecida:** `partition = hash(key) % num_partitions` — determinístico, mesma key → mesma partição
2. **Se key é null:** round-robin (Kafka 2.4+ usa "sticky partitioner" para batching melhor)
3. **Partição explícita:** producer pode sobrescrever

**Consequência crítica:** o hash usa o número de partições. Se você **mudar** o número de partições, mensagens futuras com a mesma key podem ir para partições diferentes — quebra ordenação. Dimensione com folga desde o início.

### Como dimensionar partições

**Trade-offs:**

| Poucas partições | Muitas partições |
| --- | --- |
| Menos paralelismo | Mais paralelismo |
| Menos overhead (file handles, memory) | Mais overhead por broker |
| Rebalance mais rápido | Rebalance mais lento |
| Ordenação mais forte | Ordenação fragmentada |

**Regras práticas:**
- Parallelism máximo = número de partições (no consumer group, não adianta ter mais consumers que partições)
- Cada partição custa recursos no broker (Jun Rao estima ~100 partições por GB de RAM no broker)
- **Dimensione pelo paralelismo futuro esperado** — 10-20 partições é razoável para começar em um tópico médio
- Limite prático: ~4000 partições por broker, ~200k por cluster (Kafka 2.4+)

### Exemplo: calculando partições

```
Throughput esperado: 50 MB/s
Throughput por consumer: ~5 MB/s (depende da lógica)
→ Mínimo 10 consumers para acompanhar
→ Mínimo 10 partições (um por consumer)
→ Dimensionar com folga (crescimento 2-3x): 20-30 partições
```

---

## Producers

### Acks: garantia de durabilidade

```java
// acks=0: fire and forget — não espera confirmação
// Máximo throughput, mínima garantia. Pode perder mensagens.
props.put("acks", "0");

// acks=1: líder confirmou — default histórico
// Bom throughput, pode perder se líder falhar antes de replicar.
props.put("acks", "1");

// acks=all (ou -1): todas as ISRs confirmaram
// Máxima garantia, latência um pouco maior. Produção quer isso.
props.put("acks", "all");
```

**Regra:** use `acks=all` em produção. Combine com `min.insync.replicas=2` (em cluster com 3 réplicas) para garantir que a escrita sobrevive à falha de 1 broker.

### Idempotent producer

Evita duplicação em retries. O producer atribui um ID sequencial por partição; broker descarta duplicatas.

```java
props.put("enable.idempotence", "true");
// Implica acks=all, retries=MAX_INT, max.in.flight.requests.per.connection<=5
```

**Default em Kafka 3.0+.** Sempre ligado em produção.

### Batching e compression

Kafka agrupa mensagens em batches antes de enviar — throughput vem daqui.

```java
props.put("batch.size", "16384");       // bytes por batch (16KB default)
props.put("linger.ms", "10");           // espera até 10ms para encher o batch
props.put("compression.type", "snappy"); // comprime o batch (none/gzip/snappy/lz4/zstd)
```

**Trade-off:**
- `linger.ms=0` → latência mínima, batches pequenos, throughput menor
- `linger.ms=20` → latência +20ms, batches maiores, throughput maior

**Compression:** `snappy` ou `lz4` são o padrão (bom ratio, baixo CPU). `zstd` comprime mais mas gasta mais CPU.

### Transactional producer (exactly-once)

Permite atomicidade entre múltiplos sends e commits de offset.

```java
props.put("transactional.id", "my-producer-1");
producer.initTransactions();

try {
    producer.beginTransaction();
    producer.send(new ProducerRecord<>("orders", order));
    producer.send(new ProducerRecord<>("inventory", reservation));
    producer.commitTransaction();
} catch (Exception e) {
    producer.abortTransaction();
}
```

Combinado com consumer em modo `read_committed`, implementa **exactly-once semantics** (EOS) dentro do Kafka.

### Spring Kafka — producer

```java
@Configuration
public class KafkaProducerConfig {

    @Bean
    public ProducerFactory<String, OrderEvent> producerFactory() {
        Map<String, Object> config = Map.of(
            ProducerConfig.BOOTSTRAP_SERVERS_CONFIG, "kafka:9092",
            ProducerConfig.KEY_SERIALIZER_CLASS_CONFIG, StringSerializer.class,
            ProducerConfig.VALUE_SERIALIZER_CLASS_CONFIG, JsonSerializer.class,
            ProducerConfig.ACKS_CONFIG, "all",
            ProducerConfig.ENABLE_IDEMPOTENCE_CONFIG, true,
            ProducerConfig.COMPRESSION_TYPE_CONFIG, "snappy",
            ProducerConfig.LINGER_MS_CONFIG, 10
        );
        return new DefaultKafkaProducerFactory<>(config);
    }

    @Bean
    public KafkaTemplate<String, OrderEvent> kafkaTemplate() {
        return new KafkaTemplate<>(producerFactory());
    }
}

@Service
@RequiredArgsConstructor
public class OrderService {
    private final KafkaTemplate<String, OrderEvent> kafka;

    public void publish(OrderEvent event) {
        kafka.send("orders", event.getOrderId(), event)
            .whenComplete((result, ex) -> {
                if (ex != null) {
                    log.error("Failed to publish", ex);
                } else {
                    log.info("Published to partition {} offset {}",
                        result.getRecordMetadata().partition(),
                        result.getRecordMetadata().offset());
                }
            });
    }
}
```

---

## Consumers

### Consumer Groups

Múltiplos consumers se coordenam para dividir as partições de um tópico.

```
Topic "orders" (4 partições)
    partition 0 ──→ Consumer A (group=billing)
    partition 1 ──→ Consumer A (group=billing)
    partition 2 ──→ Consumer B (group=billing)
    partition 3 ──→ Consumer B (group=billing)

E simultaneamente, outro grupo lendo o mesmo tópico:
    partition 0 ──→ Consumer X (group=analytics)
    partition 1 ──→ Consumer X (group=analytics)
    partition 2 ──→ Consumer Y (group=analytics)
    partition 3 ──→ Consumer Y (group=analytics)
```

**Regras:**
- Cada partição é atribuída a **exatamente um** consumer dentro de um grupo
- Se você tem mais consumers que partições no grupo, os extras ficam ociosos
- Grupos diferentes lêem independentemente (cada um tem seu próprio offset)

### Rebalance

Quando um consumer entra ou sai do grupo, Kafka redistribui as partições. Durante o rebalance, **o processamento pausa**.

**Estratégias de rebalance:**
- **Range** (default histórico) — distribui partições em ranges contíguos
- **RoundRobin** — distribui alternadamente
- **Sticky** — tenta preservar atribuições anteriores (menos movimento)
- **Cooperative Sticky** (Kafka 2.4+) — rebalance incremental, sem "stop the world". **Use em produção.**

**Problemas clássicos:**
- **Rebalance storms** — consumer lento → detecção de falha → rebalance → carga maior nos outros → mais lentos → rebalance... Ajuste `session.timeout.ms` e `max.poll.interval.ms`.
- **Long processing** — se processar uma mensagem demora > `max.poll.interval.ms` (5min default), Kafka acha que o consumer morreu e triggers rebalance.

### Offsets e commit

Offsets são salvos em um tópico interno (`__consumer_offsets`). Opções de commit:

**Auto-commit** — Kafka commita periodicamente em background.

```java
props.put("enable.auto.commit", "true");
props.put("auto.commit.interval.ms", "5000");
```

**Problema:** se o consumer commitar offset 100 mas morrer antes de processar a mensagem 100, ela é perdida. **Não use auto-commit em produção séria.**

**Manual commit — sync:**

```java
props.put("enable.auto.commit", "false");
// ... loop
consumer.commitSync();  // bloqueia até confirmar
```

**Manual commit — async:**

```java
consumer.commitAsync();  // não bloqueia, mas pode falhar silenciosamente
```

**Pattern recomendado (commit após processar):**

```java
while (true) {
    ConsumerRecords<String, String> records = consumer.poll(Duration.ofMillis(100));
    for (ConsumerRecord<String, String> record : records) {
        process(record);  // se der exception, não commita
    }
    consumer.commitSync();  // commita só depois de processar o batch inteiro
}
```

**At-least-once garantido** — se morrer no meio do processamento, re-lê na próxima vez (duplicação possível, por isso consumer idempotente).

### Spring Kafka — consumer

```java
@Configuration
@EnableKafka
public class KafkaConsumerConfig {

    @Bean
    public ConsumerFactory<String, OrderEvent> consumerFactory() {
        return new DefaultKafkaConsumerFactory<>(Map.of(
            ConsumerConfig.BOOTSTRAP_SERVERS_CONFIG, "kafka:9092",
            ConsumerConfig.GROUP_ID_CONFIG, "order-processor",
            ConsumerConfig.KEY_DESERIALIZER_CLASS_CONFIG, StringDeserializer.class,
            ConsumerConfig.VALUE_DESERIALIZER_CLASS_CONFIG, JsonDeserializer.class,
            ConsumerConfig.ENABLE_AUTO_COMMIT_CONFIG, false,
            ConsumerConfig.AUTO_OFFSET_RESET_CONFIG, "earliest",
            ConsumerConfig.MAX_POLL_RECORDS_CONFIG, 500,
            ConsumerConfig.MAX_POLL_INTERVAL_MS_CONFIG, 300000
        ));
    }

    @Bean
    public ConcurrentKafkaListenerContainerFactory<String, OrderEvent> kafkaListenerContainerFactory() {
        var factory = new ConcurrentKafkaListenerContainerFactory<String, OrderEvent>();
        factory.setConsumerFactory(consumerFactory());
        factory.setConcurrency(3);  // 3 threads no consumer
        factory.getContainerProperties().setAckMode(ContainerProperties.AckMode.MANUAL);
        return factory;
    }
}

@Service
public class OrderProcessor {

    @KafkaListener(topics = "orders", groupId = "order-processor")
    public void handle(
            ConsumerRecord<String, OrderEvent> record,
            Acknowledgment ack) {
        try {
            var event = record.value();
            // Idempotência
            if (processedEventRepo.exists(event.getEventId())) {
                ack.acknowledge();
                return;
            }
            orderService.process(event);
            processedEventRepo.save(event.getEventId());
            ack.acknowledge();
        } catch (Exception e) {
            log.error("Failed to process event", e);
            // Não dá ack → mensagem será reprocessada
        }
    }
}
```

### Error handling e retries

Spring Kafka oferece patterns prontos:

```java
// Retry com backoff exponencial + DLQ
@RetryableTopic(
    attempts = "3",
    backoff = @Backoff(delay = 1000, multiplier = 2.0),
    autoCreateTopics = "true",
    dltStrategy = DltStrategy.FAIL_ON_ERROR
)
@KafkaListener(topics = "orders", groupId = "order-processor")
public void handle(OrderEvent event) {
    // Se lançar exceção, Spring publica em orders-retry-0, -1, -2, e finalmente orders-dlt
    orderService.process(event);
}

@DltHandler
public void handleDlt(OrderEvent event) {
    log.error("Event landed in DLT: {}", event);
    // Alerta, salva em banco, etc.
}
```

---

## Replication e fault tolerance

### Replication factor

Cada partição tem `replication.factor` cópias. Produção usa **3** como default.

```
Tópico com replication.factor=3:
  Partition 0:
    Leader: Broker 1
    Follower: Broker 2 (ISR)
    Follower: Broker 3 (ISR)
```

**Leader** handles todas as reads/writes. **Followers** replicam passivamente. Se o leader cai, um dos followers em ISR vira leader.

### In-Sync Replicas (ISR)

Réplicas que estão atualizadas com o leader (dentro de `replica.lag.time.max.ms`, default 30s).

**`min.insync.replicas=2`** — escrita só é confirmada quando **pelo menos 2 ISRs** (incluindo o líder) recebem. Com `acks=all` + `min.insync.replicas=2` em cluster com `replication.factor=3`, você tolera falha de 1 broker sem perder dados.

### Unclean leader election

Se todas as ISRs caem, Kafka pode promover uma réplica **fora de sync** (perdendo dados). Controlado por `unclean.leader.election.enable` (default `false` — seguro).

**Cenário:** leader + ISR caem simultaneamente (ex.: rack caiu). Ou você aceita downtime (default) ou perde dados para ficar disponível (unclean).

---

## Schemas e evolução

Eventos são contratos. Sem schema registry, mudanças quebram consumers.

### Schema Registry

Servidor que armazena schemas (Avro, Protobuf, JSON Schema). Producers registram o schema; consumers buscam quando precisam decodificar. **Confluent Schema Registry** é a implementação padrão.

**Compatibility modes:**

| Mode | Permite | Uso |
| --- | --- | --- |
| BACKWARD | Consumer novo lê producer antigo | Update consumer primeiro |
| FORWARD | Consumer antigo lê producer novo | Update producer primeiro |
| FULL | Ambos | Máxima segurança |
| NONE | Qualquer mudança | Evite |

**Regras:**
- **Adicionar campo com default** — seguro (backward compatible)
- **Remover campo opcional** — seguro se consumer novo não depende
- **Mudar tipo** — nunca seguro
- **Renomear campo** — quebra

### Avro exemplo

```json
{
  "type": "record",
  "name": "OrderCreated",
  "namespace": "com.medespecialista.events",
  "fields": [
    { "name": "order_id", "type": "string" },
    { "name": "customer_id", "type": "string" },
    { "name": "amount_cents", "type": "long" },
    { "name": "currency", "type": "string", "default": "BRL" },
    { "name": "created_at", "type": { "type": "long", "logicalType": "timestamp-millis" } }
  ]
}
```

Código Java é **gerado** a partir do schema. Mudar o schema força atualização do código.

### Alternativa: Protobuf

Similar ao Avro, com melhor integração com gRPC. Use Protobuf se já está nessa stack.

---

## Kafka Connect, Streams, e ksqlDB

Ecossistema Kafka vai além de producer/consumer.

### Kafka Connect

Framework para integração com sistemas externos. Conectores prontos para PostgreSQL, MySQL, MongoDB, Elasticsearch, S3, JDBC, REST, Salesforce, e centenas de outros.

**Source connectors** — lêem de sistema externo → publicam no Kafka
**Sink connectors** — consomem do Kafka → escrevem em sistema externo

**CDC com Debezium:** source connector que lê o WAL do PostgreSQL/MySQL e publica mudanças como eventos no Kafka. **É a base do outbox pattern moderno.**

```
PostgreSQL (WAL) → Debezium → Kafka topic "db.public.orders"
                                ↓
                           Consumers reagem a mudanças
```

### Kafka Streams

Biblioteca Java (não é um cluster separado) para processamento de streams em tempo real. Lê de tópicos, aplica transformações, escreve em outros tópicos.

```java
StreamsBuilder builder = new StreamsBuilder();
KStream<String, OrderEvent> orders = builder.stream("orders");

// Filtra pedidos acima de 1000
orders.filter((key, order) -> order.getAmount() > 1000)
      .to("high-value-orders");

// Agrega totais por customer
orders.groupByKey()
      .aggregate(
          () -> 0L,
          (customerId, order, total) -> total + order.getAmount(),
          Materialized.as("customer-totals")
      )
      .toStream()
      .to("customer-totals-topic");
```

**Use cases:** agregações em tempo real, joins entre streams, enriquecimento, filtragem, windowing (tumbling, hopping, session).

### ksqlDB

SQL sobre Kafka streams. Pode fazer muito do que Kafka Streams faz, em SQL.

```sql
CREATE STREAM orders_stream (
  order_id VARCHAR,
  customer_id VARCHAR,
  amount DOUBLE
) WITH (KAFKA_TOPIC='orders', VALUE_FORMAT='JSON');

CREATE TABLE customer_totals AS
  SELECT customer_id, SUM(amount) AS total
  FROM orders_stream
  GROUP BY customer_id;
```

---

## Exactly-Once Semantics (EOS)

Kafka oferece EOS dentro do cluster via transações.

```
Producer transacional publica em topic1 + topic2 + commit de offset no consumer
  → tudo commitado atomicamente, ou nada
```

**Ingredientes:**
1. **Idempotent producer** (`enable.idempotence=true`)
2. **Transactional producer** (`transactional.id` único)
3. **Consumer em read_committed mode** (`isolation.level=read_committed`)

```java
// Pattern: read-process-write transacional
while (running) {
    var records = consumer.poll(Duration.ofMillis(100));
    producer.beginTransaction();
    for (var record : records) {
        var result = process(record);
        producer.send(new ProducerRecord<>("output", result));
    }
    // Commit de offset dentro da transação
    producer.sendOffsetsToTransaction(
        currentOffsets(consumer),
        consumer.groupMetadata()
    );
    producer.commitTransaction();
}
```

**Importante:** EOS funciona **dentro** do Kafka. Efeitos colaterais fora (escrever no banco, chamar API) não são transacionais com o Kafka. Para isso, use **outbox pattern** + consumer idempotente.

---

## KRaft: adeus Zookeeper

Historicamente, Kafka dependia do Zookeeper para metadata (quem é líder, que brokers existem, configuração). Isso era um ponto de complexidade operacional.

**KRaft (Kafka Raft):** desde Kafka 2.8 (preview) e estável em 3.3+. O Kafka usa Raft internamente para metadata, sem Zookeeper.

**Vantagens:**
- Um sistema a menos para operar
- Metadata mais escalável (suporta mais partições)
- Recovery mais rápido
- Deploy mais simples

Em 2026, **Zookeeper está deprecated**. Clusters novos devem usar KRaft.

---

## Otimização de consumers

Baseado em experiência prática — detalhes em [[Otimizando Kafka consumers]].

### Poll loop tuning

```java
// Quantos records por poll — mais = mais throughput, mais memória
props.put("max.poll.records", "500");

// Timeout máximo entre polls — se processar demorar mais, rebalance
props.put("max.poll.interval.ms", "300000");  // 5 min

// Quanto buscar por fetch — balance entre latência e throughput
props.put("fetch.min.bytes", "1024");
props.put("fetch.max.wait.ms", "500");

// Session timeout — tempo sem heartbeat antes de considerar morto
props.put("session.timeout.ms", "45000");
props.put("heartbeat.interval.ms", "3000");  // ~1/3 do session.timeout
```

### Paralelismo dentro do consumer

Um consumer pode ter múltiplas threads processando mensagens de partições diferentes em paralelo.

```java
// Spring Kafka
factory.setConcurrency(10);  // 10 threads no consumer
```

**Gotcha:** se `concurrency > num_partitions`, threads extras ficam ociosas.

### Batch processing

Em vez de processar uma mensagem por vez, acumule e processe em batch (útil para bulk insert em banco).

```java
@KafkaListener(topics = "orders", containerFactory = "batchKafkaListenerContainerFactory")
public void handleBatch(List<OrderEvent> events, Acknowledgment ack) {
    orderService.bulkProcess(events);  // 1 INSERT com todos, muito mais rápido
    ack.acknowledge();
}
```

### Async processing (cuidado)

```java
@KafkaListener(topics = "orders")
public void handle(OrderEvent event) {
    CompletableFuture.runAsync(() -> process(event));  // ⚠️ CUIDADO
    // Se o consumer commita antes do async terminar, mensagem é perdida se o worker morrer
}
```

**Regra:** processar antes de commitar. Se for async, precisa de controle de backpressure e commit após a conclusão real.

---

## Monitoramento em produção

### Métricas essenciais

**Consumer lag** — a métrica mais importante.

```bash
kafka-consumer-groups --bootstrap-server kafka:9092 \
  --group order-processor --describe
```

```
TOPIC    PARTITION  CURRENT-OFFSET  LOG-END-OFFSET  LAG
orders   0          1050            1100            50
orders   1          2000            2005            5
orders   2          500             10000           9500  ⚠️
```

Uma partição com lag crescente indica: consumer lento, erro em uma mensagem, ou concurrency insuficiente.

**Outras métricas:**
- `MessagesInPerSec`, `BytesInPerSec`, `BytesOutPerSec` por tópico
- `RequestHandlerAvgIdlePercent` — broker overload
- `UnderReplicatedPartitions` — ISR incompleta
- `OfflinePartitionsCount` — partições sem líder (bad)
- `NetworkProcessorAvgIdlePercent` — saturação de rede
- JVM: GC pauses, heap usage

### Ferramentas

- **Burrow** — lag monitoring (LinkedIn, open-source)
- **Kafka Manager / CMAK** — UI para gerenciar cluster
- **Kafka-UI (Provectus)** — UI moderna, open-source
- **Confluent Control Center** — completo, comercial
- **Prometheus JMX Exporter** — expõe métricas Kafka em Prometheus format
- **Kafka Lag Exporter** — lag de consumer groups em Prometheus

---

## Armadilhas comuns

- **Auto-commit em produção** — mensagens são "perdidas" quando consumer morre no meio do processamento. Use manual commit após o processamento.
- **Dimensionamento de partições errado** — poucas = gargalo de paralelismo (não dá para aumentar sem quebrar ordenação por key). Muitas = overhead no broker, rebalance lento.
- **Consumer não idempotente** — at-least-once garantido + não idempotente = duplicação em produção.
- **Sem Schema Registry** — mudanças em eventos quebram consumers silenciosamente. Schema Registry + Avro/Protobuf evita.
- **Mensagens gigantes** — >1MB de payload enche o broker e estoura `max.message.bytes`. Armazene binários em S3, envie URL no evento.
- **`max.poll.interval.ms` curto demais** — processamento lento dispara rebalance false positive, gerando loop. Aumente para cobrir o pior caso.
- **Misturar domínios no mesmo tópico** — acopla contexts. Um tópico por bounded context / aggregate type.
- **Não monitorar lag** — sem alerta de lag, você só descobre problema quando usuário reclama.
- **Unclean leader election em dados críticos** — default `false` é seguro; ligar só com consciência do trade-off.
- **Reset de offset para `earliest` descuidado** — consumer reprocessa todo o histórico, efeitos colaterais (emails, cobranças) acontecem de novo.
- **Não planejar retention** — disco enche, broker cai.
- **Partition key ruim** — chave que concentra mensagens em poucas partições (ex.: `country` em app brasileira = 99% em uma partição). Escolha com distribuição uniforme.
- **Rebalance storms** — consumers lentos → saem do grupo → rebalance → outros ficam com mais carga → saem → rebalance. Tune `session.timeout.ms` e `max.poll.interval.ms`.
- **Esquecer Schema Registry no producer** — escrever JSON puro funciona, mas perde compatibility checks. Avro/Protobuf desde o início.

---

## Na prática (da minha experiência)

> **Muvz — Kafka como espinha dorsal de microserviços:**
> Liderei a adoção de Kafka para comunicação entre 5 microserviços Spring Boot. Construí proof-of-concepts validando latência, throughput e padrões de consumer group, configurei o cluster em Kubernetes junto com o DevOps (usando Strimzi operator), e implementei as integrações event-driven incluindo um microserviço de email com logging e auditoria completos.
>
> **Configurações que usamos em produção:**
> - `replication.factor=3`, `min.insync.replicas=2`, `acks=all` — durabilidade
> - `enable.idempotence=true` nos producers — evita duplicação em retries
> - `compression.type=snappy` — boa compressão, CPU baixo
> - `linger.ms=10` — batching sem comprometer latência
> - Manual commit após processamento bem sucedido
> - Schema Registry + Avro para todos os eventos
> - Debezium para CDC do PostgreSQL → Kafka (outbox pattern implícito)
> - `cooperative-sticky` rebalance strategy para rebalance sem stop-the-world
>
> **Incidente marcante:** um consumer ficou com lag crescente mesmo com carga normal. Debug mostrou que `max.poll.records=500` + processamento de 2s por mensagem = `max.poll.interval.ms` de 5min era insuficiente (500 × 2s = 1000s = 16min). Rebalance infinito. Solução: reduzir `max.poll.records` para 50 e otimizar o processamento para 200ms. Lag voltou ao normal.
>
> **MedEspecialista — Kafka para replay de eventos:**
> No MedEspecialista, uso Kafka com retention de 30 dias no tópico principal de eventos de negócio. Quando lancei um novo módulo de analytics meses depois, ele processou todo o histórico. Em RabbitMQ isso seria impossível — as mensagens já teriam sido consumidas e apagadas.
>
> **Outbox pattern com Debezium** foi a decisão mais importante: zero inconsistência entre PostgreSQL e Kafka. O banco é a fonte de verdade, o Kafka é derivado. Se o Kafka cai, o WAL ainda está lá esperando — quando o Kafka volta, Debezium publica o pendente.
>
> **Lag monitoring é sagrado:** Burrow → Prometheus → Grafana com alerta de "lag > 1000 por mais de 5 min". Salvou a pele algumas vezes — problemas detectados em minutos, não horas.
>
> **A lição principal:** Kafka é poderoso, mas opera com seriedade. É uma plataforma, não uma biblioteca. Você precisa investir em operação, monitoring e schema management. O retorno é uma arquitetura resiliente, auditável, e pronta para escalar.

---

## How to explain in English

> "Kafka is my default choice for event streaming in microservices architectures. I've led its adoption at two companies, and what I value most is the combination of high throughput, durable retention, replay capability, and the ability to have multiple independent consumer groups reading the same topic.
>
> The mental model for Kafka is the immutable append-only log partitioned for parallelism. Each partition preserves ordering, and each consumer group has its own offset. This is fundamentally different from a traditional message queue, where a message is consumed once and removed.
>
> In production, I use `acks=all` with `min.insync.replicas=2` and replication factor 3 for durability. The idempotent producer is enabled by default, which prevents duplicates on retries. I use the Schema Registry with Avro for all events, which enforces backward compatibility automatically — changes that would break consumers fail at the producer level, before hitting production.
>
> On the consumer side, I always use manual offset commits after successful processing. Auto-commit is dangerous because it can commit an offset before the message is actually processed, leading to silent message loss. And I always design consumers to be idempotent, because at-least-once delivery means duplicates are possible during retries or rebalances.
>
> For atomicity between database writes and Kafka publishing, I use the outbox pattern — typically with Debezium reading the PostgreSQL WAL and publishing to Kafka automatically. This gives me exactly-once semantics effectively, without the complexity of Kafka transactions.
>
> Finally, observability is critical. Consumer lag is the most important metric — it tells you whether consumers can keep up with producers. I monitor it continuously and alert when it grows. Rebalance storms, unclean leader elections, and under-replicated partitions are the other things I watch for."

### Frases úteis em entrevista

- "Kafka is a distributed log, not a traditional queue — that's the mental model that makes everything click."
- "I use at-least-once delivery with idempotent consumers as the default. Exactly-once is rarely worth the complexity."
- "For durability, I use `acks=all` with `min.insync.replicas=2` and replication factor 3."
- "I never use auto-commit in production. Manual commit after processing is the only safe pattern."
- "Schema Registry with Avro catches breaking changes at the producer level, before they hit production."
- "The outbox pattern with Debezium gives me effective exactly-once without Kafka transactions."
- "Consumer lag is the most important metric I monitor in production."
- "When sizing partitions, I plan for 2-3x the expected consumer parallelism."
- "Log compaction lets me use Kafka as both an event log and a source of truth for current state."

### Key vocabulary

- plataforma de event streaming → event streaming platform
- broker → broker
- tópico → topic
- partição → partition
- offset → offset
- grupo de consumidores → consumer group
- rebalanceamento → rebalancing
- réplica em sincronia → in-sync replica (ISR)
- fator de replicação → replication factor
- líder / seguidor → leader / follower
- reset de offset → offset reset
- política de retenção → retention policy
- compactação de log → log compaction
- produtor idempotente → idempotent producer
- semântica de exatamente uma vez → exactly-once semantics (EOS)
- registro de esquemas → schema registry
- captura de dados de mudança → change data capture (CDC)
- atraso do consumidor → consumer lag
- desligamento gracioso → graceful shutdown

---

## Recursos

### Livros

- *Kafka: The Definitive Guide* (2nd edition) — Gwen Shapira, Todd Palino et al. (O livro)
- *Designing Event-Driven Systems* — Ben Stopford (gratuito, Confluent)
- *Kafka Streams in Action* — Bill Bejeck
- *Mastering Kafka Streams and ksqlDB* — Mitch Seymour

### Cursos

> [!info] Apache Kafka for Beginners - Learn Kafka by Hands-On
> [https://www.udemy.com/course/apache-kafka-deep-dive-hands-on-using-javabuilt-in-scripts/](https://www.udemy.com/course/apache-kafka-deep-dive-hands-on-using-javabuilt-in-scripts/)

> [!info] Apache Kafka for Developers using Spring Boot [LatestEdition]
> [https://www.udemy.com/course/apache-kafka-for-developers-using-springboot/](https://www.udemy.com/course/apache-kafka-for-developers-using-springboot/)

### Documentação

- [Apache Kafka Documentation](https://kafka.apache.org/documentation/)
- [Spring for Apache Kafka](https://docs.spring.io/spring-kafka/reference/index.html)
- [Confluent Documentation](https://docs.confluent.io/)
- [Confluent Developer](https://developer.confluent.io/) — tutoriais e quickstarts

### Ferramentas

- [Kafka-UI (Provectus)](https://github.com/provectus/kafka-ui) — UI web open-source
- [Burrow](https://github.com/linkedin/Burrow) — lag monitoring
- [Strimzi](https://strimzi.io/) — Kafka operator para Kubernetes
- [kcat (antigo kafkacat)](https://github.com/edenhill/kcat) — CLI para produzir e consumir
- [Kafka Visualization (SoftwareMill)](https://softwaremill.com/kafka-visualisation/) — visualizador interativo de replicação
- [Debezium](https://debezium.io/) — CDC connector

### Artigos essenciais

- [In the land of sizing, the one-partition Kafka topic is king](https://community.aws/posts/in-the-land-of-the-sizing-the-one-partition-kafka-topic-is-king/01-what-are-partitions)
- [Hands-Free Kafka Replication](https://www.confluent.io/blog/hands-free-kafka-replication-a-lesson-in-operational-simplicity/)
- [Intro to Apache Kafka with Spring — Baeldung](https://www.baeldung.com/spring-kafka)
- [Read Data From the Beginning Using Kafka Consumer API — Baeldung](https://www.baeldung.com/java-kafka-consumer-api-read)
- [Otimizando Kafka consumers (Medium)](https://medium.com/@alvarobacelar/otimizando-kafka-consumers-ec46342dba3d)

### Notas relacionadas

- [[Kafka Concepts]] — conceitos fundamentais em Java
- [[Setting Up Kafka]] — setup local
- [[Otimizando Kafka consumers]] — artigo + notas

---

## Veja também

- [[Mensageria]] — contexto geral, comparação com outros brokers
- [[Event Streaming]] — event sourcing, CQRS, streams
- [[RabbitMQ]] — alternativa para task queues com routing
- [[BullMQ]] — alternativa para Node.js
- [[Event Storming]] — descobrir eventos de domínio
- [[System Design]] — quando e como usar Kafka em system design
- [[Arquitetura de Software]] — event-driven architecture
- [[Spring Boot]] — integração com Spring Kafka
- [[Banco de dados]] — CDC, outbox pattern
