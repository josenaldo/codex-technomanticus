---
title: "Plano de Implementação — Trilha Dados (Engenharia de Dados)"
created: 2026-07-12
type: meta
publish: false
tags:
  - meta
  - plan
  - dados
---

# Plano de Implementação — Trilha Dados (Engenharia de Dados)

> **Para o executor:** Plano adaptado ao domínio de *notas do vault* (não código/TDD). A unidade implementável é a **nota** (padrão capítulo de livro, ~440-540 linhas). Executa-se sub-galho a sub-galho via subagente-por-nota (≤3/onda, Sonnet), com `roadmap.md` por pasta como memória de progresso. Fonte de verdade do escopo: [[00-Meta/specs/2026-07-11-dados-engenharia-trilha-design]].

**Goal:** Semear a trilha `Engenharia/Dados/` — 19 notas (4 sub-galhos + capstone), tool-neutral, centro em Analytics/Modern Data Stack.

**Arquitetura de execução:** Ritmo B das trilhas irmãs — scaffold do galho-pai → um sub-galho por vez (index+roadmap+notas) → fechamento por sub-galho (roadmaps + commit) → capstone → wrap-up (callouts nas fronteiras + Roadmap + memória). Subagente escreve a nota; o orquestrador (Opus/opusplan) só coordena, nunca escreve nota direto.

**"Tech stack":** Obsidian Flavored Markdown; skills `escrever-nota` / `verificar-nota`; Mermaid (paleta azul `#4A90D9` / âmbar `#F5A623` / vermelho `#D0021B`); `roadmap.md` recursivo.

## Global Constraints (valem em TODA nota — copiados da spec)

- **Tool-neutral absoluto:** ferramenta (dbt, Airflow, Spark, Iceberg, Snowflake…) é **exemplo citado que ancora o conceito, NUNCA tutorial**. Tutorial de ferramenta vai pra `Tecnologia/`, futuro.
- **Padrão capítulo de livro** ([[feedback_padrao_capitulo_livro]]): TL;DR `[!abstract]`, abertura problema-first, divulgação progressiva, exemplo trabalhado. Substitui o piso de 600; densidade-alvo ~440-540 linhas ([[feedback_notas_profundas_diagramas]]).
- **Fases:** SG1 = `Iniciado`, SG2 = `Adepto`, SG3 = `Adepto→Magus` (01-02 Adepto, 03-05 Magus), SG4 + capstone = `Magus`. `fase:` no frontmatter.
- **≥1 Mermaid por nota**, paleta fixa. Star schema → ER; pipeline → flowchart/DAG; ciclo de vida → grafo.
- **Seções fixas:** "Em entrevista", "How to explain in English" (tabela PT↔EN), "O que vem a seguir", `## Fontes` datadas.
- **`[!info]` de caducidade** em toda nota com ferramenta/versão viva (Iceberg/Delta/Hudi, dbt/Fusion/Fivetran, DuckDB/DuckLake). WebSearch inline nessas notas.
- **Anti-duplicação:** não reexplicar BD 02-14 (relacional/distribuído), Comunicação (mensageria), Operação (observabilidade), Segurança (PII) — **linkar**. Ver tabela de fronteiras na spec.
- **Domínio-fio do exemplo trabalhado:** e-commerce recorrente (vendas → star schema → ELT → contrato → catálogo), pra dar continuidade de capítulo.
- **Git:** stage paths explícitos + `git diff --cached` antes de commitar ([[feedback_git_commit_hygiene]]); sem Co-Authored-By ([[feedback_commits]]); push manual.
- **Nunca fabricar** experiência/cliente do usuário ([[feedback_no_fabrication]]).
- **Nunca remover `index.md`** (quebra Quartz — [[feedback_quartz_index]]).

---

## Task 0 — Scaffold do galho-pai

