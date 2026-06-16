---
title: "Fine-tuning na prática — LoRA, QLoRA, DPO"
created: 2026-06-15
updated: 2026-06-15
type: concept
progress: backlog
status: seedling
publish: true
tags:
  - anatomia-llm
  - ia
  - tokens
aliases:
  - Fine-tuning na prática
  - PEFT
  - LoRA
  - QLoRA
  - DPO
  - Adapters
  - Preference tuning
---

# Fine-tuning na prática — LoRA, QLoRA, DPO

> [!abstract] TL;DR
> A nota [[14 - Fine-tuning vs prompting vs RAG]] decide **quando** fine-tunar; esta mostra **como**. Três camadas. **Full fine-tuning** atualiza todos os pesos — máximo poder, custo proibitivo (precisa do modelo inteiro + estados do otimizador na memória). **PEFT** (parameter-efficient fine-tuning) congela o modelo base e treina só um punhado de pesos novos: **LoRA** injeta matrizes de baixo posto e treina <1% dos parâmetros; **QLoRA** põe LoRA em cima de um base quantizado em 4 bits, e aí um modelo de 65B fine-tuna numa única GPU. E depois do SFT vem o **alinhamento por preferência**: **DPO** substitui o RLHF (reward model + PPO) por uma perda direta sobre pares "resposta boa / resposta ruim" — mais barato e mais estável. A regra de bolso de 2026: **QLoRA para o SFT, DPO para o polimento**, full fine-tuning quase nunca.

## O que é

