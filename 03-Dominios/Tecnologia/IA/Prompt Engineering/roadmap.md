---
title: "Roadmap — Prompt Engineering"
created: 2026-07-02
type: meta
publish: false
tags:
  - meta
  - roadmap
---

# Roadmap — Prompt Engineering

Diagnóstico migrado de guia/roadmap - ia.md (30/06). Cada entrada tem estado de enriquecimento, score, classificação de custo e plano de execução acionável.

**Galho:** `03-Dominios/Tecnologia/IA/Prompt Engineering`

> [!warning] Diagnóstico de 30/06 — pode estar defasado. Vários itens marcados ⬜ podem já ter sido enriquecidos depois; reconciliar com o estado real ao tratar o galho.

## Régua de análise

Checklist `verificar-nota` — 12 itens (isenções por fase/tipo/broto aplicadas por nota):

| Grupo | Itens |
|-------|-------|
| ESTRUTURA | E1 TL;DR · E2 Abertura-problema · E3 Mermaid · E4 Casos práticos · E5 O que vem a seguir · E6 Inglês · E7 Tabela PT↔EN · E8 Armadilhas [!warning] |
| PROFUNDIDADE | P1 Código-com-falha · P2 Mecanismo explicado |
| LINKS | L1 Wikilink cross-galho · L2 Referência externa (URL) |
| MÍDIA | M1 Vídeo/podcast embutido |

**Esquema de `fase:` detectado:** COM fase (Iniciado) **Piso de linhas:** aplicável — Iniciado ≥300

## Tabela-resumo

| Métrica | Valor |
|---------|-------|
| Total de notas | 9 |
| ⬜ pendente | 0 |
| ➖ não precisa | 2 |
| ✅ feita | 7 |
| 🔄 em andamento | 0 |
| % concluído | 100% ✅ |

---

## Notas

#### 01 - Por que prompt engineering ainda importa   [mecânico]
- **Enriquecimento:** ➖ não precisa
- **Estado:** 301 linhas reais · fase: Iniciado · status: seedling
- **Núcleo/gaps:** E3, P1
- **Score:** 10/12
- **Plano de execução:**
  - — nenhuma
- **Resultado:** —

#### 02 - Especificidade — a primeira disciplina   [mecânico]
- **Enriquecimento:** ➖ não precisa
- **Estado:** 304 linhas reais · fase: Iniciado · status: seedling
- **Núcleo/gaps:** E3
- **Score:** 11/12
- **Plano de execução:**
  - — nenhuma
- **Resultado:** —

#### 03 - Roles e personas — escolhendo o juízo do modelo   [mecânico]
- **Enriquecimento:** ✅ feita (2026-07-03)
- **Estado:** 322 linhas · fase: Iniciado · status: seedling
- **Núcleo/gaps:** E1
- **Score:** 10/12
- **Plano de execução:**
  - Expandir TL;DR de 1 parágrafo/linha para ≥3 linhas `>` distintas dentro do callout [!abstract]
- **Resultado:** ✅ verificado PASS (2026-07-03): plano aplicado + auditoria cética passou.
- **Passe 2026-08-20 — material externo:** Subseção **O terceiro canal: prefill do turno `assistant`** — o canal de controle que a nota não cobria (os 12 hits de "prefill" no domínio eram todos o prefill/decode da inferência, sentido diferente). Mecanismo (entregar o começo da continuação elimina a parte da distribuição onde o modelo faria outra coisa), exemplo em JSONC, ponte com few-shot (demonstrar vence explicar) e callout com as 2 pegadinhas: nem toda API aceita, e o prefill geralmente não volta na resposta — causa clássica do "JSON veio quebrado". Fonte da lacuna: [[2026-ia-do-zero-ao-senior-trilha-visual]].

#### 04 - O mega-prompt do Karpathy — anatomia da anti-sycophancy   [substantivo]
- **Enriquecimento:** ✅ feita (2026-07-03)
- **Estado:** 171 linhas reais · fase: Iniciado · status: seedling
- **Núcleo/gaps:** E1
- **Score:** 9/12
- **Plano de execução:**
  - Expandir corpo para atingir ≥300 linhas de conteúdo real (faltam ~130 linhas): aprofundar mecanismo RLHF, adicionar Mermaid de "caminhos de fuga × cláusulas", expandir exemplos práticos ou adicionar variante domain-specific com case concreto
  - Expandir TL;DR de 1 linha para ≥3 linhas `>` distintas dentro do callout [!abstract]
