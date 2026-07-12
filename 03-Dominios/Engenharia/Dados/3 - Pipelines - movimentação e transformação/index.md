---
title: "Pipelines: movimentação e transformação"
type: moc
publish: true
tags:
  - dados
  - moc
created: 2026-07-12
---

# Pipelines: movimentação e transformação — Dados

O modelo dimensional do sub-galho anterior não se preenche sozinho. Este sub-galho (fase **Adepto→Magus**) é sobre os **pipelines** que trazem o dado da fonte até o warehouse e o transformam no caminho: a virada de ETL para ELT, a ingestão (batch, incremental, CDC), a transformação SQL-first (a era do analytics engineering), a orquestração como sistema, e a fronteira do streaming — quando processar dado em movimento em vez de em lote.

## Notas

1. [[01 - ETL vs ELT]]
2. [[02 - Ingestão de dados]]
3. [[03 - Transformação SQL-first]]
4. [[04 - Orquestração]]
5. [[05 - Dados em movimento]]

## Veja também

- [[03-Dominios/Engenharia/Dados/index|Dados]] — o galho-pai
- [[2 - Modelagem para analytics/index|Modelagem para analytics]] — o modelo que estes pipelines preenchem
- [[4 - Qualidade, governança e organização/index|Qualidade, governança e organização]] — o próximo, sobre confiar no que o pipeline entrega
- [[03-Dominios/Engenharia/Comunicação entre Sistemas/index|Comunicação entre Sistemas]] — a mensageria/streaming que a nota 05 referencia
