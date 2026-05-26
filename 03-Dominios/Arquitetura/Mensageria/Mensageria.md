---
title: "Mensageria"
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

# Mensageria

Comunicação assíncrona entre sistemas através de um broker intermediário que recebe, armazena e entrega mensagens. É a base de arquiteturas desacopladas, resilientes e escaláveis — e uma das skills mais pedidas em entrevistas senior.

## O que é

Mensageria é um estilo de comunicação onde **producers** enviam mensagens para um **broker** e **consumers** as processam de forma assíncrona. O producer não conhece o consumer, o consumer não precisa estar disponível no momento do envio, e o broker garante a entrega conforme as regras configuradas.

Em entrevistas, o que diferencia um senior em mensageria:

1. **Saber quando usar (e quando NÃO usar)** — nem tudo precisa de fila. Uma chamada HTTP síncrona é mais simples quando funciona.
2. **Entender as garantias de entrega** — at-most-once, at-least-once, exactly-once. E quando cada uma é apropriada.
3. **Projetar consumers idempotentes** — o princípio mais importante. Sem isso, at-least-once quebra silenciosamente.
4. **Conhecer os trade-offs entre brokers** — Kafka, RabbitMQ, SQS, BullMQ resolvem problemas diferentes.
5. **Saber lidar com falhas** — retry, backoff, dead letter queues, poison messages.
6. **Pensar em observabilidade** — lag, throughput, queue depth, consumer health.

---

## Síncrono vs assíncrono: a decisão fundamental

**Comunicação síncrona (HTTP, gRPC):**
- Request/response no mesmo instante
- Producer bloqueia esperando o consumer responder
- Falha imediatamente visível
- Acoplamento temporal forte (ambos precisam estar vivos)

**Comunicação assíncrona (mensageria):**
- Producer publica e segue em frente
- Consumer processa no seu ritmo
- Falhas tratadas via retry
- Desacoplamento temporal (consumer pode estar offline)

**Use síncrono quando:**
- A resposta é necessária para continuar (ex.: validar login, consultar saldo)
- Latência baixa é crítica e operação é rápida
- Operação é idempotente e retry é trivial
- Rastreamento de erro precisa ser imediato

**Use assíncrono quando:**
- A operação pode acontecer depois sem prejuízo (ex.: enviar email, atualizar analytics)
- Você precisa absorver picos de tráfego (buffer entre frontend e processamento pesado)
- Múltiplos consumers precisam reagir ao mesmo evento
- Resiliência importa mais que latência (ex.: se o serviço de email cair, pedidos não podem parar)
- Desacoplar times/serviços (producer não precisa conhecer consumers)

**Regra prática:** prefira síncrono por default (mais simples). Mude para assíncrono quando identificar dor concreta: latência ruim, acoplamento excessivo, picos de tráfego, resiliência insuficiente.

---

## Message Queue vs Event Streaming

A distinção mais importante em mensageria moderna. Muita gente mistura os dois conceitos.

### Message Queue (task queue)

Modelo: **mensagem é uma tarefa para ser executada**.

- Mensagem é consumida e **removida** da fila
- Cada mensagem é processada por **um** consumer (competing consumers)
- Foco em **processamento de trabalho** (jobs, emails, notificações, image processing)
- Produto clássico: RabbitMQ, AWS SQS, BullMQ, ActiveMQ

```
[Producer] → [Queue: msg1, msg2, msg3] → [Consumer A toma msg1]
                                       ↘ [Consumer B toma msg2]
```

### Event Streaming (log)

Modelo: **evento é um fato imutável que aconteceu**.

- Eventos são **persistidos** no log, não removidos após consumo
- Múltiplos consumers lêem o mesmo evento, cada um com seu próprio offset
- Eventos podem ser **reprocessados** (replay)
- Foco em **integração de dados e event-driven architecture**
- Produto clássico: Apache Kafka, Apache Pulsar, Redpanda, AWS Kinesis

```
[Producer] → [Log: event1, event2, event3, ...] ← [Consumer Group A, offset=42]
                                                 ← [Consumer Group B, offset=100]
                                                 ← [Consumer Group C, offset=0 (novo)]
```

### Tabela comparativa

