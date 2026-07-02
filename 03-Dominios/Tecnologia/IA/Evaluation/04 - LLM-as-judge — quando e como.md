---
title: "04 - LLM-as-judge — quando e como"
created: 2026-05-28
updated: 2026-07-01
type: concept
status: seedling
progress: in_progress
fase: Iniciado
tags:
  - evaluation
  - ia
  - llm-as-judge
  - vieses
publish: true
aliases:
  - LLM-as-judge
  - LLM judge
  - G-Eval
  - Model-graded eval
---

# 04 - LLM-as-judge — quando e como

> [!abstract] TL;DR
> LLM-as-judge é usar um modelo (geralmente forte) pra **avaliar output de outro modelo** aplicando uma rubrica. Resolve o gargalo de eval subjetivo em escala — humano não revisa 1000 outputs por iteração; judge sim. Funciona bem em tarefas subjetivas calibradas; falha silenciosamente em domínios especializados, em tarefas novas, e por causa de **vieses sistemáticos**: posicional (prefere primeira opção em A/B), verbosidade (prefere resposta mais longa), self-preference (modelo prefere o próprio estilo). Mitigações: chain-of-thought judging, **pairwise** em vez de score absoluto, randomização de posição, swap-judge check, e — sempre — calibração contra humano antes de confiar. Verbete: [[Dicionário de IA#LLM-as-judge|LLM-as-judge]].

> [!question]- O que eu preciso saber antes de ler isso?
> Você entende que EDD requer medição sistemática (nota 01), que o golden set é o conjunto de casos de teste (nota 02), e que a rubrica define o que "bom" significa em termos numéricos (nota 03). Esta nota cobre o mecanismo que permite escalar a anotação: substituir (parcialmente) o humano por outro LLM. O conceito central é simples — um modelo forte julga o output de outro — mas a armadilha é confiar no judge sem calibração. Você não precisa de background em ML formal; familiaridade com chamadas de API LLM e o problema de eval subjetivo é suficiente.

Cada iteração de prompt ou modelo gera dezenas — ou centenas — de outputs que precisam ser avaliados. Humano treinado é o padrão-ouro, mas não escala: revisar 1000 respostas por rodada de experimento não é operacionalmente viável em nenhum pipeline real. LLM-as-judge resolve esse gargalo delegando a anotação a um modelo forte com rubrica explícita — o ciclo de feedback que levaria dias passa a rodar em minutos.

## Quando faz sentido

Aplica:

- **Tarefas subjetivas em escala** — resumo, escrita, chat, helpfulness — onde human-only não dá conta
- **Pipelines com muitos exemplos** — golden set de 500+ itens
- **Iteração frequente** — você quer rodar eval a cada PR
- **Tarefa com rubrica clara** — judge precisa de critério, não de intuição

Não aplica (ou aplica com extremo cuidado):

- **Domínios especializados** — legal, médico, científico de fronteira — judge não tem expertise
- **Tarefas novas** — quando o próprio time não sabe ainda o que é "bom"
- **Quando o objetivo é precisão > 95%** — judge tem teto de calibração realista
- **Quando avaliado e judge são o mesmo modelo** — self-preference garantido

## Como funciona — anatomia mínima

```python
JUDGE_PROMPT = """
Você é avaliador rigoroso. Não é simpático, é objetivo.

Tarefa: {task_description}
Critério a avaliar: {criterion}
Escala: 1 (muito ruim) a 5 (excelente)

Definições de cada nível:
1 - {anchor_1}
2 - {anchor_2}
3 - {anchor_3}
4 - {anchor_4}
5 - {anchor_5}

Input do usuário: {input}
Resposta do modelo: {output}

Primeiro, raciocine sobre cada nível.
Depois, atribua o score final.

Output em JSON:
{{
  "reasoning": "<análise dimensão por dimensão>",
  "score": <1-5>,
  "issues": ["<problema 1>", "<problema 2>"]
}}
"""

def llm_judge(task, input_, output, criterion, anchors):
    response = client.messages.create(
        model="claude-opus-4-6",  # judge >= modelo avaliado
        max_tokens=600,
        messages=[{
            "role": "user",
            "content": JUDGE_PROMPT.format(
                task_description=task,
                criterion=criterion,
                anchor_1=anchors[1], anchor_2=anchors[2],
                anchor_3=anchors[3], anchor_4=anchors[4],
                anchor_5=anchors[5],
                input=input_,
                output=output,
            )
        }]
    )
    return parse_json(response.content[0].text)
```

Três decisões críticas aqui:

1. **Judge >= avaliado.** Judge fraco não distingue bom de excelente.
2. **CoT antes do score.** Pedir reasoning antes força calibração; pular vai direto pro chute. (Base do paper G-Eval.)
3. **Anchors no prompt do judge.** Sem isso, judge inventa a própria escala.

## Os 4 vieses canônicos

### 1. Position bias

Em comparação A vs B, judges tendem a preferir o que aparece **primeiro** (ou último, dependendo do modelo).

```
"Qual resposta é melhor?
A: <resposta X>
B: <resposta Y>"

→ judge marca A em ~57% mesmo quando X é objetivamente pior
```

Mitigação: **randomize ordem** em todo eval pairwise. Em N rodadas, A aparece 50% das vezes em cima.

### 2. Verbosity bias

Resposta mais longa tende a ser avaliada como melhor — mesmo quando é prolixa.

```
Resposta A (concisa, 50 palavras, correta)
Resposta B (verbosa, 300 palavras, mesma info diluída)

→ judge prefere B em ~62% dos casos
```

Mitigação:

- **Score conciseness explicitamente** na rubrica
- Normalizar comprimento antes de mostrar pro judge (truncar B ao tamanho de A)
- Penalty automática por comprimento desproporcional

### 3. Self-preference bias

GPT como judge prefere outputs gerados por GPT. Claude como judge prefere Claude. Isso foi documentado em múltiplos papers (G-Eval, Judging-LLM-as-Judge).

```
Modelos avaliados: GPT-5, Claude Opus 4
Judge: GPT-5
→ GPT-5 vence em ~58% dos pareamentos blind

Mesmo experimento, judge: Claude Opus 4
→ Claude vence em ~55%
```

Mitigações:

- **Cross-judge**: rode com 2 judges de famílias diferentes. Discordância sinaliza item ambíguo.
- Judge **diferente** do modelo em produção.
- Em produção, use **ensemble**: 2-3 judges, mediana do score.

### 4. Bandwagon / chain-of-thought leakage

Se você mostra o score do judge anterior, novo judge tende a concordar (bandwagon). Se você mostra reasoning de outro judge, vira anchor demais.

Mitigação: cada judge avalia **isolado**. Agregação acontece **depois**.

## Técnicas de mitigação

### CoT judging — G-Eval

Em vez de pedir score direto, peça reasoning estruturado:

```yaml
1. Identifique pontos fortes da resposta
2. Identifique pontos fracos
3. Aplique a rubrica dimensão por dimensão
4. SÓ ENTÃO atribua score
```

Por que funciona: judge sem CoT é prompt completion — vê output, devolve número. Judge com CoT é forçado a justificar. A justificativa expõe o que ele está medindo de fato.

Citação direta do paper G-Eval (Liu et al., 2023): *"forcing the model to generate a step-by-step evaluation rationale significantly improves correlation with human judgment."*

### Pairwise em vez de absoluto

Score absoluto: "essa resposta é 4 de 5?"
Pairwise: "A é melhor que B, B é melhor que A, ou empate?"

Por que pairwise é mais robusto:

- Humanos (e modelos) são melhores em comparar do que em pontuar absoluto
- Reduz central tendency bias (todo mundo tende a dar 3)
- Permite Elo rating (Chatbot Arena usa)
- Position bias mitiga com randomização

Quando pairwise não dá:

- Você tem só um output (não dois pra comparar)
- Custo computacional (N(N-1)/2 pares)

Solução híbrida: usa absoluto pra triagem ampla, pairwise pros top-K candidatos.

### Swap-judge consistency check

```
1. Pede judge pra avaliar A vs B → resultado R1
2. Inverte ordem: avalie B vs A → resultado R2
3. Se R1 == invert(R2): consistente
4. Se R1 != invert(R2): item ambíguo, descarta ou envia pra humano
```

Custo: 2x chamadas. Benefício: filtra ~5-15% de noise.

### Calibração com humano

Inegociável antes de confiar:

1. Sample de 30-50 itens
2. Humano (calibrado pela rubrica) atribui score
3. Judge atribui score nos mesmos itens
4. Correlação Pearson ou Spearman entre os dois
5. Se >0.7: judge calibrado, pode escalar
6. Se 0.5-0.7: judge usável mas com cautela
7. Se <0.5: judge não calibrado, refina prompt ou troca modelo

Calibração deve ser refeita:

- Ao trocar modelo do judge
- Ao mudar rubrica
- A cada 3-6 meses (drift de modelo, drift de tarefa)

## LMSYS Chatbot Arena — o caso de produção

[Chatbot Arena](https://chat.lmsys.org/) é o exemplo mais conhecido de eval pairwise em escala:

- Usuários blind comparam respostas de 2 modelos
- Voto: A melhor, B melhor, empate, ambas ruins
- Modelos rankeados por Elo, como xadrez

Por que funciona em escala:

- Pairwise > absoluto (humanos calibram comparando)
- Position bias mitigado por randomização de ordem
- Self-preference mitigado por blind (usuário não sabe qual modelo é qual)
- Volume → Elo converge (50k+ votos por modelo top)

A metodologia do Arena é a base de quase todo eval pairwise sério em 2026 — vale ler o paper *"Chatbot Arena: An Open Platform for Evaluating LLMs by Human Preference"* (Chiang et al., 2024).

## Custo realista

Judge geralmente é modelo forte (Opus 4, GPT-5, Gemini 2.5 Pro):

```
1 eval com Opus 4.6 como judge:
  ~500 tokens input + ~400 tokens output = ~$0.012 por item

Golden set de 100 itens, 4 critérios cada:
  100 × 4 × $0.012 = ~$5 por rodada completa

Com CoT judging (mais tokens output):
  ~$8-12 por rodada
```

Em PR: rodar subset (top-20 críticos) = ~$1.5/PR. Em main merge: full = ~$10.

Comparação com humano:

```
Anotador humano treinado: ~30s-2min por item
Custo equivalente: $5-15/h × 1-3min = $0.10-0.75/item
Custo de eval 100 itens: $10-75 + 50min-3h de wall-clock
```

Judge é ~10x mais barato e 50x mais rápido. Por isso vale escalar — **depois de calibrado**.

## Anti-patterns

- **Judge não-calibrado em produção** — número sem âncora, só ruído com aparência de rigor
- **Judge = avaliado** — auto-aprovação garantida
- **Sem CoT no prompt do judge** — chute disfarçado de score
- **Sem randomização em pairwise** — position bias inflando 7-10%
- **Eval só absoluto, nunca pairwise** — perde sinal em comparação A/B de prompts
- **Ignora outliers do judge** — quando judge diverge muito do humano, item ambíguo é informação
- **Re-roll até score subir** — circular, viola toda a noção de eval

## Armadilhas comuns

> [!warning] Judge não calibrado sendo tratado como fonte de verdade
> O erro mais custoso é rodar LLM-as-judge, ver scores bonitos, e tomar decisões de produto sem jamais ter comparado esses scores com julgamento humano. O judge vai ter calibração intrínseca — mas pode ser sistematicamente enviesada pro seu domínio específico. Texto técnico médico avaliado por um judge treinado em texto genérico vai inflar scores onde a precisão factual importa. A regra é inegociável: antes de promover judge a tomador de decisão, calcule correlação com 30-50 itens anotados por humano. Correlação abaixo de 0.7 significa que o judge está medindo outra coisa do que você pensa.

> [!warning] Self-preference quando avaliado e judge são o mesmo modelo
> Usar GPT-5 pra avaliar outputs do GPT-5, ou Claude pra avaliar Claude, cria um sistema que aprova a si mesmo. A literatura (Zheng et al., 2023) documenta isso: modelos preferem respostas geradas na própria família em 55-58% dos casos em avaliação blind — bem acima dos 50% esperados por acaso. Em produção, isso se traduz em: seu pipeline parece ótimo no eval, mas é porque o judge é condescendente com o modelo que conhece. Sempre use judge de família diferente do modelo em produção. Se precisar do mesmo modelo, use pelo menos versão diferente ou cross-judge com dois modelos opostos.

> [!warning] Pairwise sem randomização de ordem — position bias inflando silenciosamente
> Em avaliação A vs B, se A aparece sempre no topo e B embaixo, o judge vai preferir A em ~57% dos casos independente do conteúdo — isso é position bias documentado. A armadilha é não perceber o viés porque o sistema parece funcionar (judge dá scores, decisões são tomadas). O erro só fica visível quando você inverte A e B e os resultados mudam. A mitigação é simples mas precisa ser implementada conscientemente: randomize a ordem de apresentação em cada avaliação pairwise. Se você está acumulando scores sem randomização, os números históricos estão enviesados.

## Como explicar em inglês

Em entrevistas sobre avaliação de sistemas LLM, LLM-as-judge aparece como a solução de escala — e a resposta que demonstra experiência real inclui os vieses e as mitigações, não só o happy path:

> "LLM-as-judge solves the scaling problem in subjective eval: you can't have a human review a thousand outputs per iteration, but you can run a model. The catch is systematic biases — position bias in pairwise comparisons, verbosity bias where longer responses score higher, and self-preference where a model judges its own outputs more favorably. Mitigations are: chain-of-thought prompting before the score, pairwise over absolute scoring, randomizing order, and — non-negotiable — calibrating against human judgment before trusting the numbers. A judge that correlates below 0.7 with humans is just producing noise with the appearance of rigor."

| Português | Inglês |
|-----------|--------|
| juiz LLM | LLM judge / LLM-as-judge |
| viés posicional | position bias |
| viés de verbosidade | verbosity bias |
| auto-preferência | self-preference bias |
| avaliação pairwise | pairwise evaluation |
| julgamento em cadeia de pensamento | chain-of-thought judging |
| randomização de ordem | position randomization |
| calibração com humano | human calibration |
| correlação com julgamento humano | correlation with human judgment |
| check de consistência por inversão | swap-judge consistency check |

## O que vem a seguir

Com LLM-as-judge cobrindo a escala de avaliação, a nota 05 entra no uso contínuo desses evals: regression testing. Como garantir que cada mudança no prompt ou no modelo não quebra o que já estava funcionando — e como montar um pipeline que pega regressões antes de chegarem à produção.

Ver [[05 - Regression testing em LLMs]].

## Veja também

- [[03 - Scoring rubrics e critérios]] — judge precisa de rubrica com anchors
- [[02 - Golden datasets — como construir]] — dataset onde judge roda
- [[05 - Regression testing em LLMs]] — judge como sinal de regressão
- [[Dicionário de IA#LLM-as-judge|LLM-as-judge (verbete)]]
- [[03-Dominios/Tecnologia/IA/Anatomia dos LLMs/19 - Evaluation de LLMs em produção]] — pilar 2 contextualizado
- [[03-Dominios/Tecnologia/IA/RAG e Vector Databases/09 - Evaluation de RAG]] — Ragas usa LLM-as-judge internamente

## Fontes

- **Liu et al.** — *G-Eval: NLG Evaluation using GPT-4 with Better Human Alignment* ([arxiv:2303.16634](https://arxiv.org/abs/2303.16634), 2023)
- **Zheng et al.** — *Judging LLM-as-a-Judge with MT-Bench and Chatbot Arena* ([arxiv:2306.05685](https://arxiv.org/abs/2306.05685), 2023) — origem da catalogação de vieses
- **Chiang et al.** — *Chatbot Arena: An Open Platform for Evaluating LLMs by Human Preference* (LMSYS, 2024)
- **Anthropic** — [*Eval cookbook — LLM-as-judge*](https://github.com/anthropics/anthropic-cookbook/tree/main/misc/evals)
- **OpenAI** — [*Evals — model-graded evals*](https://github.com/openai/evals/blob/main/docs/eval-templates.md)
- **Eugene Yan** — [*LLM-as-judge patterns*](https://eugeneyan.com/writing/llm-evaluators/) (2024)
