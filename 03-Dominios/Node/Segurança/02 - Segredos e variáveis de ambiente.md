---
title: "Segredos e variáveis de ambiente"
created: 2026-05-12
updated: 2026-05-12
type: concept
status: growing
publish: true
tags:
  - node
  - segurança
  - env-vars
  - secrets
aliases:
  - Segredos Node
  - Env Vars Segurança
---

# Segredos e variáveis de ambiente

> [!abstract] TL;DR
> Segredos — chaves de API, senhas de banco, tokens OAuth — jamais devem estar hardcoded no código-fonte ou commitados no repositório; o vetor de vazamento mais comum em projetos Node.js é exatamente um `.env` esquecido no histórico do git. Em desenvolvimento, `process.env` carregado via `node --env-file=.env` (Node 20.6+) ou `dotenv` fornece segredos sem hardcode; em produção, o padrão de mercado é injetar segredos dinamicamente em runtime a partir de um secrets manager (AWS Secrets Manager, HashiCorp Vault, Doppler ou GCP Secret Manager), eliminando segredos em arquivos de configuração. A validação de variáveis de ambiente com Zod na inicialização da aplicação — `fail-fast` — é a linha de defesa que converte erros de configuração silenciosos em falhas imediatas e mensagens de erro acionáveis.

## O que é

**Variáveis de ambiente** (`env vars`) são pares chave-valor injetados no processo do sistema operacional — acessíveis via `process.env` em Node.js — para parametrizar a aplicação sem alterar o código-fonte. Elas separam configuração de código, seguindo o princípio 12-Factor App (fator III: config).

**Segredos** são um subconjunto crítico das variáveis de ambiente: valores que concedem acesso privilegiado a sistemas externos — credenciais de banco de dados, chaves de API de terceiros, tokens de autenticação, certificados privados. A diferença prática é que segredos exigem controles adicionais de acesso, rotação e auditoria que variáveis de configuração comuns não requerem.

O problema fundamental é que segredos são difíceis de manter separados do código. Desenvolvedores os colocam em arquivos de configuração que acabam sendo commitados, os imprimem em logs para debug, ou os deixam hardcoded em trechos "temporários" que persistem por anos. Cada um desses antipadrões cria um vetor de comprometimento concreto.

## Como funciona

### Antipadrões — o que NÃO fazer

**1. Hardcode no código-fonte**

```javascript
// ❌ NUNCA FAÇA ISSO — expõe a credencial a qualquer pessoa com acesso ao repositório
const db = new Client({
  host: 'prod-db.acme.internal',
  user: 'admin',
  password: 'P@ssw0rd!2024',        // hardcoded
  database: 'acme_production',
});

const stripe = new Stripe('sk_live_AbCdEf123456789XyZ'); // chave de produção no código
```

Mesmo em repositórios privados, a credencial fica no histórico git para sempre — `git log -S 'P@ssw0rd'` a encontra mesmo após um commit de remoção. Ferramentas como `trufflehog` e `git-secrets` escaneiam histórico completo.

**2. `.env` commitado no git**

```bash
# ❌ .gitignore sem .env = desastre silencioso
# Se .env não está no .gitignore, um simples `git add .` o inclui
git add .
git commit -m "add config"    # .env vai junto sem nenhum aviso
git push origin main          # credenciais agora no GitHub/GitLab
```

Uma vez commitado, mesmo que removido, o arquivo permanece acessível via `git log --all -- .env` ou clones feitos antes da remoção.

**3. `console.log` de segredos em debug**

```javascript
// ❌ Log de env vars para debug — vai parar em Datadog, CloudWatch, Splunk
app.use((req, res, next) => {
  console.log('Environment:', process.env);  // expõe TODOS os segredos do processo
  next();
});

// ❌ Também perigoso — frameworks de log estruturado serializam objetos inteiros
logger.debug({ config: process.env }, 'Starting server');
```

Logs são frequentemente coletados por sistemas de observabilidade com retenção de 30-90 dias e acessíveis a múltiplas equipes — muito além do acesso esperado para um segredo de produção.

**4. Segredos em variáveis de Docker Compose sem external secrets**

