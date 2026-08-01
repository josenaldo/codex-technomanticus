---
title: "Design — Domínio Controle de Versão"
created: 2026-07-31
updated: 2026-07-31
type: meta
publish: false
tags:
  - meta
  - spec
  - design
  - git
  - controle-de-versao
---

# Design — Domínio Controle de Versão

Spec de design do domínio `03-Dominios/Tecnologia/Controle de Versão`. Decidido em 2026-07-31, na mesma conversa que registrou as fronteiras de **Infraestrutura** (Tier 2). **Revisado no mesmo dia** após a análise de 4 repositórios de material próprio do autor — a revisão inverteu a ordem do domínio (ver *Progressão*).

---

## Por que domínio próprio (e não um galho de Infraestrutura)

1. **Quebra a espinha da estante de Infra.** O `index.md` de Infraestrutura define seu escopo como *"o que sustenta as aplicações **depois que elas saem da máquina do dev**"* — containers, orquestração, proxy, SO, provedor. Git é sobre o **histórico do código**, antes de rodar. O `GitHub CLI.md` estar lá é acidente de estante-gaveta.
2. **Volume de domínio, não de galho.** ~34 notas em 3 fases — escala de Acessibilidade (21) ou System Design (27).
3. **É a infraestrutura do *ofício*.** `git log/blame/bisect/pickaxe` é a ferramenta primária de [[03-Dominios/Engenharia/Arqueologia e Restauração de Software/index|Arqueologia de Software]].

**Camada:** `Tecnologia`. **Nome:** `Controle de Versão` (tool-neutral no topo, comporta Git + GitHub + o contraste com SVN/Jujutsu).

---

## Lente e progressão

> **Lente:** o repositório como **fonte de verdade** (o contrato de trabalho do time) e como **testemunha** (quem mudou o quê, por quê, e quando quebrou).

**Progressão (revisada 2026-07-31): do operacional para o modelo, em 7 níveis.**

O desenho original começava pelo modelo de objetos (SG1 "O modelo do Git") e só depois operava. Foi **invertido** por decisão do autor, com dois motivos que se somam:

1. **Este material vai ser compartilhado com colegas.** O domínio não é só nota pessoal — é o que o autor manda pra quem está começando. Um domínio que abre com blob/tree/DAG perde exatamente esse leitor no primeiro parágrafo.
2. **É como o próprio autor já ensina.** Os 4 workshops dele (2016–2023) abrem pelo *problema* e pela *operação*, e só sobem ao modelo depois que a pessoa já commitou — o `curso-git-github` literalmente chama o bloco de internals de **"Tomo 6 — Subindo de nível"**, depois de 5 tomos operacionais. O desenho original contrariava a pedagogia que o material dele já provou.

O antídoto contra "virar mais um tutorial" **não é começar difícil** — é **subir**. Cada nível fecha com uma ponte explícita pro seguinte, e o nível 3 recontextualiza tudo que os níveis 0-2 ensinaram como receita:

```
N0 Sobrevivência → N1 Fluxo diário → N2 Colaborar → N3 O modelo por baixo
                                                         ↓
N6 O repo como testemunha ← N5 Repositórios reais ← N4 Quando dá errado
```

**Mapa de fases do vault:** N0-N1 = Iniciado · N2-N3 = Adepto · N4-N6 = Magus.

---

## Material próprio do autor (analisado em 2026-07-31)

Quatro repositórios de workshops/cursos que o autor ministrou e compartilha com colegas. **Aproveitamento alto** — não como texto a copiar, mas como **estrutura pedagógica já validada em sala**, mais diagramas e narrativas próprias.

