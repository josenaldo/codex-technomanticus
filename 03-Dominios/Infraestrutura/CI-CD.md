---
title: "CI/CD"
created: 2026-04-11
updated: 2026-04-11
type: concept
status: evergreen
tags:
  - infraestrutura
  - devops
  - entrevista
publish: false
---

# CI/CD

Deep dive em **Continuous Integration e Continuous Delivery/Deployment** — automação de build, test, release e deploy. Para containers, ver [[Docker]]. Para K8s, ver [[Kubernetes]]. Para observabilidade, ver [[Observabilidade]].

## O que é

**CI (Continuous Integration)** — prática de **integrar código frequentemente** (várias vezes por dia) em uma branch compartilhada, com **testes automatizados** validando cada integração. Objetivo: detectar bugs cedo, reduzir merge hell, manter código sempre "releasable".

**CD** tem dois significados:

- **Continuous Delivery** — código sempre pronto para deploy em produção. Deploy é **manual mas trivial** (um clique).
- **Continuous Deployment** — código vai automaticamente para produção após passar nos testes. Sem intervenção humana.

```
Developer → commit/PR → CI pipeline → tests pass → deploy pipeline
                              ↓
                         feedback rápido
                        (minutos, não dias)
```

**Por que CI/CD importa:**

- **Feedback rápido** — bugs caros de consertar aparecem em horas, não semanas
- **Deploys menores** — menos risco, rollback fácil
- **Confiança para refatorar** — testes automatizados protegem mudanças
- **Menos manual work** — libera devs para pensar, não clicar
- **Rastreabilidade** — cada deploy tem history, audit
- **Cultura DevOps** — dev e ops trabalham juntos com objetivos comuns

**Em 2026**, CI/CD é **obrigatório** em qualquer projeto sério. Empresas que não têm já estão para trás.

Em entrevistas, o que diferencia um senior em CI/CD:

1. **Entender a pirâmide DORA** — deploy frequency, lead time, MTTR, change failure rate
2. **Pipeline bem projetado** — estágios rápidos primeiro, lentos depois
3. **Test pyramid no CI** — unit → integration → E2E → smoke
4. **Security no pipeline** — SAST, DAST, SCA, secrets scanning
5. **Estratégias de deploy** — rolling, blue-green, canary, feature flags
6. **GitOps** — Git como fonte de verdade, ArgoCD/Flux
7. **Observability de pipelines** — metrics, alertas, feedback
8. **IaC (Infrastructure as Code)** — Terraform, Pulumi, CDK
9. **Secrets management** — Vault, AWS Secrets Manager, nunca em git
10. **DORA metrics** — medir o que importa

---

## Conceitos fundamentais

### Pipeline

Sequência de estágios que seu código passa desde commit até produção:

```
Commit → Build → Unit Tests → Integration Tests → Security Scan →
Package (Docker image) → Deploy Staging → E2E Tests → Approval →
Deploy Production → Smoke Tests → Done
```

Cada estágio **pode falhar**, parando o pipeline e dando feedback ao autor.

### CI vs CD vs Continuous Deployment

```
┌──────┐    ┌──────────────────┐    ┌──────────────────────┐
│  CI  │ →  │   Continuous     │ →  │  Continuous          │
│      │    │   Delivery       │    │  Deployment          │
└──────┘    └──────────────────┘    └──────────────────────┘
Build +     Build + Test +          Build + Test +
Test         Deploy to staging       Deploy to prod
              (manual approval       automaticamente
               para prod)            (sem human)
```

**Hoje em 2026**, deployment automático é possível e praticado por empresas maduras (Netflix, Amazon, GitHub). Requer:

- Test suite muito confiável
- Feature flags
- Monitoring e rollback automático
- Cultura de "você quebrou, você conserta"

Para maioria das empresas, **Continuous Delivery com deploy manual para prod** é o sweet spot.

### Trunk-based vs GitFlow

**Trunk-based development** (moderno, recomendado):

- Todos trabalham em **main** (trunk)
- Branches curtas (< 1 dia)
- Merge frequente, muitas vezes por dia
- Feature flags para features incompletas
- Release = tag em main

**GitFlow** (legado, evitar):

