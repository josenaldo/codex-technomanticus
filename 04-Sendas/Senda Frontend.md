---
type: trail
title: Senda Frontend
domain: "[[03-Dominios/Frontend/index]]"
maturity: minimal
status: active
publish: true
created: 2024-01-01
updated: 2026-05-04
tags:
  - senda
  - frontend
---

# Senda Frontend

> Caminho de estudo de engenharia frontend. Atravessa fundamentos de linguagem (JavaScript core, TypeScript), libs e frameworks (React e ecossistema), validação, networking, debugging, ferramentas, e a disciplina de engenharia frontend (arquitetura, padrões, performance, acessibilidade).

## Pré-requisitos

(deixar vazio inicialmente; popular conforme necessário)

## Sequência

1. [[03-Dominios/Frontend/index|Frontend (engenharia)]]
2. [[03-Dominios/JavaScript/index|JavaScript]]
3. [[03-Dominios/TypeScript/index|TypeScript]]
4. [[03-Dominios/React/index|React]]
5. [[MUI|Material UI (MUI)]]
6. [[03-Dominios/React/Mantine|Mantine]]
7. [[Ícones|Ícones em React]]
8. [[TanStack Query|TanStack Query]]
9. [[TanStack Form|TanStack Form]]
10. [[React Hook Form|React Hook Form]]
11. [[Next.js|Next.js]]
12. [[03-Dominios/Frontend/Validação/index|Validação no Frontend]]
13. [[Zod|Zod]]
14. [[Yup|Yup]]
15. [[Joi|Joi]]
16. [[03-Dominios/Frontend/Networking/index|Networking no Frontend]]
17. [[Axios|Axios]]
18. [[Fetch|Fetch API]]
19. [[React Data Table|React Data Table Component]]
20. [[React Admin|React Admin]]
21. [[03-Dominios/React/Charts/index|Charts em React]]
22. [[Lightweight Charts|TradingView Lightweight Charts]]
23. [[ApexCharts|ApexCharts]]
24. [[Recharts|Recharts]]
25. [[Debugging|Frontend Debugging]]
26. [[Vite|Vite]]
27. [[Monorepos|Monorepos]]

## Trilhas relacionadas

- [[TypeScript com React]] — aprofundamento da intersecção TS+React (15 notas + MOC)

## Progresso

```dataview
TABLE WITHOUT ID
  link(file.path, regexreplace(file.folder, "^03-Domínios/", "") + "/" + file.name) AS "Nota",
  default(progresso, "pendente") AS "Status"
FROM outgoing([[]])
WHERE file.path != this.file.path AND contains(file.path, "03-Domínios/")
SORT file.folder ASC, file.name ASC
```

**Resumo:**

```dataview
TABLE WITHOUT ID
  length(rows) AS "Total",
  length(filter(rows, (r) => default(r.progresso, "pendente") = "feito")) AS "Feitas",
  length(filter(rows, (r) => default(r.progresso, "pendente") = "andamento")) AS "Em andamento",
  length(filter(rows, (r) => default(r.progresso, "pendente") = "pausado")) AS "Pausadas",
  length(filter(rows, (r) => default(r.progresso, "pendente") = "pendente")) AS "Pendentes"
FROM outgoing([[]])
WHERE file.path != this.file.path AND contains(file.path, "03-Domínios/")
GROUP BY true
```
