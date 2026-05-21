---
title: "09 - Graceful shutdown profundo"
tags:
  - node
  - observability
  - kubernetes
  - graceful-shutdown
  - production
type: note
status: growing
progresso: andamento
created: 2026-05-09
updated: 2026-05-09
publish: true
---

# Graceful shutdown profundo

> [!abstract] TL;DR
> - **Graceful shutdown** é o processo de encerrar uma aplicação de forma controlada: parar de aceitar novas conexões, aguardar as requisições em andamento terminarem, fechar recursos (banco, filas, cache) e só então sair — evitando perda de dados e erros 5xx visíveis para o cliente.
> - Em Kubernetes, o container recebe **SIGTERM** quando o pod entra no estado `Terminating`; se não encerrar dentro de `terminationGracePeriodSeconds` (padrão: 30s), o kubelet envia **SIGKILL** — que não pode ser capturado ou tratado.
> - O hook `lifecycle.preStop` com um `sleep` de ~5 segundos resolve o problema de **endpoint propagation delay**: sem ele, kube-proxy ainda roteia tráfego para o pod enquanto ele já começou a se desligar, causando 502/503.
> - `server.close()` para de aceitar novas conexões mas **não fecha conexões keep-alive existentes** — elas ficam abertas indefinidamente; use `server.closeAllConnections()` (Node 18.2+) ou implemente um timeout manual.
> - Sempre configure um **timeout de saída forçada** (`process.exit(1)` após N segundos) para evitar processos zombie no cluster — se o shutdown travar em algum recurso, o K8s SIGKILL vai chegar mesmo assim, mas o pod fica em `Terminating` consumindo slot até o timeout.

O graceful shutdown é um dos patterns mais simples de descrever e mais difíceis de implementar corretamente. A maioria dos tutoriais mostra apenas `process.on('SIGTERM', () => process.exit(0))`, que não faz nada de útil — ignora requisições em voo, não fecha conexões de banco e deixa o pool do lado do servidor com slots "zumbi". Este galho cobre a implementação completa, incluindo as armadilhas específicas de Kubernetes que causam erros de produção mesmo quando o código parece correto.

## O que é

**Graceful shutdown** (encerramento gracioso) é a técnica de terminar um processo servidor de forma controlada, garantindo que:

1. Nenhuma requisição em andamento seja abandonada no meio — o cliente não recebe um RST TCP abrupto nem um erro 502.
2. Todos os recursos externos (banco de dados, message brokers, cache distribuído) sejam fechados de forma limpa, liberando conexões e flushing de buffers pendentes.
3. Logs e métricas em memória sejam enviados antes do processo sair — sem isso, o trecho final de cada instância fica cego no observability.

O oposto é o **crash shutdown** (ou "cold shutdown"): o processo termina abruptamente, conexões TCP são resetadas sem resposta, transações de banco ficam em estado indeterminado e clientes recebem erros inesperados. Em produção, isso se traduz em picos de erro 5xx nos dashboards toda vez que um deploy acontece.

### Por que isso importa em Kubernetes

Em um ambiente Kubernetes, pods são efêmeros e reiniciados frequentemente: deploys, autoscaling, node draining, OOM killer, liveness probe failures. Sem graceful shutdown, cada reinício é uma mini-catástrofe: requisições dropadas, erros no cliente, e entradas no log de erro que dificultam distinguir bugs reais de ruído de deploy.

O Kubernetes tem mecanismos para dar tempo ao pod encerrar de forma limpa, mas o contêiner precisa cooperar ativamente. O modelo de ciclo de vida do pod define uma sequência clara de eventos entre a decisão de encerrar o pod e o processo finalmente sair.

### Ciclo de vida do pod no encerramento

Quando o Kubernetes decide encerrar um pod (seja por `kubectl delete pod`, por um deploy rolling update, ou por autoscaling down), a sequência é:

1. Pod entra no estado `Terminating` — a API server marca o pod como `deletionTimestamp` definido.
2. O **preStop hook** é executado (se configurado) — o kubelet executa o hook antes de enviar qualquer sinal ao container.
3. **SIGTERM** é enviado ao processo principal do container (PID 1).
4. O kubelet aguarda até `terminationGracePeriodSeconds` (padrão: 30s) pelo encerramento do processo.
5. Se o processo ainda estiver rodando após o grace period, o kubelet envia **SIGKILL** — que não pode ser capturado nem tratado; o processo é terminado imediatamente pelo kernel.

> [!warning] preStop e SIGTERM em versões recentes do K8s
> Em versões do Kubernetes ≥ 1.23, o preStop hook e o SIGTERM são enviados de forma **concorrente** (não sequencial como documentado originalmente). Na prática, o `sleep 5` no preStop ainda funciona como buffer para propagação de endpoints, mas o SIGTERM já foi enviado quando o sleep começa. Isso significa que o handler de SIGTERM precisa considerar que o preStop ainda pode estar rodando quando ele é invocado.

## Como funciona

### Sinais do sistema

O Unix define uma série de sinais que o kernel pode enviar a um processo. Os relevantes para shutdown são:

**SIGTERM** (sinal 15) — o sinal "por favor, encerre de forma limpa". É o padrão enviado pelo `kill PID`, pelo `kubectl delete pod` e pela maioria dos orquestradores. O processo **pode capturar** este sinal, executar limpeza e sair voluntariamente. É o sinal correto para graceful shutdown.

**SIGKILL** (sinal 9) — o sinal "morra agora, sem exceção". É enviado pelo kernel diretamente, **não pode ser capturado**, bloqueado ou ignorado por nenhum processo. Quando o Kubernetes esgota o `terminationGracePeriodSeconds`, é o SIGKILL que termina o processo à força. Não há cleanup possível após receber SIGKILL — o processo simplesmente some.

**SIGINT** (sinal 2) — enviado quando o usuário pressiona `Ctrl+C` no terminal. Em desenvolvimento, é o equivalente interativo do SIGTERM. É capturável e deve ser tratado com o mesmo handler de graceful shutdown.

```typescript
// Registrar handlers para os dois sinais capturáveis relevantes
process.on('SIGTERM', () => gracefulShutdown('SIGTERM'));
process.on('SIGINT',  () => gracefulShutdown('SIGINT'));

// SIGKILL não pode ser capturado — não existe process.on('SIGKILL')
```

Em Kubernetes especificamente, a sequência de sinais é:
- **t=0**: Pod entra em `Terminating`, preStop hook executa (se definido)
- **t=0** (ou após preStop em K8s antigo): SIGTERM enviado ao PID 1
- **t=terminationGracePeriodSeconds** (padrão 30s): SIGKILL enviado se o processo ainda existir

O valor padrão de `terminationGracePeriodSeconds` é 30 segundos, mas pode ser configurado por Deployment. O timeout do seu graceful shutdown **deve ser menor** que `terminationGracePeriodSeconds` para ter tempo de sair de forma limpa antes do SIGKILL.

### Sequência de shutdown

A ordem em que os recursos são fechados durante o shutdown importa tanto quanto o próprio ato de fechar. A sequência incorreta pode causar erros mesmo quando todos os recursos são fechados.

**Sequência correta (do externo para o interno):**

1. **Parar de aceitar novas conexões** — `server.close()`. O servidor para de fazer `accept()` em novas conexões TCP, mas conexões existentes continuam sendo servidas. Novos clientes recebem `ECONNREFUSED` (ou o load balancer redireciona para outra instância).

2. **Fechar conexões keep-alive ociosas** — `server.closeIdleConnections()` (Node 18.2+). Conexões keep-alive sem requisição ativa são fechadas imediatamente, acelerando o shutdown. Conexões com requisição em andamento continuam até a resposta ser enviada.

3. **Aguardar requisições em voo terminarem** — esperar o contador de in-flight requests chegar a zero. Com um timeout: se demorar mais que N segundos, avançar mesmo assim (clientes pendentes receberão um erro, mas isso é preferível a um pod que não encerra).

