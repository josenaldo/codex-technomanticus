---
title: "Entropia de software e decaimento"
created: 2026-06-16
updated: 2026-06-16
type: concept
progress: backlog
status: seedling
publish: false
fase: magus
tags:
  - fundamentos
  - complexidade-de-software
  - magus
  - entropia-software
  - big-ball-of-mud
  - lehman
---

# Entropia de software e decaimento

A nota sobre dívida técnica ([[10 - Dívida técnica]]) tratou do que acontece quando você deixa de *pagar de volta* o aprendizado ao código. Mas falta a pergunta de fundo: por que o sistema **piora sozinho** se ninguém faz nada? Hardware enferruja, parafusa solta, metal fadiga — coisas físicas se desgastam pelo uso. Software não tem átomos: o bit que você gravou ontem é idêntico ao de hoje. E mesmo assim todo desenvolvedor sênior sabe que sistemas **apodrecem**. Esta nota é sobre essa física estranha — a tendência do software a ganhar desordem com o tempo — e sobre por que mantê-lo saudável custa energia o tempo todo.

> [!abstract] TL;DR
> Software não se desgasta como hardware — ele **apodrece pela mudança**. Cada alteração tende a aumentar a desordem (a *entropia*) do sistema, a menos que você gaste trabalho ativamente pra combatê-la. Três ideias ancoram isso: a **teoria das janelas quebradas** (Hunt & Thomas, *The Pragmatic Programmer*) — uma bagunça visível não-consertada convida mais bagunça; o **Big Ball of Mud** (Foote & Yoder, 1997) — a arquitetura mais comum do mundo é a *ausência* de arquitetura, e isso tem causas estruturais, não morais; e as **leis de Lehman** — em especial *Continuing Change* (um sistema precisa se adaptar continuamente ou se torna inútil) e *Increasing Complexity* (a complexidade cresce conforme o sistema evolui, a menos que se trabalhe pra reduzi-la). A síntese: **o decaimento é o default** — a segunda lei da termodinâmica do software. Manter um sistema vivo exige injeção *contínua* e *deliberada* de energia.

## O que é

Tome emprestada uma palavra da física. **Entropia** é a medida da desordem de um sistema; a segunda lei da termodinâmica diz que, num sistema fechado, a entropia só tende a aumentar. Um quarto arrumado vira bagunça sozinho; bagunça nunca se arruma sozinha. Pra *baixar* a entropia local — arrumar o quarto — você precisa gastar energia.

Software se comporta assim. Hunt e Thomas chamam isso de **software entropy**: conforme um sistema é mudado ao longo do tempo, sua desordem tende a crescer, e revertê-la exige trabalho. O nome popular do fenômeno é **software rot** (ou *bit rot*, ou *code decay*) — o código "apodrece".

> [!warning] O equívoco do "desgaste"
> Software **não se desgasta como hardware**. Um parafuso fadiga porque sofre estresse físico; o seu `if` não. O código que você não toca por cinco anos roda hoje exatamente como rodava. Então de onde vem o apodrecimento? Da **mudança** — não do uso. Cada alteração feita sob pressa, sem reentender o todo, deposita um pouco de desordem. O sistema não envelhece pelo tempo que passa; envelhece pelas *mãos que passam por ele* sem cuidado. Confundir os dois leva à conclusão errada: "é velho, por isso é ruim". Não. É **mal-mantido**, e isso é uma escolha, não um destino.

A diferença é libertadora e cruel ao mesmo tempo. Libertadora porque decaimento não é inevitável como ferrugem — é reversível com trabalho. Cruel porque, justamente por não ser físico, ninguém *vê* acontecer: não há rachadura na parede, só um diff de cada vez tornando o próximo diff um pouco mais difícil.

## Janelas quebradas

Hunt e Thomas importaram uma metáfora da criminologia urbana. Pesquisadores observaram que um prédio com **uma janela quebrada** não-consertada degrada rápido: a janela sinaliza abandono, o abandono convida pichação, a pichação convida mais quebra, e em pouco tempo o prédio inteiro está arruinado. Não foi o clima — foi o sinal de que *ninguém liga*.

> [!quote] Hunt & Thomas, *The Pragmatic Programmer*
> *"Don't live with broken windows."*

Aplicada ao código, a tese é direta: **uma bagunça visível e tolerada autoriza a próxima**. Um *hack* feio que ninguém limpa, um teste comentado, um `TODO` de dois anos, um nome enganoso deixado de pé — cada um é uma janela quebrada. O dano não é só o defeito em si; é a *mensagem* que ele passa pra quem chega depois: "aqui a régua é essa". E a régua baixa se propaga. O próximo dev, vendo o desleixo, não sente culpa de adicionar o seu. Assim a entropia ganha **realimentação social**: a desordem não só persiste, ela *recruta* mais desordem.

