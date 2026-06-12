---
title: Observabilidade em mensageria
fase: magus
tags:
  - java
  - mensageria
  - magus
  - observabilidade
created: 2026-06-11
updated: 2026-06-11
type: concept
status: seedling
publish: true
---

# Observabilidade em mensageria

> [!abstract] TL;DR
> Observar um sistema de mensageria significa medir o que importa para a **saúde do fluxo de dados**: quanto a fila acumula (consumer lag), quanto tempo cada mensagem leva para ser processada e se o trace de uma requisição HTTP atravessa intacto o broker até o consumer. Com Spring Kafka 3.x e Micrometer Observation, tudo isso sai do zero com poucas linhas de configuração.

---

## O que é

Observabilidade em mensageria é a capacidade de responder, em produção, às perguntas: "as mensagens estão sendo consumidas no ritmo que chegam?", "onde foi que o processamento de _esta_ mensagem falhou?" e "qual é a latência de ponta a ponta entre o producer e o consumer?".

No ecossistema Spring Kafka isso se traduz em três camadas:

- **Métricas de producer/consumer** — contadores e temporizadores expostos pelo próprio cliente Kafka e coletados via Micrometer.
- **Consumer lag** — diferença entre o offset mais recente do topic e o offset já confirmado pelo grupo consumer; é a métrica mais direta de acúmulo de fila.
- **Tracing distribuído** — propagação do contexto de rastreamento (trace-id, span-id) como headers da mensagem, permitindo que uma única requisição seja rastreada de forma contínua do producer ao consumer, mesmo atravessando o broker.

---

## Por que importa

Sem observabilidade, o broker Kafka é uma caixa-preta. Você sabe que mensagens entram e saem, mas não sabe se o consumer está atrasando, onde um trace se perdeu ou qual partição está mais sobrecarregada.

Num contexto de entrevista para posições sênior, demonstrar que você pensa em **SLOs de mensageria** (latência de consumo, taxa de erro de processamento) e sabe instrumentar o pipeline para medir esses SLOs separa candidatos que apenas "usam Kafka" de quem o opera com responsabilidade.

---

## Como funciona

### Consumer lag — a métrica nº 1

Consumer lag é a quantidade de mensagens que o consumer ainda não processou. Formalmente:

```text
lag = latest_offset(topic, partition) - committed_offset(consumer_group, partition)
```

Um lag crescente significa que o consumer não acompanha o producer — pode ser lentidão no processamento, número insuficiente de partições ou de threads, ou um consumer travado.

O cliente Kafka nativo já expõe `kafka.consumer.records-lag` como métrica JMX. Ao registrar `MicrometerConsumerListener` na `ConsumerFactory`, essa e dezenas de outras métricas do cliente são automaticamente publicadas no `MeterRegistry` e ficam disponíveis para Prometheus/Grafana:

```java
cf.addListener(new MicrometerConsumerListener<>(meterRegistry));
```

A métrica chave a monitorar é `kafka.consumer.fetch-manager-metrics` → `records-lag-max`, que representa o lag máximo entre todas as partições atribuídas ao consumer.

### Tracing distribuído através do broker

O trace distribuído funciona injetando os dados de contexto (trace-id, span-id) nos **headers da mensagem Kafka** no momento do envio e extraindo esses headers no consumer para continuar o mesmo trace. Sem esse mecanismo, o span do producer termina no broker e o span do consumer começa do zero — a cadeia se quebra e não dá para saber que os dois pertencem à mesma operação de negócio.

O Micrometer Observation API (introduzido no Spring Kafka 3.0) cuida exatamente disso. Quando a observação está habilitada no `KafkaTemplate` e no container de listener:

1. O `KafkaTemplate` cria um span `spring.kafka.template` ao enviar, propaga o contexto nos headers da mensagem.
2. O listener container extrai os headers, cria um span filho `spring.kafka.listener` e executa o listener dentro desse contexto.
3. Qualquer backend de tracing (Zipkin, Jaeger, via Micrometer Tracing ou OpenTelemetry) recebe os dois spans vinculados.

O `ObservationRegistry` do Spring (geralmente auto-configurado pelo Spring Boot Actuator com `spring-boot-starter-actuator` e a dependência de tracing na classpath) é o ponto central de configuração.

### Métricas de producer/consumer

Além do lag, o cliente Kafka expõe métricas de throughput e latência que precisam ser coletadas ativamente. As mais relevantes para monitoramento de saúde:

| Métrica nativa do cliente | O que mede |
|---|---|
| `kafka.producer.record-send-rate` | Mensagens enviadas por segundo |
| `kafka.producer.request-latency-avg` | Latência média das requisições de produce |
| `kafka.consumer.fetch-rate` | Requisições de fetch por segundo |
| `kafka.consumer.records-consumed-rate` | Mensagens consumidas por segundo |
| `kafka.consumer.records-lag-max` | Lag máximo entre partições |
| `spring.kafka.listener` (Timer) | Duração do processamento no listener |
| `spring.kafka.template` (Timer) | Duração do envio via KafkaTemplate |

