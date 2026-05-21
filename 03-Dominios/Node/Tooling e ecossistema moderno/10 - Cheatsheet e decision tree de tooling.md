---
title: "Cheatsheet e decision tree de tooling"
created: 2026-05-12
updated: 2026-05-12
type: concept
status: seedling
progresso: andamento
publish: false
tags:
  - node
  - tooling
  - cheatsheet
  - decision-tree
aliases:
  - Cheatsheet Tooling Node
  - Decision Tree Tooling
---

# Cheatsheet e decision tree de tooling

> [!abstract] TL;DR
> Referência rápida de decisão para o ecossistema de tooling Node.js em 2026 — 5 decision trees cobrindo package manager, sistema de módulos, TypeScript, test runner e runtime alternativo. Inclui cheatsheet completo de flags CLI do Node, template de scripts para `package.json`, comparativo consolidado de package managers e exemplo de dual exports para bibliotecas. Use esta nota como folha de cola em entrevistas técnicas e como checklist de setup em projetos novos — ela agrega as decisões chave das 9 notas anteriores do galho em um único ponto de consulta rápida.

## Decision Trees

### Escolha de package manager

| Situação | Recomendação |
|----------|-------------|
| Projeto novo sem restrições | pnpm v9 |
| Deploy serverless / velocidade máxima de install | Bun |
| Compatibilidade máxima / equipe avessa a mudança | npm v10 |
| Zero-installs / CI sem step de install | yarn v4 Berry (PnP) |

> Ver [[01 - Package managers - npm, pnpm, yarn e bun]] para análise detalhada de cada opção.

### ESM vs CJS

| Situação | Recomendação |
|----------|-------------|
| Novo projeto | `"type": "module"` (ESM puro) |
| Biblioteca com dual publish | `exports` field com `"import"` e `"require"` |
| Legado com `require()` por todo lado | manter CJS, migrar gradualmente |
| Lib para edge runtimes (Cloudflare, Deno) | ESM puro |

> Ver [[03 - ESM vs CJS - módulos no Node moderno]] para guia de migração e dual package hazard.

### TypeScript em Node

| Situação | Recomendação |
|----------|-------------|
| Dev rápido sem enum/namespace | `node --experimental-strip-types` |
| Precisa de enums ou decorators | `--experimental-transform-types` (Node 22.7+) ou `tsx` (fallback) |
| Node 24+ (estável) | strip-types sem flag experimental |
| CI/build de produção | `tsc --noEmit` + `tsx` ou `esbuild` para bundle |

> Ver [[04 - TypeScript nativo - strip types e integração]] para comparativo completo de abordagens.

### Test runner

| Situação | Recomendação |
|----------|-------------|
| Sem deps extras, testes unitários simples | `node:test` |
| Snapshot, coverage rico, JSDOM | Vitest |
| Projeto legado com Jest | manter Jest ou migrar para Vitest |

> Ver [[05 - Built-in test runner - node-test]] para guia do `node:test` nativo.

### Runtime alternativo

| Situação | Recomendação |
|----------|-------------|
| Performance máxima + TypeScript nativo + startup rápido | Bun |
| Compatibilidade máxima com ecossistema Node | Node.js |
| Edge runtime (Cloudflare Workers) | Workerd/Miniflare |
| Segurança por padrão, Deno Deploy | Deno |

> Ver [[09 - Bun como runtime alternativo]] para benchmark e trade-offs de Bun vs Node.

## Cheatsheet de flags CLI

