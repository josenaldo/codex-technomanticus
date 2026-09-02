---
title: "sqlc — SQL type-safe por codegen"
type: concept
fase: adepto
tags:
  - go
  - persistencia
  - sql
  - codegen
  - sqlc
  - database-sql
publish: true
created: 2026-07-18
updated: 2026-07-18
---

# sqlc — SQL type-safe por codegen

> [!abstract] TL;DR
> **sqlc** lê seu schema SQL e suas queries SQL — arquivos `.sql` de verdade, não uma DSL Go — e **gera** structs e funções Go type-safe para cada uma: `GetUser(ctx, id) (User, error)`, com `User` já com os campos certos, nos tipos certos. Não há reflection em runtime, não há tag `db:"..."` pra manter sincronizada à mão — o mapeamento é feito **uma vez, em tempo de build**, comparando sua SQL contra o schema real do banco. Erro de coluna que não existe, ou tipo incompatível, vira erro de `sqlc generate`, não `panic` em produção às 3 da manhã. É o equivalente Go a escrever SQL puro e deixar o jOOQ (Java) ou o Prisma (Node) gerarem o client — só que sqlc não roda nada em runtime: o código gerado é Go comum, chamando `database/sql`/`pgx` como qualquer código que você escreveria manualmente.

## O problema que a nota anterior deixou em aberto

A [[03 - Query, Scan e o mapeamento manual|nota 03]] mostrou o mapeamento manual: escrever a query como string, chamar `Scan(&u.ID, &u.Name, &u.Email)`, e torcer para a ordem dos `&campo` bater com a ordem das colunas do `SELECT`. Funciona — mas cresce mal. Toda query nova repete o mesmo ritual: escrever a SQL, escrever o struct de destino, escrever o `Scan` com os ponteiros na ordem certa, e escrever o `if err := rows.Err(); err != nil` no fim do loop. Multiplique por trinta queries num serviço real e o boilerplate vira a maior parte do pacote de persistência.

Pior: nada nisso é verificado até rodar. Se você adicionar uma coluna nova no `SELECT` e esquecer de adicionar o `&campo` correspondente no `Scan`, o compilador não reclama — `Scan` recebe `...any`, então qualquer contagem de argumentos "compila". O erro só aparece em runtime, como `sql: expected 4 destination arguments in Scan, got 3` — na melhor das hipóteses; na pior, os campos batem em número mas ficam trocados de posição, e o bug é silencioso: `u.Email` recebe o valor de `u.Name` porque a ordem no `SELECT` mudou e ninguém reordenou o `Scan` junto.

sqlc ataca exatamente esse ponto: você continua escrevendo SQL — não uma DSL, não um builder fluente, SQL de verdade, no arquivo `.sql` — e uma ferramenta de linha de comando gera o código Go de mapeamento **a partir dessa SQL e do schema real**. O gerador sabe os tipos das colunas porque lê o `CREATE TABLE`; sabe quantos parâmetros a query espera porque faz parse da SQL. Column drift vira erro de `sqlc generate`, não de `Scan` em produção.

## O fluxo: schema + query → codegen → Go

```mermaid
flowchart LR
    classDef destaque fill:#FFAA0024,stroke:#FFAA00,color:#E9ECF2
    classDef neutro fill:#1B2029,stroke:#4E5666,color:#C6CCD8
    A["schema.sql\n(CREATE TABLE)"] --> D["sqlc generate"]
    B["query.sql\n(-- name: GetUser :one\nSELECT ...)"] --> D
    C["sqlc.yaml\n(config: engine, paths,\ndriver de saída)"] --> D
    D --> E["models.go\n(structs geradas)"]
    D --> F["<pacote>.sql.go\n(funções type-safe)"]
    E --> G["seu código Go\n(chama Queries.GetUser(ctx, id))"]
    F --> G
    G --> H["database/sql ou pgx\n(driver real, em runtime)"]

    class D destaque
    class G neutro
```

Três entradas, um comando, dois arquivos gerados:

- **`schema.sql`** — o DDL do seu banco: `CREATE TABLE users (id bigserial primary key, name text not null, email text not null, created_at timestamptz not null default now())`. sqlc lê isso para saber os tipos de cada coluna — é daqui que vem o mapeamento `text` → `string`, `bigserial` → `int64`, `timestamptz` → `time.Time`.
- **`query.sql`** — suas queries, cada uma anotada com um comentário especial que vira o nome da função gerada: `-- name: GetUser :one`. sqlc faz parse dessa SQL contra o schema para inferir os tipos dos parâmetros (`$1`, `$2`, ...) e das colunas retornadas.
- **`sqlc.yaml`** — a configuração: qual *engine* (`postgresql`, `mysql`, `sqlite`), onde ficam `schema.sql` e `query.sql`, para onde vai o código gerado, e qual pacote de driver o código gerado deve importar (`database/sql` ou, mais comum hoje, `pgx/v5`).

O comando `sqlc generate` roda **uma vez, em tempo de desenvolvimento** (ou no CI, como *check* de que ninguém esqueceu de regenerar) — não em runtime. O binário final da sua aplicação não carrega sqlc dentro; carrega só o código Go que ele produziu, compilado junto com o resto.

> [!info] sqlc não é um driver — é um gerador que produz código sobre um driver
> O código gerado por sqlc chama `database/sql` (ou `pgx`, se configurado) exatamente como você chamaria manualmente na [[01 - database-sql — o contrato|nota 01]] e na [[04 - pgx — o driver Postgres avançado|nota 04]]. sqlc não substitui o driver — ele **substitui o boilerplate de `Scan` manual** que você escreveria por cima do driver. As duas notas anteriores continuam valendo integralmente para entender o que roda por baixo do código gerado.

## `sqlc.yaml`: a configuração mínima

```yaml
version: "2"
sql:
  - engine: "postgresql"
    queries: "query.sql"
    schema: "schema.sql"
    gen:
      go:
        package: "db"
        out: "internal/db"
        sql_package: "pgx/v5"
        emit_json_tags: true
```

`sql_package: "pgx/v5"` é a escolha que faz o código gerado usar `pgx.Rows` e `pgxpool.Pool` em vez de `sql.DB` — a mesma decisão discutida na nota 04, só que agora tomada uma vez, na config, em vez de espalhada em cada função manual.

## Queries anotadas: os quatro tipos de retorno

```sql
-- name: GetUser :one
SELECT id, name, email, created_at FROM users WHERE id = $1;

-- name: ListUsers :many
SELECT id, name, email, created_at FROM users ORDER BY id;

-- name: CreateUser :one
INSERT INTO users (name, email) VALUES ($1, $2)
RETURNING id, name, email, created_at;

-- name: DeleteUser :exec
DELETE FROM users WHERE id = $1;
```

A anotação depois do nome (`:one`, `:many`, `:exec`, `:execrows`) diz ao gerador que forma a função Go deve ter:

| Anotação | Query espera | Função gerada retorna |
|---|---|---|
| `:one` | no máximo uma linha | `(User, error)` |
| `:many` | zero ou mais linhas | `([]User, error)` |
| `:exec` | sem linhas de retorno (INSERT/UPDATE/DELETE sem RETURNING) | `error` |
| `:execrows` | sem linhas de retorno, mas você quer saber quantas foram afetadas | `(int64, error)` |

Isso resolve, de saída, a ambiguidade que a nota 03 discutiu: a decisão entre `Query`/`QueryRow`/`Exec` deixa de ser algo que você escolhe manualmente a cada chamada — vira parte da anotação da query, e o gerador escolhe a chamada certa no driver por você.

## Código gerado: o que sqlc produz

Rodando `sqlc generate` sobre o schema e as queries acima, o gerador escreve (resumido) algo como:

```go
// internal/db/models.go — gerado, não editar

type User struct {
    ID        int64
    Name      string
    Email     string
    CreatedAt time.Time
}
```

```go
// internal/db/query.sql.go — gerado, não editar

const getUser = `-- name: GetUser :one
SELECT id, name, email, created_at FROM users WHERE id = $1
`

func (q *Queries) GetUser(ctx context.Context, id int64) (User, error) {
    row := q.db.QueryRow(ctx, getUser, id)
    var i User
    err := row.Scan(&i.ID, &i.Name, &i.Email, &i.CreatedAt)
    return i, err
}
```

Repare: o `Scan` manual **não desapareceu** — ele só deixou de ser escrito à mão. O código acima é exatamente o padrão que a nota 03 ensinou, só que gerado automaticamente, com a garantia de que a ordem dos `&campo` bate com a ordem das colunas do `SELECT`, porque as duas vieram da mesma análise da mesma query.

