---
title: "Spec — Galho 11 da trilha Java Senior (Programação Reativa)"
date: 2026-06-10
author: Josenaldo
status: draft
type: spec
publish: false
---

# Spec — Galho 11 da trilha Java Senior (Programação Reativa)

## 1. Contexto e motivação

Este é o **décimo-primeiro galho** da trilha Java Senior (roadmap em `docs/superpowers/specs/2026-06-02-java-senior-roadmap-design.md`, §5, bloco "Fundamentos enterprise e Spring", linha 148). Pressupõe leitura do roadmap, que estabelece topologia flat, esquema de 3 fases, padrões editoriais e política de poda. Os Galhos 1 (Linguagem), 2 (Collections/Streams), 3 (JVM), **4 (Concorrência)**, 5 (Swing), 6 (JavaFX), 7 (Jakarta EE), **8 (Spring Core e Boot)**, **9 (Web e APIs REST)** e **10 (Persistência de dados)** já fecharam em `main` — seus artefatos são o **template de padrão e qualidade** deste galho. As dependências diretas são os **Galhos 4, 8 e 9** (linha 150 do roadmap), com o **Galho 10** somando pra fronteira do R2DBC.

**Galho majoritariamente PESQUISA (galho novo) + uma poda cirúrgica pequena.** Diferente dos Galhos 8/9/10 (que podavam troncos densos), aqui o `Tronco a podar` do roadmap é "**nenhum (galho novo)**". O conteúdo nasce de **pesquisa em doc oficial** (Project Reactor, Spring WebFlux, R2DBC, Reactive Streams), não de um tronco a higienizar. A única poda é **cirúrgica**: a seção `## Spring WebFlux — visão geral` de `Backend/Spring Boot.md` (~95-129), deixada **de propósito** pelos Galhos 8/9/10 (com o callout "Não cobrimos em profundidade aqui — WebFlux merece sua própria nota") esperando exatamente este galho.

**A fronteira-assinatura é QUÁDRUPLA.** Os Galhos 4, 8, 9 e 10 plantaram ganchos esperando as notas deste galho. Este galho **linka de volta aos quatro**, sem re-explicar nenhum:

- **Galho 4 (o modelo de threads e o confronto reativo vs Virtual Threads):** o **confronto detalhado** (backpressure, operadores, quando reativo ainda vence) que a nota 12 do Galho 4 explicitamente adiou → [[03-Dominios/Java/Concorrência e paralelismo/12 - Virtual Threads e Project Loom|Virtual Threads e Project Loom]]; o **modelo de memória / visibilidade** que o reativo também precisa respeitar → [[03-Dominios/Java/Concorrência e paralelismo/11 - Java Memory Model em profundidade|Java Memory Model]]; pools/threads → o galho [[03-Dominios/Java/Concorrência e paralelismo/index|Concorrência e paralelismo]]. **Loom não se re-explica** — a nota 14 deste galho paga a dívida do confronto honesto.
- **Galho 9 (o stack web imperativo que o WebFlux substitui):** **Spring MVC vs WebFlux** (servlet/bloqueante vs reativo/não-bloqueante) → [[03-Dominios/Java/Web e APIs REST/01 - O que é Spring MVC — a camada web sobre o container|O que é Spring MVC]]; **DispatcherServlet vs DispatcherHandler** → [[03-Dominios/Java/Web e APIs REST/06 - O pipeline do DispatcherServlet|O pipeline do DispatcherServlet]]; **RestClient síncrono vs WebClient reativo** → [[03-Dominios/Java/Web e APIs REST/15 - Clientes HTTP — RestClient, WebClient, RestTemplate|Clientes HTTP]]. O MVC imperativo é o ponto de partida; o WebFlux é a alternativa.
- **Galho 10 (a persistência bloqueante que o R2DBC contrasta):** **JPA/JDBC bloqueante vs R2DBC reativo** → [[03-Dominios/Java/Persistência de dados/01 - O que é a camada de persistência — Spring Data, JPA e Hibernate|O que é a camada de persistência]]; o **persistence context / EntityManager** que o R2DBC **não tem** → [[03-Dominios/Java/Persistência de dados/03 - O persistence context e os estados da entidade|O persistence context]]; **lazy loading** que o R2DBC **não suporta** → [[03-Dominios/Java/Persistência de dados/07 - Fetch strategies — LAZY, EAGER e a LazyInitializationException|Fetch strategies]]. O R2DBC é o contraponto reativo, sem o cache de 1º nível.
- **Galho 8 (o container/auto-config sob o WebFlux):** o **starter/auto-configuration** que liga o stack reativo → [[03-Dominios/Java/Spring Core e Boot/15 - Auto-configuration e starters|Auto-configuration e starters]]; o **ApplicationContext** (o mesmo container, beans reativos) → [[03-Dominios/Java/Spring Core e Boot/06 - ApplicationContext — o container e seu ciclo|ApplicationContext]]. O WebFlux roda sobre o mesmo container IoC.

Os Galhos 4, 8, 9 e 10 deixaram **ganchos "Galho 11 (planejado)" / "WebFlux (planejado)" / "R2DBC (planejado)"** em texto esperando exatamente esses wikilinks (dívida reversa — §3.5). Este galho **quita** essa dívida.

**Tese central honesta (cravar via pesquisa, ZERO hype).** Programação reativa resolve I/O-bound com poucos threads (backpressure, streaming, composição não-bloqueante), mas os **Virtual Threads (Java 21 GA, JEP 444)** tornaram o modelo **imperativo** viável pra alta concorrência **sem** a complexidade do Reactor. Então **"quando NÃO usar reativo" é metade do galho**: o custo cognitivo (debugging, stack traces fragmentados, curva da equipe) só se paga quando o ganho é real (backpressure de verdade, streaming, um stack já reativo de ponta a ponta). **Sem estatística de adoção inventada** ([[feedback_no_fabrication]]) — a própria doc do Spring comenta a posição dos Virtual Threads; é dela e do confronto técnico que a tese se funda, não de "X% das empresas migraram".

Programação reativa na JVM é o **modelo push, assíncrono e não-bloqueante**: dados como um stream (`Publisher`) que empurra eventos a um `Subscriber` sob controle de demanda (`request(n)` — backpressure), composto declarativamente por operadores. O Project Reactor (`Mono`/`Flux`) implementa o Reactive Streams; o Spring WebFlux constrói uma camada web não-bloqueante sobre o Netty; o R2DBC leva o modelo reativo ao banco relacional. Depende dos Galhos 4 (threads), 8 (container) e 9 (web).

## 2. Objetivo

Produzir, em uma sessão de execução dedicada, **16 notas atômicas + 1 MOC do galho + expansão do Dicionário de Java + ativação do MOC central + poda cirúrgica da seção WebFlux do `Spring Boot.md` + quitação da dívida reversa**, em `03-Dominios/Java/Programação Reativa/` e `03-Dominios/Java/`, todas `publish: true`, em PT-BR, distribuídas em 3 fases (**4 Iniciado + 8 Adepto + 4 Magus**).

Ao terminar o galho, o leitor deve conseguir:

- **Explicar em inglês** o que é programação reativa (push/não-bloqueante vs pull/bloqueante), o Reactive Streams (as 4 interfaces e o `Flow` do Java 9), `Mono` vs `Flux`, o que é backpressure e por que `map`≠`flatMap`.
- **Reconhecer o que este galho confronta no Galho 4**: dado um cenário de alta concorrência I/O-bound, decidir entre **reativo** (backpressure nativo, streaming) e **Virtual Threads** (imperativo simples, debugging normal) — e justificar **sem hype**.
- **Reconhecer o que este galho substitui no Galho 9**: dado o stack MVC (DispatcherServlet, thread-per-request, RestClient), apontar o equivalente reativo (DispatcherHandler, event loop, WebClient) e por que os dois **não se misturam**.
- **Reconhecer o que o R2DBC perde vs a JPA do Galho 10**: sem `EntityManager`, sem persistence context (cache de 1º nível), sem dirty checking, sem lazy loading — e por que isso é o preço do não-bloqueante.
- **Projetar uma request reativa de ponta a ponta no WebFlux**: controller reativo → `WebClient`/R2DBC → operadores e error handling → backpressure → resposta `Flux`, sem bloquear o event loop.
- **Diagnosticar armadilhas clássicas**: bloquear o event loop (chamar `.block()` ou JDBC num handler reativo), esquecer de fazer `subscribe` (nada acontece), confundir `map` com `flatMap`, perder o contexto de thread com `subscribeOn`/`publishOn`, stack trace inútil, adotar reativo por hype num CRUD onde MVC+VT resolvia.

