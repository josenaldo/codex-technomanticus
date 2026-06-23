---
title: "04 - Helicone, Phoenix, OpenLLMetry — alternativas"
created: 2026-05-28
updated: 2026-05-28
type: concept
status: seedling
progress: in_progress
tags:
  - observability
  - ia
  - helicone
  - phoenix
  - openllmetry
  - opentelemetry
publish: true
aliases:
  - Helicone
  - Arize Phoenix
  - OpenLLMetry
---

# 04 - Helicone, Phoenix, OpenLLMetry — alternativas

> [!abstract] TL;DR
> Langfuse é referência, mas três alternativas resolvem problemas específicos melhor: **Helicone** entrega tracing via proxy (mudou `base_url`, virou observability) — friction zero, OSS + cloud, ótimo quando o ganho é justamente não tocar SDK; **Arize Phoenix** vem do mundo ML (não só LLM), forte em eval e integração nativa OpenTelemetry — bom pra time que já tem ML clássico em produção; **OpenLLMetry** não é backend, é coleção de instrumentações OTel-puras (Anthropic, OpenAI, etc.) que exportam pra **qualquer** backend OTel (Datadog, New Relic, Honeycomb, Grafana Tempo) — escolha quando já tem stack OTel madura e não quer trazer mais um produto. Decisão: ferramenta segue o gargalo — friction (Helicone), eval (Phoenix), reuso de stack (OpenLLMetry). (Ecossistema muda rápido; verifique a trajetória atual de cada player antes de cravar a escolha pra greenfield.)

## Helicone — proxy-based

**Como funciona:** você não muda código de chamada, só muda a `base_url` do cliente pra apontar pra Helicone. Todas as requisições passam pelo proxy deles, que captura tudo antes de repassar ao provider.

```python
import anthropic

client = anthropic.Anthropic(
    base_url="https://anthropic.helicone.ai/v1",
    default_headers={
        "Helicone-Auth": f"Bearer {os.environ['HELICONE_API_KEY']}",
        "Helicone-Session-Id": session_id,
        "Helicone-User-Id": user_id,
        "Helicone-Property-Feature": "research-agent",
    },
)
response = client.messages.create(
    model="claude-sonnet-4-6",
    max_tokens=1024,
    messages=[{"role": "user", "content": user_prompt}],
)
```