```yaml
# ❌ Segredos em plaintext no docker-compose.yml (commitado no repositório)
services:
  api:
    environment:
      DATABASE_URL: postgresql://admin:P@ssw0rd@db:5432/prod
      STRIPE_SECRET_KEY: sk_live_AbCdEf123456789XyZ
      JWT_SECRET: minha-chave-super-secreta
```

O arquivo `docker-compose.yml` é quase sempre commitado. Qualquer pessoa com acesso ao repositório tem acesso a todos os segredos de produção.

### `node --env-file=.env` (Node 20.6+)

A partir do Node.js 20.6.0, é possível carregar um arquivo `.env` diretamente pelo runtime sem nenhuma dependência externa:

```bash
# Carrega .env antes de executar o script
node --env-file=.env src/server.js

# Com múltiplos arquivos (o último tem precedência em caso de conflito)
node --env-file=.env --env-file=.env.local src/server.js

# Arquivo opcional — não falha se o arquivo não existir (Node 22.9+)
node --env-file-if-exists=.env.local --env-file=.env src/server.js
```

**Sintaxe suportada no arquivo `.env`:**

```bash
# Comentários com #
DATABASE_URL=postgresql://localhost:5432/myapp

# Aspas são opcionais para valores simples, necessárias para espaços
APP_NAME="Minha Aplicação"

# Expansão de variável (Node 20.12+)
BASE_URL=https://api.example.com
WEBHOOK_URL=${BASE_URL}/webhooks

# Valores multilinha com aspas duplas
PRIVATE_KEY="-----BEGIN RSA PRIVATE KEY-----
MIIEpAIBAAKCAQEA...
-----END RSA PRIVATE KEY-----"
```

**Comparação com `dotenv`:**

| Característica | `node --env-file` | `dotenv` |
|---|---|---|
| Dependência externa | Nenhuma | `npm install dotenv` |
| Node.js mínimo | 20.6.0 | Qualquer versão |
| `--env-file-if-exists` | 22.9+ | Via `dotenv.config({ quiet: true })` |
| Override de env existente | Não (env do shell tem precedência) | Configurável |
| Expansão de variáveis | 20.12+ | Via `dotenv-expand` |
| Integração com debuggers | Transparente | Requer `require('dotenv').config()` |

**Quando ainda usar `dotenv`:**

- Node.js < 20.6 em produção ou em pipelines legados
- Necessidade de carregar `.env` programaticamente dentro do código (não apenas no startup)
- Uso de funcionalidades avançadas como `dotenv-vault` ou integração com Doppler via CLI

```javascript
// dotenv — uso moderno com ES modules
import 'dotenv/config';          // carrega .env automaticamente
// ou
import dotenv from 'dotenv';
dotenv.config({ path: '.env.local', override: true });
```

### Convenção `.env` local vs `.env.example` no git

A convenção canônica para gerenciar env vars em projetos colaborativos:

```
.env              ← NUNCA commitado — valores reais do desenvolvedor local
.env.example      ← SEMPRE commitado — template com placeholders
.env.test         ← Pode ser commitado — valores seguros para testes automatizados
.env.local        ← NUNCA commitado — overrides locais do desenvolvedor
```

**`.gitignore` mínimo para env vars:**

```gitignore
# Environment variables — nunca commitar valores reais
.env
.env.local
.env.*.local
.env.production
.env.staging

# Manter apenas o template
!.env.example
```

**`.env.example` bem documentado:**

```bash
# .env.example — template para novos desenvolvedores
# Copie este arquivo para .env e preencha com valores reais
# Nunca coloque valores reais neste arquivo

# Banco de dados
DATABASE_URL=postgresql://user:password@localhost:5432/myapp_dev

# Autenticação
JWT_SECRET=seu-jwt-secret-de-pelo-menos-32-caracteres
JWT_REFRESH_SECRET=outro-secret-diferente-para-refresh-tokens

# Integrações externas
STRIPE_SECRET_KEY=sk_test_...           # Use chave de teste, nunca produção
STRIPE_WEBHOOK_SECRET=whsec_...
SENDGRID_API_KEY=SG....

# AWS (use IAM roles em produção — estas vars são apenas para dev local)
AWS_ACCESS_KEY_ID=AKIA...
AWS_SECRET_ACCESS_KEY=...
AWS_REGION=us-east-1
```

