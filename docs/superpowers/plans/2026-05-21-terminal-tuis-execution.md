# Galho 4 — TUIs de Dev (Lazygit + Lazydocker) — Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Entregar o galho 4 da trilha Terminal — 7 notas atômicas (2 Iniciado + 3 Adepto + 2 Magus) sobre Lazygit (5 notas) e Lazydocker (2 notas) em `03-Dominios/Terminal/TUIs/`, MOC do galho, expansão do Dicionário com bloco `## TUIs de Dev / Lazygit / Lazydocker`, e ativação do wikilink no tronco.

**Architecture:** Mesmo padrão consolidado nos galhos 2 e 3. Estrutura H2 fixa, fluxo SDD (implementer → reviewer combinado → fix se Critical/Important). Pesquisa-âncora em docs oficiais antes de cada nota. Versões reais capturadas no Task 0.

**Tech Stack:** Obsidian + Quartz, Markdown + frontmatter YAML, wikilinks. Ferramentas-alvo: Lazygit (TUI git em Go), Lazydocker (TUI Docker em Go) — ambos por Jesse Duffield.

---

## Spec de referência

`docs/superpowers/specs/2026-05-21-terminal-tuis-design.md`

## Restrições absolutas (em TODOS os subagent prompts)

1. **Sem fabricação** de experiência pessoal. Exemplos neutros (`alice`, `bob`, `myproj`) ou hipotéticos explícitos. NUNCA `josenaldo` nem `/home/josenaldo/...`.
2. **Sem invenção** de keybindings/features. Verificar via doc oficial.
3. **Sem `Co-Authored-By: Claude`**. **Sem `--no-verify`**.
4. **Paths generalizados** pra `~/...`.
5. **Wikilinks sem backticks** em `## Veja também`.
6. **Tronco wikilink obrigatório**: `[[03-Dominios/Terminal/index|Trilha Terminal]]`.
7. **MOC wikilink** em "Veja também": `[[03-Dominios/Terminal/TUIs/index|MOC do galho]]`.
8. **≥5 armadilhas** por nota, cada uma com os 4 labels (Causa / Sintoma / Como detectar / Solução).
9. **"Em inglês" em bullets bilíngues** `- **PT** — *EN*. "frase técnica curta em PT."` (8-10 termos). NUNCA tabela.
10. **Code fences corretos:** `yaml` pra config, `bash` pra shell, `text`/`diff` pra exemplos de diff.
11. **Keybindings com contexto** — Lazygit muda atalhos por painel; sempre indicar painel.
12. **Custom commands sintaxe válida** — verificar contra `docs/Custom_Command_Keybindings.md`.

---

## Task 0: Pré-flight

**Files:**
- (nenhum — só captura)

- [ ] **Step 1: Capturar versão Lazygit**

```bash
lazygit --version 2>&1 || echo "(lazygit não instalado)"
```

Anotar resultado.

- [ ] **Step 2: Capturar versão Lazydocker**

```bash
lazydocker --version 2>&1 || echo "(lazydocker não instalado)"
```

Anotar resultado.

- [ ] **Step 3: Capturar paths de config**

```bash
ls -la ~/.config/lazygit/ 2>&1 | head -10
ls -la ~/.config/lazydocker/ 2>&1 | head -10
```

Anotar o que existe.

- [ ] **Step 4: Anotar versões**

Não commitar. Anotar pra uso no Task 10 (substituir placeholders do MOC).

---

## Task 1: MOC do galho TUIs — esqueleto

**Files:**
- Create: `03-Dominios/Terminal/TUIs/index.md`

- [ ] **Step 1: Criar pasta**

```bash
mkdir -p "03-Dominios/Terminal/TUIs"
```

- [ ] **Step 2: Escrever MOC**

Use `Write` em `03-Dominios/Terminal/TUIs/index.md`:

```markdown
---
title: "TUIs de Dev"
type: moc
publish: true
created: 2026-05-21
updated: 2026-05-21
status: growing
progresso: andamento
tags:
  - terminal
  - tuis
  - lazygit
  - lazydocker
  - moc
aliases:
  - TUIs de Dev
  - Lazygit
  - Lazydocker
---
# TUIs de Dev

> [!abstract] TL;DR
> Galho 4 da trilha Terminal. Domínio de Lazygit + Lazydocker — TUIs keyboard-first em Go (Jesse Duffield) pra git e Docker. 7 notas (5 Lazygit + 2 Lazydocker) em 3 fases (2 + 3 + 2).

Esse galho cobre as duas TUIs juntas porque compartilham filosofia (keyboard-first, painéis discoverable, config YAML). Lazygit recebe mais profundidade (5 notas) porque tem customização mais profunda (`customCommands`, theming, keybindings rebind). Lazydocker é o complemento dev local pra workflows com Docker.

## Conteúdo

### Iniciado

- [[01 - Lazygit — overview e operações essenciais]]
- [[02 - Lazydocker — overview e operações comuns]]

### Adepto

- [[03 - Lazygit — operações intermediárias]]
- [[04 - Lazygit — config e customização]]
- [[05 - Lazydocker — config, customização e workflow]]

### Magus

- [[06 - Lazygit — operações avançadas]]
- [[07 - Lazydocker — debugging avançado e docker-compose]]

## Rotas alternativas

- **Apenas Lazygit**: `01` → `03` → `04` → `06`
- **Apenas Lazydocker**: `02` → `05` → `07`
- **Onboarding completo**: `01` → `02` → `03` → `05` → `06`

## Versões assumidas

- **Lazygit:** `<VERSAO_LAZYGIT>` (capturada no pré-flight)
- **Lazydocker:** `<VERSAO_LAZYDOCKER>` (capturada no pré-flight)

## Veja também

- [[Dicionário do Terminal]]
- [[03-Dominios/Terminal/index|Trilha Terminal]]
```

- [ ] **Step 3: Commit**

```bash
git add "03-Dominios/Terminal/TUIs/index.md"
git commit -m "feat(terminal-tuis): MOC do galho 4 — esqueleto"
```

---

## Task 2: Dicionário — bloco "TUIs de Dev / Lazygit / Lazydocker" esqueleto

**Files:**
- Modify: `03-Dominios/Terminal/Dicionário do Terminal.md`

- [ ] **Step 1: Localizar fim do bloco anterior**

Use `Read` no final do Dicionário pra encontrar o último verbete do bloco `## Multiplexer / Zellij` (último alfabético: `Tmux compat mode`).

- [ ] **Step 2: Inserir header**

Após o último verbete do bloco Multiplexer/Zellij, inserir:

```markdown
## TUIs de Dev / Lazygit / Lazydocker

```

Use `Edit` cuidadosamente — `old_string` = última linha de `### Tmux compat mode` + linha vazia, `new_string` = mesmo + `## TUIs de Dev / Lazygit / Lazydocker\n\n`.

- [ ] **Step 3: Confirmar `updated:` do dicionário**

Deve estar `updated: 2026-05-21`. Se não, Edit.

- [ ] **Step 4: Commit**

```bash
git add "03-Dominios/Terminal/Dicionário do Terminal.md"
git commit -m "feat(terminal-tuis): adiciona bloco 'TUIs de Dev / Lazygit / Lazydocker' ao Dicionário"
```

---

## Task 3: Nota 01 — Lazygit: overview e operações essenciais

**Files:**
- Create: `03-Dominios/Terminal/TUIs/01 - Lazygit — overview e operações essenciais.md`
- Modify: `03-Dominios/Terminal/Dicionário do Terminal.md` (verbetes: Lazygit, TUI, Command log)

- [ ] **Step 1: Pesquisa-âncora**

```
WebFetch: https://github.com/jesseduffield/lazygit
WebFetch: https://github.com/jesseduffield/lazygit/blob/master/docs/keybindings/Keybindings_en.md
```

Confirmar: layout dos painéis, keybindings core (space/c/a/p/P/b/s/d/?), filosofia do projeto.

- [ ] **Step 2: Frontmatter**

```yaml
---
title: "Lazygit — overview e operações essenciais"
created: 2026-05-21
updated: 2026-05-21
type: concept
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
```

- [ ] **Step 3: Escrever nota completa**

Estrutura H2 obrigatória: callout TL;DR + O que é/Como funciona + Na prática + Armadilhas + Em inglês + Veja também + Referências.

**TL;DR (callout):**
"Lazygit é uma TUI git em Go por Jesse Duffield: painéis keyboard-first pra status/files/branches/commits/stash. `space` stage, `c` commit, `p`/`P` pull/push, `b` branch ops, `s` stash, `?` help contextual. Vence quando você faz muitos commits parciais (hunks), troca branches frequente, ou quer visualizar history sem `git log --graph` no head."

**O que é / Como funciona** (H3s):

### Quem é Lazygit
- Autor: Jesse Duffield (mesmo de Lazydocker)
- Linguagem: Go, single binary
- Estilo: TUI modal com painéis (não modos como Vim, mas seleção de painel + keybindings contextuais)
- Foco: workflow git dia-a-dia, não substitui git CLI pra automações

### Layout dos painéis
Diagrama ASCII com 7 painéis principais:
```
┌─Status──────┬─Files──────────┐
│ branch atual│ M  src/app.js  │
│ ahead/behind│ M  README.md   │
├─Branches────┤ ?? notes.md   │
│ * main      ├────────────────┤
│   feat-1    │  Diff / preview │
├─Commits─────┤                │
│ abc1 feat..│                │
│ def2 fix...│                │
├─Stash───────┴────────────────┤
│ stash@{0} WIP — auth refactor│
├─Command log──────────────────┤
│ $ git status                 │
│ $ git diff src/app.js        │
└──────────────────────────────┘
```

(Adapte o ASCII pro layout real visualizado durante WebFetch — Lazygit moderno usa 3 colunas.)

### Navegação
- `tab` / `shift+tab` ou `]` / `[` — próximo / anterior painel
- `j` / `k` — desce / sobe dentro do painel
- `h` / `l` — em painéis com sub-tabs (e.g. Branches → Tags → Remotes → Reflog)
- `?` — help contextual (atalhos do painel ativo)
- `q` — quit
- `esc` — cancel ação atual

### Operações por painel (cheatsheet)
Tabela 3 colunas (Painel | Tecla | Ação), 15+ linhas. Conferir contra Keybindings_en.md.

