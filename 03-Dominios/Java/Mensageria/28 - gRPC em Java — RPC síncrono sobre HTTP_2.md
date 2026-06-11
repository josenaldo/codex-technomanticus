---
title: "gRPC em Java — RPC síncrono sobre HTTP/2"
fase: magus
tags:
  - java
  - mensageria
  - magus
  - grpc
  - protobuf
created: 2026-06-11
updated: 2026-06-11
type: concept
status: seedling
publish: true
aliases:
  - "gRPC"
---

# gRPC em Java — RPC síncrono sobre HTTP/2

> [!abstract] TL;DR
> gRPC é um framework de **RPC (Remote Procedure Call)** que faz uma chamada remota parecer uma chamada de função local. Roda sobre **HTTP/2** e usa **Protocol Buffers** como IDL e formato de serialização. Você escreve um `service` no `.proto`, o `protoc` gera os _stubs_ Java (cliente e servidor), e você implementa/chama métodos tipados. Suporta **quatro tipos de chamada**: _unary_, _server-streaming_, _client-streaming_ e _bidirectional-streaming_. O ponto cego: gRPC é **acoplado no tempo** — cliente e servidor precisam estar vivos ao mesmo tempo. Ele resolve comunicação síncrona ponto-a-ponto, **não** desacoplamento como mensageria faz. Em Java, a porta de entrada é `grpc-java` (e o `grpc-spring-boot-starter` para integrar com Spring Boot).

## O que é

gRPC é o framework de RPC mantido pela CNCF que faz uma chamada de rede parecer uma chamada de método local. A ideia de RPC é antiga (CORBA, Java RMI, SOAP), mas o gRPC moderniza o pacote: **HTTP/2** no transporte, **Protocol Buffers** no contrato e na serialização, e geração de código para múltiplas linguagens a partir de um único `.proto`.

O fluxo conceitual é direto:

1. Você define um `service` com seus métodos (RPCs) e as mensagens de request/response num arquivo `.proto`.
2. O compilador `protoc`, com o plugin do gRPC, gera **stubs** — interfaces tipadas. No cliente, o stub é um objeto local que espelha os métodos do serviço; chamar um método dele dispara a serialização do request em Protobuf, o envio sobre HTTP/2 e a desserialização da resposta. No servidor, é gerada uma classe base que você estende para implementar a lógica.
3. Cliente e servidor compartilham o mesmo `.proto` — o contrato é a fonte da verdade.

> [!info] RPC, não mensageria
> A palavra-chave aqui é **chamada**. Você chama `orderService.getOrder(req)` e espera a resposta — exatamente como uma função. Não há fila, não há broker, não há "publicar e esquecer". É comunicação **request/response síncrona** entre dois serviços que se conhecem.

## Por que importa

Num galho sobre **mensageria**, gRPC entra como o **contraponto síncrono**. Boa parte das decisões de arquitetura distribuída se resume a uma pergunta: *"esta comunicação precisa de resposta agora, ou pode ser desacoplada no tempo?"*

- Quando a resposta é necessária **imediatamente** e o chamador não tem o que fazer sem ela (ex.: um `BFF` consultando o serviço de catálogo para montar uma tela), RPC síncrono é a escolha natural. gRPC é a opção performática para esse caso: binário, multiplexado, com contrato forte.
- Quando o produtor **não precisa** da resposta e o consumidor pode processar depois (ex.: "pedido criado" → atualizar estoque, enviar e-mail, faturar), mensageria desacopla e dá resiliência.

Saber gRPC importa porque ele é o RPC dominante para comunicação **interna** entre microsserviços na JVM, e porque entender suas garantias (e seus acoplamentos) é o que te permite **não** usá-lo onde uma fila seria melhor. Em entrevista de sistema distribuído, contrastar "gRPC vs Kafka" é quase obrigatório — e mostra maturidade arquitetural.

## Como funciona

### Os 4 tipos de chamada

O `.proto` declara o **modo** de cada RPC pela presença (ou ausência) da keyword `stream` no request e/ou no response. São quatro combinações:

| Tipo | Request | Response | Analogia |
| --- | --- | --- | --- |
| **Unary** | 1 mensagem | 1 mensagem | Função normal: pede e recebe |
| **Server-streaming** | 1 mensagem | stream | Cliente pede; servidor responde aos poucos (ex.: paginação/feed) |
| **Client-streaming** | stream | 1 mensagem | Cliente envia uma sequência; servidor consolida e responde uma vez (ex.: upload) |
| **Bidirectional-streaming** | stream | stream | Dois fluxos independentes na mesma conexão (ex.: chat, telemetria) |