**`.env.test` para testes automatizados:**

```bash
# .env.test — valores seguros para CI/CD e testes automatizados
# Pode ser commitado pois não contém credenciais reais de produção
NODE_ENV=test
DATABASE_URL=postgresql://postgres:postgres@localhost:5432/myapp_test
JWT_SECRET=test-jwt-secret-nao-usar-em-producao
STRIPE_SECRET_KEY=sk_test_fake_key_for_testing
```

## Gestão de segredos em produção

Em produção, segredos nunca devem existir em arquivos ou variáveis de ambiente estáticas configuradas na plataforma — eles devem ser **carregados dinamicamente em runtime** a partir de um secrets manager com controle de acesso, auditoria e rotação automática.

### AWS Secrets Manager

```javascript
// src/lib/secrets.js
import {
  SecretsManagerClient,
  GetSecretValueCommand,
} from '@aws-sdk/client-secrets-manager';

const client = new SecretsManagerClient({ region: process.env.AWS_REGION });

/**
 * Carrega um segredo do AWS Secrets Manager.
 * Em produção, a autenticação é feita via IAM Role atachada à instância EC2/ECS/Lambda.
 */
export async function getSecret(secretName) {
  const command = new GetSecretValueCommand({ SecretId: secretName });
  const response = await client.send(command);

  if (response.SecretString) {
    return JSON.parse(response.SecretString);
  }

  // Binary secret (certificados, chaves binárias)
  const buffer = Buffer.from(response.SecretBinary, 'base64');
  return buffer.toString('utf8');
}

// Uso na inicialização da aplicação
const dbSecrets = await getSecret('prod/myapp/database');
// dbSecrets = { username: 'app_user', password: 'rotated-password-xyz', host: 'rds.amazonaws.com' }

const pool = new Pool({
  host: dbSecrets.host,
  user: dbSecrets.username,
  password: dbSecrets.password,
  database: 'myapp',
  ssl: { rejectUnauthorized: true },
});
```

> **Prática recomendada:** configure rotação automática no AWS Secrets Manager com Lambda rotator — o segredo é rotacionado sem intervenção manual e a aplicação carrega o novo valor na próxima inicialização ou via SIGHUP.

### HashiCorp Vault

```javascript
// src/lib/vault.js — API HTTP direta com token de autenticação
import { fetch } from 'node-fetch'; // ou global fetch (Node 21+)

const VAULT_ADDR = process.env.VAULT_ADDR;   // ex: https://vault.acme.internal:8200
const VAULT_TOKEN = process.env.VAULT_TOKEN; // token injetado pelo orchestrator (Kubernetes)

export async function getVaultSecret(path) {
  // KV v2: endpoint é /v1/secret/data/<path>
  const response = await fetch(`${VAULT_ADDR}/v1/secret/data/${path}`, {
    headers: { 'X-Vault-Token': VAULT_TOKEN },
  });

  if (!response.ok) {
    throw new Error(`Vault error: ${response.status} ${response.statusText}`);
  }

  const body = await response.json();
  return body.data.data; // KV v2 tem duplo .data
}

// Em Kubernetes, o VAULT_TOKEN é injetado via Vault Agent Injector como sidecar
// ou via CSI Secrets Store Driver, sem nunca aparecer no código
const dbCreds = await getVaultSecret('prod/myapp/database');
```

### Doppler

```bash
# CLI: injeta segredos como env vars no processo filho sem salvar em disco
doppler run -- node src/server.js

# Em Dockerfile (CI/CD com Doppler):
# doppler run --token=$DOPPLER_TOKEN -- node dist/server.js
```

```javascript
// Integração programática via Doppler API (quando CLI não é viável)
// src/lib/doppler.js
const DOPPLER_TOKEN = process.env.DOPPLER_TOKEN;

export async function getDopplerSecret(project, config, name) {
  const url = `https://api.doppler.com/v3/configs/config/secret?project=${project}&config=${config}&name=${name}`;
  const response = await fetch(url, {
    headers: {
      Authorization: `Bearer ${DOPPLER_TOKEN}`,
      'Content-Type': 'application/json',
    },
  });
  const body = await response.json();
  return body.value.raw;
}
```

### GCP Secret Manager

```javascript
// src/lib/gcp-secrets.js
import { SecretManagerServiceClient } from '@google-cloud/secret-manager';

