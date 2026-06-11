---
title: "Spring AMQP e RabbitMQ"
created: 2026-06-11
updated: 2026-06-11
type: concept
status: seedling
publish: true
fase: adepto
tags:
  - java
  - mensageria
  - adepto
  - rabbitmq
  - amqp
aliases:
  - "RabbitMQ"
---

# Spring AMQP e RabbitMQ

> [!abstract] TL;DR
> Spring AMQP é o cliente idiomático do Spring para RabbitMQ. O modelo central é **exchange → binding → queue**: o produtor nunca fala com a fila diretamente — ele publica em uma exchange, que roteia para zero ou mais filas via binding. `RabbitTemplate` produz mensagens; `@RabbitListener` consome. Quorum queues são a recomendação atual do RabbitMQ para filas duráveis e replicadas; Streams habilitam replay multi-consumidor sem destruir mensagens.

## O que é

**Spring AMQP** é o projeto do ecossistema Spring que fornece abstrações de alto nível sobre o protocolo AMQP 0-9-1, implementado principalmente pelo RabbitMQ. Ele oferece:

- `RabbitTemplate` — envio e recebimento síncrono de mensagens;
- `@RabbitListener` — consumo assíncrono orientado a anotações;
- `RabbitAdmin` — gerenciamento programático de exchanges, filas e bindings;
- Integração automática no Spring Boot 3.x via `spring-boot-starter-amqp`.

A versão corrente estável é **Spring AMQP 4.1 / Spring Boot 3.x** (linha 3.2.x também recebe suporte).

## Por que importa

RabbitMQ é amplamente adotado quando o sistema precisa de **roteamento rico de mensagens**: filtrar por assunto, fazer fan-out para múltiplos consumidores, ou balancear carga entre workers. Suas diferenças em relação ao Kafka são estruturais, e entendê-las é pré-requisito para escolher o broker certo — tema recorrente em entrevistas de nível sênior.

Além disso, quorum queues e Streams são funcionalidades modernas do RabbitMQ que o aproximam de casos de uso antes exclusivos do Kafka (durabilidade forte, replay), tornando o conhecimento ainda mais relevante para o dia a dia.

## Como funciona

### O modelo AMQP — exchange → binding → queue

No AMQP, o produtor **nunca publica diretamente em uma fila**. O fluxo é:

```
Produtor → Exchange → Binding (routing key) → Queue → Consumidor
```

| Componente | Papel |
|---|---|
| **Exchange** | Recebe a mensagem e decide para quais filas encaminhá-la |
| **Binding** | Regra que liga uma exchange a uma fila (com critério opcional) |
| **Routing key** | Rótulo enviado pelo produtor junto com a mensagem |
| **Queue** | Buffer onde a mensagem aguarda o consumidor |

#### Tipos de exchange

| Tipo | Roteamento |
|---|---|
| **direct** | Encaminha quando a routing key da mensagem é exatamente igual à routing key do binding. Ideal para work queues ponto a ponto. |
| **topic** | Aceita routing keys com curingas: `*` (uma palavra) e `#` (zero ou mais). Ex.: `order.#` casa `order.created`, `order.paid.confirmed`. |
| **fanout** | Ignora completamente a routing key e envia para **todas** as filas vinculadas. Ideal para broadcast/pub-sub. |
| **headers** | Roteia com base nos headers da mensagem em vez da routing key. Pouco usado na prática. |

> [!tip] Default exchange
> O RabbitMQ cria automaticamente uma exchange `direct` chamada `""` (string vazia). Toda fila é vinculada a ela com binding key igual ao próprio nome da fila — por isso `rabbitTemplate.convertAndSend("nomeDaFila", payload)` funciona sem configurar nada.

### RabbitTemplate e @RabbitListener

#### Produzindo mensagens

