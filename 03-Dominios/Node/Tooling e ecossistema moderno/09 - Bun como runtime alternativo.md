---
title: "Bun como runtime alternativo"
created: 2026-05-12
updated: 2026-05-12
type: concept
status: seedling
progresso: andamento
publish: false
tags:
  - node
  - bun
  - runtime
  - tooling
  - javascript
aliases:
  - Bun runtime
  - Bun JS
---

# Bun como runtime alternativo

> [!abstract] TL;DR
> Bun é um runtime JavaScript/TypeScript baseado em JavaScriptCore (não V8), escrito em Zig, adquirido pela Anthropic em dezembro de 2025. É o runtime mais rápido em benchmarks de I/O e startup, com TypeScript e JSX nativos sem configuração.
> Inclui runtime + package manager + bundler + test runner em um único binário — substituindo `node`, `npm`/`pnpm`, `esbuild`/`webpack` e Jest/Vitest de uma vez só.
> Compatibilidade com APIs Node.js é alta (Express, Fastify, Prisma funcionam), mas não é 100%: módulos com native addons (`.node`) e código que usa a API `v8` diretamente não são suportados — verifique antes de migrar.

## O que é

Bun foi criado por Jarred Sumner e lançado com a versão 1.0 em setembro de 2023, sendo adquirido pela Anthropic em dezembro de 2025. Seu objetivo declarado é ser um runtime JavaScript/TypeScript moderno e de alta performance, projetado como alternativa ao Node.js e ao Deno.

Enquanto o Node.js nasceu focado em I/O não-bloqueante com callbacks e foi adicionando suporte a ESM e TypeScript gradualmente, o Bun foi construído do zero com essas necessidades em mente: TypeScript e JSX funcionam nativamente sem Babel, sem `ts-node`, sem configuração extra.

**Posicionamento:**
- **vs Node.js**: mais rápido em startup e I/O; compatível com a maioria do ecossistema npm; não suporta native addons.
- **vs Deno**: menos restritivo por padrão (não exige permissões explícitas); compatibilidade melhor com código Node existente; foco em performance bruta mais do que em segurança por padrão.
- **vs apenas esbuild/tsc**: Bun não é só bundler ou transpiler — é um runtime completo que também faz bundling.

A filosofia central é **"one tool for everything"**: um único binário substitui `npm`/`npx`, `ts-node`, `jest`, `webpack`/`esbuild`. Menos ferramentas, menos conflito de versões, menos configuração.

## Como funciona

### JavaScriptCore vs V8

Bun utiliza **JavaScriptCore (JSC)**, o motor JavaScript do WebKit (o engine por trás do Safari), enquanto Node.js usa **V8**, o motor do Chrome/Chromium.

A diferença prática mais importante é o comportamento de JIT (Just-In-Time compilation):

- **JSC** tem inicialização mais rápida (cold start menor) porque o custo de compilação JIT é diferido e distribuído de forma diferente. Isso o torna ideal para processos de curta duração.
- **V8** tem um compilador JIT mais agressivo (TurboFan) que entrega maior throughput em código que roda por muito tempo, depois do warmup. Para servidores HTTP de longa duração com alto volume de requisições, V8 pode superar JSC depois de atingir velocidade de cruzeiro.

**Implicações práticas:**
| Cenário | Motor preferível |
|---------|-----------------|
| CLI, scripts, lambdas | JSC/Bun (startup importa) |
| Servidor HTTP de alta carga | V8/Node (JIT warmup se paga) |
| Dev tooling | JSC/Bun (install + build rápidos) |
| Processamento batch longo | V8/Node (throughput pós-warmup) |

### Bun como runtime

`bun run` executa arquivos JavaScript, TypeScript, JSX e TSX sem necessidade de pré-compilação ou configuração:

```js
// bun run app.ts   → TypeScript nativo, sem ts-node ou tsc
// bun run app.jsx  → JSX nativo, sem Babel
// bun app.ts       → atalho (omitindo 'run')
```

O Bun implementa as APIs Node.js mais usadas para garantir compatibilidade:

- `node:fs`, `node:fs/promises` — sistema de arquivos
- `node:path`, `node:os`, `node:url` — utilitários
- `node:http`, `node:https`, `node:net` — rede
- `node:crypto`, `node:buffer` — criptografia e buffers
- `node:stream`, `node:events`, `node:util` — streams e utilitários

Além da compatibilidade com Node, o Bun expõe suas próprias APIs de alta performance via namespace global `Bun`:

