---
title: "Package managers - npm, pnpm, yarn e bun"
created: 2026-05-13
updated: 2026-05-13
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
---

# Package managers - npm, pnpm, yarn e bun

> [!abstract] TL;DR
> Em 2026, há 4 gerenciadores de pacotes relevantes para projetos [[Node.js]]: **npm v10** é o default, vem bundled com o Node e cobre 99% dos casos com boa maturidade e compatibilidade universal; **pnpm v9** é o mais eficiente em disco e memória — instala cada versão de pacote uma única vez no store global e usa hard links + symlinks, tornando monorepos rápidos e enxutos; **yarn v4 Berry** aposta em Plug'n'Play (PnP), eliminando `node_modules` por completo via `.pnp.cjs` e habilitando zero-installs em CI ao commitar a cache; **Bun v1.1+** é o mais rápido de todos — 10 a 25× mais rápido que npm no install graças a I/O nativo em Zig, lockfile texto otimizado (padrão desde v1.2) e integração com seu próprio runtime. Para projetos novos sem restrições externas: **pnpm**; para performance máxima de install ou uso em edge/CLI: **Bun**; para compatibilidade máxima com tooling legado ou times conservadores: **npm**. A escolha de package manager não é cosmética — afeta lockfile, hoisting, funcionamento de workspaces, CI cache e reprodutibilidade de builds.

## O que é

### O papel do gerenciador de pacotes no ecossistema Node

Um **gerenciador de pacotes** (package manager) é a ferramenta responsável por instalar, atualizar, remover e auditar as dependências de um projeto [[Node.js]]. Ele lê o `package.json`, resolve o grafo de dependências (incluindo dependências transitivas), baixa os pacotes necessários, os organiza na pasta `node_modules` (ou em estrutura equivalente), e grava um lockfile para garantir reprodutibilidade de builds entre máquinas e ambientes.

Além de instalar pacotes, os gerenciadores modernos oferecem recursos como: execução de scripts (`run`, `exec`), suporte a workspaces para monorepos, auditoria de vulnerabilidades (baseada no banco de dados do npm advisory), gestão de versões de engines e publicação de pacotes no registry.

Sem um gerenciador de pacotes, cada projeto teria que gerenciar manualmente download, versionamento e atualização de bibliotecas — algo inviável em escala com o ecossistema JavaScript, que tem mais de 2 milhões de pacotes publicados.

### O npm registry e como os 4 managers o utilizam

O **npm registry** (`registry.npmjs.org`) é o repositório público central onde os pacotes JavaScript são publicados e distribuídos. Com mais de 2 milhões de pacotes, é o maior registry de software do mundo. **Todos os 4 gerenciadores** — npm, pnpm, yarn e Bun — consomem o mesmo registry por padrão. A diferença entre eles não está em onde buscam os pacotes, mas em como os resolvem, armazenam, organizam localmente e garantem reprodutibilidade.

É possível apontar qualquer desses gerenciadores para um registry privado (Verdaccio, GitHub Packages, Artifactory, JFrog), bastando configurar a URL do registry — a mecânica de resolução e install é a mesma.

```bash
# Exemplo: configurar registry privado no npm
npm config set registry https://registry.minha-empresa.com

# Equivalente no pnpm
pnpm config set registry https://registry.minha-empresa.com

# Equivalente no yarn v4
yarn config set npmRegistryServer https://registry.minha-empresa.com

# Equivalente no Bun
# Em bunfig.toml:
# [install]
# registry = "https://registry.minha-empresa.com"
```

### Por que alternativas ao npm existem

O npm existe desde 2010 e, por muito tempo, tinha limitações sérias: install lento, ausência de lockfile (introduzido apenas em 2017 com npm v5), hoisting flat de dependências que causava o problema do "phantom dependency" (importar pacotes não declarados no seu `package.json` porque eles estavam em `node_modules` por serem transitivos), e performance ruim em monorepos com centenas de pacotes.