4. **Fechar consumers de message queue** — parar de consumir novas mensagens do Kafka/RabbitMQ/SQS. Mensagens em processamento devem ser concluídas ou rejeitadas (NACK) antes de fechar o consumer.

5. **Fechar conexões de banco de dados** — `db.end()` ou `pool.end()`. Fechar antes das requisições HTTP terminarem causaria erros nas queries ainda em andamento.

6. **Fechar conexões de cache/outros clientes** — Redis, Elasticsearch, etc.

7. **Flush de logs e métricas** — garantir que todos os logs buffered e métricas pendentes sejam enviados. Pino com transport async, por exemplo, pode ter um buffer não flushed no momento do shutdown.

8. **`process.exit(0)`** — sair limpo. O código 0 indica sucesso; o orquestrador não vai reiniciar o pod automaticamente.

**Por que esta ordem previne erros:**

Se você fechar o banco antes das requisições HTTP terminarem (invertendo os passos 3 e 5), as queries ainda em andamento falharão com `Cannot use a pool after calling end on the pool`. Se você parar de aceitar novas conexões antes de sinalizar ao load balancer (preStop), novas requisições serão roteadas para um pod que já rejeita conexões — o cliente vê `502 Bad Gateway`.

```
Nova conexão → REJEITAR (server.close) ──────────────────────────────────┐
Conexão existente → SERVIR até finalizar ────────────────────────────────┤
In-flight requests → AGUARDAR (contador) ────────────────────────────────┤
Message queue consumer → PARAR ─────────────────────────────────────────┤
DB connections → FECHAR (db.end) ────────────────────────────────────────┤
Cache connections → FECHAR ──────────────────────────────────────────────┤
Logs/metrics → FLUSH ───────────────────────────────────────────────────┤
process.exit(0) ◄───────────────────────────────────────────────────────┘
```

### server.close() vs server.closeAllConnections()

Este é um dos pontos mais frequentemente mal compreendidos do graceful shutdown em Node.js. O comportamento de `server.close()` não é o que a maioria dos devs espera.

**`server.close(callback?)`**

Para de chamar `accept()` em novas conexões TCP. O servidor não vai mais aceitar novas conexões. O callback é chamado quando **a última conexão existente for fechada**.

O problema: **conexões keep-alive não são fechadas automaticamente**. Uma conexão HTTP/1.1 com keep-alive fica aberta indefinidamente aguardando a próxima requisição — e `server.close()` espera todas as conexões fecharem antes de chamar o callback. Se um cliente mantém uma conexão keep-alive aberta, o processo **nunca vai encerrar** (até o SIGKILL do K8s).

```typescript
// PROBLEMA: server nunca chama o callback se houver keep-alive connections
server.close(() => {
  console.log('server fechado'); // pode nunca ser chamado
});
```

**`server.closeAllConnections()`** (Node 18.2+)

Fecha imediatamente **todas** as conexões abertas — incluindo keep-alive e conexões com requisição em andamento. O callback de `server.close()` será chamado em seguida.

Usar `closeAllConnections()` sozinho é muito agressivo: mata requisições em andamento. A estratégia correta é combinar os dois:

```typescript
// CORRETO: fecha novas, aguarda in-flight, força keep-alive após timeout
server.close(); // para novas conexões

// Após aguardar requisições in-flight, forçar fechamento das keep-alive restantes
server.closeAllConnections(); // fecha todas as restantes (Node 18.2+)
```

**`server.closeIdleConnections()`** (Node 18.2+)

Fecha apenas conexões **sem requisição ativa** no momento. É mais seguro que `closeAllConnections()` para uso imediato, pois não interrompe requisições em andamento. Porém, ainda pode deixar conexões keep-alive ativas se o cliente enviou uma nova requisição entre o `server.close()` e o `closeIdleConnections()`.

| Método                      | Versão  | Comportamento                                                    |
|-----------------------------|---------|------------------------------------------------------------------|
| `server.close(cb)`          | todas   | Para de aceitar novas conexões; chama cb quando último fecha     |
| `server.closeIdleConnections()` | 18.2+ | Fecha conexões sem requisição ativa                          |
| `server.closeAllConnections()` | 18.2+ | Fecha todas as conexões imediatamente                          |

