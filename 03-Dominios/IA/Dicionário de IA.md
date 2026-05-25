---
title: "Dicionário de IA"
created: 2026-05-03
updated: 2026-05-24
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
>	
updated: 2026-05-13
## Agents and Agentic Systems

### Agent
Um programa que utiliza um LLM em um loop para realizar ações em direção a um objetivo: ele observa o estado, decide por uma chamada de ferramenta ou resposta, executa e envia o resultado de volta para o próximo passo. A propriedade definidora é a autonomia através de múltiplos turnos, não a inteligência bruta.

### agentic loop
O ciclo iterativo fundamental de um agente de IA, composto por etapas de percepção, planejamento, ação e observação. O agente processa uma entrada, decide por uma ação (frequentemente uma chamada de ferramenta), observa o resultado e repete o processo até que o objetivo final seja alcançado ou um critério de parada seja atingido.

- TODO: orchestrator-worker
- TODO: planning
- TODO: ReAct
- TODO: tool use
- TODO: subagent


## Coding Agents

### Coding agent
Um agente especializado em tarefas de engenharia de software — leitura, escrita e modificação de código, execução de comandos de shell, execução de testes e iteração até que um objetivo seja alcançado. Exemplos incluem Claude Code, Cursor, Aider e Continue.

### vibe coding
Gerar software descrevendo a intenção em linguagem natural a um LLM e aceitando o código produzido com pouca ou nenhuma revisão, guiando ajustes por prompts de follow-up até "funcionar". Termo cunhado por Andrej Karpathy em fevereiro de 2025; eficaz para protótipos e projetos descartáveis, mas acumula tech debt e risco de segurança em produção.

- TODO: Aider
- TODO: Claude Code
- TODO: Continue
- TODO: Cursor
- TODO: autonomous coding loop
- TODO: PR-driven workflow

## Context Engineering

### Chain-of-Thought (CoT)
Uma técnica de prompting que instrui o modelo a produzir etapas de raciocínio intermediárias antes de fornecer uma resposta final — tipicamente acionada por frases como "pense passo a passo". O CoT melhora a precisão em tarefas de múltiplas etapas, mas aumenta a contagem de tokens de saída, e em modelos de raciocínio estendido (extended-thinking), alimenta diretamente a geração de tokens de raciocínio.

### Comprehension gate
Um checkpoint em um fluxo agêntico onde o agente precisa demonstrar que compreendeu a tarefa, plano ou contexto antes de ter permissão para prosseguir — tipicamente reformulando os requisitos com as próprias palavras, listando edge cases ou respondendo a perguntas de verificação. Serve para flagrar mal-entendidos cedo, antes que o agente gaste tokens e turnos executando sobre uma premissa errada.

### Context window
O número máximo de tokens que um modelo pode considerar em uma única chamada de inferência, incluindo o system prompt, input do usuário, turnos anteriores, definições de ferramentas e a resposta sendo gerada. Exceder esse limite força o truncamento, sumarização ou compactação.

### system prompt
Um bloco de instruções enviado pelo desenvolvedor no início de cada chamada de API para configurar o comportamento, personalidade, limitações e contexto do modelo. Diferente das mensagens do usuário, o system prompt é tipicamente estático e re-enviado integralmente a cada turno — tornando-o um vetor de custo constante em sessões agenticas.

- TODO: context compaction
- TODO: few-shot prompting
- TODO: prompt engineering
- TODO: prompt template

## LLMs Anatomy

### KV cache
Uma técnica de otimização para inferência de Transformers que armazena os vetores Key (K) e Value (V) dos tokens anteriores na memória da GPU. Isso evita cálculos redundantes durante a geração autorregressiva, reduzindo a complexidade computacional de $O(N^2)$ para $O(N)$ por novo token, mas aumenta significativamente o uso de VRAM conforme o comprimento da sequência cresce.

