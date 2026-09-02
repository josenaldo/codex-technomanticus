---
title: "Fixtures — escopos, yield e conftest.py"
created: 2026-07-11
type: concept
fase: adepto
status: complete
publish: true
tags:
  - python
  - testes
  - pytest
  - fixtures
  - conftest
aliases:
  - "@pytest.fixture"
  - "conftest.py"
  - "fixtures do pytest"
  - "escopo de fixture"
  - "session-scoped fixture"
---

# Fixtures — escopos, yield e conftest.py

> [!abstract] TL;DR
> Uma fixture é uma função decorada com `@pytest.fixture`, e um teste "recebe" o valor dela simplesmente declarando um **parâmetro com o mesmo nome** — sem import explícito, sem instanciar nada na mão. É a injeção de dependência do próprio pytest, resolvida por introspecção de assinatura, a mesma ideia estrutural do `Depends()` do FastAPI ([[03-Dominios/Tecnologia/Python/Web e APIs REST/04 - Injeção de dependência no FastAPI — Depends|Galho 10, nota 04]]) aplicada a testes em vez de requisições HTTP. A parte que separa quem só decorou a sintaxe de quem já sofreu com uma suíte instável é o **escopo**: uma fixture `function` roda a cada teste (isolada), uma fixture `session` roda uma vez pra suíte inteira (compartilhada) — e usar o escopo errado pra o tipo errado de dado é a causa mais comum de "teste que falha só às vezes, dependendo da ordem". `yield` no lugar de `return` transforma a fixture num context manager (setup antes do `yield`, teardown depois — o mesmo padrão do `Depends()` com `yield`), e `conftest.py` é o mecanismo de descoberta automática que torna uma fixture visível pra todo teste de um diretório e seus subdiretórios, sem import nenhum.

## O bug que abre esta nota

Uma suíte de testes para o catálogo de produtos de uma loja — o mesmo tipo de API que os galhos anteriores da trilha vêm construindo. Os testes precisam de uma lista de produtos disponíveis pra rodar contra; alguém escreve uma fixture pra fornecer esses dados, sem pensar muito no escopo:

```python
import pytest


@pytest.fixture(scope="session")
def produtos_disponiveis():
    """Lista de produtos usada pelos testes do catálogo."""
    return ["camiseta", "calça", "tênis"]


def test_remover_produto_esgotado(produtos_disponiveis):
    produtos_disponiveis.remove("tênis")
    assert "tênis" not in produtos_disponiveis
    assert len(produtos_disponiveis) == 2


def test_catalogo_tem_tres_produtos(produtos_disponiveis):
    assert len(produtos_disponiveis) == 3
```

Rodado isoladamente, `test_catalogo_tem_tres_produtos` passa. Rodado depois de `test_remover_produto_esgotado`, na mesma execução da suíte inteira, falha — `len(produtos_disponiveis)` é `2`, não `3`. O autor do segundo teste jura que não mudou nada; o autor do primeiro teste jura que seu teste está correto (ele *precisa* remover um produto pra testar a lógica de "produto esgotado"). Os dois estão certos sobre o próprio teste, e os dois estão errados sobre uma premissa que nenhum dos dois questionou: que `produtos_disponiveis` chega "fresco" em cada teste.

```
$ pytest tests/test_catalogo.py -v
tests/test_catalogo.py::test_remover_produto_esgotado PASSED
tests/test_catalogo.py::test_catalogo_tem_tres_produtos FAILED

    def test_catalogo_tem_tres_produtos(produtos_disponiveis):
>       assert len(produtos_disponiveis) == 3
E       assert 2 == 3

$ pytest tests/test_catalogo.py::test_catalogo_tem_tres_produtos -v
tests/test_catalogo.py::test_catalogo_tem_tres_produtos PASSED
```

O mesmo teste, mesma máquina, mesmo código — passa sozinho, falha em conjunto. É o tipo de falha mais caro de investigar porque o instinto natural é procurar o bug **dentro** do teste que falhou, quando o bug real está na fixture, numa linha que ninguém tocou hoje.

> [!bug] O que está quebrado, em uma frase
> `scope="session"` faz o pytest chamar `produtos_disponiveis()` **uma única vez** para a suíte inteira e entregar **o mesmo objeto lista** — o mesmo endereço de memória — pra todo teste que declarar esse parâmetro; como listas são mutáveis, `test_remover_produto_esgotado` não recebe "uma cópia" pra mexer, ele mexe no objeto compartilhado, e a mutação sobrevive para o próximo teste que pedir a mesma fixture, na mesma execução.

O diagnóstico, uma vez nomeado, é direto: **o escopo de uma fixture não é sobre performance sozinho — é sobre quem é dono do dado**. `session` foi escolhido aqui (provavelmente) pensando em "não recriar a lista a cada teste, é mais rápido" — um raciocínio de performance válido para dados **imutáveis** ou que ninguém modifica (uma conexão de banco, um cliente HTTP configurado, uma constante de configuração). Mas `produtos_disponiveis` é uma lista mutável que um teste legitimamente precisa alterar como parte do próprio teste — e nesse caso o escopo certo é o oposto do que foi escolhido: `function`, o default do pytest, que garante um objeto novo a cada teste. É esse mecanismo de escopo — e o `yield`/`conftest.py` que operam em cima dele — que o resto desta nota desenvolve. Retomamos e corrigimos este bug depois de explicar como escopos funcionam de verdade.

