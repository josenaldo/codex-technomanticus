---
title: "Abstração - a ferramenta central"
created: 2026-06-16
updated: 2026-06-16
type: concept
progress: backlog
status: growing
publish: false
fase: adepto
tags:
  - engenharia
  - complexidade-de-software
  - adepto
  - abstracao
  - information-hiding
  - parnas
  - liskov
  - sicp
---

# Abstração - a ferramenta central

Se a complexidade é *o* problema deste galho ([[01 - A complexidade como problema central]]), a abstração é a ferramenta principal pra combatê-la.

Não uma entre várias — *a* principal.

Quase todo outro mecanismo de design (modularidade, encapsulamento, interfaces) é abstração aplicada de um jeito específico. Tire a abstração da mesa e os outros mecanismos desaparecem junto.

> [!abstract] TL;DR
> Abstração é uma **visão simplificada** que omite o detalhe irrelevante pra você raciocinar sobre o sistema sem ter tudo na cabeça ao mesmo tempo (Ousterhout: *"an abstraction is a simplified view of an entity, which omits unimportant details"*). Ela não te deixa **vago** — te dá um **novo nível semântico** em que dá pra ser preciso (Dijkstra). O critério do que esconder veio de **Parnas (1972)**: esconda **decisões de design propensas a mudar** — não "dados" genéricos, e não os passos de um fluxograma. Cada módulo guarda um *segredo* (uma decisão volátil); quando ela muda, a mudança fica local. Cuidado com a confusão central: **abstração não é indireção** — adicionar uma camada só abstrai se de fato **reduzir o que o chamador precisa saber**, senão é pedágio. E o contraponto sênior: a abstração **errada** custa mais caro que a duplicação que ela tentou eliminar (Metz). Prefira duplicar até a abstração certa se revelar (regra de três).

## O que é

A definição operacional vem de **John Ousterhout**, o mesmo autor que deu a definição de complexidade na nota de abertura:

> [!quote] Definição de abstração
> *"In modular programming, an abstraction is a simplified view of an entity, which omits unimportant details."*
> — John Ousterhout, *A Philosophy of Software Design*

Repare nos dois verbos escondidos: a abstração **suprime** detalhe (o que não importa) pra **amplificar** o que importa. É um filtro deliberado.

Quando você usa uma `List`, você raciocina com "adiciona no fim, pega pelo índice" e ignora se por baixo é array dinâmico ou lista encadeada. Esse detalhe foi suprimido de propósito.

E graças a esse corte você consegue pensar no *seu* problema, não no da estrutura de dados.

Por que isso ataca a complexidade na raiz?

Porque a memória de trabalho humana é finita (a *cognitive load* da nota 01). Você não consegue segurar um sistema inteiro na cabeça.

A abstração é o que te permite raciocinar sobre uma parte **sem** carregar as outras — você confia na interface e esquece a implementação.

Sem abstração, todo o sistema é um só nível, e nenhum cérebro cabe nele.

> [!note] O que a abstração ataca — e o que não consegue atacar
> A abstração é a arma principal contra a complexidade **acidental** (a que vem das ferramentas e da representação, não do problema). Ela não elimina a complexidade **essencial** — a que é inerente ao domínio: nenhuma interface enxuta faz com que cobrar imposto deixe de ter cem regras. O que a boa abstração faz é **organizar** a complexidade essencial em níveis em que você lida com um pedaço por vez, e **dissolver** a acidental que você mesmo criou. Por isso ela é central sem ser milagrosa — fronteira detalhada em [[02 - Complexidade essencial vs. acidental]] (Brooks, *No Silver Bullet*).

> [!note] A abstração tem dois lados
> Toda abstração tem uma **interface** (o que você precisa saber pra usá-la) e uma **implementação** (tudo que ela esconde). A arte está em manter a interface pequena e estável enquanto a implementação faz o trabalho pesado. Guarde essa tensão: ela volta com força em [[07 - Módulos profundos e rasos]], onde vira o critério pra dimensionar um módulo.

### Abstrair não é ficar vago — é mudar de nível

Há um mal-entendido perigoso embutido na palavra "abstrato": no uso comum, *abstrato* é sinônimo de *vago, impreciso, nebuloso*.

Em software é o **oposto**.

Quem cunhou a formulação definitiva foi **Edsger Dijkstra**:

> [!quote] Dijkstra sobre o propósito da abstração
> *"The purpose of abstraction is not to be vague, but to create a new semantic level in which one can be absolutely precise."*
> — Edsger W. Dijkstra, *EWD 356* (Grenoble, dez. 1972)

Leia com calma. A abstração não apaga informação pra te deixar na dúvida; ela **cria uma nova camada de vocabulário** em que você fala com precisão *outra* — uma precisão de nível mais alto.

Quando você diz `lista.ordenar()`, não está sendo vago sobre o algoritmo. Está sendo **exato** num nível onde "ordenar" é uma operação atômica e bem definida, e o algoritmo simplesmente não pertence a esse nível de discurso.

Trocar de nível semântico é o movimento; perder precisão seria o defeito.

Repare que Dijkstra publica isso no **mesmo mês e ano** em que Parnas publica o critério de information hiding (dez. 1972). Não é coincidência: 1972 é o ano em que a ideia de que *programar é construir torres de níveis de abstração* amadurece como disciplina.

A divisão de trabalho entre os dois é limpa:

- **Dijkstra** dá o **porquê** — criar níveis em que se é preciso.
- **Parnas** dá o **como escolher a fronteira** — esconder o volátil.

## Information hiding: esconder a decisão que vai mudar

A pergunta seguinte é inevitável: **o que** uma abstração deve esconder?

Esconder qualquer coisa não basta. Esconder a coisa errada é pior que não esconder nada.

