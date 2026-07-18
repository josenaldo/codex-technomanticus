---
title: "Go — Testes"
type: moc
publish: true
created: 2026-07-18
updated: 2026-07-18
status: growing
tags:
  - moc
  - go
  - testes
  - testing
aliases:
  - Galho 15 Go
  - Testes em Go
---
# Go — Testes

> [!abstract] TL;DR
> Galho 15 da trilha [[03-Dominios/Tecnologia/Go/index|Go]] — testar é cidadão de primeira classe da toolchain, não um add-on. 8 notas em 3 fases: o primeiro `_test.go` e o idioma table-driven (Iniciado); testify, test doubles via interface e testes de integração (Adepto); benchmarks, fuzzing e cobertura idiomática (Magus). Ao fim, você escreve testes que a comunidade Go reconhece como idiomáticos — table-driven, sem framework pesado, apoiados nas interfaces do galho 3.

O `go test` vem na caixa, e a cultura de testes de Go é enxuta: table-driven por padrão, mocks via interface, e ceticismo saudável com frameworks. Ver [[roadmap]] pro estado das notas.

## Notas por fase

### Iniciado — o básico da toolchain

1. [[01 - go test e o primeiro teste]] — arquivos `_test.go`, `TestXxx(t *testing.T)`, `go test ./...`, `t.Error`/`t.Fatal`
2. [[02 - Table-driven tests]] — o idioma central: slice de casos + `t.Run`, subtests nomeados

### Adepto — ferramentas e isolamento

3. [[03 - Testify e asserções]] — `assert` vs `require`, quando a stdlib basta, o debate "sem framework"
4. [[04 - Test doubles — interfaces e mocks]] — mockar via interface, gomock/mockery, injetar fakes
5. [[05 - Testes de integração]] — build tags, `httptest`, testcontainers-go, separar unit de integração

### Magus — medir e cobrir

6. [[06 - Benchmarks]] — `BenchmarkXxx(b *testing.B)`, `b.N`, benchstat, medir antes de otimizar
7. [[07 - Fuzzing]] — `FuzzXxx(f *testing.F)` (1.18), corpus, achar edge cases automaticamente
8. [[08 - Cobertura e testes idiomáticos]] — `-cover`, o que não testar, TDD em Go, testes como documentação

## Veja também

- [[03-Dominios/Tecnologia/Go/index|Trilha Go]] — índice geral (21 galhos + capstone)
- Galho anterior: [[03-Dominios/Tecnologia/Go/14 - Microservices e arquitetura/index|Microservices e arquitetura]]
- Próximo galho: **Observabilidade** (galho 16) — instrumentar o serviço para enxergar o que acontece em produção
