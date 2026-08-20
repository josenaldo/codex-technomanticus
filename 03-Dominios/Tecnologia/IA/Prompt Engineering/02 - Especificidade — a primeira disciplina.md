---
title: "02 - Especificidade — a primeira disciplina"
created: 2026-05-28
updated: 2026-06-28
type: concept
status: seedling
progress: in_progress
fase: iniciado
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

> [!question]- Perguntas de revisão
> 1. Qual é a diferença entre especificidade e verbosidade? Por que mais palavras podem tornar o prompt *pior*?
> 2. Das 7 perguntas-guia, quais são as duas que mais impactam a qualidade do output em tarefas de produção de texto?
> 3. Como você testaria empiricamente se um prompt está específico o suficiente?

## Por que especificidade vem antes de tudo

O modelo faz inferência sobre **o que você quer**. Quanto mais vago o pedido, mais espaço de inferência o modelo tem, e mais o output reverte ao prior — a média estatística do corpus de treino. Output médio é o que parece com ChatGPT genérico: estrutura previsível, abstrações seguras, nada acionável.

Especificar é **reduzir o espaço de inferência**. Você não precisa adivinhar a "frase mágica"; precisa eliminar as ambiguidades que fazem o modelo escolher um caminho médio.

### A analogia do GPS

Imagine dar um destino para o GPS: *"quero ir pra algum lugar bom"*. O GPS não consegue calcular rota — não sabe o que "bom" significa pra você: perto? barato? com vista? sem trânsito? Ele vai errar não porque é burro, mas porque o pedido não tem o suficiente para resolver a ambiguidade.

Um LLM funciona da mesma forma. Quando você diz *"melhore meu texto"*, o modelo não sabe o que "melhor" significa no seu contexto. Ele usa os defaults do corpus de treino: provavelmente mais polido, mais longo, mais formal, com introdução. Se isso não é o que você queria, a segunda iteração vai ser *"não, torna mais curto"* — que você poderia ter especificado na primeira tentativa.

O custo da vagueza não é apenas o resultado ruim — é o custo das iterações adicionais. Em produção, cada iteração é latência, tokens, e às vezes uma janela de contexto que acumula rounds desnecessários.

### O que o modelo preenche quando você não especifica

Quando dimensões ficam abertas, o modelo não fica em branco — ele escolhe. A tabela abaixo mostra os defaults típicos em modelos instruídos (Claude, GPT-4, Gemini):

| Dimensão não especificada | Default típico do prior |
|---|---|
| Audiência | Leitor geral, não especialista |
| Formato | Parágrafos, às vezes bullets |
| Tamanho | Médio-longo (o modelo "sente" que mais é mais) |
| Tom | Cauteloso, hedged, com disclaimers |
| Critério de qualidade | "Parece completo e bem estruturado" |
| O que preservar | O modelo decide o que é essencial |

Nenhum desses defaults é errado em abstrato — eles são razoáveis para a média dos pedidos. O problema é quando seu caso não é a média. Se você precisa de saída técnica para sênior, concisa, sem disclaimers, o prior do modelo está trabalhando contra você.

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

Note o que o prompt específico faz que o vago não faz: **todas as dimensões que você corrigiria na segunda iteração estão especificadas de antemão**. Tamanho (150-200 palavras). Tom (direto, sem hedging). O que cortar (introduções, frases motivacionais). Critério de sucesso (60 segundos de leitura, ação clara para segunda-feira). A segunda iteração vira desnecessária porque o espaço de inferência foi fechado.

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

Não precisa responder todas em todo prompt — mas precisa **saber** quais foram deixadas em aberto e por quê. A decisão de deixar uma dimensão aberta deve ser consciente ("estou ok com variância de tamanho aqui") não acidental ("esqueci de especificar"). Dimensões abertas acidentalmente são bugs latentes.

## Especificidade por tipo de tarefa

A tabela de perguntas-guia é universal, mas as dimensões mais críticas variam por categoria de tarefa:

### Tarefas de produção de texto (resumo, reescrita, geração)

As dimensões que mais impactam: **audiência**, **tamanho**, **tom**, **critério de sucesso**. Formato geralmente é markdown ou texto corrido — não precisa de muita especificação. O critério de sucesso é a alavanca mais subestimada: obriga o modelo a otimizar para um uso real, não para "parece completo".

### Tarefas de análise (revisão de código, avaliação de argumento, extração de informação)

