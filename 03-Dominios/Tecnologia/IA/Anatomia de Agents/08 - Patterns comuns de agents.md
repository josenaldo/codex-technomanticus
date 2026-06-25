---
title: "Patterns comuns de agents"
created: 2026-04-11
updated: 2026-06-25
type: concept
progress: done
status: growing
publish: true
tags:
  - anatomia-agents
  - ia
  - agents
  - patterns
aliases:
  - Patterns de agents
  - Tipos de agent
  - Agent patterns
---

# Patterns comuns de agents

A demo foi um sucesso — o agent de triagem de tickets funcionou. Mas quando o gerente de produto perguntou por que demorava 8 segundos por ticket sendo que o protótipo de uma linha de LLM levava 0,3 segundos, ninguém tinha resposta imediata. No código: um orchestrator, um research-agent, um classifier-agent, um formatter-agent, e um validator. Cinco processos para o que era, no fundo, uma chamada de classificação.

O time tinha aplicado Pattern 5 (multi-agent orchestration) a um problema que era Pattern 6 (workflow híbrido) — um LLM call dentro de um pipeline fixo. A complexidade estava correta para uma escala 50× maior, não para a task em questão. Ninguém fez a pergunta simples antes de começar: "qual pattern resolve isso com menor complexidade?"

Reconhecer o pattern certo antes de construir não é otimização prematura — é a decisão de arquitetura mais importante do projeto.

