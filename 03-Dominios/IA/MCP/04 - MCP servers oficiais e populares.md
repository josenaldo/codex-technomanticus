---
title: "MCP servers oficiais e populares"
created: 2026-04-11
updated: 2026-05-02
type: concept
status: seedling
publish: true
tags:
  - mcp
  - ia
  - servers
aliases:
  - MCP servers
  - Awesome MCP Servers
  - MCP catalog
---

# MCP servers oficiais e populares

> [!abstract] TL;DR
> Em 2026, o ecossistema [[Dicionário de IA#MCP (Model Context Protocol)|MCP]] tem **milhares de servers** disponíveis. Antes de criar próprio, **busque no Awesome MCP Servers** — chance alta de já existir. Categorias principais: filesystem/git, databases, dev tools (GitHub, Linear, Jira), comunicação (Slack, email), browsers (Playwright), busca (web, docs), observabilidade (Sentry, Datadog), AI (Anthropic, OpenAI, Hugging Face). Reuso vence build em 90% dos casos.

## Onde achar

| Recurso | Conteúdo |
|---|---|
| **github.com/punkpeye/awesome-mcp-servers** | Catálogo curated mais conhecido |
| **github.com/modelcontextprotocol/servers** | Servers oficiais Anthropic |
| **mcp.so** | Marketplace web (search + reviews) |
| **smithery.ai** | Discovery + install via CLI |
| **glama.ai/mcp/servers** | Browse + monitoring |

## Categorias principais (2026)

### Filesystem e Git

| Server | Funcionalidades |
|---|---|
| **server-filesystem** (oficial) | read_file, write_file, list_dir, search |
| **server-git** (oficial) | log, diff, blame, status |
| **server-github** (oficial) | issues, PRs, releases, files via API |
| **server-gitlab** | similar para GitLab |

### Databases

| Server | DB |
|---|---|
| **server-postgres** (oficial) | PostgreSQL — read-only por padrão |
| **server-sqlite** (oficial) | SQLite local |
| **mcp-mongodb** | MongoDB |
| **mcp-redis** | Redis |
| **mcp-snowflake** | Snowflake |

> [!warning] DB MCP é vetor de ataque
> Sempre **read-only por default**. Tool de write requer extra permission. Ver [[07 - Segurança em MCP]].

### Dev tools

| Server | Forte em |
|---|---|
| **server-github** | Issues, PRs, code search |
| **mcp-jira** | Issues, sprints, workflows |
| **mcp-linear** | Issues, projects |
| **server-sentry** | Errors, traces, releases |
| **mcp-datadog** | Metrics, logs, alerts |
| **mcp-grafana** | Dashboards, alerts |
| **mcp-pagerduty** | Incidents, oncall |

### Comunicação

| Server | Tipo |
|---|---|
| **mcp-slack** | Mensagens, channels, files |
| **mcp-discord** | Discord servers |
| **mcp-email** | IMAP/SMTP |
| **mcp-google-workspace** | Gmail, Calendar, Drive |
| **mcp-notion** | Pages, databases |
| **mcp-confluence** | Pages, search |

### Browser e web

| Server | Capacidade |
|---|---|
| **mcp-playwright** | Browser automation full |
| **mcp-puppeteer** | Headless Chrome |
| **mcp-fetch** | HTTP fetch básico |
| **mcp-brave-search** | Web search via Brave API |

### Observabilidade e cloud

| Server | Cobertura |
|---|---|
| **mcp-aws** | AWS services via SDK |
| **mcp-gcp** | Google Cloud |
| **mcp-kubernetes** | K8s clusters |
| **mcp-terraform** | Infra-as-code |
| **mcp-cloudflare** | Cloudflare APIs |

### AI e ML

| Server | Funcionalidades |
|---|---|
| **mcp-huggingface** | Models, datasets browse |
| **mcp-langfuse** | LLM traces, evals |
| **mcp-perplexity** | Web search com IA |

### Productivity

| Server | Uso |
|---|---|
| **mcp-obsidian** | Vault Obsidian (este Codex usa!) |
| **mcp-todoist** | Tasks |
| **mcp-calendar** | Calendar via CalDAV |

### Especializados

- **mcp-figma** — design files
- **mcp-stripe** — payments
- **mcp-shopify** — e-commerce
- **mcp-twilio** — SMS, calls
- **mcp-anthropic** — Anthropic API direto

## Servers que vale instalar (defaults sensatos)

Para **dev fullstack** usando [[Dicionário de IA#Claude Code|Claude Code]]/Cursor:

```json
{
  "mcpServers": {
    "filesystem": { "command": "npx", "args": ["-y", "@modelcontextprotocol/server-filesystem", "/home/user/projects"] },
    "git": { "command": "npx", "args": ["-y", "@modelcontextprotocol/server-git"] },
    "github": { "command": "npx", "args": ["-y", "@modelcontextprotocol/server-github"], "env": { "GITHUB_PERSONAL_ACCESS_TOKEN": "${TOKEN}" } },
    "postgres": { "command": "npx", "args": ["-y", "@modelcontextprotocol/server-postgres", "postgresql://localhost/dev"] },
    "fetch": { "command": "npx", "args": ["-y", "@modelcontextprotocol/server-fetch"] }
  }
}
```

Stack mínima cobre 80% das necessidades.

## Como avaliar um MCP server

Antes de instalar:

| Critério | Sinal positivo |
|---|---|
| **Manutenção** | Commits recentes, issues respondidas |
| **Estrelas/forks** | >100 stars indica adoção |
| **Documentação** | README com setup, examples |
| **Schema rigoroso** | Tools com input_schema completo |
| **Auth handling** | Não pede credentials no código |
| **License** | MIT, Apache 2 (compatible) |
| **Test suite** | Tem testes |
| **Provider** | Oficial > comunidade > anonymous |

## Riscos de servers third-party

> [!danger] MCP é vetor de ataque
> Server third-party tem **acesso ao agent**. Risco real:
>
> - Server malicioso lê seus arquivos
> - Server faz [[Dicionário de IA#prompt injection|prompt injection]]
> - Server exfiltra credentials
> - Server reporta atividade
>
> **Audite** antes de instalar — leia código, valide reputação. Server oficial Anthropic > comunidade conhecida > random repo.

Detalhes em [[07 - Segurança em MCP]].

## Quando instalar vs construir

### Instalar quando

✅ Server existe com manutenção ativa
✅ Cobertura ≥80% das suas tools
✅ Provider confiável

### Construir quando

❌ Servers existentes não cobrem domain interno
❌ Lógica acopla a APIs internas que não pode expor
❌ Server existente tem qualidade ruim
❌ Compliance exige zero third-party

Detalhes em [[05 - Construindo um MCP server local]].

## Casos do Codex Technomanticus

Stack pessoal possível:

- **mcp-obsidian** — acessar este vault de qualquer client
- **mcp-github** — gerenciar repos público + apocrypha
- **mcp-fetch** — buscar artigos para fichamento (skill /glosa)
- **mcp-langfuse** — observability dos próprios agents

## Desinstalando

```bash
# Remover do config
# Editar ~/.config/claude/claude_desktop_config.json
# Remover entry "mcpServers" : {...}
# Reiniciar client
```

Servers MCP **não persistem dados fora do disco** (geralmente). Mas verifique TOS/code antes.

## Métricas

| Métrica | Alvo |
|---|---|
| **Servers ativos por client** | 5-15 |
| **Tools por server** | <20 |
| **Latência tool call (local stdio)** | <100ms |
| **Latência tool call (remoto)** | <1s |

## Anti-patterns

- **Instalar tudo do Awesome** — dezenas de servers = LLM confuso
- **Sem audit de servers third-party** — surface de ataque grande
- **Server abandonado em produção** — bug não corrige
- **Reinventar Postgres MCP** — oficial cobre 95% dos casos
- **Client com 50 tools de 10 servers** — context rot na descoberta

## Veja também

- [[01 - O que é MCP e por que importa]]
- [[05 - Construindo um MCP server local]]
- [[07 - Segurança em MCP]]
- [[08 - Ecossistema 2026 — clients e integrações]]

## Referências

- **Awesome MCP Servers** — *github.com/punkpeye/awesome-mcp-servers*
- **MCP oficial** — *github.com/modelcontextprotocol/servers*
- **mcp.so** — marketplace
- **smithery.ai** — discovery + install
- **Anthropic** — *MCP server directory* (2026)
