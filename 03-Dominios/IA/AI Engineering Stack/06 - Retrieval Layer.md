---
title: "Retrieval Layer"
created: 2026-05-28
updated: 2026-05-28
type: concept
status: seedling
progress: in_progress
tags:
  - ai-engineering-stack
  - ia
  - retrieval
publish: true
aliases:
  - Retrieval Layer
  - Camada de recuperação
---

# Retrieval Layer

> [!abstract] TL;DR
> A Retrieval Layer responde **quando puxar conhecimento externo, de quais fontes, e como citar**. Não é só RAG vetorial — é toda forma de o modelo acessar informação que não está nos pesos: docs internos, web search, knowledge graphs, APIs. As decisões chave são: quando usar retrieval (vs deixar o modelo arriscar), hierarquia de fontes (qual ganha em conflito), regra de citação (cada claim ↔ fonte), e o que fazer quando nenhuma fonte responde.

## O que é esta camada

A Retrieval Layer existe porque o conhecimento de um LLM tem três problemas: está desatualizado (cutoff de treino), é genérico (não conhece seus docs), e não é verificável (não dá pra apontar a fonte). Retrieval resolve os três trazendo conhecimento **externo, atual, citável** pra dentro do contexto.

Template mínimo (adaptado do thread @hooeem):

```yaml
use_retrieval_when:
  - informação pode ter mudado desde o cutoff
  - precisa verificação de fonte
  - dado é externo ao modelo
  - claim factual com risco de alucinação
source_hierarchy:
  - <fonte mais confiável>
  - <fonte secundária>
  - <fallback>
citation_rule: <toda claim factual cita fonte | só claims novas | nenhuma>
conflict_rule: <fonte mais alta ganha | mais recente ganha | flag pro humano>
missing_source_rule: <recusa | diz "não sei" | tenta com aviso>
```

Retrieval Layer **decide quando e como**; a implementação (vector DB, BM25, web search, MCP) vive na trilha [[RAG e Vector Databases]].

## Decisões-chave

1. **Quando NÃO usar retrieval.** Retrieval custa latência e tokens. Pra tarefas onde o conhecimento do modelo basta (programação geral, raciocínio matemático, brainstorm), retrieval só atrapalha. A regra: use quando a resposta certa **muda** com o tempo ou com a fonte.

2. **Hierarquia de fontes.** Em produto sério, fontes têm peso: documentação interna > documentação oficial do produto > artigos respeitados > web aberta. Hierarquia explícita evita o modelo dar peso igual a tudo.

3. **Citação como contrato.** "Toda claim factual deve linkar a fonte" muda o comportamento — o modelo passa a recusar afirmações que não consegue ancorar. Penaliza criatividade, aumenta confiabilidade.

4. **Conflito entre fontes.** Inevitável quando você indexa mais de uma fonte. Três políticas comuns: (a) mais alta na hierarquia ganha; (b) mais recente ganha; (c) flag pro humano. Política implícita é receita pra alucinação.

5. **Missing source.** Quando retrieval não acha nada relevante, o sistema deveria dizer "não sei" com clareza, não preencher com geração. Sem essa regra, retrieval ruim vira porta de entrada pra alucinação.

## Onde aprofundar no Codex

- **[[RAG e Vector Databases]]** — trilha completa de retrieval, da intuição ao setup de produção.
- **[[Context Engineering/06 - Dynamic retrieval beyond RAG|Dynamic retrieval beyond RAG]]** — JIT retrieval, retrieval por agentes, MCP como retrieval channel.
- **[[Dicionário de IA#RAG (Retrieval-Augmented Generation)|Dicionário: RAG]]**.

## Veja também

- [[04 - Context Layer]] — retrieval alimenta context
- [[07 - Tool Layer]] — web search e API queries são retrieval por tool
- [[09 - Evaluation Layer]] — qualidade de retrieval é métrica própria (recall, precision@k)

## Fontes

- **@hooeem** — *Become an AI Engineer*, chapter #18, Step 5 (Retrieval layer template).
- **Lewis et al.** — [*Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks*](https://arxiv.org/abs/2005.11401) (2020). Paper original do RAG.
- **Anthropic** — [*Contextual Retrieval*](https://www.anthropic.com/news/contextual-retrieval) (2024). Pré-processamento que melhora recall.
