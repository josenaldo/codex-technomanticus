---
title: "As fases do event loop"
created: 2026-05-07
updated: 2026-05-07
type: concept
status: seedling
publish: true
tags:
  - node
  - event-loop
  - libuv
  - phases
aliases:
  - Event loop phases
  - Fases do event loop
---

# As fases do event loop

> [!abstract] TL;DR
> O event loop do Node.js roda em seis fases por iteração: **timers**, **pending callbacks**, **idle/prepare**, **poll**, **check** e **close callbacks** — nessa ordem, de forma circular. Entre cada fase, todas as microtasks pendentes são drenadas (primeiro `process.nextTick`, depois Promises e `queueMicrotask`). A fase `poll` é o coração: ela coleta novos eventos de I/O do sistema operacional e pode **bloquear** a thread esperando I/O quando não há trabalho agendado — é o que mantém servidores HTTP vivos.

## O que é

O event loop é o mecanismo que permite ao Node.js executar operações assíncronas em uma única thread JavaScript. Implementado pelo **libuv**, ele não é uma fila única — é um ciclo estruturado em **seis fases distintas**, cada uma com seu próprio tipo de trabalho e sua própria fila de callbacks.

Cada passagem completa pelo ciclo — executando todas as seis fases em sequência — é chamada de **iteração** ou **tick** do event loop. O nome "tick" vem do comportamento de relógio: o loop avança fase a fase, iteração a iteração, enquanto houver trabalho ou o processo estiver ativo.

### timers — execução de callbacks agendados por tempo

A fase **timers** executa os callbacks de `setTimeout()` e `setInterval()` cujo threshold de tempo já expirou. O libuv verifica se o delay mínimo especificado passou; se passou, o callback é elegível para execução nesta fase.

Importante: o threshold é um **mínimo**, não um máximo. Um callback com `setTimeout(fn, 100)` nunca roda antes de 100ms, mas pode rodar bem depois — dependendo do que estava acontecendo em outras fases quando o timer expirou. Se a fase `poll` estava processando um callback longo, o timer vai esperar a poll terminar antes de ser executado na próxima iteração.

O delay mínimo efetivo para `setTimeout(fn, 0)` no Node.js é **1ms** (comportamento interno do libuv), não zero. Esse detalhe é relevante para entender por que `setImmediate` pode vencer uma corrida com `setTimeout(fn, 0)`.

### pending callbacks — callbacks de I/O diferidos

A fase **pending callbacks** executa callbacks de I/O que foram diferidos para a próxima iteração do loop. O caso mais comum são erros de operações de rede como TCP — por exemplo, `ECONNREFUSED` em algumas plataformas é reportado via pending callback em vez de diretamente na fase poll.

Na grande maioria das aplicações, esta fase passa rapidamente sem executar nada. Ela existe para acomodar casos onde o SO reporta condições de erro de forma assíncrona com um tick extra de delay.

### idle, prepare — uso exclusivamente interno

As fases **idle** e **prepare** são de uso exclusivo do libuv internamente. Código JavaScript não pode agendar trabalho diretamente nessas fases. O libuv usa essas fases para preparar operações internas antes da fase poll — por exemplo, calcular o timeout correto para o I/O polling.

Na documentação oficial do Node.js, essas fases são mencionadas apenas como "only used internally". Para fins práticos em entrevistas e debugging, o que importa é saber que elas existem na sequência, mas não interagem com código de aplicação.

### poll — o coração do event loop

A fase **poll** é a mais importante e a mais complexa. Ela tem dois comportamentos distintos dependendo do estado do sistema:

**Quando a poll queue não está vazia:**
O event loop itera pelos callbacks na fila e os executa sincronicamente, um por um, até a fila esvaziar ou atingir um limite máximo do sistema operacional. Esses são os callbacks de I/O "prontos" — `fs.readFile` completou, uma conexão TCP chegou, dados chegaram num socket.

**Quando a poll queue está vazia:**
O event loop entra no modo de espera. Ele usa mecanismos do OS (`epoll` no Linux, `kqueue` no macOS/BSD, `IOCP` no Windows) para bloquear a thread eficientemente aguardando novos eventos de I/O. O tempo máximo de bloqueio é calculado pelo libuv com base no timer mais próximo que está pendente:

- Se há um timer agendado que vai expirar em Xms, o poll bloqueia por no máximo Xms
- Se há scripts `setImmediate()` agendados, o poll não bloqueia — passa direto para a fase **check**
- Se não há timers nem `setImmediate()` nem handles ativos, o loop **encerra**

Esse comportamento de bloqueio eficiente é o que torna Node.js econômico em termos de CPU: um servidor HTTP em idle não fica em busy-wait — ele fica dormindo no `epoll_wait` do kernel, consumindo praticamente zero CPU, até uma conexão chegar.

### check — execução de setImmediate

A fase **check** executa todos os callbacks registrados via `setImmediate()`. Esta fase existe imediatamente após a fase poll, o que garante que `setImmediate` sempre execute **depois** de qualquer I/O que completou na mesma iteração.

Esse posicionamento é deliberado: `setImmediate` foi projetado para executar "logo após a fase de I/O atual terminar", antes que o loop volte para verificar timers. Daí o comportamento determinístico dentro de um callback de I/O: `setImmediate` sempre vence `setTimeout(fn, 0)` quando ambos são agendados de dentro de um callback de `fs.readFile`, `http.request`, etc.

### close callbacks — limpeza de handles

A fase **close callbacks** executa callbacks registrados para o evento `close` de handles que foram fechados abruptamente. O exemplo canônico é `socket.on('close', ...)` — quando um socket é destruído via `socket.destroy()` (não via `socket.end()`), o callback `close` é enfileirado aqui.

Se um handle for fechado graciosamente (via `end()`), o evento `close` pode ser emitido diretamente, sem passar por esta fase. A fase close callbacks cobre especificamente os fechamentos abruptos.

## Por que importa

Sem entender as fases, vários comportamentos do Node.js parecem arbitrários ou quebrados:

**"`setImmediate` roda antes de `setTimeout(fn, 0)` dentro de I/O"** — só faz sentido sabendo que `setImmediate` pertence à fase **check**, que vem logo após a fase **poll** onde o callback de I/O executou. O timer, por sua vez, só é verificado na fase **timers** da próxima iteração.

**"`process.nextTick` tem prioridade sobre tudo, inclusive Promises"** — porque `nextTick` não é uma fase do event loop: é uma microtask drenada entre fases, com prioridade máxima sobre as demais microtasks (Promises, `queueMicrotask`).

**"Meu servidor não encerra mesmo sem requisições pendentes"** — porque algum handle está ativo (um `setInterval`, um socket aberto, um timer), mantendo o loop vivo na fase poll.

**"Meu timer de 100ms está disparando com 150ms de delay"** — porque a fase poll estava ocupada executando um callback de I/O quando o timer expirou. O timer só é verificado na fase timers, e a fase timers só começa na próxima iteração.

Conhecer as fases transforma comportamento aparentemente mágico em consequências previsíveis de uma sequência fixa.

## Como funciona

### Diagrama ASCII — as seis fases em ciclo

```
   ┌──────────────────────────────────┐
   │   Início de cada iteração        │
   └────────────────┬─────────────────┘
                    │
                    ▼
   ┌──────────────────────────────────┐
┌─►│          1. TIMERS               │  setTimeout(), setInterval()
│  │   (callbacks com delay expirado) │
│  └────────────────┬─────────────────┘
│          ◄── drain microtasks ──►
│  ┌────────────────▼─────────────────┐
│  │      2. PENDING CALLBACKS        │  I/O errors diferidos (ex: ECONNREFUSED)
│  └────────────────┬─────────────────┘
│          ◄── drain microtasks ──►
│  ┌────────────────▼─────────────────┐
│  │       3. IDLE, PREPARE           │  uso interno do libuv
│  └────────────────┬─────────────────┘
│          ◄── drain microtasks ──►
│  ┌────────────────▼─────────────────┐    ┌──────────────────────┐
│  │            4. POLL               │◄───│  I/O events do OS    │
│  │  (coleta eventos; pode bloquear) │    │  (epoll/kqueue/IOCP) │
│  └────────────────┬─────────────────┘    └──────────────────────┘
│          ◄── drain microtasks ──►
│  ┌────────────────▼─────────────────┐
│  │           5. CHECK               │  setImmediate()
│  └────────────────┬─────────────────┘
│          ◄── drain microtasks ──►
│  ┌────────────────▼─────────────────┐
│  │       6. CLOSE CALLBACKS         │  socket.on('close', ...)
│  └────────────────┬─────────────────┘
│          ◄── drain microtasks ──►
│                   │
│     ┌─────────────▼───────────────┐
│     │  Verificar se loop continua │
│     │  (handles/requests ativos?) │
└─────┤  SIM → próxima iteração     │
      │  NÃO → process.exit()       │
      └─────────────────────────────┘
```

