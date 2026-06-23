---
title: "Improvement Layer"
created: 2026-05-28
updated: 2026-05-28
type: concept
status: seedling
progress: in_progress
tags:
  - ai-engineering-stack
  - ia
  - improvement
publish: true
aliases:
  - Improvement Layer
  - Camada de melhoria
---

# Improvement Layer

> [!abstract] TL;DR
> A Improvement Layer transforma o sistema de IA de **one-off** em **sistema vivo**. Depois de cada uso (ou cada batch), ela pergunta: o que funcionou, o que falhou, o que mudar na próxima. Lê os logs ([[11 - Logging Layer]]) e os scores ([[09 - Evaluation Layer]]), identifica padrões, e retroalimenta Purpose, Prompt e Context. Sem essa camada o sistema estagna; com ela, vira composta: melhora exponencialmente porque cada erro vira regra nova, cada acerto vira referência.

## O que é esta camada

A Improvement Layer é o **loop fechado** do stack. Fecha o ciclo: o sistema age, registra, mede, aprende, ajusta. É a camada que separa "agente de IA implementado" de "sistema de IA operado".

Template mínimo (adaptado do thread @hooeem):

```yaml
review_cadence: <após cada run | batch diário | semanal>
questions_per_review:
  - O que funcionou (preservar)?
  - O que falhou (corrigir)?
  - O que mudar antes da próxima rodada?
artifacts:
  - prompt_version_bumps: <changelog do system prompt>
  - new_failure_modes: <adicionados ao Context Layer>
  - eval_dataset_additions: <novos casos no dataset>
  - new_guardrails: <novos checks>
ownership: <quem revisa, quem decide a mudança>
```

A regra do thread @hooeem: "After each use, ask what worked, what failed, what to change next time." A formulação parece simples mas é a única coisa que separa sistema que melhora de sistema que estagna.

## Decisões-chave

1. **Cadência.** Review a cada run dá sinal denso mas custa atenção humana. Review batch (diário ou semanal) é mais eficiente mas atrasa correção. Cadência híbrida: por-run pra incidentes graves, semanal pra padrões.

2. **Quem revisa.** Reviewer humano dá juízo mas não escala. LLM-as-judge escala mas exige calibração. Padrão maduro: humano define critério, LLM aplica em volume, humano audita amostra.

3. **O que vira artefato.** Insights só viram melhoria quando viram **algo versionado**: prompt diff, novo caso no dataset, novo guardrail. Insight que fica em ata morre.

4. **Versionamento do prompt.** Cada mudança tem versão, motivo, datas, eval scores antes/depois. Permite rollback e A/B test. Sem versionamento, melhoria vira aposta.

5. **Drift detection.** Sistema que era bom mês passado pode degradar (modelo novo no provider, fontes mudaram, distribution shift de input). Improvement Layer deveria flagar drift via eval contínua.

## Onde aprofundar no Codex

- **[[Improvement Loop]]** — trilha-irmã dedicada (em construção).
- **[[03-Dominios/Tecnologia/IA/Anatomia de Agents/09 - Evaluation de agents|Evaluation de agents]]** — eval contínua como entrada do improvement.
- **[[03-Dominios/Tecnologia/IA/Segurança e Guardrails/10 - Métricas de qualidade AI — defect escape rate, rework ratio|Métricas de qualidade AI]]** — métricas operacionais.

## Veja também

- [[09 - Evaluation Layer]] — fonte de sinal pra improvement
- [[11 - Logging Layer]] — fonte de detalhe pra improvement
- [[02 - Purpose Layer — o que o sistema é]] — improvement pode redefinir purpose se realidade exigir

## Fontes

- **@hooeem** — *Become an AI Engineer*, chapter #18, Step 11 (Improvement layer template).
- **Hamel Husain** — [*Your AI product needs evals*](https://hamel.dev/blog/posts/evals/). Eval contínua como loop de improvement.
- **Anthropic** — [*Iterative prompt engineering*](https://docs.anthropic.com/en/docs/build-with-claude/prompt-engineering/overview). Prática de versionamento.
