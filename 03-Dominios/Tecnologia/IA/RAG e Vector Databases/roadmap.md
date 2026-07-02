---
title: "Roadmap — RAG e Vector Databases"
created: 2026-07-02
type: meta
publish: false
tags:
  - meta
  - roadmap
---

# Roadmap — RAG e Vector Databases

Diagnóstico migrado de guia/roadmap - ia.md (02/07).

**Galho:** `03-Dominios/Tecnologia/IA/RAG e Vector Databases`

> [!warning] Diagnóstico de 02/07 — pode estar defasado. Vários itens marcados ⬜ podem já ter sido enriquecidos depois; reconciliar com o estado real ao tratar o galho.

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
| Total de notas | 13 |
| ⬜ pendente | 12 |
| ➖ não precisa | 1 |
| ✅ feita | 0 |
| 🔄 em andamento | 0 |
| % concluído | 0% |

---

## Notas

#### 01 - O que é RAG e quando usar   [substantivo]
- **Enriquecimento:** ⬜ pendente
- **Estado:** 187 linhas reais · fase: Iniciado · status: seedling
- **Núcleo/gaps:** E2, L2
- **Score:** 9/12
- **Plano de execução:**
  - Expandir a nota para ≥300 linhas de conteúdo real (atualmente 187; as ~119 finais são branco)
  - Adicionar parágrafo de abertura com cenário/problema concreto antes de "## A definição operacional" (ex: engenheiro que recebe pergunta sobre documento interno e o LLM alucina por não ter acesso aos dados da empresa)
  - Adicionar URLs reais às referências (Pinecone Learn RAG, Anthropic Contextual Retrieval blog, Lewis et al. arXiv:2005.11401, Eugene Yan blog)
- **Resultado:** —

#### 02 - Anatomia do pipeline RAG   [substantivo]
- **Enriquecimento:** ⬜ pendente
- **Estado:** 244 linhas reais · fase: Iniciado · status: seedling
- **Núcleo/gaps:** E2, L2, P1
- **Score:** 9/12
- **Plano de execução:**
  - Adicionar parágrafo de abertura com cenário/problema antes de "## As duas fases" (ex: engenheiro com sistema RAG que responde errado — identifica que o retrieval trouxe chunks irrelevantes, não o LLM)
  - Adicionar URLs reais às referências (Anthropic Contextual Retrieval blog, Pinecone Learn RAG, LlamaIndex docs)
  - Expandir conteúdo para ≥300 linhas reais (gap ~56 linhas) — seção de debugging end-to-end ou caso prático completo de indexing + query com código
- **Resultado:** —

#### 03 - Embeddings — representação semântica   [substantivo]
- **Enriquecimento:** ⬜ pendente
- **Estado:** 228 linhas reais · fase: Iniciado · status: seedling
- **Núcleo/gaps:** E2, L2, P1
- **Score:** 10/12
- **Plano de execução:**
  - Adicionar parágrafo de abertura com problema/cenário antes de "## A intuição" (ex: busca semântica com LIKE no banco retornando resultados irrelevantes)
  - Adicionar URLs reais às referências (openai.com/docs/embeddings, voyageai.com/docs, cohere.com/docs/embed, MTEB leaderboard, arXiv 2004.04906 DPR)
  - Expandir conteúdo para ≥300 linhas reais (gap ~72 linhas) — seção "Avaliando embeddings" (MTEB × realidade do domínio, golden set) ou caso prático de escolha de modelo PT-BR
  - Adicionar menção a [[03 - Embeddings — do token ao vetor]] (Anatomia dos LLMs) em "Veja também" — fecha bridge cross-galho ausente
- **Resultado:** —

#### 04 - Chunking — onde 50% da qualidade vive   [substantivo]
- **Enriquecimento:** ⬜ pendente
- **Estado:** ~252 linhas reais · fase: Iniciado · status: seedling
- **Núcleo/gaps:** E2, L2
- **Score:** 8/12
- **Plano de execução:**
  - Adicionar parágrafo de abertura com cenário/problema antes de "## A regra de ouro" (ex: 100k docs indexados, queries voltam irrelevantes — culpa do chunking, não do embedding)
  - Adicionar URLs reais às referências (anthropic.com/research/contextual-retrieval, python.langchain.com/docs/text_splitters, docs.llamaindex.ai)
  - Expandir conteúdo para ≥300 linhas reais (gap ~48 linhas) — seção "Erros reais de chunking" com casos documentados ou aprofundamento do contextual chunking com snippet Anthropic API real
- **Resultado:** —

#### 05 - Vector databases — pgvector, Pinecone, Qdrant   [substantivo]
- **Enriquecimento:** ⬜ pendente
- **Estado:** 299 linhas reais (1 linha curta) · fase: Iniciado · status: seedling
- **Núcleo/gaps:** E2, P1, L2
- **Score:** 9/12
- **Plano de execução:**
  - Adicionar parágrafo de abertura com cenário/problema antes de "## O que vector DB faz" (ex: migração Pinecone→pgvector por já ter Postgres, ou confundir qualidade do vector DB com qualidade do RAG) — resolve piso e núcleo faltante
  - Converter referências de domínios em itálico para URLs clicáveis reais (github.com/pgvector/pgvector, docs.pinecone.io, qdrant.tech/documentation, weaviate.io/developers, ann-benchmarks.com)
  - Adicionar `[!warning]` de caducidade antes da tabela de custo (preços datados, $25-300/mês, mudam com frequência)
- **Resultado:** —

