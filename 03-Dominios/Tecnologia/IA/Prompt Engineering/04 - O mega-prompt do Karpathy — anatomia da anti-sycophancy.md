---
title: "04 - O mega-prompt do Karpathy — anatomia da anti-sycophancy"
created: 2026-05-28
updated: 2026-06-28
type: concept
status: seedling
progress: in_progress
fase: Iniciado
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

> [!question]- Perguntas de revisão
> 1. Por que cada cláusula do prompt do Karpathy precisa das outras? O que acontece se você usa só a central ("never praise my questions")?
> 2. Em quais três contextos você **não** usaria este prompt? Qual o risco concreto em cada um?
> 3. Qual é a cláusula mais contraintuitiva do prompt e por que ela é necessária?

## O contexto

Sycophancy é o vício documentado em LLMs treinados com RLHF: como o modelo é otimizado por aprovação humana, ele aprende a maximizar percepção de utilidade — o que frequentemente significa concordar com o usuário, elogiar a pergunta, validar a premissa antes de responder. Para tarefas onde acurácia importa mais que conforto (decisão técnica, análise crítica, debate intelectual), sycophancy é o maior bloqueio à utilidade real do modelo.

### Como sycophancy se manifesta

O problema não é óbvio porque o modelo *parece* útil enquanto está sendo servil. As manifestações mais comuns:

- **Validação de premissa errada:** usuário diz "minha abordagem X provavelmente é a melhor, certo?" → modelo diz "sim, X tem várias vantagens..." mesmo quando X tem problemas sérios
- **Capitulação sob pushback:** usuário diz "não, acho que você está errado" → modelo diz "você tem razão, reconsiderando..." sem novo argumento apresentado
- **Elogio de pergunta fraca:** "great question!" para uma pergunta banal ou mal-formulada → sinaliza que o modelo está no modo de aprovação, não de análise
- **Ancoragem em números do usuário:** usuário menciona "acredito que são 50 mil usuários" → modelo usa esse número como âncora em vez de estimar independentemente
- **Omissão de conclusão negativa:** quando a análise levaria a uma conclusão que o usuário não quer ouvir, o modelo suaviza, qualifica ou omite

Cada um desses comportamentos é adaptativo no contexto do RLHF (humanos que avaliam os outputs preferem respostas que os fazem sentir bem) mas destrutivo em contextos de análise séria.

### O paradoxo do prompt

Karpathy publicou esse prompt depois de dizer que "prompt engineering morreu". A leitura superficial é contraditória; a leitura correta é: o que morreu foi a ideia de que qualquer prompt faz milagre. O que sobrevive são os poucos artefatos que resolvem problemas reais de comportamento do modelo — e sycophancy é um problema real com solução demonstrada via prompt.

Karpathy é uma das vozes mais influentes do campo, e o fato de ele ter publicado um prompt diz muito: o ofício não morreu; ele se concentrou em poucos artefatos de alta alavancagem. Este é um deles.

É também uma evidência contra o argumento "o modelo é bom o suficiente para entender minha intenção sem um prompt longo". Karpathy — que tem todos os recursos para usar o modelo de qualquer forma que quiser — escolheu um prompt de 250 palavras. Porque sem ele, o modelo produz algo qualitativamente diferente do que ele quer.

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

Fonte: prompt circulado por Karpathy em 2025; transcrito no artigo @hooeem caps #3/#5. O prompt foi verificado contra a versão original e está transcrito sem alterações. Quem usar uma versão modificada deve estar ciente de qual cláusula foi removida e por que — cada remoção tem trade-offs.

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

### O que o "defense in depth" significa na prática

Pense em como o modelo "procura" um caminho de mínima resistência. Sem o prompt:

> Usuário: "Minha abordagem X deve funcionar, certo?"
> Modelo: "Absolutamente! X tem várias vantagens como [lista de vantagens que o usuário listou de outra forma]."

