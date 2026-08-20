---
title: "Gateway reativo vs MVC — as duas variantes"
created: 2026-06-12
updated: 2026-06-12
type: concept
status: seedling
publish: true
fase: Adepto
tags:
  - java
  - microservices
  - adepto
  - gateway
aliases:
  - "Gateway reativo vs MVC"
  - "Spring Cloud Gateway Server WebMVC"
---

# Gateway reativo vs MVC — as duas variantes

> [!abstract] TL;DR
> O Spring Cloud Gateway hoje tem **duas variantes vivas** do servidor — você escolhe uma na hora de declarar o *starter*:
> - **Reativa** — `spring-cloud-starter-gateway-server-webflux`. Roda sobre **WebFlux/Netty**, modelo **não-bloqueante**. É o gateway **original**, o que a maioria dos tutoriais ainda assume.
> - **MVC** — `spring-cloud-starter-gateway-server-webmvc`. Roda sobre o **stack servlet** (bloqueante). É a variante **mais nova**, para quem **não quer** carregar o modelo reativo só por causa do gateway.
> - Os dois *starters* foram **renomeados** no trem **2025.x**: o reativo era `spring-cloud-starter-gateway` e o MVC era `spring-cloud-starter-gateway-mvc`. Usar o nome antigo é a armadilha número um.
> Regra de bolso: **time já reativo → WebFlux; time servlet/MVC sem fluência reativa → WebMVC.** O modelo reativo em si (Netty, *backpressure*) é assunto do **Galho 11** — aqui você só escolhe a variante.

## O que é

O [[03-Dominios/Tecnologia/Java/Microservices e sistemas distribuídos/10 - API Gateway — papel, roteamento, predicates e filters|API Gateway]] é a porta única na frente dos seus serviços: roteia, filtra, casa *predicates*. O Spring Cloud Gateway é a implementação idiomática desse papel no ecossistema Spring.

O que muitos não percebem é que **"Spring Cloud Gateway" não é mais um produto só**. Existem **duas variantes do servidor**, que fazem o mesmo trabalho de gateway, mas assentam sobre **stacks web diferentes**:

1. **Gateway Server WebFlux** — o gateway **reativo**, sobre o stack **WebFlux/Netty**, **não-bloqueante**. É a encarnação histórica: por anos, "Spring Cloud Gateway" *era* isto, e ponto.
2. **Gateway Server WebMVC** — o gateway sobre o stack **Spring MVC (servlet)**, **bloqueante**. Nasceu para um público específico: quem tem uma aplicação MVC tradicional e **não quer** introduzir o runtime reativo só para ter um gateway.

> [!info] Feynman: duas portarias para o mesmo prédio
> Imagine o gateway como a portaria de um condomínio. As duas variantes fazem o mesmo serviço — conferem quem entra, encaminham para o bloco certo. A diferença é o **regime de trabalho do porteiro**. Na variante reativa (WebFlux), um único porteiro atende muitas pessoas ao mesmo tempo, sem ficar parado esperando o elevador de cada uma chegar. Na variante MVC (servlet), cada atendimento ocupa um porteiro do início ao fim. O serviço entregue é igual; o que muda é **como o trabalho é organizado por baixo** — e isso decide qual contratar para o seu prédio.

A escolha entre elas acontece num ponto bem concreto: **qual *starter* você coloca no `pom.xml`/`build.gradle`**. Daí a importância de acertar o nome — e os nomes mudaram.

## Por que importa

Porque a variante errada **arrasta um stack inteiro** para o seu projeto. Não é uma flag de configuração que você troca depois; é a fundação web da aplicação.

Se você é um time **servlet/MVC tradicional** e adota, por inércia, o gateway reativo, acabou de trazer **WebFlux e Netty** para dentro de casa — um modelo de programação diferente, com regras próprias de *debug* e de não-bloqueio. Um `Thread.sleep`, um JDBC bloqueante ou um cliente HTTP síncrono no lugar errado e você **trava o event loop** do Netty, derrubando a vazão de tudo. Esse custo é real, e é exatamente o que a variante **WebMVC** existe para evitar: ela deixa você ter um gateway **sem** sair do mundo servlet que o time já domina.

