---
title: "SQLAlchemy Core — Engine, Connection e expressão SQL"
created: 2026-07-11
type: concept
status: complete
fase: adepto
publish: true
tags:
  - python
  - sqlalchemy
  - persistência
aliases:
  - "SQLAlchemy Core"
  - "create_engine"
  - "SQL injection"
  - "bind parameters"
---

# SQLAlchemy Core — Engine, Connection e expressão SQL

> [!abstract] TL;DR
> `create_engine()` cria uma **Engine**: uma fábrica de conexões com um pool por baixo, não uma conexão em si — abrir a Engine não abre TCP nenhum até a primeira query. `Connection` (via `with engine.connect() as conn:`) é o objeto que de fato empresta uma conexão do pool e executa SQL. SQLAlchemy 2.0 constrói SQL como **objetos Python encadeáveis** — `select(tabela).where(...)` — em vez de montar strings à mão; isso não é sintaxe açucarada, é a diferença entre dados e código: parâmetros viram **bind parameters** (`:nome`, resolvidos pelo driver do banco, nunca interpolados na string), o que fecha estruturalmente a porta pra **SQL injection**. `Table`/`MetaData` descrevem schema de forma imperativa, em Python, sem ORM ainda — a base sobre a qual mapped classes (nota 02) são construídas. Regra de ouro desta nota: se o valor de um usuário vira parte literal de uma string SQL antes de chegar ao banco, o sistema tem uma vulnerabilidade — não uma possibilidade de vulnerabilidade, uma vulnerabilidade de fato, explorável com uma linha de input malicioso.

## O bug que abre esta nota

Uma desenvolvedora pleno está implementando um endpoint de busca de usuários por nome, num serviço interno que consulta uma tabela `usuarios` num banco SQLite (o raciocínio e o ataque são idênticos em Postgres, MySQL ou qualquer banco relacional — a escolha de SQLite aqui é só para rodar os exemplos sem infraestrutura externa). O código parece direto ao ponto: pegar o parâmetro de busca da query string, montar o SQL, executar.

```python
from sqlalchemy import create_engine, text

engine = create_engine("sqlite:///demo.db")

def buscar_usuario_por_nome(nome_busca: str):
    """VERSÃO VULNERÁVEL — não use isto em produção. Existe aqui só para
    demonstrar o ataque antes do fix."""
    with engine.connect() as conn:
        sql = f"SELECT id, nome, email, is_admin FROM usuarios WHERE nome = '{nome_busca}'"
        resultado = conn.execute(text(sql))
        return resultado.fetchall()

# Uso "normal", que passa em todo teste manual ingênuo:
buscar_usuario_por_nome("Ana")
# -> [(1, 'Ana', 'ana@exemplo.com', 0)]
```

Funciona. Passa em code review superficial — "usa `text()` do SQLAlchemy, tem parâmetro nomeado no path, parece seguro". O problema é que `nome_busca` não é um bind parameter: é uma f-string interpolada **antes** de o SQL chegar a `text()`. Do ponto de vista do banco de dados, não existe diferença nenhuma entre "o desenvolvedor escreveu esse SQL" e "o texto que sobrou depois de colar a entrada do usuário no meio de uma string" — o banco só vê uma string SQL completa e a executa. Isso é a definição exata de SQL injection: input do usuário sendo interpretado como **código**, não como **dado**.

Um atacante — ou, mais frequentemente em produção, um teste automatizado de segurança, um scanner, ou simplesmente um usuário curioso digitando aspas simples num campo de busca — descobre isso em segundos:

```python
# O payload clássico: fecha a string SQL cedo e injeta uma condição sempre-verdadeira
payload = "' OR '1'='1"
buscar_usuario_por_nome(payload)
```

O SQL que efetivamente chega ao banco, depois da interpolação da f-string, é:

```sql
SELECT id, nome, email, is_admin FROM usuarios WHERE nome = '' OR '1'='1'
```

`'1'='1'` é sempre verdadeiro — a cláusula `WHERE` inteira colapsa para "verdadeiro para toda linha", e a query retorna **todos os usuários da tabela**, incluindo os que têm `is_admin = 1`, e incluindo colunas de e-mail que o endpoint de busca por nome nunca deveria expor em massa. Esse é o payload mais simples possível; a mesma técnica, um pouco mais elaborada, permite:

```python
# Vazamento de dados de OUTRA tabela via UNION, se o número de colunas bater
payload_union = "' UNION SELECT id, nome, senha_hash, 1 FROM credenciais --"
buscar_usuario_por_nome(payload_union)
```

