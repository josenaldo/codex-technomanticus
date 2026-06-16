---
title: "Lei de Conway"
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
  - lei-de-conway
  - organizacao
---

# Lei de Conway

A nota anterior ([[15 - Pensamento sistêmico]]) terminou com um gancho: a forma como um time se comunica acaba **estampada** na forma do software, e isso é um efeito sistêmico — uma propriedade que emerge do acoplamento entre a estrutura humana e a estrutura técnica. Esta nota desenvolve esse resultado por inteiro. Ele tem nome próprio, autor e ano, e é uma das observações mais antigas e mais subestimadas da engenharia de software. Também é o ponto onde o galho fecha, porque ele prova a tese mais incômoda de toda a trilha: **a complexidade não é só técnica — ela mora no sistema humano também.**

> [!abstract] TL;DR
> A **Lei de Conway** (Melvin Conway, 1968) diz que qualquer organização que projeta um sistema produz um design cuja **estrutura é uma cópia da estrutura de comunicação dessa organização**. O mecanismo é simples: módulos são construídos por times, e a interface entre dois módulos espelha a comunicação (ou a falta dela) entre os dois times. Consequência: a **complexidade organizacional vaza para a arquitetura** — quatro times montando um compilador tendem a produzir um compilador de quatro passes. Como o espelhamento acontece de qualquer jeito, dá pra usá-lo a favor: a **manobra inversa de Conway** molda a organização *de propósito* para **provocar** a arquitetura desejada (popularizada por *Team Topologies*, de Skelton & Pais). Moral prática: **você não conserta um problema de arquitetura que na verdade é um problema de organização mexendo só no código.**

## O que é

Pergunta de abertura: por que dois times igualmente competentes, com o mesmo problema e as mesmas ferramentas, produzem arquiteturas tão diferentes? Em 1968, **Melvin Conway** deu uma resposta que ninguém esperava — a diferença está menos na engenharia e mais em **quem fala com quem**.

A formulação literal, do artigo *How Do Committees Invent?* (Datamation, abril de 1968):

> [!quote] Lei de Conway
> *"Any organization that designs a system (defined more broadly here than just information systems) will inevitably produce a design whose structure is a copy of the organization's communication structure."*
> — Melvin E. Conway, *How Do Committees Invent?* (1968)

O **mecanismo** é quase tautológico depois que você o vê. Para que dois módulos de software se encaixem corretamente, **as pessoas** que projetam e implementam cada um precisam se comunicar — alinhar a interface, combinar o contrato, negociar quem faz o quê. Logo, a interface entre dois módulos só pode ser tão boa, tão rica e tão bem-acabada quanto a comunicação entre os dois grupos que os constroem. A estrutura de **interfaces** do sistema acaba sendo uma imagem da estrutura de **comunicação** da organização. Conway resume isso dizendo que existe uma **homomorfia** — uma correspondência estrutural — entre a organização e o sistema que ela projeta.

> [!note] O nome "Lei de Conway" não é de Conway
> Conway escreveu o artigo; o **apelido "Lei de Conway" foi cunhado por Fred Brooks**, que citou e batizou a ideia em *The Mythical Man-Month*. (É o mesmo Brooks da [[01 - A complexidade como problema central|complexidade essencial e do "No Silver Bullet"]] — o galho gira em torno de um punhado de gigantes que se citam.) Detalhe de origem: Conway submeteu o texto à *Harvard Business Review* em 1967, foi rejeitado, e só então a *Datamation* o publicou em 1968.

## A complexidade organizacional vaza para a arquitetura

Aqui está o elo direto com o galho. Se a arquitetura espelha a comunicação do time, então **a complexidade da organização vaza para a complexidade do sistema** — ela atravessa a fronteira entre o humano e o técnico e se materializa em código. Um org chart confuso, com responsabilidades sobrepostas e comunicação ruidosa, tende a parir uma arquitetura confusa, com responsabilidades sobrepostas e acoplamento ruidoso. Não porque os engenheiros sejam ruins; porque eles estão, sem querer, **codificando o formato da organização**.

