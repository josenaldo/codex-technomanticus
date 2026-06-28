---
title: "06 - Session replay e debugging"
created: 2026-05-28
updated: 2026-06-28
type: concept
status: seedling
fase: Iniciado
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
> Session replay é **reproduzir um incidente** a partir do que ficou no trace — sem pedir pro usuário reproduzir, sem screenshot, sem reconstrução mental. Pra isso funcionar, o trace precisa ter capturado: input completo, versão do prompt, modelo exato, parâmetros, tool calls com args e resultados, observações intermediárias, output final. Sem qualquer um desses, replay vira aproximação.

Estratégias práticas: **capture-replay** (re-rodar exatamente a mesma chamada), **state-replay** (retomar de um checkpoint intermediário), **diff replay** (rodar nova versão de prompt contra inputs antigos pra ver delta). Sampling vs captura completa é tradeoff de custo vs cobertura — sample errado mata replay no nascedouro. PII em trace = passivo legal; redaction na captura é parte do design, não nice-to-have ([[08 - Privacy e PII em logs]]).

> [!question]- Por que replay com trace é tão diferente de "colocar o input no playground e ver o que sai"?
> O playground assume que você sabe o input exato — e que o prompt, o modelo e os parâmetros são os mesmos que estavam em produção naquele momento. Cada um desses pode ter mudado. Sem trace, você reconstrói uma **aproximação** do que aconteceu. Com trace, você reproduce o estado exato: input capturado, `prompt_version=3.1.0`, `model=claude-sonnet-4-6`, `temperature=0.2`, `tool_calls` com args e retornos reais. A diferença entre "não consigo reproduzir" e "bug confirmado e adicionado ao dataset de regressão" é exatamente essa: o que estava capturado.

## O cenário que motiva replay

Sexta à noite. Slack do time:

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

Esse cenário é evitável — e a solução começa em design, antes da produção: o que precisa estar no trace desde o dia 1 pra que esse cenário seja resolvível em minutos, não horas.

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

A lista parece longa, mas na prática um `@observe()` decorator + `langfuse_context.update_current_observation(input=..., output=..., usage=...)` cobre a maioria. Tool calls exigem instrumentação explícita — frameworks como LangChain/LangGraph fazem isso automaticamente via callback handler.

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

Uma regra que não deve ter exceção: **feedback negativo explícito do usuário (thumbs down, reposta "unhelpful") captura 100% sempre**. Esses são os traces mais valiosos pra dataset de eval — e são os que você mais lamenta ter sampleado fora.

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

A divergência entre replay e trace original tem valor diagnóstico: se o input é idêntico mas o output mudou, algo externo ao seu código mudou — modelo do provider, temperatura de sampling, ou o próprio modelo foi atualizado silenciosamente. Documente divergências de replay; elas revelam dependências externas que você não sabia que tinha.

### State-replay — retomar de checkpoint

Em agent multi-step, replay completo é caro (custo + tempo) — e desnecessário quando o bug está num step específico. State-replay retoma de um span intermediário:

```python
def replay_from_span(trace_id: str, from_span: str):
    state = langfuse.get_span_state(trace_id, from_span)
    # Estado do agent quando entrou no span: messages, tool calls executadas, observações
    return continue_agent_from(state)
```

Útil quando o bug está no passo 5 de 7 — não precisa re-executar 1-4. A pré-condição é que cada span intermediário tenha o estado completo capturado (não apenas input/output do span, mas o estado global do agent naquele momento: mensagens acumuladas, observações passadas, ferramentas disponíveis).

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

Uma variação poderosa: **diff replay segmentado** — roda o candidato contra traces de cada segmento de usuário separadamente. O prompt candidato pode melhorar respostas em português mas piorar em inglês, ou ser melhor pra perguntas curtas e pior pra documentos longos. Análise agregada mascara essas divergências; segmentada as revela.

## Debugging de agent multi-step — onde olhar primeiro

Agents têm padrões de bug distintos de LLM single-call. O trace hierárquico (nota 02) é o que torna debugável.

**Padrão de bug mais comum em agent:** o modelo toma decisão errada em um step intermediário porque o **contexto acumulado** até ali estava inconsistente — não é o prompt, não é o modelo, é o estado.

Protocolo de debug quando agent produz output errado:

```
1. Encontra o trace da sessão com problema
2. Abre árvore de spans
3. Identifica o span onde o output começou a divergir
   (frequentemente: span N está correto; span N+1 usa resultado errado de tool call)
4. Inspeciona o span N: qual foi o retorno da tool call?
5. Verifica se o retorno é o esperado ou se o bug está na tool, não no LLM
6. Se o retorno está correto: o LLM interpretou errado — bug de prompt
7. Se o retorno está errado: bug na tool, não no LLM — debugging vai pra outra camada
```

Esse diagnóstico — "o problema é no LLM ou na tool?" — só é possível se o trace tiver retornos de tool capturados. Sem isso, toda investigação começa "na escuridão" e o culpado padrão é sempre o LLM, mesmo quando o bug está na implementação da tool.

**Breakpoints em agent (debugging interativo):**

Alguns frameworks (LangGraph, Claude Agent SDK com modo debug) suportam pausar o agent em tool calls antes de executar. Útil em desenvolvimento: você vê os args antes de chamar a API real, pode corrigir e continuar. Em produção, não é viável — aí o trace substitui o breakpoint.

## Dado sensível — redaction na captura

Replay completo exige input completo. Input completo, em domínios regulados (saúde, finanças, jurídico), contém PII. Solução **não** é "não logar input"; é **redact antes de armazenar**.

Padrão de duas vias:

- **Capture-time redaction** — PII substituída por placeholder no momento da captura (`<EMAIL>`, `<CPF>`). Replay funciona com placeholders; teste de bug semântico continua válido; PII não chega no storage
- **Capture-time encryption** — PII guardada cifrada com chave separada; redação só pra UI; replay autenticado pode descriptografar pra caso real

Ferramentas: Presidio (Microsoft), Google Cloud DLP, AWS Comprehend, ou regex caseiro pra padrões locais (CPF, CNPJ, telefone). Detalhes em [[08 - Privacy e PII em logs]].

O nível de redaction deve ser proporcional ao risco: dado de saúde (LGPD art. 11) exige tratamento diferente de e-mail corporativo. Defina categorias de sensibilidade antes de implementar — redaction genérica de "qualquer coisa parecendo PII" tende a quebrar contexto que o LLM precisava processar.

Caveat de replay com redaction: se o bug **depende do formato específico da PII** (ex: validação de CPF que aceita 11 dígitos quaisquer), replay com placeholder mascara o bug. Nesses casos, capture-time encryption com replay autenticado é a saída.

Uma terceira opção pra ambientes de dev/staging: **synthetic PII generation** — gera CPF/CNPJ/nome plausíveis que seguem o mesmo formato, substituindo os dados reais. O LLM vê dados com mesma estrutura sintática; o bug semântico relacionado ao formato é preservado; a PII real nunca sai do ambiente de produção.

## Ferramentas de replay em 2026

| Ferramenta | Replay support | Notas |
|---|---|---|
| **Langfuse** | Sim, UI tem botão "playground" que pré-popula o trace | Útil pra one-off; diff replay em massa via API |
| **Arize Phoenix** | Sim, com "experiments" pra diff replay em datasets | Forte em diff replay e comparações lado a lado |
| **Braintrust** | Sim, focado em experiments e datasets | Pago, fortemente integrado com eval CI |
| **Custom** | Sempre possível com trace bem estruturado | Diff replay em 50 linhas de Python |
| **LangSmith** | Sim, playground + experiments | Closed source + LangChain lock-in; UI polida |

Diff replay é particularmente valioso antes de fazer um upgrade de modelo (ex: de `claude-sonnet-4-5` pra `claude-sonnet-4-6`). Antes de colocar em produção, você roda o novo modelo contra 200 traces de produção e vê em quantos a qualidade melhorou, piorou, ou ficou igual. Decisão de upgrade baseada em evidência, não em intuição.

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

## Armadilhas comuns

> [!warning] Sample estratificado bem desenhado perde cobertura de bugs raros em segmentos ignorados
> Sample de 10% do tráfego parece razoável até aparecer um bug que só ocorre com usuários novos com `browser=mobile` e `input>2000 tokens`. Esse segmento talvez não apareça nos 10% da semana. A estratégia de sampling deve ser revisada periodicamente com a pergunta "quais segmentos de bug real ficaram de fora?" — e o sample estratificado deve incluir dimensões de produto (tipo de usuário, feature, volume de input), não só dimensões de sistema (erro, latência, custo).