**Arquivos:**
- Modificar: `03-Dominios/Engenharia/Dados/index.md` (reescrever MOC: os 4 sub-galhos + capstone, TL;DR, fronteiras com BD/Comunicação/Operação)
- Criar: `03-Dominios/Engenharia/Dados/roadmap.md` (roadmap recursivo do galho-pai — modo galho-pai: mapa de estado dos 4 sub-galhos, cada um `⬜ a semear`)

**Passos:**
- [ ] Reescrever `index.md` com a estrutura da trilha (usar `## Conteúdo` linkando os 4 sub-galhos por `index.md` de cada pasta; TL;DR já bom, ajustar; manter "Veja também" com BD/Comunicação)
- [ ] Criar `roadmap.md` do galho-pai a partir do `Template - Roadmap` (modo pai): tabela dos 4 sub-galhos + capstone com estado/nota-count/plano
- [ ] Commit: `git add 03-Dominios/Engenharia/Dados/index.md 03-Dominios/Engenharia/Dados/roadmap.md && git commit -m "feat(dados): scaffold do galho-pai (index + roadmap)"`

**Deliverable testável:** `index.md` renderiza no Quartz com 4 links de sub-galho (que ainda 404 até Task 1-4); `roadmap.md` lista os 4 sub-galhos.

---

## Task 1 — Sub-galho 1: Fundamentos de engenharia de dados (Iniciado, 4 notas)

**Pasta:** `03-Dominios/Engenharia/Dados/1 - Fundamentos de engenharia de dados/`

**Notas (roster da spec):**
1. `01 - O que é engenharia de dados.md` — OLTP vs OLAP; por que o banco transacional não basta; DE vs analytics engineer vs data scientist. Link BD 01/05.
2. `02 - O ciclo de vida da engenharia de dados.md` — geração→ingestão→armazenamento→transformação→serving; undercurrents (Reis/Housley). Mapa da trilha. **Mermaid: grafo do ciclo.**
3. `03 - Warehouse, lake e lakehouse.md` — os 3 paradigmas; história Inmon→Hadoop→cloud DW→lakehouse; data swamp; storage/compute.
4. `04 - Armazenamento colunar e formatos.md` — row vs colunar; Parquet/ORC/Avro; compressão/encoding; open table formats (Iceberg default 2026, Delta, Hudi; UniForm/XTable; DuckLake/Paimon citação). **`[!info]` caducidade + WebSearch inline.** Link BD 07.

**Passos:**
- [ ] Criar `index.md` do sub-galho (MOC das 4 notas, fase Iniciado) + `roadmap.md` (modo folha: 1 linha por nota, estado `⬜`)
- [ ] Escrever nota 01 via subagente (`escrever-nota`); esta é a **nota-exemplar de arranque** — usar a nota 01 de uma trilha irmã (ex.: System Design/Comunicação) como referência de forma até a 01 daqui virar exemplar próprio da trilha
- [ ] Escrever notas 02-04 via subagente-por-nota (≤3/onda; WebSearch inline na 04); barra de densidade explícita ~440-540 linhas
- [ ] Rodar `verificar-nota` em cada uma; corrigir gaps estruturais
- [ ] Atualizar `roadmap.md` (folha) → notas `✅`; atualizar `roadmap.md` (pai) → SG1 `✅`
- [ ] Commit: `git add` (paths explícitos da pasta SG1 + 2 roadmaps) `&& git commit -m "feat(dados): Galho 1 Fundamentos de engenharia de dados (4/4)"`

**Deliverable testável:** 4 notas renderizam, cada uma com TL;DR + ≥1 Mermaid + seções fixas; `verificar-nota` passa; links pra BD resolvem.

---

## Task 2 — Sub-galho 2: Modelagem para analytics (Adepto, 5 notas)

**Pasta:** `03-Dominios/Engenharia/Dados/2 - Modelagem para analytics/`

