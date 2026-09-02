---
title: "Capstone — projetando a camada de persistência de um serviço real"
created: 2026-07-11
type: concept
status: complete
fase: magus
tags:
  - python
  - sqlalchemy
  - persistência
  - capstone
publish: true
aliases:
  - "Capstone Galho 9 Python"
  - "camada de persistência de pedidos"
  - "Fechamento Persistência de dados"
---

# Capstone — projetando a camada de persistência de um serviço real

> [!abstract] TL;DR
> Esta nota fecha o Galho 9 construindo, peça por peça, a camada de dados que só faz sentido depois de ler as sete notas anteriores: o sistema de pedidos de um e-commerce simples — `Cliente`, `Produto`, `Pedido`, `ItemPedido` — modelado com [[02 - SQLAlchemy ORM — Session, mapped classes e relationships|mapped classes e `relationship()`]] (nota 02), versionado com uma [[03 - Migrations com Alembic — versionamento de schema|migration Alembic]] gerada por `--autogenerate` e revisada à mão (nota 03), consultado com [[05 - N+1 e eager loading — joinedload-selectinload vs select_related-prefetch_related|`selectinload()`]] para listar pedidos com itens e produtos sem os N+1 queries que a nota 05 diagnosticou, escrito através de uma função `criar_pedido()` que roda como [[06 - Transações e isolamento — ACID na prática, isolation levels, deadlocks de aplicação|uma única transação atômica multi-tabela]] com isolation level explícito e retry em caso de deadlock (nota 06), e servido por um `Engine` configurado com os [[07 - Connection pooling e performance em produção|parâmetros de pool]] que sustentam esse tráfego em produção (nota 07). Nenhuma peça deste desenho é conceito novo: as sete notas anteriores já ensinaram cada mecanismo isoladamente; esta nota só os amarra na ordem em que uma camada de persistência real precisa deles — schema primeiro, depois leitura eficiente, depois escrita segura, depois a infraestrutura que aguenta carga.

## O cenário: uma camada de pedidos amarra o galho inteiro

Um serviço interno de e-commerce precisa de uma camada de persistência para o fluxo mais crítico do sistema: um cliente compra um ou mais produtos, e o pedido resultante debita o estoque desses produtos — tudo isso sob concorrência real, com dezenas de clientes finalizando compras ao mesmo tempo. É o tipo de domínio que parece trivial em um protótipo de fim de semana e revela, um por um, todos os problemas que este galho passou sete notas explicando:

- A primeira versão modela `Cliente`/`Pedido`/`ItemPedido`/`Produto` como classes soltas, sem `relationship()` nem chave estrangeira declarada no ORM — o bug de abertura da [[02 - SQLAlchemy ORM — Session, mapped classes e relationships|nota 02]] — e descobre em produção que `pedido.itens` não existe como atributo navegável, só como uma query manual escrita à mão em cada lugar que precisa dela.
- A segunda versão corrige o modelo mas cria o schema do banco rodando `Base.metadata.create_all()` direto em produção — sem nenhuma migration versionada, o bug de abertura da [[03 - Migrations com Alembic — versionamento de schema|nota 03]] — e não tem como evoluir o schema depois sem apagar e recriar tabelas manualmente, arriscando dados reais.
- A terceira versão tem schema e migrations corretos, mas a tela de "meus pedidos" lista 50 pedidos com um loop que acessa `pedido.cliente.nome` e `item.produto.nome` para cada item — o N+1 que a [[05 - N+1 e eager loading — joinedload-selectinload vs select_related-prefetch_related|nota 05]] diagnosticou, disparando centenas de queries numa tela que deveria custar duas ou três.
- A quarta versão corrige a leitura mas escreve o pedido em passos soltos — insere o `Pedido`, depois cada `ItemPedido`, depois faz `UPDATE` no estoque de cada `Produto`, cada passo com seu próprio commit implícito — e sob carga, dois clientes comprando o último item do mesmo produto ao mesmo tempo às vezes vendem o mesmo item duas vezes: exatamente a ausência de atomicidade multi-tabela que a [[06 - Transações e isolamento — ACID na prática, isolation levels, deadlocks de aplicação|nota 06]] descreveu.
- A quinta versão corrige a transação mas cria uma `Engine` nova a cada request (ou usa os defaults do `create_engine()` sem pensar em `pool_size`) e, na primeira sexta-feira de tráfego alto, cai com `QueuePool limit ... timeout` — o cenário de abertura exato da [[07 - Connection pooling e performance em produção|nota 07]].

Cada uma dessas versões corrigidas corresponde a uma nota deste galho. O sistema desta capstone é a sexta versão — a que já nasce com as cinco correções embutidas, porque não há razão nenhuma para descobrir cada uma delas de novo em produção depois de já tê-las estudado aqui.

```mermaid
erDiagram
    CLIENTE ||--o{ PEDIDO : "faz"
    PEDIDO ||--|{ ITEM_PEDIDO : "contém"
    PRODUTO ||--o{ ITEM_PEDIDO : "referenciado em"

    CLIENTE {
        int id PK
        string nome
        string email UK
    }
    PEDIDO {
        int id PK
        int cliente_id FK
        datetime criado_em
        string status
    }
    ITEM_PEDIDO {
        int id PK
        int pedido_id FK
        int produto_id FK
        int quantidade
        numeric preco_unitario
    }
    PRODUTO {
        int id PK
        string nome
        numeric preco
        int estoque
    }
```

## Etapa 1: o modelo — mapped classes e as duas direções de `relationship()`

A base de qualquer camada de persistência ORM é a mesma da [[02 - SQLAlchemy ORM — Session, mapped classes e relationships|nota 02]]: classes mapeadas com `DeclarativeBase`, colunas tipadas via `Mapped[]`/`mapped_column()`, e `relationship()` declarando como as tabelas se conectam. Este sistema tem exatamente as duas direções que a nota 02 ensinou: **one-to-many** (`Pedido` → `ItemPedido`, um pedido tem vários itens) e **many-to-one** (`Pedido` → `Cliente`, cada pedido pertence a um cliente só — a mesma relação vista do lado inverso).

