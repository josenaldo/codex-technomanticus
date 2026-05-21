---
title: "Generation — passar contexto ao LLM com citação"
created: 2026-04-11
updated: 2026-05-02
type: concept
status: seedling
publish: true
tags:
  - rag
  - ia
  - generation
aliases:
  - Generation RAG
  - Citação de fonte
  - Prompt RAG
---

# Generation — passar contexto ao LLM com citação

> [!abstract] TL;DR
> Geração é onde RAG vira **resposta com citação**. Estrutura padrão de prompt: trechos delimitados + pergunta + regras explícitas (citar trecho usado, devolver "não sei" se contexto não cobre). Citação não é nice-to-have — é a feature que diferencia RAG de chatbot. Cuidado com **faithfulness**: LLM pode misturar contexto com conhecimento próprio. Padrões: structured output com source ID, system prompt restritivo, validação de citação no post-processing.

## A estrutura do prompt

```text
SYSTEM:
Você responde apenas com base nos trechos fornecidos. Cite [N] cada
afirmação usando o número do trecho. Se trechos não cobrem a pergunta,
responda: "Não encontrei essa informação."

USER:
Trechos:
[1] {chunk_1_text}
[2] {chunk_2_text}
[3] {chunk_3_text}

Pergunta: {user_question}
```

3 elementos cruciais:
1. **Delimitação** — trechos numerados, separados
2. **Regra de citação** — explícita
3. **Regra de fallback** — "não sei" como opção válida

## Por que citação importa

Sem citação:
- Usuário não sabe se LLM inventou
- Compliance (medical, legal, finance) inviável
- Auditoria impossível
- Confiança limitada

Com citação:
- Usuário verifica fonte
- Audit trail natural
- Compliance facilitado
- Confiança aumenta

## Patterns de prompt

### Pattern 1 — Numbered citations (default)

```
Trechos:
[1] FastAPI suporta async desde a versão 0.5...
[2] Para criar endpoint async, use async def...
[3] Connection pooling melhora performance...

Resposta esperada:
"FastAPI suporta async [1]. Para criar endpoints, use async def [2]. Para
performance, considere connection pooling [3]."
```

Simples, fácil de validar (regex `\[\d+\]`).

### Pattern 2 — Structured output

```python
from pydantic import BaseModel

class Citation(BaseModel):
    text: str
    sources: list[int]  # IDs dos chunks

class RAGResponse(BaseModel):
    answer: list[Citation]
    confidence: Literal["high", "medium", "low"]
    is_supported: bool
```

LLM retorna JSON válido. Validação automática.

### Pattern 3 — XML delimiters

```
<context>
  <doc id="1">...</doc>
  <doc id="2">...</doc>
</context>
<question>...</question>
```

XML reduz prompt injection (ver [[Segurança e Guardrails]]).

## System prompt restritivo

Padrão consolidado:

```
You are a {domain} assistant. Answer ONLY based on the provided context.

Rules:
1. Cite each claim with [N] referencing the source chunk.
2. If context does not contain the answer, respond: "I cannot answer
   based on available information."
3. Do NOT use external knowledge, even if you "know" the answer.
4. If chunks contradict, point out the contradiction.
5. Quote directly when accuracy is critical.

Context:
[1] {chunk_1}
[2] {chunk_2}
...

Question: {user_question}
```

A regra **3** é crítica — LLM tende a complementar com conhecimento próprio. System prompt restritivo reduz mas não elimina.

## Faithfulness — o problema central

**Faithfulness:** a resposta é fiel ao contexto (sem inventar)?

Modos comuns de falha:

| Falha | Exemplo |
|---|---|
| **Mistura de fontes** | Resposta combina dois chunks contraditórios sem notar |
| **Inferência não-suportada** | Contexto diz "FastAPI suporta async". LLM diz "FastAPI é mais rápido que Flask" (não no contexto) |
| **Generalização** | Contexto sobre v3, LLM responde sobre todas as versões |
| **Citação errada** | Cita [2] mas info está em [1] |
| **Halucinação total** | Inventa info não presente em nenhum chunk |

Mitigações:

