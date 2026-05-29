---
title: "O harness como terceira camada — código, testes, harness"
type: concept
progress: backlog
publish: true
created: 2026-05-25
updated: 2026-05-25
status: seedling
tags:
  - claude-code
  - mental-model
  - harness
  - configuracao
  - arquitetura
---

# O harness como terceira camada — código, testes, harness

> [!abstract] TL;DR
> O **harness** é a configuração que envolve o modelo — CLAUDE.md hierárquico, hooks, skills, plugins, MCP servers, integração LSP e subagents — e determina a performance do [[Dicionário de IA#Claude Code|Claude Code]] tanto quanto o modelo escolhido. A tese da Anthropic é dura: focar em benchmarks de modelo sem investir no harness produz resultados aquém do possível. Esta nota ancora os 6 galhos da trilha como componentes do harness e introduz três temas órfãos: manutenção do harness em ciclos de 3-6 meses, drift de regras escritas pra modelos antigos, e ownership organizacional (DRI ou "agent manager").

## O que é

Tradicionalmente, um codebase tem duas camadas: **código** e **testes**. O playbook da Anthropic sobre Claude Code em codebases grandes propõe uma terceira: **o harness**. É o conjunto versionado de artefatos que configura como o agente percebe e age no codebase.

A tese central, em uma frase do próprio post:

> "The ecosystem built around the model — the harness — determines how Claude Code performs more than the model alone."

Isso muda a pergunta de "qual modelo usar?" pra "como configurar a sessão pra esse modelo render?". Não substitui a primeira pergunta — soma a ela.

## Os 7 componentes do harness

Cinco extension points "core" + dois capacitadores. Cada um já é coberto em profundidade num galho desta trilha:

| Componente | Função | Coberto em |
|---|---|---|
| **CLAUDE.md** | Contexto carregado em toda sessão; hierárquico (raiz + subdiretórios) | [[03-Dominios/IA/Claude Code/Configuração/index\|Configuração]] |
| **Hooks** | Scripts em eventos do ciclo de vida; guardrails e self-improvement | [[03-Dominios/IA/Claude Code/Hooks e Guardrails/index\|Hooks e Guardrails]] |
| **Skills** | Expertise on-demand, glob-scoped, progressive disclosure | [[03-Dominios/IA/Claude Code/Skills e MCP/index\|Skills e MCP]] |
| **Plugins** | Bundles de skills+hooks+MCP distribuídos via marketplace | [[03-Dominios/IA/Claude Code/Skills e MCP/index\|Skills e MCP]] |
| **MCP servers** | Conexões com tools, dados e APIs internas | [[03-Dominios/IA/Claude Code/Skills e MCP/index\|Skills e MCP]] |
| **LSP integrations** | Navegação por símbolo (vs grep por string); nativo no Claude Code desde 2026 via *code-intelligence plugin* | — não coberto ainda na trilha |
| **Subagents** | Instâncias isoladas pra separar exploração de edição | [[03-Dominios/IA/Claude Code/Workflows/07 - Sub-agents e dispatch\|Workflows/07]] |

A ordem importa: o post recomenda construir top-down nessa sequência. Cada camada se apoia na anterior — pular CLAUDE.md pra começar com MCP server custom é tentar otimizar antes do básico funcionar.

## Os três padrões organizacionais

Além dos componentes, o post identifica três padrões que apareceram em todos os deploys bem-sucedidos.

### 1. Codebase navegável em escala

[[03-Dominios/IA/Claude Code/Mental Model/02 - Como Claude Code lê um codebase|Claude navega via grep + leitura]], não via índice central. Em escala grande, isso depende de **escopo**:

- CLAUDE.md raiz só com ponteiros + gotchas críticos
- Subdirectórios com convenções locais (carregam aditivamente)
- Comandos de teste/lint escopados por subdirectório
- `.claudeignore` versionado pra excluir generated/build/third-party
- Inicializar Claude no subdirectório do trabalho, não na raiz

### 2. Manutenção ativa do harness (3-6 meses)

Este é o tema mais subexplorado em conteúdo público sobre Claude Code: **o harness envelhece**.

> "Instructions written for your current model can work against a future one."

Exemplo concreto do post: um hook que interceptava writes pra forçar `p4 edit` em codebase Perforce ficou redundante quando Claude Code ganhou modo Perforce nativo. Pior — virou ruído.

A heurística: revisar config a cada **3-6 meses**, e atenção dobrada após release de novo modelo. Sinais de drift:
- Hooks que existem pra compensar limitação que o modelo atual não tem mais
- Regras de CLAUDE.md que prescrevem patterns que o modelo atual já segue por padrão
- Skills duplicando capability que virou nativa

### 3. Ownership organizacional

Adoção bottom-up gera entusiasmo, mas fragmenta sem alguém pra **centralizar o que funciona**. O post identifica três níveis:

- **Time dedicado** (ideal em org grande) — DevEx/DevProd construindo o harness antes do rollout
- **"Agent manager"** — papel emergente híbrido PM/engenheiro
- **DRI** (mínimo viável) — uma pessoa com autoridade sobre settings, permissions, marketplace de plugins, convenções de CLAUDE.md

Sem isso, "good setups stay tribal" — cada dev evolui o próprio e a org não aprende.

## Em escala individual

O playbook foi escrito pra orgs com milhares de devs, mas os princípios modulam pra contextos menores. Tomando como exemplo o [MedEspecialista](https://josenaldo.com.br/projects/medespecialista-platform), uma plataforma multi-repo (api, backend, admin, frontend) mantida por um senior dev solo, o padrão observado é:

- **Hub-and-spoke, não simétrico**: harness denso no repo que concentra complexidade arquitetural (`api/`: ~50 skills específicas, hooks de validação, subagents read-only, MCP Postgres + Playwright), mínimo nos outros (CLAUDE.md curto). Faz sentido — o ROI de skills detalhadas é proporcional à frequência de mudança no domínio.
- **DRI = a mesma pessoa**: não há "agent manager" nem time. Vantagem: zero overhead de coordenação. Custo: vulnerabilidade a bus factor 1 e ausência de revisão externa do harness.
- **LSP com nuance**: desde 2026 o Claude Code tem LSP **nativo**, configurável via *code-intelligence plugin* com bloco `lspServers` apontando pro language server local — a pergunta "via MCP?" ficou obsoleta (servers como `serena` e `cclsp` cobrem o mesmo terreno com mais infra pra manter). O marketplace oficial da Anthropic ship só `clangd-lsp` (C/C++) e `csharp-lsp` (C#) — sinal claro de onde a Anthropic vê maior ROI. Pra TypeScript o ganho é incremental (find-references cross-file, símbolos exportados); pra JavaScript sem tipos, é onde brilha de verdade — go-to-definition em `require('../../...')` colapsa em uma chamada o que era grep+leitura+trace. Custo de experimento é baixo (~1h pra um plugin local de ~15 linhas), o que muda a equação mesmo em escala solo.
- **Plugin (como bundle)**: só compensa quando o harness vai ser distribuído pra outras pessoas; pra setup pessoal, skills + hooks soltos resolvem.
- **Manutenção é mais barata mas igualmente necessária**: o ciclo de 3-6 meses se aplica, só que com escopo menor — uma sessão de revisão, não um sprint.

A lição: dos 7 componentes, **5 têm ROI alto mesmo em escala individual** (CLAUDE.md, hooks, skills, MCP, subagents). LSP entra quando o codebase tem bolsão de código não-tipado ou multi-linguagem; plugin só quando há audiência pra distribuir.

### O ciclo de manutenção em ação

O próprio gatilho da reavaliação do harness do MedEspecialista ilustra o padrão da Anthropic em escala individual: post novo (mai/2026) introduz componente ainda não adotado → revisão fora do ciclo regular de 3-6 meses (sinal "vale checar pós-release/publicação relevante") → avaliação registrada com critério de reversão explícito (2 semanas de uso real; se find-references / go-to-definition não substituir traces multi-grep, desinstala sem culpa). É **review + DRI** funcionando — só que o "agent manager" e o "engenheiro" são a mesma pessoa.

## Armadilhas

**Achar que modelo basta.** Trocar pra modelo mais novo sem mexer no harness deixa ganho na mesa — e às vezes regride performance se regras antigas conflitam com o modelo novo.

**Inflar CLAUDE.md.** Carregar expertise reusável no CLAUDE.md em vez de em skills polui toda sessão. Regra: CLAUDE.md = o que se aplica a *toda* tarefa neste path. Resto vai pra [[03-Dominios/IA/Claude Code/Skills e MCP/02 - Skills de processo vs domínio|skill]].

**Pular pra MCP server custom antes do básico.** "Building MCP connections before the basics are working" é antipattern explícito no post. Sem CLAUDE.md e skills funcionando, MCP só amplifica o caos.

**Harness eterno.** Configuração não é set-and-forget. Sem ciclo de revisão, em 12 meses metade das regras é peso morto.

**Adoção sem ownership.** Em time, deixar cada dev evoluir o próprio harness produz N versões fragmentadas e nenhuma compartilha aprendizado. Em solo, a ausência de revisão externa cria pontos cegos.

## Fontes

- [[02-Glosas/Promovidas/2026/2026-claude-code-large-codebases-best-practices|How Claude Code works in large codebases — Anthropic Applied AI Team]]

## Veja também

- [[03-Dominios/IA/Claude Code/index|Claude Code]] — tronco da trilha; os 6 galhos materializam os componentes do harness
- [[03-Dominios/IA/Claude Code/Mental Model/02 - Como Claude Code lê um codebase|02 - Como Claude Code lê um codebase]] — por que o harness importa: o agente navega, não indexa
- [[03-Dominios/IA/Claude Code/Configuração/02 - CLAUDE.md anatomia|CLAUDE.md anatomia]] — componente mais visível do harness
- [[03-Dominios/IA/Claude Code/Time e Automação/index|Time e Automação]] — onde os padrões organizacionais (DRI, agent manager) aprofundam
- [[03-Dominios/IA/Claude Code/Workflows/11 - Estratégias estruturais de contexto/index|Estratégias estruturais de contexto]] — sub-galho complementar sobre layout do codebase pro agente
