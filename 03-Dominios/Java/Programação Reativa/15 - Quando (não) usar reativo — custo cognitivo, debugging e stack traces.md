---
title: "Quando (não) usar reativo — custo cognitivo, debugging e stack traces"
created: 2026-06-10
updated: 2026-06-10
type: concept
progress: backlog
status: seedling
publish: true
fase: magus
tags:
  - java
  - reativa
  - magus
  - reactor
aliases:
  - "quando não usar reativo"
  - "custo cognitivo do reativo"
---

# Quando (não) usar reativo — custo cognitivo, debugging e stack traces

> [!abstract] TL;DR
> O reativo cobra um **custo cognitivo real**: stack traces fragmentados (a thread que estoura não é a que montou a cadeia), debugging sem _step_ num pipeline _lazy_/assíncrono, **contágio** (uma única lib bloqueante no meio anula o ganho) e a curva de aprendizado da equipe. Ele só vale quando o ganho é concreto — _streaming_ real, _backpressure_ de verdade, ou um _stack_ que já é reativo de ponta a ponta. Para CRUD comum com **Java 21+**, [[03-Dominios/Java/Concorrência e paralelismo/12 - Virtual Threads e Project Loom|Virtual Threads]] + [[03-Dominios/Java/Web e APIs REST/01 - O que é Spring MVC — a camada web sobre o container|Spring MVC]] é o _default_ mais barato. A própria doc do Spring é direta: _"If you have a Spring MVC application that works fine, there is no need to change."_

## O que é

Esta é a nota de **honestidade total** do galho. As notas anteriores ensinaram o _como_: `Mono`/`Flux`, operadores, `Schedulers`, `backpressure`, WebFlux. Esta pergunta o _quando não_ — porque "reativo é não-bloqueante, logo é mais rápido" é uma meia-verdade que custa caro quando aplicada sem critério.

A tese: o reativo é uma **ferramenta de troca**, não um _upgrade_. Você troca um modelo imperativo simples (uma _thread_ por requisição, _stack trace_ linear, _step debugger_ funcionando) por um modelo declarativo eficiente em I/O, mas com um custo cognitivo que se paga em horas de _debugging_ e em onboarding. Quando o ganho de eficiência é real e grande, a troca compensa. Quando não é, você importou toda a complexidade sem o benefício.

É importante separar essa crítica do que ela **não** é. Não é dizer que reativo é ruim, ou que Reactor é mal projetado, ou que ninguém deveria usar — é uma tecnologia excelente para os problemas que ela resolve. A crítica é de **adequação**: usar a ferramenta certa no lugar errado degrada qualquer projeto, e o reativo é particularmente caro de aplicar mal porque seus custos (debugging, onboarding) são contínuos e difíceis de reverter depois que o sistema cresceu. A nota não pede que você abandone o reativo; pede que você o **escolha conscientemente**, com um requisito que o justifique, em vez de adotá-lo por inércia ou moda.

## Por que importa

Em entrevista sênior, defender reativo sem reconhecer seus custos sinaliza imaturidade — soa _hype-driven_. O sinal de senioridade é o oposto: saber recusar a ferramenta da moda quando ela não cabe no problema.

E o contexto mudou. Antes do **Java 21**, reativo era quase a única forma de escalar I/O sem estourar _threads_ de plataforma. Hoje, Virtual Threads entregam alta concorrência de I/O **mantendo o código imperativo** — _stack traces_ inteiros, _step debugging_, `try/catch` normal. Isso desloca o ponto de equilíbrio: a faixa de problemas onde "reativo é a única saída" encolheu bastante. Saber onde ela ainda existe (e onde não existe mais) é o cerne desta nota. Veja o confronto detalhado em [[03-Dominios/Java/Programação Reativa/14 - Reativo vs Virtual Threads — o confronto honesto|Reativo vs Virtual Threads]].

Vale separar os dois eixos que o reativo combina e o hype confunde. Eixo um: **escalabilidade de I/O** — atender muita concorrência sem uma _thread_ de plataforma travada por requisição. Eixo dois: **semântica de fluxo** — `backpressure`, composição de _streams_, operadores sobre dados contínuos. Antes do Loom, o eixo um arrastava o eixo dois: você adotava todo o modelo reativo só para ganhar a escalabilidade. Virtual Threads quebram esse acoplamento — agora você consegue a escalabilidade de I/O **sem** assinar a semântica de fluxo. Por isso a pergunta certa virou: "eu preciso da _semântica de fluxo_?". Se a resposta é não — e para CRUD ela quase sempre é —, o reativo perdeu o argumento que o justificava. Restou só o que dá `backpressure` e _streaming_ de verdade.

