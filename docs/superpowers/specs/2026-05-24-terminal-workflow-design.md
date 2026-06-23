---
title: "Spec — Galho 7 da trilha Terminal (Workflow)"
date: 2026-05-24
author: Josenaldo
status: draft
type: spec
publish: false
---

# Spec — Galho 7 da trilha Terminal (Workflow)

## 1. Contexto e motivação

Este é o **sétimo e último galho** da trilha Terminal (roadmap em `docs/superpowers/specs/2026-05-18-trilha-terminal-design.md`; galhos 1-6 já entregues). Pressupõe leitura do roadmap e familiaridade com o vocabulário dos galhos anteriores: Editor (Neovim/LazyVim), Shell (Zsh/p10k), Multiplexer (Zellij), TUIs (Lazygit/Lazydocker), Dotfiles, CLI Utils.

O roadmap original (2026-05-18) previa galho 7 com **7 notas focadas em playbooks puros** (code review terminal, onboarding, debug container, worktrees+zellij, edição multi-arquivo, commit estruturado, refactoring). Durante o brainstorming desta sessão (2026-05-24), o escopo foi expandido pra **10 notas em 50/50 playbooks + meta-práticas**, com um capstone híbrido sintetizando a trilha inteira.

**Tese do galho:** trabalho fluido no terminal não é só recombinar ferramentas — é também ter modelo mental, ergonomia e gestão de contexto que sustentem essa composição. Playbooks mostram **o quê**; meta-práticas mostram **o porquê**. O capstone fecha mostrando o **como** integrado, em forma de tese-em-ato (anatomia de um dia keyboard-first).

**Todos os exemplos** das notas são neutros (`alice`, `bob`, `myproj`) ou hipotéticos explícitos (`# hipotético: ...`). Sem fabricação de uso pessoal — não há fluxo nem máquina nem identidade real do usuário sendo descrita.

## 2. Objetivo

Produzir, em uma sessão de execução dedicada, **10 notas atômicas + 1 MOC do galho + bloco novo no Dicionário do Terminal + ativação do wikilink no tronco** em `03-Dominios/Tecnologia/Terminal/Workflow/` e `03-Dominios/Tecnologia/Terminal/`, todas `publish: true`, em PT-BR, distribuídas em 3 fases (3 Iniciado + 4 Adepto + 3 Magus).

A trilha precisa ser:

- **Pedagógica** — leitor que terminou os galhos 1-6 entende ao final de Iniciado por que keyboard-first compensa e quando NÃO; ao final de Adepto sabe operar 4 playbooks reais; ao final de Magus consegue compor um dia de trabalho próprio.
- **Honesta** — listar limites (onde keyboard-first NÃO ajuda). Comparar fluxos com alternativas web/GUI sem hype. Quando uma escolha depende de gosto, dizer.
- **Atômica** — cada nota cobre um tópico bem-delimitado (≤300 linhas; capstone pode ir até 400). Cross-references ricos.
- **Sintética no capstone** — capstone NÃO re-explica ferramentas; **compõe**. Tese-em-ato.

## 3. Saídas concretas

### 3.1. Notas (`03-Dominios/Tecnologia/Terminal/Workflow/`)

Pasta nova, flat. 10 notas + 1 MOC:

#### Iniciado (3 notas — enquadramento + primeira vitória)

| # | Nota | Tipo | Foco |
|---|------|------|------|
| 01 | Filosofia keyboard-first — quando vale e quando NÃO | Meta | Argumento honesto: velocidade não é tudo. Quando teclado-first compensa (texto/código/navegação) e quando NÃO (graphics, ER design, exploração visual densa). Custo de aprendizado vs ganho. |
| 02 | Anatomia da sessão de trabalho | Meta | Vocabulário: sessão, tab, pane, layout, focus mode. Como pensar em "espaço de trabalho" no terminal (Zellij/tmux como WM). Modelo mental antes de receita. |
| 03 | Onboarding em projeto novo | Playbook | Fluxo: repo desconhecido → mapa mental em 30min. Comandos concretos: `zoxide` cd, `eza --tree -L 2`, `rg "TODO\|FIXME"`, telescope live_grep, `bat README.md`, `lazygit log`. |

#### Adepto (4 notas — operacionalidade)

