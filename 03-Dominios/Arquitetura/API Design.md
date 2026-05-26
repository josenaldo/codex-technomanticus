---
title: "API Design"
created: 2026-04-01
updated: 2026-04-10
type: concept
status: evergreen
tags:
  - arquitetura
  - entrevista
publish: false
---

# API Design

A arte de projetar interfaces de comunicação entre sistemas que sejam **intuitivas para o consumidor**, **consistentes**, **seguras** e **evoluíveis sem quebrar clientes existentes**. Enquanto [[Redes e Protocolos]] cobre o "como" da comunicação (HTTP, TCP, TLS) e [[System Design]] cobre o "quanto" (escala, cache, rate limiting em alto nível), esta nota foca no **contrato**: o que sua API promete, como ela responde, e como ela evolui.

## O que é

API Design é o processo de definir o contrato entre producer e consumer: endpoints, formatos de payload, códigos de erro, autenticação, versionamento. O código é implementação — o contrato é o que importa para quem consome.

O que diferencia um senior em API design:

1. **Consistência** — uma API bem projetada é previsível. Se `/patients` usa kebab-case, `/medical-records` também usa. Se `POST /patients` retorna 201 + Location, `POST /appointments` faz o mesmo.
2. **Design para o consumidor** — APIs boas são projetadas do ponto de vista de quem vai usá-las, não da estrutura do banco.
3. **Evolução sem quebrar** — backward compatibility é uma decisão, não um acidente. Adicionar é seguro; remover/renomear nunca é.
4. **Erros úteis** — um erro 400 com `{"error": "invalid"}` é inútil. Um erro com tipo, título, detalhe e ponteiro para o campo inválido economiza horas de debugging.
5. **Documentação como contrato** — OpenAPI, não um README desatualizado.
6. **Segurança pensada desde o dia 1** — auth, rate limiting, input validation, não como add-on depois.

---

## Filosofia: desenhe para o consumidor

A melhor API é aquela que deixa o desenvolvedor que a consome produtivo em 15 minutos sem precisar ler documentação extensa.

**Princípios:**

- **Princípio do menor espanto** — endpoints devem fazer o que o nome sugere. `DELETE /users/42` não pode retornar `200 OK` e não deletar nada.
- **Consistência > novidade** — use convenções estabelecidas. Não invente formato próprio de paginação.
- **Cada endpoint tem um propósito claro** — se você está descrevendo um endpoint e usando "e" demais, provavelmente são dois endpoints.
- **Esconda detalhes de implementação** — se sua API reflete exatamente o schema do banco, você está acoplando o consumidor à sua persistência.
- **Facilite o caminho feliz, permita o caminho alternativo** — o uso comum deve ser simples; casos avançados precisam ser possíveis.

---

## REST: modelagem de recursos

REST não é sobre usar HTTP — é sobre **modelar seu domínio como recursos** e usar HTTP de forma consistente para operá-los.

### Recursos são substantivos

```
✅ GET  /patients/123
✅ POST /patients
✅ GET  /patients/123/appointments
✅ POST /patients/123/appointments

❌ GET  /getPatient?id=123
❌ POST /createPatient
❌ GET  /patientAppointments?patientId=123
```

**Regras práticas:**

- Use plural consistentemente (`/patients`, não `/patient`)
- kebab-case em paths (`/medical-records`, não `/medicalRecords`)
- camelCase em JSON payloads (`{"firstName": "..."}`) — é convenção JS, e a maioria dos consumers são JS
- snake_case se sua stack/empresa usa (GitHub API usa — consistência importa mais que convenção)

### Relacionamentos: nested vs flat

**Nested** — quando o sub-recurso só faz sentido no contexto do pai:

```
GET  /patients/123/appointments        ← lista consultas do paciente 123
POST /patients/123/appointments        ← cria consulta para o paciente 123
GET  /patients/123/appointments/456    ← consulta 456 do paciente 123
```

**Flat com query parameter** — quando o recurso tem identidade própria:

```
GET  /appointments?patient_id=123      ← lista, filtrada por paciente
POST /appointments                      ← cria (paciente vai no body)
GET  /appointments/456                  ← acesso direto por ID
```

**Regra prática:** no máximo 1 nível de nesting. `/patients/123/appointments/456/notes/789` vira bagunça. Use flat a partir do 2º nível.

### Ações que não encaixam em CRUD

Nem tudo é CRUD. Como modelar "aprovar um pedido" ou "reenviar um email"?

**Opção 1 — sub-resource action (mais pragmática):**

```
POST /orders/123/approve
POST /emails/456/resend
POST /appointments/789/cancel
```

Não é REST puro, mas é claro, idiomático e amplamente aceito (GitHub API faz isso).

**Opção 2 — PATCH com state change:**

```
PATCH /orders/123
{ "status": "approved" }
```

Problema: se cancelar, aprovar e reembolsar forem ações diferentes com regras/efeitos colaterais diferentes, esse PATCH esconde a intenção.

**Opção 3 — recurso de comando:**

```
POST /order-approvals
{ "order_id": 123, "approver_id": 42 }
```

Mais RESTful puro, mas mais verboso. Útil se a aprovação tem seu próprio ciclo de vida.

### Verbos HTTP em detalhe

| Verbo | Uso | Idempotente | Safe | Body req | Body resp | Status comum |
| --- | --- | --- | --- | --- | --- | --- |
| GET | Buscar | sim | sim | não | sim | 200, 404 |
| POST | Criar, ações | não | não | sim | sim/não | 201, 200, 204, 202 |
| PUT | Substituir (replace) | sim | não | sim (completo) | sim/não | 200, 204 |
| PATCH | Atualizar parcial | não* | não | sim (diff) | sim/não | 200, 204 |
| DELETE | Remover | sim | não | não | não | 204, 200 |
| HEAD | Metadados | sim | sim | não | não | 200, 404 |
| OPTIONS | Capabilities, CORS | sim | sim | não | sim | 200, 204 |

\* PATCH pode ser idempotente dependendo da implementação (ver discussão mais abaixo).

**PUT vs PATCH — a distinção que importa:**

```http
# PUT — substitui o recurso inteiro
PUT /patients/123
{ "name": "Maria", "email": "maria@example.com", "phone": "+5511..." }

# Se você PUT sem o phone, o phone é apagado!

# PATCH — modifica apenas os campos enviados
PATCH /patients/123
{ "email": "novo@example.com" }

# O phone e o name ficam intactos.
```

