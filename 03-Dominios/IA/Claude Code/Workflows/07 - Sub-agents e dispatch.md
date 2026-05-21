---
title: "Sub-agents e dispatch — delegar tarefas"
type: concept
publish: true
created: 2026-05-13
updated: 2026-05-13
status: seedling
tags:
  - claude-code
  - workflows
  - sub-agents
  - dispatch
  - paralelismo
---

# Sub-agents e dispatch — delegar tarefas

> [!abstract] TL;DR
> Claude Code pode usar sub-agents para executar tarefas em paralelo com contexto isolado. Em vez de uma sessão longa acumulando contexto de múltiplas tarefas, você despacha agentes especializados: cada um recebe o contexto mínimo para sua tarefa, executa, e retorna o resultado. O benefício principal não é velocidade — é qualidade: agente com contexto limpo toma decisões melhores.

## O problema de contexto acumulado

Numa sessão longa sem sub-agents:

```
Tarefa A: implementar payment service
→ contexto: 50 mensagens sobre payment

Tarefa B (mesma sessão): implementar notification service
→ contexto: 50 mensagens sobre payment + 30 sobre notificações

Tarefa C: implementar order service
→ contexto: 80 mensagens sobre coisas não relacionadas a orders
```

O agente começa a confundir conceitos entre tarefas, aplica padrões da tarefa A na tarefa C, e toma decisões piores por excesso de contexto irrelevante.

## Como sub-agents funcionam

O agente principal (orquestrador) define a tarefa e o contexto necessário. O sub-agent recebe:
- Contexto específico da tarefa (arquivos relevantes, convenções)
- Escopo claro (o que fazer, o que não fazer)
- Critérios de sucesso (como saber que está pronto)

O sub-agent executa em contexto limpo, sem a história da sessão principal.

## Dispatch via Task tool

Claude Code expõe o `Task` tool para despachar sub-agents programaticamente:

```
"Use o Task tool para criar um sub-agent que vai implementar
o serviço de notificações em src/services/notifications.ts.

Contexto para o sub-agent:
- Leia src/services/orders.ts para entender o padrão de serviço
- Leia src/utils/mailer.ts para o client de email existente
- Convenções: use logger em vez de console.log, AppError para erros

Tarefa: implementar sendOrderConfirmation(orderId: string) e
sendCancellationEmail(orderId: string, reason: string).

Critério de sucesso: testes em tests/services/notifications.test.ts
passando."
```

## Dispatch em modo headless

Para automação e pipelines CI/CD, sub-agents podem ser despachados via CLI:

```bash
# Despachar sub-agent para tarefa específica
claude --print "implementa o serviço X conforme especificado em docs/spec.md" \
       --allowedTools "Read,Edit,Write,Bash(npm test)"

# Com output estruturado
claude --print "analise src/services/ e liste todos os endpoints sem autenticação" \
       --output-format json
```

## Padrão orquestrador/sub-agent

### Orquestrador define o plano

```
"Temos 3 tarefas independentes para implementar. Vou criar um
sub-agent para cada uma, já que não compartilham arquivos:

1. PaymentService (src/services/payment.ts)
2. NotificationService (src/services/notifications.ts)
3. ReportService (src/services/reports.ts)

Crie o sub-agent para PaymentService primeiro. Depois vou criar
os outros quando esse terminar."
```

### Sub-agent recebe contexto cirúrgico

O orquestrador não passa "tudo" — passa só o que o sub-agent precisa:

```
"Sub-agent para PaymentService:

Arquivos relevantes:
- src/interfaces/payment.ts (tipos existentes)
- src/config/stripe.ts (client configurado)
- tests/services/payment.test.ts (testes já escritos — faça passar)

NÃO mexa em:
- src/services/orders.ts
- src/routes/ (outro sub-agent cuida)

Implementação: src/services/payment.ts conforme interfaces em
src/interfaces/payment.ts. Use o Stripe client de src/config/stripe.ts."
```

## Quando usar sub-agents

**Use para tarefas que:**
- São independentes (não tocam os mesmos arquivos)
- Têm escopo bem definido (você consegue descrever em 3-5 linhas)
- Se beneficiam de contexto limpo (sem histórico de outras features)

**Não use para tarefas que:**
- Dependem de decisões de outra tarefa em andamento
- Precisam de contexto compartilhado (ex: migração que depende de schema)
- São explorações abertas sem critério de sucesso claro

## Context isolation como feature, não limitação

O fato de o sub-agent não ter acesso à história da sessão principal é intencional:

```
Sessão principal: 2h de debate sobre arquitetura
→ Sub-agent para implementar: recebe só a decisão final, não o debate
→ Implementa sem bias das opções descartadas
→ Resultado mais limpo
```

Se você quer que o sub-agent saiba algo, passe explicitamente. Se não passou, ele não vai "descobrir" por acidente — isso é um recurso.

## Revisão do resultado

Depois que o sub-agent completa:

```
"O sub-agent completou a implementação de PaymentService.
Revise src/services/payment.ts e confirme:
1. Segue o padrão de serviço de src/services/orders.ts
2. Usa AppError para erros de negócio
3. Os testes em tests/services/payment.test.ts passam

Se houver problemas, liste-os com arquivo:linha."
```

## Armadilhas

**Contexto insuficiente no dispatch**: se você despacha um sub-agent sem explicar as convenções do projeto, ele vai usar seus próprios padrões. Inclua sempre: padrão de arquivos similares, onde ficam os testes, convenções de erro.

**Tarefas dependentes em paralelo**: dois sub-agents que modificam o mesmo arquivo causam conflito. Mapeie dependências antes de despachar em paralelo.

**Sub-agent sem critério de sucesso**: "implemente o serviço de notificações" sem especificar o que "pronto" significa resulta em implementação que pode ou não atender ao que você precisa.

**Despachar tudo como sub-agent**: sub-agents têm overhead de contexto e dispatch. Para tarefas pequenas (uma função, um bug simples), a sessão principal é mais eficiente.

## Veja também

- [[03-Dominios/IA/Claude Code/Workflows/08 - Multi-agent|08 - Multi-agent]] — coordenar múltiplos agentes
- [[03-Dominios/IA/Claude Code/Workflows/06 - Sessões paralelas|06 - Sessões paralelas]] — worktrees para paralelismo de agentes
- [[03-Dominios/IA/Claude Code/Workflows/10 - Gestão de contexto|10 - Gestão de contexto]] — por que contexto limpo importa
- [[03-Dominios/IA/Claude Code/Time e Automação/index|Time e Automação]] — sub-agents em pipelines de time
- [[03-Dominios/IA/Claude Code/Workflows/index|Workflows]] — índice do galho
