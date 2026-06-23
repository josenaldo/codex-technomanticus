---
title: "Respostas concisas — controlar output tokens"
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
  - Output optimization
  - Respostas concisas
  - max_tokens
---

# Respostas concisas — controlar output tokens

> [!abstract] TL;DR
> [[Dicionário de IA#Completion tokens|Output tokens]] são 3-6x mais caros que input. Modelos são verbosos por default — geram explicações, preambles, e reformulações desnecessárias. Instruções como "seja conciso", max_tokens apropriado, e format constraints (JSON em vez de markdown) reduzem output em 40-70%. A técnica mais eficaz: diga ao modelo o que NÃO gerar.

## Como funciona

### Técnicas para reduzir output

| Técnica | Redução | Exemplo |
|---------|---------|---------|
| **"Seja conciso"** no [[Dicionário de IA#system prompt\|system prompt]] | 20-30% | "Responda de forma direta, sem preâmbulos" |
| **max_tokens adequado** | Limita o máximo | 2048 em vez de default |
| **Format constraints** | 30-50% | "Responda apenas com o código, sem explicação" |
| **[[Dicionário de IA#structured output\|Structured output]] (JSON)** | 40-60% | JSON schema force formato mínimo |
| **"Não explique, apenas faça"** | 30-50% | Evita verbose explanations |

### Exemplos

```
❌ "Refatore esta função" → modelo gera explicação + código + resumo = 3000 tokens

✅ "Refatore esta função. Retorne APENAS o código refatorado, sem explicação." = 800 tokens
```

### System prompt para concisão

```markdown
## Regras de output
- Seja direto e conciso
- NÃO repita a pergunta
- NÃO adicione preâmbulos ("Claro!", "Vou ajudar...")
- NÃO explique mudanças óbvias
- Para código, retorne APENAS o código alterado
- Para diffs, use o formato mínimo
```

### Impacto financeiro

Modelo verboso (5k output/call) vs conciso (1.5k output/call), 100 calls/dia, Sonnet:

| | Verboso | Conciso |
|--|---------|---------|
| Output tokens/dia | 500k | 150k |
| Custo output/dia | $7.50 | $2.25 |
| **Economia mensal** | — | **$157.50** |

## Armadilhas

- **max_tokens muito baixo** — corta a resposta no meio. Defina com margem.
- **"Sem explicação" para tarefas de aprendizado** — se você QUER entender, não peça concisão.
- **Concisão vs qualidade** — para código simples, concisão ajuda. Para debugging, a explicação pode ser essencial.

## Veja também
- [[02 - Anatomia do gasto — input, output e reasoning]]
- [[14 - Thinking budget — controlar reasoning tokens]]

## Referências
- **Anthropic** — *Prompt Engineering Guide* (2026). Seção sobre concisão.
