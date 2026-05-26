---
title: "TypeScript nativo - strip types e integração"
created: 2026-05-12
updated: 2026-05-12
type: concept
status: seedling
progresso: andamento
publish: false
tags:
  - node
  - typescript
  - strip-types
  - tooling
  - javascript
---

# TypeScript nativo - strip types e integração

> [!abstract] TL;DR
> O Node.js 22.6.0 introduziu `--experimental-strip-types`, que remove anotações de tipo diretamente do runtime sem transpilação completa — sem build step, sem ts-node.
> O Node 22.7.0 adicionou `--experimental-transform-types`, que vai além: suporta `enum` usando esbuild internamente. O Node 24 (24.12.0+) estabilizou o type stripping como padrão para sintaxe TypeScript apagável — `node app.ts` funciona sem flag. `--experimental-transform-types` (enum/namespace) permanece experimental mesmo no Node 24.
> Para desenvolvimento com hot reload, `tsx` (baseado em esbuild) é o substituto moderno do `ts-node`. Para projetos legados com ts-node, adicionar `@swc/core` como transpiler acelera significativamente a inicialização.
> Independente da estratégia de execução, configure o `tsconfig.json` com `moduleResolution: "NodeNext"` e `module: "NodeNext"` para projetos Node modernos.

## O que é

Historicamente, executar TypeScript no Node exigia uma etapa de build ou um wrapper como `ts-node`: o código `.ts` precisava ser transpilado para `.js` antes de o Node executar. Essa fricção tornava o ciclo de desenvolvimento mais lento e exigia configuração adicional.

A partir do Node 22.6.0, o runtime passou a oferecer suporte nativo para TypeScript através da **remoção de tipos** (*type stripping*): o Node lê o arquivo `.ts`, remove todas as anotações de tipo (`: string`, `interface`, `type`, `as`, etc.) e executa o JavaScript resultante diretamente. Não há transpilação de sintaxe — o código deve ser JavaScript válido sem os tipos.

### Type stripping vs transpilação completa

| Aspecto | Type stripping | Transpilação completa |
|---------|---------------|-----------------------|
| O que faz | Remove anotações de tipo | Converte sintaxe TS para JS |
| Suporta `enum` | Não (strip-types) / Sim (--experimental-transform-types) | Sim |
| Suporta decorators legados | Não | Sim |
| Velocidade | Muito rápida (pura remoção de texto) | Mais lenta (parsing + geração) |
| Sourcemaps | Não (strip-types) | Sim |
| Ferramentas | Node nativo | tsc, esbuild, SWC, Babel |

O type stripping é adequado para scripts simples, CLIs e código de servidor que não usa features TypeScript avançadas. Para projetos que dependem de `enum`, decorators legados ou `namespace`, é necessário `--experimental-transform-types` ou um transpiler completo.

### Por que suporte nativo importa

Sem build step, o fluxo de desenvolvimento fica mais simples:

- `node app.ts` funciona diretamente (Node 22.6.0+)
- Sem `npx ts-node` ou `npx tsx` para scripts rápidos
- Menos dependências no projeto
- Feedback instantâneo no terminal sem etapa de compilação

A principal limitação é que o Node **não faz verificação de tipos** — o `--experimental-strip-types` apenas apaga as anotações. Para type checking, `tsc --noEmit` continua sendo necessário separadamente.

---

## Como funciona

### `--experimental-strip-types` (Node 22.6.0+)

O Node remove as anotações de tipo do arquivo TypeScript e executa o JavaScript resultante. O mecanismo é baseado em remoção de texto: os tipos são trocados por espaços em branco para preservar os números de linha (embora sem sourcemaps, os traces ainda podem ser confusos).

**O que é suportado:**

