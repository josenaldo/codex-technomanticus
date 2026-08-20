---
title: "Testando a API REST — TestClient e dependency overrides"
created: 2026-07-11
type: concept
fase: Adepto
status: complete
publish: true
tags:
  - python
  - testes
  - pytest
  - fastapi
  - testclient
  - dependency-overrides
aliases:
  - "TestClient"
  - "app.dependency_overrides em teste"
  - "override_get_db"
  - "pytest-django client"
---

# Testando a API REST — TestClient e dependency overrides

> [!abstract] TL;DR
> `TestClient` do FastAPI (baseado em `httpx`, sobre o Starlette) faz uma requisição HTTP simulada **sem abrir porta, sem subir servidor, sem rede de verdade** — rápido o bastante para rodar centenas de vezes a cada `git commit`. `client.post("/tarefas", json={...})` retorna um objeto de resposta com `status_code` e `.json()`, e um teste de API vira só mais um `assert`, no mesmo estilo que a [[01 - pytest fundamentos — anatomia, discovery e assert introspection|nota 01]] já ensinou. A peça que faltava desde o [[03-Dominios/Tecnologia/Python/Web e APIs REST/04 - Injeção de dependência no FastAPI — Depends|Galho 10, nota 04]] — que já mencionou `app.dependency_overrides` de passagem, sem desenvolver — é esta: trocar `get_db` por uma sessão de banco de teste, e `get_current_user` por um usuário fixo, sem fazer login de verdade em cada teste. E o teste mais valioso desta nota não é o mais simples — é o que cria uma tarefa, lista, e tenta acessar a tarefa de outro usuário esperando `404`, provando de forma automatizada e repetível que a correção de Broken Access Control do [[03-Dominios/Tecnologia/Python/Segurança/05 - Autenticação e autorização na prática — a ponte com Auth e Identidade|Galho 11, nota 05]] continua valendo depois do próximo commit.

## O Postman que ninguém mais abriu depois do deploy

Um time pequeno construiu a API de Tarefas exatamente como as capstones dos Galhos 10 e 11 descreveram — `APIRouter`, `Depends(get_db)`, autenticação JWT, filtro de posse em toda query. Antes de cada deploy, alguém do time abre o Swagger UI (a documentação que a [[03-Dominios/Tecnologia/Python/Web e APIs REST/08 - Documentação automática com OpenAPI|nota 08 do Galho 10]] já mostrou nascendo de graça dos type hints), loga com uma conta de teste, clica em "Try it out" em cada endpoint, olha se a resposta "parece certa". Funciona — no sentido de que ninguém jamais viu um `500` inesperado durante esse ritual. O ritual dura uns vinte minutos, uma vez por deploy, e o time trata isso como "testado".

Três semanas depois de um deploy sem incidentes visíveis, um cliente reporta que consegue ver o título de tarefas de outra conta trocando o número no fim da URL. Ninguém no time mudou o endpoint de leitura de tarefa recentemente — o que mudou foi um refactor no serviço de domínio, dias antes, que moveu a checagem de posse de dentro da query (`Tarefa.usuario_id == current_user.id`, o padrão estrutural que a nota 05 do Galho 11 recomendou) para uma função auxiliar nova, chamada em três dos quatro endpoints — o quarto, adicionado na mesma semana por outra pessoa do time, esqueceu de chamar a função.

> [!bug] O que está quebrado, em uma frase
> O ritual manual de "clicar no Swagger antes do deploy" testa o caminho feliz de quem está logado testando a própria conta — nunca testa "usuário B tenta acessar recurso do usuário A", que é exatamente o cenário que expõe Broken Access Control, e é exatamente o cenário que ninguém lembra de simular manualmente, toda vez, em todo endpoint, antes de todo deploy.

O diagnóstico não é "o time foi descuidado" — é que teste manual e teste automatizado resolvem problemas diferentes. Um humano clicando no Swagger UI prova que a API responde algo plausível **hoje**, para o cenário que ele lembrou de testar. Não prova nada sobre o próximo commit, e não prova nada sobre um cenário que ninguém pensou em simular à mão porque parece "óbvio que já funciona". O que falta não é mais disciplina de QA manual — é um jeito de codificar "usuário B nunca acessa recurso de usuário A" como uma asserção que roda sozinha, a cada `git commit`, sem depender de ninguém lembrar de testar isso de novo. É exatamente esse jeito que o resto desta nota constrói: `TestClient` para simular a requisição HTTP sem servidor real, e `dependency_overrides` para trocar autenticação e banco por versões de teste controladas.

## `TestClient`: requisição HTTP sem servidor, sem porta, sem rede

A primeira peça é mecânica: como testar uma rota FastAPI sem rodar `uvicorn main:app` de verdade, sem abrir uma porta TCP, sem depender de rede. O FastAPI é construído sobre o **Starlette** — o framework ASGI de baixo nível que trata o roteamento e o protocolo de requisição/resposta — e o `TestClient` explora isso diretamente: ele instancia a aplicação ASGI (o objeto `app`) e simula uma requisição chamando-a **em processo**, como se fosse uma chamada de função Python, em vez de abrir um socket e mandar bytes por uma rede real.

```python
from fastapi.testclient import TestClient

from main import app

client = TestClient(app)

resposta = client.get("/tarefas")
print(resposta.status_code)   # 200, 401, o que a rota devolver — sem nenhum servidor rodando
print(resposta.json())        # corpo já parseado como dict/list Python
```

