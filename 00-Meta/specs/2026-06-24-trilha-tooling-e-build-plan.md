---
title: "Plano — Trilha Tooling e Build"
type: spec
created: 2026-06-24
updated: 2026-06-24
status: done
tags:
  - spec
  - trilha
  - tooling
  - build
---
# Plano — Trilha Tooling e Build (3 fases) — v3

## Visão

`Tecnologia/Tooling e Build` deixa de ser MOC-semente e vira **o domínio do ecossistema completo de tooling JS/TS** — não só bundlers, mas package managers, módulos, transpilação, runtime-tooling, qualidade (lint/format), monorepos, produção/CI, e o futuro (Rust/Go, IA). Padrão capítulo (~440-800+ ln, Mermaid, exemplos, "Como explicar em inglês"). Alvo: prep entrevistas, eixo frontend-web.

A tese: **tooling existe pra fechar o gap entre o que você escreve** (ESM, TS, JSX, CSS moderno, deps de terceiros) **e o que roda** (JS compatível, otimizado, empacotado, com as deps resolvidas). O eixo é o pipeline **resolver → transpilar → empacotar → otimizar → servir**, mais a camada de **gestão de dependências e qualidade** ao redor.

## Decisões fechadas (2026-06-24)

- **Escrita do ZERO com pesquisa web profunda** (não migrar texto): cada nota é nova e pesquisada (estado 2026). As 10 notas do galho `Node/Tooling e ecossistema moderno` servem só como UMA referência opcional; o conteúdo é reescrito e aprofundado.
- **`08 - Promise-based core APIs` fica no Node** (realocar p/ `Runtime e Event Loop` ou manter) — não é tooling.
- **Granularidade: mais alta** — 26 notas.
- **Pesquisa:** subagentes usam WebSearch/WebFetch pra cravar estado atual (versões, deprecações, quem substituiu quem).

## Mudanças estruturais (cleanup, APÓS escrever a trilha fresca)

1. **Remover o galho `Node/Tooling e ecossistema moderno` do Node** (exceto `08`, que fica/realoca). Os tópicos passam a viver aqui, reescritos. Atualizar MOC do Node e repointar inbounds → Tooling e Build.
2. **Absorver `Ferramentas/Vite.md`** (reescrever com pesquisa na nota de Vite); remover de Ferramentas (repoint).
3. **Criar `Biblioteca de Tooling e Build.md`** (docs Vite/webpack/Rollup, State of JS, "Tooling Report"/State of JS, oxc/Biome docs, etc.).

## Lacunas do ferramental que a v3 fecha (auditoria)
- **Gerenciadores de versão de Node** (nvm/fnm/Volta/asdf) + **corepack** → nota nova.
- **Rspack** (webpack-compat em Rust) → nota de Rust.
- **oxc/oxlint** → nota de lint + capstone.
- **Husky + lint-staged** (git hooks) → nota de lint/format.
- **Lerna + changesets** → nota de monorepo.
- **tsx/ts-node** → nota de runtime-DX.
- **Narrativa histórica** (motivo+processo pro iniciante) → nota dedicada na fase Iniciado.
- **Legados** (Grunt/Gulp/Bower/Browserify/RequireJS-AMD) → nota dedicada (o que eram, estado hoje, por que caíram, substitutos). **CRA** → nota própria.
- Fora de escopo (têm dono): Vitest/Playwright→Testes; PostCSS/autoprefixer→CSS; Storybook (workshop de componente).

## Fronteiras (anti-duplicação)

| Tema | Dono | Aqui |
|------|------|------|
| **tsc como type-checker** / project references | `TypeScript/20`,`/25` | tsc/esbuild/swc como **transpiladores** |
| **ESM×CJS como semântica da linguagem** | `TypeScript/21` | o **grafo de módulos pro bundler** e a resolução |
| **Runtime/event loop do Node** | `Node/Runtime e Event Loop` | o runtime **como ferramenta de DX** (flags, TS nativo) |
| **Build tools de outro ecossistema** (Maven/Gradle) | `Java/Build e tooling` | cross-link conceitual |
| **CSS tooling** (PostCSS, Tailwind engine) | `CSS` | menção no pipeline |
| **IA** (agentes, codegen, MCP) | `Tecnologia/IA/*` | **como a IA entra no tooling** (nota dedicada) + cross-links |

## Roster por fase (26 notas — todas `[N]` escritas do zero com pesquisa)

### 🟢 Iniciado — motivo, dependências, módulos e o pipeline (9)
1. **Por que tooling e build existem** — o gap source↔runtime; o pipeline (resolver→transpilar→bundle→otimizar→servir); o panorama 2026
2. **A evolução do tooling JS: de `<script>` ao bundler moderno** — a NARRATIVA que dá o motivo: tags `<script>` manuais → concatenação → task runners (Grunt/Gulp) → module bundlers (Browserify/webpack) → era ESM (Rollup/Vite) → era Rust/Go (esbuild/swc/Turbopack). Cada geração nasce pra resolver a dor da anterior
3. **Package managers: npm, pnpm, yarn e Bun** — modelos de `node_modules`, store do pnpm, escolha; corepack
4. **Gerenciando versões de Node** — nvm, fnm, Volta, asdf; `.nvmrc`/engines; por que importa em time/CI
5. **Semver e o grafo de dependências** — ranges, lockfiles, resolução, deps transitivas, `overrides`, `peerDependencies`
6. **ESM × CJS e o sistema de módulos** — interop, `"type": "module"`, dual packages, condicionais de export
7. **O grafo de módulos e o que é bundling** — import graph, entry/output, por que/quando bundlar (e quando não)
8. **Transpilação e targets** — Babel/SWC/esbuild/tsc; downleveling; polyfills; browserslist; strip JSX/TS
9. **Dev server e HMR** — dev × prod; ESM nativo + esbuild (modelo Vite); Hot Module Replacement; source maps