## O mecanismo central: fixture é injeção por nome de parâmetro

Antes de escopo, vale fixar o mecanismo em si, porque é ele que faz tudo o resto funcionar. Uma fixture é uma função comum decorada com `@pytest.fixture`:

```python
import pytest


@pytest.fixture
def cliente_autenticado():
    return {"id": 1, "nome": "Ana", "token": "abc123"}
```

Um teste "usa" essa fixture declarando um parâmetro com **exatamente o mesmo nome** da função decorada — nada de import, nada de instanciar a fixture manualmente, nada de chamar `cliente_autenticado()`:

```python
def test_cliente_tem_token(cliente_autenticado):
    assert cliente_autenticado["token"] == "abc123"


def test_cliente_tem_nome(cliente_autenticado):
    assert cliente_autenticado["nome"] == "Ana"
```

O que acontece, em ordem, quando o pytest roda `test_cliente_tem_token`:

1. O pytest inspeciona a **assinatura** da função `test_cliente_tem_token` — o mesmo tipo de introspecção que o `Depends()` do FastAPI usa para resolver parâmetros de rota — e encontra um parâmetro chamado `cliente_autenticado`.
2. O pytest procura, entre todas as fixtures visíveis para esse teste (definidas no próprio arquivo, ou em `conftest.py`, seção adiante), uma função decorada com `@pytest.fixture` que tenha **esse mesmo nome**.
3. Encontrada, o pytest **chama** `cliente_autenticado()` e guarda o valor de retorno.
4. Esse valor é passado como o argumento `cliente_autenticado` da função de teste, e só então o teste roda.

> [!question]- Por que não importar e chamar a fixture direto, como uma função normal?
> Funcionaria tecnicamente — `cliente_autenticado()` é uma função Python de verdade, nada impede de chamá-la à mão. O que se perde fazendo isso é exatamente o que motiva a existência do mecanismo: o pytest deixaria de controlar **quando** essa fixture roda (uma vez por teste? uma vez pra suíte inteira?), deixaria de gerenciar **teardown** (a seção de `yield` adiante), e deixaria de permitir que a mesma fixture seja **composta** por várias outras fixtures e testes diferentes sem duplicar código de setup. Chamar na mão também quebra o cache dentro do escopo: se dois testes diferentes, no mesmo `module`, pedem a mesma fixture `scope="module"`, o pytest garante que ela roda uma vez só — chamando manualmente, cada teste pagaria o custo de novo.

O nome é literal e case-sensitive: uma fixture `cliente_autenticado` só é injetada num parâmetro escrito exatamente `cliente_autenticado`. Não há resolução por tipo (como o pytest não usa type hints para casar fixture com parâmetro, ao contrário do `Depends()` do FastAPI, que resolve por assinatura completa incluindo tipos) — é resolução puramente por **nome**, o que também explica por que o pytest consegue avisar de forma clara quando uma fixture não é encontrada: `fixture 'cliente_autenticado' not found`, apontando exatamente o nome que faltou.

> [!tip] O mesmo mecanismo de injeção do FastAPI, sem o `Depends()` explícito
> No FastAPI, `Depends(minha_funcao)` é preciso porque o parâmetro poderia, em tese, ser um query param, um body, um header — o framework precisa de um sinal explícito de "isso é uma dependência, não um dado da requisição". No pytest não existe essa ambiguidade: um parâmetro de função de teste **só pode** ser uma fixture (não há "dado da requisição" concorrendo pelo mesmo espaço), então o nome sozinho já é sinal suficiente — sem precisar de um `Fixture(nome_da_fixture)` explícito na assinatura. É a mesma ideia de fundo (uma peça de código recebe algo pronto, sem construir sozinha, resolvido por introspecção de assinatura), com uma sintaxe mais enxuta porque o contexto (um teste, não uma rota HTTP) elimina a ambiguidade.

Fixtures também podem depender de outras fixtures, formando uma árvore — o mesmo princípio de composição de sub-dependências que a nota do Galho 10 já cobriu para `Depends()`:

```python
@pytest.fixture
def usuario_no_banco(sessao_db):
    usuario = Usuario(nome="Ana", email="ana@exemplo.com")
    sessao_db.add(usuario)
    sessao_db.commit()
    return usuario


def test_usuario_tem_id(usuario_no_banco):
    assert usuario_no_banco.id is not None
```

`test_usuario_tem_id` nunca menciona `sessao_db` — não precisa. `usuario_no_banco` é quem declara `sessao_db` como parâmetro, e o pytest resolve a árvore inteira sozinho: primeiro chama `sessao_db` (que é, ela mesma, outra fixture), depois passa o resultado para `usuario_no_banco`, e só então injeta o resultado final no teste.

## Escopos: quem é dono do dado, e por quanto tempo

O parâmetro `scope` de `@pytest.fixture` controla **quantas vezes** a fixture roda, e **quem compartilha** o valor produzido. É o parâmetro mais consequente da API de fixtures — errar o escopo não costuma quebrar o teste que usa a fixture diretamente, quebra um *outro* teste, mais tarde, de um jeito difícil de conectar de volta à causa (exatamente o bug de abertura desta nota).

```python
@pytest.fixture(scope="function")   # default — nem precisa escrever
def dado_a():
    ...

@pytest.fixture(scope="class")
def dado_b():
    ...

@pytest.fixture(scope="module")
def dado_c():
    ...

@pytest.fixture(scope="session")
def dado_d():
    ...
```

