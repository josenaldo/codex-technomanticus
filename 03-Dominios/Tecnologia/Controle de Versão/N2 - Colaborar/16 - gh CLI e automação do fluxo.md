---
title: "gh CLI e automação do fluxo"
created: 2026-07-31
updated: 2026-07-31
type: concept
status: seedling
fase: Adepto
tags:
  - controle-de-versao
  - git
  - github
  - tecnologia
publish: true
---

# `gh` CLI e automação do fluxo

> [!abstract] TL;DR
> O `gh` é o GitHub no terminal: abrir PR, revisar, mergear, acompanhar a CI, criar repositório e ler issues sem trocar de janela. Dois comandos mudam o dia a dia mais do que os outros — **`gh pr create`**, que abre o PR de onde você já está, e **`gh pr checkout`**, que baixa o ramo de um PR alheio para você testar de verdade em vez de revisar por leitura. Para o que não tem comando pronto, **`gh api`** fala direto com a API, com saída em JSON pronta para script.

---

## Por que sair do navegador

O fluxo do nível 2, feito pela interface, tem um custo escondido: **troca de contexto**. Você está no terminal, com o ramo pronto, e precisa ir ao navegador, achar o repositório, clicar em "Compare & pull request", preencher, voltar. Quinze segundos, dez vezes por dia, mais a atenção perdida em cada ida.

Além disso, o que se faz por clique não se automatiza. `gh` é um programa: aceita argumentos, devolve JSON, entra em script e roda em pipeline.

```bash
gh auth login       # uma vez por máquina — resolve também a autenticação do git push
gh auth status      # confirma conta, escopos e protocolo
```

Esse `gh auth login` é, aliás, a forma mais simples de resolver a autenticação da nota 05: ele configura o Git para usar as credenciais do `gh`, e o `git push` para de pedir token.

---

## O fluxo completo sem sair do terminal

```bash
git switch -c corrige-busca
# ... trabalha, commita ...
git push -u origin corrige-busca

gh pr create --fill                    # usa os commits como título e corpo
gh pr create --draft                   # como rascunho
gh pr create --reviewer ana,bruno --label bug

gh pr status                           # meus PRs, os que esperam minha revisão
gh pr list --state open --author @me
gh pr view 482                         # no terminal
gh pr view 482 --web                   # abre no navegador
gh pr checks 482                       # o resultado da CI
gh pr diff 482                         # o diff, sem sair daqui

gh pr review 482 --approve
gh pr review 482 --request-changes -b "Falta tratar lista vazia em X"
gh pr merge 482 --squash --delete-branch
```

O `--fill` merece destaque: em PRs de um commit só, ele transforma abrir um pull request num único comando, sem nada para digitar.

---

## O comando que muda a revisão

```bash
gh pr checkout 482
```

Ele baixa o ramo do PR e te coloca nele — inclusive quando o PR vem de um *fork*, caso em que fazer isso na mão é chato o suficiente para a maioria das pessoas desistir.

Por que isso importa: revisar pelo diff no navegador é ler. **Revisar com o ramo na sua máquina é executar** — rodar os testes, abrir a aplicação, tentar o caso de borda que você suspeita que quebra. A diferença de qualidade entre as duas revisões é enorme, e o que separava uma da outra era o atrito de baixar o ramo.

Terminada a revisão, `git switch -` volta para onde você estava.

---

## Repositórios e issues

```bash
gh repo create meu-projeto --private --source=. --push
gh repo clone josenaldo/workshop-git
gh repo fork owner/projeto --clone
gh repo view --web

gh issue create --title "Timeout na busca" --body "..."
gh issue list --label bug --assignee @me
gh issue view 482 --comments
gh issue close 482
```

O `gh repo create --source=. --push` resolve num comando o que a nota 05 fazia em quatro passos: cria o repositório no GitHub a partir da pasta atual, configura o remoto e já envia.

---

## Acompanhar a CI

```bash
gh run list                    # execuções recentes
gh run watch                   # acompanha a atual, ao vivo
gh run view 12345 --log-failed # só o log do que falhou
gh workflow list
gh workflow run deploy.yml     # dispara manualmente
```

O `gh run view --log-failed` é o que economiza mais tempo: em vez de navegar por uma interface de logs para achar o passo vermelho, ele imprime direto o trecho que quebrou.

---

## `gh api` — quando não existe comando

Nem tudo tem subcomando dedicado. O `gh api` conversa direto com a API, já autenticado:

```bash
gh api repos/josenaldo/workshop-git
gh api repos/{owner}/{repo}/pulls --jq '.[] | "\(.number) \(.title)"'
gh api -X PATCH repos/{owner}/{repo} -f description="Nova descrição"
gh api graphql -f query='...'
```

Os marcadores `{owner}` e `{repo}` são preenchidos a partir do repositório em que você está. O `--jq` filtra a resposta sem precisar do `jq` instalado.

A maior parte dos comandos também aceita saída estruturada, o que é o que torna o `gh` utilizável em script:

```bash
gh pr list --json number,title,author --jq '.[] | select(.author.login=="ana")'
```

