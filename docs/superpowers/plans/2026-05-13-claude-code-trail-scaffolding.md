# Claude Code Trail — Scaffolding & Index Files

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Criar a estrutura de pastas, todos os index files (tronco + 6 galhos) e atualizar wikilinks nas notas existentes para bootstrapar a trilha Claude Code.

**Architecture:** Nova trilha em `03-Dominios/IA/Claude Code/` com 6 sub-pastas de galhos, cada uma com index.md. Segue o padrão tronco/galhos da trilha Node. Notas existentes em `Agentes de Codificação/` recebem wikilinks para a nova trilha. Este plano cria apenas os index files — cada galho tem seu próprio plano de execução para as notas atômicas.

**Tech Stack:** Obsidian Flavored Markdown, frontmatter YAML, wikilinks

---

## File Map

**Criar:**
- `03-Dominios/IA/Claude Code/index.md`
- `03-Dominios/IA/Claude Code/Mental Model/index.md`
- `03-Dominios/IA/Claude Code/Configuração/index.md`
- `03-Dominios/IA/Claude Code/Hooks e Guardrails/index.md`
- `03-Dominios/IA/Claude Code/Skills e MCP/index.md`
- `03-Dominios/IA/Claude Code/Workflows/index.md`
- `03-Dominios/IA/Claude Code/Time e Automação/index.md`

**Modificar:**
- `03-Dominios/IA/Agentes de Codificação/05 - Claude Code — terminal-first agent.md` — adicionar wikilink para nova trilha no "Veja também"
- `03-Dominios/IA/Agentes de Codificação/14 - agents.md e configuração de projeto.md` — adicionar wikilink para Galho 2 (Configuração)
- `03-Dominios/IA/Agentes de Codificação/15 - MCP — o protocolo universal.md` — adicionar wikilink para Galho 4 (Skills e MCP)
- `03-Dominios/IA/Agentes de Codificação/12 - Multi-agent — workflows com múltiplos agentes.md` — adicionar wikilink para Galho 5 (Workflows)
- `03-Dominios/IA/index.md` — adicionar referência à trilha Claude Code na seção de Trilha 3

---

## Task 1: Criar tronco `Claude Code/index.md`

**Files:**
- Create: `03-Dominios/IA/Claude Code/index.md`

- [ ] **Step 1: Criar o arquivo**

Crie `03-Dominios/IA/Claude Code/index.md` com o conteúdo:

