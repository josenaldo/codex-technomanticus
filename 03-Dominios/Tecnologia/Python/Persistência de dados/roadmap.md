---
title: "Roadmap — Python Persistência de dados"
created: 2026-07-11
type: meta
publish: false
tags:
  - meta
  - roadmap
  - python
---

# Roadmap — Persistência de dados (galho 9)

Roadmap-folha do galho `Python/Persistência de dados`. Fase **Adepto→Magus** — SQLAlchemy, Django ORM, migrations, N+1, transações, connection pooling. Spec: [[00-Meta/specs/2026-07-09-python-trilha-design]]. EXEMPLAR de estrutura: `Python/Programação Reativa e Assíncrona/index.md` e `Python/Programação Reativa e Assíncrona/roadmap.md` (galho anterior, mesmo padrão).

Roster **não pré-cravado no spec** (só a descrição de alto nível "SQLAlchemy, Django ORM, migrations, N+1, transações") — desenhado nesta sessão seguindo o mesmo playbook dos Galhos 5, 7 e 8. Primeiro galho do bloco **"Backend e arquitetura"** (9-13) — muda de registro em relação aos galhos 1-8 (linguagem/execução): aqui o assunto é como sistemas Python reais guardam estado.

> [!success] Galho 9 completo — 8/8 notas (2026-07-11)
> A capstone fechou o galho amarrando o modelo ORM com `relationship()` nas duas direções (nota 02) + migration Alembic revisada (nota 03) + listagem de pedidos sem N+1 via `selectinload()` encadeado (nota 05) + `criar_pedido()` atômico multi-tabela com isolation level explícito, lock de linha e retry de deadlock (nota 06) + `Engine` dimensionada para produção (nota 07) numa camada de persistência de um sistema de pedidos real, rodável de ponta a ponta. Próximo da trilha: Galho 10 — Web e APIs REST.

## Tabela-resumo

| Métrica | Valor |
|---------|-------|
| Total de notas | 8 |
| ⬜ pendente | 0 |
| ✅ feita | 8 |
| 🔄 em andamento | 0 |
| % concluído | 100% |

---

## Notas

#### 01 - SQLAlchemy Core — Engine, Connection e expressão SQL
- **Estado:** ✅ feita (2026-07-11) · fase: Adepto
- **Escopo:** `create_engine`, `Connection`/`Engine` (pool por baixo, adiantado aqui e aprofundado na nota 07), a linguagem de expressão SQL do SQLAlchemy (`select`/`insert`/`update`/`delete` como objetos Python, não strings), `Table`/`MetaData` (definição imperativa de schema), execução de queries cruas com segurança (bind parameters, por que NUNCA fazer f-string de SQL — SQL injection). Base pra nota 02 (ORM é construído em cima do Core).
- **Resultado:** 452 linhas / 5137 palavras. Abre com um endpoint de busca vulnerável a SQL injection via f-string (payload `' OR '1'='1` e variante UNION), depois desenvolve Engine-como-fábrica/pool, Connection, `select`/`insert`/`update`/`delete` como objetos encadeáveis, `Table`/`MetaData`, e por que bind parameters fecham a injeção por construção (com allowlist para identificadores dinâmicos). 3 diagramas Mermaid (pool, ataque via bind parameter, comparativo de caminhos).

#### 02 - SQLAlchemy ORM — Session, mapped classes e relationships
- **Estado:** ✅ feita (2026-07-11) · fase: Adepto→Magus
- **Escopo:** `DeclarativeBase`/mapped classes (SQLAlchemy 2.0 style com `Mapped[]`/`mapped_column`), `Session` (unit of work, identity map, por que Session não é thread-safe), `relationship()` (one-to-many/many-to-many, `back_populates`), ciclo de vida de um objeto (transient/pending/persistent/detached). Referencia a nota 01 (Core) sem repetir.
- **Resultado:** 448 linhas / 5317 palavras. Abre com `DetachedInstanceError` ao acessar uma relationship lazy depois que a sessão fechou; desenvolve `DeclarativeBase`/`Mapped[]`/`mapped_column`, Session como Unit of Work + Identity Map (com o mecanismo real de por que dois `session.get()` retornam o mesmo objeto), por que Session não é thread-safe (paralelo com threading do Galho 7), `relationship()` one-to-many e many-to-many com tabela de associação, `back_populates` vs `backref`, e o ciclo transient→pending→persistent→detached com 3 formas de evitar o bug de abertura. 3 diagramas Mermaid (identity map, ER da relationship, stateDiagram do ciclo de vida).

