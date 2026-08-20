---
title: "@KafkaListener — consumindo mensagens"
created: 2026-06-11
updated: 2026-06-11
type: concept
status: seedling
publish: true
fase: Adepto
tags:
  - java
  - mensageria
  - adepto
  - spring-kafka
  - kafka
aliases:
  - "@KafkaListener"
---

# @KafkaListener — consumindo mensagens

> [!abstract] TL;DR
> `@KafkaListener` é o jeito idiomático de **consumir** mensagens com Spring Kafka: você anota um método, declara o tópico e o `groupId`, e o framework sobe um **message listener container** que faz o poll loop por você e entrega cada registro já desserializado. O paralelismo vem do atributo `concurrency` do `ConcurrentKafkaListenerContainerFactory` — mas ele é limitado pelo número de partições, e o tempo de processamento por mensagem precisa caber dentro de `max.poll.interval.ms`, ou o consumer é expulso do grupo num rebalance.

## O que é

`@KafkaListener` é uma anotação de método do Spring Kafka que transforma um bean comum num **consumidor de mensagens**. Em vez de você escrever o laço `while (true) { consumer.poll(...) }` e cuidar de desserialização, commit de offset e tratamento de erro na mão, você declara *o que* quer consumir e deixa o framework cuidar do *como*.

```java
@KafkaListener(topics = "orders", groupId = "order-processor")
public void onOrder(Order order) {
    // sua lógica de negócio
}
```

Por baixo, cada `@KafkaListener` é gerenciado por um **listener container** — um componente que encapsula um `KafkaConsumer` nativo e roda o poll loop. Esse é o complemento natural do produtor: enquanto o [[03-Dominios/Tecnologia/Java/Mensageria/07 - KafkaTemplate — produzindo mensagens|KafkaTemplate]] escreve no tópico, o `@KafkaListener` lê dele.

> A mecânica de baixo nível — o que é um consumer, como ele se junta a um grupo, como partições são atribuídas — está na trilha de infra: [[03-Dominios/Tecnologia/Java/Backend/Kafka/Kafka Concepts/10. Consumers|Consumers (infra)]] e [[03-Dominios/Tecnologia/Java/Backend/Kafka/Kafka Concepts/11. Consumer Groups|Consumer Groups (infra)]]. Esta nota foca na camada Spring que fica por cima.

## Por que importa

Consumir do Kafka "na unha" envolve muito código repetitivo e cheio de armadilhas: gerenciar o ciclo de vida do consumer, capturar exceções sem matar a thread, decidir quando commitar offset, lidar com rebalance. O Spring Kafka empacota tudo isso atrás de uma anotação, com vantagens concretas:

- **Ciclo de vida automático** — o container sobe e desce junto com o contexto da aplicação.
- **Desserialização declarativa** — o registro chega ao seu método já convertido para o tipo de domínio.
- **Paralelismo configurável** — um único atributo (`concurrency`) cria múltiplas threads de consumo.
- **Tratamento de erro padronizado** — retry, dead-letter topic e back-off sem instrumentação manual.

