---
title: "Casos comuns no mercado"
created: 2026-04-11
updated: 2026-05-02
type: concept
progress: backlog
status: seedling
publish: true
tags:
  - mcp
  - ia
  - casos
aliases:
  - Casos MCP
  - MCP use cases
  - MCP casos reais
---

# Casos comuns no mercado

> [!abstract] TL;DR
> Em 2026, [[Dicionário de IA#MCP (Model Context Protocol)|MCP]] virou padrão em **5 categorias** de uso: (1) **dev tools internos** (codebase, internal APIs), (2) **integrações cross-tool** (mesmo server, múltiplos clients), (3) **[[Dicionário de IA#Agent|agents]] corporativos** (workflows internos), (4) **assistentes pessoais** (vault, calendar, email), (5) **distribuição de capabilities** (publicar server público). Esta nota dá exemplos concretos por categoria + boas práticas. Reconhecer o caso certo é metade do trabalho.

## Caso 1 — Dev tools internos

> *"Meu time tem API/codebase complexa. Quero que devs falem com ela em natural language em qualquer client."*

### Setup

- [[Dicionário de IA#MCP server|MCP server]] interno expondo APIs/serviços críticos
- Hospedado internamente (HTTP+SSE em K8s)
- Auth via SSO corporativo (OAuth 2.1)
- Audit log para compliance
- Devs configuram nos seus clients ([[Dicionário de IA#Claude Code|Claude Code]], Cursor)

### Tools típicas

```python
@mcp.tool()
def get_service_status(service_name: str) -> dict:
    """Get current status of internal service."""

@mcp.tool()
def query_user(user_id: str) -> User:
    """Get user info from internal user-service API."""

@mcp.tool()
def deploy_to_staging(service: str, version: str) -> str:
    """Deploy service to staging. REQUIRES human approval."""
```

### Vantagens vs alternativas

| | MCP server interno | API direto |
|---|---|---|
| Cross-client | ✅ Reusa em todos | ❌ Cada IDE/CLI implementa |
| Onboarding | ✅ Plug-and-play | ❌ Manual |
| Auth uniforme | ✅ OAuth central | ⚠️ Fragmentado |
| Audit log | ✅ Centralizado | ⚠️ Por integration |

### Caso real

Empresa de telecom com microservices. MCP server interno expõe top 30 APIs. Devs de 5 times consomem em Claude Code/Cursor sem precisar conhecer endpoints. Onboard de novo dev passou de 2 semanas para 3 dias.

## Caso 2 — Integrações cross-tool

> *"Já uso 5 ferramentas (GitHub, Linear, Slack, etc.). Quero que LLM em qualquer client integre com tudo."*

### Setup

- Instalar Awesome MCP servers correspondentes
- Configurar auth (PATs, API keys via env)
- Cada client (Claude Desktop, Cursor) tem mesmo set de servers

### Stack típica

```json
{
  "mcpServers": {
    "github": { "command": "npx", "args": ["-y", "@modelcontextprotocol/server-github"], "env": {"GITHUB_PERSONAL_ACCESS_TOKEN": "${TOKEN}"} },
    "linear": { "command": "npx", "args": ["-y", "mcp-linear"], "env": {"LINEAR_API_KEY": "${KEY}"} },
    "slack": { "command": "npx", "args": ["-y", "mcp-slack"], "env": {"SLACK_BOT_TOKEN": "${TOKEN}"} },
    "notion": { "command": "npx", "args": ["-y", "mcp-notion"], "env": {"NOTION_API_KEY": "${KEY}"} }
  }
}
```

### Workflow exemplo

```
User: "Crie issue Linear sobre o bug que reportei no PR #123, e me chame no Slack quando review estiver pronto"

LLM:
1. github.get_pr(123) → reads PR
2. linear.create_issue(title=..., description=..., labels=["bug"])
3. slack.set_reminder("@me", "Review #123 ready")
```

3 servers, 1 conversa. Em 2024 isso requeria custom integration.

## Caso 3 — Agents corporativos

> *"Empresa quer agent que executa workflows internos com auditabilidade."*

### Setup

- MCP servers internos com **all destrutivas com human-in-the-loop**
- Slack approval flow integrado
- Compliance log (SOX, GDPR, etc.)
- Permissões fine-grained por user/role

### Tools típicas

```python
@mcp.tool()
async def refund_customer(
    customer_id: str,
    amount: float,
    reason: str
) -> dict:
    """Process refund. ALWAYS requires Manager approval via Slack."""
    if amount > 100:
        approval = await request_slack_approval(
            channel="#refunds-approval",
            payload={"customer_id": customer_id, "amount": amount, "reason": reason}
        )
        if not approval.approved:
            return {"status": "rejected", "by": approval.user}

    return await stripe.refund(customer_id, amount, reason=reason)
```

### Compliance

Cada tool call:
- Logged with user, timestamp, args, result
- Stored em DB imutável (write-once)
- Retenção 7 anos
- Audit dashboards (Grafana)

### Caso real

Empresa SaaS B2B. Agent de customer success automatizou 70% das ações repetitivas (refunds <$100, account upgrades, etc). 30% restantes vão para humano via Slack approval. Tempo médio de resolution caiu 60%.

## Caso 4 — Assistentes pessoais

> *"Quero meu LLM acessando minha vida digital — vault, calendar, email, tasks."*

### Setup pessoal

```json
{
  "mcpServers": {
    "obsidian": { "command": "uvx", "args": ["mcp-obsidian", "/home/user/vault"] },
    "calendar": { "command": "npx", "args": ["-y", "mcp-google-workspace"], "env": {"GOOGLE_OAUTH_TOKEN": "${TOKEN}"} },
    "todoist": { "command": "npx", "args": ["-y", "mcp-todoist"], "env": {"TODOIST_API_TOKEN": "${TOKEN}"} },
    "email": { "command": "npx", "args": ["-y", "mcp-imap"], "env": {"IMAP_PASSWORD": "${PASS}"} }
  }
}
```

### Workflows típicos

- "Resuma minhas reuniões da semana e crie tasks de follow-up no Todoist"
- "Adicione nota ao vault sobre essa conversa"
- "Quem mencionou X em emails dos últimos 30 dias?"

### Caveats

- Privacidade: tudo pessoal exposto ao agent
- Auth tokens devem ter scopes mínimos (read-only quando possível)
- Audit pessoal (você verifica)

### Caso real (este Codex)

[[Memória de Agentes|index]] como MCP server. Claude Code acessa vault, propõe conexões, sugere notas. Skill `/glosa` (este vault) usa MCP fetch para buscar artigos.

## Caso 5 — Distribuição de capabilities (publishing)

> *"Construí algo útil. Quero distribuir como MCP server público."*

### Setup

- Server limpo (sem creds harcoded)
- README claro com setup
- Versionamento semver
- Tests
- Submit para Awesome MCP Servers
- Registro em smithery.ai / mcp.so

### Considerações

- **Auth e security** — você é responsável se server vazar dados de users
- **Manutenção** — issues, PRs, atualizações
- **Versioning discipline** — breaking changes precisam ser major
- **License** — MIT é padrão

### Caso real

Dev solo cria `mcp-spotify` com 5 tools (playback, search, playlist). Awesome MCP Servers, 200 stars em 3 meses, 50K downloads. Vira projeto side-passive.

## Patterns que se repetem

### Pattern 1 — Server core + adapters

```
mcp-jira-core (read-only)         ← oficial, manutenção ativa
  ↑
mcp-jira-write (extends core)     ← user adiciona capabilities
mcp-jira-corporate-auth (extends) ← empresa specific
```

Composição em vez de fork.

### Pattern 2 — Server pipeline

```
LLM → MCP server A → MCP server B → result
```

Server A delega para Server B. Útil quando há orchestração.

### Pattern 3 — Multi-tenant single server

Um server, vários tenants. Auth determina what each tenant vê.

```python
@mcp.tool()
async def query_data(request, query: str):
    tenant = request.user.tenant_id
    return db.query_filtered_by_tenant(tenant, query)
```

## Quando NÃO usar MCP em produção

❌ **Latência ultra-crítica (<50ms total)** — overhead do protocol
❌ **Aplicação consumer high-volume** — onerosa em escala alta
❌ **Domínio com requisitos específicos não cobertos pela spec**
❌ **Time muito pequeno sem capacity para manter servers**

## Lições aprendidas (2025-2026)

> [!quote] Insights da indústria
>
> **De Anthropic:** *"MCP foi sucesso porque resolve N×M; não tente fazer ele resolver tudo."*
>
> **De adopters enterprise:** *"Audit log é não-negociável. Sem isso, compliance bloqueia adoção."*
>
> **De solo devs:** *"Reusar 5 servers do Awesome economiza meses vs construir tudo."*
>
> **De security teams:** *"MCP server é supply chain. Trate como dependência crítica."*

## Métricas para acompanhar

| Métrica | Por que importa |
|---|---|
| % chamadas com sucesso | Health do server |
| Latência p95 | UX |
| Custo per call | Budget |
| % com human approval | Compliance |
| Audit log completeness | Auditability |

## Veja também

- [[01 - O que é MCP e por que importa]]
- [[04 - MCP servers oficiais e populares]]
- [[06 - MCP remoto — HTTP + SSE para times]]
- [[07 - Segurança em MCP]]
- [[10 - Setup completo + best practices]]

## Referências

- **Anthropic** — *MCP case studies* (blog series 2025-2026)
- **Awesome MCP Servers** — examples por categoria
- **Cloudflare** — *MCP in production* (blog)
