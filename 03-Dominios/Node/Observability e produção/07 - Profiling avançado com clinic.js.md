---
title: "07 - Profiling avançado com clinic.js"
tags:
  - node
  - observability
  - profiling
  - performance
  - clinic-js
type: note
status: growing
progresso: andamento
created: 2026-05-09
updated: 2026-05-09
publish: true
---

# Profiling avançado com clinic.js

> [!abstract] TL;DR
> - **clinic.js** é uma suite open-source da NearForm com quatro ferramentas especializadas — `doctor`, `flame`, `bubbleprof` e `heapprofiler` — cada uma projetada para um tipo diferente de problema de performance em Node.js.
> - **clinic doctor** é sempre o primeiro passo: ele roda sua aplicação, injeta carga e gera um relatório HTML que identifica automaticamente event loop delay, problemas de I/O e crescimento de heap.
> - **clinic flame** produz um flamegraph de CPU mostrando quais funções consomem mais tempo; **clinic bubbleprof** visualiza operações assíncronas e onde o tempo é perdido esperando I/O.
> - **clinic heapprofiler** rastreia alocações de heap ao longo do tempo — diferente de um heap snapshot, ele mostra *onde* memória está sendo alocada, não apenas *o que* está vivo no momento.
> - A estratégia correta é: `doctor` para diagnóstico geral → `flame` se o problema for CPU → `bubbleprof` se for I/O/async → `heapprofiler` se for memória.

Toda aplicação Node.js em produção eventualmente enfrenta o mesmo conjunto de perguntas: por que o event loop está atrasando? qual função está consumindo CPU demais? por que a memória cresce sem parar? Responder a essas perguntas com `console.log` e intuição é ineficiente; profiling é a abordagem sistemática. clinic.js oferece uma suite de ferramentas que tornam esse processo acessível, gerando relatórios visuais ricos a partir de simples comandos CLI — sem exigir modificações no código da aplicação.

## O que é

