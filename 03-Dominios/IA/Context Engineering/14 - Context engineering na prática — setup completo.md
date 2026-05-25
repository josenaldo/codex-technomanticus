---
title: "Context engineering na prática — setup completo"
created: 2026-05-02
updated: 2026-05-02
type: concept
status: seedling
publish: true
tags:
  - context-engineering
  - ia
  - prompting
  - producao
  - setup
aliases:
  - Setup context engineering
  - Practical context engineering
  - End-to-end context setup
---

# Context engineering na prática — setup completo

> [!abstract] TL;DR
> Esta nota fecha a trilha com um exemplo end-to-end: como configurar context engineering num projeto real, do zero. Stack: `AGENTS.md` + `.agent/` (skills + state) + memory layer + JIT retrieval + guardrails. O alvo é um agente de coding em projeto Python — mas o padrão se traduz para qualquer domínio. Cada peça encaixa nas anteriores: fundamentos → camadas → retrieval → memória → guardrails. **Sem teoria — só checklist e arquivos**.

## O cenário

```
Projeto: API Python com FastAPI + Postgres
Time: 3 devs
Ferramenta principal: Claude Code (mas funciona com Cursor, Aider)
Modelo: Sonnet 4.6 com prompt caching
```

## Estrutura final

```
projeto/
├── AGENTS.md                    ← regras compartilhadas (símbolico para CLAUDE.md)
├── CLAUDE.md → AGENTS.md        ← symlink
├── .cursorrules                 ← deltas Cursor (se aplicável)
├── .agent/
│   ├── skills/
│   │   ├── debugging-fastapi.md
│   │   ├── refactoring-pydantic.md
│   │   └── adding-endpoint.md
│   ├── NOTES.md                 ← decisões e observações
│   ├── TODO.md                  ← próximos passos
│   ├── SYSTEM-DESIGN.md         ← arquitetura
│   ├── STATE.md                 ← estado da sessão (volátil, .gitignore)
│   └── DECISIONS.md             ← log de decisões importantes
├── .agent-memory/
│   ├── facts.jsonl              ← fatos persistidos (long-term)
│   └── archival.db              ← vector store de eventos
├── src/
├── tests/
└── .mcp/
    └── servers.json             ← MCP servers configurados (postgres, sentry, etc.)
```

## Passo 1 — AGENTS.md (camada imutável)

Ver [[11 - Skills e instructions como contexto]] para spec completa.

```markdown
# Projeto Pagamentos API

API REST para processar pagamentos. Stack: FastAPI + Postgres + Redis.

## Build & Test
- Install: `uv sync`
- Test: `pytest`
- Lint: `ruff check`
- Type check: `mypy src/`

## Conventions
- Pydantic v2 para todos os schemas
- Async/await em endpoints; sync em utility code
- Sempre type hints; sempre docstrings em funções públicas

## Structure
- `src/api/` — endpoints FastAPI
- `src/services/` — lógica de negócio
- `src/repositories/` — DB access (SQLAlchemy)
- `src/schemas/` — Pydantic models

## Security
- Nunca log de PII (CPF, cartão); usar redact_pii() de src/utils
- Validação de input em camada de schema, não service
- Secrets via env, nunca em código

## Workflow
1. Antes de editar: ler .agent/STATE.md e TODO.md
2. Após mudança significativa: atualizar .agent/NOTES.md
3. Antes de commit: rodar pytest + ruff
```

> [!tip] Symlink Claude Code
> ```bash
> ln -s AGENTS.md CLAUDE.md
> ```

## Passo 2 — Skills (camada de conhecimento reusável)

Cada skill resolve **um padrão recorrente**:

```markdown
# .agent/skills/adding-endpoint.md

## When to use
Quando o usuário pedir "adicione endpoint para X".

## Pattern
1. Criar schema em src/schemas/{feature}.py (Pydantic)
2. Criar service em src/services/{feature}.py
3. Criar repository se for novo recurso
4. Criar router em src/api/{feature}.py
5. Adicionar testes em tests/api/test_{feature}.py
6. Atualizar src/api/__init__.py para incluir router

## Example
Ver src/api/payments.py como template.

## Checklist
- [ ] Schema com validators (não só types)
- [ ] Service tem teste unitário
- [ ] Endpoint tem teste de integração
- [ ] Tipos estritos (no `Any`)
```

Skills carregam **só quando o agente decide que é relevante** — não inflam o contexto base.

## Passo 3 — Structured state (camada temporal)

Ver [[10 - Structured state tracking]].

```markdown
# .agent/STATE.md (volátil, gitignored)

## Tarefa atual
Adicionar endpoint POST /refunds

## Arquivos modificados
- src/schemas/refunds.py (criado, OK)
- src/services/refunds.py (em progresso)

## Próximo step
Implementar refund_payment() em service

## Bloqueios
Nenhum
```

```markdown
# .agent/TODO.md

## In progress
- [ ] Endpoint POST /refunds (responsável: agent + Maria)

## Up next
- [ ] Webhook de retry em pagamentos falhados
- [ ] Migração de coluna currency
```

## Passo 4 — Memory layer (camada persistente)

Para projeto solo, arquivos `.md` bastam (ver [[10 - Structured state tracking]]).

Para projeto com vários usuários ou sessões cruzadas, integrar Letta/Mem0/Zep:

```python
# .agent-memory/setup.py
from mem0 import Memory

memory = Memory.from_config({
    "vector_store": {"provider": "qdrant", "config": {...}},
    "llm": {"provider": "anthropic", "config": {"model": "claude-sonnet-4-6"}},
})

# Durante sessão, agente chama:
# memory.add("Maria prefere logs em INGLÊS", user_id="maria")
# memory.search("preferência de logs", user_id="maria")
```

## Passo 5 — JIT retrieval via MCP

Ver [[06 - Dynamic retrieval beyond RAG]] e [[15 - MCP — o protocolo universal]].

```json
// .mcp/servers.json
{
  "mcpServers": {
    "postgres": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-postgres", "postgresql://..."]
    },
    "sentry": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-sentry"],
      "env": {"SENTRY_TOKEN": "..."}
    },
    "filesystem": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-filesystem", "."]
    }
  }
}
```

Resultado: agente pode consultar logs, schema do DB, errors em produção, **sem indexar**.

## Passo 6 — Pipeline de montagem

Ver [[04 - Context pipelines — montagem dinâmica]].

Em Claude Code / Cursor, a pipeline é parcialmente automática (símbolico carrega `AGENTS.md`, glob/grep são tools nativas). Em código próprio:

```python
def build_context(turn):
    return [
        load_agents_md(turn.cwd),                    # imutável
        relevant_skills(turn.intent, top_k=2),        # skills sob demanda
        load_state_md(),                              # temporal
        load_relevant_memories(turn.user_id, top_k=5),# persistente
        compact_history(turn.history, budget=50_000), # temporal compactado
        turn.tool_definitions,                        # cacheável
        turn.user_message,                            # transiente
    ]
```

## Passo 7 — Guardrails determinísticos

Ver [[12 - Guardrails determinísticos]].

```python
# Pre-LLM
def pre_llm_guardrail(user_input):
    if contains_pii(user_input):
        return blocked("PII detected")
    if len(user_input) > 50_000:
        return blocked("Input too long")
    return ok()

# Post-LLM
def post_llm_guardrail(model_output):
    if not match_schema(model_output, expected_schema):
        return retry_with_correction()
    if requires_human_approval(model_output):
        return route_to_human()
    return ok()
```

## Checklist de implementação (por ordem)

> [!example] Roteiro de adoção
>
> ### Semana 1 — Fundamentos
> - [ ] Criar `AGENTS.md` (camada imutável) com 80% das regras
> - [ ] Symlink CLAUDE.md → AGENTS.md (se usa Claude Code)
> - [ ] Configurar prompt caching ([[Economia de Tokens|05 - Prompt caching na prática]])
>
> ### Semana 2 — Estado
> - [ ] Criar `.agent/SYSTEM-DESIGN.md`, `NOTES.md`, `TODO.md`
> - [ ] Adicionar `STATE.md` ao `.gitignore`
> - [ ] Adicionar workflow de leitura desses arquivos no AGENTS.md
>
> ### Semana 3 — Retrieval
> - [ ] Configurar 2-3 [[Dicionário de IA#MCP (Model Context Protocol)|MCP]] servers relevantes
> - [ ] Validar que agente usa JIT em vez de pedir paste
>
> ### Semana 4 — Skills
> - [ ] Criar 3-5 skills para padrões mais recorrentes
> - [ ] Estabelecer convenção de naming
>
> ### Mês 2 — Memória persistente (se necessário)
> - [ ] Avaliar se markdown basta ou precisa Mem0/Letta
> - [ ] Integrar memory layer
>
> ### Mês 3 — Governança
> - [ ] Adicionar pre-LLM e post-LLM guardrails básicos
> - [ ] Definir métricas (entropy, hit rate, latência)
> - [ ] Versionar mudanças em AGENTS.md como PRs

## O que medir

| Métrica | Antes | Depois esperado |
|---|---|---|
| [[Dicionário de IA#Token\|Tokens]] médios por turno | Baseline | -40% a -60% |
| Sessões que precisam restart | Baseline | -70% |
| % de PRs gerados que precisam refactor | Baseline | -30% |
| [[Dicionário de IA#Cache hit rate\|Cache hit rate]] | <20% | >70% |
| Tempo médio de tarefa | Baseline | -25% (após 3 meses de uso) |

## Quando expandir

| Sinal | Próximo passo |
|---|---|
| Skills viram redundantes | Refatorar / consolidar |
| `NOTES.md` fica enorme | Compactação periódica + arquivamento |
| Múltiplas pessoas usam o mesmo agente | Integrar memory layer compartilhada |
| Compliance pesa | Adicionar audit log + Lean-style guardrails |
| Custos crescem desproporcionalmente | Auditoria ([[Economia de Tokens|16 - Auditoria de consumo]]) |

## Veja também

- [[01 - De prompt engineering a context engineering]]
- [[04 - Context pipelines — montagem dinâmica]]
- [[10 - Structured state tracking]]
- [[11 - Skills e instructions como contexto]]
- [[12 - Guardrails determinísticos]]
- [[Agentes de Codificação]]
- [[Economia de Tokens]]

## Referências

- **Anthropic** — *Best Practices for Claude Code* (2026).
- **AGENTS.md spec** — *agents.md* (2026, Linux Foundation).
- **Anthropic** — *Effective context engineering for AI agents* (2025).
- **Augment Code** — *How to Build Your AGENTS.md* (2026).