- **`function`** (default, implícito se `scope` não for informado): a fixture roda **uma vez por função de teste**. Cada teste recebe um objeto novo — sem exceção. É o escopo mais seguro por padrão, exatamente porque elimina qualquer possibilidade de um teste vazar estado para outro através da fixture: não há estado compartilhado para vazar, porque não há compartilhamento.
- **`class`**: a fixture roda uma vez por **classe** de teste (`class TestAlgo:`), compartilhada entre os métodos dessa classe. Usado quando vários testes de uma mesma classe legitimamente operam sobre o mesmo objeto de setup, e a classe é a unidade natural de agrupamento — menos comum em suítes pytest modernas, que tendem a preferir funções soltas a classes de teste no estilo `unittest`.
- **`module`**: a fixture roda uma vez por **arquivo** de teste (`test_algo.py`), compartilhada entre todas as funções de teste (e classes) daquele arquivo. Útil para um setup caro que todos os testes de um arquivo específico precisam, mas que não vale a pena estender a outros arquivos.
- **`session`**: a fixture roda **uma única vez**, para a execução inteira da suíte (`pytest` do início ao fim), compartilhada por **todo teste que a peça**, em qualquer arquivo. É o escopo certo para recursos caros de criar e seguros de compartilhar — o exemplo canônico é uma conexão de banco de dados de teste, ou um contêiner Docker subido via `testcontainers` uma vez só para toda a suíte.

```mermaid
flowchart TB
    classDef ok fill:#4ADE8021,stroke:#4ADE80,color:#E9ECF2
    classDef neutro fill:#1B2029,stroke:#4E5666,color:#C6CCD8
    classDef destaque fill:#FFAA0024,stroke:#FFAA00,color:#E9ECF2
    subgraph SESSION["scope=session — roda 1x pra suíte inteira"]
        S1["conexão de banco de teste"]
    end

    subgraph MODULE["scope=module — roda 1x por arquivo"]
        M1["cliente HTTP configurado\npara test_pedidos.py"]
    end

    subgraph FUNCTION["scope=function (default) — roda 1x por teste"]
        F1["dict/lista de dados de entrada\nusada e modificada pelo teste"]
    end

    S1 -.compartilhado por.-> T1["test_a"]
    S1 -.compartilhado por.-> T2["test_b"]
    S1 -.compartilhado por.-> T3["test_c (outro arquivo)"]

    M1 -.compartilhado por.-> T1
    M1 -.compartilhado por.-> T2

    F1 -->|"objeto NOVO"| T1
    F1 -->|"objeto NOVO"| T2
    F1 -->|"objeto NOVO"| T3

    class SESSION ok
    class MODULE neutro
    class FUNCTION destaque
```

A regra prática que resolve a maioria das decisões de escopo, e que resolve o bug de abertura: **pergunte se o dado é mutado pelo teste, e se essa mutação pode legitimamente afetar outro teste**. Se a resposta é "o teste vai modificar isso, e cada teste precisa começar do mesmo estado inicial" → `function` (ou, na pior hipótese, um escopo mais amplo mas com um passo de reset explícito, seção seguinte). Se a resposta é "isso é caro de criar, ninguém modifica o objeto em si (só usa ele pra fazer outra coisa, como abrir uma transação nova a cada teste em cima de uma conexão compartilhada)" → `session` ou `module` é seguro e economiza tempo de execução real.

```python
@pytest.fixture(scope="session")
def engine_db():
    """Caro de criar (conecta no banco), seguro de compartilhar
    (o objeto Engine em si não muda — quem muda é o dado DENTRO do banco,
    e isso é responsabilidade de cada teste controlar, não da fixture)."""
    from sqlalchemy import create_engine
    engine = create_engine("postgresql://user:senha@localhost/teste")
    yield engine
    engine.dispose()
```

Isso conecta diretamente com o padrão `get_db` da [[03-Dominios/Tecnologia/Python/Web e APIs REST/04 - Injeção de dependência no FastAPI — Depends|nota 04 do Galho 10]]: lá, `get_db` roda **uma vez por requisição HTTP** (não por processo — o `Engine`, criado uma vez no import do módulo, é que vive por todo o ciclo de vida da aplicação). Aqui, o paralelo é `engine_db` com `scope="session"` (equivalente ao `Engine` do FastAPI, vivendo pela suíte inteira) alimentando uma outra fixture, `sessao_db`, com `scope="function"` (equivalente ao `get_db` por requisição — uma `Session` nova a cada teste, para que testes não vazem dados de banco entre si):

```python
@pytest.fixture(scope="function")
def sessao_db(engine_db):
    """Uma Session NOVA por teste, montada em cima do Engine compartilhado.
    Garante que cada teste começa com uma transação própria."""
    from sqlalchemy.orm import sessionmaker
    conexao = engine_db.connect()
    transacao = conexao.begin()
    Session = sessionmaker(bind=conexao)
    sessao = Session()
    yield sessao
    sessao.close()
    transacao.rollback()   # desfaz qualquer escrita do teste — nada persiste
    conexao.close()
```

Esse par (`engine_db` caro e compartilhado, `sessao_db` barata e isolada por teste) é o padrão de fato para testar código que toca banco — o Galho 12 aprofunda o `rollback` automático entre testes numa nota dedicada; aqui o ponto é só nomear que **escopos diferentes compostos entre si** são a ferramenta certa para "compartilhar o caro, isolar o que muda".