- **Unary**: o cliente envia um único request e recebe um único response, como uma chamada de função comum. É o modo mais usado.
- **Server-streaming**: o cliente envia um request e recebe um **stream** de mensagens de volta, lendo a sequência até o servidor sinalizar o fim.
- **Client-streaming**: o cliente escreve uma **sequência** de mensagens e as envia; o servidor responde com **uma única** mensagem (tipicamente após consumir todo o stream).
- **Bidirectional-streaming**: ambos os lados enviam sequências por um stream de leitura/escrita, e os dois streams operam **independentemente** — a ordem é por seu próprio fluxo.

> [!tip] Regra de bolso
> Comece sempre com **unary**. Os modos de streaming são poderosos, mas pagam em complexidade (backpressure, fim de stream, cancelamento). Use streaming só quando o problema é genuinamente um fluxo.

### HTTP/2 e stubs gerados

gRPC se apoia no **HTTP/2** como transporte. As propriedades do HTTP/2 que importam:

- **Multiplexação**: várias chamadas (streams) compartilham **uma única conexão TCP**, sem o _head-of-line blocking_ de conexões-por-request do HTTP/1.1. Isso é o que torna streaming bidirecional viável.
- **Frames binários** e **header compression** (HPACK): menos overhead que texto.
- **Conexões longevas**: o `Channel` do gRPC mantém a conexão aberta e a reaproveita.

A partir do `.proto`, o `protoc` (com o plugin gRPC, integrado via `protobuf-maven-plugin` no build) gera os stubs. Em `grpc-java`, o cliente recebe **mais de um sabor de stub** sobre o mesmo serviço:

- **Blocking stub** (`...BlockingStub`): a chamada **bloqueia** a thread até a resposta chegar. Simples, síncrono, ideal para unary. É o ponto de partida natural.
- **Async stub** (`...Stub`, o "future-less" baseado em `StreamObserver`): você passa um observer e recebe callbacks (`onNext`, `onError`, `onCompleted`). É o sabor obrigatório para os modos de streaming.
- (Há ainda o **future stub**, `...FutureStub`, que devolve `ListenableFuture` para unary assíncrono.)

> [!note] As três camadas do grpc-java
> O `grpc-java` se organiza em **Stub** (o que o dev usa, bindings tipados), **Channel** (abstração de conexão/roteamento) e **Transport** (HTTP/2 concreto, via Netty ou OkHttp). Você quase sempre só toca na camada Stub.

### gRPC vs REST vs mensageria

Três estilos, dois eixos. O eixo decisivo é **síncrono-RPC vs assíncrono-evento**.

| Dimensão | gRPC | REST (HTTP/JSON) | Mensageria (Kafka/Rabbit) |
| --- | --- | --- | --- |
| Estilo | RPC (chama método) | REST (manipula recurso) | Evento (publica fato) |
| Acoplamento temporal | **Acoplado** (ambos vivos) | **Acoplado** (ambos vivos) | **Desacoplado** (broker no meio) |
| Comunicação | Síncrona ponto-a-ponto | Síncrona ponto-a-ponto | Assíncrona, 1-para-N |
| Contrato | `.proto` (forte, binário) | OpenAPI (texto, frouxo) | Schema (Avro/Protobuf) no Registry |
| Transporte | HTTP/2 | HTTP/1.1+ | TCP do broker |
| Quem conhece quem | Cliente conhece servidor | Cliente conhece servidor | Produtor **não** conhece consumidores |

A leitura arquitetural:

- **gRPC e REST estão do mesmo lado** do eixo: ambos são **request/response síncrono e acoplado no tempo** — o chamador precisa que o chamado esteja no ar **agora**. gRPC é mais rápido e mais tipado; REST é mais ubíquo e amigável ao browser. Mas nenhum dos dois desacopla.
- **Mensageria está do outro lado**: o broker absorve a indisponibilidade do consumidor, permite fan-out 1-para-N e desacopla produtor de consumidor no tempo e no espaço. É o que gRPC **não** faz.

Conclusão prática: gRPC **não substitui** mensageria — resolve um problema diferente. Trocar uma fila por uma chamada gRPC "porque é mais rápido" reintroduz o acoplamento temporal que a fila existia para remover.

## Na prática

Tudo aqui é **Java** sobre `grpc-java`. Domínio neutro: um serviço de pedidos (`Order`).

Primeiro, o contrato no `.proto` — declarando um RPC **unary** e um **server-streaming**:

```protobuf
syntax = "proto3";

package order.v1;

option java_multiple_files = true;
option java_package = "com.exemplo.order.grpc";

service OrderService {
  // Unary: pede um pedido, recebe um pedido
  rpc GetOrder (GetOrderRequest) returns (Order);

  // Server-streaming: pede pedidos de um cliente, recebe um fluxo
  rpc ListOrders (ListOrdersRequest) returns (stream Order);
}

message GetOrderRequest {
  string order_id = 1;
}

message ListOrdersRequest {
  string customer_id = 1;
}

message Order {
  string order_id = 1;
  string customer_id = 2;
  int64 total_cents = 3;
}
```

