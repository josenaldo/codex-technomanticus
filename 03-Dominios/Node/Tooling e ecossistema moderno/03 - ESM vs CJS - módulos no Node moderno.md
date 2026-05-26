---
title: "ESM vs CJS - módulos no Node moderno"
created: 2026-05-13
updated: 2026-05-13
type: concept
status: seedling
progresso: andamento
publish: false
tags:
  - node
  - esm
  - cjs
  - módulos
  - tooling
  - javascript
---

# ESM vs CJS - módulos no Node moderno

> [!abstract] TL;DR
> ESM (`import`/`export`) é o padrão oficial para projetos Node novos em 2026; use `"type": "module"` no `package.json` para ativar.
> CJS (`require`/`module.exports`) é legado, mas ainda dominante em bibliotecas publicadas antes de 2022 — você vai encontrar nos dois projetos novos que mantém legado e em deps transitivas.
> A distinção fundamental: `require` é **síncrono** e resolve em runtime; `import` é **estático** (analisado antes da execução), suporta tree-shaking e permite `await` de nível superior.
> Dual publish (campo `exports` no `package.json`) é a estratégia para bibliotecas que precisam oferecer ambos os formatos sem forçar o consumidor a nenhum dos dois.

## O que é

O [[Node.js]] nasceu sem um sistema de módulos nativo na linguagem — o JavaScript de 2009 não tinha `import` nem `export`. Para resolver isso, o core team adotou a especificação **CommonJS (CJS)**, criada originalmente para ambientes server-side JavaScript, que define `require()` para importar e `module.exports` para exportar. O CJS foi a única forma oficial de modularizar código Node por mais de uma década.

Em 2015, o ECMAScript 2015 (ES6) introduziu os **ES Modules (ESM)** como o sistema de módulos nativo da linguagem, com `import` e `export` estáticos. Mas a adoção no Node demorou: a primeira implementação experimental chegou no Node 12 (2019) e a versão estável, sem flag, só no Node 14 (2020). O ecossistema npm, com milhões de pacotes CJS publicados, tornou a transição gradual e cheia de nuances de interoperabilidade.

Em 2026, o estado é o seguinte:

- **Node 22+ LTS** suporta ESM plenamente, incluindo `import.meta.dirname`, top-level `await` e `--experimental-vm-modules` para testes
- A maioria das **novas bibliotecas** é publicada como ESM puro ou dual (ESM + CJS)
- Grande parte do código **legado e das deps transitivas** ainda é CJS — o desenvolvedor senior precisa entender ambos e saber fazer o interop funcionar sem erros

O conhecimento de ESM vs CJS não é apenas teórico: é uma das **perguntas mais frequentes em entrevistas senior** de Node.js, e a fonte do erro `ERR_REQUIRE_ESM` que assombra projetos de migração.

---

## Como funciona

### CommonJS (CJS)

O CJS define um modelo simples: cada arquivo é um **módulo independente**, e o Node envolve automaticamente o código em uma função wrapper antes de executar:

```js
(function(exports, require, module, __filename, __dirname) {
  // seu código aqui
});
```

Essa wrapper é o motivo pelo qual `__filename`, `__dirname`, `module`, `exports` e `require` estão disponíveis em qualquer arquivo `.js` CJS — eles são **parâmetros da função**, não variáveis globais. Note a ordem: `exports` vem antes de `require`.

**Características principais do CJS:**

- `require()` é **síncrono**: bloqueia a thread até o módulo ser carregado e avaliado
- A resolução acontece em **runtime** (tempo de execução), não em tempo de análise
- `module.exports` é o objeto retornado ao chamador; `exports` é um atalho para `module.exports` (cuidado ao reatribuir)
- **Caching**: o `require()` usa um cache por caminho de arquivo resolvido — a mesma instância é retornada em todas as chamadas subsequentes para o mesmo módulo
- Não suporta top-level `await`
- Não pode ser tree-shaken (imports são dinâmicos por natureza)

**Exemplo completo de módulo CJS:**

