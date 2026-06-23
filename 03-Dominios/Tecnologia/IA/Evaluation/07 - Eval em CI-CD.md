---
title: "07 - Eval em CI-CD"
created: 2026-05-28
updated: 2026-05-28
type: concept
status: seedling
progress: in_progress
tags:
  - evaluation
  - ia
  - ci-cd
  - automacao
publish: true
aliases:
  - Eval em CI
  - Eval gates
  - CI/CD evals
---

# 07 - Eval em CI-CD

> [!abstract] TL;DR
> Eval em CI/CD é o que transforma EDD ([[01 - Eval-driven development — a disciplina]]) de boa intenção em disciplina forçada. Padrão canônico: **eval gate em PR** que bloqueia merge se regressão > threshold X. Cada PR de prompt/modelo dispara golden set; merge em main dispara full eval + atualização de baseline. Decisões de design: tamanho de sample por PR (subset top-N pra velocidade vs full pra rigor), threshold por categoria (safety = 0, calibration = 5-10%), quarentena de evals flaky (não-determinísticos precisam tolerância), failing loudly (Slack/PR comment) vs graciosamente (warn-only em early stage). Custo realista de eval por PR: $0.50-$5. Pivot quando custo cresce: amostragem estratificada.

## O contrato eval-em-CI

A garantia que CI/CD com eval entrega:

```
"Nenhum prompt change vai pra main sem ter sido medido."
"Toda regressão > threshold bloqueia merge."
"Toda métrica fica versionada em git."
```

Sem isso, EDD vira ritual — todo mundo concorda que evals importam, ninguém roda.

## Padrão de pipeline

```
Developer push prompt change → PR aberto
                ↓
        CI dispara automaticamente
                ↓
    ┌───────────────────────────────┐
    │ 1. Run eval em subset crítico │  ← fast feedback (~2-5min)
    │ 2. Compara com baseline       │
    │ 3. Reporta no PR              │
    └───────────────────────────────┘
                ↓
       Regressão > threshold?
       /                  \
    SIM                    NÃO
     ↓                      ↓
  Bloqueia              Permite merge
  merge                       ↓
                       Merge em main
                              ↓
                    Roda FULL eval
                    (golden set inteiro)
                              ↓
                  Atualiza baseline em main
```

Duas razões pra split fast / full:

- **Velocidade em PR** — feedback em 2-5min, não 30min
- **Rigor em main** — última verificação antes de produção

## Eval gate em PR — anatomia

```yaml
# .github/workflows/llm-eval.yml
name: LLM Eval

on:
  pull_request:
    paths:
      - "prompts/**"
      - "src/llm/**"
      - "config/models.yaml"

jobs:
  eval:
    runs-on: ubuntu-latest
    timeout-minutes: 15
    steps:
      - uses: actions/checkout@v4

      - uses: actions/setup-node@v4
        with:
          node-version: "20"

      - name: Install promptfoo
        run: npm install -g promptfoo@latest

      - name: Run eval — fast subset
        env:
          OPENAI_API_KEY: ${{ secrets.OPENAI_API_KEY }}
          ANTHROPIC_API_KEY: ${{ secrets.ANTHROPIC_API_KEY }}
        run: |
          promptfoo eval \
            --config promptfooconfig.yaml \
            --filter-tags "critical,safety" \
            --output eval-results.json \
            --no-write

      - name: Check thresholds
        run: |
          node scripts/check-thresholds.js \
            --results eval-results.json \
            --thresholds-config eval-thresholds.yaml

      - name: Comment results in PR
        if: always()
        uses: actions/github-script@v7
        with:
          script: |
            const fs = require('fs');
            const results = JSON.parse(fs.readFileSync('eval-results.json'));
            const body = formatResultsMarkdown(results);
            github.rest.issues.createComment({
              issue_number: context.issue.number,
              owner: context.repo.owner,
              repo: context.repo.repo,
              body: body,
            });
```

Companion `eval-thresholds.yaml`:

```yaml
thresholds:
  correctness:
    regression_max: 0      # Qualquer regressão bloqueia
    avg_min: 0.85

  format:
    regression_max: 0      # Quebra de shape = blocker
    pass_rate_min: 1.0

  safety:
    regression_max: 0      # Safety nunca regride
    pass_rate_min: 1.0
    automatic_failure_max: 0

  calibration:
    regression_max: 0.1    # 10% tolerância
    avg_min: 0.75

  latency_p99:
    regression_max: 0.15   # 15% tolerância
    max_ms: 3000

  cost_per_item:
    regression_max: 0.20   # 20% tolerância (modelos novos podem custar mais)
    max_usd: 0.05
```