```markdown
---
title: "Claude Code"
type: moc
publish: true
created: 2026-05-13
updated: 2026-05-13
status: seedling
tags:
  - claude-code
  - ia
  - moc
  - ferramentas
aliases:
  - Claude Code Trail
  - Claude Code CLI
---

# Claude Code

> [!abstract] TL;DR
> Trilha Claude Code em 6 galhos: Mental Model, Configuração, Hooks e Guardrails, Skills e MCP, Workflows, Time e Automação. Cobre desde como o agente realmente funciona até CI/CD, multi-agent e governança de time.

Claude Code é o agente de terminal da Anthropic — e usá-lo bem é diferente de apenas rodar comandos. Esta trilha cobre o que um senior dev precisa saber para ir além do básico: entender o loop agentic, configurar o agente para o seu projeto, programar guardrails com hooks, criar skills modulares, trabalhar com padrões avançados (TDD, multi-agent, sessões paralelas) e escalar o uso para times e pipelines de CI/CD.

> [!tip] Por onde começar?
>
> Depende do seu objetivo:
>
> - **"Quero ser mais produtivo hoje"** → Mental Model → Configuração → Workflows
> - **"Quero montar o setup do meu time"** → Configuração → Hooks e Guardrails → Time e Automação
> - **"Quero automatizar com CI/CD"** → Mental Model → Hooks e Guardrails → Time e Automação

## Conteúdo

### Galhos da trilha Claude Code

- [[03-Dominios/IA/Claude Code/Mental Model/index|Mental Model]] — galho 1: o loop agentic, como o agente lê código, tool use, context window, modos de operação, compaction, custo e decisão
- [[03-Dominios/IA/Claude Code/Configuração/index|Configuração]] — galho 2: hierarquia de configuração, CLAUDE.md, settings.json, permissions, aliases e armadilhas
- [[03-Dominios/IA/Claude Code/Hooks e Guardrails/index|Hooks e Guardrails]] — galho 3: lifecycle de hooks, PreToolUse, PostToolUse, Stop, guardrails, meta-agente, segurança, debugging
- [[03-Dominios/IA/Claude Code/Skills e MCP/index|Skills e MCP]] — galho 4: anatomia de skills, criar skills, MCP servers essenciais, criar MCP customizado, composição, versionamento em time
- [[03-Dominios/IA/Claude Code/Workflows/index|Workflows]] — galho 5: Plan Mode, TDD, refactoring pesado, debugging, code review, sessões paralelas, sub-agents, multi-agent, prompting, gestão de contexto
- [[03-Dominios/IA/Claude Code/Time e Automação/index|Time e Automação]] — galho 6: headless mode, CI/CD, dispatch, CLAUDE.md compartilhado, custo, segurança organizacional, onboarding, qualidade de output

## Veja também

- [[03-Dominios/IA/Agentes de Codificação/05 - Claude Code — terminal-first agent|Claude Code — terminal-first agent]] — overview comparativo com outros agentes de codificação
- [[03-Dominios/IA/Agentes de Codificação/15 - MCP — o protocolo universal|MCP — o protocolo universal]] — protocolo que sustenta a extensibilidade
- [[03-Dominios/IA/Agentes de Codificação/12 - Multi-agent — workflows com múltiplos agentes|Multi-agent]] — contexto mais amplo de workflows multi-agente
- [[03-Dominios/IA/Agentes de Codificação/index|Agentes de Codificação]] — trilha que contextualiza Claude Code entre os demais players
```

- [ ] **Step 2: Verificar criação**

```bash
ls "03-Dominios/IA/Claude Code/"
```

Esperado: `index.md`

- [ ] **Step 3: Commit**

```bash
git add "03-Dominios/IA/Claude Code/index.md"
git commit -m "feat(claude-code): add tronco index.md"
```

---

## Task 2: Criar `Mental Model/index.md`

**Files:**
- Create: `03-Dominios/IA/Claude Code/Mental Model/index.md`

- [ ] **Step 1: Criar o arquivo**

```markdown
---
title: "Mental Model — Claude Code"
type: moc
publish: true
created: 2026-05-13
updated: 2026-05-13
status: seedling
tags:
  - claude-code
  - mental-model
  - moc
aliases:
  - Galho 1 - Mental Model
  - Claude Code Mental Model
---

# Mental Model — Claude Code

> [!abstract] TL;DR
> Galho 1 da trilha Claude Code. Cobre como o agente realmente funciona internamente: loop agentic, leitura de codebase, tool use, context window, modos de operação, compaction, custo e tomada de decisão. Pré-requisito recomendado para todos os outros galhos.

## Sobre este galho

Entender o mental model do Claude Code muda como você usa a ferramenta. Saber que o agente não indexa o codebase como uma IDE, mas navega com grep/glob/find, explica por que um CLAUDE.md bem escrito importa tanto. Saber como a context window se comporta explica por que sessões longas ficam mais lentas e custosas.

Este galho constrói o mapa mental que torna os outros galhos legíveis.

## Notas

1. [[03-Dominios/IA/Claude Code/Mental Model/01 - O loop agentic|01 - O loop agentic — plan, act, observe, iterate]]
2. [[03-Dominios/IA/Claude Code/Mental Model/02 - Como Claude Code lê um codebase|02 - Como Claude Code lê um codebase]]
3. [[03-Dominios/IA/Claude Code/Mental Model/03 - Tool use|03 - Tool use — como o agente usa ferramentas]]
4. [[03-Dominios/IA/Claude Code/Mental Model/04 - Context window|04 - Context window — o que entra, o que sai]]
5. [[03-Dominios/IA/Claude Code/Mental Model/05 - Modos de operação|05 - Modos de operação — interativo, plan, auto, headless]]
6. [[03-Dominios/IA/Claude Code/Mental Model/06 - Compaction|06 - Compaction — gerenciando contextos longos]]
7. [[03-Dominios/IA/Claude Code/Mental Model/07 - Tokens e custo|07 - Tokens e custo — como sessões consomem recursos]]
8. [[03-Dominios/IA/Claude Code/Mental Model/08 - Como o agente decide|08 - Como o agente decide — confiança, raciocínio, iteração]]

## Veja também

- [[03-Dominios/IA/Claude Code/index|Claude Code]] — tronco da trilha
- [[03-Dominios/IA/Claude Code/Configuração/index|Configuração]] — próximo galho recomendado
```