A barra é "explicar o modelo, decidir reativo-vs-imperativo com critério honesto, e montar uma request reativa que não bloqueia o event loop" — não "escrever um operador customizado do Reactor".

## 3. Saídas concretas

### 3.1. Notas (`03-Dominios/Java/Programação Reativa/`)

Pasta **nova**, flat. 16 notas + 1 MOC (`index.md`, obrigatório pro folder-link do Quartz). Numeração global por galho (não reinicia por fase).

#### Iniciado (4 notas — o modelo mental)

| # | Nota | Escopo nuclear |
|---|------|----------------|
| 01 | O que é programação reativa — o modelo push, assíncrono e não-bloqueante | A mudança de modelo: pull/imperativo/bloqueante (pede e espera) → push/declarativo/não-bloqueante (reage a eventos); dados como stream; por que I/O-bound com poucos threads. **Nota-assinatura da QUÁDRUPLA fronteira:** o modelo de threads é do Galho 4, o stack imperativo é do Galho 9, a persistência bloqueante é do Galho 10. Linka G4 (nota 12), G9 (nota 01). |
| 02 | Reactive Streams — a spec das 4 interfaces e o `Flow` do Java 9 | `Publisher`/`Subscriber`/`Subscription`/`Processor` (a interface de 4 métodos: `onSubscribe`/`onNext`/`onError`/`onComplete`); a spec **absorvida em `java.util.concurrent.Flow`** (Java 9 — WebFetch); Reactor é **uma** implementação (RxJava/Akka Streams são outras); a spec define o **contrato de backpressure**. |
| 03 | Mono e Flux — os publishers do Project Reactor | `Mono` (0-1 elemento) vs `Flux` (0-N); criação (`just`, `fromIterable`, `defer`, `empty`, `error`, `fromCallable`); o tipo como **contrato** (cardinalidade no sistema de tipos); marble diagrams como linguagem. **Version-specific (Reactor 3.x — WebFetch).** |
| 04 | Nada acontece até o `subscribe` — lazy, assembly vs subscription, cold vs hot | A armadilha fundamental: a pipeline é **lazy** — declarar operadores não executa nada; só o `subscribe()` (ou o framework, no WebFlux) dispara; **assembly time** (montar) vs **subscription time** (rodar); **cold** (cada subscriber refaz) vs **hot** (compartilham o mesmo fluxo). |

#### Adepto (8 notas — operadores, fluxo e a camada web)

| # | Nota | Escopo nuclear |
|---|------|----------------|
| 05 | `map` e `flatMap` — transformando o fluxo *(opus)* | A confusão central do reativo: **`map`** (transformação síncrona 1:1, `T → R`) vs **`flatMap`** (transformação assíncrona que retorna outro publisher, `T → Publisher<R>`, achatado); por que aninhar publishers (uma chamada reativa dentro de outra) **exige** `flatMap`; `concatMap`/`flatMapSequential` (ordem); `transform`/`then`. |
| 06 | Combinando publishers — `zip`, `merge`, `concat`, `filter` | Composição de múltiplos streams: **`zip`** (combina elemento-a-elemento, espera os dois), **`merge`** (intercala conforme chegam), **`concat`** (um após o outro, ordenado); `filter`/`take`/`skip`/`distinct`; quando ordem importa. |
| 07 | Error handling reativo — `onErrorResume`, `onErrorReturn`, `retry` | O erro é um **sinal terminal** (`onError` encerra o fluxo); recuperação **declarativa**: `onErrorReturn` (valor fallback), `onErrorResume` (publisher fallback), `onErrorMap` (traduzir), `retry`/`retryWhen` (re-subscribe), `doOnError` (efeito sem recuperar); vs `try/catch` imperativo. Linka **G9** (exception handling MVC — `@ControllerAdvice` não pega sinal reativo igual). |
| 08 | Schedulers — `subscribeOn`, `publishOn` e em qual thread o código roda *(opus)* | O threading do Reactor: por **default roda na thread que chamou `subscribe`**; **`subscribeOn`** (afeta a origem, o início) vs **`publishOn`** (troca a thread daí pra baixo); os `Schedulers` (`parallel()`, `boundedElastic()` pra envolver código **bloqueante**, `single()`, `immediate()`); por que **nunca bloquear o event loop**. Linka **G4** (pools, threads — o reativo multiplexa poucos threads). |
| 09 | Backpressure — `request(n)` e as estratégias BUFFER/DROP/LATEST *(opus)* | O **coração** do Reactive Streams: o `Subscriber` controla a **demanda** via `request(n)` — o produtor não empurra mais do que o consumidor aguenta; o que acontece quando o produtor é mais rápido (overflow): **`onBackpressureBuffer`/`Drop`/`Latest`/`Error`**; `Flux.create` com `FluxSink`. Linka **G4** (o que os Virtual Threads **não** dão nativo — a nota 12 do G4 marca "backpressure: não nativo" nos VT). |
| 10 | Spring WebFlux — o stack não-bloqueante sobre Netty e o `DispatcherHandler` *(opus)* | O stack reativo: **event loop** (Netty, poucos threads) vs **thread-per-request** (servlet, Galho 9); **`DispatcherHandler`** vs **`DispatcherServlet`** (o mesmo papel, modelo diferente); controllers anotados reativos (`@RestController` retornando `Mono<T>`/`Flux<T>`); SSE/streaming. **Substitui o Galho 9.** Linka **G9** (notas 01/06), **G8** (auto-config/container). **Version-specific (Spring Boot 3.x — WebFetch).** |
| 11 | WebClient — o cliente HTTP reativo a fundo | O cliente não-bloqueante do WebFlux: `WebClient.create()`, `get()/post()`, `retrieve()`, **`bodyToMono`/`bodyToFlux`**, `exchangeToMono`; streaming de respostas; error handling (`onStatus`); vs **`RestClient` síncrono** (Galho 9 nota 15 — mesma API fluent, modelo oposto); quando o WebClient num stack imperativo é o "pior dos dois mundos". Linka **G9 nota 15**. |
| 12 | Functional endpoints — `RouterFunction` e `HandlerFunction` | A alternativa **funcional** aos controllers anotados no WebFlux: roteamento como **código** (`RouterFunctions.route().GET(...).build()`), `HandlerFunction` (`ServerRequest → Mono<ServerResponse>`); quando preferir functional (roteamento dinâmico, composição) vs anotado (familiar, Galho 9). Linka **G9** (controllers anotados). |

#### Magus (4 notas — persistência reativa, o confronto e a decisão)

| # | Nota | Escopo nuclear |
|---|------|----------------|
| 13 | R2DBC — persistência reativa sem `EntityManager` *(opus)* | Acesso **reativo** a banco relacional: o driver R2DBC (não-bloqueante, vs JDBC bloqueante), `R2dbcRepository` (Spring Data R2DBC), `DatabaseClient`; **o que NÃO existe**: sem `EntityManager`, sem persistence context (cache de 1º nível), sem dirty checking, **sem lazy loading** (relacionamentos resolvidos manualmente), sem `@OneToMany` automático; transações reativas (`TransactionalOperator`/`@Transactional` reativo). **Contraste direto com o Galho 10.** Linka **G10** (notas 01/03/07). **Version-specific (R2DBC / Spring Data R2DBC — WebFetch).** |
| 14 | Reativo vs Virtual Threads — o confronto honesto *(opus)* | **Paga a dívida do Galho 4 nota 12.** O confronto detalhado: ambos resolvem I/O-bound com poucos threads do SO, mas por caminhos opostos — reativo (operadores, backpressure nativo, legibilidade de cadeia, debugging difícil) vs Virtual Threads (Java 21 GA, código bloqueante normal, stack trace normal, sem backpressure nativo); **onde reativo AINDA vence** (streaming, backpressure de verdade, stack já reativo); **onde VT venceu** (a maioria dos CRUDs de alta concorrência). **Sem hype, sem estatística inventada.** Linka **G4 nota 12** (o confronto que ela adiou). |
| 15 | Quando (não) usar reativo — custo cognitivo, debugging e stack traces | **A "metade do galho".** Os custos reais: **stack traces fragmentados** (a thread que estoura não é a que montou — `Hooks.onOperatorDebug()`/checkpoints), debugging difícil (não dá pra dar step num pipeline lazy), curva da equipe, libs bloqueantes contaminam o event loop; o ganho real precisa **justificar** o custo; o checklist de decisão honesto. Linka **G4** (VT como alternativa), **G9** (MVC como default). |
| 16 | Capstone — uma request reativa de ponta a ponta no WebFlux *(opus, híbrido trace + checklist)* | **Trace:** `GET /orders` → `DispatcherHandler` → `@RestController` reativo → `WebClient` (chama serviço externo) + `R2dbcRepository` (banco reativo) → operadores (`flatMap`/`zip`) + error handling → backpressure → `Flux<OrderDto>` serializado → event loop → cliente; **sem bloquear** em nenhum ponto. **Checklist de design production-grade:** nunca `.block()` num handler, `boundedElastic()` pra qualquer lib bloqueante inevitável, error handling no fim da cadeia, backpressure consciente, `subscribe` é do framework. **Tabela "Galho 11 (reativo) ↔ equivalente imperativo (Galhos 9/10) + o confronto com VT (Galho 4)"**. Cheatsheet nota→problema. Munição de entrevista. **WebFetch.** |

