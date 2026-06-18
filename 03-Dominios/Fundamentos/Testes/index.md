---
title: "Testes"
created: 2026-06-18
updated: 2026-06-18
type: moc
status: growing
publish: true
tags:
  - fundamentos
  - testes
  - qualidade
  - entrevista
  - moc
aliases:
  - Testes
  - Testes de Software
  - Testes Automatizados
  - Testing
  - Galho - Testes
---

# Testes

> [!abstract] TL;DR
> Galho de Fundamentos sobre como verificar que o software funciona — e **continua** funcionando após
> mudanças. Escrever um teste é fácil; **desenhar uma estratégia de testes** que equilibra confiança,
> velocidade e custo de manutenção é o que diferencia um senior. Cobre a pirâmide, os tipos de teste,
> test doubles, TDD, técnicas de design de caso, flaky tests, coverage e CI/CD — tudo **stack-agnóstico**,
> linkando Java e JavaScript para o ferramental. Interview-critical.

## Sobre este galho

Este galho é a **teoria e estratégia** de testes: o que testar, qual tipo de teste, e por quê. O ferramental
concreto vive nos galhos de stack — aqui ele entra só como ponteiro.

**Fronteiras (linka, não duplica):**
- **Ferramental Java** (JUnit 5, AssertJ, Mockito, Testcontainers, Spring Boot Test, JQwik, PITest, JMH) →
  [[Testes em Java]] e o galho [[03-Dominios/Java/Testes/index|Java · Testes]].
- **Ferramental JavaScript/TS** (Vitest, Jest, Testing Library, MSW, Playwright, fast-check) →
  [[Testes em JavaScript]].
- **Testes como rede de segurança contra entropia** → [[03-Dominios/Fundamentos/Complexidade de Software/14 - Manutenção e evolução|Manutenção e evolução]].
- **Código testável é código bem desenhado** (DI, DIP) → [[03-Dominios/Fundamentos/SOLID/index|SOLID]] · [[03-Dominios/Fundamentos/Orientação a Objetos/index|OO]].
- **Design testável** (hexagonal, ports & adapters) → [[Arquitetura de Software]].

**Audiência:** dev senior em preparação para entrevista internacional. Cada nota tem seção "Em entrevista"
com frases prontas em inglês e vocabulário técnico PT→EN.

## Iniciado — o que, por que e o básico de um bom teste

1. [[01 - O que são testes e por que testar]] — função estratégica, spec executável, as duas faces em entrevista.
2. [[02 - A pirâmide de testes e suas variações]] — unit/integração/E2E, pirâmide × troféu × ampulheta, qual teste pra qual bug.
3. [[03 - Anatomia de um bom teste]] — AAA / Given-When-Then, naming, um teste = uma razão, F.I.R.S.T.
4. [[04 - Testes unitários]] — unidade, isolamento, determinismo, fixtures/factories/object mothers.

## Adepto — doubles, integração, TDD, design de caso

5. [[05 - Test doubles - dummy, stub, spy, mock, fake]] — a taxonomia de Meszaros, mock × stub, estado × interação.
6. [[06 - Testar comportamento, não implementação]] — state-based × interaction-based, over-mocking, fakes subestimados.
7. [[07 - Testes de integração]] — colaboração real, Testcontainers, o drift do ambiente.
8. [[08 - TDD - o ciclo Red-Green-Refactor]] — red → green → refactor; o que TDD força.
9. [[09 - TDD na prática]] — quando brilha × quando atrapalha; posição pragmática (test-after).
10. [[10 - Técnicas de teste e edge cases]] — equivalence partitioning, boundary value analysis, decision tables, o checklist de edge cases.
11. [[11 - Testes flaky]] — causas, mitigações, quarentena, "nunca `sleep` em teste".

## Magus — coverage, estratégias avançadas, esteira, entrevista

12. [[12 - Coverage e mutation testing]] — line/branch, 100% ≠ testado, mutation testing como complemento honesto.
13. [[13 - Além do básico - property-based, snapshot, contract, smoke]] — a long tail de tipos e quando cada um vale.
14. [[14 - Performance, carga, caos e segurança]] — microbenchmark × load × stress × chaos; SAST/DAST/deps.
15. [[15 - Testes em CI-CD]] — a esteira, paralelização, fail-fast, quarentena; rapidez como requisito.
16. [[16 - Estratégia de testes em entrevista]] — desenhar a estratégia, edge cases, inglês, vocabulário, armadilhas.

## Rotas alternativas

### Entrevista internacional
01 → 02 → 05 → 06 → 08 → 09 → 16. O porquê, a pirâmide, doubles, comportamento×implementação, TDD e o capstone.

### Fundamento sólido de unidade
01 → 03 → 04 → 05 → 06. O que é, anatomia, unitários, doubles e a filosofia de testar comportamento.

### Confiança e qualidade da suíte
10 → 11 → 12 → 13. Técnicas de caso, flaky, coverage/mutation e as estratégias avançadas.

## Todas as notas

```dataview
TABLE fase, status, updated
FROM "03-Dominios/Fundamentos/Testes"
WHERE type = "concept"
SORT file.name ASC
```

## Veja também

- [[03-Dominios/Fundamentos/index|Fundamentos (MOC do domínio)]]
- [[Testes em Java]] — o ferramental Java (JUnit, Mockito, Testcontainers)
- [[Testes em JavaScript]] — o ferramental JS/TS (Vitest, Testing Library, Playwright)
- [[Arquitetura de Software]] — design testável (hexagonal, ports & adapters)
- [[Dicionário de Fundamentos]]
