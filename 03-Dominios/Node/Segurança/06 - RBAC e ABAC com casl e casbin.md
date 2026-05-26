---
title: "RBAC e ABAC com casl e casbin"
created: 2026-05-13
updated: 2026-05-13
type: concept
status: growing
publish: true
tags:
  - node
  - segurança
  - autorização
  - rbac
  - abac
aliases:
  - RBAC Node
  - ABAC Node
  - casl
  - casbin
---

> [!abstract] TL;DR
> RBAC (Role-Based Access Control) mapeia papéis a conjuntos fixos de permissões — simples de modelar e auditar, ideal quando o conjunto de permissões é pequeno e estável. ABAC (Attribute-Based Access Control) avalia atributos do sujeito (usuário), do objeto (recurso) e do ambiente (horário, IP, tenant) para decisões de autorização de granularidade fina — mais expressivo, mas mais complexo de implementar e depurar. Na prática, use **casl** quando precisar de ABAC TypeScript-first com autorização baseada em propriedades do recurso, e use **casbin** quando precisar de políticas declarativas em arquivo (CSV, banco) com suporte a múltiplos modelos (ACL, RBAC, ABAC, REST).

## O que é

### RBAC — Role-Based Access Control

RBAC associa cada usuário a um ou mais **papéis** (roles). Cada papel carrega um conjunto fixo de permissões. A verificação é binária: o usuário tem o papel → tem a permissão.

```
Usuário → [admin, editor] → pode criar, editar, publicar post
Usuário → [viewer]        → pode apenas ler post
```

Características:
- Hierarquia plana — papéis não herdam automaticamente de outros papéis (salvo extensões explícitas)
- Fácil de auditar: "quem tem permissão X?" → "quem tem o papel Y?"
- Escalabilidade limitada: explosão de papéis quando permissões dependem do contexto

### ABAC — Attribute-Based Access Control

ABAC avalia **atributos** de três entidades para tomar a decisão:

| Entidade | Exemplos de atributos |
|----------|----------------------|
| **Sujeito** (usuário) | role, department, userId, plan |
| **Objeto** (recurso) | authorId, tenantId, status, visibility |
| **Ambiente** | IP, horário, país, método HTTP |

A decisão emerge de uma política como: "usuário pode editar post SE `post.authorId === user.id` E `post.status !== 'published'`".

### Quando usar cada um

| Critério | RBAC | ABAC |
|----------|------|------|
| Permissões simples e estáveis | Sim | Desnecessário |
| Permissões baseadas em propriedade do recurso | Não | Sim |
| Multi-tenant ou contexto dinâmico | Difícil | Sim |
| Auditoria e debugging simples | Sim | Mais complexo |
| Onboarding rápido da equipe | Sim | Exige estudo |

Regra prática: comece com RBAC e migre para ABAC (ou combine os dois) quando a lógica de autorização começar a vazar para a camada de negócio.

## Como funciona

### casl v6

**casl** é a biblioteca TypeScript-first de ABAC para Node.js. A abstração central é a `Ability`: um conjunto de regras `can`/`cannot` construídas com `AbilityBuilder`.

**Instalação:**

```bash
npm install @casl/ability
# Para integração com Mongoose:
npm install @casl/mongoose
```

**Definindo a ability do usuário:**

```typescript
// src/auth/ability.ts
import { AbilityBuilder, createMongoAbility, MongoAbility } from '@casl/ability'

type Actions = 'create' | 'read' | 'update' | 'delete' | 'manage'
type Subjects = 'Post' | 'Comment' | 'User' | 'all'

export type AppAbility = MongoAbility<[Actions, Subjects]>

export interface AuthUser {
  id: string
  roles: string[]
}

export function defineAbilityFor(user: AuthUser): AppAbility {
  const { can, cannot, build } = new AbilityBuilder<AppAbility>(createMongoAbility)

  if (user.roles.includes('admin')) {
    can('manage', 'all') // admin pode tudo
  } else if (user.roles.includes('editor')) {
    can('create', 'Post')
    can('read', 'Post')
    // Editor só edita e deleta os próprios posts (permissão condicional)
    can('update', 'Post', { authorId: user.id })
    can('delete', 'Post', { authorId: user.id })
    can('read', 'Comment')
    can('create', 'Comment')
  } else {
    // viewer
    can('read', 'Post')
    can('read', 'Comment')
  }

  // Nenhum usuário pode deletar posts publicados, independentemente do papel
  cannot('delete', 'Post', { status: 'published' }).because(
    'Published posts cannot be deleted'
  )

  return build()
}
```

