---
title: "Injeção de dependência no FastAPI — Depends"
created: 2026-07-11
type: concept
fase: adepto
status: complete
publish: true
tags:
  - python
  - web
  - fastapi
  - dependency-injection
  - depends
aliases:
  - "Depends()"
  - "Injeção de dependência no FastAPI"
  - "dependency_overrides"
  - "yield em dependências"
---

# Injeção de dependência no FastAPI — Depends

> [!abstract] TL;DR
> `Depends()` é o mecanismo central que faz o FastAPI chamar uma função **antes** de rodar o handler de uma rota, e passar o valor de retorno dessa função como parâmetro — sem que o handler saiba (nem precise saber) de onde aquele valor veio. É a mesma ideia de injeção de dependência que a [[03-Dominios/Tecnologia/Java/Spring Core e Boot/index|trilha Java já cobriu em profundidade com Spring]], só que sem contêiner, sem anotação de classe, sem XML — puramente funções Python chamando outras funções Python, resolvidas via type hints. A parte que separa quem só decorou a sintaxe de quem já sofreu em produção é o `yield`: uma dependência declarada com `yield` em vez de `return` vira, de fato, um **context manager gerenciado pelo framework** — o código antes do `yield` roda como setup, o código depois roda como teardown, e o FastAPI garante que o teardown executa mesmo se o handler levantar uma exceção. É esse detalhe que fecha (ou deixa vazando) uma sessão de banco a cada requisição.

## O incidente que abre esta nota

Uma API FastAPI que expõe pedidos de um e-commerce, construída em cima da camada de persistência que o [[03-Dominios/Tecnologia/Python/Persistência de dados/02 - SQLAlchemy ORM — Session, mapped classes e relationships|Galho 9, nota 02]] já cobriu — `Engine`, `sessionmaker`, `Session` do SQLAlchemy. O primeiro endpoint, escrito rápido, abre e fecha a sessão manualmente dentro do próprio handler:

```python
from fastapi import FastAPI
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine

from .models import Pedido

app = FastAPI()

engine = create_engine("postgresql://user:senha@localhost/loja")
SessionLocal = sessionmaker(bind=engine)


@app.get("/pedidos/{pedido_id}")
def buscar_pedido(pedido_id: int):
    session = SessionLocal()
    pedido = session.get(Pedido, pedido_id)
    if pedido is None:
        return {"erro": "não encontrado"}
    return {"id": pedido.id, "total": pedido.total}
    # session.close() NUNCA é chamado neste caminho de retorno
```

O endpoint funciona nos testes manuais. Passa em code review porque `session = SessionLocal()` parece inofensivo — é só uma linha, o padrão que o Galho 9 ensinou (`with Session(engine) as session:`) até é conhecido pelo time, só que ninguém aplicou aqui "porque é só uma leitura simples". O problema aparece em produção, sob carga real, algumas semanas depois: o pool de conexões do Postgres (configurado com um teto de 20 conexões simultâneas, [[03-Dominios/Tecnologia/Python/Persistência de dados/07 - Connection pooling e performance em produção|Galho 9, nota 07]]) começa a esgotar, e a API passa a responder `503` sob picos de tráfego que antes eram tranquilos.

> [!bug] O que está quebrado, em uma frase
> Toda `Session` aberta manualmente dentro do handler, sem um `with` ou um mecanismo equivalente de cleanup garantido, **nunca é fechada** quando o `return` acontece antes do fim natural da função (early return no caminho de erro, como o `return {"erro": ...}` acima) — a conexão correspondente fica presa ao pool até o coletor de lixo do Python decidir destruir o objeto `Session`, o que pode levar minutos sob carga, e nesse meio-tempo o pool inteiro esgota.

O diagnóstico, uma vez achado, é simples de nomear: **cleanup manual, escrito à mão, dentro de um handler que tem múltiplos caminhos de retorno, é frágil por construção** — cada `return` novo que alguém adicionar no futuro (um `if` extra, uma validação a mais) é um lugar novo onde `session.close()` pode ser esquecido. A correção não é lembrar de fechar a sessão em cada `return` — é tirar a responsabilidade de abrir/fechar sessão do handler por completo, e entregá-la a uma **dependência do FastAPI**, que garante o cleanup independentemente de como o handler termina. É esse mecanismo — `Depends()`, e em especial `Depends()` combinado com `yield` — que o resto desta nota desenvolve.

## O mecanismo central: uma função chamada antes da rota

Na forma mais simples, uma dependência é só uma função Python comum. `Depends()` diz ao FastAPI: "antes de chamar este handler, chame esta outra função, e passe o resultado dela como parâmetro":

```python
from fastapi import Depends, FastAPI

app = FastAPI()


def paginacao_padrao(limite: int = 20, offset: int = 0) -> dict[str, int]:
    return {"limite": limite, "offset": offset}


@app.get("/pedidos")
def listar_pedidos(paginacao: dict = Depends(paginacao_padrao)):
    return {
        "limite": paginacao["limite"],
        "offset": paginacao["offset"],
        "pedidos": [],  # busca real viria aqui
    }
```

O que acontece, em ordem, quando uma requisição `GET /pedidos?limite=5` chega:

1. O FastAPI olha a assinatura de `listar_pedidos` e vê o parâmetro `paginacao: dict = Depends(paginacao_padrao)`.
2. Antes de chamar `listar_pedidos`, o FastAPI chama `paginacao_padrao()` — e, como `paginacao_padrao` também tem parâmetros (`limite`, `offset`), o framework os resolve **exatamente da mesma forma que resolveria para um handler**: são query parameters, com valores-default, exatamente o mecanismo que a [[02 - Roteamento — decorators, urls.py e path operations|nota 02 deste galho]] já mostrou.
3. O valor de retorno de `paginacao_padrao()` — o dicionário `{"limite": 5, "offset": 0}` — é passado como o argumento `paginacao` de `listar_pedidos`.
4. Só então `listar_pedidos` roda, com `paginacao` já pronto.

> [!question]- Por que não chamar `paginacao_padrao(limite, offset)` direto dentro do handler, sem `Depends()`?
> Funcionaria tecnicamente, mas perderia exatamente o ponto de ter uma dependência: `Depends()` faz o FastAPI **descobrir sozinho** os parâmetros de `paginacao_padrao` (via a mesma inspeção de type hints usada em qualquer rota) e resolvê-los a partir da requisição HTTP — sem `Depends()`, o handler precisaria receber `limite`/`offset` na própria assinatura e repassar manualmente, o que é exatamente o tipo de boilerplate que a próxima seção mostra se multiplicando em cada endpoint que precisa de paginação. `Depends()` também é o que habilita cache por requisição e sobrescrita em testes (`app.dependency_overrides`, seções adiante) — nenhum dos dois existiria se a chamada fosse manual.

O nome "injeção de dependência" é o mesmo termo que a trilha Java usa com Spring, mas o mecanismo é radicalmente mais leve: não há um contêiner central de beans, não há ciclo de vida de aplicação inteiro a gerenciar, não há anotação de classe (`@Component`, `@Service`) — é resolução de parâmetro **por requisição**, decidida na assinatura da própria função de rota. Quem já usou `@Autowired` ou construtor injetado no Spring reconhece a ideia (uma peça de código recebe algo pronto, sem construir sozinha); a diferença é que o FastAPI resolve isso de novo a cada chamada HTTP, não uma vez no boot da aplicação.

## De onde vem a duplicação que `Depends()` resolve

Antes de aprofundar sub-dependências e `yield`, vale nomear o segundo cenário clássico que motiva `Depends()` — não um vazamento de recurso, mas duplicação de lógica. Cinco endpoints de uma API, escritos ao longo de semanas, cada um repetindo a mesma extração de paginação:

```python
@app.get("/pedidos")
def listar_pedidos(limite: int = 20, offset: int = 0):
    ...

@app.get("/produtos")
def listar_produtos(limite: int = 20, offset: int = 0):
    ...

@app.get("/clientes")
def listar_clientes(limite: int = 20, offset: int = 0):
    ...

@app.get("/pagamentos")
def listar_pagamentos(limite: int = 20, offset: int = 0):
    ...

@app.get("/entregas")
def listar_entregas(limite: int = 20, offset: int = 0):
    ...
```

Funciona, mas cada `limite: int = 20, offset: int = 0` é uma cópia da mesma regra de negócio (limite padrão 20, offset padrão 0). Quando o produto decide que o limite máximo deve ser 100 (para não permitir que um cliente da API peça `?limite=999999` e derrube o banco com uma query gigante), a correção precisa tocar cinco funções, uma a uma — e é fácil esquecer uma delas.

```python
from fastapi import Depends, FastAPI, Query

app = FastAPI()


def paginacao_padrao(
    limite: int = Query(default=20, le=100),
    offset: int = Query(default=0, ge=0),
) -> dict[str, int]:
    return {"limite": limite, "offset": offset}


@app.get("/pedidos")
def listar_pedidos(paginacao: dict = Depends(paginacao_padrao)):
    ...

@app.get("/produtos")
def listar_produtos(paginacao: dict = Depends(paginacao_padrao)):
    ...

@app.get("/clientes")
def listar_clientes(paginacao: dict = Depends(paginacao_padrao)):
    ...
```

`Query(le=100)` é o mesmo `Field()`-like declarativo que a [[03 - Validação e serialização com Pydantic|nota 03 deste galho]] já apresentou para corpo de requisição, aplicado aqui a um query parameter — restrição de negócio, uma vez só, num lugar só. A regra "limite máximo 100" agora existe em exatamente um lugar: dentro de `paginacao_padrao`. Mudar o teto é uma edição, não cinco.

> [!tip] `Depends()` sem parênteses na função também funciona, mas com um propósito diferente
> `Depends(paginacao_padrao)` passa a **função** (sem chamá-la) — o FastAPI é quem decide quando e como chamar. É um erro comum escrever `Depends(paginacao_padrao())` por engano (chamando a função na hora de declarar a rota, fora de qualquer contexto de requisição) — isso quebra, porque `paginacao_padrao()` exige os parâmetros `limite`/`offset` que só existem dentro de uma requisição HTTP real.

## Sub-dependências: uma dependência que depende de outra

Dependências podem, elas mesmas, ter `Depends()` na própria assinatura — formando uma **árvore de dependências** que o FastAPI resolve recursivamente, de baixo para cima, antes de finalmente chamar o handler.

