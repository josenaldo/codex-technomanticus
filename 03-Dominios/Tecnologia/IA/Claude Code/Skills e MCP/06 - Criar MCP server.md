---
title: "Criar MCP server — quando e como"
type: concept
progress: published
publish: true
created: 2026-05-13
updated: 2026-06-27
status: evergreen
tags:
  - claude-code
  - mcp
  - desenvolvimento
  - customizacao
  - server
---

# Criar MCP server — quando e como

> [!abstract] TL;DR
> Crie um [[Dicionário de IA#MCP server|MCP server]] quando o projeto tem ferramentas internas, APIs privadas, ou dados estruturados que nenhum server existente acessa. O custo mínimo é baixo: 50-100 linhas de TypeScript que expõem uma ou duas tools. O SDK oficial cuida do protocolo; você cuida só da lógica de negócio.

## A pergunta certa antes de começar

Criar um MCP server customizado é o caminho errado na maioria das vezes. Antes de escrever código, responda:

1. **Existe um server pronto?** — Consulte o [repositório oficial](https://github.com/modelcontextprotocol/servers). Há dezenas de servers. Use um antes de criar.
2. **Consigo resolver com `Bash` + tool nativa?** — Se o acesso ao sistema externo funciona via CLI, o agente já pode usar `Bash`. Um MCP server faz sentido quando o output via CLI é muito difícil de parsear ou quando a latência de parsear texto é problemática.
3. **O acesso vai se repetir?** — Se é uma operação pontual, `Bash` resolve. Se é algo que o agente vai precisar em toda sessão de desenvolvimento, um MCP server paga o custo de criação.

**Crie um server customizado quando:**
- Você tem uma API interna que nenhum server cobre
- O sistema externo requer autenticação ou lógica de negócio específica
- Você quer expor dados do projeto num formato útil para o agente (schema canônico, mapa de serviços)
- Ferramentas de build ou deploy internas que o agente deveria poder invocar com saídas estruturadas

> [!question] Teste mental
> "Se o agente tivesse acesso a essa tool, que tarefas ele conseguiria fazer melhor ou mais rápido?" Se a resposta não for concreta, o server provavelmente não vale o custo.

## Anatomia de um MCP server

Um MCP server é um processo que o Claude Code inicia como filho e com o qual se comunica via JSON-RPC sobre stdio. Você implementa dois handlers principais: `list_tools` (declara o que o server oferece) e `call_tool` (executa uma tool).

```mermaid
flowchart LR
    CC["Claude Code\n(MCP Client)"] -->|"list_tools request"| S["Seu MCP Server"]
    S -->|"tools[]"| CC
    CC -->|"call_tool(name, args)"| S
    S -->|"result"| CC
    S --> EXT["Sistema externo\n(API, DB, serviço)"]
```

O protocolo entre client e server é padronizado pelo MCP SDK. Você só implementa a lógica de negócio — o SDK cuida de deserialização, validação de schema, e transporte.

## Estrutura mínima em TypeScript

```bash
mkdir mcp-server && cd mcp-server
npm init -y
npm install @modelcontextprotocol/sdk
```

```typescript
// src/index.ts
import { Server } from "@modelcontextprotocol/sdk/server/index.js";
import { StdioServerTransport } from "@modelcontextprotocol/sdk/server/stdio.js";
import {
  CallToolRequestSchema,
  ListToolsRequestSchema,
} from "@modelcontextprotocol/sdk/types.js";

const server = new Server(
  { name: "meu-server", version: "1.0.0" },
  { capabilities: { tools: {} } }
);

// Declara as tools disponíveis
server.setRequestHandler(ListToolsRequestSchema, async () => ({
  tools: [
    {
      name: "buscar_servico",
      description: "Retorna configuração de um serviço interno pelo nome. Use quando o agente precisar saber a porta, URL base, ou dependências de um serviço.",
      inputSchema: {
        type: "object",
        properties: {
          nome: { type: "string", description: "Nome do serviço (ex: 'payments', 'orders')" },
        },
        required: ["nome"],
      },
    },
  ],
}));

// Implementa o handler de cada tool
server.setRequestHandler(CallToolRequestSchema, async (request) => {
  if (request.params.name === "buscar_servico") {
    const nome = request.params.arguments?.nome as string;
    const config = await buscarConfiguracaoServico(nome);
    return {
      content: [{ type: "text", text: JSON.stringify(config, null, 2) }],
    };
  }
  throw new Error(`Tool não encontrada: ${request.params.name}`);
});

async function main() {
  const transport = new StdioServerTransport();
  await server.connect(transport);
}

main().catch(console.error);
```

**O que cada parte faz:**

- `new Server(...)` — inicializa o server com nome e versão (usados pelo client para identificação)
- `capabilities: { tools: {} }` — declara que este server expõe tools (não resources, não prompts)
- `setRequestHandler(ListToolsRequestSchema, ...)` — responde "que tools você tem?" com a lista de tools e seus schemas de input
- `setRequestHandler(CallToolRequestSchema, ...)` — executa uma tool quando o agente a invoca
- `StdioServerTransport` — conecta via stdin/stdout ao Claude Code

## Server com estado (conexão de banco persistente)

Alguns servers precisam manter estado entre chamadas — uma conexão de banco, um cache de autenticação, um cliente HTTP com token renovável.

```typescript
import { Server } from "@modelcontextprotocol/sdk/server/index.js";
import { StdioServerTransport } from "@modelcontextprotocol/sdk/server/stdio.js";
import { CallToolRequestSchema, ListToolsRequestSchema } from "@modelcontextprotocol/sdk/types.js";
import { Pool } from "pg";

const pool = new Pool({ connectionString: process.env.DATABASE_URL });

const server = new Server(
  { name: "db-interno", version: "1.0.0" },
  { capabilities: { tools: {} } }
);

server.setRequestHandler(ListToolsRequestSchema, async () => ({
  tools: [
    {
      name: "query_pedidos",
      description: "Busca pedidos por status ou cliente. Retorna até 50 pedidos ordenados por data de criação decrescente.",
      inputSchema: {
        type: "object",
        properties: {
          status: {
            type: "string",
            enum: ["pendente", "aprovado", "enviado", "cancelado"],
            description: "Filtra por status do pedido"
          },
          cliente_id: { type: "number", description: "ID do cliente (opcional)" },
          limite: { type: "number", description: "Número máximo de resultados (padrão 20, máximo 50)" }
        },
      },
    },
  ],
}));

server.setRequestHandler(CallToolRequestSchema, async (request) => {
  if (request.params.name === "query_pedidos") {
    const { status, cliente_id, limite = 20 } = request.params.arguments as {
      status: string;
      cliente_id?: number;
      limite?: number;
    };

    const params: unknown[] = [status, Math.min(limite, 50)];
    let sql = "SELECT id, status, total, created_at FROM pedidos WHERE status = $1";

    if (cliente_id) {
      sql += " AND cliente_id = $3";
      params.push(cliente_id);
    }

    sql += " ORDER BY created_at DESC LIMIT $2";

    const { rows } = await pool.query(sql, params);
    return {
      content: [{ type: "text", text: JSON.stringify(rows, null, 2) }],
    };
  }
  throw new Error(`Tool não encontrada: ${request.params.name}`);
});

process.on("SIGTERM", async () => {
  await pool.end();
  process.exit(0);
});

async function main() {
  const transport = new StdioServerTransport();
  await server.connect(transport);
}

main().catch(console.error);
```

Note o `process.on("SIGTERM", ...)` — essencial para fechar conexões de banco corretamente quando o Claude Code encerra o server.

## Expondo resources (dados somente leitura)

Resources são dados que o agente pode consultar como referência — o schema do banco, o mapa de serviços, a documentação de um módulo. Não têm efeitos colaterais.

```typescript
import {
  ListResourcesRequestSchema,
  ReadResourceRequestSchema,
} from "@modelcontextprotocol/sdk/types.js";

const server = new Server(
  { name: "contexto-projeto", version: "1.0.0" },
  { capabilities: { tools: {}, resources: {} } }  // ← resources: {}
);

server.setRequestHandler(ListResourcesRequestSchema, async () => ({
  resources: [
    {
      uri: "projeto://servicos",
      name: "Mapa de serviços",
      description: "Lista todos os microsserviços com portas, URLs e responsabilidades",
      mimeType: "application/json",
    },
    {
      uri: "projeto://regras-negocio",
      name: "Regras de negócio críticas",
      description: "Invariantes do domínio que não podem ser violadas",
      mimeType: "text/markdown",
    },
  ],
}));

server.setRequestHandler(ReadResourceRequestSchema, async (request) => {
  switch (request.params.uri) {
    case "projeto://servicos":
      return {
        contents: [{
          uri: request.params.uri,
          mimeType: "application/json",
          text: JSON.stringify(await carregarMapaDeServicos(), null, 2),
        }],
      };
    case "projeto://regras-negocio":
      return {
        contents: [{
          uri: request.params.uri,
          mimeType: "text/markdown",
          text: await readFile("./docs/regras-negocio.md", "utf8"),
        }],
      };
    default:
      throw new Error(`Resource não encontrado: ${request.params.uri}`);
  }
});
```

O agente acessa `projeto://servicos` como referência enquanto trabalha — sem precisar invocar uma tool com efeito colateral.

## Configurar o server no settings.json

**Server compilado (produção):**

```json
{
  "mcpServers": {
    "contexto-projeto": {
      "command": "node",
      "args": ["./tools/mcp-server/dist/index.js"],
      "env": {
        "API_BASE_URL": "${API_BASE_URL}",
        "API_TOKEN": "${API_TOKEN}"
      }
    }
  }
}
```

**Server em desenvolvimento (sem build step):**

```json
{
  "mcpServers": {
    "contexto-projeto": {
      "command": "npx",
      "args": ["tsx", "./tools/mcp-server/src/index.ts"],
      "env": {
        "API_BASE_URL": "${API_BASE_URL}"
      }
    }
  }
}
```

`tsx` executa TypeScript diretamente sem compilar — conveniente durante o desenvolvimento do server.

## Onde versionar o server

```
meu-projeto/
  src/                      ← código da aplicação
  tools/
    mcp-server/
      src/
        index.ts
      package.json
      tsconfig.json
      README.md             ← como rodar e configurar
  .claude/
    settings.json           ← referencia o server em tools/
```

O server fica no repo do projeto, versionado junto. Todo dev que clona o projeto tem o server disponível — sem instalação extra além do `npm install`.

## Boas práticas de design de tools

**Nome descritivo com contexto**
`query_pedidos` é melhor que `query`. O agente escolhe a tool certa pelo nome + descrição. Em projetos com múltiplos servers, o contexto no nome evita ambiguidade.

**Descrição acionável**
Descreva o que a tool faz *e quando usá-la*. O agente usa a `description` para decidir se invoca.

```
❌ "Retorna dados de pedidos"
✅ "Busca pedidos por status ou cliente. Use quando precisar verificar o estado atual de pedidos antes de implementar lógica de processamento."
```

**Retorno estruturado**
JSON tipado em vez de texto livre. O agente raciocina sobre estrutura, não sobre texto.

```typescript
// ❌ Retorno difícil de processar
return { content: [{ type: "text", text: "Pedido 123: status pendente, total R$ 150,00" }] };

// ✅ Retorno estruturado
return { content: [{ type: "text", text: JSON.stringify({ id: 123, status: "pendente", total: 150.00 }) }] };
```

**Limite nos retornos**
Uma tool que retorna 10.000 rows vai consumir todo o contexto da sessão. Adicione paginação ou filtros obrigatórios. Documente o limite na description.

**Erros explícitos e acionáveis**
"Serviço não encontrado: payments-v3" é melhor que "404 Not Found". O agente pode agir com uma mensagem que explica o que falhou.

## Armadilhas

**Server que trava o Claude Code**
Se o processo do server travar ou não fechar stdin, o Claude Code pode ficar esperando indefinidamente. Sempre trate `SIGTERM` e feche conexões ao sair.

**Tool sem description suficiente**
O agente vai ignorar a tool se a description não deixar claro quando usá-la. Invista tempo escrevendo descriptions precisas — elas são a interface pública do seu server para o agente.

**Segredos nos args**
`"args": ["--token", "abc123"]` fica visível no processo e no `ps aux`. Sempre use env vars.

**Falta de validação de input**
O SDK valida o schema de input antes de chamar o handler, mas a validação de negócio é sua responsabilidade. Valide inputs antes de mandar para o sistema externo.

## Como explicar em inglês

**Custom MCP server** — a TypeScript (or any language) process that exposes tools, resources, and prompts for internal APIs or systems that no community server covers.

**When to create one:**
- Internal APIs that aren't public (company APIs, proprietary databases)
- Systems with custom authentication logic
- Exposing project-specific context (service map, business rules) as structured data

**The minimal pattern:**
1. `npm install @modelcontextprotocol/sdk`
2. Implement `ListToolsRequestSchema` handler — declare your tools with name, description, input schema
3. Implement `CallToolRequestSchema` handler — execute the tool and return JSON
4. Connect via `StdioServerTransport` and launch via `settings.json`

**Key phrase:** "The SDK handles the protocol. You write business logic — what the tool does and what it returns. It's about 100 lines for a simple server."

## Referências

- [MCP SDK — TypeScript](https://github.com/modelcontextprotocol/typescript-sdk) — SDK oficial com exemplos e documentação
- [MCP servers — repositório oficial](https://github.com/modelcontextprotocol/servers) — verifique se já existe um server antes de criar
- [[03-Dominios/Tecnologia/IA/Claude Code/Skills e MCP/04 - MCP overview|04 - MCP overview]] — arquitetura geral do protocolo MCP
- [[03-Dominios/Tecnologia/IA/Claude Code/Skills e MCP/05 - MCP servers essenciais|05 - MCP servers essenciais]] — servers prontos para usar antes de criar
- [[03-Dominios/Tecnologia/IA/Claude Code/Skills e MCP/07 - Compondo skills e MCP|07 - Compondo skills e MCP]] — usar o server criado em conjunto com skills
- [[03-Dominios/Tecnologia/IA/Claude Code/Skills e MCP/index|Skills e MCP]] — índice do galho
- [[03-Dominios/Tecnologia/IA/Claude Code/index|Claude Code]] — tronco da trilha
