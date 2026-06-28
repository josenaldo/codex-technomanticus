---
title: "07 - Métricas que importam — latência, custo, qualidade"
created: 2026-05-28
updated: 2026-06-28
type: concept
status: seedling
fase: Iniciado
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

> [!question]- Por que "latência média" é uma métrica perigosa em LLM — e o que usar no lugar?
> A distribuição de latência em LLM é fundamentalmente bimodal: respostas curtas terminam em 200-500ms; respostas longas (ou com reasoning) podem levar 30-60s. A média esconde os dois extremos e cria uma "latência de ninguém" — não representa nem o caso típico nem o caso crítico. Use **P95 como SLO operacional** (95% das requisições chegam em X segundos) e **P99 como alerta de cauda** (os 1% mais lentos — geralmente agents ou contexto longo). TTFT em separado para produtos de streaming, porque um usuário em chat prefere ver os primeiros tokens em 500ms do que esperar 5s pela resposta completa.

## Latência — não é só "duration"

Em LLM, latência se decompõe em sinais distintos com naturezas diferentes:

| Métrica | O que mede | Quando importa |
|---|---|---|
| **Time-to-first-token (TTFT)** | Tempo do request até o primeiro token de resposta sair | UX em streaming (chat, geração ao vivo) |
| **Time-to-completion** | Tempo total até `finish_reason` | Workflows batch, agents que esperam o output completo |
| **Tokens per second (TPS)** | Velocidade de geração após TTFT | Streaming UX após início; gargalo de longo output |
| **Latency by step** | Latência por span (LLM call, tool call, retrieval) | Debug em agent multi-step |
| **Latency by model** | P50/P95/P99 separado por `gen_ai.request.model` | Comparar Opus vs Sonnet vs Haiku — latência de Opus é ~2-3× Sonnet |
| **Latency by region** | Distribuição por região do provider | Edge cases de roteamento |
| **Token generation speed** (TPS) vs TTFT | Separa tempo de processamento da velocidade de geração | Debugging de gargalo: servidor vs modelo |

P50/P95/P99 é obrigatório em qualquer um desses. Média é enganosa em LLM porque a distribuição tem cauda longa (responses curtas de 200ms e longas de 30s no mesmo endpoint). Em distribuições bimodais como essa, a média representa literalmente nenhum dos dois grupos.

Threshold típico em 2026 (chat product):

- TTFT P95 ≤ 1.5s (streaming UX aceitável)
- Time-to-completion P95 ≤ 8s (workflow não-streaming)
- TPS médio ≥ 30 tokens/s (após start)

Esses são thresholds de produto, não de infraestrutura. Para APIs assíncronas (processamento de documento, análise de batch), os thresholds são completamente diferentes e devem ser definidos com base no contrato de serviço com o usuário, não com base em padrão de chat.

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

Nota específica sobre reasoning tokens (modelos extended thinking como Claude Sonnet com thinking habilitado): reasoning tokens custam igual a output tokens mas não aparecem na resposta do usuário — são internos ao modelo. Um token de reasoning visível no trace representa custo real que o dashboard genérico não vai mostrar como "output", viessando toda análise de custo. Certifique-se que sua instrumentação captura `reasoning_tokens` separado.

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

**Feedback implícito** é frequentemente mais honesto que feedback explícito: editar uma resposta indica que não estava boa; re-run imediato indica que não resolveu; copiar parte do output indica que aquela parte foi usada. Tracked como eventos de UI, esses sinais completam a visão de qualidade sem depender de o usuário clicar no thumbs down.

### Refusal rate

Quantas vezes o modelo recusou responder (`"Não posso ajudar com isso"`). Refusal alto pode ser:

- Guardrail funcionando (bom)
- Prompt mal calibrado (ruim — modelo recusando casos legítimos)
- Modelo upstream mudou alinhamento (provider atualizou)

Tracked em separado por feature; baseline serve como linha de alerta.

### Hallucination rate (quando há ground truth)

