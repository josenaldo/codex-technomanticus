---
title: "Testando a camada de persistência — banco de teste e rollback"
created: 2026-07-11
type: concept
fase: adepto
status: complete
publish: true
tags:
  - python
  - testes
  - pytest
  - sqlalchemy
  - persistencia
  - testcontainers
aliases:
  - "banco de teste"
  - "fixture de rollback"
  - "testcontainers-python"
  - "factory_boy"
  - "SQLite in-memory para testes"
---

# Testando a camada de persistência — banco de teste e rollback

> [!abstract] TL;DR
> Testar código que grava e lê do banco exige um banco — e a decisão de qual banco usar na suíte de testes é um trade-off explícito entre velocidade e fidelidade: `SQLite` em memória (`sqlite:///:memory:`) sobe em microssegundos mas não reproduz o comportamento do PostgreSQL de produção fielmente (a nota [[03-Dominios/Tecnologia/Python/Persistência de dados/06 - Transações e isolamento — ACID na prática, isolation levels, deadlocks de aplicação|06 do Galho 9]] já mostrou que ele mascara anomalias de isolation level), enquanto `testcontainers-python` sobe um PostgreSQL real dentro de um container Docker, pago em segundos por execução mas fiel ao banco que roda em produção. O padrão que resolve o problema mais caro — testes que sujam o banco uns para os outros — não é escolher entre os dois bancos, é uma **fixture de sessão com rollback automático**: abrir uma transação no início de cada teste, deixar o teste inteiro rodar dentro dela (inclusive commits "falsos" que a aplicação faz), e dar `rollback()` no final em vez de `commit()` — nenhuma escrita sobrevive ao teste, e o schema nunca precisa ser recriado. `factory_boy` fecha o ferramental gerando objetos de teste realistas sem repetir boilerplate de `Model(campo1=..., campo2=..., ...)` em cada teste.

## O bug que abre esta nota

A suíte de testes de um sistema de pedidos começou pequena — trinta e poucos testes, cada um recriando o schema do banco de teste do zero antes de rodar: `Base.metadata.create_all(engine)` no início, `Base.metadata.drop_all(engine)` no final, um `SQLite` em arquivo (`sqlite:///test.db`) como banco. Rodava em quatro segundos. Ninguém questionou a abordagem porque quatro segundos é imperceptível.

Oito meses depois, a suíte tem quatrocentos testes e leva um minuto e quarenta segundos para rodar. `create_all`/`drop_all` não ficaram mais lentos — o schema é o mesmo schema, criar dez tabelas leva o tempo que sempre levou. O que mudou é que **cada um dos quatrocentos testes** paga esse custo de novo, porque a fixture que recria o schema tem `scope="function"` (o [[03-Dominios/Tecnologia/Python/Testes/02 - Fixtures — escopos, yield e conftest.py|escopo default, nota 02 deste galho]]) — e ninguém tinha um jeito melhor de garantir que um teste não visse dado deixado por outro. O time tentou o remédio óbvio antes de entender o problema: mudar o escopo da fixture de banco para `session`, recriando o schema **uma vez** por execução da suíte inteira, não por teste.

A suíte ficou rápida de novo — e imediatamente instável. Um teste que cria um pedido com `status="pendente"` passa a existir no banco depois que o teste termina, porque `scope="session"` significa que ninguém dá `drop_all` até o fim de tudo. O próximo teste que faz `SELECT * FROM pedidos WHERE status = 'pendente'` esperando encontrar exatamente **um** pedido (o que ele mesmo criou) encontra dois — o seu e o órfão do teste anterior. A falha não aparece sempre: depende de quais testes rodaram antes, em que ordem, e se algum deles deixou dado "sujo" no caminho. É o mesmo tipo de bug que a nota de fixtures já descreveu para dado mutável em memória — só que agora o dado mutável não é uma lista Python, é uma linha de banco, e o "objeto compartilhado" é o arquivo `.db` inteiro.

```
$ pytest tests/test_pedidos.py -v
tests/test_pedidos.py::test_criar_pedido_pendente PASSED
tests/test_pedidos.py::test_listar_pedidos_pendentes FAILED

    def test_listar_pedidos_pendentes(sessao_db):
        pedido = Pedido(status="pendente", total=50)
        sessao_db.add(pedido)
        sessao_db.commit()
        pendentes = sessao_db.query(Pedido).filter_by(status="pendente").all()
>       assert len(pendentes) == 1
E       assert 2 == 1
```

Duas fixes ruins tentadas em sequência — recriar schema toda vez (lento) e recriar uma vez só (rápido mas sujo) — expõem a pergunta certa: como ter um banco **rápido de preparar** e **isolado por teste**, sem pagar o custo de recriar schema quatrocentas vezes? A resposta não mexe no schema — mexe na **transação**. É o assunto do resto desta nota.

