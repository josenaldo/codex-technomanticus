---
title: "Logging Layer"
created: 2026-05-28
updated: 2026-05-28
type: concept
status: seedling
progress: in_progress
tags:
  - ai-engineering-stack
  - ia
  - observability
publish: true
aliases:
  - Logging Layer
  - Camada de logs
---

# Logging Layer

> [!abstract] TL;DR
> A Logging Layer registra **o que aconteceu em cada run**, de forma estruturada e queryable: task, input, versão do prompt, tools chamadas, fontes usadas, output, score da eval, falhas, sugestões de melhoria. É o que permite debugar incidentes, calcular custo por usuário, achar regressões, identificar drift. Sem essa camada, o sistema é caixa-preta — você pode ver que algo deu errado mas não consegue dizer **onde** nem **por quê**. Observability em IA é exigência operacional, não nice-to-have.

## O que é esta camada

A Logging Layer é o **gravador estruturado** do sistema. Cada chamada do sistema produz um registro com identificadores (trace_id, span_id), insumos (prompt_version, model, params), passos (tool calls, retrieval queries), resultado (output, eval_score, custo), e flags (guardrails que dispararam, falhas).

Template mínimo (adaptado do thread @hooeem):

```yaml
record_per_run:
  - task_id e trace_id
  - input (com PII redacted se preciso)
  - prompt_version e model_version
  - tools_called: [{name, args, latency, success}]
  - sources_used: [{id, score, citation}]
  - output (raw + structured)
  - eval_score
  - guardrails_triggered
  - failures
  - improvement_suggestions
```

Padrão emergente: **[[Dicionário de IA#OpenTelemetry GenAI|OpenTelemetry GenAI]]** — semantic conventions específicas pra LLM (`gen_ai.system`, `gen_ai.request.model`, `gen_ai.usage.input_tokens`). Adotá-las dá interoperabilidade com Langfuse, Phoenix, Datadog, etc.

## Decisões-chave

1. **O que NÃO logar.** Logs de IA muitas vezes contêm PII em input/output. Política de redaction é parte do design — não escolha tardia. Sem redaction estruturada, log vira ativo de risco.

2. **Estrutura vs free-form.** Log livre é fácil de gerar, impossível de queryar. Schema estrito (campos tipados) é caro de manter mas viabiliza analytics. Comece com schema básico e expanda; nunca volte de estruturado pra livre.

3. **Trace vs log.** Trace agrupa todas as spans de uma execução (modelo + retrievals + tool calls + sub-agentes). Log é evento solto. Sistemas com agents precisam de trace; sistemas simples sobrevivem só com log.

4. **Sample rate.** Logar 100% em produção alto-volume custa caro. Sampling estratificado (todos os erros, alguns sucessos) preserva sinal economizando custo.

5. **Retenção.** Logs com PII têm prazo legal (GDPR, LGPD). Logs sem PII podem ficar mais. Política clara evita acumular passivo.

## Onde aprofundar no Codex

- **[[Observability]]** — trilha-irmã sobre observabilidade de sistemas de IA (em construção).
- **[[Dicionário de IA#tracing|Dicionário: tracing]]**, **[[Dicionário de IA#span|span]]**.
- **[[Dicionário de IA#Langfuse|Langfuse]]** e **[[Dicionário de IA#Arize Phoenix|Arize Phoenix]]** — duas ferramentas comuns.

## Veja também

- [[09 - Evaluation Layer]] — scores entram aqui
- [[10 - Guardrail Layer]] — incidentes de guardrail são registrados aqui
- [[12 - Improvement Layer]] — improvement lê estes logs

## Fontes

- **@hooeem** — *Become an AI Engineer*, chapter #18, Step 10 (Logging layer template).
- **OpenTelemetry** — [*Semantic Conventions for Generative AI*](https://opentelemetry.io/docs/specs/semconv/gen-ai/). Padrão emergente.
- **Langfuse** — [*Tracing concept*](https://langfuse.com/docs/tracing). Implementação concreta.