Do outro lado, se você **já é reativo** — sua aplicação é WebFlux, seu time conhece `Mono`/`Flux` e *backpressure* —, escolher a variante MVC seria abrir mão do modelo não-bloqueante justamente onde ele rende mais: um ponto de altíssima concorrência de I/O de rede, que é o cenário-tese do reativo.

E há a armadilha de **tooling** que afeta os dois: os *starters* foram **renomeados** no trem **2025.x**. Tutoriais, respostas de fórum e até notas suas de 2023-2024 ainda citam os nomes antigos. Colar o nome velho num projeto novo é o erro mais comum desta nota — e nem sempre o erro é óbvio no log.

## Como funciona

### A variante reativa — WebFlux/Netty

O **Gateway Server WebFlux** é o gateway **original** e **não-bloqueante**. Ele assenta sobre o stack **Spring WebFlux**, que por sua vez roda sobre o servidor **Netty**. *Starter*:

- **Atual (2025.x):** `spring-cloud-starter-gateway-server-webflux`
- **Antigo:** `spring-cloud-starter-gateway`

O ponto que a documentação crava: esse gateway **exige o runtime Netty** fornecido pelo Spring Boot + Spring WebFlux. Ele **não roda** num container servlet tradicional nem empacotado como WAR. Ou seja, ao escolher a variante reativa, você está escolhendo o stack reativo inteiro — não dá para "só usar o gateway" sem ele.

> [!important] Fronteira de galho — Galho 11 (Programação Reativa)
> **WebFlux, Netty, event loop, não-bloqueio e *backpressure*** são o assunto do [[03-Dominios/Tecnologia/Java/Programação Reativa/10 - Spring WebFlux — o stack não-bloqueante sobre Netty e o DispatcherHandler|Galho 11]]. **Esta nota não re-explica o modelo reativo** — ela só registra que a variante WebFlux do gateway *é construída sobre ele*. Se a dúvida for "como o event loop não-bloqueia?" ou "o que é *backpressure*?", a resposta está lá, não aqui. Aqui você decide *qual variante* adotar; lá você entende *como* o reativo funciona por dentro.

Quando faz sentido: time **já reativo**, ou cenário de **altíssima concorrência de I/O** onde o não-bloqueio rende a vazão que justifica o stack. É também a variante com o ecossistema mais maduro de *filters* e *predicates*, por ser a histórica.

### A variante MVC — servlet/bloqueante

O **Gateway Server WebMVC** é a variante **mais nova**, construída sobre o stack **Spring MVC (servlet)** e, portanto, **bloqueante**. *Starter*:

- **Atual (2025.x):** `spring-cloud-starter-gateway-server-webmvc`
- **Antigo:** `spring-cloud-starter-gateway-mvc`

A razão de existir é direta: **nem todo mundo quer o stack reativo**. Um time com aplicação MVC tradicional, *threads* por requisição e bibliotecas bloqueantes (JDBC, clientes HTTP síncronos) ganhava um peso desproporcional só para colocar um gateway na frente — tinha que aprender WebFlux, lidar com o event loop, vigiar bloqueios. A variante WebMVC remove esse imposto: o gateway roda no **mesmo modelo servlet** que o time já usa.

A contrapartida honesta é que você abre mão do não-bloqueio. Num gateway de pura intermediação de rede — onde I/O domina — o modelo bloqueante consome mais *threads* sob alta concorrência do que o reativo. Para muitos cenários, isso é perfeitamente aceitável; o ponto é que é uma **troca consciente**, não um detalhe.

Quando faz sentido: time **servlet/MVC** sem fluência reativa, projeto que **não quer** introduzir Netty/WebFlux, ou onde a simplicidade do *debug* síncrono vale mais do que o ganho de vazão do reativo.

### A renomeação dos starters — e quando cada um

No trem **2025.x**, os *starters* do gateway foram **renomeados** para deixar explícito que existem **duas variantes de servidor**. O esquema de nome velho não dizia qual stack você estava trazendo; o novo diz, no próprio artefato (`-server-webflux` vs `-server-webmvc`):

| Variante | Stack | Modelo | Starter atual (2025.x) | Starter antigo |
| --- | --- | --- | --- | --- |
| **Reativa** | WebFlux/Netty | não-bloqueante | `spring-cloud-starter-gateway-server-webflux` | `spring-cloud-starter-gateway` |
| **MVC** | Spring MVC (servlet) | bloqueante | `spring-cloud-starter-gateway-server-webmvc` | `spring-cloud-starter-gateway-mvc` |

