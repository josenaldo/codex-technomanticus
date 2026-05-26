---
title: "Streams"
created: 2026-05-08
updated: 2026-05-08
type: moc
status: seedling
publish: true
tags:
  - node
  - streams
  - moc
aliases:
  - Node Streams
  - Galho 3 - Streams
---

# Streams

> [!abstract] TL;DR
> Galho 3 da trilha Node Senior. Cobre a abstração fundamental do Node para processar dados sem carregar tudo em memória: 4 tipos (Readable, Writable, Duplex, Transform), backpressure, pipeline vs pipe, async iteration moderna, Web Streams interop, padrões práticos (line parser, CSV → JSONL, fetch streaming) e tuning de performance. Pré-requisito: galho 1 (Runtime e Event Loop).

## Sobre este galho

Este galho cobre **streams em Node** — abstração fundamental para processar dados em chunks sem carregar tudo em memória. Inclui o mental model dos 4 tipos (Readable, Writable, Duplex, Transform), backpressure como mecânica explícita, `pipeline` como API moderna que substitui `.pipe()`, async iteration com `for await of`, Web Streams interop (padrão universal de 2026), padrões práticos (line parser, CSV → JSONL, fetch streaming, multipart upload) e tuning de performance.

Pré-requisito: galho 1 ([[03-Dominios/Node/Runtime e Event Loop/index]]) — pressupõe entender event loop e bloqueio. Galho 2 ([[03-Dominios/Node/Paralelismo/index]]) é referência cruzada onde workers + streams se cruzam (`postMessage` + `transferList` para zero-copy).

**Audiência primária:** dev senior em prep para entrevista internacional. Cada nota tem seção "Em entrevista" com frase pronta em inglês + vocabulário.

**Audiência secundária:** o mesmo dev em produção, debugando memory growth em endpoint que processa CSVs grandes ou throughput baixo de pipeline de transform.

## Comece por aqui — trilha completa (12 notas)

### Bloco A — Mental model

1. [[01 - Por que streams]]
2. [[02 - Os 4 tipos - Readable, Writable, Duplex, Transform]]

### Bloco B — Tipos aprofundados

3. [[03 - Readable streams]]
4. [[04 - Writable streams]]
5. [[05 - Duplex e Transform]]

### Bloco C — Backpressure e pipeline

6. [[06 - Backpressure]]
7. [[07 - pipeline vs pipe - error handling]]

### Bloco D — Streams modernos

8. [[08 - Async iteration de streams]]
9. [[09 - Web Streams - interop com padrão universal]]

### Bloco E — Padrões e fechamento

10. [[10 - Padrões práticos]]
11. [[11 - Performance e tuning]]
12. [[12 - Armadilhas, regras práticas, cheatsheet]]

## Rotas alternativas

### Rota entrevista internacional

01 → 02 → 03 → 04 → 06 → 07 → 09. Foco em "explicar streams pra entrevistador".

### Rota produção

01 → 06 → 07 → 10 → 11 → 12. Foco em "escrever streams sem bugs em prod".

### Rota async-first (2026 stack)

02 → 08 → 09 → 10. Streams modernos com async iter + Web Streams.

### Rota implementing custom streams

03 → 04 → 05 → 06 → 11. Pra quem vai escrever Transform/Duplex próprio.

## Todas as notas

```dataview
TABLE status, updated
FROM "03-Dominios/Node/Streams"
WHERE type = "concept"
SORT file.name ASC
```

## Veja também

- [[03-Dominios/Node/index|Node.js (MOC central)]]
- [[Node.js]] — tronco (deep dive panorâmico)
- [[03-Dominios/Node/Runtime e Event Loop/index]] — galho 1 (pré-requisito)
- [[03-Dominios/Node/Paralelismo/index]] — galho 2 (referência cruzada onde workers + streams)
