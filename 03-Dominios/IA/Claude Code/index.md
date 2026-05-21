---
title: "Claude Code"
type: moc
publish: true
created: 2026-05-13
updated: 2026-05-13
status: seedling
tags:
  - claude-code
  - ia
  - moc
  - ferramentas
aliases:
  - Claude Code Trail
  - Claude Code CLI
---

# Claude Code

> [!abstract] TL;DR
> Trilha Claude Code em 6 galhos: Mental Model, Configuração, Hooks e Guardrails, Skills e MCP, Workflows, Time e Automação. Cobre desde como o agente realmente funciona até CI/CD, multi-agent e governança de time.

Claude Code é o agente de terminal da Anthropic — e usá-lo bem é diferente de apenas rodar comandos. Esta trilha cobre o que um senior dev precisa saber para ir além do básico: entender o loop agentic, configurar o agente para o seu projeto, programar guardrails com hooks, criar skills modulares, trabalhar com padrões avançados (TDD, multi-agent, sessões paralelas) e escalar o uso para times e pipelines de CI/CD.

> [!tip] Por onde começar?
>
> Depende do seu objetivo:
>
> - **"Quero ser mais produtivo hoje"** → Mental Model → Configuração → Workflows
> - **"Quero montar o setup do meu time"** → Configuração → Hooks e Guardrails → Time e Automação
> - **"Quero automatizar com CI/CD"** → Mental Model → Hooks e Guardrails → Time e Automação

## Conteúdo

### Galhos da trilha Claude Code

- [[03-Dominios/IA/Claude Code/Mental Model/index|Mental Model]] — galho 1: o loop agentic, como o agente lê código, tool use, context window, modos de operação, compaction, custo e decisão
- [[03-Dominios/IA/Claude Code/Configuração/index|Configuração]] — galho 2: hierarquia de configuração, CLAUDE.md, settings.json, permissions, aliases e armadilhas
- [[03-Dominios/IA/Claude Code/Hooks e Guardrails/index|Hooks e Guardrails]] — galho 3: lifecycle de hooks, PreToolUse, PostToolUse, Stop, guardrails, meta-agente, segurança, debugging
- [[03-Dominios/IA/Claude Code/Skills e MCP/index|Skills e MCP]] — galho 4: anatomia de skills, criar skills, MCP servers essenciais, criar MCP customizado, composição, versionamento em time
- [[03-Dominios/IA/Claude Code/Workflows/index|Workflows]] — galho 5: Plan Mode, TDD, refactoring pesado, debugging, code review, sessões paralelas, sub-agents, multi-agent, prompting, gestão de contexto
- [[03-Dominios/IA/Claude Code/Time e Automação/index|Time e Automação]] — galho 6: headless mode, CI/CD, dispatch, CLAUDE.md compartilhado, custo, segurança organizacional, onboarding, qualidade de output

## Veja também

- [[03-Dominios/IA/Agentes de Codificação/05 - Claude Code — terminal-first agent|Claude Code — terminal-first agent]] — overview comparativo com outros agentes de codificação
- [[03-Dominios/IA/Agentes de Codificação/15 - MCP — o protocolo universal|MCP — o protocolo universal]] — protocolo que sustenta a extensibilidade
- [[03-Dominios/IA/Agentes de Codificação/12 - Multi-agent — workflows com múltiplos agentes|Multi-agent]] — contexto mais amplo de workflows multi-agente
- [[03-Dominios/IA/Agentes de Codificação/index|Agentes de Codificação]] — trilha que contextualiza Claude Code entre os demais players
