---
title: "O que é MCP e por que importa"
created: 2026-04-11
updated: 2026-06-28
type: concept
fase: Iniciado
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

> [!question]- Por que MCP e não só function calling diretamente?
> Function calling resolve o problema local: "este model, neste app, chama esta função". MCP resolve o problema de escala: "qualquer model, em qualquer client, chama esta capability sem que o server precise saber quem está chamando". A diferença é de O(N×M) para O(N+M) — um server implementado uma vez funciona em Claude, Cursor, Copilot e qualquer client futuro, sem mudança. Function calling é adequado para tools acopladas a um produto; MCP é para capabilities que precisam ser compartilhadas ou reutilizadas entre contextos.

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

## Armadilhas comuns

> [!warning] Usar MCP onde function calling basta
> MCP faz sentido quando há reutilização entre clients ou servidores compartilhados. Para uma app single-user com tools internas — um chatbot interno com 5 funções fixas — o overhead de setup (servidor separado, configuração no client, JSON-RPC) não traz retorno. A pergunta certa é: "mais de um client vai consumir isso?" Se não, implemente direto com o SDK.

> [!warning] Confundir "MCP" com "plugin proprietary"
> MCP é especificação aberta (RFC process em github.com/modelcontextprotocol). Um server MCP escrito hoje funciona com Claude, OpenAI Codex, Cursor e qualquer client que implemente o protocolo. O risco de adotar MCP como "plugin da Anthropic" e depois descobrir que é padrão aberto é inversamente proporcional ao risco de tratar standard aberto como solução vendor-lock. Quem já viveu a era pré-REST de APIs proprietárias vai reconhecer o padrão.

> [!warning] Ignorar a hierarquia de primitivos desde o início
> Muitos times adotam MCP implementando "tudo como tool". Mas Tools, Resources e Prompts têm semânticas distintas com implicações de performance e design. Tratar dados read-only como tool faz o LLM gastar tool-call budget em operações que o client poderia carregar proativamente. Definir a hierarquia certo desde o início evita refatoração dolorosa quando o servidor já tem usuários.

## Como explicar em inglês

MCP — Model Context Protocol — is a standardized, open protocol that defines how AI clients (like Claude, Cursor, or Copilot) connect to external capability servers. Before MCP, every integration between an LLM and an external system (databases, APIs, filesystems) required a custom implementation for each client-server pair. MCP reduces this from an N×M problem to N+M by defining a common wire format (JSON-RPC 2.0), a capability model (Tools, Resources, Prompts), and a discovery mechanism (list_tools, list_resources, list_prompts).

The analogy that holds up well is USB-C: before a universal connector, you needed a different cable for every device-peripheral pair. MCP plays the same role in the AI ecosystem — write a server once, plug it into any compliant client. In 2026, with support from Anthropic, OpenAI, Google, and Microsoft, MCP has achieved the critical mass that makes it a genuine infrastructure standard rather than an experiment.

**In a technical interview**, you might say:

> "MCP gives us N+M instead of N×M integrations. A Postgres MCP server written once works in Claude, Cursor, and any future client without modification. It does this by standardizing three things: the transport layer (JSON-RPC over stdio or HTTP+SSE), the capability model (Tools execute, Resources expose data, Prompts templatize workflows), and the discovery protocol (list_tools on connect). In 2026, if you're building agents for a team, MCP is as foundational as HTTP — you don't decide whether to use it, you decide how to structure your servers."

| PT | EN |
|----|-----|
| Protocolo de contexto de modelo | Model Context Protocol |
| Servidor MCP | MCP server |
| Cliente MCP | MCP client |
| Chamada de função | Function calling |
| Descoberta de capabilities | Capability discovery |
| Primitivos | Primitives |
| Transporte | Transport |
| Integração customizada | Custom integration |
| Adoção inter-vendor | Cross-vendor adoption |
| Especificação aberta | Open specification |

## O que vem a seguir

Entender o que MCP é — e por que importa — é o passo zero. O passo seguinte é saber o que um servidor MCP pode efetivamente expor: quais são os "blocos de construção" que o protocolo oferece para modelar qualquer capability. Sem essa distinção, você vai implementar tudo como tool e perder os benefícios de performance e composição que Resources e Prompts oferecem.

A próxima nota mapeia os três primitivos e deixa claro quando usar cada um, com anti-patterns do mundo real que mostram o custo de escolher errado desde o início.

- [[02 - Os três primitivos — Tools, Resources, Prompts]] — os building blocks do que um server pode expor

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


















































































































