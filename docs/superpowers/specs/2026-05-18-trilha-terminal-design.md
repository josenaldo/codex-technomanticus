# Design: Trilha Terminal (Roadmap)

**Data:** 2026-05-18
**Status:** rascunho
**Domínio:** `03-Dominios/Terminal/`
**Tipo:** roadmap da trilha (umbrella) — cada galho terá seu próprio spec + execução

---

## Contexto

O usuário acaba de instalar um stack de ferramentas TUI/keyboard-first pra trabalhar no terminal: **Neovim + LazyVim, Lazygit, Lazydocker, Zellij, Zsh + Oh-My-Zsh + Powerlevel10k**. Ainda não domina o conjunto — quer uma trilha de domínio nova que sirva tanto como referência por ferramenta quanto como playbook de workflow.

Hoje o vault não tem trilha pra esse stack. Notas avulsas de ferramenta vivem em `03-Dominios/Ferramentas/` (Vite, IntelliJ shortcuts, Monorepos, Prompts), mas o conjunto Terminal é coeso e denso demais pra caber lá — vira trilha própria.

**Objetivo:** trilha completa que leve o usuário a **domínio pleno do stack**. O processo de implementação é o próprio caminho de aprendizado: cada galho envolve pesquisa real das ferramentas (docs oficiais, posts canônicos) e produção das notas atômicas que consolidam esse aprendizado.

---

## Escopo

- **Inclui:** Neovim/LazyVim, Zsh/Oh-My-Zsh/Powerlevel10k, Zellij, Lazygit, Lazydocker, gerenciamento de dotfiles, utilitários de CLI complementares (fzf, ripgrep, bat, eza, zoxide, atuin…), playbooks de workflow no terminal.
- **Exclui:** sistema operacional (Linux) — pertence a `Infraestrutura/Linux`. Editores não-terminal (IntelliJ, VS Code GUI) — ficam em `Ferramentas/`. Comandos shell genéricos do sistema (find, grep, awk) — pertencem a `Linux`.
- **Foco:** dev individual no terminal — não cobre sysadmin, hardening, infra remota.

---

## Fases de aprendizado

Cada galho da trilha é organizado em **3 fases progressivas**, inspiradas na hierarquia hermética. Notas atômicas carregam `fase:` no frontmatter; o MOC do galho agrupa as notas em 3 subseções (`## Iniciado` / `## Adepto` / `## Magus`).

| Fase | Equivale a | Profundidade | Objetivo |
|---|---|---|---|
| **Iniciado** | nível júnior | baixa, visão geral | Dar contato inicial — vocabulário básico, modelo mental, comandos suficientes pra começar a usar a ferramenta no dia-a-dia |
| **Adepto** | nível pleno | moderada | Domínio operacional pleno — configurar, customizar, usar com confiança em projetos reais |
| **Magus** | nível senior | profunda | Maestria — técnicas avançadas, otimização, casos de uso obscuros, decisões de arquitetura |

### Iteração: vertical por galho

Cada galho é fechado em si mesmo — Iniciado + Adepto + Magus implementados na mesma sessão de execução do galho. Não há "fase 1 de todos os galhos" antes de "fase 2 de todos". Vantagem: termina cada galho como unidade autocontida; pode-se publicar/usar um galho completo antes do próximo começar.

### Marcação

```yaml
---
title: "<título>"
type: concept
fase: iniciado     # iniciado | adepto | magus
tags: [terminal, <galho-slug>, <fase>]
...
---
```

O MOC do galho agrupa visualmente:

```markdown
## Iniciado
- [[01 - Modal editing]]
- [[02 - Motions e operadores]]
- ...

## Adepto
- [[05 - Lua para Neovim]]
- ...

## Magus
- [[10 - Registers, marks, macros]]
- ...
```

---

## Estrutura

```
03-Dominios/Terminal/
├── index.md              ← tronco MOC (roadmap interativo da trilha)
├── Editor/               ← galho 1: Neovim + LazyVim
│   └── index.md          ← galho MOC (agrupado por fase) + notas atômicas (flat)
├── Shell/                ← galho 2: Zsh + Oh-My-Zsh + Powerlevel10k
├── Multiplexer/          ← galho 3: Zellij
├── TUIs de Dev/          ← galho 4: Lazygit + Lazydocker
├── Dotfiles/             ← galho 5: gerenciamento de configs
├── CLI Utils/            ← galho 6: fzf, ripgrep, bat, eza, zoxide…
└── Workflow/             ← galho 7: playbooks cross-tool
```

Folder de cada galho é **flat** (sem subpastas por fase). A organização por fase é puramente lógica (frontmatter + MOC).

