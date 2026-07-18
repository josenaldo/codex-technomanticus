---
title: "pgx — o driver Postgres avançado"
type: concept
fase: Adepto
tags:
  - go
  - persistencia
  - postgres
  - pgx
  - pgxpool
  - database-sql
publish: true
created: 2026-07-18
updated: 2026-07-18
---

# pgx — o driver Postgres avançado

> [!abstract] TL;DR
> `database/sql` foi desenhado para ser genérico — o mesmo contrato serve para Postgres, MySQL, SQLite. Essa generalidade tem um preço: não dá para expor nada que só o Postgres tem. O [`pgx`](https://pkg.go.dev/github.com/jackc/pgx/v5) é o driver que rompe esse teto — usável de duas formas, como driver *sql.DB* comum (`pgx/v5/stdlib`) ou **nativo**, sem passar por `database/sql`, ganhando acesso a arrays, JSONB, `COPY`, tipos compostos e um pool próprio (`pgxpool`) mais rico que o do `database/sql`. Para quem trabalha só com Postgres — o caso mais comum em produção — pgx nativo é hoje o padrão-ouro do ecossistema Go: mais rápido, mais expressivo, e é o motor por baixo de ferramentas populares como sqlc e boa parte do GORM.

## O teto do contrato genérico

A [[01 - database-sql — o contrato|nota 01]] deste galho estabeleceu `database/sql` como um contrato — uma interface que qualquer banco relacional pode implementar via driver. Isso é uma escolha de design deliberada: seu código de negócio não depende de qual banco está por trás, só do pacote padrão. Ótimo para portabilidade.

Só que "portável entre MySQL, SQLite e Postgres" e "aproveita tudo que o Postgres oferece" são objetivos em tensão direta. Pense num exemplo concreto: Postgres tem um tipo nativo `int[]` — um array de inteiros dentro de uma coluna, sem precisar de tabela associativa. `database/sql` não tem ideia do que é um array Postgres, porque MySQL e SQLite não têm esse conceito. O contrato só entende `string`, `int64`, `float64`, `bool`, `[]byte`, `time.Time` — o menor denominador comum entre todos os bancos que algum dia implementarão `driver.Valuer`/`driver.Scanner`.

O mesmo vale para JSONB nativo, tipos compostos (`CREATE TYPE endereco AS (rua text, numero int)`), o comando `COPY` para inserção em massa, `LISTEN`/`NOTIFY` para pub/sub dentro do banco, ou os *prepared statements* binários do protocolo Postgres — nenhuma dessas features cabe numa interface pensada para ser genérica. Se sua equipe só usa Postgres — e a maioria das equipes Go em produção usa só um banco, não troca de SGBD todo mês — pagar esse teto de generalidade é desperdiçar capacidade real do banco que você já escolheu.

É exatamente essa lacuna que o pgx preenche.

## Duas portas de entrada: stdlib e nativo

```mermaid
flowchart TB
    App["Seu código"] --> Choice{"Qual API?"}
    Choice -->|"via database/sql"| Stdlib["pgx/v5/stdlib\n(sql.DB comum)"]
    Choice -->|"nativo"| Native["pgxpool.Pool\n(API própria do pgx)"]

    Stdlib --> Contract["Contrato database/sql\n(genérico, menor denominador comum)"]
    Native --> Full["API completa do pgx\n(arrays, JSONB, COPY, tipos compostos...)"]

    Contract --> Driver["driver pgx (protocolo\nbinário Postgres)"]
    Full --> Driver
    Driver --> PG[("Postgres")]

    style Native fill:#4A90D9,color:#fff
    style Full fill:#F5A623,color:#000
```

`pgx` oferece as duas portas, e a escolha não é ideológica — é sobre quanto do banco você quer expor:

**1. Via `database/sql`**, usando o pacote `pgx/v5/stdlib` como driver: você continua com `*sql.DB`, `db.QueryContext`, tudo que as notas 01-03 deste galho já cobriram. A única mudança é o `sql.Open("pgx", dsn)` no lugar de `sql.Open("postgres", dsn)` (o antigo `lib/pq`, hoje em modo manutenção). Ganha-se a implementação de driver mais rápida e correta disponível para Postgres, mas o contrato genérico continua sendo o teto — sem arrays nativos, sem tipos compostos.

```go
import (
    "database/sql"
    _ "github.com/jackc/pgx/v5/stdlib"
)

db, err := sql.Open("pgx", "postgres://user:pass@localhost:5432/meubanco")
if err != nil {
    log.Fatal(err)
}
defer db.Close()
// dali pra frente, é database/sql normal — QueryContext, Scan, etc.
```

**2. Nativo**, sem `database/sql` no meio — usando `pgxpool.Pool` (ou `pgx.Conn` para conexão única, mais raro em produção) diretamente:

```go
import (
    "context"
    "github.com/jackc/pgx/v5/pgxpool"
)

pool, err := pgxpool.New(context.Background(), "postgres://user:pass@localhost:5432/meubanco")
if err != nil {
    log.Fatal(err)
}
defer pool.Close()

var nome string
err = pool.QueryRow(context.Background(), "SELECT nome FROM usuarios WHERE id = $1", 42).Scan(&nome)
```

A assinatura de `QueryRow` parece quase idêntica à de `database/sql` — mesmo padrão de placeholder `$1`, mesmo `.Scan`. A diferença real não está na sintaxe da chamada; está no que passa a ser possível declarar como tipo de argumento e de retorno, e no comportamento por baixo do protocolo — que é o assunto das próximas duas seções.

> [!info] `pgx/v5` é a versão vigente
> A série `v4` do pgx ainda circula em código legado, mas o [repositório oficial](https://github.com/jackc/pgx) recomenda `v5` para todo projeto novo — API mais limpa, melhor suporte a contexto e integração nativa com o pooling que a próxima seção detalha. Import path: `github.com/jackc/pgx/v5`.

## pgxpool: o pool nativo do pgx

A [[02 - Connection pool|nota 02]] deste galho já cobriu o pool embutido em `*sql.DB` — `SetMaxOpenConns`, `SetMaxIdleConns`, `SetConnMaxLifetime`. Quando você usa pgx nativo, esse pool desaparece e entra `pgxpool.Pool`, com uma filosofia de configuração mais explícita:

```go
config, err := pgxpool.ParseConfig("postgres://user:pass@localhost:5432/meubanco")
if err != nil {
    log.Fatal(err)
}

config.MaxConns = 25
config.MinConns = 5
config.MaxConnLifetime = 30 * time.Minute
config.MaxConnIdleTime = 5 * time.Minute
config.HealthCheckPeriod = time.Minute

pool, err := pgxpool.NewWithConfig(context.Background(), config)
if err != nil {
    log.Fatal(err)
}
defer pool.Close()
```

A diferença mais prática em relação ao pool do `database/sql` é o `HealthCheckPeriod`: o `pgxpool` verifica periodicamente, em background, se as conexões ociosas ainda estão vivas — e descarta as que morreram (por exemplo, um Postgres que reiniciou ou um load balancer que fechou a conexão por timeout) antes que uma requisição real bata numa conexão morta. `database/sql` também detecta conexão morta, mas só na hora de usá-la — o `pgxpool` antecipa isso de forma proativa.

Outra diferença estrutural: cada conexão do `pgxpool` é, por baixo, um `*pgx.Conn` completo — o que significa que, ao pegar uma conexão emprestada do pool (`pool.Acquire(ctx)`), você tem acesso à API nativa inteira, não só ao subconjunto genérico. Isso importa quando alguma operação — `COPY`, por exemplo — precisa de uma conexão dedicada em vez de uma query isolada:

```go
conn, err := pool.Acquire(context.Background())
if err != nil {
    log.Fatal(err)
}
defer conn.Release()

_, err = conn.Conn().CopyFrom(
    context.Background(),
    pgx.Identifier{"usuarios"},
    []string{"nome", "email"},
    pgx.CopyFromRows([][]any{
        {"Ana", "ana@example.com"},
        {"Bruno", "bruno@example.com"},
    }),
)
```

`COPY` usa o protocolo binário do Postgres para inserção em massa — ordens de magnitude mais rápido que `N` comandos `INSERT` sequenciais, porque evita o parsing SQL e o round-trip de rede por linha. `database/sql` não tem como expressar isso: não existe um `driver.Valuer` genérico para "modo COPY". É uma operação Postgres-específica, então só existe do lado nativo do pgx.

> [!warning] `pool.Acquire` sem `Release` vaza conexão do pool
> Diferente de `QueryRow`/`Exec`, que devolvem a conexão ao pool sozinhos quando terminam, `Acquire` empresta a conexão manualmente — e é seu trabalho chamar `conn.Release()` (idealmente via `defer`, logo após o `Acquire` bem-sucedido). Esquecer isso é o equivalente, em pgx nativo, de esquecer `rows.Close()` no `database/sql`: o pool encolhe silenciosamente até esgotar `MaxConns`.

## Tipos Postgres que só o pgx entende

O ganho mais visível de usar pgx nativo é o que ele consegue mapear direto entre Go e tipos que o Postgres tem e o `database/sql` genérico não sabe representar.

**Arrays nativos.** Uma coluna `integer[]` ou `text[]` mapeia direto para um slice Go, sem serialização manual:

```go
var tags []string
err := pool.QueryRow(ctx, "SELECT tags FROM posts WHERE id = $1", 7).Scan(&tags)
// tags já é []string — pgx converteu o array Postgres automaticamente
```

Com `database/sql` puro, o mesmo `text[]` chegaria como uma string bruta no formato `{tag1,tag2,tag3}`, exigindo parsing manual ou uma lib de terceiros (`lib/pq` tinha um tipo `pq.Array` só para contornar isso).

**JSONB direto em struct.** Combinando pgx com a tag `json` de uma struct, uma coluna `jsonb` deserializa automaticamente:

```go
type Endereco struct {
    Rua    string `json:"rua"`
    Numero int    `json:"numero"`
}

var end Endereco
err := pool.QueryRow(ctx, "SELECT endereco FROM usuarios WHERE id = $1", 42).Scan(&end)
```

Isso funciona porque o pgx registra, por baixo, um `pgtype.Codec` para `jsonb` que sabe chamar `json.Unmarshal` no `[]byte` recebido do wire e popular a struct de destino — o mesmo mecanismo que a [[03 - Query, Scan e o mapeamento manual|nota 03]] descreveu para `sql.Scanner`, só que o pgx já vem com o mapeamento pronto para os tipos do Postgres, sem você escrever o `Scan()` manual.

**Tipos numéricos de precisão exata.** `numeric`/`decimal` do Postgres não cabe sem perda em `float64` — é o clássico problema de ponto flutuante aplicado a dinheiro. O pacote `github.com/jackc/pgx/v5/pgtype` expõe `pgtype.Numeric`, que preserva a precisão exata do valor Postgres em Go, algo que `database/sql` genérico, de novo, não tem como representar sem um tipo próprio.

```mermaid
flowchart LR
    subgraph PG["Tipos Postgres"]
        A1["int[] / text[]"]
        A2["jsonb"]
        A3["numeric"]
        A4["tipos compostos"]
    end
    subgraph SQLGeneric["database/sql genérico"]
        B1["string bruta\n(parsing manual)"]
    end
    subgraph PgxNative["pgx nativo"]
        C1["[]string / []int"]
        C2["struct via json tag"]
        C3["pgtype.Numeric"]
        C4["struct mapeada"]
    end

    A1 -.->|"sem pgx"| B1
    A1 -->|"com pgx"| C1
    A2 --> C2
    A3 --> C3
    A4 --> C4

    style PgxNative fill:#4A90D9,color:#fff
```

> [!info] pgtype é opt-in, não obrigatório
> Você não precisa importar `pgtype` explicitamente para os casos comuns (arrays, JSONB) — o driver já resolve a conversão para tipos Go idiomáticos (`[]string`, struct via `json`) automaticamente no `Scan`. `pgtype` entra em cena quando o tipo Postgres não tem equivalente direto e óbvio em Go — como `numeric` de precisão arbitrária, `interval`, ou tipos de rede (`inet`, `cidr`).

## Por que pgx virou o padrão-ouro

Três fatores, combinados, explicam por que o ecossistema Go convergiu para pgx quando o banco é Postgres:

1. **Performance.** O pgx implementa o protocolo binário do Postgres diretamente — evita a camada de conversão texto↔binário que drivers mais antigos (como o extinto `lib/pq`) faziam em cada query. Benchmarks publicados pelo próprio mantenedor mostram pgx consistentemente mais rápido que alternativas, especialmente em queries com muitos parâmetros ou muitas linhas de retorno.
2. **`lib/pq` está em modo manutenção.** O driver Postgres histórico do Go, `github.com/lib/pq`, [anuncia no próprio README](https://github.com/lib/pq) que não recebe mais desenvolvimento ativo desde 2021 — só correções críticas. Qualquer projeto novo que escolha `lib/pq` hoje está escolhendo um driver estagnado por preferência de familiaridade, não por vantagem técnica.
3. **Base de ferramentas do ecossistema.** [`sqlc`](https://sqlc.dev) (nota 05 deste galho) gera código que usa pgx como driver por padrão em projetos Postgres; o GORM (nota 06) também suporta pgx como driver de baixo nível. Escolher pgx hoje significa estar alinhado com o caminho que a maior parte do tooling Go para Postgres já assumiu como padrão.

> [!warning] Nativo prende você ao Postgres — decisão arquitetural, não só técnica
> Usar `pgxpool` nativo (em vez de pgx via `database/sql`) significa que seu código de acesso a dados não compila mais contra outro banco sem reescrita — você trocou portabilidade por poder de expressão. Para a maioria dos times que só usa Postgres em produção (o cenário mais comum), essa troca compensa. Se existe alguma chance real de trocar de SGBD, ou se você mantém uma lib que precisa suportar múltiplos bancos, ficar em `database/sql` (mesmo usando `pgx/v5/stdlib` como driver por baixo) preserva a saída.

## Vindo de outras stacks

| Vindo de... | Equivalente aproximado | Diferença que importa |
|---|---|---|
| Java (JDBC + driver Postgres) | JDBC genérico vs `pgjdbc` com extensões específicas | Java raramente separa "driver genérico" de "API nativa" como opção de primeira classe — pgx torna essa escolha explícita e comum |
| Node (`pg` / `node-postgres`) | `pg` já expõe arrays e JSONB nativamente por padrão | Node não tem um contrato genérico tipo `database/sql` no meio — `pg` sempre foi "nativo" |
| Python (`psycopg2`/`psycopg3`) | `psycopg` também expõe tipos Postgres avançados fora do DB-API padrão | Python tem PEP 249 (DB-API) como o análogo do `database/sql`, com a mesma tensão genérico-vs-nativo |

A situação do Go não é única — é a mesma tensão entre "contrato portável" e "poder específico do banco" que aparece em qualquer stack com uma camada de abstração de banco de dados. A diferença é que Go torna as duas opções (`database/sql` genérico vs pgx nativo) igualmente fáceis de escolher, em vez de uma ser o caminho "de fábrica" e a outra, obscura.

## Armadilhas comuns

> [!warning] Misturar `pgxpool.Pool` e `*sql.DB` no mesmo código gera confusão de API
> As duas têm métodos parecidos (`QueryRow`, `Exec`) mas assinaturas e tipos de retorno diferentes — `pgxpool.Pool.QueryRow` retorna `pgx.Row`, não `*sql.Row`. Misturar os dois estilos no mesmo pacote, achando que são intercambiáveis, gera erros de compilação confusos. Escolha um caminho (stdlib ou nativo) por serviço/repositório e mantenha consistência.

> [!warning] `Scan` em `pgx.Row` não devolve `sql.ErrNoRows`
> No `database/sql`, zero linhas retornadas por `QueryRow` produz `sql.ErrNoRows`. No pgx nativo, o erro equivalente é `pgx.ErrNoRows` — um valor diferente, do pacote `pgx`, não do pacote `sql`. Código que testa `errors.Is(err, sql.ErrNoRows)` depois de migrar de `database/sql` para pgx nativo silenciosamente para de funcionar; o teste precisa virar `errors.Is(err, pgx.ErrNoRows)`.

> [!warning] `pgxpool.New` não valida a conexão imediatamente
> Assim como o `sql.Open` do `database/sql` (nota 02), `pgxpool.New` só monta a configuração — não abre conexão de verdade nem valida credenciais. Um `pool.Ping(ctx)` logo após a criação (tipicamente no health-check de startup da aplicação) é o jeito de descobrir cedo se a string de conexão está errada, em vez de só na primeira query real.

## Como explicar em inglês

> `database/sql` is deliberately generic — its contract has to work across Postgres, MySQL, and SQLite, so it can't expose anything Postgres-specific. `pgx` is the driver that breaks that ceiling. It can be used two ways: as a drop-in `database/sql` driver (`pgx/v5/stdlib`), or natively via `pgxpool.Pool`, bypassing `database/sql` entirely. Going native unlocks Postgres-only features the generic contract can't represent — native arrays mapping straight to Go slices, JSONB unmarshaling into structs, exact-precision `numeric` via `pgtype`, and bulk `COPY` for high-throughput inserts. `pgxpool` also ships a richer pool than the stdlib one, with proactive background health checks that evict dead idle connections before a request hits them. The trade-off is real: native pgx locks your code to Postgres, trading portability for expressiveness — a trade most teams that only ever run Postgres in production are happy to make, and it's why sqlc and GORM both lean on pgx as their default Postgres driver today.

| Termo PT | Termo EN |
|---|---|
| driver nativo | native driver |
| pool de conexões | connection pool |
| verificação de saúde | health check |
| inserção em massa | bulk insert |
| tipo composto | composite type |
| precisão exata | exact precision |
| protocolo binário | binary protocol |
| modo manutenção | maintenance mode |

## O que vem a seguir

pgx nativo resolve o problema de *expressividade* — acessar o que o Postgres oferece. Mas escrever SQL como string literal, com `Scan` manual campo a campo, ainda deixa espaço para erro de tipo que só aparece em runtime: um `$1` que devia ser `int` recebendo uma `string`, um `Scan(&x)` com a ordem de colunas trocada. A [[05 - sqlc — SQL type-safe por codegen|nota 05]] mostra a segunda peça do quebra-cabeça: gerar código Go type-safe a partir do SQL que você já escreve — sem ORM, sem query builder — usando pgx como motor por baixo.

## Veja também

- [[01 - database-sql — o contrato|01 — database/sql — o contrato]] — o contrato genérico que o pgx nativo contorna
- [[02 - Connection pool|02 — Connection pool]] — o pool do `database/sql`, contraponto ao `pgxpool` desta nota
- [[03 - Query, Scan e o mapeamento manual|03 — Query, Scan e o mapeamento manual]] — o `Scan()` manual que o pgx automatiza para tipos Postgres
- [[05 - sqlc — SQL type-safe por codegen|05 — sqlc — SQL type-safe por codegen]] — próxima nota do galho, usa pgx como driver por baixo
- [[03-Dominios/Tecnologia/Go/index|Trilha Go]]

## Fontes

- jackc. *pgx — PostgreSQL Driver and Toolkit for Go*. GitHub. https://github.com/jackc/pgx (acessado em 2026-07-18)
- jackc. *pgx/v5 package documentation*. pkg.go.dev. https://pkg.go.dev/github.com/jackc/pgx/v5 (acessado em 2026-07-18)
- jackc. *pgxpool package documentation*. pkg.go.dev. https://pkg.go.dev/github.com/jackc/pgx/v5/pgxpool (acessado em 2026-07-18)
- jackc. *pgtype package documentation*. pkg.go.dev. https://pkg.go.dev/github.com/jackc/pgx/v5/pgtype (acessado em 2026-07-18)
- lib/pq maintainers. *lib/pq — Pure Go Postgres driver (maintenance mode)*. GitHub. https://github.com/lib/pq (acessado em 2026-07-18)
- The Go Authors. *database/sql package documentation*. pkg.go.dev. https://pkg.go.dev/database/sql (acessado em 2026-07-18)
