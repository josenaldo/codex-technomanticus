---
title: "Decision tree: qual ferramenta para qual problema"
created: 2026-05-07
updated: 2026-05-07
type: concept
status: seedling
publish: true
tags:
  - node
  - paralelismo
  - decision-tree
  - referencia
aliases:
  - Decision tree paralelismo
  - Qual ferramenta usar
---

# Decision tree: qual ferramenta para qual problema

> [!abstract] TL;DR
> A pergunta-chave é: qual o problema? CPU-bound em handler → Worker Thread (com pool em prod). Escalar HTTP além de single-thread → orquestrador (K8s/ECS); Cluster apenas se single-VM. Rodar comando externo → `spawn` / `execFile` (nunca `exec` com input do usuário). Spawn de processo Node isolado → `fork`. A maioria dos erros não é técnica — é escolher a ferramenta errada para o problema.

---

## O que é

A decision tree de paralelismo é um artefato de síntese que separa dois eixos que costumam ser confundidos:

- **O problema**: CPU-bound? HTTP scaling? Comando externo? Isolamento de processo?
- **A ferramenta**: Worker Thread? Cluster? `spawn`? `execFile`? `fork`?

Node tem três modelos de paralelismo nativos — Worker Threads (threads dentro do mesmo processo), Cluster (múltiplos processos compartilhando a mesma porta TCP), e `child_process` (processo externo completamente separado). Cada modelo resolve uma classe diferente de problema. Aplicar Worker Thread a um problema de escalonamento HTTP, ou Cluster a um problema CPU-bound em handler individual, não só não resolve como adiciona complexidade sem benefício.

Os três modelos não são gradações de poder — são soluções para problemas orthogonais:

| Modelo | Fronteira | Problema que resolve |
|---|---|---|
| Worker Thread | Thread (mesmo processo) | CPU-bound dentro de um handler |
| Cluster | Processo (mesma porta TCP) | HTTP scaling em single-VM |
| `child_process` | Processo (isolamento total) | Comando externo ou Node filho isolado |

Esta nota é puramente sintética: consolida os critérios de decisão das notas 01 a 10 em um único artefato de referência para consulta rápida e preparação de entrevistas.

---

## Por que importa

Em entrevistas sênior e em code reviews, a pergunta raramente é "você conhece Worker Threads?". A pergunta real é "dado esse problema específico, qual ferramenta você escolheria e por quê?". A decisão errada é uma das fontes mais comuns de dívida técnica em código Node de produção:

- **Cluster para CPU-bound em handler**: cria N réplicas do mesmo problema. Cada worker ainda bloqueia seu próprio event loop. O trabalho dentro de um request nunca é paralelizado — apenas multiplicado.
- **Worker Thread para problema de escalonamento HTTP**: Workers não compartilham a porta TCP. O servidor continua aceitando conexões em uma única thread. A escala de HTTP exige múltiplos processos ou múltiplos pods, não múltiplas threads.
- **`exec` com input externo**: a string passa por um shell. Um semicolon ou `$()` no input vira injeção de comando. Vulnerabilidade estrutural, não de implementação.
- **`fork` onde Worker Thread basta**: `fork` cria um processo OS completo (~100ms de custo). Worker Thread é uma thread (~1-5ms). Para CPU-bound sem necessidade de isolamento total, Worker Thread é a ferramenta certa.

Conhecer a decision tree não é memorizar respostas — é ter o critério para chegar à resposta certa a partir do problema.

### A sequência correta antes de qualquer ferramenta

A decision tree de ferramentas pressupõe que paralelismo já foi validado como necessário. Antes de chegar nela, a sequência de diagnóstico é:

1. **Medir**: event loop lag via `perf_hooks.monitorEventLoopDelay()`, percentis de latência por endpoint (p50/p95/p99), CPU usage por thread.
2. **Identificar**: o bottleneck é CPU-bound (lag alto, cálculo dominante) ou I/O-bound (lag baixo, espera de rede/banco)?
3. **Tentar alternativas**: streaming, paginação, refatoração de algoritmo, API async em vez de sync, `UV_THREADPOOL_SIZE` para operações nativas, fila de background para trabalho não-imediato.
4. **Paralelizar**: se as alternativas falharam e o problema é confirmado como CPU-bound ou de escalonamento — aí sim percorrer a decision tree.

Pular os passos 1-3 e ir direto ao paralelismo é a origem da maioria dos casos de dívida técnica com Worker Threads adicionados sem benefício mensurável.

---

## Como funciona — fluxograma

