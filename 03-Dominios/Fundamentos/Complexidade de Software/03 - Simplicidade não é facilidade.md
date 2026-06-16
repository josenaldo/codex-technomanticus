---
title: "Simplicidade não é facilidade"
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
  - simplicidade
  - hickey
---

# Simplicidade não é facilidade

A nota anterior ([[02 - Complexidade essencial vs. acidental]]) fechou com uma postura de combate: contra o acidental, você **simplifica**. Mas o que é, exatamente, "simplificar"? A palavra é traiçoeira. No dia a dia, a gente usa "simples" e "fácil" como sinônimos — "deixa mais simples", "facilita pra mim". Rich Hickey passou uma palestra inteira mostrando que confundir os dois é a raiz de boa parte da complexidade que a gente mesmo cria. Esta nota faz esse corte.

> [!abstract] TL;DR
> Rich Hickey (*Simple Made Easy*, Strange Loop 2011) separa dois eixos que costumamos colar. **Simple** (simples) é **objetivo** e fala de *estrutura*: vem de *simplex* — "uma dobra/trança", uma coisa sobre uma coisa só, **sem entrelaçamento**. **Easy** (fácil) é **subjetivo e relativo** — vem da raiz de *adjacent*, "estar perto": perto da mão, do familiar, das nossas capacidades atuais. São eixos diferentes: algo pode ser simples e não fácil (desconhecido), ou fácil e não simples (familiar, mas emaranhado). O ato que cria complexidade é **complect** — entrelaçar, trançar coisas juntas. Simplicidade é a recusa deliberada de complect. A armadilha: a gente escolhe pelo *fácil* (o que já está perto) e paga em *complexidade* depois.

## O que é: dois eixos, não um

Hickey insiste que "simples" e "fácil" não são pontos numa mesma régua — são **duas réguas diferentes**. Vale ir à etimologia, porque é dela que ele tira a precisão.

**Simple** vem de *sim* + *plex*: "one fold or one braid or twist" — uma dobra, uma trança. O oposto seria muitas dobras trançadas. Então simples é uma coisa que trata de **um papel, uma tarefa, um conceito, uma dimensão** do problema. E o critério, ele crava, é estrutural:

> [!quote] O que importa pra simplicidade
> *"...what matters for simplicity is that there is no interleaving."*
> — Rich Hickey, *Simple Made Easy* (2011)

Repare na palavra: **interleaving**, entrelaçamento. Simples não é sobre *quantidade* — é sobre *separação*. E, crucial, é uma propriedade **objetiva**: ou as coisas estão trançadas, ou não estão.

> [!quote] Simples é objetivo
> *"...if something is interleaved or not, that's sort of an objective thing... simple is actually an objective notion."*
> — Rich Hickey, *Simple Made Easy* (2011)

**Easy** vem de outro lugar inteiro: da raiz latina de *adjacent*, "estar perto, estar à mão". Hickey decompõe em três sentidos de "perto": perto fisicamente (já instalado, já no classpath), perto do nosso **entendimento** (familiar), e perto das nossas **capacidades** atuais. E daí vem a diferença decisiva: fácil é **relativo**.

> [!quote] Fácil é relativo
> *"...easy is relative. Right?... easy is always going to be, you know, easy for whom, or hard for whom? It's a relative term."*
> — Rich Hickey, *Simple Made Easy* (2011)

> [!example] A analogia das duas réguas
> Pense em duas perguntas diferentes sobre uma ferramenta. *"Ela mistura responsabilidades?"* — pergunta de **estrutura**, e a resposta é a mesma pra qualquer pessoa que olhe: ou mistura, ou não. *"Eu já sei usar?"* — pergunta de **distância**, e a resposta muda conforme quem pergunta: o que é familiar pra mim é estranho pra você. A primeira régua mede *simple*; a segunda mede *easy*. Tocar violino é **simples** (cordas e um arco — sem nada entrelaçado) e ao mesmo tempo nada **fácil** (anos longe das suas capacidades). Já um framework que faz tudo com uma anotação mágica é **fácil** (já está à mão) e nem por isso **simples** (por dentro, mil coisas trançadas).

