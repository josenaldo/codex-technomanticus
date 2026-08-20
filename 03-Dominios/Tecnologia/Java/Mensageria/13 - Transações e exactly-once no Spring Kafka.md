---
title: "Transações e exactly-once no Spring Kafka"
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
---

# Transações e exactly-once no Spring Kafka

> [!abstract] TL;DR
> O Kafka oferece **transações** que tornam atômico o ciclo **read-process-write**: consumir de um tópico, processar e produzir para outro(s) tópico(s) — tudo confirma ou tudo aborta. No Spring, isso é orquestrado pelo `KafkaTransactionManager` + um `transactional.id` (via `transaction-id-prefix`), e o consumidor downstream precisa de `isolation.level=read_committed` para enxergar só o que foi comitado. A pegadinha que derruba candidato sênior: **exactly-once semantics (EOS) cobre SÓ o que vive dentro do Kafka**. Escrever num banco externo *na mesma transação Kafka* não é coberto — pra isso existe o [[03-Dominios/Tecnologia/Java/Mensageria/21 - O padrão Outbox|padrão Outbox]].

## O que é

Uma **transação Kafka** agrupa um conjunto de operações de produção (e o avanço de offsets do consumidor) numa unidade atômica: ou todas as mensagens ficam visíveis para consumidores `read_committed`, ou nenhuma fica. É o mecanismo que sustenta a famosa promessa de **exactly-once semantics (EOS)** dentro do broker.

Três peças se encaixam:

- **`transactional.id`** — identificador estável do produtor transacional. É o que permite ao broker fazer *fencing* de produtores zumbis (uma instância antiga que voltou a vida depois de um rebalance é "cercada" e impedida de comitar).
- **`isolation.level=read_committed`** — config do *consumidor*. Faz o consumer só entregar mensagens até o **last stable offset (LSO)**, ignorando mensagens de transações ainda abertas ou abortadas.
- **EOS v2** — a evolução do protocolo de exactly-once (no Spring Kafka, `EOSMode.V2`, único modo desde a versão 3.0). Reduz a quantidade de `transactional.id`s necessários no padrão read-process-write.

No Spring, o `KafkaTransactionManager` é um `PlatformTransactionManager`, então você dirige tudo isso com o `@Transactional` de sempre.

## Por que importa

O Kafka é, por padrão, **at-least-once**: em falha, mensagens podem ser reprocessadas e duplicadas (ver [[03-Dominios/Tecnologia/Java/Mensageria/03 - Garantias de entrega — e a falácia do exactly-once|Garantias de entrega]]). Para pipelines onde duplicar é caro — debitar um pagamento duas vezes, emitir um pedido duplicado — você quer que o ciclo "li → processei → produzi → avancei o offset" seja **tudo ou nada**.

Sem transação, há uma janela mortal: você produz a mensagem de saída, mas crasha antes de comitar o offset de entrada. No restart, reprocessa a mesma entrada e produz a saída de novo — duplicata. A transação Kafka fecha essa janela ao incluir o **avanço do offset do consumidor dentro da própria transação de produção**.

Mas — e aqui mora o equívoco caro — isso **não** é mágica de transação distribuída. Não há *two-phase commit* entre o Kafka e o seu Postgres. EOS é uma garantia **interna ao Kafka**.

## Como funciona

### KafkaTransactionManager e transactional.id

No Spring Boot, basta definir o prefixo de id transacional no produtor:

```yaml
spring:
  kafka:
    producer:
      transaction-id-prefix: order-processor-
```

Ao detectar esse prefixo, a `DefaultKafkaProducerFactory` passa a operar em modo transacional e o Boot autoconfigura um `KafkaTransactionManager`, ligando-o ao listener container. A factory mantém um **cache de produtores transacionais**: o `transactional.id` de cada produtor é `transaction-id-prefix` + um sufixo (`order-processor-0`, `order-processor-1`...).

Manualmente, a wiring é direta:

```java
@Bean
public KafkaTransactionManager<String, String> kafkaTransactionManager(
        ProducerFactory<String, String> producerFactory) {
    return new KafkaTransactionManager<>(producerFactory);
}
```

> [!warning] Mesma factory
> O `KafkaTemplate` precisa usar **a mesma `ProducerFactory`** do transaction manager, e essa factory tem que ser `transactionCapable()`. Se não, o template produz fora da transação que você acha que abriu.

