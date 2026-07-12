---
title: "Roadmap — SG3 Pipelines: movimentação e transformação"
created: 2026-07-12
type: meta
publish: false
tags:
  - meta
  - roadmap
  - dados
---

# Roadmap — SG3 Pipelines: movimentação e transformação (folha)

Sub-galho `3 - Pipelines - movimentação e transformação` (fase Adepto→Magus: 01-02 Adepto, 03-05 Magus). Galho-pai: [[03-Dominios/Engenharia/Dados/roadmap]]. Spec: [[00-Meta/specs/2026-07-11-dados-engenharia-trilha-design]].

## Notas

| # | Nota | Fase | Escopo | Estado |
|---|------|------|--------|--------|
| 01 | ETL vs ELT | Adepto | virada cloud, storage/compute, onde ETL ainda vale, pipeline como grafo. | ✅ 222 linhas (2026-07-12) |
| 02 | Ingestão de dados | Adepto | batch vs incremental, CDC (log vs query), idempotência, EL tools. Link BD 12. `[!info]`. | ✅ 212 linhas (2026-07-12) |
| 03 | Transformação SQL-first | Magus | analytics engineering (dbt table-stakes, Fusion/Rust, SQLMesh), modularidade/testes/lineage, semantic layer. `[!info]` + WebSearch. | ✅ 293 linhas (2026-07-12) |
| 04 | Orquestração | Magus | DAG, idempotência, backfill, scheduling vs event-driven, orquestrador como sistema. Link Operação. Mermaid: DAG. | ✅ 216 linhas (2026-07-12) |
| 05 | Dados em movimento | Magus | batch vs streaming, lambda vs kappa, micro-batch, quando streaming vale. Fronteira → Comunicação/BD 14. | ✅ 282 linhas (2026-07-12) |

**Sub-galho COMPLETO (5/5) em 2026-07-12.**

## Notas

- Referência de forma: nota exemplar `1 - Fundamentos de engenharia de dados/01 - O que é engenharia de dados.md`.
- Densidade ~300-460 linhas; ≥1 Mermaid; seções fixas.
- Anti-duplicação: streaming/Kafka/mensageria em profundidade = Comunicação entre Sistemas (nota 05 só recorta o ângulo analytics + linka); replicação/log = BD 12; observabilidade/rodar em prod = Operação.
- Tool-neutral: dbt/Airflow/Fivetran/Kafka só citação, nunca tutorial. `[!info]` de caducidade nas notas com ferramenta viva (02, 03).