| Aspecto | Message Queue | Event Streaming |
| --- | --- | --- |
| Modelo mental | Fila de tarefas | Log imutável de fatos |
| Consumo | Destrutivo (remove após) | Não destrutivo (mantém) |
| Replay | Não (mensagem se foi) | Sim (offset) |
| Consumers por mensagem | Um (competing) | Múltiplos (consumer groups) |
| Ordenação | Limitada (priority queues, FIFO queues) | Garantida por partição/key |
| Retenção | Até consumo (horas/dias max) | Configurável (horas, dias, infinito) |
| Modelo de push/pull | Push (broker envia) | Pull (consumer busca) |
| Throughput típico | Mil-dezenas de milhares/s | Centenas de milhares-milhões/s |
| Use case | Background jobs, workflows, RPC assíncrono | Event-driven, analytics, CQRS, CDC |
| Produto exemplo | RabbitMQ, SQS, BullMQ | Kafka, Pulsar, Kinesis |

**Princípio:** se a pergunta é "como processar esta tarefa em background?", é queue. Se a pergunta é "como múltiplos serviços reagem a este fato?", é streaming.

### Regra prática de decisão

```
Você precisa replay ou múltiplos consumers independentes?
  ├─ Sim → Event Streaming (Kafka)
  └─ Não → Message Queue
      │
      ├─ Precisa de routing complexo (topics, fanout, headers)?
      │  └─ RabbitMQ
      │
      ├─ Node.js com jobs simples + Redis disponível?
      │  └─ BullMQ
      │
      ├─ AWS + quer managed simples?
      │  └─ SQS + SNS (pub/sub)
      │
      └─ Alta performance, baixa latência, pub/sub simples?
         └─ NATS / Redis Streams
```

---

## Garantias de entrega

Toda discussão séria de mensageria gira em torno de **delivery semantics**. Entender isso é essencial.

### At-most-once (no máximo uma vez)

- Mensagem pode ser **perdida**, nunca **duplicada**
- Producer envia e não espera confirmação; consumer processa e "esquece"
- **Performance máxima**, confiabilidade mínima
- **Quando usar:** métricas não críticas, logs de baixa prioridade, telemetria com amostragem

### At-least-once (pelo menos uma vez)

- Mensagem **nunca é perdida**, mas pode ser **duplicada**
- Producer reenvia em falha; consumer pode processar a mesma mensagem duas vezes
- **Default da maioria dos brokers** (Kafka, RabbitMQ, SQS)
- **Exige consumers idempotentes** — sem isso, duplicação causa bugs silenciosos
- **Quando usar:** a maioria dos casos reais

### Exactly-once (exatamente uma vez)

- Nem perde, nem duplica — do ponto de vista do efeito observável
- **Complexo** de implementar genuinamente em sistema distribuído
- Kafka oferece "Exactly-Once Semantics" (EOS) via transações producer↔broker↔consumer
- **Custo:** throughput menor, complexidade maior, só funciona dentro do cluster Kafka (não cross-system)
- **Quando usar:** operações financeiras críticas, contabilidade, inventário

**Na prática 99% dos casos:** **at-least-once + consumers idempotentes**. Simples, robusto, e evita a complexidade de exactly-once.

### Idempotência no consumer

Um consumer é idempotente se processar a mesma mensagem N vezes produz o mesmo resultado que processar 1 vez. Como garantir:

**1. Identificador único por mensagem + tabela de processados:**

```java
@KafkaListener(topics = "orders")
public void handle(OrderEvent event) {
    if (processedEventsRepo.exists(event.getEventId())) {
        log.info("Event {} already processed, skipping", event.getEventId());
        return;
    }
    // Processar
    orderService.process(event);
    // Marcar como processado (na mesma transação!)
    processedEventsRepo.save(new ProcessedEvent(event.getEventId()));
}
```

**2. Operações idempotentes por natureza:**

```java
// Idempotente: setar status é idempotente
orderService.setStatus(orderId, "CONFIRMED");

// Não idempotente: incrementar contador
orderService.incrementCounter(counterId);  // duas vezes = contagem errada
```

**3. Upsert em vez de insert:**

```sql
-- Idempotente
INSERT INTO orders (id, status) VALUES (?, ?)
ON CONFLICT (id) DO UPDATE SET status = EXCLUDED.status;
```