> [!example] O compilador de quatro passes
> A ilustração canônica: *"se você tem quatro grupos trabalhando num compilador, vai obter um compilador de quatro passes."* Cada grupo controla um pedaço; as fronteiras entre os pedaços viram as fronteiras entre os passes; o número de fases do compilador acaba refletindo o número de equipes, não a melhor decomposição técnica do problema. A decisão de **arquitetura** (quantos passes?) foi tomada, sem ninguém perceber, pela decisão de **organização** (quantos grupos?).
>
> Ressalva de honestidade: essa frase específica não é citação literal de Conway — é a paráfrase popularizada por Eric S. Raymond no *Jargon File* / *The New Hacker's Dictionary*. O *exemplo* do compilador, porém, está em espírito no artigo original; o fraseado é que é de Raymond.

Repare como isso reabre temas que o galho já visitou. É um efeito de **segunda ordem** ([[15 - Pensamento sistêmico]]): você organiza os times pensando só em RH e planejamento, e a consequência aparece longe dali, na forma do software. É também uma forma de **complexidade emergente** — ela não está em nenhum engenheiro nem em nenhum org chart isolado; emerge do **acoplamento** entre as duas estruturas. E é por isso que a complexidade arquitetural às vezes resiste a toda refatoração: você está combatendo no código um problema cuja raiz está no **formato da organização**, e o código teima em voltar à forma do org chart porque é isso que a comunicação real produz.

> [!warning] A armadilha do "vamos só refatorar"
> Daí o erro mais comum e mais caro: tratar como **bug de código** o que é **homomorfia de org chart**. Dois times que mal conversam vão produzir uma interface pobre entre seus módulos por mais que você refatore — porque a interface ruim *é o reflexo fiel* da comunicação ruim. Mude o código sem mudar a comunicação e a entropia ([[13 - Entropia de software e decaimento]]) o puxa de volta ao formato da organização. Fronteiras de time, carga cognitiva por time e caminhos de comunicação **são forças arquiteturais**, tão reais quanto acoplamento e coesão.

## A manobra inversa de Conway

Se a arquitetura vai espelhar a comunicação **de qualquer jeito**, há uma jogada óbvia escondida na lei: em vez de sofrer o espelhamento, **use-o**. Essa é a **manobra inversa de Conway** (*inverse Conway maneuver*, também *reverse Conway*): em vez de impor uma arquitetura e torcer pra organização segui-la, você **desenha a organização de propósito** para **provocar** a arquitetura que quer. Quer microserviços com fronteiras limpas e autônomas? Monte times pequenos, autônomos, donos de uma fatia de negócio ponta a ponta. A estrutura humana vai puxar a estrutura técnica na direção desejada.

A formulação moderna mais influente disso é **Team Topologies**, de **Matthew Skelton e Manuel Pais** (2019), que pega Conway e o transforma numa ferramenta de design organizacional. Dois conceitos da obra importam aqui:

- **Carga cognitiva por time.** Um time tem um teto de complexidade que consegue carregar na cabeça (é a *cognitive load* de [[01 - A complexidade como problema central|Ousterhout]], agora aplicada ao coletivo, não ao indivíduo). Times sobrecarregados produzem software sobrecarregado. Então você **dimensiona** as fronteiras de cada time para caber numa carga cognitiva sustentável — e essa fronteira de time vira, por Conway, uma fronteira arquitetural saudável.
- **Times alinhados ao fluxo** (*stream-aligned teams*). O tipo de time padrão na obra: dono de um único fluxo de valor de ponta a ponta (uma jornada, uma capacidade de negócio), cross-funcional e autônomo, com o mínimo de handoffs. A aposta é que, por Conway, um time assim produz um *serviço* assim — coeso, com fronteira clara, baixo acoplamento com os vizinhos.

> [!note] Conway como força de design, não como maldição
> A virada de mentalidade de *Team Topologies* é parar de ver a Lei de Conway como uma *maldição* (a organização sabota a arquitetura) e passar a vê-la como uma *alavanca*. É o ponto de alavancagem de Meadows ([[15 - Pensamento sistêmico|leverage points]]) na prática: mexer na **estrutura** da organização é uma intervenção *forte e sutil*, muito mais poderosa do que ficar reescrevendo módulos (intervenção *óbvia e fraca*). O org chart é, em boa medida, o primeiro diagrama de arquitetura — e quase ninguém o desenha pensando nisso.

## Em entrevista