**Legenda:**
- `◄── drain microtasks ──►` = drena `process.nextTick` queue completamente, depois drena Promise/`queueMicrotask` queue completamente
- A drenagem acontece entre **cada fase**, não entre callbacks da mesma fase
- Se uma microtask agendar outra microtask, ela também é drenada antes do loop avançar

### Exemplo 1 — contexto de I/O: ordem determinística

```javascript
// Dentro de um callback de I/O, a ordem setImmediate vs setTimeout é DETERMINÍSTICA
const fs = require('node:fs');

fs.readFile(__filename, () => {
  // Estamos aqui: dentro da fase POLL, executando callback de I/O
  // O loop acabou de sair da poll e vai para CHECK antes de voltar para TIMERS

  setTimeout(() => {
    console.log('timeout');    // fase TIMERS — próxima iteração
  }, 0);

  setImmediate(() => {
    console.log('immediate');  // fase CHECK — ainda nesta iteração
  });

  process.nextTick(() => {
    console.log('nextTick');   // microtask — drena ANTES de qualquer fase
  });

  Promise.resolve().then(() => {
    console.log('promise');    // microtask — drena após nextTick, antes de CHECK
  });
});
```

Saída garantida (sempre nesta ordem):

```
nextTick
promise
immediate
timeout
```

Fluxo detalhado:
1. `fs.readFile` completa → callback entra na fila da fase **poll**
2. Fase poll executa o callback → quatro itens são agendados
3. Callback termina → call stack esvazia → microtasks são drenadas:
   - `process.nextTick` drena primeiro → imprime `nextTick`
   - Promise resolve drena depois → imprime `promise`
4. Event loop avança para fase **check** → executa `setImmediate` → imprime `immediate`
5. Microtasks drenadas novamente (nenhuma pendente)
6. Fase **close callbacks** (nada)
7. Nova iteração → fase **timers** → executa `setTimeout` → imprime `timeout`

### Exemplo 2 — fora de contexto de I/O: ordem indeterminada

```javascript
// Fora de qualquer callback de I/O, a ordem setImmediate vs setTimeout(fn, 0)
// É NÃO DETERMINÍSTICA — depende de quanto tempo levou para o Node inicializar

setTimeout(() => {
  console.log('timeout');    // pode sair primeiro OU segundo
}, 0);

setImmediate(() => {
  console.log('immediate');  // pode sair primeiro OU segundo
});
```

Saída possível (varia entre execuções):

```
timeout
immediate
```

ou:

```
immediate
timeout
```

Por quê? Quando o event loop inicia, ele entra na fase **timers**. Se o Node levou mais de 1ms para inicializar (o delay mínimo efetivo de `setTimeout(fn, 0)`), o timer já expirou e `timeout` executa primeiro. Se levou menos, o timer não expirou ainda, a fase timers não executa nada, a poll passa para check e `immediate` executa primeiro. O tempo de startup do processo introduz essa variabilidade.

### Exemplo 3 — drenagem de microtasks entre fases (não entre callbacks)

```javascript
// Demonstração: microtasks drenam entre FASES, não entre cada callback da mesma fase

setTimeout(() => {
  console.log('timer 1');
  process.nextTick(() => console.log('nextTick do timer 1'));
}, 0);

setTimeout(() => {
  console.log('timer 2');
  process.nextTick(() => console.log('nextTick do timer 2'));
}, 0);
```

Saída esperada:

```
timer 1
timer 2
nextTick do timer 1
nextTick do timer 2
```

Não:

```
timer 1
nextTick do timer 1   ← ERRADO: microtasks não drenam entre callbacks da mesma fase
timer 2
nextTick do timer 2   ← ERRADO
```

Ambos os `setTimeout` estão na fase **timers** da mesma iteração. Os dois callbacks executam completamente. Só quando a fase timers termina inteira é que as microtasks são drenadas — e as duas aparecem juntas, na ordem em que foram enfileiradas.

