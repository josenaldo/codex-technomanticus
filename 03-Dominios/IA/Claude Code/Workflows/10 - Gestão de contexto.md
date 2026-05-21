---
title: "Gestão de contexto — qualidade em sessões longas"
type: concept
publish: true
created: 2026-05-13
updated: 2026-05-13
status: seedling
tags:
  - claude-code
  - workflows
  - contexto
  - sessoes-longas
  - compaction
---

# Gestão de contexto — qualidade em sessões longas

> [!abstract] TL;DR
> Sessões longas degradam a qualidade das decisões do agente — não porque o Claude fica "cansado", mas porque o contexto acumula ruído e o agente pondera conversas antigas junto com as novas. O sinal de alerta é o agente fazendo escolhas inconsistentes com decisões recentes. Gestão de contexto ativa (commits frequentes + /compact + sessions novas) mantém a qualidade estável.

## Por que o contexto degrada

O modelo de linguagem pondera todo o contexto disponível ao tomar uma decisão. Numa sessão longa:

- Decisões revertidas ainda estão no contexto e podem ser reutilizadas
- Código de iterações antigas influencia novas implementações
- Instruções de tarefas concluídas "poluem" a nova tarefa
- O histórico de debugging de um bug que já foi corrigido ainda está visível

O agente não "esquece" o que foi decidido — ele pondera tudo com peso similar.

## Sinais de degradação de contexto

Fique atento a estes padrões:

**Regressão de decisões**: o agente usa `console.log` depois de várias iterações corrigindo isso.

**Inconsistência de padrões**: numa sessão onde você implementou dois serviços, o terceiro segue um padrão diferente dos dois primeiros — provavelmente porque as implementações anteriores "competem" no contexto.

**Referências a código antigo**: o agente menciona uma função que você refatorou há 20 mensagens como se ainda existisse.

**Hesitação em decisões simples**: o agente pede confirmação de coisas que estavam claramente estabelecidas no início da sessão — sinal de que a instrução original está "diluída" pelo contexto acumulado.

## /compact — compactar o contexto

O comando `/compact` sumariza a sessão atual em um resumo comprimido, descartando os detalhes das mensagens individuais mas preservando as decisões e o estado atual.

```
Quando usar /compact:
- Depois de um commit significativo ("salvei o estado, posso compactar")
- Quando o contexto ultrapassar ~50% da janela
- Quando a tarefa muda de assunto (debugging → nova feature)
- Quando você perceber sinais de degradação
```

**Uso:**
```
/compact
```

Depois do /compact, restate a situação atual:

```
"Compactamos. Estado atual:
- Implementamos PaymentService (commit abc123) — concluído
- WebhookService ainda pendente

Próximo: implementar src/services/webhooks.ts seguindo o mesmo
padrão de PaymentService. Convenções no CLAUDE.md."
```

O restate é importante — o agente não vai "inferir" o que está pendente depois da compactação.

## Commits como pontos de salvamento

A prática mais importante para sessões longas: commitar frequentemente.

```
Benefício 1: ponto de retorno
- Se algo der errado, git revert volta ao estado anterior
- Sem commits → só opção é /compact e reimplementar

Benefício 2: marcador de progresso
- "Já commitamos PaymentService" é informação que pode ser
  incluída no restate após /compact
- O histórico git se torna a fonte de verdade do progresso

Benefício 3: oportunidade natural de /compact
- Depois de cada commit, o estado está "limpo"
- Bom momento para compactar e começar a próxima tarefa com contexto fresco
```

## Sessões novas para fases distintas

Para projetos que duram mais de uma sessão, inicie uma sessão nova para cada fase distinta em vez de continuar a mesma sessão por dias:

```
Sessão 1: implementar PaymentService e WebhookService
→ Commite tudo, feche a sessão

Sessão 2: implementar UI de checkout
→ O agente começa com contexto limpo
→ O CLAUDE.md descreve o projeto, as implementações anteriores
  estão no código — não precisa do histórico da Sessão 1

Sessão 3: testes e2e
→ Mesma coisa
```

O CLAUDE.md e o código são o "estado persistido" entre sessões. O histórico de mensagens não precisa persistir.

## Quando NÃO usar /compact

`/compact` descarta detalhes. Não use quando:

- Você está no meio de um debugging onde o histórico de hipóteses importa
- O agente está trabalhando num problema complexo e você precisa do contexto completo para revisar as decisões
- A sessão ainda está curta e não há degradação visível

Compactar por compactar tem custo: você perde contexto que pode ser útil. Compacte quando há sinal de degradação ou natural checkpoint (commit, mudança de assunto).

## Padrão de sessão saudável

```
Início da sessão:
→ Declare o objetivo e o escopo
→ Aponte os arquivos relevantes
→ Cite convenções críticas (ou confie no CLAUDE.md)

Durante a sessão:
→ Commit depois de cada unidade de trabalho completa
→ /compact + restate quando mudar de assunto ou perceber degradação
→ Se o agente fizer algo inconsistente, corrija e reforce a regra

Fim da sessão (se não concluiu):
→ Commite o estado atual
→ Deixe um comentário temporário // TODO: próximo: X se necessário
→ Próxima sessão começa com um restate do que foi feito e o que falta
```

## Tamanho de sessão como decisão de design

Sessões longas não são inevitáveis — são uma escolha de design. Algumas heurísticas:

- Cada feature em sessão própria
- Cada fase (implementação, refactoring, debugging) em sessão própria
- Cada módulo ou serviço em sessão própria

Sessão curta com contexto limpo > sessão longa com contexto degradado.

## Armadilhas

**Não commitir antes de /compact**: compactar sem commitar significa que se algo der errado no que vem depois, você não tem ponto de retorno fácil.

**Restate vago**: "vamos continuar de onde paramos" depois do /compact não funciona — o agente não sabe onde parou com a mesma precisão que antes. Seja específico no restate.

**Ignorar sinais de degradação**: quando o agente começa a fazer escolhas inconsistentes, é tentador "corrigir e continuar". Mas o contexto vai continuar degradando. Compacte e restate quando ver os sinais.

**/compact no meio de uma tarefa complexa**: compactar quando o agente está no meio de um debugging complexo descarta informação relevante. Finalize a tarefa (ou chegue a um ponto de parada natural) antes de compactar.

## Veja também

- [[03-Dominios/IA/Claude Code/Mental Model/06 - Compaction|06 - Compaction]] — como /compact funciona internamente
- [[03-Dominios/IA/Claude Code/Workflows/03 - Refactoring pesado|03 - Refactoring pesado]] — gestão de contexto em refactors longos
- [[03-Dominios/IA/Claude Code/Configuração/02 - CLAUDE.md anatomia|02 - CLAUDE.md anatomia]] — CLAUDE.md como contexto persistente entre sessões
- [[03-Dominios/IA/Claude Code/Workflows/07 - Sub-agents e dispatch|07 - Sub-agents e dispatch]] — contexto limpo por design via sub-agents
- [[03-Dominios/IA/Claude Code/Workflows/index|Workflows]] — índice do galho
