---
title: "N+1 e eager loading — joinedload/selectinload vs select_related/prefetch_related"
created: 2026-07-11
type: concept
status: complete
fase: Magus
publish: true
tags:
  - python
  - sqlalchemy
  - django
  - persistência
aliases:
  - "N+1 queries"
  - "joinedload"
  - "selectinload"
  - "subqueryload"
  - "select_related"
  - "prefetch_related"
---

# N+1 e eager loading — joinedload/selectinload vs select_related/prefetch_related

> [!abstract] TL;DR
> **N+1** é o padrão de performance mais comum e mais caro em código ORM: uma query busca N registros, e depois o código acessa uma relationship de cada um deles dentro de um loop — disparando **mais N queries**, uma por iteração, em vez de uma segunda query só. 100 pedidos viram 101 queries (1 + 100), não 1 ou 2. O ORM não avisa: cada acesso a `pedido.cliente` parece um atributo Python comum, mas por baixo é um `SELECT` novo indo ao banco. A correção chama-se **eager loading** — pedir os dados relacionados junto com a query principal, adiantando o custo pra um número fixo de queries independente de N. No SQLAlchemy há três estratégias com tradeoffs diferentes: `joinedload()` (um `LEFT OUTER JOIN` só, ótimo pra `many-to-one`/`one-to-one`, mas explode em duplicação de linhas se usado ingenuamente num `one-to-many` com muitos filhos), `selectinload()` (uma segunda query com `WHERE id IN (...)`, a escolha default pra `one-to-many`/`many-to-many` porque não duplica linha nem sofre limite de `IN`), e `subqueryload()` (uma segunda query via subquery correlacionada, alternativa mais antiga a `selectinload`, hoje relegada a casos de borda). No Django, o mapeamento conceitual é direto: **`select_related()`** faz `JOIN` (só serve pra `ForeignKey`/`OneToOneField`, o lado "um" da relação — equivalente a `joinedload`), e **`prefetch_related()`** faz uma query separada com `IN` e junta em Python (serve pra `ManyToManyField` e FK reversa, o lado "muitos" — equivalente a `selectinload`). Detectar N+1 na prática: SQLAlchemy com `echo=True` no `create_engine` ou logger `sqlalchemy.engine` em `INFO`; Django com `django-debug-toolbar` (painel SQL, conta queries por request) ou `django.db.connection.queries` (lista bruta em testes) — ambos convergem pra mesma pergunta de diagnóstico: "quantas queries essa view/endpoint disparou, e esse número cresce com o tamanho dos dados?".

## O bug que abre esta nota

Um desenvolvedor implementa um endpoint que lista os últimos 100 pedidos com o nome do cliente de cada um. O código parece direto ao ponto — busca os pedidos, itera, imprime o nome do cliente relacionado:

```python
from sqlalchemy.orm import Session
from sqlalchemy import select

with Session(engine) as session:
    pedidos = session.scalars(select(Pedido).limit(100)).all()

    for pedido in pedidos:
        print(f"Pedido #{pedido.id} — cliente: {pedido.cliente.nome}")
```

Em desenvolvimento, com um banco local de 10 registros de teste, isso roda em milissegundos e ninguém percebe nada de errado — o código passa em revisão, vai pra produção. Em produção, com dados reais, o endpoint que deveria responder em ~20ms passa a levar **800ms a 2 segundos**, e ninguém mexeu na lógica. Ligando o log de SQL do SQLAlchemy (`echo=True` no `create_engine`, como esta nota mostra adiante), o problema aparece cru:

```
INFO sqlalchemy.engine.Engine SELECT pedidos.id, pedidos.valor_centavos, pedidos.cliente_id
INFO sqlalchemy.engine.Engine FROM pedidos LIMIT 100
-- ↑ 1 query, retorna 100 linhas

INFO sqlalchemy.engine.Engine SELECT clientes.id, clientes.nome, clientes.email
INFO sqlalchemy.engine.Engine FROM clientes WHERE clientes.id = ?
INFO sqlalchemy.engine.Engine [generated in 0.00012s] (1,)
INFO sqlalchemy.engine.Engine SELECT clientes.id, clientes.nome, clientes.email
INFO sqlalchemy.engine.Engine FROM clientes WHERE clientes.id = ?
INFO sqlalchemy.engine.Engine [cached since 0.001s ago] (2,)
INFO sqlalchemy.engine.Engine SELECT clientes.id, clientes.nome, clientes.email
INFO sqlalchemy.engine.Engine FROM clientes WHERE clientes.id = ?
INFO sqlalchemy.engine.Engine [cached since 0.002s ago] (3,)
-- ... mais 97 linhas exatamente iguais a essa, uma por pedido ...
```