```python
"""models.py — modelo ORM do sistema de pedidos."""

from __future__ import annotations

from datetime import datetime
from decimal import Decimal

from sqlalchemy import ForeignKey, Numeric, String, UniqueConstraint
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Base(DeclarativeBase):
    pass


class Cliente(Base):
    __tablename__ = "clientes"

    id: Mapped[int] = mapped_column(primary_key=True)
    nome: Mapped[str] = mapped_column(String(120))
    email: Mapped[str] = mapped_column(String(255))

    pedidos: Mapped[list["Pedido"]] = relationship(back_populates="cliente")

    __table_args__ = (UniqueConstraint("email", name="uq_clientes_email"),)


class Produto(Base):
    __tablename__ = "produtos"

    id: Mapped[int] = mapped_column(primary_key=True)
    nome: Mapped[str] = mapped_column(String(200))
    preco: Mapped[Decimal] = mapped_column(Numeric(10, 2))
    estoque: Mapped[int] = mapped_column(default=0)


class Pedido(Base):
    __tablename__ = "pedidos"

    id: Mapped[int] = mapped_column(primary_key=True)
    cliente_id: Mapped[int] = mapped_column(ForeignKey("clientes.id"))
    criado_em: Mapped[datetime] = mapped_column(default=datetime.utcnow)
    status: Mapped[str] = mapped_column(String(20), default="confirmado")

    # many-to-one: cada Pedido tem UM Cliente
    cliente: Mapped["Cliente"] = relationship(back_populates="pedidos")

    # one-to-many: cada Pedido tem VÁRIOS ItemPedido
    itens: Mapped[list["ItemPedido"]] = relationship(
        back_populates="pedido", cascade="all, delete-orphan"
    )


class ItemPedido(Base):
    __tablename__ = "itens_pedido"

    id: Mapped[int] = mapped_column(primary_key=True)
    pedido_id: Mapped[int] = mapped_column(ForeignKey("pedidos.id"))
    produto_id: Mapped[int] = mapped_column(ForeignKey("produtos.id"))
    quantidade: Mapped[int]
    preco_unitario: Mapped[Decimal] = mapped_column(Numeric(10, 2))

    pedido: Mapped["Pedido"] = relationship(back_populates="itens")
    produto: Mapped["Produto"] = relationship()
```

Dois detalhes que a nota 02 já justificou e que este modelo aplica sem repetir a explicação:

- `back_populates` em ambos os lados de cada relação (`Cliente.pedidos` ↔ `Pedido.cliente`, `Pedido.itens` ↔ `ItemPedido.pedido`) — a forma explícita que a nota 02 preferiu sobre `backref`, porque cada lado da relação fica visível e navegável direto na classe onde é definido, sem "aparecer magicamente" do outro lado.
- `preco_unitario` é copiado para dentro de `ItemPedido` no momento da venda, em vez de o item apontar só para `Produto.preco` e ler o preço atual toda vez. Essa é uma decisão de modelagem deliberada e comum em sistemas de pedidos reais: o preço de um item vendido não pode mudar retroativamente se o preço do produto mudar depois — congelar o valor no momento da transação é o que torna o histórico de pedidos auditável.

> [!question]- Por que `ItemPedido` é uma tabela própria em vez de uma coluna de lista dentro de `Pedido`?
> Porque a relação entre pedido e produto carrega dados que não pertencem nem ao pedido nem ao produto isoladamente — a quantidade comprada e o preço no momento da venda. Isso é o padrão clássico de **tabela de associação com atributos próprios** (diferente da tabela de associação pura many-to-many que a nota 02 mostrou para relações sem dados extras): `ItemPedido` não é só "a ligação entre Pedido e Produto", é uma entidade com identidade e dados próprios — por isso vira uma mapped class completa, com sua própria chave primária, e não um `Table` de associação anônimo.

## Etapa 2: a migration inicial — schema como código, não como estado mutável

Com o modelo declarado, o schema real do banco nasce de uma migration Alembic gerada por `--autogenerate` e revisada à mão — exatamente o fluxo que a [[03 - Migrations com Alembic — versionamento de schema|nota 03]] ensinou, incluindo a desconfiança saudável do que o autogenerate detecta bem (colunas novas, tabelas novas, foreign keys) e do que ele não detecta de forma confiável (renomes, mudanças de tipo).

```bash
alembic revision --autogenerate -m "cria tabelas iniciais de pedidos"
```

O comando compara o `MetaData` das classes em `models.py` contra o estado atual do banco (vazio, na primeira migration) e gera um arquivo em `alembic/versions/`. Resumido — a versão completa inclui os `ForeignKeyConstraint` e o `UniqueConstraint` do email, omitidos aqui por brevidade:

```python
"""cria tabelas iniciais de pedidos

Revision ID: a1b2c3d4e5f6
Revises:
Create Date: 2026-07-11 09:00:00
"""

from alembic import op
import sqlalchemy as sa

revision = "a1b2c3d4e5f6"
down_revision = None


def upgrade() -> None:
    op.create_table(
        "clientes",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("nome", sa.String(120), nullable=False),
        sa.Column("email", sa.String(255), nullable=False),
        sa.UniqueConstraint("email", name="uq_clientes_email"),
    )
    op.create_table(
        "produtos",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("nome", sa.String(200), nullable=False),
        sa.Column("preco", sa.Numeric(10, 2), nullable=False),
        sa.Column("estoque", sa.Integer, nullable=False, server_default="0"),
    )
    op.create_table(
        "pedidos",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("cliente_id", sa.Integer, sa.ForeignKey("clientes.id"), nullable=False),
        sa.Column("criado_em", sa.DateTime, nullable=False),
        sa.Column("status", sa.String(20), nullable=False, server_default="confirmado"),
    )
    op.create_table(
        "itens_pedido",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("pedido_id", sa.Integer, sa.ForeignKey("pedidos.id"), nullable=False),
        sa.Column("produto_id", sa.Integer, sa.ForeignKey("produtos.id"), nullable=False),
        sa.Column("quantidade", sa.Integer, nullable=False),
        sa.Column("preco_unitario", sa.Numeric(10, 2), nullable=False),
    )


def downgrade() -> None:
    op.drop_table("itens_pedido")
    op.drop_table("pedidos")
    op.drop_table("produtos")
    op.drop_table("clientes")
```