Fine-tuning é mudar os [[Dicionário de IA#parameters / weights|pesos]] do modelo — diferente de prompting/RAG, que só mexem no input (ver [[14 - Fine-tuning vs prompting vs RAG]]). Mas "fine-tuning" virou guarda-chuva para coisas bem diferentes. Vale separar **o que** você ensina de **como** você ensina:

- **SFT (Supervised Fine-Tuning)** — você dá pares `entrada → saída ideal` e o modelo aprende a imitar. Ensina **forma e comportamento**: formato de output, tom, jargão de domínio, seguir um schema. É o mesmo SFT do pipeline de treino de fronteira ([[16 - Como LLMs são treinados — pretraining, SFT, RLHF]]), só que num modelo já pronto e com seus dados.
- **Preference tuning** — em vez de uma resposta certa, você dá **duas** (uma melhor, uma pior) e ensina o modelo a preferir a melhor. Ensina **julgamento**: ser mais útil, menos prolixo, recusar o que deve recusar. DPO e RLHF vivem aqui.

> [!tip] O resumo de uma frase
> SFT ensina **a imitar um exemplo**; preference tuning ensina **a escolher entre dois**. As duas camadas mexem nos pesos — o que muda é o sinal de treino.

E há um eixo ortogonal: **quantos** pesos você toca. É aí que entram full FT, LoRA e QLoRA.

## Por que importa

| Motivação | Por que fine-tuning (e não prompt/RAG) |
| --- | --- |
| **Formato/estilo consistente em escala** | Um modelo fine-tuned "já nasce" no formato — sem gastar tokens de few-shot a cada chamada |
| **Latência e custo por chamada** | Prompt curto + modelo menor especializado bate prompt gigante num flagship |
| **Jargão e comportamento de domínio** | Padrões que nenhum prompt captura bem (clínico, jurídico, código interno) |
| **Soberania / on-prem** | Você é dono dos pesos — roda local ([[08 - Modelos locais e self-hosting]]), sem vazar dado para API |
| **Destilar um comportamento** | Capturar num modelo aberto o jeito de responder de um modelo maior (fronteira com [[18 - Compressão de modelos — quantização e destilação|destilação]]) |

> [!warning] Fine-tuning ensina forma, não fatos
> O erro clássico é fine-tunar para "ensinar conhecimento". Não funciona bem: o modelo memoriza ruído e alucina com confiança. Conhecimento que muda → **RAG**. Comportamento/formato estável → fine-tuning. Ver a árvore de decisão em [[14 - Fine-tuning vs prompting vs RAG]].

## Como funciona

### Full fine-tuning — o caminho caro

Atualiza **todos** os pesos. O problema não é a inferência, é o **treino**: com Adam em precisão mista, cada parâmetro custa ~16-20 bytes (pesos fp16 + gradientes fp16 + dois estados do otimizador em fp32 + master weights). Um modelo de **7B** já pede **~120GB** só de estado de treino — multi-GPU obrigatório. Além do custo, há o risco de **catastrophic forgetting**: ao reescrever tudo, o modelo esquece habilidades gerais. Por isso, fora de labs, full FT é raro.

### LoRA — treinar 1% e fingir que treinou tudo

A sacada (Hu et al., 2021): o **update** de peso durante o fine-tuning tem **posto intrínseco baixo** — ele não precisa de todos aqueles graus de liberdade. Então, em vez de aprender a matriz cheia `ΔW` (enorme), congela-se `W` e aprende-se `ΔW = B·A`, com `A` e `B` finas (posto `r` pequeno, tipo 8-64). Treina-se só `A` e `B` — **menos de 1% dos parâmetros**.

```
W_efetivo = W_congelado + (alpha/r)·B·A
            └─ não treina ─┘  └── treina (LoRA) ──┘
```

Consequências práticas:

- **Memória despenca** — sem estados de otimizador para bilhões de pesos; o grande custo vira só o base congelado em fp16 (~14GB para um 7B).
- **Adapters são plugáveis** — o `B·A` treinado é um arquivo de poucos MB. Você troca de "personalidade" trocando o adapter, sobre o **mesmo** base. Dá para ter dezenas.
- **Hiperparâmetros que importam:** `r` (posto — capacidade), `alpha` (escala do update), e os **target modules** (em quais projeções injetar — começa por `q_proj`/`v_proj`, expande para MLP se precisar).

### QLoRA — onde compressão e fine-tuning se encontram

QLoRA (Dettmers et al., 2023) leva LoRA ao extremo: **quantiza o base congelado para 4 bits** (formato NF4) e prende os adapters LoRA, em precisão maior, por cima. O gradiente passa **através** do base quantizado, mas só os adapters aprendem.

```
[Base 4-bit NF4 — congelado]  ──>  [Adapters LoRA — fp16, treináveis]
        ~3.5GB p/ um 7B                  poucos MB
```

Com *double quantization* e *paged optimizers*, isso põe o fine-tuning de um **33B/65B numa única GPU**. É a ponte literal com a nota [[18 - Compressão de modelos — quantização e destilação]]: a [[Dicionário de IA#fine-tuning|quantização]] aqui não é só para *rodar* barato, é para *treinar* barato. Em 2026, QLoRA é o default de quem fine-tuna modelo aberto fora de um cluster.

### DPO — alinhamento por preferência sem o circo do RLHF

Depois do SFT, você quer ajustar **julgamento**. O caminho clássico, o RLHF ([[16 - Como LLMs são treinados — pretraining, SFT, RLHF]]), treina um *reward model* e depois roda PPO — duas etapas, instável, caro de acertar. O **DPO** (Rafailov et al., 2023) reformula tudo como **uma perda direta**: dado um triplo `(prompt, resposta escolhida, resposta rejeitada)`, otimize o modelo para dar mais probabilidade à escolhida que à rejeitada — sem reward model, sem loop de RL.

Um **modelo de referência** congelado (o próprio SFT) segura a rédea (um termo de KL) para o modelo não desandar. Variantes que você vai encontrar:

- **IPO** — corrige uma tendência do DPO de "overfitar" a preferência.
- **KTO** — usa rótulos binários soltos (isto é bom / isto é ruim), sem precisar de **pares** — mais fácil de coletar dado.
- **ORPO** — funde SFT + preferência numa **única** etapa, sem modelo de referência. O mais enxuto dos pipelines.

## A pipeline típica de um modelo aberto

```
Base (Llama/Qwen/Mistral)
   │  SFT com QLoRA   → ensina formato e comportamento
   ▼
Modelo instruído
   │  DPO/ORPO        → alinha julgamento (útil, conciso, seguro)
   ▼
Modelo alinhado
   │  merge + quantiza (nota 18)
   ▼
Deploy local/edge (nota 08)
```

## Quando usar qual

| Situação | Técnica | Motivo |
| --- | --- | --- |
| Tenho cluster e preciso do máximo de qualidade | **Full fine-tuning** | Só aqui vale o custo; raro |
| SFT de um modelo aberto em 1 GPU | **QLoRA** | 4-bit + adapters = cabe e é barato |
| Várias especializações sobre um base | **LoRA (adapters)** | Troca de adapter, não de modelo |
| Polir comportamento depois do SFT | **DPO** (ou ORPO) | Alinhamento estável, sem reward model |
| Só tenho rótulos "bom/ruim" avulsos | **KTO** | Dispensa pares de preferência |
| Preciso de **conhecimento atualizado** | **Nada disso → [[14 - Fine-tuning vs prompting vs RAG\|RAG]]** | Fine-tuning não guarda fatos bem |

## Ferramentas (2026)

- **HuggingFace PEFT + TRL** — `peft` implementa LoRA/QLoRA; `trl` traz `SFTTrainer`, `DPOTrainer`, `ORPOTrainer`. O caminho de referência.
- **Axolotl** — fine-tuning dirigido por arquivo de config (YAML); popular para reprodutibilidade.
- **Unsloth** — kernels otimizados: ~2× mais rápido e menos VRAM que o baseline.
- **Llama-Factory** — UI + CLI cobrindo SFT/DPO/quantização num lugar só.
- **Managed** — OpenAI fine-tuning, Together, Fireworks, Predibase: você sobe o dataset, eles treinam (geralmente LoRA por baixo) e servem.

O formato do dado é metade do jogo: SFT pede pares `instrução → resposta`; DPO pede triplos `prompt / chosen / rejected`. Dado sujo = modelo pior.

## Armadilhas

- **"Fine-tuning é sempre melhor"** — é o mais caro e o menos flexível. Esgote prompting + RAG antes ([[14 - Fine-tuning vs prompting vs RAG]]).
- **Poucos dados, ou dados sujos** — 1.000 exemplos limpos batem 100.000 ruidosos. Abaixo de ~1k, costuma memorizar em vez de generalizar.
- **`r` mal calibrado** — posto alto demais overfita e desperdiça; baixo demais não aprende. Comece pequeno (8-16) e suba se o eval pedir.
- **Esquecer de avaliar no *seu* golden set** — benchmark genérico mente. Meça o modelo fine-tuned na sua tarefa ([[17 - Evaluation de LLMs em produção]]).
- **DPO sobre-otimizado** — preferência empurrada longe demais degrada qualidade geral; o termo de KL contra o modelo de referência existe para isso — não o zere.
- **Merge de LoRA em base quantizado** — fundir o adapter de volta num base 4-bit perde precisão; sirva o adapter separado ou faça o merge em fp16.
- **Destilar de API fechada** — treinar com saídas de um modelo comercial de terceiros costuma violar os ToS do provider (mesma armadilha da [[18 - Compressão de modelos — quantização e destilação|destilação]]).

## Veja também

- [[14 - Fine-tuning vs prompting vs RAG]] — **quando** fine-tunar (esta nota é o **como**)
- [[16 - Como LLMs são treinados — pretraining, SFT, RLHF]] — SFT e RLHF na escala de laboratório
- [[18 - Compressão de modelos — quantização e destilação]] — quantização (a base do QLoRA) e destilação
- [[08 - Modelos locais e self-hosting]] — onde o modelo fine-tuned vai rodar

## Referências

- **Hu et al.** — *LoRA: Low-Rank Adaptation of Large Language Models* (2021). [arxiv:2106.09685](https://arxiv.org/abs/2106.09685). O método PEFT dominante.
- **Dettmers et al.** — *QLoRA: Efficient Finetuning of Quantized LLMs* (2023). [arxiv:2305.14314](https://arxiv.org/abs/2305.14314). NF4, double quant, paged optimizers.
- **Rafailov et al.** — *Direct Preference Optimization* (2023). [arxiv:2305.18290](https://arxiv.org/abs/2305.18290). RLHF sem reward model.
- **Hong et al.** — *ORPO: Monolithic Preference Optimization without Reference Model* (2024). [arxiv:2403.07691](https://arxiv.org/abs/2403.07691).
- **HuggingFace** — *PEFT* e *TRL* (docs). Implementações de referência de LoRA/QLoRA e SFT/DPO/ORPO.
- **Unsloth** / **Axolotl** (GitHub) — toolchains de fine-tuning otimizadas e config-driven.
