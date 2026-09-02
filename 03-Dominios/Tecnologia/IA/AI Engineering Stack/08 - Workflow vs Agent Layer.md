---
title: "Workflow vs Agent Layer"
created: 2026-05-28
updated: 2026-07-06
type: concept
status: growing
fase: iniciado
tags:
  - ai-engineering-stack
  - ia
  - arquitetura
  - agents
publish: true
aliases:
  - Workflow vs Agent
  - Camada de arquitetura
---

# Workflow vs Agent Layer

> [!abstract] TL;DR
> A pergunta mais consequente do stack: **caminho fixo (workflow) ou descoberto dinamicamente (agent)?** Workflow quando o passo-a-passo é conhecido e pode ser codificado — você orquestra LLMs em nós de um pipeline determinístico. Agent quando o caminho precisa ser descoberto em tempo de execução — o LLM escolhe a próxima ação em loop até decidir parar. A regra cardinal: **não construa agent por padrão**. Agent custa mais, falha de formas mais criativas, e debuga pior. Use workflow até provar que não resolve — e esse limiar é mais alto do que parece.

> [!question]- Quando realmente vale a pena construir um agent?
> A resposta honesta: quase nunca na primeira versão. Agent parece a escolha natural quando o domínio é "complexo" — mas complexidade no domínio não implica que o *caminho de solução* precisa ser descoberto em tempo de execução. Na maioria dos casos, a tarefa tem estrutura — você só não mapeou ainda. Workflows com routing e padrões intermediários resolvem ~80% dos problemas que as equipes acreditam precisar de agent. Use agent quando você puder provar que o caminho não pode ser predefinido.

## O problema que esta camada resolve

Você tem um modelo que responde bem. Você tem tools. Você tem contexto. Agora a pergunta que define a arquitetura inteira: como esses blocos se conectam?

Se a resposta é "o modelo decide em tempo de execução" — você escolheu agent. Se a resposta é "o código define a sequência de passos" — você escolheu workflow. A diferença não é de poder expressivo: qualquer coisa que um agent faz pode ser modelada como workflow com caminhos condicionais suficientes. A diferença é de **custo de engenharia, confiabilidade e debugabilidade**.

O erro mais frequente: construir agent porque o domínio parece "complexo" ou porque a demo com agent ficou impressionante. A maioria dos sistemas de produção que parecem precisar de agent funcionam bem — e melhor — como workflow com um conjunto rico de nós condicionais.

## Workflow vs Agent: o contraste

```mermaid
flowchart LR
    classDef ok fill:#4ADE8021,stroke:#4ADE80,color:#E9ECF2
    classDef destaque fill:#FFAA0024,stroke:#FFAA00,color:#E9ECF2
    subgraph "Workflow (caminho fixo)"
        A1["Input"]
        A2["Nó A\npré-definido"]
        A3["Nó B\npré-definido"]
        A4["Output previsível\ne auditável"]
    end

    subgraph "Agent (caminho dinâmico)"
        B1["Input"]
        B2["LLM decide\npróxima ação"]
        B3["Executa ação\nou ferramenta"]
        B4["LLM decide\nparar ou continuar"]
        B5["Output variável\nper execução"]
    end

    A1 --> A2 --> A3 --> A4
    B1 --> B2 --> B3 --> B4
    B4 -->|"continua"| B2
    B4 -->|"para"| B5

    class A4 ok
    class B5 destaque
```

## O que é esta camada

Esta camada não produz um template YAML — produz uma **decisão arquitetural** que determina o restante do stack: tools necessárias, estilo de eval, tipo de logging, custo, latência e confiabilidade.

A taxonomia da Anthropic em *Building effective agents* (2024) é útil:

| Tipo | Definição | Quem controla o fluxo |
|------|-----------|----------------------|
| **Building block** | LLM com retrieval, tools e memória — o átomo | — |
| **Workflow** | Building blocks orquestrados em **caminho predefinido** por código | Código |
| **Agent** | LLM em loop decidindo a próxima ação até concluir | Modelo |

Os padrões intermediários — que cobrem a maioria dos sistemas de produção — são workflows com nós mais ricos:

- **Prompt chaining** — output de um LLM vira input do próximo (pipeline linear)
- **Routing** — um classificador decide qual nó executar (condicional)
- **Parallelization** — múltiplos LLMs em paralelo, resultados agregados
- **Orchestrator-workers** — um LLM coordena outros LLMs especializados
- **Evaluator-optimizer** — um LLM avalia o output do outro e solicita revisão

