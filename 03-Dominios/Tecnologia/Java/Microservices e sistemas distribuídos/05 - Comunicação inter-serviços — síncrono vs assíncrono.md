---
title: "Comunicação inter-serviços — síncrono vs assíncrono"
created: 2026-06-12
updated: 2026-06-12
type: concept
status: seedling
publish: true
fase: iniciado
tags:
  - java
  - microservices
  - iniciado
  - arquitetura
aliases:
  - "Comunicação inter-serviços"
  - "Síncrono vs assíncrono"
---

# Comunicação inter-serviços — síncrono vs assíncrono

> [!abstract] TL;DR
> Quando você quebra um monolito em serviços, a chamada de método que antes acontecia *dentro do processo* vira uma chamada *pela rede*. E a rede falha, atrasa e some. A pergunta central de toda arquitetura de microsserviços é: **esse serviço deveria esperar a resposta do outro (síncrono) ou apenas avisar que algo aconteceu e seguir em frente (assíncrono)?**
> - **Síncrono** (REST, `@HttpExchange`/Feign, gRPC): request/response, simples de raciocinar, mas cria **acoplamento temporal** — se o serviço de baixo cai, o de cima cai junto (falha em cascata).
> - **Assíncrono** (eventos/mensageria): o emissor publica e não espera; **desacopla**, é resiliente, mas paga o preço da **consistência eventual**.
> Não existe "o melhor" — existe o **eixo de decisão**. Você escolhe por caso de uso.

## O que é

Num monolito, quando o módulo de pedidos precisa cobrar um cartão, ele chama um método: `pagamentoService.cobrar(...)`. A chamada é local, instantânea, e ou retorna ou lança exceção. Não há rede no meio.

Quando você separa "pedidos" e "pagamentos" em **dois serviços independentes**, essa chamada de método deixa de existir. Para um serviço pedir algo ao outro, agora ele precisa atravessar a **rede** — e a rede é um meio hostil: tem latência, pode estar congestionada, o serviço do outro lado pode estar reiniciando, ou simplesmente fora do ar.

> [!info] A metáfora de Fowler: *smart endpoints and dumb pipes*
> Martin Fowler descreve o estilo de comunicação de microsserviços como **"smart endpoints and dumb pipes"** (pontas inteligentes, canos burros): a inteligência mora nos serviços, não na infraestrutura de comunicação. O "cano" — seja HTTP ou um broker de mensagens — só transporta. Isso se opõe aos *Enterprise Service Bus* (ESB) do passado, que enfiavam regra de negócio na camada de transporte.

A **Comunicação inter-serviços** é, então, o conjunto de decisões sobre *como* esses serviços conversam pela rede. E a primeira bifurcação — a mais importante — é entre **síncrono** e **assíncrono**.

## Por que importa

Essa escolha não é um detalhe técnico de implementação. Ela **define o comportamento de falha do seu sistema inteiro**.

Pense assim: se você liga para alguém e fica no telefone esperando a resposta, vocês dois ficam *presos* àquela ligação. Se a outra pessoa não atende, você fica parado, segurando o fone. Isso é **síncrono**. Agora, se você manda uma mensagem e volta a fazer outras coisas, vocês estão **desacoplados no tempo** — a pessoa responde quando puder. Isso é **assíncrono**.

Fowler é direto sobre o risco do síncrono: *"any time you have a number of synchronous calls between services you will encounter the multiplicative effect of downtime"* — toda vez que você encadeia chamadas síncronas, as indisponibilidades **se multiplicam**. Três serviços com 99,9% de uptime cada, encadeados síncronamente, não te dão 99,9% — te dão algo pior, porque qualquer um deles derrubando *derruba a cadeia toda*.

Saber escolher o eixo certo é o que separa um sistema distribuído resiliente de uma casa de cartas que cai quando um único serviço espirra.

## Como funciona

### Síncrono — request/response e acoplamento temporal

No modelo síncrono, o serviço **A** faz uma requisição ao serviço **B** e **bloqueia esperando a resposta** antes de continuar. É o velho request/response da web.

Em Java/Spring, isso aparece como:
- **REST sobre HTTP** com um cliente declarativo: `@HttpExchange` (HTTP Interface, nativo do Spring 6) ou **OpenFeign** — você descreve a chamada como uma interface e o framework gera o cliente.
- **gRPC** — RPC binário sobre HTTP/2, mais rápido e fortemente tipado que REST. *(Aprofundado no Galho 14 — Mensageria; ver [[03-Dominios/Tecnologia/Java/Mensageria/28 - gRPC em Java — RPC síncrono sobre HTTP_2|gRPC]]. Aqui só importa que gRPC, apesar do nome "mensageria", é tipicamente um modelo síncrono request/response.)*

A vantagem é a **simplicidade de raciocínio**: você chama, espera, e tem a resposta na mão para usar na linha seguinte. O fluxo é linear, fácil de debugar, fácil de testar.