Contando: **1 query** pra buscar os 100 pedidos, mais **100 queries**, uma por pedido, pra buscar cada `cliente` individualmente — cada uma um round-trip de rede completo ao banco, mesmo que o SQL em si seja trivial. **101 queries no total**, para uma operação que deveria custar 1 ou no máximo 2. Esse é o **problema de N+1** — nomeado assim porque o custo é literalmente `1 + N`: uma query pra buscar a lista, N queries adicionais, uma por item da lista, pra buscar um dado relacionado de cada um.

> [!bug] O que está quebrado, em uma frase
> Cada acesso a `pedido.cliente` dentro do loop parece um atributo Python comum, mas dispara um `SELECT` novo pro banco — porque `relationship()` é **lazy** por padrão (ver [[02 - SQLAlchemy ORM — Session, mapped classes e relationships|nota 02]]); o custo que deveria ser fixo (1-2 queries) vira **linear no número de registros** (`1 + N` queries), e o código não dá nenhum sinal visual de que isso está acontecendo.

```mermaid
sequenceDiagram
    participant App as Código Python
    participant DB as Banco de dados

    App->>DB: SELECT * FROM pedidos LIMIT 100
    DB-->>App: 100 linhas de pedidos

    loop para cada um dos 100 pedidos
        App->>DB: SELECT * FROM clientes WHERE id = ?
        DB-->>App: 1 linha de cliente
    end

    Note over App,DB: Total: 1 + 100 = 101 queries<br/>101 round-trips de rede, um por vez
```

A razão pela qual isso é tão fácil de escrever sem perceber é justamente a elegância do ORM: `pedido.cliente.nome` é sintaxe de atributo Python, indistinguível visualmente de acessar um campo já carregado em memória. Não existe nenhum aviso sintático de "isto vai ao banco". O problema só aparece com volume — em dev, com poucos registros, 1+3 queries em vez de 1+2 não muda percepção nenhuma; em produção, com 100, 1.000, 10.000 registros, o crescimento linear vira o gargalo dominante do endpoint, e cada query paga o custo fixo de um round-trip de rede (tipicamente 1-5ms em rede local, dezenas de ms com latência real) além do custo de execução em si.

## Por que isso acontece: lazy loading por padrão

A causa raiz é exatamente o mecanismo coberto na [[02 - SQLAlchemy ORM — Session, mapped classes e relationships|nota 02]]: `relationship()`, sem nenhuma configuração adicional, usa **lazy loading** — o SQLAlchemy só dispara o `SELECT` da relação quando o atributo é efetivamente acessado, não quando o objeto principal é carregado. Isso é uma escolha de design deliberada e defensável: carregar toda relação de todo objeto sempre, mesmo quando o código nunca vai tocá-la, desperdiçaria trabalho na direção oposta. O problema não é lazy loading em si — é lazy loading **dentro de um loop**, onde o mesmo padrão de acesso se repete N vezes e cada repetição paga o custo total de um round-trip.

A solução não é "parar de usar `relationship()`" nem "carregar tudo sempre" — é **eager loading seletivo**: dizer explicitamente, na query principal, "eu sei que vou precisar de `cliente` para cada `pedido` desta lista, então traga junto". É exatamente o que as estratégias a seguir fazem, cada uma com um mecanismo de SQL diferente por baixo.

## `joinedload()`: um JOIN só

`joinedload()` resolve o N+1 fazendo o SQLAlchemy emitir um único `SELECT` com `LEFT OUTER JOIN` entre a tabela principal e a relacionada — os dados do `cliente` vêm **na mesma linha** de resultado que o `pedido`, então não existe segunda query nenhuma.

```python
from sqlalchemy.orm import joinedload
from sqlalchemy import select

with Session(engine) as session:
    stmt = select(Pedido).options(joinedload(Pedido.cliente)).limit(100)
    pedidos = session.scalars(stmt).all()

    for pedido in pedidos:
        print(f"Pedido #{pedido.id} — cliente: {pedido.cliente.nome}")
        # nenhum SELECT adicional aqui — cliente já veio no JOIN
```

SQL gerado (uma única query):

```sql
SELECT pedidos.id, pedidos.valor_centavos, pedidos.cliente_id,
       clientes_1.id AS clientes_1_id, clientes_1.nome AS clientes_1_nome
FROM pedidos
LEFT OUTER JOIN clientes AS clientes_1 ON clientes_1.id = pedidos.cliente_id
LIMIT 100
```

**`joinedload()` é a escolha certa para relações `many-to-one` e `one-to-one`** — o caso `Pedido → Cliente` do exemplo: cada `Pedido` tem exatamente **um** `Cliente`, então o `JOIN` produz exatamente uma linha de resultado por `Pedido`, sem duplicação nenhuma. É a estratégia mais eficiente possível nesse caso: uma query, um round-trip, sem overhead de segunda consulta.

### O problema de `joinedload()` em `one-to-many`: explosão de linhas

