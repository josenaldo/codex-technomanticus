---
title: "Tooling e ecossistema moderno"
created: 2026-05-12
updated: 2026-05-12
type: moc
status: growing
publish: true
tags:
  - node
  - tooling
  - ecossistema
  - package-manager
  - esm
  - typescript
  - moc
aliases:
  - Tooling Node
  - Galho 7 - Tooling
---

# Tooling e ecossistema moderno

> [!abstract] TL;DR
> Galho 7 da trilha Node Senior. Em 2026, o ecossistema de ferramentas Node evoluiu radicalmente: há 4 package managers competindo (npm v10, pnpm v9, yarn v4 Berry, Bun) com filosofias distintas de lockfile, hoisting e performance. O Node 22+ suporta TypeScript nativo via strip types — sem transpilação em dev. O test runner embutido (`node:test`) elimina dependências externas para testes unitários simples. Flags de DX como `--watch`, `--env-file` e `--import` reduzem boilerplate de setup. Single Executable Apps (SEA) empacotam Node + app em um único binário distribuível. E o Bun, adotado internamente pela Anthropic como runtime alternativo, oferece startup ~3× mais rápido com API compatível com Node.

## Sobre este galho

Este galho cobre a **camada de ferramentas** que envolve qualquer projeto Node.js moderno — desde a escolha do package manager até o empacotamento final para distribuição. O objetivo não é descrever cada ferramenta em detalhes de API, mas sim construir o **modelo mental de decisão**: quando usar pnpm vs npm vs Bun, como o ESM e CJS coexistem sem erros de interop, o que "TypeScript nativo" realmente significa no Node 22+, e quais features do runtime eliminam dependências externas.

O escopo inclui: package managers e lockfiles, semver e estratégias de atualização segura, módulos ESM/CJS (o problema de interop mais comum em 2024-2026), TypeScript via `--experimental-strip-types` e `--transform-types`, test runner built-in, flags de DX modernos, Single Executable Apps, Promise-based core APIs (fs, readline, timers/promises) e Bun como runtime alternativo para CLIs e edge workloads.

**Audiência primária:** dev senior em preparação para entrevista internacional. Cada nota inclui seção "Em entrevista" com frase pronta em inglês e vocabulário PT→EN para discussão técnica fluente.

**Audiência secundária:** dev modernizando toolchain de projeto Node existente — migrando de CommonJS para ESM, adotando TypeScript sem build step, ou avaliando troca de npm por pnpm/Bun para reduzir tempo de CI.

**Pré-requisitos:**
- [[JavaScript/Backend/Node.js|Node.js]] — tronco da trilha, conceitos fundamentais de Node
- [[03-Dominios/Node/Runtime e Event Loop/index|Runtime e Event Loop]] — galho 1, modelo mental de event loop (pressuposto ao longo de todo este galho)

## Comece por aqui — trilha completa (10 notas)

### Bloco A — Fundação

| # | Nota | O que você aprende |
|---|------|--------------------|
| 1 | [[01 - Package managers - npm, pnpm, yarn e bun]] | Diferenças de hoisting, lockfile, workspace; quando migrar |
| 2 | [[02 - Semver e gerenciamento de dependências]] | Ranges, peer deps, audit, estratégia de atualização segura |

### Bloco B — Módulos e linguagem

| # | Nota | O que você aprende |
|---|------|--------------------|
| 3 | [[03 - ESM vs CJS - módulos no Node moderno]] | Interop, `"type": "module"`, dual package, erros comuns |
| 4 | [[04 - TypeScript nativo - strip types e integração]] | `--experimental-strip-types`, `--transform-types`, tsconfig mínimo |

### Bloco C — Developer Experience

| # | Nota | O que você aprende |
|---|------|--------------------|
| 5 | [[05 - Built-in test runner - node-test]] | `node:test`, assert, mock, coverage sem Jest/Vitest |
| 6 | [[06 - DX flags modernos - watch, env-file e import]] | `--watch`, `--env-file`, `--import`, `--require` |

### Bloco D — Features avançadas

| # | Nota | O que você aprende |
|---|------|--------------------|
| 7 | [[07 - Single Executable Apps (SEA)]] | Empacotar Node + app em binário único; postject |
| 8 | [[08 - Promise-based core APIs]] | `fs/promises`, `readline/promises`, `timers/promises` |
| 9 | [[09 - Bun como runtime alternativo]] | Bun vs Node: startup, JSX, SQLite embutido, compatibilidade |

### Bloco E — Fechamento

| # | Nota | O que você aprende |
|---|------|--------------------|
| 10 | [[10 - Cheatsheet e decision tree de tooling]] | Decision tree de package manager, runtime e módulo; quick reference |

## Rotas alternativas

> [!tip] Rota entrevista (01 → 03 → 04 → 10)
> Foco em perguntas clássicas de entrevista senior: package managers, ESM/CJS, TypeScript nativo e decision tree. Cobre os tópicos mais cobrados em ~4 notas.

> [!tip] Rota modernização de projeto (02 → 03 → 04 → 06)
> Para quem precisa modernizar um projeto legado: semver seguro, migração ESM, adoção de TypeScript e DX flags sem mudar o runtime.

> [!tip] Rota DX completo (05 → 06 → 07 → 08)
> Para quem quer eliminar dependências externas: test runner nativo, flags de dev, SEA para distribuição e Promise APIs sem wrappers.

> [!tip] Rota Bun (09 → 10)
> Para quem avalia trocar o runtime: entende o que Bun oferece e usa o decision tree para decidir se a troca faz sentido no projeto atual.

## Todas as notas

```dataview
TABLE status, updated
FROM "03-Dominios/Node/Tooling e ecossistema moderno"
WHERE type = "concept"
SORT file.name ASC
```

## Veja também

- [[JavaScript/Backend/Node.js|Node.js]] — tronco da trilha Node Senior
- [[03-Dominios/Node/index|Node.js (MOC central)]] — visão geral de todos os galhos
- [[03-Dominios/Node/Runtime e Event Loop/index|Runtime e Event Loop]] — galho 1, modelo mental de event loop
- [[03-Dominios/Node/Frameworks e arquitetura/index|Frameworks e arquitetura]] — galho 4, Express, NestJS, Fastify, Hono
