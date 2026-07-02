---
title: "Roadmap — Improvement Loop"
created: 2026-07-02
type: meta
publish: false
tags:
  - meta
  - roadmap
---

# Roadmap — Improvement Loop

Diagnóstico migrado de guia/roadmap - ia.md (28/06). Cada entrada tem estado de enriquecimento, score, classificação de custo e plano de execução acionável.

**Galho:** `03-Dominios/Tecnologia/IA/Improvement Loop`

> [!warning] Diagnóstico de 28/06 — pode estar defasado. Vários itens marcados ⬜ podem já ter sido enriquecidos depois; reconciliar com o estado real ao tratar o galho.

## Régua de análise

Checklist `verificar-nota` — 12 itens (isenções por fase/tipo/broto aplicadas por nota):

| Grupo | Itens |
|-------|-------|
| ESTRUTURA | E1 TL;DR · E2 Abertura-problema · E3 Mermaid · E4 Casos práticos · E5 O que vem a seguir · E6 Inglês · E7 Tabela PT↔EN · E8 Armadilhas [!warning] |
| PROFUNDIDADE | P1 Código-com-falha · P2 Mecanismo explicado |
| LINKS | L1 Wikilink cross-galho · L2 Referência externa (URL) |
| MÍDIA | M1 Vídeo/podcast embutido |

**Esquema de `fase:` detectado:** COM fase (Iniciado)
**Piso de linhas:** aplicável — Iniciado ≥300

## Tabela-resumo

| Métrica | Valor |
|---------|-------|
| Total de notas | 7 |
| ⬜ pendente | 3 |
| ➖ não precisa | 4 |
| ✅ feita | 0 |
| 🔄 em andamento | 0 |
| % concluído | 0% |

---

## Notas

#### 01 - O ciclo eval → diff → ship   [mecânico]
- **Enriquecimento:** ➖ não precisa
- **Estado:** 301 linhas reais · fase: Iniciado · status: seedling
- **Núcleo/gaps:** E3, P1
- **Score:** 10/12
- **Plano de execução:**
  - — nenhuma
- **Resultado:** —

#### 02 - A-B testing de prompts   [substantivo]
- **Enriquecimento:** ⬜ pendente
- **Estado:** 301 linhas reais · fase: Iniciado · status: seedling
- **Núcleo/gaps:** E2
- **Score:** 9/12
- **Plano de execução:**
  - Adicionar parágrafo de abertura com problema/cenário entre o TL;DR e a primeira seção ("A unidade de teste"): a nota abre direto em tabela sem situar o leitor no problema que o A/B resolve
- **Resultado:** —

#### 03 - Prompt versioning — semver para prompts   [mecânico]
- **Enriquecimento:** ➖ não precisa
- **Estado:** 301 linhas reais · fase: Iniciado · status: seedling
- **Núcleo/gaps:** E3, P1
- **Score:** 10/12
- **Plano de execução:**
  - — nenhuma
- **Resultado:** —

#### 04 - Champion-challenger em produção   [substantivo]
- **Enriquecimento:** ⬜ pendente
- **Estado:** 266 linhas reais · fase: Iniciado · status: seedling
- **Núcleo/gaps:** E2, E3, P1
- **Score:** 9/12
- **Plano de execução:**
  - Adicionar abertura-problema (2-3 parágrafos narrativos antes de "A mecânica básica"): "como shipar um novo prompt sem quebrar prod" → por que A/B simples não basta → o que champion-challenger resolve; cobre E2 e sobe o piso para ≥300 linhas
  - Expandir TL;DR para ≥3 linhas raw de corpo (reformatar o parágrafo único em blocos por dimensão: setup / critérios / rollback / anti-padrão)
  - Converter o diagrama ASCII (linhas 32-67) para Mermaid flowchart (cobre E3)
- **Resultado:** —

#### 05 - Auto-prompt optimization — DSPy e além   [mecânico]
- **Enriquecimento:** ➖ não precisa
- **Estado:** 301 linhas reais · fase: Iniciado · status: seedling
- **Núcleo/gaps:** E3, P1
- **Score:** 10/12
- **Plano de execução:**
  - — nenhuma
- **Resultado:** —

#### 06 - Capturando feedback do usuário como sinal   [substantivo]
- **Enriquecimento:** ⬜ pendente
- **Estado:** 221 linhas reais · fase: Iniciado · status: seedling
- **Núcleo/gaps:** E3, P1
- **Score:** 10/12
- **Plano de execução:**
  - Expandir ~79 linhas de conteúdo real para atingir o piso ≥300: adicionar diagrama Mermaid do pipeline coleta→agregação→triagem→backlog (fluxo já existe como texto, só visualizar) + trecho de código-com-falha (endpoint sem `trace_id` como anti-padrão, seguido da versão corrigida)
- **Resultado:** —

#### 07 - Eval gates em CI — quando bloquear merge   [mecânico]
- **Enriquecimento:** ➖ não precisa
- **Estado:** 374 linhas reais · fase: Iniciado · status: seedling
- **Núcleo/gaps:** E3, P1
- **Score:** 10/12
- **Plano de execução:**
  - — nenhuma
- **Resultado:** —
