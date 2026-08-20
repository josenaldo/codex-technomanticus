---
title: "Lazygit — overview e operações essenciais"
created: 2026-05-21
updated: 2026-05-21
type: concept
progress: backlog
status: seedling
publish: true
fase: iniciado
tags:
  - terminal
  - tuis
  - lazygit
  - iniciado
  - git
aliases:
  - Lazygit overview
---

# Lazygit — overview e operações essenciais

> [!abstract] TL;DR
> Lazygit é uma TUI git em Go por Jesse Duffield: painéis keyboard-first pra status/files/branches/commits/stash. `space` stage, `c` commit, `p`/`P` pull/push, `n` new branch, `s` stash, `?` help contextual. Vence quando você faz muitos commits parciais (hunks), troca branches frequente, ou quer visualizar history sem `git log --graph` na cabeça.

## O que é / Como funciona

### Quem é Lazygit

**Lazygit** é uma TUI para git criada por Jesse Duffield (o mesmo autor do Lazydocker). Escrita em Go, distribui como single binary sem dependências extras.

- **Linguagem:** Go — single binary, sem runtime externo
- **Estilo:** painéis com keybindings contextuais (não modal como Vim; cada painel tem seus próprios atalhos, visíveis via `?`)
- **Foco:** workflow git dia-a-dia — staging, commits, branches, stash, rebase interativo, cherry-pick
- **Não substitui:** `git` CLI pra scripts, automações ou CI/CD; nem IDE GUI pra blame inline integrado a PR review

### Layout dos painéis

Lazygit usa 3 colunas no layout padrão. A coluna esquerda tem 5 painéis empilhados (acessados pelas teclas `1`–`5`); dentro de cada painel, `]`/`[` trocam as abas disponíveis (e.g. Branches tem abas Local, Remotes, Tags, Reflog); a coluna direita é a main view (diff, conteúdo do commit, hunk view); a borda inferior exibe o command log.

```text
┌──────────────────┬──────────────────────────────────────┐
│ 1 Status         │                                      │
├──────────────────┤                                      │
│ 2 Files          │  Main View / Diff                    │
├──────────────────┤  (conteúdo contextual do painel      │
│ 3 Local Branches │   ativo: diff, commits, hunks…)      │
├──────────────────┤                                      │
│ 4 Commits        │                                      │
├──────────────────┤                                      │
│ 5 Stash          │                                      │
├──────────────────┴──────────────────────────────────────┤
│ Command log: $ git status                               │
└─────────────────────────────────────────────────────────┘
```

O **command log** (borda inferior) exibe cada comando `git` que Lazygit executa — útil pra aprender o equivalente shell de cada ação visual.

### Navegação

| Tecla | Ação |
|---|---|
| `1` / `2` / `3` / `4` / `5` | Pula diretamente para o painel (Status / Files / Branches / Commits / Stash) |
| `0` | Foca a main view (diff, output) |
| `]` / `[` | Próxima / anterior **aba** dentro do painel ativo (e.g. Branches → Local → Remotes → Tags → Reflog) |
| `j` / `k` | Desce / sobe dentro do painel ativo |
| `<enter>` | Entra na visualização detalhada (diff, commits do branch, arquivos do commit…) |
| `<esc>` | Cancela ação ou volta da visualização detalhada |
| `?` | Help contextual — exibe keybindings do painel ativo |
| `q` | Sai do Lazygit |
| `/` | Filtra a lista do painel por texto |
| `R` | Recarrega estado do git |

### Operações por painel — cheatsheet

