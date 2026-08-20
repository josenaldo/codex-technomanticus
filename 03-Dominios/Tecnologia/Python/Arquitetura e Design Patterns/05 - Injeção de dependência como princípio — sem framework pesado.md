---
title: "Injeção de dependência como princípio — sem framework pesado"
created: 2026-07-12
type: concept
fase: Magus
status: complete
publish: true
tags:
  - python
  - arquitetura
  - design-patterns
  - dependency-injection
aliases:
  - "Injeção de dependência em Python"
  - "Composition root"
  - "DI sem container"
  - "dependency-injector"
---

# Injeção de dependência como princípio — sem framework pesado

> [!abstract] TL;DR
> Injeção de dependência (DI) não é sinônimo de framework — é um princípio: **quem decide qual implementação concreta usar não é o código que a consome, é uma camada externa a ele**, geralmente o ponto de entrada da aplicação (o *composition root*). Em Java/Spring, esse princípio quase sempre vem empacotado com um contêiner de IoC (`@Autowired`, `@Component`, scanning automático de classpath) porque a linguagem tem tipagem estática nominal e reflexão pesada — o contêiner existe para resolver, em tempo de boot, um grafo de dependências que o compilador sozinho não amarra. Python não precisa disso na maioria dos casos: funções e classes são objetos de primeira classe (o mesmo motivo que a [[01 - Por que GoF clássico é menos necessário em Python|nota 01 deste galho]] usou para explicar por que Strategy e Factory encolhem), então "decidir qual implementação injetar" é só passar um argumento — composição manual e explícita no `main.py`, sem scanning, sem reflexão, sem anotação de classe. Isso é diferente de `Depends()` do FastAPI, que é o **mecanismo** de resolução por requisição HTTP (já coberto na [[03-Dominios/Tecnologia/Python/Web e APIs REST/04 - Injeção de dependência no FastAPI — Depends|nota 04 do Galho 10]]) — esta nota discute a **decisão arquitetural** que acontece antes disso, uma vez, no bootstrap. Para aplicações muito grandes, com grafos de dependência profundos, um container dedicado como [`dependency-injector`](https://pypi.org/project/dependency-injector/) pode valer a pena — mas isso é exceção em Python, não a norma como é em Java.

## "Onde está o container de DI dessa aplicação?"

Um desenvolvedor sênior, doze anos de Spring, entra num time Python para revisar a arquitetura da API de Tarefas que este galho vem construindo — domínio puro ([[02 - Domain modeling — separando a lógica de negócio do framework|nota 02]]), Repository abstraindo persistência ([[03 - Repository pattern — abstraindo a persistência|nota 03]]), Unit of Work agrupando transações ([[04 - Unit of Work — formalizando o padrão que já existia|nota 04]]). Ele abre o `main.py`, procura pela configuração de beans, e não encontra nada parecido.

"Onde está o container de DI dessa aplicação?" — ele pergunta, genuinamente perdido. "Onde é que vocês registram qual `AbstractUnitOfWork` implementa a interface, pra o Spring... digo, pro que quer que vocês usem aqui, injetar automaticamente?"

A resposta do time é desconfortavelmente simples: "não tem container. É só uma função que instancia as coisas e passa como argumento."

Ele não fica satisfeito com essa resposta — soa como se o time estivesse pulando uma etapa importante, algo que qualquer aplicação backend séria deveria ter. Ele já viu código sem DI de verdade: singletons globais, `import` direto da implementação concreta espalhado por todo lugar, testes que não conseguem substituir nada porque tudo está hard-coded. Se não tem container, como é que esse código evita cair exatamente nessa armadilha?

A resposta fica clara olhando o `main.py` de verdade:

```python
# main.py — o composition root da aplicação
from fastapi import FastAPI
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from adapters.uow_sqlalchemy import SqlAlchemyUnitOfWork
from api.routers import tarefas

DATABASE_URL = "postgresql://user:senha@localhost/tarefas"

engine = create_engine(DATABASE_URL, pool_size=20)
SessionFactory = sessionmaker(bind=engine)


def criar_uow() -> SqlAlchemyUnitOfWork:
    """A ÚNICA linha da aplicação que sabe que a implementação é SQLAlchemy."""
    return SqlAlchemyUnitOfWork(session_factory=SessionFactory)


app = FastAPI()
app.dependency_overrides = {}  # ponto de substituição, ver seção de testes adiante
app.state.criar_uow = criar_uow
app.include_router(tarefas.router)
```

Não existe scanning de classpath, não existe anotação `@Component` marcando `SqlAlchemyUnitOfWork` como "a implementação a ser injetada", não existe um contêiner que descobre sozinho, em tempo de boot, qual classe satisfaz qual interface. Existe uma função de sete linhas — `criar_uow` — que **decide explicitamente** qual classe concreta instanciar, e esse é o único lugar do código inteiro que sabe disso. O resto da aplicação — Service Layer, handlers HTTP, testes — nunca importa `SqlAlchemyUnitOfWork` diretamente; recebe uma `AbstractUnitOfWork` já pronta, sem saber (nem precisar saber) de onde ela veio.

> [!question]- Isso não é só "esconder a injeção de dependência atrás de um nome bonito"? Onde está a inversão de controle de verdade?
> A inversão de controle está exatamente em quem **decide** a implementação: não é `criar_tarefa` (a função de caso de uso), nem `TarefaRouter` (o handler HTTP) — nenhum dos dois sabe, nem pode saber, que existe uma classe chamada `SqlAlchemyUnitOfWork`. Só o `main.py` sabe disso. Se amanhã a aplicação trocar de Postgres para outro banco, ou ganhar uma implementação de Unit of Work que grava também num event log, a mudança acontece **numa função só**, no composition root — nada na Service Layer, no domínio, ou nos handlers precisa mudar uma linha, porque eles nunca dependeram da implementação concreta, só da abstração (`AbstractUnitOfWork`). Isso É inversão de controle — só que a "inversão" não precisa de um framework para acontecer; ela é uma consequência de onde você escolhe colocar o `import` da classe concreta, uma decisão de design, não uma feature de linguagem ou biblioteca.

O resto desta nota desenvolve essa distinção com precisão: DI como **princípio** (quem decide a implementação) é diferente de `Depends()` como **mecanismo** (como o FastAPI resolve isso por requisição), e ambos são diferentes de um **container de DI dedicado** (uma biblioteca que automatiza a resolução do grafo inteiro) — que Python raramente precisa, mas que existe para quando precisa.

## Por que Spring precisa de um container, e Python geralmente não

Em Spring, a receita padrão é: uma interface (`UnitOfWork`), uma implementação anotada (`@Component class SqlUnitOfWork implements UnitOfWork`), e um ponto de consumo que declara a dependência via construtor ou `@Autowired`:

```java
public interface UnitOfWork {
    void commit();
    void rollback();
}

@Component
public class SqlUnitOfWork implements UnitOfWork {
    // ...
}

@Service
public class TarefaService {
    private final UnitOfWork uow;

    @Autowired
    public TarefaService(UnitOfWork uow) {
        this.uow = uow;
    }
}
```

Em nenhum lugar deste código alguém escreve `new SqlUnitOfWork()` dentro de `TarefaService`. O contêiner do Spring, no boot da aplicação, faz um **scan do classpath**, encontra todas as classes anotadas com `@Component`/`@Service`/`@Repository`, descobre que `SqlUnitOfWork` implementa `UnitOfWork`, e quando alguém pede um `UnitOfWork` no construtor de `TarefaService`, o contêiner resolve automaticamente qual instância entregar — usando **reflexão** para inspecionar construtores, anotações e tipos declarados em tempo de compilação.

Essa maquinaria existe porque Java precisa dela para o problema que resolve ser tratável: sem ela, cada classe do sistema precisaria receber manualmente, na mão, cada dependência transitiva de cada outra classe — uma aplicação de porte médio facilmente tem centenas de componentes, e conectar esse grafo à mão, toda vez que uma dependência nova aparece em qualquer nível, é trabalho mecânico repetitivo que ninguém quer fazer. O contêiner automatiza exatamente esse trabalho mecânico.

Python chega no mesmo lugar por um caminho mais curto, por duas razões estruturais:

**Primeira: tipagem dinâmica remove a cerimônia de declarar o contrato antes de satisfazê-lo.** Em Java, para que o contêiner saiba que `SqlUnitOfWork` "serve" onde um `UnitOfWork` é esperado, a implementação precisa declarar `implements UnitOfWork` — e o compilador verifica isso estaticamente. Python não precisa dessa declaração para o código *funcionar*: `SqlAlchemyUnitOfWork` só precisa ter os métodos `commit()`/`rollback()` que o código chamador de fato usa (o mesmo duck typing que a nota 01 já descreveu para Strategy/Factory). A checagem estática de que a implementação cumpre o contrato — quando o time quer essa garantia — vem de `Protocol` ou `abc.ABC`, discutidos adiante, sem exigir um contêiner de runtime para funcionar.

**Segunda: classes e funções são valores de primeira classe.** Em Python, `SqlAlchemyUnitOfWork` — a classe em si, não uma instância — pode ser guardada numa variável, passada como argumento, devolvida de uma função, exatamente como qualquer outro objeto. "Decidir qual implementação usar" não exige reflexão nenhuma — é só escrever `criar_uow = SqlAlchemyUnitOfWork` (ou uma função que retorna a instância certa) num único lugar do código. Não existe "descoberta automática" porque não existe necessidade de descobrir nada: a decisão já está escrita, explicitamente, como uma linha de código Python comum.

> [!tip] O nome certo para o que o `main.py` faz: composition root
> O termo vem da comunidade de DI em .NET (Mark Seemann popularizou), mas descreve exatamente o padrão do exemplo de abertura: um único lugar na aplicação — tipicamente o ponto de entrada — onde o grafo de objetos concretos é montado, e de onde as abstrações fluem para o resto do código já resolvidas. Fora do composition root, nenhuma parte do sistema deveria conter a palavra `SqlAlchemy` (nem `import sqlalchemy`) fora da própria camada de infraestrutura — é a mesma disciplina que garante que o domínio ([[02 - Domain modeling — separando a lógica de negócio do framework|nota 02]]) e a Service Layer (nota 06, a seguir) permaneçam Python puro.

## Composition root de verdade: `main.py` decidindo o grafo inteiro

O exemplo de abertura mostrou `criar_uow` sozinho — mas o composition root de uma API real decide um grafo inteiro, não uma peça isolada. Retomando os padrões já formalizados neste galho: `AbstractUnitOfWork` ([[04 - Unit of Work — formalizando o padrão que já existia|nota 04]]) agrupa um ou mais Repositories ([[03 - Repository pattern — abstraindo a persistência|nota 03]]) numa transação atômica, e a Service Layer (nota 06 deste galho, que orquestra os casos de uso) depende só da abstração:

```python
# adapters/uow_sqlalchemy.py — a única implementação concreta conhecida pelo composition root
from sqlalchemy.orm import sessionmaker

from domain.uow import AbstractUnitOfWork
from adapters.repository_sqlalchemy import SqlAlchemyTarefaRepository


class SqlAlchemyUnitOfWork(AbstractUnitOfWork):
    def __init__(self, session_factory: sessionmaker):
        self._session_factory = session_factory

    def __enter__(self) -> "SqlAlchemyUnitOfWork":
        self.session = self._session_factory()
        self.tarefas = SqlAlchemyTarefaRepository(self.session)
        return self

    def __exit__(self, *args) -> None:
        super().__exit__(*args)
        self.session.close()

    def commit(self) -> None:
        self.session.commit()

    def rollback(self) -> None:
        self.session.rollback()
```

```python
# services/tarefas.py — Service Layer, depende só da abstração
from domain.uow import AbstractUnitOfWork


def concluir_tarefa(uow: AbstractUnitOfWork, tarefa_id: int, usuario_id: int) -> None:
    with uow:
        tarefa = uow.tarefas.get(tarefa_id)
        if tarefa is None or tarefa.usuario_id != usuario_id:
            raise TarefaNaoEncontrada(tarefa_id)
        tarefa.concluir()
        uow.tarefas.add(tarefa)
        uow.commit()
```

Repare: `concluir_tarefa` recebe um `uow: AbstractUnitOfWork` — nunca importa `SqlAlchemyUnitOfWork`, nunca importa `sqlalchemy`. Quem decide **qual** `AbstractUnitOfWork` de fato chega até essa função é o composition root, conectando as peças:

```python
# main.py — composition root completo
from fastapi import FastAPI, Depends
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from adapters.uow_sqlalchemy import SqlAlchemyUnitOfWork
from domain.uow import AbstractUnitOfWork
from services import tarefas as service

DATABASE_URL = "postgresql://user:senha@localhost/tarefas"
engine = create_engine(DATABASE_URL, pool_size=20)
SessionFactory = sessionmaker(bind=engine)


def get_uow() -> AbstractUnitOfWork:
    """Dependência do FastAPI (mecanismo) que devolve a UoW concreta
    decidida aqui (princípio) — a fronteira entre as duas notas."""
    return SqlAlchemyUnitOfWork(session_factory=SessionFactory)


app = FastAPI()


@app.post("/tarefas/{tarefa_id}/concluir", status_code=204)
def concluir_tarefa_endpoint(
    tarefa_id: int,
    usuario_id: int,
    uow: AbstractUnitOfWork = Depends(get_uow),
):
    service.concluir_tarefa(uow, tarefa_id, usuario_id)
```

Este é o ponto exato onde a fronteira entre esta nota e o Galho 10 fica visível no código: `Depends(get_uow)` é o **mecanismo** (o FastAPI chama `get_uow()` a cada requisição, exatamente como a [[03-Dominios/Tecnologia/Python/Web e APIs REST/04 - Injeção de dependência no FastAPI — Depends|nota 04 do Galho 10]] já explicou em profundidade — sub-dependências, `yield`, escopo por requisição, `dependency_overrides`). O que `get_uow()` **faz por dentro** — instanciar `SqlAlchemyUnitOfWork` especificamente, e não qualquer outra implementação — é a decisão de composição, o princípio que esta nota desenvolve. `Depends()` não decide *qual* implementação; ele só garante que a função que decide seja chamada no momento certo, com o ciclo de vida certo.

```mermaid
flowchart TB
    subgraph Root["Composition root — main.py"]
        DECISAO["get_uow()\ndecide: SqlAlchemyUnitOfWork"]
    end

    subgraph Mecanismo["Mecanismo de resolução — Depends() do FastAPI"]
        DEP["Depends(get_uow)\nchama get_uow() a cada requisição"]
    end

    subgraph Consumo["Código que só conhece a abstração"]
        HANDLER["concluir_tarefa_endpoint(uow)"]
        SVC["service.concluir_tarefa(uow, ...)"]
        UOW_ABS["AbstractUnitOfWork\n(interface)"]
    end

    subgraph Impl["Implementações concretas — decididas só no root"]
        SQL["SqlAlchemyUnitOfWork\n(produção)"]
        FAKE["FakeUnitOfWork\n(testes)"]
    end

    DECISAO -->|"instancia"| SQL
    DEP -->|"invoca"| DECISAO
    DEP -->|"injeta"| HANDLER
    HANDLER --> SVC
    SVC -->|"depende só de"| UOW_ABS
    UOW_ABS -.->|"implementada por"| SQL
    UOW_ABS -.->|"implementada por"| FAKE

    style DECISAO fill:#4A90D9,color:#fff
    style UOW_ABS fill:#4A90D9,color:#fff
    style SQL fill:#2d5016,color:#fff
    style FAKE fill:#F5A623,color:#000
```

Trocar a implementação em teste é exatamente o mesmo mecanismo de `dependency_overrides` que o Galho 10 já ensinou — a diferença é que aqui a substituição troca a **decisão de composição**, não só um valor de query param:

```python
# tests/test_concluir_tarefa_api.py
from fastapi.testclient import TestClient

from main import app, get_uow
from tests.fakes import FakeUnitOfWork


def get_uow_fake():
    return FakeUnitOfWork()


app.dependency_overrides[get_uow] = get_uow_fake
client = TestClient(app)


def test_concluir_tarefa_retorna_204():
    resposta = client.post("/tarefas/1/concluir", params={"usuario_id": 42})
    assert resposta.status_code == 204
```

Nenhum banco sobe, nenhuma conexão real é aberta — `get_uow_fake` é outra função de composição, só que decidindo `FakeUnitOfWork` em vez de `SqlAlchemyUnitOfWork`. O princípio (quem decide a implementação) e o mecanismo (`Depends()`/`dependency_overrides`) continuam trabalhando juntos, cada um no seu papel.

> [!warning] Composição manual não é "sem injeção de dependência"
> É comum quem vem de um ecossistema com container assumir que "sem container" significa "sem DI" — código antigo, acoplado, difícil de testar. É o oposto: o exemplo acima **é** injeção de dependência, no sentido mais estrito do termo (uma peça de código recebe suas dependências prontas, em vez de construí-las sozinha). O que falta não é o princípio, é a automação de um grafo de resolução — que, para a maioria das aplicações Python, nem chega a ser necessária, porque o grafo é pequeno o suficiente para ser montado à mão, num arquivo, de forma explícita e legível.

## Quando um container de DI dedicado passa a valer a pena

A composição manual do exemplo acima escala bem enquanto o grafo de dependências cabe confortavelmente numa função (ou poucas) de bootstrap — a maioria das APIs Python, mesmo de porte razoável, fica nessa faixa. Mas existe um ponto real em que montar o grafo à mão começa a doer: aplicações com **muitas** dependências, muitas delas compartilhadas entre várias partes do sistema, com ciclos de vida diferentes (um objeto que vive por toda a aplicação, outro por request, outro por operação) e configuração que muda por ambiente (dev usa um adapter fake de e-mail, produção usa SES, staging usa um mock que loga em vez de enviar).

Nesse cenário, a biblioteca [`dependency-injector`](https://pypi.org/project/dependency-injector/) — a mais adotada do ecossistema Python para esse propósito — oferece o que um contêiner de verdade oferece: declaração centralizada do grafo, providers com ciclos de vida diferentes (`Singleton`, `Factory`, `Resource`), *wiring* automático em funções marcadas com `@inject`, e configuração por ambiente sem reescrever o grafo inteiro:

```python
# containers.py — exemplo ilustrativo de dependency-injector, não desenvolvido em profundidade aqui
from dependency_injector import containers, providers


class Container(containers.DeclarativeContainer):
    config = providers.Configuration()

    session_factory = providers.Singleton(criar_session_factory, url=config.database_url)

    uow = providers.Factory(SqlAlchemyUnitOfWork, session_factory=session_factory)

    notificador = providers.Selector(
        config.ambiente,
        producao=providers.Singleton(SesNotificador),
        dev=providers.Singleton(NotificadorFake),
    )
```

Esta nota não desenvolve a mecânica de `dependency_injector` a fundo — o ponto é só nomear que a ferramenta existe, o problema que ela resolve (grafos grandes, providers com ciclos de vida distintos, seleção por ambiente declarativa) e por que ela é a **exceção**, não a norma, em Python. Ao contrário de Java, onde praticamente toda aplicação Spring de qualquer porte usa o container desde o primeiro dia, a maioria dos projetos Python nunca precisa de `dependency-injector` — a API de Tarefas deste galho, com um punhado de Repositories e uma Unit of Work, está confortavelmente na faixa "composição manual basta".

> [!question]- Isso não é regressão em relação ao rigor de Java? Como saber se o time "devia" estar usando um container e só não percebeu?
> O sinal prático, não teórico: o `main.py` começou a crescer de forma incômoda — muitas funções `criar_x` repetindo o mesmo padrão de "monta A, que depende de B, que depende de C", com duplicação real entre elas, ou a necessidade de trocar comportamento por ambiente (dev/staging/produção) virando uma cadeia de `if`/`else` espalhada pelo bootstrap. Enquanto o `main.py` continua legível numa passada de olho — o que é o caso da maioria das aplicações Python de porte pequeno a médio — a composição manual não é uma "versão simplificada, incompleta" de DI; é a forma completa e correta para aquele tamanho de problema. Trocar por um container antes desse ponto adiciona uma dependência nova, uma sintaxe própria pra aprender, e um nível de indireção que não paga aluguel — o mesmo raciocínio de custo/benefício que a [[03 - Repository pattern — abstraindo a persistência|nota 03]] já aplicou ao Repository pattern em si.

## `Protocol` como o contrato idiomático de uma dependência

O que uma dependência "precisa" para ser injetável em Python nunca é herdar de uma classe específica — é ter a forma certa. A [[03 - Repository pattern — abstraindo a persistência|nota 03 deste galho]] já escolheu `abc.ABC` para `AbstractRepository`, e a [[04 - Unit of Work — formalizando o padrão que já existia|nota 04]] segue o mesmo caminho para `AbstractUnitOfWork` — ambas são interfaces internas, com um número pequeno e conhecido de implementações, onde o time quer a garantia forte de `TypeError` na instanciação se alguém esquecer um método. Mas nem toda dependência injetada no composition root se encaixa nesse perfil, e é aqui que `typing.Protocol` (tipagem estrutural, mecânica completa na [[03-Dominios/Tecnologia/Python/OO e Data Model/06 - ABC e Protocol — tipagem estrutural|nota 06 do Galho 3]], não repetida aqui) entra como alternativa mais leve.

Considere uma dependência de notificação — enviar um e-mail ou uma mensagem quando uma tarefa é concluída. O time não controla a implementação de produção (um SDK de terceiros, como Amazon SES ou SendGrid), e provavelmente vai trocar de provedor mais de uma vez ao longo da vida do projeto:

```python
# domain/notificacoes.py — o contrato, como Protocol
from typing import Protocol


class Notificador(Protocol):
    def notificar(self, destinatario: str, mensagem: str) -> None: ...
```

```python
# adapters/notificador_ses.py — implementação real, sem herdar de nada
import boto3


class SesNotificador:
    def __init__(self, client=None):
        self._client = client or boto3.client("ses")

    def notificar(self, destinatario: str, mensagem: str) -> None:
        self._client.send_email(Destination={"ToAddresses": [destinatario]}, ...)
```

```python
# tests/fakes.py — outra implementação, também sem herdar de nada
class NotificadorFake:
    def __init__(self):
        self.enviadas: list[tuple[str, str]] = []

    def notificar(self, destinatario: str, mensagem: str) -> None:
        self.enviadas.append((destinatario, mensagem))
```

Nem `SesNotificador` nem `NotificadorFake` herdam de `Notificador` — nenhuma delas precisa, porque `Protocol` reconhece a forma estruturalmente. E o composition root decide, entre as duas, exatamente do mesmo jeito que decidiu entre `SqlAlchemyUnitOfWork` e `FakeUnitOfWork`:

```python
def criar_notificador(ambiente: str) -> Notificador:
    if ambiente == "producao":
        return SesNotificador()
    return NotificadorFake()
```

A régua entre `ABC` e `Protocol` para uma dependência injetada, então, não é sobre DI em si — é a mesma régua que a [[03-Dominios/Tecnologia/Python/OO e Data Model/06 - ABC e Protocol — tipagem estrutural|nota 06 do Galho 3]] já estabeleceu de forma geral, aplicada aqui ao caso específico de "definir o que uma dependência injetável precisa satisfazer":

| | `abc.ABC` | `typing.Protocol` |
|---|---|---|
| Quando usar para uma dependência | Interface interna, você controla todas as implementações (`AbstractRepository`, `AbstractUnitOfWork` deste galho) | Contrato que precisa ser satisfeito por código de terceiros, ou implementações que não devem herdar de nada seu (SDK de e-mail, client HTTP externo) |
| Checagem de que a implementação está completa | Em tempo de instanciação — `TypeError` se faltar método | Só estática, via mypy/pyright (ou em runtime, fraca, com `@runtime_checkable`) |
| Precisa que a implementação declare herança? | Sim, explicitamente | Não — qualquer classe com os métodos certos serve |
| Exemplo neste galho | `AbstractRepository` (nota 03), `AbstractUnitOfWork` (nota 04) | `Notificador` (dependência que aponta pra um SDK de terceiros) |

> [!tip] A régua não muda por causa da DI
> Não existe uma regra especial de "use Protocol para dependências injetadas" — a decisão entre ABC e Protocol é sempre a mesma pergunta que a nota do Galho 3 coloca: você é dono da hierarquia, ou o contrato precisa valer para código que você não escreveu? DI é só o contexto em que essa pergunta aparece aqui; a resposta não depende de a classe estar sendo "injetada" ou não.

## Armadilhas comuns

> [!warning] Recriar o composition root dentro de cada handler "por conveniência"
> **O que acontece:** sob pressão, alguém escreve `uow = SqlAlchemyUnitOfWork(SessionFactory)` diretamente dentro de um handler, em vez de usar `Depends(get_uow)` — "é só esse endpoint, não vale a pena passar pela dependência". **Por quê:** o handler volta a importar `SqlAlchemyUnitOfWork` diretamente, quebrando a garantia central desta nota — que só o composition root conhece a implementação concreta. Esse handler específico fica impossível de testar sem banco real, e vira o primeiro lugar que quebra silenciosamente numa futura troca de implementação. **Como evitar:** todo ponto de consumo recebe a dependência já pronta (via `Depends()`, via parâmetro de função, via injeção de construtor) — nunca instancia a implementação concreta diretamente, nem "só dessa vez".

> [!warning] Confundir "sem container" com "sem disciplina de dependência"
> **O que acontece:** um time, sem um framework forçando a estrutura, deixa `import sqlalchemy` vazar para dentro de módulos de domínio e Service Layer — sem um contêiner cobrando "isso deveria vir de fora", a disciplina de manter o composition root como único ponto de decisão de implementação depende inteiramente de revisão de código. **Por quê:** um container de DI, além de resolver o grafo, também impõe uma estrutura visível (anotações, arquivos de configuração) que documenta e reforça onde as decisões de composição acontecem. Sem essa estrutura, a disciplina precisa vir de convenção — real, mas menos automática. **Como evitar:** manter o composition root fisicamente separado (um `main.py` ou um módulo `bootstrap.py` dedicado) e revisar imports em code review — se um módulo de domínio ou Service Layer importa uma biblioteca de infraestrutura (SQLAlchemy, boto3, requests), é sinal de que uma dependência que deveria ser injetada foi resolvida no lugar errado.

> [!warning] Adotar `dependency-injector` (ou outro container) antes de precisar
> **O que acontece:** o time introduz um container de DI dedicado logo no início do projeto, "porque é assim que se faz em produção", antes de o grafo de dependências ter crescido o suficiente para justificar. **Por quê:** a mesma ressalva honesta que a [[03 - Repository pattern — abstraindo a persistência|nota 03]] fez sobre Repository se aplica aqui — cada camada de indireção tem custo de aprendizado e manutenção. Um container de DI adiciona uma sintaxe própria (`providers.Factory`, `providers.Singleton`, `@inject`) que precisa ser entendida por todo mundo que tocar o bootstrap, para um problema (grafo grande, difícil de montar à mão) que talvez nunca apareça. **Como evitar:** começar com composição manual explícita no `main.py`; migrar para um container só quando o próprio `main.py` virar o problema — muitas funções `criar_x` repetidas, necessidade real de múltiplos ciclos de vida (singleton vs. por-requisição vs. por-operação) ou configuração por ambiente que a composição manual não expressa bem mais.

## Em resumo: quando composição manual basta, quando vale um container

A pergunta do desenvolvedor sênior no início desta nota — "onde está o container de DI?" — tem uma resposta que não é "vocês esqueceram", é "a resposta certa para este tamanho de problema é não ter um". A tabela final resume a decisão:

| Situação | Resposta |
|---|---|
| Grafo pequeno (uma dúzia de dependências, poucos níveis) | Composição manual no `main.py` — explícita, legível, sem dependência nova |
| Todas as implementações são controladas pelo time | `abc.ABC` para o contrato; composição manual decide qual implementação injetar |
| Contrato precisa ser satisfeito por SDK/lib de terceiros | `typing.Protocol` — sem exigir herança de código que você não controla |
| Grafo grande, muitos providers compartilhados, ciclos de vida distintos, seleção por ambiente | Considerar `dependency-injector` — é a exceção que compensa a sintaxe extra |
| Handler/Service Layer instanciando implementação concreta diretamente | Sinal de bug arquitetural, não de simplicidade — corrigir movendo a decisão para o composition root |

O princípio central não muda entre as duas colunas: **a decisão de qual implementação concreta usar sempre acontece fora do código que a consome**. O que muda é só a ferramenta que automatiza — ou não — a montagem desse grafo. Para a maioria das aplicações Python, incluindo a API de Tarefas que este galho constrói, uma função de bootstrap explícita já entrega o mesmo desacoplamento que um contêiner entregaria, sem o peso de uma dependência a mais para aprender e manter.

## Em entrevista

> "Dependency injection, as a principle, is about inverting who decides which concrete implementation to use — the consuming code depends on an abstraction, and something external, usually the application's entry point (the composition root), decides and wires the concrete implementation. In Java/Spring that's almost always paired with a container that scans the classpath and resolves the object graph via reflection at boot time. Python usually doesn't need that machinery: classes and functions are first-class objects, so wiring a dependency graph is just calling a function and passing the result as an argument — explicit composition in `main.py`, no scanning, no reflection. That's a different concern from FastAPI's `Depends()`, which is the mechanism that resolves a dependency per HTTP request — `Depends()` doesn't decide *which* implementation to use, it just calls whatever function the composition root wrote. For most applications the manual approach scales fine; a dedicated container like `dependency-injector` only earns its keep once the dependency graph gets large enough — many shared providers, different lifecycles, environment-based selection — that hand-wiring it becomes the actual problem."

> [!question]- E se o entrevistador perguntar "Python não é mais frágil sem um container garantindo o grafo"?
> A resposta honesta reconhece a troca real: um container garante, de forma centralizada e visível, que toda dependência declarada tem uma implementação registrada — sem ele, essa garantia depende de disciplina de time e revisão de código, não de uma ferramenta cobrando automaticamente. Em compensação, para grafos pequenos (a maioria das aplicações Python de porte pequeno a médio), essa "fragilidade" nunca se materializa na prática — o `main.py` inteiro cabe numa tela, e qualquer dependência faltando quebra imediatamente, de forma óbvia, na primeira chamada. A fragilidade real do container não vem de ele existir, vem de introduzi-lo cedo demais, pagando o custo de aprendizado e indireção antes de o grafo justificar.

## Fontes

- Percival, Harry; Gregory, Bob. *Architecture Patterns with Python* — capítulo "Dependency Injection (and Bootstrapping)", O'Reilly, 2020. https://www.cosmicpython.com/book/chapter_13_dependency_injection.html (consultado em 2026-07-12) — o composition root como padrão central, contraste explícito com containers de DI de outras linguagens.
- Python documentation — `typing.Protocol`: https://docs.python.org/3/library/typing.html#typing.Protocol (consultado em 2026-07-12) — mecânica de tipagem estrutural usada para o contrato `Notificador`.
- `dependency-injector` — PyPI: https://pypi.org/project/dependency-injector/ (consultado em 2026-07-12) — container de DI dedicado para Python, mencionado como exceção para grafos grandes, não desenvolvido em profundidade nesta nota.
- Seemann, Mark. *Dependency Injection Principles, Practices, and Patterns* — Manning, 2019 — origem do termo "composition root", citado nesta nota.
- [[03-Dominios/Tecnologia/Python/Web e APIs REST/04 - Injeção de dependência no FastAPI — Depends|04 — Injeção de dependência no FastAPI: Depends]] — Galho 10, mecanismo de resolução por requisição contrastado com o princípio desta nota.
- [[03-Dominios/Tecnologia/Python/OO e Data Model/06 - ABC e Protocol — tipagem estrutural|06 — ABC e Protocol: tipagem estrutural]] — Galho 3, mecânica completa de `Protocol`/`abc.ABC` referenciada sem repetição.

## Veja também

- [[01 - Por que GoF clássico é menos necessário em Python|01 — Por que GoF clássico é menos necessário em Python]] — o mesmo raciocínio (first-class functions/classes dispensam cerimônia) aplicado a Strategy/Factory; esta nota aplica o raciocínio análogo a DI.
- [[03 - Repository pattern — abstraindo a persistência|03 — Repository pattern: abstraindo a persistência]] — `AbstractRepository`, a interface que `SqlAlchemyTarefaRepository` implementa, consumida via a `SqlAlchemyUnitOfWork` composta nesta nota.
- [[04 - Unit of Work — formalizando o padrão que já existia|04 — Unit of Work: formalizando o padrão que já existia]] — `AbstractUnitOfWork`/`SqlAlchemyUnitOfWork`, o par abstração/implementação que o composition root desta nota decide qual instanciar.
- [[06 - Service Layer — orquestrando casos de uso|06 — Service Layer: orquestrando casos de uso]] — próxima nota: a camada que consome `AbstractUnitOfWork` sem nunca importar SQLAlchemy, exatamente como `concluir_tarefa` mostrou aqui.
- [[03-Dominios/Tecnologia/Python/Web e APIs REST/04 - Injeção de dependência no FastAPI — Depends|04 — Injeção de dependência no FastAPI: Depends]] — Galho 10; mecânica completa de `Depends()`, sub-dependências e `dependency_overrides`.
- [[03-Dominios/Tecnologia/Python/OO e Data Model/06 - ABC e Protocol — tipagem estrutural|06 — ABC e Protocol: tipagem estrutural]] — Galho 3; mecânica completa de tipagem nominal vs. estrutural.
- [[index|Arquitetura e Design Patterns (Galho 13)]] — MOC deste galho.

Consultado em 2026-07-12.
