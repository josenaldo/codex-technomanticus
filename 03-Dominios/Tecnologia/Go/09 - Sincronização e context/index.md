---
title: "Go — Sincronização e context"
type: moc
publish: true
created: 2026-07-18
updated: 2026-07-18
status: growing
tags:
  - moc
  - go
  - concorrencia
  - sync
  - context
aliases:
  - Galho 9 Go
---
# Go — Sincronização e context

> [!abstract] TL;DR
> Galho 9 da trilha [[03-Dominios/Tecnologia/Go/index|Go]] — o outro lado da concorrência: quando channels não são a ferramenta certa, e como cancelar e coordenar trabalho de forma disciplinada. 8 notas em 3 fases: `sync.Mutex`/`RWMutex` (Iniciado); `WaitGroup`, `Once`, `atomic`, o race detector e `context.Context` (Adepto); padrões de cancelamento/timeout e concorrência idiomática (Magus). Ao fim, você sabe escolher entre memória compartilhada protegida e comunicação por canal — e propagar cancelamento pela árvore de goroutines sem vazar nenhuma.

Depois dos galhos 7 e 8 (goroutines, channels e select), este galho completa o ferramental de concorrência do Go: o pacote `sync` para proteger estado compartilhado quando um channel seria overkill, e `context.Context` — o mecanismo canônico do Go para propagar deadline, cancelamento e valores através de chamadas concorrentes. Ver [[roadmap]] pro estado das notas.

## Notas por fase

### Iniciado — memória compartilhada protegida

1. [[01 - Quando channels não bastam — o pacote sync]] — o trade-off "share memory by communicating" vs proteger estado direto, quando cada abordagem vence
2. [[02 - Mutex e RWMutex]] — exclusão mútua, `sync.Mutex`, `sync.RWMutex` para leituras concorrentes, deadlocks comuns

### Adepto — coordenação e visibilidade

3. [[03 - WaitGroup e Once]] — esperar N goroutines terminarem, inicialização única e thread-safe
4. [[04 - atomic e sync-atomic]] — operações atômicas de baixo nível, quando preferir a um mutex, `atomic.Value`/tipos genéricos
5. [[05 - O race detector]] — `go run -race`, o que ele detecta e o que não detecta, disciplina de CI
6. [[06 - context.Context — deadline, cancel, values]] — a interface `Context`, `WithCancel`/`WithTimeout`/`WithDeadline`, `context.Value` e seus limites

### Magus — padrões de produção

7. [[07 - Padrões de cancelamento e timeout]] — propagação de cancelamento pela árvore de goroutines, evitar vazamento, `errgroup`
8. [[08 - Padrões de concorrência idiomáticos]] — pipeline, fan-out/fan-in, worker pool, e quando NÃO usar concorrência

## Veja também

- [[03-Dominios/Tecnologia/Go/index|Trilha Go]] — índice geral (21 galhos + capstone)
- Galho anterior: [[03-Dominios/Tecnologia/Go/08 - Channels e select/index|Channels e select]]
- Próximo galho: **HTTP e frameworks web** (galho 10) — onde concorrência e context viram a espinha dorsal de todo handler de produção
