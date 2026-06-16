---
title: "Carga cognitiva e legibilidade"
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
  - carga-cognitiva
  - legibilidade
---

# Carga cognitiva e legibilidade

A nota anterior fechou dizendo que um módulo raso impõe um custo ao leitor: você paga em esforço mental cada vez que precisa entender uma interface inflada pra mudar algo com segurança ([[07 - Módulos profundos e rasos]]). Esse custo tem nome — **carga cognitiva** — e é hora de olhar pra ele de frente. Porque, no fim, todas as heurísticas de design das notas anteriores existem por um motivo só: código é **lido** muito mais vezes do que é **escrito**, e quem lê tem uma cabeça com capacidade finita.

> [!abstract] TL;DR
> **Carga cognitiva** é o esforço mental que você precisa gastar *agora* pra entender um trecho de código e mudá-lo com segurança. É **momentânea** e **individual** — uma propriedade de uma pessoa diante de uma tarefa, limitada pela memória de trabalho (que segura só ~4 chunks). Não confunda com **débito cognitivo**, que é de **time** e se acumula ao **longo do tempo** ([[11 - Dívida cognitiva]]). A teoria da carga cognitiva (Sweller) separa três tipos — intrínseca (o problema é difícil mesmo), estranha (a apresentação ruim atrapalha) e germânica (o esforço que constrói entendimento) — e os dois primeiros mapeiam direto no par essencial/acidental ([[02 - Complexidade essencial vs. acidental]]). Legibilidade é o conjunto de alavancas que cortam a carga estranha: bons nomes, localidade, consistência e o **princípio da menor surpresa**. E cuidado com métricas: complexidade ciclomática mede *uma* faceta (ramificação de fluxo), não "a" dificuldade humana.

## O que é

**Carga cognitiva** (*cognitive load*) é a quantidade de esforço mental que uma tarefa exige da sua **memória de trabalho** — a parte da mente que segura e manipula informação ativa, o "RAM" do raciocínio. Diante de um trecho de código, a carga é tudo que você precisa segurar na cabeça ao mesmo tempo pra entender o que ele faz: quais variáveis estão em jogo, qual o estado atual, que invariantes valem, o que essa chamada faz lá embaixo, o que pode dar errado.

O detalhe que torna isso urgente é uma limitação dura da biologia: a memória de trabalho é **pequena**. A estimativa clássica de Miller era "7 ± 2" itens; pesquisas mais recentes apontam algo ainda mais modesto — cerca de **4 chunks** processados simultaneamente. Quando a tarefa exige segurar mais do que cabe, você sofre **sobrecarga cognitiva**: passa a reler, a perder o fio, a errar. Carga alta não é desconforto estético — é causa direta de **mais lentidão e mais bugs**.

> [!note] Carga é uma propriedade de quem lê, não só do código
> Duas pessoas diante do mesmo arquivo podem sentir cargas muito diferentes. Quem já tem o domínio na cabeça (chunks prontos, o *conhecimento prévio* de que a teoria fala) lê com folga; quem chega de fora afoga. Por isso carga cognitiva é **momentânea e individual** — depende da tarefa, do código *e* de quem está olhando agora. Não é um número fixo gravado no arquivo.

## Carga cognitiva não é débito cognitivo

Aqui mora a distinção mais importante desta nota — e a razão dela existir como âncora conceitual. Três termos parecidos descrevem coisas diferentes, e confundi-los embaralha o diagnóstico:

| Conceito | Onde vive | Natureza |
| --- | --- | --- |
| **Débito técnico** | no código | atalhos estruturais que cobram juros em manutenção |
| **Carga cognitiva** | no indivíduo, no momento | esforço mental exigido por uma tarefa *agora* |
| **Débito cognitivo** | na mente coletiva, ao longo do tempo | erosão do entendimento compartilhado em nível de projeto |

A linha que separa os dois "cognitivos" é eixo e escala. **Carga cognitiva** é *individual* e *instantânea*: o esforço que *você* gasta pra entender *este* trecho *agora*. **Débito cognitivo** é *coletivo* e *temporal*: a erosão, ao longo de meses, da [[O programa como teoria|teoria do sistema]] que o *time* compartilha — o que acontece quando ninguém mais detém o porquê das decisões ([[11 - Dívida cognitiva]]).

A consequência prática é que você pode atacar um sem mexer no outro. Refatorar um nome ruim baixa a carga cognitiva de quem lê amanhã, mas não reconstrói sozinho o entendimento que o time perdeu. E um sistema com código impecável (carga baixa por trecho) pode estar afundado em débito cognitivo, porque a teoria do conjunto se dissolveu. Sob a lente da IA generativa, esse descolamento fica gritante — é o tema da nota de IA, que herda exatamente esta distinção.

