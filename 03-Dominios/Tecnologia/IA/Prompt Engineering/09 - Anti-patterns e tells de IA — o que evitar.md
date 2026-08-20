---
title: "09 - Anti-patterns e tells de IA — o que evitar"
created: 2026-05-28
updated: 2026-07-03
type: concept
status: seedling
progress: in_progress
fase: iniciado
tags:
  - prompt-engineering
  - ia
  - anti-patterns
  - cultura
publish: true
aliases:
  - Tells de IA
  - Frases de ChatGPT
  - AI clichés
---

# 09 - Anti-patterns e tells de IA — o que evitar

> [!abstract] TL;DR
> - Um output gerado por LLM costuma carregar marcas reconhecíveis — frases-bandeira, estruturas previsíveis, ritmos típicos — que denunciam a origem mesmo quando o conteúdo está correto.
> - Essas marcas vêm do prior estatístico: o modelo aprendeu, em milhões de exemplos, que certas frases são "tom esperado de assistente útil".
> - Esta nota cataloga as bandeiras vermelhas mais comuns, explica por que aparecem, mostra como bloquear via constraints (no padrão de [[06 - Constraints declarativas — boundaries como engenharia|nota 06]]), e nomeia os contextos onde essas estruturas são — surpreendentemente — apropriadas.
> - A regra de ouro: não basta escrever bem; é preciso bloquear o que o modelo escreve por default.

> [!question]- O que eu preciso saber antes de ler isso?
> Esta é a nota de fechamento da trilha de Prompt Engineering. Não há pré-requisito técnico específico — mas o contexto é importante: você chegou aqui depois de aprender especificidade, role, constraints, few-shot, iteration e reasoning models. Esta nota é cultural: ela documenta o que o modelo produz por default quando os prompts anteriores não estavam ativos, e o que fazer quando o output "cheira a IA" mesmo sendo tecnicamente correto. Se você usa LLMs para produzir texto que vai assinar com o seu nome, esta nota é a mais diretamente prática das nove.

Você recebe um draft — seu, ou de alguém do time — e antes de terminar o primeiro parágrafo já sente aquele desconforto: "isso parece ChatGPT". Não é nenhum erro factual. É a cadência: a frase de abertura que poderia estar em qualquer texto sobre qualquer assunto, o hedge desnecessário na segunda linha, a lista de exatamente três itens do mesmo tamanho, o fechamento motivacional que soa a palestra TED. Nada ali está tecnicamente errado — mas nada ali soa como você. Esta nota existe para nomear esse desconforto e dar ferramenta pra resolvê-lo.

## Frases bandeira-vermelha

Catálogo curado do que costuma denunciar IA. Adaptado e expandido a partir do @hooeem cap #8.

### Aberturas que não dizem nada

- *"In today's fast-paced world..."*
- *"In the rapidly evolving landscape of [X]..."*
- *"In an era of [X], it is more important than ever to..."*
- *"With the advent of [X]..."*
- *"As we navigate the complexities of [X]..."*

**Diagnóstico:** abertura genérica que serve pra qualquer tópico. Maximiza probabilidade de continuar como "introdução de artigo".

### Hedges reflexos

- *"It's important to note that..."*
- *"It's worth mentioning that..."*
- *"It's important to remember..."*
- *"It should be noted that..."*
- *"One should consider..."*

**Diagnóstico:** hedge defensivo sem informação. Toda informação no texto é "important to note" — se é importante, fala; se não é, corta.

### A estrutura "não é X, é Y"

- *"It's not just about [A], it's about [B]"*
- *"This isn't merely [A]; it's [B]"*
- *"Far from being [A], it represents [B]"*

**Diagnóstico:** padrão retórico que o modelo usa pra parecer profundo. Funciona quando a oposição é verdadeira; vira clichê quando aplicado a tudo.

### Listas com 3 ou 4 itens equilibrados

Bullets de tamanho equivalente, abrindo todos com verbo no infinitivo ou gerúndio. **Não** é problema em si — é problema quando aparece em **todo** output, independente do conteúdo.

### Conclusões motivacionais