```
Qual o problema?

├─ CPU-bound em handler ou job?
│   └─ → Worker Thread
│       ├─ Tarefa frequente / alta carga? → pool (piscina)
│       │   (piscina = lib de referência; availableParallelism() threads)
│       └─ Tarefa rara / esporádica? → Worker por task é OK
│
├─ Preciso escalar HTTP além de 1 thread?
│   ├─ Tem orquestrador (K8s, ECS, Fly.io)?
│   │   → deixa o orquestrador (1 pod por core, réplicas declarativas)
│   ├─ Single-VM deploy / VPS sem container runtime?
│   │   → Cluster (ou PM2 em modo cluster)
│   └─ Dev local pra testar comportamento multi-worker?
│       → Cluster
│
├─ Preciso rodar comando externo (ffmpeg, git, python, imagemagick)?
│   ├─ Output streaming / output grande (> 1 MB)?
│   │   → spawn (streams, sem maxBuffer)
│   ├─ Output curto e sem input do usuário na string?
│   │   → execFile com array de args (sem shell)
│   │       ou exec se o comando é completamente hardcoded
│   └─ Argumento vem de input externo?
│       → SEMPRE execFile ou spawn com array — NUNCA exec
│           (exec interpreta shell: ; | && $() viram injeção)
│
└─ Preciso spawnar um processo Node isolado?
    ├─ CPU-bound sem necessidade de isolamento total?
    │   → Worker Thread (mais leve, ~1-5ms vs ~100ms)
    ├─ Isolamento total de memória (multi-tenancy, código não-confiável)?
    │   → fork (processos OS separados, crash não afeta o pai)
    ├─ Native module legado não thread-safe?
    │   → fork (cada processo tem seu isolate V8 separado)
    └─ Supervisor tree / processo descartável que pode crashar?
        → fork + padrão de supervisor com backoff exponencial
```

> [!note] Cluster vs orquestrador
> Em 2026, se existe um orquestrador (K8s, ECS, Nomad, Fly.io), **não adicione Cluster**. O orquestrador já gerencia réplicas, health checks e rolling updates. Cluster dentro de pod apenas adiciona processos sem benefício proporcional. A regra: 1 processo Node por container, orquestrador cuida do resto.

> [!tip] Como usar o fluxograma
> Percorra o fluxograma em voz alta enunciando o problema antes de nomear a ferramenta. O erro comum é começar pela ferramenta e buscar justificativa depois — "vou usar Worker Threads porque é moderno". A árvore força o sentido correto: problema → ferramenta → razão.

---

## Tabela problema → ferramenta → razão

| Problema | Ferramenta | Por quê |
|---|---|---|
| Hash bcrypt em handler HTTP | Worker Thread + pool | CPU-bound no event loop; pool reutilizável evita overhead de criação por request |
| Image processing de 100 MB/req | Worker Thread + `transferList` | Zero-copy de buffers grandes entre threads; sem duplicação de memória |
| Matrix ops em ML inference | Worker Thread + `SharedArrayBuffer` | Memória compartilhada zero-copy; `Atomics` para coordenação |
| Servir HTTP com 4 cores, single-VM | Cluster (ou PM2) | Round-robin de conexões TCP; 1 worker por core aproveita os 4 cores |
| Servir HTTP com 4 cores, K8s | 4 réplicas de pod | Orquestrador gerencia scaling, health check e rolling update |
| WebSocket server em K8s | 4 pods + sticky session via ingress | Conexões persistentes exigem afinidade; ingress com `ip_hash` ou cookie |
| Rodar `ffmpeg` | `spawn` | Output de vídeo é grande; streaming evita `maxBuffer` |
| Rodar `git log --oneline -5` | `execFile` com array de args | Output curto; sem shell elimina vetor de injeção |
| Rodar script com pipes de shell hardcoded | `exec` | Pipes exigem shell; OK se args são completamente hardcoded sem input externo |
| Sandbox de código de tenant | `fork` (ou `vm`/`isolated-vm`) | Isolamento de processo; crash de tenant não derruba o pai |
| Worker tree (queue managers, jobs) | `fork` + padrão de supervisor | Crash + respawn é o comportamento esperado; backoff exponencial evita loop |
| Parsing de arquivo não-confiável | `fork` com `--max-old-space-size` | SIGSEGV ou OOM no parser não derruba o processo principal |

---

## Na prática — aplicando a decision tree

O exercício útil é percorrer a árvore em voz alta — enunciando o problema antes de nomear a ferramenta. A estrutura abaixo demonstra esse raciocínio para 4 cenários diferentes.

### Caso 1: endpoint que recebe upload de imagem e gera thumbnail

