---
title: "07 - Eval gates em CI — quando bloquear merge"
created: 2026-05-28
updated: 2026-06-28
type: concept
status: seedling
fase: iniciado
progress: in_progress
tags:
  - improvement-loop
  - ia
  - ci-cd
  - eval-gate
publish: true
aliases:
  - Eval gate
  - Bloqueio de merge por eval
  - PR gate de LLM
---

# 07 - Eval gates em CI — quando bloquear merge

> [!abstract] TL;DR
> [[03-Dominios/Tecnologia/IA/Evaluation/07 - Eval em CI-CD|Evaluation/07]] cobre o **pipeline** de eval em CI/CD (configuração, sampling, GitHub Actions). Esta nota foca o **gate mechanism do Improvement Loop**: regra de regressão por categoria que bloqueia merge, calibração do threshold, sampling pra fast feedback em PR, quarentena de evals flaky, e quando falhar **graciosamente** (warn) vs **alto** (block). Princípio central: threshold uniforme é anti-padrão (safety = 0 tolerância, calibration = 5-10% tolerância). Métrica do gate é "regression delta" (vs baseline da main), não "score absoluto". Sem quarentena de flaky, gate vira ruído e time ignora; sem audit de override, gate vira teatro. Custo realista: $0.50-5 por PR pra time típico (golden set 100-300, modelo médio). Onde mora o gate: GitHub Actions / GitLab CI / similar; integração com Promptfoo, Braintrust, Langfuse.

> [!question]- Quando devo bloquear vs apenas avisar?
> Bloqueie quando o custo de deixar passar é alto: regressão em safety, quebra de schema, correctness acima do threshold. Use warn-only quando a regressão é em categorias subjetivas (tom, estilo) ou quando o gate ainda está em fase de calibração. A regra prática: se você voltaria ao PR em caso de falha, bloqueie; se olharia só "para saber", avise. Em adoção inicial, comece tudo como warn-only por 2-4 semanas para calibrar os thresholds com dados reais antes de ativar bloqueios.

## Ponte com Evaluation/07

[[03-Dominios/Tecnologia/IA/Evaluation/07 - Eval em CI-CD]] cobre:

- Contrato de eval-em-CI ("nenhum prompt change vai pra main sem ter sido medido")
- Pipeline canônico (fast em PR / full em main)
- Anatomia completa de workflow GitHub Actions
- Estratégias de sampling (full, subset crítico, stratified, diff-targeted, smoke)
- Cálculo de custo realista
- Maturidade ladder

**Esta nota não duplica.** Aqui o foco é o **gate mechanism** especificamente: como decidir bloquear ou não, como calibrar threshold, como tratar flakiness sem matar o sinal. Pra o pipeline completo, vá em [[03-Dominios/Tecnologia/IA/Evaluation/07 - Eval em CI-CD]].

## O gate — o que ele é, mecanicamente

```
PR aberto/atualizado
       ↓
CI dispara eval (subset fast)
       ↓
métricas por categoria são computadas
       ↓
GATE:  para cada categoria
            regression_delta = baseline - new_score
            se regression_delta > threshold_da_categoria
               → BLOCK
            senão
               → PASS
       ↓
       ▼
   PASS → merge permitido
   BLOCK → merge bloqueado, PR comment explica
```

Diferença entre **eval em CI** e **eval gate**:

- Eval em CI = roda eval, mostra resultado
- Eval gate = decisão automática de bloqueio baseada no resultado

Eval em CI sem gate vira observação informativa que ninguém olha. Gate força ação.

## Threshold por categoria — uniformidade é anti-padrão

O instinto errado: declarar um threshold único ("regressão > 5% bloqueia merge"). Isso falha em duas direções:

- **Categorias críticas merecem tolerância zero** (safety, format/schema)
- **Categorias com variância natural** merecem tolerância maior (calibration, tom)

Template recomendado:

```yaml
thresholds:
  safety:
    regression_max: 0.0          # zero tolerância
    pass_rate_min: 1.0
    block_action: "block"

  format_schema:
    regression_max: 0.0          # quebra de schema = blocker
    pass_rate_min: 1.0
    block_action: "block"

  correctness:
    regression_max: 0.05         # 5% tolerância
    avg_min: 0.80
    block_action: "block"

  calibration:
    regression_max: 0.10         # 10% tolerância
    avg_min: 0.70
    block_action: "block"

  tone_style:
    regression_max: 0.15         # 15% tolerância
    block_action: "warn"         # comenta mas não bloqueia

  latency_p95:
    regression_max: 0.20         # 20% tolerância
    max_ms: 3000
    block_action: "block"

  cost_per_request:
    regression_max: 0.25         # custo subir 25% bloqueia
    max_usd: 0.05
    block_action: "block"
```