| Painel | Tecla | Ação |
|---|---|---|
| Files | `space` | Stage / unstage arquivo |
| Files | `enter` | Entra diff view (stage por hunk) |
| Files | `a` | Stage / unstage tudo |
| Files | `c` | Commit changes |
| Files | `A` | Amend last commit |
| Files | `d` | Discard changes (com confirm) |
| Files | `D` | Reset/discard all (com confirm) |
| Branches | `space` | Checkout |
| Branches | `n` | New branch |
| Branches | `d` | Delete branch |
| Branches | `r` | Rename branch |
| Branches | `M` | Merge into current |
| Commits | `s` | Squash down |
| Commits | `f` | Fixup down |
| Commits | `g` | Reset to |
| Commits | `c` | Copy commit (cherry-pick) |
| Stash | `space` | Apply stash |
| Stash | `g` | Pop stash |
| Stash | `d` | Drop stash |
| Global | `p` | Pull |
| Global | `P` | Push |
| Global | `?` | Help |

### Quando Lazygit ganha
- Muitos commits parciais (staging por hunks com `enter` + `space`)
- Branch switching frequente
- Stash heavy workflow
- Visualizar history sem `git log --graph`
- Resolver merge conflicts inline

### Quando `git` CLI ainda ganha
- Scripts e automações
- CI/CD
- Contextos sem TTY (SSH com pty=no)
- Comandos raros que Lazygit não cobre

### Quando IDE GUI ainda ganha
- Blame inline em código
- Integração com review de PR na mesma janela
- Pra quem não opera no terminal nativamente

**Na prática** (H3s):

### Instalação rápida
```bash
# Snap
sudo snap install lazygit

# Homebrew (mac/linux)
brew install lazygit

# Go install
go install github.com/jesseduffield/lazygit@latest

# Arch
sudo pacman -S lazygit
```

### Primeira execução
```bash
cd ~/repos/myproj
lazygit
```

Lazygit abre na pasta atual. Se não for repo git, sugere `git init`.

### Workflow primeira vez (5 minutos)
1. `tab` percorre painéis pra ver layout
2. `?` no painel Files mostra atalhos disponíveis
3. Edita arquivo num editor fora do Lazygit (ou `o` pra abrir no editor)
4. `j`/`k` no painel Files navega arquivos modificados
5. `space` stage; `c` commit; digite mensagem; `enter` confirma
6. `P` push

**Armadilhas (≥5, 4 labels)**:

1. **`d` em Files apaga changes sem aviso óbvio**
   - **Causa:** `d` é "Discard" — confirma com prompt mas é fácil de aceitar sem ler.
   - **Sintoma:** mudanças desaparecem.
   - **Como detectar:** `git reflog` (mas changes uncommitted não estão no reflog).
   - **Solução:** confirmar SEMPRE qual ação `d` está oferecendo no popup; commit-em-progresso pode ser preservado via stash (`s`) primeiro.

2. **Não saber em qual painel está**
   - **Causa:** keybindings mudam por painel (`d` em Files = discard; `d` em Branches = delete branch).
   - **Sintoma:** ação inesperada.
   - **Como detectar:** painel ativo tem borda destacada.
   - **Solução:** olhar borda; ler bottom bar com hints.

3. **Lazygit não vê config de `~/.gitconfig` em remoto sem TTY**
   - **Causa:** Lazygit requer TTY pra funcionar.
   - **Sintoma:** `lazygit` falha ou abre sem cores quando rodado em CI/CD ou cron.
   - **Como detectar:** rodar via SSH sem `-t`.
   - **Solução:** Lazygit é ferramenta interativa; pra automação use `git` puro.

4. **Pull com merge em vez de rebase (ou vice-versa)**
   - **Causa:** Lazygit respeita `pull.rebase` do git config; default git é merge.
   - **Sintoma:** merge commits indesejados após `p`.
   - **Como detectar:** `git config pull.rebase` mostra valor atual.
   - **Solução:** `git config --global pull.rebase true` (ou false) conforme preferência.

5. **Lazygit + editor externo abrindo em modo sem pty**
   - **Causa:** `os.edit` config sem editor preset ou com comando que requer TTY que não está disponível.
   - **Sintoma:** editor abre vazio ou trava ao salvar.
   - **Como detectar:** testar com editor diferente (`vim` direto).
   - **Solução:** definir `os.editPreset: "nvim"` (ou outro válido) no config (nota 04).

**Em inglês (8-10 bullets bilíngues):**
Formato: `- **PT** — *EN*. "frase técnica curta em PT."`
Termos: TUI, painel (panel), staging, hunk, commit, push, pull, stash, amend, discard.

**Veja também:**
- `[[02 - Lazydocker — overview e operações comuns]]` — TUI irmã pra Docker
- `[[03 - Lazygit — operações intermediárias]]` — rebase, cherry-pick
- `[[04 - Lazygit — config e customização]]` — `~/.config/lazygit/config.yml`
- `[[06 - Lazygit — operações avançadas]]` — bisect, customCommands
- `[[03-Dominios/Terminal/TUIs/index|MOC do galho]]`
- `[[03-Dominios/Terminal/index|Trilha Terminal]]`
- `[[Dicionário do Terminal#Lazygit|lazygit]]`, `[[Dicionário do Terminal#TUI|TUI]]`, `[[Dicionário do Terminal#Command log|command log]]`

**Referências:**
- Lazygit: https://github.com/jesseduffield/lazygit
- Keybindings: https://github.com/jesseduffield/lazygit/blob/master/docs/keybindings/Keybindings_en.md

- [ ] **Step 4: Adicionar 3 verbetes ao Dicionário**

No bloco `## TUIs de Dev / Lazygit / Lazydocker`:

```markdown
### Command log
Painel inferior do Lazygit que exibe cada comando git executado pela TUI. Útil pra aprender que comando shell equivale a uma ação visual e debuggar quando algo não funciona.

Veja também: [[01 - Lazygit — overview e operações essenciais]].

### Lazygit
TUI git em Go por Jesse Duffield. Painéis keyboard-first pra status, files, branches, commits, stash. Operações por painel com atalhos contextuais; `?` mostra help. Config YAML em `~/.config/lazygit/config.yml`.

Veja também: [[01 - Lazygit — overview e operações essenciais]], [[04 - Lazygit — config e customização]].

### TUI
Terminal User Interface — UI keyboard-first dentro do terminal, com painéis, scroll, cores, mouse opcional. Diferente de CLI (entrada e saída por linha) e GUI (gráfica). Exemplos: Lazygit, Lazydocker, htop, neomutt, ranger.

Veja também: [[01 - Lazygit — overview e operações essenciais]].
```

- [ ] **Step 5: Validar**

```bash
test -f "03-Dominios/Terminal/TUIs/01 - Lazygit — overview e operações essenciais.md"
grep -c '\[\[' "03-Dominios/Terminal/TUIs/01 - Lazygit — overview e operações essenciais.md"
grep -E "^### (Command log|Lazygit|TUI)$" "03-Dominios/Terminal/Dicionário do Terminal.md"
```

Esperado: arquivo existe, ≥7 wikilinks, 3 verbetes visíveis.

- [ ] **Step 6: Commit**

```bash
git add "03-Dominios/Terminal/TUIs/01 - Lazygit — overview e operações essenciais.md" "03-Dominios/Terminal/Dicionário do Terminal.md"
git commit -m "feat(terminal-tuis): add nota 01 — Lazygit overview"
```

---

## Task 4: Nota 02 — Lazydocker: overview e operações comuns

**Files:**
- Create: `03-Dominios/Terminal/TUIs/02 - Lazydocker — overview e operações comuns.md`
- Modify: `03-Dominios/Terminal/Dicionário do Terminal.md` (verbetes: Lazydocker, Docker-compose, Exec (Lazydocker))

- [ ] **Step 1: Pesquisa-âncora**

```
WebFetch: https://github.com/jesseduffield/lazydocker
WebFetch: https://github.com/jesseduffield/lazydocker/blob/master/docs/keybindings/Keybindings_en.md
```

Confirmar: layout, keybindings (space/d/r/e/l/R), painéis (Project/Containers/Images/Volumes/Networks/Logs/Stats).

- [ ] **Step 2: Frontmatter**

```yaml
---
title: "Lazydocker — overview e operações comuns"
created: 2026-05-21
updated: 2026-05-21
type: concept
status: seedling
publish: true
fase: iniciado
tags:
  - terminal
  - tuis
  - lazydocker
  - iniciado
  - docker
aliases:
  - Lazydocker overview
---
```

- [ ] **Step 3: Escrever nota**

**TL;DR (callout):**
"Lazydocker é TUI Docker em Go por Jesse Duffield (mesmo autor de Lazygit). Painéis: Project (top), Containers / Images / Volumes / Networks (left), Main / Logs / Stats (right). `space` start/stop, `r` restart, `e` exec shell, `l` logs full screen. Vence pra dev local com docker-compose — dashboard ao vivo de CPU/mem por container. Substitui `docker ps`/`docker logs -f` pra workflow interativo."

**O que é / Como funciona** (H3s):

### Quem é Lazydocker
- Autor: Jesse Duffield
- Filosofia: mesma do Lazygit — keyboard-first, painéis, descoberta via `?`
- Foco: dev local; não substitui portainer pra remote/multi-host

### Layout dos painéis
Diagrama ASCII (adaptar ao layout real):
```
┌─Project──────────────────────────────┐
│ docker-compose status                 │
├─Containers──┬─Logs / Config / Stats──┤
│ ▶ api       │                         │
│ ▶ db        │   <output ao vivo>      │
│ ▶ cache     │                         │
├─Images──────┤                         │
│ alpine:3.19 │                         │
│ postgres:16 │                         │
├─Volumes─────┤                         │
│ vol-data    │                         │
├─Networks────┤                         │
│ bridge      │                         │
│ myproj_net  │                         │
└─────────────┴─────────────────────────┘
```

### Operações por painel — cheatsheet
| Painel | Tecla | Ação |
|---|---|---|
| Containers | `space` | Start/stop/restart conforme estado |
| Containers | `d` | Remove (com confirm) |
| Containers | `R` | Remove with volumes |
| Containers | `r` | Restart |
| Containers | `e` | Exec `/bin/sh` |
| Containers | `l` | Logs full screen |
| Containers | `enter` | Tab Config / Top / Logs |
| Images | `d` | Remove image |
| Images | `c` | Clean unused |
| Images | `s` | Run shell on image (one-off) |
| Volumes | `d` | Remove volume |
| Networks | `d` | Remove network |
| Global | `?` | Help |
| Global | `q` | Quit |

### Dashboard ao vivo
- Tab Stats em qualquer container mostra CPU/mem/network IO em tempo real (refresh ~1s)
- Útil pra detectar memory leak, runaway CPU

### Quando Lazydocker ganha
- Dev local com docker-compose stack
- Tail multi-container logs sem grep manual
- Debug crash loop (ver restart count)
- One-off shell em container pra inspect

