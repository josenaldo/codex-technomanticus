---
title: "Complexidade essencial vs. acidental"
created: 2026-06-16
updated: 2026-06-16
type: concept
progress: backlog
status: seedling
publish: false
fase: iniciado
tags:
  - fundamentos
  - complexidade-de-software
  - iniciado
  - complexidade-essencial
  - brooks
---

# Complexidade essencial vs. acidental

A nota anterior ([[01 - A complexidade como problema central]]) terminou com um aviso desconfortável de Brooks: parte da complexidade do software é **essencial** — não some com ferramenta melhor. Esta nota faz o corte que aquela só apontou: separar o que dá pra cortar do que não dá. Porque essa distinção não é filosofia ociosa; ela muda a resposta certa pra cada dificuldade que você encontra.

> [!abstract] TL;DR
> Brooks (*No Silver Bullet*, 1986) divide a complexidade em duas: a **essencial** vem da natureza do problema — das "estruturas conceituais entrelaçadas" que o software precisa representar — e é praticamente irredutível; a **acidental** vem das ferramentas, da linguagem, da representação, do ambiente — e é onde a engenharia tem alavanca. Não há "bala de prata" porque os grandes ganhos históricos (linguagens de alto nível, GC, IDEs) atacaram o acidental, e ele já encolheu; o que sobra é a essência, que nenhuma inovação isolada elimina. *Out of the Tar Pit* (Moseley & Marks, 2006) aperta o argumento: muito do que parece essencial é acidental disfarçado, introduzido pela forma como gerimos **estado**. A utilidade prática: nomear se uma dificuldade é essencial ou acidental decide a resposta — você **refatora pra eliminar** o acidental, mas tem que **modelar e conter** o essencial.

## O que é

Brooks pega emprestada uma distinção de Aristóteles: a **essência** de uma coisa é o que ela tem de necessário, intrínseco; o **acidente** é o que ela tem por circunstância, e que poderia ser de outro jeito sem deixar de ser ela mesma. Aplicado a software:

> [!quote] Os dois tipos de dificuldade
> *"...the difficulties inherent in the nature of the software — and accidents — those difficulties that today attend its production but that are not inherent."*
> — Fred Brooks, *No Silver Bullet* (1986)

E o que é, então, essa "essência" do software? Brooks define com precisão:

> [!quote] A essência do software
> *"The essence of a software entity is a construct of interlocking concepts: data sets, relationships among data items, algorithms, and invocations of functions."*
> — Fred Brooks, *No Silver Bullet* (1986)

Repare: a essência é o **modelo conceitual** que o sistema precisa representar. Se a folha de pagamento da empresa tem trinta regras, essas trinta regras são essenciais — o programa tem que fazer as trinta, independentemente da linguagem. A complexidade **acidental**, por contraste, é tudo o que vem da *representação* dessas ideias: a sintaxe da linguagem, os limites de memória e velocidade, a configuração do ambiente, o boilerplate. Brooks chama o acidental de "the representation of these abstract entities in programming languages and the mapping of these onto machine languages within space and speed constraints".

> [!example] Uma analogia
> Imagine traduzir um romance. A **história** — a trama, os personagens, as reviravoltas — é a essência: ela é a mesma em qualquer idioma, e nenhum dicionário melhor a torna mais simples. A **tradução** — encontrar a palavra certa, lidar com trocadilhos intraduzíveis, caber na métrica — é o acidente: um tradutor melhor, um dicionário melhor, uma língua-alvo mais próxima reduzem esse esforço. Quem confunde os dois acha que um software de tradução automática "resolve" o romance. Ele só ataca o acidente. A história continua exigindo um leitor.

## Por que não há bala de prata

Aqui está o coração do argumento de Brooks, e a razão do título do ensaio. Se quase toda inovação que deu ganho de produtividade — assembler → linguagens de alto nível, gerência manual → garbage collection, editor de texto → IDE — atacou a complexidade **acidental**, então existe um teto pra esse tipo de ganho. Você só pode espremer o acidental até zero, e ele já encolheu muito. Brooks faz a conta explícita:

> [!quote] O teto do ganho acidental
> *"How much of what software engineers now do is still devoted to the accidental, as opposed to the essential? Unless it is more than 9/10 of all effort, shrinking all the accidental activities to zero time will not give an order of magnitude improvement."*
> — Fred Brooks, *No Silver Bullet* (1986)

