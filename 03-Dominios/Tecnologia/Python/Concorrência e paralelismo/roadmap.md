---
title: "Roadmap — Python Concorrência e paralelismo"
created: 2026-07-10
type: meta
publish: false
tags:
  - meta
  - roadmap
  - python
---

# Roadmap — Concorrência e paralelismo (galho 7)

Roadmap-folha do galho `Python/Concorrência e paralelismo`. Fase **Adepto→Magus** — threading, multiprocessing, concurrent.futures e asyncio fundamentals, à luz do GIL já explicado no Galho 6. Spec: [[00-Meta/specs/2026-07-09-python-trilha-design]]. EXEMPLAR de estrutura: `Python/CPython internals/index.md` e `Python/CPython internals/roadmap.md` (galho anterior, mesmo padrão).

Roster **não pré-cravado no spec** (só a descrição de alto nível "GIL, threading, multiprocessing, asyncio fundamentals") — desenhado nesta sessão seguindo o mesmo playbook do Galho 5 (Tipagem moderna). Decisão de fronteira: **o GIL em si (o que é, por que existe, free-threading/PEP 703) não é reexplicado aqui** — já está fechado nas notas 04/05/06 do Galho 6 (CPython internals); este galho referencia via wikilink e foca na caixa de ferramentas prática.

> [!success] Galho 7 completo — 8/8 notas (2026-07-10)
> A capstone fechou o galho amarrando os quatro modelos (`threading`, `multiprocessing`, `concurrent.futures`, `asyncio`) numa árvore de decisão única e num cenário integrador real: servidor `asyncio` descarregando trabalho CPU-bound via `loop.run_in_executor()` + `ProcessPoolExecutor`, com as armadilhas de misturar paradigmas (locks bloqueantes dentro de coroutines, `Pool` criado sem `run_in_executor`) nomeadas explicitamente. Próximo da trilha: Galho 8 — Programação Reativa e Assíncrona.

## Tabela-resumo

| Métrica | Valor |
|---------|-------|
| Total de notas | 8 |
| ⬜ pendente | 0 |
| ✅ feita | 8 |
| 🔄 em andamento | 0 |
| % concluído | 100% |

---

## Notas

#### 01 - Threading na prática — Thread, Lock e condições de corrida
- **Estado:** ✅ feita (2026-07-10) · fase: Adepto
- **Escopo:** `threading.Thread` (criação, start/join, daemon threads), `Lock`/`RLock`, condições de corrida com bug-driven opening (contador incrementado por múltiplas threads sem lock), por que o GIL não elimina race conditions (troca de contexto pode ocorrer entre bytecodes). Link para Galho 6 nota 04 (GIL) sem reexplicar.
- **Resultado:** 472 linhas / 5722 palavras. Cobriu `Thread`/`start`/`join`/daemon threads, anatomia da race condition via `dis` do bytecode de `contador += 1` com diagramas de interleaving, o mito "GIL torna Python thread-safe" (distinção entre atomicidade de operação C individual e sequência de bytecode composta), `Lock` vs `RLock` (reentrância), `acquire(blocking=False/timeout=)`, e `threading.local` como alternativa ao lock quando o estado não precisa ser compartilhado de fato.

#### 02 - Sincronização avançada — Semaphore, Condition, Event, Barrier
- **Estado:** ✅ feita (2026-07-10) · fase: Adepto
- **Escopo:** `Semaphore`/`BoundedSemaphore` (limitar concorrência), `Condition` (espera coordenada), `Event` (sinalização simples), `Barrier` (sincronizar N threads em um ponto), deadlock (causas clássicas: lock ordering, nested locks) e como evitar.
- **Resultado:** 522 linhas / 6316 palavras. Abre com bug real de deadlock (lock ordering invertido entre `reservar_assento`/`estornar_pagamento`, com sequenceDiagram), cobre as quatro primitivas com código testável e casos de uso, aprofunda deadlock (condições de Coffman, lock ordering consistente via `sorted(key=...)`, `RLock` não resolve, `acquire(timeout=...)` como rede de segurança, diagnóstico via `faulthandler`), tabela + flowchart de decisão, armadilhas, em entrevista, inglês e fontes.

