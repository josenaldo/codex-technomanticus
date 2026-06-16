---
title: "Lei de Conway"
created: 2026-06-16
updated: 2026-06-16
type: concept
progress: backlog
status: growing
publish: false
fase: magus
tags:
  - fundamentos
  - complexidade-de-software
  - magus
  - lei-de-conway
  - organizacao
---

# Lei de Conway

A nota anterior ([[15 - Pensamento sistêmico]]) terminou com um gancho: a forma como um time se comunica acaba **estampada** na forma do software. Isso é um efeito sistêmico — uma propriedade que emerge do acoplamento entre a estrutura humana e a estrutura técnica.

Esta nota desenvolve esse resultado por inteiro. Ele tem nome próprio, autor e ano, e é uma das observações mais antigas e mais subestimadas da engenharia de software.

Também é o ponto onde o galho fecha, porque ele prova a tese mais incômoda de toda a trilha: **a complexidade não é só técnica — ela mora no sistema humano também.**

> [!abstract] TL;DR
> A **Lei de Conway** (Melvin Conway, 1968) diz que qualquer organização que projeta um sistema produz um design cuja **estrutura é uma cópia da estrutura de comunicação dessa organização**. O mecanismo é simples: módulos são construídos por times, e a interface entre dois módulos espelha a comunicação (ou a falta dela) entre os dois times. Consequência: a **complexidade organizacional vaza para a arquitetura** — quatro times montando um compilador tendem a produzir um compilador de quatro passes. Como o espelhamento acontece de qualquer jeito, dá pra usá-lo a favor: a **manobra inversa de Conway** molda a organização *de propósito* para **provocar** a arquitetura desejada (popularizada por *Team Topologies*, de Skelton & Pais). A evidência empírica é robusta: o custo de propagação do código espelha o acoplamento da organização (MacCormack/Baldwin), e no estudo do **Windows Vista** (Nagappan/Murphy/Basili) métricas *organizacionais* previram defeitos **melhor que as métricas de código**. Mas a lei **não é destino**: a revisão de 102 estudos de Colfer & Baldwin achou o espelhamento em ~69% dos casos, e há duas formas conhecidas de **"quebrar o espelho"**. Moral prática: **você não conserta um problema de arquitetura que na verdade é um problema de organização mexendo só no código.**

## O que é

Pergunta de abertura: por que dois times igualmente competentes, com o mesmo problema e as mesmas ferramentas, produzem arquiteturas tão diferentes?

Em 1968, **Melvin Conway** deu uma resposta que ninguém esperava — a diferença está menos na engenharia e mais em **quem fala com quem**.

A formulação literal, do artigo *How Do Committees Invent?* (Datamation, abril de 1968):

> [!quote] Lei de Conway
> *"Any organization that designs a system (defined more broadly here than just information systems) will inevitably produce a design whose structure is a copy of the organization's communication structure."*
> — Melvin E. Conway, *How Do Committees Invent?* (1968)

No corpo do artigo, Conway usa um verbo ainda mais forte do que "inevitavelmente produzirá": as organizações são **"constrangidas"** (*constrained*) a copiar sua estrutura de comunicação. A frase exata é *"organizations which design systems […] are constrained to produce designs which are copies of the communication structures of these organizations"*.

A palavra importa. Não é uma tendência que dá pra contornar com disciplina ou boa vontade — é uma **restrição estrutural**, como a gravidade. Você pode lutar contra, mas paga um preço por cada metro que sobe.

O **mecanismo** é quase tautológico depois que você o vê. Para que dois módulos de software se encaixem corretamente, **as pessoas** que projetam e implementam cada um precisam se comunicar — alinhar a interface, combinar o contrato, negociar quem faz o quê.

Logo, a interface entre dois módulos só pode ser tão boa, tão rica e tão bem-acabada quanto a comunicação entre os dois grupos que os constroem. A estrutura de **interfaces** do sistema acaba sendo uma imagem da estrutura de **comunicação** da organização.

> [!note] A homomorfia, no sentido literal de Conway
> Conway não usa "homomorfia" como metáfora frouxa. Ele pergunta no artigo se a correspondência entre organização e sistema é mesmo estrutural e responde: *"Yes, the relationship is so simple that in some cases it is an identity. […] This kind of structure-preserving relationship between two sets of things is called a homomorphism."* Uma **homomorfia** é um mapeamento que **preserva estrutura**: cada grupo da organização vira um subsistema; cada canal de comunicação entre grupos vira uma interface entre subsistemas; a topologia de um lado reaparece do outro. É por isso que a lei tem força de teorema e não de provérbio — Conway está afirmando uma correspondência ponto-a-ponto, não uma analogia poética.

Há um corolário que costuma passar despercebido e que Conway enuncia com todas as letras: *"the very act of organizing a design team means that certain design decisions have already been made, explicitly or otherwise."*

Ou seja — **no instante em que você desenha o organograma do projeto, você já desenhou parte da arquitetura**, mesmo sem saber. Decidir que haverá um time de "pagamentos", um de "catálogo" e um de "identidade" é decidir, antecipadamente, que existirão três subsistemas com essas fronteiras.

O org chart é o primeiro diagrama de arquitetura, e quase ninguém o lê assim.

> [!example] O exemplo da pesquisa contratada (Conway, 1968)
> Conway ilustra o ponto com um caso de pesquisa por contrato. Uma agência de pesquisa por contrato tinha **oito pessoas** designadas para escrever um compilador COBOL e um compilador ALGOL. Resultado? **Um compilador COBOL de cinco passes e um compilador ALGOL de três passes** — porque a agência alocou cinco pessoas no COBOL e três no ALGOL. A decomposição técnica de cada compilador *seguiu a contagem de cabeças*, não a estrutura ideal do problema de compilação. É o caso real por trás da paráfrase "quatro grupos → quatro passes".

