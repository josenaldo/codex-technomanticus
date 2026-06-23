---
title: "07 - Métricas que importam — latência, custo, qualidade"
created: 2026-05-28
updated: 2026-05-28
type: concept
status: seedling
progress: in_progress
tags:
  - observability
  - ia
  - metricas
  - sli
  - slo
publish: true
aliases:
  - LLM metrics
  - Dashboards LLM
  - SLO LLM
---

# 07 - Métricas que importam — latência, custo, qualidade

> [!abstract] TL;DR
> Quatro famílias importam — **latência**, **custo**, **qualidade**, **confiabilidade** — e cada uma tem métricas distintas em LLM que APM tradicional não captura. **Latência**: P50/P95/P99 + time-to-first-token (TTFT) + time-to-completion, broken down por modelo e por tool. **Custo**: por requisição, por usuário, por sessão, por feature; sempre separando input/output/reasoning/cache. **Qualidade**: scores de eval (LLM-as-judge ou humano), thumbs up/down ratio, refusal rate, hallucination rate (quando avaliado). **Confiabilidade**: error rate, retry rate, fallback usage rate. Dashboard mínimo em qualquer stack tem essas quatro famílias. SLI/SLO em LLM são possíveis mas exigem definir threshold absoluto (qualidade ≥ 4.0, P95 ≤ 8s, error rate ≤ 1%) com error budget explícito; sem SLO, alerta vira ruído.

## Latência — não é só "duration"

Em LLM, latência se decompõe em sinais distintos com naturezas diferentes:

| Métrica | O que mede | Quando importa |
|---|---|---|
| **Time-to-first-token (TTFT)** | Tempo do request até o primeiro token de resposta sair | UX em streaming (chat, geração ao vivo) |
| **Time-to-completion** | Tempo total até `finish_reason` | Workflows batch, agents que esperam o output completo |
| **Tokens per second (TPS)** | Velocidade de geração após TTFT | Streaming UX após início; gargalo de longo output |
| **Latency by step** | Latência por span (LLM call, tool call, retrieval) | Debug em agent multi-step |
| **Latency by model** | P50/P95/P99 separado por `gen_ai.request.model` | Comparar Opus vs Sonnet vs Haiku |
| **Latency by region** | Distribuição por região do provider | Edge cases de roteamento |

P50/P95/P99 é obrigatório em qualquer um desses. Média é enganosa em LLM porque a distribuição tem cauda longa (responses curtas de 200ms e longas de 30s no mesmo endpoint).

Threshold típico em 2026 (chat product):

- TTFT P95 ≤ 1.5s (streaming UX aceitável)
- Time-to-completion P95 ≤ 8s (workflow não-streaming)
- TPS médio ≥ 30 tokens/s (após start)

## Custo — sempre por dimensão

Custo total é a métrica menos útil. Custo decomposto é onde está o sinal:

| Dimensão | Por que importa |
|---|---|
| **Por requisição** | Detectar request gigante (loop, contexto inflado) |
| **Por usuário** | Atribuição pra billing interno; detectar abuso |
| **Por sessão / conversa** | Custo de conversa longa; indica falha em context management |
| **Por feature** | "research-agent custou $4k essa semana, summarization custou $200" |
| **Por modelo** | "Opus gastou 70% do orçamento; vale o ganho de qualidade?" |
| **Por categoria de token** | Input vs output vs reasoning vs cache_read vs cache_write |

Categoria de token é fundamental: $1k em output é diferente de $1k em cache_read (5-10x mais barato). Aglomerar em "custo total" mata otimização.

Exemplo de breakdown em dashboard:

```
Feature: research-agent (últimos 7 dias)
├─ Total: $1,824.30
├─ Por categoria:
│   ├─ input_tokens:        $   324.10  (17.8%)
│   ├─ output_tokens:       $ 1,210.40  (66.4%)
│   ├─ reasoning_tokens:    $   245.80  (13.5%)
│   ├─ cache_read:          $    38.20  (2.1%)
│   └─ cache_write:          $     5.80  (0.3%)
├─ Por modelo:
│   ├─ claude-opus-4-7:     $ 1,420.10  (78%) — 2,840 requests
│   └─ claude-sonnet-4-6:   $   404.20  (22%) — 18,600 requests
└─ Por usuário (top 5):
    ├─ user_a3f2:           $   240.10  (13.2%)
    ├─ ...
```

## Qualidade — sinais combinados, não único número

Qualidade em LLM é sempre **multi-sinal**. Quatro fontes que compõem o sinal:

### Eval scores

Sinal mais forte quando há eval rodando (LLM-as-judge, humano, ou regra). Detalhes em [[Evaluation]]. Em dashboard:

- Score médio por feature, por dia/semana
- Score por prompt_version (vincula com [[05 - Versionamento de prompts]])
- Distribuição de scores (cauda baixa = casos problemáticos)

### Feedback do usuário

Thumbs up/down, edits, re-runs, abandonos:

```
Thumbs ratio = thumbs_up / (thumbs_up + thumbs_down)
Edit rate = edits / total_responses
Abandonment = sessions_abandoned_after_response / total_sessions
```

Thumbs ratio sozinho é enganoso (só 5-15% dos usuários dão feedback explícito); combinado com edit rate e abandonment, vira sinal forte.

### Refusal rate

Quantas vezes o modelo recusou responder (`"Não posso ajudar com isso"`). Refusal alto pode ser:

- Guardrail funcionando (bom)
- Prompt mal calibrado (ruim — modelo recusando casos legítimos)
- Modelo upstream mudou alinhamento (provider atualizou)

Tracked em separado por feature; baseline serve como linha de alerta.

### Hallucination rate (quando há ground truth)

Em domínios com fato verificável (RAG sobre docs internas, sistemas com knowledge base), eval pode marcar quando output contradiz fonte. Métrica: % de respostas marcadas como alucinação no eval automático.

Threshold prático: ≤ 2% em domínio crítico (saúde, jurídico, finanças); ≤ 10% em domínio criativo (escrita, brainstorm).

## Confiabilidade — error, retry, fallback

| Métrica | O que mede |
|---|---|
| **Error rate** | % de requisições que retornaram exception ou status ≠ 2xx |
| **Retry rate** | % que precisou retry (timeout, rate limit, transient error do provider) |
| **Fallback usage** | % que caiu em fallback (modelo secundário, response cached) |
| **Provider outage time** | Minutos/hora de degradação por provider |

Em 2026, providers (Anthropic, OpenAI, Google) tem SLA público (geralmente 99.5% mensal). Error rate acima disso indica problema no seu lado (rate limit, auth, payload mal formado) — não no provider.

Retry rate baixo mas estável (~0.5-2%) é normal. Spike de retry rate é primeiro sinal de outage upstream ou rate limit batendo.

## Dashboard mínimo — o que toda stack LLM precisa mostrar

Lista pragmática do que aparece num dashboard padrão de observability LLM:

**Linha 1 — saúde geral (4 widgets):**
- Requests/min (volume)
- Error rate (saúde)
- P95 latency (UX)
- Custo acumulado (dia / mês)

**Linha 2 — custo (3 widgets):**
- Top 5 features por custo
- Custo por categoria de token (stacked area)
- Custo por modelo

**Linha 3 — qualidade (3 widgets):**
- Score médio (linha temporal, marcadores de deploy)
- Thumbs ratio
- Refusal rate

**Linha 4 — distribuição (3 widgets):**
- Latency histogram (P50/P95/P99)
- Token usage histogram (detectar outliers)
- Top 10 traces de maior custo (ação)

**Drill-down opcional:**
- Por usuário
- Por sessão
- Por prompt_version (comparar antes/depois de deploy)

Esse é o "Apache Server Status" da era LLM — todo time precisa, raramente é o que vem out-of-the-box.

## SLI / SLO em LLM — como definir

SLI (Service Level Indicator) = o que você mede. SLO (Service Level Objective) = o target.

Em LLM, SLOs típicos em 2026:

| SLI | SLO típico | Error budget mensal |
|---|---|---|
| Availability (`HTTP 2xx / total`) | 99.5% | ~3.6h |
| P95 time-to-first-token | ≤ 1.5s | 5% |
| P95 time-to-completion | ≤ 8s | 5% |
| Eval score médio | ≥ 4.0 / 5 | sem error budget; trigger imediato se cai |
| Refusal rate | ≤ 5% (chat geral) | 5% |
| Error rate | ≤ 1% | 1% |

Sem SLO definido, alertas viram ruído ("latência subiu 200ms!" — mas era pra ser 200ms abaixo ou acima do quê?). SLO traz threshold absoluto + tempo de reação.

Erro comum: definir SLO de qualidade só em score médio. Score médio pode estar alto enquanto cauda piora (15% das respostas viraram 2/5). Definir SLO em **distribuição** (`% de score ≥ 4`) é mais robusto.

## Alertas e detecção de anomalia

Threshold fixo (ex: "custo > $500/h") falha em dois casos:

- **Gradual cost creep** — custo sobe lentamente; threshold nunca dispara mas no fim do mês fatura dobrou
- **Sazonalidade** — Black Friday gera spike legítimo; alerta vira false positive

Anomaly detection (baseline dinâmico, suportado por Langfuse, Braintrust, Datadog) aprende padrão normal e alerta desvio relativo. Mais efetivo em produção madura.

Combinação prática:

- **Threshold absoluto** pra crítico (cost > 2× orçamento diário, error rate > 5%, latency P95 > 20s)
- **Anomaly detection** pra qualidade (score caiu 10% vs baseline 7d) e gradual creep (custo médio diário subiu 20% week-over-week)

## Fontes

- **Google SRE Book** — [*Service Level Objectives*](https://sre.google/sre-book/service-level-objectives/). Princípios de SLI/SLO aplicáveis a LLM.
- **Anthropic** — [*Status page*](https://status.anthropic.com/) e SLA documentation.
- **OpenAI** — [*Status page*](https://status.openai.com/).
- **Honeycomb** — [*LLM observability metrics that matter*](https://www.honeycomb.io/blog) (série 2025).
- **Braintrust** — [*Top 10 LLM Observability Tools 2025*](https://www.braintrust.dev/articles/top-10-llm-observability-tools-2025).
- **LangSmith / Langfuse** — documentação dos próprios dashboards padrão.

## Veja também

- [[02 - Anatomia de um trace LLM]] — atributos que sustentam essas métricas
- [[03-Dominios/Tecnologia/IA/Economia de Tokens/04 - Monitoramento — ccusage, Langfuse, dashboards]] — ângulo de custo detalhado
- [[Evaluation]] — scores de qualidade vêm daqui
- [[06 - Session replay e debugging]] — investigação de outlier flagged por dashboard
- [[Improvement Loop]] — métricas viram input do ciclo (em construção)
