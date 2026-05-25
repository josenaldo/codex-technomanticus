---
title: "Agentes de Codificação"
type: moc
publish: true
tags:
  - agentes-codificacao
  - ia
  - moc
created: 2026-05-02
updated: 2026-05-02
---

# Agentes de Codificação

Em 2026, ferramentas de codificação AI evoluíram de "autocomplete de uma linha" para agentes autônomos que planejam, executam, testam e iteram sobre codebases inteiros. Mas a ferramenta é só metade da equação — a outra metade é saber COMO usá-la. Esta trilha mapeia todo o ecossistema: da filosofia (vibe coding vs disciplina) às ferramentas (Cursor, Claude Code, Copilot, harnesses open source), passando por protocolos (MCP), padrões de trabalho (loop agentic, multi-agent), e governança (comprehension gate, human-in-the-loop).

> [!info] Pré-requisitos
> Recomendado ter lido a [[Anatomia dos LLMs]] (Trilha 1), especialmente notas sobre tokens, context window, e APIs.

> [!tip] Como usar esta trilha
> Leia sequencialmente se está começando. Se já usa ferramentas AI, pule para a rota que resolve seu problema atual.

## Comece por aqui

Trilha sequencial recomendada.

### Bloco 1 — Filosofia e Fundamentos

O que significa codificar com IA, o gap entre usar e usar bem, e a prática central de qualidade.

- [[01 - De autocomplete a agentes autônomos]] — a evolução em 4 estágios
- [[02 - Vibe coding vs engenharia disciplinada]] — o gap que define profissionais
- [[03 - O comprehension gate]] — a regra de ouro: se não entende, não merge

### Bloco 2 — Os Players

Cada ferramenta com seus pontos fortes, limitações, configuração e quando usar.

- [[04 - Cursor — AI-native IDE]] — Composer, Agent Mode, .cursorrules
- [[05 - Claude Code — terminal-first agent]] — hooks, permissions, CLAUDE.md, MCP
- [[06 - GitHub Copilot e Copilot Agents]] — autocomplete líder + agents no GitHub
- [[07 - Windsurf e Cascade]] — o competidor com Flows
- [[08 - Gemini CLI — o player Google]] — contexto ultra-longo + multimodal
- [[09 - Aider — o pair programmer de terminal]] — Git-first, open source, model-agnostic

### Bloco 3 — Ecossistema e Protocolos

Alternativas open source, como comparar, e o protocolo que une tudo.

- [[10 - OpenCode — o harness open source]] — OpenCode, Cline, Continue
- [[11 - Comparativo — qual ferramenta para qual tarefa]] — mega-tabela de decisão
- [[12 - Multi-agent — workflows com múltiplos agentes]] — pipeline, paralelo, hierárquico
- [[13 - Devin e agentes autônomos cloud]] — expectativa vs realidade

### Bloco 4 — Workflows e Governança

Como configurar, como funciona o loop, quando confiar, e como medir.

- [[14 - agents.md e configuração de projeto]] — CLAUDE.md, .cursorrules, cross-tool
- [[15 - MCP — o protocolo universal]] — o "USB da IA" para ferramentas
- [[16 - O loop agentic — plan, act, observe]] — o ciclo fundamental + custos
- [[17 - Human-in-the-loop — quando (não) confiar]] — espectro de autonomia
- [[18 - Benchmarks e avaliação — SWE-bench e além]] — como medir qualidade real

## Rotas alternativas

### Rota prática (configurar e usar já)

*"Preciso começar a usar ferramentas AI agora"*

[[04 - Cursor — AI-native IDE]] → [[14 - agents.md e configuração de projeto]] → [[11 - Comparativo — qual ferramenta para qual tarefa]]

### Rota terminal (devs CLI-first)

*"Prefiro terminal, não IDE"*

[[05 - Claude Code — terminal-first agent]] → [[09 - Aider — o pair programmer de terminal]] → [[10 - OpenCode — o harness open source]] → [[15 - MCP — o protocolo universal]]

### Rota qualidade (não gerar código lixo)

*"Quero usar IA sem acumular tech debt"*

[[02 - Vibe coding vs engenharia disciplinada]] → [[03 - O comprehension gate]] → [[17 - Human-in-the-loop — quando (não) confiar]] → [[18 - Benchmarks e avaliação — SWE-bench e além]]

### Rota orçamento (gastar pouco ou zero)

*"Não tenho budget para ferramentas pagas"*

[[10 - OpenCode — o harness open source]] → [[09 - Aider — o pair programmer de terminal]] → [[11 - Comparativo — qual ferramenta para qual tarefa]] (rota custo-zero)

### Rota arquiteto (entender e decidir)

*"Preciso decidir ferramentas e workflows para meu time"*

[[01 - De autocomplete a agentes autônomos]] → [[11 - Comparativo — qual ferramenta para qual tarefa]] → [[12 - Multi-agent — workflows com múltiplos agentes]] → [[16 - O loop agentic — plan, act, observe]] → [[15 - MCP — o protocolo universal]]

## Leituras recomendadas

| Fonte                                      | Tipo         | Cobertura   |
| ------------------------------------------ | ------------ | ----------- |
| *Anthropic — Claude Code Documentation*    | Docs oficial | Blocos 2, 4 |
| *Cursor — Documentation*                   | Docs oficial | Bloco 2     |
| *[[Andrej Karpathy\|Karpathy]] — Vibe Coding*                   | Post         | Bloco 1     |
| *Plus8Soft — The Comprehension Gate*       | Artigo       | Bloco 1     |
| *Yao et al. — ReAct: Reasoning and Acting* | Paper        | Bloco 4     |
| *Anthropic — MCP Specification*            | Spec         | Bloco 3     |
| *SWE-bench Leaderboard*                    | Benchmark    | Bloco 4     |

## Todas as notas

```dataview
TABLE
  title AS "Título",
  status AS "Status",
  join(tags, ", ") AS "Tags"
FROM "03-Dominios/IA/Agentes de Codificação"
WHERE type != "moc"
SORT file.name ASC
```
