---
title: "RabbitMQ"
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

# RabbitMQ

Message broker tradicional baseado no protocolo **AMQP** — routing flexível via exchanges, múltiplos protocolos suportados, maturidade operacional, e o broker de facto para **task queues** e **workflows complexos**. Enquanto [[03-Dominios/Arquitetura/Mensageria/Kafka]] é uma plataforma de event streaming e [[BullMQ]] é uma job queue Node.js, RabbitMQ é o **message broker de propósito geral** mais usado no mercado enterprise.

## O que é

RabbitMQ é um message broker open-source criado em 2007, escrito em **Erlang** (herança do uso em telecom — a BEAM VM é famosa por alta disponibilidade). Implementa o **protocolo AMQP 0.9.1** nativamente, e suporta MQTT, STOMP e outros via plugins.

**O que RabbitMQ faz bem:**
- **Routing flexível** — exchanges com múltiplos padrões (direct, topic, fanout, headers)
- **Modelo conceitual claro** — producer → exchange → binding → queue → consumer
- **Maturidade operacional** — 15+ anos em produção, bem conhecido, bem documentado
- **Multi-protocolo** — AMQP, MQTT, STOMP via plugins
- **Management UI built-in** — dashboard web na porta 15672
- **Garantias de entrega** — acks manuais, publisher confirms, mensagens persistentes
- **Features avançadas** — priority queues, delayed messages (plugin), message TTL, DLX

**O que RabbitMQ NÃO faz bem (comparado a Kafka):**
- **Sem replay** — mensagens são removidas após consumo
- **Throughput menor** — ~100K mensagens/s por nó (vs milhões no Kafka)
- **Múltiplos consumers independentes** exigem fanout explícito, não é o default
- **Retenção longa** — não é projetado para ser um event log

Em entrevistas, o que diferencia um senior em RabbitMQ:

1. **Entender o modelo exchange-binding-queue** — é a abstração central, diferente de Kafka
2. **Escolher o tipo de exchange correto** — direct, topic, fanout, headers têm use cases distintos
3. **Conhecer as garantias de durabilidade** — persistent messages, durable queues, publisher confirms, acks manuais
4. **Saber projetar DLX (Dead Letter Exchange)** — fundamental para production readiness
5. **Cluster e mirrored queues / quorum queues** — entender os modos de HA e seus trade-offs
6. **Quando usar RabbitMQ vs Kafka vs BullMQ** — é a pergunta mais comum em entrevistas sobre mensageria

---

## O modelo AMQP: exchange, binding, queue

A abstração central do RabbitMQ é **diferente** da do Kafka. Entender isso é fundamental.

```
┌──────────┐    ┌────────────┐    ┌──────────┐    ┌──────────┐    ┌──────────┐
│ Producer │ ─→ │  Exchange  │ ─→ │ Binding  │ ─→ │  Queue   │ ─→ │ Consumer │
└──────────┘    └────────────┘    └──────────┘    └──────────┘    └──────────┘
                   ↑
            Producer publica
            AQUI, não na fila
```

**Diferença crítica vs Kafka:** no RabbitMQ, o producer publica em um **exchange**, não diretamente em uma queue. O exchange decide (via bindings) em quais queues colocar a mensagem. Esse desacoplamento é o que dá flexibilidade de routing.

### Componentes

**Producer** — quem publica mensagens. Publica em uma exchange com uma `routing_key`.

**Exchange** — recebe mensagens do producer e decide para quais queues roteá-las, baseado no tipo e bindings.

**Binding** — regra que conecta uma exchange a uma queue. Define critérios de roteamento (routing key, headers, etc.).

**Queue** — armazena mensagens até serem consumidas. Cada mensagem em uma queue é consumida por **um** consumer (competing consumers).

**Consumer** — processa mensagens da queue. Pode ser push (broker envia) ou pull (consumer busca via `basic.get`).

**Virtual Host (vhost)** — namespace lógico. Um cluster pode ter múltiplos vhosts (`/`, `/dev`, `/prod`) com seus próprios exchanges, queues e permissões.

**Connection** — conexão TCP/AMQP do cliente ao broker. Pesada, deve ser long-lived.

**Channel** — multiplex lógico sobre uma connection. Leve, use múltiplos (1 por thread).

### Fluxo de publicação

```
1. Producer abre connection (TCP) → channel (lógico)
2. Declara exchange (idempotente — ok criar se já existe)
3. Publica mensagem:
   publish(exchange="orders", routing_key="order.created", body=...)
4. Exchange avalia bindings
5. Para cada binding que casa, coloca cópia da mensagem na queue correspondente
6. Consumer recebe mensagem da queue
7. Consumer processa e envia ack (ou nack)
8. Queue remove mensagem (ou reenfileira em nack)
```

---

## Tipos de exchange

