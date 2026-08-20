---
title: "Capstone — hardening da API do Galho 10"
created: 2026-07-11
type: concept
status: complete
fase: magus
publish: true
tags:
  - python
  - seguranca
  - fastapi
  - owasp
  - capstone
aliases:
  - "Capstone Galho 11 Python"
  - "Hardening da API de tarefas"
  - "Fechamento Segurança"
---

# Capstone — hardening da API do Galho 10

> [!abstract] TL;DR
> Esta nota fecha o Galho 11 pegando a API de Tarefas construída na [[03-Dominios/Tecnologia/Python/Web e APIs REST/09 - Capstone — uma API REST completa de ponta a ponta|capstone do Galho 10]] — funcional, bem organizada, mas **deliberadamente ingênua em segurança**, com `usuario_id` como query param e nenhuma das oito lições deste galho aplicada — e a blinda em seis etapas incrementais, cada uma amarrando uma nota já ensinada: **autenticação real** com `Depends(get_current_user)` (nota 05, reusando o mecanismo de [[03-Dominios/Engenharia/Auth e Identidade/4 - Auth nos stacks/03 - Python — FastAPI|Auth e Identidade SG4]]); **correção de Broken Access Control** filtrando toda query por dono, com 404 uniforme em vez de 403 (nota 05); **correção de uma SSTI introduzida de propósito** num endpoint novo de busca com highlight (nota 02); **secrets movidos para `pydantic-settings`** (nota 06); **rate limiting no cadastro e no login** com `slowapi` (nota 08); e **validação de segurança revisitada** no campo de anexo de tarefa, separando forma de destino (nota 04). Nenhuma etapa introduz mecanismo novo — cada uma só aplica, ao código real do Galho 10, o que uma nota específica deste galho já desenvolveu em profundidade. Ao final, a API que saiu do Galho 10 pronta para um pentest reprovar sai desta nota pronta para o próximo passo natural: uma suíte de testes automatizados que prove, de forma repetível, que cada correção continua valendo.

## O pentest marcado para sexta-feira

A API de Tarefas do [[03-Dominios/Tecnologia/Python/Web e APIs REST/09 - Capstone — uma API REST completa de ponta a ponta|capstone do Galho 10]] está rodando em staging há duas semanas. Ela tem tudo que aquela capstone se propôs a entregar — `APIRouter` organizado, `TarefaCreate`/`TarefaRead` como contratos distintos, `Depends(get_db)` sem vazamento de sessão, exceção de domínio traduzida por exception handler central, middleware de correlation ID. O time está satisfeito: os testes manuais passam, o Swagger UI documenta os quatro endpoints, o CI está verde.

Só que aquela mesma capstone terminou com uma confissão explícita, na seção final: `usuario_id` continua chegando como **query parameter**, um espaço reservado propositalmente ingênuo, porque autenticação real ainda não existia na trilha. Qualquer cliente que chame `GET /tarefas?usuario_id=7` recebe as tarefas do usuário 7 — não importa quem realmente fez a requisição. É o mesmo `usuario_id` que o [[01 - OWASP Top 10 aplicado a Python web — o mapa|mapa deste galho]] já usou como cenário de abertura, e é exatamente o tipo de lacuna que um pentest contratado antes de assinar um cliente enterprise — o mesmo pentest citado em quase toda nota deste galho — encontra em minutos, não em dias.

O pentest está marcado para sexta-feira. Esta nota é o trabalho de terça a quinta: pegar a API do Galho 10 e aplicar, uma de cada vez, as oito lições que este galho ensinou — não como teoria isolada, mas como diffs concretos no código real que já existe.

> [!question]- Por que não simplesmente reescrever a API do zero, já segura?
> Porque isso esconderia exatamente o que esta nota existe para mostrar: quais decisões específicas do Galho 10 precisam mudar, e por quê. Reescrever do zero produziria uma API segura, mas sem o rastro que liga cada correção a um incidente concreto — o mesmo raciocínio que fez as capstones dos Galhos 9 e 10 evoluírem código existente em vez de apresentar a versão final pronta. Segurança se aprende vendo o "antes" quebrar e o "depois" resistir, não só lendo a versão final.

```mermaid
%%{init: {"theme": "base", "themeVariables": {"primaryColor": "#4A90D9"}}}%%
flowchart LR
    G10["API do Galho 10\n(funcional, ingênua)"] --> E1["Etapa 1\nAuth real (N05)"]
    E1 --> E2["Etapa 2\nBroken Access Control (N05)"]
    E2 --> E3["Etapa 3\nSSTI corrigida (N02)"]
    E3 --> E4["Etapa 4\nSecrets tipados (N06)"]
    E4 --> E5["Etapa 5\nRate limiting (N08)"]
    E5 --> E6["Etapa 6\nValidação revisitada (N04)"]
    E6 --> API["API blindada\npronta para pentest"]

    style G10 fill:#8b6914,color:#fff
    style API fill:#2d7a4a,color:#fff
```

## Etapa 0: o que muda no modelo — `Usuario` ganha uma senha

A API do Galho 10 tinha um `Usuario` sem nenhum campo de credencial — fazia sentido, porque autenticação ainda não existia na trilha. O primeiro ajuste, antes de qualquer lógica nova, é o modelo ORM ganhar o campo que a autenticação real vai precisar:

```python
"""models.py — o mesmo Usuario do Galho 10, com um campo novo."""

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
    senha_hash: Mapped[str] = mapped_column(String(255))  # NOVO — nunca a senha em texto puro

    tarefas: Mapped[list["Tarefa"]] = relationship(back_populates="usuario")

    __table_args__ = (UniqueConstraint("email", name="uq_usuarios_email"),)


class Tarefa(Base):
    __tablename__ = "tarefas"

    id: Mapped[int] = mapped_column(primary_key=True)
    usuario_id: Mapped[int] = mapped_column(ForeignKey("usuarios.id"))
    titulo: Mapped[str] = mapped_column(String(200))
    concluida: Mapped[bool] = mapped_column(default=False)
    anexo_url: Mapped[str | None] = mapped_column(String(500), default=None)  # NOVO — Etapa 6
    criada_em: Mapped[datetime] = mapped_column(default=datetime.utcnow)

    usuario: Mapped["Usuario"] = relationship(back_populates="tarefas")
```

