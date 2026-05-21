---
title: "Paralelismo"
created: 2026-05-07
updated: 2026-05-07
type: moc
status: seedling
publish: true
tags:
  - node
  - paralelismo
  - moc
aliases:
  - Worker Threads
  - Galho 2 - Paralelismo
---

# Paralelismo

> [!abstract] TL;DR
> Galho 2 da trilha Node Senior. Cobre as 3 ferramentas para fugir do single-thread: Worker Threads (CPU-bound em mesmo processo), Cluster (escalar HTTP por CPU), child_process (rodar comando externo ou spawn de Node). Inclui SharedArrayBuffer/Atomics, pool de workers, contexto de produção (PM2 vs K8s), e decision tree. Pré-requisito: galho 1 (Runtime e Event Loop).

## Sobre este galho

Este galho cobre **as 3 ferramentas de paralelismo em Node**: Worker Threads (threads JS no mesmo processo), Cluster (múltiplos processos compartilhando porta HTTP), child_process (processo externo via spawn/exec ou Node child via fork). Inclui SharedArrayBuffer/Atomics (concorrência com memória compartilhada), pool de workers (pattern de produção, `piscina`), contexto de produção em 2026 (Cluster vs PM2 vs Kubernetes) e uma decision tree completa de "qual ferramenta para qual problema".

Pré-requisito: galho 1 ([[03-Dominios/Node/Runtime e Event Loop/index]]). Em particular as notas [[09 - async-await - o que é, o que não é]] (mito da performance) e [[10 - Bloqueio do event loop - sintomas e causas]] (sintomas que pedem paralelismo).

**Audiência primária:** dev senior em prep para entrevista internacional. Cada nota tem seção "Em entrevista" com frase pronta em inglês + vocabulário.

**Audiência secundária:** o mesmo dev decidindo arquitetura ou debugando problemas de CPU em produção.

## Comece por aqui — trilha completa (12 notas)

### Bloco A — Mental model e fundamentos

1. [[01 - Por que paralelismo em Node]]
2. [[02 - As 3 ferramentas - Worker Threads, Cluster, child_process]]

### Bloco B — Worker Threads

3. [[03 - Worker Threads - fundamentos]]
4. [[04 - Comunicação entre workers - postMessage e MessageChannel]]
5. [[05 - Memória compartilhada - SharedArrayBuffer e Atomics]]
6. [[06 - Pool de workers - pattern de produção]]

### Bloco C — Multi-processo

7. [[07 - Cluster - escalando HTTP por CPU]]
8. [[08 - child_process com exec e spawn]]
9. [[09 - child_process com fork - Node child com IPC]]

### Bloco D — Produção

10. [[10 - Cluster vs PM2 vs Kubernetes - quem orquestra]]
11. [[11 - Decision tree - qual ferramenta para qual problema]]

### Bloco E — Fechamento

12. [[12 - Armadilhas, regras práticas, cheatsheet]]

## Rotas alternativas

### Rota entrevista internacional

01 → 02 → 03 → 05 → 07 → 11. Foco em "explicar os 3 modelos pra entrevistador".

### Rota produção

01 → 06 → 07 → 10 → 12. Foco em "pôr em produção".

### Rota CPU-bound

01 → 03 → 04 → 06. Foco em "escapar do bloqueio com Worker Threads".

### Rota integração com OS

01 → 02 → 08 → 09. Foco em "rodar comandos externos e spawn de Node".

## Todas as notas

```dataview
TABLE status, updated
FROM "03-Dominios/Node/Paralelismo"
WHERE type = "concept"
SORT file.name ASC
```

## Veja também

- [[03-Dominios/Node/index|Node.js (MOC central)]]
- [[Node.js]] — tronco (deep dive panorâmico)
- [[03-Dominios/Node/Runtime e Event Loop/index]] — galho 1 (pré-requisito)
