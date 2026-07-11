---
title: "Connection pooling e performance em produção"
created: 2026-07-11
type: concept
status: complete
fase: Magus
publish: true
tags:
  - python
  - sqlalchemy
  - persistência
  - produção
aliases:
  - "QueuePool"
  - "connection pooling"
  - "PgBouncer"
  - "CONN_MAX_AGE"
---

# Connection pooling e performance em produção

> [!abstract] TL;DR
> Abrir uma conexão nova a cada request é caro — handshake TCP, negociação TLS e autenticação no banco custam múltiplas rodadas de ida-e-volta, um overhead que a aplicação paga de novo a cada query se não reusar conexões. A `Engine` do SQLAlchemy já resolve isso dentro de **um processo** com um `QueuePool`: `pool_size` (conexões mantidas abertas), `max_overflow` (extras sob pico), `pool_timeout` (quanto esperar antes de desistir) e `pool_recycle` (descarta conexões velhas antes que o banco/firewall as mate silenciosamente). O Django faz o equivalente com `CONN_MAX_AGE` (conexões persistentes entre requests em vez de uma nova a cada request, dentro do mesmo processo). O problema real de produção aparece um nível acima: com Gunicorn/uWSGI rodando **N processos worker**, cada um com seu próprio pool de **M** conexões, o banco vê até **N×M** conexões simultâneas — e `max_connections` do Postgres é 100 por padrão. É fácil estourar esse limite sem que nenhum pool individual pareça mal configurado. A saída é um pooler **externo** ao processo da aplicação — PgBouncer é o padrão de fato para Postgres — que multiplexa muitas conexões de aplicação sobre poucas conexões reais ao banco, em modo `session`, `transaction` (o mais comum) ou `statement`. Pool esgotado se manifesta como timeout esperando uma conexão livre — o sintoma e o diagnóstico (contagem de conexões ativas, `pool_timeout` estourando) fecham esta nota.

## O bug que abre esta nota

Sexta-feira, 17h, um serviço de checkout começa a devolver erro 500 em rajadas. Os logs mostram a mesma exceção se repetindo, vinda de dentro do SQLAlchemy:

```
sqlalchemy.exc.TimeoutError: QueuePool limit of size 20 overflow 10 reached,
connection timed out, timeout 30
```

O time de plantão olha a configuração da aplicação e não encontra nada óbvio errado — a `Engine` foi criada com um `pool_size=20` e `max_overflow=10` que parecem generosos, folga de sobra para qualquer request individual. O que ninguém tinha calculado é que o serviço roda atrás de **Gunicorn com 8 workers**, e cada worker é um **processo Python separado**, com sua **própria Engine, e portanto seu próprio pool**. O número de conexões que a aplicação pode abrir contra o banco não é 20+10=30 — é `8 × (20+10) = 240` no pico, porque cada um dos 8 processos tem seu pool independente, sem coordenação entre si.

O PostgreSQL de produção estava configurado com `max_connections = 100` (o valor padrão de fábrica, nunca revisado). Sob tráfego normal, os workers não usam o pool inteiro simultaneamente e tudo funciona. Na sexta-feira à tarde, um pico de tráfego de fim de expediente faz vários workers atingirem `pool_size` ao mesmo tempo e começarem a abrir conexões de overflow — e o banco, que já estava perto do limite por causa de outras aplicações compartilhando a mesma instância, simplesmente recusa novas conexões com `FATAL: too many connections for role "app_user"` (do lado do Postgres) ou, do lado do cliente, o timeout de `pool_timeout` esperando uma conexão que nunca é liberada de volta ao pool porque o próprio banco está travado.

> [!bug] O que está quebrado, em uma frase
> `pool_size` e `max_overflow` controlam quantas conexões **um processo** pode abrir — multiplicar esse número pela quantidade de **processos worker** é aritmética obrigatória antes de configurar qualquer pool em produção, e "cada worker com seu próprio pool" é exatamente o cenário em que um pooler externo como PgBouncer deixa de ser opcional.

O resto desta nota desenvolve, nessa ordem, por que conexões são caras de abrir, como o `QueuePool` do SQLAlchemy amortiza esse custo dentro de um processo, o equivalente no Django, e por que — a partir de um certo número de processos worker — um pooler externo passa a ser a única forma sensata de não estourar o limite do banco.

## Por que abrir uma conexão nova é caro

Uma conexão de banco de dados não é "grátis até ser usada" — abri-la envolve várias rodadas de comunicação em sequência, cada uma pagando a latência de rede (mesmo dentro de um datacenter, ida-e-volta não é zero) mais o processamento em ambas as pontas:

```mermaid
sequenceDiagram
    participant App as Aplicação
    participant DB as Banco de dados

    App->>DB: SYN (handshake TCP)
    DB-->>App: SYN-ACK
    App->>DB: ACK
    Note over App,DB: conexão TCP estabelecida
    App->>DB: negociação TLS (se aplicável)
    DB-->>App: certificado, cipher suite
    Note over App,DB: canal criptografado pronto
    App->>DB: credenciais (usuário/senha ou certificado)
    DB->>DB: valida credenciais, checa permissões
    DB-->>App: autenticado
    Note over App,DB: SÓ AGORA a primeira query pode rodar
    App->>DB: SELECT ...
    DB-->>App: resultado
```