## Escolhendo o banco: SQLite em memória vs PostgreSQL real

Antes da fixture de isolamento, uma decisão anterior: contra qual banco os testes rodam? A resposta não é única — depende do que o teste está validando.

### SQLite in-memory: rápido, mas infiel

`sqlite:///:memory:` cria um banco SQLite que vive inteiramente em RAM, sem tocar disco, e desaparece quando a conexão fecha. Como `Engine`/`Session` do SQLAlchemy ([[03-Dominios/Tecnologia/Python/Persistência de dados/02 - SQLAlchemy ORM — Session, mapped classes e relationships|nota 02 do Galho 9]]) tratam qualquer banco compatível com o dialeto SQL de forma uniforme, trocar de PostgreSQL para SQLite em teste é, à primeira vista, só trocar a string de conexão:

```python
from sqlalchemy import create_engine

# produção
engine = create_engine("postgresql+psycopg://user:senha@host/producao")

# teste — parece equivalente, não é
engine_teste = create_engine("sqlite:///:memory:")
```

O ganho de velocidade é real e grande: sem I/O de disco, sem handshake de rede, sem processo de banco separado para inicializar — um `Engine` de SQLite em memória está pronto em microssegundos, o que importa quando a suíte tem centenas de testes rodando em CI a cada push.

O problema é que "compatível com SQL" não é o mesmo que "se comporta igual". A nota 06 do Galho 9 já documentou a divergência mais séria para quem testa transações: **SQLite serializa toda escrita por padrão** — só uma transação de escrita por vez no banco inteiro — o que torna a maioria das anomalias de isolamento (dirty read, non-repeatable read, boa parte dos cenários de deadlock de duas transações concorrentes) **estruturalmente impossíveis de reproduzir** contra SQLite. Um teste que roda contra SQLite e não encontra bug de concorrência não prova que o código está correto sob concorrência real — só prova que SQLite não tem como expor esse tipo de bug.

> [!warning] SQLite mascara anomalias de isolation level — não é um detalhe de configuração
> A [[03-Dominios/Tecnologia/Python/Persistência de dados/06 - Transações e isolamento — ACID na prática, isolation levels, deadlocks de aplicação|nota 06 do Galho 9]] é explícita sobre isso: "Testes automatizados que usam SQLite em memória (comum em suites de teste Python por velocidade) não conseguem reproduzir dirty read, non-repeatable read nem a maioria dos cenários de deadlock de duas transações concorrentes (...) porque SQLite serializa escritas por padrão. Código que depende de um isolation level específico (`REPEATABLE READ`, `SERIALIZABLE`) precisa ser testado contra o banco real de produção (...) testar só contra SQLite dá falso sentido de segurança." Essa nota vale a releitura antes de decidir "vamos usar só SQLite nos testes" — a resposta certa quase nunca é "só SQLite", é "SQLite pra maioria, Postgres real pro que depende de comportamento de banco".

Além de isolamento, há divergências menores mas reais: SQLite tem tipagem de coluna mais frouxa (aceita inserir texto numa coluna `INTEGER` sem erro, na maioria dos casos — o chamado *type affinity*, diferente da checagem estrita de tipo do PostgreSQL), não implementa todas as *window functions*/`RETURNING` avançados da mesma forma, e não tem os mesmos comportamentos de constraint em cascata (`ON DELETE`/`ON UPDATE` em foreign keys, que o SQLite só respeita se `PRAGMA foreign_keys = ON` for explicitamente ligado por conexão — e por padrão, **não está**). Um teste que passa contra SQLite porque uma constraint de FK foi silenciosamente ignorada é um teste que mente sobre o que vai acontecer em produção.

> [!question]- Se SQLite tem tantas ressalvas, por que ele ainda é usado tão amplamente em testes Python?
> Porque a maioria dos testes de um sistema real não está testando *comportamento específico de banco* — está testando **lógica de aplicação** que só incidentalmente passa por uma query: "esse pedido foi criado com o total certo?", "essa consulta filtra pelo status certo?", "esse relacionamento `joinedload` carrega os itens do pedido?". Para essa fatia (a maior, na prática), SQLite em memória se comporta de forma suficientemente próxima ao SQL padrão para validar a lógica corretamente, e o ganho de velocidade — microssegundos contra segundos, multiplicado por centenas de testes — importa de verdade para manter uma suíte rápida o bastante para rodar a cada `git commit`. A ressalva não é "nunca use SQLite", é "saiba exatamente que fatia de comportamento você não está testando quando usa".

### PostgreSQL real via testcontainers-python: fiel, mas mais lento

`testcontainers-python` resolve o problema pelo lado oposto: em vez de aproximar-se do comportamento do Postgres com um banco diferente, ele sobe um **Postgres de verdade**, num container Docker, só para a suíte de testes — a mesma imagem que roda em produção, com o mesmo dialeto SQL, os mesmos isolation levels, as mesmas constraints de fato aplicadas.

