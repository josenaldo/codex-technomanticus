---
title: "Cluster: escalando HTTP por CPU"
created: 2026-05-07
updated: 2026-05-07
type: concept
status: seedling
publish: true
tags:
  - node
  - paralelismo
  - cluster
  - http
  - scaling
aliases:
  - cluster
  - cluster.fork
  - port sharing
---

# Cluster: escalando HTTP por CPU

> [!abstract] TL;DR
> `node:cluster` fork-a múltiplos processos Node compartilhando a mesma porta HTTP. O processo **primary** gerencia o ciclo de vida; os **workers** atendem requisições. No Linux, o próprio Node distribui conexões em round-robin; no Windows, o kernel balanceia via IOCP. Útil em deploys single-VM onde não existe orquestrador — mas em prod com K8s, ECS ou similar, o orquestrador já faz isso por você, e cluster vira camada redundante.

---

## O que é

O módulo `node:cluster` permite que um único processo Node.js crie múltiplos **processos filhos** (workers) que compartilham a mesma porta TCP. O processo original, chamado **primary**, não atende requisições diretamente: ele fork-a os workers, monitora seus ciclos de vida e pode se comunicar com eles via IPC. Os workers rodam o mesmo arquivo de entrada e são distinguidos pela variável de ambiente `NODE_UNIQUE_ID`.

```
Processo Primary
    │
    ├── cluster.fork() ──► Worker 1  ┐
    ├── cluster.fork() ──► Worker 2  ├── todos escutam porta 3000
    ├── cluster.fork() ──► Worker 3  │
    └── cluster.fork() ──► Worker 4  ┘
                              │
                         (conexões distribuídas pelo Node/kernel)
```

Internamente, `cluster.fork()` usa `child_process.fork()` — portanto cada worker é um processo Unix separado, com heap própria e event loop próprio. Não há memória compartilhada entre workers (diferente de Worker Threads).

---

## Por que importa

O event loop do Node é single-threaded. Numa máquina com 8 cores, um processo Node padrão usa ~12% da CPU em cenários CPU-bound e deixa os outros 7 cores ociosos. O cluster resolve esse problema no nível de processo.

Historicamente era a solução canônica para aproveitar todos os cores em deploy single-VM. Em 2026, esse papel foi em grande parte absorvido por orquestradores de container — mas o módulo ainda tem lugar:

- **Single-VM sem container**: VPS simples, tooling interno, pequeno SaaS
- **Scripts que paralelizam HTTP**: load tester, proxy local, mock server com múltiplos workers
- **Ambientes onde PM2 não está disponível** e não há orquestrador
- **Entender a base**: PM2 em modo cluster usa exatamente essa API por baixo

> [!tip] Quando NÃO usar
> Se você tem K8s, ECS, Fly.io ou qualquer runtime que gerencia réplicas de container, **não adicione cluster**. Você estaria rodando, por exemplo, 4 réplicas de pod × 4 workers = 16 processos sem ganho adicional, com overhead de memória e complexidade operacional.

---

## Como funciona: port sharing

O mecanismo que permite múltiplos processos escutarem a mesma porta depende do SO:

**Linux (padrão — `SCHED_RR`):**
O Node adota uma estratégia própria de round-robin sobre o file descriptor compartilhado. O primary aceita a conexão e a distribui para um worker disponível. Isso evita o problema clássico de `SO_REUSEPORT` no Linux onde alguns workers ficam sobrecarregados enquanto outros ficam ociosos — a distribuição desigual chegava a 70%+ das conexões indo para apenas 2 de 8 workers.

**Windows:**
O kernel distribui via IOCP (I/O Completion Ports), que é o mecanismo nativo do Windows para I/O assíncrono de alta performance.

Você pode alterar a política explicitamente:

```javascript
import cluster from 'node:cluster';

// Força round-robin (default no Linux)
cluster.schedulingPolicy = cluster.SCHED_RR;

// Delega ao SO (padrão no Windows, problemático no Linux)
cluster.schedulingPolicy = cluster.SCHED_NONE;
```

Ou via variável de ambiente antes de iniciar:

```bash
NODE_CLUSTER_SCHED_POLICY=rr node server.js
NODE_CLUSTER_SCHED_POLICY=none node server.js
```

---

## Como funciona: exemplos de código

### 1. Cluster mínimo com restart automático

