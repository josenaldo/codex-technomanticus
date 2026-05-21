---
title: "CLAUDE.md compartilhado — o que vai no repo, o que fica local"
type: concept
publish: true
created: 2026-05-13
updated: 2026-05-13
status: seedling
tags:
  - claude-code
  - claude-md
  - time
  - configuracao
---

# CLAUDE.md compartilhado — o que vai no repo, o que fica local

> [!abstract] TL;DR
> CLAUDE.md no repo é contrato do projeto: diz ao agente quais são as convenções, proibições, e workflows que todo dev precisa seguir. O `~/.claude/CLAUDE.md` global é preferência pessoal: estilo individual, projetos pessoais, configurações que não fazem sentido para o time. A regra simples é: se todos no time deveriam seguir, vai no repo. Se só você segue, fica no seu global.

## A hierarquia de CLAUDE.md

Claude Code carrega CLAUDE.md em cascata, do mais específico ao mais geral:

```
~/.claude/CLAUDE.md          ← global, só você
<projeto>/.claude/CLAUDE.md  ← projeto (ou raiz do repo)
<subdiretório>/CLAUDE.md     ← subprojeto (módulo específico)
```

Cada nível herda do anterior e pode sobrescrever. Um CLAUDE.md na pasta `backend/` adiciona contexto específico ao backend sem precisar repetir o que está na raiz.

## O que vai no CLAUDE.md do repo

### Convenções do projeto

O que torna este projeto diferente de qualquer outro projeto TypeScript genérico:

```markdown
## Convenções

- Nomenclatura: camelCase para variáveis, PascalCase para componentes e tipos
- Estrutura: um componente por arquivo, testes em `__tests__/` ao lado do arquivo
- Imports: usar path aliases (@/components, @/utils) — nunca imports relativos com ../../
- Tratamento de erros: sempre usar Result<T, E> do utils/result.ts, nunca throw diretamente
```

### Arquitetura e módulos

O mapa que todo dev (humano ou agente) precisa antes de tocar o código:

```markdown
## Arquitetura

- `src/core/` — lógica de negócio pura, sem dependências externas
- `src/api/` — controllers HTTP, validação de input, serialização
- `src/infra/` — banco de dados, filas, email
- `src/shared/` — tipos compartilhados e utilitários

Regra: `core/` não importa de `api/` ou `infra/`. Dependência vai do externo para o centro.
```

### Comandos do projeto

Os comandos canônicos que o agente vai precisar rodar:

```markdown
## Comandos essenciais

- Build: `npm run build`
- Testes: `npm test` (unit), `npm run test:e2e` (integration)
- Dev server: `npm run dev` (porta 3000)
- Lint + typecheck: `npm run check`
- Migration: `npm run db:migrate`
```

### Restrições explícitas

O que o agente nunca deve fazer neste projeto:

```markdown
## Restrições

- Nunca modificar arquivos em `db/migrations/` diretamente — criar nova migration
- Nunca usar `any` em TypeScript — se necessário, documentar com comentário `// TODO: type this`
- Nunca commitar com `--no-verify` — os hooks existem por motivo
- Nunca apontar MCP servers para o banco de produção
```

### Catálogo de skills

```markdown
## Skills disponíveis

| Skill | Uso |
|-------|-----|
| `/tdd` | Desenvolvimento orientado a testes |
| `/convencoes` | Convenções deste projeto |
| `/review` | Checklist de code review |
| `/deploy-staging` | Checklist de deploy para staging |
```

## O que fica no `~/.claude/CLAUDE.md` global

Preferências que são suas, não do projeto:

```markdown
# Minhas preferências

## Estilo de resposta
- Respostas em português brasileiro
- Código com comentários mínimos — prefiro código autoexplicativo
- Sem introduções longas — vá direto ao ponto

## Meus atalhos
- Quando digo "revisa", quero code review completo com /review
- Quando digo "implementa", siga TDD com /tdd

## Projetos pessoais
- Meu setup preferido para projetos novos: Bun + Elysia + Drizzle
```

Isso não tem lugar no CLAUDE.md do repo — não é relevante para outros devs, e polui o contexto de todos.

## CLAUDE.md por subdiretório

Para projetos monorepo ou com módulos muito diferentes:

```
repo/
  CLAUDE.md              ← contexto geral do projeto
  backend/
    CLAUDE.md            ← Node.js, banco, API — contexto específico
  frontend/
    CLAUDE.md            ← React, componentes, testes E2E — contexto específico
  infra/
    CLAUDE.md            ← Terraform, provisionamento — contexto específico
```

O CLAUDE.md de `backend/` não precisa repetir as convenções gerais — só adiciona o que é específico para trabalhar no backend.

## Manter o CLAUDE.md atualizado

Um CLAUDE.md desatualizado é pior do que nenhum: instrui o agente a seguir práticas que o projeto abandonou.

**Triggers para atualizar:**

- Time adotou nova convenção → adicionar
- Time abandonou uma prática → remover (não comentar, não marcar como obsoleto)
- Novo MCP server configurado para o projeto → documentar
- Nova skill criada → adicionar ao catálogo
- Regra que o agente violou → adicionar nas restrições

**Ownership**: o CLAUDE.md do repo deve ter um responsável claro — geralmente o tech lead ou o engenheiro que introduziu Claude Code no time.

## Formato recomendado para CLAUDE.md de projeto

```markdown
# Contexto do projeto

[Uma ou duas frases descrevendo o que este projeto faz e qual stack usa]

## Arquitetura

[Mapa de módulos — o que cada pasta faz]

## Comandos essenciais

[Build, test, dev, migrate — o que o agente vai precisar]

## Convenções

[O que torna este projeto específico — nomenclatura, padrões]

## Restrições

[O que nunca fazer]

## Skills disponíveis

[Tabela com skills do projeto]

## MCP servers configurados

[Lista de servers ativos e o que cada um acessa]
```

Seja conciso. Um CLAUDE.md longo demais vira ruído — o agente dilui atenção sobre todo o conteúdo igualmente.

## Armadilhas

**Tudo no CLAUDE.md global**: se você documenta o projeto no `~/.claude/CLAUDE.md`, outro dev que clona o repo começa do zero. O contexto precisa estar versionado com o código.

**CLAUDE.md muito longo**: um arquivo com 500 linhas de convenções não vai ser lido completamente. Prefira skills para contexto extenso — o agente carrega skills sob demanda.

**Restrições sem motivo**: "nunca use X" sem explicação vira letra morta. "nunca use X — o módulo Y tem um workaround que precisa estar intacto" faz o agente entender o porquê e seguir a regra mesmo em edge cases.

**Documentar aspirações, não realidade**: se o time aspira a 100% de cobertura mas na prática merge PR com 60%, o CLAUDE.md não deve dizer "sempre escreva testes para 100% de cobertura". O agente vai seguir a instrução e criar conflito com PRs reais.

## Veja também

- [[03-Dominios/IA/Claude Code/Configuração/02 - CLAUDE.md anatomia|02 - CLAUDE.md anatomia]] — estrutura detalhada do arquivo
- [[03-Dominios/IA/Claude Code/Skills e MCP/08 - Skills em time|08 - Skills em time]] — catálogo de skills no repo
- [[03-Dominios/IA/Claude Code/Time e Automação/07 - Onboarding de time|07 - Onboarding de time]] — usar CLAUDE.md no processo de onboarding
- [[03-Dominios/IA/Claude Code/Time e Automação/index|Time e Automação]] — índice do galho