#### 03 - Migrations com Alembic — versionamento de schema
- **Estado:** ✅ feita (2026-07-11) · fase: Adepto
- **Escopo:** por que migrations versionadas importam (schema como código, não como estado mutável do banco de produção), `alembic init`/`revision --autogenerate`/`upgrade`/`downgrade`, o que o autogenerate NÃO detecta bem (rename de coluna, mudanças de tipo sutis) e por que revisar a migration gerada é obrigatório, migrations em CI/CD (menção breve, aprofundado em Operação/Galho 17 futuro).
- **Resultado:** 399 linhas / 4992 palavras. Abre com rename de coluna via `--autogenerate` virando `DROP COLUMN`+`ADD COLUMN` — perda silenciosa de 40 mil nomes de usuário em produção; desenvolve por que schema de produção não é recriável (analogia "Git do schema"), estrutura gerada por `alembic init` (`alembic.ini`/`env.py`/`versions/`), mecânica do diff via reflection, `upgrade`/`downgrade`/cadeia `down_revision`, modo online vs. offline, flags `compare_type`/`compare_server_default`, migrations vazias como sinal de `MetaData` desalinhado, correção manual do rename via `alter_column(new_column_name=...)`, e outros pontos cegos do autogenerate (mudança de tipo com perda de precisão, migração de dados associada). Menção breve a CI/CD e ao padrão expand/contract. 2 diagramas Mermaid (fluxo revision→upgrade→banco, cadeia de migrations encadeadas).

#### 04 - Django ORM — QuerySets, managers e migrations nativas
- **Estado:** ✅ feita (2026-07-11) · fase: Adepto→Magus
- **Escopo:** `Model`/`Manager`, `QuerySet` como lazy/preguiçoso (só executa ao iterar/avaliar), API fluente (`filter`/`exclude`/`annotate`/`aggregate`), migrations nativas do Django (`makemigrations`/`migrate`, contraste direto com Alembic da nota 03 — Django integra migrations ao ORM, SQLAlchemy não), quando escolher Django ORM vs. SQLAlchemy (tabela de decisão: acoplamento ao framework vs. flexibilidade).
- **Resultado:** 478 linhas / 6062 palavras. Abre com um `QuerySet` de pedidos pendentes guardado numa variável e reavaliado (`.count()`) antes/depois de um lote de cobrança — o segundo `.count()` reflete o estado atual do banco, não o snapshot do início, expondo a lazy evaluation; desenvolve `Manager`/`Model.objects` (com manager customizado), `QuerySet` como descrição acumulada e imutável por encadeamento, a lista oficial do que dispara avaliação (iteração/`list()`/fatiamento com passo/`bool()`/`len()`, com nota sobre fatiamento simples NÃO avaliar e cache de resultados por instância), API fluente (`filter`/`exclude`, `Q` para OR/NOT, `F` para comparar/incrementar colunas atomicamente no banco evitando condição de corrida, `annotate` vs `aggregate`), menção breve a `select_related`/`prefetch_related` linkando pra nota 05, migrations nativas (`makemigrations`/`migrate` comparando contra histórico em disco em vez de reflection contra o banco — contraste explícito com Alembic, incluindo a detecção interativa de rename e sua ressalva de não ser garantia total), e tabela de decisão SQLAlchemy vs Django ORM (acoplamento ao framework, controle fino, produtividade). 2 diagramas Mermaid (fluxo de avaliação lazy, comparação Alembic-reflection vs Django-histórico-de-migrations).

