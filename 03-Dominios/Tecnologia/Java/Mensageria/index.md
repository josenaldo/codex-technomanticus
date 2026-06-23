---
title: "Mensageria e eventos"
created: 2026-06-11
updated: 2026-06-11
type: moc
status: growing
publish: true
tags:
  - java
  - mensageria
  - moc
aliases:
  - "Mensageria e eventos"
  - "Mensageria"
  - "Messaging"
  - "Event-Driven"
  - "Galho 14 - Mensageria"
---

# Mensageria e eventos

> [!abstract] TL;DR
> O **Galho 14** cobre a **camada de aplicação Java/Spring da mensageria**: o modelo e as garantias de entrega, Spring Kafka e RabbitMQ, eventos in-process, padrões de confiabilidade (idempotência, outbox, DLQ, exactly-once), arquitetura event-driven (saga, event sourcing, CQRS), mensageria reativa, observabilidade e o contraste com gRPC. **A tese honesta: mensageria é desacoplamento, não velocidade — e o exactly-once distribuído é um mito que se resolve com idempotência.** São **29 notas** em 3 fases (Iniciado, Adepto, Magus).

## Sobre este galho

Mensageria é o **desacoplamento temporal e espacial** entre quem produz e quem consome um evento: o produtor publica um fato sem saber quem (ou quando) vai reagir. Este galho parte do modelo (comando vs evento, queue vs topic, garantias de entrega), percorre o ferramental Spring (Spring Kafka produção/consumo/erro/transação, Spring AMQP/RabbitMQ, Spring Cloud Stream, eventos in-process), sobe para os padrões de confiabilidade e arquitetura (idempotência, outbox, saga, event sourcing, CQRS, versionamento) e fecha com o contraste **RPC síncrono (gRPC) vs mensageria assíncrona**.

**Audiência primária:** dev pleno/sênior em preparação para entrevista internacional que precisa explicar arquitetura orientada a eventos com critério. **Secundária:** quem mantém um stack Kafka/RabbitMQ e precisa decidir broker, garantir confiabilidade e reconhecer quando o desacoplamento não vale o custo.

É um **galho novo/pesquisa** (doc oficial via WebFetch — Spring Kafka, Spring AMQP, Spring Cloud Stream, Kafka, Confluent, RabbitMQ, Reactor Kafka, Debezium, protobuf.dev, grpc.io), que **coexiste** com o cluster de infra-Kafka já existente no vault: este galho é a **camada de aplicação** e **não re-explica os internals do Kafka** (partições, offsets, replication, consumer groups, KRaft) — ele linka para [[03-Dominios/Tecnologia/Java/Backend/Kafka/index|Kafka (a infra)]]. Migra também o antigo `gRPC e Go.md` para as notas de Protobuf/gRPC em ângulo Java.

**A tese central, sem hype:** mensageria troca acoplamento por complexidade operacional — só vale quando o desacoplamento paga esse custo. O `exactly-once` distribuído ponta-a-ponta é majoritariamente um mito: a entrega é **at-least-once** e o efeito exactly-once vem de **consumidor idempotente**. Por isso confiabilidade (idempotência, outbox, DLQ) e "quando **não** usar broker" (o event bus in-process basta; ou o RPC síncrono é melhor) são parte central do galho.

**Fronteira-assinatura (sêxtupla):** os internals do Kafka ficam no [[03-Dominios/Tecnologia/Java/Backend/Kafka/index|cluster de infra]]; o event bus in-process é o [[03-Dominios/Tecnologia/Java/Spring Core e Boot/11 - Eventos do ApplicationContext|Galho 8]]; a transação do outbox é o [[03-Dominios/Tecnologia/Java/Persistência de dados/12 - Transações operacionais — @Transactional propagação, isolamento, rollback, readOnly|Galho 10]]; o reativo é o [[03-Dominios/Tecnologia/Java/Programação Reativa/index|Galho 11]]; as threads de consumo são o [[03-Dominios/Tecnologia/Java/Concorrência e paralelismo/index|Galho 4]]; testar mensageria é o [[03-Dominios/Tecnologia/Java/Testes/11 - Testcontainers — infra real em testes|Galho 13]]. As notas linkam de volta a essas fronteiras sem re-explicá-las.

## Iniciado

O modelo mental — antes de qualquer API.