As dimensões mais críticas: **o que preservar**, **o que cortar**, **formato de output**. Em análise, o risco é o modelo incluir observações genéricas que parecem relevantes mas não são. Especificar o que você *não* quer (não incluir recomendações gerais, não incluir contexto histórico, não sumarizar o que já sei) tem tanto impacto quanto especificar o que quer.

### Tarefas de classificação e extração estruturada

Dimensão crítica: **formato de output** (JSON, YAML, CSV com schema exato). Em classificação, também importa especificar como tratar casos ambíguos: o modelo deve escolher a categoria mais provável, retornar "unknown", ou retornar múltiplas com probabilidade? Sem isso, o comportamento em edge cases é imprevisível.

### Tarefas de raciocínio (debugging, planejamento, arquitetura)

Dimensão mais crítica: **critério de sucesso** + **o que deve ser preservado** (constraints do sistema real). Modelos de raciocínio (O1, R1, Claude 3.7 Sonnet) se saem melhor com especificação de constraints do que com especificação de processo. Em vez de "pense passo a passo", especifique os limites do problema: "solução deve usar apenas as tecnologias já no stack (lista), sem adicionar dependências novas".

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

### Aplicando o template ao exemplo antes/depois

Desmontando o "prompt específico" do exemplo acima em termos do template:

```
Tarefa: Reescrever texto como nota interna
  ↳ verbo: reescrever | objeto: texto | finalidade: nota interna

Audiência: time de engenharia sênior
  ↳ expertise técnica assumida → sem explicar conceitos básicos

Output:
  Formato: markdown, máximo um nível de heading
  Tamanho: 150 palavras, máximo 200

Tom: direto, sem hedging, sem frases de transição genéricas

Manter: todos os números e referências a sistemas
Cortar: introduções genéricas, frases motivacionais

Critério de sucesso: dev sênior lê em 60 segundos e sabe o que
  fazer na segunda-feira
```

Todas as 7 perguntas-guia têm resposta. Nenhuma linha é enfeite. É por isso que o output vem certo na primeira iteração.

### Como calibrar o nível de especificidade por contexto

Nem todo prompt precisa do template completo. A heurística: **especifique na proporção do custo de errar**.

- Conversa exploratória, sem consequência? Prompt curto, itere.
- Tarefa one-shot com resultado que vai ser usado? Preencha as 7 perguntas.
- System prompt de produto em produção? Preencha tudo + adicione few-shot + constraints explícitas.
- Sub-prompt em sistema agêntico? Trate como system prompt de produto — o sub-agente vai executar muitas vezes com esse prompt.

## Pitfall: especificidade ≠ verbosidade

O erro mais comum de quem aprende esta disciplina é inflar o prompt achando que mais palavras = mais especificidade. **Falso.** Prompt longo e vago é pior que prompt curto e específico:

- **Mais palavras significam mais ambiguidade superficial.** Cada adjetivo solto ("seja claro", "seja útil", "seja preciso") adiciona instrução sem critério verificável.
- **Tokens custam.** Cada token de system prompt entra em todo request ([[03-Dominios/Tecnologia/IA/Anatomia dos LLMs/06 - A janela de contexto|janela de contexto]]).
- **Instruções genéricas anestesiam.** Modelos treinaram em milhões de prompts genéricos; "seja claro e conciso" passa direto.

A regra empírica: cada linha do prompt deve responder uma pergunta-guia da tabela acima, ou ser cortada. Se você não consegue dizer qual ambiguidade aquela linha resolve, ela não está especificando — está enfeitando.

**Teste de concretude:** substitua o adjetivo por um critério mensurável. "Seja conciso" → "máximo 150 palavras". "Seja técnico" → "use terminologia de engenharia de software, sem explicar conceitos básicos". "Seja direto" → "sem frases de transição como 'é importante notar' ou 'vale ressaltar'". Se não conseguir substituir, a instrução não está especificando nada.

## Quando especificidade é insuficiente

Prompt específico cobre boa parte das tarefas one-shot. Para sistemas mais complexos, especificidade sozinha não basta — precisa compor com:

- **Roles** ([[03 - Roles e personas — escolhendo o juízo do modelo|nota 03]]) — estabelecem o juízo do modelo; o modelo pensa de forma diferente como "engenheiro de segurança" vs "PM de produto", e isso afeta o que ele prioriza, não apenas o tom
- **Few-shot examples** ([[05 - Few-shot examples — exemplos como contrato|nota 05]]) — mostram em vez de descrever; quando a especificação textual é difícil ("o tom certo"), um exemplo do output desejado diz mais que mil adjetivos
- **Constraints declarativas** ([[06 - Constraints declarativas — boundaries como engenharia|nota 06]]) — codificam limites como contrato; diferente de instruções, constraints são regras que o modelo não deve violar mesmo que julgue que violar seria melhor

