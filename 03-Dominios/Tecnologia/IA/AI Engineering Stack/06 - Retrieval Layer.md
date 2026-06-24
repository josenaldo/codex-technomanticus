---
title: "Retrieval Layer"
created: 2026-05-28
updated: 2026-06-24
type: concept
status: seedling
fase: Iniciado
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
> A Retrieval Layer resolve três problemas do conhecimento em LLMs: ele está **desatualizado** (cutoff de treino), é **genérico** (não conhece seus documentos), e é **não-verificável** (não dá pra apontar a fonte). A camada define quando puxar conhecimento externo, de quais fontes, em que hierarquia de prioridade, como citar e o que fazer quando nenhuma fonte responde. Implementação (RAG vetorial, BM25, web search, MCP) é decisão posterior — a política de retrieval vem antes.

## O problema que a Retrieval Layer resolve

Pergunte ao modelo sobre sua política interna de licenças de software. Ele vai responder com confiança sobre o que LLMs de front-end sabem sobre políticas de licença em geral — que não é a sua política. Pergunte sobre um acontecimento da semana passada. Ele vai responder com o que sabia até o cutoff de treino — que pode ser há um ano. Pergunte sobre a versão 4.2.1 do seu framework interno. Ele vai alucinar uma documentação plausível.

O conhecimento de um LLM tem três limitações fundamentais:
1. **Desatualizado** — cutoff de treino pode ser meses atrás; dados em tempo real não existem.
2. **Genérico** — treinado em dados públicos, não nos seus documentos internos.
3. **Não-verificável** — você não consegue apontar a fonte de uma afirmação específica do modelo.

A Retrieval Layer resolve os três trazendo conhecimento **externo, atual, citável** para dentro do contexto a cada chamada. Mas retrieval não é gratuito: custa latência, custa tokens, e pode trazer ruído se mal configurado. A camada define a **política** — quando buscar, onde buscar, como usar o que foi encontrado.

## O que é esta camada

A Retrieval Layer define **quando e como** o sistema busca conhecimento externo. A implementação (vector DB, BM25, web search, MCP) é decisão da arquitetura técnica — aqui o que importa é a política.

Template mínimo (adaptado do thread @hooeem):

```yaml
retrieval:
  use_retrieval_when:
    - "informação pode ter mudado desde o cutoff de treino"
    - "claim factual com risco de alucinação"
    - "dado é interno e não está nos pesos do modelo"
    - "usuário precisa ver a fonte para confiar"
  source_hierarchy:
    - "documentação interna verificada"
    - "documentação oficial do produto/tecnologia"
    - "publicações acadêmicas revisadas"
    - "web aberta (menor confiança)"
  citation_rule: "toda claim factual cita fonte | só claims novas | nenhuma"
  conflict_rule: "fonte mais alta na hierarquia ganha | mais recente ganha | flag pro humano"
  missing_source_rule: "recusa e explica | diz 'não sei' | tenta com aviso de baixa confiança"
```

## Decisões-chave

**1. Quando NÃO usar retrieval.** Retrieval custa latência e tokens. Para tarefas onde o conhecimento do modelo basta — raciocínio matemático, programação geral, brainstorm, revisão de texto — retrieval só adiciona overhead. A regra: use quando a resposta correta **muda com o tempo** (fatos atualizáveis) ou **depende de uma fonte** (documentos internos, dados de uma API). Use o modelo "bruto" quando o raciocínio é mais importante que o fato.

**2. Hierarquia de fontes.** Em sistemas sem hierarquia explícita, o modelo dá peso igual a documentação interna cuidadosamente revisada e a um post de blog de 2019. Hierarquia explícita permite ao sistema priorizar automaticamente e — quando fontes conflitam — saber qual ganha sem precisar de intervenção humana em cada caso.

**3. Citação como contrato de confiabilidade.** "Toda claim factual deve citar a fonte" muda radicalmente o comportamento: o modelo passa a recusar afirmações que não consegue ancorar. Isso penaliza criatividade e aumenta a frequência de "não sei" — que é exatamente o trade-off correto para sistemas onde confiabilidade é mais importante que fluência.

**4. Política para conflito entre fontes.** Quando você indexa mais de uma fonte, conflitos são inevitáveis ("a documentação diz X, mas a RFC diz Y"). Três políticas comuns: (a) mais alta na hierarquia ganha; (b) mais recente ganha; (c) flag para humano quando há conflito. Sem política explícita, o modelo decide sozinho — o que pode ou não ser o comportamento desejado.

**5. Missing source: o que fazer quando não acha nada.** Esse é o caso mais perigoso. Sem regra, o modelo pode "preencher" com geração quando o retrieval não encontra nada relevante — produzindo uma resposta fluente que parece vir de uma fonte mas não vem. A regra mais segura: `missing_source_rule: "diz que não encontrou e sugere alternativa"`.

## Casos práticos

### Cenário 1 — O assistente que alucina documentação interna

