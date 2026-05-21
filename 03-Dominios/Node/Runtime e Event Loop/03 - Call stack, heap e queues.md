---
title: "Call stack, heap e queues"
created: 2026-05-07
updated: 2026-05-07
type: concept
status: seedling
publish: true
tags:
  - node
  - event-loop
  - mental-model
  - call-stack
  - heap
aliases:
  - Call stack
  - Heap
  - Microtask queue
  - Macrotask queue
---

# Call stack, heap e queues

> [!abstract] TL;DR
> A thread JS tem quatro estruturas em runtime: a **call stack** (frames de chamada de função, ordem LIFO), o **heap** (pool de objetos gerenciado pelo GC do V8), a **microtask queue** (Promises, `process.nextTick`, `queueMicrotask`) e a **macrotask queue** (timers, callbacks de I/O). O event loop só avança para a próxima macrotask quando a call stack está vazia **e** a microtask queue está drenada.

## O que é

Quando o V8 executa código JavaScript em Node.js, ele mantém quatro estruturas distintas na memória. Entender o papel de cada uma é o pré-requisito para compreender o event loop em profundidade.

### Call stack — a pilha de execução

A call stack é a estrutura que rastreia **onde o programa está e para onde deve retornar**. Ela funciona no modelo LIFO (Last In, First Out): cada chamada de função empurra um novo **frame de execução** no topo da pilha; quando a função retorna, o frame é removido.

Cada frame contém:
- A referência à função sendo executada
- Os parâmetros recebidos
- As variáveis locais
- O endereço de retorno (onde continuar quando essa função terminar)

O V8 impõe um limite para o tamanho da call stack. Quando esse limite é atingido — geralmente por recursão infinita ou muito profunda — o runtime lança um `RangeError: Maximum call stack size exceeded`. O tamanho padrão pode ser ajustado via flag `--stack-size` (valor em kilobytes).

A call stack também funciona como a **raiz do garbage collector**: o GC usa os frames ativos da stack como ponto de entrada para descobrir quais objetos no heap ainda são alcançáveis (e portanto, não devem ser coletados).

### Heap — o pool de objetos

O heap é a região de memória onde o V8 aloca **objetos JavaScript** — arrays, objetos literais, closures, funções, strings longas, buffers. Ao contrário da stack, o heap não é organizado em ordem de inserção/remoção; ele é um espaço gerenciado dinamicamente pelo **Garbage Collector (GC)**.

O V8 organiza o heap em gerações, seguindo a hipótese geracional: *a maioria dos objetos morre jovem*:

- **Young Generation (Geração Jovem)**: onde novos objetos são alocados. Subdividida em *nursery* e *intermediate*. O GC opera aqui com o **Scavenger** (GC menor), que usa uma técnica de semi-espaço — metade do espaço está sempre vazia para receber os objetos que sobrevivem. Objetos que sobrevivem a mais de um ciclo de Scavenger são promovidos.
- **Old Generation (Geração Velha)**: objetos que sobreviveram ao Young Generation chegam aqui. O GC opera com o **Mark-Compact** (GC maior), que passa por três fases: marcação dos objetos alcançáveis, varredura para liberar os não-alcançáveis, e compactação para reduzir fragmentação.

O GC do V8 pode executar partes do trabalho de forma **concorrente** (enquanto o JS roda em paralelo), mas certas fases ainda requerem pausas curtas da thread JS — as chamadas *GC pauses* ou *stop-the-world pauses*.

**Heap e stack são estruturas distintas**: stack armazena frames de execução (referências, primitivos locais, endereços de retorno); heap armazena os objetos em si. Uma variável local na stack pode conter uma referência que aponta para um objeto no heap.

### Microtask queue — a fila de alta prioridade

A microtask queue (fila de microtarefas) armazena callbacks que devem ser executados **antes do event loop avançar para a próxima fase**. Três APIs produzem microtasks em Node.js:

| API | Ordem de prioridade |
|---|---|
| `process.nextTick(fn)` | Mais alta — drena antes das demais microtasks |
| `queueMicrotask(fn)` | Segunda — drena após todos os `nextTick` |
| `Promise.resolve().then(fn)` | Segunda — mesmo nível que `queueMicrotask` |

O nome "microtask" pode induzir ao erro de imaginar que essas tasks são menores ou mais rápidas. A diferença é **quando** são executadas: microtasks são drenadas completamente depois que cada tarefa da macrotask queue termina de executar e antes que o event loop prossiga.

### Macrotask queue — a fila principal (e a terminologia)

A macrotask queue (também chamada de **callback queue** ou **task queue** em diferentes documentações e especificações) armazena callbacks que o event loop escalona para execução futura:

- Callbacks de timers: `setTimeout`, `setInterval`
- Callbacks de I/O: resposta de `fs.readFile`, conexão de rede
- Callbacks de `setImmediate` (fase check do event loop)

A terminologia varia: a especificação do HTML e as docs do MDN usam "task queue" (ou "macrotask queue" informalmente); a documentação do Node.js fala em "callback queue". Os três termos se referem ao mesmo conceito — a fila de onde o event loop retira uma task por vez para executar.

## Por que importa

O ponto central que desbloqueia todo o entendimento do event loop é este:

> **O event loop só retira trabalho das filas quando a call stack está vazia.**

Enquanto houver qualquer código rodando na stack — qualquer função ainda não retornada —, nenhum callback de nenhuma fila será iniciado. Isso tem consequências diretas:

**`process.nextTick` em recursão trava o programa.** Se uma função agenda `process.nextTick` de si mesma recursivamente, a microtask queue nunca esvazia. O event loop fica preso drenando microtasks e nunca avança para processar callbacks de I/O, timers ou novas requisições. O processo parece vivo mas está completamente travado para qualquer trabalho externo.

**Código síncrono longo bloqueia tudo.** Um loop de 5 segundos no topo do programa mantém a stack ocupada por 5 segundos. Durante esse intervalo, nenhuma microtask ou macrotask é processada — o servidor não responde, timers não disparam, callbacks de I/O não executam.

**`RangeError: Maximum call stack size exceeded` tem causa estrutural.** O erro não é aleatório — ele sempre indica que a stack cresceu além do limite por falta de um caso-base em recursão. Entender o limite físico da stack é o primeiro passo para diagnosticar o problema.

## Como funciona

### Exemplo 1 — call stack overflow por recursão sem caso-base

```javascript
// Recursão sem caso-base: cada chamada empurra um frame na stack.
// Quando o limite é atingido, V8 lança RangeError.
function f() {
  f(); // chama a si mesma sem condição de parada
}

f();
// RangeError: Maximum call stack size exceeded
```

O erro ocorre porque cada invocação de `f()` adiciona um frame. Sem nenhum `return` ou condição que interrompa a recursão, a stack cresce até estourar o limite do V8.

Para recursão legítima e profunda, a alternativa é usar trampolining (converter recursão em iteração gerenciada) ou garantir que a profundidade máxima esteja dentro do limite. Para ajustar o limite em cenários específicos:

```bash
# Aumentar a stack para 65536 KB (64 MB) — use com cautela
node --stack-size=65536 app.js
```

### Exemplo 2 — ordem de execução: sync → microtasks → macrotasks

```javascript
console.log('1 — sync: início');

setTimeout(() => {
  console.log('5 — macrotask: setTimeout');
}, 0);

Promise.resolve().then(() => {
  console.log('3 — microtask: Promise.then');
});

process.nextTick(() => {
  console.log('2 — microtask: nextTick (prioridade máxima)');
});

queueMicrotask(() => {
  console.log('4 — microtask: queueMicrotask');
});

console.log('6 — sync: fim');
```

Saída esperada:

```
1 — sync: início
6 — sync: fim
2 — microtask: nextTick (prioridade máxima)
3 — microtask: Promise.then
4 — microtask: queueMicrotask
5 — macrotask: setTimeout
```

O fluxo exato:

1. Todo o código síncrono roda primeiro — `1` e `6` são impressos em sequência.
2. A stack esvazia. O event loop drena a microtask queue na ordem de prioridade: `nextTick` primeiro, depois `Promise.then` e `queueMicrotask` (mesma prioridade, ordem de enfileiramento).
3. Só então o event loop avança para a fase de timers e executa o callback do `setTimeout`.

> [!warning] `setTimeout(fn, 0)` não significa "imediatamente"
> O delay `0` é tratado internamente como `1ms` no Node.js (comportamento do libuv). Mais importante: mesmo com `0ms`, o callback de `setTimeout` é uma macrotask e sempre executa **depois** de todas as microtasks pendentes.

### Diagrama ASCII — as quatro estruturas

```
┌──────────────────────────────────────────────────────────────────┐
│                        Thread JavaScript                          │
│                                                                    │
│  ┌─────────────────┐          ┌──────────────────────────────┐   │
│  │   CALL STACK    │          │            HEAP               │   │
│  │   (LIFO)        │          │   (objetos JS — GC do V8)    │   │
│  │                 │          │                               │   │
│  │ ┌─────────────┐ │          │  ┌─────────────────────────┐ │   │
│  │ │  frame: f() │ │ ──────── │  │  Young Generation       │ │   │
│  │ └─────────────┘ │ ref→obj  │  │  (Scavenger / GC menor) │ │   │
│  │ ┌─────────────┐ │          │  └─────────────────────────┘ │   │
│  │ │ frame: g()  │ │          │  ┌─────────────────────────┐ │   │
│  │ └─────────────┘ │          │  │  Old Generation          │ │   │
│  │ ┌─────────────┐ │          │  │  (Mark-Compact / GC)    │ │   │
│  │ │ frame: main │ │          │  └─────────────────────────┘ │   │
│  │ └─────────────┘ │          └──────────────────────────────┘   │
│  └─────────────────┘                                              │
│                                                                    │
│  ┌─────────────────────────────────────────────────────────────┐ │
│  │                    MICROTASK QUEUE                           │ │
│  │  [ nextTick cb ] → [ Promise.then cb ] → [ queueMicro cb ] │ │
│  │  (drena completamente antes do event loop avançar)          │ │
│  └─────────────────────────────────────────────────────────────┘ │
│                                                                    │
│  ┌─────────────────────────────────────────────────────────────┐ │
│  │                    MACROTASK QUEUE                           │ │
│  │       (também: "callback queue" / "task queue")              │ │
│  │  [ setTimeout cb ] → [ fs.readFile cb ] → [ I/O cb ] …     │ │
│  │  (event loop retira UMA task por vez)                       │ │
│  └─────────────────────────────────────────────────────────────┘ │
│                                                                    │
│  Regra: event loop só avança quando stack vazia + microtasks OK  │
└──────────────────────────────────────────────────────────────────┘
```

### O ciclo do event loop em termos dessas estruturas

```
┌─────────────────────────────────────────────┐
│              Ciclo do Event Loop             │
│                                             │
│  1. Executa código síncrono até stack vazia │
│              ↓                              │
│  2. Drena TODA a microtask queue            │
│     (nextTick → Promise.then → queueMicro)  │
│              ↓                              │
│  3. Retira UMA macrotask e executa          │
│     (timer, I/O callback, setImmediate…)    │
│              ↓                              │
│  4. Drena TODA a microtask queue novamente  │
│              ↓                              │
│  5. Repete do passo 3                       │
└─────────────────────────────────────────────┘
```

## Na prática

### Inspecionando a call stack com `console.trace()`