## Como funciona

### Stack traces fragmentados: a thread que estoura não é a que montou

No imperativo, o _stack trace_ é uma narrativa: cada linha conta quem chamou quem, do `main` até o ponto da exceção. No reativo, a **montagem** (_assembly_ — onde você declara `flux.map(...).flatMap(...)`) e a **execução** (onde o erro de fato acontece, possivelmente em outra _thread_ via [[03-Dominios/Java/Programação Reativa/08 - Schedulers — subscribeOn, publishOn e em qual thread o código roda|Schedulers]]) são momentos e _threads_ diferentes. Resultado: o _stack trace_ mostra as engrenagens internas do Reactor e o ponto de _subscription_ — que a própria doc descreve como o ponto "_less interesting_" — mas **não** a linha da sua cadeia onde o erro nasceu.

O Reactor oferece duas recuperações, ambas com custo:

- **`Hooks.onOperatorDebug()`** — modo de _debug_ global que captura o _stack trace_ de montagem de **todo operador**. A doc é explícita sobre o preço: _"creating a stack trace is costly. That is why this debugging feature should only be activated in a controlled manner, as a last resort."_ É a forma "mais fácil, mas também a mais lenta" — proibido em produção.
- **`checkpoint()`** — instrumenta **pontos específicos** da cadeia. Custo localizado em vez de global; a variante `checkpoint(String)` "impõe menos custo de processamento que um `checkpoint` regular". É o que você usa quando já sabe qual cadeia precisa de rastreabilidade.

O ponto cognitivo: no imperativo, o contexto de erro é grátis e sempre completo. No reativo, é um recurso que você **paga** (em _overhead_) e **planeja** (onde colocar os `checkpoint`).

Há uma assimetria perversa aqui. O modo barato (`checkpoint`) só ajuda se você **já tinha previsto** que aquele trecho daria problema — ou seja, antes do _bug_ existir. O modo que ajuda em qualquer lugar (`Hooks.onOperatorDebug()`) é caro demais para ficar ligado. Então, no momento exato em que você mais precisa de contexto — um erro inesperado em produção — você normalmente tem o pior dos dois: sem `checkpoint` naquele ponto e sem o _hook_ global ligado. A doc sugere o meio-termo `ReactorDebugAgent` (instrumentação por _bytecode_, custo só na inicialização), mas mesmo ele é uma dependência extra e uma decisão consciente — nada disso é o _default_ gratuito do imperativo.

### Debugging sem step: o pipeline é lazy e assíncrono

Um _breakpoint_ dentro de um `.map(x -> ...)` dispara no momento da **montagem** da cadeia, não quando o dado flui — porque [[03-Dominios/Java/Programação Reativa/04 - Nada acontece até o subscribe — lazy, assembly vs subscription, cold vs hot|nada acontece até o subscribe]]. Dar _step over_ não percorre o fluxo de dados; ele percorre a construção da cadeia. Quando o dado finalmente passa, ele passa potencialmente em outra _thread_, fora do alcance do seu _step_.

Na prática isso significa: o ciclo "_breakpoint_ → _step_ → inspeciona variável" — o pão com manteiga do _debugging_ imperativo — **não funciona** num pipeline reativo. Você troca _step debugging_ por `log()`, `doOnNext()`, `doOnError()` e `checkpoint()`. É observabilidade por instrumentação, não por inspeção interativa. Funciona, mas é uma habilidade diferente que a equipe precisa adquirir.

Some um detalhe que parece menor e custa caro: **variáveis locais não atravessam o pipeline**. No imperativo, qualquer variável no escopo está disponível no _breakpoint_. No reativo, o estado que você precisa carregar entre operadores não está numa variável local — ele precisa fluir pelo próprio fluxo (via `zip`, `tuple`, ou o `Context` do Reactor). Logo, mesmo que você consiga parar num ponto, o que está visível ali raramente é o que você quer inspecionar. O modelo mental de "abrir o programa e olhar por dentro" não se aplica; você passa a raciocinar sobre o fluxo a partir de _logs_ ordenados no tempo — uma mudança real de como se diagnostica um problema.

### Contágio: uma lib bloqueante no meio anula o ganho