Em domínios com fato verificável (RAG sobre docs internas, sistemas com knowledge base), eval pode marcar quando output contradiz fonte. Métrica: % de respostas marcadas como alucinação no eval automático.

Threshold prático: ≤ 2% em domínio crítico (saúde, jurídico, finanças); ≤ 10% em domínio criativo (escrita, brainstorm).

Hallucination rate automático exige ground truth — ou RAG com documentos fonte (compara output com chunks), ou knowledge base verificável, ou casos com resposta canônica conhecida. Sem ground truth, o sinal é humano (annotation) ou LLM-as-judge com rubrica específica de factualidade.

## Confiabilidade — error, retry, fallback

| Métrica | O que mede |
|---|---|
| **Error rate** | % de requisições que retornaram exception ou status ≠ 2xx |
| **Retry rate** | % que precisou retry (timeout, rate limit, transient error do provider) |
| **Fallback usage** | % que caiu em fallback (modelo secundário, response cached) |
| **Provider outage time** | Minutos/hora de degradação por provider |

Em 2026, providers (Anthropic, OpenAI, Google) têm SLA público (geralmente 99.5% mensal). Error rate acima disso indica problema no seu lado (rate limit, auth, payload mal formado) — não no provider. Sempre categorize errors por tipo (`4xx` vs `5xx` vs timeout vs network) antes de escalar para o provider: `4xx` invariavelmente é bug do cliente.

Retry rate baixo mas estável (~0.5-2%) é normal. Spike de retry rate é primeiro sinal de outage upstream ou rate limit batendo.

**Rate limit tracking:** providers dão headers com quota usada (`x-ratelimit-remaining-requests`, `x-ratelimit-remaining-tokens`). Logar esses valores como atributos de span viabiliza prever quando o rate limit vai bater antes que as requisições comecem a falhar — prevenção em vez de reação.

## Métricas específicas de agents

Agents multi-step têm métricas que não existem em LLM single-call:

| Métrica | O que mede |
|---|---|
| **Steps por tarefa** (avg, P95) | Quantos rounds de raciocínio o agent usa pra completar; spike = loop, tool failure ou prompt mal calibrado |
| **Tool call rate por step** | Quantas tools são chamadas por step; alto = agent fazendo mais trabalho que o necessário |
| **Task completion rate** | % de tarefas concluídas sem intervenção humana; proxy de autonomia |
| **Step cost** | Custo médio por step; multiplicado por steps por tarefa = custo real de uma tarefa |
| **Abandon rate** (agent desistiu) | % de tarefas onde o agent chegou a `finish_reason=stop` mas sem completar o objetivo |
| **Human interrupt rate** | Em sistemas com HITL, % que precisou de supervisão humana |

Steps por tarefa é especialmente útil: se o P95 virou 15 steps mas deveria ser 5, algo no raciocínio do agent mudou — prompt, modelo, ou tool que começou a retornar outputs diferentes.

**Custo de tarefa vs custo de call:** erros comuns separam custo por LLM call mas não por tarefa. Um agent que usa 8 LLM calls pra completar uma tarefa simples tem custo de tarefa 8× maior que um com design mais eficiente — essa diferença não aparece em "custo por call".

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
- Latency histogram (P50/P95/P99) — idealmente split por endpoint/feature
- Token usage histogram (detectar outliers) — input vs output separados
- Top 10 traces de maior custo (ação imediata) — link direto pra trace para review

**Drill-down opcional:**
- Por usuário
- Por sessão
- Por prompt_version (comparar antes/depois de deploy)

Esse é o "Apache Server Status" da era LLM — todo time precisa, raramente é o que vem out-of-the-box.

O dashboard mínimo não é um entregável único. Ele evolui: na semana 1, latência e error rate bastam. Na semana 4, adiciona custo por feature. No mês 3, adiciona qualidade e thumbs ratio. No mês 6, SLOs e error budgets. Tentar construir tudo de uma vez resulta em dashboard que ninguém abre.

