---
title: "Macrotasks e timers: setTimeout, setInterval, setImmediate"
created: 2026-05-07
updated: 2026-05-07
type: concept
status: seedling
publish: true
tags:
  - node
  - event-loop
  - timer
  - macrotask
  - setimmediate
aliases:
  - Timers
  - setImmediate
  - setTimeout
---

# Macrotasks e timers: setTimeout, setInterval, setImmediate

> [!abstract] TL;DR
> `setTimeout` e `setInterval` rodam na fase **timers**. `setImmediate` roda na fase **check**. Em contexto de I/O, `setImmediate` é determinístico — sempre executa antes de `setTimeout(fn, 0)`, porque a fase `check` vem antes da próxima fase `timers`. Fora de I/O, a ordem entre os dois é imprevisível e depende do tempo de inicialização do processo. Para sleep idiomático em código async, use `node:timers/promises`.

## O que é

Node.js expõe três APIs para agendar callbacks fora do fluxo síncrono atual — sem ser microtasks. São as três **macrotask APIs** nativas do runtime:

### `setTimeout(callback, ms[, ...args])`

Agenda `callback` para execução **pelo menos** `ms` milissegundos no futuro, na fase **timers** do event loop. O delay é um mínimo, não um máximo — o callback pode disparar muito depois se outras fases estiverem ocupadas.

Detalhes importantes da implementação:

- Se `ms` for menor que 1, maior que 2.147.483.647 (≈ 24,8 dias) ou `NaN`, o valor é normalizado para **1ms**. O Node.js (via libuv) nunca usa delay zero — `setTimeout(fn, 0)` efetivamente se torna `setTimeout(fn, 1)`.
- Retorna um objeto `Timeout`, usado para cancelar via `clearTimeout(timeout)`.
- Argumentos adicionais após `ms` são repassados ao callback, evitando closures desnecessárias.

```javascript
const timeout = setTimeout((nome) => {
  console.log(`Olá, ${nome}`);
}, 500, 'Alice');

// Para cancelar antes de disparar:
clearTimeout(timeout);
```

### `setInterval(callback, ms[, ...args])`

Agenda `callback` para execução repetida a cada `ms` milissegundos, indefinidamente, até que `clearInterval` seja chamado. Mesmas regras de normalização de delay que `setTimeout`.

Retorna um objeto `Timeout` — a mesma classe de `setTimeout`, reutilizável com `clearInterval` e `clearTimeout` indistintamente.

```javascript
let contador = 0;
const interval = setInterval(() => {
  contador++;
  console.log(`tick ${contador}`);
  if (contador >= 5) clearInterval(interval);
}, 200);
```

> [!warning] setInterval não é "cron"
> `setInterval` não garante que os callbacks são executados exatamente a cada `ms`. Se o callback demora mais do que o intervalo para completar, ou se outras fases do event loop atrasam a execução, os disparos se acumulam e há drift progressivo. Ver seção **Armadilhas**.

### `setImmediate(callback[, ...args])`

Agenda `callback` para execução na fase **check** — a fase imediatamente após a fase **poll** na mesma iteração do event loop. Retorna um objeto `Immediate`, cancelável via `clearImmediate`.

```javascript
setImmediate(() => {
  console.log('fase check desta iteração');
});
```

`setImmediate` foi projetado especificamente para executar código **depois que os callbacks de I/O da iteração atual terminaram**, mas **antes de qualquer timer da próxima iteração**. Essa semântica é precisa dentro de callbacks de I/O; fora deles, a relação com `setTimeout(fn, 0)` é não determinística.

### `timers/promises` — versões Promise-based (Node.js 15+)

O módulo `node:timers/promises` exporta versões awaitable das três APIs, eliminando a necessidade de wrappers manuais:

```javascript
import {
  setTimeout,
  setImmediate,
  setInterval,
} from 'node:timers/promises';

// Sleep idiomático em código async
await setTimeout(1000);

// setTimeout com valor de retorno
const resultado = await setTimeout(500, 'pronto');
console.log(resultado); // 'pronto'

// setImmediate awaitable
await setImmediate();

// setInterval como async iterator
for await (const _ of setInterval(100)) {
  console.log('a cada 100ms');
  // use break para encerrar
}
```

