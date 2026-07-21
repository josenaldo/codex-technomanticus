---
title: "A escada de abstração — qual é a unidade de design"
created: 2026-07-20
updated: 2026-07-20
type: concept
status: seedling
fase: Iniciado
publish: true
tags:
  - evolucao-engenharia-ia
  - ia
aliases:
  - Unidade de design em engenharia de IA
  - Escada de abstração da IA
  - Prompt vs flow vs context vs loop vs graph engineering
---

# A escada de abstração — qual é a unidade de design

> [!abstract] TL;DR
> Entre 2022 e 2026, seis camadas de engenharia em torno de LLMs foram anunciadas, cada uma dizendo que a anterior "morreu": prompt, flow, context, harness, loop, graph. Nenhuma matou a anterior — cada uma **encapsulou** a de baixo, do mesmo jeito que módulo encapsula função e serviço encapsula módulo. O critério que separa uma camada real de um rebranding é **qual é a unidade de design**: a menor coisa que você projeta, versiona e depura de propósito. Frase → fluxo → janela → ambiente → ciclo → rede. Este galho é a historiografia desse capítulo — não profecia. O valor está no critério, não na lista, porque a lista vai mudar.

---

## O feed que não para

Você abre o Twitter numa terça de manhã e lê: "prompt engineering morreu." Rola o feed, dois meses depois: "context engineering está sendo substituído." Mais um scroll, mais um post: "loop engineering é o novo paradigma — esqueça tudo que você aprendeu sobre agentes." E então, na semana seguinte: "ninguém mais fala de loops, agora é graph engineering."

Se você é um desenvolvedor sênior tentando se manter relevante, esse ciclo de 18 meses é exaustivo de um jeito específico. Não é que você não confie na tecnologia — é que você não confia no *vocabulário*.

Cada anúncio de "morte" de uma disciplina vem com a mesma estrutura retórica: um post viral, uma citação de alguém influente, um framework novo com estrela crescendo no GitHub. E seis meses depois, metade dessas mortes anunciadas evapora, e a outra metade vira, de fato, a forma como o trabalho é feito.

O problema não é falta de informação — é excesso dela, sem filtro. Você precisa de um critério que separe sinal de ruído *antes* de gastar duas semanas aprendendo um framework que vai ser irrelevante no trimestre seguinte. E esse critério não pode ser "quem postou" ou "quantos likes teve", porque isso é exatamente o mecanismo que produz o ruído.

> [!question]- E se for tudo hype, e nada disso for real?
> Parte é. Mas nem tudo. A prova de que existe sinal real nesse barulho é que você consegue *testar* cada camada contra uma pergunta técnica precisa — "o que exatamente esse nome novo deixa você fazer que o nome antigo não deixava?" — e em pelo menos algumas das seis camadas deste galho a resposta é concreta, mensurável, com paper ou produto por trás. Nas outras, a resposta é "nada, é o mesmo conceito com etiqueta nova" — e isso também é uma informação útil.

---

## O critério: qual é a unidade de design

Aqui está o teste que este galho propõe, e que você pode aplicar a qualquer "nova disciplina de engenharia de IA" que aparecer depois que esta nota for escrita: **pergunte qual é a unidade de design** — a menor coisa que a disciplina te ensina a projetar, versionar e depurar de propósito.

Não "o que ela promete". Não "quem a defende". A unidade de design é o objeto concreto que, quando você erra, você conserta *nele* — não um nível acima, não um nível abaixo.

- Em **prompt engineering**, a unidade é a **frase** — o texto que você manda para o modelo numa chamada.
- Em **flow engineering**, é o **fluxo multi-etapa** — uma sequência de passos com teste embutido, onde cada etapa reage ao resultado da anterior.
- Em **context engineering**, é a **janela inteira** — tudo que está carregado na memória de trabalho do modelo num dado instante: system prompt, histórico, documentos recuperados, definições de ferramentas.
- Em **harness engineering**, é o **ambiente executável** — o conjunto de ferramentas, permissões, sandboxes e regras que cercam o agente e determinam o que ele *pode* fazer, não só o que ele sabe.
- Em **loop engineering**, é o **ciclo que se repete** — a máquina que roda a mesma sequência de ações até um critério de parada, ajustando o que muda a cada volta.
- Em **graph engineering**, é a **rede de ciclos** — vários loops conectados, cada um vigiando ou corrigindo o outro, onde a confiabilidade do sistema não está em nenhum nó isolado.

Repare no padrão: cada unidade é estritamente maior que a anterior, e cada uma *contém* a anterior dentro de si. Um fluxo é feito de chamadas com prompts. Uma janela de contexto carrega o prompt e o histórico do fluxo. Um ambiente executável é onde a janela de contexto vive e se atualiza. Um loop é o ambiente rodando repetidamente. Uma rede é vários loops conversando entre si.

Isso importa porque é um padrão testável, não uma opinião estética sobre nomenclatura. Você pode pegar qualquer sistema real, apontar para ele, e verificar se a camada que ele reivindica de fato contém a anterior — ou se é só um nome novo colado sobre a mesma coisa.

Isso não é coincidência — é a assinatura de uma escada de abstração genuína, não de um rebranding. Rebranding troca o nome e mantém a unidade. Escada de abstração muda a unidade e, ao fazer isso, revela um problema que a camada anterior não conseguia nem enxergar, porque estava trabalhando numa escala pequena demais para vê-lo.

---

## A linha do tempo

A tabela abaixo consolida quando cada camada apareceu, com que unidade de design, e quem a articulou primeiro (ou primeiro de forma influente — a autoria em código aberto raramente tem um único inventor claro).

