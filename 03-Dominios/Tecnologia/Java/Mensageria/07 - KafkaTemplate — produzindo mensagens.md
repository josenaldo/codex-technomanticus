---
title: "KafkaTemplate — produzindo mensagens"
fase: Adepto
tags:
  - java
  - mensageria
  - adepto
  - spring-kafka
  - kafka
created: 2026-06-11
updated: 2026-06-11
type: concept
status: seedling
publish: true
aliases:
  - KafkaTemplate
---

# KafkaTemplate — produzindo mensagens

> [!abstract] TL;DR
> `KafkaTemplate<K, V>` é o ponto de entrada do Spring Kafka para publicar mensagens. Todo `send(...)` retorna um `CompletableFuture<SendResult<K, V>>` — ignorar esse future significa aceitar perda silenciosa. A chave da mensagem determina a partição de destino: mesma chave → mesma partição → ordering garantido. Os configs `acks`, `linger.ms`, `batch.size` e `enable.idempotence` controlam o trade-off entre durabilidade e throughput.

---

## O que é

`KafkaTemplate<K, V>` é o wrapper de alto nível do Spring Kafka sobre o `KafkaProducer` nativo. Ele gerencia o ciclo de vida do producer (criação, reutilização, fechamento), expõe métodos `send(...)` fortemente tipados e integra com o mecanismo de serialização configurado no `ProducerFactory`.

A classe pertence ao módulo `spring-kafka` e está disponível desde a versão 1.x. A partir da versão 3.0 (compatível com Spring Boot 3.x), o retorno de todos os métodos `send` passou de `ListenableFuture` para `CompletableFuture` — alinhando-se com o padrão moderno da JVM.

---

## Por que importa

Sem um wrapper como o `KafkaTemplate`, o código de aplicação precisaria gerenciar diretamente o `KafkaProducer` — incluindo serialização manual, tratamento de erros de rede, retries e flush. Em entrevistas, dominar o `KafkaTemplate` sinaliza que o candidato sabe trabalhar com Kafka no contexto Spring sem cair na armadilha de reinventar infraestrutura.

Além disso, os detalhes de durabilidade (`acks=all`) e idempotência (`enable.idempotence=true`) são cobrados em perguntas de sistema distribuído: compreender o que cada config garante — e o que não garante — demonstra maturidade além do CRUD.

---

## Como funciona

### send e ProducerRecord

O `KafkaTemplate` expõe duas famílias de métodos:

- **`send(topic, key, value)`** — atalho para o caso mais comum.
- **`send(ProducerRecord<K, V> record)`** — permite controle total: partição explícita, timestamp customizado, headers HTTP-like.

Todos retornam `CompletableFuture<SendResult<K, V>>`. O `SendResult` carrega:
- `ProducerRecord<K, V>` — o registro original enviado.
- `RecordMetadata` — offset, partição e timestamp confirmados pelo broker.

**Modo assíncrono (recomendado para throughput):**

```java
CompletableFuture<SendResult<String, Order>> future =
    kafkaTemplate.send("orders", order.getId(), order);

future.whenComplete((result, ex) -> {
    if (ex == null) {
        log.info("Mensagem enviada: offset={}", result.getRecordMetadata().offset());
    } else {
        log.error("Falha ao enviar mensagem para o tópico orders", ex);
    }
});
```

**Modo síncrono (útil em scripts, testes ou fluxos sequenciais):**

```java
try {
    SendResult<String, Order> result =
        kafkaTemplate.send("orders", order.getId(), order).get(10, TimeUnit.SECONDS);
    log.info("Offset confirmado: {}", result.getRecordMetadata().offset());
} catch (ExecutionException e) {
    throw new RuntimeException("Falha no envio", e.getCause());
} catch (TimeoutException | InterruptedException e) {
    Thread.currentThread().interrupt();
    throw new RuntimeException("Timeout ou interrupção no envio", e);
}
```

> [!warning] Bloquear o thread principal em aplicações reativas ou de alto volume cancela o benefício do Kafka como buffer assíncrono. Use `.get()` com consciência.

### chave → partição

O algoritmo padrão do Kafka (`DefaultPartitioner`) mapeia a chave para uma partição pelo hash da chave (`murmur2`):

```
partição = hash(key) % numPartições
```

Consequência direta: **mensagens com a mesma chave sempre chegam à mesma partição na mesma ordem**. Isso é essencial quando o consumidor precisa de ordering por entidade (ex.: todos os eventos do pedido `#42` processados em sequência).

