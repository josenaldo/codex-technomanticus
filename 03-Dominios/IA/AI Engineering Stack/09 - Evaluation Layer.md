---
title: "Evaluation Layer"
created: 2026-05-28
updated: 2026-05-28
type: concept
status: seedling
progress: in_progress
tags:
  - ai-engineering-stack
  - ia
  - evaluation
publish: true
aliases:
  - Evaluation Layer
  - Camada de avaliação
---

# Evaluation Layer

> [!abstract] TL;DR
> A Evaluation Layer responde **como saber se o output está bom**. Não é teste unitário — é rubrica + dataset + pipeline que mede acurácia, completude, utilidade, aderência a formato, qualidade de fonte, especificidade, controle de risco. Sem evals, "está melhor" vira intuição; com evals, vira número. A regra de quem está em produção: o sistema com evals fracos perde pro sistema com evals fortes em todas as métricas que importam, porque o segundo consegue iterar com sinal e o primeiro itera no escuro.

## O que é esta camada

A Evaluation Layer é o **régua** do sistema. Mede qualidade do output de forma reproduzível — pra que mudanças (de prompt, modelo, retrieval) possam ser comparadas com objetividade.

Template mínimo (adaptado do thread @hooeem):

```yaml
success_criteria: <herda do Purpose Layer, traduzido em mensurável>
scoring_rubric:
  accuracy: 1-5
  completeness: 1-5
  usefulness: 1-5
  format_adherence: 1-5
  source_quality: 1-5
  specificity: 1-5
  risk_control: 1-5
pass_threshold: <ex: média ≥4 e nenhuma dimensão <3>
automatic_failure_conditions:
  - <condição que zera tudo, ex: vazamento de PII>
  - <ex: chamada de tool proibida>
```

Implementações reais incluem três tipos de eval: (a) **reference-based** — compara contra ground truth; (b) **reference-free** — checa propriedades intrínsecas; (c) **LLM-as-judge** — outro LLM aplica a rubrica.

## Decisões-chave

1. **Dataset de eval.** Sem dataset, não há eval. Comece pequeno (20-50 exemplos curados à mão), inclua casos fáceis, médios, difíceis, edge cases e regressões conhecidas. Cresça com casos reais que falharam.

2. **Rubrica.** Cada dimensão precisa de definição operacional. "Acurácia 4" tem que significar a mesma coisa quando dois revisores aplicam. Definições vagas degeneram pra "achismo escala 1-5".

3. **LLM-as-judge.** Útil pra escalar evals (humano não revisa 1000 casos por iteração), mas exige calibração contra humano em uma amostra. Sem calibração, é só mais um modelo opinando.

4. **Automatic failure conditions.** Coisas que zeram a nota total, não importa o resto: vazamento de PII, chamada de tool proibida, formato inválido. São o link entre Evaluation Layer e Guardrail Layer.

5. **Frequência.** Eval que roda só "no final do trimestre" não dá sinal. Idealmente roda em cada PR (regression eval) e em produção amostralmente (live eval).

## Onde aprofundar no Codex

- **[[Evaluation]]** — trilha-irmã dedicada (em construção).
- **[[Anatomia de Agents/09 - Evaluation de agents|Evaluation de agents]]** — particularidades quando o sistema é agentic.
- **[[RAG e Vector Databases/09 - Evaluation de RAG|Evaluation de RAG]]** — métricas específicas (recall, precision, faithfulness).

## Veja também

- [[02 - Purpose Layer — o que o sistema é]] — success_criteria descem daqui
- [[10 - Guardrail Layer]] — automatic_failure_conditions são guardrails
- [[11 - Logging Layer]] — scores entram em log

## Fontes

- **@hooeem** — *Become an AI Engineer*, chapter #18, Step 8 (Evaluation layer template).
- **Eugene Yan** — [*Evals are all you need*](https://eugeneyan.com/writing/evals/). Argumento por evals como vantagem competitiva.
- **Hamel Husain** — [*Your AI product needs evals*](https://hamel.dev/blog/posts/evals/). Guia prático.
