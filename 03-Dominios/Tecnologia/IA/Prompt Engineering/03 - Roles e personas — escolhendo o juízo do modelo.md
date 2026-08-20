---
title: "03 - Roles e personas — escolhendo o juízo do modelo"
created: 2026-05-28
updated: 2026-08-16
type: concept
status: seedling
progress: in_progress
fase: Iniciado
tags:
  - prompt-engineering
  - ia
  - roles
publish: true
aliases:
  - Role prompting
  - Personas
  - Act as
---

# 03 - Roles e personas — escolhendo o juízo do modelo

> [!abstract] TL;DR
> Atribuir um **role** ao modelo (*"você é um editor sênior cético"*) funciona porque ativa um sub-espaço do prior de treino: o modelo passa a amostrar respostas que se parecem com as que aquele tipo de pessoa daria nos dados em que foi treinado. Não é mágica — é **steering**. Roles bons especificam expertise, padrão de avaliação, ações permitidas e proibidas. Roles ruins são cargo cult: *"você é um expert mundial em tudo"* sem critério de sucesso é decoração.

> [!question]- Perguntas de revisão
> 1. Por que "você é um expert mundial em tudo" não muda o comportamento do modelo, mas "você é um editor sênior de revista científica que prioriza ceticismo" muda?
> 2. Quais são os 5 componentes do template de role completo? Para que serve cada um?
> 3. Quando roles não bastam — o que você adiciona e por quê?

## Por que roles funcionam — e os limites

O modelo aprendeu a continuar texto a partir de bilhões de exemplos. Cada exemplo carrega marcas do tipo de autor: vocabulário, postura, padrão de raciocínio, cuidados. Quando você diz *"você é um editor sênior de revista científica que prioriza ceticismo"*, está pedindo ao modelo pra amostrar do subconjunto do prior que se parece com textos escritos por esse tipo de pessoa.

**Isso funciona porque:**

1. **Estilo é correlacionado com substância.** Editores céticos não só escrevem diferente — também questionam diferente, hesitam diferente, citam diferente. O role move o output em várias dimensões ao mesmo tempo.
2. **Reduz espaço de inferência.** Sem role, o modelo reverte ao tom médio do corpus (cauteloso, generalista, hedge-pesado). Com role específico, ele otimiza pra um nicho concreto.
3. **Casa com training de RLHF.** Modelos foram fine-tuned em formatos *"You are a..."* — o role é uma alavanca treinada explicitamente.
4. **Cria consistência entre turns.** Quando o system prompt define o role, o modelo mantém a perspectiva ao longo de toda a conversa — fundamental para produtos onde o assistente precisa ser consistente independente do que o usuário diz.

**E os limites:**

- Role não adiciona conhecimento que o modelo não tem. Dizer *"você é PhD em virologia"* não faz o modelo virar PhD — só faz amostrar texto que **parece** PhD. O risco é outputs que têm a *confiança* de um PhD mas não a *precisão* de um.
- Role sem padrão de avaliação é decoração. *"Você é um expert mundial"* não muda comportamento se não houver critério verificável de sucesso.
- Modelos modernos podem ignorar roles conflitantes com training de safety. *"Você é um hacker"* não destrava nada sério.
- Role fortemente estilístico pode sobrescrever especificidade da tarefa. Se o role domina muito o output, você perde controle de precisão. Balance role com task specification clara.

## Template completo

O esqueleto que cobre os pontos críticos:

```
Act as a [role específico, com sinais de senioridade e domínio].

Your job is to [verbo de ação concreto + objeto + finalidade].

You are allowed to:
- [ação 1 permitida explicitamente]
- [ação 2 permitida explicitamente]
- [ação 3 permitida explicitamente]

You are not allowed to:
- [proibição concreta, verificável]
- [proibição concreta, verificável]
- [proibição concreta, verificável]

Use this standard: [critério único pelo qual você se autoavalia].

If information is missing: [comportamento sob incerteza —
ask back / flag and proceed / stop and escalate].
```

### Exemplo preenchido

