---
title: "Plano — Trilha React core"
type: spec
created: 2026-06-25
updated: 2026-06-25
status: draft
tags:
  - spec
  - trilha
  - react
  - frontend
aliases:
  - Plano React core
---

# Plano — Trilha React core (galho 1 do domínio React)

## Objetivo

`Tecnologia/React` deixa de ser monólito (`React.md`) e passa a ser um **domínio multi-galho** (como Node/Java). Este spec cobre o **galho 1: React core** — a biblioteca em si, em 3 fases (Iniciado/Adepto/Magus), padrão capítulo, **TS-first** (todos os exemplos em `.tsx` com tipos idiomáticos). Alvo: prep entrevistas internacionais, perfil Senior Fullstack, eixo frontend-web. É a **Onda A item 2** do [[00-Meta/Roadmap|Roadmap]].

**Tese:** React é uma biblioteca de UI **declarativa e baseada em componentes**, onde você descreve *o que* a UI deve ser para um dado estado e o React reconcilia *como* chegar lá. Em 2026 (React 19), o modelo se estende ao servidor (RSC) e à concorrência (transitions, `use()`, Actions). O eixo da trilha é ir do **modelo mental declarativo** até **hooks a fundo, performance, concurrent features e Server Components**.

## Domínio multi-galho — sequência

O domínio React passa a ter os galhos (cada um em subpasta, com índice, 3 fases):

1. **React core** — *este spec*
2. **React Design Patterns** *(novo — spec próprio depois)*
3. **Next.js** — App Router a fundo + Pages Router leve *(spec próprio depois)*
4. **Ecossistema** — MUI, Mantine, TanStack Query *(spec próprio depois)*
5. **TypeScript com React** — *já existe (15 notas); preservado como galho avançado de tipagem; a core linka, não duplica*
6. **Charts** — *já existe*

Decomposição deliberada: o conjunto (React + Next + libs + patterns ≈ 40+ notas) é grande demais para um spec só; cada galho é construído em sequência, com spec→plano→build próprios.

## Princípios

- **Escrita do ZERO com pesquisa** (React 19-era, estado 2026). O monólito `React.md` é referência de tópicos, NÃO fonte de migração.
- **TS-first**: exemplos em `.tsx` com tipos idiomáticos (props, `useState<T>`, handlers tipados). Tipagem básica é inline; a tipagem *difícil* (generics, polymorphic, compound, satisfies) é linkada ao galho [[03-Dominios/Tecnologia/React/TypeScript com React/index|TypeScript com React]].
- **Padrão capítulo** ([[feedback_padrao_capitulo_livro]]): problema-primeiro, registro Feynman ([[feedback_enriquecimento_feynman]]), exemplos trabalhados, Mermaid onde agrega, "Como explicar em inglês" + PT↔EN, "Armadilhas comuns". Notas profundas com diagramas ([[feedback_notas_profundas_diagramas]]).
- **Calibração por fase** ([[project_trilhas_fases_aprendizado]]).
- **Patterns enxutos aqui**: compound/render-props/HOC tocam de leve e linkam o galho **Design Patterns** (futuro). Redundância é reforço ([[feedback_redundancia_entre_notas]]).

## Fronteiras (seams)

Regra de ouro: **"o que o React é e como eu uso" fica aqui; a tipagem difícil, os padrões avançados, a infra de framework e o navegador são linkados.**

| Tema | Fica no React core | Linka para |
| ---- | ------------------ | ---------- |
| Tipagem básica (props/state/hooks/eventos) | inline, TS-first | — |
| Tipagem avançada (generics, polymorphic, compound, satisfies) | menção | galho **TypeScript com React** |
| Padrões avançados (compound, render props, HOC, prop getters) | menção/intro | galho **React Design Patterns** (futuro) |
| Infra de framework (App Router, server actions, caching, deploy) | só o conceito RSC | galho **Next.js** (futuro) |
| Libs de UI (MUI, Mantine) e server state (TanStack Query) | menção | galho **Ecossistema** (futuro) |
| Antipatterns detalhados | "Armadilhas" por nota | [[03-Dominios/Tecnologia/React/React Red Flag Manual\|React Red Flag Manual]] (companion) |
| Linguagem JS (closures, this, async) | nada | trilha **JavaScript** (pronta) |
| DOM / APIs de browser | só o que o React abstrai | **Plataforma Web** |
| Build/bundler | menção | **Tooling e Build** (pronta) |
| Testes (conceito) | como testar React | **Engenharia/Testes** |

## Roster (26 notas — 8 / 10 / 8)

