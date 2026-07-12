---
title: "Python — Mensageria"
created: 2026-07-12
type: moc
status: growing
publish: true
tags:
  - python
  - moc
aliases:
  - "Galho 14 - Mensageria"
---

# Mensageria

> [!abstract] TL;DR
> Galho 14 da trilha Python: o ferramental Python de mensageria — Celery (task queue sobre Redis/RabbitMQ, workers, retries, Beat), RQ (fila mais simples sobre Redis, contraste direto com Celery), aio-pika (cliente assíncrono RabbitMQ), kafka-python/aiokafka (producer/consumer Kafka), e a aplicação prática de garantias de entrega (idempotência, DLQ, Outbox) em código Python real. Fecha com capstone dando processamento assíncrono à API de Tarefas hexagonal do Galho 13. Fase Adepto→Magus; 8 notas. Primeiro galho do bloco "Plataforma distribuída e produção" (14-18).

## Sobre este galho

Este galho é **ferramental**, não teoria — os conceitos de mensageria (fila vs streaming, garantias de entrega, Outbox/Saga, o legado enterprise) já estão cobertos em profundidade e de forma agnóstica de linguagem em [[03-Dominios/Engenharia/Comunicação entre Sistemas/4 - Comunicação assíncrona/index|Comunicação entre Sistemas — Comunicação assíncrona]], e os brokers em si (Kafka, RabbitMQ) têm páginas dedicadas em [[03-Dominios/Engenharia/Comunicação entre Sistemas/Mensageria/index|Comunicação entre Sistemas — Mensageria]]. Este galho referencia os dois sem repetir, e foca no que muda: como Python fala com esses brokers na prática.

**Fronteiras anti-duplicação:** message queue vs event streaming, garantias de entrega (at-least-once/exactly-once/ordenação), Outbox/Saga como padrões conceituais, e o legado enterprise → [[03-Dominios/Engenharia/Comunicação entre Sistemas/4 - Comunicação assíncrona/index|Comunicação assíncrona]] (SG4), só referenciados. O que Kafka/RabbitMQ SÃO (arquitetura interna, conceitos de partição/exchange) → [[03-Dominios/Engenharia/Comunicação entre Sistemas/Mensageria/index|Mensageria (Engenharia)]], só referenciado. `asyncio`/event loop → Galhos 7-8 desta trilha, não repetido (usado em `aio-pika`/`aiokafka`). Domain Events como conceito arquitetural → Galho 13 desta trilha (capstone), aqui é onde eles finalmente saem pro mundo via broker real.

**Audiência:** quem já tem a API de Tarefas construída, blindada, testada e arquiteturalmente organizada (Galhos 9-13) e precisa desacoplar processamento pesado/notificações em processamento assíncrono de verdade.

## Adepto

1. [[01 - Panorama — Celery vs RQ vs aio-pika vs aiokafka|01 — Panorama: Celery vs RQ vs aio-pika vs aiokafka]]
2. [[02 - Celery fundamentos — broker, worker e tasks|02 — Celery fundamentos: broker, worker e tasks]]
3. [[03 - Celery em produção — retries, idempotência e Celery Beat|03 — Celery em produção: retries, idempotência e Celery Beat]]
4. [[04 - RQ — a fila simples sobre Redis|04 — RQ: a fila simples sobre Redis]]

## Adepto→Magus

5. [[05 - aio-pika — RabbitMQ assíncrono|05 — aio-pika: RabbitMQ assíncrono]]
6. [[06 - kafka-python e aiokafka — producer e consumer|06 — kafka-python e aiokafka: producer e consumer]]

## Magus

7. [[07 - Garantias de entrega na prática — DLQ e Outbox em Python|07 — Garantias de entrega na prática: DLQ e Outbox em Python]]
8. [[08 - Capstone — processamento assíncrono na API de Tarefas|08 — Capstone: processamento assíncrono na API de Tarefas]] — recapitula o galho.

## Todas as notas

```dataview
TABLE fase, status FROM "03-Dominios/Tecnologia/Python/Mensageria" WHERE type = "concept" SORT file.name ASC
```

## Veja também

- [[03-Dominios/Tecnologia/Python/index|Trilha Python]] (MOC central)
- [[03-Dominios/Engenharia/Comunicação entre Sistemas/4 - Comunicação assíncrona/index|Comunicação entre Sistemas — Comunicação assíncrona]] — conceitos de mensageria, agnósticos de linguagem
- [[03-Dominios/Engenharia/Comunicação entre Sistemas/Mensageria/index|Comunicação entre Sistemas — Mensageria]] — Kafka/RabbitMQ/BullMQ como ferramentas
- [[03-Dominios/Tecnologia/Java/Mensageria/index|Java — Mensageria]] — trilha irmã, mesmo papel (Spring Kafka/AMQP)
- [[03-Dominios/Tecnologia/Python/Arquitetura e Design Patterns/index|Arquitetura e Design Patterns]] — Galho 13 (Domain Events, Ports and Adapters — a API que este galho conecta a brokers reais)
- [[03-Dominios/Tecnologia/Python/Programação Reativa e Assíncrona/index|Programação Reativa e Assíncrona]] — Galho 8 (asyncio, usado por aio-pika/aiokafka)