### Quando `docker` CLI ainda ganha
- Scripts CI/CD
- Automação
- `docker build` complexo
- Network/volume create scripts

### Quando portainer/portainer-like ainda ganha
- Multi-host / cluster
- Equipe não-dev (UI gráfica)
- Gestão de Swarm/Kubernetes

**Na prática** (H3s):

### Instalação rápida
```bash
# Homebrew
brew install jesseduffield/lazydocker/lazydocker

# Manual binary
curl https://raw.githubusercontent.com/jesseduffield/lazydocker/master/scripts/install_update_linux.sh | bash

# Go install
go install github.com/jesseduffield/lazydocker@latest
```

### Primeira execução
```bash
cd ~/repos/myproj
lazydocker
```

Auto-detecta `docker-compose.yml` no cwd. Sem compose, mostra todos containers do daemon.

### Workflow comum (dev local)
1. `lazydocker` no diretório do projeto
2. `j`/`k` navega containers
3. `enter` em container → tab Logs (live tail)
4. `e` abre shell pra debug
5. Outra pane Zellij com editor; `r` no Lazydocker quando precisa restartar

**Armadilhas (≥5, 4 labels)**:

1. **`d` em Containers remove container, perde state local**
   - **Causa:** `d` é destrutivo; aceita com confirm rápido demais.
   - **Sintoma:** container some.
   - **Como detectar:** Lazydocker mostra menos containers que `docker ps -a`.
   - **Solução:** ler confirm dialog; usar `space` (stop) em vez de `d` se quer pausar.

2. **`R` remove com volumes — DATA LOSS**
   - **Causa:** confunde `r` (lowercase restart) com `R` (uppercase remove+volumes).
   - **Sintoma:** dados de banco no volume somem.
   - **Como detectar:** `docker volume ls` mostra volume ausente.
   - **Solução:** sempre conferir prompt; backup volume crítico antes (`docker run --rm -v vol:/d -v $(pwd):/b alpine tar cf /b/backup.tar /d`).

3. **Lazydocker não vê compose se rodado fora do dir**
   - **Causa:** auto-detect lê `./docker-compose.yml` (cwd).
   - **Sintoma:** containers aparecem soltos sem agrupamento.
   - **Como detectar:** painel Project mostra "no compose detected" ou similar.
   - **Solução:** `cd <dir-com-compose>` antes; ou usar `--compose-file <path>` (verificar flag exata).

4. **Logs muito longos quebram navegação**
   - **Causa:** tail enorme em container chatty (e.g. dev server com hot reload).
   - **Sintoma:** scroll lento, lazydocker travado.
   - **Como detectar:** observar UX.
   - **Solução:** `l` (logs fullscreen) + `gg`/`G` pra topo/fim; ou Truncar via `commandTemplates.logsViaSinceFlag` (nota 05).

5. **Exec em container Alpine sem `/bin/bash`**
   - **Causa:** `e` default usa `/bin/sh`; alguns workflows querem `bash`.
   - **Sintoma:** `/bin/bash: not found`.
   - **Como detectar:** testar `e`.
   - **Solução:** Alpine só tem `/bin/sh` (ash); pra bash usar custom command (nota 05) ou instalar bash na image.

**Em inglês (8-10 bullets bilíngues):**
Termos: container, image, volume, network, log, exec, dashboard, hot reload, health check, restart.

**Veja também:**
- `[[01 - Lazygit — overview e operações essenciais]]` — TUI irmã pra git
- `[[05 - Lazydocker — config, customização e workflow]]` — `~/.config/lazydocker/config.yml`
- `[[07 - Lazydocker — debugging avançado e docker-compose]]` — Magus
- `[[03-Dominios/Terminal/TUIs/index|MOC do galho]]`
- `[[03-Dominios/Terminal/index|Trilha Terminal]]`
- `[[Dicionário do Terminal#Lazydocker|lazydocker]]`, `[[Dicionário do Terminal#Docker-compose|docker-compose]]`, `[[Dicionário do Terminal#Exec (Lazydocker)|exec]]`

**Referências:**
- Lazydocker: https://github.com/jesseduffield/lazydocker
- Keybindings: https://github.com/jesseduffield/lazydocker/blob/master/docs/keybindings/Keybindings_en.md

- [ ] **Step 4: 3 verbetes**

```markdown
### Docker-compose
Orquestrador multi-container Docker. Define services em `docker-compose.yml` (ou `compose.yaml`). Comando: `docker compose up/down/logs/exec`. Lazydocker auto-detecta o arquivo no cwd e agrupa containers como services.

Veja também: [[02 - Lazydocker — overview e operações comuns]], [[07 - Lazydocker — debugging avançado e docker-compose]].

### Exec (Lazydocker)
Abrir shell interativo dentro de container rodando. Default key `e` (executa `/bin/sh`). Pra shell custom (`bash`, `zsh`), usar `customCommands` no config (nota 05) ou flag de imagem.

Veja também: [[02 - Lazydocker — overview e operações comuns]], [[05 - Lazydocker — config, customização e workflow]].

### Lazydocker
TUI Docker em Go por Jesse Duffield. Painéis: Project, Containers, Images, Volumes, Networks; com tabs Logs/Config/Stats por seleção. Auto-detecta `docker-compose.yml` no cwd. Config YAML em `~/.config/lazydocker/config.yml`.

Veja também: [[02 - Lazydocker — overview e operações comuns]], [[05 - Lazydocker — config, customização e workflow]].
```

- [ ] **Step 5: Validar**

```bash
test -f "03-Dominios/Terminal/TUIs/02 - Lazydocker — overview e operações comuns.md"
grep -c '\[\[' "03-Dominios/Terminal/TUIs/02 - Lazydocker — overview e operações comuns.md"
grep -E "^### (Docker-compose|Exec \(Lazydocker\)|Lazydocker)$" "03-Dominios/Terminal/Dicionário do Terminal.md"
```

- [ ] **Step 6: Commit**

```bash
git add "03-Dominios/Terminal/TUIs/02 - Lazydocker — overview e operações comuns.md" "03-Dominios/Terminal/Dicionário do Terminal.md"
git commit -m "feat(terminal-tuis): add nota 02 — Lazydocker overview"
```

---

## ✅ Checkpoint Iniciado

Após Task 4, 2 notas de Iniciado entregues.

---

## Task 5: Nota 03 — Lazygit: operações intermediárias (rebase, cherry-pick, hunks)

**Files:**
- Create: `03-Dominios/Terminal/TUIs/03 - Lazygit — operações intermediárias.md`
- Modify: `03-Dominios/Terminal/Dicionário do Terminal.md` (verbetes: Cherry-pick, Hunk, Interactive rebase, Reflog)

**Conteúdo-chave:** rebase interativo via UI, cherry-pick, staging por hunks, discard, reflog, merge conflicts.

- [ ] **Step 1: Pesquisa-âncora**

```
WebFetch: https://github.com/jesseduffield/lazygit/blob/master/docs/Rebasing.md
WebFetch: https://github.com/jesseduffield/lazygit/blob/master/docs/keybindings/Keybindings_en.md
```

Confirmar: atalhos exatos de rebase (`e` em commit, `K`/`J` reorder, `s` squash, `f` fixup, `d` drop, `m` continue), cherry-pick (`c` copy + `v` paste), staging por hunks (`enter` em arquivo + `space` em linha/hunk).

- [ ] **Step 2: Frontmatter**

```yaml
---
title: "Lazygit — operações intermediárias"
created: 2026-05-21
updated: 2026-05-21
type: concept
status: seedling
publish: true
fase: adepto
tags:
  - terminal
  - tuis
  - lazygit
  - adepto
  - git
aliases:
  - Lazygit rebase
  - Lazygit cherry-pick
---
```

- [ ] **Step 3: Escrever nota**

**TL;DR:**
"Lazygit transforma operações git delicadas em fluxos visuais: rebase interativo (`e` em commit no painel Commits), cherry-pick (`c` copy + `v` paste cross-branch), staging por hunks (`enter` em arquivo + `space` em linha), reflog (`Y`) pra recuperar branch deletada, merge conflicts auto-detectados com `enter` no arquivo abrindo conflict view com `space` pra escolher hunk."

**O que é / Como funciona** (H3s):

### Rebase interativo
- Painel Commits, `e` em commit (não o HEAD; um abaixo) → modo "Rebasing"
- Lista de commits aparece com letras de ação à esquerda
- Por commit:
  - `K`/`J` reorder up/down
  - `s` squash (combina com commit acima)
  - `f` fixup (squash sem editor de mensagem)
  - `d` drop (remove)
  - `e` edit (para pra editar)
  - `r` reword (só muda msg)
- `m` continue após resolver
- `esc` aborta

### Cherry-pick (cross-branch copy)
- Painel Commits da branch origem, `c` (copy) em commit → modo COPY
- Pode marcar múltiplos commits com `c` repetido (range com `shift+c`)
- Checkout branch destino (`space` em outra branch)
- `v` (paste) cola os commits copiados

### Staging por hunks
- Painel Files, `enter` em arquivo modificado → entra Diff inline view
- `j`/`k` navega linhas
- `space` stage/unstage hunk atual (bloco contíguo de `+/-`)
- `enter` mais profundo → seleciona linha individual; `space` stage linha
- `tab` alterna entre lado staged / unstaged
- `esc` volta pro painel Files

### Discard
- `d` em Files modificado → menu: discard changes / discard all
- Com confirm. **Não recuperável** via reflog (changes uncommitted não estão lá).

### Reflog
- `Y` (uppercase) em qualquer painel → tab Reflog (sob Branches)
- Mostra movimentações de HEAD: commits, checkouts, resets, rebases
- `space` em entry → checkout/reset to (depending on op)
- Útil pra recuperar branch deletada: encontrar último HEAD na branch, checkout

### Merge conflicts
- Após merge/rebase com conflito, painel Files mostra arquivos `UU`
- `enter` em arquivo `UU` → Conflict view com chunks ours/theirs
- `space` em chunk → escolhe ours (ou theirs, ou ambos)
- Após resolver: salva, volta pro painel Files; conflict cleared

**Na prática:**

### Workflow "limpar history antes de PR"
```text
1. Painel Commits, `e` no commit base do branch (mais antigo do trabalho)
2. Marca commits de wip/fix com `s` (squash) ou `f` (fixup)
3. `K`/`J` reorganiza ordem
4. `m` continue → Lazygit aplica
5. Push com `-f` (via custom command — nota 06 — ou git CLI)
```