Cada seta nesse diagrama é uma ida-e-volta de rede. O handshake TCP sozinho já são três mensagens; TLS adiciona sua própria negociação (troca de certificado, definição de cipher); e a autenticação no banco — validar usuário/senha, carregar permissões e configurações da sessão — é trabalho de CPU e, dependendo do mecanismo (`scram-sha-256` no Postgres, por exemplo), envolve mais de uma rodada de desafio-resposta. Nenhum desses passos acontece antes de a aplicação poder executar a primeira query de verdade — o "custo de entrada" é pago inteiro, todo santo request, se a conexão é aberta e fechada a cada vez.

O mecanismo importa mais do que qualquer número específico de milissegundos (que varia com rede, hardware, configuração de TLS e mecanismo de autenticação, e não deveria ser citado sem medir no ambiente real): o ponto estrutural é que esse custo é **fixo por conexão**, não por query, e sob carga ele se acumula de forma proporcional ao número de requests. Um endpoint que abre-executa-fecha uma conexão a cada chamada paga o handshake completo em cada chamada; o mesmo endpoint reusando uma conexão já aberta paga esse custo **uma vez**, e todas as queries subsequentes pulam direto para "enviar SQL, receber resultado". É exatamente esse reuso que um **pool de conexões** proporciona: manter um conjunto de conexões já autenticadas, abertas e ociosas, prontas para ser emprestadas — o custo de abertura é pago quando a conexão entra no pool, não a cada vez que é usada.

> [!question]- Por que não simplesmente abrir uma conexão no bootstrap e nunca fechar, sem pool nenhum?
> Uma conexão só resolve concorrência zero — o momento em que duas requisições HTTP chegam ao mesmo tempo (comum, mesmo num único processo com I/O assíncrono, e trivial sob WSGI multi-thread) exige duas conexões simultâneas, porque uma conexão de banco não pode ser usada por duas queries concorrentes ao mesmo tempo sem embaralhar resultados. O pool existe justamente para dar a cada thread/coroutine/handler uma conexão dedicada enquanto ela precisa, e devolvê-la ao conjunto assim que termina — nem uma conexão única e compartilhada (quebra sob concorrência), nem uma conexão nova por request (paga o custo de handshake toda vez).

## `QueuePool`: o pool padrão do SQLAlchemy

A [[01 - SQLAlchemy Core — Engine, Connection e expressão SQL|nota 01]] já estabeleceu que `create_engine()` cria uma fábrica com um pool por baixo — esta seção aprofunda exatamente esse pool. Para a maioria dos bancos (Postgres, MySQL, e a maior parte dos dialetos que não são SQLite em memória), o SQLAlchemy usa `QueuePool` por padrão: uma fila de conexões abertas, de onde `engine.connect()` empresta uma conexão, e para onde `conn.close()` a devolve — sem de fato encerrar o socket TCP na maioria dos casos.

```python
from sqlalchemy import create_engine

engine = create_engine(
    "postgresql+psycopg://app_user:senha@localhost:5432/meubanco",
    pool_size=10,        # conexões mantidas abertas, prontas para uso
    max_overflow=5,      # conexões EXTRAS permitidas sob pico, além de pool_size
    pool_timeout=30,     # segundos esperando uma conexão livre antes de TimeoutError
    pool_recycle=1800,   # segundos até uma conexão ser descartada e recriada
    pool_pre_ping=True,  # testa a conexão com um SELECT 1 antes de emprestá-la
)
```

### `pool_size` — quantas conexões manter abertas

`pool_size` é o número de conexões que o pool tenta manter abertas e ociosas, prontas para uso imediato. O pool **não** abre `pool_size` conexões de uma vez no momento de `create_engine()` — ele cresce sob demanda até esse teto, e conexões continuam abertas mesmo quando não estão em uso, esperando o próximo `engine.connect()`. O valor certo depende de quantas queries concorrentes a aplicação de fato executa dentro de **um processo** — não existe um número universalmente correto, e valores comuns em produção (5 a 20) dependem do padrão de concorrência do workload e, criticamente, de quantos processos worker existem (voltamos a isso na seção de PgBouncer).

### `max_overflow` — quantas extras sob pico

`max_overflow` permite que o pool abra conexões **além** de `pool_size` quando toda a fila está emprestada e mais uma é pedida — até esse limite adicional. Overflow existe para absorver picos transitórios sem falhar imediatamente, mas essas conexões extras não ficam permanentemente no pool: por padrão, ao serem devolvidas (`conn.close()`), se o pool já está com `pool_size` conexões ociosas, a conexão de overflow é de fato **fechada**, não reciclada — ela paga o custo completo de abertura de novo, na próxima vez que for necessária. `max_overflow=10` com `pool_size=20` significa um teto de 30 conexões simultâneas por processo — não 20+10 "reservadas", e sim um limite superior que só é atingido sob pico real.

### `pool_timeout` — quanto esperar antes de desistir