```python
import pytest
from testcontainers.postgres import PostgresContainer
from sqlalchemy import create_engine


@pytest.fixture(scope="session")
def postgres_container():
    """Sobe um container Postgres real, uma vez pra suíte inteira."""
    with PostgresContainer("postgres:16-alpine") as container:
        yield container


@pytest.fixture(scope="session")
def engine_postgres_teste(postgres_container):
    """Engine apontando pro banco dentro do container — mesmo dialeto de produção."""
    url = postgres_container.get_connection_url()
    engine = create_engine(url)
    Base.metadata.create_all(engine)
    yield engine
    engine.dispose()
```

`PostgresContainer` é um *context manager* que cuida do ciclo de vida inteiro: baixa a imagem (se necessário), sobe o container, espera a porta responder (testcontainers implementa um *wait strategy* — não é um `sleep` fixo, é polling até a conexão aceitar), expõe a porta mapeada do host, e derruba o container ao sair do `with`. `get_connection_url()` devolve a string de conexão pronta (`postgresql://...`) já apontando para a porta certa do container. O `scope="session"` aqui é deliberado e seguro pelo mesmo raciocínio da nota de fixtures: subir um container é caro (segundos), e o `Engine`/container em si não é mutado por teste algum — o que muda teste a teste é o **dado dentro do banco**, isolado por uma fixture separada, de escopo `function` (a fixture de rollback, seção seguinte).

O custo é real: subir um container Docker, mesmo com a imagem já baixada localmente, leva de um a alguns segundos — comparado a microssegundos de SQLite em memória, é uma ordem de grandeza (ou mais) mais lento. Para uma suíte de centenas de testes, rodar **todos** contra Postgres real via testcontainers tornaria a suíte visivelmente mais pesada — por isso o padrão de mercado não é "sempre Postgres real", é reservar isso para os testes que genuinamente dependem de comportamento específico do banco.

> [!tip] A regra prática: SQLite para a maioria, Postgres real para o que depende do banco
> Testes unitários de **lógica** (regra de negócio, cálculo, validação, um relacionamento sendo carregado) rodam bem contra SQLite em memória — rápidos, e a lógica testada não depende de nuance de isolamento ou tipo estrito do PostgreSQL. Testes de **integração** que validam algo que só o Postgres real garante — uma constraint `CHECK` específica do dialeto, um comportamento de `ON CONFLICT DO UPDATE` (upsert), um cenário de deadlock ou de isolation level como os da nota 06 do Galho 9, uma *window function* — rodam contra Postgres real via `testcontainers-python`, tipicamente num subconjunto menor e marcado (`@pytest.mark.integration`, já visto na [[03-Dominios/Tecnologia/Python/Testes/03 - Parametrização e organização de suíte|nota 03 deste galho]] sobre organização com marks). A suíte inteira não precisa escolher um lado — ela pode ter as duas camadas, cada uma pagando o custo proporcional ao que está validando.

```mermaid
flowchart LR
    subgraph SQLITE["SQLite in-memory"]
        S1["sqlite:///:memory:"]
        S2["Pronto em microssegundos"]
        S3["Escritas serializadas — mascara\nanomalias de isolation level"]
        S4["Tipagem frouxa, FK não\nvalidada por padrão"]
    end

    subgraph PG["PostgreSQL real via testcontainers"]
        P1["Container Docker: postgres:16"]
        P2["Pronto em segundos"]
        P3["Mesmo dialeto, mesmo isolation\nlevel de produção"]
        P4["Constraints reais aplicadas"]
    end

    S1 --> USO1["Testes unitários de LÓGICA\n(regra de negócio, query, relacionamento)"]
    P1 --> USO2["Testes de INTEGRAÇÃO que dependem\nde comportamento específico do banco"]

    style SQLITE fill:#4A90D9,color:#fff
    style PG fill:#2d7a4a,color:#fff
    style USO1 fill:#4A90D9,color:#fff
    style USO2 fill:#2d7a4a,color:#fff
```

## O padrão central: fixture de sessão com rollback automático

Escolhido o banco (ou os dois, em camadas diferentes), sobra o problema que abriu esta nota: como garantir que um teste não vê dado deixado por outro, **sem** recriar o schema a cada teste? A resposta é não deixar nenhuma escrita sobreviver ao teste — nem mesmo os `commit()` que o próprio código sob teste faz.

