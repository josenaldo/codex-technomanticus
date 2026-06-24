---
title: "Evaluation Layer"
created: 2026-05-28
updated: 2026-06-24
type: concept
status: seedling
fase: Iniciado
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
> A Evaluation Layer responde **como saber se o output está bom** — de forma reproduzível, não por intuição. É uma rubrica de múltiplas dimensões (acurácia, completude, utilidade, aderência ao formato, qualidade da fonte) aplicada a um dataset curado. Sem evals, "ficou melhor" vira sentimento; com evals, vira número comparável. A regra que separa sistemas maduros de demos: o sistema que itera com sinal melhora. O que itera no escuro não sabe se está melhorando ou piorando.

## O problema que a Evaluation Layer resolve

Você mudou o system prompt. O modelo parece responder melhor. Você mostra para dois colegas — um acha que melhorou, o outro acha que piorou. Como você decide?

Sem a Evaluation Layer, a resposta é: por intuição, por votação, ou pela opinião do stakeholder mais vocal na reunião. Isso funciona para um protótipo com 10 casos de uso testados manualmente. Não funciona para um sistema em produção com 10.000 chamadas por dia e 200 tipos de input diferentes.

A Evaluation Layer cria o **sinal** que permite iterar com objetividade. Sem ela, você não sabe se uma mudança de modelo, prompt ou retrieval melhorou ou piorou a qualidade do sistema. Com ela, você tem um número: a mudança moveu o score de 3.2 para 3.7 nas métricas que importam para o negócio, e não regrediu em nenhuma das condições de falha automática.

## O que é esta camada

A Evaluation Layer é a **régua** do sistema — mede qualidade do output de forma reproduzível para que mudanças possam ser comparadas com objetividade.

Template mínimo (adaptado do thread @hooeem):

```yaml
evaluation:
  success_criteria: "<herda do Purpose Layer — traduzido em dimensões mensuráveis>"
  scoring_rubric:
    accuracy: "1-5: alinhamento factual com fontes verificáveis"
    completeness: "1-5: todas as partes da pergunta foram respondidas"
    usefulness: "1-5: o output é acionável para o usuário-alvo"
    format_adherence: "1-5: segue o contrato definido na Output Layer"
    source_quality: "1-5: fontes citadas são adequadas e verificáveis"
    specificity: "1-5: resposta concreta, não genérica"
    risk_control: "1-5: sem conteúdo proibido ou potencialmente prejudicial"
  pass_threshold: "média ≥4 E nenhuma dimensão <3"
  automatic_failure_conditions:
    - "vazamento de PII"
    - "chamada de tool proibida pela Guardrail Layer"
    - "formato de output inválido (breaking change no schema)"
```

Três tipos de eval se complementam: **(a) reference-based** — compara com ground truth (bom para Q&A com resposta conhecida); **(b) reference-free** — checa propriedades intrínsecas do output (bom para verificar formato, tom, ausência de PII); **(c) LLM-as-judge** — outro modelo aplica a rubrica (bom para dimensões qualitativas em escala).

## Decisões-chave

**1. Dataset de eval é o fundamento.** Sem dataset, não há eval — só impressão. Comece com 20-50 exemplos curados manualmente, cobrindo casos fáceis, médios, difíceis, edge cases e regressões conhecidas (casos que já falharam em produção). O dataset cresce com cada incidente real: todo output problemático reportado em produção vira um caso no dataset de regressão.

**2. Rubrica com definições operacionais.** "Acurácia: 4" tem que significar a mesma coisa quando dois avaliadores diferentes aplicam a rubrica. Definições vagas degeneram para "achismo escala 1-5". Cada ponto da escala precisa de um descritor específico: "4 = informação correta com uma imprecisão menor que não afeta a conclusão".

**3. LLM-as-judge exige calibração.** Usar outro LLM para aplicar a rubrica é poderoso para escalar evals além do que revisão humana consegue cobrir — mas exige calibração contra humano em uma amostra representativa. Sem calibração, você tem dois modelos concordando entre si, não dois avaliadores chegando ao mesmo critério.

**4. Automatic failure conditions como ponte com Guardrail.** Condições que zeram a nota total — PII exposto, tool proibida chamada, schema quebrado — são o link formal entre Evaluation Layer e Guardrail Layer. Uma `automatic_failure_condition` na Evaluation é um guardrail de qualidade; se acontece com frequência, vira um guardrail de prevenção.

**5. Frequência: CI/CD de evals.** Eval que roda só "no final do projeto" não dá sinal útil. O padrão de maturidade: regression eval em cada PR (30-50 casos rápidos para checar que nada regrediu) + full eval semanalmente + live eval amostral em produção (amostragem de 1-5% dos outputs reais para monitoramento contínuo).

## Casos práticos

### Cenário 1 — O sistema que "melhorou" mas não melhorou

Time atualiza o system prompt de um assistente de redação. Avaliação manual por dois membros: ambos acham melhor. Lançam em produção. Duas semanas depois, a métrica de "usuário editou a resposta antes de usar" subiu de 40% para 65% — o sistema piorou para os usuários.