Esses padrões são mais confiáveis, mais baratos e mais debugáveis que agent puro.

## Decisões-chave

**1. O caminho é previsível?** Se você consegue desenhar o fluxograma inteiro antes de executar, é workflow. Se os nós e arestas dependem do input de cada etapa de formas que você não consegue prever antecipadamente, é agent. Teste: você conseguiria escrever o diagrama de sequência antes de rodar? Sim → workflow.

**2. Custo do erro vs custo da rigidez.** Agent erra de formas mais variadas (o loop pode divergir, entrar em ciclo ou parar antes de concluir) mas é flexível para casos inesperados. Workflow erra de forma previsível e em casos não cobertos, mas falha de modo limpo. Onde o custo do erro é alto — decisões financeiras, ações irreversíveis, sistemas médicos — prefira a falha previsível do workflow à falha criativa do agent.

**3. Profundidade do loop agentic.** Agent que precisa de 2-3 chamadas para resolver o problema é razoável. Agent que precisa de 30 chamadas geralmente está mascarando um workflow mal modelado — a tarefa tem um caminho, você só não o mapeou ainda. Quando o loop fica muito profundo, refatore em workflow.

**4. Debugabilidade e cost.** Workflow é debugável passo a passo: você sabe exatamente o que foi executado e em que ordem. Agent requer tracing pesado para entender por que escolheu cada ação — sem Logging Layer forte, agent é caixa-preta. Além disso, cada passo do loop é uma chamada ao modelo: agent com loop de 10 passos custa 10× o de uma única chamada.

**5. Padrões intermediários são a resposta certa na maioria dos casos.** Antes de construir agent puro, pergunte: este problema cabe em orchestrator-workers? Em evaluator-optimizer? Em routing com nós especializados? Esses padrões têm as vantagens de flexibilidade dos agents com muito mais previsibilidade de workflows.

## Casos práticos

### Cenário 1 — Agent onde workflow bastaria

Sistema de geração de relatórios financeiros. A equipe construiu um agent porque "o relatório tem seções diferentes dependendo do tipo de empresa". O agent decide em cada execução quais seções incluir, em que ordem, com quais dados.

Em produção: loop diverge em ~8% dos relatórios (agent inclui seção duplicada ou pula seção obrigatória). Debug é difícil porque cada execução toma um caminho diferente. Custo por relatório é 3× o estimado.

A solução: routing + workflow. Um classificador identifica o tipo de empresa (3 tipos) e roteia para um de 3 templates de workflow fixos. Cada template tem as seções certas, na ordem certa, com os dados certos. Taxa de erro: <0.1%. Custo: 1/3 do agent. Debugging: determinístico.

### Cenário 2 — Agent genuíno: pesquisa aberta

Sistema de pesquisa competitiva: "analise os três maiores concorrentes e identifique oportunidades de diferenciação". O número de etapas, as fontes a consultar, e as dimensões de análise dependem do que é encontrado em cada passo. Um workflow fixo seria muito rígido — há dimensões que só surgem depois de ler o primeiro relatório.

Este é um caso genuíno de agent: o caminho não pode ser predefinido porque depende do que é descoberto durante a execução. Aqui, o custo e a imprevisibilidade de agent são aceitáveis porque a flexibilidade é o valor central do sistema.

### Cenário 3 — O caso limítrofe: quando um workflow *precisa* virar agent

Nem toda decisão workflow-vs-agent acontece uma vez só, no design inicial. Às vezes a decisão certa no dia 1 deixa de ser certa no mês 8 — e o sinal de que chegou a hora de migrar é mais sutil do que "o workflow quebrou".

> [!question]- Como saber que um workflow que funcionava bem começou a ficar rígido demais?
> O sintoma não é erro — é **crescimento do código de roteamento**. Se a cada novo caso de uso alguém precisa adicionar mais um `if` na árvore de decisão, e essa árvore já passou de dezenas de ramos, o workflow não está mais modelando "casos previstos": está tentando simular, em código estático, uma decisão que deveria ser feita em tempo de execução.

Uma equipe de suporte ao cliente construiu um workflow de triagem: um classificador identificava a categoria do ticket (cobrança, bug, dúvida de produto, cancelamento) e roteava para um template de resposta por categoria — exatamente o padrão de routing recomendado para este tipo de problema. Funcionou bem por meses, com 6 categorias e taxa de erro baixa.

