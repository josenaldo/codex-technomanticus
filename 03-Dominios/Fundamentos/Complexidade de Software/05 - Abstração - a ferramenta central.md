---
title: "Abstração - a ferramenta central"
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
  - abstracao
  - information-hiding
  - parnas
---

# Abstração - a ferramenta central

Se a complexidade é *o* problema deste galho ([[01 - A complexidade como problema central]]), a abstração é a ferramenta principal pra combatê-la. Não uma entre várias — *a* principal. Quase todo outro mecanismo de design (modularidade, encapsulamento, interfaces) é abstração aplicada de um jeito específico.

> [!abstract] TL;DR
> Abstração é uma **visão simplificada** que omite o detalhe irrelevante pra você raciocinar sobre o sistema sem ter tudo na cabeça ao mesmo tempo (Ousterhout: *"an abstraction is a simplified view of an entity, which omits unimportant details"*). O critério do que esconder veio de **Parnas (1972)**: esconda **decisões de design propensas a mudar** — não "dados" genéricos, e não os passos de um fluxograma. Cada módulo guarda um *segredo* (uma decisão volátil); quando ela muda, a mudança fica local. Cuidado com a confusão central: **abstração não é indireção**. Adicionar uma camada só é abstração se ela de fato **reduzir o que o chamador precisa saber** — senão é só um pedágio.

## O que é

A definição operacional vem de **John Ousterhout**, o mesmo autor que deu a definição de complexidade na nota de abertura:

> [!quote] Definição de abstração
> *"In modular programming, an abstraction is a simplified view of an entity, which omits unimportant details."*
> — John Ousterhout, *A Philosophy of Software Design*

Repare nos dois verbos escondidos: a abstração **suprime** detalhe (o que não importa) pra **amplificar** o que importa. É um filtro deliberado. Quando você usa uma `List`, você raciocina com "adiciona no fim, pega pelo índice" e ignora se por baixo é array dinâmico ou lista encadeada — esse detalhe foi suprimido de propósito, e graças a isso você consegue pensar no seu problema, não no da estrutura de dados.

Por que isso ataca a complexidade na raiz? Porque a memória de trabalho humana é finita (a *cognitive load* da nota 01). Você não consegue segurar um sistema inteiro na cabeça. A abstração é o que te permite raciocinar sobre uma parte **sem** carregar as outras — você confia na interface e esquece a implementação. Sem abstração, todo o sistema é um só nível, e nenhum cérebro cabe nele.

> [!note] A abstração tem dois lados
> Toda abstração tem uma **interface** (o que você precisa saber pra usá-la) e uma **implementação** (tudo que ela esconde). A arte está em manter a interface pequena e estável enquanto a implementação faz o trabalho pesado. Guarde essa tensão: ela volta com força em [[07 - Módulos profundos e rasos]], onde vira o critério pra dimensionar um módulo.

## Information hiding: esconder a decisão que vai mudar

A pergunta seguinte é inevitável: **o que** uma abstração deve esconder? Esconder qualquer coisa não basta — esconder a coisa errada é pior que não esconder nada.

A resposta canônica é de **David Parnas**, no clássico *On the Criteria To Be Used in Decomposing Systems into Modules* (CACM 15(12), 1972). O critério dele é cirúrgico:

> [!quote] O critério de Parnas
> Cada módulo deve **esconder uma decisão de design propensa a mudar** — não "esconder dados" em abstrato, e não decompor o sistema pelos **passos do fluxograma**.

Duas negações fazem todo o peso aqui:

- **Não é "esconder dados".** Esconder o tipo de um campo é encapsulamento de superfície. O que Parnas quer esconder é a **decisão**: o formato do arquivo, o algoritmo de ordenação, a representação interna de uma tabela. Dado é consequência; a decisão é a causa.
- **Não é decompor por etapas.** A intuição ingênua manda dividir o programa pelos passos da execução (leia entrada → processe → escreva saída), um módulo por etapa. Parnas mostra que isso é frágil: cada módulo conhece detalhes dos outros, e mudar uma decisão respinga em todos. A decomposição boa é por **segredo** — cada módulo guarda uma decisão volátil e expõe só uma interface estável sobre ela.

O ganho concreto: quando a decisão escondida muda (e decisões voláteis *vão* mudar), a mudança fica **contida** dentro do módulo que a guardava. Os clientes não percebem. Compare com a nota 01: isso é atacar diretamente a **change amplification** — em vez de a mudança respingar em vinte arquivos, ela mora num só.

> [!tip] A pergunta de projeto que isso te dá
> Diante de um módulo, pergunte: *"que decisão propensa a mudar este módulo protege?"* Se você não consegue nomear o segredo, provavelmente não há abstração ali — só código agrupado por acaso. E se o segredo vaza pela interface (nomes, tipos, ordem de chamadas que denunciam a implementação), a troca futura da decisão quebra os clientes.

## Abstração ≠ indireção

Aqui mora o erro mais comum, e vale uma seção inteira: **adicionar uma camada não é, por si só, abstrair.**

Indireção é interpor algo entre o chamador e o trabalho (uma função que chama outra, uma interface com um único implementador, um wrapper). Abstração é **reduzir o que o chamador precisa saber**. As duas coisas costumam andar juntas, mas não são a mesma — e confundi-las produz arquitetura ruim.

