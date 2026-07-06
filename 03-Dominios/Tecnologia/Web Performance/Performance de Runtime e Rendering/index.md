---
title: "Performance de Runtime & Rendering — índice"
created: 2026-07-06
updated: 2026-07-06
type: index
tags:
  - web-performance
  - runtime
  - inp
  - cls
publish: true
---

# Performance de Runtime & Rendering

Galho 3 da trilha Web Performance. Depois de **medir** (G1) e **carregar rápido** (G2), aqui você mantém a página **responsiva** enquanto o usuário interage — o "responder" da metáfora *medir → carregar → responder → sustentar*. É o galho do **INP** e do **CLS de runtime**: a thread principal, as long tasks, o custo do JavaScript, o reflow/repaint, e como tirar trabalho do caminho da interação.

A ordem das notas vai da causa raiz (a thread principal única) ao remédio final (mover trabalho pra fora dela): primeiro **a thread e o custo do JS**, depois **o pipeline de rendering** (layout, paint, composite), e por fim **offload e frameworks**.

---

## Fase Iniciado

- [[03-Dominios/Tecnologia/Web Performance/Performance de Runtime e Rendering/01 - A thread principal e o event loop|01 — A thread principal e o event loop]] — por que travar uma thread só trava tudo
- [[03-Dominios/Tecnologia/Web Performance/Performance de Runtime e Rendering/02 - Long tasks e o custo do JavaScript|02 — Long tasks e o custo do JavaScript]] — tarefas > 50 ms, parse/compile/execute
- [[03-Dominios/Tecnologia/Web Performance/Performance de Runtime e Rendering/03 - INP a fundo|03 — INP a fundo]] — input delay, processing, presentation; ceder a thread

## Fase Adepto

- [[03-Dominios/Tecnologia/Web Performance/Performance de Runtime e Rendering/04 - Reflow, repaint e o custo do layout|04 — Reflow, repaint e o custo do layout]] — quando o layout recalcula e o que o força
- [[03-Dominios/Tecnologia/Web Performance/Performance de Runtime e Rendering/05 - Layout thrashing|05 — Layout thrashing]] — ler/escrever o DOM em loop, reflows síncronos, batching
- [[03-Dominios/Tecnologia/Web Performance/Performance de Runtime e Rendering/06 - Compositing e animações na GPU|06 — Compositing e animações na GPU]] — camadas, `transform`/`opacity`, `will-change`
- [[03-Dominios/Tecnologia/Web Performance/Performance de Runtime e Rendering/07 - CLS em runtime|07 — CLS em runtime]] — deslocamentos pós-carregamento: conteúdo injetado, ads, bfcache

## Fase Magus

- [[03-Dominios/Tecnologia/Web Performance/Performance de Runtime e Rendering/08 - Offload, Web Workers e o custo da hidratação|08 — Offload, Web Workers e o custo da hidratação]] — tirar trabalho da main thread; custo de framework, hidratação, islands. **Capstone**

---

## Próximo galho

**G4 — Performance em Produção** *(a construir)* — quando tudo já está otimizado no código: budgets no CI, RUM/monitoramento de regressão, DevTools em profundidade, cultura de performance. Sustenta os ganhos dos Galhos 1–3 ao longo do tempo.
