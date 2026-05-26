---
title: "GitHub CLI"
created: 2026-04-12
updated: 2026-04-12
type: concept
status: evergreen
tags:
  - infraestrutura
  - devops
  - ferramentas
publish: true
---

# GitHub CLI

Deep dive no **GitHub CLI (`gh`)** — a ferramenta de linha de comando oficial do GitHub. Repos, PRs, issues, Actions, secrets, Pages, releases, gists, API direta, e automação. Para CI/CD em geral, ver [[CI-CD]]. Para containers, ver [[Docker]]. Para terminal, ver [[Terminal]].

## O que é

`gh` é o **CLI oficial do GitHub**, lançado em 2020. Permite fazer praticamente tudo que você faz na interface web — sem sair do terminal. Criar repos, abrir PRs, rodar workflows, configurar secrets, debugar deploys, até configurar GitHub Pages via API.

**Por que usar `gh` ao invés da web UI:**

- **Velocidade** — criar um PR em 5 segundos, não 30 cliques
- **Automação** — scripting, CI/CD, deploys automatizados
- **Contexto** — você já está no terminal, no diretório do projeto
- **Composição** — pipe com `jq`, `grep`, `awk`, shell scripts
- **Reprodutibilidade** — um comando documentado > "clica ali, depois ali"

```
┌──────────────────────────────────────────────────┐
│  Seu terminal                                    │
│                                                  │
│  $ gh repo create meu-projeto --public --push    │
│  $ gh secret set DEPLOY_TOKEN < token.txt        │
│  $ gh workflow run deploy.yml                    │
│  $ gh run watch --exit-status                    │
│                                                  │
│  ✓ Repo criado, secret configurado, deploy       │
│    rodando — tudo sem abrir o browser            │
└──────────────────────────────────────────────────┘
```

### Instalação

**Linux (Debian/Ubuntu):**

```bash
# Via apt (repositório oficial)
sudo apt install gh

# Ou via Homebrew
brew install gh
```

**macOS:**

```bash
brew install gh
```

**Windows:**

```bash
# Via winget
winget install --id GitHub.cli

# Via scoop
scoop install gh

# Via choco
choco install gh
```

**Verificando a instalação:**

```bash
gh --version
# gh version 2.x.x (20xx-xx-xx)
```

---

## Autenticação

Antes de qualquer coisa, precisa autenticar. Sem isso, nada funciona.

### gh auth login

```bash
gh auth login
```

Interativo — vai perguntar:

1. **GitHub.com ou Enterprise?** — escolha o host
2. **HTTPS ou SSH?** — SSH é mais prático no dia a dia
3. **Autenticar via browser ou token?** — browser é mais fácil

```bash
# Login direto com opções
gh auth login --hostname github.com --git-protocol ssh --web

# Login com token (útil em CI/CD)
echo $GH_TOKEN | gh auth login --with-token
```

### gh auth status

Verifica se está autenticado e com quais escopos:

```bash
gh auth status
```

Saída típica:

```
github.com
  ✓ Logged in to github.com account josenaldo (keyring)
  - Active account: true
  - Git operations protocol: ssh
  - Token: gho_************************************
  - Token scopes: 'admin:public_key', 'gist', 'read:org', 'repo', 'workflow'
```

### gh auth token

Imprime o token atual — útil para usar em scripts:

```bash
gh auth token
# gho_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
```

### gh auth refresh

Adiciona escopos extras ao token existente:

```bash
# Precisa de escopo para deletar repos? Adiciona sem refazer login
gh auth refresh --scopes delete_repo
```

### gh auth logout

```bash
gh auth logout
```

### Autenticação em CI/CD

Em ambientes automatizados, use a variável de ambiente:

```bash
export GH_TOKEN="ghp_xxxxxxxxxxxxxxxxxxxx"

# Ou
export GITHUB_TOKEN="ghp_xxxxxxxxxxxxxxxxxxxx"
```

O `gh` detecta automaticamente. Muito usado em GitHub Actions:

```yaml
- name: Create PR
  env:
    GH_TOKEN: ${{ secrets.GITHUB_TOKEN }}
  run: gh pr create --title "Auto PR" --body "Gerado via CI"
```

---

## Repositórios

### gh repo create

O comando que você mais vai usar no início de um projeto. Cria o repo no GitHub e já conecta com o diretório local.

**Sintaxe:**

```bash
gh repo create [<name>] [flags]
```

**Flags principais:**

| Flag               | Descrição                          |
| ------------------ | ---------------------------------- |
| `--public`         | Repo público                       |
| `--private`        | Repo privado                       |
| `--internal`       | Repo interno (orgs)                |
| `--source <dir>`   | Diretório local como fonte         |
| `--remote <name>`  | Nome do remote (default: `origin`) |
| `--push`           | Faz push do código após criar      |
| `--clone`          | Clona o repo após criar            |
| `--description`    | Descrição do repo                  |
| `--gitignore`      | Template de .gitignore             |
| `--license`        | Licença (MIT, Apache-2.0, etc.)    |
| `--disable-wiki`   | Desabilita wiki                    |
| `--disable-issues` | Desabilita issues                  |

**Cenários reais:**

```bash
# Cenário 1: Criando repo a partir de diretório local existente
cd meu-projeto
git init
git add .
git commit -m "Initial commit"
gh repo create meu-projeto --public --source . --remote origin --push

# Cenário 2: Repo novo vazio (depois clona)
gh repo create meu-projeto --public --clone

# Cenário 3: Repo privado com descrição
gh repo create meu-projeto --private --description "Meu projeto secreto"

# Cenário 4: Repo a partir de template
gh repo create meu-novo-site --template user/template-repo --public --clone

# Cenário 5: Dentro de uma organização
gh repo create minha-org/projeto --public --source . --push
```