O **pnpm** surgiu para resolver o problema de disco e phantom dependencies: ao usar um store global com hard links, cada pacote é instalado uma única vez em todo o sistema, e o `node_modules` usa symlinks — isso impede importar o que não foi declarado. O **yarn** surgiu por pressão de performance e determinismo (o Facebook criou o yarn v1 em 2016 para resolver lentidão do npm da época). O **Bun** surgiu como um runtime alternativo ao Node que inclui um package manager nativo, apostando em velocidade extrema desde o início.

---

## Como funciona

### npm v10

O **npm v10** é o gerenciador padrão que vem instalado junto com o Node.js. Não requer instalação separada — qualquer versão do Node ≥ 18 já inclui npm funcional. Sua vantagem principal é compatibilidade universal: todo pacote, ferramenta de CI/CD e documentação assume que o npm está disponível.

**`npm install` vs `npm ci`:**

| Comando | Quando usar | Comportamento com lockfile |
|---------|-------------|---------------------------|
| `npm install` | Desenvolvimento local | Atualiza `package-lock.json` se `package.json` mudou |
| `npm ci` | CI/CD, builds reprodutíveis | Exige lockfile existente; falha se `package.json` e lockfile estiverem dessincronizados; sempre deleta `node_modules` antes de instalar |

Use `npm ci` em todo pipeline de CI — ele é mais rápido (sem resolver conflitos) e garante builds idênticos ao lockfile comitado.

**`package-lock.json` v3:**

A partir do npm v7, o lockfile usa o formato v3, que registra o grafo completo de dependências incluindo `node_modules` aninhados. Isso torna o lockfile mais confiável para reprodutibilidade mas também maior em tamanho. **Sempre comite o lockfile** — ele é o contrato de versões exatas entre ambientes.

**Workspaces:**

O npm suporta monorepos desde a v7 via `workspaces` no `package.json` raiz:

```json
{
  "name": "meu-monorepo",
  "private": true,
  "workspaces": [
    "packages/*",
    "apps/*"
  ],
  "scripts": {
    "build": "npm run build --workspaces",
    "test": "npm run test --workspaces --if-present",
    "dev": "npm run dev -w apps/web"
  },
  "engines": {
    "node": ">=20.0.0",
    "npm": ">=10.0.0"
  },
  "exports": {
    ".": "./dist/index.js",
    "./utils": "./dist/utils.js"
  }
}
```

**Segurança com `npm audit`:**

```bash
# Verificar vulnerabilidades conhecidas nas dependências
npm audit

# Tentar corrigir automaticamente (apenas minor/patch que não quebram semver)
npm audit fix

# Corrigir incluindo major versions (atenção: pode quebrar compatibilidade)
npm audit fix --force

# Ver o relatório em formato JSON para integrar com scripts de CI
npm audit --json
```

**Scripts principais:**

```bash
npm run <script>     # Executar script definido em package.json
npm exec <pkg>       # Executar binário de pacote instalado
npx <pacote>         # Executar pacote sem instalar (low-to-no install)
npm publish          # Publicar pacote no registry
npm pack             # Criar tarball local sem publicar
npm version patch    # Incrementar versão patch e criar tag git
```

---

### pnpm v9

O **pnpm** (Performant npm) usa uma arquitetura fundamentalmente diferente para armazenar e acessar pacotes. Em vez de copiar arquivos para cada `node_modules` de cada projeto, ele mantém um **store global** (`~/.pnpm-store`) onde cada versão de cada pacote existe uma única vez. Os **arquivos individuais** dentro dos pacotes são acessados por **hard links** diretos ao store — sem nenhuma duplicação de bytes em disco. Já as **entradas de pacote** em `node_modules` (o que você usa ao fazer `require('express')`) são **symlinks** que apontam para o diretório correspondente dentro de `node_modules/.pnpm/<pkg@version>/node_modules/<pkg>/` (o virtual store). É essa separação — hard links para arquivos, symlinks para diretórios de pacotes — que impede phantom dependencies: apenas pacotes explicitamente declarados no `package.json` ficam visíveis na raiz de `node_modules`.

