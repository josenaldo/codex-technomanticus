---
title: "Retrieval — hybrid search, BM25, query rewriting"
created: 2026-04-11
updated: 2026-07-06
type: concept
progress: backlog
status: seedling
publish: true
fase: iniciado
tags:
  - rag
  - ia
  - retrieval
aliases:
  - Retrieval
  - Hybrid search
  - BM25
  - Query rewriting
  - HyDE
---

# Retrieval — hybrid search, BM25, query rewriting

> [!abstract] TL;DR
> Pure vector search é o **default ingênuo**. Em produção, ninguém ganha. Padrão profissional em 2026: **[[Dicionário de IA#hybrid search|hybrid search]] ([[Dicionário de IA#BM25|BM25]] + vector) + query rewriting + [[Dicionário de IA#reranking|reranking]]**. BM25 pega exact match (nomes, IDs, termos técnicos); vector pega semântica. Combinados via Reciprocal Rank Fusion (RRF). Query rewriting (incluindo HyDE) transforma a pergunta do usuário em queries melhores. Pesquisa mostra: hybrid bate pure vector em ~95% dos casos.

> [!question]- Por que hybrid search (BM25 + vector) e não só vector search melhor?
> Vector search resolve um problema de semântica — "o quê o usuário quer dizer?" — mas falha em um problema diferente: "o usuário quer exatamente essa palavra". Um embedding de "CPF-123-456" e "CPF-123-457" vai ser quase idêntico porque os modelos generalizam padrões semânticos. BM25 trata cada token como símbolo, não significado — encontra "CPF-123-456" onde ele aparece literalmente. Hybrid não é sobre ter vector "melhor"; é sobre usar a ferramenta certa para cada tipo de query. RRF combina os dois rankings sem precisar calibrar pesos.

## Por que pure vector falha

Vector [[Dicionário de IA#embedding|embeddings]] perdem em casos específicos:

| Caso | Por que vector falha |
|---|---|
| Nome próprio | "Maria Silva" e "Maria Souza" embedam parecido |
| ID, código | "ABC-123" não tem semântica útil |
| Termo técnico raro | Embedding genérico não captura |
| Negação | "não suporta X" e "suporta X" embedam similar |
| Match exato | Usuário quer **a palavra exata**, embedding aproxima |

BM25 (variante do TF-IDF) ganha em todos esses. Vector ganha em queries semânticas, sinônimos, paráfrases.

**Hybrid usa os dois.**

## BM25 em 30 segundos

Algoritmo clássico de information retrieval:

```
score(doc, query) = sum_for_each_term_in_query(
    IDF(term) × (TF(term, doc) × (k1 + 1)) / (TF(term, doc) + k1 × (1 - b + b × |doc| / avg_dl))
)
```

Não precisa entender a fórmula — entender que:
- **TF**: quantas vezes o termo aparece no doc
- **IDF**: termos raros valem mais
- **k1, b**: parâmetros (defaults k1=1.2, b=0.75)

**Implementação:** Elasticsearch, OpenSearch, Postgres `ts_vector`, ou rank_bm25 (Python).

## Hybrid search — combinando BM25 e vector

Duas abordagens:

### 1. Reciprocal Rank Fusion (RRF) — recomendado

```python
def rrf(rankings, k=60):
    """rankings: lista de listas com IDs ordenados por relevância"""
    scores = {}
    for ranking in rankings:
        for rank, doc_id in enumerate(ranking):
            scores[doc_id] = scores.get(doc_id, 0) + 1 / (k + rank + 1)
    return sorted(scores.items(), key=lambda x: -x[1])

# Uso
vector_top50 = vector_search(query)        # IDs ordenados por similarity
bm25_top50 = bm25_search(query)            # IDs ordenados por BM25
final = rrf([vector_top50, bm25_top50])    # combinação
```

Vantagem: **sem tunar pesos**. RRF é robusto, funciona out-of-the-box.

### 2. Weighted score — alternativa

```python
def weighted_score(doc, query, alpha=0.5):
    return alpha * vector_score(doc, query) + (1 - alpha) * bm25_score(doc, query)
```

Vantagem: tunável. Desvantagem: scores em escalas diferentes (vector 0-1, BM25 sem limite) → precisa normalizar. Difícil acertar `alpha`.

## Query rewriting — pergunta ≠ query ótima

Pergunta do usuário tipicamente:
- Tem typos
- Usa pronomes ("isso", "ele")
- É vaga ("como faço aquilo?")
- Mistura múltiplas perguntas

Técnicas para melhorar:

### 1. LLM-based rewrite

```python
prompt = f"""
Reescreva a pergunta abaixo como uma query de busca melhor.
Substitua pronomes por substantivos. Remova ambiguidade.

Pergunta: {user_question}
Query: """

rewritten = llm.complete(prompt)
results = retrieve(rewritten)
```

### 2. HyDE (Hypothetical Document Embeddings)

Em vez de embedar a **pergunta**, gera uma **resposta hipotética** e embeda essa.

```python
prompt = f"""
Imagine que você está respondendo a pergunta abaixo.
Escreva 1 parágrafo respondendo (mesmo que invente).

Pergunta: {user_question}
Resposta: """

hypothetical = llm.complete(prompt)
results = retrieve(embed(hypothetical))  # embed da resposta, não pergunta
```

Razão: respostas geralmente são **mais similares** a docs relevantes do que perguntas. Funciona bem em queries abertas.

### 3. Multi-query

Gera N queries variantes e une os resultados:

```python
prompt = "Gere 3 queries diferentes para a pergunta abaixo..."
queries = llm.complete(prompt)
all_results = []
for q in queries:
    all_results.append(retrieve(q))
final = rrf(all_results)
```

Vantagem: cobre formulações diferentes. Custo: 3-5x embedding queries.

### 4. Subquestion decomposition

Pergunta complexa → várias simples:

```
"Como o produto X se compara com Y em performance e custo?"
                    ↓
- "Performance do produto X"
- "Custo do produto X"
- "Performance do produto Y"
- "Custo do produto Y"
```

Útil em multi-hop. Custo: N retrievals + sintetizador final.

## Metadata filtering

Reduzir espaço de busca **antes** de retrieve:

```sql
SELECT * FROM chunks
WHERE doc_date > '2026-01-01'
  AND lang = 'pt-br'
  AND doc_type = 'manual'
ORDER BY embedding <=> query_embedding
LIMIT 50;
```

Vantagens:
- Reduz custo de search
- Melhor recall em filtros disjuntos
- Permite **multi-tenancy** (filtrar por user_id)

Indexar metadata frequentemente filtrada (B-tree em Postgres, payload index em Qdrant).

## Top-k — quanto pegar

```
Retrieve top-50 → Rerank → top-5 ao prompt
```

Por quê:

- **Top-5 do [[Dicionário de IA#retrieval|retrieval]] direto** perde recall
- **Top-50 reraqueado** combina recall (do top-50) com precision (do reranker)
- **Top-50 sem rerank** mete ruído no prompt

Default: retrieve 50, rerank para 5-10.

## Pipeline ideal — exemplo

```mermaid
flowchart LR
    A["Pergunta do usuário"] --> B["Rewrite (LLM)"]
    B --> C["HyDE (resposta hipotética)"]
    C --> D["Vector search top-50"]
    B --> E["BM25 search top-50"]
    D --> F["RRF (fusão de rankings)"]
    E --> F
    F --> G["Rerank"]
    G --> H["Top-k final ao prompt"]
```

```python
def retrieve_with_quality(user_question, k=5):
    # 1. Rewrite
    rewritten = rewrite_with_llm(user_question)

    # 2. HyDE (opcional)
    hypothetical = generate_hypothetical(rewritten)

    # 3. Hybrid retrieval — top-50 cada
    vector_top50 = vector_search(embed(hypothetical), k=50)
    bm25_top50 = bm25_search(rewritten, k=50)

    # 4. RRF
    fused = rrf([vector_top50, bm25_top50])  # ~70-80 únicos

    # 5. Rerank
    top_k = rerank(rewritten, fused[:50])[:k]  # ver [[07 - Reranking]]

    return top_k
```

Latência total: ~500-1500ms.

## Quando NÃO precisa de hybrid

- Domínio sem termos técnicos / nomes / IDs
- Volume muito alto + custo crítico (BM25 adiciona ~50ms)
- Já tem ranking sinal forte (votos, recência)

## Métricas

| Métrica | Alvo |
|---|---|
| **Recall@50 (retrieval)** | >90% |
| **Latência retrieval** (hybrid + rewrite) | <500ms |
| **Cost por query** | <$0.001 |
| **% queries com rewrite que mudou top-k** | 20-50% |

## Armadilhas comuns

> [!warning] Usar HyDE em domínio que o LLM não conhece
> HyDE funciona gerando uma "resposta hipotética" para a pergunta e buscando por ela. O truque assume que o LLM tem conhecimento suficiente para gerar algo próximo do documento real. Em domínios muito específicos (termos proprietários, legislação local, sistemas internos), o LLM gera hipótese vaga ou incorreta — e a busca retorna ruído. Valide HyDE com recall@10 antes de usar em produção; se não bater baseline, use multi-query em vez de HyDE.

> [!warning] Tunar o parâmetro alpha do weighted score sem golden set
> `alpha = 0.5 * vector + 0.5 * bm25` parece equilibrado, mas BM25 e similaridade vetorial vivem em escalas diferentes (BM25 pode chegar a 20+, vector vai de 0 a 1). Sem normalização e sem um golden set para medir qual `alpha` melhora o recall, você está girando um botão às cegas. Prefira RRF: ele é parâmetro-free, robusto e geralmente bate weighted score sem calibração.

> [!warning] Aplicar query rewriting em queries simples — adiciona latência sem ganho
> Reescrever "o que é HNSW?" com um LLM vai provavelmente devolver "o que é HNSW?" reformulado — custo de 50-200ms de LLM para zero ganho. Reserve query rewriting para casos onde há pronomes anafóricos ("ele disse isso antes"), ambiguidade real ou perguntas muito vagas. Uma heurística simples: se a query tem mais de 10 tokens e usa pronomes, reescreva; abaixo disso, vá direto para o retrieval.

## Anti-patterns

- **Pure vector em produção** — perde em ~30% dos casos
- **Tunar `alpha` sem validar** — RRF é mais robusto
- **Query rewriting sempre** — em queries simples, adiciona latência sem ganho
- **HyDE em domínio onde modelo não tem conhecimento** — gera hipótese ruim
- **Sem metadata filtering** — busca em corpus inteiro quando podia filtrar 90%
- **Top-k = 5 sem rerank** — perde recall

## Como explicar em inglês

Retrieval is the step that determines which chunks the LLM will actually see. Pure vector search is the intuitive starting point — embed the question, find the most similar chunks — but it has a structural blind spot: semantic similarity is not the same as lexical relevance. A user searching for "Invoice #A-2024-007" gets poor results from vector search because the embedding model collapses numeric identifiers into similar representations. BM25 treats each token as a literal symbol, so exact matches score high regardless of semantic proximity.

Hybrid search combines both signals: vector for semantic intent and BM25 for exact-match recall. Reciprocal Rank Fusion is the standard way to merge the two ranked lists — it rewards documents that appear high in both rankings without requiring you to normalize incompatible score scales. The result is consistently better than either approach alone, with the Anthropic Contextual Retrieval paper showing hybrid reduces failed retrievals from 5.7% to 3.4% before even adding a reranker.

Query rewriting adds another layer: the user's raw question is often suboptimal as a search query. Pronoun resolution, typo correction, and HyDE (generating a hypothetical answer and searching for that) all improve retrieval quality. The cost is extra LLM calls, so the tradeoff depends on query complexity and latency budget.

**In a technical interview**, you might say:

> "In production RAG, I always use hybrid search — BM25 combined with vector search via Reciprocal Rank Fusion. Pure vector search fails on a predictable class of queries: proper nouns, product codes, version numbers, anything where the exact string matters. BM25 handles those perfectly. I use RRF to merge the rankings because it's robust without needing to tune weights — documents that rank high in both signals rise to the top naturally. On top of that, I add query rewriting for long or ambiguous queries and always retrieve top-50 to feed into a reranker rather than sending top-5 directly to the LLM."

| PT | EN |
|----|-----|
| busca híbrida | hybrid search |
| fusão de ranking recíproca | Reciprocal Rank Fusion (RRF) |
| reescrita de query | query rewriting |
| frequência de termos | term frequency (TF) |
| frequência inversa de documentos | inverse document frequency (IDF) |
| documento hipotético | hypothetical document (HyDE) |
| múltiplas queries | multi-query |
| filtro por metadados | metadata filtering |
| decomposição de subperguntas | subquestion decomposition |
| recuperação semântica | semantic retrieval |

## O que vem a seguir

Hybrid search com RRF entrega um top-50 de candidatos bem combinados — mas candidatos ainda não são a resposta final. O problema é que o retrieval otimiza para recall (trazer o máximo de material relevante), e o LLM precisa do inverso: poucos chunks, altamente precisos. A ponte entre recall alto e precisão alta é o reranking. A próxima nota explica por que cross-encoders fazem um trabalho que bi-encoders estruturalmente não conseguem, e como Cohere Rerank corta o top-50 em top-5 com 67% menos erros de retrieval.

- [[07 - Reranking — Cohere, Voyage, cross-encoders]] — refinar ranking do top-50 com cross-encoders

## Veja também

- [[02 - Anatomia do pipeline RAG]]
- [[05 - Vector databases — pgvector, Pinecone, Qdrant]]
- [[07 - Reranking — Cohere, Voyage, cross-encoders]]
- [[09 - Evaluation de RAG]]

## Referências

- **Anthropic** — [*Contextual Retrieval*](https://www.anthropic.com/news/contextual-retrieval) (2024)
- **Gao et al.** — [*HyDE: Precise Zero-Shot Dense Retrieval without Relevance Labels*](https://arxiv.org/abs/2212.10496) (arXiv:2212.10496, 2022)
- **Cormack et al.** — [*Reciprocal Rank Fusion outperforms Condorcet and Individual Rank Learning Methods*](https://plg.uwaterloo.ca/~gvcormac/cormacksigir09-rrf.pdf) (2009)
- **Pinecone** — [*Hybrid search guide*](https://www.pinecone.io/learn/hybrid-search-intro/) (2026)
- **Robertson & Walker** — [*Some Simple Effective Approximations to the 2-Poisson Model for Probabilistic Weighted Retrieval*](https://dl.acm.org/doi/10.1145/188490.188561) (BM25 paper, 1994)
