---
title: "NATS em Go"
type: concept
fase: adepto
tags:
  - go
  - mensageria
  - nats
  - jetstream
  - pubsub
publish: true
created: 2026-07-18
updated: 2026-07-18
---

# NATS em Go

> [!abstract] TL;DR
> **NATS** é um broker de mensageria minimalista, feito para latência baixa e operação simples — o oposto do peso operacional do Kafka. No modo **core** (`nats.Publish`/`nats.Subscribe`), mensagens são fire-and-forget: sem persistência, sem replay, at-most-once. Quando você precisa de durabilidade — mensagem sobrevive a reinício de consumer, replay, ack explícito —, liga o **JetStream**, a camada de persistência do NATS por cima do mesmo protocolo. A escolha entre NATS e Kafka não é "qual é melhor", é "qual encaixa no formato do problema": Kafka para streams de eventos de alto volume com retenção longa e ordenação forte por partição; NATS core para comunicação de baixa latência entre serviços (RPC assíncrono, service discovery, fan-out); JetStream para o meio-termo, quando você quer a simplicidade operacional do NATS mas ainda precisa de "a mensagem não pode sumir".

## O problema: nem tudo precisa de Kafka

A nota anterior mostrou Kafka em Go — tópicos particionados, offsets, consumer groups, um cluster de brokers coordenado por um protocolo de replicação sofisticado. Isso resolve muito bem streams de eventos de alto volume com retenção de dias ou semanas. Mas imagine um cenário mais modesto: três microsserviços internos que precisam trocar notificações leves — "usuário X atualizou o perfil", "pedido Y mudou de status" — sem necessidade de guardar histórico, só de entregar rápido enquanto todo mundo está de pé.

Rodar um cluster Kafka (com Zookeeper ou KRaft, discos dedicados, tuning de partições) para esse cenário é como alugar um caminhão para levar uma carta. Funciona, mas o custo operacional — configurar, monitorar, fazer capacity planning de um cluster distribuído — não se paga para uma necessidade tão simples.

É exatamente o nicho que o NATS ocupa: um binário único (`nats-server`), sem dependências externas, que sobe em milissegundos e fala pub/sub, request/reply e, quando pedido, mensageria durável — tudo isso com uma pegada de memória e complexidade operacional muito menor que Kafka. O trade-off existe (throughput sustentado e retenção de longo prazo do Kafka são difíceis de bater), mas para o caso de uso certo, NATS é "instale e use", não "monte um time de plataforma para operar".

## NATS core: pub/sub sem memória

No modo core, o NATS não guarda nada. Um publisher manda uma mensagem para um **subject** (o equivalente ao tópico do Kafka, mas hierárquico e sem partições); qualquer subscriber conectado naquele subject naquele instante recebe a mensagem. Se ninguém estiver ouvindo, a mensagem se perde — não há log, não há replay.

```mermaid
sequenceDiagram
    participant P as Publisher
    participant S as nats-server
    participant C1 as Subscriber A
    participant C2 as Subscriber B

    C1->>S: Subscribe("pedidos.criado")
    C2->>S: Subscribe("pedidos.criado")
    P->>S: Publish("pedidos.criado", msg)
    S-->>C1: msg (entregue)
    S-->>C2: msg (entregue)
    Note over S: Sem persistência —<br/>se ninguém tivesse<br/>assinado, msg some
```

Isso soa frágil, mas é uma escolha deliberada: sem log em disco para escrever a cada mensagem, o NATS core entrega latências de microssegundos a poucos milissegundos, ordens de grandeza abaixo do que um sistema com persistência garantida consegue. É o encaixe perfeito para: heartbeats, invalidação de cache distribuído, notificações efêmeras, coordenação de serviços que já toleram perder uma mensagem ocasional porque o próximo heartbeat corrige o estado.

### Subjects: hierarquia com wildcards

Onde Kafka usa tópicos "flat" (nome de string, sem estrutura interna reconhecida pelo broker), NATS usa **subjects** hierárquicos separados por ponto — `pedidos.criado`, `pedidos.cancelado`, `usuarios.perfil.atualizado` — e permite assinar padrões com wildcards:

- `*` casa exatamente um token: `pedidos.*` casa `pedidos.criado` e `pedidos.cancelado`, mas não `pedidos.criado.urgente`.
- `>` casa um ou mais tokens até o fim: `pedidos.>` casa `pedidos.criado`, `pedidos.criado.urgente`, qualquer coisa que comece com `pedidos.`.

Essa hierarquia dá um jeito barato de fazer roteamento fino sem precisar criar um tópico por combinação de evento — um único subscriber em `pedidos.>` recebe tudo relacionado a pedidos, enquanto outro assina só `pedidos.cancelado` para reagir a um caso específico.

### Publicar e assinar em Go

O cliente oficial é `github.com/nats-io/nats.go`. Conectar, publicar e assinar cabem em poucas linhas:

```go
package main

import (
    "fmt"
    "log"
    "time"

    "github.com/nats-io/nats.go"
)

func main() {
    nc, err := nats.Connect(nats.DefaultURL) // nats://127.0.0.1:4222
    if err != nil {
        log.Fatalf("conectar: %v", err)
    }
    defer nc.Close()

    // Assinar um subject — callback assíncrono
    sub, err := nc.Subscribe("pedidos.criado", func(msg *nats.Msg) {
        fmt.Printf("recebido: %s\n", string(msg.Data))
    })
    if err != nil {
        log.Fatalf("subscribe: %v", err)
    }
    defer sub.Unsubscribe()

    // Publicar
    if err := nc.Publish("pedidos.criado", []byte(`{"id":"42"}`)); err != nil {
        log.Fatalf("publish: %v", err)
    }

    time.Sleep(100 * time.Millisecond) // dar tempo do callback rodar
}
```

> [!info] Go 1.22+: range sobre canal de mensagens com `SubscribeSync`
> Além do modo callback (`Subscribe`), o cliente oferece `SubscribeSync`, que devolve um objeto do qual você faz `sub.NextMsg(timeout)` num laço — útil quando você quer controlar o pull explicitamente em vez de receber um callback assíncrono. Combinado com o loop var por-iteração do Go 1.22 (cada `for` cria sua própria variável), processar mensagens dentro de goroutines lançadas por essa alça deixou de exigir o velho truque `msg := msg` para evitar captura de variável compartilhada.

Uma variação comum é **request/reply**, onde o publisher espera uma resposta síncrona — o NATS resolve isso nativamente, sem precisar montar tópico de resposta manualmente como se faz em Kafka:

```go
resp, err := nc.Request("servico.calcular", []byte(`{"a":2,"b":3}`), 2*time.Second)
if err != nil {
    log.Fatalf("request: %v", err)
}
fmt.Println(string(resp.Data)) // resposta do outro lado
```

Do outro lado, um serviço responde assinando o mesmo subject e usando `msg.Respond`:

```go
nc.Subscribe("servico.calcular", func(msg *nats.Msg) {
    resultado := []byte(`{"soma":5}`)
    msg.Respond(resultado)
})
```

Esse padrão de RPC assíncrono embutido no protocolo é algo que Kafka não oferece de forma nativa — lá, request/reply se simula com dois tópicos e correlação manual de IDs.

### Queue groups: balanceamento de carga sem stream

Um detalhe que a tabela cross-stack acima só citou de passagem merece um exemplo: por padrão, se dois processos assinam o mesmo subject no modo core, **os dois recebem cada mensagem** — é fan-out puro, cada subscriber independente. Se a intenção for outra — distribuir mensagens entre várias instâncias do mesmo serviço, cada mensagem processada por só uma delas, como um pool de workers competindo por trabalho —, o NATS resolve isso sem precisar de stream nem persistência: basta agrupar os subscribers num **queue group**.

