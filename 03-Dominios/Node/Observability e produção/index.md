---
title: "Observability e produção"
created: 2026-05-08
updated: 2026-05-08
type: moc
status: seedling
publish: true
tags:
  - node
  - observability
  - producao
  - moc
aliases:
  - Observability Node
  - Galho 5 - Observability
---

# Observability e produção

> [!abstract] TL;DR
> Galho 5 da trilha Node Senior.
> Cobre os três pilares de observability (logs, métricas, traces) com ferramentas idiomáticas do ecossistema (pino, prom-client, OpenTelemetry).
> Diagnóstico avançado de performance e memória (clinic.js, heap snapshots).
> Patterns de resiliência que toda API precisa conhecer (graceful shutdown, circuit breaker, connection pool tuning). Pré-requisitos: galho 1 (Runtime e Event Loop) e galho 4 (Frameworks e arquitetura).

## Sobre este galho

Este galho cobre **observability e produção em Node.js**: os três pilares (logs, métricas, traces), golden signals, SLO/SLA, ferramentas idiomáticas do ecossistema (pino, prom-client, OpenTelemetry), diagnóstico avançado (clinic.js, heap snapshots) e patterns de resiliência (graceful shutdown, circuit breaker, connection pool tuning).

**Pré-requisitos:**
- [[03-Dominios/Node/Runtime e Event Loop/index]] (galho 1) — event loop phases, libuv thread pool, bloqueio — necessário para entender event loop lag e clinic.js
- [[03-Dominios/Node/Frameworks e arquitetura/index]] (galho 4) — middleware pipeline e hooks de shutdown nos frameworks

**Audiência primária:** dev senior em prep para entrevista internacional. Cada nota tem seção "Em entrevista" com frase pronta em inglês + vocabulário PT→EN.

**Audiência secundária:** o mesmo dev instrumentando ou debugando uma API em produção.

## Comece por aqui — trilha completa (12 notas)

### Bloco A — Visão geral

1. [[01 - Os três pilares - logs, métricas e traces]]

### Bloco B — Os três pilares

2. [[02 - Logging estruturado com pino]]
3. [[03 - Correlation IDs e context propagation]]
4. [[04 - Métricas com prom-client]]
5. [[05 - Node-specific metrics - event loop lag, GC, heap]]
6. [[06 - Tracing distribuído com OpenTelemetry]]

### Bloco C — Diagnóstico avançado

7. [[07 - Profiling avançado com clinic.js]]
8. [[08 - Detecção e diagnóstico de memory leaks]]

### Bloco D — Resiliência

9. [[09 - Graceful shutdown profundo]]
10. [[10 - Circuit breaker e fallback com opossum]]
11. [[11 - Connection pool tuning]]

### Bloco E — Fechamento

12. [[12 - SLOs, dashboards, alertas e cheatsheet]]

## Rotas alternativas

### Rota entrevista internacional

01 → 02 → 04 → 06 → 09 → 10 → 12. Foco em explicar os três pilares e patterns de resiliência para entrevistador.

### Rota produção e debugging

01 → 07 → 08 → 09 → 11 → 12. Para quem está debugando um problema em produção agora.

### Rota Node-specific metrics

04 → 05 → 07 → 12. Para instrumentar métricas específicas do runtime Node (event loop lag, GC, heap).

### Rota resiliência/SRE

09 → 10 → 11 → 12. Para quem está configurando resiliência numa API existente.

### Rota OpenTelemetry completa

01 → 03 → 06 → 12. Para quem quer entender distributed tracing do zero.

## Todas as notas

```dataview
TABLE status, updated
FROM "03-Dominios/Node/Observability e produção"
WHERE type = "concept"
SORT file.name ASC
```

## Veja também

- [[03-Dominios/Node/index|Node.js (MOC central)]]
- [[Node.js]] — tronco
- [[03-Dominios/Node/Runtime e Event Loop/index]] — galho 1
- [[03-Dominios/Node/Paralelismo/index]] — galho 2
- [[03-Dominios/Node/Streams/index]] — galho 3
- [[03-Dominios/Node/Frameworks e arquitetura/index]] — galho 4