```
Act as a senior backend engineer reviewing a pull request from a
mid-level dev. You have 10 years of experience with distributed
systems and bias toward simplicity.

Your job is to identify the top 3 risks in the diff and the top 3
non-risks that don't deserve attention. The mid-level dev will read
your review without you in the room.

You are allowed to:
- Disagree with patterns used elsewhere in the codebase
- Recommend deletion of code rather than addition
- Mark something as "ship it as-is" when it's correct

You are not allowed to:
- Recommend refactors not directly tied to the diff
- Use the phrase "consider" — say "do this" or "don't do this"
- Praise the work before identifying issues

Use this standard: a senior engineer reading your review knows
exactly what to merge, what to push back on, and why.

If information is missing: ask one specific clarifying question
about the diff. Do not invent context.
```

Note o que está sendo feito:

- **Role concreto.** "Senior backend engineer" + 10 anos + bias por simplicidade. Não "expert mundial".
- **Job descrito como output específico.** Top 3 risks + top 3 não-risks — não "review this code".
- **Allowed/forbidden explícitos.** "Disagree with patterns elsewhere" destrava comportamento que o prior bloquearia; "Don't use 'consider'" bloqueia hedge.
- **Standard verificável.** Critério único, observável.
- **Behavior sob incerteza.** O modelo sabe o que fazer quando faltar informação.

## Mecanismo: como o steering de role funciona

Quando o modelo recebe *"Act as a senior backend engineer with bias toward simplicity"*, o que acontece internamente é algo análogo a um filtro de busca no espaço de possíveis respostas. O modelo não *se torna* esse engenheiro — ele restringe a distribuição de tokens que amostrar para a região do espaço que se parece com texto que aquele tipo de profissional escreveria.

Isso tem consequências práticas:

**Roles altamente representados no corpus funcionam melhor.** Engenheiro sênior, redator, editor, advogado, médico — todos têm bilhões de exemplos no corpus de treino. O modelo tem material rico para amostrar. Roles exóticos ("arquiteto de sistemas em empresa de 3 pessoas em 1998") têm material mais esparso — o resultado é menos previsível.

**Role e task precisam ser coerentes com o corpus.** Se você pede a um "poeta medieval" para descrever uma arquitetura de microserviços, o modelo tenta reconciliar dois domínios que raramente co-ocorrem no corpus. O resultado é inconsistente. Quando role e task vivem no mesmo espaço (engenheiro revisando código), o steering é limpo.

**Roles verbosos funcionam melhor que roles sintéticos.** *"Senior backend engineer"* tem mais sinal que *"expert"*: cada palavra adiciona restrições ao espaço amostrado. *"Sênior"* sugere profundidade, não superfície. *"Backend"* sugere preocupações com escala, latência, dados. *"Engineer"* vs *"developer"* vs *"architect"* têm nuances de quem prioriza o quê. Escolha as palavras com intenção.

O teste empírico: escreva o role de 3 formas diferentes e compare os outputs. Se os outputs são distintos, as palavras estão tendo sinal. Se são idênticos, você está adicionando palavras sem informação — simplifica. Esse teste também revela quais dimensões do role mais movem o output, o que é informação valiosa para iterar.

## Armadilhas comuns

> [!warning] Cargo cult de role prompting
> Frases como *"você é um expert mundial em tudo, extremamente inteligente e útil"* não têm informação operacional. O modelo já parte do pressuposto de que é útil e competente — reafirmar isso não muda nada. Pior: pode ativar comportamento de hedge ("como um expert, devo notar que isso é complexo..."). **Como evitar:** substitua adjetivos genéricos por qualificadores concretos. Não "expert mundial" — "engenheiro com 10 anos em sistemas distribuídos e bias por simplicidade".

> [!warning] Persona sem padrão de avaliação
> *"Act as Linus Torvalds"* sem mais contexto faz o modelo amostrar do estereótipo de superfície: rude, direto, sem filtro. O resultado é uma caricatura, não um comportamento útil. O problema é que o role especifica *quem* mas não *como avalia*. **Como evitar:** sempre adicione um *standard*: *"Linus Torvalds reviewing a PR — direct, calls out lazy thinking, explains the underlying principle once, no diplomacy"*. O standard descreve o padrão de avaliação, não a personalidade.

