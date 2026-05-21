---
title: "Semver e gerenciamento de dependências"
created: 2026-05-13
updated: 2026-05-13
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
---

# Semver e gerenciamento de dependências

> [!abstract] TL;DR
> Semver define `MAJOR.MINOR.PATCH`: MAJOR quebra API, MINOR adiciona retrocompatível, PATCH corrige bugs sem quebrar. A versão `0.x.y` é pre-stable — qualquer mudança pode quebrar.
> Os operadores `^` (compatível com MAJOR: `>=1.2.3 <2.0.0`) e `~` (compatível com MINOR: `>=1.2.3 <1.3.0`) são os mais usados em `package.json`; evite `*` e `latest` em produção.
> Lockfiles (`package-lock.json`, `pnpm-lock.yaml`, `yarn.lock`, `bun.lock`) garantem reprodutibilidade — **sempre comite** em apps; use `npm ci` em pipelines, nunca `npm install`. Automatize atualizações com **Renovate** ou **Dependabot** para manter deps seguras sem risco de quebras silenciosas.

## O que é

O **versionamento semântico** (semver) é uma convenção de três números — `MAJOR.MINOR.PATCH` — que comunica intenção de compatibilidade entre versões de um pacote. Criado por Tom Preston-Werner (cofundador do GitHub), o semver foi adotado pelo npm como padrão universal para o ecossistema [[Node.js]] e é hoje uma das especificações mais importantes do desenvolvimento de software moderno.

No contexto do npm, o semver não é apenas uma convenção de nomenclatura: ele é a base de toda a **resolução de dependências**. Quando você escreve `"express": "^4.18.2"` no `package.json`, o npm não instala exatamente a versão `4.18.2` — ele instala a versão mais recente compatível com o range que o operador `^` define. Isso significa que builds em momentos diferentes podem instalar versões diferentes, e é exatamente por isso que o **lockfile** existe: para gravar a versão exata resolvida e garantir que todo ambiente (desenvolvimento, CI, produção) instale os mesmos bytes.

A **reprodutibilidade de builds** é crítica em produção. Um bug que aparece só em produção e não reproduz localmente é frequentemente um problema de versão — alguma dep resolveu diferente em algum ambiente. O lockfile elimina essa variável. Com mais de 2 milhões de pacotes publicados no npm registry, cada um com seus próprios ranges de versão e grafo de dependências transitivas, a chance de resolução não-determinística sem lockfile é real e constante.

---

## Como funciona

### MAJOR.MINOR.PATCH

O semver define três componentes, cada um com semântica precisa:

- **MAJOR** (`X.0.0`): mudança incompatível com versões anteriores — quebra de API pública. Código que funciona com `express@4.x` pode quebrar com `express@5.x`. Ao incrementar o MAJOR, MINOR e PATCH são zerados.
- **MINOR** (`x.Y.0`): nova funcionalidade retrocompatível — adiciona coisas sem remover. Código escrito para `1.2.0` deve continuar funcionando com `1.3.0`. Ao incrementar o MINOR, o PATCH é zerado.
- **PATCH** (`x.y.Z`): correção de bug retrocompatível — não adiciona nem remove funcionalidade, apenas corrige comportamento incorreto.

**Regras de incremento na prática:**

| Mudança | Versão anterior | Versão nova |
|---------|----------------|-------------|
| Corrigiu bug no parser | `2.3.1` | `2.3.2` |
| Adicionou novo método à API | `2.3.2` | `2.4.0` |
| Removeu parâmetro obrigatório | `2.4.0` | `3.0.0` |
| Renomeou função exportada | `2.4.0` | `3.0.0` |

**Versão `0.x.y` — pre-stable:**

Quando o MAJOR é `0`, as regras de estabilidade são relaxadas: qualquer mudança pode quebrar a API pública, mesmo uma mudança MINOR. A versão `0.x.y` sinaliza que a API ainda não está estável e pode mudar a qualquer momento. Só considere a API estável a partir de `1.0.0`.

**Pre-release tags:**

```
1.0.0-alpha.1      → Versão alpha, instável
1.0.0-beta.3       → Versão beta, mais estável que alpha
1.0.0-rc.1         → Release candidate, potencialmente a versão final
```

