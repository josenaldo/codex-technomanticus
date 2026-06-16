---
title: "Dívida de intenção"
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
  - divida-intencao
  - adr
  - rationale
---

# Dívida de intenção

A nota do hub fechou prometendo aprofundar cada uma das três dívidas, e as anteriores cobriram as duas mais antigas: a que vive no código ([[10 - Dívida técnica]]) e a que vive nas pessoas ([[11 - Dívida cognitiva]]). Esta é a terceira — a mais nova das três, e a única que nenhum agente de IA consegue pagar por você. Ela vive nos **artefatos**: nas specs, ADRs, READMEs e arquivos de contexto que registram *por que* o sistema é como é. Ou, mais frequentemente, na ausência deles. Pense num prédio cujas plantas se perderam: ele ainda fica de pé, mas ninguém ousa derrubar uma parede sem saber se ela é estrutural.

> [!abstract] TL;DR
> **Dívida de intenção** é a ausência ou erosão do **rationale externalizado** — as metas, restrições e o *porquê* das decisões — que explica por que o sistema é como é. Diferente das outras duas, ela não vive no código nem nas cabeças: vive nos **artefatos** (specs, ADRs, AGENTS.md/CLAUDE.md, não-objetivos no README, critérios de aceitação) ou na falta deles. A propriedade que a define: **só humanos geram intenção**. Um agente até *infere* um rationale plausível olhando o código, mas um palpite sobre intenção não é a intenção — é por isso que esta é a dívida que o agente não paga. E ela **compõe agora** porque cada agente começa a sessão frio: intenção não-escrita, que antes custava uma vez (no onboarding), passa a ser paga **a cada sessão, por cada agente**. Diagnostica-se com testes simples (teste dos 5 minutos, não-objetivos, ADR, linguagem ubíqua) e paga-se de um jeito só — **externalizar a intenção como artefato de primeira classe**.

## O que é

A **dívida de intenção** é a terceira peça do **Triple Debt Model** de **Margaret-Anne Storey** ([[09 - As três dívidas do software]]). A definição da fonte primária é precisa:

> [!quote] Storey, sobre a dívida de intenção
> *"Intent debt refers to the absence or erosion of explicit rationale, goals, and constraints that guide how humans and agents evolve the system."*

Repare nas duas palavras de carga: **absence** e **erosion**. A dívida não é só *nunca ter escrito* o porquê — é também ter escrito e deixado o artefato apodrecer, divergindo da intenção real até virar mentira documentada. E repare em *humans **and** agents*: o rationale precisa guiar os dois.

O traço que distingue essa dívida das outras é **onde ela mora**. A técnica vive no código; a cognitiva, nas pessoas; a de intenção, nos **artefatos**. Fowler resume o substrato em uma frase:

> [!quote] Fowler, sobre onde a dívida vive
> *"Intent debt lives in artifacts. It accumulates when the goals and constraints that should guide the system are poorly captured or maintained."*

Quais artefatos? Os que carregam o *porquê*, não o *como*: specs de intenção, **ADRs** (Architecture Decision Records), arquivos de contexto pra agentes (AGENTS.md, CLAUDE.md), a seção de **não-objetivos** do README, critérios de aceitação. Osmani aponta o lugar mais cruel — o artefato que você *nunca escreveu*:

> [!quote] Osmani, sobre o artefato ausente
> *"Intent debt lives in the artifacts you may have never wrote: the goals, constraints, and rationale for why the system is the way it is."*

O modelo é atribuído a **Storey** (paper no arXiv, 2026); **Osmani** afiou a economia da intenção, **Fowler** divulgou o substrato, e a **Developers Digest** sistematizou o diagnóstico operacional.

## A dívida que o agente não paga

Aqui está o ponto que torna esta dívida singular na era da IA — e a razão de ela ser a única das três que um agente não consegue quitar sozinho.

Um agente é ótimo pagando dívida técnica: refatora rápido, sem cansaço. Ajuda com a cognitiva: explica o código sob demanda. Mas com a intenção ele bate num muro — porque **intenção é o único input que tem de vir de você**:

> [!quote] Osmani, sobre quem gera intenção
> *"An agent can't generate intent, because intent is the one input that has to come from you."*