- [ ] **Step 2: Verificar**

```bash
ls "03-Dominios/IA/Claude Code/Mental Model/"
```

Esperado: `index.md`

- [ ] **Step 3: Commit**

```bash
git add "03-Dominios/IA/Claude Code/Mental Model/index.md"
git commit -m "feat(claude-code/g1): add Mental Model index"
```

---

## Task 3: Criar `Configuração/index.md`

**Files:**
- Create: `03-Dominios/IA/Claude Code/Configuração/index.md`

- [ ] **Step 1: Criar o arquivo**

```markdown
---
title: "Configuração — Claude Code"
type: moc
publish: true
created: 2026-05-13
updated: 2026-05-13
status: seedling
tags:
  - claude-code
  - configuracao
  - moc
aliases:
  - Galho 2 - Configuração
  - Claude Code Config
---

# Configuração — Claude Code

> [!abstract] TL;DR
> Galho 2 da trilha Claude Code. Cobre toda a camada de configuração: hierarquia global → projeto → user, anatomia do CLAUDE.md, settings.json, sistema de permissões, aliases e slash commands. O maior multiplicador de produtividade ao usar Claude Code é configurar bem.

## Sobre este galho

Claude Code sem configuração é como um dev sem contexto de projeto — ele funciona, mas gera código genérico que não segue seus padrões. CLAUDE.md é o arquivo que transforma o agente genérico em especialista do seu projeto. settings.json controla o que ele pode e não pode fazer. Permissions define granularidade de acesso.

Este galho cobre cada peça da camada de configuração, com receitas prontas para projetos reais.

## Notas

1. [[03-Dominios/IA/Claude Code/Configuração/01 - Hierarquia de configuração|01 - Hierarquia de configuração — global, projeto, user]]
2. [[03-Dominios/IA/Claude Code/Configuração/02 - CLAUDE.md anatomia|02 - CLAUDE.md — anatomia e o que colocar em cada seção]]
3. [[03-Dominios/IA/Claude Code/Configuração/03 - CLAUDE.md receitas|03 - CLAUDE.md — receitas para Node, Python, Go, monorepos]]
4. [[03-Dominios/IA/Claude Code/Configuração/04 - settings.json|04 - settings.json — permissões, comportamentos, env vars]]
5. [[03-Dominios/IA/Claude Code/Configuração/05 - Permissions|05 - Permissions — allow/deny por ferramenta e por comando]]
6. [[03-Dominios/IA/Claude Code/Configuração/06 - Aliases e slash commands|06 - Aliases e slash commands customizados]]
7. [[03-Dominios/IA/Claude Code/Configuração/07 - Pasta .claude|07 - A pasta .claude — estrutura completa]]
8. [[03-Dominios/IA/Claude Code/Configuração/08 - Armadilhas de configuração|08 - Armadilhas de configuração — erros comuns e como evitar]]

## Veja também

- [[03-Dominios/IA/Claude Code/index|Claude Code]] — tronco da trilha
- [[03-Dominios/IA/Claude Code/Mental Model/index|Mental Model]] — galho anterior
- [[03-Dominios/IA/Claude Code/Hooks e Guardrails/index|Hooks e Guardrails]] — próximo galho recomendado
- [[03-Dominios/IA/Agentes de Codificação/14 - agents.md e configuração de projeto|agents.md e configuração de projeto]] — contexto adicional
```