`TestClient` é, por baixo, um `httpx.Client` configurado com um **transport ASGI** apontando direto para o objeto `app` — em vez de resolver um hostname e abrir uma conexão TCP, o `httpx` entrega a requisição simulada diretamente à aplicação, que processa exatamente a mesma pilha de middleware, roteamento, validação Pydantic e exception handlers que processaria numa requisição real vinda da rede. Nada nessa pilha sabe (nem precisa saber) que a requisição não veio de um cliente HTTP de verdade — do ponto de vista do FastAPI, é uma requisição como qualquer outra.

> [!question]- Se não existe rede de verdade, esse teste ainda é confiável, ou é "de mentirinha"?
> É confiável para o que ele se propõe a testar: o comportamento da **aplicação** — roteamento, validação de entrada, execução do handler, serialização de resposta, exception handlers, status codes. O que ele não exercita é a camada de rede em si (DNS, TLS, proxies reversos, balanceadores de carga, timeouts de conexão) — isso é território de um teste de integração/end-to-end contra um ambiente real, um nível acima na pirâmide de testes já coberta em [[03-Dominios/Engenharia/Testes/index|Engenharia/Testes]]. `TestClient` fica na fronteira entre teste unitário e teste de integração: mais realista que chamar a função Python do handler diretamente (porque passa pela validação Pydantic, pelo roteamento, pelos middlewares — tudo que só existe quando o FastAPI processa a requisição como um todo), mas mais rápido e determinístico que subir um servidor de verdade e falar com ele por rede.

O ganho de velocidade é o que torna essa abordagem viável para rodar centenas de vezes por suíte: sem custo de handshake TCP, sem custo de subir um processo `uvicorn` separado, sem risco de porta já ocupada travando o CI — um teste de endpoint via `TestClient` roda na casa de milissegundos, comparável a um teste unitário puro, mesmo exercitando a pilha HTTP completa.

### Um teste completo: `POST /tarefas`

Retomando a API de Tarefas construída nas capstones dos Galhos 10 e 11 — `TarefaCreate`/`TarefaRead` como contratos distintos ([[03-Dominios/Tecnologia/Python/Web e APIs REST/09 - Capstone — uma API REST completa de ponta a ponta|Galho 10, capstone]]), `Depends(get_current_user)` protegendo a rota ([[03-Dominios/Tecnologia/Python/Segurança/09 - Capstone — hardening da API do Galho 10|Galho 11, capstone]]) — o primeiro teste de verdade valida status code **e** o formato do JSON de resposta, não só "não quebrou":

```python
# tests/test_tarefas.py
from fastapi.testclient import TestClient

from main import app

client = TestClient(app)


def test_criar_tarefa_retorna_201_com_shape_correto():
    resposta = client.post(
        "/tarefas",
        json={"titulo": "Revisar PR #482"},
        headers={"Authorization": "Bearer token-de-teste-valido"},
    )

    assert resposta.status_code == 201

    corpo = resposta.json()
    assert corpo["titulo"] == "Revisar PR #482"
    assert corpo["concluida"] is False
    assert isinstance(corpo["id"], int)
    assert isinstance(corpo["usuario_id"], int)
    assert "criada_em" in corpo
    # o cliente NUNCA manda usuario_id — a checagem confirma que o servidor
    # não devolve nem aceita esse campo vindo do payload (Galho 11, nota 05)
    assert "senha" not in corpo and "senha_hash" not in corpo
```

Esse teste, do jeito que está escrito, ainda não passa de verdade num CI limpo — `"Bearer token-de-teste-valido"` não é um JWT válido, e `Depends(get_db)` tentaria abrir uma conexão real contra o Postgres de produção, que não existe (nem deveria existir) no ambiente de teste. As duas próximas seções resolvem exatamente essas duas dependências externas, uma de cada vez, com o mecanismo que dá nome a esta nota.

## `app.dependency_overrides`: trocando `get_db` sem tocar em produção

A [[03-Dominios/Tecnologia/Python/Web e APIs REST/04 - Injeção de dependência no FastAPI — Depends|nota 04 do Galho 10]] já nomeou o mecanismo, de passagem, na seção "O que torna o FastAPI testável": `app.dependency_overrides` é um dicionário que mapeia uma função de dependência original para uma substituta. Toda rota que declara `Depends(get_db)` recebe, em teste, o que estiver mapeado para `get_db` nesse dicionário — sem tocar em um handler sequer, sem `if os.environ.get("TESTING")` espalhado pelo código de produção.

```python
# tests/conftest.py
from collections.abc import Generator

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy.pool import StaticPool

from db import get_db
from main import app
from models import Base

engine_teste = create_engine(
    "sqlite:///:memory:",
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,   # garante UMA conexão compartilhada — necessário para SQLite em memória
)
SessionTeste = sessionmaker(bind=engine_teste)


@pytest.fixture(scope="session", autouse=True)
def criar_schema_de_teste():
    """Cria as tabelas uma vez para a sessão de testes inteira, a partir do MESMO
    metadata declarativo (Base) usado em produção — nunca um schema escrito à mão
    em paralelo, que poderia divergir do real."""
    Base.metadata.create_all(bind=engine_teste)
    yield
    Base.metadata.drop_all(bind=engine_teste)


def override_get_db() -> Generator[Session, None, None]:
    """Substituto de get_db — mesma assinatura, mesma forma de yield/finally,
    mas apontando para o Engine de teste em vez do Engine de produção."""
    db = SessionTeste()
    try:
        yield db
    finally:
        db.close()


@pytest.fixture
def client() -> Generator[TestClient, None, None]:
    app.dependency_overrides[get_db] = override_get_db
    yield TestClient(app)
    app.dependency_overrides.clear()   # nunca esquecer — próxima seção explica por quê
```

