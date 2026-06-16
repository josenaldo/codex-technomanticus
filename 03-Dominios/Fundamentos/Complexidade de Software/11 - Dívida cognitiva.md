---
title: "Dívida cognitiva"
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
  - divida-cognitiva
  - entendimento-compartilhado
---

# Dívida cognitiva

A nota do hub apresentou o tabuleiro das três dívidas e prometeu aprofundar cada peça ([[09 - As três dívidas do software]]). Esta é a do meio — a que não vive no código nem nos artefatos, mas nas **cabeças do time**. É a mais escorregadia das três, porque é a única que nenhuma ferramenta enxerga: você pode ter um repositório impecável e, ainda assim, estar à beira do precipício. Imagine uma equipe que herda um sistema antigo: tudo compila, os testes passam, mas ninguém ousa mexer numa certa parte — porque a pessoa que entendia *por que* aquilo funciona saiu há dois anos. O código está lá, intacto. O **entendimento** evaporou. Esse buraco tem nome.

> [!abstract] TL;DR
> **Dívida cognitiva** é a erosão, ao longo do tempo, do **entendimento compartilhado** que um time tem do seu sistema: o que ele faz, por que as decisões foram tomadas e como mudá-lo com segurança. É uma propriedade de **nível de projeto/time** — coletiva e temporal —, diferente da **carga cognitiva** (individual e momentânea, [[08 - Carga cognitiva e legibilidade]]) e da **dívida técnica** (que mora no código). Sua base teórica é a tese de [[04 - O programa como teoria|Naur de que um programa é uma teoria]]: dívida cognitiva é o que se acumula quando o time perde essa teoria. Código limpo e testes verdes **não** a impedem. Combate-se com **prática humana** — pairing, review, retrospectivas, documentar o porquê. O termo moderno é de Margaret-Anne Storey (2026); o fenômeno é mais velho que o nome.

## O que é

**Dívida cognitiva** é a erosão progressiva do **entendimento compartilhado** que uma equipe detém sobre o sistema que constrói e mantém. Não é o esforço de uma pessoa diante de um trecho difícil *agora* — isso é carga cognitiva. É a deterioração lenta, ao longo de meses e anos, da capacidade *coletiva* do time de responder três perguntas sobre o sistema:

- **O que** ele faz, de verdade, nas bordas e nos casos especiais.
- **Por que** está estruturado assim — quais decisões foram tomadas, contra quais alternativas, sob quais restrições.
- **Como** mudá-lo com segurança, sem quebrar invariantes que ninguém lembra mais que existem.

São exatamente as três capacidades que [[04 - O programa como teoria|Naur]] atribui a quem tem a *teoria* do programa. Por isso a definição mais precisa de dívida cognitiva é: **o que se acumula quando o time, gradualmente, perde a teoria do sistema.**

O termo moderno foi cunhado por **Margaret-Anne Storey** (2026), como uma das três peças do [[09 - As três dívidas do software|Triple Debt Model]]. Storey a define como propriedade de nível de time/projeto — "*the erosion of shared understanding across a team*". Mas o **fenômeno** é muito mais velho que o nome: todo veterano já viu um sistema "morrer" no sentido de Naur quando a equipe que o entendia se dispersou. O que Storey faz é dar nome, lugar no modelo e contraste com as outras dívidas.

> [!note] Por que é tão fácil de ignorar
> Dívida técnica deixa rastro no código — um linter fareja, uma métrica pontua, um code smell salta aos olhos. Dívida cognitiva não deixa rastro *no artefato*: ela vive na ausência de algo que está na cabeça das pessoas. Por isso ela passa despercebida até o dia em que a pessoa que detinha o entendimento sai — e o buraco aparece de uma vez. É uma dívida que você só vê quando já é tarde.

## Não confunda: as três coisas

Três termos parecidos descrevem coisas diferentes, e embaralhá-los embaralha o diagnóstico — e, portanto, o remédio. Esta é a mesma tabela das notas [[08 - Carga cognitiva e legibilidade|08]] e [[09 - As três dívidas do software|09]], porque a distinção é o eixo de tudo:

| Conceito | Onde vive | Natureza |
| --- | --- | --- |
| **Débito técnico** | no código | atalhos estruturais que cobram juros em manutenção |
| **Carga cognitiva** | no indivíduo, no momento | esforço mental exigido por uma tarefa *agora* |
| **Dívida cognitiva** | na mente coletiva, ao longo do tempo | erosão do entendimento compartilhado em nível de projeto |

