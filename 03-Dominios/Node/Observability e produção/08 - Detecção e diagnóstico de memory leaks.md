---
title: "08 - Detecção e diagnóstico de memory leaks"
tags:
  - node
  - observability
  - memory
  - debugging
  - performance
type: note
status: growing
progresso: andamento
created: 2026-05-09
updated: 2026-05-09
publish: true
---

# Detecção e diagnóstico de memory leaks

> [!abstract] TL;DR
> - **Memory leak** em Node.js ocorre quando objetos continuam referenciados na heap após não serem mais necessários, impedindo o garbage collector de liberá-los — a heap cresce indefinidamente até o processo encerrar com OOM.
> - O primeiro sinal é `process.memoryUsage().heapUsed` crescendo monotonicamente ao longo do tempo, mesmo com carga estável ou em períodos ociosos; RSS também costuma subir junto.
> - A ferramenta canônica de diagnóstico é o **heap snapshot** (`v8.writeHeapSnapshot()`): capture dois snapshots — um antes e um após carga — e compare no Chrome DevTools (aba Memory > Comparison view) para identificar quais objetos estão sendo retidos.
> - **clinic heapprofiler** complementa os snapshots rastreando alocações ao longo do tempo, mostrando *onde* memória está sendo alocada (callstack), não apenas *o que* está vivo no snapshot.
> - As causas mais comuns são: listeners de `EventEmitter` não removidos, caches sem limite de tamanho ou TTL, closures capturando escopos grandes, timers não cancelados e estado global que cresce sem bound.

Memory leaks são bugs silenciosos: a aplicação funciona bem nos primeiros minutos ou horas, mas degradá gradualmente — latência sobe, GC trava a event loop com mais frequência, até que o processo crasha com `FATAL ERROR: Reached heap limit Allocation failed - JavaScript heap out of memory`. Detectar e diagnosticar esses vazamentos exige uma combinação de monitoramento contínuo, coleta de evidências (heap snapshots e allocation timelines) e análise estruturada das retainer paths. Este galho cobre o toolkit completo.

## O que é

Um **memory leak** em Node.js é qualquer situação em que objetos permanecem referenciados na heap V8 após não serem mais úteis para a aplicação, tornando-os inelegíveis para coleta pelo garbage collector. O efeito acumulativo é um crescimento contínuo da heap — mesmo sem aumento de carga — que eventualmente esgota a memória disponível e encerra o processo com um erro OOM (Out of Memory).

É importante distinguir memory leak de uso legítimo de memória. Uma aplicação que carrega um índice de busca na inicialização e mantém 500 MB em memória de forma estável não está com leak; uma aplicação que começa com 50 MB e cresce para 1 GB depois de algumas horas de tráfego normal provavelmente está.

### Fontes comuns de vazamento

- **Event listeners não removidos**: cada chamada a `emitter.on()` adiciona um listener; se o listener não for removido quando o objeto associado é descartado, ele mantém referência viva para o escopo do callback.
- **Caches sem limite**: um `Map` ou objeto usado como cache que cresce sem limite de tamanho ou TTL acumula entradas indefinidamente.
- **Closures com escopo amplo**: funções criadas dentro de callbacks que capturam variáveis grandes (como `req`, `res`, buffers) em closures de longa duração.
- **Timers não cancelados**: `setInterval` sem `clearInterval` correspondente mantém o callback — e tudo que ele captura — vivo para sempre.
- **Streams não consumidas**: streams em modo flowing que acumulam dados no buffer interno sem serem drenadas (backpressure não tratado).
- **Estado global acumulado**: arrays, maps ou sets mantidos em escopo de módulo que crescem a cada requisição sem remoção de entradas antigas.

## Como funciona

### Sinais de vazamento

O sintoma primário de um memory leak é o crescimento monotônico de `heapUsed` ao longo do tempo. Outros indicadores:

