# Galho 7 — Tooling e ecossistema moderno: Plano de Execução

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Criar 10 notas atômicas + 1 MOC em `03-Dominios/Node/Tooling e ecossistema moderno/` cobrindo o ecossistema de ferramentas modernas do Node.js (package managers, semver, ESM vs CJS, TypeScript nativo, test runner, DX flags, SEA, Promise APIs e Bun), e podar as seções correspondentes do tronco `Node.js.md`. Contexto: maio de 2026 — npm v10, pnpm v9, yarn v4 (Berry), Bun (adquirido pela Anthropic), Node 22.18 LTS com `--experimental-strip-types`, Node 24 com TypeScript nativo estável.

**Architecture:** Cada nota é um arquivo Markdown independente em `03-Dominios/Node/Tooling e ecossistema moderno/`. O MOC serve como ponto de entrada com rotas alternativas. O tronco `Node.js.md` é podado ao final com callouts de migração.

**Tech Stack:** Obsidian Flavored Markdown, frontmatter YAML, wikilinks `[[]]`, callouts `[!abstract]`, dataview query no MOC. Package managers: npm v10, pnpm v9, yarn v4 Berry, Bun v1.1+. Runtime: Node 22.18 LTS (`--experimental-strip-types`), Node 24 (TypeScript estável). Módulos: ESM (padrão 2026), CJS (legado/libs). Bundlers mencionados: esbuild, Rollup, tsup.

---

## REGRAS CRÍTICAS PARA O AGENTE EXECUTOR

> ⚠️ **ONE commit per note, NOT bundled.** Cada task = 1 nota = 1 commit dedicado. Commitar múltiplas notas em 1 commit é violação do workflow.
>
> ⚠️ **Nenhuma nota abaixo do mínimo de linhas declarado.** Abaixo do mínimo a nota perde profundidade para o nível senior exigido. O mínimo é piso, não teto.
>
> ⚠️ **"Em entrevista" obrigatoriamente 3+ sentenças em inglês interligadas.** Proibido one-liner.
>
> ⚠️ **Sem Co-Authored-By em commits.** Mensagens seguem o formato: `feat(node/g7): add <número> - <título>`.
>
> ⚠️ **Self-check antes de cada commit** — ver checklist na seção Self-Check abaixo.
>
> ⚠️ **Informações atualizadas para maio de 2026:** npm v10, pnpm v9, yarn v4 Berry, Node 22.18+ com strip-types experimental, Node 24 com TypeScript nativo estável. Nunca referenciar APIs deprecadas como default atual.

## Self-Check (executar antes de cada commit de nota)

```
[ ] Frontmatter completo: title, created, updated, type, status, progresso, publish, tags, aliases (quando aplicável)
[ ] TL;DR callout [!abstract] presente com conteúdo denso (> 3 linhas)
[ ] Contagem de linhas >= mínimo declarado para esta nota
[ ] "Em entrevista" tem 3+ sentenças em inglês (não one-liner)
[ ] "Vocabulário PT→EN" tem >= 6 termos com tradução
[ ] Cada armadilha tem: (a) descrição + (b) código-problema + (c) fix
[ ] "Como funciona" tem >= 3 subsecções (headings ###)
[ ] Número de exemplos de código >= mínimo declarado para esta nota
[ ] Wikilinks para [[Node.js]] e [[Tooling e ecossistema moderno]] (MOC) presentes
[ ] "Fontes" com pelo menos 1 link oficial da ferramenta principal
```

---

## Estrutura de arquivos

**Criar:**

```
03-Dominios/Node/Tooling e ecossistema moderno/
├── index.md                                                (MOC — Task 1)
├── 01 - Package managers - npm, pnpm, yarn e bun.md       (Task 2)
├── 02 - Semver e gerenciamento de dependências.md         (Task 3)
├── 03 - ESM vs CJS - módulos no Node moderno.md           (Task 4)
├── 04 - TypeScript nativo - strip types e integração.md   (Task 5)
├── 05 - Built-in test runner - node-test.md               (Task 6)
├── 06 - DX flags modernos - watch, env-file e import.md   (Task 7)
├── 07 - Single Executable Apps (SEA).md                   (Task 8)
├── 08 - Promise-based core APIs.md                        (Task 9)
├── 09 - Bun como runtime alternativo.md                   (Task 10)
└── 10 - Cheatsheet e decision tree de tooling.md          (Task 11)
```

**Modificar:**

```
03-Dominios/JavaScript/Backend/Node.js.md     (poda: 2 seções → callouts — Task 12)
03-Dominios/Node/index.md                     (adicionar galho 7 — Task 12)
```

---

## Task 1: MOC — Tooling e ecossistema moderno

**Files:**
- Create: `03-Dominios/Node/Tooling e ecossistema moderno/index.md`

**Commit:** `feat(node/g7): add MOC - Tooling e ecossistema moderno`

- [ ] **Step 1: Criar o arquivo MOC**

Criar `03-Dominios/Node/Tooling e ecossistema moderno/index.md` com:

```markdown
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
```

Conteúdo do MOC deve incluir:

1. **Callout `[!abstract] TL;DR`** cobrindo o galho (4+ linhas): o ecossistema de ferramentas em 2026, os 4 package managers (npm v10, pnpm v9, yarn v4, Bun), TypeScript nativo no Node 22+, o test runner embutido `node:test`, DX flags (`--watch`, `--env-file`), SEA e Bun como runtime alternativo da Anthropic.

2. **Seção `## Sobre este galho`** com:
   - Descrição do escopo (2-3 parágrafos)
   - Pré-requisitos: `[[Node.js]]` (tronco), `[[03-Dominios/Node/Runtime e Event Loop/index|Runtime e Event Loop]]` (galho 1)
   - Audiência primária: dev senior prep entrevista internacional
   - Audiência secundária: dev modernizando toolchain de projeto Node existente

3. **Seção `## Comece por aqui — trilha completa (10 notas)`** organizada em blocos:
   - **Bloco A — Fundação**: `[[01 - Package managers - npm, pnpm, yarn e bun]]`, `[[02 - Semver e gerenciamento de dependências]]`
   - **Bloco B — Módulos e linguagem**: `[[03 - ESM vs CJS - módulos no Node moderno]]`, `[[04 - TypeScript nativo - strip types e integração]]`
   - **Bloco C — Developer Experience**: `[[05 - Built-in test runner - node-test]]`, `[[06 - DX flags modernos - watch, env-file e import]]`
   - **Bloco D — Features avançadas**: `[[07 - Single Executable Apps (SEA)]]`, `[[08 - Promise-based core APIs]]`, `[[09 - Bun como runtime alternativo]]`
   - **Bloco E — Fechamento**: `[[10 - Cheatsheet e decision tree de tooling]]`

