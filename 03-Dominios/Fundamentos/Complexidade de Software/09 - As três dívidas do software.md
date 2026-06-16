---
title: "As três dívidas do software"
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
  - triple-debt-model
  - dividas
  - storey
---

# As três dívidas do software

A nota anterior fechou separando carga cognitiva (individual, momentânea) de débito cognitivo (de time, ao longo do tempo) — e prometeu que o segundo era só uma de três peças ([[08 - Carga cognitiva e legibilidade]]). Esta nota apresenta o tabuleiro completo. Quando falamos que software "apodrece", costumamos pensar só no código. Mas o código é apenas um dos três lugares onde a saúde de um sistema pode se deteriorar. Há mais duas dívidas — e elas vivem fora do código, em lugares que nenhum linter alcança.

> [!abstract] TL;DR
> O **Triple Debt Model** (Margaret-Anne Storey, 2026) propõe que a saúde do software é corroída por **três dívidas que interagem mas são independentes**: a **dívida técnica** vive no **código** (atalhos de implementação que comprometem a evolução futura), a **dívida cognitiva** vive nas **pessoas** (erosão do entendimento compartilhado de um time ao longo do tempo) e a **dívida de intenção** vive nos **artefatos** (ausência do rationale, metas e restrições externalizados). São independentes: dá pra ter dívida técnica baixíssima e dívida de intenção altíssima ao mesmo tempo — código de IA limpinho, mas ninguém registrou *por quê*. O modelo surge agora porque a IA generativa baratea o código e desloca o risco do *escrever* pro *entender* e pro *saber o porquê*. Esta nota é o **hub**: ela enquadra as três e passa o bastão pras notas [[10 - Dívida técnica]], [[11 - Dívida cognitiva]] e [[12 - Dívida de intenção]].

## O que é

O **Triple Debt Model** foi articulado por **Margaret-Anne Storey** em *From Technical Debt to Cognitive and Intent Debt* (arXiv, 2026). A tese central é simples e desconfortável: a dívida técnica — o conceito que Ward Cunningham popularizou nos anos 1990 — sempre foi tratada como *a* forma de degradação do software. Mas ela é só uma das três. Storey argumenta que existem outras duas formas de dívida, historicamente subvalorizadas, que erodem a saúde de um sistema por caminhos que o código não revela.

> [!quote] Storey, sobre o modelo
> *"This article proposes a Triple Debt Model for reasoning about software health, built around three interacting debt types: technical debt in code, cognitive debt in people, and intent debt in externalized knowledge."*

A genialidade do modelo está em **separar os lugares**. Cada dívida vive num substrato diferente — código, mentes, artefatos —, tem uma natureza diferente e limita uma coisa diferente. Confundi-las (chamar tudo de "dívida técnica") é confundir o diagnóstico e, portanto, o remédio. **Martin Fowler** e **Addy Osmani** popularizaram o framework depois; a fonte primária, a que cunha e defende o modelo, é o paper de Storey.

## As três dívidas

| Dívida | Onde vive | Natureza | O que limita |
| --- | --- | --- | --- |
| **Técnica** | no **código** | atalhos de implementação que cobram juros | quão fácil é **evoluir** o sistema |
| **Cognitiva** | nas **pessoas** | erosão do entendimento compartilhado do time | quão seguro é **raciocinar** sobre o sistema e mudá-lo |
| **De intenção** | nos **artefatos** | ausência/erosão do rationale, metas e restrições externalizados | se o sistema ainda **reflete os objetivos** originais |

**Dívida técnica** é a clássica: módulos emaranhados, atalhos de deadline, abstrações erradas — escolhas de implementação que comprometem a capacidade de mudar o código no futuro. Ela mora no código, e ferramentas conseguem farejá-la (linters, métricas, code smells). É a que esta trilha já tratou de viés ao longo das notas de complexidade, e é o tema da próxima → [[10 - Dívida técnica]].

**Dívida cognitiva** mora nas cabeças do time. É a erosão, ao longo do tempo, dos modelos mentais compartilhados necessários pra raciocinar sobre o sistema e mudá-lo com segurança — a perda da [[O programa como teoria|teoria do sistema]] de Naur. Diferente da carga cognitiva (individual, do momento), é uma propriedade de **nível de time/projeto** ([[08 - Carga cognitiva e legibilidade]]). Aprofundada em → [[11 - Dívida cognitiva]].

**Dívida de intenção** mora nos artefatos — ou na sua ausência. É a falta do rationale externalizado: as metas, restrições e o *porquê* das decisões que nunca foram escritos em lugar nenhum. Osmani a define de forma certeira:

> [!quote] Osmani, sobre a dívida de intenção
> *"Intent debt lives in the artifacts you may have never wrote: the goals, constraints, and rationale for why the system is the way it is."*

Ela limita se o sistema ainda reflete o que se pretendia construir — e, na era dos agentes, o quão bem uma IA consegue evoluí-lo sem fabricar intenção. Aprofundada em → [[12 - Dívida de intenção]].

## Independentes, mas interagentes

O ponto mais importante — e o mais contraintuitivo — é que **as três dívidas são independentes**. Não é uma escada onde uma leva à outra; são três eixos ortogonais. Você pode estar bem num e péssimo noutro.

O exemplo que torna isso vívido é o do **código de IA limpo sem intenção registrada**. Imagine um agente que gera um módulo impecável: bem nomeado, testado, sem duplicação, complexidade ciclomática baixa. **Dívida técnica perto de zero.** Mas em lugar nenhum está escrito *por que* aquele módulo existe, que restrição de negócio ele protege, o que ele deliberadamente *não* faz. **Dívida de intenção altíssima.** As duas convivem no mesmo arquivo, no mesmo instante. Osmani crava:

> [!quote] As dívidas operam de forma independente
> *"An agent can't generate intent, because intent is the one input that has to come from you."*

> [!example] O sintoma clássico do descolamento
> Um agente "conserta" um bug removendo uma *guard clause* cujo propósito nunca foi registrado em nenhum artefato. O código fica mais limpo (dívida técnica caiu!), os testes passam — e três semanas depois um caso de borda que aquela cláusula protegia explode em produção. A dívida técnica diminuiu *enquanto* a dívida de intenção cobrava sua fatura. Tratar isso como "problema de código" é remédio errado pra doença errada.

Que sejam independentes não significa que não conversem. Elas **interagem**: dívida cognitiva alta dificulta enxergar a dívida técnica; dívida de intenção alta acelera a dívida cognitiva (sem o *porquê* registrado, o entendimento se dissolve mais rápido). Por isso Storey fala em *interacting debt types*, e por isso nenhuma se resolve de uma vez — todas exigem manutenção contínua.

## Por que o modelo surge agora

Por que separar três dívidas só em 2026, se a dívida técnica existe desde os anos 1990? Porque a **IA generativa mudou a importância relativa das três**. O argumento de Storey é que a IA não elimina o risco — ela o **desloca**.

Enquanto escrever código era caro, o gargalo da engenharia era a produção: o esforço se concentrava em *escrever*. A dívida técnica dominava o palco porque escrever bem era a parte difícil. A IA inverte a economia: gerar código vira barato e rápido — rápido demais pra que o entendimento humano acompanhe. O gargalo migra do *escrever* pro **entender** (dívida cognitiva) e pro **saber o porquê** (dívida de intenção).

> [!quote] Storey, sobre o deslocamento
> *"As AI generates code faster than teams can understand it, two under appreciated forms of debt accumulate: cognitive debt, the erosion of shared understanding across a team, and intent debt, the absence of externalized rationale that developers and AI agents need to work safely with code."*

Osmani adiciona o golpe econômico: a intenção não-escrita antes custava barato (você só pagava no onboarding ou quando alguém saía do time). Agora você paga **a cada sessão, por cada agente**, porque cada agente começa frio, sem a intenção tácita que humanos acumulavam em conversas de corredor. *"Un-externalized intent used to cost you once in a while... Now you pay it every session."*

> [!note] Fronteira: o lente geral × a manifestação na IA
> Este galho trata as três dívidas pela lente **geral e atemporal** — elas existiriam mesmo sem IA, e a engenharia já convivia com versões mais lentas de todas. As **manifestações específicas da era da IA** (rendição cognitiva, comprehension gate, vibe coding, como agentes fabricam intenção) vivem em [[03-Dominios/IA/O Lado Sombrio da IA/index|O Lado Sombrio da IA]], onde a [[Débito cognitivo]] já tem nota própria. Esta nota linka pra lá, mas não invade o terreno: aqui o foco é o **modelo conceitual**, não o sintoma da IA.

## Em entrevista

> [!tip] Como articular o Triple Debt Model
> Mencionar as três dívidas sinaliza julgamento sênior porque mostra que você não reduz "qualidade de software" a código limpo. Frase de efeito: *"Clean code is necessary but not sufficient — you can ship zero technical debt and still drown in intent debt if nobody wrote down the why."* Em PT: deixe explícito que a dívida técnica é a única que um linter pega, e que as outras duas (entendimento de time, rationale externalizado) só se combatem com **prática humana** — pair programming, ADRs, documentar o porquê. Se o entrevistador tocar em IA, conecte: *"AI shifts the bottleneck from writing code to understanding it and knowing the intent"* — e cite que agentes não conseguem *gerar* intenção, só humanos conseguem. É um framework de 2026, atribuível a Margaret-Anne Storey: citar a fonte mostra que você lê literatura, não só posts.

## Fontes

- [[02-Glosas/2026-from-technical-debt-to-cognitive-and-intent-debt|From Technical Debt to Cognitive and Intent Debt — Margaret-Anne Storey (arXiv)]] — a **fonte primária** do Triple Debt Model
- [[02-Glosas/2026-fowler-fragments-triple-debt-model|Fragments: April 2 — Martin Fowler]] — divulgação ("técnica → código, cognitiva → pessoas, intenção → artefatos")
- [[02-Glosas/2026-the-intent-debt|The Intent Debt — Addy Osmani]] — a independência das dívidas e a economia da intenção
- [[02-Glosas/2026-intent-debt-the-ai-era-debt-nobody-is-tracking|Intent Debt: The AI-Era Debt Nobody Is Tracking — Developers Digest]] — releitura operacional da dívida de intenção

> [!note] Sobre o lastro
> O modelo é atribuído a **Margaret-Anne Storey** (paper no arXiv, 2026); **Fowler** e **Osmani** o popularizaram. Todas as citações em inglês são **verbatim** das seções "Citações" das glosas acima. **Ressalva honesta:** não li o paper de Storey página a página — as afirmações reproduzem o argumento e o vocabulário registrados nas glosas com alta fidelidade, mas detalhes de fraseado podem diferir do original. Padrão de marcação seguindo [[06 - Abstrações que vazam]].

## Veja também

- [[10 - Dívida técnica]] — a dívida que vive no código, em profundidade
- [[11 - Dívida cognitiva]] — a dívida que vive nas pessoas, em profundidade
- [[12 - Dívida de intenção]] — a dívida que vive nos artefatos, em profundidade
- [[08 - Carga cognitiva e legibilidade]] — o par carga × débito que esta nota completa
- [[Débito cognitivo]] — a manifestação na era da IA, no Lado Sombrio da IA
- [[Dicionário de Fundamentos]] — verbetes do domínio