---

## Estratégia de execução

Este spec é **roadmap** — define o mapa completo da trilha (todos os galhos e suas notas), mas **não** é executado de uma vez. Cada galho terá:

1. Seu próprio **spec** (`docs/superpowers/specs/YYYY-MM-DD-terminal-<galho>-design.md`)
2. Seu próprio **plano de execução** (`docs/superpowers/plans/YYYY-MM-DD-terminal-<galho>-execution.md`)
3. Sua própria **sessão de implementação** (pesquisa + escrita de todas as notas das 3 fases)

**Pattern do Node:** o vault já segue isso (ver `2026-05-07-node-roadmap-design.md` + 8 specs por galho).

### O que é criado agora (com este roadmap)

- `Terminal/index.md` — tronco MOC completo, listando os 7 galhos
  - Galhos já implementados → wikilink ativo pro `index` do galho
  - Galhos pendentes → bullet de texto puro marcado como `(planejado)` (evita red links no graph)
- Nenhuma pasta de galho ainda — elas nascem quando o galho é implementado

### O que vem nas sessões futuras (uma por galho)

- Pasta `<Galho>/` criada
- `<Galho>/index.md` (MOC do galho) escrito, agrupando notas em ## Iniciado / ## Adepto / ## Magus
- Todas as notas atômicas do galho escritas (mapa definido neste roadmap, podendo ajustar antes)
- `index.md` do tronco atualizado pra ativar o wikilink do galho

### Ordem sugerida

1. **Editor** — denso e íngreme; estabelece base do estudo
2. **Shell** — já em uso, formaliza setup atual e expande
3. **Multiplexer** — destrava workflow de múltiplas sessões
4. **TUIs de Dev** — ganho rápido de produtividade (Lazygit/Lazydocker)
5. **CLI Utils** — incremental, conforme adoção
6. **Dotfiles** — depois que o setup já está maduro
7. **Workflow** — por último; depende dos anteriores

A ordem é sugestão — o usuário escolhe a cada sessão.

---

## Galhos e mapas de notas

### Galho 1 — Editor (~13 notas)

*Neovim + LazyVim. O mais denso da trilha.*

**Iniciado** (4 notas — usar Neovim/LazyVim básico no dia-a-dia)

| # | Nota |
|---|------|
| 01 | Modal editing — modos (normal, insert, visual) e filosofia |
| 02 | Motions e operadores — a gramática essencial |
| 03 | Edição básica — yank/paste, search/replace, buffers/windows/tabs |
| 04 | LazyVim — instalação, tour, navegação com Telescope e neo-tree |

**Adepto** (5 notas — configurar e dominar)

| # | Nota |
|---|------|
| 05 | Lua para Neovim — o mínimo necessário pra configurar |
| 06 | Estrutura de config — `init.lua`, `~/.config/nvim`, autocmds |
| 07 | lazy.nvim — plugins, lifecycle, lazy-loading |
| 08 | Customizando LazyVim — adicionar plugins, override de keymaps, opts |
| 09 | LSP no Neovim — Mason, nvim-lspconfig, nvim-cmp |

**Magus** (4 notas — maestria)

| # | Nota |
|---|------|
| 10 | Registers, marks, macros — o poder oculto |
| 11 | Workflow avançado — quickfix, sessions, refactoring pesado |
| 12 | Treesitter avançado — textobjects, queries customizadas |
| 13 | Snippets (LuaSnip) e debugging (DAP) |

---

### Galho 2 — Shell (~8 notas)

*Zsh + Oh-My-Zsh + Powerlevel10k.*

**Iniciado** (3 notas)

| # | Nota |
|---|------|
| 01 | Zsh vs Bash — o que muda, por que migrar |
| 02 | Zsh essencial — aliases, funções, opts (setopt) |
| 03 | Oh-My-Zsh — anatomia + plugins essenciais (git, z, fzf-tab, autosuggestions, syntax-highlighting) |

**Adepto** (3 notas)

| # | Nota |
|---|------|
| 04 | Powerlevel10k — instant prompt, config wizard, customização |
| 05 | Completion system (compsys) — modelo mental |
| 06 | ZLE — Zsh Line Editor, key bindings, widgets |

**Magus** (2 notas)

| # | Nota |
|---|------|
| 07 | Globbing avançado e parameter expansion |
| 08 | Plugins, themes e custom no OMZ — escrevendo o seu |

---

### Galho 3 — Multiplexer (~7 notas)

*Zellij.*

**Iniciado** (3 notas)