```go
// Três instâncias do mesmo worker, todas no grupo "workers-pedidos":
nc.QueueSubscribe("pedidos.criado", "workers-pedidos", func(msg *nats.Msg) {
    fmt.Printf("processado por esta instância: %s\n", string(msg.Data))
})
```

Cada mensagem publicada em `pedidos.criado` vai para **uma única** instância do grupo `workers-pedidos`, escolhida pelo servidor — as outras não recebem nada daquela mensagem específica. É o análogo, em espírito, ao que um consumer group faz no Kafka (várias instâncias dividindo o consumo de um tópico), só que sem partições, sem persistência e sem rebalanceamento coordenado — o servidor NATS decide o roteamento a cada mensagem, em tempo real, sem protocolo de coordenação visível. A troca: sem partições, não há garantia de ordem entre mensagens do mesmo subject processadas por instâncias diferentes do grupo — se ordenação estrita importa, isso é argumento a favor de JetStream (que preserva a ordem de entrega dentro de um consumer) ou de Kafka (que preserva ordem por partição).

## JetStream: quando "pode sumir" deixa de ser aceitável

Core NATS resolve o caso "entregar rápido, tolerar perda". Mas e quando a mensagem representa dinheiro, um pedido, um evento que não pode simplesmente evaporar se o consumer estiver fora do ar no momento da publicação? Para isso existe o **JetStream** — habilitado desde o NATS 2.2 (2021), uma camada de persistência construída sobre o mesmo protocolo NATS, não um sistema separado.

Com JetStream, você declara um **stream** — um log persistente vinculado a um ou mais subjects — e o servidor passa a gravar cada mensagem publicada naqueles subjects em disco (ou memória, configurável), com retenção controlável por tempo, tamanho ou número de mensagens.

```mermaid
flowchart LR
    P["Publisher"] -->|publish| S["Subject: pedidos.criado"]
    S --> ST["Stream JetStream\n(persistido em disco)"]
    ST --> C1["Consumer durável 1\n(ack explícito)"]
    ST --> C2["Consumer durável 2\n(replay independente)"]

    style ST fill:#4A90D9,color:#fff
    style C1 fill:#F5A623,color:#000
    style C2 fill:#F5A623,color:#000
```

A diferença estrutural em relação ao core: consumers do JetStream são **duráveis** — o servidor lembra até onde cada consumer leu, exatamente como o Kafka lembra offsets por consumer group. Se o consumer cair e voltar, ele retoma de onde parou em vez de perder tudo que foi publicado no meio-tempo. E cada consumer pode ter sua própria posição de leitura, então dois consumers diferentes podem processar o mesmo stream em ritmos e pontos diferentes — o mesmo desacoplamento de "múltiplos leitores independentes" que Kafka oferece via consumer groups, discutido na nota 01.

### Publicar e consumir com JetStream em Go

```go
package main

import (
    "context"
    "fmt"
    "log"
    "time"

    "github.com/nats-io/nats.go"
    "github.com/nats-io/nats.go/jetstream"
)

func main() {
    nc, err := nats.Connect(nats.DefaultURL)
    if err != nil {
        log.Fatalf("conectar: %v", err)
    }
    defer nc.Close()

    js, err := jetstream.New(nc)
    if err != nil {
        log.Fatalf("jetstream: %v", err)
    }

    ctx, cancel := context.WithTimeout(context.Background(), 5*time.Second)
    defer cancel()

    // Declarar (ou obter, se já existir) o stream
    stream, err := js.CreateOrUpdateStream(ctx, jetstream.StreamConfig{
        Name:     "PEDIDOS",
        Subjects: []string{"pedidos.>"},
        Storage:  jetstream.FileStorage, // persistido em disco
    })
    if err != nil {
        log.Fatalf("criar stream: %v", err)
    }

    // Publicar — agora com ack de persistência
    ack, err := js.Publish(ctx, "pedidos.criado", []byte(`{"id":"42"}`))
    if err != nil {
        log.Fatalf("publish: %v", err)
    }
    fmt.Printf("gravado no stream %s, sequência %d\n", ack.Stream, ack.Sequence)

    // Consumer durável — sobrevive a reinício do processo
    cons, err := stream.CreateOrUpdateConsumer(ctx, jetstream.ConsumerConfig{
        Durable:   "worker-pedidos",
        AckPolicy: jetstream.AckExplicitPolicy,
    })
    if err != nil {
        log.Fatalf("criar consumer: %v", err)
    }

    msgs, err := cons.Fetch(10, jetstream.FetchMaxWait(2*time.Second))
    if err != nil {
        log.Fatalf("fetch: %v", err)
    }
    for msg := range msgs.Messages() {
        fmt.Printf("processando: %s\n", string(msg.Data()))
        msg.Ack() // sem isso, a mensagem volta a ser redeliverada
    }
}
```

