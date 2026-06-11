---
title: "Dead Letter Topic — o padrão DLQ"
aliases:
  - DLQ
fase: adepto
tags:
  - java
  - mensageria
  - adepto
  - spring-kafka
  - rabbitmq
type: concept
status: seedling
publish: true
created: 2026-06-11
updated: 2026-06-11
---

# Dead Letter Topic — o padrão DLQ

> **TL;DR** — Quando uma mensagem falha repetidamente e os retries se esgotam, ela não pode ser descartada silenciosamente. O padrão DLQ (Dead Letter Queue / Dead Letter Topic) a redireciona para um destino separado — o `*-dlt` no Kafka ou o *dead-letter exchange* no RabbitMQ — onde pode ser inspecionada, alertada e reprocessada depois que a causa-raiz for corrigida.

---

## O que é

Dead Letter Queue (DLQ) — ou Dead Letter Topic (DLT) no vocabulário Kafka — é o destino para o qual uma mensagem é encaminhada quando não pôde ser processada com sucesso após todas as tentativas de retry configuradas.

O nome vem da analogia com o serviço postal: cartas que não chegam ao destinatário são enviadas para uma "caixa de cartas mortas" para análise posterior.

No contexto Java/Spring, o padrão materializa-se de formas ligeiramente diferentes dependendo do broker:

- **Apache Kafka + Spring Kafka**: um tópico auxiliar com sufixo `-dlt` (ex.: `pedidos-dlt`), gerenciado pelo `DeadLetterPublishingRecoverer` ou pelo mecanismo de retries não-bloqueantes do `@RetryableTopic`.
- **RabbitMQ + Spring AMQP**: um *dead-letter exchange* (DLX) para o qual a fila original encaminha mensagens rejeitadas ou expiradas.

---

## Por que importa

Sem esse padrão, uma mensagem problemática tem apenas dois destinos possíveis: loop infinito de retries (travando o consumidor) ou descarte silencioso (perda de dado). Nenhum dos dois é aceitável em sistemas de produção.

O DLQ resolve três problemas reais:

1. **Visibilidade**: mensagens com falha ficam acessíveis para diagnóstico.
2. **Continuidade**: o consumidor não fica bloqueado esperando uma mensagem que jamais vai funcionar.
3. **Recuperabilidade**: após corrigir o bug, é possível reprocessar o DLT sem perda de dados.

---

## Como funciona

### DeadLetterPublishingRecoverer

O `DeadLetterPublishingRecoverer` é a peça central para DLT no Spring Kafka quando se usa a abordagem *blocking retry* (via `DefaultErrorHandler`). Ele é invocado pelo framework depois que todos os retries se esgotam.

O que ele faz:
- Publica a mensagem falha num tópico chamado `<tópico-original>-dlt` (padrão), na mesma partição do registro original.
- Adiciona automaticamente headers de diagnóstico ao registro publicado no DLT: `KafkaHeaders.DLT_EXCEPTION_FQCN`, `DLT_EXCEPTION_MESSAGE`, `DLT_EXCEPTION_STACKTRACE`, `DLT_ORIGINAL_TOPIC`, `DLT_ORIGINAL_PARTITION`, `DLT_ORIGINAL_OFFSET`, `DLT_ORIGINAL_TIMESTAMP`, entre outros.
- Comita o offset do registro original, permitindo que o consumidor avance.

Requisito importante: **o tópico DLT deve ter pelo menos tantas partições quanto o tópico original**, pois o recoverer publica na mesma partição por padrão.

### @RetryableTopic

O `@RetryableTopic` é o mecanismo de *non-blocking retries* do Spring Kafka. Em vez de bloquear o *thread* do consumidor durante o backoff, ele republica a mensagem em tópicos de retry intermediários (`<tópico>-retry-0`, `<tópico>-retry-1`, …) e, após esgotar as tentativas, encaminha para o DLT automaticamente.

