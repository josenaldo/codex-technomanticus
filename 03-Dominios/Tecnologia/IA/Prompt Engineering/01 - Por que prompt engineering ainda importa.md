---
title: "01 - Por que prompt engineering ainda importa"
created: 2026-05-28
updated: 2026-06-28
type: concept
status: seedling
progress: in_progress
fase: Iniciado
tags:
  - prompt-engineering
  - ia
  - meta
publish: true
aliases:
  - Prompt engineering morreu
  - Por que prompt ainda importa
---

# 01 - Por que prompt engineering ainda importa

> [!abstract] TL;DR
> Em 2025, virou meme dizer que *"prompt engineering morreu"*. A frase pegou porque era meio verdade e meio venda: o que morreu foi o **prompt como bala de prata** — a ideia de que a frase mágica isolada resolve qualquer tarefa. O que segue vivo é o **prompt como interface**, **prompt como contrato** e **prompt como camada** dentro de um sistema maior. Esta nota separa um do outro e posiciona a trilha: prompt engineering é uma camada bem-definida dentro do Prompt Layer do [[AI Engineering Stack]], não a disciplina inteira.

> [!question]- Perguntas de revisão
> 1. Qual é a diferença entre "prompt como bala de prata" e "prompt como camada"? Por que a segunda sobreviveu?
> 2. Context engineering e prompt engineering se excluem ou se incluem? Desenhe a relação hierárquica.
> 3. Que evidências concretas mostram que prompt engineering ainda tem peso em 2025-2026?

## A tese "prompt engineering morreu"

A frase ganhou tração em 2025 quando vários nomes do campo — Karpathy à frente — passaram a defender que *context engineering* era a disciplina que importava, e que prompt engineering tinha virado *"jardim de infância"*.

**Por que a tese pegou:**

1. **O cansaço com prompt-magia.** Threads, cursos e ebooks vendiam *"a frase de 50 dólares que muda tudo"*. Não mudava — e ficou óbvio.
2. **A ascensão dos agentes.** Sistemas agênticos rodam por horas, milhões de tokens, múltiplas fontes. Nenhum prompt único sobrevive a isso; o problema verdadeiro é montar o ambiente informacional.
3. **Modelos melhores.** GPT-4, Claude 3.5, Gemini 1.5 ficaram robustos o suficiente pra entender intenção razoavelmente formulada. A penalidade por prompt ruim caiu — não desapareceu.
4. **Marketing de uma disciplina nova.** *Context engineering* precisava de espaço; matar prompt engineering simbolicamente abria mercado conceitual.

Tudo isso é parcialmente verdade — mas a leitura literal vira erro.

### O mecanismo do equívoco

Pense em como um cozinheiro experiente reage a um forno de nova geração. O forno é mais preciso, distribui calor melhor, perdoa mais erros de temperatura. O cozinheiro novato conclui: *"facas afiadas não importam mais"*. O cozinheiro sênior conclui: *"com um forno melhor, minha faca afiada produz resultados ainda melhores"*.

Modelos mais capazes reduzem o custo de um prompt ruim — mas amplificam o retorno de um prompt bom. A assimetria só cresce: num modelo fraco, um prompt horrível e um prompt razoável produzem outputs parecidos (ambos ruins). Num modelo forte, a distância entre prompt medíocre e prompt preciso se torna a diferença entre produto e demo.

## O que de fato morreu

| Morreu | Por quê |
|---|---|
| **Prompt como bala de prata** | A ideia de que a frase certa, isolada, é tudo o que importa. Sem contexto, memória, retrieval e guardrails, prompt nenhum sustenta um sistema. |
| **Prompt sem contexto** | Escrever instrução sem pensar no que mais entra na janela de contexto produz demos, não produtos. |
| **Prompt como ritual mágico** | *"Você é um expert mundial em..."* repetido sem propósito não muda nada. Cargo cult. |
| **Prompt como skill terminal** | Pessoas vendiam "prompt engineer" como carreira completa. Em 2026, é uma sub-habilidade dentro de AI engineering, não um cargo. |

