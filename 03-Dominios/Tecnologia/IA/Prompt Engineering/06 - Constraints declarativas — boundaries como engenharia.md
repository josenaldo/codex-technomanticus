---
title: "06 - Constraints declarativas — boundaries como engenharia"
created: 2026-05-28
updated: 2026-05-28
type: concept
status: seedling
progress: in_progress
tags:
  - prompt-engineering
  - ia
  - constraints
publish: true
aliases:
  - Constraints
  - Boundaries no prompt
  - Declarative constraints
---

# 06 - Constraints declarativas — boundaries como engenharia

> [!abstract] TL;DR
> Constraints declarativas são **boundaries codificadas no prompt** — não como sugestão ("seja conciso"), mas como cláusula verificável ("máximo 200 palavras; se exceder, recomece"). Funcionam como contrato in-prompt: o modelo se autoavalia contra a cláusula antes de devolver. Esta nota cobre as 8 dimensões em que faz sentido constranger (estilo, escopo, evidência, autoridade, segurança, output, tempo, qualidade), um template plug-and-play, e a diferença crítica entre constraint declarativa (aspiracional) e [[Segurança e Guardrails|guardrail]] de sistema (imposto por código). Constraint dentro do prompt é pedido; guardrail é trava.

## O que é uma constraint declarativa

Uma constraint declarativa é uma cláusula no prompt que diz: *"você não pode X; se chegar perto de X, faça Y"*. Diferente de uma sugestão estilística, ela tem três marcas:

1. **Verificável.** O modelo (e você, ao auditar) consegue checar se foi cumprida.
2. **Acionável sob violação.** A cláusula descreve o que fazer quando a constraint não pode ser respeitada.
3. **Imperativa.** Não usa hedge ("tente", "se possível"); usa direto ("não faça", "se faltar X, faça Y").

Exemplo:

```
RUIM (sugestão estilística):
Tente ser conciso.

BOM (constraint declarativa):
Máximo 150 palavras. Se a tarefa exigir mais, devolva uma lista do
que está faltando em vez de exceder o limite.
```

A segunda tem critério, ação sob violação, e força do imperativo.

## As 8 dimensões

Cada uma cobre uma classe de constraints úteis. Não é necessário usar todas em todo prompt — é necessário **saber** quais foram deixadas em aberto.

### 1. Style (estilo)

Tom, vocabulário, registro. Constrains o "como" do output.

```
Style: direto, sem hedging. Sem "é importante notar". Sem disclaimers
no início. Sem frases motivacionais no fim.
```

### 2. Scope (escopo)

O que está dentro e fora do que pode ser respondido. Constrains a fronteira da tarefa.

```
Scope: responda apenas perguntas técnicas sobre o código fornecido.
Se a pergunta for sobre estratégia de negócio ou time, responda
"fora do escopo" e pare.
```

### 3. Evidence (evidência)

Como afirmações devem ser justificadas. Constrains o suporte de cada claim.

```
Evidence: toda afirmação numérica deve vir com a fonte. Se você
inferiu o número, marque como "[inferido, baixa confiança]". Se não
sabe, escreva "não sei".
```

### 4. Authority (autoridade)

Qual a fonte de verdade quando há conflito. Constrains hierarquia de evidência.

```
Authority: se a documentação fornecida contradiz seu conhecimento de
treino, prefira a documentação. Marque divergências como "[doc
contradiz prior]".
```

### 5. Safety (segurança)

Limites de conteúdo, áreas proibidas. Constrains o que **não** entra no output.

```
Safety: não inclua exemplos com dados pessoais reais. Não cite IPs,
emails ou nomes próprios fora do escopo técnico. Se o input contém
PII, faça redaction antes de citar.
```

### 6. Output (formato)

Estrutura concreta da resposta. Constrains o formato do payload.

```
Output: markdown com no máximo dois níveis de heading. Sem tabelas
HTML. Sem code fences vazios. Se devolver código, sempre com
language tag na fence.
```

### 7. Time (tempo)

Faixa temporal válida de informação. Constrains o horizonte temporal.

```
Time: trate como referência apenas eventos anteriores a janeiro de
2026. Se a pergunta envolve evento posterior, responda "fora da
janela de conhecimento".
```

### 8. Quality (qualidade)

Critério único pelo qual o modelo se autoavalia antes de devolver. Constrains o standard.

```
Quality: a resposta está pronta quando um leitor sênior consegue
agir nela sem precisar perguntar. Se você não tem certeza de que
isso vale, marque "[incerto: <razão>]" e devolva.
```

## Template plug-and-play

Um esqueleto que cobre as dimensões principais:

```
Constraints:
- Style: <constraint de tom>
- Scope: <fronteira do que responder>
- Evidence: <padrão de justificação>
- Output: <formato concreto>
- Quality: <critério de "pronto">

Do not:
- <proibição 1 verificável>
- <proibição 2 verificável>
- <proibição 3 verificável>

If you cannot comply:
- <comportamento sob violação: ask back / flag and proceed / stop>
```

