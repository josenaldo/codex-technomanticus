---
title: "Promises por dentro"
created: 2026-05-07
updated: 2026-05-07
type: concept
status: seedling
publish: true
tags:
  - node
  - event-loop
  - promise
  - microtask
aliases:
  - Promise mechanics
  - Promise internals
---

# Promises por dentro

> [!abstract] TL;DR
> Uma Promise tem 3 estados: **pending**, **fulfilled** e **rejected**. Uma vez liquidada (settled), é imutável — não pode voltar a pending nem mudar de estado. `.then(cb)` não executa `cb` imediatamente: enfileira `cb` na microtask queue, mesmo que a promise já esteja resolvida. Encadeamento de `.then` devolve uma **nova** promise a cada chamada; erros propagam automaticamente até o primeiro `.catch`. `Promise.resolve(x)` é açúcar sintático para criar uma promise já fulfillada — equivalente a `new Promise((res) => res(x))`, mas mais legível. Em Node.js, promises rejeitadas sem handler disparam o evento `unhandledRejection`; no Node 15+ o padrão passou a terminar o processo.

## O que é

Uma **Promise** é um objeto que representa o resultado eventual de uma operação assíncrona. Ela age como um proxy: você não tem o valor ainda, mas tem um objeto ao qual pode encadear handlers que serão executados quando o valor chegar (ou quando a operação falhar).

### Os três estados

```
pending ──── resolve(v) ───▶ fulfilled (imutável, valor = v)
pending ──── reject(e)  ───▶ rejected  (imutável, reason = e)
```

Uma promise **liquidada** (settled) é toda promise que não está mais em pending — seja ela fulfilled ou rejected. A especificação garante que, após atingir qualquer um dos estados finais, a promise **nunca** muda. Isso torna promises seguras para múltiplos consumidores: você pode chamar `.then()` dezenas de vezes na mesma promise e cada handler recebe o mesmo valor.

O termo **resolved** (resolvida) tem um significado técnico mais sutil: uma promise está "resolved" quando sua trajetória foi fixada — seja com um valor direto, seja "seguindo" outra promise (thenable). Uma promise pode estar resolved mas ainda pending, se ela foi resolvida com outra promise que ainda não liquidou.

### O executor e sua execução síncrona

```javascript
const p = new Promise((resolve, reject) => {
  // Este bloco executa AGORA, de forma síncrona
  console.log('executor rodando');
  resolve(42);
});

console.log('depois do new Promise');
// Output:
// executor rodando
// depois do new Promise
```

O executor roda síncronamente dentro do construtor — é o único ponto síncrono da API de Promise. O que acontece depois de `resolve()` ou `reject()` é que os handlers registrados com `.then()` são **enfileirados como microtasks** — e microtasks só rodam após o código síncrono atual terminar.

### O `.then()` e a microtask queue

A propriedade mais importante e mais mal-compreendida das Promises:

```javascript
const p = new Promise((resolve) => resolve(42));

p.then((v) => console.log('then:', v));
console.log('síncrono');

// Output:
// síncrono
// then: 42
```

Mesmo que `p` já esteja fulfillada no momento em que `.then()` é chamado, o callback **não roda imediatamente**. Ele é enfileirado na microtask queue e só executa depois que todo o código síncrono do stack frame atual terminar. Isso é uma garantia da spec — handlers de Promise são sempre assíncronos, sem exceção.

Isso significa que o modelo de execução de Promises é previsível: você nunca precisa se perguntar se um `.then()` vai rodar agora ou depois. A resposta é sempre "depois do síncrono atual".

### Encadeamento — cada `.then()` retorna uma nova promise

```javascript
const p1 = Promise.resolve(1);

const p2 = p1.then((v) => v + 1);   // p2 é uma NOVA promise
const p3 = p2.then((v) => v * 2);   // p3 é outra promise nova

p3.then((v) => console.log(v));     // 4
```

Cada chamada a `.then()` cria e retorna uma promise nova. O estado dessa nova promise depende do que o handler retorna:

| O handler...                   | A nova promise...                     |
| ------------------------------ | ------------------------------------- |
| Retorna um valor primitivo `v` | É fulfillada com `v`                  |
| Retorna outra promise `q`      | Segue o estado de `q` (torna-se `q`)  |
| Lança uma exceção              | É rejeitada com o erro                |
| Não tem handler para esse lado | Propaga o mesmo estado da promise pai |

