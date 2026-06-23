---
title: "Anatomia dos LLMs"
type: moc
publish: true
tags:
  - anatomia-llm
  - ia
  - moc
created: 2026-05-02
updated: 2026-06-20
aliases:
  - LLMs
  - Large Language Models
---

# Anatomia dos LLMs

[[Dicionário de IA#LLM (Large Language Model)|LLMs]] são a infraestrutura central da engenharia de software assistida por IA em 2026. Mas usar um LLM sem entender como ele funciona é como dirigir sem saber que o carro tem freio — funciona até o momento em que não funciona. Esta trilha percorre a anatomia completa: de como texto vira números (tokens) até por que uma sessão de agente custa $25 e como pagar $5. Cobre arquitetura, modelos em produção (incluindo o ecossistema chinês), APIs, pricing, treino, evaluation, e as técnicas que determinam se você gasta dinheiro ou queima dinheiro.

> [!info] Pré-requisitos
> Nenhum. Esta trilha é o ponto de entrada da [[03-Dominios/Tecnologia/IA/index|Formação Engenheiro de IA]]. Começa do zero e constrói progressivamente.

> [!warning] Preços e versões de modelos
> Os preços e versões de modelos mencionados refletem o estado de **maio de 2026**. Este campo muda a cada trimestre. Verifique sempre a documentação oficial do provider antes de tomar decisões de arquitetura.

> [!tip] O que diferencia um senior em LLMs
> 1. Tem modelo mental correto de tokenização e estima [[Dicionário de IA#Token|tokens]] de cabeça (~4 chars/token EN, ~3 PT-BR, mais para código)
> 2. Distingue pretraining, SFT e RLHF — sabe explicar por que um modelo recusa/aceita certos prompts
> 3. Entende [[Dicionário de IA#attention|attention]] e context window de forma prática — sabe por que "lost in the middle" acontece
> 4. Usa [[Dicionário de IA#temperature|`temperature`]], [[Dicionário de IA#top-p|`top_p`]], [[Dicionário de IA#top-k|`top_k`]] com intenção, não como mágica
> 5. Desenha prompts que retornam JSON válido consistentemente via [[Dicionário de IA#structured output|structured outputs]] + validação + retry
> 6. Sabe quando usar streaming vs não (UX vs facilidade de parsing)
> 7. Aplica [[Dicionário de IA#Prompt caching|prompt caching]] corretamente e mede impacto em custo
> 8. Faz **tiering** de modelos — roteia para Haiku/Flash o que der, escala para Opus/GPT-5 o necessário
> 9. Mede tudo: tokens in/out, latência, custo, taxa de erro
> 10. Trata LLM como **fonte não-confiável** — valida, faz retry, tem fallback, não confia em "parece ok"

## Comece por aqui

Trilha sequencial recomendada — leia na ordem para construir do conceito até a decisão prática.

### Bloco 1 — Fundamentos do Transformer

O alicerce. O que é um LLM, como texto vira tokens, o mecanismo que faz tudo funcionar, como o texto sai token a token, e o que limita o que o modelo "vê".

- [[01 - O que é um LLM]] — definição, categorias (dense vs MoE), estado da arte 2026
- [[02 - Tokens e tokenização]] — BPE, vocabulário, como texto vira números, custos por token
- [[03 - Embeddings — do token ao vetor]] — como o ID do token vira um vetor com significado; geometria do significado; estático vs contextual
- [[04 - Atenção e o mecanismo transformer]] — self-attention, Q/K/V, softmax, máscara causal, multi-head, FFN *(núcleo conceitual)*
	- [[04a - KV cache, prefill e decode — a física da inferência]] — *(Magus)* custo quadrático, prefill vs decode, o KV cache
	- [[04b - Encolhendo o KV cache — MHA, MQA, GQA, MLA]] — *(Magus)* as variantes de atenção que reduzem o cache
	- [[04c - Atenção eficiente — FlashAttention, sparse e híbrida]] — *(Magus)* atacando o custo O(n²); attention sinks
- [[05 - Completação — o loop autoregressivo]] — logits, softmax na saída, amostragem (greedy/top-k/top-p/temperatura), o loop token a token
- [[06 - A janela de contexto]] — input vs output tokens, limites reais, "lost in the middle"

### Bloco 2 — Modelos em Produção

Quem compete com quem, quanto custam, e quando usar cada um.

- [[07 - Panorama de modelos 2026]] — GPT-5.x, Claude 4.x, Gemini 3.x, Llama 4, benchmarks
- [[08 - Modelos chineses — DeepSeek, Qwen, Kimi, GLM]] — os players open-weight que mudaram o mercado
- [[09 - Dense vs Mixture-of-Experts]] — a escolha arquitetural que define custo e performance
- [[10 - Modelos locais e self-hosting]] — Ollama, vLLM, hardware, quando vale a pena

### Bloco 3 — APIs e Infraestrutura

Como a comunicação funciona, quanto custa, e como gastar menos.

- [[11 - APIs de LLM — anatomia de uma chamada]] — request/response, roles, temperature, tools
- [[12 - Pricing de APIs — como calcular custos]] — fórmulas, tabelas de preço, custos ocultos
- [[13 - Prompt caching e otimizações de API]] — caching, Batch API, model routing, compressão
- [[14 - Streaming, batching e latência]] — TTFT, TPOT, SSE, otimizações de inferência

### Bloco 4 — Conceitos Avançados

O que muda quando modelos "pensam", quando customizar, e para onde tudo isso vai.

- [[15 - Reasoning models e chain-of-thought]] — o1/o4, Claude Thinking, custos de reasoning
- [[16 - Fine-tuning vs prompting vs RAG]] — árvore de decisão para adaptação de LLMs
- [[17 - O futuro dos LLMs — tendências 2026-2027]] — agentes, contexto infinito, commoditização

### Bloco 5 — Treino e Avaliação

Como modelos chegam ao comportamento que você vê — e como medir se estão funcionando em produção.

- [[18 - Como LLMs são treinados — pretraining, SFT, RLHF]] — o pipeline canônico, Constitutional AI, DPO
- [[19 - Evaluation de LLMs em produção]] — golden set, LLM-as-judge, traces, A/B test

### Bloco 6 — Eficiência, compressão e customização (avançado)

Como modelos ficam menores, mais baratos, rodáveis localmente e adaptados ao seu caso — o lado avançado do Nível 5.

- [[20 - Compressão de modelos — quantização e destilação]] — reduzir precisão (quantização) e treinar alunos menores (destilação)
- [[21 - Fine-tuning na prática — LoRA, QLoRA, DPO]] — como customizar os pesos: PEFT/LoRA/QLoRA e alinhamento por preferência (DPO)

## Rotas alternativas

### Rota custo-zero (começar sem gastar)

*"Quero rodar IA localmente sem pagar API"*

[[01 - O que é um LLM]] → [[02 - Tokens e tokenização]] → [[10 - Modelos locais e self-hosting]] → [[12 - Pricing de APIs — como calcular custos]]

### Rota arquiteto (entender para projetar sistemas)

*"Preciso tomar decisões técnicas sobre qual modelo e infra usar"*

[[04 - Atenção e o mecanismo transformer]] → [[06 - A janela de contexto]] → [[09 - Dense vs Mixture-of-Experts]] → [[11 - APIs de LLM — anatomia de uma chamada]] → [[14 - Streaming, batching e latência]]

### Rota decisor (escolher e comprar)

*"Preciso decidir qual modelo usar no meu projeto"*

[[07 - Panorama de modelos 2026]] → [[08 - Modelos chineses — DeepSeek, Qwen, Kimi, GLM]] → [[12 - Pricing de APIs — como calcular custos]] → [[16 - Fine-tuning vs prompting vs RAG]]

### Rota otimização (reduzir custos)

*"Já uso LLMs e quero gastar menos"*

[[02 - Tokens e tokenização]] → [[12 - Pricing de APIs — como calcular custos]] → [[13 - Prompt caching e otimizações de API]] → [[15 - Reasoning models e chain-of-thought]]

### Rota produção (do POC ao deploy confiável)

*"Quero levar LLM para produção com observabilidade real"*

[[11 - APIs de LLM — anatomia de uma chamada]] → [[18 - Como LLMs são treinados — pretraining, SFT, RLHF]] → [[19 - Evaluation de LLMs em produção]] → [[Economia de Tokens|04 - Monitoramento — ccusage, Langfuse, dashboards]]

## Trilha de aprendizado em 5 níveis (do zero ao domínio)

> [!example] Roadmap prático
>
> ### Nível 1 — Intuição (3-5 dias)
> Use ChatGPT/Claude/Gemini pesadamente em problemas reais. Observe quando acertam, quando alucinam, quando são chatos demais.
>
> **Leitura:** [The Illustrated Transformer (Jay Alammar)](https://jalammar.github.io/illustrated-transformer/), [3Blue1Brown — But what is a GPT?](https://www.3blue1brown.com/lessons/gpt).
>
> **Check:** consegue explicar "atenção" usando analogia concreta?
>
> ### Nível 2 — Conceitos técnicos (2-3 semanas)
> Tokenização, embeddings, context window, parâmetros da API, pretraining → SFT → RLHF, limitações.
>
> **Leitura:** [State of GPT — Andrej Karpathy](https://www.youtube.com/watch?v=bZQun8Y4L2A) (clássico).
>
> **Check:** lê resposta do LLM e tem intuição do porquê ele respondeu assim.
>
> ### Nível 3 — API hands-on (3-4 semanas)
> Construa scripts com Anthropic e OpenAI: chat, streaming, tool use, structured outputs. Implemente golden set + evaluation. Compare latência e custo entre 3 modelos. Implemente prompt caching e meça impacto.
>
> **Check:** consegue levantar uma integração LLM em produção com confiança.
>
> ### Nível 4 — Produção (1-2 meses)
> Observabilidade (Langfuse/Helicone/LangSmith), guardrails (PII, output filtering, prompt injection), retry/fallback/timeout, rate limits, cost management.
>
> **Check:** assume ownership de um serviço LLM-backed.
>
> ### Nível 5 — Avançado (ongoing)
> [[21 - Fine-tuning na prática — LoRA, QLoRA, DPO|Fine-tuning quando justificado (LoRA, QLoRA, DPO)]], LLMs locais (Ollama, vLLM), [[20 - Compressão de modelos — quantização e destilação|quantização/destilação]], evaluation profunda (LLM-as-judge, A/B test), papers (Attention is All You Need, InstructGPT, LLaMA, etc).

## Leituras recomendadas

| Fonte                                       | Autor               | Tipo            | Cobertura                            |
| ------------------------------------------- | ------------------- | --------------- | ------------------------------------ |
| *Attention Is All You Need*                 | Vaswani et al.      | Paper           | Bloco 1 — arquitetura Transformer    |
| *Build a Large Language Model from Scratch* | Sebastian Raschka   | Livro           | Blocos 1-2 — construção prática      |
| *Let's build GPT from scratch*              | Andrej Karpathy     | Vídeo (YouTube) | Bloco 1 — implementação completa     |
| *Let's build the GPT tokenizer*             | Andrej Karpathy     | Vídeo (YouTube) | Nota 02 — BPE do zero                |
| *3Blue1Brown — Transformers explained*      | Grant Sanderson     | Vídeo (YouTube) | Nota 04 — visualização de atenção    |
| *DeepSeek-V3 Technical Report*              | DeepSeek AI         | Paper           | Notas 08-09 — MoE e modelos chineses |
| *LLM Cost Comparison*                       | Artificial Analysis | Site            | Notas 12-13 — pricing atualizado     |
| *InstructGPT paper*                         | OpenAI              | Paper           | Nota 18 — fundamento do RLHF         |
| *Constitutional AI*                         | Anthropic           | Paper           | Nota 18 — alignment via princípios   |
| *AI Engineering*                            | Chip Huyen          | Livro (2025)    | Notas 18-19 — eval e produção        |

## How to explain in English

> [!note] Elevator pitch
> *"LLMs are transformer-based neural networks trained to predict the next token. From that objective emerges remarkable language and code abilities. For production, the right framing is treating them as **stochastic functions with untyped outputs** — structured outputs, validation, retries, evaluation, and observability are not optional, they're the same engineering discipline applied to any unreliable dependency."*

### Talking points por tópico

- **On hallucination:** *"Mitigated with RAG and citations, structured outputs for format stability, and LLM-as-judge for fact verification. Features should be designed assuming hallucination will happen — nothing critical relies on the LLM being right."*
- **On cost:** *"Prompt caching and model tiering are the biggest wins. Caching a 4-5K-token system prompt typically cuts feature cost by 80%+."*
- **On evaluation:** *"Prompts without evals are superstition. Golden sets run on every prompt change is the bare minimum."*
- **On context window:** *"1M tokens sounds great until you benchmark lost-in-the-middle. RAG-filtered 8K usually beats raw dumps."*

### Vocabulário-chave

| PT-BR | EN |
|---|---|
| modelo de linguagem grande | large language model (LLM) |
| transformador | transformer |
| atenção / auto-atenção | attention / self-attention |
| tokenização | tokenization |
| pré-treinamento | pretraining |
| ajuste fino supervisionado | supervised fine-tuning (SFT) |
| aprendizado por reforço com feedback humano | reinforcement learning from human feedback (RLHF) |
| alucinação | hallucination |
| janela de contexto | context window |
| corte de conhecimento | knowledge cutoff |
| temperatura | temperature |
| amostragem | sampling |
| amostragem por núcleo | nucleus sampling (top-p) |
| saída estruturada | structured output |
| cache de prompt | prompt caching |
| uso de ferramenta | tool use / function calling |
| conjunto dourado | golden set |
| juiz LLM | LLM-as-judge |
| tempo até o primeiro token | time to first token (TTFT) |
| não-determinismo | non-determinism |
| injeção de prompt | prompt injection |

## Todas as notas

```dataview
TABLE
  title AS "Título",
  status AS "Status",
  join(tags, ", ") AS "Tags"
FROM "03-Dominios/Tecnologia/IA/Anatomia dos LLMs"
WHERE type != "moc"
SORT file.name ASC
```
