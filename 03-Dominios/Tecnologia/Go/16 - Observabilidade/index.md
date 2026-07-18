---
title: "Go — Observabilidade"
type: moc
publish: true
created: 2026-07-18
updated: 2026-07-18
status: growing
tags:
  - moc
  - go
  - observabilidade
  - pprof
  - otel
aliases:
  - Galho 16 Go
---
# Go — Observabilidade

> [!abstract] TL;DR
> Galho 16 da trilha [[03-Dominios/Tecnologia/Go/index|Go]] — como enxergar o que um serviço Go está fazendo em produção. 8 notas em 3 fases: os três pilares e logging estruturado com `slog` (Iniciado); profiling com `pprof`, métricas Prometheus e `expvar` (Adepto); tracing distribuído com OpenTelemetry e a prática de observar em produção (Magus). Ao fim, você sabe instrumentar, coletar e interpretar sinais de um serviço Go rodando de verdade.

Observabilidade em Go tem uma vantagem rara: o runtime já vem instrumentado — `pprof` e `expvar` são biblioteca padrão, não dependência externa. Este galho parte desse alicerce nativo e sobe até o ecossistema padrão de produção (Prometheus, OpenTelemetry). Ver [[roadmap]] pro estado das notas.

## Notas por fase

### Iniciado — os sinais básicos

1. [[01 - Os três pilares em Go]] — logs, métricas e traces; o que cada um responde e como se complementam
2. [[02 - Logging estruturado com slog]] — `log/slog`, handlers, níveis, contexto e correlação de logs

### Adepto — instrumentando o runtime

3. [[03 - pprof — CPU e memória]] — `net/http/pprof`, perfis de CPU/heap/goroutine, coleta em produção
4. [[04 - Analisando profiles]] — `go tool pprof`, flame graphs, identificando hot paths e vazamentos
5. [[05 - Métricas com Prometheus]] — client_golang, counters/gauges/histograms, exposição `/metrics`
6. [[06 - expvar e runtime metrics]] — `expvar` da stdlib, `runtime.MemStats`, métricas do GC e goroutines

### Magus — tracing e produção

7. [[07 - OpenTelemetry — tracing]] — spans, contexto de propagação, exporters, instrumentação de HTTP/gRPC
8. [[08 - Observabilidade em produção]] — correlação logs/métricas/traces, SLOs, dashboards, custo de instrumentar

## Veja também

- [[03-Dominios/Tecnologia/Go/index|Trilha Go]] — índice geral (21 galhos + capstone)
- Galho anterior: [[03-Dominios/Tecnologia/Go/15 - Testes/index|Testes]]
- Próximo galho: **Runtime interno** (galho 17) — o que acontece por baixo do que este galho observa de fora