`RabbitTemplate` é o ponto central de envio. O método mais comum no dia a dia é `convertAndSend`, que converte o objeto Java para `Message` usando o `MessageConverter` configurado (padrão: `SimpleMessageConverter` — serializa `String` e `Serializable`; substitua por `Jackson2JsonMessageConverter` para JSON):

```java
@Service
public class PedidoProdutor {

    private final RabbitTemplate rabbitTemplate;

    public PedidoProdutor(RabbitTemplate rabbitTemplate) {
        this.rabbitTemplate = rabbitTemplate;
    }

    public void publicar(PedidoCriadoEvent evento) {
        // exchange + routing key explícitos
        rabbitTemplate.convertAndSend("pedidos.topic", "pedido.criado", evento);
    }
}
```

Para mensagens de baixo nível (byte array + `MessageProperties`), use `send()`:

```java
rabbitTemplate.send("pedidos.topic", "pedido.criado",
    new Message("hello".getBytes(), new MessageProperties()));
```

#### Consumindo com @RabbitListener

```java
@Component
public class PedidoConsumidor {

    @RabbitListener(queues = "pedidos.criados.queue")
    public void handle(PedidoCriadoEvent evento) {
        // AUTO ack: Spring confirma automaticamente após o método retornar
        System.out.println("Processando pedido: " + evento.id());
    }
}
```

#### Modos de acknowledgment

| Modo | Comportamento |
|---|---|
| **AUTO** (padrão) | Spring faz `basicAck` após retorno sem exceção; nack automático se o método lançar exceção. |
| **MANUAL** | O método recebe `Channel` e chama `basicAck` / `basicNack` explicitamente. |
| **NONE** | Broker considera toda mensagem confirmada assim que entregue ("fire-and-forget"). |

Ack manual:

```java
@RabbitListener(queues = "pedidos.criados.queue",
                ackMode = "MANUAL")
public void handle(PedidoCriadoEvent evento,
                   Channel channel,
                   @Header(AmqpHeaders.DELIVERY_TAG) long deliveryTag) throws IOException {
    try {
        processar(evento);
        channel.basicAck(deliveryTag, false);
    } catch (Exception e) {
        // false = não requeue (manda para DLX se configurada)
        channel.basicNack(deliveryTag, false, false);
    }
}
```

Configuração via `application.yml`:

```yaml
spring:
  rabbitmq:
    host: localhost
    port: 5672
    username: guest
    password: guest
    listener:
      simple:
        acknowledge-mode: AUTO          # AUTO | MANUAL | NONE
        prefetch: 10                    # mensagens não confirmadas por consumidor
        default-requeue-rejected: false # false → vai para DLX em vez de loop
```

### Quorum queues e Streams

#### Quorum queues

Quorum queues são o tipo de fila **recomendado pelo RabbitMQ** para cenários que exigem durabilidade e alta disponibilidade. São baseadas no algoritmo **Raft** e replicam mensagens em um quorum de nós antes de confirmar ao produtor (via publisher confirms).

Características chave (fonte: documentação oficial RabbitMQ):
- Sempre duráveis — não existem quorum queues transientes;
- Replicação antes de confirmar ao produtor com `publisher confirms`;
- Tratamento nativo de **poison messages** (dead-letter automático após N tentativas);
- Requerem mínimo **3 nós** para tolerância a falhas real;
- Latência maior que classic queues devido ao overhead do consenso;
- Não suportam exclusive queues nem prefetch global (global QoS).

Declarando no Spring AMQP:

```java
@Bean
public Queue pedidosQueue() {
    return QueueBuilder.durable("pedidos.criados.queue")
        .quorum()          // x-queue-type: quorum
        .build();
}
```

#### Streams

Streams são **logs append-only persistentes e replicados** — o modelo é idêntico ao do Kafka. Diferença central em relação às filas: a semântica é **não-destrutiva** — mensagens não são removidas após o consumo; múltiplos consumidores podem ler os mesmos dados a partir de qualquer offset.