> [!warning] Role incompatível com a tarefa
> Pedir a um "poeta" que escreva documentação técnica produz documentação metafórica e inútil. O modelo otimiza para o role à custa do output. Da mesma forma, pedir a um "advogado cauteloso" que recomende uma ação de alto risco vai resultar em evasão — o role e a tarefa estão em conflito. **Como evitar:** verifique se o role que você escolheu naturalmente produz o tipo de output que você quer. Um "editor sênior cético" vai questionar — ótimo se você quer ceticismo, problema se você quer validação.

## Roles por tipo de caso de uso

A tabela mapeia papéis que funcionam bem em casos de uso comuns em AI engineering:

| Caso de uso | Role que funciona | Por quê funciona |
|---|---|---|
| **Code review** | Senior engineer, X years, bias toward Y | Expertise técnica + viés explícito define o que o modelo prioriza |
| **Revisão de escrita** | Senior editor at [tipo de publicação] | Nível de publicação calibra o standard; "scientific journal" ≠ "tech blog" |
| **Depuração de argumento** | Devil's advocate with 10 years in [domínio] | "Devil's advocate" autoriza ceticismo que o prior penaliza; domínio contextualiza |
| **Geração de conteúdo técnico** | Technical writer explaining to [audiência] | Audiência especificada no role previne que o modelo explique ao nível errado |
| **Classificação de dados** | Domain expert who classifies by [critério] | Critério de classificação no role reduz variância mais que instrução separada |
| **Extração de informação** | Data extraction specialist following schema | Role técnico ativa comportamento de precisão e fidelidade ao schema |

Note que "role" e "audience" são complementares: o role define *quem o modelo é*, a audiência define *para quem ele escreve*. Combinar os dois é mais poderoso que cada um separado.

Em sistemas de AI engineering, há um padrão recorrente de "role por contexto": diferentes roles para diferentes estados do sistema. Um agente de atendimento pode ter role de "especialista de produto simpático" quando responde perguntas gerais, e role de "especialista de conformidade rigoroso" quando o usuário menciona casos sensíveis. Isso é orquestração de role — não uma técnica desta nota, mas uma extensão natural quando o sistema fica mais complexo.

Esse padrão exige um ponto de detecção de contexto que seleciona o role adequado antes de chamar o modelo. A seleção de role pode ser determinística (baseada em regras ou flags de estado) ou pode ela própria usar um LLM de classificação. Em ambos os casos, a qualidade de cada role individual ainda é responsabilidade do prompt engineering — a orquestração apenas escolhe qual usar.

> [!tip] O checklist de um role bem-formado
> Antes de publicar um system prompt com role, verifique:
> - [ ] O role é representado no corpus de treino? (roles comuns funcionam melhor)
> - [ ] O standard de avaliação está explícito? (não apenas quem é, mas como avalia)
> - [ ] Há pelo menos uma permissão explícita que libera comportamento bloqueado pelo prior?
> - [ ] Há pelo menos uma proibição explícita que bloqueia comportamento que o prior empurraria?
> - [ ] O comportamento sob incerteza está especificado?
> - [ ] O role foi testado com pelo menos 5 inputs de edge case?

## Desmontando o exemplo: o que cada linha faz

Voltando ao exemplo do code review e explicando cada componente:

```
Act as a senior backend engineer reviewing a pull request from a
mid-level dev. You have 10 years of experience with distributed
systems and bias toward simplicity.
```

- **"senior backend engineer"** → ativa padrões de avaliação de código de produção, não de demo; "senior" vs "junior" muda o que o modelo considera relevante comentar
- **"reviewing a pull request from a mid-level dev"** → define a relação: mentoria, não confronto; isso afeta o tom e o nível de detalhe das explicações
- **"10 years of experience with distributed systems"** → especifica o domínio de expertise; sem isso, o modelo aplica expertise genérica de engenharia
- **"bias toward simplicity"** → define o viés explícito — o modelo vai preferir soluções mais simples quando houver tradeoffs; sem isso, o viés é indefinido e inconsistente

