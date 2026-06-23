---
title: "Estado da arte do harness engineering (junho 2026)"
created: 2026-06-19
updated: 2026-06-19
type: reference
status: growing
publish: false
tags:
  - pesquisa
  - harness-engineering
  - agentic-engineering
  - ia
  - dossie
---

# Estado da arte do harness engineering — dossiê de pesquisa (jun/2026)

> [!info] O que é este documento
> Lastro de uma pesquisa profunda (deep-research, 110 agentes, 27 fontes, 16 achados verificados adversarialmente) sobre as disciplinas emergentes em torno de agentes de codificação. Alimenta o enriquecimento dos galhos do domínio IA. **Cada achado foi votado por verificadores independentes** (formato `N-M`); 2 claims foram refutadas (0-3) e estão marcadas como NÃO-USAR.

## Síntese

Em junho de 2026 o campo consolidou o **harness** como uma terceira camada de engenharia — acima dos pesos (Weights Era) e do contexto (Context Era) — formalizada tanto na academia quanto na prática industrial (Anthropic). "Agentic engineering" emergiu como disciplina nomeada, com workshop dedicado no ICSE 2026. No tooling, MCP amadureceu, Agent Skills firmaram o progressive disclosure e o OpenTelemetry avançou convenções GenAI. **Consenso:** o harness importa e merece ser reportado. **Disputa aberta:** agente único generalista vs. multi-agente; e nenhuma das quatro taxonomias de harness venceu.

## Achados confirmados

### Harness como terceira camada
- **Progressão weights→context→harness** (survey arXiv:2604.08224, 9-abr-2026, 21 autores). Harness Era = "external memory stores, tool registries, protocol definitions, sandboxes, sub-agent orchestration, compression pipelines". Anthropic define o Claude Agent SDK como *"general-purpose agent harness"*. `[0]2-1 + [3]3-0`
- **Decomposição Memory/Skills/Protocols + Harness** (mesmo survey). Harness NÃO é uma 4ª externalização — é *"the runtime environment within which these forms operate"*, provendo orquestração/constraints/observabilidade/feedback. Mediadores: sandboxing, observability, compression, evaluation, approval loops, sub-agent orchestration. `[1]2-1`
- **6 dimensões analíticas** (survey §6.2): agent loop/control flow · sandboxing · human oversight/approval · observability/feedback · config/permissions/policy · context budget. `[2]3-0`

### Taxonomias concorrentes (nenhuma venceu)
- **11 aspectos** (NLAHs, Pan et al., arXiv:2603.25723, mar/2026): agent loops · tool design · context eng · filesystem · memory/state · validação/parada · safety/sandbox · runtime defaults · observability/replay · retry/recovery · budget. `[10]2-1`
- **CAR — Control/Agency/Runtime** (preprint 202603.1756, ~23-abr-2026). Audita 63 trabalhos; arco software→prompt→context→harness engineering. `[11]3-0 + [13]3-0`
- **Ganhos harness-sensitive + HarnessCard** (mesmo CAR): *"many reported agent gains may be partly harness-sensitive rather than purely model-driven"*; propõe reportar o harness junto ao modelo. `[12]3-0`

### Context / memory engineering
- **Context engineering = "natural progression of prompt engineering"** (Anthropic Applied AI, 29-set-2025; autores Rajasekaran/Dixon/Ryan/Hadfield). Curar o conjunto ótimo de tokens; gerencia todo o estado de contexto. `[18]3-0`
- **Context rot** (termo do Chroma Research, adotado pela Anthropic): atenção n² → "attention budget" finito; recall cai conforme tokens crescem. `[19]3-0`
- **Técnicas duráveis** (Anthropic): compaction (+ tool-result clearing no Claude Developer Platform) · structured note-taking/agentic memory (memory tool file-based, beta desde 29-set-2025) · sub-agentes p/ isolamento (retornam sumário de 1.000-2.000 tokens). `[20][21][22] 3-0`
- **Compaction é insuficiente p/ long-running**: precisa de artefatos duráveis — lista JSON de features (JSON > Markdown porque o modelo modifica menos), `claude-progress.txt`, histórico git inicial (Anthropic, 26-nov-2025; menciona "context anxiety" do Sonnet 4.5). `[4]3-0`