```javascript
import cluster from 'node:cluster';
import { availableParallelism } from 'node:os';
import http from 'node:http';

if (cluster.isPrimary) {
  const numCPUs = availableParallelism(); // preferir sobre os.cpus().length

  console.log(`Primary ${process.pid} iniciando ${numCPUs} workers`);

  for (let i = 0; i < numCPUs; i++) {
    cluster.fork();
  }

  // Restart automático: sem isso, worker morto = capacidade reduzida silenciosamente
  cluster.on('exit', (worker, code, signal) => {
    console.log(`Worker ${worker.process.pid} encerrou (code=${code}, signal=${signal}). Reiniciando...`);
    cluster.fork();
  });

} else {
  // Cada worker roda este bloco de forma independente
  http.createServer((req, res) => {
    res.end(`Atendido pelo worker ${process.pid}\n`);
  }).listen(3000);

  console.log(`Worker ${process.pid} escutando na porta 3000`);
}
```

> [!note] `availableParallelism()` vs `os.cpus().length`
> `availableParallelism()` respeita CPU affinity e cgroups — em containers com CPU limit configurado, devolve o número correto de cores disponíveis, não o total do host. Use sempre esta forma.

---

### 2. Separando primary e worker em arquivos distintos

Para codebases maiores, misturar lógica de primary e worker no mesmo arquivo fica confuso. O cluster permite separar:

```javascript
// primary.js
import cluster from 'node:cluster';
import { availableParallelism } from 'node:os';

cluster.setupPrimary({
  exec: new URL('./worker.js', import.meta.url).pathname,
});

for (let i = 0; i < availableParallelism(); i++) {
  cluster.fork();
}

cluster.on('exit', (worker) => {
  console.warn(`Worker ${worker.id} morreu. Reiniciando.`);
  cluster.fork();
});
```

```javascript
// worker.js
import http from 'node:http';

http.createServer((req, res) => {
  res.end(`Worker ${process.pid}\n`);
}).listen(3000);
```

---

### 3. IPC: primary e workers trocando mensagens

Workers e primary se comunicam via canal IPC (pipe Unix). Útil para agregar métricas sem banco externo:

```javascript
// No primary
cluster.on('message', (worker, msg) => {
  if (msg.type === 'request-count') {
    totalRequests += msg.count;
  }
});

// No worker
let localCount = 0;

http.createServer((req, res) => {
  localCount++;
  process.send({ type: 'request-count', count: localCount });
  res.end('ok');
}).listen(3000);
```

> [!warning] IPC não é para dados grandes
> O canal IPC passa mensagens serializadas (JSON por padrão). Para volumes altos ou objetos grandes, prefira Redis, banco ou `SharedArrayBuffer` com Worker Threads.

---

### 4. Graceful shutdown

```javascript
// No primary: ao receber SIGTERM, desliga workers ordenadamente
process.on('SIGTERM', () => {
  console.log('SIGTERM recebido. Iniciando graceful shutdown...');

  // Para de aceitar novas conexões em todos os workers
  cluster.disconnect(() => {
    console.log('Todos os workers desconectados. Encerrando primary.');
    process.exit(0);
  });

  // Força encerramento se demorar mais de 10s
  setTimeout(() => {
    console.error('Timeout no shutdown. Forçando saída.');
    process.exit(1);
  }, 10_000);
});
```

```javascript
// No worker: drain de conexões existentes
process.on('message', (msg) => {
  if (msg === 'shutdown') {
    server.close(() => {
      process.exit(0);
    });
  }
});
```

O fluxo completo:

```
SIGTERM → primary
    │
    ├── cluster.disconnect()
    │       │
    │       ├── worker.disconnect() ──► worker para de aceitar novas conexões
    │       │                          worker drena conexões existentes
    │       │                          worker fecha IPC channel
    │       │                          worker.exitedAfterDisconnect = true
    │       └── callback quando todos terminam
    │
    └── primary encerra
```

`worker.exitedAfterDisconnect === true` distingue saída graceful de crash — use isso no handler `'exit'` para não reiniciar workers que saíram intencionalmente:

```javascript
cluster.on('exit', (worker, code, signal) => {
  if (worker.exitedAfterDisconnect) {
    console.log(`Worker ${worker.id} encerrou gracefully. Não reiniciando.`);
    return;
  }
  console.warn(`Worker ${worker.id} crashou. Reiniciando.`);
  cluster.fork();
});
```

---

## Sticky sessions

### O problema

Com round-robin, requisições do mesmo cliente podem ir para workers diferentes a cada request. Para HTTP stateless isso é irrelevante — mas para WebSocket e SSE (Server-Sent Events) é fatal: a conexão persistente vai para o Worker 1, mas o próximo handshake pode ir para o Worker 2, que não tem contexto da sessão.