### read-process-write atômico

O padrão canônico: o listener consome, processa e produz, tudo sob uma transação iniciada pelo container. O ponto sutil é o **lado do consumidor downstream** — quem vai ler o tópico de saída precisa de `read_committed`:

```yaml
spring:
  kafka:
    consumer:
      isolation-level: read_committed
```

O default do Kafka é `read_uncommitted`, ou seja, o consumidor enxerga mensagens de transações ainda não comitadas (e até de transações abortadas). Com `read_committed`, ele só lê até o **last stable offset (LSO)** — só o que foi efetivamente comitado. Sem isso, todo o esforço transacional do produtor vaza: alguém lá embaixo lê dados de transações que foram abortadas.

A atomicidade do ciclo vem de o avanço do offset de leitura ser enviado **dentro da transação de produção**. Container transacional + `read_committed` no downstream = read-process-write end-to-end dentro do Kafka.

### EOS v2 e o LIMITE crítico

Aqui está a fronteira que separa o candidato que "ouviu falar de exactly-once" do que entendeu.

**EOS v2 garante exactly-once apenas para o que está dentro do Kafka.** Mensagem de entrada → mensagem de saída → offset: atômico. Ponto final do escopo da garantia.

O que NÃO está coberto: o efeito colateral num **sistema externo**. Se o seu processamento grava uma linha no banco *e* produz um evento no Kafka, você tem um **dual-write** — duas escritas em dois sistemas sem uma transação que abrace os dois. A transação Kafka pode comitar e o banco falhar (ou vice-versa). Não existe rollback cruzado.

A solução correta não é forçar um *two-phase commit* frágil: é o **[[03-Dominios/Tecnologia/Java/Mensageria/21 - O padrão Outbox|padrão Outbox]]**. Você grava o evento como uma linha numa tabela `outbox` *na mesma transação do banco* que altera o estado do domínio, e um processo separado publica essa linha no Kafka depois. Assim a escrita no domínio e o "intent de publicar" são atômicos no banco — e o Kafka entra só na etapa de entrega, onde idempotência (ver [[03-Dominios/Tecnologia/Java/Mensageria/20 - Idempotência — o pilar do at-least-once|Idempotência]]) cobre as eventuais republicações.

## Na prática

Pipeline de exemplo (domínios neutros): consumir eventos de pedido (`orders`), validar, e produzir eventos de pagamento (`payments`), tudo atômico dentro do Kafka.

```yaml
spring:
  kafka:
    bootstrap-servers: localhost:9092
    producer:
      transaction-id-prefix: payment-processor-
      acks: all
    consumer:
      group-id: payment-service
      isolation-level: read_committed
      enable-auto-commit: false
```

```java
@Component
public class PaymentProcessor {

    private final KafkaTemplate<String, PaymentEvent> kafkaTemplate;

    public PaymentProcessor(KafkaTemplate<String, PaymentEvent> kafkaTemplate) {
        this.kafkaTemplate = kafkaTemplate;
    }

    // Container transacional: o offset de 'orders' é comitado
    // DENTRO da mesma transação Kafka que produz em 'payments'.
    @KafkaListener(topics = "orders", groupId = "payment-service")
    @Transactional("kafkaTransactionManager")
    public void onOrder(OrderEvent order) {
        PaymentEvent payment = toPayment(order);
        kafkaTemplate.send("payments", payment.orderId(), payment);
        // se algo lançar daqui pra frente, a transação aborta:
        // a mensagem em 'payments' nunca fica visível pra read_committed,
        // e o offset de 'orders' não avança.
    }

    private PaymentEvent toPayment(OrderEvent order) {
        return new PaymentEvent(order.orderId(), order.amount());
    }
}
```

Quando precisar de uma transação Kafka *local* e pontual, fora de um listener, o `KafkaTemplate` oferece `executeInTransaction`:

```java
boolean ok = kafkaTemplate.executeInTransaction(t -> {
    t.send("payments", "order-1", payment1);
    t.send("payments", "order-2", payment2);
    return true; // commit ao retornar normal; rollback se lançar
});
```

> [!note] Order/Payment são placeholders
> `OrderEvent`/`PaymentEvent` são domínios genéricos só para ilustrar o read-process-write. Não há contrato real por trás deles.

