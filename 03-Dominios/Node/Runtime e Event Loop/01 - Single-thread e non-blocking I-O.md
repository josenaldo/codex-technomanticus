---
title: "Single-thread e non-blocking I/O"
created: 2026-05-07
updated: 2026-05-07
type: concept
status: seedling
publish: true
tags:
  - node
  - event-loop
  - mental-model
  - non-blocking
aliases:
  - Single-threaded
  - Non-blocking I/O
---


# Single-thread e non-blocking I/O

> [!abstract] TL;DR
> Node.js é single-thread: existe uma única thread que executa código JavaScript. Mesmo assim, ele atende milhares de conexões simultâneas porque I/O (disco, rede, banco) é delegado ao sistema operacional via libuv. A thread JS não fica bloqueada esperando — ela registra um callback e volta a processar outras tarefas. O I/O acontece em paralelo, no OS; o JS permanece sequencial.

## O que é

**Single-threaded** significa que existe exatamente uma thread responsável por executar código JavaScript no processo Node.js. Não há execução paralela de código JS — se duas requisições chegam ao mesmo tempo, uma delas espera a outra terminar de executar o trecho JS atual.

**Non-blocking I/O** significa que chamadas de I/O (leitura de arquivo, consulta de banco, requisição HTTP) retornam imediatamente, sem bloquear essa thread. O resultado não está disponível na hora — o Node registra um callback que será chamado quando a operação completar. Enquanto isso, a thread JS fica livre para processar outras coisas.

Esses dois conceitos se complementam: o modelo só funciona porque o I/O não retém a thread. Se o I/O bloqueasse, a única thread ficaria parada esperando e o servidor não processaria mais nada durante esse intervalo.

A definição oficial da documentação do Node.js resume bem:

> "The event loop is what allows Node.js to perform non-blocking I/O operations — despite the fact that a single JavaScript thread is used by default — by offloading operations to the system kernel whenever possible."
>
> — [Node.js Docs — The Node.js Event Loop](https://nodejs.org/en/learn/asynchronous-work/event-loop-timers-and-nexttick)

## Por que importa

A pergunta clássica em entrevista — e a confusão mais comum entre devs vindos de outras stacks — é:

> "Se Node é single-thread, como ele aguenta milhares de requisições simultâneas?"

A resposta revela o trade-off central do Node e exige entender a distinção entre dois tipos de trabalho:

| Tipo de trabalho | Descrição | Node se sai... |
|---|---|---|
| **I/O-bound** | A maior parte do tempo é gasta esperando disco, rede ou banco | Muito bem — a thread JS fica livre enquanto o OS trabalha |
| **CPU-bound** | A maior parte do tempo é gasta em cálculo puro (criptografia pesada, compressão, ML) | Mal — a thread JS fica ocupada e bloqueia tudo mais |

Node foi projetado para o caso I/O-bound. Servidores web, APIs REST, gateways, BFFs (Backend for Frontend), proxies — esses perfis passam >90% do tempo aguardando respostas externas. É exatamente aqui que o modelo brilha.

O trade-off oposto também precisa ser claro: uma operação CPU-bound longa — digamos, um loop de 2 segundos processando uma imagem — congela a thread JS e impede que qualquer outra requisição seja atendida nesse intervalo. Para esse caso existem [[02 - V8, libuv e thread pool|Worker Threads]] e processos filhos.

## Como funciona

### Fluxo básico — fs.readFile

O exemplo mais direto do modelo non-blocking:

```javascript
const fs = require('node:fs');

console.log('1 — antes de readFile'); // executa imediatamente

fs.readFile('./dados.json', 'utf8', (err, conteudo) => {
  // Este callback SÓ é chamado depois que o OS termina de ler o arquivo.
  // Pode levar milissegundos ou segundos — não importa.
  if (err) throw err;
  console.log('3 — arquivo lido, tamanho:', conteudo.length);
});

console.log('2 — depois de readFile'); // executa ANTES do callback
```

Saída esperada:

```
1 — antes de readFile
2 — depois de readFile
3 — arquivo lido, tamanho: <N>
```

A linha `2` imprime antes da linha `3` porque `fs.readFile` retorna imediatamente após registrar a operação. A thread JS não espera. O OS faz a leitura em paralelo e, quando termina, coloca o callback na fila do event loop.

### Comparação com a versão bloqueante

```javascript
const fs = require('node:fs');

console.log('1 — antes de readFileSync');

// readFileSync BLOQUEIA a thread JS até o arquivo ser lido por completo.
// Durante esse tempo, nenhuma outra requisição é atendida.
const conteudo = fs.readFileSync('./dados.json', 'utf8');

console.log('2 — arquivo lido, tamanho:', conteudo.length);
console.log('3 — depois de readFileSync');
```

Saída esperada:

```
1 — antes de readFileSync
2 — arquivo lido, tamanho: <N>
3 — depois de readFileSync
```

Agora tudo é sequencial. `readFileSync` trava a thread até o I/O terminar. Em um servidor web, isso significa que todas as outras requisições pendentes ficam congeladas enquanto esse arquivo é lido.

### Diagrama — o que acontece por baixo

```
Thread JS (única)
│
├─► console.log('1')                  ← executa na thread JS
│
├─► fs.readFile(...)                  ← registra operação e retorna imediatamente
│       │
│       └─► Node Bindings (C++)
│               │
│               └─► libuv
│                       │
│                       └─► OS (kernel — multi-threaded)
│                               │
│                               │  [leitura do disco acontece aqui,
│                               │   em paralelo, fora da thread JS]
│                               │
│                               └─► notifica libuv quando pronto
│                                       │
│                                       └─► callback entra na fila do event loop
│
├─► console.log('2')                  ← executa na thread JS (enquanto OS trabalha)
│
│   [event loop pega o callback da fila]
│
└─► callback(err, conteudo)           ← executa na thread JS
        │
        └─► console.log('3')
```

A thread JS nunca para. Ela registra, processa outras coisas, e retoma o callback quando o OS sinaliza que terminou.

## Na prática

### Comparação com o modelo thread-per-request

Em servidores como Apache (modo prefork) ou Tomcat (configuração padrão), cada requisição recebe sua própria thread do pool:

```
Modelo thread-per-request (Apache prefork / Tomcat default):

Req 1 ──► Thread 1 [======= aguarda DB =======] ──► responde
Req 2 ──► Thread 2 [===== aguarda arquivo =====] ──► responde
Req 3 ──► Thread 3 [======= aguarda API =======] ──► responde
Req 4 ──► Thread 4 [aguarda ...]
...
Req N ──► aguarda thread disponível no pool
```

Cada thread consome memória de stack mesmo quando está bloqueada esperando I/O. Uma thread Java, por padrão, reserva entre 256 KB e 512 KB de stack. Com 1.000 conexões simultâneas, isso representa entre 256 MB e 512 MB só de overhead de stacks — antes de qualquer dado da aplicação.

```
Modelo Node.js (event loop + non-blocking I/O):

Req 1 ──► registra I/O ──► (OS trabalha) ──► callback na fila
Req 2 ──► registra I/O ──► (OS trabalha) ──► callback na fila
Req 3 ──► registra I/O ──► (OS trabalha) ──► callback na fila
...
Req N ──► registra I/O ──► (OS trabalha) ──► callback na fila

Thread JS: processa callbacks conforme chegam — uma de cada vez, sem bloqueio
```

Uma conexão inativa em Node não retém uma thread — ela consome apenas alguns bytes no objeto de socket do event loop.

### Quando cada modelo ganha

**Node ganha em:**
- APIs REST de alta concorrência (padrão observado em libs do ecossistema: Express, Fastify, NestJS)
- Gateways e proxies reversos
- Servidores de WebSocket / real-time (chat, notificações, dashboards ao vivo)
- BFFs que agregam múltiplas APIs downstream
- Caso típico em microserviços I/O-bound: o serviço passa >80% do tempo aguardando respostas de outros serviços ou do banco

**Thread-per-request ganha em:**
- Aplicações CPU-bound intensas (processamento de imagem, transcodificação de vídeo, ML)
- Workloads onde cada requisição faz computação pesada e continuada
- Ambientes onde Virtual Threads (Java 21+) ou goroutines (Go) entregam concorrência sem o overhead de threads nativas

> Imagine um servidor que processa uploads de imagem com redimensionamento em tempo real. Para cada upload, ele executa um algoritmo pesado de compressão. Nesse cenário, a única thread JS ficaria ocupada com o CPU durante cada requisição, e as demais ficariam na fila esperando. Aqui, Go ou Java com Virtual Threads seriam escolhas mais adequadas.

## Armadilhas

### 1. Achar que `async`/`await` cria uma nova thread

`async`/`await` é açúcar sintático sobre Promises — não cria thread alguma. O código ainda roda na mesma thread JS única. A ilusão de paralelismo vem do fato de que operações I/O são delegadas ao OS, não de que `async` distribui trabalho entre threads.

```javascript
// Isso NÃO cria uma thread nova.
// O await apenas suspende a função e devolve o controle ao event loop
// até o I/O completar.
async function buscaDados() {
  const resultado = await fetch('https://api.exemplo.com/dados'); // I/O delegado ao OS
  return resultado.json(); // executa de volta na thread JS quando pronto
}
```

A nota [[09 - async-await - o que é, o que não é]] aprofunda essa distinção com exemplos de execução passo a passo.

### 2. Assumir que todo I/O em Node é non-blocking

Node oferece versões síncronas (bloqueantes) de muitas APIs — e elas existem intencionalmente (úteis em scripts de inicialização, por exemplo). O sufixo `Sync` é o sinal de alerta:

```javascript
// Bloqueia a thread JS — NUNCA use em código de servidor em produção
const dados = fs.readFileSync('./config.json', 'utf8');
const conteudo = require('node:fs').readFileSync('./outro.txt');

// DNS síncrono — raramente usado, mas existe
const enderecos = require('node:dns').lookupSync('exemplo.com');
```

Usar `readFileSync`, `writeFileSync`, ou qualquer `*Sync` dentro de um handler de requisição HTTP trava o event loop para todas as conexões ativas durante a duração dessa leitura. Em produção, isso manifesta como latência súbita e inexplicável sob carga.

A nota [[10 - Bloqueio do event loop - sintomas e causas]] cobre como diagnosticar esse problema.

### 3. Confundir "single-threaded" com "single-process"

Node é single-threaded para código JS, mas o processo Node não é de thread única internamente. libuv mantém um thread pool (4 threads por padrão, configurável via `UV_THREADPOOL_SIZE`) para operações que o kernel não suporta de forma assíncrona nativa — como algumas operações de filesystem e DNS. O código JS nunca interage diretamente com esse pool; ele é um detalhe de implementação de libuv. A nota [[02 - V8, libuv e thread pool]] explora isso em detalhe.

## Em entrevista

### Frase pronta (inglês)

> "Node.js uses a single-threaded event loop with non-blocking I/O. The JS thread never blocks on I/O — it delegates to the OS via libuv and registers a callback. This is what allows a single process to handle thousands of concurrent connections without thread-per-request overhead."

Use essa frase como abertura quando perguntarem "How does Node.js handle concurrency?" ou "Explain Node.js's threading model." Em seguida, esteja pronto para aprofundar qualquer ponto: o que acontece com CPU-bound, como o event loop organiza os callbacks, ou por que `async`/`await` não cria threads.

### Vocabulário de entrevista

| Termo em inglês | Equivalente / contexto |
|---|---|
| **single thread** | thread única — a única thread que executa código JS |
| **non-blocking I/O** | I/O não-bloqueante — chamadas de I/O retornam imediatamente |
| **event-driven model** | modelo orientado a eventos — o fluxo é guiado por callbacks enfileirados pelo event loop |
| **concurrent connections** | conexões concorrentes — múltiplas conexões ativas simultaneamente sem uma thread por conexão |
| **callback** | função registrada para execução futura quando uma operação assíncrona completa |
| **libuv** | biblioteca C que implementa o event loop e abstrai I/O assíncrono cross-platform |
| **thread pool** | pool de threads interno do libuv para operações sem suporte nativo assíncrono no kernel |

### Perguntas de follow-up comuns

- *"What happens when you have a CPU-intensive operation in Node?"* → A thread JS fica ocupada, novas requisições não são processadas. Solução: Worker Threads, child_process, ou offload para serviço separado.
- *"Is Node.js truly single-threaded?"* → Para código JS, sim. Internamente, libuv usa um thread pool para operações específicas — mas o JS nunca interage com essas threads diretamente.
- *"When would you NOT use Node.js?"* → CPU-bound workloads — image processing, video transcoding, ML inference — onde Go, Rust ou Java com Virtual Threads são mais adequados.

## Veja também

- [[02 - V8, libuv e thread pool]] — como V8 e libuv dividem o trabalho; o que o thread pool realmente faz
- [[09 - async-await - o que é, o que não é]] — por que `async` não cria threads; o que `await` realmente faz
- [[10 - Bloqueio do event loop - sintomas e causas]] — como detectar e corrigir código que trava a thread JS
- [[Node.js]] — tronco: panorama completo do runtime (V8, fases do event loop, streams, frameworks)
- [[JavaScript Fundamentals]] — fundamentos JS: call stack, heap, event loop básico
