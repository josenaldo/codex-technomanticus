---
title: O problema — por que tokens custam dinheiro
created: 2026-05-02
updated: 2026-07-03
type: concept
status: evergreen
publish: true
fase: Iniciado
tags:
  - economia-tokens
  - ia
  - custos
aliases:
  - Token economics
  - Por que tokens custam
progress: done
---

# O problema — por que tokens custam dinheiro

> [!abstract] TL;DR
> Cada token que um LLM processa custa dinheiro porque consome GPU: compute na fase prefill (input) e bandwidth de memória na fase decode (output). Output é 3-6x mais caro que input porque é sequencial e compute-intensivo. Em 2026, um engenheiro usando agentes AI full-time pode gastar $50-200/mês em tokens — equivalente a uma assinatura de SaaS premium. Sem entender essa economia, é impossível otimizar, e sem otimizar, o custo escala sem controle.

Um engenheiro abre o painel de billing na sexta-feira e encontra uma fatura de $25 só daquele dia — e não faz ideia de onde veio. Ele rodou um agente de coding a tarde inteira, fez algumas perguntas, pediu uns refactors. Não sentiu nada de anormal. Mas os números não mentem: dezenas de chamadas, cada uma relendo o histórico inteiro da conversa, cada uma gerando um pedaço de resposta. A fatura é a soma de decisões invisíveis — quantos tokens entraram, quantos saíram, quantas vezes o mesmo contexto foi reprocessado. Sem entender *como* esse custo se acumula, a reação natural é ou pânico ("vou parar de usar agentes") ou resignação ("é o preço de fazer negócio"). Nenhuma das duas resolve o problema, porque nenhuma explica a mecânica por trás do número.

## O que é