Quem só tinha prompt engineering no portfólio levou impacto real. Quem tinha prompt engineering **mais** context, evals, guardrails, orquestração — só ficou mais valioso.

### Por que cargo cult não funciona

Ritual mágico tem uma lógica sedutora: *alguém disse que funcionou, então repito.* O problema é que prompts de 2023 para GPT-3.5 eram otimizados para um modelo que precisava de scaffolding externo para raciocinar. Em Claude 3.5 ou GPT-4o, o mesmo scaffolding pode na verdade **restringir** o modelo — interferir com mecanismos internos que o modelo já domina. Prompt engineering exige calibração contínua com o modelo-alvo, não reutilização cega de templates.

Isso não significa que boas práticas não se transferem — significam. *Especificidade*, *roles bem definidos*, *few-shot com exemplos honestos*: tudo isso funciona em qualquer modelo capaz. O que não se transfere é a forma exata, o tom, o nível de detalhe. Tratar o prompt como template imutável é exatamente o erro que o cargo cult comete.

## O que segue vivo

O ofício do prompt continua sendo a interface mais direta com o modelo. Três framings que sobrevivem:

### Prompt como interface

O prompt é a **API humana** do modelo. Não importa quantas camadas você adicionou em volta — em algum momento, alguém escreve texto que vai pro modelo, e a qualidade desse texto define o teto do sistema. Como toda interface, ele compõe com o resto: bom prompt sobre context ruim falha; context bom sob prompt ruim também falha.

Pense na analogia com APIs REST: você pode ter a melhor infraestrutura de nuvem do mundo, mas se o contrato da API for ambíguo — endpoints mal nomeados, parâmetros sem validação, documentação imprecisa — o sistema vai falhar nas mãos dos clientes. O prompt é exatamente isso: o contrato entre o desenvolvedor e o modelo. A clareza do contrato determina a confiabilidade do sistema.

A diferença entre uma API e um prompt, porém, é que o modelo vai *tentar* cumprir o contrato mesmo quando ele é ambíguo — enquanto uma API retorna um erro de validação. Essa tolerância do modelo é sedutora em desenvolvimento, e perigosa em produção. O comportamento de "fazer o melhor possível com o que tem" produz outputs que parecem corretos sem sê-lo, e falhas que são difíceis de reproduzir e diagnosticar.

Diferente de APIs REST, porém, modelos de linguagem são mais *tolerantes* com contratos mal escritos — o modelo vai tentar entender a intenção mesmo quando a instrução é ambígua. Isso parece uma vantagem, mas na prática é uma armadilha: o modelo vai *adivinhar* o que você quis dizer, e essa adivinhação é não-determinística. Em produção, você não quer adivinhos; quer especificações claras.

O teste prático: leia seu prompt como se fosse a primeira vez, sem o contexto mental que você carrega sobre o sistema. Se você puder interpretar uma instrução de duas formas diferentes e razoáveis, o modelo vai fazer o mesmo — inconsistentemente.

### Prompt como contrato

Um prompt bem escrito é um **contrato declarativo**: estabelece quem o modelo é, o que deve fazer, o que não deve fazer, sob que critério se autoavalia. Roles, constraints e few-shot examples são cláusulas desse contrato. A trilha trata o ofício nesse registro — não como adivinhação, como engenharia de especificação.

O que torna um contrato de prompt eficaz não é o comprimento — é a completude nas dimensões certas:

1. **Identidade** — Quem o modelo é neste sistema? (Role e persona)
2. **Tarefa** — O que ele deve fazer, em que nível de detalhe?
3. **Limites** — O que ele *não* deve fazer, explicitamente?
4. **Critério de qualidade** — Como ele sabe se fez bem? (Autoavaliação implícita via exemplos ou critério explícito)
5. **Formato de saída** — Em que forma o resultado deve chegar?

