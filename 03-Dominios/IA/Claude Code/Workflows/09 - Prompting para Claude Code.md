---
title: "Prompting para Claude Code — comunicar tarefas com precisão"
type: concept
publish: true
created: 2026-05-13
updated: 2026-05-13
status: seedling
tags:
  - claude-code
  - workflows
  - prompting
  - comunicacao
  - precisao
---

# Prompting para Claude Code — comunicar tarefas com precisão

> [!abstract] TL;DR
> Prompts vagos produzem implementações que "funcionam" mas não fazem o que você queria. A diferença entre um prompt eficaz e um ineficaz está em especificar: o que você sabe (contexto relevante), o que você quer (comportamento esperado), e o que não quer (restrições). O agente toma decisões para preencher lacunas — sua job é minimizar as lacunas.

## O que o agente faz com um prompt

Quando você dá uma instrução ao Claude Code, o agente:

1. Lê o CLAUDE.md para entender o contexto do projeto
2. Examina os arquivos relevantes para entender o estado atual
3. Interpreta sua instrução dentro desse contexto
4. **Preenche todas as lacunas com suas próprias decisões**

O passo 4 é onde os problemas acontecem. Quanto mais vago o prompt, mais decisões o agente toma sozinho — e mais chance de divergir do que você queria.

## O princípio do "porquê antes do como"

A diferença mais importante em prompting para agentes:

```
❌ Como: "Use um Map em vez de um objeto para esse cache"

✓ Por que: "Esse cache precisa preservar a ordem de inserção
           e ter deleção O(1). Escolha a estrutura de dados
           mais adequada para isso."
```

Quando você especifica o "como", o agente implementa mecanicamente.
Quando você especifica o "porquê", o agente entende o objetivo e pode:
- Identificar que sua solução proposta não resolve o problema
- Sugerir uma abordagem melhor
- Fazer a implementação correta mesmo em edge cases não especificados

## Quatro elementos de um prompt eficaz

### 1. Contexto relevante

O que o agente precisa saber que não está óbvio no código:

```
"O endpoint POST /api/orders está lento em produção.
Temos ~10k pedidos por dia, pico de 50 req/s às 12h.
O banco tem índice em orders.customer_id mas não em orders.created_at."
```

### 2. Comportamento esperado

O que "pronto" significa em termos observáveis:

```
"Após a mudança, o endpoint deve responder em <100ms para
95% das requisições. Os testes existentes em
tests/routes/orders.test.ts devem continuar passando."
```

### 3. Restrições explícitas

O que não pode mudar, mesmo que faça sentido mudar:

```
"Não altere a interface pública do endpoint (path, método, payload).
Não use cache em memória — não temos Redis em produção.
As queries devem continuar funcionando com PostgreSQL 13."
```

### 4. Arquivos relevantes

Para onde olhar (e para onde não olhar):

```
"Foco em: src/routes/orders.ts, src/services/orders.ts,
src/db/queries/orders.ts

Não mexa em: src/middlewares/, src/config/"
```

## Exemplos contrastados

### Vago vs. Preciso

```
❌ Vago:
"Melhore a performance do serviço de orders"

✓ Preciso:
"O método OrderService.findByCustomer() está demorando >500ms
quando o cliente tem mais de 100 pedidos. A query SQL está em
src/db/queries/orders.ts linha 34. O problema parece ser
N+1: fazemos uma query por item de cada pedido.

Corrija usando JOIN ou batch query. Os testes em
tests/services/orders.test.ts devem passar.
Não altere a assinatura de findByCustomer()."
```

### Feature request

```
❌ Vago:
"Adicione autenticação no endpoint de admin"

✓ Preciso:
"O endpoint GET /api/admin/reports (src/routes/admin.ts linha 23)
não tem autenticação. Adicione o middleware requireAdmin que está
em src/middlewares/auth.ts. O middleware verifica o header
Authorization: Bearer <token> e checa se o usuário tem role 'admin'
em nossa tabela users.

Escreva um teste em tests/routes/admin.test.ts que verifica:
1. Request sem header retorna 401
2. Request com token de usuário normal retorna 403
3. Request com token de admin retorna 200"
```

## Prompts para exploração

Quando você genuinamente não sabe o que quer, diga isso explicitamente:

```
"Não sei como implementar rate limiting na nossa API.
Tenho opções: middleware em Express, Redis, serviço dedicado.
Qual faz mais sentido dado nosso stack (Node.js, Postgres, sem Redis)?
Não implemente ainda — só me explique as opções com trade-offs."
```

Pedir análise antes de implementação é válido — e mais eficiente do que receber uma implementação que você vai rejeitar.

## Tamanho do prompt

Prompts mais longos não são sempre melhores. O que importa é a relação sinal/ruído:

**Alto sinal:** contexto que muda a decisão do agente
**Ruído:** contexto que o agente ignoraria de qualquer forma

```
❌ Ruído:
"Este é um projeto de e-commerce desenvolvido por nossa equipe.
Usamos boas práticas de desenvolvimento e prezamos pela qualidade..."

✓ Sinal:
"Projeto Node.js/TypeScript com Express + Postgres.
Convenções em CLAUDE.md. Testes com Jest em tests/."
```

## Iteração vs. reescrita

Quando o agente entrega algo errado, a tentação é reescrever tudo. Mas geralmente é mais eficiente:

```
"O resultado está quase certo, mas:
1. Você usou console.log em vez de logger (src/utils/logger.ts)
2. O erro em linha 45 deveria ser AppError, não Error genérico
3. O teste não cobre o caso de orderId inválido

Corrija só esses 3 pontos. O resto está certo."
```

Prompt de correção específico é mais rápido do que refazer tudo — e preserva o que estava bom.

## Prompts de diagnóstico

Para entender o que o agente entendeu:

```
"Antes de implementar, explique em 3 bullet points como você
vai resolver o problema. Não escreva código ainda."
```

Se a explicação estiver errada, corrija antes de gastar tokens na implementação.

## Armadilhas

**"Faça o melhor possível"**: sem critério de sucesso, o agente define o próprio critério — que pode não ser o seu.

**Prompt que descreve a solução, não o problema**: se você descreve a solução, o agente implementa a solução descrita, mesmo que haja uma melhor. Descreva o problema.

**Restrições implícitas**: se você assume que o agente vai preservar um comportamento existente, mas não disse isso, ele pode refatorar de forma que quebra o comportamento.

**Contexto demais sem relevância**: um prompt com 500 linhas de contexto irrelevante é tão ruim quanto sem contexto — o agente vai ponderar tudo igualmente.

## Veja também

- [[03-Dominios/IA/Claude Code/Workflows/01 - Plan Mode|01 - Plan Mode]] — Plan Mode para confirmar entendimento antes de executar
- [[03-Dominios/IA/Claude Code/Workflows/04 - Debugging complexo|04 - Debugging complexo]] — descrever comportamento observado vs. esperado
- [[03-Dominios/IA/Claude Code/Mental Model/08 - Como o agente decide|08 - Como o agente decide]] — como o agente preenche lacunas
- [[03-Dominios/IA/Claude Code/Configuração/02 - CLAUDE.md anatomia|02 - CLAUDE.md anatomia]] — contexto permanente que reduz repetição de prompts
- [[03-Dominios/IA/Claude Code/Workflows/index|Workflows]] — índice do galho
