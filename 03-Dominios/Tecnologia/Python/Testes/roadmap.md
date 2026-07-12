---
title: "Roadmap — Python Testes"
created: 2026-07-11
type: meta
publish: false
tags:
  - meta
  - roadmap
  - python
---

# Roadmap — Testes (galho 12)

Roadmap-folha do galho `Python/Testes`. Fase **Adepto** — pytest, fixtures, mocking, coverage, TDD (Percival & Gregory como fonte). Spec: [[00-Meta/specs/2026-07-09-python-trilha-design]]. EXEMPLAR de estrutura: `Python/Segurança/index.md` e `Python/Segurança/roadmap.md` (galho anterior, mesmo padrão).

Roster **não pré-cravado no spec** (só a descrição de alto nível "pytest, fixtures, mocking, coverage, TDD") — desenhado nesta sessão seguindo o mesmo playbook dos Galhos 5, 7, 8, 9, 10 e 11. Quarto galho do bloco **"Backend e arquitetura"** (9-13) — testa o que os Galhos 9-11 construíram.

**Fronteira cravada:** a teoria e estratégia de testes (pirâmide, tipos de teste, test doubles como conceito, flaky tests, mutation testing) já está coberta de forma stack-agnóstica em [[03-Dominios/Engenharia/Testes/index|Engenharia/Testes]] (21 notas conceituais + ferramental Java/JS). Este galho é só o ferramental `pytest` aplicado ao código Python já construído na trilha — nenhuma nota deste galho reexplica pirâmide de testes ou taxonomia de test doubles, só referencia.

## Tabela-resumo

| Métrica | Valor |
|---------|-------|
| Total de notas | 9 |
| ⬜ pendente | 0 |
| ✅ feita | 9 |
| 🔄 em andamento | 0 |
| % concluído | 100% |

---

## Notas

#### 01 - pytest fundamentos — anatomia, discovery e assert introspection
- **Estado:** ✅ feita (2026-07-11) · fase: Adepto
- **Escopo:** por que `pytest` dominou sobre `unittest` (assert nativo do Python com introspecção automática via rewrite de bytecode, vs. `self.assertEqual` verboso), anatomia de um teste (`test_*.py`, função `test_*`, sem herança de classe obrigatória), discovery automático, markers básicos (`@pytest.mark.skip`/`xfail`), rodando com `pytest -v`/`-k`/`-x`. Referencia a pirâmide de testes de Engenharia/Testes sem repetir.
- **Resultado:** 483 linhas / 4567 palavras. Abre com dev vindo de Java/JUnit surpreso com assert rewriting; cobre anatomia mínima, discovery por convenção (diagrama Mermaid), markers, flags de execução, contraste tabelado com `unittest`, exemplo de negócio (desconto progressivo) fechando com `pytest.approx`.

#### 02 - Fixtures — escopos, yield e conftest.py
- **Estado:** ✅ feita (2026-07-11) · fase: Adepto
- **Escopo:** `@pytest.fixture`, injeção por nome de parâmetro (mecanismo de DI do próprio pytest), escopos (`function`/`class`/`module`/`session`) e quando usar cada um, fixtures com `yield` pra setup/teardown (paralelo ao `Depends` com `yield` do Galho 10 nota 04 — mesma ideia, contextos diferentes), `conftest.py` como compartilhamento entre arquivos de teste sem import explícito.
- **Resultado:** 482 linhas / 5949 palavras. Abre com fixture `session` guardando lista mutável causando falha dependente de ordem entre testes; desenvolve mecanismo de injeção por nome, os 4 escopos com regra prática, paralelo `yield` com `Depends()` do Galho 10 (sequenceDiagram), `conftest.py` com herança por diretório.

