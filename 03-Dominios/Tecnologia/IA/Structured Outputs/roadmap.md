---
title: "Roadmap — Structured Outputs"
created: 2026-07-01
type: meta
publish: false
tags:
  - meta
  - roadmap
---

# Roadmap — Structured Outputs

Diagnóstico migrado de guia/roadmap - ia.md (30/06). Cada entrada tem estado de enriquecimento, score, classificação de custo e plano de execução acionável.

**Galho:** `03-Dominios/Tecnologia/IA/Structured Outputs`
**Diagnóstico:** 2026-06-28 (migrado 2026-07-01)
**Última execução:** 2026-07-02 (galho concluído — 7 ✅ + 1 ➖)

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
| Total de notas | 8 |
| ⬜ pendente | 0 |
| ➖ não precisa | 1 |
| ✅ feita | 7 |
| 🔄 em andamento | 0 |
| % concluído | 100% |

---

## Notas

#### 01 - O problema do output não estruturado   [mecânico]
- **Enriquecimento:** ➖ não precisa
- **Estado:** 301 linhas reais · fase: Iniciado · status: seedling / in_progress
- **Núcleo/gaps:** E3
- **Score:** 11/12
- **Plano de execução:**
  - — nenhuma (opcional: adicionar diagrama Mermaid da taxonomia de falhas ou do pipeline texto→schema→semântica)
- **Resultado:** —

#### 02 - JSON Schema como contrato   [substantivo]
- **Enriquecimento:** ✅ feita (2026-07-02)
- **Estado:** 241 linhas reais · fase: Iniciado · status: seedling
- **Núcleo/gaps:** E2, E3, P1
- **Score:** 9/12
- **Plano de execução:**
  - Expandir volume para ≥300 linhas reais: adicionar exemplo de schema inválido (P1 código-com-falha) ou caso prático end-to-end (classificação de bug ou extração de entidade) → resolve P1 e fecha piso Iniciado simultaneamente
  - Corrigir abertura: reescrever abertura de "JSON Schema é uma especificação…" para cenário que motiva o schema antes da definição formal → resolve E2
- **Resultado:** P1 resolvido com seção nova "Caso prático — do schema quebrado ao contrato confiável" (schema "Tentativa 1" falhando de 3 formas + "Tentativa 2" corrigido). E2 resolvido reescrevendo abertura de "JSON Schema 101" com cenário de bug report antes da definição formal. 241→385 linhas reais. Score ~10/12. E3/E4 seguem abertos (fora do plano).

#### 03 - Function calling como mecanismo de output   [substantivo]
- **Enriquecimento:** ✅ feita (2026-07-02)
- **Estado:** 215 linhas reais · fase: Iniciado · status: seedling
- **Núcleo/gaps:** E3, P1
- **Score:** 10/12
- **Plano de execução:**
  - Adicionar diagrama Mermaid do fluxo (prompt → tool definition → provider validation → tool_use block → output) → resolve E3, +~15 linhas reais
  - Adicionar exemplo P1 de código-com-falha: trecho sem `tool_choice` forçado mostrando resposta em texto livre e parse falhando → resolve P1, +~15-20 linhas reais
  - Expandir "A anatomia" com diagrama de sequência ou adicionar caso end-to-end (extração de invoice) para cruzar piso de 300 linhas reais (~40-50 linhas densas)
- **Resultado:** E3 resolvido com flowchart Mermaid (prompt→tool def→provider validation→tool_use→output). P1 resolvido em "Armadilhas comuns" (sem tool_choice forçado → NameError + fix). Caso end-to-end de extração de invoice adicionado. status seedling→growing. ~300→451 linhas. Checklist: só E4 (seção própria) e M1 (mídia) faltam. Sem desvio.

#### 04 - OpenAI Structured Outputs — strict mode   [substantivo]
- **Enriquecimento:** ✅ feita (2026-07-02)
- **Estado:** 302 linhas reais · fase: Iniciado · status: seedling
- **Núcleo/gaps:** E3, P1
- **Score:** 10/12
- **Plano de execução:**
  - Verificar modelos e limites numéricos contra docs OpenAI atuais antes de enriquecer (caducidade: gpt-4.1, gpt-5, gpt-5-mini, gpt-5-thinking, o3, o4; limites: 100 props, 5 níveis, 500 enum values, 15000 chars)
  - Adicionar diagrama Mermaid do fluxo de constrained decoding (schema → grammar → decoder → token válido → output) → resolve E3, +~15 linhas
  - Adicionar exemplo P1 de código-com-falha: trecho com `strict: false` ou sem `additionalProperties: false` em objeto aninhado, mostrando o erro de schema que o SDK rejeita → resolve P1, +~15-20 linhas
- **Resultado:** Limites numéricos (100 props, 5 níveis, 500 enums, 15000 chars) verificados contra docs OpenAI atuais — corretos, sem correção. E3 resolvido com Mermaid flowchart (schema→grammar→decoder→token→output). P1 resolvido com snippet strict:true sem additionalProperties:false em objeto aninhado + BadRequestError real. updated→2026-07-02. 360 linhas. Só E4 falta (fora do plano).

