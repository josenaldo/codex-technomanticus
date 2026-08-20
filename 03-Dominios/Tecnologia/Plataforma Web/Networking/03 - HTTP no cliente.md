---
title: "HTTP no cliente"
created: 2026-06-28
updated: 2026-06-28
type: note
fase: iniciado
tags:
  - plataforma-web
  - networking
  - browser
  - javascript
  - http
  - entrevista
publish: true
---

# HTTP no cliente

> [!abstract] TL;DR
> O protocolo HTTP define a comunicação entre browser e servidor: métodos (GET/POST/PUT/PATCH/DELETE), status codes (2xx/3xx/4xx/5xx), headers de autenticação/cache/CORS, e o mecanismo de cookies. Do ponto de vista do cliente, o mais crítico é: entender o que cada status code significa, como configurar CORS corretamente, e como usar headers de autenticação e cache.

---

## Métodos HTTP e semântica

| Método | Semântica | Idempotente | Com body |
|---|---|---|---|
| `GET` | Ler recurso | Sim | Não |
| `POST` | Criar recurso | Não | Sim |
| `PUT` | Substituir recurso completo | Sim | Sim |
| `PATCH` | Atualizar parcialmente | Não* | Sim |
| `DELETE` | Remover recurso | Sim | Opcional |
| `HEAD` | Como GET, sem body na resposta | Sim | Não |
| `OPTIONS` | Checar o que é suportado (preflight CORS) | Sim | Não |

*`PATCH` pode ser idempotente dependendo da implementação.

**Idempotente**: chamadas múltiplas com os mesmos dados produzem o mesmo estado final.

---

## Status codes essenciais

```
2xx — Sucesso
  200 OK                  — Requisição bem-sucedida
  201 Created             — Recurso criado (POST bem-sucedido)
  204 No Content          — Sucesso sem body (DELETE bem-sucedido)
  206 Partial Content     — Range request (streaming de vídeo)

3xx — Redirecionamento
  301 Moved Permanently   — URL mudou para sempre (SEO: atualizar links)
  302 Found               — Redirecionamento temporário
  304 Not Modified        — Cache ainda válido (ETag/Last-Modified)

4xx — Erro do cliente
  400 Bad Request         — Body malformado ou parâmetros inválidos
  401 Unauthorized        — Não autenticado (falta token)
  403 Forbidden           — Autenticado mas sem permissão
  404 Not Found           — Recurso não existe
  409 Conflict            — Conflito de estado (ex: email duplicado)
  410 Gone                — Removido permanentemente (diferente do 404)
  422 Unprocessable       — Validação falhou (campos inválidos)
  429 Too Many Requests   — Rate limit atingido

5xx — Erro do servidor
  500 Internal Server Error — Bug no servidor
  502 Bad Gateway          — Servidor upstream não respondeu
  503 Service Unavailable  — Servidor sobrecarregado ou em manutenção
  504 Gateway Timeout      — Servidor upstream demorou demais
```

---

## Headers de autenticação

```javascript
// Bearer token (JWT, OAuth)
fetch('/api/me', {
  headers: {
    'Authorization': `Bearer ${accessToken}`,
  },
});

// Basic Auth (usuário:senha em base64) — só via HTTPS
const credentials = btoa(`${username}:${password}`);
fetch('/api/resource', {
  headers: { 'Authorization': `Basic ${credentials}` },
});

// API Key em header
fetch('/api/data', {
  headers: { 'X-API-Key': apiKey },
});

// API Key em query param (menos seguro — aparece em logs)
fetch(`/api/data?api_key=${apiKey}`);
```

---

## CORS — Cross-Origin Resource Sharing

```javascript
// Request cross-origin — o browser adiciona automaticamente:
// Origin: https://meu-site.com

// Resposta precisa ter:
// Access-Control-Allow-Origin: https://meu-site.com  (ou '*')
// Access-Control-Allow-Credentials: true  (se usar cookies)

// Simple requests (não disparam preflight):
// - Métodos: GET, POST, HEAD
// - Headers permitidos: Accept, Accept-Language, Content-Language, Content-Type (com restrições)
// - Content-Type: application/x-www-form-urlencoded, multipart/form-data, text/plain

// Preflight (OPTIONS) é disparado quando:
// - Método não é GET/POST/HEAD
// - Header não é simples (ex: Authorization, Content-Type: application/json)
// - Usa cookies com credentials: 'include'

// Na prática: POST com JSON sempre dispara preflight
fetch('https://api.outro.com/data', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json', // ← dispara preflight
    'Authorization': 'Bearer token',    // ← dispara preflight
  },
  body: JSON.stringify(data),
  credentials: 'include', // enviar cookies cross-origin
});
```