`override_get_db` tem a mesma forma que `get_db` — mesma assinatura de retorno (`Generator[Session, None, None]`), mesmo padrão `try/yield/finally` que a [[02 - Fixtures — escopos, yield e conftest.py|nota 02 deste galho]] já explicou para fixtures em geral, e que a nota 04 do Galho 10 explicou para dependências do FastAPI. A única diferença é de onde vem a `Session`: `SessionTeste`, montada sobre um `engine_teste` que aponta para um banco **SQLite em memória**, não o Postgres real de produção.

> [!warning] SQLite em memória é rápido, mas não é 100% fiel ao Postgres
> `sqlite:///:memory:` é a escolha certa para este teste de endpoint — rápido, sem dependência externa, sem estado que sobrevive entre execuções da suíte. Mas SQLite e Postgres divergem em detalhes reais: tipos de coluna, comportamento de constraint, isolamento de transação. Um teste que valida "o endpoint devolve o shape certo de JSON" está seguro em SQLite; um teste que valida comportamento fino de concorrência ou de uma constraint específica do Postgres precisa do banco real — a [[06 - Testando a camada de persistência — banco de teste e rollback|nota 06 deste galho]] desenvolve essa ressalva em profundidade, incluindo `testcontainers-python` como alternativa mais fiel. Aqui, para testar a **API**, não a camada de persistência em si, SQLite em memória é a escolha pragmática.

Com a fixture `client` disponível via `conftest.py` — sem nenhum import explícito no arquivo de teste, o mesmo mecanismo de descoberta automática que a nota 02 já ensinou — o teste de criação de tarefa já pode rodar contra um banco de teste real, isolado, recriado do zero a cada execução da suíte:

```python
# tests/test_tarefas.py
def test_criar_tarefa_retorna_201_com_shape_correto(client):
    resposta = client.post(
        "/tarefas",
        json={"titulo": "Revisar PR #482"},
        headers={"Authorization": "Bearer token-de-teste-valido"},
    )
    assert resposta.status_code == 201
    # ... resto do teste, igual à versão anterior
```

O token continua sendo um problema — `Depends(get_current_user)` ainda tentaria decodificar `"token-de-teste-valido"` como um JWT de verdade e falharia com `401`. É exatamente o mesmo mecanismo de override, aplicado a uma segunda dependência, que fecha essa lacuna.

## `app.dependency_overrides` para autenticação: usuário fixo, sem login de verdade

A [[03-Dominios/Tecnologia/Python/Segurança/05 - Autenticação e autorização na prática — a ponte com Auth e Identidade|nota 05 do Galho 11]] mostrou `get_current_user` decodificando um JWT de verdade — `PyJWT`, `jwt.decode`, expiração, assinatura. Gerar um token real e válido em cada teste funcionaria, mas acopla toda a suíte de API ao mecanismo interno de autenticação: qualquer mudança no algoritmo de assinatura, no formato do payload, ou no tempo de expiração do token quebraria centenas de testes que não têm nada a ver com autenticação em si — eles só precisam de **um usuário autenticado qualquer**, para testar a lógica de tarefas.

`app.dependency_overrides` resolve isso da mesma forma que resolveu `get_db`: troca `get_current_user` por uma função que devolve um usuário fixo, sem decodificar nada.

```python
# tests/conftest.py (continuação)
from auth import get_current_user
from models import Usuario

USUARIO_DE_TESTE = Usuario(id=1, nome="Ana Teste", email="ana@teste.com", senha_hash="irrelevante")


def override_get_current_user() -> Usuario:
    """Substituto de get_current_user — devolve um usuário fixo, sem decodificar JWT nenhum.
    A suíte de testes de tarefas não está testando autenticação — está testando tarefas."""
    return USUARIO_DE_TESTE


@pytest.fixture
def client() -> Generator[TestClient, None, None]:
    app.dependency_overrides[get_db] = override_get_db
    app.dependency_overrides[get_current_user] = override_get_current_user
    yield TestClient(app)
    app.dependency_overrides.clear()
```

Com os dois overrides ativos, o teste de criação de tarefa passa a rodar de ponta a ponta sem depender de banco real nem de um JWT real — só do comportamento da própria API:

```python
def test_criar_tarefa_retorna_201_com_shape_correto(client):
    resposta = client.post("/tarefas", json={"titulo": "Revisar PR #482"})
    # nenhum header de Authorization — o override já devolve o usuário fixo

    assert resposta.status_code == 201
    corpo = resposta.json()
    assert corpo["titulo"] == "Revisar PR #482"
    assert corpo["usuario_id"] == USUARIO_DE_TESTE.id
    assert corpo["concluida"] is False
```

```mermaid
%%{init: {"theme": "base", "themeVariables": {"primaryColor": "#4A90D9"}}}%%
sequenceDiagram
    participant Teste as test_criar_tarefa(client)
    participant TC as TestClient
    participant App as app (FastAPI, em processo)
    participant DepDB as Depends(get_db)
    participant DepAuth as Depends(get_current_user)
    participant Handler as criar_tarefa()

    Teste->>TC: client.post("/tarefas", json={"titulo": "..."})
    TC->>App: requisição ASGI simulada (sem rede)
    App->>DepDB: resolve get_db
    Note over DepDB: app.dependency_overrides[get_db]<br/>→ override_get_db (SQLite em memória)
    DepDB-->>App: db (Session de TESTE)
    App->>DepAuth: resolve get_current_user
    Note over DepAuth: app.dependency_overrides[get_current_user]<br/>→ override_get_current_user (usuário fixo)
    DepAuth-->>App: current_user (USUARIO_DE_TESTE)
    App->>Handler: criar_tarefa(dados, current_user, db)
    Handler->>DepDB: db.add(tarefa), db.commit()
    Handler-->>App: return tarefa
    App-->>TC: 201 {"id": 1, "usuario_id": 1, "titulo": "...", ...}
    TC-->>Teste: resposta.status_code, resposta.json()
```