> [!info] Mudança no Node.js 11
> Antes do Node.js 11 (lançado em outubro de 2018), o comportamento era diferente: microtasks eram drenadas apenas entre iterações completas do loop, não entre fases. A partir do Node.js 11, o comportamento foi alinhado com o dos browsers: microtasks drenam entre cada fase. Se estiver mantendo código para Node.js <= 10, esse detalhe é relevante.

### Exemplo 4 — poll blocking e por que servidores ficam vivos

```javascript
const http = require('node:http');

const server = http.createServer((req, res) => {
  res.end('ok');
});

server.listen(3000, () => {
  console.log('Server listening on port 3000');
  // A partir daqui, o processo NUNCA encerra sozinho.
  // Por quê? O server.listen() registra um handle TCP ativo.
  // Na fase poll, o libuv faz epoll_wait()/kqueue() esperando conexões.
  // Enquanto o handle TCP estiver ativo, o loop nunca determina que
  // não há trabalho — ele sempre volta para poll e bloqueia esperando.
});

// Sem nenhuma outra linha de código, o processo permanece vivo indefinidamente.
// Para encerrar: server.close() → remove o handle → loop pode finalizar
```

Contraste com um script sem handles ativos:

```javascript
// Este script encerra naturalmente após ~0ms
setTimeout(() => {
  console.log('executou');
  // Nenhum handle ativo após isso — o loop verifica e encerra
}, 100);

// Fluxo:
// 1. Código síncrono termina
// 2. Poll bloqueia por 100ms (o único timer pendente)
// 3. Fase timers executa o callback
// 4. Loop verifica: nenhum handle ou timer ativo → process.exit(0)
```

## Na prática

### Poll phase e o "loop alive check"

O event loop mantém uma contagem interna de **handles** e **requests** ativos. Um handle é qualquer recurso que pode produzir eventos enquanto estiver ativo: timers, sockets, servidores TCP, file watchers. Um request é uma operação única em andamento (uma leitura de arquivo, uma conexão sendo estabelecida).

O loop encerra quando essa contagem chega a zero e a phase poll determina que não há trabalho futuro. Isso explica comportamentos práticos:

- `setInterval(fn, 1000)` mantém o processo vivo — cria um timer handle ativo
- `server.listen()` mantém o processo vivo — cria um TCP handle ativo
- `fs.readFile(path, cb)` cria um request ativo durante a leitura, mas encerra quando completa
- `server.unref()` — desregistra o handle da contagem "alive check" sem fechar o servidor. O processo pode encerrar mesmo com o servidor aberto, se não houver outro handle ativo

```javascript
// server.unref() — útil em CLIs que não devem ficar vivas por causa de um servidor
const server = http.createServer(handleRequest);
server.listen(0); // porta aleatória
server.unref();   // o servidor existe, mas não impede o processo de encerrar

// O processo vai encerrar quando o código principal terminar,
// mesmo com o servidor ainda registrado
```

### Calculando o timeout da poll

O libuv calcula dinamicamente quanto tempo a fase poll pode bloquear antes de precisar avançar. O cálculo considera:

1. Se há callbacks `setImmediate()` agendados → timeout = 0 (não bloqueia)
2. Se há timers pendentes → timeout = tempo até o próximo timer expirar
3. Se há handles ativos mas nenhum timer → timeout = indefinido (bloqueia até evento)
4. Se não há nada → loop encerra (não chega a bloquear)

Esse mecanismo garante que `setTimeout(fn, 100)` dispare com precisão razoável: a poll sabe que deve sair em no máximo 100ms para que a fase timers execute o callback.

### Diagnóstico: qual fase está bloqueando?

Quando um timer de 50ms está disparando com 200ms de delay, a causa mais comum é um callback de I/O ou outro callback de alguma fase anterior que está executando código síncrono longo. Para diagnosticar:

```javascript
// Instrumentação simples: medir lag do event loop
const INTERVAL_MS = 50;
let lastTime = Date.now();

setInterval(() => {
  const now = Date.now();
  const lag = now - lastTime - INTERVAL_MS;
  if (lag > 10) {
    console.warn(`Event loop lag: ${lag}ms`);
  }
  lastTime = now;
}, INTERVAL_MS);
```

Lag consistente acima de alguns milissegundos indica código bloqueante em alguma das fases. A nota [[10 - Bloqueio do event loop - sintomas e causas]] aprofunda o diagnóstico.

## Armadilhas

### 1. Microtasks drenam entre fases, não entre callbacks da mesma fase