**Notas opus (7):** 05 (map/flatMap — a confusão central), 08 (Schedulers — threading sutil), 09 (Backpressure — o coração), 10 (WebFlux — o stack), 13 (R2DBC — o contraste com G10), 14 (Reativo vs VT — a tese, paga dívida do G4), 16 (capstone síntese). As demais → sonnet. **Toda** nota version-specific (02 `Flow` Java 9, 03 Reactor 3.x, 10 WebFlux/Boot 3.x, 11 WebClient, 13 R2DBC, 14 VT Java 21, 16) faz WebFetch no Step 1 independentemente do modelo.

**Decisões de fronteira (escopo de outro dono — texto "(planejado)" sem wikilink, OU link-back sem re-explicar):**
- **Threads / Virtual Threads / Loom / o Memory Model / pools** → Galho 4 (COMPLETO). **Linkar de volta, nunca re-explicar Loom.** Primeira face da fronteira-assinatura; a nota 14 paga a dívida do confronto.
- **Spring MVC / DispatcherServlet / RestClient / serialização / content negotiation** → Galho 9 (COMPLETO). **Linkar de volta** (MVC imperativo vs WebFlux reativo). Segunda face.
- **JPA / Hibernate / EntityManager / persistence context / `@Transactional` (JPA) / JDBC / lazy loading** → Galho 10 (COMPLETO). **Linkar de volta** (bloqueante vs R2DBC reativo). Terceira face.
- **Container / IoC / AOP / auto-config / starters** → Galho 8 (COMPLETO). **Linkar de volta** (o WebFlux roda sobre o mesmo container). Quarta face.
- **Mensageria reativa / Reactor Kafka / Spring Cloud Stream reativo** → Galho 14 (planejado, texto). O streaming aqui é HTTP/SSE, não broker.
- **Resiliência / circuit breaker reativo / backpressure distribuído / Resilience4j reativo** → Galho 16 (planejado, texto). O backpressure aqui é in-process (Reactive Streams), não distribuído.
- **Segurança reativa (Spring Security WebFlux / `ReactiveSecurityContext`)** → Galho 12 (planejado, texto).
- **Testes reativos (`StepVerifier` / `@WebFluxTest`)** → Galho 13 (planejado, texto — citar que se testa com `StepVerifier`, sem ensinar a stack).

### 3.2. MOC do galho

`03-Dominios/Java/Programação Reativa/index.md`:
- `type: moc`, `status: growing`
- Frontmatter padrão (`title: "Programação Reativa"`, tags `java`/`reativa`/`moc`, aliases `["Programação Reativa", "Reactive Programming", "Project Reactor", "Spring WebFlux", "Galho 11 - Reativa"]`)
- TL;DR callout (galho cobre o modelo reativo na JVM: o que é reativo e o Reactive Streams, `Mono`/`Flux` e os operadores, schedulers e backpressure, Spring WebFlux e WebClient, R2DBC, e o confronto honesto reativo vs Virtual Threads — quando usar e quando NÃO)
- "Sobre este galho" + audiência primária/secundária + nota de que é **galho novo (majoritariamente pesquisa)** com uma poda cirúrgica (a seção WebFlux do `Spring Boot.md`) e de **quádrupla fronteira** (confronta o modelo de threads do Galho 4, substitui o stack web do Galho 9, contrasta a persistência do Galho 10, roda sobre o container do Galho 8) + a **tese central** (Virtual Threads mudaram o cálculo — reativo virou nicho)
- Conteúdo agrupado em 3 H2 (`## Iniciado` / `## Adepto` / `## Magus`) com wikilinks pras 16 notas (uma linha descritiva cada)
- **Rotas alternativas (5):**
  - **Completa** — 01 → 16 em ordem
  - **Entrevista internacional** — 01 → 03 → 05 → 09 → 10 → 14 → 16 (modelo, Mono/Flux, map/flatMap, backpressure, WebFlux, reativo-vs-VT, capstone — o que mais cai)
  - **Os operadores do Reactor** — 03 → 04 → 05 → 06 → 07 → 08 (Mono/Flux, lazy, map/flatMap, combinação, erro, schedulers)
  - **O stack web reativo** — 01 → 10 → 11 → 12 → 13 → 16 (modelo, WebFlux, WebClient, functional, R2DBC, capstone)
  - **Reativo vs Virtual Threads** (a ponte com o Galho 4) — 01 → 09 → 14 → 15 + nota 12 do Galho 4 (a decisão honesta)
- "Veja também": MOC central `[[03-Dominios/Java/index|Trilha Java]]`, **Galho 4** (Concorrência — o modelo de threads e o confronto VT), **Galho 9** (Web e APIs REST — o stack imperativo que o WebFlux substitui), **Galho 10** (Persistência — a JPA bloqueante que o R2DBC contrasta), **Galho 8** (Spring Core e Boot — o container sob o WebFlux), Dicionário de Java; Galhos 12/13/14/16 como texto "(planejado)" sem wikilink
- Dataview "Todas as notas do galho"

### 3.3. Dicionário de Java (EXPANSÃO — não recriar)

`03-Dominios/Java/Dicionário de Java.md` já existe (**296 verbetes** após o Galho 10, `type: glossary`, `updated: 2026-06-09`, seções alfabéticas únicas `## A`…`## Z` com verbetes `### `). Este galho **expande** o arquivo existente inserindo os verbetes **em ordem alfabética case-insensitive (sem acento)** nas seções de letra apropriadas. **Nunca recriar o arquivo nem reordenar verbetes existentes.** Atualizar `updated` no frontmatter para `2026-06-10`.

Verbetes a inserir (~28, conferir dups antes):

`assembly time / subscription time`, `backpressure`, `boundedElastic (Scheduler)`, `cold publisher / hot publisher`, `concatMap`, `DatabaseClient (R2DBC)`, `DispatcherHandler`, `event loop`, `Flow (java.util.concurrent)`, `Flux`, `flatMap (reativo)`, `functional endpoint (RouterFunction)`, `map (reativo)`, `marble diagram`, `merge / concat / zip`, `Mono`, `Netty`, `non-blocking I/O`, `onBackpressureBuffer / Drop / Latest`, `onErrorResume / onErrorReturn`, `Processor (Reactive Streams)`, `Project Reactor`, `Publisher / Subscriber / Subscription`, `publishOn / subscribeOn`, `R2DBC`, `R2dbcRepository`, `Reactive Streams`, `request(n) (demanda)`, `retry / retryWhen`, `Scheduler (Reactor)`, `Spring WebFlux`, `StepVerifier`, `WebClient`.