Quando todas as conexões do pool (incluindo overflow) estão emprestadas e uma nova é pedida, `engine.connect()` não falha imediatamente — ele **espera** até `pool_timeout` segundos por uma conexão que seja devolvida. Se ninguém devolve dentro desse prazo, a exceção do bug de abertura desta nota é levantada: `TimeoutError: QueuePool limit ... reached, connection timed out, timeout 30`. Esse é o sinal mais direto de pool esgotado em produção — e o primeiro lugar a olhar quando ele aparece é: (1) o pool está mesmo pequeno demais para a carga, ou (2) queries estão demorando demais / conexões estão vazando sem devolução (o mesmo padrão de "esquecer o `with`" coberto na nota 01), segurando conexões emprestadas por muito mais tempo do que deveriam.

### `pool_recycle` — evitar conexões mortas por timeout do lado do banco

Bancos de dados e firewalls intermediários frequentemente derrubam conexões TCP ociosas depois de um tempo — o Postgres tem `idle_in_transaction_session_timeout` e comportamentos configuráveis, load balancers e firewalls corporativos costumam ter seus próprios timeouts de conexão ociosa (minutos a poucas horas, dependendo do ambiente), e o lado do SQLAlchemy não é automaticamente avisado disso: do ponto de vista do pool, a conexão continua parecendo "boa", só que na próxima tentativa de uso ela falha com um erro de conexão perdida (`OperationalError: server closed the connection unexpectedly`, ou similar).

`pool_recycle=1800` instrui o pool a **descartar proativamente** qualquer conexão com mais de 1800 segundos (30 minutos) de idade, mesmo que pareça saudável, e abrir uma nova em seu lugar na próxima vez que for pedida — antes que ela seja usada e falhe de forma inesperada em produção. O valor deve ficar **abaixo** do timeout mais agressivo conhecido no caminho de rede (banco, firewall, load balancer) — um `pool_recycle` de 30 minutos não ajuda nada se algum firewall no meio do caminho derruba conexões ociosas depois de 10.

`pool_pre_ping=True` é uma defesa complementar, não substituta: antes de emprestar uma conexão do pool, o SQLAlchemy executa um `SELECT 1` (ou equivalente) barato para confirmar que ela ainda está viva; se não estiver, descarta e tenta outra, de forma transparente para quem chamou `engine.connect()`. `pool_recycle` previne o problema proativamente por idade; `pool_pre_ping` o detecta reativamente por teste — as duas técnicas juntas cobrem cenários diferentes (uma conexão pode morrer por outros motivos além de idade — reinício do banco, falha de rede transitória).

```mermaid
flowchart TD
    A["engine.connect() pede uma conexão"] --> B{"Pool tem conexão\nociosa disponível?"}
    B -->|Sim| C{"pool_pre_ping habilitado?"}
    C -->|Sim| D["SELECT 1 de teste"]
    D -->|OK| E["Empresta a conexão"]
    D -->|Falhou| F["Descarta, cria nova conexão"]
    F --> E
    C -->|Não| E
    B -->|Não| G{"Já atingiu\npool_size + max_overflow?"}
    G -->|Não| H["Abre nova conexão\n(handshake + auth)"]
    H --> E
    G -->|Sim| I["Espera até pool_timeout\npor uma devolução"]
    I -->|Devolvida a tempo| E
    I -->|Estourou o tempo| J["TimeoutError:\nQueuePool limit reached"]
```

## Pooling no Django: `CONN_MAX_AGE`

O Django tem seu próprio mecanismo, mais simples que o `QueuePool` do SQLAlchemy: `CONN_MAX_AGE`, configurado em `DATABASES` em `settings.py`, controla quanto tempo (em segundos) uma conexão pode ser reusada entre requests **dentro do mesmo processo**, antes de ser fechada e recriada.

```python
# settings.py
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": "meubanco",
        "USER": "app_user",
        "PASSWORD": "senha",
        "HOST": "localhost",
        "PORT": "5432",
        "CONN_MAX_AGE": 600,       # conexão reusada por até 10 minutos entre requests
        "CONN_HEALTH_CHECKS": True,  # equivalente ao pool_pre_ping do SQLAlchemy
    }
}
```

O comportamento padrão histórico do Django é `CONN_MAX_AGE = 0`: **uma conexão nova por request**, fechada ao final de cada request — o pior cenário de custo de handshake, mas também o mais simples de raciocinar (nenhum estado de conexão vaza entre requests). `CONN_MAX_AGE=None` mantém a conexão indefinidamente aberta enquanto o processo worker viver (equivalente, em espírito, a `pool_recycle` desabilitado); um valor numérico como `600` reusa a conexão entre requests desse mesmo processo por até 10 minutos antes de fechá-la e abrir outra — o meio-termo mais comum em produção.

O ponto conceitual que vale destacar é que **o Django não implementa um pool de múltiplas conexões por processo da forma que o `QueuePool` do SQLAlchemy faz** — cada processo/thread worker do Django tipicamente mantém **uma** conexão persistente (por thread, sob WSGI multi-thread), reusada entre requests até `CONN_MAX_AGE` expirar, não um conjunto de N conexões emprestáveis. Isso simplifica o modelo mental (não há `pool_size`/`max_overflow` para configurar), mas também significa que a mesma pergunta de "quantos processos worker × quantas conexões por processo" se aplica igualmente — só que o "quantas conexões por processo" tende a ser próximo de 1 por thread, em vez de um pool configurável.

