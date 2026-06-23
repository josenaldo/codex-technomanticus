---
title: "01 - Eval-driven development — a disciplina"
created: 2026-05-28
updated: 2026-05-28
type: concept
status: seedling
progress: in_progress
tags:
  - evaluation
  - ia
  - edd
  - disciplina
publish: true
aliases:
  - EDD
  - Eval-driven development
  - Evals first prompts second
---

# 01 - Eval-driven development — a disciplina

> [!abstract] TL;DR
> Eval-driven development (EDD) é o shift de *"rodei 3 vezes e olhei, parece bom"* pra **medição sistemática contínua**. A analogia com TDD é direta: TDD escreve teste antes do código; EDD escreve eval antes do prompt. O princípio operacional é *"evals first, prompts second"* — sem dataset e rubrica, qualquer mudança de prompt vira aposta. EDD se aplica a qualquer sistema repetível com LLM em produção; é overkill em one-shots, brainstorming e exploração inicial. Parafraseando a tese de Hamel Husain em *Your AI Product Needs Evals*: sem evals você não tem produto, tem demo.

## O shift conceitual

Antes:

```
1. Escrever prompt v1
2. Testar 3-5 inputs manualmente
3. "Parece bom" → deploy
4. Usuário reclama → mudar prompt v2
5. Testar 3-5 inputs (diferentes dos anteriores)
6. "Tá melhor" → deploy
7. Usuário reclama de outra coisa
8. Repetir, sem nunca saber se v2 > v1 ou v3 > v2
```

Depois (EDD):

```
1. Definir o que "bom" significa → rubrica
2. Coletar 30-100 exemplos canônicos → golden set
3. Rodar baseline com prompt v1 → score X
4. Mudar pra v2 → roda eval → score Y
5. Decide com base em X vs Y, não em "achei melhor"
6. Bug em prod → vira novo caso no golden set → regression test permanente
```

A diferença não é só rigor. É **memória**. Com EDD, o conhecimento acumulado fica no dataset; sem EDD, fica espalhado em decisões de quem estava no time naquele dia.

## Analogia com TDD

| TDD | EDD |
|---|---|
| Escreve teste antes do código | Escreve eval antes do prompt |
| Vermelho → verde → refactor | Baseline → mudar prompt → re-medir |
| Cobertura de teste | Cobertura de cenários no golden set |
| Regressão = teste antigo que quebrou | Regressão = score caiu no golden set |
| Falha de teste bloqueia merge | Falha de eval bloqueia merge ([[07 - Eval em CI-CD]]) |

A analogia tem um limite importante: testes tradicionais são **booleanos** (passa ou falha); evals são **graduados** (score 4.2/5 com threshold em 4.0). Isso muda o ferramental, mas não a mentalidade.

## O princípio: evals first, prompts second

Antes de escrever uma linha de prompt:

1. **Tarefa.** Qual o input e o output esperado em palavras humanas?
2. **Critério de sucesso.** Como você reconhece um output bom? Liste 3-5 dimensões.
3. **Exemplos.** 5-10 pares input-output que você consideraria sucesso. Comece pelo dataset, mesmo que minúsculo.
4. **Anti-tests.** 2-3 inputs onde o modelo **deveria** recusar ou responder "não sei".

Só **depois** desses quatro passos é hora de escrever prompt. Esse trabalho upstream é o que evita o ciclo de iteração cega.

> [!tip] Hamel Husain — *Your AI Product Needs Evals*
> *"Most teams skip evals because they feel slower upfront. But the alternative is iterating on prompts forever without knowing if you're moving forward or sideways. The team that builds evals first ships better products faster — not because they're more rigorous, but because every change generates signal instead of noise."*

## Quando EDD aplica

Aplica:

- **Pipelines de produção** — qualquer sistema que vai rodar 1000+ vezes/dia
- **Tarefas repetíveis** — classificação, extração, resumo, roteamento, geração com schema
- **Sistemas críticos** — finance, healthcare, legal, compliance (eval é parte do dossiê de auditoria)
- **Multi-prompt pipelines** — quando você tem 3+ chamadas encadeadas e precisa isolar qual mudou

Não aplica (ou é overkill):