> [!warning] Capturar tool call name mas não o retorno — replay inutilizável pra bugs em tool use
> É comum logar "tool X foi chamada com args Y" mas esquecer de logar o **retorno da ferramenta**. Em bugs de agent, frequentemente o problema está no que o LLM **viu como resultado da tool**, não nos args que passou. Sem o retorno capturado no trace, você não consegue nem perguntar "o que o modelo recebeu de volta antes de tomar a decisão errada?" Capture sempre `{name, args, result}` completos nos spans de tool call.

> [!warning] Tratar replay como substituto de eval estruturada
> Replay é poderoso pra debugar um incidente específico. Mas virar padrão de "rodo replay de N casos e vejo se ainda acontece" sem rubrica formal é eval ad-hoc — dependente de julgamento humano inconsistente. Use replay pra identificar bugs e adicioná-los a datasets formais de regressão. O julgamento sistemático fica na eval estruturada ([[05 - Regression testing em LLMs]]).

## Como explicar em inglês

**Interview quote:** *"When a production bug is reported, we pull the trace by user ID and timestamp, see the exact input, prompt version, model, and tool call results. We replay it in under a minute — and either confirm it's reproducible and add it to our regression dataset, or see that it diverges and understand why. We stopped closing bugs as 'intermittent' after implementing this."*

| Português | Inglês |
|---|---|
| Reproduzir incidente sem redeploy | Reproducing an incident without redeployment |
| Replay de captura (re-roda chamada original) | Capture replay (re-runs the original call) |
| Replay de estado (retoma de checkpoint) | State replay (resumes from a checkpoint) |
| Diff replay (nova versão contra inputs antigos) | Diff replay (new version against historical inputs) |
| Redaction de PII no momento da captura | PII redaction at capture time |
| Sampling por cauda (tail-based sampling) | Tail-based sampling |
| Captura completa vs amostra estratificada | Full capture vs stratified sampling |
| Adicionar bug reproduzido ao dataset de regressão | Adding a reproduced bug to the regression dataset |
| Divergência entre replay e original | Divergence between replay and original trace |
| Pré-deploy: roda candidato contra traces históricos | Pre-deploy: run the candidate against historical traces |

## O que vem a seguir

Session replay fecha o loop de debugging individual. A nota 07 muda o ângulo: de "o que aconteceu nessa sessão específica" pra "o que está acontecendo no sistema todo" — as métricas de latência, custo e qualidade que um dashboard de produção precisa mostrar pra o time operar LLMs com confiança e detectar degradações antes do usuário reclamar.

## Fontes

- **Langfuse** — [*Playground & Replay*](https://langfuse.com/docs/playground).
- **Arize Phoenix** — [*Experiments & Datasets*](https://docs.arize.com/phoenix/datasets-and-experiments/how-to-experiments).
- **OpenTelemetry** — [*Tail-based sampling in OTel Collector*](https://opentelemetry.io/docs/collector/configuration/). Mecanismo de sampling pra tracing volumoso.
- **Microsoft Presidio** — [microsoft.github.io/presidio](https://microsoft.github.io/presidio/). PII detection + redaction, OSS.
- **Microsoft Presidio** — [microsoft.github.io/presidio](https://microsoft.github.io/presidio/). Lib de PII detection e redaction.
- **LangSmith** — [smith.langchain.com](https://smith.langchain.com/). Alternativa closed-source com UI de replay e experiments da LangChain.
- **Braintrust** — [braintrustdata.com](https://www.braintrustdata.com/). Pago, focado em experiments + eval CI integrado.

## Veja também

- [[02 - Anatomia de um trace LLM]] — o que precisa estar no span pra replay funcionar
- [[05 - Versionamento de prompts]] — versão de prompt é peça obrigatória do replay
- [[08 - Privacy e PII em logs]] — redaction na captura; synthetic PII pra replay seguro
- [[03-Dominios/Tecnologia/IA/Evaluation/05 - Regression testing em LLMs]] — diff replay é base de regression testing
- [[03-Dominios/Tecnologia/IA/Evaluation/07 - Eval em CI-CD]] — gate de CI que usa diff replay antes de promover prompt
- [[Improvement Loop]] — bug capturado em replay vira dataset de eval (em construção)
- [[Dicionário de IA#Session replay|Dicionário: Session replay]], [[Dicionário de IA#Tail-based sampling|Dicionário: Tail-based sampling]]