- Branches long-lived: main, develop, feature/*, release/*, hotfix/*
- Merges complexos
- Releases raros
- Mais overhead

Em 2026, **trunk-based + feature flags + CD** é o padrão. GitFlow é considerado anti-pattern para a maioria dos times.

### DORA metrics

DevOps Research and Assessment — 4 métricas que correlacionam com performance:

| Métrica | High performers | Elite |
| --- | --- | --- |
| **Deployment Frequency** | 1x/dia a 1x/semana | On-demand (muitas por dia) |
| **Lead Time for Changes** | < 1 dia | < 1 hora |
| **Change Failure Rate** | 0-15% | 0-15% |
| **Mean Time to Restore (MTTR)** | < 1 dia | < 1 hora |

**Meça isso no seu time.** Metrics in, insights out.

---

## GitHub Actions

Em 2026, **GitHub Actions** é a plataforma CI/CD mais popular. Integração nativa com GitHub, ecossistema enorme, grátis para projetos públicos e generous free tier para privados.

### Conceitos

- **Workflow** — arquivo `.yml` em `.github/workflows/` que define o pipeline
- **Job** — grupo de steps rodando na mesma máquina
- **Step** — ação individual (shell command ou action)
- **Action** — componente reutilizável (marketplace)
- **Runner** — máquina que executa (GitHub-hosted ou self-hosted)
- **Event** — trigger (push, PR, schedule, manual, ...)

### Hello world

```yaml
# .github/workflows/ci.yml
name: CI

on:
    push:
        branches: [main]
    pull_request:
        branches: [main]

jobs:
    test:
        runs-on: ubuntu-latest
        steps:
            - uses: actions/checkout@v4

            - uses: actions/setup-node@v4
              with:
                  node-version: '22'
                  cache: 'npm'

            - run: npm ci
            - run: npm run lint
            - run: npm test
            - run: npm run build
```

### Triggers

```yaml
on:
    push:
        branches: [main, develop]
        paths:
            - 'src/**'
            - 'package*.json'
        tags: ['v*']

    pull_request:
        branches: [main]

    schedule:
        - cron: '0 3 * * *'     # todo dia 3am UTC

    workflow_dispatch:          # manual trigger
        inputs:
            environment:
                type: choice
                options: [staging, production]

    release:
        types: [published]

    workflow_run:               # após outro workflow
        workflows: [CI]
        types: [completed]
```

### Matrix builds

Testa em múltiplas versões/OS em paralelo:

```yaml
jobs:
    test:
        strategy:
            fail-fast: false
            matrix:
                os: [ubuntu-latest, macos-latest, windows-latest]
                node: [20, 22, 24]
        runs-on: ${{ matrix.os }}
        steps:
            - uses: actions/checkout@v4
            - uses: actions/setup-node@v4
              with:
                  node-version: ${{ matrix.node }}
            - run: npm test
```

### Secrets

```yaml
- name: Deploy
  env:
      AWS_ACCESS_KEY_ID: ${{ secrets.AWS_ACCESS_KEY_ID }}
      AWS_SECRET_ACCESS_KEY: ${{ secrets.AWS_SECRET_ACCESS_KEY }}
  run: |
      aws s3 sync ./dist s3://my-bucket/
```

Secrets são configurados em **Settings > Secrets and variables > Actions**.

**Environments** permitem secrets scoped e approval gates:

```yaml
jobs:
    deploy-prod:
        environment: production     # requer approval configurado
        runs-on: ubuntu-latest
```

### OIDC — sem secrets estáticos

Melhor que secrets: GitHub Actions pode assumir roles IAM via OIDC, sem credenciais armazenadas.

```yaml
permissions:
    id-token: write
    contents: read

jobs:
    deploy:
        runs-on: ubuntu-latest
        steps:
            - uses: aws-actions/configure-aws-credentials@v4
              with:
                  role-to-assume: arn:aws:iam::123456789:role/deploy-role
                  aws-region: us-east-1

            - run: aws s3 sync ./dist s3://my-bucket/
```

**Configuração:** AWS IAM Identity Provider para GitHub OIDC, role com trust policy apontando para seu repo.

**Benefício:** credenciais **temporárias**, escopo limitado, audit trail. Sem rotação de secrets.

### Reusable workflows

Evite duplicação:

```yaml
# .github/workflows/build.yml (reusable)
on:
    workflow_call:
        inputs:
            node-version:
                type: string
                required: true

jobs:
    build:
        runs-on: ubuntu-latest
        steps:
            - uses: actions/checkout@v4
            - uses: actions/setup-node@v4
              with:
                  node-version: ${{ inputs.node-version }}
            - run: npm ci && npm run build

# .github/workflows/ci.yml (caller)
jobs:
    build:
        uses: ./.github/workflows/build.yml
        with:
            node-version: '22'
```

### Composite actions

Ação customizada em `.github/actions/my-action/action.yml`:

```yaml
name: 'My Action'
inputs:
    name:
        required: true
runs:
    using: 'composite'
    steps:
        - run: echo "Hello ${{ inputs.name }}"
          shell: bash
```

### Cache

```yaml
- uses: actions/cache@v4
  with:
      path: ~/.npm
      key: ${{ runner.os }}-node-${{ hashFiles('**/package-lock.json') }}
      restore-keys: |
          ${{ runner.os }}-node-

# Ou use cache built-in de setup-*
- uses: actions/setup-node@v4
  with:
      cache: 'npm'
```

### Self-hosted runners

Para workloads especializadas (GPU, licenças) ou network restrito. Instale o runner agent em sua máquina e registre no GitHub.

**Cuidado:** self-hosted runners expõem sua infraestrutura. Não use em repos públicos sem isolamento.

---

## GitLab CI/CD

Alternativa ao GitHub Actions. Integração nativa com GitLab, pipelines como código via `.gitlab-ci.yml`.

```yaml
# .gitlab-ci.yml
stages:
    - build
    - test
    - deploy

