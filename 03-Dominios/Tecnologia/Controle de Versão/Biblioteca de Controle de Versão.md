---
title: "Biblioteca de Controle de Versão"
created: 2026-07-31
updated: 2026-07-31
type: reference
status: seedling
aliases:
  - Biblioteca de Git
tags:
  - controle-de-versao
  - git
  - github
  - referências
lang: pt
publish: true
---

# Biblioteca de Controle de Versão

> Recursos externos curados pra **praticar** Git, não só ler sobre ele. A aposta do domínio é que as notas explicam o **modelo** (por que o commit é um snapshot, o que o index é, por que o conflito acontece) e delegam a **repetição** — decorar comandos, sentir o que `rebase` faz com o grafo — pros simuladores abaixo. Ler sobre rebase não ensina rebase; quebrar e recuperar um repositório de brinquedo, sim.
>
> Todos os links verificados em **2026-07-31**.

## Simuladores interativos (o núcleo)

Ambientes onde você digita comandos de verdade e **vê o DAG se mexer**. Comece pelo primeiro.

- **[Learn Git Branching](https://learngitbranching.js.org/)** — o canônico. Sandbox visual com níveis progressivos (Introdução → Ramos remotos → tópicos avançados: `rebase -i`, `cherry-pick`, `--force`, tags, relative refs `HEAD~`/`^`). Tem **[versão em português](https://learngitbranching.js.org/?locale=pt_BR)** e um [modo sandbox livre](https://learngitbranching.js.org/?NODEMO) onde você inventa o cenário. É o par exato do SG1 e do SG2 deste domínio.
- **[Visualizing Git](https://git-school.github.io/visualizing-git/)** (git-school) — sandbox puro, sem níveis: você digita, o grafo desenha. Melhor que o Learn Git Branching pra *testar uma hipótese específica* ("o que `reset --soft` faz com o ponteiro?"), porque não tem objetivo a cumprir.
- **[Explain Git with D3](https://onlywei.github.io/explain-git-with-d3/)** — mais antigo e mais simples que os dois acima, mas a animação de `rebase` e `cherry-pick` continua sendo a mais didática que existe.
- **[Oh My Git!](https://ohmygit.org/)** — jogo de cartas open source (desktop, gratuito) sobre Git, com repositórios reais por trás. Bom pra quem trava com terminal: cada carta é um comando, e o grafo é o tabuleiro.
- **[Git Exercises](https://gitexercises.fracz.com/)** — exercícios que você resolve **no seu próprio terminal**, num repo clonado, com verificação automática por push. Aqui não tem simulação: é Git de verdade, com correção. O melhor complemento depois do Learn Git Branching.
- **[git-katas](https://github.com/eficode-academy/git-katas)** (Eficode) — coleção de katas com scripts que montam o cenário sujo (conflito, história bagunçada, commit perdido) pra você resolver. Feito pra treinar **recuperação**, que é justamente o que o SG2 cobre.
- **[git-sim](https://github.com/initialcommit-com/git-sim)** — CLI que gera imagem/vídeo do que um comando *vai* fazer no seu repo real, antes de rodar. Útil pra conferir um `rebase -i` arriscado — e pra gerar diagrama de nota.

## Tutoriais guiados (passo a passo, no terminal)

- **[Git Immersion](https://gitimmersion.com/)** — 50+ labs curtos, do `init` ao `rebase`, cada um com o comando e o resultado esperado. Sequencial e sem enrolação.
- **[Git How To](https://githowto.com/)** — mesma ideia, tour guiado; versão em vários idiomas.
- **[GitHub Skills](https://skills.github.com/)** — cursos oficiais que rodam **dentro de um repositório seu**, com o Actions corrigindo cada passo. É a melhor porta pro lado *plataforma* (PRs, review, protection rules, Actions) — o SG3 deste domínio.

## Referência e teoria

- **[Pro Git](https://git-scm.com/book/en/v2)** (Chacon & Straub) — livro oficial, gratuito, em português também. O capítulo **10 (Git Internals)** é a fonte primária do SG1: objetos, refs, packfiles.
- **[git-scm — documentação](https://git-scm.com/doc)** — as man pages. `git help <comando>` é a mesma coisa, offline.
- **[Think Like (a) Git](https://think-like-a-git.net/)** — ensaio que explica Git via teoria dos grafos. Curto, e é o texto que faz o `reflog` "clicar".
- **[How Git Works](https://wizardzines.com/zines/git/)** (Julia Evans) — zine paga sobre o modelo mental; o [blog dela](https://jvns.ca/) tem material gratuito excelente sobre internals e sobre *por que* Git confunde.

## Socorro (quando já quebrou)

- **[Oh Shit, Git!?!](https://ohshitgit.com/)** — receitas pro "eu fiz merda, e agora?". Versão sem palavrão em **[Dangit, Git!?!](https://dangitgit.com/)** (ambas com tradução em português).

## Em português

Bloco herdado e reverificado do repositório [`aprendendo-git-e-github`](https://github.com/josenaldo/aprendendo-git-e-github) — o mapa de recursos PT-BR que o autor mantém desde 2023 pra indicar a colegas. Todos os links abaixo revalidados em 2026-07-31.

**Guia rápido e referência**

- **[Git — Guia prático](https://rogerdudler.github.io/git-guide/index.pt_BR.html)** (Roger Dudler) — uma página, os comandos essenciais. O melhor "cola" pra quem está no nível 0.
- **[Cheat sheet Git/GitHub em português](https://training.github.com/downloads/pt_BR/github-git-cheat-sheet/)** — PDF oficial do GitHub Training. Imprima.
- **[Pro Git em português](https://git-scm.com/book/pt-br/v2)** — o livro oficial, traduzido e gratuito.
- **[Git Magic (pt-BR)](http://www-cs-students.stanford.edu/~blynn/gitmagic/intl/pt_br/)** — livro curto e gratuito, abordagem "comece usando, entenda depois".

**Socorro em português**

- **[Oh Shit, Git!?! (pt-BR)](https://ohshitgit.com/pt_BR)** — receitas pro "fiz merda, e agora?". Versão sem palavrão: **[Dangit, Git!?! (pt-BR)](https://dangitgit.com/pt_BR)**.

**Interativo em português**

- **[Learn Git Branching em PT-BR](https://learngitbranching.js.org/?locale=pt_BR)** — o simulador principal, traduzido.

## Material próprio (workshops do autor)

Cursos e workshops que o autor ministrou e compartilha. São a base pedagógica deste domínio.

- **[workshop-git](https://github.com/josenaldo/workshop-git)** (2016, 9 tomos) — o mais completo tecnicamente; a sequência de diagramas de branching é a melhor parte.
- **[curso-git-github](https://github.com/josenaldo/curso-git-github)** (2017, 6 tomos) — com GitKraken; o "Tomo 6 — Subindo de nível" é a ponte tutorial→modelo.
- **[escrita-sem-medo-com-git-e-github](https://github.com/josenaldo/escrita-sem-medo-com-git-e-github)** (2021) — Git pra **não-programadores** (acadêmicos). A metáfora da máquina do tempo e a seção "o que o Git NÃO faz" vêm daqui.
- **[aprendendo-git-e-github](https://github.com/josenaldo/aprendendo-git-e-github)** (2023) — o mapa de recursos que virou o bloco PT-BR acima.

> [!warning] Datado
> Os dois primeiros usam GitKraken/TortoiseGit como fio condutor, dizem `master` em vez de `main`, e ensinam `git checkout` para trocar de branch (hoje: `switch`/`restore`). O conteúdo conceitual segue válido; a superfície de comandos, não.

## Outros recursos úteis

- **[Atlassian Git Tutorials](https://www.atlassian.com/git/tutorials)** — do básico ao avançado, com diagramas bons de merge/rebase.
- **[Git Flight Rules](https://github.com/k88hudson/git-flight-rules)** — manual de procedimentos "o que fazer quando X acontece", no estilo dos checklists de aviação.
- **[gitignore.io](https://www.toptal.com/developers/gitignore)** — gera `.gitignore` por stack (agora hospedado pela Toptal).
- **[Git Succinctly](https://www.syncfusion.com/succinctly-free-ebooks/git/overview)** — ebook gratuito, curto, em inglês.

## Como usar isto nas notas

> [!tip] Convenção do domínio
> Toda nota de **SG1** e **SG2** fecha com um callout `[!tip] Pratique` apontando pro **nível ou exercício específico** que treina aquele conceito — não pra home do site. A nota entrega o modelo; o link entrega a repetição. Isso é o que impede o domínio de virar mais um tutorial de Git.

## Veja também

- [[03-Dominios/Tecnologia/Controle de Versão/index|Controle de Versão]] — o domínio
- [[03-Dominios/Tecnologia/Terminal/index|Terminal]] — Lazygit e `delta`, as ferramentas de terminal pra Git