## Armadilhas

### (1) Achar que a transação Kafka cobre a escrita no DB

A mais cara. O candidato configura `transaction-id-prefix`, vê o `@Transactional`, e conclui que produzir no Kafka + salvar no banco no mesmo método é atômico. **Não é** — é um dual-write. A transação Kafka cobre só o Kafka; a transação do banco cobre só o banco. Não há commit cruzado. Resultado: pagamento gravado no banco mas evento perdido (ou o inverso) quando um dos dois falha. A resposta certa é **Outbox**, não "confiar no `@Transactional`".

### (2) `transactional.id` reusado entre instâncias

Se duas instâncias da aplicação rodam com o **mesmo `transactional.id`**, o broker faz *fencing*: ele assume que a segunda é o "renascimento" da primeira (um produtor zumbi) e cerca uma delas, abortando suas transações. Em deploy escalado horizontalmente, o `transaction-id-prefix` precisa render ids **únicos por instância** (o Spring deriva ids estáveis por partição no read-process-write, mas o prefixo não pode colidir entre instâncias que não deveriam se cercar). Sintoma típico: `ProducerFencedException` e transações abortando sozinhas.

### (3) Misturar produção transacional e não-transacional no mesmo template

Um `KafkaTemplate` cuja `ProducerFactory` tem `transaction-id-prefix` é transacional. Tentar usá-lo para um `send` "solto" fora de qualquer transação — ou misturar ele com um template não-transacional sobre estados diferentes — gera comportamento confuso: ou o send exige uma transação ativa, ou você acha que comitou algo que ficou pendente. Decida por template: ou é transacional (e todo uso passa por transação / `executeInTransaction`), ou não é. Não misture os dois papéis no mesmo bean.

## Em entrevista

### Frase pronta (inglês)

"Kafka transactions make the read-process-write cycle atomic: consuming from an input topic, producing to output topics, and committing the consumer offsets all succeed or all abort together, driven in Spring by a `KafkaTransactionManager` and a stable `transactional.id`. The crucial caveat I always stress is that exactly-once semantics is internal to Kafka — it covers messages and offsets within the broker, but it does not span an external database. A method that both writes to Postgres and produces to Kafka is a dual-write, not a distributed transaction, so for end-to-end correctness I reach for the Outbox pattern plus idempotent consumers rather than pretending `@Transactional` gives me cross-system atomicity. On the consumer side I also make sure downstream readers run with `isolation.level=read_committed`, otherwise they'd see uncommitted or aborted records and the whole transactional effort leaks."

### Vocabulário

| Termo PT | Termo EN |
|---|---|
| id transacional | transactional.id |
| cercamento / produtor zumbi | fencing / zombie producer |
| último offset estável | last stable offset (LSO) |
| leitura confirmada | read_committed |
| semântica exatamente-uma-vez v2 | EOS v2 |
| escrita dupla | dual-write |
| lê-processa-escreve | read-process-write |

## Veja também

- [[03-Dominios/Tecnologia/Java/Mensageria/index|Mensageria (MOC do galho)]]
- [[03-Dominios/Tecnologia/Java/index|Trilha Java]]
- [[03-Dominios/Tecnologia/Java/Mensageria/03 - Garantias de entrega — e a falácia do exactly-once|Garantias de entrega]]
- [[03-Dominios/Tecnologia/Java/Mensageria/20 - Idempotência — o pilar do at-least-once|Idempotência]]
- [[03-Dominios/Tecnologia/Java/Mensageria/21 - O padrão Outbox|O padrão Outbox]]
- [[03-Dominios/Tecnologia/Java/Dicionário de Java|Dicionário de Java]]

## Referências

- Spring for Apache Kafka — Reference, seção *Transactions* (`KafkaTransactionManager`, `transactionIdPrefix`, `EOSMode.V2`): https://docs.spring.io/spring-kafka/reference/kafka/transactions.html
- Apache Kafka — Documentation (delivery semantics, transactions): https://kafka.apache.org/documentation/
- Confluent Platform — Consumer Configurations, `isolation.level` (`read_committed` / `read_uncommitted`, default `read_uncommitted`, last stable offset): https://docs.confluent.io/platform/current/installation/configuration/consumer-configs.html
- Confluent Platform — Exactly-once semantics: https://docs.confluent.io/platform/current/