O problema apareceu quando o catálogo de produtos triplicou e o número de categorias de ticket subiu para mais de 40, muitas delas com sobreposição ("cobrança de produto cancelado" é cobrança ou cancelamento?). A árvore de routing virou uma cascata de exceções e casos especiais — cada ticket ambíguo exigia um novo ramo manual. O workflow não tinha ficado "errado"; o espaço de casos cresceu além do que routing fixo consegue cobrir sem reescrita constante.

A migração: em vez de um classificador de categoria fixa, um agent com acesso a tools (busca no catálogo, histórico do cliente, política de reembolso) decide, ticket a ticket, quais informações precisa consultar antes de responder — sem uma árvore de categorias pré-definida. O ganho não foi velocidade nem custo (o agent é mais caro por ticket) — foi a eliminação da manutenção constante da árvore de routing, que já consumia mais engenharia do que o valor entregue.

> [!summary] O sinal de migração
> Não é "o workflow errou uma vez". É "o custo de manter a árvore de decisão cresce mais rápido que o valor que ela entrega" — o caminho deixou de ser previsível o suficiente para compensar codificá-lo à mão.

## Frameworks que implementam a distinção

A distinção workflow-vs-agent não é só conceitual — ela molda qual ferramenta você escolhe para implementar. Dois mundos de frameworks surgiram, cada um otimizado para um lado da decisão.

> [!question]- Por que não existe um framework único que resolve os dois casos igualmente bem?
> Porque as garantias que cada lado precisa são diferentes. Workflow quer **execução durável e auditável de um caminho conhecido** — o framework precisa garantir que, mesmo com falhas de infraestrutura, cada passo previsto rode até o fim, na ordem certa. Agent quer **um jeito ergonômico de modelar um grafo de estados que o próprio modelo navega** — o framework precisa expor ciclos, condicionais dinâmicas e memória de forma que o LLM consiga decidir a próxima aresta. Otimizar para as duas coisas ao mesmo tempo dilui as duas.

**LangGraph** modela agents como grafos de estado explícitos: nós são passos (chamadas ao LLM, tools), arestas podem ser condicionais e — a diferença central em relação a workflow puro — o próprio grafo permite ciclos, onde o LLM decide se volta a um nó anterior ou segue em frente. É a ferramenta certa para a *lógica de decisão* do agent: memória, streaming, observabilidade por trace (tokens, custo, latência).

**Temporal** (e, num nicho adjacente, **Prefect**) resolvem o problema oposto: execução durável de um processo já definido. Temporal garante que um workflow de longa duração — horas ou dias, com múltiplas chamadas externas — complete mesmo que a infraestrutura caia no meio do caminho, com retries e persistência de estado geridos pela plataforma, não pelo código da aplicação. Prefect ocupa um espaço parecido, geralmente com menos cerimônia de configuração, para equipes que priorizam simplicidade sobre garantias de nível financeiro.

Isso leva a um padrão de arquitetura híbrida cada vez mais comum: **Temporal (ou Prefect) na camada macro** — o ciclo de vida durável do job, com retries e checkpoints — e **LangGraph na camada micro**, dentro de uma única etapa desse job, para o raciocínio cíclico e imprevisível do agent. Ou seja: o workflow durável envolve o agent, não o substitui. A pergunta "workflow ou agent" desta nota decide o *miolo* de cada etapa; a escolha de framework de durabilidade decide como esse miolo sobrevive a falhas de longo prazo.

| Framework | Resolve | Garantia central |
|-----------|---------|-------------------|
| LangGraph | Lógica do agent (grafo de estados navegado pelo LLM) | Ciclos, memória, observabilidade por trace |
| Temporal | Execução durável de processos de longa duração | Completude mesmo com falha de infraestrutura |
| Prefect | Orquestração de pipelines, com menos cerimônia que Temporal | Agendamento e retries com setup mais simples |

```mermaid
flowchart TB
    classDef neutro fill:#1B2029,stroke:#4E5666,color:#C6CCD8
    classDef destaque fill:#FFAA0024,stroke:#FFAA00,color:#E9ECF2
    subgraph macro ["Camada macro — Temporal / Prefect"]
        direction LR
        M1["Job de longa duração\nrecebido"] --> M2["Checkpoint\npersistido"]
        M2 --> M3["Retry automático\nse infra falhar"]
        M3 --> M4["Job completo\nmesmo após horas"]
    end

    M2 -.->|"dentro de uma etapa do job"| micro

    subgraph micro ["Camada micro — LangGraph"]
        direction LR
        A1["Nó: LLM decide\npróxima ação"] --> A2["Nó: executa\ntool"]
        A2 --> A3["Nó: LLM avalia\nresultado"]
        A3 -->|"ciclo"| A1
        A3 -->|"conclui"| A4["Retorna à camada macro"]
    end

    class macro neutro
    class micro destaque
```

