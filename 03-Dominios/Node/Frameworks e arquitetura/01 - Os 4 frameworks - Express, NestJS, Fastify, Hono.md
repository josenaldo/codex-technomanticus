---
title: "Os 4 frameworks: Express, NestJS, Fastify, Hono"
created: 2026-05-08
updated: 2026-05-08
type: concept
status: seedling
publish: true
tags:
  - node
  - frameworks
  - mental-model
  - express
  - nestjs
  - fastify
  - hono
aliases:
  - Visão geral frameworks Node
  - 4 frameworks Node
---

# Os 4 frameworks: Express, NestJS, Fastify, Hono

> [!abstract] TL;DR
> Em 2026, a decisão pragmática em Node passa por quatro modelos: Express (middleware-based e ubíquo), NestJS (opinativo, DI e decorators), Fastify (schema-first e performance), Hono (edge-first e Fetch API). Não existe campeão universal. Existe matching problema -> ferramenta.

## O que é

**Express** é o framework minimalista e "unopinionated" do ecossistema Node. A documentação oficial o descreve como uma camada fina de features web com uso forte de middleware; em 2026, Express 5.x é a linha corrente.

**NestJS** é um framework TypeScript opinativo para server-side apps escaláveis. O modelo central combina módulos, controllers, providers, decorators e um container de dependency injection.

**Fastify** é um framework HTTP focado em baixo overhead, plugin architecture e schemas. A própria documentação recomenda JSON Schema para validar rotas e serializar respostas.

**Hono** é um framework pequeno e multi-runtime baseado em Web Standards. Roda em Cloudflare Workers, Deno, Bun, AWS Lambda e Node, com API baseada em `Request`/`Response`.

## Por que importa

Confundir os modelos leva a escolhas caras. Usar NestJS em um microserviço simples pode introduzir DI e decorators sem retorno. Usar Express por hábito em um domínio enterprise grande pode deixar estrutura demais na disciplina individual de cada dev. Usar Fastify sem schema desperdiça o diferencial do framework. Usar Hono em app que depende profundamente de `fs`, `net` ou bibliotecas Node-only pode bater em constraints de edge.

## Como funciona

| Framework | Modelo | Use case típico | Maturidade | Trade-offs |
| --- | --- | --- | --- | --- |
| Express | Middleware-based, minimalista | Microsserviços simples, prototipagem, glue code | Maduro, v5.x | Pouca estrutura; precisa montar validation, DI e contracts manualmente |
| NestJS | Opinativo, DI, decorators | Apps enterprise, time grande, domínio complexo | Maduro, v10+ | Curva de aprendizado; overhead em apps simples |
| Fastify | Schema-first, performance-focused | APIs com contrato claro e throughput alto | Maduro, v5.x | Plugin encapsulation exige mental model; ecossistema menor que Express |
| Hono | Ultralight, edge-first, Fetch API | Edge workers, serverless, multi-runtime | Mais recente, v4+ | Ecossistema menor; edge limita APIs Node-specific |

```typescript
// Express 5
import express from "express";

const app = express();
app.get("/hello", (_req, res) => res.json({ greeting: "hello" }));
app.listen(3000);
```

```typescript
// NestJS
@Controller()
export class AppController {
  @Get("/hello")
  hello() {
    return { greeting: "hello" };
  }
}
```

```typescript
// Fastify
import Fastify from "fastify";

const app = Fastify();
app.get("/hello", async () => ({ greeting: "hello" }));
await app.listen({ port: 3000 });
```

```typescript
// Hono
import { Hono } from "hono";

const app = new Hono();
app.get("/hello", (c) => c.json({ greeting: "hello" }));
export default app;
```

## Na prática

- Microsserviço I/O-bound simples, time pequeno: Express ou Fastify.
- App enterprise, time grande, DI complexa: NestJS.
- API com schema bem definido e throughput alto: Fastify.
- Edge worker, serverless ou multi-runtime: Hono.
- Comparação detalhada: [[12 - Decision tree + cheatsheet]].

### Cenário 1: webhook receiver

Imagine uma API que recebe webhooks de Stripe/GitHub, valida assinatura, grava evento bruto e responde rápido. O domínio é pequeno, o throughput é moderado e o risco principal é latência/timeout do provedor. Express resolve bem se o time já conhece o ecossistema; Fastify ganha se schema e serialização forem parte central do contrato.

