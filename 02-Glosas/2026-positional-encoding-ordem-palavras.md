---
title: "É Genial! Como a IA Sabe a Ordem das Palavras?"
aliases: ["É Genial! Como a IA Sabe a Ordem das Palavras?"]
source: https://youtube.com/watch?v=uynsyoxIJq0
author: Sandeco Channel - Decomplicated IA
site: YouTube
channel: Sandeco Channel - Decomplicated IA
video_id: uynsyoxIJq0
duration: "00:14:34"
published: 2025-04-29
read: 2026-06-18
type: glosa
progress: backlog
status: lido
tags: [positional-encoding, transformers, llm, embeddings, nlp]
lang: pt
publish: false
---

# É Genial! Como a IA Sabe a Ordem das Palavras? — Sandeco Channel - Decomplicated IA

> [!info] Vídeo
> [▶ Assistir no YouTube](https://youtube.com/watch?v=uynsyoxIJq0) · 14:34 · Sandeco Channel - Decomplicated IA

## TL;DR

O Transformer substituiu a LSTM porque permite processamento paralelo em GPUs, mas perdeu a noção natural de sequência. O positional encoding resolve isso injetando a posição de cada token via funções seno e cosseno — criando um padrão oscilatório similar a um metrônomo onde posições iniciais variam muito e posições finais variam pouco. O embedding final do Transformer é a soma matricial do embedding de token com o embedding de posição.

## Pontos-chave

- O Transformer substituiu a LSTM porque a LSTM era sequencial por natureza, impedindo uso pleno de GPUs; Transformers processam todos os tokens em paralelo — mas precisam de uma forma matemática de codificar onde cada token está na sequência.
- O positional encoding usa seno e cosseno calculados a partir de ângulos derivados da posição (`pos`) e do índice de dimensão (`i`): `PE(pos, 2i) = sin(pos / 10000^(2i/d_model))` — a constante 10.000 (decay) controla a frequência de oscilação.
- O comportamento é semelhante a um metrônomo: os primeiros valores do embedding de posição oscilam com amplitude alta (variam muito entre posições consecutivas) enquanto os últimos variam quase nada — criando uma "impressão digital" única para cada posição.
- O `d_model` (tamanho do embedding) deve ser par porque o positional encoding ocupa pares de dimensões: cada par (2i, 2i+1) recebe respectivamente sin e cos do mesmo ângulo.
- O embedding final do Transformer = embedding de token + embedding de posição (soma elemento a elemento, mesma dimensão `d_model`).
- Essa soma permite que as GPUs processem os tokens em qualquer ordem durante o treinamento sem perder a informação sequencial — a posição está codificada nos próprios números.
- O mecanismo de atenção (próxima aula) recebe esses embeddings combinados e faz com que o contexto determine a atenção dada a cada posição.

## Momentos-chave

- [00:00] — Introdução: o que tem a ver um metrônomo com Transformer?
- [00:27] — O problema da sequência: por que simplesmente numerar posições não funciona
- [01:14] — Exemplo com dias da semana: dados ciclotímicos precisam de codificação circular
- [03:13] — Seno e cosseno de cada posição: a solução matemática
- [04:30] — A LSTM vs Transformer: sequencial vs. paralelo em GPU
- [05:20] — Por que positional encoding existe: permitir paralelismo sem perder sequência
- [06:10] — Fórmula do positional encoding: variáveis pos, i, d_model e decay (10.000)
- [09:00] — O comportamento metrônomo: variação alta no início, mínima no fim
- [11:30] — Plotagem visual: a impressão digital de cada posição
- [12:45] — Soma matricial: embedding final = token + posição
- [13:50] — Conclusão: embeddings do Transformer prontos para entrar no mecanismo de atenção

## Citações

> "Hoje você vai descobrir qual é a relação entre as redes do GPT, Cloud, Gemini, Dipsic, Quen com o metrônomo. O que tem a ver um metrônomo com as redes neurais Transformer?" — [00:05]

> "As redes Transformers, elas vieram para substituir uma rede chamada LSTM, que era muito boa com sequências de palavras, mas o problema dela é que ela era totalmente sequencial. Não era possível a gente usar a GPU em sua plenitude" — [04:30]

> "para que eu saiba aonde está cada texto, né, efetivamente dentro de um contexto para que a GPUs possam processar, eu preciso saber em que sequência cada texto está. Por isso que eu preciso do position encoding" — [05:20]

> "Você vê as ondas de informação acontecendo. Isso aqui é super importante você entender, porque é dessa forma que o transformer vai enxergar as palavras." — [03:13]

## Meu comentário

*Escreva aqui sua reação, surpresas, discordâncias.*

## Ver também

- [[04 - Atenção e o mecanismo transformer]] <!-- sugestão; validar -->
- [[02 - Tokens e tokenização]] <!-- sugestão; validar -->
