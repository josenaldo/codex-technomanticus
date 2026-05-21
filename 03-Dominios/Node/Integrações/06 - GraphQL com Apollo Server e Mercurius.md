---
title: "GraphQL com Apollo Server e Mercurius"
created: 2026-05-12
updated: 2026-05-12
type: concept
status: growing
publish: true
tags:
  - node
  - graphql
  - apollo
  - integrações
aliases:
  - Apollo Server
  - Mercurius GraphQL
  - GraphQL Node
---

# GraphQL com Apollo Server e Mercurius

> [!abstract] TL;DR
> **Apollo Server v4** é o servidor GraphQL mais popular do ecossistema Node.js: framework-agnostic por padrão (roda standalone via HTTP nativo) e integra com Express/Fastify/Koa via adaptadores (`expressMiddleware`, `startServerAndListen`). **Mercurius** é a alternativa Fastify-native que compila resolvers com JIT para throughput muito superior em workloads de alta concorrência — benchmarks apontam 2-3× mais req/s que Apollo em Fastify. **DataLoader** é o padrão canônico para resolver o problema N+1 em resolvers de campo: agrupa chamadas individuais em lotes por tick de event loop e deduplica chaves repetidas. **Subscriptions** são entregues via WebSockets: Apollo usa `graphql-ws` + `PubSub`; Mercurius tem `mercurius-subscriptions` com integração direta ao `fastify-websocket`. **Persisted queries** (APQ no Apollo, hashes SHA-256) eliminam o parse/validate overhead em produção e reduzem payload de rede enviando apenas o hash da query. Veja [[03-Dominios/Node/Integrações/index|Integrações]] para o contexto completo do galho.

## Como funciona

### Schema-first (SDL) vs code-first, resolvers e context

**Schema-first** define o schema usando SDL (Schema Definition Language) — strings em formato `type Query { ... }` — e depois associa resolvers ao mapa de campos. É a abordagem mais legível para equipes com designers de API e mantém o contrato explícito e versionável como artefato de texto.

**Code-first** (via bibliotecas como `TypeGraphQL` ou `Nexus`) gera o schema programaticamente a partir de decorators ou builders TypeScript. O benefício é type-safety completa sem duplicação: os tipos TypeScript e o schema GraphQL derivam da mesma fonte de verdade. A desvantagem é que o schema SDL resultante não é o ponto central de documentação — ele é gerado e não editado manualmente.

Os **resolvers** são funções que preenchem cada campo. A assinatura é `(parent, args, context, info)`:

| Parâmetro | Descrição |
|---|---|
| `parent` | Valor resolvido do tipo pai (campo raiz = `undefined`) |
| `args` | Argumentos declarados no campo SDL (`id: ID!`) |
| `context` | Objeto compartilhado por todos os resolvers na requisição (user auth, DataLoaders, DB clients) |
| `info` | Metadados do campo: `fieldName`, `returnType`, `path`, `schema` |

O **context** é construído uma vez por request. Em Apollo v4 com Express, é o segundo argumento de `expressMiddleware`. Em Mercurius, é a função `context` no objeto de opções do plugin. Colocar os DataLoaders no context garante que o escopo de batching seja por request e não global (o que causaria cache "stale" entre requests).

### Plugins (Apollo) e hooks (Mercurius)

**Apollo plugins** seguem a interface `ApolloServerPlugin` e expõem lifecycle hooks assíncronos:

- `requestDidStart` → chamado no início de cada operação
- `parsingDidStart` / `validationDidStart` → parse e validação do documento
- `executionDidStart` → início da execução (aqui se instrumenta tracing por resolver)
- `willSendResponse` → permite modificar a resposta antes de enviar

**Mercurius hooks** são registrados via `fastify.graphql.addHook(name, handler)`. Os hooks principais são `preExecution` (modifica query/variables antes de executar), `onResolution` (acessa resultado) e `preSubscriptionExecution`. Por rodar sobre Fastify, o Mercurius também herda todos os hooks HTTP do framework (onRequest, onSend, etc.), o que facilita integrar auth e rate-limiting sem código extra.

