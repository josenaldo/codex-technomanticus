---
title: "Roadmap — Python Core"
created: 2026-07-09
type: meta
publish: false
tags:
  - meta
  - roadmap
  - python
---

# Roadmap — Core (galho 1)

Roadmap-folha do galho `Python/Core`. Fase **Iniciado** — sintaxe, tipos, controle de fluxo, funções, erros/exceções, módulos/imports. Spec: [[00-Meta/specs/2026-07-09-python-trilha-design]]. EXEMPLAR de estrutura: `Java/Web e APIs REST/index.md` e notas 01-05 até este galho fechar e virar exemplar próprio.

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

#### 01 - O que é Python e como ele executa   [substantivo]
- **Estado:** ✅ feita (2026-07-09) · fase: Iniciado · **EXEMPLAR da trilha**
- **Escopo:** interpretador, bytecode (.pyc), REPL, CPython vs outras implementações (PyPy, MicroPython), o ciclo `.py` → compilação → execução.
- **Resultado:** 323 linhas / 5147 palavras; Mermaid, 2 [!warning], 3 [!question]-. Fontes: Real Python (6 artigos), docs.python.org/PEPs (6), PyPy/MicroPython/Jython.

#### 02 - Tipos e variáveis
- **Estado:** ✅ feita (2026-07-09) · fase: Iniciado
- **Escopo:** dynamic+strong typing, variável como rótulo (não caixa), mutabilidade vs imutabilidade, armadilha do mutable default argument, `None`, tipos primitivos, `is` vs `==`.
- **Resultado:** 450 linhas / 4547 palavras; Mermaid, [!warning] dedicado ao mutable default. Fontes: Real Python (3), Fluent Python, docs.python.org data model.

#### 03 - Operadores e expressões
- **Estado:** ✅ feita (2026-07-09) · fase: Iniciado
- **Escopo:** aritméticos (`/` vs `//`, `**`), comparação encadeada, `and`/`or` retornando operando, bitwise, atribuição aumentada (`__iadd__`), tabela de precedência, walrus operator (PEP 572).
- **Resultado:** 445 linhas / 4845 palavras; Mermaid. Fontes: docs.python.org, PEP 572, PEP 465, Real Python, Python Morsels.

#### 04 - Controle de fluxo — if/elif/else e match/case
- **Estado:** ✅ feita (2026-07-09) · fase: Iniciado
- **Escopo:** truthiness (falsy table, `__bool__`/`__len__`), ternário, match/case (destructuring de sequência/dict/classe, guards, `__match_args__`), debate match vs if/elif.
- **Resultado:** 572 linhas / 4882 palavras; Mermaid. Fontes: PEP 634/635/636, PEP 308, Real Python, Ben Hoyt (benchmark).

#### 05 - Loops — for, while, range, enumerate, zip
- **Estado:** ✅ feita (2026-07-09) · fase: Iniciado
- **Escopo:** `for` como for-each, `range` lazy, `enumerate`, `zip` (truncamento + `strict=True`), `while`, `break`/`continue`, cláusula `else` de loop.
- **Resultado:** 491 linhas / 4739 palavras; Mermaid. Fontes: docs.python.org, Real Python, Python Morsels, Alyssa Coghlan.

#### 06 - Funções — definição, argumentos e escopo básico
- **Estado:** ✅ feita (2026-07-09) · fase: Iniciado
- **Escopo:** posicional/nomeado/default (referencia mutable default da nota 02), `*args`/`**kwargs`, positional-only `/` e keyword-only `*` (PEP 570/3102), LEGB.
- **Resultado:** 538 linhas / 5669 palavras; Mermaid (cadeia LEGB). Fontes: docs.python.org, Real Python, PEP 570, PEP 3102, Fluent Python.

#### 07 - Strings e formatação
- **Estado:** ✅ feita (2026-07-09) · fase: Iniciado
- **Escopo:** imutabilidade, métodos de string, slicing, as 3 gerações de formatação (%/`.format`/f-string), format specs, debug f-strings, `str` vs `bytes`/encoding.
- **Resultado:** 506 linhas / 5458 palavras; 2 Mermaid. Fontes: Real Python (f-strings, encodings), PEP 3101/498/701.

#### 08 - Erros e exceções
- **Estado:** ✅ feita (2026-07-09) · fase: Iniciado
- **Escopo:** try/except/else/finally, hierarquia de exceções, `raise`/`raise ... from ...`, exceções customizadas, seção dedicada EAFP vs LBYL.
- **Resultado:** 628 linhas / 6018 palavras; 2 Mermaid. Fontes: docs.python.org, Real Python, Microsoft Python DevBlog, PEP 8.

#### 09 - Módulos e imports
- **Estado:** ✅ feita (2026-07-09) · fase: Iniciado · **FECHA o galho**
- **Escopo:** sistema de import, `sys.path`, pacotes regulares vs namespace packages (PEP 420), imports absolutos/relativos (PEP 328), `__name__ == "__main__"`, circular imports, recapitulação do Galho 1 + ponte pros Galhos 2/3.
- **Resultado:** 585 linhas / 6705 palavras; 2 Mermaid. Fontes: docs.python.org, PEP 328/420, Real Python, Alyssa Coghlan.
