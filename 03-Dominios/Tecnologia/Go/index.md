---
title: "Go"
type: moc
publish: true
created: 2026-05-21
updated: 2026-07-16
status: growing
tags:
  - moc
  - go
aliases:
  - Estante Go
  - Golang
---
# Go

> [!abstract] TL;DR
> Trilha Go organizada em **21 galhos + capstone**, do zero até produção — construída como se Go fosse a primeira linguagem (sem suposições), no mesmo padrão das trilhas [[03-Dominios/Tecnologia/Java/index|Java]] e [[03-Dominios/Tecnologia/Python/index|Python]]. Cada galho é um conjunto de notas atômicas em 3 fases (Iniciado/Adepto/Magus), padrão capítulo, com uma **lente cross-stack** ("vindo de Java/Node/Python, em Go é assim") como recurso didático. Fecha o último backend sem trilha do grimório. **EM CONSTRUÇÃO** — semeando a partir de [[00-Meta/specs/2026-07-16-trilha-go-design|Design]] + [[00-Meta/specs/2026-07-16-trilha-go-plano|Plano]].

Go aparece aqui como linguagem compilada, estaticamente tipada e orientada a concorrência, com binários autocontidos e stdlib forte — a linguagem do mundo cloud-native (Docker, Kubernetes, Terraform são escritos nela). Ver [[roadmap]] pro estado de cada galho.

> [!info] Trilha em construção
> Os wikilinks de cada galho aparecem conforme ele é escrito. Galhos ⬜ ainda não existem como pasta.

## Galhos da trilha

### Bloco 1 — Fundamentos da linguagem

1. ⬜ **Fundamentos e sintaxe** — modelo de compilação, tipos básicos, controle de fluxo, funções, pacotes/módulos, ponteiros, idiomático
2. ⬜ **Tipos, structs e métodos** — value vs pointer semantics, embedding, o que substitui "classe"
3. ⬜ **Interfaces e composição** — interfaces implícitas, composição sobre herança, type assertions/switch
4. ⬜ **Erros como valor** — `error`, wrapping, `errors.Is/As`, sentinel, `panic`/`recover`
5. ⬜ **Coleções e dados** — slices (e seu modelo de memória), arrays, maps, strings/runes/bytes
6. ⬜ **Generics** — type parameters (1.18+), constraints, quando usar

### Bloco 2 — Concorrência (o coração do Go)

7. ⬜ **Goroutines e o scheduler** — concorrência vs paralelismo, modelo GMP
8. ⬜ **Channels e select** — buffered/unbuffered, fan-in/fan-out, pipelines
9. ⬜ **Sincronização e context** — `sync`, `atomic`, race detector, `context.Context`

### Bloco 3 — Backend e serviços

10. ⬜ **net/http e web frameworks** — handlers, middleware, Gin/Chi/Echo
11. ⬜ **Persistência** — `database/sql`, pool, pgx, sqlc, GORM, migrations
12. ⬜ **gRPC e protobuf** — Go como casa nativa
13. ⬜ **Mensageria** — Kafka/NATS, workers, filas
14. ⬜ **Microservices e arquitetura** — project layout, hexagonal, DI (Wire)

### Bloco 4 — Produção e maestria

15. ⬜ **Testes** — `go test`, table-driven, testify, benchmarks, fuzzing
16. ⬜ **Observabilidade** — pprof, `slog`, expvar, OTel, métricas
17. ⬜ **Runtime interno** — scheduler GMP a fundo, GC, memory model, escape analysis
18. ⬜ **Cloud-native e produção** — build estático, cross-compile, distroless, Docker/K8s
19. ⬜ **Segurança** — crypto stdlib, validação, `govulncheck`, secure coding

### Bloco 5 — Domínio e entrevista

20. ⬜ **Go idiomático** — Effective Go, erros comuns de quem vem de outra linguagem, linters
21. ⬜ **Preparação para entrevista de Go** — perguntas clássicas, live coding, gotchas

### Capstone

- ⬜ **Construir um serviço Go de produção do zero** — costura os 21 galhos

## Veja também

- [[03-Dominios/Tecnologia/Java/index|Java]] · [[03-Dominios/Tecnologia/Python/index|Python]] · [[03-Dominios/Tecnologia/Node/index|Node]] — trilhas irmãs, mesmo padrão estrutural
- [[03-Dominios/Engenharia/Comunicação entre Sistemas/index|Comunicação entre Sistemas]] — gRPC (galho 12) é cidadão nativo do ecossistema Go
- [[Senda Go]] — recursos externos (cursos/vídeos/livros) usados como pesquisa prévia
