---
title: "Roadmap — Walkthroughs"
created: 2026-07-07
type: meta
publish: false
tags:
  - meta
  - roadmap
  - system-design
---

# Roadmap — Walkthroughs (sub-galho 4)

Roadmap-folha do sub-galho `System Design/4 - Walkthroughs`. Fase **Magus** (o coração da trilha — notas DENSAS: alvo ~500-600 linhas / 6-8k palavras, exemplo numérico, ~15-25 buscas web). Spec: [[00-Meta/specs/2026-07-06-system-design-trilha-design]]. EXEMPLAR de estrutura: [[1 - Framework de entrevista/01 - O que é System Design e o que a entrevista avalia]].

**Espinha fixa por walkthrough:** requisitos (RF/RNF) → estimativas (back-of-envelope) → API & modelo de dados → diagrama macro → deep dives (1-2 componentes difíceis) → gargalos & trade-offs → variações de follow-up. Cada nota aplica building blocks (SG2) e padrões (SG3) com cross-link explícito.

## Tabela-resumo

| Métrica | Valor |
|---------|-------|
| Total de notas | 8 |
| ⬜ pendente | 0 |
| ✅ feita | 8 |
| 🔄 em andamento | 0 |
| % concluído | 100% ✅ |

---

## Notas

#### 01 - URL Shortener   [substantivo]
- **Estado:** ✅ feita (2026-07-07) · fase: Magus
- **Peças-chave:** base62 de contador vs hash+colisão vs KGS, read-heavy 100:1, cache-aside, KV store, 301 vs 302, analytics assíncrono, custom alias, expiração.
- **Aplica:** SG2-02 Caching, SG2-04 Sharding, SG1-03 estimativas.
- **Fontes:** Alex Xu Vol.1 cap.8; Hello Interview (bitly); System Design Primer; Twitter Snowflake.
- **Resultado:** 416 linhas / 6796 palavras; 3 Mermaid (macro, cache-aside sequence, analytics async), 3 [!warning], 5 [!question]-. Espinha fixa completa. Verificado: links e URLs ok.

#### 02 - News Feed e Timeline   [substantivo]
- **Estado:** ✅ feita (2026-07-07) · fase: Magus
- **Peças-chave:** fan-out on-write vs on-read, problema da celebridade (híbrido `is_precomputed`), feed cache (Redis, 800 entradas/20B), ranking cronológico vs ML (EdgeRank→~100k fatores), pull/push.
- **Aplica:** SG3-01 Pub/Sub, SG2-05 filas, SG2-02 caching, SG2-04 sharding.
- **Fontes:** Alex Xu Vol.2; High Scalability/antirez; Hello Interview; Meta Eng; X Eng Blog.
- **Resultado:** 372 linhas / 6593 palavras; 5 Mermaid, 3 [!warning], 4 [!question]-. Verificado: links e URLs ok.

#### 03 - Chat System   [substantivo]
- **Estado:** ✅ feita (2026-07-07) · fase: Magus
- **Peças-chave:** WebSocket vs polling/SSE, chat server stateful, presence (heartbeat+pub/sub), entrega at-least-once+dedup+ACK, ordering por sequence, fila offline/push, message store sharded, roteamento entre chat servers.
- **Aplica:** SG2-05 filas, SG2-06 CAP, SG2-04 sharding, SG3-01 pub/sub.
- **Fontes:** Alex Xu Vol.2; Slack Eng (2023); Discord "Trillions of Messages"; WhatsApp/Erlang.
- **Resultado:** 387 linhas / ~6617 palavras; 4 Mermaid (inc. sequenceDiagram de envio), 3 [!warning], 4 [!question]-. Verificado: links e URLs ok.

#### 04 - Distributed Rate Limiter   [substantivo]
- **Estado:** ✅ feita (2026-07-07) · fase: Magus
- **Peças-chave:** contagem global (Redis central vs local+sync), atomicidade via Lua/GCRA, race conditions com trace numérico, fail-open vs fail-closed, Redis como SPOF/hot spot, sliding window distribuído.
- **Aplica:** SG3-04 Rate Limiting (mecanismo), SG3-06 API Gateway, SG2-02 Redis. Fecha o forward-link da SG3.
- **Fontes:** Alex Xu Vol.1; Figma Eng; Kong/Envoy docs; Brandur (redis-cell/GCRA); Redis.io.
- **Resultado:** 334 linhas / 6366 palavras; 3 Mermaid (macro, local+sync, race sequenceDiagram), 3 [!warning], 4 [!question]-. Trace numérico do Lua. Verificado: links e URLs ok.