O diagrama nomeia o ponto central: nada no `Handler` (`criar_tarefa`) muda entre produção e teste — a mesma função, a mesma assinatura, o mesmo `Depends(get_db)`/`Depends(get_current_user)` na declaração. O que muda é **o que está atrás** de cada `Depends()`, e essa troca acontece inteiramente fora do código de produção, no dicionário `app.dependency_overrides`, montado pela fixture `client` de teste.

> [!tip] `dependency_overrides` funciona para qualquer `Depends()`, não só banco e auth
> O mesmo padrão substitui qualquer dependência — um cliente HTTP para uma API externa por um stub que devolve dados fixos, um serviço de envio de e-mail por um double que só registra chamadas, uma dependência de feature flag por um valor fixo para o teste. Qualquer parâmetro de rota resolvido via `Depends()` é, por construção, um ponto de substituição em teste — a técnica de mock em si (`unittest.mock`, `pytest-mock`, quando substituir não é só trocar uma função inteira mas controlar o comportamento de um objeto complexo) é o assunto da [[04 - Mocking com unittest.mock e pytest-mock|nota 04 deste galho]], não repetido aqui.

> [!warning] Esquecer `app.dependency_overrides.clear()` vaza override entre testes
> **O que acontece:** um teste faz `app.dependency_overrides[get_current_user] = override_para_admin` (por exemplo, para testar uma rota que só admin acessa) e não desfaz isso ao final — o próximo teste da suíte, que esperava o usuário fixo padrão, herda a substituição do teste anterior, produzindo falhas que dependem da ordem de execução dos testes. **Por quê:** `app.dependency_overrides` é um dicionário pertencente à instância `app` inteira, compartilhado por toda a suíte — não existe escopo automático por teste; o FastAPI não sabe (nem tenta saber) quando um teste "terminou". **Como evitar:** a fixture `client` mostrada acima já resolve isso estruturalmente — o `app.dependency_overrides.clear()` depois do `yield` roda como teardown garantido (o mesmo mecanismo de `yield` em fixtures que a nota 02 já ensinou), independentemente do teste passar ou falhar. Um teste que precisa de um override diferente do padrão (como o cenário "usuário B" da seção seguinte) sobrescreve a chave especificamente, dentro do próprio teste, e a fixture ainda garante a limpeza completa ao final.

## O par Django: `Client` e `pytest-django`

Django resolve o mesmo problema — testar uma view sem servidor real — com um mecanismo equivalente em espírito, embora sintaticamente diferente. O `django.test.Client` (biblioteca padrão do Django, funciona com `unittest.TestCase` ou solto) simula requisições contra as URLs registradas, exatamente como `TestClient` simula contra as rotas FastAPI:

```python
# Django puro, sem pytest-django
from django.test import TestCase


class TarefaViewTests(TestCase):
    def test_criar_tarefa_retorna_201(self):
        resposta = self.client.post(
            "/tarefas/",
            data={"titulo": "Revisar PR #482"},
            content_type="application/json",
        )
        self.assertEqual(resposta.status_code, 201)
```

Quando o projeto já adotou `pytest` como runner (o caminho que este galho segue desde a [[01 - pytest fundamentos — anatomia, discovery e assert introspection|nota 01]]), o plugin `pytest-django` substitui esse `self.client` por uma **fixture** chamada `client`, seguindo o mesmo mecanismo de injeção por nome de parâmetro:

```python
# Com pytest-django — função solta, sem TestCase
import pytest


def test_criar_tarefa_retorna_201(client):
    resposta = client.post(
        "/tarefas/",
        data={"titulo": "Revisar PR #482"},
        content_type="application/json",
    )
    assert resposta.status_code == 201
```

Duas peças do `pytest-django` merecem nome, porque não têm equivalente direto na versão FastAPI mostrada acima:

- **`django_db` (marker)** — por padrão, `pytest-django` **bloqueia** qualquer acesso a banco de dados dentro de um teste, levantando um erro explícito se algum código tentar tocar o banco sem permissão. Um teste que precisa persistir dado real declara `@pytest.mark.django_db` (ou recebe a fixture `db`), o que sinaliza explicitamente "este teste toca banco" — o oposto do FastAPI, onde `Depends(get_db)` já é substituído silenciosamente pelo override sem nenhum marcador extra no teste.

```python
import pytest


@pytest.mark.django_db
def test_criar_tarefa_persiste_no_banco(client):
    resposta = client.post("/tarefas/", data={"titulo": "..."}, content_type="application/json")
    assert resposta.status_code == 201
    # sem @pytest.mark.django_db, esta linha levantaria um erro de acesso a banco não autorizado
```

- **Autenticação via `force_login`** — em vez de um dicionário de `dependency_overrides` trocando uma função de dependência, `pytest-django`/`Client` expõe `client.force_login(usuario)`, que injeta a sessão autenticada direto no cliente de teste, pulando o fluxo de login real (senha, formulário) da mesma forma que `override_get_current_user` pula a decodificação de JWT:

```python
@pytest.mark.django_db
def test_usuario_ve_apenas_as_proprias_tarefas(client, django_user_model):
    usuario = django_user_model.objects.create_user(username="ana", password="irrelevante")
    client.force_login(usuario)

    resposta = client.get("/tarefas/")
    assert resposta.status_code == 200
```