- *"By embracing these principles, you'll be well-equipped to..."*
- *"The journey of [X] is just beginning..."*
- *"Remember, the key to success lies in..."*
- *"With the right approach, [anything] is within reach."*

**Diagnóstico:** fechamento que substitui conclusão real por afirmação aspiracional. Marca de palestra TED em texto técnico.

### Em-dashes em excesso

Uso compulsivo de em-dash (—) pra criar pausas dramáticas dentro da frase. Não é o em-dash em si — é a **frequência**: três por parágrafo, em todos os parágrafos.

### Frases de transição genéricas

- *"That being said..."*
- *"With that in mind..."*
- *"Having said that..."*
- *"All things considered..."*

**Diagnóstico:** conectivo neutro que poderia ser cortado sem perda. Aparece pra parecer fluido.

### "Crucial", "pivotal", "vital", "paramount"

Adjetivos de intensidade emocional sobre conceitos técnicos. Tudo é "crucial" no texto de IA. Quando tudo é crucial, nada é.

### "Let's dive in" / "Let's explore"

Marcas explícitas de tutorial. Em contexto de tutorial é OK; em texto técnico ou ensaio, denuncia.

### "Game-changer", "groundbreaking", "revolutionary"

Hype como filler. Aparece em descrição de qualquer tecnologia.

### Disclaimers e ressalvas reflexas

- *"As an AI, I..."*
- *"I should mention that I may not have the most recent..."*
- *"This is just a general overview, and..."*
- *"Please consult a professional for..."* (fora de contexto que exige)

**Diagnóstico:** training de safety vazando pra texto que não pede compliance.

### "In conclusion" / "In summary"

Sinal de redação escolar. Repete o que já foi dito, sem agregar.

### "Whether you're a [X] or a [Y]..."

Frase pra cobrir audiência ampla, mas tem cara de copy de blog post de SaaS.

## Por que essas frases denunciam IA

Três mecanismos:

### 1. Probabilidade alta no corpus de treino

O modelo aprendeu de bilhões de textos da web — onde "in today's fast-paced world" é genuinamente comum como abertura de artigo. O prior estatístico empurra pra essas continuações com força. Sem instrução em contrário, o modelo segue o prior.

### 2. Lack of specificity

Frases genéricas funcionam pra qualquer tópico — é por isso que o modelo escolhe quando o prompt é vago. Especificidade no input ([[02 - Especificidade — a primeira disciplina|nota 02]]) reduz a chance dessas frases aparecerem; ambiguidade aumenta.

### 3. RLHF empurrando pra "tom esperado"

O treino com aprovação humana tende a recompensar respostas que **parecem** úteis e completas. Disclaimers, hedges e fechamentos motivacionais sinalizam "esforço" e foram historicamente recompensados. O modelo aprendeu a produzi-los por reflexo.

## Como bloquear via constraints

A nota [[06 - Constraints declarativas — boundaries como engenharia|06]] cobre o framework geral. Aqui vai um bloco "Do not" pronto pra colar em prompts onde você quer eliminar tells:

```
Avoid:
- Phrases "in today's fast-paced world", "in the rapidly evolving
  landscape", "in an era of"
- Hedges "it's important to note", "it's worth mentioning",
  "it should be noted"
- The pattern "it's not X, it's Y" as rhetorical filler
- Motivational closings ("by embracing these principles", "the
  journey is just beginning")
- Excessive em-dashes (max 1 per paragraph)
- Generic transitions ("that being said", "with that in mind")
- Hype adjectives without justification (crucial, pivotal,
  game-changer, revolutionary)
- Tutorial markers ("let's dive in", "let's explore")
- AI disclaimers ("as an AI", "I should mention I may not have...")
- "In conclusion" / "In summary" as section labels
- "Whether you're X or Y" framing
```

Esse bloco isolado, no fim de qualquer prompt de geração de texto, sobe a qualidade do output mais que muita instrução elaborada.

Essa lista vai ficar desatualizada. O conjunto de frases-bandeira evolui — algumas ficam famosas demais e modelos novos aprendem a evitá-las, outras novas surgem. Trate a lista como viva; revisite a cada release importante de modelo.

