---
title: "Python"
type: moc
publish: true
created: 2026-05-21
updated: 2026-07-11
status: growing
tags:
  - moc
  - python
aliases:
  - Estante Python
---
# Python

> [!abstract] TL;DR
> Trilha Python organizada em **19 galhos** progressivos, do zero até produção — passando por data model, tipagem, concorrência, persistência, web/APIs, arquitetura, mensageria, microservices e certificação. Cada galho é um conjunto de notas atômicas em 3 fases de aprendizado (Iniciado/Adepto/Magus), no mesmo padrão da trilha [[03-Dominios/Tecnologia/Java/index|Java]]. POV fullstack backend — IA com Python fica pra uma trilha futura cross-language. A trilha cresce um galho por vez; só os galhos publicados têm link ativo abaixo.

Python aparece aqui como linguagem de propósito geral com foco em desenvolvimento backend fullstack. Semeando a partir do spec [[00-Meta/specs/2026-07-09-python-trilha-design]] — ver [[roadmap]] pro estado de cada galho.

## Galhos da trilha

### Núcleo da linguagem

1. [[03-Dominios/Tecnologia/Python/Core/index|Core]] — sintaxe, tipos, controle de fluxo, funções, erros/exceções, módulos/imports (9 notas, 2026-07-09)
2. [[03-Dominios/Tecnologia/Python/Collections e Comprehensions/index|Collections e Comprehensions]] — list/dict/set/tuple, comprehensions, itertools, módulo collections (8 notas, 2026-07-09)
3. [[03-Dominios/Tecnologia/Python/OO e Data Model/index|OO e Data Model]] — classes, dunder methods, properties, dataclasses, ABC/Protocol, metaclasses, composição vs herança (9 notas, 2026-07-09)
4. [[03-Dominios/Tecnologia/Python/Funcional e idiomas avançados/index|Funcional e idiomas avançados]] — iterators, generators, yield from, closures, decorators, functools, context managers via generator (9 notas, 2026-07-10)
5. [[03-Dominios/Tecnologia/Python/Tipagem moderna/index|Tipagem moderna]] — type hints, Union/Optional, generics, mypy/pyright, TypedDict/Literal/NewType, Pydantic, typing avançado (8 notas, 2026-07-10)
6. [[03-Dominios/Tecnologia/Python/CPython internals/index|CPython internals]] — ceval loop, PyObject/refcounting, GC geracional, GIL, free-threading (PEP 703), memory management, profiling (9 notas, 2026-07-10)

### Concorrência e execução

7. [[03-Dominios/Tecnologia/Python/Concorrência e paralelismo/index|Concorrência e paralelismo]] — threading, multiprocessing, concurrent.futures, asyncio fundamentals (8 notas, 2026-07-10)
8. [[03-Dominios/Tecnologia/Python/Programação Reativa e Assíncrona/index|Programação Reativa e Assíncrona]] — asyncio deep-dive, aiohttp, ASGI, back-pressure (8 notas, 2026-07-11)

### Backend e arquitetura

9. [[03-Dominios/Tecnologia/Python/Persistência de dados/index|Persistência de dados]] — SQLAlchemy, Django ORM, migrations, N+1, transações (8 notas, 2026-07-11)
10. [[03-Dominios/Tecnologia/Python/Web e APIs REST/index|Web e APIs REST]] — Django vs FastAPI vs Flask, routing, serialização, validação com Pydantic (9 notas, 2026-07-11)
11. [[03-Dominios/Tecnologia/Python/Segurança/index|Segurança]] — OWASP Top 10, injeção, XSS/CSRF, validação como segurança, secrets, supply chain, rate limiting (9 notas, 2026-07-11)
12. **Testes** — pytest, fixtures, mocking, coverage, TDD *(planejado)*
13. **Arquitetura e Design Patterns** — Repository/Unit of Work, DI, hexagonal/clean architecture *(planejado)*

### Plataforma distribuída e produção

14. **Mensageria** — Celery, RQ, aio-pika, kafka-python/aiokafka *(planejado)*
15. **Microservices e sistemas distribuídos** — comunicação entre serviços em Python *(planejado)*
16. **Build e tooling** — packaging moderno (uv, poetry), virtual envs, pyproject.toml, ruff/black *(planejado)*
17. **Observabilidade e produção** — logging, OpenTelemetry, WSGI/ASGI, deploy *(planejado)*
18. **Cloud-native e produção** — containers Python, serverless/Lambda Python *(planejado)*

### Certificação

19. **Certificação (PCEP/PCAP)** — guia de estudo mapeado aos galhos 1-6 *(planejado)*

## Referência

- [[03-Dominios/Tecnologia/Python/Python Backend|Python Backend]] — tronco original (em transição; sendo podado conforme galhos absorvem o conteúdo)
- [[03-Dominios/Tecnologia/Python/Instalando Anaconda no Ubuntu|Instalando Anaconda no Ubuntu]] — setup de ambiente
- [[Senda Python]] — lista de cursos/vídeos/livros externos usada como pesquisa prévia da trilha

## Veja também

- [[03-Dominios/Tecnologia/Java/index|Java]] — trilha irmã, mesmo padrão estrutural
- [[03-Dominios/Tecnologia/Node/index|Node]] — trilha irmã no ecossistema JS
- [[03-Dominios/Engenharia/Comunicação entre Sistemas/index|Comunicação entre Sistemas]] — conceitos de API/mensageria que os galhos 10/14/15 implementam em Python