### Workflow "trazer hotfix de master pra feature"
```text
1. Painel Branches → checkout master
2. Painel Commits → `c` em commit do hotfix
3. Painel Branches → checkout feature
4. Painel Commits → `v` paste
5. Conflicts? Resolver com flow descrito acima.
```

### Workflow "stage parcial pra commit atômico"
```text
1. Edita arquivo com 2 mudanças não-relacionadas
2. Painel Files → `enter` em arquivo
3. Hunk 1: `space` (stage)
4. Hunk 2: pula (não stage)
5. `esc` → painel Files (arquivo aparece como "modified + staged")
6. `c` commit → só staged vai
7. Resto do arquivo continua modified — commit separado depois
```

**Armadilhas (≥5, 4 labels)**:

1. **Rebase com commit já pushado vira force-push**
   - **Causa:** rebase altera SHA; remoto rejeita normal push.
   - **Sintoma:** `push` falha com "non-fast-forward".
   - **Como detectar:** após rebase, `p` falha.
   - **Solução:** force-push (use `--force-with-lease` via custom command — nota 06); confirmar que branch não é shared (main).

2. **Discard apaga changes não-recuperáveis**
   - **Causa:** `d` em Files com changes uncommitted; reflog não cobre uncommitted.
   - **Sintoma:** trabalho perdido.
   - **Como detectar:** `git reflog` não mostra; `git stash list` não mostra (se não stashed antes).
   - **Solução:** stash (`s`) antes de discardar como hábito.

3. **Cherry-pick com conflito sem resolver — Lazygit fica em estado "cherry-picking"**
   - **Causa:** `v` paste com conflito.
   - **Sintoma:** painel Files mostra `UU`; painel Commits mostra "cherry-pick in progress".
   - **Como detectar:** olhar status panel topo.
   - **Solução:** resolver conflict normalmente, ou `esc`/Abort no menu pra cancelar cherry-pick.

4. **Reflog não cobre tudo (e.g. uncommitted)**
   - **Causa:** reflog rastreia movimentos de HEAD, não working tree.
   - **Sintoma:** "discardei changes uncommitted, reflog não tem".
   - **Como detectar:** `git fsck --lost-found` pode achar blobs órfãos.
   - **Solução:** se ficou commit, está no reflog; se uncommitted, perdido (a menos que esteja no stash ou em backup local).

5. **Staging por hunks aceita o hunk inteiro mesmo querendo só uma linha**
   - **Causa:** `space` em modo hunk = hunk todo; pra linha precisa `enter` mais profundo.
   - **Sintoma:** mais linhas staged do que esperado.
   - **Como detectar:** `tab` pra lado staged confirma.
   - **Solução:** `enter` no hunk → modo line; `space` em linha; `esc` volta.

**Em inglês (8-10 bullets bilíngues):**
Termos: rebase, cherry-pick, hunk, stage, discard, reflog, conflict, squash, fixup, force-push.

**Veja também:**
- `[[01 - Lazygit — overview e operações essenciais]]` — pré-req
- `[[04 - Lazygit — config e customização]]` — `editPreset` pra conflict resolution externa
- `[[06 - Lazygit — operações avançadas]]` — bisect, customCommands
- `[[03-Dominios/Terminal/TUIs/index|MOC do galho]]`
- `[[03-Dominios/Terminal/index|Trilha Terminal]]`
- `[[Dicionário do Terminal#Cherry-pick|cherry-pick]]`, `[[Dicionário do Terminal#Hunk|hunk]]`, `[[Dicionário do Terminal#Interactive rebase|interactive rebase]]`, `[[Dicionário do Terminal#Reflog|reflog]]`

**Referências:**
- Lazygit Rebasing: https://github.com/jesseduffield/lazygit/blob/master/docs/Rebasing.md
- Lazygit Keybindings: https://github.com/jesseduffield/lazygit/blob/master/docs/keybindings/Keybindings_en.md

- [ ] **Step 4: 4 verbetes**

```markdown
### Cherry-pick
Copiar 1 ou mais commits de uma branch pra outra. No Lazygit: painel Commits, `c` (copy) na branch origem → checkout destino → `v` (paste). Conflitos são tratados como merge conflict normal.

Veja também: [[03 - Lazygit — operações intermediárias]].

### Hunk
Bloco contíguo de mudanças num diff git — várias linhas próximas marcadas como `+`/`-`. Lazygit permite stage hunk-por-hunk (`enter` + `space`) ou linha-por-linha (`enter` mais profundo). Diff tools chamam isso de "chunk" também.

Veja também: [[03 - Lazygit — operações intermediárias]].

### Interactive rebase
`git rebase -i <base>` com UI Lazygit. Painel Commits, `e` em commit base. Cada commit ganha letra de ação: `s` squash, `f` fixup, `d` drop, `e` edit, `r` reword. Reorder com `K`/`J`. `m` continua após resolver.

Veja também: [[03 - Lazygit — operações intermediárias]].

### Reflog
Log de movimentos de HEAD (commits, checkouts, resets, rebases). No Lazygit: `Y` em qualquer painel abre tab Reflog. Útil pra recuperar branch deletada ou desfazer reset acidental. Não cobre changes uncommitted (não há reflog do working tree).

Veja também: [[03 - Lazygit — operações intermediárias]].
```

- [ ] **Step 5: Validar**

```bash
test -f "03-Dominios/Terminal/TUIs/03 - Lazygit — operações intermediárias.md"
grep -c '\[\[' "03-Dominios/Terminal/TUIs/03 - Lazygit — operações intermediárias.md"
grep -E "^### (Cherry-pick|Hunk|Interactive rebase|Reflog)$" "03-Dominios/Terminal/Dicionário do Terminal.md"
```

- [ ] **Step 6: Commit**

```bash
git add "03-Dominios/Terminal/TUIs/03 - Lazygit — operações intermediárias.md" "03-Dominios/Terminal/Dicionário do Terminal.md"
git commit -m "feat(terminal-tuis): add nota 03 — Lazygit intermediário"
```

---

## Task 6: Nota 04 — Lazygit: config e customização (`config.yml`)

**Files:**
- Create: `03-Dominios/Terminal/TUIs/04 - Lazygit — config e customização.md`
- Modify: `03-Dominios/Terminal/Dicionário do Terminal.md` (verbete: Editor preset)

**Conteúdo-chave:** estrutura do `config.yml`, seções gui/git/os/keybinding/customCommands, theme custom, editPreset, versionar via dotfiles.

- [ ] **Step 1: Pesquisa-âncora**

```
WebFetch: https://github.com/jesseduffield/lazygit/blob/master/docs/Config.md
```

Confirmar: seções válidas, propriedades atuais, default values.

- [ ] **Step 2: Frontmatter**

```yaml
---
title: "Lazygit — config e customização"
created: 2026-05-21
updated: 2026-05-21
type: concept
status: seedling
publish: true
fase: adepto
tags:
  - terminal
  - tuis
  - lazygit
  - adepto
  - config
aliases:
  - Lazygit config
---
```

- [ ] **Step 3: Escrever nota**

**TL;DR:**
"Lazygit lê `~/.config/lazygit/config.yml` (YAML). Seções principais: `gui` (theme, scrollOff), `git` (paging, log args), `os` (editPreset), `keybinding` (rebind raro), `customCommands` (intro — profundo em nota 06). Theme custom usa cores hex/nome; `editPreset: \"nvim\"` integra com Neovim; mouse, ícones, statusBar tudo configurável. Versionar config nos dotfiles = setup repetível."

**O que é / Como funciona** (H3s):

### Local e formato
- Path: `~/.config/lazygit/config.yml` (XDG_CONFIG_HOME respeitado)
- Formato YAML; comentários com `#`
- Config sem arquivo = defaults
- Reload: Lazygit lê na startup; mudanças requerem restart (`q` + `lazygit`)

### Seções principais

#### `gui:`
- `theme:` — cores dos elementos (activeBorderColor, inactiveBorderColor, etc.)
- `showFileTree: true|false` — tree view vs flat list em Files
- `scrollOffMargin: 2` — linhas de buffer ao scroll
- `mouseEvents: true|false` — habilita clique
- `showIcons: true|false` — ícones nerd font em arquivos
- `language: "en"` — i18n

Exemplo:
```yaml
gui:
  theme:
    activeBorderColor:
      - "#74c7ec"
      - bold
    inactiveBorderColor:
      - "#7f849c"
  showFileTree: true
  showIcons: true
  mouseEvents: true
```

#### `git:`
- `paging.colorArg: "always"` — passa `--color=always` pra git
- `paging.useConfig: true` — usa `core.pager` do git
- `log.order: "topo-order"` — ordem de commits
- `log.showWholeGraph: true` — graph completo (slow em repos grandes)
- `pull.rebase: true` — default pull com rebase
- `branchLogCmd: "git log --graph ..."` — comando custom pra branch log

Exemplo:
```yaml
git:
  paging:
    colorArg: "always"
    useConfig: false
  log:
    order: "topo-order"
    showWholeGraph: true
```

#### `os:`
- `editPreset: "nvim" | "vim" | "vscode" | "helix" | "emacs"` — preset built-in
- `edit:` — comando custom: `{{filename}}` é placeholder
- `editAtLine:` — comando custom abrindo na linha: `{{filename}}`, `{{line}}`
- `open: "xdg-open {{filename}}"` — abrir arquivo no app default

Exemplo:
```yaml
os:
  editPreset: "nvim"
  # Alternativa custom:
  # edit: "nvim {{filename}}"
  # editAtLine: "nvim +{{line}} {{filename}}"
```

#### `keybinding:`
- Rebind raro (defaults são bons)
- Estrutura: `keybinding.<context>.<action>: <key>`
- Exemplo: `keybinding.universal.quit: "Q"` (caso `q` colida com outra coisa)

```yaml
keybinding:
  universal:
    quit: "q"
  # raramente necessário
```

#### `customCommands:` (intro)
Atalho YAML mapeando key → shell command. Cobertura profunda em nota 06.

Exemplo simples:
```yaml
customCommands:
  - key: "<C-r>"
    command: "git push --force-with-lease"
    context: "global"
    description: "Force-push with lease"
```

### Theme custom
```yaml
gui:
  theme:
    activeBorderColor:
      - "#a6e3a1"     # green nerdy
      - bold
    inactiveBorderColor: ["#585b70"]
    selectedLineBgColor: ["#313244"]
    optionsTextColor: ["#cdd6f4"]
```

Cores: nome (`green`, `red`, ...) ou hex (`#aabbcc`).

