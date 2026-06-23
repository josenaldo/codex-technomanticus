---
title: "03 - Langfuse — open-source standard"
created: 2026-05-28
updated: 2026-05-28
type: concept
status: seedling
progress: in_progress
tags:
  - observability
  - ia
  - langfuse
  - oss
publish: true
aliases:
  - Langfuse
  - Langfuse @observe
  - Langfuse self-host
---

# 03 - Langfuse — open-source standard

> [!abstract] TL;DR
> Langfuse virou referência OSS em LLM observability em 2026 — licença MIT, adoção significativa em times de produção, com SDK em múltiplas linguagens. Arquitetura é PostgreSQL (metadados) + ClickHouse (traces de alto volume) + Next.js (UI), tudo open. Dois jeitos de rodar: **Cloud** (`cloud.langfuse.com`, free tier generoso, pago acima de 50k observações/mês) ou **self-hosted** (Docker Compose em 5 min; Helm pra produção). O API surface é mínimo: decorator `@observe()` em Python ou wrappers em JS/TS/integrações com LangChain/LlamaIndex/Vercel AI SDK. Features além de tracing: **prompt management versionado**, **datasets pra eval offline**, **evaluators built-in (LLM-as-judge)**. Escolha Langfuse quando quer OSS sério, time de 3+ pessoas, e quer manter dados (self-host) ou quer começar rápido sem trocar de stack depois (Cloud é o mesmo produto).

## Por que Langfuse virou referência

Três fatores empilhados:

1. **Licença MIT real** — código todo OSS, sem "open-core" escondendo features críticas. Self-host roda a mesma coisa do Cloud.
2. **Cobertura horizontal** — tracing + prompts + datasets + evals em uma plataforma. Substitui 3-4 ferramentas separadas em times menores.
3. **Integrações maduras** — Python decorator + JS/TS wrapper + integrações OOTB com LangChain, LlamaIndex, Vercel AI SDK, OpenAI/Anthropic/Google. Curva de adoção curta.

Helicone é friction-light (integra mudando `base_url`), mas é proxy-only — não cobre prompt management e eval no mesmo produto. LangSmith é mais polido, mas closed source e proprietário. Phoenix é OSS puro mas mais focado em eval. Langfuse fica no meio: OSS, completo, com SDKs sólidos. (O ecossistema muda rápido — confira a trajetória atual de cada player antes de cravar a escolha.)

## Arquitetura

```
                  +---------------------+
   Client SDK --> | Langfuse API server | --> ClickHouse (traces, observations)
   (Python/JS)    | (Next.js + tRPC)    | --> PostgreSQL (prompts, datasets,
                  +---------------------+      users, projects)
                            ^
                            |
                  +---------+---------+
                  | Next.js UI / API  |
                  | (dashboards,      |
                  |  prompt mgmt,     |
                  |  evals)           |
                  +-------------------+
```

- **PostgreSQL** pra dados relacionais (users, projects, prompts, datasets, configurações de eval)
- **ClickHouse** pra colunas — traces e observations chegam em volume alto, ClickHouse é o que aguenta queries analíticas em bilhões de linhas
- **API server + UI** num único monólito Next.js — simplifica deploy

Self-host mínimo: `docker compose up` puxa os 4 serviços e roda.

## Cloud vs self-host — decisão

| Critério | Cloud | Self-host |
|---|---|---|
| Tempo até primeiro trace | 2 minutos | 30 minutos (Docker) / horas (Helm prod) |
| Custo inicial | Free até 50k observations/mês | Custo de infra (uns $50-200/mês pra começar) |
| Dados onde | Cloud Langfuse (EU ou US, escolhível) | Sua infra |
| PII compliance | Depende do contrato + DPA | Você controla 100% |
| Upgrades | Automático | Você gerencia (versões mensais) |
| Quando faz sentido | MVP, time pequeno, sem restrição de dado | Enterprise, dado regulado, alto volume |

Caminho comum: começar no Cloud, migrar pra self-host quando volume passa de ~100k observations/mês ou quando compliance bate. Migração é direta porque o produto é o mesmo binário.

## SDK — decorator `@observe()` em Python

Exemplo concreto, ponta a ponta:

```python
import os
from anthropic import Anthropic
from langfuse import Langfuse, observe  # v3 SDK; em v2 era `from langfuse.decorators import observe`
from langfuse.decorators import langfuse_context

os.environ["LANGFUSE_PUBLIC_KEY"] = "pk-lf-..."
os.environ["LANGFUSE_SECRET_KEY"] = "sk-lf-..."
os.environ["LANGFUSE_HOST"] = "https://cloud.langfuse.com"  # ou seu self-host

langfuse = Langfuse()
client = Anthropic()


@observe(name="research-agent.synthesize")
def synthesize(question: str, context: list[str]) -> str:
    # Captura input/contexto no span atual
    langfuse_context.update_current_observation(
        input={"question": question, "n_sources": len(context)},
        metadata={"feature": "research-agent", "version": "v2.3"},
    )

    response = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=2000,
        system="Você sintetiza fontes em resposta clara e citada.",
        messages=[{
            "role": "user",
            "content": f"Pergunta: {question}\n\nFontes:\n" + "\n---\n".join(context),
        }],
    )

    answer = response.content[0].text

    langfuse_context.update_current_observation(
        output=answer,
        usage={
            "input": response.usage.input_tokens,
            "output": response.usage.output_tokens,
        },
    )
    return answer


@observe(name="research-agent")
def research(question: str) -> str:
    # Span pai — `synthesize` vira span filho automaticamente
    sources = retrieve(question)        # outra função decorada — vira span irmão
    return synthesize(question, sources)


answer = research("o que é melhor em 2026 — RAG ou long context?")
langfuse.flush()   # garantir envio antes do script terminar
```

