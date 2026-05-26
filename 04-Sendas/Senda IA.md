---
title: "Trilha IA"
created: 2026-04-01
updated: 2026-05-02
type: moc
status: evergreen
tags:
  - ia
  - trilha
  - roadmap
  - aprendizado
publish: true
---

# Trilha IA

> Roadmap estruturado para um fullstack senior sair de **zero conhecimento em IA** até **domínio operacional** em ~9-12 meses de estudo consistente (10-15h/semana). Esta é a trilha que eu seguiria hoje se tivesse que recomeçar. Otimizada para **shipping features com IA em produção**, não para virar ML researcher. Cada fase tem objetivo claro, checkpoints de progresso, e links para as notas evergreen correspondentes.

> [!info] Esta senda vs Formação Engenheiro de IA
> **Esta senda** é um **roadmap pessoal** com fases mensais, projetos hands-on e checkpoints. É o "como eu estudaria do zero".
>
> A **[[03-Dominios/IA/index|Formação Engenheiro de IA]]** é um **curriculum de leitura** com 8 trilhas atomizadas + 4 sendas transversais (Praticante, Arquiteto, Líder Técnico, Open Source). É a "biblioteca de referência".
>
> As duas se complementam: use **esta senda** para definir o que estudar quando; use a **Formação** como fonte de notas detalhadas em cada fase.

## Princípios da trilha

1. **Top-down, não bottom-up.** Não começar por matemática. Começar por intuição e uso; desce para fundamentos só quando precisa.
2. **Praticar desde o dia 1.** Cada fase tem projetos. Conhecimento sem aplicação evapora.
3. **Uma ferramenta a fundo antes de espalhar.** Dominar Claude Code + Anthropic SDK antes de tentar cobrir OpenAI, Gemini, frameworks.
4. **RAG antes de fine-tuning.** Custo-benefício real.
5. **Evaluation desde cedo.** Sem golden set é superstição.
6. **Construir portfolio público.** Repos, blog posts, exemplos — isso destrava oportunidades.
7. **Inglês técnico junto.** Ler papers, docs, posts em inglês. É onde o conhecimento vive.

## Como usar este roadmap

- **Não pule fases.** Cada uma depende da anterior.
- **Marque checkpoints.** Só avance quando atender o "Check".
- **Se travar, revisite fase anterior.** Gaps de fundamento aparecem como dor em fases avançadas.
- **Adapte ritmo.** 10h/semana = ~12 meses; 20h/semana = ~6 meses.
- **Documente.** Blog ou notas pessoais; ensinar solidifica.

## Visão geral (12 meses)

```text
Mês 1     | Fase 0: Cultura e intuição
Mês 2-3   | Fase 1: Fundamentos conceituais
Mês 4-5   | Fase 2: LLMs hands-on (APIs, prompting)
Mês 6-7   | Fase 3: RAG e knowledge bases
Mês 8-9   | Fase 4: Agents e orquestração
Mês 10-11 | Fase 5: Produção (eval, custo, segurança)
Mês 12+   | Fase 6: Especialização
```

## Fase 0 — Cultura e intuição (1-2 semanas)

**Objetivo:** calibrar radar. Saber distinguir sinal de hype. Entender o vocabulário.

### O que fazer

