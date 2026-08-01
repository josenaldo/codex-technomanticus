---
title: "Capstone — assumir um repositório desconhecido"
created: 2026-07-31
updated: 2026-07-31
type: concept
status: seedling
fase: Magus
tags:
  - controle-de-versao
  - git
  - legado
  - capstone
  - tecnologia
publish: true
---

# Capstone — assumir um repositório desconhecido

> [!abstract] TL;DR
> O exercício que costura os sete níveis: você recebe acesso a um repositório que nunca viu, de um sistema em produção, sem documentação e sem os autores originais. Em **quatro horas**, usando só o que o repositório contém, você deve sair sabendo o que é aquele sistema, quem o construiu, onde está o risco, como o time trabalhava, e por onde começar. Este roteiro é a sequência de perguntas — e cada uma delas usa uma nota deste domínio.

---

## A situação

É segunda-feira. Você foi contratado para cuidar de um sistema que sustenta a operação de uma empresa há oito anos. Recebeu:

- acesso de leitura ao repositório;
- o nome de duas pessoas que "sabem alguma coisa" e não têm agenda esta semana;
- uma pasta compartilhada com documentação de 2019.

Não recebeu: visão geral da arquitetura, mapa de módulos, histórico de decisões, ou qualquer indicação do que é perigoso mexer.

**O repositório tem todas essas informações.** Não em prosa, mas em evidência — e as próximas quatro horas são sobre extraí-la.

> [!info] Por que quatro horas, e por que sozinho
> Porque é o tempo que você tem antes da primeira reunião em que alguém vai perguntar "e aí, o que achou?". Chegar nela com **evidência** em vez de impressão muda toda a relação seguinte — e é uma das habilidades mais concretas que este domínio entrega.

---

## Hora 1 — O terreno

**Clone com a história inteira.** Nada de raso (notas 27 e 30) — a investigação depende dela.

```bash
git clone --filter=blob:none <url> projeto && cd projeto
```

**Qual é o tamanho e a idade disto?**
```bash
git log --oneline | wc -l                      # quantos commits
git log --reverse --format="%ad %an" | head -1 # quando começou, e por quem
git log -1 --format="%ad"                      # último commit — o projeto está vivo?
du -sh .git                                    # peso do repositório
```

**Como o time trabalhava?**
```bash
git log --merges --oneline | head -20          # usam PR? qual o padrão de merge?
git branch -r --sort=-committerdate | head -30 # ramos vivos e ramos fósseis (nota 13)
git tag --sort=-creatordate | head -20         # há releases? com que ritmo?
git log --format="%s" | head -50               # convenção de mensagem? (nota 14)
```

Essas quatro respostas já dizem muito: um projeto com merges de PR, tags regulares e mensagens padronizadas foi cuidado; um com commits diretos na `main`, sem tag e mensagens "ajustes" te conta outra história — e ambas são informação útil sobre o que esperar.

**O que o repositório declara sobre si?**
```bash
ls -a                     # README, CONTRIBUTING, CODEOWNERS, .github/, .gitattributes
cat .gitignore            # o que eles decidiram não versionar (nota 06)
cat .gitmodules 2>/dev/null   # depende de outros repositórios? (nota 28)
```

Um `CODEOWNERS` (nota 15) é um presente: ele é o mapa de responsabilidade que ninguém escreveu em prosa.

---

## Hora 2 — Quem, e quanto disso ainda existe

**Quem construiu isto?**
```bash
git shortlog -sn --no-merges | head -20
```

**Quanto do conhecimento saiu pela porta?** (nota 33)
```bash
git shortlog -sn --no-merges --since="1 year ago"    # quem está ativo
git shortlog -sn --no-merges --until="1 year ago"    # quem construiu
```

Cruze as duas listas. A proporção de autoria histórica que não aparece na lista recente é o seu **risco de conhecimento**, e é um número que vale levar para a primeira reunião.

**Onde cada pessoa atuava?**
```bash
git shortlog -sn --no-merges -- src/pagamentos/
git shortlog -sn --no-merges -- src/relatorios/
```

Isso responde com quem falar sobre o quê — inclusive fora da empresa, se as duas pessoas disponíveis não cobrirem as áreas críticas.