## Usando o código gerado

```go
package main

import (
    "context"
    "fmt"
    "log"

    "github.com/jackc/pgx/v5/pgxpool"
    "meuservico/internal/db"
)

func main() {
    ctx := context.Background()

    pool, err := pgxpool.New(ctx, "postgres://user:pass@localhost:5432/meudb")
    if err != nil {
        log.Fatal(err)
    }
    defer pool.Close()

    queries := db.New(pool) // Queries geradas, embrulhando o pool

    novo, err := queries.CreateUser(ctx, db.CreateUserParams{
        Name:  "Ana",
        Email: "ana@example.com",
    })
    if err != nil {
        log.Fatal(err)
    }

    achado, err := queries.GetUser(ctx, novo.ID)
    if err != nil {
        log.Fatal(err)
    }
    fmt.Printf("%+v\n", achado) // {ID:1 Name:Ana Email:ana@example.com CreatedAt:...}

    todos, err := queries.ListUsers(ctx)
    if err != nil {
        log.Fatal(err)
    }
    fmt.Println(len(todos), "usuários")
}
```

`db.New(pool)` recebe o pool de conexões — o mesmo `*pgxpool.Pool` da [[02 - Connection pool|nota 02]] — e devolve um struct `*Queries` com um método por query anotada. Daqui pra frente, chamar o banco é chamar método Go comum, com tipos conferidos pelo compilador: passar uma `string` onde a query espera `int64` para `$1` não compila, porque `GetUser` foi gerado com assinatura `GetUser(ctx context.Context, id int64)`.

## Armadilhas comuns

> [!warning] Código gerado precisa ser regenerado a cada mudança de schema ou query
> sqlc não observa o banco em runtime — ele lê `schema.sql` e `query.sql` no momento em que você roda `sqlc generate`. Se você alterar a tabela no banco de produção via migration mas esquecer de atualizar `schema.sql` e rodar `sqlc generate` de novo, o código gerado fica **desatualizado silenciosamente**: ele continua compilando, porque nada no Go sabe que o schema real mudou — só vai quebrar em runtime, com um erro do driver, quando a query não bater mais com as colunas reais. A prática comum é rodar `sqlc generate` (e idealmente `sqlc vet`, que valida as queries contra um banco real) como *step* do CI, logo depois de aplicar migrations — assunto que a [[07 - Migrations|nota 07]] cobre em detalhe.

> [!warning] sqlc não é bom para queries construídas dinamicamente
> Um filtro de busca com "N campos opcionais, monte o `WHERE` conforme o que veio preenchido" é o caso clássico onde SQL estático não serve — e sqlc trabalha com SQL estático, parseado em tempo de geração. Dá para contornar com `sqlc.narg()` (parâmetros nulos opcionais) e `CASE WHEN` dentro da própria query, mas passa do ponto onde vale a pena forçar; nesse cenário, um query builder dinâmico (dentro do próprio `database/sql`, montando a string manualmente com cuidado contra SQL injection, ou um ORM como o GORM da próxima nota) tende a ser mais direto.

> [!warning] Código gerado é código gerado — não edite `query.sql.go` à mão
> Qualquer edição manual no arquivo gerado se perde no próximo `sqlc generate`. Se a query gerada não faz o que você precisa, o ajuste é no `.sql` de origem, nunca no `.go` de saída — o comentário `// Code generated by sqlc. DO NOT EDIT.` no topo do arquivo não é decoração.

## Vindo de Java/Node: sqlc como o jOOQ/Prisma do Go

| Ferramenta | Stack | Fonte de verdade | O que gera |
|---|---|---|---|
| **sqlc** | Go | schema SQL + queries SQL, ambos escritos por você | funções Go type-safe, sem runtime próprio |
| **jOOQ** | Java | schema do banco (introspecção) | classes Java + DSL fluente type-safe, com codegen via plugin Maven/Gradle |
| **Prisma** | Node/TS | `schema.prisma` (DSL própria, não SQL) | client TypeScript type-safe, com um *query engine* próprio em runtime (binário Rust) |