1. [[03-Dominios/Tecnologia/Java/Mensageria/01 - O que é mensageria e arquitetura orientada a eventos|01 — O que é mensageria e arquitetura orientada a eventos]] — síncrono vs assíncrono, desacoplamento temporal/espacial, comando vs evento; por que mensageria não é "velocidade".
2. [[03-Dominios/Tecnologia/Java/Mensageria/02 - Os modelos de mensageria — queue vs topic|02 — Os modelos de mensageria (queue vs topic)]] — point-to-point vs publish-subscribe, o broker como intermediário, JMS como spec histórica.
3. [[03-Dominios/Tecnologia/Java/Mensageria/03 - Garantias de entrega — e a falácia do exactly-once|03 — Garantias de entrega e a falácia do exactly-once]] — at-most/at-least/exactly-once e por que o exactly-once distribuído se resolve com idempotência.
4. [[03-Dominios/Tecnologia/Java/Mensageria/04 - O ecossistema de brokers na JVM|04 — O ecossistema de brokers na JVM]] — Kafka vs RabbitMQ vs Artemis vs cloud; critérios de escolha.
5. [[03-Dominios/Tecnologia/Java/Mensageria/05 - Kafka numa página para o dev de aplicação|05 — Kafka numa página para o dev de aplicação]] — log/tópico/partição/offset na visão de app; KRaft (Zookeeper removido no Kafka 4.0); linka a infra.
6. [[03-Dominios/Tecnologia/Java/Mensageria/06 - Spring para mensageria — o panorama|06 — Spring para mensageria (o panorama)]] — Spring Kafka, Spring AMQP, Spring Cloud Stream, Spring Integration: o que cada um resolve.

## Adepto

Spring Kafka, RabbitMQ e eventos in-process.

7. [[03-Dominios/Tecnologia/Java/Mensageria/07 - KafkaTemplate — produzindo mensagens|07 — KafkaTemplate (produzindo mensagens)]] — `send`, serializers, chave→partição, send assíncrono, `acks`/`linger.ms`/idempotent producer.
8. [[03-Dominios/Tecnologia/Java/Mensageria/08 - @KafkaListener — consumindo mensagens|08 — @KafkaListener (consumindo mensagens)]] — o listener container, `ConcurrentKafkaListenerContainerFactory`, concorrência × partições, group, `auto.offset.reset`.
9. [[03-Dominios/Tecnologia/Java/Mensageria/09 - (De)serialização de mensagens|09 — (De)serialização de mensagens]] — `JsonSerializer`/type headers/`trusted.packages`, `ErrorHandlingDeserializer` e o poison pill.
10. [[03-Dominios/Tecnologia/Java/Mensageria/10 - Ack modes e commit de offset|10 — Ack modes e commit de offset]] — `AckMode`, auto-commit desligado, at-least-once na prática, `Acknowledgment`.
11. [[03-Dominios/Tecnologia/Java/Mensageria/11 - Tratamento de erro no consumo|11 — Tratamento de erro no consumo]] — `DefaultErrorHandler` (ex-`SeekToCurrentErrorHandler`), backoff, exceções não-retentáveis.
12. [[03-Dominios/Tecnologia/Java/Mensageria/12 - Dead Letter Topic — o padrão DLQ|12 — Dead Letter Topic (o padrão DLQ)]] — `DeadLetterPublishingRecoverer`, `@RetryableTopic`, DLT/`*-dlt`; DLX no RabbitMQ.
13. [[03-Dominios/Tecnologia/Java/Mensageria/13 - Transações e exactly-once no Spring Kafka|13 — Transações e exactly-once no Spring Kafka]] — `KafkaTransactionManager`, read-process-write, `isolation.level=read_committed`, EOS v2 e seu limite.
14. [[03-Dominios/Tecnologia/Java/Mensageria/14 - Schema e contratos — Avro e Schema Registry|14 — Schema e contratos (Avro e Schema Registry)]] — por que schema, Avro + Schema Registry, compatibilidade fwd/bwd/full.
15. [[03-Dominios/Tecnologia/Java/Mensageria/15 - Spring AMQP e RabbitMQ|15 — Spring AMQP e RabbitMQ]] — exchange/binding/queue/routing, `@RabbitListener`, quorum queues/streams; Kafka vs RabbitMQ.
16. [[03-Dominios/Tecnologia/Java/Mensageria/16 - Eventos in-process do Spring|16 — Eventos in-process do Spring]] — `@TransactionalEventListener` (AFTER_COMMIT); quando o event bus interno substitui um broker.
17. [[03-Dominios/Tecnologia/Java/Mensageria/17 - Spring Cloud Stream — a abstração de binders|17 — Spring Cloud Stream (a abstração de binders)]] — o modelo funcional (`Supplier`/`Function`/`Consumer`), binders; quando a indireção vale.
18. [[03-Dominios/Tecnologia/Java/Mensageria/18 - Kafka Streams pela API Java|18 — Kafka Streams pela API Java]] — `KStream`/`KTable`, topologia, stateless vs stateful, state stores.

## Magus

Arquitetura, confiabilidade e o contraste RPC.

