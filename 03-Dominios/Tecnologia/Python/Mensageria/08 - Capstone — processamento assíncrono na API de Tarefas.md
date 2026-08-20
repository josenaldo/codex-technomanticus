---
title: "Capstone — processamento assíncrono na API de Tarefas"
created: 2026-07-12
type: concept
fase: magus
status: complete
publish: true
tags:
  - python
  - mensageria
  - capstone
aliases:
  - "Capstone Galho 14 Python"
  - "Outbox e Domain Event na API de Tarefas"
  - "Fechamento do galho Mensageria"
---

# Capstone — processamento assíncrono na API de Tarefas

> [!abstract] TL;DR
> A [[03-Dominios/Tecnologia/Python/Arquitetura e Design Patterns/08 - Capstone — refatorando a API de Tarefas pra arquitetura hexagonal|capstone do Galho 13]] deixou a API de Tarefas arquiteturalmente pronta pra crescer — domínio puro, Repository, Unit of Work, Service Layer, Ports and Adapters — mas ainda **100% síncrona** num ponto crítico: quando o usuário conclui uma tarefa, notificar alguém sobre isso (o gancho que a própria capstone do Galho 13 já apontou para este galho) ainda aconteceria, se implementado ingenuamente, dentro do mesmo request/response que grava a conclusão no banco. Esta capstone fecha esse buraco amarrando as sete notas deste galho, uma por peça: `Tarefa.concluir()` passa a levantar um **Domain Event** `TarefaConcluida` (o gancho que a capstone do Galho 13 deixou); a `Unit of Work` grava esse evento numa tabela `outbox` na **mesma transação** que marca a tarefa como concluída ([[07 - Garantias de entrega na prática — DLQ e Outbox em Python|nota 07]]); uma Celery Beat task faz polling dessa tabela e publica os eventos pendentes ([[02 - Celery fundamentos — broker, worker e tasks|nota 02]], [[03 - Celery em produção — retries, idempotência e Celery Beat|nota 03]]); a publicação de fato acontece numa exchange RabbitMQ via aio-pika ([[05 - aio-pika — RabbitMQ assíncrono|nota 05]]); um **consumer assíncrono**, também aio-pika, recebe `TarefaConcluida` e chama o `AbstractNotificador`/`SlackAdapter` já construído na nota 07 do Galho 13 — sem que o handler HTTP espere um milissegundo a mais por isso; e se esse consumer falhar repetidamente ao processar um evento, ele vai para uma **Dead Letter Queue** em vez de travar o processamento dos próximos ([[07 - Garantias de entrega na prática — DLQ e Outbox em Python|nota 07]] de novo). Nenhuma peça é nova — cada uma já foi ensinada isolada nas sete notas anteriores; o trabalho desta capstone é integrá-las contra o código real da API de Tarefas, na ordem em que a conclusão de uma tarefa efetivamente percorre o sistema. Fecha o galho e aponta para o [[03-Dominios/Tecnologia/Python/index|Galho 15 — Microservices e sistemas distribuídos]]: a mesma API, agora falando com um broker de verdade, já tem a espinha dorsal de comunicação assíncrona que um sistema distribuído formaliza como arquitetura, não mais como capstone de um único galho.

## Onde a capstone do Galho 13 parou — e o que ainda está errado

A [[03-Dominios/Tecnologia/Python/Arquitetura e Design Patterns/08 - Capstone — refatorando a API de Tarefas pra arquitetura hexagonal|capstone do Galho 13]] terminou com uma API de Tarefas organizada em seis camadas — domínio puro, Repository, Unit of Work, composition root, Service Layer, Ports and Adapters — com uma frase explícita apontando pra este galho: "cada vez que `mover_tarefa` grava uma `Notificacao` e dispara um `notificador.enviar()`, ela está, na prática, reagindo a um fato que aconteceu no domínio... de um jeito ainda acoplado (a Service Layer decide explicitamente 'grave a notificação, depois envie o e-mail')". Essa observação vale, com a mesma força, para o caso de uso que esta capstone escolhe como cenário central: **concluir uma tarefa**.

O `concluir_tarefa` que a capstone do Galho 13 deixou pronto, no Passo 5 daquele refactor, é isto:

```python
"""services/tarefas.py — o estado em que o Galho 13 deixou o caso de uso."""

def concluir_tarefa(comando: ConcluirTarefaComando, uow: AbstractUnitOfWork) -> Tarefa:
    with uow:
        tarefa = uow.tarefas.get_do_usuario(comando.tarefa_id, comando.usuario_id)
        if tarefa is None:
            raise TarefaNaoEncontrada(comando.tarefa_id)

        tarefa.concluir()  # a regra de subtarefas pendentes mora na entidade
        uow.tarefas.add(tarefa)
        uow.commit()
        return tarefa
```

Funciona, e sozinho não tem nenhum defeito — mas o requisito de negócio que chega logo depois é o mesmo que a nota 01 deste galho já usou como caso canônico de abertura, só que aplicado aqui em vez de a um e-mail de boas-vindas: **"quando o usuário conclui uma tarefa, notifique-o por Slack"**. A tentação óbvia é a mesma da capstone do Galho 13 para `mover_tarefa` — chamar `notificador.enviar()` logo depois de `uow.commit()`, dentro do próprio `concluir_tarefa`:

```python
"""O jeito ingênuo — funciona, mas amarra o tempo de resposta do handler ao Slack."""

def concluir_tarefa(comando: ConcluirTarefaComando, uow: AbstractUnitOfWork, notificador: AbstractNotificador) -> Tarefa:
    with uow:
        tarefa = uow.tarefas.get_do_usuario(comando.tarefa_id, comando.usuario_id)
        if tarefa is None:
            raise TarefaNaoEncontrada(comando.tarefa_id)
        tarefa.concluir()
        uow.tarefas.add(tarefa)
        uow.commit()

    notificador.enviar(destinatario="#tarefas-concluidas", mensagem=f"Tarefa '{tarefa.titulo}' concluída")
    return tarefa
```