O critério de escolha, em uma frase: **siga o stack do seu time.**

| Situação | Escolha |
| --- | --- |
| Aplicação/time **já reativo** (WebFlux) | **WebFlux** (`-server-webflux`) |
| **Altíssima concorrência de I/O**, vazão é o gargalo | **WebFlux** |
| Time **servlet/MVC tradicional**, sem fluência reativa | **WebMVC** (`-server-webmvc`) |
| **Não quer** introduzir Netty/WebFlux no projeto | **WebMVC** |
| *Debug* síncrono simples vale mais que vazão de I/O | **WebMVC** |

Não há uma variante "certa" universal. Há a variante **coerente com o resto da aplicação**. O pior dos mundos é misturar: gateway reativo num time que escreve tudo bloqueante (veja Armadilhas).

## Na prática

A mesma escolha — um gateway na frente de um `orders-service` — declarada nas duas variantes. **Você inclui apenas UMA** das dependências abaixo, conforme o stack do time.

Variante **reativa** (WebFlux/Netty):

```xml
<!-- VARIANTE REATIVA — sobre WebFlux/Netty (não-bloqueante) -->
<!-- Nome ATUAL (trem 2025.x). Antigo: spring-cloud-starter-gateway -->
<dependency>
    <groupId>org.springframework.cloud</groupId>
    <artifactId>spring-cloud-starter-gateway-server-webflux</artifactId>
</dependency>
```

Variante **MVC** (servlet/bloqueante):

```xml
<!-- VARIANTE MVC — sobre o stack servlet (bloqueante) -->
<!-- Nome ATUAL (trem 2025.x). Antigo: spring-cloud-starter-gateway-mvc -->
<dependency>
    <groupId>org.springframework.cloud</groupId>
    <artifactId>spring-cloud-starter-gateway-server-webmvc</artifactId>
</dependency>
```

O mesmo par no Gradle (Kotlin DSL), para deixar inequívoco que é **uma ou outra**:

```kotlin
// Escolha UMA. Não inclua as duas no mesmo módulo.

// --- Reativa (WebFlux/Netty) ---
implementation("org.springframework.cloud:spring-cloud-starter-gateway-server-webflux")

// --- MVC (servlet) ---
implementation("org.springframework.cloud:spring-cloud-starter-gateway-server-webmvc")
```

A configuração de rota em `application.yml` tem a mesma forma nas duas variantes — *predicates* e *filters* casam um caminho e encaminham para o serviço-alvo:

```yaml
spring:
  cloud:
    gateway:
      routes:
        - id: orders-route
          uri: http://orders-service
          predicates:
            - Path=/api/orders/**
          filters:
            - StripPrefix=1
```

O que **não** muda: o conceito de gateway, *predicates*, *filters* e roteamento — isso é a [[03-Dominios/Tecnologia/Java/Microservices e sistemas distribuídos/10 - API Gateway — papel, roteamento, predicates e filters|nota 10]]. O que muda é **o stack web por baixo**, decidido inteiramente pelo *starter* que você escolheu acima.

## Armadilhas

### (1) Usar o nome de starter antigo (pré-renomeação)

`spring-cloud-starter-gateway` e `spring-cloud-starter-gateway-mvc` são os nomes **antigos**, anteriores ao trem 2025.x. Tutoriais, respostas de Stack Overflow e snippets de 2023-2024 ainda os usam à vontade — e copiar de lá num projeto novo no trem 2025.x é o erro mais frequente desta nota. Os nomes atuais são `spring-cloud-starter-gateway-server-webflux` (reativo) e `spring-cloud-starter-gateway-server-webmvc` (MVC). Ao iniciar um projeto, confira o nome contra a **documentação da versão do seu trem**, não contra o primeiro blog que o Google trouxer.

### (2) Gateway reativo num time sem experiência WebFlux