| Flag | Propósito | Exemplo |
|------|-----------|---------|
| `--watch` | Reinicia ao salvar | `node --watch server.js` |
| `--env-file` | Carrega .env sem dotenv | `node --env-file .env app.js` |
| `--import` | Pré-carrega módulo (ESM) | `node --import ./setup.js app.js` |
| `--require` | Pré-carrega módulo (CJS) | `node --require ts-node/register app.ts` |
| `--inspect` | Debug (attach Chrome) | `node --inspect server.js` |
| `--inspect-brk` | Debug pausado no início | `node --inspect-brk server.js` |
| `--max-old-space-size` | Limite de heap V8 | `node --max-old-space-size=4096 app.js` |
| `--experimental-strip-types` | TypeScript sem build | `node --experimental-strip-types app.ts` |
| `--experimental-transform-types` | TypeScript com enum/decorators | `node --experimental-transform-types app.ts` |
| `--enable-source-maps` | Source maps no stack trace | `node --enable-source-maps dist/app.js` |
| `--test` | Executa test runner | `node --test **/*.test.js` |
| `--test-reporter` | Formato dos resultados | `node --test --test-reporter=spec` |
| `--watch` com `--test` | Watch para testes | `node --test --watch` |

> Ver [[06 - DX flags modernos - watch, env-file e import]] para exemplos práticos e casos de uso avançados.

## Template de scripts

Template para projetos Node.js + TypeScript modernos. Cobre os cenários mais comuns de desenvolvimento, build, testes e qualidade de código:

```json
{
  "scripts": {
    "dev": "node --watch --experimental-strip-types --env-file .env src/index.ts",
    "dev:debug": "node --inspect --watch --experimental-strip-types src/index.ts",
    "build": "tsc --noEmit && esbuild src/index.ts --bundle --platform=node --outfile=dist/index.js",
    "start": "node dist/index.js",
    "test": "node --experimental-strip-types --test src/**/*.test.ts",
    "test:watch": "node --experimental-strip-types --test --watch src/**/*.test.ts",
    "test:coverage": "node --experimental-strip-types --test --experimental-test-coverage src/**/*.test.ts",
    "lint": "eslint src/",
    "typecheck": "tsc --noEmit"
  }
}
```

**Pontos-chave deste template:**

- `dev` usa `--watch` nativo (sem nodemon), `--experimental-strip-types` (sem ts-node) e `--env-file` (sem dotenv).
- `dev:debug` adiciona `--inspect` para attach com Chrome DevTools ou VS Code.
- `build` executa `tsc --noEmit` para typecheck puro antes de empacotar com `esbuild`.
- `test:coverage` usa o coverage nativo do Node (`--experimental-test-coverage`), sem Istanbul.
- Nenhum `ts-node`, `nodemon` ou `dotenv` como dependência de runtime.

## Comparativo de package managers

Resumo das características principais para decisão rápida:

| | npm v10 | pnpm v9 | yarn v4 Berry | Bun |
|-|---------|---------|--------------|-----|
| **Lockfile** | `package-lock.json` | `pnpm-lock.yaml` | `.yarn/cache` + `yarn.lock` | `bun.lockb` (binário) |
| **Hoisting** | Flat (default) | Strict (symlinks) | PnP (sem node_modules) | Flat |
| **Workspace** | Sim | Sim (catalogs) | Sim | Sim |
| **Performance** | Referência | 2-3× mais rápido | PnP elimina I/O | 10-25× mais rápido |
| **Nota detalhada** | [[01 - Package managers - npm, pnpm, yarn e bun\|Ver nota]] | [[01 - Package managers - npm, pnpm, yarn e bun\|Ver nota]] | [[01 - Package managers - npm, pnpm, yarn e bun\|Ver nota]] | [[09 - Bun como runtime alternativo\|Ver nota]] |

**Resumo de quando escolher cada um:**

- **npm**: equipe conservadora, CI já configurado, sem tempo para migração.
- **pnpm**: projetos novos — evita phantom deps por padrão, monorepos com catalogs.
- **yarn Berry (PnP)**: zero-installs em CI, projetos que precisam de reprodutibilidade total.
- **Bun**: velocidade de install como prioridade, projetos TypeScript-first sem equipe grande.

## Dual exports — exemplo

Configuração de `exports` field para publicar biblioteca com suporte simultâneo a CJS e ESM:

```json
{
  "name": "minha-lib",
  "exports": {
    ".": {
      "import": "./dist/index.mjs",
      "require": "./dist/index.cjs",
      "types": "./dist/index.d.ts"
    }
  }
}
```

Veja [[03 - ESM vs CJS - módulos no Node moderno]] para o guia completo de dual package hazard — incluindo como evitar que o estado seja duplicado quando consumidores misturam `require()` e `import()` na mesma aplicação.

## Armadilhas comuns

### Misturar `"type": "module"` com `require()` sem transição planejada

```js
// ❌ Problema: adicionar "type": "module" ao package.json sem atualizar imports
// Arquivo: src/utils.js
// const fs = require('fs');           → SyntaxError: require is not defined in ES module scope
// const config = require('./config.json');   → mesmo erro em todos os require()

// ✅ Fix: migrar require() para import/import() gradualmente
// import fs from 'node:fs';
// import config from './config.json' assert { type: 'json' };
// Ou manter CJS (sem "type": "module") e migrar arquivo por arquivo usando .mjs
// Estratégia segura: renomear arquivos ESM para .mjs enquanto mantém .js em CJS
```

### Usar `--experimental-strip-types` com enums TypeScript

```js
// ❌ Problema: código com enum não funciona com strip-types puro
// enum Status { Active = 'active', Inactive = 'inactive' }
// node --experimental-strip-types app.ts
// → SyntaxError: TypeScript enum is not supported in strip-only mode

// ✅ Fix 1: adicionar --experimental-transform-types para suporte a enums/namespaces
// node --experimental-transform-types app.ts

// ✅ Fix 2 (preferível a longo prazo): migrar enums para const objects
// const Status = { Active: 'active', Inactive: 'inactive' } as const;
// type Status = typeof Status[keyof typeof Status];
// → sem flags extras, compatível com strip-types puro e tree-shaking
```

### Confundir `--import` com `--require` em projetos ESM

```js
// ❌ Problema: usar --require em projeto com "type": "module"
// node --require ./setup.cjs server.js
// setup.cjs não pode usar import/export — é forçado a ser CJS
// Gera conflito de contexto quando setup precisa de módulos ESM

// ✅ Fix: usar --import para projetos ESM (carrega arquivo ESM antes do entry point)
// node --import ./setup.js server.js
// setup.js pode usar import/export normalmente como qualquer módulo ESM
// Para compatibilidade com ambos os sistemas, --require ainda é válido em CJS
// Regra de ouro: --import para ESM, --require para CJS
```

### Usar `node:test` sem entender o modelo de subtests

```js
// ❌ Problema: criar subtests sem await — race condition silenciosa
import { test } from 'node:test';
import assert from 'node:assert/strict';

// test('validar usuário', (t) => {
//   t.test('nome obrigatório', () => { ... });   // subtest não awaited
//   t.test('email válido', () => { ... });       // pode não executar antes do pai terminar
// });

// ✅ Fix: sempre await subtests e usar async/await consistentemente
test('validar usuário', async (t) => {
  await t.test('nome obrigatório', () => {
    assert.throws(() => criarUsuario({ nome: '' }));
  });
  await t.test('email válido', () => {
    assert.doesNotThrow(() => criarUsuario({ nome: 'Ana', email: 'ana@ex.com' }));
  });
});
```

## Em entrevista

**P: Como você escolhe um package manager para um novo projeto em 2026?**

For a new project without constraints, I default to pnpm v9 because of its strict hoisting model — packages can only import what they explicitly declare in their `package.json`, which prevents accidental phantom dependency bugs that can surface in production but not locally. If the project is serverless or CLI-heavy where install speed matters, I'd evaluate Bun, which is 10-25x faster at cold installs. I'd only choose npm if the team strongly prefers maximum ecosystem compatibility or if there are CI/CD scripts tightly coupled to npm's exact behavior.

---