- **RSS crescendo continuamente**: o sistema operacional está alocando mais páginas de memória para o processo.
- **GC cada vez mais frequente, mas heap não reduz**: o collector está trabalhando mais sem conseguir liberar memória — sinal de que os objetos têm referências ativas.
- **Aumento de latência gradual**: GC pause time sobe porque a heap maior exige coletas mais longas.
- **Crash com OOM**: `FATAL ERROR: Reached heap limit Allocation failed - JavaScript heap out of memory`.
- **Aviso do Node.js**: `MaxListenersExceededWarning: Possible EventEmitter memory leak detected. N listeners added to [EventEmitter]` — indica acúmulo de listeners.

A forma mais simples de confirmar um leak é monitorar `process.memoryUsage()` em intervalos regulares e plotar ou logar o resultado. Se `heapUsed` sobe consistentemente ao longo de minutos ou horas sem jamais recuar para o baseline, há um leak.

```typescript
// Monitoramento básico de crescimento de heap
import { memoryUsage } from 'node:process';

let baseline: number | null = null;
const THRESHOLD_MB = 100;

const monitor = setInterval(() => {
  const { heapUsed, heapTotal, rss, external } = memoryUsage();

  if (baseline === null) {
    baseline = heapUsed;
  }

  const growthMB = (heapUsed - baseline) / 1024 / 1024;
  const heapUsedMB = heapUsed / 1024 / 1024;
  const rssMB = rss / 1024 / 1024;

  console.log(
    `[memory] heapUsed=${heapUsedMB.toFixed(1)}MB rss=${rssMB.toFixed(1)}MB growth=+${growthMB.toFixed(1)}MB`
  );

  if (growthMB > THRESHOLD_MB) {
    console.warn(
      `[memory] ALERT: heap grew ${growthMB.toFixed(1)} MB since baseline. Possible leak.`
    );
    // Aqui: disparar alerta, escrever heap snapshot, etc.
  }
}, 30_000).unref(); // .unref() evita que o timer impeça o processo de sair
```

> [!warning] Flutuação do GC
> `heapUsed` oscila naturalmente com o ciclo do GC — pode cair 20-30% depois de uma coleta. Não alerte em leituras únicas. Observe a tendência ao longo de múltiplas leituras ou use uma sliding window para calcular o crescimento médio.

### Heap snapshot

Um **heap snapshot** é uma fotografia de todos os objetos vivos na heap V8 em um dado momento, incluindo seus tamanhos e as referências entre eles. Ele é capturado em formato `.heapsnapshot` (JSON especializado) e pode ser analisado no Chrome DevTools.

#### Capturando via código

```typescript
import v8 from 'node:v8';
import path from 'node:path';
import fs from 'node:fs';

// Captura snapshot sob demanda via sinal SIGUSR2
// Uso: kill -USR2 <PID>  ou  kubectl exec ... -- kill -USR2 1
process.on('SIGUSR2', () => {
  const dir = process.env.HEAP_SNAPSHOT_DIR ?? '/tmp';

  // Garante que o diretório existe
  fs.mkdirSync(dir, { recursive: true });

  const filename = v8.writeHeapSnapshot(
    path.join(dir, `heap-${Date.now()}.heapsnapshot`)
  );

  console.log(`[heap] Snapshot written to ${filename}`);
});
```

O sinal `SIGUSR2` é conveniente porque não encerra o processo — apenas aciona o handler. Em Kubernetes, use:

```bash
# Encontre o PID do processo Node (geralmente 1 em contêineres)
kubectl exec -it <pod> -- kill -USR2 1

# Copie o snapshot para a máquina local
kubectl cp <pod>:/tmp/heap-1234567890.heapsnapshot ./heap-before.heapsnapshot
```

#### Captura automática próximo ao OOM

O flag `--heap-snapshot-near-heap-limit` instrui o V8 a escrever snapshots automaticamente quando a heap se aproxima do limite:

```bash
# Captura até 3 snapshots quando heap se aproxima do limite máximo
node --heap-snapshot-near-heap-limit=3 server.js
```

Isso é útil em produção quando o processo está prestes a crashar — os snapshots são escritos antes do OOM, permitindo análise post-mortem.

#### Workflow de análise no Chrome DevTools

