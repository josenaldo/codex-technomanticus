---
title: "CI/CD com GitHub Actions"
type: concept
publish: true
created: 2026-05-13
updated: 2026-05-13
status: seedling
tags:
  - claude-code
  - ci-cd
  - github-actions
  - automacao
  - headless
---

# CI/CD com GitHub Actions

> [!abstract] TL;DR
> Claude Code em GitHub Actions significa rodar `claude --print` como step de um workflow. Os casos de uso mais úteis são: code review automático em PRs, geração de changelog, verificação de regressões, e análise de cobertura de testes. A configuração é simples — API key como secret, step com headless mode, output capturado e postado como comentário.

## Configuração básica

Todo workflow que usa Claude Code precisa de:

1. `ANTHROPIC_API_KEY` como secret no repositório (`Settings > Secrets > Actions`)
2. `claude` instalado no step (via `npm install -g @anthropic-ai/claude-code` ou o action oficial)

```yaml
# .github/workflows/claude-review.yml
name: Claude Code Review

on:
  pull_request:
    types: [opened, synchronize]

jobs:
  review:
    runs-on: ubuntu-latest
    permissions:
      pull-requests: write
      contents: read

    steps:
      - uses: actions/checkout@v4
        with:
          fetch-depth: 0  # Necessário para git diff completo

      - name: Install Claude Code
        run: npm install -g @anthropic-ai/claude-code

      - name: Run review
        env:
          ANTHROPIC_API_KEY: ${{ secrets.ANTHROPIC_API_KEY }}
        run: |
          DIFF=$(git diff origin/main...HEAD)
          REVIEW=$(echo "$DIFF" | claude --print --no-permission-prompts \
            --allowedTools "" \
            "Você é um revisor de código. Analise este diff e identifique:
            1. Bugs potenciais
            2. Problemas de segurança
            3. Violações das convenções do projeto (ver CLAUDE.md)
            Seja conciso. Máximo 10 itens.")
          echo "REVIEW<<EOF" >> $GITHUB_OUTPUT
          echo "$REVIEW" >> $GITHUB_OUTPUT
          echo "EOF" >> $GITHUB_OUTPUT
        id: review

      - name: Post review comment
        uses: actions/github-script@v7
        with:
          script: |
            github.rest.issues.createComment({
              issue_number: context.issue.number,
              owner: context.repo.owner,
              repo: context.repo.repo,
              body: `## Análise automática\n\n${{ steps.review.outputs.REVIEW }}`
            })
```

## Action oficial da Anthropic

Anthropic disponibiliza uma GitHub Action que simplifica a integração:

```yaml
- uses: anthropics/claude-code-action@v1
  with:
    anthropic-api-key: ${{ secrets.ANTHROPIC_API_KEY }}
    prompt: "Analise este PR e identifique regressões potenciais"
    allowed-tools: "Read,Grep,Bash"
```

A action cuida de instalar o Claude Code, configurar permissões, e capturar o output.

## Casos de uso em CI/CD

### Review automático de PR

```yaml
- name: Claude PR Review
  env:
    ANTHROPIC_API_KEY: ${{ secrets.ANTHROPIC_API_KEY }}
    GH_TOKEN: ${{ secrets.GITHUB_TOKEN }}
  run: |
    git diff origin/${{ github.base_ref }}...HEAD > /tmp/pr.diff
    claude --print --no-permission-prompts \
      --allowedTools "Read,Grep" \
      --max-turns 10 \
      "$(cat /tmp/pr.diff)" \
      > /tmp/review.txt
    gh pr comment ${{ github.event.number }} --body "$(cat /tmp/review.txt)"
```

### Geração de changelog

```yaml
on:
  push:
    tags: ['v*']