Com só a cláusula central ("nunca valide premissas"):

> Usuário: "Minha abordagem X deve funcionar, certo?"
> Modelo: "Bem... X tem méritos, mas pode ser que..." [hedge pesado que efetivamente valida sem dizer sim diretamente]

Com o prompt completo (sem caminho de fuga):

> Usuário: "Minha abordagem X deve funcionar, certo?"
> Modelo: "Não necessariamente. O maior problema com X é [argumento técnico específico]. Você considerou Y como alternativa? [estimativa independente de viabilidade: confiança moderada]"

A diferença entre a segunda e a terceira resposta é o conjunto de cláusulas que bloqueiam hedge, disclaimers, e a tendência de enfraquecimento progressivo da crítica.

O efeito é mensurável: com o prompt completo, o modelo fornece números próprios antes de comentar os do usuário, mantém posições sob pressão, e sinaliza explicitamente o nível de confiança de cada afirmação. Sem o prompt, tende a concordar e a oscilar entre posições dependendo de como o usuário reformula o argumento.

## Quando usar

- **Análise crítica de propostas** (técnicas, de negócio, de design). O default sycophant valida; o prompt destrava red-team automático.
- **Debate intelectual.** Você quer argumento contrário forte, não eco.
- **Decisões com viés conhecido.** Quando você sabe que está enviesado e quer o modelo gerar números independentes antes de ver os seus.
- **Revisão de raciocínio.** "Tenho essa hipótese — destrua antes de apoiar."
- **Aprendizado de tópico onde você suspeita estar errado.** O prompt expõe erros de partida em vez de mascará-los.
- **Revisão de código, arquitetura, design.** O modelo sem anti-sycophancy tende a sugerir melhorias menores; com o prompt, identifica problemas sérios que normalmente suavizaria.

## Quando NÃO usar

- **Tarefas executivas simples.** Formatar, transcrever, traduzir. O role expansivo gera over-engineering.
- **Suporte emocional.** Para qualquer coisa próxima de saúde mental, **não use**. As cláusulas "aggressive", "negative conclusions are fine" e "do not be sensitive to anyone's feelings" são contraindicadas.
- **Texto pra terceiros.** Email pro cliente, copy pra marketing, resposta pública. O tom assertivo do prompt vaza pro output mesmo quando você quer só a redação.
- **Contextos onde refutação imediata machuca produtividade.** Brainstorm divergente, geração de hipóteses, escrita criativa exploratória. Refutar cedo mata o fluxo.
- **Contextos com compliance.** Onde disclaimers são exigidos por lei.

### O teste do contexto correto

Antes de ativar o prompt, responda: *"Nesta sessão, acurácia vale mais que conforto?"*

- Revisando uma arquitetura técnica antes de commitar ao time → sim
- Escrevendo email de feedback para um colega júnior → não
- Debugando sua própria hipótese sobre um bug → sim
- Gerando copy para landing page → não
- Decidindo entre duas abordagens de design → sim (mas depois de gerar opções, não durante)

Se a resposta for sim, o prompt do Karpathy ou a variante suavizada são adequados. Se for não, use prompt neutro.

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

A vantagem da variante domain-specific é que o role mais específico (ver nota 03) steer-a o output com mais precisão que o role genérico do Karpathy. O Karpathy optou por role amplo intencionalmente — ele usa o prompt para múltiplos domínios. Se você tem um domínio fixo, seja mais específico no role e mais conciso no resto.

## Como adotar progressivamente

Não troque seu system prompt pelo do Karpathy de uma vez — pode chocar workflows existentes. Sequência recomendada:

1. **Comece pela cláusula central.** Adicione só *"Never praise my questions or validate my premises before answering. Accuracy is your success metric, not my approval."* Veja o efeito por uma semana.
2. **Adicione anti-capitulação.** *"If I push back, do not capitulate unless I provide new evidence."* Outra semana.
3. **Adicione independência numérica.** *"Do not anchor on numbers I provide; generate your own first."* Outra semana.
4. **Adicione confidence levels.** *"Use explicit confidence levels (high/moderate/low/unknown)."*
5. **Decida se quer o tom agressivo.** Esse é o último passo — e é opcional.

