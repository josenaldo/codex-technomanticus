---
title: "CLAUDE.md — receitas para Node, Python, Go, monorepos"
type: concept
publish: true
created: 2026-05-13
updated: 2026-05-13
status: seedling
tags:
  - claude-code
  - configuracao
  - claude-md
  - receitas
---

# CLAUDE.md — receitas para Node, Python, Go, monorepos

> [!abstract] TL;DR
> Templates prontos de CLAUDE.md para os stacks mais comuns. Adapte copiando o template relevante e preenchendo os campos marcados com `[...]`. Cada receita cobre: visão geral, estrutura, stack, convenções e restrições. Um CLAUDE.md com 80% de preenchimento é infinitamente melhor que nenhum.

## Receita: Node.js / TypeScript

```markdown
## Projeto

[Nome]: [descrição em 1-2 frases. Contexto de negócio.]
[Tipo: API REST / GraphQL / CLI / fullstack Next.js / etc.]

## Arquitetura

- `src/` — código-fonte TypeScript
- `src/[routes|api|controllers]/` — entry points HTTP
- `src/services/` — lógica de negócio
- `src/[db|repositories]/` — acesso a dados
- `src/utils/` — utilitários compartilhados
- `tests/` — [jest / vitest], espelhando estrutura de src/

## Stack

- Node [versão], TypeScript [versão]
- [Framework: Express / Fastify / NestJS / Next.js]
- [ORM/DB: Prisma / TypeORM / node-postgres / Drizzle]
- [Testes: Jest / Vitest + [supertest / @testing-library]]
- Logger: [winston / pino] em `src/utils/logger.ts` — use `logger.info/warn/error`, não `console.*`

## Convenções

- Erros: [AppError / HttpException / custom class] em `src/errors/`
- Nomes de arquivos: [kebab-case / camelCase]
- Imports absolutos via `@/` mapeado para `src/`
- [Adicionar convenções do projeto]

## Comandos

- `npm test` — toda a suite
- `npm test -- --testPathPattern=[padrão]` — filtrar testes
- `npm run lint` — ESLint
- `npm run build` — compilar
- `npm run dev` — desenvolvimento local

## Restrições

- Não use `any` — prefira `unknown` com type guard
- Não instale dependências sem perguntar
- [Adicionar restrições específicas]
```

## Receita: Python

```markdown
## Projeto

[Nome]: [descrição em 1-2 frases.]
[Tipo: API FastAPI / Django / script / CLI / pacote]

## Arquitetura

- `[app|src]/` — código-fonte principal
- `[app|src]/[routers|views|controllers]/` — entry points
- `[app|src]/services/` — lógica de negócio
- `[app|src]/models/` — modelos de dados [SQLAlchemy / Pydantic / dataclasses]
- `tests/` — pytest, espelhando estrutura do app

## Stack

- Python [versão]
- [Framework: FastAPI / Django / Flask]
- [ORM/DB: SQLAlchemy / Django ORM / psycopg2]
- [Testes: pytest + [httpx / pytest-django]]
- [Gerenciador de pacotes: pip + requirements.txt / poetry / uv]
- [Linter/formatter: ruff / black + isort]

## Convenções

- Type hints obrigatórios em todas as funções públicas
- Schemas de validação: [Pydantic / marshmallow] em `[app]/schemas/`
- [Estilo de imports: absolutos / relativos]
- [Convenções específicas do projeto]

## Comandos

- `pytest` — toda a suite
- `pytest tests/[módulo]/ -v` — módulo específico
- `ruff check .` — lint
- `ruff format .` — formatação
- `[uvicorn app.main:app --reload / python manage.py runserver]` — dev

## Restrições

- Não use `type: ignore` sem comentário explicativo
- Não modifique migrations manualmente — use `alembic revision` / `manage.py makemigrations`
- [Adicionar restrições específicas]
```

## Receita: Go

