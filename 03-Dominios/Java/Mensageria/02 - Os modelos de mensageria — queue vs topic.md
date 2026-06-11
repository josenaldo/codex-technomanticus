---
title: "Os modelos de mensageria — queue vs topic"
created: 2026-06-11
updated: 2026-06-11
type: concept
status: seedling
publish: true
fase: iniciado
tags:
  - java
  - mensageria
  - iniciado
aliases:
  - "Point-to-point vs Publish-Subscribe"
---

# Os modelos de mensageria — queue vs topic

> [!abstract] TL;DR
> Há dois modelos fundamentais de entrega de mensagens: **point-to-point (fila)**, onde cada mensagem é consumida por exatamente um consumidor, e **publish-subscribe (tópico)**, onde cada assinante recebe sua própria cópia. RabbitMQ implementa os dois via exchanges e filas com semântica push; Kafka os combina nativamente via consumer groups com semântica pull. JMS é a spec histórica Jakarta para brokers tradicionais — Kafka e RabbitMQ não implementam JMS.

## O que é

Mensageria assíncrona se baseia em dois contratos de entrega fundamentais, cada um com garantias diferentes sobre *quem* recebe *o quê*:

**Point-to-point (fila / queue)**: uma mensagem publicada é entregue a **um único consumidor**. Se vários consumidores escutam a mesma fila, o broker distribui as mensagens entre eles — um padrão chamado *competing consumers*. Pense numa fila de atendimento: o próximo da fila vai para o caixa que ficar livre primeiro.

**Publish-subscribe (tópico / topic)**: uma mensagem publicada é entregue a **todos os assinantes independentes**. Cada assinante recebe sua própria cópia. Pense num boletim informativo: todo assinante recebe o mesmo email, e a leitura de um não remove o email dos outros.

Esses dois modelos não são exclusivos de um broker. RabbitMQ implementa os dois por meio de tipos de exchange. Kafka os combina dentro da mesma abstração de tópico, usando *consumer groups*.

## Por que importa

A escolha do modelo define o comportamento de todo o sistema downstream:

- **Fila (point-to-point)** é a escolha natural para **work queues**: processar um pedido, cobrar um pagamento, enviar um email transacional. A semântica garante que o trabalho não seja feito em duplicata por múltiplos workers.
- **Tópico (pub-sub)** é a escolha natural para **eventos de domínio**: "Pedido foi criado" precisa ser consumido pelo serviço de estoque *e* pelo serviço de notificações *e* pelo serviço de analytics — cada um de forma independente.
- Escolher o modelo errado leva a bugs sutis: usar pub-sub onde queria competing consumers faz o trabalho ser executado N vezes; usar fila onde queria broadcast impede que serviços independentes recebam o mesmo evento.

## Como funciona

### Point-to-point (queue)

Numa fila clássica, o broker retém a mensagem até que um consumidor a receba e a confirme (acknowledge). Se múltiplos consumidores escutam a mesma fila, o broker entrega cada mensagem a **um único consumidor disponível** — geralmente round-robin ou ao primeiro a pedir. Isso é o padrão **competing consumers**.

O efeito prático do competing consumers é escala horizontal de throughput: se o processamento de uma mensagem leva 1 segundo e chegam 100 mensagens por segundo, basta adicionar consumidores para manter o ritmo — sem alteração no produtor ou na estrutura da fila.

No RabbitMQ, o roteamento de filas passa por um **exchange**. O exchange do tipo `direct` ou `fanout` decide para quais filas a mensagem vai. A fila em si é FIFO e entrega cada mensagem a exatamente um consumidor.

```text
Producer → Exchange → Queue → Consumer A
                             (Consumer B fica idle ou recebe a próxima)
```

### Publish-subscribe (topic)

No modelo pub-sub, cada assinante mantém seu próprio cursor de leitura. Uma mensagem publicada é entregue a **todos os grupos de consumidores cadastrados**, de forma independente. O avanço de leitura de um assinante não afeta os demais.

No Kafka, o **consumer group** é a unidade que combina os dois modelos:

- Consumidores no **mesmo group** competem pelas partições do tópico — semântica de fila dentro do grupo.
- Consumidores em **groups diferentes** são completamente independentes — semântica pub-sub entre grupos.

Isso permite, por exemplo, que o serviço de `Shipment` e o serviço de `Payment` consumam o mesmo tópico `order.created` de forma independente, enquanto cada serviço escala horizontalmente com múltiplos workers dentro do seu próprio group.

```text
Producer → Topic (partições) → Group A: Consumer A1, A2 (competing)
                             → Group B: Consumer B1 (independente)
```

No RabbitMQ, pub-sub é implementado com um exchange do tipo `fanout`: o exchange copia a mensagem para **todas as filas vinculadas** a ele. Cada serviço assinante cria sua própria fila e a vincula ao exchange.

### Push vs pull

**RabbitMQ usa push**: o broker entrega ativamente as mensagens aos consumidores registrados assim que ficam disponíveis. O consumidor não precisa perguntar — o broker empurra até o limite de prefetch configurado. Isso reduz latência, mas exige que o consumidor gerencie o backpressure.

**Kafka usa pull**: o consumidor chama `poll()` em loop para buscar mensagens do broker. O broker nunca empurra. Isso dá ao consumidor controle total sobre o ritmo de consumo — útil quando o processamento é variável ou sujeito a picos. O tradeoff é que o consumidor precisa de um loop ativo.

```java
// Kafka — semântica pull explícita
while (true) {
    ConsumerRecords<String, String> records = consumer.poll(Duration.ofMillis(100));
    for (ConsumerRecord<String, String> record : records) {
        process(record);
    }
}
```