Na prática, muita gente usa POST para updates parciais (menos correto) ou PATCH sempre (pragmático). O importante é **consistência dentro da sua API**.

**PATCH: JSON Merge Patch vs JSON Patch:**

```http
# JSON Merge Patch (RFC 7396) — simples, o mais usado
PATCH /patients/123
Content-Type: application/merge-patch+json
{ "email": "novo@example.com", "phone": null }
# (null = remover o campo)

# JSON Patch (RFC 6902) — operações explícitas, para casos avançados
PATCH /patients/123
Content-Type: application/json-patch+json
[
  { "op": "replace", "path": "/email", "value": "novo@example.com" },
  { "op": "add", "path": "/tags/-", "value": "vip" },
  { "op": "remove", "path": "/phone" }
]
```

**Default:** JSON Merge Patch. Só use JSON Patch se você precisa das operações avançadas (add a array, test, move).

---

## Status codes: use com significado

Status codes são parte do contrato. Um 200 com `{"success": false}` no body é uma má prática clássica que confunde monitoring, retries, e caches.

### 2xx — Sucesso

| Código | Quando usar |
| --- | --- |
| **200 OK** | GET com dados, PUT/PATCH/POST com response body |
| **201 Created** | POST que criou um novo recurso. **Inclua `Location` header** apontando para o novo recurso |
| **202 Accepted** | Requisição aceita mas não completa (processamento assíncrono). Retorne job ID ou URL de status |
| **204 No Content** | DELETE bem sucedido, ou update sem response body |

```http
POST /patients
{ "name": "Maria", "email": "maria@example.com" }

HTTP/1.1 201 Created
Location: /patients/123
Content-Type: application/json
{ "id": 123, "name": "Maria", "email": "maria@example.com", "created_at": "..." }
```

### 3xx — Redirecionamento

Raramente usado em APIs JSON. Aparece em redirects HTTP gerais e em APIs com ETags (304 Not Modified).

### 4xx — Erro do cliente

| Código | Quando usar | Confusão comum |
| --- | --- | --- |
| **400 Bad Request** | Payload malformado (JSON inválido, tipo errado) | Usar para erro de validação → use 422 |
| **401 Unauthorized** | Falta autenticação ou credenciais inválidas | Na verdade significa "unauthenticated" |
| **403 Forbidden** | Autenticado, mas sem permissão | Quando mostrar 403 vs 404 (leak de existência) |
| **404 Not Found** | Recurso não existe | Usar para endpoint inexistente vs recurso inexistente |
| **405 Method Not Allowed** | Verbo HTTP errado no endpoint | Inclua `Allow` header |
| **409 Conflict** | Estado atual do recurso impede a operação | Ex.: tentar criar user com email já usado |
| **410 Gone** | Recurso existia mas foi removido permanentemente | Diferente de 404 — 410 é intencional |
| **415 Unsupported Media Type** | `Content-Type` não suportado | |
| **422 Unprocessable Entity** | Payload válido sintaticamente, mas inválido semanticamente | Erro de validação de campos |
| **429 Too Many Requests** | Rate limit excedido | Inclua `Retry-After` header |

**401 vs 403 — a distinção:**

- **401** — "Eu não sei quem você é" (autenticação). Peça para o cliente fazer login/enviar token.
- **403** — "Eu sei quem você é, mas você não pode fazer isso" (autorização).

**404 vs 403 — security through obscurity:**

Se um user tenta acessar `/admin/users/42` e não tem permissão, retornar 403 vaza a informação de que o endpoint existe. Algumas APIs retornam 404 para esconder, outras retornam 403 explícito. Depende do modelo de ameaça.

### 5xx — Erro do servidor

| Código | Quando usar |
| --- | --- |
| **500 Internal Server Error** | Erro não tratado (bug). Nunca exponha stack trace |
| **502 Bad Gateway** | Proxy/gateway recebeu resposta inválida do upstream |
| **503 Service Unavailable** | Indisponível temporariamente (manutenção, sobrecarga). Inclua `Retry-After` |
| **504 Gateway Timeout** | Upstream não respondeu a tempo |

**Regra de ouro:** 5xx significa "é nosso problema, tente de novo depois". 4xx significa "é seu problema, conserte antes de tentar de novo". Isso é importante para clients decidirem se vão fazer retry automático.

---

## Tratamento de erros: RFC 9457 Problem Details

A maneira mais difundida de padronizar erros em APIs HTTP. Substitui a antiga RFC 7807.

```json
HTTP/1.1 422 Unprocessable Entity
Content-Type: application/problem+json

{
  "type": "https://api.medespecialista.com/errors/validation",
  "title": "Validation Error",
  "status": 422,
  "detail": "The request contains invalid fields",
  "instance": "/api/patients",
  "errors": [
    {
      "field": "email",
      "code": "invalid_format",
      "message": "Email must be a valid email address"
    },
    {
      "field": "birth_date",
      "code": "in_future",
      "message": "Birth date cannot be in the future"
    }
  ],
  "trace_id": "abc-123-def-456"
}
```

**Campos obrigatórios (RFC 9457):**

- `type` — URI identificando o tipo do erro. Clientes podem fazer match nisso para decidir comportamento.
- `title` — resumo curto, legível, **não varia** para o mesmo tipo.
- `status` — mesmo valor do HTTP status.

**Campos opcionais e customizados:**

- `detail` — explicação específica desta ocorrência, pode variar.
- `instance` — URI da ocorrência específica.
- Extensões customizadas como `errors`, `trace_id`, etc.

**Boas práticas:**

1. **Use Content-Type `application/problem+json`** — sinaliza claramente que é um problem detail.
2. **Inclua trace ID** — para o cliente reportar ao seu suporte, você encontra o request nos logs.
3. **Não vaze informação interna** — não retorne stack trace, query SQL, ou nomes de tabelas.
4. **Mensagens actionable** — "email inválido" não ajuda. "Email deve ter formato `user@domain.tld`" ajuda.
5. **Consistência** — todos os erros da API seguem o mesmo formato.

**Implementação Spring Boot (Spring 6+):**

