---
title: "Next.js"
type: moc
publish: true
created: 2026-06-27
updated: 2026-06-27
status: evergreen
tags:
  - react
  - nextjs
  - app-router
  - moc
aliases:
  - Next.js
  - Next.js (galho)
  - App Router
---

# Next.js (App Router)

> [!abstract] TL;DR
> O galho do **framework** que completa o domínio React: como o Next.js cabeia React Server Components, Actions e Suspense numa aplicação full-stack real, em 3 fases (Iniciado/Adepto/Magus), **TS-first**, baseline **Next 15 / React 19**. Next.js é **complemento do React** — o [[03-Dominios/Tecnologia/React/React core/index|React core]] é pré-requisito: aqui não se re-ensina a primitiva, mostra-se o cabeamento (file-system routing, Server Actions em `<form>`, o modelo de 4 caches, streaming via `loading.tsx`, deploy). Diferenças do Next 14 ficam em callouts `[!warning]`; o horizonte do Next 16 (`'use cache'`) em `[!info]`.

## 🟢 Iniciado — o modelo mental

- [[03-Dominios/Tecnologia/React/Next.js/01 - O que é o Next.js e por que existe|01 - O que é o Next.js e por que existe]] — meta-framework sobre React; o que resolve; App Router como padrão; quando NÃO usar
- [[03-Dominios/Tecnologia/React/Next.js/02 - App Router vs Pages Router|02 - App Router vs Pages Router]] — file-system routing; o salto de paradigma; o Pages Router legado de leve
- [[03-Dominios/Tecnologia/React/Next.js/03 - Estrutura de rotas - layouts, pages, loading, error|03 - Estrutura de rotas: layouts, pages, loading, error]] — arquivos especiais; nested layouts; route groups; rotas dinâmicas
- [[03-Dominios/Tecnologia/React/Next.js/04 - Server vs Client Components|04 - Server vs Client Components]] — o conceito central; o boundary `'use client'`; composição server/client
- [[03-Dominios/Tecnologia/React/Next.js/05 - Data fetching no Server|05 - Data fetching no Server]] — `async` components; `fetch` no server; waterfalls vs paralelo; request memoization

## 🟡 Adepto — o dia a dia em produção

- [[03-Dominios/Tecnologia/React/Next.js/06 - Server Actions e mutations|06 - Server Actions e mutations]] — `'use server'`; `<form action>`; `revalidatePath`/`revalidateTag`; segurança
- [[03-Dominios/Tecnologia/React/Next.js/07 - O modelo de caching do Next 15|07 - O modelo de caching do Next 15]] — os 4 caches; uncached-by-default; diffs do 14; horizonte `'use cache'` (16)
- [[03-Dominios/Tecnologia/React/Next.js/08 - Rendering strategies - SSR, SSG, ISR, PPR|08 - Rendering strategies: SSR, SSG, ISR, PPR]] — estático vs dinâmico; `generateStaticParams`; ISR; PPR
- [[03-Dominios/Tecnologia/React/Next.js/09 - Streaming, Suspense e loading.tsx|09 - Streaming, Suspense e loading.tsx]] — streaming SSR; `loading.tsx` como Suspense automático; UX progressiva
- [[03-Dominios/Tecnologia/React/Next.js/10 - Route Handlers e APIs|10 - Route Handlers e APIs]] — `route.ts`; métodos HTTP; handler vs Server Action
- [[03-Dominios/Tecnologia/React/Next.js/11 - Metadata, SEO e assets sociais|11 - Metadata, SEO e assets sociais]] — Metadata API; `generateMetadata`; OG images; sitemap/robots
- [[03-Dominios/Tecnologia/React/Next.js/12 - Navegação e o Router|12 - Navegação e o Router]] — `<Link>` e prefetch; `useRouter`; soft vs hard navigation; `staleTimes`

## 🔴 Magus — borda, produção e síntese

- [[03-Dominios/Tecnologia/React/Next.js/13 - Middleware e auth na borda|13 - Middleware e auth na borda]] — `middleware.ts`; Edge runtime; proteção de rota; defense-in-depth
- [[03-Dominios/Tecnologia/React/Next.js/14 - Otimizações - Image, Font, bundle, Turbopack|14 - Otimizações: Image, Font, bundle, Turbopack]] — `next/image`; `next/font`; `dynamic()`; Turbopack; Core Web Vitals
- [[03-Dominios/Tecnologia/React/Next.js/15 - Deploy - Vercel e self-host|15 - Deploy: Vercel e self-host]] — Vercel zero-config; `output: standalone` + Docker; edge vs node; env vars
- [[03-Dominios/Tecnologia/React/Next.js/16 - Capstone - arquitetura, decisões e entrevista|16 - Capstone: arquitetura, decisões e entrevista]] — decision trees; anti-patterns; legado Pages Router; entrevista; mapa de revisão

## Veja também

- [[03-Dominios/Tecnologia/React/React core/index|React core]] — a biblioteca (RSC, Actions, Suspense — as primitivas que o Next cabeia)
- [[03-Dominios/Tecnologia/React/TypeScript com React/index|TypeScript com React]] — tipagem de componentes e hooks
- [[03-Dominios/Tecnologia/React/Design Patterns/index|React Design Patterns]] — catálogo de padrões
- [[03-Dominios/Tecnologia/React/Dicionário de React|Dicionário de React]] — glossário do domínio
- [[03-Dominios/Tecnologia/React/index|React (domínio)]]
