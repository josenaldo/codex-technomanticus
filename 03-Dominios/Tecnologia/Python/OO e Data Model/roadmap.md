---
title: "Roadmap — Python OO e Data Model"
created: 2026-07-09
type: meta
publish: false
tags:
  - meta
  - roadmap
  - python
---

# Roadmap — OO e Data Model (galho 3)

Roadmap-folha do galho `Python/OO e Data Model`. Fase **Adepto→Magus** — o coração do "Python Fluente" (Ramalho). Spec: [[00-Meta/specs/2026-07-09-python-trilha-design]]. EXEMPLAR de estrutura: `Python/Core/index.md` e `Python/Collections e Comprehensions/index.md`.

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

#### 01 - Classes — definição, atributos e métodos   [substantivo]
- **Estado:** ✅ feita (2026-07-09) · fase: Adepto
- **Escopo:** `self`/bound methods, `__init__` vs `__new__`, atributo de classe mutável compartilhado (paralelo com mutable default do Core), `@classmethod`/`@staticmethod`.
- **Resultado:** 522 linhas / 5610 palavras; 3 Mermaid, [!warning] dedicado. Fontes: docs.python.org, Real Python, Fluent Python (Ramalho).

#### 02 - Herança e MRO
- **Estado:** ✅ feita (2026-07-09) · fase: Adepto
- **Escopo:** `super()` MRO-aware, herança múltipla real (vs Java), diamond problem, C3 linearization, `__mro__`, isinstance/issubclass, ponte pra Mixins (nota 09).
- **Resultado:** 483 linhas / 4758 palavras; 2 Mermaid. Fontes: docs.python.org (C3 histórico), Raymond Hettinger, Real Python.

#### 03 - O Data Model — dunder methods essenciais
- **Estado:** ✅ feita (2026-07-09) · fase: Adepto→Magus · **nota central do galho**
- **Escopo:** `__repr__` vs `__str__`, `__eq__`/`__hash__` (contrato de hashability), `__len__`/`__bool__`, `__getitem__`/`__iter__` (exemplo FrenchDeck-style + Vetor2D).
- **Resultado:** 517 linhas / 5511 palavras; 3 Mermaid, [!warning] dedicado. Fontes: Fluent Python (Ramalho, fonte canônica), docs.python.org Data Model, Hynek Schlawack.

#### 04 - Properties e encapsulamento
- **Estado:** ✅ feita (2026-07-09) · fase: Adepto
- **Escopo:** `@property`/setter/deleter, `_convenção` vs `__name mangling`, filosofia "consenting adults", quando encapsular de fato importa.
- **Resultado:** 539 linhas / 5343 palavras; 2 Mermaid, 2 [!warning]. Fontes: docs.python.org, Real Python, Effective Python (Slatkin), Fluent Python.

#### 05 - Dataclasses
- **Estado:** ✅ feita (2026-07-09) · fase: Adepto
- **Escopo:** `@dataclass` (PEP 557), `field()`/default_factory, `__post_init__`, `frozen`/`order`/`kw_only`, comparação de 3 vias (manual/namedtuple/dataclass), ponte pro Pydantic (Galho 5).
- **Resultado:** 506 linhas / 5520 palavras; 3 Mermaid. Fontes: PEP 557, docs.python.org, Real Python, Fluent Python.

#### 06 - ABC e Protocol — tipagem estrutural
- **Estado:** ✅ feita (2026-07-09) · fase: Adepto→Magus
- **Escopo:** `abc.ABC`/`@abstractmethod` (nominal), `typing.Protocol` (structural, PEP 544), `@runtime_checkable` e suas limitações, `collections.abc` mapeado aos dunders da nota 03.
- **Resultado:** 506 linhas / 5157 palavras; 2 Mermaid. Fontes: PEP 544, docs.python.org, mypy docs, Fluent Python.

#### 07 - Operator overloading e protocolos avançados
- **Estado:** ✅ feita (2026-07-09) · fase: Magus · **abre o bloco Magus**
- **Escopo:** `__add__`/`__radd__` (despacho duplo), `__iadd__` in-place, `__call__`, `__enter__`/`__exit__` (protocolo completo do `with`), `contextlib.contextmanager`.
- **Resultado:** 601 linhas / 5701 palavras; 4 Mermaid. Fontes: Fluent Python cap. 16, docs.python.org, PEP 343, Real Python.

#### 08 - Metaclasses — introdução
- **Estado:** ✅ feita (2026-07-09) · fase: Magus
- **Escopo:** `type` como metaclasse padrão/fábrica de classes, metaclasse customizada, casos reais (Django ModelBase, ABCMeta), citação de Tim Peters, alternativas (`__init_subclass__`, decorators de classe).
- **Resultado:** 376 linhas / 5053 palavras; 2 Mermaid. Fontes: Real Python, docs.python.org, PEP 487, Fluent Python.

#### 09 - Composição vs herança
- **Estado:** ✅ feita (2026-07-09) · fase: Magus · **FECHA o galho**
- **Escopo:** "favor composition over inheritance" (GoF), Pato/PatoDeBorracha, fragile base class, exemplo Robô com composição, Mixins retomados, recapitulação do galho, ponte pros Galhos 4 e 5.
- **Resultado:** 433 linhas / 5540 palavras; 2 Mermaid. Fontes: Design Patterns (GoF), python-patterns.guide, Effective Python (Slatkin), Fluent Python.