- Anotações de tipo inline (`: string`, `: number`, `: SomeInterface`)
- Interfaces e type aliases (`interface Foo {}`, `type Bar = ...`)
- Generics em funções e classes
- `as` casts e `satisfies`
- Parâmetros opcionais e não-nulos (`?`, `!`)
- `readonly`, `public`, `private`, `protected` em classes

**O que NÃO é suportado:**

- `enum` (gera código JavaScript, não é apenas anotação)
- `namespace` (mesmo motivo)
- Decorators legados (`@Decorator` estilo TypeScript < 5 com `experimentalDecorators`)
- `const enum` (substituído por valores literais em tempo de compilação)
- Paths aliases do tsconfig (`@/components/...`) — o Node não resolve paths do tsconfig
- `.tsx` (JSX + TypeScript) — não suportado pelo mecanismo nativo de strip-types; use tsx CLI ou um bundler

**Execução básica:**

```bash
# Node 22.6.0 a 22.x
node --experimental-strip-types app.ts

# Saída esperada (Node 22.6.x — aviso é normal):
# ExperimentalWarning: Type Stripping is an experimental feature...
# Hello from TypeScript!
```

**Exemplo de arquivo compatível com strip-types:**

```ts
// app.ts — compatível com --experimental-strip-types
interface User {
  name: string;
  age: number;
}

function greet(user: User): string {
  return `Olá, ${user.name}! Você tem ${user.age} anos.`;
}

const users: User[] = [
  { name: "Alice", age: 30 },
  { name: "Bob", age: 25 },
];

for (const user of users) {
  console.log(greet(user));
}
```

> [!important]
> A partir do Node 22.18.0 (LTS do ramo 22), o type stripping é habilitado **por padrão** — `node app.ts` funciona sem nenhuma flag para sintaxe TypeScript apagável (interfaces, type aliases, generics, etc.). O flag `--experimental-strip-types` não é mais necessário nessa versão, embora o comportamento continue ativo. Ambientes de produção no Node 22 devem usar 22.18+.

---

### `--experimental-transform-types` (Node 22.7.0+)

Introduzido uma versão após o strip-types, o `--experimental-transform-types` vai além: usa **esbuild** internamente para transformar construções TypeScript que geram código JavaScript real, como `enum`.

**O que adiciona sobre strip-types:**

- Suporte a `enum` (convertido para objetos JavaScript)
- Suporte a `const enum` (inlining de valores)
- Suporte a `namespace` básico

**Trade-offs:**

- Mais lento que strip-types porque invoca esbuild
- Sourcemaps habilitados automaticamente (implica `--enable-source-maps`)
- Ainda não resolve paths aliases do tsconfig

**Execução com --experimental-transform-types:**

```bash
# Node 22.7.0 a 22.x
node --experimental-transform-types app.ts

# Node 24 — type stripping é padrão para sintaxe apagável, mas enum/namespace ainda requer a flag
node app.ts                              # TypeScript sem enum/namespace: funciona sem flag (Node 24+)
node --experimental-transform-types app.ts  # ainda necessário para enum/namespace em qualquer versão
```

**Exemplo usando enum (requer --experimental-transform-types ou tsx):**

```ts
// status.ts — requer --experimental-transform-types (ou tsx)
enum Status {
  Active = "active",
  Inactive = "inactive",
  Pending = "pending",
}

function describe(status: Status): string {
  switch (status) {
    case Status.Active:   return "Usuário ativo";
    case Status.Inactive: return "Usuário inativo";
    case Status.Pending:  return "Aguardando ativação";
  }
}

console.log(describe(Status.Active));   // Usuário ativo
console.log(describe(Status.Pending));  // Aguardando ativação
```

> [!tip]
> No Node 24 (24.12.0+), o type stripping para sintaxe apagável é o comportamento padrão — `node app.ts` funciona diretamente sem nenhuma flag para código TypeScript que não usa `enum` ou `namespace`. `--experimental-transform-types` permanece experimental mesmo no Node 24 e ainda é necessário para enum e namespace.

---