RabbitMQ tem 4 tipos built-in de exchange, cada um com semântica de routing diferente. Escolher o tipo certo é a decisão mais importante.

### Direct Exchange

Roteia mensagens para queues cujo binding tem **routing key exatamente igual** à routing key da mensagem.

```
Producer → publish(routing_key="error") → [Direct Exchange]
                                              │
           binding: "error" ──────────────→ [error-queue]
           binding: "warning" ─────────────→ [warning-queue]
           binding: "info" ────────────────→ [info-queue]
```

**Uso típico:** roteamento simples por categoria.

```javascript
// Producer
await channel.assertExchange('logs-direct', 'direct', { durable: true });
channel.publish('logs-direct', 'error', Buffer.from('Database connection failed'));

// Consumer (queue para erros apenas)
await channel.assertQueue('error-queue');
await channel.bindQueue('error-queue', 'logs-direct', 'error');
await channel.consume('error-queue', handleError);
```

**Default exchange:** toda queue é automaticamente bindada à "default exchange" (exchange vazia `""`) com routing key = nome da queue. Isso é por que `publish('', 'my-queue', msg)` publica direto numa queue chamada `my-queue`.

### Fanout Exchange

**Ignora routing key** e entrega cópia para **todas** as queues bindadas. É o pub/sub clássico.

```
Producer → publish(any routing_key) → [Fanout Exchange]
                                          │
                                          ├──→ [queue-1] → Consumer A
                                          ├──→ [queue-2] → Consumer B
                                          └──→ [queue-3] → Consumer C
```

**Uso típico:** broadcast de eventos — notificações, updates de cache, log aggregation.

```javascript
// Producer
await channel.assertExchange('order-events', 'fanout', { durable: true });
channel.publish('order-events', '', Buffer.from(JSON.stringify(orderEvent)));

// Multiple consumers, cada um com sua queue
await channel.assertQueue('inventory-queue');
await channel.bindQueue('inventory-queue', 'order-events', '');

await channel.assertQueue('notification-queue');
await channel.bindQueue('notification-queue', 'order-events', '');

await channel.assertQueue('analytics-queue');
await channel.bindQueue('analytics-queue', 'order-events', '');
```

Cada consumer (inventory, notification, analytics) recebe **cópia** de todas as mensagens.

### Topic Exchange

Roteia por **pattern matching** na routing key. Usa `.` como separador e `*` (exatamente uma palavra) ou `#` (zero ou mais palavras) como wildcards.

```
Producer → publish(routing_key="order.created.br") → [Topic Exchange]
                                                         │
           binding: "order.created.*" ─────────→ [br-and-us-creates]
           binding: "order.*.br" ──────────────→ [all-br-events]
           binding: "order.#" ─────────────────→ [all-order-events]
           binding: "#.error" ─────────────────→ [all-errors]
```

**Uso típico:** roteamento por padrões hierárquicos — logs por nível/módulo, eventos por região/tipo, notificações por categoria.

```javascript
// Publisher
await channel.assertExchange('events', 'topic', { durable: true });
channel.publish('events', 'medical.appointment.confirmed.br', payload);

// Consumer A: todos os eventos médicos no Brasil
await channel.bindQueue('br-medical', 'events', 'medical.#.br');

// Consumer B: só confirmações de consulta (qualquer país)
await channel.bindQueue('confirmations', 'events', 'medical.appointment.confirmed.*');

// Consumer C: tudo
await channel.bindQueue('everything', 'events', '#');
```

**Regra prática:** topic exchange é o default razoável quando você quer flexibilidade. Pode imitar direct (sem wildcards) ou fanout (bind com `#`) se precisar.

### Headers Exchange

Roteia baseado em **headers da mensagem**, não em routing key. Usa match type `all` (AND) ou `any` (OR).

```
Producer → publish(headers={format: "pdf", type: "invoice"}) → [Headers Exchange]
                                                                      │
           binding: {format:"pdf", x-match:"all"} ─────→ [pdf-queue]
           binding: {type:"invoice", x-match:"any"} ──→ [invoice-queue]
```

**Uso típico:** roteamento complexo que não cabe em uma routing key simples. Raro na prática — topic exchange cobre a maioria dos casos.

```javascript
await channel.assertExchange('doc-processing', 'headers', { durable: true });

channel.publish('doc-processing', '', buffer, {
  headers: { format: 'pdf', language: 'pt-br', classification: 'invoice' }
});

// Queue que processa PDFs em qualquer idioma
await channel.bindQueue('pdf-processor', 'doc-processing', '', {
  'format': 'pdf',
  'x-match': 'all'
});
```

### Comparação rápida