### Kubernetes preStop hook

O **endpoint propagation delay** é a armadilha mais sutil do graceful shutdown em K8s e causa 502/503 em deploys mesmo quando o código de shutdown está correto.

**O problema:**

Quando um pod entra em `Terminating`, o Kubernetes precisa remover o pod dos `Endpoints` do Service para que o kube-proxy pare de rotear tráfego para ele. Mas essa atualização de endpoints é **assíncrona**: o API server atualiza o objeto `Endpoints`, o controller manager propaga para os nós, e cada kube-proxy nos nós atualiza suas regras de iptables/ipvs. Esse processo leva entre 1 e 10 segundos dependendo do tamanho do cluster.

Durante esse intervalo, o pod está:
- Recebendo SIGTERM (ou já começou o shutdown)
- Ainda sendo listado nos endpoints pelos kube-proxy dos nós
- Recebendo novas requisições do load balancer

Se o servidor já fechou (`server.close()`), as novas conexões recebem `ECONNREFUSED`, que o kube-proxy repassa como `502 Bad Gateway` para o cliente.

**A solução: preStop hook com sleep**

```yaml
lifecycle:
  preStop:
    exec:
      command: ["sleep", "5"]  # aguarda propagação de endpoints
```

O `sleep 5` atrasa o início do shutdown, dando tempo para que todos os kube-proxy removam o pod dos endpoints antes de começar a rejeitar conexões. O valor de 5 segundos é uma heurística amplamente adotada; em clusters grandes ou com latência de API server alta, pode ser necessário aumentar para 10-15s.

**Ajuste correspondente no terminationGracePeriodSeconds:**

Se o preStop dura 5s e o shutdown leva até 25s, o `terminationGracePeriodSeconds` precisa ser pelo menos 30s (5 + 25). O tempo total é: `preStop duration + shutdown duration < terminationGracePeriodSeconds`.

### Timeouts

Todo código de shutdown precisa de um **timeout de saída forçada**. Sem ele, um bug no código de shutdown (deadlock, promise que nunca resolve, DB que não responde) pode fazer o pod ficar em `Terminating` para sempre — consumindo um slot no nó, impedindo novos pods de escalar, e geralmente causando confusão operacional.

O timeout de saída forçada deve ser configurado **antes** do handler de SIGTERM, usando `setTimeout().unref()` para não impedir o processo de sair normalmente quando o shutdown completa antes do timeout:

```typescript
// Safety net: force exit 1s antes do SIGKILL do K8s (terminationGracePeriodSeconds = 30)
const FORCE_EXIT_TIMEOUT_MS = 29_000;

const forceExitTimer = setTimeout(() => {
  console.error('Forced exit: graceful shutdown exceeded timeout, forcing process.exit(1)');
  process.exit(1); // código 1 para indicar shutdown não-gracioso
}, FORCE_EXIT_TIMEOUT_MS).unref(); // .unref() permite que o processo saia normalmente antes do timeout

// Em condições normais, o shutdown completa e process.exit(0) cancela o timer implicitamente
```

O `.unref()` é crítico: sem ele, o `setTimeout` mantém o event loop ativo mesmo após o processo ter concluído tudo e chamado `process.exit()`. Com `.unref()`, se o processo sai normalmente (via `process.exit(0)`), o timer é descartado sem disparar.

## Na prática

### Handler completo de graceful shutdown

O exemplo a seguir implementa um handler de graceful shutdown completo para uma aplicação Node.js com HTTP server (Express/Fastify/http nativo), PostgreSQL e Redis.

