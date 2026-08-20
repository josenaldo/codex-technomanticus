---
title: "Spring para mensageria — o panorama"
created: 2026-06-11
updated: 2026-06-11
type: concept
status: seedling
publish: true
fase: Iniciado
tags:
  - java
  - mensageria
  - iniciado
  - spring-kafka
aliases:
  - "Spring messaging overview"
---

# Spring para mensageria — o panorama

> [!abstract] TL;DR
> O ecossistema Spring oferece três projetos complementares para mensageria: **Spring Kafka** (cliente idiomático para Apache Kafka), **Spring AMQP** (cliente para RabbitMQ via protocolo AMQP) e **Spring Cloud Stream** (abstração de mais alto nível que cobre ambos e outros brokers com modelo funcional). Escolher a camada certa evita over-engineering e dependências desnecessárias.

## O que é

Quando um projeto Spring precisa se comunicar de forma assíncrona por mensagens, há mais de um caminho. O ecossistema oferece projetos em diferentes níveis de abstração:

| Projeto | Nível | Broker(s) primário(s) |
|---|---|---|
| Spring for Apache Kafka | Cliente direto | Apache Kafka |
| Spring AMQP | Cliente direto | RabbitMQ (AMQP 0-9-1 e 1.0) |
| Spring Cloud Stream | Abstração de binders | Kafka, RabbitMQ, Pulsar, Kinesis… |
| Spring Integration | Framework EIP | Qualquer canal/adapter |

**Spring Integration** implementa os padrões de integração empresarial (EIP) de Gregor Hohpe — pipes, filtros, routers, transformadores — e é o projeto mais antigo e abrangente. Ele não tem nota dedicada neste galho, mas vale saber que existe; o restante do galho foca nos três primeiros.

## Por que importa

Toda plataforma de mensageria expõe uma API de baixo nível (producer/consumer Kafka, channel AMQP) que pode ser usada diretamente. O Spring adiciona:

- **Gerenciamento de ciclo de vida** — contêineres de listener que sobem e descem com o contexto.
- **Conversão de mensagens** — serialização/desserialização automática de objetos Java.
- **Integração com transações** — coordenação com `@Transactional`.
- **Tratamento de erros padronizado** — dead-letter topics/queues, retry declarativo.
- **Observabilidade** — métricas Micrometer sem instrumentação manual.

Escolher a abstração errada tem custo real:
- Usar Spring Cloud Stream quando você só precisa de Kafka adiciona dependências, configuração extra e um modelo mental mais complexo.
- Usar o cliente Kafka bruto quando você quer suportar dois brokers duplica código de infraestrutura.

## Como funciona

### Spring Kafka

Spring for Apache Kafka (versão estável atual: 4.1.x; compatível com Spring Boot 3.x/Java 17+) aplica os padrões do Spring ao produtor e consumidor Kafka nativos.

**KafkaTemplate** encapsula o `KafkaProducer` e fornece métodos síncronos e assíncronos para envio:

```java
// Envio simples
kafkaTemplate.send("meu-topico", "chave", payload);

// Envio com callback
kafkaTemplate.send("meu-topico", payload)
    .whenComplete((result, ex) -> {
        if (ex != null) log.error("Falha no envio", ex);
    });
```

**@KafkaListener** transforma um método em consumidor gerenciado pelo contêiner de listener:

```java
@KafkaListener(topics = "meu-topico", groupId = "meu-grupo")
public void consumir(String mensagem, @Header(KafkaHeaders.RECEIVED_KEY) String chave) {
    // processa mensagem
}
```

O contêiner gerencia threads, rebalanceamento de partições, confirmação de offset e retry com dead-letter topic (DLT).

### Spring AMQP

Spring AMQP (versão estável atual: 4.1.x) aplica o mesmo padrão ao protocolo AMQP, tendo RabbitMQ como implementação de referência. Suporta também AMQP 1.0 e RabbitMQ Streams.

**RabbitTemplate** é o equivalente ao `KafkaTemplate` para o mundo AMQP:

```java
// Envio para exchange com routing key
rabbitTemplate.convertAndSend("minha-exchange", "routing.key", payload);

// Request/Reply síncrono
RespostaDto resposta = (RespostaDto)
    rabbitTemplate.convertSendAndReceive("exchange", "rk", pedido);
```

**@RabbitListener** marca métodos consumidores:

```java
@RabbitListener(queues = "minha-fila")
public void processar(PedidoDto pedido) {
    // processa pedido
}
```

A diferença conceitual central em relação ao Kafka: no AMQP as mensagens são roteadas por *exchanges* e *routing keys* para *queues* (filas com semântica de consumo e exclusão), enquanto no Kafka são publicadas em *topics* com *partitions* (log imutável e retentivo).

### Spring Cloud Stream

Spring Cloud Stream (versão estável atual: 5.0.x) introduz uma camada de abstração chamada **binder** que desacopla o código de negócio do broker específico. O mesmo código de aplicação roda sobre Kafka, RabbitMQ, Apache Pulsar, Amazon Kinesis, Azure Event Hubs ou Google PubSub trocando apenas a dependência do binder.

O **modelo funcional** usa interfaces Java padrão (`Function`, `Consumer`, `Supplier`) como definição das funções de mensageria:

```java
// Consumidor puro (entrada, sem saída)
@Bean
public Consumer<PedidoDto> processarPedido() {
    return pedido -> log.info("Recebido: {}", pedido);
}

// Transformador (entrada → saída)
@Bean
public Function<PedidoDto, NotaFiscalDto> emitirNota() {
    return pedido -> gerarNota(pedido);
}

// Fonte (sem entrada, produz mensagens)
@Bean
public Supplier<String> gerarEvento() {
    return () -> "evento-" + System.currentTimeMillis();
}
```