> [!question]- `force_login` e `dependency_overrides` resolvem exatamente o mesmo problema?
> A intenção é idêntica — pular o mecanismo real de autenticação em teste, sem reimplementar login de verdade a cada caso — mas o ponto de intervenção é diferente, e vale nomear a diferença porque ela reflete a diferença de arquitetura entre os dois frameworks. `dependency_overrides` troca a **função** que o FastAPI chamaria para resolver a identidade — o mecanismo de injeção de dependência inteiro, coberto em detalhe pela [[03-Dominios/Tecnologia/Python/Web e APIs REST/04 - Injeção de dependência no FastAPI — Depends|nota 04 do Galho 10]]. `force_login` opera uma camada abaixo: ele popula a **sessão** (o mecanismo nativo `django.contrib.auth` que [[03-Dominios/Engenharia/Auth e Identidade/4 - Auth nos stacks/02 - Python — Django|Auth e Identidade SG4, Python — Django]] já cobriu) diretamente no `Client` de teste, sem passar por nenhuma "dependência" no sentido FastAPI — Django não tem um `Depends()` equivalente para autenticação, `request.user` é resolvido por middleware de sessão, não por injeção de parâmetro. Uma API DRF autenticada via token (não sessão) usaria, em vez de `force_login`, `client.credentials(HTTP_AUTHORIZATION=f"Token {token.key}")` ou um token real gerado em fixture — o padrão específico depende do backend de autenticação escolhido, mas o princípio — pular o fluxo real de login, injetar identidade diretamente — é o mesmo dos dois lados.

| Aspecto | FastAPI (`TestClient`) | Django (`Client`/`pytest-django`) |
|---|---|---|
| Requisição simulada | `TestClient(app)`, sobre `httpx` + transport ASGI | `Client()`, ou fixture `client` do `pytest-django` |
| Trocar banco por versão de teste | `app.dependency_overrides[get_db] = override_get_db` | `@pytest.mark.django_db` (habilita acesso; usa banco de teste automático) |
| Trocar autenticação por usuário fixo | `app.dependency_overrides[get_current_user] = override_...` | `client.force_login(usuario)` |
| Ponto de intervenção | Dicionário de override na instância `app` | Sessão populada direto no `Client`, ou `db_user_model`/token de fixture |
| Acesso a banco sem marcação explícita | Permitido (a substituição já aponta para banco de teste) | Bloqueado por padrão — exige `django_db` explícito |

## O teste mais rico: criar, listar, e a tarefa que não é sua

Voltando ao objetivo original desta nota — provar, de forma automatizada, que a correção de Broken Access Control do [[03-Dominios/Tecnologia/Python/Segurança/09 - Capstone — hardening da API do Galho 10|Galho 11, capstone]] continua valendo — o teste isolado de criação não basta. O cenário que expõe o bug do incidente de abertura precisa de **dois usuários**: um cria uma tarefa, outro tenta acessá-la.

```python
# tests/test_tarefas.py
from models import Usuario

USUARIO_A = Usuario(id=1, nome="Ana", email="ana@teste.com", senha_hash="irrelevante")
USUARIO_B = Usuario(id=2, nome="Bruno", email="bruno@teste.com", senha_hash="irrelevante")


def override_usuario(usuario: Usuario):
    """Fábrica de override — devolve uma função Depends() fixa para UM usuário específico,
    permitindo trocar 'quem está logado' dentro do próprio teste."""
    def _override() -> Usuario:
        return usuario
    return _override


def test_fluxo_completo_criar_listar_e_negar_acesso_de_outro_usuario(client):
    from auth import get_current_user
    from main import app

    # --- Usuário A cria uma tarefa ---
    app.dependency_overrides[get_current_user] = override_usuario(USUARIO_A)
    resposta_criacao = client.post("/tarefas", json={"titulo": "Fechar relatório fiscal"})
    assert resposta_criacao.status_code == 201
    tarefa_id = resposta_criacao.json()["id"]

    # --- Usuário A lista suas próprias tarefas: a tarefa criada aparece ---
    resposta_listagem_a = client.get("/tarefas")
    assert resposta_listagem_a.status_code == 200
    titulos_de_a = [t["titulo"] for t in resposta_listagem_a.json()]
    assert "Fechar relatório fiscal" in titulos_de_a

    # --- Usuário B (outra identidade) tenta acessar a MESMA tarefa ---
    app.dependency_overrides[get_current_user] = override_usuario(USUARIO_B)
    resposta_acesso_indevido = client.get(f"/tarefas/{tarefa_id}")

    # Regressão de Broken Access Control (Galho 11, nota 05): 404, não 200 nem 403 —
    # a query já nasce filtrada por dono, então a tarefa de A "não existe" para B
    assert resposta_acesso_indevido.status_code == 404

    # --- Usuário B lista as PRÓPRIAS tarefas: a tarefa de A não aparece ---
    resposta_listagem_b = client.get("/tarefas")
    assert resposta_listagem_b.status_code == 200
    titulos_de_b = [t["titulo"] for t in resposta_listagem_b.json()]
    assert "Fechar relatório fiscal" not in titulos_de_b

    # --- Usuário B tenta APAGAR a tarefa de A — verbo destrutivo, mesma proteção ---
    resposta_delete_indevido = client.delete(f"/tarefas/{tarefa_id}")
    assert resposta_delete_indevido.status_code == 404
```

Este teste único cobre o que o incidente de abertura desta nota mostrou como lacuna: não é "o endpoint devolve 200 para o dono", é "o endpoint devolve **404** para quem não é dono, em GET **e** em DELETE, não só no caminho que alguém lembrou de testar manualmente". Se um refactor futuro remover a chamada à função de checagem de posse num dos quatro verbos — exatamente o incidente do cenário de abertura, onde o quarto endpoint esqueceu de chamar `_buscar_tarefa_do_usuario` — este teste **falha**, imediatamente, no CI, antes do código chegar a produção. É a diferença entre "alguém vai perceber isso no próximo pentest, se sobrar orçamento" e "o pipeline vermelho impede o merge".