```java
@RestControllerAdvice
public class GlobalExceptionHandler extends ResponseEntityExceptionHandler {

    @ExceptionHandler(ResourceNotFoundException.class)
    public ProblemDetail handleNotFound(ResourceNotFoundException ex) {
        ProblemDetail problem = ProblemDetail.forStatusAndDetail(
            HttpStatus.NOT_FOUND, ex.getMessage());
        problem.setType(URI.create("https://api.example.com/errors/not-found"));
        problem.setTitle("Resource Not Found");
        problem.setProperty("trace_id", MDC.get("traceId"));
        return problem;
    }

    @Override
    protected ResponseEntity<Object> handleMethodArgumentNotValid(
            MethodArgumentNotValidException ex, ...) {
        List<Map<String, String>> errors = ex.getBindingResult()
            .getFieldErrors().stream()
            .map(err -> Map.of(
                "field", err.getField(),
                "code", Objects.requireNonNull(err.getCode()),
                "message", Objects.requireNonNull(err.getDefaultMessage())
            )).toList();

        ProblemDetail problem = ProblemDetail.forStatusAndDetail(
            HttpStatus.UNPROCESSABLE_ENTITY, "Validation failed");
        problem.setProperty("errors", errors);
        return ResponseEntity.unprocessableEntity().body(problem);
    }
}
```

---

## Paginação

Nunca retorne coleções sem paginação. Duas abordagens principais:

### Offset-based (skip/limit)

```
GET /patients?page=2&size=20
GET /patients?offset=40&limit=20

Response:
{
  "data": [...],
  "pagination": {
    "page": 2,
    "size": 20,
    "total_items": 1523,
    "total_pages": 77
  },
  "links": {
    "first": "/patients?page=1&size=20",
    "prev": "/patients?page=1&size=20",
    "next": "/patients?page=3&size=20",
    "last": "/patients?page=77&size=20"
  }
}
```

**Prós:** simples, permite pular para página específica, inclui total.

**Contras:**

- Performance degrada com offset grande (`OFFSET 10000` faz o DB ler e descartar 10000 rows)
- Dados inseridos/removidos entre requests causam duplicação ou skip ("page drift")
- `COUNT(*)` para total pode ser caro em tabelas grandes

**Quando usar:** datasets pequenos/médios, interfaces com "pular para página X", dados que mudam pouco.

### Cursor-based (keyset)

```
GET /patients?limit=20&after=eyJpZCI6MTIzLCJjcmVhdGVkIjoiMjAyNi0wNC0wMSJ9

Response:
{
  "data": [...],
  "pagination": {
    "has_more": true,
    "next_cursor": "eyJpZCI6MTQzLCJjcmVhdGVkIjoiMjAyNi0wNC0wMiJ9"
  }
}
```

O cursor é tipicamente base64 do último registro da página anterior (ex.: `{id: 143, created: "..."}`).

**Prós:**

- Performance constante mesmo em datasets enormes (usa índice para buscar a partir do cursor)
- Sem "page drift" — novos itens não afetam páginas já visitadas
- Ideal para scroll infinito

**Contras:**

- Não dá para pular direto para página N
- Cursor é opaco (cliente não pode manipular)
- Implementação mais complexa

**Quando usar:** feeds, timelines, logs, datasets grandes, dados em mudança constante.

### Implementação de cursor (SQL)

```sql
-- Primeira página
SELECT * FROM patients
WHERE active = true
ORDER BY created_at DESC, id DESC
LIMIT 20;

-- Páginas seguintes (cursor = último created_at + id da página anterior)
SELECT * FROM patients
WHERE active = true
  AND (created_at, id) < ('2026-04-01 10:00:00', 143)
ORDER BY created_at DESC, id DESC
LIMIT 20;
```

A comparação composta `(created_at, id) <` usa o índice composto e é O(log n), independentemente da profundidade.

---

## Filtering, sorting, searching

### Filtros simples (query params)

```
GET /patients?status=active&specialty=cardio&age_min=18&age_max=65
```

**Convenções:**

- Filtro exato: `?status=active`
- Ranges: `?age_min=18&age_max=65` ou `?age[gte]=18&age[lte]=65`
- Múltiplos valores: `?specialty=cardio,dermato` ou `?specialty=cardio&specialty=dermato`
- Negação: `?status_not=cancelled` (pouco padronizado)

### Filtros complexos: RSQL/FIQL ou query DSL

Para filtros muito dinâmicos, considere uma mini linguagem:

```
GET /patients?filter=status==active;age=ge=18;specialty=in=(cardio,dermato)
```

Ou uma abordagem tipo GraphQL com operadores:

```json
POST /patients/search
{
  "filter": {
    "and": [
      { "status": { "eq": "active" } },
      { "age": { "gte": 18 } },
      { "specialty": { "in": ["cardio", "dermato"] } }
    ]
  },
  "sort": [{ "created_at": "desc" }],
  "limit": 20
}
```

**Regra prática:** comece com query params simples. Migre para DSL só quando clientes pedirem consistentemente por filtros complexos.

### Sorting

```
GET /patients?sort=name,asc
GET /patients?sort=-created_at,name   ← prefixo "-" = desc
GET /patients?sort=created_at:desc,name:asc
```

Escolha **uma** convenção e seja consistente.

### Search (full-text)

```
GET /patients?q=maria+silva
GET /patients/search?q=maria
```

Para busca séria, use um motor dedicado (Elasticsearch, PostgreSQL `tsvector`). Não use `LIKE '%query%'` em produção com volume.

---

## Versionamento

Toda API publicada precisa de uma estratégia de versionamento explícita. Escolher "vamos ver depois" significa quebrar consumers sem aviso.

### URL path versioning (mais comum)

```
GET /api/v1/patients
GET /api/v2/patients
```

**Prós:** explícito, visível em logs, fácil de rotear, funciona com cache HTTP e CDN.

**Contras:** "impuro" do ponto de vista REST (o recurso é o mesmo, só muda a representação).

**Quando usar:** APIs públicas, quando clareza importa mais que pureza. Esta é a escolha default para a maioria das APIs modernas (Stripe, GitHub, Twitter).

### Header versioning

```
GET /api/patients
Accept: application/vnd.medespecialista.v2+json
```

**Prós:** mais "correto" conceitualmente — a URL identifica o recurso, o header negocia a representação.

**Contras:** menos visível, difícil de testar via browser ou curl direto, cache HTTP precisa usar `Vary: Accept`.