**Verificando permissões:**

```typescript
// src/posts/posts.service.ts
import { defineAbilityFor } from '../auth/ability'
import { subject } from '@casl/ability'

async function getPost(user: AuthUser, postId: string) {
  const ability = defineAbilityFor(user)

  if (ability.cannot('read', 'Post')) {
    throw new Error('Forbidden')
  }

  return db.findPost(postId)
}

async function updatePost(user: AuthUser, postId: string, data: Partial<Post>) {
  const ability = defineAbilityFor(user)
  const post = await db.findPost(postId)

  // subject() é necessário para que casl avalie as condições do objeto
  if (ability.cannot('update', subject('Post', post))) {
    throw new Error('Forbidden: you can only edit your own posts')
  }

  return db.updatePost(postId, data)
}
```

**Permissões condicionais — só edita o próprio post:**

```typescript
// A regra abaixo permite 'update' apenas quando post.authorId === user.id
can('update', 'Post', { authorId: user.id })

// Verificação correta: passa o objeto real, não só a string 'Post'
const post = { id: '123', authorId: 'user-42', title: 'Olá' }
const ability = defineAbilityFor({ id: 'user-42', roles: ['editor'] })

ability.can('update', subject('Post', post))   // true — é o dono
ability.can('update', subject('Post', { ...post, authorId: 'outro' })) // false
```

### Middleware Express/NestJS com casl

**Express middleware — bloqueio por subject:**

```typescript
// src/middlewares/authorize.ts
import { Request, Response, NextFunction } from 'express'
import { subject as caslSubject, ForcedSubject } from '@casl/ability'
import { defineAbilityFor, Actions, Subjects } from '../auth/ability'

type ResourceLoader = (req: Request) => Promise<Record<string, unknown>>

export function authorize(
  action: Actions,
  subjectType: Subjects,
  loadResource?: ResourceLoader
) {
  return async (req: Request, res: Response, next: NextFunction) => {
    try {
      const user = req.user // populado por middleware de autenticação JWT
      if (!user) return res.status(401).json({ error: 'Unauthorized' })

      const ability = defineAbilityFor(user)

      if (loadResource) {
        const resource = await loadResource(req)
        if (ability.cannot(action, caslSubject(subjectType, resource))) {
          return res.status(403).json({ error: 'Forbidden' })
        }
      } else {
        if (ability.cannot(action, subjectType)) {
          return res.status(403).json({ error: 'Forbidden' })
        }
      }

      next()
    } catch (err) {
      next(err)
    }
  }
}

// Uso nas rotas:
// router.put('/posts/:id',
//   authenticate,
//   authorize('update', 'Post', (req) => db.findPost(req.params.id)),
//   postsController.update
// )
```

**NestJS — Guard com casl:**

```typescript
// src/auth/casl.guard.ts
import { CanActivate, ExecutionContext, Injectable, ForbiddenException, SetMetadata } from '@nestjs/common'
import { Reflector } from '@nestjs/core'
import { defineAbilityFor, Actions, Subjects } from './ability'

export const CHECK_ABILITY = 'check_ability'

// Decorator para marcar o handler
export const UseAbility = (action: Actions, subject: Subjects) =>
  SetMetadata(CHECK_ABILITY, { action, subject })

@Injectable()
export class CaslGuard implements CanActivate {
  constructor(private reflector: Reflector) {}

  async canActivate(context: ExecutionContext): Promise<boolean> {
    const rule = this.reflector.get<{ action: Actions; subject: Subjects }>(
      CHECK_ABILITY,
      context.getHandler()
    )
    if (!rule) return true // sem restrição definida no handler

    const request = context.switchToHttp().getRequest()
    const user = request.user
    if (!user) throw new ForbiddenException('Not authenticated')

    const ability = defineAbilityFor(user)
    if (ability.cannot(rule.action, rule.subject)) {
      throw new ForbiddenException('Insufficient permissions')
    }
    return true
  }
}

// Uso no controller:
// @UseGuards(JwtAuthGuard, CaslGuard)
// @UseAbility('delete', 'Post')
// @Delete(':id')
// async remove(@Param('id') id: string) { ... }
```

