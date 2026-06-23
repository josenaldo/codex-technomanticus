---
title: "O que é programação reativa — o modelo push, assíncrono e não-bloqueante"
created: 2026-06-10
updated: 2026-06-10
type: concept
progress: backlog
status: seedling
publish: true
fase: iniciado
tags:
  - java
  - reativa
  - iniciado
  - reactor
aliases:
  - "programação reativa"
  - "reactive programming"
  - "modelo não-bloqueante"
---

# O que é programação reativa — o modelo push, assíncrono e não-bloqueante

> [!abstract] TL;DR
> Programação reativa é um paradigma **assíncrono** em que os dados fluem como um **stream** que *empurra* (push) eventos para quem reage, em vez de você *puxar* (pull) cada valor. O ganho prático é escala **I/O-bound**: poucos threads servem muitas conexões que estão só esperando, porque nenhum thread fica **bloqueado** parado. Importa na entrevista porque a pergunta clássica é "o que é reativo e quando faz sentido" — e a resposta certa é "throughput e uso de recursos sob alta concorrência", não "deixa cada request mais rápido".

## O que é

Programação reativa é, na definição do Project Reactor, "um paradigma de programação assíncrona concernido a streams de dados e à propagação de mudança". Três eixos definem o modelo, e os três se opõem ao estilo imperativo tradicional:

- **Push vs pull** — No modelo *pull* (o `Iterator` clássico), **você** decide quando chamar `next()` e puxar o próximo valor. No modelo *push* (o par `Publisher`/`Subscriber`), é o `Publisher` que **notifica** o `Subscriber` dos novos valores *à medida que eles chegam* ("as they come"). Quem controla o fluxo é a fonte, não o consumidor.
- **Assíncrono vs síncrono** — No síncrono, a chamada não retorna até o resultado estar pronto. No assíncrono, você registra o que fazer *quando* o resultado chegar e libera o fluxo de execução enquanto isso.
- **Não-bloqueante vs bloqueante** — Bloquear é manter um thread parado esperando um I/O (rede, banco, disco) terminar. Não-bloqueante é nunca prender um thread numa espera: ele é devolvido ao pool e volta ao trabalho quando o dado chega.

A peça que costura tudo é tratar **dados como um fluxo** ("data as a flow") de eventos manipulado por um vocabulário rico de operadores — em vez de um valor isolado que você obtém e processa linha a linha.

## Por que importa

O caso de uso onde reativo brilha é **I/O-bound**: aplicações que passam a maior parte do tempo *esperando* por sistemas externos (chamadas HTTP, queries de banco, filas), não calculando.

No modelo bloqueante, cada conexão em espera prende um thread. Como diz a doc do Reactor, "threads (possivelmente muitos threads) ficam ociosos, esperando por dados". Threads são um recurso caro e limitado; com mil conexões esperando, você precisa de mil threads parados — e o servidor satura não por estar trabalhando, mas por estar *esperando*.

O modelo não-bloqueante inverte isso: quando um fluxo vai esperar I/O, "você deixa a execução trocar para outra tarefa ativa que usa os mesmos recursos subjacentes, e depois volta ao processo atual quando o processamento assíncrono terminar". Poucos threads passam a servir muitas conexões, porque nenhum fica preso na espera.

Em entrevista isso vira a pergunta direta: *o que é reativo e quando faz sentido?* A resposta de sênior não é "é mais rápido" — é "**maximiza throughput e uso de recursos** sob alta concorrência I/O-bound".

## Como funciona

### Push vs pull: quem controla o fluxo

A diferença não é detalhe de API, é quem dirige. No `Iterator` (pull), o consumidor está no comando: ele puxa um item, processa, puxa o próximo. Se a fonte é lenta, o consumidor bloqueia esperando.

No `Publisher`/`Subscriber` (push), a fonte está no comando: ela emite eventos e o subscriber *reage*. Mas há um contrapeso — o **backpressure**. O subscriber pode sinalizar quanto consegue processar (`request(n)`: "me mande no máximo n elementos"), o que permite ao consumidor "sinalizar ao produtor que a taxa de emissão está alta demais". Isso transforma o modelo num **híbrido push-pull**: a fonte empurra, mas dentro do limite que o consumidor pediu — evitando que um produtor rápido afogue um consumidor lento.

### Não-bloqueante: por que poucos threads servem muitas conexões

