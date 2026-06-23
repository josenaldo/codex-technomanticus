---
title: "Observability"
type: moc
publish: true
tags:
  - observability
  - ia
  - moc
created: 2026-05-28
updated: 2026-05-28
aliases:
  - Observabilidade de LLMs
  - LLM Observability
  - Tracing
---

# Observability

Sem observability, debugar LLM em produção é arqueologia — você sabe que algo quebrou ontem mas não sabe o quê. Stack tracking convencional (APM, logs estruturados, métricas) foi desenhado pra HTTP, banco e fila — não pra um sistema onde a unidade de trabalho é uma chamada com 12k tokens de entrada, 3 ferramentas executadas no meio, 1.800 tokens de raciocínio invisíveis ao usuário e um output que pode variar de 200 a 8.000 tokens dependendo da pergunta. Esta trilha define **observability de LLM como disciplina distinta**: o que precisa ser instrumentado, em que padrão, com qual ferramenta, e como manter compliance enquanto você loga prompts que muitas vezes contêm PII.

> [!info] Pré-requisitos
> [[Anatomia dos LLMs]] resolve a unidade básica (token, contexto, custo). Recomendo passar antes pelo ângulo de custo em [[Economia de Tokens/04 - Monitoramento — ccusage, Langfuse, dashboards]] — esta trilha **complementa** aquela: lá o foco é dinheiro, aqui o foco é qualidade, debug e compliance.

> [!warning] Esta trilha não duplica a nota de monitoramento de custos
> A nota [[Economia de Tokens/04 - Monitoramento — ccusage, Langfuse, dashboards]] cobre o ângulo financeiro (ccusage, dashboards de provider, alertas de custo, breakdown por modelo). Esta trilha cobre o restante: anatomia de trace, escolha de ferramenta de tracing, versionamento de prompts, session replay, métricas além de custo, e PII em logs. Quando precisar dos dois ângulos, leia em conjunto.

## Comece por aqui

Trilha sequencial recomendada — por quê → o que é o dado → ferramentas → práticas de uso → compliance.

### Bloco 1 — Por quê (1 nota)

A justificativa pra ter uma stack separada de observability pra LLM.

- [[01 - Por que LLMs precisam de observabilidade]] — APM tradicional não captura o que importa em LLM systems; o que está faltando; o custo de não ter

### Bloco 2 — O dado (1 nota)

A estrutura fundamental que toda ferramenta de tracing manipula.

- [[02 - Anatomia de um trace LLM]] — sessão, trace, spans; convenções semânticas OpenTelemetry GenAI; hierarquia em agents; diagrama da árvore de trace

### Bloco 3 — Ferramentas (2 notas)

O ecossistema de tracing em 2026 — quem é referência e quem são alternativas viáveis.

- [[03 - Langfuse — open-source standard]] — por que Langfuse virou referência OSS; arquitetura; self-host vs cloud; decorator `@observe()`; quando escolher
- [[04 - Helicone, Phoenix, OpenLLMetry — alternativas]] — Helicone (proxy), Arize Phoenix (ML-native), OpenLLMetry (puro OTel); tabela de comparação; quando cada um cabe

### Bloco 4 — Práticas (3 notas)

Como usar tracing pra resolver problemas operacionais reais.

- [[05 - Versionamento de prompts]] — prompt como artefato versionado, não config string; semver-pra-prompt; dev/staging/prod; tying a versão ao trace
- [[06 - Session replay e debugging]] — reproduzir bug a partir de dados de observability; captura completa vs sampling; estratégias de replay
- [[07 - Métricas que importam — latência, custo, qualidade]] — P50/P95/P99, TTFT, cost per user, feedback ratio; dashboards essenciais; SLI/SLO para LLM

### Bloco 5 — Compliance (1 nota)

A camada legal e ética sem a qual logging vira passivo.

- [[08 - Privacy e PII em logs]] — PII como vetor de vazamento default; redaction em captura; retention; GDPR, LGPD, EU AI Act

