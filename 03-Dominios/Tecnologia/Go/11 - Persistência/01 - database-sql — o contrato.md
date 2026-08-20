---
title: "database/sql — o contrato"
type: concept
fase: iniciado
tags:
  - go
  - persistencia
  - database-sql
  - drivers
  - sql
publish: true
created: 2026-07-18
updated: 2026-07-18
---

# database/sql — o contrato

> [!abstract] TL;DR
> `database/sql` não fala com nenhum banco — é uma **interface**. O trabalho real de abrir socket, autenticar e falar o protocolo binário do Postgres, MySQL ou SQLite fica com um **driver**, importado só pelo efeito colateral (`_ "github.com/lib/pq"`), que se registra num registro global via `sql.Register` dentro de um `init()`. `sql.Open` não conecta a nada — só valida os argumentos e devolve um `*sql.DB`, que **não é uma conexão**: é um **pool** de conexões geridas pela biblioteca padrão. `Query`/`QueryRow` leem, `Exec` escreve — e cada uma tem uma forma própria de reportar erro e liberar recursos. Entender esse desenho — biblioteca padrão define o contrato, driver externo implementa — é o que torna o resto do galho (pool, scan, pgx, sqlc, GORM) legível como variações sobre a mesma base, não ferramentas desconexas.

## O problema: um Go que fala com qualquer banco

Imagine que você está escrevendo uma aplicação Go que precisa falar com Postgres. Óbvio, certo? Importa o driver do Postgres, chama as funções dele, pronto. Mas e se, dois anos depois, a empresa migrar para MySQL? Ou se você quiser rodar os testes de integração contra SQLite em memória, sem subir um Postgres real? Se todo o seu código de acesso a dados chama diretamente a API específica do driver Postgres, a migração vira uma reescrita.

Java resolveu esse problema nos anos 90 com JDBC: uma interface padrão (`java.sql.Connection`, `java.sql.Statement`) que qualquer banco implementa via driver próprio, mais uma `DriverManager` central que resolve qual driver usar a partir da connection string. Python tem a PEP 249 (DB-API 2.0) — um contrato parecido, cumprido por `psycopg2`, `mysqlclient`, `sqlite3`. Node não tem um padrão tão rígido — cada driver (`pg`, `mysql2`) expõe sua própria API, e é o ORM (Knex, Prisma) que costuma abstrair a diferença.

Go escolheu o caminho do JDBC: um pacote da biblioteca padrão, `database/sql`, define o **contrato** — os tipos e métodos que qualquer código Go usa para falar com um banco relacional — e delega a implementação real do protocolo de rede a um **driver** externo, importado só pelo pacote específico do banco. O código de aplicação nunca importa `lib/pq` ou `go-sql-driver/mysql` diretamente nas suas chamadas — só no import, para registrar o driver. Tudo o resto passa por `database/sql`.

## Anatomia: quem faz o quê

```mermaid
flowchart LR
    subgraph App["Seu código"]
        A["sql.Open('postgres', dsn)"] --> B["*sql.DB"]
        B --> C["db.Query / db.Exec"]
    end

    subgraph Std["database/sql (biblioteca padrão)"]
        D["Interface driver.Driver\ndriver.Conn\ndriver.Stmt"]
        E["Registro global\nsql.Register"]
    end

    subgraph Driver["Driver externo (import _)"]
        F["lib/pq, pgx, go-sql-driver/mysql..."]
        G["Protocolo de rede do banco\n(TCP, autenticação, wire format)"]
    end

    C -.usa contrato.-> D
    F -.se registra em.-> E
    F --> G
    B -."abre conexões via".-> F

    style D fill:#4A90D9,color:#fff
    style E fill:#4A90D9,color:#fff
    style F fill:#F5A623,color:#000
```

`database/sql` define duas coisas: a API pública que você chama (`sql.DB`, `sql.Rows`, `sql.Stmt`) e um segundo conjunto de interfaces, em `database/sql/driver`, que qualquer driver precisa implementar (`driver.Driver`, `driver.Conn`, `driver.Stmt`) para se plugar nesse contrato. Um driver como `lib/pq` implementa `driver.Driver` e, no `init()` do seu pacote, se registra:

```go
// dentro do pacote lib/pq, simplificado
func init() {
    sql.Register("postgres", &Driver{})
}
```

É exatamente por isso que a importação de driver em código Go tem essa forma peculiar:

```go
import (
    "database/sql"

    _ "github.com/lib/pq" // import só pelo efeito colateral do init()
)
```

O `_` (blank identifier) diz ao compilador "importe este pacote, rode seu `init()`, mas eu não vou referenciar nenhum símbolo dele diretamente". Sem o `_`, o compilador reclamaria de import não usado — porque, de fato, nenhuma função ou tipo de `lib/pq` aparece no seu código. Toda a interação passa por `database/sql`, que consulta o registro global (`sql.Register`) na hora de `sql.Open` para descobrir qual driver corresponde ao nome `"postgres"`.

> [!question]- Por que não `import pq "github.com/lib/pq"` e usar as funções dele direto?
> Porque isso quebraria o desacoplamento inteiro. Se o seu código de acesso a dados chamasse tipos específicos de `lib/pq`, trocar de driver (por exemplo, para `pgx` rodando em modo compatibilidade com `database/sql`) exigiria reescrever cada chamada. O import-só-efeito-colateral é o preço de manter seu código falando apenas com `*sql.DB`, `*sql.Rows` e `*sql.Row` — tipos que qualquer driver compatível sabe preencher.

## `sql.Open`: não conecta, só prepara

A primeira surpresa de quem espera um comportamento tipo `psycopg2.connect(...)` (que já abre socket e autentica na hora): `sql.Open` **não conecta a lugar nenhum**.

```go
db, err := sql.Open("postgres", "postgres://user:senha@localhost/meubanco?sslmode=disable")
if err != nil {
    log.Fatal(err)
}
defer db.Close()
```

`sql.Open` faz só duas coisas: valida se existe um driver registrado sob o nome `"postgres"` e valida a sintaxe do DSN (*data source name*, a string de conexão) contra o parser desse driver. Nenhum pacote é enviado à rede. O `error` retornado aqui é quase sempre um erro de configuração (driver não registrado, DSN malformado) — nunca "banco fora do ar" ou "senha errada". Isso só aparece na primeira operação real, porque `*sql.DB` abre conexões físicas de forma **preguiçosa (lazy)**, sob demanda.

Se você quer forçar a conexão imediatamente — por exemplo, para falhar rápido no health check de inicialização — o pacote oferece `Ping`:

```go
if err := db.Ping(); err != nil {
    log.Fatalf("não conectou ao banco: %v", err)
}
```

`Ping` abre (ou reutiliza) uma conexão do pool e roda um comando trivial contra o banco só para confirmar que a rede e as credenciais funcionam. Sem chamar `Ping` (ou qualquer query), um `sql.Open` com credenciais completamente erradas compila, roda e não devolve erro nenhum — até a primeira `Query`.

