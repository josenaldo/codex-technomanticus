---
title: "Design — Trilha Go"
type: spec
created: 2026-07-16
updated: 2026-07-16
status: growing
publish: false
tags:
  - meta
  - spec
  - roadmap
  - go
aliases:
  - Design Trilha Go
  - Spec Go
---

# Design — Trilha Go

> [!abstract] TL;DR
> Construir a trilha **Go** em `03-Dominios/Tecnologia/Go/` como trilha completa "do zero" (escala Java/Python): **21 galhos + capstone**, notas atômicas em 3 fases (Iniciado/Adepto/Magus), padrão capítulo com lente cross-stack ("vindo de Java/Node/Python, em Go é assim"). Fecha o último backend sem trilha do grimório (Java 18 · Node 8 · Python 19 · **Go →**).

## Contexto e decisão de escopo

Go é o **último backend sem trilha atômica** do vault. Hoje existem só stubs: `Go Backend.md` (358 linhas, rico em troubleshooting de produção com lente cross-stack), `Go.md` (28 ln) e `index.md` (29 ln).

**Perfil-alvo:** Senior Fullstack (já sênior em Java, Node e Python), preparação para entrevistas internacionais remotas.

**Escopo escolhido — Opção A (trilha completa "do zero", escala Java/Python).** Rationale do usuário: começar cada linguagem como se fosse a primeira evita suposições que atrapalham, e produz material autossuficiente, fácil de retomar e compartilhar. Descartadas: Opção B ("Go para o poliglota", ~8-10 galhos enxutos) e Opção C (galho único).

**Fio condutor:** mesmo tratando Go como primeira linguagem, cada galho carrega a **lente cross-stack** como recurso didático (não como pré-requisito) — herdando o que o `Go Backend.md` já faz bem. O leitor não precisa saber Java/Node/Python, mas quem sabe ganha as pontes.

## Roster de galhos (21 + capstone)

### Bloco 1 — Fundamentos da linguagem
1. **Fundamentos e sintaxe** — modelo de compilação, tipos básicos, controle de fluxo, funções, `go run`/`go build`, zero values, pacote `main`.
2. **Tipos, structs e métodos** — value vs pointer semantics, structs, métodos, embedding; o que substitui "classe".
3. **Interfaces e composição** — interfaces implícitas, composição sobre herança, `any`/empty interface, type assertions/switch, "accept interfaces, return structs".
4. **Erros como valor** — `error`, wrapping, `errors.Is`/`errors.As`, sentinel errors, `panic`/`recover`, contraste com exceções.
5. **Coleções e dados** — slices (e seu modelo de memória: len/cap/aliasing), arrays, maps, strings/runes/bytes.
6. **Generics** — type parameters (1.18+), constraints, quando usar vs interfaces.

### Bloco 2 — Concorrência (o coração do Go)
7. **Goroutines e o scheduler** — concorrência vs paralelismo, o modelo GMP por cima, `go` statement, `GOMAXPROCS`.
8. **Channels e select** — buffered/unbuffered, direções, `select`, fan-in/fan-out, pipelines, close semantics.
9. **Sincronização e context** — `sync` (Mutex/RWMutex/WaitGroup/Once), `atomic`, race detector, `context.Context`, cancelamento/timeout, padrões de concorrência.

### Bloco 3 — Backend e serviços
10. **net/http e web frameworks** — handlers, middleware, roteamento, Gin/Chi/Echo, REST idiomático.
11. **Persistência** — `database/sql`, connection pool, pgx, sqlc, GORM, migrations (golang-migrate/goose).
12. **gRPC e protobuf** — Go como casa nativa; fronteira com a trilha [[03-Dominios/Engenharia/Comunicação entre Sistemas/index|Comunicação entre Sistemas]].
13. **Mensageria** — Kafka/NATS, workers, filas, padrões de consumo.
14. **Microservices e arquitetura** — project layout (`cmd`/`internal`/`pkg`), hexagonal/clean, DI (Wire), config (Viper).

### Bloco 4 — Produção e maestria
15. **Testes** — `go test`, table-driven, testify, mocks/interfaces, testes de integração, benchmarks, fuzzing.
16. **Observabilidade** — pprof, `slog`, expvar, OpenTelemetry, métricas (Prometheus).
17. **Runtime interno** — scheduler GMP a fundo, garbage collector, memory model, escape analysis (o par do "CPython internals").
18. **Cloud-native e produção** — build estático, cross-compile, distroless, Docker/K8s, graceful shutdown.
19. **Segurança** — crypto stdlib, validação de input, `govulncheck`, dependências, secure coding.