Cada verbete: definição curta (1-3 linhas) em PT-BR + `Veja também:` apontando pra(s) nota(s) canônica(s) do galho. **Conferir com grep os verbetes já existentes** (possíveis cruzamentos: `WebClient`/`RestClient` (Galho 9 — `WebClient` pode já ter menção; complementar/linkar), `Virtual Threads` (Galho 4 — linkar de `backpressure`/nota 14, **não duplicar**), `@Transactional` (Galhos 8/10 — a transação reativa é diferente, linkar)) para **não duplicar** — quando um termo reativo tocar um já existente, **linkar entre si** em vez de criar segundo verbete. **Conferir 1:1** que os headings dos verbetes batem EXATAMENTE com as âncoras `[[Dicionário de Java#...]]` usadas nas notas (extrair as âncoras das notas via grep e conferir, como nos Galhos 4-10).

### 3.4. MOC central (ativação do Galho 11)

`03-Dominios/Java/index.md` já existe. Task **mínima**: trocar a linha do item 11 (atualmente `11. Programação Reativa *(planejado)* — Reactor, WebFlux, backpressure, R2DBC`) por wikilink ativo no padrão dos galhos fechados:

```markdown
11. [[03-Dominios/Java/Programação Reativa/index|Programação Reativa]] — o modelo reativo na JVM: Reactive Streams, Project Reactor (Mono/Flux e operadores), schedulers e backpressure, Spring WebFlux e WebClient, R2DBC, e o confronto honesto reativo vs Virtual Threads
```

Atualizar `updated` para `2026-06-10`. Não mexer no resto do MOC central (galhos 12-17 permanecem "(planejado)").

### 3.5. Dívida reversa (ganchos "Galho 11 / WebFlux / R2DBC / planejado") + poda cirúrgica

Pré-flight localizou **a poda cirúrgica + 13 ponteiros** (incl. 3 parágrafos de fronteira) a quitar após as notas existirem.

#### 3.5.1. Poda CIRÚRGICA — `Backend/Spring Boot.md` (seção WebFlux)

**Poda mínima — uma única seção.** Substituir `## Spring WebFlux — visão geral` (linhas ~95-129: intro "Alternativa reativa ao Spring MVC", Quando usar / Quando NÃO usar, o exemplo `ReactiveController` com `Mono`/`Flux`, e o callout "Não cobrimos em profundidade aqui — WebFlux merece sua própria nota"), do heading `## Spring WebFlux` até imediatamente antes do próximo `## ` (`## Spring Cloud — visão geral`, ~131), por callout `[!nota] Migrado para galho próprio` + wikilinks pras notas do galho:

```markdown
## Spring WebFlux — visão geral

> [!nota] Migrado para galho próprio
> Expandido no galho [[03-Dominios/Java/Programação Reativa/index|Programação Reativa]]. Veja [[03-Dominios/Java/Programação Reativa/10 - Spring WebFlux — o stack não-bloqueante sobre Netty e o DispatcherHandler|Spring WebFlux]], [[03-Dominios/Java/Programação Reativa/01 - O que é programação reativa — o modelo push, assíncrono e não-bloqueante|O que é programação reativa]] e o confronto honesto [[03-Dominios/Java/Programação Reativa/14 - Reativo vs Virtual Threads — o confronto honesto|Reativo vs Virtual Threads]].
```

**NÃO TOCAR no `Spring Boot.md` (menções incidentais a WebFlux fora da seção-core):**
- linha ~35 (diagrama da arquitetura Spring — `Spring WebFlux, Spring Expression Language, JDBC template`) — **deixar intacta**;
- linha ~735 (sob `## Quando usar` — `**Spring WebFlux:** quando precisa de non-blocking I/O...`) — **deixar intacta** (é uma menção de uma linha numa lista de "quando usar cada projeto", não a seção core);
- callouts dos Galhos 8/9 (`## O que é`/IoC/AOP/`## Gerenciamento de transações` (callout do Galho 10)/Config/Actuator/`## Spring MVC pipeline`) → **intactos**;
- `## Spring Cloud — visão geral` (incl. OpenFeign) → Galho 16; `## Camadas típicas`/`## Troubleshooting`/`## Quando usar`/`## Armadilhas comuns`/`## How to explain in English`/`## Recursos` → **intactos**.

**Atualizar `updated: 2026-06-10`** e adicionar wikilink `[[03-Dominios/Java/Programação Reativa/index|Programação Reativa]]` no `## Veja também` do tronco (se já não houver). Confirmar os números de linha na execução (política §9 do roadmap — ler antes de podar). Não tocar em `Backend/Spring Data JPA.md` (hub do Galho 10), `Backend/Spring Security.md` (Galho 12), `Backend/Kafka/` (Galho 14).

#### 3.5.2. Dívida reversa inline (13 ponteiros → wikilinks)

| # | Arquivo:linha | Texto atual (resumo) | Vira wikilink pra |
|---|---|---|---|
| 1 | `index.md` item 11 (MOC central) | `11. Programação Reativa *(planejado)*` | ativação (§3.4) |
| 2 | `Concorrência e paralelismo/12 - Virtual Threads:81` (callout) | "O confronto detalhado ... pertence ao **Galho 11 — Programação Reativa**" | **nota 14** (Reativo vs Virtual Threads — paga a dívida do confronto) |
| 3 | `Concorrência e paralelismo/index.md:91` | "- Programação Reativa (Galho 11) — planejado." | **MOC do galho** |
| 4 | `Web e APIs REST/01 - O que é Spring MVC:104` | "...o **WebFlux** (Galho 11, planejado), construído sobre Reactor..." | **nota 10** (WebFlux) |
| 5 | `Web e APIs REST/01 - O que é Spring MVC:188` | comentário de código "// WebFlux (Galho 11, planejado) usaria outro starter e Mono<Order>." | **nota 10** (manter o comentário, trocar o texto pelo wikilink) |
| 6 | `Web e APIs REST/15 - Clientes HTTP:23` | "O `WebClient` é o cliente reativo ... uso reativo/streaming = Galho 11, planejado" | **nota 11** (WebClient) |
| 7 | `Web e APIs REST/15 - Clientes HTTP:113` | heading "### WebClient: menção — reativo, do WebFlux (uso reativo/streaming = Galho 11, planejado)" | simplificar o heading (remover "(... Galho 11, planejado)") e pôr o wikilink **na linha 127** (não pôr wikilink no heading) |
| 8 | `Web e APIs REST/15 - Clientes HTTP:127` | "O uso aprofundado do `WebClient` ... é tema do Galho 11 (planejado)." | **nota 11** (WebClient) |
| 9 | `Web e APIs REST/15 - Clientes HTTP:274` | "Reserve o `WebClient` para quando o serviço inteiro for reativo (tema do Galho 11, planejado)." | **nota 11** ou MOC |
| 10 | `Web e APIs REST/15 - Clientes HTTP:303` | "O uso reativo/streaming do `WebClient` (WebFlux/Reactor) é tema do Galho 11 (planejado)." (o Feign/Galho 16 na mesma frase **permanece** texto) | **nota 10/11** (manter Galho 16 como "(planejado)") |
| P1 | `Concorrência e paralelismo/index.md:91` | (= ponteiro 3 — é o horizonte-list de uma linha; **vira wikilink pro MOC**, não é "intocável" aqui) | **MOC do galho** |
| P2 | `Spring Core e Boot/index.md:32` (parágrafo fronteira) | "Spring Reativa com WebFlux (Galho 11) ... planejados" | trecho do Galho 11 → wikilink pro **MOC do galho** |
| P3 | `Web e APIs REST/index.md:32` (parágrafo fronteira) | "Spring Reativa/WebFlux (Galho 11) ... planejados" | trecho do Galho 11 → wikilink pro **MOC do galho** |
| P4 | `Persistência de dados/index.md:32` (parágrafo fronteira) | "Persistência reativa/R2DBC (Galho 11) ... planejados" | trecho do Galho 11 → wikilink pro **MOC do galho** (ou nota 13 R2DBC) |

**Não tocar nos horizonte-lists de uma linha** (`Spring Core e Boot/index.md:97`, `Web e APIs REST/index.md:95`, `Persistência de dados/index.md:92`) — são listas-resumo de galhos futuros; 12/13/14/16/17 permanecem "(planejado)" lá (e o Galho 11 também, se aparecer junto — **mas se o item for SÓ o Galho 11**, ativar; conferir na execução). **Exceção:** o `Concorrência/index.md:91` é um item dedicado SÓ ao Galho 11 ("- Programação Reativa (Galho 11) — planejado.") → **ativar** (vira wikilink pro MOC). Em todos os pontos, manter como texto "(planejado)" qualquer referência a galhos **ainda** inexistentes (12/13/14/16/17). Confirmar os números de linha na execução via grep `"Galho 11"`/`"planejado"`/`"WebFlux"`/`"R2DBC"`/`"reativ"`.

