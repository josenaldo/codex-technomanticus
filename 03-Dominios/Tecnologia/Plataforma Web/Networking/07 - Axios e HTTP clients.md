---
title: "Axios e HTTP clients"
created: 2026-06-28
updated: 2026-06-28
type: note
fase: adepto
tags:
  - plataforma-web
  - networking
  - browser
  - javascript
  - axios
  - http-client
  - entrevista
publish: true
---

# Axios e HTTP clients

> [!abstract] TL;DR
> Axios é um cliente HTTP baseado em Promises para browser e Node.js. Suas vantagens sobre fetch bruto: serialização/deserialização automática de JSON, interceptors para autenticação e retry global, tratamento correto de erros (rejeita em 4xx/5xx), cancelamento via `AbortController`, e interface simétrica entre browser e Node. Em 2024, `fetch` nativo resolveu muitas das lacunas — Axios ainda vale pela ergonomia dos interceptors.

---

## Configuração inicial

```javascript
import axios from 'axios';

// Criar instância configurada (não usar axios diretamente)
export const api = axios.create({
  baseURL: 'https://api.exemplo.com',
  timeout: 10000,                            // ms até timeout
  headers: {
    'Content-Type': 'application/json',
    'Accept': 'application/json',
  },
});
```

---

## Métodos HTTP

```javascript
// GET
const response = await api.get('/users', {
  params: { page: 1, limit: 20 }, // serializado como ?page=1&limit=20
});
const users = response.data; // Axios já parseia JSON

// POST
const created = await api.post('/users', {
  name: 'Alice',
  email: 'alice@exemplo.com',
});

// PUT / PATCH
await api.put(`/users/${id}`, user);
await api.patch(`/users/${id}`, { name: 'Alice Atualizada' });

// DELETE
await api.delete(`/users/${id}`);

// Múltiplas requests em paralelo
const [user, posts] = await Promise.all([
  api.get(`/users/${id}`),
  api.get(`/users/${id}/posts`),
]);
```

---

## Diferenças em relação ao fetch

| | fetch | Axios |
|---|---|---|
| JSON automático | Não (`.json()` manual) | Sim |
| Rejeita em 4xx/5xx | Não (verificar `response.ok`) | Sim |
| Interceptors | Manual | Nativo |
| Progress de upload | XHR manual | `onUploadProgress` |
| CSRF token automático | Não | Com interceptor |
| Timeout nativo | `AbortSignal.timeout()` | `timeout` option |
| Node.js | Sim (17.5+) | Sim (desde sempre) |

---

## Interceptors — a killer feature

```javascript
// Interceptor de request: adicionar token a todos os requests
api.interceptors.request.use(
  (config) => {
    const token = getAccessToken();
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => Promise.reject(error)
);

// Interceptor de response: refresh automático de token
api.interceptors.response.use(
  (response) => response, // Passar respostas bem-sucedidas
  async (error) => {
    const originalRequest = error.config;
    
    // 401 e ainda não tentou refresh
    if (error.response?.status === 401 && !originalRequest._retry) {
      originalRequest._retry = true;
      
      try {
        const newToken = await refreshAccessToken();
        setAccessToken(newToken);
        originalRequest.headers.Authorization = `Bearer ${newToken}`;
        return api(originalRequest); // retry com novo token
      } catch (refreshError) {
        redirectToLogin();
        return Promise.reject(refreshError);
      }
    }
    
    return Promise.reject(error);
  }
);
```

---

## Erros do Axios

```javascript
try {
  const response = await api.get('/api/users/999');
} catch (error) {
  if (axios.isAxiosError(error)) {
    // Erro HTTP (4xx, 5xx) ou rede
    if (error.response) {
      // Servidor respondeu com status de erro
      console.error('Status:', error.response.status);
      console.error('Dados:', error.response.data);
      console.error('Headers:', error.response.headers);
      
      if (error.response.status === 404) {
        return null;
      }
    } else if (error.request) {
      // Request foi feita mas sem resposta (sem rede, timeout)
      console.error('Sem resposta:', error.request);
    } else {
      // Erro ao configurar a request
      console.error('Config error:', error.message);
    }
  } else {
    throw error; // Erro não é do Axios
  }
}
```

---

## Upload com progresso

```javascript
async function uploadFile(file, onProgress) {
  const formData = new FormData();
  formData.append('file', file);
  
  const response = await api.post('/api/upload', formData, {
    headers: { 'Content-Type': 'multipart/form-data' },
    onUploadProgress: (progressEvent) => {
      if (progressEvent.lengthComputable) {
        const percent = Math.round(
          (progressEvent.loaded * 100) / progressEvent.total
        );
        onProgress(percent);
      }
    },
    timeout: 0, // sem timeout para uploads grandes
  });
  
  return response.data;
}
```

---

## Cancelamento com AbortController

```javascript
const controller = new AbortController();

try {
  const response = await api.get('/api/search', {
    params: { q: query },
    signal: controller.signal, // Axios 1.x suporta AbortSignal
  });
  return response.data;
} catch (error) {
  if (axios.isCancel(error) || error.name === 'AbortError') {
    return null; // cancelado normalmente
  }
  throw error;
}

// Cancelar
controller.abort();
```

---

## Quando usar fetch vs Axios

```
Use fetch nativo quando:
  - Projeto sem dependências adicionais (script simples, pequena lib)
  - Você precisa de streaming (response.body)
  - Node.js 18+ e não quer dependência
  - Quer usar AbortSignal.any() ou AbortSignal.timeout()

Use Axios quando:
  - Precisa de interceptors para auth/retry global
  - Múltiplos desenvolvedores: API mais familiar e consistente
  - Upload com progresso
  - Compatibilidade com Node.js legado (< 18)
  - Quer serialização/deserialização automática de JSON
  - Projeto já usa Axios (consistência)
```

---

## Alternativas modernas ao Axios

```javascript
// ofetch (Nuxt, Unjs) — fetch moderno com ergonomia de Axios
import { ofetch } from 'ofetch';
const user = await ofetch('/api/users/1', { baseURL: 'https://api.exemplo.com' });

// ky — wrapper fetch minimalista
import ky from 'ky';
const user = await ky.get('https://api.exemplo.com/users/1').json();

// TanStack Query (React Query) — gerenciamento de estado server com cache
const { data, isLoading } = useQuery({
  queryKey: ['user', id],
  queryFn: () => api.get(`/users/${id}`).then(r => r.data),
  staleTime: 5 * 60 * 1000, // 5 minutos
});

// SWR (Vercel) — alternativa ao React Query
const { data, error } = useSWR(`/api/users/${id}`, fetcher);
```

---

> [!question] Para fixar
> 1. Qual o principal problema com fetch que Axios resolve automaticamente?
> 2. O que são interceptors? Descreva um caso de uso real.
> 3. Como o Axios trata erros HTTP diferente do fetch?
> 4. Por que `onUploadProgress` do Axios usa XHR internamente?
> 5. Quando você escolheria fetch nativo sobre Axios?

---

## Veja também

- [[03-Dominios/Tecnologia/Plataforma Web/Networking/06 - AbortController|06 — AbortController]] — anterior
- [[03-Dominios/Tecnologia/Plataforma Web/Networking/08 - Networking em entrevista|08 — Networking em entrevista]] — próxima e capstone
- [[03-Dominios/Tecnologia/Plataforma Web/Networking/01 - fetch em profundidade|01 — fetch em profundidade]] — fundação do Axios
