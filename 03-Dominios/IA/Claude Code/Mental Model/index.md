---
title: "Mental Model — Claude Code"
type: moc
publish: true
created: 2026-05-13
updated: 2026-05-13
status: seedling
tags:
  - claude-code
  - mental-model
  - moc
aliases:
  - Galho 1 - Mental Model
  - Claude Code Mental Model
---

# Mental Model — Claude Code

> [!abstract] TL;DR
> Galho 1 da trilha Claude Code. Cobre como o agente realmente funciona internamente: loop agentic, leitura de codebase, tool use, context window, modos de operação, compaction, custo e tomada de decisão. Pré-requisito recomendado para todos os outros galhos.

## Sobre este galho

Entender o mental model do Claude Code muda como você usa a ferramenta. Saber que o agente não indexa o codebase como uma IDE, mas navega com grep/glob/find, explica por que um CLAUDE.md bem escrito importa tanto. Saber como a context window se comporta explica por que sessões longas ficam mais lentas e custosas.

Este galho constrói o mapa mental que torna os outros galhos legíveis.

## Notas

1. [[03-Dominios/IA/Claude Code/Mental Model/01 - O loop agentic|01 - O loop agentic — plan, act, observe, iterate]]
2. [[03-Dominios/IA/Claude Code/Mental Model/02 - Como Claude Code lê um codebase|02 - Como Claude Code lê um codebase]]
3. [[03-Dominios/IA/Claude Code/Mental Model/03 - Tool use|03 - Tool use — como o agente usa ferramentas]]
4. [[03-Dominios/IA/Claude Code/Mental Model/04 - Context window|04 - Context window — o que entra, o que sai]]
5. [[03-Dominios/IA/Claude Code/Mental Model/05 - Modos de operação|05 - Modos de operação — interativo, plan, auto, headless]]
6. [[03-Dominios/IA/Claude Code/Mental Model/06 - Compaction|06 - Compaction — gerenciando contextos longos]]
7. [[03-Dominios/IA/Claude Code/Mental Model/07 - Tokens e custo|07 - Tokens e custo — como sessões consomem recursos]]
8. [[03-Dominios/IA/Claude Code/Mental Model/08 - Como o agente decide|08 - Como o agente decide — confiança, raciocínio, iteração]]

## Veja também

- [[03-Dominios/IA/Claude Code/index|Claude Code]] — tronco da trilha
- [[03-Dominios/IA/Claude Code/Configuração/index|Configuração]] — próximo galho recomendado
