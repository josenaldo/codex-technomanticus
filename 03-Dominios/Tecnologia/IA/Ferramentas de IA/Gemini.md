---
title: "Gemini"
created: 2026-04-01
updated: 2026-04-11
type: concept
progress: backlog
status: evergreen
tags:
  - ia
  - llm
  - ferramentas
  - google
  - gemini
publish: true
---

# Gemini

> Gemini é a aposta do Google em [[Dicionário de IA#LLM (Large Language Model)|LLMs]], e em 2026 é o modelo mais multimodal e o único com [[Dicionário de IA#Context window|context window]] de 2M tokens. Para um fullstack senior, Gemini é relevante principalmente em três casos: (1) quando o problema envolve imagem, áudio ou vídeo nativamente; (2) quando você precisa processar documentos gigantes em uma única chamada; (3) quando sua stack já vive no Google Cloud. Fora desses casos, Claude e GPT costumam oferecer experiência melhor em coding interativo. Esta nota cobre os modelos, ferramentas (Gemini CLI, Code Assist, Vertex AI), diferenciais, limitações, e como encaixar Gemini na sua stack. Para comparação detalhada ver [[Comparativo de LLMs]].

## O que é

**Gemini** é a família de LLMs do **Google DeepMind**, lançada originalmente em dezembro de 2023 como sucessor de PaLM/Bard e rapidamente iterada (1.0 → 1.5 → 2.0 → 2.5). Em 2026, é o modelo multimodal mais completo do mercado — treinado desde o pretraining com texto, imagem, áudio, vídeo e código, não "bolted on" depois.

Posicionamento:

- **Google Cloud / Workspace first** — integração profunda com GCP, Workspace, Android, Chrome.
- **Multimodal nativo** — único a oferecer multimodalidade coesa entre tipos.
- **Contextos gigantes** — 1M a 2M tokens em 2.5 Pro.
- **Grounding com Google Search** — capacidade de buscar e citar dados atuais da web durante geração.
- **Live API** — interação voice + vision em tempo real (similar a Advanced Voice Mode).

### Ecosystem em 2026

1. **Gemini (app)** — interface consumer (web, mobile), sucessor do Bard.
2. **Gemini API / AI Studio** — APIs diretas com billing e prototipagem.
3. **Vertex AI** — plataforma enterprise no GCP com governance, data residency, model management.
4. **Gemini CLI** — CLI coding agent (análogo a Claude Code).
5. **Gemini Code Assist** — extensão para IDEs (análogo a Copilot).
6. **Gemini em Workspace** — Docs, Sheets, Gmail, Meet com Gemini embutido.
7. **Gemini Live** — voice + camera real-time em mobile.
8. **AgentSpace** — plataforma enterprise para agents no GCP.

## O que diferencia um senior usando Gemini

1. **Usa Gemini onde ele brilha** — multimodal, contexto gigante, grounding — e outros modelos no resto.
2. **Escolhe Vertex AI em enterprise** por governance e data residency.
3. **Aproveita grounding com Google Search** em vez de montar [[Dicionário de IA#RAG (Retrieval-Augmented Generation)|RAG]] quando a fonte é web pública.
4. **Usa multimodal real** (não só "imagem anexada") — combina texto + imagem + vídeo em um único prompt.
5. **Domina `GEMINI.md`** — análogo a CLAUDE.md, usado pelo Gemini CLI e Code Assist.
6. **Conhece o pricing Vertex AI vs API direta** — pode ser confuso.
7. **Usa Gemini 2.5 Flash como workhorse** de triagem com custo agressivo.
8. **Entende limitações do 2M window** — context rot real em tasks difíceis.
9. **Integra [[Dicionário de IA#MCP (Model Context Protocol)|MCP]]** quando possível (suporte crescente em 2026).
10. **Mede antes de migrar** — não assume "Gemini > X" baseado em benchmarks públicos.

## Modelos Gemini — família 2.5

Em 2026, a família ativa é Gemini 2.5 (atualizações 2.5 Pro, 2.5 Flash, 2.5 Flash-Lite). Algumas específicas emergem para coding (Gemini 2.5 Code).

| Modelo | Força | Context | Velocidade | Use case |
| --- | --- | --- | --- | --- |
| **Gemini 2.5 Pro** | Mais capaz, multimodal, contexto 2M | 1M-2M tokens | Médio | Análise complexa, multimodal, contextos gigantes |
| **Gemini 2.5 Flash** | Equilíbrio, barato e rápido | 1M tokens | Rápido | Workhorse diário, batch, streaming |
| **Gemini 2.5 Flash-Lite** | Ultra-rápido, ultra-barato | 1M tokens | Muito rápido | Classificação massiva, triagem |
| **Gemini 2.5 Code** | Coding-optimized | Amplo | Médio | Code completion, review, generation |

### Quando usar qual

**Pro:**

- Análise densa de documento longo
- Multi-modal complexa (imagem + vídeo + texto)
- Tasks com raciocínio profundo
- Contextos > 500K tokens

**Flash:**

- Default para produção em escala
- Chatbots
- Sumarização
- Tool use em agents

**Flash-Lite:**

- Classificação em volume
- Triagem de tickets
- Moderação de conteúdo
- Use case de latência < 100ms

## Diferenciais técnicos

### 1. Multimodal nativo

Gemini foi treinado desde o início com múltiplos modos. Não é um modelo de texto com um "encoder de imagem bolted on" — tokens de imagem, áudio, e vídeo vivem no mesmo espaço do que texto. Isso permite:

- **Image reasoning:** descrever, comparar, contar objetos em imagens.
- **Video understanding:** analisar sequências, captions automáticos, QA sobre vídeo.
- **Audio processing:** transcrição com contexto, análise de tonalidade, diarização.
- **Mixed prompts:** combinar tipos em um prompt ("olha essa imagem + esse vídeo e me diz se o produto é o mesmo").

Casos reais onde Gemini é objetivamente melhor que alternativas:

- Análise de screenshots/wireframes (UI, diagramas).
- Captions de vídeo em produção.
- OCR de formulários manuscritos.
- QA sobre docs que têm gráficos/tabelas (imagens).

### 2. Context window 2M

Gemini 2.5 Pro suporta até 2M tokens — o maior público entre principais LLMs em 2026. Permite:

- Carregar código-fonte de projetos médios inteiros.
- Processar vídeos longos (até ~2h de vídeo em contexto).
- Analisar dezenas de documentos em uma única chamada.

**Mas:** "lost in the middle" é real. Em tasks difíceis, recomenda-se RAG mesmo em contextos grandes.

### 3. Grounding com Google Search

Capability única de consultar Google Search durante a geração, citando URLs na resposta. Elimina [[Dicionário de IA#Hallucination|alucinação]] em fatos atuais e permite respostas com informação mais recente que o cutoff do modelo.

```python
response = client.generate_content(
    model="gemini-2.5-pro",
    contents="Qual é a última versão do React e quais breaking changes tem?",
    tools=[{"google_search": {}}]
)
# resposta cita URLs e retorna info atualizada
```

Útil em:

- Assistentes que precisam de dados atuais
- Research com citação
- QA sobre events recentes

### 4. Live API

API de tempo real com voice + video. Permite experiências como:

- Assistente de câmera que descreve o que vê em tempo real.
- Conversa por voz com latência sub-segundo.
- Tutor que "vê" a tela do aluno e guia.

Usada em apps mobile (Gemini Live no Android) e em alguns produtos consumer do Google.

### 5. Integração Google Cloud

Via Vertex AI, você obtém:

- **Data residency** — rodar em região específica.
- **Private endpoints** — tráfego não sai da VPC.
- **Model Garden** — catálogo com Gemini + modelos de terceiros (Anthropic inclusive via Vertex).
- **Integração IAM** do GCP.
- **Audit logs** centralizados.
- **Committed use discounts**.

Para empresas já no GCP, Vertex é natural.

## Gemini CLI — coding no terminal

CLI análogo a Claude Code. Permite interação conversacional para tarefas de coding com acesso ao filesystem.

```bash
# Instalação
npm install -g @google/gemini-cli

# Uso
gemini
> Implement pagination in src/api/users.ts using cursor-based approach
```

Features:

- Leitura de `GEMINI.md` na raiz do projeto como contexto
- Edição de arquivos com preview
- Execução de comandos shell
- Integração MCP (crescente em 2026)

Diferenças vs Claude Code:

- **Multimodal:** pode analisar screenshots, diagramas no contexto do projeto.
- **Context 2M:** pode carregar mais contexto de uma vez.
- **Grounding:** pode buscar docs oficiais em tempo real durante a task.

Em 2026, é uma alternativa viável ao Claude Code para quem está no ecossistema Google.

## Gemini Code Assist (IDE)

Extensão para VS Code e JetBrains, análogo a Copilot. Integra:

- Code completion
- Chat com contexto
- Smart actions (explain, refactor, test)
- Integração com Google Cloud (logs, metrics)

Pontos fortes:

- Integração com Google Cloud para debugging de apps hospedadas no GCP.
- Grounding em docs oficiais.
- Versão gratuita para devs individuais.

## GEMINI.md — contexto do projeto

Análogo a CLAUDE.md. Gemini CLI e Code Assist lêem automaticamente. Mesma filosofia:

```markdown
# Project Gemini instructions

Python FastAPI backend with Pydantic, SQLAlchemy, and pytest.

## Commands
- `poetry run pytest` — tests
- `poetry run ruff check` — lint
- `poetry run ruff format` — format
- `poetry run uvicorn main:app --reload` — dev server

## Conventions
- Async endpoints with async DB session
- Pydantic for all API models
- Dependency injection via FastAPI Depends
- Type hints mandatory
```

## Pricing (2026, aproximado)

Via API direta ou Vertex AI:

| Modelo | Input (/1M tokens) | Output (/1M tokens) |
| --- | --- | --- |
| Gemini 2.5 Pro | ~$1.25 (≤200K) / ~$2.50 (>200K) | ~$5 / ~$10 |
| Gemini 2.5 Flash | ~$0.30 | ~$2.50 |
| Gemini 2.5 Flash-Lite | ~$0.10 | ~$0.40 |

Em benchmarks de custo, **Gemini Flash é um dos mais agressivos** — frequentemente 2-3x mais barato que Claude Haiku em tasks equivalentes.

Ter em mente:

- Cobrança de contexto longo tem tier (>200K mais caro no Pro).
- Context caching disponível com descontos.
- Batch API para descontos adicionais.
- Free tier generoso para dev/prototipagem via AI Studio.

## Quando escolher Gemini

### Cenários onde brilha

- **Multimodal:** imagem, vídeo, áudio + texto em prompts.
- **Contextos gigantes:** processar documentos muito longos em uma chamada.
- **Budget-sensitive escala:** Flash/Flash-Lite são extremamente competitivos.
- **Stack GCP:** Vertex AI é natural, governance facilita.
- **Grounding:** quando precisa de info atual da web.
- **Mobile com Live API:** experiências voice+vision em tempo real.

### Cenários onde não é primeira escolha

- **Coding complexo interativo:** Claude Code ainda costuma levar.
- **Ecossistema de agents:** Anthropic MCP e Claude Agent SDK são mais maduros.
- **Tool use em produção crítica:** teste bem — Claude/GPT são mais consistentes historicamente.

### Recomendação prática em abril/2026

- **Multimodal qualquer coisa:** comece com Gemini.
- **Contexto > 500K:** Gemini 2.5 Pro.
- **Classificação em alta escala:** considere Gemini Flash-Lite vs Haiku lado a lado em benchmark próprio.
- **Outros use cases:** Claude ou GPT, a menos que o stack já esteja no GCP.

## Armadilhas comuns

### 1. Assumir "2M tokens funcionam perfeitamente"

Context rot é real. **Fix:** teste empiricamente; use RAG para > 500K.

### 2. Usar Pro onde Flash resolveria

Flash é bom o suficiente para 90% dos casos. **Fix:** default Flash, escala para Pro.

### 3. Grounding sem validação

Google Search pode retornar info errada ou desatualizada. **Fix:** sempre validar citações para decisões críticas.

### 4. Ignorar diferença de pricing API vs Vertex

Mesma model, pricing pode variar. **Fix:** ler docs específicas antes de comparar com Claude/GPT.

### 5. Multimodal "só porque tem"

Nem todo problema precisa de imagem/áudio. **Fix:** usar multimodal onde agrega, não como diferencial artificial.

### 6. GEMINI.md vs CLAUDE.md vs AGENTS.md

Projeto polyglot de agents precisa decidir qual manter. **Fix:** em 2026, AGENTS.md está virando comum; replique em GEMINI.md se Gemini CLI for primary.

### 7. Sem data residency em enterprise

Dados de saúde/finanças em API direta sem garantias. **Fix:** Vertex AI com configuração apropriada.

### 8. Esquecer rate limits

AI Studio free tier tem limits agressivos. **Fix:** migrar para paid quando usage sobe.

### 9. Live API sem planning de custo

Streaming contínuo soma tokens rápido. **Fix:** budget e telemetria por sessão.

### 10. Comparar benchmarks sem replicar

Claims de "Gemini > Claude em X" frequentemente não replicam no seu caso. **Fix:** golden set próprio.

## Como ganhar experiência prática

Esta nota é estrutura sobre Gemini. Para internalizar, prática é insubstituível. Três caminhos curados:

### Caminho 1 — Multimodal exploratório (1 semana)

Em problema real que envolva imagem + texto (análise de screenshot UI, OCR + raciocínio sobre diagrama, descrição de fotos):

- Implementar com Gemini 2.5 Pro via AI Studio (free tier generoso)
- Comparar com Claude Sonnet (vision) no mesmo problema
- Golden set de 20 exemplos + métricas (acurácia, latência, custo)

**Critério de sucesso:** entende empiricamente onde Gemini multimodal brilha e onde Claude/GPT são equivalentes.

### Caminho 2 — Long context vs RAG no Codex Technomanticus (1 semana)

Comparação prática:

- Base de notas do vault (~500K tokens depois de meses de uso)
- Tentar RAG normal com Gemini Flash + embeddings
- Tentar jogar tudo no contexto (Gemini 2.5 Pro com 1M-2M tokens)
- Comparar: latência, custo por query, qualidade no golden set

**Critério de sucesso:** tem opinião própria, baseada em dados, sobre quando 2M context vale e quando RAG ganha.

### Caminho 3 — Vertex AI enterprise setup em projeto profissional (quando aparecer)

Em projeto profissional regulado (saúde, finance, gov), configurar projeto GCP com Vertex AI: Gemini habilitado, região restrita (data residency), IAM granular, audit log no Cloud Logging, deploy via endpoint privado. Comparar TCO vs API direta.

**Critério de sucesso:** entende differenças concretas Vertex vs API direta para compliance.

---

**Sugestão de ordem:** Caminho 1 → Caminho 2 → Caminho 3.

**Princípios universais:**

- **Multimodal é o killer app do Gemini.** Em texto puro, Claude costuma superar em qualidade mesmo quando benchmarks públicos sugerem o contrário.
- **Flash é extremamente competitivo em custo.** Para workloads de classificação, vale benchmark próprio.
- **Vertex AI em enterprise é diferenciador.** Data residency, IAM, audit logs — coisas que em API direta exigem trabalho próprio.
- **Live API ainda é nicho** mas promissor para apps mobile.
- **Context 2M é "nice to have"**, não game-changer — RAG continua sendo melhor pattern para a maior parte dos casos.

## How to explain in English

### Short pitch

"Gemini is Google's LLM family, and in 2026 it's the most capable multimodal model in production and the only one with a 2M context window. The right use cases are anything multimodal, very long context tasks, and high-volume classification where Flash-Lite offers the best cost per token. For interactive coding, Claude Code typically leads, but Gemini CLI is a solid alternative for teams already in the Google ecosystem."

### Deeper version

"Gemini's distinctive technical advantages are native multimodality and context size. Native multimodal means the same model handles text, image, audio, and video without separate encoders, so mixed prompts work cleanly — combining a screenshot with a video and a text question in one call works coherently. The 2M context window allows loading entire codebases or hours of video in a single request, though lost-in-the-middle still applies.

The Gemini ecosystem has a consumer app, a developer API via AI Studio, Vertex AI for enterprise, Gemini CLI as a coding agent, Gemini Code Assist for IDEs, and Workspace integration. In enterprise, Vertex AI is the default choice for data residency and IAM integration — real enablers when dealing with regulated data.

Where Gemini actually deploys best in 2026: multimodal features where text-only LLMs can't compete, and high-volume classification where Gemini Flash-Lite's pricing makes a measurable difference. Everything else — interactive coding, agents, deep reasoning — Claude or specialized options typically lead. Benchmark on real data, not benchmarks."

### Talking points

- "Gemini's native multimodal is a real architectural advantage, not marketing."
- "Flash is surprisingly competitive on cost. Worth benchmarking against Haiku and 4o-mini for any workload."
- "Vertex AI matters in enterprise — data residency and IAM are real."
- "2M tokens is nice but lost-in-the-middle is still lost-in-the-middle."
- "Grounding with Google Search reduces hallucination on current events, but validate for critical decisions."

### Key vocabulary

- multimodal → multimodal
- ancoragem → grounding
- raio-x / imagem → image / x-ray
- residência de dados → data residency
- governança → governance
- tempo real → real-time
- latência sub-segundo → sub-second latency
- janela de contexto → context window
- orçamento de tokens → token budget

## Recursos

### Oficial

- [Gemini API Docs](https://ai.google.dev/gemini-api/docs)
- [Google AI Studio](https://aistudio.google.com/)
- [Vertex AI docs](https://cloud.google.com/vertex-ai/docs)
- [Gemini CLI](https://github.com/google/generative-ai-cli) — CLI oficial
- [Gemini Code Assist](https://cloud.google.com/products/gemini/code-assist)
- [Gemini models reference](https://ai.google.dev/gemini-api/docs/models/gemini)

### Tutoriais

- [Gemini Cookbook](https://github.com/google-gemini/cookbook)
- [Grounding with Google Search](https://ai.google.dev/gemini-api/docs/grounding)
- [Long context guide](https://ai.google.dev/gemini-api/docs/long-context)
- [Multimodal guide](https://ai.google.dev/gemini-api/docs/vision)

### Comparativos

- [LMSYS Leaderboard](https://chat.lmsys.org/) — leaderboard público
- [Artificial Analysis](https://artificialanalysis.ai/) — benchmarks independentes

## Deep dives — Gemini research, multimodal, enterprise

### Multimodal nativo — como é diferente

Modelos como GPT-4 começaram text-only e tiveram image encoders adicionados depois. Gemini foi treinado desde o pretraining com todos os modos — texto, imagem, áudio, vídeo — compartilhando o mesmo espaço de tokens.

**Consequências práticas:**

- **Cross-modal reasoning:** o modelo pode raciocinar "juntando" info de imagem e texto organicamente.
- **Video understanding:** Gemini processa sequências de frames com contexto temporal, não só frames isolados.
- **Audio transcription em contexto:** áudio é transcrito considerando contexto textual disponível (exemplo: ambíguidades são resolvidas usando o contexto da conversa).

**Onde vale benchmark:** se seu use case precisa de cross-modal, Gemini frequentemente domina. Text-only, Claude ou GPT costumam equiparar ou superar.

### Context window 2M — o que funciona e não funciona

2M tokens é muito. Na prática:

**Funciona bem:**

- Carregar codebases médias inteiras para análise.
- Processar 1-2 horas de vídeo.
- Múltiplos documentos em uma chamada para comparação lado-a-lado.

**Não funciona tão bem:**

- Lost-in-the-middle ainda é real em contextos > 300K.
- Latência aumenta muito.
- Custo por chamada pode ser significativo.
- Muitos use cases ainda prefere RAG com 8-16K de contexto filtrado.

**Regra prática:** use o context window grande para casos onde raciocínio cross-document é essencial; RAG para o resto.

### Grounding com Google Search

Feature única do Gemini: habilitar uma "tool" de Google Search que o modelo invoca durante a geração, retornando resposta com citações de URLs.

```python
response = client.generate_content(
    model="gemini-2.5-pro",
    contents="Qual a última versão do React e breaking changes?",
    tools=[{"google_search": {}}]
)
# resposta cita URLs Web
```

**Quando usar:**

- Informação que muda (notícias, versões, preços).
- Research com citação obrigatória.
- QA que exige fonte verificável.

**Limitações:**

- Qualidade depende do ranking do Google.
- Custo adicional.
- Latência maior (espera pela busca).
- Não é substituto de RAG sobre dados privados.

### Live API — voice + video em tempo real

Gemini Live é API de streaming bidirecional com suporte a áudio e vídeo em tempo real. Latência sub-segundo. Usado em Gemini app mobile para "conversa com o câmera".

**Arquitetura:**

- WebSocket bidirecional.
- Client envia áudio/vídeo chunks.
- Server envia text/audio responses em stream.
- Modelo processa tudo no mesmo contexto multimodal.

**Use cases:**

- Assistentes de câmera (descrever o que vê).
- Conversas naturais por voz.
- Tutor com compreensão visual.

### Vertex AI — o caminho enterprise

Vertex AI é a plataforma GCP para ML/AI em produção. Para Gemini, adiciona:

- **Data residency:** rodar em região específica (crítico para LGPD/GDPR).
- **Private endpoints:** tráfego não sai da VPC.
- **IAM GCP:** permissions granulares via Google Cloud.
- **Audit logs:** centralizados em Cloud Logging.
- **SLA empresarial:** uptime garantido.
- **Model Garden:** catálogo com Gemini + Claude (via parceria) + Llama + outros.
- **Committed Use Discounts:** descontos por compromisso.

Para empresas reguladas (saúde, finance), Vertex é frequentemente obrigatório, não opcional.

## Casos comuns no mercado

Padrões frequentes em times usando Gemini em produção. Não são casos vividos pessoalmente — são armadilhas recorrentes documentadas em post-mortems, talks, e literatura técnica.

### Caso 1 — Multimodal vs text-only benchmarking

**Padrão observado:** feature que combina imagem + texto (ex: análise de exames com laudo textual, descrição de UI a partir de screenshot, OCR + raciocínio). Benchmark típico em 3 opções:

- **Claude Sonnet + Vision:** qualidade decente, mas trata imagem como input "isolado".
- **GPT-4o:** similar a Claude, variabilidade alta.
- **Gemini 2.5 Pro:** qualidade superior por raciocínio cross-modal nativo.

Para casos regulados, decisão tipicamente vai para Gemini via Vertex AI (data residency).

**Lição:** para cross-modal, Gemini é default. Mas benchmark no caso específico.

### Caso 2 — Custo Flash vs Haiku para classificação

**Padrão observado:** feature de triagem rodando com Claude Haiku. Benchmark com Gemini Flash mostra:

- Acurácia no golden set quase idêntica (diferença < 1%).
- Latência tipicamente ~20% menor.
- Custo 2-3x menor.

Migração trivial, economia significativa. Edge cases ambíguos podem continuar em Haiku.

**Lição:** Flash é extremamente competitivo em custo. Vale benchmark lado-a-lado.

### Caso 3 — 2M context "funcionou" mas custou caro

**Padrão observado:** time tenta análise de documento longo (~400K tokens) jogando no contexto do Gemini Pro. Funciona — modelo extrai insights. Mas:

- Latência: ~45s por chamada.
- Custo: ~$2.50 por chamada.
- Qualidade: boa, mas context rot detectável em detalhes do meio.

Migração para RAG com chunking semântico tipicamente: latência → ~3s, custo → ~$0.15, qualidade subjetivamente melhor.

**Lição:** 2M é capability, não sempre a solução. RAG quase sempre bate.

### Caso 4 — Grounding retornando info errada

**Padrão observado:** feature de Q&A sobre informações que mudam (versões, guidelines, notícias) usando Gemini + Google Search grounding. Em alguns casos, retorna info de fontes não-confiáveis (blogs vs fontes oficiais/papers).

**Fix típico:**

- Filter de sources por domínio (só domínios confiáveis).
- Validação humana para decisões críticas.
- Fallback para RAG sobre fontes curadas.

**Lição:** grounding é útil mas precisa de validação. Google Search não garante qualidade de fonte.

### Caso 5 — Vertex AI vs API direta — confusion

**Padrão observado:** time inicialmente usa API direta do Gemini. Migra para Vertex AI por compliance. Descobre que pricing, quotas e features variam entre os dois. Prompt caching se comporta diferente. Re-ajuste leva semanas.

**Fix típico:**

- Escolher Vertex desde dia 1 se compliance é requisito.
- Documentação clara da stack para novos devs.

**Lição:** Vertex e API direta não são drop-in replacements. Planejar a escolha.

## Exercícios hands-on

### Lab 1 — Multimodal em problema real

1. Escolha problema que envolve imagem + texto (análise de screenshot UI, OCR + raciocínio).
2. Implemente com Gemini 2.5 Pro via AI Studio.
3. Compare com Claude Sonnet (vision).
4. Golden set + métricas.

### Lab 2 — Long context experiment

1. Base de documentos de ~500K tokens.
2. Tente RAG normal com Gemini Flash.
3. Tente jogar tudo no contexto (Gemini Pro).
4. Compare: latência, custo, qualidade no golden set.

### Lab 3 — Grounding para Q&A

1. Construa Q&A sobre informações que mudam (tech news, versões).
2. Habilite Google Search grounding.
3. Teste com perguntas reais.
4. Meça precisão e qualidade de fontes.

### Lab 4 — Gemini CLI em workflow real

1. Instale Gemini CLI.
2. Use em projeto por 1 semana.
3. Compare com Claude Code.
4. Documente diferenças de UX.

### Lab 5 — Vertex AI enterprise setup

1. Configure projeto GCP com Vertex AI.
2. Habilite Gemini.
3. Restrinja região (ex: southamerica-east1).
4. Configure IAM granular.
5. Audit log setup.
6. Deploy simples usando o endpoint.

## Veja também

- [[Anatomia dos LLMs|LLMs]]
- [[Context Engineering]]
- [[Anatomia de Agents|Agents]]
- [[Claude]]
- [[GitHub Copilot]]
- [[Codex]]
- [[Comparativo de LLMs]]
- [[03-Dominios/Tecnologia/IA/index|Inteligência Artificial]]
- [[MCP]]
- [[RAG e Vector Databases]]
- [[Senda IA]]