const client = new SecretManagerServiceClient();
// Autenticação via Application Default Credentials (ADC)
// Em GKE/Cloud Run: Workload Identity Federation — sem service account keys em disco

export async function getGcpSecret(projectId, secretId, version = 'latest') {
  const name = `projects/${projectId}/secrets/${secretId}/versions/${version}`;
  const [secretVersion] = await client.accessSecretVersion({ name });
  return secretVersion.payload.data.toString('utf8');
}

// Uso na inicialização
const PROJECT_ID = process.env.GOOGLE_CLOUD_PROJECT;
const dbPassword = await getGcpSecret(PROJECT_ID, 'db-password');
```

## Validação de env vars com Zod na inicialização

A ausência de uma variável de ambiente crítica frequentemente causa erros crípticos em runtime — um `Cannot read properties of undefined` em vez de "DATABASE_URL não foi configurada". O padrão `fail-fast` com Zod resolve isso.

```javascript
// src/config/env.js — schema de validação executado na inicialização
import { z } from 'zod';

const envSchema = z.object({
  // Node environment
  NODE_ENV: z.enum(['development', 'test', 'production']).default('development'),
  PORT: z.coerce.number().int().min(1).max(65535).default(3000),

  // Banco de dados
  DATABASE_URL: z.string().url('DATABASE_URL deve ser uma URL PostgreSQL válida'),
  DATABASE_POOL_MAX: z.coerce.number().int().min(1).max(100).default(10),

  // Autenticação — segredos obrigatórios em produção
  JWT_SECRET: z.string().min(32, 'JWT_SECRET deve ter pelo menos 32 caracteres'),
  JWT_REFRESH_SECRET: z
    .string()
    .min(32, 'JWT_REFRESH_SECRET deve ter pelo menos 32 caracteres'),
  JWT_ACCESS_TTL: z.string().default('15m'),
  JWT_REFRESH_TTL: z.string().default('7d'),

  // AWS (opcionais — em produção usa IAM Role)
  AWS_REGION: z.string().default('us-east-1'),
  AWS_SECRET_NAME: z.string().optional(),

  // Stripe
  STRIPE_SECRET_KEY: z
    .string()
    .startsWith('sk_', 'STRIPE_SECRET_KEY deve começar com sk_'),
  STRIPE_WEBHOOK_SECRET: z
    .string()
    .startsWith('whsec_', 'STRIPE_WEBHOOK_SECRET deve começar com whsec_'),
}).refine(
  (env) => {
    // Em produção, JWT_SECRET não pode ser um valor de desenvolvimento
    if (env.NODE_ENV === 'production') {
      return !env.JWT_SECRET.includes('dev') && !env.JWT_SECRET.includes('test');
    }
    return true;
  },
  { message: 'JWT_SECRET contém valor de desenvolvimento em NODE_ENV=production' }
);

// Fail-fast: lança exceção detalhada imediatamente se env vars estão erradas
let env;
try {
  env = envSchema.parse(process.env);
} catch (error) {
  if (error instanceof z.ZodError) {
    console.error('❌ Configuração de ambiente inválida:\n');
    error.errors.forEach(({ path, message }) => {
      console.error(`  ${path.join('.')}: ${message}`);
    });
    process.exit(1); // falha rápida — nunca sobe com config inválida
  }
  throw error;
}

export default env;
```

```javascript
// src/server.js — importa config validada, não process.env diretamente
import env from './config/env.js';

// A partir daqui, env é tipado e garantidamente correto
const server = app.listen(env.PORT, () => {
  console.log(`Server running on port ${env.PORT} (${env.NODE_ENV})`);
});
```

O output em caso de erro é imediatamente acionável:

```
❌ Configuração de ambiente inválida:

  DATABASE_URL: DATABASE_URL deve ser uma URL PostgreSQL válida
  JWT_SECRET: JWT_SECRET deve ter pelo menos 32 caracteres
  STRIPE_SECRET_KEY: STRIPE_SECRET_KEY deve começar com sk_