Em ambos os casos, plugins/hooks são o lugar correto para: logging de operações lentas, APM (DataDog, NewRelic, OpenTelemetry), rate limiting por operação e blocking de operações non-persisted em produção.

### DataLoader pattern para evitar N+1 em resolvers

O problema N+1 ocorre quando um resolver de campo dispara 1 query para cada item de uma lista. Para uma lista de 100 posts, o resolver `post.author` faria 100 queries individuais para buscar o autor de cada post.

**DataLoader** resolve isso em duas etapas:

1. **Batching**: acumula todas as chaves solicitadas durante o tick atual do event loop e chama a `batchFn` uma única vez com o array de chaves.
2. **Deduplication**: se a mesma chave aparecer múltiplas vezes no batch, a `batchFn` recebe cada chave apenas uma vez e o resultado é reutilizado para todos os callers.

O escopo do DataLoader deve ser **por request** (instanciado no context). Um DataLoader global acumularia cache entre requests de usuários distintos, causando vazamento de dados. A `batchFn` deve retornar um array de resultados na **mesma ordem e tamanho** do array de chaves recebido — o DataLoader faz o mapeamento posicional, então `keys[0]` → `results[0]`.

## Snippets de código

### 1. Apollo Server v4 com Express middleware

```typescript
import express from "express";
import http from "http";
import { ApolloServer } from "@apollo/server";
import { expressMiddleware } from "@apollo/server/express4";
import { ApolloServerPluginDrainHttpServer } from "@apollo/server/plugin/drainHttpServer";
import cors from "cors";
import bodyParser from "body-parser";

const typeDefs = `#graphql
  type Book {
    id: ID!
    title: String!
    author: Author!
    publishedYear: Int
  }

  type Author {
    id: ID!
    name: String!
    books: [Book!]!
  }

  type Query {
    books: [Book!]!
    book(id: ID!): Book
    authors: [Author!]!
  }

  type Mutation {
    addBook(title: String!, authorId: ID!, publishedYear: Int): Book!
  }
`;

interface Context {
  userId?: string;
  token?: string;
}

const resolvers = {
  Query: {
    books: async (_: unknown, __: unknown, ctx: Context) => {
      // access ctx.userId for authorization checks
      return db.findAllBooks();
    },
    book: async (_: unknown, args: { id: string }) => db.findBookById(args.id),
    authors: () => db.findAllAuthors(),
  },
  Mutation: {
    addBook: async (
      _: unknown,
      args: { title: string; authorId: string; publishedYear?: number }
    ) => db.createBook(args),
  },
  Book: {
    author: (parent: { authorId: string }) => db.findAuthorById(parent.authorId),
  },
};

async function startServer() {
  const app = express();
  const httpServer = http.createServer(app);

  const server = new ApolloServer<Context>({
    typeDefs,
    resolvers,
    plugins: [ApolloServerPluginDrainHttpServer({ httpServer })],
  });

  await server.start();

  app.use(
    "/graphql",
    cors<cors.CorsRequest>(),
    bodyParser.json(),
    expressMiddleware(server, {
      context: async ({ req }) => ({
        userId: req.headers["x-user-id"] as string,
        token: req.headers.authorization,
      }),
    })
  );

  await new Promise<void>((resolve) =>
    httpServer.listen({ port: 4000 }, resolve)
  );
  console.log("Apollo Server ready at http://localhost:4000/graphql");
}

startServer();
```

### 2. Mercurius com Fastify

```typescript
import Fastify from "fastify";
import mercurius from "mercurius";

const app = Fastify({ logger: true });

const schema = `
  type Product {
    id: ID!
    name: String!
    price: Float!
    category: Category!
  }

  type Category {
    id: ID!
    label: String!
  }

  type Query {
    products: [Product!]!
    product(id: ID!): Product
  }

  type Mutation {
    createProduct(name: String!, price: Float!, categoryId: ID!): Product!
  }
