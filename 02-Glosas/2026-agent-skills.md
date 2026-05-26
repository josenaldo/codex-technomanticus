---
title: "Agent Skills"
aliases: ["Agent Skills"]
source: https://addyosmani.com/blog/agent-skills/
author: Addy Osmani
site: AddyOsmani.com
published: 2026-05-03
read: 2026-05-26
type: glosa
status: lido
tags: [agent-skills, ai-coding-agents, sdlc, software-engineering, anti-rationalization]
lang: en
publish: false
---

# Agent Skills — Addy Osmani

## TL;DR

Addy Osmani apresenta seu projeto open source Agent Skills (27k stars) como tentativa de "remontar o scaffolding de engenheiro sênior" sobre agentes de IA. A tese: agentes pulam por padrão o trabalho que não aparece no diff (specs, testes, reviews, disciplina de escopo); skills são markdown com frontmatter que injetam workflows com critério de saída concreto, tabelas anti-racionalização pré-escritas e disclosure progressivo, ancorados em práticas do Software Engineering at Google.

## Pontos-chave

- O comportamento padrão de qualquer agente de IA é tomar o caminho mais curto até "feito": escreve o código, declara vitória, pula spec/teste/review/escopo — exatamente o trabalho que sêniores aprendem a forçar a si mesmos.
- Uma "skill" não é documentação de referência — é workflow: sequência de passos com checkpoints que produzem evidência e critério de saída definido. "Process over prose" é a regra que separa skill útil de markdown bonito.
- O repo organiza ~20 skills em 6 fases SDLC (Define, Plan, Build, Verify, Review, Ship) + `/code-simplify`, com 7 slash commands no topo. Uma feature complexa pode ativar 11 skills em sequência; um bugfix pequeno pode usar 3.
- Cinco princípios de design são load-bearing: (1) process over prose, (2) anti-rationalization tables, (3) verification não-negociável, (4) progressive disclosure, (5) scope discipline.
- Anti-rationalization tables (rebuttals pré-escritos pra desculpas comuns) é a inovação mais distinta: LLMs são excelentes em racionalizar, então você pré-escreve a réplica antes da desculpa ser fabricada — funciona pra times humanos pelo mesmo motivo.
- Skills carregam DNA do *Software Engineering at Google*: Hyrum's Law, test pyramid + Beyoncé Rule, DAMP over DRY em testes, PRs de ~100 linhas com labels Critical/Nit/Optional/FYI, Chesterton's Fence, trunk-based development, code-as-liability — práticas que o modelo "leu" no treino mas não aplica às 3h da manhã.
- Os cinco não-negociáveis do meta-skill servem também pra times humanos: surface assumptions, pare quando requirements conflitam, push back quando justificado, prefira solução boring/óbvia, toque só no que foi pedido.

## Citações

> "The default behaviour of any AI coding agent is to take the shortest path to 'done.'"

> "Process over prose. Workflows over reference. Steps with exit criteria over essays without them."

> "Anti-rationalization tables are pre-written rebuttals to lies the agent hasn't yet told."

> "Scope discipline is the single biggest determinant of whether an agent's PR is mergeable or has to be unwound."

> "The senior-engineer parts of the job are no longer optional, even when the engineer is a model."

## Meu comentário

*Escreva aqui sua reação, surpresas, discordâncias.*

## Ver também

-