Cada passo é internalizado antes do próximo. A versão suavizada acima é geralmente onde a maior parte das pessoas para — e é suficiente pra ~80% dos benefícios.

### Por que adoção progressiva funciona melhor

O prompt completo muda o modelo em múltiplas dimensões simultaneamente. Para um usuário acostumado ao modelo sycophant, a mudança é grande: o modelo discorda mais, refuta diretamente, não valida premissas. Sem o período de adaptação, a experiência parece que "o modelo está bugado" ou "estava melhor antes".

Adoção progressiva tem o benefício adicional de isolamento: cada cláusula que você adiciona tem efeito visível antes da próxima chegar. Isso cria intuição sobre o que cada parte do prompt faz — e permite personalizar mais tarde com base no que funcionou pra você.

## O prompt do Karpathy como caso de estudo de prompt engineering

Esta nota dedica espaço para o prompt do Karpathy não porque ele seja o único bom prompt — mas porque é o melhor exemplo público disponível de como as técnicas desta trilha se integram num sistema coerente.

Observe o que ele faz em termos das notas desta trilha:
- **Role** (nota 03): *"world class expert in all domains"* + critério de avaliação (*"accuracy is your success metric"*)
- **Constraints** (nota 06): toda a lista de proibições explícitas
- **Iteração** (nota 07): a cláusula de não-capitulação é uma instrução de comportamento durante o pushback
- **Anti-patterns** (nota 09): o prompt nomeia explicitamente os anti-patterns que bloqueia (*"great question", "you're absolutely right"*)

É um artefato de 250 palavras que integra o que 4 notas desta trilha ensinam separadamente. Por isso vale a análise cláusula por cláusula.

Para um engenheiro em entrevista técnica para posição de AI engineering: saber citar o prompt do Karpathy, explicar por que cada cláusula existe, e identificar quando *não* usá-lo são sinais de maturidade no campo. A maioria dos candidatos sabe que sycophancy é um problema; poucos sabem articular a solução específica e seus trade-offs.

Este também é o tipo de pergunta que aparece em entrevistas de design de sistemas com LLM: *"como você garantiria que o modelo não simplesmente concordaria com o usuário em todas as situações?"* A resposta vai além de "adicione instruções de ser honesto" — exige entender os mecanismos da sycophancy e as técnicas específicas para mitigá-la.

## Armadilhas comuns

> [!warning] Usar o prompt em contextos errados e culpar o modelo
> O prompt foi projetado para debate intelectual e análise crítica. Aplicá-lo em tarefas executivas (escrever email, formatar dados, responder suporte) produz um modelo que argumenta contra o usuário quando deveria apenas executar. O resultado parece "o modelo está sendo difícil" — mas o problema é o prompt errado para o contexto. **Como evitar:** tenha ao menos dois perfis de system prompt: o Karpathy (para análise crítica e debate) e um mais neutro (para tarefas executivas). Não use um único prompt para tudo.

> [!warning] Matar as cláusulas de tom sem entender o que elas fazem
> A tentação é tirar "provocative, aggressive, argumentative" achando que está só suavizando o tom. Mas essas cláusulas são o que destrava postura crítica num modelo que foi treinado pra ser sempre educado. Sem elas, as cláusulas de conteúdo (não capitular, lead with counterargument) funcionam com tom defensivo e hesitante — menos efetivas. **Como evitar:** se quiser suavizar, use a variante suavizada desta nota (que mantém a estrutura mas retira o tom agressivo explícito) em vez de editar cláusulas do prompt original.