#### 06 - Retrieval — hybrid search, BM25, query rewriting   [mecânico]
- **Enriquecimento:** ⬜ pendente
- **Estado:** 306 linhas reais · fase: Iniciado · status: seedling
- **Núcleo/gaps:** E3, L2
- **Score:** 10/12
- **Plano de execução:**
  - Adicionar URLs clicáveis às 5 referências (Anthropic Contextual Retrieval 2024, HyDE arXiv 2212.10496, RRF Cormack 2009, Pinecone hybrid guide, BM25 Robertson 1994)
  - Opcional: adicionar Mermaid com flowchart do pipeline completo (rewrite → HyDE → hybrid top-50 → RRF → rerank → top-k)
- **Resultado:** —

#### 07 - Reranking — Cohere, Voyage, cross-encoders   [substantivo]
- **Enriquecimento:** ⬜ pendente
- **Estado:** 146 linhas reais · fase: Iniciado · status: seedling
- **Núcleo/gaps:** P1, L2
- **Score:** 10/12
- **Plano de execução:**
  - Expandir conteúdo para atingir piso de 300 linhas reais (gap ~154 linhas): aprofundar métricas com exemplos numéricos, seção sobre fine-tuning domain-specific de rerankers, expandir "Filtragem antes de rerank" com pipeline comentado
  - Adicionar URLs clicáveis às referências (Anthropic Contextual Retrieval: anthropic.com/news/contextual-retrieval; BGE: github.com/FlagOpen/FlagEmbedding)
  - Opcional: bloco de código com falha (rerank sem hybrid → garbage in, garbage out)
- **Resultado:** —

#### 08 - Generation — passar contexto ao LLM com citação   [substantivo]
- **Enriquecimento:** ⬜ pendente
- **Estado:** 352 linhas reais · fase: Iniciado · status: growing
- **Núcleo/gaps:** E2, E3, P1, L2
- **Score:** 8/12
- **Plano de execução:**
  - Adicionar parágrafo de abertura visível (não colapsável) antes de "## A estrutura do prompt" com cenário concreto de falha (chunks certos recuperados, mas resposta mistura contexto com conhecimento de treino sem avisar)
  - Adicionar URLs clicáveis às referências (Liu et al. arXiv 2307.03172, Asai et al. arXiv 2310.11511, Yan et al. arXiv 2401.15884, Anthropic Citations API)
  - Opcional: diagrama Mermaid (sequenceDiagram retrieve→rerank→extract→generate→verify)
- **Resultado:** —

#### 09 - Evaluation de RAG   [substantivo]
- **Enriquecimento:** ⬜ pendente
- **Estado:** 325 linhas reais · fase: Iniciado · status: seedling
- **Núcleo/gaps:** E2, L2
- **Score:** 10/12
- **Plano de execução:**
  - Adicionar parágrafo de abertura (2-3 frases) apresentando o cenário: RAG deployado com respostas boas em teste manual mas erros sutis em produção — sem saber se o problema é retrieval, reranking ou generation
  - Adicionar URLs completas às referências (docs.ragas.io, trulens.org, deepeval.com, arXiv 2309.15217 RAGAS, Eugene Yan)
- **Resultado:** —

#### 10 - RAG vs long context vs fine-tuning   [substantivo]
- **Enriquecimento:** ⬜ pendente
- **Estado:** 240 linhas reais · fase: Iniciado · status: seedling
- **Núcleo/gaps:** P1, L2
- **Score:** 10/12
- **Plano de execução:**
  - Adicionar URLs completas à seção "## Referências" (platform.openai.com/docs/guides/fine-tuning, docs.anthropic.com context-windows, eugeneyan.com, ai-engineering.ai)
  - Expandir corpo com ~65 linhas reais para atingir piso de 300: aprofundar "Híbridos" com fluxo passo-a-passo (escolha inicial → golden set → critérios de adição de componente) e [!question]- sobre híbrido prematuro como dívida técnica
- **Resultado:** —

#### 11 - Padrões avançados — Graph RAG, Agentic RAG, multi-hop   [mecânico]
- **Enriquecimento:** ➖ não precisa
- **Estado:** 341 linhas reais · fase: Iniciado · status: seedling
- **Núcleo/gaps:** P1
- **Score:** 11/12
- **Plano de execução:**
  - — nenhuma
- **Resultado:** —

#### 12 - Setup completo — checklist de produção   [substantivo]
- **Enriquecimento:** ⬜ pendente
- **Estado:** 339 linhas reais · fase: Iniciado · status: seedling
- **Núcleo/gaps:** E2, L2
- **Score:** 10/12
- **Plano de execução:**
  - Adicionar parágrafo de abertura com cenário/problema antes de "## Stack recomendada" (ex: RAG "funcionando em dev" que colapsa em produção por falta de fallback e evaluation)
  - Adicionar URLs reais às referências (Anthropic Contextual Retrieval blog, Eugene Yan blog, Pinecone production guide, Chip Huyen AI Engineering)
- **Resultado:** —

#### 13 - PageIndex — RAG vectorless por árvore de documentos   [substantivo]
- **Enriquecimento:** ⬜ pendente
- **Estado:** 174 linhas reais · fase: Iniciado · status: seedling / progress: backlog
- **Núcleo/gaps:** P1
- **Score:** 11/12
- **Plano de execução:**
  - Nota está 126 linhas abaixo do piso (≥300): expandir "## Como funciona" com exemplo de nó JSON real (title/node_id/start_index/end_index/summary/nodes) e detalhar "## Relação com padrões avançados" (Agentic RAG, Hierarchical retrieval, Long-context RAG) com diferencial concreto de cada
  - Atualizar `status: seedling` e `progress: backlog` para refletir o estado real da nota (conteúdo já maduro)
- **Resultado:** —