| # | Nota |
|---|------|
| 01 | Zellij vs tmux vs screen — por que Zellij |
| 02 | Modelo mental — sessions, tabs, panes |
| 03 | Modos básicos e keybindings essenciais (normal, pane, tab) |

**Adepto** (2 notas)

| # | Nota |
|---|------|
| 04 | Sessões persistentes — detach, attach, gerenciamento |
| 05 | Layouts declarativos em KDL |

**Magus** (2 notas)

| # | Nota |
|---|------|
| 06 | Modos avançados (resize, scroll, search) e plugins |
| 07 | Integração com Neovim e shell — focus events, navegação cross-pane |

---

### Galho 4 — TUIs de Dev (~7 notas)

*Lazygit + Lazydocker.*

**Iniciado** (2 notas)

| # | Nota |
|---|------|
| 01 | Lazygit — overview e operações essenciais (stage, commit, branch, push/pull) |
| 02 | Lazydocker — overview e operações comuns (containers, images, logs) |

**Adepto** (3 notas)

| # | Nota |
|---|------|
| 03 | Lazygit — operações intermediárias (rebase interativo, cherry-pick, hunks) |
| 04 | Lazygit — config e customização (`config.yml`) |
| 05 | Lazydocker — config, customização e workflow |

**Magus** (2 notas)

| # | Nota |
|---|------|
| 06 | Lazygit — operações avançadas (bisect, custom commands, integração com hooks) |
| 07 | Lazydocker — debugging avançado e integração com docker-compose |

---

### Galho 5 — Dotfiles (~6 notas)

**Iniciado** (2 notas)

| # | Nota |
|---|------|
| 01 | Por que versionar dotfiles — princípios e armadilhas |
| 02 | GNU stow — symlinks declarativos (abordagem mais simples) |

**Adepto** (2 notas)

| # | Nota |
|---|------|
| 03 | chezmoi — manager completo (templates, sync entre máquinas) |
| 04 | Bare git repo — abordagem minimalista |

**Magus** (2 notas)

| # | Nota |
|---|------|
| 05 | Secrets em dotfiles — git-crypt, age, sops |
| 06 | Bootstrap de máquina nova — script + dotfiles automatizado |

---

### Galho 6 — CLI Utils (~9 notas)

**Iniciado** (4 notas — o núcleo que muda o dia-a-dia)

| # | Nota |
|---|------|
| 01 | fzf — fuzzy finder universal, integração com Zsh e Neovim |
| 02 | ripgrep (rg) — grep moderno |
| 03 | bat — cat com syntax highlight |
| 04 | eza — ls moderno |

**Adepto** (3 notas)

| # | Nota |
|---|------|
| 05 | zoxide — cd inteligente |
| 06 | atuin — history sync e search |
| 07 | jq + yq — JSON/YAML processing |

**Magus** (2 notas)

| # | Nota |
|---|------|
| 08 | tldr + cheat — manpages práticas em fluxo |
| 09 | Outras úteis — fd, delta, dust, btop, htop |

---

### Galho 7 — Workflow (~7 notas)

*Playbooks cross-tool. Implementado por último — depende dos galhos anteriores.*

**Iniciado** (2 notas)

| # | Nota |
|---|------|
| 01 | Code review básico no terminal (gh + Neovim) |
| 02 | Onboarding em projeto novo — fluxo de exploração (Telescope + ripgrep) |

**Adepto** (3 notas)

| # | Nota |
|---|------|
| 03 | Debug de container Docker (Lazydocker + logs + exec) |
| 04 | Worktrees + sessões Zellij paralelas |
| 05 | Edição multi-arquivo (Telescope + quickfix + macros) |

**Magus** (2 notas)

| # | Nota |
|---|------|
| 06 | Fluxo de commit estruturado (Lazygit + hooks + commitlint) |
| 07 | Refactoring em projeto inteiro (rg + Neovim quickfix + LSP) |

---

## Padrão das notas

### Tronco (`Terminal/index.md`)

```markdown
---
title: "Terminal"
type: moc
publish: true
created: 2026-05-18
updated: 2026-05-18
status: growing
progresso: andamento
tags:
  - terminal
  - moc
  - dev-environment
aliases:
  - Terminal
---
# Terminal

> [!abstract] TL;DR
> Trilha do ambiente de trabalho no terminal: editor (Neovim/LazyVim), shell (Zsh/p10k), multiplexer (Zellij), TUIs (Lazygit/Lazydocker), dotfiles, CLI utils e playbooks de workflow. 7 galhos, ~57 notas distribuídas em 3 fases (Iniciado → Adepto → Magus) por galho.

## Conteúdo

### Galhos
- Editor — galho 1 (planejado): Neovim + LazyVim (modal editing, plugins, LSP)
- Shell — galho 2 (planejado): Zsh + Oh-My-Zsh + Powerlevel10k
- Multiplexer — galho 3 (planejado): Zellij
- TUIs de Dev — galho 4 (planejado): Lazygit, Lazydocker
- Dotfiles — galho 5 (planejado): gerenciamento de configs e sync
- CLI Utils — galho 6 (planejado): fzf, ripgrep, bat, eza, zoxide…
- Workflow — galho 7 (planejado): playbooks cross-tool

## Veja também
- [[03-Dominios/Infraestrutura/Linux/index|Linux]]
- [[03-Dominios/Ferramentas|Ferramentas]]
```

