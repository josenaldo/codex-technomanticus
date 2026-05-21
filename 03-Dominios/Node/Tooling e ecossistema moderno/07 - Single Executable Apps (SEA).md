---
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
---

# Single Executable Apps (SEA)

> [!abstract] TL;DR
> Single Executable Applications (SEA) permitem empacotar um script Node.js em um único binário nativo sem precisar que o Node esteja instalado no destino — útil para CLIs distribuíveis e ferramentas internas.
> O processo Node SEA usa `sea-config.json` + `node --experimental-sea-config` + `postject` para injetar o script no binário do Node; disponível como experimental no Node 20, em desenvolvimento ativo no Node 22 (stability 1.1 — a API ainda pode mudar).
> Alternativa mais simples: `bun build --compile` faz o mesmo em um único comando. Principal limitação de ambas as abordagens: o binário final inclui o runtime completo (~60-90 MB), e o Node SEA não suporta addons nativos (`.node` files) nem múltiplos arquivos sem bundling prévio.

## O que é

Single Executable Applications (SEA) é uma feature do Node.js que empacota um script JavaScript (ou um bundle JS) dentro do próprio binário do Node, gerando um executável autossuficiente que não depende de uma instalação de Node no ambiente de destino.

**Casos de uso principais:**

- **CLIs distribuíveis**: ferramentas de linha de comando que podem ser distribuídas como um único arquivo binário para sistemas sem Node instalado — similar ao que Go ou Rust oferecem nativamente.
- **Ferramentas internas**: scripts de automação ou utilitários de equipe que precisam rodar em máquinas de produção ou CI sem instalar o Node.js como dependência.
- **Scripts sem gerenciador de dependências**: automações simples que de outra forma exigiriam `npm install` antes de rodar.
- **Distribuição comercial**: projetos que não querem expor código-fonte em forma de arquivos `.js` legíveis no sistema de arquivos do cliente.

O SEA não substitui Docker ou ambientes de container — o binário ainda é dependente do sistema operacional e da arquitetura (um binário construído no Linux não roda no Windows). Para distribuição cross-platform, é preciso gerar um binário por plataforma alvo.

## Como funciona

### Fluxo Node SEA (experimental Node 20.0.0, active development Node 22 — stability 1.1)

O processo requer cinco etapas manuais:

**1. Criar o bundle JavaScript único**

O SEA só aceita um único arquivo JS de entrada — sem `require()` dinâmico de múltiplos arquivos. Se o projeto tiver múltiplos módulos, é preciso fazer um bundle primeiro (esbuild, rollup, etc.):

```bash
# Bundlar o projeto em um único arquivo (esbuild)
npx esbuild src/index.js --bundle --platform=node --outfile=dist/bundle.js
```

**2. Criar o `sea-config.json`**

```json
{
  "main": "dist/bundle.js",
  "output": "dist/sea-prep.blob",
  "disableExperimentalSEAWarning": true,
  "useSnapshot": false,
  "useCodeCache": true
}
```

- `main`: caminho para o bundle JS (único arquivo de entrada)
- `output`: arquivo blob intermediário que será injetado no binário
- `disableExperimentalSEAWarning`: suprime o aviso `ExperimentalWarning: Single Executable Application` (Node 21.7.0+)
- `useCodeCache`: melhora o tempo de startup compilando o JS antecipadamente (V8 bytecode)

**3. Gerar o blob com o script injetável**

```bash
node --experimental-sea-config sea-config.json
# Output: dist/sea-prep.blob
```

**4. Copiar o binário do Node e injetar o blob via postject**

```bash
# Copiar o binário Node para o nome da sua aplicação
cp $(which node) myapp

# No macOS: remover assinatura de código antes de modificar
# codesign --remove-signature myapp

# Injetar o blob no binário copiado
npx postject myapp NODE_SEA_BLOB dist/sea-prep.blob \
  --sentinel-fuse NODE_SEA_FUSE_fce680ab2cc467b6e072b8b5df1996b2

# No macOS: re-assinar com identidade ad-hoc após injeção
# codesign --sign - myapp
```

**5. Testar o binário gerado**

```bash
./myapp --version  # deve rodar seu bundle, não o node CLI
./myapp            # executa o script empacotado
```

**Assets estáticos:** o `sea-config.json` suporta a chave `assets` para incluir arquivos não-JS (JSON, templates) que podem ser lidos com `require('node:sea').getAsset(key)`:

```json
{
  "main": "dist/bundle.js",
  "output": "dist/sea-prep.blob",
  "assets": {
    "config.json": "src/default-config.json",
    "template.html": "src/template.html"
  }
}
```

```js
// Dentro do bundle, ler um asset embutido:
import { getAsset } from 'node:sea';
const config = JSON.parse(getAsset('config.json', 'utf8'));
```

### bun build --compile (alternativa mais simples)

O Bun oferece compilação em um único comando, sem etapas manuais de postject:

```bash
# TypeScript direto, sem bundle separado
bun build src/index.ts --compile --outfile myapp

# Com target de plataforma (cross-compilation experimental)
bun build src/index.ts --compile --target=bun-linux-x64 --outfile myapp-linux
```

O binário gerado pelo `bun build --compile` inclui o runtime JavaScriptCore (mais leve que o V8) e o script compilado. O resultado final tem tamanho similar ao Node SEA (~50-80 MB), mas o processo é consideravelmente mais simples.

**Limitações do bun compile:**
- Compatibilidade com APIs Node.js não é 100% — alguns módulos que dependem de internos do Node podem não funcionar.
- Ainda em maturação para uso em produção (avisos experimentais em algumas versões).
- Cross-compilation funciona apenas para targets Bun, não para Linux/Windows arbitrários.

### Comparação: Node SEA vs bun compile vs pkg (descontinuado)

| Aspecto | Node SEA | bun build --compile | pkg (descontinuado) |
|---|---|---|---|
| Comando de build | 5 etapas + postject | 1 comando | 1 comando |
| Suporte a TypeScript | Não nativo (precisa bundle) | Nativo | Não nativo |
| Tamanho do binário | ~60-90 MB | ~50-80 MB | ~60-80 MB |
| Compatibilidade Node API | 100% (é o Node) | ~90-95% | ~95% |
| Addons nativos (.node) | Não suportado | Não suportado | Suportado (limitado) |
| Maturidade (2026) | Active development (stability 1.1) | Beta/experimental | Descontinuado (2023) |
| Cross-compilation | Não (gerar por plataforma) | Experimental | Sim |
| Assets estáticos | Sim (via sea-config) | Sim (import attributes) | Sim |

> [!warning] pkg está descontinuado
> O pacote `pkg` (Vercel) foi descontinuado em 2023. Projetos que o usavam devem migrar para Node SEA ou `bun build --compile`. O `@yao-pkg/pkg` é um fork da comunidade, mas sem garantias de manutenção ativa.

## Quando usar

**Use Node SEA quando:**
- O projeto usa APIs Node.js específicas ou addons nativos que não funcionam no Bun.
- A compatibilidade com Node.js é um requisito não negociável.
- O ambiente de destino é Linux/Windows/macOS e o binário precisa ser construído separadamente para cada plataforma.
- O projeto já tem um pipeline de build com esbuild/rollup — adicionar as etapas de SEA é incremental.

**Use bun build --compile quando:**
- O projeto é novo e pode assumir compatibilidade com Bun.
- A simplicidade do pipeline de build é importante (especialmente em CI).
- O projeto usa TypeScript e quer evitar uma etapa de bundle separada.
- O público-alvo usa macOS/Linux x64/arm64 (plataformas melhor suportadas pelo Bun).

**Não use SEA nem bun compile quando:**
- A aplicação precisa de addons nativos (`.node` files, bindings C++).
- O tamanho do binário é uma restrição crítica — ~60 MB é o mínimo.
- O projeto tem muitas dependências com recursos dinâmicos de módulos que não sobrevivem ao bundle.
- Docker ou containers são uma opção viável — a imagem final é mais previsível e reproduzível que um binário SEA.

## Armadilhas comuns

### Armadilha 1: SEA não suporta addons nativos (.node files)

Módulos que dependem de extensões nativas compiladas (`.node` files), como `bcrypt`, `sharp` ou bindings de banco de dados, não podem ser incluídos no blob do SEA. Tentar incluir um bundle que os usa resultará em erro em runtime.

```js
// ❌ Problema: bundle com addon nativo incluído no SEA
// dist/bundle.js importa 'bcrypt' que usa um .node addon
import bcrypt from 'bcrypt';      // bcrypt requer um addon nativo compilado (.node file)
const hash = await bcrypt.hash('password', 10);
// ./myapp → Error: Cannot find module 'bcrypt_lib.node'
// Addons nativos não são encontrados dentro do blob SEA
```

```js
// ✅ Fix: substituir por implementação JS pura para o SEA
import { hash } from 'bcryptjs';  // bcryptjs: implementação JS pura, sem .node
const result = await hash('password', 10);
// Ou: separar o binário SEA de funcionalidades que exigem addons nativos
// e usar Docker/container para casos que precisam de bcrypt nativo
```

### Armadilha 2: Esquecer de gerar um binário por plataforma alvo

Um binário SEA gerado no macOS não roda no Linux e vice-versa — o binário é uma cópia do Node nativo da máquina de build. Distribuir um único binário para múltiplas plataformas requer builds separados, tipicamente em CI.

```js
// ❌ Problema: gerar o binário apenas na máquina local (macOS) e distribuir para Linux
// O binário é um Mach-O (macOS), não um ELF (Linux)
// cp $(which node) myapp   → copia o Node macOS arm64
// npx postject myapp ...
// ./myapp no Linux → exec format error

// ✅ Fix: configurar CI com jobs por plataforma (cada runner gera o binário nativo)
// build-linux: runs-on ubuntu-latest → myapp-linux
// build-macos: runs-on macos-latest  → myapp-macos
// build-win:   runs-on windows-latest → myapp.exe
```