### 🟢 Iniciado — fundamentos (8)
1. **O que é React e a UI declarativa** — modelo mental declarativo vs imperativo, componentes, React 19-era
2. **JSX a fundo** — expressões, children, fragments, no que JSX compila (`jsx` runtime)
3. **Componentes e props** — function components, props tipadas, composição, children
4. **Renderização: o que dispara um render** — render→commit, estado vs props, idempotência do render
5. **`useState` e estado local** — updater function, batching, imutabilidade do estado
6. **Eventos e formulários controlados** — synthetic events, handlers tipados, controlled inputs
7. **Listas e keys** — render de listas, por que keys importam (intro a reconciliation)
8. **Renderização condicional e composição** — padrões de composição, children, slots (intro)

### 🟡 Adepto — hooks, estado, efeitos (10)
9. **`useEffect` e o modelo de efeitos** — quando roda, cleanup, deps, "You Might Not Need an Effect"
10. **`useRef` e refs** — DOM refs, ref de valor, `forwardRef` e ref-as-prop (React 19)
11. **`useContext` e Context API** — provider, consumo, quando usar *(linka TS-com-React)*
12. **`useReducer` e estado complexo** — reducer pattern vs `useState`
13. **Memoização: `useMemo`, `useCallback`, `React.memo` — e o React Compiler** — quando memoizar, custo, e como o **React Compiler** (auto-memoização, React 19-era) muda essa história
14. **Custom hooks** — regras dos hooks, extração e composição de lógica
15. **Estado: local, elevado e externo** — lifting state, quando externalizar (Zustand/Redux como menção)
16. **Reconciliation e diffing a fundo** — o algoritmo, keys, bailout de render
17. **Performance no React** — re-renders, React DevTools Profiler, `lazy`/Suspense, code splitting, o efeito do React Compiler
18. **Error boundaries** — capturar erros de render, fallbacks, `react-error-boundary`

### 🔴 Magus — concurrent, RSC, React 19, capstone (8)
19. **Suspense e data fetching no cliente** — Suspense boundaries, estados de carregamento
20. **Concurrent features** — `useTransition`, `useDeferredValue`, prioridade de render
21. **O hook `use()`** — ler promises e context condicionalmente (React 19)
22. **Actions no React 19** — `useActionState`, `useOptimistic`, `useFormStatus`, form actions
23. **Server Components (RSC)** — modelo server/client, `'use client'`/`'use server'`, boundaries *(conceito; infra → galho Next.js)*
24. **Arquitetura de componentes** — composição, colocation, onde o estado mora, estrutura de projeto
25. **Testing React** — React Testing Library, o que testar, user-event *(linka Engenharia/Testes)*
26. **Capstone — React na prática e em entrevista** — decision tree, modelo mental unificado, perguntas-modelo, mapa de revisão, "como explicar em inglês"

## Artefatos do domínio

- **`Dicionário de React`** — já existe; enriquecer com verbetes da trilha (conforme surgem).
- **Índice do galho React core** — `index.md` da subpasta, MOC das 3 fases.
- **Índice do domínio React** (`React/index.md`) — reescrever como MOC multi-galho ao fim (linkando os 6 galhos), preservando libs/recursos.
- **`React.md`** (monólito) — aposentar em stub apontando pra trilha, repointando inbounds. (decidir no teardown se vira stub ou é mantido como visão-geral curta)

## Execução

Pasta-alvo do galho: `03-Dominios/Tecnologia/React/React core/` (notas `01 - …` a `26 - …` + `index.md`).

1. **Escrever o galho fresco** (com pesquisa), em ondas por fase, gate `/verificar-nota` por nota e `/verificar-wikilinks` por fase. Padrão subagente-por-nota.
2. **Pós-escrita (teardown):** criar/atualizar índice do galho; atualizar `React/index.md` para multi-galho; aposentar `React.md` em stub; repointar inbounds; verificar 0 quebras; atualizar [[00-Meta/Roadmap|Roadmap]].
3. **(Opcional) Ciclo de qualidade:** `/plantar-duvidas` → `/colher-duvidas`; `/enriquecer-nota`.

## Fora de escopo (deste galho)

- **Next.js** (App Router, server actions, caching, deploy) → galho próprio.
- **React Design Patterns** (compound, render props, HOC a fundo) → galho próprio.
- **MUI, Mantine, TanStack Query** → galho Ecossistema.
- **Tipagem avançada React** → galho TypeScript com React (existe).
- Linguagem JS, DOM/browser, build → trilhas/domínios próprios (prontos).

## Padrões e referências

- [[00-Meta/Roadmap|Roadmap de Trilhas]] (Onda A, item 2)
- [[project_trilhas_fases_aprendizado]], [[feedback_padrao_capitulo_livro]], [[feedback_notas_profundas_diagramas]], [[feedback_notas_atomicas]], [[project_tronco_galhos_pattern]], [[project_artefatos_dominio]]
- Trilhas-modelo já construídas: [[03-Dominios/Tecnologia/JavaScript/index|JavaScript]] (26), [[03-Dominios/Tecnologia/TypeScript/index|TypeScript]] (27), [[03-Dominios/Tecnologia/Tooling e Build/index|Tooling e Build]] (26)