**Exemplo completo — fluxo real com degit:**

```bash
# Cria projeto a partir de template (sem histórico git)
npx degit user/template-astro meu-site
cd meu-site

# Inicializa git
git init
git add .
git commit -m "feat: initial commit from template"

# Cria repo no GitHub e faz push
gh repo create meu-site --public --source . --remote origin --push
```

Saída:

```
✓ Created repository josenaldo/meu-site on GitHub
  https://github.com/josenaldo/meu-site
✓ Added remote https://github.com/josenaldo/meu-site.git
✓ Pushed commits to https://github.com/josenaldo/meu-site.git
```

### gh repo clone

```bash
# Clone por nome (se for seu repo ou de um org que você pertence)
gh repo clone meu-projeto

# Clone por owner/repo
gh repo clone josenaldo/meu-projeto

# Clone por URL
gh repo clone https://github.com/josenaldo/meu-projeto

# Clone em diretório específico
gh repo clone josenaldo/meu-projeto ./pasta-destino

# Clone com opções extras do git
gh repo clone josenaldo/meu-projeto -- --depth 1
```

### gh repo fork

Faz fork e já clona:

```bash
# Fork + clone
gh repo fork owner/repo --clone

# Fork sem clone (só cria no GitHub)
gh repo fork owner/repo

# Fork em uma organização
gh repo fork owner/repo --org minha-org
```

### gh repo view

Mostra info do repo sem abrir o browser:

```bash
# Repo atual (diretório onde você está)
gh repo view

# Repo específico
gh repo view josenaldo/meu-projeto

# Abrir no browser
gh repo view --web

# Formato JSON (para scripts)
gh repo view --json name,url,defaultBranchRef
```

### gh repo list

Lista seus repos:

```bash
# Seus repos
gh repo list

# Repos de uma org
gh repo list minha-org

# Filtros
gh repo list --public --language python --limit 20

# JSON para scripts
gh repo list --json name,url,isPrivate --limit 50
```

### gh repo delete

```bash
# Cuidado! Sem volta
gh repo delete josenaldo/repo-teste --yes
```

### gh repo edit

```bash
# Mudar descrição
gh repo edit --description "Nova descrição"

# Habilitar/desabilitar features
gh repo edit --enable-wiki=false --enable-issues=true

# Mudar visibilidade
gh repo edit --visibility public
```

---

## Pull Requests

O ciclo de vida completo de PRs, direto do terminal.

### gh pr create

```bash
# Interativo (vai perguntar título, body, etc.)
gh pr create

# Com título e body inline
gh pr create --title "feat: adicionar autenticação OAuth" \
  --body "Implementa login via Google e GitHub OAuth2"

# PR de uma branch específica para outra
gh pr create --base main --head feature/auth \
  --title "feat: autenticação OAuth" \
  --body "## Mudanças
- Login via Google OAuth2
- Login via GitHub OAuth2
- Testes unitários"

# PR como draft
gh pr create --draft --title "WIP: nova feature"

# PR com reviewers e labels
gh pr create --title "fix: memory leak" \
  --reviewer josenaldo,outro-dev \
  --label bug,priority-high

# PR com assignee
gh pr create --title "feat: dashboard" --assignee @me

# Abrir editor para escrever o body
gh pr create --title "feat: algo grande" --body-file changelog.md
```

### gh pr list

```bash
# PRs abertas
gh pr list

# Todas (incluindo fechadas/merged)
gh pr list --state all

# Filtros
gh pr list --author josenaldo
gh pr list --label bug
gh pr list --base main
gh pr list --search "is:open review:required"

# Saída JSON
gh pr list --json number,title,author,state --limit 20
```

Saída típica:

```
Showing 3 of 3 open pull requests in josenaldo/meu-projeto

ID    TITLE                       BRANCH          CREATED AT
#12   feat: autenticação OAuth    feature/auth    about 2 hours ago
#11   fix: memory leak            fix/mem-leak    about 1 day ago
#10   docs: atualizar README      docs/readme     about 3 days ago
```

### gh pr view

```bash
# PR do branch atual
gh pr view

# PR específica por número
gh pr view 12

# Abrir no browser
gh pr view 12 --web

# JSON (para scripts)
gh pr view 12 --json title,body,state,reviews,statusCheckRollup

# Ver comments
gh pr view 12 --comments
```

### gh pr checkout

Faz checkout da branch de uma PR — essencial para code review local:

```bash
# Checkout por número
gh pr checkout 12

# Checkout por branch
gh pr checkout feature/auth

# Checkout com detach (sem criar branch local)
gh pr checkout 12 --detach
```

### gh pr review

```bash
# Aprovar
gh pr review 12 --approve

# Aprovar com comentário
gh pr review 12 --approve --body "LGTM! Boa implementação."

# Pedir changes
gh pr review 12 --request-changes --body "Faltou tratamento de erro no login"

# Comentar (sem aprovar ou rejeitar)
gh pr review 12 --comment --body "Pergunta: por que usar OAuth e não OIDC?"
```

### gh pr diff

Vê o diff sem fazer checkout:

```bash
# Diff da PR atual
gh pr diff

# Diff de PR específica
gh pr diff 12

# Só nomes de arquivos alterados
gh pr diff 12 --name-only
```

### gh pr merge

```bash
# Merge interativo
gh pr merge 12

# Merge commit (padrão do GitHub)
gh pr merge 12 --merge

# Squash merge
gh pr merge 12 --squash

# Rebase merge
gh pr merge 12 --rebase

# Auto-merge (espera checks passarem)
gh pr merge 12 --auto --squash

# Deletar branch após merge
gh pr merge 12 --squash --delete-branch

# Sem confirmação
gh pr merge 12 --squash --delete-branch --yes
```

### gh pr close / reopen