O modelo não-bloqueante depende de um _event loop_ com **poucas** _threads_ que nunca podem parar. Se uma chamada bloqueante (um driver JDBC, um SDK síncrono, um `Thread.sleep`, um `.block()` mal colocado) roda numa _thread_ do _event loop_, ela **trava o loop inteiro** — todas as outras requisições naquela _thread_ ficam paradas. O ganho de escalabilidade evapora, e você ainda paga toda a complexidade reativa.

A doc do Spring põe isso em termos de dependências: _"If you have blocking persistence APIs (JPA, JDBC) or networking APIs to use, Spring MVC is the best choice for common architectures at least. It is technically feasible \[...\] to perform blocking calls on a separate thread but you would not be making the most of a non-blocking web stack."_ Ou seja: dá para isolar o bloqueante num _scheduler_ separado (`Schedulers.boundedElastic()`), mas aí você está rodando um modelo de _thread pool_ disfarçado de reativo — sem o benefício, com o custo. É o pior dos dois mundos.

O contágio é especialmente traiçoeiro porque é **silencioso em desenvolvimento**. Com um usuário e baixa concorrência, a chamada bloqueante na _thread_ do _event loop_ termina rápido e nada parece errado — testes passam, _demo_ funciona. O problema só aparece sob carga real, quando várias requisições disputam as poucas _threads_ do loop e uma chamada lenta congela todas as outras que compartilham aquela _thread_. É uma bomba-relógio que não dispara no ambiente onde você normalmente a encontraria. Por isso o Reactor oferece o `BlockHound` — um agente que detecta chamadas bloqueantes em _threads_ não-bloqueantes e estoura na hora; vale a pena no _stack_ reativo justamente porque o olho humano não pega esse erro em revisão de código.

### Curva da equipe vs o ganho real: o checklist honesto

Reativo é um modelo de programação **declarativo, funcional e não-bloqueante** simultaneamente — três mudanças de paradigma de uma vez. A doc do Spring reconhece: _"Imperative programming is the easiest way to write, understand, and debug code"_ e, para times grandes, _"keep in mind the steep learning curve in the shift to non-blocking, functional, and declarative programming."_ A recomendação oficial é cautelosa: _"start small and measure the benefits \[...\] We expect that, for a wide range of applications, the shift is unnecessary."_

A pergunta de decisão não é "reativo é melhor?" — é "**o ganho de I/O é grande o bastante para pagar o custo cognitivo permanente desta equipe?**". Na maioria dos CRUDs, a resposta honesta é não.

## Na prática

### Stack trace fragmentado vs com checkpoint

Sem instrumentação, o _trace_ aponta para as engrenagens do Reactor, não para a sua cadeia:

```text
java.lang.IndexOutOfBoundsException: Index 5 out of bounds for length 3
    at java.base/...Objects.checkIndex(Objects.java:385)
    at java.base/...ArrayList.get(ArrayList.java:427)
    at reactor.core.publisher.FluxMap$MapSubscriber.onNext(FluxMap.java:106)
    at reactor.core.publisher.FluxFlatMap$FlatMapMain.onNext(FluxFlatMap.java:386)
    at reactor.core.publisher.FluxRange$RangeSubscription.slowPath(FluxRange.java:154)
    at reactor.core.publisher.Operators$...request(...)
    ... (50+ linhas internas do Reactor, nenhuma do SEU código de montagem)
```

Com um `checkpoint("após enriquecer usuário")` na cadeia, o Reactor anexa o ponto de montagem:

```text
java.lang.IndexOutOfBoundsException: Index 5 out of bounds for length 3
    ...
Error has been observed at the following site(s):
    *__checkpoint ⇢ após enriquecer usuário
Original Stack Trace:
    at com.exemplo.UserService.enrich(UserService.java:42)   <-- AGORA aponta pro seu código
```

A diferença entre 30 minutos e 30 segundos de investigação mora nesse `checkpoint`. Mas note: **você teve que prever** onde colocá-lo. No imperativo, esse contexto viria de graça.

### Contágio em código: o bloqueante escondido

O anti-padrão clássico — uma chamada bloqueante (`JpaRepository`) executada direto na _thread_ do _event loop_:

```java
// PROBLEMA: findById() é bloqueante (JDBC) e roda na thread do event loop Netty.
// Sob carga, trava o loop inteiro — todas as requisições daquela thread param.
@GetMapping("/{id}")
public Mono<User> get(@PathVariable Long id) {
    return Mono.fromCallable(() -> jpaRepository.findById(id).orElseThrow());
    // sem Scheduler: roda no event loop — contágio silencioso
}
```