## Complecting: o verbo que fabrica complexidade

Se "simples" é a ausência de entrelaçamento, precisa existir um verbo pro ato de entrelaçar. Hickey ressuscita uma palavra inglesa antiga: **complect**.

> [!quote] Complect
> *"[to] complect... to interleave or entwine or braid."*
> — Rich Hickey, *Simple Made Easy* (2011)

Esse é o coração da tese. A complexidade não cai do céu — ela é **produzida**, toda vez que a gente trança duas preocupações que poderiam viver separadas. Misturar autenticação com lógica de negócio? Complecting. Amarrar a ordem de execução à correção do resultado? Complecting. Pôr estado e identidade no mesmo objeto mutável? Complecting. Cada trança dessas adiciona um eixo a mais que você precisa segurar na cabeça ao mesmo tempo — e é exatamente esse "ao mesmo tempo" que destrói a capacidade de raciocinar sobre o sistema (o tema que abre toda a trilha em [[01 - A complexidade como problema central]]).

Simplicidade, então, não é um estado mágico — é uma **disciplina negativa**: a recusa de complect. Manter cada coisa sobre uma coisa só, *des*-trançada. Hickey chama isso de a única forma de a gente conseguir "reasonar" sobre software: você consegue pegar uma peça simples e entendê-la *sem* ter que arrastar junto todas as outras peças com que ela estaria entrelaçada.

> [!note] Conexão com a nota anterior
> Lembra do corte de Brooks em [[02 - Complexidade essencial vs. acidental]]? Boa parte da complexidade **acidental** nasce exatamente de complecting — a gente entrelaça preocupações que o domínio nunca pediu que fossem juntas. *Out of the Tar Pit* aponta o estado como o réu principal; Hickey diria que estado é complexo porque *complecta* valor com tempo/identidade. Recusar complect é a tática concreta por trás de "combater o acidental". Esta nota é a **postura de valor** que sustenta o galho inteiro: você gere complexidade *não complectando*.

## A armadilha: a gente decide pelo fácil e paga em complexo

Aqui está a parte incômoda. Se simples e fácil são eixos diferentes, qual deles a gente usa pra decidir? Hickey é direto: a indústria decide pelo **fácil**. Escolhemos a ferramenta familiar, a que já está à mão, a que deixa começar rápido. E faz sentido no curtíssimo prazo — fácil é, por definição, o caminho de menor resistência *agora*.

O problema é a fatura. Fácil otimiza o **começar**; simples otimiza o **continuar**. A ferramenta fácil te deixa produtivo no minuto zero e te entrega um sistema entrelaçado no mês seis — quando o emaranhado que você não viu cobra juros em cada mudança. Simplicidade quase nunca é a escolha fácil de início: exige parar, pensar na estrutura, separar o que o atalho juntaria. É um **investimento deliberado**, pago adiantado, contra um custo que só apareceria depois.

> [!warning] Fácil de começar não é simples de manter
> O viés é traiçoeiro porque os dois sentidos de "near" se reforçam: a ferramenta familiar (perto do entendimento) também costuma ser a já instalada (perto fisicamente). Tudo grita "use isto". Mas familiaridade não é uma propriedade do *design* — é uma propriedade *sua*, e temporária: o que é estranho hoje vira familiar com prática. Já o entrelaçamento é do design, e é permanente até alguém destrançar. Trocar simplicidade por facilidade é hipotecar a estrutura do sistema pra economizar na curva de aprendizado de quem escreve. Hickey: a gente acaba com sistemas que são fáceis de *escrever* e impossíveis de *raciocinar*.