Duas revisões manuais que a nota 03 já ensinou a fazer por hábito, antes de rodar `upgrade`:

- Conferir a ordem de `create_table`: `clientes` e `produtos` antes de `pedidos`, `pedidos` antes de `itens_pedido` — o autogenerate normalmente acerta essa ordem de dependência de foreign keys sozinho, mas é o tipo de coisa que vale olhar, porque um `create_table` fora de ordem quebra o `upgrade` com um erro de foreign key para uma tabela que ainda não existe.
- `server_default="0"` em `estoque` e `server_default="confirmado"` em `status` — sem isso, se a tabela já tivesse linhas (não é o caso desta migration inicial, mas seria em uma migration futura que adiciona uma coluna `NOT NULL` a uma tabela populada), o `ADD COLUMN` falharia por violar a restrição `NOT NULL` nas linhas existentes. Registrar o hábito aqui, mesmo não sendo estritamente necessário nesta migration zero, é o tipo de disciplina que a nota 03 recomendou manter constante.

```bash
alembic upgrade head
```

## Etapa 3: listando pedidos sem N+1 — `selectinload()` nas duas relações

A tela mais comum de qualquer sistema de pedidos é a listagem: "meus pedidos", com o nome do cliente (opcional, se for uma visão administrativa) e, para cada pedido, os itens com o nome do produto. Escrita ingenuamente, essa listagem é o cenário de abertura exato da [[05 - N+1 e eager loading — joinedload-selectinload vs select_related-prefetch_related|nota 05]]: 1 query para os pedidos, mais 1 query por pedido para carregar `itens` (lazy), mais 1 query por item para carregar `produto` (lazy) — para 50 pedidos com 3 itens cada, isso é 1 + 50 + 150 = **201 queries** para uma tela que deveria custar 3.

```python
from sqlalchemy import select
from sqlalchemy.orm import selectinload

def listar_pedidos_do_cliente(session: Session, cliente_id: int) -> list[Pedido]:
    stmt = (
        select(Pedido)
        .where(Pedido.cliente_id == cliente_id)
        .options(
            selectinload(Pedido.itens).selectinload(ItemPedido.produto),
        )
        .order_by(Pedido.criado_em.desc())
    )
    return list(session.scalars(stmt))
```

A escolha de `selectinload()` — em vez de `joinedload()` — nas duas relações não é arbitrária: ambas são **one-to-many** ou passam por uma cadeia que termina em one-to-many (`Pedido.itens` é one-to-many; `ItemPedido.produto` é many-to-one, mas está aninhada dentro de uma relação one-to-many). A nota 05 já explicou por que `joinedload()` em relações one-to-many multiplica linhas — um `LEFT JOIN` de 1 pedido com 3 itens retorna 3 linhas repetindo os dados do pedido, exigindo `.unique()` para desduplicar — enquanto `selectinload()` faz uma segunda query com `WHERE pedido_id IN (...)` que não sofre essa explosão. Resultado: **3 queries no total**, não 3 por pedido — uma para os pedidos, uma para todos os itens de todos os pedidos encontrados (via `IN`), uma para todos os produtos referenciados por esses itens (via `IN` novamente) — independente de haver 5 ou 500 pedidos na página.

```mermaid
sequenceDiagram
    participant App
    participant DB as Banco

    App->>DB: SELECT * FROM pedidos WHERE cliente_id = ?
    DB-->>App: 50 pedidos
    App->>DB: SELECT * FROM itens_pedido WHERE pedido_id IN (...)
    DB-->>App: todos os itens desses 50 pedidos
    App->>DB: SELECT * FROM produtos WHERE id IN (...)
    DB-->>App: todos os produtos referenciados
    Note over App,DB: 3 queries totais, não 201 — independente de N pedidos
```

> [!warning] Conferir com `echo=True` antes de confiar na contagem
> A nota 05 insistiu nisso e vale repetir aqui: a forma de saber que a listagem realmente ficou em 3 queries — e não em 4, 5, ou de volta a 201 por um `selectinload()` esquecido em algum nível de aninhamento — é rodar a query com `create_engine(..., echo=True)` (ou o listener de `sqlalchemy.engine` da nota 05) num teste de integração e contar as linhas de SQL emitidas. Confiar de olho no código, sem medir, é exatamente o hábito que deixa um N+1 novo passar despercebido quando alguém adiciona uma relação nova à listagem meses depois.

## Etapa 4: `criar_pedido()` — a transação atômica multi-tabela

Esta é a operação de escrita mais crítica do sistema: criar um pedido precisa inserir um `Pedido`, inserir um ou mais `ItemPedido`, e decrementar o `estoque` de cada `Produto` envolvido — **tudo ou nada**. Se o estoque não for suficiente para qualquer item, a operação inteira precisa falhar sem deixar nem o pedido nem nenhum decremento de estoque parcialmente commitado. É exatamente o cenário que abriu a [[06 - Transações e isolamento — ACID na prática, isolation levels, deadlocks de aplicação|nota 06]] — uma transferência bancária sem transação perde dinheiro; um pedido sem transação vende estoque que não existe.

