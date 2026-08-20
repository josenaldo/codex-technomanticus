---
title: "Configurar o Git a seu favor"
created: 2026-07-31
updated: 2026-07-31
type: concept
status: seedling
fase: magus
tags:
  - controle-de-versao
  - git
  - tecnologia
publish: true
---

# Configurar o Git a seu favor

> [!abstract] TL;DR
> Meia dúzia de linhas de configuração eliminam boa parte do atrito que você sentiu nos níveis anteriores: `rerere` para não resolver o mesmo conflito duas vezes, `zdiff3` para ver a base no conflito, `push.autoSetupRemote` para o `push` nunca mais pedir argumento, `includeIf` para usar identidades diferentes por pasta. Além disso: **hooks** executam código nos seus eventos (e não são versionados por padrão — daí os frameworks), e **`.gitattributes`** ensina o Git a tratar tipos de arquivo de formas diferentes, inclusive gerando diff legível de `.docx` e PDF.

---

## O arquivo que resolve

Tudo abaixo mora no `~/.gitconfig` (nota 02) e pode ser escrito de uma vez. Comece por este bloco — cada linha corresponde a uma dor concreta dos níveis anteriores:

```ini
[core]
    editor = code --wait
    excludesFile = ~/.gitignore_global

[init]
    defaultBranch = main

[pull]
    rebase = true              # histórico linear (nota 11)

[push]
    autoSetupRemote = true     # fim do "git push -u origin ..." (Git 2.37+)
    followTags = true          # tags anotadas vão junto (nota 14)

[rerere]
    enabled = true             # grava e reaplica resoluções de conflito (nota 21)

[merge]
    conflictStyle = zdiff3     # mostra a BASE junto dos dois lados (nota 21)

[rebase]
    autoSquash = true          # entende os commits --fixup (nota 24)
    autoStash = true           # guarda e devolve o pendente sozinho

[fetch]
    prune = true               # some com refs de ramos deletados no servidor

[diff]
    algorithm = histogram      # diffs mais legíveis que o padrão
    colorMoved = zebra         # destaca blocos MOVIDOS vs alterados

[help]
    autocorrect = prompt       # "git stauts" → pergunta se você quis dizer status
```

Duas dessas merecem destaque porque quase ninguém conhece.

**`rerere.enabled`** — *reuse recorded resolution*. O Git grava como você resolveu cada conflito e, quando o mesmo conflito reaparecer (o que é a regra em rebases repetidos e em ramos de longa duração), ele aplica a resolução sozinho. Para quem faz rebase com frequência, é a configuração que mais economiza tempo no domínio inteiro.

**`diff.colorMoved`** — distingue visualmente código que foi **movido** de código que foi **alterado**. Numa refatoração que reorganiza arquivos, isso transforma um diff ilegível de 500 linhas num diff onde as 20 linhas que realmente mudaram saltam aos olhos. É especialmente útil em revisão (nota 12).

---

## Aliases

```ini
[alias]
    s = status -sb
    lg = log --oneline --graph --decorate --all
    last = log -1 --stat
    unstage = restore --staged
    amend = commit --amend --no-edit
    fixup = commit --fixup
    wip = "!git add -A && git commit -m 'wip'"
    undo = reset --soft HEAD~1
    recover = "!git reflog | head -30"
```

O prefixo `!` executa comando de shell em vez de subcomando do Git, o que permite compor.

Um conselho contra o excesso: aliases muito criativos criam dependência de máquina. Quando você estiver num servidor ou pareando com alguém, os seus atalhos não existem. Aliases para o que você usa dez vezes por dia, comandos completos para o resto.

---

## `includeIf`: identidades por pasta

O caso clássico: projetos pessoais assinam com o e-mail pessoal, projetos do trabalho com o corporativo — e esquecer disso significa commits com autoria errada (nota 02), corrigíveis só por reescrita de histórico.

```ini
# ~/.gitconfig
[user]
    name = Ana Ribeiro
    email = ana@pessoal.com

[includeIf "gitdir:~/trabalho/"]
    path = ~/.gitconfig-trabalho
```

