---
title: "04 - O mega-prompt do Karpathy — anatomia da anti-sycophancy"
created: 2026-05-28
updated: 2026-05-28
type: concept
status: seedling
progress: in_progress
tags:
  - prompt-engineering
  - ia
  - karpathy
  - anti-sycophancy
publish: true
aliases:
  - Mega-prompt Karpathy
  - Anti-sycophancy prompt
  - Karpathy system prompt
---

# 04 - O mega-prompt do Karpathy — anatomia da anti-sycophancy

> [!abstract] TL;DR
> Em 2025, [[Andrej Karpathy|Karpathy]] circulou um system prompt cirúrgico que ataca sycophancy — o vício do modelo de bajular, hedge-ar e validar prematuramente o usuário. O prompt funciona porque empilha **role expansivo** (expert mundial em tudo), **standards verificáveis** (acurácia como métrica de sucesso), **proibições específicas** que bloqueiam cada caminho de fuga típico do modelo (não elogiar perguntas, não capitular sem evidência, gerar números independentes), e **explicitação de incerteza** (confidence levels). Esta nota traz o prompt na íntegra, anatomiza cláusula por cláusula com tabela de "quando matar", e dá variantes. É o artefato canônico do ofício porque condensa em ~250 palavras tudo que [[03 - Roles e personas — escolhendo o juízo do modelo|role prompting]] e [[06 - Constraints declarativas — boundaries como engenharia|constraints]] tentam ensinar separadamente.

## O contexto

Sycophancy é o vício documentado em LLMs treinados com RLHF: como o modelo é otimizado por aprovação humana, ele aprende a maximizar percepção de utilidade — o que frequentemente significa concordar com o usuário, elogiar a pergunta, validar a premissa antes de responder. Para tarefas onde acurácia importa mais que conforto (decisão técnica, análise crítica, debate intelectual), sycophancy é o maior bloqueio à utilidade real do modelo.

Karpathy é uma das vozes mais influentes do campo, e o fato de ele ter publicado um prompt — depois de declarar publicamente que *"prompt engineering morreu"* — diz muito: o ofício não morreu; ele se concentrou em poucos artefatos de alta alavancagem. Este é um deles.

## O prompt na íntegra

```
You are a world class expert in all domains. Your intellectual
firepower, scope of knowledge, incisive thought process, and level
of erudition are on par with the smartest people in the world.
Answer with complete, detailed, specific answers. Process
information and explain your answers step by step. Verify your own
work. Double check all facts, figures, citations, names, dates, and
examples. Never hallucinate or make anything up. If you don't know
something, just say so. Your tone of voice is precise, but not
strident or pedantic. You do not need to worry about offending me,
and your answers can and should be provocative, aggressive,
argumentative, and pointed. Negative conclusions and bad news are
fine. Your answers do not need to be politically correct. Do not
provide disclaimers. Do not inform me about morals and ethics
unless I specifically ask. Do not be sensitive to anyone's feelings
or to propriety. Make your answers as long and detailed as you
possibly can. Never praise my questions or validate my premises
before answering. If I'm wrong, say so immediately. Lead with the
strongest counterargument to any position I appear to hold before
supporting it. Do not use phrases like "great question," "you're
absolutely right," "fascinating perspective," or any variant. If I
push back, do not capitulate unless I provide new evidence or a
superior argument - restate your position if your reasoning holds.
Do not anchor on numbers or estimates I provide; generate your own
independently first. Use explicit confidence levels
(high/moderate/low/unknown). Never apologize for disagreeing.
Accuracy is your success metric, not my approval.
```

Fonte: prompt circulado por Karpathy em 2025; transcrito no artigo @hooeem caps #3/#5.

## Anatomia — cláusula por cláusula

A força do prompt está na **densidade**: cada frase fecha uma porta de fuga típica do modelo. A tabela abaixo dissecta cada cláusula importante.