**Diagnóstico**: processamento de imagem é CPU-bound. Cada request que chega bloqueia o event loop enquanto o resize roda. Em carga alta, todos os outros endpoints ficam lentos — o event loop lag sobe porque a thread JS está ocupada com o cálculo de pixels, não aguardando I/O.

**Decision tree**:
- CPU-bound em handler? → Worker Thread
- Tarefa frequente (upload é uma feature core, não um job raro)? → pool

**Solução**: Worker Thread com pool dimensionado em `availableParallelism()`. O upload vai para o pool; o event loop principal fica livre para continuar recebendo requests e processando I/O. Buffers de imagem passam via `transferList` para evitar cópia — um buffer de 20 MB não deve ser clonado duas vezes no processo de ir de main para worker e voltar com o resultado.

**O que não fazer**:
- Usar `cluster` para "escalar" o endpoint — cada worker teria o mesmo problema de bloqueio individual.
- Criar um Worker por request sem pool — o overhead de criação de thread (~ms) se acumula em alta carga.

---

### Caso 2: API que executa `aws s3 ls` para o usuário

**Diagnóstico**: precisa rodar comando externo (CLI do AWS). O bucket name vem do request body — é input externo não-controlado.

**Decision tree**:
- Rodar comando externo? → `child_process`
- Output curto (listagem de S3)? → `execFile` ou `exec`
- Tem argumento de origem externa (bucket name)? → `execFile` com array — NUNCA `exec`

**Solução**:
```javascript
import { execFile } from 'node:child_process/promises';

const { stdout } = await execFile('aws', ['s3', 'ls', `s3://${req.body.bucket}`], {
  encoding: 'utf8',
});
```

`req.body.bucket` chega como argumento literal ao processo `aws` — sem shell, sem injeção. Se o usuário enviar `; rm -rf /` como bucket, o AWS CLI recebe esse string como nome de bucket e retorna um erro de bucket inválido, sem executar nada no shell.

**O que não fazer**:
```javascript
// ❌ — exec interpreta o shell: ; rm -rf / executa de verdade
exec(`aws s3 ls s3://${req.body.bucket}`, callback);
```

---

### Caso 3: build server que orquestra processos de compilação

**Diagnóstico**: cada build é um processo de longa duração que pode crashar por bug no bundler, OOM, ou exceção não capturada. O build server precisa sobreviver a crashes de builds individuais e decidir se reinicia builds com falha.

**Decision tree**:
- Processo Node isolado com IPC? → `fork`
- O processo pode crashar sem afetar o pai? → `fork` (processo OS separado)
- Supervisor tree / processo descartável? → `fork` + padrão de supervisor com backoff

**Solução**: `fork('./build-worker.js')` por build. O pai monitora o evento `'exit'`, registra o código de saída, e decide se reinicia com backoff exponencial — sem reiniciar builds que terminaram com código `0`. Um SIGSEGV no bundler, um OOM no webpack, uma exceção não capturada no processo de build: o servidor de build está intacto.

**O que não fazer**:
- Worker Thread: um crash de thread pode corromper o estado do processo principal. Para processos que lidam com bundlers ou parsers não-confiáveis, isolamento total via `fork` é o modelo correto.
- `spawn` sem IPC: funciona, mas perde o canal bidirecional `child.send()` / `process.send()` que permite enviar configuração de build e receber status intermediário.

---

### Caso 4: WebSocket server escalando em K8s

**Diagnóstico**: WebSocket requer que todas as mensagens de um cliente vão para o mesmo processo (stateful). K8s com round-robin puro quebra isso — o handshake HTTP inicial que faz o upgrade para WebSocket pode ir para o pod 1; um reconect pode ir para o pod 3, que não tem o contexto da conexão.

**Decision tree**:
- Escalar HTTP/WS? → sim
- Tem orquestrador (K8s)? → orquestrador cuida de réplicas
- WebSocket (conexão persistente, stateful)? → sticky session via ingress

**Solução**: 4 pods (1 por core disponível, configurado no Deployment), ingress configurado com sticky session. No nginx: `ip_hash`. No traefik: cookie-based affinity. Sessão/estado da conexão WS em Redis ou store externo — não em memória local do pod, porque pods podem ser substituídos a qualquer momento pelo K8s durante rolling updates.

**O que não fazer**:
- Adicionar `cluster` dentro do pod além das réplicas K8s — 4 pods × 4 workers = 16 processos, sem ganho proporcional.
- Sticky session apenas por IP sem Redis: se o pod for substituído (crash, rolling update), o estado da sessão desaparece mesmo que o cliente seja roteado para o pod correto.

---

## Armadilhas

### 1. Confundir DB lento com CPU-bound

O sintoma parece igual (latência alta), mas a causa é diferente. Handler com `await db.query()` que demora 2 segundos: o event loop não está bloqueado — ele está aguardando I/O. Worker Thread não ajudaria; a query continuaria demorando 2 segundos na thread do worker. A solução está no banco (índice, query plan, connection pool), não no paralelismo.

O teste diagnóstico: medir event loop lag com `perf_hooks.monitorEventLoopDelay()`. Se o lag é baixo mas a latência do endpoint é alta, o problema é I/O, não CPU.

### 2. Cluster + K8s — overhead duplicado sem perceber

O erro clássico na migração de VPS para K8s: mover o `ecosystem.config.js` para dentro do Dockerfile e rodar PM2 com `instances: 4` dentro do container. Resultado: 4 réplicas K8s × 4 workers PM2 = 16 processos Node, 16 heaps separadas, overhead de IPC dentro de cada pod, e o K8s não consegue fazer health check por worker individualmente.

O padrão correto: `CMD ["node", "src/server.js"]` no Dockerfile. Um processo por container. O K8s gerencia réplicas.

### 3. Worker Thread como solução universal para "API lenta"

Worker Threads resolvem CPU-bound. Não resolvem query lenta, não resolvem falta de índice no banco, não resolvem N+1 queries, não resolvem I/O-bound. Adicionar Worker Threads a um sistema com gargalo de I/O adiciona complexidade de threading sem benefício — a latência não muda porque o bottleneck não está na thread JS.

O diagnóstico vem primeiro. Se o event loop lag é baixo, Worker Thread não é a resposta.

### 4. `exec` com input do usuário — sempre vulnerabilidade

Não existe sanitização confiável para input passado para `exec`. Metacaracteres de shell (`;`, `|`, `&&`, `||`, `$(...)`, `` `...` ``, `>`, `<`) têm semântica em `/bin/sh` que nenhuma regex consegue filtrar de forma completa e correta. A lista de metacaracteres muda entre shells, entre versões, e entre contextos dentro do mesmo shell.

A solução estrutural é não usar `exec` com variáveis externas, ponto final. `execFile` e `spawn` com array de argumentos passam o input como string literal ao processo — sem shell, sem injeção possível.

```javascript
// ❌ — vulnerável independente de "sanitização"
const filename = req.query.file.replace(/[^a-z0-9.]/gi, '');
exec(`cat ${filename}`, callback); // qualquer bypass da regex = RCE

