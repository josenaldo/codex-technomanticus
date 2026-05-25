---
title: "Context Engineering"
type: moc
publish: true
tags:
  - context-engineering
  - ia
  - moc
created: 2026-05-02
updated: 2026-05-02
---

# Context Engineering

Em 2026, prompt engineering é o jardim de infância. A disciplina real que separa demos de produtos é **context engineering**: o ambiente informacional inteiro que cerca o LLM — system prompts, retrieved docs, tool definitions, memória persistente, histórico, scratchpad. [[Andrej Karpathy|Karpathy]] resumiu: *"o LLM é a CPU, a janela de contexto é a RAM, e você é o sistema operacional"*. Anthropic chamou de "load-bearing skill" do ano. Esta trilha mapeia o campo: dos fundamentos teóricos (context rot, atenção quadrática) à arquitetura (pipelines, camadas, retrieval), à memória (self-editing, shared, structured) e à produção (guardrails, qualidade, setup completo).

> [!info] Pré-requisitos
> Recomendado ter lido [[Anatomia dos LLMs]] (Trilha 1) — especialmente [[03 - A janela de contexto]], [[04 - Atenção e o mecanismo transformer]] e [[11 - Prompt caching e otimizações de API]]. [[Agentes de Codificação]] (Trilha 2) e [[Economia de Tokens]] (Trilha 3) são contexto direto: os ganhos de redução de tokens vêm em grande parte de bom context engineering.

> [!warning] Disciplina em ebulição
> Context engineering ainda está sendo formalizada. Ferramentas (Letta, Zep, Mem0, AGENTS.md spec) evoluem rápido. As **ideias** desta trilha (camadas, pipelines, rot, JIT) são robustas; as **ferramentas específicas** podem ter sido superadas — sempre verifique versões.

## Comece por aqui

Trilha sequencial recomendada — fundamentos → arquitetura → memória → produção.

### Bloco 1 — Fundamentos (3 notas)

O salto conceitual de prompt para context, a hierarquia de pilares, e o mecanismo central que justifica tudo: context rot.

- [[01 - De prompt engineering a context engineering]] — a evolução, a definição operacional, a analogia OS de Karpathy
- [[02 - Os quatro pilares — prompt, context, intent, specification]] — hierarquia de disciplinas, framing alternativo write/select/compress/isolate
- [[03 - Context rot e atenção diluída]] — Chroma research 2025, lost-in-the-middle, atenção quadrática

### Bloco 2 — Arquitetura de Contexto (4 notas)

Como montar o ambiente em runtime, em camadas, com retrieval dinâmico e compressão.

- [[04 - Context pipelines — montagem dinâmica]] — assembly em runtime, fontes, spectrum pre-indexed↔JIT
- [[05 - Camadas de contexto — persistente, temporal, transiente]] — hierarquia de memória, onde guardar o quê
- [[06 - Dynamic retrieval beyond RAG]] — JIT retrieval, MCP, Claude Code como referência
- [[07 - Compressão e pruning de informação]] — compactação, sliding window, padrão híbrido

### Bloco 3 — Memória e Estado (4 notas)

Padrões para o estado do agente: self-editing, multi-agent, structured files, instructions versionadas.

- [[08 - Memória agentica — self-editing memory]] — MemGPT/Letta, OS-inspired, tool calls de memória
- [[09 - Shared memory em multi-agent]] — handoff vs shared state vs message queue, regra do resumo
- [[10 - Structured state tracking]] — `NOTES.md`, `TODO.md`, `STATE.md` como memory layer
- [[11 - Skills e instructions como contexto]] — AGENTS.md spec, cross-tool config, skills marketplace

### Bloco 4 — Controle e Produção (3 notas)

Da disciplina ao deploy: guardrails determinísticos, métrica de qualidade, setup end-to-end.