**4. Chave de idempotência natural do domínio:**

Ex.: pagamento tem `payment_intent_id` único. Processar 2 vezes = mesmo resultado (cobrança única).

---

## Padrões de mensageria

### Point-to-Point (fila simples)

Uma mensagem é consumida por **um** consumer. Se há múltiplos consumers inscritos na fila, cada um pega mensagens diferentes (competing consumers). Clássico de task queue.

```
[Producer] → [Queue] → [Consumer 1 pega msg A]
                     → [Consumer 2 pega msg B]
                     → [Consumer 3 pega msg C]
```

**Uso:** background jobs, envio de email, processamento de imagens.

### Publish-Subscribe (pub/sub)

Uma mensagem vai para **todos** os subscribers. Cada subscriber recebe sua própria cópia.

```
[Producer] → [Topic] → [Subscriber A recebe msg]
                     → [Subscriber B recebe msg]
                     → [Subscriber C recebe msg]
```

**Uso:** notificações, eventos de domínio, broadcast.

**Implementações:**
- Kafka: múltiplos consumer groups lendo o mesmo tópico
- RabbitMQ: exchange tipo `fanout`
- Redis Pub/Sub: canais (sem persistência — mensagens perdidas se subscriber está offline)
- AWS SNS: tópicos com múltiplos subscribers (SQS queues, Lambda, email, etc.)

### Fan-out

Uma mensagem dispara múltiplas ações em paralelo. É pub/sub quando cada ação é um serviço diferente.

```
order.created → Inventory Service (decrementar estoque)
             → Notification Service (enviar email)
             → Analytics Service (registrar conversão)
             → Audit Service (logar auditoria)
```

Cada consumer processa independentemente. Se o Analytics Service cair, Inventory e Notification continuam funcionando. Desacoplamento total.

### Competing Consumers

Múltiplas instâncias do **mesmo** consumer processando em paralelo, para escalar throughput. Cada mensagem vai para exatamente uma instância.

```
[Queue] → [Consumer instance 1]
        → [Consumer instance 2]
        → [Consumer instance 3]
```

No Kafka, isso é automático via consumer groups e partições — cada partição é atribuída a uma única instância do grupo.

### Request-Reply assíncrono

Pattern onde um request é enviado e a resposta vem de volta via outra fila, com correlação por ID.

```
Client → [request-queue] → Server
Server → [reply-queue]   → Client (correlation_id = original id)
```

**Uso:** RPC assíncrono, integração entre sistemas que se comunicam por mensageria mas precisam de retorno.

**Cuidado:** esse pattern é frequentemente um sinal de que você devia usar HTTP síncrono. Só use se houver razão arquitetural forte.

### Dead Letter Queue (DLQ)

Fila especial para mensagens que falharam após N retries. Evita que mensagens "venenosas" fiquem travando o processamento.

```
msg → Queue → Consumer (retry 1, 2, 3 falham) → DLQ → alerta + investigação manual
```

**Boas práticas:**
- Toda fila em produção deve ter DLQ associada
- Alerte quando a DLQ tem itens (deveria ser raro)
- Inclua metadata no DLQ: erro, stack trace, timestamp, número de tentativas
- Permita replay manual após consertar o bug

### Outbox Pattern

Garantir atomicidade entre **escrita no banco** e **publicação de mensagem**. Problema clássico: como garantir que "salvei o pedido E publiquei o evento" sejam atômicos?

**Abordagem ingênua (falha):**

```java
@Transactional
public void createOrder(Order order) {
    orderRepo.save(order);           // ✓ commit no banco
    kafka.send("orders", event);     // ✗ se falha aqui, banco já commitou
}
```

Se o Kafka estiver fora, o pedido é criado mas o evento nunca sai. Inconsistência silenciosa.

**Outbox Pattern:**

```java
@Transactional
public void createOrder(Order order) {
    orderRepo.save(order);
    outboxRepo.save(new OutboxEvent("order.created", serialize(event)));
    // Ambos na mesma transação — ou vai tudo ou vai nada
}

// Processo separado lê a tabela outbox e publica
@Scheduled(fixedDelay = 1000)
public void publishOutbox() {
    List<OutboxEvent> pending = outboxRepo.findPending(100);
    for (var event : pending) {
        kafka.send(event.getTopic(), event.getPayload());
        outboxRepo.markPublished(event.getId());
    }
}
```

