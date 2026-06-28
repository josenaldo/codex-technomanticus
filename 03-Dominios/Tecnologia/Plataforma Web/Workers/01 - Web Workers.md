---
title: "Web Workers"
created: 2026-06-28
updated: 2026-06-28
type: note
fase: Iniciado
tags:
  - plataforma-web
  - workers
  - browser
  - javascript
  - concorrencia
  - entrevista
publish: true
---

# Web Workers

> [!abstract] TL;DR
> Web Workers executam código JavaScript em threads separadas — sem bloquear o main thread. São a única forma de paralelismo real no browser. Comunicam-se com a página principal via `postMessage` (cópia de dados) ou `SharedArrayBuffer` (memória compartilhada, com Atomics). Não têm acesso ao DOM — calculam, o main thread renderiza.

---

## Por que Web Workers?

JavaScript é single-threaded. Uma operação cara (parse de JSON gigante, cálculo científico, compressão de imagem) bloqueia o main thread — o UI trava, animações param, eventos não respondem.

```javascript
// ❌ Bloqueia o main thread — UI congela por vários segundos
function processLargeData(data) {
  return data.map(item => heavyComputation(item)); // síncrono
}

// ✅ Web Worker — não bloqueia nada
const worker = new Worker('worker.js');
worker.postMessage(data);
worker.onmessage = (event) => renderResults(event.data);
```

---

## Criar e se comunicar com um Worker

```javascript
// main.js
const worker = new Worker('/worker.js');
// Também possível com módulos ES:
// const worker = new Worker('/worker.js', { type: 'module' });

// Enviar dados para o worker
worker.postMessage({ action: 'process', data: largeArray });

// Receber resposta
worker.onmessage = (event) => {
  console.log('Resultado:', event.data);
};

// Tratar erros
worker.onerror = (error) => {
  console.error('Worker error:', error.message, 'em', error.filename, ':', error.lineno);
};

// Terminar o worker (libera thread)
worker.terminate();
```

```javascript
// worker.js — roda em thread separada
// Sem acesso a: document, window, DOM
// Tem acesso a: fetch, setTimeout, indexedDB, console, crypto, etc.

self.onmessage = (event) => {
  const { action, data } = event.data;
  
  if (action === 'process') {
    const result = data.map(item => heavyComputation(item));
    self.postMessage(result); // enviar resultado de volta
  }
};

// Tratar erros não capturados no worker
self.onerror = (error) => {
  console.error('Uncaught error in worker:', error);
};
```

---

## Transferência de dados: cópia vs transferência

Por padrão, `postMessage` **copia** os dados (structured clone algorithm). Para arrays grandes, isso é caro:

```javascript
const largeBuffer = new ArrayBuffer(100 * 1024 * 1024); // 100MB

// ❌ Cópia — 100MB copiados de volta e para frente
worker.postMessage(largeBuffer);

// ✅ Transferência — zero-copy; o buffer é movido (main thread perde acesso)
worker.postMessage(largeBuffer, [largeBuffer]);
// largeBuffer.byteLength === 0 agora no main thread
```

**Objetos transferíveis:** `ArrayBuffer`, `MessagePort`, `ImageBitmap`, `OffscreenCanvas`, `ReadableStream`/`WritableStream`, `TransformStream`.

---

## Padrão: worker como serviço

```javascript
// worker-service.js — interface limpa para usar um worker
class WorkerService {
  constructor(workerUrl) {
    this.worker = new Worker(workerUrl, { type: 'module' });
    this.pending = new Map(); // id → { resolve, reject }
    this.nextId = 0;
    
    this.worker.onmessage = (event) => {
      const { id, result, error } = event.data;
      const pending = this.pending.get(id);
      
      if (!pending) return;
      this.pending.delete(id);
      
      if (error) {
        pending.reject(new Error(error));
      } else {
        pending.resolve(result);
      }
    };
    
    this.worker.onerror = (error) => {
      // Rejeitar todas as promises pendentes em caso de crash
      this.pending.forEach(({ reject }) => reject(error));
      this.pending.clear();
    };
  }

  call(action, data, transferable = []) {
    return new Promise((resolve, reject) => {
      const id = this.nextId++;
      this.pending.set(id, { resolve, reject });
      this.worker.postMessage({ id, action, data }, transferable);
    });
  }

  terminate() {
    this.worker.terminate();
  }
}

// worker.js — corresponde ao protocolo
self.onmessage = async (event) => {
  const { id, action, data } = event.data;
  
  try {
    let result;
    if (action === 'compress') result = await compress(data);
    else if (action === 'parse') result = parseHeavy(data);
    else throw new Error(`Unknown action: ${action}`);
    
    self.postMessage({ id, result });
  } catch (error) {
    self.postMessage({ id, error: error.message });
  }
};

// Uso no main thread
const imageService = new WorkerService('/image-worker.js');
const compressed = await imageService.call('compress', imageBuffer, [imageBuffer]);
```

