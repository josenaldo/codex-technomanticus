---
title: "Dívida técnica"
created: 2026-06-16
updated: 2026-06-16
type: concept
progress: backlog
status: seedling
publish: false
fase: adepto
tags:
  - fundamentos
  - complexidade-de-software
  - adepto
  - divida-tecnica
  - cunningham
  - refactoring
---

# Dívida técnica

A nota anterior apresentou o tabuleiro das três dívidas e prometeu aprofundar cada uma ([[09 - As três dívidas do software]]). Esta é a primeira: a dívida que vive **no código** — a mais antiga, a mais famosa e, justamente por isso, a mais distorcida. Quase todo mundo já usou a expressão "dívida técnica" numa reunião. Quase ninguém sabe que a metáfora original dizia algo bem diferente do que virou no boca a boca.

> [!abstract] TL;DR
> **Ward Cunningham** cunhou a metáfora da dívida em 1992 (relatório de experiência do WyCash, em OOPSLA). A ideia: *enviar* código com seu entendimento de primeira passada é como **pegar dinheiro emprestado** — tudo bem, *desde que você pague a dívida* refatorando à medida que aprende. O **principal** é o atalho; os **juros** são o arrasto de trabalhar contra código que não está bem certo, e eles **compõem** — quanto mais você carrega a dívida, mais cara fica cada mudança. **Nuance crucial e muito mal-citada:** a metáfora de Cunningham **nunca foi sobre escrever código ruim de propósito** — era sobre a *distância entre o seu entendimento atual e o código*. O **Quadrante de Fowler** (2009) refina: dívida pode ser *deliberada × inadvertida* e *prudente × imprudente* — nem toda dívida é falha moral. Paga-se com **refatoração** ([[14 - Manutenção e evolução]]); a meta é **gerenciar**, não zerar. No fundo, dívida técnica é, em larga medida, **complexidade acidental acumulada no código** ([[02 - Complexidade essencial vs. acidental]]).

## O que é

A metáfora nasceu de um problema bem concreto: como Cunningham, trabalhando num produto financeiro (o WyCash), explicava a *stakeholders* por que valia a pena continuar mexendo num código que "já funcionava". A resposta foi falar a língua deles — a língua de finanças. O trecho original, do relatório de OOPSLA 1992, é curto e cirúrgico:

> [!quote] Cunningham, WyCash (OOPSLA, 1992)
> *"Shipping first time code is like going into debt. A little debt speeds development so long as it is paid back promptly with a rewrite. [...] The danger occurs when the debt is not repaid. Every minute spent on not-quite-right code counts as interest on that debt."*

Repare na lógica: ir pra produção com o código que reflete seu entendimento *de agora* não é o erro — é até saudável, porque acelera o aprendizado. O erro é **não pagar de volta**: deixar o "código não-quite-certo" acumular enquanto seu entendimento avança. Cada minuto trabalhando contra esse código desalinhado **é juro**.

> [!warning] A metáfora que quase todo mundo cita errado
> A leitura popular de "dívida técnica" virou *"escrevemos código porco pra entregar rápido, e isso é a dívida"*. **Não é o que Cunningham disse.** Em 2009 ele gravou um vídeo (*"Debt Metaphor"*) justamente pra corrigir o mal-entendido. O ponto dele era a **distância entre o entendimento e o código** — não a desleixo deliberado. Nas palavras dele, a dívida é *"writing code to reflect your current understanding of a problem even if that understanding is partial"*; e mais — toda a metáfora *"depends upon you writing code that is clean enough to be able to refactor as you come to understand your problem"*. Ou seja: o código precisa estar **limpo o bastante pra ser refatorado**. Quem usa "dívida técnica" como desculpa pra entregar lixo inverteu o sentido original.

O que de fato corrói o sistema, segundo ele, é parar de devolver o aprendizado ao código:

> [!quote] Cunningham, "Debt Metaphor" (2009)
> *"I think that there were plenty of cases where people would rush software out the door and learn things but never, never put that learning back into the program and that by analogy was borrowing money thinking that you never had to pay it back."*

## Principal e juros

A metáfora financeira tem duas partes, e confundi-las atrapalha a conversa. O **principal** é a quantia que você "tomou emprestada": o atalho de implementação em si — a abstração apressada, o módulo emaranhado, o caso de borda deixado pra depois. Pagar o principal é fazer a refatoração que conserta aquilo de uma vez.