> [!warning] `CONN_MAX_AGE` alto sem `CONN_HEALTH_CHECKS` reproduz o problema de conexão morta
> Manter uma conexão viva por muito tempo (`CONN_MAX_AGE=None` ou um valor alto) sem `CONN_HEALTH_CHECKS=True` corre o mesmo risco do `pool_recycle` mal configurado no SQLAlchemy: a conexão pode ter sido derrubada silenciosamente por um firewall ou pelo próprio banco, e o Django só descobre isso ao tentar usá-la, falhando o request em andamento. `CONN_HEALTH_CHECKS=True` (disponível desde o Django 4.1) faz uma checagem leve antes de reusar a conexão, análoga ao `pool_pre_ping`.

## O problema de N workers × M conexões — e por que um pool por processo não basta

Voltando ao bug de abertura: o ponto crítico é que **tanto o `QueuePool` do SQLAlchemy quanto o mecanismo de conexão do Django operam dentro de um único processo**. Servidores WSGI/ASGI de produção — Gunicorn, uWSGI — tipicamente rodam múltiplos **processos worker** para aproveitar múltiplos núcleos de CPU (contornando o GIL do Python, que limita paralelismo de CPU dentro de um único processo — assunto do Galho 7 desta trilha). Cada processo worker é um interpretador Python independente, com sua própria `Engine`, seu próprio pool, sua própria memória.

```mermaid
flowchart TB
    subgraph SemPooler["Sem pooler externo — cada worker com pool próprio"]
        W1["Worker 1\npool_size=20"] --> DB1[("PostgreSQL\nmax_connections=100")]
        W2["Worker 2\npool_size=20"] --> DB1
        W3["Worker 3\npool_size=20"] --> DB1
        W4["Worker 4\npool_size=20"] --> DB1
        W5["... até Worker 8"] --> DB1
    end
```

Com Gunicorn configurado para 8 workers e cada worker com `pool_size=20` + `max_overflow=10`, o teto teórico de conexões simultâneas contra o banco é `8 × 30 = 240` — mais que o dobro do `max_connections=100` padrão do Postgres. Sob tráfego baixo isso nunca se manifesta (cada worker usa poucas conexões do seu pool); sob pico, é exatamente o cenário do bug de abertura desta nota: vários workers atingindo overflow ao mesmo tempo, e o banco recusando conexão nova a partir do worker que chega depois do limite ser atingido.

Reduzir `pool_size` por worker é uma mitigação parcial (menos conexões por processo), mas não resolve o problema estrutural: o número de workers tende a crescer com a carga (mais tráfego → mais processos ou mais réplicas do serviço → mais pools independentes), e cada novo processo multiplica o total outra vez. A pergunta certa não é "qual `pool_size` configurar", é "quantas conexões reais o banco pode sustentar, dividido por quantos processos existirão no pico" — e essa divisão, com auto-scaling e múltiplas réplicas de deploy, frequentemente chega a um número pequeno demais para ser útil, ou exige coordenação que nenhum pool por-processo consegue fazer sozinho.

## PgBouncer: multiplexando conexões de aplicação sobre poucas conexões reais

A solução estrutural é introduzir um **pooler externo** ao processo da aplicação — um serviço dedicado, rodando entre a aplicação e o banco, que mantém um número pequeno e fixo de conexões reais abertas contra o Postgres, e multiplexa um número muito maior de conexões "de aplicação" sobre esse conjunto reduzido. Para Postgres, o pooler de fato-padrão da indústria é o **PgBouncer**.

```mermaid
flowchart TB
    subgraph ComPgBouncer["Com PgBouncer — muitas conexões de app, poucas conexões reais"]
        WA["Worker 1..8\n(8 × 30 = até 240\nconexões de app)"] --> PB["PgBouncer\n(pool de ~20 conexões\nreais ao banco)"]
        PB --> DB2[("PostgreSQL\nmax_connections=100\nusa só ~20")]
    end
```

Do ponto de vista de cada worker da aplicação, nada muda — ele continua abrindo conexões via seu `QueuePool` normalmente, só que a URL de conexão aponta para o PgBouncer (porta `6432` por convenção, não a porta `5432` do Postgres). O PgBouncer aceita todas essas conexões "de aplicação" (podem ser centenas) e as multiplexa sobre um pool próprio, muito menor, de conexões **reais** ao Postgres — a fração exata (ex.: 20 conexões reais servindo 240 conexões de aplicação) depende do padrão de uso, mas o princípio é que a maioria das conexões de aplicação está ociosa a maior parte do tempo (esperando a próxima query do handler que a "possui"), então poucas conexões reais bastam para servir muito mais conexões lógicas, desde que o pooler saiba reatribuir uma conexão real assim que ela fica livre.

### Os três modos do PgBouncer

O comportamento de multiplexação do PgBouncer depende do modo de pooling configurado — a diferença está em **quando** uma conexão real é devolvida ao pool interno do PgBouncer, disponível para outra conexão de aplicação:

- **`session`** — a conexão real fica atrelada à conexão de aplicação por toda a duração da sessão (do `connect` ao `disconnect`). É o modo mais compatível (suporta tudo que Postgres suporta, incluindo `LISTEN`/`NOTIFY`, prepared statements de sessão, `SET` de variáveis de sessão), mas oferece o menor ganho de multiplexação — se a aplicação mantém conexões abertas por muito tempo (o próprio `QueuePool` fazendo isso), o PgBouncer não consegue reaproveitar aquela conexão real para outra sessão enquanto a primeira não desconectar.
- **`transaction`** — a conexão real é devolvida ao pool interno assim que a **transação atual** termina (commit ou rollback), não quando a sessão de aplicação desconecta. É o modo mais usado em produção, porque oferece a maior parte do ganho de multiplexação sem exigir mudanças profundas na aplicação — mas impõe restrições: recursos atrelados a uma sessão específica (prepared statements nomeados fora do escopo da transação, `SET` de variável de sessão que deveria persistir entre transações, `LISTEN`/`NOTIFY`) podem se comportar de forma inesperada, porque a "mesma" conexão de aplicação pode, entre duas transações, acabar mapeada para conexões reais **diferentes** do lado do Postgres.
- **`statement`** — a conexão real é devolvida após cada **statement** individual, o mais agressivo dos três; não suporta transações multi-statement explícitas do lado da aplicação, e é usado só em cenários bem específicos (proxies read-only de alta cardinalidade). Raro fora de casos de nicho.

> [!warning] Modo `transaction` e transações longas em bloco de sessão
> Em modo `transaction`, qualquer recurso que a aplicação espera persistir "durante toda a sessão" (fora do escopo de uma transação individual) é um risco — a nota 06 do galho cobre transações e isolation levels com mais rigor; aqui vale a ressalva prática: migrar para PgBouncer em modo `transaction` costuma exigir auditar código que assume `SET search_path`, prepared statements de sessão nomeados, ou `LISTEN`/`NOTIFY` fora de uma transação — código que funcionava direto contra o Postgres pode se comportar diferente atrás do PgBouncer em modo `transaction`, silenciosamente.

### Configuração mínima ilustrativa

```ini
; pgbouncer.ini — exemplo mínimo ilustrativo
[databases]
meubanco = host=localhost port=5432 dbname=meubanco

[pgbouncer]
listen_port = 6432
listen_addr = *
auth_type = scram-sha-256
pool_mode = transaction
max_client_conn = 1000    ; conexões de APLICAÇÃO aceitas
default_pool_size = 20    ; conexões REAIS mantidas por database/user
```

E do lado da aplicação, a única mudança é a porta (e, dependendo do modo, desabilitar recursos incompatíveis do lado do driver — como prepared statement caching automático de alguns drivers, que pode precisar de ajuste em modo `transaction`):

```python
engine = create_engine(
    "postgresql+psycopg://app_user:senha@localhost:6432/meubanco",  # 6432 = PgBouncer
    pool_size=20,
    max_overflow=10,
)
```

Nesse arranjo, o `QueuePool` da aplicação continua existindo e fazendo seu trabalho normalmente — controlando concorrência **dentro do processo** — mas agora ele está conectado ao PgBouncer, não diretamente ao Postgres, e é o PgBouncer quem garante que o número de conexões **reais** contra o banco fica dentro do que o Postgres foi configurado para aguentar, independentemente de quantos workers/processos/réplicas a aplicação tiver no pico.

## Monitoramento básico de pool esgotado

O sintoma mais direto é a exceção já vista no bug de abertura: `TimeoutError: QueuePool limit of size X overflow Y reached, connection timed out, timeout Z` (SQLAlchemy) ou, do lado do Django, um `OperationalError` de conexão recusada pelo banco quando `CONN_MAX_AGE` alto acumula conexões demais. Diagnosticar a causa raiz segue uma sequência prática:

1. **Confirmar que é esgotamento de pool, não lentidão de query.** Um `pool_timeout` estourando pode significar pool pequeno demais para a carga real, ou queries individuais demorando tanto que seguram conexões emprestadas por mais tempo do que deveriam — o log de erro por si só não distingue os dois; olhar a duração média das queries no mesmo período ajuda a decidir qual é o caso.
2. **Contar conexões ativas no banco**, do lado do Postgres: `SELECT count(*) FROM pg_stat_activity WHERE datname = 'meubanco';`, opcionalmente agrupado por `state` (`active` vs `idle` vs `idle in transaction`) e por `usename`/`application_name` para identificar qual processo/serviço está consumindo mais. Um número alto de conexões em `idle in transaction` é um sinal específico de transações abertas e nunca commitadas/revertidas — conexões seguradas sem necessidade, exatamente o padrão de "esquecer o `with`" coberto na nota 01.
3. **Multiplicar workers × `pool_size`+`max_overflow`** e comparar contra `max_connections` do Postgres (`SHOW max_connections;`) — a aritmética do bug de abertura desta nota, feita explicitamente, antes de qualquer mudança de configuração.
4. **Instrumentar o pool via eventos do SQLAlchemy**, para observar tamanho e uso do pool em tempo real, sem depender só do erro estourando:

```python
from sqlalchemy import event

@event.listens_for(engine, "checkout")
def on_checkout(dbapi_conn, connection_record, connection_proxy):
    pool = engine.pool
    print(f"[pool] emprestada — em uso: {pool.checkedout()}, disponíveis: {pool.checkedin()}")
```

