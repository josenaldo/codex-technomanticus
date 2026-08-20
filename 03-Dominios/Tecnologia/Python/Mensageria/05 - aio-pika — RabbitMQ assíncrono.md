---
title: "aio-pika — RabbitMQ assíncrono"
created: 2026-07-12
updated: 2026-07-12
type: concept
status: seedling
fase: Adepto→Magus
tags:
  - python
  - mensageria
  - rabbitmq
  - asyncio
  - aio-pika
publish: true
aliases:
  - "aio-pika"
  - "connect_robust"
  - "AMQP assíncrono em Python"
---

# aio-pika — RabbitMQ assíncrono

> [!abstract] TL;DR
> aio-pika é um cliente **assíncrono** (`asyncio`) que fala o protocolo AMQP 0-9-1 direto com o RabbitMQ — sem a camada de "tarefa" que Celery e RQ colocam no meio (cobertas nas notas 02-04 deste galho). `connect_robust()` abre uma conexão com **reconexão automática**: se o RabbitMQ reiniciar, o cliente reconecta e redeclara exchanges/queues/bindings sozinho. Publicar é declarar uma exchange e chamar `exchange.publish(...)` com uma routing key; consumir é declarar uma queue, fazer bind numa exchange, e iterar mensagens com `async for message in queue.iterator()`. A decisão que mais separa código de brinquedo de código de produção é **ack manual**: com `no_ack=False` (o padrão), a mensagem só sai da fila depois que o código chama `message.ack()` explicitamente — se o processo cair no meio do processamento, a mensagem volta para a fila em vez de desaparecer. O preço de todo esse controle: nada de retry, nada de idempotência, nada de dead-letter vem de graça — é código seu.

## Um roteador de eventos que uma task queue não modela bem

O time da plataforma de cursos do resto deste galho decidiu construir um serviço de notificações centralizado. A ideia é simples no papel: em vez de cada microsserviço (pedidos, pagamentos, matrículas) implementar seu próprio código de envio de push notification e e-mail, um único **serviço de notificações** escuta o que acontece no sistema inteiro e decide, a partir do tipo de evento, qual notificação disparar e para quem.

O problema aparece assim que alguém tenta desenhar o contrato. O serviço de notificações precisa reagir a eventos de **três origens diferentes**, que não se conhecem entre si e não deveriam precisar se conhecer:

- `pedidos-service` publica `pedido.criado` e `pedido.cancelado`.
- `pagamentos-service` publica `pagamento.confirmado` e `pagamento.recusado`.
- `cursos-service` publica `curso.concluido`.

Modelar isso com Celery, como a nota 01 deste galho já registrou, exigiria que cada um desses três serviços conhecesse a existência do serviço de notificações e chamasse `.delay()` numa task que mora fisicamente noutro código-base — ou, pior, que o serviço de notificações expusesse `enviar_notificacao_pedido_criado.delay(...)`, `enviar_notificacao_pagamento_confirmado.delay(...)` como tasks separadas que cada produtor precisa importar e chamar corretamente. Isso acopla os três serviços produtores ao vocabulário interno do serviço de notificações, e cada evento novo (`curso.iniciado`, `pedido.reembolsado`) exige uma mudança coordenada nos dois lados.

O que o time realmente precisa é um **roteador de mensagens** que os produtores publicam sem saber quem — ou quantos — vão consumir, e onde o serviço de notificações decide, de forma centralizada, quais padrões de evento lhe interessam. Isso é exatamente o modelo `exchange → binding → queue` do AMQP, já apresentado em [[03-Dominios/Engenharia/Comunicação entre Sistemas/Mensageria/RabbitMQ|Comunicação entre Sistemas — RabbitMQ]]: os três serviços produtores publicam numa **exchange do tipo topic** compartilhada, com uma routing key que descreve o evento (`pedido.criado`, `pagamento.confirmado`), e o serviço de notificações declara **uma única queue** com bindings que capturam os padrões que interessam — sem que nenhum produtor precise saber que esse consumidor existe.

> [!question]- Por que não usar RQ ou Celery com uma fila só e cada produtor publicando na "fila de notificações"?
> Porque isso empurra a decisão de roteamento para o produtor: cada um dos três serviços precisaria saber, hardcoded, o nome da fila de notificações e publicar diretamente nela — voltando ao acoplamento que o desenho está tentando evitar. Com uma exchange topic no meio, o produtor só declara "isto é um evento do tipo `pedido.criado`" e publica; quem decide se isso interessa a alguém — e a quantos consumidores, hoje ou no futuro — é o binding, configurado do lado do consumidor. Adicionar um segundo consumidor (um serviço de auditoria, por exemplo) não exige tocar em nenhum dos três produtores — só criar uma segunda queue com seus próprios bindings na mesma exchange.

