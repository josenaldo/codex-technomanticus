---
title: "Roadmap — Python Tipagem moderna"
created: 2026-07-10
type: meta
publish: false
tags:
  - meta
  - roadmap
  - python
---

# Roadmap — Tipagem moderna (galho 5)

Roadmap-folha do galho `Python/Tipagem moderna`. Fase **Adepto** — type hints, generics, checagem estática (mypy/pyright) e validação em runtime (Pydantic). Spec: [[00-Meta/specs/2026-07-09-python-trilha-design]]. EXEMPLAR de estrutura: `Python/Core/index.md`, `Python/OO e Data Model/index.md`, `Python/Funcional e idiomas avançados/index.md`.

> [!note] Fronteira com o Galho 3
> `typing.Protocol` e `abc.ABC` (tipagem estrutural vs. nominal) já foram cobertos em profundidade em [[03-Dominios/Tecnologia/Python/OO e Data Model/06 - ABC e Protocol — tipagem estrutural|OO e Data Model/06]]. Este galho não repete esse conteúdo — assume-o como pré-requisito e foca em type hints básicos, generics, tooling estático e Pydantic.

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

#### 01 - Type hints — fundamentos e gradual typing
- **Estado:** ✅ feita (2026-07-10) · fase: Adepto
- **Escopo:** anotações de variáveis/parâmetros/retorno (PEP 484), gradual typing (Python continua dinamicamente tipado em runtime — hints são só metadados, ignorados pelo interpretador salvo introspecção explícita), `__annotations__`, diferença entre type hint e type checking de fato, quando vale a pena tipar.
- **Resultado:** 449 linhas / 6199 palavras; 1 Mermaid, 5 [!warning], 3 [!question]-. Fontes: PEP 484, PEP 526, PEP 3107, PEP 563, PEP 649, docs.python.org (typing), Real Python, Fluent Python (Ramalho).

#### 02 - Union, Optional e o operador `|`
- **Estado:** ✅ feita (2026-07-10) · fase: Adepto
- **Escopo:** `Optional[X]` = `Union[X, None]`, PEP 604 (`X | Y`, Python 3.10+) substituindo `Union`/`Optional` na sintaxe moderna, narrowing de tipo (`if x is not None`), `None` como valor de retorno implícito e suas armadilhas de tipagem.
- **Resultado:** 406 linhas / 5634 palavras; 1 Mermaid, 5 [!warning]. Fontes: docs.python.org, PEP 604, PEP 484, mypy cheat sheet/issue #6687, comparação Java/Kotlin.

#### 03 - Generics — `TypeVar`, `Generic` e sintaxe moderna
- **Estado:** ✅ feita (2026-07-10) · fase: Adepto
- **Escopo:** `TypeVar`, classes genéricas via `Generic[T]`, PEP 585 (generics nos builtins: `list[int]` em vez de `List[int]`, Python 3.9+), PEP 695 (sintaxe `class Pilha[T]`/`def f[T](x: T) -> T`, Python 3.12+), bound/constrained TypeVars.
- **Resultado:** 469 linhas / 5787 palavras; 2 Mermaid, 4 [!warning], 5 [!question]-. Fontes: PEP 484/585/695, docs.python.org, typing.python.org, Real Python, Fluent Python (Ramalho).

#### 04 - `mypy` e `pyright` — checagem estática na prática
- **Estado:** ✅ feita (2026-07-10) · fase: Adepto
- **Escopo:** instalação e uso via CLI, `strict` mode, tipagem incremental em código legado (`# type: ignore`, `reveal_type`), diferenças mypy vs. pyright (Microsoft, usado pelo Pylance/VS Code), integração em CI (pre-commit, GitHub Actions), o que checagem estática pega que testes não pegam.
- **Resultado:** 401 linhas / 6573 palavras; 1 Mermaid, 6 [!warning], 3 [!question]-. Fontes: docs mypy 2.2, mypy-lang.org, comparação oficial Microsoft mypy-vs-pyright, pre-commit/mirrors-mypy, Real Python, Fluent Python (Ramalho).

#### 05 - `TypedDict`, `Literal`, `NewType` e `Final`
- **Estado:** ✅ feita (2026-07-10) · fase: Adepto
- **Escopo:** `TypedDict` (dicts com schema estático, ponte com JSON/APIs), `Literal` (valores específicos como tipo, ex. `Literal["GET", "POST"]`), `NewType` (tipos distintos sobre o mesmo tipo base, ex. `UserId = NewType("UserId", int)`), `Final`/`ClassVar`.
- **Resultado:** 540 linhas / 6756 palavras; 3 Mermaid, 7 [!warning]. Fontes: PEP 589/655/586/591, typing.python.org, docs.python.org, Real Python, mypy docs, Fluent Python (Ramalho).

#### 06 - Pydantic — validação em runtime
- **Estado:** ✅ feita (2026-07-10) · fase: Adepto
- **Escopo:** `BaseModel`, diferença crucial entre type hints (checados só estaticamente, ignorados em runtime) e validação Pydantic (checada de fato ao instanciar), field validators, serialização/desserialização (`model_dump`/`model_validate`), Pydantic v2 (Rust core, `pydantic-core`) vs. v1, ponte explícita pro Galho 10 (Web e APIs REST, FastAPI usa Pydantic nativamente).
- **Resultado:** 480 linhas / 5415 palavras; 1 Mermaid, 6 [!warning], 2 [!question]-. Fontes: pydantic.dev, docs.pydantic.dev, GitHub pydantic-core, FastAPI docs, Real Python, Fluent Python (Ramalho).

#### 07 - Typing avançado — `overload`, `Self`, `ParamSpec`
- **Estado:** ✅ feita (2026-07-10) · fase: Adepto→Magus
- **Escopo:** `@typing.overload` (múltiplas assinaturas pra uma função), `Self` (PEP 673, retorno do próprio tipo em métodos encadeados/subclasses), `ParamSpec`/`Concatenate` (PEP 612, tipar decorators genéricos — ponte com o Galho 4), variância (covariância/contravariância) em generics, quando a tipagem "custa mais que ajuda".
- **Resultado:** 530 linhas / 6630 palavras; 4 Mermaid, 8 [!warning]. Fontes: PEP 673, PEP 612, docs.python.org (typing.overload), Real Python, Fluent Python (Ramalho).

#### 08 - Capstone — tipagem moderna
- **Estado:** ✅ feita (2026-07-10) · fase: Magus · **FECHA o galho**
- **Escopo:** recapitulação do galho num exemplo único e tipado ponta a ponta (`ApiClient[TModelo]` genérico, validação Pydantic, `TypedDict`/`Literal`/`NewType`/`Final`, builder via `Self`, `Union`+narrowing, `@overload`, retry via `ParamSpec`, `mypy --strict` limpo), ponte pro Galho 6 (CPython internals).
- **Resultado:** 604 linhas / 6160 palavras; 2 Mermaid, 5 [!warning], 25 wikilinks. Fontes: PEPs reaproveitadas das notas irmãs, docs.python.org, pydantic.dev.