A **economia de [[Dicionário de IA#Token|tokens]]** é a disciplina de entender, medir, prever e otimizar o gasto de tokens em workflows com [[Dicionário de IA#LLM (Large Language Model)|LLMs]]. É a interseção de três áreas:

1. **Engenharia** — como a arquitetura do prompt/contexto afeta consumo
2. **Finanças** — como tokens se traduzem em custo real
3. **Performance** — como o consumo de tokens afeta velocidade e qualidade

## Por que importa

Sem controle de tokens:

- Uma sessão de 1h com um [[Dicionário de IA#Agent|agente]] pode custar $5-25 sem que você perceba
- Um agente rodando em CI/CD 24/7 pode gerar faturas de $1000+/mês
- 70% dos tokens gastos podem ser desperdício (contexto irrelevante, retries, verbosidade)

## Como funciona

### De onde vem o custo

```mermaid
graph TD
    A[Você envia um prompt] --> B[Tokens de input processados<br>fase prefill — compute-bound]
    B --> C[Modelo gera resposta<br>fase decode — memory-bound]
    C --> D["Custo = input × preço_input<br>+ output × preço_output"]
```

| Fase                     | Recurso consumido    | Por que custa                                                 |
| ------------------------ | -------------------- | ------------------------------------------------------------- |
| **Input (prefill)**      | GPU compute (FLOPs)  | Processar N tokens pela rede neural inteira                   |
| **Output (decode)**      | GPU memory bandwidth | Cada token é gerado sequencialmente, 1 forward pass por token |
| **Reasoning (thinking)** | GPU memory bandwidth | Tokens internos de raciocínio, cobrados como output           |

### A assimetria input/output

Output é 3-6x mais caro que input porque:

- Cada token de output requer um forward pass completo pelo modelo
- A geração é **sequencial** (autoregressive) — não pode ser paralelizada
- O [[Dicionário de IA#KV cache|KV cache]] cresce com cada token gerado, consumindo mais memória

| Provider/Modelo   | Input $/MTok | Output $/MTok | Ratio |
| ----------------- | ------------ | ------------- | ----- |
| Claude Sonnet 4.6 | $3.00        | $15.00        | 5x    |
| GPT-5.4           | $2.50        | $15.00        | 6x    |
| Claude Opus 4.6   | $5.00        | $25.00        | 5x    |
| Gemini Flash      | $0.50        | $3.00         | 6x    |
| GPT-4.1 Nano      | $0.10        | $0.40         | 4x    |

### Os cinco vilões do consumo de tokens

| Vilão                    | % típico do gasto | Descrição                                              |
| ------------------------ | ----------------- | ------------------------------------------------------ |
| **Contexto acumulado**   | 30-40%            | Histórico que cresce a cada turn do agente             |
| **[[Dicionário de IA#tool definition\|Tool definitions]]**     | 5-15%             | Schemas JSON de ferramentas reenviados em cada chamada |
| **Respostas verbosas**   | 10-20%            | Modelo gera mais texto do que necessário               |
| **Retries e erros**      | 10-25%            | Agente erra, tenta de novo, paga dobrado               |
| **Contexto irrelevante** | 10-20%            | Arquivos inteiros no prompt quando 20 linhas bastavam  |

### Cenário real: custo de um dia de trabalho

Engenheiro usando Claude Sonnet 4.6 com agente de coding (8h):

| Fase do dia              | Calls  | Input médio | Output médio | Custo      |
| ------------------------ | ------ | ----------- | ------------ | ---------- |
| Manhã: 3 features        | 30     | 50k         | 15k          | $11.25     |
| Tarde: debugging         | 20     | 30k         | 5k           | $3.30      |
| Tarde: refactoring       | 15     | 80k         | 20k          | $8.10      |
| Code review              | 5      | 100k        | 10k          | $2.25      |
| **Total sem otimização** | **70** | —           | —            | **$24.90** |
| **Total com otimização** | **70** | —           | —            | **~$8-12** |

A diferença de 2-3x vem de: [[Dicionário de IA#Prompt caching|prompt caching]], context pruning, model routing, e respostas concisas.

## A regra de Pareto dos tokens

> **80% da economia vem de 3 técnicas:**
>
> 1. [[Dicionário de IA#Prompt caching|Prompt caching]] (tokens estáticos não reprocessados)
> 2. Context pruning (remover o irrelevante)
> 3. Model routing (usar budget model quando possível)

## Armadilhas

> [!warning] "Tokens são baratos"
> Individualmente sim — frações de centavo por chamada. Mas em volume de agente (dezenas de chamadas por hora, cada uma relendo o contexto acumulado) essas frações somam rápido. É o mesmo erro de julgamento que subestima juros compostos: o problema não é o valor unitário, é a repetição.

> [!warning] "Otimizar tokens degrada qualidade"
> Falso — e geralmente o oposto. Remover contexto irrelevante MELHORA a qualidade da resposta (menos ruído pro modelo filtrar) e reduz custo ao mesmo tempo. Não existe trade-off aqui; existe preguiça de podar o prompt.

> [!warning] "Não preciso monitorar"
> Sem métricas, otimizar tokens é adivinhação. Você não sabe se o vilão é contexto acumulado, retries ou respostas verbosas até medir — e cada vilão pede uma correção diferente.

> [!warning] Focar só em input
> Output é de 3 a 6x mais caro que input (ver tabela de assimetria acima). Um modelo verboso que gera 10k tokens quando 2k bastariam está desperdiçando muito mais no output do que qualquer economia feita cortando o prompt de entrada.

## O que vem a seguir

Saber que existe um custo — e que ele nasce da assimetria input/output e dos cinco vilões do consumo — ainda não diz **quanto** cada parte da conversa pesa na fatura. Um agente moderno não gasta tokens só em "o que você digitou" e "o que ele respondeu": existe também o *reasoning* interno (tokens de raciocínio, cobrados como output, mas invisíveis na resposta final) e o *cache* (que muda drasticamente o preço efetivo do mesmo token). A próxima nota, [[02 - Anatomia do gasto — input, output e reasoning]], abre essa caixa-preta e decompõe exatamente onde cada dólar da fatura foi parar.

## Veja também

- [[02 - Anatomia do gasto — input, output e reasoning]] — decomposição detalhada
- [[04 - Monitoramento — ccusage, Langfuse, dashboards]] — como medir
- [[05 - Prompt caching na prática]] — a primeira otimização a implementar

## Referências

- **Anthropic** — *Pricing* (2026). Tabela oficial de preços por modelo, incluindo prompt caching (cache write/read) e batch processing. [claude.com/pricing](https://claude.com/pricing)
- **Artificial Analysis** — *Anthropic: Intelligence, Performance & Price Analysis* (2026). Comparativo independente de custo por tarefa entre modelos Claude e concorrentes. [artificialanalysis.ai/providers/anthropic](https://artificialanalysis.ai/providers/anthropic)