O mecanismo se apoia em algo que já é verdade sobre `Session`/`Engine` (vocabulário da [[03-Dominios/Tecnologia/Python/Persistência de dados/02 - SQLAlchemy ORM — Session, mapped classes e relationships|nota 02 do Galho 9]], não reexplicado aqui): uma `Connection` pode ter uma transação aberta manualmente com `connection.begin()`, e uma `Session` pode ser **amarrada a essa connection específica** via `sessionmaker(bind=connection)` em vez de `bind=engine`. Quando a `Session` amarrada assim recebe um `session.commit()` do código sob teste, o SQLAlchemy encerra o *savepoint* interno da sessão, mas a transação externa aberta manualmente na `Connection` continua aberta — nada é escrito de fato no banco até essa transação externa também ser confirmada. Se em vez de confirmá-la a fixture der `rollback()` nela, **todo o trabalho feito dentro do teste desaparece**, incluindo os commits que o teste (ou o código sob teste) pensava que eram definitivos.

```python
# tests/conftest.py
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


@pytest.fixture(scope="session")
def engine_teste():
    """Engine compartilhado pela suíte inteira — schema criado uma vez."""
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(engine)
    yield engine
    engine.dispose()


@pytest.fixture
def sessao_db(engine_teste):
    """Uma Session NOVA por teste, presa a uma transação externa
    que nunca é confirmada — nenhuma escrita sobrevive ao teste."""
    conexao = engine_teste.connect()
    transacao_externa = conexao.begin()

    Session = sessionmaker(bind=conexao)
    sessao = Session()

    yield sessao

    sessao.close()
    transacao_externa.rollback()   # desfaz TUDO, mesmo commits do teste
    conexao.close()
```

```python
# tests/test_pedidos.py
def test_criar_pedido_pendente(sessao_db):
    pedido = Pedido(status="pendente", total=50)
    sessao_db.add(pedido)
    sessao_db.commit()   # "commita" — mas só dentro da transação externa
    assert pedido.id is not None


def test_listar_pedidos_pendentes(sessao_db):
    # sessao_db chega aqui LIMPA — o pedido do teste anterior nunca existiu
    # de fato no banco, porque a transação externa dele levou rollback
    pedido = Pedido(status="pendente", total=30)
    sessao_db.add(pedido)
    sessao_db.commit()
    pendentes = sessao_db.query(Pedido).filter_by(status="pendente").all()
    assert len(pendentes) == 1   # sempre 1, em qualquer ordem de execução
```

A composição de escopos é a mesma regra já fixada na [[03-Dominios/Tecnologia/Python/Testes/02 - Fixtures — escopos, yield e conftest.py|nota 02 deste galho]]: `engine_teste` é caro de criar (ou, no caso do container Postgres, muito mais caro) e não é mutado em si — `scope="session"` é seguro. `sessao_db` é o dado que o teste manipula ativamente — `scope="function"` (o default) garante que cada teste começa de uma transação externa nova, sem herdar nada do teste anterior.

```mermaid
sequenceDiagram
    participant Fixture as sessao_db (fixture)
    participant Conexao as Connection
    participant Teste as função de teste
    participant Banco as banco de teste

    Note over Fixture,Banco: Com fixture de rollback
    Fixture->>Conexao: connect() + begin() (transação externa)
    Fixture->>Teste: yield sessao (bound à connection)
    Teste->>Banco: INSERT/UPDATE via sessao_db.commit()
    Note over Banco: commit do teste só fecha o savepoint interno<br/>— nada durável ainda, transação externa segue aberta
    Teste-->>Fixture: teste termina (passa ou falha)
    Fixture->>Conexao: rollback() da transação externa
    Note over Banco: TUDO desfeito — próximo teste vê banco limpo

    Note over Fixture,Banco: Sem isolamento (schema recriado 1x, scope=session)
    participant Teste2 as test_A
    participant Teste3 as test_B
    Teste2->>Banco: INSERT + commit() de verdade
    Note over Banco: dado do test_A permanece
    Teste3->>Banco: SELECT esperando só o próprio dado
    Banco-->>Teste3: retorna dado do test_A também — FALHA dependente de ordem
```

> [!question]- Por que não simplesmente dar `DELETE FROM` em cada tabela ao final de cada teste, em vez desse esquema de transação externa?
> Funcionaria, mas é mais lento e mais frágil de manter. `DELETE FROM` em cada tabela precisa conhecer **todas** as tabelas do schema (e a ordem certa, respeitando foreign keys, ou desabilitar constraints temporariamente) — toda vez que uma tabela nova é adicionada ao schema, o código de limpeza precisa lembrar de incluí-la, e esquecer uma tabela produz exatamente o mesmo tipo de vazamento silencioso que a fixture de rollback elimina por construção. `rollback()` de uma transação, por outro lado, desfaz **qualquer** escrita feita dentro dela, em qualquer tabela, sem precisar saber quais tabelas existem — é uma garantia estrutural do próprio banco (parte do "A" e do "D" de ACID, [[03-Dominios/Tecnologia/Python/Persistência de dados/06 - Transações e isolamento — ACID na prática, isolation levels, deadlocks de aplicação|nota 06 do Galho 9]]), não uma lista de limpeza que alguém precisa manter atualizada.