Essa arquitetura traz dois benefícios principais:
1. **Economiza disco**: um projeto com 500 dependências que compartilha 80% com outro projeto ocupa apenas 20% extra de espaço.
2. **Impede phantom dependencies**: `node_modules` é estrito — só estão acessíveis os pacotes declarados no `package.json`. Um pacote transitivo não pode ser importado diretamente pelo seu código.

**Comandos básicos pnpm:**

```bash
# Instalar dependências (equivalente a npm install)
pnpm install

# Adicionar dependência
pnpm add express
pnpm add -D typescript          # devDependency
pnpm add -g pnpm@latest         # global

# Remover dependência
pnpm remove lodash

# Executar script
pnpm run build
pnpm build                       # shorthand (sem "run")

# Limpar o store global de pacotes não referenciados
pnpm store prune

# Verificar integridade do store
pnpm store status

# Executar comando apenas em workspaces com mudanças (CI incremental)
pnpm --filter "...[origin/main]" run test
```

**Workspaces com `pnpm-workspace.yaml`:**

```yaml
# pnpm-workspace.yaml (na raiz do monorepo)
packages:
  - 'packages/*'
  - 'apps/*'
  - '!**/__tests__/**'   # Excluir pastas de test
```

```bash
# Rodar build em todos os workspaces
pnpm -r run build

# Rodar apenas no workspace "web"
pnpm --filter web run dev

# Adicionar pacote apenas no workspace "api"
pnpm --filter api add fastify

# Adicionar dependência local entre workspaces
pnpm --filter web add @meu-projeto/shared@workspace:*
```

O arquivo `.npmrc` na raiz do projeto controla comportamentos do pnpm:

```ini
# .npmrc
shamefully-hoist=false           # Padrão — não hoisteia tudo (mais seguro)
# shamefully-hoist=true          # Habilita hoisting plano (compatibilidade com ferramentas antigas)
strict-peer-dependencies=false   # Evitar falha em peer deps não resolvidas
auto-install-peers=true          # Instalar peer deps automaticamente
```

---

### yarn v4 Berry

O **yarn v4 Berry** representa uma reescrita completa do yarn v1. A mudança mais radical é o **Plug'n'Play (PnP)**: em vez de criar uma estrutura `node_modules` no disco, o yarn gera um único arquivo `.pnp.cjs` que serve como mapa de resolução de módulos. Quando Node.js tenta resolver um `import`, o PnP intercepta e resolve diretamente do cache comprimido em `.yarn/cache`, sem acesso a disco para cada módulo.

**Zero-installs** é a consequência direta: ao commitar `.yarn/cache` no git, qualquer clone do repositório pode rodar sem executar `yarn install` — os pacotes já estão lá, comprimidos como ZIPs. Isso elimina a variável de disponibilidade do registry em deploys.

**Configuração `.yarnrc.yml`:**

```yaml
# .yarnrc.yml — configuração principal do yarn v4
nodeLinker: pnp                   # Modo PnP (padrão do yarn v4)
# nodeLinker: node-modules         # Modo compatível (fallback para ferramentas sem suporte a PnP)

yarnPath: .yarn/releases/yarn-4.x.x.cjs   # Versão do yarn commitada no repo

compressionLevel: mixed           # Compressão das caches
enableGlobalCache: false          # Cache local ao invés de global

# Plugins instalados
plugins:
  - path: .yarn/plugins/@yarnpkg/plugin-interactive-tools.cjs
    spec: "@yarnpkg/plugin-interactive-tools"
```

**Comandos principais yarn v4:**

```bash
# Instalar dependências
yarn install

# Adicionar pacote
yarn add express
yarn add -D @types/node

# Executar pacote sem instalação permanente (equivalente ao npx)
yarn dlx create-next-app@latest meu-projeto

# Rodar script
yarn build
yarn run dev

# Workspaces
yarn workspaces foreach -A run build    # Todos os workspaces
yarn workspace web add react            # Adicionar em workspace específico

# Verificar problemas de dependências
yarn dedupe
yarn constraints
```

**PnP vs node-modules mode:**

