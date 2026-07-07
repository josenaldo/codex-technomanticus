---
title: "Roadmap — Padrões recorrentes"
created: 2026-07-07
type: meta
publish: false
tags:
  - meta
  - roadmap
  - system-design
---

# Roadmap — Padrões recorrentes (sub-galho 3)

Roadmap-folha do sub-galho `System Design/3 - Padrões recorrentes`. Fase **Adepto** (alvo de densidade ~440-540 linhas / alto word-count). Spec: [[00-Meta/specs/2026-07-06-system-design-trilha-design]]. EXEMPLAR do galho: [[1 - Framework de entrevista/01 - O que é System Design e o que a entrevista avalia]].

## Tabela-resumo

| Métrica | Valor |
|---------|-------|
| Total de notas | 6 |
| ⬜ pendente | 0 |
| ✅ feita | 6 |
| 🔄 em andamento | 0 |
| % concluído | 100% ✅ |

---

## Notas

#### 01 - Pub-Sub e event-driven em escala   [substantivo]
- **Estado:** ✅ feita (2026-07-07) · fase: Adepto
- **Escopo:** broker, tópicos, publishers/subscribers desacoplados, fan-out, event notification vs state transfer, ordering por partição, acoplamento temporal, custos (eventual consistency, spaghetti de eventos), broker como SPOF.
- **Fronteira:** linka [[Arquitetura de Software]] (EDA); usa filas do SG2-05 como substrato.
- **Fontes:** Kleppmann DDIA cap.11; Fowler "What do you mean by Event-Driven"; Google Cloud Pub/Sub ordering; AWS SNS+SQS fanout.
- **Resultado:** 268 linhas / 5003 palavras; 3 Mermaid (inc. sequenceDiagram), 3 [!warning], 4 [!question]-. Verificado: links-irmãos e URLs ok.

#### 02 - CQRS sob a ótica de system design   [substantivo]
- **Estado:** ✅ feita (2026-07-07) · fase: Adepto · **expandida** (v1 saiu leve, 202ln/3467pal → reforçada)
- **Escopo:** separar read/write models por escala/latência; exemplo ponta-a-ponta (outbox→Debezium→Kafka→Elasticsearch); 4 níveis de CQRS c/ tabela; consistência eventual write→read (read-your-writes, concorrência otimista, UI otimista); quando NÃO usar (teste de Udi Dahan).
- **Fronteira:** **reforço** de [[Event Storming]]/[[Arquitetura de Software]] + cross-link; foco em escala, não modelagem de domínio.
- **Fontes:** Fowler (CQRS); Azure Architecture Center; Udi Dahan (When to Avoid CQRS / Clarified CQRS); Debezium (CQRS+Outbox); Greg Young.
- **Resultado:** 302 linhas / 6032 palavras; 5 Mermaid, 3 [!warning], 3 [!question]-. Verificado: links-irmãos e URLs ok.

#### 03 - Event Sourcing sob a ótica de system design   [substantivo]
- **Estado:** ✅ feita (2026-07-07) · fase: Adepto
- **Escopo:** log append-only imutável como fonte da verdade; estado por replay; auditoria/temporal queries; event store + projeções + snapshots; custos (versionamento/upcasting, replay caro, LGPD vs imutabilidade); par com CQRS; quando usar (financeiro/saúde/logística).
- **Fronteira:** **reforço** de [[Event Storming]] + cross-link; foco no custo/escala de operar um event store.
- **Fontes:** Fowler (Event Sourcing); Kurrent/EventStoreDB (guide + KurrentDB 26.1, mai/2026); Azure Architecture Center; Kleppmann DDIA.
- **Resultado:** 369 linhas / 6734 palavras; 4 Mermaid (log+projeções, snapshot replay, concorrência otimista, event-store-as-bus), 5 [!warning], 4 [!question]-. Verificado: links-irmãos e URLs ok.

#### 04 - Rate Limiting   [substantivo]
- **Estado:** ✅ feita (2026-07-07) · fase: Adepto
- **Escopo:** token/leaky bucket, fixed window (problema da borda), sliding window log/counter; trade-off memória/precisão/burst; onde aplicar (user/key/IP, edge vs serviço); distribuído com Redis (INCR+EXPIRE) e por que Lua garante atomicidade; 429 + Retry-After + RateLimit-* headers; backoff no cliente.
- **Fronteira:** mecanismo aqui; sistema completo é o walkthrough SG4-04 (só citado). Redis geral → SG2-02.
- **Fontes:** Cloudflare/Figma eng blogs; Stripe/Kong docs; RFC 6585 (429); IETF ratelimit-headers draft v11; freeCodeCamp Redis+Lua.
- **Resultado:** 288 linhas / ~5013 palavras; 4 Mermaid (token bucket, borda fixed-window, race distribuída sequenceDiagram, arquitetura em camadas), 3 [!warning], 4 [!question]-. Verificado: links e URLs ok.

#### 05 - Circuit Breaker e resiliência   [substantivo]
- **Estado:** ✅ feita (2026-07-07) · fase: Adepto
- **Escopo:** falha em cascata + esgotamento de recursos; timeout; retry com backoff+jitter (retry storm); circuit breaker (closed/open/half-open, thresholds, reset); bulkhead; fallback/graceful degradation; idempotência como pré-req de retry.
- **Fronteira:** reforça Resilience4j de [[Spring Boot]] sob ótica de design; não vira tutorial da lib. CAP/degradação → SG2-06.
- **Fontes:** Nygard *Release It!*; Fowler (CircuitBreaker); Resilience4j docs; AWS Builders' Library (backoff+jitter, idempotência); Netflix Hystrix (deprecado nov/2018).
- **Resultado:** 288 linhas / 5013 palavras; 4 Mermaid (inc. stateDiagram-v2 dos 3 estados + cascata/bulkhead), 4 [!warning], 5 [!question]-. Verificado: links e URLs ok.

#### 06 - API Gateway e BFF   [substantivo]
- **Estado:** ✅ feita (2026-07-07) · fase: Adepto · **FECHA o sub-galho**
- **Escopo:** cross-cutting concerns no gateway (roteamento/composição, auth, TLS, rate-limit, agregação, transformação de protocolo, observabilidade); gateway ≠ LB (distinção cravada); padrões Azure (Routing/Aggregation/Offloading); BFF por tipo de cliente; riscos SPOF/gargalo/god-object; quando é over-engineering.
- **Fronteira:** linka [[API Design]]; distingue gateway de load balancer (SG2-01); rate limit mecânico → nota 04.
- **Fontes:** Sam Newman (Building Microservices 2ª ed. + BFF pattern); Azure Architecture Center (Gateway Aggregation/Offloading); Netflix Tech Blog (2012); Kong docs.
- **Resultado:** 299 linhas / 5533 palavras; 6 Mermaid (clientes→gateway→N, 3 padrões, gateway vs LB, BFF, riscos, N-S vs L-O), 3 [!warning], 4 [!question]-. Forward-link [[4 - Walkthroughs/index]] intencional (SG4 não criado). Verificado: links e URLs ok.