- **System prompt restritivo** (acima)
- **Reduzir temperature** (0 ou 0.2 para tarefas factuais)
- **Validação automática** (LLM-as-judge: a resposta usa info do contexto?)
- **Estimativa de confidence** (LLM declara confidence)

Detalhes em [[09 - Evaluation de RAG]].

## Quando dizer "não sei"

> [!tip] Devolver "não sei" é feature, não falha
> RAG-bom é melhor que RAG-tudo-respondendo. Condições para "não sei":
> - Reranker top-1 score <0.6 ([[07 - Reranking — Cohere, Voyage, cross-encoders|07 - Reranking]])
> - Contexto não cobre a pergunta semanticamente
> - Pergunta fora do escopo do dataset

LLM-as-judge auxiliar:

```python
def is_answerable(question, chunks):
    prompt = f"""
    Os trechos abaixo são suficientes para responder?
    Pergunta: {question}
    Trechos: {chunks}

    Responda: yes/no/partial
    """
    return llm.complete(prompt)
```

## Output formatting

### Resposta direta + citações inline

```
"FastAPI suporta async desde a versão 0.5 [1]. Para criar um endpoint async,
use async def antes da função handler [2]."
```

Mais usado. Boa UX.

### Resposta + sources separados

```json
{
  "answer": "FastAPI suporta async desde a versão 0.5...",
  "sources": [
    {"chunk_id": 1, "page": 42},
    {"chunk_id": 2, "page": 51}
  ]
}
```

Útil para UIs com tooltips ou expansíveis.

### Quote-driven

```
> "FastAPI fully supports async since v0.5"
> — manual.md, page 42

> "Endpoints can be made async by using `async def`..."
> — manual.md, page 51
```

Em domínios legal ou medical, citações textuais reduzem ambiguidade.

## Modelos para generation

| Modelo | Forte em RAG | Custo |
|---|---|---|
| **Claude Sonnet 4.6** | Excelente em seguir instruções restritivas | Médio |
| **GPT-5** | Muito bom, costuma "complementar" mais | Médio |
| **Gemini 2.5 Pro** | Long context, multimodal | Médio |
| **Haiku / Flash / GPT-4o-mini** | Bom para QA simples, barato | Baixo |
| **Llama 3.3 70B** | Self-hosted | $$ infra |

> [!tip] Tiering em RAG
> Use Haiku/Flash para 90% das perguntas simples. Escala para Sonnet/Opus quando confidence baixa ou pergunta complexa.

## Latência típica

| Componente | Latência |
|---|---|
| Generation com 5 chunks de 500 tokens | 500ms-2s |
| Streaming (TTFT) | 200-500ms |
| Total user-facing (com retrieval) | 1-3s |

Streaming é crucial para UX em RAG — usuário vê resposta começando imediatamente.

## Métricas

| Métrica | Alvo |
|---|---|
| **Faithfulness** (LLM-as-judge) | >90% |
| **Citation accuracy** (citação aponta info correta) | >95% |
| **% respostas "não sei" apropriadas** | 5-15% |
| **Latência generation** | <2s (p95) |
| **Cost por resposta** | <$0.005 |

## Anti-patterns

- **Sem regra de citação** — LLM responde sem fontes
- **Sem regra de "não sei"** — força resposta mesmo sem info
- **Temperature alta** (>0.5) em RAG factual — mais hallucination
- **Não validar citações** — citação errada passa
- **Modelo grande para tudo** — Haiku resolve a maioria
- **Sem streaming** — UX ruim
- **Prompt sem delimitação** — confusão entre context e instruction

## Veja também

- [[01 - O que é RAG e quando usar]]
- [[06 - Retrieval — hybrid search, BM25, query rewriting]]
- [[07 - Reranking — Cohere, Voyage, cross-encoders]]
- [[09 - Evaluation de RAG]]
- [[Segurança e Guardrails|07 - Security-focused prompting]]

## Referências

- **Anthropic** — *Citations API* (2024)
- **Eugene Yan** — *Patterns for Building LLM-based Systems* (2024)
- **OpenAI** — *Structured outputs guide* (2026)
