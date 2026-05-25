---
title: "Pricing de APIs — como calcular custos"
created: 2026-05-02
updated: 2026-05-02
type: concept
status: seedling
publish: true
tags:
  - anatomia-llm
  - ia
  - tokens
aliases:
  - Custo de API
  - Pricing LLM
  - Token pricing
---

# Pricing de APIs — como calcular custos

> [!abstract] TL;DR
> APIs de LLM cobram por milhão de tokens (MTok), com preços separados para input e output — output é 3-6x mais caro. Em 2026, custos variam de $0.10/MTok (modelos budget) a $25/MTok (flagships). Prompt caching reduz input em até 90%. Batch APIs dão 50% de desconto. A fórmula do custo real é: (input_tokens × preço_input + output_tokens × preço_output + reasoning_tokens × preço_output) ÷ 1.000.000. Não controlar isso é queimar dinheiro.

## O que é

O modelo de pricing de LLM APIs é **pay-per-[[Dicionário de IA#Token|token]]**: você paga proporcionalmente à quantidade de tokens processados (input) e gerados (output) em cada chamada. Não há cobrança por tempo de sessão, número de chamadas, ou storage.

## Por que importa

Sem entender pricing, um engenheiro pode:

- Gastar $50/dia em uma sessão de agente que poderia custar $5
- Escolher o modelo mais caro por default quando um budget resolve
- Ignorar otimizações (caching, batching) que reduzem custos em 50-90%

## Como funciona

### A fórmula fundamental

```
Custo = (input_tokens × preço_input / 1M) + (output_tokens × preço_output / 1M)
```

**Exemplo concreto com Claude Sonnet 4.6:**

- Input: 50.000 tokens × $3.00/MTok = $0.15
- Output: 10.000 tokens × $15.00/MTok = $0.15
- **Total: $0.30 por chamada**

### Tabela de preços (maio 2026)

| Provider      | Modelo                | Tier      | Input $/MTok | Output $/MTok | Cache Read |
| ------------- | --------------------- | --------- | ------------ | ------------- | ---------- |
| **Anthropic** | Claude Opus 4.6       | Flagship  | $5.00        | $25.00        | $0.50      |
|               | Claude Sonnet 4.6     | Mid       | $3.00        | $15.00        | $0.30      |
|               | Claude Haiku 4.5      | Budget    | $1.00        | $5.00         | $0.10      |
| **OpenAI**    | GPT-5.4               | Flagship  | ~$2.50       | ~$15.00       | ~$0.25     |
|               | o4-mini               | Reasoning | ~$1.10       | ~$4.40        | —          |
|               | GPT-4.1 Nano          | Budget    | ~$0.10       | ~$0.40        | ~$0.01     |
| **Google**    | Gemini 3.1 Pro        | Flagship  | ~$2.00       | ~$12.00       | ~$0.20     |
|               | Gemini 3 Flash        | Mid       | ~$0.50       | ~$3.00        | ~$0.05     |
|               | Gemini 2.5 Flash-Lite | Budget    | ~$0.10       | ~$0.40        | —          |

### Mecanismos de desconto

| Mecanismo                  | Desconto típico | Como funciona                                                                   |
| -------------------------- | --------------- | ------------------------------------------------------------------------------- |
| **[[Dicionário de IA#Prompt caching\|Prompt caching]]**         | 50-90% no input | Partes estáticas do prompt (system, docs) são cacheadas entre chamadas          |
| **[[Dicionário de IA#batch API\|Batch API]]**              | ~50% em tudo    | Enviar tasks em lote para processamento assíncrono (SLA de horas, não segundos) |
| **Commitment plans**       | 20-40%          | Comprometer volume mensal com o provider                                        |
| **Provedor intermediário** | Variável        | Together, Fireworks, Groq oferecem modelos open-weight com markup menor         |

### Custos ocultos que as pessoas esquecem

| Item                       | Por que é custo oculto                                                                                |
| -------------------------- | ----------------------------------------------------------------------------------------------------- |
| **Tool definitions**       | Schemas JSON de ferramentas são input tokens — 10 tools podem consumir 2-5k tokens por chamada        |
| **Histórico acumulado**    | Cada turn do agente reenvia todo o histórico. Turn 50 inclui turns 1-49 como input                    |
| **[[Dicionário de IA#Reasoning tokens\|Reasoning tokens]]**       | Modelos de reasoning (o4, Claude Thinking) geram tokens internos de "pensamento" cobrados como output |
| **Retries**                | Se o agente erra e tenta de novo, paga-se duas vezes                                                  |
| **Contexto desnecessário** | Arquivos inteiros no prompt quando só 20 linhas eram relevantes                                       |

### Simulação: custo de um dia de desenvolvimento

Cenário: engenheiro usando Claude Sonnet 4.6 como agente de codificação, 8h de trabalho.

| Atividade                          | Chamadas | Input/chamada | Output/chamada | Subtotal    |
| ---------------------------------- | -------- | ------------- | -------------- | ----------- |
| Debugging (5 bugs)                 | 25       | 30k tokens    | 5k tokens      | $2.63       |
| Feature nova (2 features)          | 40       | 50k tokens    | 15k tokens     | $15.00      |
| Refactoring                        | 10       | 80k tokens    | 20k tokens     | $5.40       |
| Code review                        | 5        | 100k tokens   | 10k tokens     | $2.25       |
| **Total sem otimização**           | **80**   | —             | —              | **$25.28**  |
| **Total com prompt caching (70%)** | **80**   | —             | —              | **~$12.00** |

### Ferramentas de monitoramento

| Ferramenta                | O que faz                                                  |
| ------------------------- | ---------------------------------------------------------- |
| **ccusage**               | Monitora consumo do Claude Code por sessão                 |
| **Langfuse**              | Tracing de LLM com custo por chamada                       |
| **Helicone**              | Proxy que loga e visualiza consumo                         |
| **Dashboard do provider** | Visão geral de gastos na conta                             |
| **Planilha simples**      | Log diário de `usage.input_tokens` + `usage.output_tokens` |

## Checklist

- [ ] Definir orçamento diário/mensal antes de começar
- [ ] Configurar alertas de gasto no dashboard do provider
- [ ] Ativar prompt caching para system prompts e docs estáticos
- [ ] Usar Batch API para tarefas não urgentes
- [ ] Monitorar `usage` no response de cada chamada
- [ ] Revisar tool definitions — remover descrições verbosas
- [ ] Considerar modelo budget para tarefas simples (model routing)
- [ ] Sumarizar histórico longo em vez de acumular indefinidamente

## Armadilhas

- **"$3/MTok é barato"** — para uma chamada isolada, sim. Para 1000 chamadas/dia de um agente com 50k tokens de input cada, são $150/dia.
- **"Output tokens não importam"** — output é 3-6x mais caro que input. Um modelo verboso que gera 5x mais texto que o necessário custa 5x mais em output.
- **Não separar input e output no cálculo** — cálculos que usam "preço médio por token" subestimam custos reais porque ignoram a assimetria.
- **Ignorar reasoning tokens** — modelos de reasoning podem gastar 10-50x mais em tokens internos do que o output visível. Monitore `thinking_tokens` no response.
- **"Caching resolve tudo"** — caching ajuda com partes estáticas. Se cada chamada tem contexto significativamente diferente, o cache hit rate é baixo.

## Veja também

- [[02 - Tokens e tokenização]] — como contar tokens
- [[09 - APIs de LLM — anatomia de uma chamada]] — estrutura do request que gera custo
- [[11 - Prompt caching e otimizações de API]] — como reduzir a conta

## Referências

- **Anthropic** — *API Pricing* (2026). Tabela oficial de preços.
- **OpenAI** — *API Pricing* (2026). Tabela oficial de preços.
- **Artificial Analysis** — *LLM Cost Comparison* (2026). Comparativo independente.
- **CostGoat** — *LLM API Pricing Tracker* (2026). Agregador de preços atualizado.