A distinção é sutil e decisiva. Um agente *pode* inferir um rationale plausível olhando o código — "essa guard clause deve estar aqui pra evitar divisão por zero". Mas isso é um **palpite**, não a intenção. Talvez a cláusula proteja um caso de borda regulatório que nunca foi escrito em lugar nenhum. Inferir não é recuperar: o agente fabrica uma intenção que *parece* certa e implementa a coisa errada com convicção. A Developers Digest é seca a respeito:

> [!quote] Developers Digest, sobre o que agentes leem
> *"AI agents cannot read minds or infer unwritten constraints. They read documented artifacts. If artifacts don't match actual intent, agents implement the documented wrong thing."*

E há a **economia do cold start**, o golpe que faz essa dívida compor *agora*. Times humanos absorviam intenção por osmose: conversas de corredor, code reviews, memória institucional acumulada por anos. Um agente não tem nada disso — ele começa **a sessão fria**, sem a intenção tácita que o time construiu. Osmani fecha a conta:

> [!quote] Osmani, sobre a economia da intenção
> *"Un-externalized intent used to cost you once in a while, at onboarding or after someone left. Now you pay it every session."*

Antes, intenção não-escrita era um custo raro — você pagava no onboarding de alguém novo ou quando um veterano saía. Agora você paga **a cada sessão, por cada agente**, porque cada agente é, em efeito, um colega novo que esqueceu tudo de ontem. A dívida de intenção deixou de ser custo suave (onboarding lento) e virou custo direto de throughput.

## Como diagnosticar

Como você sabe que tem dívida de intenção alta, se ela vive justamente na *ausência* de coisas? A Developers Digest propõe quatro testes rápidos. São perguntas, não métricas — e é exatamente isso que as torna úteis numa reunião.

> [!tip] Os quatro testes da dívida de intenção
> - **Teste dos 5 minutos.** Você consegue, em cinco minutos, articular pra que o sistema **serve**, pra que ele **NÃO serve**, e as **três restrições mais duras** que ele respeita? Se não, a intenção não está externalizada — está (na melhor das hipóteses) na sua cabeça.
> - **Teste dos não-objetivos.** O README diz o que o sistema **não vai fazer**? Quase nenhum diz. Não-objetivos são a parte mais barata e mais negligenciada da intenção — e a que mais protege contra "melhorias" que quebram o propósito.
> - **Teste do ADR.** Os commits **materiais** (os que mudam o significado do sistema, não os de formatação) têm um registro de decisão associado? Se decisões grandes não deixam rastro escrito, o *porquê* evaporou junto com a thread do Slack.
> - **Teste da linguagem ubíqua.** Pegue um termo-chave do domínio e peça pra **três colegas** definirem. Se as três definições divergem, não há intenção compartilhada sobre o que as palavras significam — e código construído sobre termos ambíguos herda a ambiguidade.

O fio comum dos quatro: eles testam se a intenção está **fora da cabeça**, num lugar que um colega novo — ou um agente frio — conseguiria ler. Se a resposta depende de "pergunta pro fulano", a dívida está lá.

## Como se paga

Diferente da dívida técnica, que se paga refatorando aos poucos, a dívida de intenção tem um movimento único e claro: **externalizar a intenção como artefato de primeira classe**. Não é documentação por documentação — é registrar o *porquê* no lugar onde humanos e agentes vão lê-lo. Algumas práticas concretas, destiladas das fontes:

- **Especifique a intenção, não a implementação.** A spec valiosa não descreve *como* o código faz — descreve o que o sistema deve garantir e o que ele deliberadamente não faz. Implementação muda; intenção persiste.
- **Escreva ADRs barato e agressivo.** Toda decisão material merece um registro curto: contexto, opções, escolha, consequências. Caro é *não* ter o registro quando, dois anos depois, alguém (ou um agente) for desfazer a decisão sem saber o que ela protegia.
- **Não-objetivos em todo README.** Uma seção curta de "o que isto não faz" desarma metade das regressões de propósito antes de elas acontecerem.
- **Atualize o artefato de intenção no MESMO PR que muda o significado.** Esta é a regra antierosão: se o PR muda *o que o sistema é pra ser*, ele atualiza o artefato que descreve isso — na mesma entrega. Intenção que só se atualiza "depois" nunca se atualiza.
- **Torne a intenção executável.** Intenção codificada em **testes, tipos e regras de lint no CI** não pode apodrecer em silêncio: se a intenção e o código divergem, o build quebra. É a forma mais durável de rationale — a que se autoverifica.