Todas as funções do módulo aceitam um objeto `options` com:
- `ref: false` — o timer não mantém o processo vivo (equivalente a chamar `.unref()`)
- `signal` — um `AbortSignal` para cancelamento cooperativo

### Tabela comparativa

| API | Fase do event loop | Repete? | Retorno | Cancelamento |
|---|---|---|---|---|
| `setTimeout(fn, ms)` | timers | Não | `Timeout` | `clearTimeout` |
| `setInterval(fn, ms)` | timers (repetido) | Sim | `Timeout` | `clearInterval` |
| `setImmediate(fn)` | check | Não | `Immediate` | `clearImmediate` |
| `timers/promises setTimeout` | timers | Não | `Promise<T>` | `AbortSignal` |
| `timers/promises setImmediate` | check | Não | `Promise<T>` | `AbortSignal` |
| `timers/promises setInterval` | timers (repetido) | Sim (async iterator) | `AsyncIterator` | `AbortSignal` / `break` |

## Por que importa

A distinção de fases entre `setTimeout`/`setInterval` (fase **timers**) e `setImmediate` (fase **check**) determina a **ordem de execução** em cenários que misturam I/O e timers. Esse detalhe aparece com frequência em entrevistas sênior e em debugging de bugs sutis de ordem de execução.

Mais concretamente:

**Dentro de um callback de I/O**, `setImmediate` é determinístico: sempre executa antes de qualquer `setTimeout(fn, 0)`. O motivo é geométrico — a fase `poll` (onde o callback de I/O executou) é seguida diretamente pela fase `check`. A fase `timers` só é verificada na **próxima iteração**. Portanto, agendar via `setImmediate` dentro de I/O é a forma idiomática de dizer "execute no próximo slot disponível após este callback" com garantia de ordem.

**Fora de I/O**, a relação é imprevisível. O event loop inicia na fase `timers`. Se o processo levou mais de 1ms para inicializar (o mínimo normalizado de `setTimeout(fn, 0)`), o timer já expirou e dispara primeiro. Se levou menos, a fase `timers` não encontra nada, avança até `check` e o `setImmediate` dispara primeiro. Essa variabilidade de 1–2ms de startup torna o resultado não determinístico entre execuções.

Compreender essa diferença é o que separa "eu sei que existe `setImmediate`" de "eu sei *quando* usá-lo corretamente".

## Como funciona

### Exemplo 1 — `setTimeout(fn, 0)`: o delay mínimo de 1ms

```javascript
console.log('início');

setTimeout(() => {
  console.log('timer disparou');
}, 0); // delay 0 é normalizado para 1ms internamente

console.log('fim do síncrono');

// Saída:
// início
// fim do síncrono
// timer disparou
```

O callback nunca executa sincronamente — mesmo com delay 0. O código síncrono atual (call stack) sempre termina antes de qualquer fase do event loop processar seus callbacks. E o delay efetivo é pelo menos 1ms, não zero.

### Exemplo 2 — Em contexto de I/O: `setImmediate` sempre primeiro

```javascript
const fs = require('node:fs');

fs.readFile(__filename, () => {
  // Estamos na fase POLL, executando um callback de I/O
  // O loop vai para CHECK antes de voltar para TIMERS

  setTimeout(() => {
    console.log('timeout'); // fase TIMERS — próxima iteração
  }, 0);

  setImmediate(() => {
    console.log('immediate'); // fase CHECK — ainda nesta iteração
  });
});

// Saída sempre garantida:
// immediate
// timeout
```

O fluxo detalhado:
1. `fs.readFile` completa → callback entra na fila da fase **poll**
2. Fase **poll** executa o callback → `setTimeout` e `setImmediate` são agendados
3. Fase **poll** termina → event loop avança para **check**
4. Fase **check** executa `setImmediate` → imprime `immediate`
5. Iteração termina → nova iteração começa → fase **timers** → imprime `timeout`

Essa ordem é **garantida e determinística** quando ambos são agendados de dentro de um callback de I/O.

### Exemplo 3 — Fora de I/O: ordem não determinística