| # | Nota | Tipo | Foco |
|---|------|------|------|
| 04 | Setup matinal e tear-down | Playbook | Sessões Zellij named (`zellij -s projeto`), restore de layout KDL, abrir lazygit/nvim em panes específicos. Tear-down: detach vs kill, persistência via atuin. Hábitos de "começar" e "encerrar". |
| 05 | Code review no terminal | Playbook | gh CLI (`pr list`, `pr checkout`) + lazygit (diff por arquivo) + delta (diff colorido) + nvim (anotações inline). Quando voltar pro browser (UI de discussions, threads longas). |
| 06 | Ergonomia das mãos | Meta | Leader keys cross-tool (Space no nvim, prefix no Zellij). Atalhos consistentes que valem aprender. CapsLock→Ctrl. Custom keymaps: quando customizar e quando aceitar default. RSI básico. |
| 07 | Worktrees + Zellij paralelos | Playbook | `git worktree add` + sessão Zellij por worktree. Multi-task sem stash. Quando vale (review enquanto trabalha) e quando complica (`node_modules`, lock-files, estado de DB compartilhado). |

#### Magus (3 notas — síntese)

| # | Nota | Tipo | Foco |
|---|------|------|------|
| 08 | Refactoring multi-arquivo | Playbook | `rg` pra mapear padrão → nvim quickfix (`:cdo`, `:cfdo`) ou `:%s` cross-file → LSP rename pra refactor type-aware. Cuidado com `:cdo` quando mudanças invalidam matches. |
| 09 | Transições de contexto | Meta | Switching cost cognitivo. Deep work vs shallow tasks. Sessions efêmeras (oneshot) vs persistentes (named). Política de tabs (uma tab = um contexto). Como fechar contextos sem perder estado. |
| 10 | **Capstone — Sessão ideal: anatomia de um dia keyboard-first** | Capstone (META+PLAYBOOK) | Tese-em-ato. Cenário: dia típico do dev keyboard-first. Fluxo cronológico do boot ao tear-down, integrando galhos 1-7. Decisões em pontos de bifurcação. NÃO re-explica nada. |

### 3.2. MOC do galho (`Workflow/index.md`)

Estrutura:

```markdown
---
title: "Workflow"
type: moc
publish: true
created: 2026-05-24
updated: 2026-05-24
status: growing
tags: [terminal, workflow, moc]
aliases: [MOC Workflow, Galho 7]
---
# Workflow

> [!abstract] TL;DR
> Galho 7 e último da trilha Terminal. 5 playbooks que recombinam ferramentas dos galhos 1-6 + 4 meta-práticas (filosofia, anatomia da sessão, ergonomia, transições de contexto) + 1 capstone sintetizando a trilha inteira em forma de "anatomia de um dia keyboard-first". 10 notas (3 Iniciado + 4 Adepto + 3 Magus).

[parágrafo de contextualização: explicar que este galho NÃO é mais uma ferramenta, é a tese sobre como recombinar tudo]

## Conteúdo

### Iniciado
- [[01 - Filosofia keyboard-first — quando vale e quando não]]
- [[02 - Anatomia da sessão de trabalho]]
- [[03 - Onboarding em projeto novo]]

### Adepto
- [[04 - Setup matinal e tear-down]]
- [[05 - Code review no terminal]]
- [[06 - Ergonomia das mãos]]
- [[07 - Worktrees + Zellij paralelos]]

### Magus
- [[08 - Refactoring multi-arquivo]]
- [[09 - Transições de contexto]]
- [[10 - Sessão ideal — anatomia de um dia keyboard-first]]

## Tools usadas por cada nota

| Nota | Galho 1 (Editor) | Galho 2 (Shell) | Galho 3 (Multiplexer) | Galho 4 (TUIs) | Galho 5 (Dotfiles) | Galho 6 (CLI Utils) |
|------|------|------|------|------|------|------|
| 01 | — | — | — | — | — | — |
| 02 | — | — | Zellij conceitos | — | — | — |
| 03 | nvim+telescope | — | — | lazygit | — | zoxide, eza, rg, bat |
| 04 | nvim | — | Zellij sessions+layouts | lazygit | dotfiles config | atuin |
| 05 | nvim | — | Zellij panes | lazygit | — | delta, bat, gh CLI |
| 06 | nvim keymaps | Zsh keybindings | Zellij keybindings | — | — | — |
| 07 | nvim | — | Zellij named sessions | lazygit | — | — |
| 08 | nvim+quickfix+LSP | — | — | — | — | rg |
| 09 | — | — | Zellij sessions | — | — | atuin |
| 10 | tudo | tudo | tudo | tudo | tudo | tudo |

## Rotas alternativas

- **Mínimo viável (Iniciado primeiro):** `01` → `02` → `03` — entende filosofia, vocabulário, primeiro fluxo concreto.
- **Quer ser produtivo já:** `03` → `04` → `05` — onboarding, setup matinal, code review. Pula meta-prática.
- **Quer entender modelo mental:** `01` → `02` → `06` → `09` — pula playbooks, foca nas 4 meta-práticas.
- **Refactor pesado:** `08` direto (assume Editor + CLI Utils dominados).
- **Capstone:** `10` — só depois de ter lido as 9 anteriores.

## Veja também

- [[Dicionário do Terminal]]
- [[03-Dominios/Tecnologia/Terminal/index|Trilha Terminal]]
- [[03-Dominios/Tecnologia/Terminal/Editor/index|Editor (galho 1)]]
- [[03-Dominios/Tecnologia/Terminal/Shell/index|Shell (galho 2)]]
- [[03-Dominios/Tecnologia/Terminal/Multiplexer/index|Multiplexer (galho 3)]]
- [[03-Dominios/Tecnologia/Terminal/TUIs/index|TUIs de Dev (galho 4)]]
- [[03-Dominios/Tecnologia/Terminal/Dotfiles/index|Dotfiles (galho 5)]]
- [[03-Dominios/Tecnologia/Terminal/CLI Utils/index|CLI Utils (galho 6)]]
```

