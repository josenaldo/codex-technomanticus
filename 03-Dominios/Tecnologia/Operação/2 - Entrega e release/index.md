---
title: "Entrega e release"
type: moc
publish: true
tags:
  - operacao
  - devops
  - ci-cd
  - moc
created: 2026-07-08
---

# Entrega e release — Operação

Levar código a produção **com segurança e velocidade** — as duas coisas ao mesmo tempo, não uma às custas da outra. Este sub-galho (fase **Adepto**) trata a entrega como problema de engenharia: como desenhar um pipeline que dá feedback rápido sem abrir mão de gates, quais estratégias de deploy trocam risco por custo, como reverter em segundos, como mudar o schema do banco sem downtime, e como versionar a própria infraestrutura. O leitor já sabe usar GitHub Actions; aqui aprende as **decisões** que separam um deploy de sexta 18h que derruba o site de um deploy que ninguém percebe.

## Notas

1. [[01 - Pipeline de CI-CD como decisão de design]]
2. [[02 - Deployment strategies]]
3. [[03 - Progressive delivery e rollback]]
4. [[04 - Migrations de banco em produção]]
5. [[05 - GitOps e Infrastructure as Code]]
6. [[06 - Secrets e configuração em produção]]

## Veja também

- [[Operação/index|Operação]] — o galho-pai
- [[1 - O ofício de operar/index|O ofício de operar]] — o enquadramento (deploy≠release vem de lá)
- [[3 - Rodar em produção/index|Rodar em produção]] — o que acontece depois que a release sobe
