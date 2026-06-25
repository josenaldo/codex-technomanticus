---
title: "Plano de Implementação — Galho React core"
type: spec
created: 2026-06-25
updated: 2026-06-25
status: draft
tags:
  - spec
  - plano
  - react
aliases:
  - Implementação React core
---

# Plano de Implementação — Galho React core

> **Para executores:** implementa o spec [[00-Meta/specs/2026-06-25-trilha-react-core-plan|Plano — Trilha React core]]. Execução **subagente-por-nota**, em ondas por fase, gate de qualidade entre fases. Passos com checkbox (`- [ ]`).

**Objetivo:** escrever o galho **React core** (26 notas, 3 fases, TS-first) em `03-Dominios/Tecnologia/React/React core/`, e ao fim tornar `React/` um domínio multi-galho.

**Abordagem:** cada nota é escrita por um subagente via `/escrever-nota` (núcleo capítulo + Feynman), pesquisando React 19-era (2026) via WebSearch. Exemplos em `.tsx`. Commit por sub-lote; gate `/verificar-nota` por nota; `/verificar-wikilinks` por fase.

**Stack/convenções:** Obsidian + Quartz; React 19 + TypeScript; padrão capítulo; fases Iniciado/Adepto/Magus; PT-BR + "Como explicar em inglês".

## Global Constraints (valem para TODA nota)

- **Escrita do ZERO com pesquisa** — `React.md` é referência de tópicos, NÃO migração. Pesquisar estado 2026 (React 19.x) via WebSearch; fontes em `## Referências`.
- **TS-first** — todos os exemplos em `.tsx` com tipos idiomáticos (props tipadas, `useState<T>`, handlers `React.ChangeEvent<…>`). Tipagem básica inline; tipagem difícil → linkar [[03-Dominios/Tecnologia/React/TypeScript com React/index|TypeScript com React]].
- **Padrão capítulo** — problema-primeiro; registro Feynman; exemplos trabalhados; Mermaid onde agrega; "Como explicar em inglês" + tabela PT↔EN; "Armadilhas comuns" (≥3 `[!warning]`); TL;DR `[!abstract]`; resumo em 1 linha.
- **Fase calibra a régua** — Iniciado: sem assumir base de React; Adepto: pleno; Magus: sênior, runtime/concurrent-aware.
- **Frontmatter** — `type: concept`, `fase: <iniciado|adepto|magus>`, `created: 2026-06-25`, `updated: 2026-06-25`, `status: seedling`, `publish: true`, `tags` (incluindo `react`, `entrevista`, a fase).
- **Seams (linkar, não duplicar):** tipagem difícil → galho TypeScript com React; padrões avançados → galho Design Patterns (futuro — citar sem wikilink se não existir); infra Next/RSC → galho Next.js (futuro); libs UI/server-state → galho Ecossistema (futuro); antipatterns → [[03-Dominios/Tecnologia/React/React Red Flag Manual|React Red Flag Manual]]; JS → trilha JavaScript; DOM → Plataforma Web; testes → Engenharia/Testes.
- **Wikilinks só para alvos confirmados** (`ls` antes; sem títulos inventados — atenção a maiúsc/minúsc). Verbetes no [[03-Dominios/Tecnologia/React/Dicionário de React|Dicionário de React]] (já existe) conforme surgirem.
- **Anti-fabricação** ([[feedback_no_fabrication]]).
- **Numeração** conforme o roster do spec (`01 - …` a `26 - …`).

## Estrutura de arquivos

Pasta-alvo: `03-Dominios/Tecnologia/React/React core/`

- **Criar (26):** `01 - O que é React e a UI declarativa.md` … `26 - Capstone ...md` (títulos do roster do spec)
- **Criar (1):** `index.md` do galho (MOC das 3 fases) — na Wave 4
- **Reescrever (teardown):** `03-Dominios/Tecnologia/React/index.md` → MOC multi-galho
- **Aposentar (teardown):** `React.md` → stub apontando pra trilha (ou visão-geral curta), inbounds repointados
- **Manter:** `Dicionário de React.md`, galho `TypeScript com React/`, galho `Charts/`, stubs de libs

---

## Procedimento por nota (template — cada uma das 26)

Um subagente por nota:

- [ ] **1. Pesquisar** o tópico (WebSearch, React 19-era 2026): API atual, edge cases, júnior vs sênior, mudanças do React 19.
- [ ] **2. Escrever** via `/escrever-nota` no path exato, fase indicada, exemplos `.tsx`, cobrindo o escopo do roster + seams (linkando).
- [ ] **3. Auto-gate** `/verificar-nota`; corrigir o que reprovar.
- [ ] **4. Reportar** ao orquestrador: escopo coberto, fontes, wikilinks, linhas, score.

Orquestrador **commita por sub-lote** (paths explícitos) e roda `/verificar-wikilinks` ao fim de cada fase.

---

## Wave 1 — Iniciado (notas 01–08)

Sub-lotes de até 5 subagentes; um por nota. Escopo = linha do roster do spec.

