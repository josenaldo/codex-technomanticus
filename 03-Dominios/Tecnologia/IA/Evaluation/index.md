---
title: "Evaluation"
type: moc
publish: true
tags:
  - evaluation
  - ia
  - moc
created: 2026-05-28
updated: 2026-05-28
aliases:
  - Evals
  - Avaliação de LLMs
  - LLM Evaluation
---

# Evaluation

Sem evals, desenvolvimento com LLM vira vibes: qualquer sistema com LLM em produção que não tenha eval-driven development está iterando no escuro. Karpathy chama isso de *"vibe coding"*; Hamel Husain, em *Your AI Product Needs Evals*, argumenta que sem evals você tem demo, não produto; Eugene Yan vai mais longe — *"evals are all you need"* — e defende que evals são a vantagem competitiva real, mais ainda que o prompt em si. Esta trilha é a **casa mestre** de eval no Codex: trata evaluation como uma disciplina contínua (não como teste de aceite no fim do projeto), e cobre desde a mentalidade (EDD — eval-driven development) até a operação em CI/CD e a especialização por tipo de sistema avaliado.

> [!info] Pré-requisitos
> [[Anatomia dos LLMs]] é suficiente. Familiaridade com [[AI Engineering Stack]] ajuda a entender onde a Evaluation Layer se encaixa, mas não é obrigatória.

> [!warning] Esta trilha é a disciplina; as notas contextuais ficam nas anatomias
> Já existem três notas de eval no Codex, cada uma cobrindo eval **dentro** de um contexto específico:
> - [[03-Dominios/Tecnologia/IA/Anatomia dos LLMs/19 - Evaluation de LLMs em produção]] — eval de LLM puro em produção (4 pilares: golden set, LLM-as-judge, observabilidade, A/B test)
> - [[03-Dominios/Tecnologia/IA/Anatomia de Agents/09 - Evaluation de agents]] — eval de sistemas agentic (task completion rate, trace review, error types)
> - [[03-Dominios/Tecnologia/IA/RAG e Vector Databases/09 - Evaluation de RAG]] — métricas canônicas Ragas (context precision/recall, faithfulness, answer relevance)
>
> Esta trilha **não duplica** o conteúdo delas. É o tronco que define eval como disciplina; aquelas três são os galhos contextuais. A nota [[08 - Eval por contexto — LLM, RAG, agent, prompt]] fecha a ponte e linka pra cada uma.

## Comece por aqui

Trilha sequencial recomendada — mentalidade → construção do dataset/rubrica → operação contínua → especialização.

### Bloco 1 — Mentalidade (1 nota)

A virada de chave conceitual que precede qualquer ferramenta.

- [[01 - Eval-driven development — a disciplina]] — o shift de *"rodei 3 vezes e parece bom"* pra medição sistemática; analogia com TDD; quando EDD aplica vs. quando é overkill

### Bloco 2 — Construção (3 notas)

Os três artefatos que viabilizam eval automatizado: o dataset, a rubrica e o juiz.

- [[02 - Golden datasets — como construir]] — pares input-output canônicos, representatividade, edge cases, anti-tests, versionamento
- [[03 - Scoring rubrics e critérios]] — design de rubrica, escalas (Likert, binário, multi-dim), inter-rater agreement, anchored scales com exemplos
- [[04 - LLM-as-judge — quando e como]] — quando funciona, vieses (posicional, verbosidade, self-preference), técnicas de mitigação

### Bloco 3 — Operação (3 notas)

A passagem do laboratório pro pipeline contínuo — onde eval vira parte do ciclo de vida do produto.

- [[05 - Regression testing em LLMs]] — snapshot diff, semantic vs string diff, quando rebless do snapshot, categorias de teste
- [[06 - Frameworks 2026 — Promptfoo, Braintrust, Langfuse, Patronus, Phoenix]] — comparação dos cinco frameworks dominantes em 2026, decision tree, self-hosted vs SaaS
- [[07 - Eval em CI-CD]] — eval gates em PR, estratégias de sampling, quarentena de evals flaky, workflow GitHub Actions

### Bloco 4 — Especialização (1 nota)

Como eval muda quando o sistema avaliado é mais que um prompt isolado.

- [[08 - Eval por contexto — LLM, RAG, agent, prompt]] — eval de prompt, de RAG, de agent e de LLM base; ponte com as três notas contextuais existentes

### Bloco 5 — Abstenção (1 nota)

O comportamento que você precisa **projetar** para poder medir. As notas 01 e 02 dizem para incluir anti-tests no golden set; esta cobre o outro lado — por que o modelo não se abstém sozinho, como se implementa abstenção num sistema real, e como se sabe se ela está calibrada.