| Exchange | Critério | Wildcards | Performance | Uso |
| --- | --- | --- | --- | --- |
| **Direct** | Match exato de routing key | Não | Máxima | Routing simples, 1 key = 1 queue |
| **Fanout** | Ignora key | Não | Altíssima (sem match) | Broadcast / pub-sub |
| **Topic** | Pattern match em key | `*`, `#` | Alta | Flexibilidade, hierarquia |
| **Headers** | Match de headers | N/A | Menor | Casos raros sem key natural |

---

## Garantias de durabilidade

RabbitMQ oferece múltiplas camadas de garantia. Use **todas** em produção se não pode perder mensagens.

### 1. Durable exchange

Exchange sobrevive ao restart do broker.

```javascript
await channel.assertExchange('orders', 'topic', { durable: true });
```

### 2. Durable queue

Queue sobrevive ao restart do broker. **Não basta durable** — mensagens ainda podem ser perdidas se não forem persistent.

```javascript
await channel.assertQueue('order-processing', { durable: true });
```

### 3. Persistent message

A mensagem é gravada em disco (não só em memória). Sobrevive ao restart se a queue também for durable.

```javascript
channel.publish('orders', 'order.created', buffer, {
  persistent: true  // delivery mode 2
});
```

**Combinação necessária para durabilidade:**
```
durable exchange + durable queue + persistent message
```

Se qualquer um faltar, mensagens podem ser perdidas em crash.

### 4. Publisher confirms

Garante que o broker recebeu e persistiu a mensagem. Sem isso, a publicação é "fire and forget" do ponto de vista do publisher.

```javascript
// Ativar confirms no channel
const confirmChannel = await connection.createConfirmChannel();

await confirmChannel.publish('orders', 'order.created', buffer,
  { persistent: true },
  (err, ok) => {
    if (err) {
      // Broker não confirmou — retry ou alertar
      console.error('Publish failed', err);
    } else {
      // Confirmado
      console.log('Published successfully');
    }
  }
);

// Ou versão com Promise
await confirmChannel.publishAsync('orders', 'order.created', buffer, { persistent: true });
```

**Em Spring AMQP:** habilite com `spring.rabbitmq.publisher-confirm-type=correlated`.

### 5. Consumer acks manuais

Por default, RabbitMQ pode entregar a mensagem e considerá-la consumida imediatamente (`autoAck: true`). Se o consumer crashar antes de processar, a mensagem se perde.

**Solução:** acks manuais após processamento bem-sucedido.

```javascript
await channel.consume('order-processing', async (msg) => {
  if (!msg) return;
  try {
    await processOrder(JSON.parse(msg.content.toString()));
    channel.ack(msg);  // Confirma processamento
  } catch (err) {
    // Rejeitar e requeue (ou não — depende da estratégia)
    channel.nack(msg, false, false);  // false, false = não requeue, vai para DLX
  }
}, { noAck: false });  // IMPORTANTE: manual acks
```

### 6. Prefetch (QoS)

Limita quantas mensagens não-ack'd o consumer pode ter por vez. Sem isso, o broker entrega tudo de uma vez para o primeiro consumer (ignorando competing consumers).

```javascript
// Consumer recebe no máximo 10 mensagens por vez
await channel.prefetch(10);
```

**Recomendação:** `prefetch = concurrency` (quantas mensagens o consumer processa em paralelo). Padrão é `prefetch=1` em workers simples.

---

## Dead Letter Exchange (DLX)

Padrão crítico para production. Mensagens que falham, são rejeitadas, ou expiram são roteadas para outra exchange — a DLX — que normalmente entrega em uma "dead letter queue" (DLQ).

### Por que DLX

- **Poison messages** — mensagem que sempre falha. Sem DLX, fica em loop para sempre.
- **Expiração** — mensagens com TTL expiradas
- **Rejeição** — consumer faz `nack(msg, false, false)` (não requeue)
- **Queue cheia** — queue tem `x-max-length` e está cheia

### Configuração

```javascript
// Declarar DLX e sua queue
await channel.assertExchange('orders.dlx', 'fanout', { durable: true });
await channel.assertQueue('orders.dlq', { durable: true });
await channel.bindQueue('orders.dlq', 'orders.dlx', '');

// Queue principal configurada para enviar rejeições para a DLX
await channel.assertQueue('orders', {
  durable: true,
  arguments: {
    'x-dead-letter-exchange': 'orders.dlx',
    // Opcional: reescrever routing key ao mandar pra DLX
    'x-dead-letter-routing-key': 'failed',
    // Opcional: TTL — mensagens expiradas vão para DLX
    'x-message-ttl': 86400000  // 24h
  }
});
```

### Retries com delay via DLX

RabbitMQ não tem delay nativo de retry. Pattern clássico: usar DLX com TTL para implementar retry com delay.

```
[orders] → fail → [orders.retry.30s] (TTL=30s, DLX=orders) → expira → [orders]
```

