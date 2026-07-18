---
title: "Go — Goroutines e o scheduler"
type: moc
publish: true
created: 2026-07-18
updated: 2026-07-18
status: growing
tags:
  - moc
  - go
  - concorrencia
  - goroutines
  - scheduler
aliases:
  - Galho 7 Go
---
# Go — Goroutines e o scheduler

> [!abstract] TL;DR
> Galho 7 da trilha [[03-Dominios/Tecnologia/Go/index|Go]] — a unidade de concorrência que faz do Go um caso à parte entre linguagens de backend. 8 notas em 3 fases: o vocabulário concorrência-vs-paralelismo e o `go` statement (Iniciado); o modelo GMP por baixo do capô, o ciclo de vida de uma goroutine e o mantra "compartilhe memória comunicando" comparado a threads/event loop/GIL (Adepto); as armadilhas clássicas de leak e captura de variável de loop, e o julgamento de quando goroutines são a ferramenta certa (Magus). Ao fim, você entende não só como lançar uma goroutine, mas por que o scheduler do Go faz isso ser barato — e onde isso ainda pode dar errado.

Goroutines são a resposta do Go para "como fazer concorrência sem forçar o programador a orquestrar threads do SO". Custam ~2KB de stack, o runtime multiplexa milhares delas sobre um punhado de threads via o scheduler M:N, e o idioma da linguagem empurra você a comunicar por canais em vez de proteger memória compartilhada com locks. Ver [[roadmap]] pro estado das notas.

## Notas por fase

### Iniciado — o vocabulário e o gatilho

1. [[01 - Concorrência vs paralelismo]] — a distinção de Rob Pike, por que Go foi desenhado em torno dela
2. [[02 - A goroutine — o go statement]] — sintaxe, o que acontece ao lançar, custo de stack, `main` não espera

### Adepto — o motor por baixo

3. [[03 - O modelo GMP por cima]] — Goroutine/Machine/Processor, work stealing, por que não é 1:1 com threads do SO
4. [[04 - O ciclo de vida de uma goroutine]] — criação, estados (runnable/running/waiting), preempção, término
5. [[05 - Comunicar em vez de compartilhar]] — o mantra do Go, canais como alternativa a mutex, quando cada um serve
6. [[06 - Goroutines vs threads, event loop e GIL]] — comparação com Java/Node/Python, custo relativo, o que cada modelo troca

### Magus — julgamento

7. [[07 - Armadilhas — leaks e loop var]] — goroutine leak (canal sem receiver, contexto sem cancelamento), captura de variável de loop pré/pós Go 1.22
8. [[08 - Quando (não) usar goroutines]] — overhead que não compensa, quando um worker pool ou código síncrono é melhor

## Veja também

- [[03-Dominios/Tecnologia/Go/index|Trilha Go]] — índice geral (21 galhos + capstone)
- Galho anterior: [[03-Dominios/Tecnologia/Go/06 - Generics/index|Generics]]
- Próximo galho: **Channels e select** (galho 8) — onde canais deixam de ser mencionados de passagem e viram o mecanismo central de comunicação entre goroutines