```bash
gh pr close 12
gh pr close 12 --comment "Não vamos implementar isso agora"
gh pr reopen 12
```

### gh pr edit

```bash
gh pr edit 12 --title "Novo título"
gh pr edit 12 --add-label bug --add-reviewer josenaldo
gh pr edit 12 --base develop
```

---

## Issues

### gh issue create

```bash
# Interativo
gh issue create

# Com título e body
gh issue create --title "Bug: login falha no Safari" \
  --body "## Descrição
Safari 17+ não processa o callback OAuth.

## Passos para reproduzir
1. Abrir app no Safari
2. Clicar em Login
3. Tela fica branca

## Esperado
Redirect para dashboard"

# Com labels e assignee
gh issue create --title "feat: dark mode" \
  --label enhancement,ui \
  --assignee @me

# Issue a partir de arquivo
gh issue create --title "Bug report" --body-file bug-report.md
```

### gh issue list

```bash
# Issues abertas
gh issue list

# Filtros
gh issue list --state closed
gh issue list --label bug
gh issue list --assignee @me
gh issue list --milestone "v2.0"
gh issue list --search "is:open label:bug sort:created-asc"

# JSON
gh issue list --json number,title,labels,assignees --limit 50
```

### gh issue view

```bash
# Ver issue
gh issue view 42

# No browser
gh issue view 42 --web

# Com comentários
gh issue view 42 --comments

# JSON
gh issue view 42 --json title,body,comments
```

### gh issue close / reopen

```bash
gh issue close 42
gh issue close 42 --comment "Resolvido na PR #12"
gh issue close 42 --reason "not planned"
gh issue reopen 42
```

### gh issue edit

```bash
gh issue edit 42 --title "Novo título"
gh issue edit 42 --add-label priority-high
gh issue edit 42 --remove-label wontfix
gh issue edit 42 --add-assignee josenaldo
```

### gh issue comment

```bash
gh issue comment 42 --body "Investigando agora. Parece ser problema de CORS."
```

---

## GitHub Actions

Aqui é onde `gh` **brilha de verdade**. Gerenciar workflows, secrets, e debugar runs — tudo do terminal, sem ficar clicando na aba Actions.

### gh workflow list

Lista os workflows do repo:

```bash
gh workflow list
```

Saída:

```
NAME                 STATUS   ID
Deploy to Pages      active   12345678
CI Tests             active   12345679
Release              active   12345680
```

### gh workflow view

```bash
# Ver detalhes de um workflow
gh workflow view "Deploy to Pages"

# Por ID
gh workflow view 12345678

# Ver o YAML do workflow
gh workflow view "Deploy to Pages" --yaml
```

### gh workflow run

**Dispara um workflow manualmente** — essencial para deploys on-demand:

```bash
# Disparar pelo nome
gh workflow run "Deploy to Pages"

# Disparar pelo arquivo
gh workflow run deploy.yml

# Disparar com inputs (para workflows que aceitam workflow_dispatch inputs)
gh workflow run deploy.yml -f environment=production -f version=v2.1.0

# Disparar em branch específica
gh workflow run deploy.yml --ref feature/nova-feature

# Disparar em outro repo
gh workflow run deploy.yml --repo josenaldo/meu-site
```

**Exemplo de workflow que aceita dispatch:**

```yaml
# .github/workflows/deploy.yml
name: Deploy to Pages
on:
  push:
    branches: [main]
  workflow_dispatch:
    inputs:
      environment:
        description: 'Ambiente de deploy'
        required: true
        default: 'production'
        type: choice
        options:
          - staging
          - production
```

### gh run list

Lista as execuções recentes:

```bash
# Últimas runs
gh run list

# Filtrar por workflow
gh run list --workflow deploy.yml

# Filtrar por status
gh run list --status failure
gh run list --status success

# Filtrar por branch
gh run list --branch main

# Limitar resultados
gh run list --limit 5

# JSON
gh run list --json databaseId,status,conclusion,name,createdAt --limit 10
```

Saída típica:

```
STATUS  TITLE                  WORKFLOW         BRANCH  EVENT              ID          ELAPSED  AGE
✓       feat: update config    Deploy to Pages  main    push               12345678    2m30s    5m
✗       fix: typo              CI Tests         main    push               12345677    1m12s    1h
*       docs: readme           Deploy to Pages  main    workflow_dispatch  12345676    0m45s    2m
```

Legenda: `✓` = sucesso, `✗` = falha, `*` = em andamento

### gh run view

Ver detalhes de uma run específica:

```bash
# Por ID
gh run view 12345678

# Ver logs da run
gh run view 12345678 --log

# Ver APENAS logs de jobs que falharam (muito útil para debug!)
gh run view 12345678 --log-failed

# Ver no browser
gh run view 12345678 --web

# JSON com detalhes
gh run view 12345678 --json jobs,status,conclusion
```

**`--log-failed` é ouro puro para debugging.** Ao invés de abrir o browser e clicar em cada step procurando o erro, o comando já filtra e mostra só o que falhou:

```bash
gh run view 12345678 --log-failed
```

Saída:

```
deploy   deploy   2026-04-12T10:30:15.1234567Z Error: Resource not accessible by integration
deploy   deploy   2026-04-12T10:30:15.2345678Z   Ensure GITHUB_TOKEN has 'pages: write' permission
```

### gh run watch

**Assiste uma run em tempo real** — como `tail -f` para o Actions:

```bash
# Watch da última run
gh run watch

# Watch de run específica
gh run watch 12345678

# Watch com exit status (retorna 0 se sucesso, 1 se falha)
# Perfeito para scripts!
gh run watch --exit-status
```

**`--exit-status` é essencial para automação.** O comando bloqueia até a run terminar e retorna o exit code:

```bash
# Dispara e espera
gh workflow run deploy.yml
sleep 3  # Espera a run aparecer
gh run watch --exit-status

# Se falhar, o script para (com set -e)
echo "Deploy concluído com sucesso!"
```

### gh run rerun

Reroda uma run que falhou:

```bash
# Reroda tudo
gh run rerun 12345678

# Reroda só os jobs que falharam
gh run rerun 12345678 --failed

# Em modo debug (mais logs)
gh run rerun 12345678 --debug
```

### gh run cancel

```bash
gh run cancel 12345678
```

### Secrets — gh secret set / list / delete

Secrets são variáveis sensíveis usadas nos workflows. **Nunca coloque tokens, senhas ou chaves diretamente no código.**

#### gh secret set

```bash
# Set interativo (vai pedir o valor)
gh secret set MY_SECRET

# Set a partir de valor inline
gh secret set MY_SECRET --body "meu-valor-secreto"

# Set a partir de arquivo (mais seguro — não fica no histórico do shell)
gh secret set DEPLOY_TOKEN < token.txt

# Set a partir de pipe
echo "meu-valor" | gh secret set MY_SECRET

# Set em repo específico
gh secret set MY_SECRET --repo josenaldo/meu-projeto --body "valor"

# Set para um environment específico
gh secret set MY_SECRET --env production --body "valor-prod"

# Set em nível de organização
gh secret set ORG_SECRET --org minha-org --body "valor"

# Set com visibilidade na org
gh secret set ORG_SECRET --org minha-org \
  --visibility selected \
  --repos repo1,repo2,repo3
```

**Exemplo real — configurando cross-repo dispatch token:**

```bash
# Gera um Personal Access Token (PAT) com escopo 'repo' e 'workflow'
# Depois seta como secret
gh secret set CROSS_REPO_TOKEN < pat-token.txt
```

Esse token é usado em workflows para disparar ações em outros repos:

```yaml
# No workflow do repo de conteúdo
- name: Trigger site rebuild
  uses: peter-evans/repository-dispatch@v3
  with:
    token: ${{ secrets.CROSS_REPO_TOKEN }}
    repository: josenaldo/meu-site
    event-type: content-update
```

#### gh secret list

```bash
# Listar secrets do repo
gh secret list

# Listar secrets de um environment
gh secret list --env production

# Listar secrets de uma org
gh secret list --org minha-org
```

Saída:

```
NAME               UPDATED
CROSS_REPO_TOKEN   about 2 hours ago
DEPLOY_KEY         about 1 day ago
NPM_TOKEN          about 1 month ago
```

**Nota:** `gh secret list` mostra **nomes e datas**, nunca os valores. Uma vez setado, o valor do secret não pode ser lido — só sobrescrito.

#### gh secret delete

```bash
gh secret delete MY_SECRET
gh secret delete MY_SECRET --env production
```

### Variables — gh variable set / list / delete

Variables são como secrets, mas **não são sensíveis** — os valores aparecem nos logs:

```bash
gh variable set SITE_URL --body "https://meu-site.com"
gh variable list
gh variable delete SITE_URL
```

---

## GitHub Pages

Configurar GitHub Pages via CLI é feito com `gh api`, já que não existe um subcomando dedicado.

### Habilitando GitHub Pages via API

```bash
# Configura Pages para usar GitHub Actions como source
gh api repos/OWNER/REPO/pages \
  -X POST \
  --input - <<EOF
{
  "source": {
    "branch": "main",
    "path": "/"
  },
  "build_type": "workflow"
}
EOF
```

**Exemplo real — configurando Pages para um site Astro:**

```bash
# Habilita Pages com source = GitHub Actions
gh api repos/josenaldo/meu-site/pages \
  -X POST \
  --input - <<EOF
{
  "build_type": "workflow"
}
EOF
```

Saída:

```json
{
  "url": "https://josenaldo.github.io/meu-site/",
  "status": "built",
  "build_type": "workflow",
  "source": {
    "branch": "main",
    "path": "/"
  }
}
```

### Verificando configuração de Pages

```bash
gh api repos/OWNER/REPO/pages
```

### Atualizando configuração

```bash
gh api repos/OWNER/REPO/pages \
  -X PUT \
  --input - <<EOF
{
  "build_type": "workflow",
  "source": {
    "branch": "main",
    "path": "/"
  }
}
EOF
```

### Custom domain

```bash
# Configurar domínio customizado
gh api repos/OWNER/REPO/pages \
  -X PUT \
  -f cname="meu-dominio.com"

# Forçar HTTPS
gh api repos/OWNER/REPO/pages \
  -X PUT \
  -F https_enforced=true
```

---

## Releases

### gh release create

```bash
# Release a partir de uma tag
gh release create v1.0.0

# Com título e notas
gh release create v1.0.0 \
  --title "v1.0.0 - Primeiro release" \
  --notes "## Novidades
- Feature A
- Feature B

## Correções
- Fix C"

# Gerar notas automaticamente (baseado nos commits desde última tag)
gh release create v1.0.0 --generate-notes

# Pre-release
gh release create v2.0.0-beta.1 --prerelease --generate-notes

# Draft (não publica ainda)
gh release create v1.0.0 --draft --generate-notes

# Com assets (binários, zips, etc.)
gh release create v1.0.0 ./dist/app-linux-amd64 ./dist/app-darwin-amd64

# Com notas de um arquivo
gh release create v1.0.0 --notes-file CHANGELOG.md

# Apontando para branch específica
gh release create v1.0.0 --target main
```

### gh release list

```bash
gh release list

# Incluindo drafts
gh release list --exclude-drafts=false

# Limitar
gh release list --limit 5
```

### gh release view

```bash
gh release view v1.0.0

# No browser
gh release view v1.0.0 --web
```

### gh release download