variables:
    NODE_VERSION: "22"

build:
    stage: build
    image: node:22-alpine
    script:
        - npm ci
        - npm run build
    artifacts:
        paths:
            - dist/
        expire_in: 1 week

test:
    stage: test
    image: node:22-alpine
    script:
        - npm ci
        - npm test

deploy-prod:
    stage: deploy
    image: alpine:latest
    before_script:
        - apk add --no-cache rsync openssh-client
    script:
        - rsync -az dist/ user@prod:/var/www/
    only:
        - main
    environment:
        name: production
        url: https://app.example.com
    when: manual
```

**Features:**

- **Stages** e dependencies explícitas
- **Artifacts** entre jobs
- **Environments** com URLs
- **Protected variables**
- **Parent-child pipelines**
- **DAG** com `needs`

**GitLab vs GitHub Actions:**

- GitLab: mais integrado (issues, CI, registry, IAM tudo junto)
- GitHub Actions: marketplace maior, mais comunidade
- Ambos são excelentes. Escolha depende de onde seu código mora.

---

## Outras plataformas

### CircleCI

Popular, fast, boa UX. `.circleci/config.yml`. Orbs (equivalente a actions). Free tier generoso.

### Jenkins

Veterano (2011), self-hosted, poderoso mas complexo. Jenkinsfile (Groovy ou declarativo). Ainda comum em empresas grandes com investimento legacy. **Evite para projetos novos.**

### Azure Pipelines

Parte do Azure DevOps. Bom se já está no ecossistema Microsoft.

### Bitbucket Pipelines

Se já usa Bitbucket. `bitbucket-pipelines.yml`.

### Drone CI

Self-hosted, container-native. Lightweight.

### Buildkite

Híbrido (UI cloud, runners self-hosted). Popular em empresas médias/grandes.

### Woodpecker CI

Fork open-source do Drone. Crescendo.

**Em 2026, GitHub Actions + ArgoCD é a stack mais popular.** GitLab CI em segundo.

---

## Pipeline design

### Estrutura padrão

```
┌─────────────────────────────────────────────┐
│  1. Checkout + Setup  (< 1 min)              │
├─────────────────────────────────────────────┤
│  2. Lint + Format     (< 1 min)              │
├─────────────────────────────────────────────┤
│  3. Unit Tests        (< 2 min)              │
├─────────────────────────────────────────────┤
│  4. Build             (< 3 min)              │
├─────────────────────────────────────────────┤
│  5. Integration Tests (< 5 min)              │
├─────────────────────────────────────────────┤
│  6. Security Scan     (< 2 min)              │
├─────────────────────────────────────────────┤
│  7. Build Docker      (< 3 min)              │
├─────────────────────────────────────────────┤
│  8. Push Registry     (< 2 min)              │
├─────────────────────────────────────────────┤
│  9. Deploy Staging    (< 3 min)              │
├─────────────────────────────────────────────┤
│ 10. E2E Tests         (< 10 min)             │
├─────────────────────────────────────────────┤
│ 11. Deploy Prod       (< 3 min)              │
├─────────────────────────────────────────────┤
│ 12. Smoke Tests       (< 2 min)              │
└─────────────────────────────────────────────┘

Total: < 30 min idealmente
```

### Princípios

**1. Fail fast** — estágios rápidos primeiro. Lint antes de testes, unit antes de E2E.

**2. Parallel when possible** — unit e linting podem rodar em paralelo.

```yaml
jobs:
    lint: { runs-on: ubuntu-latest, steps: [...] }
    unit: { runs-on: ubuntu-latest, steps: [...] }
    integration:
        needs: [lint, unit]
        runs-on: ubuntu-latest
        steps: [...]
```

**3. Cache aggressively** — node_modules, Maven repo, Docker layers, build artifacts.

**4. Short feedback loop** — 10-15 min ideal para PR feedback. Mais que 30 min é ruim.

**5. Reproducible** — pipeline deve ser determinístico. Random failures são bugs.

**6. Artifacts immutable** — build uma vez, deploy em múltiplos ambientes.

**7. Pipelines as code** — versionado no git, não em UI clicada.

### Test pyramid no CI

```
        ┌─────────────┐
        │   E2E (5)   │ ← 2-10 min, caros
        ├─────────────┤
        │Integration  │ ← 5-30s cada, moderados
        │   (20-50)   │
        ├─────────────┤
        │Unit Tests   │ ← ms cada, baratos, milhares
        │  (100s+)    │
        └─────────────┘
