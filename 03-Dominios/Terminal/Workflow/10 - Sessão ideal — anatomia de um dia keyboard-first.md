---
title: "Sessão ideal — anatomia de um dia keyboard-first"
created: 2026-05-24
updated: 2026-05-24
type: concept
progress: backlog
status: seedling
publish: true
fase: magus
tags:
  - terminal
  - workflow
  - magus
  - capstone
  - sintese
aliases:
  - Capstone Workflow
  - Sessão ideal
  - Dia keyboard-first
---

# Sessão ideal — anatomia de um dia keyboard-first

> [!abstract] TL;DR
> Capstone do galho 7 e fechamento da trilha Terminal. Reconta um dia típico do dev keyboard-first do boot ao tear-down, integrando galhos 1-7. Cenário hipotético neutro (alice, dev backend, feature nova). Cada momento aciona uma ou mais notas anteriores via wikilink. Decisões em pontos de bifurcação. NÃO re-explica nada — assume galhos 1-7 dominados.

## Cenário

Alice é dev backend num monorepo Python/TypeScript. Hoje começa uma feature de autenticação OAuth que vai durar ~3 dias. Trabalha em laptop Ubuntu 24.04 + segundo monitor; usa Zellij + Neovim/LazyVim + Lazygit + dotfiles versionados com chezmoi.

## Fluxo (cronológico)

### Boot (08h00–08h15)

Alice abre o emulator de terminal e roda:

```bash
work codex-oauth
```

A função `work` (do `~/.zshrc`) faz: `zoxide query codex-oauth` → `cd` → `zellij a -c codex-oauth` com layout default. Vê 3 tabs (code/git/server). Lazygit já roda na tab "git".

→ Referência: [[04 - Setup matinal e tear-down]], [[02 - Anatomia da sessão de trabalho]].

### Onboard de contexto (08h15–08h45)

Não trabalha nessa feature há 3 dias. Lê scratch file pra restaurar contexto:

```bash
nvim ~/scratch/codex-oauth-todo.md
# 2026-05-21 EOD: parei em src/auth/oauth.ts:142, falta caso edge: refresh token sem expiração explícita
```

Faz onboard rápido do estado atual:

```bash
eza --tree -L 2 --git-ignore src/auth/
rg "TODO|FIXME" src/auth/
lazygit  # ver últimos commits
```

→ Referência: [[03 - Onboarding em projeto novo]].

### Deep work bloco 1 (08h45–11h00)

Alice ativa focus mode (Alt-f no Zellij), maximiza a tab "code". Abre `:Telescope find_files`, escolhe `src/auth/oauth.ts`. Vai até linha 142. Comunica ao time no Slack: "deep work até 11h, DM só pra emergência real". DND ativado.

Trabalha. Usa atalhos de leader key (`<leader>ff`, `<leader>fg`, `gd` LSP definition). Periodicamente, salva session: `:mksession!`.

→ Referência: [[09 - Transições de contexto]], [[06 - Ergonomia das mãos]].

### Pausa intencional (11h00–11h15)

Alice fecha o laptop. Caminha 5min, alonga pulso, bebe água. NÃO checa Slack/email.

→ Referência: [[06 - Ergonomia das mãos]], [[09 - Transições de contexto]].

### Code review urgente (11h15–11h45)

DM do tech lead: "tem 10min pra olhar PR #1234? bloqueia release". Alice abre uma worktree pra não perder estado da feature:

```bash
git worktree add ~/repos/codex-myproj-review-1234 main
cd ~/repos/codex-myproj-review-1234
gh pr checkout 1234
```

Nova sessão Zellij é criada. Alice abre lazygit, lê diff por arquivo, anota observações em `review-notes.md` em pane paralelo:

```bash
gh pr review 1234 --request-changes --body "$(cat review-notes.md)"
```

Detach da sessão de review, volta pra sessão de feature:

```bash
zellij a codex-oauth
```

Worktree fica pra futura limpeza.

→ Referência: [[07 - Worktrees + Zellij paralelos]], [[05 - Code review no terminal]].

### Almoço (12h00–13h00)

Sessão Zellij detached — estado preservado.

### Refactoring multi-arquivo (14h00–15h30)

Alice percebe que o nome `validateToken` deveria ser `verifyToken` (alinhar com vocabulário do RFC). Refactor toca ~20 ocorrências em 12 arquivos.

```bash
# Mapear
rg "\bvalidateToken\b" --stats
```

```text
# Editor: LSP rename pelo símbolo
# Cursor em `validateToken` → <leader>rn → verifyToken → Enter
```

```bash
# Verificar resíduos (comments, strings, docs)
rg "validateToken"
# Resta uma referência em docs/oauth.md
```

Pra resíduos não-código, usa quickfix:

```text
:grep "validateToken"
:copen
:cdo s/validateToken/verifyToken/gc
```

Roda testes; tudo passa.

