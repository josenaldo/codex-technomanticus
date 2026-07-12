---
title: "Roadmap — Python Build e tooling"
created: 2026-07-12
type: meta
publish: false
tags:
  - meta
  - roadmap
  - python
---

# Roadmap — Build e tooling (galho 16)

Roadmap-folha do galho `Python/Build e tooling`. Fase **Iniciado→Adepto** — packaging moderno (uv, poetry), virtual envs, pyproject.toml, ruff/black. Spec: [[00-Meta/specs/2026-07-09-python-trilha-design]]. EXEMPLAR de estrutura: `Python/Microservices e sistemas distribuídos/index.md` e `roadmap.md` (galho anterior, mesmo padrão).

**Fronteira cravada:** segurança de dependências (`pip-audit`, lockfiles como defesa) já em [[03-Dominios/Tecnologia/Python/Segurança/07 - Segurança de dependências e supply chain|Galho 11 nota 07]] — aqui lockfiles são tratados pela lente de REPRODUTIBILIDADE, não segurança. Java/Build e tooling (20 notas, Maven/Gradle) é o exemplar de aplicação numa stack — este galho mantém a escala já estabelecida (8 notas), porque o spec Python é mais estreito.

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

#### 01 - Panorama — por que packaging Python era confuso
- **Estado:** ✅ feita (2026-07-12) · fase: Iniciado
- **Resultado:** 247 linhas / 3195 palavras (nota-mapa mais leve). Abre com dev novo achando 6 arquivos de config sem fonte de verdade; percorre `setup.py`/`setup.cfg`/`requirements.txt`/`Pipfile`, PEP 518/621 como solução, contraste breve com Maven/Gradle.
- **Escopo:** história rápida e honesta do caos histórico — `setup.py`, `setup.cfg`, `requirements.txt`, `Pipfile`, cada ferramenta resolvendo um pedaço do problema sem um padrão unificado, contraste com Maven/Gradle da trilha Java (referenciando [[03-Dominios/Tecnologia/Java/Build e tooling/index|Java — Build e tooling]] sem repetir). Mapa do galho.

#### 02 - Virtual environments — isolamento de dependências
- **Estado:** ✅ feita (2026-07-12) · fase: Iniciado
- **Resultado:** 249 linhas / 3322 palavras. Abre com `sudo pip install` global quebrando o `apt` do Ubuntu (incidente real documentado); `venv` nativo, PEP 668 (`externally-managed-environment`), `.gitignore` do `.venv/`, alternativas históricas (`virtualenv`/`conda`) mencionadas brevemente.
- **Escopo:** `venv` nativo do Python, por que isolar dependências por projeto é essencial (evitar conflito de versão entre projetos diferentes na mesma máquina), ativação/desativação, `.gitignore` do `venv/`.

#### 03 - pyproject.toml — o padrão unificado
- **Estado:** ✅ feita (2026-07-12) · fase: Iniciado
- **Resultado:** 275 linhas / 2683 palavras. PEP 518 (`[build-system]`) e PEP 621 (`[project]`); namespace `[tool.*]` compartilhado; `pyproject.toml` real e completo do serviço de Tarefas com 4 seções `[tool.*]` (ruff, pytest, mypy, coverage).
- **Escopo:** PEP 518/621, `pyproject.toml` substituindo `setup.py`/`setup.cfg`/`requirements.txt` como fonte única de verdade — seção `[project]` (metadados, dependências), `[build-system]`, `[tool.*]` (configuração de ruff/black/pytest, todas no mesmo arquivo).

#### 04 - uv — o gerenciador moderno
- **Estado:** ✅ feita (2026-07-12) · fase: Adepto
- **Resultado:** 306 linhas / 3760 palavras. Abre com CI caindo de 4min pra 8s migrando de pip pra uv; `uv venv`/`uv add`/`uv lock`/`uv sync`/`uv run`, `uv python install`/`pin` pra versão do interpretador.
- **Escopo:** `uv` (Astral, escrito em Rust) como gerenciador de projeto completo — `uv venv`, `uv add`/`uv remove`, `uv sync`, `uv lock` (lockfile determinístico), `uv run`. Por que a velocidade importa em CI (resolução de dependências que levava minutos em segundos).