1. Abra o Chrome e acesse `chrome://inspect` → "Open dedicated DevTools for Node"  
   (ou simplesmente DevTools em qualquer aba → aba **Memory**)
2. Clique em **Load** e carregue o primeiro snapshot (`heap-before.heapsnapshot`)
3. Carregue o segundo snapshot (`heap-after.heapsnapshot`)
4. Selecione o segundo snapshot e mude a view para **Comparison**
5. Ordene por **# Delta** (coluna de novas alocações) — os objetos no topo são os que mais cresceram
6. Clique em um construtor para expandir as instâncias
7. Selecione uma instância e examine o painel **Retainers** — ele mostra o caminho de referências que mantém o objeto vivo (da instância até um GC root)
8. Siga o retainer path até encontrar a referência raiz: variável global, closure, listener, etc.

### clinic heapprofiler

Enquanto heap snapshots mostram o que está vivo em um momento, `clinic heapprofiler` rastreia as **alocações ao longo do tempo** — onde no código a memória está sendo alocada, representado como um flamegraph de alocação.

```bash
# Instala clinic.js globalmente
npm install -g clinic

# Executa a aplicação com heapprofiler e autocannon para gerar carga
clinic heapprofiler -- node server.js

# Em outro terminal, aplique carga
autocannon -c 100 -d 30 http://localhost:3000/

# Ctrl+C encerra o profiling e abre o relatório HTML
```

O relatório mostra um flamegraph onde o eixo X representa bytes alocados (não tempo). Frames largos indicam funções que alocam muita memória. Ao contrário do heap snapshot, `heapprofiler` aponta para onde a alocação acontece no código — útil quando o snapshot mostra muitos objetos genéricos (strings, arrays) sem contexto claro.

> [!tip] Snapshot vs. heapprofiler
> Use heap snapshots quando você sabe que há um leak e quer encontrar *o que* está sendo retido. Use `clinic heapprofiler` quando a heap cresce mas os snapshots não apontam claramente para a causa — ele revela *onde no código* a memória está sendo alocada.

### Causas comuns

| Causa | Padrão | Detecção no snapshot |
|---|---|---|
| EventEmitter sem removeListener | Listeners acumulando por request | Array de listeners grande em um EventEmitter |
| Cache sem limite | Map/Object crescendo indefinidamente | Construtor da entidade cacheada com # Delta alto |
| Closure capturando escopo amplo | Função referenciando `req`/`res`/buffer | Closure → Object com muitos campos |
| setInterval sem clearInterval | Timer rodando para sempre | TimersList retendo callbacks |
| Stream não consumida | Buffer interno crescendo | Buffer com retained size alto |
| Estado global acumulado | Array/Map em módulo crescendo | Array/Map em escopo global |

### Estratégia de diagnóstico

O processo de diagnóstico segue uma sequência definida para evitar trabalho desnecessário:

1. **Confirme o leak com métricas**: monitore `heapUsed` por período suficiente (horas em produção, minutos com carga artificial) e verifique crescimento monotônico.
2. **Capture baseline**: com a aplicação em estado conhecido (inicializada, antes de carga), escreva o primeiro heap snapshot.
3. **Aplique carga ou aguarde**: reproduza o comportamento que causa o leak — carga de requisições, operações específicas, passagem de tempo.
4. **Force GC e capture segundo snapshot**: `global.gc()` (requer `--expose-gc`) antes do segundo snapshot garante que apenas objetos com referências reais apareçam. Depois escreva o snapshot.
5. **Compare no Chrome DevTools**: use Comparison view, ordene por # Delta.
6. **Siga o retainer path**: encontre o GC root que está segurando os objetos.
7. **Corrija no código**: remova o listener, adicione limite ao cache, limpe o timer, etc.
8. **Valide a correção**: repita o ciclo e confirme que o crescimento para.

## Na prática

### Polling de memória com alerta por tendência

Em vez de alertar em leituras únicas, mantenha uma janela deslizante e alerte quando a tendência for consistentemente crescente:

```typescript
import { memoryUsage } from 'node:process';

const WINDOW_SIZE = 5;      // número de amostras na janela
const GROWTH_THRESHOLD = 50; // MB de crescimento para disparar alerta
const readings: number[] = [];

setInterval(() => {
  const { heapUsed, rss } = memoryUsage();
  readings.push(heapUsed);

  if (readings.length > WINDOW_SIZE) {
    readings.shift();
  }

  if (readings.length === WINDOW_SIZE) {
    const oldest = readings[0];
    const newest = readings[WINDOW_SIZE - 1];
    const growthMB = (newest - oldest) / 1024 / 1024;

    if (growthMB > GROWTH_THRESHOLD) {
      console.warn(
        `[memory] Tendência de crescimento: +${growthMB.toFixed(1)} MB nas últimas ${WINDOW_SIZE} amostras`
      );
    }
  }

  console.log({
    heapUsedMB: (heapUsed / 1024 / 1024).toFixed(1),
    rssMB: (rss / 1024 / 1024).toFixed(1),
  });
}, 30_000).unref();
```

### Heap snapshot via sinal em produção

```typescript
import v8 from 'node:v8';
import path from 'node:path';
import fs from 'node:fs';

const SNAPSHOT_DIR = process.env.HEAP_SNAPSHOT_DIR ?? '/tmp/heapdumps';
let snapshotCount = 0;
const MAX_SNAPSHOTS = 5; // evitar encher o disco

process.on('SIGUSR2', () => {
  if (snapshotCount >= MAX_SNAPSHOTS) {
    console.warn('[heap] Limite de snapshots atingido, ignorando sinal');
    return;
  }

  fs.mkdirSync(SNAPSHOT_DIR, { recursive: true });

  const filename = v8.writeHeapSnapshot(
    path.join(SNAPSHOT_DIR, `heap-${process.pid}-${Date.now()}.heapsnapshot`)
  );

  snapshotCount++;
  console.log(`[heap] Snapshot #${snapshotCount} escrito em: ${filename}`);
});
```

### Padrão de vazamento: EventEmitter sem cleanup

```typescript
import { EventEmitter } from 'node:events';

const dataEmitter = new EventEmitter();

// PROBLEMA: listener adicionado a cada requisição, nunca removido.
// Após N requisições, há N listeners ativos. dataEmitter.rawListeners('data').length === N
app.get('/stream', (req, res) => {
  dataEmitter.on('data', (chunk) => {
    res.write(chunk); // mas res já pode ter sido fechado em requisições anteriores!
  });
});

// CORREÇÃO: registre o listener e remova quando a conexão fechar.
app.get('/stream', (req, res) => {
  const handler = (chunk: Buffer) => {
    if (!res.writableEnded) {
      res.write(chunk);
    }
  };

  dataEmitter.on('data', handler);

  // res.on('close') é disparado quando o cliente desconecta ou a resposta termina
  res.on('close', () => {
    dataEmitter.off('data', handler);
  });
});
```

> [!tip] emitter.once()
> Se você precisa do evento apenas uma vez, use `emitter.once()` em vez de `emitter.on()`. O listener é removido automaticamente após a primeira emissão.

### Padrão de vazamento: cache sem limite

```typescript
// PROBLEMA: cache cresce indefinidamente.
// Com 1 milhão de usuários únicos, o Map terá 1 milhão de entradas.
const userCache = new Map<string, unknown>();

async function getUser(id: string): Promise<unknown> {
  if (!userCache.has(id)) {
    userCache.set(id, await fetchUser(id));
  }
  return userCache.get(id);
}

// CORREÇÃO: use LRU cache com tamanho máximo e TTL.
import { LRUCache } from 'lru-cache';

const userCache = new LRUCache<string, unknown>({
  max: 500,                    // máximo de 500 entradas
  ttl: 1000 * 60 * 5,          // 5 minutos de TTL por entrada
  updateAgeOnGet: true,        // reinicia TTL ao acessar
});