### Versionar config nos dotfiles
- Mover `~/.config/lazygit/config.yml` pra repo de dotfiles
- Symlink ou stow:
  ```bash
  ln -s ~/repos/dotfiles/lazygit/config.yml ~/.config/lazygit/config.yml
  ```
- Galho 5 (Dotfiles) cobre estratégias completas

**Na prática** (H3s):

### Setup mínimo recomendado
```yaml
# ~/.config/lazygit/config.yml
gui:
  showIcons: true
  showFileTree: true
git:
  paging:
    colorArg: "always"
  pull:
    rebase: true
os:
  editPreset: "nvim"
```

### Theme escuro custom (Catppuccin-ish)
```yaml
gui:
  theme:
    activeBorderColor: ["#a6e3a1", "bold"]
    inactiveBorderColor: ["#585b70"]
    optionsTextColor: ["#cdd6f4"]
    selectedLineBgColor: ["#313244"]
    cherryPickedCommitBgColor: ["#f5c2e7"]
    cherryPickedCommitFgColor: ["#1e1e2e"]
```

### Integração com Neovim em pane vizinho
- `editPreset: "nvim"` + galho 3 (Multiplexer) → `o` em arquivo no Lazygit abre Neovim no pane atual
- Pra abrir em pane vizinho do Zellij, usar custom edit command com `zellij action` (nota 07 do galho 3)

**Armadilhas (≥5, 4 labels)**:

1. **`paging.useConfig: true` causa output sem cor em Lazygit**
   - **Causa:** Lazygit confia no `core.pager` do git, que pode strip cores em pager externo.
   - **Sintoma:** diff sem cores.
   - **Como detectar:** comparar com `useConfig: false`.
   - **Solução:** `useConfig: false` + `colorArg: "always"`.

2. **`editPreset` errado → editor não abre**
   - **Causa:** preset name typo (`"neovim"` em vez de `"nvim"`).
   - **Sintoma:** `o` em arquivo não faz nada ou erro.
   - **Como detectar:** Lazygit log (debug mode).
   - **Solução:** conferir presets válidos no docs/Config.md; ou usar `edit:` custom.

3. **YAML indent errado quebra config inteiro**
   - **Causa:** YAML sensível a indent (2 espaços), copy-paste com tab.
   - **Sintoma:** Lazygit startup com erro de parse ou ignora config.
   - **Como detectar:** olhar bottom bar pra warning; ou `yq` valida (`yq . config.yml`).
   - **Solução:** sempre 2 spaces, nunca tab.

4. **`gui.theme` cor inválida**
   - **Causa:** hex sem `#` ou nome de cor inexistente.
   - **Sintoma:** elementos sem cor ou Lazygit não inicia.
   - **Como detectar:** comparar com exemplo do docs.
   - **Solução:** usar valores conhecidos (`green`, `red`, ...) ou hex válido `#aabbcc`.

5. **`customCommands` com `context` errado não dispara**
   - **Causa:** context define onde o keybinding aplica (`global`, `files`, `commits`, etc.); typo silencia.
   - **Sintoma:** custom command não responde ao key.
   - **Como detectar:** trocar pra `context: global` temporariamente; se funciona, era context.
   - **Solução:** consultar lista de contexts válidos em `docs/Custom_Command_Keybindings.md`.

**Em inglês (8-10 bullets bilíngues):**
Termos: config, theme, preset, keybinding, custom command, paging, scrollback, hex color, indent, parse.

**Veja também:**
- `[[01 - Lazygit — overview e operações essenciais]]` — pré-req
- `[[06 - Lazygit — operações avançadas]]` — customCommands profundo
- `[[03-Dominios/Terminal/Editor/index|Editor (Neovim)]]` — `editPreset: nvim`
- `[[03-Dominios/Terminal/TUIs/index|MOC do galho]]`
- `[[03-Dominios/Terminal/index|Trilha Terminal]]`
- `[[Dicionário do Terminal#Editor preset|editor preset]]`, `[[Dicionário do Terminal#Lazygit|lazygit]]`

**Referências:**
- Lazygit Config: https://github.com/jesseduffield/lazygit/blob/master/docs/Config.md

- [ ] **Step 4: 1 verbete**

```markdown
### Editor preset
Preset YAML do Lazygit (`os.editPreset`) que define como abrir arquivos no editor configurado. Built-ins: `nvim`, `vim`, `vscode`, `helix`, `emacs`. Pra editor custom usar `os.edit` / `os.editAtLine` com placeholders `{{filename}}` e `{{line}}`.

Veja também: [[04 - Lazygit — config e customização]].
```

- [ ] **Step 5: Validar**

```bash
test -f "03-Dominios/Terminal/TUIs/04 - Lazygit — config e customização.md"
grep -c '\[\[' "03-Dominios/Terminal/TUIs/04 - Lazygit — config e customização.md"
grep -E "^### Editor preset$" "03-Dominios/Terminal/Dicionário do Terminal.md"
```

- [ ] **Step 6: Commit**

```bash
git add "03-Dominios/Terminal/TUIs/04 - Lazygit — config e customização.md" "03-Dominios/Terminal/Dicionário do Terminal.md"
git commit -m "feat(terminal-tuis): add nota 04 — Lazygit config"
```

---

## Task 7: Nota 05 — Lazydocker: config, customização e workflow

**Files:**
- Create: `03-Dominios/Terminal/TUIs/05 - Lazydocker — config, customização e workflow.md`
- Modify: `03-Dominios/Terminal/Dicionário do Terminal.md` (sem verbetes novos; já temos Docker-compose, Exec, Lazydocker — referencia)

**Conteúdo-chave:** `~/.config/lazydocker/config.yml`, gui/commandTemplates/customCommands, workflow com docker-compose, podman alternative.

- [ ] **Step 1: Pesquisa-âncora**

```
WebFetch: https://github.com/jesseduffield/lazydocker/blob/master/docs/Config.md
WebFetch: https://github.com/jesseduffield/lazydocker/blob/master/docs/Custom_Commands.md
```

- [ ] **Step 2: Frontmatter**

```yaml
---
title: "Lazydocker — config, customização e workflow"
created: 2026-05-21
updated: 2026-05-21
type: concept
status: seedling
publish: true
fase: adepto
tags:
  - terminal
  - tuis
  - lazydocker
  - adepto
  - config
  - docker
aliases:
  - Lazydocker config
---
```

- [ ] **Step 3: Escrever nota**

**TL;DR:**
"Lazydocker lê `~/.config/lazydocker/config.yml`. Seções: `gui` (theme), `commandTemplates` (rebind `dockerCompose` pra podman/outros), `customCommands` (atalhos shell com placeholders `{{.Container.ID}}`). Workflow recomendado: Lazydocker rodando num pane Zellij ao lado do dev server; restart on demand. Auto-detecta `docker-compose.yml` no cwd."

**O que é / Como funciona** (H3s):

### Local e formato
- Path: `~/.config/lazydocker/config.yml`
- Formato YAML
- Reload requer restart

### Seções principais

#### `gui:`
- `theme:` cores (mesma ideia do Lazygit)
- `showAllContainers: true|false` — mostrar stopped também
- `language: "en"`

Exemplo:
```yaml
gui:
  theme:
    activeBorderColor:
      - "#a6e3a1"
      - bold
  showAllContainers: true
```

#### `commandTemplates:`
Rebind comandos internos. Útil pra:
- Substituir `docker` por `podman`
- Substituir `docker compose` v2 por `docker-compose` v1 (ou vice-versa)
- Adicionar flags default (e.g. `--no-color`)

```yaml
commandTemplates:
  dockerCompose: "docker compose"   # v2 (espaço); v1 seria "docker-compose"
  restartService: "{{ .DockerCompose }} restart {{ .Service.Name }}"
  up: "{{ .DockerCompose }} up -d"
```

Pra podman:
```yaml
commandTemplates:
  dockerCompose: "podman-compose"
```

#### `customCommands:`
Atalhos shell com placeholders Go template.

Exemplo: shell `bash` em vez de `/bin/sh`:
```yaml
customCommands:
  containers:
    - name: "bash"
      command: "docker exec -it {{ .Container.ID }} bash"
      serviceNames: []
      attach: true
```

Exemplo: backup volume:
```yaml
customCommands:
  volumes:
    - name: "backup"
      command: "docker run --rm -v {{ .Volume.Name }}:/v -v $(pwd):/b alpine tar czf /b/{{ .Volume.Name }}.tar.gz /v"
      attach: false
```

Placeholders disponíveis (verificar em Custom_Commands.md):
- `{{ .Container.ID }}`, `{{ .Container.Name }}`, `{{ .Container.Image }}`
- `{{ .Service.Name }}` (compose)
- `{{ .Image.ID }}`, `{{ .Image.Name }}`
- `{{ .Volume.Name }}`

#### `logs:`
- `timestamps: true|false`
- `since: "60m"` — só logs últimos 60 min
- `tail: "100"` — só últimas 100 linhas

```yaml
logs:
  timestamps: true
  since: "10m"
  tail: "500"
```

**Na prática** (H3s):

### Setup mínimo (podman-compose user)
```yaml
gui:
  showAllContainers: true
commandTemplates:
  dockerCompose: "podman-compose"
logs:
  timestamps: true
  since: "30m"
```

### Custom command: bash em vez de sh
```yaml
customCommands:
  containers:
    - name: "bash"
      command: "docker exec -it {{ .Container.ID }} bash || docker exec -it {{ .Container.ID }} sh"
      attach: true
```

(O `|| sh` fallback cobre imagens Alpine sem bash.)

### Workflow recomendado
- Pane Zellij com Lazydocker sempre visível
- Dev server num pane vizinho
- Lazydocker pra restart container quando config muda
- `enter` em container → Tab Logs (auto-tail)

### Auto-detect docker-compose
- Lazydocker no `cd` de projeto com `docker-compose.yml` → agrupa containers como services
- Mostra dependências (`depends_on`) e status agregado no painel Project

**Armadilhas (≥5, 4 labels)**:

1. **`commandTemplates.dockerCompose` desatualizado vs `docker compose` v2**
   - **Causa:** Docker Compose mudou de `docker-compose` (v1, com hífen) pra `docker compose` (v2, espaço); Lazydocker default pode estar com sintaxe antiga.
   - **Sintoma:** comandos compose falham com "docker-compose: command not found".
   - **Como detectar:** `docker compose version` (espaço) vs `docker-compose --version` (hífen).
   - **Solução:** definir explicitamente `dockerCompose: "docker compose"` no config.

2. **Custom command com placeholder errado**
   - **Causa:** typo em `{{ .Container.ID }}` (Go template é case-sensitive).
   - **Sintoma:** command falha ou string literal `<no value>` aparece.
   - **Como detectar:** rodar manualmente o command com sub `{{...}}` substituído.
   - **Solução:** consultar lista de placeholders em `Custom_Commands.md`.

