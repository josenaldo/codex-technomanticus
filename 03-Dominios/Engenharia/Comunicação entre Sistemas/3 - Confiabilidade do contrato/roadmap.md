---
title: "Roadmap — Confiabilidade do contrato"
created: 2026-07-09
type: meta
publish: false
tags:
  - meta
  - roadmap
  - comunicacao-entre-sistemas
---

# Roadmap — Confiabilidade do contrato (sub-galho 3)

Roadmap-folha do sub-galho `Comunicação entre Sistemas/3 - Confiabilidade do contrato`. Fase **Adepto→Magus** (o contrato promete — como garantir que se sustenta sob falha, retry e o tempo). Spec: [[00-Meta/specs/2026-07-09-comunicacao-entre-sistemas-trilha-design]]. EXEMPLAR: notas dos sub-galhos 1 e 2 desta trilha.

## Tabela-resumo

| Métrica | Valor |
|---------|-------|
| Total de notas | 5 |
| ⬜ pendente | 0 |
| ✅ feita | 5 |
| 🔄 em andamento | 0 |
| % concluído | 100% ✅ |

---

## Notas

#### 01 - Idempotência   [substantivo]
- **Estado:** ✅ feita (2026-07-09) · fase: Adepto
- **Escopo:** GET/PUT/DELETE idempotentes vs POST, Idempotency-Key (Stripe), draft IETF, armazenamento atômico, cache seletivo de erros, ponte pra Java/Mensageria 20.
- **Fronteira:** reforço/migração de `API Design.md`; linka Java/Mensageria 20.
- **Resultado:** 292 linhas / 6199 palavras; 3 Mermaid. Fontes: Stripe Idempotent Requests, IETF draft, PayPal-Request-Id, Google AIP-155, RFC 9110.

#### 02 - Versionamento e evolução de contrato   [substantivo]
- **Estado:** ✅ feita (2026-07-09) · fase: Adepto
- **Escopo:** URL/header/query/date versioning, 6 regras de evolução segura, processo de breaking change (caso Twitter API), RFC 8594 + RFC 9745, ponte GraphQL/gRPC.
- **Fronteira:** reforço/migração de `API Design.md`.
- **Resultado:** 363 linhas / 6688 palavras; 2 Mermaid. Fontes: RFC 8594, RFC 9745, Zalando, Stripe/Shopify/GitHub, Twitter shutdown.

#### 03 - Caching HTTP e requisições condicionais   [substantivo]
- **Estado:** ✅ feita (2026-07-09) · fase: Adepto
- **Escopo:** Cache-Control, ETag/If-None-Match/304, optimistic locking com If-Match/412, ponte com GraphQL (persisted queries).
- **Fronteira:** reforço/migração de `API Design.md`.
- **Resultado:** 297 linhas / 7217 palavras; 2 Mermaid, 3 [!warning]. Fontes: RFC 9111/7232/5861, AWS S3 conditional writes, Apollo APQ.

#### 04 - Rate limiting como contrato   [substantivo]
- **Estado:** ✅ feita (2026-07-09) · fase: Adepto
- **Escopo:** headers de resposta (X-RateLimit-* vs draft IETF RateLimit), 429+Retry-After, tiers, backoff do cliente. Algoritmo é System Design SG3-04 — aqui só o que a API expõe.
- **Fronteira:** reforço leve; fronteira explícita com SG (linkada, não repetida).
- **Resultado:** 256 linhas / 4728 palavras (deliberadamente mais curta); Mermaid. Fontes: IETF draft RateLimit headers, GitHub/Stripe rate limits, RFC 6585/9110/9457.

#### 05 - Webhooks e operações assíncronas   [substantivo]
- **Estado:** ✅ feita (2026-07-09) · fase: Adepto · **FECHA o sub-galho**
- **Escopo:** 202 Accepted+polling, webhooks (HMAC, retry, dedup, dead letter), bulk operations (207 Multi-Status), fecha com "webhooks são mensageria invertida".
- **Fronteira:** reforço/migração de `API Design.md`; ponte explícita pro sub-galho 4.
- **Resultado:** 328 linhas / 7357 palavras; 3 Mermaid. Fontes: Stripe webhooks, RFC 9110, Azure async request-reply, Google AIP-151, Shopify bulk API.
