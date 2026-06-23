---
title: "Mensageria"
type: moc
publish: true
created: 2026-05-21
updated: 2026-05-21
status: seedling
tags:
  - moc
  - arquitetura
  - mensageria
aliases:
  - Messaging
---
# Mensageria

> [!abstract] TL;DR
> Galho de Mensageria dentro de Arquitetura — message brokers, event streaming e filas de trabalho. Cobre os principais players: Kafka, RabbitMQ e BullMQ.

Mensageria é o tecido que conecta serviços desacoplados em sistemas distribuídos. Esta estante separa os conceitos por estilo: brokers tradicionais orientados a fila (RabbitMQ), plataformas de event streaming com log append-only (Kafka) e filas de jobs em background apoiadas em Redis (BullMQ). A nota-mãe traz o panorama; as notas-filhas detalham cada ferramenta.

## Conteúdo

- [[Mensageria]] — visão geral do tema
- [[Event Streaming]] — modelo de streaming de eventos
- [[03-Dominios/Engenharia/Comunicação entre Sistemas/Mensageria/Kafka]] — plataforma de event streaming
- [[RabbitMQ]] — message broker AMQP
- [[BullMQ]] — fila de jobs sobre Redis

## Veja também

- [[03-Dominios/Engenharia/Arquitetura/index|Arquitetura]]
