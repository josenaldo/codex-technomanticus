---
title: "Part 1 · The Black Box (An Engineer's Guide to Harness Orchestration)"
aliases: ["Part 1 · The Black Box", "An Engineer's Guide to Harness Orchestration"]
source: https://agentfield.ai/blog/harness-as-black-box
author: Santosh Kumar Radha
site: AgentField
published: 2026-04-29
read: 2026-05-26
type: glosa
status: lido
tags: [harness, agent-orchestration, ai-agents, variance-absorption, membrane-engineering]
lang: en
publish: false
---

# Part 1 · The Black Box — Santosh Kumar Radha

## TL;DR

Santosh Kumar Radha (AgentField) argumenta que o "harness" (Claude Code, Codex, Gemini CLI, OpenCode) é um objeto computacional fundamentalmente novo, definido pela combinação simultânea de três propriedades — agência, embodiment e persistência — que nenhuma primitiva anterior teve junta. Daí decorre que orquestrar harnesses é projetar contratos e membranas seletivamente permeáveis, mais perto de "gerenciar funcionários" do que de "escrever workflows".

## Pontos-chave

- Há duas formas de usar inteligência num sistema: chamada constrita (one-shot, input/output estruturados, sem ferramentas) e loop autônomo (objetivo entra, ambiente acessado, resultado verificado sai). A maioria das decisões de orquestração reduz a escolher qual forma cada passo quer.
- O harness se distingue por três propriedades ortogonais: agency (decide quando agir), embodiment (escreve arquivos, roda comandos, hits APIs), persistência (filesystem, memória e identidade persistem). Função tem zero das três; microserviço tem embodiment + persistência sem agency; loop de agente tem agency sem embodiment durável.
- A propriedade mais útil do harness é **variance absorption**: o mesmo call shape lida com uma distribuição de tarefas relacionadas, condicionado em runtime pelo prompt e pelo workspace. Não é necessário um pipeline diferente por classe de tarefa.
- Variance absorption tem dois eixos: modelo (frontier absorve mais) e design do harness (prompt apertado, tools curadas, workspace focado). Os autores reportam ter marcado 95/100 com Claude Haiku e com modelo open source barato usando a mesma arquitetura — design pesa tanto quanto modelo.
- Empiricamente, 40 invocações da mesma task no mesmo modelo produziram 25 diffs distintos (uma solução recorreu 9x, 19 apareceram apenas 1x). Trajetórias divergem; outcomes convergem sob verificação. O modelo tem **attractor states** — soluções preferidas pelo prior do treino.
- "Black box" é pedagogicamente enganoso: o harness tem uma **membrana seletivamente permeável**. Objetivo, configuração de boundary e outcome estruturado atravessam livremente; deliberação interna nunca atravessa; rationales e estado parcial precisam de trabalho ativo via journal.
- Quando se orquestra harness, mudam três coisas: (1) controle de processo dá lugar a verificação de outcome; (2) prompt engineering dá lugar a membrane engineering (tools, working dir, budget, success criteria); (3) o orquestrador vira supervisor — define condições, não passos.

## Citações

> "The atomic unit of intelligence has climbed. A token. A model call. An agent loop. A harness."

> "Only the harness has all three together, and it is the simultaneous presence of all three that produces every architectural concern in this series."

> "Trajectories diverge while outcomes converge under verification."

> "Harness orchestration is the design of contracts, boundaries, and verifications between intelligences you cannot see inside."

> "The orchestrator becomes a supervisor. It no longer specifies the work; it specifies the conditions under which the work is done and the conditions under which it is accepted."

## Meu comentário

*Escreva aqui sua reação, surpresas, discordâncias.*

## Ver também

-
