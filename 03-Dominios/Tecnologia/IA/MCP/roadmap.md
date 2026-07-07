---
title: "Roadmap — MCP"
created: 2026-07-02
type: meta
publish: false
tags:
  - meta
  - roadmap
---

# Roadmap — MCP

Diagnóstico migrado de guia/roadmap - ia.md (02/07). Cada entrada tem estado de enriquecimento, score, classificação de custo e plano de execução acionável.

**Galho:** `03-Dominios/Tecnologia/IA/MCP`

> [!success] Galho MCP **completo** em 2026-07-06 — 10/10 notas enriquecidas via fan-out ≤3 verificado (onda 1: 04·05·06 · onda 2: 07·08·09 · onda 3: 10). Nota 01 fechada em passada anterior com desvio de piso registrado (251 linhas).

## Régua de análise

Checklist `verificar-nota` — 12 itens (isenções por fase/tipo/broto aplicadas por nota):

| Grupo | Itens |
|-------|-------|
| ESTRUTURA | E1 TL;DR · E2 Abertura-problema · E3 Mermaid · E4 Casos práticos · E5 O que vem a seguir · E6 Inglês · E7 Tabela PT↔EN · E8 Armadilhas [!warning] |
| PROFUNDIDADE | P1 Código-com-falha · P2 Mecanismo explicado |
| LINKS | L1 Wikilink cross-galho · L2 Referência externa (URL) |
| MÍDIA | M1 Vídeo/podcast embutido |

**Esquema de `fase:` detectado:** COM fase (Iniciado)
**Piso de linhas:** aplicável — Iniciado ≥300

## Tabela-resumo

| Métrica | Valor |
|---------|-------|
| Total de notas | 10 |
| ⬜ pendente | 0 |
| ➖ não precisa | 0 |
| ✅ feita | 10 |
| 🔄 em andamento | 0 |
| % concluído | 100% |

---

## Notas

#### 01 - O que é MCP e por que importa   [substantivo]
- **Enriquecimento:** ✅ feita (2026-07-06) — ⚠️ **desvio de piso:** plano aplicado (TL;DR expandido p/ 3 linhas; seção "Um MCP server mínimo, primitivo a primitivo" com walkthrough; Mermaid sequenceDiagram handshake+discovery+invocação; 4 hyperlinks clicáveis), MAS ficou em 251 linhas totais (182 não-branco), abaixo do piso T1 de 300. Passada extra futura opcional.
- **Estado:** 191 linhas reais · fase: Iniciado · status: seedling
- **Núcleo/gaps:** E1, E3, L2
- **Score:** 8/12
- **Plano de execução:**
  - Expandir ~110 linhas (piso não passa) com caso prático detalhado (ex: walkthrough de um MCP server mínimo anotando cada primitivo) ou expandindo "Quando MCP brilha/NÃO é a resposta" com exemplos narrados
  - Expandir TL;DR para ≥3 linhas densas no `[!abstract]`
  - Adicionar diagrama Mermaid (sequenceDiagram handshake list_tools + tool_call, ou graph LR da topologia N×M→N+M)
  - Converter referências em hyperlinks clicáveis (modelcontextprotocol.io, github.com/modelcontextprotocol, awesome-mcp-servers)
- **Resultado:** —

#### 02 - Os três primitivos — Tools, Resources, Prompts   [substantivo]
- **Enriquecimento:** ✅ feita (2026-07-06) — Abertura narrativa (server que expõe tudo como Tool e desperdiça budget/latência do LLM); Mermaid graph LR (LLM→Tool, Client→Resource, LLM/User→Prompt); 3 hyperlinks (modelcontextprotocol.io/docs/concepts/tools, docs.anthropic.com, punkpeye/awesome-mcp-servers); 315 linhas. Verificado: URLs conferem.
- **Estado:** 303 linhas reais · fase: Iniciado · status: seedling
- **Núcleo/gaps:** E2, E3, L2
- **Score:** 9/12
- **Plano de execução:**
  - Adicionar parágrafo narrativo de abertura antes de "## A tríade" com cenário concreto (ex: tudo-como-tool desperdiçando budget/latência)
  - Converter referências em hyperlinks clicáveis (modelcontextprotocol.io/docs/concepts/tools, docs.anthropic.com, awesome-mcp-servers)
  - Adicionar diagrama Mermaid (graph LR comparando quem invoca cada primitivo: LLM→Tool, Client→Resource, LLM/User→Prompt)
- **Resultado:** —