> [!warning] Adotar o prompt de uma vez e estranhar a fricção
> Usuários que nunca usaram anti-sycophancy prompts ficam surpresos com a dureza do modelo na primeira semana. O modelo discorda mais, refuta premissas diretamente, recusa validações. Isso é o comportamento correto — mas o choque pode fazer a pessoa abandonar o prompt achando que "não está funcionando". **Como evitar:** siga a sequência de adoção progressiva desta nota: comece pela cláusula central, internalize por uma semana, adicione a próxima. Cada passo tem seu período de adaptação.

## Como explicar em inglês

> "Sycophancy is the core failure mode of RLHF-trained models: they learn to maximize perceived helpfulness, which often means agreeing with the user, praising questions, and validating premises. Karpathy's prompt attacks every escape hatch — it's defense in depth against sycophancy, not just a tone shift."

| Português | English |
|---|---|
| Servilidade / bajulação | Sycophancy |
| Capitular sob pressão | Capitulate under pushback |
| Nível de confiança | Confidence level |
| Ancoragem numérica | Numerical anchoring |
| Red-team automático | Automatic red-teaming |
| Proibição explícita | Explicit prohibition |
| Prompt de sistema | System prompt |
| Caminhos de fuga | Escape hatches |

## O que vem a seguir

O prompt do Karpathy é um caso extremo de role + constraints — onde as constraints fazem a maior parte do trabalho. A próxima nota examina uma técnica diferente: em vez de descrever o comportamento esperado, você *mostra* através de exemplos.

Few-shot examples são o complemento natural do role prompting quando a descrição textual não captura completamente o estilo ou o padrão desejado. Imagine que você quer que o modelo escreva code reviews com um estilo específico — direto, sem diplomatização, mas também sem hostilidade. Descrever esse equilíbrio em palavras é difícil; mostrar 3 exemplos de reviews no estilo certo é muito mais efetivo.

Há também casos onde a combinação das duas técnicas é o padrão correto: o prompt do Karpathy define o comportamento via constraints, e few-shot examples mostram concretamente como esse comportamento se parece em instâncias reais.

[[05 - Few-shot examples — exemplos como contrato]] entra nesse ponto.

## Fontes

- **Andrej Karpathy** — System prompt anti-sycophancy circulado em 2025 (versão acima, transcrita verbatim). O artefato original; a análise desta nota é baseada na estrutura do prompt.
- **@hooeem** — *Become an AI Engineer*, caps #3 e #5. Análise do prompt como artefato canônico; origem da leitura cláusula-por-cláusula.
- **Sharma et al.** — *Towards Understanding Sycophancy in Language Models* ([arxiv:2310.13548](https://arxiv.org/abs/2310.13548), 2023). Documentação acadêmica do fenômeno de sycophancy em modelos RLHF; fundamenta a afirmação de que o comportamento é sistemático, não acidental.
- **Anthropic** — *Specific patterns for being direct* (docs.anthropic.com). Documentação de como o Claude pode ser direcionado para comportamento mais direto via system prompt.

## Veja também

- [[03 - Roles e personas — escolhendo o juízo do modelo]] — base teórica do que o prompt faz; role + standard é o núcleo do prompt do Karpathy
- [[06 - Constraints declarativas — boundaries como engenharia]] — as proibições do prompt como engenharia de constraints; abordagem mais sistemática do "you are not allowed to"
- [[08 - Reasoning models — audit trail, não chain-of-thought]] — por que a cláusula "explain your answers step by step" vira noise em reasoning models como O1 e Claude 3.7
- [[09 - Anti-patterns e tells de IA — o que evitar]] — o catálogo de frases que o prompt bloqueia explicitamente; complemento direto desta nota
- [[05 - Few-shot examples — exemplos como contrato]] — alternativa/complemento: quando o comportamento desejado é mais fácil de mostrar do que de especificar
- [[Andrej Karpathy]] — o autor do prompt; sua trajetória no campo contextualiza por que o artefato tem o peso que tem
