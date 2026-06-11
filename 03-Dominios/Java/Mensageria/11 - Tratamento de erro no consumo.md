---
title: "Tratamento de erro no consumo"
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
  - spring-kafka
aliases:
  - "Kafka error handling"
  - "DefaultErrorHandler"
  - "Consumer error handling Spring Kafka"
---

# Tratamento de erro no consumo

> [!abstract] TL;DR
> Quando um listener lança exceção, o Spring Kafka decide se tenta de novo, desiste ou encaminha para outra fila. O `DefaultErrorHandler` — substituto do `SeekToCurrentErrorHandler` desde a versão 2.8 — centraliza essa decisão: configura quantas tentativas fazer, quanto esperar entre elas (`BackOff`) e quais erros nem adianta retentar (`addNotRetryableExceptions`). Dominar essa tríade é o que separa um consumer robusto de um que trava a partição inteira.

## O que é

Processar uma mensagem Kafka pode falhar: banco indisponível, dados malformados, violação de regra de negócio. O broker não tem como saber disso — ele só sabe se o offset foi confirmado ou não. Quem decide o que fazer com o erro é o **error handler** configurado no `ConcurrentMessageListenerContainer`.

No Spring Kafka, a interface central é `CommonErrorHandler` (introduzida na versão 2.8). Ela unificou os antigos handlers separados para listener de registro e listener de batch. A implementação padrão é o `DefaultErrorHandler`, que substitui o `SeekToCurrentErrorHandler` e o `RecoveringBatchErrorHandler` a partir da versão 2.8.

```
Listener lança exceção
        │
        ▼
  DefaultErrorHandler
        │
        ├─ Exceção não-retentável? ──► Recovery (ex.: DLQ)
        │
        ├─ BackOff esgotado? ─────────► Recovery (ex.: DLQ)
        │
        └─ Ainda tem tentativas? ─────► seek + re-entrega
```

## Por que importa

Kafka garante ordenação dentro de uma partição. Se o consumer trava numa mensagem com erro e fica retentando indefinidamente sem política de back-off, **toda a partição fica bloqueada**: nenhuma mensagem posterior é processada, o lag cresce e o sistema degrada silenciosamente.

Definir uma estratégia de erro explícita resolve três problemas práticos:

- **Falhas transitórias** (rede, banco) — retentar com espera é suficiente.
- **Falhas determinísticas** (desserialização inválida, validação) — retentar é inútil; enviar para DLQ é o caminho.
- **Falhas em cascata** — limitar tentativas e usar back-off exponencial evita sobrecarregar o sistema que já está com problema.

## Como funciona

### DefaultErrorHandler — o handler padrão desde 2.8

O `DefaultErrorHandler` é registrado via `setCommonErrorHandler()` na factory do container. Ele sucede o `SeekToCurrentErrorHandler` (e o `RecoveringBatchErrorHandler`), que foram marcados como deprecated na versão 2.8 do Spring Kafka.

Internamente, quando um listener lança exceção, o handler:

1. Verifica se a exceção está na lista de não-retentáveis → se sim, vai direto para o recoverer.
2. Consulta o `BackOff` para saber se ainda há tentativas → se esgotado, vai para o recoverer.
3. Se ainda há tentativas, faz seek do offset de volta e aguarda o intervalo configurado.

O recoverer padrão é um simples log de warning. Em produção, quase sempre substitui-se por um `DeadLetterPublishingRecoverer` (ver nota 12).

```java
// Handler mínimo — 3 tentativas com 1 segundo de espera entre elas
DefaultErrorHandler handler = new DefaultErrorHandler(new FixedBackOff(1_000L, 2L));

// Registrando na factory
factory.setCommonErrorHandler(handler);
```

> [!info] Versão
> `DefaultErrorHandler` foi introduzido no Spring Kafka 2.8 (Spring Boot 2.6+). No Boot 3.x (Spring Kafka 3.x) é o padrão ativo.

### Estratégias de back-off

O contrato de back-off é definido pela interface `BackOffExecution` do Spring Framework. O Spring Kafka aceita qualquer implementação; as mais usadas são:

**`FixedBackOff`** — intervalo fixo entre tentativas.

