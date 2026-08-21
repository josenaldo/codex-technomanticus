---
title: "MCP"
type: moc
publish: true
tags:
  - mcp
  - ia
  - moc
created: 2026-04-11
updated: 2026-05-02
aliases:
  - Model Context Protocol
  - MCP protocol
---

# MCP — Model Context Protocol

**[[Dicionário de IA#MCP (Model Context Protocol)|MCP]]** é o "USB-C para [[Dicionário de IA#Agent|agents]] de IA": padrão aberto para conectar [[Dicionário de IA#LLM (Large Language Model)|LLMs]] a sistemas externos. Lançado pela Anthropic em novembro de 2024, virou padrão de facto em 2025-2026 com adoção de OpenAI, Google, Microsoft, Cursor, Windsurf, e ecossistema de **3000+ servers** em Awesome MCP Servers. Em 2026, **MCP é infrastructure-grade** — não experimento. Se você está construindo aplicação com agents, MCP é tão essencial quanto HTTP.

> [!info] Pré-requisitos
> Recomendado ter passado por [[Anatomia de Agents]] (Trilha 2 — fundamentos de tools) e [[Agentes de Codificação]] (visão prática). Para construção de servers, helps ter Python ou TypeScript.

> [!tip] A premissa central
> N clients × M sistemas = N×M integrações custom (era pré-MCP). Com MCP: N clients + M servers = N+M conexões padronizadas. Quando N e M crescem, a diferença é gigante.

## Comece por aqui

Trilha sequencial recomendada — fundamentos → arquitetura → construção → operação.

### Bloco 1 — Fundamentos (3 notas)

O quê, por quê, e como funciona.

- [[01 - O que é MCP e por que importa]] — definição, lifecycle, quando usar
- [[02 - Os três primitivos — Tools, Resources, Prompts]] — diferenças e quando usar cada
- [[03 - Arquitetura cliente-servidor]] — stdio vs HTTP+SSE, JSON-RPC, lifecycle

### Bloco 2 — Servers (2 notas)

Reusar antes de construir; construir quando necessário.

- [[04 - MCP servers oficiais e populares]] — catálogo, decision criteria, defaults sensatos
- [[05 - Construindo um MCP server local]] — Python SDK, FastMCP, schemas, MCP Inspector

### Bloco 3 — Produção (2 notas)

De server local a server compartilhado seguro.

- [[06 - MCP remoto — HTTP + SSE para times]] — auth, deploy, observabilidade
- [[07 - Segurança em MCP]] — prompt injection, supply chain, defense in depth

### Bloco 4 — Ecossistema e Casos (3 notas)

Visão de mercado e patterns reusáveis.

- [[08 - Ecossistema 2026 — clients e integrações]] — clients, marketplaces, hosting managed
- [[09 - Casos comuns no mercado]] — 5 categorias de uso com exemplos
- [[10 - Setup completo + best practices]] — checklist 4 fases, distilled best practices

## Rotas alternativas

### Rota prática (vou usar MCP hoje)
*"Quero plugar [[Dicionário de IA#Claude Code|Claude Code]] com Postgres + GitHub"*

[[01 - O que é MCP e por que importa]] → [[04 - MCP servers oficiais e populares]] → [[03 - Arquitetura cliente-servidor]] → [[07 - Segurança em MCP]]

### Rota construtor (vou criar MCP server)
*"Tenho API/sistema interno e quero expor como MCP"*

[[02 - Os três primitivos — Tools, Resources, Prompts]] → [[05 - Construindo um MCP server local]] → [[10 - Setup completo + best practices]] → [[Anatomia de Agents|03 - Tool design — princípios e categorias]]

### Rota arquiteto (deploy team-wide)
*"Servidor compartilhado para equipe, com compliance"*

[[03 - Arquitetura cliente-servidor]] → [[06 - MCP remoto — HTTP + SSE para times]] → [[07 - Segurança em MCP]] → [[09 - Casos comuns no mercado]] → [[Segurança e Guardrails|11 - Governance as architecture]]

### Rota cético (vale a pena adotar?)
*"Por que MCP em vez de function calling?"*

[[01 - O que é MCP e por que importa]] → [[08 - Ecossistema 2026 — clients e integrações]] → [[09 - Casos comuns no mercado]]

### Rota security (red team posture)
*"MCP é vetor de ataque — preciso entender riscos"*

[[07 - Segurança em MCP]] → [[Segurança e Guardrails|02 - Slopsquatting — o ataque via alucinação]] → [[Segurança e Guardrails|06 - Permissões e sandboxing]] → [[10 - Setup completo + best practices]]

## Como esta trilha se conecta

```mermaid
graph TB
    M["MCP<br/>(esta trilha)"] --> A["Anatomia de Agents<br/>tools são MCP-able"]
    M --> AC["Agentes de Codificação<br/>Cursor/Claude Code consomem MCP"]
    M --> S["Segurança e Guardrails<br/>MCP é vetor"]
    M --> C["Context Engineering<br/>JIT retrieval via MCP"]
    M --> R["RAG e Vector Databases<br/>MCP servers de docs/dados"]
    M --> ME["Memória de Agentes<br/>memory via MCP"]
```

MCP é **camada de infraestrutura** que toca quase tudo no stack de agentes.

## Leituras recomendadas

| Fonte | Tipo | Cobertura |
|---|---|---|
| **Anthropic — MCP announcement** | Blog (nov 2024) | Nota 01 |
| **MCP Specification** | Spec oficial (modelcontextprotocol.io) | Trilha inteira |
| **MCP Python SDK** | github.com/modelcontextprotocol/python-sdk | Notas 05, 10 |
| **MCP TypeScript SDK** | github.com/modelcontextprotocol/typescript-sdk | Nota 05 |
| **Awesome MCP Servers** | github.com/punkpeye/awesome-mcp-servers | Nota 04 |
| **MCP Inspector** | github.com/modelcontextprotocol/inspector | Notas 05, 10 |
| **OWASP Top 10 for LLMs** | owasp.org | Nota 07 |
| **Anthropic — MCP best practices** | docs.anthropic.com | Nota 10 |
| **Cloudflare — MCP on Workers** | developers.cloudflare.com | Notas 06, 08 |
| **Claude Course** | YouTube (Anthropic) | Visão geral |

## Veja também

- [[Anatomia de Agents]] — fundamentos genéricos
- [[Agentes de Codificação]] — coding agents (todos suportam MCP)
- [[Context Engineering]] — JIT retrieval via MCP
- [[Segurança e Guardrails]] — defesa contra MCP malicioso
- [[Memória de Agentes]] — memória via MCP servers
- [[RAG e Vector Databases]] — alternativa quando MCP não cabe
- [[03-Dominios/Tecnologia/IA/index|Formação Engenheiro de IA]]
