---
title: "Roadmap — Performance de Runtime & Rendering"
created: 2026-07-06
type: meta
publish: false
tags:
  - meta
  - roadmap
---

# Roadmap — Performance de Runtime & Rendering

Roadmap do galho `03-Dominios/Tecnologia/Web Performance/Performance de Runtime e Rendering`. Galho **em construção**: eixo primário = **escrita** (8 notas); enriquecimento (M1 mídia) secundário. Roster derivado do [[00-Meta/specs/2026-07-05-dominio-web-performance-design|design 2026-07-05]] (escopo do Galho 3) + `index.md`.

## Régua de análise

- **Escrita:** ⬜ não escrita · 🔄 rascunho · ✅ escrita + verificada + commitada (YYYY-MM-DD).
- **Enriquecimento:** ⬜ pendente · ➖ n/a · ✅ enriquecida (gap esperado = M1 mídia).

**Esquema de `fase:`:** COM fase (Iniciado/Adepto/Magus; piso guiado pelo padrão capítulo).

## Tabela-resumo

| Métrica | Valor |
|---------|-------|
| Total de notas | 8 |
| ⬜ não escritas | 0 |
| ✅ escritas | 8 |
| % escrito | 100% |

---

## Notas

#### 01 - A thread principal e o event loop   [substantivo]
- **Fase:** Iniciado · **Escrita:** ✅ (2026-07-06) · **Enriquecimento:** ⬜ (M1)
- **Escopo:** single-thread, task queue, o que compete (JS, layout, paint); por que travar a thread trava a interação. Liga a [[03-Dominios/Tecnologia/Plataforma Web/Eventos/index|Eventos]]/event loop do JS.

#### 02 - Long tasks e o custo do JavaScript   [substantivo]
- **Fase:** Iniciado · **Escrita:** ✅ (2026-07-06) · **Enriquecimento:** ⬜ (M1)
- **Escopo:** tasks > 50 ms, parse/compile/execute, o que gera long tasks; Long Tasks API, TBT (liga [[03-Dominios/Tecnologia/Web Performance/Medição e Core Web Vitals/07 - Métricas de apoio|G1 nota 07]]).

#### 03 - INP a fundo   [substantivo]
- **Fase:** Iniciado · **Escrita:** ✅ (2026-07-06) · **Enriquecimento:** ⬜ (M1)
- **Escopo:** as 3 fases do INP (input delay, processing, presentation delay); yield to main thread, `scheduler.yield`, `isInputPending`, `postTask`. Aprofunda [[03-Dominios/Tecnologia/Web Performance/Medição e Core Web Vitals/02 - Os três Core Web Vitals|G1 nota 02]].

#### 04 - Reflow, repaint e o custo do layout   [substantivo]
- **Fase:** Adepto · **Escrita:** ✅ (2026-07-06) · **Enriquecimento:** ⬜ (M1)
- **Escopo:** pipeline layout→paint→composite; quando recalcula; propriedades caras. Liga a [[03-Dominios/Tecnologia/Plataforma Web/Rendering Pipeline/index|Rendering Pipeline]].

#### 05 - Layout thrashing   [substantivo]
- **Fase:** Adepto · **Escrita:** ✅ (2026-07-06) · **Enriquecimento:** ⬜ (M1)
- **Escopo:** ler/escrever DOM em loop forçando reflow síncrono; forced synchronous layout; batching (read-then-write), `requestAnimationFrame`. Código com falha + solução.

#### 06 - Compositing e animações na GPU   [substantivo]
- **Fase:** Adepto · **Escrita:** ✅ (2026-07-06) · **Enriquecimento:** ⬜ (M1)
- **Escopo:** camadas de composição, `transform`/`opacity` (compostas) vs `top`/`left`/`width` (reflow), `will-change`, custo de camadas. Liga [[03-Dominios/Tecnologia/CSS/12 - Performance CSS|CSS 12]].

#### 07 - CLS em runtime   [substantivo]
- **Fase:** Adepto · **Escrita:** ✅ (2026-07-06) · **Enriquecimento:** ⬜ (M1)
- **Escopo:** deslocamentos APÓS o carregamento — conteúdo injetado, ads, banners, expand/collapse; `min-height`, transform em vez de layout; bfcache. Fronteira: dimensões de imagem/fonte = G2.

#### 08 - Offload, Web Workers e o custo da hidratação   [substantivo]
- **Fase:** Magus · **Escrita:** ✅ (2026-07-06) · **Enriquecimento:** ⬜ (M1)
- **Escopo:** mover trabalho pra fora da main thread (Web Workers); custo de JS de framework, hidratação, islands/RSC, code-splitting no runtime. Capstone; ponte pro Galho 4. Liga [[03-Dominios/Tecnologia/React/React core/17 - Performance no React|React 17]], [[03-Dominios/Tecnologia/Plataforma Web/Workers/index|Workers]].

---

## Fronteiras (o que NÃO duplicar)

- **Carregamento/LCP/critical path** → Galho 2. Aqui, o que acontece DEPOIS que a página carregou.
- **Dimensões de imagem/fonte (CLS de carregamento)** → Galho 2 nota 04/05. Aqui, CLS disparado por interação/runtime.
- **Event loop / microtasks (fundamento da linguagem)** → [[03-Dominios/Tecnologia/JavaScript/index|JavaScript]] e [[03-Dominios/Tecnologia/Plataforma Web/Eventos/index|Plataforma Web/Eventos]]; aqui, a ótica de performance.
- **Rendering pipeline interno** → [[03-Dominios/Tecnologia/Plataforma Web/Rendering Pipeline/index|Rendering Pipeline]]; aqui, o custo em runtime.
- Notas existentes (React 17, CSS 12, Rendering Pipeline, Workers, Eventos) = **linkadas como reforço**.

## Próximos passos

1. Semear 01→08 via `escrever-nota`, fechando cada uma com `verificar-nota`.
2. Ao completar, subir o estado no roadmap do domínio e no [[00-Meta/Roadmap]].
3. Rodada de enriquecimento (M1).
