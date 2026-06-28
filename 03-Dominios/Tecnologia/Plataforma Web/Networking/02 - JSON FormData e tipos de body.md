---
title: "JSON, FormData e tipos de body"
created: 2026-06-28
updated: 2026-06-28
type: note
fase: Iniciado
tags:
  - plataforma-web
  - networking
  - browser
  - javascript
  - fetch
  - entrevista
publish: true
---

# JSON, FormData e tipos de body

> [!abstract] TL;DR
> O body de um fetch pode ser JSON (mais comum para APIs REST), `FormData` (para upload de arquivos — sem definir `Content-Type`, o browser define com boundary automaticamente), URL-encoded (formulários HTML tradicionais), `Blob`/`ArrayBuffer` (dados binários) ou `ReadableStream` (streaming). O tipo do body determina o `Content-Type` — e em muitos casos, você não deve definir o header manualmente.

---

## JSON — o mais comum

```javascript
// Enviar JSON
const response = await fetch('/api/products', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json', // obrigatório para JSON
    'Accept': 'application/json',
  },
  body: JSON.stringify({
    name: 'Camiseta',
    price: 49.90,
    tags: ['roupa', 'casual'],
  }),
});

const created = await response.json();
```

---

## FormData — para upload de arquivos

```javascript
const formData = new FormData();
formData.append('name', 'Alice');
formData.append('avatar', fileInput.files[0]); // File object
formData.append('tags', 'frontend');
formData.append('tags', 'javascript'); // múltiplos valores com mesma key

// ❌ NUNCA definir Content-Type manualmente com FormData
// O browser precisa calcular o boundary automaticamente
const response = await fetch('/api/users', {
  method: 'POST',
  body: formData,
  // headers: { 'Content-Type': 'multipart/form-data' } // ❌ quebra o boundary!
});

// O browser define automaticamente:
// Content-Type: multipart/form-data; boundary=----WebKitFormBoundaryXXX
```

> [!warning] Não defina Content-Type com FormData
> Se você definir `Content-Type: multipart/form-data` manualmente, o browser não inclui o `boundary` — e o servidor não consegue parsear o body. Deixe o browser calcular automaticamente omitindo o header.

---

## URL-encoded — formulários tradicionais

```javascript
// Como formulários HTML com method="POST" e sem enctype="multipart/form-data"
const params = new URLSearchParams();
params.append('username', 'alice');
params.append('password', 'senha123');

const response = await fetch('/api/login', {
  method: 'POST',
  headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
  body: params,
});

// Equivalente a:
// body: 'username=alice&password=senha123'
```

---

## Blob e ArrayBuffer — dados binários

```javascript
// Enviar imagem como Blob
const blob = await fetch('/placeholder.jpg').then(r => r.blob());
const response = await fetch('/api/avatar', {
  method: 'PUT',
  headers: { 'Content-Type': blob.type }, // 'image/jpeg'
  body: blob,
});

// Enviar ArrayBuffer (processado em TypedArray)
const buffer = new ArrayBuffer(8);
const view = new Uint8Array(buffer);
view[0] = 42;

const response2 = await fetch('/api/binary', {
  method: 'POST',
  headers: { 'Content-Type': 'application/octet-stream' },
  body: buffer,
});
```

---

## Texto simples

```javascript
await fetch('/api/log', {
  method: 'POST',
  headers: { 'Content-Type': 'text/plain' },
  body: 'Este é um log de texto simples',
});
```

---

## ReadableStream — body em streaming

```javascript
// Enviar um stream diretamente (ex: vídeo sendo capturado)
const stream = await navigator.mediaDevices.getUserMedia({ video: true })
  .then(s => s.getTracks()[0])
  // ... processar em ReadableStream

// Ler response como stream
const response = await fetch('/api/large-file');
const reader = response.body.getReader();

while (true) {
  const { done, value } = await reader.read();
  if (done) break;
  
  processChunk(value); // Uint8Array com o chunk atual
}
```

---

## Tabela de tipos de body

| Tipo | Content-Type | Quando usar |
|---|---|---|
| `JSON.stringify(obj)` | `application/json` | APIs REST |
| `FormData` | `multipart/form-data; boundary=...` | Upload de arquivos |
| `URLSearchParams` | `application/x-www-form-urlencoded` | Formulários tradicionais |
| `Blob` | `blob.type` | Imagens, binários |
| `ArrayBuffer` | `application/octet-stream` | Dados binários raw |
| `string` | `text/plain` | Texto simples |
| `ReadableStream` | Depende do uso | Streaming |

---

## FormData a partir de um formulário HTML

```html
<form id="profile-form">
  <input name="name" type="text" value="Alice">
  <input name="avatar" type="file">
  <input name="bio" type="text" value="Desenvolvedora">
</form>
```

```javascript
const form = document.getElementById('profile-form');

form.addEventListener('submit', async (event) => {
  event.preventDefault();
  
  // Criar FormData a partir do formulário — pega todos os inputs automaticamente
  const formData = new FormData(form);
  
  // Adicionar campos programaticamente
  formData.append('timestamp', Date.now().toString());
  
  // Verificar conteúdo
  for (const [key, value] of formData) {
    console.log(key, value);
  }
  
  const response = await fetch('/api/profile', {
    method: 'POST',
    body: formData, // sem Content-Type!
  });
});
```

---

## Resposta de diferentes formatos

```javascript
// Detectar formato pela resposta
const response = await fetch('/api/export');
const contentType = response.headers.get('Content-Type') ?? '';

let data;
if (contentType.includes('application/json')) {
  data = await response.json();
} else if (contentType.includes('text/')) {
  data = await response.text();
} else {
  data = await response.blob();
  const url = URL.createObjectURL(data);
  downloadLink.href = url;
  downloadLink.click();
}
```

---

> [!question] Para fixar
> 1. Por que você não deve definir `Content-Type` ao usar `FormData`?
> 2. Qual a diferença entre `FormData` e `URLSearchParams` como body?
> 3. Como você criaria um `FormData` que captura todos os campos de um formulário HTML existente?
> 4. O que acontece se você chamar `response.json()` em uma resposta com body HTML?
> 5. Quando você usaria `ArrayBuffer` em vez de `Blob` como body?

---

## Veja também

- [[03-Dominios/Tecnologia/Plataforma Web/Networking/01 - fetch em profundidade|01 — fetch em profundidade]] — anterior
- [[03-Dominios/Tecnologia/Plataforma Web/Networking/03 - HTTP no cliente|03 — HTTP no cliente]] — próxima
- [[03-Dominios/Tecnologia/Plataforma Web/Web APIs/04 - Clipboard e File API|Web APIs 04 — File API]] — File object e FileReader