4. **Seção `## Rotas alternativas`** com pelo menos 3 rotas:
   - Rota entrevista (01 → 03 → 04 → 10): package managers + ESM + TypeScript nativo + cheatsheet
   - Rota modernização de projeto (02 → 03 → 04 → 06): semver + ESM + TypeScript + DX flags
   - Rota DX completo (05 → 06 → 07 → 08): test runner + flags + SEA + Promise APIs
   - Rota Bun (09 → 10): runtime alternativo + decision tree

5. **Seção `## Todas as notas`** com query dataview:
   ```dataview
   TABLE status, updated
   FROM "03-Dominios/Node/Tooling e ecossistema moderno"
   WHERE type = "concept"
   SORT file.name ASC
   ```

6. **Seção `## Veja também`** com wikilinks para: `[[Node.js]]`, `[[03-Dominios/Node/index|Node.js (MOC central)]]`, `[[03-Dominios/Node/Runtime e Event Loop/index|Runtime e Event Loop]]`, galhos anteriores relevantes.

**Mínimo de linhas:** 80

---

## Task 2: Nota 01 — Package managers - npm, pnpm, yarn e bun

**Files:**
- Create: `03-Dominios/Node/Tooling e ecossistema moderno/01 - Package managers - npm, pnpm, yarn e bun.md`

**Commit:** `feat(node/g7): add 01 - Package managers - npm, pnpm, yarn e bun`

**Frontmatter:**
```yaml
title: "Package managers - npm, pnpm, yarn e bun"
created: 2026-05-12
updated: 2026-05-12
type: concept
status: seedling
progresso: andamento
publish: false
tags:
  - node
  - npm
  - pnpm
  - yarn
  - bun
  - package-manager
  - tooling
```

**Conteúdo mínimo (350+ linhas):**

1. **Callout `[!abstract] TL;DR`** (4+ linhas): em 2026 existem 4 package managers relevantes — npm v10 (default, bundled com Node), pnpm v9 (mais eficiente via hard links, workspaces superior), yarn v4 Berry (PnP sem node_modules, zero-installs), Bun v1.1+ (o mais rápido de todos, adquirido pela Anthropic). Para projetos novos sem restrições: pnpm; para edge/velocidade máxima: Bun; para compatibilidade máxima: npm.

2. **Seção `## O que é`** explicando:
   - O papel do package manager no ecossistema Node
   - O que é o registry npm e como os 4 managers usam o mesmo
   - Por que existem alternativas ao npm

3. **Seção `## Como funciona`** com subsecções:

   ### npm v10
   - O package manager padrão, bundled com Node
   - `npm ci` vs `npm install` (diferença de lockfile e CI)
   - `package-lock.json` v3 (desde npm v7)
   - `npm workspaces` para monorepos
   - `npm audit` e `npm audit fix` para segurança
   - Scripts principais: `npm run`, `npm exec`, `npx`
   - Snippet: estrutura do package.json com scripts, engines, exports

   ### pnpm v9
   - Hard links + virtual store: instala cada versão de pacote uma vez, compartilha via links
   - `node_modules` com symlinks (compatível com a maioria das ferramentas)
   - `pnpm-workspace.yaml` para monorepos
   - `pnpm store prune` para limpar cache
   - Snippet: instalação básica, workspace config, filtros de monorepo

   ### yarn v4 Berry
   - Plug'n'Play (PnP): sem `node_modules`, imports resolvidos via `.pnp.cjs`
   - Zero-installs: checar `.yarn/cache` no git → deploys sem `yarn install`
   - `yarn dlx` (equivalente ao npx)
   - Snippet: `.yarnrc.yml` config, PnP mode vs node-modules mode

   ### Bun v1.1+
   - JavaScriptCore engine (não V8), implementação nativa em Zig
   - `bun install` — benchmark: 10-25x mais rápido que npm
   - `bun.lockb` (lockfile binário)
   - `bun run`, `bun exec`, `bunx`
   - Compatibilidade com package.json existente
   - Snippet: instalação, `bun add`, `bun remove`

4. **Tabela comparativa** nos eixos: velocidade, node_modules, lockfile, workspaces, compatibilidade, PnP, CI/CD, popularidade 2026.

5. **Seção `## Quando usar`** com decision tree textual:
   - Novo projeto TypeScript sem restrições → pnpm v9
   - Performance máxima de instalação → Bun
   - Monorepo com workspaces → pnpm (melhor DX) ou npm workspaces (menos config)
   - Restrição: equipe quer compatibilidade máxima → npm
   - Zero-installs em CI → yarn v4 Berry com PnP

6. **Seção `## Armadilhas comuns`** (3+ armadilhas com código-problema + fix):
   - Misturar lockfiles de diferentes managers no mesmo projeto
   - `pnpm` em monorepo sem `shamefully-hoist` quebrando ferramentas que assumem `node_modules` flat
   - Bun PnP sem IDE support quebrar intellisense

7. **Seção `## Em entrevista`** com 3+ sentenças em inglês sobre escolha de package manager em 2026.

8. **Seção `## Vocabulário`** PT→EN com 8+ termos: gerenciador de pacotes, registro, bloqueio de versões, workspaces, cache, link físico, link simbólico, resolução de módulo.

9. **Seção `## Fontes`** com links oficiais de todos os 4 managers.

10. **Seção `## Veja também`** com `[[Tooling e ecossistema moderno]]`, `[[02 - Semver e gerenciamento de dependências]]`, `[[Node.js]]`.

**Mínimo de código:** 6 snippets (npm, pnpm, yarn, bun + tabela comparativa + package.json exemplo)

---

## Task 3: Nota 02 — Semver e gerenciamento de dependências

**Files:**
- Create: `03-Dominios/Node/Tooling e ecossistema moderno/02 - Semver e gerenciamento de dependências.md`

**Commit:** `feat(node/g7): add 02 - Semver e gerenciamento de dependências`

**Frontmatter:**
```yaml
title: "Semver e gerenciamento de dependências"
created: 2026-05-12
updated: 2026-05-12
type: concept
status: seedling
progresso: andamento
publish: false
tags:
  - node
  - semver
  - dependências
  - lockfile
  - tooling
```

**Conteúdo mínimo (280+ linhas):**

