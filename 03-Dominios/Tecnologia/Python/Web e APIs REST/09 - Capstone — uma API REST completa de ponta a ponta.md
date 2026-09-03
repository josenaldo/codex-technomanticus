---
title: "Capstone — uma API REST completa de ponta a ponta"
created: 2026-07-11
type: concept
status: complete
fase: adepto
publish: true
tags:
  - python
  - web
  - fastapi
  - capstone
aliases:
  - "Capstone Galho 10 Python"
  - "API de tarefas de ponta a ponta"
  - "Fechamento Web e APIs REST"
---

# Capstone — uma API REST completa de ponta a ponta

> [!abstract] TL;DR
> Esta nota fecha o Galho 10 construindo, versão a versão, a API que só faz sentido depois de ler as oito notas anteriores: um serviço de tarefas multiusuário — `Usuario`/`Tarefa` — em **FastAPI**, consumindo a camada de persistência SQLAlchemy que o [[03-Dominios/Tecnologia/Python/Persistência de dados/index|Galho 9]] já construiu. Cada peça amarrada aqui já foi ensinada isoladamente: rotas organizadas em [[02 - Roteamento — decorators, urls.py e path operations|`APIRouter`]] (nota 02), entrada e saída separadas em modelos [[03 - Validação e serialização com Pydantic|Pydantic distintos]] (nota 03), sessão de banco injetada via [[04 - Injeção de dependência no FastAPI — Depends|`Depends()` com `yield`]] (nota 04), falhas de domínio traduzidas por um [[06 - Tratamento de erros e respostas HTTP padronizadas|exception handler central seguindo o contrato de erro proposto na nota 06]], e um [[07 - Middleware e o ciclo de vida da requisição|middleware de correlation ID e tempo de resposta]] (nota 07) observando toda requisição. Nada disso é conceito novo — esta nota não introduz mecanismo nenhum que as oito anteriores não tenham coberto; ela só os organiza na ordem em que uma API real precisa deles, e nomeia, ao final, exatamente o que falta (autenticação e autorização) para essa API deixar de ser um protótipo e virar um serviço que pode ser exposto de verdade.

## O cenário: uma API de tarefas amarra o galho inteiro

Um time pequeno precisa expor, via HTTP, o sistema de tarefas que várias notas deste galho já usaram como exemplo recorrente — a [[02 - Roteamento — decorators, urls.py e path operations|nota 02]] roteou um CRUD de tarefas nos três frameworks; a [[03 - Validação e serialização com Pydantic|nota 03]] mostrou o padrão `Create`/`Read` com o exemplo de usuário. Esta capstone junta os dois recursos — `Usuario` cria `Tarefa`s — numa API real, com persistência de verdade por trás, não mais um dicionário em memória como os exemplos didáticos das notas anteriores usaram para focar em um conceito de cada vez.

É o tipo de serviço que parece trivial em um protótipo de fim de semana e revela, uma a uma, exatamente as lacunas que este galho passou oito notas cobrindo:

- A primeira versão escreve tudo dentro de `main.py`, sem `APIRouter` — funciona com três endpoints, mas não escala além disso, o problema que a [[02 - Roteamento — decorators, urls.py e path operations|nota 02]] já descreveu para Flask/Django e que também se aplica ao FastAPI quando a API cresce.
- A segunda versão usa uma única classe Pydantic para entrada e saída — o mesmo incidente de abertura da [[03 - Validação e serialização com Pydantic|nota 03]], só que aqui o campo que vaza não é uma senha, é o `usuario_id` de outra pessoa, exposto num campo que deveria ser somente interno.
- A terceira versão abre a `Session` do SQLAlchemy manualmente dentro de cada handler — o bug de vazamento de conexão que abriu a [[04 - Injeção de dependência no FastAPI — Depends|nota 04]], só que agora contra o pool configurado no [[03-Dominios/Tecnologia/Python/Persistência de dados/07 - Connection pooling e performance em produção|Galho 9, nota 07]].
- A quarta versão deixa uma exceção de "tarefa não encontrada" subir crua, virando um `500` genérico com traceback — o incidente de três formatos de erro coexistindo que abriu a [[06 - Tratamento de erros e respostas HTTP padronizadas|nota 06]].
- A quinta versão não tem nenhuma forma de correlacionar logs de uma mesma requisição sob carga — o problema exato que o correlation ID da [[07 - Middleware e o ciclo de vida da requisição|nota 07]] resolve.

Cada uma dessas versões corrigidas corresponde a uma nota deste galho. O sistema desta capstone é a sexta versão — a que já nasce com as cinco correções embutidas, exatamente o mesmo movimento que a [[03-Dominios/Tecnologia/Python/Persistência de dados/08 - Capstone — projetando a camada de persistência de um serviço real|capstone do Galho 9]] fez para a camada de dados.

```mermaid
erDiagram
    USUARIO ||--o{ TAREFA : "cria"

    USUARIO {
        int id PK
        string nome
        string email UK
    }
    TAREFA {
        int id PK
        int usuario_id FK
        string titulo
        bool concluida
        datetime criada_em
    }
```

## Etapa 0: o modelo — consumindo o Galho 9 sem repeti-lo

O modelo ORM não é conteúdo novo desta nota — é exatamente o vocabulário de `DeclarativeBase`/`Mapped[]`/`relationship()` que o [[03-Dominios/Tecnologia/Python/Persistência de dados/02 - SQLAlchemy ORM — Session, mapped classes e relationships|Galho 9, nota 02]] já ensinou, aplicado ao par `Usuario`/`Tarefa` em vez de `Cliente`/`Pedido`:

```python
"""models.py — modelo ORM, reaproveitando o vocabulário do Galho 9."""

from __future__ import annotations

from datetime import datetime

from sqlalchemy import ForeignKey, String, UniqueConstraint
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Base(DeclarativeBase):
    pass


class Usuario(Base):
    __tablename__ = "usuarios"

    id: Mapped[int] = mapped_column(primary_key=True)
    nome: Mapped[str] = mapped_column(String(120))
    email: Mapped[str] = mapped_column(String(255))

    tarefas: Mapped[list["Tarefa"]] = relationship(back_populates="usuario")

    __table_args__ = (UniqueConstraint("email", name="uq_usuarios_email"),)


class Tarefa(Base):
    __tablename__ = "tarefas"

    id: Mapped[int] = mapped_column(primary_key=True)
    usuario_id: Mapped[int] = mapped_column(ForeignKey("usuarios.id"))
    titulo: Mapped[str] = mapped_column(String(200))
    concluida: Mapped[bool] = mapped_column(default=False)
    criada_em: Mapped[datetime] = mapped_column(default=datetime.utcnow)

    usuario: Mapped["Usuario"] = relationship(back_populates="tarefas")
```

Esta nota não reexplica `relationship(back_populates=...)`, o ciclo de vida `transient → pending → persistent → detached`, nem por que `Session` não é thread-safe — tudo isso já foi coberto em profundidade pelo Galho 9, e o único ponto novo que esta capstone acrescenta é **como** essa camada de dados é servida através de HTTP, não como ela funciona por dentro.

## Etapa 1: `APIRouter` — organizando antes de crescer

A [[02 - Roteamento — decorators, urls.py e path operations|nota 02 deste galho]] já mostrou `APIRouter` isoladamente; aqui ele é o ponto de partida real, não um exemplo didático — toda rota de tarefa nasce dentro de um módulo próprio, nunca direto em `main.py`:

```python
"""routers/tarefas.py — versão 1: só roteamento organizado, sem os outros mecanismos ainda."""

from fastapi import APIRouter

router = APIRouter(prefix="/tarefas", tags=["Tarefas"])

tarefas_db: dict[int, dict] = {}  # placeholder — substituído pela Session real na Etapa 3


@router.get("")
def listar_tarefas():
    return list(tarefas_db.values())


@router.post("", status_code=201)
def criar_tarefa(titulo: str):
    ...
```

```python
"""main.py"""

from fastapi import FastAPI

from routers.tarefas import router as tarefas_router

app = FastAPI(title="API de Tarefas")
app.include_router(tarefas_router)
```

`prefix="/tarefas"` e `tags=["Tarefas"]` fazem o mesmo papel que a nota 02 já descreveu: toda rota interna do router herda o prefixo, e a tag agrupa essas rotas na navegação do Swagger UI que a [[08 - Documentação automática com OpenAPI|nota 08]] cobre adiante. Esta primeira versão ainda tem os dois problemas nomeados no cenário de abertura — um único parâmetro solto (`titulo: str`) em vez de um modelo de entrada, e um dicionário em memória em vez de persistência real. As próximas quatro etapas resolvem, uma de cada vez, exatamente essas lacunas.

## Etapa 2: Pydantic — `TarefaCreate` e `TarefaRead` como contratos distintos

A [[03 - Validação e serialização com Pydantic|nota 03 deste galho]] já estabeleceu o padrão canônico — dois modelos por recurso, nunca um só fazendo os dois papéis — usando `UsuarioCreate`/`UsuarioRead` como exemplo. Aqui o mesmo padrão se aplica a `Tarefa`, com uma diferença que vale nomear: o campo que precisa ficar fora do modelo de entrada não é uma senha, é `usuario_id` — numa API sem autenticação ainda (o [[03-Dominios/Tecnologia/Python/Segurança/index|Galho 11]] resolve isso), o `usuario_id` do criador **não pode vir do corpo da requisição**, porque isso permitiria qualquer cliente criar uma tarefa em nome de outra pessoa só informando um ID diferente.

```python
"""schemas.py — modelos de entrada/saída, nunca a mesma classe para os dois papéis."""

from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class TarefaCreate(BaseModel):
    """O que o CLIENTE manda — nunca inclui usuario_id."""
    titulo: str = Field(min_length=1, max_length=200)


class TarefaRead(BaseModel):
    """O que o SERVIDOR devolve."""
    model_config = ConfigDict(from_attributes=True)  # constrói direto do objeto ORM (Galho 9)

    id: int
    usuario_id: int
    titulo: str
    concluida: bool
    criada_em: datetime
```

> [!warning] `usuario_id` em `TarefaCreate` é o mesmo erro estrutural do `hashed_password` na nota 03
> A [[03 - Validação e serialização com Pydantic|nota 03]] mostrou um `hashed_password` vazando na **saída** porque um único modelo servia entrada e saída. Aqui o risco é simétrico e na direção oposta: se `usuario_id` aparecesse em `TarefaCreate`, ele vazaria na **entrada** — qualquer cliente poderia mandar `{"titulo": "...", "usuario_id": 999}` e criar uma tarefa atribuída a outro usuário. O `usuario_id` de uma `Tarefa` nova vem sempre do contexto da requisição (de quem está autenticado, uma vez que o Galho 11 resolver isso), nunca de um campo que o próprio cliente controla — o mesmo princípio de "nunca confiar em dado que o chamador pode forjar" que atravessa autenticação, autorização e validação de entrada.

