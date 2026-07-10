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
| ⬜ pendente | 6 |
| ✅ feita | 3 |
| 🔄 em andamento | 0 |
| % concluído | 33% |

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
- **Estado:** ⬜ pendente · fase: Magus
- **Escopo:** Global Interpreter Lock como mecanismo de proteção do reference counting (não do "estado global" em geral), o mito popular vs. o motivo real, `sys.setswitchinterval()`, quando o GIL é liberado (I/O, extensões C, `numpy`), por que threads Python não paralelizam CPU-bound.

#### 05 - GIL e concorrência na prática — threading vs multiprocessing
- **Estado:** ⬜ pendente · fase: Magus
- **Escopo:** impacto real do GIL em `threading` (útil pra I/O-bound, inútil pra CPU-bound), `multiprocessing` como fuga (processos separados, cada um com seu GIL), custo de serialização entre processos, ponte explícita pro Galho 7 (Concorrência e paralelismo), onde o tema é aprofundado.

#### 06 - Free-threading — o GIL opcional (PEP 703)
- **Estado:** ⬜ pendente · fase: Magus
- **Escopo:** PEP 703 (Python 3.13+, build `--disable-gil`/"free-threaded"), o que muda de verdade (biased reference counting, per-object locks), estado atual (experimental/opt-in, ecossistema de extensões C ainda adaptando), o que muda pro dia a dia de quem não compila Python do zero.

#### 07 - Memory management — allocators, pymalloc e arenas
- **Estado:** ⬜ pendente · fase: Magus
- **Escopo:** hierarquia de alocadores do CPython (`pymalloc` sobre `malloc` do SO), arenas/pools/blocks (256KB/4KB/tamanhos fixos), por que objetos pequenos são rápidos de alocar em Python, `sys.getallocatedblocks()`, quando Python "devolve" memória pro SO de fato (raramente — arena freeing).

#### 08 - Profiling — `cProfile`, `py-spy`, `tracemalloc`
- **Estado:** ⬜ pendente · fase: Magus
- **Escopo:** `cProfile`/`profile` (profiling determinístico, overhead), `py-spy` (sampling profiler, attach em processo rodando, zero instrumentação), `tracemalloc` (rastreamento de alocação de memória, achar vazamentos), `memory_profiler` como bônus, quando usar cada ferramenta.

#### 09 - Capstone — CPython internals
- **Estado:** ⬜ pendente · fase: Magus · **FECHA o galho**
- **Escopo:** recapitulação do galho diagnosticando e otimizando um programa Python real (ex.: função lenta identificada via `cProfile`, vazamento de memória via ciclo de referência achado via `tracemalloc`/`gc`, decisão threading vs. multiprocessing justificada pelo GIL), ponte pro Galho 7 (Concorrência e paralelismo).