#### 03 - queue.Queue e o padrão produtor-consumidor
- **Estado:** ✅ feita (2026-07-10) · fase: Adepto
- **Escopo:** `queue.Queue`/`LifoQueue`/`PriorityQueue`, thread-safety nativa, padrão produtor-consumidor com worker pool, `task_done()`/`join()`, poison pill pattern para encerramento gracioso.
- **Resultado:** 501 linhas / 5615 palavras. Abre com bug real (reimplementar produtor-consumidor à mão com Lock+Condition), cobre as 3 variantes de fila, mecanismo de thread-safety interno (Condition por dentro), worker pool completo e funcional, `task_done()`/`join()` com sequenceDiagram, poison pill (1 por worker), armadilha de `empty()`/`full()`/`qsize()` não-confiáveis para controle de fluxo, e 2 cenários de produção (pool de downloads concorrentes, pipeline de 2 estágios encadeados).

#### 04 - multiprocessing na prática — Pool, ProcessPoolExecutor e orquestração
- **Estado:** ✅ feita (2026-07-10) · fase: Adepto→Magus
- **Escopo:** API de `multiprocessing.Pool` (`map`/`apply_async`/`imap`), `ProcessPoolExecutor` (interface concurrent.futures), quando usar cada um, `Manager` para estado compartilhado, `spawn` vs `fork` vs `forkserver` (start methods, diferença de comportamento entre SO). Link para Galho 6 nota 05 (custo de serialização/pickle, shared_memory) sem repetir — aqui é sobre orquestração/API, lá é sobre o mecanismo de custo.
- **Resultado:** 546 linhas / 6304 palavras. Abre com bug real (script `Pool`-based que funciona no Linux via herança implícita de estado global sob `fork` e quebra com `KeyError` no macOS sob `spawn`), cobre as 4 formas de despacho do `Pool` (`map`/`imap`/`imap_unordered`/`apply_async`, tabela de decisão), `chunksize`, `ProcessPoolExecutor` como interface unificada com `ThreadPoolExecutor` (tabela `Pool` vs `ProcessPoolExecutor`), `Manager` (proxies via processo servidor, custo de IPC por operação) vs `Value`/`Array` (memória compartilhada tipada, mais rápida), `fork`/`spawn`/`forkserver` em detalhe com fix via `get_context()` + `initializer`/`initargs`, árvore de decisão final, armadilhas, em entrevista, inglês e fontes.

#### 05 - concurrent.futures — a abstração unificadora
- **Estado:** ✅ feita (2026-07-10) · fase: Adepto→Magus
- **Escopo:** `ThreadPoolExecutor`/`ProcessPoolExecutor` sob a interface comum `Executor`, `Future` (submit, result, callbacks via `add_done_callback`), `as_completed` vs `map`, por que essa API existe (trocar threading↔multiprocessing sem reescrever a orquestração), quando a abstração vaza (exceções em processos, picklability).
- **Resultado:** 467 linhas / 5183 palavras. Abre com bug real (troca `ThreadPoolExecutor`→`ProcessPoolExecutor` de um cálculo de risco que quebra com `PicklingError` só no `.result()`, não no `submit()`), cobre a interface `Executor` unificada (`submit`/`map`/`shutdown`), ciclo de vida do `Future` (stateDiagram + sequenceDiagram: PENDING→RUNNING→FINISHED/CANCELLED), API completa (`.result()`, `.done()`, `.exception()`, `.add_done_callback()`, `.cancel()`), `submit()` vs `map()` vs `as_completed()` (tabela de decisão por cenário), os dois vazamentos centrais da abstração (exceções adiadas até `.result()` — inclusive fire-and-forget que engole erros — e picklability de `ProcessPoolExecutor` que só falha tarde, com fix via `initializer`/`initargs`), tabela ThreadPoolExecutor vs ProcessPoolExecutor, armadilhas, em entrevista, inglês e fontes.

#### 06 - asyncio fundamentals — event loop, coroutines e Task
- **Estado:** ✅ feita (2026-07-10) · fase: Magus
- **Escopo:** modelo de concorrência cooperativa (single-thread, sem GIL como fator), `async def`/`await`, event loop (`asyncio.run`), `Task` vs coroutine crua, por que `asyncio` é pra I/O-bound (não CPU-bound — reforça a árvore de decisão do Galho 6). Bug-driven opening: coroutine nunca aguardada (`RuntimeWarning: coroutine was never awaited`).
- **Resultado:** 411 linhas / 5975 palavras. Abre com bug real (chamar `async def` sem `await`, gerando `RuntimeWarning: coroutine was never awaited` + `TypeError` na linha seguinte), contrasta com preempção de threads/processos vistas nas notas 01-05 (concorrência cooperativa, um único thread, GIL não é fator relevante), explica `await` como cessão explícita de controle ao event loop (sequenceDiagram A/B intercaladas), aprofunda o mecanismo de `asyncio.run()` (flowchart: cria loop → agenda Task raiz → roda até completar → cancela pendentes → fecha), a distinção central `await coroutine` (sequencial, bloqueia a função) vs `asyncio.create_task()` (agenda e roda concorrentemente) com medição de tempo real (2s vs 1s) e tabela de decisão, uma camada extra sobre o que uma coroutine é por baixo (mecanismo de gerador/`yield`, por que chamar não executa), a árvore de decisão I/O-bound vs CPU-bound com o terceiro ramo asyncio (e por que uma coroutine CPU-bound sem `await` trava o loop inteiro, com exemplo de heartbeat congelado), armadilhas, em entrevista, inglês e fontes.