Princípios:

- **Safety/schema = zero tolerância** — qualquer regressão bloqueia
- **Qualidade técnica = 5-10%** — variância natural, mas regressão grande importa
- **Qualidade subjetiva = 10-15% + warn-only** — sinaliza, não bloqueia
- **Custo/latência = 15-25%** — tolerância maior, mas piso absoluto declarado
- **block_action** pode ser `block` (PR bloqueado) ou `warn` (PR comment, merge OK)

## Calibração do threshold — too tight vs too loose

Threshold é dial duplo: muito apertado vira gate flaky (bloqueia merge em ruído estatístico); muito frouxo vira teatro (deixa passar regressões reais).

### Sinais de threshold muito apertado

- Gate bloqueia merges sem que time perceba mudança comportamental
- Time começa a usar override (`[skip-eval]`) rotineiramente
- Reblessing do baseline acontece "pra desbloquear", não por mudança real
- Bloqueios em categorias subjetivas (tom, estilo) que variam naturalmente

### Sinais de threshold muito frouxo

- Regressões reais entram em main, viram incidente em prod
- Eval verde em PR, métricas em produção pioram após merge
- Time perde confiança no gate como sinal de qualidade

### Como calibrar

1. **Comece warn-only por 2-4 semanas** — coleta dados de "que regressão é normal" vs "que regressão é real"
2. **Olha variância histórica** — calcula desvio padrão das categorias em 30 dias; threshold ≈ 2σ pra começar
3. **Aperta categoria por categoria** — não tudo de uma vez
4. **Reabre o threshold se vira fonte de override** — gate que ninguém respeita não existe

Calibração é processo, não constante. Reabra periodicamente.

## Sampling pra PR — fast feedback sem perder rigor

Rodar full golden set (200-2000 itens) em cada PR não escala. Em time típico, full eval custa $1-5 e demora 5-15min. Em PR busy, isso vira gargalo.

A estratégia: **fast em PR, full em main** (detalhe completo em [[03-Dominios/Tecnologia/IA/Evaluation/07 - Eval em CI-CD]]). O essencial do gate aqui:

| Quando | O que roda | Quem decide |
|---|---|---|
| PR aberto/atualizado | Subset "crítico" (~30-50 itens marcados `priority=high` ou `tags=safety,critical`) | Gate fast |
| Merge em main | Full golden set | Gate full + baseline update |
| Daily/weekly em main | Full golden set contra produção atual | Drift detection |

Subset crítico precisa cobrir:

- Toda categoria com `regression_max=0` (safety, schema)
- Pelo menos N exemplos de cada categoria com `regression_max>0` (estatística mínima)
- Edge cases já conhecidos como problemáticos

Tradeoff explícito: subset pequeno = rápido + pode perder regressão; subset maior = lento + custa mais. Calibra pela latência de feedback que time tolera.

## Quarentena de evals flaky

LLM tem variância intrínseca. Mesmo com `temperature=0`, snapshot do modelo muda, cache de infra muda, encoding muda. Alguns itens do golden set vão ser **flaky** — passam 80% das vezes, falham 20%.

Sem quarentena, evals flaky destroem confiança no gate. Time começa a ignorar "regressão" porque "sempre falha aleatório". Gate vira ruído.

Detecção:

```python
# rodar mesmo item N vezes contra o mesmo baseline
for item in golden_set:
    results = [run_eval(item) for _ in range(5)]
    pass_rate = sum(r.passed for r in results) / 5

    if pass_rate < 0.6:
        item.metadata["status"] = "broken"  # excluir
    elif pass_rate < 1.0:
        item.metadata["status"] = "flaky"
        item.metadata["tolerance"] = compute_tolerance(results)
    else:
        item.metadata["status"] = "stable"
```

Tratamento por nível de flakiness:

| Pass rate | Status | Ação no gate |
|---|---|---|
| > 95% | Stable | Bloqueia merge normalmente |
| 80-95% | Slightly flaky | Mantém no subset crítico, tolerância maior |
| 60-80% | Flaky | **Quarentena**: roda mas não bloqueia; flag pra revisão |
| < 60% | Broken | Exclui do golden set; expected outcome precisa revisão |

Quarentena com expiração — não fica eterna:

```yaml
quarantine:
  - id: edge_042
    reason: "Flaky em 25% — modelo varia tom"
    quarantined_at: "2026-04-12"
    review_by: "2026-06-12"     # revisita em 60 dias
    owner: "ai-team"
```

