---
title: "Roadmap — Python CPython internals"
created: 2026-07-10
type: meta
publish: false
tags:
  - meta
  - roadmap
  - python
---

# Roadmap — CPython internals (galho 6)

Roadmap-folha do galho `Python/CPython internals`. Fase **Magus** — o "como por dentro" do interpretador de referência: objetos, memória, GIL e profiling. Equivalente ao galho [[03-Dominios/Tecnologia/Java/JVM/index|JVM]] do Java. Spec: [[00-Meta/specs/2026-07-09-python-trilha-design]]. EXEMPLAR de estrutura: `Python/Core/index.md` (nota 01 revisitada aqui em profundidade), `Python/Tipagem moderna/index.md`.

## Tabela-resumo

| Métrica | Valor |
|---------|-------|
| Total de notas | 9 |
| ⬜ pendente | 0 |
| ✅ feita | 9 |
| 🔄 em andamento | 0 |
| % concluído | 100% ✅ |

---

## Notas

#### 01 - O interpretador por dentro — ceval loop e frame objects
- **Estado:** ✅ feita (2026-07-10) · fase: Magus
- **Escopo:** revisita `Core/01` com profundidade CPython real — o loop `ceval.c` (`_PyEval_EvalFrameDefault`), frame objects (`PyFrameObject`), a pilha de avaliação, como bytecode vira execução de fato (não só o que foi mostrado no Core, mas o "motor" por trás), diferença entre CPython/PyPy/outras implementações citada brevemente.
- **Resultado:** 259 linhas / 4690 palavras — abaixo da densidade-alvo (440-540) por causa de erro de limite de sessão que interrompeu o agente antes do fechamento pleno; estrutura completa (TL;DR, Como funciona, Armadilhas, Em entrevista, Fontes datadas). Cobre split `_PyInterpreterFrame`/`PyFrameObject` (3.11+), especialização adaptativa (PEP 659), JIT experimental (PEP 744), contraste PyPy/MicroPython. Desvio registrado — candidato a passada de enriquecimento futura.

#### 02 - Objetos em CPython — `PyObject`, refcounting e tipos internos
- **Estado:** ✅ feita (2026-07-10) · fase: Magus
- **Escopo:** `PyObject`/`PyVarObject` (struct C por trás de todo objeto Python), `ob_refcnt`/`ob_type`, por que "tudo é objeto" tem custo de memória real, small int cache (-5 a 256), string interning, `sys.getrefcount()`/`sys.getsizeof()` na prática.
- **Resultado:** 362 linhas / 4907 palavras — mesmo desvio de densidade da nota 01 (sessão interrompida), estrutura completa (O que é/Por que importa/Como funciona/Na prática/Armadilhas/Em entrevista/Fontes). Números de `sys.getsizeof`/`sys.getrefcount` medidos empiricamente em CPython 3.12.3 nesta sessão.

#### 03 - Reference counting e o Garbage Collector geracional
- **Estado:** ✅ feita (2026-07-10) · fase: Magus
- **Escopo:** reference counting como mecanismo primário (determinístico, ao contrário do GC da JVM), o problema de ciclos de referência (`a.x = b; b.x = a`), o GC geracional (3 gerações, `gc` module, `gc.collect()`), `__del__` e finalização, `weakref` como saída pra ciclos sem GC.
- **Resultado:** 349 linhas / 5184 palavras — mesmo desvio de densidade das notas 01-02 (sessão interrompida), estrutura completa. Contraste explícito com `Java/JVM/03 - Garbage Collection` (tracing vs. refcounting). Fontes: PEP 442, Real Python (weakref), Fluent Python (Ramalho).

#### 04 - O GIL — o que é de verdade e por que existe
- **Estado:** ✅ feita (2026-07-10) · fase: Magus
- **Escopo:** Global Interpreter Lock como mecanismo de proteção do reference counting (não do "estado global" em geral), por que `ob_refcnt++`/`--` não é atômico em C e o *lost update* que isso causaria sem lock, `sys.setswitchinterval()`, quando o GIL é liberado (I/O bloqueante, `Py_BEGIN_ALLOW_THREADS`, NumPy), por que threads Python não paralelizam CPU-bound mas paralelizam I/O-bound de verdade.
- **Resultado:** 428 linhas / 6847 palavras — densidade completa, dentro/acima do alvo de 440-540 (ligeiramente abaixo em linhas, dentro em palavras), acima das notas 01-03 do galho. Estrutura completa (TL;DR, Como funciona, contraste GIL vs. threads Java vs. event loop Node.js, diagnóstico de contenção via `py-spy`, Armadilhas, Em entrevista com follow-up sobre free-threading/PEP 703/779, Fontes datadas). Verificado via WebSearch: estado atual do free-threading (Python 3.13 experimental, 3.14 oficialmente suportado sob PEP 779, GIL-off por padrão só ~2027-2028), sub-interpretadores com GIL próprio (PEP 684) citados como nuance.