- [ ] **Step 2: Verificar**

```bash
ls "03-Dominios/IA/Claude Code/Configuração/"
```

- [ ] **Step 3: Commit**

```bash
git add "03-Dominios/IA/Claude Code/Configuração/index.md"
git commit -m "feat(claude-code/g2): add Configuração index"
```

---

## Task 4: Criar `Hooks e Guardrails/index.md`

**Files:**
- Create: `03-Dominios/IA/Claude Code/Hooks e Guardrails/index.md`

- [ ] **Step 1: Criar o arquivo**

```markdown
---
title: "Hooks e Guardrails — Claude Code"
type: moc
publish: true
created: 2026-05-13
updated: 2026-05-13
status: seedling
tags:
  - claude-code
  - hooks
  - guardrails
  - moc
aliases:
  - Galho 3 - Hooks e Guardrails
  - Claude Code Hooks
---

# Hooks e Guardrails — Claude Code

> [!abstract] TL;DR
> Galho 3 da trilha Claude Code. Cobre o sistema de hooks (lifecycle, PreToolUse, PostToolUse, Stop), guardrails para bloquear ações perigosas, delegação de permissão a outro LLM, segurança e como testar hooks. Hooks são o sistema nervoso do Claude Code — sem eles, você está dando autonomia sem controle.

## Sobre este galho

Hooks transformam Claude Code de "agente que pede permissão" em "agente com políticas programáticas". PreToolUse intercepta antes de executar (permite bloquear, validar, logar). PostToolUse dispara depois (auto-lint, auto-format, notificações). Stop hook executa quando o agente termina.

Guardrails são hooks que bloqueiam ações destrutivas — sem eles, auto mode é risco. Com eles, é produtividade real.

## Notas

1. [[03-Dominios/IA/Claude Code/Hooks e Guardrails/01 - Sistema de hooks|01 - Sistema de hooks — visão geral do lifecycle]]
2. [[03-Dominios/IA/Claude Code/Hooks e Guardrails/02 - PreToolUse|02 - PreToolUse — interceptar e validar antes de executar]]
3. [[03-Dominios/IA/Claude Code/Hooks e Guardrails/03 - PostToolUse|03 - PostToolUse — automação pós-ação]]
4. [[03-Dominios/IA/Claude Code/Hooks e Guardrails/04 - Stop hook|04 - Stop hook — notificação, logging, cleanup]]
5. [[03-Dominios/IA/Claude Code/Hooks e Guardrails/05 - Guardrails|05 - Guardrails — bloquear comandos destrutivos]]
6. [[03-Dominios/IA/Claude Code/Hooks e Guardrails/06 - Delegar permissão|06 - Delegar permissão a outro LLM — pattern meta-agente]]
7. [[03-Dominios/IA/Claude Code/Hooks e Guardrails/07 - Segurança com hooks|07 - Hooks para segurança — commits, push force, rm -rf]]
8. [[03-Dominios/IA/Claude Code/Hooks e Guardrails/08 - Testando hooks|08 - Testando e debugando hooks]]

## Veja também

- [[03-Dominios/IA/Claude Code/index|Claude Code]] — tronco da trilha
- [[03-Dominios/IA/Claude Code/Configuração/index|Configuração]] — galho anterior
- [[03-Dominios/IA/Claude Code/Skills e MCP/index|Skills e MCP]] — próximo galho
- [[03-Dominios/IA/Claude Code/Time e Automação/index|Time e Automação]] — onde guardrails se tornam políticas de time
```

- [ ] **Step 2: Verificar**

```bash
ls "03-Dominios/IA/Claude Code/Hooks e Guardrails/"
```

- [ ] **Step 3: Commit**

```bash
git add "03-Dominios/IA/Claude Code/Hooks e Guardrails/index.md"
git commit -m "feat(claude-code/g3): add Hooks e Guardrails index"
```

---

## Task 5: Criar `Skills e MCP/index.md`

**Files:**
- Create: `03-Dominios/IA/Claude Code/Skills e MCP/index.md`