A resposta canônica é de **David Parnas**, no clássico *On the Criteria To Be Used in Decomposing Systems into Modules* (CACM 15(12), 1972). O critério dele é cirúrgico:

> [!quote] O critério de Parnas
> Cada módulo deve **esconder uma decisão de design propensa a mudar** — não "esconder dados" em abstrato, e não decompor o sistema pelos **passos do fluxograma**.

Duas negações fazem todo o peso aqui:

- **Não é "esconder dados".** Esconder o tipo de um campo é encapsulamento de superfície. O que Parnas quer esconder é a **decisão**: o formato do arquivo, o algoritmo de ordenação, a representação interna de uma tabela. Dado é consequência; a decisão é a causa.
- **Não é decompor por etapas.** A intuição ingênua manda dividir o programa pelos passos da execução (leia entrada → processe → escreva saída), um módulo por etapa. Parnas mostra que isso é frágil: cada módulo conhece detalhes dos outros, e mudar uma decisão respinga em todos. A decomposição boa é por **segredo** — cada módulo guarda uma decisão volátil e expõe só uma interface estável sobre ela.

O ganho concreto: quando a decisão escondida muda (e decisões voláteis *vão* mudar), a mudança fica **contida** dentro do módulo que a guardava. Os clientes não percebem.

Compare com a nota 01: isso é atacar diretamente a **change amplification**. Em vez de a mudança respingar em vinte arquivos, ela mora num só.

### O exemplo do próprio Parnas: o índice KWIC

Parnas não argumenta no abstrato. Ele pega um programinha de brinquedo, o **KWIC** (*Key Word In Context*), e o decompõe de **duas** formas pra contrastá-las.

O KWIC recebe linhas de texto, gera todas as rotações circulares de cada linha (tirar a primeira palavra e jogá-la no fim, repetidamente) e imprime tudo em ordem alfabética.

- **Decomposição 1 — por etapas do fluxograma.** Um módulo lê a entrada, outro gera as rotações, outro alfabetiza, outro imprime. Parece organizado, mas é uma armadilha: *todos* os módulos compartilham o conhecimento de **como as linhas estão armazenadas na memória** (qual array, qual layout de caracteres). Mude essa decisão de armazenamento — por exemplo, pra economizar memória guardando índices em vez de copiar caracteres — e você toca em **todos** os módulos de uma vez.
- **Decomposição 2 — por segredo.** Aqui aparece um módulo `Line Storage` cujo **único** trabalho é guardar o segredo "como os caracteres ficam dispostos na memória". Os outros módulos não sabem nada do layout: pedem "me dá a i-ésima palavra da j-ésima linha" e recebem. Trocar a representação interna agora mexe **só** dentro de `Line Storage`.

A diferença fica nítida quando você olha o que cada decomposição expõe. Na primeira, o alfabetizador mergulha no array bruto:

```text
# Decomposição 1 — o alfabetizador conhece o layout
caracteres[][] global         # array compartilhado por TODOS
alfabetizar():
    para cada par de linhas i, j em caracteres[][]:
        comparar lendo caractere a caractere de caracteres[i] e caracteres[j]
    # mude o layout de 'caracteres' → este código quebra
```

Na segunda, o mesmo alfabetizador fala só com a interface do `Line Storage` e nunca toca no layout:

```text
# Decomposição 2 — o alfabetizador só conhece a interface
alfabetizar():
    para cada par de linhas i, j:
        comparar palavra(i, 0..) com palavra(j, 0..)   # via Line Storage
    # 'palavra(linha, k)' é a interface; o layout interno é segredo
    # trocar array por índices empacotados → SÓ Line Storage muda
```

A primeira versão *vaza* o segredo (o layout) pra dentro de quem só queria ordenar. A segunda o sela atrás de uma operação nomeada.

> [!example] O segredo, isolado num módulo
> Na segunda decomposição, cada módulo é caracterizado por *uma* decisão de design que ele esconde dos demais. `Line Storage` esconde o layout dos caracteres; o módulo de circular shifts esconde *como* as rotações são computadas (calculadas na hora? pré-materializadas?); o alfabetizador esconde o algoritmo de ordenação. Cada segredo é uma alavanca que você pode mexer sem o sistema inteiro saber.

A lição que atravessou meio século: a decomposição que **parece** mais natural (seguir o fluxo de execução) é justamente a que mais espalha conhecimento — e portanto a mais frágil a mudanças.

A decomposição boa contraria a intuição. Ela agrupa por **o que precisa ser escondido**, não por **o que acontece primeiro**.

Abaixo, o desenho do information hiding em uma fronteira: o chamador depende só da interface; o segredo volátil fica trancado atrás dela.

```mermaid
flowchart LR
    C1[Chamador A] --> I
    C2[Chamador B] --> I
    C3[Chamador C] --> I
    subgraph M[Módulo]
        I[Interface\nestável e pequena]
        I -.protege.-> S[(Segredo:\ndecisão volátil\nformato / algoritmo /\nlayout interno)]
    end
    style S fill:#3b2f1e,stroke:#b8860b,color:#f5deb3
    style I fill:#1e2a3b,stroke:#4682b4,color:#d6e4f0
```

*Leitura do diagrama:* os chamadores tocam apenas a interface (caixa azul); o segredo (caixa âmbar) — a decisão que vai mudar — fica selado atrás dela, de modo que trocá-lo não chega a ninguém de fora.

> [!tip] A pergunta de projeto que isso te dá
> Diante de um módulo, pergunte: *"que decisão propensa a mudar este módulo protege?"* Se você não consegue nomear o segredo, provavelmente não há abstração ali — só código agrupado por acaso. E se o segredo vaza pela interface (nomes, tipos, ordem de chamadas que denunciam a implementação), a troca futura da decisão quebra os clientes.