- **One-shots** — "me escreve um email pro meu chefe agora"
- **Brainstorming** — exploração criativa onde "errado" não tem definição
- **POC inicial** — primeira semana descobrindo se o problema tem solução. Antes de ter eval, você precisa ter sistema.
- **Tarefas verdadeiramente subjetivas** — escolha de capa de livro, escrita de poesia sem brief específico

O risco de fazer EDD prematuro é gastar 2 semanas montando golden set pra um produto que pivota. O risco de não fazer EDD depois que o produto estabilizou é ficar refém de intuição.

## Maturidade EDD

| Nível | Sinal |
|---|---|
| **0** | *"Olhei e tá bom"* |
| **1** | Golden set ad-hoc em planilha; rodada manual ocasional |
| **2** | Eval automatizado em CI bloqueando merge |
| **3** | Eval em CI + observabilidade em prod ([[03-Dominios/Tecnologia/IA/Anatomia dos LLMs/19 - Evaluation de LLMs em produção]]) |
| **4** | A/B test em prod com métricas de negócio + judge calibrado |
| **5** | Eval contínuo — golden set evolui com casos reais, regression tests acumulados, dashboard de saúde |

Meta para 2026, segundo Hamel: nível 2 como mínimo absoluto pra qualquer produto com LLM em prod.

## A objeção comum — *"evals são caros"*

Custo típico de eval (Sonnet 4.6, golden set de 100 itens):

```
100 itens × ~$0.005/item = $0.50 por rodada
× 30 rodadas/mês (PRs + main merges) = $15/mês
```

Custo de **não** fazer eval, em produto com LLM em prod:

- 1 incidente de regressão silenciosa = ~16h de debug + churn de usuário
- 1 rollback de prompt em prod = 4-8h de discussão sem dados
- Tempo perdido em "esse prompt é melhor?" sem resposta objetiva = ~8h/semana por engenheiro

O ROI é claro. A objeção real raramente é custo; é cultura.

## OpenAI sobre evals no core

A OpenAI documenta o framework OpenAI Evals com a frase *"evals are at the core of how we develop our models"*. A mensagem implícita pra quem constrói **em cima** dos modelos é a mesma — se o lab que treinou o modelo trata eval como infraestrutura crítica, quem usa o modelo em produto não pode tratar como afterthought.

## Anti-patterns

- **Eval só pre-launch** — escreve eval pra lançar, nunca mais roda
- **Eval rodando, ninguém lendo** — pipeline existe, scores ninguém olha
- **Golden set congelado** — não evolui com bugs reais; vira fóssil
- **Métricas técnicas sem métricas de negócio** — accuracy 92% que não move resolution rate
- **Eval-driven sem driver** — métrica existe, ninguém é responsável por levantar
- **Eval no humano em vez do humano no loop** — humano só revisando output sem feedback que volta pro dataset

## Como começar amanhã

1. Escolha **um** prompt em produção. O mais crítico.
2. Coleta 20 inputs reais dos últimos 7 dias (logs).
3. Escreve a resposta esperada à mão pra cada um. Sim, 20 vezes. Isso é o golden set v0.
4. Define 3 dimensões de qualidade ([[03 - Scoring rubrics e critérios]]).
5. Roda manualmente — o que você acharia 4-5/5, o que acharia 1-2/5?
6. Codifica isso em script. Roda em CI próximo PR.

Em uma semana você tem nível 1. Em duas, nível 2. O resto é refinamento.

## Veja também

- [[02 - Golden datasets — como construir]]
- [[03 - Scoring rubrics e critérios]]
- [[07 - Eval em CI-CD]]
- [[03-Dominios/Tecnologia/IA/AI Engineering Stack/09 - Evaluation Layer]]
- [[03-Dominios/Tecnologia/IA/Anatomia dos LLMs/19 - Evaluation de LLMs em produção]] — os 4 pilares aplicados em produção

## Fontes

- **Hamel Husain** — [*Your AI Product Needs Evals*](https://hamel.dev/blog/posts/evals/) (2024+)
- **Eugene Yan** — [*Evals are all you need*](https://eugeneyan.com/writing/evals/) (2024)
- **OpenAI** — [*OpenAI Evals* (github.com/openai/evals)](https://github.com/openai/evals) — *"evals at the core"*
- **Chip Huyen** — *AI Engineering* (2025), cap. sobre evaluation
- **Andrej Karpathy** — *"Vibe coding"* (X/Twitter, 2025) — termo que motiva o contrapeso disciplinar do EDD