| Painel | Tecla | Ação |
|---|---|---|
| Files | `space` | Stage / unstage arquivo |
| Files | `enter` | Entra diff view (stage por hunk com `space`) |
| Files | `a` | Stage / unstage todos os arquivos |
| Files | `c` | Commit das mudanças staged |
| Files | `A` | Amend no último commit |
| Files | `d` | Opções de discard (confirma antes de apagar) |
| Files | `D` | Abre menu de opções de reset (soft / mixed / hard / nuke working tree) |
| Files | `s` | Stash all changes |
| Files | `S` | Ver opções de stash |
| Files | `e` | Editar arquivo no editor externo |
| Branches | `space` | Checkout do branch selecionado |
| Branches | `n` | Criar novo branch |
| Branches | `d` | Opções de delete do branch |
| Branches | `R` | Renomear branch |
| Branches | `M` | Ver opções de merge no branch atual |
| Branches | `r` | Rebase no branch selecionado |
| Branches | `-` | Checkout do branch anterior |
| Commits | `s` | Squash no commit abaixo |
| Commits | `f` | Fixup no commit abaixo |
| Commits | `d` | Drop commit |
| Commits | `r` | Reword da mensagem do commit |
| Commits | `e` | Editar commit (inicia rebase interativo) |
| Commits | `g` | View reset options (soft/mixed/hard) |
| Commits | `C` | Cherry-pick (copiar commit) |
| Commits | `V` | Colar cherry-pick |
| Stash | `space` | Apply stash entry |
| Stash | `g` | Pop stash entry |
| Stash | `d` | Drop stash entry |
| Stash | `n` | Criar branch a partir do stash |
| Global | `p` | Pull |
| Global | `P` | Push |
| Global | `z` | Undo |
| Global | `Z` | Redo |
| Global | `?` | Help contextual |
| Global | `:` | Executar comando shell arbitrário |

### Quando Lazygit ganha

- **Commits parciais (hunks):** `enter` em Files abre hunk view; `space` stage/unstage hunk individual ou linhas selecionadas com `v` — muito mais rápido que `git add -p`
- **Branch switching frequente:** painel Branches com preview do diff, checkout em `space`
- **Stash heavy workflow:** ver stash list e aplicar/dropar sem memorizar índices (`stash@{0}`)
- **Visualizar history:** commit graph no painel Commits, sem precisar decorar `git log --graph --all --oneline`
- **Resolver merge conflicts inline:** navega por hunks com `<left>`/`<right>`, escolhe lado com `space`
- **Rebase interativo:** squash, fixup, drop, reorder — tudo com teclas simples no painel Commits

### Quando `git` CLI ainda ganha

- **Scripts e automações:** Lazygit é interativo; CLI é compositável com pipes e subshells
- **CI/CD:** sem TTY, sem TUI
- **Contextos SSH sem PTY:** `ssh user@host command` não aloca TTY; Lazygit exige terminal interativo
- **Comandos raros:** `git notes`, `git bundle`, `git archive` e outros que Lazygit não expõe diretamente

### Quando IDE GUI ainda ganha

- **Blame inline em código:** ver quem mudou cada linha sem sair do editor aberto no arquivo
- **Review de PR na mesma janela:** comentar linhas, ver status de checks, aprovar — integrado na IDE
- **Usuários não-nativos de terminal:** curva de entrada menor com mouse + menu visual

---

## Na prática

### Instalação rápida

```bash
# Snap (Ubuntu/Linux)
sudo snap install lazygit

# Homebrew (macOS e Linux)
brew install lazygit

# Go install (requer Go ≥1.19)
go install github.com/jesseduffield/lazygit@latest

# Arch Linux
sudo pacman -S lazygit
```

(Referência: Lazygit 0.61+; keybindings podem variar em versões mais antigas.)

### Primeira execução

```bash
cd ~/repos/myproj
lazygit
```

Lazygit abre no repositório da pasta atual. Se a pasta não for um repo git, oferece `git init`. Para sair: `q`.

### Workflow primeira vez (5 minutos)

1. Teclas `1`–`5` saltam entre os 5 painéis; `]`/`[` trocam abas dentro do painel ativo — observar que o conteúdo da main view muda
2. `?` no painel Files mostra os atalhos disponíveis naquele contexto
3. Edite um arquivo no seu editor normalmente (ou `e` dentro do Lazygit pra abrir no editor configurado)
4. `j`/`k` no painel Files navega entre os arquivos modificados
5. `enter` em um arquivo abre hunk view; `space` stage hunk; `<esc>` volta
6. `space` no painel Files faz stage do arquivo inteiro
7. `c` abre campo pra mensagem de commit; `enter` confirma
8. `P` push — Lazygit mostra o comando executado no command log

---

## Armadilhas

**1. `d` em Files apaga mudanças sem aviso óbvio**

- **Causa:** `d` no painel Files abre menu de opções de discard — e a confirmação é rápida o suficiente pra pressionar `enter` sem ler.
- **Sintoma:** mudanças desaparecem do working tree e não estão no staging.
- **Como detectar:** mudanças uncommitted não ficam no `git reflog` — se você discardou sem stash, não há recuperação fácil.
- **Solução:** hábito de usar `s` (stash) antes de operações destrutivas; ler o menu de confirmação antes de pressionar `enter`.