```js
// Servidor HTTP com Bun.serve()
const server = Bun.serve({
  port: 3000,
  async fetch(req) {
    const url = new URL(req.url);

    if (url.pathname === "/") {
      return new Response("Hello from Bun!", {
        headers: { "Content-Type": "text/plain" },
      });
    }

    if (url.pathname === "/json") {
      return Response.json({ runtime: "bun", version: Bun.version });
    }

    return new Response("Not Found", { status: 404 });
  },
  error(err) {
    return new Response(`Internal Error: ${err.message}`, { status: 500 });
  },
});

console.log(`Servidor rodando em http://localhost:${server.port}`);
```

Outras APIs exclusivas do Bun: `Bun.file()` (leitura lazy de arquivos), `Bun.password` (hash bcrypt nativo), `Bun.sqlite` (SQLite embutido), `Bun.redis` (cliente Redis nativo).

### Bun como package manager

O gerenciador de pacotes do Bun é 10–25× mais rápido que o npm em benchmarks de install a frio, graças a downloads paralelos, cache global em disco e um formato de lockfile binário:

```js
// Comandos equivalentes: npm → bun
// npm install              →  bun install
// npm install react        →  bun add react
// npm install -D jest      →  bun add -d jest
// npm remove lodash        →  bun remove lodash
// npm update               →  bun update
// npm run dev              →  bun run dev   (ou: bun dev)
// npx create-next-app      →  bunx create-next-app
// npm ci                   →  bun install --frozen-lockfile
```

O lockfile gerado é `bun.lockb` — um arquivo binário, não legível por humanos como o `package-lock.json`. Ele garante instalações reproduzíveis e é significativamente menor em disco, mas `git diff bun.lockb` não mostra mudanças legíveis.

O Bun é **compatível com `package.json` existente**: scripts, `dependencies`, `devDependencies`, `peerDependencies` e workspaces funcionam sem alteração.

### Bun como bundler

O Bun inclui um bundler nativo mais rápido que o esbuild (segundo benchmarks oficiais), acessado via `bun build`:

```js
// bun build src/app.ts --outdir dist
// bun build src/app.ts --outdir dist --target browser
// bun build src/app.ts --outdir dist --minify
// bun build src/app.ts --outdir dist --sourcemap external

// Targets disponíveis:
//   browser  → bundle para navegador (sem APIs Node)
//   bun      → bundle para rodar no Bun
//   node     → bundle compatível com Node.js
```

O flag `--compile` gera um binário executável autossuficiente (equivalente ao SEA do Node.js, porém mais simples de usar):

```js
// Gera um executável único: ./minha-ferramenta
// bun build src/cli.ts --compile --outfile minha-ferramenta

// O binário inclui o runtime Bun + código transpilado
// Não requer Bun instalado na máquina de destino
// Funciona em: Linux x64, macOS x64/arm64, Windows x64

// Para cross-compile:
// bun build src/cli.ts --compile --target bun-linux-x64 --outfile minha-ferramenta-linux
```

### Bun como test runner

O Bun inclui um test runner com API compatível com Jest, eliminando a necessidade de instalar e configurar Jest ou Vitest:

```js
// arquivo: src/math.test.ts
import { describe, test, expect, mock, beforeEach } from "bun:test";
import { soma, divide } from "./math";

describe("soma", () => {
  test("retorna a soma de dois números", () => {
    expect(soma(2, 3)).toBe(5);
  });

  test("funciona com negativos", () => {
    expect(soma(-1, 1)).toBe(0);
  });
});

describe("divide", () => {
  test("lança erro ao dividir por zero", () => {
    expect(() => divide(10, 0)).toThrow("divisão por zero");
  });
});

