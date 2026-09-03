---
title: "Arquitetura de um sistema de memória"
created: 2026-04-25
updated: 2026-06-28
type: concept
fase: iniciado
progress: backlog
status: seedling
publish: true
tags:
  - memoria-agentes
  - ia
  - arquitetura
  - fundamentos
aliases:
  - Arquitetura de memória
  - Write-manage-read loop
  - Memory architecture
---

# Arquitetura de um sistema de memória

> [!abstract] TL;DR
> Sistemas de memória de agentes têm uma arquitetura comum, independente de implementação: **ingestão** (write), **indexação** (organização), **retrieval** (read), **manutenção** (compactação, forget, lint) e **schema/governance** (regras). O survey de 2026 (Du et al.) formaliza esse fluxo como **write-manage-read loop** e identifica 5 mecanismos arquiteturais distintos: context-resident compression, retrieval-augmented stores, reflective self-improvement, hierarchical virtual context e policy-learned management. Um framework complementar — Storage / Reflection / Experience — descreve a maturidade evolutiva de cada implementação. Este vocabulário é a base para comparar ferramentas concretas (Letta, Mem0, Zep, MemPalace, basic-memory, A-MEM) sem cair em anedota.

> [!question]- Dúvidas e lacunas desta nota
> - Dúvida gerada pelo conteúdo: A nota descreve "policy-learned management" como majoritariamente research — quais são os obstáculos concretos que impedem adoção em produção? Latência de decisão, custo de treino, instabilidade do RL reward signal?
> - Lacuna potencial: A nota classifica maturidade com o framework Storage/Reflection/Experience, mas não discute como medir onde uma implementação específica está nesses estágios — existe benchmark ou heurística prática para isso?

## O que é