```

- **Unit** — roda em cada commit, feedback em segundos
- **Integration** — roda em PR
- **E2E** — roda em PR (críticos) + em deploy staging (smoke)

Ver [[Testes em JavaScript]] e [[Testes em Java]] para deep dive.

### Build matrix para múltiplos ambientes

```yaml
strategy:
    matrix:
        environment: [staging, production]
        include:
            - environment: staging
              url: https://staging.example.com
            - environment: production
              url: https://example.com
              requires_approval: true
```

---

## Security no pipeline

### SAST (Static Application Security Testing)

Analisa código-fonte para vulnerabilidades.

**Ferramentas:**

- **SonarQube / SonarCloud** — análise multi-language
- **CodeQL** (GitHub) — integrado, grátis em repos públicos
- **Semgrep** — fast, rules customizáveis
- **Snyk Code**

```yaml
# GitHub CodeQL
- uses: github/codeql-action/init@v3
  with:
      languages: javascript, typescript
- uses: github/codeql-action/analyze@v3
```

### DAST (Dynamic Application Security Testing)

Testa app rodando contra ataques comuns.

**Ferramentas:**

- **OWASP ZAP** — grátis, popular
- **Burp Suite** — comercial, profissional
- **Nuclei** — template-based

### SCA (Software Composition Analysis)

Verifica dependências de terceiros (npm, Maven, pip) por CVEs conhecidos.

**Ferramentas:**

- **Dependabot** (GitHub) — integrado, grátis
- **Snyk** — mais completo
- **Trivy** — também para imagens Docker
- **npm audit** / **yarn audit**
- **OWASP Dependency-Check**

```yaml
- name: Run Trivy vulnerability scanner
  uses: aquasecurity/trivy-action@master
  with:
      scan-type: fs
      severity: CRITICAL,HIGH
      exit-code: 1
```

### Secrets scanning

Detecta credenciais commitadas por engano.

**Ferramentas:**

- **GitHub secret scanning** (built-in, grátis)
- **gitleaks** — CLI, roda em pre-commit ou CI
- **TruffleHog**

```yaml
- uses: gitleaks/gitleaks-action@v2
```

### Container scanning

```yaml
- name: Build image
  run: docker build -t myapp:${{ github.sha }} .

- name: Scan with Trivy
  uses: aquasecurity/trivy-action@master
  with:
      image-ref: myapp:${{ github.sha }}
      severity: CRITICAL,HIGH
      exit-code: 1
```

Ver [[Docker]] (seção Security).

### License compliance

Para projetos com dependências open source, verificar licenças:

- **FOSSA** — comercial
- **License Finder** — open source
- **Snyk Open Source**

### Signing e supply chain

- **Sigstore / Cosign** — assinar imagens Docker e artifacts
- **SLSA** (Supply-chain Levels for Software Artifacts) — framework
- **SBOM** (Software Bill of Materials) — lista de componentes

```bash
cosign sign --key cosign.key myapp:1.0
cosign verify --key cosign.pub myapp:1.0
```

---

## Deployment strategies

### 1. Recreate

Para tudo, sobe tudo novo. **Downtime.**

**Quando usar:** incompatibilidade (schema DB que não permite coexistência), dev/staging.

### 2. Rolling update (default K8s)

Substitui Pods gradualmente. **Zero downtime.**

```yaml
strategy:
    type: RollingUpdate
    rollingUpdate:
        maxSurge: 25%
        maxUnavailable: 0
```

Ver [[Kubernetes]].

### 3. Blue-Green

Duas versões rodando, switch instantâneo:

```
Blue (v1, receiving 100% traffic)
Green (v2, ready but idle)

→ switch load balancer →

Blue (v1, idle, can rollback)
Green (v2, receiving 100% traffic)
```

**Prós:** rollback instantâneo, validação em produção, zero downtime.

**Contras:** 2x recursos durante transição, DB schema precisa ser compatible.

### 4. Canary

Pequena porcentagem para nova versão, crescendo:

```
v1 (90% traffic) + v2 (10% traffic)
    ↓ (wait, monitor metrics)
v1 (50%) + v2 (50%)
    ↓
v1 (10%) + v2 (90%)
    ↓
v2 (100%)
```

**Prós:** minimiza blast radius, dá tempo para detectar problemas, confiança crescente.

**Contras:** mais complexo, requer observabilidade madura.

**Ferramentas:**

- **Argo Rollouts** (K8s-native)
- **Flagger** (Flux + service mesh)
- **Istio** / **Linkerd** (traffic splitting)

### 5. A/B testing

Canary baseado em **atributos do user**, não em %:

```
Users com feature_flag=on → v2
Users com feature_flag=off → v1
```

Permite validar hipóteses de produto, não só de infra.

### 6. Feature flags (LaunchDarkly, Unleash, Flagsmith)

**Separar deploy de release.** Deploy código com feature desligada, liga quando quer.

```javascript
if (featureFlags.isEnabled('new-dashboard', { user })) {
    return <NewDashboard />;
}
return <OldDashboard />;
```

**Vantagens:**

- Deploy continuamente sem "liberar" features
- Rollback = flip switch (sem redeploy)
- Gradual rollout por % ou segmento
- Kill switch para emergências

**Regra:** feature flags > branches long-lived. Morte do GitFlow.

---

## GitOps

**Git como fonte de verdade.** Infraestrutura e config declarativa versionada, operator observa e aplica.

```
Dev → commit manifest → Git →
  Operator (ArgoCD/Flux) observa → detecta drift →
    Aplica no cluster → Reconcilia
