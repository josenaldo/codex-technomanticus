---
title: "07 - Iteration patterns — keep, change, do-not"
created: 2026-05-28
updated: 2026-07-03
type: concept
status: seedling
progress: in_progress
fase: Iniciado
tags:
  - prompt-engineering
  - ia
  - iteration
publish: true
aliases:
  - Iteration prompt
  - Keep change do-not
  - Refining prompts
---

# 07 - Iteration patterns — keep, change, do-not

> [!abstract] TL;DR
> O modo errado de iterar um output é dizer *"try again, make it better"* — o modelo regenera às cegas, frequentemente piorando o que estava bom.
>
> O modo certo é nomear três conjuntos: **Keep** (o que estava certo e não pode mudar), **Change** (o que precisa virar X), **Do not** (o que apareceu no output anterior e não pode reaparecer).
>
> Esta nota cobre o template, quando iterar vs quando recomeçar do zero, e o sinal mais importante de que sua iteração está doente: loop infinito porque o primeiro prompt não era específico.

> [!question]- O que eu preciso saber antes de ler isso?
> Esta nota assume que você já tem prompts razoáveis (especificidade, role, constraints) e quer refinar o output sem jogar fora o que já está funcionando. O padrão Keep/Change/Do-not é um protocolo de diff: você explicita ao modelo o que manter, o que alterar, e o que bloquear. Se você ainda está no estágio de montar um prompt do zero, comece pelas notas anteriores — especialmente [[02 - Especificidade — a primeira disciplina]] e [[06 - Constraints declarativas — boundaries como engenharia]]. Iteração sem um prompt de partida razoável é só tentativa e erro mais organizada.

## Por que iteração estruturada importa

A maioria das pessoas itera por intuição: "não ficou bom, tenta de novo". O problema é que "não ficou bom" é uma avaliação total — e o modelo trata como instrução para regenerar totalmente. O que ficou ruim é substituído, mas o que ficou bom também é jogado fora.

O template Keep/Change/Do-not força explicitação: você tem que nomear o que ficou certo antes de pedir mudança. Esse ato de nomear — de articular o que você quer preservar — é também onde você descobre o que estava vago no prompt original. A iteração bem-feita é uma auditoria retroativa do prompt.

## O anti-pattern: "try again, make it better"

```
RUIM:
[output 1]
> "Try again, make it better."
[output 2 — pior em algum lugar, melhor em outro]
> "No, like the first but better."
[output 3 — agora misturando os dois e perdendo coisas]
```

O modelo não tem como saber o que estava bom no output anterior. Sem ancoragem, ele regenera **tudo** — incluindo o que estava certo. Resultado: melhora local em uma dimensão, regressão em outra. A entropia do output sobe a cada rodada.

A causa: o modelo trata cada turno como uma nova geração, não como um diff sobre a anterior. Você precisa explicitar o diff.

## O template Keep / Change / Do not

```
[output anterior está acima]

Keep:
- <coisa específica do output anterior que está certa>
- <coisa específica do output anterior que está certa>

Change:
- <dimensão A: de X para Y>
- <dimensão B: de X para Y>

Do not:
- <padrão que apareceu e não deve reaparecer>
- <padrão que apareceu e não deve reaparecer>
```

Três regras:

1. **Keep deve ser concreto.** Não "o tom geral" — sim "o segundo parágrafo, com a estatística sobre X". Quanto mais ancorado em trecho específico, melhor.
2. **Change deve ter direção.** Não "menos formal" — sim "menos formal, no mesmo registro do exemplo do mestre [[Andrej Karpathy]]" ou "menos formal: cortar 'Caro leitor' e abrir com afirmação". A mudança precisa apontar pra onde vai.
3. **Do not deve nomear o sintoma.** O ponto de "Do not" é bloquear especificamente o que apareceu e atrapalhou: "Não usar 'em conclusão'", "Não retomar a frase 'fast-paced world'".

### Exemplo

```
[output 1: artigo de 600 palavras]

Keep:
- A abertura com a estatística sobre custo (primeiro parágrafo)
- A tabela de comparação (terceira seção)
- O fechamento citando o paper de 2024

Change:
- Tom: de "consultoria" para "engenheiro com 15 anos de campo".
  Modelo: prosa do Karpathy nos posts dele.
- Tamanho: de 600 para 350 palavras

Do not:
- Não usar "in today's fast-paced world"
- Não fechar com call to action genérico
- Não reintroduzir disclaimers sobre limitações
```

A iteração 2 entrega algo utilizável. Sem o template, a iteração 2 frequentemente piora a tabela (que estava certa) e mantém o tom de consultoria (que era o problema).

## Quando iterar vs quando recomeçar

Iteração não é sempre a resposta. Quatro sinais de que recomeçar do zero é mais barato:

