---
title: "Setup completo — checklist de produção"
created: 2026-04-11
updated: 2026-05-06
type: concept
status: seedling
publish: true
tags:
  - rag
  - ia
  - setup
  - producao
aliases:
  - Setup RAG produção
  - Checklist RAG
  - RAG production
---

# Setup completo — checklist de produção

> [!abstract] TL;DR
> Esta nota fecha a trilha com o checklist end-to-end para colocar RAG em produção. Stack base: pgvector + Cohere Rerank + Sonnet + Ragas + Langfuse. Roadmap: 4 fases × 2 semanas. Saída: RAG funcional com observabilidade, evaluation em CI, fallback, citação obrigatória, custo previsível. Pular fases = retrabalho. **Investimento total: ~6-8 semanas part-time.**

## Stack recomendada (2026)

```
┌────────────────────────────────────────────────────────────┐
│  1. Parsing:        unstructured / Docling / pypdf         │
│  2. Chunking:       LangChain RecursiveCharacterTextSplitter│
│  3. Embedding:      OpenAI text-embedding-3-large          │
│  4. Vector DB:      pgvector (Postgres)                    │
│  5. Hybrid search:  pgvector + ts_vector (BM25)            │
│  6. Reranking:      Cohere Rerank-3                         │
│  7. Generation:     Anthropic Claude Sonnet 4.6            │
│  8. Evaluation:     Ragas + golden set                     │
│  9. Observability:  Langfuse                               │
│  10. Tracing:       OpenTelemetry                          │
└────────────────────────────────────────────────────────────┘
```

Custo total típico: **$50-200/mês** para 100K queries.

## Roadmap de 4 fases

```mermaid
gantt
    title Roadmap RAG em produção - 8 semanas
    dateFormat  YYYY-MM-DD
    section Fase 1
    Indexação básica          :a1, 2026-05-02, 14d
    section Fase 2
    Quality (rerank+rewrite)  :b1, after a1, 14d
    section Fase 3
    Evaluation + CI           :c1, after b1, 14d
    section Fase 4
    Produção + observabilidade :d1, after c1, 14d
```

## Fase 1 — Indexação básica (semanas 1-2)

**Objetivo:** ter RAG mínimo funcional.

### Checklist

- [ ] Coletar documentos representativos (start: 100-1000)
- [ ] Parser que extrai texto preservando estrutura
- [ ] Chunking recursivo (500-1000 tokens, 10% overlap)
- [ ] Validação manual de 10 amostras de chunks
- [ ] Postgres com extension `vector` instalada
- [ ] Schema com `chunks` table + `documents` table + metadata JSONB
- [ ] Index HNSW em embedding column
- [ ] Script de indexação idempotente
- [ ] Embedding via OpenAI text-embedding-3-large
- [ ] Top-k vector search funcionando
- [ ] Generation com Sonnet 4.6 + system prompt restritivo
- [ ] Citação `[N]` no output

### Saída esperada

Demo funcional. Performance ainda tosca, mas ciclo completo end-to-end.

## Fase 2 — Quality (semanas 3-4)

**Objetivo:** subir qualidade do retrieval.

### Checklist

- [ ] BM25 search (Postgres `ts_vector` ou Elasticsearch)
- [ ] Hybrid retrieval com Reciprocal Rank Fusion (RRF)
- [ ] Cohere Rerank em top-50 → top-5
- [ ] Query rewriting com LLM (system prompt curto, modelo barato)
- [ ] HyDE para queries vagas (opcional)
- [ ] Metadata filtering (data, tipo, tenant)
- [ ] Threshold de "não sei" baseado em rerank score
- [ ] Test manual de 20 queries em diferentes categorias

### Saída esperada

Recall@5 >70% em golden set. Citação correta >80%.

## Fase 3 — Evaluation + CI (semanas 5-6)

**Objetivo:** medir e prevenir regressão.

### Checklist

- [ ] Golden set de 50-100 queries com ground truth
- [ ] Ragas integrado: context_precision, recall, faithfulness, answer_relevance
- [ ] Categorias no golden set: factual, multi-hop, out-of-scope, adversarial
- [ ] Pipeline CI roda eval em PRs que tocam RAG
- [ ] Threshold mínimo bloqueia merge
- [ ] LLM-as-judge para faithfulness (Claude Opus ou GPT-5)
- [ ] Validação automática de citation accuracy
- [ ] Test de "out-of-scope": RAG diz "não sei" quando deveria
- [ ] Comparação A/B entre versões em ambiente staging

### Saída esperada

Eval automatizado funcionando. Métricas baseline registradas.

## Fase 4 — Produção (semanas 7-8)

**Objetivo:** deploy seguro com observabilidade.

### Checklist

- [ ] Langfuse integrado (trace de cada query)
- [ ] Dashboard: latência p95, cost/query, error rate, faithfulness
- [ ] Rate limiting per user
- [ ] Retry com backoff em falha de provider
- [ ] Fallback: se Cohere Rerank fail, segue sem rerank com warning
- [ ] Streaming response no frontend
- [ ] Citações clicáveis na UI
- [ ] Log estruturado: query, retrieved IDs, response, user_feedback
- [ ] Mecanismo de feedback (thumbs up/down)
- [ ] A/B test infra (variantes de prompt/modelo)
- [ ] Alert se faithfulness cair >5% em 24h
- [ ] Documentação operacional (runbook)
- [ ] Plan de re-indexação (semanal? on-change?)

### Saída esperada

RAG em produção com confiança. Time consegue debugar via Langfuse.

## Configuração-modelo (pgvector)

