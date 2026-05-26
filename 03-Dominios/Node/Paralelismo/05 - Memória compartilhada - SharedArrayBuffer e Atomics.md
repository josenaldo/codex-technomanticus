---
title: "Memória compartilhada: SharedArrayBuffer e Atomics"
created: 2026-05-07
updated: 2026-05-07
type: concept
status: seedling
publish: true
tags:
  - node
  - paralelismo
  - worker-threads
  - sharedarraybuffer
  - atomics
  - concurrency
aliases:
  - SharedArrayBuffer
  - SAB
  - Atomics
  - Race conditions em JS
---

# Memória compartilhada: SharedArrayBuffer e Atomics

> [!abstract] TL;DR
> `SharedArrayBuffer` (SAB) é um buffer visível simultaneamente em múltiplos Workers — diferente de `ArrayBuffer`, que é clonado ou transferido. Uma vez que há memória compartilhada, há risco de race conditions: toda leitura ou escrita precisa passar pelos `Atomics` (`load`, `store`, `add`, `compareExchange` etc.). Para coordenação entre threads, `Atomics.wait` e `Atomics.notify` funcionam como uma variável de condição primitiva — mas `wait` só pode ser chamado dentro de workers, nunca no main thread. Casos legítimos: matrizes grandes em ML/processamento de imagem, contadores compartilhados, semáforos. Na maioria dos casos, prefira mensagens.

---

## O que é

### SharedArrayBuffer

`SharedArrayBuffer` (SAB) é uma variante de `ArrayBuffer` projetada para existir em memória compartilhada entre múltiplas threads de execução. Enquanto um `ArrayBuffer` comum é clonado (cópia de bytes) ou transferido (move a propriedade) ao passar por `postMessage`, um SAB é compartilhado por referência — a mesma região de memória física é acessível em todas as threads que o receberam.

```javascript
// main.js
import { Worker } from 'node:worker_threads';

// Aloca 4 KB de memória compartilhada
const sab = new SharedArrayBuffer(4096);

const w1 = new Worker('./worker.js');
const w2 = new Worker('./worker.js');

// SAB não entra em transferList — não é movido, é compartilhado
w1.postMessage({ sab });
w2.postMessage({ sab });

// Tanto w1 quanto w2 enxergam o mesmo bloco de memória
```

```javascript
// worker.js
import { parentPort } from 'node:worker_threads';

parentPort.once('message', ({ sab }) => {
  // A mesma região de memória alocada no main
  const view = new Int32Array(sab);
  console.log('byteLength:', sab.byteLength); // 4096
});
```

O SAB é acessado por meio de `TypedArray`s que apontam para ele: `Int8Array`, `Uint8Array`, `Int16Array`, `Uint16Array`, `Int32Array`, `Uint32Array`, `BigInt64Array`, `BigUint64Array`, `Float32Array`, `Float64Array`. O `TypedArray` é apenas uma "janela" — o buffer subjacente é o SAB.

```javascript
const sab = new SharedArrayBuffer(16); // 16 bytes

const i32 = new Int32Array(sab);  // 4 inteiros de 32 bits (4 × 4 = 16 bytes)
const u8  = new Uint8Array(sab);  // 16 bytes individuais — mesma memória!

// Qualquer TypedArray sobre o mesmo SAB enxerga os mesmos bytes
i32[0] = 0x01020304;
console.log(u8[0], u8[1], u8[2], u8[3]); // 4 3 2 1 (little-endian em x86)
```

**Desde ES2024**, o SAB pode ser criado com `maxByteLength` para permitir crescimento posterior:

```javascript
const sab = new SharedArrayBuffer(1024, { maxByteLength: 16 * 1024 });
console.log(sab.growable);    // true
console.log(sab.byteLength);  // 1024

sab.grow(4096);
console.log(sab.byteLength);  // 4096
```

O crescimento é seguro e atômico — mas nunca é possível reduzir o tamanho. SABs não-growable têm tamanho fixo para sempre.

---

### Atomics

`Atomics` é um objeto namespace (não um construtor — não existe `new Atomics`) com métodos estáticos que realizam operações atômicas sobre `TypedArray`s que apontam para um `SharedArrayBuffer`. Uma operação atômica é indivisível: do ponto de vista de qualquer outra thread, ela acontece inteiramente ou não acontece — nunca é observada pela metade.

