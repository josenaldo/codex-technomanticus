---
title: "Operação"
type: moc
publish: true
tags:
  - operacao
  - devops
  - sre
  - moc
aliases:
  - Operação
  - SRE
  - Operação de Software
created: 2026-06-23
updated: 2026-07-08
---

# Operação (DevOps/SRE) — aplicar tudo junto em produção

O par do [[System Design/index|System Design]]: se aquela trilha ensina a **desenhar** o sistema no whiteboard, esta ensina a **mantê-lo vivo em produção**. É escrita para quem **já conhece as peças** — os containers, o Kubernetes, o CI/CD, a observabilidade, o backend — e quer saber **como operá-las juntas**, com as decisões e os trade-offs que só aparecem quando o serviço está no ar e alguém precisa acordar às 3h da manhã para consertá-lo.

> [!info] Onde isto se encaixa
> As **ferramentas** vivem na estante [[03-Dominios/Tecnologia/Infraestrutura/index|Infraestrutura]] (Docker, Kubernetes, CI/CD, Observabilidade, Nginx — o "o que é" e a sintaxe). Aqui é a **prática de operar**: como combinar essas ferramentas, quando usar cada estratégia, e o que fazer quando tudo dá errado. A ótica de aplicação-JVM (JVM em container, contrato K8s da app Spring) mora no [[Spring Boot|galho Cloud-native do Java]]; aqui a visão é **agnóstica de linguagem**. Cloud gerenciada (AWS/GCP) é cobertura à parte.

## Sub-galhos

### 1 · O ofício de operar *(Iniciado→Adepto)*
O que muda quando o código vira um serviço que alguém precisa manter vivo.
- [[1 - O ofício de operar/index|O ofício de operar]]

### 2 · Entrega e release *(Adepto)*
Levar código a produção com segurança e velocidade: pipelines, deploy strategies, rollback, migrations.
- [[2 - Entrega e release/index|Entrega e release]]

### 3 · Rodar em produção *(Adepto→Magus)*
Manter o sistema no ar, escalando e sem derrubar ninguém: containers, Kubernetes, zero-downtime, capacidade.
- [[3 - Rodar em produção/index|Rodar em produção]]

### 4 · Observar e responder *(Magus)*
Reliability engineering: enxergar o sistema, medir confiabilidade e reagir quando ele quebra.
- [[4 - Observar e responder/index|Observar e responder]]

### ★ Capstone *(Magus)*
- [[Anatomia de um incidente de produção]] — um incidente do sintoma ao postmortem, costurando tudo *(ao fechar o SG4)*

## Recursos

- *Site Reliability Engineering* & *The SRE Workbook* — Google ([sre.google/books](https://sre.google/books/))
- *The DevOps Handbook* — Gene Kim et al.
- *Accelerate* — Forsgren, Humble, Kim (as 4 métricas DORA)
- *Release It!* — Michael Nygard (padrões de estabilidade)
- [AWS Builders' Library](https://aws.amazon.com/builders-library/)

## Veja também

- [[System Design/index|System Design]] — desenhar o sistema (o par desta trilha)
- [[03-Dominios/Tecnologia/Infraestrutura/index|Infraestrutura]] — as ferramentas (Docker, K8s, Nginx, cloud) — referência
- [[Arquitetura de Software]] — estilos, microserviços, observabilidade conceitual
- [[03-Dominios/Ciência/Sistemas Operacionais/index|Sistemas Operacionais]] — a teoria por baixo
