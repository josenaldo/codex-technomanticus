---
title: "O harness como terceira camada — código, testes, harness"
type: concept
progress: backlog
publish: true
created: 2026-05-25
updated: 2026-06-19
status: growing
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

[[962d850e52b48c08de3e51ccb37098ef_MD5.jpg|Open: Pasted image 20260619100614.png]]
![[962d850e52b48c08de3e51ccb37098ef_MD5.jpg]]
## Os 7 componentes do harness

Cinco extension points "core" + dois capacitadores. Cada um já é coberto em profundidade num galho desta trilha:

| Componente | Função | Coberto em |
|---|---|---|
| **CLAUDE.md** | Contexto carregado em toda sessão; hierárquico (raiz + subdiretórios) | [[03-Dominios/Tecnologia/IA/Claude Code/Configuração/index\|Configuração]] |
| **Hooks** | Scripts em eventos do ciclo de vida; guardrails e self-improvement | [[03-Dominios/Tecnologia/IA/Claude Code/Hooks e Guardrails/index\|Hooks e Guardrails]] |
| **Skills** | Expertise on-demand, glob-scoped, progressive disclosure | [[03-Dominios/Tecnologia/IA/Claude Code/Skills e MCP/index\|Skills e MCP]] |
| **Plugins** | Bundles de skills+hooks+MCP distribuídos via marketplace | [[03-Dominios/Tecnologia/IA/Claude Code/Skills e MCP/index\|Skills e MCP]] |
| **MCP servers** | Conexões com tools, dados e APIs internas | [[03-Dominios/Tecnologia/IA/Claude Code/Skills e MCP/index\|Skills e MCP]] |
| **LSP integrations** | Navegação por símbolo (vs grep por string); nativo no Claude Code desde 2026 via *code-intelligence plugin* | — não coberto ainda na trilha |
| **Subagents** | Instâncias isoladas pra separar exploração de edição | [[03-Dominios/Tecnologia/IA/Claude Code/Workflows/07 - Sub-agents e dispatch\|Workflows/07]] |

A ordem importa: o post recomenda construir top-down nessa sequência. Cada camada se apoia na anterior — pular CLAUDE.md pra começar com MCP server custom é tentar otimizar antes do básico funcionar.

## Dois cortes do mesmo harness

A lista de 7 componentes acima é um corte **autoral**: "que artefatos eu escrevo pra configurar o Claude Code?". Em 2026 a academia formalizou um corte **funcional** do mesmo objeto — *"que funções o harness precisa prover?"*. Vale guardar os dois, porque eles se iluminam.

O survey *Externalization in LLM Agents* (arXiv:2604.08224, abr/2026) decompõe a cognição externalizada em três dimensões — **Memory** (estado), **Skills** (procedimento) e **Protocols** (contratos de interação) — e define o harness não como uma quarta dimensão, mas como **o runtime que hospeda as três** e provê os mediadores (sandboxing, observabilidade, compressão, avaliação, approval loops, orquestração de sub-agentes). É a mesma figura, vista de cima: onde a Anthropic lista *o que você edita*, o survey nomeia *o que aquilo serve*.

| Componente autorável (Anthropic) | Função que ele encarna (survey) |
|---|---|
| CLAUDE.md, MCP servers | Memory + Protocols (contexto e contratos com dados/tools) |
| Skills, plugins | Skills (procedimento especializado) |
| Hooks | Mediadores (approval loops, guardrails) |
| Subagents | Orquestração de sub-agentes (mediador) |
| LSP | Protocols (contrato agente↔código) |

> [!info] E há mais de dois cortes
> Existem pelo menos quatro taxonomias concorrentes do harness em 2026 (survey de 6 dimensões; Memory/Skills/Protocols; os 11 aspectos dos NLAHs; o CAR — Control/Agency/Runtime), e **nenhuma venceu**. O tratamento tool-agnóstico desse debate — e por que conviver com as quatro lentes é mais útil que escolher uma — está em [[03-Dominios/Tecnologia/IA/Anatomia de Agents/11 - Harness engineering — a terceira camada|Harness engineering — a terceira camada]]. Esta nota é a **instanciação concreta** daquele conceito num harness real.

## Os três padrões organizacionais

Além dos componentes, o post identifica três padrões que apareceram em todos os deploys bem-sucedidos.

### 1. Codebase navegável em escala

[[03-Dominios/Tecnologia/IA/Claude Code/Mental Model/02 - Como Claude Code lê um codebase|Claude navega via grep + leitura]], não via índice central. Em escala grande, isso depende de **escopo**:

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

## A versão acadêmica da tese: ganhos harness-sensitive

