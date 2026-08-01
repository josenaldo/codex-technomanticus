---
title: "Ler história de verdade"
created: 2026-07-31
updated: 2026-07-31
type: concept
status: seedling
fase: Magus
tags:
  - controle-de-versao
  - git
  - legado
  - tecnologia
publish: true
---

# Ler história de verdade

> [!abstract] TL;DR
> Quatro ferramentas respondem quase tudo sobre o passado de um código: **`blame`** diz quem tocou cada linha por último (e com `-w -C` atravessa reformatação e movimentação de arquivo); a **pickaxe** (`log -S`) encontra o commit em que um trecho **apareceu ou sumiu**; **`log -L`** segue a evolução de uma função específica ao longo do tempo; e **`log --diff-filter=D`** acha quando algo foi apagado. A armadilha universal é o `blame` apontar para o commit de reformatação em massa — resolvida com um arquivo de revisões ignoradas.

---

## As perguntas que aparecem no legado

Você abre um arquivo de um sistema com dez anos e encontra:

```java
// não remover — quebra o relatório da diretoria
if (cliente.getTipo() == 3 && !feriado) {
    aplicarDescontoLegado(pedido);
}
```

Três perguntas imediatas: **quando isso entrou? quem escreveu? qual era o problema?** Sem essas respostas, você tem duas opções ruins — mexer no escuro ou não mexer nunca.

O repositório sabe. Só é preciso saber perguntar.

---

## `blame`: quem tocou cada linha por último

```bash
git blame arquivo.java
git blame -L 40,60 arquivo.java        # só um trecho
git blame <commit> -- arquivo.java     # como estava naquele ponto do tempo
```

Cada linha vem com o commit, o autor e a data. Daí você pega o hash e lê o contexto completo:

```bash
git show <hash>                        # a mudança inteira e a mensagem
git log --merges --ancestry-path <hash>..HEAD | tail -5   # por qual PR isso entrou
```

Essa segunda linha é o truque de investigação mais útil da nota: ela encontra o **commit de merge** que trouxe aquele commit para a linha principal. E, com a estratégia de merge do time, a mensagem daquele merge costuma trazer o número do PR — que leva à discussão, à revisão e à issue. É o caminho do código de volta ao *por quê*.

### As três flags que fazem o `blame` funcionar de verdade

```bash
git blame -w -C -C -- arquivo.java
```

- **`-w`** ignora mudanças de espaço em branco. Sem isso, uma reindentação faz o `blame` apontar para quem reindentou.
- **`-C`** detecta linhas **movidas ou copiadas de outro arquivo** no mesmo commit. Repetido (`-C -C`), procura também em arquivos que o commit não tocou.
- **`-M`** detecta movimentação dentro do mesmo arquivo.

Sem elas, num código que passou por refatorações, o `blame` mente com frequência — atribuindo tudo a quem reorganizou.

> [!warning] O commit de reformatação em massa que apaga a história
> **O que acontece:** o time rodou um formatador automático em 2023 e commitou tudo de uma vez. Hoje o `blame` do projeto inteiro aponta para aquele commit e para aquela pessoa.
> **Por quê:** a linha foi de fato modificada — o Git está sendo literal.
> **Como resolver:** liste os commits a ignorar num arquivo e diga ao Git para pulá-los.
> ```bash
> echo "a3f1c9d5e2b8471f0c6d9a3e7b52814f6d0e9c2a  # formatador, 2023" >> .git-blame-ignore-revs
> git config blame.ignoreRevsFile .git-blame-ignore-revs
> ```
> **Versione esse arquivo** — assim todo o time e as plataformas de hospedagem (que o reconhecem) passam a ignorar os mesmos commits. Fazer isso **no mesmo dia** de qualquer reformatação em massa é uma prática que poupa anos de `blame` inútil.

---

## Pickaxe: quando este trecho apareceu ou sumiu

O `blame` responde sobre o estado atual. Ele não ajuda quando o que você procura **não está mais lá** — a função que foi removida, a constante que sumiu, o `TODO` que alguém apagou.

```bash
git log -S"aplicarDescontoLegado" --oneline           # commits que MUDARAM a quantidade de ocorrências
git log -S"aplicarDescontoLegado" -p                  # com o diff junto
git log -G"desconto.*legado" --oneline                # regex: commits cujo diff casa com o padrão
git log -S"CHAVE_API" --all                           # em todos os ramos
```

A diferença entre `-S` e `-G` importa:

- **`-S`** conta ocorrências: mostra só os commits onde a quantidade daquele texto **mudou** — tipicamente onde ele nasceu e onde morreu. É preciso e silencioso.
- **`-G`** casa contra o texto do diff: mostra todo commit cujo diff mencione o padrão, inclusive movimentações. É abrangente e ruidoso.

Comece com `-S`. Ele é a ferramenta certa para "quando esta coisa entrou no código?", e costuma devolver dois ou três commits em vez de duzentos.

---

## `log -L`: a evolução de uma função

```bash
git log -L :aplicarDescontoLegado:PedidoService.java     # por nome de função
git log -L 40,60:arquivo.java                            # por faixa de linhas
```