```java
// 1 000 ms de espera, 2 re-tentativas (3 tentativas no total)
new FixedBackOff(1_000L, 2L)

// Sem limite de tentativas (útil para falhas transitórias graves,
// mas exige um circuit-breaker externo para não bloquear a partição)
new FixedBackOff(5_000L, Long.MAX_VALUE)
```

**`ExponentialBackOffWithMaxRetries`** — intervalo dobra a cada tentativa, com teto configurável.

```java
ExponentialBackOffWithMaxRetries bo = new ExponentialBackOffWithMaxRetries(6);
bo.setInitialInterval(1_000L);   // 1 s na 1ª tentativa
bo.setMultiplier(2.0);           // 2 s, 4 s, 8 s…
bo.setMaxInterval(30_000L);      // teto de 30 s
```

> [!tip] Regra prática
> Use `FixedBackOff` para ambientes controlados (testes, retry simples). Use `ExponentialBackOffWithMaxRetries` em produção quando o serviço dependente pode estar sobrecarregado — evita tempestade de retry.

### Exceções não-retentáveis

Alguns erros são **determinísticos**: a mensagem está malformada, o contrato de tipo não bate, a validação de negócio sempre vai falhar com aquele payload. Retentar não resolve — só desperdiça tempo e bloqueia a partição.

`addNotRetryableExceptions()` instrui o handler a pular as tentativas e acionar o recoverer imediatamente para essas classes de exceção.

```java
handler.addNotRetryableExceptions(
    IllegalArgumentException.class,   // validação de negócio
    ValidationException.class         // Jakarta Validation
);
```

O Spring Kafka já trata como não-retentáveis por padrão:

| Exceção | Motivo |
|---|---|
| `DeserializationException` | Payload corrompido — retry sempre vai falhar |
| `MessageConversionException` | Conversão de tipo falhou |
| `ConversionException` | Idem |
| `MethodArgumentResolutionException` | Assinatura do listener incompatível |
| `ClassCastException` | Tipo incompatível |

> [!warning] Cuidado com a lista padrão
> Erros de desserialização chegam embrulhados em `DeserializationException` quando o `ErrorHandlingDeserializer` está ativo. Se você usar um deserializador customizado sem esse wrapper, a exceção pode não estar na lista padrão — adicione explicitamente.

## Na prática

Configuração típica de produção: `DefaultErrorHandler` com back-off exponencial, exceções não-retentáveis definidas e recoverer apontando para a DLQ.

```java
@Configuration
public class KafkaConsumerConfig {

    @Bean
    public DefaultErrorHandler errorHandler(
            KafkaTemplate<String, Object> kafkaTemplate) {

        // Recoverer envia para <topico-original>.DLT após esgotar tentativas
        DeadLetterPublishingRecoverer recoverer =
                new DeadLetterPublishingRecoverer(kafkaTemplate);

        // Back-off: 1 s → 2 s → 4 s → 8 s → 16 s → 30 s (teto), 5 re-tentativas
        ExponentialBackOffWithMaxRetries bo =
                new ExponentialBackOffWithMaxRetries(5);
        bo.setInitialInterval(1_000L);
        bo.setMultiplier(2.0);
        bo.setMaxInterval(30_000L);

        DefaultErrorHandler handler = new DefaultErrorHandler(recoverer, bo);

        // Erros determinísticos — não retentar
        handler.addNotRetryableExceptions(
                IllegalArgumentException.class,
                ValidationException.class
        );

        return handler;
    }

    @Bean
    public ConcurrentKafkaListenerContainerFactory<String, Object>
            kafkaListenerContainerFactory(
                    ConsumerFactory<String, Object> consumerFactory,
                    DefaultErrorHandler errorHandler) {

        ConcurrentKafkaListenerContainerFactory<String, Object> factory =
                new ConcurrentKafkaListenerContainerFactory<>();
        factory.setConsumerFactory(consumerFactory);
        factory.setCommonErrorHandler(errorHandler);
        return factory;
    }
}
```

Após esgotar as tentativas, o `DeadLetterPublishingRecoverer` envia a mensagem para o tópico DLT (Dead Letter Topic). O detalhamento desse padrão está na [[03-Dominios/Java/Mensageria/12 - Dead Letter Topic — o padrão DLQ|nota 12]].

> [!info] Boot 3.x auto-configuração
> Com Spring Boot 3.x, é possível configurar partes do error handler via `application.yml` (número de tentativas, back-off) usando as propriedades `spring.kafka.listener.*`. A configuração programática ainda é necessária para cenários avançados (recoverer customizado, lista de não-retentáveis).

