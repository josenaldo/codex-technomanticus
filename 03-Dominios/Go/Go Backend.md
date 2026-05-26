---
title: "Go Backend"
created: 2026-04-10
updated: 2026-04-10
type: concept
status: seedling
tags:
  - go
  - backend
  - entrevista
publish: false
---

# Go Backend

Go para backend — goroutines, net/http, e o ecossistema para serviços de alta performance. Para entrevistas, o foco é em como Go resolve os mesmos problemas de produção que Java e Node.js, com sua abordagem idiomática.

## O que é

Go é uma linguagem compilada, statically typed, projetada pelo Google para serviços de backend de alta performance. Destaca-se por: goroutines (concorrência leve), compilação rápida, binários estáticos, e stdlib poderosa.

**Onde Go brilha:** microserviços, CLI tools, infraestrutura (Docker, Kubernetes, Terraform são escritos em Go), APIs de alta performance.

## Frameworks e bibliotecas

| Ferramenta | Papel | Equivalente Java/Node |
| --- | --- | --- |
| net/http (stdlib) | HTTP server/router | Servlet API |
| Gin / Chi / Echo | Web framework | Express / Spring MVC |
| GORM | ORM | Hibernate / Sequelize |
| sqlc | Type-safe SQL (code gen) | jOOQ / Prisma |
| pgx | Driver PostgreSQL avançado | HikariCP + JDBC |
| Wire | Dependency injection (compile-time) | Spring DI / NestJS DI |

**Filosofia Go:** stdlib forte, frameworks opcionais, composição sobre herança, erros explícitos sobre exceções.

## Troubleshooting em produção

Problemas recorrentes e suas soluções idiomáticas em Go — comparáveis aos problemas de Java/Spring Boot e Node.js.

### Connection pool (database/sql)

**Go tem pool built-in no `database/sql`:**

```go
import (
    "database/sql"
    _ "github.com/jackc/pgx/v5/stdlib"
)

db, err := sql.Open("pgx", "postgres://user:pass@localhost/db")
if err != nil {
    log.Fatal(err)
}

// Configurar pool
db.SetMaxOpenConns(25)           // máximo de conexões abertas
db.SetMaxIdleConns(10)           // máximo de idle connections
db.SetConnMaxLifetime(5 * time.Minute)  // reciclar conexões
db.SetConnMaxIdleTime(1 * time.Minute)  // fechar idle connections
```

**Monitorar:**

```go
stats := db.Stats()
log.Printf("Open: %d, InUse: %d, Idle: %d, WaitCount: %d, WaitDuration: %s",
    stats.OpenConnections, stats.InUse, stats.Idle,
    stats.WaitCount, stats.WaitDuration)

// Exportar para Prometheus
prometheus.MustRegister(prometheus.NewGaugeFunc(
    prometheus.GaugeOpts{Name: "db_open_connections"},
    func() float64 { return float64(db.Stats().OpenConnections) },
))
```

### N+1 queries

**Go não tem ORM lazy loading por default**, o que torna N+1 menos comum mas ainda possível:

```go
// RUIM — N+1 manual
doctors, _ := db.Query("SELECT id, name FROM doctors")
for doctors.Next() {
    var d Doctor
    doctors.Scan(&d.ID, &d.Name)
    // 1 query por doctor
    rows, _ := db.Query("SELECT * FROM appointments WHERE doctor_id = $1", d.ID)
    // ...
}

// BOM — JOIN
rows, _ := db.Query(`
    SELECT d.id, d.name, a.id, a.date
    FROM doctors d
    LEFT JOIN appointments a ON a.doctor_id = d.id
    WHERE d.active = true
`)

// BOM — sqlc (type-safe, gera Go code a partir de SQL)
// query.sql
// -- name: GetDoctorsWithAppointments :many
// SELECT d.*, a.* FROM doctors d
// LEFT JOIN appointments a ON a.doctor_id = d.id;

// BOM — GORM Preload
var doctors []Doctor
db.Preload("Appointments").Find(&doctors)
```