O erro conceitual mais comum: imaginar que cada callback de `setTimeout` ou callback de I/O tem suas próprias microtasks drenadas imediatamente após. Não é assim.

A drenagem de microtasks ocorre uma vez quando **a fase inteira termina**, não entre cada callback da fila. Se dez timers expiram na mesma iteração e cada um agenda um `process.nextTick`, todos os dez `nextTick` callbacks executam juntos após todos os dez timers completarem — não intercalados entre os timers.

```javascript
// Armadilha: assumir que nextTick roda após CADA setTimeout
for (let i = 0; i < 3; i++) {
  setTimeout(() => {
    console.log(`timer ${i}`);
    process.nextTick(() => console.log(`  → nextTick após timer ${i}`));
  }, 0);
}

// Saída REAL:
// timer 0
// timer 1
// timer 2
//   → nextTick após timer 0
//   → nextTick após timer 1
//   → nextTick após timer 2

// Saída ERRADA (que alguns esperam):
// timer 0
//   → nextTick após timer 0   ← NÃO ACONTECE
// timer 1
//   → nextTick após timer 1
// timer 2
//   → nextTick após timer 2
```

### 2. Confundir "poll queue" com "macrotask queue genérica"

A poll queue é a fila **interna da fase poll** — ela contém callbacks de I/O que o kernel reportou como prontos. A expressão "macrotask queue" (usada em documentações de browser e algumas libs) não mapeia diretamente para nenhuma fila única do Node.js.

No Node, há filas distintas por fase: fila de timers (fase timers), fila de pending callbacks, fila de poll, fila de check (setImmediate). Quando se fala em "macrotask queue" no contexto do Node, na prática se está falando sobre a fase poll na maioria dos casos, mas o conceito simplificado de "uma fila só" é uma abstração que o libuv não usa internamente.

A distinção importa para debugging: um callback enfileirado via `setImmediate` não está na mesma fila que um callback de `fs.readFile`. Eles serão executados em fases diferentes, com potencial de microtasks sendo drenadas entre eles.

### 3. `setImmediate` vs `setTimeout(fn, 0)` fora de I/O: não assuma ordem

É tentador usar `setImmediate` como substituto de `setTimeout(fn, 0)` para "executar assincronamente mas logo". Dentro de callbacks de I/O, sim — `setImmediate` sempre ganha. Mas em código de top-level ou em timers aninhados, a ordem não é garantida.

```javascript
// FRÁGIL: assume que setImmediate sempre vem antes
function adiarParaProximaTick(fn) {
  setImmediate(fn); // "vai rodar antes do próximo setTimeout"
}

// ROBUSTO: se a intenção é executar após I/O atual, use explicitamente
// dentro de callbacks de I/O onde o comportamento é determinístico
```

Se o objetivo é garantir que algo execute depois de todas as microtasks mas antes de qualquer timer, a ferramenta correta é `setImmediate` **dentro de um callback de I/O**. Em top-level, a única garantia absoluta é `process.nextTick` (microtask, roda antes de qualquer fase).

### 4. `process.nextTick` recursivo paralisa o event loop

`process.nextTick` não é uma fase — é uma microtask com prioridade máxima. Se um callback de `nextTick` agendar outro `nextTick` recursivamente, a microtask queue nunca esvazia. O event loop **nunca avança para a próxima fase**.

```javascript
// PARALISAÇÃO TOTAL: nenhuma fase do event loop é alcançada
function bloquear() {
  process.nextTick(bloquear);
}
bloquear();

// Qualquer setTimeout, setImmediate, ou callback de I/O registrado depois
// NUNCA executa. O processo parece vivo, mas está completamente travado
// drenando nextTick em loop infinito na thread principal.
```

Esse comportamento é idêntico para `queueMicrotask` ou Promises encadeadas recursivamente — qualquer microtask que produz microtasks indefinidamente paralisa o loop. `process.nextTick` é apenas o mais comum nesse antipadrão.

## Em entrevista

### Frase pronta (inglês)

> "The Node.js event loop runs in six phases per iteration: timers, pending callbacks, idle/prepare, poll, check, and close callbacks. The poll phase is the most interesting — it picks up new I/O events from the OS using `epoll`, `kqueue`, or `IOCP` depending on the platform, and it can block waiting for I/O until the nearest timer is due. Between every phase, microtasks are drained — first all `process.nextTick` callbacks, then all Promise and `queueMicrotask` callbacks. That's why `process.nextTick` and Promise callbacks are higher priority than any timer or I/O callback, and why `setImmediate` always beats `setTimeout(fn, 0)` when both are scheduled from inside an I/O callback."