```js
// math.cjs
const PI = 3.14159265358979;

function circleArea(radius) {
  return PI * radius * radius;
}

function circumference(radius) {
  return 2 * PI * radius;
}

// Exportando como objeto com múltiplas funções
module.exports = {
  circleArea,
  circumference,
  PI,
};

// Alternativa: exports.circleArea = circleArea;
// (evite reatribuir exports = {...} — quebra a referência para module.exports)
```

```js
// app.cjs
const { circleArea, circumference, PI } = require('./math.cjs');

console.log(`Área: ${circleArea(5).toFixed(2)}`);   // 78.54
console.log(`Perímetro: ${circumference(5).toFixed(2)}`); // 31.42

// Segunda chamada — retorna o mesmo objeto cacheado (sem re-executar math.cjs)
const math2 = require('./math.cjs');
console.log(math2 === require('./math.cjs')); // true — mesma referência no cache
```

---

### ES Modules (ESM)

O ESM é o sistema de módulos nativo do JavaScript moderno. Diferente do CJS, os imports são **estáticos**: o motor JavaScript analisa todas as declarações `import` antes de executar qualquer linha de código. Isso possibilita tree-shaking, análise de dependências em tempo de build, e top-level `await`.

**Características principais do ESM:**

- `import`/`export` são analisados **estaticamente** antes da execução
- Suporta **top-level `await`** — o módulo age como uma função assíncrona para quem o importa
- `import.meta.url` fornece a URL do módulo atual (substitui `__filename`)
- `import.meta.dirname` / `import.meta.filename` fornecem diretório e caminho do módulo (Node 20.11.0+ / Node 21.2+ / Node 22+; para versões anteriores, use `fileURLToPath`)
- **Exports nomeados**, **export default**, e **namespace imports** (`import * as`)
- **Imutável por design**: o objeto de namespace de um módulo é read-only (não pode ser monkey-patched como `module.exports`)
- Pode ser tree-shaken por bundlers (Rollup, esbuild, Vite, tsup)

**Exemplo ESM equivalente ao CJS acima:**

```js
// math.mjs (ou math.js em projeto com "type": "module")
export const PI = 3.14159265358979;

export function circleArea(radius) {
  return PI * radius * radius;
}

export function circumference(radius) {
  return 2 * PI * radius;
}

// Export default (opcional — pode coexistir com named exports)
export default { circleArea, circumference, PI };
```

```js
// app.mjs
import { circleArea, circumference, PI } from './math.mjs';
// Ou: import math from './math.mjs';          // default export
// Ou: import * as math from './math.mjs';     // namespace import

console.log(`Área: ${circleArea(5).toFixed(2)}`);
console.log(`Perímetro: ${circumference(5).toFixed(2)}`);

// Top-level await — só funciona em ESM
const config = await fetch('/api/config').then(r => r.json());
console.log(config);
```

---

### Como ativar ESM no Node

O Node determina o formato do módulo pela extensão do arquivo e pelo campo `"type"` do `package.json` mais próximo:

| Arquivo | `"type"` no package.json | Formato |
|---------|--------------------------|---------|
| `.mjs` | qualquer | sempre ESM |
| `.cjs` | qualquer | sempre CJS |
| `.js` | `"module"` | ESM |
| `.js` | `"commonjs"` (padrão) | CJS |
| `.js` | ausente | CJS (legado padrão) |

A regra prática: **`.mjs` é sempre ESM, `.cjs` é sempre CJS**, independente do `package.json`. As extensões explícitas eliminam ambiguidade — úteis em projetos que misturam os dois formatos.

**Configuração para projeto ESM puro:**

```json
// package.json
{
  "name": "meu-projeto",
  "version": "1.0.0",
  "type": "module",
  "engines": { "node": ">=18.0.0" },
  "scripts": {
    "start": "node src/index.js",
    "dev": "node --watch src/index.js"
  }
}
```

