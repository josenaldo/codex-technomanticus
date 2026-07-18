---
title: "Go — Generics"
type: moc
publish: true
created: 2026-07-18
updated: 2026-07-18
status: growing
tags:
  - moc
  - go
  - generics
  - type-parameters
aliases:
  - Galho 6 Go
---
# Go — Generics

> [!abstract] TL;DR
> Galho 6 da trilha [[03-Dominios/Tecnologia/Go/index|Go]] — o recurso mais recente e mais debatido da linguagem. 7 notas em 3 fases: o problema que existia antes do Go 1.18 e a sintaxe de type parameters (Iniciado); constraints, tipos genéricos e type inference (Adepto); a fronteira generics vs interfaces e os padrões/limites reais de uso em produção (Magus). Ao fim, você sabe quando generics resolve algo que interface não resolve — e quando é só complexidade extra.

Generics chegou tarde ao Go (1.18, 2022) de propósito: a linguagem preferiu esperar por um design que não sacrificasse simplicidade de leitura por abstração. Este galho cobre a sintaxe, as constraints que substituem `interface{}` com segurança de tipo, e — o mais importante — o julgamento de quando usar generics em vez do idioma de interfaces já visto no galho 3. Ver [[roadmap]] pro estado das notas.

## Notas por fase

### Iniciado — o problema e a sintaxe

1. [[01 - Por que generics — o problema antes de 1.18]] — duplicação de código por tipo, `interface{}` + type assertion, `go generate`, o que motivou a proposta
2. [[02 - Type parameters — a sintaxe]] — `[T any]`, funções genéricas, instanciação explícita vs inferida

### Adepto — constraints e tipos genéricos

3. [[03 - Constraints]] — `constraints.Ordered`, interfaces como constraint, union de tipos, `~` para underlying types
4. [[04 - Tipos genéricos]] — structs e tipos genéricos, métodos em tipos genéricos, estruturas de dados (stack, lista ligada)
5. [[05 - Type inference]] — quando o compilador infere, quando exige anotação explícita, limites da inferência

### Magus — julgamento de uso

6. [[06 - Generics vs interfaces — quando usar cada um]] — polimorfismo de comportamento (interface) vs polimorfismo de dado (generics), critérios de decisão
7. [[07 - Padrões e limites dos generics]] — slices/maps utilitários genéricos, o que a stdlib fez (`slices`, `maps`), armadilhas e over-engineering

## Veja também

- [[03-Dominios/Tecnologia/Go/index|Trilha Go]] — índice geral (21 galhos + capstone)
- Galho anterior: [[03-Dominios/Tecnologia/Go/05 - Coleções e dados/index|Coleções e dados]]
- Próximo galho: **Goroutines e o scheduler** (galho 7) — onde a trilha entra em concorrência, o outro grande diferencial de Go