#### 05 - N+1 e eager loading — joinedload/selectinload vs select_related/prefetch_related
- **Estado:** ✅ feita (2026-07-11) · fase: Magus
- **Escopo:** o problema de N+1 com bug-driven opening real (loop que acessa `.relationship` de cada objeto, disparando 1 query por iteração), `joinedload`/`selectinload`/`subqueryload` no SQLAlchemy (quando cada um faz sentido), `select_related`/`prefetch_related` no Django (JOIN vs. query separada), como DETECTAR N+1 na prática (SQL logging, `django-debug-toolbar`, `sqlalchemy.engine` echo).
- **Resultado:** 436 linhas / 5222 palavras. Abre com um endpoint de listagem de 100 pedidos disparando 101 queries (1 + 100, uma por `pedido.cliente` lazy) — SQL log real via `echo=True`; desenvolve `joinedload()` (1 JOIN, ótimo em many-to-one/one-to-one, explosão de linhas em one-to-many exigindo `.unique()`), `selectinload()` (2ª query com `IN`, default recomendado pra one-to-many/many-to-many) e `subqueryload()` (legado, subquery correlacionada); mapeia direto pra `select_related()`/`prefetch_related()` do Django (JOIN vs. query separada + join em Python), referenciando a nota 04 pro QuerySet lazy sem repetir; cobre detecção via `echo=True`/logger `sqlalchemy.engine`, contador de queries via `event.listens_for`, `django-debug-toolbar`, `connection.queries` e `assertNumQueries`. 2 diagramas Mermaid (sequenceDiagram do N+1, flowchart da explosão de linhas do JOIN).

#### 06 - Transações e isolamento — ACID na prática, isolation levels, deadlocks de aplicação
- **Estado:** ✅ feita (2026-07-11) · fase: Magus
- **Escopo:** ACID revisitado com exemplos Python reais (não teoria abstrata — já coberto genericamente em Fundamentos/Teoria da Computação se existir, aqui é a aplicação), isolation levels (`READ COMMITTED`/`REPEATABLE READ`/`SERIALIZABLE`) e o que cada um previne/permite (dirty read, non-repeatable read, phantom read), `session.begin()`/context manager de transação, deadlock de aplicação (duas transações competindo por locks em ordem diferente — paralelo direto ao deadlock de threading do Galho 7 nota 02, referenciar sem repetir).
- **Resultado:** 481 linhas / 5132 palavras. Abre com transferência bancária sem transação (débito commitado isoladamente, exceção antes do crédito → dinheiro desaparece) vs. com `session.begin()` (atômico); percorre ACID com exemplo Python por letra (Atomicity via bloco transacional, Consistency via `CheckConstraint` barrando bug de saldo negativo mesmo sem validação em Python, Isolation como núcleo da nota, Durability via WAL/fsync conceitual); desenvolve os 4 isolation levels do padrão SQL com exemplo de código pra cada anomalia (dirty read impossível de reproduzir em PostgreSQL, non-repeatable read reproduzível contra `READ COMMITTED` default, phantom read com nota sobre `REPEATABLE READ` do Postgres ser mais forte que o mínimo do padrão SQL); contrasta `session.begin()`/`begin_nested()` do SQLAlchemy com `transaction.atomic()` do Django (savepoints aninháveis); ressalva honesta sobre SQLite serializar escritas por padrão, mascarando as anomalias; deadlock de transação como paralelo direto do deadlock de threading do Galho 7 nota 02 (referenciado, não reexplicado) — duas UPDATEs em ordem invertida, banco detecta e mata uma transação com erro real, mitigado por ordem consistente de acesso (sort por id) e retry com backoff exponencial checando a mensagem específica de deadlock. 2 diagramas Mermaid (progressão dos 4 isolation levels, sequenceDiagram do deadlock de transação com detecção e vítima).