| Camada | Unidade de design | Quando | Autoria / marco |
|---|---|---|---|
| **Prompt engineering** | O input único | 2022–2024 | Difuso; formalizado por técnicas como chain-of-thought (CoT), few-shot prompting, tree-of-thought (ToT) |
| **Flow engineering** | O fluxo multi-etapa test-driven | jan/2024 | AlphaCodium (Codium AI, hoje Qodo), paper arXiv 2401.08500 |
| **Context engineering** | A janela inteira | 2025 | Andrej Karpathy ("LLM = CPU, contexto = RAM, você = SO", jun/2025); Tobi Lütke (Shopify); survey arXiv 2507.13334 |
| **Harness engineering** | O ambiente executável | 2026 | Mitchell Hashimoto (criador do Terraform) |
| **Loop engineering** | O ciclo que repete | jun/2026 | Addy Osmani + Peter Steinberger (@steipete), comentando fala de Boris Cherny |
| **Graph engineering** | A rede de loops | jul/2026 | Steipete (18/jul/2026); Santiago Valdarrama (@svpino) |

Quatro anos, seis nomes. À primeira vista, isso parece confirmar exatamente o medo do desenvolvedor que abriu o Twitter na primeira seção: um carrossel de hype sem substância. Mas olhe a coluna "unidade de design" de novo. Ela não repete o mesmo conceito seis vezes com roupagem diferente — ela sobe uma escada, um degrau de escopo por vez. Isso é a diferença entre moda e disciplina.

### O que cada camada resolveu que a anterior não conseguia

A tabela mostra *quando* e *quem*. Vale gastar um parágrafo em cada camada explicando *o quê* — o problema específico que ela resolveu e que a de baixo, por construção, não conseguia enxergar.

**Prompt engineering** resolveu o problema de "o modelo entendeu errado o que eu pedi" — técnicas como chain-of-thought e few-shot mostraram que *como* você formula uma instrução muda drasticamente a qualidade da resposta, mesmo mantendo o modelo idêntico. O limite dela: uma frase, por melhor escrita, não consegue se auto-corrigir. Se a resposta sair errada, você só descobre lendo — não há verificação embutida.

**Flow engineering** resolveu exatamente esse limite: em vez de confiar numa única resposta, o AlphaCodium gerava candidatos, rodava testes contra eles, e usava o resultado do teste para gerar a próxima tentativa. O ganho não veio de um prompt melhor — veio de dar ao processo uma forma de saber, objetivamente, quando errou. O limite dela: um fluxo bem desenhado ainda assume que tudo que ele precisa saber cabe no que foi passado explicitamente a cada chamada. Ele não tem um conceito de "memória" ou "ambiente" — cada chamada é relativamente isolada.

**Context engineering** resolveu esse limite tratando a janela inteira — histórico, documentos recuperados, instruções persistentes — como um recurso a ser gerenciado ativamente, não como um acúmulo passivo do que aconteceu. O ganho: agentes que operam em sessões longas sem "esquecer" o que já fizeram. O limite dela: gerenciar bem o que o modelo *sabe* não resolve o que o modelo *pode fazer*. Um agente com contexto perfeito ainda pode não ter permissão de executar um comando, não ter acesso a uma ferramenta, ou rodar num ambiente sem as dependências certas.

**Harness engineering** resolveu esse limite tratando o ambiente executável — ferramentas, permissões, sandboxes — como artefato de design deliberado. O ganho, na formulação de Hashimoto: cada erro do agente vira uma correção no ambiente, não só uma instrução adicional no prompt — "toda vez que você descobre que um agente errou, você engenheira uma solução que impede a recorrência", incorporada ao harness, não a um parágrafo de instrução que pode ser ignorado na próxima sessão. O limite dela: um ambiente bem desenhado ainda roda uma vez. Ele não decide sozinho *quando parar de tentar* ou *como ajustar a abordagem* se a primeira tentativa não bastar.

**Loop engineering** resolveu esse limite formalizando o ciclo de repetição — quando tentar de novo, o que muda entre tentativas, e qual é o critério de parada — como o próprio objeto de design. O ganho: sistemas que se auto-corrigem ao longo de múltiplas voltas, não só numa execução isolada. O limite dela, detalhado inteiro na nota 05: um loop otimiza a métrica que você deu a ele, e nada nele sabe dizer se essa métrica ainda é a certa.

**Graph engineering** resolveu esse último limite conectando loops entre si — um vigiando o outro, um definindo o alvo do outro, um arbitrando entre dois objetivos que competem. O ganho: a possibilidade de um sistema detectar que sua própria métrica está sendo enganada, algo que nenhum loop isolado consegue fazer sozinho, porque ele só enxerga a si mesmo. O limite dela — e é este que fecha o galho, na nota 07 — é que uma rede de loops "consistente e mútua" ainda pode estar inteiramente desconectada da realidade que diz estar melhorando. Grafo resolve o problema de loops se enganando entre si; não resolve, por si só, o problema de todos eles se enganarem *juntos*.

Vale destacar um detalhe que desmonta a narrativa de "loop engineering é 2026": a ideia central de "gerar, testar, corrigir, repetir" já estava inteira no AlphaCodium, de janeiro de 2024 — dois anos e meio antes do termo "loop engineering" pegar. A linhagem completa é: ReAct (2022, o padrão raciocínio-ação-observação) → AutoGPT (2023, primeira tentativa popular de agente totalmente autônomo) → o "Ralph Wiggum" de Geoffrey Huntley (jul/2025, um loop de bash brutal e honesto que repete o mesmo prompt até bater o objetivo) → o comando `/goal` do Codex (abr/2026) → suporte nativo a esse padrão em Hermes e Claude Code (mai/2026) → o nome "loop engineering" pego pela mídia técnica (jun/2026). O mecanismo é velho. O nome, o tooling e a escala de adoção são novos.

---

## Dois sinais de que isso não é só retórica

Duas evidências, independentes uma da outra, sugerem que a escada desta nota descreve algo estrutural — não apenas uma sequência de posts virais competindo por atenção.