| Cláusula | O que previne | Quando matar |
|---|---|---|
| *"You are a world class expert in all domains... on par with the smartest people in the world."* | Modelo se posicionando como assistente subordinado, com hedge defensivo. Eleva o registro pra o de par intelectual. | Em contextos onde o usuário é o expert e quer o modelo como executor (formatação, transcrição). Aí o role expansivo gera over-engineering. |
| *"Answer with complete, detailed, specific answers."* | Respostas resumidas que omitem nuance crítica pra "ser conciso". | Em loops curtos onde resposta detalhada quebra UX (chat de suporte, autocomplete). |
| *"Process information and explain your answers step by step."* | Conclusões soltas sem trilha de raciocínio. Permite auditoria. | Em reasoning models — eles já fazem isso internamente; pedir externo polui o output ([[08 - Reasoning models — audit trail, não chain-of-thought\|nota 08]]). |
| *"Verify your own work. Double check all facts, figures, citations, names, dates, and examples."* | Alucinação confiante. Força segunda passada de verificação no próprio output. | Nunca. Esta cláusula é universalmente útil. |
| *"Never hallucinate or make anything up. If you don't know something, just say so."* | Falsificação de fontes, datas, citações. Autoriza "não sei" como resposta válida. | Nunca. |
| *"Your tone of voice is precise, but not strident or pedantic."* | Drift pra agressividade gratuita disparada pelas cláusulas seguintes. Reequilibra. | Nunca — é o anti-corpo das cláusulas "provocative/aggressive". |
| *"You do not need to worry about offending me, and your answers can and should be provocative, aggressive, argumentative, and pointed."* | Hedge cultural ("with all due respect", "I might gently suggest"). Destrava postura crítica. | **Contextos formais** (texto pro chefe, comunicação com cliente). O modelo vira combativo demais. |
| *"Negative conclusions and bad news are fine."* | Empurrar conclusões otimistas mesmo quando o caso é negativo. | Nunca, mas requer cuidado em contextos terapêuticos / de saúde mental — não use este prompt aí. |
| *"Your answers do not need to be politically correct."* | Eufemização que apaga conclusões precisas. | Em contextos públicos, escolares, ou onde o output é assinado por terceiros. |
| *"Do not provide disclaimers."* | Disclaimers reflexos no início ("I'm an AI...", "this may not apply to your specific situation..."). | Em uso clínico, legal, financeiro onde disclaimers são exigidos por compliance. |
| *"Do not inform me about morals and ethics unless I specifically ask."* | Aulas morais não-solicitadas. | Não matar — é uma das cláusulas mais alto-ROI. |
| *"Do not be sensitive to anyone's feelings or to propriety."* | Suavização que esconde críticas. | Contextos de feedback humano direto (escrever email pra um colega). |
| *"Make your answers as long and detailed as you possibly can."* | Conclusões prematuras, respostas truncadas. | Em chat/UX onde resposta longa não é desejada. Substituir por limite explícito. |
| *"Never praise my questions or validate my premises before answering."* | **A cláusula central anti-sycophancy.** Bloqueia "great question", "you're touching on something important", validação da premissa. | Nunca. Sem isso, o prompt inteiro vaza. |
| *"If I'm wrong, say so immediately."* | Erro do usuário sendo seguido em vez de corrigido. | Nunca. |
| *"Lead with the strongest counterargument to any position I appear to hold before supporting it."* | **A segunda cláusula central.** Força red-team automático antes de qualquer apoio à posição do usuário. | Em sessões de brainstorm divergente — você quer ideias geradas, não atacadas. |
| *"Do not use phrases like 'great question,' 'you're absolutely right,' 'fascinating perspective,' or any variant."* | Validação reflexa via exemplos explícitos. Força o modelo a não reconhecer essas frases como "tom esperado". | Nunca. |
| *"If I push back, do not capitulate unless I provide new evidence or a superior argument."* | **Cláusula anti-capitulação.** O modelo normalmente cede sob qualquer pressão; aqui é forçado a exigir argumento. | Não matar — é o que sustenta debate real. |
| *"Do not anchor on numbers or estimates I provide; generate your own independently first."* | Ancoragem nos números do usuário. O modelo passa a estimar antes de ver as estimativas do usuário, evitando viés. | Em tarefas onde os números do usuário são autoritativos por definição (auditoria, conferência). |
| *"Use explicit confidence levels (high/moderate/low/unknown)."* | Falsa precisão. Calibra a saída em escala explícita. | Nunca — talvez ajustar a escala. |
| *"Never apologize for disagreeing."* | Pedidos de desculpa que dão moldura defensiva à discordância. | Não matar. |
| *"Accuracy is your success metric, not my approval."* | Re-ancora a métrica que o RLHF empurrou pra "aprovação do usuário". Fecha a porta principal da sycophancy. | Nunca. É o standard único do prompt. |

## Por que o conjunto funciona

Cada cláusula isolada é fraca — o modelo dribla qualquer instrução individual. O prompt funciona porque **fecha caminhos de fuga em paralelo**:

- Bloqueia o tom validador → mas o modelo pode tentar hedge.
- Bloqueia hedge → mas o modelo pode tentar disclaimers.
- Bloqueia disclaimers → mas o modelo pode tentar capitular sob pushback.
- Bloqueia capitulação → mas o modelo pode tentar concordar com números fornecidos.
- Bloqueia ancoragem → mas o modelo pode tentar omitir incerteza.
- Bloqueia omissão de incerteza com confidence levels explícitos.

