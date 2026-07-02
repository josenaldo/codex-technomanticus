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

> [!warning] Diagnóstico de 02/07 — pode estar defasado. Vários itens marcados ⬜ podem já ter sido enriquecidos depois; reconciliar com o estado real ao tratar o galho.

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
| ⬜ pendente | 10 |
| ➖ não precisa | 0 |
| ✅ feita | 0 |
| 🔄 em andamento | 0 |
| % concluído | 0% |

---

## Notas

#### 01 - O que é MCP e por que importa   [substantivo]
- **Enriquecimento:** ⬜ pendente
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
- **Enriquecimento:** ⬜ pendente
- **Estado:** 303 linhas reais · fase: Iniciado · status: seedling
- **Núcleo/gaps:** E2, E3, L2
- **Score:** 9/12
- **Plano de execução:**
  - Adicionar parágrafo narrativo de abertura antes de "## A tríade" com cenário concreto (ex: tudo-como-tool desperdiçando budget/latência)
  - Converter referências em hyperlinks clicáveis (modelcontextprotocol.io/docs/concepts/tools, docs.anthropic.com, awesome-mcp-servers)
  - Adicionar diagrama Mermaid (graph LR comparando quem invoca cada primitivo: LLM→Tool, Client→Resource, LLM/User→Prompt)
- **Resultado:** —

#### 03 - Arquitetura cliente-servidor   [mecânico]
- **Enriquecimento:** ⬜ pendente
- **Estado:** 354 linhas reais · fase: Iniciado · status: seedling
- **Núcleo/gaps:** P1, L1, L2
- **Score:** 9/12
- **Plano de execução:**
  - Converter referências em hyperlinks Markdown clicáveis (modelcontextprotocol.io/spec, jsonrpc.org, MCP Inspector)
  - Adicionar ≥1 wikilink cross-galho (ex: [[Context Engineering]] ou [[Agentes de Codificação]]) em seção relevante
- **Resultado:** —

#### 04 - MCP servers oficiais e populares   [substantivo]
- **Enriquecimento:** ⬜ pendente
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
- **Enriquecimento:** ⬜ pendente
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
- **Enriquecimento:** ⬜ pendente
- **Estado:** 376 linhas reais · fase: Iniciado · status: seedling
- **Núcleo/gaps:** E2, L2, P1
- **Score:** 9/12
- **Plano de execução:**
  - Adicionar parágrafo de abertura narrativo antes de "## Quando partir para HTTP+SSE" com cenário concreto (time compartilhando o mesmo servidor de banco)
  - Converter referências em links Markdown clicáveis com https:// (MCP Spec — Transports, Smithery, Cloudflare Workers for MCP)
  - Opcional: exemplo de código-com-falha (client sem header Authorization → 401, ou server sem TLS rejeitado)
- **Resultado:** —

#### 07 - Segurança em MCP   [mecânico]
- **Enriquecimento:** ⬜ pendente
- **Estado:** 327 linhas reais · fase: Iniciado · status: seedling
- **Núcleo/gaps:** L2
- **Score:** 11/12
- **Plano de execução:**
  - Converter as 4 referências finais em links Markdown clicáveis com https:// (OWASP Top 10 for LLMs, MCP Spec — Security)
- **Resultado:** —

#### 08 - Ecossistema 2026 — clients e integrações   [substantivo]
- **Enriquecimento:** ⬜ pendente
- **Estado:** ~327 linhas reais (371 total, ~44 em branco) · fase: Iniciado · status: growing
- **Núcleo/gaps:** E1, E2, P1
- **Score:** 9/12
- **Plano de execução:**
  - Expandir `[!abstract]` de 1 parágrafo comprimido para ≥3 linhas separadas (protocolo inter-vendor; ecossistema de 3000+ servers; o que mudou em 2026 — Tasks + code-execution + managed hosting)
  - Adicionar parágrafo de abertura com cenário antes de "## Os clients que falam MCP" (avaliação de qual client adotar, consenso inter-vendor)
  - Adicionar `[!warning]`/`[!info]` de validade em "## Métricas de adoção (2026)" (números envelhecem rápido; conferir Awesome MCP Servers e smithery.ai)
- **Resultado:** —

#### 09 - Casos comuns no mercado   [mecânico]
- **Enriquecimento:** ⬜ pendente
- **Estado:** 320 linhas reais · fase: Iniciado · status: seedling
- **Núcleo/gaps:** E3, L2
- **Score:** 10/12
- **Plano de execução:**
  - Adicionar URLs reais às referências (Anthropic blog, github.com/punkpeye/awesome-mcp-servers, blog.cloudflare.com)
  - Opcional: diagrama Mermaid dos 5 casos (graph TD MCP → Caso1..5)
- **Resultado:** —

#### 10 - Setup completo + best practices   [substantivo]
- **Enriquecimento:** ⬜ pendente
- **Estado:** ~393 linhas reais · fase: Iniciado · status: seedling
- **Núcleo/gaps:** E2, E5, L2
- **Score:** 9/12
- **Plano de execução:**
  - Adicionar seção/parágrafo "O que vem a seguir" após "## Referências" fechando o ciclo do galho MCP, apontando para galhos relacionados ([[Agentes de Codificação]], [[Economia de Tokens]])
  - Adicionar URLs reais nas referências (modelcontextprotocol.io/spec, github.com/modelcontextprotocol/python-sdk, docs.anthropic.com, MCP Inspector)
  - Opcional: parágrafo de abertura com cenário antes de "## Stack recomendada" (de "funciona no Inspector" a "está em produção para o time")
- **Resultado:** —