## 4. Convenções por nota

Herda §7 do roadmap e §4 dos specs dos Galhos 8/9/10. Reforços específicos:

### 4.1. Frontmatter

```yaml
---
title: "<título>"
created: 2026-06-10
updated: 2026-06-10
type: concept
progress: backlog
status: seedling
publish: true
fase: iniciado | adepto | magus
tags:
  - java
  - reativa
  - <fase>
  - <tags específicas: reactor, reactive-streams, mono-flux, operadores, backpressure, schedulers, webflux, webclient, r2dbc, virtual-threads, ...>
aliases:
  - <aliases opcionais>
---
```

H1 `# Título` após o frontmatter (padrão dos galhos publicados).

### 4.2. Estrutura H2 obrigatória

- `> [!abstract] TL;DR` (callout, NÃO H2) — 2-4 linhas: conceito + regra prática + por que importa
- `## O que é` / `## Por que importa` / `## Como funciona` (≥3 subseções H3 em notas Adepto/Magus)
- `## Na prática` — exemplos compiláveis; framing **neutro** (`Order`/`Customer`/`Product`/`OrderService`/`OrderRepository`); "padrão observado em apps WebFlux"; NUNCA `Patient`/`MedEspecialista`/"no meu projeto"/1ª pessoa
- `## Armadilhas` — **≥2** (Iniciado) / **≥3** (Adepto/Magus), cada uma `### (N) Título` + descrição + exemplo curto de código demonstrando o problema + fix em 1 linha (H3 numerado, NÃO callout `[!warning]`)
- `## Em entrevista` — subheading `### Frase pronta (inglês)` com **3+ sentenças** (trade-off + decisão + caveat) + subheading `### Vocabulário` com tabela `| Termo PT | Termo EN |` de **6+ termos**
- `## Veja também` — wikilinks **SEM backticks**, SEM âncoras same-file `[[#...]]`; sempre inclui notas relacionadas do galho + `[[03-Dominios/Java/Programação Reativa/index|Programação Reativa (MOC do galho)]]` + `[[03-Dominios/Java/index|Trilha Java]]` + (quando tocar threads/VT) a nota do **Galho 4** + (quando tocar MVC/DispatcherServlet/WebClient) a nota do **Galho 9** + (quando tocar R2DBC/persistência) a nota do **Galho 10** + (quando tocar container/auto-config) a nota do **Galho 8** + verbetes do Dicionário
- `## Referências` — docs oficiais (`projectreactor.io/docs`, `docs.spring.io/spring-framework/reference/web/webflux.html`, `r2dbc.io`, `docs.spring.io/spring-data/r2dbc`, `reactive-streams.org`). Afirmações version-specific fundadas em fonte verificada via WebFetch.

### 4.3. Restrições absolutas

1. **Quádrupla fronteira-assinatura (linkar de volta aos Galhos 4, 8, 9 e 10)** — todo conceito que toca o modelo de threads/VT aponta pra nota do **Galho 4** (sem re-explicar Loom); o que substitui o stack web aponta pro **Galho 9** (MVC vs WebFlux, sem re-explicar DispatcherServlet); o que contrasta a persistência aponta pro **Galho 10** (JDBC/JPA bloqueante vs R2DBC); o que roda no container aponta pro **Galho 8**. Galhos 12-16 = texto "(planejado)", sem wikilink.
2. **Sem fabricação** de experiência pessoal. Exemplos neutros (`Order`, `Customer`, `Product`) — NUNCA `Patient`/`josenaldo`/`MedEspecialista`/1ª pessoa. **Zero estatística de adoção inventada** — vale **dobrado** pra "quando usar reativo" (notas 14/15): **sem** "X% das empresas migraram pra reativo", **sem** "a maioria adota WebFlux", **sem** número de market share. A tese se funda no confronto técnico e na posição documentada do Spring sobre Virtual Threads, não em adoção inventada.
3. **Sem invenção** de APIs/comportamentos. WebFetch obrigatório no Step 1 das notas version-specific (02, 03, 10, 11, 13, 14, 16) e pra **toda afirmação version-specific**. Pontos minados verificados via WebFetch: **Reactor 3.x** (versão atual da família); que o **Reactive Streams foi absorvido em `java.util.concurrent.Flow`** (Java 9); **Spring WebFlux** (baseline Boot 3.x, Netty); **WebClient é o cliente reativo** (vs `RestClient` síncrono, Spring 6.1 — Galho 9); **R2DBC NÃO tem `EntityManager`/lazy/cache de 1º nível**; **Virtual Threads = GA/final no Java 21 (JEP 444)** — cravado no Galho 4; e a **posição atual do Spring sobre Virtual Threads tornarem WebFlux menos necessário** (a própria doc comenta). Nada "de memória".
4. **Code samples compiláveis** — Java moderno (records pra DTO, `var`); imports `reactor.core.publisher.*` (`Mono`/`Flux`), `org.springframework.web.reactive.*`/`org.springframework.web.bind.annotation.*` (WebFlux), `org.springframework.r2dbc.*`/`org.springframework.data.r2dbc.*` (R2DBC); `properties`/`yaml`/`sql` em fences corretas. Marble diagrams em ` ```text ` quando úteis.
5. **Comparações justas** — reativo vs imperativo, `map` vs `flatMap`, `subscribeOn` vs `publishOn`, `Mono` vs `Flux`, WebFlux vs MVC, R2DBC vs JPA, controllers anotados vs functional endpoints, **reativo vs Virtual Threads**: sempre "quando X" E "quando Y". As notas 14/15 são o ápice da honestidade (a tese: VT tornaram reativo nicho — sem hype nem dogma anti-reativo).
6. **Wikilinks sem backticks** em "Veja também"; MOC do galho + MOC central obrigatórios. **Não linkar galhos inexistentes** (12-16) — texto "(planejado)".
7. **Code fences corretos:** ` ```java ` pra código, ` ```sql ` pra schema R2DBC, ` ```properties `/` ```yaml ` pra config, ` ```text ` pra marble diagram/output. Sempre fechadas.
8. **`fase:` no frontmatter + na tag** — obrigatório.
9. **Higiene de commits** — sem `Co-Authored-By: Claude`, sem `--no-verify`, `git add <path>` nominal (nunca `-A` — bot de backup Obsidian Git roda em timer), 1 commit por nota, controlador commita (subagents write-only). Guardar contra `.git/index.lock`.
10. **Tom pedagógico graduado** — Iniciado assume Galhos 1-2 + 4 (threads/VT básicos) + 9 (MVC básico); Magus assume o galho inteiro + Galhos 4 (VT a fundo), 9 (web) e 10 (persistência).

## 5. Conteúdo por nota (síntese)

Esboço do recorte. **Galho novo: tudo nasce de pesquisa** (não há tronco a higienizar, exceto a seção WebFlux do `Spring Boot.md`, que é magra). Afirmações version-specific fundadas em doc oficial via WebFetch. Fontes-base: `projectreactor.io/docs/core/release/reference/`, `docs.spring.io/spring-framework/reference/web/webflux.html`, `r2dbc.io`, `docs.spring.io/spring-data/r2dbc/docs/current/reference/html/`, `reactive-streams.org`.

