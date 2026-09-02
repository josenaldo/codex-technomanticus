---
title: "Go — Interfaces e composição"
type: moc
publish: true
created: 2026-07-18
updated: 2026-07-18
status: growing
tags:
  - moc
  - go
  - interfaces
  - composicao
aliases:
  - Galho 3 Go
---
# Go — Interfaces e composição

> [!abstract] TL;DR
> Galho 3 da trilha [[03-Dominios/Tecnologia/Go/index|Go]] — como Go faz polimorfismo sem herança: interfaces implícitas (satisfação estrutural), o `any`/type assertions e o idioma "accept interfaces, return structs" (Iniciado/Adepto); embedding de interfaces e as pegadinhas de `io.Reader`/`io.Writer` (Adepto); o nil interface/typed-nil e design idiomático de interfaces pequenas (Magus). Ao fim, você projeta contratos desacoplados do tipo concreto — o jeito Go de fazer abstração.

Aqui o Go completa a aposta do galho 2: comportamento vem de métodos, e contratos vêm de interfaces satisfeitas implicitamente — sem `implements`, sem hierarquia declarada.

## Notas por fase

### Iniciado — o contrato implícito

1. [[01 - Interfaces implícitas e satisfação estrutural]] — sem `implements`, duck typing estático, satisfação por método set
2. [[02 - O empty interface e any]] — `interface{}`/`any`, quando (não) usar, custo de boxing
3. [[03 - Type assertions e type switch]] — `v, ok := x.(T)`, `switch v := x.(type)`, panics evitáveis

### Adepto — o idioma das interfaces

4. [[04 - Accept interfaces, return structs]] — por que essa regra, exceções, acoplamento em construtores
5. [[05 - Interfaces pequenas — io.Reader e io.Writer]] — o padrão stdlib, interfaces de um método, composabilidade
6. [[06 - Interface embedding]] — compor interfaces maiores a partir de menores, `io.ReadWriter`

### Magus — design idiomático

7. [[07 - O nil interface e o typed-nil]] — a armadilha clássica, `(*T)(nil)` dentro de uma interface não-nil
8. [[08 - Design idiomático de interfaces]] — definir no consumidor, interfaces mínimas, quando NÃO criar uma interface

## Veja também

- [[03-Dominios/Tecnologia/Go/index|Trilha Go]] — índice geral (21 galhos + capstone)
- Galho anterior: [[03-Dominios/Tecnologia/Go/02 - Tipos, structs e métodos/index|Tipos, structs e métodos]]
- Próximo galho: **Erros como valor** (galho 4) — `error`, wrapping, `errors.Is/As`, `panic`/`recover`