1. **Callout `[!abstract] TL;DR`** (3+ linhas): Semver define MAJOR.MINOR.PATCH — MAJOR quebra API, MINOR adiciona retrocompatível, PATCH corrige. Os operadores `^` (compatível com MAJOR) e `~` (compatível com MINOR.PATCH) são os mais usados; lockfiles (`package-lock.json`, `pnpm-lock.yaml`, `bun.lockb`) garantem reprodutibilidade. Automatização de atualizações via Renovate ou Dependabot é prática essencial em 2026.

2. **Seção `## O que é`**: introdução ao Semver e por que importa para o ecossistema Node.

3. **Seção `## Como funciona`** com subsecções:

   ### MAJOR.MINOR.PATCH
   - Definição clara de cada componente
   - Regras de incremento (quebra de API, feature nova, bugfix)
   - Versão `0.x.y` (pre-stable: qualquer mudança pode quebrar)

   ### Operadores de range
   - `^1.2.3` → `>=1.2.3 <2.0.0` (padrão do `npm install`)
   - `~1.2.3` → `>=1.2.3 <1.3.0`
   - `*` e `latest` (perigosos)
   - `>=`, `<=`, `=`, `-` (range explícito)
   - `||` para disjunção
   - Snippet: exemplos de cada operador em package.json

   ### Lockfiles e reprodutibilidade
   - Por que commitar o lockfile é obrigatório
   - `npm ci` lê lockfile sem modificar (ideal para CI)
   - `npm install` pode atualizar o lockfile
   - Diferença entre `package-lock.json` v2 vs v3

   ### Atualizando dependências com segurança
   - `npm outdated` e `npm update`
   - `npx npm-check-updates` para ver atualizações de MAJOR
   - Renovate: PRs automáticos agrupados por categoria
   - Dependabot: integrado ao GitHub, PRs individuais
   - Estratégia de pinning vs range em projetos diferentes

   ### overrides e resolutions
   - `overrides` (npm v8+): forçar versão de dependência transitiva
   - `resolutions` (yarn) e `pnpm.overrides` para o mesmo objetivo
   - Snippet: uso de overrides para vulnerabilidade em dep transitiva

4. **Seção `## Quando usar`** com guidance de quando usar cada estratégia (pinning vs range, Renovate vs Dependabot).

5. **Seção `## Armadilhas comuns`** (3+ com código-problema + fix):
   - Não commitar lockfile em bibliotecas (diferente de apps)
   - Usar `*` em produção
   - Não rodar `npm ci` em CI (usar `npm install` perde reprodutibilidade)

6. **Seção `## Em entrevista`** com 3+ sentenças em inglês sobre semver e estratégias de atualização.

7. **Seção `## Vocabulário`** PT→EN (6+ termos): versionamento semântico, bloqueio de dependência, dependência transitiva, resolução de conflito, fixação de versão, atualização automatizada.

8. **Seção `## Fontes`** com link para semver.org e docs do npm.

9. **Seção `## Veja também`** com `[[Tooling e ecossistema moderno]]`, `[[01 - Package managers - npm, pnpm, yarn e bun]]`, `[[Node.js]]`.

**Mínimo de código:** 5 snippets (package.json com ranges, npm ci, overrides, npm outdated, Renovate config exemplo)

---

## Task 4: Nota 03 — ESM vs CJS - módulos no Node moderno

**Files:**
- Create: `03-Dominios/Node/Tooling e ecossistema moderno/03 - ESM vs CJS - módulos no Node moderno.md`

**Commit:** `feat(node/g7): add 03 - ESM vs CJS - módulos no Node moderno`

**Frontmatter:**
```yaml
title: "ESM vs CJS - módulos no Node moderno"
created: 2026-05-12
updated: 2026-05-12
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
```

**Conteúdo mínimo (300+ linhas):**

1. **Callout `[!abstract] TL;DR`** (3+ linhas): ESM (`import`/`export`) é o padrão oficial para novos projetos Node em 2026; CJS (`require`/`module.exports`) é legado mas ainda dominante em bibliotecas publicadas antes de 2022. A distinção fundamental: `require` é síncrono e resolve em runtime, `import` é assíncrono (pode ser top-level `await`) e resolvido estaticamente. Dual publish (`exports` field em package.json) permite oferecer ambos os formatos para libs.

2. **Seção `## O que é`**: histórico dos sistemas de módulo no Node, por que ESM substituiu CJS, timeline de adoção.

3. **Seção `## Como funciona`** com subsecções:

   ### CommonJS (CJS)
   - `require()` síncrono, resolução em runtime
   - `module.exports` e `exports`
   - Wrapping automático em função `(function(module, exports, require, __filename, __dirname) {...})`
   - Caching: `require` retorna o mesmo objeto em chamadas subsequentes
   - Snippet: exemplo de módulo CJS completo

   ### ES Modules (ESM)
   - `import`/`export` estáticos, analisados antes da execução
   - Top-level `await` (ESM only)
   - `import.meta.url`, `import.meta.dirname` (substitui `__dirname`)
   - Named exports, default exports, namespace imports
   - Snippet: módulo ESM equivalente ao CJS acima

   ### Como ativar ESM no Node
   - `"type": "module"` no package.json (todos os `.js` → ESM)
   - Extensão `.mjs` para ESM explícito, `.cjs` para CJS explícito
   - Sem `"type": "module"` → `.js` é CJS (default legado)
   - Snippet: package.json com `"type": "module"` + `tsconfig.json` NodeNext

   ### Interop CJS ↔ ESM
   - ESM pode importar CJS com `import pkg from 'cjs-pkg'` (default export = `module.exports`)
   - CJS NÃO pode usar `require()` em módulo ESM (erro sincrónico vs assíncrono)
   - `createRequire` para chamar `require` de dentro de ESM
   - `import()` dinâmico: funciona em CJS para carregar ESM
   - Snippet: `import()` dinâmico em CJS e `createRequire` em ESM

   ### Dual publish de bibliotecas
   - Campo `exports` em package.json com chaves `"import"` e `"require"`
   - Ferramentas: `tsup`, `unbuild` para gerar ESM + CJS simultaneamente
   - Armadilha: dual publish com tipos incorretos (`@types` separados por condicional)
   - Snippet: package.json com `exports` dual + tsup config

4. **Seção `## Quando usar`** com guidance para novos projetos vs libs vs legado.