**Vantagens originais:**
- Setup em 5 minutos — uma linha de código
- Custom headers viram dimensões de filtro no dashboard
- Cache semântico no edge (Cloudflare) — armazena respostas completas, redução adicional além de [[Dicionário de IA#Prompt caching|prompt caching]] do provider
- AI Gateway: load balancing entre providers, failover, rate limiting

**Tradeoffs:**
- Proxy adiciona um hop na rede — latência extra, mais um ponto de falha entre app e provider
- Modelo proxy-only limita feature surface comparado a Langfuse/Phoenix (sem prompt registry nativo nem datasets de eval no mesmo plano)
- Ecossistema de LLM observability muda rápido — confira trajetória atual (releases, atividade no GitHub, modelo de pricing) antes de cravar pra greenfield

**Quando escolher Helicone:**
- Precisa de proxy real (cache semântico no edge, failover entre providers, gateway)
- Setup precisa ser literalmente zero-código (só mexer em `base_url`)
- Time minúsculo onde nenhum SDK pode tocar (single-file Python ou Node)
- Projeto legado já integrado

## Arize Phoenix — ML-native + OTel-first

**Como funciona:** Phoenix é OSS construído sobre OpenTelemetry desde o começo — não usa SDK proprietário, usa OTel direto. É um backend de tracing + uma plataforma de evals em cima.

```python
from phoenix.otel import register
from openinference.instrumentation.anthropic import AnthropicInstrumentor

# Inicializa tracer OTel apontando pro Phoenix
tracer_provider = register(
    project_name="research-agent",
    endpoint="http://localhost:6006/v1/traces",  # local; troca por phoenix.arize.com em cloud
)

# Instrumenta o SDK da Anthropic automaticamente
AnthropicInstrumentor().instrument(tracer_provider=tracer_provider)

# A partir daqui, qualquer messages.create() é instrumentada sem mais código
import anthropic
client = anthropic.Anthropic()
response = client.messages.create(
    model="claude-sonnet-4-6",
    max_tokens=1024,
    messages=[{"role": "user", "content": "explica MCP"}],
)
```

**Diferenciais:**
- **OpenTelemetry nativo** — sem SDK proprietário. Exporta pra Phoenix, mas também pra qualquer backend OTel
- **ML observability além de LLM** — drift detection, embedding visualization, vector store inspection — vem do background da Arize em ML clássico
- **Evals nativos** — LLM-as-judge, code checks, human annotation, custom evaluators
- **Integrações OOTB** — OpenAI Agents SDK, Claude Agent SDK, LangGraph, CrewAI, LlamaIndex, DSPy
- **Mesmo produto local e cloud** — `docker run` em dev, `phoenix.arize.com` em produção, mesma API

**Quando escolher Phoenix:**
- Time já tem ML clássico em produção (recomendação, classificação, etc.)
- Quer OTel-puro sem amarrar a SDK proprietário
- Foco principal é **eval contínua de qualidade**, não só observability
- Precisa de embedding visualization / drift detection no mesmo lugar

## OpenLLMetry — instrumentação OTel pura

**O que é (e o que NÃO é):** OpenLLMetry **não é backend**. É uma coleção de bibliotecas community-driven (Traceloop) que instrumentam SDKs de LLM (Anthropic, OpenAI, Google, Cohere, Mistral, Bedrock) seguindo as semantic conventions OTel GenAI. Os traces vão pra qualquer backend OTel.

```python
from traceloop.sdk import Traceloop

# Aponta pra qualquer backend OTel:
Traceloop.init(
    app_name="research-agent",
    api_endpoint="https://api.honeycomb.io/v1/traces",  # ou Datadog, ou Grafana Tempo
    headers={"x-honeycomb-team": HONEYCOMB_API_KEY},
)

# Pronto. Qualquer chamada LLM agora vira span no Honeycomb
import anthropic
client = anthropic.Anthropic()
response = client.messages.create(
    model="claude-sonnet-4-6",
    max_tokens=1024,
    messages=[{"role": "user", "content": "..."}],
)
```

**Decoradores opcionais pra estruturar workflows:**

```python
from traceloop.sdk.decorators import workflow, task

@workflow(name="research")
def research(question: str) -> str:
    sources = retrieve(question)
    return synthesize(question, sources)

@task(name="synthesize")
def synthesize(question: str, sources: list[str]) -> str:
    # ... chamada LLM aqui é capturada automaticamente
    ...
```

**Diferenciais:**
- **Backend-agnostic** — Datadog, Honeycomb, New Relic, Grafana, Langfuse, Phoenix, qualquer coisa que aceite OTLP
- **Zero novo produto** — se o time já tem Datadog em produção, traces de LLM aparecem no mesmo Datadog
- **Padrão emergente** — segue OTel GenAI semantic conventions sem desvio
- **Lightweight** — só instrumentação; sem UI, sem prompt registry, sem datasets

**Quando escolher OpenLLMetry:**
- Stack de observability já madura (Datadog, Honeycomb, Grafana)
- Não quer mais um backend pra operar
- Compliance/centralização exige que todos os traces fiquem na mesma plataforma
- Time de plataforma forte, time de IA pequeno

**Cuidado:** sem UI dedicada pra LLM, debug de prompt vs versão fica menos fluido que Langfuse/Phoenix. Compensa com queries customizadas no backend.

## Tabela comparativa

| Ferramenta | Hosting | Modelo de integração | Custo | Forte em | Melhor para |
|---|---|---|---|---|---|
| **Langfuse** | OSS + Cloud | SDK proprietário + OTel import | Free self-host / freemium cloud | Cobertura horizontal (trace + prompts + evals) | Time de IA dedicado, OSS sério |
| **Helicone** | Cloud + OSS | Proxy (base_url change) | Freemium | Friction zero, cache semântico edge, gateway | Setup zero-código, proxy real |
| **Arize Phoenix** | OSS (local + cloud) | OTel + auto-instrumentation | Free self-host / pago cloud | Eval nativo + ML observability + drift | Time com ML clássico em prod |
| **OpenLLMetry** | Lib (sem backend) | OTel auto-instrumentation | Free (lib) + custo do backend escolhido | Reuso de stack existente | Stack OTel madura, time plataforma forte |

## Como decidir — em uma pergunta

| Sua situação | Escolha |
|---|---|
| "Quero OSS, tudo num lugar, dado meu" | Langfuse self-host |
| "Quero começar em 5 min sem operar nada" | Langfuse Cloud |
| "Já tenho Datadog/Honeycomb e não quero outra UI" | OpenLLMetry + seu backend |
| "Time já faz ML clássico; quero observability unificada" | Arize Phoenix |
| "Projeto legado já em Helicone" | Mantém Helicone |
| "Quero proxy de verdade (cache, failover, gateway)" | Helicone, Portkey, ou LiteLLM Gateway |

## Combinações comuns

Stack não precisa ser monolítica. Padrões que aparecem em times médios:

- **OpenLLMetry → Langfuse** — instrumentação OTel pura, backend Langfuse. Tira lock-in de SDK, ganha UI especializada
- **Langfuse + Phoenix** — Langfuse pra prompt management e tracing day-to-day; Phoenix pra eval de qualidade em datasets grandes
- **OpenLLMetry → Datadog/Honeycomb** — quando observability geral é compartilhada com SRE; LLM vira mais uma dimensão

## Fontes

- **Helicone** — [Documentação](https://docs.helicone.ai) · [LLM Observability blog](https://www.helicone.ai/blog/llm-observability).
- **Arize Phoenix** — [phoenix.arize.com](https://phoenix.arize.com) · [GitHub Arize-ai/phoenix](https://github.com/Arize-ai/phoenix) · [Docs](https://docs.arize.com/phoenix).
- **OpenLLMetry** — [GitHub traceloop/openllmetry](https://github.com/traceloop/openllmetry) · [Docs Traceloop](https://www.traceloop.com/docs/openllmetry/introduction).
- **OpenInference** — [GitHub Arize-ai/openinference](https://github.com/Arize-ai/openinference). Instrumentações OTel mantidas pela Arize, alternativa a OpenLLMetry pra alguns SDKs.

## Veja também

- [[03 - Langfuse — open-source standard]] — o ponto de partida e referência OSS
- [[02 - Anatomia de um trace LLM]] — a hierarquia que todas as ferramentas materializam
- [[07 - Métricas que importam — latência, custo, qualidade]] — quais dashboards montar em qualquer backend
- [[03-Dominios/Tecnologia/IA/Economia de Tokens/04 - Monitoramento — ccusage, Langfuse, dashboards]] — ângulo de custo dessas mesmas ferramentas
- [[Dicionário de IA#Arize Phoenix|Dicionário: Arize Phoenix]], [[Dicionário de IA#OpenTelemetry GenAI|Dicionário: OpenTelemetry GenAI]]