A mensagem rejeitada vai para a retry queue, expira após 30s, e volta para a queue original via DLX.

**Implementação:**

```javascript
// Retry queue: espera 30s e volta para orders
await channel.assertQueue('orders.retry.30s', {
  durable: true,
  arguments: {
    'x-message-ttl': 30000,
    'x-dead-letter-exchange': '',  // default exchange
    'x-dead-letter-routing-key': 'orders'  // volta para orders queue
  }
});

// Consumer rejeita mandando pra retry queue
channel.publish('', 'orders.retry.30s', msg.content, {
  persistent: true,
  headers: { 'x-retry-count': (msg.properties.headers?.['x-retry-count'] || 0) + 1 }
});
channel.ack(msg);
```

Combinando múltiplas retry queues com TTLs crescentes, você implementa exponential backoff. Após N tentativas (verificando `x-retry-count`), envia para DLQ final.

### Delayed messages plugin

Alternativa mais elegante: plugin `rabbitmq_delayed_message_exchange` suporta delay nativamente.

```javascript
// Requer plugin instalado no broker
await channel.assertExchange('delayed', 'x-delayed-message', {
  durable: true,
  arguments: { 'x-delayed-type': 'direct' }
});

// Publish com delay de 30s
channel.publish('delayed', 'my.key', buffer, {
  persistent: true,
  headers: { 'x-delay': 30000 }
});
```

---

## Clustering e alta disponibilidade

RabbitMQ suporta cluster para HA e escala. A estratégia mudou ao longo do tempo.

### Mirrored Queues (legacy)

Historicamente, queues eram replicadas via **mirrored queues** — cada queue tem um master e réplicas. Caso o master cai, um mirror é promovido.

**Problemas:**
- Performance sofrível em grandes clusters
- Split-brain em network partitions
- Sincronização lenta após reconexão

**Deprecado em RabbitMQ 3.9+.** Clusters novos devem usar Quorum Queues.

### Quorum Queues (atual)

Implementação moderna baseada em **Raft consensus**. Replicação consistente, sem split-brain.

```javascript
await channel.assertQueue('orders', {
  durable: true,
  arguments: { 'x-queue-type': 'quorum' }
});
```

**Características:**
- Consistência forte (Raft)
- Tolera falha de até `(N-1)/2` nodes em cluster com N réplicas (tipicamente 3)
- Performance melhor que mirrored em grandes clusters
- Ideal para mensagens críticas que não podem ser perdidas

**Trade-offs:**
- Performance de publicação um pouco menor que queue clássica single-node
- Armazenamento baseado em memória + WAL (diferente de classic queues)
- Não suporta todas as features de classic queues (ex.: priority queues tradicionais)

### Streams (RabbitMQ 3.9+)

RabbitMQ também ganhou um tipo de queue chamado **stream**, que é essencialmente um log append-only **à la Kafka** — persistência de longa duração, múltiplos consumers com offset próprio, replay.

**Quando usar:** quando você quer recursos de event streaming mas já tem infra RabbitMQ.

**Importante:** streams **não substituem Kafka** em todos os casos — são uma adição, não o foco principal do produto. Para event streaming sério, Kafka continua sendo a escolha padrão.

### Cluster formation

Nodes do cluster conversam via Erlang distribution. Configuração típica em `rabbitmq.conf`:

```
cluster_formation.peer_discovery_backend = rabbit_peer_discovery_k8s
cluster_formation.k8s.host = kubernetes.default.svc.cluster.local
```

Para Kubernetes, existe o **RabbitMQ Cluster Operator** oficial que gerencia tudo.

---

## Patterns comuns

### Work Queue (Task Queue)

Distribuir tarefas entre múltiplos workers.

```
[Producer] → [queue] → [Worker 1] (processa task A)
                    → [Worker 2] (processa task B)
                    → [Worker 3] (processa task C)
```

- Round-robin por default
- Prefetch controla fairness
- Persistent + durable + manual ack para não perder

### Publish-Subscribe (Fanout)

Broadcast para múltiplos consumers, cada um com sua própria fila.

```
[Producer] → [Fanout Exchange] → [queue A] → [Consumer A]
                               → [queue B] → [Consumer B]
                               → [queue C] → [Consumer C]
```

### Routing (Direct Exchange)

Logs por severidade, eventos por tipo.

```
[Producer] → [Direct Exchange]
                  ├─"error"──→ [error-queue]
                  ├─"warning"→ [warning-queue]
                  └─"info"───→ [info-queue]
```

### Topics (Topic Exchange)

Eventos hierárquicos com subscrições por padrão.

```
publish routing_key="kern.critical"
    → [Topic Exchange]
          ├─"kern.*"    → [kernel-logs]
          ├─"*.critical"→ [critical-alerts]
          └─"#"         → [all-logs]
```