```typescript
// Express: simples, explícito, bom para glue code.
app.post("/webhooks/github", verifyGithubSignature, async (req, res) => {
  await inbox.save({ source: "github", payload: req.body });
  res.status(202).json({ accepted: true });
});
```

```typescript
// Fastify: contrato explícito na rota.
app.post("/webhooks/github", {
  schema: {
    body: GithubWebhookSchema,
    response: { 202: AcceptedSchema },
  },
}, async (req, reply) => {
  await inbox.save({ source: "github", payload: req.body });
  return reply.code(202).send({ accepted: true });
});
```

### Cenário 2: produto enterprise com módulos

Imagine um backend com billing, usuários, permissões, auditoria, integrações e jobs internos. O problema já não é só "servir HTTP"; é manter boundaries por feature, lifecycle, DI, testes e composição de concerns. NestJS fica mais atraente porque força uma gramática comum.

```typescript
@Module({
  imports: [BillingModule, IdentityModule, AuditModule],
  controllers: [InvoicesController],
  providers: [CreateInvoiceUseCase, InvoicePolicy],
})
export class InvoicesModule {}
```

O custo é real: decorators, módulos, providers e scopes precisam ser aprendidos. Mas, em time maior, convenção compartilhada frequentemente vale mais do que liberdade local.

### Cenário 3: edge API

Se o requisito é responder perto do usuário em Cloudflare Workers, Deno Deploy ou runtime similar, a pergunta muda. Express e NestJS assumem Node HTTP; Hono assume Web Standards.

```typescript
const app = new Hono();

app.get("/flags/:userId", async (c) => {
  const flags = await c.env.KV.get(`flags:${c.req.param("userId")}`, "json");
  return c.json(flags ?? {});
});
```

Essa decisão é menos sobre sintaxe e mais sobre deploy target. Edge runtime costuma limitar filesystem, sockets e tempo de CPU; escolher Hono evita carregar abstrações que não foram desenhadas para esse ambiente.

### Heurística de decisão rápida

Faça quatro perguntas antes de escolher:

1. **Qual é o deploy target?** Node tradicional, container, serverless, edge?
2. **O contrato HTTP é central?** Se sim, schema-first pesa a favor de Fastify.
3. **O domínio é grande?** Se sim, DI e módulos pesam a favor de NestJS ou Clean Architecture manual.
4. **O time já domina qual modelo?** Familiaridade não decide sozinha, mas reduz risco.

### Como revisar essa escolha em arquitetura

Procure sinais concretos, não preferências:

- Se o projeto é Express e já tem 40 services com wiring espalhado, pergunte por composition root ou container.
- Se o projeto é NestJS e só tem 4 endpoints CRUD, questione o overhead.
- Se o projeto é Fastify sem schemas, o principal diferencial está subutilizado.
- Se o projeto é Hono mas depende de libs Node-only, a portabilidade é ilusória.
- Se a justificativa é "performance", peça benchmark do caso real: payload, DB, rede, CPU, warm/cold start.

> [!warning] Benchmark não é arquitetura
> Framework overhead raramente é o gargalo principal de um backend com banco, fila, rede externa e autenticação. Use benchmark para eliminar opções inviáveis, não para transformar escolha de framework em ranking universal.

### Anti-decision tree

Alguns sinais indicam que a decisão está sendo tomada pelo critério errado:

```text
"Vamos de NestJS porque é enterprise"
  -> Qual complexidade enterprise existe agora?

"Vamos de Fastify porque é mais rápido"
  -> O gargalo medido é framework overhead?

"Vamos de Express porque todo mundo conhece"
  -> Quem vai impor estrutura, validation e error handling?

"Vamos de Hono porque é moderno"
  -> O deploy target é edge ou multi-runtime de verdade?
```

O papel de senior é transformar preferência em hipótese verificável. Se a hipótese não menciona deploy, contrato, domínio, time e operação, ela ainda está incompleta.

### Compatibilidade com os galhos anteriores

Framework não substitui fundamentos:

- [[03-Dominios/Node/Runtime e Event Loop/index]] continua decidindo impacto de CPU-heavy work, timers, microtasks e bloqueio.
- [[03-Dominios/Node/Paralelismo/index]] continua necessário quando o problema é CPU-bound ou isolamento de processo.
- [[03-Dominios/Node/Streams/index]] continua aparecendo em upload, download, proxy, CSV, multipart e respostas longas.