> [!note] Por que a confusão é perigosa
> Quando alguém diz "esse código tem carga cognitiva alta", está falando de uma *experiência de leitura* — solúvel com legibilidade. Quando diz "estamos com débito cognitivo", está falando de uma *perda organizacional de entendimento* — solúvel com práticas de time (pair programming, reviews, documentar o porquê). Tratar o segundo como se fosse o primeiro ("é só refatorar os nomes") é remédio errado pra doença errada.

## Os três tipos de carga

A **teoria da carga cognitiva** (*cognitive load theory*), formulada por **John Sweller** no fim dos anos 1980 no contexto de educação, separa a carga em três tipos. Trazidos pro código, eles encaixam com precisão no par essencial/acidental ([[02 - Complexidade essencial vs. acidental]]):

- **Carga intrínseca** (*intrinsic*) — a dificuldade inerente ao próprio problema. Um algoritmo de consenso distribuído é difícil de entender porque consenso distribuído *é* difícil, não porque o código está mal escrito. Isso mapeia na **complexidade essencial**: é o piso irredutível, a dificuldade que nenhuma refatoração elimina.
- **Carga estranha** (*extraneous*) — o esforço imposto pela *apresentação* ruim, não pelo problema. Nomes enganosos, estado espalhado, indireção gratuita, formatação caótica: tudo que faz você gastar memória de trabalho com coisas que não são o problema. Isso é a **complexidade acidental** vivida pela cabeça do leitor — e é exatamente a parte que dá pra cortar.
- **Carga germânica** (*germane*) — o esforço *produtivo*, o que constrói entendimento durável (formar chunks, montar a teoria do sistema). Não é desperdício; é o trabalho mental que vira conhecimento. O objetivo do bom design não é zerar toda carga — é liberar memória de trabalho da carga estranha pra sobrar capacidade pra intrínseca e germânica.

> [!tip] A conta que importa
> Na teoria, as três cargas são aproximadamente **aditivas**: intrínseca + estranha + germânica = carga total, e a sobrecarga acontece quando a soma estoura a memória de trabalho. Você não controla a intrínseca (o problema é o que é) nem quer matar a germânica (ela é o aprendizado). O alvo do design — e da legibilidade — é uma coisa só: **espremer a carga estranha até quase zero**, pra que a cabeça do leitor caiba no problema de verdade.

## Alavancas de legibilidade

Legibilidade é o nome do conjunto de escolhas que reduzem a **carga estranha**. Vale lembrar o motivo de fundo: código é lido muito mais vezes do que é escrito, então otimizar pra escrita rápida à custa da leitura é trocar uma economia pequena por um imposto perpétuo. As principais alavancas:

- **Bons nomes.** Um nome que diz o que a coisa é e faz poupa o leitor de reconstruir o sentido a partir do uso. `daysSinceLastLogin` é um chunk pronto; `d` força você a rastrear de onde veio e o que significa — pura carga estranha.
- **Localidade.** Coisas que mudam juntas devem ficar **perto**. Quando entender uma função exige pular entre sete arquivos, cada salto consome um slot da memória de trabalho que devia estar no problema. Manter o relacionado próximo é manter a cabeça do leitor inteira.
- **Consistência.** Quando o código segue padrões previsíveis (mesma forma pra mesma intenção), o leitor reaproveita chunks em vez de aprender cada trecho do zero. Inconsistência obriga a tratar tudo como caso especial.
- **Princípio da menor surpresa** (*principle of least astonishment*, POLA). Um componente deve se comportar do jeito que a maioria dos leitores **espera** — alinhado ao modelo mental deles. Um método chamado `getUser` que silenciosamente grava no banco viola o princípio: a surpresa custa caro, porque o leitor confiou no nome e errou. Seguir convenções da plataforma é a forma mais barata de não surpreender.

Todas essas alavancas combatem o que Ousterhout chama de **obscuridade** (*obscurity*): quando uma informação importante pra entender o código **não é óbvia** — está implícita, escondida num efeito colateral, dependente de contexto que o leitor não tem. Obscuridade é, nas palavras dele, um dos dois grandes sintomas de complexidade (o outro é a *change amplification* da nota 01). Legibilidade é, no fundo, a guerra contra a obscuridade.

> [!warning] "Eu entendo, então está claro"
> O autor de um trecho quase nunca sente a carga estranha que ele impõe — porque carrega na cabeça todo o contexto que o leitor não tem. "Pra mim está óbvio" é o viés que produz código obscuro. O teste honesto não é se *você* entende; é se alguém **sem o seu contexto** entende. Por isso code review e a pergunta "o que um leitor precisa saber que não está aqui?" valem mais que a sua própria sensação de clareza.

## A armadilha das métricas

Se carga cognitiva importa tanto, por que não medir e botar um número no CI? Porque as métricas que temos medem **facetas**, não o todo — e tratar uma faceta como "a" complexidade é cair numa armadilha.