Por que essa restrição existe? Conway dá a razão econômica. Times pequenos e bem coordenados são caros e raros; o instinto da gestão é o oposto.

> [!quote] A flexibilidade da organização (Conway, 1968)
> *"Because the design that occurs first is almost never the best possible, the prevailing system concept may need to change. Therefore, flexibility of organization is important to effective design."*
>
> Tradução: como o primeiro design quase nunca é o melhor, o conceito do sistema vai precisar mudar — e, se a organização for rígida, ela **trava** a arquitetura no formato errado. A flexibilidade do org chart é pré-requisito para a flexibilidade da arquitetura. (É exatamente este parágrafo que a [[#A manobra inversa de Conway|manobra inversa]] vai levar ao extremo, mais adiante.)

> [!note] O nome "Lei de Conway" não é de Conway
> Conway escreveu o artigo; o **apelido "Lei de Conway" foi cunhado por Fred Brooks**, que citou e batizou a ideia em *The Mythical Man-Month* (1975). (É o mesmo Brooks da [[01 - A complexidade como problema central|complexidade essencial e do "No Silver Bullet"]] — o galho gira em torno de um punhado de gigantes que se citam.) Detalhe de origem: Conway submeteu o texto à *Harvard Business Review* em 1967, foi rejeitado, e só então a *Datamation* o publicou em 1968. O próprio site de Conway credita o batismo a Brooks e diz secamente: *"The name stuck."*

## A complexidade organizacional vaza para a arquitetura

Aqui está o elo direto com o galho. Se a arquitetura espelha a comunicação do time, então **a complexidade da organização vaza para a complexidade do sistema** — ela atravessa a fronteira entre o humano e o técnico e se materializa em código. Um org chart confuso, com responsabilidades sobrepostas e comunicação ruidosa, tende a parir uma arquitetura confusa, com responsabilidades sobrepostas e acoplamento ruidoso. Não porque os engenheiros sejam ruins; porque eles estão, sem querer, **codificando o formato da organização**.

> [!example] O compilador de quatro passes
> A ilustração canônica: *"se você tem quatro grupos trabalhando num compilador, vai obter um compilador de quatro passes."* Cada grupo controla um pedaço; as fronteiras entre os pedaços viram as fronteiras entre os passes; o número de fases do compilador acaba refletindo o número de equipes, não a melhor decomposição técnica do problema. A decisão de **arquitetura** (quantos passes?) foi tomada, sem ninguém perceber, pela decisão de **organização** (quantos grupos?).
>
> Ressalva de honestidade: essa frase específica não é citação literal de Conway — é a paráfrase popularizada por Eric S. Raymond no *Jargon File* / *The New Hacker's Dictionary*. O *exemplo* do compilador, porém, está em espírito no artigo original; o fraseado é que é de Raymond.

Conway vai além do exemplo bonitinho e descreve um **mecanismo de degeneração** que é assustadoramente atual. Ele explica, em três passos, por que sistemas grandes "se desintegram":

> [!quote] Por que sistemas grandes se desintegram (Conway, 1968)
> Primeiro, a percepção de que o sistema será grande — somada a certas pressões na organização — torna **irresistível a tentação de alocar gente demais** num esforço de design. Segundo, aplicar a sabedoria convencional de gestão a uma organização de design grande faz sua **estrutura de comunicação se desintegrar**. Terceiro, a **homomorfia garante que a estrutura do sistema vai refletir essa desintegração** ocorrida na organização.

Leia de novo o passo um. Conway está dizendo que a causa-raiz de muito software ruim é **organizacional, não técnica**: a empresa tinha gente disponível, então jogou gente no problema, e a homomorfia fez o resto.

Ele crava isso numa frase que merece estar pregada na parede de todo gerente de engenharia: *"Probably the greatest single common factor behind many poorly designed systems now in existence has been the availability of a design organization in need of work."* — o maior fator isolado por trás de sistemas mal projetados é, simplesmente, **ter uma organização de design ociosa precisando de trabalho**.

Note o eco com a [[01 - A complexidade como problema central|Lei de Brooks]]: adicionar gente a um projeto atrasado o atrasa mais — e Conway dá a *razão estrutural* por trás disso. (Aliás, foi George Mealy, colega de Brooks no OS/360, quem primeiro propôs chamar a observação de "Lei de Conway", num simpósio de 1968 — ver lastro.)

### O monólito distribuído: a homomorfia se vingando

A versão moderna mais cara da desintegração tem nome: **monólito distribuído** (*distributed monolith*). É o sistema que tem todos os custos de microserviços (rede, latência, *eventual consistency*, complexidade operacional) e nenhum dos benefícios (autonomia, deploy independente, isolamento de falhas).

Os serviços foram fisicamente separados, mas continuam **acoplados**. Os sintomas são reconhecíveis:

- uma mudança num serviço exige deploy coordenado de vários;
- serviços compartilham o mesmo banco de dados;
- cadeias de chamadas síncronas com mais de dois saltos de profundidade;
- uma falha num serviço cascateia para os outros;
- ninguém consegue subir um serviço sozinho sem subir meia constelação junto.

A pergunta certa diante disso não é "como conserto isso?" e sim *"por que isso aconteceu?"*.

Pela Lei de Conway, a resposta costuma ser organizacional. Os serviços foram fatiados pelas **fronteiras do código antigo** (um "lift and shift" do monólito) ou pelas **camadas técnicas** (time de frontend, time de backend, time de banco) em vez de por **capacidade de negócio**.

Você pode decompor o código, mas se o mesmo grupo de pessoas continua coordenando cada release, o acoplamento não mudou — só trocou de camada. Quando os times precisam conversar o tempo todo para fazer qualquer coisa, a homomorfia transforma essa conversa permanente em **acoplamento permanente** entre os serviços.

O monólito distribuído é a Lei de Conway aplicada a uma organização cuja comunicação real é um emaranhado — só que agora o emaranhado tem latência de rede no meio.

> [!warning] A armadilha do "vamos só refatorar"
> Daí o erro mais comum e mais caro: tratar como **bug de código** o que é **homomorfia de org chart**. Dois times que mal conversam vão produzir uma interface pobre entre seus módulos por mais que você refatore — porque a interface ruim *é o reflexo fiel* da comunicação ruim. Mude o código sem mudar a comunicação e a entropia ([[13 - Entropia de software e decaimento]]) o puxa de volta ao formato da organização. Fronteiras de time, carga cognitiva por time e caminhos de comunicação **são forças arquiteturais**, tão reais quanto acoplamento e coesão.

Repare como isso reabre temas que o galho já visitou. É um efeito de **segunda ordem** ([[15 - Pensamento sistêmico]]): você organiza os times pensando só em RH e planejamento, e a consequência aparece longe dali, na forma do software. É também uma forma de **complexidade emergente** — ela não está em nenhum engenheiro nem em nenhum org chart isolado; emerge do **acoplamento** entre as duas estruturas. E é por isso que a complexidade arquitetural às vezes resiste a toda refatoração: você está combatendo no código um problema cuja raiz está no **formato da organização**.

## A evidência: a hipótese do espelhamento

A Lei de Conway poderia ter ficado para sempre como uma anedota elegante. O que a tirou do reino do folclore foi um programa de pesquisa empírica que a reformulou como **hipótese do espelhamento** (*mirroring hypothesis*).

A hipótese é a previsão testável de que a arquitetura técnica de um produto e a arquitetura social da organização que o produz são **homólogas** — fronteiras de módulo alinhadas com fronteiras de equipe, dependências técnicas alinhadas com canais de comunicação.

O estudo seminal é de **Alan MacCormack, Carliss Baldwin e John Rusnak (2012)**, *Exploring the duality between product and organizational architectures*. A sacada metodológica foi medir a modularidade de software com uma métrica objetiva: o **custo de propagação** (*propagation cost*) — a proporção média de elementos de design afetados quando você muda um elemento qualquer, escolhido ao acaso.

- **Custo de propagação alto** = mexer numa peça mexe em quase tudo (arquitetura emaranhada).
- **Custo de propagação baixo** = mudanças ficam contidas (arquitetura modular).

> [!example] Mozilla: o número que prova a tese
> Os autores compararam produtos construídos por organizações de tipos opostos — software proprietário (organizações concentradas, co-localizadas) versus open source (organizações distribuídas, fracamente acopladas). O caso mais citado é o do navegador **Mozilla**. Quando a Netscape/Mozilla **redesenhou deliberadamente** o produto para abrir o código e permitir contribuição distribuída, o custo de propagação **despencou de 17,35% para 2,78%** — a arquitetura ficou dramaticamente mais modular. A organização ficou mais frouxamente acoplada *de propósito*, e o produto acompanhou. A comparação com o **Linux** (open source desde a origem) reforça o padrão: organizações distribuídas tendem a produtos mais modulares; organizações concentradas, a produtos mais integrados.

A conclusão central do estudo é a forma "forte" da lei, agora com dado: **organizações fracamente acopladas desenvolvem produtos mais modulares do que organizações fortemente acopladas**. A Lei de Conway deixou de ser uma frase de efeito e virou uma previsão que sobrevive a um teste estatístico com métricas reproduzíveis.

### O estudo do Windows Vista: a organização prevê o defeito

Se o estudo da Mozilla mostra que a *estrutura* do produto espelha a *estrutura* da organização, há um achado ainda mais forte — e desconfortável: a estrutura da organização prevê **onde os bugs vão aparecer**, e prevê *melhor que as próprias métricas de código*.

Em 2008, **Nachiappan Nagappan, Brendan Murphy e Victor Basili** publicaram *The Influence of Organizational Structure on Software Quality: An Empirical Case Study* (ICSE 2008 / Microsoft Research TR-2008-11). Eles estudaram o desenvolvimento do **Windows Vista** — um dos maiores artefatos de software já construídos — e fizeram uma pergunta provocadora: e se a "qualidade" de um binário pudesse ser prevista *sem olhar uma linha do seu código*, só pela forma como a organização que o produziu estava estruturada?

Para isso, definiram um conjunto de **métricas organizacionais** — métricas que descrevem *quem* escreveu o código e *como* esses contribuidores se distribuíam pela organização, não o código em si. Entre elas:

- **Profundidade de propriedade (*depth of master ownership*)** — quão fundo na hierarquia está o "dono" do binário; ownership concentrado no topo vs. pulverizado.
- **Número de organizações contribuindo (*organization intersection factor*)** — quantas unidades organizacionais internas diferentes mexeram naquele binário.
- **Número de engenheiros** e **ex-engenheiros** (gente que tocou o código e já saiu), **frequência de edição**, e o **grau de propriedade organizacional** do código.

> [!example] O número do Vista: organização supera código
> O modelo construído **só com métricas organizacionais** identificou binários propensos a falha com **precisão e recall de cerca de 85%** — e foi **estatisticamente superior** aos modelos baseados nas métricas tradicionais de código: *churn* (volume de mudança), complexidade, cobertura de testes, dependências e contagem de bugs pré-release. Ou seja: *quão fragmentada e dispersa era a organização que tocou um pedaço de código previu melhor a presença de defeitos do que o quão complexo era esse código.* É a Lei de Conway transformada em métrica de risco — a homomorfia não só molda a forma do produto, ela molda a distribuição dos seus *defeitos*.

A lição prática é dura. Se um binário foi tocado por sete unidades organizacionais diferentes, com ownership disperso e muita rotatividade, ele vai ser frágil **independentemente** de quão limpo o código pareça numa review. O defeito não nasce da complexidade do código; nasce do **gap de coordenação** entre todas as mãos que passaram por ali — exatamente o que a [[#Congruência sócio-técnica: o refinamento|congruência sócio-técnica]] (logo abaixo) vai formalizar.

## Congruência sócio-técnica: o refinamento

Há um problema na formulação ingênua da lei: ela fala de "estrutura de comunicação" como se fosse uma coisa só, fixa e óbvia.

Mas *qual* estrutura de comunicação importa? A do org chart? A das dependências reais entre as tarefas?

**Cataldo, Herbsleb e Carley (2008)** afiaram a ideia com o conceito de **congruência sócio-técnica** (*socio-technical congruence*): o que prediz produtividade não é a comunicação em abstrato, e sim o **alinhamento entre as necessidades de coordenação que o trabalho exige e os canais de coordenação que de fato existem**.

A diferença é sutil e importante. O trabalho tem **dependências técnicas**: o módulo A chama o módulo B, então quem mexe em A precisa coordenar com quem mexe em B. Isso gera uma **necessidade de coordenação**.

Daí o teste:

- Se a estrutura social de coordenação real (quem fala com quem, quem revisa o quê) **bate** com essas necessidades, há congruência — e o trabalho flui.
- Se não bate — duas pessoas cujos módulos se acoplam, mas que nunca conversam —, há **gap de coordenação**, e o defeito nasce ali. (É a mesma fenda que o estudo do Vista mediu como "número de organizações tocando um binário".)

> [!example] O número da congruência
> No estudo empírico de Cataldo et al., quando os padrões de coordenação dos desenvolvedores eram **congruentes** com suas necessidades reais de coordenação, o tempo para resolver uma *modification request* caiu, em média, **~32%**. A mensagem prática: modularidade pura não basta para representar as dependências reais do trabalho; é preciso casar a *rede social* da equipe com a *rede técnica* do código.

Por que isso é um refinamento e não só uma nota de rodapé? Porque ele desloca o alvo. A Lei de Conway ingênua diz "mude o org chart". A congruência sócio-técnica diz: o que você quer mudar é a **rede de coordenação efetiva** — e ela nem sempre segue o org chart. Dois desenvolvedores em times diferentes que revisam o PR um do outro toda semana têm um canal de comunicação real que **não aparece em organograma nenhum**. É essa rede invisível, e não a caixinha hierárquica, que a homomorfia copia para a arquitetura.

## A manobra inversa de Conway

Se a arquitetura vai espelhar a comunicação **de qualquer jeito**, há uma jogada óbvia escondida na lei: em vez de sofrer o espelhamento, **use-o**.

Essa é a **manobra inversa de Conway** (*inverse Conway maneuver*, também *reverse Conway*, termo popularizado pela ThoughtWorks): em vez de impor uma arquitetura e torcer pra organização segui-la, você **desenha a organização de propósito** para **provocar** a arquitetura que quer.

Conway, de novo, já tinha a intuição. Como vimos lá em cima, ele afirmou que *"flexibility of organization is important to effective design"* — a flexibilidade do org chart é o que permite a arquitetura evoluir.

A manobra inversa é levar isso ao extremo: tratar o org chart como uma **alavanca de design** que você ajusta de propósito, e não como um dado de RH imutável. Se a organização vai virar arquitetura, então projete a organização *para obter a arquitetura que você quer*.

Quer microserviços com fronteiras limpas e autônomas? Monte times pequenos, autônomos, donos de uma fatia de negócio ponta a ponta. A estrutura humana vai puxar a estrutura técnica na direção desejada.

A formulação moderna mais influente disso é **Team Topologies**, de **Matthew Skelton e Manuel Pais** (2019), que pega Conway e o transforma numa ferramenta de design organizacional. A obra propõe uma "linguagem de padrões" para times com **quatro tipos** e **três modos de interação**:

> [!abstract] Os quatro tipos de time (Team Topologies)
> - **Stream-aligned (alinhado ao fluxo)** — o tipo padrão e majoritário: dono de um único fluxo de valor ponta a ponta (uma jornada, uma capacidade de negócio), cross-funcional, autônomo, com o mínimo de handoffs. Por Conway, produz um *serviço* coeso, de fronteira clara.
> - **Platform (plataforma)** — provê serviços internos (CI/CD, observabilidade, infra) que **reduzem a carga cognitiva** dos times de fluxo, oferecidos como produto self-service.
> - **Enabling (capacitador)** — ajuda outros times a adquirirem capacidades que lhes faltam (uma nova prática, uma nova tecnologia); atua e sai de cena.
> - **Complicated-subsystem (subsistema complicado)** — cuida de uma parte que exige conhecimento especialista profundo (um motor de cálculo, um codec, um modelo matemático), isolando essa complexidade dos demais.

> [!abstract] Os três modos de interação
> - **Collaboration (colaboração)** — dois times trabalham junto, intensamente, por um período, para descobrir algo novo. Alto fluxo de comunicação, alto custo: deliberado e temporário.
> - **X-as-a-Service (X-como-serviço)** — um time consome o que o outro provê com **mínima comunicação**, através de uma interface bem definida. É o modo que produz fronteiras limpas e desacopladas.
> - **Facilitating (facilitação)** — um time (tipicamente o *enabling*) ajuda outro a remover impedimentos e a aprender.

A genialidade do esquema é que **cada modo de interação é, ele próprio, uma alavanca de Conway** — projetado para produzir o espelhamento certo.

- Quer uma fronteira de serviço limpa e estável entre dois domínios? Coloque os times em modo *X-as-a-Service*: a comunicação mínima e contratual vira, por Conway, uma interface mínima e estável.
- Quer descobrir onde a fronteira *deve* ficar num espaço ainda nebuloso? Modo *Collaboration* temporário — a alta comunicação vira fronteiras fluidas enquanto vocês exploram, e depois você "congela" via *X-as-a-Service*.

Os quatro tipos de time, por sua vez, são quatro *formatos de subsistema* pré-desenhados: o *stream-aligned* produz um serviço de negócio coeso; o *platform* produz uma plataforma interna com API self-service; o *complicated-subsystem* produz um módulo isolado de alta especialização. Você escolhe o tipo de time *sabendo* qual peça de arquitetura ele vai parir.

> [!note] Conway como força de design, não como maldição
> A virada de mentalidade de *Team Topologies* é parar de ver a Lei de Conway como uma *maldição* (a organização sabota a arquitetura) e passar a vê-la como uma *alavanca*. É o ponto de alavancagem de Meadows ([[15 - Pensamento sistêmico|leverage points]]) na prática: mexer na **estrutura** da organização é uma intervenção *forte e sutil*, muito mais poderosa do que ficar reescrevendo módulos (intervenção *óbvia e fraca*). A **carga cognitiva por time** é o limitador-chave: cada time tem um teto de complexidade que cabe na cabeça (é a *cognitive load* de [[01 - A complexidade como problema central|Ousterhout]], aplicada ao coletivo). Times sobrecarregados produzem software sobrecarregado, então você **dimensiona** as fronteiras de cada time para caber numa carga sustentável — e essa fronteira vira, por Conway, uma fronteira arquitetural saudável.

### A API como substituta da conversa

Há um truque arquitetural embutido na manobra inversa que merece destaque: **a interface bem definida substitui a comunicação intensa**.

Quando dois times precisam interagir muito, têm duas saídas:

1. Coordenar o tempo todo — caro, frágil, não escala.
2. **Acordar um contrato — uma API — e parar de conversar no dia a dia**: cada lado evolui atrás do contrato com autonomia.

Pela Lei de Conway, é exatamente a segunda saída que produz uma fronteira de serviço saudável. A comunicação que *resta* entre os times é fina, formal e estável — e a interface que resta entre os serviços herda essas propriedades.

Foi essa lógica que a **Amazon** institucionalizou. No começo dos anos 2000, Bezos reorganizou a engenharia em **"two-pizza teams"** — times pequenos o bastante para serem alimentados por duas pizzas — justamente para *reduzir a sobrecarga de comunicação*.

E em 2006, numa entrevista famosa à *ACM Queue*, Werner Vogels descreveu o princípio **"you build it, you run it"**: cada serviço tem um time integralmente responsável por ele, do design à operação em produção.

Times pequenos, autônomos, donos de uma capacidade ponta a ponta e obrigados a falar entre si **só através de interfaces de serviço** — é a manobra inversa de Conway aplicada antes de o termo existir. O resultado homólogo foi a arquitetura de serviços que virou marca registrada da AWS.

## Conway não é destino

Até aqui a lei pareceu uma força quase determinística. Não é. Ela é uma **gravidade**, não uma **lei de aço**: dá para resistir, mas custa energia, e é melhor saber onde se está resistindo.

A evidência mais honesta vem da própria escola que defendeu o espelhamento. **Colfer & Baldwin (2016)**, em *The Mirroring Hypothesis: Theory, Evidence, and Exceptions*, revisaram **102 estudos empíricos** em três níveis (dentro de uma firma, entre firmas, e em projetos abertos colaborativos). O espelhamento se confirmou em **~69% dos casos** — e *não* nos outros 31%. E o padrão dos resultados é informativo:

- **Mais forte dentro de uma firma** — onde a hierarquia e a co-localização apertam o acoplamento social.
- **Mais fraco entre firmas** — contratos e fronteiras de empresa relaxam o espelhamento.
- **Mais fraco ainda em projetos open source colaborativos** — onde estranhos coordenam por artefatos públicos, não por relações sociais densas.

Colfer & Baldwin organizaram as exceções — os casos em que a lei *não* se confirmou — em duas classes simétricas, que são, na verdade, as **duas receitas para "quebrar o espelho"**:

> [!abstract] Duas formas de quebrar o espelho
> 1. **Organização integrada produzindo tecnologia modular.** Uma empresa concentrada e fortemente acoplada *consegue*, com esforço deliberado, criar **partições modulares internas** — regras de design e interfaces internas tão rígidas que impõem modularidade ao produto apesar da organização concentrada. (É o que a Mozilla fez: a organização concentrada *projetou* a modularidade antes de distribuir.)
> 2. **Organização distribuída produzindo tecnologia integrada.** Grupos espalhados e não-integrados conseguem, via **contratos relacionais** fortes (regras compartilhadas, padrões, governança, confiança), construir um produto altamente integrado que sua estrutura frouxa "não deveria" permitir.

A lição: a homomorfia é a *configuração-padrão*, não a única possível. Mas quebrar o espelho **custa** — exige investimento contínuo em regras de design, governança ou relações de confiança que segurem a estrutura contra a gravidade de Conway. Quem quebra o espelho sem pagar esse custo só atrasa o momento em que a arquitetura volta ao formato do org chart.

### O org chart não é a estrutura de comunicação real

O erro mais comum ao aplicar a lei é confundir **organograma** com **estrutura de comunicação**. Conway falou em *communication structure*, não em hierarquia.

A estrutura que a arquitetura copia é a dos **canais reais** — quem revisa o PR de quem, quem está no mesmo Slack, quem almoça junto, quem responde rápido. E essa rede raramente coincide com as caixinhas do RH.

Isso muda o que você precisa observar. Em times remotos e assíncronos, o "input" da lei muda: a comunicação de alta largura de banda e baixa latência (a conversa de corredor que alinhava a interface na hora) é substituída por canais de **alta latência** (PR review, issue, doc).

A *lei* continua valendo — a arquitetura ainda copia a comunicação —, mas o que ela copia agora é uma rede mais esparsa e formal. Frequentemente isso até empurra para arquiteturas **mais modulares e contratuais**, porque a fricção de coordenar de forma síncrona favorece "definir uma API e seguir em frente" em vez de "vamos sincronizar toda terça".

A topologia de **revisão de código** e de **canais async** vira, na prática, a estrutura de comunicação que a homomorfia copia — não o organograma.

> [!example] CODEOWNERS: a estrutura de comunicação que você pode ler
> Num mundo de PRs, a estrutura de comunicação real fica *gravada em arquivo*. O `CODEOWNERS` (GitHub/GitLab) declara, por caminho do repositório, **quem precisa aprovar uma mudança** — ou seja, quem fala com quem antes de qualquer código entrar. É a rede de coordenação de Cataldo tornada explícita e versionada.
>
> Por isso o `CODEOWNERS` é, ele mesmo, uma alavanca de Conway. Se um diretório exige aprovação de *cinco* times diferentes, você acabou de declarar que aquela parte do código é um ponto de coordenação pesado — e, por homomorfia, ela tenderá a virar um gargalo arquitetural (o "binário tocado por muitas organizações" do estudo do Vista). O ideal inverso: **exatamente um time responsável por cada área**, com ownership descobrível. Quando o mapa de ownership é limpo e congruente com as dependências técnicas, a comunicação flui pelos canais certos; quando é difuso, o gap de coordenação vira defeito.
>
> A leitura prática: para *enxergar* a estrutura de comunicação real de uma organização remota, não olhe o organograma — olhe o grafo de "quem-revisa-quem" no histórico de PRs e o `CODEOWNERS`. É *essa* topologia que a arquitetura vai copiar.

> [!question] E o time cirúrgico de Brooks?
> O **surgical team** de Brooks (*The Mythical Man-Month*, cap. 3, ideia original de Harlan Mills) é uma estrutura *Conway-aware* avant la lettre. Brooks queria **integridade conceitual** — "o sistema deve ser produto de uma mente, ou no máximo duas, agindo *uno animo*". O time cirúrgico (um "cirurgião" central, todos os outros apoiando-o) é desenhado justamente para **minimizar os caminhos de comunicação** que decidem o design. Pela Lei de Conway, menos mentes nas decisões críticas → menos fragmentação de comunicação → maior coesão arquitetural. Brooks atacou o problema de Conway pelo lado da estrutura social *antes* de Conway ter um nome.

## Armadilhas comuns

> [!warning] Três modos clássicos de errar com Conway
> - **Monólito distribuído.** Fatiar serviços pela tecnologia (front/back/DB) ou pelo código legado em vez de por capacidade de negócio. A comunicação permanente entre os times vira acoplamento permanente entre os serviços. Você paga rede e perde autonomia. *Sintoma:* "não dá pra fazer deploy do serviço A sem subir B e C juntos."
> - **Reorg theater (reorganização sem rearquitetura — e vice-versa).** Mexer no org chart esperando que a arquitetura se conserte sozinha, **sem** mexer no código, ou refatorar o código **sem** mexer na comunicação. As duas estruturas estão acopladas: mexer numa só e esperar a outra acompanhar por mágica é apostar contra a homomorfia. A manobra inversa funciona quando você muda *organização e arquitetura juntas*, de propósito.
> - **Cargo cult de modelos de outras empresas.** Copiar a *estrutura* de times de uma empresa famosa como se fosse um framework universal (ver o "modelo Spotify" logo abaixo). Você não importa a estrutura de outra empresa; você projeta a *sua* a partir da arquitetura que quer e da carga cognitiva que seus times aguentam.

> [!danger] O "modelo Spotify" e sua própria retratação
> O caso de cargo cult mais famoso da engenharia tem nome: o **"modelo Spotify"** — squads, tribes, chapters e guilds — descrito num whitepaper de 2012 (Henrik Kniberg & Anders Ivarsson) e copiado por incontáveis empresas como receita de agilidade em escala.
>
> O problema: **a própria Spotify nunca operou de forma estável como o documento descrevia.** Engenheiros e coaches da casa admitiram depois que, *quando escreveram o doc, já não faziam mais aquilo*, e que o modelo gerou problemas reais internamente — coordenação fraca entre squads, trabalho duplicado, *ownership* confuso, dependência excessiva da senioridade individual. O artigo original já trazia o aviso explícito de ser *"um retrato do momento, não uma jornada concluída"* — aviso que quase todo mundo que copiou o modelo ignorou.
>
> A lição de Conway aqui é dupla. Primeiro: **estrutura organizacional não é um framework que se instala** — ela tem que casar com a *sua* arquitetura-alvo e com a *sua* carga cognitiva. Segundo, e mais sutil: copiar a estrutura de comunicação de outra empresa só faz sentido se você também quer copiar a *arquitetura* dela — e quase ninguém para pra pensar nisso. O cargo cult é a manobra inversa de Conway feita às cegas: você muda os times sem saber que arquitetura está provocando.

> [!note] Monorepo vs. polyrepo também é Conway
> Até a escolha de **repositório** é uma expressão da lei — Conway aplicado ao *layout de código-fonte*. As fronteiras dos seus repositórios tendem a copiar as fronteiras dos times, e vice-versa: o repo molda quem vê o quê, quem pode mudar o quê, e quem precisa coordenar com quem.
>
> - **Polyrepo** (um repo por serviço/time) reforça **autonomia e ownership claros** — fronteiras de segurança e de release rígidas, baixo acoplamento entre times. Alinhado a times de fluxo independentes (e à manobra inversa para microserviços). O preço: coordenar mudanças *cross-repo* é caro.
> - **Monorepo** favorece **reuso, visibilidade e padronização cross-projeto** — refatoração atômica entre projetos, um único histórico. Alinhado a times que compartilham muito código. O preço: escalar a organização num único repo exige *tooling* pesado e governança de ownership (de novo o `CODEOWNERS`), senão vira terra de ninguém.
>
> Nenhum é "certo"; cada um **materializa uma estrutura de comunicação diferente**. Times com ciclos de release e culturas de engenharia muito distintos raramente convivem bem num mesmo monorepo — a fricção que surge é a homomorfia protestando. Escolher o layout de repo sem pensar na topologia de times é, de novo, deixar a homomorfia decidir por você.

## Em entrevista

> [!tip] Como isso aparece numa entrevista
> A Lei de Conway é munição de ouro para perguntas de **system design** e de **liderança técnica**, porque mostra que você pensa além do código.
> - **Cite a lei em uma frase** e dê o exemplo do compilador de quatro passes — é memorável e prova que você entende o mecanismo (interfaces espelham comunicação).
> - Quando perguntarem *"por que essa arquitetura ficou assim?"* ou *"como você quebraria este monólito?"*, traga a **manobra inversa**: "antes de decidir os serviços, eu olharia as fronteiras de time, porque a arquitetura vai acabar copiando a organização — então desenho os times para obter os serviços que quero." Cite **Team Topologies** (times de fluxo, *X-as-a-Service*) e **carga cognitiva por time**.
> - **Traga evidência empírica, não só anedota.** Cite o estudo do **Windows Vista** (Nagappan/Murphy/Basili): métricas *organizacionais* previram defeitos com ~85% de precisão, melhor que métricas de código. É a prova de que "isto é organizacional" não é hand-waving.
> - **Mostre que você sabe os limites.** Senioridade de verdade é saber que a lei *não é destino*: cite os ~69% de Colfer & Baldwin e as duas formas de quebrar o espelho (partições modulares internas; contratos relacionais). Isso te separa de quem decorou uma frase de efeito.
> - **Diagnostique o monólito distribuído** corretamente: "isto parece um problema de arquitetura, mas é um problema de organização — refatorar código sem mexer em comunicação não resolve." E saiba citar o caso da Amazon ("two-pizza teams", "you build it, you run it") como manobra inversa real.
> - **Cuidado com o cargo cult:** se alguém propuser "vamos adotar o modelo Spotify", saber que a própria Spotify não o operava como descrito é um sinal de leitura crítica, não de decoreba.

E aqui o galho fecha. Ele começou definindo complexidade como uma propriedade da **estrutura** do sistema ([[01 - A complexidade como problema central|Ousterhout]]), passou pelos mecanismos de gerenciá-la (abstração, modularidade), aprendeu que ela **decai** com o tempo ([[13 - Entropia de software e decaimento]]) e que é **emergente** ([[15 - Pensamento sistêmico]]).

E termina reconhecendo que o "sistema" não é só o código: é **código + time + processo**. A Lei de Conway é a prova final dessa tese — a estrutura humana e a estrutura técnica são a mesma estrutura, vistas de dois ângulos.

Gerenciar complexidade, no fim, é gerenciar o todo sócio-técnico, não só os arquivos.

> [!quote] A síntese do galho em uma frase
> Toda decisão de design é uma decisão sobre complexidade — e algumas das decisões de design mais importantes você toma quando desenha o **org chart**, não o código.

## Referências

- **Melvin E. Conway** — *How Do Committees Invent?* (*Datamation*, vol. 14, n. 4, abril de 1968, p. 28-31). Origem da Lei de Conway, da homomorfia organização↔sistema, dos três passos da "desintegração" e da frase sobre a "organização ociosa em busca de trabalho". Texto e formulação canônica no site do autor: [melconway.com — Conway's Law](https://www.melconway.com/Home/Conways_Law.html) · [PDF do artigo](https://www.melconway.com/Home/pdf/committees.pdf).
- **Alan MacCormack, Carliss Y. Baldwin & John Rusnak** — *Exploring the Duality Between Product and Organizational Architectures: A Test of the "Mirroring" Hypothesis* (*Research Policy* 41(8), 2012; HBS Working Paper 08-039). Teste empírico do espelhamento via **custo de propagação**; o caso Mozilla (17,35% → 2,78%) e a comparação com o Linux; conclusão de que organizações fracamente acopladas produzem produtos mais modulares. [PDF (HBS)](https://www.hbs.edu/ris/Publication%20Files/08-039_1861e507-1dc1-4602-85b8-90d71559d85b.pdf).
- **Nachiappan Nagappan, Brendan Murphy & Victor R. Basili** — *The Influence of Organizational Structure on Software Quality: An Empirical Case Study* (ICSE 2008; Microsoft Research TR-2008-11). Estudo do **Windows Vista**: métricas **organizacionais** (profundidade de propriedade, número de organizações contribuindo, número de engenheiros/ex-engenheiros, frequência de edição) preveem propensão a falha com **precisão e recall ~85%** — estatisticamente superiores a métricas de código (churn, complexidade, cobertura, dependências, bugs pré-release). [Página MSR](https://www.microsoft.com/en-us/research/publication/the-influence-of-organizational-structure-on-software-quality-an-empirical-case-study/) · [TR (PDF)](https://www.microsoft.com/en-us/research/wp-content/uploads/2016/02/tr-2008-11.pdf).
- **Lyra J. Colfer & Carliss Y. Baldwin** — *The Mirroring Hypothesis: Theory, Evidence, and Exceptions* (*Industrial and Corporate Change* 25(5), 2016; HBS Working Paper 16-124). Revisão de **102 estudos**; espelhamento em ~69%; mais forte dentro da firma, mais fraco entre firmas e em open source; as duas classes de exceção (partições modulares internas; contratos relacionais) que "quebram o espelho". [PDF (HBS)](https://www.hbs.edu/ris/download.aspx?name=16-124.pdf).
- **Marcelo Cataldo, James D. Herbsleb & Kathleen M. Carley** — *Socio-Technical Congruence: A Framework for Assessing the Impact of Technical and Work Dependencies on Software Development Productivity* (ESEM, 2008). Refinamento da lei: alinhar **necessidades de coordenação** com **canais de coordenação reais** reduziu o tempo de resolução de modification requests em ~32%.
- **Matthew Skelton & Manuel Pais** — *Team Topologies: Organizing Business and Technology Teams for Fast Flow* (IT Revolution Press, 2019). Origem, nesta nota, da **manobra inversa de Conway** como ferramenta de design, dos **quatro tipos de time** (stream-aligned, platform, enabling, complicated-subsystem), dos **três modos de interação** (collaboration, X-as-a-service, facilitating) e da **carga cognitiva por time**.
- **Frederick P. Brooks Jr.** — *The Mythical Man-Month* (1975). Onde o apelido **"Lei de Conway"** foi popularizado, e onde está o **time cirúrgico** (cap. 3) como estrutura Conway-aware. Mesmo Brooks de [[01 - A complexidade como problema central]].
- **Werner Vogels** — *A Conversation with Werner Vogels* (entrevista a Jim Gray, *ACM Queue*, 2006). Origem do princípio **"you build it, you run it"** na Amazon, e do modelo de times-de-serviço autônomos — manobra inversa de Conway na prática.
- **Henrik Kniberg & Anders Ivarsson** — *Scaling Agile @ Spotify with Tribes, Squads, Chapters & Guilds* (whitepaper, 2012), com o aviso de ser "um retrato do momento". A retratação posterior (relatos de ex-funcionários e da própria comunidade de que a Spotify não operava o modelo como descrito, e dos problemas que ele gerou) sustenta o aviso de cargo cult desta nota.
- **Martin Fowler** — *Conway's Law* (bliki, martinfowler.com) e a literatura corrente sobre o **monólito distribuído** (*distributed monolith*) como falha de Conway: serviços fatiados por org/tecnologia que continuam acoplados (deploy conjunto, banco compartilhado, cadeias síncronas), pagando o "imposto distribuído" sem a autonomia. Base da seção sobre o anti-padrão.
- **CODEOWNERS / topologia de revisão** — documentação de `CODEOWNERS` (GitHub/GitLab) e a discussão de *collective code ownership* à luz de Conway (ex.: Industrial Logic) como evidência de que a estrutura de comunicação real, em orgs remotas/assíncronas, mora no grafo de "quem-revisa-quem", não no organograma. Base, junto de **Cataldo et al.**, da seção sobre org chart ≠ estrutura de comunicação.

> [!note] Sobre o lastro das afirmações
> Conferidos na pesquisa que alimentou esta nota: a **citação literal** da Lei de Conway, o ano (1968), o veículo (*Datamation*, após rejeição da *HBR* em 1967), a passagem da **homomorfia**, os **três passos da desintegração**, a frase da "organização ociosa", a citação sobre **flexibilidade da organização** e o **exemplo da agência de pesquisa por contrato** (COBOL 5 passes / ALGOL 3 passes) — todos atribuídos ao artigo de Conway via o site do próprio autor e resenhas do paper original. Os números **MacCormack/Baldwin** (Mozilla 17,35%→2,78%) e **Colfer & Baldwin** (102 estudos, ~69%, as duas exceções) foram conferidos em buscas sobre os papers da HBS; **não li os PDFs página a página** (o conteúdo binário não foi extraível pela ferramenta) — os números vêm das fontes secundárias e do briefing de pesquisa, com referência ao PDF primário. O **~32%** de Cataldo et al. e os tipos/modos de *Team Topologies* foram conferidos em buscas sobre os trabalhos.
>
> **Sobre o estudo do Vista (Nagappan/Murphy/Basili 2008):** o achado central — que métricas **organizacionais** previram propensão a falha com **~85% de precisão e recall**, batendo as métricas de código — foi conferido pelo *abstract* do artigo (verbatim: *"the organizational metrics when applied to data from Windows Vista were statistically significant predictors of failure-proneness"* e que a precisão/recall foi *"significantly higher"* que churn/complexidade/cobertura/dependências/bugs pré-release) e por múltiplas fontes secundárias que reportam a cifra de 85%. **O PDF primário do TR não foi extraível página a página pela ferramenta** (binário); a lista detalhada de métricas (profundidade de propriedade, número de organizações contribuindo etc.) vem do abstract e das resenhas secundárias, não de leitura integral do paper.
>
> **Correção de lastro herdada:** a versão anterior desta nota dizia ter "ficado com a versão do próprio Conway" contra a atribuição a **George Mealy**. Pesquisa adicional indica que **Mealy de fato propôs o nome "Conway's Law" antes** — no *National Symposium on Modular Programming* de julho de 1968, antes do livro de Brooks (1975). O mais preciso é: **Mealy provavelmente cunhou o termo; Brooks o popularizou** (e é por Brooks que o mundo o conhece). Mantenho ambas as figuras no texto com essa nuance.
>
> **Ressalva honesta:** o exemplo do **compilador de quatro passes** é a paráfrase de Eric S. Raymond (*Jargon File* / *New Hacker's Dictionary*), não fraseado literal de Conway. As aplicações a microserviços, monorepo/polyrepo, refatoração e entropia são minha leitura conectando as fontes, não exemplos textuais dos autores. Padrão de marcação seguindo [[06 - Abstrações que vazam]].

## Veja também

- [[15 - Pensamento sistêmico]] — Conway é pensamento sistêmico aplicado ao par organização ↔ arquitetura; o gancho desta nota nasce ali
- [[01 - A complexidade como problema central]] — onde o galho abre; a complexidade que Conway mostra ser também organizacional; Lei de Brooks e carga cognitiva de Ousterhout
- [[13 - Entropia de software e decaimento]] — por que a arquitetura "volta" ao formato do org chart se você refatora sem mexer na comunicação
- [[03-Dominios/Arquitetura/Arquitetura de Software|Arquitetura de Software]] — o domínio onde fronteiras de módulo e de time se encontram
- [[Dicionário de Fundamentos]] — verbetes do domínio (ver *Lei de Conway* e *Hipótese do espelhamento*)