### Armadilha 3: Incluir o diretório node_modules no bundle sem tree-shaking

Se o bundle for gerado com `esbuild --bundle` sem otimização, todas as dependências (incluindo devDependencies não removidas) podem ser incluídas, inflando o blob e o binário final.

```js
// ❌ Problema: bundle sem tree-shaking — inclui dependências desnecessárias
// npx esbuild src/index.js --bundle --platform=node --outfile=dist/bundle.js
// Resultado: bundle.js com 15 MB (inclui lodash completo, tipos TypeScript, etc.)
// Binário final: ~80 MB

// ✅ Fix: ativar minification e tree-shaking, externalizar módulos nativos
// npx esbuild src/index.js \
//   --bundle --platform=node --minify --tree-shaking=true \
//   --external:*.node --outfile=dist/bundle.js
// Resultado: bundle.js com 3 MB → Binário final: ~65 MB
```

## Em entrevista

**Q: What are Single Executable Applications in Node.js and when would you use them?**

Single Executable Applications, or SEA, is a Node.js feature (experimental since Node 20, active development in Node 22 at stability level 1.1 — meaning the API can still change) that bundles a JavaScript script into the Node.js binary itself, producing a standalone executable that runs without Node.js installed on the target machine. The primary use case is distributing command-line tools or automation scripts as a single binary — similar to what Go or Rust developers can do natively. You would reach for SEA when you need to deliver a CLI tool to machines that don't have Node installed, or when you want to avoid shipping `node_modules` directories or requiring users to run `npm install` before using a tool.

**Q: What is the difference between Node SEA and `bun build --compile`, and how do you choose between them?**

Both approaches produce a standalone binary that includes the runtime and your application script, but they differ significantly in ergonomics and compatibility. Node SEA involves five manual steps — generating a blob, copying the Node binary, and injecting with `postject` — while `bun build --compile` does everything in a single command and supports TypeScript natively without a separate bundle step. The trade-off is runtime compatibility: Node SEA literally uses the Node.js runtime, so any code that works with Node will work in the binary; `bun build --compile` uses Bun's JavaScriptCore-based runtime, which has approximately 90-95% Node.js API compatibility. If your project relies on Node-specific internals or native addons, Node SEA is the only option; for greenfield TypeScript CLIs where simplicity matters, `bun build --compile` is the faster path.

**Q: What are the main limitations of Node SEA that engineers should know before choosing it?**

The most important limitation is that SEA does not support native addons — modules that use compiled `.node` files, like `bcrypt` or `sharp`, cannot be bundled and will fail at runtime. The second key limitation is platform specificity: the generated binary is a copy of the Node.js binary from the build machine, so you need a separate build for each target platform (Linux x64, Linux arm64, macOS arm64, Windows x64), typically in CI. The third limitation is binary size: because the full Node.js runtime is included, the minimum binary size is around 60-90 MB, which can be a concern for lightweight utility tools. Finally, SEA requires that all application code be bundled into a single JavaScript file before injection, which means adding an esbuild or rollup step to the build pipeline if the project has multiple modules.

## Vocabulário

| Português | Inglês |
|---|---|
| Aplicação executável única | Single Executable Application (SEA) |
| Binário | Binary / executable |
| Runtime embutido | Embedded runtime |
| Ativo estático | Static asset |
| Injeção de blob | Blob injection |
| Compilação antecipada | Ahead-of-time compilation (AOT) |
| Addon nativo | Native addon |
| Compilação cruzada | Cross-compilation |
| Empacotamento | Bundling |
| Assinatura de código | Code signing |

## Fontes

- [Node.js Docs — Single Executable Applications](https://nodejs.org/api/single-executable-applications.html) — documentação oficial com o fluxo completo de build
- [Node.js 20.0.0 Changelog — SEA introduced](https://nodejs.org/en/blog/release/v20.0.0) — anúncio da feature como experimental
- [postject — npm](https://www.npmjs.com/package/postject) — ferramenta de injeção de blobs em binários
- [Bun Docs — bun build --compile](https://bun.sh/docs/bundler/executables) — documentação do bun compile para binários autossuficientes

## Veja também

- [[Tooling e ecossistema moderno]] — índice do galho 7
- [[06 - DX flags modernos - watch, env-file e import]] — nota anterior no galho
- [[08 - Promise-based core APIs]] — próxima nota no galho
- [[09 - Bun como runtime alternativo]] — Bun como runtime alternativo, com bun compile
- [[Node.js]] — tronco da trilha Node Senior
- [[03-Dominios/Node/index|Node.js (MOC central)]] — visão geral de todos os galhos da trilha Node Senior