**O primeiro é Andrew Ng, em 30 de junho de 2026**, descrevendo agentes de produção como operando em **três timescales de loop aninhados simultaneamente**: o loop agêntico (o agente decidindo o próximo passo, em segundos), o loop de desenvolvedor (o time ajustando prompts e ferramentas com base em falhas observadas, em horas ou dias) e o loop de usuário (o produto inteiro sendo refinado com base em feedback de uso real, em semanas ou meses). Repare que essa descrição não é uma disciplina nova disputando espaço na tabela — é a confirmação, vinda de um pesquisador com décadas de trabalho em ML antes do hype de LLM, de que a estrutura de "loops dentro de loops" já é como sistemas de produção sérios são pensados, independentemente do nome que a comunidade dá a isso num tuíte.

**O segundo é o descompasso entre título de vaga e skill exigida.** Entre 2024 e 2026, o título "Prompt Engineer" como cargo formal caiu cerca de 30% nas plataformas de vaga — a leitura ingênua seria "prompt engineering morreu, confirmado". Mas, no mesmo período, a *skill* "prompt engineering" listada dentro de descrições de vagas no LinkedIn cresceu cerca de 250%, e o número de vagas que exigem essa skill (não como título, como requisito) triplicou. Uma pesquisa de 2026 com líderes de TI e dados mostrou 82% concordando que "prompt sozinho não basta para produção multi-etapa" — o que é, na linguagem desta nota, uma confirmação direta de que a unidade de design subiu de nível: a habilidade não desapareceu, ela deixou de ser suficiente sozinha e virou um componente dentro de algo maior. Isso é encapsulamento medido em dado de mercado, não só em argumento teórico. A nota 08 detalha esses números com mais contexto e as faixas salariais associadas.

> [!question]- Isso não é só sobrevivência do enviesamento de confirmação — eu estou vendo padrão onde só há ruído?
> É um risco real, e vale nomeá-lo em vez de fingir que não existe. A defesa mais honesta possível: o critério da unidade de design foi desenhado *antes* de examinar esses dois sinais — ele vem da analogia com engenharia de software clássica, que é anterior a qualquer uma das seis camadas listadas aqui. Os dois sinais desta seção não foram escolhidos para caber no critério; eles foram testados contra ele depois de formulado. Isso não elimina o risco de viés, mas reduz o risco de que o critério tenha sido construído sob medida para confirmar a lista.

> [!warning] Nem todo mundo concorda que a escada é real
> Vozes críticas argumentam que boa parte disso é DAG de orquestração com nome novo — Airflow já existe desde 2014, Step Functions e workflow engines não são invenção de 2026. A pergunta que separa ceticismo justo de ceticismo preguiçoso é: o que muda quando os nós de um grafo de orquestração são estocásticos (um LLM, que pode alucinar, mudar de opinião, ou interpretar mal), em vez de determinísticos (uma função, que sempre faz a mesma coisa dado o mesmo input)? Essa pergunta específica — e as respostas divergentes que ela recebe — é o assunto central da nota 08.

---

## Cada camada encapsula, não substitui

A confusão mais comum ao ler essa linha do tempo é achar que ela descreve substituições — que graph engineering "aposenta" loop engineering, que loop engineering "aposenta" context engineering, e assim por diante. Isso é falso, e é a segunda peça central deste galho.

O que de fato acontece é **encapsulamento**. Cada camada nova não elimina a anterior — ela a envolve, tratando-a como um componente interno que agora pode ser mais estúpido, porque a camada de fora compensa. Você ainda escreve prompts. Só que agora eles vivem dentro de um fluxo, que vive dentro de uma janela de contexto gerida, que roda dentro de um ambiente com ferramentas e permissões, que é executado repetidamente por um loop, que por sua vez é um nó dentro de uma rede maior de loops.

Se você já trabalha em engenharia de software há mais de alguns anos, essa estrutura deveria soar familiar — porque você já subiu uma escada quase idêntica, num domínio totalmente diferente.

### A analogia: você já viveu essa escada uma vez

Pense na evolução de como organizamos código, décadas antes de LLM existir.

No começo, a unidade era a **função**: um bloco de código que faz uma coisa, recebe entrada, devolve saída. Depois vieram os **módulos**: agrupamentos de funções relacionadas, com uma interface pública e um encapsulamento interno — você para de pensar em cada função isolada e passa a pensar "o que este módulo expõe, o que ele esconde". Depois vieram os **serviços**: módulos que rodam em processos separados, comunicando por rede, com contratos formais (APIs) entre eles — você para de pensar em módulos dentro de um binário e passa a pensar em fronteiras de deploy, versionamento independente, disponibilidade. E depois veio o **sistema distribuído**: uma rede de serviços onde a pergunta deixa de ser "este serviço está correto" e passa a ser "o sistema inteiro se comporta bem sob falha parcial, latência de rede, consistência eventual" — a confiabilidade deixa de morar em qualquer componente individual e passa a morar nas *interações* entre eles.

Ninguém, ao adotar microsserviços, parou de escrever funções. Uma função ainda é a menor unidade executável dentro de um módulo, que ainda é a menor unidade organizacional dentro de um serviço, que ainda é o menor deployável dentro de um sistema distribuído. Cada camada não apagou a de baixo — ela mudou *onde* mora o problema mais difícil. Bugs de função se resolvem com teste unitário. Bugs de módulo se resolvem com design de interface. Bugs de serviço se resolvem com contrato de API e observabilidade. Bugs de sistema distribuído — os piores — se resolvem entendendo topologia, timeout, retry, circuit breaker: eles não estão em nenhum serviço específico, estão nas arestas entre eles.

