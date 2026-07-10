---
title: "Roadmap — Python Funcional e idiomas avançados"
created: 2026-07-10
type: meta
publish: false
tags:
  - meta
  - roadmap
  - python
---

# Roadmap — Funcional e idiomas avançados (galho 4)

Roadmap-folha do galho `Python/Funcional e idiomas avançados`. Fase **Adepto→Magus** — o "como por dentro" de generators, iterators, decorators e closures, mais o kit `functools`. Spec: [[00-Meta/specs/2026-07-09-python-trilha-design]]. EXEMPLAR de estrutura: `Python/Core/index.md`, `Python/Collections e Comprehensions/index.md`, `Python/OO e Data Model/index.md`.

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

#### 01 - Iterators e o protocolo `__iter__`/`__next__`
- **Estado:** ✅ feita (2026-07-10) · fase: Adepto
- **Escopo:** protocolo iterator completo (`__iter__` retorna self ou outro objeto, `__next__` levanta `StopIteration`), iterator vs iterable, `iter()`/`next()` embutidos, aprofunda o que `Python/OO e Data Model/03` só tocou via Data Model, `itertools` como ponte (já visto no Galho 2).
- **Resultado:** 466 linhas / 5057 palavras; 2 Mermaid, 4 [!warning], 3 [!question]-. Fontes: docs.python.org, PEP 234, Real Python, Fluent Python (Ramalho).

#### 02 - Generators — `yield` e generator functions
- **Estado:** ✅ feita (2026-07-10) · fase: Adepto
- **Escopo:** generator functions (`yield` suspende/retoma estado), diferença de generator expressions (já vistas no Galho 2), lazy evaluation, `send()`/`throw()`/`close()`, por que generators implementam o protocolo iterator de graça.
- **Resultado:** 449 linhas / 5919 palavras; 3 Mermaid, 6 [!warning], 2 [!question]-. Fontes: PEP 255, PEP 342, docs.python.org, Real Python, Fluent Python (Ramalho).

#### 03 - `yield from` e delegação de generators
- **Estado:** ✅ feita (2026-07-10) · fase: Adepto→Magus
- **Escopo:** `yield from` como delegação transparente (PEP 380), subgenerators, propagação de valores/exceções, caso de uso real (flatten de estruturas aninhadas, pipelines de geradores).
- **Resultado:** 388 linhas / 5310 palavras; 1 Mermaid, 4 [!warning], 2 [!question]-. Fontes: PEP 380, PEP 342, PEP 492, docs.python.org, Real Python, Fluent Python (Ramalho).

#### 04 - Closures de verdade
- **Estado:** ✅ feita (2026-07-10) · fase: Adepto
- **Escopo:** free variables, `nonlocal`, factory functions, o que ficou pendente do Core nota 06 (LEGB), late binding em closures dentro de loops (armadilha clássica), comparação com o modelo de closures de outras linguagens.
- **Resultado:** 486 linhas / 6195 palavras; 2 Mermaid, 5 [!warning], 4 [!question]-. Fontes: PEP 3104, docs.python.org, Real Python, Fluent Python (Ramalho), Baeldung/Oracle (comparação Java).

#### 05 - Decorators — fundamentos
- **Estado:** ✅ feita (2026-07-10) · fase: Adepto→Magus
- **Escopo:** funções como cidadãos de primeira classe, decorator sem argumento (`@decorador`), `*args`/`**kwargs` no wrapper, por que decorators são só açúcar sintático pra `func = decorador(func)`, casos de uso (logging, timing, memoização simples).
- **Resultado:** 418 linhas / 5124 palavras; 2 Mermaid, 5 [!warning], 4 [!question]-. Fontes: docs.python.org (glossário, functools), PEP 318, Real Python, Fluent Python (Ramalho).

#### 06 - Decorators com argumentos e `functools.wraps`
- **Estado:** ✅ feita (2026-07-10) · fase: Magus
- **Escopo:** decorator factory (decorator que recebe argumentos), 3 níveis de aninhamento de função, `functools.wraps` e por que preservar `__name__`/`__doc__` importa, decorators empilhados (ordem de aplicação).
- **Resultado:** 501 linhas / 6418 palavras; 4 Mermaid, 5 [!warning]. Fontes: docs.python.org (functools.wraps), PEP 318, Real Python, Fluent Python (Ramalho), Design Patterns (GoF).

#### 07 - `functools` — ferramentas funcionais
- **Estado:** ✅ feita (2026-07-10) · fase: Adepto→Magus
- **Escopo:** `lru_cache`/`cache` (memoização real, contraste com a memoização manual da nota 05), `partial`/`partialmethod` (aplicação parcial), `reduce` (por que saiu de built-in — PEP 3100, quando ainda faz sentido vs. builtins nomeados), `singledispatch`/`singledispatchmethod` (polimorfismo por tipo de argumento, ponte com `Protocol`/`ABC` do Galho 3).
- **Resultado:** 481 linhas / 6029 palavras; 2 Mermaid, 6 [!warning], 3 [!question]-. Fontes: docs.python.org (functools), PEP 3100, PEP 443, Real Python, Fluent Python (Ramalho), Artima (Guido van Rossum).

#### 08 - Context managers via generator
- **Estado:** ✅ feita (2026-07-10) · fase: Magus
- **Escopo:** `@contextlib.contextmanager`, `yield` como ponto de divisão `__enter__`/`__exit__`, tratamento de exceção dentro do gerador (relançada no ponto do `yield`, via `.throw()` interno), comparação com o protocolo `__enter__`/`__exit__` manual (já visto em `OO e Data Model/07`), `contextlib.suppress`/`ExitStack` como bônus.
- **Resultado:** 501 linhas / 5637 palavras; 2 Mermaid, 6 [!warning], 3 [!question]-. Fontes: docs.python.org (contextlib), PEP 343, PEP 342, Real Python, Fluent Python (Ramalho).

#### 09 - Capstone — funcional e idiomas avançados
- **Estado:** ✅ feita (2026-07-10) · fase: Magus · **FECHA o galho**
- **Escopo:** recapitulação do galho amarrando generators (`yield from`)+closures+decorators (simples e com argumentos, `functools.wraps`)+functools (`lru_cache`/`singledispatch`)+context manager via generator num pipeline ETL lazy único, ponte pro Galho 5 (Tipagem moderna).
- **Resultado:** 510 linhas / 5802 palavras; 2 Mermaid, 5 [!warning], 3 [!question]-. Fontes: docs.python.org, PEPs 255/342/380/318/343, Real Python, Fluent Python (Ramalho).