- **01 — O que é programação reativa (pesquisa).** O modelo push/assíncrono/não-bloqueante vs pull/síncrono/bloqueante; dados como stream que empurra eventos; por que serve I/O-bound (poucos threads, muitas conexões esperando). **A quádrupla fronteira numa frase:** o modelo de threads é do Galho 4, o stack imperativo é do Galho 9, a persistência bloqueante é do Galho 10. Armadilhas: achar que "reativo = mais rápido" (é sobre throughput/recursos, não latência por request); achar que "reativo = assíncrono" (é mais que isso — backpressure). Linka G4 nota 12, G9 nota 01. Fontes: projectreactor.io, reactive-streams.org.
- **02 — Reactive Streams (pesquisa).** As 4 interfaces (`Publisher`/`Subscriber`/`Subscription`/`Processor`) e os 4 sinais (`onSubscribe`/`onNext`/`onError`/`onComplete`); a spec **absorvida em `java.util.concurrent.Flow`** no Java 9 (**WebFetch**); Reactor/RxJava/Akka Streams como implementações; a spec define o contrato de **backpressure** (prenúncio da 09). Armadilhas: implementar `Publisher` na mão (use Reactor); confundir a spec (`Flow`) com a implementação (Reactor). Fontes: reactive-streams.org, JDK `Flow` javadoc.
- **03 — Mono e Flux (pesquisa).** `Mono` (0-1) vs `Flux` (0-N) — cardinalidade no tipo; criação (`just`/`fromIterable`/`defer`/`empty`/`error`/`fromCallable`); marble diagram como linguagem; **Reactor 3.x** (WebFetch). Armadilhas: `Mono.just(expensiveCall())` (avalia eager — use `defer`/`fromCallable`); usar `Flux` onde `Mono` bastava (cardinalidade errada). Fontes: projectreactor.io (Mono/Flux).
- **04 — Nada acontece até o subscribe (pesquisa).** Lazy: declarar operadores não roda nada; `subscribe()` dispara (no WebFlux, o framework subscreve); assembly time vs subscription time; cold (cada subscriber refaz a origem) vs hot (`share()`/`publish()` — compartilham). Armadilhas: esquecer o `subscribe` (pipeline nunca roda — o bug nº1 do iniciante); efeito colateral em `map` esperando que rode no assembly. Fontes: projectreactor.io (subscribe, hot/cold).
- **05 — map e flatMap (pesquisa, opus).** `map` (síncrono, `T → R`) vs `flatMap` (assíncrono, `T → Publisher<R>`, achata); por que uma chamada reativa dentro de outra exige `flatMap` (senão vira `Mono<Mono<T>>`); `concatMap` (ordem)/`flatMapSequential`; `then`/`thenMany`. Armadilhas: `map` com função que retorna `Mono` (vira `Flux<Mono<T>>` — use `flatMap`); `flatMap` quando a ordem importa (use `concatMap`); explosão de concorrência sem `flatMap(fn, concurrency)`. Fontes: projectreactor.io (transforming).
- **06 — Combinando publishers (pesquisa).** `zip` (par a par, espera os dois), `merge` (intercala conforme chegam), `concat` (sequencial, ordenado); `filter`/`take`/`skip`/`distinct`. Armadilhas: `merge` quando precisava de ordem (use `concat`); `zip` com fluxos de tamanhos diferentes (para no menor). Fontes: projectreactor.io (combining).
- **07 — Error handling reativo (pesquisa).** Erro = sinal terminal (`onError` encerra); `onErrorReturn`/`onErrorResume`/`onErrorMap`/`retry`/`retryWhen`/`doOnError`; vs `try/catch`. Linka **G9** (`@ControllerAdvice` no MVC — no WebFlux o tratamento é na cadeia ou no `WebExceptionHandler`). Armadilhas: `try/catch` em volta de uma cadeia reativa (não pega o sinal — use `onError*`); `retry()` infinito sem backoff (use `retryWhen` com backoff); engolir o erro com `onErrorReturn` sem logar. Fontes: projectreactor.io (error handling).
- **08 — Schedulers (pesquisa, opus).** Por default roda na thread do `subscribe`; `subscribeOn` (afeta a origem) vs `publishOn` (troca a thread daí pra baixo); `Schedulers.parallel()`/`boundedElastic()`(bloqueante)/`single()`/`immediate()`; **nunca bloquear o event loop**. Linka **G4** (pools/threads — o reativo multiplexa poucos threads). Armadilhas: chamar JDBC/lib bloqueante num operador sem `boundedElastic()` (trava o event loop); achar que `subscribeOn` troca a thread no meio (é `publishOn`); `subscribeOn` múltiplo (só o primeiro vale). Fontes: projectreactor.io (schedulers).
- **09 — Backpressure (pesquisa, opus).** O coração do Reactive Streams: `request(n)` — o consumidor controla a demanda; overflow: `onBackpressureBuffer`/`Drop`/`Latest`/`Error`; `Flux.create` com `FluxSink` e `OverflowStrategy`. Linka **G4** (a nota 12 marca "backpressure: não nativo" nos Virtual Threads — o que reativo dá e VT não). Armadilhas: produtor rápido + consumidor lento sem estratégia (`OutOfMemory` no buffer default ilimitado); `onBackpressureDrop` perdendo dados sem perceber; ignorar backpressure num `Flux.create`. Fontes: reactive-streams.org, projectreactor.io (backpressure).
- **10 — Spring WebFlux (pesquisa, opus).** Event loop (Netty, poucos threads) vs thread-per-request (servlet, Galho 9); `DispatcherHandler` vs `DispatcherServlet`; `@RestController` reativo retornando `Mono`/`Flux`; SSE/streaming (`text/event-stream`); **Boot 3.x** (WebFetch). Substitui o Galho 9. Linka **G9** (notas 01/06 — MVC/DispatcherServlet), **G8** (auto-config/starter `spring-boot-starter-webflux`). Armadilhas: misturar `spring-boot-starter-web` e `-webflux` (o MVC vence, vira bloqueante); bloquear no handler (`.block()`/JDBC — mata o event loop); achar que WebFlux "é mais rápido" pra request única (não — é throughput). Fontes: docs.spring.io/spring-framework (webflux).
- **11 — WebClient (pesquisa).** `WebClient.create()`/`builder()`, `get()/post()`, `retrieve()`, `bodyToMono`/`bodyToFlux`, `exchangeToMono`, `onStatus`; streaming; vs `RestClient` síncrono (Galho 9 nota 15 — mesma API fluent, modelo oposto); o "pior dos dois mundos" (WebClient + `.block()` num stack imperativo). Linka **G9 nota 15**. Armadilhas: `WebClient` + `.block()` num serviço MVC (use `RestClient`); não tratar `onStatus` (erro HTTP vira `WebClientResponseException`); reusar `WebClient` errado (é thread-safe, crie um). Fontes: docs.spring.io/spring-framework (webflux-webclient).
- **12 — Functional endpoints (pesquisa).** `RouterFunctions.route().GET(...).build()`, `HandlerFunction` (`ServerRequest → Mono<ServerResponse>`); functional (roteamento como código, composição) vs anotado (familiar, Galho 9); quando cada. Linka **G9** (controllers anotados). Armadilhas: misturar functional e anotado sem critério; `ServerResponse` esquecendo de ser reativo; lógica de negócio no router. Fontes: docs.spring.io/spring-framework (webflux-functional).
- **13 — R2DBC (pesquisa, opus).** Driver reativo (não-bloqueante) vs JDBC (bloqueante); `R2dbcRepository`/`DatabaseClient` (Spring Data R2DBC); **o que NÃO existe**: sem `EntityManager`, sem persistence context, sem dirty checking, **sem lazy loading** (relação resolvida manualmente com `flatMap`), sem cache de 1º nível; transações reativas (`TransactionalOperator`). **Contraste direto com o Galho 10.** Linka **G10** (notas 01 — a pilha JPA; 03 — o persistence context que falta; 07 — o lazy que falta). **WebFetch.** Armadilhas: esperar lazy loading do JPA (não existe — resolva com `flatMap`); usar JDBC bloqueante "junto" do R2DBC (mata o ganho); achar que R2DBC é "JPA reativo" (não tem ORM nem cache). Fontes: r2dbc.io, docs.spring.io/spring-data/r2dbc.
- **14 — Reativo vs Virtual Threads (pesquisa, opus).** **Paga a dívida do Galho 4 nota 12.** Ambos: I/O-bound com poucos threads do SO. Reativo: operadores, backpressure nativo, composição, **debugging difícil**, contágio (tudo precisa ser reativo). Virtual Threads (Java 21 GA): código bloqueante normal, stack trace normal, **sem backpressure nativo**, sem contágio. **Onde reativo ainda vence:** streaming real, backpressure de verdade, stack já reativo ponta a ponta. **Onde VT venceu:** a maioria dos CRUDs de alta concorrência. **Sem hype, sem estatística inventada** (a posição do Spring sobre VT é documentada — citar). Linka **G4 nota 12** (o confronto que ela adiou). Armadilhas: adotar reativo "pela performance" num CRUD (VT resolve mais simples); achar que VT "matam" o reativo (streaming/backpressure ainda pedem reativo); comparar latência (é throughput/recursos). Fontes: docs.spring.io (reactive vs virtual threads), openjdk JEP 444 (cravado no Galho 4).
- **15 — Quando (não) usar reativo (pesquisa).** **A metade do galho.** Custos: stack traces fragmentados (`Hooks.onOperatorDebug()`/`checkpoint()` — caro), debugging sem step, curva da equipe, libs bloqueantes contaminam; o ganho precisa justificar; checklist honesto de decisão. Linka **G4** (VT como alternativa), **G9** (MVC como default). Armadilhas: reativo por hype/CV-driven; reativo "pela metade" (uma lib bloqueante no meio anula tudo); subestimar o custo de manutenção/onboarding. Fontes: projectreactor.io (debugging), docs.spring.io.
- **16 — Capstone: uma request reativa de ponta a ponta no WebFlux (pesquisa, opus, híbrido).** **Trace:** `GET /orders` → `DispatcherHandler` → `@RestController` reativo → `WebClient` (serviço externo) + `R2dbcRepository` (banco reativo) → `flatMap`/`zip` + error handling → backpressure → `Flux<OrderDto>` → event loop → cliente; **sem bloquear**. **Checklist production-grade:** nunca `.block()` num handler; `boundedElastic()` pra lib bloqueante inevitável; error handling no fim; backpressure consciente; o `subscribe` é do framework. **Tabela "Galho 11 (reativo) ↔ imperativo (Galhos 9/10) + o confronto com VT (Galho 4)"** (`DispatcherHandler`↔`DispatcherServlet`, `WebClient`↔`RestClient`, R2DBC↔JPA, event loop↔thread-per-request↔Virtual Threads). Cheatsheet nota→problema. Munição de entrevista. Armadilhas de raciocínio: "reativo é sempre melhor pra escala" (VT — nota 14); "é só trocar o tipo de retorno" (o stack inteiro muda); "WebClient é mais rápido" (throughput, não latência). Fontes: docs.spring.io, projectreactor.io.