Use essa frase ao responder:
- *"Walk me through the Node.js event loop"*
- *"What are the phases of the event loop?"*
- *"Why does `setImmediate` run before `setTimeout(fn, 0)` sometimes?"*
- *"How does Node handle thousands of concurrent connections on one thread?"*

### Vocabulário de entrevista

| Termo em inglês | Contexto / tradução |
|---|---|
| **event loop phase** | fase do event loop — uma das seis etapas da iteração (timers, pending callbacks, idle/prepare, poll, check, close callbacks) |
| **loop iteration / tick** | iteração do loop — uma passagem completa pelas seis fases |
| **drain microtasks** | drenar microtasks — executar completamente a fila de microtasks (nextTick → Promises) antes de avançar de fase |
| **poll phase** | fase poll — fase que coleta eventos de I/O do OS; pode bloquear aguardando I/O |
| **block waiting for I/O** | bloquear esperando I/O — comportamento da fase poll quando não há trabalho; o kernel notifica quando eventos chegam |
| **handle** | handle — recurso ativo que pode produzir eventos (server, socket, timer); mantém o loop vivo enquanto ativo |
| **epoll / kqueue / IOCP** | mecanismos de I/O polling do OS: epoll (Linux), kqueue (macOS/BSD), IOCP (Windows) |
| **non-deterministic ordering** | ordem não determinística — quando `setImmediate` vs `setTimeout(fn, 0)` em top-level pode variar entre execuções |
| **timer threshold** | threshold do timer — o delay mínimo de um `setTimeout`/`setInterval`; o timer só dispara quando esse mínimo passou |
| **starve the event loop** | faminar o event loop — impedir que outras fases executem bloqueando o loop em microtasks ou código síncrono |

### Perguntas de follow-up comuns

- *"What happens if there's nothing to do in the poll phase?"* → O loop calcula o timeout com base no próximo timer. Se não há timers nem `setImmediate`, e há handles ativos (como um servidor TCP), a poll bloqueia indefinidamente até um evento de I/O chegar. Se não há handles ativos, o processo encerra.

- *"Why is `process.nextTick` not in the event loop diagram?"* → Porque `nextTick` não é uma fase — é uma microtask drenada entre fases. Ele não tem um "slot" no ciclo; ele sempre corre entre a fase atual e a próxima.

- *"What's the difference between `setImmediate` and `process.nextTick`?"* → `setImmediate` é a fase **check** — próxima fase após poll na iteração atual. `process.nextTick` é microtask — drena antes da próxima fase, qualquer que seja ela. `nextTick` tem prioridade maior que `setImmediate`.

- *"How does the event loop keep a server alive?"* → `server.listen()` registra um TCP handle ativo. O loop só encerra quando a contagem de handles ativos chega a zero. Enquanto o servidor estiver ouvindo, há sempre um handle ativo, a fase poll sempre tem uma razão para continuar, e o processo nunca encerra.

- *"Can you block the event loop from JavaScript code?"* → Sim, de duas formas: código síncrono longo (um loop de computação ocupando a call stack) ou microtasks recursivas (um `process.nextTick` que agenda outro `nextTick`). Em ambos os casos, nenhuma outra fase executa durante o bloqueio.

## Veja também

- [[03 - Call stack, heap e queues]] — as estruturas de memória que o event loop manipula: call stack, heap, microtask queue e macrotask queue
- [[05 - Microtasks - nextTick, queueMicrotask, Promise.then]] — deep dive na drenagem de microtasks: ordem de prioridade, casos de borda, recursão perigosa
- [[06 - Macrotasks e timers - setTimeout, setInterval, setImmediate]] — comportamento detalhado dos timers: jitter, drift, coalescing, e comparação completa das APIs
- [[07 - I-O assíncrono - kernel vs thread pool]] — o que acontece dentro da fase poll: como epoll/kqueue/IOCP notificam o libuv e quais operações usam o thread pool vs I/O assíncrono nativo do kernel
- [[10 - Bloqueio do event loop - sintomas e causas]] — como identificar e corrigir quando uma das fases está bloqueando o loop em produção
- [[Node.js]] — tronco: panorama completo do runtime com diagrama de arquitetura e links para toda a trilha