- [[12 - Guardrails determinísticos]] — control plane, pre/post-LLM, kill paths, three-tier control
- [[13 - Entropia e qualidade de contexto]] — sinal por token, "context as architecture", context products
- [[14 - Context engineering na prática — setup completo]] — checklist end-to-end, de zero ao agente robusto

### Bloco 5 — Prompting e Skills (2 notas)

Técnicas atomizadas e distribuição de behaviors reutilizáveis.

- [[15 - Técnicas de prompting — zero-shot, few-shot, CoT, ToT]] — taxonomia de técnicas, quando usar cada
- [[16 - Agent skills marketplace e SKILL.md]] — formato, distribuição, ecossistema 2026

## Rotas alternativas

### Rota prática (preciso aplicar agora)
*"Tenho um projeto rodando — quero context engineering aplicado essa semana"*

[[01 - De prompt engineering a context engineering]] → [[11 - Skills e instructions como contexto]] → [[10 - Structured state tracking]] → [[14 - Context engineering na prática — setup completo]]

### Rota teórica (entender o campo)
*"Quero entender por que isso virou disciplina"*

[[01 - De prompt engineering a context engineering]] → [[02 - Os quatro pilares — prompt, context, intent, specification]] → [[03 - Context rot e atenção diluída]] → [[13 - Entropia e qualidade de contexto]]

### Rota multi-agent (orquestração)
*"Vou construir sistema com vários agentes colaborando"*

[[04 - Context pipelines — montagem dinâmica]] → [[08 - Memória agentica — self-editing memory]] → [[09 - Shared memory em multi-agent]] → [[12 - Guardrails determinísticos]]

### Rota arquiteto (design de sistemas)
*"Preciso desenhar a infra de context engineering para um produto"*

[[03 - Context rot e atenção diluída]] → [[04 - Context pipelines — montagem dinâmica]] → [[05 - Camadas de contexto — persistente, temporal, transiente]] → [[06 - Dynamic retrieval beyond RAG]] → [[14 - Context engineering na prática — setup completo]]

### Rota custo (alinhada com Trilha 3)
*"Já leio Economia de Tokens — quero saber como isso conecta com context engineering"*

[[03 - Context rot e atenção diluída]] → [[07 - Compressão e pruning de informação]] → [[06 - Dynamic retrieval beyond RAG]] → [[Economia de Tokens|03 - Por que agentes gastam tanto]]

## Leituras recomendadas

| Fonte | Tipo | Cobertura |
|-------|------|-----------|
| *Anthropic — Effective context engineering for AI agents* | Artigo | Trilha inteira |
| *Karpathy — Tweet on context engineering (jun 2025)* | Tweet | Notas 01-02 |
| *Chroma Research — Context Rot* | Paper técnico | Nota 03 |
| *Liu et al. — Lost in the Middle* | Paper TACL | Nota 03 |
| *Packer et al. — MemGPT (arxiv:2310.08560)* | Paper | Nota 08 |
| *Letta — Memory Blocks* | Doc | Nota 08 |
| *AGENTS.md spec (agents.md)* | Spec | Nota 11 |
| *Anthropic Cookbook — Context engineering* | Cookbook | Notas 04, 07 |
| *Atlan — Context Engineering Framework* | Guia enterprise | Notas 02, 13 |
| *Sebastian Raschka — Components of A Coding Agent* | Artigo | Notas 07, 10 |

## Veja também

- [[Memória de Agentes]] — pesquisa irmã focada em memória; sobreposição forte em Bloco 3
- [[Agentes de Codificação]] — onde context engineering vive na prática (CLAUDE.md, MCP)
- [[Economia de Tokens]] — context engineering bem feito reduz custo automaticamente
- [[Spec-Driven Development]] — specification engineering como pilar superior (nota 02)
- [[RAG e Vector Databases]] — fundação do retrieval (nota 06)

## Todas as notas

```dataview
TABLE
  title AS "Título",
  status AS "Status",
  join(tags, ", ") AS "Tags"
FROM "03-Dominios/IA/Context Engineering"
WHERE type != "moc"
SORT file.name ASC
```
