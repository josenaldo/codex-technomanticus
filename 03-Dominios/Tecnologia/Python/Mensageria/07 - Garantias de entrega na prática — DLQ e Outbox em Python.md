---
title: "Garantias de entrega na prática — DLQ e Outbox em Python"
created: 2026-07-12
updated: 2026-07-12
type: concept
status: seedling
fase: magus
tags:
  - python
  - mensageria
  - sqlalchemy
  - celery
  - rabbitmq
  - outbox
  - dlq
publish: true
aliases:
  - "Dead Letter Queue em Python"
  - "Outbox pattern em Python"
  - "DLQ e Outbox"
  - "x-dead-letter-exchange"
---

# Garantias de entrega na prática — DLQ e Outbox em Python

> [!abstract] TL;DR
> Duas falhas diferentes, duas soluções diferentes. Quando uma mensagem **falha repetidamente** — payload malformado, bug de negócio, dependência externa fora do ar por horas — descartá-la silenciosamente ou martelar retries pra sempre são as duas opções ruins; a terceira é uma **Dead Letter Queue (DLQ)**: uma fila separada onde a mensagem problemática pousa pra investigação, sem travar o processamento normal. No RabbitMQ isso é suporte **nativo** do broker — uma política `x-dead-letter-exchange` na declaração da fila principal, sem nenhum código de aplicação extra. No Celery, sem DLX nativa, o padrão é manual: capturar a exceção depois de `max_retries` esgotado e mover explicitamente para uma fila de erro. O segundo problema é estrutural, não de retry: o **dual-write** entre banco e broker — gravar um pedido no banco E publicar o evento correspondente não são atômicos, porque vivem em dois sistemas diferentes; se o publish falhar depois do commit, o pedido existe mas ninguém fica sabendo; se o commit falhar depois do publish, outros serviços já reagiram a um pedido que nunca existiu. A correção é o **Outbox pattern**: a Unit of Work grava o evento numa tabela `outbox` **na mesma transação** da mudança de negócio — atomicidade que o banco já garante de graça — e um processo separado (poller, ou CDC) lê essa tabela e publica de fato, depois, de forma retentável. DLQ resolve "o que fazer quando processar falha demais"; Outbox resolve "como publicar sem nunca ficar dessincronizado do banco". Os dois continuam exigindo idempotência do lado consumer — nenhum dos dois vira exactly-once.

## O incidente: o pedido que existe, mas ninguém sabe

Uma sexta-feira à noite, pico de tráfego de uma plataforma de cursos. Um aluno finaliza a matrícula num curso pago. O serviço de matrículas roda o código que qualquer pessoa que já passou pela nota 04 do Galho 13 desta trilha reconheceria — uma Unit of Work coordenando a gravação de negócio:

```python
def confirmar_matricula(uow: AbstractUnitOfWork, matricula_id: int) -> None:
    with uow:
        matricula = uow.matriculas.get(matricula_id)
        matricula.confirmar()
        uow.matriculas.add(matricula)
        uow.commit()  # a matrícula já existe, é permanente

    # 💥 aqui, fora da transação — porque publicar num broker nunca
    # faz parte de uma transação de banco relacional
    publicar_evento_matricula_confirmada(matricula)
```

`uow.commit()` roda, o PostgreSQL grava a linha, a transação encerra com sucesso. Um instante depois, a chamada que publica `matricula.confirmada` no RabbitMQ — fora de qualquer transação, porque não existe transação que cubra PostgreSQL e RabbitMQ ao mesmo tempo — encontra o broker momentaneamente inacessível: um failover de cluster, uma rede saturada pelo próprio pico de tráfego, um timeout de dois segundos que a aplicação nem trata com cuidado. O `publish` lança uma exceção que sobe até um log que ninguém está olhando às 22h de sexta.

A matrícula existe. Está lá, na tabela `matriculas`, com status `confirmada`, correta e imutável. Mas o efeito que essa confirmação deveria disparar — liberar o acesso ao conteúdo do curso, no serviço de conteúdo; emitir a nota fiscal, no serviço financeiro; notificar o aluno por e-mail — nunca aconteceu, porque nenhum desses três serviços jamais recebeu o evento. Do ponto de vista do aluno, a compra "deu certo": a tela mostrou confirmação. Só que, minutos depois, ele tenta acessar o curso que acabou de comprar e recebe "acesso negado" — porque o serviço de conteúdo nunca ficou sabendo que aquela matrícula existe.

O inverso também acontece, com a mesma facilidade, se alguém "conserta" o bug publicando **antes** de commitar: o evento sai, o serviço de conteúdo já libera o acesso, e um segundo depois o commit no banco falha — por um deadlock, por uma constraint violada — e a matrícula nunca chega a existir de verdade. Agora existe um aluno com acesso a um curso que, oficialmente, ele nunca comprou.