Pre-releases têm precedência menor que a versão estável equivalente: `1.0.0-rc.1 < 1.0.0`. O npm não instala automaticamente pre-releases, mesmo que atendam ao range declarado — é necessário especificar explicitamente (`"^1.0.0-beta.1"`).

**Build metadata:**

```
1.0.0+build.123    → Build metadata, ignorada para comparação
1.0.0+sha.a1b2c3d  → Referência ao commit de build
```

Build metadata é ignorada pelo npm para comparação de versões: `1.0.0+build.1` e `1.0.0+build.2` são consideradas iguais. Usada principalmente para rastreamento de build em pipelines.

---

### Operadores de range

O `package.json` não exige versões exatas — você pode declarar um **range** que define quais versões são aceitáveis. O npm resolverá para a maior versão disponível dentro do range e registrará a versão exata no lockfile.

```json
{
  "dependencies": {
    "express": "^4.18.2",
    "lodash": "~4.17.0",
    "typescript": "5.4.5",
    "jest": ">=29.0.0 <30.0.0",
    "eslint": ">=8.0.0",
    "some-lib": "^2.0.0 || ^3.0.0",
    "legacy-dep": "*"
  }
}
```

**`^` (caret) — compatível com MAJOR:**

`^1.2.3` resolve para `>=1.2.3 <2.0.0`. É o operador padrão do `npm install` — quando você roda `npm install express`, o npm adiciona `"express": "^4.x.x"` automaticamente. A lógica: o MAJOR não muda, então não há quebra de API.

Atenção especial para versões `0.x.y`:
- `^0.3.4` → `>=0.3.4 <0.4.0` (trata o MINOR como breaking para `0.x`)
- `^0.0.3` → `>=0.0.3 <0.0.4` (trata o PATCH como breaking para `0.0.x`)

**`~` (tilde) — compatível com MINOR:**

`~1.2.3` resolve para `>=1.2.3 <1.3.0`. Mais conservador que `^` — só aceita patches, não novas features. Útil quando o projeto é sensível a mudanças mesmo retrocompatíveis, ou quando a lib tem histórico de introduzir bugs em versões MINOR.

**`*` e `latest` — perigosos:**

`"express": "*"` ou `"express": "latest"` instalam a versão mais recente disponível, incluindo MAJOR releases. Se o `express` lançar uma versão com breaking changes, seu próximo `npm install` instalará essa versão e potencialmente quebrará o projeto. **Nunca use em produção** — use um range explícito e deixe o lockfile fixar a versão.

**Ranges explícitos:**

```json
{
  "node-fetch": ">=2.6.7 <3.0.0",
  "jest": "=29.7.0",
  "webpack": ">=5.0.0"
}
```

- `>=X.Y.Z`: qualquer versão a partir de X.Y.Z
- `<=X.Y.Z`: qualquer versão até X.Y.Z
- `=X.Y.Z`: exatamente esta versão (equivalente a sem operador)

**`||` — disjunção:**

```json
{
  "react": "^17.0.0 || ^18.0.0"
}
```

Útil em libs publicadas para declarar compatibilidade com múltiplas gerações de uma dep. O npm instalará a maior versão disponível que satisfaça qualquer um dos ranges.

---

### Lockfiles e reprodutibilidade

O **lockfile** é o contrato de versões exatas entre todos os ambientes que rodam o projeto. Ele registra não apenas as versões diretas, mas todo o grafo resolvido de dependências transitivas — incluindo hashes de integridade para detectar adulteração.

**Lockfiles por package manager:**

| Package manager | Lockfile | Formato |
|----------------|----------|---------|
| npm | `package-lock.json` | JSON |
| pnpm | `pnpm-lock.yaml` | YAML |
| yarn | `yarn.lock` | YAML-like |
| Bun v1.2+ | `bun.lock` | Texto (padrão desde v1.2) |

**Regra fundamental: sempre comite o lockfile em apps.** Libs publicadas no npm podem omitir o lockfile do git (quem instala a lib resolverá as deps com seu próprio lockfile), mas **apps em produção** devem sempre commitar o lockfile. Sem ele, dois ambientes rodando `npm install` em momentos diferentes podem instalar versões diferentes de deps transitivas.