`senha_hash` nunca guarda a senha em texto puro — o mecanismo de hash é o mesmo `pwdlib`/`PasswordHash.recommended()` (Argon2id por padrão) já cravado em [[03-Dominios/Engenharia/Auth e Identidade/4 - Auth nos stacks/03 - Python — FastAPI|Auth e Identidade SG4]], não repetido aqui. `anexo_url` é o campo que a Etapa 6 desenvolve — um link opcional que o usuário anexa à tarefa (um documento, uma imagem de referência), a peça que traz de volta a discussão de validação de segurança da [[04 - Validação de input como controle de segurança|nota 04]].

## Etapa 1: autenticação real — `usuario_id` deixa de ser query param

A [[05 - Autenticação e autorização na prática — a ponte com Auth e Identidade|nota 05 deste galho]] já mostrou exatamente onde `Depends(get_current_user)` se encaixa na árvore de dependências que o Galho 10 ensinou, e a [[03-Dominios/Engenharia/Auth e Identidade/4 - Auth nos stacks/03 - Python — FastAPI|nota de Auth e Identidade SG4]] já resolveu o mecanismo interno — `OAuth2PasswordBearer`, `PyJWT`, `pwdlib`. Esta etapa não reexplica nenhuma das duas; só aplica o que as duas já ensinaram ao código concreto da API de Tarefas.

```python
"""auth.py — mecanismo reusado de Auth e Identidade SG4, sem repetir uma linha dele."""

from datetime import datetime, timedelta, timezone
from typing import Annotated

import jwt
from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from pwdlib import PasswordHash
from sqlalchemy import select
from sqlalchemy.orm import Session

from config import settings  # Etapa 4 — pydantic-settings
from db import get_db
from models import Usuario

password_hash = PasswordHash.recommended()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


class NaoAutenticado(Exception):
    """Exceção de domínio pura — sem import de FastAPI, mesmo padrão da nota 05."""


def hash_senha(senha_plana: str) -> str:
    return password_hash.hash(senha_plana)


def verificar_senha(senha_plana: str, senha_hash: str) -> bool:
    return password_hash.verify(senha_plana, senha_hash)


def criar_access_token(usuario_id: int, expira_em_minutos: int = 15) -> str:
    agora = datetime.now(timezone.utc)
    payload = {
        "sub": str(usuario_id),
        "iat": agora,
        "exp": agora + timedelta(minutes=expira_em_minutos),
    }
    return jwt.encode(payload, settings.jwt_secret, algorithm=settings.jwt_algorithm)


def get_current_user(
    token: Annotated[str, Depends(oauth2_scheme)],
    db: Session = Depends(get_db),
) -> Usuario:
    try:
        payload = jwt.decode(token, settings.jwt_secret, algorithms=[settings.jwt_algorithm])
    except jwt.InvalidTokenError:
        raise NaoAutenticado("Token ausente, expirado ou inválido")

    usuario = db.scalar(select(Usuario).where(Usuario.id == int(payload["sub"])))
    if usuario is None:
        raise NaoAutenticado("Usuário do token não existe mais")
    return usuario
```

O único ponto novo — porque a API do Galho 10 nunca teve um endpoint de cadastro nem de login — são os dois endpoints que emitem o token que `get_current_user` consome:

```python
"""routers/auth.py — cadastro e login, os dois pontos de entrada da autenticação."""

from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy import select
from sqlalchemy.orm import Session

from auth import criar_access_token, hash_senha, verificar_senha
from db import get_db
from models import Usuario
from schemas import UsuarioCreate, UsuarioRead

router = APIRouter(tags=["Autenticação"])


@router.post("/usuarios", response_model=UsuarioRead, status_code=201)
def cadastrar_usuario(dados: UsuarioCreate, db: Session = Depends(get_db)):
    usuario = Usuario(nome=dados.nome, email=dados.email, senha_hash=hash_senha(dados.senha))
    db.add(usuario)
    db.commit()
    db.refresh(usuario)
    return usuario


@router.post("/token")
def login(form: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    usuario = db.scalar(select(Usuario).where(Usuario.email == form.username))
    if usuario is None or not verificar_senha(form.password, usuario.senha_hash):
        raise HTTPException(status_code=401, detail="Credenciais inválidas")
    return {"access_token": criar_access_token(usuario.id), "token_type": "bearer"}
```

`UsuarioCreate` segue o mesmo princípio já cravado no Galho 10, nota 03, e revisitado na [[02 - Injeção — SQL, template, comando e deserialização insegura|nota 02]]: `senha` é um campo de **entrada**, nunca de saída — `UsuarioRead` não tem `senha_hash` nem `senha` em lugar nenhum, exatamente o incidente de vazamento de `hashed_password` que a nota 03 do Galho 10 abriu.

> [!warning] `OAuth2PasswordRequestForm` espera `application/x-www-form-urlencoded`, não JSON
> Um erro comum ao ligar `/token` pela primeira vez: o cliente manda `{"username": "...", "password": "..."}` como JSON, e o FastAPI devolve `422` porque `OAuth2PasswordRequestForm` — a classe que `fastapi.security` fornece especificamente para esse endpoint — espera dados de formulário (`username`/`password` como campos de form, não de body JSON), seguindo a especificação OAuth2 que [[03-Dominios/Engenharia/Auth e Identidade/4 - Auth nos stacks/03 - Python — FastAPI|Auth e Identidade SG4]] já documentou. Não é um bug da API — é o contrato esperado do fluxo `password grant`, e o Swagger UI já sabe disso e monta o formulário certo automaticamente.

Com `auth.py` e os dois endpoints em pé, toda rota da API de Tarefas troca `usuario_id: int` (query param) por `current_user: Annotated[Usuario, Depends(get_current_user)]` — a mudança de assinatura, sozinha, já fecha o `401` para quem não tem token válido. Mas, como a [[05 - Autenticação e autorização na prática — a ponte com Auth e Identidade|nota 05]] insiste em nomear, **autenticado não é autorizado** — e é exatamente por isso que a Etapa 2 não é opcional.

## Etapa 2: Broken Access Control — cada endpoint filtra por dono

O erro mais comum documentado na nota 05 é `current_user` presente na assinatura e nunca usado dentro do handler. Esta etapa corrige, endpoint por endpoint, os quatro handlers de Tarefa do Galho 10 — a versão vulnerável (que troca só `usuario_id: int` por `current_user`, sem filtrar nada) e a versão corrigida (que filtra a query pelo dono desde a busca, nunca busca solto e compara depois):