> [!question]- Isso não seria resolvido só colocando um `try/except` em volta do `publish`, retentando algumas vezes antes de desistir?
> Retry ajuda com falhas **transitórias** de rede — o broker volta em dois segundos, a segunda tentativa funciona, ninguém percebe nada. Mas não resolve o problema de fundo: entre o commit do banco e o publish bem-sucedido, sempre existe uma janela onde o processo pode simplesmente morrer — `SIGKILL` de um autoscaler, crash por falta de memória, deploy que reinicia o pod no pior milissegundo possível. Não importa quantos retries o código tente: se o processo não sobrevive até completar o publish, o evento nunca sai, e nenhum log de "falhei ao publicar, vou tentar de novo" ajuda, porque não existe mais processo nenhum rodando esse `try/except`. É o mesmo problema, só que a probabilidade de acontecer cai — a janela continua lá, só fica menor. A correção estrutural para esse tipo de janela é o assunto da segunda metade desta nota: mover a garantia de "isso precisa ser publicado" para dentro do banco, onde atomicidade já existe sem precisar de retry nenhum.

Este é o **dual-write problem**, já nomeado com precisão em [[03-Dominios/Engenharia/Comunicação entre Sistemas/4 - Comunicação assíncrona/04 - Outbox e Saga|Outbox e Saga]] — esta nota não repete a definição formal nem o argumento contra 2PC que já está lá, só aplica a solução (Outbox) com SQLAlchemy e Celery/aio-pika de verdade. Antes de chegar lá, esta nota resolve um problema irmão, mas diferente: o que fazer quando uma mensagem que **chegou** ao consumer falha repetidamente ao ser processada — o assunto da Dead Letter Queue.

## Dead Letter Queue — a terceira opção entre "descartar" e "tentar pra sempre"

A nota 03 deste galho já cravou o mecanismo de retry do Celery — `autoretry_for`, `retry_backoff`, `max_retries` — e o que acontece quando `max_retries` se esgota: a task levanta `MaxRetriesExceededError` e fica marcada como `FAILURE`. Essa nota também já registrou, na tabela de armadilhas, que confundir "task falhou de forma transitória" com "task falhou de forma permanente" é o erro central de configurar `autoretry_for` genérico demais. O que fica por resolver é: depois que uma mensagem esgota os retries — ou depois que um handler decide explicitamente "isso não é transitório, não adianta tentar de novo" — para onde ela vai?

As duas respostas ingênuas são as duas erradas:

- **Descartar silenciosamente** — a mensagem simplesmente desaparece, o log registra uma linha que ninguém vai ler até um cliente reclamar dias depois. É exatamente o padrão do incidente de abertura desta nota, só que a origem da falha é diferente (processamento, não publish).
- **Tentar pra sempre** — sem um teto, uma mensagem com payload malformado (um `KeyError` determinístico, por exemplo) volta pro início da fila em loop infinito, sendo entregue, falhando, e voltando — consumindo throughput do worker/consumer sem nunca ter chance real de suceder, e sem nunca sinalizar pra ninguém que existe um problema.

A **Dead Letter Queue** é a terceira via: uma fila separada, dedicada a mensagens que falharam de forma permanente, onde elas ficam paradas — visíveis, investigáveis, sem bloquear a fila principal — até alguém (um humano, ou um job de reprocessamento) decidir o que fazer com elas.

```mermaid
flowchart TD
    classDef marca fill:#8855DF33,stroke:#8855DF,color:#E9ECF2
    classDef neutro fill:#1B2029,stroke:#4E5666,color:#C6CCD8
    classDef destaque fill:#FFAA0024,stroke:#FFAA00,color:#E9ECF2
    A["Mensagem entregue ao consumer"] --> B{"Processamento OK?"}
    B -->|"Sim"| C["ack — sai da fila"]
    B -->|"Não, erro transitório"| D{"Tentativas < limite?"}
    D -->|"Sim"| E["nack com requeue<br/>ou autoretry"]
    E --> A
    D -->|"Não, esgotou"| F["Dead Letter Queue"]
    B -->|"Não, erro permanente<br/>(payload malformado, bug)"| F

    F --> G["Investigação manual<br/>ou reprocessamento dirigido"]

    class C neutro
    class F marca
    class E destaque
```

**Resumo em uma frase:** DLQ não é sobre evitar a falha — é sobre garantir que uma falha permanente vire um sinal visível e investigável, em vez de um descarte silencioso ou um loop que nunca resolve nada.

### RabbitMQ — DLQ é uma política do broker, não código de aplicação