- Usar ChatGPT, Claude e Gemini pesadamente em problemas reais por 1-2 semanas.
- Assistir: [3Blue1Brown — Neural Networks series](https://www.3blue1brown.com/topics/neural-networks).
- Ler: [The Illustrated Transformer — Jay Alammar](https://jalammar.github.io/illustrated-transformer/).
- Seguir: [Simon Willison's Weblog](https://simonwillison.net/) por algumas semanas.
- Fazer conta na [Anthropic Console](https://console.anthropic.com/) e na [OpenAI Platform](https://platform.openai.com/).

### Notas de apoio

- [[03-Dominios/IA/index|Inteligência Artificial]] — seção "O que é" e "Hierarquia dos conceitos"
- [[Comparativo de LLMs]] — para escolher qual ferramenta usar

### Checkpoint

> Você consegue explicar para um colega não-técnico a diferença entre "machine learning", "deep learning" e "LLM" com exemplos concretos. Você identifica buzzwords vs substância em posts sobre IA.

## Fase 1 — Fundamentos conceituais (4-6 semanas)

**Objetivo:** modelo mental correto de ML, deep learning, e como LLMs se encaixam.

### O que fazer na Fase 1

**Estude** (~80% do tempo):

- ML básico: supervised/unsupervised/RL, training/validation/test, overfitting, métricas (accuracy, precision, recall, F1).
- Deep learning geral: rede neural, backprop (intuição), loss, ativação.
- Tokenização, embeddings, similaridade de cosseno.
- Transformer e attention (intuitivamente).
- Pretraining → fine-tuning → RLHF — entender por que modelos se comportam como se comportam.

**Pratique** (~20%):

- Sklearn: classificar um dataset próprio (spam, sentiment, etc.).
- Tokenizar texto com tiktoken e analisar.
- Calcular cosine similarity entre embeddings de frases.

### Recursos principais (Fase 1)

- Livro: *Hands-On Machine Learning* — Aurélien Géron (partes I-II)
- Curso: [Andrew Ng — ML Specialization](https://www.coursera.org/specializations/machine-learning-introduction)
- Curso: [fast.ai — Practical Deep Learning](https://course.fast.ai/)
- Vídeo: [Let's build GPT from scratch — Karpathy](https://www.youtube.com/watch?v=kCc8FmEb1nY) (2h, opcional mas transformador)
- Blog: [The Illustrated Transformer](https://jalammar.github.io/illustrated-transformer/)

### Notas de apoio (Fase 1)

- [[03-Dominios/IA/index|Inteligência Artificial]] — trilha completa de conceitos
- [[Anatomia dos LLMs|LLMs]] — fundamentos de arquitetura

### Checkpoint da Fase 1

> Você lê um tweet sobre GPT-5 ou Claude 5 e entende o que está sendo discutido sem precisar pesquisar termos. Você explica CoT, attention, context window, RLHF em linguagem simples.

## Fase 2 — LLMs hands-on (6-8 semanas)

**Objetivo:** proficiência real em usar LLMs, via chat e via API.

### O que fazer na Fase 2

**Prompting**:

- Zero-shot, few-shot, chain-of-thought, self-consistency.
- System prompts estruturados (role + rules + format + examples).
- XML delimiters.
- Output constraints.

**API**:

- Anthropic Messages API — chat básico, streaming, tool use, structured outputs.
- OpenAI Chat Completions — paralelo, comparar.
- Parâmetros: temperature, top_p, max_tokens, stop, system.
- Prompt caching.

**Projetos** (obrigatório fazer pelo menos 3):

1. **Chatbot terminal com histórico** — streaming, Claude API.
2. **Classificador de tickets** — few-shot com structured outputs. Construa golden set de 30 exemplos, meça accuracy.
3. **Extrator estruturado de PDFs** — recebe texto livre, retorna JSON validado por schema.
4. **Sumarizador com chunking** — processa doc longo via chunk → summary → consolidate.

### Recursos da Fase 2

- [Anthropic Prompting Guide](https://docs.anthropic.com/en/docs/build-with-claude/prompt-engineering/overview)
- [Anthropic API docs](https://docs.anthropic.com/en/api/messages)
- [OpenAI API docs](https://platform.openai.com/docs)
- [Prompting Guide (community)](https://www.promptingguide.ai/)
- [Effective Context Engineering — Anthropic](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents)

### Notas de apoio (Fase 2)

- [[Anatomia dos LLMs|LLMs]] — parâmetros da API, tokenização, sampling
- [[Context Engineering]] — técnicas e context engineering

### Checkpoint da Fase 2

> Você consegue levantar uma feature de IA em projeto real num dia. Escolhe modelo justificadamente. Seus prompts têm estrutura clara. Você mede accuracy/faithfulness contra golden set antes de dar deploy.

## Fase 3 — RAG e bases de conhecimento (6-8 semanas)

**Objetivo:** dominar retrieval-augmented generation. Injetar dados do seu domínio em LLMs.

### O que fazer na Fase 3

**Fundamentos**:

- Embeddings: modelos, dimensões, custo.
- Vector databases: pgvector, Pinecone, Qdrant — escolher e usar.
- Chunking: fixed, recursive, semantic, structure-aware.
- Hybrid search (BM25 + vector), reranking.
- Query rewriting, HyDE.

**Evaluation**:

- Ragas: context precision, recall, faithfulness.
- Golden set com (pergunta, resposta, chunks esperados).
- Medir retrieval separado de generation.

**Projeto principal**:

- **QA sobre base de docs reais** — ~100 documentos (manuais, wiki, FAQs).
  - Indexar com structure-aware chunking.
  - Hybrid search + Cohere Rerank.
  - Citação de fonte obrigatória.
  - Golden set de 30 perguntas com respostas esperadas.
  - Ragas rodando em CI.

### Recursos da Fase 3

- [Pinecone — Learn RAG](https://www.pinecone.io/learn/retrieval-augmented-generation/)
- [Anthropic — Contextual Retrieval](https://www.anthropic.com/news/contextual-retrieval)
- [LlamaIndex docs](https://docs.llamaindex.ai/)
- [Ragas docs](https://docs.ragas.io/)
- Paper: [Lost in the Middle](https://arxiv.org/abs/2307.03172)
- Livro: *AI Engineering* — Chip Huyen (capítulos de RAG)

### Notas de apoio (Fase 3)

- [[RAG e Vector Databases]] — trilha completa atomizada (13 notas)
- [[RAG e Vector Databases|03 - Embeddings — representação semântica]] — embeddings deep dive
- [[RAG e Vector Databases|04 - Chunking — onde 50% da qualidade vive]] — chunking estratégias
- [[RAG e Vector Databases|06 - Retrieval — hybrid search, BM25, query rewriting]] — hybrid retrieval
- [[RAG e Vector Databases|13 - PageIndex — RAG vectorless por árvore de documentos]] — retrieval para documentos longos sem vector DB
- [[Anatomia dos LLMs|LLMs]] — embeddings, context window

### Checkpoint da Fase 3

> Você desenha RAG justificando cada escolha (chunk size, retrieval strategy, rerank). Implementa evaluation rigoroso. Seu RAG funciona melhor que "pure vector" em dataset próprio com evidência quantitativa.

## Fase 4 — Agents e orquestração (6-8 semanas)

**Objetivo:** construir sistemas que raciocinam, usam ferramentas e iteram autonomamente.

### O que fazer na Fase 4

**Fundamentos**:

- ReAct pattern, tool use nativo.
- Tool design: descrição, schemas, outputs compactos.
- Memory: working memory + persistent notes.
- Planning: plan-then-execute vs dynamic.
- Guardrails: max_steps, sandboxing, human-in-the-loop.
- MCP (Model Context Protocol): clients, servers, primitivos.

**Projetos**:

1. **Agent de research** — recebe pergunta, usa web search + read_url + record_finding, responde com citações. Construa do zero com Anthropic SDK, sem framework.
2. **MCP server próprio** — expõe 3 tools de um domínio que você conhece. Conecte a Claude Code ou Claude Desktop e use de verdade.
3. **Agent de coding restrito** — recebe bug report + arquivo, propõe diff. Sandboxed. Human review antes de aplicar.

### Recursos da Fase 4

- [Building Effective Agents — Anthropic](https://www.anthropic.com/research/building-effective-agents) — **leitura obrigatória**
- [Claude Agent SDK Docs](https://docs.anthropic.com/en/docs/agents)
- [Claude Code](https://docs.anthropic.com/en/docs/claude-code)
- [MCP spec](https://modelcontextprotocol.io/)
- [Awesome MCP Servers](https://github.com/punkpeye/awesome-mcp-servers)
- [12-Factor Agents](https://github.com/humanlayer/12-factor-agents)
- [Agentic Engineering — Addy Osmani](https://addyosmani.com/blog/agentic-engineering/)

### Notas de apoio (Fase 4)

- [[Anatomia de Agents]] — trilha completa de fundamentos genéricos (9 notas)
- [[Agentes de Codificação]] — coding agents (Cursor, Claude Code, Copilot)
- [[Context Engineering]] — pipelines, camadas, JIT retrieval, AGENTS.md, prompting, skills
- [[MCP]] — trilha completa: protocolo, servers, construção, segurança (10 notas)

### Checkpoint da Fase 4

> Você consegue construir um agent do zero, sem framework, e explicar cada decisão. Entende onde agents falham em produção. Tem um MCP server próprio rodando em uso real.

## Fase 5 — Produção (6-8 semanas)

**Objetivo:** operar sistemas com IA em produção com confiança. Custo, latência, segurança, evaluation.

### O que fazer na Fase 5

**Observabilidade**:

- Integrar Langfuse ou LangSmith em projeto real.
- Tracing: cada chamada LLM com input, output, tokens, latência, custo.
- Dashboards: cost per feature, error rate, p99 latency.

**Evaluation contínua**:

- Prompts como código (git, review, versionado).
- Golden sets por feature, rodados em CI.
- LLM-as-judge para tarefas subjetivas.
- A/B test em produção.

**Custo**:

- Tiering de modelos (Haiku/Flash para triagem, Sonnet/GPT-4 para escalada).
- Prompt caching agressivo.
- Batch API quando aplicável.
- Monitoramento de budget.

**Segurança**:

- Prompt injection defense (delimitação, allowlisting, classification).
- PII detection e filtering.
- OWASP Top 10 for LLMs.
- Supply chain: review de packages, servers, skills.

**Resiliência**:

- Retry, backoff, circuit breaker.
- Fallback para modelos alternativos.
- Rate limits do provedor.
- Schema validation com retry corrective.

### Projeto

- **Operacionalizar um projeto anterior em "produção simulada"**: observabilidade completa, golden set em CI, cost dashboard, fallbacks, segurança.

### Recursos da Fase 5

- Livro: *AI Engineering* — Chip Huyen (capítulos finais)
- [Langfuse docs](https://langfuse.com/docs)
- [OWASP Top 10 for LLMs](https://owasp.org/www-project-top-10-for-large-language-model-applications/)
- [Simon Willison — Prompt injection](https://simonwillison.net/series/prompt-injection/)
- [Patterns for building LLM-based systems — Eugene Yan](https://eugeneyan.com/writing/llm-patterns/)

### Notas de apoio (Fase 5)

- [[Anatomia dos LLMs|17 - Evaluation de LLMs em produção]] — golden set, LLM-as-judge, traces
- [[Anatomia de Agents|09 - Evaluation de agents]] — task completion, regression tests
- [[Economia de Tokens]] — trilha completa: monitoramento, hard limits, ROI
- [[Segurança e Guardrails]] — trilha completa: SAST, sandbox, slopsquat, EU AI Act
- [[Spec-Driven Development]] — disciplina sobre AI code, validation contínua
- [[RAG e Vector Databases]] — evaluation de RAG

### Checkpoint da Fase 5

> Você assume ownership de um sistema com IA em produção. Sabe debugar, otimizar, responder incidentes. Seu custo é previsível e seus deploys são seguros.

## Fase 6 — Especialização (ongoing)

**Objetivo:** aprofundar em um vetor específico. Não tente fazer tudo; escolha um foco por 6 meses.

### Vetores possíveis

**ML real:** voltar e aprender fine-tuning (LoRA, QLoRA, DPO), model training, evaluation rigorosa. Ideal se você se apaixonar pela parte técnica.

**Agentic engineering:** multi-agent orchestration, planning complexo, tool design avançado, RL from execution feedback. Ideal para quem quer construir agents sofisticados.

**Ferramentas e workflows:** virar expert em uma stack (Claude Code + skills + MCP + CLAUDE.md). Publicar skills, contribuir para ecossistema, ensinar.

**AI-native product:** pensar produto com IA no centro, não como feature. Design de UX para IA, gestão de expectativas, onboarding.

**Research:** ler papers semanalmente, entender estado da arte, seguir labs (Anthropic, OpenAI, DeepMind, Meta AI).

**Domain-specific:** aplicar IA ao seu domínio — medicina, legal, finance, education. Construir expertise profunda na interseção.

### Recursos contínuos

- Simon Willison blog e newsletter
- The Pragmatic Engineer — seção AI
- Latent Space Podcast
- Anthropic Engineering blog
- Papers with Code
- Hugging Face blog
- [DeepLearning.AI short courses](https://www.deeplearning.ai/short-courses/) — dezenas de cursos curtos

## Ferramentas recomendadas por fase

| Fase | Essenciais                                            | Opcionais                       |
| ---- | ----------------------------------------------------- | ------------------------------- |
| 0    | ChatGPT, Claude, Gemini web                           | —                               |
| 1    | Jupyter, sklearn, numpy, pandas                       | fast.ai lib                     |
| 2    | Anthropic SDK, OpenAI SDK, tiktoken, promptfoo        | LangChain (leve)                |
| 3    | pgvector, sentence-transformers, Ragas, Cohere Rerank | Pinecone, Qdrant, LlamaIndex    |
| 4    | Anthropic SDK, Claude Code, MCP SDK                   | LangGraph, CrewAI               |
| 5    | Langfuse, promptfoo, Sentry                           | Helicone, LangSmith, Braintrust |
| 6    | depende do vetor escolhido                            | —                               |

## Projetos para portfolio

Ao final das fases 2-5, você deve ter no GitHub pelo menos:

1. **Chatbot com streaming** (fase 2)
2. **Classificador com structured outputs + golden set** (fase 2)
3. **Sumarizador de documentos longos** (fase 2)
4. **QA RAG sobre docs reais com evaluation** (fase 3)
5. **Agent de research com MCP server próprio** (fase 4)
6. **Sistema de produção com observabilidade completa** (fase 5)

Isso é um portfolio forte. Acompanhe cada repo com README que explica decisões, trade-offs e evaluations.

## Links de referência (legado)

### AGENTS.md e context engineering

- [Como reduzi em 70% o uso do context window no Copilot](https://www.linkedin.com/pulse/como-reduzi-em-70-o-uso-do-context-window-github-copilot-lemos-cycnf/)
- [Complete Guide to AGENTS.md](https://www.aihero.dev/a-complete-guide-to-agents-md)
- [Effective Context Engineering — Anthropic](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents)

### Agent Skills

- [Agent Skills spec](https://agentskills.io/home)
- [Agent Skills in 2026 — Neon](https://neon.com/blog/agent-skills-in-2026)
- [Equipping Agents with Skills — Claude Blog](https://claude.com/blog/equipping-agents-for-the-real-world-with-agent-skills)
- [Claude Agent Skills](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/overview)
- [Cursor Skills](https://cursor.com/docs/context/skills)
- [Codex Skills](https://developers.openai.com/codex/skills/)
- [Anthropic Skills repo](https://github.com/anthropics/skills)
- [Awesome Copilot Skills](https://github.com/github/awesome-copilot/tree/main/skills)
- [CopilotSkills](https://github.com/Oxilith/CopilotSkills)
- [Antigravity Kit](https://github.com/vudovn/antigravity-kit) — [docs](https://antigravity-kit.vercel.app/docs)
- [Antigravity Workflows](https://github.com/harikrishna8121999/antigravity-workflows)
- [Skills CLI (skills.sh)](https://skills.sh/)

### Ferramentas Claude

- [Claude Course](https://www.youtube.com/watch?v=WLZqPonSrK0)
- [Context Lens](https://github.com/TiagoSchr/context-lens)
- [Everything Claude Code](https://github.com/affaan-m/everything-claude-code)
- [Junie (JetBrains AI)](https://www.jetbrains.com/guide/ai/article/junie/)

### Copilot

- [Copilot Customization Overview](https://code.visualstudio.com/docs/copilot/customization/overview)
- [Awesome Copilot](https://github.com/github/awesome-copilot)

### Agentic Engineering e leituras

- [Agentic Engineering — Addy Osmani](https://addyosmani.com/blog/agentic-engineering/)
- [Factory Model — Addy Osmani](https://addyosmani.com/blog/factory-model/)
- [The Third Golden Age of Software](https://newsletter.pragmaticengineer.com/p/the-third-golden-age-of-software)
- [Spec-Driven Development](https://www.infoq.com/articles/spec-driven-development/)
- [12-Factor Agents](https://github.com/humanlayer/12-factor-agents)
- [Full Cycle com Agents (playlist)](https://www.youtube.com/playlist?list=PLucm8g_ezqNoAkYKXN_zWupyH6hQCAwxY)

### Testing AI

- [TestSprite](https://www.testsprite.com/)

## Veja também

- [[03-Dominios/IA/index|IA]] — portal do domínio
- [[03-Dominios/IA/index|Formação Engenheiro de IA]] — curriculum estruturado em 8 trilhas + 4 sendas transversais
- **Trilhas atomizadas:**
    - [[Anatomia dos LLMs]] · [[Anatomia de Agents]] · [[Agentes de Codificação]]
    - [[Economia de Tokens]] · [[Context Engineering]] · [[Spec-Driven Development]] · [[Segurança e Guardrails]]
    - [[Memória de Agentes]]
- **Notas conceituais:** [[03-Dominios/IA/index|Inteligência Artificial]] · [[Context Engineering]] · [[RAG e Vector Databases]] · [[MCP]]
- **Ferramentas:** [[Claude]] · [[GitHub Copilot]] · [[Codex]] · [[Gemini]] · [[Comparativo de LLMs]]
- **Sendas relacionadas:** [[Senda Entrevistas]]