`ConfigDict(from_attributes=True)` em `TarefaRead` é o detalhe que a nota 03 já introduziu de passagem e que esta capstone usa de fato: permite construir `TarefaRead.model_validate(tarefa_orm)` direto a partir do objeto `Tarefa` do SQLAlchemy, sem passar por um dicionário intermediário escrito à mão — a ponte natural entre o modelo ORM da Etapa 0 e o modelo de resposta HTTP desta etapa.

## Etapa 3: `Depends(get_db)` — a sessão do Galho 9, injetada por requisição

A [[04 - Injeção de dependência no FastAPI — Depends|nota 04 deste galho]] já resolveu, em profundidade, o vazamento de `Session` que acontece quando ela é aberta manualmente dentro do handler — e já mostrou o padrão `get_db` exato que esta etapa aplica, consumindo o `Engine`/`sessionmaker` que o [[03-Dominios/Tecnologia/Python/Persistência de dados/02 - SQLAlchemy ORM — Session, mapped classes e relationships|Galho 9, nota 02]] ensinou a configurar:

```python
"""db.py — Engine e sessionmaker, configurados como o Galho 9, nota 07, ensinou."""

from collections.abc import Generator

from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

engine = create_engine(
    "postgresql+psycopg://app:senha@db.interno:5432/tarefas",
    pool_size=10,
    max_overflow=5,
    pool_timeout=30,
    pool_recycle=1800,
    pool_pre_ping=True,
)
SessionLocal = sessionmaker(bind=engine)


def get_db() -> Generator[Session, None, None]:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
```

```python
"""routers/tarefas.py — versão 3: Session injetada, persistência real."""

from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.orm import Session

from db import get_db
from models import Tarefa
from schemas import TarefaCreate, TarefaRead

router = APIRouter(prefix="/tarefas", tags=["Tarefas"])


@router.get("", response_model=list[TarefaRead])
def listar_tarefas(usuario_id: int, db: Session = Depends(get_db)):
    stmt = select(Tarefa).where(Tarefa.usuario_id == usuario_id)
    return db.scalars(stmt).all()


@router.post("", response_model=TarefaRead, status_code=201)
def criar_tarefa(dados: TarefaCreate, usuario_id: int, db: Session = Depends(get_db)):
    tarefa = Tarefa(usuario_id=usuario_id, titulo=dados.titulo)
    db.add(tarefa)
    db.commit()
    db.refresh(tarefa)
    return tarefa
```

`db: Session = Depends(get_db)` não menciona `SessionLocal`, `create_engine`, nem pool — toda essa mecânica já foi coberta pelo Galho 9 e é consumida aqui, não repetida. Vale nomear um detalhe honesto sobre esta versão: `usuario_id` ainda entra como query parameter, um espaço reservado propositalmente ingênuo — a forma correta e definitiva de saber "quem é o usuário fazendo esta requisição" é `Depends(get_usuario_atual)`, exatamente como a [[04 - Injeção de dependência no FastAPI — Depends|nota 04]] já adiantou na seção de autenticação, e que só faz sentido implementar depois que o [[03-Dominios/Tecnologia/Python/Segurança/index|Galho 11]] cobrir o mecanismo de token/sessão por trás dele. Esta capstone marca esse ponto explicitamente na síntese final, em vez de fingir que o problema já está resolvido.

```mermaid
sequenceDiagram
    participant Cliente
    participant FastAPI
    participant get_db as get_db() (dependência)
    participant Handler as criar_tarefa()
    participant DB as Banco (Galho 9)

    Cliente->>FastAPI: POST /tarefas {"titulo": "..."}
    FastAPI->>get_db: chama get_db()
    get_db->>get_db: db = SessionLocal() (setup)
    get_db-->>FastAPI: yield db
    FastAPI->>Handler: criar_tarefa(dados, usuario_id, db)
    Handler->>DB: INSERT INTO tarefas (...)
    DB-->>Handler: tarefa persistida (id atribuído)
    Handler-->>FastAPI: return tarefa (objeto ORM)
    FastAPI->>FastAPI: response_model=TarefaRead filtra/serializa
    FastAPI->>get_db: retoma após o yield
    get_db->>get_db: db.close() (teardown, garantido)
    FastAPI-->>Cliente: 201 {"id": 1, "usuario_id": ..., "titulo": ..., ...}
```

## Etapa 4: exceção de domínio + exception handler — o contrato da nota 06, aplicado

A [[06 - Tratamento de erros e respostas HTTP padronizadas|nota 06 deste galho]] já propôs, explicitamente para esta capstone, o envelope de erro `type`/`title`/`status`/`detail`/`instance`. Esta etapa aplica esse contrato: uma exceção de domínio pura para "tarefa não encontrada", sem nenhum import de FastAPI, e um `@app.exception_handler` central que a traduz.

```python
"""domain/exceptions.py — exceção pura, sem conhecimento de HTTP."""

class TarefaNaoEncontrada(Exception):
    def __init__(self, tarefa_id: int) -> None:
        self.tarefa_id = tarefa_id
        super().__init__(f"Tarefa {tarefa_id} não encontrada")


class TarefaNaoPertenceAoUsuario(Exception):
    def __init__(self, tarefa_id: int, usuario_id: int) -> None:
        self.tarefa_id = tarefa_id
        self.usuario_id = usuario_id
        super().__init__(f"Tarefa {tarefa_id} não pertence ao usuário {usuario_id}")
```