#### 03 - Parametrização e organização de suíte
- **Estado:** ✅ feita (2026-07-11) · fase: Adepto
- **Escopo:** `@pytest.mark.parametrize` (evita duplicação de teste quase-idêntico variando só o dado de entrada), `ids` customizados pra legibilidade do output, marks customizados registrados em `pytest.ini`/`pyproject.toml`, organização de diretório (`tests/unit`/`tests/integration`, espelhando estrutura do código), fixtures parametrizadas.
- **Resultado:** 465 linhas / 4921 palavras. Abre com 15 testes quase-idênticos de CPF onde um copy-paste deixa um assert invertido passar despercebido; desenvolve `parametrize`/`ids`, marks customizados com `-m "not slow"` (pre-commit vs CI), organização `tests/unit`/`tests/integration`, fixtures parametrizadas.

#### 04 - Mocking com unittest.mock e pytest-mock
- **Estado:** ✅ feita (2026-07-11) · fase: Adepto
- **Escopo:** `Mock`/`MagicMock`/`patch` da biblioteca padrão `unittest.mock`, `pytest-mock` como wrapper mais ergonômico (fixture `mocker`), `patch` como context manager vs decorator vs fixture, `autospec` (por que mock sem spec deixa passar erro de assinatura), quando mockar vs quando NÃO mockar (referencia a filosofia de test doubles de Engenharia/Testes sem repetir a taxonomia completa).
- **Resultado:** 502 linhas / 4377 palavras. Abre com mock sem spec mascarando um refactor que renomeou método, bug só explodindo em produção; desenvolve `Mock`/`MagicMock`, os 3 estilos de `patch`, `spec`/`autospec=True`, regra prática de quando mockar (fronteiras externas) vs não mockar (código interno), exemplo de mock de consulta de CEP externa.

#### 05 - Testando a API REST — TestClient e dependency overrides
- **Estado:** ✅ feita (2026-07-11) · fase: Adepto
- **Escopo:** `TestClient` do FastAPI (Starlette por baixo, faz requisição sem subir servidor real), `app.dependency_overrides` (já mencionado no Galho 10 nota 04 — agora desenvolvido: como trocar `get_current_user`/`get_db` por versões de teste), Django test client/`pytest-django` como equivalente. Teste de um endpoint completo da API de Tarefas (Galho 10) validando status code + shape da resposta.
- **Resultado:** 471 linhas / 6188 palavras. Abre com regressão de Broken Access Control não pega por testes só manuais via Swagger; desenvolve `TestClient` (transport ASGI em processo), `dependency_overrides` trocando `get_db`/`get_current_user`, contraste com `pytest-django`. Teste mais rico: criar tarefa como usuário A, trocar override pra usuário B, validar 404 — regressão automatizada do fix de Broken Access Control do Galho 11.

#### 06 - Testando a camada de persistência — banco de teste e rollback
- **Estado:** ✅ feita (2026-07-11) · fase: Adepto
- **Escopo:** banco de teste isolado (SQLite in-memory como opção rápida mas com ressalva honesta — não é 100% fiel ao Postgres de produção, referencia a nota 06 do Galho 9 sobre isolation levels), Postgres real via `testcontainers-python` como alternativa mais fiel, fixture de sessão com rollback automático entre testes (transação que nunca commita de verdade), factory de dados de teste (menção a `factory_boy` como padrão de mercado).
- **Resultado:** 390 linhas / 5415 palavras. Abre com migração de "recriar schema a cada teste" (lento) pra `scope="session"` sem isolamento (dado órfão vazando entre testes); desenvolve trade-off SQLite vs Postgres real via testcontainers, fixture de rollback com `connection.begin()`/`SAVEPOINT`, `factory_boy` breve.

#### 07 - Coverage — pytest-cov e o que ele não mede
- **Estado:** ✅ feita (2026-07-11) · fase: Adepto
- **Escopo:** `pytest-cov`, `--cov-report`, gate de coverage em CI, e a ressalva honesta central da nota — 100% de coverage de LINHA não significa 100% de coverage de CASO (um `if` testado só no caminho feliz conta como "coberto" mesmo sem testar o `else`) — referencia mutation testing como o próximo degrau (conceito já em Engenharia/Testes, aqui só menção de `mutmut` como ferramenta Python equivalente ao PIT do Java).
- **Resultado:** 376 linhas / 5344 palavras. Abre com fintech "98% coverage" tendo bug de inversão de parâmetros não pego porque o teste só fazia `assert resultado is not None`; desenvolve `pytest-cov` técnico, distinção execução vs correção, `--cov-branch`, 2 diagramas Mermaid (3 degraus de rigor + pipeline). Mutation testing só referenciado (`mutmut`).

