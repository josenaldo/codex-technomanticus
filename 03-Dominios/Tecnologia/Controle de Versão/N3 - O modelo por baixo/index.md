---
title: "N3 — O modelo por baixo"
type: moc
publish: true
created: 2026-07-31
updated: 2026-07-31
status: seedling
tags:
  - moc
  - controle-de-versao
  - git
aliases:
  - O modelo por baixo
  - Git nível 3
  - Git internals
---

# N3 — O modelo por baixo

> [!abstract] TL;DR
> Este nível **não ensina comando novo**. Ele reexplica tudo o que você usa desde o nível 0 — commit, branch, `add`, merge — em termos do que o Git realmente faz: um banco de objetos endereçados por hash, um grafo dirigido acíclico, arquivos de 41 bytes chamados refs, e um índice binário que é ao mesmo tempo área de preparação e cache. Depois dele, `reset --hard` deixa de ser reza e vira um ponteiro se movendo num grafo.

---

## Por que agora, e não antes

Este é o ponto de virada do domínio, e a posição dele foi escolhida de propósito.

Começar por aqui — blob, tree, DAG — é o que a maioria do material técnico faz, e é o que perde a maioria dos leitores. Sem ter commitado, ramificado e quebrado alguma coisa antes, "commit é um snapshot imutável endereçado por conteúdo" é uma frase sem gancho.

Depois de três níveis de uso, a mesma frase responde perguntas que você já teve: *por que o `--amend` cria um commit novo? Por que ramificar é instantâneo mesmo num repositório gigante? Por que o Git às vezes diz que o arquivo mudou quando eu só troquei de ramo?*

**A promessa deste nível:** você vai parar de decorar regras e passar a deduzi-las. Todas as recomendações que os níveis anteriores pediram por disciplina — não force push, não rebase história publicada, commite antes de trocar de ramo — deixam de ser etiqueta e viram consequência de como a coisa funciona.

---

## As 5 notas

| # | Nota | O que ela reexplica |
|---|------|---------------------|
| 17 | [[03-Dominios/Tecnologia/Controle de Versão/N3 - O modelo por baixo/17 - Tudo tem hash - o modelo de objetos\|Tudo tem hash — o modelo de objetos]] | o que o Git guarda: blob, tree, commit, tag — e por que o nome é o conteúdo |
| 18 | [[03-Dominios/Tecnologia/Controle de Versão/N3 - O modelo por baixo/18 - Commit é snapshot não diff - o DAG\|Commit é snapshot, não diff — o DAG]] | por que o histórico é um grafo, e por que o diff é calculado e não guardado |
| 19 | [[03-Dominios/Tecnologia/Controle de Versão/N3 - O modelo por baixo/19 - Refs HEAD e branch como ponteiro\|Refs, HEAD e branch como ponteiro]] | branch é um arquivo de 41 bytes; `detached HEAD` deixa de assustar |
| 20 | [[03-Dominios/Tecnologia/Controle de Versão/N3 - O modelo por baixo/20 - O index por dentro\|O index por dentro]] | o que `add` realmente faz, e por que a área de preparação existe |
| 21 | [[03-Dominios/Tecnologia/Controle de Versão/N3 - O modelo por baixo/21 - Merge e rebase por dentro\|Merge e rebase por dentro]] | three-way merge, ancestral comum, e por que rebase reescreve |

---

## Veja também

- [[03-Dominios/Tecnologia/Controle de Versão/index|Controle de Versão]] — o domínio e os 7 níveis
- [[03-Dominios/Tecnologia/Controle de Versão/N2 - Colaborar/index|N2 — Colaborar]] — o nível anterior
- [[03-Dominios/Tecnologia/Controle de Versão/Biblioteca de Controle de Versão|Biblioteca]] — *Pro Git* cap. 10 e *Think Like (a) Git* são as leituras que acompanham este nível
