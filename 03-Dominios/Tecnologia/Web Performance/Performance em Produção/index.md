---
title: "Performance em Produção — índice"
created: 2026-07-06
updated: 2026-07-06
type: index
tags:
  - web-performance
  - produção
  - ci
  - cultura
publish: true
---

# Performance em Produção

Galho 4 da trilha Web Performance — o que **fecha** o domínio. Depois de aprender a **medir** (G1), **carregar rápido** (G2) e **manter responsivo** (G3), aqui você aprende a **sustentar** — o "sustentar" da metáfora *medir → carregar → responder → sustentar*. Porque performance conquistada apodrece: sem um sistema que a vigie, cada deploy adiciona "só mais um script" e, em meses, você volta ao vermelho.

Este galho transforma performance de esforço pontual em **prática de engenharia**: budgets que quebram o build, RUM em produção, detecção de regressão, diagnóstico avançado, o business case para priorizar, e a cultura que mantém tudo de pé.

---

## Fase Iniciado

- [[03-Dominios/Tecnologia/Web Performance/Performance em Produção/01 - Do lab ao CI - Lighthouse CI|01 — Do lab ao CI: Lighthouse CI]] — automatizar a auditoria no pipeline
- [[03-Dominios/Tecnologia/Web Performance/Performance em Produção/02 - Budgets no pipeline|02 — Budgets no pipeline]] — bundle size + performance budgets como gate que falha o build
- [[03-Dominios/Tecnologia/Web Performance/Performance em Produção/03 - RUM em produção|03 — RUM em produção]] — o pipeline de dados de campo: coletar, transportar, guardar, visualizar

## Fase Adepto

- [[03-Dominios/Tecnologia/Web Performance/Performance em Produção/04 - Detecção de regressão e alertas|04 — Detecção de regressão e alertas]] — comparar releases, alertar quando o p75 piora
- [[03-Dominios/Tecnologia/Web Performance/Performance em Produção/05 - Monitoramento sintético contínuo|05 — Monitoramento sintético contínuo]] — checagens agendadas e ferramentas de monitoramento
- [[03-Dominios/Tecnologia/Web Performance/Performance em Produção/06 - Diagnóstico avançado no DevTools|06 — Diagnóstico avançado no DevTools]] — o Performance panel a fundo: flame chart, culprit

## Fase Magus

- [[03-Dominios/Tecnologia/Web Performance/Performance em Produção/07 - O business case da performance|07 — O business case da performance]] — ligar métrica a receita e priorizar
- [[03-Dominios/Tecnologia/Web Performance/Performance em Produção/08 - Cultura de performance|08 — Cultura de performance]] — ownership, prevenir o apodrecimento. **Capstone do domínio**

---

## Fim do domínio

Este é o último galho de Web Performance. Ao completá-lo, o domínio cobre o ciclo inteiro — *medir → carregar → responder → sustentar*. Volte ao [[03-Dominios/Tecnologia/Web Performance/index|índice do domínio]] para o mapa completo.