> [!warning] Vazamento de estado entre testes por escopo escolhido errado
> **O que acontece:** uma fixture com escopo mais amplo que `function` (`class`, `module`, `session`) devolve um objeto **mutável** — uma lista, um dicionário, uma instância de classe com atributos que podem ser alterados — e algum teste, mesmo sem intenção maliciosa, modifica esse objeto como parte de exercitar o comportamento sob teste. Todo teste seguinte que peça a mesma fixture, na mesma execução da suíte, recebe o objeto já modificado, não o estado original. **Por quê:** escopo maior que `function` significa literalmente "a mesma referência de objeto, reaproveitada" — não é uma cópia nova, é o mesmo objeto Python na memória. Mutação em um lugar é visível em todo lugar que segura essa referência. **Como evitar:** a regra da seção anterior — dado mutável que o teste modifica como parte do próprio teste usa `scope="function"` (o default, muitas vezes nem precisa ser escrito). Quando um escopo maior é necessário por custo (ex: uma conexão), o dado mutável de fato (a transação, a `Session`) fica numa fixture **separada**, de escopo menor, construída em cima da fixture cara — como `sessao_db` acima, construída sobre `engine_db`. A falha só aparece quando a suíte roda inteira, numa ordem específica — rodar um teste isolado nunca revela o bug, o que faz esse tipo de erro escapar fácil de uma revisão apressada.

## `yield` em fixtures: setup, teste, teardown

O mesmo padrão que a nota 04 do Galho 10 já cobriu para `Depends()` — trocar `return` por `yield` transforma a fixture num context manager: o código **antes** do `yield` roda como setup, o valor do `yield` é o que é injetado no teste, e o código **depois** do `yield` roda como teardown, garantido mesmo se o teste falhar.

```python
import pytest


@pytest.fixture
def arquivo_temporario(tmp_path):
    caminho = tmp_path / "dados.json"
    caminho.write_text('{"chave": "valor"}')   # setup
    yield caminho                               # injetado no teste
    caminho.unlink(missing_ok=True)             # teardown — sempre roda
```

```python
def test_le_arquivo(arquivo_temporario):
    conteudo = arquivo_temporario.read_text()
    assert "chave" in conteudo


def test_arquivo_falha_de_proposito(arquivo_temporario):
    raise AssertionError("teste propositalmente quebrado")
```

Mesmo `test_arquivo_falha_de_proposito` levantando uma exceção antes de terminar, `caminho.unlink(missing_ok=True)` roda de qualquer forma — o pytest retoma a execução da fixture depois do `yield` independentemente do teste ter passado, falhado, ou levantado um erro inesperado. É exatamente a mesma garantia que `Depends()` com `yield` dá para o teardown de uma dependência do FastAPI mesmo quando o handler levanta uma exceção — o mecanismo por baixo é o protocolo de generator do Python nos dois casos, só que orquestrado por sistemas diferentes: o pytest orquestra em torno do ciclo de vida de **um teste**, o FastAPI orquestra em torno do ciclo de vida de **uma requisição HTTP**.

```mermaid
sequenceDiagram
    participant Pytest as pytest (runner)
    participant Fixture as fixture (yield)
    participant Teste as função de teste

    Pytest->>Fixture: chama fixture()
    Fixture->>Fixture: setup (código antes do yield)
    Fixture-->>Pytest: yield valor
    Pytest->>Teste: chama teste(valor)
    alt teste passa
        Teste-->>Pytest: assert OK
    else teste falha
        Teste-->>Pytest: AssertionError / exceção
    end
    Pytest->>Fixture: retoma execução após o yield
    Fixture->>Fixture: teardown (código depois do yield)
    Note over Pytest,Fixture: Mesmo padrão do Depends() com yield<br/>(Galho 10, nota 04) — setup/valor/teardown —<br/>aplicado ao ciclo de UM TESTE, não de uma requisição HTTP
```

> [!question]- Por que não usar sempre `try/finally` dentro da própria fixture, mesmo sem `yield`?
> `yield` **é** o `try/finally` — só que expresso de um jeito que o pytest entende e gerencia automaticamente. Sem `yield`, uma fixture com `return` não tem como executar código depois que o teste terminou; ela simplesmente devolve um valor e encerra ali. `try/finally` sozinho, fora do padrão de `yield`, não tem onde "pausar" para deixar o teste rodar no meio — é justamente o protocolo de generator (a palavra-chave `yield`) que permite a fixture suspender sua própria execução, devolver o controle para o pytest rodar o teste inteiro, e só então retomar de onde parou para fazer o cleanup. Na prática, o padrão idiomático combina os dois: `yield` para o ponto de pausa, `try/finally` dentro da fixture para garantir que o teardown roda mesmo se o próprio setup (antes do `yield`) já tiver criado recursos parciais que precisam de limpeza condicional.

```python
@pytest.fixture
def conexao_de_rede():
    conexao = abrir_conexao()
    try:
        yield conexao
    finally:
        conexao.fechar()   # roda mesmo se o teste levantar exceção
```

> [!tip] Fixtures com `yield` e escopo amplo: setup uma vez, teardown uma vez
> O teardown de uma fixture `scope="session"` só roda **depois do último teste da suíte inteira** — não depois de cada teste individual que a usou. Isso é coerente com o resto do mecanismo (setup também roda uma vez só, no primeiro teste que pedir a fixture), mas vale nomear explicitamente porque é fácil assumir, por hábito com `function`, que teardown acontece "depois de cada teste que usa essa fixture" — não é o caso para escopos maiores.