Com a Observation API ativada, `spring.kafka.listener` e `spring.kafka.template` também geram spans de tracing, não apenas timers.

---

## Na prática

### Habilitando Micrometer Observation no Spring Kafka

**Dependências** (Spring Boot 3.x com `spring-kafka`):

```xml
<!-- pom.xml -->
<dependency>
    <groupId>org.springframework.boot</groupId>
    <artifactId>spring-boot-starter-actuator</artifactId>
</dependency>
<dependency>
    <groupId>io.micrometer</groupId>
    <artifactId>micrometer-tracing-bridge-otel</artifactId>
</dependency>
<dependency>
    <groupId>io.opentelemetry</groupId>
    <artifactId>opentelemetry-exporter-zipkin</artifactId>
</dependency>
```

**Configuração Java** — habilitando observation em KafkaTemplate e listener container:

```java
@Configuration
public class KafkaObservabilityConfig {

    @Bean
    public ConsumerFactory<String, String> consumerFactory(
            MeterRegistry meterRegistry) {
        var configs = Map.<String, Object>of(
            ConsumerConfig.BOOTSTRAP_SERVERS_CONFIG, "localhost:9092",
            ConsumerConfig.GROUP_ID_CONFIG, "meu-grupo",
            ConsumerConfig.KEY_DESERIALIZER_CLASS_CONFIG, StringDeserializer.class,
            ConsumerConfig.VALUE_DESERIALIZER_CLASS_CONFIG, StringDeserializer.class
        );
        var cf = new DefaultKafkaConsumerFactory<String, String>(configs);
        // Registra métricas nativas do cliente Kafka no MeterRegistry
        cf.addListener(new MicrometerConsumerListener<>(meterRegistry));
        return cf;
    }

    @Bean
    public ProducerFactory<String, String> producerFactory(
            MeterRegistry meterRegistry) {
        var configs = Map.<String, Object>of(
            ProducerConfig.BOOTSTRAP_SERVERS_CONFIG, "localhost:9092",
            ProducerConfig.CLIENT_ID_CONFIG, "meu-producer",
            ProducerConfig.KEY_SERIALIZER_CLASS_CONFIG, StringSerializer.class,
            ProducerConfig.VALUE_SERIALIZER_CLASS_CONFIG, StringSerializer.class
        );
        var pf = new DefaultKafkaProducerFactory<String, String>(configs);
        pf.addListener(new MicrometerProducerListener<>(meterRegistry));
        return pf;
    }

    @Bean
    public KafkaTemplate<String, String> kafkaTemplate(
            ProducerFactory<String, String> pf) {
        var template = new KafkaTemplate<>(pf);
        // Habilita Micrometer Observation (propaga trace context nos headers)
        template.setObservationEnabled(true);
        return template;
    }

    @Bean
    public ConcurrentKafkaListenerContainerFactory<String, String> kafkaListenerContainerFactory(
            ConsumerFactory<String, String> cf) {
        var factory = new ConcurrentKafkaListenerContainerFactory<String, String>();
        factory.setConsumerFactory(cf);
        // Habilita observation no consumer (extrai trace context dos headers)
        factory.getContainerProperties().setObservationEnabled(true);
        return factory;
    }
}
```

**Configuração YAML** (auto-configuração do Spring Boot Actuator):

```yaml
management:
  tracing:
    sampling:
      probability: 1.0   # 100% para dev; ajustar em produção
  endpoints:
    web:
      exposure:
        include: health, metrics, prometheus
  metrics:
    export:
      prometheus:
        enabled: true

spring:
  kafka:
    bootstrap-servers: localhost:9092
    consumer:
      group-id: meu-grupo
    producer:
      client-id: meu-producer
```

> [!tip] Observation desativa os timers legados
> Quando `observationEnabled = true`, os `Timer`s legados (`spring.kafka.listener`, `spring.kafka.template`) são desativados e substituídos pelas observações — que geram tanto métricas quanto spans de tracing. Não ative os dois ao mesmo tempo.

### Consumer com trace propagado

```java
@Component
public class MeuConsumer {

    @KafkaListener(topics = "pedidos", groupId = "meu-grupo")
    public void processar(ConsumerRecord<String, String> record) {
        // O trace context já foi extraído dos headers pelo container
        // Qualquer log aqui aparecerá com o mesmo traceId do producer
        log.info("Processando pedido: {}", record.value());
        // ... lógica de negócio
    }
}
```

---

## Armadilhas

### (1) Só logar sem correlação de trace — o trace quebra ao atravessar o broker