**Quando usar:** APIs internas entre times com tooling consistente, quando você quer esconder versionamento dos consumers.

### Query parameter

```
GET /api/patients?version=2
```

**Prós:** simples de testar.

**Contras:** mistura versão com filtros, pode ser ignorado por caches.

**Quando usar:** raramente. É a opção menos recomendada.

### Estratégias de evolução

A **melhor estratégia é não precisar de versão nova**. Para isso, projete para evolução:

1. **Adicionar campos é seguro** — consumers ignoram campos desconhecidos.
2. **Remover ou renomear campos nunca é seguro** — é uma breaking change.
3. **Nunca mude o tipo de um campo existente** — se `age` era number, não vire string.
4. **Enum values: adicione com cuidado** — consumers podem fazer `switch` e explodir em valor novo. Documente como lidar com unknown.
5. **Default values: nunca mude** — clientes confiam no comportamento atual.
6. **Deprecation antes de remoção** — marque o campo como deprecated, espere meses, só aí remova em uma nova versão.

**Quando você precisa de breaking change:**

1. Release `v2` em paralelo com `v1`
2. Comunique deprecation de `v1` com prazo (ex.: 12 meses)
3. Monitore uso de `v1` por client (via API key)
4. Avise clients que ainda usam `v1` individualmente
5. Desligue `v1` só depois de confirmar que ninguém relevante usa

**Header de deprecation (RFC 8594):**

```http
HTTP/1.1 200 OK
Deprecation: Sun, 11 Nov 2026 23:59:59 GMT
Sunset: Sun, 11 May 2027 23:59:59 GMT
Link: <https://api.example.com/v2/patients>; rel="successor-version"
```

---

## Autenticação e autorização

### Métodos comuns

| Método | Como | Quando usar |
| --- | --- | --- |
| **Basic Auth** | `Authorization: Basic <base64(user:pass)>` | Nunca em produção sem HTTPS; uso interno muito simples |
| **API Key** | Header customizado ou `Authorization: ApiKey ...` | APIs server-to-server, integrações B2B |
| **Bearer Token (opaque)** | `Authorization: Bearer <token>` — token armazenado server-side | Sessões server-side |
| **JWT** | `Authorization: Bearer <jwt>` — token self-contained | APIs stateless, microserviços |
| **OAuth 2.0** | Fluxos para delegação (authorization code, client credentials) | Acesso delegado, login via Google/GitHub |
| **OIDC** | OAuth 2.0 + camada de identidade (ID tokens) | SSO, login social |
| **mTLS** | Certificados mútuos em TLS | Comunicação entre microserviços, zero trust |

### JWT: prós e contras

**Prós:**

- Self-contained — servidor valida sem consultar banco
- Funciona em sistemas distribuídos sem sessão compartilhada
- Payload carrega claims (user ID, roles, tenant) assinados

**Contras:**

- **Revogação é difícil** — JWT válido por design até expirar. Para revogação imediata, precisa de blacklist (adeus stateless).
- **Não coloque dados sensíveis no payload** — é só base64, não encriptação.
- **Tamanho** — JWTs ficam maiores que session IDs, pagando em cada request.
- **Algoritmos inseguros** — `alg: none` e confusão HS256/RS256 são vetores clássicos de ataque.

**Boas práticas JWT:**

- Expiração curta (15 min - 1h) + refresh token de longo prazo
- Armazene refresh token server-side para permitir revogação
- Use RS256 ou ES256 (assimétrico) em sistemas multi-serviço
- Valide `iss`, `aud`, `exp`, `nbf` em toda verificação
- Nunca confie em `alg` do header do token ao validar

### API Key best practices

- Transmitir via header, nunca em query string (vaza em logs)
- Use um prefixo identificável (`sk_live_...`, `pk_test_...`) — facilita detecção se vazar
- Keys são bearer tokens — revogue imediatamente se suspeitar de comprometimento
- Hash no banco (armazene `sha256(key)`, não a key)
- Rotate periodicamente, suporte múltiplas keys ativas por cliente
- Rate limit por key

### Authorization (após autenticação)

- **RBAC** (Role-Based Access Control) — users têm roles, roles têm permissões. Simples, funciona para a maioria.
- **ABAC** (Attribute-Based Access Control) — decisão baseada em atributos (user, recurso, contexto). Mais flexível, mais complexo.
- **ReBAC** (Relationship-Based) — Google Zanzibar style. Ideal para sistemas tipo Google Drive ("alice shared with bob").

```java
// Spring Security RBAC
@PreAuthorize("hasRole('ADMIN')")
@DeleteMapping("/patients/{id}")
public void delete(@PathVariable Long id) { ... }

// ABAC — regra mais rica
@PreAuthorize("@authService.canEditPatient(authentication, #id)")
@PutMapping("/patients/{id}")
public void update(@PathVariable Long id, ...) { ... }
```

---

## Idempotência

Operações idempotentes: executar N vezes produz o mesmo resultado que executar 1 vez. Crítico para confiabilidade.

**GET, PUT, DELETE são idempotentes por definição (no REST).** **POST não é** — criar 2 vezes cria 2 recursos. O problema: retries de network fazem POSTs duplicados.

### Idempotency Key pattern (Stripe style)

Cliente envia header `Idempotency-Key` com valor único (UUID) em requests POST. Servidor:

1. Verifica se já processou essa key → se sim, retorna o mesmo resultado (sem re-executar)
2. Se não, processa normalmente e armazena `(key → response)` com TTL (24h típico)

```http
POST /payments
Idempotency-Key: 550e8400-e29b-41d4-a716-446655440000
{ "amount": 100, "currency": "BRL", "card_token": "tok_..." }
```

**Implementação:**

```java
@PostMapping("/payments")
public ResponseEntity<Payment> createPayment(
        @RequestHeader("Idempotency-Key") String idempotencyKey,
        @RequestBody PaymentRequest req) {

    // Tenta recuperar resposta cacheada
    var cached = idempotencyStore.get(idempotencyKey);
    if (cached != null) {
        if (!cached.request().equals(req)) {
            // Mesma key, request diferente → erro
            return ResponseEntity.status(422).body(...);  // "key reused with different request"
        }
        return ResponseEntity.status(cached.status()).body(cached.response());
    }

    // Processa e armazena (atomicamente com a operação!)
    Payment payment = paymentService.process(req);
    idempotencyStore.put(idempotencyKey, req, 201, payment, Duration.ofHours(24));
    return ResponseEntity.status(201).body(payment);
}
```

