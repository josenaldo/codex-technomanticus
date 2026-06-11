---
title: "Programação Reativa"
created: 2026-06-10
updated: 2026-06-11
type: moc
status: growing
publish: true
tags:
  - java
  - reativa
  - moc
aliases:
  - "Programação Reativa"
  - "Reactive Programming"
  - "Project Reactor"
  - "Spring WebFlux"
  - "Galho 11 - Reativa"
---

# Programação Reativa

> [!abstract] TL;DR
> O **Galho 11** cobre o modelo reativo na JVM: o que é programação reativa e o Reactive Streams, `Mono`/`Flux` e os operadores do Project Reactor, schedulers e backpressure, Spring WebFlux e WebClient, R2DBC, e o **confronto honesto reativo vs Virtual Threads** — quando usar e, principalmente, quando **não** usar. São **16 notas** em 3 fases (Iniciado, Adepto, Magus).

## Sobre este galho

Programação reativa é o **modelo push, assíncrono e não-bloqueante** da JVM: dados como um stream que empurra eventos a quem reage, sob controle de demanda (backpressure), compostos declarativamente por operadores. Este galho parte do conceito e do Reactive Streams, percorre o Project Reactor (`Mono`/`Flux`, operadores, schedulers, backpressure), sobe pra camada web (Spring WebFlux, WebClient, functional endpoints), desce pro banco (R2DBC) e fecha com a decisão de engenharia: **quando reativo paga o próprio custo**.

**Audiência primária:** dev pleno/sênior que vai encarar entrevista internacional e precisa explicar o modelo reativo com critério. **Secundária:** quem mantém ou avalia um stack WebFlux/R2DBC e precisa decidir entre reativo e o imperativo.

É um **galho novo** (majoritariamente pesquisa em doc oficial — Project Reactor, Spring WebFlux, R2DBC, Reactive Streams), com uma única **poda cirúrgica**: a seção `## Spring WebFlux` do tronco `Backend/Spring Boot.md`, que apenas apontava "merece sua própria nota". E tem **quádrupla fronteira**: este galho **confronta o modelo de threads do Galho 4** ([[03-Dominios/Java/Concorrência e paralelismo/index|Concorrência e paralelismo]] — o confronto reativo vs Virtual Threads), **substitui o stack web do Galho 9** ([[03-Dominios/Java/Web e APIs REST/index|Web e APIs REST]] — Spring MVC imperativo vs WebFlux reativo), **contrasta a persistência do Galho 10** ([[03-Dominios/Java/Persistência de dados/index|Persistência de dados]] — JPA/JDBC bloqueante vs R2DBC reativo) e **roda sobre o container do Galho 8** ([[03-Dominios/Java/Spring Core e Boot/index|Spring Core e Boot]]). As notas linkam de volta a essas fronteiras sem re-explicá-las.

**A tese central, sem hype:** os **Virtual Threads** (Java 21 GA) tornaram o modelo imperativo viável pra alta concorrência I/O-bound **sem** a complexidade do Reactor — então reativo virou **nicho**: ainda vence em streaming real e backpressure de verdade, mas perdeu a maioria dos CRUDs. Por isso "quando **não** usar reativo" é metade do galho.

Mensageria reativa/Reactor Kafka é o galho [[03-Dominios/Java/Mensageria/25 - Mensageria reativa — Reactor Kafka|Mensageria]]; resiliência/backpressure distribuído (Galho 16) e segurança reativa/WebFlux Security (Galho 12) são planejados, sem cobertura aqui; testes reativos com `StepVerifier` são o galho [[03-Dominios/Java/Testes/15 - Testando código reativo — StepVerifier e @WebFluxTest|Testes]].

## Iniciado

O modelo mental — antes de qualquer operador.

- [[03-Dominios/Java/Programação Reativa/01 - O que é programação reativa — o modelo push, assíncrono e não-bloqueante|01 — O que é programação reativa]] — push vs pull, não-bloqueante, e por que serve I/O-bound com poucos threads.
- [[03-Dominios/Java/Programação Reativa/02 - Reactive Streams — a spec das 4 interfaces e o Flow do Java 9|02 — Reactive Streams]] — a spec das 4 interfaces (`Publisher`/`Subscriber`/`Subscription`/`Processor`) e o `java.util.concurrent.Flow` do Java 9.
- [[03-Dominios/Java/Programação Reativa/03 - Mono e Flux — os publishers do Project Reactor|03 — Mono e Flux]] — os publishers do Reactor: `Mono` (0-1) vs `Flux` (0-N) e a criação.
- [[03-Dominios/Java/Programação Reativa/04 - Nada acontece até o subscribe — lazy, assembly vs subscription, cold vs hot|04 — Nada acontece até o subscribe]] — lazy, assembly vs subscription time, cold vs hot.

## Adepto

Operadores, fluxo e a camada web.

