---
title: "Plano de Implementação — Galho Ecossistema React"
type: spec
created: 2026-06-27
updated: 2026-06-27
status: in_progress
tags:
  - spec
  - plano
  - react
  - ecossistema
aliases:
  - Implementação Ecossistema React
---

# Plano de Implementação — Galho Ecossistema React

> **Para executores:** implementa o spec [[00-Meta/specs/2026-06-27-galho-ecossistema-react-design|Spec — Galho Ecossistema React]]. Execução **subagente-por-nota**, em ondas por fase, gate de qualidade entre fases. Passos com checkbox (`- [ ]`).

**Objetivo:** escrever o galho **Ecossistema React** (13 notas, 3 fases, TS-first) em `03-Dominios/Tecnologia/React/Ecossistema/` — fechando o domínio React (React core + Design Patterns + Next.js + Ecossistema).

**Abordagem:** cada nota é escrita por um subagente via `/escrever-nota`, pesquisando a documentação oficial da lib dominante da categoria + WebSearch (estado 2026). Exemplos `.tsx`/`.ts`. Organização **por categoria de problema**, não lib-por-lib. Commit por sub-lote; gate `/verificar-nota` por nota; `/verificar-wikilinks` por fase.

**Stack/convenções:** Obsidian + Quartz; **React 19 + TypeScript**, libs do ecossistema em suas versões 2026 (TanStack Query v5, Zustand v5, Redux Toolkit 2.x, RHF + Zod, Jotai, TanStack Table v8, etc.); padrão capítulo; fases Iniciado/Adepto/Magus; PT-BR + "Como explicar em inglês".

## Global Constraints (valem para TODA nota)

- **Eixo por categoria de problema** — cada nota ensina a **categoria** (server state, client state, forms, component systems, tables, data-viz) através da lib dominante; NÃO catalogar toda lib. Evita o "tour raso de 15 libs" que briga com o padrão capítulo.
- **Complemento do React core (pré-requisito)** — NÃO re-ensinar primitiva. Toda nota que toca primitiva abre com callout `[!info]` linkando a nota canônica do React core e foca na lib externa:
  - Estado local/elevado/externo → [[03-Dominios/Tecnologia/React/React core/15 - Estado - local, elevado e externo|React core 15]]
  - useState → [[03-Dominios/Tecnologia/React/React core/05 - useState e estado local|React core 05]]
  - Context → [[03-Dominios/Tecnologia/React/React core/11 - useContext e Context API|React core 11]]
  - useReducer → [[03-Dominios/Tecnologia/React/React core/12 - useReducer e estado complexo|React core 12]]
  - Memoização/re-render → [[03-Dominios/Tecnologia/React/React core/13 - Memoização - useMemo, useCallback, React.memo e o React Compiler|React core 13]] · [[03-Dominios/Tecnologia/React/React core/17 - Performance no React|React core 17]]
  - Suspense → [[03-Dominios/Tecnologia/React/React core/19 - Suspense e data fetching no cliente|React core 19]]
  - RSC → [[03-Dominios/Tecnologia/React/React core/23 - Server Components (RSC)|React core 23]]
- **Fronteira com o Next.js (anti-duplicação)** — a nota 12 (TanStack Query em RSC) **costura** com o galho Next.js, sem duplicar. Callout `[!info]` para:
  - Data fetching no server → [[03-Dominios/Tecnologia/React/Next.js/05 - Data fetching no Server|Next.js 05]]
  - Caching do Next 15 → [[03-Dominios/Tecnologia/React/Next.js/07 - O modelo de caching do Next 15|Next.js 07]]
  - Server vs Client Components → [[03-Dominios/Tecnologia/React/Next.js/04 - Server vs Client Components|Next.js 04]]
