---
title: "03 - Scoring rubrics e critérios"
created: 2026-05-28
updated: 2026-05-28
type: concept
status: seedling
progress: in_progress
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
> Rubrica é o **dicionário operacional** que transforma "esse output é bom?" numa pergunta com resposta reproduzível. Boa rubrica separa critérios **objetivos** (formato, presença de campos, latência — binário ou contagem) de **subjetivos** (acurácia, helpfulness, tom — escala). Escala mais usada é 1-5 Likert com **anchored examples** — cada nível tem 1-2 outputs de referência. Sem anchors, *"score 4"* significa coisas diferentes pra cada anotador. Inter-rater agreement (Cohen's kappa ou simples % agreement) é o teste de qualidade da rubrica: se dois anotadores treinados discordam em >20% dos casos, a rubrica está vaga.

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

## Veja também

- [[02 - Golden datasets — como construir]] — dataset + rubrica andam juntos
- [[04 - LLM-as-judge — quando e como]] — escalar a rubrica
- [[05 - Regression testing em LLMs]] — rubrica como threshold de regressão
- [[AI Engineering Stack/09 - Evaluation Layer]] — template de rubrica @hooeem
- [[Segurança e Guardrails]] — automatic failure conditions = guardrails

## Fontes

- **@hooeem** — *Become an AI Engineer*, caps. #14 (rubrica) e #18 (Evaluation layer)
- **Cohen, J.** — *A coefficient of agreement for nominal scales* (1960) — origem do kappa
- **OpenAI** — [*Evals cookbook*](https://github.com/openai/evals) — exemplos de rubrica multi-dim
- **Anthropic** — [*Eval cookbook*](https://github.com/anthropics/anthropic-cookbook/tree/main/misc/evals) — rubric design patterns
- **Liu et al.** — *G-Eval* ([arxiv:2303.16634](https://arxiv.org/abs/2303.16634)) — rubrica formal pra judge
- **Eugene Yan** — [*Evals are all you need*](https://eugeneyan.com/writing/evals/)
