---
title: "N6 — O repositório como testemunha"
type: moc
publish: true
created: 2026-07-31
updated: 2026-07-31
status: seedling
tags:
  - moc
  - controle-de-versao
  - git
  - legado
aliases:
  - O repositório como testemunha
  - Git nível 6
  - Forense de repositório
---

# N6 — O repositório como testemunha

> [!abstract] TL;DR
> Os seis níveis anteriores usaram o repositório para **guardar** trabalho. Este o usa para **investigar** — um sistema que você não escreveu, cuja documentação não existe e cujos autores saíram da empresa. `blame` e pickaxe respondem *quando e por que esta linha existe*; `bisect` encontra o commit exato que quebrou algo; a análise de frequência de mudança revela onde o design dói e quem sabe o quê. É o nível que justifica este domínio existir.

---

## A virada de uso

Um repositório de dez anos é o registro mais completo e mais honesto que existe sobre um sistema. Ele não é uma documentação que alguém escreveu com boas intenções e abandonou: é o rastro do que **de fato** aconteceu, commit a commit, com data, autoria e — quando o time teve disciplina (nota 14) — motivo.

Nada mais no projeto tem essa propriedade. O código diz *o que é hoje*. Os testes dizem *o que se esperava*. Só o histórico diz **como chegou aqui** — e "como chegou aqui" costuma ser a informação que falta para decidir o que fazer a seguir.

> [!info] A relação com a arqueologia de software
> Este sub-galho é o **instrumento**; o **método** de assumir e trabalhar com sistemas legados mora em [[03-Dominios/Engenharia/Arqueologia e Restauração de Software/index|Engenharia/Arqueologia e Restauração de Software]].
> A divisão é deliberada: aqui você aprende o que os comandos revelam e como interpretá-los; lá, o ofício de conduzir a investigação, negociar com quem paga a conta e decidir o que refatorar.

---

## As 3 notas + capstone

| # | Nota | A pergunta que responde |
|---|------|-------------------------|
| 31 | [[03-Dominios/Tecnologia/Controle de Versão/N6 - O repositório como testemunha/31 - Ler história de verdade\|Ler história de verdade]] | "por que esta linha existe?" · "quando este comportamento entrou?" |
| 32 | [[03-Dominios/Tecnologia/Controle de Versão/N6 - O repositório como testemunha/32 - bisect - achar o commit que quebrou\|`bisect` — achar o commit que quebrou]] | "qual commit exatamente causou isto?" |
| 33 | [[03-Dominios/Tecnologia/Controle de Versão/N6 - O repositório como testemunha/33 - Forense de repositório\|Forense de repositório]] | "onde dói mais?" · "quem sabe o quê?" · "o que muda sempre junto?" |
| 34 | [[03-Dominios/Tecnologia/Controle de Versão/34 - Capstone - assumir um repositório desconhecido\|Capstone — assumir um repositório desconhecido]] | as primeiras quatro horas num repositório alheio |

> **Estado (2026-07-31):** **escrita completa — 3/3 notas + capstone.** Falta enriquecimento de mídia (M1). Ver o [[03-Dominios/Tecnologia/Controle de Versão/N6 - O repositório como testemunha/roadmap|roadmap do nível]].

---

## Veja também

- [[03-Dominios/Tecnologia/Controle de Versão/index|Controle de Versão]] — o domínio e os 7 níveis
- [[03-Dominios/Engenharia/Arqueologia e Restauração de Software/index|Engenharia/Arqueologia e Restauração de Software]] — o método que usa este instrumento
- [[03-Dominios/Tecnologia/Controle de Versão/N3 - O modelo por baixo/18 - Commit é snapshot não diff - o DAG|18 — o DAG]] — a estrutura que todas as buscas deste nível percorrem