`;

const resolvers = {
  Query: {
    products: async (_: unknown, __: unknown, ctx: { userId: string }) => {
      return productRepository.findAll();
    },
    product: async (_: unknown, { id }: { id: string }) =>
      productRepository.findById(id),
  },
  Mutation: {
    createProduct: async (
      _: unknown,
      args: { name: string; price: number; categoryId: string }
    ) => productRepository.create(args),
  },
  Product: {
    category: (parent: { categoryId: string }, _: unknown, ctx: { categoryLoader: any }) =>
      ctx.categoryLoader.load(parent.categoryId),
  },
};

app.register(mercurius, {
  schema,
  resolvers,
  graphiql: process.env.NODE_ENV !== "production",
  context: (req) => ({
    userId: req.headers["x-user-id"] as string,
    categoryLoader: createCategoryLoader(), // DataLoader per-request
  }),
});

app.listen({ port: 4000 }, () => {
  console.log("Mercurius ready at http://localhost:4000/graphql");
});
```

### 3. DataLoader para batching de queries em resolvers de campo

```typescript
import DataLoader from "dataloader";
import { Pool } from "pg";

const pool = new Pool({ connectionString: process.env.DATABASE_URL });

// batchFn recebe array de chaves e deve retornar array de resultados
// na MESMA ORDEM e MESMO TAMANHO — regra fundamental do DataLoader
async function batchUsersByIds(ids: readonly string[]) {
  const { rows } = await pool.query<{ id: string; name: string; email: string }>(
    `SELECT id, name, email FROM users WHERE id = ANY($1::uuid[])`,
    [ids]
  );

  // Montar mapa id → row para preservar a ordem de ids
  const userMap = new Map(rows.map((u) => [u.id, u]));

  // Retornar na mesma ordem dos ids recebidos (null se não encontrar)
  return ids.map((id) => userMap.get(id) ?? null);
}

// Factory: instanciar por request para evitar cache cross-request
export function createUserLoader() {
  return new DataLoader(batchUsersByIds, {
    maxBatchSize: 100, // limite de segurança por batch
    cacheKeyFn: (key) => key, // default, mas explícito para clareza
  });
}

// Context type com loaders
interface RequestContext {
  userId: string;
  userLoader: DataLoader<string, { id: string; name: string; email: string } | null>;
}

// Resolver que usa o loader — dispara 1 query para N posts
const resolvers = {
  Post: {
    author: (parent: { authorId: string }, _: unknown, ctx: RequestContext) =>
      ctx.userLoader.load(parent.authorId),
  },
  Comment: {
    user: (parent: { userId: string }, _: unknown, ctx: RequestContext) =>
      ctx.userLoader.load(parent.userId),
  },
};

// Apollo context factory — instancia loader por request
const contextFn = async ({ req }: { req: Express.Request }): Promise<RequestContext> => ({
  userId: req.headers["x-user-id"] as string,
  userLoader: createUserLoader(), // novo loader a cada request
});
```

### 4. Subscriptions com PubSub (Apollo) e mercurius-subscriptions

```typescript
// ── Apollo Server + graphql-ws ──────────────────────────────────────────────
import express from 'express';
import { ApolloServer } from "@apollo/server";
import { ApolloServerPluginDrainHttpServer } from '@apollo/server/plugin/drainHttpServer';
import { makeExecutableSchema } from "@graphql-tools/schema";
import { PubSub } from "graphql-subscriptions";
import { useServer } from "graphql-ws/lib/use/ws";
import { WebSocketServer } from "ws";
import http from "http";

const pubsub = new PubSub();

const typeDefs = `#graphql
  type Message {
    id: ID!
    content: String!
    from: String!
    channel: String!
  }

  type Query {
    _empty: String
  }

  type Mutation {
    sendMessage(channel: String!, content: String!, from: String!): Message!
  }

  type Subscription {
    messageSent(channel: String!): Message!
  }
