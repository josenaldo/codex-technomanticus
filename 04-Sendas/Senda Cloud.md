---
type: trail
title: Senda Cloud
domain: "[[03-Dominios/Tecnologia/Cloud/index]]"
maturity: minimal
status: active
publish: true
created: 2024-01-01
updated: 2026-07-20
tags:
  - senda
  - cloud
---

# Senda Cloud

> [!abstract] TL;DR
> Esta Senda é ordem de **leitura** — o [[03-Dominios/Tecnologia/Cloud/roadmap|Roadmap]] é ordem de *construção*. Os dois nem sempre coincidem: o Roadmap rastreia o que já foi escrito; esta Senda sugere por onde entrar na trilha depois que ela existir. Os links crus que antes viviam aqui (AWS Architecture Center, Well-Architected, etc.) migraram pra [[03-Dominios/Tecnologia/Cloud/Biblioteca|Biblioteca]].

## Pré-requisitos

(deixar vazio inicialmente; popular conforme necessário)

## Trilha de leitura sugerida

A trilha Cloud tem 24 galhos em 5 blocos. Como ordem de *leitura* (não de construção), agrupe em 3 etapas:

1. **Fundamentos** (Bloco 1) — o modelo mental antes de qualquer serviço específico: o que é a nuvem, como um provedor é organizado, o Well-Architected Framework como bússola, IAM como base de tudo.
2. **Primitivos + serverless** (Blocos 2 e 3) — compute, rede, armazenamento, bancos gerenciados, DNS/CDN, e depois a camada serverless/event-driven que se apoia neles.
3. **Governança + maestria** (Blocos 4 e 5) — operar, sustentar e governar o que foi construído (IaC, observabilidade, segurança, FinOps, resiliência), fechando com a consolidação por provedor (AWS e DigitalOcean a fundo) e a certificação.

Quem já usa DigitalOcean no dia a dia pode adiantar a leitura do galho de consolidação DigitalOcean (Bloco 5) como âncora prática antes de completar a etapa 1 — ver "Como ler" no [[03-Dominios/Tecnologia/Cloud/index|domínio Cloud]].

## Domínio e recursos

- [[03-Dominios/Tecnologia/Cloud/index|Domínio Cloud]] — MOC com o roster completo dos 24 galhos + capstone.
- [[03-Dominios/Tecnologia/Cloud/Biblioteca|Biblioteca — Cloud]] — recursos externos por provedor (AWS, DigitalOcean, Azure, Google Cloud).
- [[03-Dominios/Tecnologia/Cloud/Dicionário|Dicionário — Cloud]] — glossário provider-neutro.

## Progresso

```dataview
TABLE WITHOUT ID
  link(file.path, regexreplace(file.folder, "^03-Dominios/", "") + "/" + file.name) AS "Nota",
  default(progresso, "pendente") AS "Status"
FROM outgoing([[]])
WHERE file.path != this.file.path AND contains(file.path, "03-Dominios/")
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
WHERE file.path != this.file.path AND contains(file.path, "03-Dominios/")
GROUP BY true
```
