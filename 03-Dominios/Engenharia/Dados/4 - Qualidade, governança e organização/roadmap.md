---
title: "Roadmap — SG4 Qualidade, governança e organização"
created: 2026-07-13
type: meta
publish: false
tags:
  - meta
  - roadmap
  - dados
---

# Roadmap — SG4 Qualidade, governança e organização (folha)

Sub-galho `4 - Qualidade, governança e organização` (fase Magus). Galho-pai: [[03-Dominios/Engenharia/Dados/roadmap]]. Spec: [[00-Meta/specs/2026-07-11-dados-engenharia-trilha-design]].

## Notas

| # | Nota | Fase | Escopo | Estado |
|---|------|------|--------|--------|
| 01 | Qualidade e observabilidade de dados | Magus | dimensões de qualidade, testes de dados, 5 pilares de data observability (freshness/volume/schema/quality/lineage), anomalias, SLA de dados. Link Operação. `[!info]`. | ✅ 211 linhas (2026-07-13) |
| 02 | Data contracts e schema evolution | Magus | contrato produtor↔consumidor, shift-left, compat back/forward, silent breakage, primitivos de contrato nos warehouses 2026. Link Comunicação. `[!info]` caducidade. | ✅ 186 linhas (2026-07-13) |
| 03 | Governança, catálogo e lineage | Magus | metadata, data catalog, lineage end-to-end, PII/LGPD/GDPR, classificação/mascaramento, data as a product. Link Segurança. | ✅ 235 linhas (2026-07-13) |
| 04 | Arquiteturas organizacionais | Magus | warehouse centralizado vs data mesh (domínios/produto/self-service/governança federada) vs data fabric, Conway, mesh hype vs necessidade. Link System Design. Fecha o corpo. | ✅ 233 linhas (2026-07-13) |

**Sub-galho COMPLETO (4/4) em 2026-07-13.**

## Notas de execução

- Referência de forma: nota exemplar `1 - Fundamentos de engenharia de dados/01 - O que é engenharia de dados.md`.
- Densidade ~250-350 linhas; ≥1 Mermaid na paleta; 4 seções fixas (Em entrevista, How to explain in English + tabela PT/EN, O que vem a seguir, Fontes); TL;DR + Perguntas que esta nota responde no topo.
- Tool-neutral: Monte Carlo/Great Expectations/dbt tests/OpenLineage/DataHub/Collibra só citação, nunca tutorial. `[!info]` de caducidade nas notas com ferramenta viva (01, 02).
- Anti-duplicação: observabilidade de sistema/SLO = Operação (linkar, recortar só o ângulo de dados); schema registry/versionamento de contrato de API = Comunicação; criptografia/PII em profundidade = Segurança; Conway/organização de times = System Design.
- Exemplo-fio: e-commerce (contrato da tabela de pedidos, catálogo da dim_produto, mesh por domínio de vendas/logística).