Isso resolve o requisito — mas reintroduz, com um nome diferente, exatamente o problema que abriu a nota 01 deste galho: o handler HTTP que responde `PATCH /tarefas/{id}/concluir` agora espera o `SlackAdapter.enviar()` terminar (uma chamada `requests.post()` síncrona, bloqueante, para um serviço de terceiros) antes de devolver `200 OK` ao cliente. Se o webhook do Slack estiver lento — rate limit, instabilidade momentânea, timeout de rede — o cliente HTTP que só queria saber "a tarefa foi marcada como concluída?" fica esperando por um canal de notificação que não faz parte do contrato imediato da resposta. É o mesmo raciocínio, a mesma pergunta ("por que o handler está esperando um serviço de terceiros responder, se a resposta não depende dele?"), agora aplicado ao domínio real desta trilha em vez de a um e-mail de cadastro.

> [!bug] O que está "quebrado", em uma frase — mesmo com a arquitetura hexagonal pronta
> A API do Galho 13 tem domínio isolado, Repository, UoW e Service Layer testáveis — mas nenhuma dessas camadas resolve, sozinha, o acoplamento de **tempo**: concluir uma tarefa e notificar alguém sobre isso continuam acontecendo no mesmo processo, na mesma chamada, sob o mesmo timeout HTTP, porque nada nesta arquitetura ainda tirou a notificação do caminho síncrono.

A arquitetura hexagonal do Galho 13 resolveu "onde a lógica mora" (acoplamento estrutural). Este galho resolve um problema diferente: "quando a lógica roda" (acoplamento temporal). Os dois são complementares, não concorrentes — e é exatamente por isso que esta capstone não reabre nenhuma decisão do Galho 13: `AbstractNotificador`, `SlackAdapter`, `AbstractUnitOfWork`, `Tarefa` continuam exatamente como estavam. O que muda é **como** o evento "tarefa concluída" sai do processo da API e chega até quem precisa reagir a ele.

```mermaid
%%{init: {"theme": "base", "themeVariables": {"primaryColor": "#4A90D9", "primaryBorderColor": "#2E5C8A", "lineColor": "#4A90D9"}}}%%
flowchart LR
    A["Galho 13\nArquitetura hexagonal\n(ONDE a lógica mora)"] --> B["Este galho\nMensageria\n(QUANDO a lógica roda)"]
    B --> C["Handler HTTP\nresponde em milissegundos,\nnão espera o Slack"]

    style A fill:#8b6914,color:#fff
    style B fill:#4A90D9,color:#fff
    style C fill:#2d7a4a,color:#fff
```

## Peça 1 — o Domain Event `TarefaConcluida` finalmente sai pro mundo

A capstone do Galho 13 já tinha `Tarefa` como uma entidade de domínio puro, com `concluir()` decidindo sozinha, a partir de suas próprias `subtarefas`, se a conclusão é permitida. O que faltava — e é exatamente o gancho que aquela capstone deixou para este galho — é `concluir()` também **registrar o fato** de que a conclusão aconteceu, como um objeto de primeira classe que outras partes do sistema podem reagir a ele, sem que `Tarefa` precise saber quem são essas outras partes:

```python
"""domain/events.py — Domain Events. Python puro, zero import de framework."""

from dataclasses import dataclass, field
from datetime import datetime
from uuid import uuid4


@dataclass(frozen=True)
class TarefaConcluida:
    """Um fato que já aconteceu — não uma instrução, um registro do passado."""

    tarefa_id: int
    usuario_id: int
    titulo: str
    evento_id: str = field(default_factory=lambda: str(uuid4()))
    ocorrido_em: datetime = field(default_factory=datetime.utcnow)
```

E `Tarefa`, em `domain/tarefa.py`, ganha uma lista de eventos pendentes — o padrão de "coleção de eventos de domínio" que o próprio livro-fonte do Galho 13 (Percival & Gregory) usa para deixar a entidade registrar fatos sem publicá-los ela mesma:

```python
"""domain/tarefa.py — a mesma Tarefa da capstone do Galho 13, com uma responsabilidade a mais."""

from dataclasses import dataclass, field
from datetime import datetime

from domain.events import TarefaConcluida


class TarefaComSubtarefasPendentesError(Exception):
    def __init__(self, tarefa_id: int) -> None:
        self.tarefa_id = tarefa_id
        super().__init__(f"Tarefa {tarefa_id} tem subtarefas pendentes")


@dataclass
class Tarefa:
    id: int | None
    usuario_id: int
    titulo: str
    concluida: bool = False
    criada_em: datetime = field(default_factory=datetime.utcnow)
    subtarefas: list["Tarefa"] = field(default_factory=list, compare=False)
    eventos: list[TarefaConcluida] = field(default_factory=list, compare=False, repr=False)

    def __eq__(self, outro: object) -> bool:
        if not isinstance(outro, Tarefa):
            return NotImplemented
        return self.id is not None and self.id == outro.id

    def __hash__(self) -> int:
        return hash(self.id)

    def concluir(self) -> None:
        pendentes = [s for s in self.subtarefas if not s.concluida]
        if pendentes:
            raise TarefaComSubtarefasPendentesError(self.id)

        self.concluida = True
        self.eventos.append(
            TarefaConcluida(tarefa_id=self.id, usuario_id=self.usuario_id, titulo=self.titulo)
        )
```

Repare no que **não** mudou: `TarefaComSubtarefasPendentesError` continua sendo a mesma exceção de domínio da capstone do Galho 13, o `__eq__`/`__hash__` de Entity continua comparando só o `id`, e `concluir()` continua decidindo sozinha, sem consultar nada fora de si mesma. A única adição é `self.eventos.append(...)` — uma linha, no fim do método, depois que a invariante de negócio já foi satisfeita. `Tarefa` não importa `aio_pika`, não importa `Session`, não sabe que existe um broker. Ela só registra, na própria lista `eventos`, que algo aconteceu — quem lê essa lista e decide o que fazer com ela é responsabilidade de uma camada de fora, exatamente como o Repository e a Unit of Work já são responsabilidade de fora do domínio.