1. **Você está na terceira iteração e ainda não está perto.** Cada iteração adiciona ruído acumulado da história de conversa. Reset com prompt melhor.
2. **O Keep está vazio.** Se nada do output anterior vale a pena preservar, não está iterando — está produzindo do zero com prompt poluído pelo contexto anterior.
3. **As mudanças são estruturais, não locais.** "Quero outro gênero" não é iteração; é nova tarefa.
4. **O modelo perdeu o fio.** Se a iteração introduziu contradições com instruções anteriores, frequentemente é mais limpo recomeçar do que tentar des-instruir.

A regra prática: **se a segunda iteração ainda não chegou, a terceira raramente chega.** Volte ao prompt original, aplique o aprendizado de "o que estava faltando", e dispare de novo.

> [!tip] O número de iterações é um sinal de saúde do prompt
> Prompts bem-escritos raramente precisam de mais de 2 iterações para refinamento local. Se você está rotineiramente chegando à 4ª ou 5ª iteração, o gargalo não está na iteração — está na qualidade do prompt base. Invista mais no prompt original e menos no ciclo de refinamento.

### A dimensão certa do loop

Existe uma cadência empírica que os melhores praticantes convergem:

- **Iteração 1:** ajuste de estilo ou comprimento. Dura 1 rodada.
- **Iteração 2:** ajuste de profundidade ou escopo. Dura 1-2 rodadas.
- **Iteração 3+:** você está adicionando constraints ao prompt original — o que é trabalho de prompt design, não de iteração. Pare, consolide no prompt, e re-dispare.

Iterações acima de 3 são raramente mais eficientes do que parar e melhorar o prompt. Cada rodada extra polui o contexto da conversa com instruções conflitantes e aumenta a probabilidade de regressão em dimensões que estavam certas.

## Regressões e como lidar

Iteração frequentemente introduz regressão: você melhorou o tom, mas o modelo encurtou o que não deveria. Duas estratégias:

**Estratégia 1 — Keep mais granular.** Se a segunda iteração regrediu algo que você não mencionou no Keep, isso é sinal de que o Keep original era insuficiente. Na próxima rodada, adicione o item que regrediu ao Keep explicitamente.

**Estratégia 2 — Consolidar no prompt mestre.** Se a mesma dimensão regride repetidamente, ela pertence ao prompt original como constraint, não ao loop de iteração. Uma constraint permanente tem mais peso que uma instrução de iteração conversacional.

### Teste de regressão manual

Antes de aceitar o output de uma iteração, compare side-by-side com o output anterior nas dimensões que estavam certas. Perguntas úteis:
- O que estava no Keep ainda está igual?
- A mudança pedida no Change aconteceu na direção certa?
- Algo que não era nem Keep nem Change foi alterado?

Se o output regrediu em algo que estava certo e você não pediu mudança, a iteração não funcionou — repita com Keep mais específico.

## O sinal mais importante: por que você está iterando?

A pergunta de calibração mais útil é: *"Por que precisei iterar?"*

| Por que iterou | Diagnóstico | O que adicionar ao prompt original |
|---|---|---|
| Output ficou no formato errado | Constraint de Output ausente | Seção `Output:` com formato concreto |
| Tom não bateu | Role e Style constraints fracas | Role mais específico + Style constraint |
| Resposta foi superficial | Profundidade e audiência não especificados | "Para audiência de X. Profundidade: Y" |
| Modelo inventou fatos | Evidence constraint ausente | "Se não sabe, diga 'não sei'" |
| Output veio com clichês | Sem Do-not list | Adicionar [[09 - Anti-patterns e tells de IA — o que evitar\|lista de anti-patterns]] |
| Modelo saiu do escopo | Scope constraint ausente | Seção `Scope:` explícita |
| Output muito longo | Quality/Output sem limite | "Máximo X palavras" |

Iterar é normal. Iterar repetidamente pela mesma razão é sinal de prompt sub-especificado. Use cada iteração pra alimentar o prompt seguinte — transforme o aprendizado de cada ciclo em constraints permanentes.

## Armadilhas comuns

> [!warning] Iteração infinita por baixa especificidade
> O loop tóxico mais comum: prompt vago → output médio → "make it more X" → output deslizado, perdendo Y → "now bring Y back" → ping-pong. O modelo está obedecendo; o problema é que o prompt não tem alvo. Sintoma: depois de 3 iterações você não está mais perto do que queria do que estava na 1. A saída: pare, reescreva o prompt original com todas as constraints que descobriu, dispare uma única vez. Você não estava iterando — estava descobrindo o prompt que deveria ter escrito de início.