### 3.3. Tronco (`03-Dominios/Tecnologia/Terminal/index.md`)

Mudanças:

- Linha 33: `Workflow — galho 7 (planejado): playbooks cross-tool` vira:
  ```
  - [[03-Dominios/Tecnologia/Terminal/Workflow/index|Workflow]] — galho 7: playbooks cross-tool (onboarding, review, worktrees, refactoring) + meta-práticas (filosofia keyboard-first, ergonomia, transições de contexto) + capstone (anatomia de um dia)
  ```
- Frontmatter: `progresso: andamento` → `progresso: completo` (trilha fechada com 7 galhos)
- Frontmatter: `updated: 2026-05-21` → `updated: 2026-05-24`
- TL;DR: bump "~57 notas" → "~67 notas" e refletir que a trilha está completa

### 3.4. Dicionário do Terminal (`03-Dominios/Tecnologia/Terminal/Dicionário do Terminal.md`)

Novo bloco `## Workflow` com **10-15 verbetes** próprios de meta-práticas/workflow. Ordem alfabética (case-insensitive). Cada verbete com "Veja também" linkando a nota relevante.

Candidatos a verbetes (mapa indicativo; lista final definida durante execução):

| Verbete | Conceito |
|---------|----------|
| capstone | Nota-síntese que compõe ao invés de re-explicar |
| context switching cost | Custo cognitivo de alternar entre contextos |
| deep work | Trabalho focado de longa duração |
| dotfiles bootstrap | Setup automatizado de máquina nova (cf. galho 5) |
| ephemeral session | Sessão Zellij sem nome, descartada ao fechar |
| focus mode | Modo de Zellij/tmux que esconde UI auxiliar |
| keyboard-first | Filosofia: teclado prioritário; mouse opcional |
| leader key | Tecla de prefixo pra atalhos custom (Space, Ctrl-A) |
| named session | Sessão Zellij persistente com nome |
| quickfix | Lista de erros/matches do Neovim, navegável |
| RSI | Repetitive Strain Injury; ergonomia importa |
| shallow task | Tarefa rápida, baixa profundidade cognitiva |
| switching cost | Custo (de contexto) ao trocar de tarefa |
| tear-down | Encerramento intencional da sessão de trabalho |
| worktree | Git: múltiplos working trees do mesmo repo |

Frontmatter: bump `updated:` pra `2026-05-24`.

### 3.5. Resumo de outputs

| Item | Quantidade | Localização |
|------|-----------|-------------|
| Notas atômicas novas | 10 | `Terminal/Workflow/0X - ...md` |
| MOC do galho | 1 | `Terminal/Workflow/index.md` |
| Tronco atualizado | 1 | `Terminal/index.md` |
| Dicionário atualizado | 1 | `Terminal/Dicionário do Terminal.md` |

**Total:** 11 arquivos novos + 2 modificados = **13 arquivos tocados** na sessão de execução.

## 4. Padrão das notas

### 4.1. Frontmatter (notas atômicas)

