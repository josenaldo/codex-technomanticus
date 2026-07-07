---
title: "System Design"
type: moc
publish: true
tags:
  - system-design
  - moc
created: 2026-07-06
---

# System Design — trilha de entrevista sênior

A habilidade de **desenhar sistemas em escala no whiteboard**: conduzir os 45-60 min de uma entrevista de system design com estrutura, estimativas defensáveis e trade-offs explícitos. Trilha em 3 fases (Iniciado → Adepto → Magus), organizada em quatro sub-galhos.

> [!info] Onde isto se encaixa
> Esta trilha é a **forma macro sob escala**. O ofício de arquitetura (estilos, DDD, SOLID, Conway) vive em [[Arquitetura de Software]]; a modelagem de domínio em [[Event Storming]]; os contratos entre sistemas em [[03-Dominios/Engenharia/Comunicação entre Sistemas/index|Comunicação entre Sistemas]]. Aqui, tópicos desses galhos reaparecem **sob a ótica de system design** — reforço com cross-link, não duplicação.

## Sub-galhos

### 1 · Framework de entrevista *(Iniciado)*
O processo antes do conteúdo: como não travar nos primeiros 10 minutos.
- [[1 - Framework de entrevista/index|Framework de entrevista]]

### 2 · Building blocks *(Adepto)*
O vocabulário de escala: load balancing, caching, sharding, filas, CAP, CDN.
- [[2 - Building blocks/index|Building blocks]]

### 3 · Padrões recorrentes *(Adepto)*
Pub/Sub, CQRS, Event Sourcing, Rate Limiting, Circuit Breaker, API Gateway — sob a ótica de escala.
- [[3 - Padrões recorrentes/index|Padrões recorrentes]]

### 4 · Walkthroughs *(Magus)*
Os oito designs clássicos ponta a ponta, cada um aplicando os blocos e padrões.
- [[4 - Walkthroughs/index|Walkthroughs]]

## Veja também

- [[Arquitetura de Software]] — estilos, DDD, microserviços, C4/ADR, observabilidade
- [[Event Storming]] — modelagem de domínio, event sourcing
- [[System Design]] — nota-tronco (overview/porta de entrada)
- [[03-Dominios/Engenharia/Arquitetura/index|Arquitetura]] — o domínio