Contratos que omitem uma dessas dimensões produzem outputs instáveis na dimensão omitida. Se você não especificou formato, o modelo escolhe o que parece razoável para ele — que pode não ser o que você quer. Se não especificou limites, o modelo vai além quando achar que isso ajuda — o que é especialmente problemático em contextos onde limites importam (saúde, direito, finanças).

### Prompt como camada

Quando você modela um sistema em camadas (ver [[AI Engineering Stack]]), o prompt vira uma **camada nomeada** com responsabilidade clara: especificar comportamento. Separada de Context Layer (conhecimento), Output Layer (formato), Guardrail Layer (limites impostos por código). Como qualquer camada, é versionada, testada, deployada.

A vantagem de tratar o prompt como camada é que erros ficam localizados. Quando o sistema retorna outputs errados, você pode isolar: é o prompt (instrução ambígua)? É o contexto (dado errado inserido)? É o guardrail (constraint mal especificado)? Sem separação clara, o debug vira chute.

Equipes maduras colocam o system prompt em git como qualquer outro arquivo de configuração. Cada mudança tem um PR, um diff, uma justificativa. Quando um release do Claude quebra comportamento esperado, a equipe olha o diff entre a versão que funcionava e a atual — e tem o que comparar. Sem versionamento de prompt, esse processo é impossível.

## Onde mora dentro do AI Engineering Stack

Esta trilha mora explicitamente dentro de uma camada: [[03-Dominios/Tecnologia/IA/AI Engineering Stack/03 - Prompt Layer|AI Engineering Stack — Prompt Layer]]. A relação:

```
AI Engineering Stack (11 camadas)
└── Layer 03 — Prompt Layer
    └── Prompt Engineering (esta trilha)
        ├── Especificidade
        ├── Roles e personas
        ├── Few-shot
        ├── Constraints
        ├── Iteration
        ├── Reasoning models
        └── Anti-patterns
```

Em paralelo, [[Context Engineering]] mora *acima* de várias camadas — orquestra Prompt Layer + Context Layer + Memory Layer + Retrieval Layer. **Context Engineering não substitui Prompt Engineering; contém.** A relação não é "morreu / vingou", é "menor dentro de maior".

### Por que a posição dentro do stack importa para o engenheiro

Quando você tem clareza de que o prompt vive em uma camada específica, o design do sistema muda. Em vez de perguntar *"como faço meu prompt resolver tudo?"*, você pergunta *"o que este prompt precisa especificar, e o que pertence a outras camadas?"*

Exemplos práticos dessa separação:

- **Conhecimento do domínio** — não vai no prompt. Vai no contexto (RAG, base de dados, documentos). O prompt diz *como usar* o conhecimento, não carrega o conhecimento em si.
- **Regras de negócio imutáveis** — podem ir no prompt (como constraints) ou num guardrail de código. O prompt é mais flexível; o código é mais confiável para regras que não podem ser violadas.
- **Tom e persona** — vai no prompt. É comportamento, não dado.
- **Histórico de conversa** — vai no contexto. O prompt não deveria replicar estado que o sistema gerencia.

Essa clareza de responsabilidade é o que diferencia um sistema bem arquitetado de um prompt enorme que tenta fazer tudo e falha em condições de borda.

## Sinais de que prompt engineering segue carregando peso

- **Karpathy publicar prompt.** Em 2025, Karpathy circulou o sistema anti-sycophancy ([[04 - O mega-prompt do Karpathy — anatomia da anti-sycophancy|nota 04]]). Quem diz que prompt morreu não publica template de prompt.
- **Anthropic e OpenAI manterem docs de prompt engineering ativas.** Páginas de melhores práticas continuam recebendo atualização — porque o efeito é real e mensurável em evals.
- **Papers continuam saindo.** *The Prompt Report* (Schulhoff et al., 2024) cataloga 58 técnicas distintas. Disciplina morta não tem survey acadêmico.
- **Modelos novos quebram prompts antigos.** Cada release exige re-tune do system prompt. Se prompt não importasse, isso não aconteceria.

