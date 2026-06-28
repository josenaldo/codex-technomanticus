---
title: "01 - Por que LLMs precisam de observabilidade"
created: 2026-05-28
updated: 2026-05-28
type: concept
status: seedling
progress: in_progress
fase: Iniciado
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

> [!question]- O que eu preciso saber antes de ler isso?
> Você entende o que é observability em sistemas convencionais — o conceito de tracing distribuído, métricas, logs, e ferramentas como Datadog, Prometheus ou New Relic. Familiaridade básica com chamadas de API LLM (input, output, tokens) é o suficiente. Esta nota não pressupõe que você usou Langfuse ou qualquer ferramenta de LLM observability — ela explica por que você vai precisar de uma ferramenta assim ao colocar LLMs em produção.

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

## O que LLM observability não é

Vale clarificar os limites pra não inflar o escopo:

- **Não é guardrails em runtime** — detectar e bloquear inputs/outputs problemáticos é função de [[03-Dominios/Tecnologia/IA/Segurança e Guardrails/01 - Código gerado por IA é untrusted|Segurança e Guardrails]], não de observability. Observability *registra* o que aconteceu; guardrail *intervém* antes de acontecer.
- **Não é eval** — observability captura dados; eval julga qualidade com rubrica. São complementares: observability fornece o dataset que eval consome.
- **Não é monitoring de infra LLM** — se você está rodando modelos on-prem (vLLM, Ollama), precisa de observability de GPU/memória também, mas isso é infra-monitoring, não LLM observability de aplicação.
- **Não é analytics de produto** — DAU, retenção, funnel de conversão são product metrics. LLM observability responde "o que o modelo fez?", não "como o usuário se comportou?"

## Diferença pra observability tradicional — em uma linha

APM é caixa-preta com métricas; LLM observability é **árvore de decisão com tokens, prompts, tools e custos em cada nó**. Mesma palavra, problema diferente, ferramenta diferente. Misturar os dois leva a stack de logging que nem time de IA nem time de plataforma usa direito.

## A analogia que facilita

Pense em LLM observability como **caixa-preta de avião**, não como APM de servidor web.

APM de servidor mede throughput: quantas requisições por segundo, qual o P99, qual o error rate. É essencial pra SRE manter o serviço no ar. Mas se um avião cai, throughput não explica nada. A caixa-preta grava **cada decisão que o piloto tomou**, **cada instrumento que ele consultou**, **cada alerta que apareceu** — porque incidentes de avião exigem reconstrução fiel da sequência de eventos.

LLMs falham de formas não-binárias: a requisição "completou" com status 200, mas a resposta estava errada, ou cara demais, ou violou uma constraint de negócio. Status 200 não é sinal de sucesso. Você precisa gravar **o prompt que foi usado** (não só o path), **os tokens que foram consumidos** (por categoria), **qual chunk do RAG influenciou a resposta**, e **qual model version respondeu** (o provider pode ter trocado sem avisar).

## Maturidade de observability em produto LLM

| Nível | Sinal |
|---|---|
| 0 | Nenhum log além do APM padrão; debug por screenshot |
| 1 | Log estruturado com prompt_id, model, tokens e cost |
| 2 | Ferramenta dedicada (Langfuse/Braintrust); traces por sessão |
| 3 | Sampling configurado; dashboard de custo por feature; PII masking |
| 4 | Traces conectados a eval scores; feedback de usuário capturado |
| 5 | Traces alimentam golden set automaticamente; alert em regressão de qualidade |

Meta razoável pra 2026: nível 3 antes de 500 usuários ativos; nível 4-5 antes de monetizar.

## Como observability fecha o loop de melhoria

O fluxo de melhoria em produto com LLM tem quatro estações:

```
Prod → Observability → Eval → Improvement → Prod
```

Cada estação depende da anterior:

1. **Prod** gera eventos (chamadas reais de usuários)
2. **Observability** captura esses eventos como traces com contexto completo
3. **Eval** usa os traces como golden set ou como source pra samplear novos casos
4. **Improvement** testa mudanças de prompt/modelo contra o golden set
5. **Prod** recebe a versão melhorada, gerando novos traces

Sem observability, esse loop quebra na segunda estação. Você tem dados de prod, mas não consegue usá-los porque não gravou o prompt, o model, ou os tokens. O time opera no escuro.