```python
"""routers/tarefas.py — versão final, com auth real e filtro de posse em toda query."""

from typing import Annotated

from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.orm import Session

from auth import get_current_user
from db import get_db
from domain.exceptions import TarefaNaoEncontrada
from models import Tarefa, Usuario
from schemas import TarefaCreate, TarefaRead

router = APIRouter(prefix="/tarefas", tags=["Tarefas"])


@router.get("", response_model=list[TarefaRead])
def listar_tarefas(
    current_user: Annotated[Usuario, Depends(get_current_user)],
    db: Session = Depends(get_db),
):
    # A query nasce restrita ao dono — nunca "todas as tarefas, filtra depois"
    stmt = select(Tarefa).where(Tarefa.usuario_id == current_user.id)
    return db.scalars(stmt).all()


@router.post("", response_model=TarefaRead, status_code=201)
def criar_tarefa(
    dados: TarefaCreate,
    current_user: Annotated[Usuario, Depends(get_current_user)],
    db: Session = Depends(get_db),
):
    # usuario_id vem do TOKEN, nunca de um campo do payload — TarefaCreate não tem esse campo
    tarefa = Tarefa(usuario_id=current_user.id, titulo=dados.titulo, anexo_url=dados.anexo_url)
    db.add(tarefa)
    db.commit()
    db.refresh(tarefa)
    return tarefa


def _buscar_tarefa_do_usuario(db: Session, tarefa_id: int, usuario_id: int) -> Tarefa:
    tarefa = db.scalar(
        select(Tarefa).where(Tarefa.id == tarefa_id, Tarefa.usuario_id == usuario_id)
    )
    if tarefa is None:
        # 404 uniforme — tarefa inexistente e tarefa de outro usuário são indistinguíveis
        # de fora, exatamente a decisão já justificada na capstone do Galho 10
        raise TarefaNaoEncontrada(tarefa_id)
    return tarefa


@router.patch("/{tarefa_id}/concluir", response_model=TarefaRead)
def concluir_tarefa(
    tarefa_id: int,
    current_user: Annotated[Usuario, Depends(get_current_user)],
    db: Session = Depends(get_db),
):
    tarefa = _buscar_tarefa_do_usuario(db, tarefa_id, current_user.id)
    tarefa.concluida = True
    db.commit()
    db.refresh(tarefa)
    return tarefa


@router.delete("/{tarefa_id}", status_code=204)
def remover_tarefa(
    tarefa_id: int,
    current_user: Annotated[Usuario, Depends(get_current_user)],
    db: Session = Depends(get_db),
):
    tarefa = _buscar_tarefa_do_usuario(db, tarefa_id, current_user.id)
    db.delete(tarefa)
    db.commit()
```

Repare que `TarefaNaoPertenceAoUsuario` — a segunda exceção que a capstone do Galho 10 já tinha registrado, com seu próprio exception handler devolvendo 404 — deixa de ser necessária nesta versão: como a própria query já filtra por `usuario_id == current_user.id`, uma tarefa de outro usuário simplesmente **não existe** do ponto de vista da consulta, então `TarefaNaoEncontrada` sozinha já cobre os dois casos. É a mesma economia que a nota 05 nomeou como vantagem estrutural: filtrar na query, em vez de buscar e comparar depois, torna estruturalmente impossível esquecer a checagem de posse — não existe uma segunda etapa para alguém remover por engano numa refatoração futura.

```mermaid
%%{init: {"theme": "base", "themeVariables": {"primaryColor": "#D0021B", "primaryBorderColor": "#8B0000", "lineColor": "#D0021B"}}}%%
sequenceDiagram
    participant Atacante
    participant API_Antes as API (Galho 10)
    participant API_Depois as API (esta capstone)

    Note over Atacante,API_Antes: ANTES — Etapas 1 e 2 ausentes
    Atacante->>API_Antes: GET /tarefas?usuario_id=7
    API_Antes-->>Atacante: 200 OK — tarefas de outra pessoa

    Note over Atacante,API_Depois: DEPOIS — Etapas 1 e 2 aplicadas
    Atacante->>API_Depois: GET /tarefas (sem token)
    API_Depois-->>Atacante: 401 Unauthorized
    Atacante->>API_Depois: GET /tarefas/42 (token válido, tarefa de outro usuário)
    API_Depois-->>Atacante: 404 Not Found — query já filtrada por dono
```

## Etapa 3: a SSTI introduzida de propósito — e a correção

Esta etapa acrescenta um endpoint que a capstone do Galho 10 nunca teve: **busca de tarefas por título, com o termo buscado destacado (highlight) na resposta**. É um pedido de produto plausível — "quero ver, na lista de resultados, qual parte do título bateu com a minha busca" — e é exatamente o tipo de recurso que, implementado da forma mais rápida possível, reintroduz a vulnerabilidade central da [[02 - Injeção — SQL, template, comando e deserialização insegura|nota 02 deste galho]].

### A versão vulnerável

```python
"""routers/tarefas.py — endpoint NOVO, vulnerável de propósito."""

from jinja2 import Template


@router.get("/buscar")
def buscar_tarefas_com_highlight(
    termo: str,
    current_user: Annotated[Usuario, Depends(get_current_user)],
    db: Session = Depends(get_db),
):
    stmt = select(Tarefa).where(
        Tarefa.usuario_id == current_user.id,
        Tarefa.titulo.icontains(termo),
    )
    tarefas = db.scalars(stmt).all()

    resultados = []
    for tarefa in tarefas:
        titulo_destacado = tarefa.titulo.replace(termo, f"<mark>{termo}</mark>")
        # VULNERÁVEL: o texto do usuário vira parte do TEXTO-FONTE do template,
        # antes da compilação — o mesmo erro estrutural do relatório da fintech
        # no incidente de abertura da nota 02
        template = Template(f"<span>{titulo_destacado}</span>")
        resultados.append({"id": tarefa.id, "html": template.render()})
    return resultados
```