**Detalhes críticos:**

- Armazene atomicamente com a operação (mesmo DB transaction) — se não, race condition pode criar 2 pagamentos
- Cache respostas de erro também (incluindo 500), senão client retry cria o recurso 2x
- TTL curto o suficiente para não crescer sem limite, longo o suficiente para cobrir retries (Stripe usa 24h)
- Valide que o request é idêntico em retries com mesma key

---

## Rate limiting em APIs

Detalhes de implementação e algoritmos estão em [[System Design]]. Aqui foco no **contrato** que a API expõe.

### Headers de resposta

```http
HTTP/1.1 200 OK
X-RateLimit-Limit: 1000
X-RateLimit-Remaining: 847
X-RateLimit-Reset: 1712750400
```

Ou o padrão IETF (RFC 9331 draft):

```http
RateLimit-Limit: 1000
RateLimit-Remaining: 847
RateLimit-Reset: 37
RateLimit-Policy: 1000;w=3600
```

### 429 Too Many Requests

```http
HTTP/1.1 429 Too Many Requests
Retry-After: 60
Content-Type: application/problem+json

{
  "type": "https://api.example.com/errors/rate-limit",
  "title": "Rate Limit Exceeded",
  "status": 429,
  "detail": "You have exceeded the rate limit of 1000 requests per hour",
  "retry_after_seconds": 60
}
```

**Boas práticas:**

- Sempre inclua `Retry-After` (em segundos ou como data HTTP)
- Informe o limit no response, não só quando excedido
- Diferentes tiers/endpoints podem ter limites diferentes — documente
- Clients devem implementar exponential backoff quando receberem 429

---

## Caching HTTP

APIs que ignoram caching HTTP desperdiçam uma das maiores ferramentas de performance da web.

### Cache-Control

```http
# Não cachear
Cache-Control: no-store

# Validar com servidor em toda request (mas pode cachear em 304)
Cache-Control: no-cache

# Cachear por 5 minutos publicamente (CDN)
Cache-Control: public, max-age=300

# Cachear só no browser, não em proxies
Cache-Control: private, max-age=300

# Stale-while-revalidate
Cache-Control: max-age=60, stale-while-revalidate=300
```

### ETag e conditional requests

```http
# Primeira request
GET /patients/123
HTTP/1.1 200 OK
ETag: "a1b2c3d4"
{ "id": 123, "name": "Maria", ... }

# Request seguinte
GET /patients/123
If-None-Match: "a1b2c3d4"

# Se não mudou
HTTP/1.1 304 Not Modified
# (sem body — cliente usa versão cacheada)

# Se mudou
HTTP/1.1 200 OK
ETag: "e5f6g7h8"
{ "id": 123, "name": "Maria Silva", ... }
```

**ETag é tipicamente:** hash do body, ou `version` do recurso, ou `updated_at` formatado.

### Optimistic locking com If-Match

Evita lost updates — usuário A edita, usuário B edita, B sobrescreve A sem saber.

```http
PUT /patients/123
If-Match: "a1b2c3d4"
{ "name": "Novo Nome", ... }

# Se ETag atual bate
HTTP/1.1 200 OK

# Se alguém editou entre o GET e o PUT
HTTP/1.1 412 Precondition Failed
```

---

## Bulk operations

Em vez de N requests, uma request processa múltiplos itens.

### Bulk create/update

```http
POST /patients/bulk
{
  "operations": [
    { "action": "create", "data": { "name": "Alice" } },
    { "action": "create", "data": { "name": "Bob" } },
    { "action": "update", "id": 42, "data": { "email": "..." } }
  ]
}

Response: 207 Multi-Status
{
  "results": [
    { "status": 201, "id": 100 },
    { "status": 422, "error": { "field": "name", ... } },
    { "status": 200, "id": 42 }
  ]
}
```

**Considerações:**

- **Transação?** Tudo ou nada (all-or-nothing), ou parcial (best-effort)? Documente.
- **Limite de tamanho** — não aceite 10 milhões de items em uma request.
- **Performance** — bulk deve ser mais rápido que N individuais, senão não vale a complexidade.
- **Status code 207** — indica resposta mista (alguns sucessos, alguns erros).

---

## File upload

### Multipart form data (simples)

```http
POST /documents
Content-Type: multipart/form-data; boundary=...

--boundary
Content-Disposition: form-data; name="metadata"
Content-Type: application/json

{ "title": "Exame médico" }
--boundary
Content-Disposition: form-data; name="file"; filename="exame.pdf"
Content-Type: application/pdf

<binary content>
--boundary--
```

**Limites:** OK para arquivos pequenos (< 10MB). Tem overhead de base64 se enviado como JSON.

### Presigned URLs (arquivos grandes)

Cliente sobe direto pro storage (S3), sem passar pela sua API.

```
Passo 1: Cliente pede URL de upload
  POST /documents/upload-url
  { "filename": "video.mp4", "content_type": "video/mp4", "size": 500000000 }

  Response:
  {
    "upload_url": "https://bucket.s3.amazonaws.com/...?X-Amz-Signature=...",
    "document_id": "doc-123",
    "expires_at": "..."
  }

Passo 2: Cliente faz PUT direto no S3
  PUT <upload_url>
  (corpo = arquivo binário)

Passo 3: Cliente confirma
  POST /documents/doc-123/confirm
```

**Prós:** sua API não carrega o arquivo na memória, escala sem limite, mais rápido.

**Contras:** mais complexo, cliente precisa entender o fluxo.

### Chunked/resumable upload

Para uploads enormes com recuperação de falha: cliente envia em pedaços, servidor junta. S3 Multipart Upload, Google Resumable Upload, tus.io protocol.

---

## Operações de longa duração (async)

O que fazer quando uma operação leva mais que alguns segundos? Não segure o HTTP request.

### Pattern: 202 Accepted + polling

```
Cliente: POST /exports
Servidor: 202 Accepted
          Location: /jobs/abc-123
          { "job_id": "abc-123", "status": "pending" }

Cliente: GET /jobs/abc-123  (poll periodicamente)
Servidor: { "status": "running", "progress": 45 }
          ...
          { "status": "completed", "result_url": "/exports/download/abc-123" }

Cliente: GET /exports/download/abc-123
```

