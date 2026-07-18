---
title: "Migrations"
type: concept
fase: Magus
tags:
  - go
  - persistencia
  - database
  - migrations
  - sql
  - postgres
  - deploy
publish: true
created: 2026-07-18
updated: 2026-07-18
---

# Migrations

> [!abstract] TL;DR
> **Migration** é um arquivo `.sql` (ou uma função Go) que descreve uma mudança incremental no schema do banco — "criar tabela X", "adicionar coluna Y" — junto com o comando inverso para desfazer. Go não tem um ORM "oficial" com migrations embutidas (como o Entity Framework do .NET ou o Django do Python); o ecossistema resolveu isso com ferramentas dedicadas e independentes de framework. As duas dominantes são **golang-migrate** (CLI + biblioteca, o mais próximo de um Flyway em Go: arquivos numerados `NNNNNN_nome.up.sql` / `.down.sql`, versão do schema rastreada numa tabela `schema_migrations`) e **goose** (mesma ideia, mas migrations podem ser Go puro além de SQL, úteis quando a mudança precisa de lógica que SQL não expressa). Ambas resolvem o mesmo problema real: como levar o schema do banco de produção do estado A para o estado B, de forma repetível, versionada e auditável — sem alguém rodando `ALTER TABLE` manualmente via psql às três da manhã.

## O problema que motiva migrations

Imagine o cenário sem nenhuma ferramenta: o time decide adicionar uma coluna `email_verified boolean` na tabela `users`. Alguém escreve o `ALTER TABLE` e roda direto no banco de staging. Funciona. Semana seguinte, outra pessoa esquece de rodar o mesmo comando em produção, e o deploy quebra em runtime com `column "email_verified" does not exist` — um erro que só aparece quando o código novo já está rodando contra o schema velho.

Pior: como alguém, três meses depois, sabe **exatamente** que sequência de `ALTER TABLE` levou o banco de um ambiente novo (vazio) até o estado atual? Sem registro, a resposta vira arqueologia — vasculhar histórico de Slack, perguntar para quem "lembra".

Migrations resolvem isso transformando cada mudança de schema em um **arquivo versionado no repositório**, com duas propriedades:

1. **Sequência ordenada** — cada migration tem um número ou timestamp que define a ordem de aplicação. O schema de qualquer ambiente é sempre "a soma de todas as migrations aplicadas até aqui, em ordem".
2. **Reversibilidade declarada** — cada migration `up` (aplicar) tem um par `down` (desfazer), então voltar um passo é tão mecânico quanto avançar um.

O banco passa a guardar, numa tabela de controle própria, **qual foi a última migration aplicada**. Rodar as ferramentas de novo, num ambiente já atualizado, não faz nada — elas comparam o estado do banco com os arquivos disponíveis e aplicam só o que falta. Isso é o que torna migrations seguras de rodar repetidamente em CI/CD, inclusive em pipelines que fazem deploy várias vezes ao dia.

```mermaid
flowchart LR
    A["schema vazio"] -->|"0001_create_users.up.sql"| B["users existe"]
    B -->|"0002_add_email_verified.up.sql"| C["users + email_verified"]
    C -->|"0003_create_orders.up.sql"| D["users + orders"]

    D -.->|"0003_create_orders.down.sql"| C
    C -.->|"0002_add_email_verified.down.sql"| B
    B -.->|"0001_create_users.down.sql"| A

    style A fill:#999,color:#fff
    style D fill:#4A90D9,color:#fff
```

Cada seta sólida é `up`; cada seta pontilhada é o `down` correspondente, disponível caso algo precise voltar atrás. A tabela `schema_migrations` no banco guarda um único número: em qual ponto dessa linha o ambiente está agora.

## golang-migrate: o CLI, equivalente a um Flyway em Go