O `msg.Ack()` explícito é o mesmo contrato conceitual do `commit` de offset no Kafka: até você confirmar, o servidor considera a mensagem "em voo" e vai redeliverá-la se o ack não chegar dentro do prazo configurado (`AckWait`). A diferença de fundo em relação ao "at most once" do core: com JetStream, uma falha do consumer entre receber a mensagem e processá-la resulta em reentrega, não em perda — o preço, como sempre em mensageria, é a possibilidade de duplicata, que volta a exigir idempotência do lado de quem consome (assunto da nota 05 deste galho).

### Retenção: quem pode reler a mesma mensagem

Um detalhe que decide boa parte do design é a **política de retenção** do stream, configurada em `StreamConfig.Retention`:

- `LimitsPolicy` (padrão) — a mensagem fica retida até expirar por tempo/tamanho configurado, **independente** de quantos consumers já a leram. Vários consumers duráveis podem reler o mesmo histórico, cada um na sua própria posição — o mesmo modelo do Kafka, onde a leitura não remove a mensagem do log.
- `WorkQueuePolicy` — a mensagem é **removida do stream assim que um consumer der ack** nela. Só pode haver um consumer "efetivo" por mensagem — é o modelo de fila de tarefas clássica (um item, processado uma vez, some depois), mais próximo de RabbitMQ do que do modelo de log do Kafka.
- `InterestPolicy` — a mensagem some quando não há mais nenhum consumer interessado nela (todos os consumers registrados já deram ack).

Escolher `WorkQueuePolicy` para um stream que várias equipes querem reler independentemente é um erro de design clássico: a segunda equipe a assinar encontra o stream vazio, porque a primeira já consumiu e confirmou tudo. Streams de evento de domínio, pensados para múltiplos consumidores desacoplados, quase sempre querem `LimitsPolicy`; filas de trabalho ponto-a-ponto (um processador por item) é que combinam com `WorkQueuePolicy`.

### Consumo contínuo com `Consume`

O exemplo anterior usou `Fetch`, que puxa um lote finito e retorna. Para um worker de vida longa, que fica processando mensagens indefinidamente, o cliente oferece `Consume`, que registra um callback e entrega mensagens continuamente — o análogo, em JetStream, do `Subscribe` do core:

```go
consCtx, err := cons.Consume(func(msg jetstream.Msg) {
    fmt.Printf("processando: %s\n", string(msg.Data()))
    if err := processar(msg.Data()); err != nil {
        msg.Nak() // pede redelivery em vez de Ack
        return
    }
    msg.Ack()
})
if err != nil {
    log.Fatalf("consume: %v", err)
}
defer consCtx.Stop()

select {} // manter o processo vivo
```

`msg.Nak()` (*negative ack*) é o gesto explícito de "não consegui processar, tente de novo" — diferente de simplesmente não chamar `Ack()`, que só resulta em redelivery depois do `AckWait` expirar por timeout. Nak sinaliza a falha imediatamente, o que costuma acelerar o retry em cenários onde o erro já é conhecido no momento do processamento (a nota 06 deste galho aprofunda essa mecânica de retry e quando ela precisa de backoff em vez de redelivery imediata).

