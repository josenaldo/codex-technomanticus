---
title: "Armadilhas, regras práticas, cheatsheet"
created: 2026-05-07
updated: 2026-05-07
type: concept
status: seedling
publish: true
tags:
  - node
  - paralelismo
  - cheatsheet
  - armadilhas
  - referencia
aliases:
  - Cheatsheet paralelismo
  - Armadilhas Node paralelismo
---

# Armadilhas, regras práticas, cheatsheet

> [!abstract] TL;DR
> Nota de fechamento do galho 2. Top 10 armadilhas extraídas das notas 01–11, tabela ferramenta×atributo, decision tree compactada em 1 tela, vocabulário PT→EN consolidado do galho (19 termos), e próximos galhos recomendados (Streams, Observability, Segurança).

---

## Top 10 armadilhas

### 1. Worker sem `terminate` em shutdown → leak de threads

**Problema:** Workers ativos impedem o processo de encerrar. Sem cleanup explícito no SIGTERM, threads ficam órfãs e o processo trava no shutdown.

```javascript
// ❌ pool criado, nunca destruído
const pool = new Piscina({ filename: './worker.js' });
```

**Fix:**

```javascript
process.on('SIGTERM', async () => {
  await pool.destroy();       // piscina
  // ou: await worker.terminate(); // Worker individual
  process.exit(0);
});
```

---

### 2. IPC leak — mensagens acumulando na fila quando child não lê → memory growth

**Problema:** O canal IPC entre pai e filho tem buffer. Se o pai envia mensagens mais rápido do que o filho as consome, a fila cresce sem limite. O processo cresce em memória silenciosamente.

```javascript
// ❌ parent envia sem backpressure
setInterval(() => child.send(grandeBatch), 10);
// filho processa a 1/s — fila cresce 100x por segundo
```

**Fix:** implementar backpressure (aguardar `drain` ou confirmação do filho antes de enviar o próximo lote), ou fechar o canal após a troca de dados com `child.disconnect()`.

---

### 3. Race condition em `SharedArrayBuffer` sem `Atomics` → corrupção de estado

**Problema:** Duas threads lendo e escrevendo no mesmo índice de um SAB sem coordenação. As operações `view[0]++` não são atômicas — são três instruções de CPU. Com duas threads em paralelo, o resultado é imprevisível.

```javascript
// ❌ não atômico — race condition garantida com 2+ workers
const view = new Int32Array(sab);
view[0]++;
```

**Fix:**

```javascript
// ✓ sempre Atomics para leitura e escrita compartilhada
Atomics.add(view, 0, 1);
// ou: Atomics.load / Atomics.store / Atomics.compareExchange
```

---

### 4. `exec` com input do usuário → shell injection

**Problema:** `child_process.exec` sempre invoca um shell (`/bin/sh`). Input não sanitizado pode injetar comandos arbitrários.

```javascript
// ❌ CVE esperando para acontecer
exec(`convert ${req.body.filename} output.png`);
// filename = 'x; rm -rf /'  → desastre
```

**Fix:**

```javascript
// ✓ execFile ou spawn com array de args — sem shell, sem injeção
execFile('convert', [req.body.filename, 'output.png']);
// ou: spawn('convert', [req.body.filename, 'output.png'])
```

---

### 5. Cluster com estado em memória (cache local) → comportamento inconsistente entre workers

**Problema:** Cluster cria N processos independentes. Estado em memória (Map, objeto global, cache) existe separadamente em cada worker. Requisições para o mesmo endpoint chegam em workers diferentes — o estado nunca converge.

```javascript
// ❌ cada worker tem seu próprio Map — 4 workers = 4 caches desconexos
const cache = new Map();
app.get('/item/:id', (req, res) => {
  if (cache.has(req.params.id)) return res.json(cache.get(req.params.id));
  // ...
});
```

**Fix:** estado compartilhado em camada externa — Redis, banco de dados, ou serviço dedicado. Nenhuma escrita crítica em memória de processo worker.

---

### 6. Fork sem cleanup de child em parent crash → processos zumbi

**Problema:** Se o processo pai crasha sem sinalizar os filhos, os filhos ficam órfãos — rodando sem supervisão, consumindo recursos, sem chance de encerramento gracioso.

```javascript
// ❌ nenhum handler de cleanup no pai
const child = fork('./worker.js');
// pai crasha → child continua vivo indefinidamente
```

**Fix:**