Casos de uso típicos (fonte: documentação oficial RabbitMQ):
- **Large fan-out**: muitos consumidores sem precisar de uma fila por consumidor;
- **Replay**: re-consumir mensagens a partir de timestamp ou offset;
- **Grandes backlogs**: eficiência superior às filas clássicas para acúmulo de milhões de mensagens.

Limitações: não suportam TTL de mensagem, Dead Letter Exchange, priority queuing nem configuração transiente.

## Na prática

Exemplo completo de configuração de exchange, queue, binding e listener para um domínio de pedidos:

```java
@Configuration
public class MensageriaConfig {

    // Exchange do tipo topic
    @Bean
    public TopicExchange pedidosExchange() {
        return new TopicExchange("pedidos.topic");
    }

    // Fila quorum durável
    @Bean
    public Queue pedidosCriadosQueue() {
        return QueueBuilder.durable("pedidos.criados.queue")
            .quorum()
            .build();
    }

    // Binding: routing key "pedido.criado" → fila
    @Bean
    public Binding pedidosCriadosBinding(Queue pedidosCriadosQueue,
                                         TopicExchange pedidosExchange) {
        return BindingBuilder.bind(pedidosCriadosQueue)
            .to(pedidosExchange)
            .with("pedido.criado");
    }

    // Converter JSON (necessário para objetos não-String)
    @Bean
    public MessageConverter jsonMessageConverter() {
        return new Jackson2JsonMessageConverter();
    }

    @Bean
    public AmqpTemplate amqpTemplate(ConnectionFactory connectionFactory) {
        RabbitTemplate template = new RabbitTemplate(connectionFactory);
        template.setMessageConverter(jsonMessageConverter());
        return template;
    }
}
```

```yaml
# application.yml
spring:
  rabbitmq:
    host: localhost
    port: 5672
    username: guest
    password: guest
    listener:
      simple:
        acknowledge-mode: AUTO
        prefetch: 10
        default-requeue-rejected: false
```

Consumidor com `@RabbitListener`:

```java
@Component
public class PedidoConsumidor {

    @RabbitListener(queues = "pedidos.criados.queue")
    public void handle(PedidoCriadoEvent evento) {
        // lógica de negócio
    }
}
```

## Kafka vs RabbitMQ — quando usar cada um

| Critério | RabbitMQ (AMQP) | Kafka |
|---|---|---|
| **Modelo de roteamento** | Rico: exchange + routing key (direct/topic/fanout/headers) | Simples: tópico + partição |
| **Persistência pós-consumo** | Mensagem deletada após ack (fila) | Log imutável; retention configurável |
| **Replay** | Não nativo em filas; suportado em Streams | Nativo (offset rewind) |
| **Throughput** | Alto, mas inferior ao Kafka em escala extrema | Muito alto (otimizado para batch/log) |
| **Complexidade operacional** | Menor para clusters pequenos | Maior (Zookeeper/KRaft, partições) |
| **Ideal para** | Roteamento fino, work queues, RPC assíncrono | Event streaming, auditoria, analytics |

> [!tip] Regra de bolso
> Se a pergunta for "quem deve processar esta mensagem e de que forma?", use RabbitMQ. Se a pergunta for "o que aconteceu no sistema?", use Kafka.

## Armadilhas

### (1) Requeue infinito — o poison message em loop

Com `default-requeue-rejected=true` (padrão), qualquer exceção não tratada faz a mensagem voltar ao início da fila. Se o erro for determinístico (ex.: payload inválido), a mensagem vai girar indefinidamente, sobrecarregando consumidores.

**Solução**: configure `default-requeue-rejected=false` e combine com uma Dead Letter Exchange (DLX). Assim, após a rejeição, a mensagem vai para a DLQ em vez de loopear. Quorum queues oferecem `delivery-limit` (ex.: `x-delivery-limit: 3`) que envia para DLX após N tentativas automaticamente.