```python
from fastapi import Depends, FastAPI, Header, HTTPException

app = FastAPI()


def get_tenant_id(x_tenant_id: str = Header(...)) -> str:
    """Extrai o tenant a partir de um header customizado — base de tudo abaixo."""
    if not x_tenant_id:
        raise HTTPException(status_code=400, detail="X-Tenant-Id obrigatório")
    return x_tenant_id


def get_configuracao_tenant(tenant_id: str = Depends(get_tenant_id)) -> dict:
    """Depende de get_tenant_id — usa o tenant já resolvido para buscar config."""
    configuracoes = {
        "loja-a": {"moeda": "BRL", "limite_pedidos": 500},
        "loja-b": {"moeda": "USD", "limite_pedidos": 1000},
    }
    config = configuracoes.get(tenant_id)
    if config is None:
        raise HTTPException(status_code=404, detail="tenant desconhecido")
    return config


@app.get("/pedidos")
def listar_pedidos(config: dict = Depends(get_configuracao_tenant)):
    return {"moeda": config["moeda"], "limite": config["limite_pedidos"]}
```

`listar_pedidos` nunca menciona `get_tenant_id` diretamente — não precisa. `get_configuracao_tenant` é quem declara `Depends(get_tenant_id)`, e o FastAPI monta a cadeia sozinho: para resolver `config`, primeiro resolve `tenant_id` (chamando `get_tenant_id`, que por sua vez lê o header `X-Tenant-Id` da requisição), e só então chama `get_configuracao_tenant(tenant_id)`.

```mermaid
%%{init: {"theme": "base", "themeVariables": {"primaryColor": "#4A90D9"}}}%%
flowchart TB
    REQ["Requisição HTTP\nheader X-Tenant-Id: loja-a"]

    subgraph Arvore["Árvore de dependências resolvida de baixo para cima"]
        D1["get_tenant_id()\nlê o header, valida presença"]
        D2["get_configuracao_tenant(tenant_id)\nusa o retorno de D1"]
    end

    HANDLER["listar_pedidos(config)\nsó roda depois que D1 e D2 já terminaram"]

    REQ --> D1
    D1 -->|"tenant_id = 'loja-a'"| D2
    D2 -->|"config = {moeda, limite_pedidos}"| HANDLER

    style REQ fill:#4A90D9,color:#fff
    style D1 fill:#4A90D9,color:#fff
    style D2 fill:#4A90D9,color:#fff
    style HANDLER fill:#2d7a4a,color:#fff
```

Essa composição é o que permite construir peças pequenas e reaproveitáveis — `get_tenant_id` sozinho já é útil em qualquer rota que só precise saber qual tenant está fazendo a requisição, sem precisar da configuração completa. Times que crescem uma API FastAPI de verdade acabam com dezenas de dependências pequenas, compostas em árvores diferentes conforme o endpoint precisa de mais ou menos contexto — o mesmo princípio de composição que motiva funções pequenas em qualquer código, aplicado à camada de resolução de parâmetros.

> [!question]- E se duas dependências diferentes, na mesma árvore, dependerem da mesma sub-dependência?
> É o cenário mais comum na prática — por exemplo, `get_configuracao_tenant` e uma outra dependência `get_usuario_atual` (auth, ver seção adiante) podem ambas depender de `get_tenant_id`. A seção seguinte (escopo por request) responde exatamente essa pergunta: por padrão, o FastAPI **não chama `get_tenant_id` duas vezes** na mesma requisição — ele reaproveita o resultado já calculado.

## Escopo por request: cada `Depends` roda (no máximo) uma vez por requisição

Esse é o detalhe de mecanismo mais fácil de assumir errado vindo de outros ecossistemas de DI: uma dependência do FastAPI **não** tem escopo de aplicação inteira (não é um singleton criado uma vez no boot, como um bean `@Singleton` do Spring) — ela é recalculada **a cada requisição HTTP**. Mas dentro de uma única requisição, se a mesma função de dependência aparece mais de uma vez na árvore (como no caso de `get_tenant_id` sendo usado por duas dependências diferentes), o FastAPI a chama **uma única vez** e reaproveita o resultado para todo o resto da árvore daquela requisição.

```python
contador_chamadas = {"get_tenant_id": 0}


def get_tenant_id(x_tenant_id: str = Header(...)) -> str:
    contador_chamadas["get_tenant_id"] += 1
    return x_tenant_id


def dependencia_a(tenant_id: str = Depends(get_tenant_id)) -> str:
    return f"a-{tenant_id}"


def dependencia_b(tenant_id: str = Depends(get_tenant_id)) -> str:
    return f"b-{tenant_id}"


@app.get("/debug")
def handler(a: str = Depends(dependencia_a), b: str = Depends(dependencia_b)):
    return {"a": a, "b": b, "chamadas_get_tenant_id": contador_chamadas["get_tenant_id"]}
```

Numa única requisição a `/debug`, `contador_chamadas["get_tenant_id"]` fica em **1**, não 2 — mesmo `get_tenant_id` aparecendo nas duas ramificações da árvore (via `dependencia_a` e via `dependencia_b`). Esse comportamento é controlado pelo parâmetro `use_cache` de `Depends()`, que é `True` por padrão:

```python
def dependencia_a(tenant_id: str = Depends(get_tenant_id, use_cache=True)):  # default, redundante escrever
    ...

def dependencia_c(tenant_id: str = Depends(get_tenant_id, use_cache=False)):  # força nova chamada
    ...
```

`use_cache=False` é raro na prática — o caso de uso legítimo é uma dependência com efeito colateral intencional que precisa rodar de novo mesmo já tendo sido chamada (por exemplo, gerar um novo valor aleatório a cada ocorrência, em vez de reaproveitar). Na maioria esmagadora dos casos, o comportamento padrão (`True`) é exatamente o que se quer: evita trabalho redundante (uma segunda query ao banco, uma segunda chamada de rede) só porque duas partes da árvore de dependências precisam do mesmo dado.

> [!warning] O cache é por requisição, não entre requisições
> É fácil ler "cache" e assumir um cache de aplicação (Redis, `functools.lru_cache`, algo que sobrevive entre chamadas HTTP diferentes). Não é isso — o cache de `Depends()` vive e morre dentro do ciclo de vida de **uma** requisição; a próxima requisição HTTP, mesmo idêntica à anterior, chama `get_tenant_id` de novo, do zero. Para cache de verdade entre requisições (ex: configuração de tenant que muda raramente), a ferramenta certa é uma camada de cache explícita — fora do escopo desta nota — não confiar no `use_cache` de `Depends()`.

## `yield` em dependências: setup, handler, teardown

A seção que fecha o incidente de abertura. Quando uma dependência usa `yield` em vez de `return`, ela deixa de ser uma função simples e passa a se comportar como um **context manager** — o código antes do `yield` roda como setup (equivalente ao `__enter__`), o valor do `yield` é o que é injetado no handler, e o código depois do `yield` roda como teardown (equivalente ao `__exit__`), garantido pelo FastAPI mesmo que o handler levante uma exceção.

```python
from collections.abc import Generator

from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy import create_engine

from .models import Pedido

app = FastAPI()

engine = create_engine("postgresql://user:senha@localhost/loja", pool_size=20)
SessionLocal = sessionmaker(bind=engine)


def get_db() -> Generator[Session, None, None]:
    db = SessionLocal()
    try:
        yield db          # setup terminou aqui — db é o que chega no handler
    finally:
        db.close()         # teardown — SEMPRE roda, mesmo se o handler levantar exceção


@app.get("/pedidos/{pedido_id}")
def buscar_pedido(pedido_id: int, db: Session = Depends(get_db)):
    pedido = db.get(Pedido, pedido_id)
    if pedido is None:
        raise HTTPException(status_code=404, detail="pedido não encontrado")
    return {"id": pedido.id, "total": pedido.total}
```

Esta é a correção direta do bug de abertura: `get_db` centraliza a abertura e o fechamento da `Session` num lugar só, e o `try/finally` interno garante que `db.close()` roda **independentemente de como `buscar_pedido` termina** — retorno normal, `raise HTTPException`, ou qualquer outra exceção não tratada. Não importa quantos `return`/`raise` existam dentro do handler daqui para frente; o cleanup não depende mais de disciplina do desenvolvedor lembrando de fechar a sessão em cada caminho.

```mermaid
sequenceDiagram
    participant Cliente
    participant FastAPI
    participant get_db as get_db() (dependência)
    participant Handler as buscar_pedido()

    Cliente->>FastAPI: GET /pedidos/42
    FastAPI->>get_db: chama get_db()
    get_db->>get_db: db = SessionLocal() (setup)
    get_db-->>FastAPI: yield db
    FastAPI->>Handler: buscar_pedido(pedido_id=42, db=db)
    alt handler termina normalmente
        Handler-->>FastAPI: return {"id": 42, ...}
    else handler levanta exceção
        Handler-->>FastAPI: raise HTTPException / outro erro
    end
    FastAPI->>get_db: retoma a execução após o yield
    get_db->>get_db: db.close() (teardown, no finally)
    FastAPI-->>Cliente: resposta HTTP (200 ou erro)
```

> [!question]- Isso é o mesmo mecanismo de `@contextmanager` do `contextlib`?
> Sim, no espírito — uma função com `yield` cercada por `try/finally` é exatamente a forma que um context manager assume quando escrito com `@contextlib.contextmanager`, em vez de uma classe com `__enter__`/`__exit__`. O FastAPI reconhece esse padrão em dependências automaticamente (sem precisar do decorator `@contextmanager` explícito) e gerencia o ciclo de vida sozinho: chama a dependência até o `yield`, injeta o valor, e depois retoma a execução (rodando o `finally`) quando o handler termina — seja com sucesso, seja com exceção. O mecanismo de context manager em si (protocolo `__enter__`/`__exit__`, o que `@contextmanager` faz por baixo) já é assunto coberto em profundidade em outra parte da trilha; o ponto aqui é só que `Depends()` com `yield` **é** esse padrão, aplicado ao ciclo de vida de uma requisição HTTP inteira.

### Sub-dependências com `yield`: o teardown respeita a ordem

Quando uma dependência com `yield` depende de outra dependência com `yield`, o FastAPI garante que o teardown acontece na **ordem inversa** do setup — a última dependência a fazer setup é a primeira a fazer teardown, o mesmo princípio de pilha (LIFO) que qualquer `with` aninhado segue:

```python
def get_db() -> Generator[Session, None, None]:
    db = SessionLocal()
    print("abrindo sessão")
    try:
        yield db
    finally:
        print("fechando sessão")
        db.close()


def get_pedido_service(db: Session = Depends(get_db)) -> "PedidoService":
    print("criando service")
    service = PedidoService(db)
    try:
        yield service
    finally:
        print("finalizando service")
        # cleanup específico do service, se houver
```

Para uma requisição que usa `get_pedido_service`, a ordem impressa é sempre: `abrindo sessão` → `criando service` → (handler roda) → `finalizando service` → `fechando sessão`. O recurso "mais externo" (a sessão de banco, aberta primeiro) só é liberado depois que tudo que dependia dele (o service, aberto depois) já terminou seu próprio cleanup — exatamente a garantia que se espera de context managers aninhados.

> [!warning] Uma exceção no `finally` de uma dependência com `yield` pode mascarar o erro original do handler
> **O que acontece:** se o handler levanta uma exceção e o código no `finally` de uma dependência (o teardown) também levanta uma exceção — por exemplo, `db.close()` falhando porque a conexão já caiu — a exceção do teardown pode se sobrepor à exceção original do handler, tornando o erro real mais difícil de rastrear no log. **Por quê:** é o mesmo comportamento de qualquer `try/finally` em Python — uma exceção levantada dentro de um bloco `finally` substitui qualquer exceção que estivesse "em trânsito" vindo do bloco `try`. **Como evitar:** manter o código de teardown simples e defensivo (capturar e logar erros de cleanup em vez de deixá-los propagar sem controle), e nunca colocar lógica de negócio no teardown — só liberação de recurso.

## Casos de uso reais além da sessão de banco

### Filtros e query params compartilhados

A mesma ideia de `paginacao_padrao` se estende a qualquer conjunto de query params que reaparece em vários endpoints — um filtro de intervalo de datas usado tanto em `/pedidos` quanto em `/pagamentos`, por exemplo:

```python
from datetime import date

from fastapi import Depends, Query


def filtro_periodo(
    data_inicio: date | None = Query(default=None),
    data_fim: date | None = Query(default=None),
) -> dict[str, date | None]:
    if data_inicio and data_fim and data_inicio > data_fim:
        raise HTTPException(status_code=400, detail="data_inicio não pode ser depois de data_fim")
    return {"inicio": data_inicio, "fim": data_fim}


@app.get("/pedidos")
def listar_pedidos(periodo: dict = Depends(filtro_periodo), db: Session = Depends(get_db)):
    ...


@app.get("/pagamentos")
def listar_pagamentos(periodo: dict = Depends(filtro_periodo), db: Session = Depends(get_db)):
    ...
```

Repare que a validação de negócio ("`data_inicio` não pode ser depois de `data_fim`") vive num lugar só — sem `Depends()`, essa checagem apareceria duplicada em cada handler que aceita esse par de filtros, com o risco real de as duas cópias divergirem ao longo do tempo (alguém corrige a regra num endpoint e esquece do outro).

### Múltiplos endpoints consumindo a mesma sessão de banco

O padrão `get_db` da seção anterior não é usado uma vez só — é reaproveitado em toda rota que precisa tocar o banco, exatamente como o [[03-Dominios/Tecnologia/Python/Persistência de dados/02 - SQLAlchemy ORM — Session, mapped classes e relationships|Galho 9]] descreveu como "uma sessão por unidade de trabalho": cada requisição HTTP é uma unidade de trabalho, e `Depends(get_db)` garante uma `Session` nova por requisição, nunca compartilhada entre requisições concorrentes (o mesmo problema de `Session` não ser thread-safe que a nota do Galho 9 já cobriu).

```python
@app.post("/pedidos", status_code=201)
def criar_pedido(dados: PedidoCreate, db: Session = Depends(get_db)):
    pedido = Pedido(**dados.model_dump())
    db.add(pedido)
    db.commit()
    db.refresh(pedido)
    return pedido


@app.get("/pedidos")
def listar_pedidos(
    paginacao: dict = Depends(paginacao_padrao),
    db: Session = Depends(get_db),
):
    return db.query(Pedido).offset(paginacao["offset"]).limit(paginacao["limite"]).all()
```

Nenhum dos dois handlers menciona `SessionLocal`, `create_engine`, nem qualquer detalhe de como a sessão foi construída — essa mecânica inteira (Engine, pool de conexões, `sessionmaker`) já foi coberta em profundidade pelo Galho 9 e não é repetida aqui; o que esta nota acrescenta é só o mecanismo de FastAPI que entrega essa sessão pronta a cada handler, e garante o fechamento dela ao final.

### Autenticação: `Depends()` é o mecanismo, não o conteúdo

Uma das aplicações mais comuns de `Depends()` em qualquer API FastAPI real é autenticação — uma dependência que lê um header/cookie, valida um token, e devolve o usuário autenticado (ou levanta `401` se a validação falhar):

```python
def get_usuario_atual(token: str = Depends(oauth2_scheme)) -> "Usuario":
    ...  # decodifica o token, valida, busca o usuário — conteúdo do Galho 11


@app.get("/pedidos/meus")
def listar_meus_pedidos(
    usuario: "Usuario" = Depends(get_usuario_atual),
    db: Session = Depends(get_db),
):
    return db.query(Pedido).filter(Pedido.usuario_id == usuario.id).all()
```