A armadilha é o **acoplamento temporal** (*temporal coupling*): A e B precisam estar **vivos ao mesmo tempo** para a operação funcionar. Se B está fora do ar, A não tem o que fazer a não ser falhar (ou esperar, o que muitas vezes é pior). E quando A falha porque B falhou, e C dependia de A... você tem uma **falha em cascata** (*cascading failure*).

### Assíncrono — eventos, desacoplamento e consistência eventual

No modelo assíncrono, o serviço **A** **não chama** o serviço **B**. Em vez disso, A **publica um evento** ("Pedido foi criado") num broker de mensagens (Kafka, RabbitMQ) e **segue em frente imediatamente**, sem esperar ninguém. Quem se interessar pelo evento — B, C, ou um serviço que nem existe ainda — **consome** quando puder.

> [!info] A inversão fundamental
> No síncrono, A *sabe* quem é B e *manda* B fazer algo ("cobre esse cartão, agora, e me diga se deu certo").
> No assíncrono, A apenas *anuncia um fato* ("este pedido foi criado") e **não sabe nem se importa** quem vai reagir. O conhecimento sobre "quem faz o quê" sai do emissor.

A vantagem é o **desacoplamento temporal**: B pode estar fora do ar quando o evento é publicado. A mensagem fica no broker, esperando. Quando B volta, ele processa a fila acumulada. A nunca soube que B estava offline, e nunca parou por isso. Fowler resume a receita: *"make your calls asynchronous"* como forma de gerenciar o downtime.

O preço é a **consistência eventual** (*eventual consistency*): logo depois que A publica "Pedido criado", o pagamento **ainda não foi processado**. Existe uma janela de tempo em que o sistema está num estado "intermediário", e seu código (e seu produto) precisam tolerar isso. "Eventualmente" tudo se acerta — mas não *instantaneamente*.

> [!warning] Fronteira de galho
> Como **coordenar uma transação de negócio** que atravessa vários serviços assíncronos (ex.: criar pedido → reservar estoque → cobrar pagamento, com rollback se algo falha) é o padrão **Saga**, e isso é assunto do **Galho 14 — Mensageria**. Esta nota só estabelece o *eixo de decisão* síncrono/assíncrono. O *como* do event-driven (Saga, outbox, event sourcing) **não é re-explicado aqui** — ver [[03-Dominios/Tecnologia/Java/Mensageria/22 - Saga — transações distribuídas por eventos|Saga]].

### O eixo de decisão — quando cada um

Não escolha por modismo. Escolha pela **natureza da operação**:

| Use **síncrono** quando… | Use **assíncrono** quando… |
| --- | --- |
| Você precisa da resposta *agora* para continuar (ex.: validar saldo antes de confirmar a compra). | A operação pode acontecer "em segundo plano" (ex.: enviar e-mail de confirmação, atualizar relatório). |
| A consistência forte é obrigatória no momento da resposta. | Consistência eventual é aceitável pelo negócio. |
| O fluxo é uma **consulta** (leitura) que retorna dados. | O fluxo é uma **notificação de fato** ("isto aconteceu"). |
| Há poucos saltos e o acoplamento temporal é tolerável. | Você quer desacoplar, resistir a quedas e escalar consumidores independentemente. |

Regra de bolso: **leitura/consulta tende a síncrono; reação a eventos de negócio tende a assíncrono.** E a maioria dos sistemas reais é **híbrida** — usa os dois, cada um onde faz sentido.

## Na prática

O mesmo cenário — `order-service` precisa que `payment-service` cobre um pagamento — resolvido nos dois eixos:

```text
SÍNCRONO (request/response — acoplamento temporal)

  order-service                          payment-service
       |                                       |
       |  POST /payments  (HTTP/gRPC)          |
       |-------------------------------------->|
       |                                       | processa...
       |          200 OK { status: paid }      |
       |<--------------------------------------|
       |                                       |
   (BLOQUEADO esperando)            se payment-service cai aqui,
                                    order-service FALHA junto
                                    -> falha em cascata


ASSÍNCRONO (evento — desacoplamento temporal)

  order-service        message broker         payment-service
       |                    |                       |
       | publish            |                       |
       | "OrderCreated" --->|                       |
       |  (segue em frente) |                       |
       |                    |---- entrega --------->| processa...
       |                    |                       |
       |                    |<-- "PaymentDone" -----|
       |                    |                       |
  order-service NUNCA       se payment-service está fora,
  ficou bloqueado;          a mensagem ESPERA na fila e é
  reage ao evento de        entregue quando ele voltar
  volta quando chega        -> sem cascata
```

No síncrono, os dois serviços compartilham o mesmo instante. No assíncrono, o broker (o "cano burro") absorve a diferença de tempo entre quem produz e quem consome.

## Armadilhas