### `tsx` — substituto do ts-node

`tsx` é a ferramenta preferida para desenvolvimento TypeScript no Node em 2026. Baseado em **esbuild**, oferece transpilação rápida com suporte completo a TypeScript e ESM.

**Vantagens sobre ts-node:**

- Muito mais rápido (esbuild vs tsc)
- Suporte nativo a ESM sem configuração extra
- `tsx watch` para hot reload em desenvolvimento
- Resolve `paths` aliases do `tsconfig.json`
- Suporta `.ts`, `.tsx`, `.mts`, `.cts`
- Sem necessidade de `ts-node/esm` loader separado

**Instalação e uso básico:**

```bash
# Instalar como dev dependency
npm install --save-dev tsx

# Executar arquivo TypeScript diretamente
npx tsx app.ts

# Hot reload em desenvolvimento
npx tsx watch src/server.ts

# Especificar tsconfig customizado
npx tsx --tsconfig tsconfig.dev.json src/index.ts

# Como script no package.json
# "dev": "tsx watch src/server.ts"
# "start": "tsx src/server.ts"
```

**Exemplo com paths aliases (funciona com tsx, não com node nativo):**

```ts
// tsconfig.json define: "paths": { "@/utils/*": ["src/utils/*"] }
// tsx resolve corretamente; node nativo ignora

import { formatDate } from "@/utils/date";  // ✅ funciona com tsx
import { logger } from "@/lib/logger";       // ✅ funciona com tsx

const date = formatDate(new Date());
logger.info(`Data formatada: ${date}`);
```

> [!tip]
> Use `tsx` para desenvolvimento e hot reload. Para produção, compile com `tsc` (ou `tsup`/`esbuild`) e execute o JavaScript gerado com `node`.

---

### `ts-node` com SWC

`ts-node` foi a ferramenta dominante para executar TypeScript no Node antes do tsx. Em projetos **legados** já configurados com ts-node, vale usar o transpiler **SWC** (escrito em Rust) para acelerar a inicialização significativamente.

**Quando ainda faz sentido:**

- Projeto já configurado com ts-node e Jest que depende de `ts-jest`
- Configurações complexas de paths com ts-node hooks já funcionando
- Dependências que assumem ts-node como executor (alguns frameworks legados)

**Configuração do ts-node com SWC:**

```json
// tsconfig.json — habilitar SWC como transpiler do ts-node
{
  "compilerOptions": {
    "target": "ES2022",
    "module": "NodeNext",
    "moduleResolution": "NodeNext",
    "strict": true,
    "outDir": "dist",
    "rootDir": "src"
  },
  "ts-node": {
    "swc": true,
    "esm": true
  }
}
```

**Uso com loader ESM:**

```bash
# Instalar dependências
npm install --save-dev ts-node @swc/core @swc/helpers

# Executar com loader ESM (necessário para projetos com "type": "module")
node --loader ts-node/esm src/index.ts

# Ou via script no package.json:
# "dev": "node --loader ts-node/esm src/index.ts"
```

> [!warning]
> Para projetos novos, prefira `tsx`. O `ts-node` com SWC é uma estratégia de **otimização incremental** para projetos legados — não o ponto de partida ideal.

---

### `tsconfig` para Node moderno

A configuração do `tsconfig.json` tem impacto direto em como TypeScript se integra ao Node moderno. As opções mais críticas são `module` e `moduleResolution`.

**Opções essenciais:**

- `moduleResolution: "NodeNext"` — resolve imports com a mesma lógica do Node ESM: busca `.js`, `package.json#exports`, etc. É obrigatório para código que usa `import` com extensão `.js` em arquivos `.ts` (convenção ESM)
- `module: "NodeNext"` — gera ESM ou CJS dependendo do `package.json` do arquivo (`.mts` → ESM, `.cts` → CJS, `.ts` → segue `"type"` do package.json)
- `target: "ES2022"` ou superior — aproveita features nativas como top-level await, `Array.at()`, `Object.hasOwn()`
- `strict: true` — habilita todo o conjunto de checagens rígidas (recomendado sempre)

