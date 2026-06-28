---
title: "Reranking — Cohere, Voyage, cross-encoders"
created: 2026-04-11
updated: 2026-05-02
type: concept
progress: backlog
status: seedling
publish: true
fase: Iniciado
tags:
  - rag
  - ia
  - reranking
aliases:
  - Reranking
  - Cross-encoder
  - Rerankers
  - Cohere Rerank
---

# Reranking — Cohere, Voyage, cross-encoders

> [!abstract] TL;DR
> Reranker é um modelo que **refina o ranking** dos top-N do retrieve. Diferente de [[Dicionário de IA#embedding|embeddings]] (bi-encoders, embedam query e doc separadamente), rerankers são **cross-encoders** — analisam query+doc juntos, com atenção total entre eles. Resultado: ranking muito mais preciso, ao custo de latência (cada par requer 1 forward pass). Padrão: [[Dicionário de IA#retrieval|retrieve]] top-50, [[Dicionário de IA#reranking|rerank]] → top-5. Modelos: Cohere Rerank (default), Voyage Rerank, BGE Reranker (open source). **Skip rerank = ruído no prompt.**

> [!question]- Por que reranker depois de vector search e não só vector search melhor?
> Um embedding melhor não resolve o problema estrutural: bi-encoders comprimem query e documento em vetores independentes — eles nunca "se veem" juntos. A distância cosseno mede similaridade global, não relevância específica para a pergunta. Um reranker cross-encoder processa `[query][SEP][documento]` como um par único, ativando atenção cruzada entre todos os tokens de ambos. Isso permite detectar que "Python suporta async" é mais relevante para "como fazer chamadas async em Python?" do que "Python é uma linguagem de alto nível" — mesmo que o segundo documento tenha embedding mais similar à query genérica. Melhorar o bi-encoder ajuda na margem; cross-encoder resolve a classe inteira de problema.

## Por que rerankers existem

Embeddings (bi-encoders):

```
Query  → encoder → vector_q
Doc    → encoder → vector_d
score = cosine(vector_q, vector_d)
```

Rápido, mas **encoders nunca se conhecem**. Vetores otimizados para approximate similarity, não relevância profunda.

Rerankers (cross-encoders):

```
[Query] [SEP] [Doc] → encoder → score
```

Query e doc **passam juntos** pelo encoder. Atenção total entre eles. Resultado: muito mais preciso, mas O(N) — precisa rodar uma vez por par.

## Trade-off explícito

| | Bi-encoder (embedding) | Cross-encoder (reranker) |
|---|---|---|
| **Latência por doc** | 0ms (pré-computado) | 50-200ms |
| **Precisão** | Boa | Excelente |
| **Escalabilidade** | Bilhões | Milhares |
| **Uso** | Top-50 do corpus | Top-5 do top-50 |

Pipeline ideal: bi-encoder filtra de 1M para 50; cross-encoder refina de 50 para 5.

## Modelos populares (2026)

| Reranker | Provider | Latência | Forte em |
|---|---|---|---|
| **Cohere Rerank 3** | Cohere API | 100-300ms | Default, multilingual |
| **Voyage Rerank-2** | Voyage AI | 100-300ms | Premium quality |
| **BGE Reranker v2-m3** | BAAI (open) | self-hosted | Open source forte |
| **Jina Reranker v2** | Jina AI | 100-300ms | Multilingual, multimodal |
| **MS MARCO** | Microsoft (open) | self-hosted | Baseline open source |

Default sensato em 2026: **Cohere Rerank** (API simples, qualidade alta) ou **BGE-Reranker-v2-m3** (self-hosted).

## Como usar — Cohere

```python
import cohere

co = cohere.Client(api_key="...")

response = co.rerank(
    model="rerank-3",
    query="user question",
    documents=[
        "doc 1 text...",
        "doc 2 text...",
        # ... up to 1000 docs
    ],
    top_n=5
)

# response.results: [{index: 2, relevance_score: 0.94}, ...]
final_docs = [docs[r.index] for r in response.results]
```

Custo: $1 / 1000 chamadas (1 chamada = 1 query + N docs). 100 docs por query: $1 / 100K queries. Barato.

## Como usar — BGE (self-hosted)

```python
from FlagEmbedding import FlagReranker

reranker = FlagReranker('BAAI/bge-reranker-v2-m3')

pairs = [(query, doc) for doc in candidates]
scores = reranker.compute_score(pairs)
ranked = sorted(zip(candidates, scores), key=lambda x: -x[1])[:5]
```

Custo: free (GPU), latência depende do hardware.

## Quando usar cada

```mermaid
graph TD
    A["Latência crítica<br/>(<500ms total)?"] -->|sim| B["Skip rerank<br/>ou rerank top-10"]
    A -->|não| C{"Self-hosted<br/>requirements?"}
    C -->|sim| D["BGE Reranker"]
    C -->|não| E{"Multilingual?"}
    E -->|sim| F["Cohere Rerank<br/>multilingual-v3"]
    E -->|não| G["Cohere Rerank-3<br/>(default)"]
```

## O ganho real

> [!example] Anthropic Contextual Retrieval (2024)
> Hybrid search (BM25 + vector) sozinho: 5.7% failed retrievals
> Hybrid + Reranker: 1.9% failed retrievals
> **Redução de 67%** apenas adicionando reranker.

Esse é o efeito típico em produção. Skip rerank = deixar dinheiro na mesa.

## Latência considerações

```
Top-50 docs × 200ms / doc = ~10s    ❌ inviável

Solução: batch
Top-50 docs em 1 batch call = 200-400ms total ✅
```

APIs (Cohere, Voyage) batcham automaticamente. Self-hosted: configure batch size.

## Filtragem antes de rerank

Para reduzir custo e latência, filtre **antes** do rerank:

```python
# 1. Hybrid retrieval — top-50
candidates = hybrid_retrieve(query, k=50)

# 2. Filter por relevance_score baixo (sinais óbvios de irrelevância)
filtered = [c for c in candidates if c.score > MIN_THRESHOLD]

# 3. Rerank apenas o que passou
top5 = rerank(query, filtered, top_n=5)
```

## Validação de threshold

Default: aceita top-N do reranker, sem threshold. Mas em produção:

```python
top5 = rerank(query, candidates, top_n=5)

# Se nem o top-1 tem boa relevância, devolve "não sei"
if top5[0].relevance_score < 0.6:
    return "Não encontrei informação relevante para sua pergunta."
```

Threshold típico: 0.5-0.7 (dependente do modelo).

## Reranker para multimodal

Modelos multimodais (Cohere Embed v4, Jina Reranker multimodal) ranqueiam pares **texto + imagem**. Útil em busca visual ou docs com diagramas.

## Métricas

| Métrica | Alvo |
|---|---|
| **NDCG@10** (após rerank) | >0.7 |
| **Precision@5** | >70% |
| **Latência rerank** | <500ms |
| **Cost rerank / total RAG** | <20% |
| **Threshold de "não sei"** | top-1 score <0.6 |

## Armadilhas comuns

> [!warning] Rerankar sem hybrid retrieve — garbage in, garbage out
> O reranker refina o ranking do top-50, mas não cria relevância do nada. Se o top-50 do vector search não contém os documentos certos (baixo recall), o reranker vai ordenar 50 documentos mediocres — e o melhor do lote ainda vai ser ruim. O padrão correto é hybrid retrieval primeiro (para maximizar recall no top-50), depois reranker (para maximizar precisão no top-5). Rerankar sem hybrid é otimizar a segunda etapa enquanto ignora a primeira.

> [!warning] Rerankar top-1000 por cautela
> Cada documento no batch de rerank custa uma forward pass de cross-encoder. Top-50 em uma chamada de API Cohere leva 200-400ms total. Top-1000 pode levar 4-8s e custa 20x mais — sem ganho proporcional, porque os documentos adicionais já teriam recall baixo do retrieval. O sweet spot empírico é rerankar top-50 a top-100. Se você sente que precisa de mais de 100 candidatos, o problema está no retrieval, não no reranker.

> [!warning] Sem threshold de relevância — força resposta mesmo quando não há informação
> Por padrão, o reranker retorna um score de relevância. Se o top-1 tem score 0.2 (muito baixo), forçar a geração de uma resposta com esse chunk quase certamente vai resultar em hallucination — o LLM vai complementar o que falta com conhecimento próprio. Defina um threshold (tipicamente 0.5-0.7 dependendo do modelo) e devolva "não encontrei informação relevante" quando nenhum chunk passa. Isso não é falha — é o comportamento correto de um sistema RAG honesto.

## Anti-patterns

- **Skip rerank em produção** — Anthropic mostrou 67% redução de failed retrievals
- **Rerank top-1000** — caro sem ganho marginal vs top-50
- **Sem threshold de relevância** — força resposta mesmo sem info
- **Rerankear sem hybrid retrieve** — top-50 vector ruim → rerank salva pouco
- **Reranker diferente do dataset de treino** — domain mismatch
- **Não validar reranker em golden set** — assume que qualquer reranker é melhor

## Como explicar em inglês

Reranking is the step that bridges high recall and high precision. After hybrid retrieval gives you a top-50 with good recall, the reranker reorders those 50 candidates using a fundamentally different model architecture. Bi-encoders (the ones that generate embeddings) encode query and document independently — they never interact. Cross-encoders process the query-document pair together, allowing full attention between every token in both. This makes them dramatically more accurate at judging relevance, at the cost of running once per pair instead of once per query.

The practical result is significant. Anthropic's Contextual Retrieval paper shows that adding a reranker after hybrid search reduces failed retrievals from 3.4% to 1.9% — a 44% improvement just from this single step. The cost is minimal: a batch call to Cohere Rerank for 50 documents takes 200-400ms and costs roughly $1 per 100,000 queries.

The architecture pattern is fixed: retrieve top-50 (for recall), rerank to top-5 (for precision), then pass only those 5 to the LLM. The reranker also provides relevance scores that enable a "I don't know" gate — if the top-1 score is below 0.6, the system returns a fallback instead of forcing a hallucinated answer.

**In a technical interview**, you might say:

> "I always add a reranker between retrieval and generation. The reason is architectural: vector embeddings encode query and document independently, so similarity score is an approximation of relevance. A cross-encoder like Cohere Rerank-3 processes the query and each candidate document as a pair, with full self-attention between them — it can reason about whether the document actually answers the question, not just whether it's topically similar. In production, I retrieve top-50 from hybrid search, rerank to top-5, and use the top-1 relevance score as a threshold gate: if it's below 0.6, I return 'I couldn't find relevant information' rather than risk a hallucinated answer."

| PT | EN |
|----|-----|
| reordenação | reranking |
| codificador cruzado | cross-encoder |
| codificador duplo | bi-encoder |
| pontuação de relevância | relevance score |
| passagem direta | forward pass |
| limiar de relevância | relevance threshold |
| recuperação em lote | batch retrieval |
| recuperações falhas | failed retrievals |
| precisão do topo | top-N precision |
| recall com reordenação | recall@N with reranking |

## O que vem a seguir

Depois de retrieval + rerank, você tem os 5 chunks mais relevantes para a pergunta. O trabalho não acabou — agora o desafio é transformar esses chunks em uma resposta confiável. Como estruturar o prompt para que o LLM cite as fontes? Como ordenar os chunks dentro do contexto para evitar o efeito "lost in the middle"? Como garantir que a resposta não invente informação além do que está nos trechos? A próxima nota cobre a etapa de geração — incluindo estrutura de prompt, padrões de citação e como tratar faithfulness em produção.

- [[08 - Generation — passar contexto ao LLM com citação]] — gerar resposta fiel com citações explícitas

## Veja também

- [[02 - Anatomia do pipeline RAG]]
- [[06 - Retrieval — hybrid search, BM25, query rewriting]]
- [[09 - Evaluation de RAG]]
- [[Anatomia dos LLMs|03 - A janela de contexto]]

## Referências

- **Anthropic** — *Contextual Retrieval* (2024)
- **Cohere** — *Rerank documentation* (2026)
- **Voyage AI** — *Reranker docs* (2026)
- **BGE** — *github.com/FlagOpen/FlagEmbedding* (2026)
- **Nogueira & Cho** — *Passage Re-ranking with BERT* (paper original cross-encoder, 2019)























