```python
"""routers/tarefas.py — versão 4: serviço de domínio levanta exceção pura, sem try/except na rota."""

from domain.exceptions import TarefaNaoEncontrada, TarefaNaoPertenceAoUsuario


def buscar_tarefa_do_usuario(db: Session, tarefa_id: int, usuario_id: int) -> Tarefa:
    tarefa = db.get(Tarefa, tarefa_id)
    if tarefa is None:
        raise TarefaNaoEncontrada(tarefa_id)
    if tarefa.usuario_id != usuario_id:
        raise TarefaNaoPertenceAoUsuario(tarefa_id, usuario_id)
    return tarefa


@router.patch("/{tarefa_id}/concluir", response_model=TarefaRead)
def concluir_tarefa(tarefa_id: int, usuario_id: int, db: Session = Depends(get_db)):
    tarefa = buscar_tarefa_do_usuario(db, tarefa_id, usuario_id)
    tarefa.concluida = True
    db.commit()
    db.refresh(tarefa)
    return tarefa
```

```python
"""main.py — exception handlers centrais, registrados uma vez, aplicados à API inteira."""

import logging

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from domain.exceptions import TarefaNaoEncontrada, TarefaNaoPertenceAoUsuario

logger = logging.getLogger("api")
app = FastAPI(title="API de Tarefas")


@app.exception_handler(TarefaNaoEncontrada)
def tratar_tarefa_nao_encontrada(request: Request, exc: TarefaNaoEncontrada):
    return JSONResponse(
        status_code=404,
        content={
            "type": "tarefa-nao-encontrada",
            "title": "Tarefa não encontrada",
            "status": 404,
            "detail": str(exc),
            "instance": str(request.url),
        },
    )


@app.exception_handler(TarefaNaoPertenceAoUsuario)
def tratar_tarefa_de_outro_usuario(request: Request, exc: TarefaNaoPertenceAoUsuario):
    return JSONResponse(
        status_code=404,  # 404, não 403 — não confirma a existência da tarefa a quem não é dono
        content={
            "type": "tarefa-nao-encontrada",
            "title": "Tarefa não encontrada",
            "status": 404,
            "detail": "Tarefa não encontrada",
            "instance": str(request.url),
        },
    )


@app.exception_handler(Exception)
def tratar_erro_nao_previsto(request: Request, exc: Exception):
    logger.exception("Erro não tratado em %s", request.url)
    return JSONResponse(
        status_code=500,
        content={
            "type": "erro-interno",
            "title": "Erro interno do servidor",
            "status": 500,
            "detail": "Ocorreu um erro inesperado. A equipe já foi notificada.",
            "instance": str(request.url),
        },
    )
```

> [!question]- Por que `TarefaNaoPertenceAoUsuario` também devolve 404, e não 403?
> Um `403 Forbidden` confirmaria implicitamente "esta tarefa existe, mas você não pode acessá-la" — informação que um cliente mal-intencionado poderia usar para enumerar IDs de tarefas de outros usuários só observando a diferença entre 403 (existe, não é sua) e 404 (não existe). Devolver 404 nos dois casos — tarefa inexistente ou tarefa de outro usuário — é uma prática comum em APIs que levam a sério não vazar a existência de um recurso que o solicitante não tem direito de ver, mesmo que isso pareça, à primeira vista, "menos preciso" que distinguir os dois casos. Essa é uma decisão de segurança, não de HTTP puro, e aparece com mais profundidade no [[03-Dominios/Tecnologia/Python/Segurança/index|Galho 11]] quando autorização por recurso for o assunto central — aqui vale só nomear a escolha e o motivo, sem desenvolver o mecanismo de autorização em si.

`buscar_tarefa_do_usuario` não sabe que está sendo chamada de dentro de uma rota HTTP — poderia ser chamada de um teste, de um script de manutenção, de um worker de fila — porque não importa nada de FastAPI. `concluir_tarefa` não tem `try/except` nenhum: a exceção sobe naturalmente do serviço de domínio até o handler registrado em `main.py`, exatamente o padrão que a nota 06 descreveu como "tradução centralizada, nunca `try/except` espalhado".

## Etapa 5: middleware — correlation ID e tempo de resposta

A [[07 - Middleware e o ciclo de vida da requisição|nota 07 deste galho]] já mostrou os dois casos de uso mais comuns de middleware em produção; esta etapa os aplica juntos, como a camada mais externa da API — a posição que garante que ambos rodam para **toda** requisição, incluindo as que os exception handlers da Etapa 4 acabam rejeitando:

```python
"""main.py — middleware de correlation ID e tempo de resposta."""

import time
import uuid
from contextvars import ContextVar

from fastapi import Request

correlation_id_var: ContextVar[str] = ContextVar("correlation_id", default="")


@app.middleware("http")
async def middleware_de_correlation_id_e_tempo(request: Request, call_next):
    correlation_id = request.headers.get("X-Correlation-ID", str(uuid.uuid4()))
    correlation_id_var.set(correlation_id)
    inicio = time.perf_counter()

    response = await call_next(request)

    duracao_ms = (time.perf_counter() - inicio) * 1000
    response.headers["X-Correlation-ID"] = correlation_id
    response.headers["X-Response-Time-Ms"] = f"{duracao_ms:.2f}"
    logger.info(
        "%s %s — %s — %sms",
        request.method, request.url.path, correlation_id, f"{duracao_ms:.2f}",
    )
    return response
```