O build gera os stubs via `protobuf-maven-plugin`. Dependências no `pom.xml`:

```xml
<dependencies>
  <dependency>
    <groupId>io.grpc</groupId>
    <artifactId>grpc-netty-shaded</artifactId>
    <version>1.66.0</version>
  </dependency>
  <dependency>
    <groupId>io.grpc</groupId>
    <artifactId>grpc-protobuf</artifactId>
    <version>1.66.0</version>
  </dependency>
  <dependency>
    <groupId>io.grpc</groupId>
    <artifactId>grpc-stub</artifactId>
    <version>1.66.0</version>
  </dependency>
</dependencies>

<build>
  <extensions>
    <extension>
      <groupId>kr.motd.maven</groupId>
      <artifactId>os-maven-plugin</artifactId>
      <version>1.7.1</version>
    </extension>
  </extensions>
  <plugins>
    <plugin>
      <groupId>org.xolstice.maven.plugins</groupId>
      <artifactId>protobuf-maven-plugin</artifactId>
      <version>0.6.1</version>
      <configuration>
        <protocArtifact>com.google.protobuf:protoc:3.25.1:exe:${os.detected.classifier}</protocArtifact>
        <pluginId>grpc-java</pluginId>
        <pluginArtifact>io.grpc:protoc-gen-grpc-java:1.66.0:exe:${os.detected.classifier}</pluginArtifact>
      </configuration>
      <executions>
        <execution>
          <goals>
            <goal>compile</goal>
            <goal>compile-custom</goal>
          </goals>
        </execution>
      </executions>
    </plugin>
  </plugins>
</build>
```

O **servidor** estende a classe base gerada (`OrderServiceImplBase`) e responde via `StreamObserver`:

```java
public class OrderServiceImpl extends OrderServiceGrpc.OrderServiceImplBase {

    @Override
    public void getOrder(GetOrderRequest request,
                         StreamObserver<Order> responseObserver) {
        Order order = Order.newBuilder()
                .setOrderId(request.getOrderId())
                .setCustomerId("cust-42")
                .setTotalCents(19990)
                .build();

        responseObserver.onNext(order);   // 1 resposta (unary)
        responseObserver.onCompleted();   // fim da chamada
    }

    @Override
    public void listOrders(ListOrdersRequest request,
                           StreamObserver<Order> responseObserver) {
        // Server-streaming: vários onNext, depois onCompleted
        for (int i = 1; i <= 3; i++) {
            responseObserver.onNext(Order.newBuilder()
                    .setOrderId("ord-" + i)
                    .setCustomerId(request.getCustomerId())
                    .setTotalCents(1000L * i)
                    .build());
        }
        responseObserver.onCompleted();
    }
}

// Subindo o servidor
Server server = ServerBuilder.forPort(9090)
        .addService(new OrderServiceImpl())
        .build()
        .start();
server.awaitTermination();
```

O **cliente** abre um `ManagedChannel` e usa o **blocking stub** para a chamada unary:

```java
ManagedChannel channel = ManagedChannelBuilder
        .forAddress("localhost", 9090)
        .usePlaintext()          // sem TLS — só em dev
        .build();

OrderServiceGrpc.OrderServiceBlockingStub stub =
        OrderServiceGrpc.newBlockingStub(channel);

// Unary: bloqueia até a resposta
Order order = stub.getOrder(GetOrderRequest.newBuilder()
        .setOrderId("ord-1")
        .build());
System.out.println(order.getTotalCents());

// Server-streaming: blocking stub devolve um Iterator
Iterator<Order> it = stub.listOrders(ListOrdersRequest.newBuilder()
        .setCustomerId("cust-42")
        .build());
it.forEachRemaining(o -> System.out.println(o.getOrderId()));

channel.shutdown();
```

Com **Spring Boot**, o `grpc-spring-boot-starter` reduz o cerimonial: o servidor vira um bean anotado com `@GrpcService`, e o cliente injeta o stub com `@GrpcClient` — o starter gerencia o `Server`, o `Channel` e o ciclo de vida junto do contexto Spring.

```java
@GrpcService
public class OrderServiceImpl extends OrderServiceGrpc.OrderServiceImplBase {
    // mesma implementação; o starter registra e expõe o serviço
}

@Service
public class OrderClient {

    @GrpcClient("order-service")
    private OrderServiceGrpc.OrderServiceBlockingStub stub;

    public long total(String id) {
        return stub.getOrder(GetOrderRequest.newBuilder()
                .setOrderId(id)
                .build()).getTotalCents();
    }
}
```