```

### ArgoCD

Mais popular em 2026. UI web, multi-cluster, Helm/Kustomize support.

```yaml
apiVersion: argoproj.io/v1alpha1
kind: Application
metadata:
    name: myapp-prod
    namespace: argocd
spec:
    project: default
    source:
        repoURL: https://github.com/myorg/k8s-manifests
        targetRevision: main
        path: apps/myapp/prod
    destination:
        server: https://kubernetes.default.svc
        namespace: myapp-prod
    syncPolicy:
        automated:
            prune: true
            selfHeal: true
```

Commit no git → ArgoCD detecta → aplica → cluster reconciliado.

### Flux

Alternativa ao ArgoCD. Mais CNCF, mais lightweight. UI separada.

### Vantagens do GitOps

- **Audit trail** — git log
- **Rollback** — git revert
- **Self-healing** — operator reverte mudanças manuais (drift)
- **Declarativo** — estado desejado em código
- **Review** — PRs em manifests

### Repository strategy

**Mono-repo vs Multi-repo:**

- **App + manifests no mesmo repo** — simples, mas acopla
- **App repo + manifests repo separados** — desacopla, recommended for teams
- **Manifests repo único com diretório por app** — popular

---

## Infrastructure as Code

### Terraform

De facto standard. HCL (HashiCorp Configuration Language).

```hcl
resource "aws_vpc" "main" {
    cidr_block = "10.0.0.0/16"
    tags = { Name = "main" }
}

resource "aws_eks_cluster" "main" {
    name     = "production"
    role_arn = aws_iam_role.eks.arn
    vpc_config {
        subnet_ids = aws_subnet.private[*].id
    }
}
```

```bash
terraform init
terraform plan          # preview
terraform apply         # aplica
terraform destroy
```

**Regras:**

- **State remoto** (S3 + DynamoDB lock) — nunca local em produção
- **Modules** para reuso
- **Workspaces** ou diretórios por environment
- **`terraform plan` em PR** — revisa o que vai mudar

### Pulumi

Infrastructure as Code com **linguagens reais** (TypeScript, Python, Go, .NET).

```typescript
import * as aws from "@pulumi/aws";

const vpc = new aws.ec2.Vpc("main", {
    cidrBlock: "10.0.0.0/16",
    tags: { Name: "main" }
});
```

**Vantagens sobre Terraform:** type-safety, loops/condicionais nativos, IDE support.

### AWS CDK / CDK for Terraform

Similar ao Pulumi, focado em AWS (ou Terraform).

### Ansible

Configuration management (vs orchestration). Útil para setup de VMs, mas IaC moderno prefere Terraform + containers imutáveis.

---

## Secrets management

### Nunca em git

```
❌ .env no repo
❌ hardcoded em código
❌ em CI scripts
```

### Onde guardar

**Cloud native:**

- **AWS Secrets Manager / Parameter Store**
- **GCP Secret Manager**
- **Azure Key Vault**

**Multi-cloud / self-hosted:**

- **HashiCorp Vault** — padrão ouro
- **SOPS** (Mozilla) — criptografa YAML/JSON com chaves GPG/KMS. Commitável no git.
- **Sealed Secrets** (Bitnami) — K8s-specific

### Injeção em runtime

**Kubernetes:**

- **External Secrets Operator** — sincroniza Secrets com Vault/AWS
- **Vault Agent Injector** — inject em tempo de execução

**Docker:**

```bash
docker run --env-file .env myapp
docker run -e DB_PASSWORD=$DB_PASSWORD myapp
```

**CI/CD:**

- GitHub Actions Secrets (ou environments)
- OIDC (best) — sem credenciais estáticas

### Pre-commit hooks

Detecta secrets antes de commit:

```bash
pip install pre-commit
```

```yaml
# .pre-commit-config.yaml
repos:
    - repo: https://github.com/gitleaks/gitleaks
      rev: v8.18.0
      hooks:
          - id: gitleaks
```

---

## Observabilidade do pipeline

### Metrics importantes

- **Build duration** — por job, por stage
- **Success rate** — % de pipelines green
- **Time to first failure** — quanto demora para detectar problema
- **Queue time** — tempo esperando runner
- **Flaky test rate** — % de testes com falha aleatória
- **Pipeline cost** — minutos × custo/min

### Onde visualizar

- **GitHub Insights** — básico
- **Datadog CI Visibility** — completo, comercial
- **Jenkins plugins** — se usa Jenkins
- **Grafana + custom metrics** — flexível

### Alertas

- Master break (CI falhou em main)
- Taxa de sucesso < X%
- Duration > Y min
- Flaky test > Z%

### Notifications

- **Slack** — webhooks ou app oficial
- **Email** — menos usado
- **PagerDuty** — incidentes sérios

```yaml
- name: Notify Slack on failure
  if: failure()
  uses: 8398a7/action-slack@v3
  with:
      status: ${{ job.status }}
      webhook_url: ${{ secrets.SLACK_WEBHOOK }}