## Casos práticos: antes e depois

Duas reescritas completas, aplicando o catálogo acima a texto corrido — não só a frase isolada.

### Caso 1 — abertura de post técnico

**Original (cheio de tells):**

> "In today's fast-paced world, understanding API rate limiting is more important than ever. It's important to note that rate limiting isn't just about preventing abuse — it's about ensuring fair access for all users. Whether you're a solo developer or part of a large team, mastering this concept is crucial."

**Diagnóstico:** quatro tells na mesma abertura — cliché temporal genérico ("in today's fast-paced world"), hedge reflexo ("it's important to note"), a estrutura "não é X, é Y", fechamento de audiência ampla ("whether you're..."), e o adjetivo de intensidade ("crucial"). Zero informação técnica nas primeiras 40 palavras.

**Reescrita (sem tells):**

> "Rate limiting exists because your API has a ceiling — CPU, database connections, downstream quotas — and someone will hit it, on purpose or by accident. This post covers the three algorithms that enforce that ceiling: token bucket, sliding window, and fixed window, and when each one breaks."

**O que mudou:** a abertura começa pelo *porquê técnico* (existe um teto), não por um cliché temporal. Zero hedge, zero frase de audiência ampla. A segunda frase já entrega o índice do post — sem precisar de "crucial" ou "important" pra justificar a leitura.

### Caso 2 — fechamento de e-mail interno

**Original (cheio de tells):**

> "In conclusion, by embracing these new deployment practices, the team will be well-equipped to handle future challenges. The journey towards better DevOps is just beginning, and with the right approach, continuous improvement is within reach."

**Diagnóstico:** "in conclusion" como rótulo de redação escolar, fechamento motivacional duplo ("well-equipped", "the journey is just beginning"), e uma frase de esperança genérica ("within reach") sem nenhum próximo passo concreto.

**Reescrita (sem tells):**

> "Next sprint we move the deploy pipeline to staged rollouts — 10% of traffic, then 50%, then 100%, with automatic rollback on error-rate spike. I'll open the RFC Thursday."

**O que mudou:** o fechamento motivacional vira compromisso concreto, com número e prazo. Não há "jornada" nem "abraçar" — há uma ação datada que qualquer leitor consegue cobrar depois.

## Quando esses padrões são OK

Honestidade: nem toda estrutura "típica de IA" é ruim. Em contextos certos, estruturas previsíveis funcionam — por isso o modelo as aprendeu como default.

| Padrão | Quando é OK |
|---|---|
| Listas com 3-4 itens equilibrados | Documentação técnica, especificações, checklists |
| "In summary" / "In conclusion" | Texto longo (~2000 palavras) onde o leitor agradece o resumo final |
| Tutorial markers ("let's dive in") | Tutorial real, conteúdo educacional explícito |
| Bullets curtos e numerados | Receitas, instruções step-by-step, runbooks |
| Disclaimers | Conteúdo médico, legal, financeiro onde compliance exige |
| Motivational closing | Marketing copy onde o objetivo é mover a ação |
| Hedge ("it should be noted") | Texto acadêmico ou científico onde o hedge é norma do registro |
| "Crucial / pivotal" | Quando a coisa é genuinamente crucial — e você consegue justificar |

A diferença entre clichê e estrutura útil: **se a estrutura serve a uma audiência específica naquele contexto, é útil; se aparece independente do contexto, é clichê.**

## Como detectar tells no seu próprio workflow

Um processo simples de auditoria de output em três passos:

**Passo 1 — Escaneio de abertura e fechamento.** As frases-bandeira aparecem com frequência desproporcional no início e no fim do texto. Leia a primeira frase e a última frase. Se ambas passam pela lista de clichês, o texto provavelmente tem mais dentro.

**Passo 2 — Verificação de simetria.** Listas com exatamente o mesmo número de itens, parágrafos de comprimento idêntico, seções de peso equivalente. Se o output parece graficamente equilibrado demais, é sinal de simetria artificial.