### Pattern: webhooks (callbacks)

Cliente registra um URL de callback. Quando a operação termina, você faz POST nesse URL.

```
POST /exports
{ "callback_url": "https://client.com/webhook/exports" }

Response: 202 Accepted
{ "job_id": "abc-123" }

[... tempo depois ...]

Servidor → Cliente:
POST https://client.com/webhook/exports
X-Webhook-Signature: sha256=...
{ "job_id": "abc-123", "status": "completed", "result_url": "..." }
```

→ Ver seção de Webhooks abaixo.

### Pattern: Server-Sent Events / WebSocket

Para updates em tempo real (progresso de upload, notificações).

→ Ver [[Redes e Protocolos]] para detalhes de SSE vs WebSocket.

---

## Webhooks

Sua API dispara eventos para URLs que clientes registram. É o inverso de uma API normal — você é o cliente agora.

### Design

```http
POST https://customer.com/webhooks/orders
Content-Type: application/json
X-Webhook-Event: order.completed
X-Webhook-Id: wh-evt-abc123
X-Webhook-Signature: sha256=3d5e...
X-Webhook-Timestamp: 1712750400

{
  "id": "wh-evt-abc123",
  "type": "order.completed",
  "created_at": "2026-04-10T12:00:00Z",
  "data": {
    "order_id": "ord-42",
    "amount": 1500,
    "currency": "BRL"
  }
}
```

### Segurança

**1. Assinatura HMAC:**

```
signature = HMAC-SHA256(webhook_secret, timestamp + "." + body)
```

O cliente verifica a assinatura usando o secret compartilhado. Isso garante autenticidade (veio de você) e integridade (não foi alterado).

**2. Timestamp validation:**

Inclua timestamp na assinatura e rejeite webhooks antigos (> 5 min) — previne replay attack.

**3. HTTPS obrigatório** — webhooks transportam dados sensíveis.

### Confiabilidade

Webhooks vão falhar. Design para isso:

- **Retries com backoff exponencial** — 5s, 30s, 2min, 10min, 1h, 6h, 24h (Stripe usa isso)
- **Deduplicate no cliente** — use `X-Webhook-Id` como idempotency key
- **Dead letter** — após N tentativas falhadas, marque como failed e alerte
- **Dashboard de replays** — permita cliente re-enviar eventos manualmente para debug

### Eventos: design

- **Naming:** `resource.action` (`order.created`, `payment.failed`, `user.updated`)
- **Imutabilidade:** eventos são fatos que aconteceram. Não edite eventos publicados.
- **Versionamento:** `order.created.v2` para evolução de schema.
- **Order não garantida:** cliente deve tolerar receber eventos fora de ordem.

---

## REST vs GraphQL vs gRPC: decisão

Resumo das 3 principais abordagens. Detalhes em [[Redes e Protocolos]].

### Quando escolher REST

- APIs **públicas**, consumidas por múltiplos clientes desconhecidos
- CRUD bem mapeado para recursos
- Precisa de cache HTTP nativo, CDN, tooling amplo
- Default razoável quando não há razão forte para outra coisa

### Quando escolher GraphQL

- **Clientes diferentes precisam de dados diferentes** (mobile economiza bytes, web quer tudo, admin quer relações profundas)
- **Evita múltiplas requests** — uma query pega tudo que a tela precisa
- **Schema fortemente tipado** importa (auto-documentação, code generation)

**Cuidados:**

- **N+1** é o problema número 1 — use DataLoader pattern
- **Rate limiting** é complexo (uma query pode ser arbitrariamente cara) — use query complexity analysis ou custo por campo
- **Caching** HTTP não funciona naturalmente (tudo é POST em `/graphql`). Precisa de cache em nível de resolver ou extensões como persisted queries
- **Não é bala de prata** — para CRUD simples, REST é mais simples

### Quando escolher gRPC

- **Comunicação interna** entre microserviços onde latência e throughput importam
- **Contrato forte** via `.proto` com code generation em qualquer linguagem
- **Streaming** (uni ou bidirecional)
- HTTP/2 multiplexing

**Cuidados:**

- Não funciona nativamente em browsers (precisa de gRPC-Web proxy)
- Debugging binário é mais chato que JSON
- Menos ferramentas/tooling para APIs públicas

### Híbrido

APIs modernas frequentemente misturam:

- **REST + OpenAPI** na borda (para clients externos, mobile, web)
- **gRPC** entre serviços internos
- **GraphQL** em camada BFF (Backend for Frontend) agregando múltiplos serviços internos

---

## Documentação: OpenAPI

A documentação é parte do contrato. Se não está documentado, não faz parte da API (do ponto de vista do consumer).

### OpenAPI (antigo Swagger)

Padrão de facto para documentar APIs REST. Gera clients, servers, docs interativos, mocks.

```yaml
# openapi.yaml
openapi: 3.1.0
info:
  title: MedEspecialista API
  version: 2.0.0
  description: API para gestão de consultas médicas

servers:
  - url: https://api.medespecialista.com/v2

paths:
  /patients/{id}:
    get:
      summary: Get patient by ID
      parameters:
        - name: id
          in: path
          required: true
          schema:
            type: integer
      responses:
        '200':
          description: Patient found
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/Patient'
        '404':
          $ref: '#/components/responses/NotFound'

components:
  schemas:
    Patient:
      type: object
      required: [id, name, email]
      properties:
        id: { type: integer }
        name: { type: string, example: "Maria Silva" }
        email: { type: string, format: email }
        birth_date: { type: string, format: date }
```

### Geração automática no Spring Boot

```java
// build.gradle
implementation 'org.springdoc:springdoc-openapi-starter-webmvc-ui:2.3.0'

// Controller com anotações
@RestController
@RequestMapping("/patients")
@Tag(name = "Patients", description = "Patient management")
public class PatientController {

    @GetMapping("/{id}")
    @Operation(summary = "Get patient by ID")
    @ApiResponses({
        @ApiResponse(responseCode = "200", description = "Patient found"),
        @ApiResponse(responseCode = "404", description = "Not found")
    })
    public Patient findById(@PathVariable Long id) { ... }
}
```

Gera Swagger UI automaticamente em `/swagger-ui.html`.

### Design-first vs Code-first