A linha que separa os dois "cognitivos" é **eixo e escala**. Carga cognitiva é *individual* e *instantânea*: o esforço que *você* gasta pra entender *este* trecho *agora* ([[08 - Carga cognitiva e legibilidade]]). Dívida cognitiva é *coletiva* e *temporal*: a erosão, ao longo do tempo, da teoria que o *time* compartilha.

A consequência prática é que você ataca um sem mexer no outro. **Refatorar um nome ruim** baixa a carga cognitiva de quem lê amanhã — mas não reconstrói sozinho o entendimento que o time perdeu. E o inverso é o mais perigoso: um sistema com **código impecável** (carga baixa por trecho, dívida técnica zero) pode estar afundado em dívida cognitiva, porque a teoria do conjunto se dissolveu. Limpeza de código não compra entendimento de time.

> [!note] Remédio errado pra doença errada
> Quando alguém diz "esse código tem carga cognitiva alta", está falando de uma *experiência de leitura* — solúvel com legibilidade. Quando diz "estamos com dívida cognitiva", está falando de uma *perda organizacional de entendimento* — solúvel com práticas de time. Tratar o segundo como se fosse o primeiro ("é só refatorar os nomes") é gastar energia no lugar errado enquanto o problema real cresce.

## A base teórica: a teoria do programa

Dívida cognitiva não é um conceito solto de 2026 — ela tem raiz teórica funda, em **Peter Naur** ([[04 - O programa como teoria]], 1985). A tese de Naur é que programar não é produzir *texto* (código), e sim **construir uma teoria**: um conhecimento em grande parte tácito, na cabeça de quem desenvolve, que permite mapear o programa ao mundo, justificar sua estrutura e evoluí-lo com coerência. Código e documentação são externalizações *parciais* dessa teoria — nunca a substituem.

O corolário de Naur é a chave: **um programa "morre" quando a equipe que detém sua teoria se dispersa.** O que sobra é texto — ainda executa, mas quem não tem a teoria só consegue fazer remendos que não se encaixam no design, degradando o sistema. Reviver o programa não é ler a documentação: é **reconstruir a teoria**, trabalho lento e caro que só pessoas fazem.

Dívida cognitiva é exatamente esse morrer, em câmera lenta e em parcelas. Não é o evento binário "a equipe se dispersou"; é a erosão contínua que leva até lá — cada pessoa que sai, cada decisão cujo porquê não foi registrado, cada parte do sistema que vira terra de ninguém. É por isso que **código limpo e testes verdes não impedem dívida cognitiva**: eles atestam o *texto*, e o texto nunca foi a teoria. Você pode ter o artefato perfeito e ter perdido a capacidade de raciocinar sobre ele.

> [!tip] A analogia da cidade
> Pense numa cidade antiga cujos engenheiros originais já morreram. As construções continuam de pé, as ruas continuam pavimentadas — o "código" está intacto. Mas ninguém sabe mais por que aquele cano passa por ali, qual muro é estrutural e qual é decorativo, o que acontece se você desviar aquele riacho. Mexer vira aposta. A cidade não ruiu; o **mapa mental** que permitia evoluí-la com segurança é que se perdeu. Dívida cognitiva é a cidade sem seus engenheiros.

## Sinais de alerta

Como a dívida cognitiva não deixa rastro no código, você a diagnostica pelo **comportamento do time**, não por uma métrica. Os sintomas são gerais — valem para qualquer stack, com ou sem IA:

> [!warning] Sintomas de dívida cognitiva acumulando
> - **Medo de mudar.** Hesitação em mexer numa parte do código porque ninguém entende direito o que ela faz — "se funciona, não toca".
> - **Conhecimento tribal concentrado.** Dependência crescente do "só fulano sabe": uma ou duas pessoas viram gargalo de qualquer mudança numa área.
> - **O sistema vira caixa-preta.** Funciona, mas o *porquê* das decisões se perdeu — ninguém consegue explicar a estrutura, só constatar que "é assim".
> - **Onboarding cada vez mais lento.** Gente nova demora mais e mais pra ficar produtiva, porque a teoria que precisa absorver não está escrita em lugar nenhum.
> - **Arqueologia constante.** Cada mudança começa com horas de "git blame" e leitura de código tentando reconstruir intenção que deveria estar clara.

Esses sinais raramente aparecem isolados — e tendem a se reforçar. Quanto menos gente entende, mais o conhecimento se concentra; quanto mais concentrado, mais lento o onboarding; quanto mais lento o onboarding, mais o sistema vira caixa-preta. É uma espiral.