## 6. Pré-flight: verificações feitas

Executado nesta fase de brainstorming (2026-06-10); itens version-specific re-confirmados na execução de cada nota via WebFetch:

1. **Galho novo confirmado** — `Tronco a podar: nenhum` no roadmap (linha 152). Não há tronco dedicado a higienizar; o conteúdo nasce de pesquisa. **Única poda: cirúrgica** (a seção WebFlux do `Spring Boot.md`).
2. **Poda cirúrgica mapeada** — `Backend/Spring Boot.md` `## Spring WebFlux — visão geral` (linhas 95-129, até antes de `## Spring Cloud` em 131): intro, Quando usar/NÃO usar, exemplo `ReactiveController`, callout "Não cobrimos em profundidade aqui — WebFlux merece sua própria nota". **Deixada de propósito pelos Galhos 8/9/10.** Menções incidentais a preservar: linha 35 (diagrama), 735 (sob `## Quando usar`).
3. **Fabricação no tronco-fonte** — a seção WebFlux do `Spring Boot.md` usa `User`/`ReactiveController` (neutro); **some com a poda**. Notas usam `Order`/`Customer`/`Product`. Nenhuma fabricação de experiência pessoal a carregar (galho de pesquisa).
4. **Dívida reversa localizada** — a poda cirúrgica + 13 ponteiros (§3.5.2), em: MOC central (item 11), Concorrência/12 :81 (callout confronto), Concorrência/index :91 (item dedicado), Web 01 :104/:188, Web 15 :23/:113/:127/:274/:303, e os parágrafos Spring Core index :32 / Web index :32 / Persistência index :32. Horizonte-lists (Spring Core :97, Web :95, Persistência :92) intactos. Confirmar linhas na execução.
5. **Dicionário** — **296 verbetes** após o Galho 10; seções alfabéticas únicas `## A`…`## Z`; verbetes `### `; `updated: 2026-06-09`. Verbetes possivelmente já existentes a conferir/linkar (não duplicar): `WebClient`/`RestClient` (Galho 9), `Virtual Threads` (Galho 4), `@Transactional` (Galhos 8/10 — transação reativa é diferente), `Netty` (Galho 9 — pode existir). Expansão alfabética (~28), nunca recriar/reordenar; conferir âncoras 1:1.
6. **MOC central** — `03-Dominios/Java/index.md` item 11 (`11. Programação Reativa *(planejado)* — Reactor, WebFlux, backpressure, R2DBC`, ~linha 43, no bloco "Fundamentos enterprise e Spring"); galhos ativos usam `N. [[path/index|Title]] — summary`; `updated: 2026-06-09`.
7. **Troncos/notas intocáveis** — `Backend/Spring Data JPA.md` (hub do Galho 10), `Backend/Spring Security.md` (Galho 12), `Backend/Kafka/` (Galho 14), `Backend/Testes em Java.md` (Galho 13); todas as notas dos Galhos 4/8/9/10 (só recebem o link-back/dívida reversa onde mapeado).
8. **Versões a cravar via WebFetch na execução** — Reactor (família 3.x atual); Reactive Streams absorvido em `java.util.concurrent.Flow` (Java 9); Spring WebFlux (baseline Boot 3.x, Netty); WebClient é o cliente reativo (vs `RestClient` síncrono, Spring 6.1); R2DBC / Spring Data R2DBC (versões atuais); Virtual Threads = GA/final Java 21 JEP 444 (cravado no Galho 4); posição documentada do Spring sobre VT e WebFlux. Boot 3.x baseline. Fonte: `projectreactor.io`, `docs.spring.io`, `r2dbc.io`, `reactive-streams.org`. Nada de memória.

Nenhum número de adoção é inventado (vale **dobrado** pras notas 14/15). Quando faltar fato verificável, **PERGUNTAR** antes de escrever.

## 7. Critérios de aceitação do galho

Além dos critérios gerais (§10 do roadmap):

1. 16 notas em `03-Dominios/Java/Programação Reativa/`, frontmatter completo com `fase:`, `publish: true`, distribuídas 4/8/4.
2. MOC do galho com 3 subseções de fase + 5 rotas alternativas + dataview + folder-link resolve (`index.md` presente).
3. Dicionário de Java **expandido** (não recriado) com ~28 verbetes; verbetes dos Galhos 1-10 intactos; `updated: 2026-06-10`; dups conferidos e linkados (não duplicar `WebClient`/`Virtual Threads`/`Netty`/`@Transactional`); headings conferidos 1:1 com as âncoras usadas nas notas (via grep).
4. MOC central `Java/index.md` com Galho 11 ativado (item 11 vira wikilink); resto intacto (12-17 "(planejado)").
5. **Poda cirúrgica executada**: `Spring Boot.md` seção `## Spring WebFlux — visão geral` vira callout. **Menções incidentais intactas** (linha 35 diagrama, 735 "Quando usar"); seções de outros galhos intactas (callouts dos Galhos 8/9/10; Cloud/Camadas típicas/Troubleshooting). `Spring Data JPA.md`/`Spring Security.md`/`Kafka/` intactos.
6. **Dívida reversa quitada**: os 13 ponteiros com wikilinks corretos (Concorrência/12 :81→nota 14; Concorrência/index :91→MOC; Web 01 :104/:188→nota 10; Web 15 :23/:113/:127/:274/:303→nota 11; parágrafos de fronteira→MOC); galhos ainda inexistentes (12-16) permanecem texto "(planejado)"; horizonte-lists intactos.
7. Cada nota: TL;DR; code samples compiláveis (Java moderno, `Mono`/`Flux`, imports `reactor.*`/`org.springframework.web.reactive.*`/R2DBC, fences corretas — `java`/`sql`/`yaml`/`text`); "Em entrevista" com `### Frase pronta (inglês)` 3+ sentenças + `### Vocabulário` tabela 6+ termos PT→EN; "Armadilhas" com exemplo+fix (≥2 Iniciado, ≥3 Adepto/Magus); wikilinks (galho + MOC central + Galho 4 quando tocar threads/VT + Galho 9 quando tocar MVC/WebClient + Galho 10 quando tocar R2DBC + Galho 8 quando tocar container + Dicionário); "Referências" com docs oficiais verificadas.
8. **Quádrupla fronteira-assinatura respeitada**: cada conceito que toca threads/VT linka de volta ao Galho 4 sem re-explicar Loom; o que substitui o web linka o Galho 9; o que contrasta a persistência linka o Galho 10; o que roda no container linka o Galho 8; galhos 12-16 só como texto "(planejado)"; nenhum wikilink pra galho inexistente.
9. **Fronteiras de escopo respeitadas**: backpressure **in-process** (distribuído = Galho 16); streaming **HTTP/SSE** (mensageria/Kafka reativo = Galho 14); segurança reativa = Galho 12; testes reativos (`StepVerifier`/`@WebFluxTest`) só citados = Galho 13; zero conteúdo profundo de Mensageria/Security/Test/Distribuído; **Loom nunca re-explicado** (Galho 4).
10. **Zero fabricação** de experiência pessoal; **zero estatística de adoção inventada** (vale dobrado pras notas 14/15 — sem "X% migraram"); afirmações version-specific citam a versão verificada via WebFetch; **a tese reativo-vs-VT é honesta** (sem hype pró-reativo nem dogma anti-reativo).
11. 1 commit por nota; sem `Co-Authored-By: Claude`; sem `--no-verify`; stage nominal (nunca `-A`); subagents write-only, controlador commita.
12. `verificar-wikilinks` roda limpo na pasta do galho (as quebras legadas da árvore Java NÃO são deste galho; evitar âncoras same-file).