O `Template(f"<span>{titulo_destacado}</span>")` monta o **texto-fonte** do template dinamicamente, concatenando o título da tarefa (que veio de `TarefaCreate.titulo`, um campo de entrada que qualquer usuário controla) dentro da string que o Jinja2 compila. Se um usuário cria uma tarefa com o título `{{ config.items() }}` — sintaticamente uma `str` perfeitamente válida, que passa por qualquer `Field(min_length=..., max_length=...)` sem disparar erro nenhum, exatamente o ponto central da [[04 - Validação de input como controle de segurança|nota 04]] — e depois busca por qualquer termo que apareça nesse título, o `.replace()` insere o payload dentro da string do template, e o Jinja2 avalia `{{ config.items() }}` como expressão de verdade:

```bash
# Cria uma tarefa com título malicioso
curl -X POST /tarefas -d '{"titulo": "{{ config.items() }}"}' -H "Authorization: Bearer $TOKEN"

# Busca por qualquer termo que bata com o título
curl "/tarefas/buscar?termo=config" -H "Authorization: Bearer $TOKEN"
# Resposta inclui: "html": "<span><mark>ItemsView({'jwt_secret': '...', ...})</mark></span>"
```

A `jwt_secret` — a mesma chave que assina todo `access_token` da Etapa 1 — vaza pela busca. E, como a nota 02 já desenvolveu em profundidade, a mesma classe de bug não para em vazamento de configuração: um título malicioso mais elaborado, explorando a cadeia `__class__.__mro__.__subclasses__()`, chega a execução de código arbitrário no servidor.

> [!bug] O que está quebrado, em uma frase
> O highlight foi implementado montando o texto-fonte do template a partir de dado que o próprio usuário controla (o título da tarefa) — exatamente o erro estrutural que a nota 02 nomeou como a diferença entre "valor de contexto" e "texto-fonte compilado".

### A correção

A defesa é a mesma que a nota 02 já cravou: o template é sempre uma string **fixa**, e o valor do usuário entra exclusivamente como argumento de contexto — nunca compõe o texto que o Jinja2 compila.

```python
"""routers/tarefas.py — corrigido: template fixo, título só como valor de contexto."""

from jinja2 import Template

TEMPLATE_HIGHLIGHT = Template("<span>{{ titulo }}</span>")


def _destacar_termo(titulo: str, termo: str) -> str:
    """Constrói o HTML de destaque SEM montar o texto-fonte do template a partir de input."""
    partes = titulo.split(termo)
    titulo_com_marcacao = f"<mark>{termo}</mark>".join(partes) if termo else titulo
    # titulo_com_marcacao é um VALOR — entra no template como contexto, nunca como sintaxe
    return TEMPLATE_HIGHLIGHT.render(titulo=titulo_com_marcacao)


@router.get("/buscar")
def buscar_tarefas_com_highlight(
    termo: str,
    current_user: Annotated[Usuario, Depends(get_current_user)],
    db: Session = Depends(get_db),
):
    stmt = select(Tarefa).where(
        Tarefa.usuario_id == current_user.id,
        Tarefa.titulo.icontains(termo),
    )
    tarefas = db.scalars(stmt).all()
    return [{"id": t.id, "html": _destacar_termo(t.titulo, termo)} for t in tarefas]
```

`TEMPLATE_HIGHLIGHT` é uma string **fixa**, definida uma única vez, fora do handler — nunca recriada a partir de `titulo_com_marcacao`. O valor com marcação `<mark>` entra como `titulo=titulo_com_marcacao`, um argumento de contexto, exatamente o padrão que a nota 02 já demonstrou com o exemplo do relatório da fintech corrigido. Com essa mudança, um título `{{ config.items() }}` volta a ser exibido como **texto literal** — `<mark>config</mark>.items() }}` — nunca reinterpretado como expressão Jinja2, porque nunca fez parte do texto-fonte compilado.

> [!tip] Autoescape, sozinho, não teria fechado esta vulnerabilidade
> Vale nomear explicitamente por que este não é um caso de "esqueceram o autoescape" — autoescape (o assunto central da [[03 - XSS e CSRF nos frameworks Python|nota 03]]) protege contra HTML/JS malicioso **dentro de um valor de contexto**, quando o template em si é fixo. Aqui o problema é categoricamente diferente: o próprio **texto-fonte do template** era montado dinamicamente. Nenhuma configuração de autoescape resolve isso — a correção tinha que ser estrutural (template fixo), não uma flag ligada ou desligada.

## Etapa 4: secrets em `pydantic-settings`

A API do Galho 10 tinha a `DATABASE_URL` escrita inline em `db.py` (`create_engine("postgresql+psycopg://app:senha@db.interno:5432/tarefas", ...)`), e a Etapa 1 desta nota acabou de introduzir uma `jwt_secret` — o exato tipo de valor que, se hardcoded, vira o incidente de abertura da [[06 - Secrets e configuração segura|nota 06 deste galho]]. Esta etapa move os dois para uma classe `Settings` tipada, seguindo o padrão que a nota 06 já desenvolveu:

```python
"""config.py — configuração tipada, falha rápido se faltar algo obrigatório."""

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

    # Obrigatórios — sem default, ValidationError na inicialização se faltarem
    database_url: str
    jwt_secret: str

    # Opcionais — default explícito e documentado
    jwt_algorithm: str = "HS256"
    access_token_expire_minutes: int = 15
    rate_limit_login: str = "5/minute"      # Etapa 5
    rate_limit_cadastro: str = "5/hour"     # Etapa 5


settings = Settings()
```

```python
"""db.py — Engine lê de settings, não de literal."""

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from config import settings

engine = create_engine(
    settings.database_url,
    pool_size=10,
    max_overflow=5,
    pool_timeout=30,
    pool_recycle=1800,
    pool_pre_ping=True,
)
SessionLocal = sessionmaker(bind=engine)
```

```bash
# .env — nunca commitado (nota 06); .env.example commitado como template vazio
DATABASE_URL=postgresql+psycopg://app:senha-real@db.interno:5432/tarefas
JWT_SECRET=uma-chave-forte-gerada-so-para-este-ambiente
```

Se `DATABASE_URL` ou `JWT_SECRET` não existirem no ambiente (nem no `.env`), `Settings()` levanta `ValidationError` **na inicialização do processo** — a API se recusa a subir com configuração incompleta, em vez de subir e falhar de forma imprevisível na primeira requisição, exatamente o comportamento fail-fast que a nota 06 desenvolveu como diferença entre "o deploy falhou com mensagem clara" e "a aplicação está no ar retornando 500 para todo mundo".

