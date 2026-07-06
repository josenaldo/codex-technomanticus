---
title: "Testes JS — índice"
created: 2026-07-06
updated: 2026-07-06
type: index
tags:
  - testes
  - javascript
  - vitest
  - playwright
publish: true
aliases:
  - Testes em JavaScript
  - Testes JS
  - Testing JavaScript
---

# Testes no ecossistema JS

Galho de Tecnologia sobre o **ferramental de testes JavaScript/TypeScript** — o "como fazer" concreto que instrumenta a teoria de [[03-Dominios/Engenharia/Testes/index|Engenharia/Testes]]. Cobre o stack moderno de 2026: **Vitest** (unit), **Testing Library** (componentes React), **MSW** (mock de rede), **Playwright** (E2E), mais cobertura, flaky e CI.

> [!abstract] TL;DR
> A teoria de testes é stack-agnóstica (pirâmide, doubles, TDD — tudo em [[03-Dominios/Engenharia/Testes/index|Engenharia/Testes]]); este galho é o **ferramental JS**. Em 2026 o stack padrão é **Vitest** para unit (2–4× mais rápido que o Jest, default para novos projetos), **Testing Library** para componentes, **MSW v2** para mockar a rede e **Playwright** para E2E. Aqui você aprende a config, a API e as armadilhas de cada um — sempre linkando de volta à teoria, nunca a reescrevendo.

## Fronteiras (linka, não duplica)

- **Teoria e estratégia** (pirâmide, test doubles, TDD, design de caso, flaky/coverage conceituais) → [[03-Dominios/Engenharia/Testes/index|Engenharia/Testes]].
- **Ferramental Java** (JUnit 5, Mockito, Testcontainers) → [[03-Dominios/Tecnologia/Java/Testes/index|Java/Testes]] — o galho-paralelo.
- **`node:test` e o cenário de test runners** → [[03-Dominios/Tecnologia/Tooling e Build/19 - Test runner nativo (node-test) e o cenário de testes|Tooling 19]].
- **React em si** → [[03-Dominios/Tecnologia/React/index|React]]; aqui, como **testá-lo**.

---

## Fase Iniciado — o terreno e o teste unitário

1. [[03-Dominios/Tecnologia/Testes JS/01 - O cenário de testes JS|01 — O cenário de testes JS]] — Vitest vs Jest e o ecossistema
2. [[03-Dominios/Tecnologia/Testes JS/02 - Vitest - setup e o primeiro teste|02 — Vitest: setup e o primeiro teste]] — config, `test`/`describe`, `expect`
3. [[03-Dominios/Tecnologia/Testes JS/03 - Matchers e asserções|03 — Matchers e asserções]] — a API do `expect`
4. [[03-Dominios/Tecnologia/Testes JS/04 - Organização e ciclo de vida|04 — Organização e ciclo de vida]] — `describe`, hooks, `test.each`
5. [[03-Dominios/Tecnologia/Testes JS/05 - Testando código assíncrono|05 — Testando código assíncrono]] — `resolves`/`rejects`, fake timers

## Fase Adepto — doubles, componentes, rede

6. [[03-Dominios/Tecnologia/Testes JS/06 - Mocking com Vitest|06 — Mocking com Vitest]] — `vi.fn`, `vi.spyOn`, `vi.mock`
7. [[03-Dominios/Tecnologia/Testes JS/07 - Testing Library - filosofia e queries|07 — Testing Library: filosofia e queries]] — queries user-centric
8. [[03-Dominios/Tecnologia/Testes JS/08 - Testando componentes React|08 — Testando componentes React]] — `render`, `screen`, `user-event`
9. [[03-Dominios/Tecnologia/Testes JS/09 - MSW - mockando a rede|09 — MSW: mockando a rede]] — handlers, `http`/`graphql`, v2
10. [[03-Dominios/Tecnologia/Testes JS/10 - Testando hooks e estado|10 — Testando hooks e estado]] — `renderHook`, `act`, providers
11. [[03-Dominios/Tecnologia/Testes JS/11 - Snapshot testing|11 — Snapshot testing]] — `toMatchSnapshot`, quando usar
12. [[03-Dominios/Tecnologia/Testes JS/12 - Cobertura no ecossistema JS|12 — Cobertura no ecossistema JS]] — v8 vs istanbul, thresholds

## Fase Magus — E2E, qualidade, CI, estratégia

13. [[03-Dominios/Tecnologia/Testes JS/13 - Playwright - E2E|13 — Playwright: E2E]] — locators, auto-wait, fixtures, trace
14. [[03-Dominios/Tecnologia/Testes JS/14 - Playwright além do básico|14 — Playwright além do básico]] — component testing, auth, visual
15. [[03-Dominios/Tecnologia/Testes JS/15 - Playwright vs Cypress|15 — Playwright vs Cypress]] — o cenário E2E
16. [[03-Dominios/Tecnologia/Testes JS/16 - Testes flaky em JS|16 — Testes flaky em JS]] — auto-wait, retries, isolamento
17. [[03-Dominios/Tecnologia/Testes JS/17 - Testes na CI|17 — Testes na CI]] — matriz, sharding, cache, reporters
18. [[03-Dominios/Tecnologia/Testes JS/18 - Capstone - estratégia de testes de um app JS-TS production-grade|18 — Capstone: estratégia de testes de um app JS/TS]] — junta tudo. **Capstone**

---

## Veja também

- [[03-Dominios/Engenharia/Testes/index|Engenharia/Testes]] — a teoria que este galho instrumenta.
- [[00-Meta/specs/2026-07-06-galho-testes-js-design|Design do galho]] — decisões e roster.