```python
from dataclasses import dataclass
from decimal import Decimal

from sqlalchemy import select
from sqlalchemy.exc import OperationalError
from sqlalchemy.orm import Session


@dataclass
class ItemPedidoInput:
    produto_id: int
    quantidade: int


class EstoqueInsuficiente(Exception):
    def __init__(self, produto_id: int, disponivel: int, solicitado: int) -> None:
        self.produto_id = produto_id
        super().__init__(
            f"produto {produto_id}: estoque {disponivel} insuficiente para {solicitado}"
        )


def criar_pedido(
    session: Session, cliente_id: int, itens: list[ItemPedidoInput]
) -> Pedido:
    """Cria um pedido debitando estoque, atômico e com isolation level explícito."""
    max_tentativas = 3
    for tentativa in range(1, max_tentativas + 1):
        try:
            with session.begin():
                session.connection(
                    execution_options={"isolation_level": "REPEATABLE READ"}
                )

                pedido = Pedido(cliente_id=cliente_id)
                session.add(pedido)

                # ordem consistente por produto_id — evita deadlock (nota 06)
                for item_input in sorted(itens, key=lambda i: i.produto_id):
                    produto = session.execute(
                        select(Produto)
                        .where(Produto.id == item_input.produto_id)
                        .with_for_update()
                    ).scalar_one()

                    if produto.estoque < item_input.quantidade:
                        raise EstoqueInsuficiente(
                            produto.id, produto.estoque, item_input.quantidade
                        )

                    produto.estoque -= item_input.quantidade
                    pedido.itens.append(
                        ItemPedido(
                            produto_id=produto.id,
                            quantidade=item_input.quantidade,
                            preco_unitario=produto.preco,
                        )
                    )
                # commit implícito ao sair do `with session.begin()` sem exceção
            return pedido
        except OperationalError as exc:
            if "deadlock detected" in str(exc.orig).lower() and tentativa < max_tentativas:
                logger.warning(
                    "deadlock detectado criando pedido (tentativa %d/%d) — retry",
                    tentativa, max_tentativas,
                )
                continue
            raise
    raise RuntimeError("esgotou tentativas após deadlocks sucessivos")
```

Cada peça deste bloco é uma peça que a nota 06 já justificou isoladamente:

- **`with session.begin():`** é o bloco transacional explícito da nota 06 — tudo dentro dele commita junto no final ou desfaz junto se qualquer exceção subir, incluindo `EstoqueInsuficiente`. Não há `session.commit()` explícito porque `session.begin()` como context manager já faz isso ao sair sem exceção.
- **`isolation_level="REPEATABLE READ"`** explícito na conexão, em vez de aceitar o `READ COMMITTED` default do PostgreSQL, é a decisão que a nota 06 chamou de "escolher o nível certo para a invariante que importa": aqui a invariante é "o estoque que eu li no início da transação continua válido até eu decrementá-lo" — `REPEATABLE READ` garante que uma leitura repetida da mesma linha dentro da transação não muda, o que fecha a janela onde duas transações concorrentes leem o mesmo `estoque` desatualizado e ambas decidem que há saldo suficiente.
- **`.with_for_update()`** soma um lock explícito de linha por cima do isolation level — a query `SELECT ... FOR UPDATE` trava a linha do `Produto` até o fim da transação, forçando qualquer outra transação que tente o mesmo `SELECT FOR UPDATE` naquele produto a esperar em vez de prosseguir com um valor de estoque que está prestes a mudar. É a combinação isolation level + lock explícito que a nota 06 recomendou para invariantes financeiras/de estoque, mais forte do que confiar só no isolation level.
- **Ordenar `itens` por `produto_id` antes do loop** é a mitigação de deadlock que a nota 06 tirou do paralelo direto com deadlock de threading (Galho 7, nota 02): se duas transações concorrentes compram produtos sobrepostos em ordens diferentes (transação A trava produto 5 depois pede o 3; transação B trava o 3 depois pede o 5), cada uma espera a outra soltar um lock que a outra não vai soltar — deadlock circular. Ordenar consistentemente por `produto_id` em toda transação que toca múltiplos produtos elimina essa ordem invertida por construção.
- **O `except OperationalError` com retry** é a segunda camada de defesa da nota 06, para quando a ordenação consistente não é suficiente sozinha (ou quando o banco detecta um deadlock por outro motivo): o PostgreSQL detecta deadlocks ativamente e mata uma das transações envolvidas com uma mensagem específica (`deadlock detected`); a resposta correta não é propagar esse erro para o usuário como uma falha genérica, é tentar de novo — a transação inteira, do zero, porque o estado em memória (o `produto.estoque` já lido) pode estar desatualizado depois do rollback.

```mermaid
sequenceDiagram
    participant Cliente as criar_pedido()
    participant Tx as Transação (REPEATABLE READ)
    participant DB as PostgreSQL

    Cliente->>Tx: with session.begin()
    Tx->>DB: INSERT INTO pedidos (...)
    loop para cada item, ordenado por produto_id
        Tx->>DB: SELECT estoque FROM produtos WHERE id=? FOR UPDATE
        DB-->>Tx: estoque atual (linha travada)
        alt estoque insuficiente
            Tx-->>Cliente: raise EstoqueInsuficiente
            Note over Tx,DB: rollback automático — nada commitado
        else estoque suficiente
            Tx->>DB: UPDATE produtos SET estoque = estoque - ?
            Tx->>DB: INSERT INTO itens_pedido (...)
        end
    end
    Tx->>DB: COMMIT
    Note over Tx,DB: se deadlock detectado → OperationalError → retry do zero
```

> [!question]- Por que não usar `Produto.estoque -= quantidade` direto num `UPDATE` atômico (`F()`-style) em vez de ler, checar em Python e escrever?
> Essa é uma alternativa real e, em outros contextos, a nota 04 (Django ORM) recomendou exatamente esse padrão com `F()` para incrementos/decrementos simples sem condição de corrida (`Produto.objects.filter(id=x).update(estoque=F("estoque") - 1)`). A diferença aqui é que a operação **não é só decrementar** — é decrementar **condicionalmente** ("só se houver estoque suficiente, senão aborte o pedido inteiro"). Um `UPDATE ... SET estoque = estoque - ? WHERE estoque >= ?` resolveria o decremento condicional em uma única instrução atômica, mas exigiria checar `rowcount == 0` depois para saber se a condição falhou — funciona, mas empurra a lógica de negócio para dentro de uma cláusula `WHERE`, dificultando a extensão (por exemplo, se o sistema depois precisar registrar *por que* o estoque estava insuficiente, com qual valor). A leitura com `SELECT FOR UPDATE` seguida de checagem em Python é mais legível e mais fácil de estender, ao custo de uma query a mais — uma troca razoável para uma operação de checkout, que não é hot-path de milhares de requisições por segundo como um contador de likes.