**Passo 3 — Teste de certeza.** Leia um parágrafo técnico sobre algo que você sabe. Há afirmações que deveriam ser hedgeadas mas estão apresentadas com a mesma confiança que os fatos certos? Isso é tell de certeza homogênea.

Se o output passa esses três filtros, está na faixa aceitável. Se falha em dois ou três, há trabalho de revisão com constraints no próximo prompt.

### Fluxo de higiene: prompts que acumulam Do-nots

Com o tempo, cada projeto acumula seu próprio `Do-not` list: as frases que essa base de usuário detesta, os padrões que esse estilo editorial não tolera. Trate isso como dado de feedback de produto — não como lista fixa de tutoriais.

Exemplo de evolução de um Do-not list de newsletter técnica:
- Versão 1: bloqueia "in today's fast-paced world", "it's important to note"
- Versão 2: adiciona "game-changer", "groundbreaking"
- Versão 3: adiciona "whether you're a developer or a manager"
- Versão 6 (6 meses depois): lista de 20 itens específicos ao público daquela newsletter

Esse acúmulo é o que diferencia um produto de texto com voz consistente de um produto que parece diferente a cada output.

## A meta-regra

Os defaults do modelo vêm do prior treinado em milhões de exemplos e são fortes. Cada iteração de "está bom, mas tem cara de IA" vira cláusula nova no Do-not list do próximo prompt.

## Armadilhas comuns

> [!warning] Bloquear demais deixa o texto sem voz
> Excesso de Do-not pode produzir texto desnaturado: o modelo evita tantas estruturas que perde fluência natural. Bloqueie clichês que aparecem independente do conteúdo; deixe estruturas que servem ao contexto. Sinal de bloqueio excessivo: output muito curto, fragmentado, ou com transições estranhas porque o modelo evitou todas as transições naturais. Recue uma ou duas cláusulas do Do-not se isso acontecer.

> [!warning] Tell de IA pode ser jargão legítimo de um campo
> Algumas frases parecem clichê de IA mas são linguagem genuína de um domínio. "Pivotal moment" em texto de história é hipérbole; em análise de ponto crítico de função matemática, é terminologia precisa. "It's crucial to note" no corpo de um texto técnico médico é hedge de compliance, não tell de ChatGPT. Antes de bloquear, cheque: o uso é técnico/convencional do campo, ou é retórico/decorativo? Bloqueie só o segundo.

> [!warning] A lista de tells é viva — modelos aprendem a evitá-los
> O catálogo de frases-bandeira fica desatualizado. Quando um tell fica famoso demais, ele entra nos dados de feedback dos modelos e os modelos subsequentes aprendem a evitá-lo. Outros surgem em seu lugar. "In today's fast-paced world" ficou tão notório que modelos recentes raramente o produzem. Mas "groundbreaking" e "transformative" ainda persistem em 2025. Trate a lista como viva: revisite a cada release importante de modelo e ajuste conforme observa novos padrões.

## Anti-patterns estruturais — além das frases

Além das frases-bandeira, há anti-patterns de **estrutura** que denunciam IA:

**Simetria falsa:** o modelo tende a equilibrar tópicos artificialmente. Se você pede "vantagens e desvantagens", ele vai produzir listas de mesmo tamanho, com itens de mesmo peso — mesmo que a realidade tenha 7 vantagens fortes e 2 desvantagens menores. Simetria de layout ≠ simetria de evidência.

**Completude artificial:** o modelo tem viés pra "cobrir tudo". Um post de blog sobre um conceito simples vira tutorial completo de 2000 palavras com 10 seções. Constraint de escopo ajuda, mas o instinto de completude é forte.

**Certeza homogênea:** em texto sem instrução de uncertainty, todo parágrafo tem o mesmo grau de assertividade — o modelo apresenta especulação com a mesma confiança que fatos. Isso é tell de IA mais sutil que as frases, mas igualmente identificável por um leitor atento.

**Parágrafos de mesmo comprimento:** outputs longos tendem a ter parágrafos de 3-4 linhas uniformes, sem variação de ritmo. Texto humano tem parágrafos curtos, longos, às vezes de uma linha só. A homogeneidade é um sinal.