5. **Expor essas métricas para um sistema de observabilidade** (Prometheus, Datadog, o que a stack já usar) em vez de só logar — conexões em uso, conexões disponíveis, contagem de timeouts de pool, e (do lado do PgBouncer, se em uso) `SHOW POOLS;` via `psql` contra a porta administrativa do PgBouncer, que expõe exatamente quantas conexões de aplicação estão esperando (`cl_waiting`) por uma conexão real livre — o equivalente, no pooler externo, do que `pool_timeout` estourando significa dentro de um único processo.

## Dimensionando o pool: um cálculo de exemplo

Voltando ao cenário do bug de abertura com números concretos, o raciocínio de dimensionamento segue uma ordem fixa — banco primeiro, depois divisão entre processos, nunca o contrário:

1. **Descobrir o teto real do banco.** `SHOW max_connections;` no Postgres retorna o limite absoluto — mas esse número não deve ser tratado como "disponível para esta aplicação": bancos compartilhados por múltiplos serviços, conexões administrativas (`superuser_reserved_connections`), réplicas de leitura e ferramentas de monitoramento (`pg_stat_statements`, backups, `pgAdmin`) também consomem desse mesmo teto. Um `max_connections=100` raramente significa "100 disponíveis para este serviço" — 70-80 sobrando para a aplicação, depois de reservar margem para o resto, é uma estimativa mais realista em ambientes compartilhados.
2. **Contar processos worker no pico**, não em repouso — se o serviço faz auto-scaling horizontal (mais réplicas sob carga) ou usa Gunicorn com `--workers` calculado como `2 × núcleos + 1` (a heurística comum), o número de processos no pico de tráfego pode ser bem maior que em operação normal, e é esse número de pico que importa para o cálculo.
3. **Dividir o orçamento de conexões pelo número de processos no pico.** Com 80 conexões disponíveis e um pico de 8 workers × 2 réplicas = 16 processos, cada processo tem direito a `80 / 16 = 5` conexões — um `pool_size` bem menor do que os 20 usados no exemplo do bug, e provavelmente pequeno demais para dar folga de `max_overflow` sem estourar o orçamento total de novo.

```python
# Cálculo explícito, documentado no código de bootstrap da aplicação —
# não um "número que pareceu razoável" escolhido sem registro do porquê.
MAX_CONNECTIONS_DISPONIVEIS_PARA_APP = 80   # max_connections=100, menos margem
PROCESSOS_NO_PICO = 16                       # 8 workers Gunicorn x 2 réplicas
ORCAMENTO_POR_PROCESSO = MAX_CONNECTIONS_DISPONIVEIS_PARA_APP // PROCESSOS_NO_PICO  # 5

engine = create_engine(
    DATABASE_URL,
    pool_size=3,        # a maior parte do orçamento reservada para overflow
    max_overflow=2,     # 3 + 2 = 5, dentro do orçamento calculado
    pool_timeout=10,    # falhar rápido em vez de empilhar requests esperando
)
```

É exatamente esse tipo de aritmética — orçamento pequeno demais para sobrar folga real por processo — que sinaliza a hora de trocar "pool menor por worker" por "pooler externo compartilhado": com PgBouncer absorvendo a multiplexação, cada processo pode voltar a ter um `pool_size` confortável (20, 30) porque o PgBouncer é quem garante que o total de conexões **reais** contra o Postgres fica dentro do orçamento, não a soma aritmética dos pools de cada processo.

## Pooling em contexto assíncrono

O Galho 7 desta trilha cobriu `asyncio` e por que ele muda o modelo de concorrência em Python — vale uma nota breve de como isso se conecta a pooling. O `AsyncEngine` do SQLAlchemy (criado via `create_async_engine()`, usado com drivers assíncronos como `asyncpg` ou `psycopg` em modo async) usa por baixo um `AsyncAdaptedQueuePool` — conceitualmente o mesmo `QueuePool` já descrito nesta nota (mesmos parâmetros: `pool_size`, `max_overflow`, `pool_timeout`, `pool_recycle`), adaptado para emprestar e devolver conexões de forma compatível com `await`/corrotinas em vez de bloquear a thread.

```python
from sqlalchemy.ext.asyncio import create_async_engine

async_engine = create_async_engine(
    "postgresql+asyncpg://app_user:senha@localhost:5432/meubanco",
    pool_size=20,
    max_overflow=10,
    pool_recycle=1800,
)
```

O raciocínio de dimensionamento (workers × pool, orçamento do banco, PgBouncer como saída estrutural) não muda por a aplicação ser assíncrona — o que muda é que, sob `asyncio` com um único processo, muitas corrotinas concorrentes podem competir pelo mesmo pool **dentro do mesmo processo**, sem a divisão em múltiplos processos worker do modelo síncrono tradicional. Isso desloca parte da pressão: menos processos multiplicando o total (potencialmente 1 processo por núcleo, em vez de vários workers WSGI), mas mais concorrência real disputando o mesmo `pool_size` dentro desse processo — o cálculo de dimensionamento da seção anterior continua válido, só com um "N" (número de processos) tipicamente menor e um "M" (conexões concorrentes por processo) potencialmente maior.

## Armadilhas comuns