O mesmo mecanismo que funciona bem pra `many-to-one` vira um problema em `one-to-many` com muitos filhos — o caso inverso, um `Cliente` que tem **muitos** `Pedido`s:

```python
stmt = select(Cliente).options(joinedload(Cliente.pedidos)).limit(100)
clientes = session.scalars(stmt).unique().all()  # .unique() é OBRIGATÓRIO aqui
```

SQL gerado:

```sql
SELECT clientes.id, clientes.nome,
       pedidos_1.id AS pedidos_1_id, pedidos_1.valor_centavos AS pedidos_1_valor_centavos
FROM clientes
LEFT OUTER JOIN pedidos AS pedidos_1 ON pedidos_1.cliente_id = clientes.id
LIMIT 100
```

Se cada `Cliente` tem em média 20 `Pedido`s, o `JOIN` produz **uma linha por combinação cliente×pedido** — um `Cliente` com 20 pedidos aparece **20 vezes** no resultado bruto do `SELECT`, uma vez para cada `Pedido` relacionado, com todos os dados do `Cliente` repetidos em cada uma dessas 20 linhas. O SQLAlchemy desduplica isso na camada Python (por isso o `.unique()` é exigido — sem ele, a query levanta erro pedindo explicitamente esse `.unique()`), mas o **banco ainda processou e transmitiu N linhas redundantes pela rede**: com 100 clientes × 20 pedidos médios, isso é 2.000 linhas de dados de `Cliente` duplicados brutalmente, transmitidos e depois jogados fora na desduplicação. Com relações ainda maiores (um cliente com 500 pedidos, um post com 10.000 comentários), o `JOIN` explode em volume de dados transferidos, e a economia de "só 1 query" perde pro custo de transferir uma quantidade de dados N vezes maior que o necessário.

```mermaid
flowchart LR
    subgraph joined["joinedload em one-to-many — explosão de linhas"]
        C1["Cliente #1"] -->|JOIN| P1a["Pedido A"]
        C1 -->|JOIN| P1b["Pedido B"]
        C1 -->|JOIN| P1c["Pedido C"]
        note1["Cliente #1 aparece<br/>3 VEZES no resultado bruto,<br/>1 por pedido"]
    end
```

> [!warning] `joinedload()` em `one-to-many` sem `.unique()`
> **O que acontece:** `session.scalars(stmt).all()` sem `.unique()` numa query com `joinedload()` sobre uma relação `one-to-many` levanta `InvalidRequestError`, pedindo explicitamente `.unique()` antes de `.all()`. **Por quê:** o `JOIN` produz linhas duplicadas do lado "um" (uma por item do lado "muitos"); sem desduplicar, o resultado teria objetos `Cliente` Python repetidos — tecnicamente o mesmo objeto (o identity map da [[02 - SQLAlchemy ORM — Session, mapped classes e relationships|nota 02]] garante isso), mas repetido na lista de resultado. **Como evitar:** usar `selectinload()` em vez de `joinedload()` para relações `one-to-many`/`many-to-many` — é a estratégia recomendada pela documentação oficial exatamente por não ter esse problema, coberta a seguir.

## `selectinload()`: uma segunda query com `IN`

`selectinload()` resolve o mesmo problema com uma estratégia estruturalmente diferente: em vez de um `JOIN`, emite **uma segunda query separada**, filtrando pelas chaves primárias dos objetos já carregados na primeira.

```python
from sqlalchemy.orm import selectinload

with Session(engine) as session:
    stmt = select(Cliente).options(selectinload(Cliente.pedidos)).limit(100)
    clientes = session.scalars(stmt).all()   # sem .unique() — não há duplicação aqui

    for cliente in clientes:
        for pedido in cliente.pedidos:        # já carregado, nenhum SELECT novo
            print(pedido.valor_centavos)
```

SQL gerado (duas queries, não uma só, mas nenhuma delas explode em volume):

```sql
-- Query 1: os clientes
SELECT clientes.id, clientes.nome FROM clientes LIMIT 100

-- Query 2: TODOS os pedidos dos 100 clientes carregados, de uma vez
SELECT pedidos.id, pedidos.valor_centavos, pedidos.cliente_id
FROM pedidos
WHERE pedidos.cliente_id IN (1, 2, 3, 4, 5, /* ... até 100 ids */)
```

Duas queries fixas, **independente de quantos pedidos cada cliente tem** — 100 clientes com 20 pedidos cada ainda são só 2 queries, não 100, e a segunda query retorna exatamente 2.000 linhas de `Pedido`, sem nenhum dado de `Cliente` duplicado nelas. É por isso que **`selectinload()` é a escolha default recomendada para relações `one-to-many` e `many-to-many`**: paga o custo de uma segunda query (ainda infinitamente melhor que N queries), mas sem o problema de explosão de linhas do `joinedload()`.

