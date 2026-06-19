---
title: "O Segredo das Múltiplas Mentes do ChatGPT e do Gemini"
aliases: ["O Segredo das Múltiplas Mentes do ChatGPT e do Gemini"]
source: https://youtube.com/watch?v=p-8UNsVD3AM
author: Sandeco Channel - Decomplicated IA
site: YouTube
channel: Sandeco Channel - Decomplicated IA
video_id: p-8UNsVD3AM
duration: "00:11:30"
published: 2025-09-20
read: 2026-06-18
type: glosa
progress: backlog
status: lido
tags: [multihead-attention, transformers, llm, arquitetura, nlp]
lang: pt
publish: false
---

# O Segredo das Múltiplas Mentes do ChatGPT e do Gemini — Sandeco Channel - Decomplicated IA

> [!info] Vídeo
> [▶ Assistir no YouTube](https://youtube.com/watch?v=p-8UNsVD3AM) · 11:30 · Sandeco Channel - Decomplicated IA

## TL;DR

O multi-head attention é a técnica que faz o ChatGPT e o Gemini "pensarem com múltiplas cabeças". Em vez de aplicar o mecanismo de atenção uma única vez, o Transformer projeta o embedding de cada token em múltiplos subespaços (cabeças) usando projeções lineares — análogas a lanternas iluminando um objeto 3D de ângulos diferentes. Cada projeção cria uma "sombra" (cabeça de atenção) que captura um aspecto diferente do contexto, separando assuntos que poderiam se misturar e reduzindo alucinações.

## Pontos-chave

- Multi-head attention é a aplicação paralela de múltiplos mecanismos de atenção sobre o mesmo embedding de entrada: cada "cabeça" usa uma projeção linear diferente (matriz de pesos), capturando aspectos distintos do contexto.
- A analogia das lanternas explica intuitivamente: iluminar um objeto 3D com uma lanterna gera uma sombra (projeção 2D); múltiplas lanternas de ângulos diferentes geram múltiplas sombras, cada uma revelando aspectos que as outras não veem.
- O Transformer original (artigo "Attention Is All You Need") usou 8 cabeças de atenção; modelos modernos podem ter dezenas ou centenas, com o limite prático sendo o custo computacional.
- Mais cabeças = assuntos mais bem separados no espaço vetorial = menor probabilidade de alucinação: quando os assuntos se misturam no espaço, o modelo pode combinar contextos indevidos na geração.
- Cada cabeça multiplica o embedding de entrada por uma matriz de projeção diferente, gerando um "sub-embedding" menor; ao final, as saídas de todas as cabeças são concatenadas e multiplicadas por outra matriz de projeção para retornar ao tamanho original.
- A separação de assuntos por projeções é como girar dois grupos de dados confusos: antes da projeção, estão misturados; depois, separam-se claramente — o modelo pode atrair cada palavra para o assunto correto.
- O mecanismo de atenção (aula anterior) já opera sobre embeddings combinados com positional encoding; o multi-head attention é a "versão amplificada" que paraleliza esse processo em múltiplos espaços.

## Momentos-chave

- [00:00] — Introdução: "o segredo das múltiplas mentes do ChatGPT e do Gemini"
- [01:00] — Retomada do problema: a palavra "ponto" em um texto com assuntos transporte e moda
- [02:00] — Analogia das lanternas: projeção 3D → sombra 2D = cabeça de atenção
- [04:00] — Três projeções (lanternas) = três cabeças de atenção para a mesma palavra
- [05:30] — Por que projetar? Para separar assuntos misturados no espaço vetorial
- [07:00] — Demonstração manual com as mãos: dados misturados vs. separados após projeção
- [08:30] — Transformer original: 8 cabeças; modelos modernos: dezenas
- [09:20] — Mais projeções = mais separação = menos alucinação
- [10:30] — Conclusão: "várias cabeças pensam melhor do que uma"

## Citações

> "Multiad attention é uma técnica que está dentro do transformer e faz com que o chatpt e o Gemini pensem melhor na hora que eles vão aplicar ou extrair alguma informação dentro deles." — [00:27]

> "quando eu acendo a luz, o que acontece é que eu tenho aqui embaixo, ó, uma sombra, tá vendo? Uma sombra. é a partir da projeção desse vetor neste plano. Nada demais também tudo muito simples" — [02:00]

> "Na verdade, o Transformer original trabalhou com oito projeções. Sandeco, oito projeções. Como assim? Porque no mundo 3D eu consigo ver as três projeções, mas oito projeções é uma coisa que eu não consigo ver, né? Entretanto, isso acontece matematicamente, sim." — [08:30]

> "quanto mais projeções eu tiver, mais separados os dados, os assuntos estarão uns dos outros. E aí quando você escrever para solicitar, né, pro chatt e pro Gemini gerar algum tipo de assunto, eh, se os assuntos estão bem separados, eles não vão se misturar. Ou seja, nem o chatpt, nem o Gemini vão alucinar." — [09:20]

## Meu comentário

*Escreva aqui sua reação, surpresas, discordâncias.*

## Ver também

- [[04 - Atenção e o mecanismo transformer]] <!-- sugestão; validar -->