> [!tip] O truque central em uma frase
> O código sob teste **acha** que está commitando de verdade (`session.commit()` roda sem erro, o objeto ganha `id`, tudo se comporta como produção) — mas a fixture já abriu uma transação externa antes disso, e só ela decide se o trabalho sobrevive; como a fixture sempre dá `rollback()` no teardown, a resposta é sempre "não sobrevive". O teste testa o comportamento real de commit sem pagar o preço de um commit real.

### Um detalhe que quebra o padrão: `session.commit()` dentro de `SAVEPOINT`

Uma armadilha comum ao implementar esse padrão pela primeira vez: se o código sob teste chama `session.commit()` mais de uma vez, e a `Session` não está configurada para usar um `SAVEPOINT` aninhado dentro da transação externa, o SQLAlchemy pode tentar de fato confirmar (ou até fechar) a transação externa antes da hora, quebrando o isolamento. A correção padrão é registrar um evento que reabre um `SAVEPOINT` automaticamente sempre que a sessão de teste encerra um:

```python
from sqlalchemy import event


@pytest.fixture
def sessao_db(engine_teste):
    conexao = engine_teste.connect()
    transacao_externa = conexao.begin()

    Session = sessionmaker(bind=conexao)
    sessao = Session()

    # garante que múltiplos commit()/rollback() do código sob teste
    # não escapam da transação externa
    sessao.begin_nested()

    @event.listens_for(sessao, "after_transaction_end")
    def reabrir_savepoint(session, transacao):
        if transacao.nested and not transacao._parent.nested:
            session.begin_nested()

    yield sessao

    sessao.close()
    transacao_externa.rollback()
    conexao.close()
```

Esse detalhe não é essencial de entender linha a linha para usar o padrão — o que importa reter é o motivo dele existir: `commit()` chamado várias vezes dentro do mesmo teste é comum (a aplicação real faz isso o tempo todo), e a fixture de rollback precisa continuar segurando a transação externa aberta mesmo assim, ou o isolamento entre testes quebra silenciosamente na primeira vez que um teste exercitar um fluxo com múltiplos commits.

## `factory_boy`: dados de teste sem boilerplate repetido

Com o banco isolado resolvido, sobra um problema menor mas real: cada teste que precisa de um `Pedido`, um `Usuario`, um `Produto` de exemplo acaba reescrevendo `Model(campo1=valor1, campo2=valor2, ...)` com valores mais ou menos arbitrários — e conforme o modelo ganha campos obrigatórios novos, cada um desses construtores espalhados pela suíte precisa ser atualizado.

`factory_boy` é o padrão de mercado para resolver isso: uma **factory** declara, uma vez, como montar um objeto de teste "razoável" por padrão, com todos os campos preenchidos, e cada teste só sobrescreve o que é relevante para aquele caso específico.

```python
import factory
from factory.alchemy import SQLAlchemyModelFactory


class PedidoFactory(SQLAlchemyModelFactory):
    class Meta:
        model = Pedido
        sqlalchemy_session_persistence = "commit"

    status = "pendente"
    total = factory.Faker("pydecimal", left_digits=3, right_digits=2, positive=True)
    criado_em = factory.Faker("date_time_this_year")


def test_pedido_confirmado_muda_status(sessao_db):
    PedidoFactory._meta.sqlalchemy_session = sessao_db
    pedido = PedidoFactory(status="confirmado")   # só sobrescreve o que importa
    assert pedido.total > 0   # os demais campos vieram preenchidos pela factory
```

`factory.Faker` gera dados plausíveis (valores decimais, datas, nomes, e-mails) em vez de constantes fixas repetidas em todo teste — o que também ajuda a expor bugs que só aparecem com dados variados (um teste que sempre usa `total=50` nunca vai descobrir um bug de arredondamento que só aparece com `total=33.33`). `SQLAlchemyModelFactory` integra a factory com a `Session` de teste, então os objetos criados já entram no banco de teste isolado da fixture de rollback — a factory não substitui o padrão de isolamento desta nota, ela só reduz o boilerplate de criar dados dentro dele. Este galho não aprofunda mais `factory_boy` além deste exemplo — o ferramental completo (`SubFactory` para relacionamentos, `Sequence` para valores únicos, estratégias `build`/`create`) fica fora do escopo aqui.

## Acelerando testcontainers no dia a dia

