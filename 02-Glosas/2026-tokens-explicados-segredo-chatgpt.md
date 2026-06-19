---
title: "Tokens Explicados: O Segredo Por Trás do ChatGPT"
aliases: ["Tokens Explicados: O Segredo Por Trás do ChatGPT"]
source: https://youtube.com/watch?v=Am73u_4y0ok
author: Sandeco Channel - Decomplicated IA
site: YouTube
channel: Sandeco Channel - Decomplicated IA
video_id: Am73u_4y0ok
duration: "00:19:49"
published: 2025-02-03
read: 2026-06-18
type: glosa
progress: backlog
status: lido
tags: [tokenizacao, llm, nlp, bpe, transformers]
lang: pt
publish: false
---

# Tokens Explicados: O Segredo Por Trás do ChatGPT — Sandeco Channel - Decomplicated IA

> [!info] Vídeo
> [▶ Assistir no YouTube](https://youtube.com/watch?v=Am73u_4y0ok) · 19:49 · Sandeco Channel - Decomplicated IA

## TL;DR

Tokenização é o processo pelo qual LLMs como o GPT convertem texto em unidades numéricas chamadas tokens, usando o algoritmo Byte Pair Encoding (BPE). O BPE quebra o texto em caracteres e iterativamente agrupa os pares mais frequentes, descobrindo raízes de palavras que permitem ao modelo generalizar — inclusive para textos com erros de grafia.

## Pontos-chave

- Tokens não são palavras: o BPE quebra o texto em caracteres individuais primeiro, e só depois forma sub-palavras ao agrupar pares frequentes — um mesmo token pode corresponder a uma raiz como "feliz" presente em "infeliz", "felicidade" e "infelizmente".
- A ponte entre texto humano e números computacionais passa obrigatoriamente pela tokenização: mapear palavras diretamente a inteiros inteiros causa problemas de normalização (números grandes dominam redes neurais); One-Hot Encoding perde contexto semântico; embeddings, a solução real, dependem de tokens como fundação.
- O algoritmo BPE tem três passos centrais: (1) converter tudo em minúsculas, (2) separar todos os caracteres, (3) repetir N vezes a fusão do par de caracteres/tokens mais frequente — o hiperparâmetro N define o tamanho do vocabulário resultante.
- O valor de N é um hiperparâmetro crítico: muito grande converge para palavras inteiras (perde generalização); muito pequeno mantém apenas caracteres (tokens sem significado). Estratégias práticas incluem basear N no tamanho do corpus, em limiar de frequência mínima, ou ajustar iterativamente pela performance de validação.
- Tokens permitem que o modelo lide com erros de ortografia: "felizmente" grafado com "i" ainda é tokenizado com a raiz "feliz", que atrai as palavras de contexto corretas e guia a completação para a forma correta.
- A tarefa de completação — o coração do GPT — opera inteiramente sobre tokens: tokens de entrada alimentam o modelo, que prevê o próximo token; a sequência de previsões produz a resposta.
- Tokens são a base dos embeddings, que serão o tema da aula seguinte da série: sem tokenização não há representação vetorial contextualizada do texto.

## Momentos-chave

- [00:00] — Introdução: por que uma pessoa leiga deve entender tokenização
- [00:44] — ChatGPT explica ao vivo a importância da tokenização
- [01:21] — A tarefa de completação: tokens de entrada → previsão de próximos tokens
- [02:11] — Token vs. palavra: esclarecimento da confusão mais comum
- [02:47] — O desafio de ligar texto (humano) a números (computador)
- [04:53] — Falha do One-Hot Encoding: palavras distantes no espaço vetorial
- [06:44] — Apresentação do BPE (Byte Pair Encoding) como algoritmo do GPT
- [07:24] — Passo 1 do BPE: converter tudo em minúsculas
- [09:14] — Passo 3 do BPE: contar e fundir os pares mais frequentes
- [13:49] — Exemplo com "feliz/felicidade/infeliz": tokens como raízes de palavras
- [17:04] — Hiperparâmetro N e as quatro estratégias para escolhê-lo
- [18:50] — Estratégia mais usada: ajuste iterativo por performance de validação

## Citações

> "tokenização é o processo de dividir um texto em pedaços menores chamados tokens que podem ser palavras partes de palavras ou até caracteres" — [00:53]

> "token a token é a metade de uma palavra é parte de uma palavra" — [02:11]

> "tokens não são palavras você não pode dizer porque antes do GPT processar qualquer coisa ele pega todas as palavras e quebra né separa seus caracteres" — [07:58]

> "feli ou feliz como sendo uma raiz de palavra isso é importante porque na hora da completação ele vai poder encontrar exatamente a parte da raiz da palavra que é importante na classificação" — [14:11]

> "a gente sabe que os tokens né são a base dos embeddings então na próxima aula no próximo vídeo nós vamos falar exatamente sobre isso" — [19:00]

## Meu comentário

*Escreva aqui sua reação, surpresas, discordâncias.*

## Ver também

- [[02 - Tokens e tokenização]] <!-- sugestão; validar -->