## 8. Riscos e mitigações

| Risco | Mitigação |
|---|---|
| **Re-explicar Loom/Virtual Threads** em vez de linkar de volta ao Galho 4 (1ª face) | Restrição 4.3.1; a nota 14 cobre o **confronto** (reativo vs VT), linkando a nota 12 do Galho 4; review por fase grep `Thread.ofVirtual|carrier thread|pinning` nas notas que não a 14/08. |
| **Re-explicar DispatcherServlet/Spring MVC** em vez de linkar ao Galho 9 (2ª face) | Restrição 4.3.1; a nota 10 cobre o `DispatcherHandler`, **contrastando** com o DispatcherServlet (link), sem reconstruí-lo; review por fase. |
| **Re-explicar JPA/EntityManager/lazy** em vez de linkar ao Galho 10 (3ª face) | Restrição 4.3.1; a nota 13 cobre o que o R2DBC **não tem**, linkando o Galho 10; review por fase. |
| **Hype pró-reativo / dogma anti-reativo** nas notas 14/15 | Restrição 4.3.2/4.3.5; a tese é honesta (reativo virou nicho, mas ainda vence em streaming/backpressure); **zero estatística inventada**; review manual das notas 14/15 grep `% d[ao]s (dev|empresas)|market share|maioria (adota|migrou)`. |
| **Inventar estatística de adoção** ("X% migraram pra reativo/WebFlux") | Restrição 4.3.2 (vale dobrado); a tese se funda no confronto técnico + posição documentada do Spring (WebFetch), não em adoção; review por fase. |
| **Inventar API/versão "de memória"** (Reactor operators, WebFlux, R2DBC, `Flow` no Java 9) | WebFetch no Step 1 das notas version-specific (02/03/10/11/13/14/16) e pra toda afirmação version-specific; baseline Boot 3.x/Reactor 3.x; Referências com fonte oficial. |
| **Bloquear o event loop nos exemplos** (`.block()`/JDBC num handler) ensinando errado | As notas 08/10/13/16 explicitam "nunca bloquear"; exemplos usam `boundedElastic()` pra bloqueante inevitável; review dos code samples. |
| **Poda cirúrgica danificar menções incidentais** no `Spring Boot.md` | Ler o tronco primeiro (§9 roadmap); podar **só** `## Spring WebFlux — visão geral` (95-129); linhas 35/735 e callouts dos Galhos 8/9/10 explicitamente intocáveis. |
| **Invadir Galho 14 (mensageria)** ao falar de streaming, ou **Galho 16** ao falar de backpressure | Streaming = HTTP/SSE (Kafka reativo = Galho 14, texto); backpressure = in-process (distribuído = Galho 16, texto); review por fase. |
| **Invadir Galho 13 (testes)** ao falar de `StepVerifier` | Citar que se testa com `StepVerifier`/`@WebFluxTest`, sem ensinar a stack; Galho 13 (texto). |
| Versões envelhecerem (Boot 3.x vs 4.x, Reactor 3.x) | Baseline 3.x (como Galhos 8/9/10), citando 4.x como "mais recente"; WebFetch por nota version-specific; declarar version-specificity no corpo. |
| Galho denso (16 notas) inflar notas individuais (operadores/WebFlux/R2DBC) | Distribuição 4/8/4 fixada; se uma nota passar de ~600 linhas, dividir nota (não galho — [[feedback_notas_atomicas]]); functional endpoints já separada do WebFlux; reativo-vs-VT separado de quando-não-usar. |
| Dicionário: duplicar verbete já existente (`WebClient`, `Virtual Threads`, `Netty`, `@Transactional`) | Grep dos existentes antes de inserir; quando tocar um existente, **linkar** em vez de duplicar; inserção alfabética, nunca recriar; conferir âncoras 1:1. |
| Bot de backup (Obsidian Git) commitando no meio | Padrão dos Galhos 2-10: subagents write-only; controlador commita imediatamente após cada nota com `git add` nominal (nunca `-A`); guardar contra `.git/index.lock`. |

## 9. Próximos passos

1. **Aprovação deste spec**
2. **Plano de execução** via skill `superpowers:writing-plans` → `docs/superpowers/plans/2026-06-10-java-galho-11-reativa-execution.md`
3. **Execução** via `superpowers:subagent-driven-development` **direto na `main`** (subagents write-only; sonnet por padrão, opus nas notas 05/08/09/10/13/14/16; review **por fase** + fix loop; push manual do usuário)
4. **Verificação** de wikilinks + conferência de âncoras do Dicionário
5. **Atualização da memória** `project_trilha_java` (Galho 11 completo) antes do próximo galho

## 10. Documentos relacionados

- `2026-06-02-java-senior-roadmap-design.md` — roadmap macro (18 galhos)
- `2026-06-09-java-galho-10-persistencia-design.md` / `...-execution.md` — Galho 10 (molde mais recente de galho híbrido com poda + tripla fronteira + dívida reversa; este galho usa-o como template direto)
- `2026-06-08-java-galho-09-web-rest-design.md` — Galho 9 (dependência: o stack MVC imperativo que o WebFlux substitui — notas 01/06/15)
- `2026-06-03-java-galho-04-concorrencia-design.md` — Galho 4 (dependência: o modelo de threads e os Virtual Threads — a nota 12 espera o confronto que a nota 14 deste galho paga)
- `2026-06-08-java-galho-08-spring-core-design.md` — Galho 8 (dependência: o container/auto-config sob o WebFlux)
- Galho 10 (Persistência) — a JPA/JDBC bloqueante que o R2DBC contrasta (notas 01/03/07)
- Artefatos a atualizar: `03-Dominios/Java/Dicionário de Java.md`, `03-Dominios/Java/index.md`, `03-Dominios/Java/Backend/Spring Boot.md` (poda cirúrgica — seção WebFlux), `Concorrência e paralelismo/12 - Virtual Threads e Project Loom`, `Concorrência e paralelismo/index.md`, `Web e APIs REST/01 - O que é Spring MVC`, `Web e APIs REST/15 - Clientes HTTP`, `Spring Core e Boot/index.md`, `Web e APIs REST/index.md`, `Persistência de dados/index.md` (dívida reversa)
- Fontes-base do galho: `projectreactor.io/docs/core/release/reference/`, `docs.spring.io/spring-framework/reference/web/webflux.html`, `r2dbc.io`, `docs.spring.io/spring-data/r2dbc/docs/current/reference/html/`, `reactive-streams.org`
- Memórias: [[project_trilha_java]], [[project_trilhas_fases_aprendizado]], [[project_tronco_galhos_pattern]], [[feedback_galhos_direto_main]], [[feedback_no_fabrication]], [[feedback_quartz_index]], [[feedback_commits]], [[feedback_dataview_inline_code]], [[feedback_notas_atomicas]], [[feedback_enriquecimento_feynman]]