| Aspecto | PnP (padrão) | node-modules |
|---------|-------------|--------------|
| Velocidade de install | Muito rápido | Normal |
| Tamanho em disco | ~60% menor | Padrão |
| Zero-installs possível | Sim | Não |
| Compatibilidade com ferramentas | Requer suporte explícito | Universal |
| Phantom dependencies bloqueados | Sim | Não |

Para ferramentas sem suporte a PnP (alguns bundlers legados, IDEs sem plugin), o fallback `nodeLinker: node-modules` no `.yarnrc.yml` permite usar yarn v4 sem PnP.

---

### Bun v1.1+

O **Bun** é um runtime JavaScript que inclui package manager, bundler, test runner e transpiler nativos. Diferentemente de npm, pnpm e yarn — que são ferramentas que gerenciam pacotes para o Node.js — o Bun é um runtime completo construído sobre o motor **JavaScriptCore** (o mesmo do Safari/WebKit) e implementado em **Zig**, uma linguagem de sistemas com performance próxima a C.

O package manager do Bun é integrado ao runtime: `bun install` usa I/O nativo em Zig com operações de arquivo altamente otimizadas, paralelização agressiva de downloads e um **lockfile texto** (`bun.lock`, padrão desde Bun v1.2) — legível por humanos e revisável em pull requests. O formato binário legado `bun.lockb` ainda é suportado mas não é mais o padrão.

**Benchmarks de install (2025–2026, projeto médio ~500 deps):**

| Gerenciador | Tempo (cold cache) | Tempo (warm cache) |
|-------------|--------------------|--------------------|
| npm v10 | ~45s | ~20s |
| pnpm v9 | ~20s | ~8s |
| yarn v4 | ~18s | ~6s |
| Bun v1.1+ | **~4s** | **~1.5s** |

```bash
# Instalar dependências (cria node_modules compatível com Node)
bun install

# Adicionar pacote
bun add express
bun add -d @types/bun             # devDependency
bun add -g bun@latest             # global

# Remover pacote
bun remove lodash

# Executar script (compatível com package.json scripts)
bun run build
bun dev                            # Shorthand se "dev" existe em scripts

# Executar arquivo diretamente (sem compilação prévia)
bun run src/index.ts

# Equivalente ao npx
bunx create-next-app@latest

# Executar comando de pacote local (equivalente a npx/pnpm exec)
bunx tsc --noEmit

# Lockfile texto (padrão desde Bun v1.2) — legível diretamente
cat bun.lock

# Lockfile binário legado — visualizar como texto (se ainda usando bun.lockb)
bun ./bun.lockb
```

O Bun gera um `node_modules` convencional por padrão, garantindo compatibilidade com ferramentas que assumem essa estrutura. Desde Bun v1.2 (início de 2025), o lockfile padrão é `bun.lock` (texto, legível e revisável em PRs). O formato binário legado `bun.lockb` ainda é suportado para projetos existentes.

**Compatibilidade com `package.json` existente:** O Bun lê e respeita `package.json` padrão. Projetos npm/pnpm/yarn podem usar `bun install` como drop-in replacement para install mais rápido, mesmo sem migrar o runtime. É possível ter `package-lock.json` e `bun.lock` coexistindo, mas o recomendado é escolher um e usar `--frozen-lockfile` em CI.

---

## Comparativo geral

| Eixo | npm v10 | pnpm v9 | yarn v4 Berry | Bun v1.1+ |
|------|---------|---------|---------------|-----------|
| **Velocidade install** | Lento | Rápido | Rápido | Ultra-rápido |
| **Uso de disco** | Alto (cópias) | Muito baixo (hard links) | Baixo (PnP) | Baixo |
| **node_modules** | Flat hoisted | Symlinks + virtual store | Não (PnP) ou node-modules | Convencional |
| **Lockfile** | `package-lock.json` (JSON) | `pnpm-lock.yaml` (YAML) | `yarn.lock` (YAML) | `bun.lock` (texto, padrão v1.2+) |
| **Workspaces** | Sim (nativo v7+) | Excelente (pnpm-workspace.yaml) | Sim (nativo) | Sim (nativo) |
| **Compatibilidade** | Universal | Muito alta | Requer suporte PnP | Alta (node_modules mode) |
| **PnP / zero-installs** | Não | Não | Sim (modo padrão) | Não |
| **CI/CD** | Bom (`npm ci`) | Excelente | Excelente (zero-install) | Excelente |
| **Phantom deps bloqueados** | Não | Sim | Sim | Não (modo padrão) |
| **Popularidade 2026** | Dominante | Em ascensão | Estável | Crescendo |
| **Ideal para** | Compatibilidade, legado | Monorepos, eficiência | Zero-installs, equipes grandes | CLIs, edge, máxima velocidade |