```mermaid
%%{init: {"theme": "base", "themeVariables": {"primaryColor": "#4A90D9"}}}%%
flowchart TD
    A["Usuário A: POST /tarefas<br/>cria tarefa (id=X)"] --> B["Usuário A: GET /tarefas<br/>tarefa X aparece na lista"]
    B --> C["Troca override para Usuário B"]
    C --> D["Usuário B: GET /tarefas/X"]
    D --> E{"Status esperado?"}
    E -->|"404 — correto"| F["Broken Access Control<br/>continua corrigido"]
    E -->|"200 — REGRESSÃO"| G["Teste FALHA — bloqueia o merge<br/>antes do pentest encontrar em produção"]
    C --> H["Usuário B: DELETE /tarefas/X"]
    H --> I{"Status esperado?"}
    I -->|"404 — correto"| F
    I -->|"204/200 — REGRESSÃO"| G

    style F fill:#2d7a4a,color:#fff
    style G fill:#D0021B,color:#fff
```

> [!question]- Por que trocar o override DENTRO do teste, em vez de duas fixtures `client_a`/`client_b` separadas?
> As duas abordagens funcionam; a escolha aqui é pedagógica e também prática. Trocar `app.dependency_overrides[get_current_user]` no meio do teste deixa explícito, na leitura linear do código, o momento exato em que a identidade muda — "a partir daqui, quem está fazendo a requisição é outra pessoa" — o que ajuda a comunicar a intenção do teste a quem lê. Em uma suíte maior, com muitos testes que precisam de "dois usuários interagindo", vale a pena extrair duas fixtures (`client_como_usuario_a`, `client_como_usuario_b`) que já vêm com o override certo aplicado — reduzindo a repetição do padrão `override_usuario(...)` em cada teste, o mesmo princípio de composição de fixtures que a [[02 - Fixtures — escopos, yield e conftest.py|nota 02 deste galho]] já desenvolveu para `engine_db`/`sessao_db`.

> [!tip] Este é o teste que a nota 05 do Galho 11 já cobrou, sem desenvolver
> A [[03-Dominios/Tecnologia/Python/Segurança/05 - Autenticação e autorização na prática — a ponte com Auth e Identidade|nota 05 do Galho 11]] listou, no checklist de armadilhas, "existe pelo menos um teste automatizado por endpoint sensível simulando 'usuário B tenta acessar recurso do usuário A'?" como item não-opcional — sem mostrar o código, porque `TestClient`/fixtures ainda não tinham sido ensinados naquele ponto da trilha. Este teste é essa dívida paga: a prova de que "autenticado não é autorizado" não é só uma frase de code review, é uma asserção que roda a cada commit.

## Armadilhas comuns

> [!warning] Testar só o caminho feliz de autenticação, nunca o de acesso cruzado
> **O que acontece:** a suíte cobre "usuário logado cria/lê/atualiza a própria tarefa" com testes verdes, e "usuário não logado recebe 401" — mas nunca "usuário logado tenta acessar recurso de outro usuário logado". É exatamente o gap do incidente de abertura desta nota, e o mesmo apontado como armadilha na nota 05 do Galho 11. **Por quê:** os dois primeiros cenários são os que qualquer desenvolvedor pensa em testar primeiro, porque são os que ele mesmo exercitaria manualmente logando com uma conta só. O terceiro cenário exige pensar deliberadamente como um atacante, não como um usuário legítimo. **Como evitar:** todo endpoint que opera sobre um recurso com dono ganha, na suíte, pelo menos um teste no formato desta nota — dois usuários, um cria, o outro tenta acessar/editar/apagar, espera `403`/`404`. Tratar isso como item do checklist de PR de qualquer endpoint novo sobre recurso protegido, não como cobertura "bônus".

> [!warning] Override de dependência que não reflete o comportamento real da dependência original
> **O que acontece:** `override_get_current_user` sempre devolve um usuário **ativo**, mas a dependência real também precisa lidar com usuário desativado, token expirado, usuário deletado depois de emitido o token — e nenhum teste cobre esses casos porque o override "sempre funciona". **Por quê:** um override simplificado demais testa só o caminho onde a substituição funciona perfeitamente — não testa o comportamento real de `get_current_user` em si (que é conteúdo de outra suíte, focada na função `get_current_user` isoladamente, sem TestClient), mas também corre o risco de dar falsa confiança de que "autenticação está testada" quando só a integração com usuário válido está. **Como evitar:** ter overrides separados para os poucos casos que a suíte de API precisa simular (usuário válido, ausência de token) e, à parte, uma suíte unitária específica para `get_current_user` (sem `TestClient`, chamando a função Python diretamente com um JWT forjado de teste) cobrindo token expirado, assinatura inválida, usuário inexistente — a fronteira entre "testar a API que consome a dependência" e "testar a dependência em si" evita que uma suíte tente cobrir demais e nenhuma cubra bem.