```ini
# ~/.gitconfig-trabalho
[user]
    email = ana.ribeiro@empresa.com
[commit]
    gpgsign = true
```

Qualquer repositório dentro de `~/trabalho/` passa a usar a identidade corporativa automaticamente. Resolve de vez um erro que é chato de desfazer.

---

## Hooks: código nos seus eventos

Hooks são scripts em `.git/hooks/` que o Git executa em momentos determinados. Os que importam no dia a dia:

| Hook | Quando | Uso típico |
|---|---|---|
| `pre-commit` | antes de criar o commit | lint, formatador, detector de segredo (nota 25) |
| `commit-msg` | com a mensagem escrita | validar formato (Conventional Commits, nota 14) |
| `pre-push` | antes de enviar | rodar testes rápidos |
| `post-checkout` | ao trocar de ramo | reinstalar dependências |

> [!warning] Hooks não são versionados
> **O que acontece:** você escreve um `pre-commit` excelente, e nenhum colega o tem — porque `.git/` não vai no clone. **Por quê:** é proposital, e é uma decisão de segurança: se hooks fossem versionados, clonar um repositório qualquer executaria código de terceiros na sua máquina. **Como resolver:** ou aponte para uma pasta versionada — `git config core.hooksPath .githooks` —, ou use um framework que faz isso: **lefthook** e **pre-commit** são agnósticos de linguagem; **husky** e **lint-staged** são o padrão no ecossistema JS, e o vault os cobre em [[03-Dominios/Tecnologia/Tooling e Build/index|Tooling e Build]] (nota 16).

E a contrapartida honesta: hooks locais são **contornáveis** (`git commit --no-verify`). Eles servem para dar retorno rápido ao desenvolvedor, não para garantir. A garantia mora no servidor — CI e rulesets (nota 15).

---

## `.gitattributes`: ensinar o Git sobre seus arquivos

Diferente do `.gitconfig`, este arquivo **é versionado** e vale para todo o time. Ele fica na raiz do projeto.

```gitattributes
# fim de linha normalizado para todos, independente do sistema (nota 02)
* text=auto
*.sh text eol=lf
*.bat text eol=crlf

# tratar como binário (não tentar mesclar nem diferenciar)
*.png binary
*.pdf binary

# diff palavra a palavra para texto corrido
*.tex diff=tex
*.md diff=markdown

# arquivos que não devem ir no zip de release
docs/rascunhos/ export-ignore

# nunca tentar mesclar automaticamente este arquivo
CHANGELOG.md merge=union
```

O `text=auto` é o mais importante: ele resolve, de forma centralizada e para o time inteiro, o problema de fim de linha que a nota 02 tratava máquina a máquina.

E há um recurso que fecha um buraco aberto lá na nota 01 — *"o Git não compara Word e PDF de forma útil"*:

```gitattributes
*.docx diff=word
*.pdf diff=pdf
```

```ini
# no ~/.gitconfig
[diff "word"]
    textconv = pandoc --to=markdown
[diff "pdf"]
    textconv = pdftotext
```

O `textconv` faz o Git **converter o arquivo para texto antes de comparar**. O diff passa a mostrar o que mudou no conteúdo do documento, não `Binary files differ`. O repositório continua guardando o binário original — a conversão é só para exibição, e é local (cada pessoa precisa ter a ferramenta instalada). Para quem versiona documentos, muda a experiência por completo.

---

## Manutenção e desempenho

```bash
git maintenance start        # agenda otimizações periódicas em segundo plano
```

Disponível desde o Git 2.29, registra tarefas agendadas que mantêm o repositório compacto (empacotamento, pré-busca, atualização do grafo de commits) sem esperar pelo `gc` automático.

Para repositórios grandes:

```bash
git config core.fsmonitor true     # monitor do sistema de arquivos (Git 2.37+)
git config core.untrackedCache true
```

O `fsmonitor` acelera drasticamente o `git status` em projetos enormes, porque o Git passa a perguntar ao sistema operacional quais arquivos mudaram em vez de conferir os metadados de cada um (nota 20).

---

## Armadilhas comuns