**tsconfig.json completo recomendado para Node 22+:**

```json
{
  "compilerOptions": {
    "target": "ES2022",
    "module": "NodeNext",
    "moduleResolution": "NodeNext",
    "lib": ["ES2022"],
    "outDir": "dist",
    "rootDir": "src",
    "strict": true,
    "noUncheckedIndexedAccess": true,
    "noImplicitOverride": true,
    "declaration": true,
    "declarationMap": true,
    "sourceMap": true,
    "removeComments": false,
    "esModuleInterop": false,
    "forceConsistentCasingInFileNames": true,
    "skipLibCheck": true
  },
  "include": ["src/**/*"],
  "exclude": ["node_modules", "dist"]
}
```

> [!important]
> Com `moduleResolution: "NodeNext"`, os imports em arquivos `.ts` devem usar a extensão `.js` (não `.ts`):
> ```ts
> import { helper } from "./helper.js";  // ✅ correto com NodeNext
> import { helper } from "./helper";     // ❌ falha com NodeNext (sem extensão)
> import { helper } from "./helper.ts";  // ❌ extensão .ts não é válida em import
> ```

---

## Quando usar

| Cenário | Ferramenta recomendada |
|---------|------------------------|
| Script rápido, sem `enum` ou decorators | `node --experimental-strip-types` (Node 22.6+) |
| Script com `enum`, Node 22 | `node --experimental-transform-types` (Node 22.7+) |
| Qualquer script TypeScript, Node 24 | `node` (suporte nativo estável) |
| Dev server com hot reload | `tsx watch` |
| Projeto legado com ts-node | `ts-node` + SWC (otimização incremental) |
| Build para produção | `tsc` ou `tsup` ou `esbuild` → `node dist/index.js` |
| Testes com Jest | `ts-jest` ou `tsx` + `vitest` |
| Monorepo com aliases complexos | `tsx` (resolve paths do tsconfig) |

### Comparativo detalhado

| | Node nativo (strip) | Node nativo (--experimental-transform-types) | tsx | ts-node + SWC |
|--|---------------------|----------------------------------------------|-----|----------------|
| Velocidade de início | ⚡ Muito rápida | 🟡 Rápida | ⚡ Muito rápida | 🟡 Rápida |
| Suporte a `enum` | ❌ | ✅ | ✅ | ✅ |
| Sourcemaps | ❌ | ✅ | ✅ | ✅ |
| Paths aliases | ❌ | ❌ | ✅ | ✅ (com config) |
| Hot reload | ❌ (use --watch) | ❌ (use --watch) | ✅ (tsx watch) | ❌ |
| Zero dependência | ✅ | ✅ | ❌ (dev dep) | ❌ (dev dep) |
| Node mínimo | 22.6.0 | 22.7.0 | 18+ | 12+ |

---

## Armadilhas comuns

### Armadilha 1: Usar `enum` com `--experimental-strip-types`

`enum` gera código JavaScript real (um objeto com mapeamento bidirecional), não é apenas uma anotação de tipo. Por isso, `--experimental-strip-types` não consegue processar enums — o Node não sabe como transformar a sintaxe em JS válido.

```ts
// ❌ Problema — enum com --experimental-strip-types
// node --experimental-strip-types app.ts
enum Direction {
  Up = "UP",
  Down = "DOWN",
  Left = "LEFT",
  Right = "RIGHT",
}

function move(dir: Direction) {
  console.log(`Moving: ${dir}`);
}

move(Direction.Up);
// SyntaxError: Unexpected token 'enum'
// (strip-types não transforma enum, apenas remove anotações)
```