### Agentic engineering como disciplina
- **AGENT 2026** — workshop dedicado no ICSE 2026 (Rio, terça 14-abr-2026). Define como *"emerging discipline focused on the design, development, and operation of systems that exhibit goal-directed autonomy"*. Escopo: requirements, arquitetura, V&V, AgentOps, responsible AI, human-agent interaction. `[8][9]3-0`
- **Caso GitLab Orbit** (issue #163): 135K linhas Rust, ~95% gerado por IA, 4 pessoas, ~2 semanas, 259 MRs. Práticas: guardrails deliberados, agent context files (AGENTS.md/CLAUDE.md com sync por CI), custom skills, 15+ CI jobs — *"not ad hoc prompting"*. ⚠️ AUTO-REPORTADO, first-party, sem auditoria. `[6]2-1 + [7]3-0` (confiança: média)

### Loop / disputa
- **Single vs multi-agent: EM ABERTO** (Anthropic, fim 2025): *"still unclear whether a single, general-purpose coding agent performs best... or multi-agent."* Estudos: ganhos multi-agente ~4% a ~4x do custo. `[5]3-0`

### Tooling e protocolos 2026
- **MCP Tasks (SEP-1686)**: primitiva async experimental (call-now/fetch-later); roadmap 2026 mira gaps de lifecycle (retry semantics, expiry policies). `[14]3-0`
- **Agent Skills / progressive disclosure** em 3 níveis (metadata YAML no startup ~30-100 tokens → SKILL.md on-demand → arquivos só quando lidos), filesystem-based. Standard aberto 18-dez-2025. `[15][16]3-0`
- **OpenTelemetry GenAI semantic conventions**: experimentais; convenção de agentes em definição (não graduou p/ stable em jun/2026). `[17]3-0`

## NÃO USAR — claims refutadas (0-3)
- ❌ Que NLAHs (harness em linguagem natural) atingem **paridade** com código nativo em benchmarks de coding/terminal/computer-use. (Refutada — não afirmar paridade.)
- ❌ Que a convenção semântica de **aplicação** de agentes do OpenTelemetry foi **finalizada em 2025**. (Ainda experimental — usar "sendo definida".)

## Questões em aberto
1. Agente único vs. multi-agente em codebases reais — sem resolução empírica.
2. Qual taxonomia de harness consolidará o vocabulário (ou ficam como lentes complementares).
3. HarnessCard será adotado pela comunidade de evals?
4. Quando as convenções GenAI/agentes do OpenTelemetry graduarão p/ stable.
5. Falta padrão auditável p/ métricas de produtividade ("~95% IA" da GitLab).

## Fontes primárias
- arXiv:2604.08224 — *Externalization in LLM Agents* (survey)
- arXiv:2603.25723 — *Natural-Language Agent Harnesses*
- preprints.org 202603.1756 — *Harness Engineering for Language Agents (CAR)*
- anthropic.com/engineering/effective-harnesses-for-long-running-agents (nov/2025)
- anthropic.com/engineering/effective-context-engineering-for-ai-agents (set/2025)
- conf.researchr.org/home/icse-2026/agent-2026
- gitlab.com/gitlab-org/orbit/knowledge-graph/-/issues/163
- blog.modelcontextprotocol.io/posts/2026-mcp-roadmap/
- platform.claude.com/docs/.../agent-skills/best-practices
- opentelemetry.io/blog/2025/ai-agent-observability/
- simonwillison.net/2025/Nov/4/code-execution-with-mcp/

## Notas que este dossiê alimentou
- [[03-Dominios/Tecnologia/IA/Anatomia de Agents/11 - Harness engineering — a terceira camada]]
- [[03-Dominios/Tecnologia/IA/Claude Code/Mental Model/09 - O harness como terceira camada]]
- (+ enriquecimentos Tier 2 em Evaluation, Agentes de Codificação, MCP, Context Engineering, Improvement Loop)