O `--` comenta o resto da query original (o fechamento de aspas que sobraria), e o `UNION SELECT` concatena os resultados de uma tabela completamente diferente — `credenciais`, que o endpoint de busca de usuários jamais deveria tocar — na resposta. Em bancos que suportam múltiplas declarações por chamada (dependendo do driver e da configuração), o mesmo tipo de brecha permite ir além de leitura: `'; DROP TABLE usuarios; --` é o exemplo folclórico, mas variações que fazem `UPDATE`/`DELETE` silenciosos são igualmente reais e mais perigosas por não deixarem rastro óbvio.

> [!bug] O que está quebrado, em uma frase
> `f"... WHERE nome = '{nome_busca}'"` trata o input do usuário como parte do **código SQL**, não como um **valor** — qualquer caractere de controle SQL (aspas, `--`, `;`) dentro do input muda a estrutura lógica da query, não só o valor buscado.

O fix não é escapar aspas manualmente (frágil — sempre existe algum caractere ou encoding que escapa do escape) nem validar a entrada com regex (também frágil, e resolve o sintoma, não a causa). O fix é estrutural: nunca deixar o valor do usuário tocar a string SQL. É exatamente isso que a linguagem de expressão do SQLAlchemy — e `text()` com parâmetros nomeados — force por padrão, o assunto do resto desta nota.

```python
def buscar_usuario_por_nome_seguro(nome_busca: str):
    with engine.connect() as conn:
        sql = text("SELECT id, nome, email, is_admin FROM usuarios WHERE nome = :nome")
        resultado = conn.execute(sql, {"nome": nome_busca})
        return resultado.fetchall()

# O mesmo payload, agora inofensivo — tratado como STRING LITERAL, não como SQL:
buscar_usuario_por_nome_seguro("' OR '1'='1")
# -> [] (nenhum usuário se chama literalmente "' OR '1'='1")
```

O SQL enviado ao driver do banco é sempre o mesmo texto fixo, `WHERE nome = :nome` — o valor `' OR '1'='1` é transmitido separadamente, como dado, pelo protocolo do driver (não por concatenação de string), e o banco o compara literalmente contra a coluna `nome`. Não existe interpretação de `'`, `--` ou `;` como sintaxe SQL nesse caminho — esses caracteres são só texto dentro de um valor de string, do início ao fim.

## `create_engine()`: a Engine é uma fábrica, não uma conexão

O primeiro conceito a desembaraçar é que `create_engine()` **não abre uma conexão com o banco**. Ele cria um objeto `Engine`, que funciona como uma fábrica configurada — sabe como conectar (via uma URL de conexão, que codifica dialeto, driver, credenciais, host, banco), mas só abre uma conexão TCP de verdade quando alguma operação de fato precisa de uma.

```python
from sqlalchemy import create_engine

# Isto NÃO toca o disco nem abre nenhuma conexão ainda
engine = create_engine("sqlite:///demo.db", echo=True)
print(type(engine))  # <class 'sqlalchemy.engine.base.Engine'>
```

A URL de conexão segue o formato `dialeto+driver://usuario:senha@host:porta/banco` — `sqlite:///demo.db` usa o dialeto SQLite com o driver padrão (`sqlite3`, da stdlib), sem usuário/senha/host porque SQLite é um arquivo local; `postgresql+psycopg://user:pass@localhost:5432/meubanco` seria o equivalente para Postgres com o driver `psycopg` (3.x). `echo=True` faz a Engine logar todo SQL executado no stdout — inestimável para depurar exatamente o que a expressão SQL do SQLAlchemy está gerando por baixo, e ferramenta central para detectar N+1 (aprofundado na nota 05 do galho).

O ponto conceitual mais importante da Engine é que ela guarda, internamente, um **pool de conexões** (por padrão, `QueuePool` para a maioria dos bancos — aprofundado na nota 07 do galho). Criar uma Engine não cria conexões no pool imediatamente; o pool começa vazio e cresce sob demanda, até um limite configurável. O papel da Engine é orquestrar esse ciclo: quando código pede uma conexão, ela empresta uma do pool (criando uma nova se necessário e se houver espaço) ou espera até uma ficar disponível; quando o código termina, a conexão volta pro pool em vez de ser fechada de verdade — reuso é o que evita o custo de handshake TCP + autenticação a cada operação.

```mermaid
flowchart LR
    subgraph App["Código da aplicação"]
        A["engine.connect()"]
    end
    subgraph Engine["Engine (fábrica + config)"]
        P["Pool de conexões<br/>(QueuePool, tipicamente)"]
    end
    subgraph DB["Banco de dados"]
        C1["conexão TCP 1"]
        C2["conexão TCP 2"]
        C3["conexão TCP 3 (ociosa no pool)"]
    end

    A -->|"pede uma conexão"| P
    P -->|"empresta (reusa ou cria)"| C1
    P -.->|"já emprestada"| C2
    P -.->|"disponível, aguardando"| C3
    C1 -->|"conn.close() devolve<br/>ao pool, não fecha o socket"| P
```

