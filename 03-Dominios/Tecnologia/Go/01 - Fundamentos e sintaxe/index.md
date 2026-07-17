---
title: "Go — Fundamentos e sintaxe"
type: moc
publish: true
created: 2026-07-16
updated: 2026-07-16
status: growing
tags:
  - moc
  - go
  - fundamentos
aliases:
  - Galho 1 Go
  - Fundamentos do Go
---
# Go — Fundamentos e sintaxe

> [!abstract] TL;DR
> Galho 1 da trilha [[03-Dominios/Tecnologia/Go/index|Go]] — a fundação da linguagem, do "por que o Go existe" até escrever código idiomático desde a primeira linha. 8 notas em 3 fases: dos fundamentos de compilação e sintaxe (Iniciado), passando por funções, pacotes e módulos (Adepto), até ponteiros/modelo de memória e o idioma do Go (Magus).

Este galho constrói o alicerce: ao fim dele, você compila e roda Go, entende zero values e conversões, domina o único loop e o idioma `if err != nil`, escreve funções com múltiplos retornos e closures, organiza código em pacotes e módulos, entende ponteiros sem aritmética, e sabe escrever Go que não parece "Java disfarçado". Ver [[roadmap]] pro estado das notas.

## Notas por fase

### Iniciado — a linguagem no papel

1. [[01 - O que é Go e o modelo de compilação]] — filosofia, compilação estática, binário autocontido, `go run` vs `go build`, primeiro programa
2. [[02 - Variáveis, tipos básicos e zero values]] — `var`/`:=`, tipos básicos, `const`/`iota`, zero values, conversão explícita
3. [[03 - Controle de fluxo]] — `if` com init, `for` (o único loop), `switch` sem fallthrough, `defer` (intro)

### Adepto — estruturando programas

4. [[04 - Funções]] — múltiplos retornos, named returns, variádicas, first-class functions, closures, `defer` a fundo
5. [[05 - Pacotes, imports e visibilidade]] — `package`, imports, visibilidade por capitalização, `init()`
6. [[06 - Módulos e o toolchain]] — `go.mod`/`go.sum`, `go mod init/tidy`, GOPATH→modules, toolchain embutido

### Magus — o que o sênior enxerga

7. [[07 - Ponteiros e o modelo de memória]] — `*T`/`&`/`*p`, pass-by-value, `new` vs `&T{}`, sem aritmética, escape analysis (teaser)
8. [[08 - Idiomático desde o início]] — gofmt como lei, convenções de nome, Go Proverbs, erros de quem vem de outra linguagem

## Veja também

- [[03-Dominios/Tecnologia/Go/index|Trilha Go]] — índice geral (21 galhos + capstone)
- Próximo galho: **Tipos, structs e métodos** (galho 2) — onde structs e métodos com receiver começam a construir o modelo de tipos do Go