### casbin

**casbin** separa o **modelo de controle de acesso** (arquivo `.conf`) das **políticas** (CSV, banco de dados, Redis). Suporta ACL, RBAC, ABAC e modelos híbridos.

**Instalação:**

```bash
npm install casbin
```

**Arquivo de modelo — `model.conf`:**

```ini
# model.conf
[request_definition]
r = sub, obj, act

[policy_definition]
p = sub, obj, act

[role_definition]
g = _, _

[policy_effect]
e = some(where (p.eft == allow))

[matchers]
m = g(r.sub, p.sub) && r.obj == p.obj && r.act == p.act
```

**Arquivo de políticas — `policy.csv`:**

```csv
p, admin, /posts, read
p, admin, /posts, write
p, admin, /posts, delete
p, editor, /posts, read
p, editor, /posts, write
p, viewer, /posts, read

g, alice, admin
g, bob, editor
g, carol, viewer
```

**Uso no código:**

```typescript
// src/auth/casbin.ts
import { newEnforcer, Enforcer } from 'casbin'
import path from 'path'

let enforcer: Enforcer

async function getEnforcer(): Promise<Enforcer> {
  if (!enforcer) {
    enforcer = await newEnforcer(
      path.resolve(__dirname, 'model.conf'),
      path.resolve(__dirname, 'policy.csv')
    )
  }
  return enforcer
}

// Verificação de autorização (async)
async function checkAccess(user: string, resource: string, action: string): Promise<boolean> {
  const e = await getEnforcer()
  return e.enforce(user, resource, action)
}

// Exemplo de uso em middleware Express:
export async function casbinMiddleware(req: Request, res: Response, next: NextFunction) {
  const user = req.user?.id ?? 'anonymous'
  const resource = `/${req.path.split('/')[1]}` // e.g., /posts
  const action = req.method === 'GET' ? 'read' : 'write'

  const allowed = await checkAccess(user, resource, action)
  if (!allowed) {
    return res.status(403).json({ error: 'Forbidden' })
  }
  next()
}
```

**Adapter de banco de dados (PostgreSQL via TypeORM):**

```typescript
import { newEnforcer } from 'casbin'
import { TypeORMAdapter } from 'typeorm-adapter'

const adapter = await TypeORMAdapter.newAdapter({
  type: 'postgres',
  host: process.env.DB_HOST,
  port: Number(process.env.DB_PORT),
  username: process.env.DB_USER,
  password: process.env.DB_PASS,
  database: process.env.DB_NAME,
})

const enforcer = await newEnforcer('model.conf', adapter)
// Políticas agora vivem no banco; use enforcer.addPolicy(), removePolicy() etc.
await enforcer.addPolicy('alice', '/posts', 'delete')
await enforcer.savePolicy()
```

## Integração com JWT

O padrão mais comum em APIs stateless é embutir os papéis (e opcionalmente permissões granulares) diretamente no payload do JWT.

```typescript
// src/auth/jwt.ts
import jwt from 'jsonwebtoken'
import { defineAbilityFor, AuthUser } from './ability'

interface JwtPayload {
  sub: string
  roles: string[]
  permissions?: string[] // opcional: permissões granulares pré-computadas
  iat: number
  exp: number
}

// Ao gerar o token (login / refresh):
function signToken(user: AuthUser): string {
  const payload: JwtPayload = {
    sub: user.id,
    roles: user.roles, // e.g., ['editor']
    permissions: computePermissions(user), // opcional
    iat: Math.floor(Date.now() / 1000),
    exp: Math.floor(Date.now() / 1000) + 3600,
  }
  return jwt.sign(payload, process.env.JWT_SECRET!)
}

// Middleware de autenticação — popula req.user e req.ability:
export async function authenticate(req: Request, res: Response, next: NextFunction) {
  const token = req.headers.authorization?.replace('Bearer ', '')
  if (!token) return res.status(401).json({ error: 'No token' })

  try {
    const payload = jwt.verify(token, process.env.JWT_SECRET!, { algorithms: ['HS256'] }) as JwtPayload
    const user: AuthUser = { id: payload.sub, roles: payload.roles }
    req.user = user
    // Instância de Ability criada uma vez por requisição
    req.ability = defineAbilityFor(user)
    next()
  } catch {
    res.status(401).json({ error: 'Invalid token' })
  }
}

function computePermissions(user: AuthUser): string[] {
  const map: Record<string, string[]> = {
    admin: ['posts:read', 'posts:write', 'posts:delete', 'users:manage'],
    editor: ['posts:read', 'posts:write'],
    viewer: ['posts:read'],
  }
  return user.roles.flatMap((r) => map[r] ?? [])
}
```