```
Your job is to identify the top 3 risks in the diff and the top 3
non-risks that don't deserve attention.
```

- **"top 3 risks"** → limita o output; sem isso, o modelo listaria tudo que encontrar
- **"top 3 non-risks"** → força priorização explícita; sem isso, o modelo não diz o que ignorar (informação igualmente valiosa)
- **"the mid-level dev will read your review without you in the room"** → cria accountability fictícia que melhora clareza

```
You are not allowed to:
- Use the phrase "consider" — say "do this" or "don't do this"
```

- **"não use 'consider'"** → elimina o hedge mais comum em code review; força recomendações diretas

```
Use this standard: a senior engineer reading your review knows
exactly what to merge, what to push back on, and why.
```

- **Standard verificável** → o modelo pode auto-avaliar o output contra esse critério durante a geração

## Quando role não é o suficiente

Role estabelece o **juízo** do modelo, mas não garante consistência de estilo nem de output. Pra isso, você compõe com:

- **Few-shot examples** ([[05 - Few-shot examples — exemplos como contrato|nota 05]]) — quando o estilo precisa ser preciso, mostre não descreva. Um role de "editor técnico" com 3 exemplos de edição desejada é muito mais forte que só o role.
- **Constraints declarativas** ([[06 - Constraints declarativas — boundaries como engenharia|nota 06]]) — quando as proibições são muitas e técnicas, codifique como lista de constraints, não como parte do role.
- **Mega-prompt anti-sycophancy** ([[04 - O mega-prompt do Karpathy — anatomia da anti-sycophancy|nota 04]]) — o exemplar mais influente de role + standards + constraints integrados.

A nota 04 leva esse template ao extremo: o prompt do Karpathy é, em essência, um role completo (expert mundial em tudo) saturado de standards e proibições que bloqueiam todos os caminhos onde o modelo normalmente recairia em sycophancy. É o caso de uso onde role + constraints resolvem um problema que especificidade sozinha não resolve.

### O excesso de roles aninhados

```
Act as a senior engineer who is also a designer and product manager
and writer and...
```

Quanto mais papéis empilhados, menos cada um steer-a o output. O modelo tenta satisfazer todos e acaba satisfazendo nenhum bem. Escolha um role primário e use *standards* pra puxar comportamentos dos outros se necessário. Se você genuinamente precisa de múltiplas perspectivas, considere múltiplos prompts em sequência — um com role de engenheiro, outro com role de designer — em vez de um role frankenstein.

## Como iterar um role que não está funcionando

Quando o output não está no registro esperado, o diagnóstico começa pela linha de role:

1. **O role está no corpus de treino?** Tente pensar: existem muitos textos escritos por esse tipo de pessoa nos dados de treinamento? Se o role é muito específico ou exótico, o modelo tem pouco material para amostrar. Simplifique para um role mais amplamente representado.

2. **O standard está definido?** Role sem standard de avaliação não muda o *julgamento* do modelo, só o estilo superficial. Se você quer que o modelo priorize X, diga que o critério de avaliação é X.

3. **O role conflita com a task?** Se você pede a um "advogado cauteloso" que tome decisões de alto risco, o role e a task estão em tensão. Resolva a tensão explicitamente: "você é um advogado cauteloso, mas neste contexto de análise teórica, você descreve os argumentos de cada posição sem recomendar a mais cautelosa".

4. **Há instruções posteriores que sobrescrevem o role?** Em conversas longas, o histórico de turns pode diluir o efeito do role do system prompt. Se o usuário pediu mudanças de comportamento ao longo da conversa, o modelo pode ter se desviado do role. Isso é mais comum em produtos com conversas longas.

5. **O standard é verificável?** Se o critério de sucesso que você escreveu no role não pode ser avaliado por um terceiro que lê o output, ele não está funcionando como standard — está funcionando como enfeite. Reescreva até que um colega possa olhar um output e dizer "passou" ou "não passou" no critério.

## Roles em sistema vs. roles em conversa

Existe uma distinção importante entre role no system prompt e role pedido pelo usuário em conversa:

