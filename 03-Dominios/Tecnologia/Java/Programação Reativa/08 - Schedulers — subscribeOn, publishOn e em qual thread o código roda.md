---
title: "Schedulers — subscribeOn, publishOn e em qual thread o código roda"
created: 2026-06-10
updated: 2026-06-10
type: concept
progress: backlog
status: seedling
publish: true
fase: adepto
tags:
  - java
  - reativa
  - adepto
  - schedulers
  - reactor
aliases:
  - "Schedulers Reactor"
  - "subscribeOn publishOn"
---

# Schedulers — subscribeOn, publishOn e em qual thread o código roda

> [!abstract] TL;DR
> Por default um pipeline reativo roda inteiro na thread que chamou `subscribe` — Reactor não cria threads sozinho. Pra mudar isso você tem dois operadores: `subscribeOn` muda a thread **da origem** (o topo da cadeia, onde os dados nascem) e vale pra cadeia toda; `publishOn` troca a thread **daí pra baixo** (dos operadores seguintes em diante). A regra de ouro: código bloqueante (JDBC, chamada HTTP síncrona, `Thread.sleep`) **DEVE** ser isolado em `Schedulers.boundedElastic()` pra não travar o event loop — bloquear uma thread de `Schedulers.parallel()` derruba a vazão de todas as requisições que compartilham aquele pool.

## O que é

Um `Scheduler` em Reactor é uma abstração sobre **onde** (em qual thread, de qual pool) o trabalho de um pipeline reativo é executado. É o equivalente reativo de um `ExecutorService`, mas pensado pra orquestrar os sinais (`onNext`, `onComplete`, `request(n)`) de um `Flux`/`Mono`.

O ponto que confunde todo mundo: **Reactor não escolhe threads por você**. Diferente do que a palavra "reativo" sugere, montar uma cadeia de operadores não dispara nenhuma concorrência. Tudo roda, por default, na thread que chamou `subscribe`. Os `Schedulers` e os operadores `subscribeOn`/`publishOn` são a forma **explícita** de introduzir mudança de thread.

## Por que importa

Em entrevista e na vida real, o erro número um com Reactor não é de lógica — é de threading. Alguém chama uma lib bloqueante (um `repository.findById()` JDBC, um cliente HTTP síncrono) dentro de um `map` ou `flatMap`, sem pensar em qual thread aquilo vai rodar. Como o pipeline normalmente roda na thread do event loop (poucas threads, uma por core), uma única chamada bloqueante **trava uma fatia inteira da capacidade do servidor**. Sob carga, todas as requisições que caem naquela thread param.

Entender `subscribeOn` × `publishOn` e quando usar `boundedElastic()` é o que separa "escrevi código reativo" de "escrevi código reativo que não derruba a produção".

Há ainda um motivo de design: ao ser explícito sobre qual pool executa cada trecho, você ganha **isolamento de recursos**. Trabalho de CPU não compete com I/O bloqueante pelas mesmas threads; um pico de chamadas lentas ao banco fica contido no `boundedElastic()` e não contamina o pool que serve o cálculo. Esse particionamento deliberado de pools é uma das vantagens que o modelo reativo oferece sobre "uma thread por requisição" ingênuo.

## Como funciona

### Por default: roda na thread que chamou `subscribe`

A documentação do Reactor é explícita: *"o operador mais ao topo (a origem) roda na thread em que a chamada `subscribe()` foi feita"*. Não há mágica. Se você monta um `Flux`, encadeia dez `map`, e chama `subscribe()` na thread `main`, os dez `map` e a emissão dos dados acontecem todos na `main`.

Isso é consequência direta da [[03-Dominios/Tecnologia/Java/Programação Reativa/04 - Nada acontece até o subscribe — lazy, assembly vs subscription, cold vs hot|natureza lazy do pipeline]]: a fase de *assembly* (montagem da cadeia) não decide thread nenhuma; só a fase de *subscription* é que executa, e ela herda a thread de quem assinou.

### `subscribeOn`: afeta a origem (o início da cadeia)

`subscribeOn(scheduler)` muda a thread em que a **subscrição** acontece — ou seja, a thread em que a **origem** começa a produzir os dados. O efeito sobe pela cadeia até o topo.

Duas sutilezas que caem em prova:

