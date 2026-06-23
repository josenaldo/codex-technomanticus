---
title: "Guardrail Layer"
created: 2026-05-28
updated: 2026-05-28
type: concept
status: seedling
progress: in_progress
tags:
  - ai-engineering-stack
  - ia
  - guardrails
  - segurança
publish: true
aliases:
  - Guardrail Layer
  - Camada de guardrails
---

# Guardrail Layer

> [!abstract] TL;DR
> A Guardrail Layer define **o que o sistema NÃO pode fazer** e impõe isso por código fora do modelo. Difere da Prompt Layer (que pede comportamento): aqui são checks determinísticos antes do input chegar no modelo, depois do output sair, e em qualquer tool call. Categorias: ações permitidas sem aprovação, ações que exigem aprovação, ações proibidas, casos que devem flagar humano, condições de stop, regras de escalation. Sem essa camada, a Prompt Layer é só desejo.

## O que é esta camada

A Guardrail Layer é o **sistema imunológico** do AI engineering stack. Ela checa input antes do modelo ver, valida output antes do usuário receber, intercepta tool calls antes de executar. Tudo isso por código — não por pedido ao modelo.

Template mínimo (adaptado do thread @hooeem):

```yaml
allowed_without_approval:
  - <ação de baixo risco>
requires_approval:
  - <ação reversível, médio risco>
forbidden:
  - <ação irreversível, alto risco>
must_flag:
  - <padrões que precisam atenção: PII, low confidence, conflito>
must_stop_when:
  - <condições que forçam o sistema a parar imediatamente>
escalation_rule: <quem é acionado quando, em que canal, com que SLA>
```

A distinção crucial: **Prompt Layer pede; Guardrail Layer impõe**. "Não responda perguntas médicas" no system prompt é Prompt Layer (frágil). Classificador que detecta intent médico e bloqueia antes do modelo gerar é Guardrail Layer (robusto).

## Decisões-chave

1. **Pre vs post.** Guardrail pre-LLM filtra input (PII redaction, intent classification, [[Dicionário de IA#prompt injection|prompt injection]] detection). Guardrail post-LLM valida output (schema check, toxicity filter, factuality check). Sistemas sérios fazem os dois.

2. **Deterministic vs LLM-based.** Guardrail por regex ou classifier é rápido e barato mas tem falsos negativos. Guardrail por LLM (ex: Llama Guard, custom classifier) tem melhor recall mas adiciona latência e custo. Layered approach (deterministic primeiro, LLM como segunda linha) é o padrão.

3. **Aprovação humana.** Onde está o threshold? Confidence baixo? Custo alto? Classe sensível? A decisão define UX e velocidade.

4. **Kill switches.** Condição que **para** o sistema sem perguntar. Ex: 5 tool failures em sequência, custo da sessão acima do orçamento, padrão de jailbreak detectado. Sem kill switches, agente bug pode rodar até queimar conta.

5. **Logging de incidente.** Toda vez que um guardrail dispara é dado. Sem log, você não consegue ajustar threshold nem identificar padrão de ataque.

## Onde aprofundar no Codex

- **[[Segurança e Guardrails]]** — trilha completa, especialmente [[Segurança e Guardrails/04 - A pirâmide de validação AI|A pirâmide de validação AI]].
- **[[Context Engineering/12 - Guardrails determinísticos|Guardrails determinísticos]]** — control plane antes e depois do LLM.
- **[[Dicionário de IA#Guardrail|Dicionário: Guardrail]]**.

## Veja também

- [[03 - Prompt Layer]] — pedido frágil; aqui é imposição
- [[07 - Tool Layer]] — guardrails interceptam tool calls
- [[09 - Evaluation Layer]] — automatic_failure_conditions são guardrails de qualidade

## Fontes

- **@hooeem** — *Become an AI Engineer*, chapter #18, Step 9 (Guardrail layer template).
- **NIST** — [*AI Risk Management Framework (AI RMF 1.0)*](https://www.nist.gov/itl/ai-risk-management-framework). Categorização de riscos.
- **Meta** — [*Llama Guard*](https://huggingface.co/meta-llama/Llama-Guard-3-8B). Modelo dedicado a guardrails.