A "arquitetura de um sistema de memória" não é uma arquitetura específica — é o conjunto de componentes que **toda** implementação tem em alguma forma, ainda que disfarçada. Quando se compara o LLM Wiki de [[Andrej Karpathy|Karpathy]], o servidor [[Dicionário de IA#MCP (Model Context Protocol)|MCP]] `basic-memory`, o tier system de Letta, o grafo temporal do Zep, o retrieval vetorial do Mem0 e a metáfora espacial do MemPalace, parece à primeira vista que cada um implementa algo radicalmente diferente. Não é o caso. Por baixo da superfície, todos resolvem as mesmas cinco perguntas: o que entra, como organizar, como buscar, como manter e quais são as regras.

Esse mapa arquitetural genérico é o vocabulário com o qual a trilha discute implementações específicas. As notas sobre cada ferramenta concreta — [[09 - Panorama de implementações (abril 2026)|panorama]], [[10 - LLM-knowledge-base (Wendel) — direto do gist|LLM-knowledge-base]], [[14 - Letta (ex-MemGPT)|Letta]], [[13 - basic-memory — MCP nativo Obsidian|basic-memory]], entre outras — vão se referir constantemente a esses cinco componentes. Sem o mapa, comparar implementações vira disputa de marca; com o mapa, vira conversa técnica.

## Por que importa

Sem essa base, comparar implementações vira anedota: "Mem0 é melhor que Letta", "Zep ganha do A-MEM", "use markdown e não vector DB". Com critério — qual componente cada solução prioriza, quais trade-offs assume, quais ignora — vira análise. Profissionais que conhecem o vocabulário arquitetural conseguem ler um repositório novo em 20 minutos, identificar o que ele faz bem e o que ignora, e decidir se serve para o caso de uso em mãos.

Há também um motivo pragmático: para projetar um sistema próprio (caminho previsto na nota [[23 - Guia de implementação do zero]]), o primeiro passo é mapear o caso de uso aos cinco componentes — quanto entra por dia, quão estruturada é a entrada, qual a latência aceitável de retrieval, quem mantém o sistema, quais regras de governança existem. Sem essa decomposição, o projeto começa pelo substrato (vector DB? markdown? grafo?) — que é exatamente a decisão menos importante. E para discurso público — entrevistas, talks, mentoria — o vocabulário é o que separa quem entende o campo de quem consome marketing.

## Como funciona — componentes universais

O loop fundamental é três operações em ciclo, com duas camadas de governança que perpassam tudo. O survey de Du et al. (2026) chama isso de **write-manage-read loop**, condensação útil de uma ideia que já aparecia em formas variadas em Park et al. (2023) e no gist de Karpathy.

```mermaid
graph TB
    subgraph Inputs
        I1[Conversações]
        I2[Documentos]
        I3[Eventos]
    end

    subgraph Pipeline_de_memoria [Pipeline de memória]
        ING[Ingestão<br/>write]
        IDX[Indexação]
        RET[Retrieval<br/>read]
        MAN[Manutenção<br/>manage]
        SCH[Schema/Governance]
    end

    subgraph Outputs
        O1[Resposta com contexto]
        O2[Sugestões proativas]
    end

    I1 --> ING
    I2 --> ING
    I3 --> ING
    ING --> IDX
    IDX -->|store| RET
    RET --> O1
    RET --> O2
    MAN -.->|compact/lint/forget| IDX
    SCH -.->|guides| ING
    SCH -.->|guides| MAN
```

Os cinco componentes funcionam assim:

### 1. Ingestão (write)

Decide o que entra na memória. As perguntas relevantes são: **o que filtrar**, **em que granularidade**, **quando processar** e **quem decide**. Em sistemas como o LLM Wiki, a ingestão é orquestrada por humano que decide quais fontes brutas alimentam a wiki — o [[Dicionário de IA#LLM (Large Language Model)|LLM]] compila, mas o humano cura. Em sistemas conversacionais como Mem0 e Letta, a ingestão é majoritariamente automática: o [[Dicionário de IA#Agent|agente]] extrai fatos de cada turno e decide o que persistir.

A granularidade é talvez a decisão mais subestimada. Gravar conversas inteiras é fácil mas inútil para [[Dicionário de IA#retrieval|retrieval]]; extrair fatos atômicos é caro mas alimenta busca precisa; armazenar resumos perde nuance. Cada implementação faz uma escolha aqui, e essa escolha governa muito do que vem depois. Sistemas que ingerem tudo sem filtro entram em colapso de sinal/ruído em poucas semanas — gravar tudo é gravar nada.

### 2. Indexação

Como organizar o que foi ingerido. Os eixos comuns são: **vetorial** ([[Dicionário de IA#embedding|embeddings]] + similarity search), **grafo** (entidades e relações explícitas, com travessia), **hierárquico** (tiers de memória, RAM/disk), e **espacial** (memory palace, organização por loci). Implementações reais costumam combinar: Zep usa grafo temporal, Mem0 mistura vetorial e relacional, Letta organiza em tiers explícitos de tamanho.

A decisão central é o trade-off entre **custo de write** e **custo de read**. Indexação rica (embeddings + grafo + hierarquia) gasta no momento da escrita para tornar a leitura barata e precisa; indexação minimalista (só append em arquivo) é trivial no write mas joga toda a complexidade para o read. Não há resposta universal — depende da assimetria entre frequência de ingestão e frequência de query no caso de uso.

```mermaid
quadrantChart
    title "Trade-off custo write vs custo read"
    x-axis "Custo de write baixo" --> "Custo de write alto"
    y-axis "Custo de read alto" --> "Custo de read baixo"
    quadrant-1 "Ideal — raro"
    quadrant-2 "Indexação rica"
    quadrant-3 "Append-only simples"
    quadrant-4 "Indexação cara sem retrieval"
    "Markdown append-only": [0.15, 0.2]
    "Vetor + grafo — Mem0/Zep": [0.7, 0.75]
    "Hierárquico — Letta": [0.6, 0.65]
    "Memory palace — MemPalace": [0.55, 0.85]
```

### 3. Retrieval (read)

Como buscar quando o agente precisa. Os padrões consolidados são: **similarity search** (cosine ou dot product sobre embeddings), **graph traversal** (seguir arestas a partir de entidades mencionadas), **[[Dicionário de IA#hybrid search|hybrid search]]** ([[Dicionário de IA#BM25|BM25]] lexical combinado com vetor semântico) e **[[Dicionário de IA#reranking|reranking]]** (segundo passo que reordena top-N por relevância semântica fina). Decisões importantes: tamanho do top-k, query rewriting (transformar a pergunta antes de buscar), e se há ou não cache de resultados.

Retrieval é onde a maior parte do esforço de pesquisa acadêmica se concentra — porque é mensurável: dá para benchmarkar com LongMemEval e ver número subindo. É também onde mais se exagera. Um retrieval excelente sobre uma memória mal mantida produz respostas precisamente erradas; um retrieval mediano sobre uma memória bem curada produz respostas certas. A nota [[21 - Comparativo crítico (LongMemEval)|comparativo crítico]] explora essa assimetria.

### 4. Manutenção (manage)

A operação mais negligenciada e a que mais separa sistemas reais de protótipos. Manutenção engloba: **compactação** (resumir logs antigos, reduzir verbosidade sem perder fato), **deduplicação** (detectar e fundir registros redundantes), **forget policy** (TTL, importância decay, eviction de baixo uso), e **lint** (detectar contradições, links quebrados, órfãos, schema violations).

Sem manutenção contínua, qualquer sistema de memória vira **wiki rot** — o termo é apropriado: mesmo padrão das wikis que cresceram sem manutenção e viraram cemitérios de páginas obsoletas. Em sistemas LLM o problema é pior: o agente recupera o lixo com a mesma confiança que recupera o conteúdo bom, e contamina respostas. O gist de Karpathy chama essa operação de "lint" deliberadamente, evocando o paralelo com linters de código — manutenção como prática rotineira, não como evento heroico.

### 5. Schema/Governance

As regras que governam tudo o resto: o `CLAUDE.md` ou `AGENTS.md` que ensina o LLM como organizar páginas, os YAMLs de configuração que definem TTL, os documentos de design que dizem o que constitui uma "entidade" no grafo. Schema não é apenas configuração técnica — é onde a maior parte do design real vive.

A observação contraintuitiva, e que aparece em quase toda implementação madura, é que **o substrato importa menos do que o schema**. Se duas implementações usam markdown como storage, ainda podem produzir sistemas radicalmente diferentes dependendo das regras de organização. Inversamente, um vector DB com schema bem desenhado pode emular muito do que uma implementação markdown faz. É no schema que o conhecimento operacional de cada projeto se acumula, e é por isso que documentos como o do Wendel ou o `basic-memory` README têm valor desproporcional ao tamanho — eles codificam decisões que parecem triviais até você tentar outra coisa.

## 5 mecanismos arquiteturais (do survey 2026)

Du et al. (2026) propõem uma classificação ortogonal aos cinco componentes — em vez de "o que cada sistema tem", olham para "como cada sistema resolve a memória de longo prazo". Cinco mecanismos emergem como dominantes na literatura:

1. **Context-resident compression.** Compactar o histórico dentro do próprio contexto da chamada — resumir turnos antigos, manter só fatos essenciais. Sem armazenamento externo. Limite: o que cabe no [[Dicionário de IA#Context window|context window]].

2. **Retrieval-augmented stores.** Armazenamento externo ([[Dicionário de IA#vector database|vector DB]], grafo, arquivos) acessado via query no momento da inferência — [[Dicionário de IA#RAG (Retrieval-Augmented Generation)|RAG]]-like. A maior parte das implementações comerciais (Mem0, Zep, basic-memory) cai aqui.

3. **Reflective self-improvement.** O agente reflete sobre a própria memória e a refina ativamente — extrai padrões, consolida insights, abstrai princípios. Origem em Park et al. (2023) com o ciclo observation/reflection/planning das generative agents.

4. **Hierarchical virtual context.** Analogia direta com sistemas operacionais — RAM/disk, paging entre tiers de memória de tamanhos diferentes. Letta (ex-MemGPT) é o exemplar canônico, e a metáfora "memória virtual para LLM" é a marca registrada do projeto.

5. **Policy-learned management.** Reinforcement learning aprende quando armazenar, quando esquecer, quando consolidar. Ainda majoritariamente research — pouca tração em produção, mas direção promissora para automatizar decisões de manutenção que hoje são heurísticas.

Implementações reais quase nunca implementam um mecanismo puro — são combinações. Letta é primariamente hierarchical mas usa retrieval; Zep é primariamente retrieval-augmented mas tem reflective steps; basic-memory é retrieval-augmented com compression em alguns fluxos. Os cinco mecanismos são lentes para análise, não caixas mutuamente exclusivas.

## Padrão Storage / Reflection / Experience

Um framework complementar — frequentemente referenciado na literatura como "From Storage to Experience" — descreve **maturidade evolutiva** de uma implementação em três estágios:

1. **Storage.** Preservação bruta. Memory stream do Park, log append-only do Karpathy, raw transcripts. O sistema lembra o que aconteceu, sem refinamento. Útil mas baixa densidade de sinal.

2. **Reflection.** Refinamento ativo. Resumos, extração de fatos, estruturação em entidades, identificação de relações. O sistema deixa de ser arquivo e passa a ser conhecimento organizado. É aqui que a maior parte das implementações de 2026 está.

3. **Experience.** Abstração reusável. Skills aprendidas, princípios destilados, **procedural memory** (ver [[03 - Taxonomia da memória (episódica, semântica, procedural)|taxonomia]]). O sistema deixa de só lembrar e passa a saber fazer. É o estágio mais raro, e o mais valioso para agentes que evoluem ao longo do tempo.

A utilidade prática deste framework é classificar maturidade. Quando se avalia uma ferramenta nova, perguntar "isto está em qual estágio?" é frequentemente mais informativo do que comparar features. Um sistema em estágio Storage com retrieval impecável ainda é menos poderoso do que um sistema em estágio Experience com retrieval mediano — porque o segundo destila conhecimento, e o primeiro só preserva.

## Detalhando os 5 mecanismos com exemplos práticos

A classificação de Du et al. ganha substância quando associada a exemplos concretos e ao custo relativo de cada mecanismo.

```mermaid
graph LR
    subgraph M1 ["① Context-resident compression"]
        C1["Resumir turnos antigos<br/>no próprio contexto"]
        C2["Custo: compute de summarize<br/>Limite: context window"]
    end

    subgraph M2 ["② Retrieval-augmented stores"]
        R1["RAG clássico aplicado à memória<br/>Vector DB / grafo / markdown"]
        R2["Custo: embedding + query<br/>Escala: ilimitada"]
    end

    subgraph M3 ["③ Reflective self-improvement"]
        RE1["Agente reflete sobre memória<br/>extrai padrões, consolida"]
        RE2["Custo: chamada LLM extra<br/>Valor: conhecimento destilado"]
    end

    subgraph M4 ["④ Hierarchical virtual context"]
        H1["Tiers RAM/disco<br/>Paginação entre níveis"]
        H2["Custo: orchestração de tiers<br/>Exemplar: Letta/MemGPT"]
    end

    subgraph M5 ["⑤ Policy-learned management"]
        P1["RL decide quando armazenar<br/>esquecer, consolidar"]
        P2["Custo: treino + inferência<br/>Maturidade: research"]
    end
```

**① Context-resident compression** na prática. Imagine um chatbot de suporte com histórico de 50 turnos. Em vez de truncar os turnos mais antigos (perdendo contexto) ou carregar todos (estourando o context window), o sistema compacta os 40 turnos mais antigos em um resumo de 5 parágrafos. O agente responde com os 10 turnos recentes mais o resumo. Claude Code usa variação desse mecanismo ao compactar sessões longas com `/compact`. O limite é claro: se o resumo falha em preservar um fato crítico, ele se perde para sempre — não há armazenamento externo de fallback.

**② Retrieval-augmented stores** na prática. O mesmo chatbot de suporte agora persiste cada preferência extraída do usuário em um vector DB. Quando o usuário retorna semanas depois, o agente faz similarity search de "preferências do usuário X" e recupera os fragmentos mais relevantes. `basic-memory`, Mem0 e Zep caem aqui. A diferença entre eles está no que indexam (markdown puro, fatos extraídos, grafo temporal) e como recuperam.

**③ Reflective self-improvement** na prática. O sistema de generative agents de Park et al. (2023) faz isso explicitamente: após um conjunto de interações, o agente reflete — "o que aprendi de importante sobre essa pessoa?" — e gera uma observação de alto nível que persiste. Não é só lembrar fatos; é sintetizar insights. Custo: uma chamada LLM extra a cada ciclo de reflexão. Valor: o sistema acumula conhecimento de ordem superior que não existia nos episódios brutos.

**④ Hierarchical virtual context** na prática. Letta (ex-MemGPT) mantém um "core memory" (informações essenciais sobre o usuário, sempre no contexto), um "archival memory" (base persistida fora do contexto, recuperada via função) e um "recall memory" (histórico de conversas). O agente pode mover informação entre tiers — promoção e evicção explícitas. A metáfora SO/memória virtual é literal: há paginação de conteúdo entre memória "quente" e "fria" exatamente como um OS faz com RAM e swap.

**⑤ Policy-learned management** na prática. Research ativa: o sistema observa quais memórias foram úteis nas queries subsequentes (sinal de relevância), quais não foram (sinal de noise), e aprende uma política de quando persistir, quando consolidar, quando esquecer. O obstáculo para produção é o reward signal — definir o que é "útil" de forma estável é não-trivial, e instabilidades no RL se propagam para a qualidade da memória.

## O write-manage-read loop em ciclo contínuo

O loop não é linear — é iterativo. A cada ciclo, o sistema aprende com o que foi recuperado e usa esse aprendizado para refinar o que mantém.

```mermaid
graph LR
    W["WRITE<br/>Ingestão"] -->|"filtra e estrutura"| M["MANAGE<br/>Manutenção"]
    M -->|"compacta, deduplica, esquece"| ST[("Storage<br/>Indexado")]
    ST -->|"recupera top-k"| R["READ<br/>Retrieval"]
    R -->|"alimenta resposta"| AG["Agente<br/>(responde)"]
    AG -->|"nova interação gera nova entrada"| W
    AG -->|"feedback implícito: foi útil?"| M
```

O ciclo revela uma propriedade importante: **manage não é pós-processamento periódico, é integrante do loop**. Todo ciclo de ingestão deveria disparar verificação de duplicatas; todo ciclo de recuperação deveria alimentar algum sinal de relevância que a manutenção usa. Implementações que tratam manage como "tarefa do fim de semana" deixam o loop incompleto — e a degradação acumula entre as execuções manuais de limpeza.

Na prática, a frequência de cada operação difere:

| Operação | Frequência recomendada | Custo por execução |
|---|---|---|
| Ingestão | A cada interação | Baixo (extract + write) |
| Deduplicação | A cada ingestão ou diária | Médio (comparação vetorial) |
| Compactação | Semanal ou por trigger de tamanho | Alto (LLM summarize) |
| Lint (links, schema) | Diário via CI | Baixo (parse de arquivos) |
| Forget policy (evicção) | Mensal ou por TTL | Baixo (filter por data/score) |
| Reflexão (self-improvement) | Semanal ou por threshold de volume | Alto (LLM reflection) |

A coluna de custo explica por que a maior parte dos sistemas skipa compactação e reflexão: são as operações mais caras e os benefícios aparecem no longo prazo, não na demo. É exatamente aí que sistemas amadurecem ou apodrecem.

## Quando NÃO usar uma arquitetura completa

Não há virtude em sobre-engenharia. Há cenários onde implementar todos os cinco componentes é desperdício:

- **Protótipos.** Começar com só ingestão append-only e retrieval simples (busca por substring ou top-1 vector). Validar valor antes de investir em manutenção e schema.
- **Casos one-shot.** Tarefas que terminam numa sessão não têm acumulação para arquitetar. Memória aqui é histórico de conversa, e o context window resolve.
- **Equipes que não sustentarão a manutenção.** Manage sem disciplina vira lixo acelerado — o sistema decai mais rápido do que se não tivesse manutenção alguma, porque as expectativas são maiores. Melhor não prometer manutenção do que prometer e abandonar.
- **Quando RAG basta.** Recuperação sobre corpus estático, sem composição entre fontes, sem evolução temporal. Ver [[04 - RAG vs memória de longo prazo]] e [[05 - Beyond RAG - quando RAG não basta]] para o critério de quando RAG é suficiente e quando não é.

> [!warning] Manutenção sem evaluation é teatro
> O componente de manutenção é especialmente vulnerável a virar atividade performática. Compactação que não preserva fatos críticos, lint que não detecta contradições reais, forget policy que evicta o que importava — sem métricas que validem cada operação, manutenção piora o sistema em vez de melhorar. Antes de implementar manage, definir como medir se está funcionando.

## Exercício de mapeamento: diagnosticar um sistema existente

A utilidade prática do mapa de cinco componentes é que ele permite diagnosticar qualquer sistema — próprio ou de terceiro — com um checklist rápido. Para um sistema em avaliação, pergunte:

> [!example] Checklist de arquitetura
> - **Ingestão:** O que filtra o que entra? É manual, automático ou híbrido? A granularidade é fato atômico, parágrafo ou documento?
> - **Indexação:** Qual o substrato? Vetorial, grafo, hierárquico, flat? Write-heavy ou read-heavy por design?
> - **Retrieval:** Similarity search pura, graph traversal, híbrida (BM25 + vetor)? Tem reranking? Qual o top-k padrão?
> - **Manutenção:** Existe compactação? Com que frequência? Há forget policy? Quem roda o lint?
> - **Governance:** Existe CLAUDE.md, AGENTS.md ou documento de regras? O schema de frontmatter é validado?

Sistemas que respondem "não existe" para manutenção e governance estão, quase sem exceção, no caminho de se tornarem lixão. Não por mal design — por omissão que parece razoável no começo e compõe negativamente com o tempo.

## Armadilhas comuns

> [!warning] Armadilha 1: Focar só no retrieval ignorando a manutenção
> Retrieval é mensurável, tem benchmark, tem número que sobe em demo. Manutenção é invisível, tediosa e os erros aparecem meses depois. O resultado previsível: esforço desproporcional em retrieval, esqueleto de manutenção que ninguém alimenta, sistema bonito por seis meses e lixão depois. A regra assimétrica: retrieval ruim dá respostas erradas imediatamente — é detectável. Manutenção ruim dá respostas erradas lentamente, acumulando silenciosamente, até o sistema virar fonte de confusão em vez de conhecimento.

> [!warning] Armadilha 2: Schema implícito vira inconsistência crônica
> Sem regras escritas explicitamente, o LLM espalha conteúdo sem coerência. A primeira nota usa um padrão; a centésima usa outro; ninguém percebe até alguém tentar buscar por algo que existe em três formatos diferentes. O efeito é especialmente ruim em markdown, onde o schema é opcional por design. Escrever o schema antes de começar é barato; corrigir inconsistência em vault grande é trabalho de semanas. Um CLAUDE.md ou AGENTS.md com as regras básicas — naming, frontmatter, taxonomia — resolve o problema antes de ele surgir.

> [!warning] Armadilha 3: Confundir substrato com arquitetura
> Markdown vs vector DB é detalhe de substrato — o nível físico abaixo da arquitetura. O write-manage-read loop é o ponto arquitetural real. Debates que ficam no nível "qual storage" perdem substância: duas implementações com o mesmo substrato markdown podem ser arquiteturalmente opostas (uma com manage sofisticado, outra append-only), e duas com substrato diferente (uma markdown, uma vetorial) podem ser arquiteturalmente equivalentes no loop. Escolher substrato antes de mapear o loop é começar pela decisão menos importante.

> [!warning] Armadilha 4: Ingestão sem filtro degrada a relação sinal/ruído
> Gravar tudo parece mais seguro do que filtrar — afinal, melhor ter e não precisar do que precisar e não ter. Na prática, gravar tudo significa que a memória vira diário em vez de knowledge base. O retrieval devolve contexto irrelevante misturado com o que importa, e o agente perde capacidade de discriminar. Filtrar agressivamente na ingestão é menos custoso do que limpar depois — e manda sinal claro para o agente sobre o que merece persistência.

## Como explicar em inglês

> [!tip] Interview quote
> "Every agent memory system, regardless of implementation, shares the same five components: ingestion, indexing, retrieval, maintenance, and governance. The write-manage-read loop is the architectural pattern that connects them. Understanding this vocabulary lets you evaluate any new framework in under 20 minutes."

| Português | Inglês |
|-----------|--------|
| ingestão | ingestion |
| indexação | indexing |
| manutenção | maintenance |
| governança / esquema | governance / schema |
| compactação | compaction |
| deduplicação | deduplication |
| política de esquecimento | forget policy |
| loop escrever-gerenciar-ler | write-manage-read loop |
| memória hierárquica | hierarchical memory |
| busca híbrida | hybrid search |

## O que vem a seguir

Com o vocabulário arquitetural em mãos — os cinco componentes, os cinco mecanismos do survey e o framework de maturidade Storage/Reflection/Experience — a [[09 - Panorama de implementações (abril 2026)|nota 09]] aplica esse vocabulário ao mercado real. Ela mapeia uma dúzia de implementações em três famílias (inspiradas no LLM Wiki, frameworks de produção e acadêmicas), apresenta uma tabela síntese com hedges nos números e um fluxograma de escolha. O critério de comparação vem desta nota; o mapa do que existe vem da próxima.

## Veja também

- [[06 - O LLM Wiki Pattern (gist do Karpathy)]] — instância concreta do pattern, com Ingest/Query/Lint mapeados aos componentes
- [[07 - Por que Obsidian e markdown como substrato]] — substrato é decisão ortogonal à arquitetura
- [[20 - Surveys e estado da arte 2026]] — formalização acadêmica do write-manage-read loop e dos 5 mecanismos
- [[09 - Panorama de implementações (abril 2026)|09 - Panorama]] — quem implementa o quê, classificado pelos componentes desta nota
- [[21 - Comparativo crítico (LongMemEval)|21 - Comparativo crítico]] — comparação técnica usando este vocabulário
- [[23 - Guia de implementação do zero]] — aplicar a arquitetura num projeto novo, mapeando caso de uso aos componentes

## Referências

- Du et al. (2026). *A Survey on Memory in Large Language Model Agents*. [arxiv.org/abs/2603.07670](https://arxiv.org/abs/2603.07670). Formaliza o write-manage-read loop e classifica os 5 mecanismos arquiteturais.
- Karpathy, A. (2026). *LLM Wiki — gist*. [gist.github.com/karpathy/442a6bf555914893e9891c11519de94f](https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f). Operações Ingest / Query / Lint como mapeamento prático dos componentes.
- Park, J. S. et al. (2023). *Generative Agents: Interactive Simulacra of Human Behavior*. [arxiv.org/abs/2304.03442](https://arxiv.org/abs/2304.03442). Ciclo observation / reflection / planning, base do mecanismo reflective self-improvement.
- Framework "Storage / Reflection / Experience" — referenciado em literatura recente sobre maturidade de sistemas de memória; estágios evolutivos de preservação bruta a abstração reusável.
