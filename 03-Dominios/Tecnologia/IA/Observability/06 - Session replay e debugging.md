---
title: "06 - Session replay e debugging"
created: 2026-05-28
updated: 2026-05-28
type: concept
status: seedling
progress: in_progress
tags:
  - observability
  - ia
  - replay
  - debugging
publish: true
aliases:
  - Session replay
  - Trace replay
  - Debug LLM em produção
---

# 06 - Session replay e debugging

> [!abstract] TL;DR
> Session replay é **reproduzir um incidente** a partir do que ficou no trace — sem pedir pro usuário reproduzir, sem screenshot, sem reconstrução mental. Pra isso funcionar, o trace precisa ter capturado: input completo, versão do prompt, modelo exato, parâmetros, tool calls com args e resultados, observações intermediárias, output final. Sem qualquer um desses, replay vira aproximação. Estratégias práticas: **capture-replay** (re-rodar exatamente a mesma chamada), **state-replay** (retomar de um checkpoint intermediário), **diff replay** (rodar nova versão de prompt contra inputs antigos pra ver delta). Sampling vs captura completa é tradeoff de custo vs cobertura — sample errado mata replay no nascedouro. PII em trace = passivo legal; redaction na captura é parte do design, não nice-to-have ([[08 - Privacy e PII em logs]]).

## O cenário que motiva replay

Sexta-feira, 22h. Slack do time:

> "@time-de-ia o cliente reclamou que o assistant deu uma resposta errada às 14h32 pra um caso de incidente fiscal. Print anexo."

Sem trace bem instrumentado:
1. Tenta achar a sessão pelo timestamp → 12 sessões no minuto
2. Reconstrói mentalmente qual input gerou aquela resposta
3. Cola input no playground com o prompt atual (talvez já mudou)
4. Resposta diferente → "não consigo reproduzir"
5. Caso vira "intermitente", arquiva

Com trace bem instrumentado:
1. Filtro `user_id=X, time>=14:30, time<=14:34` → 1 trace
2. Abre o trace → vê input completo, prompt v3.1.0, modelo `claude-sonnet-4-6`, tool calls, output
3. Botão "replay" → roda mesma chamada, mesma versão de prompt, mesmo modelo
4. Resposta reproduzida → vira caso de eval permanente

A diferença não é ferramenta. É **o que foi capturado**.

## O que precisa estar capturado pra replay funcionar

Lista de captura mínima por trace:

- **Input completo** — não truncado, não redacted no campo errado
- **System prompt + versão** — `prompt_id`, `prompt_version`, label ativa naquele momento
- **Model + parâmetros** — `model` (subversão), `temperature`, `max_tokens`, `top_p`, `tools` schema
- **Tool calls** — nome, args, retorno (não só "tool foi chamada"; o retorno é crítico, porque LLM viu)
- **Observações intermediárias** — em agent multi-step, cada round de observação
- **Output completo** — não truncado; com `finish_reason` real
- **Random seed** (quando provider expõe) — pra reprodutibilidade exata
- **Timestamp + provider response_id** — pra cruzar com logs do provider em caso de bug do lado deles

Se uma dessas peças estiver faltando, replay vira aproximação — útil pra debugar direção, inútil pra reproduzir caso exato.

## Sampling vs captura completa

Logar 100% das requisições em produção alto-volume custa caro. Tradeoffs:

| Estratégia | Cobertura | Custo storage | Reprodutibilidade |
|---|---|---|---|
| Log 100% | Total | Alto | Perfeita |
| Sample 10% aleatório | 10% | 10% | Bug raro pode escapar |
| Sample estratificado | Variável | Médio | Boa pra bugs típicos |
| Log apenas erros + sample de sucessos | Erros 100% + sucesso 1-10% | Baixo | Bug em sucesso (qualidade) escapa |
| Tail-based sampling | Erros + outliers de latência/custo | Baixo-médio | Cobertura inteligente |

**Sample estratificado é o padrão prático em produção:**

```python
def should_sample(trace) -> bool:
    if trace.has_error:           return True   # 100%
    if trace.eval_score < 3.0:    return True   # qualidade ruim, 100%
    if trace.latency_p > 10_000:  return True   # outlier de latência, 100%
    if trace.cost_usd > 0.50:     return True   # outlier de custo, 100%
    if trace.user_feedback < 0:   return True   # thumbs down, 100%
    if trace.user_in_vip_segment: return True   # usuários críticos, 100%
    return random.random() < 0.10                # 10% do resto
```

**Tail-based sampling** (suportado por OpenTelemetry Collector, Datadog, Honeycomb) é a versão mais sofisticada: decide se mantém trace **depois** que terminou — viabiliza manter todos os outliers automaticamente sem regras manuais.

Regra de bolso: garantir captura 100% em janela curta (últimos 7 dias) e samples estratificados pra retenção longa.

## Estratégias de replay

Três modos, do mais direto ao mais sofisticado:

### Capture-replay — re-roda a chamada inteira

```python
def replay_trace(trace_id: str):
    trace = langfuse.get_trace(trace_id)
    # Reconstrói exatamente a chamada original:
    response = client.messages.create(
        model=trace.model,
        system=trace.system_prompt,
        messages=trace.messages,
        max_tokens=trace.params["max_tokens"],
        temperature=trace.params["temperature"],
    )
    return response
```