Pense em um garçom (thread) e mesas (conexões). No modelo bloqueante, o garçom anota o pedido e fica *parado ao lado da mesa* até a comida ficar pronta na cozinha (o I/O). Com 20 mesas esperando, você precisa de 20 garçons parados.

No modelo não-bloqueante, o garçom anota, manda pra cozinha e vai atender outra mesa; quando a comida fica pronta, ele é avisado e volta para servir. Um punhado de garçons atende um salão inteiro — porque ninguém fica parado esperando a cozinha.

Essa é a razão de o reativo casar com cargas I/O-bound: a maior parte do tempo é *espera*, e não-bloqueante é justamente nunca pagar um thread para esperar.

### Reativo ≠ mais rápido: é throughput/recursos, não latência por request

Este é o ponto que separa quem entendeu de quem decorou. Reativo **não** torna uma request individual mais rápida — uma query de banco que leva 50 ms continua levando 50 ms, reativa ou não. A latência *por request* não melhora (pode até piorar um tiquinho, pelo overhead de composição).

O que muda é o **agregado**: com os mesmos poucos threads, o sistema sustenta muito mais requests *concorrentes* sem saturar, porque os threads não ficam presos esperando. O ganho está em **throughput** e **uso de recursos**, não em latência individual. Trocar "reativo é rápido" por "reativo escala melhor sob concorrência I/O-bound" é a correção que entrevistador procura.

### A quádrupla fronteira: threads, web, persistência, container

Esta nota é a *assinatura* do galho porque programação reativa toca quatro fronteiras que já têm casa em outras trilhas — e o erro comum é re-explicar todas aqui:

- **Threads (Galho 4)** — O "modelo de threads" que sustenta o não-bloqueante (event loop, e a alternativa moderna dos Virtual Threads / Loom) é assunto do Galho 4. Aqui só usamos o conceito; o aprofundamento está lá. Veja [[03-Dominios/Tecnologia/Java/Concorrência e paralelismo/12 - Virtual Threads e Project Loom|Virtual Threads e Project Loom]].
- **Web (Galho 9)** — O stack web *imperativo* (Spring MVC, um thread por request) é o contraponto do reativo na camada web. Está no Galho 9: [[03-Dominios/Tecnologia/Java/Web e APIs REST/01 - O que é Spring MVC — a camada web sobre o container|O que é Spring MVC]].
- **Persistência (Galho 10)** — A persistência *bloqueante* (JDBC/JPA tradicional) é o que mais ameaça quebrar uma cadeia reativa: basta um driver bloqueante para prender um thread do event loop. O contraste com drivers reativos é tema do Galho 10.
- **Container (Galho 8)** — O ciclo de vida e o container Spring onde tudo isso é orquestrado é assunto do Galho 8.

Guardar esse mapa evita o erro de tratar reativo como uma coisa isolada: ele é uma *reorganização* de quatro camadas que você já conhece.

## Na prática

A diferença de **modelo** aparece já na assinatura de um endpoint. Compare retornar uma coleção materializada com retornar um stream reativo:

```java
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RestController;
import reactor.core.publisher.Flux;
import reactor.core.publisher.Mono;

import java.util.List;

@RestController
public class OrderController {

    private final OrderRepository orders;

    public OrderController(OrderRepository orders) {
        this.orders = orders;
    }

    // Imperativo (pull): o método só retorna quando a List inteira
    // estiver materializada em memória. Enquanto o banco responde,
    // o thread que serve esta request fica BLOQUEADO esperando.
    @GetMapping("/orders/blocking")
    public List<Order> listBlocking() {
        return orders.findAllBlocking();
    }

    // Reativo (push): retorna um Flux<Order> — uma "promessa" de 0..N
    // Orders que serão EMPURRADAS conforme chegam. O thread não
    // bloqueia: ele é liberado e os elementos fluem ao subscriber.
    @GetMapping("/orders/reactive")
    public Flux<Order> listReactive() {
        return orders.findAll();
    }

    // Mono<T> é o caso de 0..1: uma promessa de no máximo um valor.
    @GetMapping("/orders/{id}")
    public Mono<Order> getOne(String id) {
        return orders.findById(id);
    }
}
```

Os dois tipos centrais do Reactor:

```text
Mono<T>  →  publisher de 0 ou 1 elemento   (ex.: buscar um Order por id)
Flux<T>  →  publisher de 0 a N elementos    (ex.: stream de Orders)
```