Diferente de Celery, o RabbitMQ tem suporte **nativo** a dead lettering — não é um padrão que a aplicação precisa implementar do zero, é uma propriedade que se declara na fila. Uma mensagem é roteada automaticamente para uma **Dead Letter Exchange (DLX)** quando qualquer uma destas três condições acontece, segundo a documentação oficial ([RabbitMQ, *Dead Lettering*](https://www.rabbitmq.com/docs/dlx), 2026):

- o consumer chama `nack`/`reject` com `requeue=False` — exatamente o `message.nack(requeue=False)` que a nota 05 deste galho já usou no serviço de notificações, sem detalhar ainda pra onde a mensagem vai;
- a mensagem excede seu TTL (`x-message-ttl`, se configurado na fila ou na própria mensagem);
- a fila atinge seu limite de tamanho (`x-max-length`) e a mensagem mais antiga é descartada para dar espaço à nova.

A configuração acontece na **declaração da fila principal**, como um argumento extra — não numa camada separada de retry escrita à mão:

```python
import aio_pika

async def declarar_fila_com_dlq(channel: aio_pika.Channel) -> aio_pika.Queue:
    # A Dead Letter Exchange é uma exchange comum — direct é suficiente
    # quando não há necessidade de roteamento por padrão de routing key.
    dlx = await channel.declare_exchange(
        "matriculas.dlx", aio_pika.ExchangeType.DIRECT, durable=True,
    )
    dlq = await channel.declare_queue("matriculas.dlq", durable=True)
    await dlq.bind(dlx, routing_key="matriculas.falhas")

    # A fila principal aponta para a DLX via argumento de política —
    # nenhum código de aplicação decide o roteamento, o broker decide.
    fila_principal = await channel.declare_queue(
        "matriculas.processar",
        durable=True,
        arguments={
            "x-dead-letter-exchange": "matriculas.dlx",
            "x-dead-letter-routing-key": "matriculas.falhas",
        },
    )
    return fila_principal
```

O detalhe que costuma surpreender quem configura isso pela primeira vez: **nenhuma mudança é necessária no código do consumer** além de já chamar `nack(requeue=False)` no caminho de erro permanente — o roteamento pra DLX é inteiramente responsabilidade do broker, a partir do argumento `x-dead-letter-exchange` declarado na fila de origem. O consumer da fila principal sequer precisa saber que a DLQ existe.

```python
async def processar_matricula(message: aio_pika.abc.AbstractIncomingMessage) -> None:
    try:
        evento = json.loads(message.body)
        liberar_acesso_ao_curso(evento["matricula_id"])
        await message.ack()
    except (KeyError, json.JSONDecodeError):
        # payload malformado — não adianta tentar de novo, é permanente
        logger.error("Payload inválido, mensagem vai para a DLQ: %s", message.body)
        await message.nack(requeue=False)
    except ServicoConteudoIndisponivel:
        # erro transitório — devolve pra fila principal, tenta de novo depois
        await message.nack(requeue=True)
```

> [!question]- Por que não simplesmente configurar `x-message-ttl` e deixar o RabbitMQ decidir sozinho quando desistir de uma mensagem?
> TTL resolve um problema diferente: "essa mensagem perdeu validade depois de N segundos/minutos", útil para eventos com prazo de relevância (uma cotação de preço que expira, um código de verificação de dois fatores). Ele não distingue entre "essa mensagem ainda é relevante mas o processamento falhou" e "essa mensagem simplesmente ficou velha esperando na fila" — as duas acionam o mesmo TTL. Combinar TTL com dead lettering funciona bem quando o requisito real é os dois ao mesmo tempo (mensagens que expiram vão para investigação, não somem), mas usar só TTL como substituto de uma política de retry com DLQ dedicada mistura duas decisões de negócio diferentes numa única configuração — geralmente vale a pena separar: `nack(requeue=False)` explícito no código para "processamento falhou permanentemente", TTL separado só onde existe prazo de validade real do dado.

> [!tip] A DLQ é uma fila comum — trate-a como uma
> Não existe magia especial numa fila que recebe mensagens mortas: ela é uma `queue` do RabbitMQ como qualquer outra, e pode (deve) ter seu próprio consumer — um processo que lê a `matriculas.dlq`, registra métricas (`unacked` alto na DLQ é um sinal de alerta tão válido quanto na fila principal), e decide, mensagem a mensagem ou em lote, se republica na fila original (depois de corrigir o bug que causou a falha) ou arquiva permanentemente para auditoria.

### Celery — sem DLX nativa, o padrão é manual

Celery não tem um conceito de "Dead Letter Exchange" embutido — a fila que ele usa (Redis ou RabbitMQ) é um detalhe de implementação escondido atrás da abstração de task, e o framework não expõe um argumento equivalente a `x-dead-letter-exchange` para configurar. O padrão, então, é explícito: capturar a exceção depois que `max_retries` se esgota e mover a mensagem "à mão" para uma fila de erro.

```python
from celery import shared_task
from celery.exceptions import MaxRetriesExceededError

@shared_task(
    bind=True,
    autoretry_for=(ConnectionError, TimeoutError),
    retry_backoff=True,
    max_retries=5,
)
def liberar_acesso_curso(self, matricula_id: int, evento_id: str):
    try:
        _liberar_acesso(matricula_id, evento_id)
    except MaxRetriesExceededError:
        mover_para_fila_de_erro.delay(
            task_original="liberar_acesso_curso",
            args={"matricula_id": matricula_id, "evento_id": evento_id},
            motivo="max_retries esgotado",
        )
        raise
```

```python
@shared_task
def mover_para_fila_de_erro(task_original: str, args: dict, motivo: str):
    # Persistir o registro é o que importa — a "fila de erro" pode ser
    # uma tabela de banco (mais fácil de consultar e reprocessar em lote
    # do que uma fila cega), não necessariamente outra fila de mensagens.
    TaskFalhada.objects.create(
        task_original=task_original,
        args=args,
        motivo=motivo,
        criada_em=timezone.now(),
    )
    logger.error("Task movida para fila de erro: %s (%s)", task_original, motivo)
```

Uma variação comum, mais próxima do modelo de fila real do RabbitMQ: em vez de gravar numa tabela, publicar explicitamente numa segunda fila Celery dedicada a erros, roteando com `task_routes` ou `.apply_async(queue="erros")` — o mesmo mecanismo de roteamento por fila já coberto na nota 01 deste galho, aplicado aqui a mensagens mortas em vez de tipos de trabalho:

```python
@shared_task(bind=True, max_retries=5)
def processar_pagamento(self, pedido_id: int):
    try:
        _processar(pedido_id)
    except OperationalError as exc:
        try:
            raise self.retry(exc=exc, countdown=2 ** self.request.retries)
        except MaxRetriesExceededError:
            registrar_falha_permanente.apply_async(
                args=[pedido_id], queue="fila-de-erro",
            )
```

> [!warning] `task_reject_on_worker_lost` não é uma DLQ
> **O que acontece:** um time configura `task_reject_on_worker_lost=True` esperando que isso funcione como uma dead-letter queue — mensagens de tasks cujo worker morreu no meio da execução "vão para algum lugar seguro". **Por quê:** essa opção controla um comportamento bem mais estreito — quando um worker é encerrado (`SIGKILL`, OOM killer) no meio de uma task, `task_reject_on_worker_lost=True` faz o broker rejeitar a mensagem (em vez de deixá-la marcada como "em processamento" para sempre, o mesmo problema de mensagem `unacked` presa já coberto na nota 05 deste galho para aio-pika). Rejeitar, no RabbitMQ, sem uma DLX configurada na fila, simplesmente **requeue** a mensagem por padrão — ela volta para o início da fila e é entregue de novo, não vai para nenhuma fila de erro. É um mecanismo de recuperação de falha de infraestrutura (worker morreu), não de roteamento de mensagens problemáticas. **Como evitar:** tratar `task_reject_on_worker_lost` como parte da resiliência a falhas de worker (ajuda a não perder trabalho quando um processo morre) e configurar a fila de erro — manual no Celery, `x-dead-letter-exchange` no RabbitMQ puro — como uma decisão separada, orientada a "essa mensagem falhou repetidamente ao processar", não a "o worker que a segurava morreu".

## Casos práticos

### Cenário 1: poison message travando uma fila inteira

O serviço de notificações da nota 05 deste galho recebe, num dia comum, um evento malformado — um payload publicado por uma versão antiga do `pedidos-service`, ainda rodando num pod que não foi atualizado no último deploy, com um campo renomeado. `json.loads(message.body)` funciona (é JSON válido), mas o código seguinte, `evento["usuario_id"]`, lança `KeyError` porque o campo agora se chama `usuario`. Sem DLX configurada e com `message.process()` (o atalho que faz `nack(requeue=True)` automaticamente em qualquer exceção, coberto na nota 05), essa mensagem específica volta pro início da fila, é entregue de novo, lança o mesmo `KeyError`, volta de novo — um loop infinito que consome throughput do consumer sem nunca ter chance de suceder, porque o campo nunca vai aparecer sozinho. A correção teve duas partes: trocar `message.process()` por `ack`/`nack` explícitos que distinguem erro transitório de erro de payload, e configurar `x-dead-letter-exchange` na fila principal — a partir daí, a mesma classe de erro passa a aparecer imediatamente na DLQ, visível no RabbitMQ Management Plugin, em vez de silenciosamente consumir ciclos de worker por dias até alguém notar a taxa de throughput anormalmente baixa.

### Cenário 2: reprocessamento em lote depois de corrigir um bug

Uma tabela `TaskFalhada` (o padrão manual do Celery, seção anterior) acumula 340 registros de `processar_pagamento` que falharam com `IntegrityError` porque uma migração de banco mal coordenada deixou uma constraint `NOT NULL` numa coluna que o código ainda não preenchia. Depois de corrigir o bug e rodar a migração corretiva, o time precisa reprocessar as 340 tasks — e é aqui que a decisão de "fila de erro = tabela" (em vez de fila de mensagens) se paga: uma query simples (`TaskFalhada.objects.filter(motivo__contains="IntegrityError", reprocessada=False)`) seleciona exatamente o subconjunto afetado, e um script dispara `.delay()` de novo para cada uma, marcando `reprocessada=True` conforme confirma sucesso — algo que seria mais difícil de fazer com precisão numa fila RabbitMQ pura, onde selecionar "só as mensagens que falharam por esse motivo específico" exigiria inspecionar o corpo de cada mensagem uma a uma.

## O dual-write problem, aplicado: Outbox com SQLAlchemy real

DLQ resolve o que fazer quando o processamento de uma mensagem que **já chegou** falha. O problema do incidente de abertura desta nota é anterior a isso — é sobre garantir que o evento **saia** de forma consistente com a mudança de negócio que o originou. A definição formal do dual-write problem, por que "banco primeiro, broker depois" e "broker primeiro, banco depois" têm as duas uma janela de falha, e por que 2PC não é a resposta em arquitetura de microsserviços já estão em [[03-Dominios/Engenharia/Comunicação entre Sistemas/4 - Comunicação assíncrona/04 - Outbox e Saga|Outbox e Saga]] — esta seção não repete nada disso, só mostra o padrão com SQLAlchemy e a `AbstractUnitOfWork` já estabelecida na [[03-Dominios/Tecnologia/Python/Arquitetura e Design Patterns/04 - Unit of Work — formalizando o padrão que já existia|nota 04 do Galho 13]].

```mermaid
sequenceDiagram
    participant App as Serviço de Matrículas
    participant DB as Banco (PostgreSQL)
    participant Broker as RabbitMQ

    rect rgb(240, 240, 240)
    Note over App,Broker: SEM Outbox — dual write
    App->>DB: INSERT matricula (confirmada) — COMMIT
    Note over DB: matrícula já é permanente
    App->>Broker: publish("matricula.confirmada")
    Broker--xApp: falha — broker inacessível
    Note over App,Broker: matrícula existe, evento nunca saiu —<br/>nenhum outro serviço fica sabendo
    end
```

```mermaid
sequenceDiagram
    participant App as Serviço de Matrículas
    participant DB as Banco (PostgreSQL)
    participant Poller as Outbox Poller
    participant Broker as RabbitMQ

    rect rgb(240, 240, 240)
    Note over App,Broker: COM Outbox — atomicidade local
    App->>DB: INSERT matricula<br/>INSERT outbox_event (mesma transação)
    Note over DB: COMMIT único — as duas linhas<br/>existem juntas, ou nenhuma existe
    Poller->>DB: SELECT eventos pendentes
    DB-->>Poller: outbox_event (não publicado)
    Poller->>Broker: publish("matricula.confirmada")
    Broker-->>Poller: confirmado
    Poller->>DB: UPDATE outbox_event SET publicado=true
    end
```

**Resumo em uma frase:** a diferença entre os dois diagramas não é "publicar com mais cuidado" — é mover a decisão "isso precisa ser publicado" para dentro da mesma transação que já garante atomicidade de graça, e deixar a publicação de verdade acontecer depois, de forma retentável.

### A tabela `OutboxEvent`

Seguindo o mesmo estilo de `Mapped`/`mapped_column` já estabelecido em [[03-Dominios/Tecnologia/Python/Persistência de dados/02 - SQLAlchemy ORM — Session, mapped classes e relationships|SQLAlchemy ORM — Session, mapped classes e relationships]] (Galho 9, não repetido aqui):

```python
# infra/models.py
from datetime import datetime
from sqlalchemy import String, Text
from sqlalchemy.orm import Mapped, mapped_column
from infra.orm_base import Base  # a mesma DeclarativeBase do Galho 9


class OutboxEvent(Base):
    __tablename__ = "outbox_events"

    id: Mapped[int] = mapped_column(primary_key=True)
    evento_id: Mapped[str] = mapped_column(String(64), unique=True)
    tipo: Mapped[str] = mapped_column(String(80))          # "matricula.confirmada"
    routing_key: Mapped[str] = mapped_column(String(80))
    payload: Mapped[str] = mapped_column(Text)              # JSON serializado
    criado_em: Mapped[datetime] = mapped_column(default=datetime.utcnow)
    publicado: Mapped[bool] = mapped_column(default=False)
    publicado_em: Mapped[datetime | None] = mapped_column(default=None)
```

`evento_id` é gerado uma única vez, no momento em que a linha é criada — nunca recalculado — pela mesma razão já estabelecida na nota 03 deste galho para a chave de idempotência de tasks Celery: se fosse recalculado a cada tentativa de publicação, a checagem de deduplicação do lado consumer nunca encontraria a entrada anterior.

### A Unit of Work grava o evento na mesma transação do negócio

A peça central: `AbstractUnitOfWork` já expõe os Repositories de uma operação de negócio através de uma única `Session` compartilhada, e `commit()` já é o único ponto explícito onde tudo acumulado até ali vira permanente, de uma vez (mecânica cravada na nota 04 do Galho 13, não repetida aqui). O Outbox não exige nenhum mecanismo novo — só mais um Repository exposto pela mesma Unit of Work:

```python
# domain/unit_of_work.py — adicionando outbox ao contrato já existente
class AbstractUnitOfWork(ABC):
    matriculas: AbstractMatriculaRepository
    outbox: AbstractOutboxRepository
    # __enter__/__exit__/commit()/rollback() já definidos na nota 04 do Galho 13
```

```python
# services/confirmar_matricula.py — a versão corrigida
import json
from uuid import uuid4

def confirmar_matricula(uow: AbstractUnitOfWork, matricula_id: int) -> None:
    with uow:
        matricula = uow.matriculas.get(matricula_id)
        matricula.confirmar()
        uow.matriculas.add(matricula)

        uow.outbox.add(OutboxEvent(
            id=None,
            evento_id=str(uuid4()),
            tipo="matricula.confirmada",
            routing_key="matricula.confirmada",
            payload=json.dumps({
                "matricula_id": matricula.id,
                "usuario_id": matricula.usuario_id,
                "curso_id": matricula.curso_id,
            }),
        ))

        uow.commit()  # UM commit — matrícula E evento pendente, juntos, ou nenhum dos dois
```

Não existe mais nenhuma chamada de rede para o broker dentro deste caso de uso. `uow.commit()` só toca o banco — a mesma máquina ACID que a [[03-Dominios/Tecnologia/Python/Persistência de dados/06 - Transações e isolamento — ACID na prática, isolation levels, deadlocks de aplicação|nota 06 do Galho 9]] já cobre em profundidade garante que `matriculas` e `outbox_events` ganham a linha nova juntas ou nenhuma delas ganha nada. O problema do incidente de abertura — a janela entre "banco confirmou" e "broker confirmou" — deixou de existir dentro deste caso de uso, porque o broker não é mais tocado aqui.

> [!warning] Gravar o evento fora da transação do negócio anula o Outbox inteiro
> **O que acontece:** alguém "otimiza" o código acima movendo `uow.outbox.add(...)` para depois de `uow.commit()`, com um segundo `commit()` separado — talvez achando que separar as duas escritas deixa o código "mais claro". **Por quê:** isso recria exatamente o dual-write problem, só que entre duas tabelas do mesmo banco em vez de banco e broker — ainda são dois `commit()`s separados, e uma falha entre os dois deixa a matrícula confirmada sem nenhum evento pendente registrado. O ganho inteiro do Outbox depende de as duas escritas estarem na **mesma** transação — a mesma regra que a nota 04 do Galho 13 já estabeleceu como armadilha central ("um caso de uso, um `commit()`"). **Como evitar:** o evento é só mais um `Repository.add()` chamado dentro do mesmo `with uow:`, antes do único `uow.commit()` da operação — nunca uma escrita separada, depois, com seu próprio commit.

### O worker de polling

Um processo separado — aqui, uma Celery Beat task, já cravada com profundidade na nota 03 deste galho — lê a tabela periodicamente e publica de verdade:

```python
# tasks.py
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
            _publicar_via_aio_pika(evento)
            evento.publicado = True
            evento.publicado_em = datetime.utcnow()
            session.commit()  # marca UMA linha por vez — não em lote
    finally:
        session.close()
```

```python
app.conf.beat_schedule = {
    "publicar-outbox": {
        "task": "tasks.publicar_eventos_pendentes",
        "schedule": 2.0,  # a cada 2 segundos — latência aceitável para eventos de negócio
    },
}
```

`_publicar_via_aio_pika` reaproveita exatamente o `PublicadorDeEventos` já mostrado na nota 05 deste galho — uma connection de longa duração, reaproveitada, não uma nova por evento:

```python
_publicador = PublicadorDeEventos("amqp://guest:guest@localhost/")

async def _publicar_via_aio_pika_async(evento: OutboxEvent) -> None:
    await _publicador.publicar(
        routing_key=evento.routing_key,
        payload=json.loads(evento.payload),
    )

def _publicar_via_aio_pika(evento: OutboxEvent) -> None:
    asyncio.run(_publicar_via_aio_pika_async(evento))
```

> [!warning] Marcar como publicado em lote, não linha a linha
> **O que acontece:** para reduzir o número de `UPDATE`s, o worker publica as 100 mensagens do lote e só depois roda um único `UPDATE ... WHERE id IN (...)` cobrindo todas de uma vez, no fim do loop. **Por quê:** se o processo morrer depois de publicar 60 das 100 mensagens, mas antes do `UPDATE` final, nenhuma das 100 foi marcada como publicada — a próxima execução do poller lê as mesmas 100 linhas de novo (não só as 40 restantes) e publica as 60 já enviadas uma segunda vez. É a mesma armadilha já registrada em [[03-Dominios/Engenharia/Comunicação entre Sistemas/4 - Comunicação assíncrona/04 - Outbox e Saga|Outbox e Saga]] para o Polling Publisher genérico — aqui, em código Python real. **Como evitar:** marcar cada linha como publicada imediatamente após o `publish` correspondente ter sido confirmado, como o código acima já faz (`session.commit()` dentro do loop, não depois dele) — o custo é uma escrita a mais por mensagem, o ganho é reduzir a janela de duplicação de "o lote inteiro" para "no máximo uma mensagem".

### Onde CDC entra, sem repetir a mecânica

O worker de polling acima paga dois custos que crescem com volume: latência (o evento só sai no próximo tick, aqui até 2 segundos) e carga de leitura constante na tabela `outbox_events`. A alternativa de escala — Change Data Capture, lendo o write-ahead log do PostgreSQL em vez de fazer `SELECT` — já está descrita com profundidade em [[03-Dominios/Engenharia/Comunicação entre Sistemas/4 - Comunicação assíncrona/04 - Outbox e Saga|Outbox e Saga]] (seção "Transaction log tailing (CDC)"), incluindo o Debezium como ferramenta de referência. Nada muda no lado Python além de a tabela `OutboxEvent` continuar existindo exatamente como está — o Debezium lê o WAL de fora, sem precisar de nenhum código de aplicação adicional além da tabela em si. A decisão entre poller e CDC é de infraestrutura e volume, não de modelagem: os dois caminhos publicam a partir da mesma tabela `outbox_events`.

## Armadilhas comuns

> [!warning] Esquecer idempotência no consumer porque "o Outbox já resolveu"
> **O que acontece:** depois de implementar o Outbox e ver o pedido fantasma desaparecer, o time remove (ou nunca implementa) a checagem de idempotência do lado que consome `matricula.confirmada`. **Por quê:** tanto o poller quanto o CDC podem publicar com sucesso e morrer antes de marcar a linha como publicada (poller) ou antes do offset de leitura do WAL avançar (CDC) — na próxima execução, o mesmo evento sai de novo. O Outbox garante **at-least-once**, nunca exactly-once, exatamente como já registrado em [[03-Dominios/Engenharia/Comunicação entre Sistemas/4 - Comunicação assíncrona/04 - Outbox e Saga|Outbox e Saga]]. A disciplina de idempotência do consumer — chave de deduplicação checada dentro da mesma transação do efeito, upsert em vez de insert cego — já cravada em código Python real na nota 03 deste galho, continua sendo obrigatória. **Como evitar:** tratar Outbox e idempotência do consumer como as duas metades da mesma garantia de ponta a ponta, nunca como alternativas — o `evento_id` gerado na criação da linha `OutboxEvent` é exatamente a chave que o consumer deveria usar para deduplicar.

> [!warning] DLQ sem alerta, só arquivamento passivo
> **O que acontece:** a fila (ou tabela) de erro é configurada corretamente, mensagens param de se perder e param de causar loop infinito — mas ninguém monitora o volume dela, e ela vira um cemitério silencioso que só alguém olha quando um cliente reclama. **Por quê:** DLQ resolve o sintoma imediato (a fila principal não trava, nada se perde silenciosamente) mas não resolve, sozinha, o problema de visibilidade operacional — uma mensagem parada na DLQ ainda representa um efeito de negócio que não aconteceu (o e-mail não foi enviado, o acesso não foi liberado), só que agora documentado em vez de descartado. **Como evitar:** monitorar o tamanho da DLQ/tabela de erro como uma métrica de primeira classe — um alerta simples ("mais de N mensagens na DLQ na última hora") já transforma "silêncio até alguém notar por acaso" em "alerta acionável em minutos", o mesmo padrão de correção já registrado no cenário da saga presa em [[03-Dominios/Engenharia/Comunicação entre Sistemas/4 - Comunicação assíncrona/04 - Outbox e Saga|Outbox e Saga]].

## Em entrevista

Uma pergunta clássica de entrevista sênior sobre sistemas distribuídos é "como você garante que um evento de negócio nunca se perde ao publicar num broker?" — e a resposta fraca para nessa frase, como se "usar um broker confiável" fosse suficiente. A resposta que sinaliza profundidade nomeia o problema estrutural primeiro: "a publicação nunca é atômica com a escrita de negócio porque são dois sistemas diferentes — então eu movo a garantia de atomicidade para dentro do banco, gravando o evento numa tabela outbox na mesma transação da mudança de negócio, e deixo um processo separado, retentável, cuidar da publicação de verdade." Um segundo sinal forte é mencionar sem que perguntem que isso não elimina duplicação — só elimina perda — e que o consumer continua precisando ser idempotente. Um terceiro sinal, mais raro: saber a diferença entre DLQ (o que fazer quando o processamento falha depois que a mensagem chegou) e Outbox (como garantir que a mensagem saia de forma consistente com o banco) — os dois aparecem juntos em produção, mas resolvem problemas diferentes, e confundir os dois numa resposta de entrevista é um sinal de que a pessoa leu sobre o assunto sem ter debugado nenhum dos dois em produção.

## Como explicar em inglês

> "There are two different failure modes here, and they need two different fixes. A Dead Letter Queue handles messages that keep failing after they've already been delivered — instead of silently dropping them or retrying forever, they land in a separate queue for investigation. RabbitMQ supports this natively: you declare `x-dead-letter-exchange` on the main queue, and any message that gets `nack`ed without requeue, expires, or gets dropped for queue length automatically routes there — no application code needed beyond the queue declaration itself. Celery doesn't have that built in, so the pattern is manual: catch `MaxRetriesExceededError` and explicitly move the failed task into an error table or a dedicated error queue. The second problem is structural, not about retries at all — it's the dual-write problem: saving a record to the database and publishing an event to a broker aren't atomic, because they're two different systems. If the publish fails after the commit, the record exists but nobody downstream knows. The Outbox pattern fixes this by writing the event to an outbox table in the *same* transaction as the business write — atomicity the database already gives you for free — and a separate process, either a poller or a CDC tool reading the write-ahead log, publishes it afterward, retryable, decoupled from the original transaction. Neither pattern gets you exactly-once — the outbox guarantees at-least-once, so the consumer on the other end still needs to be idempotent."

| PT | EN |
|----|----|
| Fila de mensagens mortas | Dead letter queue (DLQ) |
| Exchange de mensagens mortas | Dead letter exchange (DLX) |
| Mensagem envenenada | Poison message |
| Problema de escrita dupla | Dual-write problem |
| Tabela de saída | Outbox table |
| Publicador por polling | Polling publisher |
| Captura de dados de mudança | Change data capture (CDC) |
| Reprocessamento em lote | Batch reprocessing |
| Confirmação negativa | Negative acknowledgment (nack) |

## O que vem a seguir

Esta nota fecha o galho de Mensageria em Python aplicando, com código real, a última peça que faltava entre "ferramenta escolhida" (nota 01) e "sistema confiável em produção": o que fazer quando falha, e como nunca ficar dessincronizado do banco. As próximas notas da trilha saem de mensageria e entram em como esses sistemas expõem uma API — o assunto natural depois de garantir que os eventos internos são confiáveis é garantir que a superfície HTTP também é.

- [[03-Dominios/Engenharia/Comunicação entre Sistemas/4 - Comunicação assíncrona/04 - Outbox e Saga|Outbox e Saga]] — a teoria completa do dual-write, Saga e compensação, que esta nota aplicou sem repetir.
- [[03-Dominios/Tecnologia/Python/Arquitetura e Design Patterns/04 - Unit of Work — formalizando o padrão que já existia|Unit of Work — formalizando o padrão que já existia]] — `AbstractUnitOfWork`, reaproveitada aqui para gravar o evento na mesma transação do negócio.

## Veja também

- [[03-Dominios/Tecnologia/Python/Mensageria/index|Mensageria (MOC do galho)]]
- [[01 - Panorama — Celery vs RQ vs aio-pika vs aiokafka|01 — Panorama: Celery vs RQ vs aio-pika vs aiokafka]] — onde este galho começou, comparando as quatro ferramentas que esta nota agora fecha aplicando garantias de entrega.
- [[03 - Celery em produção — retries, idempotência e Celery Beat|03 — Celery em produção: retries, idempotência e Celery Beat]] — o retry que esgota antes de uma mensagem chegar à DLQ manual do Celery, e a idempotência que o Outbox continua exigindo do consumer.
- [[05 - aio-pika — RabbitMQ assíncrono|05 — aio-pika: RabbitMQ assíncrono]] — `nack(requeue=False)`, `connect_robust()` e o `PublicadorDeEventos` reaproveitados aqui para publicar a partir do worker de polling.
- [[03-Dominios/Tecnologia/Python/Persistência de dados/index|Persistência de dados (Galho 9)]] — `Mapped`/`mapped_column` e a `Session` do SQLAlchemy que a tabela `OutboxEvent` reaproveita sem repetir a mecânica.

## Fontes

- RabbitMQ — [*Dead Lettering*](https://www.rabbitmq.com/docs/dlx) (acessado 2026-07-12) — `x-dead-letter-exchange`, `x-dead-letter-routing-key`, condições que disparam dead lettering (nack, TTL, tamanho máximo de fila).
- Celery — [*Tasks — Celery 5.6.3 documentation*](https://docs.celeryq.dev/en/stable/userguide/tasks.html) (acessado 2026-07-12) — `MaxRetriesExceededError`, `task_reject_on_worker_lost`, ausência de DLX nativa no framework.
- Celery — [*Configuration and defaults*](https://docs.celeryq.dev/en/stable/userguide/configuration.html) (acessado 2026-07-12) — `task_reject_on_worker_lost` e seu escopo real (rejeição por worker morto, não roteamento para fila de erro).
- [[03-Dominios/Engenharia/Comunicação entre Sistemas/4 - Comunicação assíncrona/04 - Outbox e Saga|Comunicação entre Sistemas — Outbox e Saga]] (2026-07-09) — definição canônica do dual-write problem, Outbox Pattern, Polling Publisher vs CDC, reaproveitada por referência nesta nota sem repetição.
- [[03-Dominios/Tecnologia/Python/Arquitetura e Design Patterns/04 - Unit of Work — formalizando o padrão que já existia|Unit of Work — formalizando o padrão que já existia]] (2026-07-12) — `AbstractUnitOfWork`, `SqlAlchemyUnitOfWork`, regra de commit explícito, reaproveitadas aqui para gravar o `OutboxEvent`.
- aio-pika docs — [*AsyncIO client for RabbitMQ*](https://aio-pika.readthedocs.io/) (acessado 2026-07-12) — declaração de exchange/queue com argumentos, `nack(requeue=False)`, base do exemplo de DLX desta nota.

Consultado em 2026-07-12.