```javascript
const sab = new SharedArrayBuffer(4);
const view = new Int32Array(sab);

// Todas as operações Atomics recebem (typedArray, index, ...)
Atomics.store(view, 0, 42);        // escreve 42 em view[0] atomicamente
const val = Atomics.load(view, 0); // lê view[0] atomicamente → 42
```

Sem `Atomics`, acessos concorrentes ao mesmo índice de um SAB são comportamento indefinido do ponto de vista de linearidade: o compilador JIT e o CPU são livres para reordenar operações, usar registradores em cache, e nunca publicar o valor escrito para as demais threads.

---

## Por que importa

A proposta padrão de comunicação entre workers é `postMessage` com o algoritmo de clone estruturado. Essa abordagem é segura por design — cada thread tem sua própria cópia dos dados, e não há estado compartilhado. O problema aparece em dois cenários específicos:

**1. Custo de cópia em buffers grandes.** Mesmo com `transferList` (zero-copy entre duas threads), um buffer que precisa ser lido por N workers ao mesmo tempo exige N-1 cópias ou N-1 ping-pongs sequenciais. Uma matriz de 500 MB usada por 8 workers para inferência paralela em ML não se distribui bem via mensagens.

**2. Coordenação de baixa latência.** Quando múltiplos workers precisam ler e escrever contadores, flags de controle, ou pequenas estruturas de estado compartilhado, o overhead de serialização + troca de mensagens + agendamento de eventos pode ser maior que o trabalho real. Um contador de progresso atualizado por 16 workers, lido 60 vezes por segundo pelo main thread, é mais eficiente em SAB.

`SharedArrayBuffer` + `Atomics` é a solução de **memória compartilhada de baixo nível em JavaScript** — análoga a `pthreads` com variáveis protegidas por mutex, mas com a API de `Atomics` como primitiva em vez de mutex explícito. A vantagem é eficiência máxima; a desvantagem é que race conditions voltam a ser possíveis.

---

## Como funciona

### A race condition canônica

O exemplo mais simples de race condition: dois workers incrementando um contador compartilhado sem sincronização.

```javascript
// worker.js — CÓDIGO INCORRETO
import { parentPort } from 'node:worker_threads';

parentPort.once('message', ({ sab }) => {
  const view = new Int32Array(sab);

  for (let i = 0; i < 100_000; i++) {
    view[0]++;  // RUIM: read + increment + write são três operações separadas
  }

  parentPort.postMessage('done');
});
```

```javascript
// main.js — demonstração do problema
import { Worker } from 'node:worker_threads';

const sab = new SharedArrayBuffer(4);
const view = new Int32Array(sab);

const workers = [new Worker('./worker.js'), new Worker('./worker.js')];
let done = 0;

for (const w of workers) {
  w.postMessage({ sab });
  w.once('message', () => {
    if (++done === workers.length) {
      console.log(view[0]); // Esperado: 200000. Real: qualquer coisa entre 100001 e 200000.
    }
  });
}
```

O que acontece em `view[0]++`:

1. Thread A lê `view[0]` → obtém 99
2. Thread B lê `view[0]` → obtém 99 (ainda não viu a escrita de A)
3. Thread A escreve 100
4. Thread B escreve 100
5. Resultado: 100 em vez de 101 — um incremento perdido

Isso não é um bug raro ou específico de hardware — é o comportamento esperado quando dois agentes leem e escrevem a mesma posição de memória sem sincronização. Pode acontecer a qualquer momento.

---

### Todas as operações Atomics

`Atomics` oferece três categorias de operações:

**Leitura e escrita simples:**

```javascript
const sab = new SharedArrayBuffer(16);
const view = new Int32Array(sab);

// store: escreve atomicamente, retorna o valor armazenado
Atomics.store(view, 0, 100);   // → 100

// load: lê atomicamente
Atomics.load(view, 0);         // → 100

// exchange: escreve e retorna o VALOR ANTIGO
const old = Atomics.exchange(view, 0, 999); // old = 100; view[0] agora = 999
```

**Aritmética e bits (todas retornam o VALOR ANTIGO):**

```javascript
Atomics.store(view, 0, 10);

Atomics.add(view, 0, 5);   // retorna 10; view[0] agora = 15
Atomics.sub(view, 0, 3);   // retorna 15; view[0] agora = 12
Atomics.and(view, 0, 0b1010); // retorna 12 (0b1100); view[0] = 0b1000 = 8
Atomics.or(view, 0, 0b0011);  // retorna 8;  view[0] = 0b1011 = 11
Atomics.xor(view, 0, 0b1111); // retorna 11; view[0] = 0b0100 = 4
```