```yaml
---
title: "<título>"
type: concept
publish: true
fase: iniciado | adepto | magus
tags:
  - terminal
  - workflow
  - <fase>
  - <tema-slug>     # ex: keyboard-first, sessao, ergonomia, worktree
created: 2026-05-24
updated: 2026-05-24
status: seedling
aliases:
  - <termo-curto>
---
```

### 4.2. Estrutura de notas regulares (notas 01-09)

```markdown
# <Título>

> [!abstract] TL;DR
> <3-5 linhas. Tese curta + 2 fatos operacionais.>

## O que é / Como funciona

### <conceito 1>
### <conceito 2>
[modelo mental, vocabulário, componentes; tabelas quando aplicável]

## Na prática

### <cenário 1>
### <cenário 2>
[comandos, receitas, exemplos concretos; alias/funções sugeridas]

## Armadilhas

### (1) <título da armadilha>
**Causa:** ...
**Sintoma:** ...
**Como detectar:** ...
**Solução:** ...

[≥4 armadilhas por nota]

## Em inglês

Termos técnicos que aparecem ao ler docs e fóruns sobre o tópico:

- **<PT>** — *<EN>*. "<frase em PT usando o termo>"
[8-10 bullets]

## Veja também

- [[<nota irmã>]]
- [[03-Dominios/Tecnologia/Terminal/Workflow/index|MOC do galho]]
- [[03-Dominios/Tecnologia/Terminal/index|Trilha Terminal]]
- [[Dicionário do Terminal#<verbete>|<verbete>]]

## Referências

- <docs oficiais quando aplicável>
- <posts canônicos opcionais>
```

### 4.3. Estrutura do capstone (nota 10)

Capstone NÃO segue o padrão acima. Compõe ao invés de re-explicar.

```markdown
# Sessão ideal: anatomia de um dia keyboard-first

> [!abstract] TL;DR
> Capstone do galho 7 e fechamento da trilha Terminal. Reconta um dia típico do dev keyboard-first do boot ao tear-down — quando começa cada playbook, quando se aplica cada meta-prática, quando voltar pra GUI. Não re-explica ferramentas (assume galhos 1-7 dominados); decisões em cada bifurcação. Tese-em-ato.

## Cenário

[setup hipotético neutro: alice, dev backend, primeiro dia trabalhando num feature novo]

## Fluxo (cronológico)

### Boot (08h)
[setup matinal → Zellij named session → restore layout → atuin import]

### Onboard (08h30)
[chega num módulo do repo desconhecido → P1 onboarding]

### Trabalho profundo (09h-12h)
[worktree pro feature + sessão paralela; deep work; transição de contexto evitada]

### Review (13h)
[PR review com gh + lazygit + delta + nvim]

### Refactoring (14h-16h)
[P5 refactoring multi-arquivo com rg + quickfix + LSP]

### Tear-down (18h)
[detach vs kill, atuin sync, encerramento]

## Decisões em pontos de bifurcação

### Quando voltar pro browser?
### Quando worktree NÃO compensa?
### Quando sair do foco profundo?

[5-7 dilemas reais, cada um com critério decisório]

## Em inglês

[10 bullets de termos vindos da composição]

## Veja também

[wikilink pras 9 notas anteriores + MOCs dos 6 galhos anteriores + Dicionário]

## Referências

[opcional; capstone normalmente não tem]
```

### 4.4. Padrões de qualidade (já estabelecidos nos galhos 1-6)

- **TL;DR:** callout `[!abstract]`, 3-5 linhas, com tese + 2 fatos operacionais.
- **Armadilhas:** mínimo 4 por nota regular. Padrão `### (N) Título` + 4 labels (`**Causa:**`, `**Sintoma:**`, `**Como detectar:**`, `**Solução:**`).
- **Em inglês:** 8-10 bullets no padrão `**PT** — *EN*. "frase em PT."`.
- **Wikilinks:** "Veja também" sempre incluindo MOC do galho + tronco + Dicionário; cross-galho quando aplicável.
- **Sem fabricação:** sem `josenaldo`, `/home/josenaldo/`, "no meu setup", "no meu fluxo". Exemplos com `alice`, `bob`, `myproj` ou hipóteses explícitas.
- **Versões hedged:** "0.4x+; verifique localmente" — herdado do galho 6.
- **Comandos testáveis:** validados em docs/man ou (quando possível) localmente.

## 5. Estratégia de execução

### 5.1. Esta sessão (apenas spec + plano)

