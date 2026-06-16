---
title: "Módulos profundos e rasos"
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
  - modularidade
  - ousterhout
  - encapsulamento
---

# Módulos profundos e rasos

A nota anterior fechou com uma promessa: abstração tem dois lados — uma **interface** (o que você precisa saber pra usá-la) e uma **implementação** (tudo que ela esconde), e a arte está em manter a interface pequena enquanto a implementação faz o trabalho pesado ([[05 - Abstração - a ferramenta central]]). Esta nota transforma essa tensão num critério concreto pra dimensionar um módulo. A pergunta deixa de ser "este módulo é grande ou pequeno?" e vira "quanta complexidade ele esconde por unidade de interface que cobra?".

> [!abstract] TL;DR
> John Ousterhout mede um módulo pela sua **profundidade** (*depth*): a razão entre a funcionalidade que ele entrega e a complexidade da interface que ele expõe. Um **módulo profundo** (*deep module*) tem interface pequena e esconde muita coisa — é o que dá lucro, porque você aprende pouco e ganha muito. Um **módulo raso** (*shallow module*) tem interface quase tão complicada quanto a implementação — paga o custo de mais uma camada sem o benefício de esconder nada. O erro mais comum que produz módulos rasos é a **classitis**: a crença de que mais classes pequenas é sempre melhor. Profundidade importa mais que tamanho.

## O que é

Todo módulo — uma classe, uma função, um pacote, um serviço — tem duas partes. A **interface** é o que um cliente precisa ter na cabeça pra usá-lo: assinaturas, parâmetros, tipos de retorno, efeitos colaterais, modos de falha, ordem de chamadas. A **implementação** é todo o resto: o código que faz o trabalho, e que o cliente legitimamente ignora.

Ousterhout propõe pensar nessa relação como uma **razão**:

> [!quote] Profundidade de módulo
> *"The best modules are deep: they have a lot of functionality hidden behind a simple interface."*
> — John Ousterhout, *A Philosophy of Software Design*

A profundidade é o **benefício líquido** da abstração. A funcionalidade escondida é o que você ganha; a interface é o que você paga (em carga cognitiva — a *cognitive load* da nota 01). Um bom módulo entrega muito e cobra pouco. Um módulo ruim cobra quase tanto quanto entrega — e às vezes cobra mais, virando saldo negativo.

> [!note] Profundidade ≠ tamanho
> Profundidade não é sobre o módulo ter muitas linhas. Um módulo profundo pode ser enorme por dentro — o que importa é que a **interface** seja pequena em relação a isso. E um módulo minúsculo pode ser raso: se a interface dele é quase do tamanho do que ele faz, ele não abstrai nada. O eixo certo de avaliação é a razão, não a contagem de linhas nem de classes.

Visualmente, Ousterhout desenha cada módulo como um retângulo: a **largura do topo** é o tamanho da interface; a **área** é a funcionalidade total. O módulo profundo é alto e estreito (pouca interface, muita área); o raso é largo e baixo (muita interface, pouca área).

## Módulos profundos: pouca interface, muita máquina

O exemplo canônico de Ousterhout é a **API de I/O de arquivos do Unix**. Você usa basicamente quatro chamadas — `open`, `read`, `write`, `close` — e atrás delas mora uma quantidade colossal de máquina: gerenciamento de blocos em disco, cache de páginas, agendamento de I/O, permissões, journaling, representação de diretórios. A interface tem um punhado de funções; a implementação tem dezenas de milhares de linhas. Razão altíssima. É por isso que quase ninguém precisa entender um sistema de arquivos pra ler um arquivo.

O caso extremo é o **garbage collector** ([[03 - Garbage Collection — o conceito]]): ele esconde uma quantidade enorme de funcionalidade atrás de **nenhuma interface**. Você não chama o GC — ele simplesmente acontece. Interface zero, funcionalidade gigante: profundidade no limite teórico. Por isso o GC é uma das abstrações mais valiosas que existem, *quando não vaza* (e a nota 06 mostrou onde ela vaza).