> [!warning] `Atomics.add` retorna o valor ANTIGO
> `Atomics.add(view, 0, 1)` se comporta como pós-incremento em C (`val++`): o valor retornado é o que estava antes. O novo valor é `retorno + 1`. Confundir isso com pré-incremento é uma armadilha clássica — especialmente ao usar o retorno para tomar decisões de controle de fluxo.

**Compare-and-swap (CAS):**

```javascript
// compareExchange(view, index, expected, newValue)
// — Se view[index] === expected: escreve newValue, retorna expected
// — Se view[index] !== expected: não escreve nada, retorna o valor atual

Atomics.store(view, 0, 42);

// Caso 1: valor é o esperado — escrita acontece
const r1 = Atomics.compareExchange(view, 0, 42, 100);
// r1 = 42 (antigo); view[0] = 100

// Caso 2: valor mudou — escrita NÃO acontece
const r2 = Atomics.compareExchange(view, 0, 42, 200);
// r2 = 100 (valor atual, diferente de 42); view[0] permanece 100
```

CAS é o bloco de construção de praticamente todos os algoritmos lock-free. Se o retorno for igual ao `expected` passado, a operação teve sucesso. Se for diferente, outro agente modificou o valor no intervalo — e o código deve tentar novamente (retry loop).

---

### Incremento correto com Atomics

```javascript
// worker.js — CÓDIGO CORRETO
import { parentPort } from 'node:worker_threads';

parentPort.once('message', ({ sab }) => {
  const view = new Int32Array(sab);

  for (let i = 0; i < 100_000; i++) {
    Atomics.add(view, 0, 1);  // indivisível — safe com múltiplos workers
  }

  parentPort.postMessage('done');
});
```

```javascript
// main.js
import { Worker } from 'node:worker_threads';

const sab = new SharedArrayBuffer(4);
const view = new Int32Array(sab);

const workers = [new Worker('./worker.js'), new Worker('./worker.js')];
let done = 0;

for (const w of workers) {
  w.postMessage({ sab });
  w.once('message', () => {
    if (++done === workers.length) {
      console.log(view[0]); // Sempre 200000 — sem race condition
    }
  });
}
```

---

### Sincronização com `wait` e `notify`

`Atomics.wait` e `Atomics.notify` implementam uma **variável de condição** primitiva — o padrão é análogo a `pthread_cond_wait`/`pthread_cond_signal`.

```
Atomics.wait(typedArray, index, expectedValue[, timeout])
  → 'ok' | 'not-equal' | 'timed-out'

Atomics.notify(typedArray, index[, count])
  → número de agentes acordados
```

**Semântica de `wait`:**
1. Verifica se `typedArray[index] === expectedValue`. Se não, retorna `'not-equal'` imediatamente (o valor já mudou antes do wait — não há necessidade de bloquear).
2. Se sim, suspende a thread até receber um `notify` nesse índice, ou até o timeout expirar.
3. Quando acordada, retorna `'ok'`. Se o timeout expirar primeiro, retorna `'timed-out'`.

**Semântica de `notify`:**
- Acorda até `count` threads em `wait` no mesmo `index` do mesmo SAB.
- Se `count` for omitido, acorda todas.
- Retorna o número de threads efetivamente acordadas.

> [!danger] `Atomics.wait` não funciona no main thread
> Chamar `Atomics.wait` no thread principal do Node.js (ou no main thread do browser) lança um `TypeError: Atomics.wait cannot be called in this context`. O main thread não pode ser bloqueado — ele precisa do event loop rodando. Use `Atomics.wait` apenas dentro de workers. Para o main thread, existe `Atomics.waitAsync`, que retorna uma Promise.

---

### Padrão producer-consumer com `wait`/`notify`

```javascript
// Protocolo: índice 0 = flag de estado
// 0 = aguardando dado; 1 = dado disponível

// producer-worker.js
import { parentPort } from 'node:worker_threads';

parentPort.once('message', ({ sab }) => {
  const ctrl = new Int32Array(sab, 0, 1);   // primeiro Int32: flag de controle
  const data = new Float64Array(sab, 4);    // resto: dados (offset 4 bytes)

  // Gera e publica dados em loop
  for (let i = 0; i < 10; i++) {
    // Espera consumer processar o dado anterior (flag volta a 0)
    Atomics.wait(ctrl, 0, 1); // bloqueia enquanto flag = 1

    // Escreve dado
    data[0] = Math.random() * 1000;
    data[1] = i;

    // Sinaliza que dado está pronto
    Atomics.store(ctrl, 0, 1);
    Atomics.notify(ctrl, 0, 1);
  }

  parentPort.postMessage('producer done');
});
```

