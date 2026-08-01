---
title: "N4 — Quando dá errado"
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
  - Quando dá errado
  - Git nível 4
---

# N4 — Quando dá errado

> [!abstract] TL;DR
> O nível que separa quem sabe Git de quem sobrevive a ele. Desfazer com precisão em vez de tentativa e erro, recuperar o que parecia perdido, reescrever a história sem quebrar a de ninguém, agir quando um segredo vaza, e configurar a ferramenta para que ela trabalhe a seu favor. **Nada aqui é decorável** — tudo decorre do modelo do [[03-Dominios/Tecnologia/Controle de Versão/N3 - O modelo por baixo/index|nível 3]]: objetos imutáveis, refs de 41 bytes, alcançabilidade.

Este é o nível que você procura em pânico, às onze da noite, com um `push --force` já dado. Ele foi escrito para ser útil nesse estado: cada nota abre pelo sintoma, e as respostas vêm antes das explicações.

---

## As 5 notas

| # | Nota | Para quando |
|---|------|-------------|
| 22 | [[03-Dominios/Tecnologia/Controle de Versão/N4 - Quando dá errado/22 - A árvore de decisão do desfazer\|A árvore de decisão do desfazer]] | "quero desfazer, mas não sei qual comando" |
| 23 | [[03-Dominios/Tecnologia/Controle de Versão/N4 - Quando dá errado/23 - reflog - nada se perde de fato\|`reflog` — nada se perde de fato]] | "sumiu" |
| 24 | [[03-Dominios/Tecnologia/Controle de Versão/N4 - Quando dá errado/24 - Reescrever história com segurança\|Reescrever história com segurança]] | limpar o ramo antes de propor; corrigir commits antigos |
| 25 | [[03-Dominios/Tecnologia/Controle de Versão/N4 - Quando dá errado/25 - Segredos no histórico\|Segredos no histórico]] | vazou senha, chave ou dado sensível |
| 26 | [[03-Dominios/Tecnologia/Controle de Versão/N4 - Quando dá errado/26 - Configurar o Git a seu favor\|Configurar o Git a seu favor]] | parar de sofrer as mesmas coisas todo dia |

> **Estado (2026-07-31):** **escrita completa — 5/5 notas.** Falta enriquecimento de mídia (M1). Ver o [[03-Dominios/Tecnologia/Controle de Versão/N4 - Quando dá errado/roadmap|roadmap do nível]].

---

## A regra que atravessa o nível inteiro

> **Antes de publicar, a história é sua e você pode reescrevê-la. Depois de publicar, ela é de todos — e a correção passa a ser um commit novo, não uma alteração do passado.**

Ela apareceu como conselho na nota 04, virou aviso na 11 e 12, ganhou mecanismo na 21. Aqui ela é o critério que separa as duas metades de quase toda árvore de decisão.

---

## Veja também

- [[03-Dominios/Tecnologia/Controle de Versão/index|Controle de Versão]] — o domínio e os 7 níveis
- [[03-Dominios/Tecnologia/Controle de Versão/N3 - O modelo por baixo/index|N3 — O modelo por baixo]] — o mecanismo de que este nível depende
- [[03-Dominios/Tecnologia/Controle de Versão/Biblioteca de Controle de Versão|Biblioteca]] — *Oh Shit, Git!?!* e os *git-katas* são o par prático deste nível