### (1) Fazer tudo síncrono "porque é mais simples"

É a armadilha mais comum, e a mais cara. REST síncrono é fácil de começar, então times saem encadeando chamada após chamada: o serviço A chama B, que chama C, que chama D — tudo bloqueante. Funciona lindamente no ambiente de dev, com tudo no ar.

Em produção, isso vira o **efeito multiplicativo do downtime** que Fowler alerta. Cada salto adiciona latência (você espera A+B+C+D somados) e cada serviço vira um **ponto único de falha para toda a corrente**. D piscou? A operação inteira morre. Você construiu um monolito distribuído — com todo o acoplamento do monolito *mais* a fragilidade da rede. O acoplamento temporal te pega de surpresa só quando algo cai.

### (2) Fazer assíncrono onde uma chamada simples bastava

O oposto também dói. Eventos e mensageria são poderosos, mas trazem **complexidade real**: broker para operar, consistência eventual para o produto tolerar, ordenação de mensagens, idempotência, rastreamento distribuído de um fluxo que não é mais linear. Debugar "por que esse pedido não foi cobrado" num fluxo de 5 eventos é muito mais difícil do que ler um stacktrace de uma chamada síncrona.

Se a operação é uma **consulta que precisa da resposta imediata** — "qual o saldo deste cliente?" — transformar isso em evento é over-engineering. Você paga toda a complexidade do assíncrono para resolver um problema que uma chamada request/response resolveria em uma linha. **Async não é "mais moderno"; é uma troca.** Use quando o desacoplamento vale o custo, não por reflexo.

### (3) Ignorar que síncrono *precisa* de rede de proteção

Mesmo quando síncrono é a escolha certa, ele não pode ser "ingênuo". Uma chamada HTTP sem **timeout** fica pendurada esperando para sempre quando o outro lado trava — e segura recursos (threads, conexões) até esgotar. Sem **retry**, **circuit breaker** e **fallback**, uma chamada síncrona é uma cascata esperando para acontecer. *(Esses padrões de resiliência são o foco do resto deste Galho 16 — ver [[03-Dominios/Tecnologia/Java/Microservices e sistemas distribuídos/21 - Os padrões de falha distribuída|Padrões de falha distribuída]].)*

## Em entrevista

### Frase pronta (inglês)

> "The core decision in inter-service communication is synchronous versus asynchronous. Synchronous request-response — REST, HTTP interfaces, or gRPC — is simple to reason about, but it creates temporal coupling: the caller and the callee must both be alive at the same time, and chained synchronous calls multiply downtime, leading to cascading failures. Asynchronous, event-driven communication decouples services in time through a message broker, which makes the system far more resilient, but the trade-off is eventual consistency. There's no universally correct answer — I pick per use case: synchronous when I need the response immediately to proceed, asynchronous when I'm reacting to a business fact and can tolerate eventual consistency. Most real systems are hybrid, and even synchronous calls need timeouts, retries, and circuit breakers to avoid becoming cascading failures."

### Vocabulário

- **síncrono** — *synchronous*
- **assíncrono** — *asynchronous*
- **acoplamento temporal** — *temporal coupling*
- **orientado a eventos** — *event-driven*
- **falha em cascata** — *cascading failure*
- **requisição-resposta** — *request-response*
- **consistência eventual** — *eventual consistency*
- **desacoplamento** — *decoupling / loose coupling*
- **corretor de mensagens / broker** — *message broker*

## Veja também

- [[03-Dominios/Tecnologia/Java/Microservices e sistemas distribuídos/09 - Comunicação síncrona — OpenFeign e HTTP Interface|Comunicação síncrona]] — o lado síncrono aprofundado neste galho
- [[03-Dominios/Tecnologia/Java/Microservices e sistemas distribuídos/21 - Os padrões de falha distribuída|Padrões de falha distribuída]] — timeout, retry, circuit breaker (a rede de proteção do síncrono)
- [[03-Dominios/Tecnologia/Java/Mensageria/22 - Saga — transações distribuídas por eventos|Saga (Galho 14)]] — fronteira: como coordenar transações assíncronas
- [[03-Dominios/Tecnologia/Java/Mensageria/28 - gRPC em Java — RPC síncrono sobre HTTP_2|gRPC (Galho 14)]] — fronteira: RPC síncrono tipado sobre HTTP/2
- [[03-Dominios/Tecnologia/Java/Microservices e sistemas distribuídos/index|Microservices e sistemas distribuídos (MOC do galho)]]
- [[03-Dominios/Tecnologia/Java/index|Trilha Java]]

## Referências

- Lewis, James; Fowler, Martin. *Microservices* — martinfowler.com. https://martinfowler.com/articles/microservices.html — seções *Smart endpoints and dumb pipes*, *Decentralized Governance*, *Decentralized Data Management* e o alerta *"Synchronous calls considered harmful"* / efeito multiplicativo do downtime.
