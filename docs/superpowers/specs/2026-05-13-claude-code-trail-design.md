# Design: Trilha Claude Code

**Data:** 2026-05-13  
**Status:** aprovado  
**Domínio:** `03-Dominios/IA/Claude Code/`

---

## Contexto

O vault já possui uma nota `05 - Claude Code — terminal-first agent.md` dentro de `IA/Agentes de Codificação/`, que cobre visão geral comparativa com outras ferramentas. Esta trilha é uma expansão independente e aprofundada — a nota existente permanece onde está como overview comparativo, com wikilink apontando para a nova trilha.

**Objetivo:** cobrir o que um senior dev precisa saber sobre Claude Code além de comandos básicos — do mental model até automação e governança de time.

---

## Escopo

- **Inclui:** Claude Code CLI — configuração, hooks, skills, MCP, workflows, CI/CD, time
- **Exclui:** Anthropic SDK/API para construção de agentes (tema de trilha separada)
- **Público:** dev individual (produtividade), tech lead (time), engenheiro de automação (CI/CD)

---

## Estrutura

```
03-Dominios/IA/Claude Code/
├── index.md                    ← tronco: mapa + rota por persona
├── Mental Model/
├── Configuração/
├── Hooks e Guardrails/
├── Skills e MCP/
├── Workflows/
└── Time e Automação/
```

### index.md — tronco

- Visão geral da trilha
- Roteamento por persona:
  - **"Quero ser mais produtivo hoje"** → Mental Model → Configuração → Workflows
  - **"Quero montar o setup do meu time"** → Configuração → Hooks e Guardrails → Time e Automação
  - **"Quero automatizar com CI/CD"** → Mental Model → Hooks e Guardrails → Time e Automação
- Links para todos os galhos
- Seção "Veja também": wikilink para `05 - Claude Code — terminal-first agent.md`

---

## Galhos

### Galho 1 — Mental Model (~8 notas)

*O que o agente realmente é e como ele pensa — a base que torna todos os outros galhos legíveis.*

| # | Nota |
|---|------|
| 01 | O loop agentic — plan, act, observe, iterate |
| 02 | Como Claude Code lê um codebase — indexação, contexto, relevância |
| 03 | Tool use — como o agente usa ferramentas (bash, read, edit, grep) |
| 04 | Context window — o que entra, o que sai, por que isso importa |
| 05 | Modos de operação — interativo, plan mode, auto mode, headless |
| 06 | Compaction — como o Claude Code gerencia contextos longos |
| 07 | Tokens e custo — como sessões consomem tokens na prática |
| 08 | Como o agente decide — confiança, raciocínio, iteração |

**Index do galho:** overview do mental model, por que entender o internals muda como você usa a ferramenta, links para as 8 notas.

---

### Galho 2 — Configuração (~8 notas)

*Transformar o agente genérico num especialista do seu projeto.*

| # | Nota |
|---|------|
| 01 | Hierarquia de configuração — global → projeto → user (precedência) |
| 02 | CLAUDE.md — anatomia e o que colocar em cada seção |
| 03 | CLAUDE.md — receitas para projetos Node, Python, Go, monorepos |
| 04 | settings.json — permissões, comportamentos, variáveis de ambiente |
| 05 | Permissions — allow/deny por ferramenta e por comando bash |
| 06 | Aliases e slash commands customizados |
| 07 | `.claude/` — estrutura completa da pasta de configuração |
| 08 | Armadilhas de configuração — erros comuns e como evitar |

**Index do galho:** por que configuração é o maior multiplicador de produtividade, links para as 8 notas.

---

### Galho 3 — Hooks e Guardrails (~8 notas)

*Controle programático do que o agente pode e não pode fazer.*

| # | Nota |
|---|------|
| 01 | Sistema de hooks — visão geral do lifecycle |
| 02 | PreToolUse — interceptar e validar antes de executar |
| 03 | PostToolUse — auto-lint, auto-format, notificações pós-ação |
| 04 | Stop hook — notificação, logging, cleanup ao terminar |
| 05 | Guardrails — bloquear comandos destrutivos ou perigosos |
| 06 | Delegar permissão a outro LLM — pattern de meta-agente |
| 07 | Hooks para segurança — evitar commits acidentais, push force, rm -rf |
| 08 | Testando e debugando hooks |

**Index do galho:** por que hooks são o sistema nervoso do Claude Code, links para as 8 notas.

---