steps:
  - name: Generate changelog
    env:
      ANTHROPIC_API_KEY: ${{ secrets.ANTHROPIC_API_KEY }}
    run: |
      COMMITS=$(git log $(git describe --tags --abbrev=0 HEAD^)..HEAD --oneline)
      CHANGELOG=$(echo "$COMMITS" | claude --print \
        "Transforme estes commits em um changelog estruturado por categoria:
        - Features, Bug Fixes, Breaking Changes, Internal.
        Formato markdown. Tom neutro, técnico.")
      echo "$CHANGELOG" > CHANGELOG_LATEST.md
```

### Verificação de convenções

```yaml
on:
  pull_request:

steps:
  - name: Check conventions
    env:
      ANTHROPIC_API_KEY: ${{ secrets.ANTHROPIC_API_KEY }}
    run: |
      FILES=$(git diff --name-only origin/main...HEAD | grep '\.ts$')
      for file in $FILES; do
        RESULT=$(claude --print --allowedTools "Read" \
          --max-turns 3 \
          "Verifica se $file segue as convenções do projeto (ver CLAUDE.md).
          Responda somente: PASS ou FAIL: <motivo>")
        if echo "$RESULT" | grep -q "^FAIL"; then
          echo "::error file=$file::$(echo $RESULT | sed 's/^FAIL: //')"
          exit 1
        fi
      done
```

### Análise de cobertura

```yaml
on:
  pull_request:

steps:
  - name: Run tests with coverage
    run: npm run test:coverage -- --json > coverage.json

  - name: Analyze coverage gaps
    env:
      ANTHROPIC_API_KEY: ${{ secrets.ANTHROPIC_API_KEY }}
    run: |
      claude --print --allowedTools "Read" \
        "Analise coverage.json e identifique os 3 módulos com menor cobertura.
        Para cada um, sugira os casos de teste mais importantes que estão faltando." \
        > coverage-analysis.txt
      cat coverage-analysis.txt
```

## Controle de permissões no CI

Em CI, sempre use `--allowedTools` para restringir o que o agente pode fazer:

| Caso de uso | Tools necessárias |
|-------------|-------------------|
| Review de código | `Read,Grep` |
| Análise de diff | Nenhuma (só lê stdin) |
| Verificação de convenções | `Read` |
| Geração de docs | `Read,Write` |
| Testes automatizados | `Read,Bash` |

Nunca deixe o agente com acesso irrestrito em CI. O pipeline tem acesso ao código completo — com tools livres, um prompt mal construído pode modificar arquivos no checkout.

## Limitação de tokens e tempo

```yaml
- name: Claude analysis
  timeout-minutes: 5  # Timeout do step no Actions
  env:
    ANTHROPIC_API_KEY: ${{ secrets.ANTHROPIC_API_KEY }}
  run: |
    claude --print \
      --max-turns 8 \
      --no-permission-prompts \
      "..."
```

`--max-turns` controla quantas tool calls o agente faz (cada uma consome tokens). `timeout-minutes` é o limite de tempo do job inteiro.

## Armadilhas

**API key exposta em logs**: nunca use `set -x` com o step que tem `ANTHROPIC_API_KEY` no ambiente. O `set -x` imprime variáveis de ambiente em logs públicos.

**Uso de `--no-permission-prompts` sem `--allowedTools`**: o agente pode fazer qualquer coisa no checkout. Sempre combine as duas flags.

**Diff muito grande para o contexto**: PRs com centenas de arquivos modificados vão exceder o contexto do modelo. Filtre para arquivos relevantes antes de passar para o agente.

**Custo por PR**: cada análise custa tokens. Com muitos PRs por dia, o custo pode surpreender. Adicione condicional para rodar só em PRs de certas branches ou acima de determinado tamanho.

## Veja também

- [[03-Dominios/IA/Claude Code/Time e Automação/01 - Headless mode|01 - Headless mode]] — flags e comportamento do `claude --print`
- [[03-Dominios/IA/Claude Code/Time e Automação/03 - Dispatch via claude -p|03 - Dispatch via `claude -p`]] — padrões de invocação
- [[03-Dominios/IA/Claude Code/Time e Automação/05 - Controle de custo|05 - Controle de custo]] — monitorar gasto em automações
- [[03-Dominios/IA/Claude Code/Time e Automação/index|Time e Automação]] — índice do galho