- [ ] **01 - O que é React e a UI declarativa** — declarativo vs imperativo, componentes, React 19-era
- [ ] **02 - JSX a fundo** — expressões, children, fragments, no que JSX compila (`jsx` runtime)
- [ ] **03 - Componentes e props** — function components, props tipadas, composição, children
- [ ] **04 - Renderização: o que dispara um render** — render→commit, estado vs props, idempotência
- [ ] **05 - useState e estado local** — updater, batching, imutabilidade
- [ ] **06 - Eventos e formulários controlados** — synthetic events, handlers tipados, controlled inputs
- [ ] **07 - Listas e keys** — render de listas, por que keys importam (intro reconciliation)
- [ ] **08 - Renderização condicional e composição** — composição, children, slots (intro)
- [ ] **Gate Iniciado:** commit por sub-lote; `/verificar-wikilinks 03-Dominios/Tecnologia/React/React core`; corrigir quebras reais.

## Wave 2 — Adepto (notas 09–18)

- [ ] **09 - useEffect e o modelo de efeitos** — deps, cleanup, "You Might Not Need an Effect"
- [ ] **10 - useRef e refs** — DOM refs, ref de valor, `forwardRef`/ref-as-prop (React 19)
- [ ] **11 - useContext e Context API** — provider, consumo, quando usar (linka TS-com-React)
- [ ] **12 - useReducer e estado complexo** — reducer vs `useState`
- [ ] **13 - Memoização: useMemo, useCallback, React.memo — e o React Compiler** — quando memoizar, custo, auto-memoização do React Compiler
- [ ] **14 - Custom hooks** — regras dos hooks, extração e composição
- [ ] **15 - Estado: local, elevado e externo** — lifting state, Zustand/Redux (menção)
- [ ] **16 - Reconciliation e diffing a fundo** — algoritmo, keys, bailout
- [ ] **17 - Performance no React** — re-renders, Profiler, `lazy`/Suspense, code splitting, efeito do React Compiler
- [ ] **18 - Error boundaries** — capturar erros de render, fallbacks, `react-error-boundary`
- [ ] **Gate Adepto:** commit por sub-lote; `/verificar-wikilinks`; corrigir quebras reais.

## Wave 3 — Magus (notas 19–26)

- [ ] **19 - Suspense e data fetching no cliente** — Suspense boundaries, loading states
- [ ] **20 - Concurrent features** — `useTransition`, `useDeferredValue`, prioridade
- [ ] **21 - O hook use()** — ler promises e context (React 19)
- [ ] **22 - Actions no React 19** — `useActionState`, `useOptimistic`, `useFormStatus`, form actions
- [ ] **23 - Server Components (RSC)** — modelo server/client, `'use client'`/`'use server'`, boundaries (conceito; infra → Next.js)
- [ ] **24 - Arquitetura de componentes** — composição, colocation, onde o estado mora
- [ ] **25 - Testing React** — React Testing Library, user-event, o que testar (linka Engenharia/Testes)
- [ ] **26 - Capstone — React na prática e em entrevista** — decision tree, modelo mental, perguntas-modelo, mapa de revisão (deve costurar wikilinks pras 25 irmãs — confirmar cada um via `ls`)
- [ ] **Gate Magus:** commit por sub-lote; `/verificar-wikilinks`; corrigir quebras reais.

## Wave 4 — Teardown e integração

- [ ] **4.1 Criar `index.md`** do galho `React core/` — MOC das 3 fases (links pras 26), com seam pros galhos vizinhos (TS-com-React, Design Patterns futuro, Next.js futuro).
- [ ] **4.2 Reescrever `React/index.md`** como MOC multi-galho — listar os 6 galhos (React core, Design Patterns [futuro], Next.js [futuro], Ecossistema [futuro], TypeScript com React, Charts), preservando libs/recursos e "Veja também".
- [ ] **4.3 Aposentar `React.md`** — virar stub curto apontando pro galho React core (ou visão-geral enxuta); repointar inbounds que citam `[[React]]` como conteúdo. Decidir stub vs visão-geral ao inspecionar os inbounds.
- [ ] **4.4 `/verificar-wikilinks 03-Dominios/Tecnologia/React`** — 0 quebras reais.
- [ ] **4.5 Atualizar [[00-Meta/Roadmap|Roadmap]]:** React (core) 🧱→🟡 (domínio em construção, galho 1/6 feito); marcar Onda A item 2 em progresso.
- [ ] **4.6 (Opcional) Ciclo de qualidade:** `/plantar-duvidas` → `/colher-duvidas`; `/enriquecer-nota`.
- [ ] **4.7 Commit final** + `status: done` neste plano.

---

## Self-review (cobertura do spec)

- Roster 26/26 → Waves 1–3 item a item ✓
- TS-first + seams → Global Constraints ✓
- React Compiler → notas 13 e 17 ✓
- Dicionário de React (existe) → verbetes no procedimento por nota ✓
- React vira multi-galho + aposentar monólito → Wave 4 ✓
- Atualização do Roadmap → Wave 4.5 ✓
- Fora de escopo (Next/Patterns/Ecossistema/tipagem) → respeitado pelos seams ✓