### Goroutine leak

**Equivalente a thread leak em Java ou event listener leak em Node.**

**Sintoma:** memória cresce lentamente, número de goroutines só aumenta.

**Diagnóstico com pprof:**

```go
import _ "net/http/pprof"

// Em outro terminal:
// go tool pprof http://localhost:6060/debug/pprof/goroutine
// (pprof) top
// (pprof) web  ← visualização gráfica

// Ou via código
fmt.Println("Goroutines:", runtime.NumGoroutine())
```

**Causas comuns:**
- Channel sem receiver (goroutine bloqueia em `ch <- data` para sempre)
- HTTP request sem timeout (goroutine espera response infinitamente)
- Context não cancelado

```go
// RUIM — goroutine vaza se ninguém lê do channel
go func() {
    result := expensiveComputation()
    ch <- result  // bloqueia para sempre se ninguém lê
}()

// BOM — usar context para cancelar
ctx, cancel := context.WithTimeout(context.Background(), 5*time.Second)
defer cancel()

go func() {
    select {
    case ch <- expensiveComputation():
    case <-ctx.Done():
        return  // goroutine liberada
    }
}()
```

### Memory profiling

```go
import "runtime/pprof"

// Heap profile
f, _ := os.Create("heap.prof")
pprof.WriteHeapProfile(f)
f.Close()

// Analisar
// go tool pprof heap.prof
// (pprof) top
// (pprof) list FunctionName
```

**`pprof` é uma das maiores vantagens de Go** — profiling de CPU, memória, goroutines, mutex contention, tudo built-in. Equivalente ao VisualVM/JFR do Java, mas sem precisar de ferramenta externa.

### API timeout e context propagation

**Go usa `context.Context` para timeout e cancelamento — propagado em toda a chain:**

```go
func (s *Server) HandleGetDoctor(w http.ResponseWriter, r *http.Request) {
    // Context do request — cancela se o client desconectar
    ctx := r.Context()

    // Timeout de 5s para a chamada ao banco
    ctx, cancel := context.WithTimeout(ctx, 5*time.Second)
    defer cancel()

    doctor, err := s.repo.FindByID(ctx, id)
    if err != nil {
        if errors.Is(err, context.DeadlineExceeded) {
            http.Error(w, "timeout", http.StatusGatewayTimeout)
            return
        }
        http.Error(w, "internal error", http.StatusInternalServerError)
        return
    }
    json.NewEncoder(w).Encode(doctor)
}
```

**Context se propaga naturalmente:** HTTP handler → service → repository → database driver. Se o client desconectar, o context é cancelado e todas as operações downstream param.

### Circuit breaker

```go
// Com gobreaker (Sony)
import "github.com/sony/gobreaker"

cb := gobreaker.NewCircuitBreaker(gobreaker.Settings{
    Name:        "external-api",
    MaxRequests: 3,                            // requests em half-open
    Interval:    10 * time.Second,             // janela de contagem
    Timeout:     30 * time.Second,             // tempo em open antes de half-open
    ReadyToTrip: func(counts gobreaker.Counts) bool {
        return counts.ConsecutiveFailures > 5  // abre após 5 falhas consecutivas
    },
})

result, err := cb.Execute(func() (interface{}, error) {
    return callExternalAPI()
})
```

### Cache stampede prevention

**Go tem `singleflight` na stdlib — resolve cache stampede de forma elegante:**

```go
import "golang.org/x/sync/singleflight"

var group singleflight.Group

func GetDoctor(ctx context.Context, id string) (*Doctor, error) {
    // Se 100 goroutines pedem o mesmo doctor ao mesmo tempo,
    // só 1 faz a query. As outras 99 esperam e recebem o mesmo resultado.
    result, err, _ := group.Do("doctor:"+id, func() (interface{}, error) {
        return repo.FindByID(ctx, id)
    })
    if err != nil {
        return nil, err
    }
    return result.(*Doctor), nil
}
```