```json
// tsconfig.json — para TypeScript com resolução NodeNext
{
  "compilerOptions": {
    "target": "ES2022",
    "module": "NodeNext",
    "moduleResolution": "NodeNext",
    "outDir": "dist",
    "rootDir": "src",
    "strict": true,
    "declaration": true,
    "declarationMap": true,
    "sourceMap": true
  },
  "include": ["src/**/*"]
}
```

> [!important] `moduleResolution: "NodeNext"` obriga extensões explícitas
> Com `NodeNext`, TypeScript exige que imports de arquivos locais incluam a extensão: `import { foo } from './foo.js'` — mesmo que o arquivo seja `foo.ts`. Isso reflete o comportamento real do Node com ESM (que não resolve extensões automaticamente).

---

### Interop CJS ↔ ESM

A regra de ouro: **ESM pode importar CJS, mas CJS não pode `require()` ESM**.

**ESM importando CJS:**

```js
// ESM importando um pacote CJS (ex: uuid@8 — versão pré-ESM)
import uuidPkg from 'uuid'; // module.exports vira o default export
const { v4: uuidv4 } = uuidPkg;

// Ou desestruturando diretamente (Node tenta detectar named exports)
import { v4 as uuidv4 } from 'uuid'; // pode falhar em alguns pacotes CJS
```

**CJS tentando importar ESM — ERRO:**

```js
// ❌ ERR_REQUIRE_ESM — CJS não pode importar módulo ESM com require()
const esmModule = require('./esm-module.mjs');
// Error [ERR_REQUIRE_ESM]: require() of ES Module './esm-module.mjs' not supported.
// Instead change the require of ./esm-module.mjs to a dynamic import()
```

**Soluções para interop:**

```js
// Solução 1: dynamic import() em CJS para carregar ESM
// app.cjs
async function loadEsmModule() {
  // import() retorna uma Promise — funciona em CJS para carregar ESM
  const { default: esmFn, namedExport } = await import('./esm-module.mjs');
  return esmFn();
}

loadEsmModule().then(console.log);

// Solução 2: createRequire em ESM para chamar require() (para CJS-only deps)
// app.mjs
import { createRequire } from 'node:module';
import { fileURLToPath } from 'node:url';

const require = createRequire(import.meta.url);

// Agora pode usar require() dentro de ESM — útil para deps que não têm ESM build
const lodash = require('lodash');
const _ = lodash;

console.log(_.chunk([1, 2, 3, 4], 2)); // [[1,2],[3,4]]
```

> [!tip] `import()` dinâmico funciona nos dois mundos
> `import()` é uma expressão (não uma declaração) e funciona tanto em CJS quanto em ESM. Em CJS, é a única maneira de carregar módulos ESM. Em ESM, é a maneira de fazer imports condicionais ou lazy.

---

### Dual publish de bibliotecas

Uma biblioteca que quer suportar consumidores CJS e ESM simultaneamente usa o campo **`exports`** no `package.json` com chaves condicionais. O campo `exports` tem **precedência sobre `main`** — se `exports` estiver presente, `main` é ignorado para os caminhos cobertos.

**Estrutura de dual publish:**

```json
// package.json de uma biblioteca dual-format
{
  "name": "minha-lib",
  "version": "2.0.0",
  "type": "module",
  "main": "./dist/index.cjs",
  "module": "./dist/index.js",
  "types": "./dist/index.d.ts",
  "exports": {
    ".": {
      "import": {
        "types": "./dist/index.d.ts",
        "default": "./dist/index.js"
      },
      "require": {
        "types": "./dist/index.d.cts",
        "default": "./dist/index.cjs"
      }
    },
    "./utils": {
      "import": "./dist/utils.js",
      "require": "./dist/utils.cjs"
    }
  },
  "files": ["dist"],
  "scripts": {
    "build": "tsup src/index.ts --format cjs,esm --dts"
  },
  "devDependencies": {
    "tsup": "^8.0.0",
    "typescript": "^5.4.0"
  }
}
```

```ts
// tsup.config.ts
import { defineConfig } from 'tsup';

export default defineConfig({
  entry: ['src/index.ts', 'src/utils.ts'],
  format: ['cjs', 'esm'],  // gera dist/index.cjs e dist/index.js
  dts: true,               // gera .d.ts e .d.cts automaticamente
  splitting: false,
  sourcemap: true,
  clean: true,
  treeshake: true,
});
```