```typescript
import http from 'node:http';
import { Pool } from 'pg';
import { createClient } from 'redis';

const db = new Pool({ connectionString: process.env.DATABASE_URL });
const redis = createClient({ url: process.env.REDIS_URL });

const server = http.createServer(app);

// ── Rastreamento de requisições in-flight ──────────────────────────────────────
let inflightRequests = 0;
let isShuttingDown = false;

server.on('request', (req, res) => {
  inflightRequests++;

  // Quando o servidor está encerrando, sinalizar ao cliente para fechar a conexão
  if (isShuttingDown) {
    res.setHeader('Connection', 'close');
  }

  res.on('finish', () => {
    inflightRequests--;
  });
});

function waitForInflightRequests(timeoutMs = 20_000): Promise<void> {
  return new Promise((resolve) => {
    // Se já está zerado, resolve imediatamente
    if (inflightRequests === 0) {
      resolve();
      return;
    }

    const deadline = Date.now() + timeoutMs;

    const check = () => {
      if (inflightRequests === 0) {
        resolve();
      } else if (Date.now() >= deadline) {
        console.warn(`Shutdown: ${inflightRequests} in-flight requests abandoned after timeout`);
        resolve(); // avança mesmo com requisições pendentes após timeout
      } else {
        setTimeout(check, 100);
      }
    };

    check();
  });
}

// ── Safety net: força saída antes do SIGKILL do K8s ───────────────────────────
// terminationGracePeriodSeconds = 30; preStop = 5; restam ~25s para shutdown
// Saímos forçado em 29s para dar margem de 1s antes do SIGKILL
setTimeout(() => {
  console.error('Forced exit: shutdown timeout exceeded (29s), calling process.exit(1)');
  process.exit(1);
}, 29_000).unref();

// ── Handler principal de graceful shutdown ─────────────────────────────────────
async function gracefulShutdown(signal: string): Promise<void> {
  console.log(`[shutdown] Received ${signal} — starting graceful shutdown`);
  isShuttingDown = true;

  // 1. Parar de aceitar novas conexões
  server.close();
  console.log('[shutdown] 1/6 — server.close() called, no new connections accepted');

  // 2. Fechar conexões keep-alive ociosas (Node 18.2+)
  if (typeof server.closeIdleConnections === 'function') {
    server.closeIdleConnections();
    console.log('[shutdown] 2/6 — idle connections closed');
  }

  // 3. Aguardar requisições in-flight terminarem (máx. 20s)
  await waitForInflightRequests(20_000);
  console.log('[shutdown] 3/6 — in-flight requests drained');

  // 4. Fechar conexões restantes (keep-alive com cliente inativo)
  if (typeof server.closeAllConnections === 'function') {
    server.closeAllConnections();
    console.log('[shutdown] 4/6 — all remaining connections closed');
  }

  // 5. Fechar recursos externos
  try {
    await db.end();
    console.log('[shutdown] 5a/6 — PostgreSQL pool closed');
  } catch (err) {
    console.error('[shutdown] PostgreSQL close error:', err);
  }

  try {
    await redis.quit();
    console.log('[shutdown] 5b/6 — Redis client closed');
  } catch (err) {
    console.error('[shutdown] Redis close error:', err);
  }

  // 6. Sair limpo
  console.log('[shutdown] 6/6 — graceful shutdown complete');
  process.exit(0);
}

// Registrar handlers
process.on('SIGTERM', () => gracefulShutdown('SIGTERM'));
process.on('SIGINT',  () => gracefulShutdown('SIGINT'));

// Iniciar servidor
await redis.connect();
server.listen(3000, () => {
  console.log('Server listening on :3000');
});
```

### Kubernetes Deployment com preStop e terminationGracePeriodSeconds