## `conftest.py`: fixtures que aparecem sem import

Até aqui, toda fixture dos exemplos estava definida no mesmo arquivo do teste que a usa. Na prática, fixtures reaproveitadas por **vários** arquivos de teste — uma conexão de banco de teste, um cliente HTTP autenticado, dados de exemplo comuns — vivem num arquivo especial chamado `conftest.py`, que o pytest trata de um jeito diferente de qualquer outro arquivo Python do projeto.

```
projeto/
├── src/
│   └── loja/
│       └── ...
└── tests/
    ├── conftest.py              # fixtures visíveis para TODO teste em tests/
    ├── test_catalogo.py
    ├── test_pedidos.py
    └── integracao/
        ├── conftest.py          # fixtures visíveis SÓ para tests/integracao/
        └── test_checkout.py
```

```python
# tests/conftest.py
import pytest


@pytest.fixture(scope="session")
def engine_db():
    from sqlalchemy import create_engine
    engine = create_engine("postgresql://user:senha@localhost/teste")
    yield engine
    engine.dispose()


@pytest.fixture(scope="function")
def sessao_db(engine_db):
    ...  # mesmo código já mostrado
```

```python
# tests/test_pedidos.py — NENHUM import de conftest.py
def test_criar_pedido(sessao_db):
    pedido = Pedido(total=100)
    sessao_db.add(pedido)
    sessao_db.commit()
    assert pedido.id is not None
```

`test_pedidos.py` usa `sessao_db` sem nenhum `from conftest import sessao_db`, sem nenhuma linha de import ligando os dois arquivos. O pytest descobre `conftest.py` automaticamente durante a coleta de testes (a fase de discovery já introduzida na nota 01 deste galho) e disponibiliza toda fixture ali definida para **qualquer teste no mesmo diretório, e em qualquer subdiretório** — recursivamente. Um `conftest.py` dentro de `tests/integracao/` adiciona fixtures que só existem **naquele** subdiretório (e nos que estiverem abaixo dele), sem afetar `test_catalogo.py` ou `test_pedidos.py` na raiz de `tests/`.

```mermaid
flowchart TB
    classDef neutro fill:#1B2029,stroke:#4E5666,color:#C6CCD8
    C1["tests/conftest.py\n(engine_db, sessao_db)"]
    C2["tests/integracao/conftest.py\n(cliente_http_real)"]

    T1["test_catalogo.py\nvê: engine_db, sessao_db"]
    T2["test_pedidos.py\nvê: engine_db, sessao_db"]
    T3["integracao/test_checkout.py\nvê: engine_db, sessao_db, cliente_http_real"]

    C1 -->|"visível para todo tests/"| T1
    C1 -->|"visível para todo tests/"| T2
    C1 -->|"herdado + somado ao local"| C2
    C2 -->|"visível só em integracao/"| T3

    class C1 neutro
    class C2 neutro
```

Isso é o que torna `conftest.py` genuinamente poderoso — uma fixture de setup caro, escrita uma vez, fica automaticamente acessível a cada arquivo de teste novo que alguém criar naquele diretório, sem nenhuma cerimônia de import. É também exatamente o motivo pelo qual `conftest.py` confunde quem chega numa suíte pela primeira vez: abrir `test_pedidos.py` e ver `sessao_db` como parâmetro de um teste, sem NENHUMA pista visual de onde `sessao_db` vem (nenhum import no topo do arquivo), é desorientador até alguém explicar que existe um arquivo especial, com nome mágico, que o pytest varre sozinho.

> [!question]- Por que o nome tem que ser exatamente `conftest.py`?
> É uma convenção fixa que o pytest reconhece internamente durante a fase de coleta — o mesmo tipo de "nome mágico" que `test_*.py`/`*_test.py` já é para arquivos de teste (nota 01 deste galho). Renomear para `fixtures.py` ou `common.py` faz o pytest ignorar o arquivo completamente para fins de descoberta automática de fixtures — nesse caso, as fixtures só ficariam disponíveis via import explícito, perdendo exatamente a propriedade que torna `conftest.py` diferente de um módulo Python comum.

> [!warning] `conftest.py` na raiz errada esconde ou duplica fixtures sem aviso
> **O que acontece:** um projeto acumula mais de um `conftest.py` em níveis diferentes da árvore de diretórios de teste, cada um redefinindo uma fixture com o mesmo nome (por exemplo, dois `conftest.py` diferentes, cada um com sua própria versão de `sessao_db`, com comportamento sutilmente diferente). O pytest não aponta um erro — ele silenciosamente usa a definição **mais próxima** do teste na árvore de diretórios (a fixture local do `conftest.py` mais aninhado "sobrescreve" a de um `conftest.py` mais acima), o que é uma feature intencional (permitir override por subdiretório) mas também uma fonte real de confusão quando ninguém lembra que a sobrescrita existe. **Por quê:** é o mesmo princípio de escopo léxico que qualquer sistema hierárquico de configuração usa — o mais específico vence — mas sem nenhum aviso explícito no terminal de que uma fixture está sendo sobrescrita, ao contrário de, por exemplo, um linter reclamando de variável redefinida. **Como evitar:** manter fixtures compartilhadas amplamente em **um** `conftest.py` na raiz de `tests/`, e usar `conftest.py` de subdiretório só para fixtures genuinamente locais àquele subconjunto de testes (como `cliente_http_real`, usado só pelos testes de integração) — não para redefinir, com nome igual, uma fixture que já existe mais acima na árvore.

