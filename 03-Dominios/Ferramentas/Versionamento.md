---
title: "Versionamento"
created: 2026-04-01
updated: 2026-04-02
type: concept
status: seedling
tags:
  - ferramentas
  - git
  - entrevista
publish: false
---

# Versionamento

Git — o sistema de controle de versão que todo dev usa. Comandos essenciais, workflows, e boas práticas.

## O que é

Git é um sistema de controle de versão distribuído criado por Linus Torvalds (2005). Cada desenvolvedor tem uma cópia completa do repositório. É a base de todo workflow moderno de desenvolvimento — branches, PRs, CI/CD.

## Como funciona

### Áreas do Git

```text
Working Directory → Stage (Index) → Local Repository → Remote Repository
      ↑                  ↑                ↑                    ↑
   git add          git commit        git push            git fetch/pull
```

- **Working Directory:** arquivos no disco, com modificações
- **Stage (Index):** área de preparação — o que vai no próximo commit
- **Local Repository:** histórico de commits local (`.git/`)
- **Remote Repository:** servidor (GitHub, GitLab, Bitbucket)

### Comandos essenciais

```bash
# Configuração
git config --global user.name "Josenaldo"
git config --global user.email "josenaldo@email.com"

# Iniciar / clonar
git init
git clone https://github.com/user/repo.git

# Status e diff
git status                     # estado atual
git diff                       # mudanças não staged
git diff --staged              # mudanças staged (prontas pro commit)
git log --oneline -10          # últimos 10 commits
git log --graph --oneline      # histórico visual

# Stage e commit
git add file.txt               # stage arquivo específico
git add .                      # stage tudo (cuidado!)
git commit -m "feat: add login"
git commit --amend             # editar último commit (antes de push!)

# Branches
git branch                     # listar branches
git branch feature/login       # criar branch
git checkout feature/login     # mudar para branch
git checkout -b feature/login  # criar e mudar (atalho)
git switch feature/login       # mudar (Git 2.23+)
git switch -c feature/login    # criar e mudar (Git 2.23+)

# Merge e rebase
git merge feature/login        # merge branch no atual
git rebase main                # reaplica commits sobre main

# Remote
git push origin feature/login
git push -u origin feature/login  # set upstream
git pull                       # fetch + merge
git fetch                      # baixar sem merge

# Desfazer
git restore file.txt           # descartar mudanças no working dir
git restore --staged file.txt  # unstage (manter mudanças)
git reset --soft HEAD~1        # desfaz commit, mantém staged
git reset --mixed HEAD~1       # desfaz commit, mantém no working dir
git reset --hard HEAD~1        # desfaz commit e descarta tudo (⚠️ destrutivo)
git revert abc123              # cria commit que desfaz outro (seguro)

# Stash
git stash                      # guardar mudanças temporariamente
git stash pop                  # restaurar e remover do stash
git stash list                 # listar stashes
git stash apply stash@{0}      # restaurar sem remover

# Tags
git tag v1.0.0                 # tag leve
git tag -a v1.0.0 -m "Release 1.0.0"  # tag anotada
git push origin v1.0.0
```

### Merge vs Rebase

| Aspecto | Merge | Rebase |
| --- | --- | --- |
| Histórico | Preserva (merge commit) | Linear (reescreve) |
| Quando usar | Branch compartilhada, PRs | Branch local, limpeza |
| Segurança | Sempre seguro | ⚠️ Não rebase branches publicadas |
| Conflitos | Resolve uma vez | Resolve por commit |

**Regra de ouro:** nunca rebase em branches que outros usam. Rebase na branch local antes de abrir PR para manter histórico limpo.

### Resolução de conflitos

```text
<<<<<<< HEAD
código da sua branch
=======
código da branch que está entrando
>>>>>>> feature/login
```

1. Abrir arquivo com conflito
2. Escolher qual versão manter (ou combinar)
3. Remover marcadores (`<<<<<<<`, `=======`, `>>>>>>>`)
4. Stage e commit

**Dica:** usar `git mergetool` ou o resolver do VS Code/IntelliJ.

