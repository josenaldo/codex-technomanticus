---
title: "Entropia e qualidade de contexto"
created: 2026-05-02
updated: 2026-05-02
type: concept
progress: backlog
status: seedling
publish: true
tags:
  - context-engineering
  - ia
  - prompting
  - qualidade
aliases:
  - High-entropy context
  - Context quality
  - Signal to noise context
---

# Entropia e qualidade de contexto

> [!abstract] TL;DR
> Mais contexto **não é** melhor contexto. A pergunta certa: *quanto sinal por token?* Contexto de **alta entropia** é denso em informação útil; contexto de **baixa entropia** é diluído com redundância, ruído, distractors. A pesquisa de [[03 - Context rot e atenção diluída|context rot]] mostrou: cada token de baixa entropia rouba atenção dos tokens de alta entropia. Engenharia de qualidade de contexto = **maximizar a densidade de sinal por unidade de janela**.

## A reformulação

```
Pergunta antiga: "Como cabo mais informação no contexto?"
Pergunta nova:   "Como aumento o sinal por token?"
```

A primeira pergunta levou ao crescimento de janelas (1M, 2M [[Dicionário de IA#Token|tokens]]). A segunda levou a context engineering.

## High-entropy vs low-entropy

| | Alta entropia | Baixa entropia |
|---|---|---|
| **Sinal por token** | Alto | Baixo |
| **Redundância** | Mínima | Alta |
| **Distractors** | Filtrados | Presentes |
| **Modelo "atende" bem** | Sim | Não — dilui |
| **Custo eficiente** | Sim | Desperdício |

> [!example] Mesma pergunta, dois contextos
>
> **Baixa entropia (3K tokens):**
> Documentação inteira do produto pasted, incluindo 10 sections que falam de funcionalidades não relacionadas, 5 exemplos de código tangenciais, 2 release notes históricas.
>
> **Alta entropia (300 tokens):**
> Os 3 parágrafos diretamente relevantes à pergunta + 1 exemplo de código que demonstra a feature alvo.
>
> Modelo responde **melhor** ao 2º. Custa **10x menos**. Atenção dilui menos.

## A frase: "context as architecture, not content"

> [!quote] Atlan — Context Engineering Framework (2026)
> *"Context engineering is not a content problem — it is an architecture problem."*

Significa: o problema de qualidade de contexto não se resolve adicionando mais conteúdo nem editando frases. Resolve-se com **arquitetura**: pipeline ([[04 - Context pipelines — montagem dinâmica]]), camadas ([[05 - Camadas de contexto — persistente, temporal, transiente]]), retrieval ([[06 - Dynamic retrieval beyond RAG]]), compressão ([[07 - Compressão e pruning de informação]]).

## Os quatro tipos de "lixo" em contexto

### 1. Redundância

Mesma informação em múltiplas formas: documentação + comentário no código + [[Dicionário de IA#system prompt|system prompt]] repetindo. O modelo não ganha nada com a 3ª repetição — perde atenção.

**Mitigação:** deduplicar antes de injetar. Hash de chunks, similarity threshold.

### 2. Distractors

Informação **plausível** mas irrelevante. O modelo é puxado por similaridade semântica.

> Pergunta: *"Qual é a senha do servidor de produção?"*
> Distractor: docs sobre senha do servidor de staging, da CI, do dev local.
>
> Modelo confunde e responde a errada com confiança.

**Mitigação:** filtragem agressiva no [[Dicionário de IA#retrieval|retrieval]] (não top-k cego). Re-rank com LLM para alta-stakes. Validação de output.

### 3. Stale data

Informação que era verdade ontem e não é hoje.

**Mitigação:** TTL em memória persistente; preferir [[06 - Dynamic retrieval beyond RAG|JIT retrieval]] em domínios voláteis; auditoria periódica.

### 4. Bloat estrutural

Schemas verbosos, JSON pretty-printed, XML, comentários inúteis. Conteúdo pode ser denso, formato é diluído.

**Mitigação:** minificação. JSON sem whitespace. YAML em vez de JSON quando aplicável. CSV em vez de tabelas markdown verbosas.

## Métricas de entropia

Não existe métrica única, mas combinar três funciona:

| Métrica | Como medir | Alvo |
|---|---|---|
| **Tokens efetivos** | Repete a pergunta com 50% do contexto removido aleatório; resposta mantém qualidade? | Drop <10% |
| **Density score** | Embeddings de chunks com cosine sim < 0.7 → diversos | >0.6 |
| **Information per token** | Quantidade de fatos únicos / tokens (medido com fact extraction) | Maior é melhor, comparado a baseline |

## A "máxima da sala"

Se contexto é o **ambiente** do modelo, então a regra de ouro vem da arquitetura física: *"a sala precisa ter tudo necessário e nada além"*.

| Sala bagunçada | Sala bem arrumada |
|---|---|
| Tudo "está lá" se você procurar | Tudo importante visível |
| Você fica distraído | Você foca |
| Mais coisas piora | Menos coisas com curadoria melhora |

## Context products — versionamento de qualidade

Times maduros tratam contexto como **produto**:

> [!info] Atlan — Enterprise framework (2026)
> *"Context products: versioned, tested, governed bundles aimed at specific query patterns."*

- Bundle de contexto v1.0 → testes gold mostram accuracy 92%
- v1.1 → reduz tokens em 30%, accuracy 91% (aceito)
- v1.2 → adiciona retrieval JIT, accuracy 95% (promove)

Mudança em contexto = PR + review + métricas.

## Test gold — o jogo da entropia

Para medir qualidade de contexto rigorosamente:

```
1. Conjunto de queries representativas (50-200)
2. Para cada query, gabarito (resposta correta)
3. Variar contexto: full → pruned → compressed → JIT
4. Medir: accuracy, tokens, latência, cost
5. Pareto front entre qualidade e custo
```

Sem test gold, "melhorar contexto" vira intuição.

## Anti-patterns

- **Mais contexto sempre** — viola tudo que pesquisa de rot mostrou
- **Pretty-print em JSON** — desperdício gratuito
- **Concatenar 50 documentos sem rerank** — distractors em massa
- **Comentários genéricos no system prompt** — "be helpful" rouba atenção
- **Usar janela inteira "porque dá"** — quanto mais perto do limite, pior atenção

## Veja também

- [[03 - Context rot e atenção diluída]]
- [[06 - Dynamic retrieval beyond RAG]]
- [[07 - Compressão e pruning de informação]]
- [[Economia de Tokens|02 - Anatomia do gasto — input, output e reasoning]]

## Referências

- **Atlan** — *Context Engineering Framework for Enterprise AI* (2026).
- **Anthropic** — *Effective context engineering for AI agents* (2025).
- **Chroma Research** — *Context Rot: How Increasing Input Tokens Impacts LLM Performance* (jul 2025).
- **FlowHunt** — *Context Engineering: The Definitive Guide to Mastering AI System Design* (2025).