- **Design-first** — escreva o OpenAPI primeiro, gere o código a partir dele. Força pensar no contrato antes, melhor para APIs públicas.
- **Code-first** — escreva o código com anotações, OpenAPI é gerado. Mais rápido, mas o OpenAPI é resultado, não intenção.

### Contract testing

Garante que a implementação conforma ao contrato documentado:

- **Pact** — consumer-driven contract testing
- **Prism** — mock server a partir do OpenAPI
- **Dredd** — testa a API contra o OpenAPI

---

## Testes de API

### Pirâmide de testes

1. **Unit tests** — lógica isolada (services, validators)
2. **Integration tests** — controller + service + DB (Testcontainers)
3. **Contract tests** — contrato entre serviços (Pact)
4. **End-to-end tests** — fluxos completos (poucos, caros)

### Exemplo Spring Boot

```java
@SpringBootTest
@AutoConfigureMockMvc
@Testcontainers
class PatientControllerIT {

    @Container
    static PostgreSQLContainer<?> postgres = new PostgreSQLContainer<>("postgres:16");

    @Autowired MockMvc mvc;

    @Test
    void shouldReturn422WhenEmailIsInvalid() throws Exception {
        mvc.perform(post("/patients")
                .contentType(APPLICATION_JSON)
                .content("""
                    { "name": "Maria", "email": "not-an-email" }
                    """))
            .andExpect(status().isUnprocessableEntity())
            .andExpect(jsonPath("$.errors[0].field").value("email"))
            .andExpect(jsonPath("$.errors[0].code").value("invalid_format"));
    }
}
```

→ Detalhes de testes em [[Testes]], [[Testes em Java]]

---

## Armadilhas comuns

- **Verbos em URLs** — `POST /createUser` em vez de `POST /users`.
- **Status code sempre 200** — `{ "success": false, "error": "..." }` com HTTP 200 quebra monitoring, retries e caches.
- **Não paginar coleções** — `GET /orders` retornando 100k registros derruba DB e cliente.
- **Envelopes desnecessários** — `{ "data": { "data": { "results": [...] } } }`. Um envelope simples ou payload direto bastam.
- **Mudar API sem versionar** — quebrar consumers sem aviso destrói confiança.
- **Mensagens de erro inúteis** — `{"error": "Invalid"}` não ajuda ninguém.
- **Expor IDs internos sequenciais** — `/orders/1`, `/orders/2` vaza volume de negócio. Use UUIDs ou IDs opacos para recursos públicos.
- **Expor schema do banco** — API é contrato, banco é implementação. Desacople.
- **Ignorar caching HTTP** — não usar ETag/Cache-Control é desperdício grátis.
- **Auth só "depois"** — retrofit de autenticação é sempre mais custoso que desde o início.
- **Rate limiting "depois"** — sem rate limiting, um cliente com bug derruba sua API.
- **Documentação desatualizada** — pior que não ter. Gere a partir do código ou falhe builds quando divergir.
- **PUT para atualização parcial** — PUT substitui inteiro. Se você não manda todos os campos, eles são apagados.
- **Campos opcionais que viram obrigatórios** — breaking change silenciosa.
- **Retornar datas sem timezone** — use ISO 8601 com timezone (`2026-04-10T12:00:00Z`).
- **Retornar dinheiro como float** — use inteiros em centavos ou decimal string. Float tem imprecisão.
- **Singulares e plurais misturados** — `/user/123` e `/patients/456` na mesma API. Consistência.
- **N+1 oculto** — cliente pegando lista e fazendo detail request para cada item. Deixe a API retornar o necessário.
- **Não tolerar fields desconhecidos** — parser estrito quebra no primeiro campo novo adicionado.

---

## Na prática (da minha experiência)

> **MedEspecialista — API REST com RFC 9457 e Problem Details:**
> Implementei um `@RestControllerAdvice` global que traduz exceções de domínio em respostas Problem Details padronizadas. Todo erro tem `type`, `title`, `status`, `detail`, `trace_id` e, quando aplicável, um array `errors` com `field`, `code`, `message`. O frontend React mostra mensagens ao usuário usando o `code` (para i18n) e loga o `trace_id` — quando um usuário reporta um problema, eu busco pelo trace_id nos logs do backend e encontro o request exato. Reduziu drasticamente o tempo de debugging.
>
> **Idempotency para pagamentos:**
> No endpoint de criação de pagamento, exijo header `Idempotency-Key` (UUID). Armazeno a chave + hash do request + response em uma tabela com TTL de 24h. Se o mesmo key vem de novo com mesmo request, retorno a response cacheada. Se vem com request diferente, retorno 422 "key reused". Isso salvou mais de uma vez: mobile com rede ruim retentando o pagamento que tinha ido pelo primeiro tentativa.
>
> **Versionamento por URL path:**
> Uso `/api/v1/...` desde o dia 1. Quando precisei fazer breaking change em um endpoint, lancei `/api/v2/patients` em paralelo, mantive v1 funcionando, e só desliguei v1 depois de 6 meses e de confirmar por logs que nenhum cliente usava mais. Sem drama.
>
> **Paginação cursor-based no feed:**
> A listagem de consultas agendadas do médico usa cursor-based pagination (encoded com created_at + id). Inicialmente tinha offset, mas com médicos que têm milhares de consultas históricas, offset com página 500 ficava lento. Cursor resolve em O(log n) via índice composto `(doctor_id, created_at DESC, id DESC)`.
>
> **OpenAPI como contrato:**
> SpringDoc gera o OpenAPI a partir das annotations. O frontend (React + TypeScript) consome esse OpenAPI via `openapi-typescript` para gerar tipos e clients automaticamente. Quando o backend muda um campo, o TypeScript quebra no frontend — erro de compilação, não em runtime. Esse ciclo salvou vários bugs antes de chegar em produção.
>
> **A lição principal:** tratar a API como um produto, não como uma consequência do código. Quem vai consumir ela? Como fica a experiência dele? O que acontece quando ela falhar? Essas perguntas importam mais que detalhes de implementação.

---

## How to explain in English