Características confirmadas na documentação oficial:
- Os nomes padrão dos tópicos de retry seguem o padrão `<tópico>-retry-<delay>` e o DLT recebe o sufixo `-dlt`.
- É possível customizar os sufixos com `retryTopicSuffix` e `dltTopicSuffix`.
- O DLT pode ter um handler dedicado via `@DltHandler` no mesmo bean listener.
- Exceções consideradas fatais (ex.: `DeserializationException`, `MessageConversionException`) são enviadas diretamente ao DLT sem retries, evitando loops infinitos.
- A estratégia padrão de falha no DLT é `ALWAYS_RETRY_ON_ERROR`: se o handler do DLT falhar, a mensagem retorna ao DLT para não bloquear outras.

### DLQ no RabbitMQ

No RabbitMQ, o equivalente ao DLT é o *Dead Letter Exchange* (DLX). Uma mensagem torna-se "dead-lettered" em quatro situações documentadas:

1. Negada pelo consumidor via `basic.reject` ou `basic.nack` com `requeue = false`.
2. TTL da mensagem expirado.
3. Fila cheia (limite de comprimento atingido).
4. Limite de reentregas excedido (quorum queues).

A configuração recomendada pela documentação oficial é via *policies* (permite atualização dinâmica sem reimplantar a aplicação):

```bash
rabbitmqctl set_policy DLX ".*" '{"dead-letter-exchange":"my-dlx"}' --apply-to queues
```

Alternativamente, via argumentos de fila (requer recriação da fila para alterar): `x-dead-letter-exchange` e `x-dead-letter-routing-key`.

Por padrão o RabbitMQ usa publicação não confirmada para o DLX, o que pode causar perda em clusters. Quorum queues oferecem *at-least-once dead-lettering* com confirms internos habilitados.

---

## Na prática

### Blocking retry com DeadLetterPublishingRecoverer

```java
@Configuration
public class KafkaErrorHandlerConfig {

    @Bean
    public DefaultErrorHandler errorHandler(KafkaTemplate<Object, Object> kafkaTemplate) {
        DeadLetterPublishingRecoverer recoverer =
            new DeadLetterPublishingRecoverer(kafkaTemplate);
        // 3 tentativas com 1 segundo de intervalo
        FixedBackOff backOff = new FixedBackOff(1_000L, 2L);
        return new DefaultErrorHandler(recoverer, backOff);
    }
}
```

Registros com falha são publicados automaticamente em `<tópico-original>-dlt`.

### Non-blocking retry com @RetryableTopic

```java
@Service
public class PedidoListener {

    @RetryableTopic(
        attempts = "4",                    // 1 original + 3 retries
        backoff = @BackOff(delay = 2_000, multiplier = 2.0, maxDelay = 30_000),
        dltTopicSuffix = "-dlt",
        kafkaTemplate = "pedidosKafkaTemplate"
    )
    @KafkaListener(topics = "pedidos", groupId = "pedidos-consumer")
    public void consumir(PedidoEvent evento) {
        // processamento de negócio
        processarPedido(evento);
    }

    @DltHandler
    public void handleDlt(PedidoEvent evento, @Header(KafkaHeaders.DLT_EXCEPTION_MESSAGE) String erro) {
        // registrar, alertar, persistir para análise manual
        log.error("Mensagem no DLT — erro: {}, evento: {}", erro, evento);
    }
}
```

**Convenção de nome**: o tópico DLT gerado será `pedidos-dlt`. Os tópicos de retry intermediários seguem o padrão `pedidos-retry-2000`, `pedidos-retry-4000`, etc. (baseados no delay configurado).

### Configuração via builder (alternativa ao annotation)

```java
@Bean
public RetryTopicConfiguration pedidosRetryConfig(
        KafkaTemplate<String, PedidoEvent> template) {
    return RetryTopicConfigurationBuilder
        .newInstance()
        .exponentialBackoff(2_000, 2, 30_000)
        .maxAttempts(4)
        .dltTopicSuffix("-dlt")
        .includeTopics(List.of("pedidos"))
        .create(template);
}
```

---

## Armadilhas

