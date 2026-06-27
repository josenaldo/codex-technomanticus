---
title: "Plano de Implementação — Galho Next.js (App Router)"
type: spec
created: 2026-06-27
updated: 2026-06-27
status: in_progress
tags:
  - spec
  - plano
  - react
  - nextjs
aliases:
  - Implementação Next.js App Router
---

# Plano de Implementação — Galho Next.js (App Router)

> **Para executores:** implementa o spec [[00-Meta/specs/2026-06-27-galho-nextjs-app-router-design|Spec — Galho Next.js (App Router)]]. Execução **subagente-por-nota**, em ondas por fase, gate de qualidade entre fases. Passos com checkbox (`- [ ]`).

**Objetivo:** escrever o galho **Next.js (App Router)** (16 notas, 3 fases, TS-first, baseline Next 15) em `03-Dominios/Tecnologia/React/Next.js/`.

**Abordagem:** cada nota é escrita por um subagente via `/escrever-nota`, pesquisando a documentação oficial do Next 15 + WebSearch (estado 2026). Exemplos `.tsx`/`.ts`. Commit por sub-lote; gate `/verificar-nota` por nota; `/verificar-wikilinks` por fase.

**Stack/convenções:** Obsidian + Quartz; **Next.js 15 + App Router + React 19 + TypeScript**; padrão capítulo; fases Iniciado/Adepto/Magus; PT-BR + "Como explicar em inglês".

## Global Constraints (valem para TODA nota)

- **Baseline Next 15** — todo exemplo e default assume Next 15 / App Router / React 19. **Caching no modelo do 15** ("uncached by default": `fetch` e Route Handlers GET não cacheados por padrão; `staleTimes`).
- **Versionamento explícito e isolável** — diffs do **Next 14** em callouts `[!warning]`; horizonte do **Next 16** (`'use cache'` / cache components) em callouts `[!info]`. Isolar o que é específico do modelo de cache do 15 em seção/callout identificável, para **promover o baseline pro 16 ser troca cirúrgica**.
- **Complemento do React (pré-requisito)** — NÃO re-ensinar primitiva. Toda nota que toca primitiva abre com callout `[!info]` linkando a nota canônica do React core e foca no "como o Next cabeia":
  - RSC → [[03-Dominios/Tecnologia/React/React core/23 - Server Components (RSC)|React core 23]]
  - Actions → [[03-Dominios/Tecnologia/React/React core/22 - Actions no React 19|React core 22]]
  - Suspense → [[03-Dominios/Tecnologia/React/React core/19 - Suspense e data fetching no cliente|React core 19]]
  - `use()` → [[03-Dominios/Tecnologia/React/React core/21 - O hook use()|React core 21]]
  - Context → [[03-Dominios/Tecnologia/React/React core/11 - useContext e Context API|React core 11]]
  - Error boundaries (`error.tsx`) → [[03-Dominios/Tecnologia/React/React core/18 - Error boundaries|React core 18]]
- **Redundância é reforço** — sobreposição deliberada sob a ótica do framework é permitida; linkar a nota canônica, não podar.
- **Escrita do ZERO com pesquisa** — fonte primária: docs oficiais Next 15 (nextjs.org/docs) + WebSearch 2026. Citar em `## Referências`. **Anti-fabricação** ([[feedback_no_fabrication]]): não inventar APIs/flags; confirmar nome e default.
- **TS-first** — exemplos `.tsx`/`.ts` com tipos idiomáticos (`Metadata`, `NextRequest`, `PageProps`, etc.).
- **Padrão capítulo** — problema-primeiro; registro Feynman; exemplos trabalhados; Mermaid onde agrega; "Como explicar em inglês" + tabela PT↔EN; "Armadilhas comuns" (≥3 `[!warning]`); TL;DR `[!abstract]`; resumo em 1 linha. ~440–540 linhas.
- **Frontmatter** — `type: concept`, `fase: <iniciado|adepto|magus>`, `created: 2026-06-27`, `updated: 2026-06-27`, `status: seedling`, `publish: true`, `tags` (incluindo `react`, `nextjs`, `entrevista`, a fase).
- **Wikilinks só para alvos confirmados** (`ls` antes; sem títulos inventados — atenção a caixa). Verbetes no [[03-Dominios/Tecnologia/React/Dicionário de React|Dicionário de React]] conforme surgirem.
- **Numeração** conforme roster do spec (`01 - …` a `16 - …`).

## Estrutura de arquivos