- **Redundância é reforço** — sobreposição deliberada sob a ótica da categoria é permitida; linkar a nota canônica, não podar.
- **Escrita do ZERO com pesquisa** — fonte primária: docs oficiais da lib dominante (TanStack, Zustand, Redux Toolkit, React Hook Form, Zod, Jotai, MUI, Mantine, Radix) + WebSearch 2026. Citar em `## Referências`. **Anti-fabricação** ([[feedback_no_fabrication]]): não inventar APIs/flags; confirmar nome, versão e default.
- **Absorver stub quando indicado** — notas marcadas *(absorve X)* devem **ler o stub flat existente**, garimpar o conteúdo bom e incorporá-lo; o stub vira ponteiro no teardown (Wave 4). Stubs: `MUI.md` · `Mantine.md` · `TanStack Query.md` · `React Hook Form.md` · `TanStack Form.md` · `React Data Table.md` · `React Admin.md`.
- **`Charts/` intacto** — a nota 11 (data-viz) **linka** [[03-Dominios/Tecnologia/React/Charts/index|Charts]] pros deep-dives por lib; NÃO absorve nem reescreve a sub-área.
- **TS-first** — exemplos `.tsx`/`.ts` com tipos idiomáticos (generics de `useQuery`, tipos de store do Zustand, `z.infer` do Zod, `ColumnDef<T>` do TanStack Table, etc.).
- **Padrão capítulo** — problema-primeiro; registro Feynman; exemplos trabalhados; Mermaid onde agrega; "Como explicar em inglês" + tabela PT↔EN; "Armadilhas comuns" (≥3 `[!warning]`); TL;DR `[!abstract]`; resumo em 1 linha. ~440–540 linhas.
- **Frontmatter** — `type: concept`, `fase: <iniciado|adepto|magus>`, `created: 2026-06-27`, `updated: 2026-06-27`, `status: seedling`, `publish: true`, `tags` (incluindo `react`, `ecossistema`, `entrevista`, a fase).
- **Wikilinks só para alvos confirmados** (`ls` antes; sem títulos inventados — atenção a caixa). Verbetes no [[03-Dominios/Tecnologia/React/Dicionário de React|Dicionário de React]] conforme surgirem.
- **Numeração** conforme roster do spec (`01 - …` a `13 - …`).

## Estrutura de arquivos

Pasta-alvo: `03-Dominios/Tecnologia/React/Ecossistema/` (criar)

- **Criar (13):** `01 - O ecossistema React - o mapa.md` … `13 - Capstone ...md` (títulos do roster abaixo)
- **Criar (1):** `index.md` do galho (MOC das 3 fases) — Wave 4
- **Modificar (teardown):** `03-Dominios/Tecnologia/React/index.md` (galho Ecossistema ⬜→🟩; ajustar bloco "Recursos e libs" que aponta pros stubs); `00-Meta/Roadmap.md` (linha React → ✅ completo; bullet 113)
- **Aposentar (converter em ponteiros):** `MUI.md`, `Mantine.md`, `TanStack Query.md`, `React Hook Form.md`, `TanStack Form.md`, `React Data Table.md`, `React Admin.md` → cada um vira stub-ponteiro pra nota de categoria correspondente (Wave 4), preservando os `[[...]]` existentes.
- **Manter:** `Charts/` (intacto, linkado), `Dicionário de React.md` (enriquecer), `Ícones.md`, `React Red Flag Manual.md`, demais galhos.

---

## Procedimento por nota (template — cada uma das 13)

Um subagente por nota:

- [ ] **1. Pesquisar** o tema (docs oficiais da lib dominante + WebSearch 2026): API atual, versão, defaults, exemplos idiomáticos TS. Se a nota *absorve* um stub, **ler o stub primeiro** e garimpar o conteúdo aproveitável.
- [ ] **2. Escrever** via `/escrever-nota` no path exato, fase indicada, exemplos `.tsx`/`.ts`; abrir com callout `[!info]` de pré-requisito quando tocar primitiva do React core ou costurar com o Next.js (ver Global Constraints).
- [ ] **3. Auto-gate** `/verificar-nota`; corrigir o que reprovar.
- [ ] **4. Reportar** ao orquestrador: tema coberto, fontes, wikilinks usados, linhas, score.

Orquestrador **commita por sub-lote** (paths EXPLÍCITOS — working tree pode ter trabalho paralelo do usuário) e roda `/verificar-wikilinks` ao fim de cada fase.

---

## Wave 1 — Iniciado (notas 01–03)