O diagrama deixa explícito o que a tabela só descreve: a camada macro não substitui a decisão desta nota — ela só garante que, uma vez que você decidiu que uma etapa é agent (o grafo cíclico do LangGraph), essa etapa sobrevive a falhas de infraestrutura sem perder o progresso já feito.

## Armadilhas comuns

> [!warning] Construir agent por padrão ou por impressão
> "A demo ficou incrível" não é critério arquitetural. Agent impressiona em demos porque parece autônomo e inteligente — em produção, essa autonomia é exatamente o que produz falhas imprevisíveis. O ônus da prova é do agent: só use quando você provar que workflow não resolve o problema.

> [!warning] Não calcular custo do loop agentic
> Cada chamada ao modelo no loop tem custo. Um agent com loop médio de 8 passos e 5.000 chamadas por dia é 40.000 chamadas ao modelo por dia — talvez 10× o orçamento previsto. Calcule custo por execução antes de escolher agent, não depois do faturamento chegar.

> [!warning] Agent sem kill switch
> Loop agentic sem condição de parada explícita pode rodar indefinidamente — ou até atingir o limite de contexto da API e falhar com erro. Defina sempre: número máximo de iterações, custo máximo por sessão, e comportamento quando esses limites são atingidos. Esses kill switches vivem na Guardrail Layer.

> [!question]- Como esse loop "sem freio" quebra na prática?
> Cada iteração do loop agentic acrescenta a ação anterior e o resultado dela ao histórico enviado no próximo prompt — o contexto só cresce, nunca encolhe sozinho. Sem um limite explícito, o loop não para por "decisão ruim" isolada: ele para porque o histórico acumulado excede a janela de contexto do modelo, e a chamada seguinte falha com erro de tamanho — geralmente no meio de uma tarefa, sem ter produzido resposta útil.

```python
# Sem kill switch: o loop só termina quando o modelo decide parar —
# ou quando o contexto acumulado estoura o limite da API.
def run_agent(task):
    history = [task]
    while True:
        response = llm.call(history)          # cada chamada reenvia TODO o histórico
        if response.is_final:
            return response
        action_result = execute(response.action)
        history.append(response)
        history.append(action_result)         # histórico só cresce — nunca é podado
        # se o modelo nunca decidir parar, ou ficar preso revisando
        # a mesma ação, isto roda até o request falhar por excesso de tokens

# Com kill switch: iterações, custo e comportamento de parada são explícitos —
# a falha vira um retorno controlado, não uma exceção de contexto estourado.
def run_agent_safe(task, max_iterations=8, max_cost_usd=2.00):
    history = [task]
    cost = 0.0
    for step in range(max_iterations):
        response = llm.call(history)
        cost += response.cost_usd
        if response.is_final:
            return response
        if cost > max_cost_usd:
            return AbortedResult(reason="max_cost_exceeded", step=step)
        action_result = execute(response.action)
        history.append(response)
        history.append(action_result)
    return AbortedResult(reason="max_iterations_exceeded", step=max_iterations)
```

O segundo bloco não torna o agent "mais inteligente" — só transforma uma falha inevitável (estouro de contexto, custo sem teto) em uma falha *previsível e tratável*, o mesmo valor que o workflow entrega por padrão.

## Critérios objetivos para a decisão workflow vs agent

Em vez de intuição, use estas perguntas como checklist antes de decidir:

**O caminho tem estrutura previsível?**
- Sim, sempre os mesmos passos → workflow puro
- Sim, mas com condicionais → workflow com routing
- Depende do input em formas que não consigo antecipar → candidate a agent

**Qual é o custo tolerável por execução?**
- Orçamento muito apertado por query → workflow (custo fixo e previsível)
- Pode absorver variabilidade → agent pode ser aceitável

**Qual é o custo do erro?**
- Ação irreversível, impacto financeiro, segurança → workflow (falha previsível)
- Erro recuperável, ambiente exploratório → agent pode ser aceitável