3. **`attach: true` em command que não é interativo**
   - **Causa:** `attach: true` espera TTY; comandos one-shot terminam logo.
   - **Sintoma:** Lazydocker trava aguardando ENTER ou retorna imediato.
   - **Como detectar:** observar UX.
   - **Solução:** `attach: false` pra one-shot; `attach: true` só pra shell/REPL.

4. **Logs com `since` muito curto perde contexto**
   - **Causa:** `since: "1m"` corta logs históricos importantes.
   - **Sintoma:** logs vazios em containers com pouca atividade.
   - **Como detectar:** rodar `docker logs <container>` direto compara.
   - **Solução:** ajustar `since` pra `"24h"` ou remover (tail completo).

5. **YAML indent errado quebra config**
   - **Causa:** mesmo do Lazygit — tab em vez de spaces.
   - **Sintoma:** Lazydocker startup com erro ou ignora config.
   - **Como detectar:** `yq . ~/.config/lazydocker/config.yml`.
   - **Solução:** 2 spaces sempre.

**Em inglês (8-10 bullets):**
Termos: config, command template, placeholder, container, service, volume, logs, timestamp, tail, attach.

**Veja também:**
- `[[02 - Lazydocker — overview e operações comuns]]` — pré-req
- `[[07 - Lazydocker — debugging avançado e docker-compose]]` — Magus
- `[[03-Dominios/Terminal/TUIs/index|MOC do galho]]`
- `[[03-Dominios/Terminal/index|Trilha Terminal]]`
- `[[Dicionário do Terminal#Docker-compose|docker-compose]]`, `[[Dicionário do Terminal#Exec (Lazydocker)|exec]]`, `[[Dicionário do Terminal#Lazydocker|lazydocker]]`

**Referências:**
- Lazydocker Config: https://github.com/jesseduffield/lazydocker/blob/master/docs/Config.md
- Custom Commands: https://github.com/jesseduffield/lazydocker/blob/master/docs/Custom_Commands.md

- [ ] **Step 4: Sem verbetes novos** — apenas referencia existentes (Docker-compose, Exec, Lazydocker da nota 02).

- [ ] **Step 5: Validar**

```bash
test -f "03-Dominios/Terminal/TUIs/05 - Lazydocker — config, customização e workflow.md"
grep -c '\[\[' "03-Dominios/Terminal/TUIs/05 - Lazydocker — config, customização e workflow.md"
```

Esperado: ≥7 wikilinks.

- [ ] **Step 6: Commit**

```bash
git add "03-Dominios/Terminal/TUIs/05 - Lazydocker — config, customização e workflow.md"
git commit -m "feat(terminal-tuis): add nota 05 — Lazydocker config"
```

---

## ✅ Checkpoint Adepto

Após Task 7, 3 notas Adepto entregues. Total no galho: 5 notas + MOC.

---

## Task 8: Nota 06 — Lazygit: operações avançadas (bisect, custom commands, hooks)

**Files:**
- Create: `03-Dominios/Terminal/TUIs/06 - Lazygit — operações avançadas.md`
- Modify: `03-Dominios/Terminal/Dicionário do Terminal.md` (verbetes: Bisect (Lazygit), Custom command (Lazygit), Worktree)

**Conteúdo-chave:** bisect via UI, customCommands schema completo + exemplos verificáveis, git hooks (pre-commit framework), worktrees no Lazygit.

- [ ] **Step 1: Pesquisa-âncora**

```
WebFetch: https://github.com/jesseduffield/lazygit/blob/master/docs/Custom_Command_Keybindings.md
WebFetch: https://pre-commit.com/
WebFetch: https://github.com/jesseduffield/lazygit/blob/master/docs/Custom_Pagers.md
```

Confirmar: schema YAML de customCommands (key, command, context, description, prompts, output), contexts válidos (`global`, `files`, `commits`, `branches`, etc.), placeholders Go template.

- [ ] **Step 2: Frontmatter**

```yaml
---
title: "Lazygit — operações avançadas"
created: 2026-05-21
updated: 2026-05-21
type: concept
status: seedling
publish: true
fase: magus
tags:
  - terminal
  - tuis
  - lazygit
  - magus
  - custom-commands
  - hooks
aliases:
  - Lazygit bisect
  - Lazygit customCommands
---
```

- [ ] **Step 3: Escrever nota**

**TL;DR:**
"Magus em Lazygit: bisect via UI (painel Commits, `b`), customCommands em YAML (`key`, `command`, `context`, `prompts`), git hooks nativos respeitados (pre-commit framework é o padrão), worktrees (`w` no painel Branches). Custom commands viabilizam force-push with lease, conventional commits prompt, fast PR creation — atalhos próprios que viram parte do workflow."

**O que é / Como funciona** (H3s):

### Bisect — encontrar regressão
- Painel Commits, `b` em um commit conhecidamente good → Lazygit pergunta good/bad
- Marcar atual como bad, ou escolher commit good
- Lazygit checkout commit do meio → você testa
- Marca `good`/`bad` → próximo commit do meio
- Em ~log2(N) commits identifica a regressão
- `B` pra abort

### customCommands — schema completo
```yaml
customCommands:
  - key: "<key>"
    command: "<shell command>"
    context: "<context>"
    description: "<descrição opcional>"
    output: "<output_mode>"     # popup | log | none | terminal
    prompts:
      - type: "<prompt_type>"   # input | menu | confirm | menuFromCommand
        title: "<title>"
        options:                # pra menu
          - name: "..."
            value: "..."
            description: "..."
```

Contexts comuns:
- `global` — qualquer painel
- `files` — painel Files
- `commits` — painel Commits
- `branches` — painel Branches
- `localBranches`, `remoteBranches`
- `stash`

Placeholders em command (Go template):
- `{{ .SelectedFile.Name }}` (em context `files`)
- `{{ .SelectedLocalCommit.Sha }}`
- `{{ .SelectedLocalBranch.Name }}`
- `{{ .CheckedOutBranch.Name }}`
- `{{ .Form.<field> }}` (output de prompts)

### Exemplos verificáveis

#### Force-push with lease (segurança)
```yaml
customCommands:
  - key: "F"
    command: "git push --force-with-lease origin {{ .CheckedOutBranch.Name }}"
    context: "global"
    description: "Force-push with lease"
    output: "log"
    prompts:
      - type: "confirm"
        title: "Force-push with lease em {{ .CheckedOutBranch.Name }}?"
```

#### Conventional commit prefix
```yaml
customCommands:
  - key: "<C-v>"
    command: "git commit -m \"{{.Form.Type}}: {{.Form.Subject}}\""
    context: "files"
    description: "Conventional commit"
    output: "log"
    prompts:
      - type: "menu"
        key: "Type"
        title: "Tipo"
        options:
          - { name: "feat",     value: "feat",     description: "Nova feature" }
          - { name: "fix",      value: "fix",      description: "Bug fix" }
          - { name: "docs",     value: "docs",     description: "Docs" }
          - { name: "refactor", value: "refactor", description: "Refactor" }
          - { name: "test",     value: "test",     description: "Test" }
          - { name: "chore",    value: "chore",    description: "Chore" }
      - type: "input"
        key: "Subject"
        title: "Subject"
```

#### Fast PR creation (com gh CLI)
```yaml
customCommands:
  - key: "<C-p>"
    command: "gh pr create --base main --head {{ .CheckedOutBranch.Name }} --fill"
    context: "global"
    description: "Create PR pra main"
    output: "log"
```

#### Custom branch creation com prefixo
```yaml
customCommands:
  - key: "<C-n>"
    command: "git checkout -b {{.Form.Type}}/{{.Form.Name}}"
    context: "localBranches"
    description: "New typed branch"
    prompts:
      - type: "menu"
        key: "Type"
        title: "Tipo"
        options:
          - { name: "feat", value: "feat" }
          - { name: "fix",  value: "fix" }
          - { name: "exp",  value: "exp" }
      - type: "input"
        key: "Name"
        title: "Nome (kebab-case)"
```

### Git hooks (não-Lazygit-specific)
Lazygit respeita git hooks nativos (`.git/hooks/pre-commit`, `commit-msg`, etc.). Não tem hooks próprios extensíveis.