```bash
# Download de todos os assets
gh release download v1.0.0

# Asset específico
gh release download v1.0.0 --pattern "*.tar.gz"

# Para diretório específico
gh release download v1.0.0 --dir ./downloads

# Última release
gh release download --pattern "*.zip"
```

### gh release delete

```bash
gh release delete v1.0.0 --yes

# Deletar release e a tag
gh release delete v1.0.0 --yes --cleanup-tag
```

---

## Gists

### gh gist create

```bash
# Criar gist público de um arquivo
gh gist create script.sh

# Gist privado (secret)
gh gist create --public=false script.sh

# Com descrição
gh gist create -d "Script útil para backup" script.sh

# Múltiplos arquivos
gh gist create file1.py file2.py file3.py

# A partir de stdin
echo '{"key": "value"}' | gh gist create --filename config.json

# Abrir no browser após criar
gh gist create --web script.sh
```

### gh gist list

```bash
gh gist list

# Filtrar por visibilidade
gh gist list --public
gh gist list --secret

# Limitar
gh gist list --limit 10
```

### gh gist view / edit / delete

```bash
# Ver conteúdo
gh gist view GIST_ID

# Editar (abre editor)
gh gist edit GIST_ID

# Adicionar arquivo ao gist
gh gist edit GIST_ID --add novo-arquivo.txt

# Deletar
gh gist delete GIST_ID
```

---

## API direta — gh api

Quando não existe um subcomando para o que você precisa, `gh api` resolve. É um **curl autenticado** para a API REST (e GraphQL) do GitHub.

### REST API

```bash
# GET (padrão)
gh api repos/josenaldo/meu-projeto

# Com query parameters
gh api repos/josenaldo/meu-projeto/commits --jq '.[0].sha'

# POST
gh api repos/josenaldo/meu-projeto/dispatches \
  -X POST \
  -f event_type="deploy"

# POST com body JSON
gh api repos/josenaldo/meu-projeto/issues \
  -X POST \
  -f title="Bug encontrado" \
  -f body="Descrição do bug"

# PUT
gh api repos/josenaldo/meu-projeto/topics \
  -X PUT \
  --input - <<EOF
{"names": ["astro", "blog", "portfolio"]}
EOF

# DELETE
gh api repos/josenaldo/meu-projeto/pages -X DELETE

# Paginação automática
gh api repos/josenaldo/meu-projeto/issues --paginate

# Campos específicos com jq
gh api repos/josenaldo/meu-projeto --jq '.stargazers_count'
```

### GraphQL API

```bash
# Query simples
gh api graphql -f query='
  query {
    viewer {
      login
      repositories(first: 5, orderBy: {field: UPDATED_AT, direction: DESC}) {
        nodes {
          name
          url
          stargazerCount
        }
      }
    }
  }
'

# Com variáveis
gh api graphql -f query='
  query($owner: String!, $name: String!) {
    repository(owner: $owner, name: $name) {
      issues(first: 10, states: OPEN) {
        nodes {
          title
          number
          createdAt
        }
      }
    }
  }
' -f owner="josenaldo" -f name="meu-projeto"
```

### Flags úteis do gh api

| Flag                | Descrição                                   |
| ------------------- | ------------------------------------------- |
| `-X METHOD`         | Método HTTP (GET, POST, PUT, DELETE, PATCH) |
| `-f key=value`      | Campo string no body JSON                   |
| `-F key=value`      | Campo tipado (detecta int, bool, null)      |
| `--input -`         | Lê body JSON de stdin                       |
| `--input file.json` | Lê body JSON de arquivo                     |
| `--jq <expr>`       | Filtra output com jq                        |
| `--paginate`        | Paginação automática                        |
| `-H key:value`      | Header customizado                          |
| `--hostname`        | Para GitHub Enterprise                      |
| `-t template`       | Go template para formatação                 |

### Exemplos práticos

```bash
# Ver rate limit
gh api rate_limit --jq '.rate'

# Listar collaborators
gh api repos/OWNER/REPO/collaborators --jq '.[].login'

# Habilitar branch protection
gh api repos/OWNER/REPO/branches/main/protection \
  -X PUT \
  --input - <<EOF
{
  "required_status_checks": {
    "strict": true,
    "contexts": ["ci/tests"]
  },
  "enforce_admins": true,
  "required_pull_request_reviews": {
    "required_approving_review_count": 1
  },
  "restrictions": null
}
EOF

# Disparar repository_dispatch (cross-repo trigger)
gh api repos/OWNER/REPO/dispatches \
  -X POST \
  -f event_type="deploy" \
  -f 'client_payload[ref]=main'

# Ver comentários de uma PR
gh api repos/OWNER/REPO/pulls/123/comments --jq '.[].body'

# Listar GitHub Actions artifacts
gh api repos/OWNER/REPO/actions/artifacts --jq '.artifacts[].name'
```

---

## Configuração e personalização

### gh config set

```bash
# Editor padrão
gh config set editor "code --wait"
gh config set editor vim

# Protocolo git padrão
gh config set git_protocol ssh

# Browser padrão
gh config set browser "firefox"

# Prompt para PRs
gh config set prompt disabled

# Pager
gh config set pager "less -R"
```

### gh config get

```bash
gh config get editor
gh config get git_protocol
```

### gh config list

```bash
gh config list
```

### gh alias set

Cria atalhos para comandos frequentes:

```bash
# Alias simples
gh alias set pv "pr view"
gh alias set co "pr checkout"

# Alias com flags
gh alias set my-prs "pr list --author @me"
gh alias set my-issues "issue list --assignee @me"

# Alias complexo (shell command)
gh alias set --shell pr-stats 'gh pr list --json number,title,additions,deletions | jq ".[] | {number, title, lines: (.additions + .deletions)}"'

# Alias para workflow
gh alias set deploy "workflow run deploy.yml"
gh alias set watch-deploy "run watch --exit-status"

# Alias para log de falhas
gh alias set why-fail "run view --log-failed"
```