### RPC (Remote Procedure Call)

RabbitMQ é o único dos brokers populares que tem **RPC assíncrono bem suportado** via `reply_to` + `correlation_id`.

```
Client → publish(reply_to="cb-queue", correlation_id="req-1") → [rpc-queue]
                                                                    │
                                                                    ↓
                                                                [Server]
                                                                    │
         ←── publish(to=cb-queue, correlation_id="req-1") ──────────┘
```

**Boilerplate:**

```javascript
// Client
const cbQueue = await channel.assertQueue('', { exclusive: true });  // callback queue temporária
const correlationId = uuid();

channel.consume(cbQueue.queue, (msg) => {
  if (msg?.properties.correlationId === correlationId) {
    // recebeu a resposta
  }
}, { noAck: true });

channel.sendToQueue('rpc_queue', Buffer.from(request), {
  correlationId,
  replyTo: cbQueue.queue
});
```

**Aviso:** considere se você realmente precisa de RPC via mensageria. HTTP é mais simples para a maioria dos casos. RPC sobre mensageria faz sentido quando o client quer desacoplamento forte ou quando o server é offline frequentemente.

### Delayed Message

Via plugin `rabbitmq_delayed_message_exchange` (ver seção DLX).

---

## Spring AMQP (Spring Boot)

Integração com RabbitMQ na stack Java.

### Configuração

```yaml
# application.yml
spring:
  rabbitmq:
    host: localhost
    port: 5672
    username: guest
    password: guest
    virtual-host: /
    publisher-confirm-type: correlated
    publisher-returns: true
    listener:
      simple:
        acknowledge-mode: manual
        prefetch: 10
        concurrency: 3
        max-concurrency: 10
        retry:
          enabled: true
          initial-interval: 1000
          max-attempts: 3
          multiplier: 2.0
```

### Producer

```java
@Configuration
public class RabbitConfig {

    @Bean
    public TopicExchange ordersExchange() {
        return new TopicExchange("orders", true, false);
    }

    @Bean
    public Queue orderProcessingQueue() {
        return QueueBuilder.durable("order-processing")
            .withArgument("x-dead-letter-exchange", "orders.dlx")
            .withArgument("x-queue-type", "quorum")
            .build();
    }

    @Bean
    public Binding binding() {
        return BindingBuilder.bind(orderProcessingQueue())
            .to(ordersExchange())
            .with("order.created");
    }
}

@Service
@RequiredArgsConstructor
public class OrderPublisher {
    private final RabbitTemplate rabbit;

    public void publish(OrderEvent event) {
        rabbit.convertAndSend("orders", "order.created", event,
            message -> {
                message.getMessageProperties().setDeliveryMode(MessageDeliveryMode.PERSISTENT);
                return message;
            },
            new CorrelationData(event.getOrderId()));
    }
}
```

### Consumer

```java
@Component
public class OrderConsumer {

    @RabbitListener(queues = "order-processing")
    public void handle(OrderEvent event, Channel channel,
                       @Header(AmqpHeaders.DELIVERY_TAG) long tag) throws IOException {
        try {
            // Idempotência
            if (processedEventRepo.exists(event.getEventId())) {
                channel.basicAck(tag, false);
                return;
            }

            orderService.process(event);
            processedEventRepo.save(event.getEventId());
            channel.basicAck(tag, false);
        } catch (Exception e) {
            log.error("Failed to process event", e);
            // reject sem requeue → vai para DLX
            channel.basicNack(tag, false, false);
        }
    }
}
```

### Publisher Confirms

```java
@Component
@RequiredArgsConstructor
public class PublisherConfirmCallback implements RabbitTemplate.ConfirmCallback {

    @Override
    public void confirm(CorrelationData correlationData, boolean ack, String cause) {
        if (ack) {
            log.debug("Message confirmed: {}", correlationData.getId());
        } else {
            log.error("Message NOT confirmed: {}, cause: {}",
                correlationData.getId(), cause);
            // retry ou alertar
        }
    }
}
```

---

## Monitoring em produção

### RabbitMQ Management Plugin

Built-in, UI web na porta 15672. Habilitar:

```bash
rabbitmq-plugins enable rabbitmq_management
```

Mostra:
- Queues e tamanhos
- Exchange bindings
- Connections e channels
- Message rates (in/out, ack, deliver)
- Cluster status
- Alarms (memory, disk)

### Métricas importantes

- **Queue depth** (`messages_ready`) — crescimento contínuo = problema
- **Unacked messages** — mensagens em processamento
- **Publish rate vs deliver rate** — mismatch = consumer não acompanha
- **Connection count** — deveria ser estável
- **Memory alarm** — se atingir `vm_memory_high_watermark` (40% default), publisher blocks
- **Disk alarm** — se disk < `disk_free_limit` (50MB default), publisher blocks
- **Consumer utilization** — % do tempo que o consumer está ativo (não idle)
- **Mirroring sync status** (mirrored queues) ou **Raft term changes** (quorum queues)

