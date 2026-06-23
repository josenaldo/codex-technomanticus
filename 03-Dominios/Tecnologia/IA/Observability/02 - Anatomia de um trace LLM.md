---
title: "02 - Anatomia de um trace LLM"
created: 2026-05-28
updated: 2026-05-28
type: concept
status: seedling
progress: in_progress
tags:
  - observability
  - ia
  - opentelemetry
  - trace
  - span
publish: true
aliases:
  - Trace anatomy
  - OpenTelemetry GenAI
  - Trace tree
---

# 02 - Anatomia de um trace LLM

> [!abstract] TL;DR
> A unidade fundamental é uma hierarquia: **sessão → trace → spans**. Sessão agrupa interações de um mesmo usuário/conversa; trace representa uma "tarefa" completa (uma mensagem do usuário sendo respondida); spans são as etapas dentro da trace (LLM call, tool call, retrieval, sub-agent). O padrão emergente é **OpenTelemetry GenAI Semantic Conventions**, que define atributos como `gen_ai.system`, `gen_ai.request.model`, `gen_ai.usage.input_tokens` — adotá-los garante portabilidade entre Langfuse, Phoenix, Datadog, Grafana. Em agents multi-step, a árvore vira larga e profunda: trace raiz, span por LLM call, span por tool execution, sub-spans pra retrieval e pra sub-agents. Sem hierarquia explícita, debug em agent vira impossível.

## Os três níveis da hierarquia

```
Session (user_id ou conversation_id)
└── Trace #1 (mensagem 1 do usuário)
    ├── Span: LLM call (planejamento)
    ├── Span: tool_use (busca interna)
    │   └── Span: LLM call (formatação do resultado)
    └── Span: LLM call (resposta final)
└── Trace #2 (mensagem 2 do usuário)
    └── ...
```

| Nível | Granularidade | Identificador | Vida útil |
|---|---|---|---|
| Session | Conversa / usuário | `session_id`, `user_id` | Dias / semanas |
| Trace | Uma tarefa do usuário | `trace_id` (UUID v4 / 128 bits) | Segundos / minutos |
| Span | Uma operação interna | `span_id` (UUID / 64 bits) + `parent_span_id` | Milissegundos / segundos |

A regra simples: **trace é o que você mostra pro stakeholder pra explicar uma resposta**; **span é o que você abre pra debugar uma etapa específica**.

## OpenTelemetry GenAI — convenções semânticas

OpenTelemetry (OTel) padronizou (ainda em status `experimental` em 2026, mas amplamente adotado) os atributos pra spans de IA generativa. Adotar essas convenções dá portabilidade — instrumenta uma vez, exporta pra qualquer backend OTel-compatible.

**Atributos obrigatórios em qualquer span LLM:**

```python
span.set_attribute("gen_ai.system", "anthropic")              # provider
span.set_attribute("gen_ai.request.model", "claude-sonnet-4-6") # modelo solicitado
span.set_attribute("gen_ai.response.model", "claude-sonnet-4-6") # modelo efetivamente usado
span.set_attribute("gen_ai.operation.name", "chat")           # chat | text_completion | embeddings
```

**Atributos de uso (tokens):**

```python
span.set_attribute("gen_ai.usage.input_tokens", 1500)
span.set_attribute("gen_ai.usage.output_tokens", 380)
# Não-padrão mas convencionado entre Langfuse/Phoenix:
span.set_attribute("gen_ai.usage.cache_read_input_tokens", 900)
span.set_attribute("gen_ai.usage.cache_creation_input_tokens", 100)
span.set_attribute("gen_ai.usage.reasoning_tokens", 240)
```

**Atributos de parâmetros de requisição:**

```python
span.set_attribute("gen_ai.request.max_tokens", 1024)
span.set_attribute("gen_ai.request.temperature", 0.7)
span.set_attribute("gen_ai.request.top_p", 0.95)
span.set_attribute("gen_ai.request.stop_sequences", ["</answer>"])
```

**Atributos de resposta:**

```python
span.set_attribute("gen_ai.response.id", "msg_01ABC...")       # ID do provider
span.set_attribute("gen_ai.response.finish_reasons", ["end_turn"])
```

**Eventos de span (preferir pra prompt e resposta):**

Prompts e respostas não devem ir como atributos (atributos são indexados e podem vazar PII pra logs de baixo controle). A convenção é colocá-los como **span events** — payload anexo, redactável separadamente:

```python
span.add_event("gen_ai.content.prompt", attributes={
    "gen_ai.prompt.0.role": "system",
    "gen_ai.prompt.0.content": SYSTEM_PROMPT,   # candidato a redaction
    "gen_ai.prompt.1.role": "user",
    "gen_ai.prompt.1.content": user_input,      # candidato a redaction
})

span.add_event("gen_ai.content.completion", attributes={
    "gen_ai.completion.0.role": "assistant",
    "gen_ai.completion.0.content": response_text,
    "gen_ai.completion.0.finish_reason": "end_turn",
})
```

Política de PII separada — span events podem ser droppados em export sem perder o resto do trace.

## Hierarquia em agents multi-step