Depois de criar:

```bash
gh deploy                    # = gh workflow run deploy.yml
gh watch-deploy              # = gh run watch --exit-status
gh why-fail 12345678         # = gh run view 12345678 --log-failed
gh my-prs                    # = gh pr list --author @me
```

### gh alias list

```bash
gh alias list
```

### gh alias delete

```bash
gh alias delete pv
```

---

## Extensions — gh extension

Extensions são plugins que adicionam comandos ao `gh`.

### Instalar extensions

```bash
# Instalar
gh extension install dlvhdr/gh-dash      # Dashboard TUI para PRs e issues
gh extension install mislav/gh-branch     # Branch management
gh extension install vilmibm/gh-screensaver  # Diversão
gh extension install github/gh-copilot    # GitHub Copilot no terminal

# Instalar de URL
gh extension install https://github.com/owner/gh-extension
```

### Gerenciar extensions

```bash
# Listar instaladas
gh extension list

# Atualizar todas
gh extension upgrade --all

# Atualizar uma
gh extension upgrade dlvhdr/gh-dash

# Remover
gh extension remove dlvhdr/gh-dash
```

### Extensions recomendadas

- **`gh-dash`** — dashboard TUI, visualiza PRs e issues de vários repos
- **`gh-copilot`** — GitHub Copilot no terminal, sugere comandos
- **`gh-branch`** — gerenciamento de branches com fuzzy search
- **`gh-poi`** — limpa branches locais já merged

---

## SSH Keys

```bash
# Adicionar chave SSH pública
gh ssh-key add ~/.ssh/id_ed25519.pub --title "Meu notebook"

# Listar chaves
gh ssh-key list

# Deletar
gh ssh-key delete KEY_ID
```

---

## Codespaces

Codespaces são ambientes de dev na cloud. `gh codespace` gerencia tudo do terminal:

```bash
# Criar codespace
gh codespace create --repo josenaldo/meu-projeto

# Com machine type específico
gh codespace create --repo josenaldo/meu-projeto --machine largePremiumLinux

# Listar codespaces
gh codespace list

# Conectar via SSH
gh codespace ssh

# Abrir no VS Code
gh codespace code

# Ver logs
gh codespace logs

# Parar codespace (economiza créditos)
gh codespace stop

# Deletar
gh codespace delete

# Port forwarding
gh codespace ports forward 3000:3000
```

---

## gh browse

Abre coisas no browser rapidamente:

```bash
# Repo atual
gh browse

# Arquivo específico
gh browse src/main.py

# Linha específica
gh browse src/main.py:42

# Settings
gh browse --settings

# Issues
gh browse --issues

# Wiki
gh browse --wiki

# Projects
gh browse --projects

# Repo específico
gh browse --repo josenaldo/meu-projeto
```

---

## Fluxo real: Deploy automático com gh

Este é um fluxo completo que combina vários comandos `gh` para montar um sistema de deploy automático — repo de conteúdo que dispara rebuild de um site estático.

### 1. Criar o repo do site a partir de template

```bash
# Cria o projeto a partir de um template (ex: Astro)
npx degit withastro/astro-starter meu-site
cd meu-site

# Inicializa git e faz primeiro commit
git init
git add .
git commit -m "feat: initial commit from Astro template"

# Cria repo público no GitHub e faz push
gh repo create meu-site --public --source . --remote origin --push
```

### 2. Criar o workflow de deploy

Cria `.github/workflows/deploy.yml`:

```yaml
name: Deploy to Pages

on:
  push:
    branches: [main]
  workflow_dispatch:
  repository_dispatch:
    types: [content-update]

permissions:
  contents: read
  pages: write
  id-token: write

concurrency:
  group: "pages"
  cancel-in-progress: true

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with:
          node-version: 20
          cache: npm
      - run: npm ci
      - run: npm run build
      - uses: actions/upload-pages-artifact@v3
        with:
          path: ./dist

  deploy:
    needs: build
    runs-on: ubuntu-latest
    environment:
      name: github-pages
      url: ${{ steps.deployment.outputs.page_url }}
    steps:
      - uses: actions/deploy-pages@v4
        id: deployment
```

```bash
git add .github/
git commit -m "ci: add deploy workflow"
git push
```

### 3. Configurar GitHub Pages via API

```bash
# Habilita Pages com GitHub Actions como source
gh api repos/josenaldo/meu-site/pages \
  -X POST \
  --input - <<EOF
{
  "build_type": "workflow"
}
EOF
```

### 4. Verificar que o primeiro deploy rodou

```bash
# Lista as runs recentes
gh run list --limit 3

# Assiste a run em tempo real
gh run watch --exit-status
```

Se falhou:

```bash
# Pega o ID da run que falhou
gh run list --status failure --limit 1

# Vê os logs de erro
gh run view <RUN_ID> --log-failed
```

### 5. Configurar secrets para cross-repo dispatch

No repo de **conteúdo** (que vai disparar rebuilds do site):

```bash
# Gera um PAT com escopo 'repo' e 'workflow' no GitHub
# Settings → Developer settings → Personal access tokens → Fine-grained tokens
# Salva em um arquivo temporário
echo "github_pat_xxxxxxxxxxxxx" > /tmp/pat-token.txt

# Seta como secret no repo de conteúdo
gh secret set CROSS_REPO_TOKEN --repo josenaldo/meu-conteudo < /tmp/pat-token.txt

# Remove o arquivo temporário
rm /tmp/pat-token.txt

# Verifica que o secret foi criado
gh secret list --repo josenaldo/meu-conteudo
```

### 6. Criar workflow de dispatch no repo de conteúdo

No repo de conteúdo, cria `.github/workflows/notify-site.yml`:

```yaml
name: Notify Site to Rebuild

on:
  push:
    branches: [main]

jobs:
  notify:
    runs-on: ubuntu-latest
    steps:
      - name: Trigger site rebuild
        uses: peter-evans/repository-dispatch@v3
        with:
          token: ${{ secrets.CROSS_REPO_TOKEN }}
          repository: josenaldo/meu-site
          event-type: content-update
```

### 7. Testar o fluxo completo

```bash
# No repo de conteúdo — faz uma mudança e push
cd ~/repos/meu-conteudo
echo "Novo artigo" >> artigo.md
git add artigo.md
git commit -m "feat: novo artigo"
git push

# Verifica que o dispatch rodou no repo de conteúdo
gh run list --repo josenaldo/meu-conteudo --limit 1

# Verifica que o site está sendo rebuilded
gh run list --repo josenaldo/meu-site --limit 1

# Assiste o deploy do site
gh run watch --repo josenaldo/meu-site --exit-status
```

### 8. Diagrama do fluxo completo

```
┌─────────────────┐     git push      ┌──────────────────────┐
│  Repo Conteúdo  │ ───────────────→  │  GitHub Actions      │
│  (markdown)     │                   │  notify-site.yml     │
└─────────────────┘                   └──────────┬───────────┘
                                                 │
                                    repository_dispatch
                                    (CROSS_REPO_TOKEN)
                                                 │
                                                 ↓
┌─────────────────┐                   ┌──────────────────────┐
│  GitHub Pages   │  ←── deploy ────  │  Repo Site           │
│  (site live)    │                   │  deploy.yml          │
└─────────────────┘                   │  (build + deploy)    │
                                      └──────────────────────┘
```

---

## Combinando com outros comandos

`gh` fica **absurdamente poderoso** quando combinado com ferramentas Unix.

### Pipe com jq

```bash
# Listar PRs abertas com número de linhas alteradas
gh pr list --json number,title,additions,deletions \
  | jq '.[] | {number, title, lines: (.additions + .deletions)}'

# Top 5 repos por estrelas
gh repo list --json name,stargazerCount --limit 50 \
  | jq 'sort_by(-.stargazerCount) | .[0:5] | .[] | "\(.name): \(.stargazerCount) ⭐"'

# Issues sem assignee
gh issue list --json number,title,assignees \
  | jq '[.[] | select(.assignees | length == 0)]'
```

### Shell scripts de automação

```bash
#!/bin/bash
# deploy.sh — Dispara deploy e espera resultado

set -e

echo "🚀 Disparando deploy..."
gh workflow run deploy.yml

echo "⏳ Esperando a run aparecer..."
sleep 5

echo "👀 Assistindo deploy..."
gh run watch --exit-status

echo "✅ Deploy concluído com sucesso!"
echo "🌐 Site: $(gh api repos/josenaldo/meu-site/pages --jq '.html_url')"
```

### Bulk operations

```bash
# Fechar todas as issues com label "wontfix"
gh issue list --label wontfix --json number --jq '.[].number' \
  | xargs -I {} gh issue close {} --comment "Fechando — não planejado"

# Deletar todas as runs canceladas
gh run list --status cancelled --json databaseId --jq '.[].databaseId' \
  | xargs -I {} gh run delete {}

# Adicionar label em todas as issues abertas
gh issue list --json number --jq '.[].number' \
  | xargs -I {} gh issue edit {} --add-label "needs-triage"
```

### Integração com fzf (fuzzy finder)

```bash
# Checkout de PR com fuzzy search
gh pr list --json number,title \
  | jq -r '.[] | "\(.number) \(.title)"' \
  | fzf \
  | awk '{print $1}' \
  | xargs gh pr checkout

# View de issue com fuzzy search
gh issue list --json number,title \
  | jq -r '.[] | "\(.number) \(.title)"' \
  | fzf \
  | awk '{print $1}' \
  | xargs gh issue view
```

### Usando em CI/CD

```yaml
# .github/workflows/auto-merge-dependabot.yml
name: Auto-merge Dependabot

on: pull_request

permissions:
  contents: write
  pull-requests: write

jobs:
  auto-merge:
    if: github.actor == 'dependabot[bot]'
    runs-on: ubuntu-latest
    steps:
      - name: Auto-merge
        env:
          GH_TOKEN: ${{ secrets.GITHUB_TOKEN }}
        run: gh pr merge ${{ github.event.pull_request.number }} --squash --auto
```

---

## Boas práticas

### 1. Use SSH, não HTTPS

```bash
gh config set git_protocol ssh
```

SSH com chave ed25519 é mais seguro e não pede senha toda hora.

### 2. Crie aliases para o que você faz todo dia

```bash
gh alias set co "pr checkout"
gh alias set prs "pr list --author @me"
gh alias set runs "run list --limit 5"
gh alias set deploy "workflow run deploy.yml"
gh alias set why "run view --log-failed"
```

### 3. Use `--json` + `--jq` ao invés de parsear texto

```bash
# Ruim — frágil, depende do formato de texto
gh pr list | grep "feat"

# Bom — estruturado, confiável
gh pr list --json title --jq '.[] | select(.title | test("feat"))'
```

### 4. Use `--exit-status` em scripts

```bash
# Em scripts, sempre use --exit-status para propagar erros
gh run watch --exit-status || {
  echo "Deploy falhou!"
  gh run view --log-failed
  exit 1
}
```

### 5. Nunca coloque tokens no código

```bash
# Ruim
gh secret set TOKEN --body "ghp_abc123"  # fica no histórico do shell

# Bom
gh secret set TOKEN < token.txt
rm token.txt

# Melhor ainda
gh secret set TOKEN  # interativo, pede o valor
```

### 6. Use Fine-grained PATs

