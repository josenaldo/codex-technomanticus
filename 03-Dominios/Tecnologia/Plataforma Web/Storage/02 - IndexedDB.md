---
title: "IndexedDB"
created: 2026-06-28
updated: 2026-06-28
type: note
fase: Iniciado
tags:
  - plataforma-web
  - storage
  - browser
  - javascript
  - indexeddb
  - entrevista
publish: true
---

# IndexedDB

> [!abstract] TL;DR
> IndexedDB é o banco de dados NoSQL do browser: armazena objetos JavaScript estruturados, suporta índices, transações e queries assíncronas. Cabe centenas de MB (com quotas por origem). É a solução para dados complexos que precisam persistir offline, como catálogos de produtos, dados de usuário, rascunhos, histórico. A API nativa é verbosa — em produção, use wrappers como `idb` ou `Dexie.js`.

---

## Conceitos fundamentais

```
Database (banco)
  ├── Object Store (coleção/tabela)
  │     ├── Registros (objetos JS arbitrários)
  │     └── Index (índice secundário para queries)
  └── Transaction (agrupa operações; readonly ou readwrite)
```

Regras:
- Toda operação é dentro de uma **transaction** — nunca diretamente no banco
- Transactions com `readonly` podem rodar em paralelo; `readwrite` são exclusivas
- Uma transaction se commita automaticamente ao terminar — ou faz rollback se houver erro

---

## API nativa (verbosa)

```javascript
// Abrir banco (cria se não existir)
const request = indexedDB.open('meu-banco', 1); // nome, versão

// Executado só quando a versão aumenta (ou banco criado pela primeira vez)
request.onupgradeneeded = (event) => {
  const db = event.target.result;
  
  // Criar object store com keyPath (equivalente à primary key)
  const store = db.createObjectStore('produtos', { keyPath: 'id' });
  // Ou autoIncrement
  // const store = db.createObjectStore('logs', { autoIncrement: true });
  
  // Criar índices (para queries por campos diferentes do keyPath)
  store.createIndex('categoria', 'categoria', { unique: false });
  store.createIndex('nome', 'nome', { unique: false });
};

request.onsuccess = (event) => {
  const db = event.target.result;
  
  // Escrever
  const tx = db.transaction('produtos', 'readwrite');
  const store = tx.objectStore('produtos');
  
  store.add({ id: 1, nome: 'Camiseta', categoria: 'roupas', preco: 49.90 });
  store.put({ id: 1, nome: 'Camiseta P', categoria: 'roupas', preco: 44.90 }); // upsert
  store.delete(2);
  
  tx.oncomplete = () => console.log('Gravado com sucesso');
  tx.onerror = (e) => console.error('Erro:', e.target.error);
};

request.onerror = (event) => {
  console.error('Falha ao abrir banco:', event.target.error);
};
```

---

## Usando a biblioteca `idb` (recomendado)

A biblioteca `idb` (de Jake Archibald) envolve IndexedDB com Promises — elimina toda a verbosidade:

```javascript
import { openDB } from 'idb';

const db = await openDB('meu-banco', 1, {
  upgrade(db) {
    const store = db.createObjectStore('produtos', { keyPath: 'id' });
    store.createIndex('categoria', 'categoria');
  },
});

// CRUD com async/await
await db.add('produtos', { id: 1, nome: 'Camiseta', categoria: 'roupas', preco: 49.90 });
await db.put('produtos', { id: 1, nome: 'Camiseta P', preco: 44.90 }); // upsert
await db.delete('produtos', 1);

const produto = await db.get('produtos', 1);
const todos = await db.getAll('produtos');

// Query por índice
const roupas = await db.getAllFromIndex('produtos', 'categoria', 'roupas');

// Contar
const total = await db.count('produtos');
```

---

## Queries com cursor

Para percorrer grandes conjuntos de dados sem carregar tudo na memória:

```javascript
// Iterar com cursor (idb)
const tx = db.transaction('produtos', 'readonly');
let cursor = await tx.store.openCursor();

while (cursor) {
  console.log(cursor.key, cursor.value);
  cursor = await cursor.continue();
}

// Cursor com range
import { IDBKeyRange } from 'idb'; // não precisa importar — é global

// Produtos com preço entre 10 e 100
const tx2 = db.transaction('produtos', 'readonly');
const index = tx2.store.index('preco');
let cursor2 = await index.openCursor(IDBKeyRange.bound(10, 100));

while (cursor2) {
  console.log(cursor2.value);
  cursor2 = await cursor2.continue();
}

// Outros ranges
IDBKeyRange.only(42);             // exatamente 42
IDBKeyRange.lowerBound(10);       // >= 10
IDBKeyRange.upperBound(100);      // <= 100
IDBKeyRange.bound(10, 100, false, true); // 10 <= x < 100 (exclusive upper)
```

---

## Transações explícitas

Para operações que precisam ser atômicas:

```javascript
// Transferência entre stores (precisa de uma única transaction)
async function transferStock(fromId, toId, quantity) {
  const tx = db.transaction('estoque', 'readwrite');
  
  const from = await tx.store.get(fromId);
  const to = await tx.store.get(toId);
  
  if (from.quantidade < quantity) {
    tx.abort(); // rollback explícito
    throw new Error('Estoque insuficiente');
  }
  
  await tx.store.put({ ...from, quantidade: from.quantidade - quantity });
  await tx.store.put({ ...to, quantidade: to.quantidade + quantity });
  
  await tx.done; // aguardar commit
}
```

---

## Padrão: cache offline com IndexedDB

```javascript
class ProductCache {
  constructor(db) {
    this.db = db;
  }

  async getOrFetch(category) {
    // 1. Tentar do cache
    const cached = await this.db.getAllFromIndex('products', 'category', category);
    
    if (cached.length > 0) {
      return cached;
    }
    
    // 2. Buscar da rede
    try {
      const response = await fetch(`/api/products?category=${category}`);
      const products = await response.json();
      
      // 3. Salvar no cache
      const tx = this.db.transaction('products', 'readwrite');
      await Promise.all([
        ...products.map(p => tx.store.put(p)),
        tx.done,
      ]);
      
      return products;
    } catch (error) {
      if (cached.length > 0) return cached; // fallback ao cache antigo
      throw error;
    }
  }

  async invalidate(category) {
    const tx = this.db.transaction('products', 'readwrite');
    const index = tx.store.index('category');
    let cursor = await index.openCursor(IDBKeyRange.only(category));
    
    while (cursor) {
      await cursor.delete();
      cursor = await cursor.continue();
    }
  }
}
```

---

## Versioning e migrações

```javascript
const db = await openDB('meu-banco', 3, {
  upgrade(db, oldVersion, newVersion, transaction) {
    // Migrações encadeadas — cada case cai no próximo (sem break)
    switch (oldVersion) {
      case 0:
        // banco novo
        db.createObjectStore('users', { keyPath: 'id' });
        // cai para case 1
      case 1:
        // adicionar índice que não existia na v1
        transaction.objectStore('users').createIndex('email', 'email', { unique: true });
        // cai para case 2
      case 2:
        // v2 → v3: adicionar novo store
        db.createObjectStore('sessions', { keyPath: 'token' });
    }
  },
});
```

---

> [!question] Para fixar
> 1. Qual a diferença entre `add()` e `put()` no IndexedDB?
> 2. Por que toda operação IndexedDB precisa estar dentro de uma transaction?
> 3. O que acontece se você não chamar `tx.done` ou `tx.abort()` explicitamente?
> 4. Quando você usaria IndexedDB em vez de localStorage?
> 5. Como você faria uma query de "todos os produtos da categoria 'roupas' com preço abaixo de R$100"?

---

## Veja também

- [[03-Dominios/Tecnologia/Plataforma Web/Storage/01 - Cookies e Web Storage|01 — Cookies e Web Storage]] — anterior
- [[03-Dominios/Tecnologia/Plataforma Web/Storage/03 - Cache API e offline-first|03 — Cache API e offline-first]] — próxima
- [[03-Dominios/Tecnologia/Plataforma Web/Workers/03 - Service Workers e ciclo de vida|Workers 03 — Service Workers]] — Cache API integrada ao Service Worker