> "My approach to API design is to think of it as a product — the consumer's experience matters more than the internal implementation. I follow REST principles by default: resources as nouns, proper HTTP verbs, semantic status codes, and standardized error responses using RFC 9457 Problem Details.
>
> Consistency is the most important property of a good API. If one endpoint paginates with `page` and `size`, all of them do. If one uses kebab-case in paths, all of them do. The mental overhead of inconsistency compounds quickly for consumers.
>
> For errors, I use Problem Details with a standard shape: type, title, status, detail, and an errors array for validation. I always include a trace ID so when a user reports an issue, I can find the exact request in logs. I never return HTTP 200 for errors — that breaks monitoring, retries, and caching semantics.
>
> For pagination, I default to cursor-based for anything that grows over time or needs infinite scroll, because offset performance degrades with deep pages and suffers from page drift. Offset is fine for small, static datasets where users need to jump to a specific page.
>
> I treat versioning as a first-class concern. I use URL path versioning because it's explicit and works well with HTTP caching. But I design for evolution — adding fields is always safe, removing or renaming never is. A version bump is a last resort, not the default.
>
> For POST operations that create resources or process payments, I implement idempotency keys — the Stripe pattern. The client sends an `Idempotency-Key` header with a UUID, and I store the result atomically with the operation. Retries from network failures become safe.
>
> Finally, I treat the OpenAPI spec as part of the contract, not as documentation. I generate it from the code with SpringDoc and let the frontend consume it with openapi-typescript to generate types. That turns breaking changes into compile errors in the frontend before they ever hit production."

### Frases úteis em entrevista

- "I follow REST principles by default and deviate only when I have a clear reason."
- "Consistency matters more than perfection — pick a convention and stick to it."
- "I use Problem Details (RFC 9457) for all error responses to have a predictable shape."
- "I design for evolution: adding fields is safe, removing them never is."
- "For pagination, cursor-based is my default for anything that grows or needs infinite scroll."
- "Idempotency keys make retries safe — I use the Stripe pattern for payment operations."
- "Every API needs rate limiting from day one, not retrofitted later."
- "The OpenAPI spec is the contract, not the documentation — I generate TypeScript types from it."
- "I never return HTTP 200 for errors. Status codes are part of the contract."
- "I version explicitly in the URL path for public APIs — it's more visible and debuggable."
- "Webhook design is API design inverted — you're the client, and retries + signatures are mandatory."

### Key vocabulary

- contrato da API → API contract
- recurso → resource
- ponto de extremidade → endpoint
- carga útil → payload
- envelope de resposta → response envelope
- paginação baseada em cursor → cursor-based pagination
- paginação baseada em offset → offset-based pagination
- versionamento → versioning
- compatibilidade retroativa → backward compatibility
- mudança incompatível → breaking change
- depreciação → deprecation
- chave de idempotência → idempotency key
- limitação de taxa → rate limiting
- autenticação → authentication
- autorização → authorization
- negociação de conteúdo → content negotiation
- requisição condicional → conditional request
- filtragem, ordenação → filtering, sorting
- especificação da API → API specification (OpenAPI)
- teste de contrato → contract testing
- gancho da web → webhook
- assinatura HMAC → HMAC signature

---

## Recursos

### Livros

- *API Design Patterns* — JJ Geewax (Google; o livro mais prático sobre design de APIs REST)
- *Designing Web APIs* — Brenda Jin, Saurabh Sahni, Amir Shevat (visão de produto)
- *RESTful Web APIs* — Leonard Richardson, Mike Amundsen (HATEOAS e hipermídia)
- *GraphQL in Action* — Samer Buna (GraphQL na prática)

### Guidelines públicas (estudo)

- [Google Cloud API Design Guide](https://cloud.google.com/apis/design) — guia canônico, rico em exemplos
- [Microsoft REST API Guidelines](https://github.com/microsoft/api-guidelines)
- [Stripe API Reference](https://stripe.com/docs/api) — exemplo de API REST premium
- [GitHub REST API](https://docs.github.com/en/rest) — exemplo de API madura
- [Zalando RESTful API Guidelines](https://opensource.zalando.com/restful-api-guidelines/)

### Padrões e RFCs

- [RFC 9457 — Problem Details for HTTP APIs](https://www.rfc-editor.org/rfc/rfc9457.html)
- [RFC 7396 — JSON Merge Patch](https://www.rfc-editor.org/rfc/rfc7396)
- [RFC 6902 — JSON Patch](https://www.rfc-editor.org/rfc/rfc6902)
- [RFC 8594 — Sunset HTTP Header](https://www.rfc-editor.org/rfc/rfc8594)
- [OpenAPI Specification](https://spec.openapis.org/oas/latest.html)
- [JSON:API](https://jsonapi.org/) — spec opinativa de envelope e paginação

### Ferramentas

- [Swagger Editor](https://editor.swagger.io/) — edição visual de OpenAPI
- [Stoplight](https://stoplight.io/) — design-first de APIs
- [Postman](https://www.postman.com/) — teste e documentação
- [Bruno](https://www.usebruno.com/) — alternativa open-source ao Postman
- [Pact](https://pact.io/) — contract testing
- [Prism](https://stoplight.io/open-source/prism) — mock server a partir de OpenAPI
- [openapi-typescript](https://github.com/drwpow/openapi-typescript) — gera tipos TS a partir de OpenAPI
- [SpringDoc](https://springdoc.org/) — OpenAPI para Spring Boot

### Vídeos

> [!info] REST do Jeito Certo
> [https://www.youtube.com/playlist?list=PLkpjQs-GfEMPituMCb77qd90onpF3khFt](https://www.youtube.com/playlist?list=PLkpjQs-GfEMPituMCb77qd90onpF3khFt)

### Fontes sobre idempotência

- [Stripe — Idempotent Requests](https://docs.stripe.com/api/idempotent_requests)
- [Idempotency in Payment Processing](https://www.computer.org/publications/tech-news/trends/idempotency-in-payment-processing-architecture)

---

## Veja também

- [[Redes e Protocolos]] — HTTP, TCP, TLS, WebSocket, gRPC em profundidade
- [[System Design]] — rate limiting, caching, escala, patterns
- [[Arquitetura de Software]] — DDD, bounded contexts, como APIs expõem domínios
- [[Spring Boot]] — implementação prática de APIs REST na stack Java
- [[Node.js]] — implementação em Node/Express/NestJS
- [[Python Backend]] — Django REST Framework, FastAPI
- [[Go Backend]] — net/http, Gin, gRPC
- [[Banco de dados]] — paginação, consistência, otimização de queries
- [[Testes]] — estratégias de teste
