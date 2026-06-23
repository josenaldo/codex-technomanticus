# Galho 11 — Programação Reativa (Java Senior) — Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Criar o Galho 11 da trilha Java Senior — 16 notas atômicas (o que é reativo, Reactive Streams, Mono/Flux, lazy/subscribe, map/flatMap, combinação, error handling, schedulers, backpressure, Spring WebFlux, WebClient, functional endpoints, R2DBC, reativo vs Virtual Threads, quando não usar, capstone) em 3 fases + MOC do galho + expansão do Dicionário + ativação do MOC central + **poda cirúrgica** da seção WebFlux do `Backend/Spring Boot.md` + **quitação de 13 ponteiros de dívida reversa**.

**Architecture:** Padrão galhos + 3 fases (Iniciado/Adepto/Magus). Pasta flat `03-Dominios/Tecnologia/Java/Programação Reativa/`, notas `publish: true` em PT-BR, numeração global 01-16 (4/8/4). **Galho NOVO — majoritariamente PESQUISA:** o `Tronco a podar` do roadmap é "nenhum"; o conteúdo nasce de doc oficial via WebFetch (Project Reactor, Spring WebFlux, R2DBC, Reactive Streams). Única poda: **cirúrgica** (a seção `## Spring WebFlux — visão geral` do `Spring Boot.md`, deixada de propósito pelos Galhos 8/9/10). **QUÁDRUPLA fronteira-assinatura:** cada conceito que toca threads/VT linka de volta ao **Galho 4** (sem re-explicar Loom); o que substitui o web linka o **Galho 9** (MVC vs WebFlux); o que contrasta a persistência linka o **Galho 10** (JDBC/JPA vs R2DBC); o que roda no container linka o **Galho 8**. **Tese central honesta:** Virtual Threads (Java 21 GA) tornaram reativo nicho — "quando NÃO usar" é metade do galho, sem hype, sem estatística inventada. Galhos 12/13/14/16 = texto "(planejado)", sem wikilink. **Direto na `main`** ([[feedback_galhos_direto_main]]); push manual do usuário.

**Tech Stack:** Obsidian Flavored Markdown, frontmatter YAML, wikilinks, callouts, Dataview, Quartz v4. Verificação via WebFetch (`projectreactor.io/docs`, `docs.spring.io/spring-framework/reference/web/webflux.html`, `r2dbc.io`, `docs.spring.io/spring-data/r2dbc`, `reactive-streams.org`).

---

## Convenções aplicadas a TODAS as notas (ler antes de qualquer task)

**Frontmatter** (ajustar `title`/`fase`/`tags`/`aliases` por nota; `created`/`updated: 2026-06-10`):

```yaml
---
title: "<título sem prefixo numérico>"
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
  - <1-3 tags de conceito: reactor, reactive-streams, mono-flux, operadores, backpressure, schedulers, webflux, webclient, r2dbc, virtual-threads>
aliases:
  - <aliases>
---
```

H1 `# Título` após o frontmatter (padrão dos galhos publicados).

**Estrutura H2 obrigatória** (nesta ordem):

1. `> [!abstract] TL;DR` — 2-4 linhas. Callout, NÃO H2.
2. `## O que é` — definição.
3. `## Por que importa` — relevância pra senior/entrevista. (Pode fundir com "O que é" em Iniciado curtas.)
4. `## Como funciona` — H3s; mínimo 3 em Adepto/Magus.
5. `## Na prática` — código compilável; framing neutro; **NUNCA** 1ª pessoa, `Patient`, `Doctor`, `Appointment`, `Josenaldo`, `MedEspecialista`. Domínios neutros: `Order`, `Customer`, `Product`, `OrderService`, `OrderRepository`. Records pra DTO. Imports `reactor.core.publisher.*` (`Mono`/`Flux`), `org.springframework.web.reactive.*` / `org.springframework.web.bind.annotation.*` (WebFlux), `org.springframework.r2dbc.*` / `org.springframework.data.r2dbc.*` (R2DBC).
6. `## Armadilhas` — ≥2 (Iniciado) / ≥3 (Adepto/Magus). Cada uma: `### (N) Título` + descrição + exemplo curto + fix em 1 linha (H3 numerado, NÃO callout `[!warning]`).
7. `## Em entrevista` — `### Frase pronta (inglês)` com **3+ sentenças** (trade-off + decisão + caveat) + `### Vocabulário` **6+ termos** em tabela `| Termo PT | Termo EN |`.
8. `## Veja também` — wikilinks SEM backticks, SEM âncoras same-file `[[#...]]`. Sempre: notas do galho + `[[03-Dominios/Tecnologia/Java/Programação Reativa/index|Programação Reativa (MOC do galho)]]` + `[[03-Dominios/Tecnologia/Java/index|Trilha Java]]` + (quando tocar threads/VT) a nota do **Galho 4** + (quando tocar MVC/DispatcherServlet/WebClient) a nota do **Galho 9** + (quando tocar R2DBC/persistência) a nota do **Galho 10** + (quando tocar container/auto-config) a nota do **Galho 8** + verbetes do Dicionário.
9. `## Referências` — docs oficiais consultadas (`projectreactor.io/...`, `docs.spring.io/...webflux...`, `r2dbc.io`, `docs.spring.io/spring-data/r2dbc`, `reactive-streams.org`).

**Tamanho:** 200-500 linhas (densas até 600 — limite de [[feedback_notas_atomicas]]).

**Restrições absolutas:**
- **QUÁDRUPLA fronteira-assinatura.** Mapeamento de link-back **Galho 4** (threads/VT, não re-explicar Loom): o confronto reativo vs VT → `Concorrência e paralelismo/12 - Virtual Threads e Project Loom`; visibilidade/memória → `11 - Java Memory Model em profundidade`; pools → `Concorrência e paralelismo/index`. Mapeamento **Galho 9** (o web imperativo): MVC vs WebFlux → `Web e APIs REST/01 - O que é Spring MVC — a camada web sobre o container`; DispatcherServlet vs DispatcherHandler → `Web e APIs REST/06 - O pipeline do DispatcherServlet`; RestClient vs WebClient → `Web e APIs REST/15 - Clientes HTTP — RestClient, WebClient, RestTemplate`. Mapeamento **Galho 10** (a persistência bloqueante): a pilha JPA → `Persistência de dados/01 - O que é a camada de persistência — Spring Data, JPA e Hibernate`; o persistence context que falta → `Persistência de dados/03 - O persistence context e os estados da entidade`; o lazy que falta → `Persistência de dados/07 - Fetch strategies — LAZY, EAGER e a LazyInitializationException`. Mapeamento **Galho 8** (o container): auto-config/starter → `Spring Core e Boot/15 - Auto-configuration e starters`; o container → `Spring Core e Boot/06 - ApplicationContext — o container e seu ciclo`.
- **Galhos 12-16 só como texto "(planejado)", SEM wikilink.** Greps de review checam `\[\[[^]]*(Galho (12|13|14|16)|Spring Security|Reactor Kafka|StepVerifier|circuit breaker|saga)`.
- Sem fabricação ([[feedback_no_fabrication]]); usar `Order`/`Customer`/`Product`. **Zero estatística de adoção inventada** — vale **DOBRADO** pras notas 14/15 (sem "X% migraram pra reativo/WebFlux", sem "a maioria adota", sem market share). A tese reativo-vs-VT se funda no confronto técnico + posição documentada do Spring (WebFetch), não em adoção.
- **Pesquisa pras partes version-specific:** notas 02/03/10/11/13/14/16 fundam-se em WebFetch (Step 1); qualquer outra que cravar versão também confirma. Toda afirmação version-specific verificada: **Reactor 3.x** (família atual); **Reactive Streams absorvido em `java.util.concurrent.Flow`** (Java 9); **Spring WebFlux** (baseline Boot 3.x, Netty); **`WebClient` é o cliente reativo** (vs `RestClient` síncrono, Spring 6.1 — Galho 9); **R2DBC NÃO tem `EntityManager`/lazy/cache de 1º nível**; **Virtual Threads = GA/final Java 21 JEP 444** (cravado no Galho 4); **posição documentada do Spring sobre VT tornarem WebFlux menos necessário**. Boot 4.x já é a release atual — **manter 3.x como baseline** (como os Galhos 8/9/10), citando 4 como "mais recente" quando relevante. Nada de memória.
- **Não re-explicar o que é de outro galho:** threads/VT/Loom/memória/pools → Galho 4 (linkar); Spring MVC/DispatcherServlet/RestClient/serialização → Galho 9 (linkar); JPA/EntityManager/persistence context/lazy/JDBC → Galho 10 (linkar); container/IoC/AOP/auto-config → Galho 8 (linkar); mensageria reativa/Reactor Kafka → Galho 14 (texto); resiliência/circuit breaker reativo/backpressure distribuído → Galho 16 (texto); segurança reativa → Galho 12 (texto); testes reativos (`StepVerifier`/`@WebFluxTest`) → Galho 13 (texto — citar, sem ensinar).
- Comparações justas (quando X E quando Y): reativo vs imperativo, `map` vs `flatMap`, `subscribeOn` vs `publishOn`, `Mono` vs `Flux`, WebFlux vs MVC, R2DBC vs JPA, anotado vs functional, **reativo vs Virtual Threads**.
- Code fences: ` ```java `, ` ```sql ` (schema R2DBC), ` ```properties `/` ```yaml ` (config), ` ```bash `, ` ```text ` (marble diagram/output). Sempre fechadas.
- Commits: sem `Co-Authored-By: Claude`; sem `--no-verify`; `git add <path>` nominal (bot de backup roda em timer — NUNCA `-A`; guardar contra `.git/index.lock`); 1 commit por nota; direto na `main`; **sem push, sem deploy**. Subagents NÃO rodam git — o controlador commita.

**Modelo por nota:** sonnet por padrão; **opus** nas **05** (map/flatMap), **08** (Schedulers), **09** (Backpressure), **10** (WebFlux), **13** (R2DBC), **14** (Reativo vs VT) e **16** (capstone).

**Fontes oficiais (base):**
- Project Reactor reference: `https://projectreactor.io/docs/core/release/reference/`
- Reactor — Mono/Flux/operators: `https://projectreactor.io/docs/core/release/reference/#which-operator`
- Reactor — schedulers/threading: `https://projectreactor.io/docs/core/release/reference/#schedulers`
- Reactor — backpressure/`Flux.create`: `https://projectreactor.io/docs/core/release/reference/#producing`
- Reactor — error handling: `https://projectreactor.io/docs/core/release/reference/#error.handling`
- Reactor — debugging: `https://projectreactor.io/docs/core/release/reference/#debugging`
- Reactive Streams: `https://www.reactive-streams.org/`
- Spring WebFlux: `https://docs.spring.io/spring-framework/reference/web/webflux.html`
- Spring WebClient: `https://docs.spring.io/spring-framework/reference/web/webflux-webclient.html`
- Spring WebFlux functional: `https://docs.spring.io/spring-framework/reference/web/webflux-functional.html`
- R2DBC: `https://r2dbc.io/`
- Spring Data R2DBC: `https://docs.spring.io/spring-data/r2dbc/docs/current/reference/html/`
- Spring — reactive vs Virtual Threads / blocking: `https://docs.spring.io/spring-framework/reference/web/webflux/reactive-spring.html`

---

## Task 0: Pré-flight — pasta, terreno e baselines

**Files:**
- Create: `03-Dominios/Tecnologia/Java/Programação Reativa/` (pasta)