Este único middleware resolve dois casos de uso que a nota 07 tratou separadamente: `correlation_id` amarra toda linha de log de uma requisição, o mesmo dado presente em qualquer resposta de erro do contrato da Etapa 4 via `instance`/logs correlacionados; `X-Response-Time-Ms` é o header de observabilidade mais básico de qualquer API em produção. Como é o único middleware registrado, a pergunta de ordem que a nota 07 levantou (qual `add_middleware`/`@app.middleware` fica mais externo) não se aplica ainda aqui — mas vale a nota: se um middleware de autenticação for adicionado depois (Galho 11), ele precisa ficar **mais interno** que este, para que o correlation ID e o tempo de resposta continuem cobrindo até as requisições rejeitadas por token inválido — o mesmo raciocínio do incidente de abertura da nota 07.

> [!tip] `logger.exception` do handler de `Exception` já se beneficia do correlation ID
> Como `correlation_id_var` é um `ContextVar`, um `logging.Filter` configurado no logger da aplicação (mecanismo já descrito na nota 07, não repetido aqui) injeta o `correlation_id` em **toda** linha de log emitida durante aquela requisição — incluindo o `logger.exception(...)` do handler de erro genérico da Etapa 4. Isso fecha o círculo do incidente de abertura da nota 06: um erro 500 inesperado, investigado depois via log, já vem correlacionado com a requisição exata que o causou, sem precisar cruzar timestamp manualmente.

## O sistema completo

Juntando as cinco etapas — modelo consumindo o Galho 9 (0), `APIRouter` (1), `TarefaCreate`/`TarefaRead` distintos (2), `Depends(get_db)` (3), exceção de domínio + exception handler central (4), middleware de correlation ID e tempo (5) — a API fica assim, de ponta a ponta:

```python
"""main.py — API de Tarefas, completa."""

import logging
import time
import uuid
from contextvars import ContextVar

from fastapi import Depends, FastAPI, Request
from fastapi.responses import JSONResponse
from sqlalchemy import select
from sqlalchemy.orm import Session

from db import get_db
from domain.exceptions import TarefaNaoEncontrada, TarefaNaoPertenceAoUsuario
from models import Tarefa
from schemas import TarefaCreate, TarefaRead

logger = logging.getLogger("api")
correlation_id_var: ContextVar[str] = ContextVar("correlation_id", default="")

app = FastAPI(title="API de Tarefas", version="1.0.0")


@app.middleware("http")
async def middleware_de_correlation_id_e_tempo(request: Request, call_next):
    correlation_id = request.headers.get("X-Correlation-ID", str(uuid.uuid4()))
    correlation_id_var.set(correlation_id)
    inicio = time.perf_counter()
    response = await call_next(request)
    duracao_ms = (time.perf_counter() - inicio) * 1000
    response.headers["X-Correlation-ID"] = correlation_id
    response.headers["X-Response-Time-Ms"] = f"{duracao_ms:.2f}"
    logger.info("%s %s — %s — %sms", request.method, request.url.path, correlation_id, f"{duracao_ms:.2f}")
    return response


@app.exception_handler(TarefaNaoEncontrada)
def tratar_tarefa_nao_encontrada(request: Request, exc: TarefaNaoEncontrada):
    return JSONResponse(status_code=404, content={
        "type": "tarefa-nao-encontrada", "title": "Tarefa não encontrada",
        "status": 404, "detail": str(exc), "instance": str(request.url),
    })


@app.exception_handler(TarefaNaoPertenceAoUsuario)
def tratar_tarefa_de_outro_usuario(request: Request, exc: TarefaNaoPertenceAoUsuario):
    return JSONResponse(status_code=404, content={
        "type": "tarefa-nao-encontrada", "title": "Tarefa não encontrada",
        "status": 404, "detail": "Tarefa não encontrada", "instance": str(request.url),
    })


@app.exception_handler(Exception)
def tratar_erro_nao_previsto(request: Request, exc: Exception):
    logger.exception("Erro não tratado em %s", request.url)
    return JSONResponse(status_code=500, content={
        "type": "erro-interno", "title": "Erro interno do servidor",
        "status": 500, "detail": "Ocorreu um erro inesperado. A equipe já foi notificada.",
        "instance": str(request.url),
    })


def buscar_tarefa_do_usuario(db: Session, tarefa_id: int, usuario_id: int) -> Tarefa:
    tarefa = db.get(Tarefa, tarefa_id)
    if tarefa is None:
        raise TarefaNaoEncontrada(tarefa_id)
    if tarefa.usuario_id != usuario_id:
        raise TarefaNaoPertenceAoUsuario(tarefa_id, usuario_id)
    return tarefa


router = APIRouter(prefix="/tarefas", tags=["Tarefas"])


@router.get(
    "", response_model=list[TarefaRead],
    summary="Lista as tarefas de um usuário",
)
def listar_tarefas(usuario_id: int, db: Session = Depends(get_db)):
    stmt = select(Tarefa).where(Tarefa.usuario_id == usuario_id)
    return db.scalars(stmt).all()


@router.post(
    "", response_model=TarefaRead, status_code=201,
    summary="Cria uma nova tarefa",
)
def criar_tarefa(dados: TarefaCreate, usuario_id: int, db: Session = Depends(get_db)):
    tarefa = Tarefa(usuario_id=usuario_id, titulo=dados.titulo)
    db.add(tarefa)
    db.commit()
    db.refresh(tarefa)
    return tarefa


@router.patch(
    "/{tarefa_id}/concluir", response_model=TarefaRead,
    summary="Marca uma tarefa como concluída",
)
def concluir_tarefa(tarefa_id: int, usuario_id: int, db: Session = Depends(get_db)):
    tarefa = buscar_tarefa_do_usuario(db, tarefa_id, usuario_id)
    tarefa.concluida = True
    db.commit()
    db.refresh(tarefa)
    return tarefa


@router.delete(
    "/{tarefa_id}", status_code=204,
    summary="Remove uma tarefa",
)
def remover_tarefa(tarefa_id: int, usuario_id: int, db: Session = Depends(get_db)):
    tarefa = buscar_tarefa_do_usuario(db, tarefa_id, usuario_id)
    db.delete(tarefa)
    db.commit()


app.include_router(router)
```

