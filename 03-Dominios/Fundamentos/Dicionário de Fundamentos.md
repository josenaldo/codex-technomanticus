---
title: "Dicionário de Fundamentos"
created: 2026-06-07
updated: 2026-06-16
type: glossary
status: seedling
aliases:
  - Glossário de Fundamentos
tags:
  - glossary
  - fundamentos
lang: pt
publish: true
---

# Dicionário de Fundamentos

> Termos de ciência da computação e engenharia de software que sobrevivem à troca de linguagem, framework ou paradigma — o vocabulário comum das outras estantes.

<!--
Como usar este glossário:

- Cada verbete é um `###` dentro de uma `##` temática.
- Linkar de outra nota: [[Dicionário de Fundamentos#Nome do termo]]
- Customizar texto exibido: [[Dicionário de Fundamentos#Nome do termo|texto]]
- A skill /verbete adiciona termos automaticamente em ordem alfabética.
- Ajuste `lang:` no frontmatter (`pt` ou `en`) — define o idioma das definições.
-->

## Abstração e design

### Abstração errada (the wrong abstraction)
Abstração extraída cedo ou de duplicação apenas aparente, que com o tempo só sobrevive à custa de parâmetros e condicionais empilhados para servir casos que não compartilham um segredo real. Tese de Sandi Metz (*The Wrong Abstraction*, 2016): "duplication is far cheaper than the wrong abstraction" — a duplicação tem custo honesto e linear, a abstração errada tem custo escondido e composto, agravado pela falácia do custo afundado. Remédio: re-inline ("the fastest way forward is back") e re-extração; prevenção: regra de três.

*Veja também: [[05 - Abstração - a ferramenta central]]*

### Abstração que vaza (leaky abstraction)
Abstração que falha em esconder completamente a complexidade subjacente que pretendia simplificar, forçando quem a usa a entender detalhes da camada de baixo. Termo de Joel Spolsky (*The Law of Leaky Abstractions*, 2002): "toda abstração não-trivial, em algum grau, vaza" — abstrações poupam tempo de trabalho, mas não de aprendizado.

*Veja também: [[Abstrações que vazam]]*

### Classitis
Síndrome nomeada por Ousterhout (*A Philosophy of Software Design*): a crença de que classes devem ser sempre pequenas e numerosas leva a fragmentar demais, produzindo muitas **classes rasas** em vez de poucas profundas. Cada peça parece simples isolada, mas o sistema todo fica mais complexo — há mais interfaces pra aprender e mais costuras (acoplamento) entre os fragmentos. O critério correto não é "classe pequena", e sim **profundidade** (funcionalidade ÷ complexidade da interface).

*Veja também: [[07 - Módulos profundos e rasos]]*

### Information hiding
Princípio de Parnas (*On the Criteria To Be Used in Decomposing Systems into Modules*, 1972): cada módulo deve esconder uma decisão de design propensa a mudar, localizando o impacto de mudanças futuras. Não é "esconder dados" nem decompor pelos passos do fluxograma — é guardar a decisão volátil atrás de uma interface estável.

*Veja também: [[05 - Abstração - a ferramenta central]]*

### Lei de Hyrum (Hyrum's Law)
Com um número suficiente de usuários de uma API, todo comportamento observável passa a ser dependido por alguém, independentemente do que o contrato promete. É o extremo lógico do vazamento de abstrações: em escala, toda a implementação vira interface implícita — alguém depende até dos bugs (Hyrum Wright / Titus Winters, *Software Engineering at Google*).

*Veja também: [[06 - Abstrações que vazam]]*

### Módulo profundo (deep module)
Módulo cuja **interface é pequena em relação à funcionalidade que esconde** — a razão funcionalidade ÷ complexidade de interface é alta (Ousterhout, *A Philosophy of Software Design*). É o que dá lucro: o cliente aprende pouco e ganha muito. O oposto é o **módulo raso** (*shallow module*), cuja interface é quase tão complicada quanto a implementação, pagando o custo de mais uma camada sem esconder nada. Exemplos profundos: o I/O de arquivos do Unix (`open`/`read`/`write`/`close`) e o garbage collector (funcionalidade enorme, interface zero). Profundidade importa mais que tamanho.

*Veja também: [[07 - Módulos profundos e rasos]]*

### Princípio da menor surpresa (POLA)
Um componente deve se comportar do jeito que a maioria dos seus leitores e usuários **espera** — alinhado ao modelo mental deles —, porque a surpresa custa carga cognitiva: o leitor confiou no nome ou na convenção e errou. *Principle of least astonishment*, formulado em design de linguagens de programação (1972). Um `getUser` que silenciosamente grava no banco viola o princípio; seguir as convenções da plataforma é a forma mais barata de não surpreender.

*Veja também: [[08 - Carga cognitiva e legibilidade]]*

## Complexidade e dívidas

### Carga cognitiva
Esforço mental momentâneo e individual para entender e mudar um trecho de código com segurança. É distinta do débito cognitivo, que é uma propriedade coletiva e acumulada ao longo do tempo: a carga é o custo do "agora" de uma pessoa diante do código.

*Veja também: [[08 - Carga cognitiva e legibilidade]]*

### Complexidade cognitiva (Cognitive Complexity)
Métrica da SonarSource (white paper de G. Ann Campbell, 2018) que mede *compreensibilidade*, não testabilidade — motivada pela tese "*testability != understandability*". Penaliza o que quebra a leitura linear: dá um incremento extra por **nível de aninhamento** e não penaliza atalhos que facilitam a leitura (um `switch` plano conta como um). É um proxy melhor que a complexidade ciclomática pra "quão difícil isso é de ler", mas continua sendo um proxy: ignora nomes, contexto e conhecimento prévio do leitor.

*Veja também: [[08 - Carga cognitiva e legibilidade]]*

### Complexidade acidental
Complexidade que vem das ferramentas, da linguagem e da representação escolhidas — não do problema em si. É onde o esforço de engenharia compensa, porque pode ser reduzida com melhores abstrações, linguagens e ferramentas.

*Veja também: [[02 - Complexidade essencial vs. acidental]]*

### Complexidade essencial
Complexidade inerente ao problema que o software resolve. Em larga medida é irredutível: nenhuma ferramenta ou linguagem melhor a elimina, porque ela é da natureza do domínio, não da implementação (Fred Brooks, *No Silver Bullet*).

*Veja também: [[02 - Complexidade essencial vs. acidental]]*

### Débito cognitivo
Erosão, ao longo do tempo, do entendimento compartilhado que uma equipe tem sobre o sistema. É uma propriedade de nível de projeto (coletiva e temporal), não o esforço individual de um leitor — distinção que o separa da carga cognitiva (Margaret-Anne Storey, *Triple Debt Model*).

*Veja também: [[11 - Dívida cognitiva]]*

### Débito de intenção
Ausência ou erosão do rationale externalizado — metas, restrições e o porquê das decisões — que explica por que o sistema é como é. Diferente das outras dívidas, vive nos artefatos (specs, ADRs, AGENTS.md) ou na falta deles, e só humanos a geram (Storey; Addy Osmani).

*Veja também: [[12 - Dívida de intenção]]*

### Débito técnico
Custo futuro acumulado por atalhos de implementação. Como um empréstimo, cobra "juros" na forma de manutenção mais cara a cada mudança, até ser pago por refatoração — metáfora cunhada por Ward Cunningham.

*Veja também: [[10 - Dívida técnica]]*

### Entropia de software
Tendência de um sistema a aumentar em desordem e complexidade conforme é modificado, a menos que se gaste energia ativa para contê-la. É o "software rot": sem manutenção deliberada, a estrutura decai e fica cada vez mais cara de mudar.

*Veja também: [[13 - Entropia de software e decaimento]]*

### Functional Relational Programming (FRP)
Arquitetura proposta por Moseley & Marks (*Out of the Tar Pit*, 2006) para minimizar complexidade acidental, combinando um núcleo funcional puro (que carrega a lógica essencial com transparência referencial, sem estado) ao modelo relacional de Codd (que estrutura os dados e o estado essencial que sobra). A ideia é empurrar o estado mutável — apontado pelos autores como a maior fonte de complexidade — para um canto pequeno, explícito e controlado. Não confundir com *Functional Reactive Programming*, que usa a mesma sigla mas é outra coisa.

*Veja também: [[02 - Complexidade essencial vs. acidental]]*

### Hipótese do espelhamento (mirroring)
Reformulação testável da Lei de Conway: a arquitetura técnica de um produto e a arquitetura social da organização que o produz são homólogas — fronteiras de módulo alinhadas com fronteiras de equipe. MacCormack, Baldwin & Rusnak (2012) confirmaram empiricamente que organizações fracamente acopladas produzem produtos mais modulares; Colfer & Baldwin (2016), revisando 102 estudos, acharam o espelhamento em ~69% dos casos, com duas formas conhecidas de "quebrar o espelho".

*Veja também: [[16 - Lei de Conway]]*

### Lei de Conway
Organizações que projetam sistemas produzem desenhos cuja estrutura espelha a estrutura de comunicação da própria organização (Melvin Conway, 1968).

*Veja também: [[16 - Lei de Conway]]*

### Mudança amplificada (change amplification)
Sintoma de complexidade em que uma mudança conceitualmente pequena exige editar muitos lugares do código — trocar uma cor padrão que está hardcoded em vinte arquivos. Um dos três sintomas de Ousterhout (*A Philosophy of Software Design*); nasce sobretudo de **dependências** (peças que não podem ser mudadas isoladamente). O custo da mudança fica desproporcional ao tamanho da intenção.

*Veja também: [[01 - A complexidade como problema central]]*

### Programação como construção de teoria (theory building)
Tese de **Peter Naur** (*Programming as Theory Building*, 1985): o produto real da programação não é o código, e sim a **teoria** que os desenvolvedores formam — como o programa corresponde ao mundo, por que está estruturado assim, e como evoluí-lo com coerência. "Teoria" no sentido de **Ryle**: uma capacidade (*knowing-how*), não um texto. Código e documentação são externalizações *parciais*; o "porquê" é majoritariamente **tácito** (Polanyi). Corolário: um programa "morre" quando a equipe que detém sua teoria se dispersa — ainda executa, mas ninguém consegue modificá-lo com segurança.

*Veja também: [[04 - O programa como teoria]]*

### Programação tática vs. estratégica
Duas posturas diante de cada decisão de design (Ousterhout, *A Philosophy of Software Design*). A **tática** otimiza o agora — "fazer funcionar" o mais rápido possível —, e seu extremo é o *tactical tornado*, que despeja features deixando complexidade para os outros limparem. A **estratégica** trata o bom design como meta primária ("a great design, which also happens to work"), com mentalidade de **investimento**: ~10–20% do tempo aplicado em design rende ao longo da vida do sistema, evitando os juros compostos da complexidade.

*Veja também: [[01 - A complexidade como problema central]]*

### Quadrante de dívida técnica (Technical Debt Quadrant)
Modelo de Martin Fowler (2009) que cruza dois eixos — deliberada × inadvertida (você sabia que criava a dívida?) e prudente × imprudente (a decisão foi pensada?) — para mostrar que nem toda dívida é falha moral. Os quatro cantos canônicos: *"We don't have time for design"* (deliberada/imprudente), *"We must ship now and deal with the consequences"* (deliberada/prudente), *"What's layering?"* (inadvertida/imprudente, o pior caso) e *"Now we know how we should have done it"* (inadvertida/prudente, praticamente inevitável). Desarma o falso dilema "refatorar tudo vs. nunca refatorar".

*Veja também: [[10 - Dívida técnica]]*

### Regra do Escoteiro (Boy Scout Rule)
"Deixe o código mais limpo do que você o encontrou": toda vez que toca um arquivo, melhore-o um pouquinho. Adaptada por Robert C. Martin (Uncle Bob) no *Clean Code* (2008) a partir do lema escoteiro de Baden-Powell. É a forma mais barata de gerenciar dívida técnica — mil melhorias minúsculas no lugar do grande refator que quase nunca acontece, pagando juros antes que componham.

*Veja também: [[10 - Dívida técnica]]*

## Performance e observabilidade

### p99
Percentil 99 de uma métrica — tipicamente latência: o valor abaixo do qual ficam 99% das requisições, ou seja, apenas 1% é mais lento que isso. Usado em SLOs e monitoramento porque médias escondem a cauda da distribuição: p50 (mediana) descreve o caso típico, enquanto p95/p99/p999 revelam a experiência dos piores casos — justamente onde pausas de GC, lock contention e cold starts aparecem.