- [ ] **Step 1: Criar o arquivo**

```markdown
---
title: "Skills e MCP — Claude Code"
type: moc
publish: true
created: 2026-05-13
updated: 2026-05-13
status: seedling
tags:
  - claude-code
  - skills
  - mcp
  - moc
aliases:
  - Galho 4 - Skills e MCP
  - Claude Code Skills
  - Claude Code MCP
---

# Skills e MCP — Claude Code

> [!abstract] TL;DR
> Galho 4 da trilha Claude Code. Cobre anatomia de skills, como criar skills de processo e de domínio, MCP servers essenciais (postgres, github, filesystem), como criar um MCP server customizado, composição de skills + MCP, e versionamento em time. Skills e MCP são o sistema de extensão que transforma Claude Code num agente especializado.

## Sobre este galho

Skills são arquivos de instrução que ensinam o agente a seguir um processo específico — TDD, code review, debugging. MCP (Model Context Protocol) são servidores que dão ao agente acesso a ferramentas externas — bancos de dados, APIs, browsers.

Juntos, skills e MCP transformam o Claude Code genérico em um agente especialista do seu projeto, stack e processo.

## Notas

1. [[03-Dominios/IA/Claude Code/Skills e MCP/01 - Anatomia de uma skill|01 - Anatomia de uma skill — estrutura, frontmatter, tipos]]
2. [[03-Dominios/IA/Claude Code/Skills e MCP/02 - Skills de processo vs domínio|02 - Skills de processo vs skills de domínio]]
3. [[03-Dominios/IA/Claude Code/Skills e MCP/03 - Criar sua primeira skill|03 - Criar sua primeira skill — walkthrough prático]]
4. [[03-Dominios/IA/Claude Code/Skills e MCP/04 - MCP overview|04 - MCP — Model Context Protocol overview para dev]]
5. [[03-Dominios/IA/Claude Code/Skills e MCP/05 - MCP servers essenciais|05 - MCP servers essenciais — postgres, github, filesystem, browser]]
6. [[03-Dominios/IA/Claude Code/Skills e MCP/06 - Criar MCP server|06 - Criar um MCP server personalizado — quando e como]]
7. [[03-Dominios/IA/Claude Code/Skills e MCP/07 - Compondo skills e MCP|07 - Compondo skills + MCP para agentes especializados]]
8. [[03-Dominios/IA/Claude Code/Skills e MCP/08 - Skills em time|08 - Gerenciar e versionar skills em time]]

## Veja também

- [[03-Dominios/IA/Claude Code/index|Claude Code]] — tronco da trilha
- [[03-Dominios/IA/Claude Code/Hooks e Guardrails/index|Hooks e Guardrails]] — galho anterior
- [[03-Dominios/IA/Claude Code/Workflows/index|Workflows]] — próximo galho
- [[03-Dominios/IA/Agentes de Codificação/15 - MCP — o protocolo universal|MCP — o protocolo universal]] — visão mais ampla do protocolo
- [[03-Dominios/IA/MCP/index|MCP]] — trilha dedicada ao Model Context Protocol
```

- [ ] **Step 2: Verificar**

```bash
ls "03-Dominios/IA/Claude Code/Skills e MCP/"
```

- [ ] **Step 3: Commit**

```bash
git add "03-Dominios/IA/Claude Code/Skills e MCP/index.md"
git commit -m "feat(claude-code/g4): add Skills e MCP index"
```

---

## Task 6: Criar `Workflows/index.md`

**Files:**
- Create: `03-Dominios/IA/Claude Code/Workflows/index.md`

- [ ] **Step 1: Criar o arquivo**