1. Brainstorming → spec aprovado (em curso)
2. Spec doc salvo em `docs/superpowers/specs/2026-05-24-terminal-workflow-design.md` + commit
3. User review do spec
4. `writing-plans` → plano em `docs/superpowers/plans/2026-05-24-terminal-workflow-execution.md` + commit
5. Sem implementação nesta sessão

### 5.2. Próxima sessão (execução)

- **Pré-flight:** checar versões de `gh`, `git worktree`, Zellij (já capturadas em galhos anteriores; reusar).
- **Implementação task a task,** uma nota por commit, com `git add <path>` explícito (**nunca `git add -A`**).
- **Cross-task review subagent ao final** (Sonnet, **não 1M context** — dá erro de créditos).
- **Validação:** `verificar-wikilinks` na pasta `03-Dominios/Tecnologia/Terminal/Workflow/` + Dicionário consistente + tronco com wikilink ativo + frontmatter do tronco em `progresso: completo`.

### 5.3. Hard constraints (continuam de galhos anteriores)

- Sem `Co-Authored-By: Claude` em commits.
- Sem `--no-verify`.
- Subagent dispatches em Sonnet com contexto curto. 1M context não é usado.
- Stage explícito de arquivos do galho — não tocar nas mudanças não-relacionadas no working tree.
- Sem fabricação de identidade/setup do usuário.

## 6. Relação com galhos anteriores

| Galho | Como o galho 7 usa |
|-------|---------------------|
| Editor (1) | nvim + telescope (notas 03, 04, 05, 06, 08, 10); quickfix + LSP (08, 10) |
| Shell (2) | Zsh keybindings (06); funções/aliases em receitas (03, 04, 10) |
| Multiplexer (3) | Zellij sessions + layouts + named sessions (02, 04, 07, 09, 10) |
| TUIs (4) | lazygit (03, 04, 05, 07, 10); lazydocker mencionado de passagem se aplicável |
| Dotfiles (5) | configs versionadas referenciadas em setup matinal (04, 10) |
| CLI Utils (6) | zoxide, eza, rg, bat, delta, atuin, fzf — composições concretas em 03, 04, 05, 08, 10 |

Notas do galho 7 **não re-explicam** ferramentas dos galhos anteriores — apenas referenciam via wikilink e usam em receitas.

## 7. Volume estimado

| Fase | Notas | Tipo | Notas estimadas (linhas) |
|------|-------|------|--------------------------|
| Iniciado | 3 | 2M + 1P | ~250 linhas/nota |
| Adepto | 4 | 1M + 3P | ~280 linhas/nota |
| Magus | 3 | 1M + 1P + 1C | ~280 (M, P) / ~400 (capstone) |
| **Total** | **10** | **4M + 5P + 1C** | **~2.900 linhas totais** |

+ MOC do galho (~120 linhas)
+ ~10-15 verbetes novos no Dicionário (~200 linhas)
+ Tronco atualizado (3 linhas mudadas)

## 8. Critério de pronto

A sessão de execução estará pronta quando:

- [ ] 11 arquivos em `03-Dominios/Tecnologia/Terminal/Workflow/` (10 notas + MOC)
- [ ] Todas as 10 notas com frontmatter consistente (`publish: true`, `fase:`, tags corretas)
- [ ] Notas 01-09 com TL;DR `[!abstract]`, ≥4 armadilhas no padrão completo, 8-10 bullets "Em inglês"
- [ ] Capstone (10) compondo (sem re-explicar) e referenciando as 9 anteriores
- [ ] `## Workflow` no Dicionário com 10-15 verbetes em ordem alfabética, todos com "Veja também"
- [ ] `Dicionário do Terminal` com `updated: 2026-05-24`
- [ ] Tronco (`Terminal/index.md`) com wikilink ativo pro galho 7 e `progresso: completo`
- [ ] `verificar-wikilinks 03-Dominios/Tecnologia/Terminal/Workflow/` → 0 broken
- [ ] Cross-task review subagent (Sonnet) sem Critical/Important pendentes
- [ ] Nenhum commit com `Co-Authored-By: Claude`
- [ ] Nenhum `git add -A`; apenas stages explícitos de arquivos do galho

## 9. Próximos passos pós-spec

1. **Esta sessão:** spec aprovado → `writing-plans` → plano de execução com task list completa
2. **Sessão seguinte:** execução do plano (10 notas + MOC + Dicionário + tronco)
3. **Após galho 7:** trilha Terminal está completa. Possível próximo: trilha nova (não definida ainda).