Essa última linha é o mecanismo de propagação de erros: se uma promise rejeitada não tem handler de rejeição em um `.then()`, a rejeição passa adiante — como uma exceção não capturada que sobe a pilha.

## Por que importa

Promises são a fundação de toda a programação assíncrona moderna em JavaScript. `async/await` é syntactic sugar sobre Promises — um `await expr` é essencialmente um `.then()` em `expr`, com a diferença que o resto da função async é o callback.

Sem entender que `.then()` enfileira microtasks (não executa imediatamente), você vai criar bugs sutis de ordem de execução — especialmente ao misturar código síncrono com código async em testes ou em inicialização de serviços.

Sem entender que cada `.then()` retorna uma promise nova, você vai esquecer `return` dentro de chains e criar promises soltas que propagam erros silenciosamente — um dos bugs mais difíceis de debugar em codebases JavaScript.

## Como funciona

### 1. Estados e imutabilidade

```javascript
const p = new Promise((resolve, reject) => {
  resolve(42);
  reject(new Error('ignorado')); // sem efeito — já resolvida
  resolve(99);                   // sem efeito — já resolvida
});

p.then((v) => console.log(v)); // 42
```

Após a primeira chamada a `resolve()`, qualquer chamada subsequente — seja `resolve()` ou `reject()` — é silenciosamente ignorada. Isso é parte do contrato da Promise.

### 2. Encadeamento com transformações

```javascript
Promise.resolve(2)
  .then((v) => v + 1)     // 3
  .then((v) => v * 2)     // 6
  .then((v) => {
    console.log(v);        // 6
    return v;
  });
```

Cada `.then()` recebe o resultado do anterior e pode transformá-lo. A chain é lazy: os callbacks só rodam quando cada promise predecessora liquida.

### 3. Propagação de erros

```javascript
Promise.resolve('ok')
  .then(() => {
    throw new Error('algo deu errado');
  })
  .then(() => {
    console.log('este nunca roda');
  })
  .catch((e) => {
    console.log('capturado:', e.message); // capturado: algo deu errado
  })
  .then(() => {
    console.log('continua após o catch'); // roda normalmente
  });
```

Erros pulam todos os `.then()` intermediários que não têm handler de rejeição, e são capturados pelo primeiro `.catch()`. Após o `.catch()` completar sem lançar, a chain retorna ao estado fulfilled — o `.then()` seguinte ao `.catch()` executa normalmente.

Para rejeitar a chain após um `.catch()`, basta relançar o erro:

```javascript
.catch((e) => {
  logger.error(e);
  throw e; // mantém a rejeição propagando
})
```

### 4. `Promise.resolve(x)` vs `new Promise((res) => res(x))`

```javascript
// Equivalentes na prática
const p1 = Promise.resolve(42);
const p2 = new Promise((resolve) => resolve(42));

// Promise.resolve com thenable — segue o estado
const p3 = Promise.resolve(fetch('/api/data')); // mesma coisa que fetch('/api/data')
```

`Promise.resolve(x)` é idiomático para normalizar um valor que pode ser síncrono ou uma promise. Se `x` já é uma Promise nativa, o runtime retorna `x` diretamente sem criar uma nova promise — otimização garantida pela spec.

### 5. Anti-pattern: Promise constructor desnecessário

```javascript
// RUIM — "Promise constructor anti-pattern"
async function getData(url) {
  return new Promise((resolve, reject) => {
    fetch(url)
      .then((res) => resolve(res))
      .catch((err) => reject(err));
  });
}

// BOM — fetch já retorna uma Promise
async function getData(url) {
  return fetch(url);
}
```

Envolver uma promise em outra promise com o construtor é redundante e perigoso: se o código dentro do executor lançar uma exceção síncrona antes de chamar `reject()`, você perde o erro — ele vira uma rejeição não tratada invisível. Use o construtor apenas quando estiver adaptando uma API baseada em callbacks.

### 6. Deferred pattern — válido, mas evite como padrão

O "deferred pattern" extrai `resolve` e `reject` para fora do executor, criando um objeto que terceiros podem resolver:

```javascript
function createDeferred() {
  let resolve, reject;
  const promise = new Promise((res, rej) => {
    resolve = res;
    reject = rej;
  });
  return { promise, resolve, reject };
}

// Uso
const deferred = createDeferred();

// Em algum lugar do código
deferred.resolve(42);

// Em outro lugar
deferred.promise.then((v) => console.log(v));
```

Esse padrão tem usos legítimos — coordenação entre sistemas, testes que precisam de controle externo sobre resolução. Mas como padrão geral é um smell: indica que a lógica de resolução deveria estar encapsulada na própria promise, não vazada para fora.

