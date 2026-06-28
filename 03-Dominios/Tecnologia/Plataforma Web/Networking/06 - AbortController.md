---
title: "AbortController e cancelamento"
created: 2026-06-28
updated: 2026-06-28
type: note
fase: Adepto
tags:
  - plataforma-web
  - networking
  - browser
  - javascript
  - fetch
  - cancelamento
  - entrevista
publish: true
---

# AbortController e cancelamento

> [!abstract] TL;DR
> `AbortController` é a primitiva de cancelamento do browser: cria um `signal` que pode ser passado para `fetch`, Timers, Event Listeners e qualquer API que o suporte. Quando `controller.abort()` é chamado, todos os receptores do signal são notificados e a operação é cancelada. É a solução correta para: cancelar requests desatualizados ao mudar de rota, implementar timeout de rede, ou limpar recursos quando um componente é desmontado.

---

## AbortController básico

```javascript
const controller = new AbortController();
const signal = controller.signal;

signal.aborted;  // false inicialmente
signal.reason;   // undefined, ou a razão passada para abort()

// Cancelar
controller.abort('Usuário navegou para outra página'); // razão opcional

signal.aborted; // true
signal.reason;  // 'Usuário navegou para outra página'
```

---

## Cancelar um fetch

```javascript
const controller = new AbortController();

// Passar o signal para o fetch
const fetchPromise = fetch('/api/data', {
  signal: controller.signal,
});

// Cancelar após 5 segundos (timeout manual)
const timeoutId = setTimeout(() => {
  controller.abort('Timeout: requisição demorou mais de 5s');
}, 5000);

try {
  const response = await fetchPromise;
  clearTimeout(timeoutId); // limpar timeout se completou antes
  const data = await response.json();
  return data;
} catch (error) {
  if (error.name === 'AbortError') {
    console.log('Request cancelado:', error.message);
    return null;
  }
  throw error; // re-throw erros de rede reais
}
```

---

## `AbortSignal.timeout()` — a forma mais simples

```javascript
// Criar um signal que aborta automaticamente após N ms
const response = await fetch('/api/data', {
  signal: AbortSignal.timeout(5000), // timeout de 5 segundos
});
```

> [!tip] Combinando timeouts
> Use `AbortSignal.any([signal1, signal2])` para combinar múltiplos signals — aborta quando qualquer um deles for acionado:
> ```javascript
> const response = await fetch(url, {
>   signal: AbortSignal.any([
>     userCancelController.signal,  // cancelamento do usuário
>     AbortSignal.timeout(10000),   // timeout de 10s
>   ]),
> });
> ```

---

## Padrão: cancelar requisição anterior ao pesquisar

```javascript
let currentController = null;

async function searchProducts(query) {
  // Cancelar request anterior se ainda estiver em andamento
  currentController?.abort('Nova pesquisa iniciada');
  currentController = new AbortController();
  
  try {
    const response = await fetch(`/api/products?q=${encodeURIComponent(query)}`, {
      signal: currentController.signal,
    });
    
    if (!response.ok) throw new Error(`HTTP ${response.status}`);
    return await response.json();
    
  } catch (error) {
    if (error.name === 'AbortError') return; // ignorar cancelamentos
    throw error;
  }
}

// Input de busca: cancela request anterior ao digitar
searchInput.addEventListener('input', () => {
  searchProducts(searchInput.value);
});
```

---

## Padrão: cancelar ao sair do componente (React)

```javascript
// React: cancelar fetch ao desmontar o componente
function useProductSearch(query) {
  const [products, setProducts] = useState([]);
  
  useEffect(() => {
    const controller = new AbortController();
    
    async function load() {
      try {
        const response = await fetch(`/api/products?q=${query}`, {
          signal: controller.signal,
        });
        const data = await response.json();
        setProducts(data);
      } catch (error) {
        if (error.name !== 'AbortError') {
          console.error(error);
        }
      }
    }
    
    load();
    
    // Cleanup: cancelar quando componente desmontar ou query mudar
    return () => controller.abort();
  }, [query]);
  
  return products;
}
```

---

## Cancelar Event Listeners com AbortSignal

```javascript
const controller = new AbortController();
const { signal } = controller;

// Adicionar múltiplos listeners que todos serão removidos de uma vez
document.addEventListener('click', handleClick, { signal });
document.addEventListener('keydown', handleKeydown, { signal });
window.addEventListener('resize', handleResize, { signal });

// Remover todos de uma vez
controller.abort();
// Equivalente a chamar removeEventListener para cada um — mas muito mais limpo
```

---

## Propagar cancelamento para operações customizadas

```javascript
// Verificar se foi cancelado dentro de uma operação longa
async function processLargeFile(file, signal) {
  const chunks = splitIntoChunks(file, 1024);
  
  for (const chunk of chunks) {
    // Verificar cancelamento antes de cada chunk
    if (signal.aborted) {
      throw new DOMException('Processamento cancelado', 'AbortError');
    }
    
    await processChunk(chunk);
  }
}

// Ouvir o evento 'abort' para cancelar operações assíncronas
async function streamingOperation(signal) {
  return new Promise((resolve, reject) => {
    const abortHandler = () => {
      // Limpar recursos e rejeitar
      cleanup();
      reject(new DOMException('Operação cancelada', 'AbortError'));
    };
    
    signal.addEventListener('abort', abortHandler, { once: true });
    
    startOperation((result) => {
      signal.removeEventListener('abort', abortHandler);
      resolve(result);
    });
  });
}
```

---

## Identificar AbortError corretamente

```javascript
function isAbortError(error) {
  // Verificar pela propriedade name (não instanceof — DOMException é complicado)
  return error.name === 'AbortError';
}

try {
  await fetch(url, { signal });
} catch (error) {
  if (isAbortError(error)) {
    // Cancelamento esperado — não logar como erro
    return;
  }
  
  // Erro de rede real — logar e tratar
  logError(error);
  throw error;
}
```

---

> [!question] Para fixar
> 1. O que `controller.abort()` faz? Como o fetch recebe a notificação de cancelamento?
> 2. Qual a diferença entre `AbortSignal.timeout(5000)` e usar `setTimeout(() => controller.abort(), 5000)`?
> 3. Como você cancelaria múltiplos listeners de evento de uma vez?
> 4. Por que um fetch cancelado lança `AbortError` em vez de simplesmente resolver a Promise?
> 5. Como você propagaria cancelamento para uma operação customizada (não-fetch)?

---

## Veja também

- [[03-Dominios/Tecnologia/Plataforma Web/Networking/05 - WebSockets|05 — WebSockets]] — anterior
- [[03-Dominios/Tecnologia/Plataforma Web/Networking/07 - Axios e HTTP clients|07 — Axios e HTTP clients]] — próxima
- [[03-Dominios/Tecnologia/Plataforma Web/Networking/01 - fetch em profundidade|01 — fetch em profundidade]] — o signal vai no options do fetch