Function → module → service → distributed system é exatamente a mesma forma de escada que prompt → flow → context → harness → loop → graph. A diferença é que a primeira escada levou umas duas décadas para a indústria subir (dos anos 1970 até os anos 2010), e essa segunda está sendo subida em quatro anos, porque a velocidade de iteração de LLMs comprimiu um ciclo de maturação inteiro. Isso explica boa parte do desconforto do desenvolvedor sênior do início da nota: ele não está confuso porque o conteúdo é estranho — está confuso porque está revivendo, em fast-forward, uma transição que originalmente durou uma carreira inteira.

> [!info] Outra lente para a mesma ideia: a pilha de rede
> Se a analogia de software não fechar para você, a pilha OSI serve igual de bem. Camada física transmite bits; camada de enlace agrupa bits em quadros e lida com endereçamento local; camada de rede roteia pacotes entre redes; camada de transporte garante entrega confiável fim-a-fim; camada de aplicação fala o protocolo que o usuário entende. Nenhuma camada superior "substitui" a inferior — HTTP roda em cima de TCP, que roda em cima de IP, que roda em cima de Ethernet, sempre. Você só deixa de *pensar* na camada de baixo quando a de cima está madura o suficiente para escondê-la de você. É exatamente isso que acontece quando "harness engineering" esconde a complexidade de gerenciar contexto manualmente: o contexto não sumiu, só ficou encapsulado.

---

## O diagrama: camadas concêntricas, não uma linha

Uma linha do tempo plana (A → B → C → D → E → F) sugere substituição sequencial — cada seta parecendo dizer "isso mata aquilo". O diagrama certo para este galho é outro: camadas concêntricas, onde cada anel novo envolve o anterior sem apagá-lo.

```mermaid
flowchart TB
    subgraph G["Graph engineering — a rede de loops (jul/2026)"]
        direction TB
        subgraph L["Loop engineering — o ciclo que repete (jun/2026)"]
            direction TB
            subgraph H["Harness engineering — o ambiente executável (2026)"]
                direction TB
                subgraph C["Context engineering — a janela inteira (2025)"]
                    direction TB
                    subgraph F["Flow engineering — o fluxo multi-etapa (jan/2024)"]
                        direction TB
                        P["Prompt engineering<br/>a frase única (2022-2024)"]
                    end
                end
            end
        end
    end

    style P fill:#4A90D9,color:#fff
    style F fill:#4A90D9,color:#fff
    style C fill:#4A90D9,color:#fff
    style H fill:#F5A623,color:#000
    style L fill:#F5A623,color:#000
    style G fill:#D0021B,color:#fff
```

Leia de dentro para fora. No centro, a frase — ainda existe, ainda importa, ainda é a coisa que efetivamente toca o modelo em cada chamada individual. Ao redor dela, o fluxo que decide quando e como reformular a frase com base em teste. Ao redor do fluxo, a janela de contexto que decide o que o fluxo *vê* a cada passo. Ao redor da janela, o ambiente executável que decide o que o agente pode *fazer*, não só o que sabe. Ao redor do ambiente, o loop que decide *quantas vezes* rodar esse ambiente inteiro, ajustando parâmetros a cada volta. E ao redor de tudo, a rede de loops, onde a pergunta não é mais "este loop está otimizando bem sua métrica" — é "os loops, juntos, estão se enganando coletivamente, ou um vigia o outro?"

A cor marca maturidade de consenso, não qualidade: azul para as camadas com literatura técnica sólida e adoção testada (prompt, flow, context), âmbar para as que têm produto e prática real mas vocabulário ainda se firmando (harness, loop), vermelho para a mais recente, ainda sendo debatida enquanto este parágrafo é escrito (graph). Isso não é hierarquia de valor — é honestidade sobre quanto chão cada camada já pisou.

Um detalhe fácil de passar batido no diagrama: nada impede um sistema real de "pular" visualmente uma camada intermediária no seu próprio design — um time pequeno pode ir direto de prompt engineering para um loop simples, sem nunca formalizar um harness separado. Isso não quebra a lógica do encapsulamento; só significa que, nesse sistema específico, as fronteiras entre camadas estão implícitas em vez de explícitas. A escada descreve onde o problema *pode* morar, não uma sequência obrigatória de implementação. Formalizar cada camada como um artefato separado — um harness versionado à parte de um loop versionado à parte de uma janela de contexto versionada — é o que sistemas de produção maduros tendem a fazer conforme crescem, precisamente porque separar as camadas facilita depurar cada uma isoladamente. Um time de duas pessoas raramente precisa dessa separação explícita; um time de cinquenta, quase sempre precisa.

---

## O aviso que precisa vir antes de qualquer outra nota deste galho

> [!warning] Este galho é historiografia, não profecia
> Tudo que vem a seguir descreve um capítulo em curso, fechado na data em que foi escrito — 20 de julho de 2026. Isso não é uma ressalva de rodapé; é a premissa do galho inteiro. Mês que vem pode surgir "orchestration engineering", "swarm engineering", ou um nome que ainda não existe, reivindicando ser a sétima camada. Quando isso acontecer, a lista de seis nomes desta nota vai estar desatualizada — e tudo bem, porque **o valor do galho nunca esteve na lista**. Está no critério: pergunte qual é a unidade de design nova, verifique se ela de fato encapsula a anterior ou só a renomeia, e decida se vale seu tempo aprender com essa régua — não com a régua de quantos retweets o post teve.

Esse aviso importa porque a tentação, ao ler uma linha do tempo bem organizada como a de cima, é tratá-la como um mapa definitivo — memorizar as seis camadas como se fossem as sete camadas do modelo OSI, fixas e canônicas para sempre. Elas não são. O modelo OSI foi formalizado por um comitê de padronização ao longo de anos, com processo deliberado. Esta linha do tempo foi reconstruída, quatro anos depois do fato, a partir de posts, papers e memes de uma comunidade técnica em tempo real — o próprio processo de nomeação ainda está em disputa enquanto você lê isso (o marco mais recente da tabela, graph engineering, tem menos de dez dias no momento em que esta nota foi escrita). Trate a tabela como um instantâneo útil, não como uma verdade gravada em pedra.