5. **Seção `## Armadilhas comuns`** (3+ com código-problema + fix):
   - `__dirname` não existe em ESM → usar `import.meta.dirname`
   - `require()` de arquivo `.json` funciona em CJS mas não em ESM (usa `import` com `assert { type: 'json' }` ou `createRequire`)
   - Bibliotecas que exportam apenas CJS dentro de projeto ESM

6. **Seção `## Em entrevista`** com 3+ sentenças em inglês sobre ESM vs CJS e estratégia de migração.

7. **Seção `## Vocabulário`** PT→EN (6+ termos): módulo, resolução de módulo, importação estática, importação dinâmica, exportação nomeada, exportação padrão, publicação dual.

8. **Seção `## Fontes`** com links para a documentação Node.js sobre ESM e CJS.

9. **Seção `## Veja também`** com `[[Tooling e ecossistema moderno]]`, `[[04 - TypeScript nativo - strip types e integração]]`, `[[Node.js]]`.

**Mínimo de código:** 7 snippets (CJS module, ESM module, package.json com type:module, interop import(), createRequire, dual publish exports field, tsup config)

---

## Task 5: Nota 04 — TypeScript nativo - strip types e integração

**Files:**
- Create: `03-Dominios/Node/Tooling e ecossistema moderno/04 - TypeScript nativo - strip types e integração.md`

**Commit:** `feat(node/g7): add 04 - TypeScript nativo - strip types e integração`

**Frontmatter:**
```yaml
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
```

**Conteúdo mínimo (320+ linhas):**

1. **Callout `[!abstract] TL;DR`** (3+ linhas): Node 22.18+ introduz `--experimental-strip-types` — executa arquivos `.ts` removendo anotações de tipo sem transpilação real (enums e namespaces são rejeitados). Node 24+ estabiliza o suporte. Alternativas antes do suporte nativo: `tsx` (dev), `ts-node` com SWC (`ts-node/esm`), `swc-node` (mais rápido). O tsconfig recomendado para Node moderno usa `moduleResolution: "NodeNext"` e `module: "NodeNext"`.

2. **Seção `## O que é`**: diferença entre type stripping e transpilação real, por que o suporte nativo importa.

3. **Seção `## Como funciona`** com subsecções:

   ### --experimental-strip-types (Node 22.18+)
   - O Node remove anotações de tipo e executa o JS resultante
   - Limitações: não suporta `enum`, `namespace`, decorators legados, `const enum`
   - Sem sourcemaps (stack traces podem ser confusos)
   - Sem `paths` aliases (não faz resolução de módulo TypeScript)
   - Snippet: `node --experimental-strip-types app.ts`

   ### --transform-types (Node 22.19+ / Node 24)
   - Adiciona suporte a `enum` usando esbuild internamente
   - Mais lento que strip-types puro por causa do esbuild
   - Node 24: estável e sem a flag experimental
   - Snippet: `node --transform-types app.ts` vs Node 24 sem flag

   ### tsx — o substituto do ts-node
   - `tsx` usa esbuild internamente, suporta TypeScript e ESM
   - `tsx watch` para desenvolvimento com hot reload
   - Suporta `paths` aliases via tsconfig
   - Snippet: instalação e uso básico, `tsx --tsconfig`

   ### ts-node com SWC
   - `ts-node/esm` loader para ESM
   - `@swc/core` como transpiler (mais rápido que tsc)
   - Quando ainda faz sentido (projetos legados com ts-node configurado)
   - Snippet: tsconfig com `ts-node: { swc: true }` e `loader ts-node/esm`

   ### tsconfig para Node moderno
   - `moduleResolution: "NodeNext"` — resolve importações `.js` mesmo em `.ts`
   - `module: "NodeNext"` — gera ESM ou CJS baseado em package.json
   - `target: "ES2022"` ou superior
   - `strict: true` obrigatório
   - Snippet: tsconfig.json completo recomendado para Node 22+

4. **Seção `## Quando usar`** com tabela: Node nativo vs tsx vs ts-node+SWC vs tsc+node.

5. **Seção `## Armadilhas comuns`** (3+ com código-problema + fix):
   - Usar `enum` com `--experimental-strip-types` (não suportado)
   - `paths` aliases do tsconfig não funcionam com node nativo (usar `--import` com loader custom ou tsx)
   - Stack traces sem sourcemap quando se usa strip-types

6. **Seção `## Em entrevista`** com 3+ sentenças em inglês sobre TypeScript nativo no Node e quando substituir tsx/ts-node.

7. **Seção `## Vocabulário`** PT→EN (6+ termos): remoção de tipos, transpilação, mapa de fonte, alias de caminho, resolução de módulo, decorador.

8. **Seção `## Fontes`** com links para: nodejs.org changelog (22.18), repositório tsx, documentação ts-node.

9. **Seção `## Veja também`** com `[[Tooling e ecossistema moderno]]`, `[[03 - ESM vs CJS - módulos no Node moderno]]`, `[[Node.js]]`.

**Mínimo de código:** 6 snippets (strip-types, transform-types, tsx uso, ts-node config, tsconfig NodeNext, package.json com engines)

---

## Task 6: Nota 05 — Built-in test runner - node-test

**Files:**
- Create: `03-Dominios/Node/Tooling e ecossistema moderno/05 - Built-in test runner - node-test.md`

**Commit:** `feat(node/g7): add 05 - Built-in test runner - node-test`

**Frontmatter:**
```yaml
title: "Built-in test runner - node:test"
created: 2026-05-12
updated: 2026-05-12
type: concept
status: seedling
progresso: andamento
publish: false
tags:
  - node
  - testing
  - node-test
  - tooling
  - javascript
aliases:
  - node:test
  - node test runner
```

**Conteúdo mínimo (320+ linhas):**

1. **Callout `[!abstract] TL;DR`** (3+ linhas): `node:test` (disponível desde Node 18, estável em Node 20+) oferece `test`, `describe`, `it`, `before`, `after`, `beforeEach`, `afterEach`, `t.mock.fn`, `t.mock.timers` — sem dependências externas. É competitivo com Vitest para projetos simples. Para Testing Library e JSDOM ainda use Vitest/Jest. `node --test --watch` e reporters (`--test-reporter=spec`) completam o setup básico.

2. **Seção `## O que é`**: histórico da adição do test runner nativo, motivação (zero deps, integrado ao runtime), onde se encaixa vs Vitest/Jest.

