---
title: "Configuração — Claude Code"
type: moc
publish: true
created: 2026-05-13
updated: 2026-05-13
status: seedling
tags:
  - claude-code
  - configuracao
  - moc
aliases:
  - Galho 2 - Configuração
  - Claude Code Config
---

# Configuração — Claude Code

> [!abstract] TL;DR
> Galho 2 da trilha Claude Code. Cobre toda a camada de configuração: hierarquia global → projeto → user, anatomia do CLAUDE.md, settings.json, sistema de permissões, aliases e slash commands. O maior multiplicador de produtividade ao usar Claude Code é configurar bem.

## Sobre este galho

[[Dicionário de IA#Claude Code|Claude Code]] sem configuração é como um dev sem contexto de projeto — ele funciona, mas gera código genérico que não segue seus padrões. CLAUDE.md é o arquivo que transforma o [[Dicionário de IA#Agent|agente]] genérico em especialista do seu projeto. settings.json controla o que ele pode e não pode fazer. Permissions define granularidade de acesso.

Este galho cobre cada peça da camada de configuração, com receitas prontas para projetos reais.

## Notas

1. [[03-Dominios/IA/Claude Code/Configuração/01 - Hierarquia de configuração|01 - Hierarquia de configuração — global, projeto, user]]
2. [[03-Dominios/IA/Claude Code/Configuração/02 - CLAUDE.md anatomia|02 - CLAUDE.md — anatomia e o que colocar em cada seção]]
3. [[03-Dominios/IA/Claude Code/Configuração/03 - CLAUDE.md receitas|03 - CLAUDE.md — receitas para Node, Python, Go, monorepos]]
4. [[03-Dominios/IA/Claude Code/Configuração/04 - settings.json|04 - settings.json — permissões, comportamentos, env vars]]
5. [[03-Dominios/IA/Claude Code/Configuração/05 - Permissions|05 - Permissions — allow/deny por ferramenta e por comando]]
6. [[03-Dominios/IA/Claude Code/Configuração/06 - Slash commands customizados|06 - Slash commands customizados]]
7. [[03-Dominios/IA/Claude Code/Configuração/07 - Pasta .claude|07 - A pasta .claude — estrutura completa]]
8. [[03-Dominios/IA/Claude Code/Configuração/08 - Armadilhas de configuração|08 - Armadilhas de configuração — erros comuns e como evitar]]

## Veja também

- [[03-Dominios/IA/Claude Code/index|Claude Code]] — tronco da trilha
- [[03-Dominios/IA/Claude Code/Mental Model/index|Mental Model]] — galho anterior
- [[03-Dominios/IA/Claude Code/Hooks e Guardrails/index|Hooks e Guardrails]] — próximo galho recomendado
- [[03-Dominios/IA/Agentes de Codificação/14 - agents.md e configuração de projeto|agents.md e configuração de projeto]] — contexto adicional
