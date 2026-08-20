---
title: "Streams e SSE"
created: 2026-06-28
updated: 2026-06-28
type: note
fase: adepto
tags:
  - plataforma-web
  - networking
  - browser
  - javascript
  - streams
  - sse
  - entrevista
publish: true
---

# Streams e SSE

> [!abstract] TL;DR
> Streams permitem processar dados à medida que chegam — sem esperar a resposta completa. `Response.body` é um `ReadableStream` que pode ser consumido em chunks (ideal para download de arquivos grandes ou respostas de LLMs). Server-Sent Events (SSE) é o protocolo padrão para streaming unidirecional do servidor para o browser — simples, baseado em HTTP/1.1, com reconexão automática.

---

## Streams — Fetch Streaming

```javascript
// Ler a response como stream, chunk por chunk
const response = await fetch('/api/large-data');

if (!response.ok) throw new Error(`HTTP ${response.status}`);

const reader = response.body.getReader();
const decoder = new TextDecoder(); // chunk é Uint8Array — decodificar para string
let fullText = '';

while (true) {
  const { done, value } = await reader.read();
  if (done) break;
  
  const chunk = decoder.decode(value, { stream: true }); // stream: true para multi-byte chars
  fullText += chunk;
  
  updateProgressBar(fullText.length);
}

console.log('Completo:', fullText);
```

---

## Progresso de download com streams

```javascript
async function downloadWithProgress(url, onProgress) {
  const response = await fetch(url);
  
  if (!response.ok) throw new Error(`Download falhou: ${response.status}`);
  
  const contentLength = response.headers.get('Content-Length');
  const total = contentLength ? parseInt(contentLength) : null;
  
  const reader = response.body.getReader();
  const chunks = [];
  let received = 0;
  
  while (true) {
    const { done, value } = await reader.read();
    if (done) break;
    
    chunks.push(value);
    received += value.length;
    
    if (total) {
      onProgress(received / total); // 0.0 a 1.0
    }
  }
  
  // Montar Blob final
  const blob = new Blob(chunks);
  return blob;
}

// Uso
const blob = await downloadWithProgress('/api/export.csv', (progress) => {
  progressBar.style.width = `${progress * 100}%`;
});

const url = URL.createObjectURL(blob);
downloadLink.href = url;
downloadLink.click();
URL.revokeObjectURL(url);
```

---

## Streaming de LLM (padrão moderno)

Respostas de LLMs vêm em chunks de texto — ideal para streaming com fetch:

```javascript
async function streamCompletion(prompt, onChunk) {
  const response = await fetch('/api/chat', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ prompt }),
  });
  
  const reader = response.body.getReader();
  const decoder = new TextDecoder();
  
  while (true) {
    const { done, value } = await reader.read();
    if (done) break;
    
    const text = decoder.decode(value, { stream: true });
    onChunk(text);
  }
}

// Uso
const output = document.getElementById('output');
await streamCompletion('Explique streams em JavaScript', (chunk) => {
  output.textContent += chunk; // exibir tokens à medida que chegam
});
```

---

## Server-Sent Events (SSE)

SSE é um protocolo HTTP padrão para streaming do servidor para o cliente. O servidor envia linhas no formato `data: ...\n\n`.

### Cliente

```javascript
const eventSource = new EventSource('/api/events');

// Evento padrão (sem tipo)
eventSource.onmessage = (event) => {
  const data = JSON.parse(event.data);
  updateUI(data);
};

// Eventos tipados
eventSource.addEventListener('stock-update', (event) => {
  renderStockPrice(JSON.parse(event.data));
});

eventSource.addEventListener('notification', (event) => {
  showNotification(JSON.parse(event.data));
});

// Erros e reconexão
eventSource.onerror = (event) => {
  if (eventSource.readyState === EventSource.CLOSED) {
    console.log('Conexão encerrada');
  } else {
    // readyState === CONNECTING — reconectando automaticamente
    console.log('Reconectando...');
  }
};

// Encerrar conexão
eventSource.close();
```