---

## Quando usar

### Árvore de decisão textual

**1. Novo projeto TypeScript sem restrições externas:**
→ Use **pnpm v9**. Melhor trade-off entre performance, eficiência de disco, segurança contra phantom deps e tooling maduro.

**2. Performance máxima de install (CI caro ou projetos com muitas deps):**
→ Use **Bun**. A diferença de 10–25× em install frio é real e impacta diretamente custo de CI. Se o projeto usa Node como runtime mas só quer install rápido, basta `bun install` sem migrar o runtime.

**3. Monorepo grande com múltiplos pacotes e apps:**
→ Use **pnpm** (melhor DX, `pnpm-workspace.yaml` mais flexível, filtros por workspace) ou **npm workspaces** se a equipe é conservadora e não quer onboarding adicional.

**4. Equipe exige máxima compatibilidade com ferramentas e não quer aprender nova ferramenta:**
→ Use **npm**. Universal, documentado em todo lugar, suporte nativo de todas as ferramentas de CI/CD.

**5. Deploy sem `npm install` / zero-installs em CI:**
→ Use **yarn v4 Berry** com PnP e `.yarn/cache` commitado no git. O deploy nunca depende de disponibilidade do registry.

**6. Projeto legado Node.js com `node_modules` flat e ferramentas que assumem hoisting:**
→ Use **npm** ou **pnpm com `shamefully-hoist=true`** como transição. Evite PnP sem validar compatibilidade de todas as ferramentas usadas.

**7. CLI ou ferramenta edge que precisa de startup mínimo:**
→ Use **Bun** como runtime e package manager. Startup ~3× mais rápido que Node, APIs compatíveis, sem config extra.

---

## Armadilhas comuns

> [!danger] Armadilha 1: Misturar lockfiles de diferentes package managers no mesmo projeto

**Descrição:** Ter `package-lock.json`, `pnpm-lock.yaml` e `bun.lock` ao mesmo tempo no mesmo repositório significa que cada dev está usando o package manager que preferir. O resultado é que cada ambiente tem versões diferentes de pacotes transitivos, bugs aparecem em produção que não reproduzem em desenvolvimento, e o CI pode instalar versões diferentes a cada build.

**Código problemático:**
```bash
# Dev A usa npm, cria package-lock.json
npm install
git add package-lock.json

# Dev B usa pnpm, cria pnpm-lock.yaml
pnpm install
git add pnpm-lock.yaml

# CI usa yarn, ignora os dois lockfiles acima
yarn install   # Resolve do zero — pode pegar versões diferentes!
```

**Fix:** Escolha um gerenciador e force seu uso via `package.json`:
```json
{
  "packageManager": "pnpm@9.1.0",
  "scripts": {
    "preinstall": "npx only-allow pnpm"
  }
}
```
O campo `packageManager` (suportado pelo Corepack desde Node 16.9) e o script `preinstall` com `only-allow` garantem que qualquer tentativa de usar outro gerenciador falha com mensagem clara. Adicione ao `.gitignore` os lockfiles dos outros managers.

---

> [!warning] Armadilha 2: pnpm em monorepo sem `shamefully-hoist` quebrando ferramentas que assumem `node_modules` flat