> [!example] Por que o conserto pequeno importa tanto
> Imagine duas bases. Na primeira, todo *hack* temporário vem com um comentário "REMOVER quando X" e é de fato removido; nomes ruins são renomeados na primeira vez que alguém tropeça neles. Na segunda, "depois eu arrumo" virou folclore e ninguém mais arruma nada. A diferença técnica entre as duas, no dia zero, era mínima — um *hack* aqui, um nome ali. A diferença em dois anos é abissal, e ela não veio de uma decisão grande: veio de mil decisões pequenas de **deixar a janela quebrada**. É por isso que a regra é não conviver com ela — não porque um defeito isolado seja caro, mas porque ele *normaliza o próximo*.

## Big Ball of Mud

Se janelas quebradas explicam a *dinâmica* do decaimento, **Brian Foote e Joseph Yoder** nomearam o *destino* dele. No paper *Big Ball of Mud*, apresentado na 4ª conferência **PLoP em 1997** (eles creditam a Brian Marick a cunhagem do termo), descreveram a arquitetura que emerge quando ninguém combate a entropia:

> [!quote] Foote & Yoder, *Big Ball of Mud* (PLoP, 1997)
> *"A Big Ball of Mud is a haphazardly structured, sprawling, sloppy, duct-tape-and-baling-wire, spaghetti-code jungle."*

O *insight* genial do paper não é condenar o lodo — é observar, com honestidade desconfortável, que ele é a **arquitetura mais comum do mundo**. A *de-facto standard*. A maioria dos sistemas em produção, agora, é uma bola de lama. E os autores se recusam a tratar isso como mero fracasso moral de programadores preguiçosos. Eles perguntam *por que* o lodo se forma, e a resposta é estrutural:

- **Pressão de tempo** (*business pressures*) — entregar agora quase sempre vence projetar direito; o mercado paga pela função, não pela arquitetura.
- **Rotatividade** (*developer turnover*) — quem construiu o entendimento foi embora; quem chega remenda o que não compreende (eco direto de [[11 - Dívida cognitiva|dívida cognitiva]]).
- **Crescimento aos pedaços** (*piecemeal growth*) — o sistema cresce uma feature por vez, sem ninguém parando pra rever o todo.
- **Entropia** — o pano de fundo de tudo: na ausência de força contrária, a desordem se acumula.

> [!note] Por que isso não é só xingamento
> É tentador usar "Big Ball of Mud" como insulto — "esse projeto é uma bola de lama". Mas o valor do paper é o oposto: ele *explica* o lodo em vez de só desprezá-lo. As mesmas forças que produzem lodo (entregar rápido, time que muda, crescer por incremento) são forças **legítimas de negócio**. O lodo não é o que acontece quando os programadores são ruins; é o que acontece quando ninguém gasta energia, *de propósito e de forma contínua*, pra impedi-lo. Isto conecta de volta à [[10 - Dívida técnica|dívida técnica]]: a bola de lama é, em larga medida, dívida que ninguém pagou, composta por anos. Reconhecer as causas é o primeiro passo pra não tratar a doença como se fosse caráter.

## As leis de Lehman

Se janelas quebradas são a *psicologia* do decaimento e a bola de lama é o *resultado*, faltava a **física** — a parte que diz "isto vai acontecer, são leis". Quem a forneceu foi **Meir (Manny) Lehman**, com László Belády, a partir de 1974, estudando a evolução do OS/360 da IBM. São **oito leis** no total (formuladas entre 1974 e 1996), mas duas bastam pra ancorar o decaimento.

A primeira é a **Lei da Mudança Contínua** (*Continuing Change*):

> [!quote] Lehman, Lei I — Continuing Change
> *"An E-type system must be continually adapted or it becomes progressively less satisfactory."*

Um sistema **E-type** é aquele escrito pra *mecanizar uma atividade humana ou social* — ele vive imerso no mundo real que modela (um sistema de folha de pagamento, um e-commerce, um prontuário). E o mundo muda: leis, regras de negócio, expectativas. Logo o sistema precisa mudar *junto*, continuamente, ou vai ficando cada vez **menos útil** mesmo sem ninguém mexer nele. Software não tem o luxo de "ficar pronto" — ficar parado já é decair, porque o terreno em volta se move.

A segunda é a que dá nome ao tema desta nota inteira, a **Lei da Complexidade Crescente** (*Increasing Complexity*):

> [!quote] Lehman, Lei II — Increasing Complexity
> *"As an E-type system evolves, its complexity increases unless explicit work is done to maintain or reduce it."*

Repare na cláusula final — ela é o coração da coisa: *"unless explicit work is done"*. A complexidade não cresce porque alguém é desleixado; cresce **por padrão**, como subproduto inevitável da evolução. Cada mudança, mesmo limpa, adiciona um caso, uma interação, uma exceção. Sem trabalho *explícito* em sentido contrário, a curva só sobe. Esta é, literalmente, a [[01 - A complexidade como problema central|complexidade como problema central]] elevada a lei empírica: ela não é um evento, é uma *tendência*.