### 7. `unhandledRejection` em Node.js

Quando uma promise é rejeitada e nenhum handler de rejeição é registrado dentro de um tick do event loop, o Node.js emite o evento `unhandledRejection` no objeto `process`:

```javascript
process.on('unhandledRejection', (reason, promise) => {
  console.error('Promise rejeitada sem handler:', reason);
  console.error('Promise:', promise);
  // Em produção: exportar para o sistema de logging/alertas
});
```

O comportamento padrão evoluiu ao longo das versões do Node:

| Versão      | Comportamento padrão                            |
| ----------- | ----------------------------------------------- |
| Node < 15   | Aviso no stderr, processo continua              |
| Node 15+    | Termina o processo com exit code não-zero       |
| Node 22+    | Termina o processo (mesmo comportamento)        |

Terminar o processo é o comportamento correto para a maioria dos cenários de produção: uma promise rejeitada sem handler indica um estado inesperado que o código não sabe tratar — continuar rodando nesse estado é perigoso.

O flag `--unhandled-rejections` permite controlar o comportamento explicitamente:

```bash
node --unhandled-rejections=throw app.js   # lança exceção (padrão Node 15+)
node --unhandled-rejections=warn  app.js   # aviso apenas (legado)
node --unhandled-rejections=none  app.js   # silencia completamente (perigoso)
```

> [!warning] Nunca silenciar `unhandledRejection` em produção
> `--unhandled-rejections=none` ou engolir o evento sem logar é uma forma garantida de criar bugs fantasma — erros que ocorrem silenciosamente sem deixar rastro. Sempre logue o `reason` com contexto suficiente para investigação posterior.

## Na prática

### Normalização de APIs value-or-promise

Libs que aceitam tanto valores síncronos quanto promises usam `Promise.resolve()` para normalizar:

```javascript
async function processInput(input) {
  // input pode ser um valor ou uma promise — não importa
  const value = await Promise.resolve(input);
  return transform(value);
}
```

Isso evita que o chamador precise saber se a função retorna síncronamente ou não.

### Handler de `unhandledRejection` em produção

Em aplicações Node.js de produção, o handler global é sempre presente e exporta para o sistema de logging:

```javascript
process.on('unhandledRejection', (reason, promise) => {
  logger.error({
    event: 'unhandled_rejection',
    reason: reason instanceof Error ? reason.stack : String(reason),
  });
  // Deixar o processo terminar — o process manager (PM2, systemd) vai reiniciar
});
```

### Fire and forget — quando é aceitável

Em casos onde a rejeição é genuinamente irrelevante (operações de melhor esforço, side effects não críticos), `void` documenta a intenção:

```javascript
// void comunica que a rejeição foi considerada e deliberadamente ignorada
void updateAnalyticsCache(userId);

// Melhor ainda: trate internamente na própria função
async function updateAnalyticsCache(userId) {
  try {
    await cache.set(userId, await fetchAnalytics(userId));
  } catch (e) {
    logger.warn('analytics cache update failed', { userId, error: e });
    // Falha silenciosa intencional, com log
  }
}
```

`void` sem `.catch()` interno ainda vai disparar `unhandledRejection` se a promise rejeitar. O padrão correto é sempre tratar internamente quando fire-and-forget for necessário.

### `Promise.all([])` e casos extremos

```javascript
Promise.all([])
  .then((results) => console.log(results)); // []

// Promise.all falha rápido — rejeita no primeiro erro
Promise.all([
  Promise.resolve(1),
  Promise.reject(new Error('falhou')),
  Promise.resolve(3),
]).catch((e) => console.log(e.message)); // 'falhou'
// Os outros valores (1, 3) são descartados silenciosamente

// Promise.allSettled aguarda todos — nunca rejeita
Promise.allSettled([
  Promise.resolve(1),
  Promise.reject(new Error('falhou')),
]).then((results) => console.log(results));
// [
//   { status: 'fulfilled', value: 1 },
//   { status: 'rejected', reason: Error('falhou') }
// ]
```

## Armadilhas

### 1. Esquecer `return` dentro de `.then()`

```javascript
// RUIM — retorna undefined; a promise interna não é encadeada
fetchUser(id)
  .then((user) => {
    fetchPermissions(user.id); // promise solta — sem return!
  })
  .then((permissions) => {
    console.log(permissions); // undefined, não as permissões
  });

// BOM
fetchUser(id)
  .then((user) => {
    return fetchPermissions(user.id); // encadeia corretamente
  })
  .then((permissions) => {
    console.log(permissions); // os dados corretos
  });
```

