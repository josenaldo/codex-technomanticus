---
title: "Spec — Galho Ecossistema React"
type: spec
status: approved
created: 2026-06-27
updated: 2026-06-27
tags:
  - spec
  - react
  - ecossistema
  - planejamento
---

# Spec — Galho Ecossistema React

> [!abstract] TL;DR
> **Galho final do domínio React** (fecha React = React core + Design Patterns + Next.js + Ecossistema): as bibliotecas que vivem fora da React, organizadas **por categoria de problema** (não lib-por-lib), em **~13 notas** / 3 fases / **TS-first**. Pré-requisito: React core; complementa o Next.js (server state no mundo RSC). Inclui **client-state (Zustand/Redux/Jotai)** — gap que não estava no sketch original — e **data-viz/charts** como categoria. Stubs flat existentes são absorvidos em ponteiros; a sub-área `Charts/` fica intacta e linkada.

## Contexto e objetivo

- **Domínio:** `03-Dominios/Tecnologia/React/Ecossistema/` (novo galho, irmão de `React core/`, `Design Patterns/`, `Next.js/`).
- **Perfil-alvo:** Senior Fullstack Developer, prep entrevistas internacionais remotas (frontend).
- **Posição no Roadmap:** Onda A (tripé frontend); **último galho planejado do domínio React** → ao concluir, React passa a **✅ completo** (galho 4/4 dos construídos; sub-galhos restantes = TypeScript com React e Charts, já existentes).
- **Padrão de execução:** brainstorming → spec (este arquivo) → writing-plans → subagente-por-nota (Sonnet), commit por sub-lote com paths explícitos, direto na `main`.

## Decisões cravadas

### Eixo organizador
- **Por categoria de problema**, não lib-por-lib. Cada nota ensina a categoria através da biblioteca dominante; não cataloga toda lib. Evita o "tour raso de 15 libs" que briga com o padrão capítulo.

### Escopo (gaps resolvidos)
- **Inclui client-state global** (Zustand / Redux Toolkit / Jotai) — não estava no sketch original do índice, mas é central pra entrevista; o React core só toca "estado externo" de leve (nota 15).
- **Inclui data visualization / charts** como categoria — a nota de categoria ensina como escolher/usar libs de gráficos e **linka a sub-área `Charts/` existente** (Recharts/ApexCharts/Lightweight) pros deep-dives. `Charts/` NÃO é absorvido; permanece como sub-área de aprofundamento.

### Material existente
- **Stubs flat absorvidos em ponteiros** (mesma jogada do Next.js stub): conteúdo bom de `MUI.md` (141 linhas) e `Mantine.md` (130) é refundido na nota de component systems; esqueletos de backlog (`TanStack Query.md`, `React Hook Form.md`, `TanStack Form.md`, `React Data Table.md`, `React Admin.md`) são absorvidos nas notas de categoria. Todos viram ponteiros pro galho.
- **`Charts/` intacto**, só linkado.
- **`Dicionário de React.md`** enriquecido com verbetes conforme surgirem.

### Fronteira com galhos vizinhos (anti-duplicação)
- **React core** = a primitiva (estado, context, effects). Callout `[!info]` de pré-requisito; não re-ensinar.
- **Next.js** = data fetching/cache no framework. A nota 12 (TanStack Query em RSC) costura com o Next; callout `[!info]` pras notas de data fetching/caching do galho Next.js, sem duplicar.
- **Redundância é reforço**: sobreposição deliberada sob a ótica da categoria é permitida; linkar, não podar.

## Estrutura do galho — ~13 notas, 3 fases

### 🟢 Iniciado — o mapa e as grandes distinções (3)
1. **O ecossistema React: o mapa** — o que vive fora da lib; categorias (server state, client state, forms, UI, tables, charts); como escolher dependência (manutenção, bundle size, lock-in, comunidade).
2. **Server state vs client state** — a distinção que organiza tudo; estado de servidor ≠ estado de UI; por que isso fez o TanStack Query existir.
3. **Component libraries e design systems** — MUI vs Mantine vs shadcn/ui vs headless (Radix) vs Tailwind; estilizado vs headless; como escolher e tematizar. *(absorve `MUI.md` + `Mantine.md`)*