**JMS (Jakarta Messaging)**: a spec histórica da plataforma Jakarta (antes Java EE) para mensageria em brokers tradicionais como ActiveMQ e IBM MQ. JMS define `Queue` e `Topic` como tipos explícitos da API. **Kafka e RabbitMQ não implementam JMS** — cada um tem sua própria API cliente. Spring abstrai parte disso via `JmsTemplate` (JMS), `RabbitTemplate` (RabbitMQ) e `KafkaTemplate` (Kafka), mas as semânticas subjacentes diferem.

## Na prática

**Cenário 1 — Competing consumers para processar pedidos**

Cada pedido deve ser processado por exatamente um worker. Uma fila garante isso:

```java
// Spring AMQP (RabbitMQ) — competing consumers
@RabbitListener(queues = "order.processing")
public void processOrder(Order order) {
    // somente UM worker recebe este pedido
    paymentService.charge(order);
}
```

Escalar para 3 workers significa 3 instâncias do listener na mesma fila — o throughput triplica sem risco de processamento duplicado.

**Cenário 2 — Pub-sub para evento de domínio**

Quando um `Order` é criado, múltiplos serviços precisam reagir de forma independente:

```java
// Spring Kafka — produtor publica no tópico
kafkaTemplate.send("order.created", order.getId().toString(), order);

// Consumer Group: shipment-service
@KafkaListener(topics = "order.created", groupId = "shipment-service")
public void onOrderCreated(Order order) {
    shipmentService.reserveStock(order);
}

// Consumer Group: notification-service (independente do anterior)
@KafkaListener(topics = "order.created", groupId = "notification-service")
public void onOrderCreated(Order order) {
    notificationService.sendConfirmation(order);
}
```

Ambos os grupos consomem o mesmo evento; o progresso de um não afeta o outro.

**Cenário 3 — Fanout exchange no RabbitMQ para broadcast**

```java
// RabbitMQ com fanout exchange
// Payment confirmado → notifica estoque E analytics simultaneamente
rabbitTemplate.convertAndSend("payment.confirmed.fanout", "", paymentEvent);
// Cada serviço tem sua própria fila vinculada ao exchange
```

## Armadilhas

### (1) Usar topic onde queria competing consumers

Se múltiplos workers do mesmo serviço escutam tópicos Kafka mas estão em **consumer groups diferentes**, cada worker recebe **todas** as mensagens — o trabalho é executado N vezes.

```java
// ERRADO: dois grupos distintos para o mesmo serviço
@KafkaListener(topics = "payment.process", groupId = "payment-worker-1")
@KafkaListener(topics = "payment.process", groupId = "payment-worker-2")
// Resultado: cada pagamento é cobrado DUAS vezes
```

A correção é usar o **mesmo** `groupId` para todos os workers do mesmo serviço — Kafka distribui as partições entre eles automaticamente.

### (2) Assumir ordering global num topic particionado

Kafka garante ordem **dentro de uma partição**, não entre partições. Se um tópico tem 3 partições e você publica `OrderCreated` e `OrderCancelled` para o mesmo pedido sem garantir que vão para a mesma partição (via `key`), o consumidor pode processar o cancelamento antes da criação.

A solução: usar o `orderId` (ou a entidade raiz) como chave de particionamento. Mensagens com a mesma chave sempre vão para a mesma partição, preservando a ordem por entidade.

```java
// Garante ordering para o mesmo pedido
kafkaTemplate.send("order.events", order.getId().toString(), event);
//                                  ^^^^^^^^^^^^^^^^^^^^ chave de partição
```

## Em entrevista

### Frase pronta (inglês)

"There are two fundamental messaging models: point-to-point queues, where each message is consumed by exactly one consumer, and publish-subscribe topics, where every independent subscriber receives its own copy. RabbitMQ implements both through exchange types — fanout for broadcast, direct/topic for routing — and uses a push model to deliver messages. Kafka unifies both models through consumer groups: consumers within the same group compete for partitions like a queue, while different groups each receive all messages independently like pub-sub, with consumers pulling via poll. JMS is the historical Jakarta spec for traditional brokers; Kafka and RabbitMQ have their own APIs and do not implement JMS."

### Vocabulário

| Português                     | English                        |
| ----------------------------- | ------------------------------ |
| Fila                          | Queue                          |
| Tópico                        | Topic                          |
| Consumidor concorrente        | Competing consumer             |
| Difusão / transmissão ampla   | Broadcast                      |
| Assinante                     | Subscriber                     |
| Entrega                       | Delivery / message delivery    |
| Grupo de consumidores         | Consumer group                 |
| Partição                      | Partition                      |
| Exchange (RabbitMQ)           | Exchange                       |
| Modelo de push / pull         | Push model / pull model        |

## Veja também

- [[03-Dominios/Java/Mensageria/index|Mensageria (MOC do galho)]]
- [[03-Dominios/Java/index|Trilha Java]]
- [[03-Dominios/Java/Mensageria/01 - O que é mensageria e arquitetura orientada a eventos|O que é mensageria]]
- [[03-Dominios/Java/Mensageria/04 - O ecossistema de brokers na JVM|O ecossistema de brokers]]
- [[03-Dominios/Java/Dicionário de Java|Dicionário de Java]]

## Referências

- RabbitMQ — Queues: <https://www.rabbitmq.com/docs/queues> (consultado em 2026-06-11)
- RabbitMQ — Exchanges: <https://www.rabbitmq.com/docs/exchanges> (consultado em 2026-06-11)
- Apache Kafka — Introduction: <https://kafka.apache.org/intro> (consultado em 2026-06-11)
