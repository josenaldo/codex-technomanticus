---
title: "01 - Por que LLMs precisam de observabilidade"
created: 2026-05-28
updated: 2026-05-28
type: concept
status: seedling
progress: in_progress
tags:
  - observability
  - ia
  - apm
  - tracing
publish: true
aliases:
  - LLM observability é diferente
  - APM para LLM
---

# 01 - Por que LLMs precisam de observabilidade

> [!abstract] TL;DR
> APM tradicional (Datadog, New Relic, Prometheus) foi desenhado pra capturar requisições HTTP, queries de banco e fila de mensagens — três coisas que LLM systems também têm, mas que **não explicam onde o tempo, o custo ou a qualidade vai**. O que falta no APM clássico em sistema com LLM: contagem de tokens (entrada, saída, raciocínio, cache), versão do prompt usado, sequência de tool calls, passos de retrieval com scores, latência por etapa do agent, modelo exato (até a subversão), e custo calculado da requisição. Sem essa camada extra, debug vira screenshot do usuário e A/B vira fé. Hamel Husain trata observability como gêmeo de eval em *Your AI Product Needs Evals*: eval te diz se está bom; observability te diz o que aconteceu.

## O que o APM tradicional captura — e o que perde

| Camada | APM tradicional vê | APM tradicional não vê |
|---|---|---|
| HTTP | Status, duração, path, payload | Versão do prompt embutido no payload |
| DB | Query, duração, rows afetadas | Por que essa query foi feita |
| Cache | Hit/miss em Redis | Hit/miss em [[Dicionário de IA#Prompt caching\|prompt caching]] do provider |
| Resource | CPU, memória, IO | Tokens consumidos, custo da requisição |
| Erros | Stack trace, exception | Refusal, hallucination, low-confidence answer |
| Latência | Tempo total da requisição | Tempo dentro do LLM vs tempo em tool call vs retrieval |

Um exemplo concreto: requisição de 4.2 segundos no APM aparece como "/api/chat respondeu em 4200ms". Em LLM, esses 4.2 segundos se decompõem em algo como: 200ms de retrieval, 80ms de embedding da query, 3.400ms de geração do modelo (dos quais 800ms são de raciocínio com [[Dicionário de IA#Extended thinking|extended thinking]]), 320ms de tool call, 200ms de pós-processamento. O APM mostra um número; observability mostra **onde gastar atenção**.

## O que precisa estar no trace

Lista mínima do que um trace LLM precisa carregar — fora do que APM tradicional já dá:

- **Tokens** — `input_tokens`, `output_tokens`, `reasoning_tokens`, `cache_read_input_tokens`, `cache_creation_input_tokens` (cada um separado, não agregado)
- **Versão do prompt** — qual `prompt_id` + `version` foi materializado nessa chamada
- **Tool calls** — nome da tool, args, resultado, latência, sucesso
- **Retrieval** — query, top-k, IDs dos chunks retornados, scores
- **Modelo exato** — não "claude-sonnet" mas `claude-sonnet-4-6` (subversão importa pra debug)
- **Parâmetros** — `temperature`, `max_tokens`, `top_p`, `thinking_budget`, `tools` schema enviado
- **Custo da requisição** — calculado em USD, com breakdown por categoria de token
- **Finish reason** — `end_turn`, `tool_use`, `max_tokens`, `stop_sequence` — porque cortou
- **Feedback do usuário** (quando existe) — thumbs up/down, edits, re-runs
- **Score de eval** (quando aplicável) — sinal contínuo de qualidade

Sem essa lista, três operações ficam impossíveis: debug de incidente específico, atribuição de custo por feature/usuário, e detecção de regressão de qualidade.

## Observability vs APM vs product metrics

São três camadas distintas — confundi-las gera relatórios inúteis pro time errado.

| Camada | Pergunta que responde | Audiência | Granularidade |
|---|---|---|---|
| Product metrics | DAU subiu? Retenção caiu? | Produto, executivo | Agregado por dia/semana |
| APM | API tá no ar? P99 tá ok? | SRE, plataforma | Por endpoint, por instância |
| LLM observability | Por que essa resposta foi ruim? Quanto custou? | Engenharia de IA, time de prompt | Por trace, por span |

Um time só com APM e product metrics vê *"latência subiu 30% essa semana"* mas não consegue dizer se é problema do retrieval, do provider, ou de uma versão nova do prompt que adicionou 800 tokens ao system. Esse gap é exatamente o que LLM observability preenche.

## O custo de NÃO ter

Sem observability dedicada, o que sobra:

- **Debug-por-screenshot** — usuário manda print no Slack, time tenta reconstruir o input mentalmente; reprodução fica caso a caso
- **A/B test cego** — equipe muda prompt v1 → v2, "parece melhor", sem dataset compartilhado nem trace pra revisar quando reclamação chega
- **Atribuição de custo impossível** — fatura de $40k no fim do mês sem saber qual feature/produto consumiu o quê
- **Regressão silenciosa** — nova versão do modelo (provider atualizou) muda qualidade; time descobre 3 semanas depois, pelo NPS
- **Compliance impossível** — auditor pede "mostre os 5 últimos casos em que o modelo recusou", time não consegue recuperar
- **Loop de melhoria interrompido** — sem trace, não há dataset; sem dataset, não há eval; sem eval, não há loop ([[Improvement Loop]])

Hamel Husain coloca o argumento de forma direta: *"if you can't see what your model did, you can't improve it, debug it, or trust it"*. Observability é o pré-requisito invisível dos outros dois pilares (eval e improvement).

## Diferença pra observability tradicional — em uma linha

APM é caixa-preta com métricas; LLM observability é **árvore de decisão com tokens, prompts, tools e custos em cada nó**. Mesma palavra, problema diferente, ferramenta diferente. Misturar os dois leva a stack de logging que nem time de IA nem time de plataforma usa direito.

## Fontes

- **Anthropic** — [*Building effective agents*](https://www.anthropic.com/research/building-effective-agents). Seção sobre tracing como pré-requisito de agent confiável.
- **Hamel Husain** — [*Your AI Product Needs Evals*](https://hamel.dev/blog/posts/evals/). Argumento de observability como gêmeo do eval.
- **Honeycomb** — [*LLM observability is just observability — except when it isn't*](https://www.honeycomb.io/blog) (série de posts 2025). Defesa da camada dedicada.
- **OpenTelemetry** — [*Generative AI*](https://opentelemetry.io/docs/specs/semconv/gen-ai/). Padrão emergente que reconhece o gap.

## Veja também

- [[02 - Anatomia de um trace LLM]] — o que vai dentro de cada trace
- [[07 - Métricas que importam — latência, custo, qualidade]] — quais dashboards montar
- [[03-Dominios/Tecnologia/IA/AI Engineering Stack/11 - Logging Layer]] — onde isso entra no stack
- [[03-Dominios/Tecnologia/IA/Economia de Tokens/04 - Monitoramento — ccusage, Langfuse, dashboards]] — ângulo de custo desse mesmo problema