### (1) DLQ sem alarme nem monitoramento

Configurar o DLT e não monitorá-lo equivale a não tê-lo. Mensagens acumulam no DLT silenciosamente enquanto o sistema aparenta estar saudável. A boa prática é conectar o consumer group do DLT a um alerta (Prometheus + Alertmanager, Datadog, etc.) que dispare quando o lag do tópico `*-dlt` crescer acima de zero.

### (2) Reprocessar o DLT sem corrigir a causa-raiz

Replay do DLT é uma operação válida — mas só após corrigir o bug que causou a falha. Repuplicar mensagens do DLT no tópico original sem consertar o consumidor as devolve ao DLT imediatamente, criando um loop de replay. Antes do reprocessamento: diagnosticar, corrigir, testar, só então republicar.

### (3) Retry topics multiplicando partições e recursos

Cada tópico de retry criado pelo `@RetryableTopic` consome recursos do broker (partições, armazenamento, conexões). Em cenários com muitos listeners e muitas tentativas de retry, isso pode explodir o número de tópicos no cluster. Avalie usar `SameIntervalTopicReuseStrategy.SINGLE_TOPIC` para backoffs fixos (padrão desde Spring Kafka 4.1) ou limitar o número de tentativas.

---

## Em entrevista

**Frases-chave em inglês:**

- *"A dead letter topic is where messages land after all retry attempts are exhausted, preventing data loss without blocking the consumer."*
- *"With `@RetryableTopic`, Spring Kafka implements non-blocking retries by forwarding failed messages to intermediate retry topics and eventually to the DLT."*
- *"One common pitfall is setting up a DLT without any alerting — messages silently pile up and the team only finds out during an incident."*
- *"Before replaying a DLT, you must fix the root cause; otherwise the messages just cycle back."*

**Vocabulário técnico:**

| Termo | Significado |
|---|---|
| Dead Letter Topic (DLT) | Tópico Kafka destino de mensagens com falha irrecuperável |
| Dead Letter Exchange (DLX) | Exchange RabbitMQ destino de mensagens dead-lettered |
| `DeadLetterPublishingRecoverer` | Bean Spring Kafka que publica no DLT após retries bloqueantes |
| `@RetryableTopic` | Anotação para retries não-bloqueantes com DLT automático |
| `@DltHandler` | Método anotado que processa mensagens chegadas ao DLT |
| Non-blocking retry | Retry via tópicos intermediários, sem bloquear o thread do consumidor |
| DLT replay | Operação de reprocessar mensagens acumuladas no DLT |

---

## Veja também

- [[03-Dominios/Java/Mensageria/MOC — Galho 14 Mensageria|MOC — Galho 14 Mensageria]]
- [[03-Dominios/Java/Trilha Java Senior|Trilha Java Senior]]
- [[03-Dominios/Java/Mensageria/11 - Tratamento de erro no consumo|Tratamento de erro no consumo]]
- [[03-Dominios/Java/Mensageria/15 - Spring AMQP e RabbitMQ|Spring AMQP e RabbitMQ]]
- [[03-Dominios/Java/Mensageria/26 - Observabilidade em mensageria|Observabilidade em mensageria]]
- [[03-Dominios/Java/Dicionário de Java|Dicionário de Java]]

---

## Referências

- Spring for Apache Kafka — Non-Blocking Retries / DLT Strategies: <https://docs.spring.io/spring-kafka/reference/retrytopic/dlt-strategies.html>
- Spring for Apache Kafka — Retry Topic Configuration: <https://docs.spring.io/spring-kafka/reference/retrytopic/retry-config.html>
- Spring for Apache Kafka — Topic Naming: <https://docs.spring.io/spring-kafka/reference/retrytopic/topic-naming.html>
- Spring for Apache Kafka — DeadLetterPublishingRecoverer: <https://docs.spring.io/spring-kafka/reference/kafka/annotation-error-handling.html>
- RabbitMQ — Dead Letter Exchanges: <https://www.rabbitmq.com/docs/dlx>
