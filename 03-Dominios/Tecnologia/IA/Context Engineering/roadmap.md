---
title: "Roadmap — Context Engineering"
created: 2026-07-02
type: meta
publish: false
tags:
  - meta
  - roadmap
---

# Roadmap — Context Engineering

Diagnóstico migrado de guia/roadmap - ia.md (30/06). Cada entrada tem estado de enriquecimento, score, classificação de custo e plano de execução acionável.

**Galho:** `03-Dominios/Tecnologia/IA/Context Engineering`

> [!warning] Diagnóstico de 30/06 — pode estar defasado. Vários itens marcados ⬜ podem já ter sido enriquecidos depois; reconciliar com o estado real ao tratar o galho.

## Régua de análise

Checklist `verificar-nota` — 12 itens (isenções por fase/tipo/broto aplicadas por nota):

| Grupo | Itens |
|-------|-------|
| ESTRUTURA | E1 TL;DR · E2 Abertura-problema · E3 Mermaid · E4 Casos práticos · E5 O que vem a seguir · E6 Inglês · E7 Tabela PT↔EN · E8 Armadilhas [!warning] |
| PROFUNDIDADE | P1 Código-com-falha · P2 Mecanismo explicado |
| LINKS | L1 Wikilink cross-galho · L2 Referência externa (URL) |
| MÍDIA | M1 Vídeo/podcast embutido |

**Esquema de `fase:` detectado:** COM fase (Adepto)
**Piso de linhas:** aplicável — Adepto ≥400

## Tabela-resumo

| Métrica | Valor |
|---------|-------|
| Total de notas | 16 |
| ⬜ pendente | 0 |
| ➖ não precisa | 9 |
| ✅ feita | 7 |
| 🔄 em andamento | 0 |
| % concluído | 100% ✅ |

---

## Notas

#### 01 - De prompt engineering a context engineering   [mecânico]
- **Enriquecimento:** ✅ feita (2026-07-03)
- **Estado:** 401 linhas · fase: Adepto · status: growing
- **Núcleo/gaps:** P1, L2
- **Score:** 10/12
- **Plano de execução:**
  - Adicionar URLs reais às referências (tweet Karpathy, memo Lutke/Shopify, doc Anthropic "Building effective agents", Bytebytego guide, paper "Lost in the Middle")
- **Resultado:** ✅ verificado PASS (2026-07-03): plano aplicado + auditoria cética passou.

#### 02 - Os quatro pilares — prompt, context, intent, specification   [mecânico]
- **Enriquecimento:** ✅ feita (2026-07-03)
- **Estado:** 401 linhas · fase: Adepto · status: growing
- **Núcleo/gaps:** P1, L2
- **Score:** 10/12
- **Plano de execução:**
  - Adicionar URLs reais às referências (Karpathy "Software Is Changing (Again)", Anthropic "Building effective agents", Braintrust "Evals-driven development", NIST AI RMF, EU AI Act, Hamel Husain "Your AI Product Needs Evals")
- **Resultado:** ✅ verificado PASS (2026-07-03): plano aplicado + auditoria cética passou.

#### 03 - Context rot e atenção diluída   [mecânico]
- **Enriquecimento:** ➖ não precisa
- **Estado:** 401 linhas · fase: Adepto · status: growing
- **Núcleo/gaps:** P1
- **Score:** 11/12
- **Plano de execução:**
  - — nenhuma
- **Resultado:** —

#### 04 - Context pipelines — montagem dinâmica   [mecânico]
- **Enriquecimento:** ➖ não precisa
- **Estado:** 401 linhas · fase: Adepto · status: growing
- **Núcleo/gaps:** P1
- **Score:** 11/12
- **Plano de execução:**
  - — nenhuma
- **Resultado:** —

#### 05 - Camadas de contexto — persistente, temporal, transiente   [mecânico]
- **Enriquecimento:** ➖ não precisa
- **Estado:** 402 linhas · fase: Adepto · status: growing
- **Núcleo/gaps:** P1
- **Score:** 11/12
- **Plano de execução:**
  - — nenhuma
- **Resultado:** —

#### 06 - Dynamic retrieval beyond RAG   [mecânico]
- **Enriquecimento:** ✅ feita (2026-07-03)
- **Estado:** 385 linhas · fase: Adepto · status: growing
- **Núcleo/gaps:** —
- **Score:** 12/12
- **Plano de execução:**
  - Nota 15 linhas abaixo do piso Adepto (≥400) — expandir "Estado da arte" ou "Métricas" com ~15 linhas de substância para cruzar o limite formal
- **Resultado:** ✅ verificado PASS (2026-07-03): plano aplicado + auditoria cética passou.

#### 07 - Compressão e pruning de informação   [mecânico]
- **Enriquecimento:** ➖ não precisa
- **Estado:** 401 linhas · fase: Adepto · status: growing
- **Núcleo/gaps:** P1
- **Score:** 11/12
- **Plano de execução:**
  - — nenhuma
- **Resultado:** —