- [ ] **Step 1: Confirmar `main`**

```bash
git branch --show-current
```
Expected: `main`. NÃO criar branch.

- [ ] **Step 2: Criar a pasta do galho**

```bash
mkdir -p "03-Dominios/Tecnologia/Java/Programação Reativa"
```

- [ ] **Step 3: Confirmar títulos exatos das notas dos Galhos 4/8/9/10 (linkadas de volta)**

```bash
ls "03-Dominios/Tecnologia/Java/Concorrência e paralelismo/" | grep -E "^(11|12) "
ls "03-Dominios/Tecnologia/Java/Web e APIs REST/" | grep -E "^(01|06|15) "
ls "03-Dominios/Tecnologia/Java/Persistência de dados/" | grep -E "^(01|03|07) "
ls "03-Dominios/Tecnologia/Java/Spring Core e Boot/" | grep -E "^(06|15) "
```
Expected: G4 — `11 - Java Memory Model em profundidade`, `12 - Virtual Threads e Project Loom`; G9 — `01 - O que é Spring MVC — a camada web sobre o container`, `06 - O pipeline do DispatcherServlet`, `15 - Clientes HTTP — RestClient, WebClient, RestTemplate`; G10 — `01 - O que é a camada de persistência — Spring Data, JPA e Hibernate`, `03 - O persistence context e os estados da entidade`, `07 - Fetch strategies — LAZY, EAGER e a LazyInitializationException`; G8 — `06 - ApplicationContext — o container e seu ciclo`, `15 - Auto-configuration e starters`. Anotar divergências.

- [ ] **Step 4: Relocalizar a dívida reversa (13 ponteiros — linhas podem ter mudado)**

```bash
grep -rn "Galho 11\|galho 11\|WebFlux\|R2DBC\|reativ" "03-Dominios/Tecnologia/Java/Concorrência e paralelismo/12 - Virtual Threads e Project Loom.md" "03-Dominios/Tecnologia/Java/Concorrência e paralelismo/index.md" "03-Dominios/Tecnologia/Java/Web e APIs REST/01 - O que é Spring MVC — a camada web sobre o container.md" "03-Dominios/Tecnologia/Java/Web e APIs REST/15 - Clientes HTTP — RestClient, WebClient, RestTemplate.md" "03-Dominios/Tecnologia/Java/Spring Core e Boot/index.md" "03-Dominios/Tecnologia/Java/Web e APIs REST/index.md" "03-Dominios/Tecnologia/Java/Persistência de dados/index.md"
grep -n "Programação Reativa\|planejado" "03-Dominios/Tecnologia/Java/index.md"
```
Expected (anotar linhas reais pra Task 21): MOC central item 11 (`~43`); Concorrência/12 :~81 (callout confronto); Concorrência/index :~91 (item dedicado); Web 01 :~104/:188; Web 15 :~23/:113/:127/:274/:303; Spring Core index :~32 (parágrafo) e :~97 (horizonte-list — NÃO tocar); Web index :~32 (parágrafo) e :~95 (horizonte-list — NÃO tocar); Persistência index :~32 (parágrafo) e :~92 (horizonte-list — NÃO tocar).

- [ ] **Step 5: Baseline do Dicionário**

```bash
grep -cE "^### " "03-Dominios/Tecnologia/Java/Dicionário de Java.md"
```
Expected: **296** (baseline pós-Galho 10). Anotar o número real.

- [ ] **Step 6: Mapear a seção a podar (pra Task 20) e as menções incidentais a preservar**

```bash
grep -nE "^## " "03-Dominios/Tecnologia/Java/Backend/Spring Boot.md"
grep -niE "webflux|reactive|reactor|r2dbc|mono<|flux<|reativ" "03-Dominios/Tecnologia/Java/Backend/Spring Boot.md"
```
Expected: `## Spring WebFlux — visão geral` (início ~95, fim = imediatamente antes de `## Spring Cloud — visão geral` ~131 — a única seção core deste galho, com intro/Quando usar/Quando NÃO usar/exemplo `ReactiveController`/callout "Não cobrimos em profundidade aqui"). **Menções incidentais a PRESERVAR:** linha ~35 (diagrama da arquitetura) e ~735 (sob `## Quando usar` — `**Spring WebFlux:** quando precisa de non-blocking I/O...`). INTOCÁVEIS: callouts dos Galhos 8/9/10 (`## O que é`/IoC/AOP/`## Gerenciamento de transações`/Config/Actuator/`## Spring MVC pipeline`), `## Spring Cloud`/`## Camadas típicas`/`## Troubleshooting`/`## Quando usar`. Anotar ranges reais.

- [ ] **Step 7: Fixar fatos a verificar via WebFetch** — Reactor 3.x (versão atual); Reactive Streams absorvido em `java.util.concurrent.Flow` (Java 9); Spring WebFlux (baseline Boot 3.x, Netty); `WebClient` é o cliente reativo (vs `RestClient` síncrono, Spring 6.1); R2DBC sem `EntityManager`/lazy/cache; Virtual Threads = GA Java 21 JEP 444 (cravado no Galho 4); posição documentada do Spring sobre VT vs WebFlux. Nada de memória.

- [ ] **Step 8: Sem commit** (preparação).

---

## Fase INICIADO (notas 01-04)

### Task 1: Nota 01 — O que é programação reativa — o modelo push, assíncrono e não-bloqueante

**Files:**
- Create: `03-Dominios/Tecnologia/Java/Programação Reativa/01 - O que é programação reativa — o modelo push, assíncrono e não-bloqueante.md`

- [ ] **Step 1: Pesquisar** — WebFetch `https://projectreactor.io/docs/core/release/reference/` (intro) + `https://www.reactive-streams.org/`. CONFIRMAR: o modelo push/assíncrono/não-bloqueante vs pull/síncrono/bloqueante; dados como stream; por que serve I/O-bound (poucos threads, muitas conexões esperando); reativo é sobre throughput/recursos, não latência por request.