```javascript
// Top-level: fora de qualquer callback de I/O
setTimeout(() => {
  console.log('timeout');    // pode ser primeiro OU segundo
}, 0);

setImmediate(() => {
  console.log('immediate');  // pode ser primeiro OU segundo
});

// Possível saída A (processo demorou > 1ms para inicializar):
// timeout
// immediate

// Possível saída B (processo demorou < 1ms para inicializar):
// immediate
// timeout
```

Nunca assuma uma ordem específica neste cenário. O resultado varia entre execuções e entre ambientes (máquina de desenvolvimento vs. container de CI vs. produção).

### Exemplo 4 — `setInterval` com handler lento (drift e reentrância)

```javascript
// Cenário problemático: handler demora mais que o intervalo
let execucoes = 0;

const interval = setInterval(() => {
  execucoes++;
  console.log(`[${Date.now()}] execução ${execucoes} início`);

  // Simula trabalho síncrono que demora 200ms
  const deadline = Date.now() + 200;
  while (Date.now() < deadline) { /* busy wait — apenas para ilustração */ }

  console.log(`[${Date.now()}] execução ${execucoes} fim`);

  if (execucoes >= 3) clearInterval(interval);
}, 100); // intervalo de 100ms, mas handler leva 200ms

// Comportamento real:
// - A execução 1 começa ~100ms, termina ~300ms
// - A execução 2 começa ~300ms (não ~200ms como esperado)
// - O intervalo NÃO dispara callbacks simultâneos — ele aguarda a fase timers
// - Há drift acumulado: cada execução começa mais tarde do que o agendado
```

Node.js não executa callbacks de `setInterval` em paralelo — a thread JS é single-threaded. Se o handler demora mais que o intervalo, a próxima execução simplesmente começa na próxima oportunidade em que a fase **timers** é alcançada. Não há "callbacks empilhados" executando simultaneamente, mas há drift crescente.

### Exemplo 5 — Sleep idiomático com `timers/promises`

```javascript
import { setTimeout as sleep } from 'node:timers/promises';

async function processar(items) {
  for (const item of items) {
    await processarItem(item);
    await sleep(100); // pausa de 100ms entre cada item — sem callbacks manuais
  }
}
```

Comparado ao padrão de callback antigo:

```javascript
// Padrão antigo — difícil de compor, propenso a erros
function aguardar(ms, callback) {
  setTimeout(callback, ms);
}

// Padrão moderno — awaitable, cancelável, integrável com AbortSignal
import { setTimeout as sleep } from 'node:timers/promises';

const ac = new AbortController();
const { signal } = ac;

try {
  await sleep(5000, undefined, { signal }); // sleep de 5s cancelável
} catch (err) {
  if (err.name === 'AbortError') {
    console.log('sleep cancelado antes de completar');
  }
}

// Para cancelar externamente:
ac.abort();
```

### Exemplo 6 — Loop com `setTimeout` recursivo vs. `setInterval` (anti-drift)

```javascript
// setInterval com drift — inadequado para polling de precisão
setInterval(() => {
  realizarTarefa(); // se demorar, o próximo disparo se afasta do schedule
}, 1000);

// setTimeout recursivo com cálculo de drift — mais robusto
function agendarProximaExecucao() {
  const inicio = Date.now();

  realizarTarefa();

  const duracao = Date.now() - inicio;
  const proximo = Math.max(0, 1000 - duracao); // compensa o tempo gasto

  setTimeout(agendarProximaExecucao, proximo);
}

agendarProximaExecucao();

// Versão async com timers/promises — mais limpa e cancelável
import { setTimeout as sleep } from 'node:timers/promises';

async function loop(signal) {
  while (!signal.aborted) {
    const inicio = Date.now();
    await realizarTarefaAsync();
    const duracao = Date.now() - inicio;
    await sleep(Math.max(0, 1000 - duracao), undefined, { signal });
  }
}
```

## Na prática

### Preferir `setImmediate` sobre `setTimeout(fn, 0)` dentro de I/O

Quando a intenção é "execute este código na próxima oportunidade, após este callback de I/O terminar", `setImmediate` é a escolha correta — e a única com garantia de ordem:

```javascript
// Dentro de qualquer callback de I/O:
fs.readFile(caminho, (err, dados) => {
  if (err) throw err;

  // BOM: explícito e determinístico em contexto de I/O
  setImmediate(() => {
    processarDados(dados);
  });

  // AMBÍGUO: funciona na prática mas sem garantia de ordem
  setTimeout(() => {
    processarDados(dados);
  }, 0);
});
```