Review periódico de quarentena: ou o item é recuperado (judge melhor, expected ajustado), ou é descartado de vez. Quarentena permanente vira problema crônico.

## Failing gracefully vs failing loudly

| Modo | Quando |
|---|---|
| **Block merge** | Categoria crítica (safety, schema), regressão acima do threshold, sem override válido |
| **Warn-only com PR comment** | Categoria subjetiva, mudança esperada (deploy de modelo novo), early adoption do gate |
| **Slack notification** | Sempre — canal dedicado pra eval results |
| **Auto-rebless do baseline em main** | Após merge passar full eval; baseline cresce com main |

Pattern recomendado em adoção gradual:

```
Mês 1-2:   Warn-only — gate roda, PR comenta, ninguém é bloqueado.
           Time vê: "ah, então é assim que gate funciona."
Mês 3:     Block apenas em safety regression (zero tolerância).
           Conversa inicial sobre threshold.
Mês 4:     Block em correctness > 5% regression.
           Calibração com dados reais coletados.
Mês 6+:    Apertando thresholds progressivamente.
           Quarentena de flaky estabilizada.
```

Forçar block desde o dia 1 = pushback do time, gate vira inimigo. Warn-only por 8 semanas = cultura interna se forma, gate vira ferramenta. **Adoção gradual ganha de big bang.**

## Override mechanism — válvula de escape

Mesmo gate maduro precisa de válvula de escape. Casos onde override é legítimo:

- Hotfix em incidente de prod (eval lento, urgência alta)
- Mudança de modelo do provider (baseline precisa ser reblesseado)
- Falha de infraestrutura do eval (não da mudança)

Override sem audit = teatro. Override com audit:

```yaml
# .github/workflows/llm-eval.yml — trecho de override
- name: Check skip-eval label
  id: check_skip
  run: |
    if [[ "${{ contains(github.event.pull_request.labels.*.name, 'skip-eval') }}" == "true" ]]; then
      echo "skip=true" >> $GITHUB_OUTPUT
      echo "::warning::Eval skipped via 'skip-eval' label"

      # Audit: log no Slack
      curl -X POST $SLACK_WEBHOOK -d "{
        \"text\": \"Eval skipped on PR #${{ github.event.pull_request.number }} by ${{ github.actor }}\"
      }"
    fi

- name: Run eval
  if: steps.check_skip.outputs.skip != 'true'
  run: promptfoo eval ...
```

Princípios do override:

- **Label/flag explícito** — não basta argumentar no PR
- **Audit log** — quem usou, quando, por quê
- **Quarentena pós-override** — PR que mergiou com `[skip-eval]` roda full eval em main + alerta se regrediu
- **Cap mensal** — overrides > N por mês = sinal de gate mal calibrado, revisita

## Anti-padrões

- **Threshold uniforme** — safety com mesma tolerância de tom
- **Block desde o dia 1** — sem calibração, vira friction; time desativa ou ignora
- **Sem quarentena de flaky** — gate ruidoso = gate ignorado
- **Override sem audit** — `[skip-eval]` virou rotina, ninguém sabe por quê
- **Sem baseline atualizado** — comparação contra baseline de 6 meses atrás
- **Eval só em PR, não em main** — main pode regredir entre PRs (dependência externa muda)
- **Block sem PR comment** — reviewer não sabe o que falhou, só "eval failed"
- **Comment sem actionable info** — "eval falhou" sem mostrar qual categoria, qual delta
- **Sem rebless period em quarentena** — flaky vira eterno
- **Gate ignorando custo** — full eval com Opus 4 em todo PR custa $100/dia, time desativa

## PR comment — qualidade do feedback importa

Gate que falha sem explicação não é gate, é castigo. PR comment deve mostrar:

```markdown
## LLM Eval Results

| Categoria | Baseline | This PR | Delta | Threshold | Status |
|---|---|---|---|---|---|
| safety | 100% | 100% | 0% | 0% | PASS |
| format_schema | 100% | 100% | 0% | 0% | PASS |
| correctness | 0.85 | 0.82 | -3.5% | -5% | PASS |
| calibration | 0.78 | 0.69 | -11.5% | -10% | BLOCK |
| tone_style | 0.81 | 0.75 | -7.4% | -15% | WARN |
| cost_avg | $0.012 | $0.015 | +25% | +25% | PASS (no limite) |

**Reasoning**: calibration caiu 11.5% (acima do threshold de 10%).
Categorias mais afetadas: edge_cases (down 18%), low_confidence (down 14%).

**Recomendação**: revisar `prompts/research-system/v3.1.txt`. Diff vs v3.0 removeu
instrução de "expressa incerteza quando relevante" — possível causa.

[Ver dashboard completo](https://eval-dashboard.example.com/pr-XXX)
```