**`npm ci` vs `npm install`:**

| Comando | Quando usar | Comportamento com lockfile |
|---------|-------------|---------------------------|
| `npm install` | Desenvolvimento local | Lê o lockfile mas pode atualizá-lo se `package.json` mudou; instala no `node_modules` existente |
| `npm ci` | CI/CD, builds reprodutíveis | Exige lockfile existente; **falha** se lockfile e `package.json` estiverem dessincronizados; sempre apaga e recria `node_modules` do zero |

Use `npm ci` em todo pipeline de CI/CD. Ele é mais rápido (sem resolução de conflitos), determinístico, e falha ruidosamente se o lockfile estiver desatualizado — o que é exatamente o comportamento correto em um pipeline.

```yaml
# .github/workflows/ci.yml — exemplo de uso correto do npm ci
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with:
          node-version: '20'
          cache: 'npm'           # Cache do ~/.npm entre runs
      - run: npm ci              # Instala exatamente o lockfile — nunca npm install
      - run: npm test
```

**`package-lock.json` v2 vs v3:**

A partir do npm v7, o lockfile usa o formato v2, que registra o grafo completo incluindo `node_modules` aninhados e suporta workspaces — recursos ausentes no v1. O v3, introduzido no npm v9, é uma versão compacta do v2 que remove o campo `dependencies` redundante mantido no v2 apenas para compatibilidade retroativa com npm 6. O npm v6 gerava v1; npm v7–v8 geram v2 por padrão; npm v9+ geram v3. O lockfile v3 não é legível pelo npm v6 — se precisar de compatibilidade com Node/npm antigos, verifique a versão mínima esperada.

---

### Atualizando dependências com segurança

Declarar um range semver não garante que você recebe automaticamente novas versões — o lockfile fixa a versão exata. Para receber atualizações, é necessário atualizá-lo deliberadamente. Existem três estratégias complementares:

**`npm outdated` — visibilidade do estado atual:**

```bash
npm outdated

# Saída:
# Package    Current  Wanted   Latest   Location
# express    4.18.2   4.19.2   4.21.0   node_modules/express
# lodash     4.17.20  4.17.21  4.17.21  node_modules/lodash
# typescript 5.3.3    5.3.3    5.5.2    node_modules/typescript
```

- **Current**: versão instalada (lockfile)
- **Wanted**: maior versão dentro do range declarado no `package.json`
- **Latest**: última versão disponível no registry (pode incluir MAJOR novo)

**`npm update` — atualiza dentro do range:**

```bash
npm update              # Atualiza todas as deps para o máximo do range declarado
npm update express      # Atualiza apenas o express
```

O `npm update` respeita os ranges do `package.json` — não vai instalar uma versão MAJOR nova se você declarou `^4.x`. Ele atualiza o lockfile para a versão mais recente dentro do range.

**`npx npm-check-updates` (ncu) — mostra e aplica atualizações de MAJOR:**

```bash
# Ver o que pode ser atualizado (incluindo MAJOR)
npx npm-check-updates

# Aplicar as atualizações no package.json (sem instalar)
npx npm-check-updates -u

# Depois, instalar as novas versões
npm install

# Filtrar apenas uma dep específica
npx npm-check-updates express -u

# Atualizar apenas minor e patch (não MAJOR)
npx npm-check-updates --target minor
```

O `ncu` modifica o `package.json` com os ranges atualizados — após rodar, execute `npm install` para atualizar o lockfile. Sempre rode os testes depois: atualizações de MAJOR podem ter breaking changes.

**Renovate — PRs automáticos com máxima configurabilidade:**

