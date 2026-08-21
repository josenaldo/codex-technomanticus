---
title: "Ferramentas de IA"
type: moc
publish: true
tags:
  - ferramentas-ia
  - ia
  - moc
created: 2026-04-11
updated: 2026-05-02
aliases:
  - Ferramentas IA
  - AI tools catalog
---

# Ferramentas de IA

Catálogo de ferramentas de IA usadas na engenharia de software em 2026 — modelos, IDEs com IA, agents cloud, e comparativos. Cada nota é deep dive em uma ferramenta específica, com setup, capabilities, custo, quando usar. Para visão arquitetural sobre **categorias** de ferramentas, ver [[Agentes de Codificação]] (coding agents) e [[Anatomia de Agents]] (fundamentos genéricos).

> [!tip] Como navegar
> Cada nota é um deep dive de uma ferramenta. Para escolher, use o **[[Comparativo de LLMs]]** que cruza modelos por custo, qualidade, latência, e use case.

## Ferramentas mapeadas

### Coding agents e IDEs

- **[[Claude]]** — Anthropic: Claude Code, API, Agent SDK, MCP, sandboxing
- **[[GitHub Copilot]]** — completions no IDE, chat, agent mode (Microsoft/GitHub)
- **[[Codex]]** — agent cloud da OpenAI (sandbox, async, retorna PR)
- **[[Gemini]]** — multimodal do Google, Code Assist, contextos longos

### Comparativos

- **[[Comparativo de LLMs]]** — tabela definitiva: qual usar quando, por custo, qualidade, latência

## Como escolher

```mermaid
graph TD
    A["Caso de uso"] --> B{"Tipo?"}
    B -->|"Coding diário"| C["[[Claude]] (Claude Code)<br/>ou Cursor"]
    B -->|"IDE-first"| D["[[GitHub Copilot]]<br/>ou Cursor"]
    B -->|"Async / overnight"| E["[[Codex]]<br/>ou Devin"]
    B -->|"Multimodal / contexto longo"| F["[[Gemini]]"]
    B -->|"Self-hosted"| G["DeepSeek / Qwen / Llama (ver [[Anatomia dos LLMs]])"]
    A --> H["Não sei?"]
    H --> I["[[Comparativo de LLMs]]"]
```

## O que falta neste catálogo

Não cobertos com profundidade aqui (ver outras trilhas):

- **Cursor** — coberto em [[Agentes de Codificação|04 - Cursor — AI-native IDE]]
- **[[Dicionário de IA#Aider|Aider]]** — coberto em [[Agentes de Codificação|09 - Aider — o pair programmer de terminal]]
- **OpenCode** — coberto em [[Agentes de Codificação|10 - OpenCode — o harness open source]]
- **Windsurf** — coberto em [[Agentes de Codificação|07 - Windsurf e Cascade]]
- **Devin** — coberto em [[Agentes de Codificação|13 - Devin e agentes autônomos cloud]]
- **Kiro** — coberto em [[Spec-Driven Development|08 - Ferramentas SDD — Kiro, Spec Kit, OpenSpec, Tessl]]
- **Letta, Mem0, Zep** — cobertos em [[Memória de Agentes]]

## Cadência de manutenção

Ferramentas mudam **rápido**. Versões, pricing, capabilities movem trimestralmente.

| Item | Cadência |
|---|---|
| Versões e capabilities | Trimestral |
| Pricing | Trimestral |
| Comparativo | Semestral |
| Setup guides | Anual ou em breaking changes |

## Veja também

- [[03-Dominios/Tecnologia/IA/index|index do domínio IA]]
- [[Anatomia dos LLMs]]
- [[Anatomia de Agents]]
- [[Agentes de Codificação]]
- [[03-Dominios/Tecnologia/IA/index|Formação Engenheiro de IA]]
