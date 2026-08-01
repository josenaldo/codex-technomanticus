---
title: "Controle de Versão"
type: moc
publish: true
created: 2026-07-31
updated: 2026-07-31
status: growing
tags:
  - moc
  - controle-de-versao
  - git
  - github
aliases:
  - Git
  - GitHub
  - Versionamento
  - Version Control
---

# Controle de Versão

> [!abstract] TL;DR
> Um caminho de **7 níveis** que começa onde você está — precisando parar de salvar `tcc-final-v3-AGORA-VAI.docx` — e termina lendo um repositório alheio como quem lê um raio-X. Os primeiros níveis são tutorial honesto: instalar, commitar, ramificar, colaborar. Do **nível 3** em diante, o mesmo material é reexplicado por baixo — e aí `reset --hard` deixa de ser reza e vira ponteiro se movendo num grafo.

Este domínio existe porque Git não é infraestrutura. Infraestrutura é o que sustenta a aplicação *depois que ela sai da máquina do dev*; Git é sobre o **histórico do código**, antes de rodar. E é, na prática, a ferramenta primária do ofício de consultor de legado — `log`, `blame`, `pickaxe`, `bisect` são o instrumento com que se lê um sistema que ninguém mais entende.

A lente que atravessa tudo: **o repositório como fonte de verdade** (o contrato de trabalho do time) **e como testemunha** (quem mudou o quê, por quê, e quando quebrou).

> [!info] Este material é feito pra ser compartilhado
> Cada nível é publicável e útil sozinho — dá pra mandar só o N0 pra quem está começando, sem que falte contexto. A ordem é do operacional pro conceitual, de propósito: quem começa por blob/tree/DAG desiste no primeiro parágrafo. O antídoto contra "ser mais um tutorial de Git" não é começar difícil — é **subir**.

---

## Os 7 níveis

| Nível | Sub-galho | O quê | Fase | Notas |
|---|-----------|-------|------|------:|
| **N0** | [[03-Dominios/Tecnologia/Controle de Versão/N0 - Sobrevivência/index\|Sobrevivência]] ✅ | o problema que o Git resolve · instalar e configurar · primeiro repositório · desfazer sem susto · GitHub e o repo na nuvem | Iniciado | 5 |
| **N1** | [[03-Dominios/Tecnologia/Controle de Versão/N1 - O fluxo diário/index\|O fluxo diário]] ✅ | `.gitignore` · ler o histórico · branches na prática · conflitos sem pânico · stash e worktrees · sincronizar com o time | Iniciado/Adepto | 6 |
| **N2** | [[03-Dominios/Tecnologia/Controle de Versão/N2 - Colaborar/index\|Colaborar]] ✅ | pull requests e code review · estratégias de branching · bom commit, tags e semver · GitHub como plataforma · `gh` CLI | Adepto | 5 |
| **N3** | [[03-Dominios/Tecnologia/Controle de Versão/N3 - O modelo por baixo/index\|O modelo por baixo]] ✅ | tudo tem hash · commit é snapshot e o DAG · refs/HEAD/branch como ponteiro · o index por dentro · merge e rebase por dentro | Adepto/Magus | 5 |
| **N4** | [[03-Dominios/Tecnologia/Controle de Versão/N4 - Quando dá errado/index\|Quando dá errado]] ✅ | a árvore de decisão do desfazer · `reflog` · reescrever história com segurança · segredos vazados · configurar o Git a seu favor | Magus | 5 |
| **N5** | [[03-Dominios/Tecnologia/Controle de Versão/N5 - Repositórios reais/index\|Repositórios reais]] ✅ | monorepo e clones parciais · submódulos e subtrees · cirurgia de repositório · Git no CI/CD e GitOps | Magus | 4 |
| **N6** | [[03-Dominios/Tecnologia/Controle de Versão/N6 - O repositório como testemunha/index\|O repositório como testemunha]] ✅ | ler história (`blame`, pickaxe) · `bisect` · forense de repositório | Magus | 3 |
| — | [[03-Dominios/Tecnologia/Controle de Versão/34 - Capstone - assumir um repositório desconhecido\|Capstone]] ✅ | assumir um repositório desconhecido — as primeiras 4 horas num repo alheio | Magus | 1 |

O **N3 é o ponto de virada**: ele não ensina comando novo, reexplica os anteriores como mecanismo. Do N4 em diante, o domínio é sobre o que tutorial não cobre — recuperação, reescrita segura, vazamento de segredo, cirurgia e forense.

---

## Artefatos do domínio

- [[03-Dominios/Tecnologia/Controle de Versão/GitHub CLI|GitHub CLI]] — **referência de consulta** do `gh` (2006 linhas, por área), migrada de `Infraestrutura/` em 2026-07-31. O capítulo que ensina o fluxo é a nota 16.
- [[03-Dominios/Tecnologia/Controle de Versão/Biblioteca de Controle de Versão|Biblioteca de Controle de Versão]] — recursos externos curados, **com peso em simuladores interativos** (Learn Git Branching, Visualizing Git, Oh My Git!, Git Exercises, git-katas) e **bloco PT-BR** herdado do repositório [`aprendendo-git-e-github`](https://github.com/josenaldo/aprendendo-git-e-github) do autor. É a peça que permite às notas explicarem o *modelo* e delegarem a *repetição*.

> **Estado (2026-07-31):** **ESCRITA COMPLETA — 34/34 notas**, 7 níveis + capstone. Roster, lente e progressão por níveis fechados no [[00-Meta/specs/2026-07-31-dominio-controle-de-versao-design|design]] — que inclui a análise dos 4 repositórios de workshop do autor e o mapa de aproveitamento item a item. Construção sequencial **N0 → N6 → capstone**, com validação a cada nível. **N0 escrito para público geral** — estudante/acadêmico que precisa parar de perder arquivos, sem pressupor programação; do N1 em diante o público estreita gradualmente pro perfil dev.

---

## Fronteiras — versionamento que já mora em outras trilhas

Este domínio **linka** as notas abaixo como reforço, **nunca as reescreve**.

- [[03-Dominios/Engenharia/Arqueologia e Restauração de Software/index|Engenharia/Arqueologia e Restauração de Software]] — o **método** de ler um sistema legado. O N6 daqui é o **instrumento**.
- [[03-Dominios/Engenharia/Operação/index|Engenharia/Operação]] — CI/CD, deploy e GitOps como disciplina de entrega. Aqui só o contrato repo↔pipeline (nota 30).
- [[03-Dominios/Tecnologia/Terminal/index|Terminal]] — Lazygit (TUIs 01-06), `delta` (CLI Utils 10) e bare repo pra dotfiles seguem morando lá.
- [[03-Dominios/Tecnologia/Tooling e Build/index|Tooling e Build]] — husky/lint-staged (nota 16) e supply chain de dependências (nota 24).
- [[03-Dominios/Tecnologia/Infraestrutura/index|Infraestrutura]] — de onde o `GitHub CLI` saiu em 2026-07-31; a estante lá é sobre o que roda **depois** que o código sai da máquina do dev.

---

## Veja também

- [[00-Meta/Roadmap|Roadmap de Trilhas]] — Controle de Versão entra como **Tier 0**.
- [[00-Meta/specs/2026-07-31-dominio-controle-de-versao-design|Design do domínio]] — roster completo, análise do material próprio e justificativa das fronteiras.
- [[03-Dominios/Carreira/Entrevistas/index|Entrevistas]] — fluxo de trabalho com Git é pergunta recorrente de entrevista sênior.
