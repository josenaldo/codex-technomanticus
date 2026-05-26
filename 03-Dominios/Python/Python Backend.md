---
title: "Python Backend"
created: 2026-04-10
updated: 2026-04-10
type: concept
status: seedling
tags:
  - python
  - backend
  - entrevista
publish: false
---

# Python Backend

Django, FastAPI e o ecossistema Python para backend — do ORM ao deploy em produção. Para entrevistas, o foco é em como Python resolve os mesmos problemas de produção que Java e Node.js resolvem de formas diferentes.

## O que é

Python é a terceira linguagem mais usada para backend web, com dois frameworks dominantes:

- **Django** — full-featured, "batteries included". ORM, admin, auth, migrations built-in. Equivalente ao Spring Boot em filosofia.
- **FastAPI** — moderno, async-first, baseado em type hints. Equivalente ao NestJS em abordagem.

## Frameworks

| Framework | Estilo | Equivalente Java/Node |
| --- | --- | --- |
| Django | Full-featured, ORM integrado | Spring Boot |
| FastAPI | Async, type-safe, OpenAPI auto | NestJS + Fastify |
| Flask | Minimalista, extensível | Express |
| Celery | Task queue (não é framework web) | BullMQ, Spring @Async |

## Troubleshooting em produção

Problemas recorrentes e suas soluções idiomáticas em Python — comparáveis aos problemas de Java/Spring Boot e Node.js.

### Connection pool exausto

**Django:**

```python
# settings.py
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'mydb',
        'CONN_MAX_AGE': 600,  # reutilizar conexões por 10 min (default: 0 = fecha cada request)
        'CONN_HEALTH_CHECKS': True,  # Django 4.1+ — verifica se conexão está viva
        'OPTIONS': {
            'MAX_CONNS': 20,  # com django-db-connection-pool
        },
    }
}
```

**Django sem pool real:** por default, Django usa 1 conexão por request e fecha no final. `CONN_MAX_AGE` reutiliza, mas não é um pool verdadeiro como HikariCP. Para pool real, usar `django-db-connection-pool` ou `pgbouncer` como proxy externo.

**FastAPI + SQLAlchemy:**

```python
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

engine = create_engine(
    "postgresql://user:pass@localhost/db",
    pool_size=10,           # conexões mantidas
    max_overflow=5,         # extras temporárias
    pool_timeout=30,        # timeout para adquirir conexão
    pool_recycle=1800,      # reciclar conexões a cada 30 min
    pool_pre_ping=True,     # health check antes de usar
)
```

### N+1 queries

**Django ORM:**

```python
# RUIM — N+1
doctors = Doctor.objects.all()
for d in doctors:
    print(d.appointments.count())  # 1 query por doctor

# BOM — select_related (FK, OneToOne — faz JOIN)
doctors = Doctor.objects.select_related('specialty').all()

# BOM — prefetch_related (ManyToMany, reverse FK — 2 queries)
doctors = Doctor.objects.prefetch_related('appointments').all()

# BOM — annotation (aggregation sem carregar relações)
from django.db.models import Count
doctors = Doctor.objects.annotate(
    appointment_count=Count('appointments')
).all()
```

**Detectar N+1:**

```python
# Django Debug Toolbar (dev) — mostra todas as queries por request
# Em produção: django-querycount ou nplusone
INSTALLED_APPS += ['debug_toolbar', 'nplusone']

NPLUSONE_RAISE = True  # levanta exceção em N+1 (dev/test)
```

### Memory leak

**Diagnóstico:**

```python
# tracemalloc — built-in desde Python 3.4
import tracemalloc

tracemalloc.start()
# ... rodar código
snapshot = tracemalloc.take_snapshot()
top = snapshot.statistics('lineno')
for stat in top[:10]:
    print(stat)

# objgraph — visualizar referências
import objgraph
objgraph.show_most_common_types(limit=20)
objgraph.show_growth()  # chamar periodicamente para ver o que cresce
```

**Causas comuns em Django:**
- Querysets não avaliados acumulados em listas
- Sinais (signals) que acumulam receivers
- Cache em memória sem limite (`dict` que só cresce)
- `DEBUG=True` em produção — Django guarda **todas as queries** em `connection.queries`

```python
# CRÍTICO — sempre False em produção
DEBUG = False  # se True, acumula todas as SQL queries na memória
```

### Worker management (Gunicorn)

**Equivalente ao thread pool do Tomcat:**