A diferença mais relevante para quem migra de Node é essa última coluna: o Prisma Client faz suas queries passarem por um *query engine* próprio, um processo separado que traduz as chamadas do client para SQL em runtime. sqlc **não tem esse runtime** — o código gerado chama `pgx`/`database/sql` diretamente, sem camada intermediária. É mais parecido com o jOOQ nesse aspecto: ambos geram código estático em build-time e delegam a execução real ao driver JDBC/Go padrão, sem processo próprio rodando ao lado da aplicação. A diferença sqlc vs. jOOQ é que jOOQ introspecciona o banco vivo para gerar as classes, enquanto sqlc lê arquivos `.sql` versionados — o que faz mais sentido no fluxo Go de manter schema e migrations como texto no repositório, tema que volta na nota de Migrations.

## Como explicar em inglês

> sqlc is a code generator, not an ORM and not a runtime library: you write real SQL — a schema file with `CREATE TABLE` statements and a queries file with annotated `SELECT`/`INSERT`/`UPDATE` statements — and `sqlc generate` produces plain Go structs and functions from them, with types inferred straight from the schema. There's no reflection at call time and no struct tags to keep in sync by hand; the mapping between SQL columns and Go fields is verified once, at generation time, against the real schema. Each query gets a return-shape annotation — `:one`, `:many`, `:exec`, `:execrows` — that tells sqlc which of `QueryRow`, `Query`, or `Exec` to call underneath. Compared to Prisma, which ships its own runtime query engine, sqlc's generated code calls `database/sql` or `pgx` directly — closer in spirit to jOOQ, which also generates static, compile-time-checked code from a real schema rather than running a query engine of its own.

| Termo PT | Termo EN |
|---|---|
| geração de código | code generation / codegen |
| tipo seguro em tempo de compilação | compile-time type-safe |
| schema (DDL) | schema |
| anotação de query | query annotation |
| driver de saída | output driver / sql_package |
| drift de schema | schema drift |
| código gerado | generated code |
| não editar manualmente | do not edit by hand |

## O que vem a seguir

sqlc resolve o boilerplate de mapeamento mantendo você no controle total da SQL — o preço é que toda query precisa existir, escrita à mão, num arquivo `.sql` antes de virar função Go. A [[06 - GORM — o ORM|próxima nota]] olha para o extremo oposto do espectro: um ORM completo, onde structs Go **geram** a SQL em runtime, sem você escrever `SELECT` nenhum — com o ganho de produtividade em CRUD simples e as armadilhas clássicas de ORM (N+1, queries opacas, mágica que esconde o que realmente roda no banco) que vêm junto.

## Veja também

- [[01 - database-sql — o contrato|01 — database/sql — o contrato]] — a interface que o código gerado por sqlc chama por baixo
- [[02 - Connection pool|02 — Connection pool]] — o pool (`*pgxpool.Pool` ou `*sql.DB`) que `db.New()` recebe como dependência
- [[03 - Query, Scan e o mapeamento manual|03 — Query, Scan e o mapeamento manual]] — o padrão que sqlc automatiza; entender o manual primeiro torna o gerado legível
- [[04 - pgx — o driver Postgres avançado|04 — pgx — o driver Postgres avançado]] — `sql_package: "pgx/v5"` na config do sqlc usa exatamente este driver
- [[06 - GORM — o ORM|06 — GORM — o ORM]] — próxima nota, o extremo oposto do espectro codegen vs. ORM dinâmico
- [[07 - Migrations|07 — Migrations]] — como manter `schema.sql` sincronizado com o banco real ao longo do tempo
- [[03-Dominios/Tecnologia/Go/index|Trilha Go]]

## Fontes

- sqlc. *Documentation — Getting started*. docs.sqlc.dev. https://docs.sqlc.dev/en/latest/ (acessado em 2026-07-18)
- sqlc. *Reference — Configuration (sqlc.yaml)*. docs.sqlc.dev. https://docs.sqlc.dev/en/latest/reference/config.html (acessado em 2026-07-18)
- sqlc. *How-to guides — Query annotations*. docs.sqlc.dev. https://docs.sqlc.dev/en/latest/howto/query-annotations.html (acessado em 2026-07-18)
- sqlc-dev. *sqlc — repositório oficial*. GitHub. https://github.com/sqlc-dev/sqlc (acessado em 2026-07-18)
- The Go Authors. *Package database/sql*. pkg.go.dev. https://pkg.go.dev/database/sql (acessado em 2026-07-18)