Quando a chave é `null`, o producer distribui as mensagens entre partições em modo round-robin (ou sticky batch nas versões mais recentes do cliente Kafka). **Não há garantia de ordering sem chave.**

### configs de durabilidade e throughput

Os três eixos principais de tuning do producer:

| Config | Padrão | Significado |
|---|---|---|
| `acks` | `all` (Kafka 3.0+) | Quantas réplicas devem confirmar a escrita |
| `linger.ms` | `0` | Tempo de espera para encher um batch |
| `batch.size` | `16384` (16 KB) | Tamanho máximo do batch em bytes |
| `enable.idempotence` | `true` (Kafka 3.0+) | Garante exatamente uma entrega por sessão de producer |

**`acks` — durabilidade vs latência:**

- `acks=0`: o producer não espera confirmação. Máximo throughput, zero durabilidade.
- `acks=1`: o broker líder confirma, mas réplicas ainda não gravaram. Uma falha de liderança pode perder a mensagem.
- `acks=all` (ou `-1`): todas as réplicas in-sync confirmam. Mais lento, durabilidade máxima.

**`linger.ms` e `batch.size` — throughput vs latência:**

O producer acumula mensagens em memória antes de transmitir. Um batch transmite com mais eficiência (menos round-trips de rede) mas introduz latência artificial. `linger.ms=0` transmite imediatamente; valores como `5` ou `10` ms podem dobrar o throughput em cargas altas.

**`enable.idempotence` — producer idempotente:**

Com `enable.idempotence=true`, o broker rastreia um número de sequência por `(producerId, partição)` e descarta duplicatas causadas por retries de rede. Isso requer `acks=all` e `max.in.flight.requests.per.connection <= 5`. No Kafka 3.0+ e Spring Boot 3.x, esse é o padrão — não é necessário configurar explicitamente, mas vale confirmar que nada sobrescreve o valor.

---

## Na prática

### Configuração (application.yaml)

```yaml
spring:
  kafka:
    bootstrap-servers: localhost:9092
    producer:
      key-serializer: org.apache.kafka.common.serialization.StringSerializer
      value-serializer: org.springframework.kafka.support.serializer.JsonSerializer
      acks: all
      properties:
        linger.ms: 5
        batch.size: 32768
        enable.idempotence: true
```

> [!tip] `JsonSerializer` do Spring Kafka adiciona headers de tipo por padrão (`__TypeId__`). Em integrações com consumidores não-Spring, desative com `spring.kafka.producer.properties.spring.json.add.type.headers=false` ou use um serializer Avro.

### Bean de configuração e uso do KafkaTemplate

```java
// Domínio
public record Order(String id, String customerId, BigDecimal total) {}

// Serviço produtor
@Service
@RequiredArgsConstructor
public class OrderProducer {

    private static final String TOPIC = "orders";
    private final KafkaTemplate<String, Order> kafkaTemplate;

    public void publish(Order order) {
        CompletableFuture<SendResult<String, Order>> future =
            kafkaTemplate.send(TOPIC, order.id(), order);

        future.whenComplete((result, ex) -> {
            if (ex == null) {
                RecordMetadata meta = result.getRecordMetadata();
                log.info("Order {} enviado → partição={} offset={}",
                    order.id(), meta.partition(), meta.offset());
            } else {
                // KafkaProducerException permite acessar o ProducerRecord original
                log.error("Falha ao publicar order {}: {}", order.id(), ex.getMessage());
            }
        });
    }

    // Variante com ProducerRecord para controle total
    public void publishWithHeaders(Order order) {
        ProducerRecord<String, Order> record =
            new ProducerRecord<>(TOPIC, null, order.id(), order);
        record.headers().add("source-service", "order-service".getBytes());

        kafkaTemplate.send(record).whenComplete((result, ex) -> {
            if (ex != null) log.error("Erro no envio", ex);
        });
    }
}
```

### Configuração Java explícita (quando não se usa Boot auto-config)