## Etapa 5: a `Engine` pronta para produção

Toda essa camada de dados só sustenta tráfego real se a `Engine` que a alimenta estiver configurada com os parâmetros de pool que a [[07 - Connection pooling e performance em produção|nota 07]] ensinou — não os defaults do `create_engine()`, que servem bem para desenvolvimento local mas sub-dimensionam ou super-dimensionam silenciosamente um serviço em produção.

```python
from sqlalchemy import create_engine

engine = create_engine(
    "postgresql+psycopg://app:senha@db.interno:5432/pedidos",
    pool_size=10,        # conexões mantidas abertas por worker, prontas para uso
    max_overflow=5,      # extras permitidas sob pico — total 15 por worker
    pool_timeout=30,     # segundos esperando conexão livre antes de TimeoutError
    pool_recycle=1800,   # descarta conexões com mais de 30min (evita firewall/timeout do servidor)
    pool_pre_ping=True,  # testa com SELECT 1 antes de emprestar — evita conexão morta
)
```

O dimensionamento de `pool_size`/`max_overflow` segue o cálculo que a nota 07 chamou de worked-example: orçamento total do banco (`max_connections` do PostgreSQL, tipicamente 100 por padrão) dividido pelo número de processos/workers que vão manter pool aberto ao mesmo tempo. Um serviço rodando atrás de Gunicorn com 4 workers, cada um com `pool_size=10 + max_overflow=5 = 15`, soma até 60 conexões no pico — dentro do orçamento de 100, com folga para outras conexões administrativas e para um segundo serviço que também bate no mesmo banco. Multiplicar `pool_size` sem fazer essa conta — o mesmo erro do cenário de abertura da nota 07 (8 workers × 30 conexões = 240 contra um limite de 100) — é a causa mais comum de `QueuePool limit ... timeout` em produção.

> [!info] Quando `PgBouncer` entra no desenho
> Se este serviço crescer para rodar em múltiplos processos/workers (ou múltiplas instâncias do serviço, cada uma com sua própria `Engine`) ao ponto de o cálculo acima não fechar contra o `max_connections` do banco — mesmo com `pool_size` bem dimensionado por processo, a soma de todos os processos ainda estoura o orçamento — a resposta que a nota 07 descreveu é um pooler externo como `PgBouncer` em modo `transaction`, multiplexando centenas de conexões lógicas dos workers sobre uma dezena de conexões físicas reais contra o Postgres. Este sistema de pedidos, do tamanho descrito aqui (um serviço, poucos workers), não justifica essa peça extra ainda — mas a decisão de quando introduzi-la é exatamente a mesma conta de "conexões físicas necessárias vs. disponíveis" que a nota 07 ensinou a fazer antes de adicionar infraestrutura nova.

## O sistema completo

Juntando as cinco etapas — modelo com `relationship()` nas duas direções (1), migration Alembic revisada (2), listagem sem N+1 via `selectinload()` (3), `criar_pedido()` atômico com isolation level e retry de deadlock (4), `Engine` dimensionada para produção (5) — o desenho da camada de persistência fica assim, de ponta a ponta:

```python
"""persistencia.py — camada de persistência do sistema de pedidos, completa."""

from __future__ import annotations

import logging
from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal

from sqlalchemy import ForeignKey, Numeric, String, UniqueConstraint, create_engine, select
from sqlalchemy.exc import OperationalError
from sqlalchemy.orm import (
    DeclarativeBase,
    Mapped,
    Session,
    mapped_column,
    relationship,
    selectinload,
)

logger = logging.getLogger("persistencia")


class Base(DeclarativeBase):
    pass


class Cliente(Base):
    __tablename__ = "clientes"
    id: Mapped[int] = mapped_column(primary_key=True)
    nome: Mapped[str] = mapped_column(String(120))
    email: Mapped[str] = mapped_column(String(255))
    pedidos: Mapped[list["Pedido"]] = relationship(back_populates="cliente")
    __table_args__ = (UniqueConstraint("email", name="uq_clientes_email"),)


class Produto(Base):
    __tablename__ = "produtos"
    id: Mapped[int] = mapped_column(primary_key=True)
    nome: Mapped[str] = mapped_column(String(200))
    preco: Mapped[Decimal] = mapped_column(Numeric(10, 2))
    estoque: Mapped[int] = mapped_column(default=0)


class Pedido(Base):
    __tablename__ = "pedidos"
    id: Mapped[int] = mapped_column(primary_key=True)
    cliente_id: Mapped[int] = mapped_column(ForeignKey("clientes.id"))
    criado_em: Mapped[datetime] = mapped_column(default=datetime.utcnow)
    status: Mapped[str] = mapped_column(String(20), default="confirmado")
    cliente: Mapped["Cliente"] = relationship(back_populates="pedidos")
    itens: Mapped[list["ItemPedido"]] = relationship(
        back_populates="pedido", cascade="all, delete-orphan"
    )


class ItemPedido(Base):
    __tablename__ = "itens_pedido"
    id: Mapped[int] = mapped_column(primary_key=True)
    pedido_id: Mapped[int] = mapped_column(ForeignKey("pedidos.id"))
    produto_id: Mapped[int] = mapped_column(ForeignKey("produtos.id"))
    quantidade: Mapped[int]
    preco_unitario: Mapped[Decimal] = mapped_column(Numeric(10, 2))
    pedido: Mapped["Pedido"] = relationship(back_populates="itens")
    produto: Mapped["Produto"] = relationship()


@dataclass
class ItemPedidoInput:
    produto_id: int
    quantidade: int


class EstoqueInsuficiente(Exception):
    def __init__(self, produto_id: int, disponivel: int, solicitado: int) -> None:
        self.produto_id = produto_id
        super().__init__(
            f"produto {produto_id}: estoque {disponivel} insuficiente para {solicitado}"
        )


def criar_pedido(
    session: Session, cliente_id: int, itens: list[ItemPedidoInput]
) -> Pedido:
    max_tentativas = 3
    for tentativa in range(1, max_tentativas + 1):
        try:
            with session.begin():
                session.connection(
                    execution_options={"isolation_level": "REPEATABLE READ"}
                )
                pedido = Pedido(cliente_id=cliente_id)
                session.add(pedido)
                for item_input in sorted(itens, key=lambda i: i.produto_id):
                    produto = session.execute(
                        select(Produto)
                        .where(Produto.id == item_input.produto_id)
                        .with_for_update()
                    ).scalar_one()
                    if produto.estoque < item_input.quantidade:
                        raise EstoqueInsuficiente(
                            produto.id, produto.estoque, item_input.quantidade
                        )
                    produto.estoque -= item_input.quantidade
                    pedido.itens.append(
                        ItemPedido(
                            produto_id=produto.id,
                            quantidade=item_input.quantidade,
                            preco_unitario=produto.preco,
                        )
                    )
            return pedido
        except OperationalError as exc:
            if "deadlock detected" in str(exc.orig).lower() and tentativa < max_tentativas:
                logger.warning(
                    "deadlock detectado criando pedido (tentativa %d/%d) — retry",
                    tentativa, max_tentativas,
                )
                continue
            raise
    raise RuntimeError("esgotou tentativas após deadlocks sucessivos")


def listar_pedidos_do_cliente(session: Session, cliente_id: int) -> list[Pedido]:
    stmt = (
        select(Pedido)
        .where(Pedido.cliente_id == cliente_id)
        .options(selectinload(Pedido.itens).selectinload(ItemPedido.produto))
        .order_by(Pedido.criado_em.desc())
    )
    return list(session.scalars(stmt))


def criar_engine_producao(url: str):
    return create_engine(
        url,
        pool_size=10,
        max_overflow=5,
        pool_timeout=30,
        pool_recycle=1800,
        pool_pre_ping=True,
    )
```