Mas todas essas técnicas dependem de o pedido base já estar específico. Adicionar role num prompt vago é cargo cult; adicionar few-shot exige saber o que conta como exemplo correto. Especificidade é o piso de tudo.

### O diagnóstico de iterações excessivas

Se você está na terceira iteração de um prompt e ainda não chegou no resultado, a causa mais provável é ambiguidade não resolvida, não "o modelo não entendeu". Pergunte:

1. *Qual dimensão eu não especifiquei na primeira versão?* (Geralmente audiência ou critério de sucesso)
2. *As correções que estou fazendo na segunda e terceira iteração eram previsíveis antes de enviar?* (Se sim, eram especificáveis desde o início)
3. *Estou descrevendo o que quero, ou descrevendo o que não gostei no último output?* (Feedback negativo é menos eficiente que especificação positiva)

Esse diagnóstico é mais útil do que "iterar mais" — porque identifica o padrão de ambiguidade que vai se repetir no próximo prompt.

## Armadilhas comuns

> [!warning] Especificar o "como" em vez do "o quê"
> O erro clássico: descrever o processo que o modelo deve seguir em vez do resultado esperado. *"Primeiro analise o texto, depois identifique os pontos principais, depois resuma"* é instrução de processo. *"Resumo em 3 bullets dos pontos acionáveis, audiência C-level"* é especificação de resultado. Modelos mais capazes frequentemente ignoram scripts de processo — eles inferem o melhor processo para o resultado especificado. **Como evitar:** especifique o output, não os passos. Reserve instruções de processo para casos em que o caminho importa tanto quanto o destino (como raciocínio step-by-step em tarefas complexas).

> [!warning] Usar adjetivos sem critério de verificação
> Instruções como "seja preciso", "seja profissional", "seja útil" são vazias de conteúdo operacional. O modelo vai satisfazer qualquer uma delas com o output que já ia produzir — porque são verdadeiras por definição na auto-avaliação do modelo. Você diz "seja preciso", ele produz o output padrão e avalia: *parece preciso? sim.* A instrução não mudou nada. **Como evitar:** use a substituição de concretude: transforme cada adjetivo em critério verificável por terceiro. "Preciso" → "inclua apenas afirmações que você possa confirmar com os dados fornecidos; sinalize incerteza explicitamente". "Profissional" → "sem gírias, sem emojis, sem hedging excessivo".

> [!warning] Deixar o critério de sucesso implícito
> Sem critério explícito, o modelo otimiza para "parece bem feito" — que é a versão média do que parece bem feito no corpus de treino. Isso produz outputs que parecem completos mas não são acionáveis: introdução, desenvolvimento, conclusão, nenhuma ação clara. **Como evitar:** encerre o prompt com uma frase de critério: *"Isto está pronto quando um dev sênior sem contexto prévio lê e sabe exatamente o que fazer na segunda-feira"*. O critério não precisa ser verificável pelo modelo — ele molda o alvo do processo de geração.

## Como explicar em inglês

> "Specificity is about reducing the model's inference space. The vaguer your request, the more the model defaults to its training prior — which is the statistical average of all responses, not what you actually need. The goal isn't a longer prompt; it's a prompt where every line eliminates a real ambiguity."

| Português | English |
|---|---|
| Especificidade | Specificity |
| Espaço de inferência | Inference space |
| Prior do modelo | Model's prior / training prior |
| Audiência | Audience / target reader |
| Critério de sucesso | Success criterion |
| Verbosidade | Verbosity |
| Prompt vago | Vague prompt |
| Output acionável | Actionable output |

## O que vem a seguir

Com o pedido específico — audiência, formato, tamanho, tom, critério — o próximo nível é *de quem* o modelo está falando. Roles e personas definem o juízo que o modelo aplica ao conteúdo: não o estilo superficial, mas a perspectiva com que analisa, prioriza e pondera tradeoffs. Um prompt específico bem construído se torna muito mais poderoso quando combinado com o role certo. [[03 - Roles e personas — escolhendo o juízo do modelo]] entra nesse ponto.

## Fontes