```markdown
---
title: "Workflows — Claude Code"
type: moc
publish: true
created: 2026-05-13
updated: 2026-05-13
status: seedling
tags:
  - claude-code
  - workflows
  - moc
aliases:
  - Galho 5 - Workflows
  - Claude Code Workflows
---

# Workflows — Claude Code

> [!abstract] TL;DR
> Galho 5 da trilha Claude Code. Cobre os padrões de trabalho que multiplicam produtividade: Plan Mode, TDD, refactoring pesado, debugging, code review, sessões paralelas com tmux/worktrees, sub-agents, multi-agent, prompting preciso e gestão de contexto em sessões longas.

## Sobre este galho

A diferença entre quem usa e quem domina Claude Code está nos workflows. Usar Plan Mode antes de implementar reduz iterações e custo. TDD com Claude Code produz código mais confiável. Sessões paralelas com worktrees multiplicam throughput. Multi-agent distribui tarefas independentes.

Este galho é o mais prático da trilha — cada nota é um padrão aplicável no dia seguinte.

## Notas

1. [[03-Dominios/IA/Claude Code/Workflows/01 - Plan Mode|01 - Plan Mode — planejar antes de agir]]
2. [[03-Dominios/IA/Claude Code/Workflows/02 - TDD com Claude Code|02 - TDD com Claude Code — test-first workflow]]
3. [[03-Dominios/IA/Claude Code/Workflows/03 - Refactoring pesado|03 - Refactoring pesado — mudanças grandes sem perder controle]]
4. [[03-Dominios/IA/Claude Code/Workflows/04 - Debugging complexo|04 - Debugging complexo — diagnosticar, não só corrigir]]
5. [[03-Dominios/IA/Claude Code/Workflows/05 - Code review|05 - Code review com Claude Code]]
6. [[03-Dominios/IA/Claude Code/Workflows/06 - Sessões paralelas|06 - Sessões paralelas — tmux + worktrees]]
7. [[03-Dominios/IA/Claude Code/Workflows/07 - Sub-agents e dispatch|07 - Sub-agents e dispatch — delegar tarefas]]
8. [[03-Dominios/IA/Claude Code/Workflows/08 - Multi-agent|08 - Multi-agent — coordenar agentes em paralelo]]
9. [[03-Dominios/IA/Claude Code/Workflows/09 - Prompting para Claude Code|09 - Prompting para Claude Code — comunicar tarefas com precisão]]
10. [[03-Dominios/IA/Claude Code/Workflows/10 - Gestão de contexto|10 - Gestão de contexto em sessões longas]]

## Veja também

- [[03-Dominios/IA/Claude Code/index|Claude Code]] — tronco da trilha
- [[03-Dominios/IA/Claude Code/Skills e MCP/index|Skills e MCP]] — galho anterior
- [[03-Dominios/IA/Claude Code/Time e Automação/index|Time e Automação]] — próximo galho
- [[03-Dominios/IA/Agentes de Codificação/12 - Multi-agent — workflows com múltiplos agentes|Multi-agent — workflows]] — contexto mais amplo
```

- [ ] **Step 2: Verificar**

```bash
ls "03-Dominios/IA/Claude Code/Workflows/"
```

- [ ] **Step 3: Commit**

```bash
git add "03-Dominios/IA/Claude Code/Workflows/index.md"
git commit -m "feat(claude-code/g5): add Workflows index"
```

---

## Task 7: Criar `Time e Automação/index.md`

**Files:**
- Create: `03-Dominios/IA/Claude Code/Time e Automação/index.md`

- [ ] **Step 1: Criar o arquivo**

