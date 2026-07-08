---
title: "Rodar em produção"
type: moc
publish: true
tags:
  - operacao
  - devops
  - kubernetes
  - moc
created: 2026-07-08
---

# Rodar em produção — Operação

A release subiu. Agora vem a parte que não acaba: **manter o sistema no ar**, escalando com a demanda e sem derrubar ninguém a cada deploy. Este sub-galho (fase **Adepto→Magus**) trata o que acontece depois do deploy — o container como unidade imutável, o contrato que o Kubernetes espera da sua aplicação, como fazer um rolling update sem perder requests, como escalar sob pico sem quebrar o orçamento, e como um serviço sobrevive quando uma dependência sua fica lenta. O leitor já sabe o que é um Pod; aqui aprende a **operá-lo em produção**.

## Notas

1. [[01 - Containers em produção]]
2. [[02 - O contrato de produção do Kubernetes]]
3. [[03 - Zero-downtime e alta disponibilidade]]
4. [[04 - Escala e capacidade]]
5. [[05 - Rede e borda em produção]]
6. [[06 - Resiliência operacional]]

## Veja também

- [[Operação/index|Operação]] — o galho-pai
- [[2 - Entrega e release/index|Entrega e release]] — como a release chegou aqui
- [[4 - Observar e responder/index|Observar e responder]] — enxergar e reagir quando o sistema quebra
