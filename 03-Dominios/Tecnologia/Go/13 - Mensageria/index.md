---
title: "Go — Mensageria"
type: moc
publish: true
created: 2026-07-18
updated: 2026-07-18
status: growing
tags:
  - moc
  - go
  - mensageria
  - kafka
  - nats
aliases:
  - Galho 13 Go
---
# Go — Mensageria

> [!abstract] TL;DR
> Galho 13 da trilha [[03-Dominios/Tecnologia/Go/index|Go]] — comunicação assíncrona entre serviços via filas e tópicos. 7 notas em 3 fases: por que desacoplar com mensageria (Iniciado); Kafka em Go, NATS em Go e o padrão de consumers/workers (Adepto); garantias de entrega/idempotência, retry/DLQ/backpressure e padrões de processamento (Magus). Ao fim, você projeta pipelines assíncronos resilientes em Go, sabendo quando trocar chamada síncrona por mensagem.

Mensageria é a resposta de Go pra desacoplamento temporal entre serviços: produtor e consumidor não precisam estar de pé ao mesmo tempo, e falhas de um lado não derrubam o outro. Ver [[roadmap]] pro estado das notas.

## Notas por fase

### Iniciado — por que mensageria

1. [[01 - Por que mensageria — desacoplamento]] — acoplamento temporal vs síncrono, quando trocar HTTP por mensagem, trade-offs

### Adepto — as ferramentas

2. [[02 - Kafka em Go]] — client (segmentio/kafka-go ou confluent-kafka-go), producer/consumer, partições, offsets
3. [[03 - NATS em Go]] — pub/sub, request/reply, JetStream, comparação com Kafka
4. [[04 - Consumers e workers]] — worker pools, consumer groups, graceful shutdown, concorrência no consumo

### Magus — garantias e resiliência

5. [[05 - Entrega e idempotência]] — at-most-once/at-least-once/exactly-once, chaves de idempotência, deduplicação
6. [[06 - Retry, DLQ e backpressure]] — retry com backoff, dead letter queue, controle de fluxo sob carga
7. [[07 - Padrões de processamento]] — pipeline, fan-out/fan-in, outbox pattern, saga

## Veja também

- [[03-Dominios/Tecnologia/Go/index|Trilha Go]] — índice geral (21 galhos + capstone)
- Próximo galho: **Microservices e arquitetura** (galho 14) — onde os serviços conectados por mensageria ganham fronteiras e contratos formais
