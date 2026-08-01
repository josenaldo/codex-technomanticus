---
title: "Versionamento"
created: 2026-04-01
updated: 2026-07-31
type: concept
progress: done
status: evergreen
tags:
  - ferramentas
  - git
  - entrevista
publish: false
---

# Versionamento

> [!info] Tronco podado — o conteúdo virou domínio próprio
> Esta nota era um monólito sobre Git (comandos, merge × rebase, workflows, Conventional Commits, boas práticas). Em **2026-07-31** o assunto ganhou domínio próprio, com 7 níveis do tutorial operacional ao modelo interno: **[[03-Dominios/Tecnologia/Controle de Versão/index|Tecnologia/Controle de Versão]]**.
>
> Nada foi perdido — cada seção daqui foi absorvida e expandida numa nota atômica. O mapa está abaixo.

## Para onde foi cada coisa

| O que havia aqui | Onde está agora |
|---|---|
| O que é Git, VCS distribuído, história | [[03-Dominios/Tecnologia/Controle de Versão/N0 - Sobrevivência/01 - O problema que o Git resolve\|01 — O problema que o Git resolve]] |
| Configuração inicial (`user.name`, `user.email`) | [[03-Dominios/Tecnologia/Controle de Versão/N0 - Sobrevivência/02 - Instalar e configurar o Git\|02 — Instalar e configurar o Git]] |
| Áreas do Git, `add`/`commit`/`log`, ciclo de vida | [[03-Dominios/Tecnologia/Controle de Versão/N0 - Sobrevivência/03 - Seu primeiro repositório\|03 — Seu primeiro repositório]] |
| Desfazer: `restore`, `reset`, `revert`, `amend` | [[03-Dominios/Tecnologia/Controle de Versão/N0 - Sobrevivência/04 - Desfazer sem susto\|04 — Desfazer sem susto]] · árvore de decisão completa na nota 22 (N4) |
| Remotos, `push`/`pull`/`fetch` | [[03-Dominios/Tecnologia/Controle de Versão/N0 - Sobrevivência/05 - GitHub - colocar o repositório na nuvem\|05 — GitHub]] · [[03-Dominios/Tecnologia/Controle de Versão/N1 - O fluxo diário/11 - Sincronizar com o time\|11 — Sincronizar com o time]] |
| `.gitignore` | [[03-Dominios/Tecnologia/Controle de Versão/N1 - O fluxo diário/06 - Ignorar arquivos - o gitignore e suas regras\|06 — Ignorar arquivos]] |
| Branches, merge × rebase, resolução de conflitos | [[03-Dominios/Tecnologia/Controle de Versão/N1 - O fluxo diário/08 - Branches na prática\|08 — Branches na prática]] · [[03-Dominios/Tecnologia/Controle de Versão/N1 - O fluxo diário/09 - Conflito - por que acontece e como resolver\|09 — Conflito]] · mecanismo por baixo na nota 21 (N3) |
| Stash | [[03-Dominios/Tecnologia/Controle de Versão/N1 - O fluxo diário/10 - Guardar trabalho pela metade - stash e worktrees\|10 — stash e worktrees]] |
| Git Flow, GitHub Flow, Trunk-Based | [[03-Dominios/Tecnologia/Controle de Versão/N2 - Colaborar/13 - Estratégias de branching\|13 — Estratégias de branching]] |
| Conventional Commits, semver, tags, boas práticas | [[03-Dominios/Tecnologia/Controle de Versão/N2 - Colaborar/14 - Anatomia de um bom commit\|14 — Anatomia de um bom commit]] |
| PRs, proteção da `main`, review | [[03-Dominios/Tecnologia/Controle de Versão/N2 - Colaborar/12 - Pull requests e a cultura de code review\|12 — Pull requests]] · [[03-Dominios/Tecnologia/Controle de Versão/N2 - Colaborar/15 - GitHub como plataforma\|15 — GitHub como plataforma]] |
| Clients gráficos (Sourcetree, GitKraken) | mencionados em [[03-Dominios/Tecnologia/Controle de Versão/N0 - Sobrevivência/02 - Instalar e configurar o Git\|02]]; TUIs em [[03-Dominios/Tecnologia/Terminal/index\|Terminal]] |
| Recursos externos e material de estudo | [[03-Dominios/Tecnologia/Controle de Versão/Biblioteca de Controle de Versão\|Biblioteca de Controle de Versão]] |

> [!note] O que **não** migrou, e por quê
> As duas seções abaixo são **material de entrevista**, não de trilha: relato pessoal e articulação em inglês. O domínio novo é escrito para público amplo e não incorpora experiência pessoal do autor, então elas ficam preservadas aqui. Se forem trabalhadas, o destino natural é [[03-Dominios/Carreira/Entrevistas/index|Carreira/Entrevistas]].

## Na prática (da minha experiência)

> Uso GitHub Flow em todos os projetos — feature branches + PRs + CI obrigatório. Conventional Commits para mensagens padronizadas, o que permite changelogs automáticos. No MedEspecialista, GitHub Actions roda testes e linting em cada PR, e merge só é permitido com review aprovado e checks verdes. Para deploys, tags (`v1.0.0`) disparam o pipeline de release.

## How to explain in English

"Git is central to my development workflow. I follow GitHub Flow — short-lived feature branches, pull requests with code review, and CI/CD that validates every change before merge to main.

I use Conventional Commits for semantic commit messages, which enables automatic changelog generation and semantic versioning. Each commit should be atomic — doing one thing — so it can be reverted independently if needed.

For branch management, I prefer rebase over merge for feature branches to maintain a clean linear history. I rebase my feature branch on main before opening a PR, resolve any conflicts locally, then the PR shows a clean diff. After review and CI passes, we squash-merge to main.

One thing I always emphasize is protecting the main branch — requiring PR reviews, passing CI checks, and never allowing force pushes. This ensures main is always deployable."

### Key vocabulary

- branch → branch: linha independente de desenvolvimento
- commit → commit: snapshot do código em um ponto no tempo
- merge → merge: combinar branches
- rebase → rebase: reaplicar commits sobre outra base
- stash → stash: guardar mudanças temporariamente
- pull request → pull request (PR): proposta de merge com review
- conflito → merge conflict
- histórico → git history / git log
- tag → tag: marcador de versão

## Veja também

- [[03-Dominios/Tecnologia/Controle de Versão/index|Controle de Versão]] — o domínio completo
- [[03-Dominios/Tecnologia/Terminal/index|Terminal]]