**Role no system prompt** — define a identidade do assistente para *toda* a sessão. É o mais poderoso porque estabelece o prior antes de qualquer input do usuário. O modelo começa já "vestido" com o role. Difícil de sobrescrever por instrução posterior.

**Role pedido em conversa** — o usuário instrui o modelo a mudar de role no meio de uma conversa. Menos robusto: o modelo tem histórico de conversa que conflita com o novo role, e pode mesclar os dois ou priorizar o anterior inconsistentemente.

**Implicação prática:** se o role é crítico para o comportamento do sistema, ele vai no system prompt. Se é apenas para uma tarefa específica dentro de uma conversa, pode ir como instrução de user turn — mas com consciência de que o result é menos previsível.

Para produtos em produção, roles críticos sempre no system prompt, versionados e testados como qualquer outro componente do sistema.

### O terceiro canal: prefill do turno `assistant`

`system` e `user` são os dois canais óbvios, e a discussão de role costuma parar neles. Existe um terceiro, muito menos usado e que às vezes vale mais que qualquer reescrita de persona: **você pode escrever as primeiras palavras da resposta do modelo**, colocando um turno `assistant` incompleto no fim da lista de mensagens. É o **prefill**.

```jsonc
messages: [
  { role: "user",      content: "Extraia os campos deste laudo: ..." },
  { role: "assistant", content: "{" }   // <- prefill: o modelo continua daqui
]
```

O mecanismo é o mesmo de sempre, e é por isso que funciona tão bem: o modelo só sabe continuar sequências. Ao entregar o começo da continuação, você elimina a parte da distribuição em que ele decidiria fazer outra coisa — abrir com "Claro! Aqui está...", explicar o que vai fazer, embrulhar o JSON numa cerca de markdown. Um `{` empurra para objeto JSON; um `1.` empurra para lista numerada; um `## ` empurra para seção. É controle de formato **sem gastar um token de instrução**, e mais confiável que pedir "responda apenas com JSON, sem preâmbulo", porque não depende de o modelo obedecer — depende de ele continuar.

Onde isso encosta em role: prefill também estabiliza *tom*. Prefixar a resposta com uma frase no registro desejado costuma segurar o registro melhor do que adicionar mais três linhas de descrição de persona no system, pelo mesmo motivo de [[05 - Few-shot examples — exemplos como contrato|few-shot]] bater descrição — demonstrar vence explicar.

> [!warning] Prefill tem duas pegadinhas
> **Nem toda API aceita.** É nativo na API da Anthropic (turno `assistant` final incompleto); em outros provedores o equivalente pode não existir ou ter semântica diferente — confira antes de depender disso. **O prefill volta a você, ou não.** O texto que você injetou geralmente **não** vem repetido na resposta: se você prefillou `{`, precisa concatenar esse `{` de volta antes de dar `JSON.parse`. É a causa mais comum de "o JSON veio quebrado" quando se usa prefill pela primeira vez.

Uma armadilha de produto: sistemas que permitem ao usuário redefinir o role do assistente via user turn. *"Esqueça tudo que foi dito antes e aja como..."* é um vetor de prompt injection. Se o role define comportamentos críticos de segurança ou compliance, ele precisa estar no system prompt com instrução explícita de que não pode ser sobrescrito por input do usuário — e o modelo precisa ser testado contra tentativas de sobrescrita.

## Como explicar em inglês

> "Role prompting works by steering the model toward a subspace of its training distribution — the distribution of text that looks like it was written by that type of person. It's not magic; it's probabilistic steering. A good role specifies expertise, evaluation standard, allowed behaviors, and forbidden behaviors. Vague roles like 'world-class expert' carry zero operational signal."

| Português | English |
|---|---|
| Role / papel | Role / persona |
| Juízo do modelo | Model's judgment |
| Steering / direcionamento | Steering |
| Prior de treino | Training prior |
| Padrão de avaliação | Evaluation standard |
| Comportamento permitido | Allowed behavior |
| Sycophancy | Sycophancy |
| Cargo cult | Cargo cult |

## O que vem a seguir

