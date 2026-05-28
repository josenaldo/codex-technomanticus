---
title: "Workflow vs Agent Layer"
created: 2026-05-28
updated: 2026-05-28
type: concept
status: seedling
progress: in_progress
tags:
  - ai-engineering-stack
  - ia
  - arquitetura
  - agents
publish: true
aliases:
  - Workflow vs Agent
  - Camada de arquitetura
---

# Workflow vs Agent Layer

> [!abstract] TL;DR
> A pergunta mais consequente do stack: **caminho fixo (workflow) ou descoberto dinamicamente (agent)?** Workflow quando o passo-a-passo é conhecido — você orquestra LLMs em nós de um pipeline. Agent quando o caminho precisa ser decidido em tempo de execução — o LLM escolhe a próxima ação em loop até decidir parar. A regra cardinal: **não construa agent por padrão**. Agent custa mais, falha mais, debuga pior. Use quando workflow não consegue resolver — e essa fronteira é mais alta do que parece.

## O que é esta camada

Esta camada não produz template — produz **decisão arquitetural**. A escolha entre workflow e agent determina o resto do stack: tools necessárias, estilo de eval, tipo de logging, custo, latência.

A formalização da Anthropic em *Building effective agents* (2024) ajuda a clarear o vocabulário:

- **Building blocks** — LLM com retrieval, tools, memory. O átomo.
- **Workflows** — building blocks orquestrados em **caminho predefinido** por código.
- **Agents** — LLM em loop decidindo a próxima ação até concluir.

Workflow não é "agent inferior" — é uma escolha arquitetural diferente, geralmente melhor.

## Decisões-chave

1. **Caminho é previsível?** Se você consegue desenhar o flowchart inteiro, é workflow. Se nós e arestas dependem do input de cada etapa, é agent.

2. **Custo do erro vs custo da rigidez.** Agent erra mais (loop pode divergir) mas é flexível. Workflow erra menos mas falha em casos não previstos. Onde o custo do erro é alto (financeiro, irreversível), prefira workflow.

3. **Profundidade do loop.** Agent que precisa de 2-3 chamadas chega lá. Agent que precisa de 30 chamadas pra resolver um problema, normalmente está mascarando um workflow mal modelado.

4. **Debugabilidade.** Workflow é debugável passo a passo. Agent exige tracing pesado ([[Dicionário de IA#tracing|tracing]]) pra entender por que escolheu cada ação. Sem [[11 - Logging Layer]] forte, agent é caixa-preta.

5. **Padrões intermediários.** Entre puro workflow e puro agent existem padrões: **prompt chaining**, **routing**, **parallelization**, **orchestrator-workers**, **evaluator-optimizer**. A maioria dos sistemas de produção é um desses, não agent puro.

## Onde aprofundar no Codex

- **[[Anatomia de Agents/10 - Workflow vs Agent|10 - Workflow vs Agent]]** — discussão profunda (a ser publicada).
- **[[Anatomia de Agents/08 - Patterns comuns de agents|Patterns comuns de agents]]** — orchestrator-worker, planning, ReAct.
- **[[Spec-Driven Development]]** — workflows formalizados como spec executável.

## Veja também

- [[02 - Purpose Layer — o que o sistema é]] — Purpose Layer informa se a tarefa precisa de agent
- [[07 - Tool Layer]] — agents dependem de tools; workflows podem funcionar sem
- [[09 - Evaluation Layer]] — eval de agent é fundamentalmente mais difícil que eval de workflow

## Fontes

- **@hooeem** — *Become an AI Engineer*, chapter #18, Step 7 (Workflow vs Agent).
- **Anthropic** — [*Building effective agents*](https://www.anthropic.com/engineering/building-effective-agents) (2024). Definição de building blocks → workflows → agents.
- **Lilian Weng** — [*LLM-powered Autonomous Agents*](https://lilianweng.github.io/posts/2023-06-23-agent/) (2023).
