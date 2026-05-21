---
title: "CLAUDE.md — anatomia e o que colocar em cada seção"
type: concept
publish: true
created: 2026-05-13
updated: 2026-05-13
status: seedling
tags:
  - claude-code
  - configuracao
  - claude-md
---

# CLAUDE.md — anatomia e o que colocar em cada seção

> [!abstract] TL;DR
> CLAUDE.md é o documento de onboarding do agente para o seu projeto — equivalente ao que você explicaria para um dev sênior que acabou de entrar no time. Tem estrutura recomendada em 6 seções: visão geral, arquitetura, stack, convenções, comandos e o que evitar. A regra de ouro: se você precisaria explicar para um novo dev, coloque no CLAUDE.md.

## O que é

CLAUDE.md é um arquivo Markdown lido no início de cada sessão do Claude Code. É a única forma de dar contexto persistente ao agente sobre o seu projeto — sem ele, o agente age com suposições genéricas.

**Por que importa:** o agente não tem memória entre sessões. O CLAUDE.md é a memória externa — o que você coloca lá, o agente sabe em toda sessão nova.

## Estrutura recomendada

### Seção 1: Visão geral do projeto

O que é o projeto em 2-3 frases. O agente usa isso para entender contexto antes de agir.

```markdown
## Projeto

API REST de gestão de pedidos para e-commerce B2B. Serve ~50 clientes corporativos.
Multi-tenant: cada cliente tem schema separado no PostgreSQL.
```

### Seção 2: Arquitetura

Onde as coisas importantes ficam e como se relacionam. Não precisa ser exaustivo — só o suficiente para o agente navegar sem exploração desnecessária.

```markdown
## Arquitetura

- `src/api/` — rotas Express (um arquivo por domínio)
- `src/services/` — lógica de negócio (injetada nas rotas)
- `src/db/` — queries com node-postgres (sem ORM)
- `src/middleware/` — auth, rate limiting, logging
- `tests/` — jest, um arquivo de teste por service
```

### Seção 3: Stack e dependências

O que está instalado e como usar. Evita que o agente instale uma lib que já existe ou use a errada.

```markdown
## Stack

- Node 20, TypeScript 5, Express 4
- PostgreSQL 15 com node-postgres (pg)
- Redis para cache e sessões (ioredis)
- Jest + supertest para testes
- Logger: winston em `src/utils/logger.ts` — use `logger.info/warn/error`, não `console.*`
```

### Seção 4: Convenções de código

O que o time decidiu que não está explícito no código. Sem isso, o agente adivinha.

```markdown
## Convenções

- Erros de negócio usam `AppError` de `src/errors/AppError.ts` (não throw Error diretamente)
- Queries SQL ficam em `src/db/queries/[domínio].ts`, não inline nos services
- Nomes de arquivos: kebab-case. Nomes de classes: PascalCase
- Toda rota nova precisa de teste de integração cobrindo happy path e 401
- Commits: conventional commits (`feat:`, `fix:`, `refactor:`)
```

### Seção 5: Comandos de desenvolvimento

Os comandos que o agente vai precisar rodar com frequência. Com eles documentados, o agente não precisa explorar o package.json toda vez.

```markdown
## Comandos

- `npm test` — rodar toda a suite
- `npm test -- --testPathPattern=auth` — rodar testes de um módulo
- `npm run lint` — ESLint
- `npm run build` — compilar TypeScript
- `npm run db:migrate` — rodar migrations pendentes
- `docker-compose up -d` — iniciar Postgres + Redis localmente
```

### Seção 6: O que evitar / restrições

Guardrails em linguagem natural — o que o agente não deve fazer, mesmo que tecnicamente possível. Esta seção previne muitos erros.

```markdown
## Restrições

- Nunca use `any` em TypeScript — use `unknown` e faça type guard
- Não modifique arquivos em `src/db/migrations/` — use `npm run db:migrate:create`
- Não instale novas dependências sem perguntar — avaliar impacto no bundle
- Não faça push direto na branch main
- Não use `console.log` — use o logger
```

## O que NÃO colocar no CLAUDE.md

**Documentação técnica detalhada**: o agente lê o código, não precisa de explicação linha a linha.

**Listas exaustivas de todos os arquivos**: mencione só os arquivos-chave. Para o resto, o agente navega.

**Instruções que já estão no código**: se o código fala por si, não repita em prosa.

**Conteúdo que muda frequentemente**: o CLAUDE.md deve ser estável. Se muda toda semana, vai estar desatualizado na metade das sessões.

## Tamanho ideal

**Menos é mais.** Um CLAUDE.md de 100 linhas bem escritas é melhor que 500 linhas com ruído. O agente lê tudo — contexto desnecessário polui o contexto útil.

Regra prática: se você não precisaria explicar para um dev experiente que acabou de entrar no projeto, provavelmente não precisa estar no CLAUDE.md.

## CLAUDE.md como documento vivo

O CLAUDE.md deve evoluir com o projeto. Bom momento para atualizar:
- Quando uma nova lib é adotada
- Quando uma convenção muda
- Quando o agente toma uma decisão errada por falta de contexto (esse é o sinal mais claro)

## Armadilhas

**CLAUDE.md vazio**: o agente vai fazer suposições genéricas sobre stack, convenções e estrutura. O custo de 30 minutos escrevendo um bom CLAUDE.md é recuperado na primeira sessão.

**Regras sem contexto**: "não use X" sem explicar por quê é frágil. Com o por quê, o agente entende quando a regra se aplica e quando é edge case.

**Desatualizado**: um CLAUDE.md que diz "usamos Mongoose" quando o projeto migrou para Prisma há 3 meses ativamente confunde o agente. Revise quando a stack mudar.

## Veja também

- [[03-Dominios/IA/Claude Code/Configuração/01 - Hierarquia de configuração|01 - Hierarquia de configuração]] — onde o CLAUDE.md se encaixa
- [[03-Dominios/IA/Claude Code/Configuração/03 - CLAUDE.md receitas|03 - CLAUDE.md receitas]] — templates por stack
- [[03-Dominios/IA/Claude Code/Mental Model/08 - Como o agente decide|08 - Como o agente decide]] — como CLAUDE.md influencia decisões
- [[03-Dominios/IA/Claude Code/Configuração/index|Configuração]] — índice do galho

## Referências

- [Claude Code — CLAUDE.md](https://docs.anthropic.com/pt/docs/claude-code/memory)