**Pre-commit framework** (https://pre-commit.com/) é o padrão moderno:
```bash
# Instalar
pipx install pre-commit

# No repo, criar .pre-commit-config.yaml
cat > .pre-commit-config.yaml <<'EOF'
repos:
  - repo: https://github.com/pre-commit/pre-commit-hooks
    rev: v4.5.0
    hooks:
      - id: trailing-whitespace
      - id: end-of-file-fixer
      - id: check-yaml
EOF

# Install hooks no .git
pre-commit install
```

Após isso, `c` no Lazygit dispara pre-commit ao commitar. Se falhar, Lazygit mostra erro e bloqueia.

### Worktrees no Lazygit
- `w` no painel Branches → painel Worktrees
- Listar worktrees existentes (`git worktree list`)
- `n` em Worktrees → criar novo (branch + path)
- `space` em worktree → switch (Lazygit muda pra esse worktree)
- Útil pra trabalhar em 2+ branches simultaneamente sem stash

**Na prática** (H3s):

### Workflow bisect
```text
1. main quebrou; commit antigo (3 meses atrás) sabidamente funcionava
2. Painel Commits → encontra commit antigo good
3. `b` nele → escolhe "Mark as good"
4. Lazygit checkout commit do meio
5. Testar (rodar testes, rodar app)
6. `b` no commit atual → "Bad" ou "Good"
7. Lazygit converge em ~7 iterações pra repo com 100 commits suspeitos
8. Resultado: commit culpado identificado
```

### Workflow custom commands no dia-a-dia
- `F` (force-push with lease) em vez de digitar
- `<C-v>` (conventional commit) em vez de pensar prefixo
- `<C-p>` (PR creation) em vez de browser
- Cada custom command é YAML versionado nos dotfiles

### Workflow worktree pra hotfix
```text
1. Trabalhando em feature/auth, dev server rodando
2. Bug em prod precisa fix urgente
3. Painel Branches → `w` → Worktrees
4. `n` → cria worktree em ../myproj-hotfix com branch hotfix/security
5. Lazygit abre nele
6. Fix + push
7. Volta pro worktree principal (sem stash, sem checkout)
```

**Armadilhas (≥5, 4 labels)**:

1. **Bisect com testes não-determinísticos**
   - **Causa:** flaky tests dão sinais inconsistentes good/bad.
   - **Sintoma:** bisect aponta commit que não é culpado real.
   - **Como detectar:** rerun bisect dá resultado diferente.
   - **Solução:** rodar teste 3-5x em cada commit antes de marcar; ou `git bisect skip` pra commits ambíguos.

2. **customCommand sem `output` deixa em popup oculto**
   - **Causa:** default output pode esconder output (depende da versão).
   - **Sintoma:** command roda mas não vê resultado.
   - **Como detectar:** `git log` confirma commit foi feito mesmo sem output visível.
   - **Solução:** `output: "log"` ou `output: "popup"` explícito.

3. **`{{ .Form.Subject }}` com aspas duplas literais**
   - **Causa:** subject com `"` quebra o shell command.
   - **Sintoma:** commit message truncada ou erro shell.
   - **Como detectar:** testar com input contendo `"`.
   - **Solução:** escape com `printf "%q"` ou heredoc dentro do command; alternativamente, sanitizar input.

4. **Worktree em pasta que vira filha do repo**
   - **Causa:** `git worktree add ./hotfix` (mesmo dir do repo) cria worktree DENTRO do repo, confuso.
   - **Sintoma:** Lazygit no repo principal vê arquivos do worktree filho.
   - **Como detectar:** `git status` mostra dir extra.
   - **Solução:** sempre criar worktree em path SIBLING (`../myproj-hotfix`), não filho.

5. **pre-commit framework lento bloqueia `c`**
   - **Causa:** hooks pesados (linter inteiro do repo, tests).
   - **Sintoma:** Lazygit congela ao commitar.
   - **Como detectar:** rodar `pre-commit run --all-files` direto vê o tempo.
   - **Solução:** hook só em arquivos staged (`stages: [pre-commit]` default); usar `pre-commit run --files` em alternativa de speed.

**Em inglês (8-10 bullets):**
Termos: bisect, regression, custom command, prompt, placeholder, hook, worktree, force-push, lease, framework.

**Veja também:**
- `[[03 - Lazygit — operações intermediárias]]` — pré-req (rebase, cherry-pick)
- `[[04 - Lazygit — config e customização]]` — onde customCommands vivem
- `[[03-Dominios/Terminal/TUIs/index|MOC do galho]]`
- `[[03-Dominios/Terminal/index|Trilha Terminal]]`
- `[[Dicionário do Terminal#Bisect (Lazygit)|bisect]]`, `[[Dicionário do Terminal#Custom command (Lazygit)|custom command]]`, `[[Dicionário do Terminal#Worktree|worktree]]`

**Referências:**
- Custom Command Keybindings: https://github.com/jesseduffield/lazygit/blob/master/docs/Custom_Command_Keybindings.md
- Pre-commit framework: https://pre-commit.com/
- git-worktree: https://git-scm.com/docs/git-worktree

- [ ] **Step 4: 3 verbetes**

```markdown
### Bisect (Lazygit)
UI visual do `git bisect` no Lazygit. Painel Commits, `b` em commit → escolhe Good/Bad. Lazygit checkout o commit do meio; você testa; marca; em ~log2(N) iterações identifica a regressão. `B` aborta.

Veja também: [[06 - Lazygit — operações avançadas]].

### Custom command (Lazygit)
Atalho YAML no `config.yml` mapeando key → shell command. Schema: `key`, `command`, `context`, `description`, `output`, `prompts`. Placeholders Go template como `{{ .CheckedOutBranch.Name }}`. Viabiliza force-push with lease, conventional commits, fast PR creation, branch creation com prefixo.

Veja também: [[06 - Lazygit — operações avançadas]], [[04 - Lazygit — config e customização]].

### Worktree
Múltiplos working dirs do mesmo repo git, cada um em branch própria. Comando: `git worktree add <path> <branch>`. No Lazygit: `w` em Branches abre painel Worktrees pra criar/listar/switch. Útil pra hotfix sem stash do trabalho atual.

Veja também: [[06 - Lazygit — operações avançadas]].
```

- [ ] **Step 5: Validar**

```bash
test -f "03-Dominios/Terminal/TUIs/06 - Lazygit — operações avançadas.md"
grep -c '\[\[' "03-Dominios/Terminal/TUIs/06 - Lazygit — operações avançadas.md"
grep -E "^### (Bisect \(Lazygit\)|Custom command \(Lazygit\)|Worktree)$" "03-Dominios/Terminal/Dicionário do Terminal.md"
```

- [ ] **Step 6: Commit**

```bash
git add "03-Dominios/Terminal/TUIs/06 - Lazygit — operações avançadas.md" "03-Dominios/Terminal/Dicionário do Terminal.md"
git commit -m "feat(terminal-tuis): add nota 06 — Lazygit avançado"
```

---

## Task 9: Nota 07 — Lazydocker: debugging avançado e docker-compose

**Files:**
- Create: `03-Dominios/Terminal/TUIs/07 - Lazydocker — debugging avançado e docker-compose.md`
- (Sem verbetes novos no Dicionário.)

**Conteúdo-chave:** stack docker-compose no Lazydocker, inspect verboso, logs filter, exec custom, debug crash loop, health checks, compose overrides.

- [ ] **Step 1: Pesquisa-âncora**

```
WebFetch: https://github.com/jesseduffield/lazydocker/blob/master/docs/Config.md
WebFetch: https://docs.docker.com/compose/
WebFetch: https://docs.docker.com/engine/reference/builder/#healthcheck
```

- [ ] **Step 2: Frontmatter**

```yaml
---
title: "Lazydocker — debugging avançado e docker-compose"
created: 2026-05-21
updated: 2026-05-21
type: concept
status: seedling
publish: true
fase: magus
tags:
  - terminal
  - tuis
  - lazydocker
  - magus
  - debugging
  - docker-compose
aliases:
  - Lazydocker debugging
---
```

- [ ] **Step 3: Escrever nota**

**TL;DR:**
"Magus em Lazydocker: stack docker-compose mostrado como grupo com dependências; `enter` em container abre Config (env vars, ports, mounts), Top (processes), Stats (CPU/mem live). Logs filter via regex e tail. Exec custom via customCommand pra shell preferido. Debug crash loop: olhar restart count + tail logs + Config. Health checks visíveis. Compose overrides (`docker-compose.override.yml`) auto-carregados."

**O que é / Como funciona** (H3s):

### Stack docker-compose no Lazydocker
- Painel Project (top) mostra "compose detected" se há `docker-compose.yml`/`compose.yaml` no cwd
- Containers agrupados por service name (`api`, `db`, `cache`, ...)
- Status agregado: número de containers up/down por service
- `enter` em service → expande containers daquele service

### Inspect verboso
- `enter` em container individual → tabs:
  - **Logs** — tail live
  - **Config** — JSON inspect (env vars, exposed ports, mounts, networks)
  - **Top** — `docker top` (processos rodando)
  - **Stats** — CPU/mem live (~1s refresh)
  - **(outros)** — depende da versão (Image config, Restart Logs)

### Logs filter e tail
- Tab Logs em container → tail automático
- `l` (lowercase) em container → fullscreen
- Em fullscreen: navegação Vim-like (`j`/`k`, `gg`/`G`, `/regex` busca — verificar atalho)
- Config global: `logs.timestamps`, `logs.since`, `logs.tail` controlam buffer

### Exec custom — shell preferido
Default `e` usa `/bin/sh`. Pra bash/zsh/etc., usar customCommand.

Exemplo com fallback (alpine fix):
```yaml
customCommands:
  containers:
    - name: "bash-or-sh"
      command: "docker exec -it {{ .Container.ID }} bash 2>/dev/null || docker exec -it {{ .Container.ID }} sh"
      attach: true
```

### Debug crash loop
1. Container com restart count > 0 (visível no painel Containers)
2. `enter` → tab Logs → ver último output antes do crash
3. Tab Config → conferir env vars / commando
4. Tab Top → ver se processo está zumbi
5. Restart manual (`r`) ou stop+remove+up

### Health checks
- `HEALTHCHECK` no Dockerfile dispara check periódico
- Lazydocker exibe status na coluna do container: `(healthy)`, `(unhealthy)`, `(starting)`
- Container `unhealthy` é alertado visualmente
- Tab Inspect → "Health" → último check, próximo intervalo, count de falhas

### Compose overrides
- Docker Compose auto-carrega `docker-compose.override.yml` ao lado de `docker-compose.yml`
- Lazydocker respeita (porque usa `docker compose` por trás)
- Pra ver merged config: `docker compose config` (CLI) — Lazydocker pode ter atalho ou requer CLI direto

**Na prática** (H3s):

### Workflow "stack dev local não sobe"
```text
1. `lazydocker` em diretório com docker-compose.yml
2. Painel Project mostra services
3. Service `db` está restart loop (count 5+)
4. `enter` em container db → tab Logs
5. Vê erro: "FATAL: database 'app' does not exist"
6. Custom command pra criar DB:
   docker exec -it <pg> psql -U postgres -c "CREATE DATABASE app;"
7. Service `db` healthy → outros services sobem
```

### Workflow "debug HTTP no API container"
```text
1. Container api up mas requests retornam 500
2. `enter` → tab Logs → ver stack trace
3. Tab Config → confirma env var `DATABASE_URL` correta
4. `e` (exec) → curl localhost interno: `curl http://localhost:3000/health`
5. Identifica problema no app
```

### Workflow "limpar imagens órfãs após muito dev"
```text
1. `lazydocker`
2. Painel Images
3. `c` (clean unused) — confirma
4. Liberou ~5GB
```

### Workflow "subir override pra teste local"
```text
1. Criar docker-compose.override.yml com:
   services:
     api:
       environment:
         DEBUG: "true"
       ports:
         - "3001:3000"
2. `docker compose up -d` (ou via custom command no Lazydocker)
3. Lazydocker mostra api com override aplicado
```

**Armadilhas (≥5, 4 labels)**:

1. **Lazydocker fora do dir de compose**
   - **Causa:** auto-detect lê cwd; sem compose.yml, mostra containers soltos.
   - **Sintoma:** containers não agrupados por service.
   - **Como detectar:** painel Project não mostra service tree.
   - **Solução:** `cd <dir>` antes; ou flag `--compose-file` (verificar disponibilidade).

2. **Container unhealthy sem health check definido aparece como "running"**
   - **Causa:** sem `HEALTHCHECK` no Dockerfile, Docker não monitora.
   - **Sintoma:** container responde 5xx mas Lazydocker mostra "running" verde.
   - **Como detectar:** `docker inspect <container> | jq '.[].State.Health'` retorna null.
   - **Solução:** adicionar `HEALTHCHECK` no Dockerfile ou `healthcheck:` no compose.

3. **Logs filter regex case-sensitive**
   - **Causa:** Lazydocker logs search usa regex sensível a case por default.
   - **Sintoma:** "/Error" não acha "error".
   - **Como detectar:** comparar count com `docker logs <c> | grep -i error | wc -l`.
   - **Solução:** prefixar com `(?i)` no regex; ou conferir config.

4. **Restart count reseta após `lazydocker` restart**
   - **Causa:** Lazydocker mostra restart count do daemon Docker; restart manual de container reseta.
   - **Sintoma:** count que era 5 vira 0 após você restartar.
   - **Como detectar:** óbvio.
   - **Solução:** ler `docker inspect <c> | jq '.[].RestartCount'` se quiser valor agregado; mas note que Docker reseta também em alguns cenários.

5. **Compose `depends_on` sem `condition: service_healthy` falha silenciosa**
   - **Causa:** `depends_on: [db]` espera só start, não healthy.
   - **Sintoma:** api sobe antes do db estar pronto; crash loop.
   - **Como detectar:** comparar timing de logs api vs db.
   - **Solução:** `depends_on: db: { condition: service_healthy }` no compose; e db ter HEALTHCHECK.

**Em inglês (8-10 bullets):**
Termos: stack, service, dependency, health check, inspect, override, regex, restart loop, daemon, ephemeral.

**Veja também:**
- `[[02 - Lazydocker — overview e operações comuns]]` — pré-req
- `[[05 - Lazydocker — config, customização e workflow]]` — customCommands
- `[[03-Dominios/Terminal/TUIs/index|MOC do galho]]`
- `[[03-Dominios/Terminal/index|Trilha Terminal]]`
- `[[Dicionário do Terminal#Docker-compose|docker-compose]]`, `[[Dicionário do Terminal#Exec (Lazydocker)|exec]]`, `[[Dicionário do Terminal#Lazydocker|lazydocker]]`

**Referências:**
- Lazydocker: https://github.com/jesseduffield/lazydocker
- Docker Compose: https://docs.docker.com/compose/
- HEALTHCHECK: https://docs.docker.com/engine/reference/builder/#healthcheck

- [ ] **Step 4: Sem verbetes novos.**

- [ ] **Step 5: Validar**

```bash
test -f "03-Dominios/Terminal/TUIs/07 - Lazydocker — debugging avançado e docker-compose.md"
grep -c '\[\[' "03-Dominios/Terminal/TUIs/07 - Lazydocker — debugging avançado e docker-compose.md"
```

- [ ] **Step 6: Commit**

```bash
git add "03-Dominios/Terminal/TUIs/07 - Lazydocker — debugging avançado e docker-compose.md"
git commit -m "feat(terminal-tuis): add nota 07 — Lazydocker debugging + docker-compose"
```

---

## ✅ Checkpoint Magus

Após Task 9, 7 notas escritas.

---

## Task 10: Pass final no MOC do galho

**Files:**
- Modify: `03-Dominios/Terminal/TUIs/index.md`

- [ ] **Step 1: Substituir placeholders de versão**

Use Edit:

`old_string`:
```markdown
- **Lazygit:** `<VERSAO_LAZYGIT>` (capturada no pré-flight)
- **Lazydocker:** `<VERSAO_LAZYDOCKER>` (capturada no pré-flight)
```

`new_string` (substituir pelos valores capturados em Task 0):
```markdown
- **Lazygit:** <VERSAO_REAL_LAZYGIT>
- **Lazydocker:** <VERSAO_REAL_LAZYDOCKER>
```

- [ ] **Step 2: Confirmar wikilinks**

```bash
for n in "01 - Lazygit — overview e operações essenciais" "02 - Lazydocker — overview e operações comuns" "03 - Lazygit — operações intermediárias" "04 - Lazygit — config e customização" "05 - Lazydocker — config, customização e workflow" "06 - Lazygit — operações avançadas" "07 - Lazydocker — debugging avançado e docker-compose"; do
  test -f "03-Dominios/Terminal/TUIs/${n}.md" && echo "ok: $n" || echo "FALTA: $n"
done
```

Esperado: 7 `ok:`.

- [ ] **Step 3: Commit**

```bash
git add "03-Dominios/Terminal/TUIs/index.md"
git commit -m "$(cat <<'EOF'
docs(terminal-tuis): pass final no MOC do galho

Substitui placeholders <VERSAO_*> pelas versões reais capturadas no
pré-flight. Confirma que todos os 7 wikilinks de notas estão ativos.
EOF
)"
```

---

## Task 11: Pass final no Dicionário do Terminal

**Files:**
- Modify: `03-Dominios/Terminal/Dicionário do Terminal.md`

- [ ] **Step 1: Listar verbetes do bloco**

```bash
awk '/^## TUIs de Dev \/ Lazygit \/ Lazydocker$/{f=1; next} /^## /{f=0} f && /^### /' "03-Dominios/Terminal/Dicionário do Terminal.md"
```

Verbetes esperados (14) em ordem alfabética case-insensitive:
1. Bisect (Lazygit)
2. Cherry-pick
3. Command log
4. Custom command (Lazygit)
5. Docker-compose
6. Editor preset
7. Exec (Lazydocker)
8. Hunk
9. Interactive rebase
10. Lazydocker
11. Lazygit
12. Reflog
13. TUI
14. Worktree

- [ ] **Step 2: Reordenar se necessário**

Use Edit pra mover blocos fora de ordem. Cada verbete = `### Nome` + corpo + linha vazia + `Veja também:` + linha vazia.

- [ ] **Step 3: Confirmar "Veja também" em cada verbete**

```bash
awk '/^## TUIs de Dev \/ Lazygit \/ Lazydocker$/{f=1; next} /^## /{f=0}
     f && /^### / { v=$0; getline; getline; while(NF==0) getline; if ($0 !~ /^Veja também:/) print v " — sem Veja também" }' \
  "03-Dominios/Terminal/Dicionário do Terminal.md"
```

Esperado: nenhum output.

- [ ] **Step 4: Contagem**

```bash
awk '/^## TUIs de Dev \/ Lazygit \/ Lazydocker$/{f=1; next} /^## /{f=0} f && /^### /' "03-Dominios/Terminal/Dicionário do Terminal.md" | wc -l
```

Esperado: 14.

- [ ] **Step 5: Commit (se houve mudança)**

```bash
git status --short "03-Dominios/Terminal/Dicionário do Terminal.md"
```

Se modificado:
```bash
git add "03-Dominios/Terminal/Dicionário do Terminal.md"
git commit -m "$(cat <<'EOF'
docs(terminal): pass final no Dicionário (bloco TUIs de Dev / Lazygit / Lazydocker)

Garante ordem alfabética case-insensitive no bloco; cada verbete tem
Veja também. Contagem final: 14 verbetes novos.
EOF
)"
```

Sem mudanças = pular commit.

---

## Task 12: Atualizar tronco — ativar wikilink do TUIs

**Files:**
- Modify: `03-Dominios/Terminal/index.md`

- [ ] **Step 1: Edit tronco**

`old_string`:
```markdown
- TUIs de Dev — galho 4 (planejado): Lazygit, Lazydocker
```

`new_string`:
```markdown
- [[03-Dominios/Terminal/TUIs/index|TUIs de Dev]] — galho 4: Lazygit + Lazydocker (operações, config, debugging)
```

- [ ] **Step 2: `updated:` do tronco**

Edit pra `updated: 2026-05-21` se já não estiver.

- [ ] **Step 3: Confirmar**

```bash
grep -n "TUIs" "03-Dominios/Terminal/index.md"
```

Esperado: wikilink ativo aparece; `(planejado)` desaparece.

- [ ] **Step 4: Commit**

```bash
git add "03-Dominios/Terminal/index.md"
git commit -m "$(cat <<'EOF'
feat(terminal): tronco com wikilink ativo pro galho 4 (TUIs de Dev)

Substitui bullet "TUIs de Dev (planejado)" por wikilink ativo
[[03-Dominios/Terminal/TUIs/index|TUIs de Dev]] após entrega do galho 4.
EOF
)"
```

---

## Task 13: Validação final

**Files:**
- (nenhum)

- [ ] **Step 1: Verificar wikilinks**

```bash
python3 .agents/skills/verificar-wikilinks/scripts/check_wikilinks.py "03-Dominios/Terminal/TUIs/" --respect-public-only
```

Lê o JSON em `/tmp/wikilinks-report-*.json`. Esperado: `links_broken: 0`.

- [ ] **Step 2: Sanity check**

```bash
ls -1 "03-Dominios/Terminal/TUIs/" | sort
git log --oneline | head -16
git log --format="%H %s" -16 | grep -i "co-authored" || echo "ok: nenhum commit com Co-Authored-By"
```

Esperado:
- 8 arquivos (7 notas + index)
- ~13-16 commits do galho
- Nenhum Co-Authored-By

- [ ] **Step 3: Contagem final do Dicionário**

```bash
awk '/^## TUIs de Dev \/ Lazygit \/ Lazydocker$/{f=1; next} /^## /{f=0} f && /^### /' "03-Dominios/Terminal/Dicionário do Terminal.md" | wc -l
```

Esperado: 14.

- [ ] **Step 4: Final cross-task review (opcional mas recomendado)**

Dispatch reviewer subagent pra revisar o galho inteiro buscando inconsistências cross-task (mesmo padrão dos galhos 2 e 3).

- [ ] **Step 5: Declarar galho fechado**

Reporte:
- 7 notas + MOC entregues
- 14 verbetes no Dicionário
- Tronco com wikilink ativo
- Zero wikilinks broken
- Zero commits com Co-Authored-By
- Próximo galho (5 — Dotfiles) quando o usuário quiser

---

## Self-review do plano

**Spec coverage:** todas seções 3.1-3.4, 4.1-4.3, 5 → tasks atribuídas. Critério de pronto seção 8 → Tasks 10-13.

**Placeholder scan:** placeholders `<VERSAO_LAZYGIT>`, `<VERSAO_LAZYDOCKER>`, `<VERSAO_REAL_*>` são intencionais (resolvidos no Task 10 com valores capturados em Task 0). Nenhum TBD/TODO no corpo dos specs de notas.

**Type consistency:** nomes de arquivos consistentes (Tasks 1, 3-9, 10). Verbetes consistentes (Tasks 3-8, 11).

**Cross-galho:** Task 6 (nota 04) referencia galho 1 (Editor) via wikilink ao MOC dele — `03-Dominios/Terminal/Editor/index.md` existe (verificado em galho 3).

Pronto pra execução.