## Armadilhas

### (1) Retry infinito bloqueando a partição inteira

Configurar `FixedBackOff` com `Long.MAX_VALUE` tentativas sem nenhum circuit-breaker externo é uma bomba-relógio. Uma mensagem problemática que sempre falha (erro transitório que virou permanente, serviço que nunca voltou) vai segurar o processamento de toda a partição por horas ou dias.

**Solução:** use `ExponentialBackOffWithMaxRetries` com um número razoável de tentativas (5–10), depois envie para DLQ e deixe o processamento continuar.

### (2) Retentar erro de desserialização

Erros de desserialização são determinísticos: o payload não vai mudar entre tentativas. Retentar só atrasa o inevitável e ocupa a partição.

**Solução:** `DeserializationException` já é não-retentável por padrão quando o `ErrorHandlingDeserializer` está ativo. Confirme que ele está configurado no `ConsumerFactory`. Se usar deserializador customizado sem o wrapper, adicione a exceção explicitamente via `addNotRetryableExceptions`.

### (3) Back-off fixo curto sob falha persistente

Se o banco caiu e o back-off é de 100 ms com 10 tentativas, o consumer vai martelar o banco 10 vezes por mensagem, por todas as partições, sem parar. Numa aplicação com 20 partições e 1 000 mensagens no lag, isso vira uma tempestade de requisições contra um serviço já degradado.

**Solução:** use back-off exponencial com teto (ex.: máximo 30 s) e considere integrar com Resilience4j CircuitBreaker no listener para pausar o container enquanto o serviço dependente está fora.

## Em entrevista

> "When a Kafka consumer throws an exception, how does Spring Kafka decide whether to retry?"

Resposta estruturada (EN):

> "Spring Kafka delegates that decision to the `CommonErrorHandler` — specifically, the `DefaultErrorHandler` introduced in version 2.8 to replace the deprecated `SeekToCurrentErrorHandler`. It consults a `BackOff` strategy — fixed or exponential — to determine retry count and delay. If the exception is classified as non-retryable via `addNotRetryableExceptions`, retries are skipped entirely and the record goes straight to the recoverer, typically a `DeadLetterPublishingRecoverer`. Once the back-off is exhausted, the same recovery path triggers. This prevents a single bad record from blocking an entire partition indefinitely."

**Vocabulário-chave:**

| Termo | Contexto |
|---|---|
| `CommonErrorHandler` | interface base de error handling no Spring Kafka 2.8+ |
| `DefaultErrorHandler` | implementação padrão; substitui `SeekToCurrentErrorHandler` |
| `BackOff` / `BackOffExecution` | contrato de espera entre tentativas |
| `FixedBackOff` | intervalo constante entre retries |
| `ExponentialBackOffWithMaxRetries` | intervalo cresce exponencialmente com teto |
| `addNotRetryableExceptions` | marca exceções que não devem ser retentadas |
| `DeadLetterPublishingRecoverer` | recoverer que envia para DLT após tentativas esgotadas |
| seek | operação de reposicionar o offset para re-processar a mensagem |

## Veja também

- [[03-Dominios/Java/Mensageria/index|MOC — Mensageria]]
- [[03-Dominios/Java/index|Trilha Java Senior]]
- [[03-Dominios/Java/Mensageria/12 - Dead Letter Topic — o padrão DLQ|Dead Letter Topic — o padrão DLQ]]
- [[03-Dominios/Java/Mensageria/10 - Ack modes e commit de offset|Ack modes e commit de offset]]
- [[03-Dominios/Java/Mensageria/09 - (De)serialização de mensagens|(De)serialização de mensagens]]
- [[03-Dominios/Java/Dicionário de Java|Dicionário de Java]]

## Referências

- Spring Kafka Reference — Error Handling: https://docs.spring.io/spring-kafka/reference/kafka/annotation-error-handling.html
- Spring Kafka 2.8 Release Notes — DefaultErrorHandler introduction: https://spring.io/blog/2021/10/27/spring-for-apache-kafka-2-8-is-available
- Spring Framework `BackOff` / `ExponentialBackOff`: https://docs.spring.io/spring-framework/docs/current/javadoc-api/org/springframework/util/backoff/ExponentialBackOff.html
