---
title: "Roadmap — Testes JS"
created: 2026-07-06
type: meta
publish: false
tags:
  - meta
  - roadmap
---

# Roadmap — Testes JS

Roadmap do galho `03-Dominios/Tecnologia/Testes JS`. Galho **em construção**: eixo primário = **escrita** (18 notas); enriquecimento (M1 mídia) secundário. Roster derivado do [[00-Meta/specs/2026-07-06-galho-testes-js-design|design 2026-07-06]] + `index.md`.

## Régua de análise

- **Escrita:** ⬜ não escrita · 🔄 rascunho · ✅ escrita + verificada + commitada (YYYY-MM-DD).
- **Enriquecimento:** ⬜ pendente · ➖ n/a · ✅ enriquecida (gap esperado = M1 mídia).

**Esquema de `fase:`:** COM fase (Iniciado/Adepto/Magus; piso guiado pelo padrão capítulo).

## Tabela-resumo

| Métrica | Valor |
|---------|-------|
| Total de notas | 18 |
| ⬜ não escritas | 14 |
| ✅ escritas | 4 |
| % escrito | 22,2% |

---

## Notas

#### 01 - O cenário de testes JS   [substantivo]
- **Fase:** Iniciado · **Escrita:** ✅ (2026-07-06) · **Enriquecimento:** ⬜ (M1)
- **Escopo:** Vitest vs Jest, ecossistema 2026, quando cada um; mapa do galho. Liga [[03-Dominios/Tecnologia/Tooling e Build/19 - Test runner nativo (node-test) e o cenário de testes|Tooling 19]] e [[03-Dominios/Engenharia/Testes/index|Engenharia/Testes]].

#### 02 - Vitest - setup e o primeiro teste   [substantivo]
- **Fase:** Iniciado · **Escrita:** ✅ (2026-07-06) · **Enriquecimento:** ⬜ (M1)
- **Escopo:** config Vite-native, `test`/`it`/`describe`, `expect`, modo watch, `vitest.config`.

#### 03 - Matchers e asserções   [substantivo]
- **Fase:** Iniciado · **Escrita:** ✅ (2026-07-06) · **Enriquecimento:** ⬜ (M1)
- **Escopo:** `toBe`/`toEqual`/`toStrictEqual`/`toMatchObject`/`toThrow`, matchers assimétricos, `expect` API.

#### 04 - Organização e ciclo de vida   [substantivo]
- **Fase:** Iniciado · **Escrita:** ✅ (2026-07-06) · **Enriquecimento:** ⬜ (M1)
- **Escopo:** `describe`, hooks (`beforeEach`/`afterEach`/`beforeAll`), `test.each`, `.skip`/`.only`/`.todo`, isolamento.

#### 05 - Testando código assíncrono   [substantivo]
- **Fase:** Iniciado · **Escrita:** ⬜ · **Enriquecimento:** ➖
- **Escopo:** `async`/`await`, `resolves`/`rejects`, `expect.assertions`, fake timers (`vi.useFakeTimers`/`advanceTimersByTime`).

#### 06 - Mocking com Vitest   [substantivo]
- **Fase:** Adepto · **Escrita:** ⬜ · **Enriquecimento:** ➖
- **Escopo:** `vi.fn`, `vi.spyOn`, `vi.mock` (module/partial), `mockReturnValue`/`mockResolvedValue`, `vi.hoisted`, reset. Liga [[03-Dominios/Engenharia/Testes/05 - Test doubles - dummy, stub, spy, mock, fake|Engenharia/Testes 05]].

#### 07 - Testing Library - filosofia e queries   [substantivo]
- **Fase:** Adepto · **Escrita:** ⬜ · **Enriquecimento:** ➖
- **Escopo:** "teste como o usuário usa", `getBy`/`queryBy`/`findBy`, `*AllBy`, prioridade de queries (role > label > text), `screen`.

#### 08 - Testando componentes React   [substantivo]
- **Fase:** Adepto · **Escrita:** ⬜ · **Enriquecimento:** ➖
- **Escopo:** `render`, `screen`, `@testing-library/user-event`, `findBy` async, `cleanup`, o que testar num componente. Liga [[03-Dominios/Tecnologia/React/React core/index|React core]].

#### 09 - MSW - mockando a rede   [substantivo]
- **Fase:** Adepto · **Escrita:** ⬜ · **Enriquecimento:** ➖
- **Escopo:** MSW v2 (`http`/`HttpResponse`/`graphql`), `setupServer` (node) vs `setupWorker` (browser), reuso entre Vitest/Playwright/Storybook. Liga Engenharia/Testes 05/07.