## Como mitigar

A pista está na natureza do problema: dívida cognitiva é perda de **teoria compartilhada**, então o remédio é **reconstruir teoria compartilhada** — e tratá-la como algo que se mantém ativamente, não como um estado que se atinge uma vez. Nenhuma ferramenta faz isso; é trabalho humano, contínuo.

- **Espalhar a teoria entre pessoas.** Pair programming, mob programming, code review com foco em *entendimento* (não só em achar bugs), rotação de quem mexe em cada área. O objetivo é nunca deixar a teoria caber numa cabeça só.
- **Documentar o porquê, não só o quê.** O código já mostra o *quê*. O que se perde — e o que precisa ser externalizado — é o **porquê**: as decisões tomadas, as alternativas descartadas e *por que* foram descartadas, as restrições que justificam a estrutura. (Essa externalização é o tema da dívida vizinha → [[12 - Dívida de intenção]].)
- **Checkpoints de reconstrução.** Retrospectivas, sessões de knowledge-sharing, design reviews, *brown bags*. Momentos deliberados em que o time re-sincroniza o modelo mental que naturalmente diverge no dia a dia.
- **Tratar entendimento como ativo a manter.** Assim como você dedica esforço a pagar dívida técnica (refactoring), reserve esforço pra pagar dívida cognitiva. Ela não se resolve sozinha, e adiar só aumenta os juros — em forma de medo, gargalos e onboarding lento.

> [!note] Por que prevenir é mais barato que reconstruir
> Naur já alertava: reconstruir a teoria de um programa depois que ela se perdeu é caro e lento — às vezes mais caro do que reescrever. Manter o entendimento vivo enquanto a teoria *ainda existe* na cabeça das pessoas custa uma fração disso. A mitigação mais barata da dívida cognitiva é não deixá-la acumular.

## A mesma ideia, sob a lente da IA

> [!note] Fronteira: o tratamento geral × a manifestação na IA
> Esta nota trata a dívida cognitiva pela lente **geral e atemporal** — o fenômeno existe desde sempre na engenharia, muito antes da IA, e seus sinais e remédios não dependem de nenhuma tecnologia específica. A **manifestação na era da IA generativa** — como agentes que geram código mais rápido do que o entendimento estabiliza *aceleram* a dívida cognitiva, e práticas específicas como o *comprehension gate* — vive em [[03-Dominios/IA/O Lado Sombrio da IA/Débito cognitivo|Débito cognitivo]], dentro de [[03-Dominios/IA/O Lado Sombrio da IA/index|O Lado Sombrio da IA]]. As duas notas são o **mesmo conceito por lentes diferentes** e se reforçam: esta é a base atemporal, aquela é o sintoma agudo do momento. Vá pra lá pra entender por que a IA torna esta dívida mais urgente do que nunca.

## Fontes

- [[02-Glosas/2026-from-technical-debt-to-cognitive-and-intent-debt|From Technical Debt to Cognitive and Intent Debt — Margaret-Anne Storey (arXiv)]] — a **fonte primária** do termo moderno: define a dívida cognitiva como "*the erosion of shared understanding across a team*", propriedade de nível de time/projeto.

> [!note] Sobre o lastro
> O **termo moderno** "dívida cognitiva" é atribuível a **Margaret-Anne Storey** (paper no arXiv, 2026), como peça do Triple Debt Model. O **fenômeno**, porém, é muito mais antigo que o nome — está na tese de [[04 - O programa como teoria|Naur]] (1985) sobre a morte do programa e na noção folclórica de *tribal knowledge* que precede qualquer literatura formal. Toda citação em inglês é **verbatim** da seção "Citações" da glosa acima; não li o paper de Storey página a página — as afirmações reproduzem o argumento registrado na glosa com alta fidelidade, mas detalhes de fraseado podem diferir do original. Padrão de marcação seguindo [[06 - Abstrações que vazam]].

## Veja também

- [[09 - As três dívidas do software]] — o hub que enquadra as três dívidas; esta nota aprofunda a do meio
- [[08 - Carga cognitiva e legibilidade]] — o par carga (individual, momentânea) × dívida (de time, no tempo)
- [[04 - O programa como teoria]] — a base teórica (Naur): o que exatamente se perde quando há dívida cognitiva
- [[03-Dominios/IA/O Lado Sombrio da IA/Débito cognitivo|Débito cognitivo (lente IA)]] — o mesmo conceito sob a ótica da IA generativa
- [[Dicionário de Fundamentos]] — verbetes do domínio
