---
title: "MCP — o protocolo universal"
created: 2026-05-02
updated: 2026-05-02
type: concept
status: seedling
publish: true
tags:
  - agentes-codificacao
  - ia
  - ferramentas
aliases:
  - MCP
  - Model Context Protocol
  - Protocolo de contexto
---

# MCP — o protocolo universal

> [!abstract] TL;DR
> O Model Context Protocol (MCP) é um padrão aberto criado pela Anthropic que define como agentes AI se conectam com ferramentas externas (bancos de dados, APIs, file systems, browsers). É o "USB da IA" — uma interface universal que permite que qualquer agente use qualquer ferramenta sem integração custom. Em 2026, Claude Code, Cursor, Gemini CLI e harnesses open source suportam MCP. Saber configurar MCP servers é a skill que transforma um agente genérico em um agente específico para o seu projeto.

## O que é

**MCP** é um protocolo de comunicação entre:

- **Host** — o agente AI (Claude Code, Cursor, etc.)
- **Server** — uma ferramenta ou serviço (PostgreSQL, GitHub, browser, etc.)
- **Client** — a ponte entre host e server (geralmente embutida no host)

O protocolo define três primitivas:

| Primitiva     | O que faz                         | Exemplo                                     |
| ------------- | --------------------------------- | ------------------------------------------- |
| **Tools**     | Ações que o modelo pode invocar   | `read_file`, `execute_sql`, `search_github` |
| **Resources** | Dados que o modelo pode ler       | Schemas de BD, documentação, configs        |
| **Prompts**   | Templates de prompt pré-definidos | `analyze-pr`, `explain-error`               |

## Por que importa

Sem MCP, cada ferramenta precisa de integração custom com cada agente — N×M integrações. Com MCP, cada ferramenta implementa o protocolo uma vez e funciona com qualquer agente — N+M integrações.

## Como funciona

### Arquitetura

```mermaid
graph LR
    A[Agent Host] --> B[MCP Client]
    B --> C[MCP Server 1: PostgreSQL]
    B --> D[MCP Server 2: GitHub]
    B --> E[MCP Server 3: Browser]
    B --> F[MCP Server 4: Custom]
```

### Configuração em Claude Code

```json
// .claude/mcp.json
{
  "servers": {
    "postgres": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-postgres"],
      "env": {
        "DATABASE_URL": "postgresql://user:pass@localhost/mydb"
      }
    },
    "github": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-github"],
      "env": {
        "GITHUB_TOKEN": "${GITHUB_TOKEN}"
      }
    },
    "filesystem": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-filesystem", "/path/to/docs"]
    }
  }
}
```

### MCP Servers populares (2026)

| Server                | O que faz                 | Uso                         |
| --------------------- | ------------------------- | --------------------------- |
| `server-postgres`     | Query e schema inspection | Debugging de BD, migrações  |
| `server-github`       | Issues, PRs, files        | Workflow de desenvolvimento |
| `server-filesystem`   | Leitura de arquivos       | Documentação, configs       |
| `server-brave-search` | Busca na web              | Pesquisa técnica            |
| `server-puppeteer`    | Browser automation        | Testes visuais              |
| `server-slack`        | Mensagens e canais        | Notificações                |

### Criando um MCP Server custom

```typescript
// server.ts - exemplo mínimo
import { McpServer } from "@modelcontextprotocol/sdk/server/mcp.js";

const server = new McpServer({ name: "my-project-tools" });

// Registrar uma tool
server.tool(
  "get_user_count",
  "Returns the current number of active users",
  {},
  async () => {
    const count = await db.query("SELECT COUNT(*) FROM users WHERE active = true");
    return { content: [{ type: "text", text: `Active users: ${count}` }] };
  }
);

// Registrar um resource
server.resource(
  "api-schema",
  "openapi://schema",
  async () => ({
    contents: [{
      uri: "openapi://schema",
      mimeType: "application/json",
      text: JSON.stringify(openApiSpec)
    }]
  })
);
```

## Quando usar

| Cenário                                     | MCP ajuda?                     |
| ------------------------------------------- | ------------------------------ |
| Agente precisa consultar banco de dados     | ✅ server-postgres              |
| Agente precisa criar issues/PRs             | ✅ server-github                |
| Agente precisa acessar documentação interna | ✅ server-filesystem            |
| Tarefa simples de edição de código          | ❌ Overkill                     |
| Integração one-off com API externa          | ⚠️ Pode valer se for recorrente |

## Armadilhas

- **Muitos servers = muitos tokens** — cada server registra tools no contexto. 10 servers com 5 tools cada = 50 tool definitions = muitos tokens de input.
- **Security** — MCP servers podem ter acesso a dados sensíveis (BD, GitHub tokens). Configure credenciais com cuidado e restrinja permissões.
- **"MCP para tudo"** — nem toda integração precisa de MCP. Para tarefas simples, um script bash direto é mais eficiente.
- **Servers instáveis** — servers comunitários podem ter bugs. Teste antes de confiar em produção.

## Veja também

- [[05 - Claude Code — terminal-first agent]] — MCP em Claude Code
- [[16 - O loop agentic — plan, act, observe]] — como tools MCP se encaixam no loop
- [[11 - Comparativo — qual ferramenta para qual tarefa]] — quais ferramentas suportam MCP
- [[03-Dominios/IA/Claude Code/Skills e MCP/index|Skills e MCP — Claude Code]] — como usar MCP servers no Claude Code e criar servers customizados

## Referências

- **Anthropic** — *Model Context Protocol Specification* (2026). Spec oficial.
- **ModelContextProtocol** — *GitHub Organization* (github.com/modelcontextprotocol). Código e servers.
- **MCP Hub** — *Server Directory* (2026). Catálogo de MCP servers disponíveis.