### 🟡 Adepto — ferramentas (legadas e modernas) e qualidade (11)
10. **Ferramentas legadas: Grunt, Gulp, Bower, Browserify, RequireJS/AMD** — o que eram, **estado hoje**, por que caíram, o que as substituiu
11. **webpack — o veterano** — entry/output/loaders/plugins; por que dominou e por que perde espaço; onde ainda importa
12. **Create React App e a era dos scaffolders** — CRA: ascensão e **descontinuação** (2025); `create-vite`/`create-next-app`; por que o scaffolder opinativo morreu
13. **Vite a fundo** — dois motores (esbuild dev, Rollup build), config, plugins, assets *(absorve `Ferramentas/Vite.md`)*
14. **Rollup, esbuild e Rolldown** — Rollup pra libs/output formats; esbuild como motor (Go); Rolldown (Rust, futuro motor do Vite)
15. **Turbopack, Rspack e a corrida Rust/Go** — bundlers em Rust; webpack-compat (Rspack); por que o ecossistema migrou de linguagem
16. **Linting, formatting e git hooks** — ESLint (flat config), Prettier, Biome, oxlint; Husky + lint-staged; papel em CI; type-aware lint
17. **Otimização de bundle** — tree-shaking (e o que o impede), code splitting, lazy loading, `sideEffects`, análise, minificação
18. **O runtime como ferramenta de DX** — `--watch`, `--env-file`, TS nativo (strip types); tsx/ts-node
19. **Test runner nativo (`node:test`) e o cenário de test tooling** — runner embutido vs Vitest/Jest (linka `Engenharia/Testes`)
20. **Bun como runtime e toolkit all-in-one** — runtime + pm + bundler + test; quando vale, quando não

### 🔴 Magus — escala, produção, futuro (6)
21. **Monorepos: workspaces, Turborepo, Nx, Lerna/changesets** — workspaces; orquestração e caching de tasks; versionamento/publish
22. **Single Executable Apps (SEA) e empacotamento** — empacotar um app num binário
23. **Build em produção, CI e determinismo** — build reprodutível, cache, artefatos, env/secrets, source maps em prod
24. **Supply chain e segurança de dependências** — integridade de lockfile, `npm audit`, provenance, typosquatting (linka `Engenharia/Segurança`, `Node/Segurança`)
25. **IA no tooling e build** — agentes que configuram/migram build, codegen, lint/review por IA, MCP no dev loop; o que muda e o que não (linka `IA/Anatomia de Agents`, `IA/Agentes de Codificação`, `IA/AI Engineering Stack`)
26. **Decision tree, futuro e entrevista (capstone)** — que ferramenta pra que projeto (app/lib/monorepo); consolidação (Vite+Rolldown, oxc); perguntas de entrevista + "como explicar em inglês" + mapa de revisão

**Total: 26 notas** (9/11/6). Todas novas, com pesquisa web.

## Sequência de execução

1. **Escrever a trilha fresca** (com pesquisa), em ondas por fase, revisão entre fases. Criar `Biblioteca de Tooling e Build`.
2. **Cleanup estrutural** (commit próprio, no fim): remover galho `Node/Tooling e ecossistema moderno` (exceto `08`, realocada), absorver/remover `Ferramentas/Vite.md`, repointar inbounds, atualizar MOCs de Node/Ferramentas/Tooling. Verificar 0 quebras.
3. MOC por fase.

## Status final — COMPLETA (2026-06-24)

Trilha **26/26 feita, escrita do zero com pesquisa web, e pushada** (público).

- 🟢 Iniciado 9/9 — commit `8181909`
- 🟡 Adepto 11/11 — commit `37322ff`
- 🔴 Magus 6/6 — commit `a0637fa` (21 Monorepos · 22 SEA · 23 Build/CI · 24 Supply chain · 25 IA no tooling · 26 capstone entrevista). ~3.880 linhas, ~26 diagramas Mermaid.
- ♻️ Cleanup estrutural — commit `34d043a`: galho `Node/Tooling e ecossistema moderno` **promovido a domínio próprio** (extinto do Node). Nota `08 - Promise-based core APIs` realocada p/ `Node/Runtime e Event Loop/13` (é stdlib async, não tooling — decisão revista vs. checkpoint, que supunha nº 11 livre; galho já ia até 12). Stub `Ferramentas/Vite.md` removido (reescrito na nota 13 - Vite a fundo). Inbounds repointados: Node MOC + tronco `Node.js.md`, `Segurança/index` + `Segurança/01`, `Ferramentas/index`, `Senda Frontend`. Node passou de 9→8 galhos (numeração 8/9 de Segurança/Integrações mantida, com nota de graduação — sem renumerar internals).
- Checker: 0 quebras reais. Resíduos = falso-positivo `[[index]]` (ambíguo, Obsidian resolve local) + 1 quebra pré-existente alheia em `02 - Sequelize`.
- Biblioteca de Tooling e Build criada (na fase Iniciado).

## Decisões — todas fechadas (ver acima).

## Âncoras
- Padrões: [[project_trilhas_fases_aprendizado]], [[feedback_padrao_capitulo_livro]], [[feedback_notas_profundas_diagramas]], [[feedback_notas_atomicas]] (teto 2400), [[project_artefatos_dominio]], [[project_camadas_reorg]].