### A evidência mais honesta: o custo de ignorar

Quando equipes decidem *"não vamos nos preocupar com o prompt, o modelo é bom o suficiente"*, o que acontece é previsível: o comportamento é inconsistente, os outputs variam muito entre runs similares, e o sistema produz alucinações onde um contrato mais explícito as eliminaria. O custo de um prompt mal especificado não é um crash — é um produto que funciona 60% do tempo e ninguém sabe por quê os outros 40% falham.

Isso não é teórico. Times que investiram em prompt engineering estruturado — roles claros, constraints explícitas, few-shot calibrado — reportam redução de hallucination rate mensurável. Não porque prompt é magia, mas porque instrução clara reduz ambiguidade, e ambiguidade é a principal causa de comportamento inesperado em LLMs.

## O papel do prompt em sistemas agênticos

O argumento mais forte para "prompt engineering morreu" vem dos sistemas agênticos: loops que rodam por horas, chamam ferramentas, tomam decisões, orquestram sub-agentes. Num sistema assim, o prompt inicial parece irrelevante — o que importa é toda a arquitetura.

Esse argumento confunde **o prompt que você vê** com **todos os prompts do sistema**.

Um sistema agêntico típico tem múltiplos prompts:
- **Orquestrador principal** — define a persona e a estratégia geral
- **Prompts de sub-tarefa** — instruções específicas para cada ferramenta ou sub-agente
- **Prompts de verificação** — critérios para o modelo avaliar seus próprios outputs
- **Prompts de formatação** — como estruturar resultados antes de passar para a próxima etapa

Num sistema com 10 sub-agentes, você tem pelo menos 10-15 prompts para escrever e manter. A disciplina de prompt engineering não desaparece — ela se *multiplica*. E a complexidade adicional de manter todos esses prompts coerentes entre si torna o ofício ainda mais crítico.

O que muda em sistemas agênticos é que um prompt mal escrito não apenas produz um output ruim — ele pode iniciar uma cascata de erros que se amplifica ao longo do loop. O orquestrador interpreta mal a tarefa, delega incorretamente para sub-agentes, que produzem resultados parciais, que o orquestrador sintetiza erroneamente. Em sistemas de múltiplos passos, a qualidade do prompt de entrada determina se os erros se acumulam ou se cancelam.

A lição: em sistemas agênticos, prompt engineering importa *mais*, não menos — só que distribuído por mais pontos de falha.

Para o engenheiro que constrói um agente pela primeira vez, a sensação é de que a complexidade vem da orquestração. Na prática, a maioria dos bugs de comportamento vêm de prompts de sub-tarefas mal especificados: o sub-agente entende a tarefa de forma diferente do que o orquestrador esperava, e o loop inteiro deriva. Corrigir esses bugs exige ler o prompt do sub-agente, não apenas o código de orquestração.

## Evolução histórica da disciplina

Para entender onde estamos, ajuda ver de onde viemos.

**2020-2022 — A era GPT-3:** Prompt engineering nasceu como *black art*. Os modelos eram menos previsíveis, e encontrar a formulação certa parecia mais alquimia do que engenharia. Nessa época, "jailbreaks" e "magic phrases" tinham efeito real porque os modelos eram sensíveis ao framing de formas imprevisíveis. O hype de "prompt como habilidade mágica" tem raízes aqui.

**2023 — O boom:** ChatGPT populariza o campo. Cursos, ebooks, cargos de *"Prompt Engineer"* surgem. Anthropic e OpenAI publicam guias. A disciplina existe, mas está inflada por expectativas irreais. É nessa fase que se vende "a frase certa que muda tudo".