```

---

## Exemplo completo: fullstack app

```yaml
# .github/workflows/ci-cd.yml
name: CI/CD

on:
    push:
        branches: [main]
    pull_request:
        branches: [main]

env:
    REGISTRY: ghcr.io
    IMAGE_NAME: ${{ github.repository }}

jobs:
    lint-and-test:
        runs-on: ubuntu-latest
        steps:
            - uses: actions/checkout@v4

            - uses: actions/setup-node@v4
              with:
                  node-version: '22'
                  cache: 'npm'

            - run: npm ci
            - run: npm run lint
            - run: npm run type-check
            - run: npm test -- --coverage

            - name: Upload coverage
              uses: codecov/codecov-action@v4
              with:
                  token: ${{ secrets.CODECOV_TOKEN }}

    security:
        runs-on: ubuntu-latest
        steps:
            - uses: actions/checkout@v4

            - name: Run Trivy
              uses: aquasecurity/trivy-action@master
              with:
                  scan-type: fs
                  severity: CRITICAL,HIGH
                  exit-code: 1

            - name: CodeQL
              uses: github/codeql-action/init@v3
              with:
                  languages: javascript

            - uses: github/codeql-action/analyze@v3

    build-and-push:
        needs: [lint-and-test, security]
        if: github.ref == 'refs/heads/main'
        runs-on: ubuntu-latest
        permissions:
            contents: read
            packages: write
            id-token: write
        outputs:
            image: ${{ steps.meta.outputs.tags }}
        steps:
            - uses: actions/checkout@v4

            - uses: docker/setup-buildx-action@v3

            - uses: docker/login-action@v3
              with:
                  registry: ${{ env.REGISTRY }}
                  username: ${{ github.actor }}
                  password: ${{ secrets.GITHUB_TOKEN }}

            - name: Extract metadata
              id: meta
              uses: docker/metadata-action@v5
              with:
                  images: ${{ env.REGISTRY }}/${{ env.IMAGE_NAME }}
                  tags: |
                      type=sha
                      type=ref,event=branch

            - uses: docker/build-push-action@v5
              with:
                  context: .
                  push: true
                  tags: ${{ steps.meta.outputs.tags }}
                  labels: ${{ steps.meta.outputs.labels }}
                  cache-from: type=gha
                  cache-to: type=gha,mode=max

            - name: Scan built image
              uses: aquasecurity/trivy-action@master
              with:
                  image-ref: ${{ steps.meta.outputs.tags }}
                  severity: CRITICAL
                  exit-code: 1

    deploy-staging:
        needs: build-and-push
        runs-on: ubuntu-latest
        environment: staging
        steps:
            - name: Update staging manifests
              run: |
                  # Atualiza tag em k8s-manifests repo
                  # ArgoCD detecta e aplica
                  curl -X POST "$MANIFEST_API" \
                       -H "Authorization: $TOKEN" \
                       -d '{"tag": "${{ needs.build-and-push.outputs.image }}"}'

    e2e-staging:
        needs: deploy-staging
        runs-on: ubuntu-latest
        steps:
            - uses: actions/checkout@v4
            - uses: actions/setup-node@v4
              with:
                  node-version: '22'
            - run: npm ci
            - run: npx playwright install --with-deps
            - run: npx playwright test --config=playwright.staging.config.ts

    deploy-prod:
        needs: e2e-staging
        runs-on: ubuntu-latest
        environment: production       # requires manual approval
        steps:
            - name: Update production manifests
              run: |
                  curl -X POST "$MANIFEST_API/prod" \
                       -H "Authorization: $TOKEN" \
                       -d '{"tag": "${{ needs.build-and-push.outputs.image }}"}'
