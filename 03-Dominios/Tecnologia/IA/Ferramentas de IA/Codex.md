---
title: "Codex"
created: 2026-04-01
updated: 2026-07-01
type: concept
fase: Iniciado
progress: backlog
status: evergreen
tags:
  - ia
  - llm
  - ferramentas
  - openai
  - codex
publish: true
---

# Codex

> [!abstract] TL;DR
> **[[Dicionário de IA#Coding agent|Coding agent]] cloud-native da OpenAI**: diferente de [[Dicionário de IA#Claude Code|Claude Code]] ou Copilot (que rodam no seu IDE local), Codex opera em um sandbox na nuvem, clona o repo, executa autonomamente, e retorna um PR pronto para review.
> O diferencial para um senior dev não é velocidade de digitação — é **paralelismo assíncrono**: você despacha 5 tasks independentes, fecha o laptop, e volta horas depois com 5 PRs. Nenhuma ferramenta local faz isso.
> Esta nota cobre o que Codex é em 2026 (diferente do "Codex 2021", que era apenas um modelo de linguagem), como usar na prática, trade-offs reais, e quando faz sentido adotar. Para comparação de ferramentas, ver [[Comparativo de LLMs]]; para o padrão de agents em geral, [[Anatomia de Agents|Agents]].

> [!question]- Codex substitui Claude Code ou são ferramentas complementares?
> São complementares com papéis distintos. Codex é cloud-based, assíncrono e ideal para tasks longas que podem rodar sem supervisão — implementar um feature bem especificado, dependency update, batch de refactors. Claude Code é local, interativo e ideal para fluxo contínuo onde você itera com o agente em tempo real — exploração de codebase, debugging, pair programming. Um senior típico usa Claude Code para trabalho diário e Codex para tasks paralelas de background enquanto trabalha em outra coisa.

## O que é

**Codex** em 2026 é o **coding agent cloud-native** da OpenAI. Essa é a encarnação atual do nome — o Codex original era um modelo (derivado de GPT-3) que alimentava a primeira versão do Copilot e foi descontinuado em 2023. Em 2024-2025 a OpenAI relançou "Codex" como **produto agent**, não como modelo.

### Capacidades principais

- **Receber tarefas em linguagem natural** via web UI, CLI, VS Code extension, ou API.
- **Executar em sandbox cloud isolado** — containers efêmeros com acesso ao repo.
- **Clonar e modificar repositórios GitHub** (com OAuth).
- **Rodar testes, builds, linters** no sandbox.
- **[[Dicionário de IA#PR-driven workflow|Abrir PRs automaticamente]]** com descrição gerada.
- **Processar múltiplas tasks em paralelo** — 5, 10, 20 tarefas simultâneas.
- **Codex Skills** — instruções reutilizáveis via `AGENTS.md`.
- **Integração com ChatGPT app** — pode ser invocado direto do app principal.
- **CLI local** (`codex`) — alternativa ao fluxo web quando você quer mais controle.

### O modelo por trás

Codex usa modelos OpenAI internos especializados em coding, derivados das famílias **GPT-4.x**, **o1** e **o3**. A OpenAI rotula de "Codex models" quando fine-tunados para tarefas agentic de código. Usuários não escolhem modelo diretamente na UI web; na API e CLI, pode-se selecionar entre variantes.

### As três modalidades de uso

1. **Codex Cloud (async)** — UI web ou ChatGPT, sandbox cloud, PR como output.
2. **Codex CLI (local)** — ferramenta no terminal, executa no seu ambiente local com sandbox leve.
3. **Codex em IDEs** — extension VS Code permite invocar tasks no cloud a partir do editor.

## O que diferencia um senior usando Codex

1. **Sabe quando usar Codex vs Claude Code vs Copilot.** Async/batch em Codex; interativo em Claude Code; inline em Copilot.
2. **Escreve `AGENTS.md` bem estruturado** — o equivalente ao CLAUDE.md para Codex.
3. **Escreve tasks com escopo claro** — Codex funciona melhor com descrições específicas do que com objetivos vagos.
4. **Delega em paralelo** tasks independentes para aproveitar a arquitetura async.
5. **Revisa cada PR gerado** — nunca merge sem human review, mesmo que todos os checks passem.
6. **Configura sandbox** com credentials apropriados (leituras de docs internos, acesso a CI, etc).
7. **Usa Codex Skills** para workflows recorrentes.
8. **Entende limites de sandbox** — não espera que Codex converse com serviços externos sem configuração.
9. **Mede custo por task** — Codex é cobrado por compute + tokens, pode ficar caro.
10. **Evita Codex para tarefas que exigem exploração interativa** — agent mode do Copilot ou Claude Code são melhores.

## Arquitetura e fluxo

```mermaid
flowchart TD
    Dev["👤 Developer\n1. Descreve task em linguagem natural\n'Add rate limiting to /api/v1/search'"]
    API["🌐 Codex UI / API\n2. Dispatcher cria sandbox container"]
    Sandbox["📦 Sandbox Container\n3. Clona repo · instala deps\n4. Lê AGENTS.md e código\n5. Planeja abordagem\n6. Edita arquivos\n7. Roda testes\n8. Itera se falhar"]
    PR["🔀 GitHub PR\n9. Abre PR com descrição + commits\n   + checks automáticos"]

    Dev --> API --> Sandbox --> PR
```

Sandbox é efêmero — destruído após task completa. Cada task começa do zero, sem estado persistente (a menos que configurado via artifacts).

## AGENTS.md — a configuração crítica

O análogo do `CLAUDE.md` ou `copilot-instructions.md`. Arquivo markdown na raiz do repo que Codex lê como contexto permanente.

Em 2026, **AGENTS.md virou padrão de facto** adotado também por outras ferramentas (alguns frameworks o suportam como formato comum).

```markdown
# Agents instructions for this repo

This is a Go microservice using Echo framework and sqlx with PostgreSQL.

## Stack
- Go 1.23
- Echo web framework
- sqlx for DB access
- Testify for tests
- golangci-lint for linting

## Commands
- `make test` — run all tests
- `make lint` — run linter
- `make build` — build binary
- `make migrate` — run migrations

## Conventions
- Errors wrapped with fmt.Errorf("context: %w", err)
- No global state; use dependency injection
- All handlers return (res, error); errors mapped by middleware
- Table-driven tests for units
- One package per domain concept

## Architecture
- `cmd/` — entry points
- `internal/api/` — HTTP handlers
- `internal/service/` — business logic
- `internal/repo/` — data access
- `internal/domain/` — types and pure logic
- `pkg/` — public libraries (rare)

## Antipatterns
- panic() in library code
- Ignoring error returns
- SQL string concatenation (use parameterized queries)

## Testing conventions
- Integration tests in `*_integration_test.go` with build tag
- Mock external services with httptest
- Target >70% coverage on internal/service and internal/api
```

**Dica crítica:** AGENTS.md bem feita transforma drasticamente a qualidade do output. Um dev sênior investe 1-2h escrevendo bem no início do projeto.

## Codex Skills

Skills são instruções reutilizáveis que vivem em `.codex/skills/` ou diretamente referenciadas em `AGENTS.md`. Formato similar a outras ferramentas (frontmatter + conteúdo).

```markdown
---
name: add-endpoint
description: Add new REST endpoint with validation, tests, and docs
---

When asked to add a new endpoint:

1. Define input/output types in internal/domain/
2. Write validation in internal/api/validators/
3. Implement handler in internal/api/handlers/
4. Add route in internal/api/routes.go
5. Write unit tests for handler
6. Write integration test if touches DB
7. Update OpenAPI spec in docs/openapi.yaml
8. Add example curl in README
```

Skills aparecem como menu para o agent descobrir por demanda.

## Workflows reais com Codex

### Workflow 1 — Tasks paralelas em batch

Tenho 5 issues "pequenas" no backlog. Em vez de fazer sequencial:

1. Abro ChatGPT ou Codex UI.
2. Crio 5 tasks em paralelo, uma por issue, cada uma com link para a issue.
3. Fecho laptop, vou almoçar.
4. 1-2h depois, 5 PRs prontos para review.
5. Reviso sequencialmente, aprovando ou pedindo mudanças.

Isso destrava paralelismo de forma que nenhuma ferramenta local consegue — você não está esperando nem interagindo.

### Workflow 2 — Refactor amplo

Refactor que toca 50 arquivos (renomear um conceito, migrar lib):

1. Escrevo task detalhada explicando o "antes" e "depois".
2. Codex explora o repo, gera plano.
3. Revisa plano, ajusta.
4. Executa no sandbox, roda testes.
5. Abre PR com diff completo.

O ganho vs fazer no meu laptop: Codex persiste sem interrupção, sem distração, e é fácil lançar múltiplos refactors independentes em paralelo.

### Workflow 3 — Bug triage

Lista de 10 bugs relatados. Cada um vira uma task no Codex. Cada task investiga, tenta reproduzir, e ou: (a) abre PR com fix se claro, ou (b) retorna análise com info útil para human debugging.

### Workflow 4 — Dependency update

"Atualize todos os packages de prod para last stable minor, rode testes, abra PR com changelog" — vira uma task Codex recorrente que pode ser agendada.

## Codex CLI

Versão local do Codex. Roda no seu terminal, em ambiente do seu host (com sandboxing leve via container/firejail). Útil quando você quer:

- Controle fino sobre ambiente
- Network restrito
- Trabalhar offline parcialmente
- Debug local antes de escalar para cloud

```bash
# Instalação
npm install -g @openai/codex

# Uso básico
codex
> Add a --dry-run flag to the migration command
```

Similar em espírito ao Claude Code, mas focado em tarefas autoconfinadas vs conversação contínua.

## Diferenças com alternativas

### Codex vs Claude Code

| Aspecto | Codex | Claude Code |
| --- | --- | --- |
| **Execução** | Cloud sandbox (async) ou CLI local | Local CLI interativo |
| **Interação** | Fire-and-forget, volta ao PR | Conversacional contínuo |
| **Paralelismo** | Natural, N tasks em paralelo | Sequencial (multi-window possível) |
| **Contexto** | Repo clonado no sandbox | Filesystem local persistente |
| **Memory** | Efêmera por task | Persistente entre sessões |
| **Output** | PR/diff | Edições locais + commits |
| **Modelo** | OpenAI (GPT-4.1, o1, o3) | Anthropic (Opus/Sonnet) |
| **Configuração** | AGENTS.md + skills | CLAUDE.md + skills + hooks + MCP |
| **Integração MCP** | Crescente | Nativa e madura |
| **Custo** | Por task (compute + tokens) | Por tokens da API |

### Codex vs Copilot

- **Copilot** é integrado ao IDE; **Codex** é fire-and-forget cloud.
- **Copilot** brilha em inline e chat contextual; **Codex** brilha em tasks async completas.
- **Copilot workspace** é o mais próximo do Codex dentro da família GitHub.

### Quando escolher Codex

- **Tarefas paralelas que você quer delegar e checkar depois.**
- **Você vive no ChatGPT app** (Codex está integrado nativamente).
- **Equipes grandes** onde async scale importa mais que interatividade.
- **Repos grandes** onde sandbox com recursos dedicados ajuda.
- **Integrações CI-first** — Codex pode ser invocado de Actions para tasks automáticas.

### Quando não escolher

- **Exploração interativa** — use Claude Code ou Copilot Agent.
- **Features onde você precisa guiar decisões arquiteturais em tempo real.**
- **Projetos que precisam de contexto persistente complexo** — Codex começa do zero toda task.
- **Ambientes air-gapped ou com data residency estrita** — cloud pode não encaixar.
- **Budget sensível** — compute + tokens em tasks longas pode acumular.

## Segurança e limites

### Sandbox

Cada task roda em container isolado:

- Sem acesso a secrets externos (a menos que configurados)
- Network limitada por padrão (npm install sim, api calls externas não)
- Filesystem restrito ao clone do repo
- Destruído ao fim da task

### Credentials

- OAuth com GitHub para acesso ao repo
- Secrets do repo (GitHub Actions secrets) disponibilizados conforme política
- Data retention configurável (enterprise plans)

### Limites

- Tempo máximo por task (minutos a hora, depende do plano)
- Número de tasks simultâneas
- Compute quota

### Preocupações comuns

- **Data residency:** código vai para servidores OpenAI. Enterprise plans oferecem controles.
- **Proprietary code:** OpenAI compromete a não treinar com código de clientes enterprise.
- **Supply chain:** packages instalados no sandbox podem ser maliciosos; sandbox protege o ambiente mas não o código que você vai mergear.
- **Acesso a docs internos:** requer configuração (MCP, tools customizadas).

## Armadilhas comuns

> [!warning] Task vaga sem acceptance criteria
> "Melhore a autenticação" é a pior task que você pode dar ao Codex. Sem critério de aceitação, o agente faz mudanças válidas mas não as que você precisava, e o PR review vira retrabalho. Task boa tem: o quê, onde, como validar. Exemplo: "Adicione rate limiting de 5 req/min por IP no endpoint `/api/auth/login`. Deve retornar 429 com Retry-After header. Testes: `test_rate_limit_login.py`."

> [!warning] Merge sem review humano por confiar nos testes
> CI verde não significa output correto. Codex gera código que passa nos testes existentes mas pode ter bugs sutis de lógica de negócio, edge cases não cobertos, ou escolhas de design que parecem OK mas contradizem padrões do projeto. Todo PR de Codex precisa de review humano — CI é o chão, não o teto.

> [!warning] Paralelizar tasks com dependências entre si
> Codex task A e task B editam os mesmos arquivos em paralelo → conflito de merge garantido. O agente não vê o que a outra instância está fazendo. Para tasks com dependências, serializar: A termina → review → merge → B começa. Paralelo só funciona com tasks genuinamente independentes (arquivos e lógica disjuntos).

## Como ganhar experiência prática

Esta nota é estrutura sobre Codex. Para internalizar, prática é insubstituível. Três caminhos curados:

### Caminho 1 — AGENTS.md de alto valor + task simples (1 semana)

Em um projeto próprio:

1. Baseline: dispatch task via Codex sem AGENTS.md. Observe qualidade.
2. Escreva AGENTS.md detalhada (stack, convenções, comandos, antipatterns).
3. Re-rode mesma task. Compare qualidade do PR.
4. Itere AGENTS.md baseado em gaps.

**Critério de sucesso:** entende empiricamente o ROI de AGENTS.md; tem template próprio para próximos projetos.

### Caminho 2 — Batch paralelo no Codex Technomanticus (1-2 semanas)

Identificar 4-5 tasks pequenas e independentes no próprio vault:

- Adicionar frontmatter padrão a notas que não têm
- Atualizar 4-5 MOCs específicas
- Reorganizar 3 pastas seguindo convenção

Dispatch em paralelo para Codex CLI ou Cloud. Review cada PR sequencialmente.

**Critério de sucesso:** experimenta async/paralelo na prática; tem opinião sobre quando vale e quando não vale.

### Caminho 3 — Codex em GitHub Actions em projeto profissional (quando aparecer)

Em projeto profissional, configurar Action que dispara Codex para: dependency update semanal, geração de release notes, triagem automática de issues. Medir impacto em throughput do time.

**Critério de sucesso:** automação rodando em produção, com governance e observabilidade.

---

**Sugestão de ordem:** Caminho 1 → Caminho 2 → Caminho 3.

**Princípios universais:**

- **AGENTS.md bem feito é a diferença entre "funciona" e "não funciona".**
- **Async é uma postura mental, não só técnica.** "O que posso delegar e checar depois?" é a pergunta certa.
- **Paralelização real destrava throughput.** 5 tasks em paralelo costumam render mais que 5 sequenciais — sem task-switching.
- **Custo escala com uso.** Fácil gastar $50-100/mês em workflows pequenos; enterprise pode chegar a milhares.
- **Human review sempre.** Codex erra de formas novas e criativas.

## How to explain in English

### Short pitch

"Codex is OpenAI's cloud-native coding agent. Unlike Claude Code or Copilot, it runs in a sandbox in the cloud, clones the repo, and returns a PR. The value is async and parallel work — fire off five tasks, close the laptop, come back to five PRs ready for review. It complements interactive tools rather than replacing them."

### Deeper version

"Codex has three modes: cloud async via the web UI or ChatGPT app, local CLI for more controlled environments, and IDE integrations. Each task runs in an isolated container — clone, install deps, read AGENTS.md, plan, execute, open a PR. No persistent state between tasks; each one starts fresh.

Where Codex wins is async scale. Five small issues in the backlog? Dispatch five tasks in parallel, review PRs later. A 60-file refactor? Write a detailed task and let Codex grind while doing other work. It's a different posture from interactive coding — fire, forget, review.

The configuration that matters is AGENTS.md, which is becoming something of a standard across tools — similar in role to CLAUDE.md or copilot-instructions.md. Good AGENTS.md means Codex understands architecture, conventions, and commands without re-explaining every time.

The limits to be clear on: no persistent context between tasks, sandbox has restricted network, and pricing is compute plus tokens — long complex tasks can add up. And human-review every PR, because agents fail in creative ways that CI doesn't catch."

### Talking points

- "Async and parallel is the killer feature. Not interactive speed."
- "AGENTS.md is standard now — invest in it."
- "Always human-review, even when all checks pass."
- "Codex complements Claude Code and Copilot, it doesn't replace them."
- "Sandbox limits are features — they keep your host clean."

### Key vocabulary

- agente de código → coding agent
- caixa de areia → sandbox
- execução assíncrona → asynchronous execution
- tarefa em lote → batch task
- paralelização → parallelization
- efêmero → ephemeral
- clonagem de repositório → repository cloning
- contêiner isolado → isolated container

## Recursos

### Oficial

- [OpenAI Codex](https://openai.com/codex/) — página oficial
- [Codex Docs](https://developers.openai.com/codex/)
- [Codex Skills](https://developers.openai.com/codex/skills/)
- [Codex CLI](https://github.com/openai/codex) — projeto open source
- [Agents.md guide](https://www.aihero.dev/a-complete-guide-to-agents-md)

### Blogs e análises

- [Pragmatic Engineer — AI tools](https://newsletter.pragmaticengineer.com/)
- [Simon Willison — OpenAI posts](https://simonwillison.net/tags/openai/)

## Deep dives — Codex arquitetura, sandbox, history

### Linha do tempo do nome "Codex"

- **2021 — "Codex" original:** modelo GPT-3 fine-tuned em código público. Alimentou a primeira versão do Copilot.
- **2022 — descontinuação:** OpenAI retirou Codex como produto separado; modelos seguintes foram nomeados GPT-4, etc.
- **2024-2025 — "Codex" relançado:** não como modelo, mas como **coding agent cloud**. Usa modelos internos (GPT-4.1, o1, o3) especializados em tarefas agentic.

Isso confunde muita gente. "Codex" em 2026 é produto agent, não modelo.

### Arquitetura sandbox

Cada task Codex roda em container isolado. Pipeline típico:

1. **Task dispatch:** user cria task via UI/API/CLI.
2. **Container spawn:** container efêmero (tipicamente Docker/Firecracker).
3. **Repo clone:** shallow clone do branch especificado.
4. **Dependency install:** detecta package manager (npm, pip, go mod, cargo) e instala deps.
5. **AGENTS.md read:** parser injeta instructions no context.
6. **Agent loop:** [[Dicionário de IA#ReAct|ReAct]]-style com tools do sandbox.
7. **Test run:** se configurado, roda testes.
8. **Commit + PR:** push do branch e abertura de PR com descrição gerada.
9. **Container destroy:** tudo efêmero.

**Limitações do sandbox:**

- Sem acesso a recursos fora do sandbox (a menos que configurado).
- Network restrita (npm install sim; arbitrary API calls não por padrão).
- Filesystem apenas dentro do container.
- Tempo máximo por task (configurável).

### AGENTS.md como padrão emergente

`AGENTS.md` surgiu com Codex mas está virando padrão de facto cross-tool. Em 2026, vários frameworks aceitam o mesmo formato.

**Por que virou padrão:**

- Formato é markdown simples, tool-agnostic.
- Permite que um repo funcione com Codex, Cursor, Claude Code via leitura do mesmo arquivo.
- Comunidade gravitou em torno via awesome-lists.

Ver [Complete Guide to AGENTS.md](https://www.aihero.dev/a-complete-guide-to-agents-md).

### Async workflow mental model

Codex requer uma mudança de postura. Interactive tools (Claude Code, Copilot) são "pair programming". Codex é "delegate and review". Isso afeta:

- **Como você escreve tasks:** precisa ser auto-contida, sem contexto de conversa.
- **Como você paralellliza:** fire-and-forget, volta quando pronto.
- **Como você review:** review de PRs, não supervisionado em tempo real.

Senior devs que adotam bem Codex mudam hábitos para aproveitar async.

## Casos comuns no mercado

Padrões frequentes em times usando Codex em produção. Não são casos vividos pessoalmente — são armadilhas recorrentes documentadas em post-mortems, talks, e literatura técnica.

### Caso 1 — Task vaga virou PR ruim

"Melhore o módulo de logging" → Codex fez 40 mudanças aleatórias que misturavam style, imports, e refactor estrutural. PR inviável de revisar.

**Fix:**

- Tasks sempre com escopo claro + acceptance criteria.
- Template de task no wiki do time.
- "Se sua task tem menos de 3 sentenças, é vaga demais."

**Lição:** qualidade da task = qualidade do PR.

### Caso 2 — Over-aggressive validation breaking clients

**Padrão observado:** task "add input validation" aplica validação agressiva demais a endpoint legacy. Campos opcionais com `null` passam a ser rejeitados. Quebra clientes antigos em produção após merge — CI passou (testes não cobriam esse caso).

**Fix típico:**

- Testes de regressão contra contrato público.
- Review manual semântico, não só checks automatizados.
- Label `breaking-change` nos PRs que mudam contratos.

**Lição:** CI passing != safe. Human review semântico sempre.

### Caso 3 — Tasks paralelas conflitando

**Padrão observado:** time despacha 8 tasks em paralelo. Algumas delas tocam arquivos sobrepostos. Maioria dos PRs auto-mergeia após review independente, alguns falham com conflict irresolvível, lições só aparecem na hora do merge.

**Fix típico:**

- Serializar tasks com overlap de path.
- "Path lock" manual no planejamento.
- CI que detecta potential path conflicts entre PRs abertos.

**Lição:** paralelismo tem custo de coordenação. Não ignore.

### Caso 4 — AGENTS.md desatualizado

**Padrão observado:** refactor grande muda convenções do projeto. AGENTS.md fica desatualizada. Codex continua produzindo código no estilo antigo por semanas até alguém notar.

**Fix típico:**

- Policy: AGENTS.md faz parte de todo refactor arquitetural.
- Review mensal do arquivo.
- PR template inclui checkbox "AGENTS.md atualizada se necessário".

### Caso 5 — Cost explosion com modelo premium

**Padrão observado:** task complexa com extended thinking (o3) custa $25+ sozinha. Dev não sabia que estava usando o3. Task não era crítica. Bill do mês surpreende.

**Fix típico:**

- Budget per task alert.
- Default para GPT-4.1; o3 explicit opt-in.
- Cost dashboard por dev/feature.

**Lição:** Codex com modelos premium pode acumular rápido.

## Exercícios hands-on

### Lab 1 — AGENTS.md de alto valor

1. Projeto real.
2. Baseline: task via Codex sem AGENTS.md.
3. Escreva AGENTS.md detalhada.
4. Re-rode task. Compare qualidade do PR.

### Lab 2 — Task paralela batch

1. 5 issues pequenas e independentes.
2. Delegue todas em paralelo para Codex.
3. Review cada PR sequencialmente.
4. Meça throughput vs fazer sequencial manualmente.

### Lab 3 — Refactor com spec clara

1. Refactor real de tamanho médio (10-30 arquivos).
2. Escreva spec detalhada: before/after, acceptance criteria, out of scope.
3. Deleguê para Codex.
4. Review o PR. Avalie.

### Lab 4 — Codex CLI local

1. Instale Codex CLI.
2. Use em workflow local por alguns dias.
3. Compare com Claude Code.
4. Documente diferenças de UX e output.

### Lab 5 — GitHub Actions com Codex

1. Configure action que dispara Codex para: dependency update semanal.
2. Automated review de PRs labeled "review-me".
3. Semana de observação.
4. Ajuste skills para qualidade.

## Como explicar em inglês

*"Codex is OpenAI's cloud-based coding agent — it receives a task in natural language, clones your repo in an isolated sandbox, executes the work autonomously, and returns a pull request. It's best for long, well-specified tasks you can run in the background while you do other work."*

| Português | Inglês |
|---|---|
| agente de código | coding agent |
| tarefa assíncrona | async task |
| sandbox isolado | isolated sandbox |
| critério de aceitação | acceptance criteria |
| tarefa auto-contida | self-contained task |
| revisão humana | human review |
| tarefas paralelas | parallel tasks |
| atualização de dependência | dependency update |
| orçamento por tarefa | per-task budget |
| permissões de rede | network allowlist / network permissions |

## O que vem a seguir

Depois de entender Codex como agente cloud assíncrono, o próximo contraste útil é o [[GitHub Copilot]] — a abordagem da Microsoft/OpenAI para assistência in-editor, muito mais restrita em contexto mas com adoção massiva em times que vivem no VS Code. Para fechar o mapa de ferramentas, o [[Comparativo de LLMs]] coloca Claude, GPT, Gemini e os modelos open-source lado a lado em critérios práticos de escolha.

## Veja também

- [[Anatomia dos LLMs|LLMs]]
- [[Anatomia de Agents|Agents]]
- [[Context Engineering]]
- [[Claude]]
- [[GitHub Copilot]]
- [[Gemini]]
- [[Comparativo de LLMs]]
- [[03-Dominios/Tecnologia/IA/index|Inteligência Artificial]]
- [[MCP]]
- [[Senda IA]]