### Servidor (Node.js/Express)

```javascript
// server.js
app.get('/api/events', (req, res) => {
  // Headers obrigatórios para SSE
  res.writeHead(200, {
    'Content-Type': 'text/event-stream',
    'Cache-Control': 'no-cache',
    'Connection': 'keep-alive',
    'Access-Control-Allow-Origin': '*', // se necessário CORS
  });
  
  // Enviar evento
  function sendEvent(type, data) {
    res.write(`event: ${type}\n`);
    res.write(`data: ${JSON.stringify(data)}\n`);
    res.write('\n'); // linha em branco encerra o evento
  }
  
  // Enviar dado simples (sem tipo)
  function sendData(data) {
    res.write(`data: ${JSON.stringify(data)}\n\n`);
  }
  
  // Enviar evento com ID (browser envia Last-Event-ID na reconexão)
  let id = 0;
  function sendWithId(data) {
    res.write(`id: ${id++}\n`);
    res.write(`data: ${JSON.stringify(data)}\n`);
    res.write('\n');
  }
  
  // Exemplo: preços de ações em tempo real
  const interval = setInterval(() => {
    sendEvent('stock-update', { ticker: 'AAPL', price: 180 + Math.random() * 10 });
  }, 1000);
  
  // Limpar quando o cliente desconectar
  req.on('close', () => {
    clearInterval(interval);
    res.end();
  });
});
```

---

## SSE com autenticação

`EventSource` não permite headers customizados (incluindo `Authorization`). Alternativas:

```javascript
// Opção 1: Token na query string (menos seguro)
const source = new EventSource(`/api/events?token=${encodeURIComponent(token)}`);

// Opção 2: Cookie (usar cookies HttpOnly para a sessão)
// Browser envia cookies automaticamente

// Opção 3: Fetch com stream (mais flexível — aceita headers)
async function fetchSSE(url, headers, onEvent) {
  const response = await fetch(url, { headers });
  const reader = response.body.getReader();
  const decoder = new TextDecoder();
  let buffer = '';
  
  while (true) {
    const { done, value } = await reader.read();
    if (done) break;
    
    buffer += decoder.decode(value, { stream: true });
    const lines = buffer.split('\n');
    buffer = lines.pop() ?? ''; // manter linha incompleta no buffer
    
    for (const line of lines) {
      if (line.startsWith('data: ')) {
        onEvent(JSON.parse(line.slice(6)));
      }
    }
  }
}
```

---

## SSE vs WebSocket

| | SSE | WebSocket |
|---|---|---|
| Direção | Só servidor → cliente | Bidirecional |
| Protocolo | HTTP/1.1 | WS (upgrade do HTTP) |
| Reconexão automática | Sim (nativa no EventSource) | Manual |
| Multiplexação HTTP/2 | Sim | Não (protocolo próprio) |
| Firewall/proxies | Transparente (HTTP) | Pode ser bloqueado |
| Caso de uso | Feed de notícias, logs ao vivo, preços | Chat, jogos, colaboração em tempo real |

---

> [!question] Para fixar
> 1. Qual a diferença entre ler `response.json()` e consumir `response.body` como stream?
> 2. O que o argumento `{ stream: true }` faz no `TextDecoder.decode()`?
> 3. Por que SSE reconecta automaticamente? O que `Last-Event-ID` tem a ver com isso?
> 4. Quando você preferiria SSE em vez de WebSocket?
> 5. Por que `EventSource` não suporta headers customizados? Como você lidaria com autenticação?

---

## Veja também

- [[03-Dominios/Tecnologia/Plataforma Web/Networking/03 - HTTP no cliente|03 — HTTP no cliente]] — anterior
- [[03-Dominios/Tecnologia/Plataforma Web/Networking/05 - WebSockets|05 — WebSockets]] — próxima
- [[03-Dominios/Tecnologia/Plataforma Web/Networking/07 - AbortController|07 — AbortController]] — cancelar streams em andamento