```typescript
// Framework nenhum torna isso barato:
app.get("/report", (_req, res) => {
  const result = generateHugeCpuBoundReport(); // bloqueia event loop
  res.json(result);
});
```

Se a API sofre por CPU, escolher Fastify não resolve. Se sofre por upload gigante sem backpressure, escolher NestJS não resolve. Framework é camada HTTP; fundamentos ainda mandam.

### Critérios de maturidade de uma escolha

Uma escolha de framework está madura quando o time consegue responder:

1. Como validamos input?
2. Como formatamos erro?
3. Como observamos latência e falhas?
4. Como desligamos o app com graceful shutdown?
5. Como testamos handlers sem subir infraestrutura real?
6. Como isolamos regra de negócio da camada HTTP?
7. Como versionamos contrato?
8. Como lidamos com deploy target e limites operacionais?

Sem essas respostas, a escolha ainda é só scaffold.

### Regra prática final

Se duas opções parecem equivalentes, escolha a que reduz o risco dominante:

- risco de **desorganização** -> NestJS ou Clean Architecture explícita;
- risco de **contrato fraco** -> Fastify ou schema-first disciplinado;
- risco de **runtime incompatível** -> Hono/Web Standards;
- risco de **complexidade acidental** -> Express com poucas abstrações;
- risco de **time travar na curva de aprendizado** -> ferramenta que o time opera bem.

Essa regra evita discutir framework como identidade. Framework é mitigação de risco.

### Sinal de resposta madura

Uma resposta madura não termina em "eu escolheria X". Ela termina em uma consequência operacional:

```text
Escolheria Fastify porque o contrato é schema-first,
então eu espero ver schemas em todas as rotas críticas,
OpenAPI derivado deles e testes de payload inválido.
```

Se não há consequência verificável no repositório, a decisão ainda é retórica.

## Armadilhas

1. Escolher por hype, não por fit: "todo mundo usa NestJS" não justifica projeto pequeno.
2. Migrar framework no meio do projeto sem motivo forte: custo alto e risco de regressão.
3. Comparar performance por benchmark sintético e ignorar DB, rede, payload e observability.
4. Achar que NestJS é só "Express com decorators": o modelo de módulos e DI muda a arquitetura.
5. Confundir framework com arquitetura: Express pode ter Clean Architecture; NestJS pode virar massa acoplada.
6. Ignorar deploy target: edge, container e Lambda têm constraints diferentes.
7. Escolher Fastify por performance e depois validar tudo manualmente em controller.
8. Escolher Hono por hype sem verificar bibliotecas de auth, observability e storage do runtime alvo.

## Perguntas de entrevista

**Como você escolheria entre Express e Fastify?**
Se o time precisa de simplicidade e ecossistema máximo, Express é baseline. Se contrato, validation e serialization são centrais, Fastify entrega mais estrutura sem virar framework enterprise.

**Quando NestJS é overkill?**
Quando o app é pequeno, tem poucas dependências, domínio raso e time pequeno. Nessa situação, DI manual e Express/Fastify podem ser mais claros.

**Quando Hono entra na conversa?**
Quando o deploy é edge ou multi-runtime. Hono não é "Express menor"; é um modelo baseado em Web Standards.

**Qual erro você espera de um candidato junior?**
Responder "NestJS é melhor" ou "Fastify é mais rápido" sem falar de problema, time, domínio e deploy target.

## Em entrevista

"Node has four main framework models in 2026. Express is middleware-based and ubiquitous; NestJS is opinionated, decorator-based, and built around dependency injection; Fastify is schema-first and performance-focused; Hono is ultralight, multi-runtime, and edge-first. The decision is matching, not ranking: pick based on deploy target, domain complexity, team size, and API contract needs."

Vocabulário-chave:

- middleware-based -> baseado em middleware
- opinionated -> opinativo
- schema-first -> orientado por schema
- edge-first -> pensado para edge
- decision matching -> matching entre problema e ferramenta

## Fontes

- [Express](https://expressjs.com/)
- [NestJS docs](https://docs.nestjs.com/)
- [Fastify](https://fastify.dev/)
- [Hono docs](https://hono.dev/docs)

## Veja também

- [[03-Dominios/Node/Frameworks e arquitetura/index]]
- [[02 - Express idiomático]]
- [[03 - NestJS - fundamentos]]
- [[05 - Fastify - schema-first, plugins, performance]]
- [[06 - Hono e edge runtimes]]
- [[12 - Decision tree + cheatsheet]]
- [[Node.js]]
