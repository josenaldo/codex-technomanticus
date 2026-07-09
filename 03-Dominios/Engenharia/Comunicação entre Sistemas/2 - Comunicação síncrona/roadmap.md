---
title: "Roadmap — Comunicação síncrona"
created: 2026-07-09
type: meta
publish: false
tags:
  - meta
  - roadmap
  - comunicacao-entre-sistemas
---

# Roadmap — Comunicação síncrona (sub-galho 2)

Roadmap-folha do sub-galho `Comunicação entre Sistemas/2 - Comunicação síncrona`. Fase **Adepto** (a decisão técnica de como desenhar o contrato síncrono). Spec: [[00-Meta/specs/2026-07-09-comunicacao-entre-sistemas-trilha-design]]. EXEMPLAR: notas 01-05 do sub-galho 1 desta trilha (mesmo tom).

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

#### 01 - REST — modelagem de recursos e maturidade   [substantivo]
- **Estado:** ✅ feita (2026-07-09) · fase: Adepto
- **Escopo:** recursos como substantivos, nested vs flat, verbos HTTP (idempotência/safety), Richardson Maturity Model (0-3), HAL na prática, por que HATEOAS raramente é implementado de verdade.
- **Fronteira:** reforço/migração de `API Design.md`.
- **Resultado:** 401 linhas / 6715 palavras; Mermaid, 4 [!warning]. Fontes: Richardson Maturity Model, HAL IETF draft, Google AIP, RFC 9110, Zalando/Stripe/PayPal.

#### 02 - REST — o contrato de resposta   [substantivo]
- **Estado:** ✅ feita (2026-07-09) · fase: Adepto
- **Escopo:** status codes com tabela "quando usar"/"confusão comum", regra 4xx/5xx e retry automático, RFC 9457 Problem Details completo, content/method negotiation.
- **Fronteira:** reforço/migração de `API Design.md`; linka Java/Web e APIs REST 10 (não duplica).
- **Resultado:** 325 linhas / 6459 palavras; Mermaid, 3 [!warning]. Fontes: RFC 9457 oficial, ASP.NET/FastAPI/Go Problem Details.

#### 03 - Paginação, filtros e autenticação em REST   [substantivo]
- **Estado:** ✅ feita (2026-07-09) · fase: Adepto
- **Escopo:** offset vs cursor (Stripe/GitHub), RSQL/FIQL e filtros, full-text search, tabela comparativa de 6 métodos de auth, JWT/revogação como ponto de risco — decisão, não implementação.
- **Fronteira:** linka Node/Segurança, Java/Segurança (JWT deep-dive é lá).
- **Resultado:** 404 linhas / 6774 palavras; 2 Mermaid, 3 [!warning]. Fontes: OWASP API2:2023, Stripe/GitHub pagination, Zalando guidelines.

#### 04 - GraphQL — schema, resolvers e quando vale   [substantivo]
- **Estado:** ✅ feita (2026-07-09) · fase: Adepto
- **Escopo:** schema/SDL, queries/mutations, resolvers, problema N+1 e DataLoader, subscriptions (menção), quando vale/quando é overkill.
- **Fronteira:** linka Node/Integrações 06 (Apollo/Mercurius); Go/Java sem trilha profunda ainda (lacuna sinalizada, não preenchida).
- **Resultado:** 359 linhas / 5902 palavras; Mermaid, 3 [!warning]. Fontes: GitHub GraphQL v4, Shopify query cost.

#### 05 - gRPC — Protobuf, HTTP2 e streaming   [substantivo]
- **Estado:** ✅ feita (2026-07-09) · fase: Adepto
- **Escopo:** Protocol Buffers (`.proto`, `protoc`, binário vs JSON), HTTP/2 (multiplexação, HPACK), os 4 tipos de streaming com caso de uso concreto cada, deadlines propagados, interceptors, gRPC-Web/proxy (por que browser não fala gRPC nativo), tabela comparativa por linguagem (Go lacuna, Java/Node linkados, Python `grpc.aio`).
- **Fronteira:** linka Java/Mensageria 27-28 (Protobuf/gRPC Java), Node/Integrações 05; não duplica origem (Stubby/2015) já contada em SG1-03.
- **Resultado:** 325 linhas / 5769 palavras; 5 Mermaid, 3 [!warning]. Fontes: grpc.io (deadlines, about, web basics), protobuf.dev, benchmarks Protobuf vs JSON, HPACK, gRPC-Web/Envoy.

#### 06 - REST vs GraphQL vs gRPC — decisão   [substantivo]
- **Estado:** ✅ feita (2026-07-09) · fase: Adepto · **FECHA o sub-galho**
- **Escopo:** matriz de decisão, padrão híbrido de mercado (Netflix/Uber/Shopify), documentação como contrato (OpenAPI/.proto/SDL, design-first vs code-first), contract testing (Pact/Prism/Dredd).
- **Fronteira:** fecha o sub-galho; prepara sub-galho 3.
- **Resultado:** 325 linhas / 6238 palavras; 3 Mermaid, [!warning]. Fontes: Netflix TechBlog, Apollo Federation, Buf/Connect, Pact Docs.