3. **Seção `## Como funciona`** com subsecções:

   ### Funções básicas: test, describe, it
   - `test()` e `it()` (alias): teste individual com callback síncrono ou async
   - `describe()` para agrupamento
   - `skip()`, `todo()`, `only()` no contexto de test
   - `t.skip('motivo')` inline
   - Snippet: exemplo completo com describe/test/it/skip

   ### Asserções com node:assert/strict
   - `assert.equal`, `assert.deepEqual`, `assert.strictEqual`
   - `assert.throws`, `assert.rejects`
   - `assert.match` (regex), `assert.doesNotThrow`
   - Snippet: exemplos de cada asserção relevante

   ### Hooks: before, after, beforeEach, afterEach
   - Setup e teardown por suite e por test
   - Snippet: setup de banco de dados com before/after

   ### Mocking: t.mock.fn e t.mock.timers
   - `t.mock.fn(original)` — spy/stub com rastreamento de chamadas
   - `t.mock.method(object, 'method')` — mock de método em objeto
   - `t.mock.timers.enable()` — controle de setTimeout/setInterval
   - `t.mock.reset()` / `t.mock.restore()`
   - Snippet: mock de fetch, mock de setTimeout

   ### Executando testes
   - `node --test` — roda todos os `*.test.(mjs|cjs|js)` e `test/*.js`
   - `node --test --watch` — modo watch nativo
   - `node --test-reporter=spec` — output legível para humanos
   - `node --test-reporter=tap` — para CI/CD
   - `node --test-concurrency=4` — paralelismo
   - Snippet: scripts no package.json para test e test:watch

   ### Comparação com Vitest
   - O que `node:test` tem que Vitest não tem: zero deps, integrado ao runtime
   - O que Vitest tem que `node:test` não tem: snapshot testing, coverage nativo com istanbul, browser mode, JSDOM, Testing Library integration
   - Quando escolher cada um: tabela de decisão

4. **Seção `## Quando usar`** com decision tree: node:test vs Vitest vs Jest.

5. **Seção `## Armadilhas comuns`** (3+ com código-problema + fix):
   - Não especificar `--test` e rodar o arquivo diretamente (testes passam mas não são reportados)
   - `assert.deepEqual` vs `assert.deepStrictEqual` (diferença de tipo)
   - Mocks não restaurados entre testes causando state pollution

6. **Seção `## Em entrevista`** com 3+ sentenças em inglês sobre node:test vs frameworks de teste externos.

7. **Seção `## Vocabulário`** PT→EN (6+ termos): corredor de testes, duplo de teste, espiã de função, gancho, asserção, cobertura de código, modo de observação.

8. **Seção `## Fontes`** com link para documentação oficial `node:test`.

9. **Seção `## Veja também`** com `[[Tooling e ecossistema moderno]]`, `[[06 - DX flags modernos - watch, env-file e import]]`, `[[Node.js]]`.

**Mínimo de código:** 7 snippets (test/describe/it básico, asserções, hooks, mock de função, mock de timers, scripts package.json, tabela Vitest vs node:test)

---

## Task 7: Nota 06 — DX flags modernos - watch, env-file e import

**Files:**
- Create: `03-Dominios/Node/Tooling e ecossistema moderno/06 - DX flags modernos - watch, env-file e import.md`

**Commit:** `feat(node/g7): add 06 - DX flags modernos - watch, env-file e import`

**Frontmatter:**
```yaml
title: "DX flags modernos - watch, env-file e import"
created: 2026-05-12
updated: 2026-05-12
type: concept
status: seedling
progresso: andamento
publish: false
tags:
  - node
  - dx
  - flags
  - watch
  - env-file
  - tooling
aliases:
  - node --watch
  - node --env-file
```

**Conteúdo mínimo (250+ linhas):**

1. **Callout `[!abstract] TL;DR`** (3+ linhas): Node 18-22 introduziu flags que eliminam ferramentas externas comuns: `--watch` substitui nodemon, `--env-file` substitui dotenv, `--import` substitui loaders manuais para registrar hooks de módulo, `--inspect` e `--inspect-brk` ativam o debugger do V8. Conhecer essas flags é diferencial em entrevista — demonstra domínio do runtime sem overhead de dependências.

2. **Seção `## O que é`**: visão geral do movimento de "less is more" no tooling do Node.

3. **Seção `## Como funciona`** com subsecções:

   ### --watch (Node 18+, estável em 22)
   - Reinicia o processo quando arquivos importados mudam
   - `--watch-path` para especificar diretórios adicionais
   - Diferenças do nodemon: não observa `node_modules`, não tem config file complexo
   - Snippet: `node --watch app.js` e `node --watch --watch-path=./src app.js`

   ### --env-file (Node 20.6+)
   - Carrega variáveis de um arquivo `.env` sem `require('dotenv')`
   - Múltiplos arquivos: `--env-file=.env --env-file=.env.local`
   - Não sobrescreve variáveis já definidas no ambiente do processo
   - Snippet: uso básico e com múltiplos arquivos

   ### --import (Node 12+, comum em 22)
   - Pré-carrega um módulo ESM antes da execução do script principal
   - Usado para registrar custom module hooks (`register` API)
   - Exemplo prático: registrar `ts-node/esm` como loader
   - Snippet: `node --import ./register.mjs app.mjs`

   ### --inspect e --inspect-brk (V8 Inspector)
   - `--inspect` abre WebSocket na porta 9229, Chrome DevTools pode conectar
   - `--inspect-brk` quebra na primeira linha (pausa logo no início)
   - `about:inspect` no Chrome para conectar
   - Snippet: `node --inspect app.js` e VS Code launch.json para debug

   ### Outras flags úteis
   - `--max-old-space-size=N` para aumentar heap V8 (em MB)
   - `--enable-source-maps` para stack traces com sourcemaps
   - `--no-warnings` para suprimir experimental warnings em prod
   - `--heap-prof` para heap profiling
   - Tabela: flag → substitui → disponível desde

4. **Seção `## Quando usar`** com guidance sobre quais flags são adequadas para dev vs prod.

5. **Seção `## Armadilhas comuns`** (3+ com código-problema + fix):
   - `--env-file` não expande variáveis (`$HOME` não funciona como em bash)
   - `--watch` não detecta novos arquivos (apenas arquivos já importados no grafo de módulos)
   - Deixar `--inspect` ativo em produção (exposição de porta de debug)

6. **Seção `## Em entrevista`** com 3+ sentenças em inglês sobre modernização de toolchain usando flags nativas.

7. **Seção `## Vocabulário`** PT→EN (6+ termos): modo de observação, arquivo de variáveis de ambiente, pré-carregamento de módulo, depurador, ponto de interrupção, tamanho do heap.