> [!warning] `TestClient` sem `raise_server_exceptions=False` mascara o comportamento real de erro em produção
> **O que acontece:** por padrão, `TestClient` **propaga** exceções não tratadas do handler como exceções Python no próprio teste, em vez de deixar o exception handler genérico (`@app.exception_handler(Exception)`, coberto na capstone do Galho 10) capturá-las e devolver o `500` formatado que o cliente real receberia. **Por quê:** esse comportamento padrão existe para facilitar depuração durante o desenvolvimento do teste — ver o traceback completo no próprio `pytest`, em vez de só um `resposta.status_code == 500` genérico. Mas para um teste que quer validar especificamente **a resposta que um cliente real receberia** (o envelope de erro `type`/`title`/`status`/`detail` da nota 06 do Galho 10), esse comportamento padrão esconde exatamente o que está sendo testado. **Como evitar:** para testes que validam o contrato de erro 500 propositalmente, instanciar `TestClient(app, raise_server_exceptions=False)` — nesse modo, o `TestClient` se comporta como um cliente real, recebendo o `JSONResponse` que o exception handler genérico produziu, em vez da exceção Python crua.

## Em entrevista

- **"Como você testa um endpoint FastAPI sem subir um servidor real?"** `TestClient`, do próprio pacote `fastapi.testclient`, é um `httpx.Client` configurado com transport ASGI apontando direto para o objeto `app` — a requisição é simulada em processo, passando pela mesma pilha de roteamento, validação e exception handlers que uma requisição real, sem custo de rede.
- **"Como você troca uma sessão de banco real por uma de teste, sem mudar o código de produção?"** `app.dependency_overrides[get_db] = override_get_db` — um dicionário na instância `app` que mapeia a dependência original para a substituta; toda rota que declara `Depends(get_db)` recebe automaticamente o override em teste, sem tocar em nenhum handler.
- **"Como você testa uma rota autenticada sem fazer login de verdade em cada teste?"** O mesmo mecanismo aplicado a `get_current_user` — um override devolve um usuário fixo direto, sem decodificar JWT nenhum; a suíte de tarefas testa lógica de tarefas, não o mecanismo de autenticação em si, que tem sua própria suíte dedicada.
- **"Como você garante, de forma automatizada, que um bug de Broken Access Control não volta a acontecer?"** Um teste que simula dois usuários diferentes — um cria o recurso, o outro tenta acessar, esperando `403`/`404` — trocando o override de identidade no meio do próprio teste. Sem esse teste, a proteção de posse depende de disciplina de code review revisitando cada endpoint novo; com ele, uma regressão quebra o CI antes de chegar a produção.

> [!question]- O entrevistador pergunta: "e no Django, como você faria o equivalente?"
> A resposta madura nomeia a semelhança de objetivo e a diferença de mecânica, sem tentar forçar uma analogia 1:1: "o objetivo é o mesmo — simular uma requisição sem servidor real, e trocar autenticação/acesso a banco por versões controladas de teste. Django resolve com `django.test.Client` (ou a fixture `client` do `pytest-django`), que também simula requisições em processo. A diferença é que Django não tem um mecanismo de injeção de dependência tipo `Depends()` para trocar — autenticação em teste é resolvida populando a sessão diretamente com `client.force_login(usuario)`, e acesso a banco é controlado pelo marker `@pytest.mark.django_db`, que por padrão **bloqueia** qualquer teste de tocar banco sem essa marcação explícita — o oposto do FastAPI, onde o override já libera acesso implicitamente."

## How to explain in English

> Testing a FastAPI endpoint doesn't require a running server: `TestClient` wraps an `httpx.Client` around an ASGI transport that talks to the `app` object directly, in-process — same routing, same Pydantic validation, same exception handlers a real request would hit, but at the speed of a function call. The piece that makes this testable without touching production code is `app.dependency_overrides`, a dictionary on the `app` instance that swaps any `Depends()`-declared dependency for a test substitute — a real database session becomes an in-memory SQLite session, and a JWT-decoding `get_current_user` becomes a function that just returns a fixed test user, no login flow required. The highest-value test built on top of this isn't "endpoint returns 200" — it's a two-identity flow: user A creates a resource, then the override swaps to user B, who tries to read or delete that same resource and should get a 404. That single test is what turns "we fixed a Broken Access Control bug" into "we can't regress it without the CI catching it first" — the automated proof that a manual pentest checklist item, tested once, keeps holding after every subsequent commit. Django's equivalent swaps the mechanism, not the goal: `Client`/`pytest-django`'s `client` fixture simulates requests the same way, `force_login()` injects an authenticated session directly instead of overriding a dependency function, and `@pytest.mark.django_db` explicitly opts a test into database access, which FastAPI's override approach grants implicitly.

| PT | EN |
|----|----|
| requisição simulada / em processo | simulated / in-process request |
| substituir dependência | override a dependency |
| usuário de teste fixo | fixed test user |
| acesso cruzado entre usuários | cross-user access |
| regressão de segurança | security regression |
| fluxo completo (end-to-end dentro da API) | end-to-end flow |

## Síntese

`TestClient` resolve a mecânica — simular uma requisição HTTP completa, com toda a pilha do FastAPI processando-a, sem pagar o custo (nem o determinismo frágil) de um servidor real escutando numa porta. `app.dependency_overrides` resolve o isolamento — qualquer `Depends()`, banco ou autenticação, vira um ponto de substituição controlado em teste, sem uma linha de `if TESTING` no código de produção, o mesmo princípio de injeção de dependência que a [[03-Dominios/Tecnologia/Python/Web e APIs REST/04 - Injeção de dependência no FastAPI — Depends|nota 04 do Galho 10]] já tinha nomeado como o que torna o FastAPI testável, agora com o código real que faltava. Django resolve o mesmo par de problemas com uma mecânica diferente — `Client`/`pytest-django` para a requisição simulada, `force_login`/`django_db` para autenticação e acesso a banco — mas a intenção estrutural é idêntica nos dois ecossistemas: nenhum teste de API deveria depender de rede real, de um banco de produção, ou de um fluxo de login genuíno para validar o que a rota faz.

