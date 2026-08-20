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

Diagnóstico nota a nota. Cada entrada tem estado de enriquecimento, score, classificação de custo e plano de execução acionável. Gerado por `/diagnosticar-galho`.

**Galho:** `03-Dominios/Tecnologia/IA/Claude Code/Workflows/11 - Estratégias estruturais de contexto` **Nível:** galho-folha **Diagnóstico:** 2026-07-02 **Última execução:** 2026-07-08 (onda única: 4/4 notas enriquecidas via fan-out ≤3 verificado)

## Régua de análise

Checklist `verificar-nota` — 12 itens (isenções por fase/tipo/broto aplicadas por nota):

| Grupo | Itens |
|-------|-------|
| ESTRUTURA | E1 TL;DR · E2 Abertura-problema · E3 Mermaid · E4 Casos práticos · E5 O que vem a seguir · E6 Inglês · E7 Tabela PT↔EN · E8 Armadilhas [!warning] |
| PROFUNDIDADE | P1 Código-com-falha · P2 Mecanismo explicado |
| LINKS | L1 Wikilink cross-galho · L2 Referência externa (URL) |
| MÍDIA | M1 Vídeo/podcast embutido |

**Esquema de `fase:` detectado:** COM fase (Iniciado/Adepto/Magus) **Piso de linhas:** Iniciado ≥300 · Adepto ≥400 · Magus ≥500

## Tabela-resumo

| Métrica | Valor |
|---------|-------|
| Total de notas | 4 |
| ⬜ pendente | 0 |
| ➖ não precisa | 0 |
| ✅ feita | 4 |
| % concluído | 100% |

> Sub-galho **completo em 2026-07-08** (4/4 enriquecidas via fan-out ≤3 verificado). Custo: 4 `[substantivo]` · 0 `[mecânico]`.

---

## Notas

#### 01 - Estrutura .claude lazy-load   [substantivo]
- **Enriquecimento:** ✅ feita (2026-07-08)
- **Estado:** 281 linhas reais · fase: Iniciado · status: growing
- **Núcleo/gaps:** M1 · piso de linhas (281 < 300 para fase Iniciado)
- **Score:** 11/12
- **Plano de execução:**
  - Buscar vídeo/podcast relevante sobre lazy-load de contexto no Claude Code e embutir callout `[!tip]` com link → ativa M1
  - Expandir levemente uma seção existente (ex. "Como medir o impacto" ou "Migração incremental") para superar o piso de 300 linhas da fase Iniciado → fecha gap de piso
- **Resultado:** M1 (vídeo "Make Claude Code 100x BETTER (Context Engineering)") em "Como medir o impacto" + docs oficiais nas Referências. Expandidas "Como medir o impacto" e "Migração incremental" (Passo 6). 281→301 linhas reais (piso Iniciado ✓). DESVIO menor: não há vídeo específico só de lazy-load `.claude`/`.claudeignore`; usado o de context engineering mais próximo, justificado no callout.

#### 02 - Sandboxing de tool output   [substantivo]
- **Enriquecimento:** ✅ feita (2026-07-08)
- **Estado:** 348 linhas reais · fase: Adepto · status: growing
- **Núcleo/gaps:** linhas abaixo do piso Adepto (348<400) · L2 (seção chama "Referências", não "## Fontes") · M1 (sem [!tip] de vídeo/podcast)
- **Score:** 10/12
- **Plano de execução:**
  - Pesquisar e embutir vídeo/podcast relevante sobre PostToolUse hooks ou tool-output sandboxing → ativa M1 (também empurra linhas pro piso)
  - Renomear `## Referências` para `## Fontes` (conteúdo já qualifica) → resolve L2
  - Expandir um dos casos práticos ou adicionar variação de armadilha com mais detalhe técnico para atingir piso de 400 linhas → resolve gap de linhas
- **Resultado:** L2 (Referências→Fontes). M1 (vídeo "Claude Code Hooks Tutorial: PostToolUse Hook to Clean and Summarize Tool Output"). Expandido com detalhe técnico real (FTS5/BM25/query SQL nos Casos 1-3, 5ª armadilha handle-vs-processo, conta de tokens); 348→400 linhas reais (piso Adepto ✓). Sem desvios.

#### 03 - Indexação semântica externa   [substantivo]
- **Enriquecimento:** ✅ feita (2026-07-08)
- **Estado:** 428 linhas reais · fase: Magus · status: growing
- **Núcleo/gaps:** L2 (seção é `## Referências`, não `## Fontes`), M1 (sem vídeo/podcast `[!tip]`), abaixo do piso Magus (428 < 500)
- **Score:** 10/12
- **Plano de execução:**
  - Renomear `## Referências` para `## Fontes` (mantendo as URLs existentes) → ativa L2
  - Pesquisar e embutir 1 vídeo/podcast relevante sobre semantic search/RAG em codebase como `[!tip]` → ativa M1
  - Expandir conteúdo (ex.: mais detalhe em hybrid search, benchmarks de retrieval, ou caso prático adicional) até atingir piso de 500 linhas (fase Magus)
- **Resultado:** L2 (Referências→Fontes + 2 fontes novas). M1 (vídeo CocoIndex "build codebase indexing for RAG and semantic search"). Expansão: RRF em hybrid search, seção nova "Benchmarks de retrieval em código" (CodeSearchNet/MRR), 4º caso prático (onboarding júnior); podadas ~74 linhas de padding. 428→500 linhas (piso Magus ✓). Score 12/12. Sem desvios.

#### 04 - Knowledge graph local com AST   [substantivo]
- **Enriquecimento:** ✅ feita (2026-07-08)
- **Estado:** 478 linhas reais · fase: Magus · status: growing
- **Núcleo/gaps:** M1 (nenhum [!tip] com vídeo/podcast) · piso de linhas Magus (478 < 500)
- **Score:** 11/12
- **Plano de execução:**
  - Pesquisar vídeo/podcast relevante sobre knowledge graphs de código, blast-radius ou Tree-sitter e embutir como `[!tip]` → ativa M1
  - Expandir levemente uma seção existente (ex: mais detalhe em "Análises avançadas" ou um 4º caso prático) para superar o piso de 500 linhas da fase Magus → fecha gap de piso
- **Resultado:** M1 (podcast "KiroGraph: How a Local Code Graph Saves 80% of Your AI Tokens", AWS Developers Podcast). Expansão: subseção "Detecção de dependências circulares" (Tarjan SCC) em Análises avançadas. 478→510 linhas reais (piso Magus ✓). Score 12/12. Sem desvios.