Útil pra confirmar que bug é reprodutível (não foi flakiness do provider). Caveat: provider pode ter atualizado modelo silenciosamente; se isso aconteceu, replay diverge do trace original — e isso já é informação.

### State-replay — retomar de checkpoint

Em agent multi-step, replay completo é caro (custo + tempo). State-replay retoma de um span intermediário:

```python
def replay_from_span(trace_id: str, from_span: str):
    state = langfuse.get_span_state(trace_id, from_span)
    # Estado do agent quando entrou no span: messages, tool calls executadas, observações
    return continue_agent_from(state)
```

Útil quando o bug está no passo 5 de 7 — não precisa re-executar 1-4.

### Diff replay — nova versão contra input antigo

A ponte com [[Evaluation]]. Pega um conjunto de traces antigos, roda a versão nova do prompt nesses mesmos inputs, compara outputs.

```python
def diff_replay(trace_ids: list[str], new_prompt_label: str):
    new_prompt = langfuse.get_prompt("research-system", label=new_prompt_label)
    diffs = []
    for tid in trace_ids:
        trace = langfuse.get_trace(tid)
        new_response = client.messages.create(
            model=trace.model,
            system=new_prompt.compile(**trace.prompt_vars),
            messages=trace.messages,
            max_tokens=trace.params["max_tokens"],
        )
        diffs.append({
            "trace_id": tid,
            "old_output": trace.output,
            "new_output": new_response.content[0].text,
            "old_score": trace.eval_score,
            "new_score": eval_against(new_response.content[0].text, trace.expected),
        })
    return diffs
```

Pré-deploy: roda candidato contra 100 traces de produção, vê quantos melhoraram, quantos pioraram. É como CI/CD pra prompt — sem isso, deploy de prompt é fé.

## Dado sensível — redaction na captura

Replay completo exige input completo. Input completo, em domínios regulados (saúde, finanças, jurídico), contém PII. Solução **não** é "não logar input"; é **redact antes de armazenar**.

Padrão de duas vias:

- **Capture-time redaction** — PII substituída por placeholder no momento da captura (`<EMAIL>`, `<CPF>`). Replay funciona com placeholders; teste de bug semântico continua válido; PII não chega no storage
- **Capture-time encryption** — PII guardada cifrada com chave separada; redação só pra UI; replay autenticado pode descriptografar pra caso real

Ferramentas: Presidio (Microsoft), Google Cloud DLP, AWS Comprehend, ou regex caseiro pra padrões locais (CPF, CNPJ, telefone). Detalhes em [[08 - Privacy e PII em logs]].

Caveat de replay com redaction: se o bug **depende do formato específico da PII** (ex: validação de CPF que aceita 11 dígitos quaisquer), replay com placeholder mascara o bug. Nesses casos, capture-time encryption com replay autenticado é a saída.

## Ferramentas de replay em 2026

| Ferramenta | Replay support | Notas |
|---|---|---|
| **Langfuse** | Sim, UI tem botão "playground" que pré-popula o trace | Útil pra one-off; diff replay em massa via API |
| **Arize Phoenix** | Sim, com "experiments" pra diff replay em datasets | Forte em diff replay e comparações lado a lado |
| **Braintrust** | Sim, focado em experiments e datasets | Pago, fortemente integrado com eval CI |
| **Custom** | Sempre possível com trace bem estruturado | Diff replay em 50 linhas de Python |

Diff replay caseiro em 30 linhas:

```python
import asyncio
from langfuse import Langfuse

lf = Langfuse()

async def replay_one(trace, new_prompt):
    response = await client.messages.create(
        model=trace.metadata["model"],
        system=new_prompt.compile(**trace.metadata["prompt_vars"]),
        messages=trace.input["messages"],
        max_tokens=trace.metadata["max_tokens"],
    )
    return {
        "trace_id": trace.id,
        "old": trace.output,
        "new": response.content[0].text,
    }

async def diff_replay(label_new: str, n: int = 100):
    traces = lf.fetch_traces(name="research-agent", limit=n, in_label="production")
    new_prompt = lf.get_prompt("research-system", label=label_new)
    return await asyncio.gather(*[replay_one(t, new_prompt) for t in traces.data])
```

## Fontes

- **Langfuse** — [*Playground & Replay*](https://langfuse.com/docs/playground).
- **Arize Phoenix** — [*Experiments & Datasets*](https://docs.arize.com/phoenix/datasets-and-experiments/how-to-experiments).
- **OpenTelemetry** — [*Tail-based sampling in OTel Collector*](https://opentelemetry.io/docs/collector/configuration/). Mecanismo de sampling pra tracing volumoso.
- **Microsoft Presidio** — [microsoft.github.io/presidio](https://microsoft.github.io/presidio/). Lib de PII detection e redaction.

## Veja também

- [[02 - Anatomia de um trace LLM]] — o que precisa estar no span pra replay funcionar
- [[05 - Versionamento de prompts]] — versão de prompt é peça obrigatória do replay
- [[08 - Privacy e PII em logs]] — redaction na captura
- [[Evaluation/05 - Regression testing em LLMs]] — diff replay é base de regression testing
- [[Improvement Loop]] — bug capturado em replay vira dataset de eval (em construção)