## Corrigindo o bug de abertura

Voltando ao catálogo de produtos: a correção direta troca `scope="session"` por `scope="function"` (o default — a linha `scope=` nem precisa mais existir):

```python
import pytest


@pytest.fixture
def produtos_disponiveis():
    """Uma lista NOVA a cada teste — nenhum teste vê mutação de outro."""
    return ["camiseta", "calça", "tênis"]


def test_remover_produto_esgotado(produtos_disponiveis):
    produtos_disponiveis.remove("tênis")
    assert "tênis" not in produtos_disponiveis
    assert len(produtos_disponiveis) == 2


def test_catalogo_tem_tres_produtos(produtos_disponiveis):
    assert len(produtos_disponiveis) == 3   # agora sempre passa, em qualquer ordem
```

Rodando a suíte inteira, em qualquer ordem, `test_catalogo_tem_tres_produtos` sempre vê uma lista com três elementos — porque `produtos_disponiveis()` roda de novo, do zero, a cada teste que a pede. O custo de recriar uma lista de três strings é irrelevante; não havia ganho real de performance em `scope="session"` aqui, só um risco de correção que ninguém tinha percebido.

Se a lista fosse de fato cara de montar (por exemplo, viesse de uma query real a um banco de teste), a solução correta não seria voltar para `scope="session"` — seria separar o dado caro (que não muda) do dado que o teste manipula, com o mesmo padrão de composição de fixtures já mostrado para `engine_db`/`sessao_db`: uma fixture `session` fornecendo os dados brutos imutáveis, e uma fixture `function` construindo, a partir dela, a cópia que cada teste pode mutar livremente:

```python
@pytest.fixture(scope="session")
def produtos_do_catalogo_master():
    """Consulta cara (ex: banco de teste) — roda uma vez, dado tratado como somente-leitura."""
    return carregar_produtos_do_banco_de_teste()


@pytest.fixture
def produtos_disponiveis(produtos_do_catalogo_master):
    """Cópia nova por teste — segura para mutação."""
    return list(produtos_do_catalogo_master)
```

`list(produtos_do_catalogo_master)` cria uma lista **nova**, com os mesmos elementos, mas um objeto diferente na memória — mutar `produtos_disponiveis` dentro de um teste nunca toca `produtos_do_catalogo_master`, que continua intacto para o próximo teste que precisar dele.

## Escopos: tabela-síntese

| Escopo | Frequência | Quando usar | Risco se usado errado |
|---|---|---|---|
| `function` (default) | 1x por função de teste | Dado mutado pelo teste; qualquer setup barato; padrão seguro na dúvida | Nenhum — é o mais isolado |
| `class` | 1x por classe de teste | Setup compartilhado entre métodos de uma mesma classe de teste | Vazamento entre métodos da mesma classe se o dado for mutável |
| `module` | 1x por arquivo de teste | Setup moderadamente caro, útil só naquele arquivo | Vazamento entre testes do mesmo arquivo |
| `session` | 1x por execução da suíte inteira | Recurso caro e **imutável** (ou cuja mutação não afeta testes: conexão, engine) | Vazamento entre TODOS os testes da suíte, em qualquer arquivo — o mais caro de depurar |

## Armadilhas comuns

> [!warning] Escolher escopo amplo "porque é mais rápido" sem checar mutabilidade
> **O que acontece:** o bug de abertura desta nota, generalizado — alguém escolhe `session` ou `module` olhando só para o custo de criação do dado, sem perguntar se algum teste vai modificar o valor devolvido. **Por quê:** Python passa objetos mutáveis por referência; um escopo maior que `function` significa "o mesmo objeto, reaproveitado", não "uma cópia mais barata". **Como evitar:** a pergunta de checagem é sempre "algum teste muta este valor?" — se sim, `function` (ou uma cópia derivada de uma fixture mais ampla, como mostrado acima); se não, escopo maior é seguro e economiza tempo real de execução.

> [!warning] Ordem de execução mascarando o bug em CI
> **O que acontece:** a suíte passa localmente (na ordem em que os arquivos foram escritos, coincidentemente "segura") e falha em CI, onde o pytest pode coletar e ordenar os testes de forma ligeiramente diferente (paralelização com `pytest-xdist`, plugins de ordenação aleatória como `pytest-randomly`). **Por quê:** um bug de vazamento de estado entre testes só se manifesta em **algumas** ordens de execução — a suíte "passar sempre localmente" não é evidência de que o problema não existe, só de que a ordem local nunca expôs a dependência oculta. **Como evitar:** rodar a suíte periodicamente com `pytest-randomly` (ou equivalente) justamente para forçar ordens diferentes e expor esse tipo de acoplamento cedo, em vez de descobrir em produção via CI intermitente.