### `subqueryload()`: a estratégia mais antiga, hoje de nicho

`subqueryload()` também resolve N+1 com uma segunda query, mas usando uma **subquery correlacionada** (reexecutando a query original, sem `LIMIT`/`OFFSET`, como filtro) em vez de uma lista explícita de IDs:

```python
from sqlalchemy.orm import subqueryload

stmt = select(Cliente).options(subqueryload(Cliente.pedidos)).limit(100)
```

SQL gerado (forma aproximada — a subquery reconstrói a query original):

```sql
SELECT pedidos.id, pedidos.valor_centavos, pedidos.cliente_id, anon_1.clientes_id
FROM pedidos
JOIN (SELECT clientes.id AS clientes_id FROM clientes LIMIT 100) AS anon_1
  ON anon_1.clientes_id = pedidos.cliente_id
```

Historicamente, `subqueryload()` foi a resposta original do SQLAlchemy pra `one-to-many` antes de `selectinload()` existir. `selectinload()` (introduzido no SQLAlchemy 1.2) tornou-se preferível na maioria dos casos porque seu SQL é mais simples de entender e otimizar (`IN` sobre uma lista de IDs concretos é trivial pro otimizador do banco), enquanto o `subqueryload()` reexecuta uma subquery que pode ficar cara para consultas principais complexas com `JOIN`s próprios, `ORDER BY` não trivial, ou paginação. A documentação oficial atual recomenda `selectinload()` como padrão e reserva `subqueryload()` para casos legados ou situações específicas onde o padrão de subquery correlacionada é mensuravelmente mais rápido — algo raro o suficiente para não ser a escolha default de ninguém hoje.

### Tabela de decisão SQLAlchemy

| Estratégia | Mecanismo SQL | Queries totais | Melhor para | Cuidado |
|---|---|---|---|---|
| `joinedload()` | `LEFT OUTER JOIN`, uma query | 1 | `many-to-one`, `one-to-one` | Em `one-to-many`, duplica linhas — exige `.unique()` e pode explodir volume de dados |
| `selectinload()` | 2ª query com `WHERE id IN (...)` | 2 | `one-to-many`, `many-to-many` — escolha default | Uma query a mais mesmo quando a relação está vazia para todos os objetos |
| `subqueryload()` | 2ª query via subquery correlacionada | 2 | Casos legados/nicho onde mensuravelmente mais rápido que `selectinload` | SQL mais complexo, mais difícil de otimizar pelo banco |

## O lado Django: `select_related()` e `prefetch_related()`

Django resolve exatamente o mesmo problema, com o mesmo mapeamento conceitual de mecanismo — a diferença de nome não esconde uma diferença de ideia. Como já visto em [[04 - Django ORM — QuerySets, managers e migrations nativas|nota 04]], todo `QuerySet` é lazy por padrão; o mesmo padrão de N+1 aparece se o código acessa uma FK dentro de um loop sem eager loading:

```python
# N+1 clássico em Django
pedidos = Pedido.objects.all()[:100]     # 1 query — mas ainda não executada (lazy)

for pedido in pedidos:                    # aqui a query dos 100 pedidos executa
    print(pedido.cliente.nome)            # 1 query NOVA por iteração — 100 queries
```

### `select_related()`: JOIN, para FK e OneToOne

```python
pedidos = Pedido.objects.select_related("cliente")[:100]

for pedido in pedidos:
    print(pedido.cliente.nome)            # já carregado — 0 queries adicionais
```

`select_related()` gera um `JOIN` SQL — mecanicamente idêntico ao `joinedload()` do SQLAlchemy — e por isso tem exatamente a mesma restrição de aplicabilidade: **só funciona para `ForeignKey` e `OneToOneField`**, o lado "um" de uma relação, onde cada linha da tabela principal corresponde no máximo a uma linha relacionada. Tentar `select_related()` numa `ManyToManyField` ou numa FK reversa (o lado "muitos") não faz sentido estruturalmente — o `JOIN` produziria a mesma explosão de linhas vista em `joinedload()` sobre `one-to-many`, e o Django simplesmente não permite a chamada.

Encadeamento através de múltiplos níveis de FK funciona com `__`:

```python
pedidos = Pedido.objects.select_related("cliente__endereco")[:100]
# um JOIN duplo: pedidos → clientes → enderecos, tudo numa query
```

### `prefetch_related()`: query separada, join em Python

```python
clientes = Cliente.objects.prefetch_related("pedidos")[:100]

for cliente in clientes:
    for pedido in cliente.pedidos.all():  # já carregado — 0 queries adicionais
        print(pedido.valor_centavos)
```

SQL gerado (duas queries — Django mostra isso via `django-debug-toolbar` ou `connection.queries`, cobertos a seguir):