## Abstração ≠ indireção

Aqui mora o erro mais comum, e vale uma seção inteira: **adicionar uma camada não é, por si só, abstrair.**

Indireção é interpor algo entre o chamador e o trabalho: uma função que chama outra, uma interface com um único implementador, um wrapper.

Abstração é **reduzir o que o chamador precisa saber**.

As duas coisas costumam andar juntas, mas não são a mesma — e confundi-las produz arquitetura ruim.

Ousterhout dá nome ao caso patológico: o **shallow module** (módulo raso) e o método *pass-through*. É uma camada cuja interface é tão complicada quanto o que ela entrega, que repassa a chamada pra baixo sem esconder nada.

Você teve o custo de mais uma camada — mais um nome pra aprender, mais um arquivo pra abrir, mais um salto pra seguir no debug — **sem** o benefício de esconder complexidade.

O saldo é negativo: a indireção *adicionou* carga cognitiva em vez de reduzi-la.

> [!example] Indireção que não abstrai
> Um `UserService.getUser(id)` que só faz `return userRepository.findById(id)` — mesma assinatura, mesmos parâmetros, mesmo retorno, nenhuma decisão escondida. A camada existe, mas o chamador precisa saber exatamente o que precisaria sem ela. É indireção pura: custo de salto, benefício zero. Vira abstração de verdade só quando passa a *esconder* algo (cache, autorização, montagem de um agregado, tradução de erros) que o chamador deixa de carregar.

O teste é simples: **depois da camada, o chamador precisa saber menos?**

Se sim, você abstraiu. Se ele precisa saber o mesmo (ou mais — porque agora tem que entender a camada *e* o que há embaixo), você só empilhou indireção.

"Adicionar um nível de indireção resolve qualquer problema" é piada de programador justamente porque o nível mal-colocado *cria* problema.

## Níveis de abstração: torres que escondem o andar de baixo

Volte ao "novo nível semântico" de Dijkstra. Um sistema inteiro de software é uma **torre** desses níveis, e cada andar tem uma propriedade mágica: ele esconde o andar de baixo.

Você programa em uma linguagem de alto nível e quase nunca pensa em registradores. Usa um banco de dados e não pensa em setores de disco. Chama uma API HTTP e não pensa em pacotes TCP.

Cada nível **assume** que o de baixo funciona e fala um vocabulário mais próximo do seu problema.

```mermaid
flowchart TB
    D[Domínio do negócio\n'criar pedido', 'cobrar cliente'] --> L
    L[Biblioteca / framework\nList, HttpClient, ORM] --> P
    P[Linguagem de alto nível\nfunções, tipos, objetos] --> I
    I[Instruções / bytecode\nADD, LOAD, JMP] --> H
    H[Hardware\nregistradores, portas lógicas]
    style D fill:#1e3b2a,stroke:#2e8b57,color:#d6f0e4
    style H fill:#3b1e1e,stroke:#a0522d,color:#f0d6d6
```

*Leitura do diagrama:* cada nível depende do de baixo, mas só pela interface — quem escreve regra de negócio (topo) raciocina com "pedido" e "cliente" e legitimamente ignora registradores (base); a torre só funciona porque cada andar esconde o anterior.

O poder disso é que você só precisa segurar **um andar** na cabeça por vez.

O perigo é que andares mal-construídos vazam. E quando vazam, você é obrigado a descer de nível pra entender um bug, perdendo justamente a proteção que a torre prometia.

Esse fenômeno tem nota própria: [[06 - Abstrações que vazam]].

> [!note] Nível de abstração ≠ "alto/baixo nível" como elogio
> "Alto nível" não quer dizer "melhor" — quer dizer "mais distante do hardware, mais perto do domínio". Cada nível existe pra um público. O erro clássico é **misturar níveis no mesmo módulo** (uma função que monta SQL cru *e* decide regra de negócio *e* formata HTML): ela obriga você a pensar em três andares ao mesmo tempo, anulando a torre. Manter cada unidade em **um** nível de abstração é metade do que se chama "código limpo".

### Barreiras de abstração: a versão SICP da torre

A torre de níveis ganha uma formulação ainda mais precisa no clássico *Structure and Interpretation of Computer Programs* (SICP), de **Harold Abelson e Gerald Jay Sussman** (MIT, 1985).

Lá o conceito se chama **barreira de abstração** (*abstraction barrier*), e o desenho é literal: linhas horizontais que separam os níveis do sistema.

A regra de cada barreira é uma só frase, e vale decorar:

> [!quote] A regra da barreira (SICP)
> *"In effect, procedures at each level are the interfaces that define the abstraction barriers and connect the different levels."* — e o que está do outro lado da barreira é, por construção, **irrelevante** para o código deste lado.

O mecanismo que sustenta a barreira tem dois tipos de procedimento, e nomeá-los ajuda a enxergar a fronteira:

- **Construtores** — montam o dado abstrato a partir da representação concreta (ex.: `fazer_racional(n, d)`).
- **Seletores** — leem partes do dado abstrato sem revelar como ele é guardado (ex.: `numerador(r)`, `denominador(r)`).

Todo o resto do programa fala **só** com construtores e seletores. Ninguém acima da barreira sabe se o número racional é um par, uma lista ou dois inteiros empacotados num só.

O ganho é o mesmo do Parnas, dito de outro jeito:

> [!quote] Por que a barreira ajuda (SICP)
> *"Constraining the dependence on the representation to a few interface procedures helps us design programs as well as modify them, because it allows us to maintain the flexibility to consider alternate implementations."*

Em uma frase: porque a dependência da representação fica **confinada a poucos procedimentos de interface**, trocar a representação só obriga a reescrever esses poucos. É o `Line Storage` de Parnas, agora com vocabulário de construtor/seletor.