O YAML abaixo configura corretamente o ciclo de vida do pod para trabalhar em conjunto com o código de shutdown acima. O `preStop` de 5 segundos dá tempo para a propagação de endpoints, e o `terminationGracePeriodSeconds: 35` acomoda os 5s do preStop + até 29s do shutdown + 1s de margem.

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: my-service
spec:
  replicas: 3
  strategy:
    type: RollingUpdate
    rollingUpdate:
      maxUnavailable: 0        # nunca reduz capacidade durante deploy
      maxSurge: 1              # sobe 1 pod novo antes de matar 1 velho
  template:
    spec:
      # Deve ser maior que preStop + shutdown timeout do código
      terminationGracePeriodSeconds: 35  # 5s preStop + 29s shutdown + 1s margem

      containers:
        - name: my-service
          image: my-service:latest
          ports:
            - containerPort: 3000
          env:
            - name: DATABASE_URL
              valueFrom:
                secretKeyRef:
                  name: db-secret
                  key: url

          # Configuração de lifecycle
          lifecycle:
            preStop:
              exec:
                # Aguarda propagação de endpoints antes de iniciar shutdown
                # Sem isso: kube-proxy ainda roteia tráfego para o pod
                # enquanto ele já recusou novas conexões → 502/503
                command: ["sleep", "5"]

          # Readiness probe: K8s para de rotear tráfego se falhar
          readinessProbe:
            httpGet:
              path: /health/ready
              port: 3000
            initialDelaySeconds: 5
            periodSeconds: 10
            failureThreshold: 3

          # Liveness probe: K8s reinicia o pod se falhar
          livenessProbe:
            httpGet:
              path: /health/live
              port: 3000
            initialDelaySeconds: 15
            periodSeconds: 20
            failureThreshold: 3

          resources:
            requests:
              memory: "128Mi"
              cpu: "100m"
            limits:
              memory: "256Mi"
              cpu: "500m"
```

### Rastreamento de in-flight requests com middleware

Em frameworks como Express ou Fastify, o rastreamento pode ser feito via middleware/hook, mantendo o código de aplicação limpo e separado da lógica de shutdown.

```typescript
// middleware/inflight-tracker.ts
// Express
import { Request, Response, NextFunction } from 'express';

let _inflightCount = 0;

export function inflightTrackerMiddleware(req: Request, res: Response, next: NextFunction) {
  _inflightCount++;
  res.on('finish', () => _inflightCount--);
  res.on('close', () => {
    // 'close' dispara se a conexão foi abortada antes de 'finish'
    // evitar double-decrement: 'close' dispara APÓS 'finish' em conexões normais
  });
  next();
}

export function getInflightCount(): number {
  return _inflightCount;
}

export function waitForInflight(timeoutMs = 20_000): Promise<void> {
  return new Promise((resolve) => {
    const deadline = Date.now() + timeoutMs;
    const poll = () => {
      if (_inflightCount === 0 || Date.now() >= deadline) resolve();
      else setTimeout(poll, 100);
    };
    poll();
  });
}
```

```typescript
// Para Fastify: usar addHook em vez de middleware Express
fastify.addHook('onRequest', async (request, reply) => {
  inflightRequests++;
});

fastify.addHook('onResponse', async (request, reply) => {
  inflightRequests--;
});

