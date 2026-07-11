---
title: "Python — Web e APIs REST"
created: 2026-07-11
type: moc
status: growing
publish: true
tags:
  - python
  - moc
aliases:
  - "Galho 10 - Web e APIs REST"
---

# Web e APIs REST

> [!abstract] TL;DR
> Galho 10 da trilha Python: como expor uma aplicação Python como API HTTP em produção — panorama comparativo Django vs. FastAPI vs. Flask, roteamento, validação e serialização com Pydantic, injeção de dependência do FastAPI, Django REST Framework (serializers/viewsets/routers), tratamento de erros padronizado, middleware e ciclo de vida da requisição, documentação automática via OpenAPI, fechando com uma API completa de ponta a ponta. Fase Adepto; 9 notas. Segundo galho do bloco "Backend e arquitetura" (9-13) — consome a camada de persistência do Galho 9.

## Sobre este galho

O Galho 9 ensinou como Python guarda estado no banco; este galho ensina como Python expõe esse estado (e qualquer outra lógica de negócio) como uma API HTTP consumível. Três frameworks dominam o ecossistema: `Flask` (minimalista, WSGI, você monta o resto), `Django` (opinativo, "baterias inclusas", REST via Django REST Framework) e `FastAPI` (ASGI, tipagem como contrato via Pydantic, o mais recente e o mais indicado pela comunidade brasileira hoje — Dunossauro/FastAPI do Zero). O galho não escolhe um vencedor absoluto: mostra os três lado a lado nos temas fundamentais (roteamento, validação, erros) e aprofunda FastAPI e DRF nos temas onde cada um tem identidade própria (injeção de dependência no FastAPI; serializers/viewsets no DRF).

**Fronteiras anti-duplicação:** o protocolo ASGI cru (`scope`/`receive`/`send`) já foi coberto no [[03-Dominios/Tecnologia/Python/Programação Reativa e Assíncrona/index|Galho 8]] (nota 05) — aqui ele só é referenciado, nunca reexplicado. A camada de persistência (SQLAlchemy/Django ORM, migrations, N+1, transações, pooling) é o [[03-Dominios/Tecnologia/Python/Persistência de dados/index|Galho 9]] — aqui os endpoints consomem essa camada, sem repetir os conceitos. Autenticação/autorização de API (JWT, OAuth2, API keys) fica para o [[03-Dominios/Tecnologia/Python/Segurança/index|Galho 11]] — este galho valida e serializa dados, não protege endpoints. Testes de API (TestClient, pytest fixtures para rotas) ficam para o [[03-Dominios/Tecnologia/Python/Testes/index|Galho 12]]. Repository/Unit of Work como padrão de arquitetura formal ficam para o [[03-Dominios/Tecnologia/Python/Arquitetura e Design Patterns/index|Galho 13]].

**Audiência:** quem já fecha o núcleo da linguagem (galhos 1-6), concorrência (7-8) e persistência (9) e precisa expor tudo isso como serviço HTTP consumível por um frontend ou outro serviço.

## Adepto

1. [[01 - Django vs FastAPI vs Flask — panorama e filosofias|01 — Django vs. FastAPI vs. Flask: panorama e filosofias]]
2. [[02 - Roteamento — decorators, urls.py e path operations|02 — Roteamento: decorators, `urls.py` e path operations]]
3. [[03 - Validação e serialização com Pydantic|03 — Validação e serialização com Pydantic]]
4. [[04 - Injeção de dependência no FastAPI — Depends|04 — Injeção de dependência no FastAPI: `Depends`]]
5. [[05 - Django REST Framework — serializers, viewsets e routers|05 — Django REST Framework: serializers, viewsets e routers]]
6. [[06 - Tratamento de erros e respostas HTTP padronizadas|06 — Tratamento de erros e respostas HTTP padronizadas]]
7. [[07 - Middleware e o ciclo de vida da requisição|07 — Middleware e o ciclo de vida da requisição]]
8. [[08 - Documentação automática com OpenAPI|08 — Documentação automática com OpenAPI]]
9. [[09 - Capstone — uma API REST completa de ponta a ponta|09 — Capstone: uma API REST completa de ponta a ponta]] — recapitula o galho.

## Todas as notas

```dataview
TABLE fase, status FROM "03-Dominios/Tecnologia/Python/Web e APIs REST" WHERE type = "concept" SORT file.name ASC
```

## Veja também

- [[03-Dominios/Tecnologia/Python/index|Trilha Python]] (MOC central)
- [[03-Dominios/Tecnologia/Python/Persistência de dados/index|Persistência de dados]] — Galho 9 (a camada de dados que os endpoints deste galho consomem)
- [[03-Dominios/Tecnologia/Python/Programação Reativa e Assíncrona/index|Programação Reativa e Assíncrona]] — Galho 8 (protocolo ASGI cru, referenciado aqui sem repetição)
- [[03-Dominios/Tecnologia/Python/Segurança/index|Segurança]] — Galho 11 (próximo; autenticação/autorização de API)
- [[03-Dominios/Tecnologia/Java/Web e APIs REST/index|Java — Web e APIs REST]] — trilha irmã, EXEMPLAR estrutural (Spring MVC)