> [!warning] Fixture com `yield` que nunca chega ao teardown por exceção no próprio setup
> **O que acontece:** o código **antes** do `yield` levanta uma exceção (ex: falha ao conectar num recurso) — nesse caso o `yield` nunca é alcançado, e o código depois dele (o teardown pretendido) **também nunca roda**, porque não há generator pausado para retomar. **Por quê:** o protocolo de generator só executa o que vem depois do `yield` se a execução chegou até o `yield` — uma exceção antes dele interrompe a função ali mesmo, como qualquer exceção não tratada interromperia qualquer função. **Como evitar:** quando o setup em si envolve múltiplos passos que podem falhar parcialmente (abrir uma conexão, depois criar uma tabela temporária), envolver cada passo com seu próprio cleanup condicional, ou aceitar que uma falha no setup não deixa recurso nenhum para limpar — o problema real, nesse caso, costuma ser investigar por que o setup está falhando, não o teardown.

## Em entrevista

- **"Como o pytest sabe que um parâmetro de teste é uma fixture?"** Por nome: o pytest inspeciona a assinatura da função de teste e procura, entre as fixtures visíveis (definidas no arquivo ou em `conftest.py`), uma função decorada com `@pytest.fixture` com exatamente aquele nome. Não há resolução por tipo — é resolução textual pelo nome do parâmetro.
- **"Qual a diferença entre os escopos de fixture?"** Controlam quantas vezes a fixture roda e quem compartilha o valor: `function` (default) roda a cada teste, isolado; `class`/`module` compartilham entre métodos de uma classe ou testes de um arquivo; `session` roda uma vez para a suíte inteira. Escopo maior que `function` significa objeto **compartilhado** (mesma referência), não copiado — perigoso para dado mutável, seguro e eficiente para recurso caro e imutável (ou cuja mutação de fato não afeta os testes, como uma conexão).
- **"O que `yield` muda numa fixture?"** Transforma a fixture num context manager: código antes do `yield` é setup, o valor do `yield` é o que é injetado no teste, código depois do `yield` é teardown, garantido mesmo se o teste falhar — o mesmo padrão do `Depends()` com `yield` do FastAPI, aplicado ao ciclo de vida de um teste em vez de uma requisição HTTP.
- **"Para que serve `conftest.py`?"** É um arquivo de nome reservado que o pytest descobre automaticamente durante a coleta de testes; fixtures definidas ali ficam disponíveis para todo teste no mesmo diretório e em qualquer subdiretório, sem import explícito — o mecanismo que permite compartilhar setup caro (conexão de banco, cliente configurado) entre múltiplos arquivos de teste.
- **"Já viu um bug de teste causado por escopo errado de fixture?"** É a pergunta que testa experiência real, não só conhecimento de sintaxe — vale ter pronto um exemplo concreto (como o do catálogo de produtos desta nota): uma fixture de escopo amplo devolvendo um dado mutável, mutado por um teste, vazando para o próximo, produzindo falha dependente de ordem de execução — e nomear que a correção não é "voltar tudo para `function` por segurança", é separar dado caro-e-imutável de dado mutado-pelo-teste em fixtures diferentes, compostas.

> [!question]- O entrevistador pergunta: "fixtures do pytest são a mesma coisa que mocks?"
> Não — e vale nomear a diferença com precisão. Uma fixture é um mecanismo de **fornecimento de dado ou recurso pronto** para um teste (dado de exemplo, conexão configurada, objeto sob teste já montado) — o conteúdo dela pode ser um dado real, um objeto de produção configurado para teste, ou, sim, um mock. Um mock é uma **técnica de substituição de dependência** (um "dublê" que registra chamadas e devolve valores fixos, no vocabulário de test doubles já coberto em [[03-Dominios/Engenharia/Testes/index|Engenharia/Testes]]). Os dois se combinam o tempo todo na prática — uma fixture que devolve um `Mock()` configurado é comum — mas são conceitos ortogonais: fixture é sobre **como o valor chega até o teste** (injeção, escopo, ciclo de vida); mock é sobre **o que aquele valor é** (um substituto controlado de uma dependência real). O ferramental de mock em si (`unittest.mock`, `pytest-mock`) é assunto da [[03-Dominios/Tecnologia/Python/Testes/index|nota 04 deste galho]], não repetido aqui.

## How to explain in English

> A pytest fixture is a function decorated with `@pytest.fixture`; a test "receives" its value simply by declaring a parameter with the exact same name — no import, no manual instantiation. Pytest inspects the test function's signature and matches by name, the same structural idea as FastAPI's `Depends()` (dependency injection resolved automatically before the function under test runs), just without needing an explicit `Depends()` marker, since a test parameter can only ever be a fixture. Scope (`function`, `class`, `module`, `session`) controls how many times the fixture runs and whether its return value is shared across tests — `function` (the default) creates a fresh object per test, while `session` creates one object for the entire run, shared by every test that requests it. That distinction matters most for mutable data: sharing a mutable object across a broader scope means every test that mutates it leaks that mutation into the next test that asks for the same fixture, producing order-dependent, hard-to-reproduce failures. `yield` instead of `return` turns a fixture into a context manager — code before `yield` is setup, the yielded value is what's injected, code after `yield` is teardown, guaranteed to run even if the test fails — the exact same pattern FastAPI uses for `Depends()` with `yield`, applied to a test's lifecycle instead of an HTTP request's. `conftest.py` is pytest's auto-discovery file: fixtures defined there become available to every test in that directory and its subdirectories, with zero imports — powerful for sharing expensive setup, but confusing to newcomers who see a fixture "appear from nowhere" in a test file with no visible import.