O [Renovate](https://docs.renovatebot.com) abre PRs automáticos quando novas versões de deps são publicadas. Ele é altamente configurável: pode agrupar PRs por categoria (devDependencies, production deps, monorepo packages), definir janelas de horário para abrir PRs, testar atualizações em ambientes de staging, e muito mais.

```json
{
  "$schema": "https://docs.renovatebot.com/renovate-schema.json",
  "extends": ["config:recommended"],
  "schedule": ["* 0-8 * * 1"],
  "packageRules": [
    {
      "matchDepTypes": ["devDependencies"],
      "matchUpdateTypes": ["patch", "minor"],
      "automerge": true
    },
    {
      "matchPackagePatterns": ["^@types/"],
      "automerge": true
    },
    {
      "matchUpdateTypes": ["major"],
      "labels": ["major-update"],
      "automerge": false
    }
  ]
}
```

Esse `renovate.json` na raiz do repositório configura o Renovate para: rodar às segundas antes das 9h, fazer automerge automático de patches e minor em devDeps e pacotes `@types/`, e criar PRs com label `major-update` para MAJORs sem automerge.

**Dependabot — integrado ao GitHub, zero-config:**

O Dependabot é a alternativa integrada ao GitHub. Requer apenas um arquivo de configuração em `.github/dependabot.yml`:

```yaml
# .github/dependabot.yml
version: 2
updates:
  - package-ecosystem: "npm"
    directory: "/"
    schedule:
      interval: "weekly"
    groups:
      devDependencies:
        dependency-type: "development"
```

O Dependabot abre um PR por dep por padrão (diferente do Renovate que agrupa). É ideal para projetos simples no GitHub que querem automação com configuração mínima.

**Pinning vs range — quando usar cada um:**

| Estratégia | Quando usar |
|-----------|------------|
| Pinning (`"4.18.2"`) | Apps em produção onde reprodutibilidade absoluta é prioritária; quando uma versão específica foi testada e validada |
| Range (`"^4.18.2"`) | Libs publicadas para não impor versão exata a consumidores; projetos que confiam em Renovate/Dependabot para gerenciar atualizações |
| Range conservador (`"~4.18.2"`) | Projetos sensíveis a mudanças; libs com histórico de bugs em versões MINOR |

---

### overrides e resolutions

Às vezes uma dependência transitiva (dep de uma dep) tem uma vulnerabilidade ou bug que o mantenedor da dep direta ainda não corrigiu. Os **overrides** permitem forçar uma versão específica de uma dep transitiva em todo o grafo.

**`overrides` no npm v8.3+ (Node 16.14+):**

```json
{
  "name": "meu-app",
  "dependencies": {
    "algum-pacote": "^2.0.0"
  },
  "overrides": {
    "minimist": "^1.2.6"
  }
}
```

Isso força qualquer pacote no grafo de dependências que depende de `minimist` (independente de qual versão declara) a instalar `^1.2.6`. Use para corrigir CVEs em deps transitivas enquanto aguarda o patch oficial.

**`pnpm.overrides` para pnpm:**

```json
{
  "name": "meu-app",
  "pnpm": {
    "overrides": {
      "minimist": "^1.2.6",
      "node-fetch@<2.6.7": "2.6.7"
    }
  }
}
```

O pnpm suporta overrides condicionais por versão (`node-fetch@<2.6.7`) — útil quando você quer aplicar o override apenas para versões vulneráveis específicas.

**`resolutions` no yarn:**

```json
{
  "resolutions": {
    "minimist": "^1.2.6",
    "**/node-fetch": "2.6.9"
  }
}
```

O yarn suporta globs no path para afetar deps específicas em subgrafo (`**/node-fetch` força a versão apenas quando `node-fetch` aparece em qualquer dep transitiva).

---

## Quando usar

### Pinning vs range

Use **pinning** (`"express": "4.18.2"`) em **apps em produção** onde reprodutibilidade absoluta importa mais do que receber patches automaticamente. Um app com versões pinnadas só recebe atualizações quando você, deliberadamente, atualiza e re-valida.

Use **range** (`"express": "^4.18.2"`) em **libs publicadas**, para não impor uma versão exata aos consumidores da sua lib. Se sua lib exige exatamente `express@4.18.2`, qualquer projeto que também depende de `express@4.19.0` vai ter conflito ou instalação duplicada. Ranges em libs são cidadãos de primeira classe do ecossistema npm.

### Renovate vs Dependabot

Escolha o **Renovate** quando você precisa de:

- Agrupamento de PRs (todos os patches num único PR semanal, por exemplo)
- Regras sofisticadas por tipo de dep, por nome de pacote, por range de versão
- Automerge condicional (auto-mergear apenas patches de devDeps com CI verde)
- Configuração compartilhada entre múltiplos repositórios (presets)
- Suporte a múltiplos ecossistemas num único config (npm, Docker, GitHub Actions, Python)

Escolha o **Dependabot** quando você quer:

- Zero-config — apenas criar `.github/dependabot.yml` e funciona
- Integração nativa com GitHub security alerts (já vincula CVEs a PRs)
- Um PR por dep (rastreabilidade individual)
- Projeto simples sem necessidade de agrupamento complexo

### `npm ci` em CI

Sempre use `npm ci` em pipelines — nunca `npm install`. O `npm ci` garante que a instalação é idêntica ao lockfile comitado, falha se houver divergência, e recria `node_modules` do zero (sem estado residual de builds anteriores). O `npm install` em CI pode silenciosamente instalar versões diferentes se o lockfile estiver levemente desatualizado — o pior tipo de falha: intermitente e difícil de reproduzir.

---

## Armadilhas comuns

> [!danger] Armadilha 1: Não commitar lockfile em apps

**Descrição:** O lockfile garante que todos os ambientes instalam as mesmas versões exatas de todas as dependências, diretas e transitivas. Sem o lockfile no git, cada `npm install` pode resolver para versões ligeiramente diferentes — e um bug que aparece só em produção pode ser impossível de reproduzir localmente.

**Código problemático:**

```bash
# .gitignore — app de produção
package-lock.json   # ← ERRADO para apps
```

**Fix:** Apenas **libs publicadas** omitem o lockfile do git (pois quem instala a lib terá seu próprio lockfile). **Apps sempre commitam o lockfile**. Remova `package-lock.json` do `.gitignore` se for um app:

```bash
# Remover do .gitignore e adicionar ao git
git rm --cached package-lock.json 2>/dev/null || true
# Edite o .gitignore removendo a linha
git add package-lock.json
git commit -m "chore: track lockfile in git"
```

---

> [!danger] Armadilha 2: Usar `*` ou `latest` em produção

**Descrição:** Usar `*` ou `latest` como range significa que qualquer `npm install` pode instalar a versão mais recente do pacote, incluindo MAJORs com breaking changes. Mesmo com lockfile, qualquer `npm update` ou `npm install <novo-pacote>` pode causar uma re-resolução que pega a nova versão. O resultado é builds não-determinísticos e bugs difíceis de rastrear.

**Código problemático:**

```json
{
  "dependencies": {
    "express": "*",
    "lodash": "latest"
  }
}
```

**Fix:** Use sempre um range explícito com operador semântico + lockfile:

```json
{
  "dependencies": {
    "express": "^4.18.2",
    "lodash": "^4.17.21"
  }
}
```

O `^` garante compatibilidade de MAJOR enquanto permite receber patches e features retrocompatíveis. O lockfile fixa a versão exata resolvida.

---

> [!danger] Armadilha 3: Usar `npm install` em CI em vez de `npm ci`

**Descrição:** O `npm install` em CI pode silenciosamente atualizar o lockfile se houver qualquer divergência entre `package.json` e o lockfile comitado. Isso significa que duas execuções do mesmo pipeline em momentos diferentes podem instalar versões diferentes — e você nunca saberá, porque o CI não falhará.

**Código problemático:**

```yaml
# .github/workflows/ci.yml
- run: npm install   # ← pode atualizar lockfile e instalar versões diferentes
```

**Fix:** Sempre `npm ci` em pipelines:

```yaml
# .github/workflows/ci.yml
- uses: actions/setup-node@v4
  with:
    node-version: '20'
    cache: 'npm'
- run: npm ci        # ← falha ruidosamente se lockfile divergir de package.json
```

O `npm ci` oferece duas garantias fundamentais: instala exatamente o que está no lockfile (sem resolver nada), e falha se `package.json` e o lockfile estiverem fora de sincronia — o que é o comportamento correto para um pipeline de CI.

---

## Em entrevista

### Consistência de dependências entre ambientes

**Pergunta:** "How do you ensure dependency consistency across environments in a Node.js project?"

> "The primary mechanism for dependency consistency is the lockfile — whether that's `package-lock.json` for npm, `pnpm-lock.yaml` for pnpm, `yarn.lock` for yarn, or `bun.lock` for Bun. The lockfile captures the exact resolved version of every dependency in the graph, including transitive ones, along with their integrity hashes. Committing the lockfile to git ensures that every environment — developer machines, CI pipelines, and production deploys — installs precisely the same bytes. The second piece is always running `npm ci` in CI/CD pipelines instead of `npm install`, because `npm ci` reads the lockfile without modifying it and fails loudly if `package.json` and the lockfile diverge, rather than silently resolving to a different set of versions. For long-lived projects, tools like Renovate or Dependabot automate the process of opening pull requests when new versions are available, so the lockfile stays up to date deliberately and with CI validation on each update."

---

### Diferença entre `^` e `~`, e quando pinnar versão exata

**Pergunta:** "What is the difference between `^` and `~` in semver ranges, and when would you pin to an exact version?"

> "The caret `^` locks the MAJOR version and allows updates to MINOR and PATCH — so `^4.18.2` resolves to anything from `4.18.2` up to but not including `5.0.0`. The tilde `~` is more conservative and locks both MAJOR and MINOR, only allowing PATCH updates — so `~4.18.2` resolves to anything from `4.18.2` up to but not including `4.19.0`. In practice, `^` is the npm default and the right choice for most dependencies, because MINOR releases are supposed to be backward compatible per semver contract. I use `~` for packages that have a history of introducing subtle regressions in MINOR releases, or for security-sensitive dependencies where I want tighter control. I pin to an exact version — no operator at all — in two situations: for production applications where I want absolute reproducibility and control every update consciously, or when I've confirmed a specific version works correctly for a known-difficult upgrade and I don't want automatic drift. The trade-off of pinning is that you don't get security patches automatically, so pinning requires pairing with Renovate or Dependabot to open update PRs regularly."

---

### Vulnerabilidade crítica em dependência transitiva

**Pergunta:** "How do you handle a critical security vulnerability in a transitive dependency?"

> "The first step is to understand the exposure: `npm audit` will show the vulnerable package, its severity, and which of your direct dependencies pull it in. If the direct dependency already has a patched version in its latest release, `npm update` or `npm audit fix` will often resolve it automatically — the fix is just updating the direct dep to a version that pins the patched transitive dep. If the direct dep hasn't released a fix yet, the right tool is `overrides` in npm v8.3+ or `pnpm.overrides` in pnpm — you add a field to `package.json` that forces a specific version of the transitive dep regardless of what the direct dep declares. This bypasses the vulnerable version across the entire dependency graph immediately. I always validate the fix with `npm audit` after applying the override to confirm the CVE is cleared, and I track the upstream issue so I can remove the override once the direct dep ships its own fix — overrides are a temporary workaround, not a permanent solution."

---

## Vocabulário

| Português | Inglês |
|-----------|--------|
| versionamento semântico | semantic versioning |
| bloqueio de versões | version locking / lockfile |
| dependência transitiva | transitive dependency |
| resolução de conflito | dependency resolution / conflict resolution |
| fixação de versão | version pinning |
| atualização automatizada | automated dependency updates |
| sobrescrever dependência transitiva | override / resolution |
| intervalo de versão | version range |
| defasagem de dependência | dependency drift |
| auditoria de segurança | security audit |
| compatibilidade retroativa | backward compatibility |
| pré-lançamento | pre-release |
| metadados de build | build metadata |
| grafo de dependências | dependency graph |

---

## Fontes

- [semver.org](https://semver.org) — especificação oficial do versionamento semântico
- [npm Docs — package.json semver](https://docs.npmjs.com/cli/v10/configuring-npm/package-json#dependencies) — npm docs sobre ranges e sintaxe de dependências
- [npm Docs — npm ci](https://docs.npmjs.com/cli/v10/commands/npm-ci) — npm ci para CI/CD
- [Renovate Docs](https://docs.renovatebot.com) — configuração do Renovate para automação de atualizações

---

## Veja também

- [[Tooling e ecossistema moderno]] — MOC do galho 7
- [[01 - Package managers - npm, pnpm, yarn e bun]] — nota anterior
- [[03 - ESM vs CJS - módulos no Node moderno]] — próxima nota
- [[Node.js]] — tronco da trilha Node Senior
