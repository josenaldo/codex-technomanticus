---
title: "Roadmap — Evaluation"
created: 2026-07-01
type: meta
publish: false
tags:
  - meta
  - roadmap
---

# Roadmap — Evaluation

Diagnóstico migrado de guia/roadmap - ia.md (30/06). Cada entrada tem estado de enriquecimento, score, classificação de custo e plano de execução acionável.

**Galho:** `03-Dominios/Tecnologia/IA/Evaluation`
**Diagnóstico:** 2026-06-28 (migrado 2026-07-01)
**Última execução:** 2026-07-01 — onda substantiva (01 EDD + 02 Golden datasets) + mecânica (04 LLM-as-judge). Galho 8/8 fechado.

## Régua de análise

Checklist `verificar-nota` — 12 itens (isenções por fase/tipo/broto aplicadas por nota):

| Grupo | Itens |
|-------|-------|
| ESTRUTURA | E1 TL;DR · E2 Abertura-problema · E3 Mermaid · E4 Casos práticos · E5 O que vem a seguir · E6 Inglês · E7 Tabela PT↔EN · E8 Armadilhas [!warning] |
| PROFUNDIDADE | P1 Código-com-falha · P2 Mecanismo explicado · P4 Exemplo com número |
| LINKS | L1 Wikilink cross-galho · L2 Referência externa (URL) |
| MÍDIA | M1 Vídeo/podcast embutido |

**Esquema de `fase:` detectado:** COM fase (Iniciado)
**Piso de linhas:** aplicável — Iniciado ≥300 · Adepto ≥400 · Magus ≥500 (decisão do usuário, 2026-08-01)

## Tabela-resumo

| Métrica | Valor |
|---------|-------|
| Total de notas | 9 |
| ⬜ pendente | 0 |
| ➖ não precisa | 4 |
| ✅ feita | 5 |
| 🔄 em andamento | 0 |
| % concluído | 100% |

> [!note] Nota 09 acrescentada em 2026-08-16
> Galho estava 8/8 fechado desde 01/07. A nota **09 - Abstenção** entrou depois, a partir da comparação com o board *IA do Zero ao Sênior* ([[2026-ia-do-zero-ao-senior-trilha-visual]]), que expôs a lacuna: as notas 01 e 02 mandam incluir anti-tests no golden set, mas nada no vault explicava por que o modelo não se abstém sozinho nem como implementar o comportamento. Nasce escrita, ainda não enriquecida.

---

## Notas

#### 01 - Eval-driven development — a disciplina   [substantivo]
- **Enriquecimento:** ✅ feita (2026-07-01)
- **Estado:** 357 linhas totais / 250 não-brancas · fase: Iniciado · status: growing
- **Núcleo/gaps:** E3, P1
- **Score:** 10/12
- **Plano de execução:**
  - Adicionar diagrama Mermaid do fluxo EDD (antes→depois, ou ciclo eval/prompt/baseline) → resolve E3 e adensa a nota visualmente
  - Expandir 2-3 seções existentes (ex: "Maturidade EDD" com exemplos concretos por nível, ou "EDD em times" com mini-caso) para cruzar o piso de ~300 linhas de conteúdo não-branco
  - Expandir TL;DR para ≥3 linhas explícitas no callout (atualmente 1 linha muito longa) → resolve E1
- **Resultado:** Diagrama Mermaid do ciclo EDD (rubrica→golden→baseline→mudar→eval→deploy, com bug-de-prod realimentando o dataset) resolve E3. TL;DR expandido de 1 p/ 4 linhas (E1). Adensamento substantivo: 5 níveis de maturidade descritos "na prática" (0→5) + mini-caso trabalhado (fintech, pipeline de extração, 3 engenheiros). 302→357 linhas, cruza o piso. `updated:`/`status: growing`. (onda enriquecer-galho, 01/07)

#### 02 - Golden datasets — como construir   [substantivo]
- **Enriquecimento:** ✅ feita (2026-07-01)
- **Estado:** 316 linhas totais / 231 não-brancas · fase: Iniciado · status: growing
- **Núcleo/gaps:** E1, E2, E3, P1
- **Score:** 8/12
- **Plano de execução:**
  - Expandir TL;DR para ≥3 linhas explícitas no callout (atualmente 1 linha muito longa) → resolve E1
  - Adicionar parágrafo de abertura-problema antes de "## O que é um golden set": descrever a dor concreta ("o prompt melhorou… ou será que piorou?") que motiva o golden set → resolve E2 e adiciona linhas
  - As duas ações acima devem empurrar a nota para ≥300 linhas de conteúdo e elevar o score para ≥9/12
- **Resultado:** TL;DR reescrito em 3 blocos (o que é / como construir / pitfall do leaderboard) resolve E1. Nova seção "## A dor que o golden set resolve" antes de "## O que é um golden set" — enquadra a ausência de observabilidade sobre regressões ("melhorou ou piorou?") → resolve E2. 284→316 linhas, cruza o piso; score esperado ≥9/12. `updated:`/`status: growing`. E3/P1 ficaram fora do plano (nota conceitual). (onda enriquecer-galho, 01/07)

