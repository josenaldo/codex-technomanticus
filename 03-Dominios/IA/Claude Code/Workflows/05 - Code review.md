---
title: "Code review com Claude Code"
type: concept
publish: true
created: 2026-05-13
updated: 2026-05-13
status: seedling
tags:
  - claude-code
  - workflows
  - code-review
  - qualidade
---

# Code review com Claude Code

> [!abstract] TL;DR
> Claude Code pode fazer code review de três formas: revisar o diff atual (staged changes), revisar um arquivo específico, ou revisar um PR inteiro via `gh pr diff`. O review é mais útil quando você especifica os critérios — sem critérios, o agente lista observações genéricas de estilo. Com critérios específicos, encontra bugs reais e violações das convenções do projeto.

## Review do diff atual

O caso mais comum: antes de fazer o commit, revisar o que está em staging.

```
"Revise o diff em staging (git diff --staged) como se fosse
aprovar ou reprovar este PR.

Avalie especificamente:
1. Bugs óbvios e edge cases não tratados
2. Violações das convenções definidas no CLAUDE.md
3. Testes ausentes para comportamentos adicionados
4. Código que vai funcionar mas vai ser difícil de manter

Para cada issue: arquivo:linha, severidade (critical/warning/suggestion),
e o que deveria ser diferente.

Não liste issues de formatação — o linter cuida disso."
```

## Review de arquivo específico

Para revisão mais profunda de um arquivo antes de merge:

```
"Revise src/services/orders.ts com foco em:
1. Segurança: há algum input do usuário que chega sem validação
   até as queries SQL?
2. Performance: há queries N+1 ou loops que poderiam ser batch
   operations?
3. Cobertura: os testes em tests/services/orders.test.ts cobrem
   os casos de erro?"
```

## Review de PR via GitHub CLI

```bash
# Revisa o PR atual comparando com a branch base
gh pr diff | claude "revise este diff..."
```

Ou dentro do Claude Code:

```
"Execute gh pr diff e revise as mudanças do PR #123.
Verifique:
- Breaking changes na API pública
- Migrações de banco sem rollback
- Secrets ou credenciais hardcoded
- Performance regressions óbvias"
```

## Criteria-first review

O review mais eficaz especifica o que importa:

### Security review

```
"Faça um security review focado em OWASP Top 10.
Priorize:
1. SQL injection — há queries com concatenação de string?
2. Autenticação — há endpoints sem middleware de auth?
3. Autorização — um usuário pode acessar recursos de outro usuário?
4. Exposição de dados — há campos sensíveis no payload de resposta?

Ignora code style e qualidade geral — só segurança."
```

### Performance review

```
"Revise para problemas de performance:
1. Queries N+1: loop que faz query dentro de loop
2. Queries sem índice em colunas que filtram por user_id ou created_at
3. Payloads de response com campos desnecessários
4. Cache opportunity: dados que raramente mudam mas são consultados frequentemente

Para cada issue, estime o impacto (crítico/moderado/baixo) com base
no volume de requisições desta rota."
```

### Conventions review

```
"Revise para violações das convenções do projeto (CLAUDE.md):
1. console.log em vez de logger (src/utils/logger.ts)
2. AppError não sendo usado para erros de negócio
3. Queries SQL inline em vez de em src/db/queries/
4. TypeScript 'any' em vez de tipos explícitos

Lista com arquivo:linha para cada violação."
```

## Review antes de abrir PR (checklist)

Um slash command útil para este padrão — `.claude/commands/pr-check.md`:

```markdown
Revise as mudanças em staging/branch como checklist de PR:

- [ ] npm test — todos passando?
- [ ] Sem console.log ou código de debug
- [ ] Sem credenciais hardcoded
- [ ] Convenções do CLAUDE.md seguidas
- [ ] Testes para o que foi adicionado
- [ ] Breaking changes documentados?
- [ ] Migration tem rollback?

Veredito: APROVADO / COM RESSALVAS / REPROVADO + justificativa.
```

Uso: `/pr-check`

## Incorporando feedback do review

Depois do review, para resolver issues em lote:

```
"O review encontrou 3 issues críticos e 2 warnings:

Critical:
1. orders.ts:87 — query SQL com concatenação, risco de injection
2. orders.ts:134 — endpoint sem validação de ownership

Warning:
3. orders.ts:156 — N+1 query no loop de items
4. orders.ts:201 — console.log esquecido

Corrija os 2 critical primeiro. Para cada: mostre o before/after
e explique o fix."
```

## Armadilhas

**"Revise meu código"** sem critérios: o agente produz uma lista genérica de melhorias de estilo, complexidade ciclomática e nomes de variáveis. Útil como primeiro passo, inútil como substituto de code review real.

**Review de diff muito grande**: um diff com 1000 linhas de mudança vai receber um review superficial — o agente perde detalhes. Para PRs grandes, divida em revisões por módulo.

**Aceitar cada sugestão sem avaliar**: o agente pode sugerir refactors desnecessários durante o review. Avalie o impacto de cada sugestão antes de aplicar.

**Review sem contexto do domínio**: "é mais eficiente usar `reduce`" pode ser true em performance mas falso em legibilidade para o time. Sua expertise de domínio > sugestão do agente.

## Veja também

- [[03-Dominios/IA/Claude Code/Workflows/06 - Sessões paralelas|06 - Sessões paralelas]] — review em branch isolada
- [[03-Dominios/IA/Claude Code/Configuração/06 - Slash commands customizados|06 - Slash commands customizados]] — criar /pr-check
- [[03-Dominios/IA/Claude Code/Workflows/09 - Prompting para Claude Code|09 - Prompting para Claude Code]] — especificidade nos critérios de review
- [[03-Dominios/IA/Claude Code/Workflows/index|Workflows]] — índice do galho