```sql
-- Extensão
CREATE EXTENSION IF NOT EXISTS vector;
CREATE EXTENSION IF NOT EXISTS pg_trgm;

-- Tabelas
CREATE TABLE documents (
    id BIGSERIAL PRIMARY KEY,
    source TEXT NOT NULL,
    title TEXT,
    metadata JSONB,
    indexed_at TIMESTAMPTZ DEFAULT NOW(),
    UNIQUE(source)
);

CREATE TABLE chunks (
    id BIGSERIAL PRIMARY KEY,
    doc_id BIGINT REFERENCES documents(id) ON DELETE CASCADE,
    text TEXT NOT NULL,
    text_search tsvector GENERATED ALWAYS AS (to_tsvector('portuguese', text)) STORED,
    embedding VECTOR(1536) NOT NULL,
    metadata JSONB,
    chunk_index INT,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- Índices
CREATE INDEX idx_chunks_embedding ON chunks USING hnsw (embedding vector_cosine_ops);
CREATE INDEX idx_chunks_text ON chunks USING gin(text_search);
CREATE INDEX idx_chunks_doc_id ON chunks(doc_id);
CREATE INDEX idx_chunks_metadata ON chunks USING gin(metadata);
CREATE INDEX idx_documents_metadata ON documents USING gin(metadata);
```

## Hybrid retrieval (SQL)

```sql
WITH vector_search AS (
    SELECT
        id, text, doc_id, metadata,
        1 - (embedding <=> $1::vector) AS vector_score,
        ROW_NUMBER() OVER (ORDER BY embedding <=> $1::vector) AS vector_rank
    FROM chunks
    WHERE metadata @> $2  -- filter
    ORDER BY embedding <=> $1::vector
    LIMIT 50
),
bm25_search AS (
    SELECT
        id, text, doc_id, metadata,
        ts_rank(text_search, plainto_tsquery('portuguese', $3)) AS bm25_score,
        ROW_NUMBER() OVER (ORDER BY ts_rank(text_search, plainto_tsquery('portuguese', $3)) DESC) AS bm25_rank
    FROM chunks
    WHERE text_search @@ plainto_tsquery('portuguese', $3)
    LIMIT 50
)
SELECT
    COALESCE(v.id, b.id) AS id,
    COALESCE(v.text, b.text) AS text,
    -- RRF: 1/(60+rank)
    COALESCE(1.0 / (60 + v.vector_rank), 0) +
    COALESCE(1.0 / (60 + b.bm25_rank), 0) AS rrf_score
FROM vector_search v
FULL OUTER JOIN bm25_search b ON v.id = b.id
ORDER BY rrf_score DESC
LIMIT 50;
```

## Pipeline em código (Python)

```python
async def rag_query(question: str, user_id: str, filters: dict = None):
    # 1. Rewrite (opcional)
    rewritten = await rewrite_query(question)

    # 2. Embed
    query_emb = await embed(rewritten)

    # 3. Hybrid retrieval (top-50)
    candidates = await hybrid_search(query_emb, rewritten, filters or {}, k=50)

    # 4. Rerank (top-5)
    top_chunks = await cohere_rerank(rewritten, candidates, top_n=5)

    # 5. Threshold de "não sei"
    if top_chunks[0].relevance_score < 0.5:
        return RAGResponse(
            answer="Não encontrei essa informação na base.",
            sources=[],
            confidence="low"
        )

    # 6. Generate
    answer = await generate_with_citations(question, top_chunks)

    # 7. Log to Langfuse
    log_trace(user_id, question, top_chunks, answer)

    return answer
```

## Métricas-alvo de produção

| Métrica | Alvo |
|---|---|
| **Latência p95** | <3s |
| **Cost por query** | <$0.01 |
| **Faithfulness** | >0.9 |
| **Context precision** | >0.7 |
| **Citation accuracy** | >0.95 |
| **% "não sei" apropriado** | >70% das out-of-scope |
| **User feedback (thumbs up rate)** | >75% |

## Quando subir para padrões avançados

Sinais que indicam mudança ([[11 - Padrões avançados — Graph RAG, Agentic RAG, multi-hop|11 - Padrões avançados]]):

- Multi-hop queries falhando consistentemente → Multi-hop ou Agentic
- Domínio com entidades fortes → Graph RAG
- Queries muito variáveis em complexidade → Agentic com fallback
- Documentos longos estruturados e chunking ruim → PageIndex / Tree RAG

## Anti-patterns no setup

- **Pular Fase 3** — produção sem evaluation = caixa preta
- **Sem fallback de Cohere** — provider down = RAG down
- **Sem rate limit per user** — abuse mata budget
- **Sem feedback loop** — não sabe o que melhorar
- **Re-indexação manual** — inconsistência inevitável
- **Mesmo embedding model em domínios diferentes** — qualidade desigual
- **Cost dashboard "depois"** — descoberta de gasto alto = surpresa

## Veja também

- [[01 - O que é RAG e quando usar]] — começo da trilha
- [[09 - Evaluation de RAG]]
- [[11 - Padrões avançados — Graph RAG, Agentic RAG, multi-hop]]
- [[13 - PageIndex — RAG vectorless por árvore de documentos]]
- [[Economia de Tokens|18 - Playbook de economia — checklist completo]]
- [[Segurança e Guardrails|07 - Security-focused prompting]]

## Referências

- **Anthropic** — *Contextual Retrieval* (2024) — best practices end-to-end
- **Eugene Yan** — *RAG patterns* (2024)
- **Pinecone** — *Production RAG guide* (2026)
- **Chip Huyen** — *AI Engineering* (2025)