## SLI / SLO em LLM — como definir

SLI (Service Level Indicator) = o que você mede. SLO (Service Level Objective) = o target. SLA (Service Level Agreement) = compromisso externo com penalidade. Para uso interno, SLI + SLO bastam; SLA implica cláusula contratual.

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

Sobre error budget: o conceito vem do SRE clássico. Se o SLO de disponibilidade é 99.5% mensal, o error budget é 0.5% = ~3.6h de downtime permitido. Quando o budget esgota, time para de feature work e foca em reliability. Em LLM, a mesma lógica se aplica a qualidade: se o SLO é "90% das respostas com score ≥ 4" e a semana corrente tem 82%, o budget está sendo queimado — o que desencadeia revisão de prompt antes de novo deploy.

## Métricas que não medem o que você pensa

Algumas métricas de LLM parecem óbvias mas enganam:

- **"Latência do LLM"** — frequentemente inclui tempo de serialização, rede, e logging. O tempo real de inferência do modelo pode ser bem menor. Use TTFT do streaming como proxy mais limpo da velocidade do modelo.
- **"Taxa de sucesso"** — HTTP 200 com output malformado é "sucesso" para o servidor mas falha para o usuário. Meça também parsing success rate do output.
- **"Tokens utilizados"** — confundir tokens de input com tokens de contexto (que inclui a conversa toda) leva a análise de custo errada em chat multi-turno.
- **"Score de qualidade"** — um score médio de 4.2 pode esconder bimodalidade: 80% de respostas perfeitas (5/5) e 20% ruins (2/5). Sempre mostre distribuição, não só média.

## Alertas e detecção de anomalia

Threshold fixo (ex: "custo > $500/h") falha em dois casos:

- **Gradual cost creep** — custo sobe lentamente; threshold nunca dispara mas no fim do mês fatura dobrou
- **Sazonalidade** — Black Friday gera spike legítimo; alerta vira false positive

Anomaly detection (baseline dinâmico, suportado por Langfuse, Braintrust, Datadog) aprende padrão normal e alerta desvio relativo. Mais efetivo em produção madura.

Combinação prática:

- **Threshold absoluto** pra crítico (cost > 2× orçamento diário, error rate > 5%, latency P95 > 20s)
- **Anomaly detection** pra qualidade (score caiu 10% vs baseline 7d) e gradual creep (custo médio diário subiu 20% week-over-week)

**Cadência de revisão de alerta:** alertas que nunca disparam durante 30 dias devem ser revistos (threshold muito alto?). Alertas que disparam mais de 3 vezes/semana sem ação devem ser revistos (threshold muito baixo? ruído sazonal?). Alerta sem ação definida = ruído. Para cada alerta ativo, tenha um runbook de resposta com passo 1 de triagem.

Número de alertas ativos deve ser limitado (10-15 máximo). Mais que isso indica que o time não consegue triagem de qualidade — e começa a ignorar tudo.

## Armadilhas comuns

> [!warning] Tracking de custo total sem breakdown por categoria de token — otimização cega
> `total_cost = $1,824` não diz se o problema é contexto longo (input_tokens caro), output prolixo (output_tokens inflado), ou ausência de prompt caching (cache_read poderia ser 90% do que você pagou em input_tokens). Cada categoria tem solução diferente: contexto longo → context window management; output prolixo → instrução de brevidade no prompt; ausência de cache → ativar prompt caching. Sem o breakdown, otimização de custo é tentativa e erro.

> [!warning] Definir SLO de qualidade em score médio — cauda invisível
> Score médio de 4.2/5 parece ótimo até você ver que 12% das respostas estão em 2/5 ou abaixo. A média puxa o sinal pra cima enquanto a cauda problemática cresce. Define SLO baseado em **distribuição**: "90% das respostas com score ≥ 4.0" em vez de "score médio ≥ 4.0". Isso força o dashboard a monitorar a cauda, não só o centro.

