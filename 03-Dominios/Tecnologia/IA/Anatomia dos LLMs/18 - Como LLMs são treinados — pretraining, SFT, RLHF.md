---
title: "Como LLMs são treinados — pretraining, SFT, RLHF"
created: 2026-04-11
updated: 2026-07-03
type: concept
progress: done
status: growing
publish: true
tags:
  - anatomia-llm
  - ia
  - treino
  - rlhf
  - alignment
aliases:
  - LLM training pipeline
  - Pretraining SFT RLHF
  - Como modelos são treinados
  - Constitutional AI
---

# Como LLMs são treinados — pretraining, SFT, RLHF

> [!abstract] TL;DR
> O pipeline canônico tem **quatro estágios** que explicam quase todo o comportamento que você vê na API. **Pretraining** "decora a internet" (predict next token, custo de centenas de milhões em compute). **SFT** ensina formato de assistente. **RLHF** alinha com preferências humanas. **Constitutional AI** (Anthropic) reduz dependência de labelers via princípios escritos. Saber esse pipeline explica por que modelos são bajuladores, recusam tarefas inofensivas, e por que [[Dicionário de IA#fine-tuning|fine-tuning]] posterior muda menos do que você espera.

## O comportamento que você vê são camadas, não traços

Você usa Claude todos os dias e percebe padrões de comportamento estranhos: começa respostas com "Certamente!", às vezes recusa uma tarefa perfeitamente razoável, insiste em disclaimers quando você não pediu, e de vez em quando "alucina" um fato com absoluta confiança. Esses comportamentos parecem aleatórios, mas cada um vem de um estágio diferente do treinamento.

- O "Certamente!" e a bajulação → **RLHF**: humanos avaliadores deram feedback positivo para respostas afirmativas e amigáveis
- A recusa excessiva → **RLHF + Constitutional AI**: calibração de safety às vezes excessivamente conservadora
- A alucinação confiante → **Pretraining**: o modelo aprendeu a prever texto plausível, não a saber quando não sabe
- A qualidade geral da resposta → **SFT**: o formato de assistente foi ensinado aqui

Entender essas camadas tem valor prático: saber que recusas excessivas são artefatos de RLHF e não do modelo base significa que um system prompt claro frequentemente as reverte. Saber que alucinação vem do mecanismo central de pretraining significa que não há "modo de certeza" — RAG ou tool use são as únicas soluções reais.

## O pipeline em uma imagem

```mermaid
graph LR
    A["1️⃣ Pretraining<br/>(decorar a internet)"] --> B["2️⃣ SFT<br/>(virar assistente)"]
    B --> C["3️⃣ RLHF<br/>(alinhar com preferências)"]
    C --> D["4️⃣ Constitutional AI<br/>(princípios escritos)"]
```

Cada estágio adiciona uma camada de comportamento. **Não substitui** a anterior — modula.

## Estágio 1 — Pretraining

> *"Decorando a internet."*

| Aspecto | Detalhe |
|---|---|
| **Dados** | Trilhões de [[Dicionário de IA#Token\|tokens]] (web, livros, código, papers) |
| **Objetivo** | Dado N tokens, prever o N+1 |
| **Resultado** | Modelo "sabe" quase tudo sobre linguagem, fatos comuns, código — mas **não sabe ajudar** |
| **Custo** | Dezenas a centenas de milhões de dólares em GPU-anos |
| **Duração** | Semanas a meses em milhares de GPUs |

**Como se comporta um modelo só com pretraining:**

```
User: "A capital da França é"
Model: "Paris. A capital da Alemanha é Berlim. A capital da Espanha é Madri..."
```

Ele continua o padrão. **Não responde** à sua pergunta como assistente — completa texto plausível.

> [!info] Por que isso importa para você
> Todos os "fatos" do modelo vêm daqui. Knowledge cutoff = data dos dados de pretraining. Bias dos dados → bias do modelo. **Não é "bug" — é o mecanismo central.**

## Estágio 2 — Supervised Fine-Tuning (SFT)

> *"Aprendendo a ser assistente."*

| Aspecto | Detalhe |
|---|---|
| **Dados** | Milhares a centenas de milhares de pares `(pergunta, resposta ideal)` escritos por humanos |
| **Objetivo** | Ajustar para responder em formato de assistente |
| **Resultado** | Modelo agora **responde** "A capital da França é Paris" quando perguntado |
| **Custo** | Pequena fração do pretraining |
| **Duração** | Dias |

**A mudança de comportamento é dramática.** O mesmo modelo que continuava listando capitais agora responde *uma* pergunta com *uma* resposta.

**Quem faz SFT:**

- Anthropic, OpenAI, Google, Meta — internamente
- Comunidade open source — datasets como Anthropic HH-RLHF, OpenAssistant
- Você pode fazer SFT em modelos open source (LoRA, QLoRA, full fine-tuning)

## Estágio 3 — RLHF (Reinforcement Learning from Human Feedback)

> *"Aprendendo o que humanos preferem."*

```mermaid
graph TB
    A["Modelo gera<br/>respostas A e B"] --> B["Humano ranqueia:<br/>A é melhor que B"]
    B --> C["Treinar reward model<br/>que prediz preferência"]
    C --> D["Otimizar LLM via RL (PPO, DPO)<br/>para maximizar reward"]
```

| Aspecto | Detalhe |
|---|---|
| **Processo** | Humanos comparam respostas; treina-se *reward model*; LLM é otimizado via RL para maximizar reward |
| **Algoritmos** | PPO (Proximal Policy Optimization), DPO (Direct Preference Optimization, mais novo) |
| **Resultado** | Modelo útil, honesto, inofensivo — mais alinhado com expectativas humanas |
| **Custo** | Caro em human labelers |

**Side effects negativos do RLHF:**

- **Bajulação** — modelo aprende que humanos gostam de elogios
- **Hedging excessivo** — "isso depende de muitos fatores", "sou apenas um modelo de linguagem"
- **Recusa precaucionária** — recusa tarefas inofensivas por excesso de safety
- **Mode collapse** — diversidade de output reduz; respostas se parecem demais
- **Sycophancy** — concorda com o usuário mesmo quando deveria discordar

> [!warning] Comportamentos "chatos" são RLHF, não pretraining
> Se o modelo está se desculpando demais, hedging, ou recusando tarefas razoáveis — isso é artefato de RLHF, não falha do modelo base. **System prompt claro pode reverter** boa parte desses comportamentos.

## Estágio 4 — Constitutional AI (Anthropic)

> *"Princípios escritos no lugar de mais labelers."*

Específico da Anthropic, mas a ideia se espalhou em variantes.

| Aspecto | Detalhe |
|---|---|
| **Processo** | Conjunto de princípios escritos guia o **próprio modelo** a auto-avaliar respostas |
| **Princípios** | Exemplos: *"Be helpful, harmless, honest"*, *"Avoid sycophancy"*, *"Cite uncertainty"* |
| **Resultado** | Claude tende a ser mais consistente em recusas, mais transparente sobre seu raciocínio, menos bajulador |
| **Vantagem** | Reduz dependência de labelers humanos para safety; escala melhor |

**Implicações:** Claude tem comportamentos sutilmente diferentes de GPT — não por ser "mais inteligente", mas por ter passado por Constitutional AI em vez de só RLHF tradicional.

## Variantes recentes (2025-2026)

### DPO (Direct Preference Optimization)

Substitui RLHF tradicional. Em vez de treinar reward model + RL, otimiza diretamente do dataset de preferências. **Mais simples, mais barato, comparável em qualidade.** Adoção crescente.

> [!warning] DPO herda os defeitos do dataset de preferências
> DPO elimina o reward model, mas isso remove uma camada de filtro: sem reward model intermediário, o modelo otimiza direto sobre os pares de preferência anotados. Se o dataset tem anotadores inconsistentes, vieses sistemáticos (ex: preferir respostas mais longas só porque "parecem mais completas") ou poucas comparações difíceis, o modelo aprende exatamente esse viés — sem nada no meio para suavizar. **A qualidade do DPO é a qualidade do dataset de preferências, ponto.**

### RLAIF (RL from AI Feedback)

Usa outro LLM como labeler em vez de humano. Reduz custo. Cuidado: viés do labeler-LLM se propaga.

### Mixture of Experts pós-training

Para modelos MoE (DeepSeek, Mixtral), pós-training tem cuidados específicos com routing dos experts.

### Long-context fine-tuning

Modelos modernos (Claude 200K+, Gemini 1M+, GPT-5) precisam de SFT/RLHF em prompts longos para evitar [[06 - A janela de contexto|context rot]] muito severo.

## Escala do treinamento: comparando os estágios

Os quatro estágios têm custos, durações e volumes de dados radicalmente diferentes. Entender essas proporções ajuda a calibrar expectativas:

```mermaid
xychart-beta
    title "Volume de dados por estágio de treinamento (escala relativa)"
    x-axis ["Pretraining", "SFT", "RLHF", "Constitutional AI"]
    y-axis "Volume relativo (log scale)" 0 --> 100
    bar [100, 2, 5, 1]
```

| Estágio | Dados | Custo estimado | Duração |
|---|---|---|---|
| **Pretraining** | Trilhões de tokens (web, livros, código) | $10M–$500M | Meses em milhares de GPUs |
| **SFT** | 10k–500k pares de instrução/resposta | $10k–$500k | Dias |
| **RLHF** | 100k–1M comparações humanas | $1M–$10M (labelers) | Semanas |
| **Constitutional AI** | Princípios escritos + self-play | Menor que RLHF | Dias |

A implicação: **pretraining domina**. Todo o conhecimento e capacidade do modelo vem de lá. SFT, RLHF e CAI são ajustes finos de comportamento — não adicionam conhecimento novo, ajustam como o modelo o aplica.

## Implicações práticas para você

### 1. Fine-tuning posterior do usuário muda **pouco**

LoRA/QLoRA em cima de modelos comerciais ajusta margens. Não espere alteração radical de personalidade ou novas capacidades — pretraining domina.

### 2. Prompt engineering vence quase sempre

99% das diferenças que você quer ver no comportamento são reveladas por prompt + system message. Antes de pensar em fine-tune, exauste prompt engineering ([[Context Engineering|15 - Técnicas de prompting — zero-shot, few-shot, CoT, ToT]]).

### 3. Recusas são reverssíveis (parcialmente)

Se modelo recusa tarefa inofensiva, system prompt explicando contexto resolve em ~80% dos casos. Não é sempre "limitação do modelo" — é cautela do RLHF.

### 4. Knowledge cutoff é fixo

O modelo só sabe o que estava nos dados de pretraining + uma pequena janela de SFT. Para info recente: [[Dicionário de IA#RAG (Retrieval-Augmented Generation)|RAG]] ou [[Dicionário de IA#tool use|tool use]] (web search). Não tem como o modelo "saber" o que não viu.

### 5. Modelos diferentes têm pós-training diferente

| Modelo | Pós-training característico |
|---|---|
| **Claude** | Constitutional AI + RLHF — mais conservador, mais transparente |
| **GPT** | RLHF clássico + DPO — mais "agradável" |
| **Gemini** | RLHF + Google internal alignment |
| **Llama** | SFT + DPO open — diretamente otimizável |
| **DeepSeek** | RL focado em raciocínio — mais "raw" |

Escolha de modelo é também escolha de **persona** moldada pelo pós-training.

## Quando faz sentido fine-tune?

| Situação | Vale fine-tune? |
|---|---|
| Mudar tom de voz / persona | ✅ LoRA basta |
| Domínio jurídico/médico com vocabulário específico | ✅ Sim, com cuidado |
| Adicionar conhecimento factual | ❌ Não — use RAG |
| "Tornar o modelo mais inteligente" | ❌ Impossível — pretraining é fixo |
| Prompt está longo e caro | ⚠️ Considere fine-tune para encurtar |
| Adicionar nova skill emergente | ❌ Improvável de funcionar |

Ver [[16 - Fine-tuning vs prompting vs RAG]] para árvore de decisão.

> [!warning] Fine-tuning não adiciona conhecimento — ajusta comportamento
> É a armadilha mais comum de quem chega no fine-tuning esperando "ensinar fatos novos" ao modelo. SFT, RLHF, DPO e LoRA/QLoRA operam **depois** do pretraining, que já fixou o conhecimento factual do modelo. Esses estágios reajustam pesos para mudar *como* o modelo responde (tom, formato, o que recusa) — não *o que* ele sabe. Se o objetivo é conhecimento novo ou atualizado, a ferramenta certa é [[Dicionário de IA#RAG (Retrieval-Augmented Generation)|RAG]] ou tool use, não fine-tune.

## Como explicar em inglês

LLM training has four sequential stages that explain almost all model behavior. **Pretraining** trains on trillions of internet tokens to predict the next token — the model learns language, facts, and code but doesn't know how to be an assistant. **SFT** (Supervised Fine-Tuning) trains on thousands of instruction-response pairs written by humans, teaching the model to answer in assistant format. **RLHF** (Reinforcement Learning from Human Feedback) trains a reward model from human preference comparisons, then uses RL (usually PPO or DPO) to optimize the LLM to maximize that reward — producing helpful, harmless, honest behavior, but also side effects like sycophancy and excessive refusals. **Constitutional AI** (Anthropic-specific) uses a written set of principles and the model itself as an evaluator to reduce dependence on human labelers. The key engineering insight: most of a model's capability comes from pretraining; the other stages shape *how* it applies that capability, not how much it has.

| PT | EN |
|----|---|
| Pré-treinamento | Pretraining |
| Ajuste fino supervisionado | Supervised Fine-Tuning (SFT) |
| Aprendizado por reforço com feedback humano | Reinforcement Learning from Human Feedback (RLHF) |
| IA constitucional | Constitutional AI |
| Modelo de recompensa | Reward model |
| Otimização de política proximal | Proximal Policy Optimization (PPO) |
| Otimização direta de preferência | Direct Preference Optimization (DPO) |
| Bajulação | Sycophancy |
| Esquecimento catastrófico | Catastrophic forgetting |
| Labeler | Human labeler / human rater |

## Ver mais

- **[Andrej Karpathy — State of GPT (2023)](https://www.youtube.com/watch?v=bZQun8Y4L2A)** — a apresentação canônica do pipeline de treinamento. Karpathy explica cada estágio com diagramas, incluindo os side effects do RLHF e por que DPO está substituindo PPO. Ainda é a melhor introdução ao tema.
- **[Ouyang et al. — InstructGPT (2022)](https://arxiv.org/abs/2203.02155)** — o paper da OpenAI que introduziu RLHF para LLMs (base do ChatGPT). Mostra a diferença de comportamento entre modelo só com pretraining vs modelo com SFT vs modelo com RLHF.
- **[Anthropic — Constitutional AI (2022)](https://www.anthropic.com/research/constitutional-ai-harmlessness-from-ai-feedback)** — o paper descrevendo como a Anthropic usa princípios escritos e o próprio modelo como avaliador, reduzindo dependência de labelers humanos para safety.

## O que vem a seguir

Saber como o pipeline de treinamento molda o comportamento do modelo é só metade do trabalho — a outra metade é medir se esse comportamento é bom o suficiente para produção. As mesmas camadas discutidas aqui (bajulação do RLHF, alucinação do pretraining, recusas excessivas) são exatamente os fenômenos que os benchmarks e avaliações de [[19 - Evaluation de LLMs em produção]] tentam capturar antes que cheguem ao usuário final.

## Veja também

- [[01 - O que é um LLM]]
- [[16 - Fine-tuning vs prompting vs RAG]]
- [[19 - Evaluation de LLMs em produção]]
- [[21 - Fine-tuning na prática — LoRA, QLoRA, DPO]]

## Referências

- **OpenAI** — *InstructGPT paper* (2022) — fundamento do RLHF.
- **Anthropic** — *Constitutional AI: Harmlessness from AI Feedback* (2022).
- **Rafailov et al.** — *Direct Preference Optimization* (2023).
- **Karpathy** — *State of GPT* (2023, ainda relevante).
- **HuggingFace** — *RLHF: Reinforcement Learning from Human Feedback* (blog).