Ele reconstrói a história daquele trecho ao longo do tempo, seguindo movimentações. É a visão que responde "como esta função chegou a este estado", mostrando cada modificação em ordem — muito mais direto que ler o histórico do arquivo inteiro.

---

## Quando foi apagado

```bash
git log --diff-filter=D --oneline -- caminho/do/arquivo.java     # o commit que deletou
git log --all --full-history -- caminho/do/arquivo.java          # tudo que tocou o arquivo, mesmo removido
git show <hash>^:caminho/do/arquivo.java                          # o conteúdo antes de sumir
```

O `--full-history` é necessário porque, por padrão, o Git simplifica o histórico e pode omitir commits que ele julga irrelevantes para o estado atual — o que é exatamente o que você **não** quer numa investigação.

O `^` no último comando é "o pai do commit" (nota 18): você está pedindo o arquivo como estava imediatamente antes da remoção.

---

## Outras perguntas úteis

```bash
# quem mais mexeu neste arquivo (candidatos a conversar)
git shortlog -sn --no-merges -- src/pagamentos/

# o que mudou entre duas versões publicadas
git log --oneline v1.4.0..v1.5.0

# quando este arquivo foi renomeado
git log --follow --name-status --oneline -- arquivo.java

# quais commits tocaram este arquivo E aquele
git log --oneline -- a.java b.java

# o commit está em qual release?
git tag --contains <hash>
git branch -a --contains <hash>
```

O último par é ouro em investigação de incidente: `git tag --contains` responde **em quais versões publicadas** aquele commit está — ou seja, quem foi afetado.

---

## Armadilhas comuns

> [!warning] Confiar no `blame` como atribuição de culpa
> **O que acontece:** o nome que aparece é usado para responsabilizar alguém.
> **Por quê:** além de o `blame` mostrar apenas *quem tocou por último* — que pode ter só reindentado, ou aplicado uma mudança decidida por outra pessoa —, o uso punitivo destrói a disposição do time em mexer em código antigo.
> **Como usar direito:** o `blame` é para achar **contexto** e **com quem conversar**, não culpado. A pergunta útil é "você lembra por que isso ficou assim?", nunca "por que você fez isso?".

> [!warning] Investigar num clone raso
> **O que acontece:** `blame` mostra tudo atribuído ao commit inicial, pickaxe não acha nada.
> **Por quê:** a história não está lá (notas 27 e 30).
> **Como evitar:** para investigação, clone completo ou parcial — nunca raso.

> [!warning] Parar no commit e não chegar ao contexto
> **O que acontece:** você acha o commit e a mensagem diz "ajustes".
> **Por quê:** a disciplina da nota 14 não existia naquele time.
> **Como contornar:** suba um nível — ache o merge (`--ancestry-path`), o PR, a issue. E, se nada disso existir, olhe os **commits vizinhos no tempo**: `git log --since=<data-1dia> --until=<data+1dia> --all` costuma revelar o que estava acontecendo naquela semana, o que dá contexto mesmo sem mensagem.

---

## Resumo em uma frase

**`blame` responde "quem tocou por último", pickaxe responde "quando isto nasceu ou morreu", `-L` responde "como isto evoluiu" — e o caminho do commit até o PR é o que devolve o *porquê*.**

> [!tip] Pratique
> Pegue um repositório grande e antigo que você não conhece — o do próprio [Git](https://github.com/git/git) serve — e responda três perguntas usando só a linha de comando:
> 1. Quando a opção `--force-with-lease` foi introduzida? (`git log -S"force-with-lease" --oneline | tail -3`)
> 2. Quem escreveu a linha 100 de um arquivo qualquer, ignorando reformatações? (`git blame -w -C -L 100,100 <arquivo>`)
> 3. Aquele commit está em quais versões publicadas? (`git tag --contains <hash>`)
>
> Fazer isso num código alheio, sem contexto nenhum, é exatamente o exercício do capstone — e a sensação de conseguir responder é o argumento deste nível inteiro.

---

## O que vem a seguir

A pickaxe encontra o commit quando você sabe **o que** procurar. E quando você só sabe que **algo** quebrou entre a versão que funcionava e a de hoje, sem ideia de onde? Aí entra a busca binária no grafo.

- **32 — `bisect`: achar o commit que quebrou** — inclusive automatizado.
- [[03-Dominios/Tecnologia/Controle de Versão/N1 - O fluxo diário/07 - Ler o histórico - log e diff|07 — Ler o histórico]] — o básico de `log` e `diff` que esta nota estende.

## Fontes

- **Git** — [*git-blame*](https://git-scm.com/docs/git-blame) — `-w`, `-C`, `-M`, `--ignore-rev` e `blame.ignoreRevsFile`.
- **Git** — [*git-log*](https://git-scm.com/docs/git-log) — `-S` (pickaxe), `-G`, `-L`, `--diff-filter`, `--full-history` e a simplificação de histórico padrão.
- **Scott Chacon & Ben Straub** — [*Pro Git*, cap. 7 — "Buscando"](https://git-scm.com/book/pt-br/v2/Ferramentas-do-Git-Procurando) — `grep`, pickaxe e busca por linha.
- **Git** — [*gitrevisions*](https://git-scm.com/docs/gitrevisions) — `<commit>^`, `--contains` e intervalos.