8. **Seção `## Fontes`** com links para changelog do Node.js e docs de CLI flags.

9. **Seção `## Veja também`** com `[[Tooling e ecossistema moderno]]`, `[[05 - Built-in test runner - node-test]]`, `[[07 - Single Executable Apps (SEA)]]`, `[[Node.js]]`.

**Mínimo de código:** 5 snippets (--watch, --env-file, --import, --inspect + VS Code config, tabela de flags)

---

## Task 8: Nota 07 — Single Executable Apps (SEA)

**Files:**
- Create: `03-Dominios/Node/Tooling e ecossistema moderno/07 - Single Executable Apps (SEA).md`

**Commit:** `feat(node/g7): add 07 - Single Executable Apps (SEA)`

**Frontmatter:**
```yaml
title: "Single Executable Apps (SEA)"
created: 2026-05-12
updated: 2026-05-12
type: concept
status: seedling
progresso: andamento
publish: false
tags:
  - node
  - sea
  - binário
  - tooling
  - deploy
aliases:
  - SEA
  - Node SEA
```

**Conteúdo mínimo (220+ linhas):**

1. **Callout `[!abstract] TL;DR`** (3+ linhas): Single Executable Applications (SEA) permitem empacotar um script Node.js em um único binário nativo sem precisar que o Node esteja instalado no destino. O processo usa `sea-config.json` + `node --experimental-sea-config` + `postject` para injetar o script no binário do Node. Alternativa mais simples: `bun build --compile`. Limitações: sem suporte a múltiplos arquivos, sem `require` dinâmico de módulos nativos, tamanho mínimo de ~60 MB (o runtime completo vai junto).

2. **Seção `## O que é`**: casos de uso de SEA (CLIs distribuíveis, ferramentas internas, scripts de automação sem dependência de Node instalado).

3. **Seção `## Como funciona`** com subsecções:

   ### Fluxo Node SEA (Node 21.7+, estável no 22)
   - Passo a passo completo com snippets:
     1. Criar `sea-config.json` com `main` (bundle JS) e `output` (blob)
     2. `node --experimental-sea-config sea-config.json` → gera `.blob`
     3. Copiar o binário Node: `cp $(which node) minhaapp`
     4. Injetar o blob: `npx postject minhaapp NODE_SEA_BLOB dist.blob --sentinel-fuse NODE_SEA_FUSE_fce680ab2cc467b6e072b8b5df1996b2`
     5. Executar: `./minhaapp`
   - `disableExperimentalSEAWarning: true` no sea-config
   - Assets: incluir arquivos estáticos no blob

   ### bun build --compile (alternativa)
   - `bun build app.ts --compile --outfile minhaapp`
   - Um comando, sem postject, sem blob separado
   - Menor overhead: JavaScriptCore é mais leve que V8
   - Limitações: compatibilidade com módulos Node.js (não 100%)

   ### Comparação: Node SEA vs bun compile vs pkg (descontinuado)
   - Tabela: comando, tamanho binário, suporte TypeScript, maturidade, compatibilidade Node API

4. **Seção `## Quando usar`** com guidance: SEA para projetos Node puros sem suporte Bun, bun compile para TypeScript/Bun projects, pkg foi descontinuado.

5. **Seção `## Armadilhas comuns`** (2+ com código-problema + fix):
   - SEA não suporta `require` de addons nativos (`.node` files)
   - O binário final inclui o runtime inteiro (~60-90 MB)

6. **Seção `## Em entrevista`** com 3+ sentenças em inglês sobre quando usar SEA e alternativas.

7. **Seção `## Vocabulário`** PT→EN (6+ termos): aplicação executável única, binário, runtime embutido, ativo estático, injeção de blob, compilação antecipada.

8. **Seção `## Fontes`** com link para docs do Node.js sobre SEA e `bun build --compile`.

9. **Seção `## Veja também`** com `[[Tooling e ecossistema moderno]]`, `[[09 - Bun como runtime alternativo]]`, `[[Node.js]]`.

**Mínimo de código:** 4 snippets (sea-config.json, fluxo completo Node SEA, bun build --compile, tabela comparativa)

---

## Task 9: Nota 08 — Promise-based core APIs

**Files:**
- Create: `03-Dominios/Node/Tooling e ecossistema moderno/08 - Promise-based core APIs.md`

**Commit:** `feat(node/g7): add 08 - Promise-based core APIs`

**Frontmatter:**
```yaml
title: "Promise-based core APIs"
created: 2026-05-12
updated: 2026-05-12
type: concept
status: seedling
progresso: andamento
publish: false
tags:
  - node
  - promises
  - async
  - core-apis
  - tooling
aliases:
  - fs/promises
  - timers/promises
  - stream/promises
```

**Conteúdo mínimo (250+ linhas):**

1. **Callout `[!abstract] TL;DR`** (3+ linhas): Node.js expõe versões Promise-based dos módulos core via submódulos `node:fs/promises`, `node:stream/promises`, `node:timers/promises`, `node:readline/promises` e `node:dns/promises`. Preferir sempre estas sobre as versões callback para código async/await limpo. `stream/promises.pipeline()` é a forma correta de encadear streams sem memory leaks.

2. **Seção `## O que é`**: por que os módulos core ainda têm APIs callback e como os submódulos promises resolvem isso.

3. **Seção `## Como funciona`** com subsecções:

   ### node:fs/promises
   - `readFile`, `writeFile`, `appendFile`, `unlink`, `rename`, `mkdir`, `rm`
   - `stat`, `access`, `readdir`
   - `FileHandle` API (`open` → `read`/`write` → `close`)
   - Snippet: operações de arquivo com async/await

   ### node:stream/promises
   - `pipeline(...streams)` — encadeia streams com cleanup automático em erro
   - `finished(stream)` — aguarda stream terminar ou errar
   - Por que usar `pipeline` em vez de `.pipe()` manual (cleanup de listeners)
   - Snippet: pipeline de arquivo → transform → destino

   ### node:timers/promises
   - `setTimeout(delay, value?)` — promessa que resolve após delay
   - `setInterval(delay)` — async generator para intervalos
   - `setImmediate(value?)` — promessa que resolve no próximo tick do check
   - Snippet: delay com async/await, polling loop com setInterval generator

   ### node:readline/promises
   - `createInterface` + `question()` para input interativo async
   - Iteração linha a linha de arquivo com `for await...of`
   - Snippet: leitura de arquivo linha a linha sem carregar tudo na memória

   ### node:dns/promises
   - `lookup`, `resolve`, `reverse` como promises
   - Snippet: lookup de hostname com async/await