Princípios do comment:

- **Por categoria, não agregado** — agregado esconde
- **Delta vs threshold visível** — mostra **o quanto** passou ou falhou
- **Reasoning gerado** quando possível — apontar categorias mais afetadas
- **Link pra dashboard** — pra investigação profunda, não tudo no comment
- **Reposta atualiza em vez de duplicar** — PR não vira lixão de comments

## Armadilhas comuns

> [!warning] Threshold uniforme para todas as categorias
> Usar um único threshold para safety, correctness e tom é o erro mais comum. Safety com 5% de tolerância deixa passar falhas críticas; tom com 0% de tolerância bloqueia merges em variância natural. Defina `regression_max` por categoria e deixe `block_action` variar: `block` para críticas, `warn` para subjetivas.

> [!warning] Ativar block desde o primeiro dia
> Gate que bloqueia sem calibração gera pushback imediato — o time vira adversário do gate, não aliado. Evals flaky bloqueiam merges legítimos; thresholds mal calibrados bloqueiam quase tudo. O padrão correto: warn-only por 2-4 semanas, depois block gradual começando pelas categorias críticas. Gate que o time resiste é gate desativado.

> [!warning] Override sem audit log
> `[skip-eval]` sem registro é um gate com porta dos fundos permanentemente aberta. Sem audit, o time usa o override como rotina, não como válvula de emergência. Sempre log: quem usou, quando, qual PR, e dispare alerta de Slack. Se overrides ultrapassam N por mês, é sinal de gate mal calibrado — revisite os thresholds.

## Fontes

- **Promptfoo** — [*CI/CD integration*](https://www.promptfoo.dev/docs/integrations/ci-cd/).
- **Braintrust** — *Continuous eval patterns* (docs, 2026).
- **Langfuse** — [*Evaluation in CI/CD*](https://langfuse.com/docs/evaluation/get-started).
- **Hamel Husain** — [*Your AI Product Needs Evals*](https://hamel.dev/blog/posts/evals/).
- **GitHub Actions** — [docs](https://docs.github.com/en/actions).
- **Anthropic** — *Anthropic cookbook — eval patterns* (2026).

## Como explicar em inglês

*"An eval gate is a CI check that compares metrics from a PR's prompt changes against a baseline and automatically blocks merge if a regression exceeds the declared threshold — zero tolerance for safety, up to 15% for subjective categories like tone."*

| Português | Inglês |
|---|---|
| gate de eval | eval gate / quality gate |
| limiar / threshold | threshold / regression budget |
| delta de regressão | regression delta |
| bloquear merge | block merge / fail the gate |
| aviso sem bloqueio | warn-only |
| golden set | golden set / evaluation dataset |
| item flaky | flaky eval item |
| quarentena de eval | eval quarantine |
| override com audit | audited override |
| rebless do baseline | baseline rebless / baseline update |
| subset crítico | critical subset / priority subset |

## O que vem a seguir

Este é o último capítulo do galho **Improvement Loop**. Você percorreu o ciclo completo: medir (eval → diff → ship), experimentar (A/B testing), versionar (semver para prompts), operacionalizar em produção (champion-challenger), automatizar a otimização (DSPy), capturar sinal de usuário, e fechar o ciclo com gates de qualidade em CI.

O próximo passo natural é **instrumentar o ambiente de desenvolvimento com ferramentas de IA** — não apenas usar o loop, mas integrar assistentes que aceleram a escrita de prompts, código, e evals. Esse é o tema do galho [[03-Dominios/Tecnologia/IA/Ferramentas de IA/]] — começando pelo ecossistema de LLMs disponíveis hoje e as ferramentas que os acessam.

## Veja também

- [[03-Dominios/Tecnologia/IA/Evaluation/07 - Eval em CI-CD]] — o pipeline completo; esta nota foca o **gate**
- [[01 - O ciclo eval → diff → ship]] — gate é o que materializa o passo 2 no pipeline
- [[03 - Prompt versioning — semver para prompts]] — bump da versão dispara o gate
- [[04 - Champion-challenger em produção]] — gate é o passo **antes** do canary
- [[03-Dominios/Tecnologia/IA/Evaluation/05 - Regression testing em LLMs]] — padrão de regressão que o gate executa
- [[03-Dominios/Tecnologia/IA/Evaluation/06 - Frameworks 2026 — Promptfoo, Braintrust, Langfuse, Patronus, Phoenix]] — frameworks que o gate roda