`console.trace()` imprime a call stack atual para o stderr sem lançar um erro. É útil para entender o caminho de execução em produção ou em testes:

```javascript
function terceiro() {
  console.trace('Stack em terceiro()');
}

function segundo() {
  terceiro();
}

function primeiro() {
  segundo();
}

primeiro();
```

Saída hipotética:

```
Trace: Stack em terceiro()
    at terceiro (app.js:2:11)
    at segundo (app.js:6:3)
    at primeiro (app.js:10:3)
    at Object.<anonymous> (app.js:13:1)
    at Module._compile (node:internal/modules/cjs/loader:1358:14)
    ...
```

Os frames internos do Node (Module._compile, etc.) mostram como o próprio runtime invocou o ponto de entrada. Em stack traces de erros reais, esses frames ajudam a distinguir código da aplicação de código de módulo.

### Lendo um stack trace de erro

Ao analisar um `RangeError` ou qualquer exceção não tratada em Node, a leitura do stack trace segue de cima para baixo: o frame mais recente (onde ocorreu o erro) está no topo; o ponto de entrada do programa está no fundo:

```
RangeError: Maximum call stack size exceeded
    at processItem (worker.js:12:5)    ← onde estourou
    at processItem (worker.js:15:10)   ← chamada recursiva
    at processItem (worker.js:15:10)   ← ...repetida N vezes...
    at startProcessing (worker.js:20:3)
    at main (app.js:5:1)               ← ponto de entrada
```

O padrão de repetição do mesmo frame é a assinatura visual de recursão infinita.

### Flag `--stack-size` para recursão profunda legítima

Árvores de expressão, parsers recursivos descendentes e algoritmos de travessia profunda podem exceder o limite padrão do V8 mesmo com casos-base corretos. Nesses casos, a flag `--stack-size` permite aumentar o limite:

```bash
# Aumentar para 32 MB (padrão varia por plataforma, tipicamente ~10 MB)
node --stack-size=32768 meu-parser.js
```

Em cenários hipotéticos como processamento de ASTs com profundidade acima de 10.000 nós, esse ajuste é necessário. Mas a primeira alternativa a considerar é sempre converter a recursão em iteração explícita com uma pilha manual — mais previsível e sem dependência de flags de runtime.

## Armadilhas

### 1. Recursão sem caso-base → RangeError inevitável

Qualquer função que chama a si mesma sem uma condição de sarada vai estourar a stack. O erro não é imediato — ele depende do tamanho do frame e do limite da stack — mas é determinístico.

```javascript
// ERRADO: sem caso-base
function somar(n) {
  return n + somar(n - 1); // nunca para
}

// CORRETO: com caso-base
function somar(n) {
  if (n <= 0) return 0;      // condição de parada
  return n + somar(n - 1);
}
```

### 2. Microtasks "rodam em background" — mito perigoso

Microtasks não são assíncronas no sentido de "rodam em paralelo". Elas rodam na **mesma thread JavaScript**, no mesmo fluxo de execução — só em um momento diferente (após o código síncrono atual, antes da próxima macrotask). Isso significa que um loop de microtasks pode travar o programa tão efetivamente quanto código síncrono.

```javascript
// PERIGO: nextTick recursivo — o event loop nunca avança
function loop() {
  process.nextTick(loop); // agenda si mesmo como microtask
}

loop();
// setTimeout abaixo NUNCA dispara — macrotask queue nunca é alcançada
setTimeout(() => console.log('isso nunca imprime'), 0);
```

Microtasks são síncronas na perspectiva do event loop: enquanto houver microtasks na fila, o event loop não avança. A ilusão de "background" vem do fato de serem agendadas para *depois* do código atual, não de rodarem em paralelo.

### 3. Confundir heap (objetos) com stack (frames)

São estruturas com propósitos, tamanhos e gerenciamento completamente diferentes:

| | Call Stack | Heap |
|---|---|---|
| **O que armazena** | Frames de chamada de função | Objetos JavaScript |
| **Estrutura** | LIFO (pilha) | Pool não-ordenado |
| **Gerenciamento** | Automático pelo V8 ao chamar/retornar | Garbage Collector (Scavenger + Mark-Compact) |
| **Limite** | Fixo (configurável via `--stack-size`) | Limitado pela RAM disponível |
| **Quando cresce** | Em cada chamada de função | Em cada `new Object()`, array, closure |
| **Erro ao estourar** | `RangeError: Maximum call stack size exceeded` | `FATAL ERROR: Heap limit Allocation failed` |

Uma variável local `const obj = {}` na stack contém uma **referência** — o ponteiro ocupa espaço na stack, mas o objeto em si existe no heap.

## Em entrevista

### Frase pronta (inglês)

> "The JS thread has four runtime structures: the call stack of execution frames, the heap of objects managed by V8's garbage collector, the microtask queue for Promises and process.nextTick, and the macrotask queue for timer and I/O callbacks. The event loop can only pick up work from the queues when the call stack is empty — that's why a synchronous infinite loop blocks everything, including microtasks."

Use essa frase ao responder "Explain the JavaScript event loop", "What is the call stack?", ou "What's the difference between microtasks and macrotasks?". Em seguida, esteja pronto para detalhar a ordem de drenagem das filas ou o impacto de `process.nextTick` recursivo.

### Vocabulário de entrevista

| Termo em inglês | Equivalente PT-BR / contexto |
|---|---|
| **call stack** | pilha de chamadas — estrutura LIFO que rastreia frames de execução |
| **heap** | monte — pool de memória onde V8 aloca objetos JS, gerenciado pelo GC |
| **garbage collector** | coletor de lixo — componente do V8 que libera memória de objetos não mais alcançáveis |
| **microtask queue** | fila de microtarefas — drena completamente antes do event loop avançar |
| **macrotask queue** | fila de macrotarefas — também "callback queue" ou "task queue"; event loop retira uma task por vez |
| **stack frame** | frame de execução — contexto de uma chamada de função ativa na stack |
| **generational GC** | GC geracional — estratégia que separa objetos jovens de velhos para coletar cada grupo com técnicas diferentes |

### Perguntas de follow-up comuns

- *"What triggers a RangeError in Node.js?"* → Recursão sem caso-base que esgota o limite da call stack do V8. O limite pode ser ajustado via `--stack-size`, mas a solução estrutural é converter para iteração.
- *"What's the difference between `process.nextTick` and `Promise.then`?"* → Ambos são microtasks, mas `process.nextTick` tem prioridade maior — drena primeiro. Em `Promise.then` e `queueMicrotask`, a ordem é de chegada na fila.
- *"Can microtasks block the event loop?"* → Sim. Microtasks rodam na mesma thread JS. Um loop de microtasks (como `process.nextTick` recursivo) impede o event loop de processar qualquer macrotask — incluindo timers e callbacks de I/O.
- *"What's the difference between the heap and the stack?"* → Stack armazena frames de execução (estrutura LIFO, tamanho fixo). Heap armazena objetos JS (pool dinâmico, gerenciado pelo GC). Uma variável local na stack pode conter uma referência para um objeto no heap.

## Veja também

- [[02 - V8, libuv e thread pool]] — os componentes do runtime que gerenciam essas estruturas; V8 executa JS e gerencia heap, libuv roda o event loop
- [[04 - As fases do event loop]] — como o event loop percorre timers, I/O, check e outras fases drenando as queues
- [[05 - Microtasks - nextTick, queueMicrotask, Promise.then]] — deep dive na ordem de execução de microtasks e casos de borda
- [[Node.js]] — tronco: panorama completo do runtime com diagrama de arquitetura e links para toda a trilha
- [[JavaScript Fundamentals]] — fundamentos JS: call stack e event loop básico no contexto do browser
