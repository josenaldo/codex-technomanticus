---
title: "How Claude Code works in large codebases: Best practices and where to start"
aliases: ["How Claude Code works in large codebases: Best practices and where to start"]
source: https://claude.com/blog/how-claude-code-works-in-large-codebases-best-practices-and-where-to-start
author: Anthropic Applied AI Team
site: Claude Blog
published: 2026-05-14
read: 2026-05-25
promovida_em: 2026-05-25
type: glosa
status: lido
tags: [claude-code, harness, ai-coding, large-codebases, enterprise]
lang: en
publish: false
---

# How Claude Code works in large codebases: Best practices and where to start — Anthropic Applied AI Team

## TL;DR

O Applied AI Team da Anthropic sintetiza padrões observados em deploys de Claude Code em codebases gigantes (multi-million LOC, legados de décadas, monorepos com milhares de devs): o **harness** — composto por CLAUDE.md, hooks, skills, plugins, LSP, MCP servers e subagents — importa tanto quanto o modelo. Configuração lean+hierárquica, manutenção a cada 3-6 meses e ownership organizacional (um DRI no mínimo) definem se a adoção decola ou estagna.

## Pontos-chave

- **Navegação agentic vs RAG**: Claude Code navega o codebase como um engenheiro (file system, grep, follow references) — não depende de índice central. Em escala grande, RAG falha porque o pipeline de embedding não acompanha o ritmo de commits; agentic search trabalha sempre do código vivo.
- **O harness importa tanto quanto o modelo** (tese central): cinco extension points — CLAUDE.md, hooks, skills, plugins, MCP servers — mais LSP integrations e subagents. A ordem de construção importa; cada camada se apoia na anterior.
- **CLAUDE.md hierárquico, lean e em camadas**: root pra "big picture", subdirectórios pra convenções locais. Inicializar Claude em subdirectório funciona melhor que na raiz — ele caminha pra cima e carrega CLAUDE.md aditivamente. Comandos de teste/lint devem ser escopados por subdirectório.
- **Hooks como mecanismo de auto-melhoria**, não só guardrail: stop hook reflete sobre a sessão e propõe edits no CLAUDE.md enquanto o contexto está fresco; start hook carrega contexto específico de módulo. Skills escopadas a paths evitam carregar tudo em toda sessão; plugins distribuem setups que funcionam ("good setups can stay tribal").
- **LSP dá precisão de símbolo**: grep por nome comum em codebase grande retorna milhares de matches; LSP filtra antes de Claude ler. Investimento de alto valor pra codebases multi-linguagem ou C/C++ — um cliente fez deploy org-wide especificamente pra isso antes do rollout.
- **Manutenção como ciclo**: revisar config a cada 3-6 meses. Regras escritas pra modelos antigos podem virar limitação ativa pra modelos novos (ex: hook forçando `p4 edit` ficou redundante quando Claude Code ganhou modo Perforce nativo). Atenção especial pós-release de novo modelo.
- **Ownership organizacional**: rollouts mais rápidos tiveram investimento dedicado em infra antes do acesso amplo. Papel emergente de "agent manager" (PM/eng híbrido); mínimo viável é um DRI com autoridade sobre configuração, permissions, marketplace de plugins e convenções de CLAUDE.md.

## Citações

> "One of the most common misconceptions about Claude Code is that its capabilities are solely defined by the model used. Teams focus on a model's benchmarks and how it performs on test tasks. In practice, the ecosystem built around the model—the harness—determines how Claude Code performs more than the model alone."

> "Most teams think of hooks as scripts that prevent Claude from doing something wrong, but their more valuable use is continuous improvement. A stop hook can reflect on what happened during a session and propose CLAUDE.md updates while the context is fresh."

> "As models evolve, instructions written for your current model can work against a future one. CLAUDE.md files that guided Claude through patterns it used to struggle with may either become unnecessary or actively constraining when the next model ships... Teams should expect to do a meaningful configuration review every three to six months."

> "Bottoms-up adoption generates enthusiasm but can fragment without someone to centralize what works. You need to have an individual or a team assemble and evangelize the right Claude Code conventions... Without that work, knowledge will stay tribal and adoption will plateau."

> "For organizations without a dedicated team, the minimum viable version is a DRI: one person with ownership over the Claude Code configuration, the authority to make calls on settings, permissions policy, the plugin marketplace, and CLAUDE.md conventions, and the responsibility to keep them current."

## Meu comentário

*Escreva aqui sua reação, surpresas, discordâncias.*

## Ver também

-
