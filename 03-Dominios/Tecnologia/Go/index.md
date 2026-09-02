---
title: "Go"
type: moc
publish: true
created: 2026-05-21
updated: 2026-07-16
status: complete
tags:
  - moc
  - go
aliases:
  - Estante Go
  - Golang
---
# Go

> [!abstract] TL;DR
> Trilha Go organizada em **21 galhos + capstone**, do zero até produção — construída como se Go fosse a primeira linguagem (sem suposições), no mesmo padrão das trilhas [[03-Dominios/Tecnologia/Java/index|Java]] e [[03-Dominios/Tecnologia/Python/index|Python]]. Cada galho é um conjunto de notas atômicas em 3 fases (Iniciado/Adepto/Magus), com uma **lente cross-stack** ("vindo de Java/Node/Python, em Go é assim") como recurso didático.

Go aparece aqui como linguagem compilada, estaticamente tipada e orientada a concorrência, com binários autocontidos e stdlib forte — a linguagem do mundo cloud-native (Docker, Kubernetes, Terraform são escritos nela).

## Galhos da trilha

### Bloco 1 — Fundamentos da linguagem

1. ✅ [[03-Dominios/Tecnologia/Go/01 - Fundamentos e sintaxe/index|Fundamentos e sintaxe]] — modelo de compilação, tipos básicos, controle de fluxo, funções, pacotes/módulos, ponteiros, idiomático (8 notas, 2026-07-16)
2. ✅ [[03-Dominios/Tecnologia/Go/02 - Tipos, structs e métodos/index|Tipos, structs e métodos]] — value vs pointer semantics, embedding, o que substitui "classe" (8 notas, 2026-07-16)
3. ✅ [[03-Dominios/Tecnologia/Go/03 - Interfaces e composição/index|Interfaces e composição]] — interfaces implícitas, composição sobre herança, type assertions/switch, typed-nil (8 notas)
4. ✅ [[03-Dominios/Tecnologia/Go/04 - Erros como valor/index|Erros como valor]] — `error`, wrapping, `errors.Is/As`, sentinel, `panic`/`recover` (8 notas)
5. ✅ [[03-Dominios/Tecnologia/Go/05 - Coleções e dados/index|Coleções e dados]] — slices (e seu modelo de memória), arrays, maps, strings/runes/bytes (8 notas)
6. ✅ [[03-Dominios/Tecnologia/Go/06 - Generics/index|Generics]] — type parameters (1.18+), constraints, quando usar (7 notas)

### Bloco 2 — Concorrência (o coração do Go)

7. ✅ [[03-Dominios/Tecnologia/Go/07 - Goroutines e o scheduler/index|Goroutines e o scheduler]] — concorrência vs paralelismo, modelo GMP (8 notas)
8. ✅ [[03-Dominios/Tecnologia/Go/08 - Channels e select/index|Channels e select]] — buffered/unbuffered, fan-in/fan-out, pipelines (8 notas)
9. ✅ [[03-Dominios/Tecnologia/Go/09 - Sincronização e context/index|Sincronização e context]] — `sync`, `atomic`, race detector, `context.Context` (8 notas)

### Bloco 3 — Backend e serviços

10. ✅ [[03-Dominios/Tecnologia/Go/10 - HTTP e frameworks web/index|HTTP e frameworks web]] — handlers, middleware, Gin/Chi/Echo (8 notas)
11. ✅ [[03-Dominios/Tecnologia/Go/11 - Persistência/index|Persistência]] — `database/sql`, pool, pgx, sqlc, GORM, migrations (8 notas)
12. ✅ [[03-Dominios/Tecnologia/Go/12 - gRPC e protobuf/index|gRPC e protobuf]] — Go como casa nativa (7 notas)
13. ✅ [[03-Dominios/Tecnologia/Go/13 - Mensageria/index|Mensageria]] — Kafka/NATS, workers, filas (7 notas)
14. ✅ [[03-Dominios/Tecnologia/Go/14 - Microservices e arquitetura/index|Microservices e arquitetura]] — project layout, hexagonal, DI (Wire) (8 notas)

### Bloco 4 — Produção e maestria

15. ✅ [[03-Dominios/Tecnologia/Go/15 - Testes/index|Testes]] — `go test`, table-driven, testify, benchmarks, fuzzing (8 notas)
16. ✅ [[03-Dominios/Tecnologia/Go/16 - Observabilidade/index|Observabilidade]] — pprof, `slog`, expvar, OTel, métricas (8 notas)
17. ✅ [[03-Dominios/Tecnologia/Go/17 - Runtime interno/index|Runtime interno]] — scheduler GMP a fundo, GC, memory model, escape analysis (8 notas)
18. ✅ [[03-Dominios/Tecnologia/Go/18 - Cloud-native e produção/index|Cloud-native e produção]] — build estático, cross-compile, distroless, Docker/K8s (8 notas)
19. ✅ [[03-Dominios/Tecnologia/Go/19 - Segurança/index|Segurança]] — crypto stdlib, validação, `govulncheck`, secure coding (8 notas)

### Bloco 5 — Domínio e entrevista

20. ✅ [[03-Dominios/Tecnologia/Go/20 - Go idiomático/index|Go idiomático]] — Effective Go, erros comuns de quem vem de outra linguagem, linters (7 notas)
21. ✅ [[03-Dominios/Tecnologia/Go/21 - Preparação para entrevista de Go/index|Preparação para entrevista de Go]] — perguntas clássicas, live coding, gotchas (7 notas)

### Capstone

- ✅ [[03-Dominios/Tecnologia/Go/Capstone - Construir um serviço Go de produção|Construir um serviço Go de produção do zero]] — costura os 21 galhos (API + gRPC + persistência + concorrência + observabilidade + deploy)

## Veja também

- [[03-Dominios/Tecnologia/Java/index|Java]] · [[03-Dominios/Tecnologia/Python/index|Python]] · [[03-Dominios/Tecnologia/Node/index|Node]] — trilhas irmãs, mesmo padrão estrutural
- [[03-Dominios/Engenharia/Comunicação entre Sistemas/index|Comunicação entre Sistemas]] — gRPC (galho 12) é cidadão nativo do ecossistema Go
- [[Senda Go]] — recursos externos (cursos/vídeos/livros) usados como pesquisa prévia