**Declaração de tipo para augmentar Express `Request`:**

```typescript
// src/@types/express/index.d.ts
import { AppAbility, AuthUser } from '../../auth/ability'

declare global {
  namespace Express {
    interface Request {
      user?: AuthUser
      ability?: AppAbility
    }
  }
}
```

Boas práticas ao usar JWT com roles/permissions:
- Nunca coloque permissões sensíveis apenas no frontend — o backend sempre reverifica
- Mantenha o token curto (1h) e use refresh token para renovação
- Se revogar papel de um usuário, invalide o token ativamente (lista negra ou versão de revogação no Redis) — JWT é stateless por padrão

## Princípio do menor privilégio

O **princípio do menor privilégio** (Principle of Least Privilege — PoLP) determina que cada usuário, processo ou serviço deve ter acesso apenas ao mínimo necessário para executar sua função.

**Como aplicar em RBAC/ABAC:**

1. **Deny-by-default**: o ponto de partida é "tudo negado". Permissões são concedidas explicitamente.

   ```typescript
   // Em casl, o build() sem nenhum can() retorna uma ability que nega tudo.
   // Nunca comece com can('manage', 'all') para todos os usuários.
   ```

2. **Grants explícitos e mínimos**: adicione apenas as permissões necessárias para o papel. Revisite os papéis periodicamente.

3. **Auditoria de decisões de autorização**: registre toda decisão de `allow` e `deny` com contexto suficiente para investigação.

   ```typescript
   // src/middlewares/authorize.ts — adicionar log de auditoria
   import { logger } from '../utils/logger'

   function logAuthDecision(
     user: AuthUser,
     action: string,
     subject: string,
     allowed: boolean,
     reason?: string
   ) {
     logger.info({
       event: 'authorization_decision',
       userId: user.id,
       roles: user.roles,
       action,
       subject,
       allowed,
       reason: reason ?? null,
       timestamp: new Date().toISOString(),
     })
   }
   ```

4. **Separação de papéis (Separation of Duties)**: papéis críticos devem ser distintos — quem cria não deve poder aprovar, quem aprova não deve poder pagar.

5. **Expiração de acessos**: papéis temporários (ex: acesso de suporte) devem ter validade. Implemente `expiresAt` por papel no banco.

## Armadilhas

> [!danger] Autorização apenas no frontend
> Verificar permissões somente no cliente (esconder botão, desabilitar rota no React Router) não é segurança — é UX. Um usuário pode chamar a API diretamente com curl ou Postman. Toda decisão de autorização deve ser reforçada no backend, na camada de serviço ou em middleware dedicado, nunca apenas no frontend.

> [!danger] Papéis hardcoded no código (`if (user.role === 'admin')`)
> Hardcodar papéis espalha lógica de autorização pelo codebase, torna o sistema frágil a refatorações e impossibilita gerenciar papéis dinamicamente. Os papéis devem vir do banco de dados ou do JWT — centralize toda lógica de autorização em `defineAbility` ou em políticas casbin. Buscar `user.role === ` no código é um code smell direto.

> [!danger] Ausência de log de decisões de autorização
> Sem auditoria de eventos de `Forbidden` e `Allowed`, é impossível detectar abusos, investigar incidentes de segurança ou demonstrar conformidade (LGPD, SOC 2). Toda decisão de autorização negada deve ser logada com userId, recurso, ação e timestamp. Decisões positivas em recursos sensíveis (dados financeiros, PII) também devem ser logadas.

## Em entrevista

**Q: What is the difference between RBAC and ABAC, and when would you choose one over the other?**

