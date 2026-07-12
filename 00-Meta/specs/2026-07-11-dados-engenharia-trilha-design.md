---
title: "Design Spec — Trilha Dados (Engenharia de Dados)"
created: 2026-07-11
type: meta
publish: false
tags:
  - meta
  - spec
  - dados
---

# Design Spec — Trilha Dados (Engenharia de Dados)

> Domínio `Engenharia/Dados/` — só o `index.md` existe (esqueleto Batch 5). Última trilha de Engenharia a semear: as outras 9 disciplinas do domínio estão fechadas (Arquitetura, Comunicação, Auth, Operação, Arqueologia, Design, Segurança, Complexidade, Testes). Quinta trilha da família Engenharia pós-System Design: **System Design** (desenha) → **Operação** (opera) → **Comunicação** (contrata) → **Auth e Identidade** (quem pode o quê) → **Dados** (como construir sistemas de dados em escala).

## Ponto de vista (pedido do usuário 2026-07-11)

Trilha **tool-neutral**, modelo Comunicação entre Sistemas (que proibiu tutorial por stack) — e **não** o modelo Auth (que abriu exceção pra sub-galhos de implementação). Ferramentas (dbt, Airflow, Spark, Kafka, Snowflake/BigQuery, Iceberg/Delta) entram como **exemplos citados** que ancoram o conceito, nunca como tutorial. Trilhas específicas de ferramenta, quando necessárias, vão pra `Tecnologia/` depois (decisão do usuário; ele pretende dividir o Auth de forma análoga no futuro).

**Público-alvo / lente:** o **sênior fullstack que precisa decidir e conversar** sobre sistemas de dados — montar/avaliar uma plataforma de dados analíticos, falar a língua do campo em entrevista e em sala de arquitetura — **não** virar data engineer. Literacia sênior, não formação de especialista.

**Centro de gravidade (decisão do usuário):** **Analytics / Modern Data Stack** (mundo Kimball/dbt): modelagem dimensional, warehouse vs lake vs lakehouse, ELT, orquestração, qualidade/contratos, formatos colunares. O polo **Data-Intensive Systems** (mundo Kleppmann/DDIA — replicação, partitioning, transações distribuídas, NoSQL) **já mora em Ciência/Banco de Dados 12-14** e não é reexplicado. Streaming/processamento distribuído aparece como **um** galho de fronteira ("dados em movimento") que linka pra BD/Comunicação.

## Pesquisa web (2026-07-11) — estado do tema

