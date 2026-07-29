---
title: "Integração Empresarial (EIP)"
created: 2026-07-29
updated: 2026-07-29
type: moc
status: growing
publish: true
tags:
  - moc
  - design-de-software
  - integracao-empresarial
  - eip
  - mensageria
aliases:
  - Integração Empresarial
  - Enterprise Integration Patterns
  - EIP
  - Galho - EIP
---

# Integração Empresarial (EIP)

> [!abstract] TL;DR
> Os padrões que resolvem **como sistemas heterogêneos se integram por mensagens** — o vocabulário
> nomeado de **Hohpe & Woolf** (*Enterprise Integration Patterns*, 2004). Terceira família do galho-pai
> [[03-Dominios/Engenharia/Design de Software/Padrões de Projeto/index|Padrões de Projeto]], tratada como
> catálogo de consulta. A lente aqui é a **ferramenta de integração**: como **Apache Camel** e **Spring
> Integration** — que *são* implementações dos EIPs — encarnam cada padrão. Do bloco base (Message,
> Channel, Pipes and Filters) ao roteamento (routers, splitter/aggregator) e à confiabilidade de produção
> (guaranteed delivery, dead letter, competing consumers).

## Sobre esta família

Repertório de consulta para o sênior — inclusive em legado, onde ESBs, MOM (JMS/IBM MQ) e rotas Camel
ainda movem o coração de bancos e seguradoras. Cada nota é autocontida; a seção **Armadilhas** pesa no
*quando não usar*.

**Fronteira com [[03-Dominios/Engenharia/Comunicação entre Sistemas/index|Comunicação entre Sistemas]]:**
este catálogo trata os **padrões nomeados como vocabulário de design** (lente Camel/Spring Integration);
o galho Comunicação trata a **infra e a decisão** (qual broker, síncrono × assíncrono, JMS/IBM MQ/ESB,
garantias de entrega). Sobreposição intencional → cross-link "aprofunde na infra". **Outbox e Saga** são
padrões de arquitetura de eventos (família 5 Eventos), fora desta.

## Iniciado — os blocos base

1. [[01 - Panorama da integração]] — os 4 estilos de integração, os 6 grupos de Hohpe, a lente Camel/Spring Integration, "smart endpoints, dumb pipes".
2. [[02 - Message]] — o envelope (header + payload); Command / Document / Event Message.
3. [[03 - Message Channel]] — fila (point-to-point) × tópico (publish-subscribe); o canal que desacopla.
4. [[04 - Pipes and Filters]] — o pipeline de filtros independentes; a metáfora-mãe que faz os padrões comporem.

## Adepto — roteamento e transformação

5. [[05 - Content-Based Router + Message Filter]] — rotear pelo conteúdo (1 de N); filtrar (passa/descarta).
6. [[06 - Splitter + Aggregator]] — o par fan-out/fan-in; o Aggregator stateful e suas 4 decisões.
7. [[07 - Recipient List + Scatter-Gather + Resequencer]] — enviar a N destinos, compor respostas, reordenar.
8. [[08 - Message Translator + Normalizer]] — o Adapter da mensageria; os 4 níveis de tradução.
9. [[09 - Canonical Data Model]] — o modelo comum que corta o N×N (e o god-schema que o arruína).

## Magus — endpoints, confiabilidade e escala

*Em construção.* Consumers (Polling × Event-Driven) · Competing Consumers · Idempotent Receiver · Guaranteed Delivery + Dead Letter Channel · Message Bus × Broker.

## Todas as notas

```dataview
TABLE fase, status, updated
FROM "03-Dominios/Engenharia/Design de Software/Padrões de Projeto/Integração Empresarial (EIP)"
WHERE type = "concept"
SORT file.name ASC
```

## Veja também

- [[03-Dominios/Engenharia/Design de Software/Padrões de Projeto/index|Padrões de Projeto]] — o galho-pai e as outras famílias.
- [[03-Dominios/Engenharia/Design de Software/Padrões de Projeto/Acesso a Dados/index|Acesso a Dados]] — a família anterior.
- [[03-Dominios/Engenharia/Comunicação entre Sistemas/index|Comunicação entre Sistemas]] — a infra de mensageria por baixo dos padrões.