### Galho 4 — Skills e MCP (~8 notas)

*Capacidades modulares que transformam Claude Code num agente especializado.*

| # | Nota |
|---|------|
| 01 | Anatomia de uma skill — estrutura, frontmatter, tipos |
| 02 | Skills de processo vs skills de domínio |
| 03 | Criar sua primeira skill — walkthrough prático |
| 04 | MCP — Model Context Protocol overview para dev |
| 05 | MCP servers essenciais — postgres, github, filesystem, browser |
| 06 | Criar um MCP server personalizado — quando e como |
| 07 | Compondo skills + MCP para agentes especializados |
| 08 | Gerenciar e versionar skills em time |

**Index do galho:** skills e MCP como sistema de extensão, links para as 8 notas.

---

### Galho 5 — Workflows (~10 notas)

*Padrões de trabalho que multiplicam produtividade.*

| # | Nota |
|---|------|
| 01 | Plan Mode — planejar antes de agir, quando usar |
| 02 | TDD com Claude Code — test-first workflow |
| 03 | Refactoring pesado — estratégia para mudanças grandes sem perder controle |
| 04 | Debugging complexo — usando Claude Code para diagnosticar, não só corrigir |
| 05 | Code review com Claude Code — revisão como pair programmer |
| 06 | Sessões paralelas — tmux + worktrees para trabalhar em múltiplas frentes |
| 07 | Sub-agents e dispatch — delegar tarefas para agentes filhos |
| 08 | Multi-agent — coordenar múltiplos agentes em paralelo |
| 09 | Prompting para Claude Code — como comunicar tarefas com precisão |
| 10 | Gestão de contexto em sessões longas — quando compactar, quando reiniciar |

**Index do galho:** workflows como diferencial entre quem usa e quem domina, links para as 10 notas.

---

### Galho 6 — Time e Automação (~8 notas)

*Escalar Claude Code além do uso individual.*

| # | Nota |
|---|------|
| 01 | Headless mode — executar Claude Code sem interação humana |
| 02 | CI/CD com GitHub Actions — integrar na pipeline |
| 03 | Dispatch via `claude -p` — casos de uso e padrões |
| 04 | CLAUDE.md compartilhado — o que vai no repo, o que fica local |
| 05 | Controle de custo — monitoramento, limites, ccusage |
| 06 | Segurança organizacional — o que nunca deixar o agente fazer |
| 07 | Onboarding de time — como introduzir Claude Code sem caos |
| 08 | Avaliando qualidade do output — quando confiar, quando revisar |

**Index do galho:** escalar Claude Code de individual para organizacional, links para as 8 notas.

---

## Padrão das notas atômicas

Cada nota segue a estrutura:

```markdown
---
title: "<título>"
type: concept
publish: true
tags: [claude-code, <galho>]
created: YYYY-MM-DD
updated: YYYY-MM-DD
status: seedling
---

# <Título>

> [!abstract] TL;DR
> ...

## O que é / Como funciona

## Na prática (exemplos de código)

## Armadilhas

## Veja também

## Referências
```

---

## Relação com notas existentes

| Nota existente | Relação |
|---|---|
| `IA/Agentes de Codificação/05 - Claude Code — terminal-first agent.md` | Permanece como overview comparativo; recebe wikilink para `IA/Claude Code/index` |
| `IA/Agentes de Codificação/14 - agents.md e configuração de projeto.md` | Wikilink para Galho 2 (Configuração) |
| `IA/Agentes de Codificação/15 - MCP — o protocolo universal.md` | Wikilink para Galho 4 (Skills e MCP) |
| `IA/Agentes de Codificação/12 - Multi-agent — workflows com múltiplos agentes.md` | Wikilink para Galho 5 (Workflows) |

---

## Volume estimado

| Item | Quantidade |
|---|---|
| Galhos | 6 |
| Notas atômicas | ~50 |
| Index files (tronco + galhos) | 7 |
| **Total de arquivos** | **~57** |

---

## Ordem de implementação sugerida

1. `index.md` (tronco) — esqueleto com links TBD
2. Galho 1: Mental Model — sem isso, os outros galhos ficam sem base
3. Galho 2: Configuração — highest ROI para uso imediato
4. Galho 5: Workflows — alto valor prático
5. Galho 3: Hooks e Guardrails
6. Galho 4: Skills e MCP
7. Galho 6: Time e Automação
8. Atualizar wikilinks nas notas de `Agentes de Codificação`