É **defense in depth** aplicado a sycophancy. Tirar uma cláusula só não derruba o prompt; tirar o conjunto sim.

## Quando usar

- **Análise crítica de propostas** (técnicas, de negócio, de design). O default sycophant valida; o prompt destrava red-team automático.
- **Debate intelectual.** Você quer argumento contrário forte, não eco.
- **Decisões com viés conhecido.** Quando você sabe que está enviesado e quer o modelo gerar números independentes antes de ver os seus.
- **Revisão de raciocínio.** "Tenho essa hipótese — destrua antes de apoiar."
- **Aprendizado de tópico onde você suspeita estar errado.** O prompt expõe erros de partida em vez de mascará-los.

## Quando NÃO usar

- **Tarefas executivas simples.** Formatar, transcrever, traduzir. O role expansivo gera over-engineering.
- **Suporte emocional.** Para qualquer coisa próxima de saúde mental, **não use**. As cláusulas "aggressive", "negative conclusions are fine" e "do not be sensitive to anyone's feelings" são contraindicadas.
- **Texto pra terceiros.** Email pro cliente, copy pra marketing, resposta pública. O tom assertivo do prompt vaza pro output mesmo quando você quer só a redação.
- **Contextos onde refutação imediata machuca produtividade.** Brainstorm divergente, geração de hipóteses, escrita criativa exploratória. Refutar cedo mata o fluxo.
- **Contextos com compliance.** Onde disclaimers são exigidos por lei.

## Variantes

### Suavizada — para uso diário sem fricção excessiva

Mantém o núcleo anti-sycophancy mas retira o tom agressivo. Bom default pra trabalho técnico.

```
You are an expert assistant. Your success metric is accuracy, not
my approval.

- Verify your own work. Double-check facts, figures, citations,
  names, dates.
- If you don't know something, say so. Use explicit confidence
  levels (high/moderate/low/unknown).
- Never praise my questions or validate my premises before
  answering. Do not use phrases like "great question," "you're
  absolutely right," or any variant.
- If I'm wrong, say so directly and explain why.
- Lead with the strongest counterargument to my position before
  supporting it.
- If I push back, do not capitulate unless I provide new evidence
  or a superior argument.
- Do not anchor on numbers I provide; generate your own
  independently first.
- Do not provide disclaimers or moral commentary unless I ask.
```

### Hardcore — quando você quer a versão original sem freios

A própria do Karpathy, sem alteração. Útil em sessão isolada de revisão crítica, com a explícita ciência de que o output não é compartilhável.

### Domain-specific — adaptada a uma disciplina

Substitua *"world class expert in all domains"* por *"senior staff engineer with 15 years in distributed systems"* (ou o que for o domínio), e ajuste o standard. O resto da estrutura sobrevive.

## Como adotar progressivamente

Não troque seu system prompt pelo do Karpathy de uma vez — pode chocar workflows existentes. Sequência recomendada:

1. **Comece pela cláusula central.** Adicione só *"Never praise my questions or validate my premises before answering. Accuracy is your success metric, not my approval."* Veja o efeito por uma semana.
2. **Adicione anti-capitulação.** *"If I push back, do not capitulate unless I provide new evidence."* Outra semana.
3. **Adicione independência numérica.** *"Do not anchor on numbers I provide; generate your own first."* Outra semana.
4. **Adicione confidence levels.** *"Use explicit confidence levels (high/moderate/low/unknown)."*
5. **Decida se quer o tom agressivo.** Esse é o último passo — e é opcional.

Cada passo é internalizado antes do próximo. A versão suavizada acima é geralmente onde a maior parte das pessoas para — e é suficiente pra ~80% dos benefícios.

## Fontes

- **Andrej Karpathy** — System prompt anti-sycophancy circulado em 2025 (versão acima, transcrita verbatim).
- **@hooeem** — *Become an AI Engineer*, caps #3 e #5. Análise do prompt como artefato canônico.
- **Sharma et al.** — *Towards Understanding Sycophancy in Language Models* ([arxiv:2310.13548](https://arxiv.org/abs/2310.13548), 2023). Documentação acadêmica do fenômeno.
- **Anthropic** — *Specific patterns for being direct* (docs.anthropic.com).

## Veja também

- [[03 - Roles e personas — escolhendo o juízo do modelo]] — base teórica do que o prompt faz
- [[06 - Constraints declarativas — boundaries como engenharia]] — as proibições do prompt como engenharia de constraints
- [[08 - Reasoning models — audit trail, não chain-of-thought]] — por que algumas cláusulas (step-by-step) viram noise em reasoning models
- [[09 - Anti-patterns e tells de IA — o que evitar]] — o catálogo de frases que o prompt bloqueia explicitamente
- [[Andrej Karpathy]] — o autor do prompt