| Repo | Ano | Formato | O que é |
|---|---|---|---|
| [`workshop-git`](https://github.com/josenaldo/workshop-git) | 2016 | reveal.js, 9 tomos | **O mais completo tecnicamente.** VCS local/centralizado/distribuído · snapshots×diferenças · checksum · os 3 estados · config (editor, difftool, help) · essencial (init/clone/status/gitignore/diff/commit/rm/mv/log) · **desfazendo coisas** (amend/reset/checkout) · remotos **múltiplos** · tagging (leve×anotada) · **branching em 9 diagramas sequenciais** (branch é ponteiro → HEAD → checkout move HEAD → commit avança) · merge×rebase com diagramas · GitHub |
| [`curso-git-github`](https://github.com/josenaldo/curso-git-github) | 2017 | reveal.js, 6 tomos | Curso com **GitKraken** (GUI). Intro VCS com narrativa histórica ("O dia em que rasguei o CD!", Torvalds/BitKeeper) · workflow básico · workflow remoto · GitHub · GitKraken · **"Tomo 6 — Subindo de nível"**: SHA-1, *"Git só adiciona dados"*, snapshots×diferenças, log, diff, conflitos, .gitignore, remote, **pendrive como servidor Git** |
| [`escrita-sem-medo-com-git-e-github`](https://github.com/josenaldo/escrita-sem-medo-com-git-e-github) | 2021 | reveal.js, 13 slides md | **Git pra não-programadores** (acadêmicos: artigo, dissertação/tese, trabalho em grupo). *"Trabalhar sem controle de versão é como trabalhar sem EPI"* · *"todos mantemos uma linha do tempo"* (mas nomes de arquivo não formam uma) · **"o Git é uma máquina do tempo… com acesso a múltiplas linhas temporais"** · o que é VCS pelas 4 perguntas (o quê/quem/quando/por quê) · **seção "Limitações": o que o Git NÃO faz** (comparar Word/Excel, imagens, binários) |
| [`aprendendo-git-e-github`](https://github.com/josenaldo/aprendendo-git-e-github) | 2023 | README (124 linhas) | **Mapa curado de recursos em PT-BR**, com badges de idioma e progressão explícita: início rápido → cursos em vídeo → referência rápida → oficial → resolvendo problemas → extras → livros → ferramentas → hospedagem → avançado |

### O que aproveitar, item a item

| Ativo do material | Vai pra |
|---|---|
| Abertura pelo problema: `tcc-final-v3-AGORA-VAI.docx`, "nomes de arquivo não formam uma linha do tempo" | **nota 01** — é a melhor porta de entrada nível 0 que existe |
| *"Trabalhar sem VCS é como trabalhar sem EPI"* + as 4 perguntas (o quê/quem/quando/por quê) | **nota 01** |
| **"O que o Git NÃO faz"** (binários, Word/Excel, imagens) | **nota 01** — seção de honestidade que quase nenhum tutorial escreve |
| VCS local → centralizado → distribuído (3 diagramas) | **nota 01** |
| Narrativa histórica: "O dia em que rasguei o CD", Torvalds/BitKeeper, "Torvalds fica full pistola" | **nota 01** — abertura-problema com voz própria |
| Config inicial: identidade, editor, difftool, `git help` | **nota 02** |
| Ciclo de vida do arquivo + os 3 estados | **nota 03** |
| Regras de `.gitignore` | **nota 06** |
| **Máquina do tempo com múltiplas linhas temporais** (metáfora de branch) | **nota 08** — a metáfora que faz branch "clicar" antes do modelo |
| **Sequência de 9 diagramas de branching** (branch é ponteiro → HEAD → checkout → commit avança → volta pro main) | **nota 19** — é literalmente a nota "refs, HEAD e branch como ponteiro"; redesenhar em Mermaid |
| *"Tudo tem checksum SHA-1"* + *"Git só adiciona dados"* + snapshots×diferenças | **notas 17, 18 e 23** — o núcleo do nível 3 |
| Diagramas merge × rebase | **nota 21** |
| Múltiplos remotes (*"SIM! Com o git, podemos ter vários remotos!"*) | **nota 11** |
| Tags leves × anotadas | **nota 14** |
| **Pendrive como servidor Git** | **nota 11** — exercício que prova que "remote" é só outro repositório, sem mágica |
| Mapa de recursos PT-BR com badges de idioma | **Biblioteca do domínio** (já incorporado) |

### Datado — usar com ressalva

- **GitKraken/TortoiseGit/SourceTree** dominam o `curso-git-github` e o `workshop-git`. Hoje o eixo do vault é CLI + [[03-Dominios/Tecnologia/Terminal/index|Lazygit]]. As GUIs entram como **menção de uma linha** na nota 02, não como fio condutor.
- **`master`** em todo o material de 2016-17 → escrever `main`, com nota de rodapé sobre a mudança de 2020.
- **`git checkout`** pra trocar de branch e descartar arquivo → ensinar `switch`/`restore` (Git 2.23+) como forma primária, com `checkout` explicado como o comando antigo que faz as duas coisas (e por isso confunde).
- **`git-flight-rules`**, GitHub Guides e o link do GirlsTechTalkClub: o último está **404** (verificado 2026-07-31) — sai do mapa.

---

## Roster — 7 sub-galhos + capstone (34 notas)

### N0 · SG1 — Sobrevivência (Iniciado, 5 notas)

*Meta do nível: ao fim, a pessoa versiona um projeto sozinha e não perde trabalho. Zero teoria que não seja necessária pra isso.*

> [!important] Público do N0 — decisão de 2026-07-31
> O N0 é escrito para **público geral**: o estudante ou acadêmico que precisa parar de perder arquivos (monografia, dissertação, tese, artigo, trabalho em grupo). **Não pressupõe programação.** O dev iniciante é servido pelo mesmo texto — o fluxo é idêntico —, mas os exemplos primários são de **documentos**, não de código, e o vocabulário de programação só entra quando é inevitável (e aí explicado).
>
> Consequências: exemplos com `.docx`/`.tex`/`.csv`; a linha de comando é apresentada como ferramenta neutra, não como pressuposto; toda menção a "projeto" vale igualmente pra software e pra texto acadêmico; herda o registro do workshop [`escrita-sem-medo-com-git-e-github`](https://github.com/josenaldo/escrita-sem-medo-com-git-e-github).
>
> A partir do **N1** o público estreita gradualmente pro perfil dev, e do **N3** em diante é assumidamente técnico.

| # | Nota | Ângulo |
|---|------|--------|
| 01 | O problema que o Git resolve | `tcc-final-v3-AGORA-VAI.docx`; as 4 perguntas; VCS local→centralizado→distribuído; nascimento do Git; **o que o Git NÃO faz** |
| 02 | Instalar e configurar | identidade, editor, `git help`; menção a GUIs e ao Lazygit |
| 03 | Seu primeiro repositório | `init`, `status`, `add`, `commit`, `log` — o ciclo de vida do arquivo e os 3 estados como *receita* |
| 04 | Desfazer sem susto (nível 0) | `restore`, `restore --staged`, `commit --amend`; a regra "antes de compartilhar, é livre" |
| 05 | GitHub — colocar o repo na nuvem | conta, `remote add`, `push`, `clone`, README; `clone ≠ checkout` |

### N1 · SG2 — O fluxo diário (Iniciado/Adepto, 6 notas)

*Meta: operar Git num projeto real, sozinho ou em dupla.*

| # | Nota | Ângulo |
|---|------|--------|
| 06 | Ignorar arquivos — `.gitignore` e suas regras | ordem das regras, negação, o que nunca commitar |
| 07 | Ler o histórico — `log` e `diff` | formatos de log, `--graph`, ler um diff sem medo |
| 08 | Branches na prática — a máquina do tempo com linhas paralelas | `switch -c`, mesclar, deletar; **metáfora antes do modelo** |
| 09 | Conflito — por que acontece e como resolver sem pânico | conflito não é erro; anatomia dos marcadores; mergetool |
| 10 | Guardar trabalho pela metade — `stash` e worktrees | worktree como alternativa superior ao stash |
| 11 | Sincronizar com o time — `fetch`, `pull`, `push` | remote-tracking branch; **múltiplos remotes**; pendrive como servidor; `--force-with-lease` |

### N2 · SG3 — Colaborar (Adepto, 5 notas)

| # | Nota | Ângulo |
|---|------|--------|
| 12 | Pull requests e a cultura de code review | tamanho de PR, review como ensino, o que automatizar |
| 13 | Estratégias de branching — trunk-based, GitHub Flow, GitFlow | qual o legado usa e por quê; custo de cada uma |
| 14 | Anatomia de um bom commit — Conventional Commits, tags e semver | commit como comunicação; tag leve × anotada; changelog |
| 15 | GitHub como plataforma — issues, projects, rulesets, CODEOWNERS | branch protection, ambientes |
| 16 | `gh` CLI e automação do fluxo | absorve `Infraestrutura/GitHub CLI.md` |

### N3 · SG4 — O modelo por baixo (Adepto/Magus, 5 notas)

*O ponto de virada. Recontextualiza como mecanismo tudo que os níveis 0-2 ensinaram como receita.*

| # | Nota | Ângulo |
|---|------|--------|
| 17 | Tudo tem hash — o modelo de objetos | blob, tree, commit, tag; `cat-file`; conteúdo endereçado |
| 18 | Commit é snapshot, não diff — o DAG | por que o histórico é um grafo; o diff é calculado, não guardado |
| 19 | Refs, HEAD e branch como ponteiro de 41 bytes | a sequência de diagramas do `workshop-git`, em Mermaid; detached HEAD deixa de assustar |
| 20 | O index por dentro | o que `add` realmente faz; por que a área de stage existe |
| 21 | Merge e rebase por dentro — three-way e replay | ancestral comum; por que o conflito é inevitável; fast-forward |

### N4 · SG5 — Quando dá errado (Magus, 5 notas)

| # | Nota | Ângulo |
|---|------|--------|
| 22 | A árvore de decisão do desfazer | `reset` (soft/mixed/hard) × `restore` × `revert` × `checkout`; história publicada × local |
| 23 | `reflog` — *"o Git só adiciona dados"* | recuperar commit perdido, branch deletada, `reset --hard`; o GC e a janela real |
| 24 | Reescrever história com segurança | `rebase -i`, `cherry-pick`, a regra de ouro, `--force-with-lease` |
| 25 | Segredos no histórico — quando vaza | `filter-repo`, **rotação obrigatória**, secret scanning, prevenção |
| 26 | Configurar o Git a seu favor | aliases, `rerere`, hooks, `.gitattributes`, `autosetuprebase` |

### N5 · SG6 — Repositórios reais (Magus, 4 notas)

| # | Nota | Ângulo |
|---|------|--------|
| 27 | Monorepo × polyrepo — sparse-checkout, partial clone, LFS | quando o repo não cabe mais no clone completo |
| 28 | Submódulos e subtrees | por que submódulo dói; quando ainda assim é a resposta |
| 29 | Cirurgia de repositório | migração SVN→Git, split, merge de repos, reescrita em massa |
| 30 | Git no CI/CD e GitOps | contrato repo↔pipeline; shallow clone, tags, ambientes |

### N6 · SG7 — O repositório como testemunha (Magus, 3 notas)

*A lente do consultor de legado. É o nível que justifica o domínio existir.*

| # | Nota | Ângulo |
|---|------|--------|
| 31 | Ler história de verdade — `blame`, pickaxe (`-S`/`-G`), `--follow` | achar quando uma linha nasceu e por quê |
| 32 | `bisect` — encontrar o commit que quebrou | manual e automatizado (`bisect run`) |
| 33 | Forense de repositório — hotspots, coautoria, silos | o que a frequência de mudança revela sobre o design |

### Capstone

| # | Nota | Ângulo |
|---|------|--------|
| 34 | Capstone — assumir um repositório desconhecido | primeiras 4 horas num repo alheio: mapear história, achar donos, medir hotspots, decidir o fluxo. Costura N6 + N2 + N3 |

---

## Prática delegada a simuladores

O risco declarado é virar mais um tutorial de Git. A defesa é **separar modelo de repetição**: a nota entrega o modelo, o simulador entrega a repetição.

**Convenção obrigatória:** toda nota de **N0 a N4** fecha com callout `[!tip] Pratique` apontando pro **nível/exercício específico** — nunca pra home do site. Ex.: nota 19 (refs/HEAD) → nível de *relative refs* do Learn Git Branching; nota 23 (reflog) → kata de commit perdido do git-katas.

Acervo em [[03-Dominios/Tecnologia/Controle de Versão/Biblioteca de Controle de Versão|Biblioteca de Controle de Versão]], com bloco PT-BR incorporado do `aprendendo-git-e-github`.

---

## Fronteiras — o que NÃO entra aqui

| Assunto | Casa canônica | Como este domínio trata |
|---|---|---|
| CI/CD como disciplina de entrega | [[03-Dominios/Engenharia/Operação/index\|Engenharia/Operação]] | nota 30 cobre só o **contrato repo↔pipeline** |
| GitOps e IaC | `Operação/2 - Entrega e release/05` | callout na 30 |
| git hooks no ecossistema JS (husky, lint-staged) | [[03-Dominios/Tecnologia/Tooling e Build/index\|Tooling e Build]] (16) | nota 26 cobre hooks como mecanismo do Git |
| Lazygit, delta, TUIs | [[03-Dominios/Tecnologia/Terminal/index\|Terminal]] | **fica no Terminal**; nota 02 linka |
| Bare repo pra dotfiles | `Terminal/Dotfiles/06` | callout na 27 |
| `git-crypt`, `age`, `sops` | `Terminal/Dotfiles/07` | nota 25 trata do vazamento, não da ferramenta |
| Supply chain de dependências | `Tooling e Build/24` | callout na 25 |
| Arqueologia de software (o ofício) | [[03-Dominios/Engenharia/Arqueologia e Restauração de Software/index\|Engenharia/Arqueologia]] | N6 é o **instrumento**; a Arqueologia é o **método** |

---

## Material do vault a consumir

| Arquivo | Destino |
|---|---|
| `Tecnologia/Ferramentas/Versionamento.md` (9.8K) | sementes das notas 13, 14, 22; vira tronco podado ou é excluído |
| `Tecnologia/Infraestrutura/GitHub CLI.md` (45K) | semente da nota 16; Infra fica com callout |

---

## Ordem de construção

Sequencial **na ordem dos níveis** (N0 → N6 → capstone), com validação a cada bloco. Diferente do desenho original, aqui a ordem de construção **é** a ordem de leitura: como o material vai ser compartilhado, cada nível precisa ser publicável e útil sozinho, antes do próximo existir.

---

## Veja também

- [[00-Meta/Roadmap|Roadmap de Trilhas]] — Tier 0
- [[03-Dominios/Tecnologia/Controle de Versão/index|Índice do domínio]]
