---
title: "Roadmap — Panorama e decisão"
created: 2026-07-09
type: meta
publish: false
tags:
  - meta
  - roadmap
  - comunicacao-entre-sistemas
---

# Roadmap — Panorama e decisão (sub-galho 1)

Roadmap-folha do sub-galho `Comunicação entre Sistemas/1 - Panorama e decisão`. Fase **Iniciado** (o mapa antes do território). Spec: [[00-Meta/specs/2026-07-09-comunicacao-entre-sistemas-trilha-design]]. EXEMPLAR de estrutura até a trilha ter o seu: [[1 - Framework de entrevista/01 - O que é System Design e o que a entrevista avalia]].

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

#### 01 - O que é o contrato de comunicação   [substantivo]
- **Estado:** ✅ feita (2026-07-09) · fase: Iniciado · **EXEMPLAR da trilha**
- **Escopo:** producer/consumer, acoplamento (dados/schema vs temporal), o contrato como abstração central; sync vs async como eixo mestre.
- **Fronteira:** enquadra a trilha.
- **Resultado:** 244 linhas / 6214 palavras; 2 Mermaid, 3 [!warning], 2 [!question]-. Fontes: Enterprise Integration Patterns, Hyrum's Law, Postel's Law, Eight Fallacies, CAP theorem, Stripe idempotency, AWS Outbox.

#### 02 - RPC clássico e por que caiu   [substantivo]
- **Estado:** ✅ feita (2026-07-09) · fase: Iniciado
- **Escopo:** CORBA, DCOM, XML-RPC, SOAP/WSDL — o que resolviam, por que caíram, onde ainda sobrevivem (EDI saúde/bancos, NFe/SEFAZ, SWIFT, B2B EDIFACT/X12).
- **Fronteira:** histórico, sem tutorial.
- **Resultado:** 337 linhas / 5653 palavras; 2 Mermaid, 3 [!warning], 5 [!question]-. Fontes: ACM Queue (CORBA), Microsoft Learn (DCOM/WCF), Dave Winer (XML-RPC/SOAP), SWIFT ISO 20022, HIPAA/X12.

#### 03 - A era REST, GraphQL, gRPC   [substantivo]
- **Estado:** ✅ feita (2026-07-09) · fase: Iniciado
- **Escopo:** por que REST venceu como default (Fielding, simplicidade vs WS-*), origem motivacional de GraphQL (Facebook 2012) e gRPC (Stubby do Google); três respostas pra três problemas.
- **Fronteira:** prepara o sub-galho 2.
- **Resultado:** 227 linhas / 5133 palavras; 2 Mermaid, 2 [!warning], 2 [!question]-. Fontes: Fielding 2000, histórico GraphQL/Facebook, histórico gRPC/Stubby, Postman State of API 2025.

#### 04 - Comunicação em tempo real   [substantivo]
- **Estado:** ✅ feita (2026-07-09) · fase: Iniciado
- **Escopo:** polling/long-polling/Comet → WebSocket (handshake, full-duplex, custo de estado) → SSE (EventSource, reconexão, streaming de tokens de LLM) → WebTransport (QUIC/HTTP-3, ainda em draft IETF).
- **Fronteira:** linka [[Redes e Protocolos]].
- **Resultado:** 329 linhas / 7398 palavras; 3 Mermaid, 3 [!warning]. Fontes: RFC 6455, spec WHATWG SSE, drafts IETF WebTransport, docs OpenAI/Anthropic streaming.

#### 05 - O que está emergindo e framework de decisão   [substantivo]
- **Estado:** ✅ feita (2026-07-09) · fase: Iniciado · **FECHA o sub-galho**
- **Escopo:** tRPC, Connect (Buf), AsyncAPI, CloudEvents, MCP (linkado ao domínio IA, sem duplicar); árvore de decisão Mermaid amarrando 01-04; tabela comparativa curta por linguagem (Java/TS/Python/Go).
- **Fronteira:** fecha o sub-galho; prepara sub-galho 2.
- **Resultado:** 255 linhas / 6347 palavras; 1 Mermaid (árvore de decisão), 1 [!warning]. 24 fontes datadas.