A: RBAC assigns permissions to roles and then assigns roles to users — the authorization check is essentially a set membership test: does the user's role set contain a role that grants this permission? It is simple to implement, easy to audit ("who can delete posts?" → "anyone with the `admin` role"), and scales well for coarse-grained access control. ABAC, on the other hand, evaluates policies against attributes of the subject (user properties like `department` or `plan`), the object (resource properties like `authorId`, `status`, `tenantId`), and the environment (time of day, IP address). This makes ABAC far more expressive but also more complex to reason about and debug. I choose RBAC when the permission matrix is small and stable — think internal tools or simple SaaS tiers. I switch to ABAC (or a hybrid) when authorization depends on resource ownership or contextual conditions, for example "a user can only edit their own draft posts." Libraries like casl let you express ABAC rules in TypeScript with conditional `can('update', 'Post', { authorId: user.id })` clauses, giving you the expressiveness of ABAC with manageable complexity.

**Q: How do you implement resource-level authorization in casl — for example, allowing users to only edit their own posts?**

A: The key is combining a conditional rule with the `subject()` helper at the point of checking. When defining the ability, you write `can('update', 'Post', { authorId: user.id })` — the third argument is a MongoDB-style condition that casl stores alongside the rule. At check time, you must pass the actual resource instance wrapped with `subject('Post', post)` rather than just the string `'Post'`; otherwise casl cannot evaluate the condition and will default to denying. A common mistake is calling `ability.can('update', 'Post')` without the real object — that check ignores conditions entirely and may return `false` even when the user owns the resource. The correct pattern in a service method is: fetch the record from the database first, then call `ability.cannot('update', subject('Post', post))` and throw a `403` if it returns `true`. This ensures the authorization decision is always made against the real data, not a hypothetical type.

**Q: What is the principle of least privilege and how do you implement it in a Node.js API?**

A: The principle of least privilege means every entity — user, service account, or process — should have access to exactly what it needs and nothing more. In a Node.js API, I implement this at several layers. First, I use a deny-by-default posture: in casl, an `AbilityBuilder` that never calls `can()` produces an ability that denies everything; I never start with `can('manage', 'all')` for non-admin roles. Second, I assign narrow, role-specific grants: editors can create and update their own posts but cannot delete published posts or manage users. Third, I centralize authorization logic in a single `defineAbility` function so the rules are auditable and testable in isolation. Fourth, I add structured logging for every authorization decision, especially denials, so we can detect anomalous access patterns. Fifth, I apply the principle to service accounts and environment variables too — a microservice that only reads posts should use database credentials scoped to `SELECT` on the `posts` table, not a full `DATABASE_ADMIN` role. Regular access reviews (quarterly) ensure that roles do not accumulate permissions over time.

## Vocabulário

| Termo | Definição |
|-------|-----------|
| **RBAC** | Role-Based Access Control — modelo de autorização que mapeia papéis a permissões e usuários a papéis |
| **ABAC** | Attribute-Based Access Control — modelo de autorização que avalia atributos do sujeito, objeto e ambiente para tomar decisões de acesso |
| **Permission** | Autorização para executar uma ação específica sobre um recurso específico (ex: `update:Post`) |
| **Policy** | Regra declarativa que define quem pode fazer o quê sob quais condições; em casbin, persistida em arquivo ou banco |
| **Principal** | Entidade que solicita acesso — usuário, serviço, processo ou sistema |
| **Least Privilege** | Princípio que determina que cada entidade deve ter o mínimo de permissões necessário para sua função |
| **Subject** | Em ABAC, a entidade que solicita o acesso (usuário ou serviço); em casl, o tipo ou instância do recurso alvo |
| **Action** | Operação solicitada sobre o recurso: `read`, `create`, `update`, `delete`, `manage` |
| **Enforce** | Ato de verificar se uma requisição de acesso é permitida pela política vigente; termo central do casbin |
| **Deny-by-default** | Postura de segurança onde todo acesso é negado até que uma regra explícita o permita |

## Veja também

- [[03-Dominios/Node/Segurança/index|Segurança]]
- [[03-Dominios/Node/Segurança/04 - JWT e autenticação com jsonwebtoken|JWT e autenticação]]
- [[JavaScript/Backend/Node.js|Node.js]]
- [casl.js.org — documentação oficial](https://casl.js.org)
- [casbin.org — documentação oficial](https://casbin.org)
- [OWASP — Broken Access Control](https://owasp.org/Top10/A01_2021-Broken_Access_Control/)
