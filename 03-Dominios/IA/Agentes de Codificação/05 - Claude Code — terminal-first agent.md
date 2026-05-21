---
title: "Claude Code — terminal-first agent"
created: 2026-05-02
updated: 2026-05-02
type: concept
status: seedling
publish: true
tags:
  - agentes-codificacao
  - ia
  - ferramentas
aliases:
  - Claude Code
  - Terminal agent
  - Anthropic CLI
---

# Claude Code — terminal-first agent

> [!abstract] TL;DR
> Claude Code é o agente de terminal da Anthropic — roda no CLI, indexa o codebase inteiro, executa comandos, e itera autonomamente até resolver o problema. É o agente com melhor reasoning para código em 2026, ideal para debugging complexo, refactoring pesado, e workflows de CI/CD. O sistema de hooks e permissions dá controle granular sobre o que o agente pode fazer. Skills (SKILL.md) e CLAUDE.md são os arquivos de configuração que transformam o agente genérico em um especialista do seu projeto.

## O que é

**Claude Code** é um agente de codificação terminal-first desenvolvido pela Anthropic. Diferente de IDEs como Cursor, ele opera inteiramente no terminal — sem GUI. O fluxo é conversacional: você descreve o que quer, e o agente planeja, edita arquivos, roda comandos, analisa resultados, e itera.

## Por que importa

- **Melhor reasoning** do mercado para código (Claude Opus/Sonnet são líderes em SWE-bench)
- **Terminal-native** — integra perfeitamente em workflows de devs que vivem no terminal
- **Extensível via MCP** — conecta com qualquer ferramenta via Model Context Protocol
- **Hooks** — permitem automação e guardrails programáticos

## Como funciona

### Modos de operação

| Modo                  | Comportamento                               | Quando usar                    |
| --------------------- | ------------------------------------------- | ------------------------------ |
| **Interativo**        | Chat no terminal, pede permissão para ações | Desenvolvimento diário         |
| **Plan Mode**         | Apenas analisa, não modifica                | Entender código, planejar      |
| **Auto Mode**         | Executa sem pedir permissão (whitelist)     | Tarefas repetitivas confiáveis |
| **Headless/Dispatch** | API, sem interação humana                   | CI/CD, automação               |

### CLAUDE.md — o sistema operacional do agente

```markdown
# CLAUDE.md

## Sobre o projeto
Este é o backend do EstudeMe, um SaaS de flashcards.
Stack: Node.js 22, TypeScript, Fastify, Drizzle, PostgreSQL.

## Regras de código
- Sempre use strict TypeScript
- Error handling com Result<T, E> pattern
- Nunca use console.log em produção — use o logger (pino)
- Testes com Vitest, mínimo 80% coverage

## Comandos úteis
- `npm test` — roda testes
- `npm run lint` — verifica linting
- `npm run build` — compila TypeScript
- `npm run db:migrate` — roda migrations

## Arquitetura
- Clean Architecture: entities → use-cases → adapters → infra
- Cada módulo em src/modules/<nome>/
- Shared code em src/shared/
```

### Sistema de hooks

Hooks interceptam ações do agente em pontos específicos do lifecycle:

```json
// .claude/hooks.json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "bash",
        "command": "python3 .claude/validate-command.py"
      }
    ],
    "PostToolUse": [
      {
        "matcher": "write_file",
        "command": "npx eslint --fix $FILE"
      }
    ]
  }
}
```

| Hook                | Quando dispara                   | Uso típico                  |
| ------------------- | -------------------------------- | --------------------------- |
| `PreToolUse`        | Antes de executar uma ferramenta | Bloquear comandos perigosos |
| `PostToolUse`       | Depois de executar               | Auto-lint, auto-format      |
| `PermissionRequest` | Quando pede permissão            | Delegar decisão a outro LLM |
| `Stop`              | Quando o agente termina          | Notificação, logging        |

### Permissions — controle granular

```bash
# Permitir operações de leitura sem perguntar
claude config set permissions.allow "read_file,list_dir,grep_search"

# Permitir comandos específicos de terminal
claude config set permissions.allow "bash(npm test),bash(npm run lint)"

# Bloquear comandos perigosos
claude config set permissions.deny "bash(rm -rf),bash(git push --force)"
```

### Skills — capacidades modulares

Skills são pastas com instruções especializadas:

```
.claude/skills/
├── database-migration/
│   └── SKILL.md          # Instruções para criar migrations
├── api-endpoint/
│   └── SKILL.md          # Template para novos endpoints
└── test-coverage/
    └── SKILL.md          # Como aumentar coverage
```

### Workflows avançados

#### Dispatch (CI/CD)

```bash
# Usar Claude Code em CI/CD
claude --headless --message "Fix all lint errors and run tests" \
  --output json > result.json
```

#### Sessões paralelas (tmux)

```bash
# Terminal 1: Claude trabalhando no backend
tmux new-session -s backend "claude 'implement the auth module'"

# Terminal 2: Claude trabalhando no frontend
tmux new-session -s frontend "claude 'create the login component'"

# Terminal 3: Você monitorando
tmux attach -t backend
```

### MCP — extensibilidade

Claude Code suporta MCP servers nativamente:

```json
// .claude/mcp.json
{
  "servers": {
    "postgres": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-postgres"],
      "env": {"DATABASE_URL": "postgresql://..."}
    },
    "github": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-github"]
    }
  }
}
```

## Comparativo com Cursor

| Aspecto                  | Claude Code                | Cursor                      |
| ------------------------ | -------------------------- | --------------------------- |
| **Interface**            | Terminal (CLI/TUI)         | IDE (GUI)                   |
| **Reasoning**            | ★★★★★ (melhor do mercado)  | ★★★★ (depende do modelo)    |
| **Autocomplete**         | ★★ (não é o foco)          | ★★★★★                       |
| **Multi-file visual**    | ★★★ (diffs no terminal)    | ★★★★★ (preview visual)      |
| **Automação/CI**         | ★★★★★ (headless mode)      | ★★ (focado em interativo)   |
| **Extensibilidade**      | ★★★★★ (hooks, MCP, skills) | ★★★ (.cursorrules, limited) |
| **Curva de aprendizado** | Alta (terminal-first)      | Média (GUI familiar)        |

## Armadilhas

- **Não criar CLAUDE.md** — sem contexto do projeto, o agente gera código genérico que não segue seus padrões.
- **Auto mode sem hooks** — dar autonomia total sem guardrails é receita para desastre. Configure hooks antes de usar auto mode.
- **Ignorar o custo** — sessões longas de Claude Code com Opus podem custar $10-20/dia. Monitore com `ccusage`.
- **Não usar Plan Mode** — pular direto para implementação sem planejar gera mais iterações e mais custo.
- **Terminal anxiety** — se você não é confortável no terminal, Cursor pode ser melhor ponto de partida.

## Veja também

- [[03-Dominios/IA/Claude Code/index|Trilha Claude Code]] — aprofundamento completo em 6 galhos: mental model, configuração, hooks, skills/MCP, workflows e automação
- [[04 - Cursor — AI-native IDE]] — alternativa IDE para quem prefere GUI
- [[10 - OpenCode — o harness open source]] — alternativa open-source
- [[15 - MCP — o protocolo universal]] — como estender o Claude Code com ferramentas

## Referências

- **Anthropic** — *Claude Code Documentation* (2026). Referência oficial.
- **claudefa.st** — *Claude Code Best Practices* (2026). Guia comunitário.
- **Builder.io** — *Claude Code Workflows* (2026). Patterns de uso avançado.
