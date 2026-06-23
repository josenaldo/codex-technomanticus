---
title: "Concorrência e Paralelismo"
created: 2026-06-18
updated: 2026-06-18
type: moc
status: growing
publish: true
tags:
  - fundamentos
  - concorrencia
  - paralelismo
  - entrevista
  - moc
aliases:
  - Concorrência e Paralelismo
  - Concorrência
  - Concorrência conceitual
  - Concurrency
  - Paralelismo
  - Galho - Concorrência e Paralelismo
---

# Concorrência e Paralelismo

> [!abstract] TL;DR
> Galho de Fundamentos sobre como o software faz **mais de uma coisa ao mesmo tempo** — e por que isso é
> tão difícil de acertar. Aqui ficam os **problemas universais** (race conditions, deadlock, atomicidade/
> visibilidade/ordenação), as **primitivas de coordenação** (locks, semáforos, atômicos, STM) e, o coração
> do galho, os **cinco modelos de concorrência** (memória compartilhada, CSP, atores, event loop, dados),
> cada um com a linguagem que o levou mais longe. Tudo **stack-agnóstico**: a mecânica Java vive no galho
> Java, aqui mora a teoria. Interview-critical.

## Sobre este galho

Concorrência é o tema onde mais se erra em produção e onde o senior se separa do júnior em entrevista. Este
galho é o **andar conceitual**: os conceitos que sobrevivem à troca de linguagem, e a comparação honesta
entre os modelos que as linguagens escolheram.

**Fronteiras (linka, não duplica):**
- **Concorrência Java específica** (java.util.concurrent, `synchronized`, locks, Loom/virtual threads,
  structured concurrency) → [[03-Dominios/Tecnologia/Java/Concorrência e paralelismo/index|Concorrência (Java)]] e [[Java Concurrency]].
- **Imutabilidade como arma contra concorrência** → [[08 - Imutabilidade e estado]] (galho Paradigmas).
- **Isolamento, MVCC e locking de banco** → [[Banco de Dados]] (a nota de STM cruza, não duplica).
- **Assincronia e o modelo reativo** → [[12 - Programação reativa e dataflow]] (Paradigmas) e [[Programação Reativa]] (Java).
- **Processos, threads e scheduling no SO** → futuro galho de Sistemas Operacionais (mencionado em prosa).

**Audiência:** dev senior em preparação para entrevista internacional. Cada nota tem seção "Em entrevista"
com frases prontas em inglês e vocabulário técnico PT→EN.

## Iniciado — o terreno e os perigos universais

1. [[01 - Concorrência e paralelismo - o que é e por que é difícil]] — concorrência × paralelismo, não-determinismo, as duas faces.
2. [[02 - Processos e threads]] — isolamento × memória compartilhada, context switch, kernel/green/virtual threads.
3. [[03 - Estado compartilhado e race conditions]] — read-modify-write não-atômico, o contador clássico, data race × race condition.
4. [[04 - Atomicidade, visibilidade e ordenação]] — os três problemas que todo modelo de memória precisa resolver.

## Adepto — primitivas de coordenação

5. [[05 - Exclusão mútua - locks, mutexes e monitores]] — seção crítica, monitor, reentrância, contention.
6. [[06 - Semáforos e coordenação]] — semáforo de Dijkstra, barreiras, latches, condition variables, produtor-consumidor.
7. [[07 - Deadlock, livelock e starvation]] — as 4 condições de Coffman, prevenir/evitar/detectar, inversão de prioridade.
8. [[08 - Operações atômicas e lock-free]] — CAS, problema ABA, lock-free × wait-free.
9. [[09 - Memória transacional e otimismo]] — STM, otimista × pessimista; cruza isolamento de banco.

## Magus — os modelos, as leis, os padrões e a síntese

10. [[10 - Memória compartilhada com threads e locks]] — o modelo dominante; showcase Java.
11. [[11 - Modelos de memória e consistência]] — happens-before, sequential × relaxed, barreiras de memória.
12. [[12 - Troca de mensagens e CSP]] — "share memory by communicating"; showcase Go (goroutines + channels).
13. [[13 - O modelo de atores]] — mailbox, supervisão, "let it crash"; showcase Erlang/Elixir/BEAM.
14. [[14 - Loop de eventos e assincronia]] — event loop + async/await; showcase JavaScript + GIL/asyncio do Python.
15. [[15 - Paralelismo de dados]] — SIMD, GPU, MapReduce, fork-join/work-stealing.
16. [[16 - As leis da escala - Amdahl e Gustafson]] — o teto do speedup e por que mais núcleos nem sempre ajudam.
17. [[17 - Padrões de concorrência]] — pool, produtor-consumidor, fan-out/fan-in, pipeline, futures, work-stealing.
18. [[18 - Concorrência em entrevista]] — escolher o modelo, tabela comparativa, inglês, vocabulário, armadilhas.

## Rotas alternativas

### Entrevista internacional
01 → 03 → 04 → 07 → 10 → 11 → 18. Os problemas, deadlock, o modelo dominante, memória e o capstone.

### Os modelos de concorrência
01 → 10 → 12 → 13 → 14 → 15 → 18. O cluster comparativo do início ao fim.

### Os perigos e como evitá-los
03 → 04 → 05 → 07 → 08 → 17. Race, os três problemas, exclusão mútua, deadlock, lock-free e os padrões.

## Todas as notas

```dataview
TABLE fase, status, updated
FROM "03-Dominios/Ciência/Concorrência e Paralelismo"
WHERE type = "concept"
SORT file.name ASC
```

## Veja também

- [[03-Dominios/Ciência/index|Fundamentos (MOC do domínio)]]
- [[03-Dominios/Tecnologia/Java/Concorrência e paralelismo/index|Concorrência (Java)]] — a mecânica concreta em Java
- [[08 - Imutabilidade e estado]] — imutabilidade como antídoto ao estado compartilhado (galho Paradigmas)
- [[Banco de Dados]] — isolamento, MVCC e locking no banco
- [[Dicionário de Fundamentos]]