O `tsup` gera `dist/index.js` (ESM) e `dist/index.cjs` (CJS) por padrão, com declaration files correspondentes (`.d.ts` para ESM, `.d.cts` para CJS). O campo `exports` com `"import"` e `"require"` garante que o Node (e bundlers como Webpack e Vite) escolham o formato correto automaticamente.

> [!warning] Pitfall de tipos em dual publish
> Sem `"types"` condicional por formato, consumidores TypeScript podem receber os tipos errados. Use `"types": "./dist/index.d.ts"` no bloco `"import"` e `"types": "./dist/index.d.cts"` no bloco `"require"`. O tsup gera ambos com a flag `--dts`.

---

## Quando usar

**Use ESM puro (`"type": "module"`):**

- Projetos novos (apps, APIs, CLIs) iniciados em 2024+
- Projetos que usam bibliotecas modernas que publicam ESM puro (Vite, Vitest, chalk v5+, got v13+, sindresorhus libs)
- Quando você precisa de top-level `await` para inicialização assíncrona (banco, config remota)
- Projetos que se beneficiam de tree-shaking (microserviços com bundle de Lambda, Edge Functions)

**Mantenha CJS (ou use `.cjs` explicitamente):**

- Scripts de build/config que precisam ser executados em ambientes onde o Node não garantido ser moderno (Docker legado, ferramentas CI antigas)
- Plugins para ferramentas que ainda não migraram para ESM (algumas versões do Jest, Webpack config)
- Arquivos de configuração que o ecossistema espera em CJS (`jest.config.cjs`, `.eslintrc.cjs`)

**Use dual publish quando você é o autor da biblioteca:**

- Sua biblioteca tem consumidores em projetos CJS legados e projetos ESM modernos
- Você não quer forçar migração dos consumidores
- Use `tsup` ou `unbuild` para automatizar a geração de ambos os formatos

**Tabela de decisão rápida:**

| Cenário | Recomendação |
|---------|-------------|
| App Node novo | ESM puro com `"type": "module"` |
| API Node em projeto legado | Mantenha CJS; migre incrementalmente |
| Biblioteca npm nova | Dual publish (ESM + CJS) |
| CLI simples para distribuição | ESM; use `.mjs` se precisar misturar |
| Config de Jest/ESLint | `.cjs` explícito para evitar conflito |

---

## Armadilhas comuns

### Armadilha 1: `__dirname` e `__filename` não existem em ESM

Em CJS, `__dirname` e `__filename` são injetados pela wrapper function do Node e estão sempre disponíveis. Em ESM, essa wrapper não existe — as variáveis simplesmente não existem.

**Problema — código que quebra ao migrar para ESM:**

```js
// ❌ ERRO em ESM: ReferenceError: __dirname is not defined
import path from 'node:path';
import fs from 'node:fs';

const configPath = path.join(__dirname, 'config', 'app.json');
//                            ^^^^^^^^^ ReferenceError!

const data = fs.readFileSync(configPath, 'utf-8');
```

**Fix — usando `import.meta` para recriar as variáveis:**

```js
// ✅ ESM com Node 20.11.0+ (import.meta.dirname/filename disponível desde Node 20.11.0 / Node 21.2+)
import path from 'node:path';
import fs from 'node:fs';

// Node 20.11.0+ / Node 21.2+ / Node 22+ LTS: import.meta.dirname e import.meta.filename nativos
const __dirname = import.meta.dirname;
const __filename = import.meta.filename;

const configPath = path.join(__dirname, 'config', 'app.json');
const data = fs.readFileSync(configPath, 'utf-8');

// ── Para Node < 20.11.0 (Node 18, Node 20.0–20.10) ───────────────────────
import { fileURLToPath } from 'node:url';

const __filename_compat = fileURLToPath(import.meta.url);
const __dirname_compat = path.dirname(__filename_compat);
// Alternativa ainda mais curta:
// const __dirname_compat = fileURLToPath(new URL('.', import.meta.url));

const configPath2 = path.join(__dirname_compat, 'config', 'app.json');
```