## Estratégias de sampling

Rodar full golden set em todo PR não escala. Em produto com golden set de 500+ itens, full eval custa $5-20 e leva 5-15min. Solução: sampling estratificado.

| Estratégia | Como | Quando usar |
|---|---|---|
| **Full** | Todos os itens | Merge em main, release |
| **Subset crítico** | Itens marcados `tags: [critical, safety]` | PR rápido (default) |
| **Stratified random** | N de cada categoria | PR com mais cobertura |
| **Diff-targeted** | Itens cujo prompt afetado pelo PR | PR com mudança específica |
| **Smoke test** | 5-10 itens canônicos | Quick sanity check |

```yaml
# promptfooconfig.yaml — sampling
tests:
  - vars: { input: "..." }
    metadata:
      tags: ["critical", "format"]   # sempre roda
      priority: "high"

  - vars: { input: "..." }
    metadata:
      tags: ["edge-case", "japanese"]  # roda em full eval
      priority: "medium"
```

```bash
# Fast em PR
promptfoo eval --filter-metadata 'priority=high'

# Full em merge
promptfoo eval  # tudo
```

## Custo realista

Cálculo direto pra time típico:

```
Golden set: 200 itens
Modelo: Claude Sonnet 4.6
Tokens médios: 800 in + 400 out por item
Custo: ~$0.005/item

Fast subset (top-30 critical): $0.15 por run
Full set: $1 por run

PRs/dia: 5-10
Merges em main/dia: 3-5

Custo diário:
  PR fast: 10 × $0.15 = $1.50
  Main full: 5 × $1 = $5
  Total: ~$6.50/dia = ~$200/mês
```

Pra time enterprise com golden set de 2000+ e judges Opus 4:

```
Full eval com Opus 4 judge: $15-40 por run
10 merges/dia: $150-400/dia
Mensal: $4500-12000

Mitigação: judge mais barato (Sonnet) ou sampling estratégico
```

Custo é problema real depois de certo volume. Estratégia: judge barato em PR, judge forte em main + 1x/semana.

## Quarentena de evals flaky

LLM é estocástico. Mesmo com `temperature=0`, há variação cross-run (modelo mudou, infra cache, etc.). Alguns itens vão ser **flaky** — passam 80%, falham 20%.

Como detectar:

```python
# Roda o mesmo item N vezes
for item in golden_set:
    results = [run_eval(item) for _ in range(5)]
    if not all_equal(results):
        item.metadata.flaky = True
        item.metadata.tolerance = compute_variance(results)
```

Como tratar:

| Situação | Ação |
|---|---|
| Flakiness baixa (1-5% das runs falham) | Tolerance maior, mantém em CI |
| Flakiness média (10-20%) | Mover pra quarentena (roda mas não bloqueia merge) |
| Flakiness alta (>30%) | Excluir do golden set ou refazer expected |

Quarentena formal:

```yaml
quarantine:
  - id: edge_042
    reason: "Flaky em 25% dos runs — modelo varia tom"
    quarantined_at: "2026-04-12"
    review_by: "2026-06-12"  # revisita em 60 dias
```

Sem quarentena, evals flaky destroem confiança no CI. Times começam a ignorar "regressão" porque "sempre falha aleatório". A partir desse ponto, CI vira ruído.

## Failing gracefully vs failing loudly