**Variações:**
- **Polling simples** — como acima, um job lê a tabela
- **CDC (Change Data Capture)** — Debezium lê o WAL do Postgres e publica direto no Kafka. Mais eficiente, mais infra.

Outbox garante **at-least-once** — o processo pode publicar e morrer antes de marcar como publicado, resultando em duplicata. Consumer idempotente resolve.

### Saga (transações distribuídas)

Quando uma operação de negócio precisa coordenar múltiplos serviços e não cabe em uma transação ACID única.

**Orquestração** — um orquestrador central comanda os passos:

```
OrderSaga:
  1. PaymentService.charge() → success
  2. InventoryService.reserve() → success
  3. ShippingService.schedule() → FAILURE
  4. Compensate: InventoryService.release() + PaymentService.refund()
```

**Coreografia** — cada serviço reage a eventos, sem orquestrador:

```
OrderCreated → PaymentService
  PaymentCompleted → InventoryService
    InventoryReserved → ShippingService
      ShippingScheduled → done

  PaymentFailed → OrderService (cancel)
```

**Quando usar cada:**
- **Orquestração** — lógica de negócio complexa, ramificações condicionais, fácil de raciocinar
- **Coreografia** — desacoplamento máximo, simples para fluxos lineares, mais difícil de debugar

### Event Sourcing

Estado derivado de uma sequência imutável de eventos. Extremo dos eventos como source of truth. → Detalhes em [[Event Streaming]] e [[Event Storming]].

---

## Retry, backoff e poison messages

### Retry strategy

Quando um consumer falha, tentar de novo. Mas ingênuo pode piorar o problema:

- **Retry imediato infinito** — se o bug é permanente, gira em loop queimando CPU
- **Retry síncrono sem limite** — consumer fica travado em uma mensagem, lag cresce
- **Todos os consumers tentando ao mesmo tempo** — thundering herd no downstream

### Exponential backoff com jitter

```
tentativa 1 → imediata
tentativa 2 → 1s  + random(0, 1s)
tentativa 3 → 2s  + random(0, 1s)
tentativa 4 → 4s  + random(0, 1s)
tentativa 5 → 8s  + random(0, 1s)
...
max retries → DLQ
```

**Por que jitter?** Se 1000 consumers falham ao mesmo tempo (ex.: banco estava fora), todos retentariam no mesmo instante. Jitter distribui os retries no tempo.

### Poison messages

Mensagem que **sempre** falha — geralmente porque o payload é inválido ou representa um caso que o código não trata. Se você só retentar, ela trava a fila para sempre (especialmente se sua fila preserva ordem).

**Tratamento:**
1. Retry com limite (ex.: 3-5 tentativas)
2. Após limite, move para DLQ
3. Alerta o time
4. Consumer continua com a próxima mensagem

### Retry topic pattern (Kafka)

Kafka não tem retry nativo com delay. Pattern: múltiplos tópicos de retry com delays crescentes.

```
orders → orders.retry.5s → orders.retry.30s → orders.retry.5min → orders.dlq
```

Consumer do tópico principal falha → publica no `retry.5s` com timestamp. Consumer do `retry.5s` espera 5s antes de processar. Se falha de novo, vai pro `retry.30s`. E assim por diante.

**Spring Kafka** tem `@RetryableTopic` que automatiza isso.

---

## Ordenação de mensagens

**Fato:** ordenação global em sistema distribuído é cara. A maioria das soluções oferece ordenação **parcial**.

### Kafka: ordenação por partição

Mensagens dentro de uma mesma partição são ordenadas. Mensagens em partições diferentes não têm ordem garantida entre si.

**Estratégia:** usar uma **chave** para garantir que mensagens relacionadas vão para a mesma partição.

```java
// Todas as mensagens do user 42 vão para a mesma partição → ordem garantida
producer.send("events", "user-42", eventJson);
```

**Trade-off:** se você precisa de ordenação global, usa 1 partição → perde paralelismo.

### RabbitMQ: ordenação por fila

Fila single-consumer preserva ordem. Múltiplos consumers (competing) quebram ordem.