Rodar este sistema contra um banco de teste real — popular `clientes`/`produtos` de exemplo, chamar `criar_pedido()` de duas threads simultâneas comprando o mesmo produto com estoque baixo, e observar tanto o `SELECT FOR UPDATE` serializando as duas transações quanto (com estoque insuficiente) a segunda chamada recebendo `EstoqueInsuficiente` de forma limpa, sem debitar duas vezes — é a forma mais direta de ver as cinco peças funcionando juntas. Ativar `echo=True` na `Engine` de teste confirma a contagem de queries de `listar_pedidos_do_cliente()`: 3 queries totais, não uma por pedido.

## Armadilhas comuns

> [!warning] Modelar `relationship()` só em uma direção
> **O que acontece:** `Pedido.itens` funciona, mas não existe forma direta de, a partir de um `ItemPedido`, navegar de volta ao `Pedido` sem uma query manual — código que precisa dos dois sentidos duplica lógica de busca. **Por quê:** `relationship()` não é automaticamente bidirecional; cada direção precisa da sua própria declaração, ligadas por `back_populates`. **Como evitar:** declarar `relationship(back_populates=...)` nos dois lados de toda relação que o código vai navegar em ambas as direções — o padrão que a [[02 - SQLAlchemy ORM — Session, mapped classes e relationships|nota 02]] estabeleceu.

> [!warning] Confiar cegamente no `--autogenerate` para renomes de coluna
> **O que acontece:** renomear uma coluna no modelo Python e rodar `--autogenerate` gera um `DROP COLUMN` + `ADD COLUMN` — perda silenciosa de dados em produção, o bug de abertura exato da [[03 - Migrations com Alembic — versionamento de schema|nota 03]]. **Por quê:** o autogenerate detecta diffs por reflection estrutural (nomes de coluna, tipos), não por intenção — ele não sabe que "a coluna X virou Y" é um rename, só vê "X sumiu, Y apareceu". **Como evitar:** revisar toda migration gerada antes de rodar `upgrade`; renomes usam `op.alter_column(new_column_name=...)` manual, nunca o autogenerate cru.

> [!warning] Esquecer `selectinload()` em um nível aninhado de relação
> **O que acontece:** `selectinload(Pedido.itens)` sozinho resolve o N+1 dos itens, mas cada item ainda dispara uma query lazy para `item.produto` — o N+1 se move um nível mais fundo, sem desaparecer. **Por quê:** `selectinload()` (como `joinedload()`) só carrega antecipadamente a relação nomeada explicitamente; relações aninhadas exigem encadeamento explícito. **Como evitar:** `selectinload(Pedido.itens).selectinload(ItemPedido.produto)` — a mesma sintaxe encadeada que a [[05 - N+1 e eager loading — joinedload-selectinload vs select_related-prefetch_related|nota 05]] descreveu para relações aninhadas.

> [!warning] Decrementar estoque sem `SELECT FOR UPDATE` nem isolation level explícito
> **O que acontece:** duas transações concorrentes leem o mesmo `estoque` desatualizado, ambas decidem que há saldo suficiente, ambas decrementam — o produto vende mais unidades do que existiam. **Por quê:** sob `READ COMMITTED` (default do PostgreSQL), cada `SELECT` dentro da transação enxerga o valor commitado mais recente no momento daquele `SELECT` específico, não um snapshot fixo do início da transação — duas leituras concorrentes antes de qualquer `UPDATE` podem ver o mesmo valor. **Como evitar:** `REPEATABLE READ` (ou mais forte) combinado com `SELECT ... FOR UPDATE` explícito na linha que vai ser decrementada — o padrão que a [[06 - Transações e isolamento — ACID na prática, isolation levels, deadlocks de aplicação|nota 06]] recomendou para invariantes de estoque/financeiras.