```ts
// ✅ Fix — use --experimental-transform-types ou tsx
// node --experimental-transform-types app.ts  (Node 22.7.0+)
// ou: npx tsx app.ts

enum Direction {
  Up = "UP",
  Down = "DOWN",
  Left = "LEFT",
  Right = "RIGHT",
}

function move(dir: Direction) {
  console.log(`Moving: ${dir}`);
}

move(Direction.Up);  // Moving: UP
// Alternativa para strip-types: use const object + as const
// const Direction = { Up: "UP", Down: "DOWN" } as const;
// type Direction = typeof Direction[keyof typeof Direction];
```

---

### Armadilha 2: Paths aliases do tsconfig não funcionam com node nativo

O Node não lê o `tsconfig.json` para resolver módulos. Paths configurados em `compilerOptions.paths` funcionam apenas durante a compilação com `tsc`, não em tempo de execução. Usar `node --experimental-strip-types` com aliases causa erros de módulo não encontrado.

```ts
// ❌ Problema — paths alias com node nativo
// tsconfig.json: "paths": { "@/services/*": ["src/services/*"] }
// node --experimental-strip-types src/index.ts

import { UserService } from "@/services/user";
//                          ^^^^^^^^^^^^^^^^
// Error [ERR_MODULE_NOT_FOUND]: Cannot find package '@'
// Node não lê paths do tsconfig — resolve literalmente
```

```ts
// ✅ Fix — use tsx que resolve paths, ou use imports relativos
// Opção 1: usar tsx
// npx tsx src/index.ts  (tsx lê paths do tsconfig)

import { UserService } from "@/services/user";  // ✅ com tsx

// Opção 2: usar imports relativos (funciona com qualquer executor)
import { UserService } from "./services/user.js";  // ✅ com node nativo

// Opção 3: para node nativo com aliases, use --import com loader customizado
// node --import ./register-aliases.mjs --experimental-strip-types src/index.ts
```

---

### Armadilha 3: Stack traces confusos sem sourcemaps

O `--experimental-strip-types` não gera sourcemaps. Os números de linha nos erros correspondem ao JavaScript após a remoção dos tipos — que pode diferir do TypeScript original se os tipos ocupavam múltiplas linhas.

```ts
// ❌ Problema — stack trace aponta linha errada
// app.ts (TypeScript original)
// linha 1:  interface Config {
// linha 2:    host: string;
// linha 3:    port: number;
// linha 4:  }
// linha 5:
// linha 6:  function connect(config: Config): void {
// linha 7:    throw new Error("Falha na conexão");  // ← erro real aqui
// linha 8:  }
// linha 9:
// linha 10: connect({ host: "localhost", port: 5432 });

// Stack trace com --experimental-strip-types:
// Error: Falha na conexão
//   at connect (app.ts:3:11)  ← aponta linha 3, mas a interface foi removida
// (confuso: o desenvolvedor vê "linha 3" mas a função começa na linha 6 no ts)
```

```ts
// ✅ Fix — use tsx ou ts-node para sessões de debug
// npx tsx app.ts               (sourcemaps automáticos via esbuild)
// node --loader ts-node/esm app.ts  (sourcemaps via ts-node)

// Ou use tsc para compilar com sourcemaps e debugar o JS gerado:
// tsc && node --enable-source-maps dist/app.js

// Para debugging pontual com node nativo, aceite as linhas aproximadas
// e prefira tsx/ts-node apenas nas sessões de debug
```

> [!warning]
> Em produção, sempre compile com `tsc` (ou `tsup`) e execute o `.js` gerado com `--enable-source-maps`. Nunca execute `.ts` diretamente em produção — use node nativo com strip-types apenas para desenvolvimento e scripts.

---

## Em entrevista

**Q: What does `--experimental-strip-types` do and what are its limitations?**