> [!tip] Por que o evento nasce dentro de `Tarefa.concluir()`, e não como um `if` solto na Service Layer?
> Porque a regra "toda conclusão de tarefa gera um `TarefaConcluida`" é uma invariante do próprio ato de concluir — não uma decisão de orquestração que varia caso a caso. Se essa lógica morasse na Service Layer (`if sucesso: eventos.append(...)`), qualquer segundo caminho de código que chamasse `Tarefa.concluir()` diretamente — um script de manutenção, um teste, um worker de importação em lote, os mesmos cenários que a nota 02 do Galho 13 já usou pra justificar extrair o domínio — poderia esquecer de gerar o evento. Colocando a geração dentro do método que já garante a invariante de negócio, é estruturalmente impossível concluir uma tarefa sem que o evento correspondente exista.

## Peça 2 — a Unit of Work grava o evento na mesma transação (nota 07)

Com `Tarefa.concluir()` populando `tarefa.eventos`, falta uma peça: alguém precisa ler essa lista e persistir cada evento de forma que sobreviva a um crash do processo entre o commit da tarefa e a publicação de fato — o mesmo dual-write problem que a [[07 - Garantias de entrega na prática — DLQ e Outbox em Python|nota 07 deste galho]] já nomeou com o incidente da matrícula que existe no banco mas nunca chega a notificar ninguém. A resposta é a mesma: **Outbox**, reaproveitando a `AbstractUnitOfWork` que a nota 04 do Galho 13 já formalizou.

```python
"""domain/unit_of_work.py — o contrato ganha um terceiro Repository."""

from abc import ABC, abstractmethod

from domain.repository import AbstractRepository
from domain.repository_outbox import AbstractOutboxRepository


class AbstractUnitOfWork(ABC):
    tarefas: AbstractRepository
    outbox: AbstractOutboxRepository

    def __enter__(self) -> "AbstractUnitOfWork":
        return self

    def __exit__(self, exc_type, exc_value, traceback) -> None:
        if exc_type is not None:
            self.rollback()

    @abstractmethod
    def commit(self) -> None: ...

    @abstractmethod
    def rollback(self) -> None: ...
```

```python
"""infra/models.py — OutboxEvent, exatamente como a nota 07 já mostrou."""

from datetime import datetime
from sqlalchemy import String, Text
from sqlalchemy.orm import Mapped, mapped_column
from infra.orm import Base


class OutboxEvent(Base):
    __tablename__ = "outbox_events"

    id: Mapped[int] = mapped_column(primary_key=True)
    evento_id: Mapped[str] = mapped_column(String(64), unique=True)
    tipo: Mapped[str] = mapped_column(String(80))            # "tarefa.concluida"
    routing_key: Mapped[str] = mapped_column(String(80))
    payload: Mapped[str] = mapped_column(Text)                # JSON serializado
    criado_em: Mapped[datetime] = mapped_column(default=datetime.utcnow)
    publicado: Mapped[bool] = mapped_column(default=False)
    publicado_em: Mapped[datetime | None] = mapped_column(default=None)
```

E `concluir_tarefa`, em `services/tarefas.py`, ganha exatamente uma responsabilidade nova — traduzir cada `TarefaConcluida` da lista de eventos da entidade num `OutboxEvent` gravado pela mesma Unit of Work, antes do único `uow.commit()` da operação:

```python
"""services/tarefas.py — concluir_tarefa, versão final desta capstone."""

import json

from domain.commands import ConcluirTarefaComando
from domain.exceptions import TarefaNaoEncontrada
from domain.models import OutboxEvent
from domain.tarefa import Tarefa
from domain.unit_of_work import AbstractUnitOfWork


def concluir_tarefa(comando: ConcluirTarefaComando, uow: AbstractUnitOfWork) -> Tarefa:
    with uow:
        tarefa = uow.tarefas.get_do_usuario(comando.tarefa_id, comando.usuario_id)
        if tarefa is None:
            raise TarefaNaoEncontrada(comando.tarefa_id)

        tarefa.concluir()  # popula tarefa.eventos — a invariante já garante isso
        uow.tarefas.add(tarefa)

        for evento in tarefa.eventos:
            uow.outbox.add(OutboxEvent(
                id=None,
                evento_id=evento.evento_id,
                tipo="tarefa.concluida",
                routing_key="tarefa.concluida",
                payload=json.dumps({
                    "tarefa_id": evento.tarefa_id,
                    "usuario_id": evento.usuario_id,
                    "titulo": evento.titulo,
                    "ocorrido_em": evento.ocorrido_em.isoformat(),
                }),
            ))

        uow.commit()  # UM commit — tarefa concluída E evento pendente, juntos, ou nenhum dos dois
        return tarefa
```

Nenhuma chamada de rede — nem para o Slack, nem para o RabbitMQ — acontece dentro deste caso de uso. `uow.commit()` só toca o PostgreSQL, e a mesma garantia ACID que a nota 07 deste galho já explicou faz `tarefas` e `outbox_events` ganharem a linha nova juntas ou nenhuma delas ganhar nada. O handler HTTP que chama `concluir_tarefa` continua tendo três linhas de corpo — parse, chama, serializa, exatamente como a capstone do Galho 13 deixou — e devolve `200 OK` assim que o commit do banco termina, sem esperar Slack, RabbitMQ, ou qualquer coisa fora do PostgreSQL.