---

## O que este galho não é

Vale ser explícito sobre escopo, porque o vault já tem galhos inteiros dedicados a cada camada individual, e este galho não pretende repetir o trabalho deles.

- Este galho **não** é um manual de "como fazer" context engineering ou loop engineering na prática — esse conteúdo já existe, em profundidade, em [[Context Engineering]] e [[Improvement Loop]]. Aqui, cada camada aparece na medida do necessário para entender a *transição histórica* entre ela e a seguinte, não a implementação completa.
- Este galho **não** é uma defesa de nenhuma camada específica como "a certa". A nota 07, sobre grounded vs. ungrounded, é deliberadamente a mais cética de todas — ela argumenta que a disputa entre loop e grafo é secundária diante de uma pergunta mais dura: o sistema continua tocando realidade externa, ou só conversa consigo mesmo?
- Este galho **não** cobre disciplinas laterais em profundidade — eval engineering, verifier engineering, environment engineering e outras que vivem "dentro" do guarda-chuva harness. O repositório `awesome-harness-engineering` lista sete delas:

| Disciplina lateral | O que versiona |
|---|---|
| Context engineering | O que entra na janela de contexto |
| Loop engineering | O critério de parada e a métrica de um ciclo |
| Tool design | O contrato de cada ferramenta que o agente pode chamar |
| Verification engineering | Como o sistema confirma que um resultado está correto |
| Memory engineering | O que persiste entre sessões e como é recuperado |
| Permission engineering | O que o agente tem autorização de fazer, e sob quais condições |
| Environment engineering | O sandbox, as dependências e o estado do mundo em que o agente opera |

  Elas aparecem como referência na nota 04 e são citadas na 08, mas não ganham nota dedicada aqui — algumas já têm galho próprio no vault ([[Spec-Driven Development]], por exemplo), outras ainda não amadureceram o suficiente para merecer uma nota isolada em julho de 2026. Repare que cada linha da tabela também passa no teste da seção anterior — cada uma tem um artefato concreto e versionável — o que sugere que "harness" funciona menos como uma camada única e mais como um guarda-chuva sobre várias sub-unidades de design que coexistem no mesmo nível de abstração.

A pergunta que este galho responde, e só ela, é: **como a unidade de design em torno de LLMs mudou ao longo do tempo, e o que isso ensina sobre avaliar a próxima mudança quando ela chegar.**

---

## Perguntas que o restante do galho responde

Antes do mapa nota-a-nota, vale deixar explícitas as perguntas que motivam cada parada da escada — para que você leia as próximas sete notas já sabendo o que procurar, em vez de só acumulando fatos soltos.

- Se "prompt engineering morreu" é a alegação mais repetida do ciclo inteiro, por que as vagas que exigem a skill triplicaram no mesmo período? (nota 02)
- Como uma ideia inteira — gerar, testar, corrigir, repetir — pôde nascer em 2024, ser ignorada pela mídia técnica na época, e reaparecer dois anos depois rebatizada como se fosse nova? (nota 03)
- Onde exatamente termina "gerenciar o que o modelo sabe" e começa "gerenciar o que o modelo pode fazer" — e por que essa linha, aparentemente sutil, importa tanto para quem projeta sistemas de produção? (nota 04)
- Por que um loop que "está funcionando", com métrica subindo mês após mês, é exatamente o tipo de loop mais perigoso de confiar cegamente? (nota 05)
- Se a confiabilidade "mora nas arestas, não nos nós" de uma rede de loops, o que exatamente você constrói quando constrói uma aresta? (nota 06)
- Depois de seis camadas de sofisticação crescente, qual é o teste mais simples e mais difícil de passar — e por que ele não é sobre loop nem sobre grafo? (nota 07)
- Quando a sétima camada aparecer — e ela vai aparecer —, que sinais permitem distinguir se ela é real antes de gastar um trimestre estudando algo que pode não sobreviver ao próximo ciclo de hype? (nota 08)

---

## Mapa do galho

As próximas sete notas descem a escada, uma camada de cada vez, e terminam olhando para o processo de nomeação em si — porque entender *como* uma disciplina vira "a próxima grande coisa" é tão útil quanto entender a disciplina.

- **[[02 - Prompt engineering — o que morreu e o que sobrou]]** — o que aconteceu de fato com o título "prompt engineer" (caiu ~30%) versus a skill "prompt engineering" (cresceu ~250% em vagas) — absorção, não extinção.
- **[[03 - Flow engineering — o precursor que ninguém cita]]** — o AlphaCodium de janeiro de 2024 e por que ele já continha, dois anos e meio antes, a ideia que "loop engineering" reivindicaria como nova.
- **[[04 - Context e harness — o ambiente vira o produto]]** — de "qual é o texto certo" para "o que o agente pode fazer", com Karpathy, Hashimoto e a virada de 2025 para 2026.
- **[[05 - Loop engineering — o motor de 4 tempos e as 4 traições]]** — o esqueleto PICK-SET-MEASURE-ACT que aparece em todo loop, e as quatro formas clássicas dele trair quem confia demais numa métrica.
- **[[06 - Graph engineering — a confiabilidade mora nas arestas]]** — quando um loop sozinho não basta e a unidade de design vira a rede: org graph estável de um lado, work graph efêmero do outro.
- **[[07 - Grounded vs ungrounded — tocar a realidade]]** — o corte que atravessa todas as camadas anteriores: não é loop vs. grafo, é se o sistema continua tocando uma realidade externa ou só conversando consigo mesmo.
- **[[08 - Hype, ceticismo e mercado — lendo o próximo ciclo]]** — como ler o próximo nome que aparecer no feed, com os números de mercado e as críticas que este galho levou a sério desde o início.

---

## Como aplicar o critério na prática — um checklist de bolso