```javascript
// consumer-worker.js
import { parentPort } from 'node:worker_threads';

parentPort.once('message', ({ sab }) => {
  const ctrl = new Int32Array(sab, 0, 1);
  const data = new Float64Array(sab, 4);

  for (let i = 0; i < 10; i++) {
    // Aguarda producer sinalizar (flag = 1)
    Atomics.wait(ctrl, 0, 0); // bloqueia enquanto flag = 0

    // Consome dado
    console.log(`item ${data[1]}: valor = ${data[0].toFixed(2)}`);

    // Sinaliza que processou (flag volta a 0)
    Atomics.store(ctrl, 0, 0);
    Atomics.notify(ctrl, 0, 1);
  }

  parentPort.postMessage('consumer done');
});
```

```javascript
// main.js — orquestra producer e consumer
import { Worker } from 'node:worker_threads';

// SAB: 4 bytes (flag Int32) + 16 bytes (2 × Float64)
const sab = new SharedArrayBuffer(4 + 16);

const producer = new Worker('./producer-worker.js');
const consumer = new Worker('./consumer-worker.js');

// Ambos recebem o mesmo SAB
producer.postMessage({ sab });
consumer.postMessage({ sab });

let done = 0;
for (const w of [producer, consumer]) {
  w.once('message', (msg) => {
    console.log(msg);
    if (++done === 2) console.log('pipeline completo');
  });
}
```

---

### `Atomics.waitAsync` para o main thread

Quando o main thread precisa observar mudanças no SAB sem bloquear o event loop, use `waitAsync`:

```javascript
// main.js — observa flag sem bloquear event loop
import { Worker } from 'node:worker_threads';

const sab = new SharedArrayBuffer(4);
const ctrl = new Int32Array(sab);

// Aguarda worker sinalizar conclusão (flag = 1) — não bloqueia
const result = Atomics.waitAsync(ctrl, 0, 0);

result.value.then((outcome) => {
  console.log('worker sinalizou:', outcome); // 'ok' ou 'timed-out'
  console.log('flag atual:', Atomics.load(ctrl, 0)); // 1
});

const w = new Worker('./worker-signal.js');
w.postMessage({ sab });
```

```javascript
// worker-signal.js
import { parentPort } from 'node:worker_threads';

parentPort.once('message', ({ sab }) => {
  const ctrl = new Int32Array(sab);

  // Simula trabalho
  let soma = 0;
  for (let i = 0; i < 10_000_000; i++) soma += i;

  // Sinaliza conclusão
  Atomics.store(ctrl, 0, 1);
  Atomics.notify(ctrl, 0);

  parentPort.postMessage({ soma });
});
```

---

### Spinlock primitivo

Um spinlock usa CAS em loop para "travar" e `store` para "destravar". É a forma mais simples de exclusão mútua com `Atomics`:

```javascript
// lock.js — spinlock utilitário (NÃO use em produção sem cautela)
export function lock(view, lockIndex) {
  // Tenta adquirir o lock: muda de 0 para 1 atomicamente
  // Se retornar 0, conseguiu; se retornar 1, já estava travado
  while (Atomics.compareExchange(view, lockIndex, 0, 1) !== 0) {
    // Spinning: dá hint ao CPU de que estamos em busy-wait
    // Em produção, misture com Atomics.wait para evitar queimar CPU
  }
}

export function unlock(view, lockIndex) {
  Atomics.store(view, lockIndex, 0);
  Atomics.notify(view, lockIndex, 1); // acorda quem estiver em wait nesse índice
}
```

```javascript
// worker.js — usando o spinlock
import { parentPort } from 'node:worker_threads';
import { lock, unlock } from './lock.js';

parentPort.once('message', ({ sab }) => {
  const meta = new Int32Array(sab, 0, 2); // índice 0 = lock, índice 1 = contador
  const LOCK = 0;
  const COUNTER = 1;

  for (let i = 0; i < 10_000; i++) {
    lock(meta, LOCK);
    // Seção crítica — apenas uma thread aqui por vez
    const current = Atomics.load(meta, COUNTER);
    Atomics.store(meta, COUNTER, current + 1);
    unlock(meta, LOCK);
  }

  parentPort.postMessage('done');
});
```