### LLM (Large Language Model)
Uma rede neural — tipicamente um transformer apenas com decodificador (decoder-only) — treinada em grandes corpora de texto para prever o próximo token dada uma sequência. LLMs modernos escalam para bilhões ou trilhões de parâmetros e exibem capacidades emergentes como aprendizado em contexto e seguimento de instruções.

### memory bandwidth bottleneck
Um gargalo de desempenho onde a velocidade de transferência de dados entre a memória (HBM/VRAM) e the processador limita a execução mais do que o poder bruto de processamento. Na inferência de LLMs, a natureza sequencial da geração de tokens força o modelo a ler todos os seus parâmetros da memória para cada token produzido, tornando a fase de "decode" fortemente limitada pela largura de banda da memória.

### Speculative decoding
Uma otimização de inferência onde um modelo de rascunho (draft model) pequeno propõe sequências de tokens candidatas que um modelo alvo (target model) maior verifica em paralelo. Predições aceitas reduzem as etapas de decodificação efetivas, diminuindo a latência. O impacto no custo depende do provedor: a contagem de tokens faturados pode não diminuir mesmo que o tempo real de execução diminua.

- TODO: attention
- TODO: decoding strategy
- TODO: embedding
- TODO: fine-tuning
- TODO: inference
- TODO: parameters / weights
- TODO: sampling
- TODO: temperature
- TODO: top-k
- TODO: top-p
- TODO: transformer

## MCP — Model Context Protocol

### MCP (Model Context Protocol)
Um protocolo aberto que padroniza como aplicações de LLM expõem contexto, ferramentas e prompts para modelos através de uma arquitetura cliente-servidor. Ele desacopla os provedores de modelos das fontes de dados, permitindo que qualquer cliente compatível com MCP se conecte a qualquer servidor MCP.

- TODO: MCP client
- TODO: MCP server
- TODO: prompts (MCP)
- TODO: resources (MCP)
- TODO: tools (MCP)
- TODO: transport (stdio, SSE, HTTP)

## Memory

- TODO: episodic memory
- TODO: long-term memory
- TODO: recall
- TODO: semantic memory
- TODO: vector store
- TODO: working memory

## Monitoring and Observability

### Observability
A capacidade de inferir o estado interno de um sistema a partir de suas saídas externas — logs, métricas e traces. Em aplicações de LLM, observability vai além do monitoramento tradicional: exige rastrear qualidade das respostas (não-determinísticas), custos por chamada, cadeias de tool calls e o impacto de mudanças de prompt. As três dimensões clássicas são logs (registros de eventos), métricas (séries temporais agregadas) e traces (rastreamento de uma solicitação através do sistema).

- TODO: Arize Phoenix
- TODO: Langfuse
- TODO: OpenTelemetry GenAI
- TODO: span
- TODO: trace
- TODO: tracing

## RAG and Vector Databases

### RAG (Retrieval-Augmented Generation)
Uma técnica que fundamenta as respostas do LLM em documentos externos buscados no momento da consulta, reduzindo alucinações e permitindo atualizações de conhecimento sem necessidade de retreinamento. Um pipeline típico faz o embedding da consulta, recupera os top-K chunks relevantes de um vector store e os injeta no prompt.

- TODO: BM25
- TODO: chunking
- TODO: dense retrieval
- TODO: embedding model
- TODO: hybrid search
- TODO: reranking
- TODO: retrieval
- TODO: vector database

## Security and Guardrails

### Guardrail
Uma restrição aplicada à entrada ou saída do LLM para impor requisitos de segurança, política ou qualidade — por exemplo, bloqueando informações de identificação pessoal (PII), filtrando conteúdo prejudicial, validando esquemas de saída estruturada ou recusando solicitações fora do tópico. Guardrails podem ser aplicados no modelo (fine-tuning, system prompt) ou no pipeline (pré/pós processamento).

- TODO: content filtering
- TODO: jailbreak
- TODO: output validation
- TODO: prompt injection
- TODO: red teaming

## Sequence Models

