---
title: "Python — Concorrência e paralelismo"
created: 2026-07-10
type: moc
status: growing
publish: true
tags:
  - python
  - moc
aliases:
  - "Galho 7 - Concorrência e paralelismo"
---

# Concorrência e paralelismo

> [!abstract] TL;DR
> Galho 7 da trilha Python: as ferramentas de verdade para lidar com I/O-bound e CPU-bound em Python — `threading` (locks, sincronização, produtor-consumidor), `multiprocessing` (paralelismo real, contornando o GIL), `concurrent.futures` (a abstração que unifica os dois), e `asyncio` (concorrência cooperativa via event loop). Fase Adepto→Magus; 8 notas. Assume o Galho [[03-Dominios/Tecnologia/Python/CPython internals/index|6 (CPython internals)]] como pré-requisito — o GIL em si (o que é, por que existe, free-threading/PEP 703) já foi explicado lá; aqui o assunto é **o que fazer com essa restrição na prática**.

## Sobre este galho

O Galho 6 explicou por que `threading` não acelera CPU-bound em Python (o GIL) e por que `multiprocessing` sim (processos isolados, sem GIL compartilhado). Este galho pega esse mecanismo como dado e foca na **caixa de ferramentas**: como usar `Lock`/`Semaphore`/`Condition` corretamente sem deadlock, como orquestrar processos com `Pool`/`ProcessPoolExecutor`, como `concurrent.futures` esconde a escolha threading-vs-multiprocessing atrás de uma API comum, e como `asyncio` resolve I/O-bound de um jeito totalmente diferente (um único thread, cooperação via `await`, sem GIL como fator).

**Audiência:** quem já entende o *porquê* do GIL (Galho 6) e precisa escrever código concorrente/paralelo de verdade — a pergunta aqui não é "o que é o GIL" mas "qual ferramenta eu pego pra este problema".

## Adepto

1. [[01 - Threading na prática — Thread, Lock e condições de corrida|01 — Threading na prática: `Thread`, `Lock` e condições de corrida]]
2. [[02 - Sincronização avançada — Semaphore, Condition, Event, Barrier|02 — Sincronização avançada: `Semaphore`, `Condition`, `Event`, `Barrier`]]
3. [[03 - queue.Queue e o padrão produtor-consumidor|03 — `queue.Queue` e o padrão produtor-consumidor]]

## Adepto→Magus

4. [[04 - multiprocessing na prática — Pool, ProcessPoolExecutor e orquestração|04 — `multiprocessing` na prática: `Pool`, `ProcessPoolExecutor` e orquestração]]
5. [[05 - concurrent.futures — a abstração unificadora|05 — `concurrent.futures`: a abstração unificadora]]

## Magus

6. [[06 - asyncio fundamentals — event loop, coroutines e Task|06 — `asyncio` fundamentals: event loop, coroutines e `Task`]]
7. [[07 - asyncio na prática — gather, TaskGroup, timeouts e cancelamento|07 — `asyncio` na prática: `gather`, `TaskGroup`, timeouts e cancelamento]]
8. [[08 - Capstone — escolhendo threading vs multiprocessing vs asyncio|08 — Capstone: escolhendo threading vs multiprocessing vs asyncio]] — recapitula o galho.

## Veja também

- [[03-Dominios/Tecnologia/Python/index|Trilha Python]] (MOC central)
- [[03-Dominios/Tecnologia/Python/CPython internals/index|CPython internals]] — Galho 6 (pré-requisito; o GIL em si mora lá, não repetido aqui)
- [[03-Dominios/Tecnologia/Python/Programação Reativa e Assíncrona/index|Programação Reativa e Assíncrona]] — Galho 8 (próximo; aprofunda `asyncio` além do fundamentals: `aiohttp`, frameworks async, back-pressure)