#### 05 - Poetry — a alternativa madura
- **Estado:** ✅ feita (2026-07-12) · fase: Adepto
- **Resultado:** 338 linhas / 3341 palavras. Abre com time em Poetry desde 2019, sem motivo forte pra migrar; `[tool.poetry]`/PEP 621 nativo desde 2.0, groups de dependências, `poetry build`/`poetry publish` maduro.
- **Escopo:** Poetry como alternativa mais estabelecida (pré-uv), `pyproject.toml` com seção `[tool.poetry]`, `poetry add`/`poetry install`/`poetry.lock`, `poetry build`/`poetry publish` (publicar pacote no PyPI).

#### 06 - uv vs Poetry — trade-offs honestos
- **Estado:** ✅ feita (2026-07-12) · fase: Adepto
- **Resultado:** 185 linhas / 3499 palavras. Tabela de 6 eixos (velocidade, maturidade, escopo/interpretador, lockfile incompatível, publicação, plugins); critério honesto: uv padrão pra projeto novo, Poetry mantido sem dor de performance mensurável.
- **Escopo:** comparação direta — velocidade (uv ganha por ordem de magnitude), maturidade/ecossistema (Poetry mais estabelecido, mais anos em produção), compatibilidade de lockfile, quando cada um é a escolha certa em 2026.

#### 07 - ruff e black — linting e formatação automática
- **Estado:** ✅ feita (2026-07-12) · fase: Adepto
- **Resultado:** 341 linhas / 4240 palavras. Abre com PR travado 3 dias em discussão de estilo; ruff consolidando flake8+isort+pylint+bandit, black opinativo, `ruff format` vs black separado, `pre-commit` reusando conceito do Galho 11.
- **Escopo:** `ruff` (linter ultra-rápido, substituindo flake8+isort+pylint+bandit numa ferramenta só), `black` (formatação automática opinativa, "sem debate de estilo"), integração via `pre-commit` hooks (rodando antes de cada commit, referenciando o conceito de secret scanning como pre-commit hook já visto no Galho 11 nota 06 sem repetir).

#### 08 - Capstone — tooling consistente nos dois serviços
- **Estado:** ✅ feita (2026-07-12) · fase: Adepto
- **Escopo:** recapitula o galho aplicando `uv`+`pyproject.toml`+`ruff`+`black`+`pre-commit` de forma CONSISTENTE aos dois serviços Python construídos no Galho 15 (Tarefas e Notificações) — mesma versão de Python, mesmas regras de lint, lockfiles próprios por serviço (não um workspace monorepo compartilhado, decisão explícita e justificada). Cenário prático integrador. Aponta para o Galho 17 (Observabilidade e produção) como próximo passo.
- **Resultado:** 437 linhas / 5782 palavras. 7 peças amarrando as 7 notas anteriores nos dois serviços reais: venv isolado, `pyproject.toml` mesma estrutura, `uv` escolhido por consistência (não superioridade abstrata), `ruff`/`ruff format` mesma config, `uv python pin 3.12` explícito, repos separados (não workspace) reforçando a independência de deploy do Galho 15, `.pre-commit-config.yaml` compartilhado.

> [!success] Galho 16 completo — 8/8 notas (2026-07-12)
> Panorama do caos histórico (01) → venv (02) → pyproject.toml unificado (03) → uv (04) → Poetry (05) → uv vs Poetry honesto (06) → ruff/black (07) → capstone com decisões explícitas de consistência entre os dois serviços do Galho 15 (08). Segurança de dependências nunca repetida — sempre referenciada ao Galho 11 nota 07. Próximo da trilha: Galho 17 — Observabilidade e produção.

## Decisões e fronteiras registradas

- Segurança de dependências (`pip-audit`, lockfile como defesa contra supply chain) → Galho 11 nota 07; aqui lockfile é reprodutibilidade de build, não segurança.
- Maven/Gradle → Java/Build e tooling; referenciado pra contraste no panorama.
- CI/CD como pipeline → Engenharia/Operação, fora do escopo detalhado deste galho.
- Publicação de pacote privado/registry interno → fora do escopo (é infra, mencionado brevemente na nota 05 se relevante).
