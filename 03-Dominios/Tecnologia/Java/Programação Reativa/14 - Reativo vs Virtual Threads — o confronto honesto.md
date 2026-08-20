---
title: "Reativo vs Virtual Threads — o confronto honesto"
created: 2026-06-10
updated: 2026-06-10
type: concept
progress: backlog
status: seedling
publish: true
fase: Magus
tags:
  - java
  - reativa
  - magus
  - virtual-threads
  - reactor
aliases:
  - "reativo vs Virtual Threads"
  - "reactive vs virtual threads"
---

# Reativo vs Virtual Threads — o confronto honesto

> [!abstract] TL;DR
> Reativo e Virtual Threads (Java 21 GA, JEP 444) resolvem **o mesmo problema** — alta concorrência I/O-bound com poucos threads do SO — por caminhos opostos. Reativo te faz reescrever tudo em `Mono`/`Flux` (push, não-bloqueante, composição por operadores) e ganha **backpressure nativo** de brinde. Virtual Threads te deixam escrever código **bloqueante normal** que a JVM desbloqueia por baixo: stack trace normal, debugger normal, zero contágio. O resultado honesto: os VT tornaram o modelo imperativo **viável** pra alta concorrência sem a complexidade do Reactor, então reativo virou nicho. Reativo **ainda vence** em streaming real e backpressure de verdade ponta a ponta — mas **perdeu** o CRUD de alta concorrência, que era um dos motivos centrais pra escolher WebFlux.

## O que é

Esta é a nota-tese do galho: o confronto técnico entre **programação reativa** (Project Reactor, Spring WebFlux) e **Virtual Threads** (Project Loom) como soluções pro problema da **concorrência I/O-bound** — milhares de requests esperando banco, rede, disco.

Por anos, a resposta "séria" pra escalar I/O com poucos threads do SO era reativo: não bloqueie nenhum thread, reaja a eventos. O preço era alto — reescrever o código inteiro num estilo declarativo, perder o stack trace, contaminar toda a stack. Em **Java 21**, o JEP 444 entregou Virtual Threads como feature **final/GA**, e a equação mudou: agora dá pra ter milhares de requests concorrentes com **código bloqueante comum**.

> [!note] Esta nota assume que você já sabe o que é Virtual Thread
> O **o quê** e o **como** dos Virtual Threads (carrier threads, continuations, unmounting) são do Galho 4 — veja [[03-Dominios/Tecnologia/Java/Concorrência e paralelismo/12 - Virtual Threads e Project Loom|Virtual Threads e Project Loom]]. Aquela nota deixou explícito que "o confronto detalhado pertence ao Galho 11". **Esta nota é esse confronto.** Aqui não re-explico Loom; comparo.

## Por que importa

Numa entrevista internacional sênior, "por que reativo?" deixou de ter resposta automática. Se você responder "performance" ou "escala", o entrevistador vai (com razão) perguntar: *"e por que não Virtual Threads, que fazem o mesmo sem a complexidade?"*. Quem não sabe responder isso soa desatualizado — ou pior, dogmático.

A resposta madura não é "reativo morreu" nem "reativo é superior". É saber **exatamente** o que cada um dá e o que cada um cobra, e escolher pelo problema. A própria documentação do Spring é honesta sobre isso: ela manda você **olhar suas dependências** — se você usa APIs de persistência bloqueantes (JPA, JDBC), Spring MVC é a melhor escolha pra arquiteturas comuns. Virtual Threads só reforçam esse conselho, porque tornam o MVC bloqueante escalável.

## Como funciona

### O ponto comum: ambos resolvem I/O-bound com poucos threads do SO

O inimigo dos dois é o mesmo: **um thread do SO parado esperando I/O é desperdício caro**. No modelo clássico thread-por-request, 10.000 requests lentos exigem 10.000 threads do SO — cada um com sua stack de ~1 MB e custo de context switch. A máquina morre antes do gargalo real (o banco).

Reativo resolve **não tendo threads parados**: o thread devolve o controle ao event loop assim que dispara o I/O e só "reage" quando a resposta chega. Virtual Threads resolvem **tendo threads baratíssimos**: quando um virtual thread bloqueia em I/O, a JVM o **desmonta** do carrier thread (um thread do SO real), que fica livre pra rodar outro. Em ambos, um punhado de threads do SO serve milhares de requests. **Mesmo objetivo, mecanismos opostos.**

