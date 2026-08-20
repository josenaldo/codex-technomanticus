---
title: "Ler o histórico — log e diff"
created: 2026-07-31
updated: 2026-07-31
type: concept
status: seedling
fase: Iniciado
tags:
  - controle-de-versao
  - git
  - tecnologia
publish: true
---

# Ler o histórico — `log` e `diff`

> [!abstract] TL;DR
> Ter histórico não serve de nada se você não souber consultá-lo. `git log` responde "o que aconteceu" e aceita filtros por período, autor e arquivo; `git show` abre um commit específico; `git diff` compara dois pontos quaisquer e mostra linha a linha o que entrou e o que saiu. Ler um diff assusta na primeira vez e leva cinco minutos para virar automático — `-` é o que sumiu, `+` é o que entrou.

---

## A pergunta que aparece no mês três

Você tem uns duzentos commits. A orientadora comenta: *"na versão que li em abril, a justificativa estava mais forte — o que você mudou ali?"*.

Sem histórico, a resposta é um encolher de ombros. Com histórico mas sem saber consultá-lo, é rolar uma lista gigante procurando visualmente. Com os comandos desta nota, são trinta segundos.

O histórico do Git não é um arquivo morto. É um banco de dados que responde perguntas — e as boas perguntas são quase sempre estas quatro: **o que mudou, quando, quem fez, e o que exatamente foi alterado**.

---

## `git log`, com filtros

Sem argumento nenhum, `git log` despeja tudo. O que torna o comando útil são os recortes:

```bash
git log --oneline                     # uma linha por commit — o formato do dia a dia
git log --oneline -10                 # só os 10 últimos
git log --oneline --graph             # desenha as linhas paralelas (útil depois da nota 08)
git log --since="2026-04-01" --until="2026-04-30"   # só abril
git log --author="Ana"                # só de uma pessoa
git log --oneline -- capitulo-2.tex   # só commits que tocaram este arquivo
git log --stat                        # quais arquivos e quantas linhas em cada commit
git log -p -- capitulo-2.tex          # o conteúdo de cada mudança neste arquivo
```

Os dois traços isolados (`--`) antes do nome do arquivo servem para o Git não confundir nome de arquivo com nome de ramo. Quando não houver ambiguidade eles são opcionais, mas o hábito de escrevê-los evita erros bizarros.

Aquela pergunta da orientadora se responde assim:

```bash
git log --oneline --since="2026-04-01" -- capitulo-1.tex
```

E, para saber quem contribuiu com quanto num trabalho em grupo:

```bash
git shortlog -sn
```

```text
    47  Ana Ribeiro
    31  Bruno Costa
    12  Carla Dias
```

> [!warning] Contagem de commits não é medida de contribuição
> **O que acontece:** alguém usa o `shortlog` para argumentar quem trabalhou mais no grupo. **Por quê:** commits têm tamanhos completamente diferentes. Quem commita a cada parágrafo aparece com o triplo de quem commita a cada seção, fazendo o mesmo trabalho. **Como usar direito:** o `shortlog` serve para ver **quem tocou no quê**, não para ranquear. Para trabalho em grupo, ele é ótimo respondendo "quem mexeu na metodologia?" — não "quem se esforçou mais?".

---

## Abrir um commit específico

Todo commit tem um endereço — aquele código como `a3f1c9d`. Com ele:

```bash
git show a3f1c9d              # mensagem + tudo que mudou naquele commit
git show a3f1c9d -- arq.tex   # só o que mudou neste arquivo, naquele commit
git show a3f1c9d:arq.tex      # o arquivo INTEIRO como estava naquele momento
```

A terceira forma é a mais subestimada: ela imprime o conteúdo completo do arquivo naquele ponto do tempo, sem mexer em nada no seu projeto. É como abrir a fotografia antiga sem desarrumar o presente.

Você também pode se referir a commits por posição relativa, sem decorar códigos:

| Referência | Significa |
|---|---|
| `HEAD` | o commit em que você está agora |
| `HEAD~1` | o anterior |
| `HEAD~5` | cinco commits atrás |
| `main` | o último commit da linha principal |

---

## `git diff` — comparar dois pontos

O `log` diz *que* algo mudou. O `diff` diz *o quê*.

```bash
git diff                    # o que editei e ainda não preparei (add)
git diff --staged           # o que já preparei e ainda não commitei
git diff HEAD               # tudo que mudou desde o último commit
git diff HEAD~1 HEAD        # o que o último commit fez
git diff a3f1c9d c4d2e1a    # entre dois commits quaisquer
git diff main outra-linha   # entre duas linhas de trabalho (nota 08)
```

O primeiro caso — `git diff` puro — é o que você mais vai usar: é a revisão do que você acabou de escrever, antes de registrar.

---

## Anatomia de um diff

A primeira vez que a saída aparece, ela parece hostil. São só quatro elementos:

```diff
diff --git a/capitulo-1.tex b/capitulo-1.tex
--- a/capitulo-1.tex
+++ b/capitulo-1.tex
@@ -42,7 +42,8 @@ \section{Justificativa}
 O problema da evasão escolar tem sido estudado
-desde os anos 80, com foco em fatores econômicos.
+desde os anos 80. A literatura inicial concentrou-se
+em fatores econômicos, deixando de lado o componente
+institucional que este trabalho investiga.
 Nesse contexto, cabe perguntar
```

- **`a/` é o antes, `b/` é o depois.** Sempre nessa ordem.
- **`@@ -42,7 +42,8 @@`** localiza o trecho: a partir da linha 42, o bloco antigo tinha 7 linhas e o novo tem 8. Depois do segundo `@@`, o Git mostra em que seção você está — aqui, `\section{Justificativa}`.
- **Linhas com `-`** saíram. **Linhas com `+`** entraram.
- **Linhas sem sinal** são contexto, mostradas só para você se localizar.

