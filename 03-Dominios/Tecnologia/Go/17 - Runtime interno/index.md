---
title: "Go — Runtime interno"
type: moc
publish: true
created: 2026-07-18
updated: 2026-07-18
status: growing
tags:
  - moc
  - go
  - runtime
  - internals
aliases:
  - Galho 17 Go
  - Runtime interno Go
---
# Go — Runtime interno

> [!abstract] TL;DR
> Galho 17 da trilha [[03-Dominios/Tecnologia/Go/index|Go]] — o que roda por baixo do seu binário. É o par do "CPython internals": um diferencial sênior que cai em entrevista. 8 notas em 3 fases: o runtime não é uma VM (Iniciado); scheduler GMP a fundo, stacks que crescem, escape analysis e o garbage collector (Adepto); tuning de GC, memory model e otimização guiada por entendimento (Magus). Ao fim, você raciocina sobre custo e desempenho a partir de como Go de fato funciona.

Aqui o galho 7 (visão de topo do scheduler) vira detalhe: work stealing, write barriers, stacks contíguas e a decisão stack-vs-heap.

## Notas por fase

### Iniciado — o que é o runtime

1. [[01 - O runtime Go por baixo]] — o que o runtime faz, por que não é VM/interpretador, código linkado no binário

### Adepto — os mecanismos

2. [[02 - O scheduler GMP a fundo]] — run queues, work stealing, syscalls, preempção assíncrona (1.14)
3. [[03 - A stack de uma goroutine]] — stacks pequenas e contíguas, stack copying, por que milhões cabem
4. [[04 - Escape analysis]] — stack vs heap, `-gcflags="-m"`, o que faz um valor escapar
5. [[05 - O garbage collector]] — tri-color concurrent mark-sweep, write barrier, STW curtíssimo

### Magus — controle e otimização

6. [[06 - Tuning do GC]] — `GOGC`, `GOMEMLIMIT` (1.19), pacing, `GODEBUG=gctrace`
7. [[07 - O memory model]] — happens-before, o que channels/mutex/atomic garantem sobre visibilidade
8. [[08 - Otimização guiada por entendimento]] — reduzir alocações, `sync.Pool`, quando micro-otimizar

## Veja também

- [[03-Dominios/Tecnologia/Go/index|Trilha Go]] — índice geral (21 galhos + capstone)
- Galho anterior: [[03-Dominios/Tecnologia/Go/16 - Observabilidade/index|Observabilidade]]
- Próximo galho: **Cloud-native e produção** (galho 18) — do binário estático ao pod rodando no cluster
