---
title: "The death of the stubborn developer"
aliases: ["The death of the stubborn developer"]
source: https://sourcegraph.com/blog/the-death-of-the-stubborn-developer
author: Steve Yegge
site: Sourcegraph
published:
read: 2026-05-26
type: glosa
status: lido
tags: [chop, chat-oriented-programming, ai-coding-assistant, autonomous-agents, optionality]
lang: en
publish: false
---

# The death of the stubborn developer — Steve Yegge

## TL;DR

Yegge atualiza o argumento de "The Death of the Junior Developer": não é só júnior que vai ficar pra trás, é qualquer dev que recusar adotar Chat-Oriented Programming (CHOP) como modalidade primária. Estudos internos de clientes da Sourcegraph mostram boost mínimo de 30% em produtividade no enterprise, agentes autônomos generalistas continuam miragem, e quem persistir programando à mão vai virar o "assembly-holdout dos anos 90".

## Pontos-chave

- O termo "júnior" foi mal calibrado: há sêniores que adotam chop e disparam, e juniores que adotam e upleveling sozinhos; o recorte certo é "stubborn" — quem se recusa a fazer do chat a modalidade primária.
- Tomando emprestada uma analogia de Matt Beane (juniores cirurgiões vs. robôs cirúrgicos), Yegge mostra que o circuito que transforma júnior em sênior está quebrado: LLM executa os leaf nodes do task graph que antes serviam de aprendizado.
- Estudos internos com clientes Sourcegraph indicam boost mínimo de 30% em produtividade enterprise com chop — mesmo quando os engenheiros reclamam achando que estão mais lentos. Em casos específicos chega a 10x-20x.
- Crítica direta aos investidores apostando em agentes autônomos generalistas (Devin como caso emblemático de fanfarra sem follow-through): tecnologia transformadora cresce incrementalmente, e nada de agente geral está aparecendo em iterações públicas.
- Posição da Sourcegraph: o wrangler do task graph acima dos leaf nodes é humano, não modelo; o coding assistant serve pra acelerar input (context fetching, prompt reuse) e output (smart-apply).
- Idan Gazit (GitHub Next) tem visão alternativa respeitada por Yegge: chop é "para virtuoses" (digita rápido, lê rápido, sling de contexto manual); seria preciso uma modalidade acessível a programadores comuns — mas Yegge não banca essa promessa no curto prazo.
- Conceito novo: **Optionality**. Chop não acelera tanto o que você já sabe; acelera dramaticamente o que você nunca tentou, permitindo explorar múltiplas linguagens, backends e abordagens em paralelo a cada decisão crítica.

## Citações

> "You are getting left behind if you do not adopt chat-based programming as your primary modality."

> "The broad conclusion is that switching to chop gives enterprise engineers a minimum boost of 30% in productivity across the board — even when the engineers are grumbling and think they are slower with it."

> "I think those people are smoking some serious crack. But many are well-funded, so they're going to get a chance to give it the old college try, burning investor money like jet fuel along the way."

> "Chop may not necessarily make you a lot faster at stuff you already know how to do well. But it makes you extraordinarily faster at things you're not very good at — things that you've been putting off because you know it's going to be more work than it's worth."

> "You're like one of those crusty old assembly-language holdouts still using asm in 1990 because compiler-generated code wasn't fast enough. Stubborn bastards, the lot of 'em. Sound familiar?"

## Meu comentário

*Escreva aqui sua reação, surpresas, discordâncias.*

## Ver também

-
