---
title: "Thinking budget — controlar reasoning tokens"
created: 2026-05-02
updated: 2026-05-02
type: concept
progress: backlog
status: seedling
publish: true
tags:
  - economia-tokens
  - ia
  - custos
aliases:
  - Thinking budget
  - Reasoning budget
  - Extended thinking control
---

# Thinking budget — controlar reasoning tokens

> [!abstract] TL;DR
> Modelos de reasoning (Claude Thinking, o4) geram [[Dicionário de IA#Reasoning tokens|tokens internos de "pensamento"]] cobrados como output — a tier mais cara. Sem limite, podem gastar 50k+ [[Dicionário de IA#Token|tokens]] pensando em um problema simples. Use [[Dicionário de IA#Thinking budget|`thinking.budget_tokens`]] para limitar: 5k para tarefas moderadas, 20k para complexas, 50k+ só quando necessário. Não ativar thinking para tarefas simples é a melhor economia.

## Como funciona

### O custo do thinking

```json
// Claude com extended thinking
{
  "thinking": {"type": "enabled", "budget_tokens": 10000}
}

// Resposta:
{
  "usage": {
    "input_tokens": 5000,
    "output_tokens": 2000,
    "thinking_tokens": 8500  // ← cobrados como OUTPUT!
  }
}
```

Custo do thinking no Claude Opus: 8500 × $25/MTok = **$0.21** — só para "pensar".

### Calibrando o budget

| Tarefa | Budget recomendado | Custo extra (Opus) |
|--------|-------------------|-------------------|
| Fix de typo | 0 (não usar thinking) | $0 |
| Bug simples | 2000-5000 | $0.05-0.12 |
| Refactoring moderado | 5000-15000 | $0.12-0.37 |
| Debugging complexo | 15000-30000 | $0.37-0.75 |
| Arquitetura de sistema | 30000-50000 | $0.75-1.25 |
| Problema matemático difícil | 50000+ | $1.25+ |

### Regra prática

**Não ative thinking para tarefas que um modelo standard resolve.** Reserve para:
- Debugging de race conditions
- Decisões de arquitetura com trade-offs
- Problemas algorítmicos
- Refactoring com impacto em cascata

## Armadilhas

- **Thinking para tudo** — ativar thinking para autocomplete é pagar 10x mais pelo mesmo resultado.
- **Budget infinito** — sem limite, o modelo pode "pensar" por 100k+ tokens em problemas difíceis.
- **Não monitorar thinking_tokens** — se monitora só output, o custo de thinking fica invisível.

## Veja também
- [[02 - Anatomia do gasto — input, output e reasoning]]
- [[09 - Model routing — modelo certo para a tarefa]]
- [[13 - Reasoning models e chain-of-thought]] (Trilha 1)

## Referências
- **Anthropic** — *Extended Thinking Documentation* (2026).