**clinic.js** é uma coleção de ferramentas de diagnóstico de performance para Node.js, desenvolvida e mantida pela [NearForm](https://www.nearform.com/) e publicada como open-source. A suite agrupa quatro ferramentas com propósitos distintos sob um mesmo executor CLI:

| Ferramenta | Foco | Quando usar |
|---|---|---|
| `clinic doctor` | Diagnóstico geral | Primeiro passo sempre; identifica a categoria do problema |
| `clinic flame` | CPU profiling | Quando a CPU está alta ou response time é elevado sem I/O |
| `clinic bubbleprof` | Async profiling | Quando I/O ou operações assíncronas causam latência |
| `clinic heapprofiler` | Heap allocation | Quando a memória cresce e você precisa saber *onde* ela é alocada |

A filosofia do clinic.js é **não invasiva por padrão**: você passa seu comando de inicialização e a ferramenta injeta instrumentação transparentemente, sem alterar seu código-fonte. Os resultados são salvos em diretórios locais e abertos no browser como relatórios HTML interativos.

### Instalação

```bash
# Uso via npx (sem instalação global):
npx clinic doctor -- node server.js

# Ou instalar globalmente:
npm install -g clinic
clinic doctor -- node server.js
```

O padrão `--` separa os argumentos do clinic dos argumentos do Node.js. Tudo após `--` é o comando que será executado e monitorado.

## Como funciona

### Clinic Doctor

`clinic doctor` é a porta de entrada do diagnóstico. Ele instrumenta sua aplicação com coleta de métricas do runtime Node.js — event loop lag, uso de CPU, uso de memória e I/O — e gera um relatório HTML com análise automática dos padrões detectados.

**O que ele detecta:**

- **Event loop delay**: spikes ou aumento sustentado na latência do loop — indica código síncrono bloqueante ou microtask flooding
- **I/O issues**: correlação entre I/O wait e event loop delay — sugere gargalo em operações de disco ou rede
- **Memory leaks**: heap crescendo de forma contínua e não sendo liberado pelo GC
- **CPU hotspots**: CPU consistentemente alta sem I/O correspondente — indica trabalho computacional excessivo

**Uso básico:**

```bash
# Rodar a aplicação e coletar métricas:
npx clinic doctor -- node server.js

# O clinic abre automaticamente um relatório HTML
# Arquivo gerado em: ./<pid>.clinic-doctor-flamegraph/
```

O relatório mostra quatro séries temporais alinhadas: CPU, memory, event loop delay e handles ativos. O doctor analisa padrões entre essas séries e emite um diagnóstico textual — por exemplo, "potential event loop issue" — com sugestões de próximos passos.

**Recomendação de workflow:**

Sempre rode o doctor com carga real ou simulada. Sem carga, as métricas são quase planas e o diagnóstico é inútil. Use `autocannon` ou uma ferramenta similar para simular requisições enquanto o doctor coleta.

### Clinic Flame

`clinic flame` gera um **flamegraph de CPU** — uma visualização hierárquica de onde o tempo de CPU é gasto. Internamente, ele usa [`0x`](https://github.com/davidmarkclements/0x), um profiler de sampling de alta qualidade para V8.

**Como funciona o sampling:** O V8 interrompe a execução periodicamente (normalmente a cada 1ms) e registra o call stack atual. Depois de milhares de amostras, cada função aparece no flamegraph proporcionalmente ao tempo em que esteve presente nas amostras — isso é chamado de **wall time sampling**.

**Uso básico:**

```bash
npx clinic flame -- node server.js
```

**Lendo o flamegraph:**

- **Eixo horizontal**: proporção do tempo total de CPU gasto na função (largura = tempo)
- **Eixo vertical**: profundidade do call stack (callee acima, caller abaixo)
- **Barras largas**: funções que consomem muito tempo — são os hot paths
- **Pilhas altas e estreitas**: call stacks profundos com pouco tempo em cada nível — indica muita indireção
- **Cores**: no clinic flame, azul/verde = código otimizado pelo JIT; vermelho/laranja = código deotimizado pelo V8 (merece atenção especial)

> [!tip] Foco no topo das barras largas
> Olhe as barras largas no topo da pilha — são as funções folha que efetivamente consomem CPU, não apenas chamam outras funções. Uma função larga no meio da pilha pode ser só um intermediário que delega para filhos.

Se o clinic flame tiver problemas (por exemplo, em ambientes containerizados sem suporte a `perf`), você pode usar o `0x` diretamente:

```bash
npx 0x server.js
```

### Clinic Bubbleprof

`clinic bubbleprof` é o **profiler de operações assíncronas**. Ao contrário do flame (que foca em CPU), o bubbleprof visualiza *quanto tempo a aplicação passa esperando* — em callbacks, Promises, operações de I/O. Ele usa a API `async_hooks` do Node.js para rastrear cada operação assíncrona do início ao fim.

**O que ele responde:**

- Onde está o tempo de espera? (I/O de rede, disco, DNS, banco de dados)
- Quais operações assíncronas são mais lentas?
- Existe encadeamento desnecessário de Promises que adiciona latência?

**Uso básico:**

```bash
npx clinic bubbleprof -- node server.js
```

O relatório mostra "bolhas" (bubbles) que representam grupos de operações assíncronas. O tamanho da bolha representa o tempo de espera; a cor indica o tipo de operação. Linhas conectando bolhas mostram a cadeia de dependências assíncronas.

**Quando usar em vez do flame:**

Se o flamegraph de CPU mostra que a CPU está ociosa a maior parte do tempo (barras pequenas, muito espaço vazio), mas a latência ainda é alta, o problema está no tempo de espera — e o bubbleprof é a ferramenta certa.

### Clinic Heapprofiler

`clinic heapprofiler` rastreia **alocações de heap ao longo do tempo**. É diferente de um heap snapshot (`node --heap-snapshot` ou Chrome DevTools) em um aspecto fundamental:

- **Heap snapshot**: fotografia do heap em um instante — mostra o que está vivo
- **Heap allocation profiler**: filme do heap ao longo do tempo — mostra *onde* cada alocação foi feita

Essa distinção é crucial para diagnosticar memory leaks: o snapshot diz "há 500MB de strings no heap", mas o heapprofiler diz "essas strings foram alocadas na função `processUserData` na linha 42".

```bash
npx clinic heapprofiler -- node server.js
```

O relatório mostra um flamegraph de alocações, onde cada barra representa uma função e sua largura representa o total de bytes alocados a partir dali. Funções que aparecem largas e cujas alocações não diminuem ao longo do tempo são candidatas a memory leaks.

### Workflow de diagnóstico recomendado

O clinic.js é mais eficaz quando usado como um funil: começa amplo com `doctor` e afunila para a ferramenta especializada correta. Tentar começar com `flame` ou `bubbleprof` sem o diagnóstico inicial é como realizar cirurgia sem diagnóstico médico.

```
Problema de performance detectado
         │
         ▼
   clinic doctor          ← sempre primeiro
         │
   ┌─────┴──────┐
   │            │
CPU alto    I/O alto / event loop lag sem CPU
   │            │
   ▼            ▼
clinic flame  clinic bubbleprof
         │
   Heap crescendo
         │
         ▼
clinic heapprofiler
```

Cada ferramenta gera seu próprio diretório de output (ex: `.12345.clinic-doctor/`, `.12345.clinic-flame/`) com os arquivos HTML do relatório e os dados brutos de profiling. Esses diretórios podem ser grandes (vários MB) e devem ser adicionados ao `.gitignore`.

```bash
# Adicionar ao .gitignore do projeto:
*.clinic-doctor/
*.clinic-flame/
*.clinic-bubbleprof/
*.clinic-heapprofiler/
```

### Interpretando resultados

**Padrões que indicam event loop blocking:**

- No clinic doctor: event loop delay spike que coincide com CPU spike, mas sem I/O correspondente
- Causa típica: operação síncrona pesada (`JSON.parse` em payload grande, criptografia, regex catastrófica)
- Ação: mover para Worker Thread ou otimizar o algoritmo

**Padrões que indicam I/O bound:**

- No clinic doctor: event loop delay com I/O alto, CPU baixa
- No bubbleprof: bolhas grandes de operações de rede ou disco
- Causa típica: queries lentas no banco, N+1 queries, falta de connection pooling
- Ação: otimizar queries, usar cache, paralelizar com `Promise.all`

**Padrões que indicam CPU bound:**

- No clinic flame: barras largas e vermelhas (código deotimizado) ou funções próprias consumindo >20% do tempo
- Causa típica: serialização/deserialização excessiva, código não otimizado pelo V8
- Ação: simplificar código, evitar `delete` de propriedades (deotimiza shapes), usar Buffer em vez de strings para dados binários

**Padrões que indicam memory leak:**

- No clinic doctor: heap crescendo de forma monotônica ao longo do tempo, GC não consegue liberar
- No heapprofiler: alocações concentradas em poucas funções que crescem sem limite
- Causa típica: event listeners não removidos, closures retendo referências, caches sem limite de tamanho

## Na prática

### Uso básico com servidor HTTP

O fluxo mais comum é rodar a ferramenta e gerar carga manualmente em outro terminal:

```bash
# Terminal 1: inicia o servidor com clinic
npx clinic doctor -- node server.js

# Terminal 2: gera carga com autocannon
npx autocannon -c 100 -d 30 http://localhost:3000
# -c 100 = 100 conexões simultâneas
# -d 30  = duração de 30 segundos
```

Quando você para o servidor (Ctrl+C), o clinic processa os dados e abre o relatório no browser.

### Padrão --on-port (automatizado)

Para automatizar a geração de carga sem precisar de dois terminais, use `--on-port`:

```bash
# clinic inicia o servidor, espera ele abrir uma porta, então executa o comando de carga
npx clinic doctor --on-port 'autocannon -c 100 -d 30 localhost:{PORT}' -- node server.js

# O {PORT} é substituído automaticamente pela porta que o servidor abriu
```

Esse padrão é ideal para scripts de CI ou automação, pois é um único comando que:
1. Inicia o servidor
2. Detecta quando o servidor está pronto (ouvindo em uma porta)
3. Executa o load generator
4. Para e processa os resultados automaticamente

### Diagnóstico completo em sequência

```bash
# Passo 1: diagnóstico geral
npx clinic doctor --on-port 'autocannon -c 50 -d 20 localhost:{PORT}' -- node server.js

# Passo 2a: se suspeita de CPU, gerar flamegraph
npx clinic flame --on-port 'autocannon -c 50 -d 20 localhost:{PORT}' -- node server.js

# Passo 2b: se suspeita de I/O/async, usar bubbleprof
npx clinic bubbleprof --on-port 'autocannon -c 50 -d 20 localhost:{PORT}' -- node server.js

# Passo 2c: se suspeita de memory, usar heapprofiler (duração maior para ver tendência)
npx clinic heapprofiler --on-port 'autocannon -c 50 -d 60 localhost:{PORT}' -- node server.js
```

### Usando 0x diretamente

Quando o clinic flame encontra problemas (especialmente em containers sem `perf`), o `0x` pode ser usado diretamente — ele é a dependência subjacente do flame:

```bash
# Instalação
npm install -g 0x

# Uso básico
npx 0x server.js

# Com flags do Node.js
npx 0x --output-dir /tmp/flamegraphs --node-arg=--max-old-space-size=4096 server.js
```

O `0x` usa sampling do V8 (não `perf` do Linux por padrão) e é mais portável entre ambientes.

### Lendo um flamegraph na prática

Dado este flamegraph hipotético:

```
|                  processRequest (80%)                  |
|    parseJSON (5%)  |    queryDB (70%)    |  send (5%)  |
|                    |  pg.query (70%)     |             |
|                    |  net.Socket (60%)   |             |
```

Interpretação:
- `processRequest` aparece em 80% das amostras — é o entry point mais frequente
- `queryDB` consome 70% — problema claro
- `parseJSON` tem apenas 5% — não é gargalo
- `net.Socket` em 60% indica tempo de rede (I/O bound, não CPU bound)

**Conclusão**: o problema é na query ao banco, não em CPU. O bubbleprof seria a próxima ferramenta para entender o tempo de espera do `net.Socket`.

## Em entrevista

**What is clinic.js and why would you use it?**

clinic.js is an open-source performance diagnostic suite for Node.js applications, developed by NearForm. It bundles four specialized tools — `clinic doctor`, `clinic flame`, `clinic bubbleprof`, and `clinic heapprofiler` — each targeting a different category of performance problem. The key value proposition is that it requires no code changes: you wrap your startup command with the clinic CLI, generate some load, and get a rich visual HTML report. This makes it accessible for diagnosing production-like performance issues in staging environments without instrumenting every possible suspect in advance. I would reach for clinic.js when I notice elevated response times, high CPU usage, growing memory consumption, or event loop lag metrics in my observability stack — clinic helps me pinpoint the root cause systematically rather than guessing.

**How would you diagnose an event loop lag issue using clinic.js?**

My first step would be `clinic doctor`. I would run `npx clinic doctor --on-port 'autocannon -c 100 -d 30 localhost:{PORT}' -- node server.js` to capture metrics under representative load. The doctor report shows four aligned time series: CPU, memory, event loop delay, and active handles. If I see event loop delay spikes correlating with CPU spikes but without elevated I/O, that tells me there is synchronous blocking code on the main thread — the classic cause of event loop lag. Common culprits are heavy `JSON.parse` or `JSON.stringify` on large payloads, unoptimized regular expressions (catastrophic backtracking), synchronous file reads, or cryptographic operations done inline. Once I identify the pattern, I would use `clinic flame` to pinpoint exactly which function is consuming the CPU during those spikes. If the flamegraph shows a specific function taking a disproportionate slice of wall time, I would refactor it — either by moving it to a Worker Thread, optimizing the algorithm, or reducing the payload size.

**How do flamegraphs help identify CPU bottlenecks, and what should you look for?**

A flamegraph is a visualization where the horizontal axis represents the proportion of time spent in each function (wider = more time), and the vertical axis represents call stack depth (callee above, caller below). The most important things to look for are wide bars near the top of the stack — those are the "hot path" leaf functions that are actually consuming CPU, as opposed to just being intermediaries that call other functions. In clinic flame specifically, color coding tells you about V8 optimization status: blue and green frames are JIT-optimized code that runs efficiently, while red and orange frames represent deoptimized code — functions that the V8 optimizer had to bail out of for some reason, often because of type instability (a variable holding different types at different times), use of `arguments` object, `try/catch` in hot loops, or `delete` on object properties. A wide red bar is a high-priority optimization target because you can often get significant speedups just by fixing the deoptimization cause without changing the algorithm at all. It is also worth noting that flamegraphs from sampling profilers show wall time, not pure CPU time — I/O waits can appear as time in certain frames, so always cross-reference with the event loop delay and I/O charts from clinic doctor before concluding that a wide bar means pure CPU work.

## Vocabulário

**flamegraph**
: Visualização de profiling de CPU onde o eixo horizontal representa o tempo proporcional gasto em cada função (largura = tempo) e o eixo vertical representa a profundidade do call stack. Permite identificar visualmente funções "quentes" (hot paths) que consomem mais CPU.

**event loop lag**
: Atraso entre o momento em que um callback é enfileirado no event loop e o momento em que ele é efetivamente executado. Causado por operações síncronas bloqueantes ou acúmulo excessivo de microtasks. Medido em milliseconds; valores acima de 10-20ms em produção indicam problema.

**I/O bound**
: Descrição de uma operação ou aplicação cujo gargalo principal é o tempo de espera por operações de entrada/saída (rede, disco, banco de dados), e não pelo processamento de CPU. O event loop fica ocioso esperando callbacks de I/O.

**CPU bound**
: Descrição de uma operação ou aplicação cujo gargalo principal é o processamento de CPU — a aplicação está constantemente executando código e não pode processar mais requisições por falta de capacidade computacional, não por espera de I/O.

**heap allocation**
: Processo de reservar memória no heap do V8 para novos objetos JavaScript. Alocações excessivas aumentam a pressão sobre o Garbage Collector. O heapprofiler do clinic.js rastreia o site de cada alocação (qual função alocou) ao longo do tempo.

**async profiling**
: Técnica de profiling que rastreia operações assíncronas — Promises, callbacks, `async/await` — do início ao fim, medindo o tempo de espera em cada estágio. clinic bubbleprof usa `async_hooks` do Node.js para isso.

**hot path**
: Trecho de código executado com alta frequência ou que consome uma proporção desproporcional de recursos (CPU ou memória). Identificar e otimizar hot paths é a estratégia central de performance tuning; um flamegraph revela hot paths visualmente.

**wall time**
: Tempo real decorrido ("tempo de relógio de parede") para uma operação, incluindo tempo de CPU e tempo de espera por I/O ou scheduling do SO. Diferente de CPU time (apenas tempo em que a CPU estava realmente executando código). Profilers de sampling frequentemente medem wall time.

**tick time**
: Duração de um "tick" do event loop do Node.js — o tempo para completar uma iteração completa do loop (processar callbacks pendentes, executar microtasks, verificar I/O). Ticks longos causam event loop lag; o ideal é que cada tick seja de poucos milliseconds.

**deoptimização**
: Processo pelo qual o JIT compiler do V8 abandona código otimizado e volta ao modo de interpretação mais lento, geralmente porque a premissa de tipo estático do código foi violada em runtime. Aparece como frames vermelhos/laranjas em flamegraphs do clinic flame.

## Armadilhas

> [!warning] Profiling em produção: overhead significativo
> Todas as ferramentas do clinic.js adicionam overhead à aplicação — desde coleta de métricas (doctor) até sampling de V8 (flame) e hooking de async (bubbleprof). Nunca rode clinic diretamente em produção com tráfego real. Use um ambiente de staging com carga representativa gerada por ferramentas como `autocannon` ou `k6`. O overhead pode dobrar o tempo de resposta durante a coleta, o que distorceria a experiência do usuário e os resultados de negócio.

> [!warning] Saída HTML do clinic doctor: requer browser
> Por padrão, o clinic doctor abre o relatório no browser ao terminar. Em ambientes de CI sem interface gráfica (headless), isso causa erro ou timeout. Para uso em CI, utilize o padrão `--on-port` combinado com `--autocannon` para gerar relatório sem abrir browser, ou redirecione a saída e processe os arquivos gerados manualmente. Alternativamente, use a flag `--no-open` se disponível na versão instalada.

> [!warning] Flamegraph mede wall time, não apenas CPU time
> O sampling profiler do clinic flame (baseado em `0x`) captura o call stack a cada intervalo de tempo — isso é wall time sampling, não CPU time puro. Se sua aplicação tem muita espera de I/O, frames de I/O podem aparecer com barras largas mesmo sem consumir CPU. Antes de otimizar uma função por aparecer larga no flamegraph, valide com o clinic doctor se o problema é realmente CPU e não I/O. Uma barra larga de `net.Socket` significa espera de rede, não trabalho computacional.

> [!warning] Clinic flame pode precisar de privilégios em containers
> O clinic flame usa `0x`, que por sua vez pode tentar usar `perf` do Linux para profiling de alta fidelidade. Em ambientes Docker/Kubernetes sem permissões adequadas, isso falha silenciosamente ou gera erros. Soluções:
> - Adicionar `--cap-add=SYS_ADMIN` ao container Docker
> - Usar `--privileged` (não recomendado em produção)
> - Forçar modo sem `perf` usando `0x` diretamente com `--kernel-tracing=false`
> - Usar `npx 0x` standalone, que usa sampling do V8 por padrão sem necessitar de `perf`

> [!warning] Não combine --inspect com clinic tools
> Rodar sua aplicação com `--inspect` ou `--inspect-brk` (para debugger) ao mesmo tempo que uma ferramenta do clinic distorce significativamente os resultados. O protocolo do Chrome DevTools adiciona overhead de comunicação e pode alterar o comportamento do JIT compiler do V8. Sempre desative debuggers antes de fazer profiling. Da mesma forma, evite `NODE_OPTIONS=--inspect` no ambiente.

> [!warning] Duração insuficiente de coleta
> Um erro comum é rodar o clinic por apenas alguns segundos. Para detectar memory leaks, você precisa de pelo menos 60-120 segundos de coleta com carga constante para ver a tendência de crescimento do heap. Para flamegraphs de CPU, 20-30 segundos com alta concorrência são suficientes, mas durações muito curtas podem não capturar comportamentos transitórios. Ajuste a duração do autocannon (`-d`) de acordo com o problema que você está investigando.

## Veja também

- [[03-Dominios/Node/Observability e produção/index]] — MOC do galho 5
- [[05 - Node-specific metrics - event loop lag, GC, heap]] — métricas de event loop e heap
- [[08 - Detecção e diagnóstico de memory leaks]] — diagnóstico de memory leaks
- [[03-Dominios/Node/Runtime e Event Loop/index]] — event loop phases e libuv (galho 1)
- [[Node.js]] — tronco

## Fontes

- [clinic.js — documentação oficial](https://clinicjs.org/documentation/) — Guia completo das quatro ferramentas, incluindo interpretação de resultados e casos de uso.
- [0x — flamegraph profiler](https://github.com/davidmarkclements/0x) — Repositório oficial do 0x, ferramenta subjacente ao clinic flame, com documentação de flags e uso avançado.
- [Node.js Performance Hooks — async_hooks](https://nodejs.org/api/async_hooks.html) — API do Node.js usada pelo bubbleprof para rastrear operações assíncronas.
- [V8 — Understanding V8's Bytecode](https://medium.com/dailyjs/understanding-v8s-bytecode-317d46c94775) — Contexto sobre como o V8 compila e deotimiza código JavaScript, relevante para interpretar flamegraphs.
