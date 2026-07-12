---
title: "Panorama — Celery vs RQ vs aio-pika vs aiokafka"
created: 2026-07-12
type: concept
fase: Adepto
status: seedling
publish: true
tags:
  - python
  - mensageria
  - celery
  - rq
  - aio-pika
  - aiokafka
aliases:
  - "Ferramental Python de mensageria"
  - "Celery vs RQ"
  - "Task queue vs cliente de broker em Python"
---

# Panorama — Celery vs RQ vs aio-pika vs aiokafka

> [!abstract] TL;DR
> Python tem quatro famílias de ferramentas pra tirar trabalho do caminho síncrono de uma requisição, e elas não competem entre si — resolvem problemas diferentes. **Celery** é a task queue madura e abstrata: você marca uma função com `@app.task`, chama `.delay()`, e o framework cuida de serializar, enfileirar (sobre Redis ou RabbitMQ), rotear pra um worker e — se configurado — reexecutar em caso de falha. **RQ** faz a mesma coisa com uma fração da superfície: só Redis, API menor, menos mágica, mais fácil de ler o código-fonte inteiro num fim de tarde. **aio-pika** abandona a abstração de "tarefa": é um cliente assíncrono que fala AMQP direto com o RabbitMQ — você declara exchange, queue, binding, publica e consome, e implementa retry/idempotência com as próprias mãos. **aiokafka** (e sua prima síncrona `kafka-python`) não é task queue nenhuma: é cliente Kafka pra *event streaming* — múltiplos consumers lendo o mesmo log, não um único worker pegando uma tarefa e descartando-a. A pergunta que decide qual usar: você quer que **algo aconteça** em background (task queue: Celery/RQ) ou você quer **controle fino sobre um broker**, ou um **log de eventos que vários consumers leem** (comunicação direta: aio-pika/aiokafka)?

Um time está construindo a API de cadastro de uma plataforma de cursos. O fluxo de "criar conta" é direto: validar o formulário, gravar o usuário no banco, e mandar um e-mail de boas-vindas com um link de confirmação. No protótipo, o código é o que qualquer um escreveria primeiro:

```python
@app.post("/usuarios", status_code=201)
def criar_usuario(dados: CriarUsuarioDTO):
    usuario = repositorio.salvar(Usuario.criar(dados))
    enviar_email_boas_vindas(usuario.email)  # chama o servidor SMTP, aqui, agora
    return usuario
```

Funciona no ambiente de desenvolvimento, onde o servidor SMTP de teste responde em milissegundos. Em produção, contra o provedor de e-mail transacional real, `enviar_email_boas_vindas` leva entre 200ms e 2 segundos — às vezes mais, quando o provedor está sob carga. O handler HTTP, que devolveria `201 Created` em 15ms se só gravasse o usuário no banco, agora segura a conexão aberta esperando uma chamada de rede pra um serviço terceiro que **não tem nada a ver** com a pergunta "o usuário foi criado com sucesso?". Pior: se o SMTP cair ou responder devagar sob pico de tráfego, o cadastro inteiro trava — o serviço de terceiros virou, sem ninguém decidir isso deliberadamente, uma dependência crítica do caminho mais importante da aplicação.

A pergunta certa não é "como faço o envio de e-mail ficar mais rápido" — é **"por que o handler HTTP está esperando o SMTP responder, se a resposta HTTP não depende do resultado do e-mail?"**. O cliente que chamou `POST /usuarios` não precisa saber se o e-mail já foi entregue — precisa saber se a conta foi criada. Isso é o problema canônico que motiva desacoplar: tirar do caminho síncrono qualquer trabalho cujo resultado não faz parte do contrato imediato da resposta.

> [!question]- Por que não simplesmente rodar `enviar_email_boas_vindas` numa thread separada e devolver 201 na hora?
> Dá pra fazer isso com `threading.Thread` ou `asyncio.create_task` e resolve o sintoma imediato — a resposta HTTP não espera mais. Mas resolve mal: se o processo da API reiniciar (deploy, crash, autoscaling reduzindo réplicas) no meio da execução da thread, o e-mail simplesmente não é enviado, sem log, sem retry, sem ninguém sabendo. Não há persistência do "trabalho pendente" fora da memória do processo que o criou. É exatamente esse buraco — durabilidade, retry, e um processo separado que pode escalar independente da API — que motiva ferramental dedicado de mensageria em vez de um atalho de concorrência in-process. As notas seguintes deste galho (02, 03) tratam desse detalhe a fundo.

Esta nota é o mapa: quatro ferramentas, quatro respostas diferentes pra "e se eu não quiser mais esperar o SMTP responder", com o mesmo problema de e-mail de boas-vindas resolvido nas quatro, lado a lado, pra você comparar o código real, não só a descrição de marketing de cada uma.

## O eixo que decide: tarefa a executar vs fato a registrar

Antes de comparar ferramentas, vale nomear a pergunta que já foi respondida em profundidade — de forma agnóstica de linguagem — em [[03-Dominios/Engenharia/Comunicação entre Sistemas/4 - Comunicação assíncrona/02 - Message queue vs event streaming|Comunicação entre Sistemas — Message queue vs event streaming]]: você está lidando com uma **tarefa** (processe isso uma vez, o resultado importa pra quem pediu, depois pode esquecer) ou com um **fato** (aconteceu algo que potencialmente múltiplos serviços, hoje ou no futuro, vão querer ler)?

"Enviar e-mail de boas-vindas" é claramente uma tarefa: alguém pede, o trabalho acontece uma vez, ninguém precisa "reler" esse evento depois. É exatamente o caso de uso onde **task queues** — Celery e RQ — foram desenhadas pra brilhar: elas abstraem a fila por trás de uma API de "chame esta função depois", com retry, agendamento e resultado opcional embutidos.

