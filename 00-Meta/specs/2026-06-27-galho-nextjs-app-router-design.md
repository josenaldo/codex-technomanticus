---
title: "Spec — Galho Next.js (App Router)"
type: spec
status: approved
created: 2026-06-27
updated: 2026-06-27
tags:
  - spec
  - react
  - nextjs
  - planejamento
---

# Spec — Galho Next.js (App Router)

> [!abstract] TL;DR
> Terceiro galho construído do domínio React (depois de React core e Design Patterns): **Next.js com foco no App Router a fundo + Pages Router de leve**, **16 notas atômicas** em 3 fases (Iniciado/Adepto/Magus), **TS-first**, baseline **Next 15 / React 19**. É um **complemento do React** — exige o React core como pré-requisito e não re-ensina primitivas (RSC, Actions, Suspense), apenas cabeia como o framework as usa. Capstone de entrevista no fim.

## Contexto e objetivo

- **Domínio:** `03-Dominios/Tecnologia/React/Next.js/` (novo galho, irmão de `React core/` e `Design Patterns/`).
- **Perfil-alvo:** Senior Fullstack Developer, prep entrevistas internacionais remotas (frontend).
- **Posição no Roadmap:** Onda A (tripé frontend), galho 3/6 do domínio React multi-galho.
- **Padrão de execução:** brainstorming → spec (este arquivo) → writing-plans → subagente-por-nota (Sonnet), commit por sub-lote com paths explícitos, direto na `main`.

## Decisões cravadas

### Versão-alvo
- **Baseline: Next.js 15** (App Router estável, React 19, Turbopack).
- **Caching escrito no modelo do 15** ("uncached by default": `fetch` e Route Handlers GET não cacheados por padrão; `staleTimes`).
- Diferenças do **Next 14** marcadas em callouts `[!warning]` (entrevista e código legado batem nisso).
- O que vem no **Next 16** (`'use cache'` / cache components saindo de canary) sinalizado como horizonte em callouts `[!info]`/`[!warning]`.
- **Estruturar as notas para promover o baseline pro 16 ser troca cirúrgica**, não reescrita: isolar o que é específico do modelo de cache do 15 em seções/callouts identificáveis.

### Fronteira com React core (anti-duplicação)
- **React core** = a *primitiva* (a diretiva `'use server'`/`'use client'`, `useActionState`/`useOptimistic`, o modelo mental server/client, Suspense).
- **Next.js (este galho)** = como o *framework* cabeia: Server Actions em `<form>` + `revalidatePath`/`revalidateTag`, data fetching real no App Router, o boundary RSC dentro do file-system routing, streaming via `loading.tsx`.
- Cada nota que toca primitiva **abre com callout `[!info]`** linkando a nota correspondente do React core e foca no "como o Next faz".
- **Redundância entre notas é reforço** (convenção do vault): sobreposição deliberada sob a ótica do framework é permitida — linkar, não podar.

### Pages Router "de leve"
- **Sem nota dedicada.** O essencial mora na nota **02 (App Router vs Pages Router)** + um callout de "legado que você vai encontrar" no **capstone (16)**.

## Estrutura do galho — 16 notas, 3 fases

### 🟢 Iniciado — o modelo mental (5)
1. **O que é o Next.js e por que existe** — framework full-stack sobre React; o que resolve (routing, rendering, data, bundling); App Router como padrão; conceito de meta-framework.
2. **App Router vs Pages Router** — file-system routing; o salto de paradigma; **Pages Router "de leve" mora aqui** (o que é, por que ainda existe, noções de migração).
3. **Estrutura de rotas: layouts, pages, loading, error** — convenções de arquivo; nested layouts; route groups; templates; arquivos especiais.
4. **Server vs Client Components** — o conceito central do App Router; o boundary `'use client'`; árvore de RSC; quando cada um. (callout → React core)
5. **Data fetching no Server** — `async` components, `fetch` no server, composição, sequencial vs paralelo, request memoization.

