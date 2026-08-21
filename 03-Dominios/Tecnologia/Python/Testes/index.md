---
title: "Python — Testes"
created: 2026-07-11
type: moc
status: growing
publish: true
tags:
  - python
  - moc
aliases:
  - "Galho 12 - Testes"
---

# Testes

> [!abstract] TL;DR
> Galho 12 da trilha Python: o ferramental `pytest` aplicado à API construída nos Galhos 10-11 — anatomia de um teste e discovery, fixtures e escopos, parametrização e organização de suíte, mocking com `unittest.mock`, testando a API REST (`TestClient`), testando a camada de persistência, coverage, TDD na prática, fechando com a suíte completa de testes (unit + integração + segurança) pra API de Tarefas blindada no Galho 11. Fase Adepto; 9 notas. Quarto galho do bloco "Backend e arquitetura" (9-13).

## Sobre este galho

Este galho é **ferramental**, não teoria — a estratégia de testes (pirâmide, quando usar cada tipo de teste, test doubles como conceito, flaky tests, mutation testing) já está coberta de forma stack-agnóstica em [[03-Dominios/Engenharia/Testes/index|Engenharia/Testes]], que este galho referencia sem repetir. Aqui o assunto é `pytest` na prática: como escrever, organizar, parametrizar e rodar testes de uma API Python real, testando exatamente o código construído nos Galhos 9 (persistência), 10 (API REST) e 11 (segurança) desta mesma trilha.

**Fronteiras anti-duplicação:** a pirâmide de testes e a filosofia de test doubles (dummy/stub/spy/mock/fake) → [[03-Dominios/Engenharia/Testes/index|Engenharia/Testes]], só referenciado. Mutation testing como conceito (coverage não é qualidade) → também Engenharia/Testes, aqui só aplicado com `pytest-cov`. A API sendo testada (roteamento, Pydantic, `Depends`, DRF, erros) → Galho 10, não reexplicada. A camada de persistência sendo testada (SQLAlchemy, Session, transações) → Galho 9, não reexplicada. A autenticação/hardening sendo testado (Broken Access Control, rate limiting) → Galho 11, não reexplicado.

**Audiência:** quem já construiu a API dos Galhos 9-11 e precisa de uma suíte de testes que dê confiança real pra fazer deploy — não um tutorial de sintaxe de `assert`.

## Adepto

1. [[01 - pytest fundamentos — anatomia, discovery e assert introspection|01 — pytest fundamentos: anatomia, discovery e assert introspection]]
2. [[02 - Fixtures — escopos, yield e conftest.py|02 — Fixtures: escopos, yield e conftest.py]]
3. [[03 - Parametrização e organização de suíte|03 — Parametrização e organização de suíte]]
4. [[04 - Mocking com unittest.mock e pytest-mock|04 — Mocking com unittest.mock e pytest-mock]]
5. [[05 - Testando a API REST — TestClient e dependency overrides|05 — Testando a API REST: TestClient e dependency overrides]]
6. [[06 - Testando a camada de persistência — banco de teste e rollback|06 — Testando a camada de persistência: banco de teste e rollback]]
7. [[07 - Coverage — pytest-cov e o que ele não mede|07 — Coverage: pytest-cov e o que ele não mede]]
8. [[08 - TDD na prática com pytest|08 — TDD na prática com pytest]]
9. [[09 - Capstone — a suíte de testes da API de Tarefas|09 — Capstone: a suíte de testes da API de Tarefas]] — recapitula o galho.

## Veja também

- [[03-Dominios/Tecnologia/Python/index|Trilha Python]] (MOC central)
- [[03-Dominios/Engenharia/Testes/index|Testes (Engenharia)]] — teoria e estratégia stack-agnóstica: pirâmide, TDD, test doubles, mutation testing
- [[03-Dominios/Tecnologia/Python/Web e APIs REST/index|Web e APIs REST]] — Galho 10 (a API que este galho testa)
- [[03-Dominios/Tecnologia/Python/Segurança/index|Segurança]] — Galho 11 (o hardening que este galho valida com testes)
- [[03-Dominios/Tecnologia/Java/Testes/index|Java — Testes]] — trilha irmã, mesmo papel (JUnit 5/Mockito/Testcontainers)