## Armadilhas

### (1) gRPC onde mensageria desacoplaria melhor

A armadilha-mãe. gRPC é **acoplado no tempo**: a chamada `stub.getOrder(...)` exige que o serviço-alvo esteja **no ar agora**. Se ele cai, sua chamada falha (ou fica retentando), e o erro se propaga de volta pela cadeia síncrona — um serviço lento derruba quem o chama (*cascading failure*). Usar gRPC para algo como "notificar que o pedido foi criado" recria exatamente o acoplamento que uma fila (Kafka/Rabbit) existiria para **remover**: com mensageria, o produtor publica o fato e segue a vida; o consumidor processa quando puder, mesmo que estivesse fora do ar. **Pergunte sempre**: o chamador precisa da resposta para continuar? Se não, é evento, não RPC.

### (2) Streaming sem necessidade real

Os modos de streaming são sedutores, mas pagam caro em complexidade: você passa a lidar com `StreamObserver`, fim de stream, cancelamento, backpressure e erros parciais no meio do fluxo. A maioria esmagadora das chamadas internas é **unary** — pede um, recebe um. Adotar bidirectional-streaming "porque é moderno" para um caso que é claramente request/response transforma código simples em uma máquina de estados frágil. Use streaming **só** quando o dado é genuinamente um fluxo (telemetria contínua, upload de arquivo grande, feed em tempo real).

### (3) Expor gRPC direto ao browser

gRPC depende de recursos do HTTP/2 (controle fino sobre frames, trailers) que **os browsers não expõem** via `fetch`/`XHR`. Não dá para chamar um endpoint gRPC diretamente de JavaScript no navegador. A solução é colocar uma camada de tradução: **gRPC-Web** (com um proxy como Envoy fazendo a ponte) ou um **gateway** que transcodifica REST/JSON ↔ gRPC. Esquecer disso e tentar "consumir gRPC do front-end" é frustração garantida — gRPC nasceu para comunicação **serviço-a-serviço**, não browser-a-serviço.

## Em entrevista

### Frase pronta (inglês)

> gRPC is a high-performance RPC framework that runs over HTTP/2 and uses Protocol Buffers as its IDL and binary wire format. I reach for it for **synchronous, point-to-point** communication between internal services — when the caller genuinely needs the response right now to continue, like a BFF querying a catalog service. The key trade-off I keep in mind is that gRPC, like REST, is **temporally coupled**: both the caller and the callee must be alive at the same time, so an outage or slowdown in the callee propagates back up the call chain. That's fundamentally different from **asynchronous messaging** with a broker like Kafka, where the producer publishes a fact and moves on, and the consumer processes it whenever it's ready — fully decoupled in time. So I don't treat gRPC as a replacement for messaging; I pick gRPC when I need a synchronous answer, and messaging when I want to decouple producer from consumer and tolerate downstream failure.

### Vocabulário

| Termo (EN) | Termo (PT) | Sentido |
| --- | --- | --- |
| Remote Procedure Call (RPC) | Chamada de procedimento remoto | Fazer uma chamada de rede parecer uma chamada de função local |
| Stub | Stub | Objeto local gerado que espelha os métodos do serviço remoto |
| Unary / streaming call | Chamada unária / com streaming | Os 4 modos de RPC do gRPC |
| Temporal coupling | Acoplamento temporal | Cliente e servidor precisam estar vivos ao mesmo tempo |
| Multiplexing | Multiplexação | Várias chamadas numa única conexão HTTP/2 |
| Backpressure | Contrapressão | Controle de vazão quando o produtor é mais rápido que o consumidor |

## Veja também

- [[03-Dominios/Java/Mensageria/index|Mensageria (MOC do galho)]]
- [[03-Dominios/Java/index|Trilha Java]]
- [[03-Dominios/Java/Mensageria/27 - Protocol Buffers — a IDL e a serialização binária|Protocol Buffers]]
- [[03-Dominios/Java/Mensageria/01 - O que é mensageria e arquitetura orientada a eventos|O que é mensageria]]
- [[03-Dominios/Java/Mensageria/04 - O ecossistema de brokers na JVM|O ecossistema de brokers]]
- [[03-Dominios/Java/Dicionário de Java|Dicionário de Java]]

## Referências

- [gRPC — Documentation](https://grpc.io/docs/) — portal oficial de documentação.
- [gRPC — Core concepts, architecture and lifecycle](https://grpc.io/docs/what-is-grpc/core-concepts/) — os 4 tipos de RPC, o conceito de stub e o uso de Protocol Buffers como IDL.
- [grpc/grpc-java (GitHub)](https://github.com/grpc/grpc-java) — implementação Java do gRPC; HTTP/2, camadas Stub/Channel/Transport e geração de stubs a partir do `.proto`.
