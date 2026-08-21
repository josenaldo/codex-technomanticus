---
title: "Python — Build e tooling"
created: 2026-07-12
type: moc
status: growing
publish: true
tags:
  - python
  - moc
aliases:
  - "Galho 16 - Build e tooling"
---

# Build e tooling

> [!abstract] TL;DR
> Galho 16 da trilha Python: packaging moderno — por que o ecossistema histórico de `pip`+`venv`+`setup.py` era fragmentado, `pyproject.toml` como padrão unificado (PEP 518/621), `uv` (gerenciador moderno, rápido, escrito em Rust) e Poetry (alternativa madura) para dependências/lockfile/publicação, `ruff` (linting rápido) e `black` (formatação automática) com pre-commit hooks. Fecha com capstone aplicando tooling consistente aos dois serviços Python construídos no Galho 15. Fase Iniciado→Adepto; 8 notas. Terceiro galho do bloco "Plataforma distribuída e produção" (14-18).

## Sobre este galho

Este galho é sobre o FERRAMENTAL de desenvolvimento — como organizar, instalar e gerenciar dependências de um projeto Python real, e como manter o código formatado/lintado de forma automática e consistente. Não é sobre segurança de dependências (isso já foi coberto no [[03-Dominios/Tecnologia/Python/Segurança/07 - Segurança de dependências e supply chain|Galho 11 nota 07]] — `pip-audit`, lockfiles como defesa, typosquatting) nem sobre deploy/produção (isso é o Galho 18 futuro).

**Fronteiras anti-duplicação:** segurança de dependências (`pip-audit`, lockfiles como defesa contra supply chain attack) → [[03-Dominios/Tecnologia/Python/Segurança/07 - Segurança de dependências e supply chain|Galho 11 nota 07]], só referenciado — aqui lockfiles são tratados pelo ângulo de REPRODUTIBILIDADE de build, não segurança. Maven/Gradle como exemplar de outra stack → [[03-Dominios/Tecnologia/Java/Build e tooling/index|Java — Build e tooling]], referenciado pra contraste, não repetido. CI/CD como pipeline conceitual → [[03-Dominios/Engenharia/Operação/index|Engenharia/Operação]], referenciado se relevante.

**Audiência:** quem já construiu os dois serviços Python do Galho 15 e precisa de um jeito consistente e moderno de gerenciar dependências, ambiente e qualidade de código entre eles.

## Iniciado

1. [[01 - Panorama — por que packaging Python era confuso|01 — Panorama: por que packaging Python era confuso]]
2. [[02 - Virtual environments — isolamento de dependências|02 — Virtual environments: isolamento de dependências]]
3. [[03 - pyproject.toml — o padrão unificado|03 — pyproject.toml: o padrão unificado]]

## Adepto

4. [[04 - uv — o gerenciador moderno|04 — uv: o gerenciador moderno]]
5. [[05 - Poetry — a alternativa madura|05 — Poetry: a alternativa madura]]
6. [[06 - uv vs Poetry — trade-offs honestos|06 — uv vs Poetry: trade-offs honestos]]
7. [[07 - ruff e black — linting e formatação automática|07 — ruff e black: linting e formatação automática]]
8. [[08 - Capstone — tooling consistente nos dois serviços|08 — Capstone: tooling consistente nos dois serviços]] — recapitula o galho.

## Veja também

- [[03-Dominios/Tecnologia/Python/index|Trilha Python]] (MOC central)
- [[03-Dominios/Tecnologia/Python/Segurança/07 - Segurança de dependências e supply chain|Segurança de dependências]] — Galho 11 nota 07 (lockfiles pela lente de segurança)
- [[03-Dominios/Tecnologia/Java/Build e tooling/index|Java — Build e tooling]] — trilha irmã, mesmo papel (Maven/Gradle)
- [[03-Dominios/Tecnologia/Python/Microservices e sistemas distribuídos/index|Microservices e sistemas distribuídos]] — Galho 15 (os dois serviços que este galho organiza)