Ousterhout dá nome ao caso patológico: o **shallow module** (módulo raso) e o método *pass-through* — uma camada cuja interface é tão complicada quanto o que ela entrega, que repassa a chamada pra baixo sem esconder nada. Você teve o custo de mais uma camada (mais um nome pra aprender, mais um arquivo pra abrir, mais um salto pra seguir no debug) **sem** o benefício de esconder complexidade. O saldo é negativo: a indireção *adicionou* carga cognitiva em vez de reduzi-la.

> [!example] Indireção que não abstrai
> Um `UserService.getUser(id)` que só faz `return userRepository.findById(id)` — mesma assinatura, mesmos parâmetros, mesmo retorno, nenhuma decisão escondida. A camada existe, mas o chamador precisa saber exatamente o que precisaria sem ela. É indireção pura: custo de salto, benefício zero. Vira abstração de verdade só quando passa a *esconder* algo (cache, autorização, montagem de um agregado, tradução de erros) que o chamador deixa de carregar.

O teste é simples: **depois da camada, o chamador precisa saber menos?** Se sim, você abstraiu. Se ele precisa saber o mesmo (ou mais — porque agora tem que entender a camada *e* o que há embaixo), você só empilhou indireção. "Adicionar um nível de indireção resolve qualquer problema" é piada de programador justamente porque o nível mal-colocado *cria* problema.

## Boas vs. más abstrações

Junte as duas ideias — visão simplificada (Ousterhout) + esconder a decisão volátil (Parnas) — e o critério de qualidade cai sozinho:

- **Boa abstração:** esconde os detalhes **certos** (o volátil, o irrelevante) atrás de uma interface **pequena e estável**. Ela mantém sua promessa: você usa a interface e legitimamente esquece o resto. Os melhores módulos, em Ousterhout, são **profundos** — muita funcionalidade atrás de uma interface enxuta (assunto da [[07 - Módulos profundos e rasos]]).
- **Má abstração (errada):** ou **esconde o que você precisa** (te força a contornar a interface, abrir a caixa, depender de detalhe interno), ou **vaza o que escondeu** (a decisão interna reaparece no comportamento observável). A interface grande relativa ao que entrega é o sintoma do módulo raso; o vazamento é o tema da nota vizinha.

> [!warning] Toda abstração é uma aposta
> Você aposta em *qual* decisão é volátil e *qual* é estável — e esconde a primeira atrás da segunda. Acertar a aposta é o que separa a abstração que envelhece bem da que vira pedágio. Quando a aposta erra (você expôs o que devia esconder, ou escondeu o que devia expor), a abstração trabalha contra você. E mesmo a melhor abstração não esconde *tudo* o tempo todo — onde e por que ela falha é o assunto inteiro de [[06 - Abstrações que vazam]].

Esta nota é a afirmação **positiva**: o que abstração é e por que ela é a ferramenta central. As duas notas seguintes a tensionam pelos limites — onde abstrações **vazam** ([[06 - Abstrações que vazam]]) e como **dimensionar** um módulo pra que a abstração seja profunda, não rasa ([[07 - Módulos profundos e rasos]]).

## Referências

- **David Parnas** — [On the Criteria To Be Used in Decomposing Systems into Modules](https://dl.acm.org/doi/10.1145/361598.361623) (CACM 15(12), 1972, p. 1053-1058). Origem do *information hiding*: o critério de decomposição é esconder **decisões de design propensas a mudar**, não dados nem etapas de fluxograma. Título, veículo e ano conferidos via ACM Digital Library e dblp.
- **John Ousterhout** — *A Philosophy of Software Design* (1ª ed. 2018; 2ª ed. 2021, Yaknyam Press). Origem da definição de abstração (*"a simplified view of an entity, which omits unimportant details"*) e da distinção módulo **profundo** vs. **raso** / método *pass-through* (indireção que não abstrai).

> [!note] Sobre o lastro
> A definição de abstração de Ousterhout e a tese de Parnas ("esconder decisões propensas a mudar") foram conferidas contra resumos e fontes secundárias confiáveis na pesquisa que alimentou esta nota; os dados bibliográficos de Parnas (CACM 15(12), 1972) batem com ACM e dblp. **Ressalva honesta:** não consultei o texto integral de cada obra página a página. A formulação exata de Ousterhout sobre *pass-through methods* e o saldo "custo de indireção sem benefício" é paráfrase fiel ao argumento do livro, mas pode diferir em palavras da redação literal do autor — o padrão de marcação de incerteza segue o da nota vizinha [[06 - Abstrações que vazam]].

## Veja também

- [[06 - Abstrações que vazam]] — os limites: onde e por que mesmo boas abstrações vazam
- [[07 - Módulos profundos e rasos]] — como dimensionar um módulo pra que a abstração seja profunda
- [[01 - A complexidade como problema central]] — o problema que a abstração existe pra combater
- [[Orientação a Objetos]] — encapsulamento, o mecanismo de linguagem que implementa information hiding
- [[Dicionário de Fundamentos]] — verbetes do domínio
