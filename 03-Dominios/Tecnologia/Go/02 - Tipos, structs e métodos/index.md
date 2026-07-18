---
title: "Go — Tipos, structs e métodos"
type: moc
publish: true
created: 2026-07-16
updated: 2026-07-16
status: growing
tags:
  - moc
  - go
  - tipos
aliases:
  - Galho 2 Go
  - Structs e métodos Go
---
# Go — Tipos, structs e métodos

> [!abstract] TL;DR
> Galho 2 da trilha [[03-Dominios/Tecnologia/Go/index|Go]] — o modelo de tipos que substitui a "classe". 8 notas em 3 fases: structs, tipos nomeados e métodos (Iniciado); a decisão value vs pointer receiver, composição por embedding e o idioma do construtor (Adepto); struct tags/reflection e design de tipos idiomático (Magus). Ao fim, você modela dados e comportamento em Go sem herança — só composição.

Aqui o Go mostra sua aposta central de design: **sem classes, sem herança** — dados vivem em structs, comportamento vem de métodos com receiver, e reúso vem de composição por embedding. Ver [[roadmap]] pro estado das notas.

## Notas por fase

### Iniciado — os blocos de construção

1. [[01 - Structs — definição e inicialização]] — declarar struct, literais, zero value, aninhados, comparabilidade
2. [[02 - Tipos nomeados e definições de tipo]] — `type T Underlying`, type safety, aliases vs defined types
3. [[03 - Métodos]] — funções com receiver, métodos em qualquer tipo nomeado, method value/expression

### Adepto — modelando comportamento

4. [[04 - Value vs pointer receiver]] — cópia vs mutação, method sets, addressability, regra de consistência
5. [[05 - Composição por embedding]] — campo anônimo, promoção de métodos, composição sobre herança
6. [[06 - O idioma do construtor]] — sem construtores; `NewXxx`, zero value útil, functional options (intro)

### Magus — design de tipos

7. [[07 - Struct tags e reflection básica]] — tags, `reflect`, o caso `encoding/json`, quando não refletir
8. [[08 - Design de tipos idiomático]] — value vs reference semantics, imutabilidade por convenção, `struct{}` vazio

## Veja também

- [[03-Dominios/Tecnologia/Go/index|Trilha Go]] — índice geral (21 galhos + capstone)
- Galho anterior: [[03-Dominios/Tecnologia/Go/01 - Fundamentos e sintaxe/index|Fundamentos e sintaxe]]
- Próximo galho: **Interfaces e composição** (galho 3) — onde o comportamento vira contrato desacoplado do tipo concreto
