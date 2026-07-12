---
title: "Roadmap — SG2 Modelagem para analytics"
created: 2026-07-12
type: meta
publish: false
tags:
  - meta
  - roadmap
  - dados
---

# Roadmap — SG2 Modelagem para analytics (folha)

Sub-galho `2 - Modelagem para analytics` (fase Adepto). Galho-pai: [[03-Dominios/Engenharia/Dados/roadmap]]. Spec: [[00-Meta/specs/2026-07-11-dados-engenharia-trilha-design]].

## Notas

| # | Nota | Escopo | Estado |
|---|------|--------|--------|
| 01 | Por que modelar pra analytics | do relacional normalizado (BD 04) ao dimensional; cubo OLAP; denormalização deliberada. | ✅ 224 linhas (2026-07-12) |
| 02 | Modelagem dimensional | fatos/dimensões, grão, star schema, aditividade; Kimball. Exemplo e-commerce. Mermaid: ER do star. | ✅ 307 linhas (2026-07-12) |
| 03 | Star vs snowflake e tipos de fato | star vs snowflake; transaction/periodic/accumulating snapshot; dimensões conformadas, bus matrix. | ✅ 331 linhas (2026-07-12) |
| 04 | Slowly Changing Dimensions | SCD 0-6, surrogate keys, late-arriving dimensions. | ✅ 286 linhas (2026-07-12) |
| 05 | Além de Kimball | Inmon vs Kimball vs Data Vault; One Big Table/wide tables; medallion (bronze/silver/gold). | ✅ 260 linhas (2026-07-12) |

**Sub-galho COMPLETO (5/5) em 2026-07-12.**

## Notas

- Referência de forma: nota exemplar da trilha em `1 - Fundamentos de engenharia de dados/01 - O que é engenharia de dados.md`.
- Densidade-alvo ~300-450 linhas; ≥1 Mermaid; seções fixas.
- Anti-duplicação: normalização OLTP mora em BD 04 (linkar); modelo dimensional vs relacional é o contraste, não reexplicar 3FN.
- SG2-05 (Data Vault/wide): candidato a broto se crescer demais.