Um segundo custo, menos óbvio que o de subir o container uma vez por sessão, aparece no ciclo de desenvolvimento local: se cada execução de `pytest` sobe um container novo e o Docker precisa recriar tudo do zero a cada vez que o desenvolvedor roda a suíte, o feedback loop fica pesado mesmo com `scope="session"` dentro de uma única execução. `testcontainers-python` tem um mecanismo de **reuse** para esse caso — `PostgresContainer(...).with_kwargs(reuse=True)` (ou a variável de ambiente `TESTCONTAINERS_RYUK_DISABLED` combinada com um container nomeado) mantém o container vivo entre execuções distintas do `pytest`, em vez de derrubá-lo ao final de cada rodada. O trade-off é operacional: um container "reusado" pode acumular dado de execuções anteriores se a fixture de rollback tiver algum buraco, então esse modo é mais indicado para o loop rápido de um desenvolvedor rodando testes repetidamente na própria máquina do que para CI, onde um ambiente limpo a cada execução é justamente a garantia que se quer.

```python
from testcontainers.postgres import PostgresContainer

container = PostgresContainer("postgres:16-alpine").with_kwargs(reuse=True)
```

> [!tip] CI e máquina local podem usar estratégias diferentes
> Não há obrigação de usar o mesmo comportamento de container nos dois ambientes. Em CI, um container novo por execução (sem `reuse`) é o padrão certo — o ambiente inteiro é descartável e a garantia de estado limpo vale mais que os segundos economizados. Na máquina do desenvolvedor, `reuse=True` reduz o atrito de rodar a suíte de integração repetidamente durante um ciclo de desenvolvimento — desde que a fixture de rollback continue fazendo o trabalho pesado de isolar dado entre execuções de teste dentro da mesma sessão do container.

## Casos práticos

### Cenário 1: suíte de unit tests migrando de fixture manual para SQLite em memória

Um serviço que antes só tinha testes de lógica pura (sem tocar banco, usando objetos Python simples no lugar de `Model`) começa a crescer regras que dependem de consulta — "não permitir dois pedidos ativos para o mesmo cliente", por exemplo, que só pode ser validada consultando o banco. A migração natural não é "trocar tudo para Postgres real" — é introduzir a dupla `engine_teste`/`sessao_db` desta nota, com SQLite em memória, exatamente para esse tipo de regra:

```python
def test_nao_permite_dois_pedidos_ativos_mesmo_cliente(sessao_db):
    cliente = ClienteFactory()
    PedidoFactory(cliente=cliente, status="ativo")

    with pytest.raises(RegraDeNegocioError):
        criar_pedido(sessao_db, cliente=cliente, status="ativo")
```

`RegraDeNegocioError` é levantado pela função de aplicação `criar_pedido`, que internamente faz a consulta de checagem — o teste valida o comportamento de ponta a ponta (consulta real + regra real) sem precisar de Postgres, porque nada aqui depende de isolation level ou de uma constraint específica do dialeto Postgres.

### Cenário 2: um bug de deadlock que só aparecia em produção

Um time reportou deadlocks intermitentes em produção num fluxo de atualização de estoque com duas operações concorrentes atualizando a mesma linha em ordens diferentes — o cenário estrutural que a [[03-Dominios/Tecnologia/Python/Persistência de dados/06 - Transações e isolamento — ACID na prática, isolation levels, deadlocks de aplicação|nota 06 do Galho 9]] já descreveu em detalhe. A suíte existente, toda contra SQLite em memória, nunca tinha capturado o bug — coerente com a ressalva desta nota: SQLite serializa escritas, um deadlock de duas transações concorrentes não tem como acontecer nele. Reproduzir o bug em teste automatizado exigiu um teste novo, marcado `@pytest.mark.integration`, rodando contra Postgres real via `testcontainers-python`, com duas `Session`s SQLAlchemy diferentes (não a mesma `sessao_db` da fixture de rollback — o teste precisa de duas conexões concorrentes de verdade) disparando as duas atualizações em threads separadas e checando que o banco resolve o conflito (uma das transações recebe erro de deadlock, a outra segue). Esse teste nunca teria sido possível só com SQLite — é o caso concreto que justifica manter as duas camadas de banco de teste na mesma suíte, em vez de escolher só uma.

## Armadilhas comuns

> [!warning] Misturar `scope="session"` no schema com dado real não limpo entre testes
> **O que acontece:** o time troca a fixture de banco para `scope="session"` só para ganhar velocidade (evitar recriar schema), sem adicionar a camada de transação externa com rollback — exatamente o bug de abertura desta nota. **Por quê:** `scope="session"` no `Engine`/schema é seguro e correto; o erro é achar que isso também resolve isolamento de **dado**. São dois problemas diferentes: schema (estrutura das tabelas, caro, criado uma vez) e dado (linhas dentro das tabelas, precisa ser limpo a cada teste). **Como evitar:** manter o `Engine`/schema em `scope="session"`, mas colocar a `Session` de cada teste dentro de uma transação externa com `scope="function"` e rollback garantido no teardown — os dois escopos coexistem, cada um resolvendo o problema que lhe cabe.