#### 07 - Connection pooling e performance em produção
- **Estado:** ✅ feita (2026-07-11) · fase: Magus
- **Escopo:** por que abrir uma conexão TCP+auth nova por request é caro, `QueuePool` do SQLAlchemy (`pool_size`/`max_overflow`/`pool_timeout`/`pool_recycle`), pooling no Django (`CONN_MAX_AGE`), pooler externo (PgBouncer) e quando ele é necessário (muitos processos/workers cada um com seu próprio pool — problema clássico de Gunicorn com múltiplos workers), monitoramento básico de pool esgotado.
- **Resultado:** 359 linhas / 6040 palavras. Abre com um serviço de checkout caindo sexta às 17h com `QueuePool limit ... timeout` — Gunicorn com 8 workers, cada um com `pool_size=20`+`max_overflow=10`, multiplicando para até 240 conexões contra um Postgres com `max_connections=100` padrão; desenvolve o mecanismo de custo de handshake TCP+TLS+autenticação (sequenceDiagram), `QueuePool` parâmetro a parâmetro (`pool_size`, `max_overflow`, `pool_timeout`, `pool_recycle`, `pool_pre_ping`) referenciando a Engine-como-fábrica da nota 01 sem repetir, `CONN_MAX_AGE`/`CONN_HEALTH_CHECKS` do Django contrastando com o modelo per-processo do SQLAlchemy, o problema N workers × M conexões com diagrama comparativo antes/depois de PgBouncer, os 3 modos do PgBouncer (session/transaction/statement) com config `.ini` de exemplo, monitoramento via `pg_stat_activity`/`event.listens_for`/`SHOW POOLS`, um cálculo de dimensionamento worked-example (orçamento do banco ÷ processos no pico) e uma seção breve de pooling assíncrono (`AsyncEngine`/`AsyncAdaptedQueuePool`, ligação com o Galho 7 de asyncio). 3 diagramas Mermaid (handshake, fluxo de checkout do pool com pre-ping/timeout, comparativo com/sem PgBouncer).

#### 08 - Capstone — projetando a camada de persistência de um serviço real
- **Estado:** ✅ feita (2026-07-11) · fase: Magus
- **Escopo:** recapitula o galho projetando a camada de dados de um serviço real (ex: sistema de pedidos) — modelagem SQLAlchemy ORM (nota 02) + migration inicial via Alembic (nota 03) + query com eager loading correto evitando N+1 (nota 05) + transação atômica multi-tabela com isolation level explícito (nota 06) + configuração de pool pra produção (nota 07). Cenário prático integrador, não introduz conceito novo raso.
- **Resultado:** 630 linhas / 6308 palavras. Abre com um sistema de pedidos de e-commerce (`Cliente`/`Produto`/`Pedido`/`ItemPedido`) percorrendo cinco versões incrementais, cada uma corrigindo o bug de abertura de uma nota anterior do galho; desenvolve o modelo com `relationship()` nas duas direções (`back_populates`) e `ItemPedido` como tabela de associação com atributos próprios (preço congelado no momento da venda), a migration inicial Alembic gerada por `--autogenerate` com revisão manual da ordem de `create_table` e `server_default`, `listar_pedidos_do_cliente()` com `selectinload(Pedido.itens).selectinload(ItemPedido.produto)` colapsando 201 queries em 3, `criar_pedido()` atômica com `REPEATABLE READ` + `SELECT FOR UPDATE` + ordem consistente de lock por `produto_id` + retry em `OperationalError` de deadlock, e `create_engine()` com `pool_size`/`max_overflow`/`pool_recycle`/`pool_pre_ping` dimensionados contra o orçamento de conexões do banco, com nota sobre quando PgBouncer entra no desenho. 2 diagramas Mermaid (erDiagram do modelo, sequenceDiagram da transação de criação de pedido). Fecha o galho e aponta para o Galho 10 (Web e APIs REST) e o Galho 13 (Repository/Unit of Work formalizando os padrões que já apareceram organicamente aqui).

## Decisões e fronteiras registradas

- Teoria de banco de dados genérica (normalização, índices, CAP) → fica em Fundamentos/System Design se existir; aqui é só a aplicação Python.
- Deadlock de threading (Galho 7 nota 02) → não repetido; nota 06 faz o paralelo conceitual com deadlock de transação.
- Repository/Unit of Work como padrão de arquitetura formal → Galho 13 (Arquitetura e Design Patterns); aqui os conceitos aparecem organicamente (Session já É uma Unit of Work) mas sem nomear/formalizar o padrão.
- CI/CD de migrations, deploy → Operação (galho futuro 17), só mencionado brevemente aqui.