## Rotas alternativas

### Rota mínima (preciso resolver hoje)

*"Tenho LLM em produção e zero observability — me dê o caminho mais curto"*

[[01 - Por que LLMs precisam de observabilidade]] → [[02 - Anatomia de um trace LLM]] → [[03 - Langfuse — open-source standard]] → [[08 - Privacy e PII em logs]]

### Rota debug-first (já estou afogado em incidente)

*"Tenho um bug em produção que não consigo reproduzir — preciso instrumentar pra ontem"*

[[06 - Session replay e debugging]] → [[02 - Anatomia de um trace LLM]] → [[03 - Langfuse — open-source standard]]

### Rota platform-engineering (estou desenhando a stack)

*"Estou montando observability greenfield — quero escolher bem"*

[[02 - Anatomia de um trace LLM]] → [[04 - Helicone, Phoenix, OpenLLMetry — alternativas]] → [[03 - Langfuse — open-source standard]] → [[07 - Métricas que importam — latência, custo, qualidade]] → [[08 - Privacy e PII em logs]]

### Rota compliance-first (já fui chamado pelo jurídico)

*"Logging vazou PII / preciso documentar tracing pra auditoria"*

[[08 - Privacy e PII em logs]] → [[05 - Versionamento de prompts]] → [[02 - Anatomia de um trace LLM]]

## Leituras recomendadas

| Fonte | Tipo | Cobertura |
|-------|------|-----------|
| **OpenTelemetry** — [*Semantic Conventions for Generative AI*](https://opentelemetry.io/docs/specs/semconv/gen-ai/) | Spec | Nota 02; padrão dos atributos `gen_ai.*` |
| **Langfuse** — [*Documentation*](https://langfuse.com/docs) · [*Tracing*](https://langfuse.com/docs/tracing) | Docs | Notas 03, 05, 06 |
| **OpenLLMetry** — [*GitHub traceloop/openllmetry*](https://github.com/traceloop/openllmetry) | Lib + docs | Nota 04; instrumentação OTel pura |
| **Arize Phoenix** — [*phoenix.arize.com*](https://phoenix.arize.com) · [*GitHub*](https://github.com/Arize-ai/phoenix) | OSS + docs | Nota 04 |
| **Helicone** — [*Docs*](https://docs.helicone.ai) | Docs | Nota 04 |
| **Honeycomb** — [*LLM observability talks*](https://www.honeycomb.io/blog) | Posts + palestras | Notas 01, 07; observability geral aplicada a LLM |
| **Anthropic** — [*Building effective agents — tracing section*](https://www.anthropic.com/research/building-effective-agents) | Post | Notas 01, 02; tracing em agents |
| **Hamel Husain** — [*Your AI Product Needs Evals*](https://hamel.dev/blog/posts/evals/) | Ensaio | Nota 01; observability como gêmeo de eval |
| **EU AI Act** — [Texto consolidado](https://artificialintelligenceact.eu/) | Regulação | Nota 08 |
| **LGPD** — [Lei 13.709/2018](https://www.planalto.gov.br/ccivil_03/_ato2015-2018/2018/lei/l13709.htm) | Lei | Nota 08 |

## Veja também

- [[AI Engineering Stack]] — onde a Logging Layer e Observability se encaixam no stack
- [[AI Engineering Stack/11 - Logging Layer]] — a camada que aponta pra esta trilha como aprofundamento
- [[Evaluation]] — observability fornece o sinal contínuo; eval fornece o critério
- [[Economia de Tokens/04 - Monitoramento — ccusage, Langfuse, dashboards]] — o ângulo de custo que esta trilha complementa
- [[Improvement Loop]] — o ciclo onde traces viram dataset de eval e dataset vira nova versão (em construção)
- [[Segurança e Guardrails]] — incidentes de guardrail são registrados via observability

## Todas as notas

```dataview
LIST
FROM "03-Dominios/Tecnologia/IA/Observability"
WHERE type != "moc"
SORT file.name ASC
```