Mas nem todo problema de desacoplamento em Python é uma tarefa fire-and-forget. Às vezes você precisa de controle fino sobre roteamento de mensagens (múltiplas filas, prioridades, exchanges do tipo topic) que a abstração de tarefa esconde de propósito — aí entra **aio-pika**, falando AMQP puro. E às vezes o que você tem não é uma tarefa, é um evento de negócio que três serviços diferentes (notificações, analytics, auditoria) precisam consumir de forma independente, com possibilidade de replay — aí a ferramenta certa não é task queue nenhuma, é um cliente Kafka: **aiokafka**.

```mermaid
%%{init: {"theme": "base", "themeVariables": {"primaryColor": "#4A90D9", "primaryBorderColor": "#2E5C8A", "lineColor": "#4A90D9"}}}%%
flowchart TD
    A["Preciso tirar trabalho<br/>do caminho síncrono"] --> B{"É uma tarefa a executar<br/>uma vez, com retry,<br/>ou um fato que múltiplos<br/>consumers vão reagir/reler?"}
    B -->|"Tarefa (fire-and-forget)"| C{"Já tem RabbitMQ<br/>na stack, ou precisa<br/>de scheduling maduro<br/>(Beat)?"}
    C -->|"Sim"| D["Celery<br/>(Redis ou RabbitMQ)"]
    C -->|"Não, só Redis,<br/>quero simplicidade"| E["RQ"]
    B -->|"Controle fino direto<br/>com o broker AMQP"| F["aio-pika<br/>(assíncrono, RabbitMQ)"]
    B -->|"Fato/evento — múltiplos<br/>consumer groups, replay"| G["aiokafka / kafka-python<br/>(event streaming)"]

    style D fill:#4A90D9,color:#fff
    style E fill:#4A90D9,color:#fff
    style F fill:#F5A623,color:#000
    style G fill:#F5A623,color:#000
```

**Resumo em uma frase:** se a pergunta é "quero que isso aconteça depois, sem me importar como", é task queue (Celery/RQ); se a pergunta é "quero falar com o broker diretamente, com controle total sobre roteamento ou sobre um log de eventos", é comunicação direta (aio-pika/aiokafka) — e essa segunda categoria não é "Celery mais difícil", é uma categoria de problema diferente.

## Celery — a task queue madura e abstrata