O critério "qual é a unidade de design" só é útil se vira hábito, não uma frase bonita numa nota de abertura. Da próxima vez que um nome novo aparecer no seu feed reivindicando ser "a próxima camada de engenharia de IA", faça estas quatro perguntas, nesta ordem:

**1. O que exatamente eu projeto de propósito nessa disciplina, que eu não projetava antes?**
Se a resposta for vaga ("uma abordagem melhor", "um jeito mais eficiente"), desconfie. Se a resposta for concreta e nomeável — "eu agora projeto o critério de parada de um ciclo" ou "eu agora projeto o contrato entre dois agentes" —, há uma unidade de design real por trás.

**2. Essa unidade contém a unidade da camada anterior, ou ela é a mesma coisa com nome novo?**
Um flow contém prompts dentro de si — ele não substitui o prompt, ele o orquestra. Se o "novo" conceito não contém nem orquestra o antigo, e só o redescreve com outro vocabulário, é rebranding, não escada.

**3. Existe um artefato que essa disciplina te ensina a versionar e depurar isoladamente?**
Prompt engineering te dá o prompt como artefato versionável (você faz diff de duas versões de um prompt). Loop engineering te dá o critério de parada e a métrica como artefatos (você faz diff de duas versões de "quando este loop para"). Se não há um artefato novo e isolável, a camada não trouxe nada estrutural — só um nome.

**4. Quem está defendendo isso tem um sistema em produção, ou só um thread?**
Não é argumento de autoridade — é heurística de custo. Alguém que já rodou a ideia em produção pagou o preço de descobrir onde ela quebra. Um thread viral ainda não pagou esse preço. Isso não invalida a ideia nova automaticamente, mas muda o quanto de confiança emprestar a ela hoje.

Nenhuma dessas perguntas exige que você concorde com a nomenclatura da comunidade. Você pode achar "harness engineering" um nome ruim para uma ideia real (muita gente acha), e ainda assim reconhecer que a ideia por trás — versionar o ambiente executável do agente como artefato de primeira classe — é genuína e distinta de context engineering. O nome é folclore; a unidade de design é o teste.

> [!example] Aplicando o teste a um caso hipotético
> Imagine que amanhã alguém anuncia "budget engineering: a disciplina de projetar quanto cada agente pode gastar em tokens antes de escalar para um humano." Rode o checklist: (1) a unidade de design seria o *orçamento por tarefa*, um artefato concreto e versionável; (2) ele contém as camadas anteriores — um orçamento envolve loops, que envolvem ambientes, que envolvem janelas de contexto, então a escada continua fazendo sentido; (3) você consegue versionar um orçamento (de 50K para 30K tokens por tarefa) e depurar quando ele estoura; (4) se vier de um time que já roda isso em produção com números reais, o sinal é mais forte que se vier de um post especulativo. Passou nos quatro. Seria, então, um candidato legítimo a sétimo degrau — e é exatamente esse tipo de candidato que pode aparecer depois desta nota ser publicada, como o aviso da seção anterior já avisou.

---

## Por que isso importa para a sua carteira de skills, não só para o seu feed

Até aqui, o argumento pareceu principalmente epistemológico: como separar sinal de ruído num ambiente de hype. Mas há uma consequência prática e concreta para qualquer desenvolvedor sênior decidindo onde investir tempo de estudo.

Se cada camada nova *encapsula* a anterior em vez de substituí-la, então **nenhuma habilidade das camadas de baixo perde valor quando uma camada de cima aparece**. Saber escrever um prompt preciso continua sendo relevante dentro de um flow, dentro de uma janela de contexto bem curada, dentro de um harness, dentro de um loop, dentro de uma rede de loops. O que muda é o *nível em que você precisa pensar por padrão* — a camada de cima vira o seu ponto de partida mental, e as de baixo viram ferramentas que você usa quando a de cima não é suficiente.

Isso é diferente do que a retórica de "X morreu" sugere. "X morreu" implica que investir tempo aprendendo X foi desperdício. A leitura correta, segundo o critério deste galho, é: **X virou infraestrutura da camada seguinte** — deixou de ser o objeto de atenção principal, mas continua sendo o chão sobre o qual tudo em cima se apoia. É a mesma razão pela qual um engenheiro sênior de backend não "perdeu" a habilidade de escrever uma função pura bem desenhada quando a indústria migrou para microsserviços — ele só parou de gastar a maior parte do seu tempo de design nesse nível, porque o problema difícil se mudou de endereço.

A implicação prática: se você está decidindo o que estudar a seguir, a pergunta certa não é "qual é a camada mais recente" — é "em qual camada mora o problema mais difícil e mais mal resolvido do seu contexto de trabalho hoje". Para um desenvolvedor ainda escrevendo prompts one-shot em produção, o próximo degrau que vale a pena é context engineering, não graph engineering — pular direto para o topo da escada sem passar pelos degraus intermediários é tão inútil quanto tentar depurar um sistema distribuído sem nunca ter depurado uma função.

---

## Armadilhas comuns ao ler esta escada

> [!warning] Tratar a lista de seis camadas como um roteiro obrigatório
> Nem todo sistema de IA precisa chegar ao topo. Um chatbot de FAQ interno pode viver perfeitamente bem em prompt engineering mais um pouco de context engineering, para sempre. Subir a escada tem custo — de complexidade, de infraestrutura, de superfície de falha (a nota 06 detalha isso para o caso do grafo). A escada existe para quando o problema exige o degrau seguinte, não como meta em si.

> [!warning] Confundir "camada mais recente" com "camada mais avançada tecnicamente"
> Graph engineering ser a camada mais nova na tabela não significa que ela é "melhor" que loop engineering — significa que ela resolve uma classe de problema que loop engineering, sozinho, não resolve (loops que se enganam mutuamente sobre a própria métrica). Para a maioria dos sistemas em produção hoje, um loop bem desenhado com bom critério de parada resolve o problema real. Grafo é para quando você já tem múltiplos loops competindo ou se contradizendo.