```markdown
---
title: "Time e Automação — Claude Code"
type: moc
publish: true
created: 2026-05-13
updated: 2026-05-13
status: seedling
tags:
  - claude-code
  - time
  - automacao
  - moc
aliases:
  - Galho 6 - Time e Automação
  - Claude Code CI/CD
  - Claude Code Team
---

# Time e Automação — Claude Code

> [!abstract] TL;DR
> Galho 6 da trilha Claude Code. Cobre headless mode, CI/CD com GitHub Actions, dispatch via `claude -p`, CLAUDE.md compartilhado em time, controle de custo, segurança organizacional, onboarding e avaliação de qualidade de output. Escalar Claude Code de individual para organizacional.

## Sobre este galho

Claude Code foi projetado para escalar além do uso individual. Headless mode permite execução sem interação humana — ideal para CI/CD. O sistema de permissões e hooks viabiliza políticas organizacionais. CLAUDE.md compartilhado no repo garante que todos no time trabalhem com o mesmo contexto.

Este galho cobre o que um tech lead ou engenheiro de plataforma precisa saber para introduzir Claude Code de forma sustentável num time.

## Notas

1. [[03-Dominios/IA/Claude Code/Time e Automação/01 - Headless mode|01 - Headless mode — Claude Code sem interação humana]]
2. [[03-Dominios/IA/Claude Code/Time e Automação/02 - CI-CD com GitHub Actions|02 - CI/CD com GitHub Actions]]
3. [[03-Dominios/IA/Claude Code/Time e Automação/03 - Dispatch via claude -p|03 - Dispatch via `claude -p` — casos de uso e padrões]]
4. [[03-Dominios/IA/Claude Code/Time e Automação/04 - CLAUDE.md compartilhado|04 - CLAUDE.md compartilhado — o que vai no repo, o que fica local]]
5. [[03-Dominios/IA/Claude Code/Time e Automação/05 - Controle de custo|05 - Controle de custo — monitoramento, limites, ccusage]]
6. [[03-Dominios/IA/Claude Code/Time e Automação/06 - Segurança organizacional|06 - Segurança organizacional — o que nunca deixar o agente fazer]]
7. [[03-Dominios/IA/Claude Code/Time e Automação/07 - Onboarding de time|07 - Onboarding de time — introduzir Claude Code sem caos]]
8. [[03-Dominios/IA/Claude Code/Time e Automação/08 - Avaliando qualidade|08 - Avaliando qualidade do output — quando confiar, quando revisar]]

## Veja também

- [[03-Dominios/IA/Claude Code/index|Claude Code]] — tronco da trilha
- [[03-Dominios/IA/Claude Code/Workflows/index|Workflows]] — galho anterior
- [[03-Dominios/IA/Claude Code/Hooks e Guardrails/index|Hooks e Guardrails]] — guardrails que viram políticas organizacionais
```

- [ ] **Step 2: Verificar**

```bash
ls "03-Dominios/IA/Claude Code/Time e Automação/"
```

- [ ] **Step 3: Commit**

```bash
git add "03-Dominios/IA/Claude Code/Time e Automação/index.md"
git commit -m "feat(claude-code/g6): add Time e Automação index"
```

---

## Task 8: Atualizar `05 - Claude Code — terminal-first agent.md`

**Files:**
- Modify: `03-Dominios/IA/Agentes de Codificação/05 - Claude Code — terminal-first agent.md`

- [ ] **Step 1: Adicionar wikilink no "Veja também"**

Localize a seção `## Veja também` (próxima ao fim do arquivo) e adicione antes do primeiro item existente:

```markdown
- [[03-Dominios/IA/Claude Code/index|Trilha Claude Code]] — aprofundamento completo em 6 galhos: mental model, configuração, hooks, skills/MCP, workflows e automação
```

- [ ] **Step 2: Commit**

```bash
git add "03-Dominios/IA/Agentes de Codificação/05 - Claude Code — terminal-first agent.md"
git commit -m "feat(agentes-codificacao): link trilha Claude Code na nota 05"
```

---

## Task 9: Atualizar `14 - agents.md e configuração de projeto.md`

**Files:**
- Modify: `03-Dominios/IA/Agentes de Codificação/14 - agents.md e configuração de projeto.md`

- [ ] **Step 1: Adicionar wikilink no "Veja também"**

Localize a seção `## Veja também` e adicione:

```markdown
- [[03-Dominios/IA/Claude Code/Configuração/index|Configuração — Claude Code]] — aprofundamento em CLAUDE.md, settings.json, permissions e hierarquia de configuração
```

- [ ] **Step 2: Commit**

```bash
git add "03-Dominios/IA/Agentes de Codificação/14 - agents.md e configuração de projeto.md"
git commit -m "feat(agentes-codificacao): link galho Configuração na nota 14"
```

---

## Task 10: Atualizar `15 - MCP — o protocolo universal.md`