```javascript
// ✓ cleanup explícito em sinais do pai
process.on('SIGTERM', () => {
  child.kill('SIGTERM');
  process.exit(0);
});
process.on('exit', () => child.kill());
```

---

### 7. `transferList` esquecido em buffer grande → cópia silenciosa de bytes

**Problema:** `postMessage(buf)` sem `[buf]` no segundo argumento faz uma cópia completa do `ArrayBuffer`. Com buffers de imagem, áudio ou ML de dezenas de MB, o heap cresce o dobro por alguns milissegundos. Sem aviso em runtime — o código funciona, mas é lento.

```javascript
// ❌ cópia silenciosa de 100 MB
worker.postMessage(imagemBuffer);
```

**Fix:**

```javascript
// ✓ transferência zero-copy — original fica detached
worker.postMessage(imagemBuffer, [imagemBuffer]);
```

---

### 8. Worker preso em loop síncrono → mensagens não processadas, terminate é única saída

**Problema:** Um Worker em loop síncrono (`while(true)` ou cálculo sem pausa) não processa mensagens recebidas. O event loop do worker está travado. O pai não consegue encerrar cooperativamente — só `terminate()`, que é equivalente a SIGKILL.

```javascript
// ❌ loop síncrono bloqueia o event loop do worker
while (true) {
  processarChunk(dados);
}
// parentPort.on('message') nunca é alcançado
```

**Fix:** dividir o trabalho em chunks com pausas que liberam o event loop:

```javascript
// ✓ cede o event loop a cada chunk
async function processar(chunks) {
  for (const chunk of chunks) {
    processarChunk(chunk);
    await new Promise((r) => setImmediate(r)); // yield
  }
  parentPort.postMessage({ done: true });
}
```

---

### 9. Cluster + sticky sessions sem reverse proxy ciente → WebSocket quebra na troca de worker

**Problema:** WebSocket é uma conexão persistente. Se o reverse proxy não tem sticky sessions (affinity), requisições do mesmo cliente chegam em workers diferentes — e o handshake WebSocket não é reenviado. A conexão quebra ou fica em estado inválido.

**Fix:** configurar sticky sessions no reverse proxy:

```nginx
# nginx — ip_hash como afinidade básica
upstream node_cluster {
  ip_hash;
  server 127.0.0.1:3001;
  server 127.0.0.1:3002;
  server 127.0.0.1:3003;
  server 127.0.0.1:3004;
}
```

Ou usar `@socket.io/sticky` para afinidade baseada em cookie/sid, que é mais precisa que `ip_hash` atrás de NAT.

---

### 10. `spawn` com `shell: true` e input do usuário → shell injection idêntica ao `exec`

**Problema:** `spawn` sem `shell` é seguro. Com `shell: true`, o comportamento é idêntico ao `exec` — a string inteira é passada para `/bin/sh`. Qualquer input de usuário na string vira vetor de injeção.

```javascript
// ❌ shell: true anula a segurança do spawn
spawn('convert ' + req.body.filename + ' output.png', { shell: true });
```

**Fix:**

```javascript
// ✓ sem shell, args como array — nunca shell: true com input externo
spawn('convert', [req.body.filename, 'output.png']);
```

---

## Cheatsheet — 3 ferramentas × 5 atributos

| Atributo | Worker Thread | Cluster | child_process |
|---|---|---|---|
| **Modelo** | shared-memory (threads no mesmo processo) | shared-port (multi-processo, mesma porta TCP) | separate-process (isolamento total) |
| **Custo de criação** | ~1–5 ms por thread | ~100 ms por fork | ~100 ms por fork |
| **IPC / Comunicação** | `postMessage` / `SharedArrayBuffer` / `transferList` | IPC built-in (`worker.send` / `process.on('message')`) | stdio streams (`spawn`/`exec`) ou IPC (`fork`) |
| **Use case principal** | CPU-bound dentro de um handler ou job | Escalar servidor HTTP em single-VM sem orquestrador | Rodar comando externo (ffmpeg, python, git) ou Node filho isolado |
| **Lib de prod** | `piscina` (pool de workers) | PM2 em modo cluster (legacy) / orquestrador externo | — (use `execFile` ou `spawn` diretamente) |

> [!note] Regra rápida
> Worker Thread → CPU-bound. Cluster → HTTP scaling em single-VM. child_process → comando externo ou processo isolado.

---

## Decision tree compactada