### 🟡 Adepto — o dia a dia em produção (7)
6. **Server Actions e mutations** — `'use server'`, `<form action>`, `revalidatePath`/`revalidateTag`, progressive enhancement. (callout → React core Actions)
7. **O modelo de caching do Next 15** — os 4 caches (Request Memoization, Data Cache, Full Route Cache, Router Cache); **default uncached** no 15; `[!warning]` diffs do 14; horizonte `'use cache'` (16).
8. **Rendering strategies: SSR, SSG, ISR, PPR** — estático vs dinâmico; `generateStaticParams`; ISR/`revalidate`; PPR (Partial Prerendering) como ponte.
9. **Streaming, Suspense e `loading.tsx`** — streaming SSR; boundaries; UX de carregamento progressivo. (callout → React core Suspense)
10. **Route Handlers e APIs** — `route.ts`, métodos HTTP, Request/Response web-padrão, quando usar vs Server Action.
11. **Metadata, SEO e assets sociais** — Metadata API estática/dinâmica, `generateMetadata`, OG images, sitemap/robots.
12. **Navegação e o Router** — `<Link>`, `useRouter`, prefetch, `staleTimes`, navegação client-side vs server.

### 🔴 Magus — borda, produção e síntese (4)
13. **Middleware e auth na borda** — `middleware.ts`, Edge runtime, rewrites/redirects, padrões de proteção de rota.
14. **Otimizações: Image, Font, bundle, Turbopack** — `next/image`, `next/font`, code splitting, bundle analyzer, Turbopack.
15. **Deploy: Vercel e self-host** — Vercel-native; `output: standalone` + Docker; variáveis de ambiente; edge vs node runtime.
16. **Capstone — arquitetura, decisões e entrevista** — decision tree (qual estratégia/cache/component); anti-patterns; **legado Pages Router**; perguntas de entrevista; mapa de revisão do galho.

## Convenções herdadas (padrão cravado do vault)

- **Padrão capítulo de livro**: cada nota pega o leitor pela mão (não é referência/lista); exemplo trabalhado + divulgação progressiva.
- **Notas atômicas flat** ~440–540 linhas, TS-first, com **diagramas Mermaid**.
- **Registro Feynman**: analogias, perguntas retóricas, callouts, resumo em 1 linha.
- Frontmatter `fase:` (Iniciado/Adepto/Magus) + agrupamento no MOC.
- **`/verificar-nota`** por nota; **`/verificar-wikilinks`** por fase.
- **Subagente-por-nota** (Sonnet); commit por sub-lote com **paths EXPLÍCITOS** (working tree pode ter trabalho paralelo do usuário).
- **Direto na `main`** (convenção `feedback_galhos_direto_main`); push manual ao final.
- Índice MOC em `Next.js/index.md`; marco no `React/index` (🟩) e no `00-Meta/Roadmap.md`.
- **Capstone roda em paralelo com as últimas notas** → race no `ls`: checar/consertar o mapa de revisão do capstone depois.

## Fora de escopo (declarado)

- **i18n** (next-intl, App Router i18n) — não nesta rodada.
- **Testing em Next** (Playwright/Vitest com App Router) — coberto no domínio de testes, não aqui.
- **Nota dedicada de Pages Router** — fica "de leve" (ver decisão acima).
- **Ecossistema** (TanStack Query, MUI/Mantine) — é o próximo galho planejado, separado.

## Critérios de sucesso

- 16 notas escritas, todas passando `/verificar-nota` (score alvo ≥ 10/12 equivalente).
- 0 wikilinks quebrados no galho (`/verificar-wikilinks`).
- Índice MOC completo; `React/index` e Roadmap atualizados (galho 3/6 ✅).
- Caching escrito no modelo do 15 com diffs do 14 e horizonte do 16 isolados em callouts.
- Fronteira com React core respeitada: nenhuma nota re-ensina primitiva sem callout de remissão.