// bun test                   → roda todos os *.test.ts / *.spec.ts
// bun test --watch           → modo watch
// bun test src/math.test.ts  → roda arquivo específico
// bun test --coverage        → cobertura de código
```

A descoberta automática procura por arquivos `*.test.{js,ts,jsx,tsx}` e `*.spec.{js,ts,jsx,tsx}`. O runner suporta `describe`, `test`, `it`, `expect`, `beforeEach`, `afterEach`, `beforeAll`, `afterAll`, `mock`, `spyOn` — o suficiente para migrar suites Jest sem grandes mudanças.

### Compatibilidade com Node.js

A compatibilidade do Bun com o ecossistema Node.js é alta. Os frameworks e bibliotecas mais usados funcionam sem modificação:

**Compatíveis:** Express, Fastify, Hono, Prisma, Drizzle, Zod, Axios, Lodash, date-fns, dotenv, chalk, commander, inquirer, ws (WebSockets).

**Incompatíveis ou com restrições:**
- **Native addons (`.node` files)**: não suportados. Pacotes como `bcrypt`, `sharp`, `canvas`, `node-gyp`-based libs falham. Usar alternativas puras-JS (`bcryptjs`, `sharp` pode funcionar via WASM em versões futuras).
- **API `v8` direta**: módulos que importam `const v8 = require('v8')` para inspecionar heap, serializar objetos, etc., não funcionam — Bun usa JSC, não V8.
- **Worker threads com `--experimental` flags**: suporte parcial; verificar a tabela de compatibilidade em `bun.sh/docs/runtime/nodejs-apis`.

O flag `--bun` força o Bun a usar seu próprio runtime mesmo ao executar scripts via npm, evitando que `package.json` chame `node` implicitamente:

```js
// Sem --bun: npm scripts podem chamar Node.js internamente
// bun run dev

// Com --bun: força Bun como runtime em todo o processo
// bun --bun run dev
```

## Quando usar

A escolha entre Bun, Node e Deno depende do contexto do projeto:

> [!tip] Use Bun quando:
> - Projeto greenfield com TypeScript — sem config de transpilação necessária
> - CLIs e ferramentas de desenvolvimento — startup rápido importa
> - Serverless functions / edge workers — cold start é crítico
> - Você quer simplificar toolchain (sem Jest + esbuild + npm separados)
> - Velocidade de `bun install` em CI/CD faz diferença mensurável

> [!tip] Use Node quando:
> - Projeto usa native addons (bcrypt, sharp, canvas, bindings C++)
> - Codebase depende da API `v8` diretamente
> - Servidor HTTP de alta carga onde JIT warmup do V8 se paga
> - Time não quer adotar nova toolchain sem piloto controlado
> - Estabilidade e LTS de longo prazo são requisitos contratuais

> [!tip] Use Deno quando:
> - Segurança por padrão é requisito (permissões explícitas de rede/disco)
> - Deploy em Deno Deploy / edge com modelo de permissões granular
> - Projeto novo que pode abrir mão de compatibilidade npm em troca de segurança

## Armadilhas comuns

### `bun.lockb` não é legível por humanos

```js
// ❌ Problema: bun.lockb em diff git é binário ilegível
// git diff bun.lockb → exibe dados binários sem semântica legível
// Revisores de PR não conseguem ver quais dependências mudaram
// Ferramentas de auditoria de segurança podem não conseguir ler o lockfile

// ✅ Fix: commitar bun.lockb normalmente (o Bun consegue ler e garantir reprodutibilidade)
// Em CI: usar bun install --frozen-lockfile para garantir reprodutibilidade
// Para projetos em Bun ≥ 1.2: o lockfile padrão já é texto (bun.lock), não binário
// Para auditar: bun pm ls --all mostra a árvore de dependências resolvidas
```

### Native addons (`.node`) não são suportados

```js
// ❌ Problema: usar módulos com addons nativos no Bun
// import bcrypt from 'bcrypt';
// // bcrypt usa bcrypt.node (compilado via node-gyp) — não suportado pelo Bun
// // Erro em runtime: "Failed to load native module: bcrypt.node"

// const sharp = require('sharp');
// // sharp usa código C++ nativo — mesma situação

// ✅ Fix: usar alternativas puras-JS (sem bindings C++)
// import { hash, compare } from 'bcryptjs'; // implementação JS pura, sem .node
// // Para sharp: verificar se versão WASM está disponível, ou manter Node nessa parte
// // Regra geral: se o pacote usa node-gyp no install, não vai funcionar no Bun
```

### `Bun.serve()` cria lock-in de runtime

```js
// ❌ Problema: escrever servidor com Bun.serve() e depois tentar rodar em Node
// const server = Bun.serve({
//   port: 3000,
//   fetch(req) {
//     return new Response("Hello");
//   },
// });
// // No Node.js: ReferenceError: Bun is not defined
// // O código não roda fora do Bun sem modificação

// ✅ Fix (opção 1): use APIs compatíveis com Node se portabilidade importa
// import { createServer } from "node:http";
// // Express, Fastify, Hono funcionam tanto no Bun quanto no Node