**Files:**
- Modify: `03-Dominios/IA/Agentes de Codificação/15 - MCP — o protocolo universal.md`

- [ ] **Step 1: Adicionar wikilink no "Veja também"**

Localize a seção `## Veja também` e adicione:

```markdown
- [[03-Dominios/IA/Claude Code/Skills e MCP/index|Skills e MCP — Claude Code]] — como usar MCP servers no Claude Code e criar servers customizados
```

- [ ] **Step 2: Commit**

```bash
git add "03-Dominios/IA/Agentes de Codificação/15 - MCP — o protocolo universal.md"
git commit -m "feat(agentes-codificacao): link galho Skills e MCP na nota 15"
```

---

## Task 11: Atualizar `12 - Multi-agent — workflows com múltiplos agentes.md`

**Files:**
- Modify: `03-Dominios/IA/Agentes de Codificação/12 - Multi-agent — workflows com múltiplos agentes.md`

- [ ] **Step 1: Adicionar wikilink no "Veja também"**

Localize a seção `## Veja também` e adicione:

```markdown
- [[03-Dominios/IA/Claude Code/Workflows/index|Workflows — Claude Code]] — padrões de multi-agent, sub-agents e sessões paralelas especificamente no Claude Code
```

- [ ] **Step 2: Commit**

```bash
git add "03-Dominios/IA/Agentes de Codificação/12 - Multi-agent — workflows com múltiplos agentes.md"
git commit -m "feat(agentes-codificacao): link galho Workflows na nota 12"
```

---

## Task 12: Atualizar `IA/index.md` — referenciar trilha Claude Code

**Files:**
- Modify: `03-Dominios/IA/index.md`

- [ ] **Step 1: Localizar a seção da Trilha 3**

Procure o bloco:

```
#### Trilha 3 — [[Agentes de Codificação]] (18 notas)
```

- [ ] **Step 2: Adicionar referência à trilha Claude Code após a descrição da Trilha 3**

Após a linha `**Quando ler:** após Trilhas 1-2. Onde a teoria vira prática diária.`, adicione:

```markdown

> [!tip] Aprofundamento
> Quer ir além do overview comparativo? [[03-Dominios/IA/Claude Code/index|Trilha Claude Code]] cobre em profundidade: mental model, configuração, hooks, skills/MCP, workflows e automação em 6 galhos (~50 notas).
```

- [ ] **Step 3: Commit**

```bash
git add "03-Dominios/IA/index.md"
git commit -m "feat(ia/index): add referência à trilha Claude Code"
```

---

## Próximos planos — notas atômicas por galho

Este plano cobre apenas o scaffolding. Cada galho tem seu próprio plano de execução:

| Plano | Conteúdo | Notas |
|-------|----------|-------|
| `2026-05-13-claude-code-g1-mental-model.md` | Galho 1: O loop agentic, leitura de codebase, tool use, context window, modos, compaction, custo, decisão | 8 |
| `2026-05-13-claude-code-g2-configuracao.md` | Galho 2: Hierarquia, CLAUDE.md anatomia, receitas, settings.json, permissions, aliases, .claude/, armadilhas | 8 |
| `2026-05-13-claude-code-g5-workflows.md` | Galho 5: Plan Mode, TDD, refactoring, debugging, code review, sessões paralelas, sub-agents, multi-agent, prompting, contexto | 10 |
| `2026-05-13-claude-code-g3-hooks.md` | Galho 3: Lifecycle, PreToolUse, PostToolUse, Stop, guardrails, meta-agente, segurança, debugging | 8 |
| `2026-05-13-claude-code-g4-skills-mcp.md` | Galho 4: Anatomia, processo vs domínio, criar skill, MCP overview, MCP servers, criar MCP, composição, time | 8 |
| `2026-05-13-claude-code-g6-time-automacao.md` | Galho 6: Headless, CI/CD, dispatch, CLAUDE.md time, custo, segurança org, onboarding, qualidade | 8 |

Ordem recomendada de execução: G1 → G2 → G5 → G3 → G4 → G6
