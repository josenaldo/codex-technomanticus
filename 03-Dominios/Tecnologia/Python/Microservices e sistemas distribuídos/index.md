---
title: "Python — Microservices e sistemas distribuídos"
created: 2026-07-12
type: moc
status: growing
publish: true
tags:
  - python
  - moc
aliases:
  - "Galho 15 - Microservices e sistemas distribuídos"
---

# Microservices e sistemas distribuídos

> [!abstract] TL;DR
> Galho 15 da trilha Python: como um serviço Python se comunica com outros serviços em produção — cliente HTTP (`httpx`) com timeouts/connection pooling, resiliência na prática (`tenacity` pra retry, `pybreaker`/`circuitbreaker` pra circuit breaker), consumo de API Gateway (autenticação serviço-a-serviço, awareness de rate limit), tracing distribuído com OpenTelemetry, Saga orquestrada em código Python. Fecha com capstone extraindo um segundo serviço da API de Tarefas. Fase Magus; 8 notas. Segundo galho do bloco "Plataforma distribuída e produção" (14-18).

## Sobre este galho

Este galho é **ferramental e aplicado**, não teoria de sistemas distribuídos — os conceitos (CAP, consistência eventual, Circuit Breaker, API Gateway/BFF, service discovery) já estão cobertos em profundidade e de forma agnóstica de linguagem na trilha [[03-Dominios/Engenharia/Arquitetura/System Design/index|System Design]], e os contratos de comunicação (REST/GraphQL/gRPC, idempotência, versionamento, rate limiting, webhooks) já estão em [[03-Dominios/Engenharia/Comunicação entre Sistemas/index|Comunicação entre Sistemas]]. Este galho referencia os dois sem repetir, e foca em como CÓDIGO Python real implementa essas ideias — client HTTP resiliente, consumo de gateway, tracing, Saga.

**Fronteiras anti-duplicação:** CAP/consistência/consenso, Circuit Breaker como padrão, API Gateway/BFF como conceito → [[03-Dominios/Engenharia/Arquitetura/System Design/index|System Design]] (SG2/SG3), só referenciados. Contratos REST/GraphQL/gRPC, idempotência, rate limiting, webhooks → [[03-Dominios/Engenharia/Comunicação entre Sistemas/index|Comunicação entre Sistemas]], só referenciados. Mensageria/Outbox/DLQ → Galho 14 desta trilha, já construído, reusado aqui. Domain Events/arquitetura hexagonal → Galho 13 desta trilha, reusado. Observabilidade de produção em profundidade (logging estruturado, métricas, dashboards) → Galho 17 futuro desta trilha, só tracing é tocado aqui.

**Audiência:** quem já tem a API de Tarefas construída, testada, arquiteturalmente organizada e publicando eventos (Galhos 9-14) e precisa entender como ela conversa com OUTROS serviços Python de forma resiliente e observável.

## Magus

1. [[01 - Panorama — de monolito modular a microservices em Python|01 — Panorama: de monolito modular a microservices em Python]]
2. [[02 - Comunicação síncrona entre serviços — httpx|02 — Comunicação síncrona entre serviços: httpx]]
3. [[03 - Resiliência na prática — tenacity e circuit breaker|03 — Resiliência na prática: tenacity e circuit breaker]]
4. [[04 - Cliente de API Gateway — autenticação serviço-a-serviço|04 — Cliente de API Gateway: autenticação serviço-a-serviço]]
5. [[05 - Service discovery na prática|05 — Service discovery na prática]]
6. [[06 - Tracing distribuído com OpenTelemetry|06 — Tracing distribuído com OpenTelemetry]]
7. [[07 - Saga orquestrada em Python|07 — Saga orquestrada em Python]]
8. [[08 - Capstone — extraindo o serviço de Notificações|08 — Capstone: extraindo o serviço de Notificações]] — recapitula o galho.

## Veja também

- [[03-Dominios/Tecnologia/Python/index|Trilha Python]] (MOC central)
- [[03-Dominios/Engenharia/Arquitetura/System Design/index|System Design]] — conceitos de sistemas distribuídos em escala, agnósticos de linguagem
- [[03-Dominios/Engenharia/Comunicação entre Sistemas/index|Comunicação entre Sistemas]] — contratos REST/GraphQL/gRPC, confiabilidade
- [[03-Dominios/Tecnologia/Python/Mensageria/index|Mensageria]] — Galho 14 (broker/Outbox/DLQ, reusados aqui)
- [[03-Dominios/Tecnologia/Python/Arquitetura e Design Patterns/index|Arquitetura e Design Patterns]] — Galho 13 (Domain Events, hexagonal)
- [[03-Dominios/Tecnologia/Java/Microservices e sistemas distribuídos/index|Java — Microservices e sistemas distribuídos]] — trilha irmã, mesmo papel (Spring Cloud)