> [!tip] A pergunta que desarma a armadilha
> Antes de adotar algo, separe as duas perguntas que a gente costuma fundir: *"isto é simples?"* (mistura preocupações? quantos eixos eu vou ter que segurar juntos?) e *"isto é fácil?"* (eu já sei usar? já está à mão?). Quando a resposta for "fácil, mas não simples", você ao menos sabe que está contraindo dívida — e pode decidir conscientemente, em vez de tropeçar nela.

## Simples não é "menos coisas"

Um último mal-entendido, e Hickey o ataca de frente: simples **não** quer dizer "poucas coisas". A confusão é natural — "simplificar" soa como "reduzir", "ter menos". Mas o critério nunca foi cardinalidade.

> [!quote] Cardinalidade não é entrelaçamento
> *"...it's important to distinguish cardinality, right, counting things from actual interleaving."*
> — Rich Hickey, *Simple Made Easy* (2011)

Ele dá o exemplo da interface: simples *"doesn't mean an interface that only has one operation"*. Uma interface com vinte operações, cada uma sobre uma coisa bem separada, é **simples**. Uma interface com uma operação só que faz três coisas trançadas é **complexa**. O número de elementos é irrelevante; o que conta é se eles estão *entrelaçados* ou não.

Isso liberta. Você não precisa caber tudo numa caixinha minúscula pra ter simplicidade — uma coisa simples pode ser **bastante coisa**, desde que cada parte trate de uma preocupação só. O alvo não é encolher o sistema; é *des*-trançá-lo. (E é por isso que "simplicidade" e "minimalismo" não são a mesma coisa: dá pra ser minimalista e emaranhado, e dá pra ser grande e impecavelmente separado.)

## Referências

- **Rich Hickey** — *Simple Made Easy* (Strange Loop, setembro de 2011; a palestra foi reprisada em outras conferências depois). A distinção simple/easy, as etimologias (*simplex* = "one fold or braid"; *easy* da raiz de *adjacent* = "lie near"), o verbo *complect* ("to interleave or entwine or braid"), o caráter objetivo de simples vs. relativo de fácil, e a separação entre cardinalidade e entrelaçamento. [Vídeo + transcrição (InfoQ)](https://www.infoq.com/presentations/Simple-Made-Easy/) · [Página da Strange Loop](https://www.thestrangeloop.com/2011/simple-made-easy.html) · [Transcrição (talk-transcripts)](https://github.com/matthiasn/talk-transcripts/blob/master/Hickey_Rich/SimpleMadeEasy.md)

> [!note] Sobre o lastro das afirmações
> As citações literais desta nota — *"what matters for simplicity is that there is no interleaving"*, *"simple is actually an objective notion"*, *"easy is relative... easy for whom"*, a definição de *complect* como *"to interleave or entwine or braid"*, e *"distinguish cardinality... from actual interleaving"* (incluindo o *"doesn't mean an interface that only has one operation"*) — foram extraídas da transcrição da palestra (talk-transcripts no GitHub) na pesquisa que alimentou esta nota, não de memória. As etimologias (*simplex* = "one fold/braid"; *easy* da raiz de *adjacent* = "lie near") e o venue/ano (Strange Loop 2011) foram conferidos contra a mesma transcrição e a página oficial da conferência. A afirmação de que "a indústria decide pelo fácil" é a leitura central de Hickey na palestra, parafraseada e não citada ao pé da letra; o framing de que ela é a "postura de valor por trás do galho" é interpretação minha, não fala dele.

## Veja também

- [[02 - Complexidade essencial vs. acidental]] — o corte de Brooks; complecting é uma das fábricas de complexidade acidental
- [[04 - O programa como teoria]] — por que o entendimento (e a desentranhação) mora nas pessoas, não no código
- [[06 - Abstrações que vazam]] — quando o esconderijo da complexidade falha por baixo
- [[Dicionário de Fundamentos]] — verbetes do domínio
