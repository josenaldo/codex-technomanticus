---
title: "Comunicação entre Sistemas"
type: moc
publish: true
created: 2026-06-23
updated: 2026-07-09
status: evergreen
tags:
  - moc
  - comunicacao-entre-sistemas
aliases:
  - Comunicação entre Sistemas
  - Comunicação entre sistemas
---
# Comunicação entre Sistemas

> [!abstract] TL;DR
> A camada de aplicação acima do fio — como sistemas conversam: APIs (REST, GraphQL, gRPC), mensageria assíncrona, contratos, idempotência e versionamento. Trilha comparativa e decisória (4 sub-galhos + capstone, 23 notas): não é tutorial de implementação — isso vive nos domínios de tecnologia (Java, Node, Python, Go).

## Sobre este domínio

Sobre o transporte (TCP/HTTP/DNS, que vive em [[03-Dominios/Ciência/Redes e Protocolos/index|Redes e Protocolos]]) mora a camada de *contrato*: como desenhar uma API, escolher entre síncrono e assíncrono, versionar sem quebrar consumidores, garantir entrega e idempotência. Disciplina neutra de stack — cada tecnologia implementa e linka pra cá.

## Sub-galhos

### 1 · Panorama e decisão *(Iniciado)*
O mapa antes do território: contrato/acoplamento, RPC clássico e onde sobrevive, a era REST/GraphQL/gRPC, tempo real, o que está emergindo.
- [[1 - Panorama e decisão/index|Panorama e decisão]]

### 2 · Comunicação síncrona *(Adepto)*
REST (modelagem, maturidade, HATEOAS/HAL, contrato de resposta, paginação/filtros/auth), GraphQL, gRPC, e a decisão final entre os três.
- [[2 - Comunicação síncrona/index|Comunicação síncrona]]

### 3 · Confiabilidade do contrato *(Adepto→Magus)*
Idempotência, versionamento e evolução segura, caching HTTP, rate limiting como contrato, webhooks e operações assíncronas.
- [[3 - Confiabilidade do contrato/index|Confiabilidade do contrato]]

### 4 · Comunicação assíncrona *(Adepto→Magus)*
Síncrono vs assíncrono, message queue vs event streaming, garantias de entrega e ordenação, Outbox e Saga, legado enterprise, CloudEvents/AsyncAPI.
- [[4 - Comunicação assíncrona/index|Comunicação assíncrona]]

### ★ Capstone *(Magus)*
Um walkthrough único desenhando a comunicação de um e-commerce do zero, costurando os 4 sub-galhos numa sequência de decisões reais.
- [[Desenhando a comunicação de um sistema do zero]]

## Como usar esta trilha

Leia na ordem 1 → 2 → 3 → 4 se está construindo o mapa mental: o panorama dá o vocabulário histórico, a comunicação síncrona aprofunda REST/GraphQL/gRPC, a confiabilidade cobre o que faz o contrato se sustentar sob falha, e a comunicação assíncrona traz mensageria em nível de decisão. Se já domina o básico, vá direto ao [[Desenhando a comunicação de um sistema do zero|capstone]] e use os sub-galhos como referência quando uma decisão específica precisar de profundidade.

## Referência

- [[03-Dominios/Engenharia/Comunicação entre Sistemas/API Design|API Design]] — tronco podado (redireciona pra trilha; preserva file upload e "Na prática" do autor)
- [[03-Dominios/Engenharia/Comunicação entre Sistemas/Mensageria/index|Mensageria]] — ferramenta específica (Kafka, RabbitMQ, BullMQ, Event Streaming)

## Veja também

- [[03-Dominios/Engenharia/index|Engenharia]] — a camada
- [[03-Dominios/Ciência/Redes e Protocolos/index|Redes e Protocolos]] — o transporte (o fio) abaixo
- [[03-Dominios/Engenharia/Arquitetura/index|Arquitetura]] — a forma do sistema que se comunica
- [[03-Dominios/Engenharia/Arquitetura/System Design/index|System Design]] — escala/Pub-Sub/CQRS/Event Sourcing/API Gateway (fronteira: lá é escala, aqui é contrato)