→ Referência: [[08 - Refactoring multi-arquivo]].

### Sync com time (15h30–16h00)

Tab "sync" efêmera. Alice abre browser pra meet — único momento do dia que sai do terminal.

→ Referência: [[01 - Filosofia keyboard-first — quando vale e quando não]] (quando NÃO).

### Deep work bloco 2 (16h00–17h30)

Continua feature. Implementa caso edge do refresh token.

### Tear-down (17h30–17h45)

Alice atualiza scratch file:

```bash
nvim ~/scratch/codex-oauth-todo.md
# 2026-05-24 EOD: refactor validateToken→verifyToken feito; falta caso edge refresh sem expiração;
# amanhã: começar tests pro caso edge
```

Salva nvim session, detach Zellij (`zellij d` ou Ctrl-Q). Lazygit commit último WIP. Não usa `zellij k` (preserva pra amanhã).

→ Referência: [[04 - Setup matinal e tear-down]].

## Decisões em pontos de bifurcação

### Quando voltar pro browser?

- Threads de discussão longas em PR (>3 níveis aninhados)
- Discussions GitHub (não-código)
- Meetings, video calls
- Browsing exploratório (busca por docs externas)

→ [[01 - Filosofia keyboard-first — quando vale e quando não]] cobre limites.

### Quando worktree NÃO compensa?

- Mudança de <30min ("vai e volta rápido"); stash é mais barato
- Branch tem `node_modules` pesado que precisa re-install (a menos que monorepo + pnpm)
- DB local exige migração que vai entrar em conflito

→ [[07 - Worktrees + Zellij paralelos]].

### Quando sair do deep work?

- Mensagem real de emergência (não DM "tem 5min?")
- Pausa programada (Pomodoro)
- Notou que perdeu o flow há +15min (não vai voltar)

→ [[09 - Transições de contexto]].

### Quando reescrever a config vs aceitar default?

- Defaults inutilizáveis (lentos, conflitam) → reescrever
- Defaults funcionam mas estranhos → aceitar e adaptar-se
- Customização que beneficia <10x/semana → não vale

→ [[06 - Ergonomia das mãos]].

### Quando aceitar GUI?

- Diff visual side-by-side (alguns devs preferem)
- Code coverage report visual
- Profiling/flamegraphs (interativo)
- Quando o time inteiro está em uma ferramenta GUI

→ [[01 - Filosofia keyboard-first — quando vale e quando não]].

## Em inglês

Termos vindos da composição:
- **fluxo cronológico** — *chronological flow*. "O fluxo cronológico do dia é o que dá o esqueleto da sessão."
- **dia keyboard-first** — *keyboard-first day*. "Cada dia keyboard-first começa com setup matinal e termina com tear-down."
- **bifurcação de decisão** — *decision branch point*. "Em cada bifurcação de decisão, escolha consciente entre terminal e GUI."
- **sessão de trabalho** — *work session*. "A sessão de trabalho persistente é a unidade básica."
- **bloco de deep work** — *deep work block*. "O bloco de deep work matinal é a janela mais produtiva."
- **onboard de contexto** — *context onboarding*. "Onboard de contexto pode levar 30min em features paradas."
- **pausa intencional** — *intentional break*. "Pausa intencional não é interrupção; é regeneração."
- **fechamento limpo** — *clean shutdown*. "Fechamento limpo da sessão preserva contexto pra amanhã."
- **estado preservado** — *preserved state*. "Detach garante estado preservado; kill descarta."
- **tese-em-ato** — *thesis-in-act*. "Capstone como tese-em-ato: a teoria vira prática integrada."

## Veja também

- [[01 - Filosofia keyboard-first — quando vale e quando não]]
- [[02 - Anatomia da sessão de trabalho]]
- [[03 - Onboarding em projeto novo]]
- [[04 - Setup matinal e tear-down]]
- [[05 - Code review no terminal]]
- [[06 - Ergonomia das mãos]]
- [[07 - Worktrees + Zellij paralelos]]
- [[08 - Refactoring multi-arquivo]]
- [[09 - Transições de contexto]]
- [[03-Dominios/Terminal/Workflow/index|MOC do galho]]
- [[03-Dominios/Terminal/Editor/index|Editor (galho 1)]]
- [[03-Dominios/Terminal/Shell/index|Shell (galho 2)]]
- [[03-Dominios/Terminal/Multiplexer/index|Multiplexer (galho 3)]]
- [[03-Dominios/Terminal/TUIs/index|TUIs de Dev (galho 4)]]
- [[03-Dominios/Terminal/Dotfiles/index|Dotfiles (galho 5)]]
- [[03-Dominios/Terminal/CLI Utils/index|CLI Utils (galho 6)]]
- [[03-Dominios/Terminal/index|Trilha Terminal]]
- [[Dicionário do Terminal#capstone|capstone]]

## Referências

(sem refs externas; capstone é síntese)