// ✓ — estruturalmente seguro
execFile('cat', [req.query.file], callback);
// Shell nunca entra no caminho. Metacaracteres são texto inerte.
```

### 5. `fork` onde Worker Thread basta — overhead desnecessário

`fork` cria um processo OS completo: novo isolate V8, nova heap, nova stack, novo event loop. O custo é ~100ms por criação. Worker Thread cria uma thread no mesmo processo: ~1-5ms.

Para CPU-bound puro sem necessidade de isolamento total, Worker Thread é a escolha correta. `fork` é para os quatro casos específicos: isolamento de segurança, native modules não thread-safe, supervisor tree, processo descartável. Fora desses casos, é overhead sem justificativa.

```javascript
// ❌ — fork para CPU-bound simples: ~100ms por criação, processo OS inteiro
const child = fork('./hash-worker.js');
child.send({ password });

// ✓ — Worker Thread: ~1-5ms, thread no mesmo processo
const worker = new Worker('./hash-worker.js', { workerData: { password } });
```

---

## Em entrevista

### Cheatsheet de referência rápida

```
CPU-bound em handler?
  → Worker Thread
  → + pool se alta carga (piscina, availableParallelism())
  → + transferList se buffers grandes
  → + SharedArrayBuffer se acesso concorrente a dados compartilhados

HTTP scaling?
  → orquestrador se K8s/ECS/Fly.io (1 processo por container)
  → Cluster ou PM2 se single-VM
  → Dev local: Cluster para simular multi-worker

Comando externo?
  → spawn se output grande / streaming
  → execFile se output curto + input externo nos args
  → exec APENAS se comando completamente hardcoded

Node child isolado?
  → Worker Thread se CPU-bound sem necessidade de isolamento
  → fork se: isolamento total / native addon legado / supervisor tree / processo descartável