// ✅ Fix (opção 2): aceite o lock-in e documente o requisito explicitamente
// // Anote no README/CLAUDE.md que o projeto requer Bun >= 1.x
// // Adicione check no package.json engines: { "bun": ">=1.0.0" }
```

### `bun test` tem diferenças sutis em relação ao Jest

```js
// ❌ Problema: assumir que bun test é 100% compatível com Jest
// // jest.fn() não existe — usar mock() do bun:test
// const fn = jest.fn(); // ReferenceError: jest is not defined

// // Módulo jest-environment-jsdom não existe no Bun
// // Testes DOM que dependem de jsdom podem falhar

// ✅ Fix: importar os utilitários do módulo correto
// import { mock, spyOn, jest } from "bun:test";
// // bun:test exporta um objeto 'jest' com compatibilidade parcial
// const fn = mock(() => {}); // API nativa Bun
// const spy = spyOn(object, "method"); // funciona igual ao Jest

// // Para testes DOM: usar happy-dom como alternativa ao jsdom
// // bun add -d happy-dom e configurar em bunfig.toml
```

## Em entrevista

**P: Qual é a diferença fundamental entre Bun e Node.js em termos de engine JavaScript?**

Bun uses JavaScriptCore (JSC), the engine powering WebKit and Safari, while Node.js uses V8, the engine behind Chrome and Chromium. JSC has faster cold-start performance, which makes Bun significantly faster for short-lived processes like CLI tools and serverless functions. V8's more aggressive JIT compiler (TurboFan) tends to deliver higher throughput for long-running server processes where the warmup cost is amortized over millions of requests.

---

**P: O Bun é um substituto direto para o Node.js? Quando você não migraria?**

Bun is a near-drop-in replacement for many Node.js workloads, with strong compatibility for frameworks like Express, Fastify, and Prisma. However, I would not migrate if the project relies on native addons (`.node` files compiled via node-gyp), since Bun does not support them — packages like `bcrypt` or `sharp` require pure-JS alternatives. I would also evaluate carefully for production long-running services where V8's JIT optimizer may outperform JSC after warmup, and for teams that are not ready to adopt a new toolchain without a controlled pilot.

---

**P: O que significa dizer que o Bun é um "all-in-one toolkit"?**

Bun ships as a single binary that replaces multiple tools in the Node.js ecosystem: it is the runtime (replacing `node`), the package manager (replacing `npm`/`pnpm`/`yarn`), the bundler (replacing `esbuild`/`webpack`), and the test runner (replacing Jest or Vitest). This eliminates inter-tool version conflicts and reduces the number of dev dependencies and configuration files significantly. For greenfield TypeScript projects, this can compress the entire toolchain setup from five or more tools with separate configs down to a single `bun` binary with minimal or no configuration.

---

**P: O que é o `bun.lockb` e por que ele é diferente do `package-lock.json`?**

`bun.lockb` is a binary lockfile format used by Bun, as opposed to the human-readable JSON format of `package-lock.json` or `yarn.lock`. The binary format is faster to parse and significantly smaller on disk, which contributes to Bun's install speed advantage. The tradeoff is that `git diff bun.lockb` produces unreadable binary output. In projects using Bun ≥ 1.2, the default lockfile is the text file `bun.lock`, which is human-readable and produces useful diffs in git. In CI you use `bun install --frozen-lockfile` to enforce reproducibility.

## Vocabulário

| PT | EN |
|----|----|
| motor JavaScript | JavaScript engine |
| tempo de inicialização | startup time / cold start |
| kit de ferramentas completo | all-in-one toolkit |
| módulo nativo / addon nativo | native addon / native module |
| compatibilidade de API | API compatibility |
| arquivo de lock binário | binary lockfile |
| compilação antecipada | ahead-of-time compilation (AOT) |
| código de longa duração | long-running code / long-lived process |
| aquecimento do JIT | JIT warmup |
| bundler nativo | native bundler |

## Fontes

- Site oficial: https://bun.sh
- Bun 1.0 release: https://bun.sh/blog/bun-v1.0
- Bun GitHub: https://github.com/oven-sh/bun
- Bun — Node.js API compatibility: https://bun.sh/docs/runtime/nodejs-apis

## Veja também

- [[Tooling e ecossistema moderno]]
- [[07 - Single Executable Apps (SEA)]]
- [[01 - Package managers - npm, pnpm, yarn e bun]]
- [[08 - Promise-based core APIs]]
- [[Node.js]]
- [[03-Dominios/Node/index|Node.js (MOC central)]]