Os **juros** são o que você paga *enquanto não quita o principal*: o esforço extra em **toda** mudança futura porque o sistema está mais difícil de entender e alterar do que precisava. Lê-se um código mais confuso, testa-se mais à mão, tropeça-se mais em bugs colaterais. O juro não é um evento — é um **imposto recorrente** sobre cada tarefa que toca a área endividada.

E o detalhe que torna a metáfora perigosa de verdade: **os juros compõem**. Quanto mais tempo a dívida fica, mais código novo se apoia sobre o atalho, mais difícil fica refatorar, e mais cara fica cada mudança seguinte. É a espiral que faz times relatarem que "tudo demora três vezes mais que antes" sem nenhuma feature individual ser difícil — eles estão pagando juros sobre juros.

> [!example] Por que a distinção importa na prática
> Imagine duas decisões. (A) "Vamos cortar esse atalho agora e refatorar na sprint que vem" — você *escolheu o principal de olho aberto*, com plano de quitar. (B) "Faz três anos que ninguém mexe nesse módulo porque ninguém entende" — aí você não está pagando o principal nem percebe os juros; só sente que tudo é lento. O mesmo emaranhado de código pode ser dívida **gerenciada** (A) ou dívida **fora de controle** (B). A diferença não está no código — está em se você sabe que tem a dívida e tem plano de pagá-la.

## O quadrante de Fowler

A genialidade do relatório de Cunningham era também sua armadilha: ao virar slogan, "dívida técnica" passou a tratar *qualquer* imperfeição como pecado. **Martin Fowler** resolveu isso em 2009 com o **Technical Debt Quadrant**, que cruza dois eixos e mostra que **nem toda dívida é igual** — e nem toda é falha moral.

Os dois eixos são: **deliberada × inadvertida** (você *sabia* que estava criando dívida?) e **prudente × imprudente** (a decisão foi pensada ou irresponsável?).

| | **Imprudente** (reckless) | **Prudente** (prudent) |
| --- | --- | --- |
| **Deliberada** (deliberate) | *"We don't have time for design"* — pressa cega, sem plano de pagamento | *"We must ship now and deal with the consequences"* — atalho consciente, com plano de quitar |
| **Inadvertida** (inadvertent) | *"What's layering?"* — ignorância de fundamentos; nem sabe que está se endividando | *"Now we know how we should have done it"* — só dá pra ver o desenho certo *depois* de construir |

O quadrante mais nocivo é o **inadvertido/imprudente** ("o que é camada?"): dívida que você acumula sem saber, por não dominar o básico. O mais defensável é o **inadvertido/prudente** ("agora sabemos como deveríamos ter feito") — e ele é praticamente **inevitável**, porque o entendimento de um domínio só amadurece *construindo* (exatamente o ponto de Cunningham: você escreve com o entendimento parcial de hoje). O **deliberado/prudente** é uma decisão de negócio legítima: entregar antes pra validar mercado, e pagar a dívida com a receita depois.

> [!tip] O que o quadrante te dá
> Ele desarma duas conversas ruins. Contra o gerente que ouve "dívida técnica" e pensa "negligência", você mostra que existe dívida *prudente e inevitável* — a que vem de aprender o domínio. Contra o colega que romantiza qualquer gambiarra como "decisão pragmática", você aponta o quadrante imprudente e pergunta: cadê o plano de pagamento? A dívida deixa de ser xingamento ou desculpa e vira o que sempre foi pra Cunningham: um *trade-off* a administrar.

## Como se paga

A moeda com que se paga dívida técnica é a **refatoração**: mudar a *estrutura* do código **sem mudar o comportamento** observável. É devolver ao código o entendimento que você ganhou — exatamente o "pagar de volta" da metáfora original. Por isso dívida técnica é, no fundo, um tema de **manutenção e evolução** ([[14 - Manutenção e evolução]]): você não refatora por estética, refatora pra baixar os juros que estão encarecendo as próximas mudanças.

Mas o erro simétrico ao "ignorar a dívida" é querer **zerá-la**. Pagar toda dívida sempre é tão irracional financeiramente quanto na vida real — há dívida que *vale a pena carregar*. A dívida deliberada/prudente do quadrante é literalmente isso: às vezes o juro de carregar um atalho por seis meses é mais barato que o custo de oportunidade de não entregar agora. A meta de um time sênior não é dívida zero — é **dívida sob controle**: saber qual dívida você tem, quanto de juro ela cobra, e quitar a que está cara antes que os juros componham.