---

### Armadilha 2: `require()` de arquivos `.json` não funciona em ESM

Em CJS, `require('./config.json')` funciona nativamente — o Node parseia o JSON e retorna o objeto. Em ESM, importar JSON requer sintaxe especial (`with { type: 'json' }`) ou `createRequire`.

**Problema — import de JSON em ESM sem assert:**

```js
// ❌ ERRO em ESM (Node < 22 sem a flag, ou sem "with { type: 'json' }")
import config from './config.json';
// SyntaxError: Unexpected token (em versões antigas)
// ou: TypeError: Module "file:///..." needs an import attribute of "type: json"
```

**Fix — duas abordagens:**

```js
// ✅ Abordagem 1: import com "with { type: 'json' }" (estável no Node 22+)
import config from './config.json' with { type: 'json' };

console.log(config.database.host); // funciona normalmente

// ──────────────────────────────────────────────────────────────────────
// ✅ Abordagem 2: createRequire (compatível com Node 14+)
import { createRequire } from 'node:module';

const require = createRequire(import.meta.url);
const config2 = require('./config.json'); // require normal para JSON

console.log(config2.database.host);

// ──────────────────────────────────────────────────────────────────────
// ✅ Abordagem 3: fs + JSON.parse (máxima compatibilidade)
import { readFileSync } from 'node:fs';
import { fileURLToPath } from 'node:url';
import path from 'node:path';

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const config3 = JSON.parse(
  readFileSync(path.join(__dirname, 'config.json'), 'utf-8')
);
```

---

### Armadilha 3: biblioteca CJS-only dentro de projeto ESM

Algumas bibliotecas antigas (ou versões antigas de libs populares) publicam apenas CJS. Dentro de um projeto ESM com `"type": "module"`, o import padrão pode não funcionar corretamente para libs que usam `exports` condicional incorretamente, ou pode não expor named exports como esperado.

**Problema — named imports de lib CJS podem não funcionar:**

```js
// ❌ Pode falhar para libs CJS que não definem named exports explicitamente
// (o Node tenta detectar via static analysis, mas nem sempre funciona)
import { someFunction } from 'old-cjs-lib';
// SyntaxError: The requested module 'old-cjs-lib' does not provide an export named 'someFunction'
```

**Fix — usar default import e desestruturar, ou createRequire:**

```js
// ✅ Abordagem 1: default import + desestruturação manual
import oldLib from 'old-cjs-lib';
const { someFunction, AnotherExport } = oldLib;

someFunction('arg');

// ── Ou com createRequire (para máximo controle) ────────────────────────
// ✅ Abordagem 2: createRequire — comportamento idêntico ao require() CJS
import { createRequire } from 'node:module';
const require = createRequire(import.meta.url);

const oldLib2 = require('old-cjs-lib');
oldLib2.someFunction('arg');

// ── Verificando se a lib tem dual build ───────────────────────────────
// Muitas libs antigas ganharam ESM em versões mais recentes:
// uuid@8 → CJS only | uuid@9+ → dual publish com named exports ESM
// chalk@4 → CJS     | chalk@5+ → ESM puro
// got@11  → CJS     | got@12+  → ESM puro
// Verifique se há uma versão mais nova antes de usar o workaround.
```

---

## Em entrevista

**"What is the difference between ESM and CJS in Node.js?"**

> ESM and CJS are two module systems that coexist in Node.js, but they work fundamentally differently. CJS uses `require()`, which is synchronous and resolves modules at runtime — the module graph is discovered as the code runs. ESM uses `import`/`export`, which are static declarations analyzed by the engine before any code executes, enabling tree-shaking and top-level `await`. Another key difference is that CJS wraps each module in a function that provides `__dirname`, `__filename`, `module`, `exports`, and `require` as parameters, while ESM relies on `import.meta` for context — so code that uses `__dirname` will break when migrated to ESM without changes. In 2026, ESM is the official standard for new Node projects, but CJS is still widespread in older packages, so understanding the interop rules — ESM can import CJS, but CJS cannot `require()` ESM — is essential for any senior Node developer.

