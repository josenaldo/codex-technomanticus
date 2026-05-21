---
title: "Economia de Tokens"
type: moc
publish: true
tags:
  - economia-tokens
  - ia
  - moc
created: 2026-05-02
updated: 2026-05-02
---

# Economia de Tokens

Em 2026, tokens são a unidade econômica da engenharia assistida por IA. Cada chamada de API, cada turno de agente, cada chain-of-thought interno consome tokens — e tokens custam dinheiro real. Engenheiros que ignoram essa economia descobrem do jeito difícil: faturas de quatro dígitos, contas pessoais inflando, ou times que param de usar a ferramenta porque o ROI virou negativo. Esta trilha mapeia o ciclo completo: por que tokens custam, por que agentes amplificam o gasto, quais técnicas reduzem input/output/reasoning, qual arquitetura escolher, como impor hard limits, como auditar desperdício, e quando o agente realmente vale o custo.

> [!info] Pré-requisitos
> Recomendado ter lido a [[Anatomia dos LLMs]] (Trilha 1), especialmente [[02 - Tokens e tokenização]], [[10 - Pricing de APIs — como calcular custos]] e [[11 - Prompt caching e otimizações de API]]. Se já trabalha com [[Agentes de Codificação]] (Trilha 2), as notas sobre compactação, sub-agentes e tool compression vão ressoar imediatamente.

> [!warning] Preços e ferramentas mudam rápido
> Os preços, planos e ferramentas (ccusage, Langfuse, etc.) refletem o estado de **maio de 2026**. Tabelas de pricing mudam a cada trimestre — verifique sempre a documentação oficial antes de decidir arquitetura.

## Comece por aqui

Trilha sequencial recomendada — diagnóstico → otimização de input → arquitetura → output → governança.

### Bloco 1 — O Problema e a Visibilidade (4 notas)

Antes de otimizar, é preciso entender por que custa, por que agentes custam mais, e como medir.

- [[01 - O problema — por que tokens custam dinheiro]] — economia de GPU, prefill vs decode, escala mensal
- [[02 - Anatomia do gasto — input, output e reasoning]] — as três dimensões do custo, multiplicadores típicos
- [[03 - Por que agentes gastam tanto]] — loop, retries, tools verbosos, rabbit holes
- [[04 - Monitoramento — ccusage, Langfuse, dashboards]] — ferramentas para enxergar o gasto real

### Bloco 2 — Reduzir o Input (4 notas)

A maior parte do custo está no input. Quatro técnicas que cortam tokens antes deles entrarem no modelo.

- [[05 - Prompt caching na prática]] — KV cache reuse, 90% de desconto em prefixos repetidos
- [[06 - Context pruning — o que remover do prompt]] — sinal vs ruído, pruning estático e dinâmico
- [[07 - Compressão de tool definitions]] — schemas inflam contexto, como enxugá-los
- [[08 - Compactação de histórico em agentes]] — summarization, sliding window, compactação automática

### Bloco 3 — Arquitetura Econômica (4 notas)

Não é só sobre cortar — é sobre escolher o modelo, o modo, e o padrão arquitetural certos.

- [[09 - Model routing — modelo certo para a tarefa]] — Haiku/Sonnet/Opus, cascading, roteamento inteligente
- [[10 - Sub-agentes especializados]] — isolamento de contexto, delegação focada
- [[11 - Semantic caching]] — cache de respostas, vector DB, complemento ao prompt cache
- [[12 - Batch API — economia em volume]] — 50% off para workloads assíncronos

### Bloco 4 — Controle de Saída (2 notas)

Output e reasoning também custam — e são onde mais gente esquece de olhar.

- [[13 - Respostas concisas — controlar output tokens]] — `max_tokens`, system prompts, instruções
- [[14 - Thinking budget — controlar reasoning tokens]] — extended thinking não é grátis

### Bloco 5 — Governança e Operação (6 notas)

Da disciplina técnica à decisão de negócio: budget, hard limits, auditoria, ROI, planos, futuro.