### Prometheus exporter

```bash
rabbitmq-plugins enable rabbitmq_prometheus
```

Métricas expostas em `/metrics` na porta 15692. Plug direto no Prometheus + Grafana.

### Alerts típicos

- Queue depth > X por Y minutos
- DLQ com mensagens (deveria ser raro)
- Memory alarm ativo
- Disk alarm ativo
- Consumer count == 0 em queue com mensagens
- Connection count anômala
- Publisher confirms falhando

---

## RabbitMQ vs Kafka vs BullMQ

Comparação lado-a-lado — é a pergunta mais comum em entrevistas sobre mensageria.

| Aspecto | RabbitMQ | Kafka | BullMQ |
| --- | --- | --- | --- |
| **Modelo** | Message broker (queue) | Log distribuído | Job queue |
| **Persistência** | Até consumo (ou durável) | Retenção configurável | Até conclusão |
| **Replay** | Não | Sim | Não |
| **Routing** | Muito flexível (4 tipos de exchange) | Simples (topic + partition) | Por fila |
| **Throughput** | ~100K msg/s/node | Milhões msg/s | ~dezenas de milhares/s |
| **Latência** | Baixa (~ms) | Baixa (~ms) | Baixa |
| **Ordem** | Por queue | Por partição | FIFO por fila |
| **Múltiplos consumers independentes** | Via fanout + queue por consumer | Via consumer groups (natural) | Não suportado |
| **Complexidade operacional** | Média | Alta | Baixa (se já tem Redis) |
| **Linguagens** | Qualquer (AMQP) | Qualquer | Node.js only |
| **Delay/scheduling** | Via plugin | Via retry topics pattern | Nativo |
| **Priorities** | Sim (priority queue) | Não nativo | Sim |
| **RPC assíncrono** | Nativo (reply_to + correlation_id) | Manual | Não |
| **Protocol** | AMQP, MQTT, STOMP | Kafka protocol (binary) | Custom sobre Redis |
| **HA** | Quorum queues (Raft) | Replication (ISR) | Redis cluster |

### Quando escolher RabbitMQ

- **Task queues com routing complexo** (patterns, hierarquia, multi-atributo)
- **RPC assíncrono** bem suportado
- **Multi-linguagem** (Java + Python + Node.js + .NET)
- **Priority queues** (níveis de urgência)
- **Simplicidade operacional** vs Kafka (cluster RabbitMQ é mais simples de operar)
- **Sem necessidade de replay nem alto throughput** (milhões/s)
- **Workflows tradicionais** de microserviços — orquestração via filas

### Quando NÃO escolher RabbitMQ

- **Event streaming e event sourcing** → Kafka (retenção longa, replay, consumer groups)
- **Alto throughput (> 500K msg/s)** → Kafka escala melhor
- **Apenas Node.js + Redis disponível** → BullMQ é mais simples
- **Log de eventos imutável como source of truth** → Kafka

---

## Armadilhas comuns

- **Sem durable queue / persistent message** — perde mensagens em restart do broker
- **Auto-ack em produção** — consumer crash = mensagem perdida. Use manual ack.
- **Sem prefetch** — broker entrega tudo para o primeiro consumer, competing consumers quebra
- **Prefetch muito alto** — um consumer lento segura mensagens que outros poderiam processar
- **Sem DLX** — poison messages ficam em loop eterno rejeitando
- **Sem publisher confirms** — publicação silenciosa, não sabe se broker recebeu
- **Queue não durable** — perde mensagens em restart
- **Criar connection por mensagem** — connection é pesada. Reutilize (1 connection por processo, múltiplos channels).
- **Usar 1 channel para tudo** — channels são threading boundary. Use 1 por thread/consumer.
- **Não fechar channel/connection** — leak de recursos no broker
- **Consumer não idempotente** — retries causam duplicação (at-least-once garantido)
- **Ignorar memory alarm** — broker bloqueia publishers quando atinge watermark. Monitor.
- **Não monitorar queue depth** — lag cresce silenciosamente
- **Topic exchange sem pensar em bindings futuros** — adicionar bindings em produção pode causar desastre se o padrão for mal desenhado
- **Mirrored queues em produção moderna** — deprecado, use Quorum Queues
- **Fanout sem consumers** — mensagens publicadas e descartadas silenciosamente (nenhum binding casa)
- **Usar RabbitMQ como event log** — ele não é Kafka. Sem retention longa, sem replay.
- **Schema implícito** — sem schema validation, mudanças quebram consumers. Use JSON Schema ou Protobuf + validator.
- **Confundir exchange e queue** — producer publica em exchange, não em queue. Erro comum de iniciantes.
- **Não testar failure scenarios** — teste o que acontece quando broker cai, consumer crashar, network partition
- **Rotas (routing keys) gigantes** — queries custosas no exchange. Mantenha simples.