O diagrama abaixo desenha as barreiras como o próprio SICP as desenha: camadas empilhadas, cada uma vendo apenas a interface da camada imediatamente abaixo, nunca a implementação de duas camadas abaixo.

```mermaid
flowchart TB
    U["Programa que usa números racionais\nsoma_rac, imprime_rac"]
    B1{{"— barreira: só usa numerador / denominador / fazer_racional —"}}
    S["Operações racionais (interface)\nnumerador(r) · denominador(r) · fazer_racional(n,d)"]
    B2{{"— barreira: só usa par / primeiro / segundo —"}}
    P["Representação como par\nrepresentar r como (n . d)"]
    B3{{"— barreira: só usa cons / car / cdr —"}}
    H["Pares primitivos da linguagem\ncons · car · cdr"]
    U --> B1 --> S --> B2 --> P --> B3 --> H
    style B1 fill:#3b2f1e,stroke:#b8860b,color:#f5deb3
    style B2 fill:#3b2f1e,stroke:#b8860b,color:#f5deb3
    style B3 fill:#3b2f1e,stroke:#b8860b,color:#f5deb3
    style S fill:#1e2a3b,stroke:#4682b4,color:#d6e4f0
    style P fill:#1e3b2a,stroke:#2e8b57,color:#d6f0e4
```

*Leitura do diagrama:* cada faixa âmbar é uma **barreira** — uma linha que só deixa passar a interface, nunca a implementação. Quem soma racionais (topo) chama `numerador`/`denominador` e legitimamente ignora que `r` é um par; quem implementa o par (meio) chama `cons`/`car` e ignora como a linguagem guarda pares (base). Trocar qualquer camada por outra equivalente não atravessa as barreiras vizinhas — é a torre de Dijkstra com as fronteiras explicitamente marcadas.

> [!tip] Por que SICP importa aqui
> A grande sacada do SICP é mostrar que **a barreira é o mesmo objeto em qualquer escala**: serve para um número racional de três linhas e para uma camada inteira de aplicação. Não há diferença de natureza entre "esconder que o racional é um par" e "esconder que o repositório é Postgres" — só de tamanho. Por isso abstração é a ferramenta *central*: é o único mecanismo que se aplica idêntico do menor dado ao maior subsistema.

## Abstração nos diferentes paradigmas: cada um esconde um tipo de detalhe

Até aqui a abstração apareceu como "esconder uma decisão". Mas *que tipo* de detalhe se esconde varia conforme o paradigma — e ver os três lado a lado mostra que abstração não é um truque de orientação a objetos: é uma ideia que cada estilo de linguagem ataca por um ângulo.

São três formas complementares, cada uma escondendo uma coisa diferente:

**1. Abstração de dados (ADT) — esconde a *representação*.**

É a linha de Parnas e Liskov (logo abaixo) e a barreira do SICP: você esconde *como o dado é guardado* atrás de operações nomeadas. O cliente vê `empilhar`/`desempilhar`, não o array por baixo. O detalhe oculto é a **estrutura interna**.

**2. Abstração funcional — esconde a *ação*, tratando comportamento como dado.**

No paradigma funcional, funções são valores de primeira classe: dá pra passá-las como argumento e devolvê-las como resultado.

Uma **função de ordem superior** (*higher-order function*) abstrai um *padrão de computação*. `map(f, lista)` esconde o laço; o que varia (a operação `f`) vira parâmetro. O SICP chama isso de tratar "programas como blocos de construção" — você compõe comportamento como quem encaixa peças.

```text
# o laço é o detalhe escondido; 'f' é o que muda
map(f, lista):  para cada x em lista, colete f(x)

map(dobro,    [1,2,3]) → [2,4,6]
map(maiuscula,["a","b"]) → ["A","B"]
```

O detalhe oculto aqui não é a representação do dado — é o **mecanismo de iteração/controle**.

**3. Abstração de tipos (parametrização) — esconde a *identidade do tipo*.**

É a "abstração por parametrização" que Liskov nomeia. Com **genéricos / polimorfismo paramétrico**, um único texto de código vale para uma família inteira de tipos.

```text
# uma definição, infinitos tipos
Lista<T>  vale para  Lista<int>, Lista<String>, Lista<Pedido>...
```

O detalhe oculto é *qual* tipo concreto está em jogo: o código de `Lista` não sabe nem precisa saber se guarda inteiros ou pedidos.

> [!note] Um só conceito, três alvos
> Repare no padrão: os três escondem coisas diferentes — a **representação** (ADT), o **fluxo de controle** (funcional), a **identidade do tipo** (genéricos) — mas todos obedecem à mesma regra de Ousterhout: *suprimir o detalhe irrelevante pra amplificar o que importa*. Quando você ouve "abstração" numa entrevista de linguagem funcional e acha que é outra coisa que a abstração de OO, é a mesma ideia trocando de alvo. Saber nomear os três alvos é sinal de quem entende abstração como conceito, não como sintaxe de uma linguagem.

## Abstração por especificação: o que, não o como (Liskov)

Parnas diz *o que* esconder (a decisão volátil).

**Barbara Liskov** — criadora dos tipos abstratos de dados (ADTs) na linguagem **CLU**, no clássico *Programming with Abstract Data Types* (Liskov & Zilles, 1974) — formaliza *como* se descreve uma abstração sem revelar seu interior.

Ela nomeia dois mecanismos complementares:

- **Abstração por parametrização.** Você abstrai da *identidade* dos dados trocando-os por parâmetros. Um único texto de programa passa a representar um conjunto potencialmente infinito de computações. É o que faz `max(a, b)` valer pra quaisquer dois números, não só pra dois específicos.
- **Abstração por especificação.** Você abstrai dos *detalhes de implementação* (o **como**) para o **comportamento** em que o usuário pode confiar (o **quê**). A especificação isola os módulos uns dos outros: exige-se apenas que a implementação sustente o comportamento prometido — qualquer implementação que cumpra o contrato serve.