> [!warning] `jwt_secret` fraco reabre a Etapa 1 inteira
> Um detalhe que conecta as Etapas 1 e 4: se `JWT_SECRET` for um valor fraco ou reutilizado entre ambientes (dev e produção compartilhando a mesma chave, por exemplo), qualquer token forjável com esse segredo vazado invalida toda a autenticação da Etapa 1 — não importa quão bem filtradas as queries da Etapa 2 estejam. A defesa de secrets não é uma etapa isolada; ela é o alicerce que sustenta a Etapa 1 continuar valendo em produção.

## Etapa 5: rate limiting no cadastro e no login

`/usuarios` (cadastro) e `/token` (login) — os dois endpoints que a Etapa 1 introduziu — são exatamente o par que a [[08 - Rate limiting e proteção contra abuso|nota 08 deste galho]] identificou como alvo natural de brute force e credential stuffing. Sem limite, um atacante testa milhares de pares e-mail/senha contra `/token`, ou cria milhares de contas em `/usuarios` para outros fins de abuso (spam, esgotar um recurso limitado por conta). A defesa é `slowapi`, aplicada o mais cedo possível no pipeline — antes do hash de senha e da consulta ao banco, o mesmo ponto que a nota 08 já justificou:

```python
"""main.py — trecho de setup do slowapi."""

from slowapi import Limiter
from slowapi.util import get_remote_address

from config import settings

limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter
```

```python
"""routers/auth.py — rate limit aplicado aos dois endpoints sensíveis."""

from fastapi import Request

from main import limiter
from config import settings


@router.post("/usuarios", response_model=UsuarioRead, status_code=201)
@limiter.limit(settings.rate_limit_cadastro)
def cadastrar_usuario(request: Request, dados: UsuarioCreate, db: Session = Depends(get_db)):
    ...  # corpo idêntico ao da Etapa 1


@router.post("/token")
@limiter.limit(settings.rate_limit_login)
def login(request: Request, form: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    ...  # corpo idêntico ao da Etapa 1
```

E, seguindo o exemplo de `key="post:email"` que a nota 08 desenvolveu para fechar credential stuffing distribuído (um atacante rotacionando IPs nunca acumula limite no mesmo endereço, mas continua mirando a mesma conta-alvo), `/token` ganha uma segunda camada de limite, por e-mail tentado — não só por IP:

```python
def chave_por_email_do_form(request: Request) -> str:
    # slowapi não lê corpo de formulário nativamente na key_func padrão;
    # esta função extrai o "username" do form já parseado pelo FastAPI
    return request.state.username_tentado or get_remote_address(request)


limiter_login_por_conta = Limiter(key_func=chave_por_email_do_form)
```

```python
@router.post("/token")
@limiter.limit(settings.rate_limit_login)                 # por IP
@limiter_login_por_conta.limit("5/minute")                 # por conta-alvo
def login(request: Request, form: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    request.state.username_tentado = form.username
    usuario = db.scalar(select(Usuario).where(Usuario.email == form.username))
    if usuario is None or not verificar_senha(form.password, usuario.senha_hash):
        raise HTTPException(status_code=401, detail="Credenciais inválidas")
    return {"access_token": criar_access_token(usuario.id), "token_type": "bearer"}
```

A resposta de limite excedido segue o mesmo envelope de erro `type`/`title`/`status`/`detail` que a capstone do Galho 10 já cravou para 404/500 — a nota 08 já mostrou o `@app.exception_handler(RateLimitExceeded)` que reformata o `429` default do `slowapi` nesse contrato; não repetido aqui.

> [!question]- Por que não colocar rate limit em `/tarefas` também?
> Endpoints de leitura/escrita pós-autenticação (`GET /tarefas`, `POST /tarefas`) podem ganhar um limite mais folgado (a nota 08 mostrou `default_limits` da aplicação inteira, sobrescrito por rota), mas o risco que motiva rate limit apertado é específico de endpoints **pré-autenticação** ou que testam credenciais — é lá que um atacante ganha algo testando volume alto (adivinhar senha, enumerar contas). Um usuário já autenticado criando tarefas em volume alto é, na pior hipótese, abuso de cota de uso — um problema diferente, tratado por um limite mais alto e uniforme (`default_limits`), não pela mesma urgência de `/token`.

## Etapa 6: validação revisitada — `anexo_url` sob a lente da nota 04

O campo `anexo_url`, adicionado ao modelo na Etapa 0, é o gancho que a [[04 - Validação de input como controle de segurança|nota 04 deste galho]] previu: um campo de URL que a API eventualmente **requisita** (por exemplo, para gerar uma prévia do anexo) é exatamente o cenário onde `HttpUrl` do Pydantic garante forma, mas não destino.

```python
"""schemas.py — TarefaCreate ganha anexo_url, com a mesma armadilha de sempre."""

from pydantic import BaseModel, ConfigDict, Field, HttpUrl


class TarefaCreate(BaseModel):
    titulo: str = Field(min_length=1, max_length=200)
    anexo_url: HttpUrl | None = None  # NOVO — valida FORMA, não destino


class TarefaRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    usuario_id: int
    titulo: str
    concluida: bool
    anexo_url: str | None
    criada_em: str
```

`HttpUrl` garante que `anexo_url` é sintaticamente uma URL válida — exatamente a mesma garantia (e a mesma lacuna) que a nota 04 desenvolveu com o exemplo de `WebhookConfig`. Se um endpoint futuro desta API buscar o conteúdo desse anexo no servidor — por exemplo, `GET /tarefas/{id}/anexo/preview`, gerando uma miniatura — a mesma checagem de destino que a nota 04 já cravou precisa entrar entre a validação de forma e a requisição de saída:

```python
"""routers/tarefas.py — endpoint de preview, com a defesa de destino da nota 04."""

import ipaddress
import socket
from urllib.parse import urlparse

import httpx
from fastapi import HTTPException

FAIXAS_BLOQUEADAS = [
    ipaddress.ip_network("127.0.0.0/8"),
    ipaddress.ip_network("10.0.0.0/8"),
    ipaddress.ip_network("172.16.0.0/12"),
    ipaddress.ip_network("192.168.0.0/16"),
    ipaddress.ip_network("169.254.0.0/16"),  # inclui o endpoint de metadados cloud
]


def validar_destino_seguro(url: str) -> None:
    host = urlparse(url).hostname
    if host is None:
        raise HTTPException(400, detail="Anexo sem host válido")
    try:
        enderecos = socket.getaddrinfo(host, None)
    except socket.gaierror:
        raise HTTPException(400, detail="Não foi possível resolver o host do anexo")
    for _, _, _, _, endereco_bruto in enderecos:
        ip = ipaddress.ip_address(endereco_bruto[0])
        if any(ip in faixa for faixa in FAIXAS_BLOQUEADAS):
            raise HTTPException(400, detail="Destino do anexo não permitido")


@router.get("/{tarefa_id}/anexo/preview")
def preview_anexo(
    tarefa_id: int,
    current_user: Annotated[Usuario, Depends(get_current_user)],
    db: Session = Depends(get_db),
):
    tarefa = _buscar_tarefa_do_usuario(db, tarefa_id, current_user.id)  # Etapa 2 — posse já checada
    if tarefa.anexo_url is None:
        raise HTTPException(404, detail="Tarefa não tem anexo")

    validar_destino_seguro(tarefa.anexo_url)  # Etapa 6 — nota 04: forma já validou, destino ainda não
    with httpx.Client(follow_redirects=False) as client:
        resposta = client.get(tarefa.anexo_url)
    return {"content_type": resposta.headers.get("content-type")}
```

Repare que este endpoint reusa `_buscar_tarefa_do_usuario` da Etapa 2 — a checagem de posse não é reimplementada aqui, é a mesma função, o mesmo princípio de "estruturalmente impossível esquecer" aplicado a mais um endpoint. E `validar_destino_seguro` roda **depois** que `HttpUrl` já validou a forma no momento do `POST /tarefas` — a nota 04 chamou essa sequência de "forma → conteúdo → destino", e aqui as três camadas aparecem juntas: Pydantic (forma, na entrada), posse de recurso (quem pode ver este anexo, Etapa 2), resolução de IP (destino, nesta etapa).

## O sistema completo, com as seis etapas amarradas

```mermaid
%%{init: {"theme": "base", "themeVariables": {"primaryColor": "#4A90D9"}}}%%
flowchart TB
    subgraph Entrada["Camada transversal"]
        MW["Middleware de correlation ID\n(Galho 10, N07)"]
        RL["slowapi — rate limit\nem /usuarios e /token\n(N08)"]
    end

    subgraph AuthCamada["Autenticação"]
        TOKEN["POST /token, POST /usuarios\nJWT via pwdlib + PyJWT\n(N05 + Auth e Identidade SG4)"]
        DEP_AUTH["Depends(get_current_user)\nem toda rota de /tarefas\n(N05)"]
    end

    subgraph Autorizacao["Autorização de posse"]
        FILTRO["Toda query filtra por\nusuario_id == current_user.id\n(N05 — Broken Access Control)"]
    end

    subgraph Conteudo["Validação de conteúdo"]
        SSTI["Template fixo, título só\ncomo valor de contexto\n(N02 — SSTI corrigida)"]
        DEST["anexo_url: forma (HttpUrl)\n+ destino (resolução de IP)\n(N04)"]
    end

    subgraph Config["Configuração"]
        SET["pydantic-settings\nDATABASE_URL, JWT_SECRET\n(N06)"]
    end

    MW --> RL --> TOKEN --> DEP_AUTH --> FILTRO --> SSTI
    FILTRO --> DEST
    SET -.->|"lido por"| TOKEN
    SET -.->|"lido por"| RL

    style RL fill:#4A90D9,color:#fff
    style DEP_AUTH fill:#4A90D9,color:#fff
    style FILTRO fill:#2d7a4a,color:#fff
    style SSTI fill:#8b6914,color:#fff
    style DEST fill:#8b6914,color:#fff
    style SET fill:#c0392b,color:#fff
```

## Antes e depois: quatro ataques que passavam a não passar mais

| Ataque | Galho 10 (antes) | Esta capstone (depois) | Etapa que fecha |
|---|---|---|---|
| Ler tarefa de outro usuário trocando o `id` na URL | `200 OK`, dado alheio devolvido | `401` sem token; `404` com token de outro usuário | Etapas 1 e 2 |
| Criar tarefa em nome de outro usuário via `usuario_id` no payload | Aceito — `usuario_id` era query param controlado pelo cliente | Impossível — `usuario_id` vem só do token, `TarefaCreate` não tem esse campo | Etapa 1 |
| Título de tarefa `{{ config.items() }}` seguido de busca com highlight | `jwt_secret` e outras configs vazadas via SSTI | Título exibido como texto literal, sem execução | Etapa 3 |
| `anexo_url` apontando para `169.254.169.254` (metadados cloud) | Sem endpoint de preview no Galho 10 — mas seria requisitado sem checagem se implementado do jeito ingênuo | `400 Bad Request` antes de qualquer requisição sair do servidor | Etapa 6 |

## Armadilhas comuns ao aplicar hardening incremental

> [!warning] Corrigir Broken Access Control só no `GET`, esquecendo `PATCH`/`DELETE`
> **O que acontece:** o time filtra corretamente `listar_tarefas` por dono, testa, aprova — e esquece que `concluir_tarefa`/`remover_tarefa` tinham o mesmo padrão vulnerável antes da correção. **Por quê:** cada handler é uma função independente; corrigir um não corrige os outros automaticamente, e a suíte de testes manual costuma exercitar só o caminho mais visível (listar/criar), não os quatro verbos. **Como evitar:** centralizar a checagem de posse numa função reutilizável (`_buscar_tarefa_do_usuario`, como nesta nota), chamada por todo handler que opera sobre um `tarefa_id` — corrigir a função corrige todos os chamadores de uma vez, o mesmo raciocínio que a nota 05 já desenvolveu.

> [!warning] Adicionar um endpoint novo sem reaplicar as etapas já feitas
> **O que acontece:** o endpoint de busca com highlight (Etapa 3) nasce, na primeira versão, sem `Depends(get_current_user)` nenhum — porque "é só busca, não é dado sensível" — e sem filtrar por `usuario_id`, permitindo buscar título de tarefas de qualquer usuário. **Por quê:** cada endpoint novo reabre a superfície inteira das Etapas 1 e 2, porque nada garante automaticamente que um handler novo herda as proteções dos handlers antigos — FastAPI não tem middleware global de auth (a nota 05 já explicou o porquê), então cada rota precisa declarar `Depends(get_current_user)` explicitamente. **Como evitar:** tratar "toda rota nova sobre um recurso com dono declara `Depends(get_current_user)` e filtra por posse" como parte do checklist de PR, não como algo assumido implicitamente.

