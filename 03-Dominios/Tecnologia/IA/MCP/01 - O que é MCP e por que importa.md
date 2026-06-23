---
title: "O que é MCP e por que importa"
created: 2026-04-11
updated: 2026-05-02
type: concept
progress: backlog
status: seedling
publish: true
tags:
  - mcp
  - ia
  - protocolos
aliases:
  - O que é MCP
  - MCP definition
  - Model Context Protocol
---

# O que é MCP e por que importa

> [!abstract] TL;DR
> **[[Dicionário de IA#MCP (Model Context Protocol)|MCP (Model Context Protocol)]]** é o "USB-C para agents de IA". Antes dele, cada integração entre [[Dicionário de IA#LLM (Large Language Model)|LLM]] e sistema externo (banco de dados, filesystem, Jira, Slack) era reinventar a roda — cada cliente (Claude, Cursor, Copilot) tinha seu próprio formato de plugin. MCP, lançado pela Anthropic em **novembro de 2024** e adotado em 2025-2026 por OpenAI, Google, Microsoft, é a padronização dessa conexão. Em 2026, **se você está construindo aplicação com agents, MCP é infraestrutura básica, como HTTP**.

## A premissa

```
Antes do MCP:
  Claude  → custom integration → Postgres
  Cursor  → custom integration → Postgres
  Copilot → custom integration → Postgres
  ... cada cliente reimplementando

Depois do MCP:
  Claude  ──┐
  Cursor  ──┼─→ MCP protocol ─→ Postgres MCP server
  Copilot ──┘
  ... uma vez, qualquer cliente
```

MCP padroniza:
1. **Como** clients e servers se conectam (stdio, HTTP+SSE, WebSocket)
2. **O que** servers expõem (tools, resources, prompts)
3. **Como** clients descobrem capabilities

## Por que isso importa

Sem MCP, era N×M problema:

```
N clientes × M sistemas = N×M integrações custom
```

Com MCP:

```
N clientes × M servers = N + M conexões padronizadas
```

Linha & cair de N×M para N+M é **diferença gigante** quando N e M crescem.

## Stewardship

> [!info] Quem mantém MCP
> - **Lançado:** Anthropic (novembro 2024)
> - **Spec aberta:** github.com/modelcontextprotocol
> - **Adotado por:** Anthropic (Claude Desktop, Claude Code), OpenAI (ChatGPT, Codex), Google (Gemini), Microsoft (Copilot Studio), Cursor, Windsurf, Cline, Aider, Zed
> - **Governance:** especificação aberta com RFC process

## Os 3 primitivos

MCP define 3 tipos de coisas que servers podem expor:

| Primitivo | O que é | Exemplo |
|---|---|---|
| **[[Dicionário de IA#tools (MCP)\|Tools]]** | Funções executáveis (write) | `query_database`, `send_email` |
| **[[Dicionário de IA#resources (MCP)\|Resources]]** | Dados leitáveis (read) | Arquivos, schemas, documentos |
| **[[Dicionário de IA#prompts (MCP)\|Prompts]]** | Templates parametrizáveis | "Explain this code", "Summarize doc" |

Detalhamento em [[02 - Os três primitivos — Tools, Resources, Prompts]].

## Quando MCP brilha

✅ **Compartilhar integração entre múltiplos clients**
*"Quero que Claude E Cursor acessem nosso DB interno"*

✅ **Distribuir capability entre projetos**
*"Vou expor nossa API interna como MCP server, qualquer dev usa em qualquer ferramenta"*

✅ **Aproveitar ecossistema**
*"Awesome MCP Servers tem 500+ integrações já feitas — quero plugar Stripe, Linear, GitHub direto"*

## Quando MCP NÃO é a resposta

❌ **App single-user com tools internas** — implementação direta com SDK pode ser mais simples
❌ **Latência crítica <50ms** — overhead do protocol
❌ **Tools triviais** (calculator, regex) — não vale o setup

## O modelo mental

MCP é HTTP, não framework:

- **HTTP** padroniza request/response, headers, cookies
- **MCP** padroniza tool calls, resource fetching, prompt templates

Você não "usa HTTP" como decisão — você usa porque é o padrão. Mesmo com MCP em 2026.

## Diferença para function calling normal

| | Function calling | MCP |
|---|---|---|
| Definido onde | No código do client | No server (descoberto pelo client) |
| Reutilização | Por client | Cross-client |
| Discovery | Manual | Automático (`list_tools`) |
| Lifecycle | App-bound | Server-independent |
| Auth | Custom | Padronizado |

[[Dicionário de IA#function calling|Function calling]] resolve o problema "modelo chama função no meu código". MCP resolve "qualquer modelo chama função em qualquer servidor padrão".

## O que diferencia um senior em MCP

> [!tip]
> 1. **Sabe quando NÃO usar MCP** — single-user app com tools custom não precisa
> 2. **Distingue tools de resources de prompts** — usa cada um corretamente
> 3. **Implementa MCP servers que parecem APIs** — descrições claras, schemas precisos
> 4. **Pratica least privilege** — server só expõe o que é necessário
> 5. **Conhece o stdio vs HTTP+SSE trade-off** — local vs remoto
> 6. **Trata segurança seriamente** — MCP é vetor de [[Dicionário de IA#prompt injection|prompt injection]]
> 7. **Versiona MCP servers** — semver, breaking changes documentados
> 8. **Sabe debugar** com MCP Inspector
> 9. **Aproveita Awesome MCP Servers** — não reinventa o que existe
> 10. **Não confunde MCP com plugin proprietary** — é spec aberta

## Veja também

- [[02 - Os três primitivos — Tools, Resources, Prompts]]
- [[03 - Arquitetura cliente-servidor]]
- [[Anatomia de Agents|03 - Tool design — princípios e categorias]]
- [[Agentes de Codificação|15 - MCP — o protocolo universal]] — visão prática em coding

## Referências

- **Anthropic** — *Model Context Protocol announcement* (nov 2024)
- **MCP Specification** — *modelcontextprotocol.io* (2026)
- **GitHub** — *github.com/modelcontextprotocol* (oficial)
- **Awesome MCP Servers** — *github.com/punkpeye/awesome-mcp-servers*