### Reativo: operadores, backpressure nativo, composição — mas debugging difícil e contágio

Reativo te dá uma **álgebra de fluxos**: `map`, `flatMap`, `zip`, `retry`, `timeout` compõem pipelines assíncronos declarativamente. E te dá, **de graça e nativo**, o que nenhum outro modelo dá: **backpressure** — o consumidor sinaliza quanto aguenta via `request(n)`, e o produtor respeita. Em um stream infinito (eventos, SSE, Kafka), isso é a diferença entre o sistema sobreviver e o `OutOfMemoryError`.

O preço:

- **Debugging difícil.** O stack trace não reflete o fluxo lógico — ele mostra as entranhas do Reactor, não o seu `flatMap`. Precisa de `Hooks.onOperatorDebug()` ou `checkpoint()` pra ter pistas. Veja [[03-Dominios/Tecnologia/Java/Programação Reativa/15 - Quando (não) usar reativo — custo cognitivo, debugging e stack traces|Quando (não) usar reativo]].
- **Contágio.** Reativo é **viral**: se uma camada é reativa, tudo abaixo precisa ser. Um `Mono` que chama JDBC bloqueante no thread errado trava o event loop inteiro. Exige driver reativo (R2DBC) ponta a ponta — ou escapar com `publishOn(Schedulers.boundedElastic())`, que reintroduz threads.
- **Curva de aprendizado.** `subscribe`, cold vs hot, em qual thread o código roda — tudo conceito novo.

### Virtual Threads (Java 21 GA): código bloqueante normal, stack trace normal — mas sem backpressure nativo, sem contágio

Com Virtual Threads você escreve **código imperativo bloqueante** — `var x = repo.findById(id)` — e a JVM cuida de não desperdiçar thread do SO. O que você ganha:

- **Stack trace normal.** A exceção mostra a sua chamada, na sua linha. O debugger para onde você espera. Profilers, thread dumps, ferramentas de sempre — tudo funciona.
- **Sem contágio.** Não há cor de função: bloqueante e não-bloqueante convivem. Você adota incrementalmente.
- **Curva ~zero.** É o modelo que todo dev Java já conhece, rodando num executor diferente.

O que você **não** ganha:

- **Backpressure nativo.** Virtual Threads não têm `request(n)`. Se 1 milhão de tarefas chegam, você cria 1 milhão de virtual threads — baratos, mas não infinitos, e o recurso a jusante (pool de conexões, banco) pode afogar. Backpressure com VT é **manual**: `Semaphore`, fila limitada, pool de conexões como gargalo proposital. Funciona, mas é você quem implementa.
- **Composição declarativa de assíncrono.** Sem `zip`/`merge`/`retry` prontos; você orquestra com structured concurrency e código imperativo.

### Onde reativo AINDA vence

- **Streaming real / dados infinitos.** SSE, WebSocket, consumo de Kafka, agregação de múltiplas fontes em tempo real — fluxos que nunca "terminam" e cujo ritmo precisa ser controlado.
- **Backpressure de verdade.** Quando produtor e consumidor têm velocidades diferentes e você precisa que o sistema se auto-regule sem estourar memória — `request(n)` é nativo só no modelo reativo.
- **Stack já reativo ponta a ponta.** Se você já tem R2DBC, WebClient reativo e gateway reativo, manter o modelo é coerente e evita misturar paradigmas.

### Onde VT venceu

- **CRUD de alta concorrência.** O caso dominante: endpoint que recebe request, chama banco bloqueante (JDBC/JPA), devolve JSON. Aqui VT entregam a mesma escala do reativo com código que qualquer um lê e debuga. A própria recomendação documentada do Spring — "tem dependência bloqueante? Use MVC" — agora vem com escala embutida via VT.

### A tabela comparativa honesta

| Critério | Reativo (Reactor/WebFlux) | Virtual Threads (Java 21) |
| --- | --- | --- |
| Legibilidade | Declarativo, mas exige pensar em fluxos | Imperativo, igual ao código de sempre |
| Debugging | Difícil — stack trace é do Reactor, não do seu código | Normal — stack trace e debugger apontam sua linha |
| Backpressure | **Nativo** (`request(n)`, Reactive Streams) | Manual (semáforo, fila limitada, pool) |
| Libs bloqueantes | Proibidas no event loop (precisa R2DBC / `boundedElastic`) | OK — bloqueantes são o caso normal |
| Contágio | Viral — tudo precisa ser reativo | Nenhum — convive com código bloqueante |
| Curva de aprendizado | Alta (lazy, schedulers, hot/cold) | Quase zero (modelo conhecido) |
| Escala I/O-bound | Alta, threads fixos | Alta, virtual threads baratos |