> [!warning] Usar threshold fixo de alerta sem levar sazonalidade em conta — alerta vira ruído
> Threshold fixo ("custo > $500/h") falha em Black Friday, lançamento de feature, ou promoção de marketing — todos geram spikes legítimos que disparam alertas falsos. Depois de N alertas falsos, o time aprende a ignorar todos os alertas. Combine threshold absoluto pra limites genuinamente impossíveis (10× o máximo histórico) com anomaly detection pra desvios relativos ao padrão normal. Calibre depois de 2-4 semanas de baseline.

## Como explicar em inglês

**Interview quote:** *"We define SLOs across four metric families: latency P95, cost per request, quality score distribution, and error rate. Without explicit SLOs and error budgets, every alert feels equally urgent — you can't tell signal from noise. We learned that the hard way when we had 40 alerts fire in a week and the team stopped reading them."*

| Português | Inglês |
|---|---|
| Latência de primeiro token | Time to first token (TTFT) |
| Latência de cauda (P95, P99) | Tail latency (P95, P99) |
| Custo por categoria de token | Cost per token category |
| Taxa de recusa do modelo | Model refusal rate |
| Taxa de alucinação (com ground truth) | Hallucination rate (with ground truth) |
| Indicador de nível de serviço (ILS/SLI) | Service Level Indicator (SLI) |
| Objetivo de nível de serviço (ONS/SLO) | Service Level Objective (SLO) |
| Orçamento de erro | Error budget |
| Detecção de anomalia por baseline dinâmico | Anomaly detection with dynamic baseline |
| Custo por sessão / conversa longa | Cost per session / long conversation |

## O que vem a seguir

Com métricas bem definidas e dashboards operacionais montados, a questão que sobra é: o que fazer com os dados de usuário que passam pelos logs? A nota 08 trata de **privacy e PII** — como garantir que traces ricos em contexto não virem passivo legal, o que redactar, o que mascarar, e como manter replay útil sem armazenar dados sensíveis.

## Fontes

- **Google SRE Book** — [*Service Level Objectives*](https://sre.google/sre-book/service-level-objectives/). Princípios de SLI/SLO aplicáveis a LLM.
- **Anthropic** — [*Status page*](https://status.anthropic.com/) e SLA documentation.
- **OpenAI** — [*Status page*](https://status.openai.com/).
- **Honeycomb** — [*LLM observability metrics that matter*](https://www.honeycomb.io/blog) (série 2025).
- **Braintrust** — [*Top 10 LLM Observability Tools 2025*](https://www.braintrust.dev/articles/top-10-llm-observability-tools-2025).
- **LangSmith / Langfuse** — documentação dos próprios dashboards padrão.
- **Charity Majors** — *Observability Engineering* (O'Reilly, 2022). Capítulos sobre high cardinality e tail latency são diretamente aplicáveis a métricas de LLM.

## Veja também

- [[02 - Anatomia de um trace LLM]] — atributos que sustentam essas métricas
- [[03-Dominios/Tecnologia/IA/Economia de Tokens/04 - Monitoramento — ccusage, Langfuse, dashboards]] — ângulo de custo detalhado
- [[Evaluation]] — scores de qualidade vêm daqui
- [[06 - Session replay e debugging]] — investigação de outlier flagged por dashboard
- [[08 - Privacy e PII em logs]] — o que redactar antes que dados pessoais entrem nas métricas
- [[Improvement Loop]] — métricas viram input do ciclo de melhoria contínua (em construção)
- [[Dicionário de IA#SLI|Dicionário: SLI]], [[Dicionário de IA#SLO|Dicionário: SLO]], [[Dicionário de IA#Error budget|Dicionário: Error budget]]
- [[Dicionário de IA#TTFT|Dicionário: TTFT]], [[Dicionário de IA#Tail latency|Dicionário: Tail latency]]
- [[Dicionário de IA#Refusal rate|Dicionário: Refusal rate]], [[Dicionário de IA#Hallucination rate|Dicionário: Hallucination rate]]