Rodar `uvicorn main:app --reload` contra um Postgres local (ou o SQLite de teste que o Galho 9 já ensinou a usar como banco descartável) e chamar `GET /docs` já entrega, sem nenhuma linha de documentação escrita à mão, a spec inteira dessa API — os schemas `TarefaCreate`/`TarefaRead`, os quatro endpoints com seus status codes de sucesso, e (como a [[08 - Documentação automática com OpenAPI|nota 08]] já ensinou) espaço para enriquecer com `description`/`tags` sem sair do próprio decorator de rota. O que essa spec **não** documenta ainda de graça são as respostas de erro 404/500 — a nota 08 já nomeou essa lacuna: documentar `responses={404: {...}}` explicitamente no decorator é um passo manual a mais, não coberto por esta capstone para não alongar o exemplo, mas seguindo exatamente o mesmo mecanismo que a nota 08 descreveu.

```mermaid
flowchart TB
    classDef marca fill:#8855DF33,stroke:#8855DF,color:#E9ECF2
    classDef neutro fill:#1B2029,stroke:#4E5666,color:#C6CCD8
    classDef destaque fill:#FFAA0024,stroke:#FFAA00,color:#E9ECF2
    subgraph Entrada["Camada transversal — roda em toda requisição"]
        MW["middleware_de_correlation_id_e_tempo\n(nota 07)"]
    end

    subgraph Rota["Camada de API"]
        ROUTER["APIRouter /tarefas\n(nota 02)"]
        VALID["TarefaCreate valida entrada\nTarefaRead filtra saída\n(nota 03)"]
        DEP["Depends(get_db)\nSession por requisição\n(nota 04)"]
    end

    subgraph Dominio["Camada de domínio — não conhece HTTP"]
        SERVICO["buscar_tarefa_do_usuario()"]
        ORM["Tarefa / Usuario\nSQLAlchemy (Galho 9)"]
    end

    subgraph Erro["Tradução centralizada"]
        EH["@app.exception_handler\n(nota 06)"]
    end

    subgraph Doc["Subproduto gratuito"]
        OPENAPI["/docs, /redoc, /openapi.json\n(nota 08)"]
    end

    MW --> ROUTER --> VALID --> DEP --> SERVICO --> ORM
    SERVICO -->|"exceção de domínio"| EH
    VALID -.->|"type hints + BaseModel"| OPENAPI

    class MW neutro
    class DEP neutro
    class EH marca
    class OPENAPI destaque
```

## Armadilhas comuns

> [!warning] Deixar `usuario_id` como query parameter em vez de derivá-lo da autenticação
> **O que acontece:** exatamente o que esta capstone faz deliberadamente, como espaço reservado — `usuario_id: int` chega como query parameter, e qualquer cliente pode listar, criar ou concluir tarefas em nome de qualquer outro usuário, só trocando o valor. **Por quê:** sem um mecanismo de autenticação, não existe forma de a API saber quem está de fato fazendo a requisição — confiar num campo que o próprio cliente informa é o oposto de autenticação. **Como evitar:** substituir `usuario_id: int` (query param) por `usuario: Usuario = Depends(get_usuario_atual)` assim que o [[03-Dominios/Tecnologia/Python/Segurança/index|Galho 11]] cobrir o mecanismo — `Depends()`, como a [[04 - Injeção de dependência no FastAPI — Depends|nota 04]] já mostrou, é o mesmo lugar estrutural onde essa substituição acontece, sem tocar na lógica de negócio das rotas.

> [!warning] `response_model` esquecido numa rota nova
> **O que acontece:** um desenvolvedor adiciona um endpoint novo (por exemplo, `GET /tarefas/{id}`, não incluído nesta capstone por brevidade) e esquece `response_model=TarefaRead` — o FastAPI serializa o retorno como veio, incluindo qualquer campo que o objeto ORM carregue e que `TarefaRead` não deveria expor. **Por quê:** sem `response_model` explícito, não existe peneira — o retorno da função vira JSON diretamente, exatamente o incidente de abertura da [[03 - Validação e serialização com Pydantic|nota 03]]. **Como evitar:** todo endpoint que retorna dado de domínio declara `response_model` explicitamente, revisado como parte do checklist de PR, não como responsabilidade individual de lembrança.

> [!warning] Exception handler `Exception` genérico devolvendo `str(exc)` "para debugar mais rápido"
> **O que acontece:** durante desenvolvimento, alguém troca `"detail": "Ocorreu um erro inesperado..."` por `"detail": str(exc)` "só pra ver o erro real mais rápido", e esquece de reverter antes do deploy. **Por quê:** é exatamente o vazamento de traceback/detalhe interno que a [[06 - Tratamento de erros e respostas HTTP padronizadas|nota 06]] tratou como falha de segurança, não de UX. **Como evitar:** o handler de `Exception` genérica nunca interpola `str(exc)` na resposta — só em `logger.exception(...)`, que fica só no servidor; qualquer necessidade de ver o erro real durante desenvolvimento local passa por olhar o log, nunca por mudar o contrato de resposta.