- **Resultado:** ✅ verificado PASS (2026-07-03): plano aplicado + auditoria cética passou.

#### 05 - Few-shot examples — exemplos como contrato   [substantivo]
- **Enriquecimento:** ✅ feita (2026-07-03)
- **Estado:** 211 linhas reais · fase: Iniciado · status: seedling / in_progress
- **Núcleo/gaps:** E3
- **Score:** 11/12
- **Plano de execução:**
  - Expandir conteúdo real de 211 → ≥300 linhas: adicionar diagrama Mermaid do fluxo de decisão (zero-shot → few-shot → fine-tuning) ou expandir "Como escolher exemplos" com case concreto end-to-end
- **Resultado:** ✅ verificado WARN (2026-07-03): plano aplicado + auditoria cética passou. — WARN: ressalvas menores (ver relatório da sessão)

#### 06 - Constraints declarativas — boundaries como engenharia   [substantivo]
- **Enriquecimento:** ✅ feita (2026-07-03)
- **Estado:** 294 linhas reais · fase: Iniciado · status: seedling
- **Núcleo/gaps:** E2, L2
- **Score:** 10/12
- **Plano de execução:**
  - Converter fontes para links markdown com URL completo (ex: `[Anthropic — Provide system prompts](https://docs.anthropic.com/...)`) — resolve L2 e adiciona ≥2 linhas
  - Adicionar abertura-problema antes de "O que é uma constraint declarativa": 2-3 linhas descrevendo a frustração concreta ("você diz 'seja conciso' e o modelo escreve cinco parágrafos") — resolve E2 e empurra sobre o piso 300
- **Resultado:** ✅ verificado WARN (2026-07-03): plano aplicado + auditoria cética passou. — WARN: ressalvas menores (ver relatório da sessão)

#### 07 - Iteration patterns — keep, change, do-not   [mecânico]
- **Enriquecimento:** ✅ feita (2026-07-03)
- **Estado:** 297 linhas reais · fase: Iniciado · status: seedling
- **Núcleo/gaps:** L2
- **Score:** 10/12
- **Plano de execução:**
  - Converter fontes para links markdown com URL completo (ex: `[Anthropic — Iterating on prompts](https://docs.anthropic.com/...)`) — resolve L2
  - Expandir TL;DR de 1 para 3 linhas explícitas (cada ponto em linha própria) ou adicionar 3 linhas de conteúdo em qualquer seção — empurra sobre o piso 300
- **Resultado:** ✅ verificado WARN (2026-07-03): plano aplicado + auditoria cética passou. — WARN: ressalvas menores (ver relatório da sessão)

#### 08 - Reasoning models — audit trail, não chain-of-thought   [substantivo]
- **Enriquecimento:** ✅ feita (2026-07-03)
- **Estado:** 201 linhas reais · fase: Iniciado · status: seedling
- **Núcleo/gaps:** E1
- **Score:** 9/12
- **Plano de execução:**
  - Expandir conteúdo em ~100 linhas reais para atingir piso Iniciado ≥300 (prioridade máxima)
  - Expandir TL;DR de 1 parágrafo corrido para ≥3 linhas explícitas (bullets ou linhas separadas)
  - Adicionar pelo menos 1 caso prático com prompt incorreto vs. correto (exemplo trabalhado)
- **Resultado:** ✅ verificado PASS (2026-07-03): plano aplicado + auditoria cética passou.

#### 09 - Anti-patterns e tells de IA — o que evitar   [substantivo]
- **Enriquecimento:** ✅ feita (2026-07-03)
- **Estado:** 184 linhas reais · fase: Iniciado · status: seedling / in_progress
- **Núcleo/gaps:** E1, E2, L2
- **Score:** 7/12
- **Plano de execução:**
  - Expandir nota para ≥300 linhas de conteúdo real (faltam ~116 linhas): adicionar 2 casos práticos trabalhados — prompt original com tell vs. reescrita sem tell
  - Expandir TL;DR para ≥3 linhas de arquivo (atualmente 1 parágrafo compacto numa única linha)
  - Adicionar abertura-problema antes do primeiro H2 — cenário concreto (ex.: "você recebe um draft e percebe que parece ChatGPT")
  - Corrigir L2: substituir `(docs.anthropic.com)` por URL markdown completo `[Style guidelines](https://docs.anthropic.com/...)`
- **Resultado:** ✅ verificado WARN (2026-07-03): plano aplicado + auditoria cética passou. — WARN: ressalvas menores (ver relatório da sessão)