**Notas:**
1. `01 - Por que modelar pra analytics.md` — do relacional normalizado (link BD 04) ao dimensional; cubo OLAP; denormalização deliberada.
2. `02 - Modelagem dimensional.md` — fatos/dimensões, **grão**, star schema, aditividade; Kimball. **Exemplo trabalhado: vendas do e-commerce. Mermaid: ER do star.**
3. `03 - Star vs snowflake e tipos de fato.md` — star vs snowflake; transaction/periodic/accumulating snapshot; dimensões conformadas, bus matrix; degenerate/junk/role-playing.
4. `04 - Slowly Changing Dimensions.md` — SCD 0-6 (foco 1/2/3), surrogate keys, late-arriving.
5. `05 - Além de Kimball.md` — Inmon vs Kimball vs Data Vault; One Big Table/wide tables; medallion (bronze/silver/gold); quando fugir do star.

**Passos:**
- [ ] Criar `index.md` (fase Adepto) + `roadmap.md` (folha) do SG2
- [ ] Escrever notas 01-05 via subagente-por-nota (≤3/onda → 2 ondas: 01-03, 04-05); exemplo-fio e-commerce na 02+
- [ ] `verificar-nota` em cada; corrigir
- [ ] Atualizar roadmaps (folha + pai → SG2 `✅`)
- [ ] Commit: paths explícitos SG2 + roadmaps, `-m "feat(dados): Galho 2 Modelagem para analytics (5/5)"`

**Deliverable testável:** 5 notas; a 02 tem ER Mermaid do star schema de vendas; SCD explicado com exemplo; `verificar-nota` passa.

---

## Task 3 — Sub-galho 3: Pipelines — movimentação e transformação (Adepto→Magus, 5 notas)

**Pasta:** `03-Dominios/Engenharia/Dados/3 - Pipelines - movimentação e transformação/`

**Notas:**
1. `01 - ETL vs ELT.md` — virada cloud; storage/compute; onde ETL ainda vale; pipeline como grafo. **fase Adepto.**
2. `02 - Ingestão de dados.md` — extract; batch vs incremental; **CDC** (log vs query-based); idempotência; EL tools (Fivetran/Airbyte/dlt citação). Link BD 12. **fase Adepto. `[!info]` caducidade.**
3. `03 - Transformação SQL-first.md` — analytics engineering (dbt table-stakes; Fusion/Rust; SQLMesh); modularidade/testes/lineage como código; semantic layer. **fase Magus. `[!info]` + WebSearch inline.**
4. `04 - Orquestração.md` — DAG; dependências; idempotência/backfill; scheduling vs event-driven; orquestrador como sistema (Airflow/Dagster/Prefect citação); data assets vs tasks. Link Operação. **fase Magus. Mermaid: DAG.**
5. `05 - Dados em movimento.md` — batch vs streaming; lambda vs kappa; micro-batch; janelas/late data; quando streaming vale. **Fronteira → Comunicação (mensageria)/BD 14. fase Magus.**

**Passos:**
- [ ] Criar `index.md` (fase Adepto→Magus) + `roadmap.md` (folha) do SG3
- [ ] Escrever notas 01-05 via subagente-por-nota (2 ondas: 01-03, 04-05); WebSearch inline na 02/03; **callout de fronteira explícito na 05** (link Comunicação, não reexplicar Kafka)
- [ ] `verificar-nota` em cada; corrigir
- [ ] Atualizar roadmaps (folha + pai → SG3 `✅`)
- [ ] Commit: paths explícitos SG3 + roadmaps, `-m "feat(dados): Galho 3 Pipelines - movimentação e transformação (5/5)"`

**Deliverable testável:** 5 notas; a 04 tem Mermaid de DAG; a 05 linka Comunicação em vez de reexplicar mensageria; fases corretas no frontmatter.

---

## Task 4 — Sub-galho 4: Qualidade, governança e organização (Magus, 4 notas)

**Pasta:** `03-Dominios/Engenharia/Dados/4 - Qualidade, governança e organização/`