## Na prática

O mesmo endpoint de alta concorrência — buscar pedidos de um cliente — nos dois modelos.

### (a) Reativo: WebFlux + R2DBC

```java
import reactor.core.publisher.Flux;
import reactor.core.publisher.Mono;

@RestController
class OrderController {

    private final ReactiveOrderRepository orders;   // R2DBC, não-bloqueante

    OrderController(ReactiveOrderRepository orders) {
        this.orders = orders;
    }

    @GetMapping("/customers/{id}/orders")
    Flux<Order> ordersOf(@PathVariable Long id) {
        return orders.findByCustomerId(id)          // Flux<Order> — push, lazy
                     .filter(Order::isActive)
                     .take(100);                     // backpressure: pede só 100
    }
}
```

O retorno é um `Flux<Order>`: nada acontece até o cliente HTTP fazer `subscribe`. O event loop do Netty serve milhares de conexões com poucos threads, e `take(100)` é backpressure de verdade — o repositório nunca produz mais do que o consumidor pede. O preço: **tudo** abaixo (o driver, a connection pool) precisa ser reativo, e se algo der errado, o stack trace vai falar de operadores do Reactor, não do seu `filter`.

### (b) Imperativo: Spring MVC com Virtual Threads + JDBC

```java
import java.util.List;

@RestController
class OrderController {

    private final OrderRepository orders;           // JPA/JDBC, bloqueante

    OrderController(OrderRepository orders) {
        this.orders = orders;
    }

    @GetMapping("/customers/{id}/orders")
    List<Order> ordersOf(@PathVariable Long id) {
        return orders.findByCustomerId(id).stream() // bloqueia — e tudo bem
                     .filter(Order::isActive)
                     .limit(100)
                     .toList();
    }
}
```

Com Virtual Threads ligados (`spring.threads.virtual.enabled=true` no Spring Boot 3.2+), cada request roda num virtual thread. A chamada JDBC **bloqueia** — mas a JVM desmonta o virtual thread do carrier, que vai servir outro request. Mesma escala que (a) pra esse caso, com código que qualquer dev Java lê de primeira e cujo stack trace, em caso de erro, aponta a linha exata do `filter`.

**Análise honesta do trade-off.** Pra esse endpoint — request → banco → JSON — (b) entrega a escala de (a) com uma fração do custo cognitivo. Não há `OutOfMemoryError` salvo por backpressure aqui, porque o gargalo natural é a connection pool do banco, que já limita a vazão. Onde (a) brilharia de verdade é se a fonte fosse um stream **infinito** (eventos em tempo real) cujo ritmo precisa ser regulado — aí o `take`/`request(n)` nativo do reativo passa a ser insubstituível, e (b) precisaria de backpressure manual.

## Armadilhas

### (1) Adotar reativo "pela performance" num CRUD comum

**Descrição.** A justificativa mais comum e mais frágil pra WebFlux: *"é mais rápido / escala mais"*. Num CRUD I/O-bound, Virtual Threads entregam a mesma escala sem nenhum dos custos do reativo.

**Exemplo.** Time reescreve uma API REST inteira em `Mono`/`Flux` + R2DBC "pra aguentar carga". Ganha stack traces ilegíveis, contágio em toda a stack e onboarding lento — pra resolver um problema que `spring.threads.virtual.enabled=true` resolveria em uma linha.

**Fix.** Antes de adotar reativo, pergunte: *é streaming/backpressure de verdade, ou é CRUD de alta concorrência?* Se for CRUD, fique no imperativo e ligue Virtual Threads. Reserve reativo pros casos onde o modelo push é a essência do problema, não um detalhe de infra.

### (2) Achar que Virtual Threads "mataram" o reativo

**Descrição.** O hype inverso. Virtual Threads resolvem **concorrência por bloqueio**, não **fluxo de dados**. Eles não dão `request(n)`, não dão operadores de composição, não dão backpressure nativo.