> [!warning] Keep abstrato é Keep vazio
> "Keep: o tom geral" não ancora nada — o modelo vai regenerar achando que sabe que tom é esse. Keep eficaz cita o trecho específico do output anterior ("o segundo parágrafo com a estatística de custo") ou descreve o tom por adjetivos verificáveis ("direto, sem hedging, parágrafos de 2-3 linhas"). Se você não consegue apontar para o que está certo, o Keep está vago demais para funcionar.

> [!warning] Change sem vetor vira "try again" reformulado
> "Change: melhor" ou "Change: mais natural" não são instruções — são julgamentos sem direção. Change eficaz tem um vetor: de onde, para onde. "De tom consultoria para engenheiro de campo. Modelo: prosa do Karpathy nos posts." "De 600 para 350 palavras — corte redundâncias, não os exemplos." Sem vetor explícito, o modelo regenera do zero a partir do próprio prior, o que é exatamente o anti-pattern que o template deveria evitar.

## Quando iteração é a alavanca certa

Iteração funciona melhor quando:

- **A maior parte do output está certa**, e você quer ajustar 1-2 dimensões específicas.
- **As dimensões a mudar são locais** (um parágrafo, o título, a tabela).
- **Você consegue nomear o sintoma** que apareceu e quer bloquear.
- **O custo de regenerar tudo é alto** (output longo, computação cara).

Se nenhuma dessas vale, recomeçar do zero com prompt melhor é provavelmente mais rápido.

### Keep/Change/Do-not fora da geração de texto

O template se generaliza além de texto. Exemplos de uso:

**Code review iterativo:**
```
Keep: a análise de performance nas linhas 40-60 (está correta).
Change: a seção de segurança — adicionar análise de SQL injection, não só XSS.
Do not: não sugerir renomear variáveis — já discutimos e o nome é intencional.
```

**Refinamento de schema de dados:**
```
Keep: os campos obrigatórios e a hierarquia de objetos.
Change: os tipos de campo de string para enum onde a lista é finita.
Do not: não adicionar campos novos — a schema é de output, não de input.
```

**Revisão de plano de projeto:**
```
Keep: a ordem das fases e as dependências entre elas.
Change: o timeline — fase 2 tem mais 2 semanas.
Do not: não reabrir a decisão de arquitetura da fase 1 — está fechada.
```

O padrão é o mesmo: âncoras explícitas no que não muda, vetor claro no que muda, bloqueio nomeado no que não deve aparecer.

## Maturidade do prompt design

O ciclo de maturidade de quem escreve prompts tem padrão previsível:

1. **Novato:** dispara zero-shot, itera com "tente de novo", acumula 5-10 rodadas, frustra.
2. **Intermediário:** usa Keep/Change/Do-not, chega ao resultado em 2-3 rodadas, mas repete o mesmo ciclo para cada nova tarefa.
3. **Avançado:** usa cada iteração como input para o prompt master — cada ciclo ensina algo sobre o que o prompt original deixou vago, e esse aprendizado vira constraint permanente. Novos prompts partem de um template enriquecido.

A diferença entre intermediário e avançado não é velocidade — é a direção do aprendizado. O intermediário fica melhor em iterar; o avançado fica melhor em não precisar iterar.

## Iteração em sistemas de produção

Em sistemas de produto com usuários reais, iteração acontece em dois tempos distintos:

**Iteração de desenvolvimento (offline):** você muda o prompt e re-testa contra um conjunto de exemplos fixos. O template Keep/Change/Do-not aqui se torna um protocolo de version control de prompt: você documenta o que mudou e por quê a cada versão. Sem esse log, você não sabe o que causou uma melhoria ou regressão.

**Iteração em tempo real (conversa multi-turn):** o usuário está iterando o output dentro da conversa. Nesse caso, o modelo recebe o histórico e o usuário espera que "make it shorter" não toque no que estava certo. O template pode ser ensinado ao usuário ou embutido no system prompt como instrução de refinamento: *"Quando o usuário pedir ajuste, interprete como: manter o que não foi mencionado, mudar apenas o que for especificado."*

### Iteração como forma de aprendizado de prompt

Cada ciclo de iteração é uma sessão de descoberta sobre o que o prompt original deixou em aberto. Se você mantém um log de iterações, o padrão que emerge é uma lista de constraints ausentes no prompt v1. As melhores equipes de engenharia de prompt retroalimentam esse log no template de prompt do sistema — transformando iteração reativa em prompt design proativo.

### Version control de prompts

Em sistemas de produção, prompts mudam ao longo do tempo. Sem version control, você perde rastreabilidade — não sabe o que causou uma melhoria (ou regressão). Um log simples por versão:

```
Prompt v1 → v2: Change: tom de consultoria para técnico. Resultado: saiu mais direto mas perdeu profundidade.
Prompt v2 → v3: Keep: linguagem técnica. Change: adicionar profundidade em seção de análise. Do not: clichê "em conclusão".
```