---

## Personalizar

```bash
gh alias set prc 'pr create --fill'
gh alias set prs 'pr status'
gh alias list
```

E há um ecossistema de extensões (`gh extension install ...`) para o que a ferramenta não cobre — desde painéis no terminal até integrações específicas.

---

## Em automação e CI

Dentro de um workflow do Actions, o `gh` já vem instalado; basta fornecer o token:

```yaml
- run: gh pr comment "$PR" --body "Build publicado."
  env:
    GH_TOKEN: ${{ secrets.GITHUB_TOKEN }}
```

> [!warning] Token de automação com escopo demais
> **O que acontece:** um script usa um token pessoal com acesso a todos os repositórios da conta, guardado numa variável de ambiente. **Por quê:** é o caminho mais rápido para fazer funcionar. **Como evitar:** em CI, use o `GITHUB_TOKEN` do próprio workflow, que é temporário e restrito ao repositório. Fora dela, prefira tokens de escopo fino, limitados aos repositórios e permissões necessários, com validade. E nunca escreva o token no `.gh` do repositório nem em arquivo versionado — vale a nota 06 inteira aqui.

> [!warning] `gh` autenticado como a conta errada
> **O que acontece:** você opera num repositório de trabalho com a conta pessoal (ou o inverso), e o PR sai com a autoria errada. **Por quê:** o `gh` guarda credenciais por host, e é comum ter mais de uma conta. **Como evitar:** `gh auth status` mostra quem está ativo. Para múltiplas contas, `gh auth switch`.

---

## O que fica de referência

Esta nota cobre o **fluxo** — o que você usa toda semana e por quê. O catálogo completo de subcomandos, flags e cenários (`gh repo edit`, `gh secret`, `gh release`, `gh gist`, autenticação em CI/CD, formatos de saída) está na referência de consulta do domínio:

- [[03-Dominios/Tecnologia/Controle de Versão/GitHub CLI|GitHub CLI — referência]] — material extenso, organizado por área, para consultar quando precisar de um comando específico.

E, para o `gh` como parte de um ambiente de terminal produtivo — junto de Lazygit, `delta` e afins —, o vault cobre em [[03-Dominios/Tecnologia/Terminal/index|Terminal]].

---

## Resumo em uma frase

**O `gh` traz o GitHub para onde você já está, e o `gh pr checkout` é o que transforma revisão de leitura em revisão de execução.**

> [!tip] Vídeo — o gh do começo ao fim
> [**GitHub CLI (gh) Full Tutorial | Manage GitHub from Terminal**](https://www.youtube.com/watch?v=UBu1P7G7T8U) (Amitabh Soni, 14 min) passa por autenticação, repositórios, PRs e workflows sem sair do terminal.

> [!tip] Pratique
> Faça o ciclo inteiro sem tocar no navegador, uma vez: `git switch -c`, commit, `git push -u`, `gh pr create --fill`, `gh pr checks`, `gh pr merge --squash --delete-branch`. Cronometre. A diferença em relação ao caminho pelo navegador costuma convencer sozinha.
>
> Depois, use `gh pr checkout` no próximo PR que você for revisar, rode o projeto e teste de fato. É a mudança de hábito com maior retorno deste nível.

---

## O que vem a seguir

Você fecha aqui o **nível 2**. Sabe propor mudanças para revisão, escolher uma estratégia de ramificação, escrever um histórico que gera versão e changelog, configurar a plataforma para que os acordos sejam obrigatórios, e operar tudo isso pelo terminal.

O **nível 3 é o ponto de virada do domínio**. Ele não ensina comando novo: ele reexplica tudo o que você vem usando desde o nível 0 — commit, branch, merge, a área de preparação — em termos do que o Git realmente faz por baixo. Depois dele, `reset --hard` deixa de ser reza e vira um ponteiro se movendo num grafo, e as regras que você seguiu por disciplina passam a ter mecanismo.

- **17 — Tudo tem hash: o modelo de objetos** — a primeira nota do N3.
- [[03-Dominios/Tecnologia/Controle de Versão/N2 - Colaborar/index|N2 — Colaborar]] — o índice do nível.
- [[03-Dominios/Tecnologia/Controle de Versão/index|Controle de Versão]] — o mapa dos 7 níveis.

## Fontes

- **GitHub** — [*GitHub CLI manual*](https://cli.github.com/manual/) — a referência oficial de todos os subcomandos e flags.
- **GitHub Docs** — [*GitHub CLI*](https://docs.github.com/en/github-cli) — instalação, autenticação, aliases e uso em Actions.
- **GitHub Docs** — [*Using GitHub CLI in workflows*](https://docs.github.com/en/actions/how-tos/write-workflows/choose-what-workflows-do/use-github-cli) — o padrão de `GH_TOKEN` em automação.
- **Nota interna** — [[03-Dominios/Tecnologia/Controle de Versão/GitHub CLI|GitHub CLI (referência)]] — catálogo extenso de comandos, migrado de `Infraestrutura/` para este domínio em 2026-07-31.