Assistente de suporte técnico para produto B2B. Sem Retrieval Layer: o modelo foi treinado em dados públicos e "sabe" como APIs REST geralmente funcionam. Quando um cliente pergunta sobre o endpoint `/v2/reports/export` do produto, o modelo responde com confiança — mas o endpoint correto é `/api/v2/reports/export` (prefixo diferente) e o parâmetro `format` foi renomeado para `output_format` na v2.

Resultado: o cliente tenta o endpoint errado, falha, e culpa o suporte.

Com Retrieval Layer: o sistema indexa a documentação interna. Antes de responder sobre qualquer endpoint, consulta a documentação. Encontra `/api/v2/reports/export` com os parâmetros corretos. Responde com a fonte: "Conforme nossa documentação (link): o endpoint é `/api/v2/reports/export` com parâmetro `output_format`."

### Cenário 2 — Política de missing source em sistema de compliance

Sistema de perguntas sobre regulamentação financeira. A equipe jurídica sabe que regulações mudam frequentemente — a última coisa que querem é o modelo inventar uma regra desatualizada com ar de certeza.

```yaml
missing_source_rule: |
  Se retrieval não encontrar fonte relevante atualizada, 
  responda: "Não encontrei documentação atual sobre este ponto específico. 
  Recomendo consultar [fonte oficial] ou a equipe jurídica antes de agir."
```

Preferem um "não sei" explícito a uma resposta fluente porém incorreta. A taxa de "não sei" é uma métrica de saúde — alta demais significa que o índice de documentos precisa de atualização.

## Armadilhas comuns

> [!warning] Usar retrieval para tudo
> Retrieval não é gratuito. Adicionar retrieval a perguntas que o modelo responde corretamente com seu conhecimento de treino só adiciona latência e custo. Antes de ativar retrieval para um tipo de consulta, teste o modelo sem retrieval. Se a qualidade já for aceitável, não adicione a camada. Reserve retrieval para onde ele resolve um problema real: dados internos, fatos atualizáveis, exigência de citação.

> [!warning] Sem hierarquia de fontes, tudo tem o mesmo peso
> Sistemas que indexam múltiplas fontes sem hierarquia tratam a documentação interna revisada com o mesmo peso que um resultado aleatório de web search. Quando as fontes conflitam — e vão conflitar — o modelo decide arbitrariamente. Defina hierarquia antes de indexar a segunda fonte.

> [!warning] Sem `missing_source_rule`, retrieval ruim vira porta de alucinação
> O cenário mais perigoso: retrieval não encontra nada relevante, mas o modelo responde como se tivesse encontrado. Para o usuário, a resposta parece vir de uma fonte — mas foi gerada. A regra explícita para o caso de fonte não encontrada é tão importante quanto a regra para quando a fonte é encontrada.

## Como explicar em inglês

The Retrieval Layer addresses three fundamental limitations of LLM knowledge: it's outdated (training cutoff), generic (not your documents), and unverifiable (you can't trace a specific claim to a source). The layer defines when to retrieve external knowledge, from which sources, in what priority order, how to cite, and what to do when nothing is found. The implementation (vector DB, BM25, web search) is a technical decision made later — the retrieval policy comes first.

| PT | EN |
|----|----|
| Camada de recuperação | Retrieval Layer |
| Geração aumentada por recuperação | Retrieval-Augmented Generation (RAG) |
| Hierarquia de fontes | Source hierarchy |
| Regra de citação | Citation rule |
| Política para fonte ausente | Missing source policy |
| Regra de conflito | Conflict resolution rule |
| Busca vetorial | Vector search |
| Cutoff de treinamento | Training cutoff |
| Recall | Recall (proporção de documentos relevantes recuperados) |

## O que vem a seguir

Com o contexto enriquecido por retrieval, o sistema pode precisar de mais do que conhecimento — pode precisar **agir**: buscar em uma API externa, calcular, criar um arquivo, disparar um email. Isso é responsabilidade da **Tool Layer**: define quais ações o modelo pode executar no mundo real, com que nível de aprovação requerida, e o que fazer quando uma tool falha.

- [[07 - Tool Layer]] — o que o modelo pode fazer (ações com efeito colateral)
- [[RAG e Vector Databases]] — trilha completa: embeddings, vector DBs, hybrid search, reranking

## Onde aprofundar

- **[[RAG e Vector Databases]]** — trilha completa de retrieval, da intuição ao setup de produção (13 notas).
- **[[Context Engineering]]** → [[06 - Dynamic retrieval beyond RAG]] — JIT retrieval, retrieval por agents, MCP como retrieval channel.

## Veja também

- [[04 - Context Layer]] — retrieval alimenta o contexto de cada execução
- [[07 - Tool Layer]] — web search e API queries como tools de retrieval
- [[09 - Evaluation Layer]] — recall e precision@k como métricas de qualidade de retrieval

## Fontes

- **@hooeem** — *Become an AI Engineer*, chapter #18, Step 5 (Retrieval layer template). X/Twitter, 2025.
- **Lewis et al.** — [*Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks*](https://arxiv.org/abs/2005.11401) (2020). Paper original do RAG.
- **Anthropic** — [*Contextual Retrieval*](https://www.anthropic.com/news/contextual-retrieval) (2024). Técnica de pré-processamento que melhora recall ao adicionar contexto por chunk.
