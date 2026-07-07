---
title: "Padrões recorrentes"
type: moc
publish: true
tags:
  - system-design
  - moc
created: 2026-07-07
---

# Padrões recorrentes — System Design

Se os [[2 - Building blocks/index|Building blocks]] são as peças, este sub-galho (fase **Adepto**) é a **caixa de combinações que reaparece em quase todo design não-trivial**. Pub/Sub, CQRS, Event Sourcing, Rate Limiting, Circuit Breaker, API Gateway — cada um é uma resposta madura a um problema recorrente de escala. Aqui eles são vistos pela lente *"como usar em escala"*, não *"como modelar o domínio"* (essa mora em [[Event Storming]] e [[Arquitetura de Software]]). Domine estes padrões e você para de reinventar a roda no whiteboard: aponta o padrão pelo nome e justifica o trade-off.

## Notas

1. [[01 - Pub-Sub e event-driven em escala]]
2. [[02 - CQRS sob a ótica de system design]]
3. [[03 - Event Sourcing sob a ótica de system design]]
4. [[04 - Rate Limiting]]
5. [[05 - Circuit Breaker e resiliência]]
6. [[06 - API Gateway e BFF]]

## Veja também

- [[System Design/index|System Design]] — o galho-pai
- [[2 - Building blocks/index|Building blocks]] — as peças que estes padrões combinam
- [[4 - Walkthroughs/index|Walkthroughs]] — os designs completos onde os padrões são aplicados
