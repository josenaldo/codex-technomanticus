---
title: "Dados"
type: moc
publish: true
created: 2026-06-23
updated: 2026-07-13
status: seedling
tags:
  - moc
  - dados
aliases:
  - Dados
  - Engenharia de Dados
---
# Dados

> [!abstract] TL;DR
> A **engenharia de dados em escala** — o que vem depois de "saber SQL": modelagem dimensional, data warehouse vs lake vs lakehouse, pipelines ETL/ELT, orquestração, qualidade e contratos de dados, governança. O *como construir sistemas de dados analíticos*, neutro de ferramenta. Escrito pela lente do **sênior fullstack que precisa decidir e conversar** sobre dados — não virar data engineer.

Trata da engenharia de dados como disciplina, distinta da **teoria de banco de dados** (modelo relacional, ACID, normalização, índices, replicação, NoSQL) que vive inteira em [[03-Dominios/Ciência/Banco de Dados/index|Banco de Dados]], na camada de Ciência. Aqui ficam as decisões de construção do lado **OLAP/analytics**: como modelar para análise, como mover dados entre sistemas, como garantir consistência e qualidade em pipelines, como organizar uma plataforma de dados. Ferramentas (dbt, Airflow, Iceberg, Snowflake, Spark) aparecem como **exemplos que ancoram o conceito**, nunca como tutorial — o *como em ferramenta X* mora em [[03-Dominios/Tecnologia/index|Tecnologia]].

## Conteúdo

Trilha em 4 sub-galhos (3 fases Iniciado/Adepto/Magus) + capstone. Estado em [[03-Dominios/Engenharia/Dados/roadmap|roadmap]].

1. [[03-Dominios/Engenharia/Dados/1 - Fundamentos de engenharia de dados/index|Fundamentos de engenharia de dados]] *(Iniciado)* — OLTP vs OLAP, o ciclo de vida dos dados, warehouse/lake/lakehouse, armazenamento colunar e formatos.
2. [[03-Dominios/Engenharia/Dados/2 - Modelagem para analytics/index|Modelagem para analytics]] *(Adepto)* — modelagem dimensional, star vs snowflake, Slowly Changing Dimensions, além de Kimball.
3. [[03-Dominios/Engenharia/Dados/3 - Pipelines - movimentação e transformação/index|Pipelines: movimentação e transformação]] *(Adepto→Magus)* — ETL vs ELT, ingestão e CDC, transformação SQL-first, orquestração, dados em movimento.
4. [[03-Dominios/Engenharia/Dados/4 - Qualidade, governança e organização/index|Qualidade, governança e organização]] *(Magus)* — qualidade e observabilidade, data contracts, governança/catálogo/lineage, arquiteturas organizacionais.

★ [[03-Dominios/Engenharia/Dados/Capstone - Desenhando a plataforma de dados de uma empresa do zero|Capstone — Desenhando a plataforma de dados de uma empresa do zero]] *(Magus)* — o walkthrough decisório que costura os 4 sub-galhos, do gatilho OLTP/OLAP à escolha entre warehouse centralizado e data mesh.

## Veja também

- [[03-Dominios/Ciência/Banco de Dados/index|Banco de Dados]] — os fundamentos relacionais, SQL, transações, índices, replicação e NoSQL (o lado OLTP e distribuído)
- [[03-Dominios/Engenharia/Comunicação entre Sistemas/index|Comunicação entre Sistemas]] — mensageria e eventos que alimentam pipelines; contratos e schema registry
- [[03-Dominios/Engenharia/Operação/index|Operação]] — observabilidade e operação em produção que a plataforma de dados herda
- [[03-Dominios/Engenharia/index|Engenharia]]