### 🟡 Adepto — as ferramentas do dia a dia (5)
4. **TanStack Query I — queries, cache e invalidação** — `useQuery`, query keys, stale time / gc time, invalidação, refetch. *(absorve `TanStack Query.md`)*
5. **TanStack Query II — mutations e optimistic updates** — `useMutation`, optimistic updates, rollback, padrões de sincronização cache↔servidor.
6. **Formulários — React Hook Form + Zod** — uncontrolled-first, performance (re-render mínimo), validação com schema (Zod), integração com UI libs. *(absorve `React Hook Form.md` + `TanStack Form.md`)*
7. **Client state global — Context e Zustand** — quando Context basta, quando dói (re-render); Zustand como default moderno (store, selectors, middleware).
8. **Redux Toolkit — e quando ainda faz sentido** — RTK, slices, RTK Query; o legado vivo; Redux vs Zustand em entrevista.

### 🔴 Magus — avançado, integração e síntese (5)
9. **Estado avançado — Jotai, atoms e signals** — modelo atômico (bottom-up); o debate de signals; pra onde o estado React caminha.
10. **Tabelas e data grids — TanStack Table** — headless table; sorting/filtering/paginação/virtualização; vs MUI DataGrid (headless vs batteries-included). *(absorve `React Data Table.md` + `React Admin.md`)*
11. **Data visualization — escolhendo libs de gráficos** — landscape (Recharts/Nivo/visx/Tremor/ApexCharts); SVG vs canvas; declarativo vs imperativo; como escolher. *Linka [[03-Dominios/Tecnologia/React/Charts/index|Charts]] pros deep-dives por lib.*
12. **TanStack Query no mundo Next/RSC** — você ainda precisa de React Query com RSC? prefetch no server + hydration boundary; server state com RSC vs client cache. Costura com o galho Next.js.
13. **Capstone — montar o stack, trade-offs e entrevista** — decision trees por categoria (qual lib pra qual problema); anti-patterns; perguntas de entrevista + "como explicar em inglês"; mapa de revisão do galho.

## Convenções herdadas (padrão cravado do vault)

- **Padrão capítulo de livro**; **notas atômicas flat** ~440–540 linhas, TS-first, com **diagramas Mermaid**; **registro Feynman**.
- Frontmatter `fase:` (iniciado/adepto/magus) + agrupamento no MOC; tags incluindo `react`, `ecossistema`, `entrevista`, a fase.
- **`/verificar-nota`** por nota; **`/verificar-wikilinks`** por fase.
- **Subagente-por-nota** (Sonnet); commit por sub-lote com **paths EXPLÍCITOS** (working tree tem trabalho paralelo do usuário).
- **Direto na `main`** (convenção `feedback_galhos_direto_main`); push manual ao final.
- Índice MOC em `Ecossistema/index.md`; marco no `React/index` (🟩) e Roadmap (React → ✅ completo).
- **Capstone roda separado das últimas notas** (lição do galho Next.js) pra ver as 12 irmãs no `ls` — sem race no mapa de revisão.
- **Mídia (M1)** via `/adicionar-midia` ao final (opcional, como no Next.js).

## Fora de escopo (declarado)

- **Routing client-side (React Router)** — o Next.js cobre routing; SPA-routing fica fora desta rodada.
- **Charts deep-dive por lib** — fica na sub-área `Charts/` existente (só linkada).
- **i18n, testing libs, animação (Framer Motion)** — não nesta rodada.

## Critérios de sucesso

- ~13 notas escritas, todas passando `/verificar-nota` (alvo ≥ 10/12 equivalente).
- 0 wikilinks quebrados no galho (`/verificar-wikilinks`).
- Stubs absorvidos convertidos em ponteiros; `Charts/` intacto e linkado.
- Índice MOC completo; `React/index` e Roadmap atualizados → **React ✅ completo**.
- Fronteira com React core e Next.js respeitada (callouts de pré-requisito, sem re-ensinar primitiva).