#### 05 - Anthropic tool use para forçar formato   [substantivo]
- **Enriquecimento:** ✅ feita (2026-07-02)
- **Estado:** 311 linhas reais · fase: Iniciado · status: seedling
- **Núcleo/gaps:** E3, P1
- **Score:** 10/12
- **Plano de execução:**
  - Verificar se Anthropic lançou suporte nativo a structured outputs (beta, 2025) e decidir se a nota deve absorver o novo caminho ou restringir escopo ao mecanismo de tool use explicitamente
  - Adicionar diagrama Mermaid do fluxo (tool_choice forçado → bloco tool_use → extração input → validação) → resolve E3, +~12-15 linhas
  - Adicionar P1: snippet mostrando falha real (sem `tool_choice` explícito, resposta em texto livre; ou `stop_reason == "max_length"` com bloco incompleto) → resolve P1, +~10-15 linhas
- **Resultado:** Pesquisado: Anthropic lançou Structured Outputs beta 14/11/2025 (output_format + strict). Escopo mantido em tool use forçado, com callout [!info] no topo citando a novidade + link doc. E3 com flowchart Mermaid (tool_choice→stop_reason→tool_use→input→validação→retry). P1 com 2 snippets (tool_choice ausente; max_tokens curto truncado). Corrigido stop_reason inexistente "max_length"→"max_tokens". status seedling→growing. 379 linhas, ~11/12.

#### 06 - Gemini structured output   [substantivo]
- **Enriquecimento:** ✅ feita (2026-07-02)
- **Estado:** 229 linhas reais · fase: Iniciado · status: seedling / in_progress
- **Núcleo/gaps:** E2, E3, P1, L1
- **Score:** 8/12
- **Plano de execução:**
  - Adicionar parágrafo de abertura com problema/cenário antes de "## O mecanismo" (ex: "Você vem da OpenAI e quer trocar de provider — o schema que funcionava não roda no Gemini porque os tipos estão em caixa alta. Por quê?") → resolve E2, +~12 linhas
  - Adicionar diagrama Mermaid do fluxo: `GenerateContentConfig` (response_mime_type + response_schema) → SDK → `response.parsed` / `response.text` (fallback) → resolve E3, +~14 linhas
  - Adicionar snippet código-com-falha: schema com tipos em caixa baixa (`"type": "object"`) gerando `response.parsed == None` e shape incorreto; versão corrigida com `"OBJECT"` → resolve P1, +~15 linhas
  - Adicionar wikilink cross-galho (ex: para nota de Anatomia dos LLMs) → resolve L1
  - Expandir seção "Boas práticas" com `model_config = ConfigDict(extra="forbid")` em Pydantic (~15 linhas) para atingir piso ≥300 linhas reais
- **Resultado:** E2 (abertura migração OpenAI→Gemini, caixa alta), E3 (Mermaid GenerateContentConfig→SDK→parsed/text fallback), P1 (schema caixa baixa→parsed==None + fix caixa alta), L1 (wikilink Anatomia dos LLMs/11), Boas práticas expandida com ConfigDict(extra="forbid"). 320→421 linhas, 11/12. Só E4/M1 faltam (fora do plano).

#### 07 - Validação e retry — Pydantic, Zod   [substantivo]
- **Enriquecimento:** ✅ feita (2026-07-02)
- **Estado:** 277 linhas reais · fase: Iniciado · status: seedling
- **Núcleo/gaps:** E3, P1
- **Score:** 10/12
- **Plano de execução:**
  - Expandir seção "Boas práticas" com exemplo de `model_config = ConfigDict(extra="forbid")` para rejeitar campos extras e parágrafo sobre validar o schema em ambiente de desenvolvimento (~20-25 linhas) → eleva conteúdo real para ≥300 e fecha piso Iniciado
- **Resultado:** Duas subseções em "Boas práticas": "Rejeite campos extras — extra='forbid'" (Pydantic ConfigDict + .strict() no Zod, drift silencioso) e "Valide o schema em ambiente de desenvolvimento" (testar prompt+schema como suíte). +~24 linhas, 362→384. Piso fechado. E3/E4/M1 fora do plano.

#### 08 - Streaming de structured outputs   [substantivo]
- **Enriquecimento:** ✅ feita (2026-07-02)
- **Estado:** ~230 linhas reais · fase: Iniciado · status: seedling
- **Núcleo/gaps:** E3, P1
- **Score:** 10/12
- **Plano de execução:**
  - Adicionar diagrama Mermaid de fluxo de decisão entre os 3 caminhos (Caminho 1 → Caminho 2 → Caminho 3) → resolve E3 e eleva linhas reais, +~15-20 linhas
  - Adicionar snippet código-com-falha na seção "Armadilhas comuns" (ex: chamada ingênua a `JSON.parse(chunk)` sem buffer, mostrando o erro) → resolve P1, +~10-15 linhas
  - Expandir 1 parágrafo em "Validação em streaming" para cruzar ≥300 linhas reais
- **Resultado:** E3 com seção "Qual caminho escolher" + Mermaid de decisão Caminho 1/2/3. P1 com callout [!warning] em Armadilhas (JSON.parse(chunk)→SyntaxError + fix com buffer/partial-json). "Validação em streaming" expandida (critério monotônico + sanity_check_partial()). status seedling→growing. 302→388 linhas. Plano integral.
