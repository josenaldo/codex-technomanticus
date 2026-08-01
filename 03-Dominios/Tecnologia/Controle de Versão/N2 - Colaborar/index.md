---
title: "N2 — Colaborar"
type: moc
publish: true
created: 2026-07-31
updated: 2026-07-31
status: seedling
tags:
  - moc
  - controle-de-versao
  - git
  - github
aliases:
  - Colaborar
  - Git nível 2
---

# N2 — Colaborar

> [!abstract] TL;DR
> Os níveis 0 e 1 ensinaram a usar o Git. Este ensina a **trabalhar em equipe com ele**: propor mudanças para revisão em vez de integrar direto (*pull requests*), escolher uma estratégia de ramificação compatível com o produto, escrever um histórico que gera changelog e versão automaticamente, e usar a plataforma além do `push` — proteções de branch, automação e o `gh` no terminal.

Aqui o público estreita. Os exemplos passam a ser de equipes de software, porque as práticas deste nível existem para resolver problemas de equipe: quem revisa, quando integra, o que a máquina verifica sozinha e o que precisa de gente.

Este é também o nível mais **político** do domínio. Metade do conteúdo não é sobre comandos, e sim sobre acordos: tamanho de proposta, tom de revisão, quem pode aprovar o quê. Ferramenta não resolve isso — só torna o acordo executável.

---

## As 5 notas

| # | Nota | O que você sai sabendo |
|---|------|------------------------|
| 12 | [[03-Dominios/Tecnologia/Controle de Versão/N2 - Colaborar/12 - Pull requests e a cultura de code review\|Pull requests e a cultura de code review]] | o fluxo do PR · tamanho como fator dominante · dar e receber revisão · squash × merge × rebase |
| 13 | [[03-Dominios/Tecnologia/Controle de Versão/N2 - Colaborar/13 - Estratégias de branching\|Estratégias de branching]] | GitHub Flow, Git Flow e trunk-based · qual o legado usa e por quê · o custo do ramo de longa duração |
| 14 | [[03-Dominios/Tecnologia/Controle de Versão/N2 - Colaborar/14 - Anatomia de um bom commit\|Anatomia de um bom commit]] | commit atômico · Conventional Commits · semver · tags e changelog automático |
| 15 | [[03-Dominios/Tecnologia/Controle de Versão/N2 - Colaborar/15 - GitHub como plataforma\|GitHub como plataforma]] | issues e projects · rulesets e CODEOWNERS · Actions como contrato · segurança do repositório |
| 16 | [[03-Dominios/Tecnologia/Controle de Versão/N2 - Colaborar/16 - gh CLI e automação do fluxo\|`gh` CLI e automação do fluxo]] | o fluxo inteiro sem sair do terminal · `gh pr checkout` · `gh api` para o que não tem comando |

> **Estado (2026-07-31):** **escrita completa — 5/5 notas.** Falta enriquecimento de mídia (M1). Ver o [[03-Dominios/Tecnologia/Controle de Versão/N2 - Colaborar/roadmap|roadmap do nível]].

---

## Veja também

- [[03-Dominios/Tecnologia/Controle de Versão/index|Controle de Versão]] — o domínio e os 7 níveis
- [[03-Dominios/Tecnologia/Controle de Versão/N1 - O fluxo diário/index|N1 — O fluxo diário]] — o nível anterior
- [[03-Dominios/Tecnologia/Controle de Versão/GitHub CLI|GitHub CLI]] — referência de consulta do `gh`, complementar à nota 16
- [[03-Dominios/Engenharia/Operação/index|Engenharia/Operação]] — CI/CD e deploy como disciplina; aqui só o que o repositório contrata
