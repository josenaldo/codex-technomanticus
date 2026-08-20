---
title: "Mensageria reativa — Reactor Kafka"
alias: "Reactor Kafka"
fase: magus
tags:
  - java
  - mensageria
  - magus
  - reativa
  - kafka
type: concept
status: seedling
publish: true
created: 2026-06-11
updated: 2026-06-11
---

# Mensageria reativa — Reactor Kafka

> [!abstract] TL;DR
> Reactor Kafka é a ponte entre o Kafka e o Project Reactor: o `KafkaReceiver` expõe mensagens como um `Flux<ReceiverRecord>` com backpressure nativo, e o `KafkaSender` aceita um `Publisher<SenderRecord>` para produção não bloqueante. O modelo é poderoso quando o consumidor processa streams de alta vazão com pressão de volta real; fora desse cenário, Virtual Threads (Galho 4) entregam a mesma não-bloqueabilidade com muito menos cerimônia.

## O que é

Reactor Kafka (`io.projectreactor.kafka`) é a integração oficial do Project Reactor com o Apache Kafka. Diferentemente do Spring Kafka (que usa threads bloqueantes e o modelo `@KafkaListener`), o Reactor Kafka expõe o consumo e a produção de mensagens como streams reativos totalmente não bloqueantes.

A biblioteca define duas abstrações centrais:

- **`KafkaReceiver`** — consumidor reativo. Criado a partir de `ReceiverOptions`, expõe o método `receive()` que retorna um `Flux<ReceiverRecord<K, V>>`. A instância é lazy: o consumidor Kafka subjacente só é criado na primeira subscrição.
- **`KafkaSender`** — produtor reativo. Criado a partir de `SenderOptions`, expõe `send(Publisher<SenderRecord<K, V, C>>)` para produção assíncrona. Também lazy.

Ambos são **single-consumer/single-producer** por instância; para paralelismo, cria-se múltiplas instâncias.

## Por que importa

O modelo `@KafkaListener` (Spring Kafka) funciona bem para a maioria dos casos, mas ocupa uma thread bloqueada por partição durante o poll. Em sistemas de alta vazão com centenas de partições ou que já operam sobre um runtime reativo (WebFlux, por exemplo), manter threads bloqueadas é custo desnecessário.

O Reactor Kafka resolve isso expondo o consumo como um `Flux`, aproveitando o backpressure do Project Reactor para controlar a taxa de ingestão sem criar pressão excessiva de memória.

A pergunta certa antes de adotar: *o consumidor realmente sofre backpressure real?* Se a resposta for não — taxa de chegada previsível, processamento rápido, Virtual Threads disponíveis (Java 21+) — o caminho imperativo simples pode ser suficiente.

## Como funciona

### KafkaReceiver e KafkaSender

`KafkaReceiver` é o cliente reativo de consumo. A configuração mínima envolve `ReceiverOptions`, onde se definem bootstrap servers, deserializadores e a subscrição:

```java
ReceiverOptions<String, String> options = ReceiverOptions.<String, String>create(
        Map.of(
            ConsumerConfig.BOOTSTRAP_SERVERS_CONFIG, "localhost:9092",
            ConsumerConfig.GROUP_ID_CONFIG, "grupo-reativo",
            ConsumerConfig.KEY_DESERIALIZER_CLASS_CONFIG, StringDeserializer.class,
            ConsumerConfig.VALUE_DESERIALIZER_CLASS_CONFIG, StringDeserializer.class
        ))
    .subscription(Collections.singleton("pedidos"));

KafkaReceiver<String, String> receiver = KafkaReceiver.create(options);
```

O `KafkaSender` segue a mesma estrutura com `SenderOptions` e serializadores:

```java
SenderOptions<String, String> senderOptions = SenderOptions.<String, String>create(
        Map.of(
            ProducerConfig.BOOTSTRAP_SERVERS_CONFIG, "localhost:9092",
            ProducerConfig.KEY_SERIALIZER_CLASS_CONFIG, StringSerializer.class,
            ProducerConfig.VALUE_SERIALIZER_CLASS_CONFIG, StringSerializer.class
        ));

KafkaSender<String, String> sender = KafkaSender.create(senderOptions);
```

### Backpressure no consumo

O consumo reativo com `KafkaReceiver` respeita a demanda downstream — isso é backpressure nativo do Project Reactor. A opção `maxInFlight` (padrão: 256) limita o número de mensagens em voo simultâneo no pipeline, evitando que o consumidor avance mais rápido do que o processamento consegue acompanhar.

Para os detalhes de como o Reactor implementa backpressure (`request(n)`, estratégias `BUFFER`, `DROP`, `LATEST`), veja [[03-Dominios/Tecnologia/Java/Programação Reativa/09 - Backpressure — request(n) e as estratégias BUFFER, DROP, LATEST|Backpressure]] — essa nota não repete o conceito, apenas o aplica ao contexto Kafka.

O ponto crítico aqui é que o `poll` do Kafka é controlado pela demanda expressa pelo subscriber: se o pipeline downstream pede menos, o receiver desacelera o poll. Isso é o que diferencia o modelo do `@KafkaListener` com threads bloqueadas.

### Quando o reativo paga no consumo de stream

O Reactor Kafka justifica sua complexidade quando:

- O consumidor faz parte de um pipeline reativo mais amplo (ex.: WebFlux que agrega dados de Kafka com chamadas HTTP reativas).
- Há centenas de partições e o custo de threads bloqueadas (uma por partição no modelo imperativo) é proibitivo.
- O processamento downstream tem latência variável e backpressure real — o `Flux` com `maxInFlight` protege contra acúmulo de memória.

