---
title: "Os três primitivos — Tools, Resources, Prompts"
created: 2026-04-11
updated: 2026-05-02
type: concept
status: seedling
publish: true
tags:
  - mcp
  - ia
  - primitivos
aliases:
  - MCP primitivos
  - Tools Resources Prompts
  - MCP primitives
---

# Os três primitivos — Tools, Resources, Prompts

> [!abstract] TL;DR
> [[Dicionário de IA#MCP (Model Context Protocol)|MCP]] define **três tipos** de capability que servers expõem: **[[Dicionário de IA#tools (MCP)|Tools]]** (funções executáveis com side-effects, query_db, send_email), **[[Dicionário de IA#resources (MCP)|Resources]]** (dados leitáveis estáticos ou dinâmicos, files, schemas), e **[[Dicionário de IA#prompts (MCP)|Prompts]]** (templates parametrizáveis para tarefas comuns). Cada primitivo tem semântica diferente — confundir os três é o erro de design mais comum. **Tools modificam, Resources informam, Prompts parametrizam.**

## A tríade

```
TOOLS                RESOURCES              PROMPTS
─────                ─────────              ───────
Funções executáveis  Dados leitáveis        Templates
com side-effects     estáticos/dinâmicos    parametrizáveis

query_db(sql)        file://path/doc.md     "Explain this code"
send_email(to, ..)   schema://table/users   "Summarize {input}"
write_file(...)      git://commits/HEAD     "Refactor for {style}"
```

A regra simples:

- **Tool** = "execute para mim"
- **Resource** = "me mostre"
- **Prompt** = "use este template"

## Tools — funções executáveis

```python
@server.tool()
def query_database(sql: str) -> list[dict]:
    """Run SELECT query on production database."""
    return db.execute(sql)

@server.tool()
def send_slack_message(channel: str, message: str) -> bool:
    """Send message to Slack channel."""
    return slack.post(channel, message)
```

**Características:**
- Pode ter **side-effects** (mudar estado)
- [[Dicionário de IA#LLM (Large Language Model)|LLM]] **chama explicitamente**: "preciso enviar mensagem"
- Schema de input/output
- Tipicamente requer auth/permission

**Quando usar Tool:**
- Ação que muda o mundo (write, delete, send)
- Computação que requer compute (call API, run query)
- Descoberta dinâmica ("liste todos os arquivos modificados hoje")

## Resources — dados leitáveis

```python
@server.resource("file://{path}")
async def read_file(path: str) -> str:
    """Read file from filesystem."""
    return open(path).read()

@server.resource("schema://table/{table_name}")
async def db_schema(table_name: str) -> dict:
    """Get database schema for table."""
    return introspect(table_name)
```

**Características:**
- **Read-only** (sem side-effects)
- LLM **navega** ou client puxa proativamente
- URI-based (parecido com URL)
- Pode ser **subscribed** (notify on change)

**Quando usar Resource:**
- Dado estático ou semi-estático
- Browseable / discoverable
- Cliente quer carregar antecipadamente
- Read sem necessidade de "tool call"

**Diferença operacional:** o cliente pode **carregar Resources no contexto** sem pedir ao LLM. Tools precisam ser invocadas pelo LLM.

## Prompts — templates parametrizáveis

```python
@server.prompt()
def explain_code(language: str, code: str) -> list[Message]:
    """Explain code in plain English."""
    return [
        Message(role="system", content=f"You are an expert {language} developer."),
        Message(role="user", content=f"Explain this code:\n\n{code}")
    ]

@server.prompt()
def code_review(diff: str, focus: str = "security") -> list[Message]:
    """Generate code review with focus on specific concern."""
    return [...]
```

**Características:**
- **Templates pré-fabricados** que retornam mensagens
- Reutilizam expertise (alguém escreveu o prompt bem)
- LLM ou usuário invoca: "use the code-review prompt"
- Parametrizáveis com inputs

**Quando usar Prompt:**
- Tarefa recorrente que tem prompt-padrão bom
- Onboarding de usuários menos técnicos
- Compartilhar best practices via MCP server

## Tabela comparativa

| | Tools | Resources | Prompts |
|---|---|---|---|
| **Modifica estado?** | Sim | Não | Não |
| **Quem invoca?** | LLM decide | Client puxa ou LLM | LLM ou user |
| **Auth?** | Tipicamente requer | Pode requerer | Geralmente não |
| **Schema?** | Input + output | URI pattern | Argumentos |
| **Quando carregar?** | Sob demanda (decisão LLM) | Pode ser proativo | Sob demanda |
| **Custo típico** | Variável (chamadas externas) | Baixo (read) | Mínimo |

## Anti-pattern clássico — confundir os três

### Tool quando deveria ser Resource

```python
# Anti-pattern
@server.tool()
def get_user_schema():
    """Get schema of users table."""
    return schema_users

# Melhor
@server.resource("schema://users")
def users_schema():
    return schema_users
```

Por quê: schema é **read-only, navegável**. LLM não deveria precisar "decidir chamar" — client carrega proativamente.

### Resource quando deveria ser Tool

```python
# Anti-pattern
@server.resource("query://users-active")
def active_users_resource():
    """All currently active users."""  # Mas... se "agora" é dinâmico?
    return db.query("SELECT * WHERE active = true")
```

Por quê: query custosa que muda o tempo todo. Melhor como Tool com parâmetros.

### Tool quando deveria ser Prompt

```python
# Anti-pattern
@server.tool()
def explain_code(code: str) -> str:
    """Explain code."""
    response = llm.complete(f"Explain: {code}")
    return response

# Melhor — Prompt
@server.prompt()
def explain_code_prompt(code: str) -> list[Message]:
    """Returns prompt for code explanation."""
    return [Message(role="user", content=f"Explain: {code}")]
```

Por quê: tool ABRE outra LLM call. Prompt é **template** que o **client/LLM atual** usa. Mais barato, mais flexível.

## Discovery flow

Quando client conecta a server:

```
1. Client → Server: "list_tools()"
   Server → Client: [tool schemas]

2. Client → Server: "list_resources()"
   Server → Client: [resource URIs]

3. Client → Server: "list_prompts()"
   Server → Client: [prompt templates]

4. LLM decide o que usar baseado em:
   - User question
   - Tool descriptions
   - Resource URIs visíveis
```

Cliente bom **não floda LLM com todos** — filtra por relevância antes de incluir no contexto.

## Combinando os três — exemplo real

GitHub MCP server expõe:

**Tools:**
- `create_issue(title, body)`
- `merge_pr(pr_number)`
- `add_comment(pr, text)`

**Resources:**
- `repo://owner/repo/files/{path}` — ler arquivo
- `repo://owner/repo/issues/{number}` — ler issue
- `repo://owner/repo/prs/{number}` — ler PR

**Prompts:**
- `review-pr` — template de code review com checklist
- `triage-issue` — template para classificar issue

LLM combina: "leia o PR (resource) → use prompt review-pr → comenta (tool)".

## Métricas

| Métrica | Alvo |
|---|---|
| **Tools por server** | <20 (mais que isso vira confuso) |
| **Resources por server** | Variável, mas agrupados logicamente |
| **Prompts por server** | <10 (templates bem trabalhados) |
| **Discovery latency** | <100ms |

## Anti-patterns

- **Tudo é tool** — ignora resources e prompts
- **Tools com nomes ambíguos** — `query`, `find`, `get`
- **Resources sem URI scheme claro** — descoberta confusa
- **Prompts sem documentação** — usuário não sabe quando usar
- **Tool fazendo read** — deveria ser resource
- **Resource fazendo computação cara** — deveria ser tool

## Veja também

- [[01 - O que é MCP e por que importa]]
- [[03 - Arquitetura cliente-servidor]]
- [[05 - Construindo um MCP server local]]
- [[Anatomia de Agents|03 - Tool design — princípios e categorias]]

## Referências

- **MCP Spec** — *Tools, Resources, Prompts sections* (modelcontextprotocol.io)
- **Anthropic** — *Building MCP servers tutorial* (2025)
- **Awesome MCP Servers** — examples canônicos
