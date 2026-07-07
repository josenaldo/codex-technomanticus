---
title: "Walkthroughs"
type: moc
publish: true
tags:
  - system-design
  - moc
created: 2026-07-07
---

# Walkthroughs — System Design

O coração da trilha. Aqui os [[1 - Framework de entrevista/index|processo]], os [[2 - Building blocks/index|building blocks]] e os [[3 - Padrões recorrentes/index|padrões]] se encontram num único quadro branco: **oito designs clássicos conduzidos ponta a ponta**, cada um do enunciado vago até os trade-offs finais. Esta é a fase **Magus** — não se lê para *aprender um conceito*, lê-se para *ver o método em ação* e reconhecer os padrões que se recombinam sob restrições novas.

Cada walkthrough segue a mesma espinha: **requisitos → estimativas → API & modelo de dados → diagrama macro → deep dives → gargalos & trade-offs → variações de follow-up**. Não decore os diagramas: absorva *por que* cada peça entrou.

## Notas

1. [[01 - URL Shortener]] — hashing/base62, read-heavy, cache, colisões
2. [[02 - News Feed e Timeline]] — fan-out on-write vs on-read, o problema da celebridade
3. [[03 - Chat System]] — WebSocket, presence, entrega e ordering, fila offline
4. [[04 - Distributed Rate Limiter]] — aprofunda o padrão em sistema completo (Redis, sincronização entre nós)
5. [[05 - Notification System]] — fan-out multi-canal, templates, dedup, retry, prioridade
6. [[06 - Distributed File Storage]] — chunking, metadata service, dedup, sync, consistência
7. [[07 - Web Crawler]] — BFS distribuído, politeness, dedup de URL, armadilhas de spider
8. [[08 - Distributed Key-Value Store]] — consistent hashing, quorum, replicação, gossip, vector clocks

## Veja também

- [[System Design/index|System Design]] — o galho-pai
- [[2 - Building blocks/index|Building blocks]] — as peças que estes designs aplicam
- [[3 - Padrões recorrentes/index|Padrões recorrentes]] — os padrões que reaparecem aqui