#### 05 - Notification System   [substantivo]
- **Estado:** ✅ feita (2026-07-07) · fase: Magus · **mais densa do galho (8.1k palavras)**
- **Peças-chave:** fan-out multi-canal, fila por canal, adapters (APNs/FCM/Twilio/SES), circuit breaker por provedor, dedup/idempotência por (evento,user,canal), retry+DLQ, priorização, opt-out, compliance (TCPA/CAN-SPAM).
- **Aplica:** SG2-05 filas, SG3-05 circuit breaker, SG3-04 rate limiting, SG3-01 pub/sub.
- **Fontes:** Alex Xu Vol.1 cap.10; Uber RAMEN; Slack; AWS backoff-jitter; FCM/APNs docs.
- **Resultado:** 444 linhas / 8119 palavras; 4 Mermaid (macro, fila-por-canal, CB stateDiagram, idempotência sequence), 5 [!warning], 5 [!question]-. Verificado: links e URLs ok.

#### 06 - Distributed File Storage   [substantivo]
- **Estado:** ✅ feita (2026-07-07) · fase: Magus
- **Peças-chave:** separação metadata service × block storage, chunking (4MB), dedup por hash SHA-256, sync delta + notification, conflito/conflicted-copy, durabilidade (replicação/erasure coding), CDN pra download.
- **Aplica:** SG2-03 SQL/NoSQL (metadata), SG2-04 sharding, SG2-07 CDN, SG2-06 CAP.
- **Fontes:** Alex Xu Vol.1 cap.15; Dropbox Magic Pocket (dropbox.tech); Google Colossus; ByteByteGo (S3 durabilidade/erasure).
- **Resultado:** 386 linhas / 7136 palavras; 3 Mermaid (metadata×block macro, chunking+dedup, sync conflict sequence), 3 [!warning], 3 [!question]-. Verificado: links e URLs ok.

#### 07 - Web Crawler   [substantivo]
- **Estado:** ✅ feita (2026-07-07) · fase: Magus
- **Peças-chave:** URL frontier (front-queues priority + back-queues per-host, Mercator), politeness (robots.txt, Crawl-delay), dedup de URL (bloom filter) + conteúdo (simhash), spider traps, DNS como gargalo, freshness/re-crawl.
- **Aplica:** SG2-05 filas, SG2-04 sharding, SG3-04 rate limiting (politeness), SG2-02 caching.
- **Fontes:** Alex Xu Vol.2; Mercator (Heydon & Najork); Manku simhash; Google crawl-budget; System Design Primer.
- **Resultado:** 389 linhas / 6661 palavras; 3 Mermaid (loop, frontier, dedup), 3 [!warning], 4 [!question]-. Verificado: links e URLs ok.

#### 08 - Distributed Key-Value Store   [substantivo]
- **Estado:** ✅ feita (2026-07-07) · fase: Magus · **FECHA o sub-galho e a escrita da trilha**
- **Peças-chave:** consistent hashing, quórum R+W>N, sloppy quorum + hinted handoff, vector clocks (detecção de conflito), gossip (membership), Merkle trees (anti-entropia), tunable consistency, LSM (commit log+memtable+SSTable).
- **Aplica:** SG2-04 Sharding & Consistent Hashing, SG2-06 CAP/quorum, SG2-03 replicação. É a síntese distribuída da trilha.
- **Fontes:** Amazon Dynamo paper (SOSP 2007); Cassandra docs (gossip/repair/Merkle/hints); Riak DVVs; Kleppmann DDIA cap.5-6-9.
- **Resultado:** 413 linhas / 6913 palavras; 7 Mermaid (macro+anel, write/read sequence, quórum, hinted handoff, vector clocks, gossip, Merkle), 3 [!warning], 6 [!question]-. Verificado: links e URLs ok.
