---
title: "Context window — o que entra, o que sai, por que isso importa"
type: concept
publish: true
created: 2026-05-13
updated: 2026-05-13
status: seedling
tags:
  - claude-code
  - mental-model
  - context-window
  - tokens
---
# Context window — o que entra, o que sai, por que isso importa

> [!abstract] TL;DR
> A context window é a memória de trabalho do Claude Code: tudo que o agente "sabe" em uma sessão está nela. Sistema prompt, CLAUDE.md, histórico de conversa, e todos os outputs de tool calls consomem tokens. Quando enche, o agente esquece ou o custo dispara. Gerenciar contexto é gerenciar a qualidade e custo das sessões.

## O que é

A context window é o espaço de tokens que o modelo processa em cada chamada à API. É finita (~200k tokens nos modelos Claude mais recentes). Tudo que está dentro dela é "visível" para o agente. O que está fora não existe para ele.

Em Claude Code, a context window acumula ao longo da sessão:

```
Chamada 1: [system prompt] + [CLAUDE.md] + [turn 1]
Chamada 2: [system prompt] + [CLAUDE.md] + [turn 1] + [tool result 1] + [turn 2]
Chamada 3: [system prompt] + [CLAUDE.md] + [turn 1] + [tool result 1] + [turn 2] + [tool result 2] + [turn 3]
```

Cada iteração do loop agentic adiciona mais tokens.

## O que entra no contexto

| Componente | Tokens típicos | Notas |
|------------|---------------|-------|
| System prompt (Claude Code) | ~2.000–5.000 | Fixo por sessão |
| CLAUDE.md global | Variável | Lido no início |
| CLAUDE.md do projeto | Variável | Lido no início |
| Mensagens do usuário | Variável | Cada turn |
| Respostas do modelo | Variável | Cada turn |
| Tool call outputs | **Maior variável** | Cresce com cada Read, Bash, Grep |

### O que mais consome contexto

**Leituras de arquivo grandes**: `Read("src/huge-service.ts")` num arquivo de 2000 linhas pode adicionar 40k+ tokens de uma vez.

**Bash com output verboso**: `npm ci`, `docker build`, compiladores — o stdout completo vai para o contexto.

**Grep com muitos resultados**: `Grep("import", "src/")` num projeto grande retorna centenas de linhas.

**Múltiplas iterações**: uma sessão de debugging com 30 tool calls pode facilmente passar de 100k tokens de contexto.

## Por que isso importa

### Custo

Input tokens = dinheiro. Em uma sessão que acumula 150k tokens de contexto e tem 20 turnos, você está pagando por ~150k tokens de input por chamada, em média. Gerenciar contexto reduz custo diretamente.

### Qualidade

Com contexto saturado (próximo do limite), o modelo começa a "perder" detalhes do início da sessão. Uma instrução dada no turn 1 pode ser esquecida no turn 40. Isso é [[03-Dominios/IA/Claude Code/Mental Model/06 - Compaction|compaction]] em ação — mas compaction tem custo de fidelidade.

### Velocidade

Janelas de contexto maiores = inferência mais lenta. Uma sessão de 180k tokens responde mais devagar que uma de 10k.

## Estratégias de gerenciamento

**Leituras cirúrgicas**: use `offset` e `limit` no Read para ler apenas o trecho necessário.

```
Ruim: Read("src/big-service.ts")                        → arquivo inteiro
Bom:  Read("src/big-service.ts", offset=150, limit=40)  → só o método relevante
```

**Redirecionamento de output**: para comandos verbosos, filtre antes que entrem no contexto.

```bash
npm ci 2>&1 | tail -5
```

**Compactação manual preventiva**: use `/compact` quando você nota que a sessão cresceu, antes de atingir o limite auto.

**Sessões focadas**: cada sessão = uma tarefa. Não use a mesma sessão para refactoring do módulo A e debugging do módulo B.

**`/resume` com consciência**: retomar uma sessão compactada significa começar com um resumo — pode ter perdido detalhes.

## Armadilhas

**Ler o arquivo inteiro "só para ter"**: um CLAUDE.md que aponta para os arquivos-chave reduz exploração desnecessária.

**Confundir sessão com persistência**: o agente não "lembra" de sessões anteriores. Cada `claude` novo começa do zero (exceto com `--resume`).

**Output de CI sem filtro**: integrar Claude Code em pipelines sem filtrar output de ferramentas pode explodir o contexto em segundos.

## Veja também

- [[03-Dominios/IA/Claude Code/Mental Model/06 - Compaction|06 - Compaction]]
- [[03-Dominios/IA/Claude Code/Mental Model/07 - Tokens e custo|07 - Tokens e custo]]
- [[03-Dominios/IA/Claude Code/Mental Model/03 - Tool use|03 - Tool use]]
- [[03-Dominios/IA/Claude Code/Mental Model/index|Mental Model]] — índice do galho

## Referências

- [Anthropic — Context windows](https://docs.anthropic.com/pt/docs/about-claude/models)