> [!warning] Esquecer `msg.Ack()` trava o consumer, não silenciosamente perde
> Ao contrário do core NATS (onde uma mensagem não entregue simplesmente evapora), esquecer de dar ack numa mensagem JetStream faz o servidor **redeliverá-la** repetidamente após o `AckWait` expirar. Um bug que processa a mensagem mas nunca chama `Ack()` não passa despercebido por muito tempo — ele se manifesta como reprocessamento infinito da mesma mensagem, útil como sinal de alarme, mas só se você estiver monitorando taxa de redelivery.

## Quando NATS, quando Kafka

| Critério | NATS (core) | JetStream | Kafka |
|---|---|---|---|
| Persistência | Nenhuma | Sim, configurável | Sim, log append-only |
| Latência típica | Microssegundos–poucos ms | Poucos ms | Dezenas de ms |
| Retenção longa (dias/semanas) de alto volume | — | Possível, mas não é o forte | Ponto forte |
| Complexidade operacional | Baixa (binário único) | Baixa–média | Alta (cluster, tuning) |
| Request/reply nativo | Sim | Sim (via subject) | Não (simula com 2 tópicos) |
| Ordenação forte por partição | — | Por stream/subject | Sim, por partição |
| Ecossistema de stream processing (Kafka Streams, ksqlDB) | Não | Limitado | Rico |

Regra prática: se o problema é "componentes internos precisam se falar rápido, com tolerância a perda ocasional ou com durabilidade modesta", NATS (core ou JetStream) resolve com muito menos operação. Se o problema é "preciso de um log de eventos de negócio, replay de meses, múltiplos consumidores desacoplados no tempo, throughput sustentado de milhões de mensagens por segundo", Kafka é a ferramenta desenhada para isso. Muitas arquiteturas reais usam os dois: Kafka como espinha dorsal de eventos de domínio, NATS para a "conversa" de baixa latência entre serviços que não precisa virar registro histórico.

## Vindo de outras stacks

| Vindo de | Equivalente mais próximo | Onde NATS diverge |
|---|---|---|
| Java (Spring + RabbitMQ) | Exchange/routing key ≈ subject hierárquico | NATS não tem filas com múltiplos consumers competindo por padrão — isso é o **queue group**, um parâmetro extra na subscription (`nc.QueueSubscribe`), não um tipo de recurso separado |
| Node.js (Redis Pub/Sub) | Modo core é quase idêntico em espírito — fire-and-forget, sem persistência | JetStream é o que o Redis Pub/Sub puro nunca teve nativamente: persistência e replay embutidos no mesmo protocolo |
| Python (Celery + broker) | JetStream lembra uma fila de tarefas durável | NATS não é um sistema de filas de tarefas pronto (sem retry policy, sem agendamento por padrão) — esses padrões, quando necessários, são construídos por cima, tema da nota 06 deste galho |

## Armadilhas comuns

> [!warning] Confundir "NATS" com "NATS JetStream" na hora de decidir arquitetura
> "Vamos usar NATS porque é mais simples que Kafka" só é uma frase completa se você já decidiu se precisa de persistência. Core NATS sem JetStream não é um substituto de Kafka para nada que exija durabilidade — é uma ferramenta diferente, para um problema diferente (comunicação efêmera). Declarar isso errado cedo custa uma migração de arquitetura depois.

> [!warning] `nats.DefaultURL` aponta para `localhost` — não usar em produção sem configurar
> É comum copiar `nats.Connect(nats.DefaultURL)` de exemplos e esquecer de trocar pela URL real do cluster (`nats://user:pass@nats-cluster:4222`) antes do deploy. Diferente do Kafka, onde a lista de brokers costuma vir de variável de ambiente desde o primeiro protótipo, o exemplo "hello world" do NATS já compila e roda local sem configuração nenhuma — o que facilita esquecer de parametrizar antes de subir para produção.

> [!warning] Stream sem `Storage: FileStorage` explícito pode ficar em memória
> Dependendo da configuração padrão do servidor, um stream criado sem especificar `Storage` pode acabar como `MemoryStorage` — que se perde num restart do `nats-server`. Para qualquer stream que precise sobreviver a um reinício do broker, declare `Storage: jetstream.FileStorage` explicitamente na criação.

