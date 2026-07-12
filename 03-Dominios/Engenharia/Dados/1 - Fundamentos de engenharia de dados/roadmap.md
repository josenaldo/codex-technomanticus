---
title: "Roadmap — SG1 Fundamentos de engenharia de dados"
created: 2026-07-12
type: meta
publish: false
tags:
  - meta
  - roadmap
  - dados
---

# Roadmap — SG1 Fundamentos de engenharia de dados (folha)

Sub-galho `1 - Fundamentos de engenharia de dados` (fase Iniciado). Galho-pai: [[03-Dominios/Engenharia/Dados/roadmap]]. Spec: [[00-Meta/specs/2026-07-11-dados-engenharia-trilha-design]].

## Notas

| # | Nota | Escopo | Estado |
|---|------|--------|--------|
| 01 | O que é engenharia de dados | OLTP vs OLAP; por que o banco transacional não basta pra analytics; DE vs analytics engineer vs data scientist. | ✅ 307 linhas (2026-07-12) |
| 02 | O ciclo de vida da engenharia de dados | geração→ingestão→armazenamento→transformação→serving; undercurrents (Reis/Housley); mapa da trilha. Mermaid: grafo do ciclo. | ✅ 229 linhas (2026-07-12) |
| 03 | Warehouse, lake e lakehouse | os 3 paradigmas; história Inmon→Hadoop→cloud DW→lakehouse; data swamp; storage/compute. | ✅ 264 linhas (2026-07-12) |
| 04 | Armazenamento colunar e formatos | row vs colunar; Parquet/ORC/Avro; compressão/encoding; open table formats (Iceberg default 2026, Delta, Hudi; UniForm/XTable). `[!info]` caducidade + WebSearch. | ✅ 252 linhas (2026-07-12) |

**Sub-galho COMPLETO (4/4) em 2026-07-12.**

## Notas

- Nota 01 = **exemplar de arranque**: usar como referência de forma `Auth e Identidade/1 - Fundamentos de identidade/01 - Identidade, autenticação e autorização — o mapa.md` até a 01 daqui virar exemplar próprio.
- Densidade-alvo ~440-540 linhas; ≥1 Mermaid; seções fixas (Em entrevista / How to explain in English / O que vem a seguir / Fontes).
- Anti-duplicação: linkar BD (Ciência), não reexplicar OLTP/relacional.