**P: Qual a diferença entre ESM e CJS e quando você usaria cada um?**

CommonJS (CJS) is the original Node.js module system using `require()` and `module.exports`, while ECMAScript Modules (ESM) is the modern standard using `import`/`export`. For a new project, I always choose ESM because it is the web standard and enables static analysis, tree shaking, and top-level `await`. The main challenge is interop: CJS can import ESM only asynchronously via dynamic `import()`, but ESM cannot `require()` CJS — you need careful `exports` configuration for shared libraries. For legacy codebases with deep `require()` usage, I prefer a gradual migration strategy using `.mjs` extensions rather than a big-bang switch.

---

**P: O que mudou no Node.js com o suporte nativo a TypeScript via strip types?**

Node 22.6+ introduced the `--experimental-strip-types` flag, which allows running `.ts` files directly by stripping type annotations at parse time — no transpilation, no `ts-node`, no build step during development. This eliminates a major source of toolchain friction: developers no longer need to configure TypeScript compilation just to run a file. The key limitation is that TypeScript features that require actual code transformation — like enums, decorators, and `const enum` — are not supported without the additional `--experimental-transform-types` flag. In Node 24, strip-types became stable, so this is the direction the ecosystem is moving toward as the default development experience.

---

**P: Quando você usaria o test runner nativo do Node vs Vitest?**

I reach for `node:test` when I want zero external dependencies and my tests are purely unit tests without browser simulation or snapshot testing — the built-in runner is sufficient for most API and library testing scenarios. I switch to Vitest when I need richer features like snapshot testing, JSDOM for DOM emulation, or a more ergonomic watch mode with better UI feedback. For legacy codebases already on Jest, I weigh the migration cost carefully — Vitest is largely Jest-compatible, but the migration still requires adjusting configuration and verifying mocks. The bottom line is that `node:test` is a serious option in 2026 that most teams overlook because they default to Jest out of habit.

---

**P: Como você explicaria a diferença entre `--import` e `--require` no Node.js?**

Both flags preload a module before the entry point executes, but they operate in different module systems. `--require` is the legacy flag that loads a CommonJS module — it's synchronous and runs before anything else, which is why it was commonly used for TypeScript registration with `ts-node/register`. `--import` is the ESM equivalent: it loads an ES module asynchronously before the entry point, which means the preloaded file can use `import`/`export` freely. The practical rule is: if your project uses `"type": "module"`, use `--import`; if it's CommonJS, `--require` still works fine. Mixing them carelessly — for example, using `--require` with an ESM-only setup module — leads to subtle context isolation bugs that are hard to diagnose.

## Vocabulário consolidado

| PT | EN |
|----|----|
| gerenciador de pacotes | package manager |
| sistema de módulos | module system |
| elevação de dependências | dependency hoisting |
| dependência fantasma | phantom dependency |
| resolução de módulo | module resolution |
| árvore de decisão | decision tree |
| fila de tarefas | task pipeline |
| compilação incremental | incremental compilation |
| verificação de tipos | type checking |
| empacotador | bundler |
| transpilador | transpiler |
| cobertura de código | code coverage |
| publicação dupla | dual publish |
| remoção de anotações | type stripping |
| app executável único | single executable app |

## Veja também

- [[Tooling e ecossistema moderno]] — MOC do galho
- [[01 - Package managers - npm, pnpm, yarn e bun]]
- [[02 - Semver e gerenciamento de dependências]]
- [[03 - ESM vs CJS - módulos no Node moderno]]
- [[04 - TypeScript nativo - strip types e integração]]
- [[05 - Built-in test runner - node-test]]
- [[06 - DX flags modernos - watch, env-file e import]]
- [[07 - Single Executable Apps (SEA)]]
- [[08 - Promise-based core APIs]]
- [[09 - Bun como runtime alternativo]]
- [[Node.js]]
- [[03-Dominios/Node/index|Node.js (MOC central)]]
