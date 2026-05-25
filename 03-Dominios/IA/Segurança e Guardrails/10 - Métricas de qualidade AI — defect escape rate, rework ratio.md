---
title: "Métricas de qualidade AI — defect escape rate, rework ratio"
created: 2026-05-02
updated: 2026-05-02
type: concept
status: seedling
publish: true
tags:
  - seguranca-ia
  - ia
  - guardrails
  - metricas
aliases:
  - AI quality metrics
  - Defect escape rate
  - Rework ratio
  - Métricas qualidade IA
---

# Métricas de qualidade AI — defect escape rate, rework ratio

> [!abstract] TL;DR
> "Estamos produzindo mais com IA" não é métrica — é vibe. As métricas que importam medem **qualidade líquida**: quantos bugs escaparam para prod (defect escape rate), quanto código foi reescrito sobre código gerado (rework ratio), quanto tempo passou entre código aceito e bug em prod (mean time to defect), e quantas vulns de cada classe foram introduzidas. Sem essas métricas, time não sabe se está acumulando ou pagando débito. Esta nota dá o set mínimo para acompanhar honestamente.

## A pergunta que essas métricas respondem

> *"O ganho de velocidade está sendo comido por retrabalho e bugs?"*

Velocidade bruta sem qualidade é **ilusão produtiva**. As métricas abaixo separam ganho real de ganho aparente.

## As 5 métricas essenciais

### 1. Defect escape rate (DER)

**Definição:** % de bugs que **escapam** das camadas de validação ([[04 - A pirâmide de validação AI]]) e chegam em produção.

```
DER = bugs detectados em prod / total de bugs detectados (CI + review + prod)
```

**Alvo:** <5% para AI code; <2% para projeto maduro.

**Cuidado:** medir só "bugs detectados em prod" sem dividir mascara realidade. Time pode estar **sem bugs detectados** porque sem usuários, não porque qualidade é alta.

### 2. Rework ratio

**Definição:** % de LOC reescritas em até 2 sprints sobre LOC adicionadas.

```
Rework = LOC mudadas em files alterados pelos últimos 30 dias / LOC total adicionadas
```

**Alvo:** <20%. Acima disso, time está produzindo código que precisa ser refeito — débito puro.

**Como medir:** `git log` + análise de diff sobre arquivos. Tools: GitClear, Code Climate.

> [!info] Insight crítico
> *"Times com adoção desprotegida de IA frequentemente têm rework ratio de 40-60% — significa que mais de metade do código gerado precisou ser refeito antes de estabilizar."* — pesquisa Augment Code, 2026.

### 3. Mean time to defect (MTTD)

**Definição:** Tempo médio entre código mergido e bug detectado em prod (que não foi pego em CI/review).

**Alvo:** longe — quanto mais tempo passa sem bug, mais robusto o código.

**Sinal de alerta:** MTTD curto (dias) = código gerado tem bugs que não fomos capazes de detectar antes.

```
MTTD = média(timestamp_bug_em_prod - timestamp_merge_PR_origem)
```

### 4. Vulnerability introduction rate (VIR)

**Definição:** Quantas vulnerabilidades de cada classe (CWE) entraram via PRs nos últimos N dias.

| CWE | Categoria | Alvo |
|---|---|---|
| CWE-89 | SQL Injection | 0 |
| CWE-78 | Command Injection | 0 |
| CWE-918 | SSRF | 0 |
| CWE-798 | Hardcoded creds | 0 |
| CWE-22 | Path Traversal | 0 |
| CWE-80 | XSS | <2/mês |
| CWE-117 | Log Injection | <5/mês |

VIR > 0 em CWE crítica = camadas de validação falhando.

### 5. AI-attributable defects (AIAD)

**Definição:** Bugs que vieram especificamente de PRs com geração de IA (vs PRs humanos).

**Como medir:** label `ai-generated` em PRs (manual ou auto-detection); rastrear bugs de prod até PR origem.

```
AIAD = bugs originados em PRs com ai-generated / total bugs
```

**Alvo:** AIAD < % de PRs com IA. Se 60% PRs são AI mas AIAD = 80%, IA está produzindo qualidade pior que humano.

## Métricas vanity (a evitar)

