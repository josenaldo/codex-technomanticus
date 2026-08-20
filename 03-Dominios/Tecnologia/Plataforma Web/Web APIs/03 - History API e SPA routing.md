---
title: "History API e SPA routing"
created: 2026-06-28
updated: 2026-06-28
type: note
fase: iniciado
tags:
  - plataforma-web
  - web-apis
  - browser
  - javascript
  - spa
  - routing
  - entrevista
publish: true
---

# History API e SPA routing

> [!abstract] TL;DR
> A History API permite manipular o histórico de navegação sem recarregar a página — a base do routing em SPAs. `pushState` adiciona uma entrada ao histórico; `replaceState` substitui a atual; `popstate` dispara quando o usuário volta/avança. Junto com a URL API (`URL`, `URLSearchParams`), essas são as primitivas sobre as quais React Router, Vue Router e outros frameworks são construídos.

---

## History API

```javascript
// Estado atual
window.history.length;       // número de entradas no histórico
window.history.state;        // estado da entrada atual

// Navegar
history.back();              // mesmo que o botão ← do browser
history.forward();           // mesmo que o botão →
history.go(-2);              // 2 passos para trás
history.go(1);               // 1 passo para frente

// Adicionar entrada ao histórico (não recarrega a página)
history.pushState(state, title, url);

// Substituir entrada atual (não cria nova entrada no histórico)
history.replaceState(state, title, url);
```

---

## `pushState` vs `replaceState`

```javascript
// pushState: usuário pode voltar para esta URL
history.pushState(
  { page: 'product', id: 42 },  // state: objeto serializable (max ~2MB)
  '',                            // title: ignorado pela maioria dos browsers
  '/produtos/42'                 // URL: mesma origem, relativa ou absoluta
);

// replaceState: substitui a entrada atual — não cria nova
// Útil para: atualizar URL sem criar nova entrada (filtros, paginação)
history.replaceState(
  { filters: { color: 'blue', size: 'M' } },
  '',
  '/produtos?color=blue&size=M'
);
```

> [!warning] Restrição de origem
> `pushState` e `replaceState` só permitem URLs da mesma origem. Tentar mudar para outro domínio lança `SecurityError`.

---

## `popstate` — reagir ao botão voltar/avançar

O evento `popstate` dispara quando o usuário navega pelo histórico (botão voltar, botão avançar, `history.go()`). Não dispara em `pushState`/`replaceState`.

```javascript
window.addEventListener('popstate', (event) => {
  // event.state: o objeto passado para pushState/replaceState
  const state = event.state;
  
  if (state?.page === 'product') {
    renderProduct(state.id);
  } else {
    renderHome();
  }
});
```

---

## Roteador SPA mínimo

```javascript
const routes = {
  '/': () => render('<h1>Home</h1>'),
  '/sobre': () => render('<h1>Sobre</h1>'),
  '/contato': () => render('<h1>Contato</h1>'),
};

function navigate(path) {
  history.pushState({ path }, '', path);
  route(path);
}

function route(path) {
  const handler = routes[path] ?? routes['/'];
  handler();
}

function render(html) {
  document.getElementById('app').innerHTML = html;
}

// Interceptar cliques em links internos (event delegation)
document.addEventListener('click', (event) => {
  const link = event.target.closest('a[href]');
  if (!link) return;
  
  const url = new URL(link.href);
  if (url.origin !== location.origin) return; // link externo, deixar browser agir
  
  event.preventDefault();
  navigate(url.pathname);
});

// Reagir ao botão voltar/avançar
window.addEventListener('popstate', (event) => {
  route(location.pathname);
});

// Roteamento inicial ao carregar a página
route(location.pathname);
```

---

## URL API

Trabalhar com URLs de forma segura — sem concatenação de strings:

```javascript
const url = new URL('https://exemplo.com/produtos?color=blue&page=2#reviews');

url.href;        // 'https://exemplo.com/produtos?color=blue&page=2#reviews'
url.origin;      // 'https://exemplo.com'
url.protocol;    // 'https:'
url.host;        // 'exemplo.com'
url.hostname;    // 'exemplo.com' (sem porta)
url.port;        // '' (ou '3000' se houver)
url.pathname;    // '/produtos'
url.search;      // '?color=blue&page=2'
url.searchParams; // URLSearchParams
url.hash;        // '#reviews'

// URL relativa com base
const pageUrl = new URL('/sobre', 'https://exemplo.com');
pageUrl.href; // 'https://exemplo.com/sobre'

// URL com a URL atual como base
const currentUrl = new URL(location.href);
```