**FIFO queues** (RabbitMQ 3.9+): garantem ordenação mesmo com múltiplos consumers, mas com throughput reduzido.

### AWS SQS: FIFO queues

SQS standard não garante ordem. **SQS FIFO** garante, mas com limites de throughput (3.000 msg/s com batching).

### Regra prática

- Se não precisa de ordem → standard queue/topic, paralelismo máximo
- Se precisa de ordem por entidade (user, order) → shard key + partição/fila dedicada
- Se precisa de ordem global → 1 partição, aceita o gargalo

---

## Comparação de brokers

Cada broker resolve um problema diferente. Escolher errado é fonte comum de retrabalho.

### Apache Kafka

**Pontos fortes:**
- Alto throughput (milhões de mensagens/s)
- Persistência com retenção longa (dias, semanas, infinito)
- Replay — consumer novo pode processar histórico inteiro
- Ordenação por partição
- Consumer groups para múltiplos consumers independentes
- Ecossistema rico (Kafka Connect, Kafka Streams, Schema Registry)

**Pontos fracos:**
- Complexidade operacional (cluster, Zookeeper/KRaft, tuning)
- Latência mínima maior que brokers in-memory (~ms)
- Overkill para filas simples de tarefas

**Ideal para:** event streaming, event-driven architecture entre microserviços, CDC, analytics pipelines, replay de eventos, log de auditoria.

→ Para deep dive: [[03-Dominios/Arquitetura/Mensageria/Kafka]]

### RabbitMQ

**Pontos fortes:**
- **Routing flexível** — exchanges (direct, topic, fanout, headers)
- Priority queues
- Delayed messages (via plugin)
- Request-reply nativo
- Cluster + mirrored queues
- Protocolos múltiplos (AMQP, MQTT, STOMP)
- Latência baixa

**Pontos fracos:**
- Throughput menor que Kafka (dezenas-centenas de milhares/s)
- Sem replay — mensagens são removidas após consumo
- Mirrored queues têm limitações de performance

**Ideal para:** task queues com routing complexo, workflows, RPC assíncrono, filas com prioridade.

### AWS SQS + SNS

**SQS** — fila managed simples. **SNS** — pub/sub managed simples.

**Pontos fortes:**
- Totalmente managed, zero ops
- Integração nativa com outros serviços AWS (Lambda, etc.)
- Escalável sem configuração
- Barato em baixo/médio volume

**Pontos fracos:**
- Menos features que RabbitMQ ou Kafka
- Vendor lock-in
- Sem ordering na standard queue (FIFO queue tem throughput limitado)
- Sem replay
- Latência maior (rede AWS)

**Ideal para:** quando você já está na AWS e precisa de fila simples sem ops. Combinação SNS → múltiplas SQS é o fan-out padrão em AWS.

### BullMQ (Node.js + Redis)

Job queue para Node.js baseada em Redis.

**Pontos fortes:**
- Simples de configurar (só precisa de Redis)
- Rich job API: priority, delay, retry, cron, rate limiting
- Dashboard (Bull Board, Arena)
- Leve e rápido
- Ideal para projetos Node.js

**Pontos fracos:**
- Não é pub/sub (é job queue)
- Depende de Redis (persistência limitada em relação a Kafka)
- Node-centric

**Ideal para:** background jobs em aplicações Node.js, cron jobs, workflows de processamento.

→ Detalhes: [[BullMQ]]

### Redis Streams

Stream de mensagens sobre Redis. Similar a Kafka em modelo (log + consumer groups) mas dentro do Redis.

**Pontos fortes:**
- Se você já usa Redis, não precisa de infra adicional
- Latência muito baixa (in-memory)
- Consumer groups
- API simples

**Pontos fracos:**
- Durabilidade limitada pela persistência do Redis
- Escala limitada a um instance (ou cluster Redis)
- Ecossistema menor que Kafka

**Ideal para:** event streaming leve, quando Kafka é overkill mas Pub/Sub é insuficiente.

### NATS

Broker moderno focado em alta performance e simplicidade.

**Pontos fortes:**
- Latência sub-milisegundo
- Simples, um binário
- Cloud-native, leve
- NATS JetStream adiciona persistência e streaming

**Pontos fracos:**
- Ecossistema menor
- Sem replay nativo (JetStream resolve)

