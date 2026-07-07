---
title: "Chunking — onde 50% da qualidade vive"
created: 2026-04-11
updated: 2026-07-06
type: concept
progress: in_progress
status: growing
publish: true
fase: Iniciado
tags:
  - rag
  - ia
  - chunking
aliases:
  - Chunking
  - Chunking strategies
  - Text splitting
---

# Chunking — onde 50% da qualidade vive

> [!abstract] TL;DR
> Chunks ruins = [[Dicionário de IA#RAG (Retrieval-Augmented Generation)|RAG]] ruim, sem recuperação possível. **[[Dicionário de IA#chunking|Chunking]] é onde 50% da qualidade vive** — vector DB é commodity, [[Dicionário de IA#embedding|embeddings]] são commodity, [[Dicionário de IA#retrieval|retrieval]] algorithms são commodity. Como você quebra o texto define o que vai ser encontrado. Estratégias do mais simples ao mais sofisticado: fixed size, recursive, semantic, structure-aware, contextual chunks (Anthropic 2024). Default razoável: 512-1024 tokens com 10-20% overlap, structure-aware quando possível. **Investigue chunks gerados antes de seguir** — visualize amostras, valide manualmente.

> [!question]- Por que chunking impacta mais a qualidade que o modelo de embedding?
> O modelo de embedding recebe um chunk e o projeta no espaço vetorial da melhor forma possível — mas não tem como recuperar informação que não está no chunk. Se uma tabela foi quebrada ao meio, o embedding vai representar fielmente... metade de uma tabela. Um modelo de embedding ruim com chunks perfeitos ainda retorna resultados usáveis; um modelo excelente com chunks fragmentados produz vetores tecnicamente corretos de contextos sem sentido. O "garbage in, garbage out" se aplica literalmente: a qualidade do embedding é limitada pela qualidade do input.

Imagine o cenário: 100 mil documentos indexados, embedding model de ponta, vector DB configurado com HNSW afinado — e mesmo assim as queries voltam com top-k irrelevante. O time revisa o modelo de embedding, troca de provider, ajusta parâmetros de busca... e o problema persiste. Na maioria dos casos, a causa não está em nenhuma dessas camadas: está em como o texto foi fragmentado antes de tudo isso acontecer. Um chunk que corta uma tabela ao meio, ou que separa uma resposta do parágrafo que dá contexto a ela, gera um vetor "correto" — matematicamente fiel ao que está ali — mas semanticamente inútil, porque o que está ali é metade de uma ideia.

## A regra de ouro

> *"Garbage in, garbage out."*

Chunks gerados mal:

- Frases cortadas no meio
- Tabela quebrada com header em outro chunk
- Código fragmentado
- Citação separada da fonte

Vetores estatisticamente similares ao significado **errado** = top-k irrelevante.

## As 5 estratégias

### 1. Fixed-size chunking

```python
def fixed_chunk(text, size=500, overlap=50):
    chunks = []
    for i in range(0, len(text), size - overlap):
        chunks.append(text[i:i + size])
    return chunks
```

- **Prós:** simples, rápido
- **Contras:** corta no meio de tudo (sentenças, parágrafos, código)
- **Quando usar:** baseline, prototipos, textos uniformes
- **Default:** 500-1000 tokens com 10% overlap

### 2. Recursive chunking

Tenta partir em separadores hierárquicos: `

` → `
` → `. ` → ` `.

```python
from langchain.text_splitter import RecursiveCharacterTextSplitter

splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000,
    chunk_overlap=100,
    separators=["

", "
", ". ", " "]
)
chunks = splitter.split_text(text)
```

- **Prós:** respeita estrutura natural
- **Contras:** ainda quebra entre seções relacionadas
- **Quando usar:** **default sensato em 80% dos casos**

### 3. Semantic chunking

Embeda sentenças e quebra onde a similaridade cai.

```python
# Pseudo-code
sentences = split_sentences(text)
embeddings = embed_each(sentences)
# Quebrar onde cosine similarity entre sentenças adjacentes <0.7
```

- **Prós:** chunks mais coerentes semanticamente
- **Contras:** caro (embed cada sentença), pode ser instável
- **Quando usar:** documentos com tópicos misturados

Tools: `semantic-chunkers` (LangChain), `LlamaIndex SemanticSplitter`.

### 4. Structure-aware chunking

Aproveita estrutura do documento: headers Markdown, sections HTML, classes CSS, etc.

```python
# Markdown
chunks = split_by_markdown_headers(text, levels=[1, 2, 3])

# Code
chunks = split_by_function_or_class(code)

# HTML
chunks = split_by_html_sections(html)
```

- **Prós:** preserva contexto natural; cada chunk é unidade lógica
- **Contras:** depende de estrutura existir
- **Quando usar:** **docs técnicos, manuais, código** (sempre que houver headers)

Tools: `unstructured`, `MarkdownHeaderTextSplitter` (LangChain).

### 5. Contextual chunking (Anthropic 2024)

Cada chunk recebe **contexto sumarizado** do documento inteiro:

```
[Documento: Manual de FastAPI v3]
[Seção: Authentication]

Original chunk:
"Use o decorator @app.post('/login') para criar endpoint de autenticação..."

Chunk com contexto:
"[Manual de FastAPI v3, seção Authentication]
Use o decorator @app.post('/login') para criar endpoint de autenticação..."
```

- **Prós:** contexto preservado, dramatic improvement em accuracy
- **Contras:** custo extra de gerar contexto (LLM call por chunk)
- **Quando usar:** alta-stakes, qualidade > custo

Anthropic mostrou redução de **35% em failed retrievals** com contextual retrieval — e **49%** quando combinado com reranking (BM25 + embeddings + reranker).

> [!question]- Como isso é implementado de verdade, não em pseudo-código?
> A ideia central é usar um LLM para gerar, para cada chunk, uma ou duas frases de contexto situacional — "este chunk é sobre X, dentro do documento Y, na seção Z" — e prepender esse contexto ao chunk **antes** de embedar. O truque de custo é usar **prompt caching**: o documento inteiro fica em cache, e só o chunk individual (pequeno) varia a cada chamada, então você paga o processamento do documento completo uma única vez.
>
> ```python
> import anthropic
>
> client = anthropic.Anthropic()
>
> DOCUMENT_CONTEXT_PROMPT = """
> <document>
> {doc_content}
> </document>
> """
>
> CHUNK_CONTEXT_PROMPT = """
> Aqui está o chunk que queremos situar dentro do documento inteiro:
> <chunk>
> {chunk_content}
> </chunk>
>
> Responda apenas com um contexto curto e sucinto para situar
> este chunk no documento, com o objetivo de melhorar a busca
> por recuperação (retrieval) do chunk. Não responda mais nada
> além do contexto sucinto.
> """
>
> def situate_context(doc: str, chunk: str) -> str:
>     response = client.messages.create(
>         model="claude-opus-4-5-20251101",
>         max_tokens=1024,
>         messages=[{
>             "role": "user",
>             "content": [
>                 {
>                     "type": "text",
>                     "text": DOCUMENT_CONTEXT_PROMPT.format(doc_content=doc),
>                     "cache_control": {"type": "ephemeral"},  # cacheia o doc inteiro
>                 },
>                 {
>                     "type": "text",
>                     "text": CHUNK_CONTEXT_PROMPT.format(chunk_content=chunk),
>                 },
>             ],
>         }],
>     )
>     return response.content[0].text
> ```
>
> O contexto gerado é prependado ao chunk original antes de embedar e antes de indexar no BM25. Na prática recomendada pela Anthropic, contextual chunking funciona melhor combinado com busca híbrida (embeddings + BM25) e um passo de reranking — cada camada reduz uma fatia diferente das falhas de retrieval.

## Decisões críticas

### Tamanho do chunk

| Tamanho | Trade-off |
|---|---|
| **<200 tokens** | Granular, mas perde contexto |
| **500 tokens** | Sweet spot — default |
| **1000 tokens** | Mais contexto, retrieval menos preciso |
| **>2000 tokens** | Perde sentido de "trecho relevante" |

Heurística: **chunk ≈ resposta esperada × 2-3**.

### Overlap

```
[Chunk 1: tokens 0-500]
    [overlap: tokens 450-500]
        [Chunk 2: tokens 450-950]
```

- **Sem overlap:** info na borda perdida
- **Com overlap (10-20%):** continuidade preservada
- **Overlap excessivo (>30%):** redundância, custo

### Metadata

Cada chunk **deve** carregar:

```python
chunk = {
    "text": "...",
    "source": "manual_v3.md",
    "section": "Authentication",
    "page": 42,
    "doc_date": "2026-04-15",
    "language": "pt-br",
    "type": "tutorial"
}
```

Permite filtragem em retrieval (`WHERE doc_date > '2026-01-01'`) e citação na geração.

## Patterns por tipo de documento

| Tipo | Estratégia | Tamanho |
|---|---|---|
| **Markdown / docs** | Structure-aware (headers) | 500-1000 |
| **PDF estruturado** | Structure-aware + recursive | 500 |
| **Código** | AST-based ou function-level | 30-100 LOC |
| **Email / chat** | Por mensagem ou turno | variável |
| **Logs** | Por evento ou janela temporal | variável |
| **Tabelas** | Por linha + header preservado | uma linha |
| **Transcripts** | Por speaker turn ou tempo | 30-60s |

## Validação manual

> [!tip] Antes de indexar 100K chunks
> 1. Gere chunks de **10 documentos amostra**
> 2. Inspecione visualmente: tabelas inteiras? código completo? citações com fonte?
> 3. Faça queries gold e veja se chunks relevantes existem
> 4. Ajuste parâmetros até estar satisfeito
> 5. **Aí** indexe em escala

Pular essa etapa = retrabalho enorme depois.

## Sinais de chunking ruim

- Top-k retorna parte de tabela sem header
- Resposta cita fonte mas trecho não tem o fato citado
- Mesma seção espalhada em múltiplos chunks pequenos
- Chunks com "Tabela 3" mas sem o conteúdo da tabela
- Código quebrado no meio de uma função

## Métricas

| Métrica | Alvo |
|---|---|
| **Tamanho médio chunk** | 400-1000 tokens |
| **% chunks com metadata completa** | 100% |
| **% chunks com texto cortado mid-sentence** | <5% |
| **Recall@5 em golden set** | >80% |

## Anti-patterns

- **Fixed-size sem overlap** — info na borda perdida
- **Chunk gigante (5K tokens)** — vector "não significa" nada concreto
- **Chunks sem metadata** — não consegue filtrar nem citar
- **Re-chunkar sem re-indexar** — chunks novos com embeddings velhos
- **Chunking igual para tipos diferentes de doc** — Markdown ≠ código ≠ PDF
- **Não validar manualmente** — descoberta de problema só em produção

## Armadilhas comuns

> [!warning] Usar fixed-size chunking sem validar o output
> Fixed-size é o padrão de quem quer "colocar RAG pra funcionar rápido" — e funciona mal em produção. Chunks cortam no meio de sentenças, tabelas ficam com header num chunk e dados em outro, código é fragmentado no meio de uma função. Antes de indexar qualquer coisa em escala, inspecione visualmente pelo menos 20-30 chunks gerados. O retrabalho de re-indexar depois é sempre mais caro que validar antes.

> [!warning] Chunks sem metadata perdem rastreabilidade
> Um chunk sem metadata é um trecho de texto anônimo — não dá para filtrar por data, tipo de documento, seção, idioma ou fonte. Isso significa que não dá para citar fontes corretamente, não dá para fazer retrieval com filtros (WHERE doc_date > '2026-01-01') e não dá para debugar por que um resultado ruim chegou no contexto. Metadata é obrigatória. Sempre. Mesmo em protótipos.

> [!warning] Rechunkar sem re-indexar — ou re-indexar sem re-validar
> Quando você ajusta parâmetros de chunking (tamanho, overlap, estratégia), os chunks novos são incompatíveis com os embeddings antigos no índice. Você precisa deletar o índice antigo, re-chunkar, re-embedar, e re-indexar — do zero. E depois disso, valide com seu golden set antes de colocar em produção: chunkings diferentes produzem qualidade de retrieval diferente, e só a métrica revela se melhorou ou piorou.

## Erros reais de chunking

> [!example]- Caso: tabela de preços quebrada em produção
> Um sistema de suporte técnico indexava manuais de produto usando fixed-size chunking a 500 tokens. Uma tabela de preços com 40 linhas tinha ~1200 tokens — foi dividida em 3 chunks. O primeiro chunk carregava o header (`Produto | Preço | SLA`), o segundo e o terceiro só tinham linhas de dados soltas. Quando um cliente perguntava "quanto custa o plano Enterprise?", o retrieval trazia o chunk 2 ou 3 — números sem contexto de qual coluna era qual. O modelo respondia com valores plausíveis, mas errados, porque não tinha como saber a que coluna cada número pertencia. A correção foi trivial (structure-aware chunking, uma linha de tabela por chunk, header replicado em cada uma) — mas só foi descoberta depois de reclamações de clientes, não em teste.

> [!example]- Caso: citação sem atribuição em RAG jurídico
> Documentos legais frequentemente têm o padrão "cláusula → citação de precedente → fonte da citação" em parágrafos consecutivos. Um chunking recursivo com `chunk_size` pequeno demais (300 tokens) separava a citação da fonte que a sustentava. O sistema passou a gerar respostas citando precedentes **sem conseguir apontar de onde vieram** — o pior cenário possível em um domínio onde rastreabilidade da fonte é requisito, não bônus. O ajuste foi aumentar o `chunk_size` para acomodar o padrão citação+fonte como unidade, e usar overlap maior nas bordas.

> [!example]- Caso: re-chunking sem re-embedding em produção
> Um time ajustou o parâmetro de overlap de 10% para 20% para melhorar a continuidade entre chunks, gerou os novos chunks, mas atualizou só metade do índice por um bug de deploy parcial. O resultado: metade dos vetores no índice vinha de chunks antigos, metade de chunks novos, com sobreposições inconsistentes entre si. O sintoma era retrieval "aleatoriamente pior" — sem padrão claro, o que tornou o diagnóstico mais demorado do que se o índice inteiro estivesse simplesmente desatualizado. A lição prática: re-chunking é uma operação atômica — ou o índice inteiro é reconstruído, ou nada é.

Esses três casos compartilham um padrão: o erro nunca aparece nos testes com poucos documentos — ele aparece em escala, quando a variedade de formatos e a quantidade de queries expõe os edge cases que a amostra pequena escondia. É exatamente por isso que a validação manual (seção acima) precisa rodar **antes** de indexar em escala, não depois de reclamações chegarem.

## Como explicar em inglês

Chunking is the process of splitting source documents into smaller pieces — chunks — before embedding them and indexing them in a vector store. It sounds trivial but it's where RAG systems win or lose. The embedding model can only represent what's inside each chunk; if a key fact is split across chunk boundaries, or if a table's header lands in one chunk and its data in another, no retrieval algorithm can recover that information.

There are five main strategies, each with a different cost-quality tradeoff. Fixed-size chunking is the simplest: split at N tokens with overlap. Recursive chunking respects natural separators (double newlines, periods, spaces) in a hierarchical fallback — this is the right default for most use cases. Semantic chunking embeds individual sentences and breaks where adjacent sentence similarity drops below a threshold, which produces more coherent units but is computationally expensive. Structure-aware chunking exploits document markup — Markdown headers, HTML sections, AST nodes for code — and produces the cleanest results when the source has structure. Finally, contextual chunking (Anthropic's 2024 approach) prepends a document-level summary to each chunk before embedding, which reduced failed retrievals by 35% in their evaluation.

The decision that matters most is validation: never index at scale without first generating a sample and inspecting it manually. A 30-minute audit of 30 chunks saves hours of debugging retrieval failures in production.

**In a technical interview**, you might say:

> "I treat chunking as the highest-leverage decision in a RAG pipeline. Before touching embedding models or vector databases, I get chunking right. My default is recursive splitting at 512-1024 tokens with 10-15% overlap, using structure-aware splitting whenever the document has headers or sections. Every chunk carries metadata: source, section, date, document type. I always inspect a random sample before indexing at scale — table headers in the wrong chunk, mid-sentence cuts, code fragments — those are quality killers that no downstream optimization can fix. For high-stakes use cases, I use contextual chunking and add a summary prefix per chunk."

| PT | EN |
|----|-----|
| Fragmentação de texto | Chunking / text splitting |
| Sobreposição | Overlap |
| Chunk sensível à estrutura | Structure-aware chunk |
| Fragmentação semântica | Semantic chunking |
| Fragmentação contextual | Contextual chunking |
| Tamanho do fragmento | Chunk size |
| Conjunto de validação | Golden set |
| Metadados do fragmento | Chunk metadata |
| Indexação em escala | Large-scale indexing |
| Limite do fragmento | Chunk boundary |

## O que vem a seguir

Com chunking bem definido e embeddings no lugar, os textos estão indexados e prontos para serem buscados. O próximo passo é entender onde esses vetores vivem: os vector databases. Eles não são todos iguais — a escolha entre pgvector, Pinecone e Qdrant tem implicações de latência, custo, escala e operação que afetam diretamente como o retrieval funciona em produção.

- [[05 - Vector databases — pgvector, Pinecone, Qdrant]] — comparativo de opções, quando usar cada uma, HNSW vs IVF, filtros de metadata, custo e escala

## Veja também

- [[02 - Anatomia do pipeline RAG]]
- [[03 - Embeddings — representação semântica]]
- [[06 - Retrieval — hybrid search, BM25, query rewriting]]
- [[09 - Evaluation de RAG]]

## Referências

- **Anthropic** — [*Introducing Contextual Retrieval*](https://www.anthropic.com/news/contextual-retrieval) (2024). Redução de 35-49% em failed retrievals com contextual chunking + hybrid search + reranking.
- **LangChain** — [*Text Splitters*](https://python.langchain.com/docs/concepts/text_splitters/) (2026). Documentação oficial de `RecursiveCharacterTextSplitter` e demais splitters.
- **LlamaIndex** — [*Node Parser Modules*](https://docs.llamaindex.ai/en/stable/module_guides/loading/node_parsers/) (2026). Node parsers e chunking strategies.
- **Unstructured** — [*Chunking*](https://docs.unstructured.io/open-source/core-functionality/chunking) (2026). Document parsing e chunking para PDFs e formatos não estruturados.
