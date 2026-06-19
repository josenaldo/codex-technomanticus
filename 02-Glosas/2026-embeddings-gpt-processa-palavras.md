---
title: "Você Não Sabe Como o GPT Processa Cada Palavra"
aliases: ["Você Não Sabe Como o GPT Processa Cada Palavra"]
source: https://youtube.com/watch?v=_G_--YC5Xd4
author: Sandeco Channel - Decomplicated IA
site: YouTube
channel: Sandeco Channel - Decomplicated IA
video_id: _G_--YC5Xd4
duration: "00:18:20"
published: 2025-02-17
read: 2026-06-18
type: glosa
progress: backlog
status: lido
tags: [embeddings, llm, transformers, representacao-vetorial, janela-de-contexto]
lang: pt
publish: false
---

# Você Não Sabe Como o GPT Processa Cada Palavra — Sandeco Channel - Decomplicated IA

> [!info] Vídeo
> [▶ Assistir no YouTube](https://youtube.com/watch?v=_G_--YC5Xd4) · 18:20 · Sandeco Channel - Decomplicated IA

## TL;DR

Embeddings são a ponte entre palavras (mundo humano) e números (mundo computacional). Cada token é mapeado para um vetor de números reais — iniciado de forma aleatória e otimizado via backpropagation durante o treinamento. O tamanho desse vetor (hiperparâmetro `d_model`) define diretamente a quantidade de parâmetros da rede. O vídeo também introduz o conceito de janela de contexto: a quantidade máxima de tokens que um Transformer processa por solicitação.

## Pontos-chave

- Embeddings são a solução para ligar texto a cálculo: cada token vira uma linha de uma tabela (matriz) onde as colunas são valores numéricos — iniciados aleatoriamente e refinados pelo backpropagation até capturar semântica.
- O hiperparâmetro `d_model` define o tamanho do embedding (número de valores por token): BERT usa 768, GPT-2 usa 1.024, GPT-3 usa 12.288 — e é exatamente esse número que determina a contagem de parâmetros da rede (BERT: 340M; GPT-3: 175B).
- O valor de `d_model` é sempre par — requisito importante para o mecanismo de positional encoding que combina seno e cosseno em pares.
- Tokens que se repetem no texto ainda recebem o mesmo embedding base; a distinção por contexto e posição virá dos mecanismos seguintes (positional encoding + atenção).
- Janela de contexto é a quantidade de tokens processados por solicitação: GPT tem 128.000; o Gemini 2, segundo o vídeo, "2 bilhões" — **lapso do apresentador**: a janela real do Gemini é ~2 **milhões** (ele próprio cita "2 milhões" mais adiante). Uma janela pequena faz o modelo "esquecer" contexto anterior, degradando a coerência da resposta.
- O backpropagation encontra os melhores pesos dos embeddings por tentativa e erro: começa aleatório, propaga, mede o erro, retropropaga ajustando os valores — repetindo até convergir.
- Embeddings são a base de técnicas como RAG (Retrieval-Augmented Generation): transformar texto em vetores permite calcular similaridade semântica entre documentos e recuperar os mais relevantes.

## Momentos-chave

- [00:00] — Apresentação: "o ser humano é bom com palavras, o computador é bom com números"
- [01:33] — Embeddings como ponte entre palavras e LLMs; uso em RAG
- [02:22] — Embedding de tokens: cada token vira uma coluna (feature) de uma tabela
- [03:14] — Geração de valores aleatórios iniciais: redes neurais aprendem pela aleatoriedade
- [04:36] — `d_model`: tamanho do embedding define quantidade de parâmetros
- [06:15] — Comparação: BERT (768, 340M params), GPT-2 (1024, 1,5B), GPT-3 (12.288, 175B)
- [09:40] — Janela de contexto: quantidade de tokens por solicitação
- [12:30] — Backpropagation: como os embeddings são otimizados durante o treinamento
- [16:10] — Softmax e mecanismo de atenção: próxima aula da série
- [17:45] — Conclusão: embeddings + janela de contexto são conceitos centrais de uso de LLMs

## Citações

> "o ser humano é muito bom com palavras e o computador a máquina é muito bom com números então como é possível um computador entender as palavras" — [00:00]

> "a palavra é embeds e você precisa entender o embeds como é que ele funciona ele é bem importante porque ele é exatamente a forma como transformar da palavra para que as nossas llms da vida aí possam nos entender" — [01:52]

> "a quantidade de valores aleatórios aqui é que define o tamanho do embed veja que nesse caso aqui eu tenho um Bert que é uma rede neural tem 768 valores 768 valores assim define o tamanho do embed" — [04:36]

> "nada mais é que a quantidade de tokens processados por solicitação veja quando eu vou solicitar alguma coisa eu vou passar um texto esse texto é muito grande na verdade o que vai acontecer" — [09:40]

> "a gente vai usar muito embeds e usa muito o conceito de janela de contexto tá bom você viu como é tranquilo a sequência que a gente tá fazendo aqui sobre a rede Transformer" — [17:45]

## Meu comentário

*Escreva aqui sua reação, surpresas, discordâncias.*

## Ver também

- [[02 - Tokens e tokenização]] <!-- sugestão; validar -->
- [[03 - A janela de contexto]] <!-- sugestão; validar -->
- 💡 Lacuna: nenhuma nota cobre Embeddings especificamente — candidata a nota nova "Embeddings e representação vetorial". <!-- sugestão -->