> [!warning] O erro mais fácil de cometer aqui: publicar direto, "já que a Unit of Work está aberta mesmo"
> **O que acontece:** alguém, revisando este código, sugere simplificar chamando `notificador.enviar()` dentro do próprio `with uow:`, argumentando que "está tudo no mesmo lugar mesmo, por que não resolver de uma vez?". **Por quê:** isso desfaz o próprio ponto desta capstone — reintroduz a chamada de rede síncrona dentro do caminho crítico do handler HTTP, e viola a regra que a nota 04 do Galho 13 já cravou: a Unit of Work cobre a transação de **banco**, nunca uma chamada de rede externa. `notificador.enviar()`, se estivesse aqui, aconteceria dentro da mesma transação que grava a tarefa — e se o Slack estivesse fora do ar, a exceção de rede subiria por dentro do `with uow:`, disparando um `rollback()` que desfaria a conclusão da tarefa por causa de um problema que não tem nada a ver com o banco. **Como evitar:** a única coisa que entra na Unit of Work é o `OutboxEvent` — um registro de banco como qualquer outro. A publicação de fato, e a notificação que ela vai disparar, acontecem depois, fora da transação, na peça seguinte.

## Peça 3 — o worker Celery Beat fazendo polling da tabela outbox (notas 02/03)

Com o evento gravado na tabela `outbox_events`, falta um processo que leia essa tabela periodicamente e publique de verdade. A nota 07 deste galho já mostrou esse worker, e ele reaproveita, sem alteração de mecânica, o Celery fundamentado na [[02 - Celery fundamentos — broker, worker e tasks|nota 02]] e o Celery Beat cravado na [[03 - Celery em produção — retries, idempotência e Celery Beat|nota 03]] — uma task agendada, não uma task disparada por evento:

```python
"""tasks.py — a mesma Celery Beat task da nota 07, aplicada à tabela outbox desta capstone."""

import asyncio
import json
from datetime import datetime

from celery import shared_task

from infra.models import OutboxEvent
from infra.session import SessionLocal
from infra.publicador import PublicadorDeEventos  # o mesmo da nota 05

_publicador = PublicadorDeEventos("amqp://guest:guest@rabbitmq/")


@shared_task
def publicar_eventos_pendentes() -> None:
    session = SessionLocal()
    try:
        pendentes = (
            session.query(OutboxEvent)
            .filter(OutboxEvent.publicado.is_(False))
            .order_by(OutboxEvent.criado_em)
            .limit(100)
            .all()
        )
        for evento in pendentes:
            asyncio.run(_publicador.publicar(
                routing_key=evento.routing_key,
                payload=json.loads(evento.payload),
            ))
            evento.publicado = True
            evento.publicado_em = datetime.utcnow()
            session.commit()  # marca UMA linha por vez, dentro do loop — nota 07 explica por quê
    finally:
        session.close()
```

```python
"""celeryconfig.py — Beat agendando o polling a cada 2 segundos."""

app.conf.beat_schedule = {
    "publicar-outbox-tarefas": {
        "task": "tasks.publicar_eventos_pendentes",
        "schedule": 2.0,
    },
}
```

Este é o único pedaço da capstone onde Celery entra — não para "processar a conclusão da tarefa" (isso continua sendo responsabilidade síncrona do handler FastAPI, protegido pela Unit of Work), mas para garantir que a tabela `outbox_events` seja drenada de forma confiável e retentável, mesmo que o processo da API tenha morrido logo depois do commit. Se o worker Celery cair no meio de um lote de 100 eventos, a próxima execução do Beat (dois segundos depois) simplesmente relê a mesma query — `WHERE publicado = False` — e retoma exatamente de onde parou, sem coordenação manual nenhuma, porque `publicado` é a única fonte de verdade sobre o que já saiu.

> [!question]- Por que não publicar direto do handler FastAPI, numa task Celery normal, em vez de fazer polling da tabela?
> Essa seria a versão mais direta — `publicar_evento_tarefa_concluida.delay(evento_id)` chamado logo depois de `uow.commit()`, sem tabela outbox nenhuma. O problema é o mesmo que motivou a Peça 2 inteira: entre o `uow.commit()` bem-sucedido e a chamada `.delay()` (que precisa, ela mesma, falar com o broker do Celery para enfileirar), existe uma janela onde o processo pode morrer sem que a task chegue a ser enfileirada — o dual-write problem, só que entre o PostgreSQL e o broker do Celery em vez de entre o PostgreSQL e o RabbitMQ de aio-pika. A tabela outbox resolve exatamente essa janela: o evento pendente já está no banco, de forma durável, antes de qualquer tentativa de publicação — o worker Celery Beat só entra depois, como um processo de garantia que dorme e acorda, sem depender de ninguém ter lembrado de chamá-lo no momento certo.

## Peça 4 — a publicação de fato via aio-pika (nota 05)

`_publicador.publicar(...)`, chamado pela task acima, é o mesmo `PublicadorDeEventos` que a [[05 - aio-pika — RabbitMQ assíncrono|nota 05 deste galho]] já construiu para o serviço de notificações — uma connection de longa duração, reaproveitada, publicando numa exchange topic `eventos.dominio` com `durable=True` e `delivery_mode=PERSISTENT`:

```python
"""infra/publicador.py — reaproveitado sem alteração da nota 05."""

import json

import aio_pika


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
        if self._exchange is None:
            await self.iniciar()
        mensagem = aio_pika.Message(
            body=json.dumps(payload).encode(),
            content_type="application/json",
            delivery_mode=aio_pika.DeliveryMode.PERSISTENT,
        )
        await self._exchange.publish(mensagem, routing_key=routing_key)
```

A única coisa nova, em relação ao cenário original da nota 05 (três serviços publicando `pedido.criado`, `pagamento.confirmado`, `curso.concluido`), é a routing key: `"tarefa.concluida"`, publicada na mesma exchange `eventos.dominio` que o resto do sistema já usa. Não existe uma exchange dedicada só para eventos de Tarefa — o modelo topic da nota 05 já foi desenhado justamente para múltiplos produtores compartilharem uma exchange e múltiplos consumidores escolherem, via binding, o que lhes interessa.

## Peça 5 — o consumer que notifica, desacoplado do tempo de resposta HTTP

Esta é a peça que fecha o ciclo e resolve, de verdade, o problema nomeado na abertura desta nota: um processo Python separado — não o processo da API FastAPI, não o worker Celery — consome `tarefa.concluida` do RabbitMQ e chama o `AbstractNotificador`/`SlackAdapter` que a nota 07 do Galho 13 já construiu. O handler HTTP que respondeu `PATCH /tarefas/{id}/concluir` já devolveu `200 OK` há muito tempo quando este consumer sequer chega a rodar.

