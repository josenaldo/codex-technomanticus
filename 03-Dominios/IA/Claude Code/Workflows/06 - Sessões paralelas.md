---
title: "Sessões paralelas — tmux + worktrees"
type: concept
publish: true
created: 2026-05-13
updated: 2026-05-13
status: seedling
tags:
  - claude-code
  - workflows
  - sessoes-paralelas
  - worktrees
  - tmux
---

# Sessões paralelas — tmux + worktrees

> [!abstract] TL;DR
> Claude Code pode rodar múltiplas sessões simultâneas em worktrees git diferentes — cada agente trabalha numa branch isolada sem interferir nos arquivos do outro. O setup padrão usa `git worktree add` para criar cópias de trabalho e `tmux` (ou múltiplos terminais) para rodar sessões em paralelo. Ideal para: implementar features independentes simultaneamente, ou trabalhar numa feature enquanto outra está em review.

## O problema de sessões únicas

Sem paralelismo:
- Feature A toma 4h → Feature B começa → 4h → total: 8h sequenciais
- Não dá para trabalhar em feature B enquanto feature A está em review
- Uma sessão longa polui o contexto — o agente "mistura" o trabalho das features

## Git worktrees — a peça central

`git worktree add` cria um segundo diretório de trabalho ligado ao mesmo repositório. Cada worktree pode estar numa branch diferente.

```bash
# Worktree para feature A
git worktree add ../meu-projeto-feat-a feat/payment-integration

# Worktree para feature B  
git worktree add ../meu-projeto-feat-b feat/user-notifications

# Verificar worktrees
git worktree list
```

Resultado:
```
/home/user/meu-projeto          (main)
/home/user/meu-projeto-feat-a   (feat/payment-integration)
/home/user/meu-projeto-feat-b   (feat/user-notifications)
```

Cada diretório é uma cópia de trabalho independente — arquivos separados, sem interferência.

## Setup com tmux

```bash
# Nova sessão tmux com dois painéis
tmux new-session -d -s dev
tmux split-window -h

# Painel esquerdo: feature A
tmux send-keys -t dev:0.0 "cd ../meu-projeto-feat-a && claude" Enter

# Painel direito: feature B
tmux send-keys -t dev:0.1 "cd ../meu-projeto-feat-b && claude" Enter

# Attach à sessão
tmux attach -t dev
```

Ou simplesmente: dois terminais, cada um com `cd` para seu worktree e `claude` rodando.

## Setup com múltiplos terminais

Mais simples para quem não usa tmux:

```bash
# Terminal 1
cd ../meu-projeto-feat-a
claude

# Terminal 2
cd ../meu-projeto-feat-b
claude
```

Cada instância do Claude Code é independente — contexto, histórico, permissões.

## Padrões de uso

### Feature paralela

```
Terminal 1 — feat-a:
"Implemente integração com gateway de pagamento Stripe.
Arquivos: src/services/payment.ts, src/routes/payment.ts.
Siga as convenções do CLAUDE.md."

Terminal 2 — feat-b:
"Implemente sistema de notificações por email para eventos
de pedido. Use o SendGrid client em src/utils/mailer.ts."
```

Ambos trabalhando simultaneamente. Merges independentes.

### Review + development simultâneo

```
Terminal 1 — main:
[revisar PR, responder comentários, fazer pequenas correções]

Terminal 2 — nova feature:
[começar próxima feature enquanto o PR está em review]
```

### Experimento vs. produção

```
Terminal 1 — branch experimental:
"Tente refatorar OrderService para usar event sourcing.
Não precisa ser perfeito — quero explorar a abordagem."

Terminal 2 — branch main:
[trabalho normal de produção]
```

## Limpeza de worktrees

Depois que a branch foi mergeada:

```bash
# Remove o worktree (o diretório e o registro)
git worktree remove ../meu-projeto-feat-a

# Remove branches mergeadas
git branch -d feat/payment-integration

# Limpar worktrees stale (branch deletada remotamente)
git worktree prune
```

## Cuidados

**CLAUDE.md compartilhado**: todos os worktrees leem o mesmo `.claude/CLAUDE.md` do repositório. Qualquer mudança no CLAUDE.md de uma worktree afeta todas — ou commite ou mantenha separado.

**settings.local.json**: cada worktree tem seu próprio `.claude/settings.local.json` (não está no git). Você pode ter configurações diferentes por worktree.

**Conflitos de porta**: se dois agentes tentam rodar `npm run dev` simultaneamente, ambos vão tentar usar a mesma porta. Use portas diferentes:

```bash
# Worktree A
PORT=3001 npm run dev

# Worktree B  
PORT=3002 npm run dev
```

**Tarefas independentes**: paralelismo funciona para tarefas que não tocam os mesmos arquivos. Se ambas as features modificam `src/utils/auth.ts`, você vai ter conflito no merge.

## Quando usar

**Use sessões paralelas para:**
- Features em partes diferentes do codebase
- Feature nova + bugfix em produção
- Exploração de abordagem alternativa
- Trabalhar enquanto aguarda review

**Não use para:**
- Tarefas que tocam os mesmos arquivos (vai gerar conflito)
- Quando o contexto entre as tarefas é compartilhado (ex: migração que depende de feature)
- Quando você não consegue focar em dois contextos ao mesmo tempo

## Veja também

- [[03-Dominios/IA/Claude Code/Workflows/07 - Sub-agents e dispatch|07 - Sub-agents e dispatch]] — delegar tarefas a agentes
- [[03-Dominios/IA/Claude Code/Workflows/08 - Multi-agent|08 - Multi-agent]] — coordenar múltiplos agentes
- [[03-Dominios/IA/Claude Code/Time e Automação/index|Time e Automação]] — paralelismo em contexto de time
- [[03-Dominios/IA/Claude Code/Workflows/index|Workflows]] — índice do galho