## Em entrevista

A pergunta "desenhe uma API REST em FastAPI para X" (X sendo qualquer domínio simples) testa se a pessoa amarra os mecanismos isolados numa arquitetura coerente, ou se trata "escrever um endpoint que funciona" como suficiente.

> "I'd start with routes organized in an `APIRouter`, not everything flat in the main module — one router per resource, mounted with `include_router()`. Every resource gets two Pydantic models, never one: a `Create` schema for what comes in, a `Read` schema for what goes out, wired through `response_model` so the response is filtered by contract, not by trusting whatever the function happens to return. Database access goes through a `Depends()` dependency using `yield` — setup before the yield, teardown in a `finally` after it — so a session is guaranteed to close even if the handler raises, instead of leaking a connection on every early return. Business logic raises plain Python exceptions that know nothing about HTTP, and a small number of `@app.exception_handler` functions, registered once at the top level, translate those into a consistent error envelope — type, title, status, detail — so no route needs its own try/except, and no two endpoints format failure differently. A single middleware, registered as the outermost layer, stamps every request with a correlation ID and a response-time header, so both successful and rejected requests are traceable in logs. And the OpenAPI docs at `/docs` are a side effect of that same code — the schemas, the response models, the type hints — not a separate artifact somebody has to remember to update. What's explicitly missing from that design, and what I'd name unprompted, is authentication: nothing here proves who's calling, so an early version of a resource-scoped field like `usuario_id` has to be treated as a placeholder, replaced by a dependency that reads a real token before this ever goes to production."

> [!question]- O entrevistador pergunta: "o que você tiraria dessa arquitetura para simplificar, se o time fosse pequeno e o prazo curto?"
> A resposta madura nomeia o que é **estrutural** (não deveria ser cortado, mesmo sob pressão de prazo) e o que é **incremental** (pode esperar). `APIRouter`, dois modelos por recurso, e `Depends(get_db)` com `yield` são estruturais — cortá-los custa caro depois, porque virar `Session` manual ou modelo único é o tipo de dívida técnica que se espalha por toda rota nova adicionada enquanto a dívida não é paga. Exception handler central e middleware de correlation ID são valiosos desde o primeiro endpoint, mas o custo de adicioná-los depois é menor — uma refatoração localizada, não espalhada pelo código de negócio. `summary`/`description`/`tags` ricos na documentação, e `responses={...}` explícitos para os erros na spec OpenAPI, são os candidatos mais razoáveis a adiar sob prazo curto, porque a documentação básica (`/docs` funcionando, ainda que menos rica) já vem de graça sem esse investimento extra.

## How to explain in English

> A real REST API isn't one decision, it's five layered ones, and skipping any of them still works in a demo — it just fails the first time the API meets a second developer, a concurrent request, or an unexpected input. Routes belong in an `APIRouter`, not flat in the entrypoint module, so the codebase can grow past a handful of endpoints without becoming unreadable. Every resource needs two Pydantic models, never one — input and output are different contracts, and conflating them is how a password hash or another user's internal ID ends up where it shouldn't. Database access flows through a `yield`-based dependency, guaranteeing cleanup regardless of how the handler exits, instead of manual open/close calls that leak the first time an early return skips the close. Domain logic raises plain exceptions with zero HTTP awareness, translated to a consistent error envelope by a small number of centrally registered handlers — no route reinvents its own error shape, and no unhandled exception leaks a stack trace to the client. A single outermost middleware stamps every request — successful or rejected — with a correlation ID and timing, so production incidents are traceable instead of guessed at. And free, always-accurate OpenAPI docs fall out of the same type hints and models used for validation, not a separate artifact anyone has to remember to update. What's still missing from a stack built this way is authentication and authorization — nothing here proves who's calling, and that gap is exactly where the next stage of the journey picks up.

| PT-BR | English |
|---|---|
| API de ponta a ponta | end-to-end API |
| espaço reservado (placeholder) | placeholder |
| contrato de erro | error contract |
| camada transversal | cross-cutting layer |
| subproduto gratuito | free byproduct |
| dívida técnica | technical debt |
| checklist de PR | PR checklist |

## Síntese — o que este galho ensinou, amarrado

Recapitulando o que as nove notas cobriram juntas:

1. [[01 - Django vs FastAPI vs Flask — panorama e filosofias|01 — Django vs. FastAPI vs. Flask]] abriu o galho com o panorama comparativo — por que esta capstone escolheu FastAPI: tipagem como contrato, `Depends()` leve, documentação de graça.
2. [[02 - Roteamento — decorators, urls.py e path operations|02 — Roteamento]] ensinou `APIRouter`, aplicado aqui como a organização de base de toda rota de tarefa.
3. [[03 - Validação e serialização com Pydantic|03 — Validação e serialização com Pydantic]] ensinou `Create`/`Read` distintos e `response_model`, aplicados aqui a `TarefaCreate`/`TarefaRead`.
4. [[04 - Injeção de dependência no FastAPI — Depends|04 — Injeção de dependência no FastAPI]] ensinou `Depends()` com `yield`, aplicado aqui a `get_db()` consumindo o Galho 9.
5. [[05 - Django REST Framework — serializers, viewsets e routers|05 — Django REST Framework]] mostrou o caminho paralelo em Django — não aplicado nesta capstone (que escolheu FastAPI), mas o contraste que informa a escolha de stack.
6. [[06 - Tratamento de erros e respostas HTTP padronizadas|06 — Tratamento de erros e respostas HTTP padronizadas]] propôs o contrato de erro que esta capstone implementou de ponta a ponta, com `TarefaNaoEncontrada`/`TarefaNaoPertenceAoUsuario`.
7. [[07 - Middleware e o ciclo de vida da requisição|07 — Middleware e o ciclo de vida da requisição]] ensinou o modelo de cebola e o correlation ID, aplicado aqui como a camada mais externa da API.
8. [[08 - Documentação automática com OpenAPI|08 — Documentação automática com OpenAPI]] mostrou que a spec nasce dos mesmos type hints já escritos — nada precisou ser escrito a mais nesta capstone para `/docs` funcionar.
9. Esta nota fechou amarrando as cinco peças — roteamento, validação, injeção de dependência, tratamento de erro, middleware — numa API real, sem introduzir mecanismo novo, só integração, exatamente como a [[03-Dominios/Tecnologia/Python/Persistência de dados/08 - Capstone — projetando a camada de persistência de um serviço real|capstone do Galho 9]] fez para a camada de dados que esta API consome.