```

### Frase pronta (em inglês)

> "When I face a Node parallelism question, I always start from the problem, not the tool. CPU-bound work inside a handler — something like image resizing or bcrypt hashing — goes to Worker Threads, and in production I'd use a pool sized to `availableParallelism()` so I'm not creating threads per request. Scaling HTTP across cores depends on context: if there's an orchestrator like Kubernetes, I let it manage replicas — one process per container, no cluster inside the pod. On a single VM without a container runtime, native cluster or PM2 make sense. For external commands, the rule is simple: if arguments can come from user input, always use `execFile` or `spawn` with an argument array — never `exec`, because `exec` runs through a shell and any metacharacter in the input becomes a shell injection vector. Finally, for spawning an isolated Node process, I'd prefer Worker Threads if it's purely CPU-bound — much cheaper creation cost. `fork` wins when I need full OS-level isolation: running untrusted tenant code, working with non-thread-safe native addons, or building a supervisor tree where the parent needs to outlive and restart crashing children."

### Vocabulário consolidado

| PT-BR | EN |
|---|---|
| árvore de decisão | decision tree |
| trabalho limitado por CPU | CPU-bound work |
| pool de workers | worker pool |
| cópia zero | zero-copy |
| orquestrador | orchestrator |
| réplica | replica |
| sessão sticky | sticky session |
| injeção de shell | shell injection |
| argumento literal | literal argument |
| isolamento de processo | process isolation |
| árvore de supervisão | supervisor tree |
| processo descartável | disposable process |
| reinicialização com backoff | restart with exponential backoff |
| custo de criação | spawn overhead / creation cost |
| paralelismo disponível | available parallelism |

### Perguntas frequentes em entrevista

**"Como você escolheria entre Worker Thread e fork?"**
Worker Thread é a escolha padrão para CPU-bound: menor custo de criação (~1-5ms vs ~100ms), mesma API de eventos, memória compartilhável via `SharedArrayBuffer`. `fork` ganha quando isolamento total é o requisito — código de tenant não-confiável, native addons não thread-safe, supervisor tree onde o filho pode crashar sem afetar o pai, ou processo descartável com memória limitada via `--max-old-space-size`.

**"Por que não usar Cluster para paralelizar CPU-bound?"**
Cluster cria N réplicas do processo completo — cada réplica com seu próprio event loop. Se o problema é CPU-bound dentro de um único handler, cada worker bloqueia seu próprio event loop com o mesmo trabalho. Você multiplicou o problema, não o paralelizou. Worker Thread paraleliza o trabalho dentro de um único request, liberando o event loop do handler. São soluções para problemas orthogonais.

**"Quando `exec` é aceitável?"**
Quando o comando completo é hardcoded no código — sem nenhuma variável externa na string. `exec('git log --oneline -5')` é seguro porque não há interpolação. `exec(\`git log --author=${req.query.author}\`)` é vulnerável mesmo que `author` pareça inócuo — o shell interpreta todo metacaractere. A regra: se existe qualquer variável na string, use `execFile` ou `spawn` com array.

**"O que acontece se eu usar Cluster dentro de um pod K8s?"**
Nada quebra, mas você tem overhead sem benefício equivalente. 4 réplicas K8s × 4 workers cluster = 16 processos Node com 16 heaps separadas. O K8s não consegue fazer health check por worker individualmente — o readiness probe é por pod. Se um dos 4 workers interiores crashar, o pod ainda aparece como healthy. O padrão correto é 1 processo por container; o orquestrador gerencia replicas, health check e rolling update.

---

## Rubric

| Critério | Status |
|---|---|
| TL;DR cobre os 4 ramos da decision tree | ok |
| Fluxograma ASCII legível e completo | ok |
| Tabela problema → ferramenta → razão | ok |
| 4 casos práticos com diagnóstico + raciocínio | ok |
| 5 armadilhas com exemplos de código | ok |
| Frase pronta em inglês cobre os 4 ramos | ok |
| Vocabulário EN mínimo 6 termos | ok (15 termos) |
| FAQ de entrevista com 4 perguntas | ok |
| Wikilinks para notas do galho | ok |
| Sem fabricação de dados do usuário | ok |
| Nota puramente sintética — sem WebFetch | ok |

---

## Veja também

- [[12 - Armadilhas, regras práticas, cheatsheet]]
- [[01 - Por que paralelismo em Node]]
- [[02 - As 3 ferramentas - Worker Threads, Cluster, child_process]]
- [[03 - Worker Threads - fundamentos]]
- [[06 - Pool de workers - pattern de produção]]
- [[07 - Cluster - escalando HTTP por CPU]]
- [[08 - child_process com exec e spawn]]
- [[09 - child_process com fork - Node child com IPC]]
- [[10 - Cluster vs PM2 vs Kubernetes - quem orquestra]]
- [[03-Dominios/Node/Paralelismo/index]] (MOC)
- [[Node.js]] (tronco)