4. **Seção `## Quando usar`**: sempre preferir `node:*` sobre instalar pacotes para operações que o core já cobre.

5. **Seção `## Armadilhas comuns`** (2+ com código-problema + fix):
   - Usar `fs.readFile` (callback) em vez de `fs/promises.readFile` em código async
   - Usar `.pipe()` em vez de `stream/promises.pipeline()` → leak de listeners em erro

6. **Seção `## Em entrevista`** com 3+ sentenças em inglês sobre APIs Promise-based do Node core.

7. **Seção `## Vocabulário`** PT→EN (6+ termos): módulo central, submódulo de promessa, encadeamento de fluxos, iterador assíncrono, leitura de linha, resolução de DNS.

8. **Seção `## Fontes`** com link para docs Node.js de cada submódulo.

9. **Seção `## Veja também`** com `[[Tooling e ecossistema moderno]]`, `[[Node.js]]`, `[[03-Dominios/Node/Streams/index|Streams]]` (galho 3).

**Mínimo de código:** 6 snippets (fs/promises, stream/promises.pipeline, timers setTimeout, timers setInterval generator, readline linha a linha, dns.promises)

---

## Task 10: Nota 09 — Bun como runtime alternativo

**Files:**
- Create: `03-Dominios/Node/Tooling e ecossistema moderno/09 - Bun como runtime alternativo.md`

**Commit:** `feat(node/g7): add 09 - Bun como runtime alternativo`

**Frontmatter:**
```yaml
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
```

**Conteúdo mínimo (280+ linhas):**

1. **Callout `[!abstract] TL;DR`** (3+ linhas): Bun é um runtime JavaScript/TypeScript baseado em JavaScriptCore (não V8), escrito em Zig, adquirido pela Anthropic em 2024. É o runtime mais rápido em benchmarks de I/O e startup, com TypeScript e JSX nativos sem configuração. Inclui runtime + package manager + bundler + test runner em um único binário. Compatibilidade com APIs Node.js é alta mas não 100% — verificar antes de migrar.

2. **Seção `## O que é`**: contexto histórico, aquisição pela Anthropic, posicionamento vs Node e Deno.

3. **Seção `## Como funciona`** com subsecções:

   ### JavaScriptCore vs V8
   - JSC (WebKit engine, usado no Safari) vs V8 (Chrome engine, usado no Node)
   - JSC tem startup mais rápido, V8 tem JIT mais agressivo para código de longa duração
   - Implicações práticas para serverless vs long-running services

   ### Bun como runtime
   - `bun run app.ts` — TypeScript nativo sem configuração
   - `bun run app.jsx` — JSX nativo sem Babel
   - APIs Node.js compatíveis: `node:fs`, `node:path`, `node:http`, `node:crypto`, etc.
   - APIs não-Node: `Bun.file()`, `Bun.serve()`, `Bun.password`, `Bun.sqlite`
   - `Bun.serve()` para servidor HTTP — mais performático que `http.createServer`
   - Snippet: servidor HTTP com Bun.serve

   ### Bun como package manager
   - `bun install` — 10-25x mais rápido que npm
   - `bun.lockb` (lockfile binário, não legível por humanos)
   - Compatível com package.json existente
   - Snippet: comandos bun equivalentes ao npm

   ### Bun como bundler
   - `bun build app.ts --outdir dist` — bundler nativo
   - `bun build --compile` — SEA (binário executável)
   - Suporte a target: browser, bun, node
   - Snippet: bun build básico e --compile

   ### Bun como test runner
   - API compatível com Jest (`test`, `expect`, `describe`, `mock`)
   - `bun test` — executa todos os `*.test.ts`
   - `bun test --watch`
   - Snippet: teste básico com bun test

   ### Compatibilidade com Node.js
   - Alta compatibilidade (Express, Fastify, Prisma, etc. funcionam)
   - Incompatibilidades conhecidas: alguns módulos que usam `v8` diretamente, addons nativos (`.node`)
   - `bun --bun` flag para forçar uso do runtime Bun em scripts npm

4. **Seção `## Quando usar`** com decision tree textual: Bun vs Node em diferentes contextos.

5. **Seção `## Armadilhas comuns`** (3+ com código-problema + fix):
   - `bun.lockb` não é legível — usar `bun install --frozen-lockfile` em CI
   - Algumas diferenças de comportamento do EventEmitter em relação ao Node
   - Módulos com addons nativos (`.node`) não funcionam no Bun

6. **Seção `## Em entrevista`** com 3+ sentenças em inglês sobre Bun vs Node e quando migrar.

7. **Seção `## Vocabulário`** PT→EN (6+ termos): motor JavaScript, tempo de inicialização, kit de ferramentas completo, compilação antecipada, compatibilidade de API, módulo nativo.

8. **Seção `## Fontes`** com links para bun.sh e notas de release.

9. **Seção `## Veja também`** com `[[Tooling e ecossistema moderno]]`, `[[07 - Single Executable Apps (SEA)]]`, `[[01 - Package managers - npm, pnpm, yarn e bun]]`, `[[Node.js]]`.

**Mínimo de código:** 5 snippets (Bun.serve, bun install vs npm, bun build, bun build --compile, bun test)

---

## Task 11: Nota 10 — Cheatsheet e decision tree de tooling

**Files:**
- Create: `03-Dominios/Node/Tooling e ecossistema moderno/10 - Cheatsheet e decision tree de tooling.md`

**Commit:** `feat(node/g7): add 10 - Cheatsheet e decision tree de tooling`

**Frontmatter:**
```yaml
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
```

**Conteúdo mínimo (300+ linhas):**

1. **Callout `[!abstract] TL;DR`** (3+ linhas): Referência rápida de decisão para o ecossistema de tooling Node.js em 2026 — 5 decision trees (package manager, módulos, TypeScript, test runner, runtime), cheatsheet de flags CLI, template de scripts para package.json e comparativos consolidados.