O que acontece atrás do decorator:

1. `@observe` cria um span quando a função entra, com `name` = nome do decorator
2. Pega `trace_id` ambiente (ou cria novo se for a raiz)
3. Captura `input` (args), `output` (return), `latency`, `error` (se exception)
4. Em chamadas filhas decoradas, vincula `parent_span_id` automaticamente
5. Envia em batch async pra não bloquear hot path

## Integrações sem mexer no código de chamada

Pra LangChain ou LlamaIndex, integração é callback handler:

```python
from langfuse.callback import CallbackHandler

handler = CallbackHandler()

# LangChain
chain.invoke({"question": q}, config={"callbacks": [handler]})

# LlamaIndex
from llama_index.core import Settings
from langfuse.llama_index import LlamaIndexCallbackHandler
Settings.callback_manager = CallbackManager([LlamaIndexCallbackHandler()])
```

Pro Vercel AI SDK e Anthropic SDK direto, há wrappers que substituem o cliente — instrumenta automaticamente cada `messages.create()`.

## Prompts versionados

A feature que diferencia Langfuse de "só observability" é o registry de prompts. Cada prompt vira artefato versionado, acessível por nome + label.

```python
# Buscar prompt em produção
prompt = langfuse.get_prompt("research-system", label="production")
# Compilar com variáveis
system = prompt.compile(topic="LLM trends 2026")

response = client.messages.create(
    model="claude-sonnet-4-6",
    system=system,
    messages=[...],
    # Linka o prompt_version ao span automaticamente:
    extra_body={"langfuse_prompt": prompt},
)
```

Cuidados:
- **Cache**: `get_prompt` faz cache local (default 60s) — não bate na API a cada chamada
- **Labels**: `production`, `staging`, `latest`, ou custom — versão pode ser promovida entre labels via UI ou API
- **Fallback**: se falhar buscar, use `fallback="..."` pra não derrubar o sistema

Detalhe importante: o `prompt_version` usado em cada call vai automaticamente como atributo do span — viabiliza filtrar dashboard por versão, comparar v2.3 vs v2.4 lado a lado. É o link que [[05 - Versionamento de prompts]] aprofunda.

## Evals built-in

Langfuse roda LLM-as-judge nas próprias traces:

- Define um evaluator (rubrica + judge model) na UI
- Roda automaticamente em sample de traces de produção (1%, 10%, 100% — escolha)
- Score vira atributo do span — fica searchable, plotável, alertável

Útil pra detectar regressão em tempo real: se score médio cai 10% após deploy de novo prompt, dashboard pisca antes do usuário reclamar. Detalhes em [[03-Dominios/Tecnologia/IA/Evaluation/04 - LLM-as-judge — quando e como]].

## Datasets pra eval offline

Trace em produção vira candidato a dataset:

- Marca trace interessante na UI → vira item de dataset
- Roda nova versão do prompt contra o dataset todo → compara scores
- CI/CD integration: rodar dataset eval em cada PR ([[03-Dominios/Tecnologia/IA/Evaluation/07 - Eval em CI-CD]])

Loop completo: produção → trace → dataset → eval → nova versão de prompt → deploy → produção.

## Quando escolher Langfuse

Aplica:

- **Time de 2+ engenheiros de IA** — features de eval/prompt mgmt pagam custo de setup
- **Sistemas com agents ou pipelines multi-step** — hierarquia de span aparece de forma natural
- **Quer OSS** — self-host como opção real, sem feature crippling
- **Vai precisar de eval contínua** — integração trace ↔ dataset ↔ eval em um produto só

Não aplica (ou tem alternativa melhor):

- **Dev solo com Claude Code** — overkill; ccusage + planilha basta
- **Quer só proxy "drop in"** — Helicone resolve com mudança de `base_url`; OpenLLMetry resolve com OTel direto
- **Já tem stack OTel madura (Datadog, Honeycomb)** — OpenLLMetry exporta pra eles direto, sem trazer outro backend

## Fontes

- **Langfuse** — [Documentação](https://langfuse.com/docs) · [Tracing](https://langfuse.com/docs/tracing) · [Prompt Management](https://langfuse.com/docs/prompts/get-started) · [Self-hosting](https://langfuse.com/self-hosting).
- **Langfuse** — [GitHub langfuse/langfuse](https://github.com/langfuse/langfuse). Repo principal, licença MIT.
- **Langfuse** — [SDK Python](https://github.com/langfuse/langfuse-python) — decorator `@observe()` documentado.

## Veja também

- [[02 - Anatomia de um trace LLM]] — a hierarquia que Langfuse materializa
- [[04 - Helicone, Phoenix, OpenLLMetry — alternativas]] — quando outras ferramentas cabem melhor
- [[05 - Versionamento de prompts]] — como o registry de prompts do Langfuse encaixa
- [[Evaluation]] — Langfuse evals como parte do loop
- [[Dicionário de IA#Langfuse|Dicionário: Langfuse]]