#### 03 - Arquitetura cliente-servidor   [mecânico]
- **Enriquecimento:** ✅ feita (2026-07-06) — Referências viram hyperlinks (MCP Spec, JSON-RPC 2.0, MCP Inspector); 2 wikilinks cross-galho ([[Context Engineering]] em discovery patterns, [[Agentes de Codificação]] em config de clients); 357 linhas. Verificado: URLs e wikilinks conferem.
- **Estado:** 354 linhas reais · fase: Iniciado · status: seedling
- **Núcleo/gaps:** P1, L1, L2
- **Score:** 9/12
- **Plano de execução:**
  - Converter referências em hyperlinks Markdown clicáveis (modelcontextprotocol.io/spec, jsonrpc.org, MCP Inspector)
  - Adicionar ≥1 wikilink cross-galho (ex: [[Context Engineering]] ou [[Agentes de Codificação]]) em seção relevante
- **Resultado:** —

#### 04 - MCP servers oficiais e populares   [substantivo]
- **Enriquecimento:** ✅ feita (2026-07-06) — Abertura com cenário (agente lendo GitHub+Postgres+Slack) antes do TL;DR; awesome-mcp-servers/modelcontextprotocol/servers/mcp.so/smithery.ai viram links clicáveis; Mermaid flowchart de decisão instalar-vs-construir; [!warning] de caducidade no topo de "## Categorias principais (2026)"; ~285→323 linhas (cobre piso ≥300). Score ~11/12.
- **Estado:** 284 linhas reais · fase: Iniciado · status: seedling
- **Núcleo/gaps:** E2, E3, P1, L2
- **Score:** 8/12
- **Plano de execução:**
  - Adicionar parágrafo de abertura com cenário concreto antes do TL;DR (ex: conectar agente a GitHub/Postgres/Slack sem escrever servers do zero)
  - Converter referências em links Markdown clicáveis (awesome-mcp-servers, modelcontextprotocol/servers, mcp.so, smithery.ai)
  - Adicionar diagrama Mermaid (flowchart de decisão install vs build)
  - Adicionar `[!warning]` de caducidade no topo de "## Categorias principais (2026)" (packages/URLs/status de manutenção mudam rápido)
  - Expansão de conteúdo (abertura + Mermaid + callout) cobre o piso que falta para ≥300
- **Resultado:** —

#### 05 - Construindo um MCP server local   [substantivo]
- **Enriquecimento:** ✅ feita (2026-07-06) — TL;DR expandido p/ ≥3 linhas (SDK+decorators / stdio+JSON-RPC / tool design = 60% do trabalho); abertura com cenário (banco interno consultado por 3 clients) entre TL;DR e "## Setup mínimo"; Referências viram links clicáveis https:// (SDK Python/TS, Inspector, tutorial Anthropic); Mermaid sequenceDiagram do fluxo stdio (client→subprocess→JSON-RPC→tool). ~445 linhas, score ~12/13.
- **Estado:** 421 linhas totais · fase: Iniciado · status: seedling
- **Núcleo/gaps:** E1, E2, L2, E3
- **Score:** 8/12
- **Plano de execução:**
  - Expandir `[!abstract]` TL;DR para ≥3 linhas (o que é, como funciona, o que importa de verdade)
  - Adicionar parágrafo de abertura entre TL;DR e "## Setup mínimo" com cenário concreto (expor banco/APIs internas sem reescrever integração por client)
  - Converter referências em links Markdown clicáveis com https:// (MCP Python SDK, TypeScript SDK, Inspector, tutorial Anthropic)
  - Opcional: diagrama Mermaid do fluxo stdio (client → subprocess → server → tools)
- **Resultado:** —

#### 06 - MCP remoto — HTTP + SSE para times   [substantivo]
- **Enriquecimento:** ✅ feita (2026-07-06) — Abertura narrativa (time de 5 devs compartilhando servidor de banco, stdio vs HTTP+SSE) antes de "## Quando partir para HTTP+SSE"; 3 referências viram links clicáveis (MCP Spec—Transports, Cloudflare Workers for MCP, Smithery); callout [!example] de código-com-falha (curl sem Authorization → 401). Desvio: "Anthropic — Hosted MCP servers (beta)" ficou sem link (sem URL pública estável).
- **Estado:** 376 linhas reais · fase: Iniciado · status: seedling
- **Núcleo/gaps:** E2, L2, P1
- **Score:** 9/12
- **Plano de execução:**
  - Adicionar parágrafo de abertura narrativo antes de "## Quando partir para HTTP+SSE" com cenário concreto (time compartilhando o mesmo servidor de banco)
  - Converter referências em links Markdown clicáveis com https:// (MCP Spec — Transports, Smithery, Cloudflare Workers for MCP)
  - Opcional: exemplo de código-com-falha (client sem header Authorization → 401, ou server sem TLS rejeitado)