---

## Inline Workers com Blob URL

Para criar workers sem arquivo separado:

```javascript
const workerCode = `
  self.onmessage = (event) => {
    const result = event.data * 2;
    self.postMessage(result);
  };
`;

const blob = new Blob([workerCode], { type: 'application/javascript' });
const url = URL.createObjectURL(blob);
const worker = new Worker(url);

worker.postMessage(21);
worker.onmessage = (e) => console.log(e.data); // 42

// Limpar quando não precisar mais
worker.terminate();
URL.revokeObjectURL(url);
```

---

## SharedArrayBuffer e Atomics

Para compartilhar memória entre threads sem cópia (requer COOP/COEP headers):

```javascript
// main.js
const buffer = new SharedArrayBuffer(4); // 4 bytes compartilhados
const view = new Int32Array(buffer);

worker.postMessage({ buffer }); // não transfere — continua compartilhado
view[0] = 10; // main thread escreve

// worker.js
self.onmessage = (event) => {
  const view = new Int32Array(event.data.buffer);
  
  // Leitura/escrita segura com Atomics (evita race conditions)
  const value = Atomics.load(view, 0);    // ler atomicamente
  Atomics.store(view, 0, value + 1);      // escrever atomicamente
  Atomics.add(view, 0, 5);               // incrementar atomicamente
  
  // Esperar que main thread sinalize (block-able só em workers)
  Atomics.wait(view, 0, 10, 1000);       // aguardar view[0] != 10 por até 1000ms
  
  // Sinalizar main thread
  Atomics.notify(view, 0, 1);            // notificar 1 waiter
};
```

> [!warning] Requisitos para SharedArrayBuffer
> SharedArrayBuffer requer que a página seja "cross-origin isolated" com os headers:
> ```
> Cross-Origin-Opener-Policy: same-origin
> Cross-Origin-Embedder-Policy: require-corp
> ```
> Sem esses headers, `new SharedArrayBuffer()` lança TypeError.

---

## O que os workers podem e não podem fazer

| Disponível | Indisponível |
|---|---|
| `fetch`, `XMLHttpRequest` | `document`, `window` |
| `setTimeout`, `setInterval` | DOM APIs |
| `indexedDB` | `localStorage` (use IndexedDB) |
| `console` | `alert`, `prompt`, `confirm` |
| `crypto` | Manipulação de elementos |
| `WebAssembly` | `postMessage` para outra janela |
| `importScripts()` (Classic) | `navigator` (parcial) |
| ES Modules (com `type: 'module'`) | `location` (parcial) |

---

> [!question] Para fixar
> 1. Por que Web Workers não têm acesso ao DOM?
> 2. O que acontece com os dados enviados via `postMessage`? São copiados ou compartilhados?
> 3. O que é "transferência" no contexto de `postMessage`? O que acontece com o dado no remetente após a transferência?
> 4. Por que o padrão de "worker como serviço" com IDs é útil?
> 5. Quando você usaria `SharedArrayBuffer` em vez de `postMessage`?

---

## Veja também

- [[03-Dominios/Tecnologia/Plataforma Web/Workers/02 - SharedWorker e BroadcastChannel|02 — SharedWorker e BroadcastChannel]] — próxima
- [[03-Dominios/Tecnologia/Plataforma Web/Workers/index|Workers — índice]]
- [[03-Dominios/Tecnologia/Plataforma Web/Eventos/06 - Timers e microtasks|Eventos 06 — Timers e microtasks]] — context do main thread e event loop