Uma Engine é tipicamente criada **uma vez por processo** (não uma por request, não uma por query) — é um objeto pesado o suficiente (guarda o pool, a configuração de dialeto, metadados de tipo) para justificar ser um singleton de aplicação, geralmente instanciado no bootstrap e reusado por toda a vida do processo. Recriar `Engine` repetidamente é um anti-padrão comum: cada `create_engine()` novo cria um pool novo, isolado dos anteriores, jogando fora o benefício de reuso de conexões que é a razão de existir do pool.

## `Connection`: o objeto que de fato executa SQL

Se a Engine é a fábrica, `Connection` é o objeto emprestado do pool que efetivamente conversa com o banco. Obtém-se uma via `engine.connect()`, e o padrão idiomático é sempre usá-la como gerenciador de contexto:

```python
with engine.connect() as conn:
    resultado = conn.execute(text("SELECT 1"))
    print(resultado.scalar())  # 1
# ao sair do `with`, a conexão é devolvida ao pool automaticamente
```

`with engine.connect() as conn:` garante que a conexão retorna ao pool mesmo se uma exceção for levantada dentro do bloco — o mesmo raciocínio de `with lock:` garantindo `release()` em código de concorrência: sem o gerenciador de contexto, um `try`/`finally` explícito seria necessário para a mesma garantia, e esquecê-lo vaza conexões do pool até ele se esgotar (um sintoma clássico de produção: erros de "pool esgotado" depois de rodar sob carga por um tempo, causados por conexões nunca devolvidas em caminhos de exceção não tratados).

### Transações implícitas e `commit()`

Por padrão, no SQLAlchemy 2.0, uma `Connection` abre uma transação implicitamente na primeira execução de SQL, e essa transação precisa ser confirmada explicitamente com `conn.commit()` — sem isso, ao sair do bloco `with` sem commit, a transação é revertida (`rollback` implícito). Esse é um comportamento deliberado — "commit as you go" — que evita o erro comum de assumir que uma escrita "aconteceu" só porque o `execute()` não levantou exceção.

```python
with engine.connect() as conn:
    conn.execute(
        text("INSERT INTO usuarios (nome, email, is_admin) VALUES (:nome, :email, :admin)"),
        {"nome": "Beto", "email": "beto@exemplo.com", "admin": False},
    )
    conn.commit()   # sem isto, o INSERT é revertido ao fechar a conexão
```

Para leituras, o commit não é estritamente necessário (não há mudança a persistir), mas é hábito seguro encerrar toda unidade de trabalho de forma explícita — e existe uma variante que trata isso automaticamente: `engine.begin()` abre a conexão **já dentro de uma transação**, com commit automático ao sair do bloco sem exceção e rollback automático se uma exceção escapar.

```python
with engine.begin() as conn:   # commit automático no fim; rollback se levantar exceção
    conn.execute(
        text("INSERT INTO usuarios (nome, email) VALUES (:nome, :email)"),
        {"nome": "Carla", "email": "carla@exemplo.com"},
    )
    conn.execute(
        text("UPDATE contadores SET total = total + 1 WHERE chave = 'usuarios'"),
    )
# ambos INSERT e UPDATE são commitados juntos, ou nenhum é — atomicidade real
```

`engine.begin()` é o padrão idiomático quando o bloco representa uma unidade lógica de trabalho que deve ser tudo-ou-nada (o comportamento ACID de atomicidade, aprofundado com mais rigor na nota 06 do galho); `engine.connect()` com `commit()` manual dá controle mais fino quando é preciso decidir, no meio do código, se a transação deve ou não ser confirmada.

## A linguagem de expressão SQL: `select`/`insert`/`update`/`delete` como objetos

A parte central do SQLAlchemy Core — o que o diferencia de simplesmente rodar strings SQL cruas via `text()` — é a **linguagem de expressão** (*SQL Expression Language*): construções como `select()`, `insert()`, `update()`, `delete()` que retornam objetos Python encadeáveis, representando a query como uma **árvore de sintaxe**, não como texto. Isso significa que a query é construída, composta, e inspecionada como estrutura de dados Python antes de ser traduzida para SQL de fato — e essa tradução (chamada *compilation*) é feita pelo dialeto configurado na Engine, o que também dá portabilidade entre bancos (a mesma expressão Python pode compilar para SQL levemente diferente em SQLite vs. Postgres vs. MySQL, sem o desenvolvedor escrever SQL específico de cada um).

