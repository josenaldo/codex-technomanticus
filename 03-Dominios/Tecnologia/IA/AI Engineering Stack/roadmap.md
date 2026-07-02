---
title: "Roadmap — AI Engineering Stack"
created: 2026-07-02
type: meta
publish: false
tags:
  - meta
  - roadmap
---

# Roadmap — AI Engineering Stack

Diagnóstico migrado de guia/roadmap - ia.md (30/06). Cada entrada tem estado de enriquecimento, score, classificação de custo e plano de execução acionável.

**Galho:** `03-Dominios/Tecnologia/IA/AI Engineering Stack`

> [!warning] Diagnóstico de 30/06 — pode estar defasado. Vários itens marcados ⬜ podem já ter sido enriquecidos depois; reconciliar com o estado real ao tratar o galho.

## Régua de análise

Checklist `verificar-nota` — 12 itens (isenções por fase/tipo/broto aplicadas por nota):

| Grupo | Itens |
|-------|-------|
| ESTRUTURA | E1 TL;DR · E2 Abertura-problema · E3 Mermaid · E4 Casos práticos · E5 O que vem a seguir · E6 Inglês · E7 Tabela PT↔EN · E8 Armadilhas [!warning] |
| PROFUNDIDADE | P1 Código-com-falha · P2 Mecanismo explicado |
| LINKS | L1 Wikilink cross-galho · L2 Referência externa (URL) |
| MÍDIA | M1 Vídeo/podcast embutido |

**Esquema de `fase:` detectado:** COM fase (Iniciado 01–12, Adepto 13)
**Piso de linhas:** aplicável — Iniciado ≥300; Adepto ≥400

## Tabela-resumo

| Métrica | Valor |
|---------|-------|
| Total de notas | 13 |
| ⬜ pendente | 12 |
| ➖ não precisa | 1 |
| ✅ feita | 0 |
| 🔄 em andamento | 0 |
| % concluído | 0% |

---

## Notas

#### 01 - As 11 camadas — visão geral   [mecânico]
- **Enriquecimento:** ➖ não precisa
- **Estado:** 308 linhas · fase: Iniciado · status: seedling
- **Núcleo/gaps:** P1
- **Score:** 11/12
- **Plano de execução:**
  - — nenhuma
- **Resultado:** —

#### 02 - Purpose Layer — o que o sistema é   [mecânico]
- **Enriquecimento:** ⬜ pendente
- **Estado:** 305 linhas · fase: Iniciado · status: seedling
- **Núcleo/gaps:** P1
- **Score:** 11/12
- **Plano de execução:**
  - Remover a seção "Como explicar em inglês" duplicada (aparece duas vezes: linhas ~138 e ~159); manter a segunda versão (mais completa, com tabela PT↔EN) e excluir a primeira
- **Resultado:** —

#### 03 - Prompt Layer   [substantivo]
- **Enriquecimento:** ⬜ pendente
- **Estado:** 305 linhas totais (~204 de conteúdo efetivo; linhas 205-305 são em branco) · fase: Iniciado · status: seedling
- **Núcleo/gaps:** P1
- **Score:** 11/12
- **Plano de execução:**
  - Purgar as ~100 linhas em branco no fim do arquivo (linhas 205-305)
  - Adicionar exemplo de código-com-falha: system prompt minimalista causando comportamento inesperado em produção (ex: prompt sem `uncertainty_behavior` → modelo inventa resposta em vez de escalar) — ativa P1
  - Expandir "Decisões-chave"/"Anatomia" com exemplo trabalhado adicional para aproximar o conteúdo efetivo do piso de 300 linhas
- **Resultado:** —

#### 04 - Context Layer   [substantivo]
- **Enriquecimento:** ⬜ pendente
- **Estado:** 190 linhas (linhas 191–305 são branco) · fase: Iniciado · status: seedling
- **Núcleo/gaps:** P1
- **Score:** 11/12
- **Plano de execução:**
  - Expandir o conteúdo efetivo de ~190 para ≥300 linhas — candidatos: aprofundar "Decisões-chave" com exemplos trabalhados (ex: pull vs push com comparativo de custo por chamada), subseção "Context pipelines na prática" (compressão periódica, expiração por horizonte, reset por unidade de trabalho), ou terceiro cenário prático
  - Purgar as ~115 linhas em branco no fim do arquivo
- **Resultado:** —

#### 05 - Output Layer   [substantivo]
- **Enriquecimento:** ⬜ pendente
- **Estado:** 201 linhas reais · fase: Iniciado · status: seedling
- **Núcleo/gaps:** P1
- **Score:** 11/12
- **Plano de execução:**
  - Expandir de 201 para ≥300 linhas — candidatos: subseção "Validação pós-output", exemplos trabalhados de schema rígido vs leve, ou terceiro cenário prático (ex: sistema de geração de código com output como ação direta)
  - Adicionar bloco de código-com-falha (ex: parser Python quebrando com prosa antes do `{`; ou Pydantic rejeitando campo extra inesperado) — ativa P1
  - Purgar as ~105 linhas em branco no fim do arquivo
- **Resultado:** —