[golang-migrate](https://github.com/golang-migrate/migrate) é a ferramenta mais próxima, em espírito, do Flyway (Java) ou do Alembic (Python): arquivos SQL puros, numerados, aplicados em ordem, com uma tabela de controle de versão. Não tenta ser um ORM — só resolve migração de schema, e resolve bem, com drivers para Postgres, MySQL, SQLite, MongoDB e mais de uma dezena de bancos.

### Instalação e estrutura de arquivos

```bash
# Instala o binário CLI
go install -tags 'postgres' github.com/golang-migrate/migrate/v4/cmd/migrate@latest

# Cria o par up/down para uma nova migration
migrate create -ext sql -dir db/migrations -seq create_users_table
```

O comando `create` gera dois arquivos vazios, prontos para editar:

```
db/migrations/
├── 000001_create_users_table.up.sql
└── 000001_create_users_table.down.sql
```

A flag `-seq` usa números sequenciais (`000001`, `000002`, ...); sem ela, golang-migrate usa timestamp Unix — útil em times grandes, onde duas pessoas criando migrations no mesmo dia poderiam colidir no número sequencial se trabalharem em branches paralelas.

```sql
-- 000001_create_users_table.up.sql
CREATE TABLE users (
    id         BIGSERIAL PRIMARY KEY,
    email      TEXT NOT NULL UNIQUE,
    created_at TIMESTAMPTZ NOT NULL DEFAULT now()
);
```

```sql
-- 000001_create_users_table.down.sql
DROP TABLE users;
```

O par existe porque schema é um caminho de mão dupla: `up` leva o banco adiante, `down` desfaz exatamente essa mudança — nunca "desfaz tudo", só o passo correspondente.

### Rodando via CLI

```bash
export DATABASE_URL="postgres://user:pass@localhost:5432/mydb?sslmode=disable"

# Aplica todas as migrations pendentes
migrate -database "$DATABASE_URL" -path db/migrations up

# Desfaz a última migration aplicada
migrate -database "$DATABASE_URL" -path db/migrations down 1

# Mostra a versão atual do schema
migrate -database "$DATABASE_URL" -path db/migrations version
```

`up` sem argumento aplica **todas** as migrations pendentes, em ordem. `down 1` desfaz só a última. golang-migrate consulta a tabela `schema_migrations` para saber onde parou — se o banco já está na versão 3 e existem migrations até a 5, só a 4 e a 5 rodam.

### Rodando programaticamente (biblioteca, não só CLI)

golang-migrate também é uma biblioteca Go — útil quando o deploy quer rodar migrations como parte do próprio binário da aplicação, sem depender de um CLI externo no pipeline:

```go
package main

import (
    "log"

    "github.com/golang-migrate/migrate/v4"
    _ "github.com/golang-migrate/migrate/v4/database/postgres"
    _ "github.com/golang-migrate/migrate/v4/source/file"
)

func runMigrations(databaseURL string) error {
    m, err := migrate.New(
        "file://db/migrations",
        databaseURL,
    )
    if err != nil {
        return err
    }
    defer m.Close()

    if err := m.Up(); err != nil && err != migrate.ErrNoChange {
        return err
    }
    return nil
}

func main() {
    if err := runMigrations("postgres://user:pass@localhost:5432/mydb?sslmode=disable"); err != nil {
        log.Fatal(err)
    }
    log.Println("migrations aplicadas")
}
```

> [!info] Blank imports (`_`) carregam drivers por efeito colateral
> `_ "github.com/golang-migrate/migrate/v4/database/postgres"` e `_ "github.com/golang-migrate/migrate/v4/source/file"` não expõem nenhum símbolo usado diretamente — o import existe só para rodar o `init()` de cada pacote, que se registra internamente (padrão idêntico ao `database/sql` com drivers, visto na [[01 - database-sql — o contrato|nota 01]] deste galho). Sem esses imports, `migrate.New` falha em runtime com `unknown driver`, mesmo compilando sem erro.

`err != migrate.ErrNoChange` é o detalhe que evita tratar "não havia nada pendente" como falha — rodar `m.Up()` num banco já atualizado retorna esse erro sentinela, e é o comportamento esperado, não uma exceção.

## goose: migrations programáticas, SQL ou Go puro

[goose](https://github.com/pressly/goose) resolve o mesmo problema com uma diferença central: além de arquivos `.sql`, uma migration pode ser uma **função Go** — útil quando a mudança precisa de lógica que SQL puro não expressa bem, como recalcular um campo derivado linha a linha, ou migrar dados de um formato JSON antigo para colunas novas.

### Migration em SQL (formato goose)

```bash
goose -dir db/migrations create add_email_verified sql
```

Diferente de golang-migrate (dois arquivos), goose usa **um arquivo só**, com marcadores de comentário separando `up` e `down`:

```sql
-- +goose Up
-- +goose StatementBegin
ALTER TABLE users ADD COLUMN email_verified BOOLEAN NOT NULL DEFAULT false;
-- +goose StatementEnd

-- +goose Down
-- +goose StatementBegin
ALTER TABLE users DROP COLUMN email_verified;
-- +goose StatementEnd
```

Os comentários `-- +goose Up` / `-- +goose Down` são a sintaxe que o parser do goose reconhece; `StatementBegin`/`StatementEnd` só é necessário quando a instrução SQL contém `;` internos (funções PL/pgSQL, por exemplo) que, sem essa marcação, seriam interpretados como fim de statement pelo parser simples do goose.

### Migration em Go puro

Aqui está a diferença real de goose frente a golang-migrate — quando SQL não basta:

```go
package migrations

import (
    "context"
    "database/sql"

    "github.com/pressly/goose/v3"
)

func init() {
    goose.AddMigrationContext(upBackfillEmailVerified, downBackfillEmailVerified)
}

func upBackfillEmailVerified(ctx context.Context, tx *sql.Tx) error {
    // Lógica que SQL puro não expressa bem: por exemplo,
    // consultar um serviço externo de verificação por lote
    // não é o caso real aqui, mas ilustra o motivo de existir
    // migration em Go — processamento condicional linha a linha.
    _, err := tx.ExecContext(ctx, `
        UPDATE users SET email_verified = true
        WHERE email LIKE '%@empresa-verificada.com'
    `)
    return err
}

func downBackfillEmailVerified(ctx context.Context, tx *sql.Tx) error {
    _, err := tx.ExecContext(ctx, `
        UPDATE users SET email_verified = false
        WHERE email LIKE '%@empresa-verificada.com'
    `)
    return err
}
```

> [!info] `AddMigrationContext` recebe `*sql.Tx` — a migration roda dentro de transação por padrão
> goose executa cada migration Go dentro de uma transação (quando o driver do banco suporta DDL transacional — Postgres suporta, MySQL não totalmente). Isso significa que a assinatura das funções de migration já recebe `tx *sql.Tx`, não `db *sql.DB` — o mesmo contrato `database/sql` da [[01 - database-sql — o contrato|nota 01]], só que já dentro do escopo transacional que o goose abre e fecha por você.

### Rodando goose

```bash
export GOOSE_DRIVER=postgres
export GOOSE_DBSTRING="postgres://user:pass@localhost:5432/mydb?sslmode=disable"

goose -dir db/migrations up      # aplica pendentes
goose -dir db/migrations down    # desfaz a última
goose -dir db/migrations status  # lista aplicadas vs pendentes
```

E programaticamente, para embutir no binário de deploy (mesma motivação de golang-migrate embutido):

```go
package main

import (
    "database/sql"
    "log"

    "github.com/pressly/goose/v3"
    _ "github.com/pressly/goose/v3" // já importado acima; drivers vêm do database/sql
    _ "github.com/lib/pq"
)

func runMigrations(db *sql.DB) error {
    if err := goose.SetDialect("postgres"); err != nil {
        return err
    }
    return goose.Up(db, "db/migrations")
}

func main() {
    db, err := sql.Open("postgres", "postgres://user:pass@localhost:5432/mydb?sslmode=disable")
    if err != nil {
        log.Fatal(err)
    }
    defer db.Close()

    if err := runMigrations(db); err != nil {
        log.Fatal(err)
    }
    log.Println("migrations aplicadas")
}
```

Repare que goose, ao contrário de golang-migrate, recebe um `*sql.DB` já aberto — ele se integra ao pool de conexões da [[02 - Connection pool|nota 02]] em vez de abrir a própria conexão isolada, o que facilita reaproveitar a mesma configuração de pool (`SetMaxOpenConns` etc.) tanto para a aplicação quanto para as migrations.

## golang-migrate vs goose: quando escolher qual

| | golang-migrate | goose |
|---|---|---|
| Formato de migration | SQL puro (dois arquivos, `.up`/`.down`) | SQL (um arquivo, marcadores) **ou** função Go |
| Migration com lógica condicional | não — só SQL | sim — Go puro quando SQL não basta |
| Bancos suportados | Postgres, MySQL, SQLite, MongoDB, Cassandra, e mais de uma dezena | Postgres, MySQL, SQLite, ClickHouse, Vertica |
| Uso típico | times que só precisam de DDL versionado, sem lógica extra | times com backfills complexos ou transformação de dados na migration |
| Analogia | mais próximo do Flyway (Java) | mais próximo do Alembic (Python), que também mistura SQL e código |

Não é uma escolha ideológica — os dois resolvem o problema central igualmente bem. golang-migrate tende a vencer quando o time quer o modelo mais simples possível (arquivo SQL, nada mais); goose tende a vencer quando alguma migration, cedo ou tarde, vai precisar de lógica que SQL sozinho não escreve de forma limpa.

## Rodando migrations no deploy

A pergunta prática depois de escolher a ferramenta: **quando**, no pipeline de deploy, as migrations rodam? Três padrões comuns, cada um com um trade-off diferente:

```mermaid
sequenceDiagram
    participant CI as Pipeline CI/CD
    participant DB as Banco de dados
    participant App as Aplicação (novo binário)

    rect rgb(230, 240, 255)
    Note over CI,App: Padrão A — migration como step separado, antes do deploy
    CI->>DB: migrate up (step dedicado)
    DB-->>CI: schema atualizado
    CI->>App: deploy do binário novo
    end
```

**Padrão A — step dedicado no CI/CD, antes do deploy.** O pipeline roda `migrate -database $DATABASE_URL -path db/migrations up` (ou `goose up`) como um passo isolado, e só prossegue para o deploy do binário se esse passo for bem-sucedido. É o padrão mais comum e mais seguro: se a migration falhar, o deploy nunca acontece, e o binário antigo continua rodando contra o schema antigo — consistente.

**Padrão B — a aplicação roda as próprias migrations no boot**, via `runMigrations()` chamado em `main()` antes de subir o servidor HTTP (os exemplos programáticos acima fazem exatamente isso). Simples de operar — não precisa de step separado no pipeline — mas perigoso em produção com múltiplas réplicas: se três pods sobem ao mesmo tempo, três processos tentam rodar a mesma migration simultaneamente. golang-migrate e goose usam locks no banco (`pg_advisory_lock` no Postgres) para serializar isso, mas ainda assim é um padrão melhor reservado para ambientes de instância única ou dev local.

**Padrão C — migration desacoplada do deploy do código**, rodada manualmente ou por um job dedicado antes de qualquer deploy que dependa dela. É o padrão exigido quando a mudança de schema precisa ser **backward-compatible** por um período — por exemplo, adicionar uma coluna nova sem quebrar o binário antigo que ainda não a conhece, e só remover uma coluna velha numa migration *seguinte*, depois que todos os pods já rodam o código novo. Esse tipo de migration em duas fases (expandir, depois contrair) é o que evita o cenário de abertura desta nota — deploy quebrando por schema fora de sincronia — em sistemas com deploy contínuo e múltiplas réplicas.

> [!warning] Migration destrutiva (`DROP COLUMN`, `DROP TABLE`) e zero-downtime não combinam sem cuidado
> Se o binário antigo ainda está servindo tráfego (deploy gradual, canary, múltiplas réplicas em rolling update) e a migration remove uma coluna que esse binário antigo ainda lê, o resultado é erro em produção — não porque a migration estava errada, mas porque ela rodou cedo demais em relação ao rollout do código. A prática segura: nunca remover uma coluna na mesma migration que remove o código que a usa; espaçar em pelo menos um deploy de diferença.

> [!warning] Rodar migrations manualmente em produção quebra o rastro
> É tentador, num incidente, conectar via `psql` e rodar o `ALTER TABLE` na mão para "resolver logo". Isso desalinha a tabela `schema_migrations` do estado real do banco — a próxima vez que a ferramenta rodar, ela pode tentar reaplicar (erro de "coluna já existe") ou, pior, achar que uma migration mais recente já foi aplicada quando não foi. Se uma correção emergencial for inevitável, registre-a como uma migration nova assim que possível, para o histórico do repositório continuar sendo a fonte de verdade.

> [!warning] Migration irreversível na prática, mesmo com `down.sql` escrito
> `DROP TABLE users` como `up` e `CREATE TABLE users (...)` como `down` "desfaz" a estrutura, mas não os **dados** que estavam na tabela — esses se foram. `down` restaura schema, não estado. Para migrations destrutivas de dados reais, backup antes de aplicar em produção não é opcional.

## Lente cross-stack

Quem chega em Go vindo de outro stack de backend já conhece o problema — só muda a ferramenta:

| Stack | Ferramenta típica | Formato |
|---|---|---|
| Java/Spring | Flyway ou Liquibase | SQL versionado (Flyway) ou XML/YAML declarativo (Liquibase) |
| Python/Django | migrations do próprio Django ORM | Python gerado automaticamente a partir de mudanças no model |
| Python/SQLAlchemy | Alembic | Python, com autogeração de diff a partir dos models |
| Node/Prisma | Prisma Migrate | SQL gerado a partir do schema declarativo `.prisma` |
| Node/Knex | Knex migrations | JavaScript/TypeScript, `up`/`down` como funções |
| Go | golang-migrate ou goose | SQL puro (ambas) ou Go puro (só goose) |

A diferença mais marcante para quem vem de Django ou Prisma: essas ferramentas **geram** a migration automaticamente comparando o model declarado com o schema atual. golang-migrate e goose não fazem isso — você escreve o SQL (ou o Go) à mão, migration por migration. É consistente com a filosofia geral de Go de preferir explícito a mágico (o mesmo espírito por trás de `database/sql` exigir mapeamento manual, visto na [[03 - Query, Scan e o mapeamento manual|nota 03]]) — o trade-off é mais digitação, em troca de nunca haver um "diff automático" que interprete errado uma intenção ambígua do model.

## Como explicar em inglês

> In Go, schema migrations are handled by standalone tools rather than an ORM's built-in migration engine — the two dominant ones are **golang-migrate**, which stores each change as a pair of SQL files (`NNNNNN_name.up.sql` and `.down.sql`) and tracks the applied version in a `schema_migrations` table, and **goose**, which supports the same SQL-file pattern but also lets a migration be a plain Go function when the change needs logic SQL can't express — a data backfill, for instance. Both are idempotent: running `up` against an already-current database is a no-op, which is what makes them safe to invoke from a CI/CD pipeline on every deploy. The operational question that matters most isn't which tool to pick — it's *when* migrations run relative to the code deploy: as a separate pipeline step before the new binary ships (safest), on application boot (simplest, but risky with multiple replicas racing the same migration), or decoupled entirely for destructive changes that need an expand-then-contract rollout to stay backward-compatible with the old binary still serving traffic.

| Termo PT | Termo EN |
|---|---|
| migração de schema | schema migration |
| migração para frente / aplicar | migrate up |
| migração para trás / desfazer | migrate down |
| tabela de controle de versão | version tracking table |
| arquivo de migration | migration file |
| migração reversível | reversible migration |
| mudança de schema retrocompatível | backward-compatible schema change |
| expandir e depois contrair | expand-and-contract |
| preenchimento retroativo de dados | data backfill |

## O que vem a seguir

Migrations resolvem a evolução do **schema** — a estrutura das tabelas. A próxima nota trata de um problema adjacente, mas distinto: como garantir que várias operações sobre os **dados** aconteçam de forma atômica, e como estruturar o código de acesso a dados para que transações não vazem lógica de banco por todo o domínio da aplicação. A [[08 - Transações e o padrão repository|nota 08]] fecha o galho com transações (`BeginTx`, commit/rollback) e o padrão repository que embrulha esse controle numa interface coesa.

## Veja também

- [[01 - database-sql — o contrato|01 — database/sql — o contrato]] — o mesmo padrão de blank import por driver, e `*sql.Tx` como base do que goose usa internamente
- [[02 - Connection pool|02 — Connection pool]] — o `*sql.DB` que goose reutiliza ao rodar migrations programaticamente
- [[03 - Query, Scan e o mapeamento manual|03 — Query, Scan e o mapeamento manual]] — o mesmo espírito "explícito, não mágico" que explica por que migrations não são autogeradas em Go
- [[08 - Transações e o padrão repository|08 — Transações e o padrão repository]] — próxima nota do galho
- [[03-Dominios/Tecnologia/Go/index|Trilha Go]]

## Fontes

- golang-migrate. *migrate — Database migrations written in Go*. GitHub. https://github.com/golang-migrate/migrate (acessado em 2026-07-18)
- golang-migrate. *CLI usage*. GitHub. https://github.com/golang-migrate/migrate/blob/master/cmd/migrate/README.md (acessado em 2026-07-18)
- pressly/goose. *goose — Database migration tool*. GitHub. https://github.com/pressly/goose (acessado em 2026-07-18)
- The Go Authors. *The Go Blog — Go database/sql tutorial references*. go.dev. https://go.dev/doc/tutorial/database-access (acessado em 2026-07-18)
- pkg.go.dev. *database/sql package documentation*. pkg.go.dev. https://pkg.go.dev/database/sql (acessado em 2026-07-18)