> [!info] Lastro e escopo
> As oito leis (Continuing Change, Increasing Complexity, Self Regulation, Conservation of Organisational Stability, Conservation of Familiarity, Continuing Growth, Declining Quality, Feedback System), a autoria (Lehman & Belády), as datas (1974–1996) e o enunciado *verbatim* das Leis I e II foram conferidos na pesquisa web que alimentou esta nota (Wikipedia, *Lehman's laws of software evolution*). **Ressalva honesta:** não li os papers originais de Lehman na íntegra — os enunciados reproduzem com alta fidelidade o fraseado recuperado da fonte secundária, e há debate empírico sobre até onde as leis valem para software *open source* (o estudo original era de software monolítico e proprietário). Padrão de marcação seguindo [[06 - Abstrações que vazam]].

## O decaimento é o default

Junte as três peças e aparece um único princípio. Janelas quebradas mostram que a desordem **se realimenta socialmente**. A bola de lama mostra que ela tem **causas estruturais**, não morais. As leis de Lehman mostram que ela é uma **tendência empírica**, não um acidente. A conclusão é dura e clarificadora:

> [!warning] A segunda lei da termodinâmica do software
> **O decaimento é o estado natural.** Deixe um sistema sozinho — sem refatoração, sem reentendimento, sem alguém pagando dívida — e ele *vai* virar bola de lama. Não é risco, é trajetória. A pergunta certa nunca foi "como evitar que o sistema apodreça?" (não dá pra evitar a gravidade), e sim "**quanta energia estamos gastando pra mantê-lo de pé contra o apodrecimento?**". Um sistema saudável não é um sistema que não decai — é um onde *alguém está pagando, continuamente, o custo de combater o decaimento*.

E é por isso que a manutenção não é um luxo nem um sinal de fracasso — é a injeção de energia que mantém a entropia local baixa. Refatorar, pagar dívida técnica, reconstruir o entendimento que a rotatividade dissolveu, consertar as janelas quebradas antes que recrutem mais: tudo isso é o trabalho *explícito* que a Lei II de Lehman exige. Pare de gastar essa energia e a segunda lei cobra a conta — devagar, sem rachadura na parede, um diff de cada vez. É exatamente esse trabalho contínuo de combate à entropia que a próxima nota trata como disciplina: [[14 - Manutenção e evolução]].

## Referências

- **Brian Foote & Joseph Yoder** — [Big Ball of Mud](https://www.laputan.org/mud/) (4ª conferência PLoP, Monticello, Illinois, set/1997; também em *Pattern Languages of Program Design 4*). A arquitetura *de-facto standard*: *"a haphazardly structured, sprawling, sloppy, duct-tape-and-baling-wire, spaghetti-code jungle."* Causas estruturais do lodo: *business pressures*, *developer turnover*, *piecemeal growth*, *software entropy*. Termo creditado a Brian Marick.
- **Meir M. Lehman & László Belády** — *Laws of Software Evolution* (1974–1996). As oito leis; em especial Lei I *Continuing Change* (*"An E-type system must be continually adapted or it becomes progressively less satisfactory"*) e Lei II *Increasing Complexity* (*"its complexity increases unless explicit work is done to maintain or reduce it"*). Sumarizadas em [Lehman's laws of software evolution](https://en.wikipedia.org/wiki/Lehman%27s_laws_of_software_evolution) (Wikipedia).
- **Andrew Hunt & David Thomas** — *The Pragmatic Programmer: From Journeyman to Master* (Addison-Wesley, 1999). *Software entropy* e a *broken windows theory* aplicada a código: *"Don't live with broken windows."* Tópico "Software Entropy" do livro.

> [!note] Sobre o lastro das afirmações
> A autoria, ano e tese do *Big Ball of Mud* (Foote & Yoder, PLoP 1997) e o trecho *verbatim* da definição foram **conferidos na pesquisa web** (laputan.org e Wikipedia). As Leis de Lehman (autoria, datas, oito leis, enunciado das Leis I e II) foram conferidas na Wikipedia. A atribuição de *software entropy* / *broken windows* a Hunt & Thomas (1999) foi conferida. **Ressalva honesta:** não li os textos primários (paper de Foote & Yoder, papers de Lehman, capítulo do *Pragmatic Programmer*) integralmente — as citações reproduzem com alta fidelidade os trechos recuperados, mas o fraseado de partes não-citadas pode diferir, e há debate empírico sobre o alcance das leis de Lehman em software *open source*. Padrão de marcação seguindo [[06 - Abstrações que vazam]].

## Veja também

- [[10 - Dívida técnica]] — decaimento é, em larga medida, dívida deixada sem pagar, composta por anos
- [[14 - Manutenção e evolução]] — a disciplina que injeta energia contra a entropia ao longo da vida do sistema
- [[01 - A complexidade como problema central]] — a Lei II de Lehman é essa tese elevada a lei empírica
- [[Dicionário de Fundamentos]] — verbetes do domínio
