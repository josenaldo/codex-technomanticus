---
title: "06 - Constraints declarativas — boundaries como engenharia"
created: 2026-05-28
updated: 2026-07-03
type: concept
status: seedling
progress: in_progress
fase: Iniciado
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

> [!question]- O que eu preciso saber antes de ler isso?
> Você já conhece especificidade ([[02 - Especificidade — a primeira disciplina]]) e roles ([[03 - Roles e personas — escolhendo o juízo do modelo]]). Constraints declarativas são a terceira alavanca do prompt design: enquanto especificidade diz *o que fazer* e role diz *com que juízo fazer*, constraints dizem *o que não fazer e o que fazer quando não conseguir*. Se já sabe o que é um system prompt e já tentou dizer ao modelo "seja conciso" sem resultado consistente, você está exatamente no problema que esta nota resolve.

## O que é uma constraint declarativa

Você diz "seja conciso" e o modelo escreve cinco parágrafos. Você diz "não fuja do escopo" e ele sugere três coisas fora dele mesmo assim. O problema não é o modelo ter ignorado a instrução — é a instrução nunca ter sido, de fato, uma constraint: era um pedido de estilo, sem critério verificável e sem cláusula do que fazer quando não dá pra cumprir.

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

### O teste da cláusula de violação

A presença da cláusula de violação — o "se não conseguir cumprir, faça X" — é o que distingue uma constraint bem-escrita de uma instrução vagamente imperativa. Pergunte de cada constraint: *o que o modelo deve fazer quando essa constraint entra em conflito com o que o usuário pediu?* Se você não sabe responder, a constraint está incompleta.

Três respostas possíveis para a cláusula de violação:
- **Devolver flag e prosseguir:** o modelo cumpre o pedido mas sinaliza a violação ("output excede 150 palavras porque a tarefa exigiu — sinalizado: [excedeu limite]").
- **Pedir clarificação:** o modelo para e faz uma pergunta que destrava a resolução da constraint.
- **Recusar e parar:** para violações de safety ou escopo, o modelo simplesmente não prossegue e explica por quê.

## As 8 dimensões

Cada uma cobre uma classe de constraints úteis. Não é necessário usar todas em todo prompt — é necessário **saber** quais foram deixadas em aberto.

> [!tip] Mínimo viável de constraints
> Para a maioria dos prompts, cobrir Style + Scope + Output já sobe muito a consistência do output. Adicione Evidence quando há risco de afirmações não fundamentadas, Safety quando há dados sensíveis, e Quality quando o critério de "pronto" é subjetivo. As dimensões Authority e Time são para casos específicos — RAG com docs externos, produtos com janela temporal explícita.

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

A confusão mais comum: tratar constraint declarativa como se fosse guardrail. **Não é.** E tratar guardrail como substituto de constraint também é erro — são camadas complementares, não alternativas.

Sem constraint declarativa, o modelo vai produzir o comportamento padrão — que pode ser muito bom, mas raramente é o comportamento exato que o produto precisa. Sem guardrail, violations do modelo chegam ao usuário sem filtro. O design correto usa constraint para elevar a probabilidade de comportamento correto, e guardrail para interceptar os casos em que o modelo falha.

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

## Armadilhas comuns

> [!warning] Constraints contraditórias se cancelam
> Constraints empilhadas que se contradizem destroem o output: "seja completo e detalhado / máximo 100 palavras / cubra todos os aspectos" é insolúvel. O modelo escolhe uma — geralmente a mais saliente — e ignora as outras. Antes de despachar o prompt, leia as constraints como conjunto. Se duas se contradizem, decida qual fica. Não espere que o modelo faça essa escolha por você.

> [!warning] Constraints aspiracionais não movem comportamento
> "Seja claro / conciso / útil" são intenções, não constraints. O modelo já tenta isso por default. Constraints sem critério verificável só ocupam tokens. Substitua por formulações concretas: "máximo 150 palavras", "sem disclaimers no início", "não use a palavra 'considere'". Se você não consegue checar se a constraint foi cumprida lendo o output, ela provavelmente não está funcionando.

> [!warning] Constraint que vira mantra dilui o efeito
> Repetir a mesma constraint em três variações ("seja direto, sem hedging, sem rodeios") não reforça — confunde e infla o prompt. Diga uma vez, com critério preciso. Se a constraint não está sendo cumprida mesmo com formulação clara, o caminho não é repetir em outras palavras — é elevar a guardrail ou adicionar um exemplo que demonstre o comportamento correto (ver [[05 - Few-shot examples — exemplos como contrato]]).

## Quando constraints não bastam

Mesmo bem escritas, constraints são pedidos. Quando o custo de violação é alto:

- **Eleve a guardrail.** Vira validação determinística pós-LLM.
- **Combine com few-shot.** Exemplos que demonstram o comportamento constrangido sobem muito a aderência.
- **Considere fine-tuning.** Se a mesma constraint precisa ser cumprida em 100% das chamadas, talvez seja sinal de que pertence ao próprio modelo.

### Hierarquia de confiança

Uma forma de raciocinar sobre quando confiar em cada mecanismo:

| Mecanismo | Confiança | Custo de violação aceitável |
|---|---|---|
| Constraint declarativa | ~70-90% aderência | Qualidade degradada |
| Constraint + few-shot | ~85-95% | Qualidade degradada leve |
| Fine-tuning | ~95-99% | Custo de dado e treino |
| Guardrail determinístico | 100% (ou falha) | Zero — violação inaceitável |

Não existe constraint declarativa com 100% de aderência. O modelo é probabilístico e vai errar em edge cases. Aceitar isso e planejar o fallback é mais honesto e mais seguro do que empilhar constraints esperando perfeição.

## Constraints em system prompts de produto

Em produtos reais, constraints vivem no system prompt e são invisíveis ao usuário. Algumas considerações práticas:

- **Constraints de escopo são as mais críticas.** Um produto de suporte técnico que responde perguntas de negócio vira risível. Scope constraint é a primeira a escrever.
- **Constraints de evidence sobem credibilidade.** Em produtos B2B com especialistas na ponta, "toda afirmação técnica vem com referência ou marcada como [inferido]" é a diferença entre confiança e desconfiança do usuário.
- **Constraints de format reduzem parsing.** Se o output vai ser parseado por código, Output constraint que força JSON/markdown estruturado evita regex hacks no código de consumo.
- **Atualizar constraints sem redesenho.** Diferente de fine-tuning, constraints no system prompt podem ser atualizadas sem nenhum processo de ML — basta editar o texto. Isso é um superpower para produtos com iteração rápida de comportamento.

## Como explicar em inglês

Em entrevistas, a distinção constraint vs. guardrail é um shibboleth — quem entende diz "constraints are in-prompt requests; guardrails are code-enforced checks outside the model." Quem não entende usa os dois termos de forma intercambiável.

Uma resposta sólida para "how do you control LLM behavior in production?":

> "I use constraints declaratively inside the prompt — stating what not to do, what format to follow, and what to do when a constraint can't be met. But constraints are requests, not guarantees. For anything critical — PII exposure, out-of-scope content, safety violations — I layer deterministic guardrails outside the model: regex checks, classifiers, or output validators that block or reroute regardless of what the model produces."

| Português | Inglês |
|-----------|--------|
| constraint declarativa | declarative constraint |
| critério verificável | verifiable criterion |
| cláusula de violação | fallback clause / violation clause |
| guardrail de sistema | system-level guardrail |
| boundary da tarefa | task boundary / scope boundary |
| comportamento padrão | default behavior |
| imperativo | imperative (not hedged) |
| escopo restrito | narrow scope |
| constraint aspiracional | vague constraint / aspirational wording |
| constraints contraditórias | conflicting constraints |

## O que vem a seguir

Você agora sabe *como dizer o que não fazer* via constraint declarativa. A próxima nota muda de perspectiva: em vez de constranger o output via declarações estáticas, **você itera o prompt** usando um loop estruturado (keep / change / do-not). Esse padrão é onde a engenharia de prompt se torna processo, não tentativa e erro.

Ver [[07 - Iteration patterns — keep, change, do-not]].

## Fontes

- **@hooeem** — *Become an AI Engineer*, cap #8. Origem do framing "8 dimensões" e template Constraints/Do-not/If-cannot.
- **Anthropic** — [Provide system prompts with detailed instructions](https://docs.anthropic.com/)
  (caminho exato da página a confirmar; domínio oficial).
- **OpenAI** — [Prompt engineering guide](https://platform.openai.com/docs/guides/prompt-engineering), seção "Specify the steps".
- **Anthropic** — [Building safer LLM systems](https://docs.anthropic.com/)
  (caminho exato da página a confirmar; domínio oficial). Distinção constraint vs guardrail.

## Veja também

- [[Segurança e Guardrails]] — onde guardrails determinísticos vivem
- [[03-Dominios/Tecnologia/IA/AI Engineering Stack/03 - Prompt Layer|AI Engineering Stack — Prompt Layer]] — constraint declarativa como parte do template de camada
- [[03 - Roles e personas — escolhendo o juízo do modelo]] — role + constraints são complementares
- [[04 - O mega-prompt do Karpathy — anatomia da anti-sycophancy]] — prompt saturado de constraints declarativas
- [[09 - Anti-patterns e tells de IA — o que evitar]] — constraints como bloqueio explícito de clichês