| Métrica vanity | Por que engana | Use no lugar |
|---|---|---|
| LOC adicionadas/dia | Mais código ≠ mais valor | Features completas/sprint |
| % de PRs com IA | Uso ≠ valor | AIAD + qualidade líquida |
| [[Dicionário de IA#Token\|Tokens]] consumidos | Uso ≠ valor | Horas economizadas validadas |
| % de tests passing | Pode estar testando errado | Defect escape rate |
| Velocity (story points) | Inflado quando "easy" | Cycle time real |

## Dashboard mínimo

```
┌─────────────────────────────────────────────────┐
│   AI Code Quality Dashboard                     │
├─────────────────────────────────────────────────┤
│   Defect escape rate:   3.2%   ✅ (alvo: <5%)   │
│   Rework ratio:         18%    ✅ (alvo: <20%)  │
│   MTTD:                 14d    ✅ (alvo: >7d)   │
│   Critical CWEs (30d):  0      ✅ (alvo: 0)     │
│   AIAD vs % AI PRs:     55/60% ✅ (alvo: AIAD ≤)│
├─────────────────────────────────────────────────┤
│   Velocity (líquido):   +18% vs Q4              │
│   AI code volume:       +110% vs Q4             │
└─────────────────────────────────────────────────┘
```

Tudo em uma tela. Time olha semanalmente.

## Como instrumentar

### Para defect escape rate

- Issue tracker (GitHub, Jira) com tag `bug-from-prod`
- Pipeline de CI conta bugs detectados pre-merge (lint failures, test failures)
- Calcula proporção mensalmente

### Para rework ratio

```bash
# Pseudo-script
cd repo
since="30 days ago"

# LOC adicionadas no período
added=$(git log --since="$since" --numstat | awk '{total += $1} END {print total}')

# LOC modificadas em arquivos que tiveram >1 commit no período
rework=$(git log --since="$since" --name-only --format="" | sort | uniq -c | awk '$1 > 1' | xargs git diff --numstat HEAD~30 HEAD | awk '{total += $1} END {print total}')

echo "Rework ratio: $(bc -l <<< "$rework / $added * 100")%"
```

### Para MTTD

Requer link **PR origem ↔ bug ticket**. Convenção: PR description tem `Closes: BUG-123`. Métrica = `bug.created_at - PR.merged_at`.

### Para VIR

Saída de [[05 - SAST e SCA para código AI|SAST]] em CI agregada por CWE. Criar cards no painel.

### Para AIAD

Tag em PRs (manual ou auto: PR description menciona Cursor/Claude/etc.). Bug tracker linka a PR origem.

## Cadência

| Métrica | Frequência |
|---|---|
| Defect escape rate | Mensal |
| Rework ratio | Mensal |
| MTTD | Mensal |
| VIR | Semanal (alerta em CWE crítica) |
| AIAD | Mensal |

Revisão **trimestral** profunda: time discute tendências, ajusta processo.

## Sinais de alerta

> [!warning] Quando reagir
>
> | Sinal | Causa provável | Reação |
> |---|---|---|
> | DER subindo | Camadas de validação afrouxando | Reforce SAST, mais review |
> | Rework subindo | Specs vagas ou agente inadequado | Revisitar spec rigor |
> | MTTD encurtando | Bugs entrando "junto" do merge | Slow down, melhor review |
> | VIR > 0 em crítica | Pipeline com gap | Adicione regra específica de SAST |
> | AIAD > % AI PRs | IA pior que humano | Revisão de adoção; treinamento; melhor sandbox |

## A história que dashboards contam

```
Semana 1: AIAD = 70%, AI PRs = 40%   ← IA está ruim
Semana 4: VIR (SQL) = 3/mês          ← reincidência
Semana 6: SAST adicionada, prompt-policy reforçada
Semana 8: AIAD = 35%, AI PRs = 50%   ← melhorou
Semana 12: VIR (SQL) = 0/mês         ← controlada
Semana 16: Defect escape = 8% → 3%   ← maturidade
```

Sem métricas, time **não sabe** se intervenção funcionou.

## Anti-patterns

- **Vanity metrics em dashboard** — líderes acham que vai bem
- **Sem baseline pré-IA** — não consegue medir impacto
- **Métricas só mensais** — alerta tarde
- **Esconder DER por medo de "parecer mal"** — perde aprendizado
- **AIAD sem isolar AI vs humano** — não consegue debugar
- **Métricas sem ação** — relatório bonito sem fix implementado

## Métricas que enganam executivos

> [!danger] Reportes externos enganam
> "Velocity subiu 40% com IA" sem mencionar:
> - Rework ratio dobrou
> - Defect escape rate triplicou
> - MTTD caiu de 30d para 4d
>
> Líderes técnicos têm responsabilidade ética de **mostrar o quadro completo**. Reportar só ganho mascara dívida.

## Veja também

- [[04 - A pirâmide de validação AI]]
- [[08 - Code review de código AI — o que muda]]
- [[12 - O roadmap de segurança para times]]
- [[Economia de Tokens|17 - ROI de IA — quando o agente vale o custo]]

## Referências

- **DORA Metrics** — adaptação para AI code (2026).
- **Augment Code** — *AI Adoption Quality Metrics* (2026).
- **GitClear** — *AI-impacted code quality research* (2026).
- **METR** — *Measuring impact of AI on real-world software development* (2025).
- **Veracode** — *2025 GenAI Code Security Report* (CWE rates) (2025).