Pasta-alvo: `03-Dominios/Tecnologia/React/Next.js/` (criar)

- **Criar (16):** `01 - O que é o Next.js e por que existe.md` … `16 - Capstone ...md` (títulos do roster abaixo)
- **Criar (1):** `index.md` do galho (MOC das 3 fases) — Wave 4
- **Modificar (teardown):** `03-Dominios/Tecnologia/React/index.md` (galho Next.js ⬜→🟩); `00-Meta/Roadmap.md` (galho 3/6)
- **Aposentar:** stub `03-Dominios/Tecnologia/React/Next.js.md` (993B) → converter em stub-ponteiro pro índice do galho (Wave 4), preservando wikilinks `[[Next.js]]` existentes.
- **Manter:** `Dicionário de React.md` (enriquecer com verbetes), demais galhos

---

## Procedimento por nota (template — cada uma das 16)

Um subagente por nota:

- [ ] **1. Pesquisar** o tema (docs oficiais Next 15 + WebSearch 2026): API atual, defaults, diffs do 14, horizonte do 16, exemplos idiomáticos TS.
- [ ] **2. Escrever** via `/escrever-nota` no path exato, fase indicada, exemplos `.tsx`/`.ts`; abrir com callout `[!info]` de pré-requisito quando tocar primitiva do React (ver Global Constraints).
- [ ] **3. Auto-gate** `/verificar-nota`; corrigir o que reprovar.
- [ ] **4. Reportar** ao orquestrador: tema coberto, fontes, wikilinks usados, linhas, score.

Orquestrador **commita por sub-lote** (paths EXPLÍCITOS — working tree pode ter trabalho paralelo do usuário) e roda `/verificar-wikilinks` ao fim de cada fase.

---

## Wave 1 — Iniciado (notas 01–05)

- [x] **01 - O que é o Next.js e por que existe** — meta-framework sobre React; o que resolve (routing, rendering, data, bundling, otimização); App Router como padrão; posição no ecossistema; quando NÃO usar. ✅ 439 linhas, commitada.
- [x] **02 - App Router vs Pages Router** — file-system routing; salto de paradigma (RSC-first vs `getServerSideProps`/`getStaticProps`); **Pages Router "de leve" mora aqui** (o que é, por que ainda existe, noções de coexistência/migração). ✅ 470 linhas, commitada.
- [x] **03 - Estrutura de rotas: layouts, pages, loading, error** — arquivos especiais (`page`/`layout`/`loading`/`error`/`not-found`/`template`); nested layouts; route groups `(grupo)`; rotas dinâmicas `[slug]`/`[...catch]`. (callout error.tsx → React core 18) ✅ 506 linhas, 12/12.
- [x] **04 - Server vs Client Components** — conceito central do App Router; boundary `'use client'`; árvore de RSC; serialização de props; padrões de composição (client dentro de server). (callout → React core 23) ✅ 506 linhas, 12/12.
- [x] **05 - Data fetching no Server** — `async`/`await` em Server Components; `fetch` no server; sequencial vs paralelo; request memoization; padrões de erro/`not-found`. (callout → React core 21/19) ✅ 594 linhas, 12/12.
- [x] **Gate Iniciado:** commit por sub-lote; `/verificar-wikilinks 03-Dominios/Tecnologia/React/Next.js`; corrigir quebras reais. ✅ 0 quebras reais; 20 forward-refs (notas 06–16 + index) com nomes canônicos, resolvem nas próximas waves.

## Wave 2 — Adepto (notas 06–12)

- [ ] **06 - Server Actions e mutations** — `'use server'`; `<form action={fn}>`; `revalidatePath`/`revalidateTag`; `useActionState`/`useFormStatus` no Next; progressive enhancement; segurança (validação no server). (callout → React core 22)
- [ ] **07 - O modelo de caching do Next 15** — os 4 caches (Request Memoization, Data Cache, Full Route Cache, Router Cache); **default uncached** no 15; `fetch` cache options (`force-cache`/`no-store`/`revalidate`); `[!warning]` diffs do 14 (era cached por padrão); horizonte `'use cache'` (16). **Seção de cache isolada para promoção futura.**
- [ ] **08 - Rendering strategies: SSR, SSG, ISR, PPR** — estático vs dinâmico; `generateStaticParams`; `dynamic`/`revalidate` route segment config; ISR; PPR (Partial Prerendering) como ponte; como o Next decide.
- [ ] **09 - Streaming, Suspense e `loading.tsx`** — streaming SSR no App Router; `loading.tsx` = Suspense boundary automático; `<Suspense>` manual; UX progressiva. (callout → React core 19)
- [ ] **10 - Route Handlers e APIs** — `route.ts`; métodos HTTP; `NextRequest`/`NextResponse` e Web Request/Response; quando usar Route Handler vs Server Action; caching de GET no 15.
- [ ] **11 - Metadata, SEO e assets sociais** — Metadata API estática (`export const metadata`) e dinâmica (`generateMetadata`); OG images (`opengraph-image`); `sitemap.ts`/`robots.ts`; títulos templated.
- [ ] **12 - Navegação e o Router** — `<Link>` e prefetch; `useRouter`/`usePathname`/`useSearchParams`; navegação client vs server; `staleTimes`; `redirect`/`notFound`.
- [ ] **Gate Adepto:** commit por sub-lote; `/verificar-wikilinks`; corrigir quebras reais.