| PT | EN |
|----|----|
| fixture | fixture |
| escopo (de fixture) | fixture scope |
| setup / teardown | setup / teardown |
| injeção por nome de parâmetro | injection by parameter name |
| descoberta automática | auto-discovery |
| vazamento de estado entre testes | state leakage between tests |
| dado mutável | mutable data |
| dependência (composição de fixtures) | fixture dependency |

## Síntese

Uma fixture é a resposta do pytest para "como um teste recebe algo pronto, sem construir sozinho" — resolvida por nome de parâmetro, sem import, sem `Depends()` explícito, mas com a mesma intenção estrutural da injeção de dependência do FastAPI. O que separa uso correto de bug silencioso é o escopo: `function` (default) garante isolamento total — objeto novo a cada teste — e é a escolha segura sempre que o teste modifica o dado; escopos maiores (`class`, `module`, `session`) economizam trabalho real ao compartilhar um objeto entre múltiplos testes, mas essa economia só é segura quando o dado compartilhado não é mutado, ou quando a mutação de fato não importa para o próximo teste — errar essa distinção produz exatamente o tipo de falha mais caro de depurar: um teste que passa sozinho e falha em conjunto, dependendo da ordem. `yield` estende o mecanismo para recursos com ciclo de vida (conexão, arquivo, transação), garantindo teardown mesmo sob falha do teste — o mesmo padrão de `Depends()` com `yield`, aplicado ao escopo de um teste em vez de uma requisição HTTP. E `conftest.py` fecha o mecanismo com descoberta automática: fixtures ali definidas ficam disponíveis para todo teste do diretório e subdiretórios, sem import — poderoso para reaproveitar setup caro entre arquivos, mas responsável por boa parte da confusão de quem chega numa suíte grande pela primeira vez e não sabe que esse arquivo especial existe.

O próximo passo natural do galho usa o mecanismo de fixtures já explicado aqui como base para reduzir duplicação de teste em si — parametrizar um mesmo teste com múltiplos conjuntos de entrada, em vez de escrever uma função de teste quase-idêntica para cada caso.

## Veja também

- [[03-Dominios/Tecnologia/Python/Testes/01 - pytest fundamentos — anatomia, discovery e assert introspection|01 — pytest fundamentos: anatomia, discovery e assert introspection]] — nota anterior deste galho; anatomia de um teste e o mecanismo de discovery que também descobre `conftest.py`.
- [[03-Dominios/Tecnologia/Python/Web e APIs REST/04 - Injeção de dependência no FastAPI — Depends|04 — Injeção de dependência no FastAPI: Depends]] — Galho 10, nota 04; o paralelo estrutural completo com `Depends()`/`Depends(yield=...)` desenvolvido nesta nota, incluindo o incidente original de sessão de banco não fechada que motivou o padrão setup/teardown.
- [[03-Dominios/Tecnologia/Python/Persistência de dados/02 - SQLAlchemy ORM — Session, mapped classes e relationships|02 — SQLAlchemy ORM: Session, mapped classes e relationships]] — Galho 9; vocabulário de `Engine`/`Session` reaproveitado nos exemplos de fixture `engine_db`/`sessao_db` desta nota.
- [[03-Dominios/Engenharia/Testes/index|Testes (Engenharia)]] — teoria e estratégia stack-agnóstica de testes; test doubles (mock vs fixture) citado no callout de entrevista desta nota.
- [[03-Dominios/Tecnologia/Python/Testes/index|Testes (Galho 12)]] — MOC deste galho.

## Fontes

- pytest. *How to use fixtures*. docs.pytest.org/en/stable/how-to/fixtures.html. https://docs.pytest.org/en/stable/how-to/fixtures.html (acessado em 2026-07-11) — mecanismo central de injeção por nome, composição de fixtures.
- pytest. *Fixture finalization / executing teardown code*. docs.pytest.org/en/stable/how-to/fixtures.html#teardown-cleanup-aka-fixture-finalization. https://docs.pytest.org/en/stable/how-to/fixtures.html#teardown-cleanup-aka-fixture-finalization (acessado em 2026-07-11) — `yield`, `try/finally`, garantias de teardown.
- pytest. *Scope: sharing fixtures across classes, modules, packages or session*. docs.pytest.org/en/stable/how-to/fixtures.html#scope-sharing-fixtures-across-classes-modules-packages-or-session. https://docs.pytest.org/en/stable/how-to/fixtures.html#scope-sharing-fixtures-across-classes-modules-packages-or-session (acessado em 2026-07-11) — `function`/`class`/`module`/`session`.
- pytest. *conftest.py: sharing fixtures across multiple files*. docs.pytest.org/en/stable/reference/fixtures.html#conftest-py-sharing-fixtures-across-multiple-files. https://docs.pytest.org/en/stable/reference/fixtures.html#conftest-py-sharing-fixtures-across-multiple-files (acessado em 2026-07-11) — descoberta automática, escopo por diretório.
- Real Python. *Effective Python Testing With Pytest*. realpython.com/pytest-python-testing/. https://realpython.com/pytest-python-testing/ (acessado em 2026-07-11) — fixtures, escopo e `conftest.py` no contexto de uma suíte real.
- [[03-Dominios/Tecnologia/Python/Web e APIs REST/04 - Injeção de dependência no FastAPI — Depends|Injeção de dependência no FastAPI — Depends]] — nota do Galho 10, referenciada para o paralelo com `yield` em dependências.

Consultado em 2026-07-11.