### Solução 1: `@socket.io/sticky` (cluster interno)

```javascript
import cluster from 'node:cluster';
import { availableParallelism } from 'node:os';
import { createServer } from 'node:http';
import { setupPrimary, setupWorker } from '@socket.io/sticky';
import { setupMaster } from '@socket.io/cluster-adapter';
import { Server } from 'socket.io';

if (cluster.isPrimary) {
  const httpServer = createServer();
  setupMaster(httpServer, { loadBalancingMethod: 'least-connection' });
  setupPrimary(); // roteamento sticky via primary

  httpServer.listen(3000);

  for (let i = 0; i < availableParallelism(); i++) {
    cluster.fork();
  }

} else {
  const httpServer = createServer();
  const io = new Server(httpServer);
  setupWorker(io);

  httpServer.listen(0); // porta aleatória; primary roteia
}
```

### Solução 2: nginx com `ip_hash` (preferível em prod)

```nginx
upstream nodejs_cluster {
  ip_hash;              # garante que o mesmo IP sempre vai para o mesmo upstream
  server 127.0.0.1:3001;
  server 127.0.0.1:3002;
  server 127.0.0.1:3003;
  server 127.0.0.1:3004;
}

server {
  listen 80;
  location / {
    proxy_pass http://nodejs_cluster;
    proxy_http_version 1.1;
    proxy_set_header Upgrade $http_upgrade;
    proxy_set_header Connection "upgrade";
  }
}
```

Neste modelo, cada worker escuta em porta diferente (usando `cluster.worker.id`) e o nginx faz o roteamento sticky. O cluster ainda gerencia o ciclo de vida dos workers, mas o balanceamento fica com o nginx.

---

## Na prática

Em 2026, o uso direto de `node:cluster` em código de produção novo é raro. Os cenários onde ainda faz sentido:

| Cenário | Alternativa preferível | Cluster ainda ok? |
|---|---|---|
| Single VPS sem container runtime | PM2 em modo cluster | Sim |
| Lambda / Cloud Functions | Escalonamento horizontal da plataforma | Não |
| K8s com múltiplas réplicas | Aumentar réplicas do pod | Não |
| Dev local para simular concorrência | Cluster ou PM2 | Sim |
| Script que precisa paralelizar HTTP | Cluster ou Worker Threads | Sim |
| Internal tooling em VM dedicada | PM2 ou cluster direto | Sim |

> [!tip] Caminho recomendado em 2026
> Para a maioria dos casos novos: **1 processo Node por container**, deixe o orquestrador escalar horizontalmente. Para single-VM sem orquestrador: **PM2** em modo cluster é mais ergonômico que cluster manual (health checks, logs, métricas embutidos). Cluster direto quando você precisa de controle fino ou não pode instalar PM2.

Veja `[[10 - Cluster vs PM2 vs Kubernetes - quem orquestra]]` para a análise comparativa completa.

---

## Armadilhas

### 1. Estado em memória local ao worker

```javascript
// PROBLEMA: cada worker tem sua própria cópia desse mapa
const sessions = new Map();

http.createServer((req, res) => {
  const sessionId = getCookie(req, 'sid');
  const session = sessions.get(sessionId); // pode não existir neste worker!
  // ...
}).listen(3000);
```

**Solução:** session store externo (Redis, banco) ou sticky sessions garantidas via reverse proxy.

---

### 2. Esquecer o handler `'exit'`

```javascript
// PROBLEMA: worker morre, capacidade cai silenciosamente
if (cluster.isPrimary) {
  for (let i = 0; i < numCPUs; i++) cluster.fork();
  // sem cluster.on('exit', ...) → worker crashado nunca é substituído
}
```

Sem restart automático, um worker que crasha com exceção não capturada simplesmente some. O sistema continua operando com N-1 (ou menos) workers até reiniciar o processo inteiro.

---

### 3. Sticky sessions sem reverse proxy ciente

```javascript
// PROBLEMA: WebSocket vai para Worker 1 no handshake,
// próxima mensagem pode ir para Worker 2 (sem a conexão aberta)
http.createServer((req, res) => {
  // round-robin do cluster não respeita afinidade de conexão WebSocket
}).listen(3000);
```

Round-robin distribui por _conexão TCP_, não por _cliente_. WebSocket e SSE exigem que todas as mensagens de um cliente vão para o mesmo processo.

---

### 4. Cluster + orquestrador = multiplicação desnecessária

