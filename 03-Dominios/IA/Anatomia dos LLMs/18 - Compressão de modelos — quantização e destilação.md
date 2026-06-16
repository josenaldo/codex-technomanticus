---
title: "Compressão de modelos — quantização e destilação"
created: 2026-06-14
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
  - Compressão de modelos
  - Quantização
  - Destilação
  - Knowledge distillation
  - GPTQ
  - AWQ
  - GGUF
---

# Compressão de modelos — quantização e destilação

> [!abstract] TL;DR
> Duas famílias de técnicas para encolher um modelo. **Quantização** reduz a precisão numérica dos pesos (FP16 → INT8 → INT4): mesma arquitetura, menos bits por número, aplicada quase sempre depois do treino. É barata e é a alavanca dominante para rodar LLMs localmente. **Destilação** treina um modelo "aluno" menor para imitar um "professor" maior: produz um modelo genuinamente menor, mas exige treino. As duas trocam um pouco de qualidade por tamanho, velocidade e custo, e costumam ser combinadas (destila e depois quantiza). É a engenharia por trás de por que existe um Haiku abaixo de um Opus — e por que um modelo de 7B pode caber no seu notebook.

## O que é

"Compressão de modelos" reúne técnicas que reduzem o tamanho e o custo de inferência de um [[Dicionário de IA#LLM (Large Language Model)|LLM]] sem treiná-lo do zero. As duas dominantes são ortogonais — atacam coisas diferentes:

- **Quantização** — reduz a **precisão** com que cada [[Dicionário de IA#parameters / weights|peso]] é armazenado. Um número que ocupava 16 bits (FP16) passa a ocupar 8 (INT8) ou 4 (INT4). A contagem de parâmetros e a arquitetura não mudam — muda quantos bits cada parâmetro custa. É como salvar um JPEG com mais compressão: mesma imagem, menos resolução.
- **Destilação (knowledge distillation)** — treina um modelo **aluno** (student), menor, para reproduzir o comportamento de um modelo **professor** (teacher), maior. O aluno é uma rede genuinamente menor, com menos parâmetros. É como um residente aprendendo a diagnosticar imitando um médico experiente, em vez de reler todos os livros de medicina.

> [!tip] O resumo de uma frase
> Quantização = **mesmo cérebro, resolução menor**. Destilação = **cérebro menor, treinado pra imitar o grande**.

## Por que importa

| Motivação | Como a compressão ajuda |
| --- | --- |
| **VRAM / hardware** | INT4 corta o uso de memória em ~4× vs FP16 — é o que faz um 70B caber em ~40GB (ver [[08 - Modelos locais e self-hosting]]) |
| **Custo de inferência** | Modelos menores leem menos pesos da memória por token → menos custo, contornando o [[Dicionário de IA#memory bandwidth bottleneck\|memory bandwidth bottleneck]] |
| **Latência** | Menos bits para mover e menos parâmetros para ler reduzem o tempo por token |
| **Edge / on-device** | Destilação + quantização é o que põe um modelo num celular ou navegador |
| **Economia dos tiers** | As variantes baratas das famílias (Haiku, Flash, Nano) são, em parte, fruto de destilação do flagship — ver [[Dicionário de IA#flagship model\|flagship model]] |

Isso desmonta o mito do *"maior é sempre melhor"* discutido em [[01 - O que é um LLM]]: um modelo de 7B bem quantizado e destilado de um bom professor vence um flagship genérico antigo em tarefas específicas — e roda de graça na sua máquina.

## Como funciona

### Quantização

A ideia é representar pesos (e às vezes ativações) com menos bits. Quanto menor a precisão, menor a memória — e maior o risco de degradar a qualidade.

| Formato | Bits/peso | VRAM relativa | Impacto na qualidade |
| --- | --- | --- | --- |
| FP32 | 32 | 4× | Referência (raro em inferência) |
| FP16 / BF16 | 16 | 2× | Baseline de produção |
| INT8 | 8 | 1× | Perda quase imperceptível |
| INT4 | 4 | ~0.5× | Perda perceptível em raciocínio complexo |
| INT2 / 1.58-bit | 2 / ~1.6 | ~0.25× | Experimental; só com QAT dedicado |

**Regra de bolso de VRAM:** pesos em GB ≈ nº de parâmetros (em bilhões) × bytes por peso. Um 13B em FP16 (2 bytes) ≈ 26GB; o mesmo em INT4 (0.5 byte) ≈ ~6.5GB. (Some KV cache e overhead por cima.)

**Quando se aplica:**

- **PTQ (Post-Training Quantization)** — quantiza um modelo já treinado. Barato, rápido, não precisa de dados de treino (ou só um pequeno conjunto de calibração). É o caminho comum.
- **QAT (Quantization-Aware Training)** — simula a quantização durante o treino, então o modelo "aprende" a conviver com a baixa precisão. Mais caro, melhor qualidade em bits muito baixos (INT4 e abaixo).

**Formatos que você vai encontrar na prática:**

- **GGUF** (llama.cpp) — formato dos *k-quants* (`Q4_K_M`, `Q5_K_M`, `Q8_0`). Padrão de fato para CPU/Apple Silicon e Ollama.
- **GPTQ** — PTQ baseado em informação de segunda ordem; popular para GPU.
- **AWQ** (Activation-aware Weight Quantization) — preserva os pesos mais salientes; usado pelo [[08 - Modelos locais e self-hosting|vLLM]] (`--quantization awq`).
- **bitsandbytes / NF4** — quantização 4-bit usada em [[Dicionário de IA#fine-tuning|QLoRA]] para fine-tuning em hardware modesto.

### Destilação

Em vez de mexer nos bits, treina-se um modelo novo e menor. A sacada (Hinton, Vinyals & Dean, 2015) é que o professor ensina mais do que o rótulo certo: a distribuição completa de probabilidades sobre o vocabulário — os *soft targets* — carrega "dark knowledge" (que "gato" é mais parecido com "cachorro" do que com "carro"). O aluno treina para imitar essa distribuição, geralmente com a [[Dicionário de IA#temperature|temperature]] dos [[Dicionário de IA#logit|logits]] elevada para suavizar e expor essa estrutura fina.

Tipos principais:

- **Response-based** — o aluno imita os logits/saídas finais do professor. O clássico.
- **Feature-based** — o aluno imita também representações de camadas intermediárias.
- **Sequence-level / data distillation** — para modelos generativos: o professor gera um corpus de saídas de alta qualidade e o aluno é treinado nele (a fronteira com geração de dados sintéticos é tênue).

**Marcos que valem citar:**

- **DistilBERT** (Sanh et al., 2019) — 40% menor, 60% mais rápido, retém ~97% do desempenho do BERT.
- **Distilling step-by-step** (Google, 2023) — um T5 de 770M iguala o PaLM 540B (redução de >700×) extraindo *rationales* do professor — citado em [[01 - O que é um LLM]].
- **Modelos "mini" de fronteira** — acredita-se que variantes leves de famílias comerciais sejam destiladas de seus flagships; é parte do que viabiliza o model tiering.

### Combinando as duas

Não são concorrentes. O pipeline de menor pegada é **destilar primeiro** (cérebro menor) **e quantizar depois** (cada peso mais barato). É assim que se chega a modelos que rodam em celular ou no navegador.

## Quando usar qual

| Situação | Técnica | Motivo |
| --- | --- | --- |
| Já tenho o modelo, só quero rodar em menos VRAM | **Quantização (PTQ)** | Barata, sem retreino, GGUF/AWQ resolvem |
| Preciso de qualidade em INT4/INT2 agressivo | **QAT** | Modelo aprende a tolerar baixa precisão |
| Quero um modelo menor e mais rápido para uma tarefa | **Destilação** | Aluno especializado bate genéricos maiores |
| Edge / on-device, pegada mínima | **Destilação + quantização** | As duas se somam |
| Adaptar a um domínio sem encolher | [[Dicionário de IA#fine-tuning\|Fine-tuning]] (não é compressão) | Objetivo é especializar, não reduzir |

## Armadilhas

- **INT4 degrada raciocínio** — para coding e raciocínio complexo, prefira INT8 ou `Q5_K_M`; INT4 é perceptivelmente pior (ver armadilhas em [[08 - Modelos locais e self-hosting]]).
- **"Modelo menor é de graça"** — destilação não é grátis: exige o professor e compute de treino. O barato é a *inferência* depois, não o processo.
- **O aluno herda os vícios do professor** — vieses, alucinações e lacunas do teacher passam adiante. Destilar de um modelo ruim produz um aluno ruim, menor.
- **Quantizar modelo já pequeno dói mais** — um 70B em INT4 sofre menos (proporcionalmente) que um 3B em INT4; modelos pequenos têm menos "gordura" de precisão para perder.
- **Perplexity ≠ desempenho na sua tarefa** — sempre meça o modelo comprimido no *seu* golden set (ver [[17 - Evaluation de LLMs em produção]]), não só em benchmarks genéricos.
- **Destilar de uma API fechada pode violar ToS** — treinar um aluno a partir das saídas de um modelo comercial de terceiros frequentemente esbarra nos termos de uso do provider. Verifique antes.

## Veja também

- [[01 - O que é um LLM]] — o mito "maior é melhor" e o caso T5/PaLM
- [[07 - Dense vs Mixture-of-Experts]] — outro eixo de eficiência (esparsidade vs precisão/tamanho)
- [[08 - Modelos locais e self-hosting]] — quantização aplicada na prática (VRAM, AWQ, k-quants)
- [[14 - Fine-tuning vs prompting vs RAG]] — adaptar ≠ comprimir
- [[19 - Fine-tuning na prática — LoRA, QLoRA, DPO]] — QLoRA fine-tuna sobre um base quantizado: compressão e treino se encontram

## Referências

- **Geoffrey Hinton, Oriol Vinyals, Jeff Dean** — *Distilling the Knowledge in a Neural Network* (2015). O paper fundador da destilação e dos soft targets.
- **Victor Sanh et al. (HuggingFace)** — *DistilBERT, a distilled version of BERT* (2019). Caso de referência prático.
- **Google Research** — [*Distilling Step-by-Step*](https://research.google/blog/distilling-step-by-step-outperforming-larger-language-models-with-less-training-data-and-smaller-model-sizes/) (2023). T5 770M ≈ PaLM 540B.
- **Frantar et al.** — *GPTQ: Accurate Post-Training Quantization* (2022).
- **Lin et al.** — *AWQ: Activation-aware Weight Quantization* (2023).
- **Dettmers et al.** — *QLoRA: Efficient Finetuning of Quantized LLMs* (2023). Introduz o formato NF4.
- **Georgi Gerganov** — *llama.cpp* (GitHub). Implementação de referência dos k-quants (GGUF).