Quando **não** justifica:

- Aplicações simples com taxa de chegada estável e processamento rápido: aqui o `@KafkaListener` com Virtual Threads (Galho 4, planejado) entrega não-bloqueabilidade com muito menos cerimônia. Virtual Threads tornam o modelo imperativo suficiente ao eliminar o custo de thread bloqueada sem exigir programação reativa.
- Times sem familiaridade com o modelo reativo: a curva de aprendizado e o risco de erros (bloquear dentro do pipeline, commit fora do fluxo) superam os ganhos.

## Na prática

Consumindo um `Flux<ReceiverRecord>` com commit manual de offset:

```java
@Service
public class PedidoReativoConsumer {

    private final KafkaReceiver<String, String> receiver;

    public PedidoReativoConsumer(ReceiverOptions<String, String> options) {
        this.receiver = KafkaReceiver.create(options);
    }

    public Flux<Void> iniciar() {
        return receiver.receive()
            .flatMap(record -> processar(record)
                .doOnSuccess(v -> record.receiverOffset().acknowledge())
                .onErrorResume(ex -> {
                    // registra erro; offset não é commitado — reprocessamento na próxima poll
                    return Mono.empty();
                })
            );
    }

    private Mono<Void> processar(ReceiverRecord<String, String> record) {
        String payload = record.value();
        // lógica não bloqueante; NUNCA chamar .block() aqui
        return Mono.fromRunnable(() -> System.out.println("Processando: " + payload));
    }
}
```

Pontos de atenção no exemplo:
- `acknowledge()` só é chamado após o processamento bem-sucedido — semântica at-least-once.
- O `onErrorResume` descarta o erro sem committar o offset; o registro será reentregue.
- Nenhum `.block()` dentro do pipeline — a thread do event loop não pode ser bloqueada.

## Armadilhas

### (1) Bloquear dentro do pipeline reativo

Chamar `.block()`, `Thread.sleep()` ou qualquer operação bloqueante dentro do `flatMap` do receiver trava a thread do event loop do Reactor. O resultado é deadlock silencioso ou queda de throughput catastrófica.

A documentação do Reactor Kafka é explícita: *"Cannot block the receiver thread."*

Correção: use `publishOn(Schedulers.boundedElastic())` antes da operação bloqueante para delegá-la a um scheduler separado:

```java
receiver.receive()
    .publishOn(Schedulers.boundedElastic())
    .flatMap(record -> Mono.fromCallable(() -> operacaoBlockingAqui(record)))
    ...
```

### (2) Adotar o reativo sem necessidade real

Reactor Kafka impõe complexidade genuína: configuração de `ReceiverOptions`, gerenciamento de ciclo de vida do receiver, semântica de commit explícita, e risco elevado de erros sutis. Adotar sem backpressure real no sistema é pagar o preço sem colher o benefício.

Se o objetivo é apenas "não bloquear threads", Java 21+ com Virtual Threads e `@KafkaListener` resolve o problema com zero mudança de modelo mental.

### (3) Commit de offset fora do fluxo reativo

Chamar `receiverOffset().acknowledge()` fora do contexto do pipeline reativo — por exemplo, num callback assíncrono não encadeado ao `Flux` — quebra a garantia de ordenação do commit. O Reactor Kafka gerencia commits de forma reativa e encadeada; desrespeitar isso pode resultar em commits fora de ordem, reprocessamento incorreto ou mensagens perdidas.

A regra: o `acknowledge()` deve ser chamado dentro do operador reativo que encadeia diretamente ao `record`, nunca em código que "salta" para fora do contexto do Flux.

## Em entrevista

### Frase pronta (inglês)

"Reactor Kafka exposes Kafka consumption as a `Flux<ReceiverRecord>`, giving you native backpressure so the consumer only polls as fast as the downstream pipeline can handle. The key tradeoff is complexity: you gain flow control and thread efficiency at scale, but you must never block inside the pipeline and offset commits must stay within the reactive chain. For simpler workloads, Virtual Threads with a standard `@KafkaListener` often deliver the same non-blocking behaviour with far less ceremony."

### Vocabulário

| Termo PT | Termo EN |
|---|---|
| Receptor reativo | Reactive receiver / `KafkaReceiver` |
| Registro receptor | `ReceiverRecord` |
| Opções de receptor | `ReceiverOptions` |
| Confirmação de offset | Offset acknowledgement |
| Mensagem em voo | In-flight message |
| Pressão de volta | Backpressure |
| Subscrição | Topic subscription |
| Semântica de entrega | Delivery semantics |

## Veja também

- [[03-Dominios/Tecnologia/Java/Mensageria/index|Mensageria (MOC do galho)]]
- [[03-Dominios/Tecnologia/Java/index|Trilha Java]]
- [[03-Dominios/Tecnologia/Java/Programação Reativa/09 - Backpressure — request(n) e as estratégias BUFFER, DROP, LATEST|Backpressure]]
- [[03-Dominios/Tecnologia/Java/Programação Reativa/index|Programação Reativa]]
- [[03-Dominios/Tecnologia/Java/Mensageria/08 - @KafkaListener — consumindo mensagens|@KafkaListener]]
- [[03-Dominios/Tecnologia/Java/Dicionário de Java|Dicionário de Java]]

## Referências

- [Reactor Kafka Reference Guide](https://projectreactor.io/docs/kafka/release/reference/) — documentação oficial; fonte primária desta nota.
- `KafkaReceiver`, `KafkaSender`, `ReceiverOptions`, `SenderOptions` — APIs confirmadas na documentação oficial (acesso: 2026-06-11).