Se o bloqueante é inevitável, o mínimo é isolá-lo num _scheduler_ elástico — mas reconhecendo que isso é um _thread pool_ disfarçado, sem o ganho não-bloqueante real:

```java
// MENOS RUIM: empurra o bloqueante pra fora do event loop.
// Honesto, mas é thread pool com roupa reativa — se TODO o stack é assim, use MVC.
return Mono.fromCallable(() -> jpaRepository.findById(id).orElseThrow())
           .subscribeOn(Schedulers.boundedElastic());
```

A pergunta que essa correção levanta é a própria tese da nota: se você está empurrando tudo para `boundedElastic`, por que não Spring MVC + Virtual Threads, que faz isso de forma nativa e _step-debuggable_?

### Casos de fronteira (onde a resposta não é óbvia)

Nem todo caso cai limpo de um lado. Alguns exemplos de fronteira para calibrar o julgamento:

- **Stack já reativo, recurso novo é CRUD.** Se o sistema já é WebFlux de ponta a ponta e a equipe domina, adicionar mais um endpoint CRUD reativo é coerente — a coerência do _codebase_ pesa mais que o ganho marginal de I/O daquele endpoint isolado. Aqui o reativo "vence" por consistência, não por mérito técnico do caso.
- **Microsserviço de _gateway_/agregação.** Chamar vários serviços _downstream_ em paralelo e compor as respostas é um caso onde os operadores reativos (`zip`, `flatMap`) brilham — mesmo sem _streaming_ contínuo. Ainda assim, com Java 21+, _structured concurrency_ + Virtual Threads cobre boa parte disso de forma imperativa.
- **Picos de concorrência extrema com I/O leve.** Antes do Loom, esse era o território natural do reativo. Hoje é exatamente onde Virtual Threads competem de igual para igual — meça antes de assumir que o reativo é necessário.

O padrão dos três casos: a fronteira raramente é resolvida por "reativo é mais rápido". É resolvida por contexto — _codebase_ existente, forma do problema, versão do Java disponível.

### Checklist de decisão

```text
USE REATIVO SE (todos pesam a favor):
  [ ] Streaming real — SSE, WebSocket, dados que chegam contínuos (não req/resp simples)
  [ ] Backpressure de verdade — produtor mais rápido que consumidor, precisa de request(n)
  [ ] Stack JÁ é reativo de ponta a ponta — driver R2DBC, WebClient, sem ilhas bloqueantes
  [ ] Equipe domina o modelo OU vai investir sério em aprendê-lo

NÃO USE REATIVO SE (qualquer um pesa contra):
  [ ] CRUD comum — req chega, consulta banco, devolve JSON
  [ ] Dependência bloqueante no caminho — JPA, JDBC, SDK síncrono (= contágio)
  [ ] Equipe sem experiência e sem tempo de onboarding
  [ ] Java 21+ disponível — Virtual Threads dão concorrência de I/O com código imperativo

DEFAULT MAIS BARATO p/ CRUD em Java 21+:
  Virtual Threads + Spring MVC — imperativo, step-debuggable, stack trace inteiro,
  e ainda escala I/O. Reativo vira escolha deliberada, não padrão.
```

A regra de ouro: **reativo é uma escolha que você justifica, não um _default_ que você assume.**

## Armadilhas

### (1) Reativo por hype / CV-driven development

Adotar WebFlux porque "é moderno", "todo mundo usa" ou para enfeitar o currículo da equipe — sem nenhum requisito de _streaming_ ou _backpressure_ que justifique.

**Exemplo:** uma API de cadastro de clientes (POST cria, GET lista, PUT edita) reescrita em WebFlux + R2DBC. Zero _streaming_, zero _backpressure_, tráfego modesto. O time agora gasta o dobro do tempo em cada _bug_ porque os _stack traces_ não ajudam e o _step debugging_ sumiu. O ganho de escalabilidade nunca foi necessário — a carga sempre coube num _thread pool_ comum.

**Fix:** exija um requisito concreto antes de ir reativo. Se você não consegue nomear o _streaming_ ou o _backpressure_ que está resolvendo, não há o que resolver. _"We expect that, for a wide range of applications, the shift is unnecessary."_

### (2) Reativo "pela metade" — uma lib bloqueante no meio anula tudo

Montar todo o _stack_ reativo, mas manter uma única chamada bloqueante no caminho quente — um repositório JPA, um SDK síncrono de terceiros, um `.block()` "só nesse caso".