## Workflows

### Git Flow

```text
main ──────────────────────────────────────────
  └── develop ─────────────────────────────────
       ├── feature/login ──── merge → develop
       ├── feature/signup ─── merge → develop
       └── release/1.0 ───── merge → main + develop
                                └── tag v1.0.0
```

Branches: `main`, `develop`, `feature/*`, `release/*`, `hotfix/*`. Bom para releases planejadas.

### GitHub Flow (simplificado)

```text
main ──────────────────────────────────────
  └── feature/login ─── PR → review → merge → main
```

Só `main` + feature branches + PRs. Deploy contínuo. Mais simples, mais comum em startups.

### Trunk-Based Development

Todos commitam direto na `main` (ou branches muito curtas). Requer: feature flags, CI robusto, testes automatizados. Usado por Google, Meta.

## Conventional Commits

Padrão para mensagens de commit semânticas:

```text
<tipo>[escopo opcional]: <descrição>

[corpo opcional]

[rodapé opcional]
```

**Tipos:**

| Tipo | Quando usar |
| --- | --- |
| `feat` | Nova funcionalidade |
| `fix` | Correção de bug |
| `docs` | Documentação |
| `style` | Formatação (sem mudança de lógica) |
| `refactor` | Refatoração (sem mudar comportamento) |
| `test` | Adicionar/corrigir testes |
| `chore` | Manutenção (build, deps, configs) |
| `perf` | Melhoria de performance |
| `ci` | Mudanças de CI/CD |

**Exemplos:**

```text
feat: add patient search by specialty
fix: resolve N+1 query in appointment listing
refactor: extract notification service from controller
docs: add API documentation for patient endpoints
chore: upgrade Spring Boot to 3.2.0
feat!: change authentication from session to JWT

BREAKING CHANGE: session-based auth removed
```

**Benefícios:** changelogs automáticos, semantic versioning automático, histórico legível.

> **Fonte:** [Conventional Commits](https://www.conventionalcommits.org/en/v1.0.0/)

## Boas práticas

- **Commits atômicos:** cada commit faz uma coisa. Revertível individualmente.
- **Branch por feature:** nunca commitar direto na main. Sempre PR + review.
- **Pull antes de push:** `git pull --rebase` para evitar merge commits desnecessários.
- **`.gitignore`:** nunca commitar `node_modules/`, `.env`, `target/`, credentials.
- **Mensagens claras:** "fix: resolve timeout on patient search" > "fixed stuff"
- **Squash antes de merge:** limpar commits de "wip", "fix typo" antes de mergear.
- **Proteger main:** require PR reviews, status checks, no force push.

## Armadilhas comuns

- **Force push em branch compartilhada:** reescreve histórico de outros. Usar `--force-with-lease` se necessário.
- **Commitar secrets:** `.env`, API keys, passwords. Se acontecer, rotacionar imediatamente (git history guarda tudo).
- **Merge commits desnecessários:** usar `git pull --rebase` para manter histórico linear.
- **Branch stale:** branches abertas há semanas divergem muito. Rebase frequente.
- **Não entender `reset` vs `revert`:** `reset` reescreve histórico (local), `revert` cria commit novo (seguro para branches publicadas).

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

## Git Clients

- **CLI (terminal)** — mais poderoso, mais rápido
- **VS Code** — Git integrado com diff visual
- **IntelliJ IDEA** — Git integrado com resolve de conflitos excelente
- [Sourcetree](https://www.sourcetreeapp.com/) — GUI gratuito para Mac/Windows
- [GitKraken](https://www.gitkraken.com/) — GUI visual popular

## Recursos

- [Aprendendo Git e Github](https://josenaldo.github.io/aprendendo-git-e-github/) — guia pessoal
- [Conventional Commits](https://www.conventionalcommits.org/en/v1.0.0/) — especificação
- [Git Documentation](https://git-scm.com/doc) — referência oficial
- [Learn Git Branching](https://learngitbranching.js.org/) — exercícios interativos

## Veja também

- [[Terminal]]
- [[Docker]]