#### 06 - Retrieval Layer   [substantivo]
- **Enriquecimento:** ⬜ pendente
- **Estado:** 241 linhas reais · fase: Iniciado · status: seedling
- **Núcleo/gaps:** P1
- **Score:** 11/12
- **Plano de execução:**
  - Expandir de 241 para ≥300 linhas — candidatos: aprofundar "Métricas de qualidade do retrieval" com exemplos numéricos concretos, Cenário 3 (conflito entre fontes desatualizadas em sistema jurídico), ou expandir "Implementações comuns" com snippet de hybrid search + reranker (BM25 → embedding → cross-encoder)
  - Purgar as ~62 linhas em branco no fim do arquivo
- **Resultado:** —

#### 07 - Tool Layer   [substantivo]
- **Enriquecimento:** ⬜ pendente
- **Estado:** 219 linhas reais · fase: Iniciado · status: seedling
- **Núcleo/gaps:** P1
- **Score:** 11/12
- **Plano de execução:**
  - Expandir de 219 para ≥300 linhas — candidatos: (a) Cenário 3 mostrando tool failure handling na prática (retry+fallback evitando duplicação); (b) aprofundar "Tool design é trabalho de engenharia" com schema bem vs mal descrito lado a lado (ativa também P1); (c) expandir "Categorias de tools" com exemplos concretos em código
- **Resultado:** —

#### 08 - Workflow vs Agent Layer   [substantivo]
- **Enriquecimento:** ⬜ pendente
- **Estado:** 201 linhas reais · fase: Iniciado · status: seedling
- **Núcleo/gaps:** P1
- **Score:** 11/12
- **Plano de execução:**
  - Expandir de 201 para ≥300 linhas — candidatos: (a) Cenário 3 cobrindo caso limítrofe que migrou de workflow para agent; (b) seção de frameworks que implementam a distinção (LangGraph vs Prefect/Temporal); (c) snippet código-com-falha (loop agentic sem kill switch esgotando contexto) — ativa P1
- **Resultado:** —

#### 09 - Evaluation Layer   [substantivo]
- **Enriquecimento:** ⬜ pendente
- **Estado:** 199 linhas reais · fase: Iniciado · status: seedling
- **Núcleo/gaps:** P1
- **Score:** 11/12
- **Plano de execução:**
  - Expandir de 199 para ≥300 linhas — candidatos: (a) seção "Ferramentas de eval" (Braintrust, PromptFoo, LangSmith, Ragas); (b) expandir "Tipos de eval" com exemplos YAML/JSON para reference-based e reference-free; (c) Cenário 3 cobrindo eval de sistema RAG (recall@k, faithfulness, answer relevance)
- **Resultado:** —

#### 10 - Guardrail Layer   [substantivo]
- **Enriquecimento:** ⬜ pendente
- **Estado:** 199 linhas reais · fase: Iniciado · status: seedling
- **Núcleo/gaps:** P1
- **Score:** 11/12
- **Plano de execução:**
  - Expandir de 199 para ≥300 linhas — candidatos: (a) seção "Ferramentas de guardrail" (NeMo Guardrails, Guardrails AI, LangChain moderation); (b) expandir "Calibrando thresholds" com exemplo de log de disparo e ajuste; (c) Cenário 3 cobrindo guardrail de PII em sistema de saúde
- **Resultado:** —

#### 11 - Logging Layer   [substantivo]
- **Enriquecimento:** ⬜ pendente
- **Estado:** 211 linhas reais · fase: Iniciado · status: seedling
- **Núcleo/gaps:** P1
- **Score:** 11/12
- **Plano de execução:**
  - Expandir de 211 para ≥300 linhas — candidatos: (a) seção "Ferramentas de logging" (OpenTelemetry GenAI, Langfuse, Phoenix, Datadog); (b) expandir cada um dos 3 `[!warning]` com resolução concreta; (c) Cenário 3 cobrindo estratégia de sampling em sistema de alto volume
- **Resultado:** —

#### 12 - Improvement Layer   [substantivo]
- **Enriquecimento:** ⬜ pendente
- **Estado:** 203 linhas reais · fase: Iniciado · status: seedling
- **Núcleo/gaps:** P1
- **Score:** 11/12
- **Plano de execução:**
  - Expandir de 203 para ≥300 linhas — candidatos: (a) expandir cada um dos 3 `[!warning]` com resolução concreta; (b) Cenário 3 cobrindo drift detection automático (alertas de score + threshold); (c) subseção "Ferramentas" comparando Langfuse, Phoenix e Datadog GenAI
- **Resultado:** —

#### 13 - Setup completo — do zero ao sistema de produção   [substantivo]
- **Enriquecimento:** ⬜ pendente
- **Estado:** ~390 linhas reais · fase: Adepto · status: seedling
- **Núcleo/gaps:** P1
- **Score:** 11/12
- **Plano de execução:**
  - Expandir ~10 linhas para atingir o piso de 400 — candidatos: (a) 4º `[!warning]` cobrindo "começar a construir todas as camadas ao mesmo tempo antes de validar a Purpose Layer"; (b) expandir o checklist final com sub-itens de rollback — OU aplicar isenção de capstone (última nota do galho, funciona como recipe de fechamento do ciclo)
  - Corrigir `status: seedling` → `growing` no frontmatter — a nota está substancialmente completa (11/12, núcleo integral, seção de ponte para outros galhos)
- **Resultado:** —