```

## Rotação de segredos sem downtime

Rotação de segredos em produção exige que duas versões de uma credencial sejam válidas simultaneamente durante o período de transição — a antiga (para requests em voo) e a nova (para requests novos).

### Graceful reload com SIGHUP

```javascript
// src/server.js — recarrega segredos sem reiniciar o processo
import { getSecret } from './lib/secrets.js';

let currentSecrets = await loadSecrets();

async function loadSecrets() {
  const [dbCreds, stripeKey] = await Promise.all([
    getSecret('prod/myapp/database'),
    getSecret('prod/myapp/stripe'),
  ]);
  return { dbCreds, stripeKey };
}

// SIGHUP: convencional para "recarregar configuração sem reiniciar"
process.on('SIGHUP', async () => {
  console.log('[secrets] SIGHUP recebido — recarregando segredos...');
  try {
    const newSecrets = await loadSecrets();
    currentSecrets = newSecrets;
    console.log('[secrets] Segredos recarregados com sucesso');
  } catch (err) {
    // Falha ao recarregar: mantém segredos anteriores (não derruba o servidor)
    console.error('[secrets] Falha ao recarregar segredos, mantendo versão anterior:', err.message);
  }
});

// Em Kubernetes: kubectl exec <pod> -- kill -HUP 1
// Em ECS: evento de rotação do Secrets Manager dispara lambda que envia SIGHUP
```

### Duas versões simultâneas durante rotação

O padrão para rotação sem downtime é manter a credencial antiga válida até que todos os processos em execução tenham recarregado a nova:

```
Fase 1 — Criar nova versão:
  Secrets Manager cria nova senha no banco e publica como versão AWSPENDING
  Credencial antiga (AWSCURRENT) continua válida

Fase 2 — Testar nova versão:
  Lambda rotator verifica que AWSPENDING conecta ao banco com sucesso

Fase 3 — Promover nova versão:
  AWSPENDING vira AWSCURRENT
  Lambda envia SIGHUP para todos os pods via ECS/Kubernetes API
  Pods recarregam segredos (1-5 segundos de janela)

Fase 4 — Deprecar versão antiga:
  Após TTL configurado (ex: 5 minutos), revogar credencial antiga
```

Para JWT, a rotação usa um array de segredos aceitos para verificação:

```javascript
// Suporte a múltiplos secrets durante rotação de JWT
const JWT_SECRETS = [
  env.JWT_SECRET,              // segredo atual
  env.JWT_SECRET_PREVIOUS,     // segredo anterior (opcional, durante rotação)
].filter(Boolean);