### Bloco 5 — Domínio e entrevista
20. **Go idiomático** — Effective Go, composição idiomática, erros comuns de quem vem de Java/Node/Python, `go vet`/linters (golangci-lint), code review.
21. **Preparação para entrevista de Go** — perguntas clássicas, live coding, gotchas (nil interfaces, slice aliasing, loop variable capture pré-1.22, defer em loop, etc.).

### Capstone
- **Construir um serviço Go de produção do zero** — costura os 21 galhos: API + gRPC + persistência + concorrência + observabilidade + deploy cloud-native, conduzindo a decisão como um sênior.

## Deltas conscientes vs Java/Python

| Delta | Racional |
|-------|----------|
| **Funde** Concorrência + Async num só bloco (galhos 7-9) | Go não tem async/await — a goroutine *é* o modelo de concorrência. |
| **Adiciona** galho de Generics (6) | Novidade da linguagem (1.18+), cai em entrevista. |
| **Adiciona** galhos "Go idiomático" (20) + "Preparação para entrevista" (21) no lugar da certificação | Go **não tem certificação padrão** reconhecida (não existe OCP/PCEP do Go). Escrever Go que não pareça "Java escrito em Go" é o ganho real; drills de entrevista alimentam o capstone. |
| **Runtime interno** (17) = par do "CPython internals" | Scheduler/GC/memory model são diferencial sênior e caem em entrevista. |

## Convenções de construção (herdadas do vault)

- **Local:** `03-Dominios/Tecnologia/Go/`, galhos flat numerados (`01 - ...` a `21 - ...`).
- **Fases:** cada galho em Iniciado/Adepto/Magus — `fase:` no frontmatter + MOC agrupado. Média ~8 notas/galho → escala Java/Python (~170 notas no total, ao longo de muitas sessões).
- **Padrão capítulo:** cada nota lê como capítulo que pega o leitor pela mão — TL;DR (`[!abstract]`) → abertura-problema → mecanismo com Mermaid → casos práticos → armadilhas comuns (`[!warning]`) → "O que vem a seguir" (bridge narrativo) → Fontes. Registro Feynman (analogias, perguntas retóricas, resumo em 1 linha). Piso por fase onde o galho adota fases (Iniciado ≥300 / Adepto ≥400 / Magus ≥500), subordinado ao padrão capítulo.
- **Lente cross-stack:** callouts/tabelas PT↔"equivalente Java/Node/Python" como recurso, não como dependência.
- **Roadmap tree:** `roadmap.md` recursivo (raiz da trilha → cada galho), template `00-Meta/templates/Template - Roadmap.md`.
- **Skills:** `/escrever-nota` para notas novas, `/verificar-nota` como gate, `/enriquecer-nota` na passada de enriquecimento; `/diagnosticar-galho` gera os roadmaps.

## Poda dos stubs existentes

- **`Go Backend.md`** (rico) → vira tronco podado. Conteúdo de troubleshooting migra pros galhos certos, com callouts apontando pra lá:
  - connection pool / `database/sql` → galho **11** (Persistência)
  - goroutine leak / `singleflight` / context → galho **9** (Sincronização e context)
  - circuit breaker → galho **14** (Microservices) ou **13** (Mensageria)
  - pprof / memory profiling → galho **16** (Observabilidade)
  - graceful shutdown → galho **18** (Cloud-native e produção)
  - distributed tracing (OTel) → galho **16** (Observabilidade)
- **`Go.md`** / **`index.md`** → consolidados no MOC da trilha (`index.md` é o MOC; não remover — regra Quartz).

## Execução

- **Um galho por vez**, direto na `main` (sem branch dedicada, como Java a partir do galho 6). Push manual.
- **Ordem:** galho 1 → 21 → capstone, respeitando os blocos (fundamentos antes de concorrência antes de serviços antes de produção).
- **Governança de tokens:** notas escritas por sessão em lote razoável; parada/checkpoint conforme necessário. Fan-out de pesquisa limitado (inline ou ≤2-3 agentes haiku).

## Atualizações de rastreio ao concluir

- Mover Go de 🚫/⬜ Tier 1 para ✅ no [[00-Meta/Roadmap|Roadmap mestre]] (Backend/Runtime + backlog).
- Registrar na memória (`project_trilha_go.md` + índice `MEMORY.md`).

## Não-objetivos (YAGNI)

- **Não** cobrir toda a stdlib exaustivamente — só o que serve backend/entrevista/produção.
- **Não** criar galho de certificação (não existe padrão).
- **Não** duplicar conteúdo já coberto conceitualmente em outras trilhas (System Design, Comunicação, Operação) — linkar via fronteira, não reexplicar.