Sem `return`, a promise retornada por `fetchPermissions` flutua solta — ela executa, mas o resultado é descartado e erros viram `unhandledRejection`.

### 2. `await Promise.resolve(syncFn())` — a função síncrona já rodou

```javascript
// syncFn() executa AGORA, de forma síncrona
// O await só suspende na resolução da promise — que já está resolvida
const result = await Promise.resolve(computeHeavySync());

// Equivalente a:
const syncResult = computeHeavySync(); // bloqueia aqui
const result = await Promise.resolve(syncResult); // suspende aqui (mas a promise já resolveu)
```

Envolver uma função síncrona pesada em `Promise.resolve()` não a move para fora da thread principal. Se você precisa de verdadeira assincronicidade, use `worker_threads` ou `setImmediate`.

### 3. `Promise.all([])` resolve com array vazio, não rejeita

```javascript
// Comportamento correto, mas surpreende quem não conhece
const results = await Promise.all([]);
// results === [] — não é erro, não é undefined
```

Isso é útil quando você constrói a lista de promises dinamicamente e ela pode estar vazia.

### 4. Tratar `unhandledRejection` sem logar

```javascript
// PÉSSIMO — engole o erro completamente
process.on('unhandledRejection', () => {
  // "tratei" o evento mas não fiz nada
});

// Resultado: bugs fantasma — erros que ocorrem silenciosamente
// em produção sem deixar rastro nos logs
```

"Tratar" o evento sem logar é pior do que não tratar: o processo não vai mais terminar (comportamento pre-Node 15), mas os erros também não vão aparecer em nenhum lugar. Você tem o pior dos dois mundos.

### 5. Promise no `if` sem await

```javascript
// Esse código nunca rejeita visível — mas também nunca espera
if (await validateUser(id)) { // await correto
  await saveToDatabase(record); // sem await — fire and forget acidental
}
```

Qualquer chamada a uma função `async` sem `await` (e sem captura da promise retornada) é potencialmente um `unhandledRejection` esperando acontecer.

## Em entrevista

> [!quote] Frase pronta (use em inglês)
> "A Promise has three states: pending, fulfilled, and rejected — once settled, it's immutable. `.then` doesn't run synchronously; it queues the callback in the microtask queue, even if the promise is already resolved. Chained `.then` calls return new promises, so errors propagate down the chain until the first `.catch`. The unhandled rejection handler in Node logs the error and, by default in modern versions, terminates the process — which is the right behavior for unrecoverable bugs."

### Perguntas frequentes

**"Por que `.then()` é sempre assíncrono, mesmo para promises já resolvidas?"**
Para garantir comportamento previsível e composição correta. Se `.then()` às vezes rodasse síncronamente, o código teria que lidar com dois modelos de execução dependendo do estado da promise — exatamente o problema que Promises foram criadas para resolver.

**"Qual a diferença entre `Promise.resolve(p)` onde `p` já é uma Promise?"**
Se `p` é uma Promise nativa, `Promise.resolve(p)` retorna `p` sem criar uma nova promise. Se `p` é um thenable de terceiros, cria uma nova promise que segue `p`.

**"Quando usar `Promise.allSettled` em vez de `Promise.all`?"**
`Promise.all` é para "preciso de todos os resultados ou quero falhar rápido". `Promise.allSettled` é para "quero saber o resultado de cada operação independentemente, sem que uma falha cancele as outras".

### Vocabulário para entrevistas

| PT-BR                              | EN                         |
| ---------------------------------- | -------------------------- |
| estado (pending, fulfilled, etc.)  | state / status             |
| liquidada / resolvida              | settled                    |
| encadear                           | chain / pipe               |
| rejeição não tratada               | unhandled rejection        |
| fila de microtasks                 | microtask queue / job queue|
| executor                           | executor function          |
| propagar erro                      | propagate / bubble up      |
| açúcar sintático                   | syntactic sugar            |
| promessa solta                     | floating promise           |

## Veja também

- `[[03 - Call stack, heap e queues]]` — a microtask queue no contexto do event loop
- `[[05 - Microtasks - nextTick, queueMicrotask, Promise.then]]` — ordem de execução de microtasks e comparação com `process.nextTick`
- `[[09 - async-await - o que é, o que não é]]` — como `async/await` é sugar sobre Promises
- `[[Node.js]]` — nota-tronco do domínio Node.js