A métrica clássica é a **complexidade ciclomática** (*cyclomatic complexity*), proposta por **Thomas McCabe** em 1976. Ela conta o número de caminhos linearmente independentes pelo grafo de fluxo de controle — na prática, quantos pontos de decisão (`if`, `for`, `case`, `&&`) o código tem, mais um. É útil: alta complexidade ciclomática sinaliza muitos ramos, e muitos ramos geralmente custam mais pra testar e seguir. Mas ela mede **uma única coisa** — ramificação de fluxo — e é cega pra quase todo o resto que pesa na cabeça humana: nomes ruins, indireção, estado escondido, nível de aninhamento. **Ciclomática baixa não implica carga cognitiva baixa.** Um `switch` gigante e plano pontua alto e é trivial de ler; três `if` aninhados dentro de um loop pontuam baixo e doem.

> [!warning] Goodhart: a métrica vira alvo
> *"When a measure becomes a target, it ceases to be a good measure."* No instante em que "complexidade ciclomática < 10" vira meta de CI, gente começa a fatiar funções só pra baixar o número — produzindo a *classitis* da nota anterior ([[07 - Módulos profundos e rasos]]): mais funções rasas, mais saltos, carga total maior, métrica menor. Use métricas como **detector de fumaça** (um trecho com número alto *merece um olhar*), nunca como **alvo** a otimizar.

Houve tentativas de aproximar melhor a dificuldade humana. A mais conhecida é a **Cognitive Complexity** da **SonarSource** (white paper de **G. Ann Campbell**, 2018), criada explicitamente porque *"testability != understandability"*: a ciclomática mede testabilidade, não compreensibilidade. A métrica da Sonar penaliza o que quebra o fluxo de leitura linear — cada nível de **aninhamento** soma mais, estruturas que interrompem a leitura custam, atalhos que a facilitam não custam. É um proxy melhor que a ciclomática pra "quão difícil isso é de ler". Mas continua sendo um **proxy**: aproxima o sintoma (controle de fluxo) e ainda ignora nomes, contexto e conhecimento prévio do leitor — justamente o que torna a carga *individual*. Nenhum número captura a carga cognitiva inteira, porque parte dela mora na cabeça de quem lê, não no arquivo.

## Referências

- **John Sweller** — *cognitive load theory* (final dos anos 1980), origem da tríade **intrinsic / extraneous / germane** e da tese de que a **memória de trabalho** é o gargalo. Limite de ~4 chunks processados simultaneamente (refinamento moderno do "7 ± 2" de Miller). Verificado contra panoramas secundários (edtechbooks.org, *Cognitive load* na Wikipedia, ScienceDirect Topics) na pesquisa que alimentou esta nota; a aplicação ao **código** (intrínseca↔essencial, estranha↔acidental) é mapeamento desta nota, não afirmação literal de Sweller.
- **Thomas J. McCabe** — *A Complexity Measure* (IEEE TSE, 1976), origem da **complexidade ciclomática** como contagem de caminhos linearmente independentes no grafo de fluxo de controle (`M = E − N + 2P`). Confirmado.
- **G. Ann Campbell / SonarSource** — *Cognitive Complexity: A new way of measuring understandability* (white paper, 2018; também publicado no *International Conference on Technical Debt 2018*). Métrica que penaliza aninhamento e quebras do fluxo linear de leitura, motivada por *"testability != understandability"*. Confirmado — é um proxy de compreensibilidade, não medida direta de carga.
- **John Ousterhout** — *A Philosophy of Software Design*, origem do termo **obscurity** (*obscuridade*) como um dos dois sintomas de complexidade. Ver lastro em [[07 - Módulos profundos e rasos]].
- **Princípio da menor surpresa** (*principle of least astonishment*, POLA) — formulado em publicação de design de linguagens de 1972; um componente deve se comportar como a maioria dos leitores espera, reduzindo carga cognitiva. Confirmado.
- **Lei de Goodhart** — *"When a measure becomes a target, it ceases to be a good measure"* — atribuída a Charles Goodhart; formulação canônica de Marilyn Strathern. Paráfrase fiel.

> [!note] Sobre o lastro
> A tríade de cargas e o limite da memória de trabalho (Sweller), a ciclomática (McCabe), a Cognitive Complexity (Campbell/SonarSource) e o POLA foram conferidos por busca contra fontes primárias e panoramas confiáveis. **Ressalva honesta:** não li o white paper da SonarSource nem os papers de Sweller página a página; as afirmações reproduzem o argumento e o vocabulário com alta fidelidade, mas detalhes de fórmula e fraseado podem diferir da redação original. O mapeamento intrínseca↔essencial / estranha↔acidental é construção desta nota. Padrão de marcação seguindo [[06 - Abstrações que vazam]].

## Veja também

- [[07 - Módulos profundos e rasos]] — a interface rasa que impõe carga cognitiva ao leitor
- [[02 - Complexidade essencial vs. acidental]] — o par que carga intrínseca e estranha espelham
- [[11 - Dívida cognitiva]] — o conceito de time, ao longo do tempo, que esta nota não é
- [[Dicionário de Fundamentos]] — verbetes do domínio