**Descrição:** O pnpm não hoisteia dependências transitivas para a raiz de `node_modules` por padrão. Isso é correto do ponto de vista de segurança — mas ferramentas antigas (algumas versões do `jest`, plugins de webpack/vite, SDKs de AWS, ferramentas de CLI que fazem `require('some-transitive-dep')` diretamente) assumem que podem acessar qualquer pacote em `node_modules`, independente de quem o declarou. O resultado é erro de `MODULE_NOT_FOUND` para pacotes que existem na pasta mas não estão acessíveis.

**Código problemático:**
```bash
# Instalar com pnpm (configuração padrão, sem hoist)
pnpm install

# Ao rodar a ferramenta antiga:
# Error: Cannot find module 'some-package'
# (mesmo 'some-package' estando em node_modules/.pnpm/...)
jest --config jest.config.ts
# FAIL  Cannot find module 'ts-jest/utils' from 'jest.config.ts'
```

**Fix — opção 1 (habilitar hoist para um pacote específico):**
```ini
# .npmrc
public-hoist-pattern[]=*ts-jest*
public-hoist-pattern[]=*jest*
public-hoist-pattern[]=@types/*
```

**Fix — opção 2 (hoist completo — último recurso):**
```ini
# .npmrc
shamefully-hoist=true
```
Use `shamefully-hoist=true` apenas como solução temporária enquanto atualiza ou substitui a ferramenta incompatível. O nome "shamefully" é intencional — indica que você está abrindo mão da principal vantagem de segurança do pnpm.

---

> [!danger] Armadilha 3: yarn v4 PnP sem suporte de IDE quebrando intellisense e imports

**Descrição:** O modo PnP do yarn não usa `node_modules` convencional. IDEs (VS Code, WebStorm) precisam de configuração explícita para entender o `.pnp.cjs` e resolver tipos corretamente. Sem isso, o TypeScript Language Server não encontra as definições de tipos, todo import fica sublinhado de vermelho, e autocompletar deixa de funcionar — o projeto compila e roda, mas a experiência de desenvolvimento fica degradada.

**Código problemático:**
```bash
# Instalar em modo PnP (padrão do yarn v4)
yarn install

# Abrir VS Code — imports com erro vermelho mesmo o código funcionando
# "Cannot find module 'express' or its corresponding type declarations"
# TypeScript não consegue encontrar @types/express via PnP

# Tentativa incorreta de resolver: instalar @types globalmente
npm install -g @types/express   # Não resolve — TS precisa do arquivo .pnp.cjs
```

**Fix — instalar o SDK do yarn para o editor:**
```bash
# Gerar arquivos de integração com VS Code
yarn dlx @yarnpkg/sdks vscode

# Para WebStorm / JetBrains
yarn dlx @yarnpkg/sdks base

# Após rodar o comando, aceitar a sugestão do VS Code de usar a versão TypeScript do workspace
# (notificação aparece automaticamente ou via Cmd+Shift+P → "Select TypeScript Version")
```

O comando `yarn dlx @yarnpkg/sdks vscode` gera `.yarn/sdks/` com shims que redirecionam as chamadas do Language Server para o mecanismo PnP. Sem isso, o TS Language Server usa a versão global do TypeScript que não conhece o mapa PnP. **Este passo é obrigatório para qualquer dev novo no projeto** — inclua no README do repositório.

---

## Em entrevista

### Escolhendo package manager em 2026

**Pergunta:** "How do you choose a package manager for a new Node.js project in 2026?"

When asked about this, you can say:

> "My default choice for new projects is pnpm because it solves the two biggest pain points of npm: disk efficiency through hard links and content-addressable storage, and ghost dependency prevention through its strict non-flat node_modules structure. In a monorepo scenario, pnpm's workspace protocol and filter flags give much better developer experience than npm workspaces. If install speed is a critical concern — for example, in a CI pipeline that runs dozens of times per day — I would evaluate Bun as a drop-in replacement for the install step, since it can be 10 to 25 times faster than npm on cold cache without requiring any code changes. For teams that prioritize maximum compatibility with existing tooling and don't want any onboarding friction, npm remains a perfectly valid choice — it ships with Node and every CI provider knows how to cache it correctly."