Quando um galho é implementado, seu bullet vira wikilink ativo:
```markdown
- [[03-Dominios/Terminal/Editor/index]] — galho 1: Neovim + LazyVim (modal editing, plugins, LSP)
```

### Galho MOC (`<Galho>/index.md`)

```markdown
---
title: "<Galho>"
type: moc
publish: true
created: YYYY-MM-DD
updated: YYYY-MM-DD
status: growing
progresso: andamento
tags: [terminal, <galho-slug>, moc]
---
# <Galho>

> [!abstract] TL;DR
> ...

## Iniciado
- [[01 - Nota X]]
- [[02 - Nota Y]]

## Adepto
- [[05 - Nota Z]]
- ...

## Magus
- [[10 - Nota W]]
- ...

## Veja também
- [[03-Dominios/Terminal/index|Trilha Terminal]]
```

### Nota atômica

```markdown
---
title: "<título>"
type: concept
publish: true
fase: iniciado    # iniciado | adepto | magus
tags: [terminal, <galho-slug>, <fase>]
created: YYYY-MM-DD
updated: YYYY-MM-DD
status: seedling
---
# <Título>

> [!abstract] TL;DR
> ...

## O que é / Como funciona

## Na prática

## Armadilhas

## Veja também

## Referências
```

### Processo de pesquisa por nota

Pra cada nota:
1. **Fontes primárias:** docs oficiais da ferramenta (sempre)
2. **Fontes secundárias:** posts canônicos, vídeos de referência, repos exemplares
3. **Validação:** quando possível, executar comandos/configs localmente
4. **Síntese:** escrever a nota no padrão atômico, com TL;DR, exemplos práticos e armadilhas

A skill `glosa` pode ser usada pra fichar artigos relevantes antes de virarem nota — útil quando uma fonte densa precisa ser destilada.

---

## Relação com domínios existentes

| Existente | Relação |
|---|---|
| `03-Dominios/Infraestrutura/Linux/Comandos para entender agentes.md` | Permanece; Terminal não duplica comandos shell genéricos. Wikilink mútuo no "Veja também". |
| `03-Dominios/Ferramentas/` | Permanece pra tools fora do stack terminal-first (IntelliJ, Vite). Nada migra. |
| `03-Dominios/IA/Claude Code/` | Cruza com Workflow (Claude Code também é terminal-first). Wikilinks recíprocos quando relevante. |

---

## Volume estimado

| Galho | Iniciado | Adepto | Magus | Total |
|---|---|---|---|---|
| Editor | 4 | 5 | 4 | 13 |
| Shell | 3 | 3 | 2 | 8 |
| Multiplexer | 3 | 2 | 2 | 7 |
| TUIs de Dev | 2 | 3 | 2 | 7 |
| Dotfiles | 2 | 2 | 2 | 6 |
| CLI Utils | 4 | 3 | 2 | 9 |
| Workflow | 2 | 3 | 2 | 7 |
| **TOTAL** | **20** | **21** | **16** | **57** |

+ 8 MOCs (tronco + 7 galhos) = **~65 arquivos no fim da trilha**.

### Criado nesta sessão (escopo deste plano)

| Item | Quantidade |
|---|---|
| `Terminal/index.md` (tronco MOC) | 1 |

A sessão atual cria **apenas** o tronco. Os galhos vêm em sessões próprias com specs e execuções dedicadas.

---

## Próximos passos após este roadmap

1. **Esta sessão:** writing-plans → cria plano de execução pra escrever o `Terminal/index.md` (tarefa pequena).
2. **Sessão seguinte:** spec do Galho 1 (Editor) — design detalhado das 13 notas com fontes mapeadas por fase.
3. **Sessão de implementação do Galho 1:** pesquisa + escrita das 13 notas (Iniciado → Adepto → Magus) + MOC do galho + ativação do wikilink no tronco.
4. **Repetir** specs+execução pros galhos 2-7, na ordem que você escolher a cada sessão.