A seção *"If you cannot comply"* é frequentemente esquecida e é a mais importante. Sem ela, o modelo entra em modo "vou tentar do meu jeito" — geralmente diluindo a constraint.

### Exemplo preenchido

```
Constraints:
- Style: direto, técnico, sem hedging
- Scope: apenas o código do diff fornecido
- Evidence: cada problema apontado deve referenciar linha exata
- Output: markdown com headings ## para cada problema; bullets
  para detalhes
- Quality: pronto quando um dev sênior sabe o que mudar na próxima
  rodada

Do not:
- Não recomendar refatorações fora do diff
- Não usar a palavra "consider" — diga "faça" ou "não faça"
- Não elogiar o código antes de apontar problema

If you cannot comply:
- Se o diff é vago demais pra análise, devolva uma única pergunta
  que destrava a revisão. Não tente revisar parcialmente.
```

## Diferença vs guardrails de sistema

A confusão mais comum: tratar constraint declarativa como se fosse guardrail. **Não é.**

| Constraint declarativa | Guardrail de sistema |
|---|---|
| Vive no prompt | Vive em código fora do modelo |
| Pedido ao modelo | Trava imposta independente do modelo |
| Pode ser ignorada pelo modelo | Não pode ser ignorada |
| Auditável só via output | Auditável determinísticamente |
| Não-bloqueante | Bloqueante (mata request, faz rerun) |
| Custa tokens | Não custa tokens |

Casos:

- *"Não cite PII"* como constraint = pedido. O modelo pode falhar.
- *"Não cite PII"* como guardrail = regex que valida output e bloqueia se encontrar padrão de email/CPF/etc.

A regra prática: **constraints declarativas são para comportamento de qualidade; guardrails são para violações inaceitáveis.** Use ambas em camadas — constraint no prompt sobe a probabilidade de o modelo cumprir; guardrail garante que, se falhar, não vaza.

Ver [[Segurança e Guardrails]] para o lado deterministic. Ver [[03-Dominios/Tecnologia/IA/AI Engineering Stack/03 - Prompt Layer|Prompt Layer]] vs [[AI Engineering Stack]] (Guardrail Layer, layer 10) para a separação de camadas.

## Pitfall: constraints contraditórias

Constraints empilhadas que se contradizem destroem o output:

```
RUIM:
- Seja completo e detalhado
- Máximo 100 palavras
- Cubra todos os aspectos
```

O modelo escolhe uma — geralmente a mais saliente — e ignora a outra. Antes de despachar o prompt, releia as constraints como conjunto. Se duas se contradizem, decida qual fica e qual cai.

## Pitfall: constraints sem critério

```
RUIM:
- Seja claro
- Seja conciso
- Seja útil
```

Zero informação. O modelo já tenta isso por default. Constraints assim só ocupam tokens sem mover comportamento. Substitua por critérios verificáveis ("máximo 150 palavras", "sem hedging", "sem disclaimers no início").

## Pitfall: constraint que vira mantra

Repetir a mesma constraint em três variações ("seja direto, sem hedging, sem rodeios") não reforça — confunde. Diga uma vez, com critério.

## Quando constraints não bastam

Mesmo bem escritas, constraints são pedidos. Quando o custo de violação é alto:

- **Eleve a guardrail.** Vira validação determinística pós-LLM.
- **Combine com few-shot.** Exemplos que demonstram o comportamento constrangido sobem muito a aderência.
- **Considere fine-tuning.** Se a mesma constraint precisa ser cumprida em 100% das chamadas, talvez seja sinal de que pertence ao próprio modelo.

## Fontes

- **@hooeem** — *Become an AI Engineer*, cap #8. Origem do framing "8 dimensões" e template Constraints/Do-not/If-cannot.
- **Anthropic** — *Provide system prompts with detailed instructions* (docs.anthropic.com).
- **OpenAI** — *Prompt engineering guide*, seção "Specify the steps".
- **Anthropic** — *Building safer LLM systems* (docs.anthropic.com/safety). Distinção constraint vs guardrail.

## Veja também

- [[Segurança e Guardrails]] — onde guardrails determinísticos vivem
- [[03-Dominios/Tecnologia/IA/AI Engineering Stack/03 - Prompt Layer|AI Engineering Stack — Prompt Layer]] — constraint declarativa como parte do template de camada
- [[03 - Roles e personas — escolhendo o juízo do modelo]] — role + constraints são complementares
- [[04 - O mega-prompt do Karpathy — anatomia da anti-sycophancy]] — prompt saturado de constraints declarativas
- [[09 - Anti-patterns e tells de IA — o que evitar]] — constraints como bloqueio explícito de clichês
