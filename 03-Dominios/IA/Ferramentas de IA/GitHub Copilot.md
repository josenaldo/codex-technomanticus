---
title: "GitHub Copilot"
created: 2026-04-01
updated: 2026-04-11
type: concept
progress: backlog
status: evergreen
tags:
  - ia
  - llm
  - ferramentas
  - copilot
publish: true
---

# GitHub Copilot

> Copilot foi o primeiro [[Dicionário de IA#Coding agent|coding assistant]] de IA que um dev normal podia usar em produção. Lançado em 2021, em 2026 virou um ecossistema completo: completions no editor, chat contextual, agent mode, workspace para features multi-arquivo, integração nativa com Pull Requests, GitHub Actions, e Issues. Se você vive no GitHub, Copilot é onde a IA aparece sem você precisar trocar de janela. Esta nota cobre as capabilities, como configurar bem (skills, instructions, chat modes), workflows reais, e quando usar Copilot em vez de (ou junto com) Claude Code. Para fundamentos de LLMs ver [[Anatomia dos LLMs|LLMs]]; para comparação geral ver [[Comparativo de LLMs]].

## O que é

**GitHub Copilot** é o assistente de IA oficial do GitHub (Microsoft), integrado em VS Code, Visual Studio, JetBrains IDEs, Neovim, Xcode (beta), e na própria plataforma web do GitHub. Usa **múltiplos modelos** por baixo — em 2026, o usuário pode escolher entre GPT (OpenAI), Claude (Anthropic) e Gemini (Google), dependendo do plano e da tarefa.

Copilot evoluiu de "autocompletar inteligente" para um ecossistema com múltiplos modos:

1. **Code Completion (ghost text)** — sugestões inline enquanto você digita.
2. **Chat** — conversa contextual dentro do IDE, com acesso ao código aberto.
3. **Edit mode** — mudanças em múltiplos arquivos guiadas por instrução.
4. **Agent mode** — agent autônomo que itera em tasks multi-step (equivalente ao Claude Code / Cursor).
5. **Copilot Workspace** — planejar e implementar features no nível do repositório.
6. **Copilot for PRs** — resumo de mudanças, revisão automática, sugestões de reviewer.
7. **Copilot CLI** — assistente no terminal para shell, git, operacional.
8. **Copilot in GitHub.com** — chat sobre issues, PRs, docs do repo.

Para um senior dev em um ambiente centrado em GitHub, **Copilot é a ferramenta menos atrítica**: você não sai do IDE, não troca de ferramenta, e o contexto (arquivos abertos, projeto, issues) aparece naturalmente.

## O que diferencia um senior usando Copilot

1. **Configura `.github/copilot-instructions.md` para cada projeto** — equivalente ao CLAUDE.md para Claude Code. Maior ROI.
2. **Usa chat modes customizados** para workflows recorrentes (code review, write tests, document).
3. **Escolhe o modelo certo** (GPT para completions rápidas, Claude para raciocínio, Gemini para multimodal).
4. **Conhece e usa `/slash commands`:** `/fix`, `/tests`, `/explain`, `/doc`, `/optimize`.
5. **Sabe referenciar contexto com `#file`, `#folder`, `#problem`** em chat.
6. **Domina agent mode e sabe quando usar vs chat tradicional.**
7. **Integra com GitHub Actions e PRs** para automation.
8. **Mantém skills compartilhadas no repositório** (`.github/chatmodes/`, `.github/prompts/`).
9. **Desabilita completions em arquivos sensíveis** (secrets, config) via `.copilotignore`.
10. **Mede impacto** — tempo economizado, acceptance rate, mudanças nos hábitos.

## Modos de operação em detalhe

### 1. Code Completion (ghost text)

A experiência original do Copilot. Sugestões inline à medida que você digita, geralmente 1-20 linhas. Você aceita com `Tab`.

**O que funciona bem:**

- Boilerplate (getters, setters, migrations, imports)
- Padrões claros (filter/map/reduce, loops comuns)
- Sintaxe de libraries conhecidas
- Testes unitários triviais

**O que falha:**

- Lógica de negócio não-trivial
- Algoritmos com requisitos específicos
- Código em áreas do projeto sem contexto nos arquivos abertos

**Acceptance rate** é a métrica clássica. Acima de 30% significa que está ajudando. Abaixo de 15% indica problema (completions ruins ou contexto insuficiente).

### 2. Chat

Painel lateral para conversar sobre o código. Aceita referências explícitas a arquivos, pastas, problemas, e comandos.

**Referências de contexto:**

- `#file:src/auth.ts` — um arquivo
- `#folder:src/components` — uma pasta
- `#problem:42` — um erro/warning do VS Code
- `#selection` — código selecionado no editor

**Slash commands:**

- `/explain` — explicar código selecionado
- `/fix` — sugerir correção para erro
- `/tests` — gerar testes
- `/doc` — gerar documentação
- `/new` — scaffold de projeto/arquivo
- `/optimize` — propor otimizações

Chat é onde a maior parte do uso diário acontece para tasks não-triviais.

### 3. Edit mode

Você descreve uma mudança, Copilot aplica em múltiplos arquivos com diff preview. Você aprova ou rejeita por arquivo.

**Use case:** "Adicione validação Zod nos endpoints em src/api/, retornando 400 em caso de erro". Copilot identifica os arquivos, propõe os diffs.

### 4. Agent mode

Modo mais autônomo. Copilot itera em uma task — lê código, edita, roda comandos, vê output, ajusta. Similar a Claude Code e Cursor Agent.

**Quando usar:**

- Features multi-arquivo que cruzam camadas
- Refactors amplos
- Bug fixes que exigem investigação

**[[Dicionário de IA#Guardrail|Guardrails]]:** confirmação antes de ações destrutivas, auto-approve configurável por comando, `max_steps` implícito.

### 5. Copilot Workspace

Planejamento no nível de repositório. Dado uma issue ou descrição, Copilot:

1. Explora o repo
2. Propõe plano em seções
3. Você revisa/ajusta
4. Copilot implementa
5. Abre PR

Mais ambicioso que agent mode. Útil para features onde o escopo é grande mas bem definido.

### 6. Copilot for PRs

Integração nativa com Pull Requests:

- **PR summary** automático
- **Review sugerido** com inline comments
- **Reviewer suggestion** baseado em código tocado
- **Q&A sobre o PR** em chat lateral

Útil especialmente quando revisando PRs grandes que você não escreveu.

### 7. Copilot CLI

Assistente no terminal:

```bash
gh copilot suggest "find all TODO comments in TypeScript files"
gh copilot explain "git rebase -i HEAD~5"
```

Útil quando você esquece syntax de `find`, `awk`, `jq`.

### 8. Copilot no GitHub.com

Chat sobre:

- Um repositório (architecture, onde está X)
- Uma PR (o que mudou, por quê)
- Uma issue (contexto)
- Seus repos em geral

Acessível via interface web, sem precisar clonar.

## Configuração — onde o senior gasta tempo

### `.github/copilot-instructions.md`

**O arquivo mais importante.** Lido automaticamente e injetado em todas as interações com Copilot em chat, edit e agent mode. Use para:

- Descrever a arquitetura
- Convenções de código
- Comandos de build/test
- Stack tecnológica
- Patterns a seguir / antipatterns

Formato simples, markdown livre. Similar ao CLAUDE.md.

```markdown
# Project instructions for Copilot

This is a Next.js 15 app with Server Components, Prisma, and Zod.

## Conventions
- TypeScript strict
- Zod at every boundary (API inputs, external responses)
- Server components by default, "use client" only when needed
- Tailwind + shadcn/ui for UI

## Architecture
- `src/app/` — App Router routes
- `src/lib/` — utilities and integrations
- `src/components/` — shared UI
- `src/db/` — Prisma schema and migrations

## Testing
- Vitest for unit tests
- Playwright for e2e
- Run: `pnpm test`, `pnpm test:e2e`
```

Boa prática: revisar este arquivo a cada feature grande ou refactor arquitetural. Desatualizado = Copilot ruim.

### Chat modes customizados

Em `.github/chatmodes/`, cada arquivo define um "mode" — conjunto de instruções + prompt base que você invoca em chat.

```markdown
---
name: security-review
description: Review code for security issues
---

You are a senior security engineer reviewing code for:
- Injection (SQL, XSS, command)
- Authentication/authorization flaws
- PII exposure
- Insecure deserialization
- Race conditions

For each issue, cite OWASP and provide severity (critical/high/medium/low).
```

Você invoca com `@security-review` no chat.

### Prompts customizados

Em `.github/prompts/`, prompts parametrizados reutilizáveis:

```markdown
---
name: write-test
description: Write test for selected function
---

Write a Vitest test for the selected function. Cover:
- Happy path
- Edge cases
- Error handling

Follow our test conventions in #file:src/test-helpers.ts
```

### `.copilotignore`

Arquivos excluídos de contexto/completion. Crítico para secrets, configs sensíveis, dados.

```text
.env*
secrets/**
*.pem
*.key
prisma/seed-data/**
```

### User settings

- **Model selection:** GPT-4.1, GPT-4o, Claude Sonnet 4.x, Gemini 2.5 — disponível em planos pagos.
- **Suggestions on/off por linguagem**
- **Telemetry** — opt-out respeitado
- **Public code filter** — evita sugestões que matchem código público conhecido (importante para licensing)

## Workflows reais — dia a dia de um senior

### Dev de feature

1. **Issue no GitHub descreve o feature.**
2. Abro no VS Code, chat @workspace: "explore #file:issue-description e proponha plano"
3. Reviso e ajusto o plano.
4. Chat em edit mode: "implemente o plano"
5. Copilot aplica diffs, eu reviso.
6. Rodo testes localmente.
7. PR automatizado com summary gerado pelo Copilot.
8. Review automático + humano.

### Bug fix

1. Erro no log de produção.
2. Chat: "`#file:error-log.txt` mostra esse erro. Procure em `#folder:src/` onde pode acontecer"
3. Copilot aponta suspeitos.
4. `/fix` no arquivo problemático.
5. `/tests` para adicionar regression test.

### Code review automation

1. GitHub Actions roda Copilot review automaticamente em toda PR.
2. Copilot deixa comentários inline com sugestões.
3. Reviewers humanos focam no arquitetural e trade-offs.

### CLI rápido

```bash
gh copilot suggest "docker compose up but only the api service with logs"
# → docker-compose up api --no-log-prefix
```

## Planos (2026)

| Plano | Preço | Features principais |
| --- | --- | --- |
| **Free** | $0 | Completions limitadas, chat limitado |
| **Individual (Pro)** | ~$10/mês | Completions ilimitadas, chat, edit, agent, models básicos |
| **Pro+** | ~$19/mês | Modelos premium (Claude Sonnet, Opus, Gemini Pro), workspace |
| **Business** | ~$19/user/mês | Admin controls, compliance, audit log |
| **Enterprise** | ~$39/user/mês | Customização da organização, private fine-tuning, SSO |

Estudantes verificados e manutenedores de projetos OSS populares têm acesso gratuito.

## Diferenciais vs Claude Code / Cursor

### Onde Copilot ganha

- **Integração nativa com GitHub:** Issues, PRs, Actions, GH.com.
- **Multi-IDE:** VS Code, JetBrains, Visual Studio, Xcode, Neovim.
- **Sem friction de setup:** instala extensão, pronto.
- **PR workflow automation:** review, summary, suggest.
- **Copilot Workspace:** planejamento no nível de repositório com UI específica.
- **Gratuito/barato** para muitos casos.

### Onde Claude Code/Cursor ganham

- **Profundidade de raciocínio em tarefas longas** (Claude Opus vs models default do Copilot).
- **Customização profunda** (skills, subagents, hooks, memory).
- **CLI puro** para workflows terminal-first.
- **Worktrees e isolation** nativas (Claude Code).
- **Controle fino sobre contexto** ([[Dicionário de IA#MCP (Model Context Protocol)|MCP]] servers, context management).

### Stack típica que se mostra produtiva

Usar **os dois juntos:**

- **Copilot** para completions inline (sempre ativo no IDE), review de PR, e chat rápido sobre arquivos abertos.
- **Claude Code** para tasks não-triviais, refactors, debugging profundo, workflows customizados via skills.

Não é "ou Copilot ou Claude Code". São complementares.

## Integração com GitHub Actions

Copilot pode ser invocado em workflows para automation:

```yaml
name: AI Review
on: pull_request

jobs:
  review:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: github/copilot-review-action@v1
        with:
          chatmode: security-review
          focus: "changed files only"
```

Útil para:

- Review automático de PRs antes de humanos
- Geração de release notes
- Tagging de issues
- Triagem automática

## Armadilhas comuns

### 1. Sem `copilot-instructions.md`

Copilot adivinha arquitetura → sugestões genéricas. **Fix:** escrever uma instruções decente.

### 2. Aceitar sugestões sem ler

Ghost text bonito com bug sutil. **Fix:** leia antes de `Tab`.

### 3. Chat sem contexto

Chat sem `#file` ou `#folder` = respostas genéricas. **Fix:** sempre ancorar em arquivos.

### 4. Public code filter desligado

Risco de licensing em código público. **Fix:** manter ligado em projetos comerciais.

### 5. Sem `.copilotignore`

Secrets vazando em prompts. **Fix:** ignorar env, keys, dados.

### 6. Agent mode em projetos desconhecidos

Agent faz changes em larga escala sem entender convenções. **Fix:** usar em projeto com instructions bem feita.

### 7. Modelo errado para a tarefa

GPT rápido onde Claude longo seria melhor. **Fix:** escolher modelo conscientemente quando o plano permite.

### 8. Ignorar hooks do Git / pre-commit

Copilot comita código que falha no linter. **Fix:** rodar lint/test local antes de commit; hooks não-bypass.

### 9. Workspace para tasks pequenas

Overhead desnecessário. **Fix:** chat/edit para tasks pequenas; workspace para features médias a grandes.

### 10. Sem revisar `.github/chatmodes/` do time

Skills viram legacy desatualizado. **Fix:** review trimestral.

## Como ganhar experiência prática

Esta nota é estrutura sobre Copilot. Para internalizar, prática é insubstituível. Três caminhos curados:

### Caminho 1 — copilot-instructions.md de alto ROI (1 semana)

Em projeto próprio que você trabalha:

1. Baseline: task não-trivial, observar output do Copilot.
2. Escrever `.github/copilot-instructions.md` rica (stack, convenções, comandos, antipatterns).
3. Re-rodar mesma task. Comparar qualidade.
4. Iterar baseado em gaps.

**Critério de sucesso:** entende empiricamente o ROI do arquivo de instructions; tem template próprio para próximos projetos.

### Caminho 2 — Chat modes + skills no Codex Technomanticus (2 semanas)

Construir biblioteca de chat modes em `.github/chatmodes/` e prompts em `.github/prompts/` para tarefas recorrentes:

- `note-review` — revisar nota Obsidian (estrutura, frontmatter, links)
- `commit-message` — gerar commit message no estilo do projeto
- `quartz-frontmatter` — adicionar/corrigir frontmatter para Quartz
- Opcional: `english-review` — revisar nota em inglês para fluência

Usar `#file`, `#folder` como referências de contexto. Iterar baseado em uso real.

**Critério de sucesso:** biblioteca em uso diário; economia mensurável de tempo.

### Caminho 3 — PR automation com GitHub Actions (quando aparecer)

Em projeto profissional, configurar Action que dispara Copilot review automatizado em todas as PRs com chatmode customizado para o tipo de revisão necessária. Iterar baseado em false positives e cobertura.

**Critério de sucesso:** automação rodando em produção, com qualidade ajustada para o time.

---

**Sugestão de ordem:** Caminho 1 → Caminho 2 → Caminho 3.

**Princípios universais:**

- **Completions são substrato:** sempre ligadas, mas não o principal benefício em 2026.
- **Chat contextual é onde está o ganho real.** `#file`, `#folder`, `#problem` são fundamentais.
- **Instructions bem feitas são 60% do valor.** Sem elas, Copilot é um GPT com menos contexto.
- **Public code filter sempre ligado** em projetos comerciais. Não vale o risco licensing.
- **Pair Copilot + Claude Code** é mais forte do que escolher um.

## How to explain in English

### Short pitch

"GitHub Copilot is where AI meets the GitHub-native developer. Completions in the editor, chat with project context, agent mode for multi-step tasks, PR integration, and Workspace for repo-level planning. The mature pattern in 2026 is using it alongside Claude Code — Copilot for the always-on inline completions and PR automation, Claude Code for the heavier, customized workflows. The highest-leverage config is `.github/copilot-instructions.md` — essentially CLAUDE.md for Copilot."

### Deeper version

"Copilot in 2026 is an ecosystem, not just completions. The capabilities that matter: inline ghost text for speed, chat with file/folder/problem references for focused questions, edit mode for targeted multi-file changes, agent mode for autonomous iteration, and PR-level automation — summaries, review comments, reviewer suggestions. Copilot CLI handles shell commands that would otherwise need a google search.

Configuration is where seniors separate from juniors. The high-leverage files are `.github/copilot-instructions.md` (architecture, conventions, commands), `.github/chatmodes/` (workflows like security review and test writing), and `.github/prompts/` (parameterized prompt templates). `.copilotignore` keeps secrets out of the context. Model selection — GPT, Claude, or Gemini — picked based on the task.

The strong pairing is Copilot with Claude Code rather than choosing one. Copilot is low-friction and always on in the IDE, great for daily work. Claude Code is where heavy refactors, deep debugging, and customized skill-driven workflows happen. The two complement each other."

### Phrases

- "Instructions file is higher ROI than any prompt engineering."
- "Chat with `#file` beats chat without context, every time."
- "Public code filter stays on. License risk isn't worth it."
- "Copilot plus Claude Code, not Copilot or Claude Code."
- "Agent mode is great in well-configured projects, risky in unknown ones."

### Key vocabulary

- completação de código → code completion
- texto fantasma → ghost text
- sugestão inline → inline suggestion
- modo chat → chat mode
- modo de edição → edit mode
- modo agente → agent mode
- espaço de trabalho → workspace
- instruções do projeto → project instructions
- referência de arquivo → file reference
- comando de barra → slash command

## Recursos

### Documentação

- [GitHub Copilot Docs](https://docs.github.com/en/copilot)
- [Copilot Customization Overview](https://code.visualstudio.com/docs/copilot/customization/overview)
- [Copilot Chat Cheat Sheet](https://docs.github.com/en/copilot/using-github-copilot/copilot-chat/github-copilot-chat-cheat-sheet)
- [Copilot Workspace](https://github.com/features/preview/copilot-workspace)

### Skills e instructions

- [Awesome Copilot](https://github.com/github/awesome-copilot) — curadoria oficial
- [Awesome Copilot Skills](https://github.com/github/awesome-copilot/tree/main/skills)
- [CopilotSkills](https://github.com/Oxilith/CopilotSkills)
- [Complete Guide to AGENTS.md](https://www.aihero.dev/a-complete-guide-to-agents-md)
- [Como reduzi em 70% o uso do context window no Copilot](https://www.linkedin.com/pulse/como-reduzi-em-70-o-uso-do-context-window-github-copilot-lemos-cycnf/)

### Blog e updates

- [GitHub Blog — Copilot tag](https://github.blog/tag/github-copilot/)
- [GitHub Next](https://githubnext.com/) — experimentos e features em preview

## Deep dives — Copilot arquitetura, research, evolução

### Histórico — de OpenAI Codex a Copilot 2026

- **2021 — Copilot lançamento:** Baseado em OpenAI Codex (GPT-3 fine-tuned em código). Primeiro AI coding assistant "mainstream".
- **2022 — Copilot for Business:** policy controls, telemetry opt-out, public code filter.
- **2023 — Copilot Chat:** GPT-4 no IDE. Chat contextual muda jogo para debugging e explicação.
- **2024 — Copilot Workspace e Agent mode:** Planning no nível de repositório, agent que itera em tasks.
- **2025 — Multi-model:** usuário pode escolher Claude ou Gemini em alguns planos. Skills customizadas.
- **2026 — Ecossistema maduro:** chat modes, prompts, CLI, PR automation, Actions integration.

### Como Copilot gerencia contexto no IDE

Copilot não manda todo seu código para o servidor a cada keystroke. O client (extension VS Code) tem heurísticas:

- **Files abertos** no editor (maior peso)
- **Files "relevantes"** baseado em imports, recently edited, git-related
- **Lint/problem context** quando disponível
- **`copilot-instructions.md`** injetado como system context
- **Chat history** da sessão

Isso tudo forma o "prompt" que vai ao LLM. Você pode ver parte via VS Code developer tools quando habilita verbose logging.

**Por que importa:** quando completions ficam ruins, muitas vezes é porque o contexto está errado — arquivo relevante fechado, ou um arquivo barulhento aberto. Feche arquivos irrelevantes.

### Awesome Copilot Skills e o ecosystem

GitHub mantém [awesome-copilot](https://github.com/github/awesome-copilot), um repositório curado de chat modes, prompts, e skills que a comunidade produz. Em 2026 é o lugar principal para descobrir workflows novos.

Formato padrão:

- **Chat modes** em `.github/chatmodes/`
- **Prompt files** em `.github/prompts/`
- **Instructions** em `.github/copilot-instructions.md`

### Copilot Workspace — o formato de plano

Copilot Workspace tem um formato específico de plano que o agent segue:

```text
Topic → Specs → Plan → Implementation → Tests
```

1. **Topic:** descrição de alto nível (da issue ou usuário).
2. **Specs:** requirements concretos extraídos.
3. **Plan:** steps detalhados, arquivos a tocar.
4. **Implementation:** execução com preview por arquivo.
5. **Tests:** validação.

Você pode revisar e editar cada stage. Mais estruturado que agent mode "free-form".

### GitHub Actions integration em detalhe

Copilot exposto via Actions permite automation:

```yaml
- uses: github/copilot-review-action@v1
  with:
    chatmode: security-review
    focus: changed files only
```

Casos práticos:

- Review automático de PRs
- Sumários de release
- Triagem automática de issues
- Documentação gerada em merge

## Casos comuns no mercado

Padrões frequentes em times usando Copilot em produção. Não são casos vividos pessoalmente — são armadilhas recorrentes documentadas em post-mortems, talks, e literatura técnica.

### Caso 1 — Completion que copiou código GPL

**Padrão observado:** public code filter desligado por config legada ou esquecimento. Copilot sugere função que é cópia quase literal de projeto GPL. Descoberto em code scan (FOSSology, similar) ou auditoria de licensing.

**Fix típico:**

- Public code filter obrigatório em config central.
- OSS license scan em CI.
- Policy para todo repo comercial.
- Treinamento do time.

**Lição:** licensing risk é real. Mitigação é config + scan.

### Caso 2 — Copilot sugerindo SQL injection

**Padrão observado:** dev aceita completion que concatena string em SQL. Code review pega antes do merge, ou pior — vai a produção.

**Fix típico:**

- Chat mode `security-review` rodando em toda PR que toca DB.
- Lint rule detectando string concatenation em queries.
- Cultura: "leia antes de `Tab`".

**Lição:** Copilot não é revisor de segurança. Adicione camadas.

### Caso 3 — copilot-instructions.md desatualizado

**Padrão observado:** projeto migra (ex: REST → GraphQL, framework antigo → novo). `copilot-instructions.md` não é atualizada junto. Copilot continua sugerindo padrões antigos por semanas até alguém notar — devs novos no time aceitam sem questionar.

**Fix típico:**

- Revisão trimestral do arquivo.
- Updates no mesmo PR que muda stack.
- Parte do onboarding: "leia e atualize copilot-instructions".

**Lição:** docs vivas > docs escritas uma vez.

### Caso 4 — Chat sem `#file` → respostas genéricas

**Padrão observado:** dev novo no time reclama que "Copilot chat é ruim". Investigação revela que está perguntando sem referenciar arquivos (`"como faço isso?"`). Chat infere mal o contexto.

**Fix típico:**

- Treinamento: sempre ancorar em `#file`, `#folder`, `#problem`.
- Cheat sheet no onboarding.
- Chat modes que forçam contexto específico.

**Lição:** Copilot chat funciona muito melhor com referências explícitas.

### Caso 5 — Agent mode em projeto desconhecido

**Padrão observado:** dev tenta agent mode do Copilot em projeto legacy sem `copilot-instructions.md`. Agent faz mudanças que violam convenções implícitas. PR grande, difícil de reverter corretamente.

**Fix típico:**

- Regra: agent mode só em projetos com instructions bem feita.
- Para legacy, começar com chat interativo até entender padrões.
- Review mais rigoroso para PRs gerados por agent.

**Lição:** agent mode precisa de contexto. Sem ele, é imprevisível.

## Exercícios hands-on

### Lab 1 — copilot-instructions.md de alto ROI

1. Projeto real que você trabalha.
2. Baseline: task não-trivial, observe output do Copilot.
3. Escreva `.github/copilot-instructions.md` rica.
4. Re-rode. Compare qualidade do output.
5. Itere.

### Lab 2 — Chat mode customizado

1. Identifique workflow recorrente (ex: code review focado em segurança).
2. Escreva `.github/chatmodes/security-review.md` com instructions.
3. Use em PRs reais por 1 semana.
4. Itere.

### Lab 3 — Copilot chat com referencias

Pratique referenciar contexto:

- `#file:src/auth.ts explain this function`
- `#folder:src/api summarize the endpoints`
- `#problem:0 fix this error`
- `@workspace search for usages of X`

Meça diferença em qualidade com/sem referências.

### Lab 4 — PR automation com Actions

1. Adicione action de code review automatizado.
2. Custom chat mode para o tipo de review do seu projeto.
3. Observe PRs reais.
4. Ajuste baseado em false positives.

### Lab 5 — Workspace em task real

1. Escolha feature de tamanho médio.
2. Use Copilot Workspace desde issue.
3. Revise cada stage (specs, plan, implementation).
4. Compare vs fazer manualmente.

## Veja também

- [[Anatomia dos LLMs|LLMs]]
- [[Context Engineering]]
- [[Anatomia de Agents|Agents]]
- [[Claude]]
- [[Codex]]
- [[Gemini]]
- [[Comparativo de LLMs]]
- [[03-Dominios/IA/index|Inteligência Artificial]]
- [[MCP]]
- [[Senda IA]]