```
Qual o problema?
│
├─ CPU-bound em handler ou job?
│   └─ Worker Thread
│       ├─ Alta carga / frequente? → pool via piscina (availableParallelism() workers)
│       └─ Esporádico? → Worker por task é OK
│
├─ Escalar HTTP além de 1 thread?
│   ├─ Tem orquestrador (K8s, ECS, Fly.io)? → não adicionar Cluster; 1 processo por pod
│   └─ Single-VM sem orquestrador? → Cluster (ou PM2 em modo cluster)
│
├─ Rodar comando externo (ffmpeg, git, python, imagemagick)?
│   ├─ Output grande (> 1 MB) ou processo longo? → spawn (streams)
│   ├─ Output pequeno, comando hardcoded? → exec
│   └─ Args vêm de input externo? → SEMPRE execFile ou spawn com array; NUNCA exec
│
└─ Spawnar processo Node filho isolado?
    ├─ CPU-bound sem necessidade de isolamento? → Worker Thread (mais leve)
    ├─ Isolamento total / native module legado / código não-confiável? → fork
    └─ Supervisor tree / processo descartável? → fork + backoff exponencial
```

> [!warning] Antes de percorrer a árvore
> 1. Medir: event loop lag, percentis de latência (p50/p95/p99), CPU por thread.
> 2. Identificar: CPU-bound ou I/O-bound?
> 3. Testar alternativas: streaming, paginação, refatoração, API async, `UV_THREADPOOL_SIZE`, fila de background.
> 4. Só então: percorrer a decision tree.

---

## Vocabulário PT→EN consolidado

| PT-BR | EN |
|---|---|
| paralelismo | parallelism |
| concorrência | concurrency |
| thread de trabalho | Worker Thread |
| porta-pai | parentPort |
| bifurcar | fork |
| spawnar | spawn |
| pool de workers | worker pool |
| memória compartilhada | shared memory |
| operação atômica | atomic operation |
| condição de corrida | race condition |
| comparar-e-trocar | compare-and-swap (CAS) |
| aguardar-notificar | wait-notify |
| porta compartilhada | shared port |
| comunicação interprocesso | inter-process communication (IPC) |
| injeção de shell | shell injection |
| zumbi | zombie process |
| encerramento gracioso | graceful shutdown |
| orquestrador | orchestrator |
| réplica | replica |

---

## Próximos galhos

### Galho 3 — Streams

Para **dados grandes sem bloquear o event loop**: Readable, Writable, Transform, backpressure. Quando `JSON.parse` de payload inteiro já é o gargalo e a solução é processar em chunks enquanto os bytes chegam.

### Galho 5 — Observability

Para **observar workers e cluster em produção**: métricas de pool (fila, idle workers, throughput), profiling de Worker Threads (V8 CPU profiler, Clinic.js), alertas em event loop lag, rastreamento distribuído entre processos.

### Galho 6 — Segurança

Para **isolamento e sandbox**: `vm` module, `isolated-vm` (V8 isolate sem acesso a APIs Node), Permission Model (Node 20+), execução de código não-confiável sem acesso ao sistema de arquivos ou rede.

---

## Veja também

- [[03-Dominios/Node/Paralelismo/index]] — MOC do galho 2
- [[01 - Por que paralelismo em Node]] — quando paralelizar; CPU-bound vs I/O-bound; sequência de diagnóstico
- [[02 - As 3 ferramentas - Worker Threads, Cluster, child_process]] — visão panorâmica dos 3 modelos
- [[03 - Worker Threads - fundamentos]] — criação, eventos de ciclo de vida, terminate
- [[04 - Comunicação entre workers - postMessage e MessageChannel]] — structured clone, transferList, MessageChannel
- [[05 - Memória compartilhada - SharedArrayBuffer e Atomics]] — SAB, Atomics, race conditions
- [[06 - Pool de workers - pattern de produção]] — piscina, sizing, graceful shutdown do pool
- [[07 - Cluster - escalando HTTP por CPU]] — port sharing, round-robin, sticky sessions
- [[08 - child_process com exec e spawn]] — segurança, maxBuffer, streams de output
- [[09 - child_process com fork - Node child com IPC]] — IPC bidirecional, supervisor tree
- [[10 - Cluster vs PM2 vs Kubernetes - quem orquestra]] — onde Cluster ainda faz sentido em 2026
- [[11 - Decision tree - qual ferramenta para qual problema]] — decision tree completa com tabela problema→ferramenta→razão
- [[Node.js]] — tronco da trilha Node Senior
- [[03-Dominios/Node/Runtime e Event Loop/index]] — galho 1: event loop, async/await, bloqueio — pré-requisito do galho 2