O ponto que vale reter aqui é estrutural, não de conteúdo: `Depends()` é o **mecanismo** que o FastAPI usa para proteger rotas — a mesma árvore de sub-dependências, o mesmo escopo por requisição, o mesmo `yield` se necessário. O que entra dentro de `get_usuario_atual` (JWT, OAuth2, API keys, sessão de cookie) é o assunto do [[03-Dominios/Tecnologia/Python/Segurança/index|Galho 11]] — esta nota não desenvolve autenticação em si, só nomeia que ela se apoia no mesmo `Depends()` já explicado.

## O que torna o FastAPI testável: `app.dependency_overrides`

O motivo prático mais citado para preferir injeção de dependência (em qualquer linguagem) sobre chamar dependências diretamente de dentro do código é testabilidade — e o FastAPI expõe isso de forma direta via `app.dependency_overrides`, um dicionário que mapeia uma função de dependência original para uma função substituta:

```python
from fastapi.testclient import TestClient

from .main import app, get_db


def get_db_fake():
    db = SessionLocal_teste()  # engine de teste, ex: SQLite em memória
    try:
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = get_db_fake

client = TestClient(app)

resposta = client.get("/pedidos")
assert resposta.status_code == 200
```

`app.dependency_overrides[get_db] = get_db_fake` diz ao FastAPI: "toda vez que uma rota pedir `Depends(get_db)`, chame `get_db_fake` no lugar" — sem tocar em nenhum handler, sem mudar uma linha de código de produção. É o mesmo princípio que justifica interfaces/mocks em qualquer suíte de testes com DI: o código de produção depende de uma **abstração** (a assinatura `Session = Depends(get_db)`), não de uma implementação concreta amarrada — trocar o que está por trás da dependência é uma substituição de dicionário, não um refactor.

> [!tip] `dependency_overrides` funciona em qualquer dependência, não só nas de banco
> O mesmo padrão substitui `get_usuario_atual` por uma versão fake que sempre devolve um usuário de teste fixo (sem precisar gerar um JWT de verdade em cada teste), ou substitui uma dependência que chama uma API externa por uma versão que devolve dados fixos — qualquer lugar que usa `Depends()` é, por construção, um ponto de substituição em teste. A mecânica de escrever esses testes de verdade — fixtures do pytest, `TestClient`, organização de testes de API — é o assunto do [[03-Dominios/Tecnologia/Python/Testes/index|Galho 12]]; esta nota fica só no mecanismo que torna a substituição possível.

> [!warning] Esquecer de limpar `dependency_overrides` entre testes
> **O que acontece:** um teste faz `app.dependency_overrides[get_db] = get_db_fake` e não desfaz isso ao final — o próximo teste da suíte, que esperava a dependência real (ou uma fake diferente), herda a substituição do teste anterior, produzindo falhas que parecem aleatórias e dependentes da ordem de execução. **Por quê:** `app.dependency_overrides` é um dicionário compartilhado pela instância `app` inteira — não há escopo automático por teste, o FastAPI não sabe (nem tenta saber) quando um teste "termina". **Como evitar:** limpar o override explicitamente ao final do teste (`app.dependency_overrides.clear()` ou remoção pontual da chave), tipicamente dentro de uma fixture do pytest com teardown automático — mecanismo aprofundado no Galho 12.

## Armadilhas comuns

> [!warning] Abrir recurso manualmente dentro do handler "porque é só desta vez"
> **O que acontece:** exatamente o incidente de abertura desta nota — um handler específico decide que não vale a pena usar `Depends(get_db)` para uma operação "simples", abre a sessão (ou qualquer outro recurso) manualmente, e o cleanup depende de lembrar de fechar em todo caminho de retorno. **Por quê:** `Depends()` com `yield` centraliza o cleanup num lugar garantido pelo framework; abrir manualmente reintroduz exatamente o problema que a dependência existe para resolver — um `return`/`raise` novo, adicionado depois, é um lugar novo onde o cleanup pode ser esquecido. **Como evitar:** toda rota que usa um recurso com ciclo de vida (sessão de banco, conexão de rede, arquivo) passa por uma dependência com `yield`, sem exceção "por ser simples".

> [!warning] Confundir escopo por requisição com escopo de aplicação
> **O que acontece:** uma dependência é escrita assumindo que vai rodar uma vez só, no boot da aplicação (guardando estado mutável entre chamadas, por exemplo um contador ou uma lista que cresce a cada requisição) — mas na verdade ela roda de novo a cada requisição HTTP. **Por quê:** ao contrário de um singleton de contêiner de DI tradicional, uma dependência do FastAPI não tem vida própria fora da requisição que a disparou — o cache de `use_cache=True` só evita chamadas repetidas **dentro** da mesma árvore de uma requisição, nunca entre requisições diferentes. **Como evitar:** estado que precisa sobreviver entre requisições (uma conexão de pool, uma configuração carregada uma vez) vive fora da função de dependência — em uma variável de módulo, um objeto `Engine` criado no import, ou (em apps maiores) no `app.state` do FastAPI — e a dependência só acessa esse estado já existente, sem recriá-lo.