```sql
-- Query 1
SELECT id, nome FROM clientes LIMIT 100;

-- Query 2 — Django monta o IN automaticamente com os IDs da query 1
SELECT id, valor_centavos, cliente_id FROM pedidos
WHERE cliente_id IN (1, 2, 3, ..., 100);
```

`prefetch_related()` é mecanicamente equivalente ao `selectinload()` do SQLAlchemy: uma segunda query com `IN`, e o "join" entre as duas listas de resultado acontece em memória Python, não no banco — Django associa cada `Pedido` ao `Cliente` certo depois de trazer os dois conjuntos de dados separadamente. É a estratégia correta (e a única viável) para **`ManyToManyField`** e para o lado reverso de uma FK (`cliente.pedidos`, quando `Pedido` tem `ForeignKey(Cliente, related_name="pedidos")`) — os mesmos casos onde `joinedload`/`select_related` explodiriam em duplicação de linhas.

### Tabela de mapeamento direto SQLAlchemy ↔ Django

| SQLAlchemy | Django | Mecanismo | Serve para |
|---|---|---|---|
| `joinedload()` | `select_related()` | `JOIN`, 1 query | `many-to-one` / FK e `one-to-one` / `OneToOneField` |
| `selectinload()` | `prefetch_related()` | 2ª query com `IN`, join em Python | `one-to-many` (FK reversa) / `many-to-many` |
| `subqueryload()` | *(sem equivalente direto exposto na API pública)* | 2ª query via subquery correlacionada | Nicho — Django resolve o caso análogo internamente dentro de `prefetch_related()` |

> [!question]- Django tem algo equivalente a combinar as duas estratégias numa query só?
> Sim — as duas são encadeáveis livremente no mesmo `QuerySet`: `Pedido.objects.select_related("cliente").prefetch_related("cliente__tags")` resolve o FK `cliente` via `JOIN` e a `ManyToManyField` `tags` (que pende do lado "muitos", inacessível a `select_related`) via query separada, tudo numa única chamada fluente. O SQLAlchemy permite o mesmo com `.options(joinedload(Pedido.cliente), selectinload(Pedido.cliente).selectinload(Cliente.tags))` — cada opção de carregamento é independente e composável.

## Como detectar N+1 na prática

O maior risco do N+1 não é a existência do bug — é ele ser **invisível em código e em dev com poucos dados**, e só se manifestar como lentidão vaga em produção. Detectar cedo depende de instrumentação ativa, não de "notar que ficou lento".

### SQLAlchemy: `echo=True` e o logger `sqlalchemy.engine`

A forma mais simples, usada na abertura desta nota, é `echo=True` no `create_engine()`:

```python
from sqlalchemy import create_engine

engine = create_engine("postgresql://user:pass@localhost/db", echo=True)
# toda query executada é impressa no stdout, com parâmetros e tempo de cache
```

`echo=True` é adequado pra debugging local e scripts curtos, mas polui o log de uma aplicação real. Para produção (ou para capturar sem alterar código), a forma correta é configurar o logger Python `sqlalchemy.engine` diretamente:

```python
import logging

logging.basicConfig()
logging.getLogger("sqlalchemy.engine").setLevel(logging.INFO)
# equivalente a echo=True, mas configurável via infraestrutura de logging normal
# (nível WARNING desliga; DEBUG mostra também os resultados de linha, não só o SQL)
```

Em CI/testes, uma técnica direta é contar queries dentro de um bloco e falhar o teste se o número crescer com o tamanho dos dados:

```python
from sqlalchemy import event

contador = {"queries": 0}

@event.listens_for(engine, "before_cursor_execute")
def contar(conn, cursor, statement, parameters, context, executemany):
    contador["queries"] += 1

# ... roda o código sob teste ...
assert contador["queries"] <= 2, f"Esperava 2 queries, rodou {contador['queries']}"
```

Esse padrão — instrumentar o número de queries e travar um teto fixo em teste — é o jeito mais robusto de prevenir uma regressão futura de N+1: mesmo que ninguém leia o log manualmente, o teste falha assim que alguém reintroduzir um acesso lazy dentro de um loop.

Vale quantificar por que N+1 dói tanto em produção e quase nada em dev. Cada query, além do tempo de execução em si (frequentemente sub-milissegundo para um `SELECT` por chave primária com índice), paga um custo fixo de round-trip de rede entre a aplicação e o banco — em uma rede local de desenvolvimento, esse custo é irrisório (frações de milissegundo, às vezes mascarado ainda mais por o banco e a aplicação rodarem na mesma máquina); em produção, com o banco numa instância separada (frequentemente em outra zona de disponibilidade, adicionando latência de rede real), esse custo fixo por round-trip pode ser de 1 a 5ms mesmo em condições saudáveis. Uma query que "só" leva 0.2ms de execução ainda paga o round-trip inteiro. Multiplicado por 100 (ou 1.000, em uma paginação maior ou um relatório sem paginação), o tempo total do endpoint passa a ser dominado não pela complexidade das queries individuais, mas pelo **número** delas — e é exatamente esse número que cresce sem aviso, de forma proporcional ao tamanho da resposta, e não ao esforço de escrita do código. É esse descolamento entre "código simples de escrever" e "custo que cresce linearmente com o volume" que faz N+1 ser, na prática, o bug de performance mais comum reportado em serviços Python com ORM em produção — mais comum, inclusive, que índice de banco faltando, porque índice faltando ainda aparece em `EXPLAIN` de uma query só; N+1 só aparece olhando o número total de queries de um request inteiro.