Repare que o Git não sabe que você "reescreveu uma frase": ele vê uma linha removida e três adicionadas. Substituição, para ele, é remoção seguida de adição.

> [!question]- Por que o diff fica ilegível quando eu escrevo texto corrido?
> Porque o Git compara **linha a linha**, e num parágrafo de texto corrido o parágrafo inteiro costuma ser uma única linha imensa. Mudar uma vírgula marca a linha inteira como alterada, e você perde a granularidade. Duas soluções, ambas úteis. A primeira é escrever **uma frase por linha** no arquivo-fonte (LaTeX e Markdown ignoram a quebra ao renderizar, então a saída não muda) — isso transforma o diff em algo verdadeiramente legível. A segunda é pedir comparação por palavra:
> ```bash
> git diff --word-diff
> ```
> Para quem escreve texto no Git, a primeira dica é a que mais muda a vida.

---

## Seguir um arquivo que mudou de nome

```bash
git log --follow -- capitulo-metodologia.tex
```

Sem o `--follow`, o histórico para no ponto em que o arquivo passou a se chamar assim. Com ele, o Git segue a trilha através da renomeação — porque ele não guarda "renomeações", e sim descobre por semelhança de conteúdo que aquele arquivo é a continuação de outro.

---

## Armadilhas comuns

> [!warning] Diff de arquivo binário não diz nada
> **O que acontece:** você pede o diff de um `.docx`, `.pdf` ou imagem e recebe `Binary files a/... and b/... differ`. **Por quê:** já vimos na nota 01 — o Git compara texto, e esses formatos não são texto. **Como conviver:** o histórico continua útil (você sabe *quando* mudou e pode recuperar qualquer versão), você só não tem o "o quê" automático. É o argumento mais forte a favor de escrever em `.tex`, `.md` ou `.qmd`.

> [!warning] O histórico só é tão bom quanto as mensagens
> **O que acontece:** você filtra por período, encontra o commit certo, e a mensagem diz "att". **Por quê:** o Git registra o que você escreveu. Ele não inventa contexto. **Como evitar:** é aqui que a disciplina da nota 03 se paga. Mensagem ruim não incomoda no dia em que você escreve; incomoda seis meses depois, exatamente quando você mais precisa.

> [!warning] `git log` abre um paginador e parece travar
> **O que acontece:** a saída ocupa a tela, aparece um `:` no rodapé e o teclado não responde ao normal. **Por quê:** o Git usa um paginador (`less`) para saídas longas. **Como sair:** tecle `q`. Use as setas ou `espaço` para rolar, e `/palavra` para buscar dentro da saída. Se preferir sem paginador, `git --no-pager log --oneline -10`.

---

## Resumo em uma frase

**`log` acha o commit, `show` abre o commit, `diff` compara dois pontos — e ler `-`/`+` é toda a alfabetização necessária.**

> [!tip] Vídeo — log e show na tela
> [**Curso de git - Histórico e Versões com git log e git show**](https://www.youtube.com/watch?v=pVF7snOnqws) (Boson Treinamentos, 11 min) percorre as opções de `log` e a leitura de um commit com `show`, com a saída real no terminal.

> [!tip] Pratique
> Responda três perguntas sobre o seu próprio projeto, usando só a linha de comando:
> 1. Quantos commits eu fiz no mês passado? (`git log --oneline --since=...` )
> 2. Qual foi a última mudança no arquivo mais importante do projeto? (`git log -p -1 -- arquivo`)
> 3. Como estava aquele arquivo há dez commits? (`git show HEAD~10:arquivo`)
>
> Depois, no sandbox do **[Visualizing Git](https://git-school.github.io/visualizing-git/)**, faça alguns commits e observe como cada um vira um nó ligado ao anterior — a estrutura que o `--graph` desenha em texto.

---

## O que vem a seguir

Até aqui, sua história é uma linha reta: um commit depois do outro. A próxima nota abre a possibilidade mais poderosa do Git — trabalhar em **várias linhas ao mesmo tempo**, testar uma ideia arriscada num ramo separado e descartar ou incorporar depois, sem nunca colocar o trabalho principal em risco.

- **08 — Branches na prática** — a máquina do tempo ganha linhas paralelas.
- [[03-Dominios/Tecnologia/Controle de Versão/N1 - O fluxo diário/06 - Ignorar arquivos - o gitignore e suas regras|06 — Ignorar arquivos]] — o histórico fica muito mais legível quando não há lixo nele.

## Fontes

- **Scott Chacon & Ben Straub** — [*Pro Git*, cap. 2 — "Visualizando o Histórico de Commits"](https://git-scm.com/book/pt-br/v2/Fundamentos-de-Git-Visualizando-o-Hist%C3%B3rico-de-Commits) — filtros de `log`, formatos e limitação por caminho.
- **Git** — [*git-log*](https://git-scm.com/docs/git-log) · [*git-diff*](https://git-scm.com/docs/git-diff) · [*git-show*](https://git-scm.com/docs/git-show) — documentação oficial.
- **Git** — [*gitrevisions*](https://git-scm.com/docs/gitrevisions) — a sintaxe de `HEAD~1`, intervalos e outras formas de apontar para commits.
- **Josenaldo Matos** — [*curso-git-github*](https://github.com/josenaldo/curso-git-github) (2017), Tomo 6 — "Visualizando o histórico" e "Verificando as mudanças".
