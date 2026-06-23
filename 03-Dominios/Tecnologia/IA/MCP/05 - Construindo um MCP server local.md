---
title: "Construindo um MCP server local"
created: 2026-04-11
updated: 2026-05-02
type: concept
progress: backlog
status: seedling
publish: true
tags:
  - mcp
  - ia
  - construcao
aliases:
  - Construir MCP server
  - MCP server tutorial
  - MCP server local
---

# Construindo um MCP server local

> [!abstract] TL;DR
> Construir [[Dicionário de IA#MCP server|MCP server]] é simples: [[Dicionário de IA#SDK|SDK]] Python ou TypeScript + decorators + ~50 linhas de código. Use stdio (subprocess local) para começar. Defina tools com schema Pydantic/Zod, retorne tipos estruturados, escreva descrições claras (60% do trabalho — ver [[Anatomia de Agents|03 - Tool design — princípios e categorias]]). Teste com **MCP Inspector** antes de plugar em client real. Para algo public, considere semver, docs, examples. Para algo interno, basta o essencial.

## Setup mínimo (Python)

```bash
# Install SDK
pip install mcp
# ou
uv add mcp
```

## Hello world

```python
# server.py
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("my-server")

@mcp.tool()
def add(a: int, b: int) -> int:
    """Add two numbers."""
    return a + b

@mcp.tool()
def greet(name: str) -> str:
    """Greet a person by name."""
    return f"Hello, {name}!"

if __name__ == "__main__":
    mcp.run()  # default: stdio
```

Pronto. Tem MCP server funcional.

## Configurar no client

```json
{
  "mcpServers": {
    "my-server": {
      "command": "python",
      "args": ["/path/to/server.py"]
    }
  }
}
```

Restart client → tools `add` e `greet` aparecem disponíveis.

## Adicionando resources

```python
@mcp.resource("file://{path}")
def read_file(path: str) -> str:
    """Read file from filesystem."""
    with open(path) as f:
        return f.read()

@mcp.resource("config://settings")
def get_settings() -> dict:
    """Application settings."""
    return {"theme": "dark", "lang": "pt-br"}
```

URI patterns: `{path}` é capturado como argumento.

## Adicionando prompts

```python
from mcp.types import Message

@mcp.prompt()
def explain_code(language: str, code: str) -> list[Message]:
    """Explain code in plain English."""
    return [
        Message(role="system", content=f"You are an expert {language} dev."),
        Message(role="user", content=f"Explain this code:\n\n{code}")
    ]
```

## Schemas tipados

Pydantic é amigo:

```python
from pydantic import BaseModel, Field
from typing import Literal

class QueryParams(BaseModel):
    sql: str = Field(..., description="SQL query (SELECT only)")
    limit: int = Field(default=100, ge=1, le=1000)
    format: Literal["json", "csv"] = "json"

@mcp.tool()
def query_db(params: QueryParams) -> dict:
    """Run read-only SQL query against the database."""
    if not params.sql.strip().upper().startswith("SELECT"):
        raise ValueError("Only SELECT queries allowed")
    rows = db.execute(params.sql, limit=params.limit)
    return {"rows": rows, "format": params.format}
```

Schema é auto-gerado pelo SDK a partir dos type hints + Pydantic.

## TypeScript (alternativa)

```bash
npm install @modelcontextprotocol/sdk
```

```typescript
import { McpServer } from "@modelcontextprotocol/sdk/server/mcp.js";
import { StdioServerTransport } from "@modelcontextprotocol/sdk/server/stdio.js";
import { z } from "zod";

const server = new McpServer({
  name: "my-server",
  version: "1.0.0"
});

server.tool(
  "add",
  { a: z.number(), b: z.number() },
  async ({ a, b }) => ({
    content: [{ type: "text", text: String(a + b) }]
  })
);

const transport = new StdioServerTransport();
await server.connect(transport);
```

API similar, mais verbose. Use Python se tem opção.

## Tool design — o que importa

Tool design é **60% do trabalho** (ver [[Anatomia de Agents|03 - Tool design — princípios e categorias]]).

### Bom

```python
@mcp.tool()
def search_jira_issues(
    query: str = Field(description="JQL or free text query"),
    project: str = Field(description="Project key (e.g. PROJ)"),
    status: Literal["open", "in_progress", "done"] = None,
    limit: int = 20
) -> list[Issue]:
    """
    Search Jira issues matching criteria.

    Use when user asks about specific tickets, bugs, or tasks.
    Returns issues with id, title, status, assignee, priority.

    Do NOT use for creating issues (use create_issue instead).
    """
    return jira.search(query, project, status, limit)
```

### Ruim

```python
@mcp.tool()
def search(query: str) -> list:
    """Search."""
    return jira.search(query)
```

Diferença: o segundo deixa o LLM adivinhando.

## Erros informativos

```python
@mcp.tool()
def query_db(sql: str) -> dict:
    """Run SQL query."""
    if "DROP" in sql.upper():
        raise ValueError(
            "DROP statements forbidden. Use migration_tool for schema changes."
        )
    try:
        return db.execute(sql)
    except DatabaseError as e:
        raise ValueError(
            f"Query failed: {e}. Check table name with list_tables() first."
        )
```

Erros viram **feedback** que o agent usa para auto-correção.

## Output compacto

```python
# Errado
@mcp.tool()
def get_logs(service: str) -> str:
    return open(f"/var/log/{service}.log").read()  # 100MB

# Certo
@mcp.tool()
def get_logs(
    service: str,
    lines: int = 100,
    level: Literal["error", "warn", "info"] = None
) -> dict:
    """Get recent logs from service."""
    logs = read_log(service, tail=lines, filter_level=level)
    return {"lines": logs, "total_count": len(logs), "service": service}
```

Compactação evita context rot.

## Testando com MCP Inspector

```bash
# Roda inspector + conecta ao seu server
npx @modelcontextprotocol/inspector python server.py
```

UI web em http://localhost:5173:

- Lista tools/resources/prompts
- Permite invocar manualmente
- Mostra request/response raw
- Valida schemas

**Sempre teste no Inspector antes de plugar em client.**

## Logging e debugging

```python
import logging
logging.basicConfig(level=logging.INFO, format="[%(asctime)s] %(message)s")
logger = logging.getLogger("my-mcp-server")

@mcp.tool()
def query_db(sql: str) -> dict:
    logger.info(f"Tool called: query_db, sql={sql[:100]}")
    result = db.execute(sql)
    logger.info(f"Returned {len(result)} rows")
    return result
```

Logs vão para stderr (não interferem em stdio do JSON-RPC). Em produção, redirecionar para arquivo ou Loki.

## Dependências externas

```python
# Use env vars para credentials
import os
DB_URL = os.environ["DATABASE_URL"]

# OU passar via args do client
import sys
DB_URL = sys.argv[1] if len(sys.argv) > 1 else os.environ.get("DATABASE_URL")
```

No client config:

```json
{
  "mcpServers": {
    "my-db": {
      "command": "python",
      "args": ["server.py"],
      "env": {
        "DATABASE_URL": "${DB_URL}"
      }
    }
  }
}
```

## Empacotamento

### Para uso pessoal/projeto

Server local, roda direto. Sem packaging.

### Para distribuir

```bash
# Python — uvx
# pyproject.toml com entry_points
[project.scripts]
my-mcp-server = "my_package.server:main"

# Usuários:
uvx my-mcp-server
```

```bash
# TypeScript — npx
# package.json com bin
{
  "bin": {
    "my-mcp-server": "./dist/server.js"
  }
}

# Usuários:
npx my-mcp-server
```

Convenção em 2026: distribuir via `uvx` (Python) ou `npx` (TS) — sem install global.

## Versionamento

```python
mcp = FastMCP("my-server", version="1.2.0")
```

Semver:
- **Major** — breaking change em tool signatures
- **Minor** — adiciona tool/resource/prompt
- **Patch** — fix interno

Documente changes em CHANGELOG.

## Anti-patterns

- **Tools sem descrição** — agent escolhe errado
- **Output bruto** — context rot
- **Sem tipo no input** — Pydantic estrutura, schema auto
- **Credentials em código** — env vars sempre
- **Sem testes via Inspector** — bugs descobertos só em prod
- **Server gigante (50+ tools)** — divida em servers especializados
- **Side effects sem confirmação** — ações destrutivas precisam ser explícitas

## Métricas

| Métrica | Alvo |
|---|---|
| **Tools por server** | 5-15 |
| **Latência [[Dicionário de IA#tool call\|tool call]]** | <100ms (local) |
| **Tokens em tool description** | 50-300 |
| **Tokens em output médio** | <2K |
| **% testes passando antes de release** | 100% |

## Veja também

- [[01 - O que é MCP e por que importa]]
- [[02 - Os três primitivos — Tools, Resources, Prompts]]
- [[03 - Arquitetura cliente-servidor]]
- [[06 - MCP remoto — HTTP + SSE para times]]
- [[07 - Segurança em MCP]]
- [[Anatomia de Agents|03 - Tool design — princípios e categorias]]

## Referências

- **MCP Python SDK** — *github.com/modelcontextprotocol/python-sdk*
- **MCP TypeScript SDK** — *github.com/modelcontextprotocol/typescript-sdk*
- **MCP Inspector** — *github.com/modelcontextprotocol/inspector*
- **Anthropic tutorial** — *Building MCP servers* (2025)