- [ ] **01 - O ecossistema React: o mapa** — o que vive fora da lib; as categorias (server state, client state, forms, UI/component systems, tables, charts); como escolher dependência (manutenção, bundle size, lock-in, comunidade, TS support). Mapa Mermaid das categorias → notas do galho. Abre o galho.
- [ ] **02 - Server state vs client state** — a distinção que organiza tudo; estado de servidor (remoto, assíncrono, compartilhado, "cache de algo que não é seu") ≠ estado de UI (local, síncrono, seu); por que essa distinção fez o TanStack Query existir; tabela de decisão. (callout → React core 15)
- [ ] **03 - Component libraries e design systems** — MUI vs Mantine vs shadcn/ui vs headless (Radix) vs utility-first (Tailwind); estilizado vs headless vs unstyled; theming/tokens; como escolher (DX, customização, bundle, acessibilidade). *(absorve `MUI.md` + `Mantine.md`)*
- [ ] **Gate Iniciado:** commit por sub-lote; `/verificar-wikilinks 03-Dominios/Tecnologia/React/Ecossistema`; corrigir quebras reais (forward-refs pras notas 04–13 + index resolvem nas próximas waves).

## Wave 2 — Adepto (notas 04–08)

- [ ] **04 - TanStack Query I — queries, cache e invalidação** — `useQuery`, query keys (estrutura/hierarquia), `staleTime` vs `gcTime`, status (`pending`/`error`/`success`) e fetch status, invalidação (`invalidateQueries`), refetch, `QueryClient`/`QueryClientProvider`. Tipos genéricos. *(absorve `TanStack Query.md`)* (callout → React core 19)
- [ ] **05 - TanStack Query II — mutations e optimistic updates** — `useMutation`, ciclo `onMutate`/`onError`/`onSettled`, optimistic updates com `setQueryData` + rollback via contexto, invalidação pós-mutation, padrões de sincronização cache↔servidor. (consome a nota 04)
- [ ] **06 - Formulários — React Hook Form + Zod** — uncontrolled-first e por que importa (re-render mínimo); `useForm`/`register`/`handleSubmit`/`formState`; `Controller` pra UI libs controladas; validação com schema Zod via `zodResolver` + `z.infer` pra tipos; arrays de campos. *(absorve `React Hook Form.md` + `TanStack Form.md`; mencionar TanStack Form como alternativa emergente)* (callout → React core 06)
- [ ] **07 - Client state global — Context e Zustand** — quando Context basta e quando dói (re-render de toda a árvore consumidora); Zustand como default moderno: `create`, store + selectors (subscrição granular), `set`/`get`, middleware (`persist`, `immer`, `devtools`); fora da árvore React. (callout → React core 11 + 15)
- [ ] **08 - Redux Toolkit — e quando ainda faz sentido** — RTK como o Redux moderno (`configureStore`, `createSlice`, Immer embutido, thunks); RTK Query de relance (e por que TanStack Query costuma vencer pra server state); o legado vivo; **Redux vs Zustand em entrevista** (boilerplate, DevTools, time-travel, ecossistema). (callout → React core 12)
- [ ] **Gate Adepto:** commit por sub-lote; `/verificar-wikilinks`; corrigir quebras reais.

## Wave 3 — Magus (notas 09–12)

- [ ] **09 - Estado avançado — Jotai, atoms e signals** — modelo atômico bottom-up (átomos compostos) vs store top-down (Zustand/Redux); `atom`/`useAtom`/derived atoms; o debate de **signals** (Preact Signals, Solid) e o que isso significa pro React; pra onde o estado React caminha. (callout → React core 15)
- [ ] **10 - Tabelas e data grids — TanStack Table** — headless table (você controla a marcação); `useReactTable`, `ColumnDef<T>`, core row model; sorting/filtering/pagination/row selection; virtualização (TanStack Virtual) pra listas grandes; **headless vs batteries-included** (MUI DataGrid/AG Grid). *(absorve `React Data Table.md` + `React Admin.md`)*
- [ ] **11 - Data visualization — escolhendo libs de gráficos** — o landscape (Recharts/Nivo/visx/Tremor/ApexCharts); SVG vs canvas (volume de dados); declarativo (componível em React) vs imperativo (D3 puro); wrappers React vs D3 cru; como escolher por caso. **Linka [[03-Dominios/Tecnologia/React/Charts/index|Charts]] pros deep-dives por lib** (não reescreve a sub-área).
- [ ] **12 - TanStack Query no mundo Next/RSC** — você ainda precisa de React Query com RSC? Prefetch no server (`prefetchQuery`) + `HydrationBoundary` + `dehydrate`; server state via RSC (fetch no server) vs client cache (interatividade/refetch/optimistic); quando cada um. **Costura com o galho Next.js, sem duplicar.** (callout → Next.js 05 + 07 + 04; consome notas 04/05)
- [ ] **Gate Magus:** commit por sub-lote; `/verificar-wikilinks`; corrigir quebras reais.