### Django: `django-debug-toolbar`, `connection.queries`, contagem em teste

**`django-debug-toolbar`** é a ferramenta padrão pra desenvolvimento local: um painel injetado nas páginas renderizadas em modo debug, mostrando o número total de queries do request, o SQL de cada uma, tempo de execução, e sinalizando visualmente queries duplicadas/similares — o indicador mais direto de N+1 (uma mesma query, com parâmetros diferentes, repetida dezenas de vezes na lista é o padrão-assinatura do problema).

```python
# settings.py (ambiente de dev)
INSTALLED_APPS += ["debug_toolbar"]
MIDDLEWARE += ["debug_toolbar.middleware.DebugToolbarMiddleware"]
INTERNAL_IPS = ["127.0.0.1"]
```

Para inspeção programática (scripts, shell, ou testes fora do painel web), `django.db.connection.queries` guarda a lista bruta de SQL executado durante a sessão de debug (exige `DEBUG=True`, ou reset manual do contador entre chamadas):

```python
from django.db import connection, reset_queries
from django.conf import settings

settings.DEBUG = True
reset_queries()

pedidos = list(Pedido.objects.select_related("cliente")[:100])
for pedido in pedidos:
    _ = pedido.cliente.nome

print(len(connection.queries))   # deveria ser 1 — se for 101, o select_related não pegou
```

Em testes automatizados, o Django oferece um assertion nativo pra exatamente esse propósito — `assertNumQueries`, um context manager que falha o teste se o número de queries dentro do bloco não bater com o esperado:

```python
from django.test import TestCase

class TestListaPedidos(TestCase):
    def test_lista_pedidos_nao_tem_n_mais_1(self):
        with self.assertNumQueries(2):  # 1 pedidos + 1 prefetch de cliente(s)
            pedidos = list(Pedido.objects.select_related("cliente")[:100])
            for pedido in pedidos:
                _ = pedido.cliente.nome
```

`assertNumQueries` é o equivalente Django direto ao padrão de contador via `event.listens_for` mostrado para SQLAlchemy acima — a mesma ideia (travar um teto fixo de queries em teste) implementada como cidadão de primeira classe do framework, sem precisar de instrumentação manual.

> [!question]- Por que 100 pedidos com `select_related` ainda pode dar mais de 1 query?
> `select_related()` sozinho não elimina N+1 se o loop também acessa uma relação **diferente**, não coberta por aquele `select_related`. `Pedido.objects.select_related("cliente")` resolve `pedido.cliente` numa query só, mas se o mesmo loop também acessa `pedido.itens.all()` (uma FK reversa/`ManyToMany`), essa segunda relação precisa do próprio `prefetch_related("itens")` — cada relação acessada dentro do loop precisa da sua própria estratégia de eager loading, e esquecer uma delas reintroduz N+1 parcial só para aquela relação específica.

## Armadilhas comuns

> [!warning] `joinedload()`/`select_related()` numa relação `one-to-many` sem perceber a duplicação
> **O que acontece:** aplicar `joinedload()` (SQLAlchemy) a uma relação onde o lado "muitos" tem muitos registros gera um `JOIN` que multiplica linhas — o SQLAlchemy detecta e exige `.unique()`, mas o custo de rede/processamento do volume duplicado já foi pago; em Django, `select_related()` numa `ManyToManyField` nem sequer é permitido pela API, então esse erro específico aparece só do lado SQLAlchemy — mas o raciocínio errado ("vou usar JOIN pra tudo") é o mesmo dos dois lados. **Por quê:** `JOIN` produz uma linha por combinação, não uma linha por objeto do lado "um" — em `one-to-many`, isso significa N linhas redundantes por objeto principal, onde N é o número de filhos. **Como evitar:** usar `selectinload()`/`prefetch_related()` para qualquer relação onde o lado acessado pode ter múltiplos registros relacionados; reservar `joinedload()`/`select_related()` estritamente para `many-to-one`/`one-to-one`.