> [!abstract] TL;DR
> Agents na prática se cristalizaram em **6 patterns** repetíveis: tool-using assistant (read-only Q&A), coding agent (Claude Code/Cursor — operam no filesystem), cloud agent (Codex/Devin — sandbox cloud), [[Dicionário de IA#RAG (Retrieval-Augmented Generation)|RAG]] agent (busca dinâmica + síntese), multi-agent orchestration (CrewAI/LangGraph/AutoGen), e workflow híbrido (workflow + chamadas LLM disfarçado de agent). Reconhecer o pattern certo é meio caminho — implementar o pattern errado é fonte clássica de over-engineering.

## Os 6 patterns

```mermaid
graph TB
    A["Pattern 1<br/>Tool-using assistant"] -->|"read-only<br/>tools"| A1["Q&A, research"]
    B["Pattern 2<br/>Coding agent (local)"] -->|"filesystem<br/>local"| B1["Claude Code, Cursor"]
    C["Pattern 3<br/>Cloud agent (async)"] -->|"sandbox<br/>cloud"| C1["Codex, Devin"]
    D["Pattern 4<br/>RAG agent"] -->|"retrieval<br/>iterativo"| D1["Q&A em base de conhecimento"]
    E["Pattern 5<br/>Multi-agent"] -->|"orchestrator<br/>+ sub-agents"| E1["Workflows complexos"]
    F["Pattern 6<br/>Workflow híbrido"] -->|"workflow<br/>+ LLM steps"| F1["Pipeline previsível"]
```

## Pattern 1 — Tool-using assistant

Agent único com **ferramentas read-only**, usado para Q&A e análise.

**Exemplos:** pesquisa, análise de logs, Q&A sobre documentação interna.

**Tools:** `web_search`, `read_url`, `read_doc`, `query_db`.

**[[Dicionário de IA#Guardrail|Guardrails]]:** nenhum crítico porque tools são safe.

**Quando usar:** task de pesquisa, exploração, sem ações destrutivas.

## Pattern 2 — Coding agent (local)

Agent que edita código, roda testes, faz commits. Opera no filesystem **local** do usuário.

**Exemplos:** Claude Code, Cursor, Cline, Aider.

**Tools:** `read_file`, `write_file`, `run_shell`, `git_commit`, `glob`, `grep`.

**Guardrails essenciais:**
- `max_steps` alto mas finito (30-50)
- Confirmação antes de `git push`, `rm -rf`, operations fora do workspace
- Sandboxing quando possível
- Human review antes de merge

**Quando usar:** desenvolvimento ativo, par programmer, refactoring.

Detalhamento em [[Agentes de Codificação]].

## Pattern 3 — Cloud agent (async)

Agent rodando em sandbox cloud, recebe task, retorna PR.

**Exemplos:** OpenAI Codex, Devin.

**Vantagens:**
- Não afeta ambiente local
- Pode rodar em paralelo
- Multi-hour tasks possível

**Desvantagens:**
- Menos interativo
- Difícil de "steer" quando vai pelo caminho errado
- Confiança alta exigida

**Quando usar:** tasks longas e bem-definidas, paralelismo desejado, time já maduro com agents.

## Pattern 4 — RAG agent

Pipeline RAG com agent decidindo quando buscar, o quê buscar, quando expandir busca.

**Exemplos:** agent de pesquisa que usa web search + read, agent de Q&A sobre base de conhecimento.

**Tools:** `search` (vector ou web), `rerank`, `read_doc`.

**Diferença de RAG "pipeline fixo":** o agent decide iterativamente se o contexto obtido é suficiente.

**Quando usar:**
- Q&A em base grande onde uma busca não basta
- Multi-hop reasoning (resposta requer juntar 2-3 fontes)
- Busca exploratória

Conecta com [[Context Engineering|06 - Dynamic retrieval beyond RAG]].

## Pattern 5 — Multi-agent orchestration

Múltiplos agents especializados coordenados por orchestrator. Usado em workflows complexos.

**Frameworks:** CrewAI, AutoGen, LangGraph, Claude Agent SDK.

**Use cases:**
- Geração de conteúdo (pesquisa → draft → revisão → publicação)
- Análise de dados (fetch → clean → analyze → visualize → report)
- SDD com CIV ([[Spec-Driven Development|09 - SDD com agentes — coordinator, implementor, validator]])

**Quando usar:** tarefa decomponível em sub-tarefas com expertise distinta.

Detalhamento em [[06 - Multi-agent — orchestrator e sub-agents]].

## Pattern 6 — Workflow híbrido (workflow + agent)

Workflow determinístico com **steps que são prompts LLM ou pequenos agents**. Muita gente chama de "agent" mas é mais workflow.

**Quando usar:** quando o processo é previsível e estável. Mais barato, mais debugável.

> [!quote] Anthropic
> *"Use workflows when you can, agents when you must."*

**Exemplo:**
```python
# Workflow híbrido — não é agent
def process_ticket(ticket):
    classified = llm_classify(ticket)              # LLM step
    if classified.category == "bug":
        triaged = llm_triage(ticket, classified)   # LLM step
        return create_jira_ticket(triaged)          # determinístico
    elif classified.category == "feature":
        return llm_route_to_team(ticket)            # LLM step
    return None
```

Pattern usado em **muito** do que se chama "agent em produção" hoje.

## Como reconhecer o pattern certo

> [!question] Heurística rápida
>
> | Sinal | Pattern |
> |---|---|
> | Apenas Q&A, sem ações | Pattern 1 |
> | Coding no IDE/CLI | Pattern 2 |
> | Long-running task assíncrona | Pattern 3 |
> | Q&A em base de conhecimento grande | Pattern 4 |
> | Sub-tarefas distintas com expertise diferente | Pattern 5 |
> | Processo previsível, mas alguns steps precisam LLM | Pattern 6 |

## Anti-patterns por confusão de pattern

- **Pattern 6 chamado de Pattern 5** — workflow virando "multi-agent" desnecessariamente
- **Pattern 2 chamado de Pattern 3** — coding agent local rodando "como se fosse cloud"
- **Pattern 1 com tools destrutivas** — Q&A virando ação sem proteção
- **Pattern 4 sem rerank** — RAG agent que só busca, nunca filtra

## Combinações que funcionam

- **Pattern 4 + Pattern 5**: research multi-agent (Explorer faz Pattern 4, Writer sintetiza)
- **Pattern 2 + Pattern 5**: coding com sub-agents especializados (security, tests, etc.)
- **Pattern 6 + Pattern 1**: workflow com tool-using assistant em um dos steps

## Sinais de over-engineering

> [!warning]
> - Pattern 5 quando Pattern 6 resolveria
> - Pattern 3 quando Pattern 2 bastava
> - Pattern 4 quando RAG fixo bastava
> - Multi-agent com 5 agents para task que cabia em 1
> - Custom framework quando SDK raw bastava
>
> A regra: **comece simples, adicione complexidade só quando dói**.

```mermaid
xychart-beta
    title "Latência mediana por pattern — tarefa de Q&A/análise equivalente"
    x-axis ["P1 tool-assist", "P6 híbrido", "P4 RAG agent", "P2 coding", "P3 cloud async", "P5 multi-agent"]
    y-axis "Latência mediana (s)" 0 --> 30
    bar [2, 3, 5, 15, 60, 25]
```

> Pattern 3 (cloud async) tem latência alta por design — roda tarefas de horas. Pattern 5 (multi-agent) é mais lento que single por overhead de coordenação. Pattern 6 (workflow híbrido) é o mais rápido de LLM-based porque o fluxo é determinístico e os LLM calls são pontuais.

```mermaid
flowchart LR
    subgraph Simples
        P1["P1: Tool-using assistant\n(read-only, Q&A)"]
        P6["P6: Workflow híbrido\n(fluxo fixo + LLM steps)"]
    end
    subgraph Médio
        P4["P4: RAG agent\n(retrieval iterativo)"]
        P2["P2: Coding agent\n(filesystem local)"]
    end
    subgraph Complexo
        P3["P3: Cloud agent\n(sandbox, assíncrono)"]
        P5["P5: Multi-agent\n(orchestrator + sub-agents)"]
    end
    Simples -->|"sub-tarefas distintas\nou sem ação destrutiva"| Médio
    Médio -->|"multi-hour task\nou especialização real"| Complexo
```

## Como explicar em inglês

Agent patterns are recurring architectural templates that map task types to implementation approaches. The tool-using assistant (Pattern 1) is a single agent with read-only tools — suitable for Q&A and research tasks where no side effects are needed. The coding agent (Pattern 2) operates on a local filesystem with write-capable tools like file editing and shell execution. The cloud agent (Pattern 3) runs in an isolated sandbox and returns a result asynchronously — useful for long-running tasks but harder to steer interactively. The RAG agent (Pattern 4) goes beyond a fixed retrieval pipeline by having the agent decide when to search, what to search for, and whether the retrieved context is sufficient. Multi-agent orchestration (Pattern 5) delegates subtasks to specialized sub-agents and is the most expensive pattern in latency and coordination overhead. The workflow hybrid (Pattern 6) is often mislabeled as an "agent" — it's a deterministic pipeline with LLM calls at specific steps, which makes it faster and more predictable than a true agent. Most production systems labeled "AI agents" are actually Pattern 6.

| Português | English |
|---|---|
| padrão de agent | agent pattern |
| assistente com ferramentas | tool-using assistant |
| agente de codificação | coding agent |
| agente em nuvem | cloud agent |
| agente RAG | RAG agent |
| orquestração multi-agente | multi-agent orchestration |
| workflow híbrido | hybrid workflow |
| recuperação iterativa | iterative retrieval |
| sandbox de execução | execution sandbox |
| tarefa assíncrona | asynchronous task |
| over-engineering | over-engineering |
| complexidade desnecessária | accidental complexity |

## Ver mais

- **Anthropic — *Building Effective Agents*** (2024): A categorização canônica dos cinco padrões de workflow — prompt chaining, routing, parallelization, orchestrator-workers, evaluator-optimizer. Esta nota os mapeia para os 6 patterns mais amplos usados em 2026.
- **OpenAI — *A Practical Guide to Building Agents*** (2025): Cada pattern descrito com exemplos de vertical (suporte ao cliente, pesquisa, coding). Útil para calibrar quando cada pattern é economicamente justificado.
- **LangChain Blog — *Agent supervisor patterns*** (2025): Análise técnica de como os patterns multi-agent se comportam com LangGraph StateGraph — incluindo ciclos, fallbacks e checkpointing. Referência prática para quem implementa Pattern 5.

## Veja também

- [[01 - O que é um agent]]
- [[06 - Multi-agent — orchestrator e sub-agents]]
- [[07 - Frameworks 2026]]
- [[Agentes de Codificação]]
- [[Spec-Driven Development|09 - SDD com agentes — coordinator, implementor, validator]]
- [[Context Engineering|06 - Dynamic retrieval beyond RAG]]

## Referências

- **Anthropic** — *Building Effective Agents* (2024) — categorização canônica
- **OpenAI** — *A Practical Guide to Building Agents* (2025)
- **LangChain Blog** — *Agent supervisor patterns* (2025)