## Wave 4 — Capstone + Teardown e integração

> O **capstone roda SOZINHO, depois das 12 irmãs commitadas** (lição do Next.js: evita race no `ls` do mapa de revisão).

- [ ] **4.1 Escrever 13 - Capstone — montar o stack, trade-offs e entrevista** — decision trees por categoria (qual lib pra qual problema: server state? client state? forms? UI? tables? charts?); anti-patterns (Redux pra tudo, server state no client state, etc.); perguntas de entrevista + "como explicar em inglês"; **mapa de revisão do galho** (costurar wikilinks pras 12 irmãs — confirmar via `ls` antes). Auto-gate `/verificar-nota`. Commit.
- [ ] **4.2 Criar `index.md`** do galho `Ecossistema/` — MOC das 3 fases (links pras 13), com seam pros galhos vizinhos (React core, Next.js, TS-com-React, Charts).
- [ ] **4.3 Aposentar stubs em ponteiros** — converter `MUI.md`, `Mantine.md`, `TanStack Query.md`, `React Hook Form.md`, `TanStack Form.md`, `React Data Table.md`, `React Admin.md` em ponteiros pras notas de categoria (preservam os `[[...]]` existentes). `grep` quem linka cada um antes.
- [ ] **4.4 Atualizar `React/index.md`** — galho Ecossistema de ⬜ planejado → 🟩 (linkar o índice); ajustar o bloco "Recursos e libs" (stubs agora apontam pro galho).
- [ ] **4.5 `/verificar-wikilinks 03-Dominios/Tecnologia/React/Ecossistema`** — 0 quebras reais.
- [ ] **4.6 Atualizar [[00-Meta/Roadmap|Roadmap]]:** linha React → 🟩 **✅ completo** (Ecossistema 13, 2026-06-27); ajustar bullet 113.
- [ ] **4.7 (Opcional) Ciclo de qualidade:** `/plantar-duvidas` → `/colher-duvidas`; `/enriquecer-nota`; **Mídia (M1)** via `/adicionar-midia`.
- [ ] **4.8 Commit final** + `status: done` neste plano + push manual (confirmar com usuário).

---

## Self-review (cobertura do spec)

- Roster 13/13 → Waves 1–3 (notas 01–12) + Wave 4.1 (capstone 13) item a item ✓
- Eixo por categoria de problema (não lib-por-lib) → Global Constraints + roster ✓
- Inclui client-state (Zustand/Redux/Jotai) → notas 07/08/09 ✓
- Charts vira categoria (nota 11) mas `Charts/` intacto e só linkado → nota 11 + Global Constraints + Wave 4 (não absorve) ✓
- Stubs flat absorvidos em ponteiros → notas 03/04/06/10 *(absorve)* + Wave 4.3 ✓
- Fronteira React core (callout de pré-requisito, não re-ensinar) → Global Constraints (mapa de seams com paths confirmados) + notas 02/04/06/07/08/09 ✓
- Fronteira Next.js (nota 12 costura, não duplica) → Global Constraints + nota 12 ✓
- Redundância é reforço → Global Constraints ✓
- TS-first + padrão capítulo + Feynman + ~440–540 linhas + Mermaid → Global Constraints ✓
- Índice do galho + aposentar stubs + React/index + Roadmap → Wave 4 ✓
- Fora de escopo (React Router, charts deep-dive, i18n/testing/animação) → não há tarefa; respeitado ✓
- Capstone separado das irmãs (sem race no mapa de revisão) → Wave 4.1 ✓
- Type/naming consistency: APIs citadas (`useQuery`/`useMutation`/`invalidateQueries`/`setQueryData`/`prefetchQuery`/`HydrationBoundary`/`dehydrate`, `create`+selectors do Zustand, `configureStore`/`createSlice`, `useForm`/`zodResolver`/`z.infer`, `atom`/`useAtom`, `useReactTable`/`ColumnDef<T>`) usadas consistentemente entre notas 04/05/06/07/08/09/10/12 ✓