Personal Access Tokens clássicos têm escopo amplo demais. Prefira **Fine-grained tokens** com permissões mínimas e escopo para repos específicos.

### 7. Prefira `gh api` ao `curl` para a API do GitHub

```bash
# Ruim — precisa gerenciar autenticação manualmente
curl -H "Authorization: token $GH_TOKEN" \
  https://api.github.com/repos/OWNER/REPO

# Bom — autenticação automática, URL relativa
gh api repos/OWNER/REPO
```

### 8. Mantenha o gh atualizado

```bash
gh extension upgrade --all
# E atualize o próprio gh regularmente via seu package manager
```

---

## Troubleshooting

### "gh auth login" falha

```bash
# Verifica status atual
gh auth status

# Tenta com modo web explícito
gh auth login --web

# Se tiver firewall, usa token
gh auth login --with-token <<< "ghp_xxxxxxxxxxxx"
```

### "Resource not accessible by integration"

O token não tem as permissões necessárias. Comum com `GITHUB_TOKEN` em Actions.

**Solução:** Adicione `permissions` no workflow:

```yaml
permissions:
  contents: read
  pages: write
  id-token: write
  pull-requests: write
```

### "Could not resolve to a Repository"

```bash
# Verifica se o repo existe
gh repo view owner/repo

# Verifica se você está autenticado com a conta certa
gh auth status

# Verifica se o remote está correto
git remote -v
```

### "API rate limit exceeded"

```bash
# Verifica rate limit atual
gh api rate_limit --jq '.rate'

# Saída: {"limit":5000,"remaining":0,"reset":1681234567}

# O reset é timestamp unix — converte para ver quando libera
gh api rate_limit --jq '.rate.reset' | xargs -I {} date -d @{}
```

Para APIs autenticadas o limite é 5000 req/hora. Se estiver fazendo bulk operations, use paginação e throttling.

### Workflow não dispara com `workflow_dispatch`

```bash
# Verifica se o workflow tem trigger workflow_dispatch
gh workflow view deploy.yml --yaml | head -20

# Verifica se a branch padrão tem o workflow
gh api repos/OWNER/REPO/actions/workflows --jq '.workflows[] | {name, state}'

# Dispara com --ref explícito
gh workflow run deploy.yml --ref main
```

### Secret não funciona no workflow

- Secrets são **case-sensitive**
- Secrets não estão disponíveis em workflows disparados por **forks** (segurança)
- Verifique o nome: `gh secret list`
- Secrets de environment só funcionam se o job usa aquele environment

### "gh: command not found" após instalar

```bash
# Verifica se está no PATH
which gh

# Se instalou via Homebrew
eval "$(/home/linuxbrew/.linuxbrew/bin/brew shellenv)"

# Adiciona ao .bashrc/.zshrc
echo 'eval "$(/home/linuxbrew/.linuxbrew/bin/brew shellenv)"' >> ~/.zshrc
```

### Debug mode

Para qualquer comando que não funciona, adicione `GH_DEBUG=api`:

```bash
GH_DEBUG=api gh workflow run deploy.yml
```

Isso imprime a request/response HTTP completa — muito útil para entender o que está acontecendo.

---

## Referência rápida

```
┌──────────────────────────────────────────────────────────────────┐
│  GITHUB CLI — CHEATSHEET                                         │
├──────────────────────────────────────────────────────────────────┤
│                                                                  │
│  AUTH                                                            │
│  gh auth login          Autenticar                               │
│  gh auth status         Ver status                               │
│  gh auth token          Imprimir token                           │
│                                                                  │
│  REPOS                                                           │
│  gh repo create         Criar repo                               │
│  gh repo clone          Clonar repo                              │
│  gh repo fork           Fork repo                                │
│  gh repo view           Ver detalhes                             │
│                                                                  │
│  PULL REQUESTS                                                   │
│  gh pr create           Criar PR                                 │
│  gh pr list             Listar PRs                               │
│  gh pr view             Ver PR                                   │
│  gh pr checkout         Checkout da branch                       │
│  gh pr review           Aprovar/rejeitar                         │
│  gh pr merge            Merge                                    │
│  gh pr diff             Ver diff                                 │
│                                                                  │
│  ISSUES                                                          │
│  gh issue create        Criar issue                              │
│  gh issue list          Listar issues                            │
│  gh issue view          Ver issue                                │
│  gh issue close         Fechar issue                             │
│                                                                  │
│  ACTIONS                                                         │
│  gh workflow list       Listar workflows                         │
│  gh workflow run        Disparar workflow                        │
│  gh run list            Listar runs                              │
│  gh run view            Ver run (--log-failed!)                  │
│  gh run watch           Assistir run (--exit-status!)            │
│                                                                  │
│  SECRETS                                                         │
│  gh secret set          Configurar secret                        │
│  gh secret list         Listar secrets                           │
│  gh secret delete       Deletar secret                           │
│                                                                  │
│  API                                                             │
│  gh api <endpoint>      REST API call                            │
│  gh api graphql         GraphQL query                            │
│                                                                  │
│  RELEASES                                                        │
│  gh release create      Criar release                            │
│  gh release list        Listar releases                          │
│                                                                  │
│  UTILS                                                           │
│  gh browse              Abrir no browser                         │
│  gh gist create         Criar gist                               │
│  gh alias set           Criar atalho                             │
│  gh extension install   Instalar plugin                          │
│  gh config set          Configurar gh                            │
│  gh ssh-key add         Adicionar chave SSH                      │
│  gh codespace create    Criar codespace                          │
│                                                                  │
└──────────────────────────────────────────────────────────────────┘
```

---

## Ver também

- [[CI-CD]] — Pipelines, GitHub Actions em profundidade
- [[Terminal]] — Ferramentas de terminal e produtividade
- [[Linux]] — Fundamentos de shell scripting
- [[Docker]] — Containers e deploy