#### 08 - TDD na prática com pytest
- **Estado:** ✅ feita (2026-07-11) · fase: Adepto
- **Escopo:** o ciclo red-green-refactor aplicado com `pytest` num caso real pequeno (não reensina a filosofia de TDD, que é conceitual e agnóstica — referencia Engenharia/Testes e cita Percival & Gregory como fonte do rigor "outside-in" usado no livro-fonte da trilha), demonstra o ciclo com um caso de negócio da API de Tarefas (ex: uma regra nova — "não permitir criar tarefa com prazo no passado").
- **Resultado:** 220 linhas / 3312 palavras (aplicação prática deliberadamente mais curta — filosofia já coberta em Engenharia/Testes). Ciclo RED-GREEN-REFACTOR completo com `data_limite` no passado: RED com TestClient, GREEN com `if` solto no handler, REFACTOR movendo pra `@field_validator` sem tocar no teste. Outside-in de Percival & Gregory, reflexão honesta sobre quando TDD compensa vs atrapalha.

#### 09 - Capstone — a suíte de testes da API de Tarefas
- **Estado:** ✅ feita (2026-07-11) · fase: Adepto
- **Escopo:** recapitula o galho construindo a suíte de testes completa pra API de Tarefas blindada na capstone do Galho 11 — testes unitários (lógica pura), testes de integração (`TestClient` + banco de teste), e testes de SEGURANÇA validando os fixes do Galho 11 (teste que confirma que um usuário não acessa tarefa de outro — regressão de Broken Access Control; teste que confirma que o endpoint de busca não é mais vulnerável a SSTI; teste de rate limiting). Cenário prático integrador. Aponta para o Galho 13 (Arquitetura e Design Patterns) como próximo passo — a suíte de testes revela acoplamentos que motivam Repository/Unit of Work formal.
- **Resultado:** 633 linhas / 7097 palavras. Árvore `tests/{unit,integration,security}/` completa amarrando as 8 notas do galho ao código real das capstones dos Galhos 9-11. Núcleo original em `tests/security/`: regressão de Broken Access Control nos 4 verbos HTTP, SSTI provada por asserção negativa (`{{7*7}}` nunca vira "49"), rate limiting estourando 429 na 6ª tentativa — tratados como não-opcionais no CI. 4 diagramas Mermaid, coverage sintético com leitura honesta. Fecha apontando pro Galho 13 (padrões Repository/UoW já aparecendo informalmente na suíte).

> [!success] Galho 12 completo — 9/9 notas (2026-07-11)
> pytest fundamentos (01) → fixtures/escopos (02) → parametrização (03) → mocking (04) → testando a API REST (05) → testando persistência (06) → coverage e seus limites (07) → TDD na prática (08) → capstone com suíte completa (unit + integração + segurança) validando o hardening do Galho 11 (09). Todas as notas referenciam a teoria stack-agnóstica de Engenharia/Testes sem repeti-la — o galho é 100% ferramental `pytest` aplicado ao código real construído nos Galhos 9-11. Próximo da trilha: Galho 13 — Arquitetura e Design Patterns.

## Decisões e fronteiras registradas

- Pirâmide de testes, taxonomia de test doubles, flaky tests, mutation testing como conceito → [[03-Dominios/Engenharia/Testes/index|Engenharia/Testes]]; aqui é só a aplicação `pytest`.
- Filosofia de TDD (red-green-refactor como disciplina, outside-in vs inside-out) → também Engenharia/Testes; a nota 08 aqui só aplica o ciclo com ferramental Python.
- `unittest` legado (classe `TestCase`, `self.assert*`) mencionado só como contraste histórico na nota 01, não desenvolvido a fundo — o ferramental moderno é `pytest`.
- Testes de carga/performance (`locust`) ficam fora do escopo deste galho — são tema de Operação/produção, não de correção funcional.