### Preferir `setTimeout` recursivo sobre `setInterval` para trabalho periódico

`setInterval` é raramente a escolha correta em produção para tarefas que envolvem I/O ou lógica não trivial. O padrão recomendado em bibliotecas de produção é um `setTimeout` recursivo que calcula o próximo delay com base no tempo gasto pela execução anterior — conforme mostrado no Exemplo 6. Isso evita drift acumulado e garante um intervalo mínimo entre o fim de uma execução e o início da próxima.

### Usar `.unref()` para timers que não devem manter o processo vivo

```javascript
// Timer de keepalive/heartbeat em um processo CLI:
// Não deve impedir o processo de encerrar quando o trabalho principal termina
const heartbeat = setInterval(() => {
  enviarHeartbeat();
}, 30_000);

heartbeat.unref(); // o processo pode encerrar mesmo com o interval ativo

// Com timers/promises, use ref: false:
import { setInterval } from 'node:timers/promises';

for await (const _ of setInterval(30_000, null, { ref: false })) {
  enviarHeartbeat();
}
```

### Cancelamento cooperativo com `AbortSignal`

```javascript
import { setTimeout as sleep, setInterval } from 'node:timers/promises';

const ac = new AbortController();

// Cancelar todos os timers de uma vez:
async function tarefa() {
  try {
    await sleep(10_000, undefined, { signal: ac.signal });
    for await (const _ of setInterval(1_000, undefined, { signal: ac.signal })) {
      await realizarPasso();
    }
  } catch (err) {
    if (err.name === 'AbortError') return; // cancelado graciosamente
    throw err;
  }
}

// Em outro ponto do código, para cancelar:
ac.abort();
```

## Armadilhas

### 1. `setInterval` reentrante — handler mais lento que o intervalo

```javascript
// Armadilha: handler de 500ms com intervalo de 200ms
setInterval(async () => {
  await buscarDadosExternos(); // operação que leva ~500ms
}, 200);

// Comportamento REAL em Node.js:
// - t=0ms: 1ª execução começa
// - t=500ms: 1ª execução termina
// - t=500ms: fase timers já acumulou callbacks — a 2ª e possivelmente a 3ª disparam
//            em sequência rápida, sem o intervalo esperado entre elas
// - Resultado: rajadas de execuções seguidas de longos silêncios
```

Solução: usar `setTimeout` recursivo com cálculo de drift, ou `timers/promises setInterval` com `await` para garantir que cada iteração espera a anterior completar (o `for await` implicitamente faz isso).

### 2. Assumir que `setTimeout(fn, 0)` é instantâneo

```javascript
// Mito: "setTimeout(fn, 0) roda imediatamente após o síncrono"
// Realidade: o delay mínimo é 1ms E outras fases podem intervir

let flag = false;

setTimeout(() => { flag = true; }, 0);

// Este código NUNCA vê flag === true
// Código síncrono não "espera" o timer
console.log(flag); // sempre false aqui

// Se precisar de execução assíncrona mas imediata, use queueMicrotask ou Promise
```

### 3. Usar `setTimeout` para sleep em código async

```javascript
// RUIM: wrapper manual desnecessário, não cancelável, não composable
function sleep(ms) {
  return new Promise(resolve => setTimeout(resolve, ms));
}

// BOM: use a API nativa — é exatamente o mesmo, mas oficial e cancelável
import { setTimeout as sleep } from 'node:timers/promises';

await sleep(1000);
```

### 4. Timer com closure pesada nunca limpo — vazamento de memória

```javascript
function criarTimer(dados) {
  // dados pode ser um objeto grande — o timer mantém a referência
  const timer = setInterval(() => {
    processarDados(dados); // closure captura 'dados'
  }, 1000);

  // Se clearInterval nunca for chamado, 'dados' nunca é coletado pelo GC
  // mesmo que o caller não tenha mais referência ao objeto original

  return timer; // caller DEVE chamar clearInterval quando terminar
}

// Padrão correto: sempre limpar em cleanup/teardown
const timer = criarTimer(dadosGrandes);

// Em cleanup (ex: encerramento de servidor, componente React unmount, etc):
clearInterval(timer);
```

