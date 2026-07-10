---
title: "Roadmap — Python Collections e Comprehensions"
created: 2026-07-09
type: meta
publish: false
tags:
  - meta
  - roadmap
  - python
---

# Roadmap — Collections e Comprehensions (galho 2)

Roadmap-folha do galho `Python/Collections e Comprehensions`. Fase **Iniciado→Adepto**. Spec: [[00-Meta/specs/2026-07-09-python-trilha-design]]. EXEMPLAR de estrutura: `Python/Core/index.md` e suas 9 notas.

## Tabela-resumo

| Métrica | Valor |
|---------|-------|
| Total de notas | 8 |
| ⬜ pendente | 0 |
| ✅ feita | 8 |
| 🔄 em andamento | 0 |
| % concluído | 100% ✅ |

---

## Notas

#### 01 - Listas — criação, métodos e slicing avançado   [substantivo]
- **Estado:** ✅ feita (2026-07-09) · fase: Iniciado
- **Escopo:** criação, `.append` vs `.extend`, `.sort()` in-place vs `sorted()`, slicing avançado, cópia rasa (`.copy()`/`list(x)`/`x[:]`) vs profunda, a armadilha do `[[0]*3]*3`.
- **Resultado:** 481 linhas / 4729 palavras; 2 Mermaid, 2 [!warning]. Fontes: docs.python.org, Real Python, Python Morsels.

#### 02 - Tuplas e desempacotamento
- **Estado:** ✅ feita (2026-07-09) · fase: Iniciado
- **Escopo:** imutabilidade estrutural, tupla-como-registro vs lista-como-sequência, hashability, packing/unpacking, swap idiomático, unpacking estendido (PEP 3132), ponte pro namedtuple.
- **Resultado:** 457 linhas / 4501 palavras; 2 Mermaid. Fontes: Real Python, PEP 3132, docs.python.org, Python Morsels.

#### 03 - Dicionários
- **Estado:** ✅ feita (2026-07-09) · fase: Iniciado
- **Escopo:** `d.get()` vs `d[key]` (ponte EAFP/LBYL), views dinâmicas, dict merge (PEP 584), história da ordem de inserção 3.6→3.7, hashability de chaves.
- **Resultado:** 557 linhas / 5574 palavras; 2 Mermaid. Fontes: docs.python.org, Real Python, PEP 584, Fluent Python.

#### 04 - Sets
- **Estado:** ✅ feita (2026-07-09) · fase: Iniciado · **fecha o bloco Iniciado**
- **Escopo:** operações de conjunto, `{}` vazio é dict não set, `in` O(1) vs O(n) com benchmark real, `frozenset`, hashability.
- **Resultado:** 439 linhas / 4863 palavras; 3 Mermaid. Fontes: docs.python.org, Real Python, switowski.com (benchmark).

#### 05 - Comprehensions — list, dict, set e generator expressions
- **Estado:** ✅ feita (2026-07-09) · fase: Adepto · **abre o bloco Adepto**
- **Escopo:** list/dict/set comprehensions, performance vs loop, ternário vs filtro, generator expressions (introdução), comprehensions aninhadas, o limite de legibilidade.
- **Resultado:** 453 linhas / 5240 palavras; Mermaid. Fontes: PEP 202/289/274/20, Real Python, Fluent Python.

#### 06 - itertools — os essenciais
- **Estado:** ✅ feita (2026-07-09) · fase: Adepto
- **Escopo:** `chain`, `product`, `combinations`/`permutations`, `groupby` (com armadilha de dados não-ordenados aprofundada), `islice`, iteradores infinitos (`count`/`cycle`/`repeat`) com cautela.
- **Resultado:** 430 linhas / 4838 palavras; 1 Mermaid, 2 [!warning], 1 [!question]. Fontes: docs.python.org, Real Python, Fluent Python, more-itertools.

#### 07 - O módulo collections — Counter, defaultdict, deque, namedtuple
- **Estado:** ✅ feita (2026-07-09) · fase: Adepto
- **Escopo:** `Counter` (contagem/aritmética), `defaultdict` (vs `.setdefault()` manual), `deque` (O(1) nas duas pontas, `maxlen`), `namedtuple` (vs `dataclass`, ponte pro Galho 3).
- **Resultado:** 635 linhas / 6213 palavras; 2 Mermaid. Fontes: Real Python (4), docs.python.org, PEP 557.

#### 08 - Escolhendo a estrutura certa
- **Estado:** ✅ feita (2026-07-09) · fase: Adepto · **FECHA o galho**
- **Escopo:** capstone — tabela Big-O comparativa (list/tuple/dict/set/deque), framework de decisão em árvore, recapitulação do galho, ponte pros Galhos 3 e 4.
- **Resultado:** 322 linhas / 4657 palavras; Mermaid. Fontes: wiki.python.org/TimeComplexity, docs.python.org, Real Python.
