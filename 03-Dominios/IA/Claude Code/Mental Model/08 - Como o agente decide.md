---
title: "Como o agente decide — confiança, raciocínio, iteração"
type: concept
publish: true
created: 2026-05-13
updated: 2026-05-13
status: seedling
tags:
  - claude-code
  - mental-model
  - raciocinio
  - decisao
  - prompting
---

# Como o agente decide — confiança, raciocínio, iteração

> [!abstract] TL;DR
> Claude Code usa raciocínio antes de agir — mesmo quando você não vê. O system prompt, CLAUDE.md e o histórico da sessão moldam cada decisão. A qualidade do prompt afeta diretamente a qualidade das decisões: "adicione auth" gera uma decisão muito mais incerta que "adicione JWT auth ao middleware Express em src/middleware/auth.ts, seguindo o padrão de src/middleware/logger.ts". Explicar o *porquê* frequentemente produz resultados melhores que especificar o *como*.

## O que é

Cada tool call que Claude Code executa é precedida por raciocínio: o agente decide *o que fazer* antes de *fazer*. Esse processo usa:

1. **Contexto de sistema**: instruções built-in do Claude Code (como se comportar, quais tools usar, como pedir confirmação)
2. **CLAUDE.md**: suas instruções de projeto (convenções, restrições, preferências)
3. **Histórico da sessão**: o que foi dito e feito até agora
4. **A tarefa atual**: o que você pediu

O raciocínio não é sempre visível — em modo normal, você vê só a ação. Com Plan Mode ou `--verbose`, parte do raciocínio fica exposta.

## Decisão: clarificar vs proceder

O agente toma decisões sobre quando perguntar e quando agir:

| Situação | Comportamento típico |
|----------|---------------------|
| Tarefa clara com contexto suficiente | Age sem perguntar |
| Tarefa ambígua com múltiplas interpretações | Pergunta ou escolhe a mais conservadora |
| Ação irreversível (delete, push, drop table) | Pede confirmação explícita |
| CLAUDE.md proíbe explicitamente | Recusa e explica |

Em modo interativo, o agente pergunta. Em headless, tende a escolher a interpretação mais conservadora.

## O papel do CLAUDE.md nas decisões

O CLAUDE.md funciona como "instruções do tech lead" — moldando o comportamento do agente mais do que qualquer prompt individual.

**Exemplo: sem CLAUDE.md**

```
você: adicione tratamento de erro ao fetchUser

agente: [adiciona try/catch genérico com console.error]
```

**Com CLAUDE.md que diz "use o logger customizado em src/utils/logger.ts"**

```
você: adicione tratamento de erro ao fetchUser

agente: [adiciona try/catch usando logger.error com o formato padrão do projeto]
```

A mesma tarefa, resultado diferente porque o CLAUDE.md informou a decisão.

## Como melhorar a qualidade das decisões

### Especificidade > Generalidade

| Prompt vago | Prompt específico |
|-------------|-------------------|
| "adicione auth" | "adicione autenticação JWT ao middleware em src/middleware/auth.ts" |
| "melhore os testes" | "aumente cobertura de src/services/payment.ts para >80%, focando nos casos de erro" |
| "refatore isso" | "extraia a lógica de validação de src/controllers/users.ts para src/validators/users.ts" |

### Por que > Como

Explicar o objetivo produz decisões melhores que especificar cada passo:

```
Ruim (como): "edite src/cache.ts linha 47 para adicionar um timeout de 5000ms"

Melhor (por quê): "o Redis está causando timeouts em produção quando fica indisponível.
Adicione timeout de 5 segundos às conexões em src/cache.ts para que o serviço
degrade graciosamente em vez de travar."
```

Com o "por quê", o agente pode verificar se há outros pontos que precisam do mesmo fix, escolher a implementação certa, e adicionar um comentário explicativo.

### Plan Mode para verificar o raciocínio

```
Shift+Tab  → ativa plan mode
```

O plano gerado revela o raciocínio do agente: quais arquivos vai ler, que mudanças planeja. É um checkpoint para verificar se o agente entendeu o que você quer antes de executar.

## Incerteza e erros de decisão

O agente não é infalível. Decisões erradas comuns:

**Assumir convenções**: se o projeto não tem CLAUDE.md, o agente assume convenções genéricas que podem não se aplicar.

**Solução local**: corrige o sintoma imediato em vez do problema raiz. Causa: tarefa descreveu sintoma, não causa.

**Over-engineering**: adiciona mais do que pedido. Causa: instruções vagas permitem interpretação ampla.

**Under-engineering**: faz menos do que o esperado. Causa: tarefa ambígua, agente escolheu interpretação conservadora.

## Sinais de incerteza

O agente expressa incerteza de formas diferentes:
- Pergunta antes de agir (modo interativo)
- Adiciona comentários no código (`// Note: this assumes X`)
- Propõe alternativas ("Fiz X, mas Y poderia ser mais adequado se...")
- Status `DONE_WITH_CONCERNS` em workflows agenticos

Esses sinais são informação valiosa — não os ignore.

## Armadilhas

**Prompt de telefone quebrado**: "melhore o código" → agente faz mudanças de estilo → você diz "não era isso" → agente faz outra coisa. Cada iteração vaga desperdiça tokens e frustração. Invista 2 minutos num prompt preciso.

**Confiança implícita**: o agente não perguntará sobre tudo que não sabe. Se você não especificou o logger, ele escolheu um. Revise outputs, especialmente em sessões longas.

**Correções sem contexto**: "não era isso, tenta de novo" sem explicar o que estava errado é feedback ineficiente. Explique o que estava incorreto e por quê.

## Veja também

- [[03-Dominios/IA/Claude Code/Workflows/09 - Prompting para Claude Code|09 - Prompting para Claude Code]]
- [[03-Dominios/IA/Claude Code/Configuração/index|Configuração]] — CLAUDE.md e como moldar decisões
- [[03-Dominios/IA/Claude Code/Mental Model/01 - O loop agentic|01 - O loop agentic]]
- [[03-Dominios/IA/Claude Code/Mental Model/index|Mental Model]] — índice do galho

## Referências

- [Anthropic — Be clear and direct](https://docs.anthropic.com/pt/docs/build-with-claude/prompt-engineering/be-clear-and-direct)