Para usar a linguagem de expressão, primeiro é preciso descrever o schema em Python — o assunto da próxima seção — mas o encadeamento básico já dá o sabor:

```python
from sqlalchemy import select

stmt = select(usuarios).where(usuarios.c.nome == "Ana")
print(stmt)
# SELECT usuarios.id, usuarios.nome, usuarios.email, usuarios.is_admin
# FROM usuarios
# WHERE usuarios.nome = :nome_1
```

Note o `:nome_1` no SQL impresso — mesmo ao imprimir a query como texto para debug, o SQLAlchemy já a monta com um bind parameter, nunca com o literal `"Ana"` interpolado. Isso não é um detalhe cosmético: é a mesma garantia estrutural contra SQL injection do exemplo de abertura, só que automática, sem exigir que o desenvolvedor lembre de usar `text()` com `:nome` — a linguagem de expressão inteira é desenhada para tornar impossível, por construção, colar um valor Python direto dentro do SQL gerado.

```python
with engine.connect() as conn:
    resultado = conn.execute(stmt)
    for linha in resultado:
        print(linha.id, linha.nome, linha.email)
```

### Encadeamento: `where`, `order_by`, `limit`, condições compostas

```python
from sqlalchemy import select, and_, or_

# Encadeamento fluente — cada método retorna um novo objeto Select
stmt = (
    select(usuarios.c.id, usuarios.c.nome, usuarios.c.email)
    .where(usuarios.c.is_admin == False)
    .where(usuarios.c.nome.like("A%"))
    .order_by(usuarios.c.nome)
    .limit(10)
)

# Condições compostas com and_()/or_() (ou o operador & / | sobrecarregado)
stmt_composta = select(usuarios).where(
    and_(
        usuarios.c.is_admin == False,
        or_(usuarios.c.nome == "Ana", usuarios.c.nome == "Beto"),
    )
)
```

Cada chamada (`.where()`, `.order_by()`, `.limit()`) não modifica o objeto original — retorna um **novo** objeto `Select` com a cláusula adicionada, o mesmo padrão de imutabilidade encadeável comum em builders de outras linguagens (o `Stream` do Java, por exemplo). Isso permite montar queries base reusáveis e derivar variações sem risco de uma chamada afetar outra que compartilhe a mesma query base:

```python
base = select(usuarios).where(usuarios.c.is_admin == False)

so_ana = base.where(usuarios.c.nome == "Ana")       # nova query, independente
todos_nao_admin = base                               # `base` continua intacta
```

### `insert()`, `update()`, `delete()`

O mesmo padrão de objeto encadeável se aplica às operações de escrita:

```python
from sqlalchemy import insert, update, delete

with engine.begin() as conn:
    # INSERT — retorna o objeto Insert; .values() define as colunas
    conn.execute(insert(usuarios).values(nome="Dora", email="dora@exemplo.com"))

    # UPDATE — .where() restringe quais linhas; sem where, atualiza a tabela inteira
    conn.execute(
        update(usuarios).where(usuarios.c.nome == "Dora").values(email="dora.nova@exemplo.com")
    )

    # DELETE — mesmo raciocínio: sem .where(), apaga TUDO
    conn.execute(delete(usuarios).where(usuarios.c.nome == "Dora"))
```

> [!warning] `update()`/`delete()` sem `.where()` afeta a tabela inteira
> Diferente de um `DELETE FROM tabela` escrito por engano numa string SQL crua — que ao menos "parece" perigoso visualmente — `delete(usuarios)` sem `.where()` é sintaticamente válido e silenciosamente correto do ponto de vista do SQLAlchemy: ele apaga **todas as linhas** da tabela, porque não há filtro nenhum. Esse é um erro fácil de cometer ao refatorar uma query e esquecer de recolar a cláusula `.where()`. Revisão de código em qualquer `update()`/`delete()` deve checar explicitamente que existe um `.where()` correspondente à intenção — ou que a ausência dele é deliberada.

Inserts em lote (múltiplas linhas de uma vez) usam `.values()` com uma lista de dicionários passada diretamente ao `execute()`, mais eficiente que um loop de inserts individuais:

```python
with engine.begin() as conn:
    conn.execute(
        insert(usuarios),
        [
            {"nome": "Eva", "email": "eva@exemplo.com"},
            {"nome": "Fabio", "email": "fabio@exemplo.com"},
        ],
    )
```

## `Table` e `MetaData`: schema descrito em Python, sem ORM

