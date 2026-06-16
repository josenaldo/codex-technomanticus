---
title: "Intent Debt: The AI-Era Debt Nobody Is Tracking"
aliases: ["Intent Debt: The AI-Era Debt Nobody Is Tracking"]
source: https://www.developersdigest.tech/blog/intent-debt-the-ai-debt-nobody-is-tracking
author: Developers Digest
site: Developers Digest
published: 2026-04-22
read: 2026-06-16
type: glosa
status: lido
tags: [divida-intencao, triple-debt-model, agentes-ia, documentacao, adr]
lang: en
publish: false
---

# Intent Debt: The AI-Era Debt Nobody Is Tracking — Developers Digest

## TL;DR

Releitura prática do Triple Debt Model com foco operacional na **dívida de intenção**: ela se acumula quando as metas e restrições que deveriam guiar o sistema são mal capturadas ou desatualizadas em artefatos (CLAUDE.md, ADRs, design docs, README, critérios de aceitação). Na era dos agentes ela deixa de ser custo suave (onboarding lento) e vira **custo direto de throughput a cada execução de agente**, porque o agente lê artefatos — não mentes. O artigo oferece testes de diagnóstico e práticas de pagamento.

## Pontos-chave

- **Dívida de intenção vive nos artefatos**: limita se o sistema continua refletindo o que se pretendia construir, e afeta diretamente o quão bem agentes conseguem evoluí-lo. Seus artefatos de intenção são CLAUDE.md, ADRs, design docs, critérios de aceitação, README.
- Agentes **não leem mentes nem inferem restrições não-escritas** — leem artefatos documentados; se o artefato diverge da intenção real, o agente implementa a coisa errada documentada.
- Testes de diagnóstico: **teste dos 5 minutos** (consegue articular pra que serve, pra que NÃO serve, e as 3 restrições mais duras?), teste do CLAUDE.md vivo vs. abandonado, teste dos não-objetivos no README, teste de ADR nos commits materiais, teste da linguagem ubíqua (3 colegas definem os termos igual?).
- Pagamento: escrever CLAUDE.md antes da primeira execução de agente; escrever ADRs de forma barata e agressiva; seção de **não-objetivos** em todo README; atualizar artefatos de intenção **no mesmo PR** que muda o significado do sistema; tornar a intenção **executável** via testes, tipos e regras de lint no CI.
- **Argumento de segunda ordem:** se agentes barateiam escrever código, *verificar* fica caro — a composição do time muda de "10 engenheiros de feature" para "3 engenheiros + 7 pessoas definindo critérios de aceitação, harness de testes e monitoramento". A atividade cara migra de *construir* para *julgar o que é "correto"*.

## Citações

> "Intent debt accumulates when the goals and constraints that should guide the system are poorly captured or maintained."

> "AI agents cannot read minds or infer unwritten constraints. They read documented artifacts. If artifacts don't match actual intent, agents implement the documented wrong thing."

> "If coding agents make writing code cheap, verification becomes expensive."

> "The expensive activity shifts from building to judging what correct means."

## Meu comentário

*Escreva aqui sua reação, surpresas, discordâncias.*

## Ver também

-