> [!warning] `Depends()` chamado sem os parênteses da função dentro
> **O que acontece:** escrever `Depends(minha_dependencia())` em vez de `Depends(minha_dependencia)` — chamando a função na hora da declaração da rota, fora de qualquer contexto de requisição HTTP. **Por quê:** `Depends()` espera receber a **função em si** (um objeto *callable*), não o resultado de já tê-la chamado — o FastAPI é quem decide o momento certo de chamar, com os parâmetros certos, resolvidos a partir da requisição. **Como evitar:** revisar toda declaração `Depends(...)` como "estou passando a função, ou já chamei ela?" — o erro costuma aparecer cedo, geralmente como um `TypeError` na inicialização da rota, porque a função é chamada sem os argumentos que só existem numa requisição real.

## Em entrevista

- **"O que é `Depends()` no FastAPI, em uma frase?"** É o mecanismo de injeção de dependência do framework: uma função (ou gerador) declarada como parâmetro de rota via `Depends(minha_funcao)` é chamada automaticamente pelo FastAPI antes do handler, e o valor de retorno (ou o valor do `yield`) é injetado como argumento — sem contêiner central, sem anotação de classe, resolvido por requisição via inspeção de type hints.
- **"Qual a diferença entre uma dependência com `return` e uma com `yield`?"** `return` entrega o valor e a função termina ali — sem cleanup. `yield` transforma a dependência num context manager gerenciado pelo framework: o código antes do `yield` é setup, o valor do `yield` é o que é injetado, e o código depois do `yield` (tipicamente dentro de um `finally`) é teardown, garantido mesmo se o handler levantar exceção — é o padrão usado para abrir/fechar sessão de banco por requisição.
- **"Uma dependência roda quantas vezes por requisição?"** Por padrão (`use_cache=True`), no máximo uma vez, mesmo que apareça em múltiplos pontos da árvore de dependências daquela requisição — o FastAPI reaproveita o resultado já calculado. O cache não sobrevive entre requisições diferentes; cada requisição HTTP nova recalcula do zero.
- **"Como o FastAPI se torna testável via `Depends()`?"** `app.dependency_overrides` é um dicionário que mapeia uma dependência original para uma substituta — qualquer rota que dependa de `Depends(get_db)`, por exemplo, pode ter essa dependência trocada por uma versão fake/mock em teste, sem tocar no código de produção, porque o handler nunca depende de uma implementação concreta, só da assinatura da dependência.

> [!question]- O entrevistador pergunta: "isso é a mesma coisa que injeção de dependência do Spring?"
> A resposta madura nomeia a semelhança de intenção e a diferença de mecânica: o objetivo é o mesmo — código que recebe suas dependências prontas, em vez de construí-las sozinho, o que melhora testabilidade e desacoplamento. A diferença é onde e quando a resolução acontece. Spring resolve a árvore de beans **uma vez, no boot da aplicação** (por padrão, singletons vivendo pelo tempo de vida do contêiner, com escopos alternativos como `@RequestScope` disponíveis mas não-default), guiado por anotações de classe e um contêiner central que conhece o grafo completo de dependências da aplicação. FastAPI não tem contêiner nem grafo pré-registrado — cada `Depends()` é resolvido **a cada requisição HTTP**, a partir da assinatura da função de rota, sem nenhum registro central de "quais dependências existem" — é injeção de dependência funcional, ad-hoc, por requisição, não um contêiner de IoC clássico.

## How to explain in English

> `Depends()` is FastAPI's dependency injection mechanism: a function declared as a route parameter via `Depends(my_function)` gets called automatically before the handler runs, and its return value is injected as an argument — no central container, no class annotations, resolved per-request through type hint inspection. Dependencies can depend on other dependencies, forming a tree that FastAPI resolves bottom-up, and by default each dependency runs at most once per request even if it appears in multiple branches of that tree. The detail that separates tutorial-level knowledge from production experience is `yield`: a dependency written with `yield` instead of `return` becomes a framework-managed context manager — code before the `yield` is setup, the yielded value is what gets injected, and code after the `yield` is teardown, guaranteed to run even if the handler raises. That's the canonical pattern for opening and closing a database session once per request, replacing manual open/close calls scattered across handlers with early returns that are easy to leak. `app.dependency_overrides` is what makes all of this testable — swapping a real dependency for a fake one is a dictionary assignment, not a code change.

| PT | EN |
|----|----|
| injeção de dependência | dependency injection |
| dependência (FastAPI) | dependency |
| sub-dependência | sub-dependency |
| árvore de dependências | dependency tree |
| escopo por requisição | per-request scope |
| cache por requisição | per-request caching |
| gerador (com `yield`) | generator (with `yield`) |
| setup / teardown | setup / teardown |
| sobrescrever dependência (teste) | override a dependency (testing) |

## Síntese

