---
title: "Skills e instructions como contexto"
created: 2026-05-02
updated: 2026-05-02
type: concept
progress: backlog
status: seedling
publish: true
tags:
  - context-engineering
  - ia
  - prompting
  - configuracao
aliases:
  - AGENTS.md
  - CLAUDE.md
  - Skills agent
  - Cross-tool config
---

# Skills e instructions como contexto

> [!abstract] TL;DR
> Skills e instruction files (`AGENTS.md`, `CLAUDE.md`, `.cursorrules`) **são contexto** — só que persistente, versionado, e compartilhado entre sessões. Em 2026, `AGENTS.md` virou padrão de facto: especificação aberta sob a Linux Foundation, suportada nativamente por Cursor, Copilot, Gemini CLI, Windsurf, Aider, Zed, Warp, RooCode. Claude Code usa CLAUDE.md, mas o workaround é trivial (`ln -s AGENTS.md CLAUDE.md`). A regra de ouro: **80% das regras comuns vão em AGENTS.md, 20% específico vai em arquivo da ferramenta**.

## A separação que importa

```
┌──────────────────────────────────────┐
│  AGENTS.md  ← regras compartilhadas  │
│  (build, test, conventions)          │
└──────────────────────────────────────┘
       ↑                ↑                ↑
   CLAUDE.md       .cursorrules    .copilot-instructions
   (deltas)         (deltas)         (deltas)
```

Cada ferramenta lê o seu arquivo + (se configurado) o `AGENTS.md`. Single source of truth → menos drift, menos retrabalho.

## AGENTS.md — a especificação

> [!info] Stewardship
> AGENTS.md é uma especificação aberta, mantida pela **Agentic AI Foundation** sob a **Linux Foundation**. Surgiu de colaboração entre OpenAI Codex, Amp, Jules (Google), Cursor, Factory.

**Regras fundamentais:**

- Markdown padrão, sem schema, sem YAML frontmatter obrigatório
- Suportado nativamente por: Cursor, Copilot, Gemini CLI, Windsurf, Aider, Zed, Warp, RooCode
- Closest `AGENTS.md` to file being edited takes precedence (resolução hierárquica)
- Explicit user prompts override file contents

**Não suportado natively (em 2026):**

- Claude Code → usa `CLAUDE.md`. Workaround: `ln -s AGENTS.md CLAUDE.md`
- Algumas ferramentas legadas → workaround similar

## Estrutura típica

```markdown
# Project Name

Brief description of what the project is and what the agent should help with.

## Build & Test
- Install: `pnpm install`
- Test: `pnpm test`
- Build: `pnpm build`
- Lint: `pnpm lint`

## Conventions
- Use functional React components with hooks
- Prefer named exports over default exports
- All public functions must have JSDoc

## Project Structure
- `src/components/` — UI components
- `src/lib/` — pure logic, no React
- `src/api/` — API client wrappers

## Security Policies
- Never commit secrets to .env.example with real values
- All API calls must go through src/api/ wrapper

## Common Tasks
- Adding a new endpoint: see src/api/README.md
- Adding a UI component: follow patterns in src/components/Button.tsx
```

## Skills vs instructions — não confundir

| | Instructions (`AGENTS.md`) | Skills |
|---|---|---|
| **Escopo** | Projeto inteiro | Tarefa específica |
| **Tamanho** | 1-3K [[Dicionário de IA#Token\|tokens]] | 200 tokens a 5K cada |
| **Quando carregado** | Sempre, como contexto base | Quando a tarefa ativa |
| **Exemplo** | "Use TypeScript strict mode" | "Como debugar regression de latência" |
| **Atualização** | Raro, mudança importante | Iterativa, conforme aprende |

> [!tip] Skills emergiram em 2025-2026
> Skills são "playbooks reusáveis" que o agente carrega só quando relevante. Anthropic, OpenAI e outros padronizaram via SKILL.md / agent-skills. A diferença chave: skills **não** entram no contexto até o agente julgar que precisa — diferente de instructions que entram sempre.

## Cross-tool config — a estratégia 80/20

```
AGENTS.md (80% — regras gerais)
├── Build, test, lint commands
├── Conventions de código
├── Estrutura de pastas
├── Security policies
└── Padrões de PR

CLAUDE.md (20% — específicas Claude Code)
├── Hooks recomendados
└── MCP servers configurados

.cursorrules (20% — específicas Cursor)
├── Composer model preference
└── Auto-include patterns

.copilot-instructions (20% — específicas Copilot)
├── Suggestion style
└── Inline completion preferences
```

**Anti-pattern:** copiar-colar as mesmas regras em três arquivos. Vira drift garantido em 3 meses.

## Hierarquia e overrides

```
~/.config/agents/AGENTS.md       ← global do usuário (~5%)
   ↓ override por
projeto/AGENTS.md                 ← do projeto (90%)
   ↓ override por
projeto/src/feature-x/AGENTS.md   ← específico do diretório (5%)
   ↓ override por
prompt explícito do usuário       ← supera tudo
```

A ferramenta resolve **mais próximo do arquivo editado vence**. Convenção universal em 2026.

## Padrões emergentes

### Skills marketplace

Skills são **distribuíveis**: GitHub repos com `skill.md` + assets. Ferramentas começam a expor "instalar skill" como ação. (Ver [[Skills e Prompting]].)

### Versionamento de instructions

`AGENTS.md` virou candidato a code review. Mudança de regra = PR. Mesmo padrão de mudança de spec.

### Auto-discovery via hooks

Hooks (Claude Code) ou rules (Cursor) leem o filesystem e recomendam atualizações nos arquivos de instruction quando detectam padrões repetidos.

## O que NÃO colocar em AGENTS.md

- Segredos, credenciais, tokens
- Conteúdo sensível (PII de usuários)
- Coisas que mudam por sessão (decisões momentâneas — vão em [[10 - Structured state tracking|NOTES.md]])
- Histórico longo (vira ruído)
- Documentação completa do projeto (link para README; AGENTS.md é resumo acionável)

## Métricas

| Métrica | Alvo |
|---|---|
| **Tamanho de AGENTS.md** | 1-3K tokens (>5K vira ruído) |
| **% de regras seguidas em PRs gerados por IA** | >85% |
| **Drift entre AGENTS.md e código real** | <10% |
| **Frequência de atualização** | Mensal a trimestral |

## Anti-patterns

- **Documentação verbose** em vez de regras acionáveis
- **Regras duplicadas** entre AGENTS.md e ferramentas específicas
- **Instructions stale** — regra de 2024 ainda lá em 2026
- **AGENTS.md gigante** (>10K tokens) — vira context rot por si só
- **Nenhum AGENTS.md em projeto sério com IA** — cada sessão começa do zero

## Veja também

- [[Agentes de Codificação|14 - agents.md e configuração de projeto]]
- [[Skills e Prompting]]
- [[10 - Structured state tracking]]
- [[14 - Context engineering na prática — setup completo]]

## Referências

- **AGENTS.md spec** — *agents.md* (2026, Linux Foundation).
- **Augment Code** — *How to Build Your AGENTS.md (2026)* (2026).
- **DeployHQ** — *CLAUDE.md, AGENTS.md & Copilot Instructions* (2026).
- **Hivetrail** — *AGENTS.md vs CLAUDE.md: The AI Developer's Guide to Context Standards* (2026).
- **SmartScope** — *AGENTS.md Cross-Tool Unified Management Guide* (fev 2026).
