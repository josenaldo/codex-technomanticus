---
title: "O Segredo por Trás do GPT, Finalmente Revelado"
aliases: ["O Segredo por Trás do GPT, Finalmente Revelado"]
source: https://youtube.com/watch?v=15WwfSEGvo8
author: Sandeco Channel - Decomplicated IA
site: YouTube
channel: Sandeco Channel - Decomplicated IA
video_id: 15WwfSEGvo8
duration: "00:10:02"
published: 2025-01-20
read: 2026-06-18
type: glosa
progress: backlog
status: lido
tags: [llm, transformers, completacao, nlp, arquitetura]
lang: pt
publish: false
---

# O Segredo por Trás do GPT, Finalmente Revelado — Sandeco Channel - Decomplicated IA

> [!info] Vídeo
> [▶ Assistir no YouTube](https://youtube.com/watch?v=15WwfSEGvo8) · 10:02 · Sandeco Channel - Decomplicated IA

## TL;DR

Esta é a aula 1 de uma série de 8 sobre redes Transformer. O vídeo explica que a tarefa fundamental do GPT e de outros LLMs é a completação: dado um texto de entrada convertido em tokens, o modelo prevê iterativamente o próximo token mais provável, montando a resposta peça a peça. Toda persona, todo comportamento de "médico" ou "advogado" do ChatGPT é apenas uma especialização sobre essa única tarefa de completação.

## Pontos-chave

- A tarefa do Transformer não é "responder" — é completar texto: dado um conjunto de tokens de entrada, o modelo prevê qual é o próximo token mais provável e repete esse processo até encerrar a resposta.
- A completação é matematicamente uma classificação multi-classe: o vocabulário de uma língua pode ter 200.000–250.000 tokens; em cada passo, o modelo produz uma distribuição de probabilidade sobre todos eles e escolhe o mais provável.
- Os tokens não são palavras inteiras — a palavra "capital" é quebrada em sub-palavras pelo algoritmo BPE; os espaços entre palavras também são tokens separados (mas omitidos na visualização por economia de tela).
- O Transformer funciona de forma auto-regressiva: o token gerado é concatenado ao input original e o conjunto resultante vira o novo input para prever o próximo token — o modelo "lê o que acabou de escrever".
- Mesmo uma frase simples como "A capital do Brasil é ___" pode gerar tokens ambíguos: "Brasil" e "Brasília" compartilham sub-tokens (o token "ia" pode se combinar com "Brasil" para formar "Brasília"), demonstrando como a tokenização captura estrutura morfológica.
- O objetivo da série (8 aulas) é cobrir toda a arquitetura Transformer do zero: completação → tokens → embeddings → positional encoding → mecanismo de atenção → multi-head attention → transformer completo → vision transformer.
- Toda a conversa com o ChatGPT — independente da persona definida no prompt — é executada como uma sequência de completações sobre tokens.

## Momentos-chave

- [00:00] — Abertura: apresentação da série de 8 aulas sobre Transformer
- [00:53] — Mapa das oito aulas: completação, tokens, embeddings, positional encoding, atenção, multi-head, transformer completo, vision
- [01:01] — Aula de hoje: completação como tarefa central do Transformer
- [01:44] — Exemplo ao vivo: "A capital do Brasil é ___"
- [02:30] — Por que completação é classificação multi-classe (vocabulário de 200–250k tokens)
- [04:10] — Auto-regressividade: o token gerado vira parte do novo input
- [07:00] — Tokens ambíguos: "Brasil" vs "Brasília" compartilham sub-tokens BPE
- [09:15] — Conclusão: persona no prompt não muda a tarefa — é sempre completação

## Citações

> "a tarefa do transformer é exatamente fazer a completação tá essa palavra vem de completion né do inglês" — [01:44]

> "então você percebe que aí facilmente um vocabulário de uma língua pode atingir 200.000 250.000 tokens" — [02:30]

> "o Transformer vai adicionar ao input esse token tá que será um novo input tá é como se ele fosse ele produzisse alguma coisa que ele mesmo entende" — [04:10]

> "tem muita gente que fala assim o GPT ele é muito bom na tarefa de ser o médico na tarefa de ser advogado na verdade você está definindo uma Persona para o GPT beleza no prompt né Entretanto a tarefa que tem o GPT é a tarefa de completação" — [09:15]

## Meu comentário

*Escreva aqui sua reação, surpresas, discordâncias.*

## Ver também

- [[01 - O que é um LLM]] <!-- sugestão; validar -->
- [[02 - Tokens e tokenização]] <!-- sugestão; validar -->
