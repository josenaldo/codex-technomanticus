---
title: "Python — Programação Reativa e Assíncrona"
created: 2026-07-11
type: moc
status: growing
publish: true
tags:
  - python
  - moc
aliases:
  - "Galho 8 - Programação Reativa e Assíncrona"
---

# Programação Reativa e Assíncrona

> [!abstract] TL;DR
> Galho 8 da trilha Python: o "além do fundamentals" de `asyncio` — o event loop por dentro (selectors, callbacks, a relação real entre `Future` e `Task`), streams assíncronos de rede, `aiohttp` como cliente e servidor de produção, o protocolo ASGI que sustenta frameworks como FastAPI/Starlette, back-pressure, e os padrões de produção (supervisão de tasks, graceful shutdown, circuit breaker assíncrono) que fecham num capstone de web scraper concorrente. Fase Magus; 8 notas. Assume o Galho [[03-Dominios/Tecnologia/Python/Concorrência e paralelismo/index|7 (Concorrência e paralelismo)]] como pré-requisito — event loop/coroutines/`Task`/`gather`/`TaskGroup`/cancelamento já foram explicados lá; aqui o assunto é **rede, produção e o ecossistema em volta do asyncio**.

## Sobre este galho

O Galho 7 ensinou o vocabulário básico do `asyncio` — como escrever e orquestrar coroutines. Este galho assume esse vocabulário como dado e vai pro que você realmente faz com `asyncio` em produção: falar com a rede (streams, `aiohttp`), construir servidores assíncronos de verdade (ASGI), controlar quanto trabalho concorrente seu sistema aguenta (back-pressure), e manter isso rodando de forma resiliente (supervisão, graceful shutdown, circuit breaker).

**Audiência:** quem já escreve `async def`/`await`/`TaskGroup` com confiança (Galho 7) e precisa colocar isso pra falar com o mundo real — APIs, scrapers, integrações — sem travar o event loop ou saturar o sistema.

## Magus

1. [[01 - Event loop por dentro — selectors, callbacks e a relação Future-Task|01 — Event loop por dentro: selectors, callbacks e a relação `Future`/`Task`]]
2. [[02 - Streams assíncronos — StreamReader, StreamWriter e protocolos de rede|02 — Streams assíncronos: `StreamReader`, `StreamWriter` e protocolos de rede]]
3. [[03 - aiohttp cliente — ClientSession, connection pooling e requisições concorrentes|03 — `aiohttp` cliente: `ClientSession`, connection pooling e requisições concorrentes]]
4. [[04 - aiohttp servidor — web.Application, routing e middlewares|04 — `aiohttp` servidor: `web.Application`, routing e middlewares]]
5. [[05 - ASGI e o ecossistema de frameworks assíncronos|05 — ASGI e o ecossistema de frameworks assíncronos]]
6. [[06 - Back-pressure — Semaphore, Queue com maxsize e buffering|06 — Back-pressure: `Semaphore`, `Queue` com `maxsize` e buffering]]
7. [[07 - Padrões de produção com asyncio — supervisão de tasks, graceful shutdown, circuit breaker|07 — Padrões de produção com `asyncio`: supervisão de tasks, graceful shutdown, circuit breaker]]
8. [[08 - Capstone — web scraper assíncrono de produção|08 — Capstone: web scraper assíncrono de produção]] — recapitula o galho.

## Todas as notas

```dataview
TABLE fase, status FROM "03-Dominios/Tecnologia/Python/Programação Reativa e Assíncrona" WHERE type = "concept" SORT file.name ASC
```

## Veja também

- [[03-Dominios/Tecnologia/Python/index|Trilha Python]] (MOC central)
- [[03-Dominios/Tecnologia/Python/Concorrência e paralelismo/index|Concorrência e paralelismo]] — Galho 7 (pré-requisito; fundamentals de asyncio moram lá, não repetidos aqui)
- [[03-Dominios/Tecnologia/Python/Web e APIs REST/index|Web e APIs REST]] — Galho 10 (próximo na trilha; FastAPI/Django/Flask em profundidade — aqui só o protocolo ASGI que os sustenta)