```python
"""workers/consumer_notificacoes.py — consumer assíncrono, processo dedicado."""

import asyncio
import json

import aio_pika

from domain.notificador import AbstractNotificador
from infra.notificador_slack import SlackAdapter
from settings import SLACK_WEBHOOK_URL


async def processar_tarefa_concluida(
    message: aio_pika.abc.AbstractIncomingMessage,
    notificador: AbstractNotificador,
) -> None:
    try:
        evento = json.loads(message.body)
        notificador.enviar(
            destinatario="#tarefas-concluidas",
            mensagem=f"Tarefa '{evento['titulo']}' foi concluída pelo usuário {evento['usuario_id']}",
        )
        await message.ack()
    except (KeyError, json.JSONDecodeError):
        # payload malformado — erro permanente, não adianta tentar de novo
        await message.nack(requeue=False)
    except Exception:
        # falha ao chamar o Slack (timeout, 5xx) — pode ser transitório
        await message.nack(requeue=False)  # decisão explicada na Peça 6, abaixo


async def iniciar_consumer_notificacoes() -> None:
    notificador: AbstractNotificador = SlackAdapter(webhook_url=SLACK_WEBHOOK_URL)

    connection = await aio_pika.connect_robust("amqp://guest:guest@rabbitmq/")
    channel = await connection.channel()
    await channel.set_qos(prefetch_count=10)

    exchange = await channel.declare_exchange(
        "eventos.dominio", aio_pika.ExchangeType.TOPIC, durable=True,
    )
    queue = await channel.declare_queue(
        "notificacoes.tarefas-concluidas",
        durable=True,
        arguments={
            "x-dead-letter-exchange": "notificacoes.dlx",
            "x-dead-letter-routing-key": "tarefa.concluida.falha",
        },
    )
    await queue.bind(exchange, routing_key="tarefa.concluida")

    async with queue.iterator() as fila_iter:
        async for message in fila_iter:
            await processar_tarefa_concluida(message, notificador)


if __name__ == "__main__":
    asyncio.run(iniciar_consumer_notificacoes())
```

Repare que `SlackAdapter` é instanciado exatamente como na nota 07 do Galho 13 — `webhook_url` como único parâmetro de construção, `enviar(destinatario, mensagem)` como única operação. O consumer não sabe (nem precisa saber) que existe um `EmailAdapter` ou um `ConsoleAdapter` alternativos; troca-se `SlackAdapter` por outra implementação de `AbstractNotificador` mudando só a linha `notificador = SlackAdapter(...)`, sem tocar em `processar_tarefa_concluida` — a mesma promessa de composition root que a nota 05 do Galho 13 já formalizou, agora reaplicada num processo diferente da API HTTP.

> [!question]- Por que o consumer roda num processo Python separado, e não como uma task Celery a mais?
> Porque o problema aqui é de roteamento e desacoplamento de tempo, não de "execute isto uma vez" — o mesmo eixo de decisão que a nota 01 deste galho já formalizou. Uma task Celery seria acionada por quem publica o evento (`.delay()` chamado de algum lugar), o que reacoplaria o handler HTTP ao broker do Celery. Com aio-pika, o produtor (o worker de outbox da Peça 3) só publica numa exchange, sem saber quem — ou quantos — consumidores existem hoje. Se amanhã um segundo consumer precisar reagir ao mesmo `tarefa.concluida` (um serviço de analytics, por exemplo), ele só declara uma segunda queue com seu próprio binding na mesma exchange — sem tocar em nenhum código já existente, nem no worker que publica, nem no consumer de notificações.

```mermaid
%%{init: {"theme": "base", "themeVariables": {"primaryColor": "#4A90D9", "primaryBorderColor": "#2E5C8A", "lineColor": "#4A90D9"}}}%%
sequenceDiagram
    participant Cliente as Cliente HTTP
    participant API as FastAPI (Peça 1)
    participant DB as PostgreSQL
    participant Beat as Celery Beat (Peça 3)
    participant MQ as RabbitMQ (Peça 4)
    participant Consumer as Consumer aio-pika (Peça 5)
    participant Slack as Slack

    Cliente->>API: PATCH /tarefas/42/concluir
    API->>DB: uow.tarefas.add + uow.outbox.add (Peça 2)
    DB-->>API: COMMIT único
    API-->>Cliente: 200 OK (SEM esperar Slack)

    Note over API,Cliente: Handler já respondeu — tudo daqui pra frente<br/>é assíncrono, fora do request/response

    loop a cada 2s
        Beat->>DB: SELECT outbox_events WHERE publicado = False
        DB-->>Beat: TarefaConcluida pendente
        Beat->>MQ: publish("tarefa.concluida")
        MQ-->>Beat: confirmado
        Beat->>DB: UPDATE publicado = True
    end

    MQ->>Consumer: entrega mensagem (unacked)
    Consumer->>Slack: notificador.enviar(...)
    alt sucesso
        Slack-->>Consumer: 200
        Consumer->>MQ: message.ack()
    else falha repetida
        Consumer->>MQ: message.nack(requeue=False)
        MQ->>MQ: roteia para DLQ (Peça 6)
    end
```

## Peça 6 — a Dead Letter Queue protegendo o consumer (nota 07)

O `arguments={"x-dead-letter-exchange": ...}` já declarado na Peça 5 não é decoração — é a peça que a [[07 - Garantias de entrega na prática — DLQ e Outbox em Python|nota 07 deste galho]] já cravou como a diferença entre "descartar silenciosamente" e "tentar pra sempre", as duas respostas ruins para uma mensagem que falha repetidamente. Se o webhook do Slack estiver fora do ar por horas — não um timeout isolado, mas uma indisponibilidade prolongada — `notificador.enviar()` levanta exceção em toda tentativa, `message.nack(requeue=False)` roda toda vez, e cada mensagem que falha é roteada automaticamente pelo RabbitMQ para a DLX declarada, sem que o consumer principal trave ou fique reprocessando a mesma mensagem em loop:

```python
"""infra/dlq.py — declarando a DLQ que a Peça 5 já referencia."""

import aio_pika


async def declarar_dlq_notificacoes(channel: aio_pika.Channel) -> None:
    dlx = await channel.declare_exchange(
        "notificacoes.dlx", aio_pika.ExchangeType.DIRECT, durable=True,
    )
    dlq = await channel.declare_queue("notificacoes.tarefas-concluidas.dlq", durable=True)
    await dlq.bind(dlx, routing_key="tarefa.concluida.falha")
```

Nenhuma mudança é necessária no `processar_tarefa_concluida` da Peça 5 além do `nack(requeue=False)` que já estava lá — o roteamento para a DLX é inteiramente responsabilidade do broker, a partir do argumento declarado na fila principal. As próximas 340 (ou 3, ou 3 mil) mensagens que chegarem enquanto o Slack estiver fora do ar continuam sendo entregues, processadas, e roteadas para `notificacoes.tarefas-concluidas.dlq` sem interromper o throughput do consumer — que continua livre para processar qualquer evento novo que não dependa do Slack. Um segundo processo, dedicado, lê a DLQ periodicamente e decide se republica (depois que o Slack volta) ou arquiva para auditoria — exatamente o padrão que a nota 07 já descreveu como "a DLQ é uma fila comum, trate-a como uma".

> [!warning] Uma DLQ sem consumer dedicado é só um cemitério silencioso
> A nota 07 deste galho já registrou essa armadilha, e ela vale integralmente aqui: declarar `x-dead-letter-exchange` resolve o sintoma imediato (a fila principal não trava, nada se perde) mas não resolve, sozinho, a visibilidade operacional. Uma notificação de "tarefa concluída" parada na DLQ ainda representa um usuário que nunca recebeu o aviso no Slack — um alerta simples sobre o tamanho da `notificacoes.tarefas-concluidas.dlq` é o que transforma esse silêncio em algo acionável, em vez de uma surpresa descoberta só quando alguém reclama que "nunca recebo notificação de tarefa concluída".

## Peça 7 — e se um dia mais de um sistema precisar do mesmo evento? (nota 06, breve)

Vale nomear explicitamente o que esta capstone **não** precisou: o cenário atual tem exatamente um consumidor de `tarefa.concluida` — o serviço de notificações via Slack. RabbitMQ/aio-pika, com uma exchange topic e uma queue, é suficiente e mais simples do que o problema exigiria de outra forma. Se, no futuro, o volume de eventos crescesse e **múltiplos sistemas diferentes** precisassem consumir o mesmo `tarefa.concluida` de forma independente — não só notificação, mas também um pipeline de analytics contando quantas tarefas cada usuário conclui por semana, ou um serviço de auditoria arquivando o histórico completo com possibilidade de replay — esse seria exatamente o sinal, já nomeado na [[06 - kafka-python e aiokafka — producer e consumer|nota 06 deste galho]], de considerar Kafka em vez de RabbitMQ: múltiplos consumer groups lendo o mesmo log, cada um no seu próprio ritmo, sem que o produtor do evento precise saber quantos — ou quais — consumidores existem. Para o caso atual, com um único consumer de notificação, essa complexidade extra não se paga; é o mesmo raciocínio de "não escolher aiokafka só porque é possível" que a nota 01 deste galho já registrou como armadilha.

## A arquitetura completa, todas as sete peças juntas

```mermaid
%%{init: {"theme": "base", "themeVariables": {"primaryColor": "#4A90D9", "primaryBorderColor": "#2E5C8A", "lineColor": "#4A90D9"}}}%%
flowchart TB
    subgraph Sincrono["CAMINHO SÍNCRONO — o handler HTTP nunca espera além daqui"]
        HTTP["FastAPI\nPATCH /tarefas/id/concluir"]
        SVC["concluir_tarefa()\ntarefa.concluir() gera\nTarefaConcluida (Peça 1)"]
        UOW["Unit of Work\nuow.tarefas.add + uow.outbox.add\nUM commit (Peça 2)"]
        DB[("PostgreSQL\ntarefas + outbox_events")]
    end

    subgraph Assincrono["CAMINHO ASSÍNCRONO — fora do request/response"]
        BEAT["Celery Beat\npolling outbox_events\na cada 2s (Peça 3)"]
        MQ{"RabbitMQ\nexchange eventos.dominio (topic)\n(Peça 4)"}
        CONSUMER["Consumer aio-pika\nqueue notificacoes.tarefas-concluidas\n(Peça 5)"]
        SLACK_ADAPTER["SlackAdapter\n(AbstractNotificador, Galho 13 nota 07)"]
        DLQ["DLQ\nnotificacoes.tarefas-concluidas.dlq\n(Peça 6)"]
    end

    HTTP --> SVC --> UOW --> DB
    HTTP -.->|"200 OK — SEM esperar o resto"| Cliente["Cliente HTTP"]

    BEAT -->|"SELECT publicado=False"| DB
    BEAT -->|"publish(tarefa.concluida)"| MQ
    MQ -->|"binding: tarefa.concluida"| CONSUMER
    CONSUMER -->|"sucesso: ack()"| SLACK_ADAPTER
    CONSUMER -->|"falha repetida: nack(requeue=False)"| DLQ

    style Sincrono fill:#2d7a4a,color:#fff
    style Assincrono fill:#4A90D9,color:#fff
    style DLQ fill:#D0021B,color:#fff
    style SLACK_ADAPTER fill:#F5A623,color:#000
```

O detalhe que resume a capstone inteira, se for preciso escolher só um: a caixa `Sincrono` do diagrama acima é exatamente do mesmo tamanho que era na capstone do Galho 13 — três linhas de handler, uma Unit of Work, um commit. Nada na arquitetura hexagonal precisou crescer para acomodar mensageria. O que cresceu foi tudo o que acontece **depois** que o handler já respondeu — e é justamente esse "depois" que estava faltando para que a API deixasse de tratar o Slack como uma dependência crítica do caminho mais importante do sistema.