19. [[03-Dominios/Tecnologia/Java/Mensageria/19 - Kafka Connect pela ótica da app|19 — Kafka Connect pela ótica da app]] — source/sink, quando usar Connect vs produzir você mesmo; Connect é infra.
20. [[03-Dominios/Tecnologia/Java/Mensageria/20 - Idempotência — o pilar do at-least-once|20 — Idempotência (o pilar do at-least-once)]] — por que at-least-once exige consumidor idempotente; dedup keys, idempotent producer.
21. [[03-Dominios/Tecnologia/Java/Mensageria/21 - O padrão Outbox|21 — O padrão Outbox]] — o dual-write problem; transactional outbox + relay; CDC com Debezium.
22. [[03-Dominios/Tecnologia/Java/Mensageria/22 - Saga — transações distribuídas por eventos|22 — Saga (transações distribuídas por eventos)]] — transações locais + eventos; coreografia vs orquestração; compensação.
23. [[03-Dominios/Tecnologia/Java/Mensageria/23 - Event sourcing e CQRS|23 — Event sourcing e CQRS]] — o evento como fonte da verdade; read models; quando (não) usar.
24. [[03-Dominios/Tecnologia/Java/Mensageria/24 - Versionamento e evolução de eventos|24 — Versionamento e evolução de eventos]] — eventos como contratos duráveis; schema evolution; compat fwd/bwd.
25. [[03-Dominios/Tecnologia/Java/Mensageria/25 - Mensageria reativa — Reactor Kafka|25 — Mensageria reativa (Reactor Kafka)]] — `KafkaReceiver`/`KafkaSender`, backpressure no consumo; quando o reativo paga.
26. [[03-Dominios/Tecnologia/Java/Mensageria/26 - Observabilidade em mensageria|26 — Observabilidade em mensageria]] — consumer lag, tracing distribuído através do broker, métricas.
27. [[03-Dominios/Tecnologia/Java/Mensageria/27 - Protocol Buffers — a IDL e a serialização binária|27 — Protocol Buffers (a IDL e a serialização binária)]] — `.proto` proto3, serialização binária, schema evolution; toolchain Java.
28. [[03-Dominios/Tecnologia/Java/Mensageria/28 - gRPC em Java — RPC síncrono sobre HTTP_2|28 — gRPC em Java (RPC síncrono sobre HTTP/2)]] — os 4 tipos de chamada, HTTP/2; gRPC vs REST vs mensageria.
29. [[03-Dominios/Tecnologia/Java/Mensageria/29 - Capstone — uma mensagem de ponta a ponta|29 — Capstone (uma mensagem de ponta a ponta)]] — o fluxo completo (outbox → tópico → consumidor idempotente → DLQ → observabilidade) e o mapa de decisão.

## Rotas alternativas

- **Completa** — 01 → 29 em ordem (o caminho do modelo ao capstone).
- **Entrevista internacional** — 01 → 03 → 07 → 08 → 12 → 20 → 21 → 22 → 28 → 29 (modelo, garantias, produzir/consumir, DLQ, idempotência, outbox, saga, gRPC, capstone — o que mais cai).
- **Spring Kafka operacional** — 05 → 07 → 08 → 09 → 10 → 11 → 12 → 13 (Kafka, produção, consumo, serialização, ack, erro, DLQ, transação).
- **Confiabilidade e arquitetura event-driven** — 03 → 20 → 21 → 22 → 23 → 24 (garantias, idempotência, outbox, saga, event sourcing/CQRS, versionamento).
- **Síncrono vs assíncrono (a ponte com o gRPC)** — 01 → 02 → 27 → 28 → 29 (modelo, queue vs topic, Protobuf, gRPC, o mapa de decisão).

## Todas as notas

```dataview
TABLE fase AS "Fase", status AS "Status"
FROM "03-Dominios/Tecnologia/Java/Mensageria"
WHERE type = "concept"
SORT file.name ASC
```

## Veja também

- [[03-Dominios/Tecnologia/Java/index|Trilha Java (MOC central)]]
- [[03-Dominios/Tecnologia/Java/Backend/Kafka/index|Kafka]] — o cluster de infra (internals do Kafka) sobre o qual este galho roda
- [[03-Dominios/Tecnologia/Java/Spring Core e Boot/11 - Eventos do ApplicationContext|Eventos do ApplicationContext]] — o event bus in-process (Galho 8)
- [[03-Dominios/Tecnologia/Java/Concorrência e paralelismo/index|Concorrência e paralelismo]] — as threads de consumo (Galho 4)
- [[03-Dominios/Tecnologia/Java/Programação Reativa/index|Programação Reativa]] — a mensageria reativa/Reactor Kafka (Galho 11)
- [[03-Dominios/Tecnologia/Java/Testes/11 - Testcontainers — infra real em testes|Testes]] — testar mensageria com Testcontainers/Awaitility (Galho 13)
- [[03-Dominios/Tecnologia/Java/Dicionário de Java|Dicionário de Java]] — glossário de termos da trilha

> Galhos 15 (Build e tooling), 16 (Microservices), 17 (Cloud-native e produção) e 18 (Certificação OCP) — planejados.