- [[03-Dominios/Java/Programação Reativa/05 - map e flatMap — transformando o fluxo|05 — map e flatMap]] — a confusão central: transformação síncrona 1:1 vs assíncrona que achata publishers.
- [[03-Dominios/Java/Programação Reativa/06 - Combinando publishers — zip, merge, concat, filter|06 — Combinando publishers]] — `zip`, `merge`, `concat`, `filter` e quando a ordem importa.
- [[03-Dominios/Java/Programação Reativa/07 - Error handling reativo — onErrorResume, onErrorReturn, retry|07 — Error handling reativo]] — o erro como sinal terminal e a recuperação declarativa (`onError*`, `retry`).
- [[03-Dominios/Java/Programação Reativa/08 - Schedulers — subscribeOn, publishOn e em qual thread o código roda|08 — Schedulers]] — `subscribeOn` vs `publishOn`, os `Schedulers` e nunca bloquear o event loop.
- [[03-Dominios/Java/Programação Reativa/09 - Backpressure — request(n) e as estratégias BUFFER, DROP, LATEST|09 — Backpressure]] — o coração do Reactive Streams: `request(n)` e as estratégias de overflow.
- [[03-Dominios/Java/Programação Reativa/10 - Spring WebFlux — o stack não-bloqueante sobre Netty e o DispatcherHandler|10 — Spring WebFlux]] — o event loop sobre Netty e o `DispatcherHandler` (vs o `DispatcherServlet` do Galho 9).
- [[03-Dominios/Java/Programação Reativa/11 - WebClient — o cliente HTTP reativo a fundo|11 — WebClient]] — o cliente HTTP reativo, par do `RestClient` síncrono do Galho 9.
- [[03-Dominios/Java/Programação Reativa/12 - Functional endpoints — RouterFunction e HandlerFunction|12 — Functional endpoints]] — a alternativa funcional aos controllers anotados (`RouterFunction`/`HandlerFunction`).

## Magus

Persistência reativa, o confronto e a decisão.

- [[03-Dominios/Java/Programação Reativa/13 - R2DBC — persistência reativa sem EntityManager|13 — R2DBC]] — acesso reativo ao banco sem `EntityManager`, persistence context nem lazy loading (vs a JPA do Galho 10).
- [[03-Dominios/Java/Programação Reativa/14 - Reativo vs Virtual Threads — o confronto honesto|14 — Reativo vs Virtual Threads]] — o confronto que o Galho 4 adiou: onde reativo ainda vence e onde os Virtual Threads venceram.
- [[03-Dominios/Java/Programação Reativa/15 - Quando (não) usar reativo — custo cognitivo, debugging e stack traces|15 — Quando (não) usar reativo]] — o custo cognitivo, os stack traces fragmentados e o checklist de decisão honesto.
- [[03-Dominios/Java/Programação Reativa/16 - Capstone — uma request reativa de ponta a ponta no WebFlux|16 — Capstone]] — uma request reativa do `DispatcherHandler` ao `Flux`, sem bloquear o event loop.

## Rotas alternativas

- **Completa** — 01 → 16 em ordem (o caminho do modelo ao capstone).
- **Entrevista internacional** — 01 → 03 → 05 → 09 → 10 → 14 → 16 (modelo, `Mono`/`Flux`, `map`/`flatMap`, backpressure, WebFlux, reativo-vs-VT, capstone — o que mais cai).
- **Os operadores do Reactor** — 03 → 04 → 05 → 06 → 07 → 08 (`Mono`/`Flux`, lazy, `map`/`flatMap`, combinação, erro, schedulers).
- **O stack web reativo** — 01 → 10 → 11 → 12 → 13 → 16 (modelo, WebFlux, WebClient, functional, R2DBC, capstone).
- **Reativo vs Virtual Threads** (a ponte com o Galho 4) — 01 → 09 → 14 → 15 + [[03-Dominios/Java/Concorrência e paralelismo/12 - Virtual Threads e Project Loom|Virtual Threads e Project Loom]] (a decisão honesta).

## Todas as notas

```dataview
TABLE fase AS "Fase", status AS "Status"
FROM "03-Dominios/Java/Programação Reativa"
WHERE type = "concept"
SORT file.name ASC
```

## Veja também

- [[03-Dominios/Java/index|Trilha Java (MOC central)]]
- [[03-Dominios/Java/Concorrência e paralelismo/index|Concorrência e paralelismo]] — o modelo de threads e o confronto com Virtual Threads (Galho 4)
- [[03-Dominios/Java/Web e APIs REST/index|Web e APIs REST]] — o stack web imperativo que o WebFlux substitui (Galho 9)
- [[03-Dominios/Java/Persistência de dados/index|Persistência de dados]] — a JPA/JDBC bloqueante que o R2DBC contrasta (Galho 10)
- [[03-Dominios/Java/Spring Core e Boot/index|Spring Core e Boot]] — o container e a auto-configuration sob o WebFlux (Galho 8)
- [[03-Dominios/Java/Dicionário de Java|Dicionário de Java]] — glossário de termos da trilha

> Galhos 12 (Segurança), 13 (Testes), 14 (Mensageria), 16 (Microservices) e 17 (Cloud-native) — planejados.