**A equipe tem capacidade de debugar agent?**
- Sem Logging Layer forte e tracing → não construa agent ainda
- Instrumentação completa, observabilidade em place → agent é mais viável

**O loop precisaria de quantas iterações em média?**
- 1-3 iterações → talvez seja só um workflow com retentativas
- 4-10 → agent legítimo com kill switch
- 10+ → provavelmente um workflow mal modelado

> [!summary] Regra de ouro
> Workflow é o padrão. Agent é a exceção. O ônus da prova é sempre do agent.

## Como explicar em inglês

The Workflow vs Agent Layer is the most consequential architectural decision in the stack. Workflows are LLM-powered pipelines where the sequence of steps is predetermined by code — predictable, debuggable, cost-controlled. Agents are LLMs in a loop that decide their own next action — flexible, powerful, but expensive and harder to debug. The default should be workflow. Build agents only when you can prove the path cannot be predetermined. Most production systems that seem to need agents are actually best served by richer workflow patterns: routing, parallelization, orchestrator-workers, or evaluator-optimizer.

The nuance that separates a strong candidate in interviews: workflows can look very "smart" through rich routing and conditional logic without any agentic loop. The signal is whether the *path itself* needs to be discovered at runtime, not whether the individual steps require intelligence. A classification step that routes to one of five specialized sub-pipelines is still a workflow — the model is reasoning, but the overall structure is fixed.

> *"Most of what people call 'agents' in production are actually workflows with LLM nodes — and that's a good thing. The agentic loop should be the last resort, not the default architecture."* — Anthropic, Building effective agents (2024)

| PT | EN |
|----|----|
| Camada workflow vs agente | Workflow vs Agent Layer |
| Fluxo de trabalho | Workflow |
| Agente autônomo | Autonomous agent |
| Caminho predefinido | Predetermined path |
| Loop agentic | Agentic loop |
| Encadeamento de prompts | Prompt chaining |
| Roteamento | Routing |
| Paralelização | Parallelization |
| Orquestrador-trabalhadores | Orchestrator-workers |
| Avaliador-otimizador | Evaluator-optimizer |

## O que vem a seguir

Com a arquitetura decidida — workflow ou agent — as três próximas camadas são o **bloco de controle**: Evaluation (como saber se o output está bom), Guardrail (o que o sistema não pode fazer), e Logging (o que registrar de cada execução). Essas três camadas transformam o que você construiu em sistema confiável para produção.

A decisão mais urgente depois de workflow vs agent é a Evaluation Layer — sem rubrica de qualidade, você não tem sinal para saber se o sistema está funcionando.

- [[09 - Evaluation Layer]] — como medir se o output está bom
- [[10 - Guardrail Layer]] — o que o sistema não pode fazer
- [[Anatomia de Agents]] — trilha completa: patterns, ReAct, orchestrator-workers, planning

## Onde aprofundar

- **[[Anatomia de Agents]]** → [[10 - Workflow vs Agent — quando usar cada um]] — discussão aprofundada com critérios detalhados.
- **[[Anatomia de Agents]]** → [[08 - Patterns comuns de agents]] — orchestrator-worker, planning, ReAct.
- **Anthropic** — *Building effective agents* (2024) — a referência mais citada sobre esta distinção.

## Veja também

- [[02 - Purpose Layer — o que o sistema é]] — Purpose informa se a tarefa precisa de agent
- [[07 - Tool Layer]] — agents dependem de tools; workflows podem funcionar sem
- [[09 - Evaluation Layer]] — eval de agent é fundamentalmente mais difícil que de workflow
- [[11 - Logging Layer]] — agent sem logging forte é caixa-preta

## Fontes

- **@hooeem** — *Become an AI Engineer*, chapter #18, Step 7 (Workflow vs Agent). X/Twitter, 2025.
- **Anthropic** — [*Building effective agents*](https://www.anthropic.com/engineering/building-effective-agents) (2024). Definição de building blocks → workflows → agents + patterns intermediários.
- **Lilian Weng** — [*LLM-powered Autonomous Agents*](https://lilianweng.github.io/posts/2023-06-23-agent/) (2023). Planning, memory e tool use como componentes.
- **LangChain** — [*LangGraph vs Temporal: AI Agent Orchestration Compared*](https://www.langchain.com/resources/langgraph-vs-temporal) (2026). Distinção entre orquestração de agent (LangGraph) e execução durável de processos (Temporal), e o padrão híbrido de usar as duas camadas juntas.
