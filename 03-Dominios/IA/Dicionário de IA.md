---
title: "Dicionário de IA"
created: 2026-05-03
updated: 2026-05-26
type: glossary
status: seedling
aliases:
  - AI Glossary
  - Glossário de IA
tags:
  - glossary
  - ia
lang: pt
publish: true
---

# Dicionário de IA

> Glossário de trabalho para o domínio de IA — LLMs, agentes, RAG, MCP, engenharia de contexto e ecossistema. Definições em português, mantendo termos técnicos em inglês quando consolidados.


>[!info]- Como usar:
>- Cada verbete é um `###` dentro de uma `##` temática.
>- Linkar: [[Dicionário de IA#RAG (Retrieval-Augmented Generation)]]
>- Adicionar termos: use a skill /verbete (auto-pesquisa se faltar definição).
>- Os bullets `- TODO:` em cada seção são candidatos a verbetes; 
>	- promova conforme estudar.

## Agents and Agentic Systems

### Agent
Um programa que utiliza um LLM em um loop para realizar ações em direção a um objetivo: ele observa o estado, decide por uma chamada de ferramenta ou resposta, executa e envia o resultado de volta para o próximo passo. A propriedade definidora é a autonomia através de múltiplos turnos, não a inteligência bruta.

### agentic loop
O ciclo iterativo fundamental de um agente de IA, composto por etapas de percepção, planejamento, ação e observação. O agente processa uma entrada, decide por uma ação (frequentemente uma chamada de ferramenta), observa o resultado e repete o processo até que o objetivo final seja alcançado ou um critério de parada seja atingido.

### orchestrator-worker
Um padrão de arquitetura agêntica onde um agente orquestrador decompõe uma tarefa complexa e delega subtarefas a múltiplos agentes trabalhadores (workers) especializados, depois agrega os resultados. Permite paralelismo e separação de responsabilidades, ao custo de overhead de coordenação e de mais tokens consumidos por cada worker.

### planning
A etapa em que um agente decompõe um objetivo de alto nível em uma sequência de passos ou subtarefas antes de agir. Pode ser explícita (gerar um plano em texto que guia as ações seguintes) ou implícita no agentic loop; melhora tarefas longas e de múltiplas etapas ao reduzir desvios e retrabalho.

### ReAct
Um padrão de prompting (Reason + Act) que intercala passos de raciocínio em linguagem natural com chamadas de ferramenta: o modelo verbaliza um pensamento, escolhe uma ação, observa o resultado e repete. Foi um dos primeiros frameworks a estruturar o agentic loop e ainda embasa muitos agentes modernos.

### subagent
Um agente secundário invocado por um agente principal para executar uma subtarefa isolada, frequentemente com seu próprio contexto, prompt e ferramentas. Permite paralelizar trabalho e isolar contexto — o subagente devolve só a conclusão, não todo o histórico —, reduzindo a poluição do context window do agente principal.

### tool use
A capacidade de um LLM de invocar funções externas — buscar na web, executar código, consultar um banco — em vez de apenas gerar texto. O modelo emite uma chamada estruturada (nome + argumentos), o framework executa e devolve o resultado ao contexto; é o que transforma um LLM em um agente capaz de agir sobre o mundo.

## Coding Agents

### Aider
Um coding agent open-source de linha de comando que edita código diretamente no repositório local e cria commits Git automaticamente a cada mudança. Funciona com múltiplos modelos (Claude, GPT, modelos locais) e usa um mapa do repositório para dar contexto ao LLM.

### autonomous coding loop
Um modo de operação em que um coding agent executa o ciclo completo — escrever código, rodar testes, ler erros e corrigir — repetidamente e sem intervenção humana a cada passo, até a tarefa passar nos critérios ou atingir um limite. Maximiza autonomia, mas exige guardrails e verificação para evitar desvios silenciosos.

### Claude Code
O coding agent oficial da Anthropic, operando como CLI no terminal (e também via app desktop, web e extensões de IDE). Lê e edita arquivos, executa comandos de shell, roda testes e itera de forma agêntica; é extensível via skills, hooks, subagentes e servidores MCP.

### Coding agent
Um agente especializado em tarefas de engenharia de software — leitura, escrita e modificação de código, execução de comandos de shell, execução de testes e iteração até que um objetivo seja alcançado. Exemplos incluem Claude Code, Cursor, Aider e Continue.

### Continue
Uma extensão open-source de IDE (VS Code, JetBrains) que adiciona autocomplete, chat e edição assistida por IA, configurável com múltiplos modelos e provedores. Foca em ser um assistente integrado ao editor, mais do que um agente autônomo de terminal.

### Cursor
Um editor de código (fork do VS Code) construído em torno de IA, oferecendo autocomplete preditivo, chat com contexto do codebase e um modo agente que edita múltiplos arquivos. É um dos AI-first editors mais populares.

### PR-driven workflow
Um fluxo em que o coding agent entrega seu trabalho como um pull request — com diff, descrição e testes — para revisão humana antes do merge, em vez de commitar direto na branch principal. Reaproveita a infraestrutura de code review existente como ponto de controle de qualidade e comprehension gate.

### vibe coding
Gerar software descrevendo a intenção em linguagem natural a um LLM e aceitando o código produzido com pouca ou nenhuma revisão, guiando ajustes por prompts de follow-up até "funcionar". Termo cunhado por [[Andrej Karpathy]] em fevereiro de 2025; eficaz para protótipos e projetos descartáveis, mas acumula tech debt e risco de segurança em produção.

## Context Engineering

### Chain-of-Thought (CoT)
Uma técnica de prompting que instrui o modelo a produzir etapas de raciocínio intermediárias antes de fornecer uma resposta final — tipicamente acionada por frases como "pense passo a passo". O CoT melhora a precisão em tarefas de múltiplas etapas, mas aumenta a contagem de tokens de saída, e em modelos de raciocínio estendido (extended-thinking), alimenta diretamente a geração de tokens de raciocínio.

### Comprehension gate
Um checkpoint em um fluxo agêntico onde o agente precisa demonstrar que compreendeu a tarefa, plano ou contexto antes de ter permissão para prosseguir — tipicamente reformulando os requisitos com as próprias palavras, listando edge cases ou respondendo a perguntas de verificação. Serve para flagrar mal-entendidos cedo, antes que o agente gaste tokens e turnos executando sobre uma premissa errada.

### context compaction
A técnica de reduzir o tamanho do contexto ativo de uma sessão agêntica ao resumir ou descartar turnos antigos quando o context window se aproxima do limite, preservando o essencial para continuar a tarefa. Permite sessões longas sem estourar o limite, mas arrisca perder detalhes que pareciam irrelevantes no momento da compactação.

### Context window
O número máximo de tokens que um modelo pode considerar em uma única chamada de inferência, incluindo o system prompt, input do usuário, turnos anteriores, definições de ferramentas e a resposta sendo gerada. Exceder esse limite força o truncamento, sumarização ou compactação.

### few-shot prompting
Uma técnica que inclui no prompt alguns exemplos resolvidos da tarefa (input → output) antes da consulta real, para que o modelo infira o padrão desejado via in-context learning. Contrasta com zero-shot (nenhum exemplo); melhora consistência e formato ao custo de mais tokens de entrada.

### prompt engineering
A prática de projetar e refinar prompts — instruções, exemplos, estrutura e formato — para obter saídas mais precisas e confiáveis de um LLM sem alterar seus pesos. Inclui técnicas como Chain-of-Thought e few-shot e delimitação clara de papéis; é a camada de controle mais barata e imediata sobre o comportamento do modelo.

### prompt template
Um prompt parametrizado com placeholders preenchidos em tempo de execução com dados variáveis (input do usuário, documentos recuperados, exemplos), separando a estrutura fixa do conteúdo dinâmico. Favorece reuso, versionamento e cache hit rate ao manter o prefixo estável entre chamadas.

### system prompt
Um bloco de instruções enviado pelo desenvolvedor no início de cada chamada de API para configurar o comportamento, personalidade, limitações e contexto do modelo. Diferente das mensagens do usuário, o system prompt é tipicamente estático e re-enviado integralmente a cada turno — tornando-o um vetor de custo constante em sessões agenticas.

## Human Factors and AI Risks

### Débito cognitivo
A erosão, ao longo do tempo, do entendimento compartilhado de uma equipe sobre o que um sistema faz, por que as decisões foram tomadas e como mudá-lo. Diferente do débito técnico (que vive no código) e da carga cognitiva (momentânea), é uma propriedade de nível de projeto: o código pode estar limpo e os testes passando enquanto a [[O programa como teoria|teoria do sistema]] se perde da mente das pessoas. Acelerado pela geração de código via IA, que produz estrutura mais rápido do que o entendimento consegue estabilizar. Termo desenvolvido por Margaret-Anne Storey (2026), apoiado em Peter Naur. Ver [[Débito cognitivo]].

- TODO: débito de compreensão (comprehension debt)
- TODO: rendição cognitiva (cognitive surrender)
- TODO: deskilling
- TODO: psicose da IA (AI psychosis)
- TODO: tokenmaxxing

## LLMs Anatomy

### attention
O mecanismo central do transformer que, para cada token, pondera a relevância de todos os outros tokens da sequência e agrega suas representações conforme esses pesos. É o que permite ao modelo capturar dependências de longo alcance; sua variante multi-cabeça (multi-head) aprende vários tipos de relação em paralelo, e seu custo $O(N^2)$ no comprimento da sequência motiva otimizações como o KV cache.

### decoding strategy
O algoritmo que escolhe o próximo token a partir da distribuição de probabilidades produzida pelo modelo a cada passo — greedy (sempre o mais provável), beam search, ou amostragem estocástica controlada por temperature, top-k e top-p. Determina o equilíbrio entre determinismo/precisão e diversidade/criatividade da saída.

### embedding
A representação de um token como um vetor denso de números reais em um espaço de alta dimensão, onde a proximidade geométrica captura similaridade semântica. É a primeira transformação após a tokenização — cada token vira um vetor que as camadas Transformer manipulam. O mesmo mecanismo embasa RAG e busca semântica, onde textos são comparados pela distância entre seus vetores.

### fine-tuning
O processo de continuar o treino de um modelo pré-treinado em um conjunto de dados menor e específico para especializá-lo numa tarefa ou domínio, ajustando seus pesos. Contrasta com prompting (que não altera pesos); variantes eficientes como LoRA treinam apenas uma fração dos parâmetros para reduzir custo de memória e armazenamento.

### flagship model
O modelo mais capaz e topo de linha do catálogo de um provedor, posicionado acima de variantes menores e mais baratas da mesma família (ex.: na linha Claude, Opus é o flagship; Sonnet e Haiku ficam abaixo). Marca o estado da arte do provedor em raciocínio e capacidades gerais, ao custo de maior latência e preço por token — os modelos menores costumam ser destilações ou versões reduzidas voltadas a velocidade e economia.

### foundation model
Um modelo de grande escala treinado de forma auto-supervisionada em vastos volumes de dados não rotulados, projetado como base genérica e adaptável a muitas tarefas via fine-tuning ou prompting — em vez de treinado para uma única função. O termo, cunhado por Stanford em 2021, engloba LLMs (GPT, Claude), mas também modelos de visão e multimodais; a ideia central é a transferência: treina-se uma vez em escala e reaproveita-se em incontáveis aplicações downstream.

### Hallucination
A geração, por um LLM, de conteúdo plausível mas factualmente incorreto ou inventado — referências inexistentes, APIs e funções que não existem, fatos falsos apresentados com confiança. Não é um defeito pontual e sim uma consequência direta do objetivo de treino (prever o próximo token mais provável, não verificar a verdade); por isso não se elimina, apenas se mitiga — via RAG, verificação externa, guardrails e revisão humana. Em geração de código, manifesta-se sobretudo como chamadas a bibliotecas inexistentes e edge cases silenciosamente ignorados.

### inference
O processo de usar um modelo já treinado para gerar saídas a partir de uma entrada; em LLMs, a geração autorregressiva de tokens, um de cada vez. Contrasta com o treinamento: na inferência os pesos são fixos. É a fase que domina o custo operacional em produção e tende a ser limitada pela largura de banda de memória, não pelo poder bruto de cálculo.

### KV cache
Uma técnica de otimização para inferência de Transformers que armazena os vetores Key (K) e Value (V) dos tokens anteriores na memória da GPU. Isso evita cálculos redundantes durante a geração autorregressiva, reduzindo a complexidade computacional de $O(N^2)$ para $O(N)$ por novo token, mas aumenta significativamente o uso de VRAM conforme o comprimento da sequência cresce.

### LLM (Large Language Model)
Uma rede neural — tipicamente um transformer apenas com decodificador (decoder-only) — treinada em grandes corpora de texto para prever o próximo token dada uma sequência. LLMs modernos escalam para bilhões ou trilhões de parâmetros e exibem capacidades emergentes como aprendizado em contexto e seguimento de instruções.

### memory bandwidth bottleneck
Um gargalo de desempenho onde a velocidade de transferência de dados entre a memória (HBM/VRAM) e o processador limita a execução mais do que o poder bruto de processamento. Na inferência de LLMs, a natureza sequencial da geração de tokens força o modelo a ler todos os seus parâmetros da memória para cada token produzido, tornando a fase de "decode" fortemente limitada pela largura de banda da memória.

### parameters / weights
Os valores numéricos aprendidos durante o treino que definem o comportamento de uma rede neural — as conexões entre neurônios ajustadas para minimizar o erro. A contagem de parâmetros (bilhões a trilhões em LLMs) é uma medida grosseira de capacidade; na inferência eles ficam fixos e precisam ser lidos da memória a cada token, o que liga o tamanho do modelo ao memory bandwidth bottleneck.

### sampling
A escolha estocástica do próximo token a partir da distribuição de probabilidades do modelo, em vez de pegar sempre o mais provável. Parâmetros como temperature, top-k e top-p moldam quão aleatória ou conservadora é a seleção, controlando o trade-off entre diversidade e coerência da saída.

### Speculative decoding
Uma otimização de inferência onde um modelo de rascunho (draft model) pequeno propõe sequências de tokens candidatas que um modelo alvo (target model) maior verifica em paralelo. Predições aceitas reduzem as etapas de decodificação efetivas, diminuindo a latência. O impacto no custo depende do provedor: a contagem de tokens faturados pode não diminuir mesmo que o tempo real de execução diminua.

### temperature
Um parâmetro de amostragem que escala a distribuição de probabilidades antes da seleção do token: valores baixos (→0) tornam a saída mais determinística e focada no token mais provável; valores altos (>1) achatam a distribuição e aumentam a aleatoriedade e a criatividade — ao custo de mais erros e incoerência.

### top-k
Uma estratégia de amostragem que restringe a escolha do próximo token aos `k` candidatos mais prováveis, zerando o resto da distribuição antes de amostrar. Limita saídas absurdas ao cortar a cauda longa, mas usa um corte fixo independentemente de quão concentrada ou dispersa está a distribuição.

### top-p
Também chamada nucleus sampling, restringe a escolha do próximo token ao menor conjunto de candidatos cuja probabilidade acumulada atinge o limiar `p`. Ao contrário do top-k, o tamanho do conjunto se adapta à forma da distribuição — estreito quando o modelo está confiante, amplo quando está incerto.

### transformer
A arquitetura de rede neural introduzida em *Attention Is All You Need* (Vaswani et al., 2017) que substituiu as redes recorrentes ao processar todos os tokens de uma sequência em paralelo via o mecanismo de self-attention. É a base de praticamente todos os LLMs modernos, tipicamente na variante decoder-only. Empilha dezenas a centenas de camadas idênticas, cada uma combinando atenção multi-cabeça e redes feed-forward.

## MCP — Model Context Protocol

### MCP (Model Context Protocol)
Um protocolo aberto que padroniza como aplicações de LLM expõem contexto, ferramentas e prompts para modelos através de uma arquitetura cliente-servidor. Ele desacopla os provedores de modelos das fontes de dados, permitindo que qualquer cliente compatível com MCP se conecte a qualquer servidor MCP.

### MCP client
O componente, embutido na aplicação host (ex.: um coding agent), que abre e mantém a conexão com um servidor MCP, descobre os recursos, ferramentas e prompts que ele expõe e os repassa ao modelo. Cada cliente fala com um servidor; é a metade do protocolo que consome capacidades.

### MCP server
Um processo que expõe ferramentas, recursos e prompts a clientes MCP através do protocolo padronizado, desacoplando uma fonte de dados ou capacidade do modelo que a consome. Pode rodar localmente (via stdio) ou remotamente (via HTTP/SSE); qualquer cliente compatível pode usá-lo sem integração customizada.

### prompts (MCP)
Templates de prompt parametrizados que um servidor MCP expõe para serem invocados pelo usuário ou pela aplicação host — tipicamente como atalhos ou comandos reutilizáveis. São uma das três primitivas do MCP, ao lado de tools e resources.

### resources (MCP)
Dados de contexto somente-leitura que um servidor MCP disponibiliza ao modelo — arquivos, registros de banco, respostas de API — identificados por URI e carregados sob demanda. Diferem das tools por não executarem ações nem terem efeitos colaterais; são uma das três primitivas do MCP.

### tools (MCP)
Funções executáveis que um servidor MCP expõe para o modelo invocar — com efeitos colaterais como escrever um arquivo, chamar uma API ou rodar uma query. São descritas por JSON Schema e formam a primitiva mais ativa do MCP, ao lado de prompts e resources.

### transport (stdio, SSE, HTTP)
A camada que carrega as mensagens entre cliente e servidor MCP. `stdio` conecta processos locais via entrada/saída padrão; `HTTP` (com Server-Sent Events, SSE) conecta servidores remotos. O protocolo é o mesmo independentemente do transporte, que só muda como os bytes trafegam.

## Memory

### episodic memory
Memória de agentes que registra eventos e interações específicas com seu contexto temporal — o que aconteceu, quando, em qual sessão. Permite ao agente lembrar de episódios passados ("na última conversa você pediu X"), contrastando com a semantic memory, que guarda fatos atemporais.

### long-term memory
Informação que um agente persiste entre sessões — fora do context window — em um armazenamento externo (arquivos, banco, vector store) e recupera quando relevante. Contrasta com a working memory, limitada à janela atual; é o que dá continuidade e personalização ao agente ao longo do tempo.

### recall
O ato de recuperar de uma memória externa a informação relevante para o turno atual e injetá-la no context window. É a contraparte de leitura do armazenamento de memória; sua qualidade depende de como a informação foi indexada (ex.: embeddings em um vector store) e de quão bem a query casa com o que foi guardado.

### semantic memory
Memória de agentes que guarda fatos e conhecimento gerais e atemporais — preferências do usuário, definições, regras do domínio — sem amarrá-los a um evento específico. Contrasta com a episodic memory; é o tipo de memória frequentemente materializado como "fatos" recuperáveis por busca semântica.

### vector store
Um componente que armazena embeddings e recupera os vetores mais próximos de uma query por similaridade (ex.: cosseno), usando índices de busca aproximada (ANN). É a infraestrutura de recuperação por trás de RAG e da memória de longo prazo de agentes; muitas vezes usado como sinônimo de vector database.

### working memory
A informação imediatamente disponível ao agente no turno corrente — tudo que está no context window: prompt, turnos recentes, resultados de ferramentas. É volátil e limitada pelo tamanho da janela, contrastando com a long-term memory persistida externamente.

## Monitoring and Observability

### Arize Phoenix
Uma ferramenta open-source de observability para aplicações de LLM e agentes, voltada a tracing, avaliação e debugging de prompts e cadeias de tool calls. Construída sobre OpenTelemetry, visualiza traces e permite rodar evals sobre as execuções capturadas.

### Langfuse
Uma plataforma open-source de observability e analytics para aplicações de LLM, que captura traces, custos por chamada, latência e qualidade, além de oferecer gestão de prompts e avaliações. Integra-se aos principais SDKs e frameworks de agentes.

### Observability
A capacidade de inferir o estado interno de um sistema a partir de suas saídas externas — logs, métricas e traces. Em aplicações de LLM, observability vai além do monitoramento tradicional: exige rastrear qualidade das respostas (não-determinísticas), custos por chamada, cadeias de tool calls e o impacto de mudanças de prompt. As três dimensões clássicas são logs (registros de eventos), métricas (séries temporais agregadas) e traces (rastreamento de uma solicitação através do sistema).

### OpenTelemetry GenAI
Um conjunto de convenções semânticas do OpenTelemetry que padroniza como atributos de chamadas a LLMs — modelo, tokens, custo, prompts, tool calls — são registrados em spans e traces. Permite observability vendor-neutral, com qualquer backend compatível consumindo os dados.

### span
A unidade básica de um trace: representa uma única operação com início, fim, duração e atributos (ex.: uma chamada ao LLM ou a execução de uma ferramenta). Spans se aninham e se encadeiam para formar a árvore de um trace completo.

### trace
O registro completo do percurso de uma requisição através de um sistema, composto por spans encadeados que mostram cada etapa, sua duração e suas relações de causa. Em aplicações de LLM, um trace expõe a cadeia inteira: prompt, raciocínio, tool calls e resposta final.

### tracing
A prática de instrumentar um sistema para emitir traces e spans, tornando visível o caminho e o tempo de cada operação. Em pipelines de LLM e agentes, é a base para debugar cadeias de tool calls, atribuir custos e diagnosticar latência e falhas.

## RAG and Vector Databases

### BM25
Uma função clássica de ranqueamento por relevância baseada em frequência de termos (lexical/sparse), que pontua documentos pela ocorrência das palavras da query ajustada por raridade e comprimento. É forte em correspondência exata de termos e frequentemente combinada com busca densa em hybrid search.

### chunking
A divisão de um documento em pedaços menores (chunks) antes de gerar embeddings, equilibrando granularidade de recuperação e contexto preservado em cada pedaço. Chunks grandes demais diluem a relevância; pequenos demais perdem contexto — a estratégia de corte (por tamanho, sentença ou estrutura) afeta diretamente a qualidade do RAG.

### dense retrieval
Recuperação baseada em similaridade semântica entre embeddings densos da query e dos documentos, capturando significado mesmo sem sobreposição exata de palavras. Contrasta com a busca lexical (BM25/sparse); é o que um vector store executa.

### embedding model
Um modelo treinado especificamente para converter texto em embeddings — vetores densos cuja proximidade reflete similaridade semântica. É o componente que alimenta dense retrieval e vector stores; a escolha do modelo (dimensão, idioma, domínio) define a qualidade da recuperação.

### hybrid search
Uma estratégia de recuperação que combina busca lexical (ex.: BM25) e busca densa (embeddings), fundindo os dois rankings para aproveitar tanto correspondência exata de termos quanto similaridade semântica. Costuma superar cada método isolado, sobretudo com termos raros ou jargão.

### RAG (Retrieval-Augmented Generation)
Uma técnica que fundamenta as respostas do LLM em documentos externos buscados no momento da consulta, reduzindo alucinações e permitindo atualizações de conhecimento sem necessidade de retreinamento. Um pipeline típico faz o embedding da consulta, recupera os top-K chunks relevantes de um vector store e os injeta no prompt.

### reranking
Uma etapa de pontuação de segundo estágio que reordena um conjunto inicial de candidatos recuperados usando um modelo mais caro e preciso (tipicamente um cross-encoder), para melhorar a qualidade dos top-K passados ao LLM. Troca latência e custo por relevância.

### retrieval
A etapa de um pipeline RAG que, dada uma query, busca e devolve os trechos mais relevantes de uma base de conhecimento para injetá-los no prompt. Pode ser lexical, densa ou híbrida; sua qualidade determina o teto do que a geração consegue produzir — recuperação ruim, resposta ruim.

### vector database
Um banco de dados otimizado para armazenar embeddings e recuperar os vetores mais similares a uma query via busca aproximada de vizinhos (ANN), com índices como HNSW. É a infraestrutura por trás de dense retrieval em RAG e da memória de agentes; exemplos incluem Pinecone, Weaviate, Qdrant e pgvector.

## Security and Guardrails

### content filtering
A inspeção e bloqueio de entradas ou saídas que violem políticas — conteúdo tóxico, ilegal, sexual ou perigoso — por meio de classificadores, listas ou modelos dedicados. É um tipo de guardrail aplicado nas bordas do pipeline, antes de o input chegar ao modelo ou de o output chegar ao usuário.

### Guardrail
Uma restrição aplicada à entrada ou saída do LLM para impor requisitos de segurança, política ou qualidade — por exemplo, bloqueando informações de identificação pessoal (PII), filtrando conteúdo prejudicial, validando esquemas de saída estruturada ou recusando solicitações fora do tópico. Guardrails podem ser aplicados no modelo (fine-tuning, system prompt) ou no pipeline (pré/pós processamento).

### jailbreak
Uma técnica de prompt que contorna os guardrails e o alinhamento de um modelo para induzi-lo a produzir conteúdo proibido — via role-play, ofuscação, instruções contraditórias ou cenários hipotéticos. É uma forma específica de ataque que explora a tensão entre seguir instruções e respeitar restrições.

### output validation
A verificação programática da saída do modelo antes de usá-la — checagem de schema/JSON, tipos, faixas de valor, ausência de PII ou conformidade com regras de negócio. É um guardrail de pós-processamento que transforma a saída probabilística do LLM em algo confiável para sistemas downstream.

### prompt injection
Um ataque em que instruções maliciosas embutidas na entrada — ou em conteúdo externo que o modelo lê (uma página, um documento, um e-mail) — sequestram o comportamento do agente, sobrepondo-se às instruções legítimas. É o risco de segurança definidor de agentes com tool use, já que o modelo não distingue de forma confiável dados de comandos.

### red teaming
A prática de testar adversarialmente um sistema de IA — sondando-o com jailbreaks, prompt injections e casos extremos — para descobrir falhas de segurança e alinhamento antes que sejam exploradas em produção. Pode ser manual ou automatizada e alimenta o desenho de guardrails mais robustos.

## Sequence Models

### LSTM (Long Short-Term Memory)
Uma arquitetura de rede neural recorrente introduzida por Hochreiter & Schmidhuber (1997) que utiliza portas de entrada, esquecimento e saída para manter informações em sequências longas, mitigando o problema do gradiente evanescente de RNNs tradicionais. Dominou tarefas de modelagem de sequência como tradução e reconhecimento de fala antes de ser amplamente substituída pelo Transformer.

## Spec-Driven Development

### brainstorming (process)
Uma fase estruturada que precede a especificação, em que humano e IA exploram intenção, requisitos e alternativas de design antes de escrever qualquer plano ou código. Reduz retrabalho ao alinhar o entendimento cedo; no spec-driven development, é o passo que transforma uma ideia vaga em requisitos acionáveis.

### design doc
Um documento que descreve como um sistema ou feature será construído — arquitetura, componentes, trade-offs e alternativas consideradas — antes da implementação. No spec-driven development com IA, serve de input estruturado que o agente usa para gerar o plano e o código.

### implementation plan
Um artefato que decompõe uma especificação em uma sequência ordenada de passos executáveis, frequentemente com critérios de verificação por etapa. Em fluxos com IA, é o documento que guia a geração de código passo a passo e serve de checkpoint entre humano e agente.

### Spec-driven development
Um fluxo de trabalho onde uma especificação escrita (requisitos + design) precede a implementação, e a especificação — não apenas o código — é o artefato revisado e iterado. Com assistentes de IA, a especificação também se torna o input que impulsiona a geração de planos e a síntese de código.

### TDD with AI
A aplicação de test-driven development a fluxos assistidos por IA: escrever (ou fazer o agente escrever) os testes antes da implementação e então deixá-lo iterar até passarem. Os testes funcionam como especificação executável e guardrail, dando ao autonomous coding loop um critério objetivo de "pronto".

## Token Economy

### batch API
Uma modalidade de API para processar grandes volumes de requisições de forma assíncrona, sem garantia de baixa latência, em troca de um desconto significativo (tipicamente ~50%) sobre o preço normal. Ideal para cargas offline — avaliações, geração em massa, classificação — onde a resposta imediata não importa.

### Cache hit rate
A proporção de chamadas à API em que o prefixo do prompt foi encontrado no cache do provedor — evitando recomputação e sendo faturado com desconto significativo (~10% da taxa normal de entrada). Um cache hit rate baixo indica que o conteúdo estático não está posicionado corretamente no início do prompt, que o prefixo varia entre chamadas, ou que o TTL do cache expirou antes de ser reutilizado. Meta razoável para workloads com system prompt fixo: >60%.

### Completion tokens
O total de tokens gerados pelo modelo em uma única chamada de API, incluindo a resposta visível e os tokens de raciocínio (quando aplicável). Faturado à taxa de saída — tipicamente 3 a 10 vezes a taxa de entrada. Retornado como `completion_tokens` na interface de API compatível com OpenAI.

### cost per token
O preço unitário cobrado por token, cotado separadamente para entrada e saída (saída costuma custar 3 a 10× a entrada), com descontos para cache hits e batch. É a métrica base de custo de qualquer aplicação de LLM; multiplicada pelo volume de tokens, determina o custo operacional.

### Prompt caching
Uma otimização do provedor que armazena o estado do KV-cache de um prefixo de prompt para que solicitações subsequentes que compartilhem o mesmo prefixo pulem a recomputação e sejam faturadas com um desconto significativo (~10% da taxa de entrada padrão). Eficaz apenas para conteúdo estático — system prompts, schemas de ferramentas, documentos de referência — colocados no início do prompt.

### prompt tokens
O total de tokens enviados ao modelo numa chamada — system prompt, definições de ferramentas, histórico e input do usuário —, faturados à taxa de entrada (mais barata que a de saída). Retornado como `prompt_tokens` na interface compatível com OpenAI; são o alvo principal de otimizações como prompt caching.

### Reasoning tokens
Tokens gerados internamente por um modelo durante o raciocínio estendido — usados para chain-of-thought, autocorreção e planejamento — antes da produção da resposta final. Faturados às taxas de tokens de saída pela maioria dos provedores, embora nunca apareçam na resposta. A ausência de um `thinking_budget` pode fazer com que os tokens de raciocínio dominem o custo total de uma chamada.

### Thinking budget
Um parâmetro por solicitação que limita o número máximo de tokens de raciocínio que um modelo pode gerar antes de produzir sua resposta final. No Claude, configurado via `thinking.budget_tokens`; outras APIs expõem um seletor de `/effort`. Sem um orçamento, modelos de raciocínio estendido podem consumir dezenas de milhares de tokens de raciocínio em tarefas triviais.

### Token
A unidade atômica que um modelo de linguagem lê e emite — tipicamente um fragmento de sub-palavra produzido por um tokenizer. Preços, limites de contexto e latência são todos medidos em tokens, portanto, entender a tokenização é fundamental para a otimização de custo e desempenho.

## Tooling

### function calling
A capacidade de um LLM de produzir uma chamada estruturada (nome + argumentos em JSON) a uma função previamente declarada, em vez de texto livre, para que a aplicação a execute. É o mecanismo subjacente ao tool use; o termo enfatiza a interface estruturada exposta pelas APIs dos provedores.

### SDK
Um kit de desenvolvimento — biblioteca em uma linguagem específica (Python, TypeScript) — que abstrai as chamadas HTTP cruas à API de um provedor de LLM, oferecendo tipos, autenticação, streaming e tratamento de erros. Exemplos: o Anthropic SDK e o OpenAI SDK.

### structured output
Uma saída do modelo restrita a um formato verificável — tipicamente JSON conforme um schema declarado — em vez de texto livre, garantida por validação ou por decodificação restrita (constrained decoding). Torna a resposta do LLM consumível diretamente por código, sem parsing frágil.

### tool call
A ação de um modelo de linguagem ao invocar uma ferramenta externa durante uma geração. O modelo produz um bloco estruturado com o nome da ferramenta e seus argumentos; o framework executa a ferramenta e devolve o resultado como input do próximo turno. Erros de sintaxe em tool calls disparam retries automáticos — cada um custando um turno completo de tokens acumulados.

### tool definition
A especificação estruturada (tipicamente JSON Schema) que descreve para o modelo o nome, descrição e parâmetros aceitos de uma ferramenta disponível. Tool definitions são enviadas no system prompt a cada turno, tornando-se um custo fixo por chamada independentemente de quantas ferramentas são realmente usadas.
