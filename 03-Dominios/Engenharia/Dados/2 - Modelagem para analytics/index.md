---
title: "Modelagem para analytics"
type: moc
publish: true
tags:
  - dados
  - moc
created: 2026-07-12
---

# Modelagem para analytics — Dados

O coração da trilha. Um data warehouse só entrega valor se os dados dentro dele estiverem modelados para a pergunta analítica — e o esquema normalizado a 3FN que serve tão bem o OLTP é justamente o errado aqui. Este sub-galho (fase **Adepto**) ensina a **modelagem dimensional** de Kimball: fatos e dimensões, o grão, star vs snowflake, os tipos de fato, o problema das dimensões que mudam no tempo (SCD), e as abordagens que vão além de Kimball (Data Vault, wide tables, medallion).

## Notas

1. [[01 - Por que modelar pra analytics]]
2. [[02 - Modelagem dimensional]]
3. [[03 - Star vs snowflake e tipos de fato]]
4. [[04 - Slowly Changing Dimensions]]
5. [[05 - Além de Kimball]]

## Veja também

- [[03-Dominios/Engenharia/Dados/index|Dados]] — o galho-pai
- [[1 - Fundamentos de engenharia de dados/index|Fundamentos de engenharia de dados]] — o sub-galho anterior (onde os dados vivem)
- [[3 - Pipelines - movimentação e transformação/index|Pipelines]] — o próximo, onde o modelo é preenchido por pipelines
- [[03-Dominios/Ciência/Banco de Dados/04 - Modelagem e normalização|Banco de Dados 04]] — a normalização OLTP que este sub-galho contrasta