**Ideal para:** microserviços cloud-native, pub/sub de alta performance, edge/IoT.

### Apache Pulsar

Alternativa moderna ao Kafka. Separa compute (brokers) de storage (BookKeeper).

**Pontos fortes:**
- Multi-tenancy nativa
- Geo-replication built-in
- Suporta queue e streaming
- Escalabilidade horizontal mais simples que Kafka

**Pontos fracos:**
- Menos adotado que Kafka
- Mais complexo operacionalmente (2 sistemas: brokers + BookKeeper)

**Ideal para:** casos onde Kafka seria usado mas multi-tenancy ou geo-replication são requisitos fortes.

### Tabela resumo

| Broker | Modelo | Throughput | Latência | Replay | Ops | Ideal para |
| --- | --- | --- | --- | --- | --- | --- |
| Kafka | Log | Altíssimo | ~ms | Sim | Alta | Event streaming, EDA |
| RabbitMQ | Queue | Alto | Baixa | Não | Média | Task queues, routing |
| SQS/SNS | Queue/PubSub | Alto | Média | Não | Zero | AWS-native, simples |
| BullMQ | Queue | Médio | Baixa | Não | Baixa (Redis) | Node.js jobs |
| Redis Streams | Log | Alto | Muito baixa | Sim | Baixa | Streaming leve |
| NATS | Queue/PubSub | Muito alto | Mínima | Com JetStream | Baixa | Microserviços modernos |
| Pulsar | Log/Queue | Altíssimo | ~ms | Sim | Alta | Multi-tenant, geo |

---

## Observabilidade em mensageria

Mensageria adiciona complexidade. Sem observabilidade, debugging vira arqueologia.

### Métricas críticas

**Do broker:**
- **Queue depth / Topic lag** — quantas mensagens não processadas. Crescimento contínuo = consumer não acompanha
- **Throughput** — mensagens/s publicadas e consumidas
- **Disk usage** — importante para Kafka (retenção) e RabbitMQ (mensagens persistidas)
- **Connections** — producers e consumers conectados

**Do producer:**
- **Taxa de envio** — mensagens/s e bytes/s
- **Erros de publicação** — network errors, broker errors
- **Latência de publicação** — tempo do send ao ack

**Do consumer:**
- **Lag** (Kafka específico) — diferença entre offset atual e último offset do tópico. **A métrica mais importante**
- **Taxa de processamento** — mensagens/s
- **Taxa de erros** — mensagens que caíram em DLQ
- **Duração de processamento** — tempo médio para processar uma mensagem
- **Rebalance count** (Kafka) — rebalances frequentes indicam problema

### Distributed tracing

Um request que começa em HTTP → vira evento → processado por múltiplos consumers → precisa ser rastreável.

- Propague `traceId` como header da mensagem
- Cada consumer começa um span linkado ao span do producer
- Visualização em Jaeger/Zipkin mostra o flow completo

**Spring Kafka + OpenTelemetry** fazem isso automaticamente.

### Alertas típicos

- Lag > X por mais de Y minutos
- DLQ com itens (deveria ser raro)
- Consumer desconectado
- Disk > 80%
- Producer com taxa de erro > 1%

---

## Armadilhas comuns

- **Consumer não idempotente** — at-least-once + não idempotente = bugs silenciosos. Duplicação é inevitável.
- **Sem DLQ** — primeira poison message trava a fila para sempre.
- **Retry infinito** — mensagem venenosa causa loop de CPU e lag crescente.
- **Ignorar a ordenação** — assumir que mensagens vêm ordenadas quando a fila/partição não garante.
- **Mensagens grandes** — gigabytes em payload matam throughput. Armazene no S3, envie a URL.
- **Mistura de domínios no mesmo tópico** — acoplamento por schema. Separe por bounded context.
- **Schema sem versionamento** — mudança quebra todos os consumers. Use Schema Registry (Avro, Protobuf).
- **Polling síncrono dentro do consumer** — bloqueia a thread, não escala. Use chamadas async ou workers.
- **Commit de offset antes de processar** — perde mensagem se o consumer morrer no meio.
- **Commit depois de cada mensagem** — mata performance. Batch commits quando possível.
- **Sem observabilidade** — não saber o lag é voar cego.
- **Usar mensageria para RPC síncrono** — request-reply via mensageria quando HTTP resolveria mais simples.
- **Monólogo ignorando o banco** — escrever no banco E publicar sem outbox → inconsistência se um falha.
- **Acoplamento por evento** — um consumer que precisa de um campo específico obriga o producer a nunca remover. Eventos são contratos.
- **Partições demais** — Kafka cobra por partição (memória, file handles). Projetar sem medir custa caro.
- **Partições de menos** — limita paralelismo para sempre (não dá para aumentar sem repartition). Dimensione com folga.
- **Reprocessar eventos antigos sem cuidado** — reset de offset pode reexecutar side effects (emails enviados de novo).

