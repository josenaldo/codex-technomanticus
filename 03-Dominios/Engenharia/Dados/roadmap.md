---
title: "Roadmap — Dados (Engenharia de Dados)"
created: 2026-07-12
type: meta
publish: false
tags:
  - meta
  - roadmap
  - dados
---

# Roadmap — Dados (galho-pai)

Roadmap do galho `03-Dominios/Engenharia/Dados`. Galho-**pai**: mapeia o estado dos sub-galhos. Cada sub-galho tem seu próprio `roadmap.md` (folha). Specs de origem: [[00-Meta/specs/2026-07-11-dados-engenharia-trilha-design]] · [[00-Meta/specs/2026-07-12-dados-engenharia-trilha-plan]].

## Estado dos sub-galhos

| # | Sub-galho | Fase | Notas planejadas | Estado |
|---|-----------|------|------------------|--------|
| 0 | Scaffold do galho-pai (index + roadmap) | — | — | ✅ (2026-07-12) |
| 1 | Fundamentos de engenharia de dados | Iniciado | 4 | ⬜ a semear |
| 2 | Modelagem para analytics | Adepto | 5 | ⬜ a semear |
| 3 | Pipelines: movimentação e transformação | Adepto→Magus | 5 | ⬜ a semear |
| 4 | Qualidade, governança e organização | Magus | 4 | ⬜ a semear |
| ★ | Capstone — Desenhando a plataforma de dados de uma empresa do zero | Magus | 1 | ⬜ a semear |

**Total planejado:** 18 notas de conteúdo + 1 capstone (19) + scaffolding (index/roadmap por sub-galho).

## Ordem de execução (ritmo B)

Sub-galho a sub-galho, ponta a ponta: 1 → 2 → 3 → 4 → capstone. Subagente-por-nota (≤3/onda, Sonnet); gate `verificar-nota` por nota. Commit por sub-galho (paths explícitos, sem Co-Authored-By, push manual). Ao fechar cada sub-galho, atualizar o roadmap-folha dele e esta tabela.

## Rollup para o domínio (ao concluir)

- Callouts apontando pra cá nas notas-fronteira: [[03-Dominios/Ciência/Banco de Dados/index|Banco de Dados]] 12-14 (replicação/distribuído/NoSQL), Comunicação entre Sistemas (streaming/mensageria, contratos/schema registry), Operação (observabilidade), Segurança (PII/LGPD).
- Atualizar [[00-Meta/Roadmap]]: seção Engenharia + status de Dados (seedling → 🟢).
- Sinalizar que tutorial de ferramenta (dbt, Airflow, Spark, warehouse específico) mora em `Tecnologia/`, futuro.

## Pendências transversais

- Baseline de versões/estado 2026 (revisar na manutenção): Iceberg default de lakehouse aberto (spec v3) · Delta (Databricks/Fabric) · Hudi (upserts/CDC) · UniForm/XTable (interop) · dbt table-stakes + Fusion/Rust + Fivetran/dbt Labs (out/2025) · DuckDB/DuckLake · data contracts como primitivo de warehouse. Ecossistema volátil — `[!info]` de caducidade nas notas com ferramenta viva.
- Domínio-fio do exemplo trabalhado: e-commerce (vendas → star schema → ELT → contrato → catálogo), recorrente pra dar continuidade de capítulo.
- SG2-05 (Data Vault / wide tables): se crescer demais na escrita, candidato a broto `fase: Magus`.
