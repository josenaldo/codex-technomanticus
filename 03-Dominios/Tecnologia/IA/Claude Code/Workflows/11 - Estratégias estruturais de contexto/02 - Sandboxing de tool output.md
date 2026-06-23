---
title: "Sandboxing de tool output — interceptar antes de poluir o contexto"
type: concept
progress: backlog
publish: true
created: 2026-05-22
updated: 2026-05-22
status: seedling
fase: adepto
tags:
  - claude-code
  - workflows
  - contexto
  - tokens
  - hooks
  - mcp
  - sandboxing
aliases:
  - Tool output sandbox
  - Sandboxed tool calls
---

# Sandboxing de tool output — interceptar antes de poluir o contexto

> [!abstract] TL;DR
> Cada [[Dicionário de IA#tool call|tool call]] do [[Dicionário de IA#Claude Code|Claude Code]] (`Bash`, `Read`, [[Dicionário de IA#MCP (Model Context Protocol)|MCP]]) injeta o resultado no contexto. Um snapshot de Playwright custa ~56k [[Dicionário de IA#Token|tokens]]. Vinte issues do GitHub custam ~59k. Um log de access pode passar de 45k. Sandboxing de tool output intercepta esses resultados *antes* que cheguem ao contexto, persiste o bruto em SQLite local, e devolve ao agente apenas um resumo + um *handle* pra consultar depois. O ganho típico de 15–25% de redução em sessões dominadas por tool calls vorazes, sem perda de informação acessível.

## O que é

Uma camada externa ao Claude Code que se posiciona **entre o tool e o contexto**:

1. O agente invoca um tool (ex: `Bash("kubectl logs deploy/api --tail=2000")`).
2. Em vez de a saída de 30k tokens ir direto pro contexto, um hook intercepta.
3. A saída completa é gravada em um índice local (SQLite com FTS5) com um ID único.
4. O agente recebe de volta um resumo compactado: primeiras/últimas linhas, contagem, padrões detectados, **handle de busca**.
5. Se o agente precisar do detalhe específico, ele chama uma tool de query (`search_logs("OutOfMemoryError")`) que retorna só os trechos relevantes — também via cache local, sem rebuild.

A diferença pra leitura cirúrgica (`| tail -20` no `Bash`) é que **a informação não é perdida** — ela existe em índice consultável, só não está consumindo contexto a cada turno.

## Como funciona

### Hooks como ponto de interceptação

O Claude Code expõe pontos de hook que permitem interceptar tool calls:

- **`PreToolUse`** — reescrever o comando antes de executar (ex: adicionar paginação, redirecionar output pra arquivo).
- **`PostToolUse`** — interceptar o resultado antes de devolver pro agente.
- **`PreCompact`** — checkpoint antes da compactação automática.
- **`SessionStart`** — injetar instruções de roteamento ("use `search_logs` em vez de `kubectl logs` direto").

Sandboxing maduro usa os quatro: roteia ferramentas via SessionStart, intercepta resultados via PostToolUse, checkpoint via PreCompact.

### "Think in code" como padrão complementar

Sandboxing puro já reduz; o padrão **think in code** vai além: em vez de o agente ler 50 arquivos pra contar funções, ele escreve um script que faz a contagem e dá `console.log()` só do resultado final.

```js
// Antes: 47 × Read() = ~700 KB no contexto
// Depois: 1 × Bash(script) = ~3.6 KB
const files = fs.readdirSync('src').filter(f => f.endsWith('.ts'));
files.forEach(f => {
  const lines = fs.readFileSync('src/' + f, 'utf8').split('\n').length;
  console.log(`${f}: ${lines}`);
});
```

A regra é: **o LLM deve programar a análise, não computar a análise**. Toda vez que o agente está prestes a ler N arquivos pra reduzir a um número, ele deveria estar escrevendo um script que devolve só o número.

### Arquitetura de um sandbox típico

```
┌─────────────────┐
│  Claude Code    │
└────────┬────────┘
         │ tool call
         ▼
┌─────────────────┐
│  PreToolUse     │ ── reescreve ou substitui
│  hook           │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  Tool executa   │ (Bash, Read, MCP…)
└────────┬────────┘
         │ output bruto (50k tokens)
         ▼
┌─────────────────┐
│  PostToolUse    │ ── persiste em SQLite
│  hook           │ ── retorna resumo + handle
└────────┬────────┘
         │ output sanitizado (3k tokens)
         ▼
┌─────────────────┐
│  Contexto       │
│  do agente      │
└─────────────────┘
```

O SQLite local usa FTS5 (full-text search) ou [[Dicionário de IA#BM25|BM25]] pra recuperar trechos por relevância quando o agente chama a tool de busca.

## Quando usar

Sandboxing começa a pagar quando a sessão é dominada por **outputs grandes e exploratórios**:

- Snapshots de DOM (Playwright, MCP de browser).
- Logs de produção (kubectl, journalctl, cloud-watch).
- Listagens longas (issues, PRs, deploys).
- Dumps de configuração (`kubectl get all`, `terraform plan`).
- Output de teste com muitos casos falhando.

Para sessões de coding "puro" — onde a maioria dos tokens vem de leitura de código e geração de patches — o ganho é menor; lazy-load ([[01 - Estrutura .claude lazy-load]]) e leitura cirúrgica resolvem melhor.

## Custo da abordagem

O preço de sandboxing é complexidade operacional:

- **Hooks customizados ou MCP server dedicado** — precisa rodar e ser mantido.
- **SQLite local com índice FTS5** — cresce com a sessão; precisa de purge.
- **Tools adicionais expostas ao agente** — `search_logs`, `fetch_chunk`, etc. O agente precisa "aprender" a usá-las (via instruções de routing).
- **Risco de perda de informação** — se o resumo descarta o que era importante, o agente fica cego até pedir o trecho certo via search.

Vale pra quem opera Claude Code em escala (pipelines, multi-projeto, agentes 24/7). Para uso individual sem volume de tool calls verbosos, geralmente é overkill.

## Armadilhas

**Resumo agressivo demais perdendo o sinal**. Se o sandbox retorna só "20 linhas omitidas" sem detectar que entre elas havia um stack trace, o agente continua chamando o tool até "esbarrar" no erro. O bom resumo detecta padrões (erros, warnings, anomalias) e os preserva no compacto.

**Índice sem purge**. O SQLite cresce a cada tool call. Sem TTL ou rotação, em uma semana ocupa GB. Sandboxes sérios deletam outputs de >7 dias e purgam em SessionEnd se a sessão for descartada.

**Cobertura inconsistente**. Se hook é configurado pra interceptar só `Bash`, mas o agente usa MCP de browser direto, o output do MCP escapa do sandbox. Sandboxing requer **matchers abrangentes**, calibrados pra cada plataforma (Claude Code, Gemini CLI, etc).

**Re-routing instructions custam tokens**. Pra o agente preferir `search_logs` em vez de `kubectl logs`, o sandbox injeta instruções de routing no SessionStart. Esse próprio bloco custa ~500–1500 tokens em todo turno (vai pro prefix cache, então amortiza, mas existe).

**Licenças não-OSI**. Implementações populares (ex: `mksglu/context-mode`) usam licenças tipo Elastic License v2, que restringem oferecer o sandbox como serviço gerenciado. Pra uso interno tudo bem, mas leia antes de empacotar como produto.

## Relação com outras abordagens deste galho

Lazy-load ([[01 - Estrutura .claude lazy-load|01]]) reduz o que carrega *no boot*; sandboxing reduz o que entra *durante* a sessão a partir de tool calls. As duas combinam — não competem.

Indexação semântica ([[03 - Indexação semântica externa|03]]) e knowledge graph ([[04 - Knowledge graph local com AST|04]]) mudam *como o codebase é navegado*. Sandboxing muda *como o output de qualquer tool é armazenado*. Também ortogonais.

## Veja também

- [[03-Dominios/Tecnologia/IA/Claude Code/Hooks e Guardrails/index|Hooks e Guardrails]] — base técnica dos hooks
- [[03-Dominios/Tecnologia/IA/Claude Code/Skills e MCP/04 - MCP overview|MCP overview]] — protocolo que sustenta sandboxes externos
- [[03-Dominios/Tecnologia/IA/Claude Code/Mental Model/06 - Compaction|Compaction]] — comportamento padrão quando contexto satura
- [[03-Dominios/Tecnologia/IA/Claude Code/Mental Model/07 - Tokens e custo|Tokens e custo]] — táticas básicas de redução
- [[index|Tronco do sub-galho]]

## Aprofundamento

> [!convite] Referências externas
> - [mksglu/context-mode](https://github.com/mksglu/context-mode) — MCP server que implementa sandboxing + "think in code" + session continuity, com plugins pra Claude Code, Gemini CLI, VS Code Copilot, Cursor, Codex e outros. **Cuidado:** licença ELv2 (não-OSI, restritiva pra uso como serviço gerenciado), crescimento de stars/forks suspeito (~15k em 3 meses) e README cita Microsoft/Google/Meta como usuários sem prova. Leia o código antes de adotar; a arquitetura é o aprendizado real.
> - [alexgreensh/token-optimizer](https://github.com/alexgreensh/token-optimizer) — plugin Claude Code com 5 hooks lifecycle, dashboard local, checkpoint pré-compaction. Licença PolyForm Noncommercial (proíbe uso comercial — fica de olho se for usar em projeto pago). Repo grande, vale como referência arquitetural mesmo sem adotar.
>
> Comparativo conceitual com **RTK** (Rust Token Killer): RTK age no input do tool, reescrevendo o comando *antes* de executar. Sandboxing age no output, capturando o resultado *depois* de executar. As duas estratégias compõem: RTK reduz comandos verbosos na origem; sandboxing absorve o que ainda passa.
>
> Consumiu? Faça uma glosa em `02-Glosas/` se quiser destilar mais.