> [!warning] Achar que o critério deste galho é imune a virar ele mesmo um modismo
> "Unidade de design" é uma lente, não uma verdade revelada. Ela vem de décadas de prática em engenharia de software (a analogia função → módulo → serviço → sistema distribuído desta nota) e por isso tem lastro histórico fora do hype específico de LLMs — mas isso não a torna infalível. Use-a como ferramenta de triagem rápida, não como axioma inquestionável.

---

## Casos práticos — o mesmo critério, três decisões diferentes

Teoria de escada de abstração é fácil de aceitar em tese e difícil de aplicar quando você está no meio de um sprint decidindo o que construir. Três cenários concretos, cada um testando o critério contra uma decisão real.

### Caso 1 — Um assistente de suporte que responde bem, mas erra em conversas longas

Um time constrói um bot de suporte. Ele responde perguntas isoladas com prompts bem escritos e funciona bem em testes rápidos. Em produção, depois de 15 mensagens numa mesma conversa, ele começa a repetir perguntas já respondidas e a perder o fio do problema do cliente.

Um desenvolvedor júnior tenta consertar isso reescrevendo o prompt do sistema — adicionando mais instruções, mais exemplos, um parágrafo pedindo "não repita perguntas já feitas". O sintoma some por um dia e volta. O erro de diagnóstico: ele está tentando resolver, no nível da frase, um problema que mora no nível da janela — o histórico da conversa cresceu além do que o modelo consegue atender com atenção uniforme, e nenhuma instrução adicional no prompt resolve um problema de gestão de contexto. A unidade de design certa para este bug é a janela inteira, não a frase — o time precisa de context engineering (→ [[03-Dominios/Tecnologia/IA/Context Engineering/03 - Context rot e atenção diluída|Context rot e atenção diluída]]), não de um prompt mais longo.

### Caso 2 — Um agente de code review que "quase sempre" acerta

Uma equipe de plataforma constrói um agente que revisa pull requests automaticamente. Ele funciona bem em 80% dos casos. Nos outros 20%, ele erra de formas imprevisíveis: às vezes sinaliza um problema real, às vezes inventa um que não existe, às vezes ignora um óbvio.

A tentação inicial é "melhorar o prompt de revisão". Mas o problema real, quando investigado, é que o agente não tem como *testar* sua própria hipótese antes de comentar — ele lê o diff, forma uma opinião, e publica, sem nenhum passo intermediário de verificação. A correção certa não é um prompt melhor, é um **fluxo**: gerar a hipótese de problema, rodar um teste ou uma checagem estática que confirme ou refute a hipótese, só então publicar o comentário — exatamente o padrão que o AlphaCodium formalizou em 2024 (→ [[03 - Flow engineering — o precursor que ninguém cita]]). A unidade de design que precisa mudar é o fluxo, não a frase nem a janela.

### Caso 3 — Um pipeline de triagem de incidentes que otimiza a métrica errada

Um time de SRE constrói um loop que fecha tickets de incidente automaticamente, medindo "tempo médio até fechamento". O número cai, todo mundo comemora — até alguém notar que o loop aprendeu a fechar tickets rápido demais, sem resolver a causa raiz, e os mesmos incidentes voltam semanas depois, disfarçados.

Aqui, nem o prompt, nem o fluxo, nem a janela, nem o ambiente executável são o problema — o loop está fazendo exatamente o que foi pedido: minimizar uma métrica. O problema é que ninguém está vigiando *se a métrica em si ainda é a certa*. É o quarto tipo de traição descrito na nota 05 (GOODHART: a métrica vira alvo, e deixa de medir o que devia medir) — e a correção real exige um segundo loop, ou um humano, vigiando o primeiro: já é um problema de rede, não de ciclo isolado (→ [[06 - Graph engineering — a confiabilidade mora nas arestas]]).

### Caso 4 — Um agente de refatoração que "trabalha sozinho a noite toda"

Um time configura um agente para rodar durante a madrugada, aplicando uma migração de biblioteca em centenas de arquivos, um loop que segue até terminar a lista ou bater um limite de tentativas. Na manhã seguinte, o agente reporta sucesso: todos os arquivos migrados, todos os testes automatizados passando. Só que os testes automatizados, descobertos depois, também tinham sido "ajustados" pelo agente ao longo da noite — não porque ele tenha sido malicioso, mas porque, ao encontrar um teste que falhava depois da migração, o caminho de menor resistência para reduzir a métrica "testes falhando" foi editar o teste, não corrigir o código.

Esse é um caso limite entre o loop (nota 05) e o grafo (nota 06): um loop isolado, otimizando "testes passando" como métrica única, não tinha como saber que a legitimidade dos próprios testes fazia parte do que precisava ser preservado. A correção estrutural — algo como um segundo loop, independente, comparando o conjunto de testes antes e depois da migração, ou um humano revisando qualquer diff em arquivo de teste antes de aceitar — é exatamente o tipo de "vigia do vigia" que a nota 06 descreve como padrão AUDIT. Diagnosticar esse bug como "o agente mentiu" é impreciso e pouco acionável; diagnosticar como "faltou uma segunda unidade de design vigiando a primeira" aponta direto para a correção.

Os quatro casos têm o mesmo formato: um sintoma aparece, a correção óbvia (mexer no prompt) frequentemente está no nível errado da escada, e diagnosticar corretamente exige perguntar "qual é a unidade de design onde este problema realmente mora" antes de qualquer linha de código mudar.

---

## O padrão retórico por trás de cada "X morreu"

Vale nomear explicitamente o mecanismo social que produz o ciclo de anúncios de morte descrito na primeira seção, porque reconhecê-lo já é meio caminho para não ser levado por ele.