#### 03 - Scoring rubrics e critérios   [mecânico]
- **Enriquecimento:** ✅ feita (2026-07-01)
- **Estado:** 324 linhas reais · fase: Iniciado · status: seedling
- **Núcleo/gaps:** E1
- **Score:** 9/12
- **Plano de execução:**
  - Expandir callout `[!abstract]` TL;DR para ≥3 linhas markdown de corpo (atualmente 1 parágrafo em linha única) → resolve E1 e eleva score para 10/12
- **Resultado:** TL;DR expandido de 1 linha p/ 3 parágrafos (o que é / mecanismo / trade-off), registro Feynman. Edição cirúrgica (6+/2-), `updated:` bumpado. Score esperado 10/12. (piloto enriquecer-galho, 01/07)

#### 04 - LLM-as-judge — quando e como   [mecânico]
- **Enriquecimento:** ✅ feita (2026-07-01)
- **Estado:** 333 linhas reais · fase: Iniciado · status: seedling
- **Núcleo/gaps:** E2
- **Score:** 9/12
- **Plano de execução:**
  - Adicionar parágrafo de abertura narrativo (2-3 linhas) entre o título e a seção "Quando faz sentido" — apresentar o problema concreto (o gargalo de eval subjetivo em escala: humano não revisa mil outputs por iteração) antes de entrar nas listas → resolve E2
- **Resultado:** Parágrafo narrativo de abertura (3 linhas) inserido entre o callout `[!question]` e `## Quando faz sentido` — gargalo concreto (humano não escala p/ 1000 outputs/rodada) posiciona o LLM-as-judge antes das listas. Resolve E2. `updated:` bumpado. Sem desvios. (onda enriquecer-galho, 01/07)

#### 05 - Regression testing em LLMs   [mecânico]
- **Enriquecimento:** ➖ não precisa
- **Estado:** 317 linhas reais · fase: Iniciado · status: seedling
- **Núcleo/gaps:** E3
- **Score:** 11/12
- **Plano de execução:**
  - — nenhuma
- **Resultado:** 203→400 linhas, fecha o piso Adepto sem padding. Acrescentado: TL;DR em 3 blocos (E1); 2 vídeos verificados via oEmbed — Hamel Husain crash course + Lenny's Podcast (M1); bloco Pydantic com o campo obrigatório que força o modelo a inventar `data_calibracao`, mais a versão com `CampoExtraido` (P1); seção "De onde tirar o sinal de confiança" (autoavaliação / logprobs / autoconsistência + score de recuperação, com o ponto cego do erro estável); seção "A granularidade da abstenção" (por campo vs por documento, e a dependência de interface de revisão); Cenário 3 (agente que se abstém de **agir** — o ponto de decisão é a tool call, métrica = ações sob ambiguidade não resolvida); seção "Quando o próprio juiz precisa se abster" (`indeterminado` fora da média); exemplo de CSV com uma linha por família de anti-test; checklist de implementação; seção "O que abstenção não conserta" (recuperação ruim, modelo incapaz, grounding); 2 callouts `[!question]-` (fine-tuning não resolve; a objeção de produto); armadilhas movidas para seção `## Armadilhas comuns` própria (E8); fonte nova Kadavath et al. 2022.

#### 06 - Frameworks 2026 — Promptfoo, Braintrust, Langfuse, Patronus, Phoenix   [mecânico]
- **Enriquecimento:** ➖ não precisa
- **Estado:** 439 linhas totais / ~240 não-vazias · fase: Iniciado · status: seedling / in_progress
- **Núcleo/gaps:** E2, P1
- **Score:** 10/12
- **Plano de execução:**
  - — nenhuma (opcional E2: adicionar parágrafo de abertura antes de "## A taxonomia dos cinco" enquadrando o problema para evitar salto abrupto do TL;DR)
- **Resultado:** —

#### 07 - Eval em CI-CD   [mecânico]
- **Enriquecimento:** ➖ não precisa
- **Estado:** ~365 linhas reais · fase: Iniciado · status: seedling
- **Núcleo/gaps:** E3, P1
- **Score:** 10/12
- **Plano de execução:**
  - — nenhuma
- **Resultado:** —

#### 08 - Eval por contexto — LLM, RAG, agent, prompt   [mecânico]
- **Enriquecimento:** ➖ não precisa
- **Estado:** ~276 linhas reais / 326 linhas totais · fase: Iniciado · status: growing
- **Núcleo/gaps:** E3, P1
- **Score:** 10/12
- **Plano de execução:**
  - — nenhuma
- **Resultado:** —

#### 09 - Abstenção — projetar e medir o "não sei"   [substantivo]
- **Enriquecimento:** ✅ feita (2026-08-19)
- **Estado:** 400 linhas · fase: Adepto · status: growing
- **Núcleo/gaps:** — (T2, M1 e P1 fechados na expansão)
- **Score:** ~10/13 (checklist já com o novo item P4)
- **Plano de execução:**
  - `/adicionar-midia` — buscar vídeo/talk sobre calibração e abstenção em LLM → resolve M1
  - Acrescentar um bloco de código com o caso-problema: pipeline que grava `data_de_emissao` no campo `data_de_calibracao` por ausência de abstenção, e a versão com `null` + fila de revisão → resolve P1
  - **Expansão real de conteúdo até o piso de 400** (déficit +197): terceiro cenário prático (agente que abstém de chamar ferramenta quando o argumento é incerto), seção sobre abstenção parcial por campo vs por documento, e tratamento do caso em que o próprio juiz precisa abster. Expansão substantiva, nunca padding.
- **Resultado:** —
