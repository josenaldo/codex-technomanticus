---
title: "Indexação semântica externa — vector DB como contexto persistente"
type: concept
progress: backlog
publish: true
created: 2026-05-22
updated: 2026-05-22
status: seedling
fase: magus
tags:
  - claude-code
  - workflows
  - contexto
  - tokens
  - mcp
  - rag
  - vector-database
  - embeddings
  - semantic-search
aliases:
  - Semantic search MCP
  - RAG para codebase
  - Indexação vetorial
---

# Indexação semântica externa — vector DB como contexto persistente

> [!abstract] TL;DR
> A cada tarefa, o agente tende a redescobrir o codebase: `Grep`, `Read`, `Grep`, `Read`. Em monorepo grande, isso queima 50k–200k [[Dicionário de IA#Token|tokens]] só pra "achar onde está". Indexação semântica externa parte o codebase em [[Dicionário de IA#chunking|chunks]], gera [[Dicionário de IA#embedding|embeddings]], guarda num [[Dicionário de IA#vector database|vector DB]], e expõe via [[Dicionário de IA#MCP (Model Context Protocol)|MCP]] uma tool de `search_code(query)` que devolve só os trechos relevantes. O agente faz **uma** busca em vez de 30 grep+read, com 5%–10% do custo de tokens. Requer infra externa (API de embedding + vector DB) e disciplina de re-indexação.

## O que é

Aplicação clássica de [[Dicionário de IA#RAG (Retrieval-Augmented Generation)|RAG (Retrieval-Augmented Generation)]] ao codebase: transformar o repositório inteiro em um índice vetorial consultável, externo ao contexto do agente.

Em vez de o Claude Code:

```
Grep("authentication")        → 47 matches
Read("auth/login.ts")         → 200 linhas
Read("auth/middleware.ts")    → 150 linhas
Grep("validateToken")         → 12 matches
Read("auth/jwt.ts")           → 180 linhas
...
```

ele faz:

```
search_code("how is JWT token validation implemented") 
  → 3 chunks de ~30 linhas cada, ranqueados por relevância semântica
```

A diferença não é só volume — é **qualidade de busca**: semantic search entende intenção, encontra código relevante mesmo com nomes diferentes ("authToken", "bearer", "JWT"), e ranqueia por similaridade conceitual em vez de match literal.

## Como funciona

### Pipeline de indexação

```
┌──────────────┐    chunking      ┌──────────────┐
│   Codebase   │ ───────────────► │   Chunks     │
└──────────────┘                  │  (50-200     │
                                  │   linhas     │
                                  │   cada)      │
                                  └──────┬───────┘
                                         │
                                         ▼
                                  ┌──────────────┐
                                  │  Embedding   │
                                  │  API         │
                                  │  (OpenAI,    │
                                  │   Voyage,    │
                                  │   Gemini)    │
                                  └──────┬───────┘
                                         │
                                         ▼
                                  ┌──────────────┐
                                  │  Vector DB   │
                                  │  (Milvus,    │
                                  │   Pinecone,  │
                                  │   Qdrant,    │
                                  │   Zilliz)    │
                                  └──────┬───────┘
                                         │
                                         ▼ (via MCP)
                                  ┌──────────────┐
                                  │  Claude Code │
                                  └──────────────┘
```

### Tipos de chunking

A qualidade do retrieval depende muito de **como o código é cortado em chunks**:

- **Por janela fixa de linhas** (~200 linhas) — simples, mas corta funções no meio.
- **Por AST** (função/classe completa) — preserva semântica, mas chunks variam de tamanho.
- **Híbrido** — AST para funções pequenas, janela deslizante para arquivos longos.

Implementações sérias usam Tree-sitter pra chunking AST-aware.

### Re-indexação incremental

Indexação inicial demora (minutos a horas em repo grande). O que sustenta a abordagem é **re-indexação incremental**: a cada commit (ou save de arquivo), só os chunks afetados são re-embedados. Implementações maduras usam Merkle tree do repo pra identificar o delta com precisão.

Sem re-indexação automática, o índice vira stale rápido e o agente pesquisa "código antigo".

### Acesso via MCP

A camada que conecta tudo é um **MCP server**. Ele expõe tools como:

- `search_code(query, top_k=5)` — busca semântica.
- `search_symbol(name)` — busca exata por nome (fallback pra keyword).
- `index_status()` — health check do índice.
- `reindex(path)` — força re-indexação de um path.

Configurado uma vez no `~/.claude.json` ou via CLI:

```bash
claude mcp add claude-context \
  -e OPENAI_API_KEY=sk-... \
  -e MILVUS_TOKEN=... \
  -- npx @zilliz/claude-context-mcp@latest
```

## Quando usar

A abordagem só compensa quando o **custo de busca repetida** supera o **custo de infra**:

| Sinal | Indica indexação semântica |
|---|---|
| Monorepo >100k LOC | Sim |
| Agente faz >20 `Grep`+`Read` por sessão | Sim |
| Sessões longas onde o mesmo código é redescoberto várias vezes | Sim |
| Repo pequeno (<10k LOC) | Não — `Grep` direto resolve |
| Codebase muda muito (refactors diários) | Cuidado — índice vira stale |
| Sem orçamento pra API de embedding + vector DB | Não viável |

Tipicamente vale a pena em monorepo corporativo, plataformas de desenvolvedor internas, projetos open source grandes (Linux kernel, Kubernetes) onde o agente precisa "saber onde tudo está".

## Custo real

A abordagem não é gratuita:

- **API de embedding**: ~$0.10 por 1M tokens de embedding (OpenAI `text-embedding-3-small`). Indexar 1M LOC = ~50M tokens = ~$5 inicial.
- **Vector DB**: free tier disponível (Zilliz Cloud, Pinecone), mas a partir de algumas centenas de MB de embeddings, vira tier pago (~$20–100/mês).
- **Manutenção**: hooks pra re-indexação, monitoring de drift, purge de chunks órfãos.

Numa conta de Claude Code de $500/mês com sessões longas em monorepo, indexação que reduz 30% do consumo paga a infra em uma semana. Em projeto pequeno, o overhead engole o ganho.

## Armadilhas

**Índice stale**. Sem re-indexação automática, o agente pesquisa "código antigo" e gera patches que não compilam. Re-indexação tem que rodar em hook de save/commit, não manual.

**Qualidade de busca dependente do chunking**. Chunking ruim (janela fixa atravessando funções) gera retrievals semanticamente quebrados. Vale o investimento em chunking AST-aware desde o início.

**Lock-in em vendor**. Se você usa Zilliz Cloud + OpenAI embeddings, mover pra outro stack exige re-embedar tudo (embeddings de modelos diferentes não são comparáveis). Vale considerar **abstração via standards** (LiteLLM pra embedding, Milvus self-hosted pra DB) se a portabilidade importa.

**Dados sensíveis vazando pro embedding provider**. Embeddings de OpenAI implicam mandar código pra OpenAI. Em codebase corporativo com IP sensível, isso é vetor de risco — considere embeddings locais (sentence-transformers) ou provedores com cláusulas de não-retenção.

**Confiar na busca semântica para tudo**. Semantic search é ótimo para "onde tá a lógica de X", ruim para "todas as chamadas de exatamente esta função". Pra busca exata por símbolo, keyword search (Grep) continua melhor. Implementações maduras combinam: hybrid search com FTS5 + vector similarity.

**Indexar tudo, inclusive lixo**. `node_modules/`, builds, vendored libs entram no índice e poluem retrievals. Configure `.indexignore` (ou equivalente) tão agressivo quanto o `.gitignore`.

## Relação com outras abordagens deste galho

Lazy-load ([[01 - Estrutura .claude lazy-load|01]]) e sandboxing ([[02 - Sandboxing de tool output|02]]) reduzem o que **entra** no contexto. Indexação semântica muda **como o codebase é navegado** — em vez de carregar arquivos inteiros, o agente faz queries que retornam só o relevante.

A diferença pra knowledge graph ([[04 - Knowledge graph local com AST|04]]) é o eixo de organização: indexação semântica organiza por **similaridade conceitual** (embeddings); knowledge graph organiza por **relação estrutural** (calls, imports, inheritance). As duas se complementam — indexação acha "onde fala disso", knowledge graph acha "o que isso afeta".

## Veja também

- [[03-Dominios/Tecnologia/IA/Claude Code/Skills e MCP/04 - MCP overview|MCP overview]] — protocolo de extensão usado por todo MCP de indexação
- [[03-Dominios/Tecnologia/IA/Claude Code/Skills e MCP/05 - MCP servers essenciais|MCP servers essenciais]] — outras MCPs úteis
- [[03-Dominios/Tecnologia/IA/Context Engineering/06 - Dynamic retrieval beyond RAG|Dynamic retrieval beyond RAG]] — contexto teórico de RAG e suas evoluções
- [[04 - Knowledge graph local com AST]] — abordagem complementar (relação estrutural)
- [[03-Dominios/Tecnologia/IA/Claude Code/Workflows/11 - Estratégias estruturais de contexto/index|Tronco do sub-galho]]

## Aprofundamento

> [!convite] Referências externas
> - [zilliztech/claude-context](https://github.com/zilliztech/claude-context) — MCP de semantic search mantido pela Zilliz (empresa por trás do Milvus, vector DB open source de referência). MIT, ~12 meses de idade, ~11k stars com crescimento orgânico, ecossistema cross-platform (Claude Code, Cursor, Codex, Gemini CLI, Windsurf, etc). É a referência mais sólida do espaço. Usa Tree-sitter para chunking AST-aware, Merkle tree para re-indexação incremental, OpenAI/Voyage/Gemini para embeddings.
> - Conceitos relacionados: [Anthropic — Contextual Retrieval](https://www.anthropic.com/news/contextual-retrieval) (técnica que melhora qualidade de chunks adicionando contexto antes de embedar).
>
> Consumiu? Faça uma glosa em `02-Glosas/` se quiser destilar mais.