> [!info] `*sql.DB` é um pool, não uma conexão
> A [documentação oficial](https://pkg.go.dev/database/sql#Open) é explícita: "The returned DB is safe for concurrent use by multiple goroutines and maintains its own pool of idle connections." `*sql.DB` representa o banco como um todo — não uma sessão TCP única. Por baixo, ele mantém várias conexões físicas abertas, reaproveitadas entre chamadas. A nota seguinte deste galho ([[02 - Connection pool|02 — Connection pool]]) entra no tuning desse pool; por ora, o que importa é o modelo mental: **você abre `*sql.DB` uma vez por processo, guarda essa referência, e reusa para todas as queries** — nunca chama `sql.Open` a cada requisição.

## `Query`, `QueryRow`, `Exec`: três formas de falar com o banco

`database/sql` expõe três métodos centrais em `*sql.DB`, cada um pensado para um formato de resultado diferente.

### `Exec` — comandos que não devolvem linhas

Para `INSERT`, `UPDATE`, `DELETE` ou DDL (`CREATE TABLE`), onde o interesse está no efeito, não em linhas de retorno:

```go
result, err := db.Exec(
    "INSERT INTO produtos (nome, preco) VALUES ($1, $2)",
    "Caneta", 2.50,
)
if err != nil {
    log.Fatal(err)
}

linhasAfetadas, err := result.RowsAffected()
fmt.Println(linhasAfetadas) // 1
```

`Exec` devolve um `sql.Result`, com dois métodos: `RowsAffected()` (quantas linhas foram alteradas) e `LastInsertId()` (o ID gerado, quando o driver e o banco suportam — Postgres, notavelmente, **não** popula isso por padrão, porque não tem um conceito nativo de "last insert id"; a alternativa é `RETURNING id` na própria query).

### `QueryRow` — exatamente zero ou uma linha esperada

Para consultas onde você espera **no máximo uma linha** — busca por chave primária, `COUNT(*)`, agregações:

```go
var nome string
var preco float64

err := db.QueryRow(
    "SELECT nome, preco FROM produtos WHERE id = $1", 42,
).Scan(&nome, &preco)

if errors.Is(err, sql.ErrNoRows) {
    fmt.Println("produto não encontrado")
} else if err != nil {
    log.Fatal(err)
}
```

`QueryRow` nunca devolve `error` diretamente do próprio método — o `error` só aparece depois, no `Scan`. Se a query não encontrar nenhuma linha, `Scan` devolve o sentinel `sql.ErrNoRows` — não um `nil` silencioso, nem um valor zerado. É a forma idiomática de checar "não achei" versus "algo quebrou": comparar com `errors.Is(err, sql.ErrNoRows)`, nunca assumir que ausência de erro significa que os dados vieram.

### `Query` — zero, uma ou N linhas, com iteração manual

Para qualquer resultado que possa ter mais de uma linha:

```go
rows, err := db.Query("SELECT id, nome, preco FROM produtos WHERE preco > $1", 10.0)
if err != nil {
    log.Fatal(err)
}
defer rows.Close()

for rows.Next() {
    var id int
    var nome string
    var preco float64
    if err := rows.Scan(&id, &nome, &preco); err != nil {
        log.Fatal(err)
    }
    fmt.Printf("%d: %s (R$%.2f)\n", id, nome, preco)
}

if err := rows.Err(); err != nil {
    log.Fatal(err)
}
```

Este é o padrão que mais causa vazamento de recurso em código Go iniciante: **três pontos de erro precisam de tratamento**, não um só. `db.Query` pode falhar na hora de abrir o cursor. `rows.Scan` pode falhar linha a linha. E — o mais esquecido — `rows.Err()`, chamado **depois** do laço `for rows.Next()`, reporta qualquer erro que tenha interrompido a iteração no meio (conexão caiu, contexto cancelado). Sem checar `rows.Err()`, um laço que terminou cedo por erro de rede parece, aos seus olhos, ter simplesmente processado "todas as linhas que havia" — quando na verdade parou no meio sem avisar.

```mermaid
sequenceDiagram
    participant App as Seu código
    participant DB as *sql.DB (pool)
    participant Drv as Driver (ex: lib/pq)
    participant Srv as Servidor Postgres

    App->>DB: db.Query(sql, args...)
    DB->>Drv: pega conexão do pool
    Drv->>Srv: envia query (protocolo wire)
    Srv-->>Drv: começa a devolver linhas
    Drv-->>DB: *sql.Rows (cursor aberto)
    DB-->>App: rows, err

    loop rows.Next()
        App->>DB: rows.Next()
        DB->>Drv: busca próxima linha
        Drv-->>DB: linha ou fim
        App->>DB: rows.Scan(&campos...)
    end

    App->>DB: rows.Err()
    App->>DB: rows.Close() (via defer)
    DB->>Drv: devolve conexão ao pool
```

`rows.Close()` **precisa** ser chamado — e o idioma padrão é `defer rows.Close()` logo após checar o `err` de `Query`. Sem fechar, a conexão física usada por aquele cursor não volta para o pool: sob carga, isso esgota o pool inteiro e trava a aplicação com erros de "too many connections" — mesmo que o processo Go pareça estar rodando normalmente. `Scan` bem-sucedido em todas as linhas até `rows.Next()` devolver `false` chama `Close` automaticamente por baixo dos panos, mas contar com isso e omitir o `defer` é frágil: qualquer saída antecipada do laço (um `return`, um `break`, um `panic`) pula esse fechamento implícito.

## Casos práticos

**1. Setup mínimo — abrir, verificar, fechar:**

```go
package main

import (
    "database/sql"
    "log"

    _ "github.com/lib/pq"
)

func main() {
    db, err := sql.Open("postgres", "postgres://user:senha@localhost/meubanco?sslmode=disable")
    if err != nil {
        log.Fatalf("configuração inválida: %v", err)
    }
    defer db.Close()

    if err := db.Ping(); err != nil {
        log.Fatalf("banco inacessível: %v", err)
    }

    log.Println("conectado")
}
```

**2. `QueryRow` com tratamento explícito de "não encontrado":**

```go
func buscarProdutoPorID(db *sql.DB, id int) (nome string, preco float64, err error) {
    err = db.QueryRow(
        "SELECT nome, preco FROM produtos WHERE id = $1", id,
    ).Scan(&nome, &preco)

    if errors.Is(err, sql.ErrNoRows) {
        return "", 0, fmt.Errorf("produto %d não existe", id)
    }
    return nome, preco, err
}
```

**3. `Query` com contexto, para respeitar cancelamento e timeout — o padrão recomendado desde Go 1.8:**

```go
func listarProdutosCaros(ctx context.Context, db *sql.DB, precoMin float64) ([]Produto, error) {
    rows, err := db.QueryContext(ctx,
        "SELECT id, nome, preco FROM produtos WHERE preco > $1", precoMin,
    )
    if err != nil {
        return nil, err
    }
    defer rows.Close()

    var produtos []Produto
    for rows.Next() {
        var p Produto
        if err := rows.Scan(&p.ID, &p.Nome, &p.Preco); err != nil {
            return nil, err
        }
        produtos = append(produtos, p)
    }
    return produtos, rows.Err()
}
```

> [!info] `QueryContext` / `ExecContext` / `QueryRowContext`
> Toda operação de `database/sql` tem uma variante `*Context` que recebe um `context.Context` como primeiro argumento. Em código de produção — especialmente atrás de um handler HTTP — a variante com contexto é a recomendada por padrão: se o cliente cancelar a requisição ou o timeout expirar, a query em andamento é abortada no banco, em vez de continuar consumindo uma conexão do pool para um resultado que ninguém mais espera.

## Armadilhas comuns

> [!warning] Esquecer `defer rows.Close()` esgota o pool sob carga
> É o erro mais comum e mais silencioso do pacote: em desenvolvimento, com poucas queries, o pool tem conexões ociosas sobrando e ninguém percebe o vazamento. Em produção, sob volume real, o pool satura e a aplicação começa a travar em `db.Query` esperando uma conexão livre que nunca é devolvida. Sempre `defer rows.Close()` logo após checar o erro de `Query`.

> [!warning] `sql.Open` sem erro não significa "conectei com sucesso"
> Como visto acima, `sql.Open` só valida sintaxe e driver registrado — nunca abre socket. Um DSN com senha errada, host inexistente ou banco que não existe passa por `sql.Open` sem reclamar. Se o objetivo é falhar rápido na inicialização (o padrão saudável para qualquer serviço), chame `db.Ping()` (ou `PingContext`) logo depois.

> [!warning] Reabrir `*sql.DB` a cada requisição recria o problema que o pool resolve
> `sql.Open` é barato o suficiente para tentar chamá-lo "por conveniência" dentro de um handler HTTP — mas isso destrói o propósito do pool: cada chamada cria um novo `*sql.DB` com seu próprio conjunto de conexões, nenhuma reaproveitada da anterior. O padrão correto é abrir `*sql.DB` uma vez, na inicialização do processo, guardar a referência (campo de struct, variável de pacote, injeção de dependência) e reutilizá-la para todo o ciclo de vida da aplicação.

## Vindo de outra stack

| Vindo de | Em Go é assim |
|---|---|
| Java (JDBC) | `DriverManager.getConnection` vira `sql.Open` + registro via `sql.Register` no `init()` do driver — mesma ideia de contrato + implementação plugável, só que sem `DriverManager` central: o nome do driver já resolve tudo |
| Python (DB-API 2.0 / `psycopg2`) | `psycopg2.connect()` conecta na hora; `sql.Open` não — a conexão real só acontece na primeira operação (ou em `Ping`) |
| Node (`pg`, `mysql2`) | Sem padrão unificado — cada driver expõe API própria; `database/sql` é o equivalente ao que só um ORM/query builder ofereceria em Node |
| Qualquer ORM com "lazy connection" | O modelo lazy de `*sql.DB` é a norma em Go, não uma feature especial — todo `sql.Open` se comporta assim, com ou sem ORM por cima |

## Como explicar em inglês

> `database/sql` is Go's standard-library abstraction for relational databases — it defines the contract (`sql.DB`, `sql.Rows`, `sql.Row`), while an external driver, imported purely for its side effect (`_ "github.com/lib/pq"`), implements the actual wire protocol and registers itself via `sql.Register` inside an `init()` function. `sql.Open` doesn't connect to anything — it only validates the driver name and DSN syntax; the returned `*sql.DB` is a **connection pool**, not a single connection, and it dials lazily on the first real operation (or on an explicit `Ping`). Three core methods cover the read/write surface: `Exec` for statements with no row results, `QueryRow` for at-most-one-row lookups (which surface "not found" as the `sql.ErrNoRows` sentinel from `Scan`, not a special return value), and `Query` for multi-row results, which require checking three separate error points — the initial call, each `Scan`, and `rows.Err()` after the loop — plus a `defer rows.Close()` to return the connection to the pool.

| Termo PT | Termo EN |
|---|---|
| driver | driver |
| pool de conexões | connection pool |
| registro global de drivers | driver registry |
| conexão preguiçosa | lazy connection |
| linha não encontrada | row not found |
| cursor de resultados | result cursor |
| liberar recurso | release resource |
| esgotar o pool | exhaust the pool |

## O que vem a seguir

Ficou pendente, ao longo desta nota, uma pergunta implícita: se `*sql.DB` é um pool, quantas conexões ele mantém abertas por padrão? O que acontece quando todas estão ocupadas e chega uma nova query? Quanto tempo uma conexão ociosa fica viva antes de ser fechada? A [[02 - Connection pool|nota 02]] entra direto nesse tuning — `SetMaxOpenConns`, `SetMaxIdleConns`, `SetConnMaxLifetime` — e no comportamento real do pool sob carga, incluindo o que muda quando o banco também impõe seu próprio limite de conexões simultâneas.

## Veja também

- [[02 - Connection pool|02 — Connection pool]] — tuning do pool que `*sql.DB` já esconde por baixo desta nota
- [[03 - Query, Scan e o mapeamento manual|03 — Query, Scan e o mapeamento manual]] — o mecanismo de `Scan` aprofundado, incluindo `sql.NullString` e tipos opcionais
- [[04 - pgx — o driver Postgres avançado|04 — pgx — o driver Postgres avançado]] — alternativa a `lib/pq` com API nativa mais rica, além do modo de compatibilidade com `database/sql`
- [[08 - Transações e o padrão repository|08 — Transações e o padrão repository]] — onde `*sql.Tx`, também parte deste mesmo contrato, entra em cena
- [[03-Dominios/Tecnologia/Go/index|Trilha Go]]

## Fontes

- The Go Authors. *Package database/sql*. pkg.go.dev. https://pkg.go.dev/database/sql (acessado em 2026-07-18)
- The Go Authors. *Package database/sql/driver*. pkg.go.dev. https://pkg.go.dev/database/sql/driver (acessado em 2026-07-18)
- The Go Authors. *Go database/sql tutorial*. go.dev/wiki. https://go.dev/wiki/SQLInterface (acessado em 2026-07-18)
- The Go Authors. *Go Wiki: SQLDrivers* — lista de drivers compatíveis com database/sql. go.dev/wiki. https://go.dev/wiki/SQLDrivers (acessado em 2026-07-18)
- Go by Example. *Context*. gobyexample.com. https://gobyexample.com/context (acessado em 2026-07-18)