- **@hooeem** — *Become an AI Engineer*, cap #2. Pares before/after e a leitura "specificity destrava o resto".
- **OpenAI** — *Prompt engineering guide*, seção "Write clear instructions".
- **Anthropic** — *Be clear and direct* (docs.anthropic.com/prompt-engineering).
- **Schulhoff et al.** — *The Prompt Report* ([arxiv:2406.06608](https://arxiv.org/abs/2406.06608)), seção sobre task description specificity. Categoriza "task specification" como uma das técnicas de maior impacto consistente em benchmarks de prompting — fundamenta a afirmação de que especificidade não é intuição, é técnica documentada.

## Especificidade em system prompts de produto

Quando o prompt não é usado uma vez por você, mas executado milhares de vezes pelo seu sistema, as mesmas perguntas-guia se aplicam — mas com exigência maior de completude.

System prompts de produto têm inputs imprevisíveis: usuários vão fazer perguntas que você não antecipou, fornecer contextos parciais, tentar usos fora do escopo. A especificidade aqui tem uma dimensão adicional: **robustez a inputs adversariais ou inesperados**.

Isso se traduz em:
- **Escopo explícito** — o que o assistente *faz* e o que está *fora do escopo* (com comportamento especificado para o segundo caso)
- **Tratamento de ambiguidade** — o que o modelo deve fazer quando não tem informação suficiente: pedir mais dados? Produzir o melhor output possível com aviso? Recusar?
- **Persona consistente** — a identidade do assistente não muda por pedido do usuário; isso precisa estar no system prompt, não assumido

Esses elementos são específicos de product prompting, não de prompting avulso. A diferença não é de natureza — é de completude. Todas as 7 perguntas-guia ainda se aplicam; você só precisa responder algumas delas pensando em *todos os possíveis usuários*, não apenas no seu próprio uso.

## Especificidade e o mito do "modelo que lê sua mente"

Uma das fantasias mais comuns de usuários de LLM é que modelos mais novos e maiores "entendem o que você quis dizer" mesmo quando o prompt é vago. Isso é parcialmente verdade — modelos mais capazes fazem inferências melhores sobre intenção vaga — e totalmente perigoso.

O problema não é o output médio que o modelo produz quando você foi vago. O problema é a *variância*: se você repetir a mesma tarefa vaga 50 vezes, vai obter 50 respostas diferentes em dimensões não especificadas. Para uso pessoal casual, tudo bem. Para produção — onde consistência importa, onde os outputs são processados por sistemas downstream, onde usuários esperam comportamento previsível — variância é um bug.

Especificidade reduz variância. Não até zero (o modelo ainda tem stochasticity interna), mas reduz para o range que você toleraria. Essa é a razão técnica pela qual especificidade é a primeira disciplina: ela é o controle de variância mais direto disponível antes de chegar em temperaturas, sampling params, ou structured output.

Para tarefas que exigem output 100% determinístico (como extração estruturada de dados), especificidade no prompt deve ser combinada com structured outputs ([[03-Dominios/Tecnologia/IA/Structured Outputs/index|Structured Outputs]]) — que forcam o formato via constrangimento de geração, não apenas via instrução. Mas mesmo com structured outputs, a especificidade do conteúdo (o que extrair, o que ignorar, como tratar ambiguidade) continua sendo responsabilidade do prompt.

## Resumo: o que especificidade *não* é

Para fechar o loop, o que esta disciplina explicitamente não recomenda:

- **Não é** escrever o prompt mais longo possível
- **Não é** usar jargão técnico para "parecer especialista"
- **Não é** repetir a mesma instrução de formas diferentes ("seja conciso; escreva de forma breve; não escreva muito")
- **Não é** especificar o processo interno do modelo ("pense passo a passo antes de responder") — isso pode ajudar, mas é uma técnica separada ([[Reasoning models]] e chain-of-thought)
- **Não é** adicionar frases motivacionais ("você é o melhor assistente do mundo")

Especificidade é **precisão cirúrgica nas dimensões que importam para o seu caso**, não volume de instrução.

## Veja também

- [[01 - Por que prompt engineering ainda importa]] — por que a disciplina segue de pé e como ela se posiciona dentro do AI Engineering Stack
- [[03 - Roles e personas — escolhendo o juízo do modelo]] — próximo nível, depois que a base está específica: como o framing de identidade muda o raciocínio do modelo
- [[05 - Few-shot examples — exemplos como contrato]] — quando especificação textual é difícil, exemplos mostram o alvo diretamente
- [[06 - Constraints declarativas — boundaries como engenharia]] — como codificar "manter / cortar" de forma mais robusta que instrução textual
- [[07 - Iteration patterns — keep, change, do-not]] — quando o primeiro prompt não foi específico o bastante: padrões estruturados de iteração
