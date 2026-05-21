---
title: "Plan Mode — planejar antes de agir"
type: concept
publish: true
created: 2026-05-13
updated: 2026-05-13
status: seedling
tags:
  - claude-code
  - workflows
  - plan-mode
  - prompting
---

# Plan Mode — planejar antes de agir

> [!abstract] TL;DR
> Plan Mode faz o agente produzir um plano de implementação antes de escrever qualquer código. Ative com `Shift+Tab` ou `--plan`. O plano expõe o raciocínio do agente — você aprova, corrige ou redireciona antes de o agente agir. Para tarefas com mais de 3 arquivos envolvidos, Plan Mode quase sempre economiza iterações.

## O que é

Em modo normal, o agente age: recebe a tarefa, raciocina internamente, executa tool calls. O raciocínio é invisível.

Em Plan Mode, o agente para antes de agir e exibe o plano:
- quais arquivos vai ler
- quais mudanças planeja
- qual a ordem de execução
- quais suposições está fazendo

Você vê o raciocínio e pode corrigir antes de o agente modificar qualquer arquivo.

## Como ativar

**Interativo — teclado:**
```
Shift+Tab    → ativa Plan Mode para o próximo prompt
```

**Interativo — no prompt:**
```
/plan <tarefa>
```

**Headless:**
```bash
claude --plan "adicione autenticação JWT ao middleware"
```

**Forçar pela CLI:**
```bash
claude -p "adicione autenticação JWT" --plan
```

## Exemplo de uso

```
você: Shift+Tab, então:
"Adicione rate limiting ao endpoint POST /api/orders.
Limite: 10 requisições por minuto por IP.
Retorne 429 com Retry-After header quando exceder."

agente (Plan Mode):
Plano de implementação:

1. Ler src/middleware/ para entender o padrão existente de middleware
2. Ler src/routes/orders.ts para ver como o endpoint é definido
3. Verificar se há uma lib de rate limiting instalada (package.json)

Mudanças planejadas:
- Criar src/middleware/rateLimiter.ts com lógica de sliding window
- Modificar src/routes/orders.ts para usar o middleware no POST /api/orders
- Criar tests/middleware/rateLimiter.test.ts

Suposição: se não houver lib de rate limiting, instalar express-rate-limit.
Pergunta: o armazenamento do rate limit deve ser em memória (simples) ou
Redis (persiste entre restarts)?

Aprove para continuar ou corrija o plano.
```

Antes de escrever uma linha, você sabe o que vai mudar e pode responder à pergunta do agente.

## Quando usar

**Use Plan Mode quando:**
- A tarefa envolve mais de 2-3 arquivos
- Você não tem certeza de como o agente vai interpretar o pedido
- A tarefa é sensível (migração de banco, mudança de auth, refactor de interface pública)
- Sessão nova sem histórico do que foi feito antes

**Pode pular Plan Mode quando:**
- Correções triviais em um único arquivo
- Mudanças puramente mecânicas ("renomeie a variável X para Y em orders.ts")
- Você acabou de revisar o código manualmente e tem contexto completo

## Plan Mode vs. prompt detalhado

Plan Mode não substitui um bom prompt — complementa:

```
Ruim (Plan Mode não salva um prompt vago):
Shift+Tab → "melhore o código"

Bom (Plan Mode + prompt específico):
Shift+Tab → "extraia a lógica de cálculo de impostos de
src/services/orders.ts linhas 45-89 para um novo arquivo
src/services/taxCalculator.ts, mantendo a interface pública igual
para não quebrar os testes existentes"
```

## Corrigindo o plano

O valor do Plan Mode está em corrigir antes de executar:

```
agente: "Plano: modificar src/db/migrations/ para adicionar coluna..."

você: "Não modifique migrations manualmente. Use npm run db:migrate:create
      para gerar uma nova migration e depois preencha ela."

agente: "Entendido. Plano revisado: executar npm run db:migrate:create,
        depois editar o arquivo gerado..."
```

Uma correção no plano > horas de debug depois da implementação.

## Plan Mode em modo headless

Em automação, Plan Mode pode ser usado para inspecionar o que o agente faria antes de aprovar execução:

```bash
# Gera o plano, não executa
claude --plan "atualiza dependências desatualizadas" > plan.txt

# Revisar plan.txt manualmente, depois:
claude "atualiza dependências desatualizadas"
```

## Armadilhas

**Aprovar sem ler**: o valor do Plan Mode está em revisar o plano. Se você aprova automaticamente, está pagando o custo extra sem o benefício.

**Plan Mode para tarefas triviais**: `Shift+Tab → "corrija o typo na linha 42"` desperdiça tokens para gerar um plano para uma mudança óbvia.

**Não corrigir suposições erradas**: se o agente assume que você usa Jest mas você usa Vitest, corrija no plano. Deixar passar gera código errado que custa mais para consertar.

## Veja também

- [[03-Dominios/IA/Claude Code/Mental Model/05 - Modos de operação|05 - Modos de operação]] — Plan Mode no contexto dos 4 modos
- [[03-Dominios/IA/Claude Code/Mental Model/08 - Como o agente decide|08 - Como o agente decide]] — como o raciocínio molda decisões
- [[03-Dominios/IA/Claude Code/Workflows/09 - Prompting para Claude Code|09 - Prompting para Claude Code]] — como escrever prompts precisos
- [[03-Dominios/IA/Claude Code/Workflows/index|Workflows]] — índice do galho

## Referências

- [Claude Code — Plan Mode](https://docs.anthropic.com/pt/docs/claude-code/how-claude-code-thinks)
