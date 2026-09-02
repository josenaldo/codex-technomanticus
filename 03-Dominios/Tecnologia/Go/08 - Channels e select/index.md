---
title: "Go — Channels e select"
type: moc
publish: true
created: 2026-07-18
updated: 2026-07-18
status: growing
tags:
  - moc
  - go
  - concorrencia
  - channels
aliases:
  - Galho 8 Go
---
# Go — Channels e select

> [!abstract] TL;DR
> Galho 8 da trilha [[03-Dominios/Tecnologia/Go/index|Go]] — o mecanismo que dá nome ao lema "não comunique compartilhando memória; compartilhe memória comunicando". 8 notas em 3 fases: o channel como tubo entre goroutines e buffered vs unbuffered (Iniciado); fechamento com `range`, direções de channel e `select` (Adepto); padrões de composição (fan-in/fan-out/pipeline), worker pools e as armadilhas clássicas — deadlock, leak, panic de close duplo (Magus). Ao fim, você orquestra goroutines com channels em vez de mutexes.

Depois de dominar goroutines no galho anterior, este galho entra no meio de comunicação idiomático do Go: o channel. É a estrutura que sincroniza, transporta dados e sinaliza término entre goroutines concorrentes, e o `select` é o multiplexador que espera em vários channels ao mesmo tempo.

## Notas por fase

### Iniciado — o tubo e suas variantes

1. [[01 - Channels — o tubo entre goroutines]] — criação, envio, recebimento, bloqueio e o modelo mental de tubo
2. [[02 - Buffered vs unbuffered]] — capacidade, rendezvous síncrono vs desacoplamento assíncrono

### Adepto — controlando o fluxo

3. [[03 - Fechando channels e o range]] — `close`, o segundo valor de recebimento, iterar com `range`
4. [[04 - Direções de channel]] — `chan<-`, `<-chan`, contratos de API mais seguros em assinaturas de função
5. [[05 - select]] — multiplexar channels, `default`, timeout com `time.After`, `select` vazio

### Magus — composição e armadilhas

6. [[06 - Padrões — fan-in, fan-out, pipeline]] — distribuir trabalho, consolidar resultados, encadear estágios
7. [[07 - Worker pools]] — pool de goroutines consumindo de um channel compartilhado, controle de concorrência
8. [[08 - Armadilhas de channels]] — deadlock, goroutine leak, close de channel já fechado, send em channel fechado

## Veja também

- [[03-Dominios/Tecnologia/Go/index|Trilha Go]] — índice geral (21 galhos + capstone)
- Galho anterior: [[03-Dominios/Tecnologia/Go/07 - Goroutines e o scheduler/index|Goroutines e o scheduler]]
- Próximo galho: **Sincronização e context** (galho 9) — onde `sync` e `context` cobrem os casos que channels sozinhos não resolvem bem