fastify.addHook('onError', async (request, reply, error) => {
  // onError dispara antes de onResponse quando há erro
  // onResponse ainda será chamado após onError, então não decrementar aqui
});
```

## Em entrevista

**What is graceful shutdown and why does it matter?**

Graceful shutdown is the practice of terminating a server process in a controlled way: first stop accepting new connections, then wait for all in-flight requests to complete, then close external resources like database connections and message queue consumers, and finally exit. Without it, every deployment causes a burst of 5xx errors because active requests are abruptly cut off mid-flight — the client receives a TCP reset instead of a proper HTTP response. In high-traffic services, even a rolling deploy with three replicas can cause hundreds of dropped requests if each pod doesn't shut down gracefully.

**How does Kubernetes handle pod termination and what is terminationGracePeriodSeconds?**

When Kubernetes decides to terminate a pod — due to a rolling deploy, autoscaling, or node drain — the kubelet sends SIGTERM to the container's main process and starts a countdown timer defined by `terminationGracePeriodSeconds`, which defaults to 30 seconds. If the process hasn't exited by the time the timer expires, the kubelet sends SIGKILL, which cannot be caught or handled by the application — the process is killed immediately by the kernel. This means your graceful shutdown logic must complete within that window. A common pattern is to set a hard timeout in code at 29 seconds (1 second before the K8s SIGKILL), so you have a controlled exit path even if something in the shutdown sequence gets stuck.

**What is the preStop hook and why is it necessary even when the code handles SIGTERM correctly?**

The preStop hook solves a subtle race condition called endpoint propagation delay. When a pod enters the Terminating state, Kubernetes needs to remove it from the Service's Endpoints so that kube-proxy stops routing traffic to it. However, this propagation is asynchronous: the API server updates the Endpoints object, the update propagates to each node's kube-proxy, and each kube-proxy updates its iptables or ipvs rules. This process can take between 1 and 10 seconds. During that window, the pod is already receiving SIGTERM and starting to shut down — potentially calling `server.close()` — while kube-proxy is still sending new connections to it. The new connections hit a server that's no longer accepting connections and get a `ECONNREFUSED`, which kube-proxy surfaces as a 502 Bad Gateway. Adding `lifecycle.preStop.exec.command: ["sleep", "5"]` introduces a deliberate delay before shutdown begins, giving kube-proxy time to finish propagating the endpoint removal before the server stops accepting connections.

## Vocabulário

| Termo | Definição |
|---|---|
| **SIGTERM** | Sinal Unix 15; solicita encerramento gracioso ao processo; pode ser capturado e tratado com `process.on('SIGTERM', handler)`. |
| **SIGKILL** | Sinal Unix 9; termina o processo imediatamente via kernel; não pode ser capturado, bloqueado ou ignorado por nenhum processo. |
| **terminationGracePeriodSeconds** | Campo do Pod spec no Kubernetes que define quantos segundos o kubelet aguarda entre o SIGTERM e o SIGKILL; padrão: 30s. |
| **preStop hook** | Hook de ciclo de vida do Kubernetes executado antes do SIGTERM; usado com `sleep` para aguardar propagação de endpoints e evitar 502/503 durante deploys. |
| **keep-alive connection** | Conexão HTTP/1.1 persistente que reutiliza o mesmo socket TCP para múltiplas requisições; `server.close()` não as fecha automaticamente, exigindo `server.closeAllConnections()` ou timeout manual. |
| **in-flight request** | Requisição HTTP que foi recebida pelo servidor e está sendo processada mas ainda não recebeu resposta completa; o shutdown deve aguardar essas requisições terminarem. |
| **endpoint propagation delay** | Latência entre o pod entrar em `Terminating` e todos os kube-proxy pararem de rotear tráfego para ele; tipicamente 1-10s; resolvida com o preStop sleep. |
| **server.closeAllConnections()** | Método do `http.Server` (Node 18.2+) que fecha imediatamente todas as conexões abertas, incluindo keep-alive; complementa `server.close()` para garantir encerramento rápido. |
| **server.closeIdleConnections()** | Método do `http.Server` (Node 18.2+) que fecha apenas conexões sem requisição ativa; mais seguro que `closeAllConnections()` para uso imediato após `server.close()`. |

## Armadilhas

> [!warning] `server.close()` não fecha conexões keep-alive
> `server.close()` para de chamar `accept()` em novas conexões TCP, mas conexões keep-alive existentes ficam abertas indefinidamente aguardando a próxima requisição. O callback passado para `server.close(cb)` só é chamado quando **todas** as conexões fecham — o que pode nunca acontecer com clientes que mantêm keep-alive. Use `server.closeIdleConnections()` logo após `server.close()` e `server.closeAllConnections()` após drenar as requisições in-flight. Em Node < 18.2, a alternativa é rastrear todas as conexões manualmente via `server.on('connection', ...)` e fechá-las no shutdown.

> [!warning] Sem preStop sleep, K8s roteia tráfego para pod em shutdown
> Quando o pod entra em `Terminating`, o kube-proxy leva de 1 a 10 segundos para propagar a remoção do pod dos endpoints. Durante esse tempo, novas requisições continuam sendo roteadas para o pod. Se o servidor já chamou `server.close()`, essas requisições recebem `ECONNREFUSED`, que o cliente vê como `502 Bad Gateway`. O preStop `sleep 5` resolve isso adicionando um buffer antes do início do shutdown — sem modificar nenhuma linha do código da aplicação.

> [!warning] SIGKILL não pode ser capturado — monitore seu tempo de shutdown
> Muitos devs implementam graceful shutdown, testam localmente com `Ctrl+C`, e consideram pronto. Mas `Ctrl+C` envia SIGINT — que pode ser tratado. SIGKILL é diferente: o kernel termina o processo sem dar chance de cleanup. Se o seu shutdown toma mais de `terminationGracePeriodSeconds`, o K8s enviará SIGKILL e tudo que estava em andamento (queries, publicações em fila, flush de logs) será abortado. Monitore o tempo médio de shutdown nos logs e garanta que `terminationGracePeriodSeconds` seja generoso o suficiente. Como regra: `terminationGracePeriodSeconds ≥ preStop + shutdown_timeout + 5s de margem`.

> [!warning] Não fechar conexões de banco vaza slots do connection pool
> Se o processo termina sem chamar `db.end()` (ou `pool.end()`), as conexões no lado do servidor de banco ficam abertas por um tempo determinado pelo `tcp_keepalive` do SO ou pelo timeout do banco (PostgreSQL default: nunca expira sem configuração). Num ambiente de alta rotatividade de pods (autoscaling agressivo), isso pode exaurir o `max_connections` do banco — todas as conexões estão "em uso" por pods já mortos. Sempre feche o pool explicitamente e registre o evento: `console.log('db pool closed')` no shutdown ajuda a debugar se o shutdown completou todas as etapas.

> [!warning] `process.exit()` no meio de operações async pula callbacks pendentes
> Chamar `process.exit(0)` enquanto há Promises pendentes (awaits em andamento, microtasks na fila) descarta tudo silenciosamente — sem erro, sem warning. Um padrão comum problemático é fazer `process.on('SIGTERM', () => { cleanup(); process.exit(0); })` onde `cleanup()` é async mas não está sendo awaited. Use sempre `async function gracefulShutdown()` com `await` em cada etapa, e só chame `process.exit(0)` após todos os awaits completarem. O timeout forçado garante que o processo sai mesmo se algum await travar.

> [!warning] Dois handlers de SIGTERM causam double-shutdown
> Em aplicações com frameworks que também registram handlers de SIGTERM (PM2, alguns frameworks de teste, signal-exit), pode haver conflito. Verifique se o framework já registra um handler antes de adicionar o seu. Em frameworks como Fastify, use os hooks nativos (`fastify.addHook('onClose', ...)`) em vez de `process.on('SIGTERM')` — o Fastify já trata o sinal corretamente se iniciado com as opções adequadas.

## Veja também

- [[03-Dominios/Node/Observability e produção/index]] — MOC do galho 5
- [[11 - Connection pool tuning]] — impacto do pool no shutdown e como dimensionar conexões para suportar rotatividade de pods
- [[Node.js]] — tronco

## Fontes

- [Node.js Docs — `server.close()`](https://nodejs.org/api/net.html#serverclosecallback) — documentação oficial do método `close()` em `net.Server` (superclasse de `http.Server`), incluindo comportamento com keep-alive connections.
- [Node.js Docs — `server.closeAllConnections()` e `server.closeIdleConnections()`](https://nodejs.org/api/http.html#servercloseallconnections) — adicionados em Node 18.2.0; documenta o comportamento exato de cada método.
- [Kubernetes Docs — Pod Lifecycle: Termination](https://kubernetes.io/docs/concepts/workloads/pods/pod-lifecycle/#pod-termination) — sequência oficial de terminação de pods, incluindo preStop hooks, SIGTERM, e terminationGracePeriodSeconds.
- [Kubernetes Docs — Container Lifecycle Hooks](https://kubernetes.io/docs/concepts/containers/container-lifecycle-hooks/) — documentação do preStop hook, incluindo a nota sobre execução concorrente com SIGTERM em versões recentes.
- [Learnk8s — Graceful shutdown and zero downtime deployments in Kubernetes](https://learnk8s.io/graceful-shutdown) — artigo técnico detalhado sobre endpoint propagation delay e o papel do preStop sleep; inclui diagramas da sequência de eventos.