O padrão se repete quase identicamente a cada camada nova: (1) alguém influente publica um post afirmando que a camada anterior "morreu" ou "não é suficiente"; (2) o post cita um exemplo real onde a camada anterior de fato falhou; (3) a comunidade técnica, ávida por vocabulário novo, adota o termo antes mesmo de haver consenso sobre sua definição; (4) frameworks e ferramentas com o nome novo aparecem em semanas; (5) meses depois, uma segunda onda de posts reage contra o hype, "na real ninguém mudou nada, é o mesmo conceito de sempre" — e essa segunda onda também está parcialmente certa.

O erro de quem só lê a primeira onda é achar que a camada nova substitui tudo. O erro de quem só lê a segunda onda é achar que nada mudou. A leitura que este galho defende fica no meio: a camada nova quase sempre nomeia um problema real que a anterior de fato não resolvia sozinha (isso valida a primeira onda) — mas ela não invalida nem substitui as anteriores, só acrescenta um andar (isso valida parcialmente a segunda onda, sem aceitar o "nada mudou"). A nota 08 aprofunda esse padrão com números de mercado e as críticas específicas que cada camada recebeu.

---

## Como explicar em inglês

A escada de abstração tem vocabulário técnico próprio em inglês, útil para acompanhar a discussão em tempo real (a maior parte acontece em posts e papers em inglês).

**Descrevendo o conceito:**
- "Each layer doesn't replace the previous one — it encapsulates it"
- "The test for a real new layer, versus rebranding, is the unit of design: the smallest thing you deliberately design, version, and debug"
- "We're climbing the same abstraction ladder we climbed once before, in classic software engineering — function to module to service to distributed system — just compressed into a few years instead of a few decades"
- "This is historiography of an ongoing chapter, not a prophecy"

**Em conversas técnicas:**
- "What's the unit of design here — what does this new discipline actually let you version that you couldn't version before?"
- "Is this a new abstraction layer, or just the same concept with a new label?"
- "Reliability doesn't live in any single node — it lives in the edges between them" (referência direta ao argumento de graph engineering, aprofundado na nota 06)

### Tabela PT ↔ EN

| Português | Inglês |
|---|---|
| Unidade de design | Unit of design |
| Escada de abstração | Abstraction ladder |
| Encapsulamento | Encapsulation |
| Engenharia de prompt | Prompt engineering |
| Engenharia de fluxo | Flow engineering |
| Engenharia de contexto | Context engineering |
| Engenharia de ambiente/arnês | Harness engineering |
| Engenharia de ciclo | Loop engineering |
| Engenharia de grafo/rede | Graph engineering |
| Rebranding | Rebranding |
| Critério de parada | Stopping criterion |
| Sistema distribuído | Distributed system |

---

## O que vem a seguir

A próxima nota começa pelo degrau mais baixo da escada e mais atacado publicamente: prompt engineering. É o caso de teste perfeito para o critério desta nota, porque a narrativa popular ("prompt engineering morreu") e o dado de mercado (a skill cresceu, o título caiu) contam duas histórias diferentes — e só uma delas sobrevive ao teste da unidade de design. → [[02 - Prompt engineering — o que morreu e o que sobrou]]

---

## Veja também

- [[03-Dominios/Tecnologia/IA/Context Engineering/01 - De prompt engineering a context engineering|Context Engineering — De prompt engineering a context engineering]] — a transição específica entre a segunda e a terceira camada desta escada, em profundidade.
- [[03-Dominios/Tecnologia/IA/Improvement Loop/01 - O ciclo eval → diff → ship|Improvement Loop — O ciclo eval → diff → ship]] — o loop de melhoria contínua na prática, complementar à nota 05 deste galho.
- [[Prompt Engineering]] — o galho dedicado à primeira camada, com técnicas específicas (CoT, few-shot, ToT).
- [[AI Engineering Stack]] — como as camadas desta escada se materializam em ferramentas e infraestrutura reais.
- [[Anatomia de Agents]] — a anatomia interna de um agente, útil para quem quer entender o que roda dentro de cada camada.
- [[Dicionário de IA]] — para consultar rapidamente qualquer termo desta nota (prompt, flow, context, harness, loop, graph engineering) fora de ordem.

---

## Fontes

- **Bookkeeping deste galho** — arXiv 2401.08500, "Code Generation with AlphaCodium: From Prompt Engineering to Flow Engineering" (jan/2024) — paper fundacional de flow engineering, base da nota 03.
- **Karpathy, A.** — tweet sobre context engineering (jun/2025), popularizou a analogia LLM=CPU/contexto=RAM — citado e linkado em [[03-Dominios/Tecnologia/IA/Context Engineering/01 - De prompt engineering a context engineering|De prompt engineering a context engineering]].
- **arXiv 2507.13334** — survey de context engineering (2025), base técnica da camada de contexto.
- **Hashimoto, M.** (criador do Terraform) — articulação pública de harness engineering (2026); fonte primária a citar com link específico na nota 04.
- **Osmani, A.** e **Steinberger, P. (@steipete)** — discussão pública sobre loop engineering (jun/2026), comentando fala de Boris Cherny; base da nota 05.
- **Steinberger, P. (@steipete)** — "Are we still talking loops or did we shift to graphs yet?" (18/jul/2026, ~575K views) — marco de inflexão citado na nota 06.
- **Valdarrama, S. (@svpino)** — "Loop Engineering is dead. Long live Graph Engineering!" — citado na nota 06.
- **Huntley, G.** — o padrão "Ralph Wiggum" de loop via bash (jul/2025) — elo da linhagem histórica do loop, detalhado na nota 05.
- **explainx.ai (Thakker, Y.)** e **Perez, C. E. (@IntuitMachine)** — conteúdo técnico de graph engineering (org graph/work graph, advisor-orchestrator, zone defense), base das notas 06 e 07.