---

## Headers de cache

```javascript
// Forçar sem cache (sempre ir à rede)
fetch('/api/data', { cache: 'no-store' });

// Usar cache mas revalidar (If-None-Match / If-Modified-Since)
fetch('/api/data', { cache: 'no-cache' });

// Usar cache mesmo que expirado
fetch('/api/data', { cache: 'force-cache' });

// Resposta do servidor com diretivas de cache
// Cache-Control: max-age=3600, must-revalidate
// Cache-Control: no-cache, no-store
// ETag: "abc123"
// Last-Modified: Wed, 25 Jun 2026 12:00:00 GMT

// 304 Not Modified: browser enviou If-None-Match: "abc123"
// Servidor confirma que o cache ainda é válido — sem body
```

---

## Headers de segurança (resposta do servidor)

```
Strict-Transport-Security: max-age=31536000; includeSubDomains
  → Força HTTPS por 1 ano

Content-Security-Policy: default-src 'self'; script-src 'self' cdn.example.com
  → Define quais origens podem carregar recursos

X-Content-Type-Options: nosniff
  → Impede browser de "adivinhar" o Content-Type (MIME sniffing)

X-Frame-Options: DENY
  → Impede que a página seja carregada em iframe (clickjacking)

Referrer-Policy: strict-origin-when-cross-origin
  → Controla o header Referrer enviado em requests

Permissions-Policy: camera=(), microphone=(), geolocation=()
  → Desativa features do browser
```

---

## Cookies e headers

```
Set-Cookie: session=abc; HttpOnly; Secure; SameSite=Lax; Max-Age=3600; Path=/

Cookie: session=abc; other_cookie=val
```

O browser automaticamente adiciona o header `Cookie` em requests para a mesma origem (ou com `credentials: include`).

---

## Retry com backoff exponencial

```javascript
async function fetchWithRetry(url, options = {}, retries = 3) {
  const RETRYABLE_STATUS = new Set([429, 503, 504]);
  
  for (let attempt = 0; attempt <= retries; attempt++) {
    try {
      const response = await fetch(url, options);
      
      if (RETRYABLE_STATUS.has(response.status) && attempt < retries) {
        const delay = Math.min(1000 * Math.pow(2, attempt), 30000); // 1s, 2s, 4s...
        
        // Respeitar Retry-After do servidor (rate limiting)
        const retryAfter = response.headers.get('Retry-After');
        const waitMs = retryAfter ? parseInt(retryAfter) * 1000 : delay;
        
        await new Promise(resolve => setTimeout(resolve, waitMs));
        continue;
      }
      
      return response;
    } catch (error) {
      if (attempt === retries) throw error;
      
      const delay = Math.min(1000 * Math.pow(2, attempt), 30000);
      await new Promise(resolve => setTimeout(resolve, delay));
    }
  }
}
```

---

> [!question] Para fixar
> 1. Qual a diferença entre 401 e 403? E entre 404 e 410?
> 2. O que é "idempotência"? Por que GET e DELETE são idempotentes mas POST não é?
> 3. Quando o browser dispara um preflight CORS OPTIONS? O que acontece antes da request principal?
> 4. Qual a diferença entre `Cache-Control: no-cache` e `Cache-Control: no-store`?
> 5. Por que cookies com `HttpOnly` não podem ser lidos via JavaScript?

---

## Veja também

- [[03-Dominios/Tecnologia/Plataforma Web/Networking/02 - JSON FormData e tipos de body|02 — JSON, FormData e tipos de body]] — anterior
- [[03-Dominios/Tecnologia/Plataforma Web/Networking/04 - Streams e SSE|04 — Streams e SSE]] — próxima
- [[03-Dominios/Tecnologia/Plataforma Web/Storage/01 - Cookies e Web Storage|Storage 01 — Cookies]] — cookies em detalhe