`;

const MESSAGE_SENT = "MESSAGE_SENT";

const resolvers = {
  Mutation: {
    sendMessage: async (
      _: unknown,
      args: { channel: string; content: string; from: string }
    ) => {
      const message = { id: crypto.randomUUID(), ...args };
      await pubsub.publish(`${MESSAGE_SENT}_${args.channel}`, { messageSent: message });
      return message;
    },
  },
  Subscription: {
    messageSent: {
      subscribe: (_: unknown, { channel }: { channel: string }) =>
        // graphql-subscriptions v1.x — use asyncIterableIterator() in v2+
        pubsub.asyncIterator([`${MESSAGE_SENT}_${channel}`]),
    },
  },
};

const schema = makeExecutableSchema({ typeDefs, resolvers });

const app = express();
const httpServer = http.createServer(app);
const wsServer = new WebSocketServer({ server: httpServer, path: "/graphql" });
const serverCleanup = useServer({ schema }, wsServer);

const server = new ApolloServer({
  schema,
  plugins: [
    ApolloServerPluginDrainHttpServer({ httpServer }),
    {
      async serverWillStart() {
        return {
          async drainServer() {
            await serverCleanup.dispose();
          },
        };
      },
    },
  ],
});

// ── Mercurius subscriptions ─────────────────────────────────────────────────
// Em um projeto Fastify separado:
/*
import Fastify from 'fastify'
import mercurius from 'mercurius'
import { createMercuriusTestClient } from 'mercurius-integration-testing'

const app = Fastify()

app.register(mercurius, {
  schema,
  resolvers,
  subscription: true, // habilita WebSocket automático via fastify-websocket
})
*/
```

### 5. Plugin Apollo para logging de operações e métricas de resolver

```typescript
import { ApolloServerPlugin, GraphQLRequestContext } from "@apollo/server";

interface OperationMetrics {
  operationName: string | null;
  startTime: number;
  resolverTimings: Array<{ path: string; duration: number }>;
}

export function createLoggingPlugin(): ApolloServerPlugin {
  return {
    async requestDidStart(requestContext: GraphQLRequestContext<Record<string, unknown>>) {
      const metrics: OperationMetrics = {
        operationName: requestContext.request.operationName ?? null,
        startTime: Date.now(),
        resolverTimings: [],
      };

      return {
        async parsingDidStart() {
          return async (err?: Error) => {
            if (err) console.error("[GraphQL] Parse error", err);
          };
        },

        async validationDidStart() {
          return async (errors?: readonly Error[]) => {
            if (errors?.length) console.error("[GraphQL] Validation errors", errors);
          };
        },

        async executionDidStart() {
          return {
            willResolveField({ info }) {
              const start = Date.now();
              return (error, result) => {
                const duration = Date.now() - start;
                const path = info.path.key.toString();
                metrics.resolverTimings.push({ path, duration });

                if (duration > 100) {
                  console.warn(`[GraphQL] Slow resolver: ${path} took ${duration}ms`);
                }
              };
            },
          };
        },

        async willSendResponse() {
          const totalDuration = Date.now() - metrics.startTime;
          console.info({
            message: "[GraphQL] Operation completed",
            operation: metrics.operationName,
            totalDuration,
            slowResolvers: metrics.resolverTimings.filter((r) => r.duration > 50),
          });
        },

        async didEncounterErrors({ errors }) {
          console.error("[GraphQL] Errors encountered", errors);
        },
      };
    },
  };
}

// Registrar no Apollo Server:
// const server = new ApolloServer({ typeDefs, resolvers, plugins: [createLoggingPlugin()] })
```

### 6. Query depth limiting e complexity limiting