function verifyToken(token) {
  for (const secret of JWT_SECRETS) {
    try {
      return jwt.verify(token, secret);
    } catch {
      // Tenta o próximo secret
    }
  }
  throw new Error('Token inválido ou expirado');
}
```

## Armadilhas

> [!danger] Vazar segredos em stack traces e error handlers
> **Problema:** O error handler padrão do Express serializa o objeto `err` inteiro — que frequentemente inclui propriedades da conexão com banco (host, user, password), headers HTTP com tokens de autenticação, ou o objeto `process.env` completo quando o erro acontece durante inicialização. Qualquer cliente que acione um erro 500 recebe essas informações.
>
> ```javascript
> // ❌ Error handler que vaza internals
> app.use((err, req, res, next) => {
>   res.status(500).json({ error: err }); // serializa err.config, err.request, etc.
> });
>
> // ✅ Error handler seguro — log interno, resposta genérica para o cliente
> app.use((err, req, res, next) => {
>   logger.error({ err, requestId: req.id }, 'Unhandled error'); // log estruturado interno
>   res.status(500).json({
>     error: 'Internal server error',
>     requestId: req.id, // para correlação com logs — sem detalhes do erro
>   });
> });
> ```
>
> **Solução:** Nunca serialize `err` diretamente na resposta HTTP. Logue internamente com correlação por `requestId` e retorne mensagens genéricas ao cliente. Em Express, use `err.expose = true` explicitamente apenas para erros operacionais que devem ser retornados ao cliente.

> [!danger] `process.env` em logs estruturados (Pino/Winston serializers)
> **Problema:** Pino e Winston serializam objetos automaticamente. Um `logger.info({ env: process.env })` ou um serializer que inclui `process.env` por engano expõe todos os segredos do processo nos logs de produção — que são coletados pelo Datadog, CloudWatch, ou ELK Stack e podem ser acessados por múltiplas equipes.
>
> ```javascript
> // ❌ Pino com serializer que captura process.env acidentalmente
> const logger = pino({
>   serializers: {
>     req: (req) => ({
>       method: req.method,
>       url: req.url,
>       env: process.env, // ← vaza TODOS os segredos
>     }),
>   },
> });
>
> // ✅ Serializers explícitos com allowlist
> const logger = pino({
>   redact: ['req.headers.authorization', 'req.headers.cookie', '*.password', '*.token'],
>   serializers: {
>     req: (req) => ({
>       method: req.method,
>       url: req.url,
>       // Apenas campos específicos, nunca process.env
>     }),
>   },
> });
> ```
>
> **Solução:** Use `pino-redact` ou a opção `redact` do Pino para mascarar campos sensíveis automaticamente. Defina um serializer explícito com allowlist de campos — nunca serialize objetos inteiros de request, error ou config.

> [!danger] `.env.production` no repositório
> **Problema:** Desenvolvedores frequentemente criam `.env.production` com valores reais de produção para "facilitar o deploy" e o commitam no repositório privado. Credenciais de produção em repositório — mesmo privado — violam o princípio de least privilege: qualquer dev do time com acesso ao repositório tem acesso às credenciais de produção, mesmo que não devesse.
>
> **Solução:** Qualquer arquivo `.env.*` que contenha valores reais de produção (não placeholders) deve estar no `.gitignore`. Segredos de produção vivem exclusivamente no secrets manager. O `.env.example` é o único arquivo de ambiente que vai para o repositório.

## Em entrevista

**Q: How do you manage secrets in a Node.js production application?**

A: My approach follows a strict separation between development and production secret management. In development, I use `node --env-file=.env` (Node 20.6+) or dotenv to load secrets from a local `.env` file that's in `.gitignore` — never committed. I always maintain a `.env.example` with documented placeholders in the repository so developers know exactly what to configure. In production, I never use static environment variables baked into deployment configs. Instead, secrets are loaded at runtime from a secrets manager — AWS Secrets Manager via `@aws-sdk/client-secrets-manager`, HashiCorp Vault, or Doppler, depending on the infrastructure. The application authenticates to the secrets manager using IAM roles or Workload Identity, not hardcoded credentials. On top of that, I validate all environment variables with a Zod schema at application startup — fail-fast, with clear error messages — so misconfiguration fails immediately on boot rather than causing cryptic runtime errors hours later.

---

**Q: What's wrong with storing secrets in environment variables directly?**

A: Environment variables are a decent transport mechanism, but they have concrete security weaknesses that are often underestimated. First, they're visible to all child processes — any subprocess spawned by your Node.js app inherits the full `process.env`, including all secrets, which is a problem if you're running third-party code or shelling out. Second, they can easily leak into logs — a single `console.log(process.env)` or a Pino serializer that captures too much will dump all secrets into your observability platform. Third, in container orchestration platforms, environment variables are often stored in plaintext in the orchestrator's config store — in Kubernetes, they end up in etcd unless you use a Secrets Store CSI driver. Fourth, there's no audit trail — you can't tell who accessed a value or when. A secrets manager solves all of these: values are stored encrypted, access is controlled by IAM policies, every read is audited, and rotation is automated. The environment variable is still the delivery mechanism — the secrets manager just ensures the values are injected dynamically at runtime rather than statically baked in.

---

**Q: How would you handle secret rotation without downtime in Node.js?**

A: Secret rotation without downtime requires three things working together. First, the secrets manager — I use AWS Secrets Manager with automatic rotation enabled, which creates a Lambda rotator that generates a new credential, validates it works, and atomically promotes it to the current version while keeping the previous version valid for a configurable window. Second, the application needs to reload secrets without restarting — I implement a SIGHUP handler that re-fetches secrets from the manager and swaps them in-memory. In Kubernetes, a controller sends SIGHUP to all pods after rotation completes. Third, for JWT specifically, I maintain an array of accepted signing secrets during rotation — the new secret for signing new tokens, and the previous one still accepted for verifying tokens issued before rotation. The overlap window is typically 5-15 minutes, which covers all in-flight requests. The critical constraint is that the transition between credential versions must be atomic from the application's perspective — you never have a moment where neither the old nor the new credential is valid.

---

**Q: Why should you validate environment variables with Zod at startup?**

A: Because the alternative is discovering misconfiguration in production under load, at 2am, with a cryptic error message like `Cannot read properties of undefined (reading 'split')` — which could mean DATABASE_URL was never set. Zod validation at startup gives you three things. First, fail-fast: the process exits immediately with a clear error list before serving any requests, which means the deployment fails visibly rather than deploying a broken instance. Second, type coercion: `PORT` comes in as a string from `process.env`, but `z.coerce.number()` converts it and validates it's a valid port — you never accidentally pass the string `"3000"` to a function expecting a number. Third, the rest of the codebase can import the validated `env` object and trust it's fully typed and conformant — no more defensive `process.env.X ?? 'default'` scattered across the code. In a team context, the Zod schema also serves as living documentation of every required and optional env var, which `.env.example` alone can't provide.

## Vocabulário

- **secret** — valor que concede acesso privilegiado a um sistema externo (senha de banco, chave de API, token OAuth, certificado privado); exige controles mais rígidos que variáveis de configuração comuns — criptografia em repouso, controle de acesso granular, auditoria de leitura e rotação periódica
- **env var** — variável de ambiente; par chave-valor injetado no processo do sistema operacional, acessível via `process.env` em Node.js; mecanismo padrão de configuração de aplicações 12-Factor
- **vault** — servidor de gestão de segredos (ex: HashiCorp Vault); armazena segredos criptografados, auditando cada acesso e suportando rotação automática; o termo genérico também é usado para AWS Secrets Manager, GCP Secret Manager, etc.
- **rotation** — substituição periódica de um segredo por um novo valor sem interrupção do serviço; requer que versão antiga e nova sejam válidas simultaneamente durante uma janela de transição; mitigação fundamental contra comprometimento de credenciais de longa duração
- **least privilege** — princípio de segurança pelo qual cada componente do sistema tem acesso apenas aos recursos e segredos estritamente necessários para sua função — uma API de leitura de catálogo não deve ter acesso às credenciais do banco de dados financeiro
- **secret sprawl** — proliferação descontrolada de segredos espalhados por múltiplos locais sem inventário central: hardcoded em código, em arquivos `.env` em máquinas de desenvolvedores, em variáveis de CI/CD de múltiplas plataformas, em wikis internos; torna rotação e auditoria inviáveis
- **fail-fast** — padrão de design em que um sistema detecta condições inválidas o mais cedo possível e falha imediatamente com mensagem de erro clara, em vez de continuar em estado degradado e falhar de forma críptica mais tarde; em segredos, manifesta-se como validação Zod de `process.env` no startup da aplicação
- **Application Default Credentials (ADC)** — mecanismo do Google Cloud (e análogos da AWS como Instance Metadata Service) pelo qual o SDK autentica automaticamente usando a identidade da instância de compute — IAM Role ou Workload Identity — sem necessidade de service account keys em disco

## Veja também

- [[03-Dominios/Node/Segurança/index|Segurança]] — MOC do galho 8; visão completa da trilha de segurança Node.js
- [[JavaScript/Backend/Node.js|Node.js]] — tronco da trilha Node Senior; fundamentos de Node.js
- [[03-Dominios/Node/Segurança/01 - Supply chain attacks e npm audit|Supply chain attacks e npm audit]] — galho 8, nota 1; vetores de comprometimento via dependências npm
- [[03-Dominios/Node/Segurança/03 - Validação de entrada com Zod e Joi|Validação de entrada com Zod e Joi]] — galho 8, nota 3; validação de schemas com Zod aplicada a inputs externos
- [AWS Secrets Manager — documentação oficial](https://docs.aws.amazon.com/secretsmanager/latest/userguide/intro.html)
- [HashiCorp Vault — documentação KV v2](https://developer.hashicorp.com/vault/docs/secrets/kv/kv-v2)
- [Doppler — integração Node.js](https://docs.doppler.com/docs/node-js)
- [12-Factor App — Config (fator III)](https://12factor.net/config)