- **Resultado:** —

#### 07 - Segurança em MCP   [mecânico]
- **Enriquecimento:** ✅ feita (2026-07-06) — 4 referências finais viram links clicáveis (URLs verificadas via WebSearch): OWASP Top 10 for LLMs, MCP Spec—Security (security_best_practices), Anthropic (anúncio oficial MCP), Simon Willison prompt-injection series. Desvio: "Anthropic — MCP security best practices" não tem post dedicado; linkado ao anúncio oficial como substituto mais fiel.
- **Estado:** 327 linhas reais · fase: Iniciado · status: seedling
- **Núcleo/gaps:** L2
- **Score:** 11/12
- **Plano de execução:**
  - Converter as 4 referências finais em links Markdown clicáveis com https:// (OWASP Top 10 for LLMs, MCP Spec — Security)
- **Resultado:** —

#### 08 - Ecossistema 2026 — clients e integrações   [substantivo]
- **Enriquecimento:** ✅ feita (2026-07-06) — [!abstract] expandido de 1 parágrafo p/ 3 linhas (protocolo inter-vendor / ecossistema 3000+ servers+managed hosting / mudanças 2026: Tasks+code-execution+managed hosting); abertura com cenário (avaliar qual client adotar → consenso inter-vendor) antes de "## Os clients que falam MCP"; [!warning] de validade em "## Métricas de adoção (2026)" apontando Awesome MCP Servers + smithery.ai. Plano integral.
- **Estado:** ~327 linhas reais (371 total, ~44 em branco) · fase: Iniciado · status: growing
- **Núcleo/gaps:** E1, E2, P1
- **Score:** 9/12
- **Plano de execução:**
  - Expandir `[!abstract]` de 1 parágrafo comprimido para ≥3 linhas separadas (protocolo inter-vendor; ecossistema de 3000+ servers; o que mudou em 2026 — Tasks + code-execution + managed hosting)
  - Adicionar parágrafo de abertura com cenário antes de "## Os clients que falam MCP" (avaliação de qual client adotar, consenso inter-vendor)
  - Adicionar `[!warning]`/`[!info]` de validade em "## Métricas de adoção (2026)" (números envelhecem rápido; conferir Awesome MCP Servers e smithery.ai)
- **Resultado:** —

#### 09 - Casos comuns no mercado   [mecânico]
- **Enriquecimento:** ✅ feita (2026-07-06) — 3 referências placeholder substituídas por URLs reais verificadas via WebSearch (Anthropic "Introducing the MCP", github.com/punkpeye/awesome-mcp-servers, Cloudflare "Build and deploy Remote MCP servers"); Mermaid graph TD dos 5 casos (MCP→Caso1..5) antes de "Caso 1". Plano integral.
- **Estado:** 320 linhas reais · fase: Iniciado · status: seedling
- **Núcleo/gaps:** E3, L2
- **Score:** 10/12
- **Plano de execução:**
  - Adicionar URLs reais às referências (Anthropic blog, github.com/punkpeye/awesome-mcp-servers, blog.cloudflare.com)
  - Opcional: diagrama Mermaid dos 5 casos (graph TD MCP → Caso1..5)
- **Resultado:** —

#### 10 - Setup completo + best practices   [substantivo]
- **Enriquecimento:** ✅ feita (2026-07-06) — Seção "## O que vem a seguir" após "## Referências" fechando o ciclo do galho, com wikilinks [[Agentes de Codificação]] e [[Economia de Tokens]] (ambos têm index.md); referências viram links reais verificados via WebFetch (spec, Python SDK, Inspector); abertura opcional com cenário "funciona no Inspector → produção" antes de "## Stack recomendada". Desvio: docs.anthropic.com/mcp/best-practices não existe → trocado por anthropic.com/news/model-context-protocol. Score 11/12.
- **Estado:** ~393 linhas reais · fase: Iniciado · status: seedling
- **Núcleo/gaps:** E2, E5, L2
- **Score:** 9/12
- **Plano de execução:**
  - Adicionar seção/parágrafo "O que vem a seguir" após "## Referências" fechando o ciclo do galho MCP, apontando para galhos relacionados ([[Agentes de Codificação]], [[Economia de Tokens]])
  - Adicionar URLs reais nas referências (modelcontextprotocol.io/spec, github.com/modelcontextprotocol/python-sdk, docs.anthropic.com, MCP Inspector)
  - Opcional: parágrafo de abertura com cenário antes de "## Stack recomendada" (de "funciona no Inspector" a "está em produção para o time")
- **Resultado:** —
