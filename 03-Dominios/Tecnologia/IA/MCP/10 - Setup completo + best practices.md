---
title: "Setup completo + best practices"
created: 2026-04-11
updated: 2026-05-02
type: concept
progress: backlog
status: seedling
publish: true
tags:
  - mcp
  - ia
  - setup
  - best-practices
aliases:
  - Setup MCP
  - MCP best practices
  - MCP checklist
---

# Setup completo + best practices

> [!abstract] TL;DR
> Esta nota fecha a trilha com checklist end-to-end para construir e operar [[Dicionário de IA#MCP server|MCP servers]] em produção. Stack base: Python [[Dicionário de IA#SDK|SDK]] + Pydantic + FastMCP + uvx para distribuição. Roadmap de 4 fases × ~1 semana cada. Best practices distiladas: tool design rigoroso, schemas tipados, audit log, versioning semver, MCP Inspector na CI. **Investimento total: ~4 semanas para server interno production-ready.**

## Stack recomendada (2026)

```
┌────────────────────────────────────────────────────────┐
│  Linguagem:       Python 3.11+ (TypeScript alternativa)│
│  SDK:             mcp (FastMCP)                        │
│  Validação:       Pydantic v2                          │
│  Transport:       stdio (local) ou HTTP+SSE (team)     │
│  Hosting (HTTP):  Cloudflare Workers, Fly.io, K8s      │
│  Auth (HTTP):     OAuth 2.1 ou Bearer tokens           │
│  Distribution:    uvx (Python) ou npx (TS)             │
│  Inspector:       MCP Inspector (local + CI)           │
│  Logging:         JSON logs → Loki/CloudWatch         │
│  Monitoring:      Langfuse ou OpenTelemetry           │
└────────────────────────────────────────────────────────┘
```

## Roadmap de 4 fases

```mermaid
gantt
    title Roadmap MCP server production - 4 semanas
    dateFormat  YYYY-MM-DD
    section Fase 1
    Server local básico       :a1, 2026-05-02, 7d
    section Fase 2
    Quality (schemas+errors)  :b1, after a1, 7d
    section Fase 3
    Auth + observability      :c1, after b1, 7d
    section Fase 4
    Deploy + distribution     :d1, after c1, 7d
```

## Fase 1 — Server local (semana 1)

**Objetivo:** server stdio funcionando.

### Checklist

- [ ] `pip install mcp` ou `uv add mcp`
- [ ] Estrutura de projeto:

```
my-mcp-server/
├── pyproject.toml
├── README.md
├── src/
│   └── my_server/
│       ├── __init__.py
│       ├── server.py       # FastMCP setup
│       ├── tools.py        # @mcp.tool() definitions
│       ├── resources.py    # @mcp.resource() definitions
│       └── prompts.py      # @mcp.prompt() definitions
└── tests/
    └── test_tools.py
```

- [ ] FastMCP("my-server") com 1 tool funcionando
- [ ] Test via MCP Inspector: `npx @modelcontextprotocol/inspector python -m my_server`
- [ ] Plugar em Claude Desktop/Cursor para teste real
- [ ] Configurar logging básico

### Exemplo mínimo

```python
# src/my_server/server.py
from mcp.server.fastmcp import FastMCP
from .tools import register_tools

mcp = FastMCP("my-server", version="0.1.0")
register_tools(mcp)

def main():
    mcp.run()

if __name__ == "__main__":
    main()
```

```python
# src/my_server/tools.py
def register_tools(mcp):
    @mcp.tool()
    def hello(name: str) -> str:
        """Greet a person by name."""
        return f"Hello, {name}!"
```

## Fase 2 — Quality (semana 2)

**Objetivo:** tools robustos com schemas e error handling.

### Checklist

- [ ] Tools com Pydantic models (não primitives)
- [ ] Cada tool com docstring clara: o quê, quando, retorna o quê, quando NÃO usar
- [ ] Erros informativos (raise ValueError com mensagem útil)
- [ ] Output compacto (truncate, paginate)
- [ ] Idempotência onde possível
- [ ] Resources com URI scheme claro
- [ ] Prompts úteis (templates)
- [ ] Tests unitários para cada tool
- [ ] Validação manual via Inspector

### Exemplo de tool quality

```python
from pydantic import BaseModel, Field, validator
from typing import Literal

class SearchParams(BaseModel):
    query: str = Field(..., min_length=1, max_length=500, description="Search query in natural language")
    limit: int = Field(default=10, ge=1, le=100, description="Max results (1-100)")
    type: Literal["docs", "code", "all"] = Field(default="all")

class SearchResult(BaseModel):
    id: str
    title: str
    snippet: str = Field(..., max_length=200)
    url: str

@mcp.tool()
def search(params: SearchParams) -> list[SearchResult]:
    """
    Search internal knowledge base.

    Use when user asks 'how to', 'what is', 'where can I find'.
    Returns top results with title, snippet, and URL.

    Do NOT use for searching code (use search_code instead).
    """
    if not params.query.strip():
        raise ValueError("query cannot be empty or whitespace")

    raw = backend.search(params.query, params.limit, params.type)
    return [SearchResult(**r) for r in raw]
```

## Fase 3 — Auth + observability (semana 3)

**Objetivo:** server pronto para multi-user.

### Checklist (HTTP+SSE deploy)

- [ ] Migrar para HTTP+SSE transport
- [ ] Bearer token auth (mínimo) ou OAuth 2.1
- [ ] Per-user scoping em tools (request.user)
- [ ] Audit log estruturado (JSON):

```python
log_entry = {
    "timestamp": iso_now(),
    "user_id": request.user.id,
    "tool": "search",
    "args": sanitize(params.dict()),  # remove PII
    "duration_ms": elapsed,
    "success": True,
    "result_size": len(result)
}
logger.info(json.dumps(log_entry))
```

- [ ] Rate limiting (slowapi ou custom)
- [ ] Health check endpoint
- [ ] Métricas exportadas (Prometheus, Datadog)
- [ ] [[Dicionário de IA#tracing|Tracing]] (OpenTelemetry)

### Pattern de tool com auth

```python
@mcp.tool()
async def get_my_data(request) -> dict:
    """Get data for the authenticated user."""
    user_id = request.user.id  # extracted by middleware
    return db.query("SELECT * FROM data WHERE user_id = ?", user_id)
```

## Fase 4 — Deploy + distribution (semana 4)

**Objetivo:** server rodando 24/7 em produção.

### Checklist

- [ ] Dockerfile minimal
- [ ] CI/CD pipeline (GitHub Actions, etc.)
- [ ] Deploy: K8s, Fly.io, Cloudflare Workers, ou managed
- [ ] TLS (HTTPS) obrigatório
- [ ] Backup de state (se houver)
- [ ] Monitoring + alertas (Sentry, PagerDuty)
- [ ] Documentação operacional (runbook)
- [ ] Versioning semver começando em 1.0.0
- [ ] CHANGELOG.md
- [ ] Release process documentado

### Para servers públicos (extra)

- [ ] README com setup copy-paste
- [ ] Examples folder
- [ ] License (MIT recomendado)
- [ ] Submit ao Awesome MCP Servers
- [ ] Registro em smithery.ai / mcp.so
- [ ] Discord/issues para suporte
- [ ] Versioning rigoroso (breaking = major)

## Best practices distiladas

### Tool design

> [!tip] Os 7 princípios (resumo)
> 1. Nome claro e específico (`search_docs`, não `search`)
> 2. Descrição como docstring (o que, quando, retorna, quando NÃO)
> 3. Inputs tipados com Pydantic
> 4. Outputs compactos e estruturados
> 5. Erros informativos com sugestão
> 6. Sem sobreposição com outras tools
> 7. Idempotência quando possível

Ver [[Anatomia de Agents|03 - Tool design — princípios e categorias]].

### Schemas

```python
# ❌ Ruim
@mcp.tool()
def query(q: str) -> dict:
    """Query."""
    return db.execute(q)

# ✅ Bom
class QueryParams(BaseModel):
    sql: str = Field(..., description="Read-only SQL (SELECT)")
    limit: int = Field(default=100, ge=1, le=1000)

@mcp.tool()
def query_database(params: QueryParams) -> dict:
    """
    Run read-only SQL query against production DB.

    Use for ad-hoc analysis. Returns up to 1000 rows.
    """
    if not params.sql.strip().upper().startswith("SELECT"):
        raise ValueError("Only SELECT queries allowed")
    return db.execute(params.sql, limit=params.limit)
```

### Versioning

```
1.0.0 — initial release
1.1.0 — add new tool (backward compatible)
1.1.1 — bug fix
2.0.0 — breaking: rename tool
```

CHANGELOG documenta migrations.

### Testing

```python
# tests/test_tools.py
import pytest
from my_server.tools import search

def test_search_basic():
    result = search(SearchParams(query="test"))
    assert len(result) > 0
    assert all(r.url for r in result)

def test_search_empty_query():
    with pytest.raises(ValueError, match="cannot be empty"):
        search(SearchParams(query=""))

def test_search_limit():
    result = search(SearchParams(query="test", limit=5))
    assert len(result) <= 5
```

### Logging

```python
import logging
import json

logger = logging.getLogger("mcp-server")

class JSONFormatter(logging.Formatter):
    def format(self, record):
        log_obj = {
            "ts": self.formatTime(record),
            "level": record.levelname,
            "msg": record.getMessage(),
            "module": record.module
        }
        if hasattr(record, "tool_call"):
            log_obj.update(record.tool_call)
        return json.dumps(log_obj)
```

Logs estruturados → ship to Loki/CloudWatch para analysis.

## Anti-patterns (evite!)

- **`-y` install sem audit** — supply chain risk
- **Tools sem schema** — agent passa args errados
- **Output cru** (HTML, JSON gigante) — context rot
- **Server gigante** (50+ tools) — divida em servers especializados
- **Sem audit log** — debugging impossível, compliance impossível
- **Without MCP Inspector na CI** — bugs descobertos só em prod
- **Hardcoded credentials** — env vars sempre
- **Sem rate limiting** (HTTP) — abuse mata budget

## Métricas-alvo

| Métrica | Alvo |
|---|---|
| **Tools por server** | 5-15 |
| **Tokens em descrição de tool** | 50-300 |
| **Tokens em output médio** | <2K |
| **Latência [[Dicionário de IA#tool call\|tool call]] (stdio)** | <100ms |
| **Latência tool call (HTTP)** | <500ms |
| **Uptime (HTTP server)** | >99.9% |
| **Audit log coverage** | 100% |
| **% requests com valid schema** | 100% (validação rigorosa) |

## Quando expandir

| Sinal | Próximo passo |
|---|---|
| Server tem 30+ tools | Quebra em servers especializados |
| Múltiplos times consumindo | Migra para HTTP+SSE com auth |
| Compliance entra em jogo | Audit log persistente + retenção |
| Custo cresce | Rate limiting + caching de outputs |
| Feedback de users | Versioning rigoroso + CHANGELOG |

## Veja também

- [[01 - O que é MCP e por que importa]]
- [[02 - Os três primitivos — Tools, Resources, Prompts]]
- [[05 - Construindo um MCP server local]]
- [[06 - MCP remoto — HTTP + SSE para times]]
- [[07 - Segurança em MCP]]
- [[Anatomia de Agents|03 - Tool design — princípios e categorias]]

## Referências

- **MCP Spec** — *modelcontextprotocol.io/spec*
- **Python SDK** — *github.com/modelcontextprotocol/python-sdk*
- **Best practices Anthropic** — *docs.anthropic.com/mcp/best-practices*
- **MCP Inspector** — *github.com/modelcontextprotocol/inspector*
- **Awesome MCP Servers** — examples canônicos