## Três perguntas que observability responde — APM não

**1. Por que essa resposta custou 3x mais do que a média?**

APM mostra custo total mensal. Observability mostra qual token category inflou: `input_tokens` (prompt muito longo?), `reasoning_tokens` (extended thinking disparado desnecessariamente?), `cache_creation_input_tokens` (cache miss inesperado?). Com breakdown por span, você sabe qual estágio do pipeline consumiu o que.

**2. Por que o mesmo tipo de pergunta gera respostas inconsistentes?**

APM não tem noção de "tipo de pergunta". Observability, com `session_id`, `user_id`, e tags de feature, permite filtrar: *mostrar todos os traces de usuários que perguntaram sobre cancelamento de conta nos últimos 7 dias*. Você lê os traces lado a lado e encontra que `prompt_version: v2.1` estava ativo em 80% dos casos com resposta inconsistente.

**3. A regressão aconteceu antes ou depois do deploy de quinta?**

APM pode correlacionar latência com deploy. Observability permite correlacionar **qualidade da resposta** (via score de eval automaticamente registrado por trace) com deploy. Você plota score médio over time e vê que caiu exatamente na quinta às 14h, quando o model provider atualizou silenciosamente de `claude-sonnet-4-6-20250514` pra `claude-sonnet-4-6-20260418`.

## Quando ativar observability — não espere incidente

O erro de timing mais comum: "vamos adicionar observability depois que o produto estiver estável". Esse depois nunca chega, e quando o primeiro incidente sério acontece, o time não tem dados pra diagnosticar.

A regra prática:

- **Antes do primeiro usuário externo**: log mínimo (prompt_id, model, tokens, cost, finish_reason)
- **Antes de 100 usuários ativos**: ferramenta dedicada (Langfuse dev ou Braintrust free tier)
- **Antes de $500/mês em provider**: sampling configurado, dashboard de custo por feature
- **Antes de compliance ou regulação**: PII masking ativo, retenção configurada, audit log funcional

Observability retroativa não existe. Um trace que você não gravou é um incidente que você vai investigar no escuro.

## Mínimo viável: o que gravar antes de ter Langfuse

Se você ainda não tem ferramenta de LLM observability, o mínimo que vale gravar no log estruturado:

```python
import logging
import json

def log_llm_call(span_id, prompt_id, prompt_version, model, 
                  input_tokens, output_tokens, reasoning_tokens,
                  finish_reason, cost_usd, duration_ms,
                  feature, user_id=None):
    logging.info(json.dumps({
        "span_id": span_id,
        "prompt_id": prompt_id,
        "prompt_version": prompt_version,
        "model": model,
        "tokens": {
            "input": input_tokens,
            "output": output_tokens,
            "reasoning": reasoning_tokens,
        },
        "finish_reason": finish_reason,
        "cost_usd": cost_usd,
        "duration_ms": duration_ms,
        "feature": feature,
        "user_id": user_id,
    }))
```

Esse log estruturado já permite: atribuição de custo por feature, detecção de finish_reason inesperado, correlação de latência com model version. É um stepping stone antes de migrar pra Langfuse ou Braintrust.

## Sampling — você não precisa gravar tudo

Em produção com volume alto, gravar 100% dos traces vira custo proibitivo. Padrão recomendado:

| Estratégia | Quando | Volume alvo |
|---|---|---|
| **100% de erros** | Sempre | Todos os 4xx/5xx + finish_reason inesperado |
| **100% de casos com feedback negativo** | Sempre | Thumbs down, re-run pelo usuário |
| **Sampling de custo alto** | > threshold (e.g. > $0.10/request) | 100% desses casos |
| **Sampling aleatório** | Resto | 5-20% do volume total |
| **100% em stage/canary** | Deploy de nova versão | Todo o tráfego do canary |

Langfuse, Braintrust e Helicone têm sampling configurável nativamente. A regra de ouro: **erros e anomalias sempre; sucesso típico pode ser sampled**.

O argumento pra não sampled demais: trace que você não tem é investigação que você não pode fazer. Se você sampleou 5% e o bug acontece em 0.3% dos casos, a chance de ter um trace relevante cai pra ~1.5%. Em prática, isso se traduz em "encontramos o bug quando o CEO encontrou pessoalmente" — que é o pior timing possível.

## OpenTelemetry — o padrão emergente