Esse log é a forma de transformar iteração ad-hoc em processo replicável. Sem ele, o time repete os mesmos erros em cada novo prompt que escreve.

## Quando iterar output vs quando iterar prompt

Há uma distinção importante entre dois tipos de iteração:

**Iteração de output:** você está refinando o output atual de uma tarefa específica. O template Keep/Change/Do-not é o instrumento. Você não toca no prompt — só no turno de conversa.

**Iteração de prompt:** você está melhorando o prompt base para gerar melhores outputs nas próximas instâncias da mesma tarefa. Aqui o resultado do ciclo não vai para a conversa — vai para o prompt master.

A armadilha comum: usar iteração de output como substituto de iteração de prompt. Você refina o output hoje, mas amanhã o mesmo problema reaparece com um input diferente. Se você está resolvendo o mesmo tipo de problema repetidamente em iteração de output, o problema pertence ao prompt.

Sinal de transição: se a mesma cláusula de Change ou Do-not aparece em 3 outputs diferentes, ela virou constraint permanente — coloque no prompt, não na iteração.

## Template aplicado: checklist antes de iterar

Antes de enviar uma instrução de iteração, passe por esse checklist:

- [ ] Identifiquei o que está certo e precisa ser preservado (Keep concreto)?
- [ ] Identifiquei a mudança com direção clara, não só julgamento (Change com vetor)?
- [ ] Nomeei o padrão que apareceu e não deve reaparecer (Do-not com sintoma)?
- [ ] Estou na primeira ou segunda iteração? (Se terceira, considere reset.)
- [ ] O que estou mudando é local ou estrutural? (Se estrutural, é nova tarefa.)
- [ ] A iteração vai no output atual ou deveria ir para o prompt master?

## Como explicar em inglês

Em entrevistas, o padrão Keep/Change/Do-not pode aparecer como parte de uma pergunta mais ampla sobre "how do you refine prompts iteratively without losing what's working?":

> "I use a structured diff approach. After each generation I explicitly label what to keep — anchoring it to specific text, not abstract qualities — what to change, with direction rather than just a judgment, and what to block, naming the specific pattern that appeared and shouldn't recur. This way the model regenerates only what needs to change, instead of throwing away everything and starting fresh."

| Português | Inglês |
|-----------|--------|
| iteração de prompt | prompt iteration / prompt refinement |
| manter o que está certo | keep what's working |
| direção de mudança | change direction / change vector |
| bloquear o padrão | block the pattern / do-not constraint |
| loop infinito por vagueza | sycophantic loop / vague-prompt loop |
| recomeçar do zero | reset / start from scratch |
| diff de prompt | prompt diff |
| alta entropia de iteração | drift across iterations |
| prompt sub-especificado | underspecified prompt |
| contexto acumulado | accumulated context / conversation history |

## O que vem a seguir

Com especificidade, role, constraints, few-shot e iteration patterns no seu toolkit, você tem o vocabulário completo de prompt engineering para LLMs clássicos. A próxima nota muda o tema: **reasoning models** (o1, R1, Gemini Thinking) têm comportamento de iteração diferente — eles raciocinam internamente antes de responder, e as técnicas de prompting mudam consideravelmente.

Ver [[08 - Reasoning models — audit trail, não chain-of-thought]].

## Fontes e conexões

- **@hooeem** — *Become an AI Engineer*, cap #7. Origem do template Keep/Change/Do-not e o framing de "iteração estruturada como diff".
- **Anthropic** — [Iterating on prompts](https://docs.anthropic.com/en/docs/build-with-claude/prompt-engineering/overview). Guia oficial de boas práticas de refinamento com exemplos.
- **OpenAI** — [Prompt engineering guide](https://platform.openai.com/docs/guides/prompt-engineering), seção sobre iteration. Reforça a ideia de ciclos curtos com critério claro de melhoria.
- **Karpathy, A.** — posts em [karpathy.ai](https://karpathy.ai/) e [X/@karpathy](https://x.com/karpathy) sobre LLM prompting. Exemplo de Como Change com referência externa ("escreva no estilo do Karpathy nos posts dele") ancora a mudança de tom de forma verificável.

A confluência dessas fontes é consistente: iteração eficaz é a que explicita o diff, não a que espera o modelo adivinhar o que você queria. A variação é de terminologia (Keep/Change vs "anchor and modify"), não de princípio.

## Veja também

- [[02 - Especificidade — a primeira disciplina]] — iteração compulsiva geralmente é sintoma de prompt vago de partida
- [[06 - Constraints declarativas — boundaries como engenharia]] — Do-not é uma constraint declarativa em escala micro
- [[09 - Anti-patterns e tells de IA — o que evitar]] — o catálogo do que costuma ir no Do-not
- [[08 - Reasoning models — audit trail, não chain-of-thought]] — iteração com reasoning models tem padrões diferentes