`Depends()` resolve dois problemas ao mesmo tempo, e vale nomeá-los separadamente porque o incidente de abertura mistura os dois: **duplicação** (a mesma lógica de paginação, filtro ou extração de dado copiada em cada endpoint, um lugar a mais para divergir) e **ciclo de vida de recurso** (abrir/fechar algo — sessão de banco, conexão, arquivo — de forma que não dependa de disciplina manual em cada caminho de retorno do handler). Sub-dependências compõem peças pequenas em árvores maiores, resolvidas de baixo para cima; o escopo por requisição (com cache controlado por `use_cache`) evita trabalho redundante dentro de uma única chamada HTTP, sem nunca vazar estado entre requisições diferentes; `yield` transforma o padrão de setup/teardown num mecanismo garantido pelo framework, não uma convenção que depende de lembrança; e `app.dependency_overrides` é o que fecha o círculo, tornando qualquer dependência — banco, autenticação, serviço externo — substituível em teste sem tocar no código de produção.

O próximo passo natural do galho sai do território exclusivo de FastAPI e olha para como Django resolve o mesmo tipo de problema (validação, serialização, organização de endpoint) com sua própria camada REST, construída sobre um framework com filosofia bem diferente de injeção de dependência.

## Veja também

- [[03-Dominios/Tecnologia/Python/Persistência de dados/02 - SQLAlchemy ORM — Session, mapped classes e relationships|02 — SQLAlchemy ORM: Session, mapped classes e relationships]] — Galho 9, nota 02; mecânica completa de `Engine`/`sessionmaker`/`Session` consumida via `Depends(get_db)` nesta nota, sem repetição.
- [[03-Dominios/Tecnologia/Python/Persistência de dados/07 - Connection pooling e performance em produção|07 — Connection pooling e performance em produção]] — Galho 9; o pool de conexões que esgota no incidente de abertura desta nota.
- [[02 - Roteamento — decorators, urls.py e path operations|02 — Roteamento]] — nota irmã; mecanismo de path/query parameters reaproveitado na resolução de parâmetros de dependências.
- [[03 - Validação e serialização com Pydantic|03 — Validação e serialização com Pydantic]] — nota irmã anterior; `Query()`/`Field()` usados nesta nota para restringir parâmetros de dependências de paginação/filtro.
- [[05 - Django REST Framework — serializers, viewsets e routers|05 — Django REST Framework]] — próxima nota, contraste de filosofia de organização de endpoint num framework sem `Depends()`.
- [[03-Dominios/Tecnologia/Python/Segurança/index|Segurança]] — Galho 11; conteúdo de autenticação/autorização que se apoia no mecanismo de `Depends()` explicado aqui, sem repeti-lo.
- [[03-Dominios/Tecnologia/Python/Testes/index|Testes]] — Galho 12; fixtures de pytest e `TestClient` que operacionalizam `app.dependency_overrides` em suítes de teste reais.
- [[03-Dominios/Tecnologia/Java/Spring Core e Boot/index|Spring Core e Boot]] — trilha Java; injeção de dependência via contêiner de beans, contraste de mecânica citado nesta nota.
- [[index|Web e APIs REST (Galho 10)]] — MOC deste galho.

## Fontes

- FastAPI. *Dependencies — First Steps*. fastapi.tiangolo.com/tutorial/dependencies/. https://fastapi.tiangolo.com/tutorial/dependencies/ (acessado em 2026-07-11) — mecanismo base de `Depends()`, resolução por type hints.
- FastAPI. *Classes as Dependencies*. fastapi.tiangolo.com/tutorial/dependencies/classes-as-dependencies/. https://fastapi.tiangolo.com/tutorial/dependencies/classes-as-dependencies/ (acessado em 2026-07-11).
- FastAPI. *Sub-dependencies*. fastapi.tiangolo.com/tutorial/dependencies/sub-dependencies/. https://fastapi.tiangolo.com/tutorial/dependencies/sub-dependencies/ (acessado em 2026-07-11) — árvore de dependências, `use_cache`.
- FastAPI. *Dependencies with yield*. fastapi.tiangolo.com/tutorial/dependencies/dependencies-with-yield/. https://fastapi.tiangolo.com/tutorial/dependencies/dependencies-with-yield/ (acessado em 2026-07-11) — setup/teardown, ordem de execução em sub-dependências com `yield`, tratamento de exceção.
- FastAPI. *SQL (Relational) Databases*. fastapi.tiangolo.com/tutorial/sql-databases/. https://fastapi.tiangolo.com/tutorial/sql-databases/ (acessado em 2026-07-11) — padrão canônico `get_db` com SQLAlchemy.
- FastAPI. *Testing Dependencies with Overrides*. fastapi.tiangolo.com/advanced/testing-dependencies/. https://fastapi.tiangolo.com/advanced/testing-dependencies/ (acessado em 2026-07-11) — `app.dependency_overrides`.
- Real Python. *Dependency Injection in Python*. realpython.com/dependency-injection-python/. https://realpython.com/dependency-injection-python/ (acessado em 2026-07-11).
- Mendes, Eduardo (Dunossauro). *FastAPI do Zero*. fastapidozero.dunossauro.com. https://fastapidozero.dunossauro.com/ (acessado em 2026-07-11) — `Depends()` aplicado a sessão de banco no padrão idiomático da comunidade brasileira.
- [[03-Dominios/Tecnologia/Python/Persistência de dados/02 - SQLAlchemy ORM — Session, mapped classes e relationships|SQLAlchemy ORM — Session, mapped classes e relationships]] — nota do Galho 9, referenciada para o vocabulário de `Session`/`sessionmaker` usado nesta nota.

Consultado em 2026-07-11.