O ganho real não é sintático — é o que esse ferramental torna possível provar: que "autenticado não é autorizado", a lição central do [[03-Dominios/Tecnologia/Python/Segurança/05 - Autenticação e autorização na prática — a ponte com Auth e Identidade|Galho 11, nota 05]], deixa de ser uma checagem manual, feita uma vez, num pentest, e vira uma asserção que roda a cada commit — o mesmo tipo de garantia contínua que a [[03-Dominios/Tecnologia/Python/Segurança/09 - Capstone — hardening da API do Galho 10|capstone do Galho 11]] já apontou como a lacuna que restava depois do hardening manual. A próxima nota deste galho troca a camada testada: da API HTTP para a persistência por trás dela — como isolar um banco de teste de verdade (SQLite versus Postgres real, rollback automático entre testes) sem repetir a ressalva de fidelidade já levantada aqui.

## Veja também

- [[01 - pytest fundamentos — anatomia, discovery e assert introspection|01 — pytest fundamentos]] — anatomia de um teste e discovery, base para os testes de API desta nota.
- [[02 - Fixtures — escopos, yield e conftest.py|02 — Fixtures: escopos, yield e conftest.py]] — mecanismo de fixture com `yield` reaproveitado na fixture `client` desta nota; padrão de composição de fixtures usado para separar `override_get_db` de `override_get_current_user`.
- [[03 - Parametrização e organização de suíte|03 — Parametrização e organização de suíte]] — organização `tests/unit`/`tests/integration`; os testes de API desta nota pertencem à camada de integração dessa árvore.
- [[03-Dominios/Tecnologia/Python/Web e APIs REST/04 - Injeção de dependência no FastAPI — Depends|Galho 10, nota 04 — Injeção de dependência: Depends]] — mecanismo de `Depends()` e `app.dependency_overrides` mencionado ali de passagem, desenvolvido com código real nesta nota.
- [[03-Dominios/Tecnologia/Python/Web e APIs REST/09 - Capstone — uma API REST completa de ponta a ponta|Galho 10, capstone — API de Tarefas]] — a API concreta testada ao longo desta nota.
- [[03-Dominios/Tecnologia/Python/Segurança/05 - Autenticação e autorização na prática — a ponte com Auth e Identidade|Galho 11, nota 05 — Autenticação e autorização na prática]] — origem do padrão `Depends(get_current_user)` + filtro por dono, e da recomendação de teste "usuário B tenta acessar recurso do usuário A" validada nesta nota.
- [[03-Dominios/Tecnologia/Python/Segurança/09 - Capstone — hardening da API do Galho 10|Galho 11, capstone — hardening]] — a correção de Broken Access Control cuja regressão o teste desta nota impede.
- [[04 - Mocking com unittest.mock e pytest-mock|04 — Mocking com unittest.mock e pytest-mock]] — próxima nota deste galho; técnica de substituição mais granular que `dependency_overrides`, para quando o que precisa ser controlado é o comportamento de um objeto, não uma função de dependência inteira.
- [[06 - Testando a camada de persistência — banco de teste e rollback|06 — Testando a camada de persistência]] — próxima nota; aprofunda a ressalva de fidelidade SQLite vs. Postgres levantada aqui, e o padrão de rollback automático entre testes.
- [[03-Dominios/Tecnologia/Python/Testes/index|Testes (MOC do galho)]]

## Fontes

- FastAPI. *Testing*. fastapi.tiangolo.com/tutorial/testing/. https://fastapi.tiangolo.com/tutorial/testing/ (acessado em 2026-07-11) — `TestClient`, requisições simuladas, exemplos de assert sobre status/JSON.
- FastAPI. *Testing Dependencies with Overrides*. fastapi.tiangolo.com/advanced/testing-dependencies/. https://fastapi.tiangolo.com/advanced/testing-dependencies/ (acessado em 2026-07-11) — `app.dependency_overrides`, padrão canônico de troca de `get_db`.
- FastAPI. *Testing a Database*. fastapi.tiangolo.com/how-to/testing-database/. https://fastapi.tiangolo.com/how-to/testing-database/ (acessado em 2026-07-11) — banco de teste SQLite em memória com `StaticPool`, o padrão usado nesta nota.
- Starlette. *Test Client*. starlette.io/testclient/. https://www.starlette.io/testclient/ (acessado em 2026-07-11) — mecanismo interno do `TestClient` sobre `httpx` e transport ASGI.
- pytest-django. *Documentation — Database access*, *Documentation — client fixtures*. pytest-django.readthedocs.io. https://pytest-django.readthedocs.io/en/latest/database.html e https://pytest-django.readthedocs.io/en/latest/helpers.html#client (acessados em 2026-07-11) — marker `django_db`, fixture `client`, `force_login`.
- Real Python. *Testing Your FastAPI App with pytest*. realpython.com. https://realpython.com/fastapi-testing/ (acessado em 2026-07-11) — padrões de teste de API FastAPI com overrides de autenticação e banco.
- [[03-Dominios/Tecnologia/Python/Web e APIs REST/04 - Injeção de dependência no FastAPI — Depends|Injeção de dependência no FastAPI — Depends]] — nota do Galho 10, referenciada para o mecanismo base de `Depends()`/`dependency_overrides`.
- [[03-Dominios/Tecnologia/Python/Segurança/05 - Autenticação e autorização na prática — a ponte com Auth e Identidade|Autenticação e autorização na prática]] — nota do Galho 11, referenciada para o padrão de checagem de posse validado pelo teste de fluxo completo desta nota.

Consultado em 2026-07-11.