**2024 — A correção:** Modelos como Claude 3, GPT-4 Turbo mostram que instruções razoáveis produzem resultados razoáveis. O diferencial de uma frase *mágica* diminui. Context engineering começa a ganhar tração como campo maior. O mercado percebe que sistemas robustos precisam de retrieval, memória, guardrails — não só de um bom system prompt.

**2025-2026 — A maturidade:** A poeira assenta. Prompt engineering é uma camada essencial dentro de um stack maior. Profissionais que dominam *toda* a stack — e sabem o papel do prompt dentro dela — são os mais valorizados. O cargo de "prompt engineer" como função isolada está morto; o *ofício* de escrever prompts bem está mais vivo do que nunca.

Essa linha do tempo importa porque diz onde a trilha se posiciona: estamos na fase de maturidade, não no boom. A abordagem aqui é de engenharia, não de alquimia.

## Como avaliar se um prompt está funcionando

Uma pergunta prática que a discussão "morreu / não morreu" raramente responde: *como você sabe se seu prompt é bom?*

A resposta honesta é: **evals**. Sem um conjunto de casos de teste com resultados esperados, você está no escuro. Um prompt que funciona nos seus 5 exemplos favoritos pode falhar nos outros 500 casos de produção. Isso é verdade tanto para prompts simples quanto para system prompts complexos de produtos.

O que medir:
- **Consistência:** para a mesma entrada, o output varia muito entre runs?
- **Precision:** o output contém informação que não foi pedida ou que é incorreta?
- **Coverage:** o output cobre o que foi pedido sem omitir partes críticas?
- **Format adherence:** o modelo segue as constraints de formato quando elas importam?

Nenhuma dessas métricas substitui o julgamento humano em casos limítrofes — mas elas transformam "sinto que o prompt está bom" em "o prompt passa em 94% dos casos de teste". A trilha de [[Evaluation]] no AI Engineering Stack entra aqui; esta nota só situa que a pergunta "como saber se funciona?" é inseparável do ofício de escrever prompts.

O mínimo viável de avaliação é uma coleção de 10-20 exemplos com outputs esperados, revisados a cada mudança significativa de prompt ou troca de modelo. Não é perfeito — mas é o que separa "funciona no meu ambiente" de "tem evidência de que funciona". Para sistemas em produção com usuários reais, o investimento em evals deve crescer proporcionalmente ao risco das decisões que o sistema toma.

## A síntese honesta

A frase certa é: **prompt engineering é uma disciplina menor do que prometeram, e maior do que mataram.**

- Menor: não é a disciplina inteira de AI engineering, é uma camada.
- Maior: ainda é onde o comportamento do modelo é especificado, e nenhuma camada acima salva um prompt mal escrito.

O engenheiro que ignora prompt engineering por achar que é coisa do passado vai criar sistemas inconsistentes sem saber por quê. O engenheiro que acha que só precisa de prompt engineering vai criar demos impressionantes que não escalam. A posição correta é no meio: **prompt engineering é uma camada que você domina como parte de um stack.**

Dominar uma camada significa entender suas responsabilidades, seus limites, e suas interfaces com as camadas adjacentes. Não significa ser capaz de resolver tudo nessa camada — significa saber quando delegar para outro nível do sistema e quando o problema está, de fato, na instrução.

A trilha existe pra tratar essa camada com seriedade — sem o ar de promessa mágica de 2023, sem o niilismo de quem leu meio tweet do Karpathy.

> [!tip] Como usar esta trilha
> Cada nota subsequente trata uma alavanca específica. Você pode ler em ordem (recomendado na primeira passagem) ou pular para um tópico específico se tiver uma necessidade imediata. O índice de [[index|Prompt Engineering — MOC]] organiza as notas com contexto adicional sobre quando cada técnica importa mais. As notas são intencionalmente focadas: uma alavanca por nota, não um guia exhaustivo. Para profundidade máxima, cada nota lista fontes que vão além do que está aqui.

## Quem precisa aprender e quando importa mais