#### 08 - Memória agentica — self-editing memory   [mecânico]
- **Enriquecimento:** ➖ não precisa
- **Estado:** 413 linhas · fase: Adepto · status: growing
- **Núcleo/gaps:** P1, L1
- **Score:** 10/12
- **Plano de execução:**
  - Opcional: adicionar wikilink cross-galho para uma nota do galho [[Memória de Agentes]] em "Veja também" ou no corpo
- **Resultado:** —

#### 09 - Shared memory em multi-agent   [mecânico]
- **Enriquecimento:** ✅ feita
- **Estado:** 403 linhas · fase: Adepto · status: growing
- **Núcleo/gaps:** P1, L1
- **Score:** 10/12
- **Plano de execução:**
  - Piso: nota 11 linhas abaixo do piso Adepto (≥400) — acrescentar ~15 linhas de conteúdo substantivo (ex.: expandir "Estado da arte" ou adicionar sub-item em "Quando NÃO usar")
  - Adicionar ao menos 1 wikilink cross-galho no corpo ou em "Veja também" — candidatos: [[Concorrência]] (race conditions), [[Anatomia dos LLMs]] (janela de contexto), ou outra nota fora de Context Engineering
- **Resultado:** Acrescentado sub-item "Um teste rápido antes de orquestrar" em "Quando NÃO usar" (+15 linhas, 389→403); wikilink cross-galho [[03 - Estado compartilhado e race conditions]] (Concorrência e Paralelismo) inserido na armadilha "Estado mutável sem controle de concorrência".

#### 10 - Structured state tracking   [mecânico]
- **Enriquecimento:** ➖ não precisa
- **Estado:** 406 linhas · fase: Adepto · status: growing
- **Núcleo/gaps:** P1, L1
- **Score:** 10/12
- **Plano de execução:**
  - — nenhuma
- **Resultado:** —

#### 11 - Skills e instructions como contexto   [substantivo]
- **Enriquecimento:** ✅ feita (2026-07-03)
- **Estado:** 361 linhas · fase: Adepto · status: growing
- **Núcleo/gaps:** E3, P1
- **Score:** 10/12
- **Plano de execução:**
  - Nota abaixo do piso Adepto (≥400): expandir com 1-2 casos práticos adicionais ou converter os diagramas ASCII (separação de camadas, cross-tool 80/20, hierarquia global→projeto→diretório) para diagramas Mermaid reais
  - Adicionar 1 exemplo de código-com-falha concreto (ex: AGENTS.md com regras contraditórias entre `AGENTS.md` e `CLAUDE.md` e o comportamento não-determinístico resultante)
- **Resultado:** ✅ verificado PASS (2026-07-03): plano aplicado + auditoria cética passou.

#### 12 - Guardrails determinísticos   [substantivo]
- **Enriquecimento:** ✅ feita (2026-07-03)
- **Estado:** 347 linhas · fase: Adepto · status: growing
- **Núcleo/gaps:** P1, L1, L2
- **Score:** 9/12
- **Plano de execução:**
  - Nota abaixo do piso Adepto (≥400): expandir "Estado da arte" ou "Métricas de eficácia" ou converter o único Mermaid em 2-3 diagramas (ex: sequenceDiagram de ataque por prompt injection bloqueado pelo pre-LLM + flowchart do three-tier)
  - Adicionar URLs às referências: CIO Magazine, Arthur AI, arxiv como links reais
  - Adicionar wikilink cross-galho para o galho Segurança e Guardrails em "Veja também"
- **Resultado:** ✅ verificado PASS (2026-07-03): plano aplicado + auditoria cética passou.

#### 13 - Entropia e qualidade de contexto   [mecânico]
- **Enriquecimento:** ➖ não precisa
- **Estado:** 401 linhas · fase: Adepto · status: growing
- **Núcleo/gaps:** P1
- **Score:** 11/12
- **Plano de execução:**
  - — nenhuma
- **Resultado:** —

#### 14 - Context engineering na prática — setup completo   [mecânico]
- **Enriquecimento:** ➖ não precisa
- **Estado:** 552 linhas · fase: Adepto · status: growing
- **Núcleo/gaps:** P1
- **Score:** 11/12
- **Plano de execução:**
  - — nenhuma
- **Resultado:** —

#### 15 - Técnicas de prompting — zero-shot, few-shot, CoT, ToT   [substantivo]
- **Enriquecimento:** ✅ feita (2026-07-03)
- **Estado:** 435 linhas · fase: Adepto · status: growing
- **Núcleo/gaps:** P1, L1
- **Score:** 10/12
- **Plano de execução:**
  - Adicionar wikilink para o galho Prompt Engineering (galho 12) em "Veja também" ou na abertura do TL;DR
  - Adicionar exemplo de código-com-falha na seção Few-shot — ex: 3 exemplos da mesma classe seguidos da query, mostrando classificação errada; depois versão corrigida com exemplos diversificados
- **Resultado:** ✅ verificado PASS (2026-07-03): plano aplicado + auditoria cética passou.

#### 16 - Agent skills marketplace e SKILL.md   [mecânico]
- **Enriquecimento:** ➖ não precisa
- **Estado:** 474 linhas · fase: Adepto · status: growing
- **Núcleo/gaps:** P1
- **Score:** 11/12
- **Plano de execução:**
  - — nenhuma
- **Resultado:** —