O OpenTelemetry Semantic Conventions for GenAI (especificação 1.27+, 2025) define atributos padronizados pra spans LLM. Adoção cresce em 2026: Phoenix (Arize) é OTel-first; Langfuse exporta no formato; providers grandes planejam instrumentação nativa.

Atributos OTel GenAI relevantes:

```yaml
gen_ai.system: "anthropic"                # provider
gen_ai.model.id: "claude-sonnet-4-6"      # modelo exato
gen_ai.input.tokens: 1243                 # tokens de input
gen_ai.output.tokens: 387                 # tokens de output
gen_ai.finish_reasons: ["end_turn"]       # lista
gen_ai.usage.cost: 0.0043                 # em USD (extensão comum)
gen_ai.request.temperature: 0.7
gen_ai.request.max_tokens: 1024
```

Por que importa: padronização significa que o mesmo trace pode ser consumido por ferramentas diferentes. Você coleta em OTel, envia pra Langfuse e pra Datadog ao mesmo tempo, sem duplicar instrumentação.

## Armadilhas comuns

> [!warning] Tratar status 200 do provider como sinal de sucesso
> O erro mais comum ao instrumentar LLMs com APM convencional é configurar alertas apenas para erros HTTP (4xx, 5xx) e considerar que 200 = tudo bem. Em sistemas LLM, a resposta pode vir com status 200 e conter uma alucinação, uma recusa indevida, ou um `finish_reason: max_tokens` que cortou o output no meio. APM vai marcar essas requisições como bem-sucedidas. Observability LLM precisa capturar o `finish_reason`, o score de qualidade (se houver), e o conteúdo da resposta — para que incidentes de qualidade sejam detectáveis, não só incidentes de infraestrutura.

> [!warning] Logar apenas input e output sem o contexto intermediário
> Logar o prompt e a resposta final parece suficiente até que você precisa debugar um pipeline RAG de 3 estágios. Sem spans intermediários — retrieval, rerank, cada tool call individualmente — você sabe que o output estava errado mas não sabe se a culpa é do chunk que o retrieval trouxe, da forma como o prompt usou o chunk, ou de um tool call que retornou dado desatualizado. LLM observability requer **árvore de spans**, não só um log de entrada e saída. Cada estágio do pipeline que pode falhar independentemente precisa de um span próprio com seus próprios atributos.

> [!warning] Não versionar prompts junto com os traces
> Quando você grava um trace sem o `prompt_id` e a `version` do prompt que foi materializado naquela chamada, perde a capacidade de correlacionar incidentes com mudanças de prompt. Em 3 meses você vai ter um incidente, olhar pra um trace e não saber qual versão do prompt estava ativa naquele momento. A regra prática: sempre grave no trace o identificador e a versão do prompt como atributos do span. Com Langfuse, isso é um campo de primeira classe. Com log estruturado, é só mais dois campos no JSON.

## Como explicar em inglês

Em entrevistas sobre reliability de sistemas LLM, a distinção entre APM e LLM observability sinaliza que você operou LLMs em produção — não só em notebooks:

> "Traditional APM tools are blind to what actually matters in LLM systems: prompt versions, token breakdowns, tool call sequences, per-request costs, and quality signals. A 200 OK from the provider says nothing about whether the answer was correct or hallucinated. LLM observability fills that gap — it captures traces with full context: which prompt version ran, what tokens were consumed per category, what chunks the retrieval stage returned and with what scores, what the finish reason was. Without it, debugging is screenshot-driven and cost attribution is guesswork."

| Português | Inglês |
|-----------|--------|
| observabilidade de LLM | LLM observability |
| rastreamento distribuído | distributed tracing |
| span de chamada | LLM call span |
| tokens de raciocínio | reasoning tokens |
| tokens de cache | cache tokens |
| razão de finalização | finish reason |
| atribuição de custo | cost attribution |
| versão do prompt | prompt version |
| pipeline RAG com spans | RAG pipeline with spans |
| sinal de qualidade por trace | per-trace quality signal |

## O que vem a seguir

Com o argumento estabelecido, a nota 02 entra no que vai dentro de cada trace: a anatomia exata de um trace LLM, quais spans compõem cada tipo de pipeline, e como ler um trace pra debugar.

Ver [[02 - Anatomia de um trace LLM]].

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