A lógica é aritmética, não pessimismo. Se o acidental já é menos de 90% do esforço, então *zerar* o acidental — o melhor caso imaginável de qualquer ferramenta nova — não chega a um ganho de 10x. E o que sobra, a essência, é justamente a parte que nenhuma ferramenta toca. Daí a tese:

> [!quote] A tese central
> *"There is no single development, in either technology or management technique, which by itself promises even one order of magnitude improvement in productivity, in reliability, in simplicity."*
> — Fred Brooks, *No Silver Bullet* (1986)

> [!warning] A complexidade essencial é irredutível
> Brooks é categórico: *"The complexity of software is in essential property, not an accidental one. Hence descriptions of a software entity that abstract away its complexity often abstract away its essence."* Traduzindo a consequência: você não pode "abstrair pra longe" a complexidade essencial sem jogar fora o próprio problema. Toda onda de hype que promete eliminar a complexidade — frameworks no-code, geração de código por IA, a próxima linguagem mágica — está, na melhor das hipóteses, atacando o acidental. Manter essa distinção é uma vacina contra acreditar que a essência vai desaparecer.

## Onde o esforço de engenharia compensa

Se o essencial é (em larga medida) irredutível e o acidental é redutível, a conclusão prática é direta: **o acidental é a alavanca que você de fato pode puxar.** É lá que a refatoração paga, que escolher a abstração certa elimina dor de verdade, que melhorar o tooling rende. Tempo gasto reduzindo complexidade acidental é tempo bem gasto — você está removendo dificuldade que *não precisava existir*.

O essencial pede uma postura diferente. Você não o elimina; você o **modela bem e o contém**. Boa modelagem de domínio, fronteiras de módulo bem postas, nomes que refletem os conceitos do problema — nada disso *apaga* a complexidade essencial, mas organiza ela de um jeito que cabe na cabeça. A diferença de atitude é tudo: contra o acidental você simplifica; contra o essencial você estrutura.

> [!tip] Duas perguntas, duas respostas
> Diante de uma dificuldade, pergunte: *"isso é da natureza do problema, ou da forma como eu o representei?"* Se é da representação (acidental) → simplifique, refatore, troque a ferramenta. Se é da natureza do problema (essencial) → não espere que uma ferramenta resolva; modele com cuidado e aceite que a dificuldade é real. O erro caro é tratar essencial como acidental — passar meses procurando a ferramenta que vai "resolver" uma complexidade que é intrínseca ao negócio.

## Out of the Tar Pit: e se quase tudo for acidental?

Vinte anos depois de Brooks, **Ben Moseley e Peter Marks** retomaram o tema em *Out of the Tar Pit* (2006) com uma virada provocadora. Eles aceitam a distinção essencial/acidental de Brooks — inclusive a citam — mas a usam pra um diagnóstico mais cortante: **muito do que parece complexidade essencial é, na verdade, acidental disfarçado**, introduzido pela forma como construímos software.

A definição deles é deliberadamente mais estrita que a de Brooks:

> [!quote] Essencial vs. acidental, versão Tar Pit
> *"Essential Complexity is inherent in, and the essence of, the problem (as seen by the users). Accidental Complexity is all the rest — complexity with which the development team would not have to deal in the ideal world."*
> — Moseley & Marks, *Out of the Tar Pit* (2006)

"As seen by the users" — pelos olhos do usuário — é a chave. Se o usuário não pediria por aquilo num mundo ideal, é acidental. E qual é, segundo eles, a maior fonte de complexidade acidental nos sistemas reais? **Estado** — mais precisamente, estado mutável.

> [!quote] O réu principal: estado
> *"...it is our belief that the single biggest remaining cause of complexity in most contemporary large systems is state, and the more we can do to limit and manage state, the better."*
> — Moseley & Marks, *Out of the Tar Pit* (2006)

O raciocínio: o estado faz o comportamento do sistema depender não só da entrada de agora, mas de toda a história de entradas que levou até aqui. Isso explode o número de situações que você precisa ter na cabeça pra raciocinar com segurança — e raciocinar sobre o sistema é exatamente o que a complexidade destrói. Em segundo lugar vem o **controle** (a ordem em que as coisas acontecem): *"Control is basically about the order in which things happen"* — e os autores chegam a classificar o controle como **inteiramente acidental** no mundo ideal, já que o usuário raramente liga pra ordem interna de execução.

