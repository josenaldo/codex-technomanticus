---
title: "Galho Testes JS (ferramental) — design"
created: 2026-07-06
type: design
status: draft
publish: false
tags:
  - meta
  - design
  - testes
  - javascript
---

# Galho Testes JS (ferramental) — design

## Contexto

O Roadmap mestre ([[00-Meta/Roadmap]], Onda B item 7) pede **"Testes no ecossistema JS"** —
Vitest, Jest, Testing Library, Playwright, MSW — como trilha específica, ligando a
`Engenharia/Testes` (conceitual) e à nota 19 de Tooling (`node:test`).

O vault já tem os dois vizinhos que definem a fronteira:

- **`Engenharia/Testes`** (16 notas) = **teoria e estratégia** stack-agnóstica: pirâmide,
  test doubles (taxonomia de Meszaros), TDD, design de caso, flaky, coverage, CI — tudo
  conceitual. Seu `index` já aponta explicitamente para um **`[[Testes em JavaScript]]`**
  que **não existe ainda**. Este galho preenche esse ponteiro.
- **`Tecnologia/Java/Testes`** (21 notas) = o **ferramental Java** concreto (JUnit 5, AssertJ,
  Mockito, Testcontainers, etc.). É o **precedente estrutural** exato: um galho de ferramental
  de stack, espelhando a teoria da Engenharia.

**Princípio-guia:** este galho é o **ferramental JS/TS concreto**. Ele **não reescreve** a
teoria — linka `Engenharia/Testes` para pirâmide/doubles/TDD/flaky-conceito e ensina *como fazer
com as ferramentas*. Redundância entre notas = reforço; nunca deduplicar (ver
[[feedback_redundancia_entre_notas]]).

## Decisões de design

1. **Forma:** **galho** (não domínio multi-galho como Web Performance). Justificativa: o
   Roadmap chama de "galho/trilha específica" (singular); o `Engenharia/Testes` o referencia
   como link único `[[Testes em JavaScript]]`; o equivalente Java (`Java/Testes`) é um galho.
   Consistência > sobre-estruturar.
2. **Local:** `03-Dominios/Tecnologia/Testes JS/`. Não dentro de `JavaScript/` (as ferramentas
   servem React, Node e TS, não só a linguagem) nem de `React/` (Playwright/MSW são mais amplos).
   Um galho top-level em Tecnologia é o home honesto do toolchain JS de testes.
3. **Tamanho:** ~18 notas em 3 fases, no molde de profundidade do `Java/Testes` (21).
4. **Ritmo:** ponta a ponta (é um galho só). Semear as 18 notas na ordem, fechando cada uma
   com `verificar-nota`. Enriquecimento de mídia (M1) fica para passada futura.
5. **Convenções do vault:** notas atômicas em 3 fases (Iniciado/Adepto/Magus) com `fase:`;
   padrão capítulo de livro; Mermaid; fontes com URL; seção "Em entrevista"/inglês (é
   interview-critical, como o resto de Testes); `roadmap.md` do galho.

## Fronteiras (o que NÃO duplicar)

- **Teoria** (pirâmide, doubles, TDD, design de caso, coverage-conceito, flaky-conceito) →
  `Engenharia/Testes`. Aqui, só o **como fazer com a ferramenta**.
- **Ferramental Java** → `Java/Testes` (paralelo, não sobreposto).
- **`node:test` e o cenário de test runners** → [[03-Dominios/Tecnologia/Tooling e Build/19 - Test runner nativo (node-test) e o cenário de testes|Tooling 19]]; aqui, o uso prático de Vitest/Jest.
- **React em si** (hooks, componentes) → `React/`; aqui, como **testá-los**.

## Roster (18 notas, 3 fases)

**Iniciado — o terreno e o teste unitário**
1. `01 - O cenário de testes JS` — Vitest vs Jest, o ecossistema 2026, quando cada um; mapa do galho. (links Tooling 19, Engenharia/Testes)
2. `02 - Vitest - setup e o primeiro teste` — config Vite-native, `test`/`it`/`describe`, `expect`, watch.
3. `03 - Matchers e asserções` — `toBe`/`toEqual`/`toMatchObject`/`toThrow`, matchers assimétricos, `expect` API.
4. `04 - Organização e ciclo de vida` — `describe`, hooks (`beforeEach`/`afterEach`), `test.each`, `.skip`/`.only`/`.todo`.
5. `05 - Testando código assíncrono` — `async`/`await`, `resolves`/`rejects`, fake timers (`vi.useFakeTimers`).

**Adepto — doubles, componentes, rede**
6. `06 - Mocking com Vitest` — `vi.fn`, `vi.spyOn`, `vi.mock`, module/partial mocks. (liga Engenharia/Testes 05)
7. `07 - Testing Library - filosofia e queries` — user-centric, `getBy`/`queryBy`/`findBy`, roles, prioridade.
8. `08 - Testando componentes React` — `render`, `screen`, `user-event`, `findBy` async, cleanup.
9. `09 - MSW - mockando a rede` — handlers, `http`/`graphql`, setup node vs browser, API v2. (liga Engenharia/Testes 05/07)
10. `10 - Testando hooks e estado` — `renderHook`, `act`, wrappers de context/provider.
11. `11 - Snapshot testing` — `toMatchSnapshot`/inline, quando usar e quando evita. (liga Engenharia/Testes 13)
12. `12 - Cobertura no ecossistema JS` — v8 vs istanbul, `--coverage`, thresholds. (liga Engenharia/Testes 12)

**Magus — E2E, qualidade, CI, estratégia**
13. `13 - Playwright - E2E` — locators, auto-wait, fixtures, projects, trace viewer.
14. `14 - Playwright além do básico` — component testing em browser real, network, storageState/auth, visual.
15. `15 - Playwright vs Cypress` — o cenário E2E, trade-offs, por que Playwright dominou.
16. `16 - Testes flaky em JS` — auto-wait, retries, isolamento, `test.step`. (liga Engenharia/Testes 11)
17. `17 - Testes na CI` — matriz, sharding, cache, reporters, Playwright na CI. (liga Engenharia/Testes 15)
18. `18 - Capstone - estratégia de testes de um app JS/TS production-grade` — junta unit+component+integração(MSW)+E2E; espelha Engenharia/Testes 16 e Java/Testes 21.

## Caducidade a vigiar

- **Vitest** é default para novos projetos desde 2025; **Jest 30** é legacy mas ainda ~metade dos testes no npm (mantido pela Meta). Cravar essa foto e a data.
- **MSW v2** (2.14.x em 2026) mudou a API vs v1 (`http`/`HttpResponse`). Cravar v2.
- **Playwright** ~1.4x; component testing em browser real ainda experimental. **Cypress** em declínio.
- Testing Library é framework-agnóstica e idêntica em Vitest/Jest.

## Escopo desta entrega

Criar a pasta + `index.md` + `roadmap.md` do galho e **semear as 18 notas**. Atualizar o
ponteiro `[[Testes em JavaScript]]` no `Engenharia/Testes/index` para resolver a este galho.
Enriquecimento de mídia (M1) = passada futura.

## Veja também

- [[00-Meta/Roadmap|Roadmap de Trilhas]] — Onda B item 7.
- [[03-Dominios/Engenharia/Testes/index|Engenharia/Testes]] — a teoria que este galho instrumenta.
- [[03-Dominios/Tecnologia/Java/Testes/index|Java/Testes]] — o precedente estrutural.
- Skills: `escrever-nota`, `verificar-nota`, `diagnosticar-galho`, `enriquecer-galho`.
