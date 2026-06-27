---
title: "React core"
type: moc
publish: true
created: 2026-06-25
updated: 2026-06-25
status: evergreen
tags:
  - react
  - moc
aliases:
  - React core
---

# React core

> [!abstract] TL;DR
> O galho da **biblioteca React em si**, em 3 fases (Iniciado/Adepto/Magus), **TS-first** e React 19-era. A tese: React é uma biblioteca de UI **declarativa e baseada em componentes** — você descreve *o que* a UI deve ser para um dado estado (`UI = f(estado)`) e o React reconcilia *como* chegar lá. Em 2026 o modelo se estende ao servidor (RSC) e à concorrência (transitions, `use()`, Actions). A tipagem difícil vive no galho [[03-Dominios/Tecnologia/React/TypeScript com React/index|TypeScript com React]]; a infra de framework no futuro galho Next.js.

## 🟢 Iniciado — fundamentos

- [[01 - O que é React e a UI declarativa]] — modelo mental declarativo, componentes, React 19-era
- [[02 - JSX a fundo]] — expressões, children, fragments, no que JSX compila
- [[03 - Componentes e props]] — function components, props tipadas, composição
- [[04 - Renderização - o que dispara um render]] — render→commit, estado vs props, pureza
- [[05 - useState e estado local]] — updater, batching, imutabilidade
- [[06 - Eventos e formulários controlados]] — synthetic events, handlers tipados
- [[07 - Listas e keys]] — por que keys importam (intro a reconciliation)
- [[08 - Renderização condicional e composição]] — composição, children, slots

## 🟡 Adepto — hooks, estado, efeitos

- [[09 - useEffect e o modelo de efeitos]] — deps, cleanup, "You Might Not Need an Effect"
- [[10 - useRef e refs]] — DOM refs, valor, `forwardRef`/ref-as-prop (React 19)
- [[11 - useContext e Context API]] — provider, consumo, performance
- [[12 - useReducer e estado complexo]] — reducer vs `useState`
- [[13 - Memoização - useMemo, useCallback, React.memo e o React Compiler]] — memoização e o React Compiler
- [[14 - Custom hooks]] — regras dos hooks, extração de lógica
- [[15 - Estado - local, elevado e externo]] — lifting state, Zustand/Redux
- [[16 - Reconciliation e diffing a fundo]] — algoritmo, keys, Fiber
- [[17 - Performance no React]] — re-renders, Profiler, `lazy`/Suspense
- [[18 - Error boundaries]] — capturar erros de render, fallbacks

## 🔴 Magus — concurrent, RSC, React 19

- [[19 - Suspense e data fetching no cliente]] — Suspense boundaries, loading declarativo
- [[20 - Concurrent features]] — `useTransition`, `useDeferredValue`
- [[21 - O hook use()]] — ler promises e context (React 19)
- [[22 - Actions no React 19]] — `useActionState`, `useOptimistic`, `useFormStatus`
- [[23 - Server Components (RSC)]] — modelo server/client, boundaries
- [[24 - Arquitetura de componentes]] — composição, colocation, onde o estado mora
- [[25 - Testing React]] — React Testing Library, testar comportamento
- [[26 - Capstone - React na prática e em entrevista]] — síntese, decision tree, entrevista

## Veja também

- [[03-Dominios/Tecnologia/React/index|React (domínio)]] — os galhos do domínio
- [[03-Dominios/Tecnologia/React/TypeScript com React/index|TypeScript com React]] — tipagem avançada
- [[03-Dominios/Tecnologia/React/Dicionário de React|Dicionário de React]] — glossário
- [[03-Dominios/Tecnologia/React/React Red Flag Manual|React Red Flag Manual]] — antipatterns
- [[03-Dominios/Tecnologia/JavaScript/index|JavaScript]] · [[03-Dominios/Tecnologia/Tooling e Build/index|Tooling e Build]]
