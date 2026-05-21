---
title: "Refactoring pesado — mudanças grandes sem perder controle"
type: concept
publish: true
created: 2026-05-13
updated: 2026-05-13
status: seedling
tags:
  - claude-code
  - workflows
  - refactoring
  - context-management
---

# Refactoring pesado — mudanças grandes sem perder controle

> [!abstract] TL;DR
> Refactoring pesado com Claude Code requer 3 precauções: cobertura de testes antes de começar, atomização das mudanças em commits pequenos, e gestão ativa do contexto (sessões longas acumulam confusão). O padrão: Plan Mode para mapear o escopo, TDD como rede de segurança, commits frequentes para pontos de retorno.

## O problema de refactors grandes

Sem estrutura, um refactor grande com Claude Code tende a:

- Fazer muitas mudanças ao mesmo tempo, tornando o diff incompreensível
- Perder o contexto da intenção original à medida que a sessão cresce
- Quebrar comportamento existente sem um teste avisando
- Resultar num estado intermediário que não funciona nem compila

## Pré-condição: cobertura de testes

Antes de começar qualquer refactor significativo, verifique a cobertura:

```
"Rode npm test -- --coverage e me mostre a cobertura de
src/services/orders.ts. Precisamos ter pelo menos 70% de cobertura
nos comportamentos críticos antes de refatorar."
```

Se a cobertura for insuficiente:

```
"Antes de refatorar, escreva testes para os comportamentos
principais de OrderService: criação de pedido, cálculo de total
com desconto, e cancelamento com estorno. Cubra o happy path
e os casos de erro mais críticos."
```

## Padrão de execução

### 1. Plan Mode para mapear o escopo

```
Shift+Tab →
"Quero refatorar src/services/orders.ts (450 linhas) para:
- Extrair lógica de cálculo de preços para src/services/pricing.ts
- Extrair lógica de notificações para src/services/notifications.ts
- Deixar OrderService responsável apenas por orquestração

Antes de começar, faça um plano com:
- Quais funções vão para cada arquivo
- Qual a ordem de extração (o que extrair primeiro)
- Quais testes precisamos verificar em cada etapa"
```

### 2. Atomize em commits pequenos

Em vez de "refatore tudo de uma vez":

```
"Vamos fazer um passo de cada vez, commitando depois de cada extração.

Passo 1: extraia apenas as funções calculateTotal(), applyDiscount()
e calculateTax() para src/services/pricing.ts. Rode os testes,
confirme que passam, e commite como 'refactor: extract pricing logic'."
```

Depois que o commit for feito:

```
"Passo 2: extraia sendOrderConfirmation(), sendCancellationEmail()
para src/services/notifications.ts..."
```

Cada commit é um ponto de retorno. Se algo der errado, `git revert` volta ao estado anterior sem desfazer todo o trabalho.

### 3. Verificação contínua

Depois de cada extração:

```
"Rode npm test. Se houver falhas, mostre o erro completo antes
de tentar corrigir — preciso saber se é problema de import,
assinatura de função ou comportamento diferente."
```

## Strangler fig para mudanças de arquitetura

Para mudanças mais profundas (ex: migrar de callbacks para async/await, trocar ORM), use o padrão strangler fig: faça o novo coexistir com o velho e migre incrementalmente.

```
"Vamos migrar OrderRepository de callbacks para Promises.
Estratégia: duplicar cada método com versão Promise, marcar
o callback como @deprecated, depois remover.

Comece com findById(). Crie findByIdAsync() ao lado do findById()
existente. Atualize os callers de findById em OrderService para
usar a versão async. Confirme com os testes que o comportamento
é idêntico."
```

## Gestão de contexto em refactors longos

Refactors longos são onde o contexto do agente mais se degrada. Estratégias:

**Commit e /compact periodicamente:**
```
"Commitamos a extração de PricingService. Vou fazer /compact
antes de continuar para o próximo passo."
```

**Restate a intenção ao retomar:**
```
"Retomando o refactor de OrderService. Já extraímos:
- PricingService (commit abc123)
- NotificationService (commit def456)

Próximo passo: extrair ValidationService das funções
validateOrderItems() e validateCustomerLimit()."
```

**Sessões novas para fases distintas:**
Para refactors muito grandes (>1 dia de trabalho), considere uma sessão por fase. O CLAUDE.md do projeto orienta cada sessão nova.

## O que NÃO fazer

**"Refatore o serviço inteiro"**: sem atomização, o agente faz mudanças demais e torna impossível revisar o que mudou.

**Começar sem testes**: sem cobertura, você só descobre que quebrou algo quando vai pra produção.

**Misturar refactor com feature**: "refatore OrderService E adicione suporte a cupom de desconto" — não. Refactor primeiro, feature depois. O diff fica incompreensível.

**Deixar o contexto degradar**: sessões de refactor longas acumulam confusão. /compact + restate da situação atual previne decisões erradas por contexto poluído.

## Veja também

- [[03-Dominios/IA/Claude Code/Workflows/01 - Plan Mode|01 - Plan Mode]] — mapear o escopo antes de começar
- [[03-Dominios/IA/Claude Code/Workflows/02 - TDD com Claude Code|02 - TDD com Claude Code]] — cobertura como rede de segurança
- [[03-Dominios/IA/Claude Code/Workflows/10 - Gestão de contexto|10 - Gestão de contexto]] — manter qualidade em sessões longas
- [[03-Dominios/IA/Claude Code/Mental Model/06 - Compaction|06 - Compaction]] — como /compact funciona
- [[03-Dominios/IA/Claude Code/Workflows/index|Workflows]] — índice do galho