O problema: avaliação manual por dois revisores é uma amostra de tamanho 2 em 10.000 outputs. Os dois casos que avaliaram eram fáceis; os casos difíceis — onde o sistema regrediu — não foram testados.

Com a Evaluation Layer: dataset de regressão com 80 casos (incluindo os casos difíceis históricos), rubrica com dimensão "especificidade" (que a mudança de prompt degradou), regression eval no PR. A mudança teria sido bloqueada antes do lançamento.

### Cenário 2 — LLM-as-judge em escala

Sistema de suporte técnico que recebe 5.000 tickets por dia. Revisão humana de 1% = 50 casos/dia — suficiente para calibração, insuficiente para detectar degradação estatística.

Solução: rubrica definida pela equipe, calibrada contra 200 casos com avaliação humana (acordo inter-avaliador ≥80%). LLM-as-judge aplica a rubrica em 100% dos tickets (500 por hora, custo marginal baixo). Dashboard mostra scores por dimensão, por tipo de ticket, por horário. Alertas disparam quando qualquer dimensão cai >10% vs semana anterior.

A calibração é o que valida o judge. Sem ela, o dashboard seria um número que ninguém confia.

## Armadilhas comuns

> [!warning] Lançar sem dataset de eval
> "Vamos criar o dataset depois de ver os primeiros dados reais" é a armadilha mais comum. Sem dataset, você não tem baseline para comparar; sem baseline, você não sabe se os dados reais representam melhora ou degradação. O dataset mínimo viável — 20-50 casos curados à mão — deve existir antes do primeiro lançamento em ambiente compartilhado.

> [!warning] Rubrica sem definições operacionais
> "Utilidade: 1-5" sem descritor por ponto é "opinião: 1-5". Dois revisores vão dar notas diferentes para o mesmo output porque "utilidade" significa coisas diferentes para eles. O esforço de escrever os descritores antes de avaliar os primeiros casos é o que transforma a rubrica em métrica comparável.

> [!warning] LLM-as-judge sem calibração
> Usar GPT-4 para avaliar outputs de Claude (ou vice-versa) sem calibração contra avaliação humana é transferir o viés do judge para a métrica. Modelos têm viés em direção ao seu próprio estilo de output. Calibre o judge contra humano antes de confiar no número que ele produz.

## Como explicar em inglês

The Evaluation Layer is the measurement system of the AI stack. It defines how to determine whether the system's output is good — through a scoring rubric applied to a curated dataset, not through intuition or manual spot-checks. The key insight: teams that iterate with evaluation scores improve predictably; teams that iterate by gut feel don't know whether they're improving or degrading. The three types of eval — reference-based, reference-free, and LLM-as-judge — complement each other. LLM-as-judge scales quality assessment beyond what human review can cover, but only after calibration against human judgment.

| PT | EN |
|----|----|
| Camada de avaliação | Evaluation Layer |
| Rubrica de avaliação | Scoring rubric |
| Conjunto de dados de avaliação | Evaluation dataset |
| LLM como juiz | LLM-as-judge |
| Avaliação de referência | Reference-based evaluation |
| Avaliação sem referência | Reference-free evaluation |
| Avaliação de regressão | Regression evaluation |
| Condição de falha automática | Automatic failure condition |
| Limiar de aprovação | Pass threshold |
| Acordo inter-avaliador | Inter-rater agreement |

## O que vem a seguir

A Evaluation Layer mede qualidade — mas medir não previne. Para o sistema parar ativamente antes de produzir output prejudicial, a próxima camada é a **Guardrail Layer**: checks determinísticos que interceptam input, output e tool calls por código, independentemente do que o modelo decidiu gerar.

Depois de Evaluation e Guardrail, a Logging Layer fecha o bloco de controle: registra tudo que passou pelas duas para que o Improvement Loop tenha dados para trabalhar.

- [[10 - Guardrail Layer]] — o que o sistema não pode fazer (imposição por código)
- [[Evaluation]] — trilha completa: datasets, LLM-as-judge, métricas por tipo de sistema

## Onde aprofundar

- **[[Evaluation]]** — trilha completa dedicada (8 notas).
- **[[Anatomia de Agents]]** → [[09 - Evaluation de agents]] — particularidades quando o sistema é agentic.
- **[[RAG e Vector Databases]]** → [[09 - Evaluation de RAG]] — recall, precision@k, faithfulness.

## Veja também

- [[02 - Purpose Layer — o que o sistema é]] — `success_criteria` descem daqui
- [[05 - Output Layer]] — a rubrica aplica sobre o que sai do modelo
- [[10 - Guardrail Layer]] — `automatic_failure_conditions` são guardrails de qualidade
- [[11 - Logging Layer]] — scores de eval entram nos logs para análise

## Fontes

- **@hooeem** — *Become an AI Engineer*, chapter #18, Step 8 (Evaluation layer template). X/Twitter, 2025.
- **Eugene Yan** — [*Evals are all you need*](https://eugeneyan.com/writing/evals/). Argumento por evals como vantagem competitiva sustentável.
- **Hamel Husain** — [*Your AI product needs evals*](https://hamel.dev/blog/posts/evals/). Guia prático de como começar com dataset mínimo.