> [!warning] Testar isolation level de produção só contra a fixture de rollback em SQLite
> **O que acontece:** a fixture de rollback desta nota roda perfeitamente contra SQLite em memória — o que ela garante é isolamento **entre testes**, não fidelidade ao comportamento de concorrência do PostgreSQL. Um time pode concluir, erroneamente, que "os testes de transação passam" significa "o código está correto sob isolation level real". **Por quê:** a fixture de rollback resolve um problema (vazamento de dado entre testes), a ressalva da nota 06 do Galho 9 é sobre outro problema completamente diferente (SQLite não reproduz anomalias de concorrência real). Os dois usam a palavra "transação", mas não se substituem. **Como evitar:** usar a fixture de rollback (SQLite ou Postgres, tanto faz) para isolamento entre testes; usar Postgres real via `testcontainers-python`, especificamente, para qualquer teste que valide comportamento sob concorrência ou isolation level — os dois objetivos coexistem na mesma suíte, em camadas diferentes.

> [!warning] Container do testcontainers subindo do zero a cada teste, não a cada suíte
> **O que acontece:** a fixture do `PostgresContainer` é declarada com `scope="function"` por engano (ou copiada de um exemplo sem prestar atenção ao escopo), e a suíte passa a subir um container Docker inteiro a cada teste individual — a suíte de integração que devia levar segundos passa a levar minutos. **Por quê:** subir um container tem custo fixo de segundos (pull de imagem se necessário, start do processo, wait strategy até a porta responder) — pagar esse custo uma vez por teste, em vez de uma vez para a suíte inteira, multiplica o tempo total pelo número de testes. **Como evitar:** `scope="session"` para a fixture do container e do `Engine` construído sobre ele; a fixture de `Session`/transação externa (que de fato precisa isolar teste a teste) continua com `scope="function"`, construída em cima do `Engine` compartilhado — o mesmo padrão de composição já visto para `engine_teste`/`sessao_db`.

## Em entrevista

- **"Como você isola testes que tocam banco de dados uns dos outros?"** Uma fixture de sessão que abre uma transação externa manualmente antes do teste rodar, amarra a `Session` a essa transação, deixa o teste inteiro (inclusive os `commit()` que o código sob teste faz) rodar dentro dela, e dá `rollback()` no teardown — nada escrito pelo teste sobrevive, sem precisar recriar o schema a cada execução.
- **"SQLite ou Postgres real nos testes?"** Depende do que está sendo testado: lógica de aplicação roda bem e rápido contra SQLite em memória; qualquer coisa que dependa de comportamento específico do PostgreSQL (isolation level, constraint particular, window function) precisa de Postgres real, tipicamente via `testcontainers-python` num container Docker isolado para a suíte.
- **"Por que SQLite não é confiável para testar isolation level?"** Porque SQLite serializa toda escrita por padrão — só uma transação de escrita por vez no banco inteiro — o que torna a maioria das anomalias de concorrência (dirty read, deadlock de duas transações) estruturalmente impossíveis de reproduzir nele, dando falso sentido de segurança a um teste que "passa".
- **"Como você gera dados de teste sem repetir boilerplate?"** `factory_boy` — uma factory declara uma vez como montar um objeto de teste válido com valores padrão plausíveis, e cada teste sobrescreve só os campos relevantes para o caso específico, em vez de reescrever o construtor completo em todo teste.

## How to explain in English

> Testing a persistence layer requires a real database to test against, and that raises two independent decisions people often conflate. The first is which database: SQLite in-memory (`sqlite:///:memory:`) is ready in microseconds but serializes all writes by default, which masks most isolation-level anomalies (dirty reads, deadlocks between concurrent transactions) — fine for testing application logic, unsafe for validating anything that depends on real concurrency behavior. `testcontainers-python` solves that by spinning up an actual PostgreSQL container just for the test run — slower to start (seconds, not microseconds) but faithful to production behavior, reserved for integration tests that specifically depend on database-specific guarantees. The second decision is isolation between tests, solved by a completely different mechanism: a session fixture that opens an external transaction before the test runs, binds the test's `Session` to that transaction, lets the whole test run inside it — including any `commit()` calls the code under test makes — and rolls the external transaction back in teardown. Nothing the test wrote ever becomes durable, so the next test always starts from a clean database, without needing to recreate the schema every time. `factory_boy` rounds out the toolkit by letting a factory declare sensible defaults for a test object once, so each test only overrides the fields it actually cares about instead of repeating full constructor calls everywhere.

| PT | EN |
|----|----|
| banco de teste isolado | isolated test database |
| transação externa | external transaction |
| fixture de rollback | rollback fixture |
| commit "falso" (dentro da transação externa) | fake commit |
| mascarar anomalias de isolamento | mask isolation anomalies |
| container descartável | disposable container |
| dado de teste realista | realistic test data |