> [!warning] Queue group não substitui JetStream quando ordenação ou durabilidade importam
> É tentador usar `QueueSubscribe` para "distribuir carga" e achar que resolveu o mesmo problema que um consumer group do Kafka resolve. Não resolve dois pontos: se o processo que recebeu a mensagem cair antes de terminar de processá-la, a mensagem **não volta** — modo core não tem redelivery, porque não tem persistência nenhuma. Para carga distribuída **e** garantia de que a mensagem não se perde num crash de worker, o par certo é JetStream com múltiplos consumers duráveis (ou um único consumer compartilhado por várias goroutines via `Fetch`/`Consume`), não queue group de core NATS.

## Como explicar em inglês

> NATS is a lightweight messaging system built for low latency and minimal operational overhead — a single binary with no external dependencies, as opposed to Kafka's multi-broker cluster. Core NATS is fire-and-forget: publish to a **subject**, any currently-connected subscriber receives it, and nothing is persisted — if nobody's listening, the message is gone. **JetStream**, NATS's persistence layer added in v2.2, turns a subject into a durable, replayable **stream** with durable consumers that track their own read position and require explicit **ack**, much like Kafka's consumer-group offsets. The deciding factor between NATS and Kafka isn't which is "better" — it's fit: NATS (core or JetStream) for low-latency service-to-service communication and request/reply, Kafka for high-volume, long-retention event streams with strong per-partition ordering.

| Termo PT | Termo EN |
|---|---|
| assunto / tópico hierárquico | subject |
| núcleo (modo sem persistência) | core |
| fluxo persistido | stream |
| consumidor durável | durable consumer |
| confirmação explícita | explicit ack |
| grupo de fila | queue group |
| pergunta e resposta | request/reply |
| difusão para vários assinantes | fan-out |

## O que vem a seguir

Kafka e NATS resolvem o transporte da mensagem — publicar e entregar. Mas quem realmente processa essas mensagens do lado do consumer, com quantos workers, em que ritmo, e o que fazer quando o processamento é mais lento que a chegada de mensagens, é assunto separado. A [[04 - Consumers e workers|nota 04]] entra nesse design: como estruturar um consumer Go que lê de Kafka ou NATS e distribui o trabalho entre goroutines sem perder controle de concorrência nem overload o downstream.

## Veja também

- [[01 - Por que mensageria — desacoplamento|01 — Por que mensageria — desacoplamento]] — o problema estrutural que tanto Kafka quanto NATS resolvem
- [[02 - Kafka em Go|02 — Kafka em Go]] — o contraponto de alto volume e retenção longa, comparado nesta nota
- [[04 - Consumers e workers|04 — Consumers e workers]] — próxima nota: como processar mensagens vindas de qualquer um dos dois brokers
- [[05 - Entrega e idempotência|05 — Entrega e idempotência]] — por que at-least-once do JetStream exige consumers idempotentes
- [[03-Dominios/Tecnologia/Go/index|Trilha Go]]

## Fontes

- Synadia / NATS.io. *NATS Docs — JetStream*. docs.nats.io. https://docs.nats.io/nats-concepts/jetstream (acessado em 2026-07-18)
- Synadia / NATS.io. *NATS Docs — Subject-Based Messaging*. docs.nats.io. https://docs.nats.io/nats-concepts/subjects (acessado em 2026-07-18)
- NATS.go — Go Client for NATS. pkg.go.dev. https://pkg.go.dev/github.com/nats-io/nats.go (acessado em 2026-07-18)
- NATS.go JetStream package. pkg.go.dev. https://pkg.go.dev/github.com/nats-io/nats.go/jetstream (acessado em 2026-07-18)
- Synadia / NATS.io. *NATS Docs — Queue Groups*. docs.nats.io. https://docs.nats.io/nats-concepts/core-nats/queue (acessado em 2026-07-18)