```java
@Bean
public Queue pedidosQueue() {
    return QueueBuilder.durable("pedidos.criados.queue")
        .quorum()
        .deliveryLimit(3)                          // poison message → DLX após 3 tentativas
        .deadLetterExchange("pedidos.dlx")
        .build();
}
```

### (2) Fanout achando que filtra por routing key

Exchange `fanout` **ignora completamente a routing key**. Um erro comum é publicar com routing key `"admin"` esperando que só filas vinculadas com essa key recebam a mensagem — mas em fanout, **todas** as filas vinculadas recebem tudo.

Use `direct` ou `topic` quando precisar de filtragem. Reserve `fanout` para broadcast puro (ex.: invalidação de cache em todos os nós).

### (3) Confundir o modelo de roteamento AMQP com partições do Kafka

No Kafka, o roteamento é por **partição** (baseado em chave hash ou round-robin), e um consumidor por partição garante ordenação. No AMQP, o roteamento é por **exchange + binding**, e múltiplos consumidores concorrem pela mesma fila (work queue).

Tentar replicar o modelo de "consumidor dedicado por partição" do Kafka em RabbitMQ é over-engineering. Use as primitivas do AMQP do jeito que foram desenhadas.

## Em entrevista

**Frases em inglês prontas para uso:**

1. *"In AMQP, producers never publish directly to a queue — they send to an exchange, and the exchange routes to queues based on bindings and routing keys."*
2. *"Fanout exchanges broadcast to every bound queue regardless of routing key, so if you need filtering, you want direct or topic instead."*
3. *"With `default-requeue-rejected=true`, a poison message will spin indefinitely; setting it to `false` and wiring a dead-letter exchange is the safe default."*
4. *"Quorum queues use the Raft consensus algorithm, which means a message is only confirmed to the producer once a majority of nodes have persisted it — strong durability at the cost of some latency."*
5. *"RabbitMQ Streams give you Kafka-like replay semantics within RabbitMQ: messages aren't deleted after consumption, and consumers can seek to any offset or timestamp."*

**Vocabulário essencial:**

| Termo | Significado |
|---|---|
| **exchange** | Ponto de entrada de mensagens; decide o roteamento |
| **binding** | Regra que conecta exchange à fila (com routing key opcional) |
| **routing key** | Rótulo da mensagem usado pelo roteamento direct/topic |
| **ack / nack** | Confirmação positiva / negativa de processamento ao broker |
| **requeue** | Devolver a mensagem ao início da fila após nack |
| **dead-letter exchange (DLX)** | Exchange destino de mensagens rejeitadas ou expiradas |
| **quorum queue** | Fila replicada via Raft; substitui mirrored queues |
| **publisher confirms** | Mecanismo de confirmação do broker ao produtor após persistência |

## Veja também

- [[03-Dominios/Java/Mensageria/Mensageria|MOC — Mensageria na JVM]]
- [[03-Dominios/Java/Java|Trilha Java Sênior]]
- [[03-Dominios/Java/Mensageria/04 - O ecossistema de brokers na JVM|O ecossistema de brokers]]
- [[03-Dominios/Java/Mensageria/12 - Dead Letter Topic — o padrão DLQ|Dead Letter Topic]]
- [[03-Dominios/Java/Mensageria/02 - Os modelos de mensageria — queue vs topic|Queue vs topic]]
- [[03-Dominios/Java/Dicionário de Java|Dicionário de Java]]

## Referências

- [Spring AMQP Reference Documentation](https://docs.spring.io/spring-amqp/reference/) — versão 4.1.0 (3.2.x também suportada)
- [RabbitMQ: Quorum Queues](https://www.rabbitmq.com/docs/quorum-queues)
- [RabbitMQ: Streams](https://www.rabbitmq.com/docs/streams)
- [Spring Boot AMQP Auto-configuration](https://docs.spring.io/spring-boot/reference/messaging/amqp.html)