## Em entrevista

Uma pergunta comum para quem chega numa entrevista sênior falando de "arquitetura limpa" é: **"sua API está bem organizada em camadas — mas isso, sozinho, já resolve latência e acoplamento a serviços de terceiros?"** É uma pergunta que separa quem entende a diferença entre acoplamento estrutural e acoplamento temporal de quem confunde os dois.

> "Hexagonal architecture and dependency injection solve *where* logic lives — you get a domain layer, a repository, a service layer that don't know FastAPI or SQLAlchemy exist. But none of that, by itself, changes *when* a piece of logic runs. In my task API, completing a task and notifying someone about it over Slack were both happening inside the same HTTP request, under the same timeout, even after a full hexagonal refactor — because nothing had moved the Slack call off the synchronous path yet. The fix wasn't architectural, it was about ownership of time: the domain entity raises a `TarefaConcluida` domain event when a task is completed; the Unit of Work persists that event to an outbox table in the *same* transaction as the business change, so there's no window where the task is done but the event was never recorded; a separate Celery Beat process polls that table and publishes to RabbitMQ; and a dedicated consumer process — not the HTTP process — picks up the event and calls the notification adapter. The HTTP handler returns as soon as the database commit succeeds, full stop. If Slack is slow or down, the client never notices, because the client was never waiting on Slack in the first place."

> [!question]- O entrevistador pergunta: "e se o consumer de notificações cair por horas — o usuário nunca é avisado?"
> A resposta honesta separa dois problemas que já foram resolvidos nesta capstone por peças diferentes, e nomeia qual continua sendo uma decisão de negócio em aberto: se o consumer cair, as mensagens continuam se acumulando, intactas, na fila `notificacoes.tarefas-concluidas` do RabbitMQ (durável, com mensagens persistentes) — nada se perde, porque o publish já aconteceu e o ack só acontece depois do processamento bem-sucedido. Quando o consumer voltar, ele retoma consumindo a fila de onde parou. Isso é diferente de "o Slack está fora do ar enquanto o consumer está saudável" — esse segundo caso é o que a DLQ (Peça 6) resolve, roteando mensagens que falham repetidamente para investigação em vez de bloquear a fila. O que não está resolvido, e seria desonesto fingir que está, é a expectativa de latência da notificação em si: se o requisito de negócio for "o usuário precisa ser avisado em no máximo N segundos, sempre", isso exige SLA e alerta sobre o tamanho da fila e o lag do consumer — observabilidade operacional, não mais uma decisão de arquitetura de mensageria.

## Como explicar em inglês

> "A well-organized hexagonal architecture and a fully synchronous request path are two independent axes — you can have one without the other, and this capstone is the story of fixing the second one after the first was already done. The task API from the previous milestone had a clean domain layer and a testable service layer, but completing a task and notifying the user over Slack still happened inside the same HTTP request. The fix chains together every tool this messaging module covered: the domain entity raises a `TaskCompleted` domain event as part of its own invariant, so it's structurally impossible to complete a task without generating the event; the Unit of Work writes that event to an outbox table in the same database transaction as the business change, closing the dual-write window between 'the task is done' and 'the event is durably recorded'; a Celery Beat task polls that outbox table on a short interval and publishes pending events to a RabbitMQ topic exchange over aio-pika; a dedicated consumer process — running independently of the API and the Celery worker — subscribes to that exchange and calls the same notification port the architecture milestone already built, so swapping Slack for email again means changing one line, not the consumer's logic; and if that consumer fails repeatedly on a given message, RabbitMQ's native dead-lettering routes it to a separate queue instead of blocking everything behind it. None of these pieces is new — the point of this capstone is proving they compose into an HTTP handler that responds in milliseconds regardless of what Slack is doing."

| PT-BR | English |
|---|---|
| evento de domínio | domain event |
| tabela de saída | outbox table |
| processo de polling | polling process |
| fila de mensagens mortas | dead letter queue |
| consumer dedicado | dedicated consumer |
| desacoplamento de tempo de resposta | decoupling response latency |
| exchange compartilhada | shared exchange |

## Síntese — o que o Galho 14 inteiro ensinou

Recapitulando as sete notas deste galho, cada uma aplicada nesta capstone como uma peça concreta do fluxo de conclusão de uma tarefa:

1. [[01 - Panorama — Celery vs RQ vs aio-pika vs aiokafka|01 — Panorama]] deu o vocabulário decisório que esta capstone usou o tempo todo — tarefa vs fato, task queue vs comunicação direta — e justificou, na Peça 7, por que RabbitMQ (não Kafka) é a escolha certa para um único consumidor de notificação.
2. [[02 - Celery fundamentos — broker, worker e tasks|02 — Celery fundamentos]] deu a base de `@shared_task` e broker/worker que a Peça 3 reaproveitou para a task de polling do outbox.
3. [[03 - Celery em produção — retries, idempotência e Celery Beat|03 — Celery em produção]] deu o `beat_schedule` que agenda `publicar_eventos_pendentes` a cada 2 segundos — a Peça 3 não precisou de nenhum retry manual porque o próprio polling, retentável por natureza, já cobre o caso de falha.
4. [[04 - RQ — a fila simples sobre Redis|04 — RQ]] não entrou diretamente nesta capstone — o cenário (Beat agendado + roteamento por routing key) pede exatamente as duas features (scheduling maduro, controle fino de broker) que a nota 04 já registrou como o ponto de virada de RQ para Celery/aio-pika.
5. [[05 - aio-pika — RabbitMQ assíncrono|05 — aio-pika]] deu o `PublicadorDeEventos` reaproveitado sem alteração na Peça 4, e o modelo `connect_robust()`/ack manual/`nack(requeue=False)` que a Peça 5 aplicou ao consumer de notificações.
6. [[06 - kafka-python e aiokafka — producer e consumer|06 — kafka-python e aiokafka]] deu o contraste que a Peça 7 usou para nomear, sem desenvolver, o ponto em que Kafka substituiria RabbitMQ — múltiplos consumer groups independentes lendo o mesmo evento.
7. [[07 - Garantias de entrega na prática — DLQ e Outbox em Python|07 — Garantias de entrega na prática]] deu as duas peças estruturais desta capstone inteira: o Outbox que a Peça 2 aplicou para gravar `TarefaConcluida` na mesma transação da conclusão, e a DLQ que a Peça 6 configurou para proteger o consumer contra falhas permanentes de notificação.