Antes de escrever `select(usuarios)`, é preciso que `usuarios` exista como objeto Python — e é aqui que `Table`/`MetaData` entram. `MetaData` é um catálogo: uma coleção de objetos `Table` que descrevem o schema do banco (nomes de tabela, colunas, tipos, chaves). Definir uma `Table` **não** cria a tabela no banco automaticamente — é uma descrição, em Python, do schema que existe (ou deveria existir) no banco; criar de fato requer uma chamada explícita (`metadata.create_all(engine)`), tipicamente só usada em testes e protótipos — em produção, criação e evolução de schema são responsabilidade de migrations (Alembic, nota 03 do galho), não de `create_all()`.

```python
from sqlalchemy import MetaData, Table, Column, Integer, String, Boolean

metadata = MetaData()

usuarios = Table(
    "usuarios",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("nome", String(120), nullable=False),
    Column("email", String(255), nullable=False, unique=True),
    Column("is_admin", Boolean, nullable=False, default=False),
)

# Só em contexto de teste/protótipo — em produção isso é papel do Alembic
metadata.create_all(engine)
```

`Column` descreve cada coluna: nome, tipo (`Integer`, `String(120)` com tamanho máximo, `Boolean`, e outros tipos como `DateTime`, `Numeric`, `Text`, `ForeignKey` para relacionamentos), e restrições (`primary_key=True`, `nullable=False`, `unique=True`, `default=` para um valor padrão aplicado pelo lado do SQLAlchemy ao inserir). O objeto `usuarios` resultante expõe suas colunas via `.c` (abreviação de *columns*) — `usuarios.c.nome`, `usuarios.c.email` — que é exatamente o que alimenta `.where()`, `.values()`, e as demais construções da linguagem de expressão vistas acima.

```python
# usuarios.c dá acesso tipado às colunas, usado em toda a linguagem de expressão
print(usuarios.c.keys())           # ['id', 'nome', 'email', 'is_admin']
print(usuarios.c.nome.type)        # String(120)
print(usuarios.primary_key)        # PrimaryKeyConstraint(...)
```

Chaves estrangeiras se expressam com `ForeignKey`, ligando uma coluna de uma tabela a outra:

```python
pedidos = Table(
    "pedidos",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("usuario_id", Integer, ForeignKey("usuarios.id"), nullable=False),
    Column("total", Numeric(10, 2), nullable=False),
)
```

Essa forma imperativa — `Table`/`Column`/`MetaData` escritos explicitamente — é a base sobre a qual o ORM (nota 02 do galho) é construído: `DeclarativeBase`/mapped classes com `Mapped[]` no SQLAlchemy 2.0 geram, por baixo, exatamente esses mesmos objetos `Table`. Entender o Core primeiro é o que torna o ORM menos mágico: uma classe mapeada não é uma abstração paralela ao SQL, é uma camada de conveniência sobre a mesma árvore de expressão que `select()`/`insert()` manipulam diretamente.

## Bind parameters: `text()` com parâmetros nomeados, sempre

Quando SQL cru é necessário — uma query complexa demais para a linguagem de expressão expressar de forma legível, uma feature específica de dialeto sem equivalente em Core, ou simplesmente uma migração incremental de um sistema legado — `text()` é a ferramenta certa, mas **somente** combinado com parâmetros nomeados. O padrão é fixo: escrever `:nome_do_parametro` no SQL, e passar um dicionário (ou lista de dicionários, para múltiplas execuções) como segundo argumento de `execute()`.

```python
from sqlalchemy import text

with engine.connect() as conn:
    stmt = text("""
        SELECT id, nome, email
        FROM usuarios
        WHERE is_admin = :admin AND nome LIKE :prefixo
    """)
    resultado = conn.execute(stmt, {"admin": False, "prefixo": "A%"})
    for linha in resultado:
        print(linha.id, linha.nome)
```

O que acontece por baixo: o driver do banco (`sqlite3`, `psycopg`, etc.) recebe o SQL e os parâmetros **separadamente**, através do protocolo de comunicação com o banco — não como uma string única já montada. O banco compila (ou prepara) o SQL uma vez, com placeholders no lugar dos valores, e só então substitui os placeholders pelos valores recebidos, tratando-os estritamente como dados de um tipo conhecido (string, inteiro, booleano), nunca como fragmento de sintaxe SQL a ser interpretado. É essa separação em dois canais — SQL de um lado, dados do outro — que torna a injeção estruturalmente impossível pelo caminho de bind parameters, não uma questão de sorte ou de escaping bem feito.