```markdown
## Projeto

[Nome]: [descrição em 1-2 frases.]
[Tipo: API HTTP / CLI / serviço gRPC / biblioteca]

## Arquitetura

- `cmd/[nome]/` — entry point (main.go)
- `internal/` — código privado do projeto
- `internal/[handlers|transport]/` — HTTP handlers / gRPC
- `internal/service/` — lógica de negócio (interfaces + implementações)
- `internal/repository/` — acesso a dados
- `pkg/` — código exportável / bibliotecas internas
- `[nome]_test.go` — testes ao lado do código (convenção Go)

## Stack

- Go [versão]
- [Framework HTTP: net/http stdlib / chi / gin / echo]
- [DB: database/sql + pgx / GORM / sqlc]
- [Testes: stdlib testing + testify]
- [Logger: slog stdlib / zerolog / zap]

## Convenções

- Interfaces definidas onde são usadas (não onde são implementadas)
- Erros: retorno explícito, sem panic fora de init
- Nomes exportados: PascalCase. Internos: camelCase
- [Convenções específicas do projeto]

## Comandos

- `go test ./...` — toda a suite
- `go test ./internal/[pacote]/... -v` — pacote específico
- `go vet ./...` — análise estática
- `golangci-lint run` — lint (se instalado)
- `go build ./cmd/[nome]/` — compilar

## Restrições

- Não use `interface{}` / `any` sem necessidade forte
- Não ignore erros retornados — use `_` explicitamente quando intencional
- [Adicionar restrições específicas]
```

## Receita: Monorepo

```markdown
## Projeto

[Nome]: monorepo com [N] pacotes/apps.
[Contexto: quem são os consumidores, qual o domínio]

## Estrutura do monorepo

- `apps/` — aplicações deployáveis
  - `apps/api/` — [descrição]
  - `apps/web/` — [descrição]
- `packages/` — bibliotecas compartilhadas
  - `packages/shared/` — tipos e utilitários comuns
  - `packages/ui/` — componentes de UI

## Tooling de monorepo

- [Turborepo / Nx / Lerna / pnpm workspaces]
- Todos os comandos de build/test usam o runner do monorepo

## Convenções por workspace

- Cada `app/` e `package/` tem seu próprio `README.md` e testes
- Dependências entre pacotes: `"@[escopo]/[pacote]": "workspace:*"`
- [Convenções de naming de pacotes]

## Comandos

- `[turbo / nx] run test` — testes em todos os pacotes
- `[turbo / nx] run test --filter=[app]` — pacote específico
- `[turbo / nx] run build` — build de todos
- `[pnpm / npm] -w [comando]` — rodar na raiz

## Restrições

- Não importe de `apps/` para `packages/` — fluxo é unidirecional
- Alterações em `packages/shared` podem quebrar múltiplos consumers — testar todos
- [Restrições específicas do monorepo]
```

## Como adaptar as receitas

1. Copie o template relevante para `.claude/CLAUDE.md`
2. Substitua os `[campos]` com valores reais do projeto
3. Remova seções que não se aplicam
4. Adicione seções específicas que o template não cobre
5. Teste uma sessão — se o agente tomar uma decisão errada, adicione contexto

## Armadilhas

**Deixar campos `[...]` preenchidos**: um CLAUDE.md com placeholders confunde mais do que ajuda. Preencha ou remova.

**Copiar o template inteiro sem adaptar**: o template tem seções genéricas. Seu projeto tem particularidades — adicione-as.

**Não adicionar o `## Restrições`**: é a seção mais impactante. Sem ela, o agente vai tomar decisões que violam as convenções do time.

## Veja também

- [[03-Dominios/IA/Claude Code/Configuração/02 - CLAUDE.md anatomia|02 - CLAUDE.md anatomia]] — estrutura e princípios
- [[03-Dominios/IA/Claude Code/Configuração/04 - settings.json|04 - settings.json]] — configurações além do CLAUDE.md
- [[03-Dominios/IA/Claude Code/Configuração/index|Configuração]] — índice do galho