Juntas, essas sete notas — mais o Domain Event que nasceu diretamente do gancho deixado pela [[03-Dominios/Tecnologia/Python/Arquitetura e Design Patterns/08 - Capstone — refatorando a API de Tarefas pra arquitetura hexagonal|capstone do Galho 13]] — fecham o Galho 14. A API de Tarefas, que saiu do Galho 13 com a lógica de negócio isolada mas o tempo de resposta ainda amarrado a qualquer serviço de terceiros chamado no mesmo request, sai desta capstone com uma fronteira clara: tudo que faz parte do contrato imediato de "a tarefa foi concluída?" continua síncrono, protegido pela mesma transação de banco; tudo que é reação a esse fato — notificar, e no futuro potencialmente muito mais — roda fora do caminho crítico, publicado via broker real, com garantia de que o evento nunca se perde (Outbox) e que uma falha de processamento nunca trava o sistema inteiro (DLQ).

## O que vem a seguir

A API de Tarefas, ao final desta capstone, já tem dois processos Python rodando de forma independente e coordenados só por um banco e um broker compartilhados: o processo FastAPI (respondendo HTTP), o worker Celery (publicando o outbox), e o consumer aio-pika (notificando) — três processos, não mais um único monolito. Isso não é, ainda, um sistema distribuído formal — é uma única aplicação cujo processamento se espalhou por múltiplos processos do mesmo código-base, comunicando-se via broker em vez de chamada de função direta. O próximo galho da trilha formaliza exatamente essa transição.

- **[[03-Dominios/Tecnologia/Python/index|Galho 15 — Microservices e sistemas distribuídos]]** (próximo) — pega a espinha dorsal de comunicação assíncrona que esta capstone construiu — publicar e consumir eventos via broker real, desacoplamento de tempo entre serviços — e formaliza isso como arquitetura de múltiplos serviços de verdade: não mais "uma API e um worker do mesmo repositório", mas serviços independentes, com seus próprios deploys, seus próprios bancos, comunicando-se pelos mesmos princípios de mensageria que este galho já estabeleceu.
- [[03-Dominios/Tecnologia/Python/index|Trilha Python]] — MOC da trilha.
- [[index|Mensageria (Galho 14)]] — MOC deste galho.
- [[03-Dominios/Tecnologia/Python/Arquitetura e Design Patterns/08 - Capstone — refatorando a API de Tarefas pra arquitetura hexagonal|Arquitetura e Design Patterns — Capstone (Galho 13)]] — o código-base hexagonal que esta capstone estende com Domain Events e Outbox, sem alterar nenhuma decisão estrutural já tomada lá.
- [[03-Dominios/Tecnologia/Python/Arquitetura e Design Patterns/07 - Arquitetura hexagonal e Ports and Adapters em Python|Arquitetura hexagonal e Ports and Adapters em Python (Galho 13, nota 07)]] — origem de `AbstractNotificador`/`SlackAdapter`, reaproveitados sem alteração pelo consumer desta capstone.

## Fontes

- Percival, Harry; Gregory, Bob. *Architecture Patterns with Python: Enabling Test-Driven Development, Domain-Driven Design, and Event-Driven Microservices*. O'Reilly Media, 2020. https://www.cosmicpython.com/book/preface.html (acessado em 2026-07-12) — fonte primária do padrão de Domain Events como coleção anexada à entidade (`tarefa.eventos`), reaproveitado nesta capstone sem alteração de mecânica.
- Celery Project — [*Celery: Distributed Task Queue*](https://docs.celeryq.dev/) (acessado 2026-07-12) — base de `@shared_task` e `beat_schedule` reaplicada na Peça 3.
- aio-pika docs — [*AsyncIO client for RabbitMQ*](https://aio-pika.readthedocs.io/) (acessado 2026-07-12) — `connect_robust()`, exchange topic, ack/nack manual, reaproveitados nas Peças 4 e 5.
- RabbitMQ — [*Dead Lettering*](https://www.rabbitmq.com/docs/dlx) (acessado 2026-07-12) — `x-dead-letter-exchange` configurado na Peça 6.
- [[01 - Panorama — Celery vs RQ vs aio-pika vs aiokafka|01]], [[02 - Celery fundamentos — broker, worker e tasks|02]], [[03 - Celery em produção — retries, idempotência e Celery Beat|03]], [[04 - RQ — a fila simples sobre Redis|04]], [[05 - aio-pika — RabbitMQ assíncrono|05]], [[06 - kafka-python e aiokafka — producer e consumer|06]], [[07 - Garantias de entrega na prática — DLQ e Outbox em Python|07]] — as sete notas irmãs deste galho, cada uma fonte primária de uma peça amarrada nesta capstone.
- [[03-Dominios/Tecnologia/Python/Arquitetura e Design Patterns/08 - Capstone — refatorando a API de Tarefas pra arquitetura hexagonal|Arquitetura e Design Patterns 08 — Capstone: refatorando a API de Tarefas pra arquitetura hexagonal]] — a capstone do Galho 13, código-base hexagonal e origem do gancho de Domain Events que esta capstone desenvolve.
- [[03-Dominios/Engenharia/Comunicação entre Sistemas/4 - Comunicação assíncrona/04 - Outbox e Saga|Comunicação entre Sistemas — Outbox e Saga]] — definição canônica do dual-write problem e do padrão Outbox, aplicada com código real na nota 07 e reaplicada nesta capstone.

Consultado em 2026-07-12.