Adotar a variante WebFlux "porque é a padrão dos tutoriais" num time que nunca escreveu código reativo é comprar uma dívida silenciosa. *Debug* reativo é diferente: stack traces longos e indiretos, *backpressure* a entender, event loop a respeitar. Tudo isso é território do [[03-Dominios/Tecnologia/Java/Programação Reativa/10 - Spring WebFlux — o stack não-bloqueante sobre Netty e o DispatcherHandler|Galho 11]] — e se o time não tem essa base, a variante **WebMVC** entrega o gateway **sem** o pedágio de aprendizado. Não escolha o stack reativo por inércia; escolha-o porque o time o domina ou porque a vazão de I/O o exige.

### (3) Misturar I/O bloqueante no gateway reativo

Se você **escolheu** a variante reativa, o compromisso é **não bloquear o event loop**. Um `Thread.sleep`, um acesso JDBC bloqueante, um cliente HTTP síncrono ou qualquer chamada bloqueante dentro de um *filter* trava a *thread* do Netty — e como pouquíssimas *threads* atendem toda a carga, um único bloqueio derruba a vazão do gateway inteiro. É a contradição clássica: você pagou o preço do stack reativo e, ao injetar código bloqueante, perde justamente o benefício pelo qual pagou. O *como* não-bloquear corretamente é assunto do Galho 11; o alerta aqui é que **escolher WebFlux é assumir essa disciplina** — se o time não vai segui-la, a variante MVC é mais honesta.

## Em entrevista

### Frase pronta (inglês)

> "Spring Cloud Gateway actually ships in two live server variants today, and you pick one at the dependency level. The reactive one — `spring-cloud-starter-gateway-server-webflux` — runs on the WebFlux/Netty stack and is non-blocking; it's the original gateway. The newer one — `spring-cloud-starter-gateway-server-webmvc` — runs on the servlet stack and is blocking, and it exists for teams that don't want to pull the whole reactive runtime in just to have a gateway. Both starters were renamed in the 2025.x release train: the reactive one used to be `spring-cloud-starter-gateway` and the MVC one used to be `spring-cloud-starter-gateway-mvc`, so a lot of older tutorials still show the old names. My rule is simple: if the team is already reactive or I'm in a high-concurrency I/O scenario, I go WebFlux; if it's a traditional servlet/MVC team with no reactive fluency, I go WebMVC — because dropping blocking I/O into a reactive event loop is the fastest way to throw away the benefit I paid for."

### Vocabulário

| Português | Inglês |
| --- | --- |
| não-bloqueante | non-blocking |
| servlet | servlet |
| reativo | reactive |
| contrapressão | backpressure |
| iniciador (de dependência) | starter |
| tempo de execução | runtime |
| laço de eventos | event loop |
| trem de release | release train |

## Veja também

- [[03-Dominios/Tecnologia/Java/Microservices e sistemas distribuídos/10 - API Gateway — papel, roteamento, predicates e filters|API Gateway (papel e roteamento)]] — o conceito de gateway, predicates e filters que vale para as duas variantes
- [[03-Dominios/Tecnologia/Java/Programação Reativa/10 - Spring WebFlux — o stack não-bloqueante sobre Netty e o DispatcherHandler|Spring WebFlux (Galho 11)]] — fronteira: o modelo reativo (Netty, event loop, backpressure) sobre o qual a variante WebFlux assenta (não re-explicado aqui)
- [[03-Dominios/Tecnologia/Java/Microservices e sistemas distribuídos/index|Microservices e sistemas distribuídos (MOC do galho)]]
- [[03-Dominios/Tecnologia/Java/index|Trilha Java]]

## Referências

- *Spring Cloud Gateway Server WebFlux — Starter*. docs.spring.io/spring-cloud-gateway/reference/spring-cloud-gateway-server-webflux/starter.html — artefato `spring-cloud-starter-gateway-server-webflux`; gateway reativo exige o runtime Netty (Spring Boot + WebFlux), não roda em container servlet nem como WAR. (acesso 2026-06-12)
- *Spring Cloud Gateway Server Web MVC — Starter*. docs.spring.io/spring-cloud-gateway/reference/spring-cloud-gateway-server-webmvc/starter.html — artefato `spring-cloud-starter-gateway-server-webmvc`; variante sobre o stack servlet, para quem não quer o stack reativo. (acesso 2026-06-12)
- *Spring Cloud Gateway — Reference (5.0.x)*. docs.spring.io/spring-cloud-gateway/reference — as duas variantes de servidor (WebFlux e Web MVC) e seus stacks. (acesso 2026-06-12)