## Síntese

Testar a camada de persistência tem duas decisões independentes que costumam ser confundidas: **qual banco** usar (SQLite in-memory, rápido mas incapaz de reproduzir certas anomalias de concorrência — ou PostgreSQL real via `testcontainers-python`, fiel mas mais pesado, reservado para o que genuinamente depende de comportamento do banco) e **como isolar** um teste do outro (uma fixture de sessão que abre transação externa antes do teste e dá rollback depois, garantindo que nenhuma escrita — nem os commits que o código sob teste faz — sobrevive além daquele teste). A primeira decisão é sobre fidelidade; a segunda é sobre correção da suíte em si, e vale para qualquer banco escolhido. Resolver as duas juntas é o que torna uma suíte de testes de persistência rápida o bastante para rodar a cada commit e confiável o bastante para não mentir sobre bugs de concorrência — e `factory_boy` fecha o ferramental tirando o boilerplate repetitivo de criar dados de teste do caminho.

O próximo passo natural do galho sai da camada de dados e volta para medir a suíte como um todo: quanto do código está de fato sendo exercitado pelos testes escritos até aqui, e — mais importante — o que essa métrica não consegue enxergar.

## Veja também

- [[03-Dominios/Tecnologia/Python/Testes/02 - Fixtures — escopos, yield e conftest.py|02 — Fixtures: escopos, yield e conftest.py]] — o mecanismo de composição de fixtures (`engine_teste` caro e compartilhado, `sessao_db` isolada por teste) reaproveitado nesta nota vem direto de lá.
- [[03-Dominios/Tecnologia/Python/Testes/03 - Parametrização e organização de suíte|03 — Parametrização e organização de suíte]] — os marks (`@pytest.mark.integration`) usados para separar testes contra SQLite de testes contra Postgres real via testcontainers.
- [[03-Dominios/Tecnologia/Python/Persistência de dados/02 - SQLAlchemy ORM — Session, mapped classes e relationships|02 — SQLAlchemy ORM: Session, mapped classes e relationships]] — Galho 9; vocabulário de `Engine`/`Session`/`sessionmaker` usado sem reexplicação nesta nota.
- [[03-Dominios/Tecnologia/Python/Persistência de dados/06 - Transações e isolamento — ACID na prática, isolation levels, deadlocks de aplicação|06 — Transações e isolamento: ACID na prática, isolation levels, deadlocks de aplicação]] — Galho 9; a ressalva sobre SQLite mascarar anomalias de isolation level, referenciada e citada diretamente nesta nota.
- [[03-Dominios/Tecnologia/Python/Testes/index|Testes (Galho 12)]] — MOC deste galho.

## Fontes

- SQLAlchemy. *Joining a Session into an External Transaction (such as for test suites)*. docs.sqlalchemy.org/en/20/orm/session_transaction.html#joining-a-session-into-an-external-transaction-such-as-for-test-suites. https://docs.sqlalchemy.org/en/20/orm/session_transaction.html#joining-a-session-into-an-external-transaction-such-as-for-test-suites (acessado em 2026-07-11) — o padrão canônico de transação externa + `SAVEPOINT` + rollback usado nesta nota.
- testcontainers-python. *PostgreSQL module*. testcontainers-python.readthedocs.io/en/latest/modules/postgres/README.html. https://testcontainers-python.readthedocs.io/en/latest/modules/postgres/README.html (acessado em 2026-07-11) — `PostgresContainer`, wait strategy, `get_connection_url()`.
- factory_boy. *Orms — SQLAlchemy*. factoryboy.readthedocs.io/en/stable/orms.html#sqlalchemy. https://factoryboy.readthedocs.io/en/stable/orms.html#sqlalchemy (acessado em 2026-07-11) — `SQLAlchemyModelFactory`, `sqlalchemy_session_persistence`.
- Real Python. *Testing Third-Party APIs With Mocks* / *Effective Python Testing With Pytest*. realpython.com/pytest-python-testing/. https://realpython.com/pytest-python-testing/ (acessado em 2026-07-11) — fixtures de banco de dados e padrões de isolamento de suíte.
- SQLite Consortium. *Isolation In SQLite*. sqlite.org/isolation.html. https://sqlite.org/isolation.html (acessado em 2026-07-11) — comportamento de serialização de escritas, já citado na nota 06 do Galho 9.
- [[03-Dominios/Tecnologia/Python/Persistência de dados/06 - Transações e isolamento — ACID na prática, isolation levels, deadlocks de aplicação|Transações e isolamento — ACID na prática]] — nota do Galho 9, fonte direta da ressalva sobre SQLite citada nesta nota.

Consultado em 2026-07-11.
