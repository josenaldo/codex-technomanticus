---
title: "The Intent Debt"
aliases: ["The Intent Debt"]
source: https://addyosmani.com/blog/intent-debt/
author: Addy Osmani
site: AddyOsmani.com
published: 2026-06-05
read: 2026-06-07
type: glosa
status: lido
tags: [intent-debt, divida-tecnica, agentes-ia, documentacao, engenharia-de-software]
lang: en
publish: false
---

# The Intent Debt — Addy Osmani

## TL;DR

Osmani apresenta o "intent debt" (dívida de intenção) como a terceira dívida do Triple Debt Model de Margaret-Anne Storey: a ausência de rationale, metas e restrições externalizadas que explicam por que o sistema é como é. Enquanto agentes de IA reduzem o custo da dívida técnica e cognitiva, eles não podem gerar intenção — ela vem exclusivamente de humanos — e, pior, fazem o custo da intenção não-escrita compor a cada sessão, já que cada agente começa sem memória do contexto acumulado.

## Pontos-chave

- O Triple Debt Model distingue três dívidas: **técnica** (vive no código: módulos emaranhados, atalhos de deadline), **cognitiva** (vive na cabeça: erosão do entendimento compartilhado) e **de intenção** (vive nos artefatos nunca escritos: metas, restrições e rationale do design).
- As três dívidas operam de forma independente — um time pode ter dívida técnica baixa e dívida de intenção altíssima ao mesmo tempo.
- Agentes de IA ajudam com dívida técnica (refatoram rápido) e cognitiva (explicam código sob demanda), mas **não podem gerar intenção**: quando inferem rationale do código existente, estão fabricando, não recuperando a intenção autêntica.
- Times tradicionais absorviam intenção via contexto compartilhado prolongado (conversas de corredor, code reviews, memória institucional); times agênticos quebram essa dinâmica porque cada sessão de agente começa fria — intenção não externalizada se torna inacessível.
- A economia mudou: intenção não-escrita antes custava só no onboarding ou quando alguém saía; agora o custo é pago **a cada sessão, por cada agente**.
- Sintomas de dívida de intenção alta: agentes "consertam" bugs removendo guard clauses cujo propósito nunca foi registrado; refactors quebram comportamentos que usuários dependiam porque os testes codificavam só o comportamento anterior, nunca a intenção subjacente.
- O pagamento da dívida é um movimento único: **externalizar intenção como artefato de primeira classe** — especificar intenção (não implementação), tratar AGENTS.md como ledger de intenção (não configuração), capturar decisões no momento em que acontecem (ADRs leves) e registrar aprendizados de experimentos falhos.

## Citações

> "Intent debt lives in the artifacts you may have never wrote: the goals, constraints, and rationale for why the system is the way it is."

> "An agent can't generate intent, because intent is the one input that has to come from you."

> "An agent starts most sessions cold. It carries none of the tacit intent your humans built up over years."

> "Un-externalized intent used to cost you once in a while, at onboarding or after someone left. Now you pay it every session."

> "Write down the why, because it's becoming the most valuable thing you can leave in the repo."

## Meu comentário

*Escreva aqui sua reação, surpresas, discordâncias.*

## Ver também

-