**O projeto está acelerando ou desacelerando?**
```bash
git log --pretty=format:"%ad" --date=format:"%Y-%m" | sort | uniq -c
```

Uma queda acentuada de atividade costuma marcar o momento em que o time original saiu — e é a fronteira entre o código que alguém entendia e o código que foi mantido no escuro.

---

## Hora 3 — Onde dói

**Os hotspots** (nota 33):
```bash
git log --since="2 years ago" --name-only --pretty=format: \
  | grep -v '^$' | sort | uniq -c | sort -rn | head -25
```

Cruze essa lista com o tamanho e a complexidade dos arquivos. Os que aparecem no topo **e** são grandes são onde o custo de cada mudança futura será pago.

**Cuidado com os falsos positivos** (nota 33): commits de migração e reformatação em massa distorcem tudo.
```bash
git log --shortstat --oneline | sort -k5 -rn | head -10   # os commits gigantes
```
Se encontrar um desses, considere excluí-lo das contagens — e, se ele for uma reformatação, proponha o `.git-blame-ignore-revs` (nota 31) como primeira contribuição sua ao projeto. É pequena, indolor e melhora a vida de todo mundo dali em diante.

**O que muda sempre junto?** Pegue os três arquivos do topo e veja o que os acompanha:
```bash
git log --format="%H" -- src/pagamentos/Faturamento.java \
  | while read c; do git show --name-only --pretty=format: "$c"; done \
  | sort | uniq -c | sort -rn | head -10
```
Arquivos que aparecem em quase todos os commits daquele arquivo estão acoplados na prática, mesmo que o código não mostre.

**Há sinais de problema conhecido?**
```bash
git log --oneline --grep="hotfix\|urgente\|rollback\|revert" -i | head -20
git log --oneline --grep="workaround\|gambiarra\|temporário" -i | head -20
```
Commits de emergência marcam onde o sistema já falhou em produção. Reverts marcam onde alguém tentou mudar algo e voltou atrás — e o motivo, quando existe, é a informação mais valiosa que você vai achar hoje.

---

## Hora 4 — Perguntas específicas e a síntese

Agora você tem uma lista de suspeitos. Escolha os três arquivos mais críticos e investigue cada um (nota 31):

```bash
git blame -w -C -C -L 1,80 -- <arquivo>          # quem, ignorando reformatação
git log --oneline -20 -- <arquivo>               # a história recente dele
git log -S"<constante ou flag estranha>" --oneline   # quando aquilo entrou (pickaxe)
git log --merges --ancestry-path <hash>..HEAD | tail -5   # por qual PR entrou
```

E, se houver um comportamento estranho que você consiga reproduzir, o `bisect` (nota 32) o localiza antes do fim do dia.

### O que você deve ter ao final

Um documento de uma página, com evidência para cada afirmação:

| Item | Como você sabe |
|---|---|
| Idade, tamanho e ritmo do projeto | contagem de commits, primeiro e último commit, atividade por mês |
| Como o time trabalhava | padrão de merge, tags, mensagens, arquivos de governança |
| Risco de conhecimento | autoria histórica × autoria recente, por área |
| Os 5 pontos mais caros de mexer | hotspots cruzados com complexidade |
| Acoplamentos não declarados | arquivos que mudam sempre junto |
| Histórico de dor | hotfixes, reverts, workarounds |
| Dependências externas de repositório | submódulos, LFS, subtrees |
| **Três perguntas para as pessoas disponíveis** | o que a evidência não explicou |

A última linha é a mais importante. O tempo das duas pessoas que ainda sabem alguma coisa é o recurso mais escasso do projeto — e gastá-lo perguntando o que o repositório responde sozinho é desperdício. **Use-o para o que só elas sabem: as decisões que não deixaram rastro.**

---

## Como isso costura os sete níveis

| Nível | O que você usou |
|---|---|
| **N0** | clonar, entender o que o repositório é e o que ele não guarda |
| **N1** | ler o histórico, `log` com filtros, ler diffs |
| **N2** | reconhecer estratégia de branching, padrão de commit, governança da plataforma |
| **N3** | saber que ramo é ponteiro (ramos fósseis), que commit é snapshot, o que `--contains` significa |
| **N4** | `reflog` se você mexer errado; reconhecer sinais de reescrita de história |
| **N5** | detectar submódulos, LFS, cirurgias passadas, clone completo × raso |
| **N6** | `blame`, pickaxe, `bisect`, hotspots, acoplamento temporal, ilhas de conhecimento |