A frase da Anthropic que abre esta nota — *"the harness determines performance more than the model alone"* — ganhou em 2026 uma formulação acadêmica afiada, no preprint *Harness Engineering for Language Agents* (a proposta **CAR** — Control/Agency/Runtime). O argumento: muito do ganho de performance que se credita a um modelo novo é, na verdade, **atribuível à camada de harness** — *"many reported agent gains may be partly harness-sensitive rather than purely model-driven"*.

Por que isso deveria mudar como você lê um leaderboard? Porque quando o "Modelo X v2" sobe pontos no SWE-bench, o ranking não diz quanto veio do modelo e quanto veio do scaffold em volta. Os autores propõem um artefato leve de reporte — o **HarnessCard** — defendendo que *"progress in language agents should report not only the model, but also the harness layer that turns capability into governed action"*.

A implicação prática para quem opera Claude Code: ao comparar dois setups, **fixe o harness** antes de atribuir uma diferença ao modelo. Um eval que troca modelo *e* config ao mesmo tempo está medindo uma variável confundida.

> [!caution] Honestidade sobre a fonte
> CAR e HarnessCard vêm de um preprint **não peer-reviewed** — é posição argumentada, não achado validado. O ponto, porém, ecoa o que a própria Anthropic afirma em prosa: o harness é variável de primeira ordem, não detalhe de implementação.

## Armadilhas

**Achar que modelo basta.** Trocar pra modelo mais novo sem mexer no harness deixa ganho na mesa — e às vezes regride performance se regras antigas conflitam com o modelo novo.

**Inflar CLAUDE.md.** Carregar expertise reusável no CLAUDE.md em vez de em skills polui toda sessão. Regra: CLAUDE.md = o que se aplica a *toda* tarefa neste path. Resto vai pra [[03-Dominios/Tecnologia/IA/Claude Code/Skills e MCP/02 - Skills de processo vs domínio|skill]].

**Pular pra MCP server custom antes do básico.** "Building MCP connections before the basics are working" é antipattern explícito no post. Sem CLAUDE.md e skills funcionando, MCP só amplifica o caos.

**Harness eterno.** Configuração não é set-and-forget. Sem ciclo de revisão, em 12 meses metade das regras é peso morto.

**Adoção sem ownership.** Em time, deixar cada dev evoluir o próprio harness produz N versões fragmentadas e nenhuma compartilha aprendizado. Em solo, a ausência de revisão externa cria pontos cegos.

## Fontes

- [[02-Glosas/Promovidas/2026/2026-claude-code-large-codebases-best-practices|How Claude Code works in large codebases — Anthropic Applied AI Team]]
- [[02-Glosas/2026-ai-agent-harness-5-core-pillars|What is an AI Agent Harness? 5 Core Pillars — Duc Nguyen (AIQuinta)]] — a analogia CPU/SO e os 5 pilares operacionais
- **Externalization in LLM Agents** — [arXiv:2604.08224](https://arxiv.org/html/2604.08224v1) (abr/2026). Decomposição funcional Memory/Skills/Protocols + harness-runtime; progressão weights→context→harness. *Preprint.*
- **Harness Engineering for Language Agents (CAR)** — [preprint 202603.1756](https://www.preprints.org/manuscript/202603.1756) (abr/2026). Tese "harness-sensitive gains" e proposta HarnessCard. *Preprint, não peer-reviewed.*

## Veja também

- [[03-Dominios/Tecnologia/IA/Anatomia de Agents/11 - Harness engineering — a terceira camada|Harness engineering — a terceira camada]] — o conceito tool-agnóstico que esta nota instancia; as taxonomias concorrentes e a formalização acadêmica
- [[03-Dominios/Tecnologia/IA/Claude Code/index|Claude Code]] — tronco da trilha; os 6 galhos materializam os componentes do harness
- [[03-Dominios/Tecnologia/IA/Claude Code/Mental Model/02 - Como Claude Code lê um codebase|02 - Como Claude Code lê um codebase]] — por que o harness importa: o agente navega, não indexa
- [[03-Dominios/Tecnologia/IA/Claude Code/Configuração/02 - CLAUDE.md anatomia|CLAUDE.md anatomia]] — componente mais visível do harness
- [[03-Dominios/Tecnologia/IA/Claude Code/Time e Automação/index|Time e Automação]] — onde os padrões organizacionais (DRI, agent manager) aprofundam
- [[03-Dominios/Tecnologia/IA/Claude Code/Workflows/11 - Estratégias estruturais de contexto/index|Estratégias estruturais de contexto]] — sub-galho complementar sobre layout do codebase pro agente