async function getUser(id: string): Promise<unknown> {
  const cached = userCache.get(id);
  if (cached !== undefined) return cached;

  const user = await fetchUser(id);
  userCache.set(id, user);
  return user;
}
```

## Em entrevista

**What is a memory leak in Node.js and why is it dangerous?**

A memory leak in Node.js happens when objects remain referenced in the V8 heap after they are no longer needed by the application. Because the garbage collector can only free objects that have no live references, these objects accumulate over time and cause the heap to grow indefinitely. Unlike in lower-level languages, the developer does not manage memory manually — instead, the GC handles deallocation automatically. When references are inadvertently held, the GC has no way to know the objects are logically "done." The danger is twofold: first, increasing GC pause time as the heap grows (which stalls the event loop and raises latency); second, eventual process termination with an OOM error, taking down the entire service.

**How would you diagnose a memory leak in a production Node.js application?**

The first step is confirming the leak exists with metrics — specifically, observing that `process.memoryUsage().heapUsed` grows monotonically over time even during stable or low-traffic periods. Once confirmed, the diagnostic tool of choice is a heap snapshot. I would instrument the application to write a snapshot on demand via a signal handler (`process.on('SIGUSR2', () => v8.writeHeapSnapshot(...))`). I would capture a baseline snapshot under normal conditions, then apply load or wait for the leak to manifest, and capture a second snapshot. Comparing the two in Chrome DevTools (Memory tab, Comparison view, sorted by # Delta) reveals which object types accumulated. I then follow the retainer path for the worst offenders to find what root reference is keeping them alive — whether it's an event listener, a module-level cache, or a closure. For more complex cases where the snapshot doesn't point to an obvious cause, I use `clinic heapprofiler` to see an allocation timeline that shows exactly which call sites are creating the most objects.

**What are the most common causes of memory leaks in Node.js and how do you fix them?**

The most common cause is event listeners that are added but never removed. Every call to `emitter.on()` creates a new listener; if the emitter outlives the component that added the listener, those callbacks — along with everything they close over — stay in memory. The fix is always to call `emitter.off()` when the associated resource is done (e.g., in a `res.on('close')` handler or a component cleanup function). A close second is unbounded in-memory caches: using a plain `Map` or object as a cache without a size limit or TTL means it grows with every unique cache key. The fix is to use a proper LRU cache library like `lru-cache` with explicit `max` and `ttl` settings. Other common sources include closures that capture large objects (like entire `req`/`res` objects) in long-lived callbacks, `setInterval` calls without a corresponding `clearInterval`, and module-level arrays or maps that accumulate entries across requests without any eviction logic.

## Vocabulário

- **Heap snapshot**: Fotografia de todos os objetos vivos na heap V8 em um dado instante, serializada em formato `.heapsnapshot`. Usada para comparar o estado da memória entre dois momentos e identificar objetos acumulados.
- **Retainer**: Objeto (ou referência) que mantém outro objeto vivo na heap, impedindo sua coleta pelo GC. O retainer path é o caminho de referências desde o objeto vazando até um GC root.
- **GC root**: Ponto de entrada do garbage collector — referências que são sempre consideradas vivas (variáveis globais, stack frames ativos, closures de timers/listeners ativos). Qualquer objeto alcançável a partir de um GC root não pode ser coletado.
- **Retained size**: Tamanho total de memória que seria liberada se um objeto e todos os objetos que *só* ele referencia fossem removidos. É a medida mais útil para avaliar o impacto de um vazamento.
- **Shallow size**: Tamanho da memória ocupada pelo objeto em si, sem contar os objetos que ele referencia. Útil para entender a estrutura de um objeto mas não seu impacto total na heap.
- **V8 heap**: Região de memória gerenciada pelo engine V8 onde objetos JavaScript são alocados. Dividida em "young generation" (objetos recentes, coletados frequentemente) e "old generation" (objetos que sobreviveram múltiplas coletas).
- **RSS (Resident Set Size)**: Quantidade total de memória física que o processo Node.js está usando, incluindo heap V8, stack nativa, código compilado e módulos nativos. Sobe junto com a heap em leaks severos.
- **Detached object**: Objeto que foi desconectado da árvore viva da aplicação (e.g., um nó DOM removido de uma página) mas ainda é referenciado por código JavaScript — portanto não coletado. Em Node.js, aparece como "Detached" no heap snapshot.
- **Allocation timeline**: Visualização de alocações de memória ao longo do tempo, gerada por ferramentas como `clinic heapprofiler`. Mostra não apenas o que está vivo, mas onde no código as alocações ocorreram.
- **OOM (Out of Memory)**: Erro fatal gerado pelo V8 quando a heap atingiu o limite máximo (`--max-old-space-size`) e não conseguiu alocar mais memória. Encerra o processo imediatamente.

## Armadilhas

> [!warning] Um único snapshot não diagnostica leak
> Um heap snapshot capturado em um único momento mostra o estado atual da heap, mas não diz o que cresceu. Para diagnosticar um leak, você precisa **sempre comparar dois snapshots** — um baseline (antes) e um após carga ou tempo. A comparação no Chrome DevTools (Comparison view) é que revela o delta de alocações.

> [!warning] heapUsed flutua com o GC — não alerte em leituras únicas
> O GC pode reduzir `heapUsed` em 30-50% de uma leitura para outra. Sistemas de alerta baseados em leituras individuais geram falsos positivos. A abordagem correta é observar a **tendência ao longo de múltiplas leituras** — use uma sliding window, calcule a média ou observe o gráfico ao longo de horas. O sinal confiável de leak é crescimento monotônico que não recua mesmo após períodos ociosos.

> [!warning] `--max-old-space-size` esconde o sintoma, não cura o problema
> Aumentar o limite da heap com `node --max-old-space-size=4096 server.js` pode adiar o crash, mas o leak continua existindo. A aplicação simplesmente terá mais tempo antes de esgotar a memória. Use esse flag apenas como medida de emergência enquanto diagnostica e corrige a causa raiz — nunca como solução definitiva.

> [!warning] `emitter.setMaxListeners(0)` não remove o leak
> Quando o Node.js avisa `MaxListenersExceededWarning`, a reação comum é silenciar o aviso com `emitter.setMaxListeners(0)`. Isso remove o warning mas **não remove os listeners acumulados** — o leak continua. A correção real é garantir que `emitter.removeListener()` (ou `emitter.off()`) seja chamado quando o recurso associado ao listener é liberado.

> [!warning] Closures capturam mais do que parecem
> Em Node.js, closures capturam o escopo inteiro do contexto onde são criadas — não apenas as variáveis que o código explicitamente usa. Uma função anônima criada dentro de um handler de requisição pode capturar o objeto `req` inteiro (incluindo todos os headers, body parseado, etc.) mesmo que o código só use `req.user.id`. Se essa closure for armazenada em um lugar de longa duração (event listener, timer, cache), o objeto `req` completo permanece na heap. Prefira extrair apenas os dados necessários antes de criar a closure: `const userId = req.user.id; emitter.on('event', () => process(userId))`.

## Veja também

- `[[Observability e produção]]` — MOC do galho 5
- `[[05 - Node-specific metrics - event loop lag, GC, heap]]` — métricas de GC e heap em detalhe, incluindo flags de GC verbose
- `[[07 - Profiling avançado com clinic.js]]` — profiling com clinic heapprofiler e análise de alocações
- `[[Node.js]]` — tronco

## Fontes

- [Node.js Documentation — v8.writeHeapSnapshot()](https://nodejs.org/api/v8.html#v8writeheapsnapshotfilenameoptions) — API oficial para captura de heap snapshots programaticamente.
- [Node.js Documentation — process.memoryUsage()](https://nodejs.org/api/process.html#processmemoryusage) — campos disponíveis e significado de cada métrica de memória do processo.
- [clinic.js — heapprofiler](https://clinicjs.org/heap-profiler/) — documentação oficial do clinic heapprofiler, incluindo interpretação de flamegraphs de alocação.
- [Chrome DevTools — Memory panel](https://developer.chrome.com/docs/devtools/memory-problems/) — guia oficial do Google sobre análise de heap snapshots e identificação de memory leaks com DevTools.
