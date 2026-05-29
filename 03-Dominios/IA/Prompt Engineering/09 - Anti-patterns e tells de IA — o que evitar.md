---
title: "09 - Anti-patterns e tells de IA — o que evitar"
created: 2026-05-28
updated: 2026-05-28
type: concept
status: seedling
progress: in_progress
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
> Um output gerado por LLM costuma carregar marcas reconhecíveis — frases-bandeira, estruturas previsíveis, ritmos típicos — que denunciam a origem mesmo quando o conteúdo está correto. Essas marcas vêm do prior estatístico: o modelo aprendeu, em milhões de exemplos, que certas frases são "tom esperado de assistente útil". Esta nota cataloga as bandeiras vermelhas mais comuns, explica por que aparecem, mostra como bloquear via constraints (no padrão de [[06 - Constraints declarativas — boundaries como engenharia|nota 06]]), e nomeia os contextos onde essas estruturas são — surpreendentemente — apropriadas. A regra de ouro: não basta escrever bem; é preciso bloquear o que o modelo escreve por default.

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

**Aviso importante:** essa lista vai ficar desatualizada. O conjunto de frases-bandeira evolui — algumas ficam famosas demais e modelos novos aprendem a evitá-las, outras novas surgem. Trate a lista como viva; revisite a cada release importante de modelo.

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

## A meta-regra

Não basta escrever bem o prompt — é preciso bloquear o que o modelo escreve por default. Os defaults são fortes; eles vêm do prior treinado em milhões de exemplos. Toda iteração de "está bom, mas tem cara de IA" deveria virar uma cláusula nova no Do-not list do próximo prompt.

E sim — esta nota foi escrita evitando ativamente cada um dos padrões catalogados. Eat your own cooking.

## Pitfall: bloquear demais e ficar sem voz

Excesso de Do-not pode produzir texto desnaturado: o modelo evita tantas estruturas que perde fluência. Equilíbrio: bloqueie clichês que aparecem **independente do conteúdo**; deixe estruturas que servem ao contexto específico.

Sinal de bloqueio excessivo: o output fica curto demais, fragmentado, ou com transições estranhas porque o modelo evitou todas as transições naturais. Recue uma ou duas cláusulas do Do-not.

## Pitfall: confundir tell de IA com tell de tópico

Algumas frases parecem clichê de IA mas são jargão genuíno de um campo. *"Pivotal moment"* em texto de história é hipérbole; em análise de ponto crítico de função, é termo técnico. Antes de bloquear, cheque se o uso é técnico ou retórico.

## Cultura — por que essa nota existe na trilha

Esta nota é deliberadamente cultural, não técnica. A razão: assinar um texto produzido com ajuda de LLM e mantê-lo lendo como **seu** texto é uma habilidade que separa o ofício atual. Sem essa higiene, o output denuncia origem mesmo quando o conteúdo é seu. Com ela, o LLM vira ferramenta invisível.

Não é sobre esconder o uso de IA — é sobre ter voz própria que sobrevive ao uso.

## Fontes

- **@hooeem** — *Become an AI Engineer*, cap #8. Catálogo original das frases-bandeira, em inglês.
- **Anthropic** — *Style guidelines for Claude responses* (docs.anthropic.com).
- **OpenAI** — *Writing with clarity* (community discussions e docs).
- Observação cultural pública sobre tells de ChatGPT em 2024-2025 (Twitter/X, Reddit r/ChatGPT, fóruns de redação).

## Veja também

- [[02 - Especificidade — a primeira disciplina]] — primeira linha de defesa contra clichês: especificar input bloqueia outputs genéricos
- [[06 - Constraints declarativas — boundaries como engenharia]] — onde o Do-not list mora como categoria
- [[04 - O mega-prompt do Karpathy — anatomia da anti-sycophancy]] — prompt que bloqueia frases-bandeira específicas como cláusula central
- [[07 - Iteration patterns — keep, change, do-not]] — cada tell descoberto numa iteração vira Do-not no próximo prompt