**Exemplo:** controller WebFlux → service que chama `jpaRepository.findById()` (bloqueante) direto numa _thread_ do _event loop_ Netty. Sob carga, essa chamada trava a _thread_ do loop; como o Netty tem poucas _threads_, poucas requisições lentas congelam o servidor inteiro. Você tem toda a complexidade reativa **e** o gargalo do bloqueante — o pior dos dois mundos.

**Fix:** ou o _stack_ é reativo de ponta a ponta (R2DBC em vez de JPA, `WebClient` em vez de cliente síncrono), ou você isola o bloqueante explicitamente em `Schedulers.boundedElastic()` — e aí reconhece que está rodando um _thread pool_ disfarçado, sem o ganho não-bloqueante. _"You would not be making the most of a non-blocking web stack."_ Se há bloqueante inevitável, Spring MVC é mais honesto.

### (3) Subestimar o custo de onboarding e debugging

Tratar a curva de aprendizado como um custo único de _setup_, quando ela é um **imposto permanente** sobre cada _bug_, cada nova contratação e cada plantão.

**Exemplo:** o arquiteto domina Reactor e entrega o sistema. Seis meses depois, ele saiu; o time remanescente leva horas para diagnosticar um erro porque o _stack trace_ é opaco e ninguém sabe onde colocar `checkpoint()`. O _onboarding_ de um júnior, que seria de dias num código imperativo, vira de semanas. O custo não estava no _setup_ — estava na operação contínua.

**Fix:** ao estimar a adoção, conte o custo recorrente: _debugging_ mais lento, _onboarding_ mais longo, _bus factor_ menor. _"If you have a large team, keep in mind the steep learning curve in the shift to non-blocking, functional, and declarative programming."_ Comece pequeno, meça o ganho, e só expanda se o benefício real superar esse imposto.

## Em entrevista

### Frase pronta (inglês)

> Reactive programming isn't a free upgrade — it's a trade. You gain non-blocking I/O efficiency, but you pay a real cognitive cost: stack traces are fragmented because the thread that throws isn't the one that assembled the chain, and you lose interactive step-debugging through a lazy, asynchronous pipeline. The contagion problem is the subtle killer — a single blocking dependency like a JPA or JDBC call on the event loop negates the entire benefit, so you end up with all the complexity and none of the gain. My default for ordinary CRUD on Java 21 and up is Virtual Threads with Spring MVC: imperative code that still scales I/O, stays step-debuggable, and keeps full stack traces. I reach for reactive only when there's a concrete justification — real streaming, genuine backpressure, or a stack that's already reactive end to end. As the Spring docs put it, if your MVC application works fine, there's no need to change.

### Vocabulário

| Termo PT | Termo EN |
| --- | --- |
| custo cognitivo | cognitive cost / cognitive load |
| stack trace fragmentado | fragmented stack trace |
| ponto de montagem (da cadeia) | assembly point |
| depuração interativa / passo a passo | interactive / step debugging |
| contágio (lib bloqueante) | blocking contagion |
| event loop | event loop |
| curva de aprendizado acentuada | steep learning curve |
| de ponta a ponta | end to end |

## Veja também

- [[03-Dominios/Java/Programação Reativa/14 - Reativo vs Virtual Threads — o confronto honesto|Reativo vs Virtual Threads]]
- [[03-Dominios/Java/Programação Reativa/08 - Schedulers — subscribeOn, publishOn e em qual thread o código roda|Schedulers]]
- [[03-Dominios/Java/Concorrência e paralelismo/12 - Virtual Threads e Project Loom|Virtual Threads e Project Loom]] (Galho 4 — a alternativa)
- [[03-Dominios/Java/Web e APIs REST/01 - O que é Spring MVC — a camada web sobre o container|O que é Spring MVC]] (Galho 9 — o default imperativo)
- [[03-Dominios/Java/Programação Reativa/index|Programação Reativa (MOC do galho)]]
- [[03-Dominios/Java/index|Trilha Java]]
- [[03-Dominios/Java/Dicionário de Java|Dicionário de Java]]

## Referências

- Project Reactor Reference — _Debugging a Reactor Application_ (`Hooks.onOperatorDebug()`, `checkpoint()`, _assembly_ vs execução): https://projectreactor.io/docs/core/release/reference/debugging.html
- Spring Framework Reference — _Web on Reactive Stack / WebFlux Applicability_ (quando usar WebFlux vs MVC, dependências bloqueantes, curva de aprendizado): https://docs.spring.io/spring-framework/reference/web/webflux/new-framework.html