O preço de não entender a camada é real: configurar `concurrency` alto demais desperdiça threads, e processar mensagens devagar demais derruba o consumer do grupo. Os dois pontos aparecem em [Armadilhas](#armadilhas).

## Como funciona

### O listener container

`@KafkaListener` por si só é só uma marcação. Quem faz o trabalho é o **listener container**, criado a partir de um `ConcurrentKafkaListenerContainerFactory` — a fábrica padrão que o Spring Boot autoconfigura para você.

O container assume a responsabilidade pelo **poll loop**: ele chama `consumer.poll()` em ciclo, recebe os registros, invoca seu método anotado para cada um (ou para um lote, no modo batch) e cuida do commit de offset conforme o ack mode configurado. Você nunca escreve o `while (true)`.

O nome "Concurrent" vem do fato de que esse container é, na verdade, um *delegador*: o `ConcurrentMessageListenerContainer` cria internamente N instâncias de `KafkaMessageListenerContainer`, cada uma com seu próprio consumer rodando numa thread separada. O atributo que controla esse N é o `concurrency`.

```java
@Configuration
public class KafkaConsumerConfig {

    @Bean
    public ConcurrentKafkaListenerContainerFactory<String, Order> kafkaListenerContainerFactory(
            ConsumerFactory<String, Order> consumerFactory) {

        var factory = new ConcurrentKafkaListenerContainerFactory<String, Order>();
        factory.setConsumerFactory(consumerFactory);
        factory.setConcurrency(3); // 3 consumers, 3 threads
        return factory;
    }
}
```

### Concorrência × partições

O `concurrency=N` define quantos consumers (e quantas threads) o container vai criar. Mas há um teto natural: **o número de partições do tópico**.

A regra do Kafka é que cada partição é atribuída a no máximo um consumer *dentro do mesmo grupo*. Então, se você pede `concurrency=10` num tópico de 4 partições, só 4 consumers recebem partição — os outros 6 ficam **ociosos**, ocupando threads sem fazer nada. A própria documentação do Spring Kafka diz que, quando `concurrency` excede o número de `TopicPartitions`, cada container fica com no máximo uma partição e o excedente não trabalha.

A consequência prática:
- `concurrency <= nº de partições` → cada thread pega uma ou mais partições; bom aproveitamento.
- `concurrency == nº de partições` → uma thread por partição; paralelismo máximo dentro de um único processo.
- `concurrency > nº de partições` → threads sobrando, ociosas; desperdício de recursos.

> O paralelismo aqui é o mesmo modelo de threads da JVM — não vou re-explicar o que é uma thread, pool ou contenção. Veja a trilha [[03-Dominios/Tecnologia/Java/Concorrência e paralelismo/index|Concorrência e paralelismo]] (Galho 4). O ponto específico de mensageria é que a *unidade de paralelismo é a partição*, não a thread: você não escala um consumer além do número de partições só aumentando `concurrency`.

Vale notar uma sutileza: ao escutar **múltiplos tópicos**, a estratégia padrão de atribuição (`RangeAssignor`) pode distribuir partições de forma desigual e deixar threads ociosas mesmo quando o total de partições seria suficiente. Nesses casos, trocar para `RoundRobinAssignor` distribui melhor.

### group.id e auto.offset.reset

O **`group.id`** (declarado via `groupId` na anotação) identifica o **consumer group**. Todos os consumers com o mesmo `group.id` dividem as partições entre si — é assim que você escala horizontalmente: subir uma segunda instância da aplicação com o mesmo grupo faz o Kafka redistribuir partições entre as instâncias. Grupos diferentes leem o mesmo tópico de forma independente, cada um com seu próprio progresso (offsets).

O **`auto.offset.reset`** decide de onde o consumer começa a ler **quando não existe offset commitado** para aquele grupo — tipicamente no primeiro deploy, ou quando o offset salvo expirou. Dois valores importam:

- **`earliest`** — começa do início disponível da partição. No primeiro deploy, o consumer lê *todo o histórico* retido no tópico.
- **`latest`** (padrão do Kafka) — começa do fim. No primeiro deploy, o consumer só vê mensagens **produzidas a partir daquele momento**; tudo que já estava no tópico é ignorado.

> Atenção: `auto.offset.reset` só age na *ausência* de offset commitado. Depois que o grupo já commitou pelo menos um offset, esse parâmetro não tem mais efeito — o consumer retoma de onde parou.

## Na prática

Consumindo o tipo de domínio já desserializado:

```java
@Component
public class OrderConsumer {

    @KafkaListener(topics = "orders", groupId = "order-processor")
    public void consume(Order order) {
        // 'order' já chega desserializado do payload
        process(order);
    }
}
```

Quando você precisa de metadados (chave, partição, offset, headers), pode receber o `ConsumerRecord` cru ou desmembrar com `@Payload` e `@Header`:

```java
@KafkaListener(topics = "payments", groupId = "payment-auditor")
public void consume(
        @Payload Payment payment,
        @Header(KafkaHeaders.RECEIVED_KEY) String key,
        @Header(KafkaHeaders.RECEIVED_PARTITION) int partition,
        @Header(KafkaHeaders.OFFSET) long offset) {
    // payload + metadados de roteamento
}
```

Ou, com acesso total ao registro nativo:

```java
@KafkaListener(topics = "payments", groupId = "payment-auditor")
public void consume(ConsumerRecord<String, Payment> record) {
    String key = record.key();
    Payment payment = record.value();
    long offset = record.offset();
}
```

Configuração típica via `application.yml` (baseline Spring Boot 3.x):

```yaml
spring:
  kafka:
    bootstrap-servers: localhost:9092
    consumer:
      group-id: order-processor
      auto-offset-reset: earliest
      key-deserializer: org.apache.kafka.common.serialization.StringDeserializer
      value-deserializer: org.springframework.kafka.support.serializer.JsonDeserializer
      properties:
        spring.json.trusted.packages: "com.exemplo.dominio"
    listener:
      concurrency: 3
```

O `groupId` na anotação tem precedência sobre o `spring.kafka.consumer.group-id` do YAML; defina num lugar só para evitar confusão.

## Armadilhas

### (1) concurrency maior que o número de partições

Pedir `concurrency=12` num tópico de 4 partições não dá 12× de throughput — dá 4 consumers trabalhando e 8 threads ociosas. O Kafka nunca atribui uma partição a mais de um consumer do mesmo grupo, então o excedente fica parado. Regra de bolso: **dimensione `concurrency` para no máximo o número de partições do tópico**. Se quer mais paralelismo, aumente partições (planejando que esse número é difícil de reduzir depois) ou suba mais instâncias da aplicação com o mesmo `group.id`.

### (2) Processamento longo bloqueando o consumer → rebalance

O poll loop tem um contrato: entre uma chamada de `poll()` e a próxima, não pode passar mais que `max.poll.interval.ms` (padrão de 5 minutos no cliente Kafka). Como o container só volta a fazer poll *depois* de processar o lote anterior, um método `@KafkaListener` lento — uma chamada HTTP travada, uma query pesada — pode estourar esse limite. Quando isso acontece, o broker considera o consumer morto e dispara um **rebalance**: a partição é reatribuída a outro consumer, e o registro provavelmente é reprocessado (duplicação). Sintoma clássico: você vê rebalances frequentes e mensagens processadas mais de uma vez. Mitigações: encurtar o processamento, reduzir `max.poll.records` (menos registros por lote = menos tempo entre polls), ou empurrar trabalho pesado para fora da thread do listener.

### (3) auto.offset.reset=latest perdendo mensagens no primeiro deploy

Com `auto.offset.reset=latest` (o padrão do Kafka), um grupo *novo* só começa a ler do fim da partição. Se mensagens foram produzidas antes do consumer subir pela primeira vez, elas são **silenciosamente ignoradas** — não há erro, o tópico simplesmente "pula" o backlog. Isso surpreende em ambientes onde o produtor já está rodando antes do consumer. Se o seu caso exige processar tudo que já está no tópico, use `earliest`. Lembre que o parâmetro só vale na ausência de offset commitado; depois do primeiro commit, ele não muda mais nada.

## Em entrevista

### Frase pronta (inglês)

> In Spring Kafka, I consume messages with `@KafkaListener`, which is backed by a listener container that runs the poll loop and delivers each record already deserialized — I never write the poll loop myself. I scale throughput with the `concurrency` setting on the `ConcurrentKafkaListenerContainerFactory`, but I always cap it at the partition count, because Kafka assigns each partition to a single consumer in the group, so extra threads would just sit idle. The two things I watch most closely are `max.poll.interval.ms` — if my processing is slow enough to exceed it, the consumer gets kicked out and triggers a rebalance with possible reprocessing — and `auto.offset.reset`, since `latest` silently skips the existing backlog on a brand-new group, while `earliest` replays it.

### Vocabulário

| Termo (EN) | Termo (PT) | Nota |
|---|---|---|
| listener container | contêiner de listener | roda o poll loop por você |
| poll loop | laço de polling | `consumer.poll()` em ciclo |
| consumer group | grupo de consumidores | identificado por `group.id` |
| partition | partição | unidade de paralelismo do consumo |
| rebalance | rebalanceamento | reatribuição de partições no grupo |
| offset | offset | posição de leitura na partição |
| concurrency | concorrência | nº de consumers/threads do container |
| backlog | acúmulo/fila pendente | mensagens já no tópico |

## Veja também

- [[03-Dominios/Tecnologia/Java/Mensageria/index|Mensageria (MOC do galho)]]
- [[03-Dominios/Tecnologia/Java/index|Trilha Java]]
- [[03-Dominios/Tecnologia/Java/Backend/Kafka/Kafka Concepts/10. Consumers|Consumers (infra)]]
- [[03-Dominios/Tecnologia/Java/Backend/Kafka/Kafka Concepts/11. Consumer Groups|Consumer Groups (infra)]]
- [[03-Dominios/Tecnologia/Java/Concorrência e paralelismo/index|Concorrência e paralelismo]]
- [[03-Dominios/Tecnologia/Java/Mensageria/10 - Ack modes e commit de offset|Ack modes e commit de offset]]
- [[03-Dominios/Tecnologia/Java/Mensageria/07 - KafkaTemplate — produzindo mensagens|KafkaTemplate]]
- [[03-Dominios/Tecnologia/Java/Dicionário de Java|Dicionário de Java]]

## Referências

- Spring for Apache Kafka — Reference Documentation: `@KafkaListener`, Message Listener Containers e `ConcurrentMessageListenerContainer`. https://docs.spring.io/spring-kafka/reference/
- Spring Kafka — Concurrency e atribuição de partições (`ConcurrentMessageListenerContainer`). https://docs.spring.io/spring-kafka/reference/kafka/receiving-messages/message-listener-container.html
- Spring Kafka — Obtendo o `group.id` do consumer. https://docs.spring.io/spring-kafka/reference/kafka/receiving-messages/listener-group-id.html
- Apache Kafka — Consumer Configs (`auto.offset.reset`, `max.poll.interval.ms`, `group.id`). https://kafka.apache.org/documentation/#consumerconfigs