> [!warning] Spinlock puro queima CPU
> Um spinlock em busy-wait consome 100% de um core enquanto espera. Em produção, misture com `Atomics.wait` para ceder a thread enquanto o lock está ocupado. Prefira mensagens na maioria dos casos — só use spinlock quando a latência de microsegundos importar e a contenção for baixa e previsível.

---

### Layout de memória — indices vs bytes

Um erro frequente é confundir **índice de TypedArray** com **offset em bytes**:

```javascript
const sab = new SharedArrayBuffer(32);

const i32 = new Int32Array(sab);
// i32[0] → bytes 0-3
// i32[1] → bytes 4-7
// i32[2] → bytes 8-11

const f64 = new Float64Array(sab);
// f64[0] → bytes 0-7  (sobrepõe i32[0] e i32[1]!)
// f64[1] → bytes 8-15

// Layo explícito com offsets em bytes:
const ctrl   = new Int32Array(sab, 0, 1);      // bytes 0-3: 1 Int32 de controle
const dados  = new Float64Array(sab, 8);        // bytes 8+: Float64s de dados
// Note: bytes 4-7 ficam sem uso aqui — alinhamento
```

Ao fazer `Atomics.wait(view, index, ...)`, o `index` é o índice do `TypedArray`, não bytes. `Atomics.wait` só funciona com `Int32Array` e `BigInt64Array` — os tipos que o spec permite bloquear.

---

## Na prática

### Quando SAB + Atomics é justificado

**Matrizes grandes em ML e processamento de imagem.** Um modelo de inferência que divide uma imagem em tiles e os processa em paralelo. Cada worker recebe um SAB com os pixels — sem cópia.

```javascript
// main.js — distribui tiles de imagem entre workers
import { Worker } from 'node:worker_threads';

const WIDTH  = 1920;
const HEIGHT = 1080;
const CHANNELS = 4; // RGBA

// Toda a imagem em memória compartilhada
const imageSab = new SharedArrayBuffer(WIDTH * HEIGHT * CHANNELS);
const imageView = new Uint8Array(imageSab);

// Preenche imageView com dados de pixel (leitura de arquivo, câmera etc.)

// Divide em faixas horizontais para processamento paralelo
const WORKER_COUNT = 4;
const rowsPerWorker = Math.ceil(HEIGHT / WORKER_COUNT);

const workers = Array.from({ length: WORKER_COUNT }, (_, i) => {
  const w = new Worker('./tile-worker.js');
  w.postMessage({
    sab: imageSab,
    width: WIDTH,
    channels: CHANNELS,
    startRow: i * rowsPerWorker,
    endRow: Math.min((i + 1) * rowsPerWorker, HEIGHT),
  });
  return w;
});

// Cada worker processa sua faixa diretamente no SAB — sem cópia de ida/volta
```

```javascript
// tile-worker.js — processa uma faixa da imagem in-place
import { parentPort } from 'node:worker_threads';

parentPort.once('message', ({ sab, width, channels, startRow, endRow }) => {
  const view = new Uint8Array(sab);

  for (let row = startRow; row < endRow; row++) {
    for (let col = 0; col < width; col++) {
      const offset = (row * width + col) * channels;
      // Aplica filtro: inverte cores (simples, para exemplificar)
      view[offset]     = 255 - view[offset];     // R
      view[offset + 1] = 255 - view[offset + 1]; // G
      view[offset + 2] = 255 - view[offset + 2]; // B
      // view[offset + 3] = alpha, mantém
    }
  }

  // Neste padrão, workers escrevem em regiões disjuntas — sem necessidade de Atomics
  parentPort.postMessage({ done: true, startRow, endRow });
});
```

Neste caso, como cada worker processa uma faixa exclusiva de linhas, não há sobreposição — e `Atomics` não é necessário para os dados. Apenas um contador de progresso compartilhado (se houver) precisaria de `Atomics.add`.

---

**Contador de progresso em tempo real.** Múltiplos workers reportam progresso sem sobrecarregar o canal de mensagens:

```javascript
// worker.js — atualiza contador compartilhado
import { parentPort } from 'node:worker_threads';

parentPort.once('message', ({ progressSab, itemsToProcess }) => {
  const progress = new Int32Array(progressSab);

  for (let i = 0; i < itemsToProcess; i++) {
    // ... processa item i ...
    Atomics.add(progress, 0, 1); // incremento atômico seguro
  }

  parentPort.postMessage('done');
});
```

```javascript
// main.js — lê progresso sem envolver o worker
import { Worker } from 'node:worker_threads';

const TOTAL = 1_000_000;
const progressSab = new SharedArrayBuffer(4);
const progress = new Int32Array(progressSab);

const w = new Worker('./worker.js');
w.postMessage({ progressSab, itemsToProcess: TOTAL });

// Polling do main thread sem mensagens adicionais
const interval = setInterval(() => {
  const done = Atomics.load(progress, 0);
  console.log(`${((done / TOTAL) * 100).toFixed(1)}% concluído`);
  if (done >= TOTAL) clearInterval(interval);
}, 100);
```

---

### Quando preferir mensagens

Na maioria dos casos, `postMessage` com clone estruturado ou `transferList` é suficiente e mais seguro. Use SAB + `Atomics` apenas quando:

- O dado precisa ser **lido por múltiplas threads simultaneamente** (SAB é o único mecanismo que permite isso sem N-1 cópias).
- A **latência de serialização** é o gargalo medido, não suspeito.
- A **região de memória por thread é disjunta** (caso mais seguro — sem necessidade de sincronização nos dados).
- Você precisa de **coordenação de baixíssima latência** entre threads (microsegundos, não milissegundos).

Para qualquer caso em que os dados fluem linearmente de um worker para outro, `transferList` já é zero-copy e mais simples. Para maioria das arquiteturas de processamento, `postMessage` com `transferList` é a escolha certa.

---

## Armadilhas

> [!warning] Armadilha 1 — Acessar SAB sem `Atomics` produz race conditions silenciosas
> `view[0]++` em dois workers simultâneos é comportamento indefinido do ponto de vista de concorrência. O código **compila e roda sem erro** — a race condition aparece como resultado incorreto intermitente, difícil de reproduzir em ambiente de desenvolvimento. Regra: qualquer leitura ou escrita em posição de SAB que possa ser acessada por mais de uma thread ao mesmo tempo deve usar `Atomics`.

> [!warning] Armadilha 2 — `Atomics.wait` no main thread lança `TypeError`
> `Atomics.wait(view, 0, 0)` chamado no main thread (thread principal do Node.js ou browser) lança imediatamente: `TypeError: Atomics.wait cannot be called in this context`. O main thread não pode ser suspenso. Use `Atomics.waitAsync` no main thread — retorna uma Promise sem bloquear o event loop.

> [!warning] Armadilha 3 — Índice de TypedArray ≠ offset em bytes
> `view[1]` em um `Int32Array` é o byte 4 (não o byte 1). Ao calcular offsets manuais para layouts de SAB (ex: `new Float64Array(sab, 4)`), o segundo argumento é em **bytes**, mas as operações `Atomics` recebem **índice de TypedArray**. Misturar as duas convenções gera leitura/escrita em posições erradas. Documente o layout do SAB explicitamente no código.

> [!warning] Armadilha 4 — SAB não pode diminuir de tamanho
> Um SAB growable só cresce. Um SAB sem `maxByteLength` tem tamanho fixo para sempre. Não há como liberar parte da memória ou redimensionar para baixo. Provisione o SAB com folga — ou use múltiplos SABs menores com propósitos bem definidos.

> [!warning] Armadilha 5 — `Atomics.add` retorna o valor ANTIGO, não o novo
> `Atomics.add(view, 0, 1)` retorna o valor **antes** da adição. Se você usa o retorno para checar se foi o "décimo" worker a incrementar, o worker que retornar 9 foi o décimo (o novo valor é 10). Confundir pré/pós-incremento aqui produz bugs de off-by-one difíceis de rastrear.

> [!warning] Armadilha 6 — Atomicidade individual não compõe
> Duas operações `Atomics` consecutivas **não são atômicas juntas**. Exemplo: `Atomics.load` + `Atomics.store` para copiar um valor não é atômico — outro worker pode modificar o valor entre as duas operações. Para operações compostas, use `compareExchange` em loop (retry) ou proteja a seção com um lock.

