---
title: "System Design Practice"
created: 2026-04-01
updated: 2026-04-01
type: concept
status: seedling
tags:
  - entrevista
  - prática
publish: false
---

# System Design Practice

Exercícios e roteiro para praticar system design interviews.

## Framework de prática

### Antes da entrevista

1. **Estudar 5-6 sistemas clássicos** (ver lista abaixo)
2. **Praticar em voz alta** — falar enquanto desenha é tão importante quanto o design
3. **Cronometrar** — cada prática deve durar 45 min (5 + 5 + 5 + 10 + 15 + 5)
4. **Gravar ou praticar com alguém** — feedback é essencial

### Durante a prática

Para cada sistema, seguir o framework de [[System Design]]:

1. Clarificar requisitos (5 min)
2. Estimativas de escala (5 min)
3. API Design (5 min)
4. Diagrama de alto nível (10 min)
5. Deep dive (15 min)
6. Trade-offs e melhorias (5 min)

## Sistemas para praticar

### Nível 1 — Fundamentos

- [ ] **URL Shortener** — hash, base62, KV store, cache, redirecionamento
- [ ] **Paste Bin** — storage, content-addressable, TTL
- [ ] **Rate Limiter** — token bucket, sliding window, distributed counter

### Nível 2 — Data-intensive

- [ ] **Twitter/X Feed** — fan-out on write vs read, timeline, pub/sub
- [ ] **Instagram/Photo Sharing** — object storage, CDN, metadata DB, feed
- [ ] **Chat System (WhatsApp)** — WebSocket, presence, message queue, ordenação
- [ ] **Notification System** — multi-channel, template, priority queue, retry

### Nível 3 — Infrastructure

- [ ] **Search Engine (Google-lite)** — inverted index, ranking, crawling
- [ ] **File Storage (Dropbox)** — chunking, dedup, sync, conflict resolution
- [ ] **Video Streaming (YouTube)** — encoding pipeline, CDN, adaptive bitrate
- [ ] **Ride Sharing (Uber)** — geolocation, matching, pricing, real-time updates

## Checklist de revisão por prática

Após cada sessão, verificar:

- [ ] Clarifiquei requisitos antes de começar?
- [ ] Fiz estimativas de escala (QPS, storage)?
- [ ] Desenhei API endpoints?
- [ ] Diagrama tem os componentes essenciais?
- [ ] Fiz deep dive em pelo menos 1 componente?
- [ ] Discuti trade-offs explicitamente?
- [ ] Falei em voz alta durante todo o processo?
- [ ] Mantive dentro de 45 minutos?

## Recursos

- [System Design Primer (GitHub)](https://github.com/donnemartin/system-design-primer) — referência completa com exercícios
- [Designing Data-Intensive Applications](https://dataintensive.net/) — Martin Kleppmann
- [Architectural Katas](https://www.architecturalkatas.com/) — exercícios práticos
- [Grokking the System Design Interview](https://www.designgurus.io/course/grokking-the-system-design-interview) — curso focado

## Veja também

- [[System Design]]
- [[API Design]]
- [[Communicating Trade-offs]]