1. **A posição na cadeia quase não importa.** Você pode colocar `subscribeOn` no meio ou no fim da cadeia; ele ainda afeta a origem. Isso porque a subscrição é propagada de baixo pra cima (do subscriber em direção à origem) no momento do `subscribe`.
2. **Só o `subscribeOn` mais próximo da origem vale.** A doc diz: *"apenas a chamada `subscribeOn` mais próxima [downstream] efetivamente agenda a subscrição e os sinais de request pra origem"*. Se você empilhar dois `subscribeOn`, o que está mais perto da origem ganha; o outro é praticamente inócuo.

Use `subscribeOn` quando a **própria origem** é bloqueante ou cara — por exemplo, um `Mono.fromCallable(...)` que envolve uma chamada JDBC.

### `publishOn`: troca a thread daí pra baixo

`publishOn(scheduler)` se comporta *"como qualquer outro operador, no meio da cadeia"*: ele troca a thread de execução **dos operadores seguintes** — daquele ponto pra baixo, até encontrar outro `publishOn`. A doc: *"afeta onde os operadores subsequentes executam"*.

A diferença mental:

- `subscribeOn` = "onde a cadeia **começa** a rodar" (afeta a origem, cadeia toda).
- `publishOn` = "a partir **daqui**, troca de thread" (afeta o downstream).

Você pode ter vários `publishOn` numa cadeia, cada um trocando o contexto do trecho seguinte — é assim que se move trabalho entre pools (ex.: ler de I/O em `boundedElastic()`, depois transformar em `parallel()`).

### Os `Schedulers`: `parallel()`, `boundedElastic()`, `single()`, `immediate()`

A fábrica `Schedulers` (de `reactor.core.scheduler.Schedulers`) expõe instâncias compartilhadas:

| Scheduler | Para quê |
| --- | --- |
| `Schedulers.parallel()` | Trabalho de **CPU** (computação). Pool fixo com tantos workers quanto cores. Nunca bloqueie aqui. |
| `Schedulers.boundedElastic()` | **Envolver código BLOQUEANTE** (JDBC, I/O síncrono, libs legadas). Dá a cada tarefa bloqueante sua própria thread, com um teto pra não explodir. |
| `Schedulers.single()` | Uma única thread reutilizável, pra trabalho sequencial leve. |
| `Schedulers.immediate()` | Não troca de thread — executa o `Runnable` na thread atual. Útil como no-op quando uma API exige um `Scheduler`. |

Sobre como pools e threads funcionam por baixo (tamanho de pool, daemon threads, fila), veja o Galho 4 — não vou re-explicar aqui.

### Nunca bloquear o event loop

`Schedulers.parallel()` e `Schedulers.single()` têm um número pequeno e fixo de threads — são o "event loop" do mundo Reactor. Chamar algo bloqueante nelas é um pecado capital: a thread fica parada esperando I/O em vez de processar outros sinais, e a vazão despenca.

Reactor inclusive te protege em parte: chamar `block()`, `blockFirst()` ou `blockLast()` de dentro de uma thread `parallel()`/`single()` lança `IllegalStateException`. Mas isso não pega todo bloqueio — um `jdbcTemplate.query(...)` dentro de um `map` bloqueia silenciosamente. A defesa é arquitetural: **todo bloqueio vai pra `boundedElastic()`**, via `subscribeOn` (se a origem bloqueia) ou `publishOn` (se o trecho seguinte bloqueia).

> [!tip] Detectando bloqueios em testes
> A lib `BlockHound` (um agente de instrumentação) intercepta chamadas bloqueantes conhecidas (`Thread.sleep`, I/O de `java.net`, locks) feitas em threads não-bloqueantes e lança erro na hora. É a forma de transformar um bug silencioso de produção em uma falha barulhenta no CI.

### `subscribeOn` × `publishOn` lado a lado

Vale fixar o modelo mental numa tabela única, porque a confusão entre os dois é a fonte de quase todo bug de threading em Reactor:

| Aspecto | `subscribeOn` | `publishOn` |
| --- | --- | --- |
| O que muda | A thread da **origem** (topo da cadeia) | A thread **dos operadores seguintes** |
| Escopo do efeito | A cadeia toda (sobe até a origem) | Daquele ponto pra baixo |
| Posição importa? | Quase não — afeta a origem onde quer que esteja | Sim — só vale do ponto exato pra frente |
| Empilhar vários | Só o mais próximo da origem vale | Cada um troca o trecho seguinte (todos valem) |
| Caso de uso típico | Origem bloqueante (`fromCallable` com JDBC) | Mover trabalho entre pools no meio da cadeia |

