---
title: "Roadmap — 11 - Estratégias estruturais de contexto"
created: 2026-07-02
type: meta
publish: false
tags:
  - meta
  - roadmap
---

# Roadmap — 11 - Estratégias estruturais de contexto

Diagnóstico nota a nota. Cada entrada tem estado de enriquecimento, score, classificação
de custo e plano de execução acionável. Gerado por `/diagnosticar-galho`.

**Galho:** `03-Dominios/Tecnologia/IA/Claude Code/Workflows/11 - Estratégias estruturais de contexto`
**Nível:** galho-folha
**Diagnóstico:** 2026-07-02
**Última execução:** —

## Régua de análise

Checklist `verificar-nota` — 12 itens (isenções por fase/tipo/broto aplicadas por nota):

| Grupo | Itens |
|-------|-------|
| ESTRUTURA | E1 TL;DR · E2 Abertura-problema · E3 Mermaid · E4 Casos práticos · E5 O que vem a seguir · E6 Inglês · E7 Tabela PT↔EN · E8 Armadilhas [!warning] |
| PROFUNDIDADE | P1 Código-com-falha · P2 Mecanismo explicado |
| LINKS | L1 Wikilink cross-galho · L2 Referência externa (URL) |
| MÍDIA | M1 Vídeo/podcast embutido |

**Esquema de `fase:` detectado:** COM fase (Iniciado/Adepto/Magus)
**Piso de linhas:** Iniciado ≥300 · Adepto ≥400 · Magus ≥500

## Tabela-resumo

| Métrica | Valor |
|---------|-------|
| Total de notas | 4 |
| ⬜ pendente | 4 |
| ➖ não precisa | 0 |
| ✅ feita | 0 |
| % concluído | 0% |

> Diagnóstico concluído em 2026-07-02. Custo: 4 `[substantivo]` · 0 `[mecânico]`.

---

## Notas

#### 01 - Estrutura .claude lazy-load   [substantivo]
- **Enriquecimento:** ⬜ pendente
- **Estado:** 281 linhas reais · fase: Iniciado · status: growing
- **Núcleo/gaps:** M1 · piso de linhas (281 < 300 para fase Iniciado)
- **Score:** 11/12
- **Plano de execução:**
  - Buscar vídeo/podcast relevante sobre lazy-load de contexto no Claude Code e embutir callout `[!tip]` com link → ativa M1
  - Expandir levemente uma seção existente (ex. "Como medir o impacto" ou "Migração incremental") para superar o piso de 300 linhas da fase Iniciado → fecha gap de piso
- **Resultado:** —

#### 02 - Sandboxing de tool output   [substantivo]
- **Enriquecimento:** ⬜ pendente
- **Estado:** 348 linhas reais · fase: Adepto · status: growing
- **Núcleo/gaps:** linhas abaixo do piso Adepto (348<400) · L2 (seção chama "Referências", não "## Fontes") · M1 (sem [!tip] de vídeo/podcast)
- **Score:** 10/12
- **Plano de execução:**
  - Pesquisar e embutir vídeo/podcast relevante sobre PostToolUse hooks ou tool-output sandboxing → ativa M1 (também empurra linhas pro piso)
  - Renomear `## Referências` para `## Fontes` (conteúdo já qualifica) → resolve L2
  - Expandir um dos casos práticos ou adicionar variação de armadilha com mais detalhe técnico para atingir piso de 400 linhas → resolve gap de linhas
- **Resultado:** —

#### 03 - Indexação semântica externa   [substantivo]
- **Enriquecimento:** ⬜ pendente
- **Estado:** 428 linhas reais · fase: Magus · status: growing
- **Núcleo/gaps:** L2 (seção é `## Referências`, não `## Fontes`), M1 (sem vídeo/podcast `[!tip]`), abaixo do piso Magus (428 < 500)
- **Score:** 10/12
- **Plano de execução:**
  - Renomear `## Referências` para `## Fontes` (mantendo as URLs existentes) → ativa L2
  - Pesquisar e embutir 1 vídeo/podcast relevante sobre semantic search/RAG em codebase como `[!tip]` → ativa M1
  - Expandir conteúdo (ex.: mais detalhe em hybrid search, benchmarks de retrieval, ou caso prático adicional) até atingir piso de 500 linhas (fase Magus)
- **Resultado:** —

#### 04 - Knowledge graph local com AST   [substantivo]
- **Enriquecimento:** ⬜ pendente
- **Estado:** 478 linhas reais · fase: Magus · status: growing
- **Núcleo/gaps:** M1 (nenhum [!tip] com vídeo/podcast) · piso de linhas Magus (478 < 500)
- **Score:** 11/12
- **Plano de execução:**
  - Pesquisar vídeo/podcast relevante sobre knowledge graphs de código, blast-radius ou Tree-sitter e embutir como `[!tip]` → ativa M1
  - Expandir levemente uma seção existente (ex: mais detalhe em "Análises avançadas" ou um 4º caso prático) para superar o piso de 500 linhas da fase Magus → fecha gap de piso
- **Resultado:** —