- [[15 - Orçamento e hard limits]] — `max_tokens`, spending caps, kill switches em sessões
- [[16 - Auditoria de consumo]] — investigação causal, top offenders, cadência de revisão
- [[17 - ROI de IA — quando o agente vale o custo]] — payback, vanity metrics, decision framework
- [[18 - Playbook de economia — checklist completo]] — checklist consolidado, ordem de aplicação
- [[19 - Planos e tiers — Max, Pro, API, Enterprise]] — quando faz sentido cada modalidade
- [[20 - O futuro — tokens cada vez mais baratos]] — Moore-like trend, commoditização, implicações
- [[21 - Hacks de trincheira — Claude, Gemini e Copilot em 2026]] — manobras específicas por provedor

## Rotas alternativas

### Rota emergencial (já estou gastando demais)
*"Minha fatura está fora de controle, preciso cortar agora"*

[[04 - Monitoramento — ccusage, Langfuse, dashboards]] → [[05 - Prompt caching na prática]] → [[13 - Respostas concisas — controlar output tokens]] → [[15 - Orçamento e hard limits]] → [[18 - Playbook de economia — checklist completo]]

### Rota arquiteto (projetar sistema cost-aware)
*"Vou desenhar um sistema novo e quero custo previsível desde o dia 1"*

[[02 - Anatomia do gasto — input, output e reasoning]] → [[09 - Model routing — modelo certo para a tarefa]] → [[10 - Sub-agentes especializados]] → [[11 - Semantic caching]] → [[12 - Batch API — economia em volume]]

### Rota agente (otimizar Claude Code, Cursor, Aider)
*"Uso agentes de codificação e quero diminuir o gasto por sessão"*

[[03 - Por que agentes gastam tanto]] → [[05 - Prompt caching na prática]] → [[07 - Compressão de tool definitions]] → [[08 - Compactação de histórico em agentes]] → [[10 - Sub-agentes especializados]] → [[14 - Thinking budget — controlar reasoning tokens]]

### Rota governança (líder técnico / engineering manager)
*"Preciso decidir budget, métricas e ROI para o time"*

[[15 - Orçamento e hard limits]] → [[16 - Auditoria de consumo]] → [[17 - ROI de IA — quando o agente vale o custo]] → [[19 - Planos e tiers — Max, Pro, API, Enterprise]]

### Rota pessoa física (Pro/Max vs API)
*"Sou dev individual — vale Max, Pro, API ou misturar?"*

[[19 - Planos e tiers — Max, Pro, API, Enterprise]] → [[04 - Monitoramento — ccusage, Langfuse, dashboards]] → [[18 - Playbook de economia — checklist completo]]

### Rota estratégica (entender para onde vai)
*"Quero entender a tendência de preços antes de bater martelo em arquitetura"*

[[01 - O problema — por que tokens custam dinheiro]] → [[19 - Planos e tiers — Max, Pro, API, Enterprise]] → [[20 - O futuro — tokens cada vez mais baratos]]

## Leituras recomendadas

| Fonte | Tipo | Cobertura |
|-------|------|-----------|
| *Anthropic — Prompt Caching* | Docs oficial | Nota 05 |
| *Anthropic — Batch API* | Docs oficial | Nota 12 |
| *Anthropic — Extended Thinking* | Docs oficial | Nota 14 |
| *Anthropic — Building effective agents* | Artigo | Nota 03 |
| *Anthropic Cookbook — Token-efficient tool use* | Repo | Nota 07 |
| *ccusage* | CLI / npm | Notas 04, 16 |
| *Langfuse — Trace analysis* | Docs oficial | Notas 04, 16 |
| *GPTCache* | Open source | Nota 11 |
| *Eugene Yan — Patterns for LLM Systems* | Artigo | Nota 11 |
| *Artificial Analysis — LLM Cost Comparison* | Site | Notas 02, 09, 19 |
| *METR — AI productivity measurement* | Pesquisa | Nota 17 |

## Veja também

- [[Memória de Agentes]] — técnicas de compactação e shared memory complementam Bloco 2
- [[Agentes de Codificação]] — ferramentas que se beneficiam diretamente desta trilha
- [[RAG e Vector Databases]] — base para [[11 - Semantic caching]]

## Todas as notas

```dataview
TABLE
  title AS "Título",
  status AS "Status",
  join(tags, ", ") AS "Tags"
FROM "03-Domínios/IA/Economia de Tokens"
WHERE type != "moc"
SORT file.name ASC
```