- [[09 - Abstenção — projetar e medir o não sei]] — o incentivo que o RLHF não deu, os 4 passos (autorizar, formatar, rotear, recompensar), a matriz alucinação confiante × abstenção covarde

## Rotas alternativas

### Rota mínima (preciso resolver hoje)

*"Tenho prompt em produção sem eval — me dê o caminho mais curto"*

[[01 - Eval-driven development — a disciplina]] → [[02 - Golden datasets — como construir]] → [[03 - Scoring rubrics e critérios]] → [[07 - Eval em CI-CD]]

### Rota framework-first (já sei a teoria)

*"Quero comparar Promptfoo, Braintrust, Langfuse — qual escolher?"*

[[06 - Frameworks 2026 — Promptfoo, Braintrust, Langfuse, Patronus, Phoenix]] → [[07 - Eval em CI-CD]] → [[05 - Regression testing em LLMs]]

### Rota LLM-as-judge (quero escalar eval subjetivo)

*"Humano não revisa 1000 outputs por iteração — preciso de judge automático"*

[[03 - Scoring rubrics e critérios]] → [[04 - LLM-as-judge — quando e como]] → [[02 - Golden datasets — como construir]] → [[06 - Frameworks 2026 — Promptfoo, Braintrust, Langfuse, Patronus, Phoenix]]

### Rota por tipo de sistema

*"Estou avaliando agent / RAG / prompt simples — qual o caminho?"*

[[08 - Eval por contexto — LLM, RAG, agent, prompt]] → nota contextual correspondente (Anatomia de Agents/09, RAG/09 ou Anatomia dos LLMs/17) → volta pra [[02 - Golden datasets — como construir]] e [[03 - Scoring rubrics e critérios]]

## Leituras recomendadas

| Fonte | Tipo | Cobertura |
|-------|------|-----------|
| **Hamel Husain** — [*Your AI Product Needs Evals*](https://hamel.dev/blog/posts/evals/) | Ensaio | Trilha inteira; manifesto canônico de EDD |
| **Eugene Yan** — [*Evals are all you need*](https://eugeneyan.com/writing/evals/) | Ensaio | Notas 01, 03; argumento por evals como vantagem competitiva |
| **Chip Huyen** — *AI Engineering* (2025), capítulo sobre evaluation | Livro | Trilha inteira; visão sistemática |
| **OpenAI** — [*OpenAI Evals* (github)](https://github.com/openai/evals) | Framework + docs | Notas 02, 03, 06 |
| **Anthropic** — [*Eval cookbook*](https://github.com/anthropics/anthropic-cookbook/tree/main/misc/evals) | Cookbook | Notas 03, 04 |
| **Liu et al.** — *G-Eval: NLG Evaluation using GPT-4 with Better Human Alignment* ([arxiv:2303.16634](https://arxiv.org/abs/2303.16634)) | Paper | Nota 04 |
| **Zheng et al.** — *Judging LLM-as-a-Judge* ([arxiv:2306.05685](https://arxiv.org/abs/2306.05685)) | Paper | Nota 04; vieses do judge |
| **EleutherAI** — [*lm-evaluation-harness*](https://github.com/EleutherAI/lm-evaluation-harness) | Framework | Nota 08; benchmarks acadêmicos |

## Veja também

- [[AI Engineering Stack]] — onde a Evaluation Layer se encaixa no stack
- [[03-Dominios/Tecnologia/IA/AI Engineering Stack/09 - Evaluation Layer]] — a camada que aponta pra esta trilha como aprofundamento
- [[03-Dominios/Tecnologia/IA/Anatomia de Agents/09 - Evaluation de agents]] — eval contextual de sistemas agentic
- [[03-Dominios/Tecnologia/IA/Anatomia dos LLMs/19 - Evaluation de LLMs em produção]] — eval contextual de LLM puro em prod
- [[03-Dominios/Tecnologia/IA/RAG e Vector Databases/09 - Evaluation de RAG]] — eval contextual de pipelines RAG
- [[Improvement Loop]] — o ciclo de melhoria contínua onde evals entregam o sinal (em construção)
- [[Segurança e Guardrails]] — guardrails são automatic_failure_conditions da rubrica
- [[Prompt Engineering]] — evals dizem se o prompt melhorou ou piorou

## Todas as notas

```dataview
LIST
FROM "03-Dominios/Tecnologia/IA/Evaluation"
WHERE type != "moc"
SORT file.name ASC
```
