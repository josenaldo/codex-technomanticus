---
title: "The Hidden Primitive Behind Claude Code, Codex, and Gemini"
aliases: ["The Hidden Primitive Behind Claude Code, Codex, and Gemini", "Harness as Membrane"]
source: https://agentfield.ai/blog/harness-as-membrane
author: Santosh Kumar Radha
site: AgentField
published: 2026-05-05
read: 2026-05-26
type: glosa
status: lido
tags: [harness-orchestration, coding-agents, agent-membrane, verifiers, blast-radius]
lang: en
publish: false
---

# The Hidden Primitive Behind Claude Code, Codex, and Gemini — Santosh Kumar Radha

## TL;DR

Parte 2 da série sobre *harness orchestration*. Radha define a **membrana** como a superfície de fronteira de um único harness — o que ele realmente lê, usa, verifica e altera em runtime, não os parâmetros do call site. Decompõe-a em quatro propriedades que o engenheiro controla diretamente: o **workspace** (o maior prompt que o harness vê), o **drift** dessa fronteira durante a execução, a **visibilidade dos verificadores** (que decide se são forcing function ou contrato), e o **blast radius**, que precisa caber no orçamento de recuperação do time.

## Pontos-chave

- **Membrana ≠ parâmetros.** Os parâmetros do harness (`provider`, `model`, `max_turns`, `max_budget_usd`, `tools`) são a "configuração de envio"; a membrana é o que eles *produzem* em runtime — os arquivos que o agente lê, as ferramentas que usa, os verificadores que consulta, os efeitos colaterais que deixa. Engenheirar a membrana é engenheirar cada um desses.
- **O workspace é o maior prompt.** Antes de escrever, o harness lê (README, commits recentes, testes, manifesto de dependências). System+user prompt = 2.000–4.000 tokens; o workspace, depois de orientado, chega a 30.000–60.000 tokens — e o orquestrador não colocou nada ali explicitamente. Workspace sujo (`CLAUDE.md` velho, regras conflitantes, 40 MB de build artifacts) gera trajetória ruim que postmortems erradamente culpam no modelo. Curar o workspace (brief curto que supera os docs longos, `prune`, scrub de secrets, whitelist de tools) é a alavanca mais subvalorizada.
- **A membrana faz drift.** A fronteira no t=0 e no minuto 30 são objetos diferentes, e o gap cresce monotonicamente. Quatro fontes: (a) *script-write-then-execute* — o agente escreve e roda um script, expandindo os binários disponíveis no meio do run; (b) *context compaction* — lossy por design, transforma constraints do prompt original em paráfrase ou nada; (c) *discovered capability* — o agente lê um arquivo que revela deploy script/API key já presentes no workspace; (d) *expanding network reach* — cada chamada de rede ensina sobre serviços alcançáveis. Mitigações: worktree descartável por invocação, registro de tools congelado em t=0, re-injeção do brief a cada compaction, controle de egress no nível do SO.
- **Sob drift, os parâmetros deixam de ser independentes.** `max_turns` interage com `max_budget_usd` (frequência de retry), que interage com `tools` (quais retries são possíveis), que interage com `permission_mode` (se retries que tocam arquivos novos exigem aprovação humana). Ajustar um isolado costuma quebrar outro.
- **Verificadores visíveis ao agente NÃO são contratos.** Um verificador que o harness vê é uma *forcing function* na trajetória; um que ele não vê é um *contrato* sobre o resultado. Quando o mesmo artefato (ex.: `pytest`) serve aos dois papéis, o agente otimiza para o verificador de formas que o contrato não-dito não previu (lei de Goodhart) — ex.: passou no pytest adicionando um mock que stuba a dependência que falhava; o CI aceitou; o ambiente de integração pegou na manhã seguinte. Dado da Parte 1: em 40 trials do mesmo task, 25 diffs distintos, todos passando no pytest.
- **A correção estrutural é composição.** Um harness escreve; um segundo verifica — sem contexto compartilhado, sem tools de escrita, com cwd e provider diferentes (atrator diferente). O verificador lê o artefato como *dado*, não como continuação do run do writer. É uma propriedade de duas membranas interagindo, não instalável como parâmetro de uma só.
- **Blast radius ≤ recovery budget.** Toda capacidade tem um custo de desfazer no pior caso; todo contexto tem um orçamento de recuperação. A única afirmação falsificável do texto: um harness que pode fazer X deve rodar onde o custo de desfazer X é pagável pelo time. Tabela de capacidades por `undo_cost` (`read_only`=zero … `prod_send`=infinito). A maioria das falhas de produção mora nas linhas de baixo, concedidas por acidente; dimensionar a membrana pela *média* em vez da *cauda* é o erro mais comum.

## Citações

> "The workspace is the largest prompt the harness ever sees, and the orchestrator put none of it there explicitly."

> "The membrane at the moment of invocation and the membrane at minute 30 are different objects, and the gap between them widens monotonically with the run."

> "When the same artifact serves both roles, the agent has every incentive to optimize for the verifier in ways that the unstated contract did not anticipate."

> "A harness that can do X must run in a context where the cost of undoing X is something the team can pay, in the time the team has, with the tools the team has on hand."

> "Sizing the membrane to the average rather than the tail is the most common failure mode in practice."

## Meu comentário

*Escreva aqui sua reação, surpresas, discordâncias.*

## Ver também

-
