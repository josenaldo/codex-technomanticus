---
title: "03 - Scoring rubrics e critérios"
created: 2026-05-28
updated: 2026-07-01
type: concept
status: seedling
progress: in_progress
fase: iniciado
tags:
  - evaluation
  - ia
  - rubrica
  - scoring
publish: true
aliases:
  - Rubric
  - Scoring rubric
  - Inter-rater agreement
---

# 03 - Scoring rubrics e critérios

> [!abstract] TL;DR
> **Rubrica é o dicionário operacional** que transforma "esse output é bom?" numa pergunta com resposta reproduzível — ela define o que "bom" significa em termos operacionais, antes de qualquer ferramenta ou anotador entrar em cena. Sem rubrica, cada avaliador (humano ou LLM-judge) inventa sua própria régua; com rubrica, a régua é compartilhada e testável.
>
> Uma boa rubrica separa **critérios objetivos** (formato válido, campos obrigatórios presentes, latência — binário ou contagem automática) de **critérios subjetivos** (acurácia, helpfulness, tom — escala 1-5 Likert com **anchored examples**). Anchors são o detalhe que faz funcionar: cada nível da escala tem 1-2 outputs de referência. Sem anchors, *"score 4"* significa coisas diferentes pra cada anotador e o sinal vira ruído.
>
> O trade-off central é custo vs. fidelidade: critérios objetivos são baratos e automatizáveis, mas captam só o que é binário; critérios subjetivos captam nuances, mas exigem calibração. **Inter-rater agreement** (Cohen's kappa ou % de concordância) é o teste de sanidade da rubrica — se dois anotadores treinados discordam em >20% dos casos, o problema é a rubrica, não os anotadores. Kappa > 0.6 é o piso para confiar nos scores.

> [!question]- O que eu preciso saber antes de ler isso?
> Você entende que EDD requer medição sistemática (nota 01) e que o golden set é o conjunto de casos que serve de régua (nota 02). Esta nota cobre a régua em si: como você define numericamente o que "bom" significa. Não é necessário background em psicometria ou pesquisa quantitativa — mas se você conhece NPS, A/B test ou CSAT, vai reconhecer os padrões. A rubrica é o que transforma julgamento humano em número reproduzível.

## A função da rubrica

Rubrica resolve um problema linguístico antes de qualquer ferramenta:

```
Sem rubrica: "essa resposta é boa?"
Com rubrica: "essa resposta atende ao critério X de acordo com escala Y?"
```

A primeira pergunta é subjetiva e não-reproduzível. A segunda é operacionalizável — mesmo que ainda envolva julgamento, o julgamento agora tem **âncoras**.

## Critérios objetivos vs subjetivos

| Tipo | Exemplos | Como medir |
|---|---|---|
| **Objetivo** | Output é JSON válido? Contém campo `email`? Latência <2s? | Binário (pass/fail) ou contagem |
| **Objetivo agregado** | % de citações que apontam pra fonte real | Razão (precision/recall) |
| **Semi-objetivo** | Resposta usou apenas os chunks fornecidos? | Verificável com regex / LLM-as-judge |
| **Subjetivo** | Tom adequado? Útil pro usuário? Acurada? | Escala 1-5 com anchored examples |
| **Subjetivo composto** | Qualidade geral | Média ponderada de subjetivos |

Boa prática: **sempre comece pelos objetivos**. Eles são baratos, automatizáveis e captam ~70% dos problemas reais. Só vá pros subjetivos quando os objetivos já estão sob controle.

## Estrutura mínima de rubrica

Adaptado do template @hooeem (cap. #14 + #18):

```yaml
rubric:
  # Objetivos (pass/fail)
  format_valid:
    type: binary
    description: "Output é JSON parseável com schema válido"
    weight: critical  # falha aqui zera o resto

  required_fields_present:
    type: binary
    description: "Campos answer, confidence, sources estão presentes"
    weight: critical

  # Subjetivos (1-5)
  accuracy:
    type: likert_5
    description: "Resposta é factualmente correta?"
    weight: 1.0

  completeness:
    type: likert_5
    description: "Resposta cobre o que a pergunta pediu?"
    weight: 1.0

  source_quality:
    type: likert_5
    description: "Citações são reais, relevantes, recentes?"
    weight: 0.8

  tone:
    type: likert_5
    description: "Tom adequado pro contexto (profissional, neutro)?"
    weight: 0.5

  # Aprovação
  pass_threshold:
    avg_min: 4.0
    no_dim_below: 3
    critical_must_pass: true

  # Falhas automáticas (zeram tudo)
  automatic_failure:
    - "Vazamento de PII"
    - "Recusou tarefa legítima"
    - "Inventou citação"
```

Note três coisas:

1. **Critical fields** zeram tudo se falham. Não importa se o resto é 5/5.
2. **Weights** permitem priorizar critérios sem inflar com dimensões desbalanceadas.
3. **Automatic failure** é o link com [[Segurança e Guardrails]] — guardrails são automatic failures da rubrica.

## Escalas — quando usar cada uma

### Binária (pass/fail)

Use quando:
- Critério é objetivo verificável
- Não há gradação útil ("JSON válido" não tem "meio válido")
- Você precisa de velocidade e baixo custo de anotação

Limite: força decisões dicotômicas mesmo onde há sombra.

### Likert 1-5

Use quando:
- Critério é subjetivo com gradações naturais
- Você tem anchored examples por nível
- Vai agregar com média/mediana

Limite: pessoas tendem a evitar extremos (central tendency bias). Médias inflam pro 3.

### Likert 1-7 ou 1-10

Use quando:
- Precisa de granularidade fina (research)
- Tem mais de 3 anotadores e quer reduzir empate

Limite: anotador raramente distingue 7 de 8. Granularidade real é menor que a escala sugere.

### Pairwise (A vs B)

Use quando:
- Comparando duas versões (v1 vs v2 do prompt)
- Escala absoluta seria difícil de calibrar
- Você consegue judging A/B/empate

Vantagem: humanos são muito melhores em comparar do que em pontuar em escala absoluta. **Chatbot Arena (LMSYS)** é construído sobre isso.

### Multi-dimensional vs nota única

```yaml
# Multi-dimensional (recomendado)
output:
  accuracy: 4
  completeness: 5
  tone: 3
  format: 5

# Nota única (perde sinal)
output:
  quality: 4
```

Multi-dim permite identificar **onde** o output falha. Nota única só diz "falhou", não "por quê".

## Anchored scales — o detalhe que faz funcionar

Likert 1-5 sem anchors:

```
1 = muito ruim
2 = ruim
3 = ok
4 = bom
5 = excelente
```

Resultado: dois anotadores treinados discordam em 30%+ dos casos.

Likert 1-5 com anchors (exemplo real de rubrica de **completeness** em answer):

```yaml
completeness:
  description: "A resposta cobre o que a pergunta pediu?"

  anchors:
    5:
      definition: "Cobre todos os pontos da pergunta + contexto útil. Nada falta."
      example_input: "Como configuro auth OAuth no FastAPI?"
      example_output: "[resposta com 4 passos completos, exemplo de código,
                       link pra doc oficial, menção a edge case de refresh token]"

    4:
      definition: "Cobre o essencial da pergunta. Falta detalhe não-crítico."
      example_input: "Como configuro auth OAuth no FastAPI?"
      example_output: "[resposta com 4 passos, exemplo de código, sem link
                       pra doc, sem menção a refresh token]"

    3:
      definition: "Cobre o ponto principal. Falta um sub-ponto importante."
      example_input: "Como configuro auth OAuth no FastAPI?"
      example_output: "[resposta com 3 passos, sem exemplo de código]"

    2:
      definition: "Aborda o tema mas deixa o usuário sem caminho de ação."
      example_input: "Como configuro auth OAuth no FastAPI?"
      example_output: "FastAPI tem suporte a OAuth via Depends. Veja a doc."

    1:
      definition: "Não responde a pergunta ou responde a outra coisa."
      example_input: "Como configuro auth OAuth no FastAPI?"
      example_output: "FastAPI é um framework web em Python."
```

A diferença prática:

| | Sem anchor | Com anchor |
|---|---|---|
| Inter-rater agreement | ~60% | ~85%+ |
| Reprodutibilidade cross-tempo | Baixa | Alta |
| LLM-as-judge calibrável | Difícil | Direto ([[04 - LLM-as-judge — quando e como]]) |

Anchored rubric custa 1-2h de trabalho upfront. Paga em todas as evals subsequentes.

## Inter-rater agreement — testando a rubrica

A rubrica é boa se dois humanos treinados, vendo o mesmo output, concordam. Como medir:

### % agreement simples

```
Anotador A:  [4, 5, 3, 2, 4, 5]
Anotador B:  [4, 4, 3, 2, 5, 5]

Match exato: 4/6 = 67%
Match ±1: 6/6 = 100%
```

Bom pra estimativa rápida. Limite: não corrige por concordância ao acaso.

### Cohen's kappa

```
κ = (P_observed - P_chance) / (1 - P_chance)

P_observed = % de concordância observada
P_chance = % esperada por acaso (depende de distribuição)
```

Interpretação:

| Kappa | Concordância |
|---|---|
| <0.20 | Pobre — rubrica não funciona |
| 0.21-0.40 | Razoável |
| 0.41-0.60 | Moderada — usável com cautela |
| 0.61-0.80 | Boa — rubrica calibrada |
| 0.81-1.00 | Excelente — possivelmente trivial |

Meta prática: kappa > 0.6 entre 2 anotadores treinados.

### Quando aplicar

1. Após escrever rubrica v1
2. Dois anotadores rodam em 20-30 itens
3. Mede kappa
4. Se < 0.6: refina anchors, revisa definição, repete
5. Quando ≥ 0.6: rubrica está pronta pra produção (humano ou judge)

Pular esse passo = rubrica vaga vira ruído permanente em todos os scores.

## Calibração com judge

Quando você quer usar [[04 - LLM-as-judge — quando e como|LLM-as-judge]] pra escalar:

1. 30-50 itens anotados por humano (gold)
2. Mesmo subset rodado pelo judge
3. Calcula correlação (Pearson, Spearman) ou kappa entre humano e judge
4. Se correlação > 0.7: judge calibrado, pode escalar
5. Se < 0.7: refina prompt do judge ou refina rubrica

Sem calibração com humano, judge é só mais um modelo opinando — não é eval.

## Anti-patterns

- **Escala sem anchors** — *"score 4"* significa coisa diferente pra cada um
- **Muitas dimensões** — 12 critérios não se distinguem; vira ruído. 4-7 é teto prático.
- **Pesos invisíveis** — média simples esconde que `tone` está pesando igual a `accuracy`
- **Critério vago** — *"resposta de qualidade"* não é critério, é eufemismo
- **Sem critical fields** — output sem campo obrigatório que pontua 4/5 nas outras dimensões
- **Sem inter-rater check** — rubrica nunca foi testada com 2 humanos
- **Judge não calibrado** — rodando judge automatizado sem nunca ter comparado com humano

## Armadilhas comuns

> [!warning] Rubrica com critérios vagos — "qualidade" como dimensão
> A armadilha mais comum é criar dimensões que parecem concretas mas são vazias: "qualidade da resposta", "adequação", "clareza". Sem anchors que mostrem o que é score 1, 3 e 5, cada anotador — humano ou LLM-judge — vai interpretar esses termos de forma diferente. O sintoma é inter-rater agreement baixo (dois anotadores discordam em >30% dos casos). O diagnóstico: não é que os anotadores são ruins, é que a rubrica não operacionalizou o critério. Reescreva os critérios como perguntas binárias ou ancore cada nível com um exemplo.

> [!warning] Misturar critérios objetivos e subjetivos na mesma escala
> Critérios objetivos são binários: o JSON é válido ou não, o campo existe ou não. Critérios subjetivos são graduados: o tom é adequado numa escala 1-5. Misturar os dois na mesma escala cria confusão — "score 3" em "JSON válido" não faz sentido. A boa prática é tratar objetivos como checklist separado: falha em critério objetivo = automatic failure (não importa score nas outras dimensões). Subjetivos vão na escala. Se um output falhou no JSON, não precisa pedir pra humano avaliar o tom.

> [!warning] Rubrica sem testes de inter-rater antes de automatizar com judge
> Antes de usar LLM-as-judge com a rubrica, teste com dois humanos em pelo menos 20-30 casos e calcule o agreement. Se agreement está abaixo de 80%, o problema não vai melhorar com LLM — vai piorar, porque o judge vai sistematizar a ambiguidade. Judge é acelerador de anotação humana, não substituto de rubrica bem definida. Judge calibrado assume rubrica clara; judge com rubrica vaga produz scores sem sentido.

## Como explicar em inglês

Em entrevistas sobre sistemas de IA ou ML, perguntas sobre "como você avalia qualidade de output?" são comuns — e a resposta que demonstra experiência de produção menciona rubrica, anchors e inter-rater agreement:

> "A scoring rubric is the operational dictionary that turns 'is this output good?' into a reproducible measurement. Good rubrics separate objective criteria — binary checks like JSON validity or field presence — from subjective ones scored on a 1-5 Likert scale with anchored examples at each level. Inter-rater agreement is the quality test: if two trained annotators disagree on more than 20% of cases, the rubric is too vague, not the annotators. Once the rubric is calibrated with humans, you can scale it with LLM-as-judge."

| Português | Inglês |
|-----------|--------|
| rubrica de avaliação | scoring rubric / evaluation rubric |
| critério ancorado | anchored criterion |
| escala Likert | Likert scale |
| inter-rater agreement | inter-rater agreement |
| coeficiente kappa de Cohen | Cohen's kappa |
| falha automática | automatic failure |
| campo obrigatório | critical field |
| anotador | annotator |
| prompt de judge | judge prompt |
| calibração de judge | judge calibration |

## O que vem a seguir

Com dataset e rubrica definidos, a nota 04 entra no mecanismo que permite escalar a anotação: LLM-as-judge. Como configurar um LLM para usar sua rubrica de forma confiável, quando isso funciona, e quando você ainda precisa de humano.

Ver [[04 - LLM-as-judge — quando e como]].

## Veja também

- [[02 - Golden datasets — como construir]] — dataset + rubrica andam juntos
- [[04 - LLM-as-judge — quando e como]] — escalar a rubrica
- [[05 - Regression testing em LLMs]] — rubrica como threshold de regressão
- [[03-Dominios/Tecnologia/IA/AI Engineering Stack/09 - Evaluation Layer]] — template de rubrica @hooeem
- [[Segurança e Guardrails]] — automatic failure conditions = guardrails

## Fontes

- **@hooeem** — *Become an AI Engineer*, caps. #14 (rubrica) e #18 (Evaluation layer)
- **Cohen, J.** — *A coefficient of agreement for nominal scales* (1960) — origem do kappa
- **OpenAI** — [*Evals cookbook*](https://github.com/openai/evals) — exemplos de rubrica multi-dim
- **Anthropic** — [*Eval cookbook*](https://github.com/anthropics/anthropic-cookbook/tree/main/misc/evals) — rubric design patterns
- **Liu et al.** — *G-Eval* ([arxiv:2303.16634](https://arxiv.org/abs/2303.16634)) — rubrica formal pra judge
- **Eugene Yan** — [*Evals are all you need*](https://eugeneyan.com/writing/evals/)