#### 10 - Testando hooks e estado   [substantivo]
- **Fase:** Adepto · **Escrita:** ⬜ · **Enriquecimento:** ➖
- **Escopo:** `renderHook`, `act`, `wrapper` de context/provider, testar custom hooks e estado assíncrono.

#### 11 - Snapshot testing   [substantivo]
- **Fase:** Adepto · **Escrita:** ⬜ · **Enriquecimento:** ➖
- **Escopo:** `toMatchSnapshot`/`toMatchInlineSnapshot`, atualização, quando usa e quando evita (snapshots frágeis). Liga [[03-Dominios/Engenharia/Testes/13 - Além do básico - property-based, snapshot, contract, smoke|Engenharia/Testes 13]].

#### 12 - Cobertura no ecossistema JS   [substantivo]
- **Fase:** Adepto · **Escrita:** ⬜ · **Enriquecimento:** ➖
- **Escopo:** `--coverage`, provider v8 vs istanbul, thresholds, o que coverage NÃO diz. Liga [[03-Dominios/Engenharia/Testes/12 - Coverage e mutation testing|Engenharia/Testes 12]].

#### 13 - Playwright - E2E   [substantivo]
- **Fase:** Magus · **Escrita:** ⬜ · **Enriquecimento:** ➖
- **Escopo:** locators, auto-wait, `expect` web-first, fixtures, `projects` (browsers), trace viewer, codegen.

#### 14 - Playwright além do básico   [substantivo]
- **Fase:** Magus · **Escrita:** ⬜ · **Enriquecimento:** ➖
- **Escopo:** component testing em browser real (experimental), interceptar rede, `storageState`/auth, visual/screenshot testing.

#### 15 - Playwright vs Cypress   [substantivo]
- **Fase:** Magus · **Escrita:** ⬜ · **Enriquecimento:** ➖
- **Escopo:** o cenário E2E, arquitetura (multi-browser/processo vs in-browser), trade-offs, por que Playwright dominou; quando Cypress ainda cabe.

#### 16 - Testes flaky em JS   [substantivo]
- **Fase:** Magus · **Escrita:** ⬜ · **Enriquecimento:** ➖
- **Escopo:** causas em JS (waits arbitrários, ordem, timers, rede), auto-wait, retries, isolamento, `test.step`, quarentena. Liga [[03-Dominios/Engenharia/Testes/11 - Testes flaky|Engenharia/Testes 11]].

#### 17 - Testes na CI   [substantivo]
- **Fase:** Magus · **Escrita:** ⬜ · **Enriquecimento:** ➖
- **Escopo:** matriz de browsers/node, sharding, cache de deps/browsers, reporters, Playwright na CI, artefatos (trace/screenshots). Liga [[03-Dominios/Engenharia/Testes/15 - Testes em CI-CD|Engenharia/Testes 15]].

#### 18 - Capstone - estratégia de testes de um app JS-TS production-grade   [substantivo]
- **Fase:** Magus · **Escrita:** ⬜ · **Enriquecimento:** ➖
- **Escopo:** juntar unit (Vitest) + componente (Testing Library) + integração (MSW) + E2E (Playwright) numa estratégia coerente; troféu de testes; espelha [[03-Dominios/Engenharia/Testes/16 - Estratégia de testes em entrevista|Engenharia/Testes 16]] e Java/Testes 21. Capstone.

---

## Fronteiras (o que NÃO duplicar)

- **Teoria** (pirâmide/doubles/TDD/design de caso/coverage-conceito/flaky-conceito) → [[03-Dominios/Engenharia/Testes/index|Engenharia/Testes]]; aqui só o **como fazer com a ferramenta**.
- **Ferramental Java** → [[03-Dominios/Tecnologia/Java/Testes/index|Java/Testes]] (paralelo).
- **`node:test`/cenário de runners** → [[03-Dominios/Tecnologia/Tooling e Build/19 - Test runner nativo (node-test) e o cenário de testes|Tooling 19]].
- **React em si** → [[03-Dominios/Tecnologia/React/index|React]].

## Próximos passos

1. Semear 01→18 via `escrever-nota`, fechando cada uma com `verificar-nota`.
2. Atualizar o ponteiro `[[Testes em JavaScript]]` no `Engenharia/Testes/index` para resolver a este galho.
3. Ao completar, marcar no [[00-Meta/Roadmap]] (Onda B item 7 → feito) e rodar enriquecimento (M1).