- [ ] **Step 2: Escrever** — `fase: iniciado`, tags `[java, reativa, iniciado, reactor]`, aliases `["programação reativa", "reactive programming", "modelo não-bloqueante"]`. **Nota-assinatura da QUÁDRUPLA fronteira.** Conteúdo:
  - TL;DR: programação reativa é um modelo push/não-bloqueante onde dados fluem como um stream que empurra eventos a quem reage — serve alta concorrência I/O-bound com poucos threads, mas o modelo de threads é do Galho 4, o stack imperativo é do Galho 9 e a persistência bloqueante é do Galho 10.
  - `## O que é` — push vs pull, assíncrono vs síncrono, bloqueante vs não-bloqueante; dados como stream de eventos.
  - `## Por que importa` — escala I/O-bound (muitas conexões esperando) com poucos threads; entrevista cobra "o que é reativo e quando faz sentido".
  - `## Como funciona` — H3s: "Push vs pull: quem controla o fluxo", "Não-bloqueante: por que poucos threads servem muitas conexões", "Reativo ≠ mais rápido: é throughput/recursos, não latência por request", "A quádrupla fronteira: threads (Galho 4), web (Galho 9), persistência (Galho 10), container (Galho 8)".
  - `## Na prática` — um trecho conceitual: um endpoint que retorna `Flux<Order>` vs um que retorna `List<Order>` (```java), mostrando a diferença de modelo (sem aprofundar WebFlux — é a nota 10).
  - `## Armadilhas` — ≥2: (1) achar que "reativo = mais rápido" (é sobre recursos/throughput, não latência por request); (2) achar que "reativo = só assíncrono" (é mais: backpressure, composição declarativa).
  - `## Em entrevista` + `## Veja também` ([[02 - Reactive Streams — a spec das 4 interfaces e o Flow do Java 9]], [[03 - Mono e Flux — os publishers do Project Reactor]], **[[03-Dominios/Tecnologia/Java/Concorrência e paralelismo/12 - Virtual Threads e Project Loom|Virtual Threads e Project Loom]]** (o modelo de threads), **[[03-Dominios/Tecnologia/Java/Web e APIs REST/01 - O que é Spring MVC — a camada web sobre o container|O que é Spring MVC]]** (o stack imperativo), MOC galho, MOC central, verbetes `Project Reactor`/`non-blocking I/O`) + `## Referências`.

- [ ] **Step 3: Verificar**
```bash
grep -cE "^## (O que é|Por que importa|Como funciona|Na prática|Armadilhas|Em entrevista|Veja também|Referências)" "03-Dominios/Tecnologia/Java/Programação Reativa/01 - O que é programação reativa — o modelo push, assíncrono e não-bloqueante.md"
grep -riE "Patient|Doctor|Appointment|MedEspecialista|minha experiência|% d[ao]s (dev|empresas)" "03-Dominios/Tecnologia/Java/Programação Reativa/01 - O que é programação reativa — o modelo push, assíncrono e não-bloqueante.md"
grep -c "Concorrência e paralelismo/12" "03-Dominios/Tecnologia/Java/Programação Reativa/01 - O que é programação reativa — o modelo push, assíncrono e não-bloqueante.md"
```
Expected: ≥7 seções; segundo grep **VAZIO**; terceiro ≥1 (link de volta ao Galho 4).

- [ ] **Step 4: Commit** — `git add "<path>"` && `git commit -m "feat(java): galho 11 nota 01 — o que é programação reativa (modelo push, não-bloqueante)"`

### Task 2: Nota 02 — Reactive Streams — a spec das 4 interfaces e o Flow do Java 9

**Files:**
- Create: `03-Dominios/Tecnologia/Java/Programação Reativa/02 - Reactive Streams — a spec das 4 interfaces e o Flow do Java 9.md`

- [ ] **Step 1: Pesquisar (version-specific)** — WebFetch `https://www.reactive-streams.org/` + `https://docs.oracle.com/en/java/javase/21/docs/api/java.base/java/util/concurrent/Flow.html`. CONFIRMAR: as 4 interfaces (`Publisher`/`Subscriber`/`Subscription`/`Processor`); os 4 sinais (`onSubscribe`/`onNext`/`onError`/`onComplete`); a spec **absorvida em `java.util.concurrent.Flow`** no **Java 9**; Reactor/RxJava/Akka Streams como implementações; a spec define o contrato de backpressure. **WebFetch obrigatório.**

- [ ] **Step 2: Escrever** — `fase: iniciado`, tags `[java, reativa, iniciado, reactive-streams]`. Conteúdo:
  - TL;DR: Reactive Streams é a especificação de 4 interfaces (`Publisher`/`Subscriber`/`Subscription`/`Processor`) que padroniza streams assíncronos com backpressure — absorvida no JDK como `java.util.concurrent.Flow` (Java 9); o Reactor é uma implementação.
  - H3s: "As 4 interfaces e os 4 sinais (`onSubscribe`/`onNext`/`onError`/`onComplete`)", "O `Subscription` e o contrato de backpressure (`request(n)`/`cancel`)", "`java.util.concurrent.Flow`: a spec no JDK desde o Java 9", "Implementações: Reactor, RxJava, Akka Streams (a spec é o denominador comum)".
  - `## Na prática` — as 4 interfaces com suas assinaturas + um `Subscriber` mínimo mostrando os 4 callbacks (```java); nota de que na prática você usa Reactor, não implementa na mão.
  - `## Armadilhas` — ≥2: (1) implementar `Publisher`/`Subscriber` na mão (é sutil e fácil violar a spec — use Reactor); (2) confundir a spec (`Flow`) com a implementação (Reactor) — `Flux` não É `Flow.Publisher`, mas é adaptável.
  - `## Veja também` — [[01 - O que é programação reativa — o modelo push, assíncrono e não-bloqueante]], [[03 - Mono e Flux — os publishers do Project Reactor]], [[09 - Backpressure — request(n) e as estratégias BUFFER, DROP, LATEST]], **[[03-Dominios/Tecnologia/Java/Linguagem e sintaxe moderna/15 - A evolução do Java (8 a 25)|A evolução do Java]]** (o `Flow` chegou no Java 9), verbetes `Reactive Streams`/`Publisher / Subscriber / Subscription`/`Flow (java.util.concurrent)`.

- [ ] **Step 3: Verificar** — ≥7 seções; anti-fabricação VAZIO; `grep -i "java.util.concurrent.Flow\|Java 9"` ≥1.

- [ ] **Step 4: Commit** — `git commit -m "feat(java): galho 11 nota 02 — Reactive Streams (as 4 interfaces e o Flow do Java 9)"`

### Task 3: Nota 03 — Mono e Flux — os publishers do Project Reactor

**Files:**
- Create: `03-Dominios/Tecnologia/Java/Programação Reativa/03 - Mono e Flux — os publishers do Project Reactor.md`

- [ ] **Step 1: Pesquisar (version-specific)** — WebFetch `https://projectreactor.io/docs/core/release/reference/#core-features` (Mono/Flux). CONFIRMAR: `Mono` (0-1) vs `Flux` (0-N); criação (`just`/`fromIterable`/`defer`/`empty`/`error`/`fromCallable`); cardinalidade no tipo; marble diagrams; **Reactor 3.x** (versão atual). **WebFetch obrigatório.**

- [ ] **Step 2: Escrever** — `fase: iniciado`, tags `[java, reativa, iniciado, mono-flux, reactor]`. Conteúdo:
  - TL;DR: `Mono<T>` representa 0-1 elemento e `Flux<T>` representa 0-N — a cardinalidade fica no sistema de tipos; ambos são `Publisher`s lazy que só rodam no `subscribe`.
  - H3s: "`Mono` (0-1): zero ou um elemento", "`Flux` (0-N): um stream de zero a muitos", "Criação: `just`, `fromIterable`, `defer`, `empty`, `error`, `fromCallable`", "Marble diagrams: a linguagem visual dos operadores".
  - `## Na prática` — `Mono.just(order)`, `Flux.fromIterable(orders)`, `Mono.fromCallable(() -> repository.find(id))`, `Mono.defer(...)`; um marble diagram em ```text (```java + ```text).
  - `## Armadilhas` — ≥2: (1) `Mono.just(expensiveCall())` (avalia eager no assembly — use `defer`/`fromCallable`); (2) usar `Flux` onde `Mono` bastava (cardinalidade errada confunde quem lê); (3) `Flux.just(list)` esperando achatar (vira `Flux<List>` — use `fromIterable`).
  - `## Veja também` — [[01 - O que é programação reativa — o modelo push, assíncrono e não-bloqueante]], [[04 - Nada acontece até o subscribe — lazy, assembly vs subscription, cold vs hot]], [[05 - map e flatMap — transformando o fluxo]], verbetes `Mono`/`Flux`/`Project Reactor`/`marble diagram`.

- [ ] **Step 3: Verificar** — ≥7 seções; anti-fabricação VAZIO; `grep -i "Mono\|Flux"` ≥5.

- [ ] **Step 4: Commit** — `git commit -m "feat(java): galho 11 nota 03 — Mono e Flux (os publishers do Project Reactor)"`

### Task 4: Nota 04 — Nada acontece até o subscribe — lazy, assembly vs subscription, cold vs hot

**Files:**
- Create: `03-Dominios/Tecnologia/Java/Programação Reativa/04 - Nada acontece até o subscribe — lazy, assembly vs subscription, cold vs hot.md`

- [ ] **Step 1: Pesquisar** — WebFetch `https://projectreactor.io/docs/core/release/reference/#reactive.subscribe` + `#reactor.hotCold`. CONFIRMAR: a pipeline é lazy (declarar não roda); `subscribe()` dispara (no WebFlux o framework subscreve); assembly time vs subscription time; cold (cada subscriber refaz a origem) vs hot (`share()`/`publish()`).

- [ ] **Step 2: Escrever** — `fase: iniciado`, tags `[java, reativa, iniciado, reactor]`. Conteúdo:
  - TL;DR: um pipeline reativo é lazy — declarar operadores não executa nada; só o `subscribe()` dispara (e no WebFlux quem subscreve é o framework). Cold publishers refazem o trabalho por subscriber; hot publishers compartilham.
  - H3s: "Lazy: declarar ≠ executar (o erro nº1 do iniciante)", "Assembly time vs subscription time", "Quem chama `subscribe`: você nos testes, o framework no WebFlux", "Cold vs hot: refaz por subscriber (`defer`) vs compartilha (`share`/`publish`)".
  - `## Na prática` — um `Flux` com `.map(...)` sem `subscribe` (não roda) vs com `subscribe` (roda); um cold vs hot com `share()` (```java).
  - `## Armadilhas` — ≥2: (1) esquecer o `subscribe` (o pipeline nunca roda — bug nº1); (2) efeito colateral em `map` esperando que rode no assembly (só roda no subscribe); (3) assumir que dois subscribers de um cold publisher compartilham (cada um refaz — use `share()` se quiser hot).
  - `## Veja também` — [[03 - Mono e Flux — os publishers do Project Reactor]], [[08 - Schedulers — subscribeOn, publishOn e em qual thread o código roda]], [[10 - Spring WebFlux — o stack não-bloqueante sobre Netty e o DispatcherHandler]], verbetes `assembly time / subscription time`/`cold publisher / hot publisher`.

- [ ] **Step 3: Verificar** — ≥7 seções; anti-fabricação VAZIO; `grep -i "subscribe\|lazy"` ≥3.

- [ ] **Step 4: Commit** — `git commit -m "feat(java): galho 11 nota 04 — nada acontece até o subscribe (lazy, cold vs hot)"`

---

## Fase ADEPTO (notas 05-12)

### Task 5: Nota 05 — map e flatMap — transformando o fluxo ⟦opus⟧

**Files:**
- Create: `03-Dominios/Tecnologia/Java/Programação Reativa/05 - map e flatMap — transformando o fluxo.md`

- [ ] **Step 1: Pesquisar** — WebFetch `https://projectreactor.io/docs/core/release/reference/#which.values` (transforming). CONFIRMAR: `map` (síncrono, `T → R`) vs `flatMap` (assíncrono, `T → Publisher<R>`, achata); `concatMap` (ordem)/`flatMapSequential`; `then`/`thenMany`; o `flatMap(fn, concurrency)`.

- [ ] **Step 2: Escrever** — `fase: adepto`, tags `[java, reativa, adepto, operadores, reactor]`. **A confusão central do reativo.** ≥3 H3s: "`map`: transformação síncrona 1:1 (`T → R`)", "`flatMap`: transformação assíncrona que retorna outro publisher (`T → Publisher<R>`, achatado)", "Por que uma chamada reativa dentro de outra exige `flatMap` (senão vira `Mono<Mono<T>>`)", "`concatMap`/`flatMapSequential`: quando a ordem importa". `## Na prática`: um `map` (somar imposto) vs um `flatMap` (chamar `orderRepository.findById` que retorna `Mono`) lado a lado, mostrando o `Mono<Mono<T>>` que o `map` produziria (```java). `## Armadilhas` ≥3: usar `map` com função que retorna `Mono` (vira `Flux<Mono<T>>` — use `flatMap`); `flatMap` quando a ordem importa (intercala — use `concatMap`); explosão de concorrência sem `flatMap(fn, concurrency)`. `## Veja também` — [[03 - Mono e Flux — os publishers do Project Reactor]], [[06 - Combinando publishers — zip, merge, concat, filter]], [[08 - Schedulers — subscribeOn, publishOn e em qual thread o código roda]], verbetes `map (reativo)`/`flatMap (reativo)`/`concatMap`.

- [ ] **Step 3: Verificar** — ≥7 seções; ≥3 armadilhas; `grep -i "flatMap"` ≥3; anti-fabricação VAZIO.

- [ ] **Step 4: Commit** — `git commit -m "feat(java): galho 11 nota 05 — map e flatMap (transformando o fluxo)"`

### Task 6: Nota 06 — Combinando publishers — zip, merge, concat, filter

**Files:**
- Create: `03-Dominios/Tecnologia/Java/Programação Reativa/06 - Combinando publishers — zip, merge, concat, filter.md`

- [ ] **Step 1: Pesquisar** — WebFetch `https://projectreactor.io/docs/core/release/reference/#which.create` (combining/filtering). CONFIRMAR: `zip` (par a par, espera os dois), `merge` (intercala conforme chegam), `concat` (sequencial, ordenado); `filter`/`take`/`skip`/`distinct`.

- [ ] **Step 2: Escrever** — `fase: adepto`, tags `[java, reativa, adepto, operadores]`. ≥3 H3s: "`zip`: combina elemento-a-elemento (espera os dois)", "`merge` vs `concat`: intercalado (conforme chegam) vs ordenado (um após o outro)", "Filtrando: `filter`/`take`/`skip`/`distinct`", "Quando a ordem importa (concat) vs quando não (merge)". `## Na prática`: `Mono.zip(customerMono, orderMono)` combinando dois resultados; `Flux.merge(a, b)` vs `Flux.concat(a, b)`; `.filter(o -> o.total() > 100)` (```java + um marble ```text). `## Armadilhas` ≥3: `merge` quando precisava de ordem (use `concat`); `zip` com fluxos de tamanhos diferentes (para no menor — perde elementos); `filter` pesado que deveria ser query no banco. `## Veja também` — [[05 - map e flatMap — transformando o fluxo]], [[07 - Error handling reativo — onErrorResume, onErrorReturn, retry]], verbetes `merge / concat / zip`.

- [ ] **Step 3: Verificar** — ≥7 seções; ≥3 armadilhas; anti-fabricação VAZIO.

- [ ] **Step 4: Commit** — `git commit -m "feat(java): galho 11 nota 06 — combinando publishers (zip, merge, concat, filter)"`

### Task 7: Nota 07 — Error handling reativo — onErrorResume, onErrorReturn, retry

**Files:**
- Create: `03-Dominios/Tecnologia/Java/Programação Reativa/07 - Error handling reativo — onErrorResume, onErrorReturn, retry.md`

- [ ] **Step 1: Pesquisar** — WebFetch `https://projectreactor.io/docs/core/release/reference/#error.handling`. CONFIRMAR: erro = sinal terminal (`onError` encerra); `onErrorReturn`/`onErrorResume`/`onErrorMap`/`retry`/`retryWhen` (backoff)/`doOnError`; por que `try/catch` não pega o sinal reativo.

- [ ] **Step 2: Escrever** — `fase: adepto`, tags `[java, reativa, adepto, operadores]`. ≥3 H3s: "O erro é um sinal terminal (`onError` encerra o fluxo)", "Recuperação declarativa: `onErrorReturn` (valor), `onErrorResume` (publisher), `onErrorMap` (traduzir)", "`retry`/`retryWhen` com backoff: re-subscribe", "`try/catch` não pega o sinal reativo (e por quê)". **Linka G9** (`@ControllerAdvice` no MVC; no WebFlux o tratamento é na cadeia ou no `WebExceptionHandler`). `## Na prática`: `webClient.get()...bodyToMono(Order.class).onErrorResume(NotFoundException.class, e -> Mono.empty()).retryWhen(Retry.backoff(3, ...))` (```java). `## Armadilhas` ≥3: `try/catch` em volta de uma cadeia reativa (não pega — use `onError*`); `retry()` infinito sem backoff (martela o serviço — use `retryWhen` com backoff); engolir o erro com `onErrorReturn` sem logar (`doOnError`). `## Veja também` — [[06 - Combinando publishers — zip, merge, concat, filter]], [[11 - WebClient — o cliente HTTP reativo a fundo]], **[[03-Dominios/Tecnologia/Java/Web e APIs REST/01 - O que é Spring MVC — a camada web sobre o container|O que é Spring MVC]]** (o exception handling imperativo), verbetes `onErrorResume / onErrorReturn`/`retry / retryWhen`.

- [ ] **Step 3: Verificar** — ≥7 seções; ≥3 armadilhas; link Galho 9 presente; anti-fabricação VAZIO.

- [ ] **Step 4: Commit** — `git commit -m "feat(java): galho 11 nota 07 — error handling reativo (onErrorResume, retry)"`

### Task 8: Nota 08 — Schedulers — subscribeOn, publishOn e em qual thread o código roda ⟦opus⟧

**Files:**
- Create: `03-Dominios/Tecnologia/Java/Programação Reativa/08 - Schedulers — subscribeOn, publishOn e em qual thread o código roda.md`

- [ ] **Step 1: Pesquisar** — WebFetch `https://projectreactor.io/docs/core/release/reference/#schedulers`. CONFIRMAR: por default roda na thread do `subscribe`; `subscribeOn` (afeta a origem) vs `publishOn` (troca a thread daí pra baixo); `Schedulers.parallel()`/`boundedElastic()`(bloqueante)/`single()`/`immediate()`; nunca bloquear o event loop.

- [ ] **Step 2: Escrever** — `fase: adepto`, tags `[java, reativa, adepto, schedulers, reactor]`. ≥3 H3s: "Por default: roda na thread que chamou `subscribe`", "`subscribeOn`: afeta a origem (o início da cadeia)", "`publishOn`: troca a thread daí pra baixo", "Os `Schedulers`: `parallel()` (CPU), `boundedElastic()` (envolver bloqueante), `single()`, `immediate()`", "Nunca bloquear o event loop". **Linka G4** (pools/threads — o reativo multiplexa poucos threads). `## Na prática`: uma cadeia com `publishOn(Schedulers.parallel())` e um `Mono.fromCallable(jdbcCall).subscribeOn(Schedulers.boundedElastic())` pra envolver código bloqueante (```java). `## Armadilhas` ≥3: chamar JDBC/lib bloqueante num operador sem `boundedElastic()` (trava o event loop — todas as requests param); achar que `subscribeOn` troca a thread no meio (é `publishOn`); `subscribeOn` múltiplo (só o mais próximo da origem vale). `## Veja também` — [[04 - Nada acontece até o subscribe — lazy, assembly vs subscription, cold vs hot]], [[09 - Backpressure — request(n) e as estratégias BUFFER, DROP, LATEST]], **[[03-Dominios/Tecnologia/Java/Concorrência e paralelismo/index|Concorrência e paralelismo]]** (pools e threads), **[[03-Dominios/Tecnologia/Java/Concorrência e paralelismo/12 - Virtual Threads e Project Loom|Virtual Threads e Project Loom]]**, verbetes `publishOn / subscribeOn`/`Scheduler (Reactor)`/`boundedElastic (Scheduler)`/`event loop`.

- [ ] **Step 3: Verificar** — ≥7 seções; ≥3 armadilhas; link Galho 4 presente; `grep -i "boundedElastic\|publishOn\|subscribeOn"` ≥3; anti-fabricação VAZIO.

- [ ] **Step 4: Commit** — `git commit -m "feat(java): galho 11 nota 08 — schedulers (subscribeOn, publishOn, em qual thread)"`

### Task 9: Nota 09 — Backpressure — request(n) e as estratégias BUFFER, DROP, LATEST ⟦opus⟧

**Files:**
- Create: `03-Dominios/Tecnologia/Java/Programação Reativa/09 - Backpressure — request(n) e as estratégias BUFFER, DROP, LATEST.md`

- [ ] **Step 1: Pesquisar** — WebFetch `https://www.reactive-streams.org/` + `https://projectreactor.io/docs/core/release/reference/#producing` (`Flux.create`/overflow). CONFIRMAR: `request(n)` — o consumidor controla a demanda; overflow: `onBackpressureBuffer`/`Drop`/`Latest`/`Error`; `Flux.create` com `FluxSink` e `OverflowStrategy`.

- [ ] **Step 2: Escrever** — `fase: adepto`, tags `[java, reativa, adepto, backpressure, reactive-streams]`. **O coração do Reactive Streams.** ≥3 H3s: "`request(n)`: o consumidor controla a demanda (o produtor não empurra mais do que aguenta)", "Overflow: produtor mais rápido que o consumidor", "Estratégias: `onBackpressureBuffer`/`Drop`/`Latest`/`Error`", "`Flux.create` com `FluxSink` e `OverflowStrategy`". **Linka G4** (a nota 12 marca "backpressure: não nativo" nos Virtual Threads — o que reativo dá e VT não). `## Na prática`: um `Flux.create((sink) -> ..., OverflowStrategy.DROP)` + um `.onBackpressureBuffer(1000)` num stream rápido (```java + um marble ```text mostrando request(n)). `## Armadilhas` ≥3: produtor rápido + consumidor lento sem estratégia (buffer default pode estourar memória); `onBackpressureDrop` perdendo dados sem perceber/logar; ignorar backpressure num `Flux.create` (push sem demanda). `## Veja também` — [[02 - Reactive Streams — a spec das 4 interfaces e o Flow do Java 9]], [[08 - Schedulers — subscribeOn, publishOn e em qual thread o código roda]], [[14 - Reativo vs Virtual Threads — o confronto honesto]], **[[03-Dominios/Tecnologia/Java/Concorrência e paralelismo/12 - Virtual Threads e Project Loom|Virtual Threads e Project Loom]]** (VT não dão backpressure nativo), verbetes `backpressure`/`request(n) (demanda)`/`onBackpressureBuffer / Drop / Latest`.

- [ ] **Step 3: Verificar** — ≥7 seções; ≥3 armadilhas; link Galho 4 presente; `grep -i "backpressure\|request"` ≥3; anti-fabricação VAZIO.

- [ ] **Step 4: Commit** — `git commit -m "feat(java): galho 11 nota 09 — backpressure (request(n), BUFFER, DROP, LATEST)"`

### Task 10: Nota 10 — Spring WebFlux — o stack não-bloqueante sobre Netty e o DispatcherHandler ⟦opus⟧

**Files:**
- Create: `03-Dominios/Tecnologia/Java/Programação Reativa/10 - Spring WebFlux — o stack não-bloqueante sobre Netty e o DispatcherHandler.md`

- [ ] **Step 1: Pesquisar (version-specific)** — WebFetch `https://docs.spring.io/spring-framework/reference/web/webflux.html` + `https://docs.spring.io/spring-framework/reference/web/webflux/reactive-spring.html`. CONFIRMAR: event loop (Netty, poucos threads) vs thread-per-request (servlet); `DispatcherHandler` vs `DispatcherServlet`; `@RestController` reativo retornando `Mono`/`Flux`; SSE (`text/event-stream`); starter `spring-boot-starter-webflux`; **baseline Boot 3.x**. **WebFetch obrigatório.**

- [ ] **Step 2: Escrever** — `fase: adepto`, tags `[java, reativa, adepto, webflux]`. **Substitui o Galho 9.** ≥3 H3s: "Event loop (Netty, poucos threads) vs thread-per-request (servlet — Galho 9)", "`DispatcherHandler` vs `DispatcherServlet`: o mesmo papel, modelo diferente", "Controllers reativos: `@RestController` retornando `Mono<T>`/`Flux<T>`", "Streaming/SSE (`text/event-stream`)". **Linka G9** (notas 01/06 — MVC/DispatcherServlet), **G8** (auto-config/starter). `## Na prática`: um `@RestController` WebFlux com `Mono<OrderDto> getOrder` e `Flux<OrderDto> streamOrders(produces = TEXT_EVENT_STREAM_VALUE)` + o `spring-boot-starter-webflux` (```java + ```xml). `## Armadilhas` ≥3: misturar `spring-boot-starter-web` e `-webflux` (o MVC vence, vira bloqueante); bloquear no handler (`.block()`/JDBC — mata o event loop, todas as requests param); achar que WebFlux "é mais rápido" pra request única (é throughput, não latência). `## Veja também` — [[01 - O que é programação reativa — o modelo push, assíncrono e não-bloqueante]], [[11 - WebClient — o cliente HTTP reativo a fundo]], [[12 - Functional endpoints — RouterFunction e HandlerFunction]], **[[03-Dominios/Tecnologia/Java/Web e APIs REST/01 - O que é Spring MVC — a camada web sobre o container|O que é Spring MVC]]**, **[[03-Dominios/Tecnologia/Java/Web e APIs REST/06 - O pipeline do DispatcherServlet|O pipeline do DispatcherServlet]]**, **[[03-Dominios/Tecnologia/Java/Spring Core e Boot/15 - Auto-configuration e starters|Auto-configuration e starters]]**, verbetes `Spring WebFlux`/`DispatcherHandler`/`event loop`/`Netty`.

- [ ] **Step 3: Verificar** — ≥7 seções; ≥3 armadilhas; links Galho 9 (notas 01 + 06) e Galho 8 presentes; `grep -i "DispatcherHandler\|Netty\|event loop"` ≥2; anti-fabricação VAZIO.

- [ ] **Step 4: Commit** — `git commit -m "feat(java): galho 11 nota 10 — Spring WebFlux (Netty, DispatcherHandler, controllers reativos)"`

### Task 11: Nota 11 — WebClient — o cliente HTTP reativo a fundo

**Files:**
- Create: `03-Dominios/Tecnologia/Java/Programação Reativa/11 - WebClient — o cliente HTTP reativo a fundo.md`

- [ ] **Step 1: Pesquisar (version-specific)** — WebFetch `https://docs.spring.io/spring-framework/reference/web/webflux-webclient.html`. CONFIRMAR: `WebClient.create()`/`builder()`, `get()/post()`, `retrieve()`, `bodyToMono`/`bodyToFlux`, `exchangeToMono`, `onStatus`; streaming; vs `RestClient` síncrono (Spring 6.1). **WebFetch obrigatório.**

- [ ] **Step 2: Escrever** — `fase: adepto`, tags `[java, reativa, adepto, webclient, webflux]`. ≥3 H3s: "`WebClient`: o cliente HTTP não-bloqueante do WebFlux", "`retrieve()` + `bodyToMono`/`bodyToFlux`: consumindo a resposta", "Error handling: `onStatus` (HTTP de erro vira `WebClientResponseException`)", "Streaming de respostas (`bodyToFlux` + `text/event-stream`)", "vs `RestClient` síncrono (Galho 9 nota 15 — mesma API fluent, modelo oposto); o 'pior dos dois mundos' (`WebClient` + `.block()` num stack imperativo)". **Linka G9 nota 15.** `## Na prática`: `webClient.get().uri("/orders/{id}", id).retrieve().bodyToMono(OrderDto.class)` + um `bodyToFlux` streaming + `onStatus` (```java). `## Armadilhas` ≥3: `WebClient` + `.block()` num serviço MVC (pior dos dois mundos — use `RestClient`); não tratar `onStatus` (erro HTTP silencioso vira exceção tarde); recriar `WebClient` a cada chamada (crie um e reuse — é thread-safe). `## Veja também` — [[10 - Spring WebFlux — o stack não-bloqueante sobre Netty e o DispatcherHandler]], [[07 - Error handling reativo — onErrorResume, onErrorReturn, retry]], **[[03-Dominios/Tecnologia/Java/Web e APIs REST/15 - Clientes HTTP — RestClient, WebClient, RestTemplate|Clientes HTTP (RestClient vs WebClient)]]**, verbetes `WebClient`.

- [ ] **Step 3: Verificar** — ≥7 seções; ≥3 armadilhas; link Galho 9 nota 15 presente; anti-fabricação VAZIO.

- [ ] **Step 4: Commit** — `git commit -m "feat(java): galho 11 nota 11 — WebClient (o cliente HTTP reativo)"`

### Task 12: Nota 12 — Functional endpoints — RouterFunction e HandlerFunction

**Files:**
- Create: `03-Dominios/Tecnologia/Java/Programação Reativa/12 - Functional endpoints — RouterFunction e HandlerFunction.md`

- [ ] **Step 1: Pesquisar** — WebFetch `https://docs.spring.io/spring-framework/reference/web/webflux-functional.html`. CONFIRMAR: `RouterFunctions.route().GET(...).build()`; `HandlerFunction` (`ServerRequest → Mono<ServerResponse>`); functional vs anotado.

- [ ] **Step 2: Escrever** — `fase: adepto`, tags `[java, reativa, adepto, webflux]`. ≥3 H3s: "Roteamento como código: `RouterFunctions.route().GET(...).build()`", "`HandlerFunction`: `ServerRequest → Mono<ServerResponse>`", "Functional vs anotado: quando cada (roteamento dinâmico/composição vs familiaridade do Galho 9)". **Linka G9** (controllers anotados). `## Na prática`: um `@Bean RouterFunction<ServerResponse>` roteando `GET /orders` pra um handler + o handler `Mono<ServerResponse>` (```java). `## Armadilhas` ≥3: misturar functional e anotado sem critério (confunde); lógica de negócio no router (deixe no service); esquecer que o `ServerResponse` também é reativo (`ServerResponse.ok().body(...)`). `## Veja também` — [[10 - Spring WebFlux — o stack não-bloqueante sobre Netty e o DispatcherHandler]], **[[03-Dominios/Tecnologia/Java/Web e APIs REST/01 - O que é Spring MVC — a camada web sobre o container|O que é Spring MVC]]** (controllers anotados), verbete `functional endpoint (RouterFunction)`.

- [ ] **Step 3: Verificar** — ≥7 seções; ≥3 armadilhas; anti-fabricação VAZIO.

- [ ] **Step 4: Commit** — `git commit -m "feat(java): galho 11 nota 12 — functional endpoints (RouterFunction, HandlerFunction)"`

---

## Fase MAGUS (notas 13-16)

### Task 13: Nota 13 — R2DBC — persistência reativa sem EntityManager ⟦opus⟧

**Files:**
- Create: `03-Dominios/Tecnologia/Java/Programação Reativa/13 - R2DBC — persistência reativa sem EntityManager.md`

- [ ] **Step 1: Pesquisar (version-specific)** — WebFetch `https://r2dbc.io/` + `https://docs.spring.io/spring-data/r2dbc/docs/current/reference/html/`. CONFIRMAR: driver R2DBC (não-bloqueante) vs JDBC (bloqueante); `R2dbcRepository`/`DatabaseClient`; **sem `EntityManager`, sem persistence context, sem dirty checking, sem lazy loading, sem cache de 1º nível**; transações reativas (`TransactionalOperator`). **WebFetch obrigatório.**

- [ ] **Step 2: Escrever** — `fase: magus`, tags `[java, reativa, magus, r2dbc]`. **Contraste direto com o Galho 10.** ≥3 H3s: "R2DBC: o driver reativo (não-bloqueante) vs JDBC (bloqueante)", "`R2dbcRepository`/`DatabaseClient`: o acesso reativo", "O que NÃO existe: sem `EntityManager`, sem persistence context (cache de 1º nível), sem dirty checking, **sem lazy loading**", "Relacionamentos resolvidos manualmente (`flatMap`), não com `@OneToMany`", "Transações reativas (`TransactionalOperator`/`@Transactional` reativo)". **Linka G10** (nota 01 — a pilha JPA; nota 03 — o persistence context que falta; nota 07 — o lazy que falta). `## Na prática`: um `interface OrderRepository extends R2dbcRepository<Order, Long>` retornando `Flux<Order>`/`Mono<Order>` + resolver a relação `Customer` com `flatMap` (vs o `@ManyToOne` lazy do Galho 10) + schema (```java + ```sql). `## Armadilhas` ≥3: esperar lazy loading da JPA (não existe — resolva com `flatMap`); misturar JDBC bloqueante "junto" do R2DBC (mata o ganho — todo o caminho precisa ser reativo); achar que R2DBC é "JPA reativo" (não tem ORM, persistence context nem cache). `## Veja também` — [[10 - Spring WebFlux — o stack não-bloqueante sobre Netty e o DispatcherHandler]], [[16 - Capstone — uma request reativa de ponta a ponta no WebFlux]], **[[03-Dominios/Tecnologia/Java/Persistência de dados/01 - O que é a camada de persistência — Spring Data, JPA e Hibernate|O que é a camada de persistência]]**, **[[03-Dominios/Tecnologia/Java/Persistência de dados/03 - O persistence context e os estados da entidade|O persistence context]]** (o cache de 1º nível que o R2DBC não tem), **[[03-Dominios/Tecnologia/Java/Persistência de dados/07 - Fetch strategies — LAZY, EAGER e a LazyInitializationException|Fetch strategies]]** (o lazy que o R2DBC não tem), verbetes `R2DBC`/`R2dbcRepository`/`DatabaseClient (R2DBC)`.

- [ ] **Step 3: Verificar** — ≥7 seções; ≥3 armadilhas; links Galho 10 (notas 01 + 03 + 07) presentes; `grep -i "EntityManager\|lazy"` ≥1 (o contraste); anti-fabricação VAZIO.

- [ ] **Step 4: Commit** — `git commit -m "feat(java): galho 11 nota 13 — R2DBC (persistência reativa sem EntityManager)"`

### Task 14: Nota 14 — Reativo vs Virtual Threads — o confronto honesto ⟦opus⟧

**Files:**
- Create: `03-Dominios/Tecnologia/Java/Programação Reativa/14 - Reativo vs Virtual Threads — o confronto honesto.md`

- [ ] **Step 1: Pesquisar (version-specific)** — WebFetch `https://docs.spring.io/spring-framework/reference/web/webflux/reactive-spring.html` (posição do Spring sobre VT) + revisar a nota 12 do Galho 4 (Virtual Threads — `Concorrência e paralelismo/12`). CONFIRMAR: VT = GA/final Java 21 JEP 444 (cravado no Galho 4); a posição documentada do Spring sobre VT tornarem WebFlux menos necessário; o que reativo dá que VT não (backpressure nativo) e vice-versa (debugging normal). **WebFetch obrigatório; ZERO estatística de adoção inventada.**

- [ ] **Step 2: Escrever** — `fase: magus`, tags `[java, reativa, magus, virtual-threads, reactor]`. **Paga a dívida do Galho 4 nota 12. A tese central do galho.** ≥3 H3s: "O ponto comum: ambos resolvem I/O-bound com poucos threads do SO", "Reativo: operadores, backpressure nativo, composição — mas debugging difícil e contágio (tudo precisa ser reativo)", "Virtual Threads (Java 21 GA): código bloqueante normal, stack trace normal — mas sem backpressure nativo, sem contágio", "Onde reativo AINDA vence: streaming real, backpressure de verdade, stack já reativo ponta a ponta", "Onde VT venceu: a maioria dos CRUDs de alta concorrência". **Tabela comparativa honesta** (legibilidade, debugging, backpressure, libs bloqueantes, contágio). **Linka G4 nota 12** (o confronto que ela adiou). `## Na prática`: o mesmo endpoint de alta concorrência nos dois modelos — `Flux` + R2DBC (reativo) vs `List` + JDBC num virtual thread (imperativo) (```java), com a análise honesta de trade-off. `## Armadilhas` ≥3: adotar reativo "pela performance" num CRUD (VT resolve mais simples — sem hype); achar que VT "matam" o reativo (streaming/backpressure ainda pedem reativo); comparar latência por request (é throughput/recursos — os dois empatam em latência). **SEM estatística inventada.** `## Veja também` — [[01 - O que é programação reativa — o modelo push, assíncrono e não-bloqueante]], [[09 - Backpressure — request(n) e as estratégias BUFFER, DROP, LATEST]], [[15 - Quando (não) usar reativo — custo cognitivo, debugging e stack traces]], **[[03-Dominios/Tecnologia/Java/Concorrência e paralelismo/12 - Virtual Threads e Project Loom|Virtual Threads e Project Loom]]** (o confronto que esta nota paga), verbetes `backpressure`/`event loop`.

- [ ] **Step 3: Verificar** — ≥7 seções; ≥3 armadilhas; link Galho 4 nota 12 presente; tabela comparativa presente; **grep estatística inventada VAZIO** (`% d[ao]s (dev|empresas|projetos)|market share|maioria (adota|migrou)`); anti-fabricação VAZIO.

- [ ] **Step 4: Commit** — `git commit -m "feat(java): galho 11 nota 14 — reativo vs Virtual Threads (o confronto honesto)"`

### Task 15: Nota 15 — Quando (não) usar reativo — custo cognitivo, debugging e stack traces

**Files:**
- Create: `03-Dominios/Tecnologia/Java/Programação Reativa/15 - Quando (não) usar reativo — custo cognitivo, debugging e stack traces.md`

- [ ] **Step 1: Pesquisar** — WebFetch `https://projectreactor.io/docs/core/release/reference/#debugging` + `https://docs.spring.io/spring-framework/reference/web/webflux.html` (quando usar). CONFIRMAR: stack traces fragmentados (`Hooks.onOperatorDebug()`/`checkpoint()` — caro); debugging sem step; libs bloqueantes contaminam o event loop; o ganho precisa justificar o custo. **ZERO estatística de adoção inventada.**

- [ ] **Step 2: Escrever** — `fase: magus`, tags `[java, reativa, magus, reactor]`. **A "metade do galho".** ≥3 H3s: "Stack traces fragmentados: a thread que estoura não é a que montou (`Hooks.onOperatorDebug()`/`checkpoint()` — e o custo)", "Debugging sem step: não dá pra dar step num pipeline lazy/assíncrono", "Contágio: uma lib bloqueante no meio anula o ganho", "Curva da equipe vs o ganho real: o checklist de decisão honesto". **Linka G4** (VT como alternativa) e **G9** (MVC como default). `## Na prática`: um stack trace reativo fragmentado vs o mesmo com `checkpoint()` (```text); o checklist "use reativo SE: streaming real / backpressure de verdade / stack já reativo; NÃO use SE: CRUD comum, equipe sem experiência, Java 21+ disponível (VT)". `## Armadilhas` ≥3: reativo por hype/CV-driven (custo de manutenção real); reativo "pela metade" (uma lib bloqueante no meio anula tudo); subestimar o custo de onboarding/debugging. **SEM estatística inventada.** `## Veja também` — [[14 - Reativo vs Virtual Threads — o confronto honesto]], [[08 - Schedulers — subscribeOn, publishOn e em qual thread o código roda]], **[[03-Dominios/Tecnologia/Java/Concorrência e paralelismo/12 - Virtual Threads e Project Loom|Virtual Threads e Project Loom]]**, **[[03-Dominios/Tecnologia/Java/Web e APIs REST/01 - O que é Spring MVC — a camada web sobre o container|O que é Spring MVC]]** (o default imperativo), verbete `marble diagram`.

- [ ] **Step 3: Verificar** — ≥7 seções; ≥3 armadilhas; links Galho 4 + Galho 9 presentes; **grep estatística inventada VAZIO**; anti-fabricação VAZIO.

- [ ] **Step 4: Commit** — `git commit -m "feat(java): galho 11 nota 15 — quando (não) usar reativo (custo cognitivo, debugging)"`

### Task 16: Nota 16 — Capstone — uma request reativa de ponta a ponta no WebFlux ⟦opus⟧

**Files:**
- Create: `03-Dominios/Tecnologia/Java/Programação Reativa/16 - Capstone — uma request reativa de ponta a ponta no WebFlux.md`

- [ ] **Step 1: Pesquisar** — WebFetch `https://docs.spring.io/spring-framework/reference/web/webflux.html` (revisão) + `https://projectreactor.io/docs/core/release/reference/` (revisão). Conferir a tabela "Galho 11 ↔ imperativo (Galhos 9/10) + VT (Galho 4)" com as notas dos Galhos 4/9/10 já escritas.

- [ ] **Step 2: Escrever** — `fase: magus`, tags `[java, reativa, magus, webflux, r2dbc]`, aliases `["Capstone Reativa", "Request reativa ponta a ponta"]`. **Híbrido: trace + checklist de design.** Conteúdo:
  - TL;DR: uma request reativa atravessa `DispatcherHandler` → controller reativo → `WebClient` + R2DBC → operadores e error handling → backpressure → `Flux<OrderDto>` no event loop, sem bloquear em ponto nenhum.
  - `## O que é` / `## Por que importa`.
  - `## Como funciona` — H3s: "**Trace:** `GET /orders` da chamada à resposta (diagrama ```text: DispatcherHandler → @RestController reativo → WebClient + R2dbcRepository → flatMap/zip + onErrorResume → backpressure → Flux<OrderDto> → event loop → cliente)", "O que NÃO pode acontecer: bloquear o event loop (`.block()`/JDBC) em ponto nenhum", "**Galho 11 (reativo) ↔ imperativo (Galhos 9/10) + VT (Galho 4)** (tabela: `DispatcherHandler`↔`DispatcherServlet`, `WebClient`↔`RestClient`, R2DBC↔JPA, event loop↔thread-per-request↔Virtual Threads)".
  - `## Na prática` — o `@RestController` reativo completo: recebe a request, chama `WebClient` (serviço externo) + `R2dbcRepository` (banco), compõe com `zip`/`flatMap`, trata erro com `onErrorResume`, devolve `Flux<OrderDto>` (```java) + `### Checklist de design production-grade` (nunca `.block()` num handler; `boundedElastic()` pra lib bloqueante inevitável; error handling no fim da cadeia; backpressure consciente; o `subscribe` é do framework).
  - `## Armadilhas` (de raciocínio) ≥3: "reativo é sempre melhor pra escala" (VT — nota 14); "é só trocar o tipo de retorno pra `Mono`/`Flux`" (o stack inteiro muda); "`WebClient` é mais rápido" (throughput, não latência).
  - `## Em entrevista` (munição: o trace, o não-bloquear, reativo-vs-VT) + `### Cheatsheet` (nota→problema) + `## Veja também` (notas-chave do galho + **[[03-Dominios/Tecnologia/Java/Concorrência e paralelismo/12 - Virtual Threads e Project Loom|Virtual Threads e Project Loom]]** + **[[03-Dominios/Tecnologia/Java/Web e APIs REST/01 - O que é Spring MVC — a camada web sobre o container|O que é Spring MVC]]** + **[[03-Dominios/Tecnologia/Java/Persistência de dados/01 - O que é a camada de persistência — Spring Data, JPA e Hibernate|O que é a camada de persistência]]** + MOC galho/central) + `## Referências`.

- [ ] **Step 3: Verificar** — ≥7 seções; tabela "Galho 11 ↔ imperativo" presente (`grep -iE "DispatcherHandler|WebClient|R2DBC|event loop"`); links Galho 4 + Galho 9 + Galho 10 presentes; anti-fabricação VAZIO; sem estatística inventada (revisar manualmente).

- [ ] **Step 4: Commit** — `git commit -m "feat(java): galho 11 nota 16 — capstone (uma request reativa de ponta a ponta no WebFlux)"`

---

## Task 17: MOC do galho

**Files:**
- Create: `03-Dominios/Tecnologia/Java/Programação Reativa/index.md`

- [ ] **Step 1: Escrever** — modelar pelo `03-Dominios/Tecnologia/Java/Persistência de dados/index.md`. Frontmatter: `type: moc`, `status: growing`, `publish: true`, `title: "Programação Reativa"`, tags `[java, reativa, moc]`, aliases `["Programação Reativa", "Reactive Programming", "Project Reactor", "Spring WebFlux", "Galho 11 - Reativa"]`, `created`/`updated: 2026-06-10`. Conteúdo:
  - TL;DR — Galho 11; o modelo reativo na JVM: o que é reativo e o Reactive Streams, Mono/Flux e os operadores, schedulers e backpressure, Spring WebFlux e WebClient, R2DBC, e o confronto honesto reativo vs Virtual Threads; 16 notas em 3 fases.
  - `## Sobre este galho` — escopo + audiência + **galho novo (majoritariamente pesquisa)** com uma poda cirúrgica (a seção WebFlux do `Spring Boot.md`) + **quádrupla fronteira** (confronta o modelo de threads do Galho 4; substitui o stack web do Galho 9; contrasta a persistência do Galho 10; roda sobre o container do Galho 8) + a **tese central** (Virtual Threads tornaram reativo nicho — quando NÃO usar é metade do galho; Galhos 12/13/14/16 planejados, texto).
  - `## Iniciado` (01-04) / `## Adepto` (05-12) / `## Magus` (13-16) — wikilinks + 1 linha cada.
  - `## Rotas alternativas` — 5: **Completa** (01→16); **Entrevista internacional** (01→03→05→09→10→14→16); **Os operadores do Reactor** (03→04→05→06→07→08); **O stack web reativo** (01→10→11→12→13→16); **Reativo vs Virtual Threads** (01→09→14→15 + nota 12 do Galho 4).
  - `## Todas as notas` — Dataview (`FROM "03-Dominios/Tecnologia/Java/Programação Reativa"`, `WHERE type = "concept"`).
  - `## Veja também` — MOC central, **[[03-Dominios/Tecnologia/Java/Concorrência e paralelismo/index|Concorrência e paralelismo]]** (o modelo de threads e o confronto VT), **[[03-Dominios/Tecnologia/Java/Web e APIs REST/index|Web e APIs REST]]** (o stack imperativo), **[[03-Dominios/Tecnologia/Java/Persistência de dados/index|Persistência de dados]]** (a JPA bloqueante), **[[03-Dominios/Tecnologia/Java/Spring Core e Boot/index|Spring Core e Boot]]** (o container), Dicionário; Galhos 12/13/14/16 como texto "(planejado)" SEM wikilink.

- [ ] **Step 2: Verificar**
```bash
grep -cE "^## (Iniciado|Adepto|Magus|Rotas alternativas)" "03-Dominios/Tecnologia/Java/Programação Reativa/index.md"
grep -c "\[\[" "03-Dominios/Tecnologia/Java/Programação Reativa/index.md"
grep -E "\[\[[^]]*(Galho (12|13|14|16))" "03-Dominios/Tecnologia/Java/Programação Reativa/index.md"
```
Expected: 4 headings; ≥16 wikilinks; **último grep VAZIO**.

- [ ] **Step 3: Commit** — `git add "<path>"` && `git commit -m "feat(java): galho 11 MOC — Programação Reativa"`

---

## Task 18: Expandir o Dicionário de Java (NÃO recriar)

**Files:**
- Modify: `03-Dominios/Tecnologia/Java/Dicionário de Java.md`

- [ ] **Step 1: Extrair as âncoras realmente usadas pelas notas**
```bash
grep -rhoE "Dicionário de Java#[^]|]+" "03-Dominios/Tecnologia/Java/Programação Reativa/" | sort -u
```
A fonte da verdade é o que as notas usaram. Lista esperada (~28): `assembly time / subscription time`, `backpressure`, `boundedElastic (Scheduler)`, `cold publisher / hot publisher`, `concatMap`, `DatabaseClient (R2DBC)`, `DispatcherHandler`, `event loop`, `Flow (java.util.concurrent)`, `Flux`, `flatMap (reativo)`, `functional endpoint (RouterFunction)`, `map (reativo)`, `marble diagram`, `merge / concat / zip`, `Mono`, `Netty`, `non-blocking I/O`, `onBackpressureBuffer / Drop / Latest`, `onErrorResume / onErrorReturn`, `Processor (Reactive Streams)`, `Project Reactor`, `Publisher / Subscriber / Subscription`, `publishOn / subscribeOn`, `R2DBC`, `R2dbcRepository`, `Reactive Streams`, `request(n) (demanda)`, `retry / retryWhen`, `Scheduler (Reactor)`, `Spring WebFlux`, `WebClient`.

- [ ] **Step 2: Ler o Dicionário e conferir duplicatas** — formato `### Termo` + 1-3 linhas + `Veja também:`. **NÃO recriar/reordenar.** **Conferir verbetes já existentes pra NÃO duplicar** e **linkar entre si**: `WebClient`/`RestClient` (Galho 9 — se `WebClient` já existir como menção, complementar/linkar, não duplicar); `Virtual Threads` (Galho 4 — linkar de `backpressure`/nota 14, **não duplicar**); `Netty` (Galho 9 — pode existir; linkar); `@Transactional` (Galhos 8/10 — a transação reativa é diferente, linkar). Conferir com:
```bash
grep -nE "^### (WebClient|RestClient|Netty|Virtual Threads|@Transactional|DispatcherServlet|Reactor|Flux|Mono)" "03-Dominios/Tecnologia/Java/Dicionário de Java.md"
```

- [ ] **Step 3: Inserir em ordem alfabética** (case-insensitive, sem acento; verbetes iniciados em `@`/minúscula entram conforme o padrão do arquivo — conferir vizinhos). Cada verbete: heading EXATO da âncora + definição fiel às notas + `Veja também:` pra nota canônica (Project Reactor/non-blocking I/O→01; Reactive Streams/Publisher.../Processor/Flow→02; Mono/Flux/marble diagram→03; assembly.../cold.../hot→04; map/flatMap/concatMap→05; merge/concat/zip→06; onErrorResume/retry→07; publishOn/subscribeOn/Scheduler/boundedElastic/event loop→08; backpressure/request(n)/onBackpressure...→09; Spring WebFlux/DispatcherHandler/Netty→10; WebClient→11; functional endpoint→12; R2DBC/R2dbcRepository/DatabaseClient→13). Atualizar `updated: 2026-06-10`.

- [ ] **Step 4: Verificar**
```bash
grep -E "^### (Mono|Flux|backpressure|Spring WebFlux|R2DBC|Reactive Streams)" "03-Dominios/Tecnologia/Java/Dicionário de Java.md"
grep -cE "^### " "03-Dominios/Tecnologia/Java/Dicionário de Java.md"
```
Expected: novos presentes; contagem subiu ~28 vs baseline (296 → ~324).

- [ ] **Step 5: Commit** — `git add "<path>"` && `git commit -m "feat(java): expande Dicionário de Java com verbetes do galho 11 (Programação Reativa)"`

---

## Task 19: Ativar o Galho 11 no MOC central

**Files:**
- Modify: `03-Dominios/Tecnologia/Java/index.md`

- [ ] **Step 1: Trocar a linha do item 11** (localizar por conteúdo: `11. Programação Reativa *(planejado)* — Reactor, WebFlux, backpressure, R2DBC`) por:
```markdown
11. [[03-Dominios/Tecnologia/Java/Programação Reativa/index|Programação Reativa]] — o modelo reativo na JVM: Reactive Streams, Project Reactor (Mono/Flux e operadores), schedulers e backpressure, Spring WebFlux e WebClient, R2DBC, e o confronto honesto reativo vs Virtual Threads
```
Atualizar `updated: 2026-06-10`. Não mexer no resto (12-17 permanecem "(planejado)").

- [ ] **Step 2: Verificar**
```bash
grep -E "Programação Reativa/index" "03-Dominios/Tecnologia/Java/index.md"
grep -c "planejado" "03-Dominios/Tecnologia/Java/index.md"
```
Expected: wikilink ativo; "planejado" caiu exatamente 1 vs baseline.

- [ ] **Step 3: Commit** — `git add "<path>"` && `git commit -m "feat(java): ativa Galho 11 (Programação Reativa) no MOC central"`

---

## Task 20: Poda CIRÚRGICA do tronco (`Backend/Spring Boot.md`) — só a seção WebFlux

**Files:**
- Modify: `03-Dominios/Tecnologia/Java/Backend/Spring Boot.md`

- [ ] **Step 1: Ler o tronco e confirmar o range** (política §9 — ler antes de podar)
```bash
grep -nE "^## " "03-Dominios/Tecnologia/Java/Backend/Spring Boot.md"
```
Confirmar os limites reais de `## Spring WebFlux — visão geral` (início ~95, fim = imediatamente antes da próxima `## ` — `## Spring Cloud — visão geral` ~131). **Só esta seção é podada.**

- [ ] **Step 2: Podar `## Spring WebFlux — visão geral`** — substituir TODO o bloco da seção (do heading até imediatamente antes da próxima `## `, incluindo o `---` separador se houver, deixando um único `---` limpo antes de `## Spring Cloud`) por:
```markdown
## Spring WebFlux — visão geral

> [!nota] Migrado para galho próprio
> Expandido no galho [[03-Dominios/Tecnologia/Java/Programação Reativa/index|Programação Reativa]]. Veja [[03-Dominios/Tecnologia/Java/Programação Reativa/10 - Spring WebFlux — o stack não-bloqueante sobre Netty e o DispatcherHandler|Spring WebFlux]], [[03-Dominios/Tecnologia/Java/Programação Reativa/01 - O que é programação reativa — o modelo push, assíncrono e não-bloqueante|O que é programação reativa]] e o confronto honesto [[03-Dominios/Tecnologia/Java/Programação Reativa/14 - Reativo vs Virtual Threads — o confronto honesto|Reativo vs Virtual Threads]].
```
As menções incidentais (linha ~35 diagrama, ~735 sob `## Quando usar`) **permanecem intactas** — não as tocar.

- [ ] **Step 3: Atualizar `## Veja também` + frontmatter** — adicionar wikilink `[[03-Dominios/Tecnologia/Java/Programação Reativa/index|Programação Reativa]]` no "Veja também" do tronco (se já não houver); `updated: 2026-06-10`.

- [ ] **Step 4: Verificar (poda cirúrgica — uma seção só; resto intacto)**
```bash
grep -nE "^## " "03-Dominios/Tecnologia/Java/Backend/Spring Boot.md"
grep -c "Programação Reativa/index" "03-Dominios/Tecnologia/Java/Backend/Spring Boot.md"
grep -nE "Quando NÃO usar|ReactiveController|Não cobrimos em profundidade" "03-Dominios/Tecnologia/Java/Backend/Spring Boot.md"
grep -nE "Spring WebFlux, Spring Expression|Spring WebFlux:\*\* quando precisa" "03-Dominios/Tecnologia/Java/Backend/Spring Boot.md"
grep -nE "^## (Spring Cloud|Camadas típicas|Gerenciamento de transações|Spring MVC pipeline)" "03-Dominios/Tecnologia/Java/Backend/Spring Boot.md"
```
Expected: o `## Spring WebFlux — visão geral` agora é só callout (segundo grep ≥1 link); o conteúdo da seção (`Quando NÃO usar`/`ReactiveController`/`Não cobrimos em profundidade`) **sumiu** (terceiro grep VAZIO); as menções incidentais (diagrama linha ~35, "Quando usar" ~735) **AINDA PRESENTES** (quarto grep ≥2); callouts dos Galhos 8/9/10 (`## Gerenciamento de transações`/`## Spring MVC pipeline`) e seções de outros galhos (Spring Cloud/Camadas típicas) **AINDA PRESENTES** (último grep ≥3).

- [ ] **Step 5: Commit** — `git add "03-Dominios/Tecnologia/Java/Backend/Spring Boot.md"` && `git commit -m "refactor(java): poda cirúrgica do tronco Spring Boot — seção WebFlux migra pro galho 11"`

---

## Task 21: Quitar a dívida reversa (13 ponteiros → wikilinks)

**Files:**
- Modify: `03-Dominios/Tecnologia/Java/Concorrência e paralelismo/12 - Virtual Threads e Project Loom.md`
- Modify: `03-Dominios/Tecnologia/Java/Concorrência e paralelismo/index.md`
- Modify: `03-Dominios/Tecnologia/Java/Web e APIs REST/01 - O que é Spring MVC — a camada web sobre o container.md`
- Modify: `03-Dominios/Tecnologia/Java/Web e APIs REST/15 - Clientes HTTP — RestClient, WebClient, RestTemplate.md`
- Modify: `03-Dominios/Tecnologia/Java/Spring Core e Boot/index.md`
- Modify: `03-Dominios/Tecnologia/Java/Web e APIs REST/index.md`
- Modify: `03-Dominios/Tecnologia/Java/Persistência de dados/index.md`

- [ ] **Step 1: Relocalizar (por conteúdo — linhas podem ter mudado)**
```bash
grep -rn "Galho 11\|galho 11\|WebFlux\|R2DBC\|reativ" "03-Dominios/Tecnologia/Java/Concorrência e paralelismo/12 - Virtual Threads e Project Loom.md" "03-Dominios/Tecnologia/Java/Concorrência e paralelismo/index.md" "03-Dominios/Tecnologia/Java/Web e APIs REST/01 - O que é Spring MVC — a camada web sobre o container.md" "03-Dominios/Tecnologia/Java/Web e APIs REST/15 - Clientes HTTP — RestClient, WebClient, RestTemplate.md" "03-Dominios/Tecnologia/Java/Spring Core e Boot/index.md" "03-Dominios/Tecnologia/Java/Web e APIs REST/index.md" "03-Dominios/Tecnologia/Java/Persistência de dados/index.md"
```

- [ ] **Step 2: Aplicar os wikilinks** — em cada ponteiro, trocar o texto "Galho 11 (planejado)"/"WebFlux (Galho 11, planejado)" pelo wikilink, **mantendo natural a frase** e atualizando `updated: 2026-06-10` no frontmatter de cada arquivo tocado:
  - **Concorrência/12 - Virtual Threads (~81, callout):** "O confronto detalhado (backpressure, operadores, quando reativo ainda vence) pertence ao **Galho 11 — Programação Reativa**." → "...pertence ao **Galho 11** — [[03-Dominios/Tecnologia/Java/Programação Reativa/14 - Reativo vs Virtual Threads — o confronto honesto|Reativo vs Virtual Threads]]." (o link aponta pra nota que **paga** essa dívida).
  - **Concorrência/index (~91, item dedicado):** "- Programação Reativa (Galho 11) — planejado." → "- [[03-Dominios/Tecnologia/Java/Programação Reativa/index|Programação Reativa (Galho 11)]] — o modelo reativo e o confronto com Virtual Threads."
  - **Web 01 - O que é Spring MVC (~104):** "...o **WebFlux** (Galho 11, planejado), construído sobre Reactor..." → "...o **WebFlux** ([[03-Dominios/Tecnologia/Java/Programação Reativa/10 - Spring WebFlux — o stack não-bloqueante sobre Netty e o DispatcherHandler|Galho 11]]), construído sobre Reactor..."
  - **Web 01 - O que é Spring MVC (~188, comentário de código):** "// WebFlux (Galho 11, planejado) usaria outro starter e Mono<Order>." → "// WebFlux (Galho 11) usaria outro starter e Mono<Order>." (em comentário de código **não se põe wikilink** — só remover o "planejado"; o wikilink na prosa da linha 104 já quita a referência).
  - **Web 15 - Clientes HTTP (~23):** "O `WebClient` é o cliente reativo (parte do WebFlux; uso reativo/streaming = Galho 11, planejado)." → "O `WebClient` é o cliente reativo (parte do WebFlux; uso reativo/streaming = [[03-Dominios/Tecnologia/Java/Programação Reativa/11 - WebClient — o cliente HTTP reativo a fundo|Galho 11]])."
  - **Web 15 - Clientes HTTP (~113, heading):** "### WebClient: menção — reativo, do WebFlux (uso reativo/streaming = Galho 11, planejado)" → "### WebClient: menção — reativo, do WebFlux (uso reativo/streaming)" (**simplificar o heading**, remover o "(... Galho 11, planejado)"; o wikilink vai na prosa da linha ~127). **NÃO pôr wikilink em heading.**
  - **Web 15 - Clientes HTTP (~127):** "O uso aprofundado do `WebClient` — programação reativa, streaming de respostas, back-pressure — é tema do Galho 11 (planejado)." → "...é tema do galho [[03-Dominios/Tecnologia/Java/Programação Reativa/11 - WebClient — o cliente HTTP reativo a fundo|Programação Reativa]]."
  - **Web 15 - Clientes HTTP (~274):** "Reserve o `WebClient` para quando o serviço inteiro for reativo (tema do Galho 11, planejado)." → "...(tema do galho [[03-Dominios/Tecnologia/Java/Programação Reativa/11 - WebClient — o cliente HTTP reativo a fundo|Programação Reativa]])."
  - **Web 15 - Clientes HTTP (~303):** "O uso reativo/streaming do `WebClient` (WebFlux/Reactor) é tema do Galho 11 (planejado)." → "...é tema do galho [[03-Dominios/Tecnologia/Java/Programação Reativa/index|Programação Reativa]]." **MANTER** a menção ao Feign/Galho 16 na mesma frase como texto "(planejado)" (Galho 16 ainda não existe).
  - **Spring Core e Boot/index (~32, parágrafo de fronteira):** "Spring Reativa com WebFlux (Galho 11), Spring Security (Galho 12)... são todos planejados..." → "Spring Reativa com WebFlux é o galho [[03-Dominios/Tecnologia/Java/Programação Reativa/index|Programação Reativa]]; Spring Security (Galho 12), Testes no ecossistema Spring (Galho 13), e Microservices/Cloud com Spring Cloud (Galhos 16 e 17) são planejados..." **NÃO tocar o horizonte-list :97** (deixar 11/12/13/16 — ou ajustar só se o item 11 estiver lá isolado; conferir).
  - **Web e APIs REST/index (~32, parágrafo de fronteira):** "Spring Reativa/WebFlux (Galho 11), Spring Security (Galho 12)... são planejados..." → "Spring Reativa/WebFlux é o galho [[03-Dominios/Tecnologia/Java/Programação Reativa/index|Programação Reativa]]; Spring Security (Galho 12)... são planejados..." **NÃO tocar o horizonte-list :95.**
  - **Persistência de dados/index (~32, parágrafo de fronteira):** "Persistência reativa/R2DBC (Galho 11), segurança de dados (Galho 12)... são planejados, sem cobertura aqui." → "Persistência reativa/R2DBC é o galho [[03-Dominios/Tecnologia/Java/Programação Reativa/13 - R2DBC — persistência reativa sem EntityManager|Programação Reativa]]; segurança de dados (Galho 12), testes de repositório (Galho 13) e dados distribuídos/saga (Galho 16) são planejados..." **NÃO tocar o horizonte-list :92.**

- [ ] **Step 3: Verificar**
```bash
grep -rn "Galho 11\|galho 11" "03-Dominios/Tecnologia/Java/Concorrência e paralelismo/12 - Virtual Threads e Project Loom.md" "03-Dominios/Tecnologia/Java/Concorrência e paralelismo/index.md" "03-Dominios/Tecnologia/Java/Web e APIs REST/01 - O que é Spring MVC — a camada web sobre o container.md" "03-Dominios/Tecnologia/Java/Web e APIs REST/15 - Clientes HTTP — RestClient, WebClient, RestTemplate.md" "03-Dominios/Tecnologia/Java/Spring Core e Boot/index.md" "03-Dominios/Tecnologia/Java/Web e APIs REST/index.md" "03-Dominios/Tecnologia/Java/Persistência de dados/index.md" | grep -iE "planejado|11 \(plan" | grep -vE ":(95|97|92):"
```
Expected: **VAZIO** ou só o comentário de código da Web 01 :188 (`// WebFlux (Galho 11) usaria...` — sem "planejado") e os horizonte-lists :95/:97/:92 (que mantêm 11/12/13/16 como "(planejado)"). Conferir manualmente que cada "Galho 11" remanescente vem acompanhado do wikilink "Programação Reativa", e que os horizonte-lists permanecem intactos.

- [ ] **Step 4: Commit** — `git add` nominal dos 7 arquivos && `git commit -m "refactor(java): quita dívida reversa do galho 11 — ponteiros de reativo viram wikilinks"`

---

## Task 22: Verificação final do galho

**Files:** (somente leitura/verificação)

- [ ] **Step 1: 16 notas + MOC**
```bash
ls "03-Dominios/Tecnologia/Java/Programação Reativa/" | sort
```
Expected: 01..16 + index.md (17 arquivos).

- [ ] **Step 2: Fases (4/8/4)**
```bash
for f in "03-Dominios/Tecnologia/Java/Programação Reativa/"[0-9]*.md; do grep -H "^fase:" "$f"; done
```
Expected: 01-04 `iniciado`, 05-12 `adepto`, 13-16 `magus`.

- [ ] **Step 3: Seções obrigatórias (3 por nota)**
```bash
for f in "03-Dominios/Tecnologia/Java/Programação Reativa/"[0-9]*.md; do echo "$f: $(grep -cE '^## (Em entrevista|Armadilhas|Veja também)' "$f")"; done
```
Expected: 3 em todas.

- [ ] **Step 4: Anti-fabricação + estatística inventada + fronteiras (greps decisivos)**
```bash
grep -riE "minha experiência|no meu projeto|josenaldo|Patient|Doctor|Appointment|MedEspecialista|market share|% d[ao]s (dev|empresas|projetos)|maioria (adota|migrou)" "03-Dominios/Tecnologia/Java/Programação Reativa/"
grep -rE "\[\[[^]]*(Galho (12|13|14|16)|Spring Security|Reactor Kafka|StepVerifier|circuit breaker|saga)" "03-Dominios/Tecnologia/Java/Programação Reativa/"
grep -rn '\[\[#' "03-Dominios/Tecnologia/Java/Programação Reativa/"
```
Expected: **todos VAZIOS**.

- [ ] **Step 5: Quádrupla fronteira-assinatura (links de volta aos Galhos 4, 8, 9 e 10 presentes)**
```bash
grep -rl "Concorrência e paralelismo/12" "03-Dominios/Tecnologia/Java/Programação Reativa/" | sort
grep -rl "Web e APIs REST/0(1|6)" "03-Dominios/Tecnologia/Java/Programação Reativa/" | sort
grep -rl "Web e APIs REST/15" "03-Dominios/Tecnologia/Java/Programação Reativa/" | sort
grep -rl "Persistência de dados/0(1|3|7)" "03-Dominios/Tecnologia/Java/Programação Reativa/" | sort
grep -rl "Spring Core e Boot/(06|15)" "03-Dominios/Tecnologia/Java/Programação Reativa/" | sort
```
Expected: notas 01/08/09/14/15/16 linkam pro Galho 4 (Virtual Threads); notas 01/07/10/12/15/16 linkam pro Galho 9 (MVC/DispatcherServlet); nota 11 linka pro Galho 9 nota 15 (WebClient); notas 13/16 linkam pro Galho 10 (R2DBC vs JPA); nota 10 linka pro Galho 8 (auto-config).

- [ ] **Step 6: Frase pronta (1 por nota)**
```bash
for f in "03-Dominios/Tecnologia/Java/Programação Reativa/"[0-9]*.md; do echo "$f: $(grep -c '### Frase pronta (inglês)' "$f")"; done
```
Expected: 1 em todas.

- [ ] **Step 7: Tronco — poda cirúrgica confirmada; vizinhos intocados**
```bash
grep -c "Programação Reativa/index" "03-Dominios/Tecnologia/Java/Backend/Spring Boot.md"
grep -nE "ReactiveController|Quando NÃO usar|Não cobrimos em profundidade" "03-Dominios/Tecnologia/Java/Backend/Spring Boot.md"
grep -nE "^## (Spring WebFlux|Spring Cloud|Gerenciamento de transações)" "03-Dominios/Tecnologia/Java/Backend/Spring Boot.md"
git status --short "03-Dominios/Tecnologia/Java/Backend/Spring Security.md" "03-Dominios/Tecnologia/Java/Backend/Kafka/" "03-Dominios/Tecnologia/Java/Backend/Spring Data JPA.md"
```
Expected: `Spring Boot.md` com ≥1 link "Programação Reativa", conteúdo da seção WebFlux **VAZIO** (segundo grep), `## Spring WebFlux`/`## Spring Cloud`/`## Gerenciamento de transações` presentes (callouts/intactos); `Spring Security.md`/`Kafka/`/`Spring Data JPA.md` **sem modificação**.

- [ ] **Step 8: Skill `verificar-wikilinks`** — rodar na pasta `03-Dominios/Tecnologia/Java/Programação Reativa/` + conferir os arquivos tocados fora (MOC central, Dicionário, o tronco Spring Boot, os 2 arquivos Concorrência + 2 Web + 1 Spring Core index + 1 Persistência index da dívida reversa). Âncoras `Dicionário de Java#...` resolvem 1:1 (cross-check com o grep da Task 18 Step 1). As quebras legadas da árvore Java NÃO são deste galho — só corrigir o que este galho introduziu. Corrigir e commitar à parte se houver.

- [ ] **Step 9: Resumo de fechamento (sem commit)** — reportar: 16 notas (4/8/4), ~28 verbetes (296→~324), MOC galho + MOC central, **poda cirúrgica** (seção WebFlux do `Spring Boot.md` vira callout; menções incidentais preservadas), **dívida reversa quitada** (13 ponteiros; horizonte-lists e galhos 12-16 preservados como "(planejado)"; a dívida do confronto da nota 12 do Galho 4 paga pela nota 14), troncos vizinhos intocados (mostrar o grep), wikilinks limpos, **tese reativo-vs-VT honesta (sem hype/estatística inventada)**. Commits locais na `main`; **push manual do usuário; sem deploy**. Atualizar memória [[project_trilha_java]] com Galho 11 completo + fatos cravados via WebFetch (Reactor 3.x, `Flow` Java 9, WebFlux/Boot 3.x, R2DBC sem EntityManager/lazy, VT Java 21 GA).

---

## Self-Review (preenchido na escrita do plano)

**Spec coverage:** Tasks 1-16 ↔ spec §3.1 (16 notas, escopos idênticos, opus 05/08/09/10/13/14/16, distribuição 4/8/4); Task 17 ↔ §3.2 (MOC, 5 rotas iguais); Task 18 ↔ §3.3 (~28 verbetes, âncoras 1:1 por grep, dups conferidos/linkados com Galhos 4/9); Task 19 ↔ §3.4 (item 11); Task 20 ↔ §3.5.1 (poda cirúrgica — só `## Spring WebFlux — visão geral`; menções incidentais linha 35/735 intactas; callouts dos Galhos 8/9/10 intocados); Task 21 ↔ §3.5.2 (13 ponteiros, mapeamento idêntico, horizonte-lists :95/:97/:92 preservados, galhos 12-16 como texto, a dívida do confronto do Galho 4 paga pela nota 14); Task 0 ↔ §6 (pré-flight, baseline 296, range da poda); Task 22 ↔ §7. Quádrupla fronteira-assinatura (§4.3.1) garantida por links obrigatórios pros Galhos 4/8/9/10 nas Tasks 1/7/8/9/10/11/12/13/14/15/16 e pelo grep da Task 22 Step 5; fronteira galhos 12-16 pelo grep da Task 22 Step 4.

**Placeholder scan:** sem TBD/TODO; cada nota tem fonte WebFetch nomeada com URL, frontmatter concreto, H3s, armadilhas mínimas com conteúdo real, tamanho-alvo herdado das convenções. Pontos version-sensitive marcados com "verificar/confirmar" são instruções de verificação WebFetch (a essência da parte pesquisa do galho novo), não placeholders: Reactor 3.x, `Flow` Java 9, WebFlux/Boot 3.x, R2DBC sem EntityManager/lazy, VT Java 21 GA, posição do Spring sobre VT. A confirmação dos ranges/linhas do tronco e da dívida reversa (Tasks 0/20/21) é resolução-na-execução por política §9 do roadmap (ler antes de podar/editar).

**Type/naming consistency:** numeração 01-16 idêntica entre tasks, MOC, Dicionário, dívida reversa, poda e cheatsheet da capstone; distribuição 4/8/4 consistente; opus 05/08/09/10/13/14/16 marcadas ⟦opus⟧; filenames com em dash (sem `:`/`/` — nota 09 usa "BUFFER, DROP, LATEST" com vírgula, sem dois-pontos); mapeamento de link-back Galho 4→nota 12, Galho 9→notas (01/06/15), Galho 10→notas (01/03/07), Galho 8→notas (06/15) consistente entre spec §3.1, convenções e Tasks; âncoras do Dicionário extraídas por grep antes de inserir (Task 18) e validadas na Task 22; verbetes adjacentes (`WebClient` G9↔G11, `Virtual Threads` G4↔nota 14, `Netty` G9↔G11) linkados, não duplicados.