Esses anti-patterns estruturais não são bloqueados pela lista de frases — precisam de constraints separadas: "varie o comprimento dos parágrafos", "não equilibre listas se a evidência não é equilibrada", "use [incerto] onde você não tem certeza".

## Como explicar em inglês

Em entrevistas ou conversas sobre criação de conteúdo com IA, esta nota cobre o "como manter a voz humana":

> "The default outputs of LLMs carry statistical tells — phrases that appeared frequently in their training data and get amplified by RLHF feedback that rewarded 'helpful tone.' Blocking them requires explicit Do-not lists in the prompt. But beyond phrases, there are structural tells: symmetric lists regardless of evidence weight, artificial completeness, homogeneous confidence levels across claims. Those need structural constraints, not just lexical ones."

| Português | Inglês |
|-----------|--------|
| tell de IA | AI tell / AI giveaway |
| frases bandeira-vermelha | red-flag phrases / tell-tale phrases |
| prior estatístico | statistical prior / training prior |
| clichê | cliché / verbal filler |
| hedge reflexo | reflexive hedge / safety hedge |
| disclaimer reflexo | boilerplate disclaimer |
| simetria artificial | artificial symmetry |
| completude artificial | artificial completeness |
| voz própria | own voice / authorial voice |
| bloco Do-not | Do-not list / avoidance list |

## O que vem a seguir

Esta é a nota de fechamento da trilha de Prompt Engineering. O próximo domínio complementar são **Structured Outputs** — como forçar o modelo a produzir JSON/YAML/XML verificável em vez de prosa livre. A disciplina de anti-patterns entra no design de structured outputs: o modelo tende a adicionar explicações e disclaimers ao redor do JSON; bloquear isso via constraint é o primeiro passo do Structured Output design.

Ver o galho [[03-Dominios/Tecnologia/IA/Structured Outputs/01 - Por que structured outputs|Structured Outputs]].

## Cultura — por que essa nota existe na trilha

Esta nota é deliberadamente cultural, não técnica. A razão: assinar um texto produzido com ajuda de LLM e mantê-lo lendo como **seu** texto é uma habilidade que separa o ofício atual. Sem essa higiene, o output denuncia origem mesmo quando o conteúdo é seu. Com ela, o LLM vira ferramenta invisível.

Não é sobre esconder o uso de IA — é sobre ter voz própria que sobrevive ao uso.

### O ofício muda, o problema persiste

Em 2020, o problema era "escrever com IA parece robótico". Em 2025, o problema é "escrever com IA parece genérico". Os tells evoluem com os modelos — mas o problema de fundo é estável: o modelo escreve para uma audiência genérica, com o tom que foi recompensado em média. Isso é o oposto do que um escritor com voz faz.

A disciplina desta nota — identificar o que o modelo produz por default e substituir por escolha deliberada — é o que mantém autoria no texto mesmo quando a ferramenta é o modelo. É uma disciplina de edição, não de geração. Você usa o modelo para rascunho; você usa as constraints desta nota para trazer o rascunho de volta ao que você quis dizer.

## Fontes

- **@hooeem** — *Become an AI Engineer*, cap #8. Catálogo original das frases-bandeira, em inglês.
- **Anthropic** — *Style guidelines for Claude responses* ([docs.anthropic.com](https://docs.anthropic.com) — path específico a confirmar).
- **OpenAI** — *Writing with clarity* (community discussions e docs).
- Observação cultural pública sobre tells de ChatGPT em 2024-2025 (Twitter/X, Reddit r/ChatGPT, fóruns de redação).

## Veja também

- [[02 - Especificidade — a primeira disciplina]] — primeira linha de defesa contra clichês: especificar input bloqueia outputs genéricos
- [[06 - Constraints declarativas — boundaries como engenharia]] — onde o Do-not list mora como categoria
- [[04 - O mega-prompt do Karpathy — anatomia da anti-sycophancy]] — prompt que bloqueia frases-bandeira específicas como cláusula central
- [[07 - Iteration patterns — keep, change, do-not]] — cada tell descoberto numa iteração vira Do-not no próximo prompt
