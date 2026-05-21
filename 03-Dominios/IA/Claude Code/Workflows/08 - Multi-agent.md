---
title: "Multi-agent — coordenar múltiplos agentes"
type: concept
publish: true
created: 2026-05-13
updated: 2026-05-13
status: seedling
tags:
  - claude-code
  - workflows
  - multi-agent
  - orquestracao
  - paralelismo
---

# Multi-agent — coordenar múltiplos agentes

> [!abstract] TL;DR
> Multi-agent em Claude Code é o padrão de ter um agente orquestrador que define o plano e despacha sub-agents para executar partes independentes. O orquestrador não executa código — gerencia. Cada sub-agent executa em contexto limpo com escopo bem definido. O valor: tarefas em paralelo com contexto isolado, sem a degradação de uma sessão monolítica longa.

## Papéis no sistema multi-agent

### Orquestrador

Responsabilidades:
- Receber o objetivo de alto nível
- Decompor em tarefas independentes
- Definir o contexto mínimo de cada tarefa
- Despachar sub-agents
- Revisar e integrar os resultados
- Identificar dependências entre tarefas

O orquestrador não implementa. Ele planeja e coordena.

### Sub-agents

Responsabilidades:
- Executar uma tarefa específica com contexto fornecido
- Reportar resultado e problemas encontrados
- Não tomar decisões de arquitetura além do escopo recebido

Um sub-agent não sabe o que os outros sub-agents estão fazendo — e não deveria.

## Estrutura de um sistema multi-agent

```
Objetivo: "Implementar sistema de pagamentos"
         ↓
Orquestrador: decompõe em 4 tarefas
         ↓
┌──────────────┬──────────────┬──────────────┬──────────────┐
│  Sub-agent 1 │  Sub-agent 2 │  Sub-agent 3 │  Sub-agent 4 │
│  PaymentSvc  │  WebhookSvc  │  UI checkout │  Testes e2e  │
│  (paralelo)  │  (paralelo)  │  (paralelo)  │  (depende 1-3)│
└──────────────┴──────────────┴──────────────┴──────────────┘
         ↓
Orquestrador: revisa, integra, commita
```

## Decomposição efetiva pelo orquestrador

O primeiro trabalho do orquestrador é mapear dependências:

```
"Antes de despachar sub-agents, vou mapear as dependências:

Tarefa 1: PaymentService (src/services/payment.ts)
→ Depende de: src/config/stripe.ts (já existe)
→ Nenhuma tarefa depende dela para começar

Tarefa 2: WebhookService (src/services/webhooks.ts)
→ Depende de: PaymentService (precisa dos tipos de Payment)
→ Aguarda Tarefa 1 completar

Tarefa 3: UI de checkout (src/components/Checkout.tsx)
→ Depende de: tipos de Payment (src/interfaces/payment.ts)
→ Pode rodar em paralelo com Tarefa 1

Tarefa 4: Testes e2e (tests/e2e/payment.test.ts)
→ Depende de: Tarefas 1, 2, 3 completas

Plano: Despachar Tarefas 1 e 3 em paralelo.
Depois despachar Tarefa 2 quando 1 completar.
Despachar Tarefa 4 quando 2 e 3 completarem."
```

## Prompt de dispatch com contexto cirúrgico

O orquestrador prepara o contexto do sub-agent com precisão:

```
"Sub-agent para PaymentService:

OBJETIVO: Implementar src/services/payment.ts

CONTEXTO RELEVANTE:
- src/interfaces/payment.ts — tipos (já definidos, não altere)
- src/config/stripe.ts — Stripe client configurado
- src/services/orders.ts — exemplo do padrão de serviço a seguir
- src/utils/logger.ts — use este logger, nunca console.log
- src/utils/errors.ts — AppError para erros de negócio

TESTES: tests/services/payment.test.ts (já escritos, faça passar)

ESCOPO: apenas src/services/payment.ts
NÃO MEXA em: routes, interfaces, outros serviços

PRONTO QUANDO: todos os testes em tests/services/payment.test.ts passam"
```

## Coordenação de resultados

Depois que sub-agents completam:

```
"PaymentService e CheckoutUI completaram.
Agora revise os dois antes de despachar WebhookService:

1. src/services/payment.ts usa os tipos de src/interfaces/payment.ts
   corretamente? O WebhookService vai depender desses tipos.

2. src/components/Checkout.tsx consome a API do PaymentService
   da forma esperada? Se não, corrija antes de continuar.

Reporte: os outputs são compatíveis entre si?"
```

## Anti-padrões no multi-agent

### Orquestrador que implementa

```
❌ Errado:
"Enquanto espero o sub-agent do PaymentService,
vou implementar eu mesmo o WebhookService..."

✓ Correto:
"Enquanto espero o sub-agent do PaymentService,
vou revisar os requisitos do WebhookService e preparar
o contexto para o próximo dispatch."
```

### Sub-agent com escopo vago

```
❌ Errado:
"Implemente o sistema de pagamentos"

✓ Correto:
"Implemente src/services/payment.ts conforme os tipos em
src/interfaces/payment.ts. Faça passar tests/services/payment.test.ts.
Não mexa em outros arquivos."
```

### Sub-agents dependentes em paralelo

```
❌ Errado:
Despachar WebhookService em paralelo com PaymentService
quando WebhookService importa tipos de PaymentService.

✓ Correto:
Aguardar PaymentService completar.
Revisar os tipos exportados.
Então despachar WebhookService com esses tipos como contexto.
```

## Multi-agent com worktrees

Para isolamento máximo, cada sub-agent pode trabalhar em sua própria worktree:

```bash
# Orquestrador cria worktrees
git worktree add ../proj-payment feat/payment-service
git worktree add ../proj-checkout feat/checkout-ui

# Sub-agents rodam em worktrees separadas
# Terminal 1: cd ../proj-payment && claude (sub-agent para payment)
# Terminal 2: cd ../proj-checkout && claude (sub-agent para checkout)
```

Cada sub-agent tem arquivos completamente separados — sem conflito possível, mesmo editando arquivos adjacentes.

## Quando multi-agent faz sentido

**Faz sentido quando:**
- O objetivo tem ≥3 partes independentes que levam horas cada
- Você consegue definir critério de pronto para cada parte
- As partes têm interfaces bem definidas entre si
- O projeto tem boa cobertura de testes (sub-agents precisam saber quando terminaram)

**Não faz sentido quando:**
- A tarefa é pequena o suficiente para uma sessão
- As partes são profundamente interdependentes
- Você não sabe o suficiente para definir o escopo de cada sub-agent
- A arquitetura ainda está sendo decidida (decida antes de despachar)

## Veja também

- [[03-Dominios/IA/Claude Code/Workflows/07 - Sub-agents e dispatch|07 - Sub-agents e dispatch]] — como criar e instruir sub-agents
- [[03-Dominios/IA/Claude Code/Workflows/06 - Sessões paralelas|06 - Sessões paralelas]] — worktrees para isolamento físico
- [[03-Dominios/IA/Claude Code/Workflows/01 - Plan Mode|01 - Plan Mode]] — planejar a decomposição antes de despachar
- [[03-Dominios/IA/Claude Code/Time e Automação/index|Time e Automação]] — multi-agent em contexto de time
- [[03-Dominios/IA/Claude Code/Workflows/index|Workflows]] — índice do galho