| Modo | Quando |
|---|---|
| **Block merge** | Time maduro, eval estabilizado, threshold calibrado |
| **Warn-only** | Early stage, eval ainda calibrando, OR mudança de modelo |
| **Slack notify** | Sempre (canal #llm-evals dedicado) |
| **PR comment** | Sempre (visibilidade pra reviewer) |

Pattern recomendado em adoção gradual:

```
Mês 1-2: warn-only, comentário em PR, ninguém bloqueado
Mês 3: block em safety regression (0 tolerance)
Mês 4: block em correctness > 5% regression
Mês 6+: thresholds tightening progressivo
```

Forçar block desde o dia 1 = pushback do time. Adoção gradual = cultura.

## A/B em prod como complemento

CI mede pre-deploy. Não substitui [[Anatomia dos LLMs/17 - Evaluation de LLMs em produção|A/B em prod com métricas de negócio]]. Pattern recomendado:

```
1. CI eval → métrica subiu → merge permitido
2. Deploy em 5% via feature flag
3. Métricas de negócio em prod (conversão, NPS, resolution rate)
4. Subiu? Ramp pra 100%. Caiu? Rollback.
```

Eval em CI sozinho diz que **o sistema é tecnicamente melhor**. A/B diz que **o usuário foi impactado positivamente**. Os dois importam.

## Github Actions — exemplo completo

```yaml
# .github/workflows/llm-eval.yml
name: LLM Eval Pipeline

on:
  pull_request:
    paths:
      - "prompts/**"
      - "src/llm/**"
  push:
    branches: [main]

env:
  OPENAI_API_KEY: ${{ secrets.OPENAI_API_KEY }}
  ANTHROPIC_API_KEY: ${{ secrets.ANTHROPIC_API_KEY }}

jobs:
  fast-eval:
    if: github.event_name == 'pull_request'
    runs-on: ubuntu-latest
    timeout-minutes: 10
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with: { node-version: "20" }

      - run: npm ci

      - name: Run fast eval
        run: |
          npx promptfoo eval \
            --filter-metadata "priority=high" \
            --output results.json

      - name: Check regression thresholds
        run: node scripts/check-regression.js results.json

      - name: Comment PR
        if: always()
        run: node scripts/post-pr-comment.js results.json
        env:
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}

  full-eval:
    if: github.event_name == 'push' && github.ref == 'refs/heads/main'
    runs-on: ubuntu-latest
    timeout-minutes: 30
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with: { node-version: "20" }

      - run: npm ci

      - name: Run full eval
        run: |
          npx promptfoo eval --output results-full.json

      - name: Update baseline
        run: |
          cp results-full.json baselines/main-$(date +%Y%m%d).json
          git config user.email "ci@example.com"
          git config user.name "CI Bot"
          git add baselines/
          git commit -m "ci: update baseline $(date +%Y-%m-%d)" || true
          git push

      - name: Notify Slack
        run: node scripts/notify-slack.js results-full.json
        env:
          SLACK_WEBHOOK: ${{ secrets.SLACK_WEBHOOK }}
```

Observações:

1. PR roda fast eval — feedback rápido.
2. Merge em main roda full e atualiza baseline em git (versionado).
3. Slack notify só em main (PRs já têm comment).
4. Timeout: 10min em PR, 30min em main.

## Anti-patterns

- **Block merge desde o dia 1** — sem calibração, vira friction; time desativa
- **Threshold uniforme** — safety com mesma tolerância de calibration
- **Sem quarentena de flaky** — CI vira ruído, ninguém confia mais
- **Eval só em PR, não em main** — baseline nunca atualizado; comparação fica obsoleta
- **Eval ignorando custo** — full eval com Opus 4 em todo PR custa $100/dia
- **Sem PR comment** — reviewer não vê resultado, eval invisível
- **Block sem possibilidade de override** — não há mecanismo emergencial (e.g. `[skip-eval]` em commit message para hotfix raríssimo)
- **Baseline não-versionado** — não dá pra fazer regression cross-time

## Maturidade

| Nível | Sinal |
|---|---|
| 0 | Nenhum eval em CI; só "tested locally" |
| 1 | Eval roda em CI mas warn-only |
| 2 | Eval bloqueia merge em safety regression |
| 3 | Eval bloqueia em safety + correctness; baseline versionado |
| 4 | Fast/full split; sampling estratificado; quarentena de flaky |
| 5 | + A/B em prod; baseline auto-update; dashboard ops |

Meta pra 2026: nível 3 como padrão; nível 5 em produtos críticos.

## Veja também

- [[01 - Eval-driven development — a disciplina]] — a mentalidade que CI/CD implementa
- [[02 - Golden datasets — como construir]] — dataset rodado em CI
- [[05 - Regression testing em LLMs]] — o pattern central que CI dispara
- [[06 - Frameworks 2026 — Promptfoo, Braintrust, Langfuse, Patronus, Phoenix]] — qual framework usar
- [[Anatomia dos LLMs/17 - Evaluation de LLMs em produção]] — pilar 4 (A/B em prod) complementa CI

## Fontes

- **Promptfoo** — [*CI/CD integration docs*](https://www.promptfoo.dev/docs/integrations/ci-cd/)
- **Braintrust** — *Continuous eval patterns* (docs, 2026)
- **Langfuse** — [*Evaluation in CI/CD*](https://langfuse.com/docs/evaluation) (2026)
- **Hamel Husain** — [*Your AI Product Needs Evals*](https://hamel.dev/blog/posts/evals/)
- **GitHub Actions** — [docs](https://docs.github.com/en/actions)
- **Anthropic** — *Eval cookbook — CI patterns* (2026)
