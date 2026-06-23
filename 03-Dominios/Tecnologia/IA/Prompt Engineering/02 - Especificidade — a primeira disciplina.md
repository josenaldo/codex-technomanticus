---
title: "02 - Especificidade — a primeira disciplina"
created: 2026-05-28
updated: 2026-05-28
type: concept
status: seedling
progress: in_progress
tags:
  - prompt-engineering
  - ia
  - especificidade
publish: true
aliases:
  - Especificidade
  - Specificity in prompts
---

# 02 - Especificidade — a primeira disciplina

> [!abstract] TL;DR
> A maior parte do ganho de qualidade em prompt vem **antes** de qualquer técnica avançada — vem de especificar quem lê, o que se espera de output, qual o limite de tamanho, qual o tom, e o que conta como sucesso. Especificidade é a primeira disciplina porque destrava todas as outras: roles, few-shot e constraints só funcionam quando o pedido já está concreto. O erro mais comum é confundir especificidade com verbosidade — prompt longo e vago é pior que prompt curto e específico.

## Por que especificidade vem antes de tudo

O modelo faz inferência sobre **o que você quer**. Quanto mais vago o pedido, mais espaço de inferência o modelo tem, e mais o output reverte ao prior — a média estatística do corpus de treino. Output médio é o que parece com ChatGPT genérico: estrutura previsível, abstrações seguras, nada acionável.

Especificar é **reduzir o espaço de inferência**. Você não precisa adivinhar a "frase mágica"; precisa eliminar as ambiguidades que fazem o modelo escolher um caminho médio.

## Before / after

Caso clássico (adaptado do @hooeem cap #2):

### Prompt vago

```
Make this better.

[texto colado]
```

O modelo não sabe: melhor pra quem? Mais curto ou mais longo? Mais formal ou mais informal? Qual é o critério de "melhor"? O output reverte ao prior — algo genericamente "polido", provavelmente mais longo, provavelmente mais cauteloso, provavelmente com mais clichês de IA.

### Prompt específico

```
Reescreva o texto abaixo como uma nota interna pra um time de
engenharia sênior. Constraints:

- Audiência: devs sênior, contexto técnico assumido
- Tamanho: 150 palavras, máximo 200
- Tom: direto, sem hedging, sem "é importante notar"
- Manter: todos os números e referências a sistemas
- Cortar: introduções genéricas, frases motivacionais
- Output: markdown com no máximo um nível de heading

Critério de sucesso: um dev sênior lê em 60 segundos e sabe o que
fazer na segunda-feira.

[texto]
```

O segundo prompt entrega resultado utilizável em 1 iteração. O primeiro tipicamente exige 3-5 rodadas de "não, mais curto", "não, menos formal", "não, sem essa intro".

## Tabela de perguntas-guia

Toda vez que você escrever um prompt, percorra esta lista antes de mandar:

| Pergunta | Por que importa |
|---|---|
| **Quem lê?** | Define vocabulário, profundidade, suposições. "Dev sênior" e "stakeholder não-técnico" exigem prosas opostas. |
| **Qual o output esperado?** | Markdown? JSON? Bullets? Tabela? Código? Ambiguidade aqui força uma segunda iteração só pra ajustar formato. |
| **Qual o tamanho?** | Limite em palavras, parágrafos, ou linhas. "Curto" não é específico; "máximo 200 palavras" é. |
| **Qual o tom?** | Direto, formal, exploratório, cético. Tom indefinido reverte ao tom médio do corpus — geralmente cauteloso e clichê. |
| **O que deve ser preservado?** | Números, citações, nomes, terminologia técnica. Sem isso, o modelo parafraseia e perde precisão. |
| **O que deve ser cortado?** | Disclaimers, intros, frases motivacionais. Sem instrução explícita, o prior empurra pra incluir. |
| **Qual o critério de sucesso?** | Frase única que descreve "isto está pronto". Força o modelo a otimizar pra um alvo, não pra "parecer bom". |

Não precisa responder todas em todo prompt — mas precisa **saber** quais foram deixadas em aberto e por quê.

## Template plug-and-play

Um esqueleto que funciona pra tarefa de produção de texto:

```
Tarefa: <verbo de ação + objeto + finalidade>

Audiência: <quem lê + nível de expertise>

Output:
- Formato: <markdown / JSON / bullets / código>
- Tamanho: <faixa concreta>
- Estrutura: <opcional: seções esperadas>

Tom: <adjetivos concretos: direto, cético, irônico, ...>

Manter: <listas do que não pode ser perdido>
Cortar: <listas do que precisa ser excluído>

Critério de sucesso: <uma frase: "isto está pronto quando...">

Input:
<conteúdo>
```

A pergunta-teste do template: se eu der esse prompt pra 5 modelos diferentes, eles produzem outputs *parecidos*? Se a variância é alta, o prompt ainda tem ambiguidade — não é o modelo que está oscilando, é você que ainda não especificou o alvo.

## Pitfall: especificidade ≠ verbosidade

O erro mais comum de quem aprende esta disciplina é inflar o prompt achando que mais palavras = mais especificidade. **Falso.** Prompt longo e vago é pior que prompt curto e específico:

- **Mais palavras significam mais ambiguidade superficial.** Cada adjetivo solto ("seja claro", "seja útil", "seja preciso") adiciona instrução sem critério verificável.
- **Tokens custam.** Cada token de system prompt entra em todo request ([[03-Dominios/Tecnologia/IA/Anatomia dos LLMs/06 - A janela de contexto|janela de contexto]]).
- **Instruções genéricas anestesiam.** Modelos treinaram em milhões de prompts genéricos; "seja claro e conciso" passa direto.

A regra empírica: cada linha do prompt deve responder uma pergunta-guia da tabela acima, ou ser cortada. Se você não consegue dizer qual ambiguidade aquela linha resolve, ela não está especificando — está enfeitando.

## Quando especificidade é insuficiente

Prompt específico cobre boa parte das tarefas one-shot. Para sistemas mais complexos, especificidade sozinha não basta — precisa compor com:

- **Roles** ([[03 - Roles e personas — escolhendo o juízo do modelo|nota 03]]) — estabelecem o juízo do modelo
- **Few-shot examples** ([[05 - Few-shot examples — exemplos como contrato|nota 05]]) — mostram em vez de descrever
- **Constraints declarativas** ([[06 - Constraints declarativas — boundaries como engenharia|nota 06]]) — codificam limites como contrato

Mas todas essas técnicas dependem de o pedido base já estar específico. Adicionar role num prompt vago é cargo cult; adicionar few-shot exige saber o que conta como exemplo correto. Especificidade é o piso de tudo.

## Fontes

- **@hooeem** — *Become an AI Engineer*, cap #2. Pares before/after e a leitura "specificity destrava o resto".
- **OpenAI** — *Prompt engineering guide*, seção "Write clear instructions".
- **Anthropic** — *Be clear and direct* (docs.anthropic.com/prompt-engineering).
- **Schulhoff et al.** — *The Prompt Report* ([arxiv:2406.06608](https://arxiv.org/abs/2406.06608)), seção sobre task description specificity.

## Veja também

- [[01 - Por que prompt engineering ainda importa]] — por que a disciplina segue de pé
- [[03 - Roles e personas — escolhendo o juízo do modelo]] — próximo nível, depois que a base está específica
- [[06 - Constraints declarativas — boundaries como engenharia]] — como codificar "manter / cortar" formalmente
- [[07 - Iteration patterns — keep, change, do-not]] — quando o primeiro prompt não foi específico o bastante