- **Open table formats:** **Apache Iceberg é o default de lakehouse aberto novo em 2026** — governança vendor-neutral, partition evolution + hidden partitioning, suporte multi-engine mais amplo (Spark, Flink, Trino, Snowflake, BigQuery, DuckDB), spec v3 madura. **Delta Lake** é best-in-class dentro de Databricks/Microsoft Fabric (Liquid Clustering, UniForm), ~60% da Fortune 500 via Databricks. **Apache Hudi** vence em streaming upserts/CDC (record-level indexing, delta logs por coluna, menos write amplification). **O mercado NÃO consolidou num vencedor** — cada formato reforça sua vantagem de origem; **UniForm + Apache XTable** tornam a escolha não-permanente (escreva um, exponha os outros). Emergentes: **Paimon** (streaming-first) e **DuckLake** (metadata em SQL DB em vez de arquivos).
- **dbt virou table stakes:** se você tem warehouse + time de analytics, você usa dbt ou migra pra ele. **dbt Fusion** = novo engine em Rust (perf + DX sobre o dbt Core). **Consolidação de ecossistema:** Fivetran comprou Census (mai/2025), Tobiko Data/**SQLMesh** (set/2025) e **dbt Labs (out/2025)** — controle sobre a principal ferramenta de transformação SQL open-source + plataforma EL.
- **DuckDB "está comendo o modern data stack":** compute vai até o dado (notebooks, CI, serviços pequenos, laptops de analista) em vez de tudo ir pra um serviço central gigante. **DuckLake** = formato lakehouse que usa banco SQL padrão pra metadata (ACID sobre data lake, mais simples). "3D stack" = **dlt → duckdb → dbt**.
- **Data contracts + observabilidade viraram práticas fundamentais:** contrato define formato/qualidade/schema esperados entre partes do pipeline. Em 2026 os grandes warehouses (Snowflake, BigQuery, Databricks) **embutiram primitivos de contrato** nos planos enterprise — de projeto de engenharia virou feature de plataforma.
- **Semantic layer** deixou de ser debate (2023) e virou **pré-requisito** de projeto de BI que funciona em 2026.
- **ELT venceu ETL** no mundo cloud pela separação storage/compute (transformar no warehouse é barato e elástico). CDC (change data capture) é o padrão de ingestão incremental.
- **Clássicos estáveis (não caducam):** *The Data Warehouse Toolkit* (Kimball/Ross) pra modelagem dimensional; *Fundamentals of Data Engineering* (Reis/Housley) pro ciclo de vida + undercurrents; *Designing Data-Intensive Applications* (Kleppmann) pro lado distribuído (mas esse mora em BD/Arquitetura).

## Contexto: o que já existe (fronteiras!)

- `Ciência/Banco de Dados/` (16 notas) — **a teoria relacional inteira**: modelo relacional (02), SQL (03/09), modelagem e normalização (04), ACID/transações (05), isolamento/anomalias (06), índices (07), EXPLAIN/otimização (08), performance (10), concorrência/locking (11), **replicação/sharding/CAP (12)**, **transações distribuídas (13)**, **NoSQL/polyglot (14)**, operação em produção (15). **Regra:** o lado OLTP/relacional/distribuído-de-dados mora lá; aqui é o lado **OLAP/analytics/pipeline**. Notas 12-14 cobrem o polo DDIA — não reexplicar; linkar.
- `Comunicação entre Sistemas/` — mensageria, eventos, Kafka, contratos de API, schema registry. **Streaming e o "produtor de eventos" moram lá**; o SG3-05 (dados em movimento) linka pra cá e cobre só o ângulo *analytics* (lambda/kappa, batch vs stream pra pipeline de dados). Data contracts (SG4-02) linka pra contratos/schema evolution de lá.
- `Operação/` — observabilidade, SRE, deploy, incidentes. **Data observability (SG4-01) e orquestração (SG3-04) linkam** — a disciplina de operar sistemas mora lá; aqui é o recorte de dados.
- `Segurança/` — PII, LGPD/GDPR, mascaramento tocam governança (SG4-03) — linkar princípios, cobrir só o ângulo de dados.
- `Arquitetura/` (System Design) — arquiteturas distribuídas e trade-offs macro; data mesh (SG4-04) dialoga com organização de sistemas mas é recorte de dados.
- `Ciência/` (Fundamentos) — teoria da computação/complexidade; não toca.

## Onde mora

`03-Dominios/Engenharia/Dados/` — domínio já criado (só `index.md`), irmão de Comunicação e Auth. Engenharia de dados é disciplina neutra de ferramenta (o *como construir sistemas de dados*); a implementação concreta em cada ferramenta é `Tecnologia/`, futura.

## Estrutura de pastas

```
Engenharia/Dados/
├── index.md                                     (MOC do galho-pai — já existe, reescrever)
├── roadmap.md                                   (roadmap recursivo, novo)
├── 1 - Fundamentos de engenharia de dados/      (Iniciado)
├── 2 - Modelagem para analytics/                (Adepto)
├── 3 - Pipelines - movimentação e transformação/ (Adepto→Magus)
└── 4 - Qualidade, governança e organização/     (Magus)
+ capstone no galho-pai (Magus)
```

## Roster de notas

### Sub-galho 1 — Fundamentos de engenharia de dados (Iniciado, 4 notas)

> O vocabulário e o mapa: o que é a disciplina, o ciclo de vida, onde os dados vivem, em que formato.

| # | Nota | Escopo | Fronteira / cross-link |
|---|------|--------|------------------------|
| 01 | O que é engenharia de dados | OLTP vs OLAP (a divisão fundadora); por que o banco transacional não basta pra analytics (contenção, modelo errado, escala de leitura); data engineer vs analytics engineer vs data scientist vs analista; a disciplina como *ponte entre dados brutos e valor*. | linka BD 01/05 (OLTP); enquadra a trilha |
| 02 | O ciclo de vida da engenharia de dados | Geração → ingestão → armazenamento → transformação → serving; as *undercurrents* de Reis/Housley (segurança, gestão de dados, DataOps, arquitetura, orquestração) que atravessam tudo; onde cada sub-galho da trilha se encaixa no ciclo. | mapa da trilha inteira |
| 03 | Warehouse, lake e lakehouse | Os três paradigmas de armazenamento analítico; história (Inmon/data warehouse → Hadoop/data lake → cloud DW Snowflake/BigQuery → lakehouse); o pântano de dados (data swamp); separação storage/compute; quando cada um faz sentido. | — |
| 04 | Armazenamento colunar e formatos de arquivo | Row-oriented vs columnar e por que analytics quer coluna; Parquet/ORC/Avro; compressão e encoding (RLE, dictionary); particionamento e file layout; **open table formats** (Iceberg default 2026, Delta, Hudi; UniForm/XTable; DuckLake/Paimon como citação) — o que um "formato de tabela" resolve sobre um monte de Parquet. | linka BD 07 (índices — analogia); `[!info]` caducidade |

### Sub-galho 2 — Modelagem para analytics (Adepto, 5 notas)

> O coração da trilha: modelagem dimensional. Por que o schema normalizado do OLTP é errado pra analytics.

| # | Nota | Escopo | Fronteira / cross-link |
|---|------|--------|------------------------|
| 01 | Por que modelar pra analytics | Do relacional normalizado (3NF, linka BD 04) ao dimensional; o cubo OLAP (slice/dice/drill/roll-up); a mudança de mentalidade (otimizar leitura e compreensão humana, não escrita); denormalização deliberada. | aprofunda BD 04 |
| 02 | Modelagem dimensional | Fatos e dimensões; o **grão** (a decisão mais importante); star schema; medidas e aditividade (aditiva/semi/não-aditiva); Kimball como cânone. | núcleo do SG; exemplo trabalhado (vendas) |
| 03 | Star vs snowflake e tipos de fato | Star vs snowflake (trade-off leitura/manutenção); tipos de tabela-fato (transaction / periodic snapshot / accumulating snapshot); dimensões conformadas e a **bus matrix**; degenerate/junk/role-playing dimensions. | — |
| 04 | Slowly Changing Dimensions | O problema da dimensão que muda no tempo; SCD tipos 0-6 (foco 1/2/3), surrogate keys vs natural keys, late-arriving dimensions/facts; efeito no histórico dos relatórios. | — |
| 05 | Além de Kimball | Inmon (top-down) vs Kimball (bottom-up) vs **Data Vault** (auditabilidade/escala); **One Big Table / wide tables** (a era colunar barateou a denormalização total); **medallion architecture** (bronze/silver/gold) no lakehouse; quando fugir do star. | fecha SG2 |

### Sub-galho 3 — Pipelines: movimentação e transformação (Adepto→Magus, 5 notas)

> Como os dados chegam, se transformam e correm. ELT, ingestão, orquestração, e a fronteira do streaming.

| # | Nota | Escopo | Fronteira / cross-link |
|---|------|--------|------------------------|
| 01 | ETL vs ELT | A virada cloud: por que ELT venceu (storage/compute separados, transformar no warehouse é barato e elástico); onde ETL ainda faz sentido (compliance/PII antes do load); o pipeline como grafo. | — |
| 02 | Ingestão de dados | O "E" (extract) e por que é a parte mais chata; batch vs incremental; **CDC (change data capture)** — log-based vs query-based; full vs incremental extract; idempotência da ingestão; ferramentas de EL (Fivetran/Airbyte/dlt como citação). | linka BD 12 (replicação — log é a mesma ideia) |
| 03 | Transformação SQL-first | O paradigma **analytics engineering** (dbt-style, agora table stakes; dbt Fusion/Rust; SQLMesh): modularidade, DRY via refs, testes de dados, documentação e **lineage** como código; o semantic layer como pré-requisito 2026. | `[!info]` caducidade (dbt/Fivetran) |
| 04 | Orquestração | O pipeline como **DAG**; dependências e ordem; idempotência e **backfill**; scheduling (cron/intervalo) vs event-driven; retries e alerta; o orquestrador como sistema (Airflow/Dagster/Prefect como citação); data assets vs tasks. | linka Operação (rodar em prod) |
| 05 | Dados em movimento | Batch vs streaming pra pipeline de dados; **lambda vs kappa**; micro-batch; janelas e late data; quando streaming vale o custo (a maioria dos casos ainda é batch). **Fronteira:** o *como* da mensageria/Kafka mora em Comunicação; aqui é a decisão analytics. | **fronteira** → Comunicação (mensageria), BD 14 |

### Sub-galho 4 — Qualidade, governança e organização (Magus, 4 notas)

> O que separa um pipeline de brinquedo de uma plataforma de dados confiável. E o lado sociotécnico.

| # | Nota | Escopo | Fronteira / cross-link |
|---|------|--------|------------------------|
| 01 | Qualidade e observabilidade de dados | Dimensões de qualidade (frescor/completude/acurácia/unicidade/consistência); testes de dados (schema, not-null, unique, referential, custom); **data observability** (os 5 pilares: freshness/volume/schema/quality/lineage); detecção de anomalias; SLA de dados. | linka Operação (observabilidade) |
| 02 | Data contracts e schema evolution | Contrato produtor↔consumidor; **shift-left** (validar na fonte); versionamento e compatibilidade (back/forward); *silent breakage* (a coluna que sumiu); primitivos de contrato embutidos nos warehouses 2026. | linka Comunicação (schema registry/contratos) |
| 03 | Governança, catálogo e lineage | Metadata e o **data catalog** (discovery, ownership); data lineage end-to-end; **PII, LGPD/GDPR**, classificação e mascaramento; access control e o mínimo privilégio sobre dados; data as a product. | linka Segurança |
| 04 | Arquiteturas organizacionais | Warehouse **centralizado** vs **data mesh** (domínios donos dos dados, dados como produto, plataforma self-service, governança federada) vs data fabric; o trade-off de Conway; quando mesh é hype vs necessidade; times e ownership. | fecha o corpo; linka System Design |

### Capstone (Magus, galho-pai)

**"Desenhando a plataforma de dados de uma empresa do zero"** — walkthrough decisório costurando os 4 sub-galhos: qual armazenamento (warehouse vs lakehouse; Iceberg vs gerenciado), como modelar (dimensional vs wide table vs medallion), ELT + orquestrador, onde streaming vale, contratos + qualidade + observabilidade, centralizado vs mesh conforme o tamanho do time. Aterrissa em cenários de decisão (startup enxuta vs enterprise). Nunca fabricar experiência do usuário ([[feedback_no_fabrication]]).

**Total planejado:** 4+5+5+4 = 18 notas + 1 capstone = **19 notas**.

## Fronteiras anti-duplicação

| Tópico | Papel aqui | Mora em | Regra |
|--------|-----------|---------|-------|
| Modelo relacional, SQL, normalização, ACID, índices | base — ponto de partida | BD (Ciência) 02-11 | linkar; SG2-01 parte da normalização |
| Replicação, sharding, CAP, txn distribuída, NoSQL | o polo DDIA/distribuído | BD 12-14 | linkar; NÃO reexplicar |
| Mensageria, Kafka, eventos, schema registry | o *como* de streaming e contratos | Comunicação entre Sistemas | SG3-05 e SG4-02 são recorte analytics + link |
| Observabilidade, SRE, deploy, incidentes | disciplina de operação | Operação | SG3-04/SG4-01 linkam |
| PII, LGPD, mascaramento, access control (princípios) | uso, não teoria | Segurança | SG4-03 cobre só o ângulo de dados |
| Data mesh como organização de sistemas | recorte de dados | System Design (Conway/distribuídos) | SG4-04 linka |
| Implementação em ferramenta (dbt, Airflow, Spark, Snowflake) | citação que ancora o conceito | Tecnologia (futura) | NUNCA tutorial nesta trilha |
| ML, feature stores, MLOps | fora de escopo | — | mencionar de passagem, não cobrir |

## Padrão de escrita (herdado de System Design/Operação/Comunicação/Auth)

Nota = capítulo de livro ([[feedback_padrao_capitulo_livro]]): TL;DR `[!abstract]`, abertura problema-first, divulgação progressiva, exemplo trabalhado (um domínio-fio recorrente ajuda — ex.: um e-commerce cujas vendas viram star schema, pipeline ELT, contrato e catálogo). Densidade ~440-540 linhas ([[feedback_notas_profundas_diagramas]]). `fase:` no frontmatter (Iniciado/Adepto/Magus). ≥1 Mermaid por nota (paleta azul `#4A90D9` / âmbar `#F5A623` / vermelho `#D0021B`; pipelines pedem flowchart de DAG, o ciclo de vida pede grafo, star schema pede ER). Callouts `[!question]-` / `[!warning]`. Seções "Em entrevista" + "How to explain in English" (tabela PT↔EN). "O que vem a seguir". `## Fontes` datadas. `[!info]` de caducidade nas notas com ferramenta/versão viva (Iceberg/Delta/Hudi, dbt/Fusion/Fivetran, DuckDB/DuckLake). **Tool-neutral: ferramenta é exemplo citado, nunca tutorial** — a nota ensina o conceito e cita como 2-3 ferramentas o encarnam.

## Fontes canônicas da trilha

- **Livros:** *Fundamentals of Data Engineering* (Reis/Housley — ciclo de vida + undercurrents, espinha do SG1); *The Data Warehouse Toolkit* 3ª ed. (Kimball/Ross — modelagem dimensional, espinha do SG2); *Building a Scalable Data Warehouse with Data Vault 2.0* (Linstedt — SG2-05); *Designing Data-Intensive Applications* (Kleppmann — só o recorte de batch/stream do SG3-05); *Data Mesh* (Zhamak Dehghani — SG4-04).
- **Docs/specs:** Apache Iceberg (spec v3), Delta Lake, Apache Hudi, Apache Parquet; dbt docs + dbt Fusion; Airflow/Dagster; docs de Snowflake/BigQuery/Databricks (arquitetura, não tutorial).
- **Referência web:** Data mesh (martinfowler.com/Dehghani), Modern Data Stack surveys 2026, artigos de data observability (Monte Carlo/Barr Moses — "5 pilares"), data contracts (Chad Sanderson/PayPal engineering).

## Plano de execução (ritmo B, igual às trilhas irmãs)

1. Reescrever `index.md` do galho-pai (MOC com os 4 sub-galhos + capstone) + criar `roadmap.md` recursivo do galho-pai.
2. Semear sub-galho a sub-galho, ordem 1→2→3→4. Cada subpasta: `index.md` + `roadmap.md` + notas via subagente-por-nota (≤3/onda, Sonnet; EXEMPLAR = nota 01 de uma trilha irmã até a 01 daqui virar exemplar próprio; WebSearch inline onde a ferramenta é viva; barra de densidade explícita ~440-540 linhas).
3. Ao fechar cada sub-galho: roadmap-folha + roadmap-pai + commit (paths explícitos, sem Co-Authored-By, push manual — [[feedback_git_commit_hygiene]], [[feedback_commits]]).
4. Fechamento: capstone; callouts nas notas-fronteira (BD 12-14, Comunicação streaming/contratos, Operação observabilidade, Segurança PII); atualizar `index.md` de Engenharia se preciso; atualizar [[00-Meta/Roadmap]] (Dados: seedling → 🟢); atualizar memória (novo arquivo `project_trilha_dados.md` + MEMORY.md).

## Pontos em aberto

- **Domínio-fio do exemplo trabalhado:** proponho um **e-commerce** (vendas → star schema → pipeline ELT → contrato/qualidade → catálogo) recorrendo em todas as notas, pra dar continuidade de capítulo. Confirmar na escrita.
- **SG2-05 (Data Vault / wide tables):** se qualquer um crescer muito, candidato a broto (`fase: Magus`) em vez de nota core.
- **DuckLake/Paimon:** citação leve em SG1-04; ecossistema muito novo (2025-2026) — caducidade explícita, não aprofundar.
- **Ritmo por sessão:** 19 notas ≈ 3-4 sessões (1-2 sub-galhos/sessão). A trilha Python roda em paralelo sob responsabilidade de outro agente — sem colisão de arquivos (domínios distintos).
