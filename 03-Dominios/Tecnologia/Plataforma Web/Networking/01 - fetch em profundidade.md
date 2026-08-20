---
title: "fetch em profundidade"
created: 2026-06-28
updated: 2026-06-28
type: note
fase: iniciado
tags:
  - plataforma-web
  - networking
  - browser
  - javascript
  - fetch
  - entrevista
publish: true
---

# fetch em profundidade

> [!abstract] TL;DR
> `fetch` é a API nativa para HTTP no browser: baseada em Promises, retorna um `Response` que tem um body como stream — você precisa chamar `.json()`, `.text()` ou `.blob()` para consumir. Um detalhe contra-intuitivo: `fetch` só rejeita a Promise em erro de rede — respostas HTTP 4xx e 5xx são **resolvidas com sucesso**. Sempre verificar `response.ok`.

---

## A anatomia de uma requisição fetch

```javascript
const response = await fetch(url, options);
```

```javascript
const options = {
  method: 'POST',          // 'GET' | 'POST' | 'PUT' | 'PATCH' | 'DELETE' | 'HEAD'
  headers: {
    'Content-Type': 'application/json',
    'Authorization': `Bearer ${token}`,
    'Accept': 'application/json',
  },
  body: JSON.stringify(data), // string | Blob | BufferSource | FormData | URLSearchParams | ReadableStream
  
  // Controle de cache
  cache: 'default',     // 'default' | 'no-store' | 'reload' | 'no-cache' | 'force-cache'
  
  // Referrer
  referrerPolicy: 'strict-origin-when-cross-origin',
  
  // Credenciais (cookies)
  credentials: 'same-origin', // 'omit' | 'same-origin' | 'include'
  
  // CORS
  mode: 'cors',         // 'cors' | 'no-cors' | 'same-origin'
  
  // Redirect
  redirect: 'follow',   // 'follow' | 'error' | 'manual'
  
  // Fetch priority (hint para o browser)
  priority: 'auto',     // 'high' | 'low' | 'auto'
  
  // AbortController
  signal: controller.signal,
};
```

---

## O objeto Response

```javascript
const response = await fetch('/api/user');

// Metadata
response.ok;          // true se status 200-299
response.status;      // 200, 404, 500, etc.
response.statusText;  // 'OK', 'Not Found', etc.
response.url;         // URL final (após redirects)
response.redirected;  // true se houve redirect
response.type;        // 'basic' | 'cors' | 'opaque'

// Headers
response.headers.get('Content-Type');
response.headers.get('X-Rate-Limit');
for (const [key, value] of response.headers) { ... }

// Body (cada método consome o stream — só pode ser chamado uma vez)
const json = await response.json();           // parsear como JSON
const text = await response.text();           // como string
const blob = await response.blob();           // como Blob (imagens, binários)
const buffer = await response.arrayBuffer(); // como ArrayBuffer
const form = await response.formData();       // como FormData

// Verificar se o body ainda pode ser lido
response.bodyUsed; // true se já foi consumido
response.body;     // ReadableStream (para streaming)
```

---

## O erro mais comum: `fetch` não rejeita em erros HTTP

```javascript
// ❌ Armadilha: 404 e 500 resolvem a Promise!
const response = await fetch('/api/user/999');
// response.status === 404, mas não entrou no catch!

// ✅ Sempre verificar response.ok
const response = await fetch('/api/user/999');
if (!response.ok) {
  throw new Error(`HTTP ${response.status}: ${response.statusText}`);
}
const user = await response.json();
```

---

## Wrapper com tratamento de erro padrão

```javascript
class ApiError extends Error {
  constructor(status, statusText, body) {
    super(`${status} ${statusText}`);
    this.name = 'ApiError';
    this.status = status;
    this.body = body;
  }
}

async function apiFetch(url, options = {}) {
  const response = await fetch(url, {
    headers: { 'Accept': 'application/json', ...options.headers },
    ...options,
  });
  
  if (!response.ok) {
    const body = await response.text().catch(() => '');
    throw new ApiError(response.status, response.statusText, body);
  }
  
  // Respostas sem body (204 No Content)
  const contentType = response.headers.get('Content-Type') ?? '';
  if (response.status === 204 || !contentType.includes('application/json')) {
    return null;
  }
  
  return response.json();
}

// Uso
try {
  const user = await apiFetch('/api/users/1');
} catch (error) {
  if (error instanceof ApiError && error.status === 404) {
    console.log('Usuário não encontrado');
  } else if (error instanceof ApiError && error.status === 401) {
    redirectToLogin();
  } else {
    throw error; // re-throw erros inesperados
  }
}
```

---

## CORS e credenciais

```javascript
// Request cross-origin com cookies (credenciais)
const response = await fetch('https://api.outro-dominio.com/data', {
  credentials: 'include', // enviar cookies na request cross-origin
  // O servidor precisa responder com:
  // Access-Control-Allow-Origin: https://meu-dominio.com (não pode ser '*')
  // Access-Control-Allow-Credentials: true
});

// 'same-origin' (padrão): enviar cookies só para mesma origem
// 'omit': nunca enviar cookies
// 'include': sempre enviar cookies (inclusive cross-origin)
```

---

## Verificar se fetch está disponível (legado)

```javascript
if (!window.fetch) {
  // Polyfill: github.com/github/fetch
}
```

`fetch` está disponível em todos os browsers modernos desde 2017. Não é mais necessário verificar em projetos que suportam apenas browsers modernos.

---

> [!question] Para fixar
> 1. Quando `fetch` rejeita a Promise? O que não faz rejeitar?
> 2. Por que você não pode chamar `response.json()` duas vezes?
> 3. Qual a diferença entre `credentials: 'same-origin'` e `credentials: 'include'`?
> 4. O que é `response.ok`? Quais status codes fazem ela ser `true`?
> 5. Por que uma resposta 500 "resolveria" a Promise de um fetch?

---

## Veja também

- [[03-Dominios/Tecnologia/Plataforma Web/Networking/02 - JSON FormData e tipos de body|02 — JSON, FormData e tipos de body]] — próxima
- [[03-Dominios/Tecnologia/Plataforma Web/Networking/07 - AbortController|07 — AbortController]] — cancelar requests
- [[03-Dominios/Tecnologia/Plataforma Web/Networking/index|Networking — índice]]
