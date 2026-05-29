---
title: "Batch API — economia em volume"
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
  - Batch API
  - Batch processing LLM
---

# Batch API — economia em volume

> [!abstract] TL;DR
> [[Dicionário de IA#batch API|Batch APIs]] permitem enviar lotes de requests para processamento assíncrono com ~50% de desconto. SLA de entrega é horas (não segundos). Ideal para geração de testes em massa, documentação, migrações, e qualquer tarefa que não precisa de resposta em tempo real.

## Como funciona

### Fluxo

1. Montar array de requests (até 10.000)
2. Enviar via endpoint de batch
3. Esperar processamento (até 24h)
4. Baixar resultados

```json
// Anthropic Batch API
{
  "requests": [
    {"custom_id": "test-1", "params": {"model": "claude-sonnet-4.6", "messages": [...]}},
    {"custom_id": "test-2", "params": {"model": "claude-sonnet-4.6", "messages": [...]}},
    {"custom_id": "test-3", "params": {"model": "claude-sonnet-4.6", "messages": [...]}}
  ]
}
```

### Quando usar

| Tarefa | Batch? | Economia |
|--------|--------|----------|
| Gerar testes para 50 arquivos | ✅ | 50% |
| Documentar todas as funções de um módulo | ✅ | 50% |
| Migrar 200 arquivos de JS para TS | ✅ | 50% |
| Chat interativo | ❌ | — |
| Agente de coding em tempo real | ❌ | — |

### Pricing

| Provider | Desconto batch | SLA |
|----------|---------------|-----|
| Anthropic | ~50% | Até 24h |
| OpenAI | ~50% | Até 24h |
| Google | Variável | Variável |

## Armadilhas

- **SLA de horas** — não use para nada que precise de resposta imediata.
- **Debugging difícil** — se uma request do lote falha, identificar e reprocessar é mais complexo.
- **Não combinar com caching** — batch requests geralmente não se beneficiam de [[Dicionário de IA#Prompt caching|prompt caching]].

## Veja também
- [[09 - Model routing — modelo certo para a tarefa]]
- [[15 - Orçamento e hard limits]]

## Referências
- **Anthropic** — *Batch API Documentation* (2026).
- **OpenAI** — *Batch API Reference* (2026).