```

---

## Armadilhas comuns

- **Pipelines lentos (> 30 min)** — desanimam devs, quebram feedback loop
- **Flaky tests** — erodem confiança. Trate como bugs, não "retry until green".
- **Sem cache** — build repetitivo, lento
- **Secrets em logs** — `echo $SECRET` vaza
- **Deploy manual para prod sem gate** — erro humano
- **Pipeline sem rollback** — deploy ruim = longo downtime
- **`latest` como tag** — não é reprodutível
- **Sem artifact storage** — rebuild ao deploy
- **Unit test no E2E stage** — ordem errada
- **Build em máquina dev** — "funciona aqui, não no CI"
- **Sem lint** — bugs triviais chegam ao review
- **Sem security scan** — vulnerabilidades em produção
- **Secrets estáticos em vez de OIDC** — risco de vazamento
- **Pipelines diferentes entre staging e prod** — "staging passa, prod falha"
- **Sem smoke tests após deploy** — erro só detectado por usuário
- **Branches long-lived + merge hell** — use trunk-based
- **Sem feature flags** — deploy = release, sem controle
- **Manifests em UI clicada** — não versionado, sem audit
- **Jenkinsfiles gigantes** — difícil manter
- **Copy-paste entre workflows** — use reusable workflows
- **Sem workflow de release** — tags inconsistentes
- **Coverage gate muito agressivo** — gaming das métricas
- **Testes críticos em E2E apenas** — lento, flaky
- **Sem notifications** — ninguém sabe que quebrou
- **Pipelines sem owner** — quebra e fica quebrado
- **Deploy em sexta às 5pm** — clássico, evite

---

## Na prática (da minha experiência)

> **MedEspecialista — pipeline GitHub Actions + ArgoCD:**
>
> **CI (GitHub Actions):**
>
> 1. Lint + type-check + unit tests — ~2 min, paralelo
> 2. Integration tests com Testcontainers — ~4 min
> 3. Trivy scan em filesystem + dependências
> 4. Build Docker multi-stage com BuildKit cache
> 5. Trivy scan na imagem final
> 6. Push para GHCR com tag `sha-<hash>`
>
> **CD (ArgoCD):**
>
> 1. Workflow atualiza tag em repo de manifests
> 2. ArgoCD detecta diff em repositório
> 3. Aplica em cluster staging
> 4. Playwright E2E suite contra staging
> 5. Se passa, manifest de prod é atualizado (requer approval)
> 6. ArgoCD sincroniza prod
>
> **Decisões importantes:**
>
> **1. OIDC em vez de AWS keys.** GitHub Actions assume role via OIDC, sem credenciais estáticas. Zero risco de vazamento.
>
> **2. Trunk-based + feature flags.** Sem branches long-lived. Features incompletas atrás de flags. Merge para main várias vezes por dia.
>
> **3. Todos os testes obrigatórios em PR.** Nenhum "optional". Lint, unit, integration, security scan. Se falhou, não merga.
>
> **4. Dependabot semanal.** Auto-PR para updates de dependencies. Review rápido, merge automático de patches.
>
> **5. Pre-commit hooks** — gitleaks, lint, format. Evita perder tempo no CI por erro trivial.
>
> **6. Staging realmente igual a prod.** Mesma imagem, mesmo K8s, mesmas envs variables (com secrets diferentes). "Staging é produção do time, prod é produção do cliente."
>
> **Incidente memorável — deploy quebrado sem rollback fácil:**
>
> Deploy de frontend quebrou todas as funcionalidades. Causa: variável de env `API_URL` apontava para endpoint deprecated no staging. Como deploy era manual via `kubectl apply` (tempos pré-ArgoCD), rollback exigia encontrar manifest antigo + reapply. 20 minutos de downtime. **Lição:** GitOps. Depois disso, `git revert` + ArgoCD sync = rollback em 30 segundos.
>
> **Outro — CI demorando 50 min:**
>
> Pipeline começou a demorar mais de 45 min. Investigação: integration tests spinning up containers um por um. Fix: paralelização com matrix (ubuntu-latest × test-group), Testcontainers reuse, Docker layer caching. Pipeline caiu para 12 min.
>
> **A lição principal:** CI/CD é investimento com retorno enorme. Time economizado em debugging, rollbacks, e stress por deploys é muito maior que tempo gasto configurando. Invista em feedback rápido, security automation, e GitOps desde o dia 1 — será muito mais difícil retrofitar depois.

---

## How to explain in English

> "My CI/CD approach is GitHub Actions for CI plus ArgoCD for continuous delivery to Kubernetes. Pipelines follow fail-fast principles — lint and unit tests first (under 2 minutes for feedback), then integration tests, security scanning with Trivy and CodeQL, container builds, and finally staged deployment to staging and production.
>
> I practice trunk-based development with feature flags rather than long-lived branches. Merges happen multiple times per day, features that aren't ready are hidden behind flags, and GitFlow is considered an anti-pattern for us. This keeps the pipeline green, avoids merge conflicts, and lets us deploy continuously.
>
> For security in the pipeline, I run SAST with CodeQL, SCA with Trivy for both filesystem and container images, and secret scanning with gitleaks both in pre-commit hooks and CI. Critical vulnerabilities fail the build. I use OIDC to assume IAM roles in AWS instead of storing access keys — no static credentials means no credential leakage.
>
> Deployments follow GitOps with ArgoCD. The CI pipeline publishes Docker images and updates tags in a separate manifest repository. ArgoCD watches the manifest repo and reconciles the cluster. Rollback is a git revert — simple and fast. Staging and production are identical except for secrets and scale.
>
> For feedback loops, I aim for PR checks under 15 minutes. Anything longer hurts developer productivity. I use parallel jobs, aggressive caching, and reusable workflows to keep things fast. Test pyramid is enforced — many unit tests, fewer integration, minimal E2E.
>
> Metrics matter. I track DORA metrics — deployment frequency, lead time for changes, change failure rate, and mean time to restore. These four numbers correlate strongly with team performance.
>
> Common pitfalls I watch for: flaky tests (I treat them as bugs, not something to retry), pipelines longer than 30 minutes, secrets in logs, `latest` tags in production, and manual deploys without gates. And the classic — deploying on Friday afternoon."

### Frases úteis em entrevista

- "Trunk-based development with feature flags, not GitFlow."
- "OIDC instead of static credentials — no secrets to leak."
- "GitOps with ArgoCD for declarative continuous delivery."
- "Test pyramid enforced in CI — fast unit tests first."
- "Security scanning (SAST, SCA, container scanning) blocks the pipeline on critical findings."
- "DORA metrics — deployment frequency, lead time, change failure rate, MTTR."
- "Flaky tests are bugs. I fix them, not retry."
- "Pipelines under 15 minutes for PR feedback."
- "Staging is identical to production except for scale and data."
- "Rollback is git revert plus ArgoCD sync — seconds, not minutes."
- "Pre-commit hooks catch issues before they hit CI."

### Key vocabulary

- integração contínua → continuous integration (CI)
- entrega contínua → continuous delivery
- implantação contínua → continuous deployment
- pipeline → pipeline
- executor → runner
- trabalho → job
- etapa → step / stage
- disparador → trigger
- agendamento → schedule / cron
- cache de construção → build cache
- artefato → artifact
- revisão de código → code review
- teste de fumaça → smoke test
- reversão → rollback
- implantação canário → canary deployment
- implantação azul-verde → blue-green deployment
- sinalizador de recurso → feature flag
- segredo → secret
- varredura de vulnerabilidade → vulnerability scanning
- análise estática → static analysis (SAST)
- análise dinâmica → dynamic analysis (DAST)
- composição de software → software composition (SCA)
- infraestrutura como código → infrastructure as code (IaC)
- GitOps → GitOps

---

## Recursos

### Documentação

- [GitHub Actions Docs](https://docs.github.com/en/actions)
- [GitLab CI/CD Docs](https://docs.gitlab.com/ee/ci/)
- [ArgoCD Docs](https://argo-cd.readthedocs.io/)
- [Terraform Docs](https://developer.hashicorp.com/terraform/docs)
- [Pulumi Docs](https://www.pulumi.com/docs/)

### Livros

- **Continuous Delivery** — Jez Humble, David Farley (clássico)
- **Accelerate** — Nicole Forsgren, Jez Humble, Gene Kim (DORA metrics)
- **The DevOps Handbook** — Gene Kim et al.
- **Infrastructure as Code** — Kief Morris

### Cursos e guides

- **Full Stack Open Part 11** — CI/CD (gratuito, Helsinki)
- [DORA State of DevOps Report](https://cloud.google.com/devops) — anual

### Ferramentas essenciais

- [GitHub Actions](https://github.com/features/actions)
- [GitLab CI](https://about.gitlab.com/topics/ci-cd/)
- [ArgoCD](https://argo-cd.readthedocs.io/)
- [Flux](https://fluxcd.io/)
- [Argo Rollouts](https://argoproj.github.io/argo-rollouts/)
- [Flagger](https://flagger.app/)
- [Trivy](https://trivy.dev/)
- [Snyk](https://snyk.io/)
- [Dependabot](https://docs.github.com/en/code-security/dependabot)
- [SonarCloud](https://sonarcloud.io/)
- [CodeQL](https://codeql.github.com/)
- [Gitleaks](https://github.com/gitleaks/gitleaks)
- [pre-commit](https://pre-commit.com/)
- [act](https://github.com/nektos/act) — rodar GitHub Actions localmente
- [Terraform](https://www.terraform.io/)
- [Pulumi](https://www.pulumi.com/)
- [HashiCorp Vault](https://www.vaultproject.io/)
- [External Secrets Operator](https://external-secrets.io/)
- [SOPS](https://github.com/getsops/sops)
- [LaunchDarkly](https://launchdarkly.com/) / [Unleash](https://www.getunleash.io/) — feature flags

### Blogs

- [GitHub Engineering](https://github.blog/category/engineering/)
- [GitLab Blog](https://about.gitlab.com/blog/)
- [HashiCorp Blog](https://www.hashicorp.com/blog)
- [ArgoCD blog](https://blog.argoproj.io/)

---

## Veja também

- [[Docker]] — build de imagens em CI
- [[Kubernetes]] — deploy target
- [[Linux]] — fundação de runners
- [[Nginx]] — deploy de frontend
- [[Observabilidade]] — monitoring de pipelines e apps
- [[Testes em Java]] — CI para backend Java
- [[Testes em JavaScript]] — CI para frontend JS
- [[Arquitetura de Software]] — fitness functions em CI
- [[System Design]] — deploy strategies em escala
