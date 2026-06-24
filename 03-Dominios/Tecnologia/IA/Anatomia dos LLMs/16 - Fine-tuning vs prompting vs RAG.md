---
title: "Fine-tuning vs prompting vs RAG"
created: 2026-05-02
updated: 2026-06-24
type: concept
progress: done
status: growing
publish: true
tags:
  - anatomia-llm
  - ia
  - tokens
aliases:
  - Fine-tuning
  - RAG
  - Retrieval-Augmented Generation
  - Prompt engineering
---

# Fine-tuning vs prompting vs RAG

> [!abstract] TL;DR
> Três técnicas para adaptar um LLM ao seu caso de uso: **prompting** (instruções no contexto — custo zero, efeito imediato), **[[Dicionário de IA#RAG (Retrieval-Augmented Generation)|RAG]]** (busca e injeta informação relevante no contexto — custo moderado, dados sempre atualizados), e **[[Dicionário de IA#fine-tuning|fine-tuning]]** (retreina o modelo nos seus dados — custo alto, muda o comportamento do modelo). Em 2026, a maioria dos engenheiros resolve 95% dos problemas com prompting + RAG. Fine-tuning é reservado para tarefas de alta especialização com volume massivo.

## O erro de $5.000 que você não precisa cometer

Você está construindo um chatbot de suporte técnico. O modelo usa terminologia genérica demais, o tom está errado, e às vezes inventa informações. Alguém da equipe sugere: "vamos fazer fine-tuning". Três semanas depois, $5.000 em compute e 200 horas de engenharia, você tem um modelo fine-tuned que... performa exatamente igual ao original com um bom system prompt.

Esse cenário é repetido em dezenas de equipes por ano. A causa: confundir *qual camada do problema* cada técnica resolve.

- O modelo usa terminologia errada → **prompting** resolve (adicione exemplos e glossário ao system prompt)
- O modelo inventa informações sobre o produto → **RAG** resolve (injete a documentação atualizada a cada chamada)
- O modelo precisa classificar 50.000 tickets por dia com padrão específico → **fine-tuning** resolve (o único caso onde o custo se justifica)

O fine-tuning é a técnica mais cara e menos flexível das três. A árvore de decisão desta nota existe precisamente para você exaurir as duas primeiras antes de cogitar a terceira.

## O que é

Cada técnica opera em uma camada diferente:

| Técnica         | O que modifica                                | Persistência                          | Custo                       |
| --------------- | --------------------------------------------- | ------------------------------------- | --------------------------- |
| **Prompting**   | O input (contexto da chamada)                 | Nenhuma — reconstruído a cada chamada | Apenas tokens de input      |
| **RAG**         | O input (com dados recuperados dinamicamente) | Dados persistem no índice             | Infra de retrieval + tokens |
| **Fine-tuning** | Os pesos do modelo                            | Permanente (novo modelo)              | Treinamento + hosting       |

## Por que importa

Escolher a técnica errada é o erro mais caro em projetos de LLM:

- Fine-tuning quando prompting resolve → meses de trabalho desnecessário
- Prompting quando RAG é necessário → contexto explode e custos sobem
- RAG quando fine-tuning é necessário → qualidade nunca atinge o nível exigido

## Como funciona

### 1. Prompting (Context Engineering)

O modelo recebe todas as instruções e contexto no input de cada chamada.

```mermaid
graph LR
    A["System prompt<br>+ instruções<br>+ exemplos"] --> B[LLM]
    C["User message"] --> B
    B --> D[Resposta]
```

| Vantagem                     | Limitação                                       |
| ---------------------------- | ----------------------------------------------- |
| Zero setup, efeito imediato  | Limitado pela janela de contexto                |
| Fácil de iterar e testar     | Não "ensina" o modelo — apenas direciona        |
| Sem custo de treinamento     | Informação precisa ser reenviada a cada chamada |
| Funciona com qualquer modelo | Muito contexto → custo alto, atenção diluída    |

**Quando usar:** A primeira opção para tudo. Só migre para RAG ou fine-tuning quando prompting comprovadamente não resolve.

### 2. RAG (Retrieval-Augmented Generation)

O sistema busca informação relevante em uma base de dados e injeta no contexto antes de enviar ao modelo.

```mermaid
graph LR
    A[Query do usuário] --> B[Retriever]
    B -->|Busca semântica| C[Vector DB / Index]
    C --> D[Documentos relevantes]
    D --> E[Construir prompt]
    A --> E
    E --> F[LLM]
    F --> G[Resposta com dados atuais]
```

| Vantagem                                | Limitação                                    |
| --------------------------------------- | -------------------------------------------- |
| Dados sempre atualizados (just-in-time) | Requer infraestrutura ([[Dicionário de IA#vector store\|vector DB]], indexação) |
| Escala para milhões de documentos       | Qualidade depende do retriever               |
| Não precisa retreinar o modelo          | Aumenta input tokens (custo)                 |
| Citações e rastreabilidade              | Retrieval errado → alucinação com confiança  |

**Quando usar:**

- Base de conhecimento que muda frequentemente
- Codebase grande demais para caber no contexto
- Necessidade de citar fontes
- Múltiplas fontes de dados heterogêneas

### 3. Fine-tuning

Retreina os pesos do modelo em dados específicos do domínio.

> [!info] Esta nota é o "quando"; o "como" está na 19
> A mecânica — full fine-tuning, PEFT/LoRA/QLoRA e alinhamento por preferência (DPO) — está em [[21 - Fine-tuning na prática — LoRA, QLoRA, DPO]].

```mermaid
graph LR
    A[Modelo base] --> B[Treinamento SFT]
    C[Seus dados<br>formato: input → output] --> B
    B --> D[Modelo customizado]
    D --> E[Deploy + Hosting]
```

| Vantagem                              | Limitação                                               |
| ------------------------------------- | ------------------------------------------------------- |
| Muda o "comportamento base" do modelo | Custo alto de treinamento ($100–$10k+)                  |
| Reduz necessidade de prompt longo     | Risco de "catastrófico forgetting"                      |
| Pode aprender padrões complexos       | Precisa de dados limpos e abundantes (1k-100k exemplos) |
| Latência reduzida (sem retrieval)     | Modelo fica "congelado" nos dados de treino             |

**Quando usar:**

- Tarefa muito específica com padrão consistente (ex: classificação médica)
- Volume massivo (>10k chamadas/dia com padrão similar)
- Estilo ou formato de output muito específico
- Reduzir latência eliminando context longo

### Árvore de decisão

```mermaid
graph TD
    A{O modelo base<br>resolve com um bom prompt?} -->|Sim| B["✅ Use PROMPTING"]
    A -->|Não| C{O problema é falta<br>de informação atual?}
    C -->|Sim| D{A informação cabe<br>no contexto?}
    D -->|Sim| B
    D -->|Não| E["✅ Use RAG"]
    C -->|Não| F{O problema é<br>comportamento/estilo?}
    F -->|Sim| G{Volume alto<br>+ dados abundantes?}
    G -->|Sim| H["✅ Use FINE-TUNING"]
    G -->|Não| I["Use prompting com<br>exemplos (few-shot)"]
    F -->|Não| J["Repense o problema<br>ou combine técnicas"]
```

## Comparativo

| Critério                           | Prompting                  | RAG                 | Fine-tuning            |
| ---------------------------------- | -------------------------- | ------------------- | ---------------------- |
| **Tempo de setup**                 | Minutos                    | Dias–semanas        | Semanas–meses          |
| **Custo inicial**                  | $0                         | $100–$1k (infra)    | $1k–$50k (treinamento) |
| **Custo por chamada**              | Tokens de input            | Tokens + retrieval  | Hosting do modelo      |
| **Dados atualizados**              | Manual (reescrever prompt) | ✅ Automático        | ❌ Retreinar            |
| **Escala de dados**                | <100k tokens               | Milhões de docs     | 1k–100k exemplos       |
| **Qualidade em tarefa específica** | Boa                        | Muito boa           | Excelente              |
| **Flexibilidade**                  | Alta (muda o prompt)       | Alta (muda o index) | Baixa (retreinar)      |
| **Complexidade ops**               | Zero                       | Média               | Alta                   |

## Na prática

### Cenário 1: chatbot de suporte técnico

- **Solução:** RAG sobre documentação + prompting para tom e formato
- **Motivo:** Docs mudam semanalmente, precisam estar atualizados

### Cenário 2: agente de coding no projeto

- **Solução:** Prompting (CLAUDE.md, agents.md, context files)
- **Motivo:** O codebase já é o contexto; RAG para buscar arquivos específicos

### Cenário 3: classificador de tickets (10k/dia)

- **Solução:** Fine-tuning de modelo budget
- **Motivo:** Padrão repetitivo, volume alto, latência baixa necessária

### Cenário 4: pesquisa sobre papers acadêmicos

- **Solução:** RAG com vector DB de papers + prompting
- **Motivo:** Base de conhecimento grande e especializada

## Comparativo de custo e tempo de setup

```mermaid
xychart-beta
    title "Tempo de setup (dias) até produção"
    x-axis ["Prompting", "RAG", "Fine-tuning"]
    y-axis "Dias" 0 --> 90
    bar [0, 14, 60]
```

| Critério | Prompting | RAG | Fine-tuning |
|---|---|---|---|
| **Custo inicial** | $0 | $100–$1k | $1k–$50k |
| **Custo/chamada** | tokens de input | tokens + retrieval | hosting do modelo |
| **Flexibilidade** | Altíssima (muda o prompt) | Alta (muda o index) | Baixa (retreinar) |
| **Dados atualizados** | Manual | ✅ Automático | ❌ Retreinar |

## Armadilhas

- **"Fine-tuning é sempre melhor"** — é o mais caro e menos flexível. Use apenas quando prompting + RAG comprovadamente falham.
- **RAG sem avaliação do retriever** — se o retriever puxa documentos irrelevantes, o modelo [[Dicionário de IA#Hallucination|alucina]] com confiança, citando fontes erradas.
- **"Prompting não escala"** — com context engineering disciplinado (caching, state files, context pruning), prompting escala para a maioria dos casos.
- **Fine-tuning com poucos dados** — menos de 1000 exemplos de alta qualidade geralmente não produz melhoria significativa. O modelo pode memorizar em vez de generalizar.
- **Combinar errado** — RAG + fine-tuning pode degradar se o modelo fine-tuned ignora o contexto retrieved em favor do "conhecimento" aprendido.

## Como explicar em inglês

Three techniques to adapt an LLM to your use case, operating at different layers. **Prompting** (context engineering) puts instructions and examples in the input at call time — zero setup, immediately reversible. **RAG** (Retrieval-Augmented Generation) queries a vector index at call time and injects retrieved documents into the prompt — the model never "knows" the information, it reads it fresh each time, so it's always current. **Fine-tuning** modifies the model's weights on your data — the only technique that changes the model's behavior permanently, but also the most expensive to set up and the least flexible to update. In 2026, prompting + RAG handles 95%+ of use cases. Fine-tuning only wins when: (1) you have high daily call volume with a repetitive pattern, (2) your task requires very specific output format the base model won't follow reliably, or (3) you need to reduce latency by eliminating long system prompts.

| PT | EN |
|----|---|
| Ajuste fino | Fine-tuning |
| Engenharia de contexto | Context engineering |
| Geração aumentada por recuperação | Retrieval-Augmented Generation (RAG) |
| Índice vetorial | Vector index |
| Recuperador | Retriever |
| Ajuste fino com supervisão | Supervised Fine-Tuning (SFT) |
| Aprendizado de poucos exemplos | Few-shot learning |
| Aprendizado de nenhum exemplo | Zero-shot learning |
| Memorização catastrófica | Catastrophic forgetting |

## Ver mais

- **[Anthropic — Prompt Engineering Guide (2026)](https://docs.anthropic.com/en/docs/build-with-claude/prompt-engineering/overview)** — guia oficial com técnicas avançadas de context engineering. O ponto de partida antes de cogitar RAG ou fine-tuning.
- **[Lewis et al. — RAG: Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks (2020)](https://arxiv.org/abs/2005.11401)** — o paper fundador de RAG, que demonstrou que recuperar documentos e injetá-los no prompt supera o fine-tuning para tarefas de knowledge-intensive.
- **[Jerry Liu (LlamaIndex) — When to use RAG vs fine-tuning (2024)](https://www.llamaindex.ai)** — análise prática do criador do LlamaIndex: quando cada técnica ganha, com exemplos de arquiteturas reais de produção.

## Veja também

- [[06 - A janela de contexto]] — o limite que determina quando prompting não basta
- [[13 - Prompt caching e otimizações de API]] — otimizações para prompting de alta escala
- [[17 - O futuro dos LLMs — tendências 2026-2027]] — para onde essas técnicas estão evoluindo

## Referências

- **Lewis et al.** — *Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks* (Facebook AI, 2020). Paper fundador de RAG.
- **OpenAI** — *Fine-tuning Guide* (2026). Guia oficial com melhores práticas.
- **Anthropic** — *Prompt Engineering Guide* (2026). Referência para prompting avançado.
- **Pinecone** — *RAG Architecture Guide* (2026). Referência para implementação de RAG.