> [!example] O que torna um módulo profundo
> Uma `Map` (dicionário) é profunda: a interface é "guarde por chave, recupere por chave", e por baixo há hashing, tratamento de colisão, redimensionamento, talvez balanceamento de árvore. Você usa duas operações e esquece tudo isso. Compare com a sensação de usar uma classe que te obriga a configurar dez parâmetros antes de fazer qualquer coisa útil — essa cobra muito pra entregar pouco.

O ganho de um módulo profundo conecta direto com a nota de abertura: ele combate a **carga cognitiva** (você segura menos coisas na cabeça) e a **change amplification** (a complexidade escondida pode mudar sem respingar nos clientes, porque eles nunca dependeram dela). Profundidade é information hiding ([[05 - Abstração - a ferramenta central]]) medido pelo seu resultado.

## Módulos rasos e a classitis

Um **módulo raso** é o oposto: a interface é quase tão complexa quanto a implementação. Ele não esconde quase nada, então o custo de aprender a interface quase anula o benefício de não ler o código. Ousterhout é direto sobre o saldo:

> [!quote] O custo de um módulo raso
> *"A shallow module is one whose interface is complicated relative to the functionality it provides. Shallow modules don't help much in the battle against complexity, because the benefit they provide (not having to learn about how they work internally) is negated by the cost of learning and using their interfaces."*
> — John Ousterhout (paráfrase fiel; ver Referências)

O sintoma mais óbvio é o **método *pass-through*** (de repasse): um método cuja única função é chamar outro método com a mesma assinatura, sem agregar nada. Já vimos esse caso na nota anterior — o `UserService.getUser(id)` que só faz `return repository.findById(id)`. A camada existe, mas o cliente precisa saber exatamente o mesmo que precisaria sem ela. É indireção pura: custo de salto, benefício zero ([[05 - Abstração - a ferramenta central]]).

E aqui entra o diagnóstico mais provocador do livro — a **classitis**:

> [!quote] Classitis
> *"This belief that classes should be small, not deep, leads to a syndrome I call 'classitis'... Classitis may result in classes that are individually simple, but it increases the complexity of the overall system."*
> — John Ousterhout (paráfrase fiel; ver Referências)

**Classitis** é a crença equivocada de que mais classes, e menores, é *sempre* melhor — que fragmentar é sempre limpar. A intuição parece boa: classes pequenas são fáceis de entender uma por uma. Mas o argumento de Ousterhout vira a mesa: classes pequenas entregam pouca funcionalidade cada, então **você precisa de muitas** — e cada uma traz a própria interface pra aprender, e as **interfaces entre os fragmentos acumulam complexidade**. A conta total cresce mesmo que cada peça pareça simples. Você trocou poucos módulos profundos por muitos módulos rasos, e o sistema inteiro ficou mais difícil.

> [!warning] Cuidado com a métrica "classe pequena = código limpo"
> "Quebre essa classe grande em cinco menores" parece sempre uma boa refatoração, mas nem sempre é. Se as cinco menores só fazem sentido juntas e expõem cinco interfaces onde antes havia uma, você produziu classitis: mais nomes pra aprender, mais saltos no debug, mais acoplamento nas costuras. Antes de fragmentar, pergunte: cada fragmento esconde uma decisão própria e tem uma interface que se sustenta sozinha? Se não, o módulo grande e profundo pode ser o design correto. Tamanho de classe é um péssimo proxy pra qualidade de design.

Isso não é licença pra escrever classes-monstro que misturam tudo. É um aviso contra o exagero oposto, que a cultura atual raramente questiona. O critério não é "pequeno" nem "grande" — é **profundo**.

## A complexidade é incremental: empurre-a pra baixo

Por que módulos rasos proliferam? Porque cada um, isolado, parece inofensivo. Aqui Ousterhout reencontra uma tese que já apareceu na nota de abertura ([[01 - A complexidade como problema central]]):

> [!quote] Complexity is incremental
> *"Complexity isn't caused by a single catastrophic error; it accumulates in lots of small chunks... you have to sweat the small stuff."*
> — John Ousterhout (paráfrase fiel; ver Referências)

