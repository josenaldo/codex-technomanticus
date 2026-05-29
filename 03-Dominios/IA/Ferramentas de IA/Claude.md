---
title: "Claude"
created: 2026-04-01
updated: 2026-04-11
type: concept
progress: backlog
status: evergreen
tags:
  - ia
  - llm
  - ferramentas
  - claude
publish: true
---

# Claude

> Claude é uma das três famílias de LLM dominantes em 2026 (junto com GPT e Gemini), com diferenciais técnicos concretos: qualidade de raciocínio em tarefas longas, [[Dicionário de IA#tool use|tool use]] consistente, contexto de 1M tokens com retenção razoável (não só "no benchmark"), Claude Agent SDK limpo, e ecossistema maduro de [[Dicionário de IA#MCP (Model Context Protocol)|MCP]], skills e [[Dicionário de IA#subagent|subagents]]. Para muitos workloads de coding e agents, é a escolha default em times sérios. Esta nota é a trilha completa: modelos, API, ferramentas (Claude Code, Desktop, web), como operar em produção, e como adotar progressivamente. Para fundamentos de LLMs em geral ver [[Anatomia dos LLMs|LLMs]]; para comparação com outros modelos ver [[Comparativo de LLMs]].

## O que é

**Claude** é a família de [[Dicionário de IA#LLM (Large Language Model)|Large Language Models]] da **Anthropic** — empresa fundada em 2021 por ex-pesquisadores da OpenAI (Dario e Daniela Amodei entre os fundadores). Anthropic se posiciona como "AI safety company": treina modelos com foco em **Constitutional AI** (alinhamento via princípios escritos) e investe pesado em evaluation, red-teaming e research sobre comportamento de LLMs.

Em 2026, Claude é reconhecido como um dos top 2-3 LLMs no mundo, especialmente forte em:

- **Raciocínio complexo** e seguir instruções longas
- **Código** — escrita, review, refactor, debugging
- **Contexto longo** — processar codebases inteiras, livros, contratos
- **Tool use** — chamar funções com inputs corretos
- **Honestidade** — admitir não saber, evitar [[Dicionário de IA#Hallucination|alucinação]]
- **Safety** — recusar requisições prejudiciais sem ser chato

O ecossistema Claude em 2026 tem cinco superfícies principais:

1. **Claude.ai** — interface web e mobile para conversar.
2. **Claude API (Messages)** — integração programática.
3. **Claude Code** — CLI/IDE para coding assistido.
4. **Claude Desktop** — app desktop com MCP nativo.
5. **Claude Agent SDK** — framework para construir agents próprios.

## O que diferencia um senior usando Claude

1. **Escolhe o modelo certo por task** (Opus para complexo, Sonnet para diário, Haiku para bulk).
2. **Usa [[Dicionário de IA#Prompt caching|prompt caching]] em system prompts grandes** — economia típica de 50-90%.
3. **Pin versioning em produção** (`claude-sonnet-4-6-20260315`), não alias.
4. **Extended thinking conscientemente** — sabe quando o overhead vale a pena.
5. **Tool use com schemas rigorosos** e fallback para re-ask em erro.
6. **Claude Code com CLAUDE.md bem feito** e skills customizadas por projeto.
7. **MCP servers locais** (filesystem, git, postgres) configurados no Claude Desktop.
8. **Mede custo por feature** via console da Anthropic ou [[Dicionário de IA#Langfuse|Langfuse]].
9. **Conhece guardrails:** constitutional AI, trust & safety, refuse patterns.
10. **Usa Agent SDK para automação complexa**, não reinventa a roda com LangChain.

## Modelos Claude — família 4 e 4.6

Em 2026 (abril), a família ativa é **Claude 4.x**, com atualizações incrementais ("4.5", "4.6") trazendo melhorias sem major version bump. A hierarquia clássica permanece:

| Modelo | Força | Context | Velocidade | Custo (input/output por 1M tokens) | Use case |
| --- | --- | --- | --- | --- | --- |
| **Claude Opus 4.x** | Mais capaz, raciocínio profundo | 1M tokens | Lento | ~$15 / $75 | Arquitetura, análise densa, coding complexo |
| **Claude Sonnet 4.6** | Equilíbrio capacidade/custo | 1M tokens | Rápido | ~$3 / $15 | Coding diário, code review, chatbots |
| **Claude Haiku 4.5** | Rápido e barato | 200K tokens | Muito rápido | ~$0.80 / $4 | Classificação, extração, triagem |

**Convenção de nomes:** `claude-{family}-{tier}-{YYYYMMDD}` para versões pinadas, ou alias (`claude-sonnet-4-6`) para "last stable".

### Quando usar qual

**Opus** — quando a tarefa exige:

- Raciocínio em várias etapas com decisões sutis.
- Design de arquitetura, refactor grande, migração.
- Análise densa de textos longos (contratos, codebases).
- Debugging de problemas não-triviais.
- Situações onde errar custa mais que o token.

**Sonnet** — default para 90% das tasks:

- Coding assistido no dia a dia.
- Code review automatizado.
- Chatbots e assistentes em produção.
- Sumarização, extração estruturada.
- Tool use em agents.

**Haiku** — otimização de custo/latência:

- Classificação em volume (triagem de tickets, moderação).
- Extração em batch.
- Pré-filtragem antes de escalar para Sonnet/Opus.
- Respostas curtas em apps de alto tráfego.

**Padrão real de produção:** tiering. Haiku faz triagem/classificação → se confiança < 0.85 escala para Sonnet → se Sonnet ainda indeciso escala para Opus. Reduz custo em 5-10x sem perda de qualidade em produção.

### Extended Thinking

Claude 4.x tem **extended thinking mode**: o modelo produz um "bloco de raciocínio" privado antes da resposta final, similar ao o1/o3 da OpenAI mas mais transparente (você recebe os tokens de thinking na resposta, mesmo não enviando ao usuário).

```python
response = client.messages.create(
    model="claude-opus-4-6",
    max_tokens=8000,
    thinking={"type": "enabled", "budget_tokens": 10000},
    messages=[{"role": "user", "content": "Analyze this legal contract..."}]
)
# response.content contains both thinking blocks and text blocks
```

**Quando usar:**

- Problemas de raciocínio matemático/lógico.
- Trade-offs de design complexos.
- Análise de código longo.
- Tasks onde "pensar antes" claramente ajuda.

**Quando NÃO usar:**

- Tarefas curtas e diretas (desperdício).
- Tasks de formato estruturado (thinking pode ser ruído).
- Custos sensíveis (tokens de thinking são cobrados).

## Claude API — a Messages API

### Estrutura básica

```python
from anthropic import Anthropic

client = Anthropic()  # ANTHROPIC_API_KEY env var

response = client.messages.create(
    model="claude-sonnet-4-6",
    max_tokens=1024,
    system="You are a concise senior Python developer.",
    messages=[
        {"role": "user", "content": "Explique generators vs iterators"}
    ]
)
print(response.content[0].text)
```

### Parâmetros importantes

- **`model`** — sempre pin em produção
- **`max_tokens`** — teto de output; sempre defina
- **`system`** — string ou lista (para caching)
- **`messages`** — user/assistant alternados, primeiro sempre user
- **`temperature`** — 0-1, default 1.0 (não recomendado)
- **`top_p`** — use no lugar de temperature para estabilidade
- **`stop_sequences`** — sequências que param a geração
- **`stream`** — SSE para tokens em streaming
- **`tools`** — tool use / function calling
- **`tool_choice`** — `auto`, `any`, força uma específica
- **`thinking`** — extended thinking config
- **`metadata`** — user_id, etc para audit/debugging

### Streaming

```python
with client.messages.stream(
    model="claude-sonnet-4-6",
    max_tokens=2048,
    messages=[{"role": "user", "content": "Write an essay about..."}]
) as stream:
    for text in stream.text_stream:
        print(text, end="", flush=True)
    # Acesso à resposta completa:
    final = stream.get_final_message()
```

Streaming é obrigatório para UX conversacional (chat) e recomendado para respostas longas (latência percebida).

### Tool use

O padrão-ouro para tool calling. Claude é particularmente bom em escolher a ferramenta certa e formatar inputs corretamente.

```python
tools = [{
    "name": "get_weather",
    "description": "Get current weather for a city. Use when user asks about weather, temperature, or forecast.",
    "input_schema": {
        "type": "object",
        "properties": {
            "city": {"type": "string", "description": "City name"},
            "units": {"type": "string", "enum": ["celsius", "fahrenheit"], "default": "celsius"}
        },
        "required": ["city"]
    }
}]

response = client.messages.create(
    model="claude-sonnet-4-6",
    max_tokens=1024,
    tools=tools,
    messages=[{"role": "user", "content": "Como está o tempo em SP hoje?"}]
)

# response.stop_reason == "tool_use"
# response.content contém blocos de tipo "tool_use" com name + input
```

**Tool choice options:**

- `{"type": "auto"}` — modelo decide se usa tool
- `{"type": "any"}` — força usar alguma tool
- `{"type": "tool", "name": "X"}` — força tool específica (útil para structured outputs)

### Prompt caching — a otimização essencial

Anthropic suporta caching de partes do prompt. Você marca blocos com `cache_control: ephemeral`, e chamadas subsequentes com o mesmo prefixo têm **~90% desconto** no custo desses tokens e latência muito menor.

```python
response = client.messages.create(
    model="claude-sonnet-4-6",
    max_tokens=1024,
    system=[
        {
            "type": "text",
            "text": HUGE_INSTRUCTIONS  # 5000+ tokens de system prompt
        },
        {
            "type": "text",
            "text": FEW_SHOT_EXAMPLES,  # Few-shot examples estáticos
            "cache_control": {"type": "ephemeral"}
        }
    ],
    messages=[{"role": "user", "content": user_input}]
)
```

Regras importantes:

- **Cache tem TTL** de ~5 minutos; uso recente renova.
- **Mínimo 1024 tokens** para cache valer.
- **Até 4 blocos cacheados** por request.
- **Ordenação estável** — cache funciona por prefixo exato.

**Impacto típico:** caching de system prompt de 4-5K tokens em workload recorrente reduz custo da feature em ~80-90% e TTFT em ~30-40%. ROI imediato em qualquer caso com system prompt grande chamado com frequência.

### Structured outputs via tool use

Claude não tem "JSON mode" explícito, mas tool use forçado tem função análoga e é mais flexível.

```python
tools = [{
    "name": "classify_ticket",
    "description": "Classify a support ticket",
    "input_schema": {
        "type": "object",
        "properties": {
            "category": {"type": "string", "enum": ["bug", "feature", "question"]},
            "priority": {"type": "string", "enum": ["low", "medium", "high", "critical"]},
            "confidence": {"type": "number", "minimum": 0, "maximum": 1},
            "reasoning": {"type": "string"}
        },
        "required": ["category", "priority", "confidence", "reasoning"]
    }
}]

response = client.messages.create(
    model="claude-sonnet-4-6",
    max_tokens=1024,
    tools=tools,
    tool_choice={"type": "tool", "name": "classify_ticket"},
    messages=[{"role": "user", "content": ticket_text}]
)

# Extração garantida do JSON validado
result = response.content[0].input  # dict com category, priority, etc.
```

Benefícios:

- Schema validado no servidor.
- Saída estruturada e parseável.
- Integra com Pydantic/Zod para validação local extra.

### Batch API

Para tasks não-urgentes em volume, [[Dicionário de IA#batch API|Batch API]] processa até 50% mais barato com latência de minutos a horas.

```python
batch = client.messages.batches.create(
    requests=[
        {
            "custom_id": f"doc-{i}",
            "params": {
                "model": "claude-haiku-4-5",
                "max_tokens": 500,
                "messages": [{"role": "user", "content": doc}]
            }
        }
        for i, doc in enumerate(documents)
    ]
)
# Polling até batch.status == "ended"
```

Use cases: processamento offline, geração de embeddings de base, sumarização em massa.

## Claude Code — o coding agent

**Claude Code** é um CLI/IDE assistant oficial da Anthropic. Interativo, lê/edita arquivos locais, roda comandos, faz commits, tudo guiado por conversa em linguagem natural.

### Por que Claude Code

- **Interação nativa com Claude Opus/Sonnet** — sem intermediário.
- **MCP nativo** — conecta filesystem, git, postgres, github etc.
- **Skills customizáveis** via `.claude/skills/` e `~/.claude/skills/`.
- **CLAUDE.md** do projeto como contexto permanente.
- **Sub-agents** para workflows complexos.
- **Hooks** que executam comandos em eventos (pre/post tool use).
- **Worktrees** para isolar mudanças.
- **Memory persistente** via `memory/` do projeto.
- **Integrações IDE** (VS Code, JetBrains via plugins).

### Workflow típico

```text
$ claude
> Refatore o módulo auth/ para usar JWT em vez de session cookies.
  Mantenha backwards compatibility por 1 release.
```

Claude:

1. Lê estrutura do projeto (via CLAUDE.md e filesystem).
2. Explora módulo auth atual.
3. Propõe plano em markdown.
4. **Espera confirmação** antes de tocar código.
5. Executa em stages, commitando progresso.
6. Roda testes após cada mudança.
7. Reporta resultado final.

### CLAUDE.md — a alavanca principal

Arquivo markdown na raiz do projeto que o Claude Code lê automaticamente. Define:

- Arquitetura e módulos principais
- Convenções de código
- Comandos essenciais (test, build, lint, deploy)
- Antipatterns a evitar
- Patterns a seguir
- Como rodar testes
- Deploy process

**Uma boa CLAUDE.md é o maior ROI que se pode ter com Claude Code.** O padrão que funciona: reservar 1-2h no início de um projeto para escrever bem, e iterar regularmente quando comportamentos ruins aparecerem.

Exemplo esquelético:

```markdown
# Projeto X

## Stack
- Backend: Node.js + TypeScript + Fastify + Prisma (PostgreSQL)
- Frontend: Next.js 15 + React 19 + Tailwind + shadcn/ui
- Testes: Vitest (unit) + Playwright (e2e)

## Estrutura
- `src/app/` — Next.js app router
- `src/api/` — rotas Fastify
- `src/lib/` — utilitários e integrações
- `src/db/` — schemas Prisma + migrations

## Convenções
- TypeScript strict, sem `any`
- Zod para validação em todas as bordas
- Error handling via Result<T, E> pattern
- Nunca fazer commit direto em main

## Comandos
- `pnpm dev` — roda dev server
- `pnpm test` — unit tests
- `pnpm test:e2e` — end-to-end
- `pnpm lint` — eslint + prettier

## Antipatterns
- Nunca console.log em código de produção (use logger)
- Nunca catch sem log ou rethrow
- Nunca alterar migration já aplicada
```

### Skills em Claude Code

Skills são pacotes de instruções reutilizáveis. Ver [[Context Engineering]] para conceito. No Claude Code:

```text
.claude/skills/
├── code-review/SKILL.md
├── write-tests/SKILL.md
├── refactor/SKILL.md
└── debug/SKILL.md

~/.claude/skills/  # skills globais do usuário
├── commit/SKILL.md
└── brainstorming/SKILL.md
```

Cada `SKILL.md` tem frontmatter com `name` e `description`. Claude carrega descrições como menu e o conteúdo completo quando decide usar.

### Sub-agents

Claude Code suporta sub-agents: agents especializados invocados pelo agent principal. Útil para tasks paralelas ou que precisam de contexto isolado.

Exemplos comuns:

- **Explorer** (Haiku) — explora codebase rapidamente
- **Planner** (Opus) — propõe arquitetura
- **Implementer** (Sonnet) — escreve código
- **Reviewer** (Opus) — revisa antes de commit

### Hooks

Configure comandos que executam em eventos do Claude Code:

- `PostToolUse:Write` — rodar linter ao escrever arquivo
- `PreToolUse:Bash` — validar comando antes de executar
- `SessionStart` — carregar contexto customizado

Via `settings.json`:

```json
{
  "hooks": {
    "PostToolUse": {
      "Write": "prettier --write $CLAUDE_FILE"
    }
  }
}
```

### Instalação

```bash
# Via Anthropic
curl -fsSL https://claude.ai/install.sh | bash

# Via brew
brew install anthropic/claude/claude

# Rodar
claude
```

### Fluxo típico — uma feature

Padrão de uso do Claude Code para feature não-trivial:

1. **Setup:** `cd` no projeto com CLAUDE.md atualizada.
2. **Brainstorming:** "Preciso adicionar notificações via email para eventos X. Explora o código atual de email e proponha abordagem".
3. **Plano em markdown:** Claude escreve plano. Humano revisa, ajusta.
4. **Execução em stages:** "Execute stage 1 do plano, commite, espere."
5. **Validação:** humano roda testes, revisa diff.
6. **Iteração:** "Ajuste X, Y."
7. **Final review:** skill customizada `/review` antes do PR.

Boa prática: nunca deixar Claude rodar mais de 15-20 minutos sem checkpoint humano. É onde as coisas dão errado.

## Claude Desktop — o hub local

App desktop (macOS, Windows) para conversar com Claude fora do browser. Diferenciais:

- **MCP nativo:** configura servers em `claude_desktop_config.json`.
- **Attachments:** arquivos, imagens, PDFs.
- **Artifacts:** geração de HTML, React, markdown, SVG inline.
- **Projects:** organiza conversas e contexto por projeto.
- **Operator mode** (em alguns pacotes): controla browser/computador com supervisão.

Uso típico: tarefas que não são coding (research, writing, análise) onde quero contexto persistente de um projeto + acesso a filesystem/DB via MCP.

## Claude.ai — a interface web

- Disponível gratuito com limites e pagos (Pro, Max, Team, Enterprise).
- Projects, memory, artifacts.
- Computer use (em Max/Enterprise).
- Mobile app (iOS/Android).

Para devs, mais útil como fallback ou para sharing rápido de conversas. Para trabalho sério, API + Claude Code.

## Claude Agent SDK

Framework oficial para construir agents customizados com Claude. Alternativa a LangChain quando você quer integração nativa e menos abstrações.

```python
from claude_agent_sdk import Agent, Tool

agent = Agent(
    model="claude-sonnet-4-6",
    system="You are a research agent...",
    tools=[
        Tool(name="web_search", ...),
        Tool(name="read_url", ...)
    ],
    max_steps=15
)

result = agent.run("Research recent papers on context engineering")
```

Vantagens:

- Integração nativa com Anthropic API.
- Suporte nativo a MCP (conecta servers sem código extra).
- Observabilidade built-in.
- Sub-agents e parallel execution.

[Docs do Claude Agent SDK](https://docs.anthropic.com/en/docs/agents).

## Diferenciais técnicos de Claude

### 1. Context window 1M que funciona

Opus/Sonnet 4.x têm 1M tokens. Diferente de outros fornecedores, Anthropic tem publicado benchmarks mostrando boa retenção ao longo do contexto, não só "raw window". Isso destrava uso como: carregar codebase inteira, processar livro inteiro, análise de todo histórico de prontuário.

**Mas atenção:** ainda há context rot acima de ~200K em tasks difíceis. Não confie cegamente. Teste seu caso.

### 2. Constitutional AI e safety

Claude é treinado com Constitutional AI — um conjunto de princípios escritos que guia o próprio modelo a auto-avaliar respostas durante RLHF. Resultado:

- Recusa de requisições danosas com explicação clara.
- Menos bajulação que GPT em muitos benchmarks.
- Mais consistente em admitir não saber.
- Menos suscetível a jailbreaks simples (mas não imune).

**Trade-off:** ocasionalmente recusa tasks legítimas por excesso de cautela. System prompt claro sobre contexto resolve 95% dos casos.

### 3. Tool use de alta qualidade

Claude consistentemente escolhe tools corretamente e formata inputs em JSON válido. Anthropic investiu pesado em RLHF específico para tool use. Em benchmarks, Claude lidera ou empata com GPT-4 em tool calling.

### 4. Extended Thinking transparente

Diferente do o1 da OpenAI (que esconde thinking), Claude expõe os tokens de raciocínio. Você pode:

- Ler o pensamento do modelo (debugging, confiança).
- Decidir mostrar ao usuário ou não.
- Medir custo de thinking separadamente.

### 5. MCP nativo

Anthropic criou MCP. Claude Desktop, Claude Code e Agent SDK suportam nativamente. É onde o protocolo tem integração mais madura.

### 6. Artifacts

Na interface web e Desktop, Claude pode gerar "artifacts" — documentos, código, React components, SVG, markdown — renderizados e editáveis ao vivo na UI. Útil para prototipagem rápida.

## Quando NÃO usar Claude

- **Multimodal com áudio/vídeo nativo:** Gemini ou GPT-4o.
- **Geração de imagem:** DALL-E, Midjourney, Stable Diffusion.
- **Máximo de velocidade em cada chamada:** Haiku é rápido mas Gemini Flash ainda é mais.
- **Integração específica com Azure/Microsoft:** GPT-4 via Azure OpenAI.
- **Budget muito apertado em alta escala:** Haiku é competitivo, mas para tarefas muito simples modelos menores open-source podem ser mais baratos self-host.

## Armadilhas comuns

### 1. Usar alias em produção

`claude-sonnet-4-6` vs `claude-sonnet-4-6-20260315`. Alias muda quando Anthropic atualiza. **Fix:** pin version em produção.

### 2. Não usar prompt caching

System prompts grandes em toda chamada = dinheiro na mesa. **Fix:** marcar com `cache_control`.

### 3. Tool descriptions vagas

"search — searches" → modelo não sabe quando usar. **Fix:** descrição clara + when-to-use.

### 4. Ignorar refuse patterns

Prompt sem contexto → Claude recusa tasks legítimas. **Fix:** system prompt explicando contexto profissional.

### 5. CLAUDE.md desatualizada

Projeto mudou, CLAUDE.md não. Claude trabalha com info errada. **Fix:** revisar CLAUDE.md mensalmente ou após refactor grande.

### 6. Extended thinking em tudo

Thinking em tasks simples = custo desnecessário. **Fix:** só onde claramente ajuda.

### 7. Context dump sem RAG

"Vou jogar 500K tokens e deixar Claude virar." Context rot real, custo alto. **Fix:** RAG filtrado.

### 8. Sem observabilidade

Anthropic console mostra uso geral mas não por feature. **Fix:** Langfuse ou metadata `user_id` + análise.

### 9. Claude Code sem max_steps

Agent entra em loop. **Fix:** sempre configure limites; revise diff antes de commitar.

### 10. MCP servers community sem review

Malicioso ou buggy. **Fix:** review antes de instalar; least privilege.

## Como ganhar experiência prática

Esta nota é estrutura sobre Claude. Para internalizar, prática é insubstituível. Três caminhos curados:

### Caminho 1 — Claude Code no Codex Technomanticus (1 semana)

Adotar Claude Code como ferramenta principal para gerenciar este próprio vault Obsidian:

- Escrever uma `CLAUDE.md` na raiz do vault descrevendo: estrutura de pastas, convenções de notas (frontmatter, MOCs), workflow de publicação Quartz, antipatterns
- Pedir Claude Code para tarefas reais: "limpar inbox", "criar nova nota X usando template Y", "encontrar notas relacionadas a Z"
- Iterar a CLAUDE.md baseado em onde Claude erra

**Critério de sucesso:** consegue manter o vault com Claude Code de forma confortável; tem opinião própria sobre o que vai e o que não vai na CLAUDE.md.

### Caminho 2 — Feature LLM com Claude API + caching (2 semanas)

Construir feature pequena que use Anthropic API direto, exercitando os diferenciais do Claude:

- **Opção A:** classificador de notas com structured output via tool use forçado
- **Opção B:** sumário de PRs de um repo seu, com prompt caching no system prompt
- **Opção C:** review automático de notas Obsidian (qualidade, completude, links faltando)

Exercitar: pin version, prompt caching, structured output via tool use, retry com error feedback, observabilidade básica.

**Critério de sucesso:** feature em produção pequena, com métricas (custo, latência, acurácia) e prompt cacheado funcionando.

### Caminho 3 — Claude Agent SDK em workflow profissional (quando aparecer)

Em projeto profissional com workflow agent automatizável (sumarização em batch, triagem, geração de relatórios), implementar com Claude Agent SDK + MCP servers customizados + observabilidade. Mais demorado, mas é o que vira "agent em produção" no CV.

**Critério de sucesso:** entrega no projeto com métricas, não estudo paralelo.

---

**Sugestão de ordem:** Caminho 1 → Caminho 2 → Caminho 3.

## How to explain in English

### Elevator pitch

"Claude is one of the top three LLM families in 2026 alongside GPT and Gemini. Where it leads: reasoning on long tasks, tool use consistency, and a 1M-token context that holds up in practice. The full ecosystem includes the Anthropic API, Claude Code as a coding agent, Claude Desktop with native MCP, and the Claude Agent SDK for custom agents. The highest-ROI configuration in a Claude Code project is a well-maintained CLAUDE.md."

### Deeper version

"Anthropic has three tiers: Opus for deep reasoning, Sonnet for daily work, Haiku for cheap/fast tasks. The default production posture is aggressive tiering — Haiku handles triage, Sonnet does the heavy lifting, Opus only gets invoked for cases Sonnet flags uncertain. This alone cuts costs 5-10x on many features.

API essentials that matter: prompt caching on any system prompt over 1K tokens (often 80% savings), tool use for structured outputs, streaming for user-facing features, and pinned model versions in production so silent provider updates don't blow up the golden set.

On the tooling side, Claude Code is the agent surface — filesystem, git, and MCP servers via tool use. What matters in practice: a well-maintained CLAUDE.md as project context, custom skills for recurring workflows, and sub-agents for tasks that benefit from context isolation. Production hardening includes max_steps, human-in-the-loop for destructive actions, and a review step before merging any agent-produced change."

### Talking points

- "Tier your models. Haiku for triage, Sonnet for daily, Opus for when it matters."
- "Prompt caching pays for itself on day one for any system prompt over a thousand tokens."
- "Pin model versions in production. Aliases move under you."
- "CLAUDE.md is the highest-leverage file in a Claude Code project."
- "MCP makes Claude integrate with anything, but audit every community server."

### Key vocabulary

- modelo → model
- contexto estendido → extended context
- raciocínio estendido → extended thinking
- cache de prompt → prompt caching
- versão fixada → pinned version
- chamada de ferramenta → tool use
- escolha de ferramenta → tool choice
- fluxo de trabalho → workflow
- custo por recurso → cost per feature
- nível de modelo → model tier

## Recursos

### Documentação oficial

- [Anthropic Docs](https://docs.anthropic.com/)
- [Messages API reference](https://docs.anthropic.com/en/api/messages)
- [Prompt caching](https://docs.anthropic.com/en/docs/build-with-claude/prompt-caching)
- [Extended thinking](https://docs.anthropic.com/en/docs/build-with-claude/extended-thinking)
- [Tool use](https://docs.anthropic.com/en/docs/build-with-claude/tool-use)
- [Claude Code docs](https://docs.anthropic.com/en/docs/claude-code)
- [Claude Agent SDK](https://docs.anthropic.com/en/docs/agents)
- [MCP docs](https://modelcontextprotocol.io/)

### Prompting e engineering

- [Anthropic Prompting Guide](https://docs.anthropic.com/en/docs/build-with-claude/prompt-engineering/overview)
- [Effective Context Engineering](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents)
- [Building Effective Agents](https://www.anthropic.com/research/building-effective-agents)
- [Contextual Retrieval](https://www.anthropic.com/news/contextual-retrieval)

### Comunidade e exemplos

- [Anthropic Cookbook](https://github.com/anthropics/anthropic-cookbook)
- [Anthropic Skills](https://github.com/anthropics/skills)
- [Everything Claude Code](https://github.com/affaan-m/everything-claude-code)
- [Context Lens](https://github.com/TiagoSchr/context-lens)
- [Awesome MCP Servers](https://github.com/punkpeye/awesome-mcp-servers)

### Console e billing

- [Anthropic Console](https://console.anthropic.com/) — API keys, usage, billing
- [claude.ai](https://claude.ai/) — interface web

### Aprender

- [Anthropic Academy](https://www.anthropic.com/learn)
- [Claude Course (Alan Nichols)](https://www.youtube.com/watch?v=WLZqPonSrK0)

## Deep dives — Anthropic research e design decisions

### Constitutional AI — o paper que define o diferencial Claude

[Constitutional AI: Harmlessness from AI Feedback](https://arxiv.org/abs/2212.08073) (Bai et al., 2022) é a técnica de alinhamento que distingue Claude. Em vez de depender puramente de RLHF com humanos, Constitutional AI usa um conjunto escrito de princípios ("constitution") para o próprio modelo criticar e refinar suas respostas.

**Processo:**

1. **Supervised Learning phase:** modelo gera resposta, critica baseado em principles, revisa.
2. **RLAIF (RL from AI Feedback):** modelo pontua respostas alternativas baseado em principles.
3. **Training:** usa esses pontos como reward.

**Vantagens:**

- Escala melhor que RLHF puro (não precisa de humanos para cada exemplo).
- Princípios são explícitos e auditáveis.
- Modelo é mais consistente em recusas e menos "bajulador".

**Na prática:** explica por que Claude às vezes parece "mais principiado" e por que responde "não sei" com mais frequência do que GPT.

### Claude's Extended Thinking (Interpretable Reasoning)

Claude 4+ introduziu extended thinking mode onde o modelo produz tokens de raciocínio visíveis antes da resposta final. Diferente de o1 da OpenAI (que esconde thinking), Claude expõe.

**Por que expor importa:**

- **Auditabilidade:** você pode ver o que levou à resposta.
- **Debugging:** quando erra, você sabe onde.
- **Confiança calibrada:** thinking revela incerteza.
- **Research:** Anthropic publica pesquisa sobre interpretability usando esses tokens.

**Trade-off:** tokens de thinking são cobrados. Use budget explícito.

### MCP — o protocol criado pela Anthropic

MCP (Model Context Protocol) foi criado pela Anthropic em 2024. Ver [[MCP]] para deep dive. Pontos relevantes para Claude especificamente:

- **Claude Desktop foi o primeiro client**, oferece integração mais madura.
- **Claude Code suporta MCP nativamente** — servers aparecem como tools.
- **Claude Agent SDK facilita** conectar MCP servers custom sem código extra.
- **Ecossistema de MCP servers** é mais rico em torno de Claude.

### Claude Code arquitetura

Claude Code é construído sobre Claude Agent SDK e usa Claude Opus/Sonnet. Design decisions interessantes:

- **Filesystem access via tool use** (não via contexto dump). Modelo decide o que ler.
- **Session-based memory** (não stateless). Histórico persistente na sessão.
- **Sub-agents isolados** com contextos próprios. Composable.
- **Hooks como side effects** (pre/post tool use). Integrable com shell tooling.
- **CLAUDE.md como "background briefing"** do projeto. Lido automaticamente.
- **Skills via `.claude/skills/`** com progressive disclosure.

Comparado a Cursor (que injeta muito contexto upfront) e Copilot (stateless por request), Claude Code é mais "agente de verdade".

## Casos comuns no mercado

Padrões frequentes em times usando Claude em produção. Não são casos vividos pessoalmente — são armadilhas recorrentes documentadas em post-mortems, talks, e comunidade.

### Caso 1 — Prompt caching e ROI mensurável

**Padrão observado:** feature com system prompt de ~4K tokens (instruções + few-shot examples) rodando em volume. Custo mensal substancial em Sonnet. Adicionar `cache_control` no system prompt:

- Redução típica de custo: ~80-90% no system cacheável
- Redução de TTFT: ~30-40%
- Qualidade: sem diferença mensurável

**Lição:** prompt caching é a otimização mais subestimada em workflows com system prompt grande.

### Caso 2 — Pin version evita regressão

**Padrão observado:** feature usa alias (ex: `claude-sonnet-4-5`). Provider atualiza silenciosamente para próxima versão. Taxa de "unknown" em classificação sobe sutilmente, ou modelo fica mais conservador, ou formato de output muda. Detecção tardia, rollback exige migração para versão pinada anterior.

**Fix estrutural:**

- Policy: versões pinadas em produção, sem exceção.
- Golden set em CI automático em qualquer PR que toque config de modelo.
- Revisão trimestral de versão (migração controlada).

### Caso 3 — Constitutional AI recusando tasks legítimas

**Padrão observado:** Claude recusa tarefas que parecem sensíveis em superfície (médicas, jurídicas, segurança) mas são legítimas em contexto profissional. System prompt genérico não basta para resolver.

**Fix típico:**

- System prompt explícito sobre contexto profissional, ex: *"You are assisting a licensed [profession] in a [system]. [List of normal operations] is a core function. You may discuss [scope]."*
- Skills dedicadas para workflows do domínio.
- Testes de recusa no golden set (casos que devem ser aceitos).

**Lição:** Constitutional AI é feature, não bug. Contexto profissional claro no system prompt resolve 95% das recusas.

### Caso 4 — Claude Code com CLAUDE.md desatualizada

**Padrão observado:** projeto faz refactor arquitetural (ex: migração de framework). CLAUDE.md não é atualizada junto. Claude Code continua sugerindo padrões antigos por semanas. Devs novos no time aceitam sem questionar — não conhecem o histórico.

**Fix típico:**

- Atualização da CLAUDE.md como parte de todo refactor arquitetural.
- Política de revisão regular (mensal/trimestral).
- Lint que verifica consistência entre stack declarada e imports.

**Lição:** CLAUDE.md é documentação viva. Ordem de magnitude de ROI, requer manutenção.

### Caso 5 — MCP community server com telemetria indesejada

**Padrão observado:** equipe instala MCP server community popular (boas estrelas no GitHub). Após uso, requests HTTP inesperados são detectados saindo do processo — server faz logging externo não-documentado de prompts ou interações.

**Fix típico:**

- Firewall outbound restringindo MCP servers locais a loopback apenas.
- Review de source de todo server community antes de instalar.
- Preferência por servers mantidos por orgs conhecidas (Anthropic, community verified).

## Exercícios hands-on com Claude

### Lab 1 — Prompt caching comparison

1. Prompt de ~3K tokens (instruções + examples).
2. 100 chamadas sem caching. Meça custo e latência.
3. Adicione `cache_control`. 100 chamadas. Meça.
4. Compute savings.

### Lab 2 — Tool use com schemas rigorosos

1. Defina 3 tools com schemas Pydantic.
2. Test com inputs válidos e inválidos.
3. Observe como Claude lida com erros.
4. Adicione retry corretivo (passa erro de volta).

### Lab 3 — Extended thinking tradeoffs

1. Task: problema matemático complexo.
2. Rode sem thinking. Meça custo, latência, acurácia.
3. Rode com thinking budget=5K. Meça.
4. Rode com budget=20K. Meça.
5. Gráfico de trade-off.

### Lab 4 — CLAUDE.md bem feita

1. Projeto real que você trabalha.
2. Baseline: task não-trivial no Claude Code sem CLAUDE.md.
3. Escreva CLAUDE.md rica.
4. Re-rode. Compare qualidade.

### Lab 5 — MCP server custom

1. Escreva server Python ou TS com 3 tools do seu domínio.
2. Conecte ao Claude Desktop.
3. Use em workflow real por 1 semana.
4. Meça ganho vs trabalho manual.

### Lab 6 — Agent SDK

1. Construa agent com Claude Agent SDK.
2. Tools próprias + MCP server conectado.
3. Observabilidade via Langfuse.
4. Deploy simples (Railway, Fly).

## Veja também

- [[Anatomia dos LLMs|LLMs]] — fundamentos de LLMs
- [[Context Engineering]] — prompt/context engineering
- [[Anatomia de Agents|Agents]] — construção de agents
- [[RAG e Vector Databases]]
- [[MCP]] — protocolo criado pela Anthropic
- [[GitHub Copilot]]
- [[Codex]]
- [[Gemini]]
- [[Comparativo de LLMs]] — Claude vs alternativas
- [[03-Dominios/IA/index|Inteligência Artificial]]
- [[Senda IA]]