**"How do you handle interoperability between ESM and CJS packages?"**

> The fundamental rule is asymmetric: ESM can import CJS via a default import (where `module.exports` becomes the default export), but CJS cannot use `require()` on ESM modules — that throws `ERR_REQUIRE_ESM` because `require()` is synchronous and ESM loading is inherently asynchronous. When I'm in a CJS codebase and need to use an ESM-only package, I use dynamic `import()` inside an async function, since `import()` is an expression that works in both module systems. Conversely, when I'm in an ESM codebase and need to use a CJS package that doesn't expose named exports correctly, I use `createRequire(import.meta.url)` to get a `require` function that works as expected. For libraries I maintain, I use `tsup` to generate dual builds with the `exports` conditional field in `package.json`, so consumers can use whichever format fits their project without workarounds.

**"What's your strategy for migrating a CJS project to ESM?"**

> I approach ESM migrations incrementally rather than all at once, because a big-bang rewrite breaks things that are hard to trace back to the module change. My first step is auditing dependencies with a tool like `esm-detector` or manually checking if key packages have ESM builds — if core deps are CJS-only, I either update them first or plan for `createRequire` wrappers. Then I convert the leaf modules first (utilities with no internal imports) and work toward the entry point, because there's no circular dependency problem going that direction. The main mechanical changes are: add `"type": "module"` to `package.json`, change `require()` to `import`, change `module.exports` to `export`, replace `__dirname`/`__filename` with `import.meta.dirname`/`import.meta.filename` (Node 22+) or the `fileURLToPath` equivalent for older Node, and add `.js` extensions to all local imports (required by ESM's strict resolution). I also watch for files that must stay CJS — like `jest.config.js` before Jest adds full ESM support — and rename them to `.cjs`. Throughout the migration, I run the test suite after each converted module to catch issues early rather than debugging a fully-migrated project that doesn't start.

---

## Vocabulário

| Português | Inglês |
|-----------|--------|
| Módulo | Module |
| Resolução de módulos | Module resolution |
| Import estático | Static import |
| Import dinâmico | Dynamic import |
| Export nomeado | Named export |
| Export padrão | Default export |
| Publicação dual | Dual publish |
| Interoperabilidade | Interoperability |
| Empacotamento | Bundling |
| Quebra de API | Breaking change |
| Árvore de dependências | Dependency tree |
| Eliminação de código morto | Tree-shaking |

---

## Fontes

- [Node.js Docs — ECMAScript modules](https://nodejs.org/docs/latest/api/esm.html) — documentação oficial do suporte a ESM no Node, incluindo `import.meta`, interop e configuração
- [Node.js Docs — CommonJS modules](https://nodejs.org/docs/latest/api/modules.html) — documentação oficial do sistema CJS, incluindo a wrapper function, `require` cache e `module.exports`
- [Node.js Docs — Packages (conditional exports)](https://nodejs.org/docs/latest/api/packages.html) — documentação do campo `exports` no `package.json` e como configurar dual publish
- [tsup — Bundle your TypeScript library](https://tsup.egoist.dev/) — ferramenta para gerar builds ESM + CJS com suporte a declaration files
- [sindresorhus/esm-package](https://github.com/sindresorhus/esm-package) — lista de pacotes populares que migraram para ESM puro (útil para planejar migrações)

---

## Veja também

- [[Tooling e ecossistema moderno]] — índice do galho 7, visão geral de todas as notas
- [[04 - TypeScript nativo - strip types e integração]] — próxima nota: TypeScript sem transpilação no Node 22+
- [[01 - Package managers - npm, pnpm, yarn e bun]] — package managers e como o campo `exports` interage com resolução de deps
- [[03-Dominios/Node/index|Node.js (MOC central)]] — visão geral de todos os galhos da trilha Node Senior
- [[Node.js]] — tronco da trilha Node Senior