```mermaid
sequenceDiagram
    participant App as Código Python
    participant SA as SQLAlchemy
    participant Driver as Driver do banco
    participant DB as Banco de dados

    App->>SA: text("... WHERE nome = :nome"), {"nome": "' OR '1'='1"}
    SA->>Driver: SQL fixo + parâmetros separados (protocolo do driver)
    Driver->>DB: prepara SQL: "... WHERE nome = ?"
    Driver->>DB: envia valor "' OR '1'='1" como DADO, não como sintaxe
    DB->>DB: compara nome = "' OR '1'='1" (comparação literal de string)
    DB-->>App: 0 linhas — nenhum usuário se chama isso
```

Vale nomear a comparação explícita entre os dois caminhos que aparecem nesta nota:

| Caminho | Como o valor chega ao SQL | Vulnerável a injection? |
|---|---|---|
| f-string / `.format()` / concatenação | Interpolado na string ANTES de virar SQL — o banco não distingue "código" de "dado colado" | Sim, sempre |
| `text("... :nome")` + dict de parâmetros | Transmitido separadamente pelo protocolo do driver | Não |
| `select()`/`insert()`/`update()`/`delete()` (linguagem de expressão) | Nunca existe como string interpolável — vira bind parameter automaticamente na compilação | Não, por construção |

A regra prática, sem exceção: **nenhum valor vindo de fora do código-fonte (input de usuário, parâmetro de API, variável de ambiente que não seja puramente de configuração) deve tocar uma string SQL por concatenação, jamais** — nem mesmo "só uma vez, num script interno que ninguém mais vai rodar". A distância entre "script interno" e "endpoint exposto que alguém copiou o padrão de" costuma ser menor do que parece em retrospecto.

> [!question]- E identificadores dinâmicos — nome de tabela ou coluna vindo de uma variável? Bind parameters resolvem isso também?
> Não da mesma forma — bind parameters (`:nome`) só funcionam para **valores** (o que entra numa cláusula `WHERE coluna = :valor`), não para **identificadores** (nomes de tabela, nomes de coluna, direção de `ORDER BY`). O protocolo de bind parameters do banco não tem como aceitar "o nome da tabela é este parâmetro" — identificadores fazem parte da estrutura do SQL, não do seu conteúdo de dados. Quando um identificador precisa ser dinâmico (por exemplo, ordenar por uma coluna escolhida pelo usuário via query string), a defesa correta é uma **allowlist** explícita: validar que o valor recebido está num conjunto fixo de identificadores permitidos (`if coluna not in {"nome", "email", "criado_em"}: raise ValueError(...)`) antes de usá-lo para montar a expressão — nunca aceitar o identificador literal do usuário sem essa checagem, e nunca tentar "escapá-lo" como se fosse um valor.

## Executando e lendo resultados: `Result`, `Row`, `.scalar()`, `.mappings()`

`conn.execute()` retorna um objeto `Result` — um iterável de objetos `Row`, cada um representando uma linha do resultado, acessível por índice posicional (`linha[0]`), por nome de coluna via atributo (`linha.nome`), ou como dicionário-like via `.mappings()`.

```python
with engine.connect() as conn:
    resultado = conn.execute(select(usuarios))

    for linha in resultado:
        print(linha.id, linha.nome)          # acesso por atributo

    # .scalar() — quando a query retorna uma única coluna/valor (ex: COUNT)
    total = conn.execute(select(func.count()).select_from(usuarios)).scalar()

    # .mappings() — cada linha vira algo dict-like, útil para serializar em JSON
    resultado_dict = conn.execute(select(usuarios)).mappings()
    for linha in resultado_dict:
        print(linha["nome"], linha["email"])

    # .fetchone() / .fetchall() — variantes explícitas de consumo
    primeira = conn.execute(select(usuarios)).fetchone()
    todas = conn.execute(select(usuarios)).fetchall()
```

Um detalhe que costuma pegar quem vem de outras linguagens: `Result` é consumível **uma única vez** — depois de iterado (ou de `.fetchall()` chamado), o cursor subjacente já avançou até o fim, e tentar iterar de novo retorna vazio. Se o resultado precisa ser usado mais de uma vez, ele deve ser materializado numa lista Python (`linhas = resultado.fetchall()`) e reusado a partir dela, não reconsultado no objeto `Result` original.

## Armadilhas comuns

> [!warning] Concatenar SQL com f-string "só desta vez"
> **O que acontece:** um script interno, uma ferramenta de admin, um endpoint que "nunca vai receber input malicioso" usa f-string ou `.format()` para montar SQL com um valor vindo de fora do código. **Por quê:** a superfície de ataque não é sobre a intenção original do código, é sobre todo caminho de execução que existirá no futuro — scripts internos viram endpoints, ferramentas de admin ganham acesso mais amplo, "nunca vai receber input malicioso" é uma previsão, não uma garantia. **Como evitar:** tratar bind parameters (`text()` com `:nome` ou a linguagem de expressão) como não-negociável para qualquer valor que não seja um literal fixo escrito no próprio código-fonte — sem exceção "só desta vez".

