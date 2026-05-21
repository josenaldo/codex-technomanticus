---
title: "Criar MCP server — quando e como"
type: concept
publish: true
created: 2026-05-13
updated: 2026-05-13
status: seedling
tags:
  - claude-code
  - mcp
  - desenvolvimento
  - customizacao
  - server
---

# Criar MCP server — quando e como

> [!abstract] TL;DR
> Crie um MCP server quando o projeto tem ferramentas internas, APIs privadas, ou dados estruturados que nenhum server existente acessa. O custo mínimo de criar um server é baixo: um arquivo TypeScript com 50-100 linhas que expõe uma ou duas tools. O SDK oficial do MCP cuida do protocolo; você cuida só da lógica de negócio.

## Quando criar vs reutilizar

**Reutilize um server existente quando**:
- O caso de uso é coberto pelo ecossistema (postgres, github, filesystem, browser)
- Você só precisa de acesso básico a um sistema padrão
- A configuração do server existente é suficiente

**Crie um server customizado quando**:
- Você tem uma API interna que nenhum server cobre
- O sistema externo requer autenticação ou lógica de negócio específica
- Você quer expor dados do projeto em um formato útil para o agente (schema canônico, mapa de serviços)
- Você tem ferramentas de build ou deploy internas que o agente deveria poder invocar

## Estrutura mínima de um MCP server em TypeScript

```bash
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
      description: "Retorna configuração de um serviço interno pelo nome",
      inputSchema: {
        type: "object",
        properties: {
          nome: { type: "string", description: "Nome do serviço" },
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
    // Lógica real aqui
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

main();
```

## Padrão de server com estado

Alguns servers precisam manter estado (conexão de banco, cache de autenticação):

```typescript
import { Server } from "@modelcontextprotocol/sdk/server/index.js";
import { StdioServerTransport } from "@modelcontextprotocol/sdk/server/stdio.js";
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
      description: "Busca pedidos por status ou cliente",
      inputSchema: {
        type: "object",
        properties: {
          status: { type: "string", enum: ["pendente", "aprovado", "enviado"] },
          cliente_id: { type: "number" },
        },
      },
    },
  ],
}));

server.setRequestHandler(CallToolRequestSchema, async (request) => {
  if (request.params.name === "query_pedidos") {
    const { status, cliente_id } = request.params.arguments as any;
    const { rows } = await pool.query(
      "SELECT * FROM pedidos WHERE status = $1 AND cliente_id = $2",
      [status, cliente_id]
    );
    return {
      content: [{ type: "text", text: JSON.stringify(rows, null, 2) }],
    };
  }
  throw new Error(`Tool não encontrada: ${request.params.name}`);
});
```

A conexão `pool` persiste enquanto o server está rodando — não reabre a cada chamada.

## Expondo resources

Resources são dados somente leitura que o agente pode consultar como referência:

```typescript
import {
  ListResourcesRequestSchema,
  ReadResourceRequestSchema,
} from "@modelcontextprotocol/sdk/types.js";

server = new Server(
  { name: "contexto-projeto", version: "1.0.0" },
  { capabilities: { tools: {}, resources: {} } }
);

server.setRequestHandler(ListResourcesRequestSchema, async () => ({
  resources: [
    {
      uri: "projeto://servicos",
      name: "Mapa de serviços",
      description: "Lista todos os microsserviços com suas portas e responsabilidades",
      mimeType: "application/json",
    },
  ],
}));

server.setRequestHandler(ReadResourceRequestSchema, async (request) => {
  if (request.params.uri === "projeto://servicos") {
    const servicos = await carregarMapaDeServicos();
    return {
      contents: [
        {
          uri: request.params.uri,
          mimeType: "application/json",
          text: JSON.stringify(servicos, null, 2),
        },
      ],
    };
  }
  throw new Error(`Resource não encontrado: ${request.params.uri}`);
});
```

O agente acessa `projeto://servicos` como referência enquanto trabalha — sem precisar invocar uma tool.

## Configurar no settings.json

Para um server local compilado:

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

Para um server em desenvolvimento (sem build):

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

## Onde versionar o server

Para um server específico do projeto:

```
meu-projeto/
  src/                 ← código da aplicação
  tools/
    mcp-server/
      src/
        index.ts
      package.json
      tsconfig.json
  .claude/
    settings.json      ← referencia o server em tools/
```

O server fica no repo do projeto, versionado junto. Todo dev que clona o projeto tem o server disponível.

## Boas práticas de design de tools

**Nome descritivo**: `query_pedidos` é melhor que `query` porque o agente precisa de contexto para escolher a tool certa.

**Descrição acionável**: descreva o que a tool faz e quando usá-la. O agente usa a `description` para decidir se invoca.

**Erros explícitos**: retorne mensagens de erro que o agente possa interpretar. "Serviço não encontrado: payments-v3" é melhor que "404".

**Retorno estruturado**: JSON em vez de texto livre. O agente consegue raciocinar sobre estrutura, não sobre texto.

**Escopo limitado**: uma tool que faz uma coisa é mais confiável do que uma tool genérica. Prefira `criar_pedido` e `atualizar_pedido` a `gerenciar_pedido(acao: string)`.

## Armadilhas

**Server que trava o Claude Code**: se o processo do server travar ou não fechar stdin, o Claude Code pode ficar esperando indefinidamente. Sempre trate sinais SIGTERM e feche conexões de banco ao sair.

**Tool sem descrição suficiente**: o agente vai chamar uma tool se a descrição é clara sobre quando usá-la. "Retorna dados" não instrui — "Retorna pedidos abertos de um cliente por ID, incluindo itens e total" instrui.

**Retorno muito grande**: uma tool que retorna 10.000 rows vai consumir todo o contexto da sessão. Adicione paginação ou filtros obrigatórios.

**Segredos no args do settings.json**: `"args": ["--token", "abc123"]` fica visível no processo. Use env vars.

## Veja também

- [[03-Dominios/IA/Claude Code/Skills e MCP/04 - MCP overview|04 - MCP overview]] — arquitetura geral do MCP
- [[03-Dominios/IA/Claude Code/Skills e MCP/05 - MCP servers essenciais|05 - MCP servers essenciais]] — servers prontos para usar antes de criar um
- [[03-Dominios/IA/Claude Code/Skills e MCP/07 - Compondo skills e MCP|07 - Compondo skills e MCP]] — usar o server que você criou em conjunto com skills
- [[03-Dominios/IA/Claude Code/Skills e MCP/index|Skills e MCP]] — índice do galho