Nenhuma decisão sozinha torna um sistema complexo. A complexidade se acumula em centenas de pequenas escolhas — um método pass-through aqui, uma interface inflada ali, uma classe rasa acolá. Cada uma é defensável; a soma é uma bola de lama. A consequência prática é dura: **não dá pra esperar um momento de grande refatoração pra consertar**. Você resiste à complexidade continuamente, decisão a decisão, ou ela vence pelo acúmulo. É o "death by a thousand cuts" — morte por mil cortes.

A heurística construtiva que Ousterhout dá pra produzir profundidade é **empurrar a complexidade pra baixo** (*pull complexity downward*):

> [!quote] Pull complexity downward
> *"It is more important for a module to have a simple interface than a simple implementation."*
> — John Ousterhout (paráfrase fiel; ver Referências)

Quando você tem uma escolha entre simplificar a interface (à custa de uma implementação mais complicada) ou simplificar a implementação (à custa de uma interface mais complicada), prefira quase sempre a **interface simples**. A razão é de **assimetria de público**: o implementador é *um*; os chamadores são *muitos*. Faz sentido que a pessoa que escreve o módulo absorva a complexidade uma vez, pra que dezenas de chamadores não precisem absorvê-la cada um. Ousterhout descreve isso quase como um sacrifício — o autor do módulo carrega a dor pra que os usuários vivam melhor. Projete a interface pra tornar o **caso comum simples**, mesmo que isso te custe trabalho por dentro.

> [!tip] O teste de profundidade
> Diante de um módulo, pergunte: *"quanto um chamador precisa saber pra usá-lo, comparado a quanto ele faz?"* Se a interface é pequena e a funcionalidade é grande, você tem um módulo profundo — guarde-o. Se a interface é quase do tamanho do que ele entrega, ou se ele só repassa chamadas, você tem um módulo raso — considere fundi-lo a um vizinho, ou empurrar mais complexidade pra dentro dele até a interface valer o salto.

Profundidade é o critério; classitis é a tentação contrária; "empurre pra baixo" é o como. Esse trio é o que separa a abstração que envelhece bem do amontoado de camadas que vira pedágio — e leva direto ao próximo tema, a **carga cognitiva e a legibilidade** que essas escolhas produzem no leitor ([[08 - Carga cognitiva e legibilidade]]).

## Referências

- **John Ousterhout** — *A Philosophy of Software Design* (1ª ed. 2018; 2ª ed. 2021, Yaknyam Press). Origem dos termos **deep module / shallow module**, da definição de profundidade como razão entre funcionalidade e complexidade da interface, do método *pass-through*, do diagnóstico **classitis**, da tese *"complexity is incremental"* ("sweat the small stuff") e da heurística *"pull complexity downward"* / *"it is more important for a module to have a simple interface than a simple implementation"*. Exemplos do Unix file I/O e do garbage collector como módulos profundos são do livro.

> [!note] Sobre o lastro
> Os termos de Ousterhout (*deep/shallow module*, *classitis*, *complexity is incremental*, *pull complexity downward*) e os exemplos canônicos (Unix file I/O, garbage collector) foram conferidos contra resumos, capítulos publicados (softengbook.org) e fontes secundárias confiáveis na pesquisa que alimentou esta nota, além de coletâneas de citações do livro. **Ressalva honesta:** não consultei o texto integral página a página. As citações marcadas *"(paráfrase fiel; ver Referências)"* reproduzem o argumento e o vocabulário do autor com alta fidelidade, mas podem diferir da redação literal em pontuação ou palavras exatas; a única citação verbatim conferida diretamente é a primeira (*"The best modules are deep..."*). O padrão de marcação de incerteza segue o da nota vizinha [[06 - Abstrações que vazam]].

## Veja também

- [[05 - Abstração - a ferramenta central]] — interface vs. implementação, a tensão que a profundidade mede
- [[08 - Carga cognitiva e legibilidade]] — o custo cognitivo que interfaces rasas impõem ao leitor
- [[01 - A complexidade como problema central]] — a complexidade incremental e a change amplification que a profundidade combate
- [[06 - Abstrações que vazam]] — o outro limite: mesmo módulos profundos vazam um pouco
- [[Orientação a Objetos]] — encapsulamento, o mecanismo de linguagem por trás de módulos profundos
- [[Dicionário de Fundamentos]] — verbetes do domínio
