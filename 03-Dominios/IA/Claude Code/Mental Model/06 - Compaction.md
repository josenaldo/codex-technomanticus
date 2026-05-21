---
title: "Compaction — como o Claude Code gerencia contextos longos"
type: concept
publish: true
created: 2026-05-13
updated: 2026-05-13
status: seedling
tags:
  - claude-code
  - mental-model
  - compaction
  - context
---
# Compaction — como o Claude Code gerencia contextos longos

> [!abstract] TL;DR
> Compaction é o mecanismo que permite continuar sessões quando a context window está quase cheia. O Claude Code resume o histórico de conversa em um snapshot denso, preservando informação essencial e descartando detalhes. Auto compaction acontece automaticamente; `/compact` permite triggerar manualmente com foco explícito. O custo: alguns detalhes são perdidos. A prática saudável é compactar cedo e reiniciar para tarefas não relacionadas.

## O que é

Quando a context window se aproxima do limite, o Claude Code pode compactar a sessão: em vez de ter o histórico completo de tool calls, mensagens e outputs, o contexto passa a ter um **summary** desse histórico seguido pelas mensagens mais recentes em forma completa.

```
Antes da compaction:
[system prompt] [CLAUDE.md] [turn1][tool1][turn2][tool2]...[turn25][tool25]

Depois da compaction:
[system prompt] [CLAUDE.md] [SUMMARY: resumo dos turns 1-20] [turn21][tool21]...[turn25][tool25]
```

## Auto compaction vs manual

### Auto compaction

Acontece automaticamente quando o contexto atinge ~80% da janela disponível. Você verá uma notificação:

```
[Conversation compacted to preserve context]
```

O Claude Code chama a API uma vez para gerar o summary, então continua a sessão com o contexto compactado.

### Manual: `/compact`

```
/compact
```

Trigga compaction quando você decide, independente do tamanho do contexto. Útil antes de entrar em uma fase nova da sessão.

Você pode passar um foco para o summary:

```
/compact Focus on the authentication changes made so far
```

Com foco, o summary prioriza o que você especificou ao resumir — muito mais útil que um summary genérico.

## O que é preservado vs descartado

**Preservado com fidelidade:**
- Decisões de design explícitas ("decidimos usar JWT em vez de sessions")
- Arquivos editados e suas mudanças
- Erros encontrados e como foram resolvidos
- Instruções explícitas do usuário
- Estado final dos trabalhos em andamento

**Comprimido ou descartado:**
- Tool outputs detalhados de chamadas antigas
- Explorações que não levaram a nada
- Conteúdo de arquivos lidos (o arquivo em si não muda — pode ser relido)
- Raciocínio intermediário de turns anteriores

## Por que isso importa

### Continuidade de sessão

Sem compaction, sessões longas travavam ou exigiam reinício. Com compaction, você pode trabalhar em uma feature por horas em uma única sessão.

### Custo

Após compaction, cada novo turn processa menos tokens (o summary é mais denso que o histórico completo). Custo por turn cai.

### Risco de perda de informação

O summary é uma aproximação. Detalhes específicos de turns antigos podem ser perdidos. Se você disse "não use lodash" no turn 3 e a sessão foi compactada duas vezes desde então, o agente pode não lembrar dessa restrição.

**Mitigação:** coloque restrições importantes no CLAUDE.md, não confie só no histórico da sessão.

## Estratégias práticas

### Compactar antes, não depois

```
/compact Focus on the API design decisions made so far
```

Compacte quando a sessão está ~50% do limite, não quando já está 90%. Você tem mais controle sobre o que é preservado.

### CLAUDE.md como âncora

Qualquer coisa que precisa sobreviver entre compactions e entre sessões deve estar no CLAUDE.md. O summary pode perder detalhes; o CLAUDE.md é lido no início de cada sessão.

### Reiniciar para tarefas não relacionadas

Se acabou uma feature e vai começar outra não relacionada, inicie uma nova sessão. Uma sessão compactada com histórico de outra feature é ruído.

### `--resume` com consciência

```bash
claude --resume SESSION_ID
```

Retoma uma sessão (incluindo compacted). Útil para continuar trabalho; mas o contexto é o compacted, não o original completo.

## Armadilhas

**Confiar no histórico para restrições críticas**: "não faça X" dito há 30 turns pode não sobreviver à compaction. Repita restrições importantes ou coloque no CLAUDE.md.

**Compaction automática em momento ruim**: se você está no meio de um refactoring complexo quando a compaction auto dispara, pode perder contexto crítico. Compacte manualmente antes de atingir o limite.

**`/compact` sem foco**: sem um foco explícito, o summary é genérico. Para sessões de debugging, `/compact Focus on the root cause investigation and findings` é muito melhor que `/compact` sozinho.

## Veja também

- [[03-Dominios/IA/Claude Code/Mental Model/04 - Context window|04 - Context window]]
- [[03-Dominios/IA/Claude Code/Mental Model/07 - Tokens e custo|07 - Tokens e custo]]
- [[03-Dominios/IA/Claude Code/Configuração/index|Configuração]] — CLAUDE.md como âncora entre sessões
- [[03-Dominios/IA/Claude Code/Mental Model/index|Mental Model]] — índice do galho

## Referências

- [Claude Code — Managing context](https://docs.anthropic.com/pt/docs/claude-code/memory)