> [!warning] `prefetch_related()` custando uma query extra mesmo quando não necessário
> **O que acontece:** aplicar `prefetch_related("relacao")` num `QuerySet` cujo código, na prática, nunca acessa `.relacao` — a segunda query roda de qualquer forma, buscando dados que são descartados sem uso, sem nenhum ganho de performance e com um custo real de rede pago à toa. **Por quê:** `prefetch_related()` é avaliado eagerly assim que o `QuerySet` principal é avaliado (não é lazy por relação individual) — ele não sabe, em tempo de execução, se o código que vem depois vai de fato tocar aquele atributo. **Como evitar:** aplicar eager loading (de qualquer tipo, nos dois frameworks) só nas relações que o código efetivamente acessa no caminho em questão — revisar `select_related`/`prefetch_related`/`joinedload`/`selectinload` como parte de code review sempre que a lista de campos acessados no template/serializer mudar, não só quando o endpoint é criado.

> [!warning] Resolver N+1 "manualmente" com uma query em lote e um dicionário, reinventando o que o ORM já faz
> **O que acontece:** ao perceber o N+1, o desenvolvedor busca todos os `cliente_id` únicos, faz um único `SELECT ... WHERE id IN (...)` manual, monta um dicionário `{id: cliente}`, e substitui os acessos `pedido.cliente` por buscas nesse dicionário — reimplementando exatamente o que `selectinload()`/`prefetch_related()` já fazem, com mais código, mais chance de bug (esquecer de popular a relação em memória do jeito que o ORM espera, quebrando lazy access em outros pontos) e sem os benefícios do identity map. **Por quê:** o problema costuma ser resolvido "do zero" quando o desenvolvedor não sabe que a estratégia de eager loading já existe pronta no ORM, ou não confia nela. **Como evitar:** a resposta correta a N+1 é quase sempre uma `option()`/chamada de `QuerySet` de uma linha (`selectinload`, `prefetch_related`) — se a query precisa de lógica genuinamente mais complexa que isso não cobre, vale investigar `contains_eager()` (SQLAlchemy, para quando o `JOIN` já foi escrito manualmente na query e só falta dizer ao ORM "popule a relação com essas colunas") antes de reimplementar o batching manualmente.

> [!warning] Testar a query fora do contexto real e não pegar o N+1 escondido em serialização
> **O que acontece:** um teste chama a função que busca os pedidos e verifica que ela retorna a lista certa — mas não itera sobre `pedido.cliente` dentro do teste, então o N+1 nunca dispara ali; ele só aparece quando o serializer (DRF, Pydantic, um template Django) itera a lista completa pra montar a resposta JSON/HTML, código que o teste unitário da função de busca nunca exercitou. **Por quê:** N+1 é uma propriedade do **caminho de acesso completo**, não da query isolada — a query em si sempre roda em 1 (ou 2, com eager loading) execução; o custo N aparece só quando algo itera e toca a relação, e esse "algo" muitas vezes está numa camada diferente (serialização) do código que buscou os dados. **Como evitar:** testes de N+1 (`assertNumQueries` no Django, contador de eventos no SQLAlchemy) devem envolver o **caminho de resposta completo** — a chamada HTTP ao endpoint real, não só a função de busca isolada — para capturar queries disparadas durante serialização.

## Em entrevista

N+1 é uma das perguntas de performance mais recorrentes em entrevistas backend de nível pleno/sênior com Python — testa não só se o candidato sabe o nome do problema, mas se entende o mecanismo de lazy loading por trás dele e sabe escolher entre as estratégias de correção, não só aplicar uma genérica.

> "N+1 happens when you load a list of N records and then, for each one, trigger a separate query to fetch a related object — so instead of 1 or 2 queries total, you get 1 plus N. It's invisible in code because accessing a lazy relationship looks like a normal attribute access; the query only fires when you touch it, so it's easy to write, easy to pass code review, and easy to miss in dev with small datasets — it only becomes a visible problem at production scale, where it turns into linear query growth per request. The fix is eager loading: telling the ORM upfront which related data you'll need, so it's fetched in the same round-trip or in one batched follow-up query instead of N of them. In SQLAlchemy that's `joinedload` — a single JOIN, best for many-to-one or one-to-one, because a one-to-many JOIN duplicates the parent row once per child — versus `selectinload`, which issues a second query with a WHERE IN on the primary keys, and is the right default for one-to-many and many-to-many because it doesn't blow up row count. Django's `select_related` and `prefetch_related` map onto exactly the same distinction — JOIN versus separate query — just with framework-specific names. To catch it before it ships, I turn on SQL logging in dev, or better, assert the query count in tests — `assertNumQueries` in Django, or a query-counting event listener in SQLAlchemy — so a regression fails the test instead of surfacing as latency in production."