A receita deles segue daí: **minimizar estado**. É uma inclinação funcional/declarativa — a força do paradigma funcional puro, dizem, é que "by avoiding state (and side-effects) the entire system gains the property of referential transparency". O programa proposto, *Functional Relational Programming*, combina programação funcional com o modelo relacional de Codd justamente pra empurrar o estado pra um canto pequeno e controlado.

> [!note] O que muda de Brooks para Tar Pit
> Brooks traça a fronteira e diz "aceite o essencial, é irredutível". Moseley & Marks respondem: "concordamos com a fronteira, mas você está colocando *coisa demais* do lado essencial — boa parte dessa complexidade que você naturalizou como essencial é acidental, e nasceu da sua escolha de gerir estado mutável." É menos uma contradição de Brooks e mais um refinamento: redesenhe o sistema pra empurrar a fronteira essencial/acidental a seu favor.

## Em entrevista

> [!example] Usando a distinção em voz alta
> A moldura essencial-vs-acidental é ouro pra **justificar uma decisão de design** numa entrevista de system design ou num code review. Em vez de "acho que devíamos refatorar isso", você diz: *"Essa dificuldade aqui é acidental — vem da forma como representamos o estado, não do domínio. Dá pra eliminar com [abstração X]. Já aquela regra de negócio é essencial: nenhuma ferramenta vai simplificá-la, então o melhor que podemos fazer é isolá-la num módulo bem nomeado e contê-la."* Isso mostra três coisas de uma vez: que você sabe onde o esforço compensa, que não acredita em bala de prata, e que distingue domar complexidade de fingir que ela não existe. Bônus: citar Brooks (e, se couber, Tar Pit sobre estado) mostra leitura de fundamentos, não só prática.

## Referências

- **Frederick P. Brooks Jr.** — *No Silver Bullet — Essence and Accident in Software Engineering* (1986; reimpresso em *Computer*, vol. 20, n. 4, abril de 1987, p. 10-19; incluído na edição de aniversário de *The Mythical Man-Month*). A distinção essência/acidente (apoiada em Aristóteles), a definição da essência como "construct of interlocking concepts", e a tese de que não há bala de prata. [PDF (worrydream.com)](https://worrydream.com/refs/Brooks_1986_-_No_Silver_Bullet.pdf) · [ACM/IEEE](https://dl.acm.org/doi/10.1109/MC.1987.1663532) · [Wikipedia](https://en.wikipedia.org/wiki/No_Silver_Bullet)
- **Ben Moseley & Peter Marks** — *Out of the Tar Pit* (2006). O estado (mutável) como maior fonte de complexidade, o controle como segunda fonte, a definição estrita de essencial "as seen by the users", e a proposta de minimizar estado via *Functional Relational Programming*. [PDF (curtclifton.net)](https://curtclifton.net/papers/MoseleyMarks06a.pdf) · [Resumo — the morning paper](https://blog.acolyer.org/2015/03/20/out-of-the-tar-pit/)

> [!note] Sobre o lastro das afirmações
> Todas as citações literais desta nota — a distinção inherent/accidental e a definição da essência em Brooks; o "9/10 of all effort", a tese do "no single development... one order of magnitude", e o "essential property, not an accidental one"; em Tar Pit, a definição de Essential/Accidental Complexity, o "single biggest remaining cause of complexity... is state", o "Control is basically about the order in which things happen" e o trecho sobre *referential transparency* — foram extraídas diretamente dos PDFs primários (worrydream.com e curtclifton.net) na pesquisa que alimentou esta nota, não de memória. A autoria (Brooks; Ben Moseley e Peter Marks) e os anos (1986/1987; 2006) foram conferidos contra as fontes primárias. A vinculação a Aristóteles é confirmada pela Wikipedia e pelo próprio subtítulo "Essence and Accident". A paráfrase de *Functional Relational Programming* segue o resumo do paper; não percorri página a página toda a seção de implementação.

## Veja também

- [[01 - A complexidade como problema central]] — a nota que abre a trilha e aponta para esta divisão
- [[03 - Simplicidade não é facilidade]] — a outra face: combater o acidental é buscar simplicidade, e simples não é o mesmo que fácil
- [[06 - Abstrações que vazam]] — quando os mecanismos de gestão de complexidade falham
- [[Dicionário de Fundamentos]] — verbetes do domínio
