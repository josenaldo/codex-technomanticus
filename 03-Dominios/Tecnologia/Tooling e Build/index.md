---
title: "Tooling e Build"
type: moc
publish: true
created: 2026-06-23
updated: 2026-06-24
status: growing
tags:
  - moc
  - tooling
  - build
aliases:
  - Tooling e Build
  - Build Tools
---
# Tooling e Build

> [!abstract] TL;DR
> O ecossistema completo de tooling JS/TS, em 3 fases. A tese: **tooling existe pra fechar o gap entre o que você escreve** (ESM, TS, JSX, CSS moderno, deps de terceiros) **e o que roda** (JS compatível, otimizado, empacotado). O eixo é o pipeline **resolver → transpilar → empacotar → otimizar → servir**, mais a camada de dependências e qualidade ao redor.

Da gestão de dependências aos bundlers, passando por transpilação, qualidade (lint/format), monorepos e o futuro (Rust/Go, IA). A linguagem vive em [[03-Dominios/Tecnologia/JavaScript/index|JavaScript]] e [[03-Dominios/Tecnologia/TypeScript/index|TypeScript]]; aqui é a maquinaria que transforma esse código em algo que roda.

## 🟢 Iniciado — motivo, dependências, módulos e o pipeline

- [[01 - Por que tooling e build existem]] — o gap source↔runtime e o pipeline
- [[02 - A evolução do tooling JS - de script ao bundler moderno]] — a narrativa: por que cada geração nasceu
- [[03 - Package managers - npm, pnpm, yarn e Bun]] — node_modules, store do pnpm, escolha
- [[04 - Gerenciando versões de Node]] — nvm/fnm/Volta/mise, corepack
- [[05 - Semver e o grafo de dependências]] — ranges, lockfiles, resolução
- [[06 - ESM e CJS e o sistema de módulos]] — interop, exports, resolução pro bundler
- [[07 - O grafo de módulos e o que é bundling]] — o coração conceitual
- [[08 - Transpilação e targets]] — Babel/SWC/esbuild/tsc, downleveling, polyfills
- [[09 - Dev server e HMR]] — dev × prod, ESM nativo, Hot Module Replacement

## 🟡 Adepto — as ferramentas (legadas e modernas) e a qualidade *(a escrever)*

- 10 — Ferramentas legadas: Grunt, Gulp, Bower, Browserify, RequireJS/AMD
- 11 — webpack — o veterano
- 12 — Create React App e a era dos scaffolders
- 13 — Vite a fundo
- 14 — Rollup, esbuild e Rolldown
- 15 — Turbopack, Rspack e a corrida Rust/Go
- 16 — Linting, formatting e git hooks
- 17 — Otimização de bundle
- 18 — O runtime como ferramenta de DX
- 19 — Test runner nativo (node:test) e o cenário de testes
- 20 — Bun como runtime e toolkit all-in-one

## 🔴 Magus — escala, produção, futuro *(a escrever)*

- 21 — Monorepos: workspaces, Turborepo, Nx e changesets
- 22 — Single Executable Apps (SEA) e empacotamento
- 23 — Build em produção, CI e determinismo
- 24 — Supply chain e segurança de dependências
- 25 — IA no tooling e build
- 26 — Decision tree, futuro e entrevista (capstone)

## Referência

- [[Biblioteca de Tooling e Build]] — recursos externos curados (docs, State of JS, blogs)

## Veja também

- [[03-Dominios/Tecnologia/JavaScript/index|JavaScript]] · [[03-Dominios/Tecnologia/TypeScript/index|TypeScript]]
- [[03-Dominios/Tecnologia/Node/index|Node]] · [[03-Dominios/Tecnologia/React/index|React]]
- [[03-Dominios/Ciência/Compiladores e Linguagens/index|Compiladores e Linguagens]] — a teoria por trás da transpilação