```typescript
import depthLimit from "graphql-depth-limit";
import { createComplexityLimitRule } from "graphql-validation-complexity";
import { ApolloServer } from "@apollo/server";
import { GraphQLError } from "graphql";

// ── Depth limiting ──────────────────────────────────────────────────────────
// Bloqueia queries recursivas/profundas demais (DoS via schema deeply nested)
// Instala: npm install graphql-depth-limit
const depthLimitRule = depthLimit(
  7, // profundidade máxima permitida
  { ignore: ["__schema", "__type"] }, // ignorar introspection
  (depths) => {
    console.info("[GraphQL] Query depths:", depths);
  }
);

// ── Complexity limiting ─────────────────────────────────────────────────────
// Atribui "custo" a cada campo e bloqueia queries acima de um threshold
// Instala: npm install graphql-validation-complexity
const complexityLimitRule = createComplexityLimitRule(
  1000, // custo máximo permitido por query
  {
    scalarCost: 1,
    objectCost: 2,
    listFactor: 10, // campos de lista multiplicam o custo
    onCost: (cost) => console.info("[GraphQL] Query cost:", cost),
    formatErrorMessage: (cost) =>
      `Query exceeds complexity limit of 1000 (cost: ${cost})`,
  }
);

// ── Apollo Server com ambas as regras ───────────────────────────────────────
const server = new ApolloServer({
  typeDefs,
  resolvers,
  validationRules: [depthLimitRule, complexityLimitRule],
});

// ── Bloquear introspection em produção ─────────────────────────────────────
// Apollo Server v4 desabilita introspection via plugin ou opção nativa
import { ApolloServerPluginInlineTrace } from "@apollo/server/plugin/inlineTrace";
import { ApolloServerPluginLandingPageDisabled } from "@apollo/server/plugin/disabled";

const productionServer = new ApolloServer({
  typeDefs,
  resolvers,
  introspection: process.env.NODE_ENV !== "production", // false em prod
  plugins: [
    ApolloServerPluginLandingPageDisabled(), // desabilita Apollo Sandbox em prod
    ApolloServerPluginInlineTrace(), // opcional: habilita tracing inline para Apollo Studio / APM
  ],
});
```

## Armadilhas

> [!danger] N+1 em resolvers de campo sem DataLoader
> O problema N+1 é a causa mais frequente de degradação de performance em APIs GraphQL. Cada resolver de campo opera de forma independente: quando uma lista de 100 posts é resolvida e cada `Post.author` dispara uma query individual, o banco recebe 101 queries (1 para a lista + 100 para os autores). Sem DataLoader no context, isso passa silenciosamente em desenvolvimento (datasets pequenos) e explode em produção. A regra prática é: **qualquer resolver de campo que acessa o banco deve usar um DataLoader**. Monitore via APM (DataDog, NewRelic) o número de queries por operação GraphQL.

> [!danger] Introspection habilitada em produção
> Introspection expõe o schema inteiro da sua API: todos os tipos, campos, argumentos e directives. Um attacker pode usar essa informação para mapear a superfície de ataque, identificar campos com dados sensíveis e construir queries otimizadas para exploração. Apollo Server v4 desabilita introspection via `introspection: false` ou automaticamente quando `NODE_ENV=production`. Mas desabilitar introspection **não é suficiente por si só** — combine com autenticação no endpoint, persisted queries e rate limiting por operação.

> [!warning] Profundidade de query sem limite (DoS via queries profundas)
> GraphQL permite queries recursivas: se seu schema tem `User { friends { friends { friends { ... } } } }`, um cliente pode enviar uma query com 50 níveis de profundidade, forçando o servidor a resolver exponencialmente mais dados do que o esperado. Sem depth limiting, isso é um vetor de DoS fácil de explorar sem autenticação. Use `graphql-depth-limit` com máximo de 5-10 níveis dependendo do schema. Combine com complexity limiting (`graphql-validation-complexity`) para bloquear queries que explorem campos de lista em múltiplos níveis.

> [!warning] Não usar persisted queries em produção (parse/validate overhead)
> Cada request GraphQL com query completa exige parse (texto → AST) e validation (AST contra schema) antes da execução. Em endpoints de alta frequência, esse overhead acumula: queries complexas podem levar 5-20ms só para parse/validate. **Persisted queries** enviam apenas o hash SHA-256 da query; o servidor busca a query associada em cache (em memória ou Redis). Apollo oferece **Automatic Persisted Queries (APQ)** que negocia o hash automaticamente no primeiro request. Mercurius tem suporte nativo via `persistedQueries` option. Em produção, bloqueie queries não-persistidas com uma allowlist para zero overhead de parse em operações desconhecidas.