> [!warning] Confundir "corrigi a SSTI" com "sanitizei o texto do highlight"
> **O que acontece:** alguém tenta corrigir a Etapa 3 escapando manualmente caracteres de template (`{{`, `}}`) do título antes de montar a string — uma denylist, não a defesa estrutural. **Por quê:** é o mesmo erro que a [[04 - Validação de input como controle de segurança|nota 04]] nomeou sobre allowlist vs. denylist — uma lista de caracteres proibidos exige prever cada variação de sintaxe Jinja2 possível, e o Jinja2 tem mais de uma forma de expressar a mesma expressão perigosa. **Como evitar:** a correção real nunca é escapar o valor antes de montá-lo no texto do template — é nunca montar o texto do template a partir do valor, ponto. Template fixo, valor só como contexto, exatamente como a nota 02 e a Etapa 3 desta nota mostram.

## Em entrevista

A pergunta mais reveladora aqui não é "como você protegeria essa API" — é **"você me mostra uma API funcionando; como você decide, de forma sistemática, o que ainda falta antes dela ir para produção?"**

> "Eu não confio em 'os testes manuais passam' como sinal de segurança — code review funcional e segurança são lentes ortogonais, uma pergunta 'isso funciona no caminho feliz' e a outra pergunta 'isso resiste a alguém tentando quebrar'. Eu percorreria a API pedindo, para cada endpoint: quem pode chamar isso sem estar autenticado — e se a resposta for 'ninguém deveria', confirmar que existe uma dependência de auth de verdade, não decorativa. Depois, para cada endpoint que recebe um ID de recurso, confirmar que a query já nasce filtrada pelo dono, não que existe uma comparação manual que alguém pode esquecer de escrever numa rota nova. Depois, para cada campo de texto livre que algum dia é renderizado — template, HTML, log — confirmar que o valor nunca compõe a *sintaxe* do que está sendo montado, só o *conteúdo*. Depois, checar onde os segredos vivem — se algum `SECRET_KEY` ou string de conexão está hardcoded, isso é bloqueante, não um débito técnico para depois. Depois, checar se os dois endpoints que testam credencial (cadastro e login) têm limite de tentativas. E, por fim, para todo campo de URL que o servidor eventualmente requisita, confirmar que existe checagem de destino, não só de formato. Isso não é uma lista de itens soltos — é o mesmo roteiro que o OWASP Top 10 estrutura, aplicado sistematicamente, endpoint por endpoint, em vez de confiar que 'a gente revisa tudo' generosamente cobre a superfície inteira."

> [!question]- O entrevistador pergunta: "e depois de aplicar tudo isso, você diria que a API está 'segura'?"
> Não — e essa é a resposta certa a dar, não uma evasiva. "Segura" não é um estado binário alcançável por um checklist fechado; é uma postura contínua. Esta capstone fecha as lacunas que o Galho 10 deixou deliberadamente abertas e que este galho documentou uma a uma — mas nenhuma dessas correções tem uma prova automatizada e repetível de que continua valendo depois do próximo PR. É exatamente essa lacuna que o [[03-Dominios/Tecnologia/Python/Testes/index|Galho 12]] fecha: sem teste automatizado que simule "usuário B tenta acessar recurso do usuário A" e falhe se essa proteção regredir, a segurança desta capstone é uma fotografia de hoje, não uma garantia contínua.

## How to explain in English

> "Taking a working API to production-ready isn't one big rewrite — it's a sequence of narrow, verifiable fixes, each closing exactly one gap the previous stage left open on purpose. Real authentication replaces a query-param placeholder with a dependency that actually decodes and validates a token. Fixing broken access control means every query that fetches a resource by ID is scoped to the caller from the start, not fetched loosely and checked after the fact — that's the difference between a check someone can forget to write and a check that's structurally impossible to skip. A feature as innocuous as 'highlight my search term in the result' can reintroduce server-side template injection if the template's source text is built from user input instead of the term being passed as render context — the fix isn't escaping characters, it's never composing the template string from untrusted data in the first place. Secrets move out of literals into typed, fail-fast configuration. The two endpoints that test a credential — signup and login — get rate limited, because every failed attempt costs the server real CPU on a deliberately expensive password hash. And any URL field the server will eventually fetch itself needs a second validation layer beyond format — resolving the host and rejecting private IP ranges before the request goes out. None of this is new theory; it's the same lessons from earlier notes, applied to real code that used to be naive on purpose, so the gap between 'it works' and 'it survives a pentest' becomes visible line by line."

| PT-BR | English |
|---|---|
| hardening | hardening |
| espaço reservado (placeholder) | placeholder |
| checagem de posse | ownership check |
| 404 uniforme | uniform 404 |
| texto-fonte do template | template source text |
| valor de contexto | context value |
| configuração tipada | typed configuration |
| falhar rápido / fail-fast | fail-fast |
| limite de taxa | rate limit |
| validação de forma vs. destino | format vs. destination validation |

## Síntese — o que este galho ensinou, amarrado

Recapitulando o que as nove notas do Galho 11 cobriram juntas, cada uma aplicada nesta capstone:

1. [[01 - OWASP Top 10 aplicado a Python web — o mapa|01 — OWASP Top 10 aplicado a Python web]] deu o mapa — o pentest do cenário de abertura desta capstone é o mesmo cenário que abriu aquela nota, fechando o círculo do galho inteiro.
2. [[02 - Injeção — SQL, template, comando e deserialização insegura|02 — Injeção]] ensinou por que texto-fonte de template montado dinamicamente é SSTI, aplicado aqui à Etapa 3 (busca com highlight).
3. [[03 - XSS e CSRF nos frameworks Python|03 — XSS e CSRF]] — não amarrada diretamente nesta capstone (a API é JSON pura, sem cookie de sessão), mas o raciocínio de autoescape informou por que a Etapa 3 precisava de mais do que escape — precisava de template fixo.
4. [[04 - Validação de input como controle de segurança|04 — Validação de input como controle de segurança]] ensinou forma vs. destino, aplicado aqui à Etapa 6 (`anexo_url` e checagem de IP antes de qualquer requisição de saída).
5. [[05 - Autenticação e autorização na prática — a ponte com Auth e Identidade|05 — Autenticação e autorização na prática]] ensinou onde `Depends(get_current_user)` se encaixa e por que autenticado não é autorizado, aplicado às Etapas 1 e 2 — o núcleo desta capstone.
6. [[06 - Secrets e configuração segura|06 — Secrets e configuração segura]] ensinou `pydantic-settings` e fail-fast, aplicado na Etapa 4.
7. [[07 - Segurança de dependências e supply chain|07 — Segurança de dependências e supply chain]] — não amarrada diretamente ao código desta capstone (é disciplina de CI/lockfile, não de handler), mas pertence ao mesmo checklist de produção que esta capstone assume como pré-requisito antes do pentest de sexta-feira.
8. [[08 - Rate limiting e proteção contra abuso|08 — Rate limiting e proteção contra abuso]] ensinou `slowapi` e chave por conta-alvo, aplicado na Etapa 5.
9. Esta nota fechou amarrando as seis etapas — autenticação, autorização de posse, correção de SSTI, secrets tipados, rate limiting, validação de destino — na mesma API concreta que o [[03-Dominios/Tecnologia/Python/Web e APIs REST/09 - Capstone — uma API REST completa de ponta a ponta|Galho 10]] havia deixado deliberadamente ingênua, sem introduzir mecanismo novo, só integração — exatamente o mesmo movimento que a capstone do Galho 10 fez com roteamento, validação, injeção de dependência, erro e middleware.

Juntas, essas nove notas formam **como uma API Python real resiste, e não só funciona** — não mais "como validar um campo" ou "como emitir um JWT" isoladamente, mas como reconhecer, sistematicamente, onde uma API que passa em todo teste funcional ainda falha contra alguém tentando quebrá-la de propósito.

## O que vem a seguir

Esta capstone deliberadamente não prova, de forma automatizada e repetível, que nenhuma das seis correções continua valendo depois do próximo commit — cada verificação desta nota foi feita manualmente, lendo código e simulando um `curl`. Não é descuido: é o ponto exato onde este galho termina e o próximo começa.

- **[[03-Dominios/Tecnologia/Python/Testes/index|Galho 12 — Testes]]** (próximo) — a API blindada por esta capstone ainda não tem suíte automatizada, nem funcional (os quatro endpoints de tarefa fazem o que deveriam?) nem de segurança (um teste que simula "usuário B tenta `GET`/`PATCH`/`DELETE` num recurso do usuário A" e falha se `_buscar_tarefa_do_usuario` for removida numa refatoração futura — o teste exato que a [[05 - Autenticação e autorização na prática — a ponte com Auth e Identidade|nota 05]] já cobrou como obrigatório, sem desenvolver o mecanismo). `TestClient`, fixtures, e `app.dependency_overrides` (já citado na nota 04 do Galho 10) são as ferramentas que esse galho desenvolve.
- [[03-Dominios/Tecnologia/Python/Arquitetura e Design Patterns/index|Galho 13 — Arquitetura e Design Patterns]] — `_buscar_tarefa_do_usuario()` continua se comportando, informalmente, como uma função de Repository; esse galho formaliza o padrão, em cima do que as capstones dos Galhos 9, 10 e 11 já construíram.
- [[03-Dominios/Tecnologia/Python/index|Trilha Python]] — MOC da trilha.
- [[index|Segurança (Galho 11)]] — MOC deste galho.

## Fontes

- FastAPI. *Security — OAuth2 with Password (and hashing), Bearer with JWT tokens*. fastapi.tiangolo.com. https://fastapi.tiangolo.com/tutorial/security/oauth2-jwt/ (acessado em 2026-07-11) — padrão de `OAuth2PasswordRequestForm`/`OAuth2PasswordBearer` reusado nas Etapas 1 e 5.
- OWASP. *OWASP Top 10:2021*. owasp.org/Top10/. https://owasp.org/Top10/ (acessado em 2026-07-11) — taxonomia usada como roteiro sistemático na seção "Em entrevista" desta capstone.
- OWASP Cheat Sheet Series. *Server Side Template Injection Prevention Cheat Sheet*. cheatsheetseries.owasp.org. https://cheatsheetseries.owasp.org/cheatsheets/Server_Side_Template_Injection_Prevention_Cheat_Sheet.html (acessado em 2026-07-11) — base da correção da Etapa 3.
- OWASP Cheat Sheet Series. *Authorization Cheat Sheet*. cheatsheetseries.owasp.org. https://cheatsheetseries.owasp.org/cheatsheets/Authorization_Cheat_Sheet.html (acessado em 2026-07-11) — padrão de filtrar por dono na query, base da Etapa 2.
- Pydantic. *pydantic-settings — Settings Management*. docs.pydantic.dev. https://docs.pydantic.dev/latest/concepts/pydantic_settings/ (acessado em 2026-07-11) — base da Etapa 4.
- Sepehri, L. *slowapi — A rate limiting extension for Starlette and FastAPI*. github.com/laurentS/slowapi. https://github.com/laurentS/slowapi (acessado em 2026-07-11) — base da Etapa 5.
- [[01 - OWASP Top 10 aplicado a Python web — o mapa|01]], [[02 - Injeção — SQL, template, comando e deserialização insegura|02]], [[03 - XSS e CSRF nos frameworks Python|03]], [[04 - Validação de input como controle de segurança|04]], [[05 - Autenticação e autorização na prática — a ponte com Auth e Identidade|05]], [[06 - Secrets e configuração segura|06]], [[07 - Segurança de dependências e supply chain|07]], [[08 - Rate limiting e proteção contra abuso|08]] — as oito notas irmãs deste galho, cada uma fonte primária de uma das seis etapas amarradas nesta capstone.
- [[03-Dominios/Tecnologia/Python/Web e APIs REST/09 - Capstone — uma API REST completa de ponta a ponta|Web e APIs REST 09 — Capstone]] — a capstone do Galho 10, o código-base que esta nota evolui etapa a etapa.
- [[03-Dominios/Engenharia/Auth e Identidade/4 - Auth nos stacks/03 - Python — FastAPI|Auth e Identidade SG4 — Python — FastAPI]] — mecanismo de `get_current_user`/JWT/`pwdlib` reusado na Etapa 1, não repetido aqui.

Consultado em 2026-07-11.