```bash
# gunicorn.conf.py
workers = (2 * cpu_count) + 1   # processos (equivale a threads no Java)
worker_class = "uvicorn.workers.UvicornWorker"  # async (FastAPI)
timeout = 30                     # kill worker se demorar mais
graceful_timeout = 30            # tempo para terminar requests em andamento
max_requests = 1000              # reciclar worker após N requests (previne memory leak)
max_requests_jitter = 50         # jitter para não reciclar todos ao mesmo tempo
```

**Worker types:**
- `sync` — 1 request por worker (equivale a thread-per-request do Tomcat)
- `gthread` — thread pool por worker
- `uvicorn` — async, event-loop (equivale ao Netty/WebFlux)

### API timeout e circuit breaker

```python
# requests com timeout (SEMPRE definir timeout)
import requests

response = requests.get(
    "https://external-api.com/data",
    timeout=(3, 10),  # (connect_timeout, read_timeout) em segundos
)

# Circuit breaker com pybreaker
import pybreaker

breaker = pybreaker.CircuitBreaker(
    fail_max=5,             # abre após 5 falhas
    reset_timeout=30,       # tenta half-open após 30s
)

@breaker
def call_external_service():
    return requests.get("https://api.example.com", timeout=5)
```

### Background tasks (Celery)

**Equivalente ao Kafka consumer / BullMQ worker:**

```python
# tasks.py
from celery import Celery

app = Celery('tasks', broker='redis://localhost:6379/0')

@app.task(bind=True, max_retries=3, default_retry_delay=60)
def send_notification(self, user_id, message):
    try:
        notify_user(user_id, message)
    except ExternalServiceError as exc:
        raise self.retry(exc=exc)  # retry com backoff

# Chamar
send_notification.delay(user_id=42, message="Consulta confirmada")
```

### Database migrations seguras

```bash
# Django migrations — built-in (equivalente ao Flyway)
python manage.py makemigrations   # gera arquivo de migração
python manage.py migrate          # aplica

# Migração segura: mesma estratégia expand-and-contract
# Nunca remover coluna na mesma release que remove o código
```

```python
# migrations/0010_add_email.py
from django.db import migrations, models

class Migration(migrations.Migration):
    operations = [
        # Step 1: adiciona nullable (sem lock longo)
        migrations.AddField(
            model_name='patient',
            name='email',
            field=models.EmailField(null=True),
        ),
        # Step 2: backfill em migration separada (0011)
        # Step 3: AlterField para NOT NULL (0012, após deploy que já escreve email)
    ]
```

### Graceful shutdown

```python
# Django + Gunicorn — graceful por default (SIGTERM → finish requests → exit)
# Configurar no gunicorn.conf.py: graceful_timeout = 30

# FastAPI — lifecycle hooks
from contextlib import asynccontextmanager

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    await database.connect()
    yield
    # Shutdown
    await database.disconnect()
    await redis.close()

app = FastAPI(lifespan=lifespan)
```

### Distributed tracing

```python
# OpenTelemetry para Django
# pip install opentelemetry-instrumentation-django

from opentelemetry.instrumentation.django import DjangoInstrumentor
DjangoInstrumentor().instrument()

# Exportar para Jaeger/Zipkin
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
from opentelemetry.sdk.trace.export import BatchSpanProcessor

provider.add_span_processor(
    BatchSpanProcessor(OTLPSpanExporter(endpoint="http://jaeger:4317"))
)
```

→ Para comparação cross-stack: [[System Design]] (seção Problemas comuns em produção)

## How to explain in English

"While my primary backend stack is Java with Spring Boot, I have experience with Python for backend development as well. Django's ORM and built-in migrations make it very productive for CRUD-heavy applications. I understand how Python solves the same production problems differently — for example, Django uses `select_related` and `prefetch_related` to solve N+1 queries, which is conceptually similar to JPA's `JOIN FETCH` and `@EntityGraph`. For connection pooling, Python typically relies on external tools like PgBouncer because Django's built-in connection handling is simpler than HikariCP. And for background processing, Celery fills the same role as Kafka consumers or BullMQ workers."

### Key vocabulary

- ORM embutido → built-in ORM
- gerenciamento de workers → worker management
- fila de tarefas → task queue (Celery)
- migração de banco → database migration
- pool de conexões externo → external connection pool (PgBouncer)

## Recursos

- [Django Documentation](https://docs.djangoproject.com/) — documentação oficial
- [FastAPI Documentation](https://fastapi.tiangolo.com/) — documentação oficial
- [Django Debug Toolbar](https://django-debug-toolbar.readthedocs.io/)
- [Celery Documentation](https://docs.celeryq.dev/)
- [SQLAlchemy Documentation](https://docs.sqlalchemy.org/)

## Veja também

- [[System Design]] — troubleshooting cross-stack, building blocks
- [[API Design]]