> [!warning] Recriar a `Engine` a cada request ou a cada função
> **O que acontece:** `create_engine()` chamado dentro de uma função de handler de request, ou de um script que roda em loop, criando uma Engine (e um pool) novo a cada chamada. **Por quê:** cada Engine nova tem seu próprio pool vazio, isolado dos anteriores — o custo de abrir conexão TCP + autenticação, que o pool existe para amortizar, volta a acontecer a cada chamada, e as conexões das Engines anteriores ficam órfãs até serem coletadas pelo garbage collector, sem devolução organizada ao pool. **Como evitar:** criar a `Engine` uma vez, no bootstrap da aplicação (nível de módulo, ou injetada via container de dependências), e reusá-la por toda a vida do processo — nunca dentro de uma função chamada repetidamente.

> [!warning] Esquecer `.commit()` (ou não usar `engine.begin()`) e achar que a escrita "sumiu"
> **O que acontece:** um `INSERT`/`UPDATE` roda sem erro dentro de `with engine.connect() as conn:`, mas ao consultar depois (mesmo dentro da mesma sessão de terminal, mas em outra conexão), a linha não está lá. **Por quê:** sem `conn.commit()`, a transação implícita aberta pela primeira execução nunca é confirmada — ao sair do bloco `with` sem commit explícito, o SQLAlchemy reverte (`rollback`) a transação por padrão, silenciosamente. **Como evitar:** usar `engine.begin()` para blocos de escrita (commit automático no sucesso, rollback automático em exceção), ou chamar `conn.commit()` explicitamente ao final de cada unidade lógica de escrita dentro de `engine.connect()`.

> [!warning] `update()`/`delete()` sem `.where()`, afetando a tabela inteira
> **O que acontece:** refatoração de uma query esquece de recolar a cláusula `.where()`, e o `update()`/`delete()` resultante é sintaticamente válido — só que aplicado a todas as linhas da tabela. **Por quê:** diferente de um erro de sintaxe, isso não levanta exceção nenhuma — o SQLAlchemy executa exatamente o que foi pedido, e "nenhum filtro" é uma instrução válida, só que quase nunca a intenção real. **Como evitar:** revisar explicitamente, em code review, todo `update()`/`delete()` sem `.where()` correspondente — e, em sistemas críticos, considerar um linter/CI check que barre `update()`/`delete()` sem `.where()` na base de código.

## Em entrevista

Perguntas sobre SQLAlchemy Core em entrevista sênior costumam testar se o candidato entende a diferença entre Engine e Connection, e se reconhece SQL injection não como conceito abstrato de segurança, mas como algo que se evita por escolha de API, todo dia, sem esforço extra.

> "`create_engine()` doesn't open a connection — it creates a factory object that owns a connection pool, and connections are only opened lazily, on first use. `engine.connect()` borrows a connection from that pool, and I always use it as a context manager so it's returned to the pool even if an exception is raised. For writes, I prefer `engine.begin()` over `engine.connect()` plus manual `commit()` — it gives me automatic commit on success and automatic rollback on exception, which removes an entire class of bugs where a write silently doesn't persist because someone forgot to call `commit()`. On SQL injection specifically: the fix isn't escaping user input, it's never letting user input touch a SQL string as text in the first place. SQLAlchemy's expression language — `select()`, `insert()`, `update()`, `delete()` — builds queries as Python objects, and any value passed through `.where()` or `.values()` automatically becomes a bind parameter, transmitted to the driver separately from the SQL text. Even raw SQL through `text()` supports named bind parameters — `:name` plus a parameters dict — which the driver sends through a separate channel from the query itself, so the database engine compares the value literally as a string, never interprets it as SQL syntax. Concatenating an f-string into a SQL string is the one pattern that reopens that vulnerability, no matter how trusted the input source seems at the time."

Um follow-up comum: **"por que bind parameters não resolvem um `ORDER BY` dinâmico?"** — a resposta correta reconhece que bind parameters cobrem *valores*, não *identificadores* (nomes de coluna/tabela fazem parte da estrutura sintática do SQL, não do seu conteúdo de dados), e que a defesa nesse caso é uma allowlist explícita de identificadores permitidos, validada em código Python antes de montar a expressão.