#### 07 - asyncio na prática — gather, TaskGroup, timeouts e cancelamento
- **Estado:** ✅ feita (2026-07-10) · fase: Magus
- **Escopo:** `asyncio.gather` vs `asyncio.TaskGroup` (3.11+, tratamento estruturado de exceções), `wait_for`/timeouts, cancelamento cooperativo (`CancelledError`, shielding), `asyncio.Lock`/`asyncio.Queue` (paralelos assíncronos das primitivas de threading).
- **Resultado:** 539 linhas / 6274 palavras. Abre com bug real (`gather()` propagando a exceção de `buscar_preco` enquanto `buscar_estoque` continua rodando em segundo plano, órfã), cobre `gather()` (ordem dos resultados, `return_exceptions=True` vs comportamento padrão), `TaskGroup` (cancelamento automático das irmãs com sequenceDiagram, `ExceptionGroup`/`except*`), `wait_for()` (mecanismo interno via `cancel()`, armadilha de código bloqueante síncrono que "surda" o timeout), cancelamento cooperativo em profundidade (por que `task.cancel()` só agenda `CancelledError` no próximo `await`, obrigatoriedade de relançar, checagem explícita em loops longos), `shield()` (proteção de operação crítica contra cancelamento externo, com ressalva de que não garante espera até o fim), e as primitivas assíncronas (`asyncio.Lock`/`Semaphore`/`Queue`) como paralelos de threading — só coordenam corrotinas do mesmo event loop, não threads reais. Tabela + flowchart `gather` vs `TaskGroup`, armadilhas, em entrevista, inglês e fontes.

#### 08 - Capstone — escolhendo threading vs multiprocessing vs asyncio
- **Estado:** ✅ feita (2026-07-10) · fase: Magus
- **Escopo:** recapitula o galho com a árvore de decisão completa (I/O-bound vs CPU-bound vs paralelismo massivo), cenário prático combinando as três (ex: servidor asyncio que descarrega CPU-bound pra um ProcessPoolExecutor via `loop.run_in_executor`), armadilhas de misturar os modelos.
- **Resultado:** 454 linhas / 6597 palavras. Árvore de decisão completa (flowchart) recapitulando o critério de cada nota 01-07; cenário integrador de servidor `asyncio` descarregando `redimensionar_imagem` (CPU-bound) via `loop.run_in_executor()` + `ProcessPoolExecutor` reaproveitado, com sequenceDiagram e código testável (`ServidorUpload`, `TaskGroup` simulando 6 requisições concorrentes); 3 armadilhas de misturar modelos (`threading.Lock` bloqueante dentro de coroutine, `Pool()`/`pool.map()` sem `run_in_executor`, `asyncio.Queue` usada por threads reais) cada uma com código errado + corrigido; 3 casos práticos (scraper assíncrono em escala, pipeline batch de hash CPU-bound sem `asyncio` nenhum, e a combinação dos dois — busca assíncrona + parsing pesado via `run_in_executor`); tabela-resumo dos 4 modelos (paralelismo real, overhead, melhor caso de uso, GIL relevante, complexidade de debugging); armadilhas, em entrevista, inglês, fechamento do galho (recap das 7 notas irmãs) e fontes.

## Decisões e fronteiras registradas

- GIL em si → Galho 6 (CPython internals), não repetido aqui.
- `aiohttp`, frameworks assíncronos completos, back-pressure → Galho 8 (Programação Reativa e Assíncrona), fora do escopo deste galho (aqui é só o "fundamentals" do asyncio).
- Serialização/pickle/shared_memory (mecanismo de custo do multiprocessing) → já coberto no Galho 6 nota 05; aqui o foco é a API de orquestração (`Pool`, `ProcessPoolExecutor`, start methods).