### LSTM (Long Short-Term Memory)
Uma arquitetura de rede neural recorrente introduzida por Hochreiter & Schmidhuber (1997) que utiliza portas de entrada, esquecimento e saída para manter informações em sequências longas, mitigando o problema do gradiente evanescente de RNNs tradicionais. Dominou tarefas de modelagem de sequência como tradução e reconhecimento de fala antes de ser amplamente substituída pelo Transformer.

## Spec-Driven Development

### Spec-driven development
Um fluxo de trabalho onde uma especificação escrita (requisitos + design) precede a implementação, e a especificação — não apenas o código — é o artefato revisado e iterado. Com assistentes de IA, a especificação também se torna o input que impulsiona a geração de planos e a síntese de código.

- TODO: brainstorming (process)
- TODO: design doc
- TODO: implementation plan
- TODO: TDD with AI

## Token Economy

### Cache hit rate
A proporção de chamadas à API em que o prefixo do prompt foi encontrado no cache do provedor — evitando recomputação e sendo faturado com desconto significativo (~10% da taxa normal de entrada). Um cache hit rate baixo indica que o conteúdo estático não está posicionado corretamente no início do prompt, que o prefixo varia entre chamadas, ou que o TTL do cache expirou antes de ser reutilizado. Meta razoável para workloads com system prompt fixo: >60%.

### Completion tokens
O total de tokens gerados pelo modelo em uma única chamada de API, incluindo a resposta visível e os tokens de raciocínio (quando aplicável). Faturado à taxa de saída — tipicamente 3 a 10 vezes a taxa de entrada. Retornado como `completion_tokens` na interface de API compatível com OpenAI.

### Prompt caching
Uma otimização do provedor que armazena o estado do KV-cache de um prefixo de prompt para que solicitações subsequentes que compartilhem o mesmo prefixo pulem a recomputação e sejam faturadas com um desconto significativo (~10% da taxa de entrada padrão). Eficaz apenas para conteúdo estático — system prompts, schemas de ferramentas, documentos de referência — colocados no início do prompt.

### Reasoning tokens
Tokens gerados internamente por um modelo durante o raciocínio estendido — usados para chain-of-thought, autocorreção e planejamento — antes da produção da resposta final. Faturados às taxas de tokens de saída pela maioria dos provedores, embora nunca apareçam na resposta. A ausência de um `thinking_budget` pode fazer com que os tokens de raciocínio dominem o custo total de uma chamada.

### Thinking budget
Um parâmetro por solicitação que limita o número máximo de tokens de raciocínio que um modelo pode gerar antes de produzir sua resposta final. No Claude, configurado via `thinking.budget_tokens`; outras APIs expõem um seletor de `/effort`. Sem um orçamento, modelos de raciocínio estendido podem consumir dezenas de milhares de tokens de raciocínio em tarefas triviais.

### Token
A unidade atômica que um modelo de linguagem lê e emite — tipicamente um fragmento de sub-palavra produzido por um tokenizer. Preços, limites de contexto e latência são todos medidos em tokens, portanto, entender a tokenização é fundamental para a otimização de custo e desempenho.

- TODO: batch API
- TODO: cost per token
- TODO: prompt tokens

## Tooling

### tool call
A ação de um modelo de linguagem ao invocar uma ferramenta externa durante uma geração. O modelo produz um bloco estruturado com o nome da ferramenta e seus argumentos; o framework executa a ferramenta e devolve o resultado como input do próximo turno. Erros de sintaxe em tool calls disparam retries automáticos — cada um custando um turno completo de tokens acumulados.

### tool definition
A especificação estruturada (tipicamente JSON Schema) que descreve para o modelo o nome, descrição e parâmetros aceitos de uma ferramenta disponível. Tool definitions são enviadas no system prompt a cada turno, tornando-se um custo fixo por chamada independentemente de quantas ferramentas são realmente usadas.

- TODO: function calling
- TODO: SDK
- TODO: structured output
