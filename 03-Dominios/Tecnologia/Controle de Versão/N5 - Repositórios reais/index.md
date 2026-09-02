---
title: "N5 — Repositórios reais"
type: moc
publish: true
created: 2026-07-31
updated: 2026-07-31
status: seedling
tags:
  - moc
  - controle-de-versao
  - git
aliases:
  - Repositórios reais
  - Git nível 5
---

# N5 — Repositórios reais

> [!abstract] TL;DR
> Até aqui, todo repositório se comportou: cabia num clone, era autossuficiente, tinha uma história limpa. Este nível trata dos outros — os que **não cabem** (clone parcial, sparse-checkout, LFS), os que **dependem de outros** (submódulos, subtrees), os que precisam ser **operados** (migrar de SVN, dividir, fundir) e os que precisam **conversar com o pipeline** (o que a CI espera do repositório).

É o nível de quem herda projeto, e por isso ele é o vizinho mais próximo do [[03-Dominios/Engenharia/Arqueologia e Restauração de Software/index|ofício de trabalhar com legado]]. As decisões aqui são quase todas irreversíveis ou caras de reverter — daí o peso em "quando NÃO fazer".

---

## As 4 notas

| # | Nota | Para quando |
|---|------|-------------|
| 27 | [[03-Dominios/Tecnologia/Controle de Versão/N5 - Repositórios reais/27 - Monorepo e polyrepo\|Monorepo e polyrepo]] | o clone demora, o repositório tem gigabytes, ou você precisa decidir quantos repositórios ter |
| 28 | [[03-Dominios/Tecnologia/Controle de Versão/N5 - Repositórios reais/28 - Submódulos e subtrees\|Submódulos e subtrees]] | um repositório precisa conter outro |
| 29 | [[03-Dominios/Tecnologia/Controle de Versão/N5 - Repositórios reais/29 - Cirurgia de repositório\|Cirurgia de repositório]] | migrar de SVN, dividir um monólito, fundir dois repositórios |
| 30 | [[03-Dominios/Tecnologia/Controle de Versão/N5 - Repositórios reais/30 - Git no CI-CD e GitOps\|Git no CI/CD e GitOps]] | o pipeline se comporta diferente da sua máquina |

---

## Veja também

- [[03-Dominios/Tecnologia/Controle de Versão/index|Controle de Versão]] — o domínio e os 7 níveis
- [[03-Dominios/Tecnologia/Controle de Versão/N4 - Quando dá errado/index|N4 — Quando dá errado]] — o nível anterior; a nota 29 usa as ferramentas de lá
- [[03-Dominios/Engenharia/Operação/index|Engenharia/Operação]] — a nota 30 para na fronteira dela
