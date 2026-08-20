---
title: "Cookies e Web Storage"
created: 2026-06-28
updated: 2026-06-28
type: note
fase: iniciado
tags:
  - plataforma-web
  - storage
  - browser
  - javascript
  - cookies
  - entrevista
publish: true
---

# Cookies e Web Storage

> [!abstract] TL;DR
> O browser oferece três mecanismos de armazenamento simples: cookies (enviados ao servidor em cada request; criptográficos com `HttpOnly`/`Secure`/`SameSite`), `localStorage` (persistente, ~5-10MB, síncrono) e `sessionStorage` (limpo ao fechar a aba, ~5-10MB, síncrono). Para dados estruturados grandes ou offline, use IndexedDB. Para assets cacheados, use Cache API (Service Worker).

---

## Comparativo geral

| | Cookies | localStorage | sessionStorage | IndexedDB |
|---|---|---|---|---|
| Capacidade | 4KB | ~5-10MB | ~5-10MB | Centenas de MB |
| Enviado ao servidor | Sim (automático) | Não | Não | Não |
| Escopo | Domínio + caminho | Origem | Aba + origem | Origem |
| Persistência | Configurável | Até limpar | Fecha a aba | Até limpar |
| API | Síncrona (string) | Síncrona (string) | Síncrona (string) | Assíncrona |
| Acesso via JS | Configurável (HttpOnly) | Sim | Sim | Sim |

---

## localStorage e sessionStorage

```javascript
// Ambos têm a mesma API — só diferem em escopo/persistência

// Escrever (sempre serializado como string)
localStorage.setItem('user', JSON.stringify({ name: 'Alice', role: 'admin' }));
localStorage.setItem('count', '42');

// Ler
const raw = localStorage.getItem('user');      // string ou null
const user = raw ? JSON.parse(raw) : null;

// Verificar existência
localStorage.getItem('key') !== null;

// Remover
localStorage.removeItem('user');

// Limpar tudo
localStorage.clear();

// Iterar sobre todas as chaves
for (let i = 0; i < localStorage.length; i++) {
  const key = localStorage.key(i);
  const value = localStorage.getItem(key);
  console.log(key, value);
}

// ou usando spread (não é iterável diretamente)
Object.entries(localStorage).forEach(([key, value]) => console.log(key, value));
```

---

## Armadilhas do Web Storage

```javascript
// ❌ Salvar objeto sem JSON.stringify — vira "[object Object]"
localStorage.setItem('user', { name: 'Alice' }); // "[object Object]"

// ❌ Assumir que localStorage existe sempre
// Safari em modo privado bloqueia com quota exceeded

// ✅ Wrapper seguro
const storage = {
  set(key, value) {
    try {
      localStorage.setItem(key, JSON.stringify(value));
    } catch (e) {
      console.warn('localStorage indisponível:', e);
    }
  },
  get(key, defaultValue = null) {
    try {
      const raw = localStorage.getItem(key);
      return raw !== null ? JSON.parse(raw) : defaultValue;
    } catch (e) {
      return defaultValue;
    }
  },
  remove(key) {
    try { localStorage.removeItem(key); } catch {}
  }
};
```

---

## Evento `storage` — sincronizar entre abas

```javascript
// Dispara em OUTRAS abas da mesma origem quando localStorage muda
window.addEventListener('storage', (event) => {
  event.key;         // chave alterada (null se foi .clear())
  event.oldValue;    // valor anterior (string ou null)
  event.newValue;    // novo valor (string ou null; null se foi removido)
  event.url;         // URL da aba que fez a mudança
  event.storageArea; // localStorage ou sessionStorage
  
  if (event.key === 'cart') {
    syncCart(JSON.parse(event.newValue ?? '[]'));
  }
});
```

> [!warning] Não dispara na própria aba
> O evento `storage` só é disparado em outras abas/janelas — não na que fez a mudança. Para comunicação na mesma aba, use variáveis normais ou eventos customizados. Para comunicação entre abas mais robusta, veja BroadcastChannel (nota Workers 02).

---

## Cookies

Cookies são enviados automaticamente em cada HTTP request — ideal para autenticação (session token). Mas têm apenas 4KB e não devem armazenar dados sensíveis sem `HttpOnly`.

```javascript
// API de cookies é minimalista e inconveniente
// Ler todos os cookies (como string "key=val; key2=val2")
document.cookie; // não tem getter por chave!

// Escrever um cookie (NÃO substitui todos — adiciona/atualiza o especificado)
document.cookie = 'nome=Alice; max-age=3600; path=/; samesite=strict';

// Parser manual
function getCookie(name) {
  return document.cookie
    .split('; ')
    .find(row => row.startsWith(name + '='))
    ?.split('=')[1];
}

// Deletar (setar max-age=0 ou data no passado)
document.cookie = 'nome=; max-age=0; path=/';
```

---

## Atributos de cookies importantes

```javascript
document.cookie = [
  'session=abc123',
  'max-age=86400',          // segundos; ou: 'expires=Fri, 31 Dec 2026 23:59:59 GMT'
  'path=/',                 // path que pode ler o cookie (padrão: path atual)
  'domain=.exemplo.com',    // subdomínios inclusos (atenção: Cross-Site)
  'secure',                 // só HTTPS
  'samesite=strict',        // 'strict' | 'lax' | 'none'
].join('; ');
```

| Atributo | Efeito |
|---|---|
| `HttpOnly` | Só acessível pelo servidor (via `Set-Cookie` header), JS não lê — proteção XSS |
| `Secure` | Só enviado em HTTPS |
| `SameSite=Strict` | Nunca enviado em requests cross-site |
| `SameSite=Lax` | Enviado em navegação top-level; bloqueado em requests cross-site silenciosos |
| `SameSite=None; Secure` | Enviado sempre (cookies de terceiros) — exige Secure |
| `max-age=0` | Apagar o cookie |

> [!info] Cookie Store API (moderno)
> A **Cookie Store API** (`cookieStore`) oferece uma interface async e ergonômica — substitui `document.cookie`:
> ```javascript
> await cookieStore.set({ name: 'user', value: 'Alice', maxAge: 3600 });
> const cookie = await cookieStore.get('user');
> await cookieStore.delete('user');
> ```
> Suporte crescente (Chrome 87+, mas não Firefox ainda em 2024).

---

## Quando usar o quê

```
Precisa ser enviado ao servidor? → Cookie (com HttpOnly + SameSite)
Dado simples, pequeno, persistente? → localStorage (com JSON.stringify/parse)
Dado de sessão (limpar ao fechar aba)? → sessionStorage
Dados estruturados, grandes, ou queries? → IndexedDB
Assets para uso offline? → Cache API (Service Worker)
```

---

> [!question] Para fixar
> 1. Por que cookies são enviados automaticamente ao servidor mas localStorage não?
> 2. O que acontece se você salvar um objeto no localStorage sem `JSON.stringify`?
> 3. O evento `storage` dispara na aba que fez a mudança? Como isso afeta o design?
> 4. O que `SameSite=Strict` faz? Quando você usaria `SameSite=Lax`?
> 5. Por que `HttpOnly` protege contra XSS? O que um script malicioso poderia fazer sem esse atributo?

---

## Veja também

- [[03-Dominios/Tecnologia/Plataforma Web/Storage/02 - IndexedDB|02 — IndexedDB]] — próxima
- [[03-Dominios/Tecnologia/Plataforma Web/Networking/03 - HTTP no cliente|Networking 03 — HTTP no cliente]] — cookies em requests HTTP
- [[03-Dominios/Tecnologia/Plataforma Web/Storage/index|Storage — índice]]