Agent que faz planejamento + retrieval + várias tool calls + síntese vira árvore profunda. Exemplo real (agent de pesquisa que responde "qual o estado da arte de fine-tuning em 2026?"):

```
Trace (id: 7f3a...) — "estado da arte de fine-tuning em 2026?"
├─ duration: 18.4s
├─ total_input_tokens: 24,580
├─ total_output_tokens: 3,240
├─ total_cost_usd: 0.42
│
├── Span: agent.plan — 1.2s
│   ├── LLM call (gen_ai)
│   │   ├─ model: claude-sonnet-4-6
│   │   ├─ input_tokens: 3,200
│   │   ├─ output_tokens: 280
│   │   └─ finish_reason: tool_use
│   └── output: plan{steps: [search_arxiv, search_blog, summarize]}
│
├── Span: tool.search_arxiv — 2.8s
│   ├── attributes: {query: "fine-tuning 2026 survey", top_k: 10}
│   ├── Span: embedding — 0.3s
│   │   └── LLM call (embeddings) — 1,200 input tokens
│   └── output: [10 papers com scores]
│
├── Span: tool.search_blog — 1.4s
│   └── output: [12 posts com scores]
│
├── Span: agent.synthesize — 12.6s
│   ├── LLM call (gen_ai)
│   │   ├─ model: claude-opus-4-7
│   │   ├─ input_tokens: 19,800 (inclui contexto recuperado)
│   │   ├─ reasoning_tokens: 1,840
│   │   ├─ output_tokens: 2,960
│   │   └─ finish_reason: end_turn
│   └── output: resposta final
│
└── attributes:
    ├── eval.score: 4.6/5
    └── user.feedback: thumbs_up
```

Cada span carrega `parent_span_id` apontando pro pai. A árvore inteira é reconstruída na UI do Langfuse/Phoenix por essa relação.

## Required vs nice-to-have

Pra cada span LLM, divisão pragmática:

**Required (não-negociável):**
- `trace_id`, `span_id`, `parent_span_id`
- `start_time`, `end_time`
- `gen_ai.system`, `gen_ai.request.model`
- `gen_ai.usage.input_tokens`, `gen_ai.usage.output_tokens`
- `status` (ok / error)

**Strongly recommended:**
- `gen_ai.response.finish_reasons`
- `gen_ai.request.temperature`, `gen_ai.request.max_tokens`
- `gen_ai.usage.cache_read_input_tokens` (se usar caching)
- `cost_usd` calculado
- `prompt_version` (custom attribute) — qual versão do prompt foi usada
- Prompt e resposta como span events

**Nice-to-have:**
- `gen_ai.request.top_p`, `gen_ai.request.stop_sequences`
- `gen_ai.response.id` (ID do provider — útil pra cruzar com logs deles)
- `tools_schema` enviado
- `eval.score` (se rodou eval inline)
- `user.feedback` (se capturado depois)
- Métricas de retrieval (top-k, scores) em spans filhos

## Status do padrão em 2026

| Item | Status |
|---|---|
| `gen_ai.*` core attributes | Stable na intenção, marcados como `experimental` na spec |
| Atributos de tool calling | Em ativo desenvolvimento; convenção ainda variável entre libs |
| Atributos de cache de prompt | Não padronizado oficialmente; Langfuse/Phoenix convergiram em `gen_ai.usage.cache_*` |
| Embeddings | Convenção separada — `gen_ai.operation.name = "embeddings"` |
| Adoção em SDKs | OpenLLMetry (community) e Langfuse SDK instrumentam Anthropic, OpenAI, Google direto |
| Backends suportados | Datadog (nativo), Grafana Tempo (nativo), Langfuse (importa OTel), Phoenix (nativo OTel) |

A direção é convergente, mas em 2026 ainda há divergência entre `gen_ai.usage.input_tokens` (OTel canônico) e `gen_ai.input_tokens` (alguns SDKs). Quando instrumentar manualmente, escolha o padrão da spec e documente.

## Fontes

- **OpenTelemetry** — [*Semantic Conventions for Generative AI*](https://opentelemetry.io/docs/specs/semconv/gen-ai/). Spec oficial.
- **OpenTelemetry** — [*GenAI metrics and events*](https://opentelemetry.io/docs/specs/semconv/gen-ai/gen-ai-events/). Convenção pra span events com prompt/completion.
- **Langfuse** — [*Tracing data model*](https://langfuse.com/docs/tracing-data-model). Trace/observation/generation explicado.
- **OpenLLMetry** — [*GitHub traceloop/openllmetry*](https://github.com/traceloop/openllmetry). Implementação OTel pra provedores populares.

## Veja também

- [[03 - Langfuse — open-source standard]] — como Langfuse materializa essa hierarquia
- [[04 - Helicone, Phoenix, OpenLLMetry — alternativas]] — outras implementações
- [[05 - Versionamento de prompts]] — `prompt_version` como atributo crítico do span
- [[Dicionário de IA#OpenTelemetry GenAI|Dicionário: OpenTelemetry GenAI]]
- [[Dicionário de IA#tracing|Dicionário: tracing]], [[Dicionário de IA#span|Dicionário: span]]