**Equivalentes em outras stacks:**
- Java: cache lock com Redisson, ou Caffeine `AsyncLoadingCache`
- Node.js: promise caching (armazena a Promise, não o resultado)
- Python: dogpile.cache lock

### Graceful shutdown

```go
srv := &http.Server{Addr: ":8080", Handler: router}

// Iniciar servidor em goroutine
go func() {
    if err := srv.ListenAndServe(); err != http.ErrServerClosed {
        log.Fatal(err)
    }
}()

// Esperar sinal de shutdown
quit := make(chan os.Signal, 1)
signal.Notify(quit, syscall.SIGINT, syscall.SIGTERM)
<-quit

log.Println("Shutting down...")

// Contexto com timeout para graceful shutdown
ctx, cancel := context.WithTimeout(context.Background(), 30*time.Second)
defer cancel()

if err := srv.Shutdown(ctx); err != nil {
    log.Fatal("Forced shutdown:", err)
}
log.Println("Server stopped")
```

### Database migrations

```bash
# golang-migrate (equivalente ao Flyway)
migrate -path ./migrations -database "postgres://localhost/db" up

# Arquivos:
# migrations/000001_create_patients.up.sql
# migrations/000001_create_patients.down.sql
```

```go
// Ou programaticamente com goose
import "github.com/pressly/goose/v3"

func main() {
    db, _ := sql.Open("pgx", dsn)
    goose.Up(db, "migrations")
}
```

### Distributed tracing

```go
// OpenTelemetry para Go
import (
    "go.opentelemetry.io/otel"
    "go.opentelemetry.io/contrib/instrumentation/net/http/otelhttp"
)

// Instrumentar HTTP server
handler := otelhttp.NewHandler(router, "server")

// Instrumentar HTTP client
client := &http.Client{
    Transport: otelhttp.NewTransport(http.DefaultTransport),
}

// Context carrega trace automaticamente
func (s *Service) GetDoctor(ctx context.Context, id string) (*Doctor, error) {
    tracer := otel.Tracer("doctor-service")
    ctx, span := tracer.Start(ctx, "GetDoctor")
    defer span.End()

    return s.repo.FindByID(ctx, id)
}
```

→ Para comparação cross-stack: [[System Design]] (seção Problemas comuns em produção)

## How to explain in English

"Go is a language I appreciate for its simplicity and performance characteristics. What makes Go interesting for backend development is that many production concerns are addressed at the language level: goroutines provide lightweight concurrency without thread pool configuration, `context.Context` propagates timeouts and cancellation through the entire call chain, and `pprof` gives you CPU and memory profiling built-in.

Compared to Java, Go's approach is more explicit — there's no magic like Spring's proxy-based transactions. You manage connections, handle errors, and propagate context explicitly. This makes the code more verbose but also more predictable. The `database/sql` package includes connection pooling by default, and Go's `singleflight` package elegantly solves cache stampede — something that requires external libraries like Redisson in Java."

### Key vocabulary

- goroutine → goroutine (lightweight concurrent function)
- contexto → context (carries deadlines, cancellation, values)
- canal → channel (goroutine communication)
- perfilamento → profiling (pprof)
- binário estático → static binary

## Recursos

- [Go Documentation](https://go.dev/doc/) — documentação oficial
- [Effective Go](https://go.dev/doc/effective_go) — guia de estilo
- [Go by Example](https://gobyexample.com/) — exemplos práticos
- [sqlc](https://sqlc.dev/) — type-safe SQL code generation
- [Learn Go with Tests](https://quii.gitbook.io/learn-go-with-tests/) — TDD em Go
- [gobreaker (Sony)](https://github.com/sony/gobreaker) — circuit breaker

## Veja também

- [[System Design]] — troubleshooting cross-stack, building blocks
- [[API Design]]
- [[gRPC e Go]]