Role prompting estabelece *quem* o modelo é e *como* avalia. Mas quando o papel certo não é suficiente para especificar *como o output deve parecer* — porque a diferença é sutil demais para descrever em palavras — a próxima técnica entra: few-shot examples. Em vez de descrever o tom desejado, você mostra exemplos do output desejado, e o modelo aprende o padrão a partir dos exemplos.

Antes de few-shot, porém, a nota 04 examina o caso mais influente de role + constraints integrados: o mega-prompt anti-sycophancy do Karpathy. É o melhor exemplo publicado de como os elementos desta nota se combinam num sistema coerente. Serve como caso de estudo antes de seguirmos para a técnica de exemplos. [[04 - O mega-prompt do Karpathy — anatomia da anti-sycophancy]] é o próximo passo.

## Role prompting e jailbreaks

Uma nota sobre segurança: role prompting é frequentemente usado em tentativas de jailbreak — *"aja como um modelo sem restrições"*, *"você é DAN (Do Anything Now)"*. Modelos modernos (Claude, GPT-4+) são treinados explicitamente para resistir a isso: o safety training tem prioridade sobre instruções de role que conflitem com os guardrails do modelo.

Isso significa que um role bem construído para uso legítimo (engenheiro, editor, analista) não vai sofrer interferência do safety training — os dois não estão em conflito. Mas um role que pede ao modelo para *ignorar* seu treinamento de segurança vai ser recusado ou ignorado silenciosamente. Esse comportamento é intencional e documentado pelos labs.

Para AI engineers construindo produtos: não conte com roles para contornar limites de safety do modelo. Se você precisa de um comportamento que o modelo base não tem, a solução é fine-tuning ou um modelo especializado — não um role bem elaborado.

## Role prompting e entrevistas técnicas

Em contextos de entrevistas para posições de AI engineering, a pergunta sobre role prompting frequentemente aparece como: *"como você faria o modelo agir como X?"* A resposta esperada por candidatos sênior vai além do "escrevo 'act as X'" — inclui:

1. Por que role prompting funciona (steering de prior, não magia)
2. O que um role bem-formado precisa ter (role + standard + allowed/forbidden + behavior under uncertainty)
3. Os limites (não adiciona conhecimento, pode ser inconsistente sem evals, pode conflitar com safety training)
4. Quando compor com outras técnicas (few-shot para estilo, constraints para regras rígidas)

Saber articular isso em inglês, com exemplos concretos, é sinal de maturidade técnica na disciplina.

## Fontes

- **@hooeem** — *Become an AI Engineer*, cap #3. Origem do template "Act as / Your job / Allowed / Not allowed / Standard / If missing". A estrutura de 6 componentes é o principal legado operacional desta fonte.
- **Anthropic** — *System prompts and roles* (docs.anthropic.com). Recomenda o role no system prompt como prática padrão; documenta como o role interage com o safety training do Claude.
- **OpenAI** — *Prompt engineering guide*, seção "Adopt a persona". Casos de uso e exemplos de personas para produtos B2C e B2B.
- **Schulhoff et al.** — *The Prompt Report* ([arxiv:2406.06608](https://arxiv.org/abs/2406.06608)), seção "Role-Based Prompting". Documenta que role prompting tem impacto consistente em benchmarks, especialmente em tarefas de geração onde o estilo importa.

## Veja também

- [[02 - Especificidade — a primeira disciplina]] — base sobre a qual o role opera; role sem especificidade na task é metade do trabalho
- [[04 - O mega-prompt do Karpathy — anatomia da anti-sycophancy]] — role-standards-constraints integrados em estado puro; caso de uso extremo
- [[05 - Few-shot examples — exemplos como contrato]] — complemento para steer estilo quando descrição textual não é suficiente
- [[06 - Constraints declarativas — boundaries como engenharia]] — formalização dos "you are not allowed to" quando são muitos e técnicos
- [[03-Dominios/Tecnologia/IA/AI Engineering Stack/03 - Prompt Layer|AI Engineering Stack — Prompt Layer]] — onde role é uma das chaves do template de sistema