> [!abstract] A grande virada: protótipo da inversão de dependência
> A abstração por especificação inverte a relação natural. Sem ela, o cliente depende do **código** do módulo (e quebra quando o código muda). Com ela, o cliente depende da **especificação** — uma promessa textual — e fica livre da implementação. É a semente daquilo que décadas depois viraria o "D" do SOLID: dependa de abstrações, não de concretudes. Liskov estava dizendo isso, com outras palavras, em 1974.

Por que isso importa pra você na prática?

Porque te dá o critério do que escrever na assinatura/docstring de um método: a especificação deve dizer **o que o método garante**, nunca **como ele faz**.

No instante em que a doc menciona "usa um HashMap interno", o segredo vazou pra interface — e a abstração já começou frágil.

Veja a diferença numa especificação de `Conjunto`. A versão à esquerda vaza a implementação; a da direita promete só comportamento:

```text
# RUIM — a doc revela o como (o segredo vazou pra interface)
inserir(x):  "adiciona x ao HashMap interno; rehash se load factor > 0.75"

# BOM — a doc promete só o quê (qualquer implementação serve)
inserir(x):  "após a chamada, contém(x) é verdadeiro;
              elementos já presentes não são duplicados.
              Não diz se por baixo é hash, árvore ou bitset."
```

Qualquer estrutura que cumpra a segunda promessa — hash, árvore balanceada, bitset — pode trocar a anterior sem nenhum cliente perceber. Essa liberdade *é* a abstração por especificação.

## A boa abstração é o que torna o código testável

Há uma consequência da abstração por especificação que vale uma seção própria, porque é onde a teoria toca o teclado todo dia: **uma boa abstração é exatamente o que torna o código testável.**

A ponte é o conceito de **seam** (costura), de **Michael Feathers**, em *Working Effectively with Legacy Code* (2004).

> [!quote] Definição de seam (Feathers)
> Um *seam* é *"a place where you can alter behavior in your program without editing in that place"* — um lugar onde você troca o comportamento sem editar o código ali mesmo.

O exemplo canônico de seam é uma **interface**.

Se a classe que envia e-mail depende de uma interface `EmailSender` (não da classe concreta que fala com o SMTP), você consegue, **no teste**, injetar um `EmailSender` falso que só registra "foi chamado" — sem subir servidor de e-mail nenhum.

A interface é o ponto onde o comportamento é trocado sem editar a classe sob teste. É um seam.

Repare na cadeia que se forma:

1. Você abstrai por especificação (depende de um *contrato*, não de um *código*) — Liskov.
2. Essa especificação vira uma interface no código.
3. A interface é um seam — um ponto de troca.
4. O seam é o que deixa você substituir a implementação real por um *test double* (mock/fake/stub).
5. Logo: **código sem boas abstrações é código difícil de testar**, porque não há onde enfiar a costura.

> [!abstract] Abstração ⇒ testabilidade ⇒ inversão de dependência
> Esse é o mesmo eixo que a [[Orientação a Objetos|orientação a objetos]] chama de **inversão de dependência** (o "D" do SOLID): o código de alto nível depende de uma abstração, não da implementação concreta; o concreto é plugado de fora. Testabilidade é o sintoma observável de que a inversão foi feita direito. Quando alguém diz "esse código é impossível de testar sem subir o banco inteiro", está descrevendo, sem saber, uma **falta de abstração** — não há seam entre a regra de negócio e a infraestrutura.

> [!tip] O teste como termômetro da abstração
> Há um truque prático escondido aqui: a *dificuldade de escrever um teste unitário* é um termômetro honesto da qualidade das suas abstrações. Se pra testar uma função você precisa de mock de dez coisas, rede, relógio e sistema de arquivos, a função está acoplada a dez detalhes concretos que deveriam estar atrás de seams. O teste difícil não é o problema — é o **alarme** de uma abstração ausente. É por isso que TDD frequentemente "melhora o design": ele força você a criar os seams *antes*, não depois.

## Boas vs. más abstrações

Junte as duas ideias — visão simplificada (Ousterhout) + esconder a decisão volátil (Parnas) — e o critério de qualidade cai sozinho:

- **Boa abstração:** esconde os detalhes **certos** (o volátil, o irrelevante) atrás de uma interface **pequena e estável**. Ela mantém sua promessa: você usa a interface e legitimamente esquece o resto. Os melhores módulos, em Ousterhout, são **profundos** — muita funcionalidade atrás de uma interface enxuta (assunto da [[07 - Módulos profundos e rasos]]).
- **Má abstração (errada):** ou **esconde o que você precisa** (te força a contornar a interface, abrir a caixa, depender de detalhe interno), ou **vaza o que escondeu** (a decisão interna reaparece no comportamento observável). A interface grande relativa ao que entrega é o sintoma do módulo raso; o vazamento é o tema da nota vizinha.

> [!warning] Toda abstração é uma aposta
> Você aposta em *qual* decisão é volátil e *qual* é estável — e esconde a primeira atrás da segunda. Acertar a aposta é o que separa a abstração que envelhece bem da que vira pedágio. Quando a aposta erra (você expôs o que devia esconder, ou escondeu o que devia expor), a abstração trabalha contra você. E mesmo a melhor abstração não esconde *tudo* o tempo todo — onde e por que ela falha é o assunto inteiro de [[06 - Abstrações que vazam]].

Esta nota é a afirmação **positiva**: o que abstração é e por que ela é a ferramenta central.