---

## Na prática (da minha experiência)

> **Projetos com RabbitMQ — task queues e workflows:**
> Usei RabbitMQ em projetos onde **task queues com routing complexo** eram a necessidade. A simplicidade conceitual (exchange → binding → queue) é vantagem quando a equipe não quer investir em aprender Kafka, e o fanout exchange resolve pub/sub de forma elegante.
>
> **Decisão de escolha entre RabbitMQ e Kafka:**
> Em cada projeto, a conversa começa com: "você precisa de replay? múltiplos consumer groups independentes? retention longa?". Se a resposta é sim para qualquer uma, Kafka. Se não, RabbitMQ é mais simples de operar e cobre o caso bem.
>
> **Padrões que sempre uso em produção:**
>
> **1. Durable + persistent + manual ack + publisher confirms + DLX** — a combinação mínima para produção séria. Sem qualquer um desses, você pode perder mensagens. Já vi equipes "descobrirem" em produção que suas queues não eram durable.
>
> **2. Quorum queues sempre** — desde que RabbitMQ 3.9 trouxe Quorum Queues, paro de usar Mirrored Queues. A consistência forte via Raft vale o pequeno custo de performance.
>
> **3. DLX desde o dia 1** — toda queue principal tem DLX configurada. Uma vez tivemos uma mensagem malformada que teria travado o processamento — foi isolada na DLQ, investigamos, corrigimos o producer, e reprocessamos manualmente.
>
> **4. Idempotência nos consumers** — at-least-once garantido. Já tive incidente onde retries após crash causaram duplicação. Depois disso, `processed_events` table em todos os consumers críticos.
>
> **5. Prefetch = concurrency** — regra simples. Workers com processamento pesado ficam com prefetch baixo (1-5). Workers com processamento leve podem ter prefetch alto (50-100).
>
> **6. Management UI protegido** — `default` user com acesso a tudo é padrão de fábrica. Sempre remover em produção e criar users com permissões mínimas por vhost.
>
> **Incidente memorável:** RabbitMQ atingiu memory alarm porque um consumer crashou silenciosamente e a queue cresceu por horas. Publishers começaram a ser bloqueados e a API toda ficou lenta. Lesson learned: monitor de memory alarm + alert de consumer count == 0 em queues críticas.
>
> **Outro incidente:** mensagens eram publicadas com `persistent=true`, queue era `durable=true`, mas o exchange foi criado com `durable=false` (erro em script de provisioning). Em restart, o exchange sumiu, todos os bindings sumiram junto, e mensagens published voltavam a erro "exchange not found". Lesson learned: **tudo** precisa ser durable, e teste scenarios de restart.
>
> **A lição principal:** RabbitMQ é maduro, bem documentado, e tem features suficientes para a maioria dos casos de task queue e pub/sub clássico. Para workflows tradicionais de microserviços sem necessidades extremas de throughput ou replay, é frequentemente a escolha certa — mais simples que Kafka e mais poderoso que BullMQ. Mas requer disciplina com garantias de durabilidade e padrões de DLX — sem isso, você terá incidentes.

---

## How to explain in English

> "RabbitMQ is a traditional message broker based on AMQP. It's my default choice when I need flexible routing, priority queues, or complex workflows, and when the use case is task processing rather than event streaming.
>
> The mental model is exchange → binding → queue → consumer. Producers publish to an exchange, not directly to a queue, and the exchange decides — via bindings — which queues receive the message. This indirection is what gives RabbitMQ its routing flexibility. There are four exchange types: direct for exact key match, fanout for broadcast, topic for pattern matching with wildcards, and headers for match by headers. Topic exchange is my default because it can imitate the others.
>
> For production durability, you need a combination of configurations: durable exchanges, durable queues, persistent messages, publisher confirms, and manual consumer acks. If any of these is missing, you can lose messages. I always configure a Dead Letter Exchange for every critical queue so that poison messages or failed deliveries don't cause infinite loops — they get isolated in a DLQ for investigation.
>
> For high availability, I use Quorum Queues, which are the modern replacement for Mirrored Queues. They use Raft consensus for strong consistency and handle network partitions gracefully. Mirrored Queues are deprecated and should not be used in new clusters.
>
> The decision between RabbitMQ and Kafka comes down to the use case. If you need event replay, long retention, or multiple independent consumer groups reading the same events, Kafka is the right choice. If you need flexible routing, priority queues, RPC, or simpler operations, RabbitMQ is better. For Node.js only projects with simple background jobs, BullMQ is even simpler.
>
> Finally, like all at-least-once messaging systems, consumers must be idempotent. I use a processed events table or natural idempotency of operations to handle redelivery after crashes or rebalances."