**Exemplo.** Engenheiro migra um consumidor de eventos Kafka de Reactor pra virtual threads "porque VT mataram o reativo" e descobre que precisa reimplementar backpressure na mão — semáforo, fila limitada — pra não estourar memória quando o produtor é mais rápido que o consumidor. Reinventou, pior, o que `Flux` já dava de graça.

**Fix.** Trate a escolha por problema. Streaming real, dados infinitos e backpressure de ponta a ponta continuam sendo território do reativo — veja [[03-Dominios/Tecnologia/Java/Programação Reativa/09 - Backpressure — request(n) e as estratégias BUFFER, DROP, LATEST|Backpressure]]. VT venceram o CRUD; não venceram o streaming.

### (3) Comparar os dois por latência de um request

**Descrição.** Erro de medição clássico: rodar um benchmark de **um** request e concluir que um modelo "é mais rápido". Não é disso que se trata. A documentação do Spring é explícita: reativo **não roda mais rápido** — ele escala com um número fixo e pequeno de threads e menos memória.

**Exemplo.** Alguém mede a latência de `GET /orders/1` nos dois e anuncia "reativo é igual / pior, então não serve". A métrica certa nunca foi latência por request — é **throughput e uso de recurso sob carga concorrente alta**. Em latência de um request, os dois empatam (o gargalo é o banco).

**Fix.** Compare sob carga: milhares de requests concorrentes, medindo throughput, threads do SO usados e memória. É aí que ambos brilham — e onde a decisão real (legibilidade, debugging, backpressure) passa a pesar mais que "velocidade".

## Em entrevista

### Frase pronta (inglês)

> Reactive programming and virtual threads, which went GA in Java 21 under JEP 444, solve the same problem — high-concurrency I/O-bound work on few OS threads — but from opposite directions. Reactive makes you rewrite everything as non-blocking `Mono`/`Flux` pipelines, and in exchange you get native backpressure through `request(n)`; virtual threads let you keep writing ordinary blocking code with normal stack traces and no function coloring, but backpressure becomes your job. So my rule is to choose by problem, not by hype: for high-concurrency CRUD I now reach for virtual threads, which is also what the Spring docs imply when they say a blocking persistence dependency points you to MVC; I keep reactive for real streaming and end-to-end backpressure, where `request(n)` is genuinely irreplaceable.

### Vocabulário

| Termo PT | Termo EN |
| --- | --- |
| contágio (cor de função) | function coloring |
| backpressure nativo | native backpressure |
| limitado por I/O | I/O-bound |
| thread do SO / carrier thread | OS thread / carrier thread |
| vazão (sob carga) | throughput (under load) |
| escapatória (pra bloquear) | escape hatch (for blocking) |

## Veja também

- [[03-Dominios/Tecnologia/Java/Programação Reativa/01 - O que é programação reativa — o modelo push, assíncrono e não-bloqueante|O que é programação reativa]]
- [[03-Dominios/Tecnologia/Java/Programação Reativa/09 - Backpressure — request(n) e as estratégias BUFFER, DROP, LATEST|Backpressure]]
- [[03-Dominios/Tecnologia/Java/Programação Reativa/15 - Quando (não) usar reativo — custo cognitivo, debugging e stack traces|Quando (não) usar reativo]]
- [[03-Dominios/Tecnologia/Java/Concorrência e paralelismo/12 - Virtual Threads e Project Loom|Virtual Threads e Project Loom]]
- [[03-Dominios/Tecnologia/Java/Programação Reativa/index|Programação Reativa (MOC do galho)]]
- [[03-Dominios/Tecnologia/Java/index|Trilha Java]]
- [[03-Dominios/Tecnologia/Java/Dicionário de Java|Dicionário de Java]]

> [!info] Galhos futuros
> O custo cognitivo detalhado do reativo é o tema da nota seguinte do galho (15). Galhos 12-16 da trilha Java ainda estão planejados.

## Referências

- Spring Framework — Web on Reactive Stack / WebFlux (motivação, modelo de concorrência, backpressure e a recomendação "dependência bloqueante → Spring MVC"): https://docs.spring.io/spring-framework/reference/web/webflux/new-framework.html
- Spring Framework — Reactive Core (`HttpHandler` com non-blocking I/O e Reactive Streams back pressure): https://docs.spring.io/spring-framework/reference/web/webflux/reactive-spring.html
- OpenJDK — JEP 444: Virtual Threads (entregue como feature final no Java 21): https://openjdk.org/jeps/444
