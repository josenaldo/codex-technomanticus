---
title: "Go — Coleções e dados"
type: moc
publish: true
created: 2026-07-18
updated: 2026-07-18
status: growing
tags:
  - moc
  - go
  - slices
  - maps
  - colecoes
aliases:
  - Galho 5 Go
---
# Go — Coleções e dados

> [!abstract] TL;DR
> Galho 5 da trilha [[03-Dominios/Tecnologia/Go/index|Go]] — como Go representa coleções e texto sem generics de biblioteca nem classes de coleção. 8 notas em 3 fases: arrays, slices e maps (Iniciado); strings/runes/bytes, o modelo de memória de slices (len/cap/aliasing) e alocação com make/new (Adepto); ordenação/busca idiomáticas e o critério pra escolher a estrutura certa (Magus). Ao fim, você entende por que slice não é array, por que passar slice por valor ainda pode mutar o backing array, e quando isso importa.

Go não tem `List`, `Set` ou `ArrayList` — tem arrays de tamanho fixo, slices (a estrutura que você usa 95% do tempo) e maps, todos com semânticas de memória bem específicas que mordem quem vem de linguagens com coleções mais opacas. Ver [[roadmap]] pro estado das notas.

## Notas por fase

### Iniciado — as três estruturas

1. [[01 - Arrays e o modelo de valor]] — tamanho no tipo, cópia por valor, por que raramente se usa array direto
2. [[02 - Slices — o cavalo de batalha]] — header (ponteiro/len/cap), slicing, `append`, growth strategy
3. [[03 - Maps]] — declaração, zero value nil, comma ok, iteração não ordenada, maps como set

### Adepto — memória e alocação

4. [[04 - Strings, runes e bytes]] — UTF-8 por padrão, `string` vs `[]byte` vs `[]rune`, indexação por byte
5. [[05 - O modelo de memória de slices — len, cap e aliasing]] — backing array compartilhado, aliasing surpresa, `copy`, slice de slice
6. [[06 - make, new e alocação]] — `make` pra slice/map/channel, `new` pra ponteiro zerado, pré-alocação com capacity

### Magus — uso idiomático

7. [[07 - Ordenação e busca com slices e sort]] — `sort.Slice`, `slices.Sort` (stdlib genérica), busca binária
8. [[08 - Escolhendo a estrutura de dados certa]] — slice vs map vs struct, quando modelar set, trade-offs de performance

## Veja também

- [[03-Dominios/Tecnologia/Go/index|Trilha Go]] — índice geral (21 galhos + capstone)
- Galho anterior: [[03-Dominios/Tecnologia/Go/04 - Erros como valor/index|Erros como valor]]
- Próximo galho: **Generics** (galho 6) — onde essas mesmas estruturas ganham parametrização de tipo