A armadilha mais comum é adicionar logs nos listeners sem garantir que o trace context do producer chegue ao consumer. Sem `observationEnabled = true` em ambos os lados (producer e consumer), cada lado cria seu próprio trace independente. O resultado é que no Jaeger ou Zipkin você vê dois traces desconectados para a mesma operação de negócio, tornando o rastreamento de problemas end-to-end impossível.

**Solução**: habilitar observation tanto no `KafkaTemplate` quanto no `ContainerProperties` e garantir que o backend de tracing (Micrometer Tracing + OTel) esteja na classpath.

### (2) Ignorar o consumer lag até a fila estourar

É comum só perceber que o consumer está lento quando o sistema começa a apresentar comportamento errático — timeouts, dados desatualizados, backpressure visível na UI. Nesse ponto, o lag pode estar na casa dos milhões de mensagens.

**Solução**: configurar um alerta em `kafka.consumer.records-lag-max` com threshold baixo (por exemplo, > 1.000 mensagens durante mais de 5 minutos). O alerta deve ser acionado antes de o lag se tornar um problema operacional, não depois.

### (3) Não propagar o trace context nos headers da mensagem

Se o producer envia mensagens sem incluir os headers de tracing, o consumer não tem como reconstituir o trace. Isso acontece quando o `KafkaTemplate` é usado sem observation habilitada, ou quando mensagens são produzidas fora do Spring (por exemplo, por um producer em outra linguagem) sem implementar W3C TraceContext ou B3 nos headers.

**Solução**: padronizar o formato de propagação (W3C `traceparent` é o padrão atual do OpenTelemetry) e garantir que todos os producers — independente de linguagem — injetem esses headers. No lado Spring Kafka, `observationEnabled = true` faz isso automaticamente.

---

## Em entrevista

### Frase pronta (inglês)

"In a Kafka-based system, observability means tracking three things: consumer lag as the primary health signal for the pipeline, producer and consumer throughput metrics to detect bottlenecks, and distributed trace propagation through message headers so you can follow a single business operation across the broker boundary. With Spring Kafka 3.x and Micrometer Observation enabled on both the KafkaTemplate and the listener container, context propagation happens automatically via Kafka message headers — the producer injects the trace context and the consumer extracts it, keeping the trace chain intact. The key metric to alert on is `kafka.consumer.records-lag-max`; if it keeps growing, your consumer is falling behind and you need to act before the lag becomes unmanageable."

### Vocabulário

| Termo | Definição |
|---|---|
| **Consumer lag** | Diferença entre o offset mais recente do topic e o offset confirmado pelo consumer group; mede o acúmulo de mensagens não processadas |
| **Micrometer Observation** | API do Micrometer que instrumenta código uma vez e gera métricas, spans de tracing e logs simultaneamente via handlers registrados no `ObservationRegistry` |
| **Context propagation** | Mecanismo de transmitir o trace context (trace-id, span-id) entre serviços; em Kafka, é feito via headers da mensagem |
| **W3C TraceContext** | Padrão de propagação de trace adotado pelo OpenTelemetry; define os headers `traceparent` e `tracestate` |
| **`ObservationRegistry`** | Bean central do Micrometer Observation que agrega `ObservationHandler`s e decide como processar cada observação |
| **`MicrometerConsumerListener`** | Listener de fábrica do Spring Kafka que registra automaticamente as métricas nativas do cliente Kafka consumer no `MeterRegistry` |
| **`records-lag-max`** | Métrica nativa do cliente Kafka que expõe o lag máximo entre todas as partições atribuídas ao consumer; principal KPI de saúde do consumer |
| **Span** | Unidade de trabalho no tracing distribuído; representa uma operação com início, fim, tags e vínculo com o trace pai |

---

## Veja também

- [[03-Dominios/Java/Mensageria/index|Mensageria (MOC do galho)]]
- [[03-Dominios/Java/index|Trilha Java]]
- [[03-Dominios/Java/Mensageria/08 - @KafkaListener — consumindo mensagens|@KafkaListener]]
- [[03-Dominios/Java/Mensageria/10 - Ack modes e commit de offset|Ack modes e commit de offset]]
- [[03-Dominios/Java/Dicionário de Java|Dicionário de Java]]

Observabilidade de infraestrutura e operação de cluster em produção = [[03-Dominios/Java/Cloud-native e produção/13 - Observabilidade de operação — o panorama e os 3 seams|Galho 17 (Cloud-native e produção)]].

---

## Referências

- [Spring Kafka — Monitoring](https://docs.spring.io/spring-kafka/reference/kafka/micrometer.html) (Spring for Apache Kafka 4.1.0)
- [Spring Kafka — Micrometer Observation Appendix](https://docs.spring.io/spring-kafka/reference/appendix/micrometer.html) (Spring for Apache Kafka 4.1.0)
- [Micrometer Observation — Introduction](https://docs.micrometer.io/micrometer/reference/observation/introduction.html) (Micrometer 1.17.0)
