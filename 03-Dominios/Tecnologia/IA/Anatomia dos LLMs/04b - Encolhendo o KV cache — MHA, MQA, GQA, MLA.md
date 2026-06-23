---
title: "Encolhendo o KV cache — MHA, MQA, GQA, MLA"
created: 2026-06-20
updated: 2026-06-20
type: concept
status: growing
fase: Magus
progress: in-progress
publish: true
tags:
  - anatomia-llm
  - ia
  - inferencia
  - kv-cache
aliases:
  - MHA
  - MQA
  - GQA
  - MLA
  - Multi-Query Attention
  - Grouped-Query Attention
  - Multi-head Latent Attention
---
# Encolhendo o KV cache — MHA, MQA, GQA, MLA

> [!info] Broto de [[04 - Atenção e o mecanismo transformer]]
> Nota **Magus**. Continuação direta de [[04a - KV cache, prefill e decode — a física da inferência|KV cache, prefill e decode]] — leia aquele broto primeiro: ele mostra *por que* o KV cache domina a memória do decode. Aqui a pergunta é o passo seguinte: **como encolher esse cache sem destruir a qualidade do modelo?**

> [!abstract] TL;DR
> Olhe a fórmula do tamanho do cache — `2 × L × n_kv × d_head × bytes`. Camadas (L) e dimensão por head (d_head) são fixas pela arquitetura. A **única alavanca real é n_kv**: quantos conjuntos de Key/Value o modelo precisa guardar. Boa parte da evolução da atenção nos últimos anos é uma briga por esse número. **MHA** (original) dá um K/V por head — qualidade máxima, cache máximo. **MQA** faz todos os heads dividirem um único K/V — cache mínimo, mas a qualidade cai. **GQA** é o meio-termo que venceu: grupos de heads compartilham K/V. **MLA** muda a estratégia: comprime K/V num vetor latente low-rank — cache *menor que o MQA* e qualidade *acima do MHA*.

## Por que isso importa

[[04a - KV cache, prefill e decode — a física da inferência|Você já viu]] que o KV cache de um contexto de 100k tokens em MHA puro não cabe numa H100. Sem uma solução para isso, contexto longo seria economicamente impossível e nenhum dos modelos de janela gigante existiria. Esta é a corrida de engenharia que tornou viável o que hoje parece banal — e cai em entrevista de qualquer vaga de infra de LLM.

## A única alavanca: n_kv

Olhe de novo a fórmula do cache: `2 × L × n_kv × d_head × bytes`. L e d_head são fixos pela arquitetura. A única alavanca real é **n_kv** — quantos conjuntos de Key/Value o modelo precisa guardar. Toda a tabela abaixo é uma forma diferente de mexer nesse número.

| Variante | Como compartilha K/V | KV cache | Trade-off |
| -------- | -------------------- | -------- | --------- |
| **MHA** (Multi-Head) | Cada head tem seu próprio K/V | Máximo (n_kv = n_heads) | Qualidade máxima, cache máximo |
| **MQA** (Multi-Query) | *Todos* os heads dividem **um** K/V | Mínimo (n_kv = 1) | Cache despenca, qualidade cai em escala |
| **GQA** (Grouped-Query) | Grupos de heads dividem K/V | Intermediário (n_kv = grupos) | O dial entre MHA e MQA |
| **MLA** (Multi-head Latent) | Comprime K/V num vetor latente low-rank | Menor que MQA | Cache mínimo *e* qualidade acima do MHA |

## A evolução, uma pancada de cada vez

- **MHA** é o original do paper de 2017: 32 heads → 32 conjuntos de K/V no cache. Cada head tem total liberdade para olhar para onde quiser, com seu próprio par Key/Value. Qualidade máxima — e cache caro.
- **MQA** foi a primeira pancada (Shazeer, 2019): e se *todos* os heads consultassem o **mesmo** K/V, variando só a Query? O cache encolhe ~n_heads vezes de uma só vez. O problema: com um único K/V, o modelo perde nuance e degrada conforme a escala cresce — barato demais, e a qualidade cobra.
- **GQA** é o meio-termo que venceu: divide os heads em **poucos grupos** (ex.: 32 heads em 8 grupos), cada grupo com seu K/V. Pega quase toda a economia do MQA sem a queda de qualidade. É o padrão de [[08 - Modelos chineses — DeepSeek, Qwen, Kimi, GLM|Qwen]], Llama 2/3 e Mistral — o dial sintonizado no ponto certo entre os dois extremos.
- **MLA** muda a estratégia em vez de só mexer no dial: em vez de cortar heads, **comprime** Key e Value juntos num vetor latente de baixa dimensão antes de cachear, e os reconstrói na hora da atenção. Cache menor que o do MQA e, surpreendentemente, qualidade *acima* do MHA — a compressão funciona como um gargalo regularizador. É a aposta da família [[08 - Modelos chineses — DeepSeek, Qwen, Kimi, GLM|DeepSeek]] (V2/V3).

> [!tip] A intuição do MLA em uma frase
> MQA/GQA economizam **jogando informação fora** (menos K/V distintos). MLA economiza **comprimindo** (guarda uma versão enxuta e reconstrói quando precisa) — por isso consegue cache pequeno *sem* o sacrifício de qualidade. É a diferença entre apagar fotos e zipar a pasta.

> [!question]- Dá para ligar GQA num modelo já treinado em MHA?
> Não dá para simplesmente "ativar" — mas dá para converter com *uptraining*: agrupam-se os K/V heads (média dos pesos) e re-treina-se com uma fração pequena do compute original (~5%) para o modelo se reacomodar. Foi assim que o Llama 2 ganhou suas versões GQA. Trocar a arquitetura de atenção não é de graça, mas é muito mais barato que treinar do zero.

| Variante | Redução de memória típica | Em produção |
| -------- | ------------------------- | ----------- |
| **GQA** | 2-8x menos que MHA | Llama 2/3, Mistral, Qwen |
| **MLA** | ~1 ordem de grandeza menor que MHA | DeepSeek-V2/V3 |

## Veja também

- [[04a - KV cache, prefill e decode — a física da inferência]] — por que o cache importa (pré-requisito desta nota)
- [[04 - Atenção e o mecanismo transformer]] — a nota-mãe: o que são os heads e o multi-head
- [[04c - Atenção eficiente — FlashAttention, sparse e híbrida]] — o outro ataque: a conta O(n²)
- [[08 - Modelos chineses — DeepSeek, Qwen, Kimi, GLM]] — MLA e GQA em produção
- [[09 - Dense vs Mixture-of-Experts]] — a outra grande alavanca de eficiência (FFN esparsa)

## Referências

- **Shazeer, Noam** — [*Fast Transformer Decoding: One Write-Head is All You Need*](https://arxiv.org/abs/1911.02150) (2019). O paper original do Multi-Query Attention.
- **Ainslie et al.** — [*GQA: Training Generalized Multi-Query Transformer Models from Multi-Head Checkpoints*](https://arxiv.org/abs/2305.13245) (Google, 2023). Grouped-Query Attention e o uptraining.
- **DeepSeek-AI** — [*DeepSeek-V2: A Strong, Economical, and Efficient Mixture-of-Experts Language Model*](https://arxiv.org/abs/2405.04434) (2024). Multi-head Latent Attention (MLA) e a compressão low-rank do KV cache.