Esta nota resolve esse cenário com aio-pika de ponta a ponta: declarar a exchange, publicar eventos JSON com routing key, declarar a queue de notificações com múltiplos bindings, consumir com `async`/`await`, e — o ponto que mais separa protótipo de produção — decidir corretamente entre ack manual e automático.

## `connect_robust()`: a conexão que sobrevive a um restart do broker

Toda interação com aio-pika começa abrindo uma conexão. A biblioteca oferece duas funções para isso — `connect()` e `connect_robust()` — e a diferença entre elas é, na prática, a diferença entre um protótipo e algo que sobrevive a uma operação de manutenção no RabbitMQ:

```python
import aio_pika

# connect() — conexão simples, sem reconexão automática
connection = await aio_pika.connect("amqp://guest:guest@localhost/")

# connect_robust() — reconecta sozinho se a conexão cair
connection = await aio_pika.connect_robust("amqp://guest:guest@localhost/")
```

`connect_robust()` é a função citada em praticamente todo exemplo de produção da documentação oficial ([aio-pika docs, *Robust connection*](https://aio-pika.readthedocs.io/), 2026) por um motivo concreto: RabbitMQ **vai** reiniciar em algum momento — deploy de uma nova versão do broker, failover num cluster, um pod de Kubernetes sendo substituído. Com `connect()`, essa reinicialização derruba a conexão do cliente e o código da aplicação precisa detectar a queda e reconectar manualmente, redeclarando toda a topologia (exchange, queue, bindings) do zero — exatamente o tipo de código de resiliência repetitivo que, se esquecido em um único lugar, gera uma falha silenciosa em produção.

`connect_robust()` resolve isso internamente: monitora a conexão, e se ela cair, reconecta automaticamente com backoff, e — ponto importante — **redeclara exchanges, queues e bindings automaticamente**, desde que essas declarações tenham sido feitas através dos objetos retornados pela conexão robusta (não redeclaradas manualmente fora desse fluxo). Do ponto de vista do código de aplicação, uma queda momentânea do broker é invisível: o `async for` que está consumindo mensagens simplesmente pausa e retoma quando a conexão volta.

> [!warning] `connect_robust()` reconecta a conexão, mas não reenvia mensagens perdidas em trânsito
> **O que acontece:** um time assume que `connect_robust()` torna o publish "à prova de queda de broker" — publica uma mensagem, a conexão cai no meio da chamada, e a mensagem nunca chega ao RabbitMQ, sem nenhum erro visível no código de aplicação se o publish não for tratado com cuidado. **Por quê:** reconexão automática resolve a **disponibilidade da conexão** — o cliente volta a falar com o broker sem intervenção manual — mas não resolve a **garantia de entrega de uma publicação específica** que estava em voo no momento exato da queda. Isso é um problema diferente, coberto por **publisher confirms** (`await exchange.publish(..., mandatory=True)` combinado com o canal em modo de confirmação), que já são explicados em profundidade — de forma agnóstica de linguagem — em [[03-Dominios/Engenharia/Comunicação entre Sistemas/Mensageria/RabbitMQ|Comunicação entre Sistemas — RabbitMQ]]. **Como evitar:** tratar `connect_robust()` como resiliência de conexão, não como garantia de entrega — para publicações que não podem se perder, usar publisher confirms e, no lado da aplicação que originou o evento, um padrão de Outbox (a nota 07 deste galho cobre Outbox aplicado com código Python real).

## Declarando a topologia e publicando

Com a conexão aberta, o próximo passo é abrir um **channel** — o canal lógico multiplexado sobre a conexão TCP, o mesmo conceito já apresentado na nota de RabbitMQ em Comunicação entre Sistemas — e declarar a exchange onde os três serviços produtores vão publicar. Como o roteamento precisa casar por padrão de routing key (`pedido.*`, `pagamento.*`, e o evento único `curso.concluido`), a exchange é do tipo **topic**:

```python
import aio_pika
import json

async def publicar_evento(routing_key: str, payload: dict) -> None:
    connection = await aio_pika.connect_robust("amqp://guest:guest@localhost/")
    async with connection:
        channel = await connection.channel()

        exchange = await channel.declare_exchange(
            "eventos.dominio",
            aio_pika.ExchangeType.TOPIC,
            durable=True,
        )

        mensagem = aio_pika.Message(
            body=json.dumps(payload).encode(),
            content_type="application/json",
            delivery_mode=aio_pika.DeliveryMode.PERSISTENT,
        )

        await exchange.publish(mensagem, routing_key=routing_key)
```

Cada um dos três serviços produtores chama essa mesma função com uma routing key diferente, sem precisar saber nada sobre o serviço de notificações:

```python
# dentro de pedidos-service
await publicar_evento("pedido.criado", {"pedido_id": pedido.id, "usuario_id": pedido.usuario_id})

# dentro de pagamentos-service
await publicar_evento("pagamento.confirmado", {"pedido_id": cobranca.pedido_id, "valor": cobranca.valor})

# dentro de cursos-service
await publicar_evento("curso.concluido", {"usuario_id": matricula.usuario_id, "curso_id": matricula.curso_id})
```

Três detalhes nesse `aio_pika.Message` valem nomear porque não são o caminho padrão de um `Hello World` de AMQP:

- **`durable=True`** na exchange e **`delivery_mode=aio_pika.DeliveryMode.PERSISTENT`** na mensagem — sem os dois, a exchange e a mensagem em trânsito não sobrevivem a um restart do broker. `async_pika` não assume persistência por padrão; é uma escolha explícita, coerente com a combinação `exchange durável + queue durável + mensagem persistente` já detalhada em [[03-Dominios/Engenharia/Comunicação entre Sistemas/Mensageria/RabbitMQ|Comunicação entre Sistemas — RabbitMQ]].
- **`content_type="application/json"`** — não é obrigatório para o AMQP funcionar, mas documenta no envelope da mensagem, de forma que qualquer consumidor (Python, Java, Node.js) sabe como desserializar o `body` sem precisar de um acordo fora de banda.
- **`declare_exchange` é idempotente** — chamar de novo com os mesmos parâmetros não recria nada, só retorna uma referência à exchange existente. É seguro (e comum) declarar a mesma exchange em cada função de publish, sem precisar de um script de provisionamento separado — desde que os parâmetros (tipo, durabilidade) sejam sempre os mesmos; declarar a mesma exchange com parâmetros diferentes lança uma exceção.

```mermaid
%%{init: {"theme": "base", "themeVariables": {"primaryColor": "#4A90D9", "primaryBorderColor": "#2E5C8A", "lineColor": "#4A90D9"}}}%%
flowchart LR
    P1["pedidos-service<br/>publish('pedido.criado')"] --> EX
    P2["pagamentos-service<br/>publish('pagamento.confirmado')"] --> EX
    P3["cursos-service<br/>publish('curso.concluido')"] --> EX

    EX{"exchange topic<br/>eventos.dominio"}

    EX -->|"binding: pedido.#"| Q1["queue<br/>notificacoes.fila"]
    EX -->|"binding: pagamento.#"| Q1
    EX -->|"binding: curso.concluido"| Q1

    Q1 --> C1["serviço de notificações<br/>async for message in queue.iterator()"]

    style EX fill:#F5A623,color:#000
    style Q1 fill:#4A90D9,color:#fff
    style C1 fill:#4A90D9,color:#fff
```

**Resumo em uma frase:** três produtores que não se conhecem publicam eventos com routing keys descritivas numa exchange topic compartilhada, e um único consumidor decide — via bindings declarados do próprio lado, sem tocar nos produtores — quais padrões de evento lhe interessam.

## Declarando a queue, o bind e consumindo com `async for`

Do lado do serviço de notificações, a queue é declarada uma única vez (normalmente na inicialização do serviço) com três bindings — um para cada padrão de routing key que interessa:

```python
async def iniciar_consumidor() -> None:
    connection = await aio_pika.connect_robust("amqp://guest:guest@localhost/")
    channel = await connection.channel()
    await channel.set_qos(prefetch_count=10)

    exchange = await channel.declare_exchange(
        "eventos.dominio", aio_pika.ExchangeType.TOPIC, durable=True,
    )
    queue = await channel.declare_queue("notificacoes.fila", durable=True)

    await queue.bind(exchange, routing_key="pedido.#")
    await queue.bind(exchange, routing_key="pagamento.#")
    await queue.bind(exchange, routing_key="curso.concluido")

    async with queue.iterator() as fila_iter:
        async for message in fila_iter:
            await processar_evento(message)
```

`channel.set_qos(prefetch_count=10)` é o equivalente direto do `prefetch` já discutido na nota de RabbitMQ em Comunicação entre Sistemas: limita a quantas mensagens não confirmadas o consumer pode ter em voo ao mesmo tempo. Sem isso, o RabbitMQ pode entregar um lote grande de mensagens de uma vez para o primeiro consumer que se conectar, mesmo que outros consumers do mesmo serviço (rodando em outras réplicas) estejam ociosos — o que quebra o balanceamento de competing consumers.

O padrão `#` em `"pedido.#"` casa `pedido.criado`, `pedido.cancelado`, e qualquer routing key futura que comece com `pedido.` — incluindo `pedido.reembolsado`, se um dia esse evento passar a existir, **sem que o código do consumidor precise mudar**. Esse é o ganho concreto de topic exchange sobre a alternativa de três queues separadas (uma por origem): o serviço de notificações não precisa acompanhar, evento a evento, tudo o que os três produtores decidem publicar — só precisa manter o padrão do binding alinhado com o que interessa a ele.

`queue.iterator()` devolve um iterador assíncrono — o mesmo protocolo `async for` já visto em [[03-Dominios/Tecnologia/Python/Programação Reativa e Assíncrona/02 - Streams assíncronos — StreamReader, StreamWriter e protocolos de rede|Streams assíncronos]] deste domínio, aplicado aqui a mensagens em vez de bytes de um socket. Cada iteração do loop suspende a corrotina até a próxima mensagem chegar, cedendo o controle de volta ao event loop — que, nesse meio tempo, pode processar qualquer outra tarefa agendada nele. É o mesmo event loop coberto com profundidade em [[03-Dominios/Tecnologia/Python/Programação Reativa e Assíncrona/01 - Event loop por dentro — selectors, callbacks e a relação Future-Task|Event loop por dentro]] e usado em [[03-Dominios/Tecnologia/Python/Programação Reativa e Assíncrona/07 - Padrões de produção com asyncio — supervisão de tasks, graceful shutdown, circuit breaker|Padrões de produção com asyncio]] — a mecânica do loop em si não é reexplicada aqui, aio-pika só *usa* esse modelo de concorrência.

Existe uma alternativa por callback — `queue.consume(callback)` — em vez de `async for`, útil quando o serviço já roda outras tasks concorrentes no mesmo loop e não quer bloquear a função que iniciou o consumo:

```python
async def handler(message: aio_pika.abc.AbstractIncomingMessage) -> None:
    await processar_evento(message)

await queue.consume(handler)
# a função retorna imediatamente; o consumo continua em background no event loop
```

`queue.consume()` registra o callback e retorna — o consumo roda como uma task agendada no loop, em vez de bloquear a corrotina atual num loop `async for` explícito. A escolha entre os dois estilos é majoritariamente sobre onde o código chamador quer manter o controle: `async for` é direto de ler quando o consumo *é* a responsabilidade principal daquela corrotina (um worker dedicado); `consume(callback)` encaixa melhor quando o mesmo processo já orquestra várias fontes de trabalho concorrentes — o padrão de supervisão de múltiplas tasks já coberto em [[03-Dominios/Tecnologia/Python/Programação Reativa e Assíncrona/07 - Padrões de produção com asyncio — supervisão de tasks, graceful shutdown, circuit breaker|Padrões de produção com asyncio]].

## Connection e channel: o que abrir uma vez, o que abrir por escopo

O exemplo de `publicar_evento` acima abre uma `connection` e um `channel` novos a cada chamada, e fecha os dois ao sair do `async with`. Isso é aceitável para um exemplo didático, mas não é o padrão que um serviço real usa em produção — e entender por quê exige lembrar de um detalhe já registrado na nota de RabbitMQ em Comunicação entre Sistemas: **connection é pesada, channel é leve**.

Uma `connection` AMQP é uma conexão TCP de verdade, com handshake do protocolo, autenticação, e negociação de parâmetros — abrir e fechar uma por publicação é um desperdício de recursos de rede que se acumula rápido sob carga (cada publish pagando o custo de um three-way handshake TCP mais o handshake AMQP). O padrão correto é **uma connection de longa duração por processo**, reaproveitada, com **channels leves** abertos conforme a necessidade — um channel por corrotina concorrente que publica, por exemplo, já que channels não são thread-safe nem safe para uso concorrente sem coordenação:

```python
class PublicadorDeEventos:
    def __init__(self, amqp_url: str) -> None:
        self._amqp_url = amqp_url
        self._connection: aio_pika.RobustConnection | None = None
        self._exchange: aio_pika.abc.AbstractExchange | None = None

    async def iniciar(self) -> None:
        self._connection = await aio_pika.connect_robust(self._amqp_url)
        channel = await self._connection.channel()
        self._exchange = await channel.declare_exchange(
            "eventos.dominio", aio_pika.ExchangeType.TOPIC, durable=True,
        )

    async def publicar(self, routing_key: str, payload: dict) -> None:
        mensagem = aio_pika.Message(
            body=json.dumps(payload).encode(),
            content_type="application/json",
            delivery_mode=aio_pika.DeliveryMode.PERSISTENT,
        )
        await self._exchange.publish(mensagem, routing_key=routing_key)

    async def encerrar(self) -> None:
        if self._connection:
            await self._connection.close()
```

Esse `PublicadorDeEventos` é instanciado uma vez na inicialização de cada um dos três serviços produtores (`iniciar()` chamado no startup da aplicação, tipicamente no `lifespan` de um app FastAPI) e reaproveitado para toda publicação subsequente — a connection e a exchange já declaradas ficam vivas durante toda a vida do processo, e `connect_robust()` garante que, mesmo que o RabbitMQ reinicie no meio do dia, essa mesma instância continua funcionando sem reinicialização manual.

> [!warning] Abrir uma connection nova por mensagem publicada
> **O que acontece:** um endpoint HTTP chama `aio_pika.connect_robust(...)` dentro do handler de cada requisição, publica uma mensagem, e fecha a conexão — e sob carga moderada (algumas centenas de requisições por segundo), a latência do endpoint sobe visivelmente e o RabbitMQ passa a reportar um número de conexões abrindo e fechando constantemente no Management Plugin. **Por quê:** cada `connect_robust()` paga o custo completo de estabelecer uma conexão TCP e negociar o protocolo AMQP — handshake que, multiplicado por milhares de requisições, vira uma fração significativa da latência total do endpoint, além de pressionar o RabbitMQ com um volume de churn de conexões que ele não foi desenhado para absorver como padrão normal de uso. **Como evitar:** manter uma única connection de longa duração por processo (como o `PublicadorDeEventos` acima), inicializada no startup da aplicação e reaproveitada por toda a vida do processo — channels, que são leves, podem ser abertos com mais liberdade quando o caso de uso realmente exigir isolamento por corrotina.

## Ack manual vs auto-ack: a decisão que decide se você perde mensagens

Todo o código acima ainda não respondeu a uma pergunta central: quando, exatamente, o RabbitMQ considera uma mensagem "processada" e a remove da fila?

> [!question]- Por que essa pergunta importa — a mensagem não some da fila assim que é entregue ao consumer?
> Não necessariamente, e essa é exatamente a diferença entre auto-ack e ack manual. Com **auto-ack**, sim — o RabbitMQ remove a mensagem da fila no instante em que a entrega ao consumer, antes mesmo do código começar a processá-la. Se o processo Python cair um milissegundo depois — exceção não tratada, `kill -9`, pod de Kubernetes reciclado no meio do processamento — a mensagem já não existe mais em lugar nenhum: não foi processada, e não pode ser reprocessada, porque o broker já a descartou. Com **ack manual**, a mensagem continua na fila, marcada como "entregue mas não confirmada" (*unacked*), até o código chamar `message.ack()` explicitamente depois de terminar o processamento com sucesso. Se o processo cair antes disso, o RabbitMQ detecta a queda da conexão/canal e devolve a mensagem para a fila — outro consumer (ou o mesmo, depois de reiniciar) pode processá-la de novo.

aio-pika expõe os dois modos. Auto-ack é ativado com `no_ack=True` — mais rápido, sem o custo de rede da confirmação, mas descartando a garantia de que a mensagem foi processada com sucesso:

```python
# auto-ack — a mensagem é removida da fila na entrega, não no processamento
async with queue.iterator(no_ack=True) as fila_iter:
    async for message in fila_iter:
        await processar_evento(message)  # se isto lançar exceção, a mensagem já se foi
```

Ack manual é o padrão (`no_ack=False`, o valor default) e exige que o código confirme explicitamente:

```python
async def processar_evento(message: aio_pika.abc.AbstractIncomingMessage) -> None:
    try:
        evento = json.loads(message.body)
        await despachar_notificacao(evento, message.routing_key)
        await message.ack()
    except Exception:
        logger.exception("Falha ao processar evento de notificação")
        await message.nack(requeue=False)  # não requeue — vai para a DLX, se configurada
```

`message.ack()` confirma que o processamento terminou com sucesso e a mensagem pode sair da fila. `message.nack(requeue=False)` faz o oposto explícito: rejeita a mensagem e instrui o broker a **não** devolvê-la para o início da mesma fila (o que causaria um loop infinito se o erro for determinístico, tipo um JSON malformado) — em vez disso, se a queue estiver configurada com uma Dead Letter Exchange, a mensagem é roteada para lá, para investigação posterior. Esse padrão de DLX, com código completo, é aprofundado na nota 07 deste galho; aqui o ponto é só que `ack`/`nack` são a interface pela qual o código de aplicação participa da decisão de durabilidade.

Existe ainda um terceiro caminho, um atalho conveniente para o caso feliz: o context manager `message.process()`, usado no exemplo mais simples da nota 01 deste galho, faz `ack()` automaticamente ao sair do bloco sem exceção, e `nack(requeue=True)` automaticamente se uma exceção escapar:

```python
async with message.process():
    evento = json.loads(message.body)
    await despachar_notificacao(evento, message.routing_key)
# ack() chamado aqui, automaticamente, se nada lançou exceção
```

`message.process()` é útil para o caso simples, mas esconde uma decisão que produção geralmente quer tomar explicitamente: o requeue automático em caso de exceção é exatamente o comportamento que causa loop infinito com poison messages — uma mensagem malformada que sempre lança a mesma exceção volta pro início da fila indefinidamente, sendo entregue, falhando, e voltando, sem nunca chegar a uma DLQ. É por isso que o exemplo do serviço de notificações acima usa `ack()`/`nack(requeue=False)` explícitos em vez de `message.process()` — o controle manual é mais verboso, mas é a versão que efetivamente decide o que fazer com uma falha permanente, em vez de aceitar o default do atalho.

```mermaid
%%{init: {"theme": "base", "themeVariables": {"primaryColor": "#4A90D9", "primaryBorderColor": "#2E5C8A", "lineColor": "#4A90D9"}}}%%
sequenceDiagram
    participant P as pagamentos-service
    participant EX as exchange (topic)
    participant Q as queue notificacoes.fila
    participant C as serviço de notificações

    P->>EX: publish(routing_key="pagamento.confirmado", body=JSON)
    EX->>Q: roteia via binding "pagamento.#"
    Q->>C: entrega mensagem (unacked)
    activate C
    C->>C: json.loads + despachar_notificacao()
    alt processamento OK
        C->>Q: message.ack()
        Q->>Q: remove mensagem da fila
    else exceção no processamento
        C->>Q: message.nack(requeue=False)
        Q->>Q: roteia para DLX (se configurada)
    end
    deactivate C
```

> [!warning] Esquecer o ack manual deixa mensagens presas como *unacked* para sempre
> **O que acontece:** um time escreve um consumer com `no_ack=False` (o padrão) mas o caminho de código que processa a mensagem tem um `return` antecipado, ou uma exceção capturada silenciosamente sem chamar `ack()` nem `nack()` — e semanas depois percebe, no RabbitMQ Management Plugin, que a fila tem centenas de mensagens *unacked* que nunca saem, mesmo com o consumer aparentemente "funcionando". **Por quê:** com ack manual, uma mensagem entregue e nunca confirmada (nem `ack`, nem `nack`) fica marcada como *unacked* indefinidamente enquanto o canal que a recebeu continuar aberto — ela não volta pra fila (porque a conexão não caiu) e não sai (porque ninguém confirmou). Isso normalmente escala junto com o `prefetch_count`: com prefetch alto, um bug de "esqueci de chamar ack" acumula rápido, porque o broker continua entregando novas mensagens até o limite de prefetch, mesmo com as anteriores travadas. **Como evitar:** estruturar o processamento sempre com `try/except` cobrindo **todo** o caminho até `ack()`, garantindo que toda mensagem recebida termine em `ack()` ou `nack()` — nunca em nenhum dos dois. Monitorar `unacked messages` no RabbitMQ Management Plugin (ou via `rabbitmq_prometheus`) é o sinal operacional mais direto de que esse bug está acontecendo; um número de unacked crescendo sem parar, mesmo com o consumer rodando, é o padrão clássico.

> [!tip] `prefetch_count` e ack manual são a mesma decisão vista de dois ângulos
> `prefetch_count` limita quantas mensagens não confirmadas um consumer pode ter em voo; ack manual é o mecanismo que confirma cada uma delas. Um `prefetch_count` alto sem disciplina de ack correto amplifica o dano de qualquer bug no caminho de confirmação — mais mensagens presas, mais rápido. Um bom ponto de partida em produção é `prefetch_count` igual à concorrência real de processamento do consumer (se ele processa uma mensagem por vez, `prefetch_count=1`; se processa várias `asyncio.gather`, um valor próximo a esse grau de paralelismo).

## Casos práticos

**Consumer com backpressure real via `asyncio.Semaphore`.** O serviço de notificações do cenário de abertura, sob carga real, recebe picos de eventos de pagamento durante promoções — centenas por segundo em rajadas curtas. Processar cada evento sequencialmente dentro do `async for` seria seguro, mas lento; disparar uma task por mensagem sem limite (`asyncio.create_task` por iteração) seria rápido, mas arriscaria estourar conexões simultâneas com o provedor de push notification. A solução combina o `prefetch_count` do canal com um `asyncio.Semaphore` do lado da aplicação — o mesmo padrão de back-pressure já coberto em profundidade em [[03-Dominios/Tecnologia/Python/Programação Reativa e Assíncrona/06 - Back-pressure — Semaphore, Queue com maxsize e buffering|Back-pressure]]:

```python
semaforo = asyncio.Semaphore(20)  # no máximo 20 notificações em voo por vez

async def processar_com_limite(message: aio_pika.abc.AbstractIncomingMessage) -> None:
    async with semaforo:
        await processar_evento(message)

async with queue.iterator() as fila_iter:
    async for message in fila_iter:
        asyncio.create_task(processar_com_limite(message))
```

`prefetch_count` no channel controla quantas mensagens o **broker** entrega sem confirmação; o `Semaphore` controla quantas o **código Python** processa concorrentemente ao mesmo tempo. Os dois números não precisam ser iguais, mas normalmente valem próximos — um `prefetch_count` muito maior que o semáforo só acumula mensagens entregues e esperando vez na memória do processo, sem ganho real de throughput.

**Publish com `routing_key` derivada de dados de negócio, não hardcoded.** Um erro sutil e comum: hardcoded routing keys espalhadas pelo código de cada produtor (`"pedido.criado"` digitado em três lugares diferentes, um deles com um typo silencioso tipo `"pedido.criad"`). Centralizar as routing keys conhecidas num só lugar — um `Enum` ou um módulo de constantes compartilhado entre os produtores, se eles vivem no mesmo monorepo, ou um contrato documentado versionado se vivem em repositórios separados — evita que um typo em produção crie silenciosamente um evento que nenhum binding existente casa (o AMQP não avisa quando uma mensagem publicada não casa com nenhum binding; ela é descartada silenciosamente, a menos que a exchange esteja configurada com `mandatory=True` e o publisher trate o retorno).

```python
from enum import StrEnum

class RoutingKey(StrEnum):
    PEDIDO_CRIADO = "pedido.criado"
    PEDIDO_CANCELADO = "pedido.cancelado"
    PAGAMENTO_CONFIRMADO = "pagamento.confirmado"
    PAGAMENTO_RECUSADO = "pagamento.recusado"
    CURSO_CONCLUIDO = "curso.concluido"

await publicar_evento(RoutingKey.PAGAMENTO_CONFIRMADO, {"pedido_id": cobranca.pedido_id})
```

**Escalando o consumidor com múltiplas réplicas, sem duplicar trabalho.** Conforme o volume de eventos cresce, o time sobe uma segunda réplica do serviço de notificações — dois processos Python independentes, cada um com sua própria connection, ambos declarando a mesma queue `notificacoes.fila` e chamando `queue.iterator()`. Isso não exige nenhuma configuração especial: como a queue já existe (declarar é idempotente), as duas réplicas se tornam automaticamente **competing consumers** — o RabbitMQ distribui as mensagens entre elas, cada mensagem indo para uma única réplica, respeitando o `prefetch_count` de cada canal. Uma dúvida comum nesse ponto é se é preciso avisar o RabbitMQ que agora existem "dois workers" — não é: o broker não sabe nem precisa saber quantas réplicas de aplicação existem, ele só sabe que há dois consumers conectados na mesma queue e round-robin entre eles (ajustado pelo prefetch de cada um, não estritamente round-robin puro se um consumer estiver mais lento que o outro). É o mesmo modelo de escalonamento horizontal que já se aplica a workers Celery — adicionar capacidade de processamento é rodar mais uma cópia do processo, sem tocar em código.

## Quando aio-pika vale a complexidade extra

A pergunta que fecha esta nota é a mesma que abriu a nota 01 do galho, respondida agora com o cenário completo na mão: **aio-pika compensa quando o problema é de roteamento, não de execução de tarefa**. O serviço de notificações deste cenário não podia ser resolvido bem com `.delay()` de Celery porque o requisito central — múltiplos produtores desacoplados, um consumidor decidindo via padrão de routing key o que lhe interessa, capacidade de adicionar um quarto ou quinto consumidor sem tocar em nenhum produtor existente — é estruturalmente o modelo exchange/binding do AMQP, não o modelo "chame esta função depois" de uma task queue.

O preço pago por esse ganho é real e cumulativo: nenhum retry automático (você decide `ack`/`nack` linha por linha), nenhuma garantia de idempotência de graça (se uma mensagem for reentregue depois de um `nack(requeue=True)` ou de uma queda de conexão, o handler pode rodar duas vezes — a mesma disciplina de at-least-once + idempotência já coberta para Celery na nota 03 deste galho se aplica aqui, sem exceção), e nenhum dashboard de aplicação pronto — a observabilidade vem do RabbitMQ Management Plugin, não de uma ferramenta como o Flower que entende o que é uma "tarefa". Escolher aio-pika só pelo fato de ser assíncrono, sem esse requisito real de roteamento multi-produtor ou controle fino de topologia, tende a recriar — com mais código escrito à mão — o que Celery já entrega configurando um decorator.

## Como explicar em inglês

> "aio-pika is an asynchronous AMQP client — it talks directly to RabbitMQ using asyncio, without any task abstraction on top. I reach for it when the problem is really about message routing between decoupled producers and consumers, not about running a background job. `connect_robust()` gives you automatic reconnection — if RabbitMQ restarts, the client reconnects and redeclares the exchange, queue, and bindings on its own, so a broker restart doesn't require manual recovery code. Publishing means declaring an exchange — often a topic exchange when you need pattern-based routing — and publishing a message with a routing key; consuming means declaring a queue, binding it to that exchange with the patterns you care about, and iterating messages with `async for message in queue.iterator()`. The decision that matters most in production is manual versus automatic acknowledgment: with manual ack, a message only leaves the queue after your code explicitly calls `message.ack()` — if the process crashes mid-processing, the message goes back to the queue instead of disappearing. The trade-off is that nothing comes for free: no automatic retry, no built-in idempotency, no dashboard — you own all of that, in exchange for full control over the broker."

| PT | EN |
|----|----|
| Reconexão automática | Automatic reconnection |
| Declarar exchange/queue/binding | Declare exchange/queue/binding |
| Chave de roteamento | Routing key |
| Confirmação manual | Manual acknowledgment (ack) |
| Confirmação automática | Automatic acknowledgment (auto-ack) |
| Mensagem não confirmada | Unacked message |
| Reentrega / reenfileiramento | Requeue |
| Iterador assíncrono | Async iterator |
| Controle de fluxo / limite de mensagens em voo | Prefetch / QoS |
| Rejeitar mensagem | Reject / nack message |

## O que vem a seguir

O serviço de notificações desta nota já roteia eventos de múltiplos produtores com controle explícito sobre confirmação — mas ainda falta a peça que Celery dava de graça e aio-pika deliberadamente não dá: retry estruturado e uma fila de erro dedicada para mensagens que falham de forma permanente.

- [[06 - kafka-python e aiokafka — producer e consumer|06 — kafka-python e aiokafka: producer e consumer]] — quando nem o modelo exchange/binding é suficiente porque o requisito real é replay e múltiplos consumer groups independentes lendo o mesmo log, não uma fila que remove a mensagem ao entregar.
- [[07 - Garantias de entrega na prática — DLQ e Outbox em Python|07 — Garantias de entrega na prática: DLQ e Outbox em Python]] — o `nack(requeue=False)` desta nota, levado a uma Dead Letter Exchange configurada de verdade, e o padrão Outbox aplicado com SQLAlchemy para garantir que o publish nunca fique dessincronizado da transação de negócio que o originou.
- [[03-Dominios/Tecnologia/Python/Programação Reativa e Assíncrona/07 - Padrões de produção com asyncio — supervisão de tasks, graceful shutdown, circuit breaker|Padrões de produção com asyncio]] — como supervisionar o consumer de longa duração desta nota dentro de um processo que também precisa desligar graciosamente sem perder mensagens em voo.

## Veja também

- [[01 - Panorama — Celery vs RQ vs aio-pika vs aiokafka|01 — Panorama: Celery vs RQ vs aio-pika vs aiokafka]] — por que aio-pika é uma categoria diferente de Celery/RQ, não "Celery mais difícil"
- [[03 - Celery em produção — retries, idempotência e Celery Beat|03 — Celery em produção: retries, idempotência e Celery Beat]] — a mesma disciplina de at-least-once + idempotência, aplicada primeiro ao Celery
- [[03-Dominios/Engenharia/Comunicação entre Sistemas/Mensageria/RabbitMQ|Comunicação entre Sistemas — RabbitMQ]] — o modelo AMQP completo (tipos de exchange, DLX, quorum queues, publisher confirms) que esta nota assume como pré-requisito
- [[03-Dominios/Tecnologia/Python/Programação Reativa e Assíncrona/index|Programação Reativa e Assíncrona]] — o `asyncio`/event loop que aio-pika usa por baixo, coberto com profundidade nos Galhos 7-8 desta trilha

## Fontes

- aio-pika docs — [*AsyncIO client for RabbitMQ*](https://aio-pika.readthedocs.io/) (acessado 2026-07-12) — `connect_robust()`, declaração de exchange/queue/binding, `queue.iterator()`, `message.process()`, ack/nack manual.
- RabbitMQ — [*AMQP 0-9-1 Model Explained*](https://www.rabbitmq.com/tutorials/amqp-concepts.html) (acessado 2026-07-12) — modelo exchange/binding/queue, tipos de exchange, referência conceitual usada nesta nota sem repetição.
- RabbitMQ — [*Reliability Guide*](https://www.rabbitmq.com/reliability.html) (acessado 2026-07-12) — publisher confirms, ack manual, durabilidade — a base conceitual por trás das decisões de código desta nota.
- RabbitMQ Tutorials — [*Reliable Publishing with Publisher Confirms*](https://www.rabbitmq.com/tutorials/tutorial-seven-python.html) (acessado 2026-07-12) — exemplo oficial em Python (via pika síncrono) do padrão de confirmação usado como referência para o equivalente assíncrono em aio-pika.