**2. Não saber em qual painel está**

- **Causa:** keybindings mudam completamente por painel. `d` no Files é discard; `d` no Commits é drop commit; `d` no Stash é drop stash entry.
- **Sintoma:** ação inesperada acontece — commit dropado, branch deletado, etc.
- **Como detectar:** painel ativo tem borda ou destaque visual diferente; a bottom bar exibe hints do painel ativo.
- **Solução:** olhar qual painel está destacado antes de pressionar teclas destrutivas; `?` confirma o contexto atual.

**3. Lazygit exige TTY — não roda em CI ou cron**

- **Causa:** é uma TUI interativa que precisa de terminal alocado.
- **Sintoma:** falha silenciosa ou saída sem sentido em SSH sem `-t`, containers sem TTY, ou scripts cron.
- **Como detectar:** `ssh user@host lazygit` sem `-t` falha; em script, `[ -t 0 ]` retorna falso.
- **Solução:** usar Lazygit apenas interativamente; pra automações usar `git` CLI diretamente.

**4. Pull resulta em merge commits indesejados**

- **Causa:** `p` respeita a config `pull.rebase` do git global/local — se não estiver definida ou estiver `false`, pull faz merge.
- **Sintoma:** após `p`, painel Commits mostra um "Merge branch 'main' into..." que você não queria.
- **Como detectar:** `git config pull.rebase` — vazio ou `false` significa merge.
- **Solução:** `git config --global pull.rebase true` pra sempre usar rebase no pull, ou `git config --global pull.rebase false` pra aceitar merges conscientemente; Lazygit vai respeitar.

**5. `e` / editor não abre nada**

- **Causa:** `editPreset` ou `editor` não configurado no `~/.config/lazygit/config.yml`, e Lazygit não detectou o `$EDITOR` corretamente.
- **Sintoma:** pressionar `e` em Files não faz nada visível, ou abre editor errado.
- **Como detectar:** tentar com `e` e observar se o command log exibe algum erro; checar `echo $EDITOR` no shell.
- **Solução:** definir `os.editPreset: "nvim"` (ou `"vscode"`, `"zed"`, etc.) no config — detalhes em [[04 - Lazygit — config e customização]].

---

## Em inglês

- **TUI** — *TUI (Terminal User Interface)*. "interface keyboard-first dentro do terminal, com painéis, cores e scroll."
- **painel** — *panel*. "área independente da UI do Lazygit; cada painel tem keybindings próprios visíveis via `?`."
- **staging** — *staging*. "ato de marcar mudanças pra incluir no próximo commit; `space` no Files."
- **hunk** — *hunk*. "bloco contíguo de linhas alteradas dentro de um diff; unidade mínima de staging parcial."
- **commit** — *commit*. "snapshot imutável do estado do repositório gravado no histórico do git."
- **push** — *push*. "enviar commits locais pro repositório remoto; `P` no Lazygit."
- **pull** — *pull*. "buscar e integrar commits do repositório remoto; `p` no Lazygit."
- **stash** — *stash*. "área temporária pra guardar mudanças uncommitted sem criar commit."
- **amend** — *amend*. "modificar o último commit (mensagem ou conteúdo) sem criar um novo; `A` no painel Files."
- **discard** — *discard*. "descartar mudanças do working tree ou staging, revertendo ao estado do último commit."

---

## Veja também

- [[02 - Lazydocker — overview e operações comuns]] — TUI irmã pra Docker
- [[03 - Lazygit — operações intermediárias]] — rebase interativo, cherry-pick, squash
- [[04 - Lazygit — config e customização]] — `~/.config/lazygit/config.yml`, editPreset, temas
- [[06 - Lazygit — operações avançadas]] — bisect, customCommands, worktrees
- [[03-Dominios/Tecnologia/Terminal/TUIs/index|MOC do galho]]
- [[03-Dominios/Tecnologia/Terminal/index|Trilha Terminal]]
- [[Dicionário do Terminal#Lazygit|lazygit]], [[Dicionário do Terminal#TUI|TUI]], [[Dicionário do Terminal#Command log|command log]]

---

## Referências

- Lazygit — repositório oficial: https://github.com/jesseduffield/lazygit
- Keybindings oficiais: https://github.com/jesseduffield/lazygit/blob/master/docs/keybindings/Keybindings_en.md
