---
title: "Hooks e Guardrails — Claude Code"
type: moc
publish: true
created: 2026-05-13
updated: 2026-05-13
status: seedling
tags:
  - claude-code
  - hooks
  - guardrails
  - moc
aliases:
  - Galho 3 - Hooks e Guardrails
  - Claude Code Hooks
---

# Hooks e Guardrails — Claude Code

> [!abstract] TL;DR
> Galho 3 da trilha Claude Code. Cobre o sistema de hooks (lifecycle, PreToolUse, PostToolUse, Stop), guardrails para bloquear ações perigosas, delegação de permissão a outro LLM, segurança e como testar hooks. Hooks são o sistema nervoso do Claude Code — sem eles, você está dando autonomia sem controle.

## Sobre este galho

Hooks transformam Claude Code de "agente que pede permissão" em "agente com políticas programáticas". PreToolUse intercepta antes de executar (permite bloquear, validar, logar). PostToolUse dispara depois (auto-lint, auto-format, notificações). Stop hook executa quando o agente termina.

Guardrails são hooks que bloqueiam ações destrutivas — sem eles, auto mode é risco. Com eles, é produtividade real.

## Notas

1. [[03-Dominios/IA/Claude Code/Hooks e Guardrails/01 - Sistema de hooks|01 - Sistema de hooks — visão geral do lifecycle]]
2. [[03-Dominios/IA/Claude Code/Hooks e Guardrails/02 - PreToolUse|02 - PreToolUse — interceptar e validar antes de executar]]
3. [[03-Dominios/IA/Claude Code/Hooks e Guardrails/03 - PostToolUse|03 - PostToolUse — automação pós-ação]]
4. [[03-Dominios/IA/Claude Code/Hooks e Guardrails/04 - Stop hook|04 - Stop hook — notificação, logging, cleanup]]
5. [[03-Dominios/IA/Claude Code/Hooks e Guardrails/05 - Guardrails|05 - Guardrails — bloquear comandos destrutivos]]
6. [[03-Dominios/IA/Claude Code/Hooks e Guardrails/06 - Delegar permissão|06 - Delegar permissão a outro LLM — pattern meta-agente]]
7. [[03-Dominios/IA/Claude Code/Hooks e Guardrails/07 - Segurança com hooks|07 - Hooks para segurança — commits, push force, rm -rf]]
8. [[03-Dominios/IA/Claude Code/Hooks e Guardrails/08 - Testando hooks|08 - Testando e debugando hooks]]

## Veja também

- [[03-Dominios/IA/Claude Code/index|Claude Code]] — tronco da trilha
- [[03-Dominios/IA/Claude Code/Configuração/index|Configuração]] — galho anterior
- [[03-Dominios/IA/Claude Code/Skills e MCP/index|Skills e MCP]] — próximo galho
- [[03-Dominios/IA/Claude Code/Time e Automação/index|Time e Automação]] — onde guardrails se tornam políticas de time