#### 05 - GIL e concorrência na prática — threading vs multiprocessing
- **Estado:** ✅ feita (2026-07-10) · fase: Magus
- **Escopo:** impacto real do GIL em `threading` (útil pra I/O-bound, inútil pra CPU-bound), `multiprocessing` como fuga (processos separados, cada um com seu GIL), custo de serialização entre processos, ponte explícita pro Galho 7 (Concorrência e paralelismo), onde o tema é aprofundado.
- **Resultado:** 434 linhas / 6773 palavras — densidade completa, muito próxima da nota 04. Estrutura completa (TL;DR, mecanismo de isolamento de memória entre processos, custo de `pickle`/IPC, `shared_memory` como mitigação, `fork`/`spawn`/`forkserver`, `Queue`/`Pipe`, 2 cenários medidos, tabela de decisão I/O-bound vs CPU-bound, 4 armadilhas, Em entrevista com follow-up sobre `asyncio`, Fontes datadas). Continuação direta da nota 04; ponte honesta pro Galho 7 (ainda não escrito). Fontes: pythonspeed.com, docs oficiais de `shared_memory`/`pickle`/start methods/`concurrent.futures`, PEP 574, PEP 734.

#### 06 - Free-threading — o GIL opcional (PEP 703)
- **Estado:** ✅ feita (2026-07-10) · fase: Magus
- **Escopo:** PEP 703 (Python 3.13+, build `--disable-gil`/"free-threaded"), o que muda de verdade (biased reference counting, per-object locks), estado atual (experimental/opt-in, ecossistema de extensões C ainda adaptando), o que muda pro dia a dia de quem não compila Python do zero.
- **Resultado:** 312 linhas / 6031 palavras — abaixo do piso de linhas mas dentro do alvo de palavras (padrão do galho). Estrutura completa: 4 mecanismos (BRC, objetos imortais, contagem diferida, critical sections), tabela de overhead, estado do ecossistema (NumPy/SciPy/pandas suportados; psycopg não, issue real citada), 3 cenários práticos, 5 armadilhas. Fontes: PEP 703, PEP 779, py-free-threading.github.io, Quansight Labs, Victor Stinner.

#### 07 - Memory management — allocators, pymalloc e arenas
- **Estado:** ✅ feita (2026-07-10) · fase: Magus
- **Escopo:** hierarquia de alocadores do CPython (`pymalloc` sobre `malloc` do SO), arenas/pools/blocks (256KB/4KB/tamanhos fixos), por que objetos pequenos são rápidos de alocar em Python, `sys.getallocatedblocks()`, quando Python "devolve" memória pro SO de fato (raramente — arena freeing).
- **Resultado:** 303 linhas / 5754 palavras — abaixo do piso de linhas mas dentro do alvo de palavras (padrão do galho). Estrutura completa: hierarquia arena(1MiB 64-bit)/pool(4KiB)/block(8-512B, 64 classes), contraste com heap-com-GC da JVM, 3 cenários (RSS falso vazamento, reciclagem de workers Celery, NumPy/pandas), 4 armadilhas. Fontes: docs.python.org/c-api/memory.html, obmalloc.c, rushter.com, evanjones.ca, Real Python, Fluent Python.

#### 08 - Profiling — `cProfile`, `py-spy`, `tracemalloc`
- **Estado:** ✅ feita (2026-07-10) · fase: Magus
- **Escopo:** `cProfile`/`profile` (profiling determinístico, overhead), `py-spy` (sampling profiler, attach em processo rodando, zero instrumentação), `tracemalloc` (rastreamento de alocação de memória, achar vazamentos), `memory_profiler` como bônus, quando usar cada ferramenta.
- **Resultado:** 417 linhas / 6320 palavras — mesmo desvio de densidade em linhas do restante do galho, dentro do alvo de palavras. 3 Mermaid, 4 [!warning]. Overhead de `cProfile` medido empiricamente (4.3x), diff de `tracemalloc` (36.6 MiB). Conecta explicitamente com refcounting (03), GIL (04), pymalloc (07). Fontes: docs.python.org, GitHub py-spy, SnakeViz, PyPI memory_profiler, Real Python.

#### 09 - Capstone — CPython internals
- **Estado:** ✅ feita (2026-07-10) · fase: Magus · **FECHA o galho**
- **Escopo:** recapitulação do galho diagnosticando e otimizando um serviço real com vazamento aparente de memória — arenas/pymalloc (07) → `tracemalloc` confirma crescimento real (08) → ciclo de referência + `__del__` frágil (02/03) → `weakref` corrige → GIL barra paralelismo em threads (04) → `multiprocessing` com custo de `pickle` explicitado (05) → free-threading descartado honestamente por hoje (06) → ganho confirmado via `cProfile`/`py-spy` (08) → fecha citando o `ceval.c` (01) como motor de tudo. Ponte pro Galho 7 (Concorrência e paralelismo).
- **Resultado:** 501 linhas / 8201 palavras — densidade completa, acima do piso Magus. 3 Mermaid, 4 [!warning], linka as 8 notas irmãs do galho. Fontes: PEPs 442/659/703/744/779, docs.python.org, CPython InternalDocs, py-spy, pythonspeed.com, Fluent Python (Ramalho).