> [!question]- E se perguntarem sobre ORMs "serem imunes" a SQL injection por padrão?
> Vale corrigir a premissa com precisão: um ORM (SQLAlchemy ORM, Django ORM) torna SQL injection **muito mais difícil de introduzir por acidente**, porque o caminho padrão (filtros, `.values()`, mapped attributes) sempre passa por bind parameters automaticamente — mas não é uma garantia absoluta e incondicional. Métodos de escape hatch para SQL cru (`text()` no SQLAlchemy, `.raw()` ou `.extra()` no Django) existem justamente para casos que a linguagem de expressão não cobre bem, e usá-los com concatenação de string reabre a mesma vulnerabilidade — a proteção vem do **padrão usado**, não de o projeto "ser um ORM". Essa distinção — ferramenta segura por padrão vs. garantia incondicional — costuma ser o que separa uma resposta júnior de uma sênior nesse tópico.

## Como explicar em inglês

| PT | EN |
|----|----|
| fábrica de conexões | connection factory |
| pool de conexões | connection pool |
| bind parameter / parâmetro nomeado | bind parameter / named parameter |
| linguagem de expressão SQL | SQL expression language |
| injeção de SQL | SQL injection |
| interpolação de string | string interpolation |
| identificador (nome de tabela/coluna) | identifier |
| lista de permissão | allowlist |
| confirmar (uma transação) | commit (a transaction) |
| reverter (uma transação) | roll back (a transaction) |
| definição de schema imperativa | imperative schema definition |
| tabela mapeada / objeto de tabela | table object / mapped table |

## O que vem a seguir

Esta nota estabeleceu o Core do SQLAlchemy — Engine como fábrica, Connection como executor, `Table`/`MetaData` como schema imperativo, e a linguagem de expressão como o mecanismo que torna bind parameters o caminho padrão, fechando a porta de SQL injection por construção em vez de depender de disciplina do desenvolvedor. As próximas notas constroem sobre essa base:

- [[02 - SQLAlchemy ORM — Session, mapped classes e relationships|02 — SQLAlchemy ORM: Session, mapped classes e relationships]] — como `DeclarativeBase`/`Mapped[]` mapeiam classes Python para as mesmas estruturas `Table` vistas aqui, e como `Session` adiciona unit of work e identity map por cima do Core.
- [[03 - Migrations com Alembic — versionamento de schema|03 — Migrations com Alembic]] — como o schema descrito por `Table`/`MetaData` evolui de forma versionada em produção, em vez de `metadata.create_all()`.
- [[07 - Connection pooling e performance em produção|07 — Connection pooling e performance em produção]] — aprofunda o pool só mencionado aqui: `pool_size`, `max_overflow`, `pool_recycle`, e o problema de múltiplos workers cada um com seu próprio pool.
- [[03-Dominios/Tecnologia/Python/Persistência de dados/index|Persistência de dados (Galho 9)]] — MOC deste galho.

## Fontes

- SQLAlchemy. *Engine Configuration*. docs.sqlalchemy.org, versão 2.0. https://docs.sqlalchemy.org/en/20/core/engines.html (acessado em 2026-07-11) — `create_engine()`, URLs de conexão, `echo`.
- SQLAlchemy. *Working with Engines and Connections*. docs.sqlalchemy.org, versão 2.0. https://docs.sqlalchemy.org/en/20/core/connections.html (acessado em 2026-07-11) — `Connection`, `engine.begin()` vs `engine.connect()`, transações commit-as-you-go.
- SQLAlchemy. *SQL Expression Language Tutorial*. docs.sqlalchemy.org, versão 2.0. https://docs.sqlalchemy.org/en/20/tutorial/index.html (acessado em 2026-07-11) — `select()`/`insert()`/`update()`/`delete()`, `Table`/`MetaData`, execução e leitura de resultados.
- SQLAlchemy. *Working with Data* (Sending Parameters). docs.sqlalchemy.org, versão 2.0. https://docs.sqlalchemy.org/en/20/tutorial/data.html (acessado em 2026-07-11) — bind parameters com `text()`, `.execute()` com dicts de parâmetros.
- OWASP Foundation. *SQL Injection*. owasp.org. https://owasp.org/www-community/attacks/SQL_Injection (acessado em 2026-07-11) — anatomia do ataque, exemplos de payload, por que allowlists são a defesa correta para identificadores dinâmicos.
- Python Software Foundation. *sqlite3 — DB-API 2.0 interface for SQLite databases*. docs.python.org, versão 3.14. https://docs.python.org/3/library/sqlite3.html (acessado em 2026-07-11) — driver usado nos exemplos rodáveis desta nota.

Consultado em 2026-07-11.