**Notas:**
1. `01 - Qualidade e observabilidade de dados.md` — dimensões de qualidade; testes de dados; **5 pilares de data observability** (freshness/volume/schema/quality/lineage); anomalias; SLA de dados. Link Operação.
2. `02 - Data contracts e schema evolution.md` — contrato produtor↔consumidor; shift-left; compat back/forward; silent breakage; primitivos de contrato nos warehouses 2026. Link Comunicação. **`[!info]` caducidade.**
3. `03 - Governança, catálogo e lineage.md` — metadata; data catalog; lineage end-to-end; PII/LGPD/GDPR; classificação/mascaramento; data as a product. Link Segurança.
4. `04 - Arquiteturas organizacionais.md` — warehouse centralizado vs **data mesh** (domínios/produto/self-service/governança federada) vs data fabric; Conway; mesh hype vs necessidade. Link System Design. **fecha o corpo.**

**Passos:**
- [ ] Criar `index.md` (fase Magus) + `roadmap.md` (folha) do SG4
- [ ] Escrever notas 01-04 via subagente-por-nota (2 ondas: 01-03, 04); WebSearch inline na 01/02
- [ ] `verificar-nota` em cada; corrigir
- [ ] Atualizar roadmaps (folha + pai → SG4 `✅`)
- [ ] Commit: paths explícitos SG4 + roadmaps, `-m "feat(dados): Galho 4 Qualidade, governança e organização (4/4)"`

**Deliverable testável:** 4 notas; observabilidade cobre os 5 pilares; mesh vs central com trade-off de Conway; links pra Operação/Segurança/System Design resolvem.

---

## Task 5 — Capstone + wrap-up

**Arquivos:**
- Criar: `03-Dominios/Engenharia/Dados/Capstone - Desenhando a plataforma de dados de uma empresa do zero.md` (fase Magus, galho-pai)
- Modificar: notas-fronteira (callouts) + `00-Meta/Roadmap` + memória

**Passos:**
- [ ] Escrever o capstone via subagente: walkthrough decisório costurando os 4 SGs (armazenamento, modelagem, ELT+orquestrador, streaming onde vale, contratos+qualidade, centralizado vs mesh); cenários startup vs enterprise; e-commerce como fio; **nunca fabricar experiência do usuário**
- [ ] `verificar-nota` no capstone
- [ ] Adicionar callouts apontando pra cá nas fronteiras: BD 12-14, Comunicação (streaming/contratos/schema registry), Operação (observabilidade), Segurança (PII) — paths explícitos, um callout por nota-alvo
- [ ] Atualizar `roadmap.md` do galho-pai → tudo `✅`, trilha COMPLETA
- [ ] Atualizar [[00-Meta/Roadmap]]: Dados `seedling → 🟢`
- [ ] Atualizar memória: criar `memory/project_trilha_dados.md` + linha em `MEMORY.md`
- [ ] Commit final: paths explícitos (capstone + notas-fronteira editadas + Roadmap), `-m "docs(dados): capstone + rollup da trilha Dados — trilha COMPLETA (19/19)"`

**Deliverable testável:** capstone renderiza e referencia os 4 SGs; callouts de fronteira resolvem nos dois sentidos; Roadmap marca Dados 🟢; `git status` limpo na pasta Dados.

---

## Self-Review (cobertura da spec)

- ✅ SG1-4 + capstone = 19 notas, todas com task e roster nominal.
- ✅ Tool-neutral, fases, Mermaid, seções fixas, caducidade, anti-duplicação, e-commerce-fio: em Global Constraints (herdadas por toda task).
- ✅ Fronteiras (BD/Comunicação/Operação/Segurança/System Design) → callouts na Task 5 + links por nota.
- ✅ Execução ritmo B (scaffold→SG→fechamento→capstone→wrap-up) = seção "Plano de execução" da spec.
- ✅ Pontos em aberto da spec (e-commerce-fio, DuckLake citação leve, broto se SG2-05 crescer) → refletidos nas notas correspondentes.
- Sem placeholders de conteúdo: cada nota tem escopo nominal; o conteúdo real é gerado pela `escrever-nota` (que é o "como" desta camada).