As duas notas seguintes a tensionam pelos limites — onde abstrações **vazam** ([[06 - Abstrações que vazam]]) e como **dimensionar** um módulo pra que a abstração seja profunda, não rasa ([[07 - Módulos profundos e rasos]]).

## O custo do excesso: abstração demais também é dívida

Há um espelho do problema da má abstração que precisa de nome próprio: a **abstração em excesso** (*over-abstraction*).

A má abstração esconde a coisa errada. A abstração em excesso esconde **coisas que não precisavam ser escondidas** — generalidade construída para problemas que ninguém tem.

O retrato mais célebre disso é de **Joel Spolsky**, no ensaio *Don't Let Architecture Astronauts Scare You* (2001). O **arquiteto astronauta** é o engenheiro que sobe tanto no nível de abstração que perde o contato com qualquer problema concreto.

> [!quote] Joel Spolsky sobre os astronautas
> *"When you go too far up, abstraction-wise, you run out of oxygen."* — o arquiteto astronauta não resolve um problema real; ele resolve algo que *parece* ser o template de muitos problemas, e acaba com "imagens absurdas, abrangentes e de altíssimo nível do universo que não significam nada".

O sintoma clínico do excesso é uma abstração que **não tem cliente real hoje** — só clientes hipotéticos, "um dia podemos precisar".

A indústria tem até um troféu de meme para isso: a classe `AbstractSingletonProxyFactoryBean`, do Spring. O nome empilha quatro conceitos (`Abstract` + `Singleton` + `Proxy` + `FactoryBean`) e virou piada justamente por encarnar a abstração que se afastou do problema. (Detalhe que fecha a piada: a classe acabou *depreciada* — havia um só uso real, que também morreu.)

Dois princípios consagrados são o antídoto direto:

- **YAGNI** (*You Aren't Gonna Need It*), da Programação Extrema (Kent Beck, Ron Jeffries): não construa a capacidade até precisar dela de fato. Generalidade especulativa é dívida paga adiantado por um juro que talvez nunca venha.
- **Premature abstraction** (abstração prematura): criar a interface antes de ter casos reais suficientes para saber qual é, de fato, o eixo de variação. É a irmã da "otimização prematura" de Knuth — e prima direta da abstração *errada* de Metz, logo abaixo.

> [!warning] O excesso e o erro são parentes, não gêmeos
> Não confunda os dois. A **abstração errada** (Metz) é uma abstração que *existe e tem clientes*, mas uniu coisas que mudam por razões diferentes. A **abstração em excesso** (Spolsky/YAGNI) é uma abstração que talvez nem precise existir — generalidade sem caso de uso. O remédio compartilhado é o mesmo de sempre: **espere a evidência**. A abstração é uma aposta sobre o futuro; abstrair cedo demais é apostar antes de ver as cartas.

## A abstração errada: quando a cura é pior que a doença

Até aqui a abstração foi heroína. Hora do contraponto sênior — o que separa quem leu sobre abstração de quem já se queimou com ela.

A tese é de **Sandi Metz**, no ensaio curto e devastador *The Wrong Abstraction* (2016):

> [!quote] Sandi Metz
> *"Duplication is far cheaper than the wrong abstraction"* — e, portanto: *"prefer duplication over the wrong abstraction."*

Como uma abstração nasce errada? Metz desenha o filme em câmera lenta, e ele é tão comum que dói reconhecer:

1. Programador A vê dois trechos duplicados, **extrai** o comum num método/classe, dá um nome, troca os dois usos pela abstração nova. Limpo. Elogiável. DRY.
2. Passa o tempo. Surge um requisito **quase** igual, mas não idêntico.
3. Programador B (que pode ser você seis meses depois) **se sente obrigado** a reusar a abstração que já existe. Em vez de questioná-la, adiciona um **parâmetro** e um **`if`** pra cobrir o caso novo.
4. Mais um requisito, mais um parâmetro, mais um branch. Repita.
5. O resultado: um método que mistura ideias que não têm nada a ver, recheado de flags e condicionais, ilegível. *"Embora cada chamador ostensivamente invoque uma abstração compartilhada, o código que eles de fato rodam é praticamente único."*
6. Ninguém ousa mexer, porque "já investimos tanto nisso". É a **falácia do custo afundado** (*sunk cost*) operando como força de design.

> [!warning] Por que a abstração errada custa mais que a duplicação
> A duplicação tem um custo **honesto e visível**: mudou a regra, você altera em N lugares. Chato, mas linear e óbvio. A abstração errada tem um custo **escondido e composto**: cada novo requisito te força a *torcer* uma estrutura que não foi feita pra ele, e cada torção dificulta a próxima. A duplicação você vê; a abstração errada você só sente — tarde demais, quando o módulo já virou um nó de condicionais.

O conselho de Metz é contraintuitivo e libertador: **"the fastest way forward is back"** (o caminho mais rápido pra frente é pra trás).

Diante de uma abstração errada já instalada, o roteiro é desfazer antes de refazer:

1. **Re-inline:** copie o código da abstração de volta pra dentro de cada chamador.
2. Em cada cópia, **apague o que aquele chamador não usa** (graças às flags, dá pra saber exatamente o quê).
3. Remova os parâmetros e condicionais que só existiam pra servir vários donos.
4. Agora, com o entendimento que você não tinha no dia 1, **re-extraia** a abstração certa — se ela ainda fizer sentido.

> [!tip] A regra de três: não abstraia cedo demais
> Como evitar criar a abstração errada? Espere ela aparecer. A **regra de três** ("*three strikes and you refactor*"), popularizada por **Martin Fowler** no *Refactoring* e atribuída a **Don Roberts**: a primeira vez você só escreve; na segunda ocorrência duplicada, você range os dentes e **duplica mesmo assim**; só na **terceira** você extrai a abstração. Duas ocorrências dão informação insuficiente sobre o que é, de fato, comum entre elas — abstrair no segundo caso é apostar com pouca evidência. Na terceira, o padrão real já se revelou.

O fio que une Metz, Fowler e Parnas é um só: **a abstração é uma aposta sobre o que vai mudar junto**, e você joga melhor com mais informação.

Abstrair cedo é apostar no escuro. A duplicação temporária é o preço de esperar a luz acender.

```mermaid
flowchart TD
    A[Vejo código duplicado] --> B{Quantas ocorrências?}
    B -->|1ª ou 2ª| C[Duplique de propósito\nespere mais evidência]
    B -->|3ª| D{Elas mudam pela\nMESMA razão?}
    D -->|Não, são parecidas\npor coincidência| C
    D -->|Sim, compartilham\num segredo real| E[Extraia a abstração]
    E --> F{Surge requisito quase-igual?}
    F -->|Encaixa limpo| G[Ótimo: era a abstração certa]
    F -->|Só com flag + if| H[ALERTA: abstração errada]
    H --> I[Re-inline em cada chamador\napague o que sobra\nre-extraia se fizer sentido]
    style C fill:#1e2a3b,stroke:#4682b4,color:#d6e4f0
    style E fill:#1e3b2a,stroke:#2e8b57,color:#d6f0e4
    style H fill:#3b1e1e,stroke:#c0392b,color:#f0d6d6
    style I fill:#3b2f1e,stroke:#b8860b,color:#f5deb3
```

*Leitura do diagrama:* o caminho seguro hesita (duplica) até a terceira ocorrência **e** confirma que os trechos mudam pela mesma razão; quando um requisito novo só entra com flag e `if`, isso é o sinal de abstração errada — e a saída é desfazer (re-inline), não empilhar mais condicionais.

> [!note] DRY não é o oposto disso
> Cuidado pra não ler Metz como "duplicação é boa, DRY é mito". Não é. DRY continua valendo pra **conhecimento** genuinamente único (uma regra de negócio que só pode ter uma fonte da verdade). O alvo de Metz é a **duplicação acidental** — dois trechos que *parecem* iguais hoje mas mudam por razões diferentes. Unificá-los acopla coisas que deveriam viver separadas. A pergunta de ouro não é "esses trechos são parecidos?", e sim "**eles vão mudar sempre juntos, pela mesma razão?**". Só então há um segredo comum pra esconder.

## Armadilhas comuns

> [!warning] O catálogo dos erros de abstração
> - **Abstrair cedo demais.** Criar a interface antes de ter casos reais suficientes — a abstração errada de Metz. Antídoto: regra de três.
> - **Indireção disfarçada de abstração.** A camada *pass-through* que não esconde nada (seção *Abstração ≠ indireção*). Antídoto: "o chamador precisa saber menos depois dela?".
> - **Misturar níveis no mesmo módulo.** Regra de negócio + SQL cru + formatação juntos. Antídoto: uma unidade, um nível de abstração.
> - **O segredo vaza pela interface.** Nomes, tipos ou ordem de chamadas que denunciam a implementação (`getUserFromHashMap`, exigir `connect()` antes de `query()`). Antídoto: especifique o **quê**, nunca o **como** (Liskov).
> - **Astronautas da arquitetura.** Abstrair tão alto que a abstração não resolve mais nenhum problema concreto — generalidade sem caso de uso. Antídoto: toda abstração deve ter clientes reais *hoje*, não hipotéticos.
> - **Sunk cost.** Manter a abstração errada porque "já investimos". Antídoto: *the fastest way forward is back*.

## Em entrevista

> [!tip] Como sinalizar senioridade
> Quase todo mundo diz "abstração esconde complexidade". O sinal de senioridade é citar o **custo** da abstração errada. Se perguntarem "quando você cria uma abstração?", a resposta forte não é "sempre que vejo duplicação" — é: *"espero a terceira ocorrência e confirmo que os trechos mudam pela mesma razão; duplicação acidental que eu unifico cedo vira a abstração errada, que custa mais caro que a própria duplicação (Metz)."* E ao desenhar um módulo, nomeie **o segredo** que ele esconde (Parnas): se você não consegue nomear a decisão volátil protegida, não há abstração ali — só código agrupado por acaso.

## Referências

- **David Parnas** — [On the Criteria To Be Used in Decomposing Systems into Modules](https://dl.acm.org/doi/10.1145/361598.361623) (CACM 15(12), 1972, p. 1053-1058). Origem do *information hiding*: o critério de decomposição é esconder **decisões de design propensas a mudar**, não dados nem etapas de fluxograma. Título, veículo e ano conferidos via ACM Digital Library e dblp.
- **John Ousterhout** — *A Philosophy of Software Design* (1ª ed. 2018; 2ª ed. 2021, Yaknyam Press). Origem da definição de abstração (*"a simplified view of an entity, which omits unimportant details"*) e da distinção módulo **profundo** vs. **raso** / método *pass-through* (indireção que não abstrai).
- **Edsger W. Dijkstra** — *EWD 356 — notas do Advanced Course on Computer Systems Architecture* (Grenoble, dez. 1972). Origem da frase *"The purpose of abstraction is not to be vague, but to create a new semantic level in which one can be absolutely precise."* Atribuição e veículo (EWD 356, dez. 1972) conferidos via E.W. Dijkstra Archive (UT Austin).
- **Barbara Liskov & Stephen N. Zilles** — *Programming with Abstract Data Types* (ACM SIGPLAN Notices 9(4), 1974, p. 50-59). Origem dos tipos abstratos de dados (ADTs) e da linguagem CLU. Os termos *abstração por parametrização* e *abstração por especificação* (o **quê** vs. o **como**) são consolidados por Liskov & Guttag em *Program Development in Java: Abstraction, Specification, and Object-Oriented Design* (2000).
- **Harold Abelson & Gerald Jay Sussman** — *Structure and Interpretation of Computer Programs* (SICP), 2ª ed. (MIT Press, 1996; 1ª ed. 1985), seção 2.1.2, *Abstraction Barriers*. Origem do conceito de **barreira de abstração** (linhas que isolam níveis; *"procedures at each level are the interfaces that define the abstraction barriers"*), do par **construtores/seletores** e do argumento de que confinar a dependência da representação a poucos procedimentos de interface é o que mantém a flexibilidade de trocar a implementação. Citações conferidas contra o texto integral do SICP (mitpress / sicp.sourceacademy.org).
- **Michael C. Feathers** — *Working Effectively with Legacy Code* (Prentice Hall, 2004). Origem do conceito de **seam** (*"a place where you can alter behavior in your program without editing in that place"*): a interface como ponto de troca que torna o código testável (injetar *test doubles* sem editar a classe sob teste). Conexão com inversão de dependência (o "D" do SOLID) é leitura minha unindo Feathers e Liskov.
- **Joel Spolsky** — [Don't Let Architecture Astronauts Scare You](https://www.joelonsoftware.com/2001/04/21/dont-let-architecture-astronauts-scare-you/) (2001). Origem do **arquiteto astronauta** e da frase *"when you go too far up, abstraction-wise, you run out of oxygen"* — o retrato da abstração que sobe alto demais e perde o problema concreto. O caso `AbstractSingletonProxyFactoryBean` (Spring AOP), de fato depreciado, é exemplo notório da comunidade (docs do Spring + discussão no Hacker News), usado aqui como meme ilustrativo.
- **YAGNI / abstração prematura** — *You Aren't Gonna Need It*, princípio da Programação Extrema (Kent Beck, Ron Jeffries, Ward Cunningham): não construa capacidade antes da necessidade real. "Abstração prematura" é a aplicação à abstração do alerta de Knuth contra a otimização prematura. Conferido contra a literatura corrente de YAGNI / *rule of three*.
- **Sandi Metz** — [The Wrong Abstraction](https://sandimetz.com/blog/2016/1/20/the-wrong-abstraction) (2016). Origem de *"duplication is far cheaper than the wrong abstraction"*, da narrativa Programador A/B, da armadilha do *sunk cost* e do remédio *"the fastest way forward is back"* (re-inline). Texto integral conferido na fonte primária.
- **Martin Fowler & Don Roberts** — *Refactoring: Improving the Design of Existing Code*. Origem da **regra de três** ("*three strikes and you refactor*"); Fowler a atribui a Don Roberts. Conferido contra resumos e a verbete da Wikipedia *Rule of three (computer programming)*.

> [!note] Sobre o lastro
> Atribuições conferidas a fontes primárias ou de alta confiança nesta pesquisa: a frase de **Dijkstra** (EWD 356, dez. 1972) bate com o E.W. Dijkstra Archive; o ensaio de **Metz** foi lido na fonte primária (sandimetz.com), incluindo a frase, a narrativa A/B e o remédio do re-inline; os dados de **Liskov & Zilles** (SIGPLAN Notices 9(4), 1974) e de **Parnas** (CACM 15(12), 1972) batem com ACM/dblp; a **regra de três** confere com o *Refactoring* de Fowler (atribuição a Don Roberts). O exemplo **KWIC** (duas decomposições; módulo `Line Storage` escondendo o layout dos caracteres) é fiel ao paper de Parnas conforme fontes secundárias confiáveis (CMU 15-413, sunnyday.mit.edu).
>
> Conferidos na segunda passada: as duas citações do **SICP** sobre *abstraction barriers* (interfaces que definem as barreiras; confinar a dependência da representação a poucos procedimentos) batem com o texto integral do SICP online (seção 2.1.2). A definição de **seam** de **Feathers** (*"a place where you can alter behavior… without editing in that place"*) confere com resumos e trechos da fonte. A frase de **Spolsky** (*"run out of oxygen"*) confere com o ensaio original em joelonsoftware.com; o status *depreciado* de `AbstractSingletonProxyFactoryBean` confere com a Javadoc do Spring.
>
> **Ressalva honesta:** não li o texto integral de Parnas, Dijkstra (EWD 356 completo), Liskov & Zilles, Ousterhout, SICP e Feathers página a página. As paráfrases (o saldo *pass-through* de Ousterhout; a redação dos dois mecanismos de Liskov; os passos exatos do KWIC; o exemplo racional/par do SICP; a cadeia seam⇒testabilidade⇒inversão de dependência) são fiéis ao argumento mas podem diferir em palavras da redação literal. Os **pseudo-códigos** em blocos `text` são ilustrativos meus — fiéis ao espírito das fontes, não transcrições. A conexão seam→inversão de dependência (SOLID) e o "termômetro do teste" são minha leitura unindo Feathers, Liskov e a prática de TDD. O padrão de marcação de incerteza segue o da nota vizinha [[06 - Abstrações que vazam]].

## Veja também

- [[06 - Abstrações que vazam]] — os limites: onde e por que mesmo boas abstrações vazam
- [[07 - Módulos profundos e rasos]] — como dimensionar um módulo pra que a abstração seja profunda
- [[01 - A complexidade como problema central]] — o problema que a abstração existe pra combater
- [[Orientação a Objetos]] — encapsulamento, o mecanismo de linguagem que implementa information hiding
- [[Dicionário de Ciência da Computação#Abstração errada (the wrong abstraction)]] — o verbete do contraponto sênior
- [[Dicionário de Ciência da Computação]] — verbetes do domínio