> [!warning] Configuração global que muda o comportamento do time
> **O que acontece:** você configura `pull.rebase = true` globalmente, alguém do time não, e os históricos saem diferentes conforme quem sincronizou. **Por quê:** `~/.gitconfig` é individual. **Como evitar:** o que precisa ser igual para todos vai em `.gitattributes` (versionado) ou em regra de servidor (nota 15). O `.gitconfig` é para preferência pessoal.

> [!warning] `help.autocorrect` com correção automática
> **O que acontece:** configurado com um número (`autocorrect = 20`), o Git **executa** o comando que ele adivinhou após dois segundos. Um dia ele adivinha errado e executa algo destrutivo. **Por quê:** o valor numérico é o tempo de espera, não uma confirmação. **Como evitar:** use `prompt`, que pergunta antes.

> [!warning] Copiar um `.gitconfig` inteiro da internet
> **O que acontece:** o comportamento do Git muda de formas que você não consegue explicar, e depurar fica impossível. **Por quê:** cada linha muda um comportamento, e algumas interagem. **Como evitar:** adicione uma configuração por vez, entendendo qual dor ela resolve. `git config --list --show-origin` (nota 02) mostra de onde veio cada valor quando algo estranho acontecer.

---

## Resumo em uma frase

**O `.gitconfig` é preferência sua, o `.gitattributes` é acordo do time, os hooks são retorno rápido — e a garantia de verdade mora no servidor.**

> [!tip] Vídeo — configurações que valem a pena
> [**13 Advanced (but useful) Git Techniques and Shortcuts**](https://www.youtube.com/watch?v=ecK3EnyGD8o) (Fireship, 8 min) passa rápido por aliases, hooks e truques de configuração; bom para descobrir o que existe antes de aprofundar.

> [!tip] Pratique
> Aplique o bloco de configuração do começo desta nota e passe uma semana com ele. Depois teste o `rerere`: crie um conflito, resolva, desfaça com `git reset --hard ORIG_HEAD`, e refaça o merge — o Git deve resolver sozinho e avisar "Resolved ... using previous resolution".
>
> E, se você versiona documentos, monte o `textconv` para `.docx` ou PDF. Ver `git diff` mostrar o texto que mudou dentro de um binário é o tipo de coisa que muda a relação com a ferramenta.

---

## O que vem a seguir

Você fecha aqui o **nível 4**. Sabe desfazer com precisão, recuperar o que parecia perdido, reescrever sem quebrar a história alheia, agir quando um segredo vaza, e configurar a ferramenta para parar de sofrer.

O nível 5 sai do repositório bem-comportado e vai para os difíceis: os que não cabem mais num clone completo, os que dependem de outros repositórios, os que precisam ser divididos ou migrados, e o que o pipeline espera de tudo isso.

- **27 — Monorepo × polyrepo** — a primeira nota do N5.
- [[03-Dominios/Tecnologia/Controle de Versão/N4 - Quando dá errado/index|N4 — Quando dá errado]] — o índice do nível.

## Fontes

- **Git** — [*git-config*](https://git-scm.com/docs/git-config) — a referência de todas as chaves citadas, incluindo `includeIf`, `push.autoSetupRemote` e `help.autocorrect`.
- **Git** — [*gitattributes*](https://git-scm.com/docs/gitattributes) — `text=auto`, `diff` com `textconv`, `merge=union`, `export-ignore`.
- **Scott Chacon & Ben Straub** — [*Pro Git*, cap. 8 — "Atributos do Git"](https://git-scm.com/book/pt-br/v2/Personalizando-o-Git-Atributos-do-Git) — o exemplo canônico de diff de arquivos binários via `textconv`.
- **Scott Chacon & Ben Straub** — [*Pro Git*, cap. 8 — "Git Hooks"](https://git-scm.com/book/pt-br/v2/Personalizando-o-Git-Git-Hooks) — a lista completa de hooks e a ordem de execução.
- **Git** — [*git-maintenance*](https://git-scm.com/docs/git-maintenance) · [*git-rerere*](https://git-scm.com/docs/git-rerere) — as duas ferramentas menos conhecidas desta nota.
