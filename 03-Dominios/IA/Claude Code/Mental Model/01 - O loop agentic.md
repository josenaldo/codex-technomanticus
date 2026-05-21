---
title: "O loop agentic — plan, act, observe, iterate"
type: concept
publish: true
created: 2026-05-13
updated: 2026-05-13
status: seedling
tags:
  - claude-code
  - mental-model
  - agentic-loop
---
# O loop agentic — plan, act, observe, iterate

> [!abstract] TL;DR
> Claude Code não é um chatbot que gera texto — é um agente que executa um loop: recebe uma tarefa, planeja o que fazer, executa uma ação (tool call), observa o resultado, e itera. O loop continua até a tarefa estar completa ou o agente pedir ajuda. Entender esse loop muda como você formula pedidos e diagnostica problemas.

## O que é

Um chatbot responde e para. Um agente responde e age — e continua agindo até concluir.

O loop agentic do Claude Code tem quatro fases:

| Fase | O que acontece |
|------|----------------|
| **Plan** | O agente lê a tarefa, o contexto (CLAUDE.md, histórico), e decide qual tool usar |
| **Act** | Executa uma tool call: Read, Edit, Bash, Grep, etc. |
| **Observe** | Lê o output da tool. O output entra no contexto. |
| **Iterate** | Com base no que observou, decide a próxima ação — ou conclui |

A cada iteração, o agente tem mais informação. É por isso que o Claude Code funciona bem em tarefas abertas: ele descobre o que precisa à medida que navega.

## Como funciona na prática

### Exemplo: "fix the failing test"

Tarefa: `fix the failing test in auth.test.ts`

Loop que acontece:
1. **Plan**: preciso ver o arquivo de teste e o código que ele testa
2. **Act**: `Read("src/auth.test.ts")`
3. **Observe**: vê o teste falhar em `validateToken` — expectativa errada no mock
4. **Plan**: preciso ver a implementação de `validateToken`
5. **Act**: `Grep("validateToken", "src/")`
6. **Observe**: encontra `src/auth.ts:47`
7. **Act**: `Read("src/auth.ts", offset=40, limit=30)`
8. **Observe**: vê que o retorno mudou de `{valid: true}` para `{isValid: true}`
9. **Plan**: o teste usa `valid`, precisa usar `isValid`
10. **Act**: `Edit("src/auth.test.ts", old="result.valid", new="result.isValid")`
11. **Observe**: edição aplicada
12. **Act**: `Bash("npm test src/auth.test.ts")`
13. **Observe**: teste passando ✓
14. **Conclude**: tarefa concluída

### Visualizando o loop

Use o flag `--verbose` para ver cada tool call:

```bash
claude --verbose "fix the failing test in auth.test.ts"
```

Você verá cada Read, Grep, Edit e Bash antes do output final.

### `--max-turns`

Por padrão, o agente pode fazer quantas iterações precisar. Para limitar (útil em CI/CD ou para prevenir loops):

```bash
claude -p "task" --max-turns 20
```

## Por que isso importa

**Formule tarefas, não instruções passo a passo.** O loop agentic significa que você pode dizer "adicione autenticação JWT ao endpoint /api/users" em vez de especificar cada arquivo. O agente descobre o que ler.

**O loop é determinístico dentro do contexto.** Se o agente travou ou tomou uma decisão errada, muitas vezes é porque faltou contexto — CLAUDE.md não menciona um padrão, ou a estrutura do projeto é incomum. Adicione contexto, não instruções.

**Iterações custam tokens.** Cada tool call e seu output entram no contexto. Uma sessão com 50 tool calls é muito mais cara que uma com 10. Pedidos mais focados = menos iterações = menor custo.

## Armadilhas

**Loop infinito aparente**: o agente parece não terminar. Causa: tarefa ambígua ou bloqueio não reportado. Diagnóstico: `--verbose`. Solução: reformule a tarefa ou pressione `Esc` para interromper.

**Suposições silenciosas**: o agente assumiu algo errado no passo 1 e nunca corrigiu. Causa: contexto insuficiente. Solução: CLAUDE.md com convenções do projeto.

**Corrida de edições**: o agente edita um arquivo baseado no que leu em loop anterior, mas o arquivo mudou no meio. Pouco comum em uso interativo, mas pode acontecer com subagents paralelos.

## Veja também

- [[03-Dominios/IA/Claude Code/Mental Model/02 - Como Claude Code lê um codebase|02 - Como Claude Code lê um codebase]]
- [[03-Dominios/IA/Claude Code/Mental Model/03 - Tool use|03 - Tool use]]
- [[03-Dominios/IA/Claude Code/Mental Model/04 - Context window|04 - Context window]]
- [[03-Dominios/IA/Claude Code/Mental Model/index|Mental Model]] — índice do galho

## Referências

- [Anthropic — Claude Code overview](https://docs.anthropic.com/pt/docs/claude-code/overview)
- [Anthropic — Agentic patterns](https://docs.anthropic.com/pt/docs/build-with-claude/agents)