Repare: nada aqui *executa* a busca quando o método retorna. `Flux` e `Mono` são **descrições** do que acontecerá quando alguém se inscrever (subscribe) — e o framework web é quem se inscreve. Por isso o thread não fica preso: ele monta a receita e segue. O detalhamento de `Mono`/`Flux` e do WebFlux é de outras notas; aqui o foco é o *modelo*.

## Armadilhas

### (1) Achar que "reativo = mais rápido"

A intuição errada mais comum: trocar para reativo porque "fica mais rápido". Não fica — a latência de uma request individual não melhora; o gargalo I/O (os 50 ms do banco) continua lá. Quem mede uma única chamada em ambiente sem carga frequentemente vê a versão reativa *empatando ou perdendo*, e conclui (errado) que não vale a pena.

Exemplo: você migra um endpoint para `Flux` e cronometra um `curl` solitário — vê o mesmo tempo de antes e fica confuso.

**Fix:** meça sob **concorrência** (milhares de conexões simultâneas) e olhe **throughput e threads usados**, não latência de uma request.

### (2) Achar que "reativo = só assíncrono"

Outro reducionismo: "reativo é só rodar coisas async". Assincronicidade é parte, mas reativo é *mais*: tem **backpressure** (o consumidor regula a vazão da fonte via `request(n)`, evitando ser afogado) e **composição declarativa** (encadear operadores sobre o fluxo em vez de gerenciar callbacks à mão). Um `ExecutorService` disparando tarefas é assíncrono, mas não é reativo — não há fluxo de dados com controle de pressão nem o vocabulário de operadores.

Exemplo: alguém envolve chamadas em `CompletableFuture` e diz "agora é reativo" — mas se um produtor rápido pode estourar a memória de um consumidor lento, falta o que define o modelo.

**Fix:** trate reativo como o tripé *stream + backpressure + composição declarativa*, não como sinônimo de async.

## Em entrevista

### Frase pronta (inglês)

> Reactive programming is an asynchronous, non-blocking, push-based model where data flows as a stream and the publisher pushes events to subscribers as they come, with backpressure letting the consumer signal how much it can handle. The key trade-off to be clear about is that it does **not** make an individual request faster — per-request latency is roughly the same; what it buys you is **throughput and resource utilization** under high concurrency, because a small number of threads can serve many connections that are only waiting on I/O instead of blocking one thread per request. So my decision rule is to reach for it on **I/O-bound, high-concurrency** workloads, and the caveat is that it only pays off end-to-end if the whole chain stays non-blocking — a single blocking JDBC driver in the path defeats the purpose.

### Vocabulário

| Termo PT | Termo EN |
| --- | --- |
| modelo de empurrar (push) | push-based model |
| não-bloqueante | non-blocking |
| contrapressão | backpressure |
| fluxo de dados / stream | data stream |
| vazão | throughput |
| uso de recursos | resource utilization |
| limitado por I/O | I/O-bound |
| assinante / publicador | subscriber / publisher |

## Veja também

- [[03-Dominios/Tecnologia/Java/Programação Reativa/02 - Reactive Streams — a spec das 4 interfaces e o Flow do Java 9|Reactive Streams]]
- [[03-Dominios/Tecnologia/Java/Programação Reativa/03 - Mono e Flux — os publishers do Project Reactor|Mono e Flux]]
- [[03-Dominios/Tecnologia/Java/Concorrência e paralelismo/12 - Virtual Threads e Project Loom|Virtual Threads e Project Loom]] — o modelo de threads (Galho 4)
- [[03-Dominios/Tecnologia/Java/Web e APIs REST/01 - O que é Spring MVC — a camada web sobre o container|O que é Spring MVC]] — o stack imperativo (Galho 9)
- [[03-Dominios/Tecnologia/Java/Programação Reativa/index|Programação Reativa (MOC do galho)]]
- [[03-Dominios/Tecnologia/Java/index|Trilha Java]]
- [[03-Dominios/Tecnologia/Java/Dicionário de Java|Dicionário de Java]]

## Referências

- Project Reactor — *Reactive Programming* (Reference Guide): https://projectreactor.io/docs/core/release/reference/reactiveProgramming.html
- Project Reactor — *Reference Guide* (intro): https://projectreactor.io/docs/core/release/reference/
- Reactive Streams — *An initiative to provide a standard for asynchronous stream processing with non-blocking back pressure*: https://www.reactive-streams.org/