> [!warning] Armadilha 7 — SAB não está em `transferList` — e não deve estar
> Ao enviar um SAB via `postMessage`, **não liste-o em `transferList`**. O Node.js simplesmente ignora essa listagem — o SAB não é transferível por design. Listá-lo não causa erro, mas pode criar confusão sobre a semântica do código. A documentação do Node.js é explícita: `SharedArrayBuffer` não pode aparecer em `transferList`.

---

## Modelo mental: mapa de uso

```
                        ┌─────────────────────────────────┐
                        │     Dado flui de A → B          │
                        │     (pipeline linear)           │
                        └──────────────┬──────────────────┘
                                       │
                        ArrayBuffer + transferList (zero-copy)
                        postMessage: simples, seguro

                        ┌─────────────────────────────────┐
                        │   Múltiplos leitores, dado      │
                        │   grande, sem escrita           │
                        └──────────────┬──────────────────┘
                                       │
                        SharedArrayBuffer, sem Atomics nos dados
                        (regiões disjuntas: cada worker escreve na sua faixa)

                        ┌─────────────────────────────────┐
                        │   Múltiplos escritores na       │
                        │   mesma posição                 │
                        └──────────────┬──────────────────┘
                                       │
                        SharedArrayBuffer + Atomics (add, exchange, CAS)

                        ┌─────────────────────────────────┐
                        │   Coordenação / sincronização   │
                        │   entre threads                 │
                        └──────────────┬──────────────────┘
                                       │
                        Atomics.wait + Atomics.notify (em workers)
                        Atomics.waitAsync (em main thread)
```

---

## Em entrevista

> [!quote] Frase pronta (inglês)
> "`SharedArrayBuffer` is a buffer that's visible simultaneously across multiple Worker Threads — unlike a regular `ArrayBuffer`, which is cloned or transferred. Once you have shared memory, you have race conditions, so reads and writes need `Atomics` — `Atomics.load`, `store`, `add`, `compareExchange`, and so on. For coordination, `Atomics.wait` and `Atomics.notify` give you a primitive condition variable, but `wait` only works inside Workers, not the main thread — you'd use `waitAsync` there instead. The legitimate use cases are tight: large matrices in ML or image processing where multiple workers read the same data simultaneously, shared counters, semaphores. For most application code, message passing with `transferList` is simpler and the right default."

**Vocabulário técnico:**

| Português | Inglês |
|---|---|
| memória compartilhada | shared memory |
| operação atômica | atomic operation |
| condição de corrida | race condition |
| comparar-e-trocar | compare-and-swap (CAS) |
| aguardar e notificar | wait and notify |
| variável de condição | condition variable |
| spinlock | spinlock |
| exclusão mútua | mutual exclusion (mutex) |
| seção crítica | critical section |
| região disjunta | disjoint region |
| buffer destacado | detached buffer |
| lock-free | lock-free |

**Perguntas frequentes em entrevista:**

- *"Qual a diferença entre `SharedArrayBuffer` e `ArrayBuffer` com `transferList`?"* — Com `transferList`, a propriedade do buffer é transferida: apenas uma thread acessa por vez; o emissor fica com referência detached. `SharedArrayBuffer` é acessado por ambas as threads simultaneamente — por isso precisa de `Atomics` para evitar race conditions.

- *"Por que `Atomics.wait` não funciona no main thread?"* — O main thread é responsável pelo event loop do Node.js. Bloqueá-lo suspenderia o processamento de I/O, timers, e eventos — o processo ficaria travado. O main thread nunca pode ser suspenso de forma síncrona; daí a existência de `Atomics.waitAsync`, que retorna uma Promise e não bloqueia.

- *"Duas operações `Atomics` consecutivas são atômicas juntas?"* — Não. Cada operação `Atomics` é individualmente atômica, mas a sequência não é. Entre `Atomics.load` e o subsequente `Atomics.store`, outro worker pode modificar o valor. Para operações compostas, use `compareExchange` em loop de retry.

- *"Quando escolher SAB em vez de postMessage + transferList?"* — Quando o mesmo dado precisa ser acessado por múltiplas threads ao mesmo tempo (transferList só move para uma), ou quando a sincronização de baixíssima latência entre threads é o requisito principal. Para a maioria dos pipelines de processamento, `transferList` é suficiente e muito mais simples.

---

## Veja também

- `[[03 - Worker Threads - fundamentos]]`
- `[[04 - Comunicação entre workers - postMessage e MessageChannel]]`
- `[[06 - Pool de workers - pattern de produção]]`
- `[[Node.js]]`
