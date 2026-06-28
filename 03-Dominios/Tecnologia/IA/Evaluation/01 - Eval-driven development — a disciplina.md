---
title: "01 - Eval-driven development — a disciplina"
created: 2026-05-28
updated: 2026-05-28
type: concept
status: seedling
progress: in_progress
fase: Iniciado
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

> [!question]- O que eu preciso saber antes de ler isso?
> Esta nota não exige conhecimento de código — é conceitual. A premissa é que você já tem algum sistema com LLM: um chatbot, um extrator de dados, um classificador, qualquer coisa que roda mais de uma vez. E que você provavelmente está tomando decisões sobre esse sistema baseado em "rodar algumas vezes e ver se parece bom". EDD é a alternativa sistemática a isso. Se você vem de desenvolvimento de software tradicional, a analogia com TDD é direta e intuitiva. Se você nunca fez TDD, não preocupa — a nota explica do zero.

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

## O custo invisível de não ter evals

Equipes sem evals tomam decisões de prompt da seguinte forma: alguém muda o prompt, roda 5-10 inputs à mão, "acha que melhorou", e dá merge. O problema é que "rodar 5-10 inputs" é viés de confirmação sistemático — você tende a testar os inputs que você acha que funcionam, não os casos de borda que revelam o que não funciona.

O custo acumulado:

- **Merge do merge.** Cada PR muda o prompt baseado em intuição. Sem baseline, ninguém sabe se o sistema melhorou ou piorou no global.
- **Regressões silenciosas.** Um caso que funcionava bem de repente começa a falhar — mas como ninguém testou aquele específico, só aparece quando usuário reclama.
- **Paralisia de iteração.** Com o tempo, ninguém quer mudar nada porque "a última mudança quebrou X" — mas sem dataset, ninguém sabe o que X é.
- **Incapacidade de comparar modelos.** "Devemos migrar de GPT-4o para Claude Sonnet?" Se você não tem golden set com scores, a resposta honesta é "não sabemos".

EDD converte esse custo invisível em custo visível e gerenciável: o custo de manter o golden set e rodar evals é pequeno e previsível.

## A assimetria temporal

A objeção mais comum é que evals custam tempo no início. É verdade — e é a armadilha. O tempo é front-loaded (semana 1-2) mas o retorno é long-tail (meses a anos). Quem avalia o custo de evals só pela semana 1 vai sempre achar caro. Quem avalia pelo custo total do projeto vai sempre achar barato.

A assimetria concreta: montar um golden set de 50 casos custa ~4 horas. Cada incidente de regressão silenciosa que o golden set teria detectado custa ~8-16 horas de debug + rollback + comunicação. Um incidente paga pelo golden set. No segundo, você está lucrando.

## Como começar amanhã

1. Escolha **um** prompt em produção. O mais crítico.
2. Coleta 20 inputs reais dos últimos 7 dias (logs).
3. Escreve a resposta esperada à mão pra cada um. Sim, 20 vezes. Isso é o golden set v0.
4. Define 3 dimensões de qualidade ([[03 - Scoring rubrics e critérios]]).
5. Roda manualmente — o que você acharia 4-5/5, o que acharia 1-2/5?
6. Codifica isso em script. Roda em CI próximo PR.

Em uma semana você tem nível 1. Em duas, nível 2. O resto é refinamento.

## Armadilhas comuns

> [!warning] Montar golden set com casos felizes
> O instinto é montar o golden set com casos onde o modelo já funciona bem — o que você usou pra demonstrar que o sistema funciona. Esse dataset não detecta regressões, porque os casos problemáticos não estão nele. Golden sets úteis incluem: casos de borda, inputs ambíguos, entradas com formatação estranha, casos onde o modelo falhou historicamente, e casos onde a resposta correta é "não sei" ou "recusar". Quanto mais contra-intuitivos os casos, mais útil o conjunto.

> [!warning] Evals como formalidade de lançamento, não como prática contínua
> É comum montar evals na semana do lançamento para "ter". O problema: o golden set fica congelado, ninguém roda em PRs subsequentes, e os bugs de produção nunca voltam pro dataset. Dois meses depois, o eval existe mas não detecta nada que importa. EDD é uma prática contínua: todo bug em produção vira caso no golden set, todo PR que toca no prompt roda o eval, e o score vai para o histórico do projeto. Sem o loop de feedback entre produção e golden set, o eval vira fóssil.

> [!warning] Confiar em métricas técnicas sem métricas de negócio
> Accuracy de 92% no golden set não significa que o produto entregou valor. Um sistema de suporte que acerta o tom mas resolve 30% menos tickets do que a versão anterior está piorando o negócio, mesmo com score técnico alto. EDD completo inclui dois ciclos: evals técnicos (golden set, rubrica) para velocidade de iteração, e evals de negócio (resolution rate, CSAT, tempo de resposta) para confirmar que melhorias técnicas se traduzem em valor. Sem os dois, você pode estar otimizando a métrica errada.

## Como explicar em inglês

Em entrevistas sobre AI Engineering ou em design reviews de sistemas com LLM, a disciplina de EDD aparece como diferenciador entre quem tem experiência de produção e quem tem só experiência de prototipagem:

> "Eval-driven development is the practice of measuring systematically before and after every change to a prompt or model, instead of testing a few cases manually and calling it 'looks good.' The workflow mirrors TDD: you define what good means — golden dataset plus scoring rubric — before writing the first prompt. Every prompt change generates a score against the baseline. Every production bug becomes a new case in the golden set as a permanent regression test. Without evals, you're iterating blind."

| Português | Inglês |
|-----------|--------|
| dataset dourado | golden dataset / golden set |
| rubrica de avaliação | scoring rubric |
| regressão de qualidade | quality regression |
| eval baseline | eval baseline |
| eval em CI/CD | eval in CI/CD |
| golden set congelado | frozen/stale golden set |
| caso de borda | edge case |
| métricas de negócio | business metrics |
| avaliação graduada | graduated evaluation |
| juiz LLM | LLM-as-judge |

## O que vem a seguir

Com a disciplina estabelecida, a nota 02 entra nos detalhes práticos do asset mais importante de EDD: o golden dataset. Como construir um conjunto que realmente detecta regressões — quantos exemplos, de onde vêm, como garantem cobertura dos casos que importam.

Ver [[02 - Golden datasets — como construir]].

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