E fecha a lente do domínio: o repositório é **fonte de verdade** (foi assim que o time trabalhou) e **testemunha** (foi isto que aconteceu com o sistema).

> [!warning] O limite honesto deste exercício
> O repositório registra o que foi feito, não o que se pretendia. Ele não guarda as decisões tomadas em reunião, os requisitos que mudaram, a pressão de prazo que produziu aquele módulo, nem o contexto de negócio que fazia sentido em 2019. Quatro horas de investigação dão a você um mapa **do território**, não das intenções.
> Confundir uma coisa com a outra é o erro mais comum de quem chega com boa ferramenta e pouca humildade — e leva a diagnósticos tecnicamente corretos e politicamente suicidas. O que fazer com o mapa é o ofício, e mora em [[03-Dominios/Engenharia/Arqueologia e Restauração de Software/index|Engenharia/Arqueologia e Restauração de Software]].

---

## Resumo em uma frase

**Quatro horas de perguntas ao repositório substituem semanas de tentativa e erro — e transformam a primeira reunião de "minhas impressões" em "o que a evidência mostra".**

> [!tip] Vídeo — o mesmo problema, pelo lado do código
> [**7 Techniques to understand Legacy Code**](https://www.youtube.com/watch?v=OzwQXGLWI0g) (Jonathan Boccara, 51 min) ataca a mesma situação deste capstone — chegar num sistema que ninguém explica — mas lendo o **código**, não o repositório. As duas leituras se completam: o roteiro daqui responde quem, quando e onde dói; as técnicas de Boccara respondem o que o código faz.

> [!tip] Pratique
> Faça o roteiro inteiro num repositório de código aberto grande e que você não conhece — [Django](https://github.com/django/django), [Rails](https://github.com/rails/rails) ou o próprio [Git](https://github.com/git/git) servem. Cronometre as quatro horas e produza o documento de uma página.
>
> Depois, confira: leia o `CONTRIBUTING.md` e a documentação de arquitetura do projeto e veja quanto do que você deduziu bate. O que você acertou sem ler nada é a medida do que este domínio entregou.

---

## O que vem a seguir

Este é o fim do caminho de sete níveis. Do `tcc-final-v3-AGORA-VAI.docx` até ler um sistema de oito anos pelo rastro que ele deixou.

- [[03-Dominios/Tecnologia/Controle de Versão/index|Controle de Versão]] — o mapa completo, para revisar qualquer nível
- [[03-Dominios/Engenharia/Arqueologia e Restauração de Software/index|Engenharia/Arqueologia e Restauração de Software]] — o método que consome este instrumental
- [[03-Dominios/Tecnologia/Controle de Versão/Biblioteca de Controle de Versão|Biblioteca de Controle de Versão]] — simuladores, livros e material em português para aprofundar

## Fontes

- **Adam Tornhill** — *Your Code as a Crime Scene* — o roteiro de análise forense que estrutura as horas 2 e 3.
- **Michael Feathers** — *Working Effectively with Legacy Code* — o enquadramento de "código sem testes" e por onde começar a mexer, complementar ao mapa de risco produzido aqui.
- **Git** — [*git-log*](https://git-scm.com/docs/git-log) · [*git-shortlog*](https://git-scm.com/docs/git-shortlog) · [*git-blame*](https://git-scm.com/docs/git-blame) · [*git-bisect*](https://git-scm.com/docs/git-bisect) — os comandos usados no roteiro.
- **Josenaldo Matos** — [*workshop-git*](https://github.com/josenaldo/workshop-git) · [*curso-git-github*](https://github.com/josenaldo/curso-git-github) · [*escrita-sem-medo-com-git-e-github*](https://github.com/josenaldo/escrita-sem-medo-com-git-e-github) · [*aprendendo-git-e-github*](https://github.com/josenaldo/aprendendo-git-e-github) — os quatro workshops que serviram de base pedagógica deste domínio.
