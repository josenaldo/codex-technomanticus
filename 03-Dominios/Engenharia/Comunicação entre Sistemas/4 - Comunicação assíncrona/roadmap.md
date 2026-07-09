---
title: "Roadmap — Comunicação assíncrona"
created: 2026-07-09
type: meta
publish: false
tags:
  - meta
  - roadmap
  - comunicacao-entre-sistemas
---

# Roadmap — Comunicação assíncrona (sub-galho 4)

Roadmap-folha do sub-galho `Comunicação entre Sistemas/4 - Comunicação assíncrona`. Fase **Adepto→Magus** (desacoplar no tempo — panorama e decisão; ferramenta específica já tem casa em `Mensageria/*.md`). Spec: [[00-Meta/specs/2026-07-09-comunicacao-entre-sistemas-trilha-design]]. EXEMPLAR: notas dos sub-galhos 1-3 desta trilha.

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

#### 01 - Síncrono vs assíncrono — quando desacoplar   [substantivo]
- **Estado:** ✅ feita (2026-07-09) · fase: Adepto
- **Escopo:** latência vs throughput (Little's Law), custo real da assincronia (debugging, eventual consistency, dual-write), framework de decisão em 3 testes.
- **Fronteira:** reforço de `Mensageria.md`.
- **Resultado:** 219 linhas / 5952 palavras; Mermaid. Fontes: Little's Law, SQS backpressure, web-queue-worker pattern.

#### 02 - Message queue vs event streaming   [substantivo]
- **Estado:** ✅ feita (2026-07-09) · fase: Adepto
- **Escopo:** fila (remove após consumo) vs stream (persiste, replay), tabela comparativa, panorama de brokers (Kafka/RabbitMQ/SQS/NATS/Pulsar/BullMQ) linkado.
- **Fronteira:** referência: `Mensageria/*.md` (ferramenta individual fica lá).
- **Resultado:** 273 linhas / 5166 palavras.

#### 03 - Garantias de entrega e ordenação   [substantivo]
- **Estado:** ✅ feita (2026-07-09) · fase: Adepto
- **Escopo:** at-most/at-least/"exactly-once" (mito vs Kafka EOS real), idempotência no consumer (ponte pra nota HTTP), ordenação por partição/fila/FIFO, regra do agregado.
- **Fronteira:** reforço de `Mensageria.md`.
- **Resultado:** 256 linhas / 5335 palavras; Mermaid. Fontes: Kleppmann/DDIA, Kafka EOS, Google Pub/Sub ordering keys.

#### 04 - Outbox e Saga   [substantivo]
- **Estado:** ✅ feita (2026-07-09) · fase: Magus
- **Escopo:** dual-write problem, Outbox (Polling Publisher vs CDC/Debezium), Saga (coreografia vs orquestração), isolamento/anomalias, exemplo trabalhado pedido/estoque/pagamento/notificação.
- **Fronteira:** linka Java/Mensageria 21-22; não é System Design (Saga/Outbox não existem lá).
- **Resultado:** 347 linhas / 6485 palavras; 3 Mermaid. Fontes: Debezium/CDC, Temporal/Camunda, 2PC.

#### 05 - Legado e padrões enterprise   [substantivo]
- **Estado:** ✅ feita (2026-07-09) · fase: Magus
- **Escopo:** JMS (API portável, Jakarta Messaging), IBM MQ (confiabilidade extrema, mainframe, pagamentos), ESB (hub-and-spoke, "smart endpoints dumb pipes" de Fowler, por que virou anti-padrão) — o que resolviam, por que a indústria migrou, onde ainda aparecem (bancos, seguradoras, pagamentos).
- **Fronteira:** histórico, sem tutorial; espelha o modelo da nota irmã SG1-02 (RPC clássico).
- **Resultado:** 279 linhas / 5499 palavras; 2 Mermaid. Fontes: Hohpe/Woolf EIP, Fowler "smart endpoints dumb pipes", IBM MQ v10.0/aquisição Confluent 2026, market share MuleSoft/iPaaS.

#### 06 - O que está emergindo em mensageria   [substantivo]
- **Estado:** ✅ feita (2026-07-09) · fase: Magus · **FECHA o sub-galho e a trilha**
- **Escopo:** CloudEvents (envelope, caso real Intuit 2026), AsyncAPI ("OpenAPI dos eventos", v3), fecha "webhooks são mensageria invertida" retomando SG3-05, síntese de confiabilidade de entrega dos sub-galhos 3+4.
- **Fronteira:** fecha o sub-galho e o conteúdo principal da trilha; prepara o capstone.
- **Resultado:** 348 linhas / 7050 palavras; 2 Mermaid. Fontes: CloudEvents spec, AsyncAPI 3.1, caso Intuit/QuickBooks 2026.