> [!tip] Como isso aparece numa entrevista
> A Lei de Conway é munição de ouro para perguntas de **system design** e de **liderança técnica**, porque mostra que você pensa além do código.
> - **Cite a lei em uma frase** e dê o exemplo do compilador de quatro passes — é memorável e prova que você entende o mecanismo (interfaces espelham comunicação).
> - Quando perguntarem *"por que essa arquitetura ficou assim?"* ou *"como você quebraria este monólito?"*, traga a **manobra inversa**: "antes de decidir os serviços, eu olharia as fronteiras de time, porque a arquitetura vai acabar copiando a organização — então desenho os times para obter os serviços que quero." Isso te diferencia de quem só fala de tecnologia.
> - Bandeira de senioridade: reconhecer que *"isto parece um problema de arquitetura, mas é um problema de organização"* — e que refatorar código sem mexer em comunicação não resolve. Mencionar *Team Topologies* e **carga cognitiva por time** sela o ponto.

E aqui o galho fecha. Ele começou definindo complexidade como uma propriedade da **estrutura** do sistema ([[01 - A complexidade como problema central|Ousterhout]]), passou pelos mecanismos de gerenciá-la (abstração, modularidade), aprendeu que ela **decai** com o tempo ([[13 - Entropia de software e decaimento]]) e que é **emergente** ([[15 - Pensamento sistêmico]]), e termina reconhecendo que o "sistema" não é só o código: é **código + time + processo**. A Lei de Conway é a prova final dessa tese — a estrutura humana e a estrutura técnica são a mesma estrutura, vistas de dois ângulos. Gerenciar complexidade, no fim, é gerenciar o todo sócio-técnico, não só os arquivos.

> [!quote] A síntese do galho em uma frase
> Toda decisão de design é uma decisão sobre complexidade — e algumas das decisões de design mais importantes você toma quando desenha o **org chart**, não o código.

## Referências

- **Melvin E. Conway** — *How Do Committees Invent?* (*Datamation*, vol. 14, n. 4, abril de 1968, p. 28-31). Origem da Lei de Conway e do conceito de homomorfia entre estrutura organizacional e estrutura do sistema. Texto e formulação canônica no site do autor: [melconway.com — Conway's Law](https://www.melconway.com/Home/Conways_Law.html) · [PDF do artigo](https://www.melconway.com/Home/pdf/committees.pdf).
- **Matthew Skelton & Manuel Pais** — *Team Topologies: Organizing Business and Technology Teams for Fast Flow* (IT Revolution Press, 2019). Origem, nesta nota, da **manobra inversa de Conway** como ferramenta de design, da noção de **carga cognitiva por time** e dos **stream-aligned teams**.
- **Frederick P. Brooks Jr.** — *The Mythical Man-Month* (1975). Onde o apelido **"Lei de Conway"** foi cunhado. Mesmo Brooks de [[01 - A complexidade como problema central]].

> [!note] Sobre o lastro das afirmações
> A **citação literal** da Lei de Conway, o ano (1968) e o veículo (*Datamation*, após rejeição da *Harvard Business Review* em 1967) foram **conferidos no site do próprio Conway** na pesquisa que alimentou esta nota. Que **Brooks** cunhou o apelido "Conway's Law" em *The Mythical Man-Month* também está afirmado pelo site do autor (uma fonte secundária independente chegou a atribuir o termo a George Mealy; fiquei com a versão do próprio Conway). A existência de *Team Topologies* (Skelton & Pais, 2019) e seus conceitos (inverse Conway maneuver, carga cognitiva, stream-aligned teams) foram conferidos em resenhas e materiais sobre o livro. **Ressalva honesta:** o exemplo do **compilador de quatro passes** é a paráfrase de Eric S. Raymond (*Jargon File* / *New Hacker's Dictionary*), não fraseado literal de Conway; não li os textos primários de Conway e de *Team Topologies* página a página — as aplicações a microserviços, refatoração e entropia são minha leitura, não exemplos dos autores. Padrão de marcação seguindo [[06 - Abstrações que vazam]].

## Veja também

- [[15 - Pensamento sistêmico]] — Conway é pensamento sistêmico aplicado ao par organização ↔ arquitetura; o gancho desta nota nasce ali
- [[01 - A complexidade como problema central]] — onde o galho abre; a complexidade que Conway mostra ser também organizacional
- [[03-Dominios/Arquitetura/Arquitetura de Software|Arquitetura de Software]] — o domínio onde fronteiras de módulo e de time se encontram
- [[Dicionário de Fundamentos]] — verbetes do domínio