### 5. Ordem de `setImmediate` vs `setTimeout` fora de I/O — não assuma nada

```javascript
// Código frágil que assume setImmediate sempre primeiro
function diferir(fn) {
  setImmediate(fn); // funciona dentro de I/O, mas não em top-level
}

// Código robusto: usar dentro de callbacks de I/O quando precisar de garantia
fs.readFile(path, (err, data) => {
  setImmediate(() => processarDados(data)); // aqui é sempre correto
});
```

## Em entrevista

> [!tip] Frase pronta (inglês)
> "`setTimeout` and `setInterval` run in the **timers phase**; `setImmediate` runs in the **check phase**. The interesting detail: inside an I/O callback, `setImmediate` always runs before `setTimeout(fn, 0)` — it's deterministic, because the loop is in the poll phase and the very next phase is check. The timers phase only runs in the *next* iteration. Outside I/O, the order is non-deterministic because it depends on whether the 1ms minimum delay has elapsed by the time the first iteration starts. For modern async code, prefer `setImmediate` when you need 'run after this I/O callback', and use `node:timers/promises` for awaitable sleeps with AbortSignal support."

Use essa frase para responder:
- *"What's the difference between `setImmediate` and `setTimeout(fn, 0)`?"*
- *"When would you use `setImmediate` over `setTimeout`?"*
- *"How do timers work in Node.js?"*
- *"Why does the order of `setImmediate` vs `setTimeout` change depending on context?"*

### Vocabulário de entrevista

| Português | Inglês | Contexto |
|---|---|---|
| Fase de timers | timers phase | fase do event loop onde setTimeout/setInterval disparam |
| Fase check | check phase | fase onde setImmediate dispara, logo após poll |
| Deriva do timer | timer drift | acúmulo de atraso entre disparos esperados e reais |
| Reentrância | reentrancy | quando um handler é agendado novamente antes do anterior terminar |
| Determinístico | deterministic | comportamento previsível independente de timing externo |
| Threshold do timer | timer threshold | delay mínimo que deve passar para o timer disparar |
| Iteração do loop | loop iteration / tick | uma passagem completa pelas seis fases |
| Cancelamento cooperativo | cooperative cancellation | cancelamento via AbortSignal acordado entre produtor e consumidor |

### Perguntas de follow-up comuns

**"O que acontece se eu passar delay 0 para `setTimeout`?"**
O delay é normalizado internamente para 1ms pelo libuv. O callback nunca dispara sincronamente e sempre aguarda pelo menos 1ms — além do tempo que outras fases levarem para terminar antes de a fase `timers` ser alcançada.

**"Como evitar drift em um polling periódico?"**
Usar `setTimeout` recursivo com cálculo: `setTimeout(fn, Math.max(0, intervalo - tempoGasto))`. Ou usar `timers/promises setInterval` com `for await`, que aguarda cada iteração completar antes de iniciar a próxima.

**"Quando `setImmediate` é garantidamente determinístico?"**
Apenas quando agendado de dentro de um callback de I/O (fase poll). Nesse contexto, `setImmediate` sempre precede qualquer `setTimeout(fn, 0)` agendado no mesmo callback.

**"Por que `setInterval` raramente é correto em produção?"**
Porque ele não aguarda o handler completar antes de agendar o próximo disparo. Com operações assíncronas, o intervalo entre o fim de uma execução e o início da próxima pode ser zero — ou negativo em termos de intent. O padrão com `setTimeout` recursivo ou `for await` com `timers/promises` é mais seguro.

## Veja também

- [[04 - As fases do event loop]] — diagrama completo das seis fases; onde timers e check se encaixam no ciclo
- [[05 - Microtasks - nextTick, queueMicrotask, Promise.then]] — a camada de microtasks que tem prioridade sobre qualquer macrotask, incluindo timers
- [[07 - I-O assíncrono - kernel vs thread pool]] — o que acontece na fase poll que antecede a fase check onde setImmediate vive
- [[09 - async-await - o que é, o que não é]] — como `await setTimeout` de `timers/promises` se encaixa no modelo async/await
- [[Node.js]] — tronco: panorama completo do runtime com links para toda a trilha