Prompt engineering não é igualmente crítico para todos. Aqui está uma leitura honesta de onde o ROI é mais alto:

**Alta prioridade:**
- **Engenheiros construindo produtos com LLM** — o system prompt é parte do produto. Um prompt ruim é um bug de produto, não um bug de código.
- **Times usando LLMs internamente para automação** — pipelines de processamento, classificação, extração. Prompt impreciso = dados ruins no downstream.
- **PMs e designers de AI-native products** — precisam entender o que é possível especificar e o que não é, para não prometer features impossíveis.

**Média prioridade:**
- **Engenheiros usando LLMs como ferramentas de desenvolvimento** (Copilot, Claude Code, etc.) — boas práticas de prompting melhoram a qualidade dos outputs, mas o custo de um prompt ruim é baixo (você itera rapidamente).

**Menor prioridade imediata:**
- **Usuários finais de produtos com LLM** — o produto deveria absorver a complexidade de prompting. Se um usuário precisa aprender prompt engineering para usar seu produto, é um problema de design, não do usuário.

A hierarquia muda conforme a exposição ao modelo aumenta. Quanto mais próximo da camada de modelo, mais crítica a habilidade.

Para engenheiros em entrevistas para posições de AI engineering: a capacidade de articular o papel do prompt dentro de um stack maior — e não apenas "escrever prompts que funcionam" — é o sinal que diferencia candidatos que entendem o campo de candidatos que seguiram hypes. As entrevistas mais exigentes pedem que você explique por que um sistema falhou e como você diagnosticaria o ponto de falha. Sem clareza sobre o papel de cada camada, essa pergunta é impossível de responder bem.

## Armadilhas comuns

> [!warning] Jogar fora o bebê com a água do banho
> O meme "prompt engineering morreu" levou muitos engenheiros a ignorar completamente a qualidade do prompt, apostando que o modelo *"se vira"*. Na prática, system prompt mal estruturado penaliza o sistema inteiro — nenhuma camada de retrieval ou guardrail compensa uma instrução ambígua. **Como evitar:** trate o system prompt como especificação técnica, não como mensagem de chat. Revise, versione, teste com evals.

> [!warning] Confundir contexto com prompt
> "Context engineering" virou buzzword, e muita gente passou a chamar tudo de context — incluindo o prompt em si. A confusão obscurece responsabilidades: o prompt especifica *comportamento*; o contexto fornece *conhecimento e estado*. Misturar os dois torna difícil debugar qual camada falhou. **Como evitar:** mapeie explicitamente o que é instrução (prompt), o que é dado (contexto) e o que é limite (guardrail).

> [!warning] Tratar prompt como artefato estático
> Equipes lançam um system prompt em produção e nunca mais mexem. Com cada atualização de modelo, o comportamento deriva — às vezes sutilmente, às vezes catastroficamente. Quando o Claude 3.5 Sonnet foi substituído pelo Claude 3.5 Sonnet v2, equipes sem testes de regressão descobriram mudanças de comportamento semanas depois, em produção. **Como evitar:** inclua o system prompt no CI; rode uma bateria mínima de evals a cada troca de modelo. Prompt é código: vive em git, tem testes, tem deploy.

## Como explicar em inglês

> "Prompt engineering isn't dead — it just got scoped. It used to be oversold as the whole discipline; now it's clearly one layer in a larger system. But that layer still determines the model's behavior, and no amount of retrieval or orchestration fixes a badly specified prompt."

| Português | English |
|---|---|
| Engenharia de prompt | Prompt engineering |
| Camada de prompt | Prompt layer |
| Bala de prata | Silver bullet |
| Engenharia de contexto | Context engineering |
| Contrato declarativo | Declarative contract |
| Cargo cult | Cargo cult |
| Sistema agêntico | Agentic system |
| Anti-servilidade | Anti-sycophancy |

## O que vem a seguir