Regra prática de uma frase: **`subscribeOn` decide onde a cadeia *nasce*; `publishOn` decide onde a cadeia *continua* a partir de um ponto.**

## Na prática

Cenário: buscar um `Order` num banco via JDBC (bloqueante), depois fazer um cálculo de CPU em cima do `Customer` e do `Product`.

```java
import reactor.core.publisher.Mono;
import reactor.core.scheduler.Schedulers;

// jdbcCall é síncrono e BLOQUEANTE — encapsulamos com fromCallable
Mono<Order> orderMono =
    Mono.fromCallable(() -> orderRepository.findByIdBlocking(orderId))
        // origem bloqueante -> isola na thread elástica
        .subscribeOn(Schedulers.boundedElastic());

orderMono
    // daqui pra baixo, trabalho de CPU vai pro pool paralelo
    .publishOn(Schedulers.parallel())
    .map(order -> enrich(order))          // cálculo CPU-bound
    .map(order -> applyDiscount(order))   // cálculo CPU-bound
    .subscribe(order ->
        System.out.println("done on " + Thread.currentThread().getName()));
```

O `subscribeOn(boundedElastic())` garante que a chamada JDBC roda numa thread elástica (que **pode** bloquear). O `publishOn(parallel())` move os dois `map` pesados pro pool de CPU. Resultado: nenhuma thread do pool paralelo fica presa em I/O.

Repare que o `subscribeOn` está colado na origem e o `publishOn` vem depois — essa é a ordem idiomática quando você tem uma fonte bloqueante seguida de processamento de CPU. Se a ordem fosse invertida (`publishOn` antes do `subscribeOn`), o resultado ainda funcionaria, porque `subscribeOn` afeta a origem independente da posição — mas a leitura ficaria menos clara pra quem mantém o código depois.

Os nomes de thread deixam a troca visível:

```text
fromCallable + map(enrich) está em:  boundedElastic-1   <- subscribeOn
... após publishOn(parallel) ...
map(enrich), map(applyDiscount):     parallel-3         <- publishOn
subscribe (consumidor):              parallel-3
```

A leitura: a origem e tudo **acima** do `publishOn` rodam em `boundedElastic-1` (por causa do `subscribeOn`); do `publishOn` pra baixo, tudo migra pra `parallel-3`.

## Armadilhas

### (1) Chamar código bloqueante sem `boundedElastic()` trava o event loop

O erro clássico: enfiar uma chamada JDBC ou um cliente HTTP síncrono dentro de um operador que está rodando numa thread `parallel()`/`single()`. Aquela thread para de servir outras requisições enquanto espera o I/O. Sob carga, o pool inteiro congela e **todas** as requisições atrasam ou estouram timeout.

```java
// RUIM: findByIdBlocking() é JDBC síncrono, e este map roda no event loop
Flux<Customer> customers = customerIds
    .map(id -> customerRepository.findByIdBlocking(id)); // bloqueia parallel-N
```

Fix: isole o bloqueio em `boundedElastic()`. Como o bloqueio está na origem de cada item, envolva num `Mono.fromCallable(...).subscribeOn(...)` e use `flatMap`:

```java
Flux<Customer> customers = customerIds
    .flatMap(id ->
        Mono.fromCallable(() -> customerRepository.findByIdBlocking(id))
            .subscribeOn(Schedulers.boundedElastic()));
```

### (2) Achar que `subscribeOn` troca a thread no meio da cadeia

`subscribeOn` afeta a **origem**, não o ponto onde você o colocou. Quem quer "a partir daqui, troque de thread" precisa de `publishOn`. Confundir os dois leva a código que parece mover trabalho pra outro pool, mas não move.

```java
// EXPECTATIVA ERRADA: "expensiveCpu roda em parallel"
Mono.fromCallable(() -> loadProductBlocking())   // bloqueante
    .map(p -> expensiveCpu(p))                    // ainda roda na thread da origem
    .subscribeOn(Schedulers.parallel());          // afeta a ORIGEM, não o map
```

Aqui a origem bloqueante acabou em `parallel()` (errado: bloqueia o event loop) e o `map` herdou a mesma thread. Fix: bloqueante na origem vai pra `boundedElastic()` via `subscribeOn`; o trabalho de CPU vai pra `parallel()` via `publishOn`:

```java
Mono.fromCallable(() -> loadProductBlocking())
    .subscribeOn(Schedulers.boundedElastic())   // origem bloqueante isolada
    .publishOn(Schedulers.parallel())           // daqui pra baixo, CPU
    .map(p -> expensiveCpu(p));
```

### (3) Empilhar vários `subscribeOn` esperando que todos valham

Só o `subscribeOn` **mais próximo da origem** tem efeito; os demais são ignorados na prática. Quem coloca dois esperando combiná-los se frustra — o de cima vence e o de baixo não faz nada.

```java
Mono.fromCallable(() -> loadOrderBlocking())
    .subscribeOn(Schedulers.boundedElastic())  // ESTE vale (mais perto da origem)
    .map(o -> transform(o))
    .subscribeOn(Schedulers.parallel());        // IGNORADO na prática
```

Fix: use **um** `subscribeOn` (pra origem) e, se precisar trocar de thread no meio, use `publishOn` no ponto exato:

```java
Mono.fromCallable(() -> loadOrderBlocking())
    .subscribeOn(Schedulers.boundedElastic())  // origem
    .publishOn(Schedulers.parallel())          // troca real no meio da cadeia
    .map(o -> transform(o));
```

### (4) Criar um `Scheduler` novo a cada requisição em vez de reusar

`Schedulers.parallel()`, `boundedElastic()`, `single()` e `immediate()` retornam instâncias **compartilhadas** (singletons globais), prontas pra reuso. Já `Schedulers.newParallel(...)` / `newBoundedElastic(...)` criam pools **novos**. Chamar os `newX` dentro de um handler de requisição vaza threads: cada request gera um pool que talvez nunca seja descartado.

```java
// RUIM: cria um pool novo a cada chamada -> vazamento de threads
Mono.fromCallable(() -> loadProductBlocking())
    .subscribeOn(Schedulers.newBoundedElastic(10, 100, "leak")); // novo pool por request
```

Fix: use a instância compartilhada, ou crie um pool dedicado **uma vez** (campo/`@Bean`) e reuse:

```java
// reusa o pool global compartilhado
Mono.fromCallable(() -> loadProductBlocking())
    .subscribeOn(Schedulers.boundedElastic());
```

## Em entrevista

### Frase pronta (inglês)

> By default, a Reactor pipeline runs entirely on the thread that called `subscribe` — the framework doesn't introduce concurrency on its own. To control threading I use two operators: `subscribeOn`, which changes the thread where the source starts and affects the whole chain regardless of where I place it, and `publishOn`, which switches the execution context for everything downstream of that point. The critical rule is that any blocking call — JDBC, a synchronous HTTP client, `Thread.sleep` — must be isolated on `Schedulers.boundedElastic()`; blocking a `Schedulers.parallel()` thread would starve the event loop and tank throughput for every request sharing that pool.

### Vocabulário

| Termo PT | Termo EN |
| --- | --- |
| agendador / escalonador | scheduler |
| origem (da cadeia) | source |
| trocar de thread | switch threads |
| código bloqueante | blocking code |
| pool elástico limitado | bounded elastic pool |
| travar o event loop | starve the event loop |
| vazão | throughput |
| contexto de execução | execution context |

## Veja também

- [[03-Dominios/Tecnologia/Java/Programação Reativa/04 - Nada acontece até o subscribe — lazy, assembly vs subscription, cold vs hot|Nada acontece até o subscribe]]
- [[03-Dominios/Tecnologia/Java/Programação Reativa/09 - Backpressure — request(n) e as estratégias BUFFER, DROP, LATEST|Backpressure]]
- [[03-Dominios/Tecnologia/Java/Concorrência e paralelismo/index|Concorrência e paralelismo]] (pools e threads — Galho 4)
- [[03-Dominios/Tecnologia/Java/Concorrência e paralelismo/12 - Virtual Threads e Project Loom|Virtual Threads e Project Loom]]
- [[03-Dominios/Tecnologia/Java/Programação Reativa/index|Programação Reativa (MOC do galho)]]
- [[03-Dominios/Tecnologia/Java/index|Trilha Java]]
- [[03-Dominios/Tecnologia/Java/Dicionário de Java|Dicionário de Java]]

## Referências

- Project Reactor Reference — Threading and Schedulers: https://projectreactor.io/docs/core/release/reference/coreFeatures/schedulers.html
- Project Reactor Reference (índice): https://projectreactor.io/docs/core/release/reference/#schedulers
