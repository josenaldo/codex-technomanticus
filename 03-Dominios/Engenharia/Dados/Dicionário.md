---
title: "Dicionário — Dados"
created: 2026-07-20
updated: 2026-07-20
type: glossary
status: seedling
aliases: []
tags:
  - glossary
  - dados
lang: pt
publish: true
---

# Dicionário — Dados

> Glossário do domínio Engenharia de Dados: vocabulário da construção de sistemas analíticos — modelagem, pipelines, plataformas — neutro de ferramenta, com o exemplo de mercado citado quando ancora o conceito. Cada verbete é referenciado por uma ou mais notas das trilhas do domínio.

<!--
Como usar este glossário:

- Verbetes em ordem alfabética, um `###` cada.
- Linkar de outra nota: `[[03-Dominios/Engenharia/Dados/Dicionário#Nome do termo]]`
- Customizar texto exibido: `[[03-Dominios/Engenharia/Dados/Dicionário#Nome do termo|texto]]`
- A skill /verbete adiciona termos automaticamente em ordem alfabética.
- Cada verbete tem 2-4 linhas de definição em PT-BR, neutra de ferramenta.
-->

### OLAP

*Online Analytical Processing*: perfil de carga de trabalho analítica — poucas queries, cada uma varrendo milhões de linhas para agregar, agrupar e comparar ao longo do tempo. Otimiza **throughput de leitura**, não latência de escrita: armazenamento colunar, desnormalização e modelagem dimensional. É o lado que a engenharia de dados constrói (warehouse, lake, lakehouse), em oposição ao OLTP que serve a aplicação.

*Veja também: [[03-Dominios/Engenharia/Dados/1 - Fundamentos de engenharia de dados/01 - O que é engenharia de dados|O que é engenharia de dados]], [[03-Dominios/Engenharia/Dados/1 - Fundamentos de engenharia de dados/03 - Warehouse, lake e lakehouse|Warehouse, lake e lakehouse]]*

### OLTP

*Online Transaction Processing*: perfil de carga de trabalho transacional — muitas operações pequenas e concorrentes (insert/update/delete de poucas linhas), com latência baixa e garantias ACID. Armazenamento por linha e modelo normalizado. É o banco que serve a aplicação; os dados nascem aqui e são movidos para o OLAP por pipelines de ingestão/CDC.

*Veja também: [[03-Dominios/Ciência/Banco de Dados/index|Banco de Dados]], [[03-Dominios/Engenharia/Dados/3 - Pipelines - movimentação e transformação/index|Pipelines: movimentação e transformação]]*