### Frases úteis em entrevista

- "RabbitMQ is a traditional message broker based on AMQP — exchange, binding, queue, consumer."
- "My default exchange type is topic because it can imitate the others."
- "For production durability, you need durable exchanges, durable queues, persistent messages, publisher confirms, and manual acks."
- "Every critical queue has a Dead Letter Exchange configured — poison messages shouldn't cause infinite loops."
- "I use Quorum Queues for HA. Mirrored Queues are deprecated in modern RabbitMQ."
- "Prefetch controls fairness between competing consumers — typically set to match worker concurrency."
- "I choose RabbitMQ over Kafka when I need flexible routing and don't need event replay or massive throughput."
- "Consumer idempotency is mandatory — at-least-once delivery means duplicates will happen."
- "The reply_to + correlation_id pattern makes RabbitMQ uniquely good at RPC among message brokers."

### Key vocabulary

- corretor de mensagens → message broker
- troca → exchange
- vínculo → binding
- fila → queue
- chave de roteamento → routing key
- host virtual → virtual host (vhost)
- conexão → connection
- canal → channel
- fila durável → durable queue
- mensagem persistente → persistent message
- confirmações do publicador → publisher confirms
- confirmação manual → manual acknowledgment (ack)
- rejeição → negative acknowledgment (nack) / reject
- fila de mensagens mortas → dead letter queue (DLQ)
- troca de mensagens mortas → dead letter exchange (DLX)
- consenso Raft → Raft consensus
- fila de quórum → quorum queue
- fila espelhada → mirrored queue (legacy)
- tempo de vida da mensagem → message TTL
- busca prévia → prefetch (QoS)
- consumidores competidores → competing consumers
- leque → fanout
- tópico → topic
- direto → direct
- cabeçalhos → headers

---

## Recursos

### Documentação

- [RabbitMQ Documentation](https://www.rabbitmq.com/docs) — documentação oficial
- [RabbitMQ Tutorials](https://www.rabbitmq.com/tutorials) — tutoriais em múltiplas linguagens (Java, Python, Node.js, .NET, Go...)
- [AMQP 0.9.1 Specification](https://www.rabbitmq.com/specification.html) — o protocolo

### Livros

- *RabbitMQ in Depth* — Gavin M. Roy (o livro essencial)
- *Learning RabbitMQ* — Martin Toshev
- *Enterprise Integration Patterns* — Gregor Hohpe (os patterns clássicos que RabbitMQ implementa)

### Artigos e guias

- [Reliability Guide — RabbitMQ](https://www.rabbitmq.com/reliability.html) — garantias de entrega em detalhe
- [Quorum Queues — RabbitMQ](https://www.rabbitmq.com/quorum-queues.html)
- [RabbitMQ Streams — Overview](https://www.rabbitmq.com/streams.html)
- [Publisher Confirms — RabbitMQ](https://www.rabbitmq.com/confirms.html)
- [CloudAMQP Blog](https://www.cloudamqp.com/blog/) — RabbitMQ em profundidade, production tips
- [RabbitMQ Best Practices (CloudAMQP)](https://www.cloudamqp.com/blog/part1-rabbitmq-best-practice.html)
- [Spring AMQP Reference](https://docs.spring.io/spring-amqp/reference/) — integração com Spring

### Ferramentas

- [RabbitMQ Management Plugin](https://www.rabbitmq.com/management.html) — UI web built-in
- [Perf Test](https://www.rabbitmq.com/java-tools.html) — benchmark tool oficial
- [Delayed Message Exchange Plugin](https://github.com/rabbitmq/rabbitmq-delayed-message-exchange)
- [RabbitMQ Cluster Operator (Kubernetes)](https://www.rabbitmq.com/kubernetes/operator/operator-overview.html)
- [amqplib](https://github.com/amqp-node/amqplib) — client Node.js mais popular
- [pika](https://github.com/pika/pika) — client Python
- [Spring AMQP](https://spring.io/projects/spring-amqp) — client Java/Spring

---

## Veja também

- [[Mensageria]] — contexto geral, quando usar cada broker
- [[03-Dominios/Arquitetura/Mensageria/Kafka]] — alternativa para event streaming
- [[BullMQ]] — alternativa para Node.js com Redis
- [[Event Streaming]] — quando RabbitMQ NÃO é a escolha
- [[System Design]] — usando RabbitMQ em system design
- [[Arquitetura de Software]] — patterns de integração
- [[Spring Boot]] — integração via Spring AMQP
- [[Node.js]] — integração via amqplib
- [[API Design]] — operações assíncronas, webhooks