> [!question]- E se perguntarem "por que não simplesmente sempre usar eager loading em tudo, pra nunca ter esse problema"?
> Porque eager loading tem custo mesmo quando os dados relacionados não são necessários — cada relação carregada adiante é uma query (ou um JOIN mais pesado) a mais, rodando incondicionalmente, mesmo em caminhos de código que nunca tocam aquele atributo. Carregar tudo sempre trocaria o problema de N+1 por overfetching sistemático: toda query da aplicação carregando dados que a maioria dos caminhos de código descarta sem uso. A resposta madura é eager loading **seletivo e por caminho de acesso** — cada endpoint/view declara exatamente as relações que vai efetivamente usar, nem mais nem menos — não uma política global de "sempre eager, nunca lazy".

## Como explicar em inglês

| PT | EN |
|----|----|
| N+1 (problema de N+1 queries) | N+1 (query) problem |
| carregamento adiantado/ansioso | eager loading |
| carregamento preguiçoso | lazy loading |
| explosão de linhas (do JOIN) | row explosion / row multiplication |
| duplicação de linha | row duplication |
| round-trip (de rede) | round-trip |
| chave estrangeira | foreign key |
| busca em lote | batch fetch |
| consulta correlacionada | correlated subquery |
| painel de depuração | debug toolbar |
| contagem de queries | query count |

## O que vem a seguir

Esta nota cobriu o diagnóstico e a correção de N+1 nos dois ORMs da trilha — o próximo passo natural é a correção **ficar correta sob concorrência**, não só sob volume:

- [[04 - Django ORM — QuerySets, managers e migrations nativas|04 — Django ORM]] — QuerySets lazy e a API fluente que `select_related`/`prefetch_related` estendem; leitura recomendada antes desta nota se a lazy evaluation do `QuerySet` ainda não estiver clara.
- [[02 - SQLAlchemy ORM — Session, mapped classes e relationships|02 — SQLAlchemy ORM]] — `relationship()`, lazy loading por padrão e o ciclo de vida do objeto mapeado; base direta desta nota.
- [[06 - Transações e isolamento — ACID na prática, isolation levels, deadlocks de aplicação|06 — Transações e isolamento]] — depois de garantir que uma operação faz o número certo de queries, o próximo risco é garantir que essas queries, quando modificam dados, o fazem com a atomicidade e o isolamento certos — o assunto da próxima nota do galho.
- [[index|Persistência de dados (Galho 9)]] — MOC deste galho.

## Fontes

- SQLAlchemy. *Relationship Loading Techniques*. docs.sqlalchemy.org, versão 2.0. https://docs.sqlalchemy.org/en/20/orm/queryguide/relationships.html (acessado em 2026-07-11) — `joinedload()`, `selectinload()`, `subqueryload()`, comparação oficial de estratégias e recomendação de `selectinload` como default para `one-to-many`.
- SQLAlchemy. *Engine Configuration — Configuring Logging*. docs.sqlalchemy.org, versão 2.0. https://docs.sqlalchemy.org/en/20/core/engines.html#configuring-logging (acessado em 2026-07-11) — `echo=True`, logger `sqlalchemy.engine`, níveis INFO/DEBUG.
- SQLAlchemy. *ORM Querying Guide — Joined Eager Loading*. docs.sqlalchemy.org, versão 2.0. https://docs.sqlalchemy.org/en/20/orm/queryguide/relationships.html#joined-eager-loading (acessado em 2026-07-11) — explosão de linhas em `joinedload()` sobre coleções, exigência de `.unique()`.
- Django. *QuerySet API reference — select_related()*. docs.djangoproject.com, versão 5.x. https://docs.djangoproject.com/en/5.2/ref/models/querysets/#select-related (acessado em 2026-07-11) — mecanismo de JOIN, restrição a FK/OneToOne, encadeamento com `__`.
- Django. *QuerySet API reference — prefetch_related()*. docs.djangoproject.com, versão 5.x. https://docs.djangoproject.com/en/5.2/ref/models/querysets/#prefetch-related (acessado em 2026-07-11) — segunda query com join em Python, uso com ManyToMany e FK reversa.
- Django. *django-debug-toolbar documentation*. django-debug-toolbar.readthedocs.io. https://django-debug-toolbar.readthedocs.io/ (acessado em 2026-07-11) — painel SQL, detecção visual de queries duplicadas.
- Django. *Testing tools — assertNumQueries()*. docs.djangoproject.com, versão 5.x. https://docs.djangoproject.com/en/5.2/topics/testing/tools/#django.test.TransactionTestCase.assertNumQueries (acessado em 2026-07-11) — assertion nativa de contagem de queries em teste.
- [[02 - SQLAlchemy ORM — Session, mapped classes e relationships|02 — SQLAlchemy ORM]] — nota irmã, pré-requisito direto (lazy loading e `relationship()` não são reexplicados aqui).
- [[04 - Django ORM — QuerySets, managers e migrations nativas|04 — Django ORM]] — nota irmã, pré-requisito direto (QuerySet lazy não é reexplicado aqui).

Consultado em 2026-07-11.
