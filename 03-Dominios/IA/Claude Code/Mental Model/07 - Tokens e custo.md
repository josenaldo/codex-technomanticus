---
title: "Tokens e custo — como sessões consomem tokens na prática"
type: concept
publish: true
created: 2026-05-13
updated: 2026-05-13
status: seedling
tags:
  - claude-code
  - mental-model
  - tokens
  - custo
  - ccusage
---
# Tokens e custo — como sessões consomem tokens na prática

> [!abstract] TL;DR
> Todo token processado pelo Claude Code tem custo. Input tokens (o que entra no contexto) são a maior variável — crescem a cada turno porque o histórico completo vai no input. Uma sessão de refactoring pode acumular centenas de milhares de tokens. `ccusage` mostra o breakdown real. As maiores alavancas de redução: leituras cirúrgicas, compaction preventiva e sessões focadas.

## O que é

Claude Code usa a API da Anthropic para processar cada turno da sessão. Cada chamada à API tem um custo baseado em:

- **Input tokens**: tudo no contexto quando o modelo é chamado
- **Output tokens**: o que o modelo gera (resposta + parâmetros de tool calls)
- **Cache read tokens**: tokens que bateram no prompt cache (muito mais baratos)

Preços de referência (Claude Sonnet 4.x, ordem de grandeza):
- Input: ~$3/MTok
- Output: ~$15/MTok
- Cache read: ~$0.30/MTok

Os valores exatos mudam — consulte [anthropic.com/pricing](https://www.anthropic.com/pricing) para valores atuais.

## Como o contexto acumula tokens

O aspecto menos intuitivo: **input tokens crescem a cada turno**, porque o histórico completo da sessão vai no input de cada chamada.

```
Turno 1:  5k tokens de input
Turno 2:  5k + output1 + toolresult1  = ~12k tokens de input
Turno 3:  12k + output2 + toolresult2 = ~20k tokens de input
...
Turno 20: pode estar em 150k+ tokens de input
```

Cada Read de arquivo grande, cada Bash com output verboso, multiplica esse crescimento.

## O que mais consome tokens

| Operação | Impacto | Mitigação |
|----------|---------|-----------|
| `Read` de arquivo grande (1000+ linhas) | Alto | Use `offset` + `limit` |
| `Bash` com output longo (`npm install`, `docker build`) | Alto | `\| tail -20` para filtrar |
| `Grep` com muitos resultados | Médio | Padrões mais específicos |
| Múltiplas iterações (loop de debugging) | Acumulativo | Sessões focadas |
| `Agent` subagent calls | Médio | Isolado — não polui sessão pai diretamente |

## ccusage — rastreando o custo real

`ccusage` é uma ferramenta CLI que lê os logs do Claude Code e mostra o custo por sessão:

```bash
# Instalar
npm install -g ccusage

# Ver uso hoje
ccusage

# Ver histórico dos últimos 7 dias
ccusage --days 7
```

Output típico:

```
Session 2026-05-13 14:23 — codex-technomanticus
  Input:  145,230 tokens  ($0.44)
  Output:  12,450 tokens  ($0.19)
  Cache:   89,100 tokens  ($0.03)
  Total: $0.66
```

## Estratégias de redução de custo

### 1. Leituras cirúrgicas

```
Caro:   Read("src/big-service.ts")                       → arquivo inteiro (~60k tokens)
Barato: Read("src/big-service.ts", offset=200, limit=30) → só o método (~600 tokens)
```

Use `Grep` primeiro para localizar, `Read` com range depois.

### 2. Filtrar output de comandos

```bash
# Caro: output completo do npm ci (~500 linhas)
Bash("npm ci")

# Barato: só o que importa
Bash("npm ci 2>&1 | tail -5")
```

### 3. Compaction preventiva

`/compact` quando a sessão ainda está pequena é mais barato que deixar auto compaction rodar numa sessão grande.

### 4. Sessões focadas

Uma sessão = uma tarefa. Não acumule contexto de trabalho não relacionado.

### 5. Modelo adequado à tarefa

Para tarefas mecânicas (criar arquivo simples, renomear variável), use um modelo menor:

```bash
claude --model claude-haiku-4-5-20251001 "rename variable x to connectionTimeout in auth.ts"
```

Haiku é ~10x mais barato que Sonnet e suficiente para tarefas simples.

## Custo em perspectiva

Para uma equipe de 5 devs usando Claude Code ~2h/dia cada (estimativas amplas):

| Perfil de uso | Custo estimado/mês |
|---------------|--------------------|
| Conversacional leve (poucos reads) | ~$50–100 |
| Desenvolvimento ativo (reads frequentes) | ~$200–500 |
| Refactoring pesado / sessões longas | ~$500–1500 |

O ccusage é a fonte de verdade para o seu uso real.

## Armadilhas

**Ignorar o custo até a fatura chegar**: configure alertas de uso na Anthropic Console.

**Subagents multiplicam custo**: cada subagent (`Agent` tool) é uma sessão separada com seu próprio contexto. O custo é multiplicado pelo número de subagents.

**Cache hit rate baixo**: o prompt cache é ativado quando o início do contexto (system prompt + CLAUDE.md) é idêntico entre chamadas. Mudar o CLAUDE.md frequentemente anula o benefício de cache.

## Veja também

- [[03-Dominios/IA/Claude Code/Mental Model/04 - Context window|04 - Context window]]
- [[03-Dominios/IA/Claude Code/Mental Model/06 - Compaction|06 - Compaction]]
- [[03-Dominios/IA/Claude Code/Time e Automação/05 - Controle de custo|05 - Controle de custo]] — monitoramento em nível de time
- [[03-Dominios/IA/Claude Code/Mental Model/index|Mental Model]] — índice do galho

## Referências

- [Anthropic — Pricing](https://www.anthropic.com/pricing)
- [ccusage — npm](https://www.npmjs.com/package/ccusage)