Celery existe desde 2009 e é, de longe, a task queue mais adotada no ecossistema Python — o framework padrão citado em qualquer discussão sobre background jobs em Django, FastAPI ou Flask ([Celery Project, *Celery: Distributed Task Queue*](https://docs.celeryq.dev/), 2026). A ideia central: você define uma função Python comum, decora com `@app.task`, e ganha de graça um jeito de chamá-la de forma assíncrona.

```python
# tasks.py
from celery import Celery

app = Celery("cursos", broker="redis://localhost:6379/0")

@app.task
def enviar_email_boas_vindas(email: str) -> None:
    smtp_client.enviar(
        destinatario=email,
        assunto="Bem-vindo!",
        corpo="Sua conta foi criada.",
    )
```

```python
# handler HTTP — mesma API, resolvendo o mesmo problema da abertura
@app.post("/usuarios", status_code=201)
def criar_usuario(dados: CriarUsuarioDTO):
    usuario = repositorio.salvar(Usuario.criar(dados))
    enviar_email_boas_vindas.delay(usuario.email)  # enfileira e retorna imediatamente
    return usuario
```

`.delay(usuario.email)` é açúcar sintático para `.apply_async(args=(usuario.email,))` — serializa os argumentos (JSON por padrão), publica uma mensagem no **broker** (Redis ou RabbitMQ) e retorna na hora, sem esperar a tarefa executar. Um processo **worker** completamente separado — rodando com `celery -A tasks worker`, tipicamente em outro contêiner ou outra máquina — puxa a mensagem da fila e executa `enviar_email_boas_vindas` de verdade.

> [!question]- Por que Celery precisa de um broker separado (Redis/RabbitMQ) em vez de gerenciar a fila internamente?
> Porque a fila precisa sobreviver ao processo que a criou. Se a API cair, reiniciar, ou escalar de 3 pra 10 réplicas, a fila de tarefas pendentes não pode estar amarrada à memória de um processo específico — ela vive num serviço externo, durável, que qualquer worker (de qualquer réplica, de qualquer host) pode consumir. É o mesmo motivo pelo qual thread in-process não resolve o problema descrito na abertura: sem um broker externo, "background" vira "só até o próximo restart".

O que o Celery abstrai por baixo:

- **Serialização** — argumentos e retorno viram JSON (ou pickle, msgpack — configurável) automaticamente; cuidado com objetos não serializáveis (conexões de banco, sessões HTTP) passados como argumento.
- **Roteamento** — `.apply_async(queue="emails")` manda a tarefa pra uma fila nomeada, permitindo workers dedicados por tipo de trabalho.
- **Agendamento** — `.apply_async(countdown=60)` ou `.apply_async(eta=daqui_a_uma_hora)` atrasa a execução sem código extra.
- **Resultado assíncrono** — se um *result backend* estiver configurado (Redis, banco), `AsyncResult` permite consultar o estado (`PENDING`, `SUCCESS`, `FAILURE`) e o retorno da tarefa depois.
- **Retry declarativo e Celery Beat** (tarefas periódicas, tipo cron) — cobertos com profundidade na nota 03 deste galho.

> [!tip] Celery não exige RabbitMQ
> É comum ver "Celery = RabbitMQ" em tutoriais antigos, mas desde as primeiras versões o Celery suporta Redis como broker — mais simples de operar quando você já usa Redis pra cache, e suficiente pra maioria dos casos que não precisam de roteamento AMQP avançado (exchanges topic/fanout). RabbitMQ continua sendo a escolha certa quando você precisa de garantias de entrega mais fortes ou roteamento complexo — ver a comparação de brokers em [[03-Dominios/Engenharia/Comunicação entre Sistemas/4 - Comunicação assíncrona/02 - Message queue vs event streaming|Message queue vs event streaming]].

Vale notar que a app Celery costuma crescer sua própria configuração central conforme o projeto amadurece — roteamento por padrão de nome de tarefa, timezone do Beat, serializer explícito em vez do padrão:

```python
app.conf.update(
    task_routes={"tasks.gerar_certificado": {"queue": "certificados"}},
    task_serializer="json",
    result_serializer="json",
    accept_content=["json"],
    timezone="America/Sao_Paulo",
)
```

Esse bloco de configuração central é normal e esperado — é onde a "mágica" do Celery vira explícita, e é também o primeiro lugar a olhar quando uma tarefa se comporta de forma inesperada em produção.

O preço da abstração: Celery tem uma superfície de configuração grande — result backend, serializer, `acks_late`, `task_reject_on_worker_lost`, `worker_prefetch_multiplier`, dezenas de outras opções — e depurar "por que essa tarefa não rodou" às vezes exige entender várias camadas (broker, worker, prefetch, roteamento) ao mesmo tempo. É o trade-off central do framework: você ganha muito de graça, mas quando algo foge do caminho feliz, o "muito" vira superfície de investigação.

## RQ — a fila simples sobre Redis

RQ (Redis Queue) nasceu como reação deliberada à complexidade do Celery: "simple job queues for Python", como o próprio projeto se descreve ([python-rq.org, *RQ: Simple job queues for Python*](https://python-rq.org/), 2026). A decisão de design mais importante do RQ é também sua maior limitação: **só funciona sobre Redis**, sem suporte a RabbitMQ ou outro broker.

```python
# tasks.py — mesma função, sem decorator nenhum
def enviar_email_boas_vindas(email: str) -> None:
    smtp_client.enviar(
        destinatario=email,
        assunto="Bem-vindo!",
        corpo="Sua conta foi criada.",
    )
```

```python
# handler HTTP
from redis import Redis
from rq import Queue

fila = Queue(connection=Redis())

@app.post("/usuarios", status_code=201)
def criar_usuario(dados: CriarUsuarioDTO):
    usuario = repositorio.salvar(Usuario.criar(dados))
    fila.enqueue(enviar_email_boas_vindas, usuario.email)  # sem decorator na função
    return usuario
```

A diferença mais visível de cara: `enviar_email_boas_vindas` **não precisa de decorator** nenhum — é uma função Python comum, e quem decide que ela vira um job é quem chama `fila.enqueue(...)`. Isso é uma escolha deliberada de design: qualquer função *importável* (não uma lambda, não um método de instância sem cuidado extra) pode ser enfileirada, sem acoplar o módulo da tarefa a um objeto `app` do Celery.

O worker roda com `rq worker` (lendo a fila padrão) e executa cada job num processo filho — por padrão, um fork por job, o que isola falhas (um job que trava a memória não derruba os próximos) ao custo de mais overhead que o modelo de pool de threads/processos do Celery.

> [!warning] RQ não tem retry automático sofisticado nem scheduling nativo maduro
> **O que acontece:** um time troca Celery por RQ esperando o mesmo comportamento de retry (`autoretry_for`, backoff exponencial) e tarefas periódicas (Beat) — e descobre, em produção, que RQ trata isso como responsabilidade da aplicação, não do framework.
> **Por quê:** é a decisão de design central do RQ — menos "mágica" significa menos features embutidas. RQ tem um decorator `@job` opcional pra retry simples desde versões recentes, e o pacote irmão `rq-scheduler` cobre agendamento, mas nenhum dos dois tem a profundidade das opções nativas do Celery (`retry_backoff_max`, `retry_jitter`, cron completo via Beat).
> **Como evitar:** decidir *antes* se o projeto vai precisar de retry com backoff sofisticado e agendamento tipo-cron nativo — se sim, Celery paga esse investimento inicial maior; se o projeto é pequeno e a maior parte dos jobs é fire-and-forget simples, a simplicidade do RQ (menos infraestrutura, código mais fácil de ler do início ao fim numa tarde) compensa.

O ganho real do RQ não é performance nem features — é **debugabilidade**. A base de código do RQ é pequena o suficiente pra ler inteira; quando uma tarefa se comporta de forma inesperada, dá pra rastrear o caminho completo (enqueue → serialização → worker → execução) sem precisar entender uma dúzia de camadas de configuração. Times pequenos, ou projetos onde a complexidade operacional do Celery (result backend, roteamento multi-fila, Beat) não se paga, tendem a preferir RQ justamente por isso.

## aio-pika — falando AMQP direto, sem abstração de tarefa

Celery e RQ têm algo em comum apesar das diferenças: os dois escondem o broker atrás de uma API de "tarefa". Você nunca declara uma exchange, nunca faz um binding manual, nunca decide o nome exato de uma fila — o framework decide isso por você. **aio-pika** joga essa abstração fora deliberadamente: é um cliente **assíncrono** (`asyncio`) que fala o protocolo AMQP 0-9-1 direto com o RabbitMQ, dando acesso total aos conceitos do broker — exchange, queue, binding, routing key — sem nenhuma camada de "tarefa" no meio ([aio-pika docs, *AsyncIO client for RabbitMQ*](https://aio-pika.readthedocs.io/), 2026).

```python
import aio_pika

async def enviar_email_boas_vindas(email: str) -> None:
    connection = await aio_pika.connect_robust("amqp://guest:guest@localhost/")
    async with connection:
        channel = await connection.channel()
        exchange = await channel.declare_exchange("emails", aio_pika.ExchangeType.DIRECT)
        await exchange.publish(
            aio_pika.Message(body=email.encode()),
            routing_key="boas-vindas",
        )
```

```python
# handler HTTP — assíncrono, precisa de um framework async (FastAPI, por exemplo)
@app.post("/usuarios", status_code=201)
async def criar_usuario(dados: CriarUsuarioDTO):
    usuario = await repositorio.salvar(Usuario.criar(dados))
    await enviar_email_boas_vindas(usuario.email)  # publica e retorna, não é "delay"
    return usuario
```

Note a diferença estrutural: não existe `.delay()`. Você abre uma conexão, declara (ou referencia) uma exchange, e publica uma mensagem com uma routing key — os mesmos conceitos cobertos, de forma agnóstica de linguagem, em [[03-Dominios/Engenharia/Comunicação entre Sistemas/Mensageria/index|Comunicação entre Sistemas — Mensageria]]. `connect_robust()` é a função mais citada da biblioteca: abre uma conexão com **reconexão automática** — se o RabbitMQ cair e voltar, o cliente reconecta e redeclara topologia sozinho, o que evita boa parte do código de resiliência que você teria que escrever à mão com um cliente AMQP mais cru.

O lado consumidor é igualmente direto:

```python
async def consumir_emails():
    connection = await aio_pika.connect_robust("amqp://guest:guest@localhost/")
    async with connection:
        channel = await connection.channel()
        await channel.set_qos(prefetch_count=10)
        queue = await channel.declare_queue("fila-emails", durable=True)

        async with queue.iterator() as fila_iter:
            async for mensagem in fila_iter:
                async with mensagem.process():  # ack automático ao sair do bloco
                    smtp_client.enviar(destinatario=mensagem.body.decode(), ...)
```

> [!warning] Com aio-pika, retry e idempotência são seu problema
> **O que acontece:** um time migra de Celery pra aio-pika esperando manter o mesmo comportamento de retry automático em caso de falha — e descobre que, sem o decorator `@app.task` e as opções `autoretry_for`/`retry_backoff` do Celery, nada reenvia a mensagem sozinho.
> **Por quê:** é exatamente a troca que motiva escolher aio-pika em primeiro lugar — controle total sobre o comportamento do broker significa que **nenhum** comportamento vem de graça. Se `mensagem.process()` levantar uma exceção, cabe ao código decidir se faz `nack` com requeue, publica numa dead-letter queue, ou descarta.
> **Como evitar:** só optar por aio-pika quando o controle fino (routing complexo, prioridades, protocolos além de "task simples") vale o código extra de gerenciar retry e confirmação manualmente — a nota 07 deste galho mostra DLQ e idempotência aplicados com código real.

`async`/`await` aqui pressupõe familiaridade com o modelo de concorrência do `asyncio` — event loop, corrotinas, `async with` — já coberto nos Galhos 7-8 desta trilha e não reexplicado aqui; aio-pika só *usa* esse modelo, não o reensina.

## aiokafka e kafka-python — não é task queue, é event streaming

A quarta ferramenta muda de categoria inteira. `kafka-python` (cliente síncrono) e `aiokafka` (cliente assíncrono, `asyncio`-nativo) falam com o Apache Kafka — e Kafka não é um broker de tarefas, é um **log de eventos** ([aiokafka docs, *aiokafka: AsyncIO Kafka client*](https://aiokafka.readthedocs.io/), 2026). A diferença de propósito em relação a Celery/RQ/aio-pika não é sutil: aqui, uma mensagem publicada não desaparece ao ser consumida — ela fica no log, e múltiplos **consumer groups** independentes podem lê-la, cada um no seu próprio ritmo, com replay disponível.

Se o problema fosse só "enviar o e-mail de boas-vindas", Kafka seria uma escolha estranha — over-engineering pra uma tarefa simples de fire-and-forget. O cenário onde aiokafka faz sentido é diferente: **múltiplos serviços reagindo ao mesmo fato**. Suponha que "usuário criado" não deva só disparar um e-mail — deva também alimentar um pipeline de analytics e um serviço de recomendação de cursos, cada um lendo o evento de forma independente, e potencialmente reprocessando o histórico depois:

```python
from aiokafka import AIOKafkaProducer
import json

async def publicar_usuario_criado(usuario: Usuario) -> None:
    producer = AIOKafkaProducer(bootstrap_servers="localhost:9092")
    await producer.start()
    try:
        evento = {"tipo": "usuario_criado", "email": usuario.email, "id": str(usuario.id)}
        await producer.send_and_wait("usuarios.eventos", json.dumps(evento).encode())
    finally:
        await producer.stop()
```

```python
# handler HTTP
@app.post("/usuarios", status_code=201)
async def criar_usuario(dados: CriarUsuarioDTO):
    usuario = await repositorio.salvar(Usuario.criar(dados))
    await publicar_usuario_criado(usuario)  # publica um FATO, não agenda uma tarefa
    return usuario
```

Do lado consumidor, o serviço de e-mail e o serviço de analytics são **dois consumer groups separados**, lendo o mesmo tópico sem interferir um no outro:

```python
from aiokafka import AIOKafkaConsumer
import json

async def consumir_para_emails():
    consumer = AIOKafkaConsumer(
        "usuarios.eventos",
        bootstrap_servers="localhost:9092",
        group_id="servico-emails",  # offset independente do grupo de analytics
    )
    await consumer.start()
    try:
        async for msg in consumer:
            evento = json.loads(msg.value)
            smtp_client.enviar(destinatario=evento["email"], ...)
    finally:
        await consumer.stop()
```

Trocar `group_id="servico-emails"` por `group_id="servico-analytics"` num segundo consumer, rodando em outro processo, é o bastante pra criar um segundo leitor completamente independente do mesmo stream — sem fila, sem competing consumers, sem coordenação entre os dois times. Isso é estruturalmente impossível de replicar com Celery/RQ sem reinventar um log por baixo, porque task queue *remove* a mensagem ao consumir; log *não remove*.

> [!question]- Por que existem kafka-python (síncrono) e aiokafka (assíncrono) como bibliotecas separadas?
> `kafka-python` é o cliente Kafka mais antigo e estabelecido no ecossistema — API bloqueante, direta, sem depender de `asyncio`. `aiokafka` nasceu depois, especificamente pra aplicações que já rodam num event loop assíncrono (um servidor FastAPI, por exemplo) e não podem bloquear a thread do loop com chamadas de rede síncronas — bloquear o event loop numa aplicação `async def` derruba a concorrência de toda a aplicação, não só do handler que fez a chamada. A escolha entre as duas segue a mesma regra de qualquer biblioteca de I/O em Python: se a aplicação é `async`, use a versão `async`; se é uma aplicação síncrona tradicional (Django clássico, um script batch), `kafka-python` evita a complexidade de rodar um event loop só pra isso.

Conceitos como partição, consumer group, offset, e a distinção formal entre fila e streaming **não são reexplicados aqui** — moram em [[03-Dominios/Engenharia/Comunicação entre Sistemas/4 - Comunicação assíncrona/02 - Message queue vs event streaming|Message queue vs event streaming]] e em [[03-Dominios/Engenharia/Comunicação entre Sistemas/Mensageria/index|Comunicação entre Sistemas — Mensageria]]; esta nota assume que o modelo mental já está claro e foca em como o Python fala com ele. A nota 06 deste galho aprofunda `KafkaProducer`/`KafkaConsumer` síncronos vs `AIOKafkaProducer`/`AIOKafkaConsumer`, commit de offset manual vs automático, e (de)serialização.

## Instalação mínima

Antes de comparar código de aplicação, vale ver o que cada ferramenta exige só para existir no projeto — a diferença de superfície já aparece aqui, antes de qualquer linha de lógica de negócio.

```bash
# Celery — broker Redis (mais simples de operar que RabbitMQ para começar)
pip install celery[redis]
```

```bash
# RQ — só Redis, sem opção de outro broker
pip install rq
```

```bash
# aio-pika — cliente AMQP assíncrono
pip install aio-pika
```

```bash
# aiokafka — cliente Kafka assíncrono; kafka-python é a alternativa síncrona
pip install aiokafka
```

Nos quatro casos o broker em si (Redis, RabbitMQ, Kafka) roda como serviço externo — nenhuma das bibliotecas embute um broker; `pip install` só traz o cliente. Para desenvolvimento local, subir o broker via `docker compose` (uma imagem `redis:7`, `rabbitmq:4-management` ou `apache/kafka:4.0`) é o caminho mais rápido — os brokers em si, com profundidade, estão cobertos em [[03-Dominios/Engenharia/Comunicação entre Sistemas/Mensageria/index|Comunicação entre Sistemas — Mensageria]], não aqui.

| Ferramenta | Pacote PyPI | Depende de |
|---|---|---|
| Celery | `celery[redis]` ou `celery[librabbitmq]` | Redis **ou** RabbitMQ (externo) |
| RQ | `rq` | Redis (externo) |
| aio-pika | `aio-pika` | RabbitMQ (externo) |
| aiokafka | `aiokafka` | Kafka (externo) |

> [!question]- Preciso instalar um "servidor" separado para cada ferramenta, ou dá pra reaproveitar Redis para tudo?
> Se o projeto já usa Redis (para cache, por exemplo), Celery e RQ podem reaproveitar essa mesma instância como broker — não é preciso um Redis dedicado, embora seja boa prática isolar bancos lógicos (`redis://.../0` para cache, `redis://.../1` para fila) para não misturar chaves de propósitos diferentes na mesma instância. aio-pika e aiokafka, por outro lado, exigem RabbitMQ e Kafka respectivamente — não há como "reaproveitar" Redis para eles, porque o protocolo e o modelo de dados são incompatíveis com o que Redis oferece nativamente.

## Comparando o código lado a lado

O mesmo problema — "criar usuário, desacoplar o envio de e-mail do handler HTTP" — resolvido nas quatro ferramentas, resumido:

| Ferramenta | Chamada no handler | O que acontece por baixo |
|---|---|---|
| Celery | `enviar_email_boas_vindas.delay(usuario.email)` | Serializa, publica no broker (Redis/RabbitMQ), worker separado executa; retry/agendamento/resultado de graça |
| RQ | `fila.enqueue(enviar_email_boas_vindas, usuario.email)` | Publica no Redis (só Redis); worker faz fork por job; retry e scheduling exigem extensões |
| aio-pika | `await exchange.publish(msg, routing_key=...)` | Publica direto numa exchange AMQP; você declara topologia, gerencia ack/retry manualmente |
| aiokafka | `await producer.send_and_wait("usuarios.eventos", evento)` | Anexa ao log Kafka; múltiplos consumer groups leem de forma independente, com replay |

## Tabela de decisão

| Critério | Celery | RQ | aio-pika | aiokafka |
|---|---|---|---|---|
| Modelo mental | Task queue | Task queue | Cliente AMQP direto | Cliente de log/streaming |
| Broker(s) | Redis ou RabbitMQ | Só Redis | RabbitMQ | Kafka |
| Abstração de "tarefa" | Sim (`@app.task`) | Sim (função comum + `enqueue`) | Não — você fala com exchange/queue | Não — você publica/consome eventos |
| Retry automático | Sim, configurável (`autoretry_for`) | Básico (`@job`, extensões) | Manual | Manual (nível de aplicação) |
| Scheduling nativo | Sim (Celery Beat) | Só com `rq-scheduler` | Não | Não |
| Múltiplos consumers independentes do mesmo dado | Não (competing consumers) | Não (competing consumers) | Não, por padrão AMQP | Sim (consumer groups) |
| Replay de histórico | Não | Não | Não | Sim |
| Curva de aprendizado / superfície | Média-alta | Baixa | Média (exige conhecer AMQP) | Média-alta (exige conhecer Kafka) |
| Caso de uso canônico | Background jobs em geral, envio de e-mail/notificação, processamento pesado | Mesmo que Celery, projetos menores, times que preferem menos "mágica" | Roteamento complexo, controle fino, RPC assíncrono | Event-driven architecture, analytics, auditoria, CDC |

> [!tip] A pergunta de uma frase
> "Quero que algo aconteça em background, sem me importar como" → task queue (Celery se precisar de RabbitMQ/scheduling maduro; RQ se só tem Redis e quer simplicidade). "Quero controle fino sobre o broker, ou um log de eventos que múltiplos serviços leem de forma independente" → comunicação direta (aio-pika pra RabbitMQ; aiokafka pra Kafka).

## Casos práticos

**A mesma plataforma de cursos, seis meses depois.** O time do exemplo de abertura resolveu o problema do e-mail de boas-vindas com Celery sobre Redis — decisão correta para o volume da época, umas centenas de cadastros por dia. O produto cresce, e agora existem três tipos de trabalho em background rodando na mesma instalação Celery: envio de e-mail transacional (rápido, alto volume), geração de certificado em PDF ao concluir um curso (lento, CPU-bound, minutos em vez de segundos), e um relatório semanal de progresso por e-mail (agendado, uma vez por semana, para toda a base de alunos). Rodar os três tipos de tarefa no mesmo pool de workers é um erro sutil: um pico de geração de certificados no fim do mês pode saturar os workers e atrasar e-mails transacionais que deveriam ser quase instantâneos. A correção não muda de ferramenta — usa uma capacidade que já está lá: `.apply_async(queue="certificados")` roteia a tarefa pesada para uma fila nomeada, e um segundo grupo de workers (`celery -A tasks worker -Q certificados`) é dedicado só a ela, isolando o impacto. O relatório semanal usa Celery Beat, cravado com profundidade na nota 03. Nenhuma dessas três necessidades — roteamento por fila, isolamento de workers, agendamento — exigiu trocar de ferramenta; exigiu usar mais da superfície que o Celery já oferece.

**Integração com um parceiro de pagamento via webhook.** Um serviço de pagamentos externo notifica a aplicação, via HTTP, quando uma cobrança é confirmada ou recusada — e o contrato do parceiro exige responder `200 OK` em menos de 3 segundos, sob pena de reenvio automático (e, depois de N reenvios, suspensão temporária do endpoint). Só gravar o evento no banco e devolver 200 já resolveria o requisito de latência, mas o processamento real — atualizar o status do pedido, notificar o cliente, disparar a nota fiscal — tem múltiplos passos, alguns deles chamando outros serviços internos que também podem falhar e precisar de retry independente. Esse é um caso onde aio-pika compensa o código extra: o handler do webhook só valida a assinatura e publica um evento cru numa exchange (`pagamentos.eventos`, tipo `topic`), com routing keys diferentes por tipo de evento (`pagamento.confirmado`, `pagamento.recusado`). Consumers dedicados — um para atualização de pedido, outro para nota fiscal — assinam bindings diferentes da mesma exchange, cada um com sua própria política de retry e sua própria dead-letter queue. Celery resolveria a parte de "rodar isso depois", mas o roteamento por tipo de evento para múltiplos consumers especializados, cada um com sua fila de erro isolada, é exatamente o cenário onde falar AMQP diretamente compensa o controle extra.

**Rastreamento de eventos de aprendizado para dois times diferentes.** A mesma plataforma de cursos introduz um requisito novo: cada interação relevante do aluno (assistiu um vídeo até o fim, completou um exercício, abandonou um módulo no meio) deve alimentar dois sistemas completamente independentes — o motor de recomendação de próximos cursos (lê o histórico completo, batch, uma vez por dia) e um dashboard de analytics em tempo quase real para o time de conteúdo (lê o evento assim que acontece). Modelar isso como tarefas Celery — uma tarefa "processar evento" — funcionaria para *um* dos dois consumidores, mas não para os dois ao mesmo tempo sem truques (publicar duas tarefas idênticas toda vez que um evento acontece, o que acopla quem produz o evento a saber quantos e quais consumidores existem hoje). Isso é o sinal clássico de que o problema mudou de categoria: não é mais "execute isso uma vez", é "registre este fato para quem quiser ler, hoje ou daqui a meses" — o motor de recomendação inclusive quer reprocessar o histórico completo sempre que o algoritmo mudar, o que é replay de verdade. aiokafka resolve isso naturalmente: um único `producer.send()` por evento de aprendizado, publicado no tópico `aprendizado.eventos`, com dois consumer groups (`motor-recomendacao` e `dashboard-analytics`) lendo o mesmo stream de forma totalmente independente — nenhum dos dois sabe que o outro existe, e um terceiro consumidor pode aparecer amanhã sem que o código que publica o evento mude uma linha.

## Armadilhas comuns

> [!warning] Usar Celery para um caso de event streaming
> **O que acontece:** um time modela "usuário criado" como uma tarefa Celery (`publicar_usuario_criado.delay(...)`) mesmo sabendo que três serviços diferentes (e-mail, analytics, recomendação) precisam reagir ao mesmo evento — e descobre depois que Celery entrega a tarefa a **um** worker, não a três.
> **Por quê:** Celery é, por baixo, uma fila de competing consumers — cada mensagem vai pra um worker só, o mesmo modelo de "message queue" descrito em [[03-Dominios/Engenharia/Comunicação entre Sistemas/4 - Comunicação assíncrona/02 - Message queue vs event streaming|Message queue vs event streaming]]. Simular fan-out com Celery exige truques (publicar N tarefas, uma por consumidor conhecido) que ficam frágeis assim que um quinto serviço precisa começar a reagir ao mesmo evento sem que o código que publica precise saber disso.
> **Como evitar:** nomear explicitamente, antes de escrever código, se o cenário é "uma tarefa, um executor" (task queue) ou "um fato, N leitores independentes, possivelmente no futuro" (streaming) — a resposta decide entre Celery/RQ e aiokafka antes de qualquer linha de implementação.

> [!warning] Escolher aio-pika achando que é "Celery mais rápido"
> **O que acontece:** um time troca Celery por aio-pika esperando ganhar performance, e se surpreende com o volume de código novo — declarar exchange, gerenciar reconexão, implementar retry manual — pra reproduzir o que o Celery já fazia de graça.
> **Por quê:** aio-pika não é uma versão mais rápida do Celery — é uma ferramenta de categoria diferente, que troca conveniência por controle. Ganha-se em previsibilidade e em acesso a recursos do AMQP que o Celery não expõe (roteamento topic/fanout complexo, prioridade nativa de fila), mas perde-se tudo que o Celery abstrai.
> **Como evitar:** só escolher aio-pika quando o motivo for controle explícito sobre o broker — não performance genérica, que Celery sobre Redis já entrega bem pra volume moderado.

> [!warning] Achar que RQ é "Celery com menos funcionalidade" e nada mais
> **O que acontece:** um time avalia RQ só pela lista de features que falta (sem Beat robusto, sem múltiplos brokers) e descarta sem considerar o ganho real, que é debugabilidade e simplicidade operacional.
> **Por quê:** a comparação "quantas features tem" ignora o custo operacional de manter e depurar a superfície do Celery quando o projeto não precisa da maior parte dela — result backend configurado sem uso real, roteamento multi-fila que nunca é usado, opções de retry nunca ajustadas do padrão.
> **Como evitar:** avaliar RQ pelo que o projeto de fato precisa hoje, não pela lista de features do concorrente — projetos pequenos a médios, com Redis já na stack, ganham mais em simplicidade do que perdem em features não usadas.

## Observabilidade: como saber que a tarefa realmente rodou

Um problema que aparece igual nas quatro ferramentas, embora resolvido de formas diferentes: depois que o handler HTTP devolve `201` e segue em frente, como alguém descobre que `enviar_email_boas_vindas` de fato executou — ou falhou silenciosamente?

- **Celery** tem o ecossistema mais maduro nesse ponto: **Flower**, um dashboard web (`pip install flower`, `celery -A tasks flower`) mostra tarefas em tempo real, taxa de sucesso/falha, tempo de execução por worker, e permite inspecionar o traceback de uma tarefa que falhou — sem precisar caçar logs espalhados. É o mesmo tipo de ganho que motiva escolher Celery em primeiro lugar: muita coisa vem de graça, aqui incluindo visibilidade operacional.
- **RQ** tem o `rq-dashboard`, um projeto irmão bem mais simples que o Flower — lista de filas, jobs em andamento, jobs falhados com traceback. Cobre o essencial sem a profundidade de métricas do Flower, consistente com a filosofia geral do RQ.
- **aio-pika** não tem dashboard de aplicação — a visibilidade vem do **RabbitMQ Management Plugin**, que mostra filas, taxa de mensagens, consumers conectados, mas não sabe nada sobre "tarefas" ou o que uma mensagem representa semanticamente. Rastrear se um e-mail específico foi enviado com sucesso é responsabilidade do código da aplicação — normalmente via logging estruturado e métricas próprias (Prometheus, por exemplo).
- **aiokafka** também depende de ferramentas externas ao cliente Python — Kafka expõe métricas de lag de consumer group (quão atrás um consumer group está do fim do log), essenciais para saber se um serviço está processando eventos no ritmo em que são produzidos, mas essas métricas vêm do broker e de ferramentas de operação (Kafka Manager, Prometheus JMX Exporter), não de uma biblioteca Python.

> [!tip] O padrão gera menos observabilidade de graça, não mais controle sobre observabilidade
> É tentador ler "aio-pika e aiokafka dão mais controle" como "e, portanto, mais fácil de observar" — é o oposto. Controle fino sobre o broker significa que a aplicação também é responsável por instrumentar o que a task queue instrumentaria de graça. Isso não é motivo para nunca escolher aio-pika/aiokafka, mas é um custo real a somar na decisão, não só o custo de escrever mais código de publish/consume.

## Em entrevista

Uma pergunta comum em entrevistas sênior que tocam sistemas Python é "como você desacoplaria uma chamada lenta (SMTP, terceiros) do caminho de resposta de uma API?". A resposta que sinaliza profundidade não pula direto pro nome de uma ferramenta — nomeia primeiro a categoria do problema: "primeiro eu pergunto se é uma tarefa fire-and-forget ou um evento que múltiplos serviços vão consumir de forma independente. Se for tarefa, uso uma task queue — Celery se já preciso de scheduling maduro ou RabbitMQ, RQ se o projeto é menor e só tem Redis disponível. Se for um evento que outros serviços vão reagir de forma independente, ou que preciso poder reprocessar depois, isso já não é task queue — é streaming, e eu uso um cliente Kafka como aiokafka. Confundir os dois é o erro mais comum que vejo: gente tentando fazer fan-out de evento com uma fila que só entrega a mensagem pra um consumer."

## Como explicar em inglês

> "Python has two categories of tools for taking work off the synchronous request path. Task queues — Celery and RQ — abstract the broker behind a 'run this function later' API: you decorate or enqueue a function, and the framework handles serialization, routing to a worker, and often retry and scheduling. Celery supports both Redis and RabbitMQ as brokers and has a mature feature set — retries, periodic tasks via Celery Beat, result backends. RQ deliberately trades features for simplicity: Redis-only, a smaller codebase you can read end-to-end, less magic to debug. The other category is direct broker communication — aio-pika talks AMQP straight to RabbitMQ with no task abstraction, giving you full control over exchanges and routing at the cost of implementing retry and idempotency yourself. aiokafka is a different category entirely — it's an event streaming client, not a task queue, so instead of one worker consuming and discarding a message, multiple independent consumer groups can read the same event log, with replay available. The decision isn't 'which is faster' — it's 'do I want a task to happen once, or do I want a fact multiple services can react to independently?'"

| PT | EN |
|----|----|
| Fila de tarefas | Task queue |
| Trabalhador / consumidor | Worker |
| Corretor / broker | Broker |
| Serialização | Serialization |
| Tentativa automática | Automatic retry |
| Tarefa agendada / periódica | Scheduled / periodic task |
| Backend de resultado | Result backend |
| Cliente assíncrono | Asynchronous client |
| Grupo de consumidores | Consumer group |
| Reprocessamento | Replay |

## O que vem a seguir

Este panorama respondeu "qual ferramenta pra qual problema" — as próximas notas do galho entram fundo em cada uma. A ordem segue a mesma lógica desta nota: primeiro as duas task queues (Celery com profundidade, depois RQ em contraste direto), depois os dois clientes de broker direto.

- [[02 - Celery fundamentos — broker, worker e tasks|02 — Celery fundamentos: broker, worker e tasks]] — a arquitetura completa por trás do `.delay()` usado aqui: `@shared_task`, `.apply_async()`, `AsyncResult`, serialização.
- [[03 - Celery em produção — retries, idempotência e Celery Beat|03 — Celery em produção: retries, idempotência e Celery Beat]] — o que falta pra rodar Celery de verdade em produção, incluindo a idempotência que esta nota só menciona.
- [[04 - RQ — a fila simples sobre Redis|04 — RQ: a fila simples sobre Redis]] — RQ com profundidade, contraste ponto a ponto com Celery.
- [[05 - aio-pika — RabbitMQ assíncrono|05 — aio-pika: RabbitMQ assíncrono]] — `connect_robust()`, declaração de topologia, publish/consume com profundidade.
- [[06 - kafka-python e aiokafka — producer e consumer|06 — kafka-python e aiokafka: producer e consumer]] — commit de offset, consumer groups, (de)serialização.
- [[07 - Garantias de entrega na prática — DLQ e Outbox em Python|07 — Garantias de entrega na prática: DLQ e Outbox em Python]] — o retry manual que esta nota deixou como exercício para aio-pika, resolvido com DLQ e Outbox reais.

## Veja também

- [[03-Dominios/Tecnologia/Python/Mensageria/index|Mensageria (MOC do galho)]]
- [[03-Dominios/Engenharia/Comunicação entre Sistemas/4 - Comunicação assíncrona/02 - Message queue vs event streaming|Comunicação entre Sistemas — Message queue vs event streaming]] — a distinção conceitual fila vs streaming, agnóstica de linguagem, que fundamenta a escolha entre as quatro ferramentas
- [[03-Dominios/Engenharia/Comunicação entre Sistemas/Mensageria/index|Comunicação entre Sistemas — Mensageria]] — Kafka e RabbitMQ como brokers, arquitetura interna
- [[03-Dominios/Tecnologia/Java/Mensageria/06 - Spring para mensageria — o panorama|Java — Spring para mensageria: o panorama]] — o mesmo papel de nota-panorama, ferramental do ecossistema Spring
- [[03-Dominios/Tecnologia/Python/Programação Reativa e Assíncrona/index|Programação Reativa e Assíncrona]] — `asyncio`/event loop, usado por aio-pika e aiokafka

## Fontes

- Celery Project — [*Celery: Distributed Task Queue*](https://docs.celeryq.dev/) (acessado 2026-07-12) — arquitetura de broker/worker, `.delay()`/`.apply_async()`, serialização, result backend.
- python-rq.org — [*RQ: Simple job queues for Python*](https://python-rq.org/) (acessado 2026-07-12) — filosofia de design "simples sobre Redis", `enqueue()`, workers.
- aio-pika docs — [*AsyncIO client for RabbitMQ*](https://aio-pika.readthedocs.io/) (acessado 2026-07-12) — `connect_robust()`, declaração de exchange/queue/binding, publish/consume assíncrono.
- aiokafka docs — [*aiokafka: AsyncIO Kafka client*](https://aiokafka.readthedocs.io/) (acessado 2026-07-12) — `AIOKafkaProducer`/`AIOKafkaConsumer`, consumer groups, comparação com `kafka-python`.
- Real Python — [*Task Queues in Python*](https://realpython.com/python-celery-workers/) (acessado 2026-07-12) — panorama de task queues Python, comparação Celery vs alternativas.