> [!warning] Configurar `pool_size` sem considerar o número de processos worker
> **O que acontece:** cada worker Gunicorn/uWSGI ganha seu próprio `pool_size`/`max_overflow`, calculado como se fosse a única fonte de conexões contra o banco — exatamente o bug de abertura desta nota.
> **Por quê:** `pool_size` e `max_overflow` são por-processo; multiplicar pelo número de workers (e réplicas de deploy, se houver múltiplas instâncias do serviço) é aritmética obrigatória, não opcional.
> **Como evitar:** calcular o teto real (workers × réplicas × (`pool_size`+`max_overflow`)) e compará-lo explicitamente contra `max_connections` do banco antes de subir a configuração; a partir de um certo número de processos, introduzir um pooler externo (PgBouncer) em vez de tentar espremer `pool_size` cada vez menor por worker.

> [!warning] `pool_recycle` maior que o timeout de idle do banco/firewall
> **O que acontece:** conexões são recicladas proativamente pelo SQLAlchemy a cada `pool_recycle` segundos, mas algum componente de rede no meio do caminho (firewall corporativo, load balancer, o próprio Postgres) derruba conexões ociosas antes disso — a conexão morre silenciosamente antes de ser reciclada, e a próxima query nela falha.
> **Por quê:** `pool_recycle` só previne o problema se o valor configurado for **menor** que o timeout mais agressivo em qualquer ponto do caminho de rede — não existe um valor "seguro" universal, ele depende da infraestrutura.
> **Como evitar:** descobrir o timeout de idle mais agressivo conhecido no ambiente (perguntar ao time de infra, checar configuração de load balancer/firewall, checar `idle_in_transaction_session_timeout` e afins do Postgres) e configurar `pool_recycle` com margem de segurança abaixo dele; complementar com `pool_pre_ping=True` para os casos que `pool_recycle` não cobrir.

> [!warning] Migrar para PgBouncer em modo `transaction` sem auditar recursos de sessão
> **O que acontece:** a aplicação passa a se conectar via PgBouncer em modo `transaction` (o mais comum, pelo ganho de multiplexação), e algum código que dependia de estado de sessão persistente entre transações — `SET search_path`, prepared statements nomeados fora de transação, `LISTEN`/`NOTIFY` — começa a se comportar de forma inconsistente ou silenciosamente errada.
> **Por quê:** em modo `transaction`, duas transações da "mesma" conexão de aplicação podem ser servidas por conexões reais **diferentes** do lado do Postgres — qualquer estado que não seja parte da transação atual não tem garantia de sobreviver entre uma transação e a próxima.
> **Como evitar:** antes de migrar para modo `transaction`, auditar o código em busca desses padrões; para os casos que genuinamente precisam de estado de sessão persistente, considerar um pool dedicado em modo `session` para esse caminho específico, mantendo `transaction` para o resto.

> [!warning] Tratar `pool_size` alto como solução para queries lentas
> **O que acontece:** sob pressão de timeouts de pool, a resposta reflexa é aumentar `pool_size`/`max_overflow` — o erro desaparece temporariamente, mas o banco começa a sofrer com contenção de outra natureza (CPU, I/O, locks) porque agora há mais queries concorrentes competindo pelos mesmos recursos internos do banco.
> **Por quê:** um pool maior resolve "esperar por uma conexão livre" quando o gargalo é genuinamente concorrência de conexão; não resolve queries individualmente lentas — só permite que mais delas rodem em paralelo, geralmente piorando a lentidão de cada uma.
> **Como evitar:** diagnosticar a causa (passo 1 da seção de monitoramento) antes de mexer no tamanho do pool — se a duração média das queries está alta, o problema é indexação, plano de execução ou contenção de lock, não tamanho de pool; aumentar o pool nesse caso só empurra o gargalo para um lugar mais difícil de ver.

## Em entrevista

Perguntas sênior sobre connection pooling em produção quase sempre miram no cenário de múltiplos workers, porque é onde a intuição de "um pool bem configurado resolve tudo" quebra.

> "A connection pool inside the app process — SQLAlchemy's `QueuePool`, or Django's per-connection reuse via `CONN_MAX_AGE` — solves the cost of opening a TCP connection plus authenticating against the database on every request, by keeping a small number of already-authenticated connections around and lending them out. But that pool is scoped to a single process. The moment you run multiple worker processes — Gunicorn with N workers, say — each one has its own pool, and the real number of connections hitting the database is N times whatever you configured per worker, not the number you configured. I've seen this bite a team directly: `pool_size=20` plus `max_overflow=10` looked reasonable in isolation, but with 8 Gunicorn workers that's up to 240 connections against a Postgres instance with the default `max_connections=100` — it worked fine under light load and fell over under a traffic spike when several workers hit overflow at once. The fix isn't shrinking the per-worker pool indefinitely as worker count grows — it's introducing an external pooler, PgBouncer for Postgres, that sits between the app and the database and multiplexes many application-side connections onto a small, fixed number of real connections. In transaction pooling mode, PgBouncer hands back the real connection to its internal pool as soon as a transaction commits, not when the app's logical connection closes — which is what makes the multiplexing ratio so favorable, at the cost of needing to audit any code that assumes session-scoped state persists across transactions."

Um follow-up comum: **"como você detectaria isso em produção antes de um incidente?"** — a resposta esperada é monitoramento proativo: métricas de pool exposto via `event.listens_for` do SQLAlchemy (ou os hooks equivalentes de outras stacks), `pg_stat_activity` contado periodicamente, e alertas configurados **antes** de `pool_timeout` estourar de fato — não descobrir o problema pela primeira vez em produção via `TimeoutError` num pico de tráfego, como no bug de abertura desta nota.

