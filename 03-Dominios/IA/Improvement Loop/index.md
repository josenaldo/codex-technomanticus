---
title: "Improvement Loop"
type: moc
publish: true
tags:
  - improvement-loop
  - ia
  - moc
created: 2026-05-28
updated: 2026-05-28
aliases:
  - Ciclo de Melhoria
  - Prompt Improvement
---

# Improvement Loop

One-shot prompt é tabu — sistemas de IA em produção melhoram em loop: eval mostra regressão, diff mostra o quê mudar, ship valida. Esta trilha trata melhoria contínua como **disciplina**, não como tarefa de "limpar o prompt quando der tempo". Senta em cima de duas outras trilhas: [[Evaluation]] entrega o sinal (eval score, golden set, judge), [[Observability]] entrega o detalhe (trace, custo, latência, versão); o Improvement Loop é o ciclo que **fecha** entre as duas, traduzindo sinal e detalhe em mudanças versionadas, testadas e promovidas.

> [!info] Pré-requisitos
> [[Evaluation]] e [[Observability]] são pré-requisitos efetivos. Sem eval você não sabe se a mudança melhorou; sem observability você não sabe **o que** mudar. Esta trilha assume que ambos estão no lugar (mesmo que em estado seedling).

> [!warning] Onde esta trilha mora no stack
> A [[AI Engineering Stack/12 - Improvement Layer|Improvement Layer]] do stack referencia esta trilha como aprofundamento. O stack define o **conceito** (loop fechado, cadência, ownership); esta trilha cobre a **mecânica** (eval gate, A/B, semver, champion-challenger, auto-prompt).

## Comece por aqui

Trilha sequencial recomendada — ciclo → mecânica → automação → sinais → CI.

### Bloco 1 — O ciclo (1 nota)

A forma canônica do loop e a maturidade que ele representa.

- [[01 - O ciclo eval → diff → ship]] — observability surface → eval mede → hipótese → A/B → champion-challenger → ship; maturidade ladder; posição no [[AI Engineering Stack/12 - Improvement Layer|stack]]

### Bloco 2 — Mecânica (3 notas)

Os três artefatos operacionais do loop: o experimento, a versão, a promoção.

- [[02 - A-B testing de prompts]] — control vs treatment; sample size; frequentista vs bayesiano pra LLM; peeking como anti-padrão
- [[03 - Prompt versioning — semver para prompts]] — quando bumpar (e que cada bump dispara); ponte com [[Observability/05 - Versionamento de prompts|Observability/05]] que cobre o **como**
- [[04 - Champion-challenger em produção]] — traffic split, métricas-gate, promoção/rollback automáticos, anti-pattern do challenger eterno

### Bloco 3 — Automação (1 nota)

Quando a otimização do prompt deixa de ser artesanato.

- [[05 - Auto-prompt optimization — DSPy e além]] — DSPy (Signatures, Modules, Compilers); APE, OPRO, promptbreeder; quando auto-prompt vence vs quando ajuste manual vence

### Bloco 4 — Sinais (1 nota)

Onde vem o sinal humano que alimenta o loop.

- [[06 - Capturando feedback do usuário como sinal]] — explícito vs implícito; weighting; confounders (confirmation bias, popularity ≠ qualidade); quando feedback bate de frente com eval

### Bloco 5 — CI (1 nota)

Como o loop atravessa o pipeline de entrega.

- [[07 - Eval gates em CI — quando bloquear merge]] — threshold por categoria; sampling barato em PR + full em main; quarentena de flaky; ponte com [[Evaluation/07 - Eval em CI-CD|Evaluation/07]] que cobre o pipeline mais amplo

## Rotas alternativas

### Rota mínima (preciso resolver hoje)

*"Mudei prompt, preciso saber se melhorou — sem eval gate ainda"*

[[01 - O ciclo eval → diff → ship]] → [[02 - A-B testing de prompts]] → [[03 - Prompt versioning — semver para prompts]]

### Rota produção (já tenho eval, falta ciclo)

*"Tenho eval rodando, prompt versionado, mas mudança vai pra prod no susto"*

[[04 - Champion-challenger em produção]] → [[07 - Eval gates em CI — quando bloquear merge]] → [[06 - Capturando feedback do usuário como sinal]]

### Rota automação (já tenho loop manual)

*"Loop manual funciona mas quero escalar otimização do prompt"*

[[05 - Auto-prompt optimization — DSPy e além]] → [[02 - A-B testing de prompts]] → [[04 - Champion-challenger em produção]]

## Leituras recomendadas

| Fonte | Tipo | Cobertura |
|-------|------|-----------|
| **@hooeem** — *Become an AI Engineer*, cap. #11 (Improvement) e #18 Step 11 | Thread/Ensaio | Trilha inteira; vocabulário do "improvement layer" |
| **Hamel Husain** — [*Your AI Product Needs Evals*](https://hamel.dev/blog/posts/evals/) | Ensaio | Notas 01, 06, 07; eval como sinal contínuo |
| **Khattab et al.** — *DSPy: Compiling Declarative Language Model Calls into Self-Improving Pipelines* ([arxiv:2310.03714](https://arxiv.org/abs/2310.03714)) | Paper | Nota 05; fundamento do auto-prompt declarativo |
| **Zhou et al.** — *Large Language Models Are Human-Level Prompt Engineers* (APE, [arxiv:2211.01910](https://arxiv.org/abs/2211.01910)) | Paper | Nota 05 |
| **Yang et al.** — *Large Language Models as Optimizers* (OPRO, [arxiv:2309.03409](https://arxiv.org/abs/2309.03409)) | Paper | Nota 05 |
| **OpenAI** — [*Evals cookbook*](https://github.com/openai/openai-cookbook/tree/main/examples/evaluation) | Cookbook | Notas 01, 07 |
| **Statsig / GrowthBook / Eppo** — docs de experimentação | Documentação | Nota 02; A/B framework |

## Veja também

- [[AI Engineering Stack]] — onde a Improvement Layer se encaixa
- [[AI Engineering Stack/12 - Improvement Layer]] — a camada conceitual que esta trilha aprofunda
- [[Evaluation]] — pré-requisito; entrega o sinal pro loop
- [[Observability]] — pré-requisito; entrega o detalhe pro loop
- [[Prompt Engineering]] — onde os prompts nascem antes de virarem objeto de melhoria
- [[Structured Outputs]] — schema estável é pré-condição pra A/B comparável

## Todas as notas

```dataview
LIST
FROM "03-Dominios/IA/Improvement Loop"
WHERE type != "moc"
SORT file.name ASC
```