---

### Diferenças principais entre pnpm e npm

**Pergunta:** "What are the key differences between pnpm and npm, and why would you prefer one over the other?"

When asked about this, you can say:

> "The most important architectural difference is how they store packages on disk. npm copies files into each project's node_modules, which means if you have ten projects using the same version of lodash, you have ten copies on disk. pnpm keeps a single global content-addressable store and uses hard links, so all ten projects share the same bytes. This is why pnpm can be two to three times faster on warm cache and uses dramatically less disk space. The second major difference is module resolution strictness: npm uses a flat hoisted node_modules, which means your code can accidentally import a package that isn't declared in your package.json — it just happens to be there as a transitive dependency. This creates hidden coupling and makes builds fragile when the transitive dependency gets upgraded or removed. pnpm's virtual store with symlinks prevents this entirely. The trade-off is that some older tools assume flat node_modules and will fail with MODULE_NOT_FOUND errors in strict pnpm mode, requiring the shamefully-hoist workaround."

---

### Quando usar Bun como package manager

**Pergunta:** "When would you recommend using Bun as a package manager, and what are the trade-offs?"

When asked about this, you can say:

> "I'd recommend Bun as a package manager in two specific scenarios: first, when install speed is a bottleneck — Bun's native I/O implementation in Zig makes it 10 to 25 times faster than npm on cold cache, which directly reduces CI costs in pipelines that install from scratch frequently. Second, when you're already using Bun as your runtime, since the package manager is deeply integrated and the lockfile format is optimized for Bun's resolver. Since Bun v1.2 the default lockfile is bun.lock, a text format that is human-readable and reviewable in pull requests just like JSON or YAML lockfiles. The legacy binary format bun.lockb is still supported for existing projects. Another consideration is that Bun is newer and moves fast, so some edge cases around specific npm lifecycle hooks or unusual package structures may not be supported yet, though the compatibility story has improved significantly in v1.1. For teams already on npm or pnpm who want faster installs without changing anything else, using bun install as a drop-in replacement for the install step — while keeping the existing runtime and scripts — is a very low-risk way to get the speed benefits."

---

## Vocabulário

| Português | Inglês |
|-----------|--------|
| gerenciador de pacotes | package manager |
| registro (de pacotes) | registry |
| bloqueio de versões | version locking / lockfile |
| workspaces | workspaces (monorepo) |
| cache | cache |
| link físico | hard link |
| link simbólico | symlink / symbolic link |
| resolução de módulo | module resolution |
| dependência fantasma | phantom dependency / ghost dependency |
| hoisting plano | flat hoisting |
| dependência transitiva | transitive dependency |
| zero-instalações | zero-installs |
| armazenamento de conteúdo endereçável | content-addressable store |
| executar localmente sem instalar | run without installing (npx / bunx / yarn dlx) |

---

## Fontes

- [npm Docs — Configuring npm](https://docs.npmjs.com/cli/v10/configuring-npm) — documentação oficial npm v10
- [npm Docs — Workspaces](https://docs.npmjs.com/cli/v10/using-npm/workspaces) — documentação oficial npm workspaces
- [pnpm Documentation](https://pnpm.io/motivation) — documentação oficial pnpm v9
- [pnpm — Workspaces](https://pnpm.io/workspaces) — documentação de workspaces pnpm
- [Yarn Berry — Getting Started](https://yarnpkg.com/getting-started) — documentação oficial yarn v4
- [Yarn Berry — PnP](https://yarnpkg.com/features/pnp) — explicação do Plug'n'Play
- [Bun — Package manager](https://bun.sh/docs/cli/install) — documentação oficial Bun install
- [Bun — Workspaces](https://bun.sh/docs/install/workspaces) — documentação de workspaces Bun

---

## Veja também

- [[Tooling e ecossistema moderno]] — MOC do galho 7 da trilha Node Senior
- [[02 - Semver e gerenciamento de dependências]] — próxima nota: ranges, peer deps, audit, estratégia segura de atualização
- [[Node.js]] — tronco da trilha Node Senior