> [!question]- E se perguntarem "por que não simplesmente aumentar `max_connections` do Postgres em vez de introduzir um pooler externo?"
> Vale reconhecer que essa é uma opção real em cenários pequenos — mas conexões no Postgres não são grátis do lado do banco: cada conexão consome memória (o modelo de processo-por-conexão do Postgres, tradicionalmente; PostgreSQL 17+ manteve esse modelo, com trabalho em andamento na comunidade para reduzir esse custo em versões futuras) e adiciona overhead de coordenação interna. Elevar `max_connections` de 100 para, digamos, 500 "resolve" o sintoma imediato, mas desloca o problema para o próprio banco — mais memória consumida por conexões ociosas, mais contenção em estruturas internas compartilhadas — em vez de reduzir o número de conexões reais necessárias, que é o que um pooler externo genuinamente faz. A resposta madura reconhece o trade-off: `max_connections` mais alto é um paliativo válido em escala pequena/moderada; PgBouncer (ou pgcat, ou o pooling embutido de serviços gerenciados como RDS Proxy/Supabase) é a solução que escala, porque ataca a causa — conexões reais demais — em vez do sintoma.

## Como explicar em inglês

| PT | EN |
|----|----|
| pool de conexões | connection pool |
| conexão persistente | persistent connection |
| handshake TCP | TCP handshake |
| autenticação no banco | database authentication |
| conexão ociosa | idle connection |
| conexão emprestada/devolvida | checked-out / checked-in connection |
| tempo de espera esgotado | timeout exceeded |
| conexão morta/derrubada | stale / dropped connection |
| pooler externo | external pooler / connection pooler |
| multiplexação de conexões | connection multiplexing |
| processo worker | worker process |
| conexão real (contra o banco) | server-side connection |
| conexão de aplicação (lógica) | client-side connection |

## O que vem a seguir

Esta nota fechou o ciclo aberto pela [[01 - SQLAlchemy Core — Engine, Connection e expressão SQL|nota 01]] — o pool que a Engine "tem por baixo" ganhou nome (`QueuePool`), parâmetros (`pool_size`/`max_overflow`/`pool_timeout`/`pool_recycle`) e o problema estrutural que nenhum ajuste de pool por-processo resolve sozinho: múltiplos workers multiplicando conexões contra um limite fixo do banco, e a solução via pooler externo (PgBouncer). Com isso, o galho tem todas as peças de uma camada de persistência de produção — modelagem, migrations, N+1, transações, pool — prontas para serem integradas.

- [[01 - SQLAlchemy Core — Engine, Connection e expressão SQL|01 — SQLAlchemy Core]] — onde a Engine e seu pool foram introduzidos pela primeira vez, sem aprofundar.
- [[06 - Transações e isolamento — ACID na prática, isolation levels, deadlocks de aplicação|06 — Transações e isolamento]] — o comportamento de transação que interage diretamente com o modo `transaction` do PgBouncer.
- [[08 - Capstone — projetando a camada de persistência de um serviço real|08 — Capstone]] — integra modelagem, migration, eager loading, transação e configuração de pool num serviço real.
- [[03-Dominios/Tecnologia/Python/Persistência de dados/index|Persistência de dados (Galho 9)]] — MOC deste galho.

## Fontes

- SQLAlchemy. *Connection Pooling*. docs.sqlalchemy.org, versão 2.0. https://docs.sqlalchemy.org/en/20/core/pooling.html (acessado em 2026-07-11) — `QueuePool`, `pool_size`, `max_overflow`, `pool_timeout`, `pool_recycle`, `pool_pre_ping`.
- SQLAlchemy. *Engine Configuration*. docs.sqlalchemy.org, versão 2.0. https://docs.sqlalchemy.org/en/20/core/engines.html (acessado em 2026-07-11) — parâmetros de pool passados a `create_engine()`.
- Django Software Foundation. *Database connections* (`CONN_MAX_AGE`, `CONN_HEALTH_CHECKS`). docs.djangoproject.com, versão 5.x. https://docs.djangoproject.com/en/5.2/ref/databases/#persistent-connections (acessado em 2026-07-11) — conexões persistentes, health checks.
- PgBouncer. *PgBouncer Documentation* (pooling modes: session, transaction, statement). pgbouncer.org. https://www.pgbouncer.org/features.html (acessado em 2026-07-11) — modos de pooling e suas restrições.
- PgBouncer. *Config file* (`pool_mode`, `default_pool_size`, `max_client_conn`). pgbouncer.org. https://www.pgbouncer.org/config.html (acessado em 2026-07-11) — parâmetros de configuração.
- PostgreSQL Global Development Group. *Connections and Authentication* (`max_connections`). postgresql.org, versão 17. https://www.postgresql.org/docs/17/runtime-config-connection.html (acessado em 2026-07-11) — `max_connections` e custo de memória por conexão.
- PostgreSQL Global Development Group. *pg_stat_activity*. postgresql.org, versão 17. https://www.postgresql.org/docs/17/monitoring-stats.html#MONITORING-PG-STAT-ACTIVITY-VIEW (acessado em 2026-07-11) — monitoramento de conexões ativas.

Consultado em 2026-07-11.