```java
@Configuration
public class KafkaProducerConfig {

    @Bean
    public ProducerFactory<String, Order> producerFactory() {
        Map<String, Object> props = new HashMap<>();
        props.put(ProducerConfig.BOOTSTRAP_SERVERS_CONFIG, "localhost:9092");
        props.put(ProducerConfig.KEY_SERIALIZER_CLASS_CONFIG, StringSerializer.class);
        props.put(ProducerConfig.VALUE_SERIALIZER_CLASS_CONFIG, JsonSerializer.class);
        props.put(ProducerConfig.ACKS_CONFIG, "all");
        props.put(ProducerConfig.ENABLE_IDEMPOTENCE_CONFIG, true);
        return new DefaultKafkaProducerFactory<>(props);
    }

    @Bean
    public KafkaTemplate<String, Order> kafkaTemplate() {
        return new KafkaTemplate<>(producerFactory());
    }
}
```

---

## Armadilhas

### (1) `acks=1` esperando durabilidade real

Definir `acks=1` parece suficiente — o broker confirmou! — mas se a réplica líder falhar antes de replicar, a mensagem se perde. Em sistemas onde cada mensagem representa uma transação financeira (pagamento, estorno, pedido), isso é inaceitável. Use `acks=all` e aceite a latência adicional, que em redes locais tipicamente é de apenas alguns milissegundos.

### (2) Ignorar o `CompletableFuture` retornado por `send`

```java
// ERRADO — perda silenciosa de mensagens
kafkaTemplate.send("payments", paymentId, payment);
```

```java
// CORRETO — sempre trate o future
kafkaTemplate.send("payments", paymentId, payment)
    .whenComplete((result, ex) -> {
        if (ex != null) log.error("Falha no envio do payment {}", paymentId, ex);
    });
```

`send` é não-bloqueante. Sem `.whenComplete` ou `.get(...)`, erros de rede, serialização ou broker são silenciados. Em produção isso se manifesta como mensagens "desaparecidas" sem nenhum log de erro.

### (3) Chave nula esperando ordering

```java
// Sem chave — round-robin entre partições — SEM ordering
kafkaTemplate.send("orders", null, order);

// Com chave — mesma partição para o mesmo customerId — ordering garantido
kafkaTemplate.send("orders", order.customerId(), order);
```

Se o consumidor espera processar eventos de um mesmo cliente em sequência (máquina de estados, saga), a chave precisa ser o identificador da entidade. Chave nula distribui as mensagens aleatoriamente entre partições, quebrando o ordering.

---

## Em entrevista

### Frase pronta (inglês)

"KafkaTemplate is Spring Kafka's high-level producer abstraction. Every send call returns a CompletableFuture — you must handle it, otherwise failures are swallowed silently. The message key maps to a partition via consistent hashing, so same key always lands on the same partition and guarantees ordering for that key. For durability, I set acks=all and enable idempotence, which prevents duplicate messages from producer retries. I trade a few milliseconds of extra latency for the guarantee that no message is lost on broker failover."

### Vocabulário

| Português | Inglês |
|---|---|
| Produtor idempotente | Idempotent producer |
| Confirmação de escrita | Acknowledgment (acks) |
| Registro do produtor | ProducerRecord |
| Resultado do envio | SendResult / RecordMetadata |
| Tamanho do lote | Batch size |
| Latência de lote | Linger time |
| Réplicas em sincronia | In-sync replicas (ISR) |

---

## Veja também

- [[03-Dominios/Tecnologia/Java/Mensageria/index|Mensageria (MOC do galho)]]
- [[03-Dominios/Tecnologia/Java/index|Trilha Java]]
- [[03-Dominios/Tecnologia/Java/Backend/Kafka/Kafka Concepts/9. Producers|Producers (infra)]]
- [[03-Dominios/Tecnologia/Java/Mensageria/08 - @KafkaListener — consumindo mensagens|@KafkaListener]]
- [[03-Dominios/Tecnologia/Java/Mensageria/20 - Idempotência — o pilar do at-least-once|Idempotência]]
- [[03-Dominios/Tecnologia/Java/Mensageria/14 - Schema e contratos — Avro e Schema Registry|Schema e contratos]]
- [[03-Dominios/Tecnologia/Java/Dicionário de Java|Dicionário de Java]]

---

## Referências

- [Spring Kafka — Sending Messages](https://docs.spring.io/spring-kafka/reference/kafka/sending-messages.html) (Spring Kafka 4.1.0 / compatível com Spring Boot 3.x)
- [Spring Kafka — KafkaTemplate Javadoc](https://docs.spring.io/spring-kafka/docs/current/api/org/springframework/kafka/core/KafkaTemplate.html)
- [Apache Kafka — Producer Configs](https://kafka.apache.org/documentation/#producerconfigs)