E há a moldura econômica de segunda ordem, registrada por Fowler e pela Developers Digest: se agentes baratearam *escrever* código, a atividade cara migra pra **verificar** se o código faz a coisa certa — e verificar exige intenção externalizada como referência. *"If coding agents make writing code cheap, verification becomes expensive."* Sem intenção escrita, não há contra o quê verificar. Osmani põe o veredito:

> [!quote] Osmani, sobre o valor do porquê
> *"Write down the why, because it's becoming the most valuable thing you can leave in the repo."*

## Em entrevista

> [!tip] Como articular a dívida de intenção
> O movimento que sinaliza senioridade é mostrar que você sabe que **as três dívidas são independentes**: dá pra ter código limpo (dívida técnica zero) *e* um time que entende o sistema (dívida cognitiva baixa) e, ainda assim, **dívida de intenção altíssima** — porque ninguém registrou o *porquê* em lugar nenhum. Frase de efeito: *"Intent is the one input an agent can't generate — it has to come from a human, so the why is becoming the most valuable thing you leave in the repo."* Se o entrevistador perguntar "como você documenta decisões?", não responda "a gente escreve docs"; responda em termos de **artefato de primeira classe**: ADRs baratos, não-objetivos no README, e a regra de ouro — *atualizar a intenção no mesmo PR que muda o significado*. E mencione o teste dos 5 minutos como ferramenta de diagnóstico: "se eu não consigo dizer em cinco minutos pra que o sistema NÃO serve, a intenção não está externalizada". É um framework de 2026 (Storey); citar a fonte mostra que você acompanha a literatura.

## Fontes

- [[02-Glosas/2026-from-technical-debt-to-cognitive-and-intent-debt|From Technical Debt to Cognitive and Intent Debt — Margaret-Anne Storey (arXiv)]] — a **fonte primária**: a definição de dívida de intenção ("absence or erosion of explicit rationale, goals, and constraints")
- [[02-Glosas/2026-the-intent-debt|The Intent Debt — Addy Osmani]] — a exposição mais clara: só humanos geram intenção e a economia do cold start
- [[02-Glosas/2026-fowler-fragments-triple-debt-model|Fragments: April 2 — Martin Fowler]] — o substrato ("intent debt lives in artifacts") e o custo da verificação
- [[02-Glosas/2026-intent-debt-the-ai-era-debt-nobody-is-tracking|Intent Debt: The AI-Era Debt Nobody Is Tracking — Developers Digest]] — os testes de diagnóstico e as práticas de pagamento

> [!note] Sobre o lastro
> O termo e o modelo são atribuídos a **Margaret-Anne Storey** (paper no arXiv, 2026); **Osmani**, **Fowler** e a **Developers Digest** o afiaram e operacionalizaram. Todas as citações em inglês são **verbatim** das seções "Citações" das glosas acima. **Ressalva honesta:** não li o paper de Storey nem os posts de Osmani/Fowler/Developers Digest na íntegra — as afirmações reproduzem com alta fidelidade o argumento e o vocabulário registrados nas glosas, mas o fraseado de partes não-citadas pode diferir do original. A atribuição (Storey; afiado por Osmani/Fowler/Developers Digest) e os quatro testes de diagnóstico estão confirmados nas glosas. Padrão de marcação seguindo [[06 - Abstrações que vazam]].

## Veja também

- [[09 - As três dívidas do software]] — o hub: dívida de intenção é uma de três (código × pessoas × artefatos)
- [[11 - Dívida cognitiva]] — a dívida-irmã que vive nas pessoas; intenção não-registrada acelera a erosão do entendimento
- [[04 - O programa como teoria]] — Naur: o programa é uma teoria na cabeça; a dívida de intenção é o que sobra quando a teoria não foi externalizada
- [[Dicionário de Fundamentos]] — verbetes do domínio