> [!note] Por que isto é, no fundo, complexidade acidental
> Dívida técnica e [[02 - Complexidade essencial vs. acidental|complexidade acidental]] são quase o mesmo fenômeno vistos por ângulos diferentes. Brooks distingue a complexidade que vem do *problema* (essencial, irredutível) da que vem da *forma como o representamos* (acidental, redutível). A dívida técnica é, em larga medida, **complexidade acidental que se acumulou no código** — emaranhado, duplicação, abstrações erradas que ninguém limpou. Refatorar é, em larga medida, **remover acidental**. A diferença de foco: "complexidade acidental" descreve o *estado* do código; "dívida técnica" acrescenta a *dimensão temporal e econômica* — o juro que esse estado cobra ao longo do tempo. E é por isso que ela vive **no código**, distinta da cognitiva (nas pessoas) e da de intenção (nos artefatos) — [[09 - As três dívidas do software]].

## Em entrevista

> [!tip] Como falar de dívida técnica sem clichê
> O movimento que sinaliza senioridade é **separar principal de juros e citar o quadrante**. Frase de efeito: *"Technical debt isn't bad code — it's the gap between the code and our current understanding, and the interest is what we pay on every change until we close that gap."* Mostre que você sabe que a metáfora de Cunningham foi **mal-citada**: ela nunca defendeu escrever código ruim — ela *exige* código limpo o bastante pra ser refatorado. Use o quadrante de Fowler pra desarmar o falso dilema "refatorar tudo vs. nunca refatorar": *"Some debt is prudent and deliberate — we take it on purpose with a payback plan. The goal isn't zero debt, it's debt you've chosen and can service."* Se o entrevistador perguntar "como você prioriza dívida técnica?", responda em termos de **juros**: ataque primeiro a dívida nas áreas que mais mudam, porque é onde o juro composto dói mais.

## Referências

- **Ward Cunningham** — *The WyCash Portfolio Management System* (relatório de experiência, OOPSLA 1992). A cunhagem da metáfora: *"Shipping first time code is like going into debt... Every minute spent on not-quite-right code counts as interest on that debt."* [c2.com/doc/oopsla92.html](https://c2.com/doc/oopsla92.html)
- **Ward Cunningham** — *Debt Metaphor* (vídeo, 2009). A correção do mal-entendido: a dívida é *"writing code to reflect your current understanding of a problem even if that understanding is partial"*, e a metáfora *"depends upon you writing code that is clean enough to be able to refactor as you come to understand your problem"*; mais o *"borrowing money thinking that you never had to pay it back"*. Transcrição em [cmdev.com/papers/debt-metaphor](https://cmdev.com/papers/debt-metaphor/).
- **Martin Fowler** — *Technical Debt Quadrant* (bliki, 2009). Os dois eixos (deliberate × inadvertent, prudent × reckless) e os quatro exemplos canônicos (*"We don't have time for design"*, *"We must ship now..."*, *"Now we know how we should have done it"*, *"What's layering?"*). [martinfowler.com/bliki/TechnicalDebtQuadrant.html](https://martinfowler.com/bliki/TechnicalDebtQuadrant.html)

> [!note] Sobre o lastro das afirmações
> As citações de Cunningham (1992 e 2009) e os quatro rótulos do quadrante de Fowler foram **conferidos na pesquisa web** que alimentou esta nota: o trecho de OOPSLA 1992 vem do texto primário em c2.com; as falas de 2009 vêm da transcrição do vídeo em cmdev.com; os quadrantes vêm da divulgação do bliki de Fowler. **Ressalva honesta:** não assisti ao vídeo de 2009 do início ao fim nem li o bliki de Fowler na íntegra — as citações reproduzem com alta fidelidade os trechos verbatim recuperados das fontes acima, mas o fraseado de partes não-citadas (especialmente a ordem exata das falas no vídeo) pode diferir. A atribuição (Cunningham; Fowler), os anos (1992; 2009) e a estrutura do quadrante estão confirmados. Padrão de marcação seguindo [[06 - Abstrações que vazam]].

## Veja também

- [[09 - As três dívidas do software]] — o hub: dívida técnica é uma de três (código × pessoas × artefatos)
- [[11 - Dívida cognitiva]] — a dívida-irmã que vive nas pessoas, não no código
- [[02 - Complexidade essencial vs. acidental]] — dívida técnica ≈ complexidade acidental acumulada
- [[14 - Manutenção e evolução]] — onde a refatoração paga a dívida ao longo da vida do sistema
- [[Dicionário de Fundamentos]] — verbetes do domínio