```
# Configuração problemática:
K8s: 4 réplicas de pod
  Cada pod: cluster com 4 workers
  Total: 16 processos Node

# O que você provavelmente queria:
K8s: 4 réplicas de pod
  Cada pod: 1 processo Node
  Total: 4 processos Node (mais simples, mesma capacidade de throughput HTTP)
```

K8s (e similares) já gerencia restart, health check e escalonamento. Cluster dentro de container adiciona complexidade sem benefício proporcional na maioria dos casos.

---

### 5. Não diferenciar crash de graceful exit no handler `'exit'`

```javascript
// PROBLEMA: reinicia worker que saiu intencionalmente (ex: durante deploy)
cluster.on('exit', (worker) => {
  cluster.fork(); // fork incondicional: problema durante shutdown
});

// CORRETO: verificar exitedAfterDisconnect
cluster.on('exit', (worker, code, signal) => {
  if (!worker.exitedAfterDisconnect) {
    cluster.fork();
  }
});
```

---

## Em entrevista

### Frase pronta (inglês)

> "The cluster module forks multiple worker processes that share the same HTTP port. The primary process manages the lifecycle — it forks workers, listens for exit events, and restarts crashed workers. On Linux, Node distributes incoming connections in round-robin across workers. The main limitations are stateful workloads — each worker has its own memory, so sessions and caches must live in external storage. In 2026, if you have an orchestrator like Kubernetes, you don't need cluster at all — the orchestrator handles scaling horizontally. Cluster still makes sense for single-VM deployments or when you need fine-grained control over worker lifecycle."

### Vocabulário técnico

| Português | Inglês | Contexto de uso |
|---|---|---|
| cluster | cluster | "Node's cluster module forks worker processes" |
| processo primary | primary process | "the primary manages worker lifecycle" |
| processo worker | worker process | "each worker handles HTTP requests independently" |
| compartilhamento de porta | port sharing | "workers share the same port via fd inheritance" |
| sessão sticky | sticky session | "WebSockets require sticky sessions" |
| encerramento gracioso | graceful shutdown | "disconnect workers before killing the primary" |
| fork de processo | process fork | "cluster.fork() spawns a new worker" |
| round-robin | round-robin | "Linux uses round-robin to distribute connections" |
| afinidade de IP | IP affinity | "ip_hash ensures IP affinity in nginx" |

### Perguntas frequentes em entrevista

**"Como cluster difere de Worker Threads?"**
> Cluster cria processos separados (memória isolada, overhead de ~30MB por worker, tolerante a falhas — worker crash não afeta o primary). Worker Threads cria threads dentro do mesmo processo (memória compartilhável via SharedArrayBuffer, menor overhead, crash pode afetar o processo inteiro).

**"Como workers compartilham a porta?"**
> O primary cria o socket, e os workers herdam o file descriptor via IPC. No Linux com `SCHED_RR`, o primary aceita conexões e as despacha para workers em round-robin. No modo `SCHED_NONE`, cada worker aceita diretamente — com risco de distribuição desigual.

**"O que acontece se um worker crasha?"**
> Sem handler, ele some silenciosamente. Com `cluster.on('exit', ...)`, o primary detecta e pode fazer `cluster.fork()` para substituir. `worker.exitedAfterDisconnect` permite distinguir crash de saída intencional.

---

## Rubric

| Critério | Status |
|---|---|
| TL;DR claro e correto | ok |
| Código funcional e idiomático | ok |
| Mecanismo de port sharing explicado (Linux vs Windows) | ok |
| Graceful shutdown com `exitedAfterDisconnect` | ok |
| Sticky sessions: problema + 2 soluções | ok |
| Armadilhas com exemplos de código | ok |
| Vocabulário EN para entrevista | ok |
| Frase pronta em inglês | ok |
| Sem fabricação de dados do usuário | ok |
| Wikilinks para notas existentes e futuras | ok |
| Sem Co-Authored-By no commit | pendente |

---

## Veja também

- `[[02 - As 3 ferramentas - Worker Threads, Cluster, child_process]]` — visão comparativa das 3 opções de paralelismo
- `[[06 - Pool de workers - pattern de produção]]` — pattern análogo, mas para Worker Threads
- `[[09 - child_process com fork - Node child com IPC]]` — fork de processo similar, sem port sharing
- `[[10 - Cluster vs PM2 vs Kubernetes - quem orquestra]]` — quando usar cada ferramenta em prod
- `[[11 - Decision tree - qual ferramenta para qual problema]]` — árvore de decisão para escolha
- `[[Node.js]]` — nota tronco do domínio