The `--experimental-strip-types` flag (introduced in Node 22.6.0) tells the Node.js runtime to process TypeScript files by removing type annotations before execution, without performing any real transpilation. It replaces type syntax — interfaces, type aliases, generics, `as` casts — with whitespace, then executes the resulting JavaScript directly. The key limitations are that it does not support TypeScript constructs that generate JavaScript code, such as `enum`, `namespace`, and legacy decorators, because those cannot simply be stripped — they require actual code generation. Additionally, `--experimental-strip-types` does not produce sourcemaps, which means stack traces may point to misleading line numbers, and it does not resolve TypeScript path aliases from `tsconfig.json` since the Node module resolver does not read that file.

**Q: When would you choose `tsx` over Node's native TypeScript support?**

I would choose `tsx` whenever the project requires features that Node's native strip-types cannot handle: `enum`, path aliases defined in `tsconfig.json`, or reliable sourcemaps for debugging. `tsx` is also the clear choice for development workflows that need hot reload, since `tsx watch` automatically restarts the process on file changes — something the native Node `--watch` flag offers for `.js` files but with less TypeScript awareness. Another practical reason is compatibility with older Node versions: `tsx` works on Node 18+ while `--experimental-strip-types` requires Node 22.6.0 at minimum. For production, I would compile TypeScript with `tsc` or `tsup` regardless of which runtime tool I use in development, so the choice of tsx vs native strip-types mainly affects the developer experience and iteration speed.

**Q: What tsconfig settings are recommended for a modern Node.js project?**

For a modern Node.js project targeting Node 22+, the two most important settings are `"module": "NodeNext"` and `"moduleResolution": "NodeNext"`, which instruct TypeScript to use the same module resolution algorithm as Node's native ESM loader. This means TypeScript will require explicit file extensions in import paths — you write `import { x } from "./helper.js"` even though the file is `helper.ts`, mirroring how Node resolves modules at runtime. For the `target`, `"ES2022"` or higher is appropriate, which enables features like top-level await and class fields without downleveling. Beyond those three, `"strict": true` is mandatory for catching common type errors early, and `"sourceMap": true` plus `"declaration": true` are essential for any library or project that needs debugging support or type exports. The combination of `skipLibCheck: true` and `forceConsistentCasingInFileNames: true` rounds out a solid baseline configuration.

---

## Vocabulário

| Português | Inglês |
|-----------|--------|
| Remoção de tipos | Type stripping |
| Transpilação | Transpilation |
| Mapa de fonte | Source map |
| Alias de caminho | Path alias |
| Resolução de módulo | Module resolution |
| Decorador | Decorator |
| Enumeração | Enum (enumeration) |
| Verificação de tipos | Type checking |
| Análise estática | Static analysis |
| Compilador | Compiler |
| Carregador | Loader |
| Recarga a quente | Hot reload |

---

## Fontes

- [Node.js 22.6.0 Changelog — experimental-strip-types](https://nodejs.org/en/blog/release/v22.6.0) — anúncio oficial da feature no ramo 22
- [Node.js 22.18 LTS — TypeScript support stable in v22](https://nodejs.org/en/blog/release/v22.18.0) — versão LTS do ramo 22 que consolida o suporte
- [Node.js 24 Release — TypeScript without experimental flags](https://nodejs.org/en/blog/release/v24.0.0) — estabilização no Node 24
- [tsx — GitHub repository](https://github.com/privatenumber/tsx) — repositório oficial, instalação e documentação
- [ts-node — Documentation](https://typestrong.org/ts-node/) — documentação oficial, incluindo integração SWC
- [TypeScript: tsconfig reference](https://www.typescriptlang.org/tsconfig) — referência completa de todas as opções do tsconfig

---

## Veja também

- [[Tooling e ecossistema moderno]] — índice do galho 7
- [[03 - ESM vs CJS - módulos no Node moderno]] — nota anterior no galho
- [[03-Dominios/Node/index|Node.js (MOC central)]] — visão geral de todos os galhos da trilha Node Senior
- [[Node.js]] — tronco da trilha Node Senior