---

## Na prática (da minha experiência)

> **Muvz — migração de monolito para microserviços com Kafka:**
> Na Muvz, liderei a adoção de Kafka como event broker para comunicação entre 5 microserviços Spring Boot. A decisão por Kafka (vs RabbitMQ) foi baseada em três requisitos: **replay de eventos** (novos consumers poderiam processar histórico), **múltiplos consumers independentes** (consumer groups), e **alto throughput** (esperávamos crescimento significativo). Construí proof-of-concepts validando o setup, configurei o cluster em Kubernetes junto com o DevOps, e implementei as integrações event-driven entre os serviços — incluindo um microserviço de email com logging e auditoria completos.
>
> **Lições aprendidas:**
>
> **1. Idempotência é não-negociável.** Todos os consumers foram projetados com tabela de `processed_events` na mesma transação do processamento. Duplicatas são inevitáveis em retries, e sem idempotência tínhamos emails duplicados, pagamentos dobrados, analytics corrompidos.
>
> **2. DLQ desde o dia 1.** Toda consumer tinha DLQ configurada. Lembro de uma poison message (payload com encoding inválido) que teria travado o processamento inteiro — foi isolada na DLQ, alertamos, investigamos, e mandamos replay após consertar. Sem DLQ, seria downtime.
>
> **3. Outbox pattern para consistência.** Usamos outbox para garantir que escrita no banco e publicação no Kafka eram atômicas. Um processo Debezium lia o WAL do PostgreSQL e publicava no Kafka. Inconsistência zero.
>
> **4. Schema Registry salva vidas.** Avro + Schema Registry força você a pensar em backward compatibility antes de mudar um evento. Sem isso, quebrar consumers é questão de tempo.
>
> **5. Observability first.** Lag monitoring via Burrow → Prometheus → Grafana foi essencial. Um consumer com lag crescente era detectado em minutos, não horas depois quando usuários reclamavam.
>
> **MedEspecialista — decisão consciente por Kafka (mesmo com RabbitMQ disponível):**
> No MedEspecialista, quando precisei escolher o broker, considerei seriamente RabbitMQ (mais simples de operar). Mas escolhi Kafka por um motivo: antecipei que a fonte de verdade de eventos de negócio (consultas, pagamentos, mudanças de estado) valia como log auditável e replayável. Quando implementamos o módulo de analytics meses depois, ele processou todo o histórico do Kafka — impossível em RabbitMQ.
>
> **A lição principal:** escolha o broker pelo seu caso de uso, não pela moda. Kafka não é "o broker melhor" — é o broker certo quando você precisa de log imutável, replay, e consumer groups independentes. Para um job queue de processamento de imagens, RabbitMQ ou BullMQ seriam escolhas mais apropriadas.

---

## How to explain in English

> "Messaging is how I decouple systems in distributed architectures. The first decision I always make is whether I need a message queue or an event stream — they solve different problems. A message queue is for task processing: one consumer takes one message, processes it, and it's gone. An event stream is for facts that happened: events are persisted, and multiple consumers can read them independently, with the ability to replay history.
>
> For task queues, I use RabbitMQ when I need flexible routing or priority, BullMQ for Node.js projects with Redis, or SQS when I'm already in AWS and want zero ops. For event streaming, Kafka is my default because of its throughput, durability, replay capability, and rich ecosystem.
>
> The most important principle in messaging design is **idempotent consumers with at-least-once delivery**. Exactly-once is complex and rarely necessary — at-least-once plus idempotency gives you the same effective guarantee with much simpler code. I always implement idempotency using either a unique event ID tracked in a processed-events table, or by making the operation naturally idempotent like upserts.
>
> For reliability, every queue in production has a dead letter queue. Retries follow exponential backoff with jitter to avoid thundering herds when downstream services recover. For atomicity between database writes and message publishing, I use the outbox pattern — write both to the database in the same transaction, and a separate process publishes from the outbox.
>
> Finally, observability is non-negotiable. I monitor consumer lag as the most important metric — a growing lag means consumers can't keep up, which is often the first sign of trouble. DLQ alerts, producer error rates, and distributed tracing through the message flow complete the picture."