Se prompt engineering é uma camada com responsabilidade clara — especificar comportamento — a próxima pergunta é: *qual é o primeiro gesto concreto ao escrever um prompt?* A resposta é **especificidade**: a disciplina de reduzir o espaço de interpretação do modelo ao mínimo necessário para que ele não precise adivinhar. Sem especificidade, o modelo preenche as lacunas com defaults — e os defaults raramente são o que você quer. [[02 - Especificidade — a primeira disciplina]] entra nesse ponto.

## O que esta trilha cobre — e o que não cobre

Para ser honesto sobre o escopo:

**Esta trilha cobre:**
- Especificidade: como reduzir ambiguidade na instrução (nota 02)
- Roles e personas: como o framing de identidade afeta o comportamento (nota 03)
- Mega-prompts: anatomia de prompts longos e complexos, com o caso Karpathy (nota 04)
- Few-shot: uso de exemplos como especificação implícita (nota 05)
- Constraints declarativas: como especificar limites de forma que o modelo respeite (nota 06)
- Iteration patterns: como iterar sobre um prompt de forma sistemática (nota 07)
- Reasoning models: como o framing muda para modelos com raciocínio estendido (nota 08)
- Anti-patterns: os erros mais comuns e como evitá-los (nota 09)

**Esta trilha não cobre:**
- RAG e retrieval — pertence à [[RAG e Vector Databases]]
- Memória de sessão e entre sessões — pertence à [[Memória de Agentes]]
- Guardrails e safety de aplicação — pertence à [[Segurança e Guardrails]]
- Evals e métricas — pertence à [[Evaluation]]
- Orquestração de agentes — pertence à [[Anatomia de Agents]]

O perímetro é deliberado: esta trilha trata o *ofício da instrução*, não o stack completo. Se você precisar combinar com as outras trilhas, os wikilinks acima são os pontos de entrada.

## Fontes

- **@hooeem** — *Become an AI Engineer*, cap #1. Posição "prompt engineering ainda importa" como contraponto ao discurso dominante. Estrutura a trilha como uma das disciplinas fundamentais dentro de AI engineering, não como skill isolada.
- **Andrej Karpathy** — Tweet "context engineering > prompt engineering" (jun 2025). O argumento original que gerou o debate; vale ler o contexto completo, que é mais nuançado do que o meme sugere.
- **Anthropic** — *Prompt engineering overview* (docs.anthropic.com). Documentação ativa que continua sendo atualizada com cada versão do Claude — evidência de que o efeito é real e mensurável.
- **Schulhoff et al.** — *The Prompt Report: A Systematic Survey of Prompting Techniques* ([arxiv:2406.06608](https://arxiv.org/abs/2406.06608), 2024). 58 técnicas catalogadas, survey mais abrangente da área até a data de publicação.

## Veja também

- [[03-Dominios/Tecnologia/IA/AI Engineering Stack/03 - Prompt Layer|AI Engineering Stack — Prompt Layer]] — a camada onde esta trilha mora; explica a relação com as outras 10 camadas do stack
- [[03-Dominios/Tecnologia/IA/Context Engineering/01 - De prompt engineering a context engineering|Context Engineering — De prompt a context engineering]] — o framing "evolução" complementar; como o campo se expandiu para além do prompt isolado
- [[02 - Especificidade — a primeira disciplina]] — próxima nota: a primeira alavanca prática, o gesto mais impactante ao escrever um prompt
- [[09 - Anti-patterns e tells de IA — o que evitar]] — o lado cultural do ofício: os erros que persistem mesmo depois que você entende os fundamentos
- [[03-Dominios/Tecnologia/IA/Evaluation/index|Evaluation]] — como medir se um prompt está funcionando; complemento indispensável desta trilha
- [[03-Dominios/Tecnologia/IA/Anatomia de Agents/index|Anatomia de Agents]] — onde prompt engineering se multiplica: um agente tem muitos prompts, não apenas um