Juntas, essas nove notas formam **como servir, pela rede, o que o Galho 9 já sabe persistir** — não mais "como validar um campo" ou "como abrir uma sessão de banco" isoladamente, mas como organizar essas peças numa API que um segundo desenvolvedor consegue entender, estender e não quebrar.

## O que vem a seguir

Esta capstone deliberadamente não introduziu autenticação nem autorização — o `usuario_id` como query parameter, nomeado explicitamente como espaço reservado nas Etapas 3 e 4, é a lacuna mais visível que sobra desta API. Não é um descuido: é o ponto exato onde este galho termina e o próximo começa.

- **[[03-Dominios/Tecnologia/Python/Segurança/index|Galho 11 — Segurança]]** (próximo) — a API construída aqui não sabe quem está fazendo cada requisição; o Galho 11 cobre autenticação (provar identidade — JWT, sessão, API key) e autorização (decidir o que essa identidade pode fazer), substituindo `usuario_id: int` por `Depends(get_usuario_atual)` de forma real, e aprofundando a decisão 404-em-vez-de-403 desta capstone sob a lente de controle de acesso por recurso.
- [[03-Dominios/Tecnologia/Python/Testes/index|Galho 12 — Testes]] — `app.dependency_overrides`, já citado na nota 04, é o mecanismo que torna esta API testável sem banco real; a mecânica completa de `TestClient`/fixtures pertence a esse galho.
- [[03-Dominios/Tecnologia/Python/Arquitetura e Design Patterns/index|Galho 13 — Arquitetura e Design Patterns]] — `buscar_tarefa_do_usuario()` já se comporta, informalmente, como uma função de Repository; esse galho nomeia e formaliza esse padrão, em cima exatamente do que esta capstone e a capstone do Galho 9 já construíram.
- [[03-Dominios/Tecnologia/Python/index|Trilha Python]] — MOC da trilha.
- [[index|Web e APIs REST (Galho 10)]] — MOC deste galho.

## Fontes

- FastAPI. *Bigger Applications — Multiple Files*. fastapi.tiangolo.com/tutorial/bigger-applications/. https://fastapi.tiangolo.com/tutorial/bigger-applications/ (acessado em 2026-07-11) — organização de `APIRouter` em múltiplos módulos, o padrão estrutural desta capstone.
- FastAPI. *SQL (Relational) Databases*. fastapi.tiangolo.com/tutorial/sql-databases/. https://fastapi.tiangolo.com/tutorial/sql-databases/ (acessado em 2026-07-11) — padrão canônico de integração FastAPI + SQLAlchemy via `Depends()`.
- FastAPI. *Handling Errors* / *Response Model*. fastapi.tiangolo.com. https://fastapi.tiangolo.com/tutorial/handling-errors/ (acessado em 2026-07-11) — exception handlers e `response_model`, aplicados de ponta a ponta nesta capstone.
- Mendes, Eduardo (Dunossauro). *FastAPI do Zero*. fastapidozero.dunossauro.com. https://fastapidozero.dunossauro.com/ (acessado em 2026-07-11) — referência canônica da comunidade brasileira para o padrão idiomático de uma API FastAPI completa (router, schema, dependência, teste).
- Real Python. *Build a Full-Stack FastAPI Application*. realpython.com. https://realpython.com/ (acessado em 2026-07-11) — arquitetura de referência de uma API FastAPI de ponta a ponta.
- [[01 - Django vs FastAPI vs Flask — panorama e filosofias|01]], [[02 - Roteamento — decorators, urls.py e path operations|02]], [[03 - Validação e serialização com Pydantic|03]], [[04 - Injeção de dependência no FastAPI — Depends|04]], [[05 - Django REST Framework — serializers, viewsets e routers|05]], [[06 - Tratamento de erros e respostas HTTP padronizadas|06]], [[07 - Middleware e o ciclo de vida da requisição|07]], [[08 - Documentação automática com OpenAPI|08]] — as oito notas irmãs deste galho, cada uma fonte primária dos mecanismos amarrados nesta capstone.
- [[03-Dominios/Tecnologia/Python/Persistência de dados/08 - Capstone — projetando a camada de persistência de um serviço real|Persistência de dados 08 — Capstone]] — a capstone irmã do Galho 9, cuja camada de dados esta API consome diretamente, e cujo padrão estrutural de fechamento (versões incrementais, uma por nota) esta nota reaproveita.

Consultado em 2026-07-11.