2. **Decision trees** (5 árvores textual/markdown):

   ### Escolha de package manager
   - Projeto novo sem restrições → pnpm v9
   - Deploy serverless / velocidade máxima → Bun
   - Equipe quer compatibilidade máxima → npm v10
   - Zero-installs / CI sem install → yarn v4 Berry (PnP)

   ### ESM vs CJS
   - Novo projeto → `"type": "module"` no package.json (ESM)
   - Biblioteca com dual publish → `exports` field com `"import"` e `"require"`
   - Legado com require() por todo lado → CJS, migrar gradualmente
   - Lib publicada para edge runtimes → ESM puro

   ### TypeScript em Node
   - Dev rápido sem enum/namespace → `node --experimental-strip-types`
   - Precisa de suporte a enums → `tsx` (dev) + `tsc` (build)
   - Node 24+ → strip-types estável, sem flag
   - CI/build de produção → `tsc --noEmit` + `tsx` / `esbuild` para bundle

   ### Test runner
   - Sem deps extras, testes unitários simples → `node:test`
   - Precisa de snapshot, coverage, JSDOM → Vitest
   - Projeto legado já com Jest → manter Jest ou migrar para Vitest

   ### Runtime alternativo
   - Performance máxima + startup rápido + TypeScript nativo → Bun
   - Compatibilidade máxima com ecosistema Node → Node.js
   - Edge runtime (Cloudflare Workers) → Workerd/Miniflare (não Node/Bun)

3. **Cheatsheet de flags CLI** (tabela):
   - `--watch`, `--env-file`, `--import`, `--inspect`, `--inspect-brk`, `--max-old-space-size`, `--experimental-strip-types`, `--transform-types`, `--enable-source-maps`, `--test`, `--test-reporter`, `--test-watch`

4. **Template de scripts** no package.json para projeto típico Node + TypeScript.

5. **Tabela comparativa consolidada** dos 4 package managers com links para notas.

6. **Seção `## Em entrevista`** (3+ perguntas frequentes):
   - Como você escolhe um package manager para um novo projeto?
   - Qual a diferença entre ESM e CJS e quando usar cada um?
   - O que mudou no Node.js com o suporte nativo a TypeScript?

7. **Seção `## Vocabulário consolidado`** PT→EN (8+ termos agregando todo o galho).

8. **Seção `## Veja também`** com links para todas as 9 notas do galho + `[[Node.js]]` + `[[Tooling e ecossistema moderno]]`.

**Mínimo de código:** 4 snippets (package.json scripts template, tabela de flags, tabela package managers, exemplo de dual exports)

---

## Task 12: Poda do tronco e atualização do índice

**Files:**
- Modify: `03-Dominios/JavaScript/Backend/Node.js.md`
- Modify: `03-Dominios/Node/index.md`

**Commit:** `chore(node/g7): prune trunk - 2 sections migrated to tooling galho`

- [ ] **Step 1: Podar `### npm e Package Management` em Node.js.md**

Localizar a seção `### npm e Package Management` (aproximadamente linha 96 de `03-Dominios/JavaScript/Backend/Node.js.md`) e **substituir todo o conteúdo da seção** (mantendo apenas o heading) pelo callout de migração:

```markdown
### npm e Package Management

> [!nota] Migrado para galho próprio
> Package managers, semver e ecossistema npm foram expandidos em [[03-Dominios/Node/Tooling e ecossistema moderno/index|Tooling e ecossistema moderno]] (galho 7). Veja em particular [[01 - Package managers - npm, pnpm, yarn e bun]] (comparativo dos 4 gerenciadores: npm v10, pnpm v9, yarn v4 Berry, bun v1.1+) e [[02 - Semver e gerenciamento de dependências]] (versionamento semântico, lockfiles e estratégias de atualização automatizada com Renovate/Dependabot).
```

- [ ] **Step 2: Podar `### Node moderno — features que você deveria usar` em Node.js.md**

Localizar a seção `### Node moderno — features que você deveria usar` (aproximadamente linha 103 de `03-Dominios/JavaScript/Backend/Node.js.md`) e **substituir todo o conteúdo da seção** (incluindo todos os snippets TypeScript e bash, mantendo apenas o heading) pelo callout de migração:

```markdown
### Node moderno — features que você deveria usar

> [!nota] Migrado para galho próprio
> As features modernas do Node foram expandidas em [[03-Dominios/Node/Tooling e ecossistema moderno/index|Tooling e ecossistema moderno]] (galho 7). Veja em particular [[04 - TypeScript nativo - strip types e integração]] (`--experimental-strip-types` no Node 22.18+), [[05 - Built-in test runner - node-test]] (`node:test` com mock e watch), [[06 - DX flags modernos - watch, env-file e import]] (`--watch`, `--env-file`), [[07 - Single Executable Apps (SEA)]] e [[08 - Promise-based core APIs]] (`fs/promises`, `timers/promises`, `stream/promises`).
```

- [ ] **Step 3: Adicionar link ao `## Veja também` em Node.js.md**

Localizar a seção `## Veja também` em `03-Dominios/JavaScript/Backend/Node.js.md` e adicionar após a linha de galho 6:

```markdown
- [[03-Dominios/Node/Tooling e ecossistema moderno/index|Tooling e ecossistema moderno]] — galho 7 da trilha Node Senior; package managers (npm, pnpm, yarn, Bun), semver, ESM vs CJS, TypeScript nativo, test runner nativo, DX flags, SEA e Bun como runtime
```

- [ ] **Step 4: Adicionar galho 7 ao `03-Dominios/Node/index.md`**

Localizar a linha de galho 6 em `03-Dominios/Node/index.md` e adicionar após ela:

```markdown
- [[03-Dominios/Node/Tooling e ecossistema moderno/index]] — galho 7: package managers (npm, pnpm, yarn, Bun), semver, ESM vs CJS, TypeScript nativo, test runner nativo (`node:test`), DX flags e SEA
```

---

## Checklist final

- [ ] Task 1: MOC `index.md` criado e commitado
- [ ] Task 2: `01 - Package managers - npm, pnpm, yarn e bun.md` criado e commitado
- [ ] Task 3: `02 - Semver e gerenciamento de dependências.md` criado e commitado
- [ ] Task 4: `03 - ESM vs CJS - módulos no Node moderno.md` criado e commitado
- [ ] Task 5: `04 - TypeScript nativo - strip types e integração.md` criado e commitado
- [ ] Task 6: `05 - Built-in test runner - node-test.md` criado e commitado
- [ ] Task 7: `06 - DX flags modernos - watch, env-file e import.md` criado e commitado
- [ ] Task 8: `07 - Single Executable Apps (SEA).md` criado e commitado
- [ ] Task 9: `08 - Promise-based core APIs.md` criado e commitado
- [ ] Task 10: `09 - Bun como runtime alternativo.md` criado e commitado
- [ ] Task 11: `10 - Cheatsheet e decision tree de tooling.md` criado e commitado
- [ ] Task 12: Poda de Node.js.md (2 seções) + atualização de Node/index.md commitados
