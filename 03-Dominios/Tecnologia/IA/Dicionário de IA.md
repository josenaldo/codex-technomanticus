---
title: "Dicionário de IA"
created: 2026-05-03
updated: 2026-06-21
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

### agentic engineering
A disciplina emergente — nomeada e institucionalizada em 2026, com workshop próprio no ICSE (AGENT 2026) — que trata o design, a construção e a operação de sistemas com autonomia orientada a objetivos como engenharia estruturada, e não prompting ad hoc. Abrange requisitos, arquitetura, verificação/avaliação, AgentOps, safety e supervisão humana. Distingue-se do [[Dicionário de IA#vibe coding|vibe coding]] por apoiar-se em guardrails deliberados, arquivos de contexto, skills e enforcement por CI. Ver [[03-Dominios/Tecnologia/IA/Anatomia de Agents/11 - Harness engineering — a terceira camada|harness engineering]].

### agentic loop
O ciclo iterativo fundamental de um agente de IA, composto por etapas de percepção, planejamento, ação e observação. O agente processa uma entrada, decide por uma ação (frequentemente uma chamada de ferramenta), observa o resultado e repete o processo até que o objetivo final seja alcançado ou um critério de parada seja atingido.

### CAR (Control, Agency, Runtime)
Decomposição da camada de [[Dicionário de IA#harness|harness]] proposta em 2026 (preprint *Harness Engineering for Language Agents*) em três eixos: **Control** (quais instruções permanecem autoritativas), **Agency** (quais ações estão disponíveis) e **Runtime** (como o estado é carregado adiante e como falhas são tratadas ao longo do tempo). É uma de várias taxonomias concorrentes do harness — nenhuma virou consenso. *Preprint não peer-reviewed.* Ver [[03-Dominios/Tecnologia/IA/Anatomia de Agents/11 - Harness engineering — a terceira camada|harness engineering]].

### harness
A camada de runtime que envolve o LLM e transforma capacidade bruta em ação governada: memória externa, registries de ferramentas, protocolos, sandboxes, orquestração de [[Dicionário de IA#subagent|subagentes]] e pipelines de compressão. O modelo raciocina; o harness executa. Em 2026 foi nomeado como a "terceira camada" da capacidade de agentes (depois dos pesos e do contexto). Ver [[03-Dominios/Tecnologia/IA/Anatomia de Agents/11 - Harness engineering — a terceira camada|Harness engineering]].

### harness engineering
A engenharia deliberada do [[Dicionário de IA#harness|harness]] como disciplina estruturada — decidir conscientemente o loop de controle, o sandboxing, os gates de aprovação humana, a observabilidade, a política de permissões e o orçamento de contexto. Tese central de 2026: boa parte do ganho de performance atribuído a um "modelo novo" é, na verdade, do harness (ganhos *[[Dicionário de IA#HarnessCard|harness-sensitive]]*). Ver [[03-Dominios/Tecnologia/IA/Anatomia de Agents/11 - Harness engineering — a terceira camada|nota dedicada]].

### HarnessCard
Artefato leve de reporte proposto em 2026 (preprint CAR) para que benchmarks de agentes reportem não só o modelo, mas também a camada de [[Dicionário de IA#harness|harness]] que o cerca — análogo aos "model cards". Responde ao problema dos ganhos *harness-sensitive*: um leaderboard que troca modelo e harness ao mesmo tempo mede uma variável confundida. *Proposta de preprint não peer-reviewed.*

### loop engineering
O design deliberado do [[Dicionário de IA#agentic loop|loop de controle]] de um agente como artefato de engenharia — governança do loop, condições de parada, detecção de loop infinito, retry escalonado e pontos de aprovação humana —, em vez de apenas "usar ReAct". Termo consolidado em 2026; corresponde de perto à dimensão Runtime do [[Dicionário de IA#CAR (Control, Agency, Runtime)|CAR]].

### NLAH (Natural-Language Agent Harness)
Padrão emergente (2026) em que o comportamento do [[Dicionário de IA#harness|harness]] — fronteiras de papel, semântica de estado, tratamento de falha — é escrito em linguagem natural editável em texto puro, em vez de código hard-coded, baixando a barreira de adoção. Abordagem em pesquisa; não há evidência de que iguale código nativo em performance. *Preprint.*

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

### Audit trail (reasoning)
Em reasoning models (o3, R1, Gemini Thinking), padrão de output em que o modelo entrega resposta final + checkpoints de raciocínio + suposições + incertezas + caminho de verificação, em vez de chain-of-thought verboso. Substitui o anti-padrão "think step by step", que virou ruído em modelos de raciocínio nativo. Ver [[Prompt Engineering/08 - Reasoning models — audit trail, não chain-of-thought]].

### Chain-of-Thought (CoT)
Uma técnica de prompting que instrui o modelo a produzir etapas de raciocínio intermediárias antes de fornecer uma resposta final — tipicamente acionada por frases como "pense passo a passo". O CoT melhora a precisão em tarefas de múltiplas etapas, mas aumenta a contagem de tokens de saída, e em modelos de raciocínio estendido (extended-thinking), alimenta diretamente a geração de tokens de raciocínio.

### Comprehension gate
Um checkpoint em um fluxo agêntico onde o agente precisa demonstrar que compreendeu a tarefa, plano ou contexto antes de ter permissão para prosseguir — tipicamente reformulando os requisitos com as próprias palavras, listando edge cases ou respondendo a perguntas de verificação. Serve para flagrar mal-entendidos cedo, antes que o agente gaste tokens e turnos executando sobre uma premissa errada.

### context compaction
A técnica de reduzir o tamanho do contexto ativo de uma sessão agêntica ao resumir ou descartar turnos antigos quando o context window se aproxima do limite, preservando o essencial para continuar a tarefa. Permite sessões longas sem estourar o limite, mas arrisca perder detalhes que pareciam irrelevantes no momento da compactação.

### context rot
Degradação mensurável da qualidade da saída de um LLM conforme o contexto de entrada cresce, observável **muito antes** do limite nominal da janela. O termo foi cunhado pela Chroma Research (2025) após testar 18 modelos frontier: todos perdem acurácia com o aumento dos tokens, alguns já com poucas centenas. Para coding agents é o principal modo de falha — agentes acumulam ruído em busca, exploração e backtracking, e cada turno seguinte sofre.

### Context window
O número máximo de tokens que um modelo pode considerar em uma única chamada de inferência, incluindo o system prompt, input do usuário, turnos anteriores, definições de ferramentas e a resposta sendo gerada. Exceder esse limite força o truncamento, sumarização ou compactação.

### Deliverable-first prompting
Em geração de imagens, descrever o entregável (poster, infográfico, slide, mockup) carrega restrições implícitas — proporção, hierarquia visual, tipografia, layout — que descrever apenas a cena não carrega. Framing canônico do artigo "Become an AI Engineer" (@hooeem, capítulo #16). Ver [[Image Prompting/02 - Deliverable-first, não scene-first]].

### effective context length
O comprimento de contexto em que um LLM realmente mantém acurácia aceitável, distinto da janela **nominal** anunciada. Benchmarks como RULER (NVIDIA) e NoLiMa mostram que modelos com 128k-1M de spec sustentam, na prática, uma fração disso em tarefas multi-fato — por exemplo, Granite 3.1-8B com 128k nominal opera bem só até ~32k. Em 2026 virou métrica obrigatória para escolha de modelo em produção, já que "janela nominal" tornou-se número de marketing.

### few-shot prompting
Uma técnica que inclui no prompt alguns exemplos resolvidos da tarefa (input → output) antes da consulta real, para que o modelo infira o padrão desejado via in-context learning. Contrasta com zero-shot (nenhum exemplo); melhora consistência e formato ao custo de mais tokens de entrada.

### Multimodal prompting
Prompting que combina texto com imagens, PDFs, áudio, vídeo ou tabelas como input. Em 2026, modelos de fronteira (Claude 4.x, GPT-5, Gemini 2.x) são multimodais nativos; o gargalo é o engenheiro ainda dar apenas texto, desperdiçando capacidade do modelo. Ver [[Multimodal Prompting]].

### progressive disclosure
Mecanismo de carregamento em camadas que mantém o context window enxuto mesmo com muitas capacidades disponíveis. Nas Agent Skills: no startup, só o metadata (nome + descrição) de cada skill é pré-carregado (~30-100 tokens); o corpo do `SKILL.md` é lido sob demanda quando a skill fica relevante; arquivos de referência só carregam quando acessados (zero tokens de contexto até lá). É habilitado pelo modelo filesystem-based e é o que permite ter dezenas de skills sem inflar o contexto. Ver [[03-Dominios/Tecnologia/IA/Claude Code/Skills e MCP/01 - Anatomia de uma skill|Anatomia de uma skill]].

### prompt engineering
A prática de projetar e refinar prompts — instruções, exemplos, estrutura e formato — para obter saídas mais precisas e confiáveis de um LLM sem alterar seus pesos. Inclui técnicas como Chain-of-Thought e few-shot e delimitação clara de papéis; é a camada de controle mais barata e imediata sobre o comportamento do modelo.

### prompt template
Um prompt parametrizado com placeholders preenchidos em tempo de execução com dados variáveis (input do usuário, documentos recuperados, exemplos), separando a estrutura fixa do conteúdo dinâmico. Favorece reuso, versionamento e cache hit rate ao manter o prefixo estável entre chamadas.

### Prompt versioning
Tratar prompt como artefato versionado (não config string), com semver: major (breaking output format), minor (quality improvement), patch (typo). Cada trace registra qual versão produziu cada output, viabilizando rollback, A/B test e auditoria. Ver [[Observability/05 - Versionamento de prompts]] e [[Improvement Loop/03 - Prompt versioning — semver para prompts]].

### recency bias
A tendência de um LLM a dar mais peso à informação no fim do contexto (os tokens mais recentes) do que à que veio antes. Na prática de prompting e em agentes, instruções e dados colocados perto do final do prompt influenciam mais a saída — daí a recomendação de posicionar a tarefa atual e as restrições críticas no fim. É a contraparte "recente" do fenômeno [[Dicionário de IA#Lost in the Middle|Lost in the Middle]], que descreve a curva de atenção em U (pontas favorecidas, meio negligenciado).

### system prompt
Um bloco de instruções enviado pelo desenvolvedor no início de cada chamada de API para configurar o comportamento, personalidade, limitações e contexto do modelo. Diferente das mensagens do usuário, o system prompt é tipicamente estático e re-enviado integralmente a cada turno — tornando-o um vetor de custo constante em sessões agenticas.

### Sycophancy
Tendência de LLM em concordar com a premissa do usuário, elogiar a pergunta, ou recuar quando o usuário discorda sem novo argumento. Mitigada via prompts anti-sycophancy explícitos — o mega-prompt do [[Andrej Karpathy|Karpathy]] é o exemplo canônico, instruindo o modelo a desafiar premissas e oferecer contra-evidência. Ver [[Prompt Engineering/04 - O mega-prompt do Karpathy — anatomia da anti-sycophancy]].

### Tells de IA
Padrões linguísticos que denunciam output gerado por IA: "In today's fast-paced world", "It's important to note", "It's not X, it's Y" usado em excesso, em-dashes em flood, fechos motivacionais. Catalogados no artigo "Become an AI Engineer" (@hooeem, capítulo #8). Bloqueáveis via constraints declarativas no prompt. Ver [[Prompt Engineering/09 - Anti-patterns e tells de IA — o que evitar]].

## Evaluation and Improvement Loop

### A/B test de prompts
Comparação controlada de duas versões de prompt sob o mesmo input, medindo qualidade via eval automático, feedback do usuário ou métrica de produto. A variância alta em LLM exige amostras maiores (frequentemente N=200+ por braço), e abordagem bayesiana costuma ser mais apropriada que frequentista para decidir promoção. Ver [[Improvement Loop/02 - A-B testing de prompts]].

### Champion-challenger
Padrão de deploy em que o tráfego é dividido (ex.: 90/10) entre o prompt em produção (champion) e o candidato (challenger), com critérios objetivos de promoção: eval score, golden subset, custo e latência. Permite iteração contínua sem big-bang releases. Ver [[Improvement Loop/04 - Champion-challenger em produção]].

### DSPy
Framework de Stanford (Khattab et al., arXiv 2310.03714) que trata prompts como programas compiláveis. Define Signatures (input/output), Modules (chamadas LM) e Compilers (BootstrapFewShot, MIPROv2) que otimizam prompts contra eval functions, eliminando boa parte do prompt-tuning manual. Ver [[Improvement Loop/05 - Auto-prompt optimization — DSPy e além]].

### Eval-driven development (EDD)
Disciplina que coloca evals antes do prompt — análoga a TDD para código. O lema é "evals first, prompts second": sem dataset de avaliação e critério objetivo, "melhorar o prompt" vira opinião. Ver [[Evaluation/01 - Eval-driven development — a disciplina]].

### Eval gate
Threshold em CI/CD: queda em eval score acima de X% bloqueia merge de PR. Pode falhar silenciosamente (warn) ou ruidosamente (block); a calibração depende da maturidade do dataset e da tolerância a regressões. Ver [[Evaluation/07 - Eval em CI-CD]] e [[Improvement Loop/07 - Eval gates em CI — quando bloquear merge]].

### Golden dataset
Conjunto canônico de pares input-output usado como referência para avaliar prompts e modelos. Construído por representatividade, edge cases e anti-tests; versionado em paralelo com os prompts para que regressões sejam rastreáveis. Ver [[Evaluation/02 - Golden datasets — como construir]].

### LLM-as-judge
Uso de outro LLM (frequentemente um modelo capaz como GPT-4 ou Claude) para avaliar outputs em critérios subjetivos onde anotação humana não escala. Vieses canônicos: positional, verbosity, self-preference. Mitigações: chain-of-thought judging, pairwise comparison, swap-judge consistency. Ver [[Evaluation/04 - LLM-as-judge — quando e como]].

### Scoring rubric
Critério estruturado para pontuar outputs em avaliação: objetivos (formato, presença de campos) e subjetivos (acurácia, utilidade). Escalas 1–5 anchored (com exemplos por nível) ou binárias pass/fail; inter-rater agreement medido via Cohen's kappa. Ver [[Evaluation/03 - Scoring rubrics e critérios]].

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

### attention sink
Os primeiros tokens de uma sequência, que acumulam uma fração desproporcional da massa de [[Dicionário de IA#attention|atenção]] mesmo sem carregarem significado relevante. Funcionam como um "ralo" onde as cabeças de atenção despejam peso quando não têm nada específico para focar — uma consequência do softmax, que obriga os pesos a somarem 1 e precisa de algum lugar para escoar. Descobertos por Xiao et al. (2023) no trabalho de *StreamingLLM*; preservar esses tokens iniciais é essencial para manter a qualidade em janelas deslizantes, e o fenômeno explica o lado "início" da curva em U do [[Dicionário de IA#Lost in the Middle|Lost in the Middle]] e o complemento do [[Dicionário de IA#recency bias|recency bias]].

### backpropagation
O algoritmo que treina redes neurais calculando o gradiente da função de perda em relação a cada parâmetro, propagando o erro da camada de saída para as camadas de entrada via regra da cadeia. A cada iteração, os parâmetros são ajustados na direção oposta ao gradiente (gradiente descendente), minimizando progressivamente o erro. É o mecanismo central por trás do [[Dicionário de IA#pretraining|pretraining]] e do [[Dicionário de IA#fine-tuning|fine-tuning]] de LLMs — sem ele, os pesos da rede não seriam atualizáveis a partir dos dados.

### decoding strategy
O algoritmo que escolhe o próximo token a partir da distribuição de probabilidades produzida pelo modelo a cada passo — greedy (sempre o mais provável), beam search, ou amostragem estocástica controlada por temperature, top-k e top-p. Determina o equilíbrio entre determinismo/precisão e diversidade/criatividade da saída.

### Destilação (knowledge distillation)
Técnica de compressão em que um modelo "aluno" (student), menor, é treinado para reproduzir o comportamento de um modelo "professor" (teacher) maior — imitando não só o rótulo certo, mas a distribuição completa de probabilidades sobre o vocabulário (os *soft targets*), que carrega informação fina sobre como o professor "pensa". Produz uma rede genuinamente menor e mais barata de servir, ao custo de herdar vieses e limitações do professor; é parte do que viabiliza as variantes leves das famílias comerciais (Haiku, Flash, Nano). Distingue-se da [[Dicionário de IA#Quantização|quantização]], que reduz a precisão dos pesos sem mudar a arquitetura. Ver [[Anatomia dos LLMs/18 - Compressão de modelos — quantização e destilação]].

### embedding
A representação de um token como um vetor denso de números reais em um espaço de alta dimensão, onde a proximidade geométrica captura similaridade semântica. É a primeira transformação após a tokenização — cada token vira um vetor que as camadas Transformer manipulam. O mesmo mecanismo embasa RAG e busca semântica, onde textos são comparados pela distância entre seus vetores.

### Extended thinking
Feature de modelos Claude 4 (Anthropic) que aloca um orçamento de tokens dedicado a raciocínio interno antes de produzir a resposta final. Configurado via parâmetro `thinking` na API com `budget_tokens`; o conteúdo do raciocínio fica em blocos `thinking` separados dos blocos de resposta. Análogo conceitual ao reasoning interno de o3/R1, mas com controle de orçamento explícito. Usado pra problemas que se beneficiam de deliberação mais longa sem o custo de sempre rodar reasoning. Ver [[Anatomia dos LLMs/13 - Reasoning models e chain-of-thought]] e [[Prompt Engineering/08 - Reasoning models — audit trail, não chain-of-thought]].

### fine-tuning
O processo de continuar o treino de um modelo pré-treinado em um conjunto de dados menor e específico para especializá-lo numa tarefa ou domínio, ajustando seus pesos. Contrasta com prompting (que não altera pesos); variantes eficientes como LoRA treinam apenas uma fração dos parâmetros para reduzir custo de memória e armazenamento.

### flagship model
O modelo mais capaz e topo de linha do catálogo de um provedor, posicionado acima de variantes menores e mais baratas da mesma família (ex.: na linha Claude, Opus é o flagship; Sonnet e Haiku ficam abaixo). Marca o estado da arte do provedor em raciocínio e capacidades gerais, ao custo de maior latência e preço por token — os modelos menores costumam ser destilações ou versões reduzidas voltadas a velocidade e economia.

### FlashAttention
Família de kernels de atenção exata (Dao et al., 2022) que reorganiza a computação em blocos para minimizar o I/O entre a HBM e a SRAM da GPU — matematicamente equivalente à [[Dicionário de IA#attention|atenção]] padrão, sem perda de qualidade. Cada geração persegue o hardware do momento: a v4 (Hot Chips 2025) introduz um online softmax que pula ~90% do rescaling e chega a 22% mais rápida que o kernel cuDNN em GPUs Blackwell. É a otimização que viabilizou janelas de contexto longas na prática.

### foundation model
Um modelo de grande escala treinado de forma auto-supervisionada em vastos volumes de dados não rotulados, projetado como base genérica e adaptável a muitas tarefas via fine-tuning ou prompting — em vez de treinado para uma única função. O termo, cunhado por Stanford em 2021, engloba LLMs (GPT, Claude), mas também modelos de visão e multimodais; a ideia central é a transferência: treina-se uma vez em escala e reaproveita-se em incontáveis aplicações downstream.

### GPT (Generative Pre-trained Transformer)
Família de LLMs da OpenAI baseados na arquitetura Transformer decoder-only e treinados de forma auto-supervisionada em grandes corpora de texto para prever o próximo token. Cada versão (GPT-2, GPT-3, GPT-4…) escalou parâmetros e dados, revelando capacidades emergentes como raciocínio e seguimento de instruções. O nome é frequentemente usado de forma genérica para qualquer LLM de grande escala baseado em Transformer, embora tecnicamente se refira à linha da OpenAI.

### GQA (Grouped-Query Attention)
Esquema de atenção em que grupos de query heads compartilham um mesmo par de vetores K/V, reduzindo o tamanho do [[Dicionário de IA#KV cache|KV cache]] em até ~8× (≈90% vs multi-head attention) com perda de qualidade quase nula. Fica entre a multi-head attention (um K/V por head) e a multi-query attention (MQA, um único K/V para todas as heads); variantes mais agressivas como a MLA (Multi-Head Latent Attention, da DeepSeek) comprimem K/V numa representação latente de baixo rank. É uma das otimizações arquiteturais que tornam janelas de contexto de 1M+ economicamente viáveis.

### Hallucination
A geração, por um LLM, de conteúdo plausível mas factualmente incorreto ou inventado — referências inexistentes, APIs e funções que não existem, fatos falsos apresentados com confiança. Não é um defeito pontual e sim uma consequência direta do objetivo de treino (prever o próximo token mais provável, não verificar a verdade); por isso não se elimina, apenas se mitiga — via RAG, verificação externa, guardrails e revisão humana. Em geração de código, manifesta-se sobretudo como chamadas a bibliotecas inexistentes e edge cases silenciosamente ignorados.

### inference
O processo de usar um modelo já treinado para gerar saídas a partir de uma entrada; em LLMs, a geração autorregressiva de tokens, um de cada vez. Contrasta com o treinamento: na inferência os pesos são fixos. É a fase que domina o custo operacional em produção e tende a ser limitada pela largura de banda de memória, não pelo poder bruto de cálculo.

### KV cache
Uma técnica de otimização para inferência de Transformers que armazena os vetores Key (K) e Value (V) dos tokens anteriores na memória da GPU. Isso evita cálculos redundantes durante a geração autorregressiva, reduzindo a complexidade computacional de $O(N^2)$ para $O(N)$ por novo token, mas aumenta significativamente o uso de VRAM conforme o comprimento da sequência cresce.

### LLM (Large Language Model)
Uma rede neural — tipicamente um transformer apenas com decodificador (decoder-only) — treinada em grandes corpora de texto para prever o próximo token dada uma sequência. LLMs modernos escalam para bilhões ou trilhões de parâmetros e exibem capacidades emergentes como aprendizado em contexto e seguimento de instruções.

### logit
O score bruto e não normalizado que o modelo produz para cada token do vocabulário na camada final, antes de qualquer normalização. É um número real em escala arbitrária (pode ser negativo); o [[Dicionário de IA#softmax|softmax]] os converte numa distribuição de probabilidades de onde o próximo token é amostrado. Parâmetros como [[Dicionário de IA#temperature|temperature]], [[Dicionário de IA#top-k|top-k]] e [[Dicionário de IA#top-p|top-p]] operam sobre os logits (ou a distribuição derivada deles) para moldar a [[Dicionário de IA#decoding strategy|decoding strategy]].

### memory bandwidth bottleneck
Um gargalo de desempenho onde a velocidade de transferência de dados entre a memória (HBM/VRAM) e o processador limita a execução mais do que o poder bruto de processamento. Na inferência de LLMs, a natureza sequencial da geração de tokens força o modelo a ler todos os seus parâmetros da memória para cada token produzido, tornando a fase de "decode" fortemente limitada pela largura de banda da memória.

### MLA (Multi-head Latent Attention)
Variante de atenção introduzida no DeepSeek-V2 (2024) que comprime os vetores Key/Value num vetor latente de baixo rank antes de cachear — uma down-projection grava só o latente no [[Dicionário de IA#KV cache|KV cache]], e up-projections reconstroem K/V completos na hora da atenção. Reduz o cache em ~1 ordem de grandeza versus multi-head attention pura, indo além do [[Dicionário de IA#GQA (Grouped-Query Attention)|GQA]] (que apenas compartilha K/V entre heads); é a base dos kernels FlashMLA e da família DeepSeek-V3.

### modelos open-weight
Modelos cujos pesos treinados são publicados para download, permitindo rodar localmente, self-hostear e fazer fine-tuning (ex.: Llama, Mistral, Qwen, DeepSeek). O termo distingue-se de "open source" porque os pesos vêm frequentemente sem os dados de treino, o código de treinamento ou uma licença plenamente livre — abre-se o artefato, não a receita. Contrasta com modelos fechados servidos só via API (GPT, Claude, Gemini).

### parameters / weights
Os valores numéricos aprendidos durante o treino que definem o comportamento de uma rede neural — as conexões entre neurônios ajustadas para minimizar o erro. A contagem de parâmetros (bilhões a trilhões em LLMs) é uma medida grosseira de capacidade; na inferência eles ficam fixos e precisam ser lidos da memória a cada token, o que liga o tamanho do modelo ao memory bandwidth bottleneck.

### position embeddings
Vetores que codificam a posição de cada token na sequência, injetados nos embeddings de tokens para que o transformer — que processa todos os tokens em paralelo e é intrinsecamente insensível à ordem — saiba quem vem antes de quem. Podem ser fixos (sinusoidais, do paper original *Attention Is All You Need*), aprendidos durante o treino (GPT, BERT) ou relativos/rotacionais como o [[Dicionário de IA#RoPE (Rotary Position Embedding)|RoPE]], dominante nos modelos open-weight modernos.

### prefill
A primeira fase da inferência de um LLM, na qual o modelo processa o prompt inteiro de uma vez para construir o KV cache e preparar a geração. É **compute-bound** — o custo cresce quadraticamente com o tamanho do contexto, dominando o TTFT (time-to-first-token). Contrasta com o **decode**, fase token-a-token, que é memory-bandwidth-bound.

### pretraining
A fase inicial e mais cara do treino de um LLM, em que o modelo aprende a prever o próximo token sobre corpora massivos e não rotulados (trilhões de tokens), adquirindo de forma auto-supervisionada conhecimento linguístico, factual e de raciocínio. Produz o base model — um previsor de texto cru, sem comportamento de assistente; fases posteriores (fine-tuning, RLHF) o especializam e alinham. É o que define o knowledge cutoff do modelo.

### Quantização
Técnica de compressão que reduz a precisão numérica com que os [[Dicionário de IA#parameters / weights|pesos]] (e às vezes ativações) de um modelo são armazenados — tipicamente FP16 → INT8 → INT4 — sem alterar a contagem de parâmetros nem a arquitetura. Corta uso de VRAM e custo de inferência (INT4 usa ~4× menos memória que FP16) com perda de qualidade crescente em raciocínio complexo nos bits mais baixos. Aplicada quase sempre depois do treino (PTQ); formatos comuns são GGUF/k-quants, GPTQ, AWQ e NF4. Ver [[Anatomia dos LLMs/18 - Compressão de modelos — quantização e destilação]].

### RoPE (Rotary Position Embedding)
Esquema de codificação posicional em transformers que aplica rotações 2D aos vetores de query e key proporcionais à posição do token, em vez de somar embeddings posicionais aprendidos. Permite extrapolação relativa entre posições e é a base posicional de Llama, Qwen, Mistral e a maioria dos modelos open-weight modernos. Técnicas como YaRN e NTK-aware extension partem do RoPE para estender o contexto além do pretraining.

### sampling
A escolha estocástica do próximo token a partir da distribuição de probabilidades do modelo, em vez de pegar sempre o mais provável. Parâmetros como temperature, top-k e top-p moldam quão aleatória ou conservadora é a seleção, controlando o trade-off entre diversidade e coerência da saída.

### softmax
A função que converte um vetor de scores brutos (logits) numa distribuição de probabilidades — exponencia cada valor e normaliza para que somem 1. No transformer aparece em dois pontos críticos: pondera os pesos de [[Dicionário de IA#attention|atenção]] (forçando cada token a distribuir 100% da sua atenção entre os demais, o que origina o [[Dicionário de IA#attention sink|attention sink]]) e converte os logits da camada final na distribuição sobre o vocabulário de onde o próximo token é amostrado. A [[Dicionário de IA#temperature|temperature]] atua justamente escalando os logits antes do softmax.

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

### TTFT (time-to-first-token)
Latência entre o envio de um request a um LLM e a chegada do primeiro token gerado. É dominada pela fase de **prefill**, cuja complexidade é quadrática no tamanho do contexto, e por isso cresce rápido com prompts longos. Métrica crítica em UX de chat e ferramentas interativas, distinta de **TPOT** (time-per-output-token), que mede o ritmo do streaming após o primeiro token.

### YaRN
*Yet another RoPE extensioN.* Método para estender a janela de contexto de modelos baseados em RoPE sem retrainar do zero. Combina escala de frequências por faixa (piecewise) com ajuste da temperatura da atenção; consegue 2–4x de extensão usando ~10x menos tokens de finetune que abordagens anteriores. É a técnica por trás de várias extensões de 32k → 128k+ em modelos Llama-derivados.

## MCP — Model Context Protocol

### MCP (Model Context Protocol)
Um protocolo aberto que padroniza como aplicações de LLM expõem contexto, ferramentas e prompts para modelos através de uma arquitetura cliente-servidor. Ele desacopla os provedores de modelos das fontes de dados, permitindo que qualquer cliente compatível com MCP se conecte a qualquer servidor MCP.

### MCP client
O componente, embutido na aplicação host (ex.: um coding agent), que abre e mantém a conexão com um servidor MCP, descobre os recursos, ferramentas e prompts que ele expõe e os repassa ao modelo. Cada cliente fala com um servidor; é a metade do protocolo que consome capacidades.

### MCP server
Um processo que expõe ferramentas, recursos e prompts a clientes MCP através do protocolo padronizado, desacoplando uma fonte de dados ou capacidade do modelo que a consome. Pode rodar localmente (via stdio) ou remotamente (via HTTP/SSE); qualquer cliente compatível pode usá-lo sem integração customizada.

### MCP Tasks (SEP-1686)
Primitiva experimental do MCP (proposta SEP-1686, 2026) para comunicação assíncrona entre agentes, no padrão *call-now, fetch-later*: o cliente dispara uma operação de longa duração e busca o resultado depois, em vez de bloquear. O roadmap 2026 do protocolo mira fechar gaps de lifecycle — semântica de *retry* em falhas transitórias e políticas de expiração de resultados. *Status experimental.*

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

### Lost in the Middle
O fenômeno em que LLMs aproveitam melhor a informação no início e no fim do contexto e tendem a ignorar o que está no meio, formando uma curva de atenção em U. Tem impacto direto em RAG: um chunk relevante que caia no meio de um top-K longo pode ser desprezado mesmo tendo sido recuperado — daí a prática de posicionar os chunks de maior score nas pontas do contexto. Documentado por Liu et al. (2023).

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

### EU AI Act
Regulamentação europeia (Regulation (EU) 2024/1689) que classifica sistemas de IA por nível de risco e impõe obrigações proporcionais: práticas proibidas (banimentos), alto risco (avaliação de conformidade, transparência, supervisão humana, logging), GPAI (modelos de propósito geral) e risco mínimo. Cronograma de aplicação escalonado: banimentos desde fevereiro de 2025, obrigações GPAI desde agosto de 2025, regime completo de alto risco em agosto de 2026. Multas até €35M ou 7% do faturamento global. Sistemas de LLM em produção precisam de tracing (Art. 12) e DPIA-equivalente quando processam dados pessoais. Ver [[Observability/08 - Privacy e PII em logs]] e [[Segurança e Guardrails/11 - Governance as architecture — EU AI Act, GDPR, licenças]].

### GDPR
General Data Protection Regulation (Regulation (EU) 2016/679), em vigor desde maio de 2018. Estabelece direitos do titular de dados (acesso, retificação, apagamento, portabilidade), bases legais pra tratamento (consentimento, legítimo interesse, etc.), princípios de minimização e finalidade, obrigação de DPIA (Art. 35) para tratamentos de alto risco, e papel do DPO. Multas até €20M ou 4% do faturamento global. Em sistemas LLM, atinge logs de prompts contendo PII, retenção de traces e treinamento de modelos com dados pessoais. Ver [[Observability/08 - Privacy e PII em logs]].

### Guardrail
Uma restrição aplicada à entrada ou saída do LLM para impor requisitos de segurança, política ou qualidade — por exemplo, bloqueando informações de identificação pessoal (PII), filtrando conteúdo prejudicial, validando esquemas de saída estruturada ou recusando solicitações fora do tópico. Guardrails podem ser aplicados no modelo (fine-tuning, system prompt) ou no pipeline (pré/pós processamento).

### jailbreak
Uma técnica de prompt que contorna os guardrails e o alinhamento de um modelo para induzi-lo a produzir conteúdo proibido — via role-play, ofuscação, instruções contraditórias ou cenários hipotéticos. É uma forma específica de ataque que explora a tensão entre seguir instruções e respeitar restrições.

### LGPD
Lei Geral de Proteção de Dados Pessoais (Lei 13.709/2018), em vigor desde setembro de 2020 no Brasil. Define dado pessoal sensível (Art. 5º II), direitos do titular (Art. 18), bases legais pra tratamento (Art. 7º), e obriga relatório de impacto à proteção de dados pessoais em tratamentos de alto risco. Fiscalizada pela ANPD (Autoridade Nacional de Proteção de Dados); multas até 2% do faturamento limitadas a R$50M por infração (Art. 52, II). Em sistemas LLM, atinge logs de prompts, traces, e treinamento. Ver [[Observability/08 - Privacy e PII em logs]].

### output validation
A verificação programática da saída do modelo antes de usá-la — checagem de schema/JSON, tipos, faixas de valor, ausência de PII ou conformidade com regras de negócio. É um guardrail de pós-processamento que transforma a saída probabilística do LLM em algo confiável para sistemas downstream.

### prompt injection
Um ataque em que instruções maliciosas embutidas na entrada — ou em conteúdo externo que o modelo lê (uma página, um documento, um e-mail) — sequestram o comportamento do agente, sobrepondo-se às instruções legítimas. É o risco de segurança definidor de agentes com tool use, já que o modelo não distingue de forma confiável dados de comandos.

### red teaming
A prática de testar adversarialmente um sistema de IA — sondando-o com jailbreaks, prompt injections e casos extremos — para descobrir falhas de segurança e alinhamento antes que sejam exploradas em produção. Pode ser manual ou automatizada e alimenta o desenho de guardrails mais robustos.

## Sequence Models

### BERT (Bidirectional Encoder Representations from Transformers)
Modelo Transformer encoder-only da Google (Devlin et al., 2018) pré-treinado em duas tarefas auto-supervisionadas — masked language modeling (prever tokens mascarados) e next sentence prediction —, capturando contexto bidirecional da sequência inteira. Ao contrário dos modelos decoder-only como o [[Dicionário de IA#GPT (Generative Pre-trained Transformer)|GPT]], o BERT é otimizado para tarefas de compreensão de linguagem (classificação, NER, QA) e não para geração de texto; popularizou o paradigma de pre-training + fine-tuning em NLP.

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

### JSON Schema
Especificação (json-schema.org) usada como contrato para structured outputs em LLMs. Define `type`, `properties`, `required`, `enum`, `additionalProperties` etc.; OpenAI strict mode e Gemini structured output usam subsets dela, e Anthropic a consome via `tool input_schema`. Ver [[Structured Outputs/02 - JSON Schema como contrato]].

### SDK
Um kit de desenvolvimento — biblioteca em uma linguagem específica (Python, TypeScript) — que abstrai as chamadas HTTP cruas à API de um provedor de LLM, oferecendo tipos, autenticação, streaming e tratamento de erros. Exemplos: o Anthropic SDK e o OpenAI SDK.

### Strict mode (Structured Outputs)
Modo do OpenAI Structured Outputs que garante aderência total ao JSON Schema (response_format com `strict: true`). Aceita apenas um subset limitado de features de JSON Schema — sem `additionalProperties: true`, com todas as properties em `required` — em troca de output garantidamente válido. Ver [[Structured Outputs/04 - OpenAI Structured Outputs — strict mode]].

### structured output
Uma saída do modelo restrita a um formato verificável — tipicamente JSON conforme um schema declarado — em vez de texto livre, garantida por validação ou por decodificação restrita (constrained decoding). Torna a resposta do LLM consumível diretamente por código, sem parsing frágil.

### tool call
A ação de um modelo de linguagem ao invocar uma ferramenta externa durante uma geração. O modelo produz um bloco estruturado com o nome da ferramenta e seus argumentos; o framework executa a ferramenta e devolve o resultado como input do próximo turno. Erros de sintaxe em tool calls disparam retries automáticos — cada um custando um turno completo de tokens acumulados.

### tool definition
A especificação estruturada (tipicamente JSON Schema) que descreve para o modelo o nome, descrição e parâmetros aceitos de uma ferramenta disponível. Tool definitions são enviadas no system prompt a cada turno, tornando-se um custo fixo por chamada independentemente de quantas ferramentas são realmente usadas.

## Fundamentos

### heurística
Uma regra prática ou função aproximada que guia a tomada de decisão e a busca por soluções quando o cálculo exato é inviável ou caro demais, trocando garantia de otimalidade por eficiência. Em IA clássica, aparece como função heurística que estima a distância até o objetivo em algoritmos de busca (ex.: A*, IDA*); em sistemas modernos, embasa regras de poda, decisões de agentes e atalhos de design em prompting.
