---
title: "MCP — Model Context Protocol overview para dev"
type: concept
publish: true
created: 2026-05-13
updated: 2026-05-13
status: seedling
tags:
  - claude-code
  - mcp
  - model-context-protocol
  - overview
  - ferramentas
---

# MCP — Model Context Protocol overview para dev

> [!abstract] TL;DR
> MCP (Model Context Protocol) é o protocolo padrão que permite ao Claude Code acessar ferramentas externas: bancos de dados, APIs, browsers, sistemas de arquivo. Um MCP server expõe capabilities (tools, resources, prompts) que o agente pode invocar como se fossem tools nativas. Para o dev que usa Claude Code, MCP é o que faz o agente ter acesso ao contexto que está fora do código.

## O problema que o MCP resolve

Claude Code tem tools nativas: `Read`, `Write`, `Edit`, `Bash`, `Grep`. Com elas, o agente acessa arquivos e executa comandos. Mas não acessa diretamente:

- Banco de dados (só via SQL pelo terminal)
- GitHub Issues e PRs
- Jira, Linear, Notion
- Browser para testar UI
- APIs externas autenticadas

Antes do MCP, a única opção era invocar esses sistemas via Bash, com output de texto bruto que o agente tinha que parsear. Com MCP, o agente tem acesso a ferramentas estruturadas que retornam dados tipados.

## Como o MCP funciona

Um MCP server é um processo que roda localmente (ou remotamente) e expõe um conjunto de tools, resources e prompts via um protocolo padrão (JSON-RPC sobre stdio ou HTTP/SSE).

```
Claude Code ←→ MCP Client ←→ MCP Server ←→ Sistema externo
                (embutido)    (seu processo)  (Postgres, GitHub...)
```

O Claude Code tem um MCP client embutido. Quando você configura um MCP server no `settings.json`, o client inicia o server e expõe suas capabilities ao agente.

## Os três tipos de capability MCP

### Tools

Funções que o agente pode invocar. Similar às tools nativas do Claude Code.

```
Exemplos:
query_database(sql: string) → rows
create_issue(title: string, body: string) → issue_id
navigate_to(url: string) → page_content
```

O agente decide quando invocar uma tool baseado no contexto. O resultado volta ao agente como dados estruturados.

### Resources

Dados que o agente pode ler, como arquivos — mas de sistemas externos.

```
Exemplos:
database://schema         → estrutura das tabelas
github://repo/main/README → conteúdo de arquivo no GitHub
```

Resources são somente leitura, diferente de tools que podem ter efeitos colaterais.

### Prompts

Templates de instrução que o agente pode invocar para executar workflows pré-definidos.

```
Exemplos:
/debug-query → template para análise de query lenta
/review-migration → template para revisar uma migration de banco
```

## Configuração básica em settings.json

```json
{
  "mcpServers": {
    "postgres": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-postgres"],
      "env": {
        "DATABASE_URL": "postgresql://user:pass@localhost:5432/mydb"
      }
    }
  }
}
```

Quando Claude Code inicia, ele lança o processo `npx @modelcontextprotocol/server-postgres`, conecta via stdio, e as tools do server ficam disponíveis na sessão.

## MCP server vs tool nativa

| | Tool nativa | MCP tool |
|--|-------------|----------|
| Onde fica | Embutida no Claude Code | Servidor externo |
| Como acessa | Chamada direta | Via MCP client → server |
| Contexto disponível | Arquivos locais | Qualquer sistema externo |
| Estado | Sem estado persistente | Server pode ter estado |
| Exemplo | `Bash`, `Read`, `Edit` | `query_db`, `create_pr` |

## Por que o dev precisa entender MCP

Para **usar** Claude Code produtivamente, basta saber:
1. Quais MCP servers existem para o seu stack
2. Como configurar em `settings.json`
3. Que as tools do server aparecem naturalmente na sessão

Para **personalizar** o agente para o projeto:
1. Criar MCP servers para ferramentas internas
2. Expor dados do projeto como resources
3. Compor skills + MCP para workflows completos

## Ecossistema de MCP servers

Anthropic e a comunidade mantêm servers para os casos de uso mais comuns:

- **@modelcontextprotocol/server-postgres** — queries SQL diretas
- **@modelcontextprotocol/server-github** — PRs, Issues, código
- **@modelcontextprotocol/server-filesystem** — acesso mais granular ao filesystem
- **@modelcontextprotocol/server-brave-search** — pesquisa web
- **@modelcontextprotocol/server-puppeteer** — browser automation

Ver [[03-Dominios/IA/Claude Code/Skills e MCP/05 - MCP servers essenciais|05 - MCP servers essenciais]] para configuração e casos de uso de cada um.

## Armadilhas

**MCP server com acesso a produção**: um MCP postgres apontando para o banco de produção significa que o agente pode rodar `DROP TABLE` em produção. Configure guardrails antes de conectar MCP servers em ambientes críticos.

**Latência do server**: cada invocação de tool MCP é uma chamada ao server. Servers lentos tornam a sessão lenta. Para dados que não mudam (schema do banco, lista de projetos), considere cachear no server.

**Segredos no settings.json**: `DATABASE_URL` com senha no `settings.json` do projeto é um segredo commitado. Use variáveis de ambiente do sistema operacional em vez de valores inline.

```json
{
  "mcpServers": {
    "postgres": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-postgres"],
      "env": {
        "DATABASE_URL": "${DATABASE_URL}"  // Lê da env do sistema
      }
    }
  }
}
```

## Veja também

- [[03-Dominios/IA/Claude Code/Skills e MCP/05 - MCP servers essenciais|05 - MCP servers essenciais]] — servers prontos para usar
- [[03-Dominios/IA/Claude Code/Skills e MCP/06 - Criar MCP server|06 - Criar MCP server]] — quando e como criar um server customizado
- [[03-Dominios/IA/Claude Code/Skills e MCP/07 - Compondo skills e MCP|07 - Compondo skills e MCP]] — skills + MCP para agentes especializados
- [[03-Dominios/IA/Claude Code/Configuração/04 - settings.json|04 - settings.json]] — configuração completa de MCP no settings.json
- [[03-Dominios/IA/Claude Code/Skills e MCP/index|Skills e MCP]] — índice do galho