## Comparativo: Apollo Server v4 vs Mercurius vs Yoga v3

| Critério | Apollo Server v4 | Mercurius (Fastify) | GraphQL Yoga v3 |
|---|---|---|---|
| **Performance** | Moderada (overhead de plugin pipeline) | Alta (JIT compilation, Fastify perf) | Boa (baseado em `graphql-js` puro) |
| **Ecossistema** | Maior: Apollo Federation, Studio, APQ nativo | Médio: plugins Fastify, federation via plugin | Médio: Envelop plugins, Yoga-specific |
| **DX** | Excelente: Apollo Sandbox, Studio, APQ automático | Boa: GraphiQL, docs claras | Excelente: built-in IDE, server-sent events |
| **Framework binding** | Agnostic (Express, Fastify, Koa, standalone) | Fastify-only (plugin nativo) | Agnostic (Express, Fastify, Koa, Edge) |
| **Subscriptions** | `graphql-ws` + manual setup | Built-in via `fastify-websocket` | SSE nativo + WebSocket via plugin |
| **Federation** | Apollo Federation v2 nativo | `@mercuriusjs/federation` plugin | Yoga Stitching + Federation via plugin |
| **Melhor para** | Times grandes, Apollo Studio, microservices federation | APIs Fastify de alta performance, low-latency | APIs Edge/serverless, simplicidade, flexibilidade |

## Em entrevista

**Q: How does DataLoader solve the N+1 problem in GraphQL resolvers?**

DataLoader addresses N+1 by batching all individual `load(key)` calls that occur within the same event loop tick into a single batch function call. Instead of each resolver firing its own database query immediately, DataLoader accumulates all the keys requested during the current tick and then calls the `batchFn` once with the complete array of keys. The `batchFn` can then execute a single `WHERE id = ANY(...)` query (or equivalent) to fetch all required records at once, reducing N+1 queries down to a single round trip. Additionally, DataLoader deduplicates keys within a batch, so if multiple resolvers request the same entity, the `batchFn` receives each key only once and the result is shared across all callers. The critical implementation detail is that each DataLoader instance must be scoped to a single request via the GraphQL context — a shared global DataLoader would cache results across requests from different users, creating a security data-leak vulnerability.

**Q: What are the main differences between Apollo Server and Mercurius?**

Apollo Server v4 is framework-agnostic: it runs standalone via Node's native HTTP or integrates with Express, Fastify, Koa, and serverless via adapters, making it the default choice for teams without a strong framework preference. Mercurius is a Fastify plugin that compiles GraphQL resolvers using JIT (just-in-time) compilation and benefits directly from Fastify's low-overhead request/response lifecycle, delivering significantly higher throughput in benchmark scenarios (often 2-3× more requests/second than Apollo on the same hardware). From a developer experience perspective, Apollo has a richer ecosystem: Apollo Federation v2 for microservices, Apollo Studio for schema registry and metrics, and APQ (Automatic Persisted Queries) out of the box. Mercurius integrates naturally with the Fastify plugin ecosystem — authentication hooks, rate limiting, and logging all reuse existing `fastify-*` plugins without additional adapter code. The practical choice is: use Mercurius when you are already on Fastify and need maximum performance; use Apollo Server when you need Federation, Studio integration, or team familiarity.

**Q: How would you protect a GraphQL endpoint in production?**

The first layer of protection is disabling introspection (`introspection: false` in Apollo, `graphiql: false` in Mercurius), so attackers cannot enumerate the schema to plan targeted queries. Depth limiting (via `graphql-depth-limit`) prevents DoS attacks through deeply-nested recursive queries by rejecting any query that exceeds a configured maximum depth (typically 5-10 levels depending on schema complexity). Complexity limiting (`graphql-validation-complexity`) assigns a cost to each field and list multiplier and rejects queries that exceed a threshold, preventing attackers from crafting queries that are syntactically valid but computationally expensive. Persisted queries (APQ in Apollo, or a server-side allowlist) restrict execution to a pre-approved set of known operations, eliminating arbitrary query injection and removing parse/validate overhead for legitimate clients. Additionally, rate limiting should be applied at the operation level (not just HTTP), and authentication/authorization should be enforced in resolvers or via middleware before execution reaches the data layer.