## Wave 3 — Magus (notas 13–16)

- [ ] **13 - Middleware e auth na borda** — `middleware.ts`; matcher; Edge runtime e limites; rewrites/redirects; padrões de proteção de rota e leitura de sessão/cookie (sem cair em tutorial de lib específica).
- [ ] **14 - Otimizações: Image, Font, bundle, Turbopack** — `next/image` (layout/sizing/priority); `next/font` (self-hosting/zero CLS); code splitting/`dynamic()`; bundle analyzer; Turbopack (dev/build estado 2026).
- [ ] **15 - Deploy: Vercel e self-host** — Vercel-native (zero-config); `output: standalone` + Dockerfile; env vars (`NEXT_PUBLIC_`); edge vs node runtime; build/`next start`; cache em self-host.
- [ ] **16 - Capstone — arquitetura, decisões e entrevista** — decision tree (Server vs Client / estratégia de render / o cache certo); anti-patterns; **legado Pages Router** (callout síntese); perguntas de entrevista + "como explicar em inglês"; **mapa de revisão do galho** (costurar wikilinks pras 15 irmãs — confirmar via `ls`).
- [ ] **Gate Magus:** commit por sub-lote; `/verificar-wikilinks`; corrigir quebras reais.

## Wave 4 — Teardown e integração

- [ ] **4.1 Criar `index.md`** do galho `Next.js/` — MOC das 3 fases (links pras 16), com seam pros galhos vizinhos (React core, TS-com-React, Ecossistema planejado).
- [ ] **4.2 Aposentar stub `Next.js.md`** — converter em ponteiro pro índice do galho (preserva `[[Next.js]]` existentes), OU redirecionar via alias no `index.md`. Confirmar quem linka `[[Next.js]]` via grep antes.
- [ ] **4.3 Atualizar `React/index.md`** — galho Next.js de ⬜ planejado → 🟩 (linkar o índice).
- [ ] **4.4 `/verificar-wikilinks 03-Dominios/Tecnologia/React/Next.js`** — 0 quebras reais.
- [ ] **4.5 Atualizar [[00-Meta/Roadmap|Roadmap]]:** domínio React — galho Next.js ✅ (3/6).
- [ ] **4.6 (Opcional) Ciclo de qualidade:** `/plantar-duvidas` → `/colher-duvidas`; `/enriquecer-nota`; `/adicionar-midia`.
- [ ] **4.7 Commit final** + `status: done` neste plano + push manual (confirmar com usuário).

---

## Self-review (cobertura do spec)

- Roster 16/16 → Waves 1–3 item a item ✓
- Baseline Next 15 + diffs 14 + horizonte 16 + cache isolável → Global Constraints + nota 07 ✓
- Fronteira React core (callout de pré-requisito, não re-ensinar) → Global Constraints (mapa de seams com paths confirmados) + notas 04/05/06/09 ✓
- Pages Router "de leve" (sem nota dedicada) → nota 02 + capstone 16 ✓
- TS-first + padrão capítulo + Feynman → Global Constraints ✓
- Índice do galho + aposentar stub + React/index + Roadmap → Wave 4 ✓
- Fora de escopo (i18n/testing/Ecossistema) → não há tarefa; respeitado ✓
- Type/naming consistency: APIs citadas (`revalidatePath`/`revalidateTag`, `generateStaticParams`, `generateMetadata`, `NextRequest`/`NextResponse`, `output: standalone`, `staleTimes`) usadas consistentemente entre notas 06/07/08/10/11/12/15 ✓