---

## URLSearchParams

```javascript
// Criar a partir de string de query
const params = new URLSearchParams('color=blue&size=M&size=L');

// Criar a partir de objeto
const params2 = new URLSearchParams({ color: 'blue', page: '2' });

// Ler
params.get('color');          // 'blue'
params.get('size');           // 'M' (primeiro valor)
params.getAll('size');        // ['M', 'L'] (todos os valores)
params.has('color');          // true
params.has('weight');         // false

// Iterar
for (const [key, value] of params) {
  console.log(key, value);
}
params.forEach((value, key) => console.log(key, value));

// Modificar (retorna void — muta o objeto)
params.set('color', 'red');   // substitui todos os valores de 'color'
params.append('size', 'XL'); // adiciona sem remover existentes
params.delete('color');       // remove todos os valores de 'color'

// Serializar
params.toString(); // 'size=M&size=L&size=XL'

// A partir da URL atual
const currentParams = new URLSearchParams(location.search);

// Atualizar URL sem recarregar
const url = new URL(location.href);
url.searchParams.set('page', '3');
history.pushState({}, '', url.toString());
```

---

## Padrão: filtros e paginação via URL

Sincronizar estado de filtros com a URL é uma boa prática — permite compartilhar URLs e usar botão voltar:

```javascript
class ProductFilter {
  constructor() {
    this.container = document.getElementById('products');
    
    // Carregar estado inicial da URL
    this.loadFromURL();
    
    // Reagir ao botão voltar/avançar
    window.addEventListener('popstate', () => this.loadFromURL());
    
    // Reagir a mudanças de filtro
    document.getElementById('filters').addEventListener('change', (e) => {
      if (e.target.name) this.updateFilter(e.target.name, e.target.value);
    });
  }

  loadFromURL() {
    const params = new URLSearchParams(location.search);
    this.filters = {
      category: params.get('category') ?? 'all',
      sort: params.get('sort') ?? 'relevance',
      page: parseInt(params.get('page') ?? '1', 10),
    };
    this.render();
  }

  updateFilter(key, value) {
    this.filters[key] = value;
    this.filters.page = 1; // reset paginação ao filtrar
    this.syncToURL();
    this.render();
  }

  syncToURL() {
    const params = new URLSearchParams();
    if (this.filters.category !== 'all') params.set('category', this.filters.category);
    if (this.filters.sort !== 'relevance') params.set('sort', this.filters.sort);
    if (this.filters.page > 1) params.set('page', String(this.filters.page));
    
    const search = params.toString();
    const url = search ? `?${search}` : location.pathname;
    
    history.pushState({ filters: this.filters }, '', url);
  }

  render() {
    // Buscar e exibir produtos com this.filters
    fetchProducts(this.filters).then(products => {
      this.container.innerHTML = products.map(renderProduct).join('');
    });
  }
}
```

---

## `hashchange` — roteamento por hash (legado)

Antes da History API, SPAs usavam hashes (`#/rota`) para routing — não recarrega a página e funciona sem configuração de servidor:

```javascript
// Hash-based routing (abordagem legada)
window.addEventListener('hashchange', () => {
  const path = location.hash.slice(1) || '/'; // '#/sobre' → '/sobre'
  route(path);
});

// Navegar
location.hash = '/sobre'; // dispara hashchange
```

**Quando usar hash routing:** apenas se o servidor não puder ser configurado para servir `index.html` em todas as rotas. Em produção com servidor próprio, sempre prefira `pushState`.

---

> [!question] Para fixar
> 1. Qual a diferença entre `pushState` e `replaceState`? Quando você usaria cada um?
> 2. O evento `popstate` dispara quando você chama `history.pushState()`? Quando ele dispara?
> 3. Como você construiria um roteador SPA mínimo sem nenhuma biblioteca?
> 4. Por que usar `new URL(link.href)` em vez de comparar `link.href` com strings?
> 5. Qual é a diferença entre `params.get('size')` e `params.getAll('size')` quando há múltiplos valores?

---

## Veja também

- [[03-Dominios/Tecnologia/Plataforma Web/Web APIs/02 - MutationObserver e ResizeObserver|02 — MutationObserver e ResizeObserver]] — anterior
- [[03-Dominios/Tecnologia/Plataforma Web/Web APIs/04 - Clipboard e File API|04 — Clipboard e File API]] — próxima
- [[03-Dominios/Tecnologia/Plataforma Web/Eventos/04 - Event delegation|Eventos 04 — Event delegation]] — `closest()` para interceptar cliques em links