**Q: What are the trade-offs between GraphQL and REST when designing APIs?**

GraphQL's main advantage is its declarative data fetching model: clients specify exactly the fields they need, eliminating over-fetching (REST returns fixed response shapes) and under-fetching (REST may require multiple round trips for related resources). This is particularly valuable for mobile clients on constrained networks and for frontend teams that iterate on UI without requiring API changes. However, GraphQL introduces complexity on the server side: caching is harder because queries are dynamic (HTTP caching based on URL doesn't apply cleanly), N+1 problems require DataLoader instrumentation, and authorization logic must be applied at the field level rather than at the endpoint level. REST APIs are simpler to cache (CDN-friendly, ETag/Last-Modified headers work naturally), have a larger tooling ecosystem for API gateways and monitoring, and are more familiar to developers outside the JavaScript/GraphQL community. The practical decision often comes down to client diversity and team expertise: GraphQL shines in BFF (Backend For Frontend) layers where a single API serves multiple client types (mobile, web, desktop) with different data needs; REST is preferable for public APIs with third-party consumers, microservice-to-microservice communication, and teams without GraphQL operational experience.

## Vocabulário

| Termo | Definição |
|---|---|
| **resolver** | Função que resolve o valor de um campo GraphQL; assinatura `(parent, args, context, info)` |
| **schema** | Contrato tipado da API GraphQL definindo tipos, queries, mutations e subscriptions |
| **SDL** | Schema Definition Language — sintaxe textual para declarar schemas GraphQL (`type Query { ... }`) |
| **code-first** | Abordagem onde o schema é gerado programaticamente a partir de código (TypeGraphQL, Nexus) |
| **schema-first** | Abordagem onde o schema SDL é escrito manualmente e os resolvers são associados depois |
| **DataLoader** | Biblioteca que resolve N+1 agrupando chamadas individuais em batches por tick do event loop |
| **batching** | Agrupamento de múltiplas operações individuais em uma única operação executada de uma vez |
| **deduplication** | Remoção de chaves duplicadas num batch; o DataLoader responde o mesmo resultado para múltiplos callers |
| **subscription** | Operação GraphQL de longa duração que emite dados via WebSocket ou SSE quando eventos ocorrem |
| **PubSub** | Padrão publish/subscribe usado para distribuir eventos de mutations para subscribers ativos |
| **persisted query** | Query pré-registrada no servidor identificada por hash SHA-256; elimina parse/validate por request |
| **introspection** | Capacidade de consultar o schema completo via `__schema` e `__type`; deve ser desabilitada em produção |
| **query depth** | Nível de aninhamento de campos numa query; limitar previne DoS via queries recursivas profundas |
| **complexity limit** | Custo calculado por query baseado em número de campos e fatores de lista; bloqueia queries excessivamente custosas |
| **APQ** | Automatic Persisted Queries — protocolo Apollo que negocia hash da query automaticamente no primeiro request |
| **JIT compilation** | Técnica do Mercurius que compila resolvers para código otimizado em runtime para maior throughput |

## Veja também

- [[03-Dominios/Node/Integrações/index|Integrações]]
- [[Node.js]]
- [Apollo Server v4 — documentação oficial](https://www.apollographql.com/docs/apollo-server/)
- [Mercurius — documentação oficial](https://mercurius.dev/)
- [DataLoader — repositório e docs](https://github.com/graphql/dataloader)
- [graphql-depth-limit](https://github.com/stems/graphql-depth-limit)
- [graphql-validation-complexity](https://github.com/4Catalyzer/graphql-validation-complexity)