### Frases úteis em entrevista

- "I'd use message queues for task processing and event streaming for facts that multiple services need to react to."
- "My default is at-least-once delivery with idempotent consumers — exactly-once is rarely worth the complexity."
- "Every queue in production needs a DLQ. Poison messages will happen."
- "I use the outbox pattern to guarantee atomicity between database writes and message publishing."
- "Consumer lag is the most important metric to monitor in Kafka — it tells you if consumers can keep up."
- "For ordering, I use a partition key so related messages go to the same partition, but I don't try to guarantee global ordering."
- "Kafka for events that need replay and multiple consumer groups, RabbitMQ for complex routing, BullMQ for Node.js background jobs."

### Key vocabulary

- mensageria → messaging
- comunicação assíncrona → asynchronous communication
- produtor → producer / publisher
- consumidor → consumer / subscriber
- broker de mensagens → message broker
- fila → queue
- tópico → topic
- partição → partition
- fluxo de eventos → event stream / event streaming
- grupo de consumidores → consumer group
- fila de mensagens mortas → dead letter queue (DLQ)
- garantias de entrega → delivery guarantees
- no máximo uma vez → at-most-once
- pelo menos uma vez → at-least-once
- exatamente uma vez → exactly-once
- idempotência → idempotency
- padrão caixa de saída → outbox pattern
- captura de dados de mudança → change data capture (CDC)
- reenvio com backoff → retry with backoff
- mensagem venenosa → poison message
- registro de esquemas → schema registry
- atraso do consumidor → consumer lag
- reprocessamento → replay / reprocessing
- publicação-assinatura → publish-subscribe (pub/sub)
- leque de saída → fan-out

---

## Recursos

### Livros

- *Designing Event-Driven Systems* — Ben Stopford (Confluent, gratuito — o livro sobre Kafka e EDA)
- *Enterprise Integration Patterns* — Gregor Hohpe, Bobby Woolf (os patterns clássicos de mensageria)
- *Kafka: The Definitive Guide* — Gwen Shapira et al.
- *Designing Data-Intensive Applications* — Martin Kleppmann (capítulos sobre replicação, consistência, mensageria)
- *Building Event-Driven Microservices* — Adam Bellemare

### Online

- [Enterprise Integration Patterns](https://www.enterpriseintegrationpatterns.com/) — site com todos os patterns
- [Martin Fowler — What do you mean by "Event-Driven"?](https://martinfowler.com/articles/201701-event-driven.html)
- [Confluent Blog](https://www.confluent.io/blog/) — Kafka e streaming em profundidade
- [CloudAMQP Blog](https://www.cloudamqp.com/blog/) — RabbitMQ na prática
- [Microservices.io — Patterns](https://microservices.io/patterns/data/application-events.html) — saga, outbox, CDC

### Vídeos

> [!info] Fundamentos de Event Streaming e Mensageria
> [https://www.youtube.com/playlist?list=PLkpjQs-GfEMPituMCb77qd90onpF3khFt](https://www.youtube.com/playlist?list=PLkpjQs-GfEMPituMCb77qd90onpF3khFt)

---

## Veja também

- [[03-Dominios/Arquitetura/Mensageria/Kafka]] — deep dive em Apache Kafka
- [[RabbitMQ]] — message queue com routing flexível
- [[BullMQ]] — job queue para Node.js
- [[Event Streaming]] — event sourcing, CQRS, streams
- [[Event Storming]] — workshop para descobrir eventos de domínio
- [[System Design]] — quando e como usar mensageria em system design
- [[Arquitetura de Software]] — event-driven architecture, bounded contexts
- [[API Design]] — webhooks, operações assíncronas
- [[Banco de dados]] — transações, outbox pattern