## Em entrevista

A pergunta "como você desenharia a camada de dados de um sistema de pedidos" (ou variantes — "como você garantiria que o estoque nunca fica negativo", "como você evitaria que essa listagem fique lenta") testa se a pessoa distingue as quatro camadas independentes que compõem uma persistência de produção real, ou se trata "usar um ORM" como uma resposta única e suficiente.

> "I'd start with the model: mapped classes with `relationship()` in both directions where the code needs to navigate both ways — `Pedido.cliente` many-to-one, `Pedido.itens` one-to-many — with `back_populates` making both sides explicit rather than relying on an implicit `backref`. Schema changes go through Alembic migrations generated by `--autogenerate` but always reviewed by hand, because autogenerate is reliable for new tables and columns but not for renames or subtle type changes — it'll happily turn a rename into a silent `DROP COLUMN` if you let it. For reads, the order listing is the classic N+1 trap: looping over orders and touching `order.items` and `item.product` lazily turns one query into hundreds. `selectinload()`, chained across both relationship levels, collapses that back down to a fixed small number of queries regardless of how many orders are on the page. For the write side — creating an order that debits stock — atomicity across multiple tables is non-negotiable: a single transaction, an explicit isolation level strong enough for the invariant that matters (`REPEATABLE READ` plus `SELECT FOR UPDATE` for a stock check, not just the READ COMMITTED default), consistent lock ordering across products to avoid deadlocks, and a retry loop for the deadlocks that happen anyway under real concurrency. And none of it survives contact with production traffic without a properly sized connection pool — `pool_size` and `max_overflow` budgeted against how many processes are sharing the database's connection limit, not left at defaults. Every one of these is a separate concern, and skipping any one of them is where a system that works in a demo starts failing under real load."

Uma pergunta de acompanhamento comum: **"o que muda se o sistema crescer para múltiplos serviços escrevendo no mesmo banco?"** — a resposta sênior reconhece a fronteira sem tentar espremer tudo dentro de mais transações: nesse ponto, formalizar os padrões de acesso a dados que já apareceram organicamente aqui — `Session` como Unit of Work já é, na prática, o padrão que o Galho 13 (Arquitetura e Design Patterns) nomeia e formaliza como **Repository** e **Unit of Work** explícitos — e decisões de particionamento/sharding de dados entram no território de System Design, não mais de persistência de um único serviço.

> [!question]- O entrevistador insiste: "por que não usar `SERIALIZABLE` em toda transação, já que é o nível mais seguro?"
> Porque "mais seguro" tem custo real: `SERIALIZABLE` no PostgreSQL detecta conflitos de serialização otimisticamente e aborta transações com um erro específico que a aplicação precisa tratar com retry — sob alta concorrência, isso significa uma taxa de abort maior e mais retries do que `REPEATABLE READ` com locks explícitos e bem direcionados. A resposta sênior escolhe o isolation level mínimo que fecha a invariante que realmente importa — aqui, "o estoque lido continua válido até ser decrementado", que `REPEATABLE READ` + `SELECT FOR UPDATE` já garante — em vez de aplicar o nível mais forte disponível por precaução genérica em todo lugar, o que a nota 06 chamou de trade-off central de isolation levels: mais garantia sempre custa mais contenção.

## Como explicar em inglês

> A real order-persistence layer isn't one decision, it's four layered ones. The model comes first — mapped classes with explicit relationships in both directions, so the code can navigate an order to its customer and back without ad-hoc queries. Schema changes are version-controlled through migrations, generated automatically but always reviewed, because autogeneration is good at spotting new tables and columns and bad at recognizing intent like a rename. Reads need eager loading chained across every relationship level the view actually touches, or the classic N+1 problem just moves one level deeper instead of disappearing. Writes that touch multiple tables — creating an order while debiting stock — need to be a single atomic transaction with an isolation level and locking strategy matched to the invariant that actually matters, plus consistent lock ordering and a retry path for the deadlocks that happen anyway under real concurrency. And all of it sits on a connection pool sized against how many processes are sharing the database's connection budget, not left at framework defaults. Skip any one of these four and the system still works in a demo — it just fails the first time it meets real concurrent load.

| PT | EN |
|---|---|
| tabela de associação com atributos | association table with attributes |
| congelar o preço no momento da venda | freeze the price at time of sale |
| decremento condicional de estoque | conditional stock decrement |
| lock de linha explícito | explicit row lock |
| ordem consistente de acesso | consistent lock ordering |
| orçamento de conexões do banco | database connection budget |
| pooler externo | external pooler |
| padrão de acesso a dados | data access pattern |
| camada de persistência | persistence layer |
| tudo ou nada | all-or-nothing |

## Fechamento do Galho 9 — Persistência de dados

Esta é a última nota do Galho 9. Recapitulando o que as oito notas cobriram juntas:

1. [[01 - SQLAlchemy Core — Engine, Connection e expressão SQL|01 — SQLAlchemy Core]] abriu o galho pela camada mais baixa — `Engine`, `Connection`, a linguagem de expressão SQL (`select`/`insert`/`Table`/`MetaData`) — e mostrou por que bind parameters fecham SQL injection por construção, a base sobre a qual o ORM inteiro é construído.
2. [[02 - SQLAlchemy ORM — Session, mapped classes e relationships|02 — SQLAlchemy ORM]] subiu para o ORM propriamente dito — `DeclarativeBase`/`Mapped[]`, `Session` como Unit of Work + Identity Map, o ciclo de vida transient→pending→persistent→detached — e é a peça que esta capstone aplica diretamente no modelo `Cliente`/`Pedido`/`ItemPedido`/`Produto`.
3. [[03 - Migrations com Alembic — versionamento de schema|03 — Migrations com Alembic]] tratou schema como código versionado, não como estado mutável do banco de produção — a migration inicial desta capstone segue esse fluxo exato, `--autogenerate` seguido de revisão manual.
4. [[04 - Django ORM — QuerySets, managers e migrations nativas|04 — Django ORM]] deu o outro grande caminho do ecossistema — `QuerySet` lazy, migrations nativas integradas ao framework — como contraste explícito ao SQLAlchemy, útil para quem escolhe entre os dois em um projeto novo.
5. [[05 - N+1 e eager loading — joinedload-selectinload vs select_related-prefetch_related|05 — N+1 e eager loading]] entregou `selectinload()`/`joinedload()` (e os equivalentes Django) que esta capstone aplica direto na listagem de pedidos, colapsando 201 queries em 3.
6. [[06 - Transações e isolamento — ACID na prática, isolation levels, deadlocks de aplicação|06 — Transações e isolamento]] entregou isolation levels, locks explícitos e a mitigação de deadlock por ordem consistente — o núcleo da função `criar_pedido()` atômica desta capstone.
7. [[07 - Connection pooling e performance em produção|07 — Connection pooling]] entregou o dimensionamento de `pool_size`/`max_overflow` contra o orçamento de conexões do banco, e quando um pooler externo como PgBouncer entra no desenho — a `Engine` de produção que sustenta este sistema inteiro.
8. Esta nota fechou amarrando as cinco peças (modelo, migration, leitura sem N+1, escrita atômica, pool de produção) numa camada de persistência real, sem introduzir mecanismo novo, só integração.

Juntas, essas oito notas formam **como sistemas Python reais guardam estado em produção** — não mais "o que é uma query" (isso é pré-requisito, assumido desde a nota 01), mas "como você desenha, versiona, lê eficientemente e escreve com segurança uma camada de dados que sobrevive a carga real e concorrência real".

## O que vem a seguir

Esta capstone deliberadamente não introduziu nada além do que as sete notas anteriores já tinham ensinado — nenhum framework web completo, nenhum padrão de arquitetura formal, nenhum mecanismo novo de banco de dados. O que falta para um serviço de pedidos genuinamente completo pertence a outros galhos da trilha:

- **[[03-Dominios/Tecnologia/Python/Web e APIs REST/index|Galho 10 — Web e APIs REST]]** (próximo) — este sistema expõe `criar_pedido()` e `listar_pedidos_do_cliente()` como funções Python puras; um serviço real os expõe via endpoints HTTP, com serialização, validação de entrada e tratamento de erro HTTP apropriado para `EstoqueInsuficiente` — o degrau natural para quem já sabe persistir dados e precisa servi-los pela rede.
- [[03-Dominios/Tecnologia/Python/Arquitetura e Design Patterns/index|Galho 13 — Arquitetura e Design Patterns]] — `Session` já se comportou, ao longo deste galho, como uma Unit of Work informal; `criar_pedido()` e `listar_pedidos_do_cliente()` já se comportam como funções de um Repository informal. O Galho 13 vai nomear e formalizar esses dois padrões — `Repository` e `Unit of Work` como abstrações explícitas, desacoplando a lógica de negócio do SQLAlchemy diretamente — em cima exatamente do que foi construído aqui, sem reensinar transações ou N+1.
- [[03-Dominios/Tecnologia/Python/Programação Reativa e Assíncrona/index|Galho 8 — Programação Reativa e Assíncrona]] — se este sistema precisasse de um driver assíncrono (`AsyncEngine`/`AsyncSession`) para servir um framework ASGI, a nota 07 daquele galho já mencionou brevemente o pooling assíncrono; a integração completa com um endpoint `async def` pertence ao Galho 10.
- [[03-Dominios/Tecnologia/Python/index|Trilha Python]] — MOC da trilha.

## Fontes

- SQLAlchemy documentation. *ORM Quick Start*, *Relationship Configuration*, *Using SELECT Statements to Load ORM Entities*. docs.sqlalchemy.org, versão 2.0. https://docs.sqlalchemy.org/en/20/orm/quickstart.html (acessado em 2026-07-11)
- SQLAlchemy documentation. *Transactions and Connection Management*, *Setting Transaction Isolation Levels including DBAPI Autocommit*. docs.sqlalchemy.org, versão 2.0. https://docs.sqlalchemy.org/en/20/orm/session_transaction.html (acessado em 2026-07-11)
- Alembic documentation. *Auto Generating Migrations*, *Tutorial*. alembic.sqlalchemy.org. https://alembic.sqlalchemy.org/en/latest/autogenerate.html (acessado em 2026-07-11)
- PostgreSQL Global Development Group. *Explicit Locking*, *Transaction Isolation*. postgresql.org, documentação oficial, versão 17. https://www.postgresql.org/docs/current/explicit-locking.html (acessado em 2026-07-11)
- Fowler, M. *Patterns of Enterprise Application Architecture* — capítulos sobre Unit of Work e Repository. Addison-Wesley, 2002.
- Percival, H.; Gregory, B. *Architecture Patterns with Python* — capítulos sobre Repository e Unit of Work aplicados especificamente a SQLAlchemy. O'Reilly, 2020. https://www.cosmicpython.com/ (acessado em 2026-07-11)
- [[01 - SQLAlchemy Core — Engine, Connection e expressão SQL|01]], [[02 - SQLAlchemy ORM — Session, mapped classes e relationships|02]], [[03 - Migrations com Alembic — versionamento de schema|03]], [[04 - Django ORM — QuerySets, managers e migrations nativas|04]], [[05 - N+1 e eager loading — joinedload-selectinload vs select_related-prefetch_related|05]], [[06 - Transações e isolamento — ACID na prática, isolation levels, deadlocks de aplicação|06]], [[07 - Connection pooling e performance em produção|07]] — as sete notas irmãs deste galho, cada uma fonte primária dos mecanismos amarrados nesta capstone.
- [[03-Dominios/Tecnologia/Python/Programação Reativa e Assíncrona/08 - Capstone — web scraper assíncrono de produção|Programação Reativa e Assíncrona 08 — Capstone]] — o capstone irmão do Galho 8, mesmo padrão de fechamento, cenário integrador anterior nesta mesma trilha.

Consultado em 2026-07-11.