O framework cria os *bindings* (ligadores) automaticamente a partir dos nomes dos beans. A configuração do broker vai para `application.yml` — o código não cita Kafka ou Rabbit.

**Spring Integration** (EIP) é o projeto mais antigo: implementa padrões de pipes-and-filters para fluxos complexos de integração entre sistemas. Está fora do escopo deste galho.

## Na prática

### Tabela: projeto → quando usar

| Situação | Projeto recomendado |
|---|---|
| Só usa Kafka e precisa de controle fino (partições, headers, transações exatas) | Spring Kafka |
| Só usa RabbitMQ, com roteamento por exchanges e filas | Spring AMQP |
| Precisa suportar múltiplos brokers ou trocar broker sem reescrever código | Spring Cloud Stream |
| Fluxos de integração complexos (EIP: splitter, aggregator, router) | Spring Integration |
| Aprendendo Kafka no Spring Boot, galho 14 | Spring Kafka (foco deste galho) |

### Esboço mínimo — Spring Kafka

```xml
<!-- pom.xml -->
<dependency>
    <groupId>org.springframework.kafka</groupId>
    <artifactId>spring-kafka</artifactId>
</dependency>
```

```java
@Service
public class ProdutorKafka {
    private final KafkaTemplate<String, String> kafkaTemplate;

    public void publicar(String topico, String chave, String valor) {
        kafkaTemplate.send(topico, chave, valor);
    }
}
```

### Esboço mínimo — Spring AMQP

```xml
<dependency>
    <groupId>org.springframework.boot</groupId>
    <artifactId>spring-boot-starter-amqp</artifactId>
</dependency>
```

```java
@Service
public class ProdutorAmqp {
    private final RabbitTemplate rabbitTemplate;

    public void publicar(String exchange, String routingKey, Object payload) {
        rabbitTemplate.convertAndSend(exchange, routingKey, payload);
    }
}
```

### Esboço mínimo — Spring Cloud Stream (Kafka binder)

```xml
<dependency>
    <groupId>org.springframework.cloud</groupId>
    <artifactId>spring-cloud-stream-binder-kafka</artifactId>
</dependency>
```

```java
@Bean
public Consumer<String> processar() {
    return msg -> System.out.println("Recebido: " + msg);
}
```

```yaml
# application.yml
spring.cloud.stream.bindings.processar-in-0.destination: meu-topico
spring.cloud.stream.bindings.processar-in-0.group: meu-grupo
```

## Armadilhas

### (1) Usar Spring Cloud Stream quando o cliente direto bastava

Spring Cloud Stream é poderoso, mas adiciona uma camada de indireção. Se a aplicação só usa Kafka e não há plano de trocar de broker, o Spring Kafka direto é mais simples: configuração mais direta, menor superfície de abstração, acesso fácil a offsets e headers Kafka nativos. A abstração do binder cobra um preço em legibilidade quando você precisa depurar comportamentos Kafka específicos (transações exatas, rebalanceamento manual, headers customizados).

### (2) Misturar abstrações no mesmo serviço

Usar `KafkaTemplate` (Spring Kafka) e ao mesmo tempo definir `Function<>` beans do Spring Cloud Stream no mesmo contexto Spring causa conflitos de configuração: os dois tentam gerenciar contêineres de listener com propriedades potencialmente sobrepostas. Escolha uma camada por serviço e seja consistente.

## Em entrevista

### Frase pronta (inglês)

> "Spring's messaging ecosystem has three main layers. Spring Kafka and Spring AMQP are direct clients that give you idiomatic Spring abstractions — KafkaTemplate, RabbitTemplate, and listener annotations — over the native broker APIs. Spring Cloud Stream sits one level higher, using a binder model to decouple your business logic from the specific broker; you write plain Java functions and swap binders in configuration. Choosing between them is a trade-off between control and portability: the direct clients give you lower-level access and simpler mental models when you're committed to one broker, while Cloud Stream shines when portability or multi-broker support matters."

### Vocabulário

| Português | Inglês |
|---|---|
| cliente (direto) | client |
| abstração | abstraction |
| ligador | binder |
| modelo funcional | functional model |
| ouvinte | listener |
| gabarito / template | template |
| fila | queue |
| tópico | topic |
| partição | partition |
| troca (AMQP) | exchange |
| chave de roteamento | routing key |
| fila de mensagens mortas | dead-letter queue / dead-letter topic |

## Veja também

- [[03-Dominios/Tecnologia/Java/Mensageria/index|Mensageria (MOC do galho)]]
- [[03-Dominios/Tecnologia/Java/index|Trilha Java]]
- [[03-Dominios/Tecnologia/Java/Mensageria/07 - KafkaTemplate — produzindo mensagens|KafkaTemplate]]
- [[03-Dominios/Tecnologia/Java/Mensageria/17 - Spring Cloud Stream — a abstração de binders|Spring Cloud Stream]]
- [[03-Dominios/Tecnologia/Java/Mensageria/15 - Spring AMQP e RabbitMQ|Spring AMQP e RabbitMQ]]
- [[03-Dominios/Tecnologia/Java/Dicionário de Java|Dicionário de Java]]

## Referências

- Spring for Apache Kafka — Reference Documentation: https://docs.spring.io/spring-kafka/reference/
- Spring AMQP — Reference Documentation: https://docs.spring.io/spring-amqp/reference/
- Spring Cloud Stream — Reference Documentation: https://docs.spring.io/spring-cloud-stream/reference/
